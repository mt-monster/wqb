import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ["vRjz9Vla", "Grl8X3bQ", "xAjzVm3q", "Wj7X3WbN"]:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        is_ = d.get("is") or {}
        print(f"\n{aid}: status={d.get('status')} S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
        print(f"  pyramids={json.dumps(d.get('pyramids'), ensure_ascii=False)}")
        print(f"  settings={json.dumps({k:(d.get('settings') or {}).get(k) for k in ['region','universe','neutralization','decay','truncation']}, ensure_ascii=False)}")
        print(f"  expr={(d.get('regular') or {}).get('code','')[:150]}")
asyncio.run(main())
