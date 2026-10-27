# ai_news_scores — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `ai_news_scores` |
| 名称 | AI News Sentiment Scores |
| 类别 | OTHER |
| 数据字段数(平台) | 105 |
| 覆盖率 | 0.7924 |
| 平台已有 alpha | 12 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily sentiment scores for global equities by analyzing news articles, press releases, and regulatory disclosures using a proprietary transformer-based natural language processing model. Covering thousands of companies across major regions, it quantifies the tone and relevance of news events, offering granular sentiment metrics at both the entity and event level. By systematically capturing shifts in market sentiment and event novelty, the dataset enables researchers and investors to identify potential price-moving signals, enhance alpha generation, and improve risk management. Its comprehensive coverage and advanced scoring methodology make it a valuable resource for predicting short-term and medium-term asset returns based on news-driven market dynamics.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **105** |
| 类型分布 | MATRIX×105 |
| 平均覆盖率 | **0.792** |
| 覆盖率区间 | 0.79 ~ 0.79 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 105 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 100 | 95.2% |
| DEAD | 5 | 4.8% |

- 已实测字段：**5** 个（5%），best_sharpe 最高 **0.27**，中位 -0.24

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 104 | 0.79 | positive_score_average_value_3、positive_score_median_value_3、negative_score_maximum_value_3 |
| 修正与预期 | 1 | 0.79 | negative_sentiment_upper_estimate_2 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `positive_score_average_value_3` | MATRIX | 0.792 | 情绪与新闻 | 2 | 0.27 | 0.72 | 0.31 | DEAD | Per-stock daily mean positive sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalized 0 |
| 2 | `positive_score_median_value_3` | MATRIX | 0.792 | 情绪与新闻 | 1 | 0.02 | 0.02 | 0.05 | DEAD | Per-stock daily median of positive sentiment scores from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normal |
| 3 | `negative_score_maximum_value_3` | MATRIX | 0.792 | 情绪与新闻 | 2 | -0.24 | 1.00 | 0.01 | DEAD | Per-stock daily maximum negative sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalize |
| 4 | `negative_score_confidence_upper_bound_3` | MATRIX | 0.792 | 情绪与新闻 | 1 | -0.34 | -0.92 | -0.09 | DEAD | Per-stock daily 95% confidence upper bound for negative sentiment mean from RavenPack press releases for EUR, model variant prv23, same-day  |
| 5 | `negative_score_median_value_3` | MATRIX | 0.792 | 情绪与新闻 | 1 | -0.68 | -1.17 | -0.31 | DEAD | Per-stock daily median of negative sentiment scores from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normal |
| 6 | `negative_score_average_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean negative sentiment score across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 7 | `negative_score_average_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean negative sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 8 | `negative_score_average_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily mean negative sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalized 0 |
| 9 | `negative_score_average_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean negative sentiment score for ASI, series variant prv22, D0; average of per-event negative scores for the stock-day (0–1 scale) |
| 10 | `negative_score_average_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean negative sentiment score for USA, series variant prv25, D0 (same-day) offset |
| 11 | `negative_score_confidence_lower_bound` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean negative sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 12 | `negative_score_confidence_lower_bound_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean negative sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 13 | `negative_score_confidence_lower_bound_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily 95% confidence lower bound for negative sentiment mean from RavenPack press releases for EUR, model variant prv23, same-day  |
| 14 | `negative_score_confidence_lower_bound_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean negative sentiment score for ASI, variant prv22, D0 on the stock-day |
| 15 | `negative_score_confidence_lower_bound_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the negative sentiment score for USA, series variant prv25, D0 offset |
| 16 | `negative_score_confidence_upper_bound` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean negative sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 17 | `negative_score_confidence_upper_bound_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean negative sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 18 | `negative_score_confidence_upper_bound_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean negative sentiment score for ASI, variant prv22, D0 on the stock-day |
| 19 | `negative_score_maximum_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum negative sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 20 | `negative_score_maximum_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum negative sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 21 | `negative_score_maximum_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum negative sentiment score observed for ASI, variant prv22, D0 on the stock-day |
| 22 | `negative_score_median_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median negative sentiment score across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 23 | `negative_score_median_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median negative sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 24 | `negative_score_median_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median negative sentiment score for ASI, series variant prv22, D0; median of per-event negative scores for the stock-day (0–1 scale) |
| 25 | `negative_score_median_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median negative sentiment score for USA, series variant prv25, D0 (same-day) offset |
| 26 | `negative_score_minimum_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum negative sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 27 | `negative_score_minimum_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum negative sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 28 | `negative_score_minimum_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily minimum negative sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalize |
| 29 | `negative_score_minimum_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum negative sentiment score observed for ASI, variant prv22, D0 on the stock-day |
| 30 | `negative_score_standard_deviation` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 31 | `negative_score_standard_deviation_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores for ASI, variant prv2, D1 (per-stock daily) |
| 32 | `negative_score_standard_deviation_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily standard deviation of negative sentiment scores from RavenPack press releases for EUR, model variant prv23, same-day (D0) |
| 33 | `negative_score_standard_deviation_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores for ASI, variant prv22, D0; dispersion of per-event negative scores for the stock-day |
| 34 | `negative_sentiment_dispersion_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of negative sentiment scores for USA, series variant prv25, D0 offset |
| 35 | `negative_sentiment_lowest_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum negative sentiment score for USA, series variant prv25, D0 offset |
| 36 | `negative_sentiment_peak_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum negative sentiment score for USA, series variant prv25, D0 offset |
| 37 | `negative_sentiment_upper_estimate_2` | MATRIX | 0.792 | 修正与预期 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the negative sentiment score for USA, series variant prv25, D0 offset |
| 38 | `neutral_score_average_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean neutral sentiment score across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 39 | `neutral_score_average_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean neutral sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 40 | `neutral_score_average_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily mean neutral sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalized 0– |
| 41 | `neutral_score_average_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean neutral sentiment score for ASI, series variant prv22, D0; average of per-event neutral scores for the stock-day (0–1 scale) |
| 42 | `neutral_score_average_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean neutral sentiment score for USA, series variant prv25, D0 (same-day) offset |
| 43 | `neutral_score_confidence_lower_bound` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean neutral sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 44 | `neutral_score_confidence_lower_bound_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean neutral sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 45 | `neutral_score_confidence_lower_bound_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily 95% confidence lower bound for neutral sentiment mean from RavenPack press releases for EUR, model variant prv23, same-day ( |
| 46 | `neutral_score_confidence_lower_bound_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean neutral sentiment score for ASI, variant prv22, D0 on the stock-day |
| 47 | `neutral_score_confidence_lower_bound_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the neutral sentiment score for USA, series variant prv25, D0 offset |
| 48 | `neutral_score_confidence_upper_bound` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean neutral sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 49 | `neutral_score_confidence_upper_bound_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean neutral sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 50 | `neutral_score_confidence_upper_bound_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily 95% confidence upper bound for neutral sentiment mean from RavenPack press releases for EUR, model variant prv23, same-day ( |
| 51 | `neutral_score_confidence_upper_bound_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean neutral sentiment score for ASI, variant prv22, D0 on the stock-day |
| 52 | `neutral_score_confidence_upper_bound_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the neutral sentiment score for USA, series variant prv25, D0 offset |
| 53 | `neutral_score_maximum_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum neutral sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 54 | `neutral_score_maximum_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum neutral sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 55 | `neutral_score_maximum_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily maximum neutral sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalized |
| 56 | `neutral_score_maximum_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum neutral sentiment score observed for ASI, variant prv22, D0 on the stock-day |
| 57 | `neutral_score_maximum_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum neutral sentiment score for USA, series variant prv25, D0 offset |
| 58 | `neutral_score_median_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median neutral sentiment score across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 59 | `neutral_score_median_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median neutral sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 60 | `neutral_score_median_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily median of neutral sentiment scores from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normali |
| 61 | `neutral_score_median_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median neutral sentiment score for ASI, series variant prv22, D0 (same-day); median of per-event neutral scores for the stock-day (0–1 scale |
| 62 | `neutral_score_median_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median neutral sentiment score for USA, series variant prv25, D0 (same-day) offset |
| 63 | `neutral_score_minimum_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum neutral sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 64 | `neutral_score_minimum_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum neutral sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 65 | `neutral_score_minimum_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily minimum neutral sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalized |
| 66 | `neutral_score_minimum_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum neutral sentiment score observed for ASI, variant prv22, D0 on the stock-day |
| 67 | `neutral_score_minimum_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum neutral sentiment score for USA, series variant prv25, D0 offset |
| 68 | `neutral_score_standard_deviation` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 69 | `neutral_score_standard_deviation_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores for ASI, variant prv2, D1 (per-stock daily) |
| 70 | `neutral_score_standard_deviation_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily standard deviation of neutral sentiment scores from RavenPack press releases for EUR, model variant prv23, same-day (D0) |
| 71 | `neutral_score_standard_deviation_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores for ASI, variant prv22, D0; dispersion of per-event neutral scores for the stock-day |
| 72 | `neutral_sentiment_dispersion_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of neutral sentiment scores for USA, series variant prv25, D0 offset |
| 73 | `positive_score_average_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean positive sentiment score across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 74 | `positive_score_average_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean positive sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 75 | `positive_score_average_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean positive sentiment score for ASI, series variant prv22, D0; average of per-event positive scores for the stock-day (0–1 scale) |
| 76 | `positive_score_average_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean positive sentiment score for USA, series variant prv25, D0 (same-day) offset |
| 77 | `positive_score_confidence_lower_bound` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean positive sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 78 | `positive_score_confidence_lower_bound_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean positive sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 79 | `positive_score_confidence_lower_bound_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily 95% confidence lower bound for positive sentiment mean from RavenPack press releases for EUR, model variant prv23, same-day  |
| 80 | `positive_score_confidence_lower_bound_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the mean positive sentiment score for ASI, variant prv22, D0 on the stock-day |
| 81 | `positive_score_confidence_lower_bound_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lower 95% confidence bound for the positive sentiment score for USA, series variant prv25, D0 offset |
| 82 | `positive_score_confidence_upper_bound` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean positive sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 83 | `positive_score_confidence_upper_bound_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean positive sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 84 | `positive_score_confidence_upper_bound_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily 95% confidence upper bound for positive sentiment mean from RavenPack press releases for EUR, model variant prv23, same-day  |
| 85 | `positive_score_confidence_upper_bound_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the mean positive sentiment score for ASI, variant prv22, D0 on the stock-day |
| 86 | `positive_score_confidence_upper_bound_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Upper 95% confidence bound for the positive sentiment score for USA, series variant prv25, D0 offset |
| 87 | `positive_score_maximum_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum positive sentiment score for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 88 | `positive_score_maximum_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum positive sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 89 | `positive_score_maximum_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily maximum positive sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalize |
| 90 | `positive_score_maximum_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum positive sentiment score observed for ASI, variant prv22, D0 on the stock-day |
| 91 | `positive_score_maximum_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum positive sentiment score for USA, series variant prv25, D0 offset |
| 92 | `positive_score_median_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median positive sentiment score across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 93 | `positive_score_median_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median positive sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 94 | `positive_score_median_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median positive sentiment score for ASI, series variant prv22, D0; median of per-event positive scores for the stock-day (0–1 scale) |
| 95 | `positive_score_median_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median positive sentiment score for USA, series variant prv25, D0 (same-day) offset |
| 96 | `positive_score_minimum_value` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum positive sentiment score for a stock on a given day in USA (variant prv24, same-day D0), from RavenPack PR events scored 0–1 by the  |
| 97 | `positive_score_minimum_value_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum positive sentiment score for ASI, variant prv2, D1 (per-stock daily; scores in [0,1]) |
| 98 | `positive_score_minimum_value_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily minimum positive sentiment score from RavenPack press releases for EUR, model variant prv23, same-day (D0); scores normalize |
| 99 | `positive_score_minimum_value_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum positive sentiment score observed for ASI, variant prv22, D0 on the stock-day |
| 100 | `positive_score_minimum_value_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum positive sentiment score for USA, series variant prv25, D0 offset |
| 101 | `positive_score_standard_deviation` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores across events for a stock-day in USA (variant prv24, D0), scores in 0–1 |
| 102 | `positive_score_standard_deviation_2` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores for ASI, variant prv2, D1 (per-stock daily) |
| 103 | `positive_score_standard_deviation_3` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-stock daily standard deviation of positive sentiment scores from RavenPack press releases for EUR, model variant prv23, same-day (D0) |
| 104 | `positive_score_standard_deviation_4` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores for ASI, variant prv22, D0; dispersion of per-event positive scores for the stock-day |
| 105 | `positive_score_standard_deviation_5` | MATRIX | 0.792 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of positive sentiment scores for USA, series variant prv25, D0 offset |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `JjxZjGwE` | 0.27 | 0.07 | 0.72 | 0.31 | 0.06 | ["LOW_SHARPE | 108 | `rank(add(multiply(0.6, rank(ts_mean(ts_backfill(positive_score_average_value_3, 66), 22)))` |
| `blR5lQkN` | 0.02 | 0.00 | 0.02 | 0.05 | 0.04 | ["LOW_SHARPE | 108 | `rank(add(multiply(0.5, rank(ts_mean(ts_backfill(positive_score_median_value_3, 66), 22))),` |
| `d5OA5ZpK` | -0.24 | -0.04 | 1.00 | -0.08 | 0.17 | ["LOW_SHARPE | 108 | `trade_when(ts_sum(ts_backfill(negative_score_maximum_value_3, 5), 5) > 0, rank(reverse(ts_` |
| `9qVLqpvd` | -0.29 | -0.06 | 0.66 | 0.02 | 0.17 | ["LOW_SHARPE | 108 | `ts_zscore(rank(reverse(days_from_last_change(ts_backfill(positive_score_minimum_value_3, 3` |
| `qMWoMN8Z` | -0.34 | -0.09 | -0.92 | -0.09 | 0.08 | ["LOW_SHARPE | 108 | `rank(reverse(subtract(ts_mean(ts_backfill(negative_score_confidence_upper_bound_3, 33), 5)` |
| `d5OA5ZpE` | -0.37 | -0.09 | -0.57 | 0.01 | 0.19 | ["LOW_SHARPE | 108 | `rank(subtract(ts_zscore(ts_backfill(negative_score_maximum_value_3, 22), 10), ts_zscore(ts` |
| `Vk6gkGVb` | -0.54 | -0.15 | -2.63 | -0.67 | 0.20 | ["LOW_SHARPE | 108 | `ts_zscore(subtract(ts_av_diff(ts_backfill(positive_score_average_value_3, 66), 5), ts_av_d` |
| `A10M1GWl` | -0.68 | -0.23 | -1.17 | -0.31 | 0.06 | ["LOW_SHARPE | 108 | `rank(add(multiply(0.5, reverse(rank(ts_mean(ts_backfill(negative_score_median_value_3, 66)` |

## 七、判死记录（sealed dead_end）

- `EUR-AINEWS-POS-INTENSITY-WEAK`（None）family=None：{"dataset": "ai_news_scores", "evidence": "wave134 7 条全灭：pos 水平×强度族（pos_max-pos_avg/pos_max-pos_median/pos_avg-neg_std）Sharpe -0.55~0.35 全远低于 1.58。EUR 专用字段（_3 后缀）RavenPack 新闻情绪在 EUR D1 无预测力。wave108 的存活线索（JjxZjGwE 2Y 0.72）无法复现。", "reason": "ai_news_scores pos 水平×强度族在 EUR D1 判死：信号极弱，wave108 存活线索无法复现", "region": "EUR", "rule": "Leave ai_news_scores 全部字段族在 EUR。新闻情绪类信号在 EUR D1 普遍无预测力。", "wave": 134}
- `EUR-ai_news_scores-ADVANCED-NEG`（2026-09-03）family=ai_news_scores advanced stats：{"category": "Other", "dataset": "ai_news_scores", "evidence": "wave108 首探 8/8 FAIL；CI 带宽精度 -0.34、恐慌尖峰反转 -0.37(CW 0.356 集中)、共识漂移 -0.54(2Y -2.63) 3/3 全负；ts_max_diff×median 契约双槽 +0.02/-0.68；neg 方向族 IS 全负（B 槽 trade_when 2Y+1.00 例外）", "not_dead": "pos 水平×强度加权 JjxZjGwE(0.6×ts_mean avg66 + 0.4×ts_mean max5) IS+0.27/2Y+0.72/subU+0.31/TVR 0.059 唯一全维正，已 salvage → 与 wave107 xAY8ZlJN(2Y 0.83) 形成跨数据集复现线索：pos 

