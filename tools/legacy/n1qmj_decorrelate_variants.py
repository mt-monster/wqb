# -*- coding: utf-8 -*-
"""N1QMJ10q 去相关改造变体批（2026-09-14）。

原版：USA TOP3000 D1 STATISTICAL trunc=0.08，prod_corr=0.7225（超线 0.022），
self_corr=0.397 健康。目标：prod_corr <= 0.7 且硬闸（sharpe/fitness/2Y/margin）不掉。

变体矩阵（表达式不变）：
  V1 SUBINDUSTRY / V2 INDUSTRY / V3 SECTOR / V4 MARKET（换中性化）
  V5 universe=TOP2000（换 universe，保留 STATISTICAL）
  V6 truncation=0.05（收紧 truncate）
流程：批量提交 → 轮询至终态 → 提取 IS 指标与 checks → 对过硬闸者串行重测 prod_corr。
checkpoint: logs/_n1qmj_variants.json，可断点续跑。
"""
import asyncio
import json
import sys
from datetime import datetime

sys.path.insert(0, r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
OUT = r"D:\coding\traeCN_project\wqb\logs\_n1qmj_variants.json"

EXPR = ("group_rank(ts_zscore(ts_backfill(subtract(positive_sentiment_probability_3, "
        "negative_sentiment_probability_3), 252), 252), industry)")
BASE = {"instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000", "delay": 1,
        "decay": 0, "neutralization": "STATISTICAL", "truncation": 0.08,
        "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
        "language": "FASTEXPR", "visualization": False}

VARIANTS = {
    "V1_subindustry": {"neutralization": "SUBINDUSTRY"},
    "V2_industry":    {"neutralization": "INDUSTRY"},
    "V3_sector":      {"neutralization": "SECTOR"},
    "V4_market":      {"neutralization": "MARKET"},
    "V5_top2000":     {"universe": "TOP2000"},
    "V6_trunc05":     {"truncation": 0.05},
}


def load_state():
    try:
        return json.load(open(OUT, encoding="utf-8"))
    except Exception:
        return {"variants": {}}


def save_state(st):
    json.dump(st, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


async def poll_terminal(brain, sim_id, max_wait=1500):
    waited = 0
    while waited < max_wait:
        r = await brain._request('GET', f"{brain.base_url}/simulations/{sim_id}")
        d = brain._response_payload(r)
        status = (d or {}).get("status")
        if status in ("COMPLETE", "ERROR", "FAIL"):
            return d
        await asyncio.sleep(20)
        waited += 20
        if waited % 120 == 0:
            print(f"    ...等待仿真 {sim_id[:8]} {waited}s (status={status})")
    return {"status": "TIMEOUT"}


async def main():
    from brain_api import brain_client
    brain = brain_client
    await brain.ensure_authenticated()
    state = load_state()

    # 1) 提交缺失的变体
    to_submit = {k: v for k, v in VARIANTS.items()
                 if k not in state["variants"] or "sim_id" not in state["variants"][k]}
    if to_submit:
        payloads = []
        names = []
        for name, over in to_submit.items():
            settings = dict(BASE); settings.update(over)
            payloads.append({"type": "REGULAR", "settings": settings, "regular": EXPR})
            names.append(name)
            state["variants"].setdefault(name, {})
        batch = await brain.batch_create_simulations(payloads)
        for name, r in zip(names, batch["results"]):
            state["variants"][name]["sim_id"] = r.get("simulation_id")
            state["variants"][name]["submitted"] = r.get("ok")
            if not r.get("ok"):
                state["variants"][name]["error"] = r.get("error") or f"HTTP {r.get('status_code')}"
        save_state(state)
        print(f"[submit] {batch['submitted']}/{batch['total']} 已提交")

    # 2) 轮询至终态
    for name, rec in state["variants"].items():
        if rec.get("alpha_id") or rec.get("submitted") is False:
            continue
        sim_id = rec.get("sim_id")
        if not sim_id:
            continue
        print(f"[poll] {name} sim={sim_id[:8]}")
        d = await poll_terminal(brain, sim_id)
        rec["sim_status"] = d.get("status")
        rec["alpha_id"] = d.get("alpha")
        if d.get("message"):
            rec["sim_message"] = str(d.get("message"))[:200]
        save_state(state)
        print(f"  -> {d.get('status')} alpha={d.get('alpha')}")

    # 3) 提取指标并重测 prod_corr
    for name, rec in state["variants"].items():
        aid = rec.get("alpha_id")
        if not aid or rec.get("prod_corr"):
            continue
        d = await brain.get_alpha_details(aid)
        iss = d.get("is") or {}
        checks = {c.get("name"): c for c in (iss.get("checks") or [])}
        y2 = (checks.get("LOW_2Y_SHARPE") or {}).get("value")
        rec["metrics"] = {"sharpe": iss.get("sharpe"), "fitness": iss.get("fitness"),
                          "turnover": iss.get("turnover"), "margin": iss.get("margin"),
                          "two_year_sharpe": y2}
        gates = ((iss.get("sharpe") or 0) >= 1.58 and (iss.get("fitness") or 0) >= 1.0
                 and (y2 or 0) >= 1.58)
        rec["hard_gate_pass"] = gates
        save_state(state)
        print(f"[metrics] {name}: {rec['metrics']} gate={gates}")
        if not gates:
            continue
        pc = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
        prod = (pc.get("checks") or {}).get("production") or {}
        rec["prod_corr"] = {"max": prod.get("max_correlation"), "pass": prod.get("passes_check")}
        sc = await brain.check_self_correlation(aid, threshold=0.7)
        rec["self_corr"] = {"max": sc.get("max_correlation"), "pass": sc.get("passes_check")}
        save_state(state)
        print(f"  prod={rec['prod_corr']} self={rec['self_corr']}")

    print("\n=== 变体汇总 ===")
    for name, rec in state["variants"].items():
        m = rec.get("metrics") or {}
        pc = rec.get("prod_corr") or {}
        print(f"  {name:<16} alpha={rec.get('alpha_id')} sh={m.get('sharpe')} fit={m.get('fitness')} "
              f"2Y={m.get('two_year_sharpe')} gate={rec.get('hard_gate_pass')} "
              f"prod={pc.get('max') and round(pc['max'],4)} pass={pc.get('pass')}")


asyncio.run(main())
