# -*- coding: utf-8 -*-
"""数据探查: 拉区域 dataset 的字段清单。用法: python tmp_explore_fields.py <REGION> <dataset_id>"""
import sys, os, asyncio
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
from brain_api import brain_client


async def go():
    region = sys.argv[1]; dsid = sys.argv[2]
    delay = sys.argv[3] if len(sys.argv) > 3 else "1"
    await brain_client.ensure_authenticated()
    r = await brain_client._request(
        "GET",
        f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region={region}&delay={delay}&dataset.id={dsid}&limit=100")
    print("HTTP", r.status_code)
    d = r.json()
    res = d if isinstance(d, list) else (d.get("results") or [])
    print(f"=== {region}/{dsid} fields: {len(res)} ===")
    for x in res:
        print(f"  {str(x.get('id')):45} type={str(x.get('type')):8} cov={(x.get('coverage') or 0):.2f} "
              f"users={x.get('userCount')} alphas={x.get('alphaCount')}")
        desc = (x.get("description") or "").replace("\n", " ")[:100]
        if desc:
            print(f"      {desc}")


asyncio.run(go())
