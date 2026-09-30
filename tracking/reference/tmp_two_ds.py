# -*- coding: utf-8 -*-
"""查 acquisition_model / other571 在 EUR 的字段 + 数据集描述。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def meta(bc, ds):
    r = await bc._request("GET", f"https://api.worldquantbrain.com/data-sets/{ds}?instrumentType=EQUITY&region=EUR&delay=1&universe=TOP2500")
    if r.status_code == 200:
        d = r.json()
        print(f"\n### {ds}: {d.get('name')} | cat={(d.get('category') or {}).get('id')}")
        print("  desc:", str(d.get('description'))[:300])
async def fields(bc, ds):
    r = await bc._request("GET", f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&dataset.id={ds}&region=EUR&delay=1&universe=TOP2500&limit=50&offset=0")
    if r.status_code != 200:
        print(f"  [{ds}] fields ERR {r.status_code}"); return
    d = r.json()
    print(f"  fields count={d.get('count')}")
    for x in (d.get("results") or [])[:25]:
        print(f"    {x.get('id'):44s} {x.get('type'):8s} cov={x.get('coverage')} a={x.get('alphaCount')}")
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for ds in ("acquisition_model", "other571", "news54"):
        await meta(brain_client, ds)
        await fields(brain_client, ds)
        await asyncio.sleep(2)
asyncio.run(main())
