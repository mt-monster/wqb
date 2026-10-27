# stock_alpha_model — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `stock_alpha_model` |
| 名称 | Global Stock Selection Alpha Model |
| 类别 | MODEL |
| 数据字段数(平台) | 9 |
| 覆盖率 | 0.5545 |
| 平台已有 alpha | 56 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily scores and factor exposures for a comprehensive global stock-selection model, leveraging advanced machine learning techniques such as elastic net regression and proprietary boosting algorithms. It incorporates a wide array of quantitative signals, including value, growth, quality, momentum, analyst sentiment, and alternative data, while dynamically adjusting for crowding risks and market conditions. The model is fitted on large-cap stocks across major regions and is designed to maximize risk-adjusted returns and minimize drawdowns. Investors and analysts can use these predictive scores and factor insights to enhance portfolio construction, identify outperforming stocks, and improve timing of investment decisions, making it a valuable tool for forecasting price m

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **9** |
| 类型分布 | VECTOR×9 |
| 平均覆盖率 | **0.554** |
| 覆盖率区间 | 0.55 ~ 0.55 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 9 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 9 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 9 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 5 | 0.55 | aggregated_model_score、alternative_data_factor_score、growth_factor_score |
| 盈利与财务 | 2 | 0.55 | machine_learning_factor_score、public_equity_market_value |
| 修正与预期 | 1 | 0.55 | analyst_opinion_factor_score |
| 价量与波动 | 1 | 0.55 | momentum_reversal_factor_score |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `aggregated_model_score` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Final aggregated LEAP composite score |
| 2 | `alternative_data_factor_score` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Contribution of Alternative data style factors to the LEAP composite score |
| 3 | `analyst_opinion_factor_score` | VECTOR | 0.554 | 修正与预期 | 0 | — | — | — | UNUSABLE | Contribution of Analyst Sentiment style to the LEAP composite score |
| 4 | `growth_factor_score` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Contribution of Growth style factors to the LEAP composite score |
| 5 | `machine_learning_factor_score` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Machine-learning based sleeve score contribution |
| 6 | `momentum_reversal_factor_score` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Contribution of Price Momentum and Reversal style factors to the LEAP composite score |
| 7 | `public_equity_market_value` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Market capitalization of the company at the score date |
| 8 | `quality_factor_score` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Contribution of Quality style factors to the LEAP composite score |
| 9 | `valuation_factor_score` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Contribution of Value style factors to the LEAP composite score |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

