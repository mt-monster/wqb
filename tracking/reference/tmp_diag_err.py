# -*- coding: utf-8 -*-
"""单条提交每个 diag1 表达式，定位 ERROR 真因（隔离并发干扰）。"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    items = json.load(open("tracking/reference/exprs_eur_diag1.json", encoding="utf-8"))
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for lab, expr in items:
        payload = {"type": "REGULAR", "settings": {
            "instrumentType": "EQUITY", "region": "EUR", "universe": "TOP2500",
            "delay": 1, "decay": 4, "neutralization": "SUBINDUSTRY",
            "truncation": 0.02, "pasteurization": "ON", "nanHandling": "ON",
            "unitHandling": "VERIFY", "language": "FASTEXPR", "visualization": False, "testPeriod": "P0Y0M"},
            "regular": expr}
        r = await brain_client._request("POST", "https://api.worldquantbrain.com/simulations", json=payload)
        print(f"{lab:20s} {r.status_code} {r.text[:200]}", flush=True)
        await asyncio.sleep(3)
asyncio.run(main())
