# analyst_consensus 全字段清单（USA / TOP3000 / D1，2026-10-20）

> 来源：平台 `get_datafields(dataset_id="analyst_consensus", region="USA", delay=1, universe="TOP3000")`。
> 平台回传 `count=300`，本次取到 **300 行、全部为 VECTOR**（单次上限 300 行）。
> 另有 **10 个目标价 MATRIX 字段**需 `search="targetprice"` 单独取，列在 §0。
> 「更新频率 / 分布形态」无法从元数据得到：本文件给出覆盖、使用量、可用性档位；
> 更新频率按字段语义标注（`actual_*` = 报告事件；`estimate/forecast_*` = 分析师报告事件；`avg_*_prior` = 历史均值），
> 实测读数与机制判读见主画像 `_usa-analyst-consensus-field-profile-20261020.md`。

## 0. 目标价 MATRIX 子族（10 字段，平台 `search=targetprice` 实测）

| 字段 | 覆盖 | uc / aC |
|---|---:|---:|
| `mean_estimate_targetprice_annual12_tribes` | 0.9592 | 20 / 28 |
| `median_estimate_targetprice_annual12_tribes` | 0.9592 | — |
| `min_estimate_targetprice_annual12_tribes` | 0.9592 | 1 / 1 |
| `max_estimate_targetprice_annual12_tribes` | 0.9592 | 4 / 9 |
| `mean_estimate_fxadj_targetprice_annual12_tribes` | 0.9592 | 16 / 22 |
| `median_estimate_fxadj_targetprice_annual12_tribes` | 0.9592 | 3 / 4 |
| `min_estimate_fxadj_targetprice_annual12_tribes` | 0.9592 | 1 / 2 |
| `max_estimate_fxadj_targetprice_annual12_tribes` | 0.9592 | 6 / 6 |
| `stddev_estimate_fxadj_targetprice_annual12_tribes` | 0.9592 | 12 / 18 |
| `estimate_count_current_period_targetprice_annual12_tribes` | 0.9592 | 11 / 15 |

机制读法：目标价是**价格量纲**（跨股票不可直接横截面比较）⇒ 用 `ts_zscore`（对自身历史）或组内 `group_rank`；
可构造的无量纲形状量：`(mean−median)/stddev`（共识偏度）、`(max−min)/mean`（相对极差）、`stddev/mean`（变异系数）、
`(mean−min)/(max−mean)`（上下不对称）。已实测：只有「分歧度 × 共识偏斜」与「均值时序位置」两族达闸（见主画像 §3.1）。

## 1. 全量统计（300 VECTOR）

- 字段数：**300**；类型：VECTOR 300
- 覆盖率：min **0.3630** / 中位 **0.7203** / max **0.9521**
- `userCount=0`：**242**；`alphaCount=0`：**242**；`alphaCount>=10`：**0**
- 可用性档位：A 强 **92** / B 中 **70** / C 弱 **132** / D 弃 **6**

档位判据（本表自定义）：A = 覆盖≥0.85 且 aC≤5（低拥挤高覆盖）；B = 覆盖≥0.70 且 aC≤20；
C = 覆盖≥0.50；D = 覆盖<0.50（必须 backfill 或弃用）。

覆盖分档（VECTOR 字段）：
- [0.00, 0.50): **6**
- [0.50, 0.70): **132**
- [0.70, 0.85): **70**
- [0.85, 0.95): **90**
- [0.95, 1.00): **2**

> 硬约束：所有字段均为 VECTOR ⇒ 进矩阵算子前必须先 `vec_avg` / `vec_sum` / `vec_max` / `vec_min` / `vec_count` 聚合。

## actual_* 报告实际值（196 字段｜覆盖 0.3630–0.9521｜aC=0 的 149 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `actual_value_eps_annual12` | 0.9521 | 3 | 3 | A 强 | Actual reported annual EPS values vector; forecast periods are null/NaN |
| `actual_value_fxadj_eps_annual12` | 0.9521 | 0 | 0 | A 强 | Currency/split-adjusted actual reported annual EPS values |
| `actual_netprofit_value_annual12` | 0.9498 | 2 | 3 | A 强 | Actual reported annual Net Profit values aligned to the event periods (forecast slots e... |
| `actual_netprofit_value_fxadj_annual12` | 0.9498 | 0 | 0 | A 强 | Currency/split/regime-adjusted actual reported annual net profit values |
| `actual_revenue_value_annual12` | 0.9498 | 0 | 0 | A 强 | Actual reported annual sales value |
| `actual_revenue_value_fxadj_annual12` | 0.9498 | 0 | 0 | A 强 | Adjusted actual reported sales values (currency/splits/regime adjusted) |
| `actual_revenue_value_annual12_tribes` | 0.9497 | 1 | 1 | A 强 | Actual reported annual revenue (vendor-reported) |
| `actual_value_fxadj_revenue_annual12_tribes` | 0.9497 | 1 | 1 | A 强 | Currency/split/regime-adjusted actual reported annual revenue |
| `actual_eps_value_annual12_3` | 0.9440 | 1 | 1 | A 强 | Actual reported annual EPS value |
| `actual_eps_value_fxadj_annual12_3` | 0.9440 | 1 | 1 | A 强 | Adjusted actual reported annual EPS values (currency/split/regime adjusted) |
| `actual_epsreported_value_annual12` | 0.9433 | 3 | 3 | A 强 | Actual reported EPS value (EPSREP) |
| `actual_epsreported_value_fxadj_annual12` | 0.9433 | 0 | 0 | A 强 | Currency/split/regime-adjusted actual reported EPS value |
| `actual_pretax_value_annual12_2` | 0.9431 | 0 | 0 | A 强 | Actual reported annual PPROFIT value |
| `actual_pretax_value_fxadj_annual12_2` | 0.9431 | 1 | 1 | A 强 | Currency-adjusted actual annual pre-tax profit value |
| `actual_ebit_value_annual12` | 0.9396 | 2 | 2 | A 强 | Reported actual annual EBIT value as released by the company |
| `actual_ebit_value_fxadj_annual12` | 0.9396 | 0 | 0 | A 强 | Currency/split-adjusted actual reported annual EBIT values |
| `actual_net_value` | 0.9395 | 1 | 1 | A 强 | Actual reported annual Net Income (NET) values |
| `actual_net_value_fxadj` | 0.9395 | 0 | 0 | A 强 | Regime- and currency-adjusted actual reported annual Net Income (NET) values |
| `actual_eps_value_fxadj_quarterly16` | 0.9379 | 1 | 2 | A 强 | Regime-adjusted reported quarterly EPS actual value |
| `actual_eps_value_quarterly16` | 0.9379 | 0 | 0 | A 强 | Reported quarterly EPS actual value |
| `actual_sharesoutstanding_value_annual12` | 0.9374 | 0 | 0 | A 强 | Actual reported Number of Shares Outstanding for the period (vector aligned to events; ... |
| `actual_netprofitreported_value_annual12` | 0.9369 | 1 | 1 | A 强 | Actual reported annual Net Profit (NPROFITREP) values aligned to events; forecast perio... |
| `actual_netprofitreported_value_fxadj_annual12` | 0.9369 | 0 | 0 | A 强 | Currency- and split-adjusted actual reported annual Net Profit values |
| `actual_revenue_value_fxadj_quarterly16_3` | 0.9335 | 0 | 0 | A 强 | Regime-adjusted actual reported quarterly sales values (currency/split adjusted) |
| `actual_revenue_value_quarterly16_3` | 0.9335 | 1 | 1 | A 强 | Actual reported quarterly sales figure from vendor actuals |
| `actual_gps_value` | 0.9310 | 0 | 0 | A 强 | Actual reported value for the GPS measure (as reported, unadjusted) |
| `actual_gps_value_fxadj` | 0.9310 | 0 | 0 | A 强 | Currency/split-adjusted actual reported values for the GPS measure |
| `actual_value_eps_quarterly16_tribes` | 0.9303 | 3 | 3 | A 强 | Actual reported quarterly EPS (unadjusted) |
| `actual_value_fxadj_eps_quarterly16_tribes` | 0.9303 | 0 | 0 | A 强 | Currency/split/regime-adjusted actual reported quarterly EPS |
| `actual_taxprovision_value_annual12_tribes` | 0.9279 | 0 | 0 | A 强 | Actual reported TAXPROV values |
| `actual_value_fxadj_taxprovision_annual12_tribes` | 0.9279 | 1 | 2 | A 强 | Actual reported Tax Provision figures adjusted for currency/splits |
| `actual_revenue_value_fxadj_quarterly16` | 0.9248 | 1 | 1 | A 强 | Currency-adjusted actual reported quarterly revenue |
| `actual_revenue_value_quarterly16` | 0.9248 | 1 | 1 | A 强 | Reported quarterly revenue actuals (NaN during forecast periods) |
| `actual_net_income` | 0.9243 | 0 | 0 | A 强 | Actual reported quarterly Net Income values (aligned to event periods) |
| `actual_net_income_fxadj` | 0.9243 | 0 | 0 | A 强 | Regime-adjusted actual reported quarterly net income (currency/splits/embargo adjustments) |
| `actual_reportednet_value_annual12_2` | 0.9232 | 0 | 0 | A 强 | Actual reported NER value |
| `actual_reportednet_value_fxadj_annual12_2` | 0.9232 | 0 | 0 | A 强 | Regime-adjusted actual NER value (currency/splits adjusted) |
| `actual_pretax_reported_value_annual12_tribes` | 0.9227 | 0 | 0 | A 强 | Actual reported pre-tax profit values aligned to event dates (forecast lead periods are... |
| `actual_value_fxadj_pretax_reported_annual12_tribes` | 0.9227 | 1 | 1 | A 强 | Reported actual values for the measure adjusted for currency/splits/regime |
| `actual_ebit_value_annual12_2` | 0.9226 | 0 | 0 | A 强 | Actual reported annual EBI value, unadjusted |
| `actual_ebit_value_fxadj_annual12_2` | 0.9226 | 1 | 1 | A 强 | Currency/split adjusted actual reported EBI figures |
| `actual_pretax_value_annual12` | 0.9214 | 0 | 0 | A 强 | Actual reported value for the PRE measure (annual); vector aligned to events with NaN f... |
| `actual_pretax_value_fxadj_annual12` | 0.9214 | 0 | 0 | A 强 | Regime-adjusted actual reported values for the PRE metric (currency/split adjusted) |
| `actual_netprofit_value_fxadj_quarterly16` | 0.9179 | 0 | 0 | A 强 | Actual reported quarterly net profit adjusted for currency, splits, and regime effects |
| `actual_netprofit_value_quarterly16` | 0.9179 | 0 | 0 | A 强 | Actual reported quarterly net profit |
| `actual_fullyreported_value` | 0.9167 | 1 | 1 | A 强 | Actual reported value for the GPS metric (latest quarterly report) |
| `actual_fullyreported_value_fxadj` | 0.9167 | 0 | 0 | A 强 | Regime- and currency-adjusted actual reported values for the GPS metric |
| `actual_eps_reported_value_fxadj_quarterly16` | 0.9102 | 1 | 2 | A 强 | Reported actual EPS value adjusted for currency/splits/regime |
| `actual_eps_reported_value_quarterly16` | 0.9102 | 0 | 0 | A 强 | Reported actual EPS value |
| `actual_reportednet_value` | 0.9015 | 0 | 0 | A 强 | Actual reported value for the NER metric |
| `actual_reportednet_value_fxadj` | 0.9015 | 0 | 0 | A 强 | Regime-adjusted actual reported value for the NER metric (currency/split adjusted) |
| `actual_tangbookvalue_value_annual12_tribes` | 0.9015 | 0 | 0 | A 强 | Actual reported values for the SEQUITY measure (vector; forecast positions are NaN) |
| `actual_tangbookvalue_value_fxadj_annual12_tribes` | 0.9015 | 1 | 1 | A 强 | Currency-adjusted actual reported value(s) for the SEquity measure |
| `actual_ebit_value_quarterly16_2` | 0.8994 | 0 | 0 | A 强 | Actual reported quarterly EBI value |
| `actual_value_fxadj_ebit_quarterly16` | 0.8994 | 0 | 0 | A 强 | Regime-adjusted actual EBI values (currency/split adjusted) |
| `actual_nav_value_annual12_tribes` | 0.8993 | 0 | 0 | A 强 | Actual reported NAV value |
| `actual_value_fxadj_nav_annual12_tribes` | 0.8993 | 0 | 0 | A 强 | Reported actual values adjusted for currency, splits, and regime effects |
| `actual_pretax_reported_value_annual12` | 0.8991 | 0 | 0 | A 强 | Actual reported pre-tax profit for the annual period. |
| `actual_pretax_reported_value_fxadj_annual12` | 0.8991 | 1 | 1 | A 强 | Regime-adjusted actual reported PRR values vector |
| `actual_value_fxadj_interest_expense_annual12` | 0.8976 | 0 | 0 | A 强 | Reported actual annual Interest Expense adjusted for currency/splits |
| `actual_value_interest_expense_annual12` | 0.8976 | 0 | 0 | A 强 | Reported actual annual Interest Expense |
| `actual_ebit_value_fxadj_quarterly16_tribes` | 0.8967 | 0 | 0 | A 强 | Currency-adjusted actual reported quarterly EBIT value |
| `actual_value_ebit_quarterly16` | 0.8967 | 0 | 0 | A 强 | Actual reported value for quarterly EBIT |
| `actual_netprofit_reported_value_fxadj_quarterly16` | 0.8945 | 0 | 0 | A 强 | Currency/split/regime-adjusted reported actual value for quarterly Net Profit (Reported) |
| `actual_netprofit_reported_value_quarterly16` | 0.8945 | 0 | 0 | A 强 | Reported actual net profit for the period |
| `actual_total_assets_value_annual12` | 0.8937 | 2 | 2 | A 强 | Reported actual values vector (NaN in forecast periods) |
| `actual_total_assets_value_fxadj_annual12` | 0.8937 | 1 | 1 | A 强 | Currency/split/regime-adjusted actual reported value for the measure |
| `actual_pretax_value_fxadj_quarterly16_tribes` | 0.8876 | 0 | 0 | A 强 | Regime and currency adjusted actual reported quarterly PPROFIT |
| `actual_pretax_value_quarterly16_tribes` | 0.8876 | 0 | 0 | A 强 | Actual reported value for the PPROFIT quarterly metric |
| `actual_pretax_value` | 0.8872 | 0 | 0 | A 强 | Actual reported value for the PRE measure for the relevant quarterly period |
| `actual_pretax_value_fxadj` | 0.8872 | 0 | 0 | A 强 | Regime-adjusted actual reported value(s) for the PRE measure |
| `actual_tax_provision_value_quarterly16` | 0.8738 | 0 | 0 | A 强 | Actual reported quarterly tax provision values as reported (unadjusted) |
| `actual_value_fxadj_tax_provision_quarterly16` | 0.8738 | 0 | 0 | A 强 | Currency/regime-adjusted actual tax provision value |
| `actual_pretax_value_fxadj_quarterly16` | 0.8700 | 0 | 0 | A 强 | Adjusted actual reported figure for the PRR measure (currency and split corrected) |
| `actual_pretax_value_quarterly16` | 0.8700 | 0 | 0 | A 强 | Actual reported pretax profit for the quarterly period. |
| `actual_nav_value_annual12` | 0.8683 | 0 | 0 | A 强 | Actual reported net asset value for the annual period. |
| `actual_nav_value_fxadj_annual12` | 0.8683 | 0 | 0 | A 强 | Actual reported annual NAV value adjusted for currency/splits/regime |
| `actual_pretax_reported_value_fxadj_quarterly16` | 0.8662 | 0 | 0 | A 强 | Currency/split/regime-adjusted actual value for the PPROFITREP measure |
| `actual_pretax_reported_value_quarterly16` | 0.8662 | 0 | 0 | A 强 | Actual reported value for PPROFITREP |
| `actual_taxrate_value_annual12` | 0.8650 | 0 | 0 | A 强 | Actual reported TAXRATE value |
| `actual_taxrate_value_fxadj_annual12` | 0.8650 | 0 | 0 | A 强 | Actual reported effective tax rate for the annual period, adjusted for currency. |
| `actual_value_ebitda_annual12` | 0.8636 | 0 | 0 | A 强 | Reported actual EBITDA value for the corresponding fiscal period |
| `actual_value_fxadj_ebitda_annual12` | 0.8636 | 0 | 0 | A 强 | Currency/split/regime-adjusted actual EBITDA value |
| `actual_marketable_securities_value_annual12` | 0.8634 | 0 | 0 | A 强 | Reported actual value for Marketable Securities |
| `actual_marketable_securities_value_fxadj_annual12` | 0.8634 | 0 | 0 | A 强 | Currency/split-adjusted actual reported values |
| `actual_roe_value_annual12_tribes_2` | 0.8592 | 1 | 1 | A 强 | Company-reported actual annual ROE value as captured point-in-time under the dataset’s ... |
| `actual_dividend_value_annual12_2` | 0.8485 | 0 | 0 | B 中 | Actual reported annual dividends-per-share (DPS) value for the period |
| `actual_dividend_value_fxadj_annual12_3` | 0.8485 | 0 | 0 | B 中 | Actual annual DPS value adjusted for currency/splits/regime effects |
| `actual_operatingexpense_value_annual12` | 0.8405 | 0 | 0 | B 中 | Actual reported annual operating expenses |
| `actual_operatingexpense_value_fxadj_annual12` | 0.8405 | 0 | 0 | B 中 | Currency/regime-adjusted actual reported annual operating expenses |
| `actual_interest_expense_value` | 0.8365 | 0 | 0 | B 中 | The actual reported value for interest expense in the period. |
| `actual_interest_expense_value_adjusted` | 0.8365 | 1 | 1 | B 中 | The actual reported value for interest expense, adjusted for currency effects. |
| `actual_ebt_value_annual12` | 0.8288 | 0 | 0 | B 中 | Actual reported EBT value (regime-aware) |
| `actual_ebt_value_fxadj_annual12` | 0.8288 | 0 | 0 | B 中 | Regime- and currency-adjusted actual reported annual EBT |
| `actual_capex_value_annual12_3` | 0.8128 | 2 | 2 | B 中 | Actual reported CAPEX value (as reported, unadjusted) |
| `actual_capex_value_fxadj_annual12_3` | 0.8128 | 1 | 1 | B 中 | Currency/regime-adjusted actual reported CAPEX value |
| `actual_bvps_value_annual12_tribes` | 0.8126 | 3 | 3 | B 中 | Reported actual BVPS values for the periods (forecast periods may be empty) |
| `actual_bvps_value_fxadj_annual12_2` | 0.8126 | 1 | 1 | B 中 | Regime and currency-adjusted actual reported BVPS value |
| `actual_dividend_value_annual12` | 0.8054 | 0 | 0 | B 中 | Actual reported annual DPS value(s) |
| `actual_dividend_value_fxadj_annual12_2` | 0.8054 | 0 | 0 | B 中 | Regime-adjusted actual annual DPS (currency/split adjusted) |
| `actual_roe_value_annual12` | 0.8053 | 0 | 0 | B 中 | Actual reported value for annual return on equity. |
| `actual_cfo_value_annual12` | 0.7956 | 2 | 3 | B 中 | Reported actual operating cash flow values; forecast periods are typically NaN |
| `actual_cfo_value_fxadj_annual12` | 0.7956 | 0 | 0 | B 中 | Reported actual operating cash flow values adjusted for currency and splits |
| `actual_ebitda_value_fxadj_quarterly16` | 0.7905 | 0 | 0 | B 中 | Currency/split-adjusted actual reported EBITDA values for each period |
| `actual_ebitda_value_quarterly16` | 0.7905 | 0 | 0 | B 中 | Actual reported quarterly EBITDA |
| `actual_fcf_value_annual12` | 0.7902 | 0 | 0 | B 中 | Actual reported annual Free Cash Flow value for the company, point-in-time and regime-a... |
| `actual_fcf_value_fxadj_annual12` | 0.7902 | 1 | 1 | B 中 | Regime-adjusted actual annual FCF value (currency/split adjusted) |
| `actual_capex_value_annual12_2` | 0.7802 | 0 | 0 | B 中 | Actual reported CPX values |
| `actual_capex_value_fxadj_annual12_2` | 0.7802 | 0 | 0 | B 中 | Regime-adjusted actual reported CPX values |
| `actual_totalliab_value_annual12_tribes` | 0.7780 | 0 | 0 | B 中 | Actual reported Total Liabilities value |
| `actual_totalliab_value_fxadj_annual12_tribes` | 0.7780 | 0 | 0 | B 中 | Currency/split/regime-adjusted actual reported Total Liabilities value |
| `actual_pretax_value_fxadj_quarterly16_2` | 0.7734 | 0 | 0 | B 中 | Regime- and currency-adjusted actual reported quarterly EBT |
| `actual_pretax_value_quarterly16_2` | 0.7734 | 0 | 0 | B 中 | Actual reported quarterly EBT values (forecast positions are NaN) |
| `actual_bvps_value_annual12` | 0.7725 | 0 | 0 | B 中 | Company-reported actual annual Book Value per Share (unadjusted) |
| `actual_bvps_value_fxadj_annual12` | 0.7725 | 0 | 0 | B 中 | Adjusted actual reported Book Value Per Share value (currency/split adjusted) |
| `actual_roe_value_annual12_tribes` | 0.7660 | 0 | 0 | B 中 | Reported actual annual ROA value for the period |
| `actual_cashflowinvesting_value_annual12` | 0.7495 | 0 | 0 | B 中 | Actual reported annual CFINVEST values, with forecast periods typically filled with NaN |
| `actual_cashflowinvesting_value_fxadj_annual12` | 0.7495 | 0 | 0 | B 中 | Currency-adjusted actual reported Cash Flow from Investing (converted to default curren... |
| `actual_cogs_value_annual12_tribes` | 0.7479 | 0 | 0 | B 中 | Actual reported annual Cost of Goods Sold |
| `actual_cogs_value_fxadj_annual12_tribes` | 0.7479 | 1 | 1 | B 中 | Currency/split adjusted actual annual COGS value |
| `actual_grossmargin_value_annual12_tribes` | 0.7458 | 1 | 2 | B 中 | Reported actual GPM value for the relevant fiscal period |
| `actual_cashflowfinancing_value_annual12` | 0.7429 | 0 | 0 | B 中 | Reported actual annual Cash Flow from Financing (CFFINANCE) |
| `actual_cashflowfinancing_value_fxadj_annual12` | 0.7429 | 0 | 0 | B 中 | Actual annual Cash Flow from Financing adjusted for currency/splits/regime |
| `actual_netdebt_value_annual12_tribes_2` | 0.7400 | 2 | 2 | B 中 | Actual reported annual Net Debt (NDEBT) value |
| `actual_netdebt_value_fxadj_annual12_2` | 0.7400 | 1 | 1 | B 中 | Adjusted actual annual Net Debt value (currency/split/regime adjusted) |
| `actual_cfps_value_annual12_2` | 0.7282 | 2 | 2 | B 中 | Reported actual annual CFPS value |
| `actual_cfps_value_fxadj_annual12_2` | 0.7282 | 0 | 0 | B 中 | Currency/split-adjusted actual CFPS values |
| `actual_currentassets_value_annual12` | 0.7212 | 0 | 0 | B 中 | Actual reported annual current assets amount as disclosed by the company |
| `actual_currentassets_value_fxadj_annual12` | 0.7212 | 2 | 2 | B 中 | Currency/split/regime-adjusted actual reported annual current assets amount |
| `actual_equity_reported_value` | 0.7203 | 2 | 4 | B 中 | Actual reported value for equity for the period. |
| `actual_currentliabilities_value_annual12` | 0.7200 | 0 | 0 | B 中 | Reported actual value for annual current liabilities (unadjusted) |
| `actual_currentliabilities_value_fxadj_annual12` | 0.7200 | 0 | 0 | B 中 | Actual reported annual current liabilities adjusted for currency/regime effects |
| `actual_value_adjusted` | 0.7110 | 0 | 0 | B 中 | The actual reported value for the period, adjusted for currency effects. |
| `actual_nav_value` | 0.7040 | 0 | 0 | B 中 | Actual reported NAV values vector |
| `actual_nav_value_fxadj` | 0.7040 | 0 | 0 | B 中 | Currency/split-adjusted actual reported NAV values vector |
| `actual_value_enterprisevalue_annual12` | 0.6969 | 0 | 0 | C 弱 | Actual reported EV values vector, with forecast periods filled with nulls/NaNs |
| `actual_value_fxadj_enterprisevalue_annual12` | 0.6969 | 0 | 0 | C 弱 | Currency/regime-adjusted actual reported value for the EV metric |
| `actual_netdebt_value_annual12` | 0.6934 | 0 | 0 | C 弱 | Vector of actual reported figures for the measure aligned to event periods |
| `actual_netdebt_value_fxadj_annual12` | 0.6934 | 1 | 1 | C 弱 | Regime- and currency-adjusted actual reported values vector |
| `actual_marketable_securities_value` | 0.6849 | 0 | 0 | C 弱 | The actual reported value for marketable securities in the period. |
| `actual_marketable_securities_value_adjusted` | 0.6849 | 0 | 0 | C 弱 | The actual reported value for marketable securities, adjusted for currency effects. |
| `actual_grossmargin_value_annual12` | 0.6811 | 0 | 0 | C 弱 | Actual reported annual gross margin value |
| `actual_cfps_value_annual12` | 0.6764 | 0 | 0 | C 弱 | Vendor-reported actual value of annual cash flow per share (CPS) |
| `actual_cfps_value_fxadj_annual12` | 0.6764 | 0 | 0 | C 弱 | Regime-adjusted actual reported value of annual cash flow per share (CPS) |
| `actual_ebitdarep_value_annual12` | 0.6756 | 1 | 1 | C 弱 | Actual reported annual EBITDA values |
| `actual_ebitdarep_value_fxadj_annual12` | 0.6756 | 0 | 0 | C 弱 | Currency-adjusted actual values for annual Reported EBITDA aligned to event periods |
| `actual_reported_fx_adjusted_cogs` | 0.6656 | 0 | 0 | C 弱 | Actual reported cost of goods sold, adjusted for currency. |
| `actual_reported_value_cogs` | 0.6656 | 0 | 0 | C 弱 | Actual reported cost of goods sold for the period. |
| `actual_goodwill_value_annual12` | 0.6615 | 0 | 0 | C 弱 | Vector of company-reported actual goodwill values for annual periods aligned to the eve... |
| `actual_goodwill_value_fxadj_annual12` | 0.6615 | 0 | 0 | C 弱 | Regime- and currency/split-adjusted actual reported goodwill value |
| `actual_dividend_value_annual12_tribes` | 0.6508 | 1 | 1 | C 弱 | Actual reported total dividend value |
| `actual_dividend_value_fxadj_annual12_tribes` | 0.6508 | 0 | 0 | C 弱 | Regime-adjusted actual total dividend value (currency/splits adjustments) |
| `actual_value_gross_margin_quarterly16` | 0.6328 | 1 | 2 | C 弱 | Actual reported gross margin in the current quarter. |
| `actual_value_fxadj_gross_income_quarterly16` | 0.6303 | 0 | 0 | C 弱 | Currency and split adjusted actual reported quarterly gross income values |
| `actual_value_gross_income_quarterly16` | 0.6303 | 0 | 0 | C 弱 | Actual reported quarterly gross income values; forecast periods are empty or NaN until ... |
| `actual_depreciation_value_annual12` | 0.6300 | 4 | 4 | C 弱 | Actual reported annual depreciation values aligned to events (NaN for pure forecast per... |
| `actual_depreciation_value_fxadj_annual12` | 0.6300 | 0 | 0 | C 弱 | Adjusted actual annual depreciation values vector (currency/split/regime adjusted) |
| `actual_capex_reported_value` | 0.6202 | 0 | 0 | C 弱 | Actual reported value for capital expenditure for the period. |
| `actual_value_grossmargin_quarterly16` | 0.6151 | 0 | 0 | C 弱 | Actual reported gross margin value for the quarter. |
| `actual_capex_value_fxadj_quarterly16` | 0.6070 | 0 | 0 | C 弱 | Actual reported values for the CPX measure, adjusted for currency and stock splits and ... |
| `actual_capex_value_quarterly16` | 0.6070 | 0 | 0 | C 弱 | Actual reported values for the CPX measure, with forecast positions as NaN and actuals ... |
| `actual_value_dps_quarterly16_2` | 0.6068 | 0 | 0 | C 弱 | Actual reported quarterly DPS value |
| `actual_value_fxadj_dps_quarterly16_2` | 0.6068 | 0 | 0 | C 弱 | Currency/split-adjusted actual reported quarterly DPS values vector |
| `actual_dps_value_fxadj_quarterly16` | 0.6035 | 0 | 0 | C 弱 | Currency and split adjusted vector of reported quarterly DPS actuals aligned to event p... |
| `actual_dps_value_quarterly16` | 0.6035 | 1 | 5 | C 弱 | Actual reported DPS value |
| `actual_reported_fx_adjusted` | 0.5988 | 1 | 1 | C 弱 | Actual reported value adjusted for currency effects. |
| `actual_reported_value_3` | 0.5988 | 0 | 0 | C 弱 | Actual reported value for the period. |
| `actual_inventory_value_annual12` | 0.5966 | 0 | 0 | C 弱 | Actual reported annual Inventory value |
| `actual_inventory_value_fxadj_annual12` | 0.5966 | 0 | 0 | C 弱 | Currency/regime-adjusted actual annual inventory value |
| `actual_value_fcfps_annual12` | 0.5922 | 0 | 0 | C 弱 | Reported actual annual FCFPS values aligned to the event timeline (forecast periods empty) |
| `actual_value_fxadj_fcfps_annual12` | 0.5922 | 0 | 0 | C 弱 | Actual annual FCFPS values adjusted for currency and corporate actions (e.g., splits) |
| `actual_value_fxadj_total_debt_annual12` | 0.5768 | 0 | 0 | C 弱 | Currency-adjusted actual reported Total Debt value |
| `actual_value_total_debt_annual12` | 0.5768 | 0 | 0 | C 弱 | Actual reported value for Total Debt |
| `actual_reported_fx_adjusted_2` | 0.5717 | 0 | 0 | C 弱 | Actual reported value for the period, adjusted for currency. |
| `actual_reported_value_4` | 0.5717 | 0 | 0 | C 弱 | Actual reported value for the period. |
| `actual_reported_fx_adjusted_bvps` | 0.5545 | 0 | 0 | C 弱 | Actual reported book value per share, adjusted for currency. |
| `actual_reported_value_bvps` | 0.5545 | 0 | 0 | C 弱 | Actual reported book value per share for the period. |
| `actual_liability_value` | 0.5418 | 0 | 0 | C 弱 | The actual reported value for total liabilities in the period. |
| `actual_liability_value_adjusted` | 0.5418 | 0 | 0 | C 弱 | The actual reported value for total liabilities, adjusted for currency effects. |
| `actual_bvps_value_quarterly16_2` | 0.5416 | 0 | 0 | C 弱 | Reported actual value for quarterly book value per share. |
| `actual_value_fxadj_bvps_quarterly16_2` | 0.5416 | 0 | 0 | C 弱 | Currency/split-adjusted actual reported figure |
| `actual_cfps_value_fxadj_quarterly16` | 0.5359 | 0 | 0 | C 弱 | Currency/split-adjusted actual CPS values |
| `actual_cfps_value_quarterly16` | 0.5359 | 0 | 0 | C 弱 | Reported actual quarterly CPS values aligned to periods (vector) |
| `actual_fcf_fxadj` | 0.5285 | 0 | 0 | C 弱 | Actual reported free cash flow, adjusted for currency effects. |
| `actual_fcf_value` | 0.5285 | 0 | 0 | C 弱 | Reported actual value for free cash flow for the specified period. |
| `actual_value_return_on_equity_quarterly16` | 0.5283 | 0 | 0 | C 弱 | Actual reported return on equity in the current quarter. |
| `actual_reported_value_2` | 0.5274 | 0 | 0 | C 弱 | Actual reported value for the period. |
| `actual_current_assets_reported_value` | 0.5179 | 0 | 0 | C 弱 | Actual reported value for current assets for the period. |
| `actual_fcf_value_fxadj_quarterly16` | 0.5144 | 0 | 0 | C 弱 | Currency-adjusted actual reported quarterly FCF values |
| `actual_fcf_value_fxadj_quarterly16_tribes` | 0.5144 | 0 | 0 | C 弱 | Actual reported quarterly FCF values aligned to the event timeline (forecast slots are ... |
| `actual_value_roe_quarterly16` | 0.4717 | 0 | 0 | D 弃 | Actual reported ROE value for the quarter (filled only in actual periods) |
| `actual_return_on_capital_value_annual12` | 0.4708 | 0 | 0 | D 弃 | Actual reported value of return on capital for the annual period. |
| `actual_netdebt_value_fxadj_quarterly16` | 0.4520 | 0 | 0 | D 弃 | Actual reported net debt for the quarter, adjusted for currency effects. |
| `actual_netdebt_value_quarterly16` | 0.4520 | 0 | 0 | D 弃 | Vector of actual reported values for this measure aligned to event periods, unadjusted |
| `actual_fcf_value_fxadj_fq16` | 0.3630 | 0 | 0 | D 弃 | Actual reported free cash flow for the quarter, adjusted for currency effects. |
| `actual_fcf_value_quarterly16` | 0.3630 | 0 | 0 | D 弃 | Actual reported value for quarterly free cash flow. |

## adjusted_* 汇率/拆股调整后口径（40 字段｜覆盖 0.5179–0.7203｜aC=0 的 35 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `adjusted_actual_equity_value` | 0.7203 | 1 | 1 | B 中 | Actual reported equity value adjusted for currency. |
| `adjusted_equity_forecast_standard_deviation` | 0.7203 | 0 | 0 | B 中 | Standard deviation of equity analyst forecasts adjusted for currency. |
| `adjusted_highest_equity_forecast` | 0.7203 | 0 | 0 | B 中 | Highest analyst forecast for equity adjusted for currency. |
| `adjusted_lowest_equity_forecast` | 0.7203 | 1 | 1 | B 中 | Lowest analyst forecast for equity adjusted for currency. |
| `adjusted_mean_equity_forecast` | 0.7203 | 1 | 1 | B 中 | Mean analyst forecast for equity adjusted for currency. |
| `adjusted_mean_equity_forecast_actual` | 0.7203 | 0 | 0 | B 中 | Mean analyst forecast and actual equity value, adjusted for currency. |
| `adjusted_mean_equity_forecast_surprise` | 0.7203 | 1 | 1 | B 中 | Difference between actual and mean equity forecast, adjusted for currency. |
| `adjusted_median_equity_forecast` | 0.7203 | 0 | 0 | B 中 | Median analyst forecast for equity adjusted for currency. |
| `adjusted_median_equity_forecast_actual` | 0.7203 | 0 | 0 | B 中 | Median analyst forecast and actual equity value, adjusted for currency. |
| `adjusted_median_equity_forecast_surprise` | 0.7203 | 0 | 0 | B 中 | Difference between actual and median equity forecast, adjusted for currency. |
| `adjusted_actual_capex_value` | 0.6202 | 0 | 0 | C 弱 | Actual reported capital expenditure value adjusted for currency. |
| `adjusted_capex_forecast_standard_deviation` | 0.6202 | 0 | 0 | C 弱 | Standard deviation of capital expenditure analyst forecasts adjusted for currency. |
| `adjusted_highest_capex_forecast` | 0.6202 | 0 | 0 | C 弱 | Highest analyst forecast for capital expenditure adjusted for currency. |
| `adjusted_lowest_capex_forecast` | 0.6202 | 0 | 0 | C 弱 | Lowest analyst forecast for capital expenditure adjusted for currency. |
| `adjusted_mean_capex_forecast` | 0.6202 | 0 | 0 | C 弱 | Mean analyst forecast for capital expenditure adjusted for currency. |
| `adjusted_mean_capex_forecast_actual` | 0.6202 | 0 | 0 | C 弱 | Mean analyst forecast and actual capital expenditure value, adjusted for currency. |
| `adjusted_mean_capex_forecast_surprise` | 0.6202 | 0 | 0 | C 弱 | Difference between actual and mean capital expenditure forecast, adjusted for currency. |
| `adjusted_median_capex_forecast` | 0.6202 | 0 | 0 | C 弱 | Median analyst forecast for capital expenditure adjusted for currency. |
| `adjusted_median_capex_forecast_actual` | 0.6202 | 0 | 0 | C 弱 | Median analyst forecast and actual capital expenditure value, adjusted for currency. |
| `adjusted_median_capex_forecast_surprise` | 0.6202 | 0 | 0 | C 弱 | Difference between actual and median capital expenditure forecast, adjusted for currency. |
| `adjusted_actual_reported_value` | 0.5274 | 0 | 0 | C 弱 | Actual reported value adjusted for currency effects. |
| `adjusted_forecast_standard_deviation` | 0.5274 | 0 | 0 | C 弱 | Standard deviation of analyst forecasts adjusted for currency. |
| `adjusted_highest_forecast_value` | 0.5274 | 0 | 0 | C 弱 | Highest analyst forecast adjusted for currency effects. |
| `adjusted_lowest_forecast_value` | 0.5274 | 0 | 0 | C 弱 | Lowest analyst forecast adjusted for currency effects. |
| `adjusted_mean_forecast_actual_value` | 0.5274 | 1 | 1 | C 弱 | Mean of analyst forecasts and actual value, adjusted for currency. |
| `adjusted_mean_forecast_surprise` | 0.5274 | 0 | 0 | C 弱 | Difference between actual and mean forecast, adjusted for currency. |
| `adjusted_mean_forecast_value` | 0.5274 | 0 | 0 | C 弱 | Mean of analyst forecasts adjusted for currency effects. |
| `adjusted_median_forecast_actual_value` | 0.5274 | 0 | 0 | C 弱 | Median of analyst forecasts and actual value, adjusted for currency. |
| `adjusted_median_forecast_surprise` | 0.5274 | 0 | 0 | C 弱 | Difference between actual and median forecast, adjusted for currency. |
| `adjusted_median_forecast_value` | 0.5274 | 0 | 0 | C 弱 | Median of analyst forecasts adjusted for currency effects. |
| `adjusted_actual_current_assets_value` | 0.5179 | 0 | 0 | C 弱 | Actual reported current assets value adjusted for currency. |
| `adjusted_current_assets_forecast_stddev` | 0.5179 | 0 | 0 | C 弱 | Standard deviation of current assets analyst forecasts adjusted for currency. |
| `adjusted_highest_current_assets_forecast` | 0.5179 | 0 | 0 | C 弱 | Highest analyst forecast for current assets adjusted for currency. |
| `adjusted_lowest_current_assets_forecast` | 0.5179 | 0 | 0 | C 弱 | Lowest analyst forecast for current assets adjusted for currency. |
| `adjusted_mean_current_assets_forecast` | 0.5179 | 0 | 0 | C 弱 | Mean analyst forecast for current assets adjusted for currency. |
| `adjusted_mean_current_assets_forecast_actual` | 0.5179 | 0 | 0 | C 弱 | Mean analyst forecast and actual current assets value, adjusted for currency. |
| `adjusted_mean_current_assets_forecast_surprise` | 0.5179 | 0 | 0 | C 弱 | Difference between actual and mean current assets forecast, adjusted for currency. |
| `adjusted_median_current_assets_forecast` | 0.5179 | 0 | 0 | C 弱 | Median analyst forecast for current assets adjusted for currency. |
| `adjusted_median_current_assets_forecast_actual` | 0.5179 | 0 | 0 | C 弱 | Median analyst forecast and actual current assets value, adjusted for currency. |
| `adjusted_median_current_assets_forecast_surprise` | 0.5179 | 0 | 0 | C 弱 | Difference between actual and median current assets forecast, adjusted for currency. |

## average_forecast_* 一致预期均值（24 字段｜覆盖 0.5357–0.8924｜aC=0 的 23 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `average_forecast_actual_value_noshareout_qtr` | 0.8924 | 0 | 0 | A 强 | Mean of forecast and actual values for the quarter (no share out). |
| `average_forecast_actual_fx_adjusted_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Mean of forecast and actual values for the quarter adjusted for currency (depreciation/... |
| `average_forecast_actual_value_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Mean of forecast and actual values for the quarter (depreciation/amortization). |
| `average_forecast_equity_value` | 0.7203 | 0 | 0 | B 中 | Mean of analyst forecast values for equity for the period. |
| `average_forecast_actual_fx_adjusted_nav_qtr` | 0.7110 | 0 | 0 | B 中 | Mean of forecast and actual values for the quarter adjusted for currency (net asset val... |
| `average_forecast_actual_fx_adjusted_3` | 0.6851 | 0 | 0 | C 弱 | Mean of forecast and actual values adjusted for currency. |
| `average_forecast_actual_value` | 0.6851 | 0 | 0 | C 弱 | Mean of forecast and actual values for the period. |
| `average_forecast_actual_combined_cogs` | 0.6656 | 0 | 0 | C 弱 | Mean of both forecast and actual cost of goods sold. |
| `average_forecast_actual_fx_adjusted_cogs` | 0.6656 | 0 | 0 | C 弱 | Mean of both forecast and actual cost of goods sold, adjusted for currency. |
| `average_forecast_fx_adjusted_cogs` | 0.6656 | 0 | 0 | C 弱 | Mean forecast cost of goods sold, adjusted for currency. |
| `average_forecast_value_cogs` | 0.6656 | 0 | 0 | C 弱 | Mean forecast cost of goods sold for the period. |
| `average_forecast_actual_combined` | 0.5988 | 0 | 0 | C 弱 | Mean of both forecast and actual values for the period. |
| `average_forecast_actual_fx_adjusted` | 0.5988 | 0 | 0 | C 弱 | Mean of forecast and actual values, adjusted for currency. |
| `average_forecast_actual_combined_2` | 0.5717 | 0 | 0 | C 弱 | Mean of both forecast and actual values for the period. |
| `average_forecast_actual_fx_adjusted_2` | 0.5717 | 0 | 0 | C 弱 | Mean of both forecast and actual values, adjusted for currency. |
| `average_forecast_fx_adjusted` | 0.5717 | 0 | 0 | C 弱 | Mean forecast value adjusted for currency effects. |
| `average_forecast_surprise` | 0.5717 | 0 | 0 | C 弱 | Mean difference between actual and forecast values. |
| `average_forecast_value` | 0.5717 | 0 | 0 | C 弱 | Mean forecast value for the period. |
| `average_forecast_actual_combined_bvps` | 0.5545 | 0 | 0 | C 弱 | Mean of both forecast and actual book value per share. |
| `average_forecast_actual_fx_adjusted_bvps` | 0.5545 | 0 | 0 | C 弱 | Mean of both forecast and actual book value per share, adjusted for currency. |
| `average_forecast_fx_adjusted_bvps` | 0.5545 | 0 | 0 | C 弱 | Mean forecast value for book value per share, adjusted for currency. |
| `average_forecast_value_bvps` | 0.5545 | 1 | 1 | C 弱 | Mean forecast book value per share for the period. |
| `average_forecast_actual_fx_adjusted_qtr` | 0.5357 | 0 | 0 | C 弱 | Mean of forecast and actual values for the quarter adjusted for currency. |
| `average_forecast_actual_value_qtr` | 0.5357 | 0 | 0 | C 弱 | Mean of forecast and actual values for the quarter. |

## average_forecast_surprise_* 事件级意外（Forecast Surprise）（10 字段｜覆盖 0.5357–0.8924｜aC=0 的 8 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `average_forecast_surprise_noshareout_qtr` | 0.8924 | 0 | 0 | A 强 | Difference between actual and mean forecast value for the quarter (no share out). |
| `average_forecast_surprise_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Difference between actual and mean forecast value for the quarter (depreciation/amortiz... |
| `average_forecast_surprise_nav_qtr` | 0.7110 | 0 | 0 | B 中 | Difference between actual and mean forecast value for the quarter (net asset value). |
| `average_forecast_surprise_2` | 0.6851 | 0 | 0 | C 弱 | Difference between actual and mean forecast value. |
| `average_forecast_surprise_cogs` | 0.6656 | 1 | 1 | C 弱 | Mean difference between actual and forecast cost of goods sold. |
| `average_forecast_surprise_fx_adjusted_cogs` | 0.6656 | 0 | 0 | C 弱 | Mean difference between actual and forecast cost of goods sold, adjusted for currency. |
| `average_forecast_surprise_fx_adjusted` | 0.5717 | 0 | 0 | C 弱 | Mean difference between actual and forecast values, adjusted for currency. |
| `average_forecast_surprise_bvps` | 0.5545 | 0 | 0 | C 弱 | Mean difference between actual and forecast book value per share. |
| `average_forecast_surprise_fx_adjusted_bvps` | 0.5545 | 0 | 0 | C 弱 | Mean difference between actual and forecast book value per share, adjusted for currency. |
| `average_forecast_surprise_qtr` | 0.5357 | 1 | 1 | C 弱 | Difference between actual and mean forecast value for the quarter. |

## avg_* 历史均值（3mth/12mth prior）（10 字段｜覆盖 0.5489–0.9121｜aC=0 的 9 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `avg_net_income_3mth_prior` | 0.9121 | 0 | 0 | A 强 | Mean NET consensus value 3 months ago |
| `avg_net_income_3mth_prior_fxadj` | 0.9121 | 0 | 0 | A 强 | Mean quarterly Net Income estimate three months ago, adjusted for currency, splits, and... |
| `avg_fcf_estimate` | 0.5966 | 1 | 1 | C 弱 | Current mean of annual Free Cash Flow consensus estimates |
| `avg_fcf_estimate_fxadj` | 0.5966 | 0 | 0 | C 弱 | Current currency/split-adjusted mean consensus estimate for annual Free Cash Flow |
| `avg_fcf_forecast_actual` | 0.5966 | 0 | 0 | C 弱 | Average value of free cash flow across both forecast and actual data points. |
| `avg_fcf_forecast_actual_fxadj` | 0.5966 | 0 | 0 | C 弱 | Average value of free cash flow across forecast and actuals, adjusted for currency effe... |
| `avg_fcf_4wks_prior` | 0.5618 | 0 | 0 | C 弱 | Vendor snapshot of the mean annual Free Cash Flow consensus estimate as of four weeks p... |
| `avg_fcf_4wks_prior_fxadj` | 0.5618 | 0 | 0 | C 弱 | Average free cash flow estimate from four weeks ago, adjusted for currency effects. |
| `avg_fcf_3mth_prior` | 0.5489 | 0 | 0 | C 弱 | Vendor snapshot of the mean annual Free Cash Flow consensus estimate as of three months... |
| `avg_fcf_3mth_prior_fxadj` | 0.5489 | 0 | 0 | C 弱 | Currency and split‑adjusted mean annual Free Cash Flow consensus value from three month... |

## average_analyst_* 分析师均值/预测（7 字段｜覆盖 0.5274–0.8924｜aC=0 的 7 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `average_analyst_projection_noshareout_qtr` | 0.8924 | 0 | 0 | A 强 | Mean value of analyst forecasts for the quarter (no share out). |
| `average_analyst_projection_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Mean value of analyst forecasts for the quarter (depreciation/amortization). |
| `average_analyst_projection_nav_qtr` | 0.7110 | 0 | 0 | B 中 | Mean value of analyst forecasts for the quarter (net asset value). |
| `average_analyst_projection` | 0.6851 | 0 | 0 | C 弱 | Mean value of analyst forecasts for the period. |
| `average_analyst_forecast_value_2` | 0.5988 | 0 | 0 | C 弱 | Mean value of analyst forecasts for the period. |
| `average_analyst_projection_qtr` | 0.5357 | 0 | 0 | C 弱 | Mean value of analyst forecasts for the quarter. |
| `average_analyst_forecast_value` | 0.5274 | 0 | 0 | C 弱 | Mean of analyst forecast values for the period. |

## analyst_estimate_count_* 覆盖人数（6 字段｜覆盖 0.5357–0.8924｜aC=0 的 4 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `analyst_estimate_count_noshareout_qtr` | 0.8924 | 1 | 1 | A 强 | Number of analyst forecasts included in the quarterly consensus (no share out). |
| `analyst_estimate_count_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Number of analyst forecasts included in the quarterly consensus (depreciation/amortizat... |
| `analyst_estimate_count_2` | 0.6851 | 0 | 0 | C 弱 | Number of analyst forecasts included in the consensus. |
| `analyst_estimate_count_cogs` | 0.6656 | 0 | 0 | C 弱 | Number of analyst estimates for cost of goods sold. |
| `analyst_estimate_count_bvps` | 0.5545 | 1 | 1 | C 弱 | Number of analyst estimates for book value per share. |
| `analyst_estimate_count_qtr` | 0.5357 | 0 | 0 | C 弱 | Number of analyst forecasts included in the quarterly consensus. |

## average_projection_* 预测投影（3 字段｜覆盖 0.5357–0.7770｜aC=0 的 3 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `average_projection_fx_adjusted_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Mean analyst forecast value for the quarter adjusted for currency (depreciation/amortiz... |
| `average_projection_fx_adjusted` | 0.6851 | 0 | 0 | C 弱 | Mean analyst forecast value adjusted for currency. |
| `average_projection_fx_adjusted_qtr` | 0.5357 | 0 | 0 | C 弱 | Mean analyst forecast value for the quarter adjusted for currency. |

## average_surprise_* 意外（fx-adjusted 口径）（3 字段｜覆盖 0.5357–0.7770｜aC=0 的 3 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `average_surprise_fx_adjusted_depamort_qtr` | 0.7770 | 0 | 0 | B 中 | Surprise value for mean forecast for the quarter adjusted for currency (depreciation/am... |
| `average_surprise_fx_adjusted` | 0.6851 | 0 | 0 | C 弱 | Surprise value for mean forecast adjusted for currency. |
| `average_surprise_fx_adjusted_qtr` | 0.5357 | 0 | 0 | C 弱 | Surprise value for mean forecast for the quarter adjusted for currency. |

## 其它（逐字段看）（1 字段｜覆盖 0.5717–0.5717｜aC=0 的 1 个）

| 字段 | 覆盖 | uc | aC | 档 | 描述 |
|---|---:|---:|---:|:--:|---|
| `analyst_estimate_count` | 0.5717 | 0 | 0 | C 弱 | Number of analyst estimates included in the consensus. |
