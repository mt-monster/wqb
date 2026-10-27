# other335 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other335` |
| 名称 | Multi-Region Dividend Alpha Model Dataset |
| 类别 | OTHER |
| 数据字段数(平台) | 10 |
| 覆盖率 | 0.5589 |
| 平台已有 alpha | 2211 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset contains the outputs and components of a machine learning-based global stock selection model focused on dividend-paying equities. Leveraging a large factor library and advanced algorithms, it generates composite scores that reflect the expected performance and risk profile of stocks, with specialized sub-models for linear, hedge, and defensive scenarios. The model incorporates contextual information, risk management, and signal persistence metrics, making it highly effective for constructing portfolios that seek stable income and downside protection. By providing predictive signals and risk-adjusted rankings, this dataset is valuable for forecasting price movements, optimizing portfolio returns, and managing risk in dividend-oriented investment strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **10** |
| 类型分布 | MATRIX×10 |
| 平均覆盖率 | **0.559** |
| 覆盖率区间 | 0.43 ~ 0.68 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 5 | 50.0% |
| 稀疏 (<0.50) | 5 | 50.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 5 | 50.0% |
| UNUSABLE | 5 | 50.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 5 / UNUSABLE 5 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 9 | 0.55 | oth335_combined_all_region_hedge、oth335_combined_all_region_linear、oth335_combined_all_region_mktcap |
| 盈利与财务 | 1 | 0.68 | oth335_combined_all_region_mind |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth335_combined_all_region_hedge` | MATRIX | 0.684 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score from the hedge model component |
| 2 | `oth335_combined_all_region_linear` | MATRIX | 0.684 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score from the linear model component |
| 3 | `oth335_combined_all_region_mind` | MATRIX | 0.684 | 盈利与财务 | 0 | — | — | — | UNTESTED | Final composite Wolfe MIND dividend/income score (daily, point-in-time) |
| 4 | `oth335_combined_all_region_mktcap` | MATRIX | 0.684 | 宏观与行业 | 0 | — | — | — | UNTESTED | Market capitalization in USD |
| 5 | `oth335_combined_all_region_shield` | MATRIX | 0.684 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score from the SHIELD (defensive) model |
| 6 | `oth335_hc_combined_all_region_hedge` | MATRIX | 0.434 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Hedge model score (daily point-in-time) |
| 7 | `oth335_hc_combined_all_region_linear` | MATRIX | 0.434 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Linear model score (daily point-in-time) |
| 8 | `oth335_hc_combined_all_region_mind` | MATRIX | 0.434 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Final composite MIND score (daily point-in-time) |
| 9 | `oth335_hc_combined_all_region_mktcap` | MATRIX | 0.434 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Market capitalization in USD |
| 10 | `oth335_hc_combined_all_region_shield` | MATRIX | 0.434 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Defensive SHIELD model score (daily point-in-time) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

