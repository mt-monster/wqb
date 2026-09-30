# -*- coding: utf-8 -*-
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
IDS = ["KPNo2lgl","E5pjx9q0","mLmGQEq9","d5bMPkWY","omLjG1M5"]
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in IDS:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        is_ = d.get("is") or {}
        print(f"=== {aid} [{d.get('status')}]")
        for c in is_.get("checks", []):
            if c.get("name") in ("MATCHES_THEMES","MATCHES_PYRAMID","PROD_CORRELATION","SELF_CORRELATION","POWER_POOL_CORRELATION","PURE_POWER_POOL_THEME","REGULAR_SUBMISSION","POWER_POOL_SUBMISSION","POWER_POOL_MONTHLY_SUBMISSION"):
                print("   ", json.dumps(c, ensure_ascii=False))
asyncio.run(main())
