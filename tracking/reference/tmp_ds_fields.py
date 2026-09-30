# -*- coding: utf-8 -*-
"""拉取某区域某数据集的字段清单 + 打印该区域合法 universe（config.py 权威）。"""
import asyncio, json, os, sys
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def main():
    region = sys.argv[1]
    ds = sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else None
    uni = sys.argv[4] if len(sys.argv) > 4 else "TOP2500"
    # universe
    try:
        sys.path.insert(0, REPO)
        from wqb.config import REGIONS
        print("universes:", REGIONS.get(region, {}).get("universes"))
    except Exception as e:
        print("cfg err", e)
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    rows = []
    off = 0
    while True:
        r = await brain_client._request(
            "GET",
            f"https://api.worldquantbrain.com/data-fields?instrumentType=EQUITY&dataset.id={ds}"
            f"&region={region}&delay=1&universe={uni}&limit=50&offset={off}")
        if r.status_code != 200:
            print("ERR", r.status_code, r.text[:200]); break
        d = r.json()
        rs = d.get("results") or []
        rows.extend(rs)
        if len(rows) >= (d.get("count") or 0) or not rs:
            break
        off += 50
    print(f"total fields={len(rows)}")
    for x in rows[:80]:
        print(f"  {x.get('id'):50s} {x.get('type'):10s} cov={x.get('coverage')} users={x.get('userCount')} alphas={x.get('alphaCount')}")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        print("saved", out)


asyncio.run(main())
