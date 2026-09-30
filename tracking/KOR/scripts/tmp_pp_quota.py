# -*- coding: utf-8 -*-
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for ep in ["https://api.worldquantbrain.com/users/self/activities/submissions",
               "https://api.worldquantbrain.com/users/self"]:
        r = await brain_client._request("GET", ep)
        print(f"--- {ep} -> {r.status_code}")
        try:
            print(json.dumps(r.json(), ensure_ascii=False)[:2500])
        except Exception:
            print(r.text[:800])
asyncio.run(main())
