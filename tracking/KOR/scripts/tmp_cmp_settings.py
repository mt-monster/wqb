# -*- coding: utf-8 -*-
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
IDS = sys.argv[1:]
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in IDS:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        s = d.get("settings") or {}
        print(f"=== {aid} status={d.get('status')} type={d.get('type')}")
        print(f"    expr: {(d.get('regular') or {}).get('code','')[:180]}")
        print(f"    settings: {json.dumps(s, ensure_ascii=False)}")
        reg = d.get("regular") or {}
        print(f"    desc_len={len(reg.get('description') or '')}")
asyncio.run(main())
