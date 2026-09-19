# news_sentiment_nlp Feature Engineering Analysis Report

**Dataset**: news_sentiment_nlp
**Region**: EUR
**Delay**: 1

- **Dataset**: `news_sentiment_nlp`
- **Category**: `other`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 23

---

## 数据集画像（2026-09-11）

新闻标题 NLP 情绪数据集，23 个 VECTOR 字段全是信号类，coverage 0.9134。
三类信号：① 情绪分数（vader/textblob/sentence_sentiment avg/max/min/var）
② 情绪极性（vader/sentiwordnet positive/negative/neutral）③ 文本特征（可读性/词数/主观性）。
users 0-3 极低 → prod_corr 理论≈0，优质处女地。全部 VECTOR 字段必须先 vec_* 聚合。

## GEM 兼容模板（Concept Blocks）

> 情绪概念优先：机制 → 具体字段 → 一个实现。占位符用字段族后缀（可多字段匹配展开）。

**Concept**: 标题情绪水平（vader 复合情绪）
- **Mechanism**: VADER 复合情绪（-1~1）截面相对定位，正面情绪→long
- **Fields Used**: `headline_sentiment_vader_score`
- **Implementation Example**: `rank(ts_mean(vec_avg({headline_sentiment_vader_score}), 22))`
- **Direction**: High → long

**Concept**: 标题情绪动量（vader 情绪变化）
- **Mechanism**: 情绪的时间序列变化，捕捉情绪改善/恶化动量
- **Fields Used**: `headline_sentiment_vader_score`
- **Implementation Example**: `rank(ts_delta(vec_avg({headline_sentiment_vader_score}), 5))`
- **Direction**: High → long

**Concept**: 句间情绪极化（sentiment max-min 分歧）
- **Mechanism**: 句间情绪极差=不确定性/分歧，高极化→short（不确定性利空）
- **Fields Used**: `headline_sentence_sentiment_maximum`, `headline_sentence_sentiment_minimum`
- **Implementation Example**: `subtract(0, rank(vec_avg({headline_sentence_sentiment_maximum}) - vec_avg({headline_sentence_sentiment_minimum})))`
- **Direction**: Low（高极化） → short

**Concept**: 句内情绪方差（sentiment variance 分歧）
- **Mechanism**: 句间情绪方差=观点不一致，高方差→short
- **Fields Used**: `headline_sentence_sentiment_variance`
- **Implementation Example**: `subtract(0, rank(ts_mean(vec_avg({headline_sentence_sentiment_variance}), 22)))`
- **Direction**: Low（高方差） → short

**Concept**: 净情绪极性（vader positive-negative）
- **Mechanism**: 正极性减负极性=净情绪，净正面→long
- **Fields Used**: `headline_vader_positive_polarity`, `headline_vader_negative_polarity`
- **Implementation Example**: `rank(vec_avg({headline_vader_positive_polarity}) - vec_avg({headline_vader_negative_polarity}))`
- **Direction**: High → long

**Concept**: textblob 情绪水平（跨源情绪验证）
- **Mechanism**: TextBlob 情绪与 vader 跨源印证，正面→long
- **Fields Used**: `headline_textblob_sentiment_score`
- **Implementation Example**: `rank(ts_mean(vec_avg({headline_textblob_sentiment_score}), 22))`
- **Direction**: High → long

**Concept**: 情绪行业内相对（group_rank 中性化）
- **Mechanism**: 情绪在行业内相对定位，剥离行业情绪基调差异
- **Fields Used**: `headline_sentiment_vader_score`
- **Implementation Example**: `group_rank(ts_mean(vec_avg({headline_sentiment_vader_score}), 22), subindustry)`
- **Direction**: High → long

**Concept**: 主观性情绪交互（subjectivity×sentiment）
- **Mechanism**: 主观性高的情绪化标题更可信，主观×情绪→long
- **Fields Used**: `headline_subjectivity_score`, `headline_sentiment_vader_score`
- **Implementation Example**: `rank(vec_avg({headline_subjectivity_score}) * vec_avg({headline_sentiment_vader_score}))`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
headline_sentiment_vader_score
headline_textblob_sentiment_score
headline_sentence_sentiment_average
headline_sentence_sentiment_maximum
headline_sentence_sentiment_minimum
headline_sentence_sentiment_variance
headline_vader_positive_polarity
headline_vader_negative_polarity
headline_vader_neutral_polarity
headline_sentiwordnet_positive_polarity
headline_sentiwordnet_negative_polarity
headline_subjectivity_score
```
