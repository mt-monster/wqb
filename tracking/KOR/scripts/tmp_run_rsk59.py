# -*- coding: utf-8 -*-
"""RISK59 波 —— risk59（risk 塔未点亮 ×1.3，16 字段全 VECTOR，cov 0.9806）。
★ 关键修正：字段是 VECTOR 类型，必须 vec_* 聚合，不能直接 ts_backfill（AL3 波全 ERROR 的根因）。
冷门字段优先（u≤16）：last_rate/short_momentum/shortinterestpct/offer_rate/crowded_score。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

PROBES = [
  # --- 冷门核心（u≤16）：借券费率 vs 融资费率（做空成本）---
  ("rk_p1_lastrate",   "增量借券费率 last_rate（9u 极冷门）", "group_rank(vec_avg(rsk59_last_rate), market)"),
  ("rk_p2_offerrrate", "存量融资费率 offer_rate（13u）",      "group_rank(vec_avg(rsk59_offer_rate), market)"),
  ("rk_p3_ratespread", "借券/融资费率价差（offer-last）",     "group_rank(subtract(vec_avg(rsk59_offer_rate), vec_avg(rsk59_last_rate)), market)"),
  # --- 卖空动量（冷门 9u，帖2「稳不稳」精神）---
  ("rk_p4_shortmom",   "卖空动量 short_momentum（9u 极冷门）","group_rank(vec_avg(rsk59_short_momentum), market)"),
  ("rk_p5_shortpct",   "卖空占流通股比 shortinterestpct（13u）","group_rank(vec_avg(rsk59_shortinterestpct), market)"),
  # --- 拥挤度/挤压（冷门，反向机制）---
  ("rk_p6_crowded",    "空头拥挤度 crowded_score（16u）",     "group_rank(vec_avg(rsk59_crowded_score), market)"),
  ("rk_p7_squeeze",    "挤压风险 squeeze_risk（30u）",        "group_rank(vec_avg(rsk59_squeeze_risk), market)"),
  # --- 回补压力（DTC 族，机制不同）---
  ("rk_p8_dtc10",      "10日回补天数 daystocover10day",       "group_rank(vec_avg(rsk59_daystocover10day), market)"),
  ("rk_p9_dtc90",      "90日回补天数 daystocover90day",       "group_rank(vec_avg(rsk59_daystocover90day), market)"),
  # --- 可借供给（借券容量，41u）---
  ("rk_p10_avail",     "可借数量 indicativeavailability",     "group_rank(vec_avg(rsk59_indicativeavailability), market)"),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
         "settings": {"region":"KOR","universe":"TOP600","delay":1,"decay":4,
                      "neutralization":"STATISTICAL","truncation":0.08,"nan_handling":"ON"},
         "probes": [{"id":e[0],"mechanism":e[1],"expr":e[2]} for e in PROBES], "batches": []}
    r = await create_multi_simulation([e[2] for e in PROBES], region="KOR", universe="TOP600", delay=1,
            decay=4, neutralization="STATISTICAL", truncation=0.08,
            nan_handling="ON", pasteurization="ON", test_period="P0Y0M")
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("PID:", pid)
    out["batches"].append({"n":len(PROBES),"progress_id":pid,"ids":[e[0] for e in PROBES]})
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RSK59_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
