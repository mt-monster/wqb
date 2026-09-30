# -*- coding: utf-8 -*-
"""SI3 探测波 —— KOR shortinterest3（证券借贷/借券机制，从未挖过）。分 2 批（每批 ≤10）。"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

PROBES = [
  ("si3_p1_util",        "借券利用率水平（借出/可借，高=拥挤）", "group_rank(vec_avg(loan_utilization_ratio_twn), market)"),
  ("si3_p2_util_units",  "借券利用率（units 版）",              "group_rank(vec_avg(shrt3_utilizationpercent_units), market)"),
  ("si3_p3_util_delta",  "利用率 5 日变化（拥挤度加速）",        "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), market)"),
  ("si3_p4_util_rank",   "利用率长窗强度 ts_rank252",            "group_rank(ts_rank(vec_avg(loan_utilization_ratio_twn), 252), market)"),
  ("si3_p5_rate",        "加权平均借券费率水平",                 "group_rank(vec_avg(mean_loan_rate), market)"),
  ("si3_p6_rate_vol",    "借券费率波动率（不稳定性）",           "group_rank(vec_avg(loan_rate_volatility), market)"),
  ("si3_p7_rate_spread", "费率极差（max-min，借券难度分化）",    "group_rank(subtract(vec_avg(max_loan_rate), vec_avg(min_loan_rate)), market)"),
  ("si3_p8_rate_mom",    "费率 22 日动量",                       "group_rank(ts_delta(vec_avg(mean_loan_rate), 22), market)"),
  ("si3_p9_borrow",      "借券需求评分（1-10）",                 "group_rank(vec_avg(borrow_activity_score), market)"),
  ("si3_p10_bar",        "借券需求 bar（1-10）",                  "group_rank(vec_avg(shrt3_bar), market)"),
  ("si3_p11_duration",   "平均借券期限（天）",                   "group_rank(vec_avg(average_loan_duration_days), market)"),
  ("si3_p12_newloan",    "新增借出股数（新借券活动）",           "group_rank(vec_avg(new_loaned_share_count), market)"),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
         "settings": {"region":"KOR","universe":"TOP600","delay":1,"decay":4,
                      "neutralization":"STATISTICAL","truncation":0.08,"nan_handling":"ON"},
         "probes": [{"id":e[0],"mechanism":e[1],"expr":e[2]} for e in PROBES],
         "batches": []}
    for bi in range(0, len(PROBES), 10):
        chunk = PROBES[bi:bi+10]
        r = await create_multi_simulation([e[2] for e in chunk], region="KOR", universe="TOP600", delay=1,
                decay=4, neutralization="STATISTICAL", truncation=0.08,
                nan_handling="ON", pasteurization="ON", test_period="P0Y0M")
        loc = r.get("location") or r.get("Location")
        pid = (loc or "").rstrip("/").split("/")[-1]
        print(f"BATCH{bi//10+1}: pid={pid} n={len(chunk)} ids={[e[0] for e in chunk]}")
        out["batches"].append({"n":len(chunk),"progress_url":loc,"progress_id":pid,
                               "ids":[e[0] for e in chunk]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI3_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
