import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", "https://api.worldquantbrain.com/simulations/289ard7qW4DybL75olUaxPm")
    d = r.json()
    print("status:", d.get("status"))
    print("children:", json.dumps(d.get("children"), ensure_ascii=False)[:600])
    for ch in (d.get("children") or []):
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{ch}")
        dd = rr.json()
        print(f"  sim {ch}: status={dd.get('status')} err={json.dumps(dd.get('error') or dd.get('message'),ensure_ascii=False)[:200]}")
asyncio.run(main())
