# -*- coding: utf-8 -*-
"""新数据集 probe：price_signal_dl（Deep Learning Price Signal，cov 0.97，KOR a=51 / EUR a=3）。

先看字段，再构造 probe。
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def fetch(bc, ds, region, uni):
    rows, off = [], 0
    while True:
        url = (f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region={region}"
               f"&delay=1&universe={uni}&dataset.id={ds}&limit=50&offset={off}")
        r = await bc._request("GET", url)
        if r.status_code != 200:
            print(f"[{region}/{ds}] ERR {r.status_code}"); return rows
        d = r.json(); rs = d.get("results") or []
        rows.extend(rs)
        if not rs or off + 50 >= (d.get("count") or 0):
            break
        off += 50
    return rows


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for region, uni in [("KOR", "TOP600"), ("EUR", "TOPCS1600")]:
        for ds in ["price_signal_dl"]:
            rows = await fetch(brain_client, ds, region, uni)
            print(f"\n=== {region}/{ds}: {len(rows)} fields ===")
            for x in rows[:40]:
                print(f"  {x.get('id'):40s} {x.get('type'):8s} cov={(x.get('coverage') or 0):.3f} u={x.get('userCount')} a={x.get('alphaCount')}  {(x.get('description') or '')[:40]}")


asyncio.run(main())
