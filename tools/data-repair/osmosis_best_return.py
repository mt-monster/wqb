"""Osmosis 收益最高分配规划器（只读，产出 plan 供 review）。

基于 fresh os_scan.json（osISSharpeRatio 换算的真实 OS Sharpe）+ 平台池
（IS/investability/prod/turnover），复用 osmosis_allocate 的 quality/build_plan
核心数学，加入「收益最高」杠杆：
  1. --exclude-neg-os：剔除实盘亏损（os_sharpe<=0）的 alpha（不奖励已验证亏钱的）
  2. --exclude-region MEA：MEA 已下架
  3. prod-policy exclude：剔除 prod>=0.70
  4. quality 优先 investability，缺失回退 OS>IS（fresh）
产出两个变体对比：含 USA / 不含 USA，落 results/osmosis_best_return.json
用法: python tools/data-repair/osmosis_best_return.py
"""
import os
import sys
import json
import asyncio

HERE = os.path.dirname(os.path.abspath(__file__))
WQB = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(WQB, "world-quant-brain-mcp"))

import osmosis_allocate as OA  # noqa: E402
from brain_api import BrainApiClient  # noqa: E402

SCAN = os.path.join(WQB, "results", "os_scan.json")
OUT = os.path.join(WQB, "results", "osmosis_best_return.json")


async def fetch_pool(b):
    rows, off = [], 0
    for _ in range(200):
        r = await b.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows.extend(res)
        if not pl.get("next"):
            break
        off += 100
    return rows


def build_rows(pool, scan):
    rows = []
    for a in pool:
        if a.get("type") != "REGULAR" or a.get("status") != "ACTIVE":
            continue
        st = a.get("settings") or {}
        isd = a.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = a.get("prod")
        aid = a["id"]
        sc = scan.get(aid, {})
        rows.append({
            "alpha_id": aid,
            "region": st.get("region"),
            "delay": st.get("delay"),
            "sharpe": isd.get("sharpe"),
            "os_sharpe": sc.get("os_sharpe"),          # fresh：IS×osISSharpeRatio
            "fitness": isd.get("fitness"),
            "turnover": isd.get("turnover"),
            "investability_sharpe": (isd.get("investabilityConstrained") or {}).get("sharpe"),
            "prod": prod,
            "os_ratio": sc.get("os_ratio"),
        })
    return rows


def make_plan(rows, exclude_region):
    """复用 OA.build_plan；先做收益杠杆过滤。"""
    OA.PROD_POLICY = "exclude"
    OA.PROD_MAX = 0.70
    r = list(rows)
    # MEA 下架 + 可选排除 USA
    excl = {"MEA"}
    if exclude_region:
        excl.add(exclude_region.upper())
    r = [x for x in r if (x.get("region") or "").upper() not in excl]
    # 收益杠杆：剔除实盘亏损
    neg = [x for x in r if x.get("os_sharpe") is not None and x["os_sharpe"] <= 0]
    r = [x for x in r if not (x.get("os_sharpe") is not None and x["os_sharpe"] <= 0)]
    # prod>=0.70 剔除（含 None 保守剔除）
    none_ct = sum(1 for x in r if x.get("prod") is None)
    r = [x for x in r if not (x.get("prod") is None or x["prod"] >= 0.70)]
    scopes = OA.build_scopes(r)
    plan = OA.build_plan(scopes, eligible_only=True)
    return plan, {"neg_os_excluded": len(neg), "neg_os_ids": [x["alpha_id"] for x in neg],
                  "none_prod_excluded": none_ct}


def summarize(plan, rows):
    from collections import defaultdict
    id2r = {x["alpha_id"]: x for x in rows}
    byreg = defaultdict(list)
    for e in plan:
        byreg[e["region"]].append(e)
    tot = sum(e["points"] for e in plan)
    lines = []
    for reg in sorted(byreg, key=lambda x: -sum(e["points"] for e in byreg[x])):
        al = byreg[reg]
        pts = sum(e["points"] for e in al)
        os_vals = [id2r[e["alpha_id"]].get("os_sharpe") for e in al
                   if id2r[e["alpha_id"]].get("os_sharpe") is not None]
        n_os = len(os_vals)
        avg_os = round(sum(os_vals) / n_os, 3) if os_vals else None
        lines.append((reg, len(al), pts, round(pts / tot * 100, 1), n_os, avg_os))
    return lines, tot


async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()
    pool = await fetch_pool(b)
    scan = json.load(open(SCAN, encoding="utf-8")) if os.path.exists(SCAN) else {}
    rows = build_rows(pool, scan)
    print(f"[pool] {len(pool)} -> ACTIVE REGULAR {len(rows)} 颗; scan OS 数据 {len(scan)} 颗")

    result = {}
    for tag, excl in [("with_USA", None), ("no_USA", "USA")]:
        plan, meta = make_plan(rows, excl)
        summ, tot = summarize(plan, rows)
        elig_scopes = len(summ)
        result[tag] = {"meta": meta, "total_points": tot, "n_alphas": len(plan),
                       "n_scopes": elig_scopes, "summary": summ,
                       "plan": plan}
        print(f"\n=== 变体 {tag}: {len(plan)} 颗 / {elig_scopes} 区 / 总 {tot} 点 ===")
        print(f"    剔除实盘亏损 {meta['neg_os_excluded']} 颗: {meta['neg_os_ids']}")
        print(f"    剔除未知prod(None) {meta['none_prod_excluded']} 颗")
        print(f"    {'区':<5}{'颗':>4}{'点数':>8}{'占比%':>7}{'有OS':>5}{'avgOS':>7}")
        for reg, n, pts, pct, n_os, avg_os in summ:
            print(f"    {reg:<5}{n:>4}{pts:>8}{pct:>7}{n_os:>5}{str(avg_os):>7}")

    json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
