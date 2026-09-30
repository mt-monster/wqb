# -*- coding: utf-8 -*-
"""列 EUR 区域 news / risk / other 类数据集（未亮塔靶向）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows = []
    off = 0
    while off < 400:
        r = await brain_client._request(
            "GET",
            f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region=EUR&delay=1"
            f"&universe=TOP2500&limit=50&offset={off}")
        if r.status_code != 200:
            print("ERR", r.status_code, r.text[:150]); break
        d = r.json()
        rs = d.get("results") or []
        rows.extend(rs)
        if len(rs) < 50:
            break
        off += 50
    print("total datasets:", len(rows))
    # 按 category 分
    from collections import defaultdict
    by = defaultdict(list)
    for x in rows:
        cat = (x.get("category") or {}).get("id") or "?"
        by[cat].append(x)
    for cat in ("news", "risk", "other", "sentiment", "institutions", "insiders"):
        lst = by.get(cat, [])
        print(f"\n=== {cat} ({len(lst)}) ===")
        for x in sorted(lst, key=lambda z: (z.get("alphaCount") or 0)):
            print(f"  {x.get('id'):26s} a={x.get('alphaCount'):4d} u={x.get('userCount'):5d} "
                  f"f={x.get('fieldCount'):4d} cov={x.get('coverage')}  {str(x.get('name'))[:38]}")


asyncio.run(main())
