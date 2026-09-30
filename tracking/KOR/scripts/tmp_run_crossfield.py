# -*- coding: utf-8 -*-
"""CROSSFIELD —— 用已验证的「比值 + subindustry 轴 + SUBINDUSTRY nu + decay4」配方，
换到 shortinterest38 的未探字段（做空卖出/累计买卖/短售），找 prod 更低的正交腿。
合规：单信号（比值）。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
SPECS = [
  ("P1_short_sell_ratio", "SUBINDUSTRY", 4, 0.08, [
     ("p1_ssell_amt", "group_rank(divide(vec_avg(shrt38_stk_short_sellshort_sell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001)), subindustry)"),
     ("p2_ssell_qty", "group_rank(divide(vec_avg(shrt38_stk_short_sellshort_sell_qty), add(vec_avg(shrt38_stk_invactbuy_qty), 0.0001)), subindustry)"),
  ]),
  ("P2_accum_ratio", "SUBINDUSTRY", 4, 0.08, [
     ("p3_accum_sb",  "group_rank(divide(vec_avg(shrt38_accum_sell_amt), add(vec_avg(shrt38_accum_buy_amt), 0.0001)), subindustry)"),
     ("p4_accum_sbq", "group_rank(divide(vec_avg(shrt38_accum_sell_qty), add(vec_avg(shrt38_accum_buy_qty), 0.0001)), subindustry)"),
  ]),
  ("P3_netqty_ratio", "SUBINDUSTRY", 4, 0.08, [
     ("p5_net_qty",   "group_rank(divide(vec_avg(shrt38_stk_invactnet_buy_qty), add(vec_avg(shrt38_tot_qty_wgt), 0.0001)), subindustry)"),
     ("p6_ssell_wgt", "group_rank(divide(vec_avg(shrt38_stk_short_sellshort_sell_amt_wgt), add(vec_avg(shrt38_tot_amt_wgt), 0.0001)), subindustry)"),
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
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_CROSSFIELD_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
