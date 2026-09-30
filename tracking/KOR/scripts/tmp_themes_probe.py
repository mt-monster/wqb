# -*- coding: utf-8 -*-
"""探测 Power Pool themes 端点。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

CANDS = [
    "https://api.worldquantbrain.com/themes",
    "https://api.worldquantbrain.com/alphas/themes",
    "https://api.worldquantbrain.com/competitions/themes",
    "https://api.worldquantbrain.com/power-pool/themes",
    "https://api.worldquantbrain.com/users/self/themes",
    "https://api.worldquantbrain.com/events/themes",
]

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for url in CANDS:
        r = await brain_client._request("GET", url)
        print(f"{r.status_code} | {url}")
        if r.status_code == 200:
            t = r.text[:600]
            print("   ", t)
        elif r.status_code not in (404,):
            print("   ", r.text[:200])

asyncio.run(main())
