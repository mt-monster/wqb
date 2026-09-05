# news_sentiment_dl Feature Engineering Analysis Report

- **Dataset**: `news_sentiment_dl`
- **Category**: `other`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 66
- **Generated**: 2026-09-04T00:31:36.563422

---

## Executive Summary

本数据集提供 66 个字段（MATRIX 0 / VECTOR 66 / GROUP 0），覆盖 `other` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Description |
|---|---|---|---|
| `avg_syllables_per_word_bbgnews_enhanced` | VECTOR | 74% | Average number of syllables per word in the news article. |
| `avg_syllables_per_word_inferess` | VECTOR | 77% | Average number of syllables per word in the article. |
| `avg_syllables_per_word_trna` | VECTOR | 75% | Average number of syllables per word in the article for news analytics. |
| `avg_words_per_sentence_bbgnews_enhanced` | VECTOR | 74% | Average number of words per sentence in the Bloomberg news article. |
| `avg_words_per_sentence_inferess` | VECTOR | 77% | Average number of words per sentence in the article. |
| `avg_words_per_sentence_trna_enhanced` | VECTOR | 75% | Average number of words per sentence in the analyzed text. |
| `max_negative_word_sentiment_bbgnews_enhanced` | VECTOR | 74% | Maximum sentiment score among all negative words in the news article. |
| `max_negative_word_sentiment_inferess` | VECTOR | 77% | Maximum sentiment score among negative words in the article. |
| `max_negative_word_sentiment_trna` | VECTOR | 75% | Maximum sentiment score among negative words in the article for news analytics. |
| `max_positive_word_sentiment_bbgnews_enhanced` | VECTOR | 74% | Maximum sentiment score among all positive words in the news article. |
| `max_positive_word_sentiment_inferess` | VECTOR | 77% | Maximum sentiment score among positive words in the article. |
| `max_positive_word_sentiment_trna` | VECTOR | 75% | Maximum sentiment score among positive words in the article for news analytics. |
| `mean_negative_word_sentiment_bbgnews_enhanced` | VECTOR | 74% | Average sentiment score for all negative words in the news text. |
| `mean_negative_word_sentiment_inferess` | VECTOR | 77% | Mean sentiment score of all negative words in the article. |
| `mean_negative_word_sentiment_trna` | VECTOR | 75% | Mean sentiment score of all negative words in the article for news analytics. |
| `mean_positive_word_sentiment_bbgnews_enhanced` | VECTOR | 74% | Average sentiment score for all positive words in the Bloomberg news article. |
| `mean_positive_word_sentiment_inferess` | VECTOR | 77% | Mean sentiment score of all positive words in the article. |
| `mean_positive_word_sentiment_trna_enhanced` | VECTOR | 75% | Mean sentiment score for all positive words identified in the text. |
| `min_negative_word_sentiment_bbgnews_enhanced` | VECTOR | 74% | Minimum sentiment score among all negative words in the news article. |
| `min_negative_word_sentiment_inferess` | VECTOR | 77% | Minimum sentiment score among negative words in the article. |
| `min_negative_word_sentiment_trna` | VECTOR | 75% | Minimum sentiment score among negative words in the article for news analytics. |
| `min_positive_word_sentiment_bbgnews_enhanced` | VECTOR | 74% | Minimum sentiment score among all positive words in the news article. |
| `min_positive_word_sentiment_inferess` | VECTOR | 77% | Minimum sentiment score among positive words in the article. |
| `min_positive_word_sentiment_trna` | VECTOR | 75% | Minimum sentiment score among positive words in the article for news analytics. |
| `negative_word_count_bbgnews_enhanced` | VECTOR | 74% | Number of negative sentiment words present in the news article. |
| `negative_word_count_inferess` | VECTOR | 77% | Number of negative sentiment words identified in the article. |
| `negative_word_count_trna_enhanced` | VECTOR | 75% | Count of negative sentiment words found in the text. |
| `negative_word_sentiment_entropy_bbgnews_enhanced` | VECTOR | 74% | Entropy value reflecting the diversity of sentiment among negative words in the news text. |
| `negative_word_sentiment_entropy_inferess` | VECTOR | 77% | Entropy of sentiment distribution among negative words in the article. |
| `negative_word_sentiment_entropy_trna` | VECTOR | 75% | Entropy of sentiment distribution among negative words in the article for news analytics. |
| `negative_word_sentiment_stddev_bbgnews_enhanced` | VECTOR | 74% | Standard deviation of sentiment scores among negative words in the news article. |
| `negative_word_sentiment_stddev_inferess` | VECTOR | 77% | Standard deviation of sentiment scores for negative words in the article. |
| `negative_word_sentiment_stddev_trna_enhanced` | VECTOR | 75% | Standard deviation of sentiment scores among negative words in the text. |
| `output_metric_1_bbgnews_enhanced` | VECTOR | 74% | First custom output metric derived from Bloomberg news text features. |
| `output_metric_1_inferess` | VECTOR | 77% | First custom output metric derived from the article's text analysis. |
| `output_metric_1_trna` | VECTOR | 75% | First custom output metric derived from the article's text analysis for news analytics. |
| `output_metric_2_bbgnews_enhanced` | VECTOR | 74% | Second custom output metric derived from Bloomberg news text features. |
| `output_metric_2_inferess` | VECTOR | 77% | Second custom output metric derived from the article's text analysis. |
| `output_metric_2_trna` | VECTOR | 75% | Second custom output metric derived from the article's text analysis for news analytics. |
| `output_metric_3_bbgnews_enhanced` | VECTOR | 74% | Third custom output metric derived from Bloomberg news text analysis. |
| `output_metric_3_inferess` | VECTOR | 77% | Third custom output metric derived from the article's text analysis. |
| `output_metric_3_trna_enhanced` | VECTOR | 75% | Third custom output metric derived from enhanced text features. |
| `output_metric_4_bbgnews_enhanced` | VECTOR | 74% | Fourth custom output metric derived from Bloomberg news text analysis. |
| `output_metric_4_inferess` | VECTOR | 77% | Fourth custom output metric derived from the article's text analysis. |
| `output_metric_4_trna_enhanced` | VECTOR | 75% | Fourth custom output metric derived from advanced text analysis features. |
| `positive_word_count_bbgnews_enhanced` | VECTOR | 74% | Number of positive sentiment words present in the news article. |
| `positive_word_count_inferess` | VECTOR | 77% | Number of positive sentiment words identified in the article. |
| `positive_word_count_trna` | VECTOR | 75% | Number of positive sentiment words identified in the article for news analytics. |
| `positive_word_sentiment_entropy_bbgnews_enhanced` | VECTOR | 74% | Entropy value measuring the diversity of sentiment among positive words in the news article. |
| `positive_word_sentiment_entropy_inferess` | VECTOR | 77% | Entropy of sentiment distribution among positive words in the article. |
| `positive_word_sentiment_entropy_trna_enhanced` | VECTOR | 75% | Entropy value measuring the diversity of sentiment among positive words in the text. |
| `positive_word_sentiment_stddev_bbgnews_enhanced` | VECTOR | 74% | Standard deviation of sentiment scores among positive words in the news text. |
| `positive_word_sentiment_stddev_inferess` | VECTOR | 77% | Standard deviation of sentiment scores for positive words in the article. |
| `positive_word_sentiment_stddev_trna` | VECTOR | 75% | Standard deviation of sentiment scores for positive words in the article for news analytics. |
| `sentence_count_bbgnews_enhanced` | VECTOR | 74% | Total number of sentences in the Bloomberg news article. |
| `sentence_count_inferess` | VECTOR | 77% | Total number of sentences in the article. |
| `sentence_count_trna_enhanced` | VECTOR | 75% | Total number of sentences present in the text sample. |
| `text_complexity_score_bbgnews_enhanced` | VECTOR | 74% | A score indicating the linguistic complexity of the Bloomberg news text. |
| `text_complexity_score_inferess` | VECTOR | 77% | A score representing the linguistic complexity of the article. |
| `text_complexity_score_trna_enhanced` | VECTOR | 75% | A score representing the linguistic complexity of the analyzed text. |
| `text_perplexity_bbgnews_enhanced` | VECTOR | 74% | Perplexity score indicating the unpredictability or complexity of the news text. |
| `text_perplexity_inferess` | VECTOR | 77% | Perplexity score indicating the unpredictability of the article's text. |
| `text_perplexity_trna` | VECTOR | 75% | Perplexity score indicating the unpredictability of the article's text for news analytics. |
| `vocab_coverage_ratio_bbgnews_enhanced` | VECTOR | 74% | Proportion of words in the news article that match a reference vocabulary. |
| `vocab_coverage_ratio_inferess` | VECTOR | 77% | Proportion of words in the article matching a reference vocabulary. |
| `vocab_coverage_ratio_trna_enhanced` | VECTOR | 75% | Proportion of words in the text that match a reference vocabulary set. |

## 字段解构（Field Deconstruction）

### `avg_syllables_per_word_inferess`（VECTOR）
- **测什么**：Average number of syllables per word in the article.
- **覆盖率**：0.7723
- **字段名语义**：`avg_syllables_per_word_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `avg_words_per_sentence_inferess`（VECTOR）
- **测什么**：Average number of words per sentence in the article.
- **覆盖率**：0.7723
- **字段名语义**：`avg_words_per_sentence_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `max_negative_word_sentiment_inferess`（VECTOR）
- **测什么**：Maximum sentiment score among negative words in the article.
- **覆盖率**：0.7723
- **字段名语义**：`max_negative_word_sentiment_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `max_positive_word_sentiment_inferess`（VECTOR）
- **测什么**：Maximum sentiment score among positive words in the article.
- **覆盖率**：0.7723
- **字段名语义**：`max_positive_word_sentiment_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `mean_negative_word_sentiment_inferess`（VECTOR）
- **测什么**：Mean sentiment score of all negative words in the article.
- **覆盖率**：0.7723
- **字段名语义**：`mean_negative_word_sentiment_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `mean_positive_word_sentiment_inferess`（VECTOR）
- **测什么**：Mean sentiment score of all positive words in the article.
- **覆盖率**：0.7723
- **字段名语义**：`mean_positive_word_sentiment_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `min_negative_word_sentiment_inferess`（VECTOR）
- **测什么**：Minimum sentiment score among negative words in the article.
- **覆盖率**：0.7723
- **字段名语义**：`min_negative_word_sentiment_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `min_positive_word_sentiment_inferess`（VECTOR）
- **测什么**：Minimum sentiment score among positive words in the article.
- **覆盖率**：0.7723
- **字段名语义**：`min_positive_word_sentiment_inferess` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：对 VECTOR/GROUP 字段先截面聚合再中性化
- vec_ 向量包装：66 个 VECTOR 字段需用 vec_* 算子读取

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`avg_syllables_per_word_inferess`, `avg_words_per_sentence_inferess`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## 字段白名单（Field Whitelist）

```
avg_syllables_per_word_bbgnews_enhanced
avg_syllables_per_word_inferess
avg_syllables_per_word_trna
avg_words_per_sentence_bbgnews_enhanced
avg_words_per_sentence_inferess
avg_words_per_sentence_trna_enhanced
max_negative_word_sentiment_bbgnews_enhanced
max_negative_word_sentiment_inferess
max_negative_word_sentiment_trna
max_positive_word_sentiment_bbgnews_enhanced
max_positive_word_sentiment_inferess
max_positive_word_sentiment_trna
mean_negative_word_sentiment_bbgnews_enhanced
mean_negative_word_sentiment_inferess
mean_negative_word_sentiment_trna
mean_positive_word_sentiment_bbgnews_enhanced
mean_positive_word_sentiment_inferess
mean_positive_word_sentiment_trna_enhanced
min_negative_word_sentiment_bbgnews_enhanced
min_negative_word_sentiment_inferess
min_negative_word_sentiment_trna
min_positive_word_sentiment_bbgnews_enhanced
min_positive_word_sentiment_inferess
min_positive_word_sentiment_trna
negative_word_count_bbgnews_enhanced
negative_word_count_inferess
negative_word_count_trna_enhanced
negative_word_sentiment_entropy_bbgnews_enhanced
negative_word_sentiment_entropy_inferess
negative_word_sentiment_entropy_trna
negative_word_sentiment_stddev_bbgnews_enhanced
negative_word_sentiment_stddev_inferess
negative_word_sentiment_stddev_trna_enhanced
output_metric_1_bbgnews_enhanced
output_metric_1_inferess
output_metric_1_trna
output_metric_2_bbgnews_enhanced
output_metric_2_inferess
output_metric_2_trna
output_metric_3_bbgnews_enhanced
output_metric_3_inferess
output_metric_3_trna_enhanced
output_metric_4_bbgnews_enhanced
output_metric_4_inferess
output_metric_4_trna_enhanced
positive_word_count_bbgnews_enhanced
positive_word_count_inferess
positive_word_count_trna
positive_word_sentiment_entropy_bbgnews_enhanced
positive_word_sentiment_entropy_inferess
positive_word_sentiment_entropy_trna_enhanced
positive_word_sentiment_stddev_bbgnews_enhanced
positive_word_sentiment_stddev_inferess
positive_word_sentiment_stddev_trna
sentence_count_bbgnews_enhanced
sentence_count_inferess
sentence_count_trna_enhanced
text_complexity_score_bbgnews_enhanced
text_complexity_score_inferess
text_complexity_score_trna_enhanced
text_perplexity_bbgnews_enhanced
text_perplexity_inferess
text_perplexity_trna
vocab_coverage_ratio_bbgnews_enhanced
vocab_coverage_ratio_inferess
vocab_coverage_ratio_trna_enhanced
```

*Report generated: 2026-09-04T00:31:36.563422*