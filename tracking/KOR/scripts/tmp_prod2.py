import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ["gJblmzJl","Grb2nv13","YPbV2Zxw"]:
        got=False
        for attempt in range(8):
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
            if r.status_code==200 and r.text.strip():
                d=r.json()
                print(f"{aid} PROD: max={d.get('max')} n={len(d.get('records',[]))}")
                got=True; break
            await asyncio.sleep(25)
        if not got: print(f"{aid} PROD: 超时未返回")
        r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d3=r3.json()
        print(f"   pyramids:", json.dumps(d3.get("pyramids"), ensure_ascii=False))
asyncio.run(main())
