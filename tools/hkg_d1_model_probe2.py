# -*- coding: utf-8 -*-
"""HKG D1 Model 探针第二批（2026-09-29）：用平台真实字段。

发现：model192 HKG 平台 0 字段（DB 幽灵），model262 真实 139 字段（DB 2061 虚）。
新探针 4 条：
  - model262 预测水平/变化/不确定性 3 条（acae/aacr 科目，users 0-2）
  - model53 PD 期限结构斜率 1 条（单字段族价差，经济含义：短期信用压力）
累计探针 6 条（fast_kill 线 8）。
"""
import asyncio
import json
import sys

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
OUT = r"D:\coding\traeCN_project\wqb\logs\_hkg_d1_model_probe.json"

BASE = {"instrumentType": "EQUITY", "region": "HKG", "universe": "TOP800", "delay": 1,
        "decay": 4, "neutralization": "SECTOR", "truncation": 0.08, "maxTrade": "ON",
        "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
        "language": "FASTEXPR", "visualization": False, "simulationMode": "QUICK"}

PROBES = [
    ("model262", "acae_predict",
     "group_rank(ts_zscore(ts_backfill(mdl262_acae_trkdpitdeltapredict_funda_predict, 66), 66), industry)"),
    ("model262", "aacr_predict_delta",
     "ts_rank(ts_delta(ts_backfill(mdl262_aacr_trkdpitdeltapredict_funda_predict, 66), 22), 66)"),
    ("model262", "aacr_madp_uncertainty",
     "multiply(-1, rank(ts_mean(ts_backfill(mdl262_aacr_trkdpitdeltapredict_funda_madp, 66), 22)))"),
    ("model53", "pd_term_slope",
     "multiply(-1, rank(subtract(ts_backfill(annualized_pd_1_month_jc7, 66), ts_backfill(annualized_pd_5_year_jc7, 66))))"),
]


def load_state():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {"probes": []}


def save_state(st):
    json.dump(st, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()
    state = load_state()

    payloads = []
    for ds, tag, expr in PROBES:
        if any(p.get("tag") == tag for p in state["probes"]):
            continue
        payloads.append({"type": "REGULAR", "settings": dict(BASE), "regular": expr})
        state["probes"].append({"dataset": ds, "field": tag, "tag": tag, "expr": expr})
    if payloads:
        batch = await brain.batch_create_simulations(payloads)
        new = [p for p in state["probes"] if not p.get("sim_id")]
        for p, r in zip(new, batch["results"]):
            p["sim_id"] = r.get("simulation_id")
            p["submitted"] = r.get("ok")
            if not r.get("ok"):
                p["error"] = r.get("error") or f"HTTP {r.get('status_code')}"
        save_state(state)
        print(f"[submit] {batch['submitted']}/{batch['total']} 已提交")

    for p in state["probes"]:
        if p.get("alpha_id") or p.get("submitted") is False:
            continue
        sid = p.get("sim_id")
        waited = 0
        while waited < 900:
            r = await brain._request('GET', f"{brain.base_url}/simulations/{sid}")
            d = brain._response_payload(r) or {}
            if d.get("status") == "COMPLETE" and d.get("alpha"):
                p["alpha_id"] = d["alpha"]
                break
            if d.get("status") in ("ERROR", "FAIL"):
                p["error"] = str(d.get("message"))[:150]
                break
            await asyncio.sleep(15)
            waited += 15
        print(f"[sim] {p.get('tag')} -> {p.get('alpha_id') or p.get('error') or 'TIMEOUT'}")
        save_state(state)

    for p in state["probes"]:
        aid = p.get("alpha_id")
        if not aid or p.get("metrics"):
            continue
        d = await brain.get_alpha_details(aid)
        iss = d.get("is") or {}
        p["metrics"] = {"sharpe": iss.get("sharpe"), "fitness": iss.get("fitness"),
                        "turnover": iss.get("turnover"), "margin": iss.get("margin")}
        save_state(state)
        print(f"[metrics] {aid}: {p['metrics']}")

    print("\n=== 全部探针汇总 ===")
    for p in state["probes"]:
        m = p.get("metrics") or {}
        print(f"  {p['dataset']:<10} {(p.get('tag') or p.get('field',''))[:26]:<26} alpha={p.get('alpha_id') or 'FAIL'} "
              f"S={m.get('sharpe')} F={m.get('fitness')} tvr={m.get('turnover')}")


asyncio.run(main())