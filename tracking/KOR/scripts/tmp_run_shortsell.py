# -*- coding: utf-8 -*-
"""SHORTSELL —— 纯卖空水平/权重字段（ytq/tgw/amt_wgt）+ 借券比值，找低 prod 新腿。
配方沿用 subindustry 轴 + SUBINDUSTRY nu + decay4（已验证最优）。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
SPECS = [
  ("S1_shortlevel", "SUBINDUSTRY", 4, 0.08, [
     ("sv1_ytq",      "group_rank(vec_avg(shrt38_ytq), subindustry)"),
     ("sv2_amt",      "group_rank(vec_avg(shrt38_amt), subindustry)"),
  ]),
  ("S2_shortwgt", "SUBINDUSTRY", 4, 0.08, [
     ("sv3_amt_wgt",  "group_rank(vec_avg(shrt38_amt_wgt), subindustry)"),
     ("sv4_tot_amt_wgt", "group_rank(vec_avg(shrt38_tot_amt_wgt), subindustry)"),
  ]),
  ("S3_ratio_mix", "SUBINDUSTRY", 4, 0.08, [
     ("sv5_ytq_per_amt", "group_rank(divide(vec_avg(shrt38_ytq), add(vec_avg(shrt38_amt), 0.0001)), subindustry)"),
     ("sv6_tgw_ytq",     "group_rank(vec_avg(shrt38_tgw_ytq), subindustry)"),
  ]),
  ("S4_invact_vs_ss", "SUBINDUSTRY", 4, 0.08, [
     ("sv7_sell_ss",   "group_rank(divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_short_sellshort_sell_amt), 0.0001)), subindustry)"),
     ("sv8_buy_ss",    "group_rank(divide(vec_avg(shrt38_stk_invactbuy_amt), add(vec_avg(shrt38_stk_short_sellshort_sell_amt), 0.0001)), subindustry)"),
  ]),
]
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "batches": []}
    for gname, nu, dec, trunc, items in SPECS:
        r = await create_multi_simulation([it[1] for it in items], region="KOR", universe="TOP600", delay=1,
                decay=dec, neutralization=nu, truncation=trunc, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"{gname} pid={pid} n={len(items)}")
        out["batches"].append({"group":gname,"nu":nu,"decay":dec,"trunc":trunc,"progress_id":pid,"ids":[it[0] for it in items]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SHORTSELL_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
