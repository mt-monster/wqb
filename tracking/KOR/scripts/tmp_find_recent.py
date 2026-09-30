import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET", "https://api.worldquantbrain.com/users/self/alphas?limit=12&order=-dateCreated")
    d = r.json()
    for a in d.get("results",[]):
        print(a.get("id"), a.get("dateCreated"), str(a.get("regular",{}).get("code"))[:70] if isinstance(a.get("regular"),dict) else "")
asyncio.run(main())
