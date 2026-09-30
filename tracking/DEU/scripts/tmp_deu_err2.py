import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", "https://api.worldquantbrain.com/simulations/nOjpGko59h9gCtNpfUPBH")
    d = r.json()
    for ch in (d.get("children") or []):
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{ch}")
        dd = rr.json()
        print(f"  {ch}: status={dd.get('status')}")
        print(f"     keys={list(dd.keys())}")
        print(f"     error={json.dumps(dd.get('error'),ensure_ascii=False)[:300]}")
        print(f"     message={json.dumps(dd.get('message'),ensure_ascii=False)[:300]}")
        print(f"     raw={json.dumps(dd,ensure_ascii=False)[:400]}")
asyncio.run(main())
