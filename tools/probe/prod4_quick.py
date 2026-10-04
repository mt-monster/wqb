# -*- coding: utf-8 -*-
"""_prod4.py — 查询给定 alpha id 列表的 prod 相关性 + 直方图 0.6-0.7 桶。
用法: python logs/_prod4.py <id1> <id2> ...
"""
import sys, asyncio, json
sys.path.insert(0, "world-quant-brain-mcp")
from brain_api import brain_client as brain

IDS = sys.argv[1:]


async def one(aid):
    for attempt in range(4):
        r = await brain._request("GET", f"{brain.base_url}/alphas/{aid}/correlations/prod")
        t = (r.text or "").strip()
        if not t:
            await asyncio.sleep(15)
            continue
        try:
            d = r.json()
            if d:
                return d
        except Exception:
            pass
        await asyncio.sleep(15)
    return {}


async def main():
    await brain.ensure_authenticated()
    sem = asyncio.Semaphore(4)

    async def wrap(aid):
        async with sem:
            return aid, await one(aid)

    res = await asyncio.gather(*[wrap(a) for a in IDS])
    for aid, d in res:
        if not d:
            print(f"{aid:12s} prod=? (empty)")
            continue
        sch = d.get("schema") or {}
        mx = sch.get("max", d.get("max"))
        print(f"{aid:12s} prod_max={mx}")
        recs = d.get("records") or []
        # 打印 0.5-0.75 桶
        for row in recs:
            if isinstance(row, (list, tuple)) and len(row) >= 3:
                lo = row[0]
                try:
                    lof = float(lo)
                except Exception:
                    continue
                if 0.45 <= lof <= 0.75:
                    print(f"    bucket [{lo}, {row[1]})  n={row[2]}")


asyncio.run(main())
