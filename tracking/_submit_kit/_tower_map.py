# -*- coding: utf-8 -*-
"""金字塔「塔」映射 + 候选点塔排名（只读，不提交）。v3 — 用平台权威 pyramids 字段

塔 = 平台 alpha 的 `pyramids[].name`，形如 "IND/D1/RISK"（区域/延迟/类别，带 multiplier）。
这比本地字段反查可靠得多（本地 fields 缺 USA/IND/KOR 字段，反查大面积 UNKNOWN）。

准则（用户 2026-09-01 定）：
  ① 优先点亮未点亮的新塔
  ② 其次按绩效排序（fitness 降序）
  ③ MEA 不再自动提交，仅罗列候选交用户决定
"""
import asyncio
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
DB = WQ_ROOT / "data" / "wqb.db"
VERDICT = WQ_ROOT / "research-data" / "final_verdict_20260901.json"

BLOCK_AUTO_REGIONS = {"MEA"}   # 用户：MEA 本季度（90d 窗口）完全不考虑提交，不进队列

# ★ 点亮口径（2026-09-01 用户定案）：
#   ① 点亮 = 该 catalog 下「近 90 天（一个季度）内提交」的 ACTIVE ≥3 颗
#     （USA/FUNDAMENTAL 总 5 颗但 4 颗是 2025-09~2026-01 老 alpha → UI 未亮；USA/PV 同理）
#   ② 跨 ≥3 catalog 的 alpha 不计（平台 pyramidThemes.effective=0 实证）
WINDOW_DAYS = 90
EXCLUDE_MULTI = 3
MIN_LIT = 3


def pyr_names(a):
    return [p.get("name") for p in (a.get("pyramids") or []) if p.get("name")]


async def fetch_active(brain):
    out, offset, limit = [], 0, 100
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"status": "ACTIVE", "limit": limit, "offset": offset})
        arr = r.json().get("results") or []
        out.extend(arr)
        if len(arr) < limit:
            break
        offset += limit
        if offset > 5000:
            break
    return out


def possible_towers():
    """「可点亮塔」全集：region × delay × category。
    优先读平台目录缓存 platform_catalog_*.json（权威，含 D0、类别已归一）；
    缓存缺失时回退本地 datasets 表（2026-09-01 已同步：类别回填 + delay 列）。"""
    caches = sorted(WQ_ROOT.glob("research-data/platform_catalog_*.json"))
    if caches:
        cat = json.loads(caches[-1].read_text(encoding="utf-8"))
        out = {}
        for rg, by_delay in cat.items():
            for dk, rows in (by_delay or {}).items():
                for d in rows or []:
                    if d.get("category"):
                        out[f"{rg}/D{dk}/{d['category']}"] = rg
        if out:
            return out
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    cur.execute("SELECT id, name FROM regions")
    rid2n = dict(cur.fetchall())
    cur.execute("SELECT DISTINCT region_id, category, delay FROM datasets "
                "WHERE category IS NOT NULL")
    out = {}
    for rid, cat, delay in cur.fetchall():
        rname = rid2n.get(rid)
        if not rname or not cat:
            continue
        d = int(delay) if delay is not None else 1   # 注意 delay=0 是合法值，勿用 `or 1`
        out[f"{rname}/D{d}/{str(cat).strip().upper()}"] = rid
    con.close()
    return out


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    active = await fetch_active(brain)
    submitted_ids = {a.get("id") for a in active}
    print(f"[平台] ACTIVE alpha = {len(active)} 颗")

    # --- 已点亮塔：★ 用户 UI 校准定案（2026-09-01）---
    #   ① 点亮 = 该 catalog 下「近 WINDOW_DAYS 天提交」的 ACTIVE ≥3 颗
    #   ② 跨 ≥EXCLUDE_MULTI 个 catalog 的 alpha 不计（平台 effective=0 实证）
    MIN_LIT = 3
    EXCLUDE_MULTI = 3          # 跨 >=3 个 catalog 的提交不算点塔
    cutoff = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    cnt = Counter()                    # 每塔窗口内有效 ACTIVE 颗数
    lit_detail = defaultdict(list)
    excluded_multi, stale = [], 0
    for a in active:
        pys = pyr_names(a)
        if len(pys) >= EXCLUDE_MULTI:
            excluded_multi.append((a.get("id"), pys))
            continue
        ds = a.get("dateSubmitted")
        try:
            dt = datetime.fromisoformat(str(ds).replace("Z", "+00:00"))
        except Exception:
            dt = None
        if dt is not None and dt < cutoff:
            stale += 1                 # 窗口外的老 alpha：不计数（UI 实证）
            continue
        for nm in pys:
            cnt[nm] += 1
            lit_detail[nm].append(a.get("id"))
    lit = {nm for nm, n in cnt.items() if n >= MIN_LIT}
    if excluded_multi:
        print(f"[剔除] 跨 ≥{EXCLUDE_MULTI} catalog 的 alpha（不计点塔）{len(excluded_multi)} 颗：")
        for aid, pys in excluded_multi:
            print(f"   {aid:10s} → {pys}")
    print(f"[剔除] 提交时间超出 {WINDOW_DAYS} 天窗口的老 alpha：{stale} 颗（UI 实证不点亮）")
    print(f"\n[每塔窗口内有效颗数，点亮=≥{MIN_LIT}（窗 {WINDOW_DAYS}d）]")
    for nm, n in sorted(cnt.items(), key=lambda x: (-x[1], x[0])):
        mark = " ★点亮" if n >= MIN_LIT else ""
        print(f"   {nm:<24s} x{n}{mark}")
    print(f"[已点亮塔] {len(lit)} 座（口径：每塔 {WINDOW_DAYS}d 内 ≥{MIN_LIT} 颗；"
          f"跨 ≥{EXCLUDE_MULTI} catalog 不计）")

    # --- 未点亮塔（本地数据集目录可推导的） ---
    poss = possible_towers()
    unlit = sorted(t for t in poss if t not in lit)
    print(f"\n[可点亮塔全集(本地目录推导)] {len(poss)} 座；其中 **未点亮 {len(unlit)} 座**")
    byreg_un = defaultdict(list)
    for t in unlit:
        byreg_un[t.split("/")[0]].append(t)
    print("\n=== 未点亮塔（按区域，= 后续点塔方向） ===")
    for rg in sorted(byreg_un):
        print(f"   [{rg}] {len(byreg_un[rg])} 座: " + ", ".join(byreg_un[rg]))

    # --- 候选（权威 finalists，剔除已提交） ---
    v = json.loads(VERDICT.read_text(encoding="utf-8"))
    cands = []
    for aid, d in v["finalists"].items():
        if aid in submitted_ids:
            continue
        try:
            det = await brain.get_alpha_details(aid)
            pys = pyr_names(det)
        except Exception as e:
            pys = []
            print(f"   [warn] {aid} pyramid 拉取失败: {str(e)[:60]}")
        newp = [p for p in pys if p not in lit]
        cands.append(dict(
            alpha_id=aid, region=d.get("region"), delay=d.get("delay"),
            universe=d.get("universe"), pyramids=pys, new_pyramids=newp,
            sharpe=d.get("sharpe"), fitness=d.get("fitness"),
            turnover=d.get("turnover"), conc_weight=d.get("conc_weight"),
            is_fails=d.get("is_fails")))
    print(f"\n[候选池] finalists 剔除已提交后 = {len(cands)} 颗")

    # 排序：① 能点亮新塔优先（新塔数多的更前）② fitness 降序
    cands.sort(key=lambda c: (-(len(c["new_pyramids"]) > 0), -len(c["new_pyramids"]),
                              -(c["fitness"] or 0)))

    def fmt(c):
        tag = ("★新塔" if c["new_pyramids"] else " 已亮")
        return (f"  [{tag}] {c['alpha_id']:10s} {str(c['region']):4s} "
                f"fit={c['fitness']:>5} sh={c['sharpe']:>5} to={c['turnover']:>7} "
                f"CW={c['conc_weight']:<4s} 塔={','.join(c['pyramids']) or '—'}"
                + (f"  新增→{c['new_pyramids']}" if c["new_pyramids"] else ""))

    print("\n=== ★ 推荐队列（非 MEA｜新塔优先 → fitness 降序） ===")
    queue = [c for c in cands if c["region"] not in BLOCK_AUTO_REGIONS]
    for c in queue:
        print(fmt(c))

    print("\n=== MEA 候选（不自动提交｜交用户决定） ===")
    mea = [c for c in cands if c["region"] in BLOCK_AUTO_REGIONS]
    for c in mea:
        print(fmt(c))

    out = WQ_ROOT / "research-data" / "tower_map_20260901.json"
    out.write_text(json.dumps({
        "min_lit": MIN_LIT,
        "lit_tower_counts": dict(cnt),          # 每塔 ACTIVE 颗数（含未达标的）
        "lit_towers": sorted(lit),              # ≥3 颗才算点亮
        "lit_detail": dict(lit_detail),
        "unlit_towers": unlit,
        "queue_non_mea": queue,
        "candidates_mea": mea,
        "submitted_ids": sorted(submitted_ids),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {out}")


if __name__ == "__main__":
    asyncio.run(main())
