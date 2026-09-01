# IND Model144 Feature Engineering Ideas (Delay=1, TOP500)

**Dataset**: model144
**Region**: IND
**Delay**: 1


## Dataset Understanding

**Dataset**: model144 (Deep Learning Stock Selection)
**Fields**: 2 MATRIX fields, coverage=0.83, alphaCount=432
**Category**: Model/Deep Learning
**Description**: StarPerformer (wolfe_star) deep learning model output scores for stock selection.

## Field Deconstruction

### Core Fields (MATRIX, coverage=0.83)

1. **mdl144_score** (alphaCount=189)
   - Measures: Post-processed and normalized model score [0,1]
   - Economic meaning: DL model's stock attractiveness rating
   - Direction: Higher = more attractive
   - Type: Clipped/normalized score

2. **mdl144_predict** (alphaCount=246)
   - Measures: Raw output score from DL model
   - Economic meaning: Unprocessed model prediction
   - Direction: Higher = more attractive
   - Type: Raw model output

## Feature Engineering Concepts

### Concept 1: DL Score Momentum
**Concept**: Changes in DL model score capture shifts in model's assessment. Smoothing identifies sustained upgrades.

**Implementation Example**: `ts_mean(ts_backfill({mdl144_score}, 66), 15)`

**Rationale**: 15-day smoothing captures monthly trends in model assessment.

---

### Concept 2: Score-Predict Divergence
**Concept**: Divergence between normalized score and raw prediction indicates model confidence. Large divergence signals uncertainty.

**Implementation Example**: `subtract(ts_backfill({mdl144_score}, 66), ts_backfill({mdl144_predict}, 66))`

**Rationale**: Positive divergence indicates post-processing boosts score vs raw prediction.

---

### Concept 3: DL Score Acceleration
**Concept**: Acceleration in DL score changes identifies stocks with rapidly improving model assessment.

**Implementation Example**: `ts_delta(ts_backfill({mdl144_score}, 66), 10)`

**Rationale**: 10-day change captures recent shifts in model assessment.

---

### Concept 4: DL Score Volatility
**Concept**: Volatility in DL score indicates model uncertainty. Low volatility with high score signals stable conviction.

**Implementation Example**: `multiply(rank(ts_backfill({mdl144_score}, 66)), multiply(-1, ts_std_dev(ts_backfill({mdl144_score}, 66), 20)))`

**Rationale**: High score with low volatility (negative weight) indicates stable high conviction.

---

### Concept 5: DL Score Rank Persistence
**Concept**: Persistent high rank in DL score indicates sustained model conviction. Z-score normalizes persistence.

**Implementation Example**: `ts_zscore(rank(ts_backfill({mdl144_score}, 66)), 60)`

**Rationale**: 60-day z-score of rank identifies statistically significant persistence.

---

### Concept 6: Raw Prediction Momentum
**Concept**: Momentum in raw prediction captures model's changing assessment before post-processing.

**Implementation Example**: `ts_delta(ts_backfill({mdl144_predict}, 66), 10)`

**Rationale**: 10-day change in raw prediction captures recent model shifts.

---

### Concept 7: Score-Predict Interaction
**Concept**: Interaction between score and prediction amplifies when both align. Product captures this alignment.

**Implementation Example**: `multiply(ts_backfill({mdl144_score}, 66), ts_backfill({mdl144_predict}, 66))`

**Rationale**: Product amplifies when both normalized and raw scores are high.

---

### Concept 8: DL Score Second Derivative
**Concept**: Second derivative (acceleration of changes) identifies inflection points in model assessment.

**Implementation Example**: `ts_delta(ts_delta(ts_backfill({mdl144_score}, 66), 5), 5)`

**Rationale**: 5-day change of 5-day change captures acceleration in model upgrades.

---

## Preprocessing Decisions

Fields are MATRIX type with coverage 0.83:
- **ts_backfill(66)**: Fill gaps (important given 0.83 coverage)
- **No winsorize**: mdl144_score is already clipped [0,1]
- **rank/ts_zscore**: For cross-sectional normalization

## Field Whitelist

```json
[
  "mdl144_score",
  "mdl144_predict"
]
```

## Risk Considerations

- **Limited fields**: Only 2 fields available, limiting expression diversity.
- **Coverage 0.83**: Lower coverage may introduce bias. ts_backfill is critical.
- **DL model opacity**: Deep learning model is a black box. Monitor for regime shifts.
- **Single catalog**: Both fields from same dataset, satisfies 1-catalog constraint.