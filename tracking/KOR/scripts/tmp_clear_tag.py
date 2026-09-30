# -*- coding: utf-8 -*-
"""移除 qMxaLJpv 的 PowerPoolSelected 标签（使其走 REGULAR 提交通道）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    aid = sys.argv[1]
    # 读当前 tags
    r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
    d = r.json()
    cur = d.get("tags") or []
    print("当前 tags:", cur)
    new_tags = [t for t in cur if t != "PowerPoolSelected"]
    print("新 tags:", new_tags)
    rr = await brain_client._request("PATCH", f"https://api.worldquantbrain.com/alphas/{aid}",
                                     json={"tags": new_tags})
    print("PATCH", rr.status_code, rr.text[:200])
    await asyncio.sleep(2)
    r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
    print("回读 tags:", r2.json().get("tags"))

asyncio.run(main())
