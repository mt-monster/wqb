# -*- coding: utf-8 -*-
"""拿全 other571 在 EUR 的 30 个字段。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows=[]; off=0
    while True:
        r = await brain_client._request("GET",
            f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&dataset.id=other571"
            f"&region=EUR&delay=1&universe=TOP2500&limit=50&offset={off}")
        if r.status_code!=200: print("ERR",r.status_code); break
        d=r.json(); rs=d.get("results") or []; rows+=rs
        if len(rs)<50: break
        off+=50
    print("fields:",len(rows))
    for x in rows:
        print(f"  {x.get('id'):38s} {x.get('type'):8s} cov={x.get('coverage')} a={x.get('alphaCount')} u={x.get('userCount')}")
    json.dump(rows, open("tracking/reference/EUR_other571_fields.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
asyncio.run(main())
