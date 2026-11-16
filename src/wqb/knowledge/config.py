# -*- coding: utf-8 -*-
"""经验蒸馏阈值（单一来源，2026-11-15）。

这些数字决定“多少样本才算一条统计先验”“什么算死路提案”。它们**不直接拦候选**：
- `distill` 只据此产出统计 / 提案；
- `build_wave` 只据此做可逆降权；
- 判死仍必须走 `seal_dead_end` 的论坛取证闸。
"""
from __future__ import annotations

#: 单族/单骨架进入统计的最小样本数
MIN_FAMILY_N = 3
#: 单格（region×设置维度）进入过闸率统计的最小样本数
MIN_CELL_N = 3
#: 判“统计层面死路”的最高 sharpe（不是平台闸，只是提案门槛）
DEAD_MAX_SHARPE = 1.0
#: 判死路时主导墙的最低占比
DEAD_WALL_SHARE = 0.8
#: 进 priors 的 family / skeleton 名额
TOP_FAMILIES = 40
TOP_SKELETONS = 40
#: 蒸馏里每个族保留的示例 alpha 数
EXAMPLES = 5
#: 统计规则从 proposed 晋升 active 需要的**独立波次**确认数（P3）
PROMOTE_MIN_CONFIRMATIONS = 2
#: near 池的默认 sharpe 线（区域 thresholds 缺省时使用）
NEAR_SHARPE_MIN = 1.0
