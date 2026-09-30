import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", "https://api.worldquantbrain.com/simulations/2lF9WjbUf4PfafnfxnCUJKs")
    d = r.json()
    for ch in (d.get("children") or [])[:3]:
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{ch}")
        dd = rr.json()
        print(json.dumps(dd, ensure_ascii=False)[:600])
        print("---")
asyncio.run(main())
