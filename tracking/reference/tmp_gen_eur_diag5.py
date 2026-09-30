# -*- coding: utf-8 -*-
"""EUR diag5：把两个最强机制正交组合 + 单一信号结构化。

diag4 结果：
  c1_bear_m_bull = group_zscore((rw+vt)-(vb+fw), sub)  S=1.27 F=0.70
  a3_rw_z60      = group_zscore(ts_zscore(rw,60), sub) S=1.25 F=0.56
  a4_rw_tsrank   = group_zscore(ts_rank(rw,250), sub)  S=1.16 F=0.55
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_diag5.json"
NU = sys.argv[2] if len(sys.argv) > 2 else "subindustry"

RW = "avg_similarity_rising_wedge_pattern_120"
RB = "avg_similarity_v_reversal_bottom"
FW = "avg_similarity_falling_wedge_pattern_120"
VT = "mean_similarity_reversal_v_top"
AT = "mean_similarity_asc_triangle"
CVT = "mean_similarity_continuation_v_top"

C = [
    # A. 时序化净倾向（a3 机制 × c1 结构）—— 单一价差信号
    ("A1_z_bear_m_bull",  f"group_zscore(subtract(ts_zscore({RW}, 60), ts_zscore({RB}, 60)), {NU})"),
    ("A2_z_rw_only",      f"group_zscore(ts_zscore({RW}, 120), {NU})"),
    ("A3_z_rw_250",       f"group_zscore(ts_zscore({RW}, 250), {NU})"),
    ("A4_z_rw_20",        f"group_zscore(ts_zscore({RW}, 20), {NU})"),
    # B. 净倾向的时序化（价差再做时序）
    ("B1_tsz_of_diff",    f"group_zscore(ts_zscore(subtract({RW}, {RB}), 60), {NU})"),
    ("B2_tsr_of_diff",    f"group_zscore(ts_rank(subtract({RW}, {RB}), 250), {NU})"),
    # C. 净倾向扩展（加更多看跌形态）
    ("C1_bmb_3bear",      f"group_zscore(subtract(add(add({RW}, {VT}), {AT}), add({RB}, {FW})), {NU})"),
    ("C2_bmb_cvt",        f"group_zscore(subtract(add(add({RW}, {VT}), {CVT}), add({RB}, {FW})), {NU})"),
    # D. 纯净单腿时序（最简结构）
    ("D1_rw_tsz_solo",    f"group_zscore(ts_zscore({RW}, 60), {NU})"),
    ("D2_rw_tsr_solo",    f"group_zscore(ts_rank({RW}, 250), {NU})"),
    # E. 组合：净倾向 + 时序双重确认（乘性，非加权加）
    ("E1_z_times_bmb",    f"group_zscore(multiply(ts_zscore({RW}, 60), subtract({RW}, {RB})), {NU})"),
    ("E2_rank_of_z",      f"group_rank(ts_zscore({RW}, 60), {NU})"),
]

json.dump(C, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(C), "nu=", NU)
