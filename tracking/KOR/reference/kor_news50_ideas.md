# news50 GEM Ideas (KOR / TOP600 / delay1)

## 字段

- 主信号：analyst_recommendation_change_score_d0（users=0）、news_volatility_projection_score_d0（users=0）、event_novelty_score_d0（users=0）、positive_event_ratio_score_d0（users=0）
- 辅助：mws50_vea（事件量 users=1）、mws50_nip（冲击预测 users=1）、mws50_ghc_lna（推荐变更 users=1）
- 避开：*_sentiment_score tone 族（KOR 新闻情绪三波判死）；mws50_ess/ens 低覆盖 0.35 族；元数据字段

## 特征

- VECTOR 事件流 → vec_avg + ts_backfill 22；0-100 评分与计数均偏态 → rank 强制；d0 变体冷门优先

## 建议

- 推荐上调→正漂移（wave 143 EPS 修订 WIN 同机制）；industry 组内相对化（wave 143 验证 +0.10S）；ts_decay_linear(22) 平滑；事件量过度关注→负向反转

**Dataset**: news50
**Region**: KOR
**Delay**: 1

**Concept**: Analyst Recommendation Change Momentum
- **Mechanism**: News-carried analyst recommendation upgrades signal improving fundamentals; the market underreacts to recommendation changes distributed via news, producing post-announcement drift. expected_exposure: recommendation revision momentum.
- **Fields**: `analyst_recommendation_change_score_d0`
- **Implementation Example**: `rank(ts_backfill(vec_avg({analyst_recommendation_change_score_d0}), 22))`
- **Direction**: positive

**Concept**: Industry-Relative Recommendation Change
- **Mechanism**: Ranking recommendation-change flow within industry isolates firm-specific upgrades from sector-wide rating waves; wave 143 proved industry grouping beats sector (+0.10 Sharpe). expected_exposure: industry-neutral revision momentum.
- **Fields**: `analyst_recommendation_change_score_d0`
- **Implementation Example**: `group_rank(rank(ts_decay_linear(ts_backfill(vec_avg({analyst_recommendation_change_score_d0}), 22), 22)), industry)`
- **Direction**: positive

**Concept**: News Impact Projection Reversal
- **Mechanism**: News flagged as high market-impact triggers overreaction; prices overshoot on impact day and revert as the information is digested. expected_exposure: news overreaction reversal.
- **Fields**: `news_volatility_projection_score_d0`
- **Implementation Example**: `multiply(-1, rank(ts_backfill(vec_avg({news_volatility_projection_score_d0}), 22)))`
- **Direction**: negative

**Concept**: Novel Event Information Premium
- **Mechanism**: Genuinely novel events (high novelty score) carry more unpriced information than repeated coverage; fresh-event stocks drift as the market digests new information slowly. expected_exposure: novelty information premium.
- **Fields**: `event_novelty_score_d0`
- **Implementation Example**: `rank(ts_mean(ts_backfill(vec_avg({event_novelty_score_d0}), 22), 5))`
- **Direction**: positive

**Concept**: Positive Event Ratio Quality
- **Mechanism**: A high rolling ratio of positive to total non-neutral events marks a persistently improving news environment that is slowly priced in. expected_exposure: news environment quality.
- **Fields**: `positive_event_ratio_score_d0`
- **Implementation Example**: `group_rank(rank(ts_backfill(vec_avg({positive_event_ratio_score_d0}), 22)), industry)`
- **Direction**: positive

**Concept**: Event Volume Attention Reversal
- **Mechanism**: Extreme 91-day event volume marks attention peaks; retail-driven over-attention inflates prices that subsequently revert. expected_exposure: attention reversal.
- **Fields**: `mws50_vea`
- **Implementation Example**: `multiply(-1, rank(ts_backfill(vec_avg({mws50_vea}), 66)))`
- **Direction**: negative
