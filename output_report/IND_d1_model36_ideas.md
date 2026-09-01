# IND model36 — SmartRatios Credit Risk Model — S1 Ideas

**Dataset**: model36
**Region**: IND
**Delay**: 1


**Dataset**: model36 | **Region**: IND | **Delay**: 1 | **Universe**: TOP500
**Fields**: 42 MATRIX | **Coverage**: 0.98 | **alphaCount**: 1868

---

## Concept 1: Credit Quality Improvement

**Concept**: Improving credit quality (rising SmartRatios rank) signals reducing default risk and potential multiple expansion. Change in credit rank captures credit trajectory.

- **Implementation Example**: `ts_delta(ts_backfill({star_sr_global_rank}, 66), 10)`

## Concept 2: Leverage-Coverage Spread Shift

**Concept**: Improving leverage coverage ratio relative to peers signals strengthening balance sheet. Spread shift captures relative credit improvement.

- **Implementation Example**: `subtract(ts_backfill({star_sr_coverage}, 66), ts_backfill({star_sr_leverage}, 66))`

## Concept 3: Default Risk Percentile Momentum

**Concept**: Declining default risk percentile (improving relative credit standing) predicts positive re-rating. Momentum of default risk captures credit trajectory.

- **Implementation Example**: `ts_delta(ts_backfill({default_risk_global_percentile}, 66), 20)`

## Concept 4: Sector-Relative Credit Strength

**Concept**: Credit rank within sector vs global rank spread captures sector-specific credit dynamics. Positive = sector credit leader.

- **Implementation Example**: `subtract(rank(ts_backfill({star_sr_sector_rank}, 66)), rank(ts_backfill({star_sr_global_rank}, 66)))`

## Concept 5: Profitability-Coverage Synergy

**Concept**: Strong profitability combined with strong coverage signals high-quality credit. Interaction captures credit quality breadth.

- **Implementation Example**: `multiply(ts_backfill({star_sr_profitability}, 66), ts_backfill({star_sr_coverage}, 66))`

## Concept 6: Liquidity-Growth Divergence

**Concept**: Strong liquidity with weak growth signals defensive credit profile; weak liquidity with strong growth signals aggressive profile. Divergence captures credit style.

- **Implementation Example**: `subtract(ts_backfill({star_sr_liquidity}, 66), ts_backfill({star_sr_growth}, 66))`

## Concept 7: Industry-Relative Default Risk

**Concept**: Default risk percentile within industry captures relative credit standing. Low percentile = industry credit leader.

- **Implementation Example**: `rank(ts_backfill({default_risk_industry_percentile}, 66))`

## Concept 8: Smoothed Credit Rank Trend

**Concept**: Smoothed trend of overall credit rank filters noise and captures persistent credit improvement/deterioration.

- **Implementation Example**: `ts_mean(ts_backfill({star_sr_global_rank}, 66), 15)`