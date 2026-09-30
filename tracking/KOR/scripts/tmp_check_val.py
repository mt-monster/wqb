import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for pid in ["4l0ir239z4sd9P7xMlvmBf8","B9KEy5Hd57kcqrusH9rW0M","1iaXzU8GL5hxbDNYn4l2VZc","2Yserx6Gf5ey9MpnZsusV6X"]:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = r.json()
        aid = d.get("alpha")
        print(f"{pid}: status={d.get('status')} alpha={aid}")
        if aid:
            r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            is_ = (r2.json().get("is") or {})
            print(f"   S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
asyncio.run(main())
