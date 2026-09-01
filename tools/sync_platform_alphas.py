# -*- coding: utf-8 -*-
"""sync_platform_alphas.py — 平台 alpha → 本地 DB `alphas` 表对齐（根治"本地状态陈旧/缺失"）。

背景（2026-09-01）：本地 alphas 表与平台长期不同步，导致三类误判：
  ① 平台已 ACTIVE、本地**完全没有记录**（历史战役产物，如 KOR 5 颗）→ 被当成"待提交"；
  ② 平台已提交、本地 `status` 列仍标 UNSUBMITTED（列陈旧）→ 判"未提交"必须看
     `platform_status` / `date_submitted`；
  ③ 本地记录的 sharpe/fitness/日期 与平台不一致。
本工具以**平台为唯一权威**做幂等对齐。

设计：
  1. 一次全量拉取平台 alpha 快照（~10000 颗，约 3-5 分钟，节流+429 退避），
     缓存到 research-data/platform_alphas_snapshot_<YYYYMMDD>.json，当天再跑直接读缓存。
  2. **分级入库**（避免把 10000 条历史草稿灌进本地表）：
     - 平台 ACTIVE            → 必 INSERT / UPDATE
     - 本地已存在的记录        → 必 UPDATE（治陈旧，核心诉求）
     - 平台 UNSUBMITTED 且本地无 → 仅当 `--include-drafts`（或带绩效/近期）时才入库
     - 其余                   → 仅计数
  3. 默认 **dry-run**，必须 `--apply` 才写库；`--apply` 前自动 sqlite3 backup 备份。

用法:
  python tools/sync_platform_alphas.py                       # dry-run（默认）
  python tools/sync_platform_alphas.py --apply               # 真正写库（自动备份）
  python tools/sync_platform_alphas.py --refresh             # 强制重拉平台快照
  python tools/sync_platform_alphas.py --include-drafts      # 连有价值的未提交草稿也入库
  python tools/sync_platform_alphas.py --limit-detail 40     # 明细打印条数

运行环境: MCP venv（$WQ_PY / world-quant-brain-mcp/.venv），工具自动切换。
"""
import argparse
import asyncio
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
DB = WQ_ROOT / "data" / "wqb.db"
SNAP_DIR = WQ_ROOT / "research-data"

PAGE_SIZE = 100
PAGE_SLEEP = 1.2          # 每页之间节流
MAX_PAGES = 120           # 100*120 = 12000，覆盖上限
RECENT_DAYS = 90          # "近期提交"窗口（与点塔窗口一致）


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, str(WQ_ROOT / "world-quant-brain-mcp" / ".venv" / "Scripts" / "python.exe")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap():
    py = _mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)
    sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))


def snapshot_path():
    return SNAP_DIR / f"platform_alphas_snapshot_{datetime.now():%Y%m%d}.json"


async def fetch_snapshot(brain, window_days=None, max_pages=MAX_PAGES):
    """拉取平台 alpha 快照（轻量字段）。

    window_days: 只取近 N 天提交的 alpha。按 `-dateSubmitted` 倒序拉取，
                 一旦遇到早于窗口的提交即停止——点塔只统计近 90 天提交，
                 90 天外的历史草稿对点亮判定与队列均零影响，无需入库。
    window_days=None 或 0 → 全量拉取（约 100 页，3-5 分钟）。
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(days=window_days)) if window_days else None
    out, off, pages, stopped = [], 0, 0, "末页"
    while pages < max_pages:
        for attempt in range(5):
            try:
                r = await brain._request(
                    "GET", f"{brain.base_url}/users/self/alphas",
                    params={"limit": PAGE_SIZE, "offset": off,
                            "order": "-dateSubmitted"})
                if r.status_code == 429:
                    await asyncio.sleep(8)
                    continue
                j = r.json()
                break
            except Exception:
                if attempt == 4:
                    raise
                await asyncio.sleep(5)
        arr = j.get("results") or []
        if not arr:
            stopped = "空页"
            break
        hit_window_end = False
        for a in arr:
            ds = a.get("dateSubmitted")
            if cutoff and ds:
                try:
                    if datetime.fromisoformat(str(ds).replace("Z", "+00:00")) < cutoff:
                        hit_window_end = True
                        break
                except Exception:
                    pass
            s = a.get("settings") or {}
            isv = a.get("is") or {}
            prod = a.get("prod") or {}
            out.append({
                "id": a.get("id"),
                "type": a.get("type"),
                "status": a.get("status"),
                "stage": a.get("stage"),
                "dateSubmitted": ds,
                "region": s.get("region"),
                "universe": s.get("universe"),
                "delay": s.get("delay"),
                "sharpe": isv.get("sharpe"),
                "fitness": isv.get("fitness"),
                "turnover": isv.get("turnover"),
                "ladder": isv.get("ladderSharpe") or isv.get("isLadderSharpe"),
                "prod_corr": prod.get("correlation") if isinstance(prod, dict) else None,
                "code": (a.get("regular") or {}).get("code") or "",
            })
        if hit_window_end:
            stopped = f"越过 {window_days} 天窗口"
            break
        if len(arr) < PAGE_SIZE:
            stopped = "末页"
            break
        off += PAGE_SIZE
        pages += 1
        await asyncio.sleep(PAGE_SLEEP)
    print(f"[拉取] {len(out)} 条，{pages + 1} 页，停止原因：{stopped}")
    return out


def backup_db():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = WQ_ROOT / "data" / f"wqb.db.bak_syncalpha_{ts}"
    src = sqlite3.connect(str(DB))
    dst = sqlite3.connect(str(bak))
    src.backup(dst)
    dst.close()
    src.close()
    return bak


def _isv(d, *keys):
    for k in keys:
        if d.get(k) is not None:
            return d[k]
    return None


def main():
    ap = argparse.ArgumentParser(description="平台 alpha → 本地 DB 对齐（根治状态陈旧/缺失）")
    ap.add_argument("--apply", action="store_true", help="真正写库（默认 dry-run）")
    ap.add_argument("--refresh", action="store_true", help="强制重拉平台快照（忽略当天缓存）")
    ap.add_argument("--include-drafts", action="store_true",
                    help="把平台未提交但有绩效/近期的草稿也入库（默认只入 ACTIVE + 本地已有）")
    ap.add_argument("--window-days", type=int, default=RECENT_DAYS,
                    help=f"只对齐近 N 天提交的 alpha（默认 {RECENT_DAYS}，与点塔窗口一致；"
                         f"0 = 全量）")
    ap.add_argument("--all", action="store_true", help="等价 --window-days 0（全量拉取）")
    ap.add_argument("--limit-detail", type=int, default=25, help="明细打印条数")
    a = ap.parse_args()
    window = 0 if a.all else a.window_days

    _bootstrap()
    from brain_api import BrainApiClient

    snap = snapshot_path()
    if snap.exists() and not a.refresh:
        plat = json.loads(snap.read_text(encoding="utf-8"))
        print(f"[快照] 读缓存 {snap.name}  {len(plat)} 条（--refresh 可重拉）")
    else:
        async def _go():
            brain = BrainApiClient()
            await brain.ensure_authenticated()
            return await fetch_snapshot(brain, window_days=window)
        plat = asyncio.run(_go())
        snap.write_text(json.dumps(plat, ensure_ascii=False), encoding="utf-8")
        print(f"[快照] 保存 {len(plat)} 条 → {snap.name}")

    # 本地现有记录
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    cur.execute("SELECT id, name FROM regions")
    reg2id = {n: i for i, n in cur.fetchall()}
    cur.execute("SELECT alpha_id, status, platform_status, stage, date_submitted, dataset_id "
                "FROM alphas")
    local = {r[0]: {"status": r[1], "platform_status": r[2], "stage": r[3],
                    "date_submitted": r[4], "dataset_id": r[5]} for r in cur.fetchall()}
    # dataset 反查索引（region_id -> {field: dataset_id}）+ 各区占位数据集
    cur.execute("SELECT f.field_name, f.dataset_id, d.region_id FROM fields f "
                "JOIN datasets d ON d.id = f.dataset_id")
    f2ds = {}
    for fn, dsid, rid in cur.fetchall():
        f2ds.setdefault((rid, fn), dsid)
    cur.execute("SELECT id, region_id FROM datasets GROUP BY region_id")
    placeholder = {rid: dsid for dsid, rid in cur.fetchall()}
    con.close()

    now = datetime.now(timezone.utc)
    recent_cut = now - timedelta(days=RECENT_DAYS)

    def parse_dt(v):
        try:
            return datetime.fromisoformat(str(v).replace("Z", "+00:00"))
        except Exception:
            return None

    def resolve_dataset(p, rid):
        if rid is None:
            return None, "无区域"
        hits = Counter()
        for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", p.get("code") or ""):
            dsid = f2ds.get((rid, tok))
            if dsid:
                hits[dsid] += 1
        if hits:
            dsid, n = hits.most_common(1)[0]
            return dsid, f"字段反查×{n}"
        return placeholder.get(rid), "占位"

    todo_insert, todo_update, stats = [], [], Counter()
    plat_ids = set()
    for p in plat:
        aid = p.get("id")
        if not aid:
            continue
        plat_ids.add(aid)
        rid = reg2id.get(p.get("region"))
        lv = local.get(aid)
        if lv is None:
            # 本地无记录
            if p.get("status") != "ACTIVE":
                drafted = (p.get("sharpe") is not None or p.get("fitness") is not None)
                dt = parse_dt(p.get("dateSubmitted"))
                recent = bool(dt and dt >= recent_cut)
                if not (a.include_drafts and (drafted or recent)):
                    stats["skip_draft"] += 1
                    continue
            dsid, how = resolve_dataset(p, rid)
            todo_insert.append((p, rid, dsid, how))
        else:
            # 本地有记录 → 检查是否需要更新
            need = False
            reason = []
            if lv["platform_status"] != p.get("status"):
                need = True
                reason.append(f"plat {lv['platform_status']}→{p.get('status')}")
            if (p.get("dateSubmitted") or None) != (lv["date_submitted"] or None):
                need = True
                reason.append("date_submitted")
            if lv["stage"] != p.get("stage"):
                need = True
                reason.append("stage")
            if lv["dataset_id"] is None:
                need = True
                reason.append("补 dataset")
            if need:
                todo_update.append((p, rid, reason))
            else:
                stats["in_sync"] += 1

    local_only = [k for k in local if k not in plat_ids]

    print(f"\n平台快照 {len(plat)} 条 | 本地 alphas {len(local)} 条")
    print(f"  待新增 INSERT : {len(todo_insert)}")
    print(f"  待更新 UPDATE : {len(todo_update)}")
    print(f"  已一致        : {stats['in_sync']}")
    print(f"  跳过未提交草稿: {stats['skip_draft']}")
    print(f"  本地独有(平台无记录): {len(local_only)}")

    if todo_update:
        print(f"\n--- UPDATE 明细（前 {a.limit_detail}）---")
        for p, rid, reason in todo_update[:a.limit_detail]:
            print(f"  {p['id']:<10} {str(p.get('region')):4s} "
                  f"plat={p.get('status')} sub={str(p.get('dateSubmitted'))[:10]}  "
                  f"改动: {','.join(reason)}")
    if todo_insert:
        print(f"\n--- INSERT 明细（前 {a.limit_detail}）---")
        for p, rid, dsid, how in todo_insert[:a.limit_detail]:
            print(f"  {p['id']:<10} {str(p.get('region')):4s} plat={p.get('status')} "
                  f"sh={p.get('sharpe')} fit={p.get('fitness')} "
                  f"dataset={dsid}({how})")

    if not a.apply:
        print("\n[dry-run] 未写库。确认无误后加 --apply 执行（自动备份）。")
        return

    bak = backup_db()
    print(f"\n[backup] {bak}")
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    now_iso = datetime.now().isoformat(timespec="seconds")

    n_i = n_u = 0
    for p, rid, dsid, how in todo_insert:
        cur.execute("""INSERT INTO alphas (alpha_id, expression, region_id, dataset_id,
                       universe, delay, sharpe, fitness, turnover, is_ladder_sharpe,
                       status, alpha_type, platform_status, stage, date_submitted,
                       prod_correlation, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p.get("code") or "", rid, dsid, p.get("universe"),
                     p.get("delay"), p.get("sharpe"), p.get("fitness"),
                     p.get("turnover"), p.get("ladder"),
                     "COMPLETE" if p.get("status") == "ACTIVE" else "UNSUBMITTED",
                     p.get("type") or "REGULAR", p.get("status"), p.get("stage"),
                     p.get("dateSubmitted"), p.get("prod_corr"), now_iso, now_iso))
        n_i += 1

    for p, rid, reason in todo_update:
        dsid = None
        if local[p["id"]]["dataset_id"] is None:
            dsid, _ = resolve_dataset(p, rid)
        if dsid:
            cur.execute("""UPDATE alphas SET platform_status=?, stage=?, date_submitted=?,
                           dataset_id=COALESCE(?, dataset_id), sharpe=COALESCE(?,sharpe),
                           fitness=COALESCE(?,fitness), turnover=COALESCE(?,turnover),
                           updated_at=? WHERE alpha_id=?""",
                        (p.get("status"), p.get("stage"), p.get("dateSubmitted"), dsid,
                         p.get("sharpe"), p.get("fitness"), p.get("turnover"),
                         now_iso, p["id"]))
        else:
            cur.execute("""UPDATE alphas SET platform_status=?, stage=?, date_submitted=?,
                           sharpe=COALESCE(?,sharpe), fitness=COALESCE(?,fitness),
                           turnover=COALESCE(?,turnover), updated_at=? WHERE alpha_id=?""",
                        (p.get("status"), p.get("stage"), p.get("dateSubmitted"),
                         p.get("sharpe"), p.get("fitness"), p.get("turnover"),
                         now_iso, p["id"]))
        n_u += 1

    con.commit()
    con.close()
    print(f"\n[apply] 新增 {n_i} / 更新 {n_u}")

    # 复核
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    cur.execute("SELECT platform_status, COUNT(*) FROM alphas GROUP BY platform_status")
    print("[复核] platform_status 分布:", cur.fetchall())
    con.close()


if __name__ == "__main__":
    if "--help" not in sys.argv:
        pass
    main()
