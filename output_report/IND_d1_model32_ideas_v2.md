# IND Model32 Feature Engineering Ideas (Delay=1, TOP500)

**Dataset**: model32
**Region**: IND
**Delay**: 1


## Dataset Understanding

**Dataset**: model32 (Price Momentum)
**Fields**: 36 MATRIX fields, coverage=0.96-0.98, alphaCount=6587
**Category**: Model/Price Momentum
**Description**: Multi-horizon price momentum scores across global, regional, industry, and time-frame dimensions.

## Field Deconstruction

### Core Momentum Fields (Float Percentile 0-100)

**Global Momentum**:
- `backfill_global_momentum_rank_float` (alphaCount=276): Global peer-relative momentum
- `global_momentum_rank_float` (alphaCount=109): Overall global momentum
- `d1_global_momentum_rank_float` (alphaCount=118): Daily variant

**Regional Momentum**:
- `backfill_regional_momentum_rank_float` (alphaCount=78): Asia regional momentum
- `regional_momentum_rank_float` (alphaCount=51): Regional momentum
- `d1_regional_momentum_rank_float` (alphaCount=58): Daily variant

**Industry Momentum**:
- `backfill_industry_momentum_score_float` (alphaCount=138): Industry-relative momentum
- `industry_momentum_score_float` (alphaCount=98): Industry momentum
- `d1_industry_momentum_score_float` (alphaCount=75): Daily variant

**Time-Horizon Momentum**:
- `backfill_short_term_momentum_score_float` (alphaCount=852): ~1 week momentum
- `backfill_mid_term_momentum_score_float` (alphaCount=117): ~3-6 months momentum
- `backfill_long_term_momentum_score_float` (alphaCount=161): ~12 months momentum
- `short_horizon_momentum_score_float` (alphaCount=1987): Short-term (HIGH SATURATION)
- `mid_horizon_momentum_score_float` (alphaCount=34): Mid-term
- `long_horizon_momentum_score_float` (alphaCount=39): Long-term

**Star PM Ranks** (Integer 1-100):
- `star_pm_global_rank` (alphaCount=62): Global momentum rank
- `star_pm_shortterm` (alphaCount=232): Short-term momentum rank
- `star_pm_midterm` (alphaCount=39): Mid-term momentum rank
- `star_pm_longterm` (alphaCount=34): Long-term momentum rank

## Feature Engineering Concepts

### Concept 1: Short-Term Momentum Reversal
**Concept**: Short-term momentum in IND market tends to reverse. Fading extreme short-term momentum captures mean reversion.

**Implementation Example**: `multiply(-1, rank(ts_backfill({backfill_short_term_momentum_score_float}, 66)))`

**Rationale**: Negative rank fades high short-term momentum stocks, capturing reversal alpha.

---

### Concept 2: Global-Regional Momentum Divergence
**Concept**: When global momentum diverges from regional momentum, it signals stock-specific strength independent of regional trends.

**Implementation Example**: `subtract(ts_backfill({backfill_global_momentum_rank_float}, 66), ts_backfill({backfill_regional_momentum_rank_float}, 66))`

**Rationale**: Positive divergence indicates stock outperforming both global and regional peers.

---

### Concept 3: Industry Momentum Leadership
**Concept**: Stocks with strong industry-relative momentum are sector leaders. Ranking this metric identifies industry outperformance.

**Implementation Example**: `rank(ts_backfill({backfill_industry_momentum_score_float}, 66))`

**Rationale**: Cross-sectional rank of industry momentum identifies sector leaders.

---

### Concept 4: Multi-Horizon Momentum Alignment
**Concept**: When short, mid, and long-term momentum align, it signals sustained trend strength. Multiplicative interaction amplifies aligned signals.

**Implementation Example**: `multiply(multiply(ts_backfill({backfill_short_term_momentum_score_float}, 66), ts_backfill({backfill_mid_term_momentum_score_float}, 66)), ts_backfill({backfill_long_term_momentum_score_float}, 66))`

**Rationale**: Product of three horizons amplifies when all timeframes show positive momentum.

---

### Concept 5: Mid-Long Term Momentum Spread
**Concept**: Spread between mid-term and long-term momentum captures acceleration in trend. Widening spread indicates strengthening trend.

**Implementation Example**: `subtract(ts_backfill({backfill_mid_term_momentum_score_float}, 66), ts_backfill({backfill_long_term_momentum_score_float}, 66))`

**Rationale**: Positive spread indicates mid-term momentum accelerating vs long-term.

---

### Concept 6: Star PM Global Rank Momentum
**Concept**: Star PM global rank is a curated momentum score. Smoothing over medium term captures sustained global outperformance.

**Implementation Example**: `ts_mean(ts_backfill({star_pm_global_rank}, 66), 15)`

**Rationale**: 15-day smoothing filters noise while capturing monthly momentum trends.

---

### Concept 7: Short-Mid Term Momentum Rotation
**Concept**: Rotation from short-term to mid-term momentum indicates trend maturation. Delta captures this transition.

**Implementation Example**: `subtract(rank(ts_backfill({backfill_short_term_momentum_score_float}, 66)), rank(ts_backfill({backfill_mid_term_momentum_score_float}, 66)))`

**Rationale**: Rank difference identifies stocks transitioning from short to mid-term strength.

---

### Concept 8: Regional Momentum Persistence
**Concept**: Regional momentum that persists over time signals sustained regional outperformance. Z-score normalizes the metric.

**Implementation Example**: `ts_zscore(ts_backfill({backfill_regional_momentum_rank_float}, 66), 60)`

**Rationale**: 60-day z-score identifies statistically significant regional momentum deviations.

---

## Preprocessing Decisions

All fields are MATRIX type with coverage 0.96-0.98:
- **ts_backfill(66)**: Fill gaps (standard practice)
- **No winsorize**: Percentile scores are already bounded [0,100]
- **rank/ts_zscore**: For cross-sectional normalization

## Field Whitelist

```json
[
  "backfill_global_momentum_rank_float",
  "backfill_regional_momentum_rank_float",
  "backfill_industry_momentum_score_float",
  "backfill_short_term_momentum_score_float",
  "backfill_mid_term_momentum_score_float",
  "backfill_long_term_momentum_score_float",
  "star_pm_global_rank",
  "star_pm_shortterm",
  "star_pm_midterm",
  "star_pm_longterm"
]
```

## Risk Considerations

- **short_horizon_momentum_score_float**: Very high alphaCount (1987) indicates severe saturation. Avoid standalone use.
- **backfill_short_term_momentum_score_float**: High alphaCount (852) suggests crowding. Use in combination or with reversal logic.
- **Momentum reversal**: IND market shows short-term momentum reversal. Consider negative weights for short-term momentum.
- **Single catalog**: All fields from same dataset, satisfies 1-catalog constraint.