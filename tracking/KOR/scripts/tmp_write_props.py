# -*- coding: utf-8 -*-
"""写入 alpha 属性（name/color/tags/description）并**回读验证**（防静默丢弃）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

DESC = (
    "Idea: Capture short-selling pressure divergence in Korean equities by measuring the ratio "
    "of inactive sell amount to inactive buy amount from the short interest dataset.\n\n"
    "Rationale for data used: The shrt38 short interest dataset provides stock-level inactive sell "
    "and buy amounts which reflect the actual settlement-side pressure from short sellers; the ratio "
    "normalizes for firm size and gives a cross-sectionally comparable measure of one-sided selling.\n\n"
    "Rationale for operators used: vec_avg aggregates field vectors to a scalar, divide forms the "
    "dimensionless sell/buy ratio, group_rank within subindustry neutralizes sector composition, and "
    "hump delays trading to decorrelate the timing of trades from crowded short-interest signals."
)

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    aid = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    r = await brain_client.set_alpha_properties(
        aid, name=name, color="BLUE", tags=["PowerPoolSelected"], descriptions=DESC)
    print("PATCH status:", getattr(r, "status_code", "?"))
    if hasattr(r, "text"):
        print("PATCH body:", r.text[:400])
    # 回读
    await asyncio.sleep(2)
    rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
    d = rr.json()
    print("回读 name:", d.get("name"))
    print("回读 tags:", d.get("tags"))
    print("回读 desc_len:", len(d.get("description") or ""))
    print("回读 desc头:", (d.get("description") or "")[:120])

asyncio.run(main())
