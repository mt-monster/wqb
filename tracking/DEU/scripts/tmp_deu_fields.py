# -*- coding: utf-8 -*-
"""拉取指定 DEU 数据集的字段清单（DEU/TOP500/D1）。
用法: python tmp_deu_fields.py other532 shortinterest3
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def fetch(bc, ds):
    rows = []
    off = 0
    while True:
        url = (f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&region=DEU"
               f"&delay=1&universe=TOP500&dataset.id={ds}&limit=50&offset={off}")
        r = await bc._request("GET", url)
        if r.status_code != 200:
            print(f"[{ds}] ERR {r.status_code} {r.text[:150]}"); return rows
        d = r.json()
        rs = d.get("results") or []
        rows.extend(rs)
        if not rs or off + 50 >= (d.get("count") or 0):
            break
        off += 50
    return rows


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    out = {}
    for ds in sys.argv[1:]:
        rows = await fetch(brain_client, ds)
        out[ds] = rows
        print(f"\n=== {ds}: {len(rows)} fields ===")
        for x in rows:
            print(f"  {x.get('id'):40s} type={x.get('type'):10s} cov={(x.get('coverage') or 0):.3f} "
                  f"u={x.get('userCount')} a={x.get('alphaCount')}  {(x.get('description') or '')[:50]}")
    p = os.path.join(REPO, "tracking/DEU/cache/deu_target_fields.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nSAVED", p)


asyncio.run(main())
