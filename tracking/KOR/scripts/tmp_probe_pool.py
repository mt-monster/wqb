# -*- coding: utf-8 -*-
"""查 KOR SI 专项已入池 alpha 的表达式结构，避免重复族。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    ids = ["KPNo2lgl","E5pjx9q0","mLmGQEq9","d5bMPkWY","omLjG1M5","wpZkk1Mp","A1NXddRw"]
    for aid in ids:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        reg = d.get("regular") or {}
        s = d.get("settings") or {}
        print(f"{aid} [{d.get('status')}] nu={s.get('neutralization')} dec={s.get('decay')} trunc={s.get('truncation')}")
        print(f"    {reg.get('code','')}")
asyncio.run(main())
