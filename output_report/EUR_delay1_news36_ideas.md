# EUR D1 news36 ideas (Wave65 — agent S1; GEM LLM 402)

Dataset: `news36` VECTOR story novelty + phrase/word sentiment. Sparse → densify.
OS ACTIVE=3. Priors: leave news38/84/85; skip news54 timestamps/headlines; no resid×PV.

## Preprocess
- VECTOR: `vec_avg(field)` then `ts_backfill(..., 66)` (120 for novelty)
- Skip: `mws36_timestamp_time`, `mws36_title`, `event_effect_magnitude` (unpopulated)

## Field whitelist
| id | role | cov |
|---|---|---|
| mws36_novelty | 0–100 novelty | 0.77 |
| mws36_novelty_newest_span / oldest_span | recency of similar stories | 0.77 |
| mws36_relevance | entity relevance 0–100 | 0.77 |
| mws36_key_event_confidence | key-event classification confidence | 0.77 |
| mws36_sentiment_phrase_positive / negative | bigram phrase counts | 0.77 |
| mws36_sentiment_words_positive / negative | unigram token counts | 0.77 |
| mws36_sentiment_positive_confidence / negative_confidence | class confidence | 0.77 |
| mws36_total_words | unigram denominator | 0.77 |

## Concepts

**1 — Densified novelty mean-reversion**  
Fresh stories overreact; invert densified novelty.  
`subtract(0, rank(ts_backfill(vec_avg(mws36_novelty), 66)))`

**2 — Phrase polarity imbalance**  
`rank(ts_backfill(subtract(vec_avg(mws36_sentiment_phrase_positive), vec_avg(mws36_sentiment_phrase_negative)), 66))`

**3 — Word polarity imbalance**  
`rank(ts_backfill(subtract(vec_avg(mws36_sentiment_words_positive), vec_avg(mws36_sentiment_words_negative)), 66))`

**4 — Sentiment confidence imbalance**  
`rank(ts_backfill(subtract(vec_avg(mws36_sentiment_positive_confidence), vec_avg(mws36_sentiment_negative_confidence)), 66))`

**5 — Relevance-gated novelty**  
`multiply(rank(ts_backfill(vec_avg(mws36_novelty), 66)), rank(ts_backfill(vec_avg(mws36_relevance), 66)))`

**6 — Relevance-gated inverted negative phrases**  
`multiply(subtract(0, rank(ts_backfill(vec_avg(mws36_sentiment_phrase_negative), 66))), rank(ts_backfill(vec_avg(mws36_relevance), 66)))`

**7 — Length-normalized phrase sentiment**  
`rank(ts_backfill(divide(subtract(vec_avg(mws36_sentiment_phrase_positive), vec_avg(mws36_sentiment_phrase_negative)), add(vec_avg(mws36_total_words), 1)), 66))`

## Rules
- 7 slots × 8 structure variants; no PV mix unless a slot alone hits |S|≥1.0
- Skip entitlement/time/title
