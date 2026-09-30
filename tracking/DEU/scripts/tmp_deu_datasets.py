# -*- coding: utf-8 -*-
"""拉取 DEU/D1 可用数据集清单（TOP500），按 alphaCount 排序，识别 PPA 合格数据集。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows = []
    off = 0
    while True:
        url = (f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region=DEU"
               f"&delay=1&universe=TOP500&limit=50&offset={off}")
        r = await brain_client._request("GET", url)
        if r.status_code != 200:
            print("ERR", r.status_code, r.text[:200]); break
        d = r.json()
        rs = d.get("results") or []
        rows.extend(rs)
        if not rs or off + 50 >= (d.get("count") or 0):
            break
        off += 50
    print("total datasets:", len(rows))
    rows.sort(key=lambda x: (x.get("alphaCount") or 0))
    for x in rows:
        cat = x.get("category")
        cid = cat.get("id") if isinstance(cat, dict) else cat
        print(f"  id={x.get('id')} {x.get('name')!r} cat={cid} "
              f"fields={x.get('fieldCount')} alphas={x.get('alphaCount')} users={x.get('userCount')} cov={(x.get('coverage') or 0):.3f}")


asyncio.run(main())
