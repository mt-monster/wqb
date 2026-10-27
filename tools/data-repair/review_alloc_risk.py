#!/usr/bin/env python
"""当前已分配组合的两大风险体检：
  1) investability 衰减 ≥60%（官方建议剔除）—— 有多少颗仍在拿权重
  2) 数据集集中度（官方：Diversify across datasets，避免同跌）
"""
from __future__ import annotations

import asyncio
import os
import re
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import sys
from collections import Counter, defaultdict

_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))

from wqb.db_conn import connect as db_connect  # noqa: E402

DS_RE = re.compile(r"\b([a-z][a-z0-9]*?\d+)_[a-z0-9_]+")


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
    pool = asyncio.run(fetch_pool())
    act = [x for x in pool if x.get("status") == "ACTIVE" and x.get("type") == "REGULAR"]

    # 2026-10-27：原先写 `"data/wqb.db"`（cwd 相对），换个目录跑就静默指向不存在的库。
    con = db_connect(os.path.join(_ROOT, "data", "wqb.db"), readonly=True)
    con.row_factory = sqlite3.Row
    expr = {r["alpha_id"]: (r["expression"] or "") for r in con.execute(
        "SELECT alpha_id, expression FROM alphas WHERE expression IS NOT NULL").fetchall()}
    dsid = {r["alpha_id"]: r["dataset_id"] for r in con.execute(
        "SELECT alpha_id, dataset_id FROM alphas") .fetchall()}
    con.close()

    by: dict = defaultdict(list)
    for x in act:
        st = x.get("settings") or {}
        isd = x.get("is") or {}
        prod = isd.get("prodCorrelation")
        if prod is None:
            prod = x.get("prod")
        inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
        pts = x.get("osmosisPoints") or 0
        if pts <= 1:
            continue
        by[(st.get("region"), st.get("delay"))].append({
            "id": x.get("id"), "inv": inv, "is": isd.get("sharpe") or 0.0,
            "to": isd.get("turnover") or 0.0, "prod": prod, "pts": pts,
        })

    print("\n【1】investability 衰减体检（官方：衰减≥60% 应剔除）")
    print(f"{'scope':<9}{'已分配':>7}{'有inv':>7}{'≥60%衰减':>10}{'其权重占比':>12}")
    print("-" * 52)
    tot_bad_w = tot_w = 0
    for k in sorted(by, key=lambda k: -len(by[k])):
        al = by[k]
        w = sum(x["pts"] for x in al)
        have = [x for x in al if x["inv"] is not None and x["is"] > 0]
        bad = [x for x in have if x["inv"] / x["is"] < 0.40]
        bw = sum(x["pts"] for x in bad)
        tot_bad_w += bw
        tot_w += w
        print(f"{k[0]}D{k[1]:<7}{len(al):>7}{len(have):>7}{len(bad):>10}"
              f"{(bw / w * 100 if w else 0):>11.1f}%")
    print("-" * 52)
    print(f"合计：{tot_bad_w:,} / {tot_w:,} 点 = {tot_bad_w / tot_w * 100:.1f}% 压在衰减≥60% 的 alpha 上")

    print("\n【2】数据集集中度（每 scope 内按数据集前缀统计权重）")
    for k in sorted(by, key=lambda k: -len(by[k])):
        al = by[k]
        w = sum(x["pts"] for x in al)
        c: Counter = Counter()
        for x in al:
            e = expr.get(x["id"], "")
            m = DS_RE.findall(e)
            key = m[0] if m else (dsid.get(x["id"]) or "?")
            c[key] += x["pts"]
        top = c.most_common(5)
        share = sum(v for _, v in top) / w * 100 if w else 0
        print(f"\n  {k[0]}D{k[1]}  n={len(al)}  数据集数={len(c)}  Top5 权重占比={share:.1f}%")
        for name, v in top:
            print(f"     {name:<12}{v / w * 100:>6.1f}%   ({v:,} 点)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
