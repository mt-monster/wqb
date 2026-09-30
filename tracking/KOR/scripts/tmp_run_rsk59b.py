# -*- coding: utf-8 -*-
"""RISK59-SIGN 波 —— 费率类取反（借券成本高→负面，论坛帖2精神）+ 强化变换。
RISK59 首波实证：last_rate -0.77 / offer_rate -0.62（负=取反有效）→ 本波攻反向。
合规：单信号（multiply(-1,X) 是符号变换，非双腿相加）。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
VARIANTS = [
  # --- A 组：费率取反（成本高→负面）---
  ("s1_lastrate_inv",  "增量借券费率取反", "group_rank(multiply(-1, vec_avg(rsk59_last_rate)), market)", "STATISTICAL"),
  ("s2_offerrrate_inv","存量融资费率取反", "group_rank(multiply(-1, vec_avg(rsk59_offer_rate)), market)", "STATISTICAL"),
  ("s3_rateavg_inv",   "两费率均值取反", "group_rank(multiply(-1, divide(add(vec_avg(rsk59_offer_rate), vec_avg(rsk59_last_rate)), 2)), market)", "STATISTICAL"),
  ("s4_lastrate_ind",  "增量借券费率取反 INDUSTRY", "group_rank(multiply(-1, vec_avg(rsk59_last_rate)), market)", "INDUSTRY"),
  ("s5_lastrate_sub",  "增量借券费率取反 SUBINDUSTRY", "group_rank(multiply(-1, vec_avg(rsk59_last_rate)), market)", "SUBINDUSTRY"),
  # --- B 组：费率取反长窗平滑（压 turnover 提 2Y）---
  ("s6_lastrate_ma22","费率取反 22 日平滑", "group_rank(multiply(-1, ts_mean(vec_avg(rsk59_last_rate), 22)), market)", "INDUSTRY"),
  ("s7_lastrate_rk252","费率取反 ts_rank252", "group_rank(multiply(-1, ts_rank(vec_avg(rsk59_last_rate), 252)), market)", "INDUSTRY"),
  # --- C 组：可借供给（首波 S0.67 正向）强化 ---
  ("s8_avail_ind",     "可借供给量 INDUSTRY", "group_rank(vec_avg(rsk59_indicativeavailability), market)", "INDUSTRY"),
  ("s9_avail_rk252",   "可借供给量 ts_rank252", "group_rank(ts_rank(vec_avg(rsk59_indicativeavailability), 252), market)", "INDUSTRY"),
  # --- D 组：DTC（2Y 1.04 最好）分组轴 ---
  ("s10_dtc10_ind",    "10日回补天数 INDUSTRY", "group_rank(vec_avg(rsk59_daystocover10day), market)", "INDUSTRY"),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
         "variants":[{"id":v[0],"mechanism":v[1],"expr":v[2],"nu":v[3]} for v in VARIANTS], "batches": []}
    from itertools import groupby
    for nu, grp in groupby(VARIANTS, key=lambda v: v[3]):
        grp=list(grp)
        r = await create_multi_simulation([v[2] for v in grp], region="KOR", universe="TOP600", delay=1,
                decay=4, neutralization=nu, truncation=0.08, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"nu={nu} pid={pid} n={len(grp)} ids={[v[0] for v in grp]}")
        out["batches"].append({"nu":nu,"progress_id":pid,"ids":[v[0] for v in grp]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RSK59B_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
