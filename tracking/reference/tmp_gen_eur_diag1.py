# -*- coding: utf-8 -*-
"""EUR pattern_scores 单变量诊断批：H1(去过度平滑) × H2(neutralization)。

固定源字段 = avg_similarity_v_reversal_bottom（经验库点名的 EUR 有效信号源）
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_diag1.json"
NU = sys.argv[2] if len(sys.argv) > 2 else "diag1"

VB = "avg_similarity_v_reversal_bottom"
UP = "avg_similarity_upward_breakaway_gap"
DN = "avg_similarity_downward_breakaway_gap"

# H1: 剥掉层层平滑 —— 从"重度平滑"到"裸 rank"
C = [
    ("h1a_naked_rank",     f"group_rank({VB}, subindustry)"),
    ("h1b_rank_rev",       f"group_rank(multiply(-1, {VB}), subindustry)"),
    ("h1c_raw_sub",        f"group_rank(subtract({UP}, {DN}), subindustry)"),
    ("h1d_light_decay",    f"group_rank(ts_decay_linear({VB}, 20), subindustry)"),
    ("h1e_ts_mean5",       f"group_rank(ts_mean({VB}, 5), subindustry)"),
    ("h1f_zscore",         f"group_zscore({VB}, subindustry)"),
    ("h1g_neg_zscore",     f"group_zscore(multiply(-1, {VB}), subindustry)"),
    ("h1h_rank_mkt",       f"group_rank({VB}, market)"),
]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(C, f, ensure_ascii=False, indent=1)
print("wrote", OUT, len(C), "nu=", NU)
