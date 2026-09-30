# -*- coding: utf-8 -*-
"""SI38-AGG 波 —— shrt38 换 vec 聚合算子 + 未试 qty/ratio 结构（验证是否为独立机制）。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
PROBES = [
  ("a1_sum_netbuy",   "净买入额 vec_sum 聚合", "group_rank(vec_sum(shrt38_accum_net_buy_amt), market)"),
  ("a2_max_netbuy",   "净买入额 vec_max 聚合", "group_rank(vec_max(shrt38_accum_net_buy_amt), market)"),
  ("a3_std_netbuy",   "净买入额 vec_stddev（离散度）", "group_rank(vec_stddev(shrt38_accum_net_buy_amt), market)"),
  ("a4_range_netbuy", "净买入额 vec_range（极差）", "group_rank(vec_range(shrt38_accum_net_buy_amt), market)"),
  ("a5_qty_netbuy",   "净买入量（qty 版，未试）", "group_rank(vec_avg(shrt38_stk_invactnet_buy_qty), market)"),
  ("a6_sellbuy_ratio","卖出/买入额比（帖3 比值）", "group_rank(divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001)), market)"),
  ("a7_short_qtywgt", "卖空量权重（未试字段）", "group_rank(vec_avg(shrt38_stk_short_sellshort_sell_qty_wgt), market)"),
  ("a8_amt_level",    "总卖空额水平（未试）", "group_rank(vec_avg(shrt38_amt), market)"),
  ("a9_sum_netqty",   "净买入量 vec_sum", "group_rank(vec_sum(shrt38_accum_net_buy_qty), market)"),
  ("a10_max_netqty",  "净买入量 vec_max", "group_rank(vec_max(shrt38_accum_net_buy_qty), market)"),
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
            decay=4, neutralization="STATISTICAL", truncation=0.08, nan_handling="ON", test_period="P0Y0M")
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("PID:", pid)
    out["batches"].append({"n":len(PROBES),"progress_id":pid,"ids":[e[0] for e in PROBES]})
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI38AGG_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
