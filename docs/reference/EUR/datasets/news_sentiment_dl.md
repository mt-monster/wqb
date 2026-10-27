# news_sentiment_dl — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news_sentiment_dl` |
| 名称 | Deep Learning News Sentiment Signals |
| 类别 | OTHER |
| 数据字段数(平台) | 66 |
| 覆盖率 | 0.7558 |
| 平台已有 alpha | 2 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides enhanced sentiment signals derived from financial news and social media text using advanced deep learning techniques. By leveraging a large corpus of news articles and social media posts, the dataset applies multiple language embeddings and a deep neural network trained on millions of samples to classify sentiment related to companies and market events. The output includes sentiment scores and other text-based features, offering a refined view of market mood and reactions. These signals can be used to anticipate price movements by capturing shifts in investor sentiment and market perception, making the dataset valuable for quantitative trading strategies and risk assessment.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **66** |
| 类型分布 | VECTOR×66 |
| 平均覆盖率 | **0.756** |
| 覆盖率区间 | 0.74 ~ 0.77 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 66 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 61 | 92.4% |
| DEAD | 5 | 7.6% |

- 已实测字段：**5** 个（8%），best_sharpe 最高 **0.38**，中位 0.21

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 60 | 0.76 | positive_word_sentiment_entropy_inferess、mean_positive_word_sentiment_inferess、max_negative_word_sentiment_inferess |
| 其他 | 5 | 0.75 | avg_words_per_sentence_trna_enhanced、output_metric_3_trna_enhanced、output_metric_4_trna_enhanced |
| 风险与质量 | 1 | 0.75 | text_complexity_score_trna_enhanced |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `positive_word_sentiment_entropy_inferess` | VECTOR | 0.772 | 情绪与新闻 | 1 | 0.38 | 0.63 | — | DEAD | Entropy of sentiment distribution among positive words in the article. |
| 2 | `mean_positive_word_sentiment_inferess` | VECTOR | 0.772 | 情绪与新闻 | 2 | 0.27 | 0.54 | — | DEAD | Mean sentiment score of all positive words in the article. |
| 3 | `max_negative_word_sentiment_inferess` | VECTOR | 0.772 | 情绪与新闻 | 2 | 0.21 | 1.36 | — | DEAD | Maximum sentiment score among negative words in the article. |
| 4 | `text_complexity_score_inferess` | VECTOR | 0.772 | 情绪与新闻 | 3 | -0.05 | 0.24 | — | DEAD | A score representing the linguistic complexity of the article. |
| 5 | `min_positive_word_sentiment_inferess` | VECTOR | 0.772 | 情绪与新闻 | 1 | -0.24 | -0.55 | — | DEAD | Minimum sentiment score among positive words in the article. |
| 6 | `avg_syllables_per_word_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average number of syllables per word in the article. |
| 7 | `avg_words_per_sentence_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average number of words per sentence in the article. |
| 8 | `max_positive_word_sentiment_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum sentiment score among positive words in the article. |
| 9 | `mean_negative_word_sentiment_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean sentiment score of all negative words in the article. |
| 10 | `min_negative_word_sentiment_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum sentiment score among negative words in the article. |
| 11 | `negative_word_count_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of negative sentiment words identified in the article. |
| 12 | `negative_word_sentiment_entropy_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Entropy of sentiment distribution among negative words in the article. |
| 13 | `negative_word_sentiment_stddev_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of sentiment scores for negative words in the article. |
| 14 | `output_metric_1_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | First custom output metric derived from the article's text analysis. |
| 15 | `output_metric_2_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Second custom output metric derived from the article's text analysis. |
| 16 | `output_metric_3_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Third custom output metric derived from the article's text analysis. |
| 17 | `output_metric_4_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Fourth custom output metric derived from the article's text analysis. |
| 18 | `positive_word_count_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of positive sentiment words identified in the article. |
| 19 | `positive_word_sentiment_stddev_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of sentiment scores for positive words in the article. |
| 20 | `sentence_count_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of sentences in the article. |
| 21 | `text_perplexity_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Perplexity score indicating the unpredictability of the article's text. |
| 22 | `vocab_coverage_ratio_inferess` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Proportion of words in the article matching a reference vocabulary. |
| 23 | `avg_syllables_per_word_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average number of syllables per word in the article for news analytics. |
| 24 | `avg_words_per_sentence_trna_enhanced` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Average number of words per sentence in the analyzed text. |
| 25 | `max_negative_word_sentiment_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum sentiment score among negative words in the article for news analytics. |
| 26 | `max_positive_word_sentiment_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum sentiment score among positive words in the article for news analytics. |
| 27 | `mean_negative_word_sentiment_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean sentiment score of all negative words in the article for news analytics. |
| 28 | `mean_positive_word_sentiment_trna_enhanced` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean sentiment score for all positive words identified in the text. |
| 29 | `min_negative_word_sentiment_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum sentiment score among negative words in the article for news analytics. |
| 30 | `min_positive_word_sentiment_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum sentiment score among positive words in the article for news analytics. |
| 31 | `negative_word_count_trna_enhanced` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of negative sentiment words found in the text. |
| 32 | `negative_word_sentiment_entropy_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Entropy of sentiment distribution among negative words in the article for news analytics. |
| 33 | `negative_word_sentiment_stddev_trna_enhanced` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of sentiment scores among negative words in the text. |
| 34 | `output_metric_1_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | First custom output metric derived from the article's text analysis for news analytics. |
| 35 | `output_metric_2_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Second custom output metric derived from the article's text analysis for news analytics. |
| 36 | `output_metric_3_trna_enhanced` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Third custom output metric derived from enhanced text features. |
| 37 | `output_metric_4_trna_enhanced` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Fourth custom output metric derived from advanced text analysis features. |
| 38 | `positive_word_count_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of positive sentiment words identified in the article for news analytics. |
| 39 | `positive_word_sentiment_entropy_trna_enhanced` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Entropy value measuring the diversity of sentiment among positive words in the text. |
| 40 | `positive_word_sentiment_stddev_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of sentiment scores for positive words in the article for news analytics. |
| 41 | `sentence_count_trna_enhanced` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Total number of sentences present in the text sample. |
| 42 | `text_complexity_score_trna_enhanced` | VECTOR | 0.751 | 风险与质量 | 0 | — | — | — | UNTESTED | A score representing the linguistic complexity of the analyzed text. |
| 43 | `text_perplexity_trna` | VECTOR | 0.751 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Perplexity score indicating the unpredictability of the article's text for news analytics. |
| 44 | `vocab_coverage_ratio_trna_enhanced` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Proportion of words in the text that match a reference vocabulary set. |
| 45 | `avg_syllables_per_word_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average number of syllables per word in the news article. |
| 46 | `avg_words_per_sentence_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average number of words per sentence in the Bloomberg news article. |
| 47 | `max_negative_word_sentiment_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum sentiment score among all negative words in the news article. |
| 48 | `max_positive_word_sentiment_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum sentiment score among all positive words in the news article. |
| 49 | `mean_negative_word_sentiment_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average sentiment score for all negative words in the news text. |
| 50 | `mean_positive_word_sentiment_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average sentiment score for all positive words in the Bloomberg news article. |
| 51 | `min_negative_word_sentiment_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum sentiment score among all negative words in the news article. |
| 52 | `min_positive_word_sentiment_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum sentiment score among all positive words in the news article. |
| 53 | `negative_word_count_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of negative sentiment words present in the news article. |
| 54 | `negative_word_sentiment_entropy_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Entropy value reflecting the diversity of sentiment among negative words in the news text. |
| 55 | `negative_word_sentiment_stddev_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of sentiment scores among negative words in the news article. |
| 56 | `output_metric_1_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | First custom output metric derived from Bloomberg news text features. |
| 57 | `output_metric_2_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Second custom output metric derived from Bloomberg news text features. |
| 58 | `output_metric_3_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Third custom output metric derived from Bloomberg news text analysis. |
| 59 | `output_metric_4_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Fourth custom output metric derived from Bloomberg news text analysis. |
| 60 | `positive_word_count_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of positive sentiment words present in the news article. |
| 61 | `positive_word_sentiment_entropy_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Entropy value measuring the diversity of sentiment among positive words in the news article. |
| 62 | `positive_word_sentiment_stddev_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Standard deviation of sentiment scores among positive words in the news text. |
| 63 | `sentence_count_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of sentences in the Bloomberg news article. |
| 64 | `text_complexity_score_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score indicating the linguistic complexity of the Bloomberg news text. |
| 65 | `text_perplexity_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Perplexity score indicating the unpredictability or complexity of the news text. |
| 66 | `vocab_coverage_ratio_bbgnews_enhanced` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Proportion of words in the news article that match a reference vocabulary. |

## 六、本地回测证据

- 本地累计回测 **9** 条；其中 `ra_failed_checks` 为空的 **9** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `YP5G7ok6` | 0.38 | 0.07 | 0.63 | — | 0.26 | 0 | 114 | `ts_quantile(ts_mean(vec_avg(positive_word_sentiment_entropy_inferess), 22), 22, driver="ga` |
| `A10Mlzew` | 0.27 | 0.04 | 0.54 | — | 0.70 | 0 | 114 | `rank(ts_std_dev(vec_avg(mean_positive_word_sentiment_inferess), 5))` |
| `zqY1knoO` | 0.21 | 0.04 | 1.36 | — | 0.14 | 0 | 114 | `rank(ts_mean(vec_avg(max_negative_word_sentiment_inferess), 22))` |
| `RRVn7wYb` | -0.05 | 0.00 | -0.14 | — | 1.57 | 0 | 114 | `rank(ts_delta(vec_avg(text_complexity_score_inferess), 5))` |
| `akLq79lW` | -0.12 | -0.02 | 0.24 | — | 0.15 | 0 | 114 | `rank(multiply(rank(ts_mean(vec_avg(text_complexity_score_inferess), 22)), rank(ts_mean(vec` |
| `j23b3L7o` | -0.24 | -0.05 | -0.55 | — | 0.15 | 0 | 114 | `rank(ts_mean(vec_avg(min_positive_word_sentiment_inferess), 22))` |
| `WjP672nZ` | -0.28 | -0.07 | -1.44 | — | 0.14 | 0 | 114 | `rank(multiply(rank(ts_mean(vec_avg(text_complexity_score_inferess), 22)), rank(ts_mean(vec` |
| `KPOj7Mwj` | -0.29 | -0.04 | -1.75 | — | 0.71 | 0 | 114 | `ts_zscore(ts_std_dev(vec_avg(max_negative_word_sentiment_inferess), 5), 22)` |
| `QP3L7plW` | -0.34 | -0.08 | -1.17 | — | 0.15 | 0 | 114 | `winsorize(rank(ts_mean(vec_avg(mean_positive_word_sentiment_inferess), 22)), std=4)` |

## 七、判死记录（sealed dead_end）

- `EUR-news_sentiment_dl-SENTIMENT-WEAK`（2026-09-04）family=news_sentiment_dl sentiment word stats：{"best_2y": 1.36, "best_alpha": "zqY1knoO", "best_fitness": 0.04, "best_sharpe": 0.21, "dataset": "news_sentiment_dl", "evidence": "wave114 9 条全灭：情绪词统计（mean/max/min positive/negative sentiment）在 EUR TOP2500 整体弱信号，最强 S0.38/F0.07/2Y0.63 远低于 Mode B 线；text_complexity 交互项全负；ts_std_dev/ts_delta 快腿全负", "id": "EUR-news_sentiment_dl-SENTIMENT-WEAK", "reason": "news_sentiment_dl 情绪词统计与文本复杂度在 EUR D1 无正向预测力；p

