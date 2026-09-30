# -*- coding: utf-8 -*-
"""按 progress_id 回查 multi-simulation 子 alpha 真实 ID + 顺序。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    wf = sys.argv[1]
    with open(wf, encoding="utf-8") as f:
        wave = json.load(f)
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for b in wave["batches"]:
        pid = b["progress_id"]
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = r.json()
        children = d.get("children") or []
        print(f"\n[{b['group']}] pid={pid} status={d.get('status')} n_children={len(children)}")
        for label, cid in zip(b["ids"], children):
            rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{cid}")
            dd = rr.json()
            aid = dd.get("alpha")
            print(f"  {label:22s} -> {aid}  ({dd.get('status')})")
            await asyncio.sleep(0.3)
asyncio.run(main())
