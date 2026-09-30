# -*- coding: utf-8 -*-
"""SI3-MAIN 波 —— 攻 shortinterest3 的 `_main` 冷门族（AMR 实测 users 4-22/alphas 5-27，coverage 0.976 最高）。
策略：避开热门的 shrt3_bar(143u)/utilization(115u)，主攻极冷门高覆盖 _main 后缀字段。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

PROBES = [
  # --- A 组：借券费率 _main（冷门核心）---
  ("si3m_p1_rate_main",   "加权平均借券费率（main，冷门高覆盖）", "group_rank(vec_avg(mean_loan_rate_main), market)"),
  ("si3m_p2_ratemax_main","最高借券费率（main）",                 "group_rank(vec_avg(max_loan_rate_main), market)"),
  ("si3m_p3_ratemin_main","最低借券费率（main）",                 "group_rank(vec_avg(min_loan_rate_main), market)"),
  ("si3m_p4_ratevol_main","借券费率波动率（main，不稳定性）",     "group_rank(vec_avg(loan_rate_volatility_main), market)"),
  ("si3m_p5_spread_main", "费率极差（main，借券难度分化）",       "group_rank(subtract(vec_avg(max_loan_rate_main), vec_avg(min_loan_rate_main)), market)"),
  # --- B 组：借券规模/期限 _main ---
  ("si3m_p6_dur_main",    "平均借券期限（main，极冷门 4u）",      "group_rank(vec_avg(average_loan_duration_days_main), market)"),
  ("si3m_p7_val_main",    "借出市值 USD（main）",                 "group_rank(vec_avg(loaned_market_value_usd_main), market)"),
  ("si3m_p8_cnt_main",    "借出股数（main）",                     "group_rank(vec_avg(loaned_share_count_main), market)"),
  ("si3m_p9_txn_main",    "借券交易笔数（main，活跃度）",         "group_rank(vec_avg(transaction_count_main), market)"),
  # --- C 组：可借供给侧（冷门，借贷容量）---
  ("si3m_p10_avail_usd",  "可借市值 USD（1u 极冷门，供给容量）",  "group_rank(vec_avg(available_market_value_usd), market)"),
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
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    print("PID:", pid)
    out["batches"].append({"n":len(PROBES),"progress_id":pid,
                           "progress_url":f"https://api.worldquantbrain.com/simulations/{pid}",
                           "ids":[e[0] for e in PROBES]})
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI3M_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
