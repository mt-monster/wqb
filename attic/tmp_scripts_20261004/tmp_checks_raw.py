import asyncio, os, sys, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        # 1) alpha detail
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        is_ = d.get("is", {}) or {}
        print(f"=== {aid} (is_.checks) ===")
        for c in is_.get("checks", []):
            print("   ", c.get("name"), c.get("result"), c.get("value"), "limit", c.get("limit"))
        # 2) /check endpoint
        r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/check")
        print(f"   /check -> {r2.status_code}")
        if r2.status_code == 200 and r2.text.strip():
            print("   ", json.dumps(r2.json(), ensure_ascii=False)[:1200])
asyncio.run(main())
