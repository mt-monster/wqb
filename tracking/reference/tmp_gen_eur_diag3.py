# -*- coding: utf-8 -*-
"""EUR 形态 diag3：楔形源强化 + decay 扫描 + universe 扫描（目标 S>=1.58）。

已验证：
  - 裸 group_zscore(field, subindustry) 优于任何平滑
  - 所有形态相似度 = 反转信号（越像越回归）→ 全部取正号
  - 楔形 rising/falling 取负得 -1.07/-1.05 → 取正应有 +1.05~1.07（最强）
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_diag3.json"
NU = sys.argv[2] if len(sys.argv) > 2 else "subindustry"

RS = "avg_similarity_rising_wedge_pattern_120"
FS = "avg_similarity_falling_wedge_pattern_120"
RS0 = "avg_similarity_rising_wedge_pattern"
FS0 = "avg_similarity_falling_wedge_pattern"
VB = "avg_similarity_v_reversal_bottom"
VB120 = "avg_similarity_v_reversal_bottom_120"
CONTF = "avg_similarity_continuation_falling_wedge"
CONTR = "avg_similarity_continuation_rising_wedge_120"

C = [
    # 楔形源（取正号）
    ("w1_rs_pos",      f"group_zscore({RS}, {NU})"),
    ("w2_fs_pos",      f"group_zscore({FS}, {NU})"),
    ("w3_rs0_pos",     f"group_zscore({RS0}, {NU})"),
    ("w4_fs0_pos",     f"group_zscore({FS0}, {NU})"),
    # 楔形净倾向（单一价差）
    ("w5_rs_m_fs",     f"group_zscore(subtract({RS}, {FS}), {NU})"),
    ("w6_rs_p_fs",     f"group_zscore(add({RS}, {FS}), {NU})"),
    # V底两组（有无 _120 后缀 = 不同 lookback）
    ("w7_vb_pos",      f"group_zscore({VB}, {NU})"),
    ("w8_vb120_pos",   f"group_zscore({VB120}, {NU})"),
    # 延续楔形
    ("w9_contf_pos",   f"group_zscore({CONTF}, {NU})"),
    ("w10_contr_pos",  f"group_zscore({CONTR}, {NU})"),
    # 全形态合力（多形态平均，单一信号）
    ("w11_all4",       f"group_zscore(add(add({RS}, {FS}), add({VB}, {CONTF})), {NU})"),
    # ts_rank 版（形态历史高位 = 形态成熟）
    ("w12_rs_tsrank",  f"group_rank(ts_rank({RS}, 250), {NU})"),
]

json.dump(C, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(C), "nu=", NU)
