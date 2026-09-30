# -*- coding: utf-8 -*-
"""EUR 形态 diag4：rising wedge 强化 + 多形态合力 + 时序加速 + decay 扫描。

已知：
  - rising_wedge_pattern_120 取正 → S=+1.07（最强单形态）
  - falling_wedge / v_reversal_bottom → 取负有效
  - 规律：看跌形态相似度↑ → 收益↑（反转的反转）
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_diag4.json"
NU = sys.argv[2] if len(sys.argv) > 2 else "subindustry"

RW = "avg_similarity_rising_wedge_pattern_120"      # 看跌形态（取正 S=1.07）
AT = "avg_similarity_v_reversal_bottom"             # 看涨形态（取负 S=0.90）
AT120 = "avg_similarity_v_reversal_bottom_120"
FW = "avg_similarity_falling_wedge_pattern_120"     # 看涨（取负）
DTU = "desc_triangle_upward"                        # 三角形族
ATU = "mean_similarity_asc_triangle"
VT = "mean_similarity_reversal_v_top"               # 顶部反转 = 看跌
CVT = "mean_similarity_continuation_v_top"

C = [
    # A. rising wedge 强化：时序变化（形态新形成）
    ("a1_rw_delta20",    f"group_zscore(ts_delta({RW}, 20), {NU})"),
    ("a2_rw_delta60",    f"group_zscore(ts_delta({RW}, 60), {NU})"),
    ("a3_rw_z60",        f"group_zscore(ts_zscore({RW}, 60), {NU})"),
    ("a4_rw_tsrank",     f"group_zscore(ts_rank({RW}, 250), {NU})"),
    # B. 多形态合力（看跌形态族，方向一致）
    ("b1_two_bear",      f"group_zscore(add({RW}, {ATU}), {NU})"),
    ("b2_bear_3way",     f"group_zscore(add(add({RW}, {ATU}), {VT}), {NU})"),
    ("b3_bear_4way",     f"group_zscore(add(add({RW}, {VT}), add({ATU}, {CVT})), {NU})"),
    # C. 看跌 - 看涨（净倾向，单一价差）
    ("c1_bear_m_bull",   f"group_zscore(subtract(add({RW}, {VT}), add({AT}, {FW})), {NU})"),
    # D. reversal_v_top（顶部反转 = 看跌形态）
    ("d1_vtop_pos",      f"group_zscore({VT}, {NU})"),
    ("d2_cvt_pos",       f"group_zscore({CVT}, {NU})"),
    # E. 三角族
    ("e1_dtu_pos",       f"group_zscore({DTU}, {NU})"),
    ("e2_atu_pos",       f"group_zscore({ATU}, {NU})"),
]

json.dump(C, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(C), "nu=", NU)
