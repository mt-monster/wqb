# -*- coding: utf-8 -*-
"""w13: DEU/ShortInterest 单信号探针 (合规版)。

数据集: shortinterest3 (VECTOR 字段, 需 vec_* 聚合)
经济逻辑: 借券需求/成本高 => 空头拥挤 => 反转做多
合规约束: 每行 = 单一信号 + 时序/截面结构化, 禁止 add/加权混合。
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"

E = []  # (label, expr)

# --- 组1: shrt3_bar (借券需求 1-10) 反转 ---
E += [
    ("S1_bar_avg_neg", "rank(multiply(-1, vec_avg(shrt3_bar)))"),
    ("S2_bar_avg_z252", "rank(multiply(-1, ts_zscore(vec_avg(shrt3_bar), 252)))"),
    ("S3_bar_avg_z66", "rank(multiply(-1, ts_zscore(vec_avg(shrt3_bar), 66)))"),
    ("S4_bar_avg_rank252", "rank(multiply(-1, ts_rank(vec_avg(shrt3_bar), 252)))"),
    ("S5_bar_avg_mean5_neg", "rank(multiply(-1, ts_mean(vec_avg(shrt3_bar), 5)))"),
    ("S6_bar_avg_hump", "rank(multiply(-1, hump(vec_avg(shrt3_bar), 0.02)))"),
    ("S7_bar_max_neg", "rank(multiply(-1, vec_max(shrt3_bar)))"),
    ("S8_bar_avg_grp_subind", "group_rank(multiply(-1, vec_avg(shrt3_bar)), subindustry)"),
    ("S9_bar_avg_grp_market", "group_rank(multiply(-1, vec_avg(shrt3_bar)), market)"),
]

# --- 组2: mean_loan_rate_main (加权借贷利率) 反转 ---
E += [
    ("L1_rate_neg", "rank(multiply(-1, vec_avg(mean_loan_rate_main)))"),
    ("L2_rate_z252", "rank(multiply(-1, ts_zscore(vec_avg(mean_loan_rate_main), 252)))"),
    ("L3_rate_rank252", "rank(multiply(-1, ts_rank(vec_avg(mean_loan_rate_main), 252)))"),
    ("L4_rate_mean5_neg", "rank(multiply(-1, ts_mean(vec_avg(mean_loan_rate_main), 5)))"),
    ("L5_rate_hump", "rank(multiply(-1, hump(vec_avg(mean_loan_rate_main), 0.02)))"),
    ("L6_rate_grp_subind", "group_rank(multiply(-1, vec_avg(mean_loan_rate_main)), subindustry)"),
]

# --- 组3: loan_rate_volatility (借贷利率波动) ---
E += [
    ("V1_vol_neg", "rank(multiply(-1, vec_avg(loan_rate_volatility_p5_d1)))"),
    ("V2_vol_z252", "rank(multiply(-1, ts_zscore(vec_avg(loan_rate_volatility_p5_d1), 252)))"),
    ("V3_vol_rank252", "rank(multiply(-1, ts_rank(vec_avg(loan_rate_volatility_p5_d1), 252)))"),
    ("V4_vol_grp_subind", "group_rank(multiply(-1, vec_avg(loan_rate_volatility_p5_d1)), subindustry)"),
]

out = os.path.join(REPO, "tracking", "reference", "exprs_deu_shrt3_w13.json")
json.dump([[l, e] for l, e in E], open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
for l, e in E:
    print(f"  {l:28} {e}")
