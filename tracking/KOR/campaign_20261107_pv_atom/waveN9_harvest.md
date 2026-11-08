# Wave N9 收割（MARKET 基座 × lv60 合取腿 × delta 窗口 / ts_rank 包装）

- 派发：2026-11-07 12:17 · 设置 KOR/TOP600/D1 · MARKET · decay 4 · trunc 0.08 · nan ON
- multisim：2Ti4Pc1dK4O4bf8L94Y6aV2（2 条）+ 18z7CseMR4E29Ih1cmzBk2Y4（2 条）· 全部 COMPLETE / error 0

| id | 变体 | S | F | 2Y | sub | TO | raFail |
|---|---|---:|---:|---:|---:|---:|---:|
| rKRG91g9 | d10 × lv60 | 1.72 | 1.39 | 2.16 | 1.54 | 0.1967 | 0 |
| gJeGXMdm | ts_rank(d5,126) × lv60 | 1.66 | 1.14 | 2.15 | 1.51 | 0.2631 | 0 |
| xArGVkWg | ts_rank(d5,66) × lv60 | 1.63 | 1.11 | 2.12 | 1.49 | 0.2667 | 0 |
| JjezoVZj | d3 × lv60 | 1.49 | 0.89 | 1.95 | 1.35 | 0.3229 | 2 |

骨架统一为：multiply(group_rank(<激增腿>, sector), group_rank(ts_mean(probability_label1_2quantile_60day_ohlcv, 22), sector))
激增腿取值：d10 = ts_delta(p_5d, 10)；ts_rank 臂 = ts_rank(ts_delta(p_5d,5), W)；d3 = ts_delta(p_5d, 3)。

## 归因
1. delta 窗口单调：d3 1.49 → d5(基准) 1.88 → d10 1.72。d5 仍是峰；d10 拿到本波最高 Fitness 1.39 与最高 sub/S 0.895。
2. ts_rank 包装是纯降级：同一 delta 加 ts_rank(66/126) 后 S 由 1.88 掉到 1.63/1.66、F 由 1.35 掉到 1.11/1.14。
   机理：ts_rank 抹掉激增幅度、只留次序，与「激增强度即信号」相悖 ⇒ 该杠杆关闭。
3. sub 闸全绿：4 条 sub/S 均约 0.90，远高于 0.474 阈值 ⇒ 信号非边缘股驱动，与 risk71 的假活口不同。

## 结论
- N9 未产生新的越线件：最强 rKRG91g9 的 S 1.72 < 基准 0mYgpJzK 的 1.89。
- 但 rKRG91g9 相对 xArGra8W（d5×lv60 MARKET，prod 0.7688）是「换 delta 窗口」的结构异质变体，
  持仓不同，是本族仅剩的、尚未测 prod 的候选之一。
- 表达式杠杆已全部试完：中性化换基 −0.037 / lv22→lv60 −0.02~0.03 / decay8 反效果 / trunc 不 binding /
  delta 位移与 ts_rank 包装均降 S / winsorize 后置无效 / vector_neut 幂等 / 异源（P-down、分位桶）全灭。
  累计只能 −0.049，未达所需 −0.118。
- 本族剩余未测维度：universe（TOP600 → TOP400/TOP200）与 rKRG91g9 的 prod 实测。
