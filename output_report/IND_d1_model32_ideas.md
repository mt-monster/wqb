# IND model32 — Price Momentum Model — S1 Ideas

**Dataset**: model32
**Region**: IND
**Delay**: 1


**Dataset**: model32 | **Region**: IND | **Delay**: 1 | **Universe**: TOP500
**Fields**: 36 MATRIX | **Coverage**: 0.96 | **alphaCount**: 6587

---

## Concept 1: Momentum Horizon Spread

**Concept**: Long-term momentum minus short-term momentum captures trend maturity. Wide positive spread indicates established trend; negative spread signals short-term reversal opportunity.

- **Implementation Example**: `subtract(ts_backfill({long_term_momentum_score_float}, 66), ts_backfill({short_term_momentum_score_float}, 66))`

## Concept 2: Momentum Acceleration

**Concept**: Short-term momentum acceleration predicts continuation; deceleration predicts reversal. Captures the second derivative of price momentum.

- **Implementation Example**: `ts_delta(ts_backfill({short_term_momentum_score_float}, 66), 5)`

## Concept 3: Global-Industry Momentum Divergence

**Concept**: Stock moving with global peers but diverging from industry signals idiosyncratic strength. Global-industry divergence predicts sector rotation timing.

- **Implementation Example**: `subtract(ts_backfill({global_momentum_rank_float}, 66), ts_backfill({industry_momentum_score_float}, 66))`

## Concept 4: Regional-Global Momentum Leadership

**Concept**: Regional momentum leading global momentum predicts local fund flows. Ratio captures regional outperformance/underperformance.

- **Implementation Example**: `divide(ts_backfill({regional_momentum_rank_float}, 66), add(ts_backfill({global_momentum_rank_float}, 66), 1))`

## Concept 5: Industry-Relative Momentum Rank Spread

**Concept**: Industry rank vs global rank spread captures sector rotation timing. Positive spread = industry leader but global laggard (contrarian opportunity).

- **Implementation Example**: `subtract(rank(ts_backfill({industry_momentum_score_float}, 66)), rank(ts_backfill({global_momentum_rank_float}, 66)))`

## Concept 6: Short-Long Momentum Cross-Sectional Spread

**Concept**: Cross-sectional short vs long momentum spread predicts mean reversion. Positive = short-term strength dominating (reversal risk).

- **Implementation Example**: `subtract(rank(ts_backfill({short_term_momentum_score_float}, 66)), rank(ts_backfill({long_term_momentum_score_float}, 66)))`

## Concept 7: Smoothed Mid-Term Momentum

**Concept**: Mid-term momentum (3-6M) smoothed over 10 days captures the sweet spot between noise and signal. Less crowded than short-term, more responsive than long-term.

- **Implementation Example**: `ts_mean(ts_backfill({mid_term_momentum_score_float}, 66), 10)`

## Concept 8: Star PM Global Rank Momentum

**Concept**: Star PM global rank captures proprietary momentum score. Cross-sectional rank of this score identifies relative strength within universe.

- **Implementation Example**: `rank(ts_backfill({star_pm_global_rank}, 66))`