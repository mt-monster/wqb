# -*- coding: utf-8 -*-
"""RATIO-C 精调波 —— 解耦「2Y↑ vs prod↑」矛盾。
基线 YPbV2Zxw：S2.54 2Y1.18 prod0.7116（裸比值，prod 最低）
对比 gJblmzJl：ts_rank504 使 2Y→1.70 但 prod→0.8414（平滑推高 prod）
策略：中等窗 ts_rank(63/126/252) + decay 阶梯，找「小步提 2Y、不过 prod」的甜点。
合规：单信号。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
BASE = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
# (id, mechanism, expr, nu, decay)
VARIANTS = [
  ("c1_rk63_stat",   "比值 ts_rank63 STAT",  f"group_rank(ts_rank({BASE}, 63), market)", "STATISTICAL", 4),
  ("c2_rk126_stat",  "比值 ts_rank126 STAT", f"group_rank(ts_rank({BASE}, 126), market)", "STATISTICAL", 4),
  ("c3_rk252_stat",  "比值 ts_rank252 STAT", f"group_rank(ts_rank({BASE}, 252), market)", "STATISTICAL", 4),
  ("c4_rk63_ind",    "比值 ts_rank63 IND",   f"group_rank(ts_rank({BASE}, 63), market)", "INDUSTRY", 4),
  ("c5_rk126_ind",   "比值 ts_rank126 IND",  f"group_rank(ts_rank({BASE}, 126), market)", "INDUSTRY", 4),
  ("c6_rk252_ind",   "比值 ts_rank252 IND",  f"group_rank(ts_rank({BASE}, 252), market)", "INDUSTRY", 4),
  ("c7_base_decay10","裸比值 decay10 STAT",  f"group_rank({BASE}, market)", "STATISTICAL", 10),
  ("c8_base_decay20","裸比值 decay20 STAT",  f"group_rank({BASE}, market)", "STATISTICAL", 20),
  ("c9_rk126_d10",   "比值 ts_rank126 IND d10", f"group_rank(ts_rank({BASE}, 126), market)", "INDUSTRY", 10),
  ("c10_rk252_d10",  "比值 ts_rank252 IND d10", f"group_rank(ts_rank({BASE}, 252), market)", "INDUSTRY", 10),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
         "variants":[{"id":v[0],"mechanism":v[1],"expr":v[2],"nu":v[3],"decay":v[4]} for v in VARIANTS], "batches": []}
    for v in VARIANTS:
        r = await create_multi_simulation([v[2]], region="KOR", universe="TOP600", delay=1,
                decay=v[4], neutralization=v[3], truncation=0.08, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{v[0]} pid={pid}")
        out["batches"].append({"id":v[0],"nu":v[3],"decay":v[4],"progress_id":pid})
        await asyncio.sleep(0.6)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RATIOC_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
