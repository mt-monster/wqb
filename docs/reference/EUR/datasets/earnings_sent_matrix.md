# earnings_sent_matrix — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `earnings_sent_matrix` |
| 名称 | Global Earnings Call Sentiment Matrix |
| 类别 | EARNINGS |
| 数据字段数(平台) | 7 |
| 覆盖率 | 0.5062 |
| 平台已有 alpha | 61 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.2 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a structured, matrix-format aggregation of global company earnings call transcripts, focusing on sentiment and topic analytics. It leverages advanced natural language processing to extract and quantify positive, neutral, and negative sentiment probabilities from management presentations and Q&A sessions, across over 200 thematic topics. The data is filtered and enhanced with smart aggregation techniques, including rolling and daily sentiment measures, confidence scores, and relevance indicators. By capturing nuanced shifts in management tone and analyst reactions, the dataset enables researchers and investors to identify patterns and signals that may precede price movements, offering valuable insights for predictive modeling and alpha generation in equity markets.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **7** |
| 类型分布 | MATRIX×7 |
| 平均覆盖率 | **0.506** |
| 覆盖率区间 | 0.51 ~ 0.51 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 7 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 7 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 7 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 3 | 0.51 | likelihood_of_neutral_tone、negative_sentiment_probability_3、positive_sentiment_probability_3 |
| 情绪与新闻 | 3 | 0.51 | overall_sentiment_score、sentiment_weighting_method1、sentiment_weighting_method2 |
| 交易与微观结构 | 1 | 0.51 | intraday_delay_indicator |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `intraday_delay_indicator` | MATRIX | 0.506 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | A code indicating whether the data is updated intraday or with a delay. |
| 2 | `likelihood_of_neutral_tone` | MATRIX | 0.506 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model-estimated probability [0–1] that the intraday transcript slice has neutral sentiment; sums with the other two probabilities to 1 |
| 3 | `negative_sentiment_probability_3` | MATRIX | 0.506 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model-estimated probability [0–1] that the intraday transcript slice has negative sentiment; designed to sum to 1 with Prob_NTR and Prob_POS |
| 4 | `overall_sentiment_score` | MATRIX | 0.506 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Categorical sentiment label derived by argmax over Prob_POS, Prob_NTR, Prob_NEG; typically -1 negative, 0 neutral, 1 positive |
| 5 | `positive_sentiment_probability_3` | MATRIX | 0.506 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model-estimated probability [0–1] that the intraday transcript slice has positive sentiment; part of the three-class distribution |
| 6 | `sentiment_weighting_method1` | MATRIX | 0.506 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Aggregate transcript tone score computed via method 1; higher values indicate more positive sentiment for the segment |
| 7 | `sentiment_weighting_method2` | MATRIX | 0.506 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Alternative aggregate transcript tone score computed via method 2; higher values indicate more positive sentiment |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

