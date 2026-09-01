# IND risk70 — Multi-Factor Risk Model — S1 Ideas

**Dataset**: risk70
**Region**: IND
**Delay**: 1


**Dataset**: risk70 | **Region**: IND | **Delay**: 1 | **Universe**: TOP500
**Fields**: 35 MATRIX | **Coverage**: 1.0 | **alphaCount**: 3816

---

## Concept 1: Sector Exposure Momentum

**Concept**: Change in sector exposure captures sector rotation timing. Rising exposure signals increasing sector allocation.

- **Implementation Example**: `ts_delta(ts_backfill({sector_exposure}, 66), 10)`

## Concept 2: Hedge Fund Ownership Momentum

**Concept**: Change in hedge fund ownership captures smart money flow. Rising ownership signals institutional accumulation.

- **Implementation Example**: `ts_delta(ts_backfill({hedge_fund_ownership}, 66), 20)`

## Concept 3: Sector Exposure Rank

**Concept**: Cross-sectional rank of sector exposure identifies relative sector positioning. High rank = crowded sector (contrarian signal).

- **Implementation Example**: `rank(ts_backfill({sector_exposure}, 66))`

## Concept 4: Hedge Fund Ownership Z-Score

**Concept**: Z-score of hedge fund ownership captures statistical extremity of institutional positioning. Extreme values = crowded trades.

- **Implementation Example**: `ts_zscore(ts_backfill({hedge_fund_ownership}, 66), 60)`

## Concept 5: Sector-Ownership Divergence

**Concept**: Sector exposure rising while hedge fund ownership falling signals retail-driven sector rotation (fade). Divergence captures flow dynamics.

- **Implementation Example**: `subtract(ts_delta(ts_backfill({sector_exposure}, 66), 10), ts_delta(ts_backfill({hedge_fund_ownership}, 66), 10))`

## Concept 6: Smoothed Sector Exposure Trend

**Concept**: Smoothed sector exposure captures persistent sector allocation trend, filtering daily noise.

- **Implementation Example**: `ts_mean(ts_backfill({sector_exposure}, 66), 15)`

## Concept 7: Hedge Fund Ownership Percentile

**Concept**: Percentile rank of hedge fund ownership within recent history captures relative institutional interest vs recent past.

- **Implementation Example**: `ts_rank(ts_backfill({hedge_fund_ownership}, 66), 60)`

## Concept 8: Sector Exposure Volatility

**Concept**: Volatility of sector exposure captures stability of sector allocation. Low volatility = stable sector positioning.

- **Implementation Example**: `ts_std_dev(ts_backfill({sector_exposure}, 66), 20)`