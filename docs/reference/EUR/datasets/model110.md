# model110 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model110` |
| 名称 | Big data and machine learning based model |
| 类别 | MODEL |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.8525 |
| 平台已有 alpha | 462 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive, daily-updated global stock selection model that combines fundamental, alternative, and machine learning-based factors to generate predictive signals for over 11,000 stocks across approximately 45 countries. It includes style factors such as value, growth, quality, price momentum and reversal, analyst sentiment, and alternative data, as well as composite and tree-based model scores. The model is industry-neutralized and regularly refitted to adapt to changing market conditions. By aggregating diverse quantitative signals and leveraging advanced machine learning techniques, this dataset enables systematic investors to identify stocks with high expected returns, manage risk, and time factor exposures, making it a powerful tool for predicting price moveme

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | MATRIX×8 |
| 平均覆盖率 | **0.853** |
| 覆盖率区间 | 0.85 ~ 0.85 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 8 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 8 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 3 | 0.85 | mdl110_price_momentum_reversal、mdl110_score、mdl110_value |
| 修正与预期 | 2 | 0.85 | mdl110_analyst_sentiment、mdl110_growth |
| 盈利与财务 | 2 | 0.85 | mdl110_quality、mdl110_tree |
| 宏观与行业 | 1 | 0.85 | mdl110_alternative |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl110_alternative` | MATRIX | 0.853 | 宏观与行业 | 0 | — | — | — | UNTESTED | Composite alpha signal generated from non-traditional sources such as alternative data, big data, and unstructured information |
| 2 | `mdl110_analyst_sentiment` | MATRIX | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Aggregate sentiment score derived from analyst ratings, estimate revisions, and market sentiment factors |
| 3 | `mdl110_growth` | MATRIX | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Composite growth factor derived from forward-looking estimates and backward-looking financials, representing robust sales and earnings growt |
| 4 | `mdl110_price_momentum_reversal` | MATRIX | 0.853 | 价量与波动 | 0 | — | — | — | UNTESTED | A score indicating the influence of recent price momentum and mean-reversion effects on the stock price, capturing both trends and potential |
| 5 | `mdl110_quality` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Composite score measuring company profitability, accounting robustness, earnings quality, and risk-related financial metrics |
| 6 | `mdl110_score` | MATRIX | 0.853 | 价量与波动 | 0 | — | — | — | UNTESTED | The overall alpha signal produced by a weighted combination of all underlying factor scores (sentiment, quality, value, growth, price moment |
| 7 | `mdl110_tree` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | A composite score generated from nonlinear tree-based machine learning models, synthesizing all available individual signals and factors to  |
| 8 | `mdl110_value` | MATRIX | 0.853 | 价量与波动 | 0 | — | — | — | UNTESTED | Composite valuation factor blending multiple price-based and fundamental metrics such as P/E, P/B, and price-to-sales |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

