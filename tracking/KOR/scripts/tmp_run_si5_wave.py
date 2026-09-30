# -*- coding: utf-8 -*-
"""SI5 + 未挖维度波 —— shortinterest5（涨跌停机制，35 users 极冷门）+ shrt38 频率/单位比。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

PROBES = [
  # --- A 组：shortinterest5 涨跌停制度（极冷门，3 字段）---
  ("si5_p1_dec_ratio",   "跌停比率（跌停幅度大=波动制度特征）", "group_rank(vec_avg(max_price_decrease_ratio), market)"),
  ("si5_p2_dec_inv",     "跌停比率反向",                        "group_rank(multiply(-1, vec_avg(max_price_decrease_ratio)), market)"),
  ("si5_p3_dec_share",   "跌停/(跌停+涨停) 不对称度",           "group_rank(divide(vec_avg(max_price_decrease_ratio), add(vec_avg(max_price_decrease_ratio), vec_avg(max_price_increase_ratio))), market)"),
  ("si5_p4_plc",         "交易制度状态码（正常/受限）",          "group_rank(vec_avg(price_limit_condition), market)"),
  ("si5_p5_dec_mean22",  "跌停比率 22 日均值",                  "group_rank(ts_mean(vec_avg(max_price_decrease_ratio), 22), market)"),
  # --- B 组：shrt38 未挖维度（单位卖空金额比值，帖3 精神）---
  ("sh_s1_unit_amt",     "单位卖空金额（成交额权重/数量权重）",   "group_rank(divide(vec_avg(shrt38_tot_amt_wgt), add(vec_avg(shrt38_tot_qty_wgt), 0.0001)), market)"),
  ("sh_s2_amt_per_qty",  "每单位卖空量金额（amt/qty）",           "group_rank(divide(vec_avg(shrt38_amt), add(vec_avg(shrt38_ytq), 0.0001)), market)"),
  ("sh_s3_qrf_freq",     "聚合频率码（日/周/月）",                "group_rank(vec_avg(shrt38_pyt_qrf), market)"),
  ("sh_s4_invact_prd",   "投资者聚合窗口类型（5d/20d/月）",       "group_rank(vec_avg(shrt38_stk_agg_invactcalc_prd_typ), market)"),
  ("sh_s5_short_prd",    "卖空聚合窗口类型",                     "group_rank(vec_avg(shrt38_stk_agg_short_sellcalc_prd_typ), market)"),
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
            decay=4, neutralization="STATISTICAL", truncation=0.08,
            nan_handling="ON", pasteurization="ON", test_period="P0Y0M")
    loc = r.get("location") or r.get("Location")
    print("SUBMIT:", json.dumps(r, ensure_ascii=False)[:300], "loc=", loc)
    out["batches"].append({"n":len(PROBES),"progress_url":loc,
                           "progress_id":(loc or "").rstrip("/").split("/")[-1],
                           "ids":[e[0] for e in PROBES]})
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI5_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
