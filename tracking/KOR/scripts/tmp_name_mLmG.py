# -*- coding: utf-8 -*-
"""补写 mLmGQEq9 的 name（提交前置：name 非空）。"""
import asyncio, sys, os, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    aid = "mLmGQEq9"
    name = "KOR SI Avg Sell-Buy Ratio Sector Hump Decay20"
    r = await brain_client._request(
        "PATCH", f"https://api.worldquantbrain.com/alphas/{aid}",
        json={"name": name},
    )
    print("PATCH", r.status_code, r.text[:200])
    r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
    reg = (r2.json().get("regular") or {})
    print("verify name:", repr(reg.get("name")), "desc_len:", len(reg.get("description") or ""))

asyncio.run(main())
