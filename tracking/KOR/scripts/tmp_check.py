# -*- coding: utf-8 -*-
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wb"
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
IDS = sys.argv[1:]
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in IDS:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        st = d.get("status")
        is_ = d.get("is") or {}
        checks = {c.get('name'): c.get('result') for c in is_.get('checks',[])}
        pyr = d.get("pyramids") or []
        if isinstance(pyr, dict): pyr = [pyr]
        pn = [p.get("name") for p in pyr if isinstance(p, dict)]
        print(f"{aid} status={st} S={is_.get('sharpe')} F={is_.get('fitness')} 2Y={is_.get('checks') and [c.get('value') for c in is_.get('checks',[]) if c.get('name')=='LOW_2Y_SHARPE']}")
        print(f"   FAILs: {[k for k,v in checks.items() if v=='FAIL']}  WARNs: {[k for k,v in checks.items() if v=='WARNING']}")
        print(f"   pyramids: {pn}")
asyncio.run(main())
