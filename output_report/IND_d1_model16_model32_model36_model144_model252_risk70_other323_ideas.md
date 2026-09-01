# IND Region Feature Engineering Ideas — S1 Output

**Dataset**: model16
**Region**: IND
**Delay**: 1

# Region: IND | Universe: TOP500 | Delay: 1 | Generated: 2026-08-30
# Datasets: model16, model32, model36, model144, model252, risk70, other323

---

## Dataset 1: model16 — Fundamental Scores (Derivative)
**Category**: model | **Fields**: 8 MATRIX | **Coverage**: 1.0 | **alphaCount**: 936 | **pm**: 1.2

### Field Deconstruction
| Field | What it measures | Time dimension | Business context |
|-------|-----------------|----------------|------------------|
| analyst_revision_rank_derivative | Daily-indicator variant of momentum capturing recent price moves and analyst estimate revisions | Daily change | Analyst sentiment momentum |
| cashflow_efficiency_rank_derivative | Ranks stocks by ability to generate cash flows and operational profitability | Daily change | Operational efficiency |
| composite_factor_score_derivative | Momentum score based on analyst revisions; intraday variant | Daily change | Composite signal momentum |
| earnings_certainty_rank_derivative | Measures sustainability and certainty of earnings quality | Daily change | Earnings predictability |
| growth_potential_rank_derivative | Composite growth score qualifying expected medium-term growth potential | Daily change | Growth expectations |
| multi_factor_acceleration_score_derivative | Change in acceleration of multi-factor score vs previous period | Daily change | Factor momentum acceleration |
| multi_factor_static_score_derivative | Change in static multi-factor score vs previous period | Daily change | Factor level shift |
| relative_valuation_rank_derivative | Assesses whether stock is under/overpriced based on standard valuation multiples | Daily change | Valuation re-rating |

### Key Observations
- All fields are **derivative/change** versions of base scores — they capture **transitions**, not levels
- Coverage = 1.0 (full universe), alphaCount = 936 (moderate competition)
- The "derivative" suffix means these are already first-differences; we need **second-order** or **smoothed** signals

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **Revision Momentum Persistence** = ts_mean(analyst_revision_rank_derivative, 10)
   - Meaning: Is analyst revision momentum sustained or one-off?
   - Direction: High = persistent upward revision trend
   - Economic logic: Persistent revisions signal fundamental improvement, not noise

2. **Growth-Valuation Divergence** = growth_potential_rank_derivative - relative_valuation_rank_derivative
   - Meaning: Is growth accelerating while valuation re-rating lags?
   - Direction: Positive = growth improving faster than valuation (opportunity)
   - Economic logic: Growth-valuation gap predicts future re-rating

3. **Earnings Certainty Shift** = ts_delta(earnings_certainty_rank_derivative, 5)
   - Meaning: Is earnings predictability improving or deteriorating?
   - Direction: Positive = improving certainty (lower risk premium)
   - Economic logic: Certainty improvement reduces cost of capital

#### Q4: What is combined? (Interaction)
4. **Cashflow-Growth Synergy** = cashflow_efficiency_rank_derivative * growth_potential_rank_derivative
   - Meaning: Are cash generation and growth improving together?
   - Direction: Positive = healthy growth (cash-backed), Negative = growth without cash (risky)
   - Economic logic: Cash-backed growth is sustainable; cashless growth is fragile

5. **Multi-Factor Acceleration-Revision Alignment** = multi_factor_acceleration_score_derivative * analyst_revision_rank_derivative
   - Meaning: Is factor momentum acceleration aligned with analyst revisions?
   - Direction: Positive = confirmed momentum, Negative = conflicting signals
   - Economic logic: Alignment confirms signal strength; conflict warns of reversal

#### Q7: What is relative? (Comparison)
6. **Composite Score Momentum Rank** = rank(composite_factor_score_derivative)
   - Meaning: Cross-sectional rank of composite momentum
   - Direction: High = strongest momentum in universe
   - Economic logic: Relative momentum outperforms absolute in cross-section

### Preprocessing Decisions
- All fields: `ts_backfill(x, 66)` for gap filling (daily updates expected)
- Derivative fields: `ts_mean(x, 10)` to smooth noise (daily changes are noisy)
- Rank-based: `rank(x)` for cross-sectional comparability
- No winsorize needed (scores are already bounded/percentile-like)

---

## Dataset 2: model32 — Price Momentum Model
**Category**: model | **Fields**: 36 MATRIX | **Coverage**: 0.96 | **alphaCount**: 6587 | **pm**: 1.2

### Field Deconstruction
| Field Group | Fields | What they measure |
|-------------|--------|-------------------|
| Global momentum | backfill_global_momentum_rank, d1_global_momentum_rank_float, global_momentum_rank_float, star_pm_global_rank, star_pm_global_rank_d1 | Price momentum vs global peers (percentile 1-100) |
| Regional momentum | backfill_regional_momentum_rank, d1_regional_momentum_rank_float, regional_momentum_rank_float, star_pm_region_rank, star_pm_region_rank_d1 | Price momentum vs regional (Asia) peers |
| Industry momentum | backfill_industry_momentum_score, d1_industry_momentum_score_float, industry_momentum_score_float, star_pm_industry, star_pm_industry_d1 | Price momentum vs TRBC industry peers |
| Time-horizon momentum | backfill_long/mid/short_term_momentum_score, d1_*_float, star_pm_long/mid/shortterm* | Momentum at different horizons (long=12M, mid=3-6M, short=1W) |

### Key Observations
- **alphaCount = 6587** — high competition, but momentum is a proven signal family
- Multiple horizons and peer groups allow **cross-sectional spread** construction
- IND region: momentum has been partially validated (model32 not in dead_ends, but pv-based momentum families have mixed results)
- **prod_risk**: Momentum is a common signal — need **structural differentiation** (horizon spread, peer-group spread) to avoid prod_corr saturation

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **Momentum Horizon Spread** = long_term_momentum_score_float - short_term_momentum_score_float
   - Meaning: Is long-term momentum stronger than short-term (trend) or vice versa (reversal)?
   - Direction: Positive = established trend, Negative = short-term reversal
   - Economic logic: Horizon spread captures trend maturity; wide spread = late-stage trend

2. **Momentum Acceleration** = ts_delta(short_term_momentum_score_float, 5)
   - Meaning: Is short-term momentum accelerating?
   - Direction: Positive = momentum building, Negative = momentum fading
   - Economic logic: Acceleration predicts continuation; deceleration predicts reversal

#### Q4: What is combined? (Interaction)
3. **Global-Industry Momentum Divergence** = global_momentum_rank_float - industry_momentum_score_float
   - Meaning: Is stock moving with global peers or diverging from industry?
   - Direction: Positive = global leader, Negative = industry laggard
   - Economic logic: Global-industry divergence signals idiosyncratic strength

4. **Regional-Global Momentum Ratio** = regional_momentum_rank_float / (global_momentum_rank_float + 1)
   - Meaning: Is regional momentum leading or lagging global momentum?
   - Direction: >1 = regional outperformance, <1 = regional underperformance
   - Economic logic: Regional leadership predicts local fund flows

#### Q7: What is relative? (Comparison)
5. **Industry-Relative Momentum Rank** = rank(industry_momentum_score_float) - rank(global_momentum_rank_float)
   - Meaning: Industry rank vs global rank spread
   - Direction: Positive = industry leader but global laggard (contrarian opportunity)
   - Economic logic: Industry-global rank spread captures sector rotation timing

6. **Short-Long Momentum Cross-Sectional Spread** = rank(short_term_momentum_score_float) - rank(long_term_momentum_score_float)
   - Meaning: Cross-sectional short vs long momentum spread
   - Direction: Positive = short-term strength dominating (reversal risk)
   - Economic logic: Cross-sectional horizon spread predicts mean reversion

### Preprocessing Decisions
- All fields: `ts_backfill(x, 66)` (coverage 0.96, minor gaps)
- Percentile scores: `rank(x)` for cross-sectional normalization
- Horizon spreads: direct subtraction (same scale 0-100)
- No winsorize needed (percentile scores are bounded)

---

## Dataset 3: model36 — SmartRatios Credit Risk Model
**Category**: model | **Fields**: 42 MATRIX | **Coverage**: 0.98 | **alphaCount**: 1868 | **pm**: 1.2

### Field Deconstruction
| Field Group | Fields | What they measure |
|-------------|--------|-------------------|
| Credit risk components | credit_risk_coverage/growth/leverage/liquidity/profitability_score_* | Percentile scores (0-100) for credit risk sub-components |
| Default risk percentiles | default_risk_country/global/industry/region/sector_percentile_* | 1-year default probability percentile within peer group |
| SmartRatios ranks | star_sr_country/global/industry/region/sector_rank, star_sr_coverage/growth/leverage/liquidity/profitability | SmartRatios percentile ranks (1-100, higher = lower risk) |

### Key Observations
- **Credit risk is a dead family in IND** (model192 CDS dead, quant_factor_lib CASSIE dead, model36 not explicitly dead but same family)
- However: model36 is **SmartRatios** (different methodology from CDS/CASSIE), and **default risk percentile** is a ranking, not a raw score
- **prod_risk**: Credit risk signals may correlate with value/quality factors already in prod pool
- **Key differentiation**: Use **relative credit improvement** (change in percentile) rather than level

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **Credit Quality Improvement** = ts_delta(star_sr_global_rank, 21)
   - Meaning: Is global credit rank improving over past month?
   - Direction: Positive = improving creditworthiness, Negative = deteriorating
   - Economic logic: Credit improvement reduces risk premium, boosts valuation

2. **Leverage-Coverage Spread Shift** = ts_delta(credit_risk_leverage_score_main - credit_risk_coverage_score_main, 10)
   - Meaning: Is leverage improving faster than coverage (risky) or vice versa (safe)?
   - Direction: Positive = leverage improving faster (risk building), Negative = coverage improving (safe)
   - Economic logic: Leverage-coverage divergence predicts credit stress

#### Q4: What is combined? (Interaction)
3. **Profitability-Leverage Credit Synergy** = credit_risk_profitability_score_main * credit_risk_leverage_score_main
   - Meaning: Are profitability and leverage improving together?
   - Direction: High = strong credit (profitable + low leverage), Low = weak credit
   - Economic logic: Profitability-leverage synergy captures credit quality holistically

4. **Industry-Global Credit Divergence** = star_sr_industr_rank - star_sr_global_rank
   - Meaning: Is company credit improving vs industry but lagging globally?
   - Direction: Positive = industry leader, Negative = industry laggard
   - Economic logic: Industry-relative credit strength predicts sector rotation

#### Q7: What is relative? (Comparison)
5. **Country-Global Credit Spread** = star_sr_country_rank - star_sr_global_rank
   - Meaning: Country rank vs global rank spread
   - Direction: Positive = country leader (local champion), Negative = global leader (export competitiveness)
   - Economic logic: Country-global spread captures local vs international competitiveness

### Preprocessing Decisions
- All fields: `ts_backfill(x, 66)` (coverage 0.98, minimal gaps)
- Percentile scores: `ts_delta(x, 21)` for monthly change, `rank(x)` for cross-sectional
- No winsorize needed (percentile scores bounded)

---

## Dataset 4: model144 — Stock Selection DL Model
**Category**: model | **Fields**: 2 MATRIX | **Coverage**: 0.83 | **alphaCount**: 432 | **pm**: 1.2

### Field Deconstruction
| Field | What it measures | Time dimension | Business context |
|-------|-----------------|----------------|------------------|
| mdl144_predict | Raw output score from StarPerformer (wolfe_star) deep learning model | Daily | DL alpha signal |
| mdl144_score | Post-processed and normalized model score, clipped to [0,1] | Daily | Systematic alpha signal |

### Key Observations
- **Only 2 fields** — limited but focused (deep learning stock selection)
- Coverage 0.83 (acceptable), alphaCount 432 (low competition)
- **prod_risk**: DL model scores may correlate with existing ML/AI signals in prod pool
- **Key differentiation**: Use **score dynamics** (change, volatility) rather than level

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **DL Score Momentum** = ts_delta(mdl144_score, 5)
   - Meaning: Is DL model score improving?
   - Direction: Positive = model upgrading stock, Negative = downgrading
   - Economic logic: Score momentum predicts near-term performance

2. **DL Score Volatility** = ts_std_dev(mdl144_score, 21)
   - Meaning: How stable is the DL model's assessment?
   - Direction: High = uncertain/volatile signal, Low = confident/stable signal
   - Economic logic: Low volatility signals high conviction; high volatility signals noise

#### Q4: What is combined? (Interaction)
3. **Raw-Normalized Score Divergence** = mdl144_predict - mdl144_score
   - Meaning: How much does normalization change the raw signal?
   - Direction: Large divergence = extreme raw score (clipped), Small = normal range
   - Economic logic: Divergence captures tail behavior of DL model

### Preprocessing Decisions
- `ts_backfill(x, 66)` for gap filling (coverage 0.83)
- `ts_delta(x, 5)` for weekly momentum, `ts_std_dev(x, 21)` for monthly volatility
- `rank(x)` for cross-sectional normalization

---

## Dataset 5: model252 — SHIELD Defensiveness Model
**Category**: model | **Fields**: 5 (3 MATRIX + 2 VECTOR) | **Coverage**: 0.79 | **alphaCount**: 905 | **pm**: 1.2

### Field Deconstruction
| Field | What it measures | Time dimension | Business context |
|-------|-----------------|----------------|------------------|
| defensiveness_composite_score | SHIELD model output score for defensive (risk/quality) rating (0-1) | Daily | Defensive stock selection |
| mdl252_shield | Primary SHIELD composite risk/defense score (0-1) | Daily | Risk/defense composite |
| mdl252_shield2 | Auxiliary/alternate SHIELD risk/defense score (0-1) | Daily | Alternate risk measure |
| firm_market_value | Market capitalization | Daily | Size factor |
| total_equity_market_value_2 | Market capitalization on score's effective date | Daily | Size factor (alternate) |

### Key Observations
- **Defensiveness/quality** is a proven factor, but IND has seen quality families fail (fnd44/90)
- **Differentiation**: SHIELD is a **composite risk/defense** score, not pure quality — may have different dynamics
- Coverage 0.79 (acceptable), alphaCount 905 (moderate competition)
- **Key insight**: Use **defensiveness change** and **size interaction** rather than level

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **Defensiveness Momentum** = ts_delta(defensiveness_composite_score, 10)
   - Meaning: Is stock becoming more defensive?
   - Direction: Positive = increasing defensiveness (flight to quality), Negative = decreasing
   - Economic logic: Defensiveness momentum predicts risk-off rotation

2. **Shield Score Convergence** = mdl252_shield - mdl252_shield2
   - Meaning: Are primary and alternate shield scores converging?
   - Direction: Near zero = consistent signal, Large divergence = model uncertainty
   - Economic logic: Convergence confirms signal; divergence warns of model risk

#### Q4: What is combined? (Interaction)
3. **Defensiveness-Size Interaction** = defensiveness_composite_score * rank(firm_market_value)
   - Meaning: Is defensiveness concentrated in large caps?
   - Direction: High = large-cap defensive (institutional flight), Low = small-cap defensive (retail flight)
   - Economic logic: Size-defensiveness interaction captures different investor behaviors

### Preprocessing Decisions
- `ts_backfill(x, 66)` for gap filling (coverage 0.79)
- `ts_delta(x, 10)` for bi-weekly momentum
- `rank(x)` for cross-sectional normalization

---

## Dataset 6: risk70 — Multi-Factor Risk Model
**Category**: risk | **Fields**: 35 MATRIX | **Coverage**: 1.0 | **alphaCount**: 3816 | **pm**: 1.0

### Field Deconstruction
| Field Group | Fields | What they measure |
|-------------|--------|-------------------|
| Market cap | apacm6_total_market_cap_usd, current_market_cap_usd | Total market capitalization |
| Hedge fund ownership | hedge_fund_number_owners, hedge_fund_ownership_percentage | Hedge fund ownership metrics |
| Sector exposures | sector_exposure_* (18 sectors) | Exposure to sector risk factors |
| Market exposure | broad_market_exposure_factor | Exposure to overall market factor |
| Momentum | sector_relative_momentum | Momentum relative to sector peers |
| Industry/Country factor | short_term_industry_country_factor | Short-term industry+country exposure |
| US flags | us_equity_*_flag, us_equity_short_interest_ratio | US-specific indicators (limited relevance for IND) |

### Key Observations
- **Risk model exposures** are typically used for **neutralization**, not alpha generation
- However: **sector exposure changes** and **hedge fund ownership dynamics** can be alpha signals
- Coverage = 1.0 (full), alphaCount = 3816 (high competition)
- **Key differentiation**: Use **exposure changes** and **ownership dynamics**, not raw exposures

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **Sector Exposure Shift** = ts_delta(sector_exposure_banking_2, 21)
   - Meaning: Is banking sector exposure increasing?
   - Direction: Positive = increasing banking exposure (sector rotation), Negative = decreasing
   - Economic logic: Sector exposure shifts predict sector performance

2. **Hedge Fund Ownership Momentum** = ts_delta(hedge_fund_ownership_percentage, 21)
   - Meaning: Are hedge funds increasing ownership?
   - Direction: Positive = hedge fund accumulation (smart money), Negative = distribution
   - Economic logic: Hedge fund ownership momentum predicts institutional sentiment

#### Q4: What is combined? (Interaction)
3. **Sector Momentum-Exposure Alignment** = sector_relative_momentum * sector_exposure_banking_2
   - Meaning: Is sector momentum aligned with sector exposure?
   - Direction: Positive = momentum + exposure aligned (trend confirmation), Negative = divergence
   - Economic logic: Alignment confirms sector trend; divergence warns of reversal

4. **Hedge Fund Concentration** = hedge_fund_ownership_percentage / (hedge_fund_number_owners + 1)
   - Meaning: Average ownership per hedge fund
   - Direction: High = concentrated ownership (conviction), Low = dispersed ownership
   - Economic logic: Concentration signals conviction; dispersion signals uncertainty

### Preprocessing Decisions
- `ts_backfill(x, 66)` for gap filling (coverage 1.0, minimal gaps)
- `ts_delta(x, 21)` for monthly change
- `rank(x)` for cross-sectional normalization

---

## Dataset 7: other323 — Global Equity Premarket Data
**Category**: other | **Fields**: 11 VECTOR | **Coverage**: 1.0 | **alphaCount**: 1091 | **pm**: 1.4

### Field Deconstruction
| Field | What it measures | Time dimension | Business context |
|-------|-----------------|----------------|------------------|
| actual_shares_outstanding | Unrounded shares outstanding count | Daily | Share structure |
| oth323_esod | Date of most recent shares outstanding figure | Daily | Data freshness |
| oth323_esor | Number of shares outstanding (unrounded) | Daily | Share structure |
| oth323_ibc | Bloomberg Company ID | Static | Identifier |
| oth323_ibs | Bloomberg security-level identifier | Static | Identifier |
| oth323_par_amt | Par amount or face value of security | Static | Security structure |
| oth323_pxrls | Standard round lot size | Static | Trading structure |
| oth323_pxtls | Minimum tradable lot size | Static | Trading structure |
| par_value_amount | Par or face value | Static | Security structure |
| round_lot_size_value | Standard round lot size | Static | Trading structure |
| trade_lot_size_value | Minimum tradable lot size | Static | Trading structure |

### Key Observations
- **Premarket data** is mostly **static/security master** data (shares outstanding, lot sizes, identifiers)
- **Limited alpha potential**: Static fields don't change, so no time-series signal
- **Possible angle**: **Shares outstanding changes** (corporate actions) or **lot size liquidity** effects
- Coverage = 1.0, alphaCount = 1091 (moderate competition)
- **Recommendation**: **Low priority** — mostly static data, limited alpha potential

### Feature Concepts

#### Q2: What is changing? (Dynamics)
1. **Shares Outstanding Change** = ts_delta(actual_shares_outstanding, 21)
   - Meaning: Are shares outstanding changing (buybacks, issuance)?
   - Direction: Positive = issuance (dilution), Negative = buybacks (accretion)
   - Economic logic: Share count changes predict EPS impact and corporate actions

#### Q7: What is relative? (Comparison)
2. **Lot Size Liquidity Ratio** = trade_lot_size_value / (round_lot_size_value + 1)
   - Meaning: Minimum lot size vs standard lot size ratio
   - Direction: High = fragmented liquidity (retail), Low = institutional liquidity
   - Economic logic: Lot size ratio captures liquidity fragmentation

### Preprocessing Decisions
- `ts_backfill(x, 66)` for gap filling
- `ts_delta(x, 21)` for monthly change (shares outstanding)
- `rank(x)` for cross-sectional normalization

---

## Cross-Dataset Combination Opportunities

### Combination 1: model16 + model32 (Fundamental + Momentum)
- **Concept**: Fundamental revision momentum + price momentum alignment
- **Expression**: `rank(ts_mean(analyst_revision_rank_derivative, 10)) + rank(short_term_momentum_score_float)`
- **Logic**: Fundamental momentum confirms price momentum; divergence warns of reversal

### Combination 2: model36 + model252 (Credit + Defensiveness)
- **Concept**: Credit quality improvement + defensiveness momentum
- **Expression**: `rank(ts_delta(star_sr_global_rank, 21)) + rank(ts_delta(defensiveness_composite_score, 10))`
- **Logic**: Credit improvement + defensiveness = flight to quality signal

### Combination 3: model144 + risk70 (DL + Hedge Fund)
- **Concept**: DL model score + hedge fund ownership momentum
- **Expression**: `rank(ts_delta(mdl144_score, 5)) + rank(ts_delta(hedge_fund_ownership_percentage, 21))`
- **Logic**: DL signal + smart money flow = confirmed alpha

---

## Priority Ranking for Wave 1

| Priority | Dataset | Concept | Rationale |
|----------|---------|---------|-----------|
| 1 | model16 | Revision Momentum Persistence | Fundamental momentum, low competition, full coverage |
| 2 | model32 | Momentum Horizon Spread | Proven signal, structural differentiation from prod pool |
| 3 | model36 | Credit Quality Improvement | Credit family dead but SmartRatios different methodology |
| 4 | model144 | DL Score Momentum | Low competition, DL signal differentiation |
| 5 | model252 | Defensiveness Momentum | Quality family dead but SHIELD is risk/defense composite |
| 6 | risk70 | Hedge Fund Ownership Momentum | Smart money flow, moderate competition |
| 7 | other323 | Shares Outstanding Change | Low priority, mostly static data |

---

## Diversity Assessment

| Dimension | Coverage | Notes |
|-----------|----------|-------|
| Operator | ts_delta, ts_mean, rank, subtract, multiply, divide | Good mix of time-series and cross-sectional |
| Field | analyst_revision, momentum, credit, DL score, defensiveness, hedge fund, shares | 7 distinct signal families |
| Skeleton | single-field momentum, cross-field spread, interaction, rank | 4 distinct skeleton types |
| Preprocessing | ts_backfill, ts_delta, ts_mean, rank, ts_std_dev | 5 preprocessing operators |
| Return source | fundamental momentum, price momentum, credit improvement, DL signal, smart money | 5 distinct return sources |
| Failure risk | model36 (credit family dead), model252 (quality family dead), other323 (static) | 3 datasets with elevated risk |

---

## Next Steps (S2)

1. **brain-makeSomeGem** with `--ideas-file` pointing to this document
2. Generate 8-12 candidates per priority dataset (model16, model32, model36, model144)
3. Focus on **change/momentum** signals rather than **level** signals (differentiation from prod pool)
4. Ensure **cross-dataset correlation < 0.4** by using different signal families