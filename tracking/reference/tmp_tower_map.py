# -*- coding: utf-8 -*-
"""建立 (region, dataset_id) -> category 映射，并统计 261 候选池的塔归属。

只用平台 dataset 元信息（category.name）+ 本地候选池，不做任何本地 alphas 表的塔推断
（塔归属来自平台 pyramid 匹配，与 datasets.category 不等价，但 category 是 dataset 的固有属性）。
"""
import sys, os, asyncio, json, sqlite3, re
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
from brain_api import brain_client

MIX_PAT = re.compile(r"add\s*\(\s*multiply|multiply\s*\(\s*0?\.\d|\*\s*0\.\d+\s*\+|\+\s*0\.\d+\s*\*", re.I)

REGION_NAME = {1: "USA", 2: "KOR", 3: "ASI", 4: "MEA", 5: "IND", 6: "EUR",
               7: "GBR", 8: "GLB", 9: "HKG", 10: "DEU"}


async def go():
    await brain_client.ensure_authenticated()

    # 1) 拉全部 dataset 元信息 -> {(region,name): category}
    ds_cat = {}
    for region in ["IND", "KOR", "ASI", "USA", "EUR", "GBR", "GLB", "HKG", "DEU", "JPN", "CHN", "TWN", "MEA"]:
        off = 0
        while True:
            r = await brain_client._request(
                "GET",
                f"https://api.worldquantbrain.com/data-sets?instrumentType=EQUITY&region={region}&delay=1&limit=50&offset={off}")
            if r.status_code != 200:
                break
            d = r.json()
            res = d.get("results") or []
            for x in res:
                cat = (x.get("category") or {})
                key = (region, str(x.get("id")))
                ds_cat[key] = cat.get("name") if isinstance(cat, dict) else cat
            if len(res) < 50:
                break
            off += 50

    json.dump({f"{k[0]}|{k[1]}": v for k, v in ds_cat.items()},
              open(os.path.join(REPO, "tracking", "reference", "ds_category_map.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"[ds] 拉取 {len(ds_cat)} 个 (region,dataset)->category")

    # 2) 候选池
    c = sqlite3.connect(os.path.join(REPO, "data", "wqb.db")); c.row_factory = sqlite3.Row
    rows = c.execute("""SELECT alpha_id, expression, sharpe, fitness, two_year_sharpe, region_id,
        dataset_id, universe, neutralization, turnover, sub_universe_sharpe, prod_correlation, self_correlation
      FROM alphas WHERE sharpe >= 1.58 AND two_year_sharpe >= 1.58 AND fitness >= 1.0
        AND soft_deleted = 0 AND (prod_correlation IS NULL)""").fetchall()

    kosher = [dict(r) for r in rows if not MIX_PAT.search(r["expression"] or "")]
    print(f"[pool] prod未测={len(rows)}  无混腿={len(kosher)}")

    # 3) 按 (region, category) 聚合
    from collections import defaultdict
    agg = defaultdict(list)
    for a in kosher:
        rn = REGION_NAME.get(a["region_id"], str(a["region_id"]))
        cat = ds_cat.get((rn, str(a["dataset_id"])), "?")
        agg[(rn, cat)].append(a)

    print("\n=== 候选池 (region, category) 分布 ===")
    for k in sorted(agg, key=lambda k: -len(agg[k])):
        print(f"  {k[0]:4}/{k[1] or '?':22} n={len(agg[k]):4}  bestS={max(a['sharpe'] for a in agg[k])}")


asyncio.run(go())
