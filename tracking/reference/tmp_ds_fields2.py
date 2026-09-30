# -*- coding: utf-8 -*-
"""拉某数据集的字段清单（data-fields，覆盖 category/type/coverage/userCount/alphaCount）。
用法: python tmp_ds_fields2.py <REGION> <DELAY> <DATASET_ID> [limit]
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    reg = sys.argv[1] if len(sys.argv) > 1 else "KOR"
    delay = sys.argv[2] if len(sys.argv) > 2 else "1"
    ds = sys.argv[3] if len(sys.argv) > 3 else "insiders5"
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows = []
    off = 0
    while off < 600:
        url = (f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region={reg}"
               f"&delay={delay}&universe=TOP3000&dataset.id={ds}&limit=50&offset={off}")
        r = await brain_client._request("GET", url)
        if r.status_code != 200:
            print(f"HTTP {r.status_code}: {r.text[:200]}")
            break
        d = r.json()
        rs = d.get("results") or []
        if not rs: break
        rows += rs
        if not d.get("next"): break
        off += 50
    print(f"{reg}/{ds}: {len(rows)} fields")
    rows.sort(key=lambda x: -((x.get("userCount") or 0)))
    for f in rows:
        print(f"  {f.get('id'):48s} type={f.get('type','?'):8s} cov={f.get('coverage')} "
              f"uC={f.get('userCount')} aC={f.get('alphaCount')}  {(f.get('description') or '')[:50]}")
    out = os.path.join(REPO, f"tracking/reference/fields_{reg}_{ds}.json")
    with open(out, "w", encoding="utf-8") as fp:
        json.dump(rows, fp, ensure_ascii=False, indent=1)
    print("SAVED", out)

asyncio.run(main())
