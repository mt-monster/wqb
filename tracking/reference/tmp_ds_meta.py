# -*- coding: utf-8 -*-
"""查 pattern_scores 数据集的官方描述（理解字段语义）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    r = await brain_client._request("GET",
        "https://api.worldquantbrain.com/data-sets/pattern_scores?instrumentType=EQUITY&region=EUR&delay=1&universe=TOP2500")
    print(r.status_code)
    d = r.json()
    for k in ("id","name","description","category","subcategory","fieldCount","alphaCount","userCount","coverage","valueScore","pyramidMultiplier"):
        print(f"  {k}: {str(d.get(k))[:400]}")
asyncio.run(main())
