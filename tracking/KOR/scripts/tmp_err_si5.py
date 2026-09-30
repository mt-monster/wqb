import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    resp = await brain_client._request("GET", "https://api.worldquantbrain.com/simulations/2ZXB50e9P4C9bWMe5y2hJZT")
    d = resp.json()
    ch = d.get("children",[])
    print("n_children:", len(ch), "type:", type(ch[0]).__name__)
    for cid in ch[:3]:
        r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{cid}")
        j = r2.json()
        print("\n---", cid, "status=", j.get("status"))
        print(json.dumps(j, ensure_ascii=False)[:900])
asyncio.run(main())
