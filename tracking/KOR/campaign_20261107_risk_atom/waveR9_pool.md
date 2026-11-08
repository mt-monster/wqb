# Wave R9 池（锚点 × 2Y 破闸手册的设置轴 · READY）

> 依据：Claude/skills/brain-how-to-pass-alpha-test/references/two-year-sharpe-playbook.md
> 锚点：leA58QNO = subtract(0.5, group_rank(ts_mean(srisku−srisk, 66), sector)) · STATISTICAL · decay4 · trunc0.08
> 读数：**S 1.24 / F 0.93 / 2Y 1.41 / TO 0.0879 / raFail 3**

## 手册给的三条硬依据
1. **§1 中性化**（ZZ47696 GLB 同内核 7 组）：纯风险因子用 STATISTICAL/FAST/SLOW/SLOW_AND_FAST 时近两年 2Y 全崩
   （1.15 / 1.30 / 0.96 / 0.72），换 **CROWDING 2.17 / REVERSION_AND_MOMENTUM 2.04**，**全期 Sharpe 几乎不变**。
   机理解释：风险因子模型近两年与信号重叠，把有效收益一起中性化掉了。
   ⇒ 我的锚点正是纯风险因子（风险估计收缩幅度），完全命中该情形。
2. **⚠ 反向边界**：RAM/CROWDING **对反转类信号无效**（KOR risk71 实测 RAM 0.78/2Y −0.40、CROWDING 1.07/2Y −0.02）。
   ⇒ 不要把 RAM/CROWDING 用在 dsrt 反转族上；本战役反转族已判死（见下）。
3. **Fitness = Sharpe × √(505 × margin)**，且 margin 几乎只由 setting 决定（换 setting 跨 2.3×）
   ⇒ 换中性化有机会**同时**修 2Y 与 F（我当前 F 0.93 只差 0.07）。

## 手册 §4 已正式判死 KOR 残差反转家族（与本战役独立结论一致）
- risk71 上 8 变体（低换手门控 / 换手 sign-switch / 缩量门控 / 内层 industry GN / RAM / CROWDING / 波动门控 / signed_power）**全部 2Y ≤ 0.16**。
- 成因：KOR 2022–23 题材动量 + 2023-11 卖空禁令。判死范围是 **(region, family)**。
- 本战役 R2 独立复现：omEJq8mk S2.13/2Y0.10、d5W3jkkw S2.49/2Y−0.47、9qxdXZZq S1.57/2Y−0.02。
- ⇒ **反转族不再投入**（含 omEJq8mk）；RAM/CROWDING 也救不了它。

## R9 表达式（8 条几何，**统一用 neutralization=CROWDING**，decay4 trunc0.08）
记号 D = subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk)

| # | 目的 | 算子 | 表达式 |
|---|---|---:|---|
| R9-01 | **对照臂**（隔离中性化效应，必须留） | 4 | subtract(0.5, group_rank(ts_mean(D, 66), sector)) |
| R9-02 | 手册§2 内层 GN 细粒度 subindustry | 5 | subtract(0.5, group_rank(group_neutralize(ts_mean(D, 66), subindustry), sector)) |
| R9-03 | 手册§2 内层 GN industry | 5 | subtract(0.5, group_rank(group_neutralize(ts_mean(D, 66), industry), sector)) |
| R9-04 | 手册§2 signed_power 0.5 压长尾 | 5 | subtract(0.5, group_rank(signed_power(ts_mean(D, 66), 0.5), sector)) |
| R9-05 | 手册§2 quantile(normalize) 替代 rank | 5 | quantile(normalize(ts_mean(D, 66))) |
| R9-06 | 手册§2 外层 ts_zscore 252 | 5 | ts_zscore(subtract(0.5, group_rank(ts_mean(D, 66), sector)), 252) |
| R9-07 | ts_decay_linear 替 ts_mean（换平滑几何） | 4 | subtract(0.5, group_rank(ts_decay_linear(D, 66), sector)) |
| R9-08 | 手册§2 margin 回补 ts_av_diff 66 | 5 | subtract(0.5, group_rank(ts_av_diff(ts_mean(D, 66), 66), sector)) |

## 关键铁律（手册明示，易踩）
- **内层 GN 粒度必须严格细于外层 setting**，否则被外层投影吸收（内 industry + 外 SUBINDUSTRY → SELF_CORR 0.993 ≈ 恒等）。
  CROWDING 不是分组轴，因此内层 GN 不会被吸收。
- **换手低给小 decay**：本族 TO 0.0879 极低，decay=4 可能偏大 ⇒ 后续单开一波扫 decay {1,2}。
- 手册说 ts_zscore 外层用来修 Weight Concentration；但我 R4 测过 **内层** ts_zscore(D,252) S 仅 0.03，位置不同，勿混淆。

## 执行计划（2 槽，串行）
1. R9 = 上述 8 条 × neutralization=**CROWDING**
2. R10 = 同样 8 条（可精简到 4 条）× neutralization=**REVERSION_AND_MOMENTUM**
3. 取两批最优 → 单开 decay {1,2} + trunc {0.05} 微调
4. 过关件 → 逐年覆盖 + self/prod MCP 终验
