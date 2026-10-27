# model16 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model16` |
| 名称 | Fundamental Scores |
| 类别 | MODEL |
| 数据字段数(平台) | 24 |
| 覆盖率 | 0.635 |
| 平台已有 alpha | 36 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Reuters Instrument Codes (RIC), facilitating cross-referencing of securities across two major financial data platforms. By enabling seamless integration of data from Bloomberg and Refinitiv, it helps analysts and portfolio managers ensure accurate security identification, streamline data aggregation, and reduce errors in multi-source research workflows. While not directly predictive of price movements, this mapping is essential for robust data management, enabling more reliable analysis and backtesting when combining datasets that use different security identifiers.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **24** |
| 类型分布 | MATRIX×24 |
| 平均覆盖率 | **0.635** |
| 覆盖率区间 | 0.45 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 8 | 33.3% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 16 | 66.7% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 16 | 66.7% |
| UNTESTED | 8 | 33.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 8 / UNUSABLE 16 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 9 | 0.63 | growth_potential_rank_derivative、multi_factor_acceleration_score_derivative、multi_factor_static_score_derivative |
| 盈利与财务 | 8 | 0.59 | cashflow_efficiency_rank_derivative、earnings_certainty_rank_derivative、fscore_bfl_quality |
| 修正与预期 | 4 | 0.73 | analyst_revision_rank_derivative、composite_factor_score_derivative、fscore_bfl_momentum |
| 价量与波动 | 3 | 0.64 | relative_valuation_rank_derivative、fscore_bfl_value、fscore_value |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `analyst_revision_rank_derivative` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Daily-indicator variant of momentum capturing recent price moves and analyst estimate revisions |
| 2 | `cashflow_efficiency_rank_derivative` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ranks stocks by their ability to generate cash flows and operational profitability |
| 3 | `composite_factor_score_derivative` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Momentum score based on analyst revisions; intraday variant |
| 4 | `earnings_certainty_rank_derivative` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Measures the sustainability and certainty of earnings quality |
| 5 | `growth_potential_rank_derivative` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite growth score qualifying the stock’s expected medium‑term growth potential |
| 6 | `multi_factor_acceleration_score_derivative` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the acceleration of multi-factor score compared to previous period. |
| 7 | `multi_factor_static_score_derivative` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in static multi-factor score compared to previous period. |
| 8 | `relative_valuation_rank_derivative` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assesses whether the stock is under or overpriced based on standard valuation multiples indicator variant |
| 9 | `fscore_bfl_quality` | MATRIX | 0.457 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite measuring earnings quality, stability, and balance-sheet resilience |
| 10 | `fscore_bfl_value` | MATRIX | 0.457 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation composite indicating how under- or overpriced a stock is versus common valuation measures; higher is better (c |
| 11 | `fscore_bfl_growth` | MATRIX | 0.456 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Growth composite estimating expected medium-term growth potential (e.g., revenues, earnings); higher is better (0–100) |
| 12 | `fscore_bfl_momentum` | MATRIX | 0.456 | 修正与预期 | 0 | — | — | — | UNUSABLE | Composite momentum measure reflecting recent price dynamics and analyst estimate revisions to identify improving or dete |
| 13 | `fscore_bfl_profitability` | MATRIX | 0.455 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Profitability composite ranking firms by ability to generate cash flows and operational efficiency; higher is better (0– |
| 14 | `fscore_bfl_surface` | MATRIX | 0.454 | 风险与质量 | 0 | — | — | — | UNUSABLE | Static composite “style surface” score aggregating the five primary style scores; larger surface implies higher rank |
| 15 | `fscore_quality` | MATRIX | 0.453 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite measuring the sustainability and certainty of earnings |
| 16 | `fscore_value` | MATRIX | 0.453 | 价量与波动 | 0 | — | — | — | UNUSABLE | Composite assessing whether the stock is under- or overpriced using standard valuation measures (e.g., multiples) |
| 17 | `fscore_growth` | MATRIX | 0.453 | 风险与质量 | 0 | — | — | — | UNUSABLE | Composite measuring the stock’s expected medium-term growth potential |
| 18 | `fscore_momentum` | MATRIX | 0.452 | 修正与预期 | 0 | — | — | — | UNUSABLE | Composite momentum metric focused on recent analyst estimate revisions to identify stocks experiencing upward or downwar |
| 19 | `fscore_profitability` | MATRIX | 0.452 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite ranking stocks by their ability to generate cash flows and operational profitability |
| 20 | `fscore_bfl_surface_accel` | MATRIX | 0.450 | 风险与质量 | 0 | — | — | — | UNUSABLE | Acceleration (derivative) of the pentagon surface score relative to the previous month |
| 21 | `fscore_bfl_total` | MATRIX | 0.450 | 风险与质量 | 0 | — | — | — | UNUSABLE | Blended composite M-Score combining the static pentagon surface score and its acceleration into an overarching rating |
| 22 | `fscore_surface` | MATRIX | 0.450 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Static overall “style surface” score combining Value, Growth, Profitability, Momentum, and Quality; larger surface impli |
| 23 | `fscore_surface_accel` | MATRIX | 0.446 | 风险与质量 | 0 | — | — | — | UNUSABLE | Acceleration (derivative) of the pentagon surface score, indicating whether the overall style surface is rising or falli |
| 24 | `fscore_total` | MATRIX | 0.446 | 风险与质量 | 0 | — | — | — | UNUSABLE | Final blended score that combines the static pentagon surface score with its acceleration |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

