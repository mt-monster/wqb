#!/usr/bin/env python
"""只读诊断：当前 Osmosis 分配 vs 理论最优（per-scope 100k + prod<0.7）。

输出：
  1. 各 scope 的 ACTIVE REGULAR 颗数 / 当前已分配(>1)颗数 / 当前点数和
  2. 理论最优方案（可指定排除区）每 scope 应分配颗数与点数和
  3. 差异清单：该分未分、分多了、scope 未启用

不写平台。用法：
  WQ_PY=... python tools/data-repair/review_osmosis_best.py [--purge-cache] [--exclude USA,MEA]
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sqlite3
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

import osmosis_allocate as OA  # noqa: E402

TOTAL = OA.TOTAL_BUDGET


def purge_cache() -> int:
    try:
        from wqb.db_conn import connect as _db_connect
        con = _db_connect(readonly=False)
        cur = con.execute("DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'")
        n = cur.rowcount
        con.commit()
        con.close()
        return n
    except Exception as e:  # noqa: BLE001
        print(f"[cache] 清理失败: {e}", file=sys.stderr)
        return -1


async def fetch_pool() -> list:
    from brain_api import brain_client
    rows: list = []
    off = 0
    for _ in range(200):
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        pl = r["result"] if isinstance(r, dict) and isinstance(r.get("result"), dict) else r
        res = pl.get("results", []) or []
        if not res:
            break
        rows.extend(res)
        if not pl.get("next"):
            break
        off += 100
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--purge-cache", action="store_true", help="先清 user_alphas 缓存(TTL 7天)")
    ap.add_argument("--exclude", default="USA,MEA", help="排除的 region（逗号分隔）")
    ap.add_argument("--prod-policy", default="exclude")
    ap.add_argument("--prod-max", type=float, default=0.70)
    a = ap.parse_args()

    if a.purge_cache:
        n = purge_cache()
        print(f"[cache] 清除 user_alphas 缓存 {n} 条")

    OA.PROD_POLICY = a.prod_policy
    OA.PROD_MAX = a.prod_max

    pool = asyncio.run(fetch_pool())
    excl = {x.strip().upper() for x in a.exclude.split(",") if x.strip()}

    act = [x for x in pool if x.get("status") == "ACTIVE" and x.get("type") == "REGULAR"]
    print(f"\nOS 池总 {len(pool)} 颗，其中 ACTIVE REGULAR {len(act)} 颗\n")

    cur: dict = defaultdict(list)   # scope -> [(id, pts, prod, inv)]
    for x in act:
        st = x.get("settings") or {}
        isd = x.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = x.get("prod")
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
        cur[(st.get("region"), st.get("delay"))].append({
            "id": x.get("id"),
            "pts": x.get("osmosisPoints") or 0,
            "prod": prod,
            "inv": inv,
            "sharpe": isd.get("sharpe"),
            "os": (x.get("os") or {}).get("sharpe"),
        })

    print("=" * 96)
    print(f"{'scope':<10}{'ACTIVE':>7}{'已分配':>8}{'当前点数和':>12}{'达标?':>8}   说明")
    print("=" * 96)
    for k in sorted(cur, key=lambda k: -len(cur[k])):
        al = cur[k]
        n = len(al)
        got = [x for x in al if x["pts"] > 1]
        tot = sum(x["pts"] for x in got)
        ok = "YES" if (n >= 10 and len(got) >= 10 and 99000 <= tot <= 101000) else "no"
        note = []
        if k[0] in excl:
            note.append("已排除(策略)")
        elif n < OA.MIN_PER_SCOPE:
            note.append(f"不足10颗(差{OA.MIN_PER_SCOPE - n})")
        elif len(got) < OA.MIN_PER_SCOPE:
            note.append(f"仅分了{len(got)}颗")
        print(f"{k[0]}D{k[1]:<8}{n:>7}{len(got):>8}{tot:>12}{ok:>8}   {'; '.join(note)}")
    print("=" * 96)

    # ---- 理论最优 ----
    rows = OA.load_candidates_platform()
    rows = [r for r in rows if (r.get("region") or "").upper() not in excl]
    scopes = OA.build_scopes(rows)
    plan = OA.build_plan(scopes, per_scope_budget=True)

    agg: dict = defaultdict(list)
    for e in plan:
        agg[(e["region"], e["delay"])].append(e["points"])

    print("\n【理论最优】per-scope 各 100k / prod-policy=exclude / 排除 " + ",".join(sorted(excl)))
    print("-" * 96)
    print(f"{'scope':<10}{'颗数':>6}{'点数和':>10}{'启用?':>8}")
    print("-" * 96)
    for k, pts in sorted(agg.items(), key=lambda kv: -sum(kv[1])):
        print(f"{k[0]}D{k[1]:<8}{len(pts):>6}{sum(pts):>10}{'YES' if len(pts) >= 10 else 'no':>8}")
    print("-" * 96)
    tot_scope = sum(1 for k, p in agg.items() if len(p) >= 10)
    print(f"合格 scope 数 = {tot_scope}（平台要求 ≥3）｜总暴露 = {sum(sum(p) for p in agg.values()):,} 点")

    # ---- 差异 ----
    cur_keys = {k for k, al in cur.items() if len([x for x in al if x['pts'] > 1]) >= 10}
    opt_keys = {k for k, p in agg.items() if len(p) >= 10}
    add = sorted(opt_keys - cur_keys)
    drop = sorted(cur_keys - opt_keys)
    print("\n【差异】")
    if not add and not drop:
        print("  scope 集合一致")
    for k in add:
        print(f"  + 应新增 scope {k[0]}D{k[1]}：ACTIVE {len(cur.get(k, []))} 颗，可再 +{TOTAL:,} 点暴露")
    for k in drop:
        print(f"  - 应撤掉 scope {k[0]}D{k[1]}")

    # 每个共同 scope 内：应分但当前=1 的
    for k in sorted(opt_keys & cur_keys):
        opt_ids = {e["alpha_id"] for e in plan if (e["region"], e["delay"]) == k}
        zero = [x for x in cur.get(k, []) if x["pts"] <= 1 and x["id"] in opt_ids]
        extra = [x for x in cur.get(k, []) if x["pts"] > 1 and x["id"] not in opt_ids]
        if zero or extra:
            print(f"  ~ {k[0]}D{k[1]}：应分未分 {len(zero)} 颗 / 多分 {len(extra)} 颗")

    # 被 prod 剔除的黑名单
    ex_al = [(k, x) for k, al in cur.items() for x in al if x["prod"] is not None and x["prod"] >= a.prod_max]
    if ex_al:
        print(f"\n【prod≥{a.prod_max} 被剔除】{len(ex_al)} 颗：")
        for k, x in sorted(ex_al, key=lambda t: -t[1]["prod"])[:30]:
            print(f"  {x['id']}  {k[0]}D{k[1]}  prod={x['prod']:.4f}  IS={x['sharpe']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
