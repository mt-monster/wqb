# -*- coding: utf-8 -*-
"""RATIO-D 解耦波 —— 找「提 2Y 但 prod 涨得少」的旋钮。
已知：decay/ts_rank 平滑同向推高 2Y 与 prod。本波试非线性/轴/其他平滑。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
B="divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
GROUPS = [
  ("D1_stat_d4", "STATISTICAL", 4, [
     ("d1_sp_power",  f"group_rank(signed_power(subtract({B},0.5),0.5), market)"),
     ("d2_zscore252", f"group_rank(ts_zscore({B}, 252), market)"),
     ("d3_rank_only", f"group_rank(rank({B}), market)"),
  ]),
  ("D2_stat_d4b", "STATISTICAL", 4, [
     ("d4_median5",   f"group_rank(ts_median({B}, 5), market)"),
     ("d5_mean3",     f"group_rank(ts_mean({B}, 3), market)"),
     ("d6_decaylin10",f"group_rank(ts_decay_linear({B}, 10), market)"),
  ]),
  ("D3_ind_d4", "INDUSTRY", 4, [
     ("d7_exch_rk126",f"group_rank(ts_rank({B},126), exchange)"),
     ("d8_rk378",     f"group_rank(ts_rank({B}, 378), market)"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_RATIOD_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
