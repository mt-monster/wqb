import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ["omLjG1M5","A1NXddRw","wpZkk1Mp"]:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        print(f"\n{aid}:")
        print("  pyramids:", json.dumps(d.get("pyramids"), ensure_ascii=False))
        print("  status:", d.get("status"))
        is_ = d.get("is") or {}
        print("  code:", str(d.get("regular",{}).get("code"))[:90])
asyncio.run(main())
