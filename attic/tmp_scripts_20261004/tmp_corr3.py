# -*- coding: utf-8 -*-
"""查 prod 高相关桶的alpha明细（samples/max id）。"""
import asyncio, os, sys, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    aid=sys.argv[1]
    # 尝试 prod 相关明细端点
    for path in [f"alphas/{aid}/correlations/prod", f"alphas/{aid}/correlations/prod/samples"]:
        r=await brain_client._request("GET", f"https://api.worldquantbrain.com/{path}")
        print(f"--- {path} -> {r.status_code}")
        if r.status_code==200 and r.text.strip():
            try:
                d=r.json(); print(json.dumps(d,ensure_ascii=False)[:2000])
            except: print(r.text[:500])
asyncio.run(main())
