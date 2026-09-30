import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ["YPbV2Zxw"]:
        # prod 相关性（长窗口轮询）
        for attempt in range(6):
            r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
            if r.status_code==200 and r.text.strip():
                d=r.json()
                print(f"{aid} PROD: max={d.get('max')} min={d.get('min')} n={len(d.get('records',[]))}")
                break
            else:
                print(f"  [{attempt}] status={r.status_code} body_empty={not r.text.strip()} 等 20s")
                await asyncio.sleep(20)
        # self 相关性
        r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/self")
        if r2.status_code==200 and r2.text.strip():
            d2=r2.json(); print(f"{aid} SELF: max={d2.get('max')}")
        # pyramid
        r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        print(f"{aid} pyramids:", json.dumps(r3.json().get("pyramids"), ensure_ascii=False))
asyncio.run(main())
