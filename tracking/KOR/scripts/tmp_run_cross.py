# -*- coding: utf-8 -*-
"""CROSS 波 —— 跨数据源比值（rsk59 借券/融资结构 vs shrt38 成交），降 prod 的独立几何。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
GROUPS = [
  ("X1_stat_d4", "STATISTICAL", 4, [
     ("x1_offer_last",  "group_rank(divide(vec_avg(rsk59_offer_rate), add(vec_avg(rsk59_last_rate), 0.0001)), market)"),
     ("x2_si_avail",    "group_rank(divide(vec_avg(rsk59_short_interest), add(vec_avg(rsk59_indicativeavailability), 0.0001)), market)"),
     ("x3_dtc_ratio",   "group_rank(divide(vec_avg(rsk59_daystocover10day), add(vec_avg(rsk59_daystocover90day), 0.0001)), market)"),
  ]),
  ("X2_stat_d4b", "STATISTICAL", 4, [
     ("x4_sh38_ratio",  "group_rank(divide(vec_avg(shrt38_tot_amt_wgt), add(vec_avg(shrt38_ytq), 0.0001)), market)"),
     ("x5_sq_crowd",    "group_rank(divide(vec_avg(rsk59_squeeze_risk), add(vec_avg(rsk59_crowded_score), 1)), market)"),
     ("x6_s3util",      "group_rank(vec_avg(rsk59_s3utilization), market)"),
  ]),
  ("X3_stat_d4c", "STATISTICAL", 4, [
     ("x7_si_per_avail", "group_rank(divide(vec_avg(rsk59_shortinterestnotional), add(vec_avg(rsk59_indicativeavailability), 0.0001)), market)"),
     ("x8_dtc10_rk126",  "group_rank(ts_rank(vec_avg(rsk59_daystocover10day), 126), market)"),
  ]),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, items in GROUPS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=0.08, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_CROSS_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
