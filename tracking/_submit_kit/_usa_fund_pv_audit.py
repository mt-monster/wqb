# -*- coding: utf-8 -*-
"""审计 USA/D1/FUNDAMENTAL(x5) 与 USA/D1/PV(x3) 的计入明细 + KOR buy_sell 字段归属。"""
import asyncio
import json
import sqlite3
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
TARGETS = ("USA/D1/FUNDAMENTAL", "USA/D1/PV")


def expr_of(a):
    code = a.get("regular")
    return (code.get("code") if isinstance(code, dict) else str(code)) or ""


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    out, off = [], 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"status": "ACTIVE", "limit": 100, "offset": off})
        arr = r.json().get("results") or []
        out.extend(arr)
        if len(arr) < 100 or off > 5000:
            break
        off += 100

    for t in TARGETS:
        print(f"\n===== {t} 计入明细 =====")
        for a in out:
            pys = [p.get("name") for p in (a.get("pyramids") or []) if p.get("name")]
            if t not in pys:
                continue
            print(f"  {a.get('id')} name={str(a.get('name'))[:24]:24s} "
                  f"sub={str(a.get('dateSubmitted'))[:10]} 挂塔数={len(pys)} 塔={pys}")
            print(f"      expr: {expr_of(a)[:110]}")

    # KOR buy_sell 字段归属
    con = sqlite3.connect(str(WQ_ROOT / "data" / "wqb.db"))
    cur = con.cursor()
    cur.execute("SELECT d.name, d.category FROM datasets d "
                "JOIN regions r ON r.id=d.region_id WHERE r.name='KOR'")
    catmap = {n: c for n, c in cur.fetchall()}
    con.close()
    for f in ("buy_sell_ratio_top20_250d_filled", "buy_sell_tx_count_ratio_all_60d_filled"):
        for tag, url, params in (
            ("single", f"{brain.base_url}/data-fields/{f}",
             {"region": "KOR", "universe": "TOP600", "delay": 1}),
            ("list", f"{brain.base_url}/data-fields",
             {"region": "KOR", "delay": 1, "search": f, "limit": 10, "offset": 0}),
        ):
            try:
                r = await brain._request("GET", url, params=params)
                txt = r.text
                if "Invalid" in txt or not txt.strip():
                    print(f"[{f}] {tag}: {txt[:50]}")
                    await asyncio.sleep(2)
                    continue
                j = r.json()
                items = [x for x in (j if isinstance(j, list) else [j]) if isinstance(x, dict)]
                ds = items[0].get("dataset") if items else None
                dsid = ds if isinstance(ds, str) else (ds or {}).get("id")
                print(f"[{f}] {tag}: dataset={dsid} category={catmap.get(dsid, '?')}")
                break
            except Exception as e:
                print(f"[{f}] {tag}: ERR {str(e)[:60]}")
                await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
