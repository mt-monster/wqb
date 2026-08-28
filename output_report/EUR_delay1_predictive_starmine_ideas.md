# EUR D1 predictive_starmine ideas (Wave68 — agent S1; GEM 402)

Dataset: `predictive_starmine` MATRIX, cov≥0.85 only.
Skip Wave21: ARM/RelVal **global rank**, P/IV rank, FY1 earnings surprise, EQ composite.
Skip analyst revision % changes (prior ban). Skip low-coverage actuals.
OS ACTIVE=3. No resid×PV.

## Concepts (0-alpha)
1. ARM secondary earnings component — `arm_secondary_earnings_component_score_3`
2. RelVal EV/EBITDA component — `rel_val_ev_ebitda_component_score_3`
3. F12M EBITDA predicted surprise % — `predicted_surprise_pct_f12m_ebitda_5`
4. SmartEstimate next-vs-this EBITDA growth — `smest_growth_next_vs_this_yr_ebitda_5`
5. SmartEstimate this-vs-last earnings growth — `smest_growth_this_vs_last_yr_earnings_2`
6. Market-implied vs SmartGrowth 5y EPS CAGR disagreement — `market_implied_5yr_eps_cagr` − `forward_5yr_eps_cagr_projection`
7. Warranted forward PE invert — `iv_warranted_f12m_pe_3`
