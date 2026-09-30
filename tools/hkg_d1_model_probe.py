# -*- coding: utf-8 -*-
"""HKG D1 Model 探针批（2026-09-29）。

S0 白名单：model192（cov 1.0, ac=2）、model53（cov 0.86, ac=3）、model262（cov 0.70, ac=8）
  —— 三者均跨区无死路、拥挤度低、体检包齐。
S1 字段：全部 users=0 冷门（理论 prod≈0），语义归类干净（基本面/PD/预测类，无标识符字段）。
探针：7 条独立仿真（QUICK 模式降本，无 checks 不可提交——探针只看 |S| 形状），形状 5 族：
  group_rank+ts_zscore / ts_rank+ts_delta / rank 平滑 / 乘法交互 / 负向 PD。
设置：HKG TOP800 D1 SECTOR decay4 trunc0.08（tracking/HKG/config/settings.json）。
"""
import asyncio
import json
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
OUT = r"D:\coding\traeCN_project\wqb\logs\_hkg_d1_model_probe.json"

BASE = {"instrumentType": "EQUITY", "region": "HKG", "universe": "TOP800", "delay": 1,
        "decay": 4, "neutralization": "SECTOR", "truncation": 0.08, "maxTrade": "ON",
        "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
        "language": "FASTEXPR", "visualization": False, "simulationMode": "QUICK"}

PROBES = [
    ("model192", "mdl192_id_pu",
     "group_rank(ts_zscore(ts_backfill(mdl192_id_pu, 66), 66), industry)"),
    ("model192", "mdl192_ohlsonscore_di",
     "multiply(-1, rank(ts_mean(ts_backfill(mdl192_ohlsonscore_di, 66), 22)))"),
    ("model192", "mdl192_opincltd_di",
     "ts_rank(ts_delta(ts_backfill(mdl192_opincltd_di, 66), 22), 66)"),
    ("model53", "mdl53_jc6_1month",
     "multiply(-1, group_rank(ts_mean(ts_backfill(mdl53_jc6_1month, 66), 22), industry))"),
    ("model53", "annualized_pd_3_month_jc7",
     "ts_rank(multiply(-1, ts_delta(ts_backfill(annualized_pd_3_month_jc7, 66), 22)), 66)"),
    ("model262", "mdl262_predictiveni_ttm_predict",
     "group_rank(ts_zscore(ts_backfill(mdl262_predictiveni_ttm_predict, 66), 66), industry)"),
    ("model262", "mdl262_predictiveebit_a_predict",
     "ts_rank(ts_delta(ts_backfill(mdl262_predictiveebit_a_predict, 66), 22), 66)"),
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
    done = {p.get("sim_id") for p in state["probes"] if p.get("sim_id")}

    # 1) 提交缺失探针
    payloads = []
    for ds, field, expr in PROBES:
        if any(p.get("expr") == expr for p in state["probes"]):
            continue
        settings = dict(BASE)
        payloads.append({"type": "REGULAR", "settings": settings, "regular": expr})
        state["probes"].append({"dataset": ds, "field": field, "expr": expr})
    if payloads:
        batch = await brain.batch_create_simulations(payloads)
        new = [p for p in state["probes"] if not p.get("sim_id")]
        for p, r in zip(new, batch["results"]):
            p["sim_id"] = r.get("simulation_id")
            p["submitted"] = r.get("ok")
            if not r.get("ok"):
                p["error"] = r.get("error") or f"HTTP {r.get('status_code')}"
        save_state(state)
        print(f"[submit] {batch['submitted']}/{batch['total']} 探针已提交")

    # 2) 轮询终态（QUICK 出结果快）
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
        print(f"[sim] {p['dataset']}/{p['field'][:30]} -> {p.get('alpha_id') or p.get('error') or 'TIMEOUT'}")
        save_state(state)

    # 3) 收割指标
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

    print("\n=== 探针汇总 ===")
    for p in state["probes"]:
        m = p.get("metrics") or {}
        print(f"  {p['dataset']:<10} {p['field'][:35]:<35} alpha={p.get('alpha_id')} "
              f"S={m.get('sharpe')} F={m.get('fitness')} tvr={m.get('turnover')}")


asyncio.run(main())