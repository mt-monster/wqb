# -*- coding: utf-8 -*-
"""KOR insd5 第三批：H1/H2 强信号（2Y=-2.7）取反 + 推 S。
核心: divide(vec_sum(insd5_trd_amt), vec_sum(insd5_source_data)) —— 交易额/持股数
取反 = 内部人交易活跃度反向（2Y 预期 +2.7）
推 S 旋钮: decay / 分组轴 / signed_power / 双窗 / 归一化
"""
import json, os
REPO = r"D:\coding\traeCN_project\wqb"
E = []
def add(l, e): E.append([l, e])

BASE = "divide(vec_sum(insd5_trd_amt), add(1, vec_sum(insd5_source_data)))"

# --- K 组：直接取反 ---
add("K1_neg_base", f"group_rank(multiply(-1, {BASE}), sector)")
add("K2_neg_base_hump", f"hump(group_rank(multiply(-1, {BASE}), sector), hump=0.003)")
add("K3_neg_tsmean22", f"group_rank(multiply(-1, ts_mean({BASE}, 22)), sector)")
add("K4_neg_tsmean66", f"group_rank(multiply(-1, ts_mean({BASE}, 66)), sector)")
add("K5_neg_decay_linear10", f"hump(group_rank(multiply(-1, ts_decay_linear({BASE}, 10)), sector), hump=0.003)")
add("K6_neg_decay_linear20", f"hump(group_rank(multiply(-1, ts_decay_linear({BASE}, 20)), sector), hump=0.003)")

# --- L 组：换分组轴（subindustry / industry / market / 无分组） ---
add("L1_neg_subind", f"group_rank(multiply(-1, {BASE}), subindustry)")
add("L2_neg_ind", f"group_rank(multiply(-1, {BASE}), industry)")
add("L3_neg_market", f"group_rank(multiply(-1, {BASE}), market)")
add("L4_neg_plain_rank", f"rank(multiply(-1, {BASE}))")
add("L5_neg_zscore", f"zscore(multiply(-1, {BASE}))")

# --- M 组：signed_power 压尾 + 时序归一 ---
add("M1_neg_sp05", f"signed_power(group_rank(multiply(-1, {BASE}), sector), 0.5)")
add("M2_neg_tsrank252", f"group_rank(ts_rank(multiply(-1, {BASE}), 252), sector)")
add("M3_neg_tszscore252", f"group_rank(ts_zscore(multiply(-1, {BASE}), 252), sector)")
add("M4_neg_tsdelta22", f"group_rank(ts_delta(multiply(-1, {BASE}), 22), sector)")

# --- N 组：二次取反确认（正号版本，验证符号） ---
add("N1_pos_base", f"group_rank({BASE}, sector)")
add("N2_neg_ratio_inverse", "group_rank(divide(vec_sum(insd5_source_data), add(1, vec_sum(insd5_trd_amt))), sector)")

out = os.path.join(REPO, "tracking/reference/exprs_kor_insd5_w3.json")
json.dump(E, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {len(E)} -> {out}")
for l, e in E: print(f"  {l:26s} {e[:118]}")
