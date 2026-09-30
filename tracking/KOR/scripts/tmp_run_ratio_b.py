# -*- coding: utf-8 -*-
"""SI38-RATIO 强化波 —— 攻 YPbV2Zxw（sell/buy 比值 S2.54/SUB2.26 全过，仅 2Y 1.18<1.58）。
机制：卖出额/买入额比值（论坛帖3「单字段无信号→比值有信号」核心）。
目标：2Y ≥1.58。手段：nu 杠杆 + 长窗平滑 + 分组轴 + 秩变换。合规：单信号。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
BASE = "divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
VARIANTS = [
  ("r1_base_stat",   "比值基线 STATISTICAL",              f"group_rank({BASE}, market)", "STATISTICAL"),
  ("r2_base_ind",    "比值 INDUSTRY",                     f"group_rank({BASE}, market)", "INDUSTRY"),
  ("r3_base_subind", "比值 SUBINDUSTRY",                  f"group_rank({BASE}, market)", "SUBINDUSTRY"),
  ("r4_ma5_ind",     "比值 vec 层 5 日平滑 IND",          f"group_rank(divide(ts_mean(vec_avg(shrt38_stk_invactsell_amt),5), add(ts_mean(vec_avg(shrt38_stk_invactbuy_amt),5), 0.0001)), market)", "INDUSTRY"),
  ("r5_ma22_ind",    "比值 22 日平滑 IND",                f"group_rank(divide(ts_mean(vec_avg(shrt38_stk_invactsell_amt),22), add(ts_mean(vec_avg(shrt38_stk_invactbuy_amt),22), 0.0001)), market)", "INDUSTRY"),
  ("r6_rk252_sub",   "比值 ts_rank252 SUBIND",            f"group_rank(ts_rank({BASE}, 252), market)", "SUBINDUSTRY"),
  ("r7_rk504_ind",   "比值 ts_rank504 IND",               f"group_rank(ts_rank({BASE}, 504), market)", "INDUSTRY"),
  ("r8_sectaxis_ind","比值 sector 轴 IND",                f"group_rank({BASE}, sector)", "INDUSTRY"),
  ("r9_subaxis_sub", "比值 subindustry 轴 SUBIND",        f"group_rank({BASE}, subindustry)", "SUBINDUSTRY"),
  ("r10_decay10_ind","比值 长decay IND（按需改 decay）",  f"group_rank({BASE}, market)", "INDUSTRY"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RATIO_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
