# Wave F6 设计（2026-11-07，槽位空即派）

> 前置事实：fnd90 cfc market 轴 S1.02/F0.87/sub0.96/margin97bp 但 2Y 0.42（2023 S 0.01 信号死亡征兆）；icfroe3y 2Y 1.36、pscore 2Y 1.12 是 fnd90 近年仍活的两轴。中性化 3 点曲线：SUBINDUSTRY（基线已有）+ FAST（F5 在飞）+ SLOW（本波）。

## F6-SLOW 批（中性化对比第 2 点，8 条 = F5-FAST 同式）
W1/W2/W8/W9/W6/W10 fnd45 + icfroe subind/sector fnd90，neutralization=SLOW。
判读：三点曲线找「S 抬且 2Y 不崩」的中间档。

## F6-B 批（SUBINDUSTRY 设置，cfc 深化 + 2Y 修复 8 条）
| # | 表达式 | 目的 |
|---|---|---|
| C1 | group_zscore(ts_backfill(fnd90_game_cash_flow_coverage, 252), market) | rank→zscore 几何对照（保幅值，PPA 实证 zscore 救 sub 的同族手段） |
| C2 | group_rank(ts_backfill(fnd90_game_cash_flow_coverage, 66), market) | 回填窗 66 vs 252（信号新鲜度） |
| C3 | winsorize(group_rank(ts_backfill(fnd90_game_cash_flow_coverage, 252), market), std=4) | rank 后 winsorize 改权重几何（risk70 先例：放 rank 之后才真改变） |
| C4 | group_rank(add(rank(ts_backfill(fnd90_game_cash_flow_coverage, 252)), rank(ts_backfill(fnd90_qes_gamef_icfroe_3y, 252))), market) | cfc(前置强) × icfroe3y(2Y1.36 近年活) 2 腿互补 |
| C5 | group_rank(subtract(rank(ts_backfill(fnd90_game_cash_flow_coverage, 252)), rank(ts_backfill(fnd90_qes_gamef_ohlson, 252))), market) | cfc − ohlson（质量−困境）2 腿 |
| C6 | group_rank(ts_delta(ts_backfill(fnd90_game_cash_flow_coverage, 252), 66), market) | 改善趋势轴（修 2023 死亡：水平→动量） |
| C7 | group_rank(ts_backfill(fnd90_qes_gamef_icfroe_5y, 252), market) | icfroe 也换 market 轴（cfc 的 market 跳变复刻测试） |
| C8 | group_rank(ts_backfill(fnd90_game_cash_flow_coverage, 252), sector) | sector 中间粒度 |

算子数：全部 2-7 ≤12 ✓。同数据集双腿 add 不违禁混（ATOM 单数据集）。
判读预案：C4/C5 若 S≥1.2 且 2Y≥1.0 → 直升全闸候选；C6 若救活 2Y 但 S<0.8 → 动量轴与水平轴互补配对再混；C1 若 sub/S 改善 → 权重几何换轴有效。
