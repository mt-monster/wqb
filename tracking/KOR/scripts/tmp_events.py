# -*- coding: utf-8 -*-
"""查询当前开放的 Power Pool 主题（events / competitions）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for url in [
        "https://api.worldquantbrain.com/events",
        "https://api.worldquantbrain.com/users/self/competitions",
    ]:
        print(f"\n=== {url} ===")
        r = await brain_client._request("GET", url)
        print("HTTP", r.status_code)
        if r.status_code == 200:
            print(json.dumps(r.json(), ensure_ascii=False, indent=1)[:3000])
        else:
            print(r.text[:300])

asyncio.run(main())
