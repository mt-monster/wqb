# news_sentiment_nlp — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news_sentiment_nlp` |
| 名称 | News Sentiment Signal Features |
| 类别 | OTHER |
| 数据字段数(平台) | 23 |
| 覆盖率 | 0.9134 |
| 平台已有 alpha | 5 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides granular sentiment and NLP-derived features extracted from individual news stories and financial articles. It includes metrics such as polarity, readability, subjectivity, and various sentiment scores (positive, negative, fear, certainty, uncertainty, financial up/down, hype, volatility) at both story and entity levels. The data is available at intraday, daily, and hourly intervals, covering thousands of securities across major regions. By quantifying the emotional and informational tone of news in real time, these features can help analysts and models anticipate market reactions, identify sentiment-driven price movements, and enhance alpha generation strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **23** |
| 类型分布 | VECTOR×23 |
| 平均覆盖率 | **0.913** |
| 覆盖率区间 | 0.91 ~ 0.91 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 23 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 14 | 60.9% |
| DEAD | 8 | 34.8% |
| DEAD_TURNOVER | 1 | 4.3% |

- 已实测字段：**9** 个（39%），best_sharpe 最高 **0.39**，中位 0.09

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 23 | 0.91 | headline_vader_positive_polarity、headline_textblob_sentiment_score、headline_vader_negative_polarity |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `headline_vader_positive_polarity` | VECTOR | 0.913 | 情绪与新闻 | 1 | 0.39 | — | — | DEAD_TURNOVER | Positive polarity component from VADER for the headline, typically between 0 and 1 |
| 2 | `headline_textblob_sentiment_score` | VECTOR | 0.913 | 情绪与新闻 | 2 | 0.25 | 0.83 | 0.24 | DEAD | TextBlob polarity sentiment score of the headline, approximately from -1 (negative) to 1 (positive) |
| 3 | `headline_vader_negative_polarity` | VECTOR | 0.913 | 情绪与新闻 | 2 | 0.22 | 0.39 | -0.03 | DEAD | Negative polarity component from VADER for the headline, typically between 0 and 1 |
| 4 | `headline_subjectivity_score` | VECTOR | 0.913 | 情绪与新闻 | 2 | 0.10 | 0.81 | 0.24 | DEAD | TextBlob subjectivity score of the headline, from 0 (objective) to 1 (subjective) |
| 5 | `headline_sentence_sentiment_average` | VECTOR | 0.913 | 情绪与新闻 | 2 | 0.09 | -0.28 | -0.22 | DEAD | Mean of the per-sentence sentiment scores within the headline |
| 6 | `headline_sentence_sentiment_maximum` | VECTOR | 0.913 | 情绪与新闻 | 2 | -0.05 | -0.32 | -0.06 | DEAD | Maximum per-sentence sentiment score within the headline, based on the same sentiment metric used for sentence analysis |
| 7 | `headline_unique_word_count` | VECTOR | 0.913 | 情绪与新闻 | 1 | -0.08 | -0.17 | -0.12 | DEAD | Number of unique words in the headline |
| 8 | `headline_sentiwordnet_positive_polarity` | VECTOR | 0.913 | 情绪与新闻 | 1 | -0.23 | 0.39 | -0.12 | DEAD | Positive polarity score from SentiWordNet for the headline text (approximately 0–1) |
| 9 | `headline_flesch_kincaid_score` | VECTOR | 0.913 | 情绪与新闻 | 1 | -0.39 | -0.41 | -0.11 | DEAD | Flesch–Kincaid Grade Level readability score of the headline text |
| 10 | `headline_average_sentence_length` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average number of words per sentence in the headline |
| 11 | `headline_flesch_readability_score` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Flesch Reading Ease score of the headline text |
| 12 | `headline_gunning_fog_index` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Gunning Fog readability index of the headline text |
| 13 | `headline_sentence_sentiment_median` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median of the per-sentence sentiment scores within the headline |
| 14 | `headline_sentence_sentiment_minimum` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum per-sentence sentiment score within the headline |
| 15 | `headline_sentence_sentiment_variance` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Variance of the per-sentence sentiment scores within the headline |
| 16 | `headline_sentiment_vader_score` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | VADER compound sentiment score of the headline text, approximately ranging from -1 (negative) to 1 (positive) |
| 17 | `headline_sentiwordnet_negative_polarity` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Negative polarity score from SentiWordNet for the headline text (approximately 0–1, not necessarily summing to 1 with ot |
| 18 | `headline_sentiwordnet_neutral_polarity` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Neutral polarity score from SentiWordNet for the headline text (approximately 0–1) |
| 19 | `headline_smog_readability_index` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | SMOG readability index of the headline text |
| 20 | `headline_stopword_frequency` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Proportion of stop words among the words in the headline |
| 21 | `headline_total_sentence_count` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of sentences detected in the headline |
| 22 | `headline_vader_neutral_polarity` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Neutral polarity component from VADER for the headline, typically between 0 and 1 |
| 23 | `headline_word_count_total` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of words in the headline |

## 六、本地回测证据

- 本地累计回测 **12** 条；其中 `ra_failed_checks` 为空的 **8** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `xAY8ZlJN` | 0.23 | 0.04 | 0.83 | 0.24 | 0.24 | 0 | 107 | `add(multiply(0.6, rank(vec_avg(headline_textblob_sentiment_score))), multiply(0.4, rank(ve` |
| `kqVoG5PP` | 0.22 | 0.04 | -0.01 | — | 0.31 | ["LOW_SHARPE | s2_news_sentiment_nlp_d1 | `ts_zscore(subtract(vec_avg(headline_vader_negative_polarity), vec_avg(headline_vader_posit` |
| `xAY8ZlJW` | 0.19 | 0.03 | 0.39 | -0.03 | 0.30 | 0 | 107 | `add(multiply(0.5, ts_zscore(subtract(vec_avg(headline_vader_negative_polarity), vec_avg(he` |
| `KPOd1vKl` | 0.10 | 0.01 | 0.81 | 0.24 | 0.26 | 0 | 107 | `rank(add(multiply(0.6, vec_avg(headline_subjectivity_score)), multiply(0.4, abs(vec_avg(he` |
| `WjPQ5Y5x` | 0.09 | 0.02 | -0.28 | -0.22 | 0.25 | 0 | 107 | `ts_quantile(subtract(vec_avg(headline_sentence_sentiment_average), vec_avg(headline_senten` |
| `883jJqpq` | 0.09 | 0.02 | -0.28 | — | 0.25 | ["LOW_SHARPE | s2_news_sentiment_nlp_d1 | `ts_quantile(subtract(vec_avg(headline_sentence_sentiment_average), vec_avg(headline_senten` |
| `pwPrLW9X` | -0.05 | 0.00 | -0.32 | -0.06 | 0.17 | 0 | 107 | `ts_zscore(ts_av_diff(ts_backfill(vec_avg(headline_sentence_sentiment_maximum), 66), 22), 2` |
| `akLbz31R` | -0.05 | 0.00 | -0.32 | — | 0.17 | ["LOW_SHARPE | s2_news_sentiment_nlp_d1 | `ts_zscore(ts_av_diff(ts_backfill(vec_avg(headline_sentence_sentiment_maximum), 66), 22), 2` |
| `d5OVG9Gx` | -0.08 | -0.01 | -0.17 | -0.12 | 0.27 | 0 | 107 | `rank(divide(vec_avg(headline_unique_word_count), vec_avg(headline_word_count_total)))` |
| `RRVbzLmg` | -0.21 | -0.04 | 0.81 | — | 0.25 | ["LOW_SHARPE | s2_news_sentiment_nlp_d1 | `winsorize(multiply(vec_avg(headline_subjectivity_score), abs(vec_avg(headline_textblob_sen` |
| `XgWQ0Vjl` | -0.23 | -0.04 | 0.39 | -0.12 | 0.26 | 0 | 107 | `rank(add(multiply(0.5, rank(vec_avg(headline_sentiwordnet_positive_polarity))), multiply(0` |
| `mLgRvdP6` | -0.39 | -0.09 | -0.41 | -0.11 | 0.15 | 0 | 107 | `rank(add(multiply(0.4, reverse(ts_av_diff(ts_backfill(vec_avg(headline_flesch_kincaid_scor` |

## 七、判死记录（sealed dead_end）

- `EUR-NSNLP-SPARSE-TWO-WALLS`（None）family=None：{"dataset": "news_sentiment_nlp", "evidence": "wave133 5 条全灭：turnover 1.23-1.38 全超 0.70 硬闸 + CW 全 FAIL。稀疏事件流两堆墙（CW+turnover）在 EUR D1 无可避免。情绪×强度族（textblob×word_count/vader/subjectivity）在标准设置（SUBINDUSTRY/decay4）下无法复现 wave107 的存活线索。", "reason": "news_sentiment_nlp 情绪×强度族在 EUR D1 判死：稀疏事件流导致 CW+turnover 双墙，信号强度不足（Sharpe -0.18~0.32）", "region": "EUR", "rule": "Leave news_sentiment_nlp 全部字段族在 EUR。稀疏事件流的 
- `EUR-news_sentiment_nlp-STRUCTURE-DEAD`（2026-09-03）family=news_sentiment_structure：{"category": "Other", "dataset": "news_sentiment_nlp", "evidence": "wave107 首探 8/8 FAIL; 词汇丰富度 -0.08、avg-median 分歧 0.09、max 极值加速 -0.05、复杂度反转+情绪加速 -0.39、sentiwordnet 极性强度 -0.23 全灭（2Y ≤0）", "not_dead": "情绪×强度/流量组合腿 2Y 0.83/0.81 存活线索: xAY8ZlJN textblob×word_count 与 KPOd1vKl subjectivity×abs(textblob); turnover 0.24-0.30 需 decay/窗口收敛; 留 Mode A 收敛候选", "pattern": "可读性/复杂度/句级结构类字段（flesch/gunning/unique_w
- `EUR-news_sentiment_dl-SENTIMENT-WEAK`（2026-09-04）family=news_sentiment_dl sentiment word stats：{"best_2y": 1.36, "best_alpha": "zqY1knoO", "best_fitness": 0.04, "best_sharpe": 0.21, "dataset": "news_sentiment_dl", "evidence": "wave114 9 条全灭：情绪词统计（mean/max/min positive/negative sentiment）在 EUR TOP2500 整体弱信号，最强 S0.38/F0.07/2Y0.63 远低于 Mode B 线；text_complexity 交互项全负；ts_std_dev/ts_delta 快腿全负", "id": "EUR-news_sentiment_dl-SENTIMENT-WEAK", "reason": "news_sentiment_dl 情绪词统计与文本复杂度在 EUR D1 无正向预测力；p
- `EUR-NONMODEL-TOWER-CEILING`（2026-09-11）family=non_model_tower_sparse_event_sentiment_analyst：{"datasets": [{"dataset": "news54", "max_sharpe": 0.4, "reason": "mws54_factor semi-annual+单边恒正+稀疏", "tower": "news"}, {"dataset": "news_sentiment_nlp", "max_sharpe": 0.39, "reason": "情绪信号弱,净极性turnover1.24高超手", "tower": "other"}, {"dataset": "analyst45", "max_sharpe": 0.32, "reason": "分析师想法表现弱,zscore/delta turnover1.5+", "tower": "analyst"}], "evidence": "三塔回测全灭,S0 calibrate预警与实测完全一致(news0.50→0.40

