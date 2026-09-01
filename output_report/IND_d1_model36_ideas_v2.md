# IND Model36 Feature Engineering Ideas (Delay=1, TOP500)

**Dataset**: model36
**Region**: IND
**Delay**: 1


## Dataset Understanding

**Dataset**: model36 (SmartRatios Credit Risk)
**Fields**: 42 MATRIX fields, coverage=0.98, alphaCount=1868
**Category**: Model/Credit Risk
**Description**: SmartRatios credit risk model scores measuring default probability across multiple dimensions (coverage, growth, leverage, liquidity, profitability).

## Field Deconstruction

### Credit Risk Component Scores (Float Percentile 0-100)

**Coverage**:
- `credit_risk_coverage_score_main` (alphaCount=59): Ability to cover interest/debt
- `star_sr_coverage` (alphaCount=56): Coverage percentile rank

**Growth**:
- `credit_risk_growth_score_main` (alphaCount=29): Growth/stability factors
- `star_sr_growth` (alphaCount=55): Growth percentile rank

**Leverage**:
- `credit_risk_leverage_score_main` (alphaCount=30): Leverage factors
- `star_sr_leverage` (alphaCount=46): Leverage percentile rank

**Liquidity**:
- `credit_risk_liquidity_score_main` (alphaCount=15): Liquidity factors
- `star_sr_liquidity` (alphaCount=26): Liquidity percentile rank

**Profitability**:
- `credit_risk_profitability_score_main` (alphaCount=34): Profitability factors
- `star_sr_profitability` (alphaCount=73): Profitability percentile rank

### Default Risk Percentiles (Higher = Lower Risk)

- `default_risk_global_percentile_main` (alphaCount=71): Global default risk rank
- `default_risk_country_percentile_main` (alphaCount=63): Country default risk rank
- `default_risk_region_percentile_main` (alphaCount=49): Regional default risk rank
- `default_risk_industry_percentile_main` (alphaCount=42): Industry default risk rank
- `default_risk_sector_percentile_main` (alphaCount=38): Sector default risk rank

### Star SR Ranks (Integer 1-100, Higher = Lower Risk)

- `star_sr_global_rank` (alphaCount=73): Global credit quality rank
- `star_sr_country_rank` (alphaCount=143): Country credit quality rank
- `star_sr_region_rank` (alphaCount=64): Regional credit quality rank
- `star_sr_sector_rank` (alphaCount=83): Sector credit quality rank
- `star_sr_industr_rank` (alphaCount=39): Industry credit quality rank

## Feature Engineering Concepts

### Concept 1: Credit Quality Momentum
**Concept**: Improving credit quality (rising star_sr_global_rank) signals strengthening fundamentals. Smoothing captures sustained improvement.

**Implementation Example**: `ts_mean(ts_backfill({star_sr_global_rank}, 66), 15)`

**Rationale**: 15-day smoothing captures monthly credit quality trends.

---

### Concept 2: Profitability-Leverage Interaction
**Concept**: Strong profitability with low leverage indicates high-quality balance sheet. Multiplicative interaction amplifies this combination.

**Implementation Example**: `multiply(ts_backfill({star_sr_profitability}, 66), ts_backfill({star_sr_leverage}, 66))`

**Rationale**: Product amplifies when both profitability and leverage scores are high (low risk).

---

### Concept 3: Coverage-Growth Divergence
**Concept**: When coverage (ability to service debt) diverges from growth, it signals financial stability vs growth trade-off.

**Implementation Example**: `subtract(ts_backfill({star_sr_coverage}, 66), ts_backfill({star_sr_growth}, 66))`

**Rationale**: Positive divergence indicates strong debt coverage relative to growth.

---

### Concept 4: Global-Country Credit Spread
**Concept**: Spread between global and country credit ranks identifies stocks with strong global standing relative to domestic peers.

**Implementation Example**: `subtract(ts_backfill({star_sr_global_rank}, 66), ts_backfill({star_sr_country_rank}, 66))`

**Rationale**: Positive spread indicates global credit strength exceeding country-level strength.

---

### Concept 5: Default Risk Industry Leadership
**Concept**: Stocks with low default risk relative to industry peers are sector leaders in credit quality.

**Implementation Example**: `rank(ts_backfill({default_risk_industry_percentile_main}, 66))`

**Rationale**: Cross-sectional rank identifies industry credit quality leaders.

---

### Concept 6: Liquidity-Profitability Balance
**Concept**: Balance between liquidity and profitability indicates financial flexibility. Delta captures shifts in this balance.

**Implementation Example**: `ts_delta(subtract(ts_backfill({star_sr_liquidity}, 66), ts_backfill({star_sr_profitability}, 66)), 10)`

**Rationale**: 10-day change in liquidity-profitability spread captures balance shifts.

---

### Concept 7: Credit Risk Sector Relative Strength
**Concept**: Sector-relative credit rank identifies stocks with strong credit within their sector. Z-score normalizes across time.

**Implementation Example**: `ts_zscore(ts_backfill({star_sr_sector_rank}, 66), 60)`

**Rationale**: 60-day z-score identifies statistically significant sector credit strength.

---

### Concept 8: Multi-Dimensional Credit Quality
**Concept**: Combining coverage, profitability, and leverage creates a composite credit quality score. Product amplifies when all dimensions align.

**Implementation Example**: `multiply(multiply(ts_backfill({star_sr_coverage}, 66), ts_backfill({star_sr_profitability}, 66)), ts_backfill({star_sr_leverage}, 66))`

**Rationale**: Three-way product amplifies when all credit dimensions show strength.

---

## Preprocessing Decisions

All fields are MATRIX type with coverage 0.98:
- **ts_backfill(66)**: Fill gaps (standard practice)
- **No winsorize**: Percentile scores are already bounded [0,100]
- **rank/ts_zscore**: For cross-sectional normalization

## Field Whitelist

```json
[
  "star_sr_global_rank",
  "star_sr_country_rank",
  "star_sr_region_rank",
  "star_sr_sector_rank",
  "star_sr_coverage",
  "star_sr_growth",
  "star_sr_leverage",
  "star_sr_liquidity",
  "star_sr_profitability",
  "default_risk_global_percentile_main",
  "default_risk_country_percentile_main",
  "default_risk_industry_percentile_main"
]
```

## Risk Considerations

- **star_sr_country_rank**: High alphaCount (143) suggests potential saturation. Use in combination.
- **Credit risk in IND**: IND market may have different credit dynamics than developed markets. Monitor for regime shifts.
- **Single catalog**: All fields from same dataset, satisfies 1-catalog constraint.