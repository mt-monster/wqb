# EUR D1 news38 ideas (Wave64 — agent S1; GEM LLM unavailable 402)

Dataset: `news38` VECTOR news analytics. Sparse event stream → densify before CS rank.
OS ACTIVE=3. Priors: no resid×v_rev×wedge cookie-cutter; no entitlement/time metadata; news84/85 left.

## Preprocess
- VECTOR: `vec_avg(field)` then `ts_backfill(..., 66)` (or 120 for tone)
- Prefer `trade_when` / backfill densify to avoid CONCENTRATED_WEIGHT
- Skip: `*_entitlement`, `*_time`, `mws38_action`, `mws38_type`, `mws38_version`, `mws38_previous`

## Field whitelist (usable)
| id | role | cov |
|---|---|---|
| mws38_sg_tone_score | signed tone (sg) | 0.74 |
| mws38_sg_positive_score / mws38_sg_negative_score | polarity | 0.74 |
| mws38_sg_positive_freq / mws38_sg_negative_freq | polarity intensity | 0.74 |
| mws38_relevances | story–stock relevance | 0.83 |
| market_impact_indicator | attention / heat | 0.83 |
| mws38_related_num | related entity count | 0.83 |
| mws38_score / mws38_value | generic news score/value | 0.74 |
| story_analytics_relevance_score | composite analytics | 0.90 |
| story_analytics_metric_value | analytics metric | 0.83 |

## Concepts (mechanism → fields → example)

**Concept 1 — Densified signed tone mean-reversion**  
Negative tone after densify predicts rebound (invert).  
Fields: `mws38_sg_tone_score`  
Implementation:
`subtract(0, rank(ts_backfill(vec_avg(mws38_sg_tone_score), 66)))`

**Concept 2 — Polarity imbalance (pos−neg)**  
Fields: `mws38_sg_positive_score`, `mws38_sg_negative_score`  
Implementation:
`rank(ts_backfill(subtract(vec_avg(mws38_sg_positive_score), vec_avg(mws38_sg_negative_score)), 66))`

**Concept 3 — Frequency-weighted polarity**  
Fields: `mws38_sg_positive_freq`, `mws38_sg_negative_freq`  
Implementation:
`rank(ts_backfill(subtract(vec_avg(mws38_sg_positive_freq), vec_avg(mws38_sg_negative_freq)), 66))`

**Concept 4 — Relevance-gated tone**  
Only tone where relevance is high (multiply ranks).  
Fields: `mws38_sg_tone_score`, `mws38_relevances`  
Implementation:
`multiply(rank(ts_backfill(vec_avg(mws38_sg_tone_score), 66)), rank(ts_backfill(vec_avg(mws38_relevances), 66)))`

**Concept 5 — Attention heat vs relevance**  
Crowding heat without relevance is noise; prefer relevance−heat.  
Fields: `story_analytics_relevance_score`, `market_impact_indicator`  
Implementation:
`rank(ts_backfill(subtract(vec_avg(story_analytics_relevance_score), vec_avg(market_impact_indicator)), 66))`

**Concept 6 — Entity breadth × tone**  
Broad stories with negative tone.  
Fields: `mws38_related_num`, `mws38_sg_tone_score`  
Implementation:
`multiply(rank(ts_backfill(vec_avg(mws38_related_num), 66)), subtract(0, rank(ts_backfill(vec_avg(mws38_sg_tone_score), 66))))`

**Concept 7 — Analytics metric vs score disagreement**  
Fields: `story_analytics_metric_value`, `mws38_score`  
Implementation:
`rank(ts_backfill(subtract(vec_avg(story_analytics_metric_value), vec_avg(mws38_score)), 66))`

**Concept 8 — Long-window tone drift**  
Fields: `mws38_sg_tone_score`  
Implementation:
`rank(ts_delta(ts_backfill(vec_avg(mws38_sg_tone_score), 120), 22))`

## Generation rules for Wave64
- Each slot = one concept family; 6–8 structural variants (window 66/120, invert, group_neutralize industry optional)
- **Do not** paste capacq/yield 3-leg PV mix unless a news slow leg alone shows |S|≥1.0 on a 8-expr probe first
- First batch: pure news concepts only (no PV fast legs)
