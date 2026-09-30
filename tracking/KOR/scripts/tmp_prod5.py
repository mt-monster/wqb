import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        got=False
        for attempt in range(10):
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
            if r.status_code==200 and r.text.strip():
                d=r.json(); print(f"{aid} PROD: max={d.get('max')}"); got=True; break
            await asyncio.sleep(20)
        if not got: print(f"{aid} PROD 超时")
asyncio.run(main())
