# -*- coding: utf-8 -*-
"""EUR 形态 diag2：在已验证方向（取负、裸 rank）上做单变量精调。

基线：group_zscore(multiply(-1, VB), subindustry)  S=0.90
变量：
  A. 中性化扫描（SUBINDUSTRY / INDUSTRY / MARKET / SECTOR / STATISTICAL / SLOW_AND_FAST / NONE）
  B. 分组轴 + 外层平滑（ts_decay_linear 短窗 5/20/60）
  C. 形态族扩展（其他底部/顶部形态取负）
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_diag2.json"
VB = "avg_similarity_v_reversal_bottom"
VT = "avg_similarity_v_reversal_top"
UP = "avg_similarity_upward_breakaway_gap_120"
DN = "avg_similarity_downward_breakaway_gap_120"
RA = "avg_similarity_rising_wedge_pattern_120"
FA = "avg_similarity_falling_wedge_pattern_120"

C = [
    # A. 中性化由 CLI 扫；这里固定 SUBINDUSTRY，扫外层平滑与分组轴
    ("a1_raw_neg_z_sub",      f"group_zscore(multiply(-1, {VB}), subindustry)"),
    ("a2_neg_z_ind",          f"group_zscore(multiply(-1, {VB}), industry)"),
    ("a3_neg_z_mkt",          f"group_zscore(multiply(-1, {VB}), market)"),
    ("a4_neg_rank_smooth5",   f"group_rank(ts_decay_linear(multiply(-1, {VB}), 5), subindustry)"),
    ("a5_neg_rank_smooth20",  f"group_rank(ts_decay_linear(multiply(-1, {VB}), 20), subindustry)"),
    ("a6_neg_rank_smooth60",  f"group_rank(ts_decay_linear(multiply(-1, {VB}), 60), subindustry)"),
    # B. 形态族：顶部 vs 底部（按研究：top->负、bottom->正，但我们实测 bottom 取负有效 → 全部取负试）
    ("b1_neg_vt",             f"group_zscore({VT}, subindustry)"),   # top 取正 = 等价 -(-top)
    ("b2_neg_upgap",          f"group_zscore(multiply(-1, {UP}), subindustry)"),
    ("b3_neg_risingwedge",    f"group_zscore(multiply(-1, {RA}), subindustry)"),
    ("b4_neg_fallingwedge",   f"group_zscore({FA}, subindustry)"),
    # C. 多形态净倾向（单一价差信号，合规）
    ("c1_top_m_bottom",       f"group_zscore(subtract({VT}, {VB}), subindustry)"),
    ("c2_bottom_m_top",       f"group_zscore(subtract({VB}, {VT}), subindustry)"),
]

json.dump(C, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(C))
