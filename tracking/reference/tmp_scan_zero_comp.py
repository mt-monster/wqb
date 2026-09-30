# -*- coding: utf-8 -*-
"""跨区域"零竞争数据集"扫描（按可产出性排序）。

筛选：coverage>=0.6, fieldCount>=8, alphaCount<=80
输出按 (region, alphaCount) 排序，标出 KOR/DEU/EUR/IND/ASI/GBR 批次。
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

TARGETS = {
    "KOR": "TOP600", "DEU": "TOP500", "EUR": "TOPCS1600",
    "IND": "TOP500", "ASI": "MINVOL1M", "GBR": "TOP3500",
}


async def fetch(bc, region, uni):
    rows, off = [], 0
    while True:
        url = (f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region={region}"
               f"&delay=1&universe={uni}&limit=50&offset={off}")
        r = await bc._request("GET", url)
        if r.status_code != 200:
            return rows
        d = r.json(); rs = d.get("results") or []
        rows.extend(rs)
        if not rs or off + 50 >= (d.get("count") or 0):
            break
        off += 50
    return rows


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    allout = {}
    for region, uni in TARGETS.items():
        rows = await fetch(brain_client, region, uni)
        cands = [x for x in rows if (x.get("coverage") or 0) >= 0.6
                 and (x.get("fieldCount") or 0) >= 8 and (x.get("alphaCount") or 0) <= 80]
        cands.sort(key=lambda x: (x.get("alphaCount") or 0))
        allout[region] = [{"id": x.get("id"), "name": x.get("name"),
                           "cat": (x.get("category") or {}).get("id") if isinstance(x.get("category"), dict) else x.get("category"),
                           "fields": x.get("fieldCount"), "alphas": x.get("alphaCount"),
                           "cov": round(x.get("coverage") or 0, 3)} for x in cands]
        print(f"\n=== {region} ({uni}) 合格 {len(cands)} ===")
        for c in allout[region][:12]:
            print(f"  {c['id']:26s} cat={c['cat']:14s} f={c['fields']:4d} a={c['alphas']:4d} cov={c['cov']:.3f}  {c['name'][:38]}")
    p = os.path.join(REPO, "tracking/reference/zero_competition_scan.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(allout, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nSAVED", p)


asyncio.run(main())
