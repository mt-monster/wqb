# EUR D1 news84 ideas (Wave40 slot1 weak probe)

Dataset: news84 transferred news sentiment. Coverage ~0.80 MATRIX. Distinct from news85 DNN (Wave39 max |S|0.32, left).

## Preprocess
- `ts_backfill(field, 66)` on all MATRIX scores (cov < 0.85)
- Bounded sentiment: no winsorize
- Counts: `rank`
- VECTOR `mws84_sentiment`: `vec_avg` first (not used in slot1 MATRIX batch)

## Concept

**Concept**: Transferred-news mean sentiment as cross-sectional rank after backfill.

**Implementation Example**:
`rank(ts_backfill(mean_sentiment_score_transfer, 66))`

**Concept**: Primary-minus-secondary transferred sentiment disagreement.

**Implementation Example**:
`rank(subtract(ts_backfill(mean_primary_sentiment_score_transfer, 66), ts_backfill(mean_secondary_sentiment_score_transfer, 66)))`

**Concept**: Sentiment mixed with news-item intensity.

**Implementation Example**:
`add(0.6*rank(ts_backfill(mean_sentiment_score_transfer, 66)), 0.4*rank(ts_backfill(news_item_count_transfer, 66)))`
