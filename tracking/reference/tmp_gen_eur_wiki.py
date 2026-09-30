# -*- coding: utf-8 -*-
"""EUR other571（Wikipedia 浏览量）注意力信号表达式。

研究依据（2026-09-29 WebSearch）：
  - Han 2026 (Russell 1000)：注意力溢价 t=2.16~3.14，组合 Sharpe 1.30；零售重股溢价 2.1×
  - Pyun 2024 (Economics Letters)：浏览量上升 → 收益上升（tercile 单调）；**周频 > 月频**
  - fffinstill 2026（70,886 obs 实测）：>3x 尖峰 → 次周 −0.95%（64% 负）→ 反向
  - Da/Engelberg/Gao 2011：关注度尖峰 → 当日 +0.5~0.8%，1-3 月后反转
  ⇒ **两阶段**：注意力加速 → 短期正；见顶 → 反转。
  ⇒ 信号构造 = 用短窗 vs 长窗的**加速比**（views7d / views28d）捕捉第一阶段；
     用 views1y 归一化消除规模效应。
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "tracking/reference/exprs_eur_wiki.json"

T = "oth571_viewstoday"
D7 = "oth571_views7d"
D14 = "oth571_views14d"
D28 = "oth571_views28d"
D84 = "oth571_views84d"
Y1 = "oth571_views1y"
M7 = "oth571_views7dmobile"

C = [
    # A. 注意力加速（短窗 vs 长窗）
    ("wik1_acc7_28",   f"group_zscore(divide({D7}, add({D28}, 1)), subindustry)"),
    ("wik2_acc7_84",   f"group_zscore(divide({D7}, add({D84}, 1)), subindustry)"),
    ("wik3_acc14_84",  f"group_zscore(divide({D14}, add({D84}, 1)), subindustry)"),
    ("wik4_acc28_y1",  f"group_zscore(divide({D28}, add({Y1}, 1)), subindustry)"),
    # B. 注意力水平（规模归一化）
    ("wik5_lvl7_y1",   f"group_zscore(divide({D7}, add({Y1}, 1)), subindustry)"),
    ("wik6_lvl28_y1",  f"group_zscore(divide({D28}, add({Y1}, 1)), subindustry)"),
    ("wik7_lvl1y",     f"group_zscore({Y1}, subindustry)"),
    # C. 日频尖峰（当日 vs 7d 均值）
    ("wik8_spike",     f"group_zscore(divide({T}, add(divide({D7}, 7), 1)), subindustry)"),
    # D. 时序加速
    ("wik9_d7_delta",  f"group_zscore(ts_delta(divide({D7}, add({D28}, 1)), 20), subindustry)"),
    ("wik10_d28_delta", f"group_zscore(ts_delta({D28}, 20), subindustry)"),
    # E. 反向版（尖峰后反转）
    ("wik11_spike_neg", f"group_zscore(multiply(-1, divide({T}, add(divide({D7}, 7), 1))), subindustry)"),
    ("wik12_acc_neg",   f"group_zscore(multiply(-1, divide({D7}, add({D28}, 1))), subindustry)"),
]

json.dump(C, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(C))
