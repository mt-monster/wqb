# IND Model252 Feature Engineering Ideas (Delay=1, TOP500)

**Dataset**: model252
**Region**: IND
**Delay**: 1


## Dataset Understanding

**Dataset**: model252 (SHIELD Defensiveness)
**Fields**: 5 fields (2 MATRIX, 3 VECTOR), coverage=0.79, alphaCount=905
**Category**: Model/Risk/Quality
**Description**: SHIELD model output scores representing defensive (risk/quality) ratings for securities.

## Field Deconstruction

### Core Fields

**MATRIX Fields** (coverage=0.79):

1. **defensiveness_composite_score** (alphaCount=421)
   - Measures: SHIELD model composite defensive score [0,1]
   - Economic meaning: Overall defensive/quality rating
   - Direction: Higher = more defensive/lower risk

2. **total_equity_market_value_2** (alphaCount=422)
   - Measures: Market capitalization on score's effective date
   - Economic meaning: Company size
   - Direction: Higher = larger company
   - **Note**: High alphaCount suggests saturation

**VECTOR Fields** (coverage=0.785, require vec_* operators):

3. **mdl252_shield** (alphaCount=82)
   - Measures: Primary SHIELD composite risk/defense score [0,1]
   - Type: VECTOR (requires vec_avg, vec_std, etc.)

4. **mdl252_shield2** (alphaCount=66)
   - Measures: Auxiliary SHIELD composite score [0,1]
   - Type: VECTOR

5. **firm_market_value** (alphaCount=68)
   - Measures: Market capitalization
   - Type: VECTOR

## Feature Engineering Concepts

### Concept 1: Defensiveness Momentum
**Concept**: Changes in defensiveness score capture shifts in risk/quality assessment. Smoothing identifies sustained trends.

**Implementation Example**: `ts_mean(ts_backfill({defensiveness_composite_score}, 66), 15)`

**Rationale**: 15-day smoothing captures monthly defensiveness trends.

---

### Concept 2: Defensive Size Interaction
**Concept**: Large-cap defensive stocks are "quality anchors". Multiplicative interaction amplifies this combination.

**Implementation Example**: `multiply(rank(ts_backfill({defensiveness_composite_score}, 66)), rank(ts_backfill({total_equity_market_value_2}, 66)))`

**Rationale**: Product of ranks amplifies when both defensiveness and size are high.

---

### Concept 3: Defensiveness Acceleration
**Concept**: Acceleration in defensiveness changes identifies stocks rapidly improving risk profile.

**Implementation Example**: `ts_delta(ts_backfill({defensiveness_composite_score}, 66), 10)`

**Rationale**: 10-day change captures recent shifts in defensive assessment.

---

### Concept 4: Defensive Volatility
**Concept**: Volatility in defensiveness score indicates assessment uncertainty. Low volatility with high score signals stable quality.

**Implementation Example**: `multiply(rank(ts_backfill({defensiveness_composite_score}, 66)), multiply(-1, ts_std_dev(ts_backfill({defensiveness_composite_score}, 66), 20)))`

**Rationale**: High defensiveness with low volatility (negative weight) indicates stable quality.

---

### Concept 5: Defensive Rank Persistence
**Concept**: Persistent high rank in defensiveness indicates sustained quality. Z-score normalizes persistence.

**Implementation Example**: `ts_zscore(rank(ts_backfill({defensiveness_composite_score}, 66)), 60)`

**Rationale**: 60-day z-score of rank identifies statistically significant persistence.

---

### Concept 6: Size-Defensive Divergence
**Concept**: When defensiveness diverges from size, it signals quality independent of market cap. Spread captures this.

**Implementation Example**: `subtract(rank(ts_backfill({defensiveness_composite_score}, 66)), rank(ts_backfill({total_equity_market_value_2}, 66)))`

**Rationale**: Positive divergence indicates high defensiveness relative to size.

---

### Concept 7: Defensive Second Derivative
**Concept**: Second derivative (acceleration of changes) identifies inflection points in defensive assessment.

**Implementation Example**: `ts_delta(ts_delta(ts_backfill({defensiveness_composite_score}, 66), 5), 5)`

**Rationale**: 5-day change of 5-day change captures acceleration in defensive upgrades.

---

### Concept 8: Defensive Z-Score Breakout
**Concept**: Z-score breakout in defensiveness identifies statistically significant quality improvements.

**Implementation Example**: `ts_zscore(ts_backfill({defensiveness_composite_score}, 66), 60)`

**Rationale**: 60-day z-score identifies significant deviations from mean defensiveness.

---

## Preprocessing Decisions

**MATRIX fields** (coverage 0.79):
- **ts_backfill(66)**: Fill gaps (important given 0.79 coverage)
- **No winsorize**: defensiveness_composite_score is already bounded [0,1]
- **rank/ts_zscore**: For cross-sectional normalization

**VECTOR fields**: Require vec_* operators (vec_avg, vec_std, etc.) - not used in these concepts to keep expressions simple.

## Field Whitelist

```json
[
  "defensiveness_composite_score",
  "total_equity_market_value_2"
]
```

## Risk Considerations

- **total_equity_market_value_2**: High alphaCount (422) suggests saturation. Use in combination with defensiveness.
- **Coverage 0.79**: Lower coverage may introduce bias. ts_backfill is critical.
- **VECTOR fields**: mdl252_shield/shield2/firm_market_value require vec_* operators, adding complexity. Focus on MATRIX fields for simplicity.
- **Single catalog**: All fields from same dataset, satisfies 1-catalog constraint.