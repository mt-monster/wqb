# -*- coding: utf-8 -*-
"""过线 4 族（prod<=0.7）代表：self_corr 本地复验 + submit_verdict 前置信息。"""
import asyncio
import json
import sys

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
PASSES = ["Vk65zLzG", "vRk6og8b", "blRnKEk6", "883Y3bAW"]
OUT = r"D:\coding\traeCN_project\wqb\logs\_triage_pass4.json"


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()
    res = {}
    for aid in PASSES:
        rec = {}
        try:
            sc = await brain.check_self_correlation(aid, threshold=0.7)
            rec['self_corr'] = {"max": sc.get("max_correlation"), "pass": sc.get("passes_check"),
                                "status": sc.get("status")}
            d = await brain.get_alpha_details(aid)
            iss = d.get("is") or {}
            checks = {c.get("name"): c for c in (iss.get("checks") or [])}
            rec['metrics'] = {"sharpe": iss.get("sharpe"), "fitness": iss.get("fitness"),
                              "two_year_sharpe": (checks.get("LOW_2Y_SHARPE") or {}).get("value"),
                              "margin": iss.get("margin"), "turnover": iss.get("turnover")}
            rec['platform'] = f"{d.get('status')}/{d.get('stage')}"
            print(f"{aid}: self={rec['self_corr']} metrics={rec['metrics']} {rec['platform']}")
        except Exception as e:
            rec['error'] = str(e)[:150]
            print(f"{aid}: ERROR {str(e)[:100]}")
        res[aid] = rec
        json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


asyncio.run(main())
