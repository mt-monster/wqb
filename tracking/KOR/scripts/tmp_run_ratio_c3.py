# -*- coding: utf-8 -*-
"""RATIO-C 重发（≥2 条/批，同 nu+decay 配对）。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
BASE = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
# 按 (nu,decay) 分组，每组 ≥2
GROUPS = [
  ("G1_stat_d4", "STATISTICAL", 4, [
     ("c1_rk63_stat",  f"group_rank(ts_rank({BASE}, 63), market)"),
     ("c2_rk126_stat", f"group_rank(ts_rank({BASE}, 126), market)"),
     ("c3_rk252_stat", f"group_rank(ts_rank({BASE}, 252), market)"),
  ]),
  ("G2_stat_d10", "STATISTICAL", 10, [
     ("c7_base_d10", f"group_rank({BASE}, market)"),
     ("c9_rk126_d10", f"group_rank(ts_rank({BASE}, 126), market)"),
  ]),
  ("G3_stat_d20", "STATISTICAL", 20, [
     ("c8_base_d20", f"group_rank({BASE}, market)"),
     ("c10_rk252_d20", f"group_rank(ts_rank({BASE}, 252), market)"),
  ]),
  ("G4_sub_d4", "SUBINDUSTRY", 4, [
     ("c12_rk126_sub", f"group_rank(ts_rank({BASE}, 126), market)"),
     ("c13_rk63_sub",  f"group_rank(ts_rank({BASE}, 63), market)"),
     ("c6_rk252_sub",  f"group_rank(ts_rank({BASE}, 252), market)"),
  ]),
  ("G5_ind_d4", "INDUSTRY", 4, [
     ("c5_rk126_ind", f"group_rank(ts_rank({BASE}, 126), market)"),
     ("c4_rk63_ind",  f"group_rank(ts_rank({BASE}, 63), market)"),
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
        ok = "success" in str(r).lower() or pid
        print(f"{gname} pid={pid} ok={ok} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"progress_id":pid,
                               "ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RATIOC_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
