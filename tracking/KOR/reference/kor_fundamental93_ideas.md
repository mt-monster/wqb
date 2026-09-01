# fundamental93 GEM Ideas (KOR / TOP600 / delay1)

**Dataset**: fundamental93
**Region**: KOR
**Delay**: 1

**Concept**: Accrual Anomaly Short Leg
- **Mechanism**: High accruals indicate earnings inflated by non-cash items; Sloan (1996) documents that high-accrual firms underperform. expected_exposure: sector-neutral quality short leg.
- **Fields**: `fnd93_accruals_d1_current_t` (z-score of current accruals ratio vs LTM)
- **Implementation Example**: `multiply(-1, rank({fnd93_accruals_d1_current_t}))`
- **Direction**: negative (short high accruals)

**Concept**: Tax Accrual Aggressiveness
- **Mechanism**: Tax expense minus cash tax paid captures aggressive accrual management via tax accounts; persistent high values flag earnings manipulation risk. expected_exposure: quality.
- **Fields**: `fnd93_tax_accruals_11`
- **Implementation Example**: `multiply(-1, rank({fnd93_tax_accruals_11}))`
- **Direction**: negative

**Concept**: Asset Growth Anomaly
- **Mechanism**: Firms expanding assets rapidly (Cooper et al. asset growth anomaly) tend to underperform; YoY asset change ratio is the carrier. expected_exposure: size/quality blend.
- **Fields**: `fnd93_accrualsratio_d1_asset_change`
- **Implementation Example**: `multiply(-1, rank({fnd93_accrualsratio_d1_asset_change}))`
- **Direction**: negative

**Concept**: Accrual Instability Penalty
- **Mechanism**: High LTM volatility of the accruals ratio signals unstable reporting quality and unreliable earnings; investors underprice the risk. expected_exposure: low-vol/quality.
- **Fields**: `fnd93_accruals_d1_dts`
- **Implementation Example**: `multiply(-1, rank({fnd93_accruals_d1_dts}))`
- **Direction**: negative

**Concept**: Deferred Tax Expense Red Flag, Sector Relative
- **Mechanism**: Elevated deferred tax expense ratios indicate book-tax divergence; rank within sector isolates firm-level quality from industry tax regimes. expected_exposure: sector-neutral quality.
- **Fields**: `fnd93_deferred_tax_expense_11`
- **Implementation Example**: `multiply(-1, group_zscore({fnd93_deferred_tax_expense_11}, sector))`
- **Direction**: negative

**Concept**: Persistent Tax Accrual Level (LTM smoothing)
- **Mechanism**: A persistent high level of tax accruals over 252 days filters one-off items and identifies structurally aggressive reporters. expected_exposure: quality.
- **Fields**: `fnd93_tax_accruals_31`
- **Implementation Example**: `multiply(-1, rank(ts_mean({fnd93_tax_accruals_31}, 252)))`
- **Direction**: negative

**Concept**: Deferred Tax Liability Surprise vs Own History
- **Mechanism**: Current deferred tax liability far above its own trailing window (z-score) marks fresh book-tax divergence events. expected_exposure: quality/momentum blend.
- **Fields**: `fnd93_liability_d1_current_t`
- **Implementation Example**: `multiply(-1, rank({fnd93_liability_d1_current_t}))`
- **Direction**: negative

**Concept**: Accrual Mean Reversion Gap
- **Mechanism**: When the current accruals t-statistic spikes above the LTM mean, the ratio tends to revert; fading extreme prints captures the reversion. expected_exposure: quality/mean-reversion.
- **Fields**: `fnd93_accruals_d1_current_t`, `fnd93_accruals_d1_mean`
- **Implementation Example**: `multiply(-1, rank(subtract({fnd93_accruals_d1_current_t}, ts_mean({fnd93_accruals_d1_mean}, 252))))`
- **Direction**: negative
