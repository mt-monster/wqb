# EUR D1 ml_factor_proj ideas (Wave67 — agent S1; GEM 402)

Dataset: `ml_factor_proj` MATRIX. Leave model354 valuation (max S0.26) and NEWS.
Wave9 already tested EPS/price/FCF/accrual/ML-feature ranks — do not repeat.
OS ACTIVE=3. No resid×PV. Skip return/alpha/price-ratio fields.

## Concepts (0-alphaCount, cov=1.0)
1. Analyst coverage change — `change_analyst_coverage_count`
2. Consensus rating change — `change_analyst_consensus_rating`
3. FY2 EPS dispersion change — `change_dispersion_fy2_eps_estimates`
4. Cash conversion cycle change (invert) — `change_cash_conversion_cycle_2`
5. Abnormal capex change (invert) — `change_abnormal_capital_investment_2`
6. Asset turnover growth — `change_asset_turnover_growth`
7. Capex/sales intensity change (invert) — `change_capex_to_sales_ratio`

MATRIX: no `vec_avg`. Variants include ts_delta / short ts_mean to lift TVR (W66 value yields sat at 2–4%).
