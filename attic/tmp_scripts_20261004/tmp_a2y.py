import asyncio, os, sys, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        is_ = d.get("is", {}) or {}
        print(f"=== {aid} === keys:", list(is_.keys()))
        print("  sharp:", is_.get("sharpe"), "fitness:", is_.get("fitness"), "turnover:", is_.get("turnover"))
        print("  full is_ checks:", json.dumps(is_.get("checks",[]), ensure_ascii=False)[:900])
asyncio.run(main())
