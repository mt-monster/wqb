# -*- coding: utf-8 -*-
"""KOR insd5 第四批：修正取反手法（关键发现：group_rank(-x) != -group_rank(x)）。
正确取反 = subtract(0.5, group_rank(x)) 或 multiply(-1, group_rank(x))。
目标：把 H1/H2 的 S=-0.96 转成 +0.96，2Y 从 -2.72 转 +2.72。
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"
E = []
def add(l, e): E.append([l, e])

BASE = "divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data)))"
BASE2 = "ts_decay_linear(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data))), 10)"

# --- P 组：正确取反（在 rank 外层）---
add("P1_sub05_rank", f"subtract(0.5, group_rank({BASE}, sector))")
add("P2_neg_rank_out", f"multiply(-1, group_rank({BASE}, sector))")
add("P3_sub05_rank_hump", f"subtract(0.5, hump(group_rank({BASE}, sector), hump=0.003))")
add("P4_sub05_rank2", f"subtract(0.5, group_rank({BASE2}, sector))")
add("P5_neg_rank2_out", f"multiply(-1, group_rank({BASE2}, sector))")

# --- Q 组：反转被排序对象（rank 内取负 → 1-rank，等价取反）---
add("Q1_rank_neg_in", f"hump(subtract(1, group_rank({BASE}, sector)), hump=0.003)")
add("Q2_group_rank_neg_in", f"group_rank(ts_rank(multiply(-1, {BASE}), 252), sector)")

# --- R 组：直接对原始信号取负（不 rank），让中性化处理 ---
add("R1_neg_raw", f"multiply(-1, {BASE})")
add("R2_neg_raw_hump", f"hump(multiply(-1, {BASE}), hump=0.003)")
add("R3_neg_raw_decay", f"hump(multiply(-1, {BASE2}), hump=0.003)")
add("R4_neg_raw_zscore", f"zscore(multiply(-1, {BASE}))")

# --- S 组：其他强信号正确取反（I2/J1/G1）---
add("S1_neg_I2", "subtract(0.5, hump(group_rank(ts_decay_linear(divide(vec_sum(insd5_vol_af), add(1, vec_sum(insd5_vol_bf))), 20), sector), hump=0.003))")
add("S2_neg_J1", "subtract(0.5, hump(group_rank(divide(vec_sum(insd5_fa_tr), add(0.001, vec_sum(insd5_fb_tr))), sector), hump=0.003))")
add("S3_neg_G1", "subtract(0.5, group_rank(divide(subtract(vec_sum(insd5_vol_af), vec_sum(insd5_vol_bf)), add(1, vec_sum(insd5_vol_bf))), sector))")

# --- T 组：trd_amt 变体（不同分母）---
add("T1_amt_over_vol", "subtract(0.5, group_rank(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_vol_bf))), sector))")
add("T2_amt_over_data", "subtract(0.5, group_rank(divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_data))), sector))")
add("T3_amt_log", "subtract(0.5, group_rank(log(add(1, vec_sum(insd5_trd_amt))), sector))")

out = os.path.join(REPO, "tracking/reference/exprs_kor_insd5_w4.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
for l, e in E: print(f"  {l:22s} {e[:118]}")
