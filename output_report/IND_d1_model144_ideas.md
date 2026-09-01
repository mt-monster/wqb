# IND model144 — DL Stock Selection — S1 Ideas

**Dataset**: model144
**Region**: IND
**Delay**: 1


**Dataset**: model144 | **Region**: IND | **Delay**: 1 | **Universe**: TOP500
**Fields**: 2 MATRIX | **Coverage**: 0.83 | **alphaCount**: 432

---

## Concept 1: DL Score Momentum

**Concept**: Deep learning stock selection score momentum captures the trajectory of ML model confidence. Rising DL score signals increasing model conviction.

- **Implementation Example**: `ts_delta(ts_backfill({mdl144_score}, 66), 10)`

## Concept 2: DL Score Volatility

**Concept**: Volatility of DL score captures model uncertainty. Low volatility = stable conviction; high volatility = model disagreement.

- **Implementation Example**: `ts_std_dev(ts_backfill({mdl144_score}, 66), 20)`

## Concept 3: DL Score Rank

**Concept**: Cross-sectional rank of DL score identifies relative ML conviction within universe. High rank = strongest model signal.

- **Implementation Example**: `rank(ts_backfill({mdl144_score}, 66))`

## Concept 4: DL Score Acceleration

**Concept**: Acceleration of DL score captures second-order model dynamics. Positive acceleration = strengthening signal.

- **Implementation Example**: `ts_delta(ts_delta(ts_backfill({mdl144_score}, 66), 5), 5)`

## Concept 5: Smoothed DL Score Trend

**Concept**: Smoothed DL score filters noise and captures persistent model conviction trend.

- **Implementation Example**: `ts_mean(ts_backfill({mdl144_score}, 66), 15)`

## Concept 6: DL Score Z-Score

**Concept**: Z-score of DL score captures statistical extremity of model signal. Extreme values = high conviction opportunities.

- **Implementation Example**: `ts_zscore(ts_backfill({mdl144_score}, 66), 60)`

## Concept 7: DL Raw Predict Momentum

**Concept**: Momentum of raw DL prediction captures unprocessed model signal trajectory. Complements processed score momentum.

- **Implementation Example**: `ts_delta(ts_backfill({mdl144_predict}, 66), 10)`

## Concept 8: DL Score-Predict Divergence

**Concept**: Divergence between processed score and raw prediction captures post-processing effects. Wide divergence = heavy normalization.

- **Implementation Example**: `subtract(ts_backfill({mdl144_score}, 66), ts_backfill({mdl144_predict}, 66))`