#!/usr/bin/env python
"""扫描当前已分配（pts>1）中 investability Sharpe < 阈值 的 alpha，按区分组。"""
from __future__ import annotations

import asyncio
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "world-quant-brain-mcp"))

THR = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0


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
d: dict = defaultdict(list)
for x in pool:
    st = x.get("settings") or {}
    isd = x.get("is") or {}
    if x.get("status") != "ACTIVE" or x.get("type") != "REGULAR":
        continue
    pts = x.get("osmosisPoints") or 0
    if pts <= 1:
        continue
    inv = (isd.get("investabilityConstrained") or {}).get("sharpe")
    if inv is None or inv >= THR:
        continue
    sv = isd.get("sharpe") or 0
    d[st.get("region")].append((x["id"], sv, inv, inv / sv if sv else 0, pts))

print(f"\n已分配 alpha 中 inv < {THR} 的清单\n")
for reg in sorted(d, key=lambda k: -len(d[k])):
    print(f"{reg}: {len(d[reg])} 颗，合计 {sum(t[4] for t in d[reg]):,} 点")
    for aid, sv, inv, ratio, pts in sorted(d[reg], key=lambda t: t[2]):
        print(f"   {aid:<10} IS={sv:<6} inv={inv:.3f}  ratio={ratio:.2f}  pts={pts:,}")
print(f"\n合计 {sum(len(v) for v in d.values())} 颗")
