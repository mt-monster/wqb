# -*- coding: utf-8 -*-
"""SI3-UTIL 深化波 —— 围绕「借券利用率动量」机制（6XjWq9wJ S0.62/2Y1.54 为最强腿）。
合规：单信号结构化（ts_delta/ts_mean/group 轴/nu 变化），无 add 双腿混合。
每项单独指定 settings（nu 是决定性杠杆）。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

# (id, mechanism, expr, nu)
VARIANTS = [
  # --- 基线复现 + nu 杠杆（决定 2Y）---
  ("u1_delta5_stat",   "利用率5日变化 基线 STATISTICAL", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), market)", "STATISTICAL"),
  ("u2_delta5_ind",    "利用率5日变化 INDUSTRY（nu 提 2Y）", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), market)", "INDUSTRY"),
  ("u3_delta5_subind", "利用率5日变化 SUBINDUSTRY", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), market)", "SUBINDUSTRY"),
  # --- 变化窗口扫描 ---
  ("u4_delta10",       "利用率10日变化", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 10), market)", "INDUSTRY"),
  ("u5_delta22",       "利用率22日变化", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 22), market)", "INDUSTRY"),
  ("u6_delta3",        "利用率3日变化", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 3), market)", "INDUSTRY"),
  # --- 归一化变化（相对水平，去量纲）---
  ("u7_relchg22",      "利用率相对22日均值的变化率", "group_rank(divide(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), add(ts_mean(vec_avg(loan_utilization_ratio_twn), 22), 0.0001)), market)", "INDUSTRY"),
  # --- 分组轴变化（破 CW，KOR 小宇宙）---
  ("u8_delta5_sector", "利用率5日变化 sector 轴", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), sector)", "INDUSTRY"),
  ("u9_delta5_subind_axis", "利用率5日变化 subindustry 轴", "group_rank(ts_delta(vec_avg(loan_utilization_ratio_twn), 5), subindustry)", "INDUSTRY"),
  # --- units 版利用率（另一字段同名机制，验稳健）---
  ("u10_units_delta5", "units版利用率5日变化", "group_rank(ts_delta(vec_avg(shrt3_utilizationpercent_units), 5), market)", "INDUSTRY"),
]

async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    await brain_client.ensure_authenticated()
    out={"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "variants": [
        {"id":v[0],"mechanism":v[1],"expr":v[2],"nu":v[3]} for v in VARIANTS], "batches": []}
    # 按 nu 分组提交（nu 在 settings 层，不同 nu 必须分批）
    from itertools import groupby
    for nu, grp in groupby(VARIANTS, key=lambda v: v[3]):
        grp=list(grp)
        r = await create_multi_simulation([v[2] for v in grp], region="KOR", universe="TOP600", delay=1,
                decay=4, neutralization=nu, truncation=0.08, nan_handling="ON", test_period="P0Y0M")
        pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
        print(f"nu={nu} pid={pid} n={len(grp)} ids={[v[0] for v in grp]}")
        out["batches"].append({"nu":nu,"progress_id":pid,"ids":[v[0] for v in grp]})
        await asyncio.sleep(1)
    with open(os.path.join(REPO,"tracking/KOR/candidates/wave_SI3U_submitted.json"),"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=1)
asyncio.run(main())
