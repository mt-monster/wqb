# -*- coding: utf-8 -*-
"""为 PP 候选写入合规 description（≥100 字符，三段式）并回读 regular.description。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

DESC = (
    "Idea: This alpha captures short-selling pressure in Korean equities by measuring the ratio of "
    "inactive sell amount to inactive buy amount reported in the Korean short interest dataset, "
    "then ranking the ratio within sector groups so that only relative pressure is traded.\n\n"
    "Rationale for data used: The shrt38 short interest dataset reports settlement-side inactive sell "
    "and buy amounts at stock level. Their ratio isolates one-sided selling pressure that is comparable "
    "across firms of different sizes, which is the economically meaningful quantity for short interest.\n\n"
    "Rationale for operators used: vec_avg collapses the vector fields to scalar values, divide forms a "
    "dimensionless ratio, group_rank neutralizes sector composition, and hump limits day-to-day changes "
    "so that the timing of trades is decorrelated from crowded short-interest signals."
)

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        r = await brain_client._request("PATCH", f"https://api.worldquantbrain.com/alphas/{aid}",
                                        json={"regular": {"description": DESC}})
        print(f"{aid} PATCH {r.status_code}")
        await asyncio.sleep(2)
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = rr.json()
        got = (d.get("regular") or {}).get("description")
        print(f"   回读 desc_len={len(got or '')} 头={ (got or '')[:70] }")

asyncio.run(main())
