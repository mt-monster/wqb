# -*- coding: utf-8 -*-
"""检查候选 alpha 的 name/description 是否满足提交前置（name 非空 + description>=100 三段式）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    ids = sys.argv[1:]
    for aid in ids:
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        d = r.json()
        reg = d.get("regular") or {}
        nm = reg.get("name") or d.get("name")
        desc = reg.get("description") or ""
        is_ = d.get("is") or {}
        print(f"\n{aid}: status={d.get('status')} name={nm!r} desc_len={len(desc)}")
        print(f"   S={is_.get('sharpe')} F={is_.get('fitness')} T={is_.get('turnover')}")
        print(f"   pyramids={json.dumps(d.get('pyramids'), ensure_ascii=False)}")
        print(f"   settings={json.dumps({k:d.get('settings',{}).get(k) for k in ['region','universe','delay','neutralization','decay','truncation','instrumentType']}, ensure_ascii=False)}")

asyncio.run(main())
