# model140 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model140` |
| 名称 | Sensitivity to the Inflation Change |
| 类别 | MODEL |
| 数据字段数(平台) | 3 |
| 覆盖率 | 0.5077 |
| 平台已有 alpha | 3 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides stock-level sensitivity estimates to expected inflation, using changes in breakeven rates and advanced machine learning techniques such as elastic net regression. It covers a wide range of global equities and includes sector, country, and performance metrics, allowing users to analyze how individual stocks and sectors respond to inflationary pressures. By quantifying inflation beta and related exposures, the dataset is valuable for portfolio managers and analysts seeking to forecast price movements, manage risk, and implement tactical asset allocation strategies in environments with changing inflation expectations.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **3** |
| 类型分布 | MATRIX×3 |
| 平均覆盖率 | **0.508** |
| 覆盖率区间 | 0.50 ~ 0.52 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 3 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 3 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 3 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 2 | 0.51 | mdl140_qes_sinc_neut、mdl140_qes_sinc_comp |
| 修正与预期 | 1 | 0.50 | mdl140_qes_sinc_sensitivity |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl140_qes_sinc_neut` | MATRIX | 0.518 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Stock-level sensitivity to expected inflation changes, "neutralized" or adjusted to remove the contemporaneous effect of benchmark interest  |
| 2 | `mdl140_qes_sinc_comp` | MATRIX | 0.503 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Composite factor combining both pure inflation sensitivity and interest rate sensitivity into a holistic metric of a stock's macro inflation |
| 3 | `mdl140_qes_sinc_sensitivity` | MATRIX | 0.502 | 修正与预期 | 0 | — | — | — | UNUSABLE | Stock-level estimated “beta” sensitivity to expected inflation, specifically to changes in the 10-year breakeven inflation rate, derived fro |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

