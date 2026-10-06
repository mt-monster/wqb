# -*- coding: utf-8 -*-
"""backfill_prod_corr.py — 补测 pc_null alpha 的平台 prod_correlation（2026-09-02）。

背景: wqb.db 中 IND 104 条 S>=1.58 达标 alpha 有 75 条 prod_correlation IS NULL
      ——不是撞墙, 而是从未在平台测过相关性。本工具用 MCP venv 的
      BrainApiClient.check_correlation(alpha_id, "production") 把"未知"变"已知"。

平台约束:
  * prod 相关性计算为异步排队, 1-5 分钟/条, 单并发/账号;
  * check_correlation 内部 30s 轮询最长 1 小时, 已决结果缓存 7 天;
  * busy = 账号已有计算在跑 → sleep 后重试; pending = 1 小时超时 → 下轮重查。

断点续跑 (必须):
  * checkpoint: results/backfill_prod_corr_<REGION>_checkpoint.json
  * 只有 max_correlation 非 None 的"已决"结果算完成, 重启自动跳过;
  * PENDING / PC_TIMEOUT 不计入完成, 下轮重试 (参考 V33/V34 续跑模式);
  * 原子写: tmp + os.replace。

风险过滤: 可选加载 tracking/_scratch/<region>_pc_null_risk_*.json 按 LOW/MED/HIGH 过滤。

用法:
  # probe: 先测 3 条 LOW 风险, 不写库
  python tools/backfill_prod_corr.py --region IND --risk low --limit 3

  # 全量: 75 条全部
  python tools/backfill_prod_corr.py --region IND

  # 全量 + 结果写回 DB (自动备份)
  python tools/backfill_prod_corr.py --region IND --apply-db

  # 续跑: 直接重跑同命令即可, checkpoint 自动跳过已决项
  # 强制全新: 环境变量 BACKFILL_PC_FRESH=1
"""
import argparse
import asyncio
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

WQ_ROOT = Path(__file__).resolve().parents[1]      # 仓库根（无盘符硬编码）
sys.path.insert(0, str(WQ_ROOT))
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

DB = WQ_ROOT / "data" / "wqb.db"
CKPT_DIR = WQ_ROOT / "results"
RISK_JSON = WQ_ROOT / "tracking" / "_scratch" / f"ind_pc_null_risk_20260902.json"

BUSY_RETRY_MAX = 30        # busy 状态最多重试 30 次 (~15 分钟)
BUSY_SLEEP = 30            # busy 后等待秒数
INTER_ITEM_SLEEP = 5       # 条与条之间的小间隔
FRESH = os.environ.get("BACKFILL_PC_FRESH", "") == "1"


def mcp_venv_python():
    p = WQ_ROOT / "world-quant-brain-mcp" / ".venv" / "Scripts" / "python.exe"
    return p if p.is_file() else sys.executable


def bootstrap():
    """非 MCP venv 运行时自动切换 (os.execv, 与 sync_platform_alphas 同模式)。"""
    py = mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)


def ckpt_path(region):
    return CKPT_DIR / f"backfill_prod_corr_{region.upper()}_checkpoint.json"


def load_ckpt(region):
    p = ckpt_path(region)
    if p.exists() and not FRESH:
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            print(f"[WARN] checkpoint 损坏, 忽略: {p}")
    return {"results": []}


def save_ckpt(region, data):
    CKPT_DIR.mkdir(exist_ok=True)
    p = ckpt_path(region)
    tmp = str(p) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1, default=str)
    os.replace(tmp, p)


def load_risk_filter(risk_arg):
    """risk_arg: None=不过滤; 'low'/'med'/'high' 或逗号组合"""
    if not risk_arg or not RISK_JSON.exists():
        return None
    want = {x.strip().upper() for x in risk_arg.split(",") if x.strip()}
    data = json.loads(RISK_JSON.read_text(encoding="utf-8"))
    # 只对 IND 有效; 其他 region 返回空集(全部跳过)还是不过滤? → 不过滤, 仅 IND 有定级
    allowed = set()
    for r in data:
        if r.get("risk", "").upper() in want:
            allowed.add(r["alpha_id"])
    print(f"[risk] 过滤 {sorted(want)}: 允许 {len(allowed)} 条 (来自 {RISK_JSON.name})")
    return allowed


#: 本地三闸的线（与 RA 口径一致）。**在排队前剪掉本地已判死的 alpha**——
#: 2026-10-06 实测：平台 prod 是单槽串行、实测 94s/条（历史吞吐 37 条/天），
#: 而未测池 841 颗里 659 颗（78%）本地就已经判死（2Y/sub 不达标），
#: 让它们进队列等于白烧 330~550 小时。
TWO_YEAR_MIN = 1.58
SUB_UNIVERSE_MIN = 1.0

#: 已实测 prod ≥ 此值 ⇒ 认定撞墙，除非显式 --remeasure-dead 否则不再排队。
#: 实测 778 颗已测值里 192 颗 ≥ 0.85，重测它们几乎不可能翻盘。
DEAD_PROD = 0.85

#: 已实测 prod ≤ 此值 ⇒ 认定远离闸门，同样不重排（0.60 以下距 0.7 有 0.1 余量）。
SAFE_PROD = 0.60


def fetch_targets(region, sharpe_min):
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    rid = cur.execute("SELECT id FROM regions WHERE name=?", (region.upper(),)).fetchone()
    if not rid:
        raise SystemExit(f"[FATAL] region {region} 不在 regions 表")
    # 权威表 alpha_corr_cache 优先（mirror 可能缺值），再回落 alphas
    rows = cur.execute("""
        SELECT a.alpha_id, a.sharpe, a.fitness, a.turnover, a.expression, a.dataset_id
        FROM alphas a
        WHERE a.region_id=? AND a.sharpe>=? AND a.prod_correlation IS NULL
        ORDER BY a.sharpe DESC
    """, (rid[0], sharpe_min)).fetchall()
    con.close()
    return rows


def prefilter(rows, apply_gates=True, remeasure_dead=False):
    """排队前剪枝：本地三闸 + 已定型值不再重排。返回 (kept, stats)。

    与 ``select_ra_basket`` 的差异：这里**不**按 corr_checked_at 判 48h stale，
    而是按「值是否已定型」判——prod ≥ 0.85 或 ≤ 0.60 的值重测几乎不改变结论，
    不该占用单槽队列。真正需要终验的只有贴闸区（0.60 < prod < 0.85）。
    """
    con = sqlite3.connect(str(DB))
    ids = [r[0] for r in rows]
    cached = {}
    for i in range(0, len(ids), 500):
        chunk = ids[i:i + 500]
        marks = ",".join("?" * len(chunk))
        for aid, prod in con.execute(
                f"SELECT alpha_id, prod_correlation FROM alpha_corr_cache "
                f"WHERE alpha_id IN ({marks})", chunk):
            if prod is not None:
                cached[aid] = prod
    for aid, prod in con.execute(
            f"SELECT alpha_id, prod_correlation FROM alphas "
            f"WHERE alpha_id IN ({','.join('?' * len(ids))})", ids) if ids else []:
        cached.setdefault(aid, prod)

    cols = {r[1] for r in con.execute("PRAGMA table_info(alphas)")}
    two_y = "a.two_year_sharpe" if "two_year_sharpe" in cols else "NULL"
    sub = "a.sub_universe_sharpe" if "sub_universe_sharpe" in cols else "NULL"
    gate_rows = {}
    if ids:
        marks = ",".join("?" * len(ids))
        for aid, ty, su in con.execute(
                f"SELECT a.alpha_id, {two_y}, {sub} FROM alphas a "
                f"WHERE a.alpha_id IN ({marks})", ids):
            gate_rows[aid] = (ty, su)
    con.close()

    kept, n_gate, n_settled = [], 0, 0
    for r in rows:
        aid = r[0]
        if apply_gates:
            ty, su = gate_rows.get(aid, (None, None))
            # 字段缺失(=未回填)时不据此判死，避免误杀
            if ty is not None and ty < TWO_YEAR_MIN:
                n_gate += 1
                continue
            if su is not None and su < SUB_UNIVERSE_MIN:
                n_gate += 1
                continue
        if not remeasure_dead:
            p = cached.get(aid)
            if p is not None and (p >= DEAD_PROD or p <= SAFE_PROD):
                n_settled += 1
                continue
        kept.append(r)
    return kept, {"gate_cut": n_gate, "settled_cut": n_settled,
                  "candidates": len(rows)}


async def check_one(brain, alpha_id, threshold=0.7):
    """测一条, 返回 dict。已决: max_correlation 非 None。"""
    for busy_try in range(1, BUSY_RETRY_MAX + 1):
        try:
            r = await brain.check_correlation(alpha_id, "production", threshold=threshold)
        except Exception as e:
            return {"alpha_id": alpha_id, "status": "ERROR", "error": str(e),
                    "max_correlation": None, "attempts": busy_try}
        status = r.get("status")
        chk = (r.get("checks") or {}).get("production") or {}
        mx = chk.get("max_correlation")
        if mx is not None:
            return {
                "alpha_id": alpha_id, "status": "OK",
                "max_correlation": mx,
                "passes": mx < threshold,
                "from_cache": bool(chk.get("from_cache")),
                "checked_at": datetime.now().isoformat(timespec="seconds"),
            }
        if status == "correlation_busy":
            if busy_try >= BUSY_RETRY_MAX:
                return {"alpha_id": alpha_id, "status": "PC_TIMEOUT",
                        "max_correlation": None, "error": "busy x30"}
            await asyncio.sleep(BUSY_SLEEP)
            continue
        # pending / data_unavailable / 其他未决 → 单独重试 3 次(每次内部已轮询1小时)
        return {"alpha_id": alpha_id, "status": "PENDING_PC",
                "max_correlation": None,
                "message": str(r.get("message") or chk.get("message") or status)[:200]}
    return {"alpha_id": alpha_id, "status": "PC_TIMEOUT", "max_correlation": None}


async def run(args):
    from brain_api import BrainApiClient

    region = args.region.upper()
    targets = fetch_targets(region, args.sharpe_min)
    print(f"[targets] {region} S>={args.sharpe_min} & pc_null: {len(targets)} 条")

    risk_allowed = load_risk_filter(args.risk)
    if risk_allowed is not None:
        targets = [t for t in targets if t[0] in risk_allowed]
        print(f"[risk] 过滤后: {len(targets)} 条")

    if args.limit:
        targets = targets[:args.limit]
        print(f"[limit] probe 模式: 只测前 {len(targets)} 条")

    # 排队前剪枝（2026-10-06）：本地三闸 + 已定型值。这是提速的主要杠杆——
    # 平台单槽 94s/条，砍掉一条就省 1.5 分钟真实等待。
    targets, stats = prefilter(targets,
                               apply_gates=not args.no_gates,
                               remeasure_dead=args.remeasure_dead)
    print(f"[prefilter] 候选 {stats['candidates']} → 实测 {len(targets)}"
          f"（本地闸砍 {stats['gate_cut']}、已定型砍 {stats['settled_cut']}）"
          + ("  [闸门已关闭]" if args.no_gates else ""))

    ckpt = load_ckpt(region)
    done = {r["alpha_id"]: r for r in ckpt["results"]
            if r.get("max_correlation") is not None}
    todo = [t for t in targets if t[0] not in done]
    print(f"[resume] checkpoint 已决 {len(done)} 条, 待测 {len(todo)} 条"
          + (" (FRESH=1 忽略)" if FRESH else ""))

    if not todo:
        print("[done] 无待测项。")
        return ckpt

    brain = BrainApiClient()
    await brain.ensure_authenticated()
    print("[auth] OK")

    t0 = time.time()
    est = 3 * 60  # 保守估计 3 分钟/条
    for i, (alpha_id, sharpe, fitness, turnover, expr, dsid) in enumerate(todo, 1):
        elapsed = i - 1
        eta_min = (len(todo) - i + 1) * est / 60
        print(f"\n[{i}/{len(todo)}] {alpha_id} S={sharpe:.2f} "
              f"(elapsed {elapsed*est//60:.0f}m, ETA {eta_min:.0f}m)")
        r = await check_one(brain, alpha_id, threshold=args.threshold)
        # 附加元数据
        r.update({"sharpe": sharpe, "fitness": fitness, "dataset_id": dsid,
                  "expr_head": (expr or "")[:80]})
        ckpt["results"].append(r)
        save_ckpt(region, ckpt)  # 每条原子写
        tag = r.get("status")
        if tag == "OK":
            print(f"  => PC={r['max_correlation']:.4f} "
                  f"{'PASS' if r['passes'] else 'WALL(>=0.7)'}"
                  + (" [cache]" if r.get("from_cache") else ""))
        else:
            print(f"  => {tag}: {str(r.get('error') or r.get('message'))[:120]}")
        await asyncio.sleep(INTER_ITEM_SLEEP)

    print(f"\n[elapsed] {(time.time()-t0)/60:.1f} min")
    return ckpt


def summary_and_maybe_apply(args, ckpt):
    results = [r for r in ckpt["results"]]
    ok = [r for r in results if r.get("max_correlation") is not None]
    walls = [r for r in ok if not r.get("passes")]
    passes = [r for r in ok if r.get("passes")]
    pend = [r for r in results if r.get("max_correlation") is None]

    print("\n===== 汇总 =====")
    print(f"已决: {len(ok)}  (WALL {len(walls)} / PASS {len(passes)})   未决: {len(pend)}")
    if passes:
        print("\n-- PASS 明细 --")
        for r in sorted(passes, key=lambda x: -(x.get("sharpe") or 0)):
            print(f"  {r['alpha_id']} S={r.get('sharpe', 0):.2f} PC={r['max_correlation']:.4f}")
    if walls:
        print("\n-- WALL(>=0.7) 明细 --")
        for r in sorted(walls, key=lambda x: -(x.get("sharpe") or 0)):
            print(f"  {r['alpha_id']} S={r.get('sharpe', 0):.2f} PC={r['max_correlation']:.4f}")
    if pend:
        print(f"\n-- 未决 {len(pend)} 条 (PENDING_PC/PC_TIMEOUT, 下轮重查) --")

    if not args.apply_db:
        print("\n[dry-run] 未写库。确认后加 --apply-db 写回 prod_correlation。")
        return

    # 写回 DB (备份 → UPDATE → 复核)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = DB.parent / f"wqb.db.bak_backfillpc_{ts}"
    src = sqlite3.connect(str(DB))
    dst = sqlite3.connect(str(bak))
    src.backup(dst)
    dst.close()
    print(f"\n[backup] {bak}")

    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    # 2026-10-06：改走权威表 set_corr_cache（会联动 mirror alphas）。
    # 此前是裸 UPDATE，只写 alphas —— 单源化后又多出一条旁路。
    import sys as _sys
    _sys.path.insert(0, str(WQ_ROOT / "src"))
    from wqb.store import CampaignStore
    store = CampaignStore(str(DB))
    n = 0
    for r in ok:
        out = store.set_corr_cache(r["alpha_id"], prod=r["max_correlation"],
                                   source="backfill_prod_corr")
        if out.get("action") == "upserted":
            n += 1
    store.close()
    print(f"[apply-db] 权威表写入 {n} 条（已联动 alphas）")
    cnt = cur.execute(
        "SELECT COUNT(*) FROM alphas a JOIN regions r ON a.region_id=r.id "
        "WHERE r.name=? AND a.sharpe>=? AND a.prod_correlation IS NULL",
        (args.region.upper(), args.sharpe_min)).fetchone()[0]
    print(f"[verify] {args.region.upper()} S>=1.58 pc_null 剩余: {cnt}")
    con.close()


def main():
    ap = argparse.ArgumentParser(description="补测 pc_null alpha 的平台 prod_correlation")
    ap.add_argument("--region", default="IND")
    ap.add_argument("--sharpe-min", type=float, default=1.58)
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--risk", help="只测指定风险组: low / med / high / 逗号组合 (需定级 JSON)")
    ap.add_argument("--limit", type=int, help="只测前 N 条 (probe 用)")
    ap.add_argument("--apply-db", action="store_true",
                    help="把已决结果写回 DB prod_correlation (自动备份)")
    ap.add_argument("--no-gates", action="store_true",
                    help="关闭本地三闸预筛（2Y/sub），全量排队——仅用于对照复测")
    ap.add_argument("--remeasure-dead", action="store_true",
                    help="连 prod>=0.85 / <=0.60 的已定型值也重测（默认跳过）")
    args = ap.parse_args()

    bootstrap()
    ckpt = asyncio.run(run(args))
    summary_and_maybe_apply(args, ckpt)


if __name__ == "__main__":
    main()
