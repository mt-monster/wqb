#!/usr/bin/env python
"""列出全部 type=SUPER 且 osmosisPoints>0 的 alpha 及其指标，判断是否该参与分配。"""
from __future__ import annotations

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))


async def go() -> list:
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


pool = asyncio.run(go())
print("=== type=SUPER 且 pts>0 的全部明细 ===\n")
print(f"{'id':<11}{'scope':<9}{'pts':>8}{'status':<9}{'IS':>7}{'inv':>7}{'prod':>8}{'sub':<12}")
tot = 0
for x in sorted(pool, key=lambda a: -(a.get("osmosisPoints") or 0)):
    if x.get("type") != "SUPER":
        continue
    pts = x.get("osmosisPoints") or 0
    if pts <= 0:
        continue
    st = x.get("settings") or {}
    isd = x.get("is") or {}
    prod = isd.get("prodCorrelation")
    if prod is None:
        prod = x.get("prod")
    inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
    print(f"{x['id']:<11}{st.get('region')}D{st.get('delay'):<7}{pts:>8,}"
          f"{x.get('status'):<9}{(isd.get('sharpe') or 0):>7.2f}"
          f"{(inv if inv is not None else -1):>7.3f}"
          f"{(prod if prod is not None else -1):>8.4f}  {(x.get('dateSubmitted') or '')[:10]}")
    tot += pts
print(f"\n合计 {tot:,} 点")
