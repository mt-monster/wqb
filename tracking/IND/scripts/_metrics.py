"""批量拉 alpha 的 is.check 明细（含 value/limit：sub / robust / 2Y 都在这里）+ 核心指标。
用法: python tracking/IND/scripts/_metrics.py <aid> [<aid> ...]
"""
import asyncio, sys, json
sys.path.insert(0, "world-quant-brain-mcp")
from brain_api import brain_client as brain

WANT = {"LOW_SHARPE","LOW_FITNESS","LOW_SUB_UNIVERSE_SHARPE","LOW_ROBUST_UNIVERSE_SHARPE",
        "IS_LADDER_SHARPE","CONCENTRATED_WEIGHT","LOW_2Y_SHARPE","CLUSTER_TEST","SELF_CORRELATION"}

async def main(ids):
    await brain.ensure_authenticated()
    out = []
    for aid in ids:
        r = await brain._request("GET", f"{brain.base_url}/alphas/{aid}")
        d = r.json(); isd = d.get("is") or {}
        row = {"aid": aid, "S": isd.get("sharpe"), "F": isd.get("fitness"),
               "TO": isd.get("turnover"), "margin": isd.get("margin"),
               "checks": {}, "fails": []}
        for c in (isd.get("checks") or []):
            n = c.get("name")
            if c.get("result") == "FAIL":
                row["fails"].append(n)
            if n in WANT:
                row["checks"][n] = {"r": c.get("result"), "v": c.get("value"), "l": c.get("limit")}
        print(f"{aid}  S={row['S']} F={row['F']} TO={row['TO']}  fails={row['fails']}")
        for n, cv in row["checks"].items():
            print(f"    {n:<28} {cv['r']:<8} value={cv['v']} limit={cv['l']}")
        out.append(row)
        await asyncio.sleep(4)
    json.dump(out, open("logs/_metrics_latest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved -> logs/_metrics_latest.json")

asyncio.run(main(sys.argv[1:]))
