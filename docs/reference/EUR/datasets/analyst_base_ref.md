# analyst_base_ref — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst_base_ref` |
| 名称 | Analyst Estimates Base Reference |
| 类别 | ANALYST |
| 数据字段数(平台) | 17 |
| 覆盖率 | 0.5523 |
| 平台已有 alpha | 7 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset serves as a placeholder or reference point for the foundational data underlying analyst estimates and key performance indicators, without containing any actual financial or market data itself. Its primary function is to facilitate access to industry classifications and essential metadata required for quantitative research, while avoiding penalization for using common base modules in research workflows. Although it does not provide direct content, it enables seamless integration of industry and company classification information, which is crucial for constructing and interpreting analyst-driven signals and for ensuring consistency in backtesting and model development. By supporting the structural backbone for more detailed analyst and KPI datasets, it indirectly aids in the acc

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **17** |
| 类型分布 | VECTOR×10　MATRIX×7 |
| 平均覆盖率 | **0.552** |
| 覆盖率区间 | 0.32 ~ 0.98 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 6 | 35.3% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 11 | 64.7% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 11 | 64.7% |
| UNTESTED | 6 | 35.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 6 / UNUSABLE 11 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 8 | 0.32 | consensus_high_estimate_annual、consensus_low_estimate_annual、consensus_mean_estimate_annual |
| 其他 | 3 | 0.78 | number_of_issued_shares_d1、number_of_issued_shares、split_adjustment_factor_daily |
| 搜索与替代数据 | 2 | 0.97 | dilution_adjustment_ratio_2、dilution_adjustment_ratio |
| 价量与波动 | 2 | 0.97 | last_close_price_2、last_close_price |
| 盈利与财务 | 1 | 0.32 | actual_category_annual |
| 宏观与行业 | 1 | 0.32 | reported_actual_value_annual |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `dilution_adjustment_ratio_2` | MATRIX | 0.979 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Point-in-time dilution adjustment ratio applied to convert per-share measures to a diluted basis (accounts for potential dilutive securities |
| 2 | `last_close_price_2` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Point-in-time corporate action–adjusted price used for ratios and analytics (not a complete price history) |
| 3 | `number_of_issued_shares_d1` | MATRIX | 0.978 | 其他 | 0 | — | — | — | UNTESTED | Point-in-time shares outstanding for the company with no forward or backfill adjustments |
| 4 | `dilution_adjustment_ratio` | MATRIX | 0.968 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Dilution adjustment factor applied to convert/normalize per-share metrics for the chosen dilution regime |
| 5 | `last_close_price` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Point-in-time corporate-action–adjusted price overlay for the security used in ratios and analytics (not a full historical price series) |
| 6 | `number_of_issued_shares` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Point-in-time shares outstanding for the security, without forward or backfill adjustments |
| 7 | `split_adjustment_factor_daily` | MATRIX | 0.390 | 其他 | 0 | — | — | — | UNUSABLE | Stock split adjustment ratio effective on the split date for the security |
| 8 | `actual_category_annual` | VECTOR | 0.316 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Classification of the annual actual value (e.g., earnings, revenue). |
| 9 | `consensus_high_estimate_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest contributing analyst estimate in the consensus snapshot |
| 10 | `consensus_low_estimate_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest contributing analyst estimate in the consensus snapshot for the metric |
| 11 | `consensus_mean_estimate_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (average) of analyst estimates in the consensus snapshot |
| 12 | `consensus_median_estimate_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates in the consensus snapshot |
| 13 | `consensus_stddev_estimate_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the analyst estimates in the consensus snapshot |
| 14 | `consensus_surprise_percentage_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage difference between consensus estimate and actual value for the annual period. |
| 15 | `consensus_vs_actual_diff_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between the actual value and the consensus (typically actual minus mean), in the same units |
| 16 | `num_estimates_consensus_annual` | VECTOR | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing analyst estimates in the consensus snapshot |
| 17 | `reported_actual_value_annual` | VECTOR | 0.316 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Reported actual figure for the specified metric, in the dataset’s stated units/currency |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

