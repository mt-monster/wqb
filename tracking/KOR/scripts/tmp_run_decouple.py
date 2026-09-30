# -*- coding: utf-8 -*-
"""解耦波 DECOUPLE —— 裸比值(prod最低几何) × nu阶梯 × 浅decay。
目标：提 2Y 但 prod 不涨。合规：单信号（比值本身是单一价差信号）。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
BASE = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
GROUPS = [
  ("D1_base_ind_d4", "INDUSTRY", 4, [
     ("d1_base_ind_d4",   f"group_rank({BASE}, market)"),
     ("d2_base_ind_d10",  f"group_rank({BASE}, market)"),
  ]),
  ("D2_base_sub_d4", "SUBINDUSTRY", 4, [
     ("d3_base_sub_d4",   f"group_rank({BASE}, market)"),
     ("d4_base_sub_d10",  f"group_rank({BASE}, market)"),
  ]),
  ("D3_base_sub_d0", "SUBINDUSTRY", 0, [
     ("d5_base_sub_d0",   f"group_rank({BASE}, market)"),
     ("d6_base_ind_d0",   f"group_rank({BASE}, market)"),
  ]),
  ("D4_sm5_sub_d0", "SUBINDUSTRY", 0, [
     ("d7_sm5_sub_d0",    f"group_rank(divide(ts_mean(vec_avg(shrt38_stk_invactsell_amt),5), add(ts_mean(vec_avg(shrt38_stk_invactbuy_amt),5), 0.0001)), market)"),
     ("d8_sm5_ind_d0",    f"group_rank(divide(ts_mean(vec_avg(shrt38_stk_invactsell_amt),5), add(ts_mean(vec_avg(shrt38_stk_invactbuy_amt),5), 0.0001)), market)"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_DECOUPLE_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
