# BE76 派发：pwaYqa6X 定向放大 8 臂（2026-11-12）

> 前置：BE75 8/8 ERROR 为平台瞬断——甄别批完整复现 pwaYqa6X S1.23/F0.92/TO0.079（与 BE70 一致）。
> 配方有效，本轮按 v2 L2 升级满波冲 S≥1.58 + 修 sub(0.30→0.58) + 修 2Y(0.69→1.58)。

## 八臂（全部 ≤12 算子，两腿均为开放族：PV×INSIDERS 双未点亮塔）

| 臂 | 变体 | 目的 |
|---|---|---|
| 1 | 两腿 winsorize(std=3) | 压尾提 sub |
| 2 | 成交额换 adv20_usd_capped_100m | 字段变体（BE68 读 0.95/2Y1.28） |
| 3 | 内部人腿换 ts_zscore(·,504) | 两腿窗口对齐 |
| 4 | 内部人腿换 insd1_valueeur（金额口径） | 论坛帖：金额口径优于数量 |
| 5 | 内部人腿换 insider_agg directional_indicator | 换数据集（同塔） |
| 6 | 三字段：+ news 情绪（无回填） | 外部报告：第三字段修 Ladder |
| 7 | **比值语义**：成交额 ÷ 内部人持仓（单位持仓流动性） | 两字段合一（省算子）+ 论坛 conviction 同构 |
| 8 | 内部人腿窗口 66→132 | decay 加深修 2Y |

## 判读预案

- 任一臂 S≥1.58 且 sub≥0.474S 且 2Y≥1.58 ⇒ 候选 #12（PV×INSIDERS 双未点亮塔）→ self/prod 终验；
- 若臂 7（比值语义）最强 ⇒ 与论坛 conviction 配方同构 ⇒ 需查与 2rmGAPqN 的族距离（inflection：2rmGAPqN 也是 valueeur/holdings 比值）；
- 若全部 <1.3 ⇒ pv20 流动性面天花板记录，转 option1/pattern_scores 待发波。