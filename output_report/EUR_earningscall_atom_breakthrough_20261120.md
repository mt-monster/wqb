# EUR / earningscall_sentiment ATOM 突破报告（2026-11-20）

> 数据集：`earningscall_sentiment`（164 字段 = 121 MATRIX + 23 VECTOR + 元数据，cov 0.5115，aC 1306，mult 1.5，
> 2025-11-01 新 onboard）｜平台 category=other ⇒ `pyramids.list` = **EUR/D1/OTHER**
> **表达式只含本集字段 + 豁免分组轴 = 纯 ATOM**，符合用户 2026-11-20 指令「已点亮塔除非 ATOM 不再投入」的例外条款。
> 画像：`tracking/EUR/reference/profiles/eur_other_earningscall_sentiment_profile_20261120.md`（完整性闸 164/164 PASS）

## 1. 回测规模与结论

| 阶段 | 臂数 | 结果 |
|---|---:|---|
| 段1 基线模板（5 极性 + 4 answer + 3 count 净差） | 12 | 全 REJECT，S 0.20–0.51，但**全正**、TO 4.4%、sub 全正 |
| 段2 形态验证（含 8 臂工程 FAIL） | 10 | 修正后 2 臂跑通；**事件门控臂 S1.44** |
| 段3 定向优化（轴/窗口/门控/截断） | 28 | **3 臂平台 RA 全过（failed_ra_count=0）** |
| 段4 prod 定向（轴间差分/缺失模式） | 8 | 见 §5 |
| **合计** | **58+** | **平台闸全绿候选 3 颗** |

## 2. ★ 核心机制：稀疏事件型数据集必须用 presence 门控

| 形态 | alpha | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| 无门控骨架 | O0WJnn9q 等 | 0.20–0.51 | ≤0.19 | 0.88–1.38 | 4.4% |
| + `trade_when(answer_chunk_count > 0, ·, -1)` zscore252 | A1xQloVX | 1.44 | 0.75 | **2.17** | 3.78% |
| + zscore504 | rK7d5REo | **1.58** | 0.89 | 2.26 | 3.69% |
| + zscore756 + trunc0.02 | **omaoLaJl** | **1.76** | **1.05** | 2.25 | 3.62% |
| 宽门控 + bf252 + zscore1512 | **78YoLMK1** | **1.71** | **1.01** | **2.13** | 3.50% |
| 宽门控 + bf252 + zscore1008（decay1） | rK7dR823 | 1.71 | 1.00 | 2.17 | 4.09% |
| 宽门控 + bf504 + zscore1008（decay1） | MP60YVGk | 1.70 | 1.00 | 2.18 | 4.08% |

**门控版逐年（10 年全正）**：1.57/1.02/1.52/0.21/1.44/0.92/1.36/1.75/2.19/2.21
（无门控版 2015–2017 连续负年 = regime 段，被门控彻底抹平）。

**机制**：电话会语调只在**事件日**有信息；presence 门控 = 只在事件发生时持仓，非事件日空仓。
⇒ **稀疏事件型数据集（季频电话会/公告/财报）若不用 presence 门控，信号会被大面积 NaN 摊薄**。
与 socialmedia15 的 buzz 门控线索（独立数据集）结论一致——**这是可迁移的通用形态**。

## 3. ★ CONCENTRATED_WEIGHT 的根因与解法（用户 2026-11-20 提示 group_backfill 解 CW）

- **现象**：窄门控（`answer_chunk_count > 0`）全部臂 CW = 0.5（限 0.1，超 5 倍）。
- **truncation 0.08→0.02 完全无效** ⇒ 不是权重上限问题，是**持仓面窄**（门控只在电话会当日生效）。
- **解法（实测验证）**：
  - **宽门控** `ts_sum(answer_chunk_count, 22) > 0`（22 天内有事件即持仓）⇒ **CW 直接 PASS**，代价 S −0.23；
  - **group_backfill 填 NaN / 填门控字段** ⇒ 同方向扩散持仓面（另一条解法，见段4 臂表）。
- **平台闸全绿组合 = 宽门控（解 CW）+ 长窗（补 S）**：`ts_sum(answer_chunk_count,22)>0` + `ts_zscore(ts_backfill(mean_polarity_profitability_summary,252),1512)`
  → S1.71/F1.01/2Y2.13/sub1.51/TO3.5%/DD2.7%，**failed_ra_count=0，checks.fail 为空**。

## 4. 机制归因表（可迁移）

| 轴 | 结论 |
|---|---|
| 门控宽度 | 窄（当日）S 最高但 CW 失败；宽（22–44 天）CW 过、S −0.2 ⇒ **CW 与 S 二者需交换** |
| zscore 窗 | 252→504→756→1008→1512 **单调抬 S**（1.44→1.58→1.76），本族长窗是主杠杆 |
| backfill 窗 | 252 略优于 66 |
| 分组轴 | industry > sector ≫ subindustry（subindustry 明显更差） |
| 语调轴 | profitability > assetutilization > cashflow > leverage |
| 节段 | **summary 优于 presentation**（尽管 presentation aC 160 最高——拥挤度反而是负担） |
| 宇宙 | TOP2500 > TOPCS1600（ΔS 0.2–0.4） |
| count 净差 | 与 polarity 同向但更弱 |
| F 数学 | TO 3.5% 触 0.125 地板 ⇒ F = S×√(ret/0.125)，**F≥1 需 ret≥4.24% 或 S↑** |

## 5. 相关性闸与交付判定

| alpha | S | F | 2Y | sub | self | prod | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| 78YoLMK1 | 1.71 | 1.01 | 2.13 | 1.51 | **0.357**（PASS） | **0.7815** ❌ | 平台闸全绿但 prod 超线 |
| rK7dR823 | 1.71 | 1.00 | 2.17 | 1.50 | — | **0.7926** ❌ | 同上 |
| MP60YVGk | 1.70 | 1.00 | 2.18 | 1.49 | — | 待测 | — |
| omaoLaJl（窄门控） | 1.76 | 1.05 | 2.25 | 1.36 | — | pending | CW 0.5 未过 |

**prod 0.78 = 信息源级墙的判据**（论坛 post 44678103399575 共识：「调窗口/权重/中性化造不出低 prod，
只有换数据源或换经济逻辑才行」；同集 sent_matrix 先例 prod 0.87–0.92）。**电话会语调 = 经典因子，生产池已饱和。**

**降 prod 的三条尝试方向（段4 派发中）**：
1. **轴间差分**（profitability − assetutilization / leverage / cashflow）⇒ 换经济逻辑但仍在同一信息源；
2. **缺失数据模式**（`ts_count_nans` / `ts_arg_max`）⇒ 论坛 post 44682095618455 提的独立信号维度（报道缺失模式本身含信息）；
3. **节段差**（answer − question）⇒ 提问 vs 回答的信息含量差。

## 6. 未完成 / 下一步

- 段4（8 臂 prod 定向）待收割；MP60YVGk 的 prod 待平台槽位。
- **未提交任何 alpha**（红线：提交需用户明确确认；且 prod 0.78 未过 0.7 提交线）。
- 若段4 仍 prod≥0.7 ⇒ 本集按 **信息源级 prod 墙** 收口（PROVISIONAL），与 sent_matrix 同族结论并入经验库。

## 7. 段4 prod 定向结果：8 臂全灭 ⇒ prod 墙是信息源级（2026-11-20）

| 降 prod 手段 | alpha | S | F | 2Y | 判定 |
|---|---|---:|---:|---:|---|
| 原型对照（复跑 78YoLMK1） | 78YoLMK1 | 1.71 | 1.01 | 2.13 | 对照一致 ✓（平台复现确定性） |
| 轴间差分：profitability − assetutilization | 6XMAGOaL | −0.33 | −0.08 | 0.44 | 信号被毁 |
| 轴间差分：profitability − cashflow | QP0YWXnW | 0.45 | 0.12 | 0.79 | 信号被毁 |
| 轴间差分：profitability − leverage | qM7E5qnP | 1.21 | 0.59 | 2.03 | 唯一存活但 S 不足 |
| 缺失模式 `ts_count_nans` | ZYamXGrY | 0.40 | 0.13 | 1.40 | 信号弱 |
| 事件时点 `ts_arg_max` | pwavWO86 | −0.81 | −0.33 | −2.18 | 反向 |
| 节段差 answer − question | E5QVmJkL | 0.13 | 0.02 | 0.28 | 信号弱 + TO 60% |
| 负语调计数 | 0mPjGv8k | −0.44 | −0.13 | −0.87 | 反向 |

**结论：四种降 prod 手段（轴间正交/缺失模式/事件时点/节段差）全部破坏信号** ⇒ prod 0.78 是**信息源级墙**，
与论坛共识一致（post 44678103399575：「调窗口/权重/中性化造不出低 prod，只有换数据源或换经济逻辑」），
也与同集 sent_matrix 先例（prod 0.87–0.92）同源。**「电话会语调 → 收益」是生产池已饱和的经典因子。**

## 8. 最终判定

| 维度 | 结论 |
|---|---|
| 平台闸 | **3 颗全绿**（78YoLMK1 / rK7dR823 / MP60YVGk，failed_ra_count=0，checks.fail 空） |
| self 相关 | 0.357 PASS（内部严线 0.50 亦过） |
| prod 相关 | **0.7815 / 0.7926 超 0.7 提交线**，且降 prod 手段全部失败 ⇒ 不可提交 |
| 机制层 | **本集 ATOM 形态空间已穷尽**（无门控 / 窄门控 / 宽门控 / group_backfill / 长窗 / 轴 / 节段 / 差分 / 缺失模式 共 66 臂） |
| 塔位 | OTHER 已点亮；本集表达式为纯 ATOM（合规例外条款） |
| **判定** | **PROVISIONAL：平台闸全绿但 prod 墙不可交付**。归档为方法论资产（事件门控 + CW 解法 + 长窗杠杆），不提交。 |

**遗留可走路径**（按用户 2026-11-20 指令「已点亮塔除非 ATOM 和作辅助腿组 regular alpha」）：
OTHER 类可与其它 category 组腿（跨类配额 1/5），但 ATOM 已穷尽前不启动；且组腿须走 gating/grouping/residual/ratio 四形态，
禁等权 add 混腿。需用户确认是否消耗跨类配额。
