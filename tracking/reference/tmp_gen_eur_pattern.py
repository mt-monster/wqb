# -*- coding: utf-8 -*-
"""生成 EUR pattern_scores probe 表达式清单（json: [[label, expr], ...]）。

设计原则（§0 铁律）：
  - 禁双腿加权相加；只用单一价差 / 比值 / 单腿时序几何
  - 信号概念：形态净倾向（看涨相似度 vs 看跌相似度）、形态突破强度、反转确认
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_pattern.json"

UP = "avg_similarity_upward_breakaway_gap_120"
UP2 = "avg_similarity_upward_symmetrical_triangle"
DN = "avg_similarity_downward_breakaway_gap_120"
DN2 = "avg_similarity_downward_symmetrical_triangle"
VB = "avg_similarity_v_reversal_bottom_120"
RA = "avg_similarity_rising_wedge_pattern_120"
FA = "avg_similarity_falling_wedge_pattern_120"
RS = "avg_similarity_rising_support_flat_resistance_120"
FS = "avg_similarity_falling_support_flat_resistance_120"
CONT = "avg_similarity_continuation_rising_wedge_120"
CONTF = "avg_similarity_continuation_falling_wedge"

C = [
    # ── 1. 形态净倾向（看涨 vs 看跌）—— 单一价差信号 ──
    ("p01_net_bull_gap",
     f"hump(group_rank(ts_decay_linear(divide(subtract({UP}, {DN}), add(add({UP}, {DN}), 0.0001)), 250), subindustry), hump=0.0025)"),
    ("p02_net_bull_tri",
     f"hump(group_rank(ts_decay_linear(divide(subtract({UP2}, {DN2}), add(add({UP2}, {DN2}), 0.0001)), 250), subindustry), hump=0.0025)"),
    # ── 2. 看涨形态强度（单腿，反转方向）──
    ("p03_vb_strength",
     f"hump(group_rank(ts_decay_linear({VB}, 250), subindustry), hump=0.0025)"),
    ("p04_up_gap_strength",
     f"hump(group_rank(ts_decay_linear({UP}, 250), subindustry), hump=0.0025)"),
    # ── 3. 反转 vs 延续（形态类型净倾向）──
    ("p05_reversal_vs_cont",
     f"hump(group_rank(ts_decay_linear(divide(subtract(add({VB}, {RA}), add({FA}, {CONT})), add(add({VB}, {RA}), add({FA}, {CONT}))), 250), subindustry), hump=0.0025)"),
    # ── 4. 支撑/阻力形态净倾向 ──
    ("p06_support_tilt",
     f"hump(group_rank(ts_decay_linear(divide(subtract({RS}, {FS}), add(add({RS}, {FS}), 0.0001)), 250), subindustry), hump=0.0025)"),
    # ── 5. 形态相似度变化（突破加速）──
    ("p07_up_gap_delta",
     f"hump(group_rank(ts_decay_linear(ts_delta({UP}, 20), 60), subindustry), hump=0.0025)"),
    ("p08_vb_delta",
     f"hump(group_rank(ts_decay_linear(ts_delta({VB}, 20), 60), subindustry), hump=0.0025)"),
    # ── 6. 形态时序排名强度（单腿）──
    ("p09_vb_tsrank",
     f"hump(group_rank(ts_decay_linear(ts_rank({VB}, 500), 250), subindustry), hump=0.0025)"),
    ("p10_up_gap_tsrank",
     f"hump(group_rank(ts_decay_linear(ts_rank({UP}, 500), 250), subindustry), hump=0.0025)"),
    # ── 7. 楔形方向净倾向 ──
    ("p11_wedge_tilt",
     f"hump(group_rank(ts_decay_linear(divide(subtract({RA}, {FA}), add(add({RA}, {FA}), 0.0001)), 250), subindustry), hump=0.0025)"),
    # ── 8. 下行形态反转（做空看跌形态）──
    ("p12_short_dn_gap",
     f"hump(group_rank(ts_decay_linear(multiply(-1, {DN}), 250), subindustry), hump=0.0025)"),
    # ── 9. industry 轴（隔离 interindustry）──
    ("p13_net_bull_gap_ind",
     f"hump(group_rank(ts_decay_linear(divide(subtract({UP}, {DN}), add(add({UP}, {DN}), 0.0001)), 250), industry), hump=0.0025)"),
    # ── 10. 市场轴 ──
    ("p14_vb_strength_mkt",
     f"hump(group_rank(ts_decay_linear({VB}, 250), market), hump=0.0025)"),
    # ── 11. 形态总强度（所有形态活跃度）──
    ("p15_pattern_activity",
     f"hump(group_rank(ts_decay_linear(add(add({UP}, {DN}), add({VB}, {RA})), 250), subindustry), hump=0.0025)"),
    # ── 12. 上行形态减下行（符号和，非加权）──
    ("p16_up_minus_dn_raw",
     f"hump(group_rank(ts_decay_linear(subtract({UP}, {DN}), 250), subindustry), hump=0.0025)"),
]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(C, f, ensure_ascii=False, indent=1)
print("wrote", OUT, len(C))
for l, e in C:
    print(f"  {l:24s} len={len(e)}")
