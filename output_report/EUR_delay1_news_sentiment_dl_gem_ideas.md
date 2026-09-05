# news_sentiment_dl GEM Ideas (wave114)

**Dataset**: news_sentiment_dl
**Region**: EUR
**Delay**: 1


**Concept**: 积极情绪词平均水平（慢腿）
- **Implementation Example**: `rank(ts_mean(vec_avg({word_sentiment_inferess}), 22))`
- **Rationale**: 积极情绪词的长期平均水平反映市场对公司的持续乐观程度，与新闻情感数据集（news73）的 globalsent 类似但字段更细（分 inferess 源）

**Concept**: 消极情绪词平均水平（慢腿）
- **Implementation Example**: `rank(ts_mean(vec_avg({word_sentiment_inferess}), 22))`
- **Rationale**: 消极情绪词的长期平均水平反映市场对公司的持续悲观程度，与积极情绪形成对照

**Concept**: 情绪词极性差异（慢腿）
- **Implementation Example**: `rank(ts_mean(subtract(vec_avg({word_sentiment_inferess}), vec_avg({word_sentiment_inferess})), 22))`
- **Rationale**: 积极-消极情绪词的差异捕捉情绪极性，比单一情绪更稳健

**Concept**: 情绪词波动率（快腿）
- **Implementation Example**: `rank(ts_std_dev(vec_avg({word_sentiment_inferess}), 5))`
- **Rationale**: 情绪词短期波动率反映情绪不稳定性，高波动可能预示反转

**Concept**: 文本复杂度变化（快腿）
- **Implementation Example**: `rank(ts_delta(vec_avg({complexity_score_inferess}), 5))`
- **Rationale**: 文本复杂度短期变化反映新闻内容的突然复杂化，可能与重大事件相关

**Concept**: 情绪词计数差异（快腿）
- **Implementation Example**: `rank(ts_delta(subtract(vec_avg({word_count_inferess}), vec_avg({word_count_inferess})), 5))`
- **Rationale**: 积极-消极词计数差异的短期变化捕捉情绪转向，比水平值更敏感

**Concept**: 情绪熵（多样性）
- **Implementation Example**: `rank(ts_mean(vec_avg({sentiment_entropy_inferess}), 22))`
- **Rationale**: 情绪熵反映情绪分布的多样性，低熵（情绪集中）可能预示趋势延续

**Concept**: 复杂度×情绪交互（组合）
- **Implementation Example**: `rank(multiply(rank(ts_mean(vec_avg({complexity_score_inferess}), 22)), rank(ts_mean(vec_avg({word_sentiment_inferess}), 22))))`
- **Rationale**: 文本复杂度与积极情绪的交互项，捕捉"复杂好消息"与"简单好消息"的差异