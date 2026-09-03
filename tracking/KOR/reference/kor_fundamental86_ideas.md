# fundamental86 GEM Ideas (KOR / TOP600 / delay1)

**Dataset**: fundamental86
**Region**: KOR
**Delay**: 1

**Concept**: Fundamental Quality Score Momentum
- **Mechanism**: Composite fundamental decile score (1-10) ranks firm quality; high-score firms drift upward as quality gets priced in slowly. expected_exposure: quality.
- **Fields**: `fnd86_fundamental_score`
- **Implementation Example**: `rank({fnd86_fundamental_score})`
- **Direction**: positive

**Concept**: Earnings Score Leadership
- **Mechanism**: Earnings sub-score captures near-term profitability; leaders in earnings quality outperform laggards. expected_exposure: quality/earnings.
- **Fields**: `fnd86_earnings_score`
- **Implementation Example**: `rank({fnd86_earnings_score})`
- **Direction**: positive

**Concept**: Composite Score, Sector Relative
- **Mechanism**: Average composite score ranked within sector isolates firm-level quality from industry beta. expected_exposure: sector-neutral quality.
- **Fields**: `fnd86_average_score`
- **Implementation Example**: `group_zscore({fnd86_average_score}, sector)`
- **Direction**: positive

**Concept**: Score Improvement Momentum (annual)
- **Mechanism**: Firms whose fundamental score improves over 252 days are on an upgrading trajectory; momentum in quality scores predicts continuation. expected_exposure: quality momentum.
- **Fields**: `fnd86_fundamental_score`
- **Implementation Example**: `rank(ts_delta({fnd86_fundamental_score}, 252))`
- **Direction**: positive

**Concept**: Earnings vs Fundamental Divergence
- **Mechanism**: When earnings score runs ahead of fundamental score, near-term profitability outpaces balance-sheet quality - an early upgrade signal. expected_exposure: earnings surprise quality.
- **Fields**: `fnd86_earnings_score`, `fnd86_fundamental_score`
- **Implementation Example**: `rank(subtract({fnd86_earnings_score}, {fnd86_fundamental_score}))`
- **Direction**: positive

**Concept**: Persistent High Quality (slow smoothing)
- **Mechanism**: Persistently high composite score over 252 days filters transient prints; structurally high-quality firms compound. expected_exposure: quality.
- **Fields**: `fnd86_average_score`
- **Implementation Example**: `rank(ts_mean({fnd86_average_score}, 252))`
- **Direction**: positive
