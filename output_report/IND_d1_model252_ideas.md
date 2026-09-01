# IND model252 — SHIELD Defensiveness — S1 Ideas

**Dataset**: model252
**Region**: IND
**Delay**: 1


**Dataset**: model252 | **Region**: IND | **Delay**: 1 | **Universe**: TOP500
**Fields**: 2 MATRIX | **Coverage**: 0.79 | **alphaCount**: 905

---

## Concept 1: Defensiveness Score Momentum

**Concept**: Rising defensiveness score signals increasing flight-to-quality demand. Momentum captures defensive rotation timing.

- **Implementation Example**: `ts_delta(ts_backfill({defensiveness_composite_score}, 66), 10)`

## Concept 2: Defensiveness Rank

**Concept**: Cross-sectional rank of defensiveness identifies relative safety within universe. High rank = most defensive stocks.

- **Implementation Example**: `rank(ts_backfill({defensiveness_composite_score}, 66))`

## Concept 3: Defensiveness Volatility

**Concept**: Volatility of defensiveness score captures stability of defensive characteristics. Low volatility = stable defensive profile.

- **Implementation Example**: `ts_std_dev(ts_backfill({defensiveness_composite_score}, 66), 20)`

## Concept 4: Defensiveness Z-Score

**Concept**: Z-score captures statistical extremity of defensive positioning. Extreme values = crowded defensive trades (contrarian signal).

- **Implementation Example**: `ts_zscore(ts_backfill({defensiveness_composite_score}, 66), 60)`

## Concept 5: Smoothed Defensiveness Trend

**Concept**: Smoothed defensiveness captures persistent defensive rotation trend, filtering daily noise.

- **Implementation Example**: `ts_mean(ts_backfill({defensiveness_composite_score}, 66), 15)`

## Concept 6: Defensiveness Acceleration

**Concept**: Acceleration of defensiveness score captures second-order defensive dynamics. Positive = strengthening defensive rotation.

- **Implementation Example**: `ts_delta(ts_delta(ts_backfill({defensiveness_composite_score}, 66), 5), 5)`

## Concept 7: Defensiveness-Market Value Divergence

**Concept**: Defensiveness score rising while market value stagnant signals defensive re-rating opportunity. Divergence captures defensive premium shift.

- **Implementation Example**: `subtract(ts_delta(ts_backfill({defensiveness_composite_score}, 66), 10), ts_delta(ts_backfill({total_equity_market_value_2}, 66), 10))`

## Concept 8: Defensiveness Percentile

**Concept**: Percentile rank within recent history captures relative defensiveness vs recent past. High percentile = recent defensive strength.

- **Implementation Example**: `ts_rank(ts_backfill({defensiveness_composite_score}, 66), 60)`