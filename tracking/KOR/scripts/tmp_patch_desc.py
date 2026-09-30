# -*- coding: utf-8 -*-
"""诊断：直接 PATCH description 并打印平台原始响应。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

DESC = (
    "Idea: Capture short-selling pressure divergence in Korean equities by measuring the ratio "
    "of inactive sell amount to inactive buy amount from the short interest dataset.\n\n"
    "Rationale for data used: The shrt38 short interest dataset provides stock-level inactive sell "
    "and buy amounts which reflect actual settlement-side pressure from short sellers; the ratio "
    "normalizes for firm size and gives a cross-sectionally comparable measure of one-sided selling.\n\n"
    "Rationale for operators used: vec_avg aggregates field vectors to a scalar, divide forms the "
    "dimensionless sell/buy ratio, group_rank within subindustry neutralizes sector composition, and "
    "hump delays trading to decorrelate the timing of trades from crowded short-interest signals."
)

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    aid = sys.argv[1]
    payload = {"regular": {"description": DESC}}
    print("发送 payload keys:", list(payload.keys()), "desc len:", len(DESC))
    r = await brain_client._request("PATCH", f"https://api.worldquantbrain.com/alphas/{aid}", json=payload)
    print("HTTP", r.status_code)
    print("RESP:", r.text[:800])
    await asyncio.sleep(3)
    rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
    d = rr.json()
    print("回读 desc_len:", len(d.get("description") or ""))
    print("回读 regular:", json.dumps(d.get("regular"), ensure_ascii=False)[:300])

asyncio.run(main())
