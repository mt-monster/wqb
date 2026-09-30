import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    from tools_sim import lookINTO_SimError_message
    await brain_client.ensure_authenticated()
    resp = await brain_client._request("GET", "https://api.worldquantbrain.com/simulations/2ZXB50e9P4C9bWMe5y2hJZT")
    ch = resp.json().get("children",[])
    locs = [f"https://api.worldquantbrain.com/simulations/{c}" for c in ch[:4]]
    r = await lookINTO_SimError_message(locs)
    for x in r.get("results",[]):
        print("ERR:", json.dumps(x.get("error"), ensure_ascii=False)[:200], "| status:", x.get("status"))
asyncio.run(main())
