# -*- coding: utf-8 -*-
"""确认 pwjpKGJ3 两个 buy_sell 字段在 KOR 的数据集归属（平台 /data-fields 权威）。"""
import asyncio
import json
import sqlite3
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
FIELDS = ["buy_sell_ratio_top20_250d_filled", "buy_sell_tx_count_ratio_all_60d_filled"]


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    con = sqlite3.connect(str(WQ_ROOT / "data" / "wqb.db"))
    cur = con.cursor()
    cur.execute("SELECT d.name, d.category FROM datasets d "
                "JOIN regions r ON r.id=d.region_id WHERE r.name='KOR'")
    catmap = {n: c for n, c in cur.fetchall()}
    con.close()

    for f in FIELDS:
        # 尝试 1：单字段端点
        combos = [
            ("single-field", f"{brain.base_url}/data-fields/{f}",
             {"region": "KOR", "universe": "TOP600", "delay": 1}),
            ("list-search", f"{brain.base_url}/data-fields",
             {"region": "KOR", "delay": 1, "search": f, "limit": 10, "offset": 0}),
        ]
        for tag, url, params in combos:
            try:
                r = await brain._request("GET", url, params=params)
                txt = r.text
                if "Invalid" in txt or not txt.strip():
                    print(f"[{f}] {tag}: 失败 ({txt[:60]})")
                    await asyncio.sleep(2)
                    continue
                j = r.json()
                items = j if isinstance(j, list) else [j]
                res = [x for x in items if isinstance(x, dict)]
                ds = res[0].get("dataset") if res else None
                dsid = ds if isinstance(ds, str) else (ds or {}).get("id")
                print(f"[{f}] {tag}: dataset={dsid} category={catmap.get(dsid, '?')}")
                break
            except Exception as e:
                print(f"[{f}] {tag}: ERR {str(e)[:60]}")
                await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
