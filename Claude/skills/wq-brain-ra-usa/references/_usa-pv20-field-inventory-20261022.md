# pv20 全字段清单（USA / TOP3000 / D1，2026-10-22 拉取）

平台计数 **1552**（`complete=true`，32 页全量）；字段元数据仅含 id / type / coverage / alphaCount / userCount / description。
分析结论与家族画像见 [`_usa-pv20-field-profile-20261022.md`](_usa-pv20-field-profile-20261022.md)。

| # | field id | type | cov | aC | uC | description |
|---:|---|---|---:|---:|---:|---|
| 1 | `adv20_usd_capped_100m` | MATRIX | 1 | 2 | 2 | Average daily traded value in USD, capped at 100 million. |
| 2 | `adv20_usd_capped_300m` | MATRIX | 1 | 3 | 2 | 20-day average daily traded value in USD, capped at 300 million. |
| 3 | `adv_alternative` | MATRIX | 1 | 2 | 2 | Alternative calculation of average daily traded volume. |
| 4 | `adv_usd_alternative` | MATRIX | 1 | 1 | 1 | Alternative calculation of average daily traded value in USD. |
| 5 | `alternative_slippage_0025` | MATRIX | 1 | 2 | 2 | Alternative estimate of transaction cost slippage with a 0.025 parameter. |
| 6 | `alternative_slippage_2` | MATRIX | 1 | 0 | 0 | Alternative estimate of transaction cost slippage. |
| 7 | `average_daily_value_20d_usd` | MATRIX | 1 | 3 | 3 | Average daily traded value in USD over the past 20 days. |
| 8 | `average_daily_volume_20d` | MATRIX | 1 | 10 | 6 | Average daily trading volume over the past 20 days. |
| 9 | `barra_ustm0_top1000_specific_return` | MATRIX | 0.356 | 2 | 2 | Specific return component for securities in the top 1000 universe as per the Barra model. |
| 10 | `barra_ustm0_top3000_specific_return` | MATRIX | 0.9628 | 45 | 26 | Specific return component for securities in the top 3000 universe as per the Barra model. |
| 11 | `beta_ccmp_250d` | MATRIX | 1 | 2 | 2 | Beta of the security to the NASDAQ Composite Index over the past 250 days. |
| 12 | `beta_dol_250d` | MATRIX | 1 | 4 | 2 | Beta of the asset to the DOL index over a 250-day period. |
| 13 | `beta_gld_250d` | MATRIX | 1 | 1 | 1 | Beta of the security to the SPDR Gold Shares ETF over the past 250 days. |
| 14 | `beta_hui_250d` | MATRIX | 1 | 0 | 0 | Beta of the security to the NYSE Arca Gold BUGS Index over the past 250 days. |
| 15 | `beta_indu_250d` | MATRIX | 1 | 2 | 2 | Beta of the security to the Dow Jones Industrial Average over the past 250 days. |
| 16 | `beta_market_60d` | MATRIX | 1 | 1 | 1 | Beta of the security to the broad market index over the past 60 days. |
| 17 | `beta_ray_250d` | MATRIX | 1 | 0 | 0 | Beta of the security to the RAY index over the past 250 days. |
| 18 | `beta_ray_60d` | MATRIX | 1 | 1 | 1 | Beta of the security to the RAY index over the past 60 days. |
| 19 | `beta_spx_250d` | MATRIX | 1 | 2 | 1 | Beta of the security to the S&P 500 Index over the past 250 days. |
| 20 | `beta_spx_60d` | MATRIX | 1 | 3 | 3 | Beta of the asset to the SPX index over a 60-day period. |
| 21 | `beta_ung_125d_normalized` | MATRIX | 1 | 1 | 1 | Normalized beta of the asset to the UNG index over 125 days. |
| 22 | `beta_ung_250d` | MATRIX | 1 | 2 | 2 | Beta of the asset to the UNG index over a 250-day period. |
| 23 | `beta_ung_60d` | MATRIX | 1 | 0 | 0 | Beta of the security to the US Natural Gas Fund over the past 60 days. |
| 24 | `beta_uso_125d` | MATRIX | 1 | 1 | 1 | Beta of the security to the US Oil ETF over the past 125 days. |
| 25 | `beta_uso_125d_normalized` | MATRIX | 1 | 0 | 0 | Normalized beta of the asset to the USO index over 125 days. |
| 26 | `beta_vix_125d` | MATRIX | 1 | 0 | 0 | Beta of the security to the VIX volatility index over the past 125 days. |
| 27 | `beta_vix_125d_normalized` | MATRIX | 1 | 3 | 2 | Normalized beta of the asset to the VIX index over 125 days. |
| 28 | `beta_vix_250d` | MATRIX | 1 | 1 | 1 | Beta of the security to the VIX volatility index over the past 250 days. |
| 29 | `beta_vix_60d` | MATRIX | 1 | 0 | 0 | Beta of the security to the VIX volatility index over the past 60 days. |
| 30 | `beta_xoi_250d` | MATRIX | 1 | 1 | 1 | Beta of the security to the NYSE Arca Oil Index over the past 250 days. |
| 31 | `beta_xoi_60d` | MATRIX | 1 | 0 | 0 | Beta of the asset to the XOI index over a 60-day period. |
| 32 | `close_to_open_return` | MATRIX | 1 | 10 | 7 | Return from previous close to current open price. |
| 33 | `crowding_top200_specific_return` | MATRIX | 0.069 | 0 | 0 | Specific return for the top 200 assets by crowding measure. |
| 34 | `dow_beta_60d` | MATRIX | 1 | 2 | 2 | Beta of the asset relative to the Dow Jones index over a 60-day period. |
| 35 | `ebt_forecast_7_1` | MATRIX | 0.8274 | 0 | 0 | Algorithmic estimate for earnings before tax, type 7, feature 1. |
| 36 | `ebt_forecast_n1` | MATRIX | 0.7655 | 0 | 0 | Algorithmic estimate for earnings before tax, type N, feature 1. |
| 37 | `ebt_forecast_o11` | MATRIX | 0.7697 | 0 | 0 | Algorithmic estimate for earnings before tax, type O, feature 11. |
| 38 | `ebt_forecast_o12` | MATRIX | 0.7912 | 0 | 0 | Algorithmic estimate for earnings before tax, type O, feature 12. |
| 39 | `ebt_forecast_o3` | MATRIX | 0.559 | 2 | 2 | Algorithmic estimate for earnings before tax, type O, feature 3. |
| 40 | `ebt_forecast_q6` | MATRIX | 0.3982 | 0 | 0 | Algorithmic estimate for earnings before tax, type Q, feature 6. |
| 41 | `ebt_predictor_p4` | MATRIX | 0.5047 | 0 | 0 | Model-derived signal related to earnings before tax, variant P, feature 4. |
| 42 | `ebt_predictor_p8` | MATRIX | 1 | 2 | 2 | Model-derived signal related to earnings before tax, variant P, feature 8. |
| 43 | `ebt_projection_9_5` | MATRIX | 0.6446 | 1 | 1 | Quantitative projection for earnings before tax, type 9, feature 5. |
| 44 | `eps_forecast_0_12` | MATRIX | 0.7921 | 0 | 0 | Algorithmic estimate for earnings per share, type 0, feature 12. |
| 45 | `eps_forecast_0_2` | MATRIX | 0.7799 | 1 | 1 | Algorithmic estimate for earnings per share, type 0, feature 2. |
| 46 | `eps_forecast_0_4` | MATRIX | 0.5414 | 0 | 0 | Algorithmic estimate for earnings per share, type 0, feature 4. |
| 47 | `eps_forecast_0_5` | MATRIX | 0.5414 | 0 | 0 | Algorithmic estimate for earnings per share, type 0, feature 5. |
| 48 | `eps_forecast_0_8` | MATRIX | 1 | 0 | 0 | Algorithmic estimate for earnings per share, type 0, feature 8. |
| 49 | `eps_forecast_0_9` | MATRIX | 0.7928 | 0 | 0 | Algorithmic estimate for earnings per share, type 0, feature 9. |
| 50 | `eps_forecast_6_11` | MATRIX | 0.9492 | 12 | 11 | Algorithmic estimate for earnings per share, type 6, feature 11. |
| 51 | `eps_forecast_6_3` | MATRIX | 0.8942 | 0 | 0 | Algorithmic estimate for earnings per share, type 6, feature 3. |
| 52 | `eps_forecast_6_4` | MATRIX | 0.8942 | 2 | 2 | Algorithmic estimate for earnings per share, type 6, feature 4. |
| 53 | `eps_forecast_6_5` | MATRIX | 0.8942 | 0 | 0 | Algorithmic estimate for earnings per share, type 6, feature 5. |
| 54 | `eps_forecast_6_6` | MATRIX | 0.8965 | 5 | 4 | Algorithmic estimate for earnings per share, type 6, feature 6. |
| 55 | `eps_forecast_6_9` | MATRIX | 0.9536 | 2 | 2 | Algorithmic estimate for earnings per share, type 6, feature 9. |
| 56 | `eps_forecast_7_10` | MATRIX | 0.9497 | 0 | 0 | Algorithmic estimate for earnings per share, type 7, feature 10. |
| 57 | `eps_forecast_7_3` | MATRIX | 0.89 | 0 | 0 | Algorithmic estimate for earnings per share, type 7, feature 3. |
| 58 | `eps_forecast_7_4` | MATRIX | 0.89 | 0 | 0 | Algorithmic estimate for earnings per share, type 7, feature 4. |
| 59 | `eps_forecast_7_5` | MATRIX | 0.89 | 0 | 0 | Algorithmic estimate for earnings per share, type 7, feature 5. |
| 60 | `eps_forecast_7_7` | MATRIX | 0.9386 | 0 | 0 | Algorithmic estimate for earnings per share, type 7, feature 7. |
| 61 | `eps_forecast_7_8` | MATRIX | 1 | 3 | 3 | Algorithmic estimate for earnings per share, type 7, feature 8. |
| 62 | `eps_forecast_7_9` | MATRIX | 0.9549 | 0 | 0 | Algorithmic estimate for earnings per share, type 7, feature 9. |
| 63 | `eps_forecast_n0` | MATRIX | 0.9452 | 0 | 0 | Algorithmic estimate for earnings per share, type N, feature 0. |
| 64 | `eps_forecast_n10` | MATRIX | 0.9288 | 0 | 0 | Algorithmic estimate for earnings per share, type N, feature 10. |
| 65 | `eps_forecast_n11` | MATRIX | 0.9288 | 0 | 0 | Algorithmic estimate for earnings per share, type N, feature 11. |
| 66 | `eps_forecast_n4` | MATRIX | 0.8384 | 0 | 0 | Algorithmic estimate for earnings per share, type N, feature 4. |
| 67 | `eps_forecast_n9` | MATRIX | 0.9452 | 0 | 0 | Algorithmic estimate for earnings per share, type N, feature 9. |
| 68 | `eps_forecast_o0` | MATRIX | 0.9367 | 1 | 1 | Algorithmic estimate for earnings per share, type O, feature 0. |
| 69 | `eps_forecast_o1` | MATRIX | 0.8946 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 1. |
| 70 | `eps_forecast_o11` | MATRIX | 0.917 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 11. |
| 71 | `eps_forecast_o2` | MATRIX | 0.917 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 2. |
| 72 | `eps_forecast_o4` | MATRIX | 0.7976 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 4. |
| 73 | `eps_forecast_o6` | MATRIX | 0.8022 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 6. |
| 74 | `eps_forecast_o7` | MATRIX | 0.8946 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 7. |
| 75 | `eps_forecast_o9` | MATRIX | 0.9367 | 0 | 0 | Algorithmic estimate for earnings per share, type O, feature 9. |
| 76 | `eps_forecast_q1` | MATRIX | 0.8188 | 0 | 0 | Algorithmic estimate for earnings per share, type Q, feature 1. |
| 77 | `eps_forecast_q2` | MATRIX | 0.8626 | 0 | 0 | Algorithmic estimate for earnings per share, type Q, feature 2. |
| 78 | `eps_predictor_p11` | MATRIX | 0.9005 | 0 | 0 | Model-derived signal related to earnings per share, variant P, feature 11. |
| 79 | `eps_predictor_p3` | MATRIX | 0.7368 | 0 | 0 | Model-derived signal related to earnings per share, variant P, feature 3. |
| 80 | `eps_predictor_p5` | MATRIX | 0.7368 | 1 | 1 | Model-derived signal related to earnings per share, variant P, feature 5. |
| 81 | `eps_predictor_p7` | MATRIX | 0.8642 | 0 | 0 | Model-derived signal related to earnings per share, variant P, feature 7. |
| 82 | `eps_predictor_p9` | MATRIX | 0.9247 | 0 | 0 | Model-derived signal related to earnings per share, variant P, feature 9. |
| 83 | `eps_projection_8_0` | MATRIX | 0.9526 | 0 | 0 | Quantitative projection for earnings per share, type 8, feature 0. |
| 84 | `eps_projection_8_5` | MATRIX | 0.8809 | 2 | 1 | Quantitative projection for earnings per share, type 8, feature 5. |
| 85 | `eps_projection_8_8` | MATRIX | 1 | 0 | 0 | Quantitative projection for earnings per share, type 8, feature 8. |
| 86 | `eps_projection_8_9` | MATRIX | 0.9526 | 0 | 0 | Quantitative projection for earnings per share, type 8, feature 9. |
| 87 | `eps_projection_9_0` | MATRIX | 0.9537 | 1 | 1 | Quantitative projection for earnings per share, type 9, feature 0. |
| 88 | `eps_projection_9_10` | MATRIX | 0.9411 | 0 | 0 | Quantitative projection for earnings per share, type 9, feature 10. |
| 89 | `eps_projection_9_4` | MATRIX | 0.8619 | 0 | 0 | Quantitative projection for earnings per share, type 9, feature 4. |
| 90 | `etf_top300_00_grouping` | MATRIX | 0.1098 | 0 | 0 | Cluster or group assignment for the ETF within the top 300 universe. |
| 91 | `etf_top300_25_cluster` | MATRIX | 0.1098 | 0 | 0 | Cluster assignment for securities in the top 300 ETFs by a specific metric. |
| 92 | `etf_top300_50_grouping` | MATRIX | 0.1098 | 0 | 0 | Cluster or group assignment for the ETF within the top 300 universe (variant 50). |
| 93 | `euro_beta_250d` | MATRIX | 1 | 0 | 0 | Beta of the asset relative to the euro over a 250-day period. |
| 94 | `euro_beta_60d` | MATRIX | 1 | 1 | 1 | Beta of the asset relative to the euro over a 60-day period. |
| 95 | `extra_riskfactor_weights` | MATRIX | 1 | 0 | 0 | Weights assigned to extra risk factors in the model. |
| 96 | `firm_market_capitalization` | MATRIX | 0.5 | 2 | 2 | Total market value of a company's outstanding shares. |
| 97 | `forward_estimate_signal_7_10` | MATRIX | 0.9193 | 0 | 0 | Numeric value representing the tenth feature of the seventh predictive indicator derived from forward-looking  |
| 98 | `forward_estimate_signal_7_6` | MATRIX | 0.8304 | 0 | 0 | Numeric value representing the sixth feature of the seventh predictive indicator derived from forward-looking  |
| 99 | `forward_estimate_signal_8_4` | MATRIX | 0.8089 | 0 | 0 | Numeric value representing the fourth feature of the eighth predictive indicator derived from forward-looking  |
| 100 | `forward_estimate_signal_9_5` | MATRIX | 0.7757 | 0 | 0 | Numeric value representing the fifth feature of the ninth predictive indicator derived from forward-looking es |
| 101 | `forward_estimate_signal_n11` | MATRIX | 0.8843 | 0 | 0 | Numeric value representing the eleventh N-type predictive indicator derived from forward-looking estimates. |
| 102 | `forward_estimate_signal_n12` | MATRIX | 0.9076 | 0 | 0 | Numeric value representing the twelfth N-type predictive indicator derived from forward-looking estimates. |
| 103 | `forward_estimate_signal_n3` | MATRIX | 0.7358 | 0 | 0 | Numeric value representing the third N-type predictive indicator derived from forward-looking estimates. |
| 104 | `forward_estimate_signal_n4` | MATRIX | 0.7358 | 0 | 0 | Numeric value representing the fourth N-type predictive indicator derived from forward-looking estimates. |
| 105 | `forward_estimate_signal_n9` | MATRIX | 0.9078 | 0 | 0 | Numeric value representing the ninth N-type predictive indicator derived from forward-looking estimates. |
| 106 | `forward_estimate_signal_o1` | MATRIX | 0.8342 | 0 | 0 | Numeric value representing the first O-type predictive indicator derived from forward-looking estimates. |
| 107 | `forward_estimate_signal_o9` | MATRIX | 0.8887 | 0 | 0 | Numeric value representing the ninth O-type predictive indicator derived from forward-looking estimates. |
| 108 | `forward_estimate_signal_p8` | MATRIX | 1 | 2 | 2 | Numeric value representing the eighth P-type predictive indicator derived from forward-looking estimates. |
| 109 | `forward_estimate_signal_q11` | MATRIX | 0.7771 | 0 | 0 | Numeric value representing the eleventh Q-type predictive indicator derived from forward-looking estimates. |
| 110 | `forward_estimate_signal_q2` | MATRIX | 0.7771 | 0 | 0 | Numeric value representing the second Q-type predictive indicator derived from forward-looking estimates. |
| 111 | `forward_estimate_signal_q3` | MATRIX | 0.4426 | 2 | 2 | Numeric value representing the third Q-type predictive indicator derived from forward-looking estimates. |
| 112 | `gold_beta_60d` | MATRIX | 1 | 1 | 1 | Beta of the asset relative to gold over a 60-day period. |
| 113 | `gold_mining_beta_60d` | MATRIX | 1 | 0 | 0 | Beta of the asset relative to the gold mining index over a 60-day period. |
| 114 | `group_slippage_estimate` | MATRIX | 1 | 1 | 1 | Estimated transaction cost slippage for a group of securities. |
| 115 | `ibes_ebt_group6_signal_12` | MATRIX | 0.8511 | 13 | 4 | Group 6 predictive signal number 12 for pre-tax earnings. |
| 116 | `ibes_ebt_group6_signal_5` | MATRIX | 0.708 | 0 | 0 | Group 6 predictive signal number 5 for pre-tax earnings. |
| 117 | `ibes_ebt_group8_signal_0` | MATRIX | 0.8466 | 1 | 1 | Group 8 predictive signal number 0 for pre-tax earnings. |
| 118 | `ibes_ebt_group8_signal_1` | MATRIX | 0.8167 | 0 | 0 | Group 8 predictive signal number 1 for pre-tax earnings. |
| 119 | `ibes_ebt_group8_signal_4` | MATRIX | 0.6831 | 3 | 2 | Group 8 predictive signal number 4 for pre-tax earnings. |
| 120 | `ibes_ebt_group8_signal_5` | MATRIX | 0.6831 | 0 | 0 | Group 8 predictive signal number 5 for pre-tax earnings. |
| 121 | `ibes_ebt_group8_signal_6` | MATRIX | 0.6877 | 0 | 0 | Group 8 predictive signal number 6 for pre-tax earnings. |
| 122 | `ibes_ebt_group8_signal_7` | MATRIX | 0.8167 | 1 | 1 | Group 8 predictive signal number 7 for pre-tax earnings. |
| 123 | `ibes_ebt_group8_signal_8` | MATRIX | 1 | 0 | 0 | Group 8 predictive signal number 8 for pre-tax earnings. |
| 124 | `ibes_ebt_group9_signal_2` | MATRIX | 0.8206 | 0 | 0 | Group 9 predictive signal number 2 for pre-tax earnings. |
| 125 | `ibes_ebt_group9_signal_4` | MATRIX | 0.6446 | 0 | 0 | Group 9 predictive signal number 4 for pre-tax earnings. |
| 126 | `ibes_ebt_group9_signal_9` | MATRIX | 0.8438 | 0 | 0 | Group 9 predictive signal number 9 for pre-tax earnings. |
| 127 | `ibes_ebt_neutral_signal_0` | MATRIX | 0.8164 | 0 | 0 | Neutral predictive signal number 0 for pre-tax earnings. |
| 128 | `ibes_ebt_neutral_signal_11` | MATRIX | 0.7891 | 3 | 3 | Neutral predictive signal number 11 for pre-tax earnings. |
| 129 | `ibes_ebt_neutral_signal_12` | MATRIX | 0.8148 | 0 | 0 | Neutral predictive signal number 12 for pre-tax earnings. |
| 130 | `ibes_ebt_neutral_signal_2` | MATRIX | 0.7891 | 1 | 1 | Neutral predictive signal number 2 for pre-tax earnings. |
| 131 | `ibes_ebt_neutral_signal_6` | MATRIX | 0.6079 | 0 | 0 | Neutral predictive signal number 6 for pre-tax earnings. |
| 132 | `ibes_ebt_other_signal_4` | MATRIX | 0.559 | 0 | 0 | Other predictive signal number 4 for pre-tax earnings. |
| 133 | `ibes_ebt_other_signal_7` | MATRIX | 0.7452 | 0 | 0 | Other predictive signal number 7 for pre-tax earnings. |
| 134 | `ibes_ebt_other_signal_8` | MATRIX | 1 | 0 | 0 | Other predictive signal number 8 for pre-tax earnings. |
| 135 | `ibes_ebt_other_signal_9` | MATRIX | 0.793 | 0 | 0 | Other predictive signal number 9 for pre-tax earnings. |
| 136 | `ibes_ebt_positive_signal_9` | MATRIX | 0.7766 | 0 | 0 | Positive predictive signal number 9 for pre-tax earnings. |
| 137 | `ibes_ebt_quarterly_signal_1` | MATRIX | 0.646 | 0 | 0 | Quarterly predictive signal number 1 for pre-tax earnings. |
| 138 | `ibes_ebt_quarterly_signal_8` | MATRIX | 1 | 0 | 0 | Quarterly predictive signal number 8 for pre-tax earnings. |
| 139 | `ibes_gps_group6_signal_0` | MATRIX | 0.9345 | 5 | 4 | Group 6 predictive signal number 0 for gross profit. |
| 140 | `ibes_gps_group6_signal_11` | MATRIX | 0.9294 | 3 | 3 | Group 6 predictive signal number 11 for gross profit. |
| 141 | `ibes_gps_group6_signal_12` | MATRIX | 0.9339 | 2 | 2 | Group 6 predictive signal number 12 for gross profit. |
| 142 | `ibes_gps_group6_signal_3` | MATRIX | 0.8611 | 0 | 0 | Group 6 predictive signal number 3 for gross profit. |
| 143 | `ibes_gps_group6_signal_4` | MATRIX | 0.8611 | 0 | 0 | Group 6 predictive signal number 4 for gross profit. |
| 144 | `ibes_gps_group7_signal_1` | MATRIX | 0.915 | 0 | 0 | Group 7 predictive signal number 1 for gross profit. |
| 145 | `ibes_gps_group7_signal_6` | MATRIX | 0.8557 | 0 | 0 | Group 7 predictive signal number 6 for gross profit. |
| 146 | `ibes_gps_group7_signal_8` | MATRIX | 1 | 0 | 0 | Group 7 predictive signal number 8 for gross profit. |
| 147 | `ibes_gps_group8_signal_0` | MATRIX | 0.9318 | 0 | 0 | Group 8 predictive signal number 0 for gross profit. |
| 148 | `ibes_gps_group8_signal_10` | MATRIX | 0.9238 | 1 | 1 | Group 8 predictive signal number 10 for gross profit. |
| 149 | `ibes_gps_group8_signal_2` | MATRIX | 0.9238 | 0 | 0 | Group 8 predictive signal number 2 for gross profit. |
| 150 | `ibes_gps_group8_signal_4` | MATRIX | 0.8397 | 0 | 0 | Group 8 predictive signal number 4 for gross profit. |
| 151 | `ibes_gps_group8_signal_5` | MATRIX | 0.8397 | 0 | 0 | Group 8 predictive signal number 5 for gross profit. |
| 152 | `ibes_gps_group8_signal_6` | MATRIX | 0.8434 | 0 | 0 | Group 8 predictive signal number 6 for gross profit. |
| 153 | `ibes_gps_group9_signal_0` | MATRIX | 0.9302 | 0 | 0 | Group 9 predictive signal number 0 for gross profit. |
| 154 | `ibes_gps_group9_signal_2` | MATRIX | 0.9141 | 2 | 2 | Group 9 predictive signal number 2 for gross profit. |
| 155 | `ibes_gps_group9_signal_3` | MATRIX | 0.8076 | 0 | 0 | Group 9 predictive signal number 3 for gross profit. |
| 156 | `ibes_gps_group9_signal_4` | MATRIX | 0.8076 | 0 | 0 | Group 9 predictive signal number 4 for gross profit. |
| 157 | `ibes_gps_group9_signal_6` | MATRIX | 0.8113 | 0 | 0 | Group 9 predictive signal number 6 for gross profit. |
| 158 | `ibes_gps_group9_signal_7` | MATRIX | 0.8936 | 0 | 0 | Group 9 predictive signal number 7 for gross profit. |
| 159 | `ibes_gps_neutral_signal_0` | MATRIX | 0.9184 | 0 | 0 | Neutral predictive signal number 0 for gross profit. |
| 160 | `ibes_gps_neutral_signal_1` | MATRIX | 0.8772 | 0 | 0 | Neutral predictive signal number 1 for gross profit. |
| 161 | `ibes_gps_neutral_signal_12` | MATRIX | 0.918 | 0 | 0 | Neutral predictive signal number 12 for gross profit. |
| 162 | `ibes_gps_other_signal_4` | MATRIX | 0.7008 | 0 | 0 | Other predictive signal number 4 for gross profit. |
| 163 | `ibes_gps_other_signal_8` | MATRIX | 1 | 2 | 2 | Other predictive signal number 8 for gross profit. |
| 164 | `ibes_gps_positive_signal_1` | MATRIX | 0.7991 | 0 | 0 | Positive predictive signal number 1 for gross profit. |
| 165 | `ibes_gps_positive_signal_11` | MATRIX | 0.8493 | 0 | 0 | Positive predictive signal number 11 for gross profit. |
| 166 | `ibes_gps_positive_signal_12` | MATRIX | 0.887 | 0 | 0 | Positive predictive signal number 12 for gross profit. |
| 167 | `ibes_gps_positive_signal_3` | MATRIX | 0.6043 | 0 | 0 | Positive predictive signal number 3 for gross profit. |
| 168 | `ibes_gps_positive_signal_7` | MATRIX | 0.7991 | 0 | 0 | Positive predictive signal number 7 for gross profit. |
| 169 | `ibes_gps_positive_signal_9` | MATRIX | 0.8875 | 0 | 0 | Positive predictive signal number 9 for gross profit. |
| 170 | `ibes_gps_quarterly_signal_1` | MATRIX | 0.7123 | 1 | 1 | Quarterly predictive signal number 1 for gross profit. |
| 171 | `ibes_gps_quarterly_signal_10` | MATRIX | 0.7809 | 0 | 0 | Quarterly predictive signal number 10 for gross profit. |
| 172 | `ibes_gps_quarterly_signal_12` | MATRIX | 0.8607 | 0 | 0 | Quarterly predictive signal number 12 for gross profit. |
| 173 | `ibes_gps_quarterly_signal_3` | MATRIX | 0.4407 | 0 | 0 | Quarterly predictive signal number 3 for gross profit. |
| 174 | `ibes_gps_quarterly_signal_4` | MATRIX | 0.4407 | 0 | 0 | Quarterly predictive signal number 4 for gross profit. |
| 175 | `ibes_gps_quarterly_signal_5` | MATRIX | 0.4407 | 0 | 0 | Quarterly predictive signal number 5 for gross profit. |
| 176 | `ibes_gps_quarterly_signal_6` | MATRIX | 0.4523 | 0 | 0 | Quarterly predictive signal number 6 for gross profit. |
| 177 | `ibes_pre_group6_signal_0` | MATRIX | 0.9287 | 2 | 2 | Group 6 predictive signal number 0 for pre-tax profit. |
| 178 | `ibes_pre_group6_signal_1` | MATRIX | 0.9092 | 0 | 0 | Group 6 predictive signal number 1 for pre-tax profit. |
| 179 | `ibes_pre_group6_signal_3` | MATRIX | 0.8343 | 1 | 1 | Group 6 predictive signal number 3 for pre-tax profit. |
| 180 | `ibes_pre_group7_signal_12` | MATRIX | 0.9269 | 0 | 0 | Group 7 predictive signal number 12 for pre-tax profit. |
| 181 | `ibes_pre_group7_signal_2` | MATRIX | 0.9193 | 0 | 0 | Group 7 predictive signal number 2 for pre-tax profit. |
| 182 | `ibes_pre_group7_signal_5` | MATRIX | 0.8249 | 0 | 0 | Group 7 predictive signal number 5 for pre-tax profit. |
| 183 | `ibes_pre_group7_signal_7` | MATRIX | 0.9042 | 0 | 0 | Group 7 predictive signal number 7 for pre-tax profit. |
| 184 | `ibes_pre_group7_signal_8` | MATRIX | 1 | 2 | 2 | Group 7 predictive signal number 8 for pre-tax profit. |
| 185 | `ibes_pre_group7_signal_9` | MATRIX | 0.927 | 0 | 0 | Group 7 predictive signal number 9 for pre-tax profit. |
| 186 | `ibes_pre_group8_signal_1` | MATRIX | 0.8979 | 0 | 0 | Group 8 predictive signal number 1 for pre-tax profit. |
| 187 | `ibes_pre_group8_signal_7` | MATRIX | 0.8979 | 1 | 1 | Group 8 predictive signal number 7 for pre-tax profit. |
| 188 | `ibes_pre_group8_signal_9` | MATRIX | 0.9238 | 0 | 0 | Group 8 predictive signal number 9 for pre-tax profit. |
| 189 | `ibes_pre_group9_signal_12` | MATRIX | 0.9207 | 0 | 0 | Group 9 predictive signal number 12 for pre-tax profit. |
| 190 | `ibes_pre_group9_signal_4` | MATRIX | 0.7757 | 0 | 0 | Group 9 predictive signal number 4 for pre-tax profit. |
| 191 | `ibes_pre_neutral_signal_0` | MATRIX | 0.9078 | 1 | 1 | Neutral predictive signal number 0 for pre-tax profit. |
| 192 | `ibes_pre_neutral_signal_6` | MATRIX | 0.7423 | 1 | 1 | Neutral predictive signal number 6 for pre-tax profit. |
| 193 | `ibes_pre_other_signal_0` | MATRIX | 0.8887 | 1 | 1 | Other predictive signal number 0 for pre-tax profit. |
| 194 | `ibes_pre_positive_signal_10` | MATRIX | 0.8336 | 0 | 0 | Positive predictive signal number 10 for pre-tax profit. |
| 195 | `ibes_pre_positive_signal_3` | MATRIX | 0.5921 | 0 | 0 | Positive predictive signal number 3 for pre-tax profit. |
| 196 | `ibes_pre_quarterly_signal_0` | MATRIX | 0.843 | 0 | 0 | Quarterly predictive signal number 0 for pre-tax profit. |
| 197 | `ibes_pre_quarterly_signal_1` | MATRIX | 0.7087 | 0 | 0 | Quarterly predictive signal number 1 for pre-tax profit. |
| 198 | `ibes_pre_quarterly_signal_5` | MATRIX | 0.4426 | 0 | 0 | Quarterly predictive signal number 5 for pre-tax profit. |
| 199 | `ibes_pre_quarterly_signal_6` | MATRIX | 0.452 | 0 | 0 | Quarterly predictive signal number 6 for pre-tax profit. |
| 200 | `ibes_pre_quarterly_signal_9` | MATRIX | 0.843 | 2 | 2 | Quarterly predictive signal number 9 for pre-tax profit. |
| 201 | `implied_volatility_250d` | MATRIX | 0.9469 | 12 | 6 | Implied volatility calculated over the past 250 trading days. |
| 202 | `industry_sector_classification_17` | MATRIX | 0.5 | 0 | 0 | The industry sector to which the company belongs. |
| 203 | `industry_top3000_1_20` | MATRIX | 1 | 0 | 0 | Indicator for membership in the top 20 industries by market cap within the top 3000 securities. |
| 204 | `industry_top3000_1_5` | MATRIX | 1 | 0 | 0 | Indicator for membership in the top 5 industries by market cap within the top 3000 securities. |
| 205 | `issuer_composite_score` | MATRIX | 0.5 | 0 | 0 | A numerical value representing a composite or ranking score for the company. |
| 206 | `issuer_legal_name_15` | MATRIX | 0.5 | 0 | 0 | The official name of the company or entity issuing the security. |
| 207 | `last_close_to_open_return` | MATRIX | 1 | 3 | 2 | Return from previous market close to current market open. |
| 208 | `log_return_5d_normalized` | MATRIX | 1 | 0 | 0 | Normalized log returns over a 5-day period. |
| 209 | `market_beta_250d` | MATRIX | 1 | 1 | 1 | Beta of the asset relative to the broad market over a 250-day period. |
| 210 | `nasdaq_beta_60d` | MATRIX | 1 | 5 | 1 | Beta of the asset relative to the Nasdaq index over a 60-day period. |
| 211 | `natural_gas_beta_125d` | MATRIX | 1 | 0 | 0 | Beta of the asset relative to natural gas over a 125-day period. |
| 212 | `negative_implied_volatility_250d` | MATRIX | 0.9469 | 0 | 0 | Negative implied volatility calculated over the past 250 trading days. |
| 213 | `negative_volatility_250d` | MATRIX | 1 | 3 | 3 | Negative volatility calculated over the past 250 trading days. |
| 214 | `net_6_feature11_predictor` | MATRIX | 0.9383 | 3 | 2 | Predictive feature 11 from indicator group 6 in the NET model. |
| 215 | `net_6_feature5_predictor` | MATRIX | 0.8715 | 0 | 0 | Predictive feature 5 from indicator group 6 in the NET model. |
| 216 | `net_7_feature0_predictor` | MATRIX | 0.9433 | 0 | 0 | Predictive feature 0 from indicator group 7 in the NET model. |
| 217 | `net_8_feature0_predictor` | MATRIX | 0.9408 | 0 | 0 | Predictive feature 0 from indicator group 8 in the NET model. |
| 218 | `net_8_feature10_predictor` | MATRIX | 0.9317 | 0 | 0 | Predictive feature 10 from indicator group 8 in the NET model. |
| 219 | `net_8_feature11_predictor` | MATRIX | 0.9317 | 0 | 0 | Predictive feature 11 from indicator group 8 in the NET model. |
| 220 | `net_9_feature11_predictor` | MATRIX | 0.9221 | 0 | 0 | Predictive feature 11 from indicator group 9 in the NET model. |
| 221 | `net_9_feature3_predictor` | MATRIX | 0.8158 | 0 | 0 | Predictive feature 3 from indicator group 9 in the NET model. |
| 222 | `net_9_feature9_predictor` | MATRIX | 0.9387 | 0 | 0 | Predictive feature 9 from indicator group 9 in the NET model. |
| 223 | `net_earnings_projection_8_1` | MATRIX | 0.9145 | 0 | 0 | Quantitative projection for net earnings, type 8, feature 1. |
| 224 | `net_earnings_projection_8_3` | MATRIX | 0.8493 | 0 | 0 | Quantitative projection for net earnings, type 8, feature 3. |
| 225 | `net_earnings_projection_8_4` | MATRIX | 0.8493 | 0 | 0 | Quantitative projection for net earnings, type 8, feature 4. |
| 226 | `net_earnings_projection_8_5` | MATRIX | 0.8493 | 0 | 0 | Quantitative projection for net earnings, type 8, feature 5. |
| 227 | `net_earnings_projection_8_7` | MATRIX | 0.9145 | 0 | 0 | Quantitative projection for net earnings, type 8, feature 7. |
| 228 | `net_earnings_projection_8_9` | MATRIX | 0.9408 | 0 | 0 | Quantitative projection for net earnings, type 8, feature 9. |
| 229 | `net_earnings_projection_9_2` | MATRIX | 0.9221 | 0 | 0 | Quantitative projection for net earnings, type 9, feature 2. |
| 230 | `net_earnings_projection_9_5` | MATRIX | 0.8158 | 0 | 0 | Quantitative projection for net earnings, type 9, feature 5. |
| 231 | `net_income_forecast_6_0` | MATRIX | 0.9443 | 0 | 0 | Algorithmic estimate for net income, type 6, feature 0. |
| 232 | `net_income_forecast_6_10` | MATRIX | 0.9383 | 0 | 0 | Algorithmic estimate for net income, type 6, feature 10. |
| 233 | `net_income_forecast_6_8` | MATRIX | 1 | 3 | 3 | Algorithmic estimate for net income, type 6, feature 8. |
| 234 | `net_income_forecast_7_11` | MATRIX | 0.9361 | 0 | 0 | Algorithmic estimate for net income, type 7, feature 11. |
| 235 | `net_income_forecast_n11` | MATRIX | 0.9044 | 0 | 0 | Algorithmic estimate for net income, type N, feature 11. |
| 236 | `net_income_forecast_o0` | MATRIX | 0.9114 | 0 | 0 | Algorithmic estimate for net income, type O, feature 0. |
| 237 | `net_income_forecast_o1` | MATRIX | 0.8542 | 0 | 0 | Algorithmic estimate for net income, type O, feature 1. |
| 238 | `net_income_forecast_o11` | MATRIX | 0.8832 | 0 | 0 | Algorithmic estimate for net income, type O, feature 11. |
| 239 | `net_income_forecast_q3` | MATRIX | 0.487 | 0 | 0 | Algorithmic estimate for net income, type Q, feature 3. |
| 240 | `net_n_feature12_predictor` | MATRIX | 0.9277 | 0 | 0 | Predictive feature 12 from indicator group N in the NET model. |
| 241 | `net_o_feature10_predictor` | MATRIX | 0.8832 | 0 | 0 | Predictive feature 10 from indicator group O in the NET model. |
| 242 | `net_o_feature4_predictor` | MATRIX | 0.7112 | 0 | 0 | Predictive feature 4 from indicator group O in the NET model. |
| 243 | `net_o_feature8_predictor` | MATRIX | 1 | 1 | 1 | Predictive feature 8 from indicator group O in the NET model. |
| 244 | `net_p_feature0_predictor` | MATRIX | 0.8952 | 0 | 0 | Predictive feature 0 from indicator group P in the NET model. |
| 245 | `net_p_feature6_predictor` | MATRIX | 0.636 | 0 | 0 | Predictive feature 6 from indicator group P in the NET model. |
| 246 | `net_profitability_predictor_p1` | MATRIX | 0.8052 | 0 | 0 | Model-derived signal related to net profit, variant P, feature 1. |
| 247 | `net_profitability_predictor_p10` | MATRIX | 0.8536 | 0 | 0 | Model-derived signal related to net profit, variant P, feature 10. |
| 248 | `net_profitability_predictor_p11` | MATRIX | 0.8536 | 0 | 0 | Model-derived signal related to net profit, variant P, feature 11. |
| 249 | `net_profitability_predictor_p5` | MATRIX | 0.6289 | 0 | 0 | Model-derived signal related to net profit, variant P, feature 5. |
| 250 | `net_profitability_predictor_p7` | MATRIX | 0.8052 | 0 | 0 | Model-derived signal related to net profit, variant P, feature 7. |
| 251 | `net_q_feature12_predictor` | MATRIX | 0.8689 | 0 | 0 | Quantitative predictive feature number 12 from the NET model. |
| 252 | `net_q_feature8_predictor` | MATRIX | 1 | 0 | 0 | Quantitative predictive feature number 8 from the NET model. |
| 253 | `net_q_feature9_predictor` | MATRIX | 0.8696 | 0 | 0 | Quantitative predictive feature number 9 from the NET model. |
| 254 | `oil_beta_250d` | MATRIX | 1 | 5 | 3 | Beta of the asset relative to oil over a 250-day period. |
| 255 | `oil_beta_60d` | MATRIX | 1 | 0 | 0 | Beta of the asset relative to oil over a 60-day period. |
| 256 | `open_to_close_return` | MATRIX | 1 | 19 | 15 | Return from market open to market close. |
| 257 | `open_to_vwap_return` | MATRIX | 0.9993 | 18 | 11 | Return from market open to volume-weighted average price. |
| 258 | `opr_6_feature10_predictor` | MATRIX | 0.6441 | 0 | 0 | Predictive feature 10 from indicator group 6 in the OPR model. |
| 259 | `opr_6_feature11_predictor` | MATRIX | 0.6441 | 0 | 0 | Predictive feature 11 from indicator group 6 in the OPR model. |
| 260 | `opr_6_feature12_predictor` | MATRIX | 0.654 | 0 | 0 | Predictive feature 12 from indicator group 6 in the OPR model. |
| 261 | `opr_6_feature4_predictor` | MATRIX | 0.4303 | 0 | 0 | Predictive feature 4 from indicator group 6 in the OPR model. |
| 262 | `opr_6_feature6_predictor` | MATRIX | 0.4461 | 0 | 0 | Predictive feature 6 from indicator group 6 in the OPR model. |
| 263 | `opr_7_feature12_predictor` | MATRIX | 0.6411 | 0 | 0 | Predictive feature 12 from indicator group 7 in the OPR model. |
| 264 | `opr_7_feature1_predictor` | MATRIX | 0.6147 | 0 | 0 | Predictive feature 1 from indicator group 7 in the OPR model. |
| 265 | `opr_7_feature6_predictor` | MATRIX | 0.4361 | 0 | 0 | Predictive feature 6 from indicator group 7 in the OPR model. |
| 266 | `opr_7_feature7_predictor` | MATRIX | 0.6147 | 0 | 0 | Predictive feature 7 from indicator group 7 in the OPR model. |
| 267 | `opr_8_feature11_predictor` | MATRIX | 0.62 | 0 | 0 | Predictive feature 11 from indicator group 8 in the OPR model. |
| 268 | `opr_8_feature2_predictor` | MATRIX | 0.62 | 0 | 0 | Predictive feature 2 from indicator group 8 in the OPR model. |
| 269 | `opr_8_feature4_predictor` | MATRIX | 0.4105 | 0 | 0 | Predictive feature 4 from indicator group 8 in the OPR model. |
| 270 | `opr_8_feature5_predictor` | MATRIX | 0.4105 | 0 | 0 | Predictive feature 5 from indicator group 8 in the OPR model. |
| 271 | `opr_8_feature6_predictor` | MATRIX | 0.4234 | 0 | 0 | Predictive feature 6 from indicator group 8 in the OPR model. |
| 272 | `opr_8_feature7_predictor` | MATRIX | 0.5921 | 0 | 0 | Predictive feature 7 from indicator group 8 in the OPR model. |
| 273 | `opr_8_feature9_predictor` | MATRIX | 0.6331 | 0 | 0 | Predictive feature 9 from indicator group 8 in the OPR model. |
| 274 | `opr_9_feature3_predictor` | MATRIX | 0.3832 | 0 | 0 | Predictive feature 3 from indicator group 9 in the OPR model. |
| 275 | `opr_9_feature5_predictor` | MATRIX | 0.3832 | 0 | 0 | Predictive feature 5 from indicator group 9 in the OPR model. |
| 276 | `opr_9_feature6_predictor` | MATRIX | 0.3913 | 0 | 0 | Predictive feature 6 from indicator group 9 in the OPR model. |
| 277 | `opr_9_feature8_predictor` | MATRIX | 1 | 0 | 0 | Predictive feature 8 from indicator group 9 in the OPR model. |
| 278 | `opr_9_feature9_predictor` | MATRIX | 0.6264 | 0 | 0 | Predictive feature 9 from indicator group 9 in the OPR model. |
| 279 | `opr_n_feature10_predictor` | MATRIX | 0.5527 | 0 | 0 | Predictive feature 10 from indicator group N in the OPR model. |
| 280 | `opr_n_feature12_predictor` | MATRIX | 0.5969 | 0 | 0 | Predictive feature 12 from indicator group N in the OPR model. |
| 281 | `opr_n_feature1_predictor` | MATRIX | 0.5287 | 0 | 0 | Predictive feature 1 from indicator group N in the OPR model. |
| 282 | `opr_n_feature5_predictor` | MATRIX | 0.3363 | 0 | 0 | Predictive feature 5 from indicator group N in the OPR model. |
| 283 | `opr_n_feature6_predictor` | MATRIX | 0.3438 | 0 | 0 | Predictive feature 6 from indicator group N in the OPR model. |
| 284 | `opr_n_feature7_predictor` | MATRIX | 0.5287 | 0 | 0 | Predictive feature 7 from indicator group N in the OPR model. |
| 285 | `opr_n_feature8_predictor` | MATRIX | 1 | 0 | 0 | Predictive feature 8 from indicator group N in the OPR model. |
| 286 | `opr_o_feature3_predictor` | MATRIX | 0.2793 | 0 | 0 | Predictive feature 3 from indicator group O in the OPR model. |
| 287 | `opr_o_feature4_predictor` | MATRIX | 0.2793 | 0 | 0 | Predictive feature 4 from indicator group O in the OPR model. |
| 288 | `opr_o_feature5_predictor` | MATRIX | 0.2793 | 0 | 0 | Predictive feature 5 from indicator group O in the OPR model. |
| 289 | `opr_o_feature6_predictor` | MATRIX | 0.2897 | 0 | 0 | Predictive feature 6 from indicator group O in the OPR model. |
| 290 | `opr_p_feature10_predictor` | MATRIX | 0.484 | 0 | 0 | Predictive feature 10 from indicator group P in the OPR model. |
| 291 | `opr_q_feature10_predictor` | MATRIX | 0.3862 | 0 | 0 | Quantitative predictive feature number 10 from the OPR model. |
| 292 | `opr_q_feature12_predictor` | MATRIX | 0.4988 | 0 | 0 | Quantitative predictive feature number 12 from the OPR model. |
| 293 | `pv20_02_5_fma_rd` | MATRIX | 0.5 | 75 | 42 | Chaikin oscillator value over a 5-20 day period. |
| 294 | `pv20_02_5_rvp_rd` | MATRIX | 0.5 | 24 | 9 | Price-volume ratio over a 5-20 day period. |
| 295 | `pv20_02_cdts_rd` | MATRIX | 0.5 | 5 | 5 | Standard deviation of returns over a 20-day period. |
| 296 | `pv20_02_cmlh_rd` | MATRIX | 0.5 | 17 | 11 | High-low midpoint change over a 20-day period. |
| 297 | `pv20_02_lmh_rd` | MATRIX | 0.5 | 16 | 8 | High minus low price range over a 20-day period. |
| 298 | `pv20_02_spcd_rd` | MATRIX | 0.5 | 23 | 10 | Daily closing price spread over a 20-day period. |
| 299 | `pv20_02_spcda_rd` | MATRIX | 0.5 | 18 | 9 | Adjusted daily closing price spread over a 20-day period. |
| 300 | `pv20_03_cmlh_rd` | MATRIX | 0.5 | 12 | 8 | High-low midpoint change over a 30-day period. |
| 301 | `pv20_04_5_rvp_rd` | MATRIX | 0.5 | 5 | 4 | Price-volume ratio over a 5-40 day period. |
| 302 | `pv20_04_cdts_rd` | MATRIX | 0.5 | 23 | 9 | Standard deviation of returns over a 40-day period. |
| 303 | `pv20_04_qil_rd` | MATRIX | 0.5 | 6 | 5 | Liquidity measure over a 40-day period. |
| 304 | `pv20_052_52_rvp_rd` | MATRIX | 0.5 | 4 | 4 | Price-volume ratio over a 25-250 day period. |
| 305 | `pv20_052_5_rvp_rd` | MATRIX | 0.5 | 5 | 5 | Price-volume ratio over a 5-250 day period. |
| 306 | `pv20_052_cdts_rd` | MATRIX | 0.5 | 11 | 7 | Standard deviation of returns over a 250-day period. |
| 307 | `pv20_052_cmlh_rd` | MATRIX | 0.5 | 23 | 16 | High-low midpoint change over a 250-day period. |
| 308 | `pv20_052_lmh_rd` | MATRIX | 0.5 | 6 | 6 | High minus low price range over a 250-day period. |
| 309 | `pv20_052_qil_rd` | MATRIX | 0.5 | 5 | 5 | Liquidity measure over a 250-day period. |
| 310 | `pv20_052_spcd_rd` | MATRIX | 0.5 | 8 | 8 | Daily closing price spread over a 250-day period. |
| 311 | `pv20_052_spcda_rd` | MATRIX | 0.5 | 4 | 4 | Adjusted daily closing price spread over a 250-day period. |
| 312 | `pv20_052vi` | MATRIX | 1 | 21 | 15 | Implied volatility over a 250-day period. |
| 313 | `pv20_052vigen` | MATRIX | 1 | 12 | 8 | Negative implied volatility over a 250-day period. |
| 314 | `pv20_1_1_rta_rd` | MATRIX | 0.5 | 18 | 5 | Average true range over a 1-day period. |
| 315 | `pv20_1_ard_accounts_payable_trade` | MATRIX | 0.7383 | 3 | 3 | ARD Accounts Payable - Trade |
| 316 | `pv20_1_cmlh_rd` | MATRIX | 0.5 | 54 | 34 | High-low midpoint change over a 1-day period. |
| 317 | `pv20_1_lmh_rd` | MATRIX | 0.5 | 14 | 8 | High minus low price range over a 1-day period. |
| 318 | `pv20_1_omlh_rd` | MATRIX | 0.5 | 9 | 8 | High-low midpoint change (open prices) over a 1-day period. |
| 319 | `pv20_1_pvt_rd` | MATRIX | 0.5 | 9 | 7 | Total volume price over a 1-day period. |
| 320 | `pv20_1_qil_rd` | MATRIX | 0.5 | 9 | 7 | Liquidity measure over a 1-day period. |
| 321 | `pv20_1_spcd_rd` | MATRIX | 0.5 | 16 | 11 | Daily closing price spread over a 1-day period. |
| 322 | `pv20_1_spcda_rd` | MATRIX | 0.5 | 3 | 3 | Adjusted daily closing price spread over a 1-day period. |
| 323 | `pv20_1_vmlh_rd` | MATRIX | 0.5 | 17 | 15 | High-low midpoint volatility over a 1-day period. |
| 324 | `pv20_1_vmt_rd` | MATRIX | 0.5 | 28 | 12 | Total market volatility over a 1-day period. |
| 325 | `pv20_21_03ftni_rd` | MATRIX | 1 | 5 | 5 | Interval factor for a 30-12 day period. |
| 326 | `pv20_21_13ftni_rd` | MATRIX | 1 | 5 | 5 | Interval factor for a 31-12 day period. |
| 327 | `pv20_21_23ftni_rd` | MATRIX | 1 | 4 | 4 | Interval factor for a 32-12 day period. |
| 328 | `pv20_21_33ftni_rd` | MATRIX | 1 | 12 | 10 | Interval factor for a 33-12 day period. |
| 329 | `pv20_21_43ftni_rd` | MATRIX | 1 | 18 | 6 | Interval factor for a 34-12 day period. |
| 330 | `pv20_21_53ftni_rd` | MATRIX | 1 | 17 | 7 | Interval factor for a 35-12 day period. |
| 331 | `pv20_21_63ftni_rd` | MATRIX | 1 | 29 | 18 | Interval factor for a 36-12 day period. |
| 332 | `pv20_21_73ftni_rd` | MATRIX | 1 | 13 | 6 | Interval factor for a 37-12 day period. |
| 333 | `pv20_21_83ftni_rd` | MATRIX | 1 | 6 | 5 | Interval factor for a 38-12 day period. |
| 334 | `pv20_252_mom` | MATRIX | 1 | 3 | 3 | Momentum factor over a 252-day period. |
| 335 | `pv20_3_lmh_rd` | MATRIX | 0.5 | 3 | 3 | High minus low price range over a 3-day period. |
| 336 | `pv20_52_5_rta_rd` | MATRIX | 0.5 | 5 | 5 | Average true range over a 5-25 day period. |
| 337 | `pv20_5_1_fma_rd` | MATRIX | 0.5 | 19 | 10 | Chaikin oscillator value over a 1-5 day period. |
| 338 | `pv20_5_cdts_rd` | MATRIX | 0.5 | 3 | 3 | Standard deviation of returns over a 5-day period. |
| 339 | `pv20_5_cmlh_rd` | MATRIX | 0.5 | 36 | 23 | High-low midpoint change over a 5-day period. |
| 340 | `pv20_5_lmh_rd` | MATRIX | 0.5 | 4 | 4 | High minus low price range over a 5-day period. |
| 341 | `pv20_5_qil_rd` | MATRIX | 0.5 | 6 | 6 | Liquidity measure over a 5-day period. |
| 342 | `pv20_5_spcd_rd` | MATRIX | 0.5 | 17 | 8 | Daily closing price spread over a 5-day period. |
| 343 | `pv20_5_spcda_rd` | MATRIX | 0.5 | 4 | 4 | Adjusted daily closing price spread over a 5-day period. |
| 344 | `pv20_a2_announcement_dt` | MATRIX | 1 | 4 | 4 | Latest Full Earnings Report Date |
| 345 | `pv20_a2_ard_share_out_from_front_cover` | MATRIX | 0.871 | 2 | 2 | ARD Shares Outstanding From The Front Cover |
| 346 | `pv20_a2_ardr_additional_paid_in_capital` | MATRIX | 0.8957 | 2 | 2 | ARD Ref Additional Paid In Capital |
| 347 | `pv20_a2_ardr_common_stock` | MATRIX | 0.9063 | 3 | 3 | ARD Ref Common Stock |
| 348 | `pv20_a2_ardr_deferred_inc_tax_asset_lt` | MATRIX | 0.5877 | 2 | 2 | ARD Ref Deferred Income Tax Asset (LT) |
| 349 | `pv20_a2_ardr_furniture_machinery_equip` | MATRIX | 0.7153 | 2 | 2 | ARD Ref Furniture/Machinery/Equipment |
| 350 | `pv20_a2_ardr_inventory` | MATRIX | 0.3697 | 4 | 4 | ARD Ref Inventories |
| 351 | `pv20_a2_ardr_par_value` | MATRIX | 0.7123 | 2 | 2 | ARD Ref Par Value |
| 352 | `pv20_a2_ardr_raw_material` | MATRIX | 0.3067 | 3 | 3 | ARD Ref Raw Materials |
| 353 | `pv20_a2_ardr_shares_outstanding` | MATRIX | 0.752 | 3 | 3 | ARD Ref Shares Outstanding |
| 354 | `pv20_a2_ardr_total_shareholders_equity` | MATRIX | 0.976 | 3 | 3 | ARD Ref Total Shareholders Equity |
| 355 | `pv20_a2_latest_period_end_dt_full_record` | MATRIX | 1 | 3 | 3 | Latest Period End Date from Full Records |
| 356 | `pv20_a_announcement_dt` | MATRIX | 1 | 2 | 2 | Latest Full Earnings Report Date |
| 357 | `pv20_a_ard_accrued_expenses` | MATRIX | 0.4107 | 1 | 1 | ARD Accrued Expenses |
| 358 | `pv20_a_ard_accts_receivable_trade` | MATRIX | 0.74 | 1 | 1 | ARD Accounts Receivable - Trade |
| 359 | `pv20_a_ard_allow_for_doubtful_accts` | MATRIX | 0.2817 | 1 | 1 | ARD Allowance For Doubtful Accounts |
| 360 | `pv20_a_ard_common_stock` | MATRIX | 0.9437 | 1 | 1 | ARD Common Stock |
| 361 | `pv20_a_ard_current_portion_of_lt_debt` | MATRIX | 0.3127 | 1 | 1 | ARD Current Portion of Long-Term Debt |
| 362 | `pv20_a_ard_deferred_inc_tax_asset_lt` | MATRIX | 0.3623 | 2 | 2 | ARD Deferred Income Tax Asset (Long-Term) |
| 363 | `pv20_a_ard_goodwll` | MATRIX | 0.6707 | 2 | 2 | ARD Goodwill |
| 364 | `pv20_a_ard_oth_noncurrent_liabilities` | MATRIX | 0.8447 | 2 | 2 | ARD Other Noncurrent Liabilities |
| 365 | `pv20_a_ard_other_current_liabilities` | MATRIX | 0.443 | 7 | 7 | ARD Other Current Liabilities |
| 366 | `pv20_a_ard_other_intangible_asset` | MATRIX | 0.6103 | 1 | 1 | ARD Other Intangible Assets |
| 367 | `pv20_a_ard_other_noncurrent_asset` | MATRIX | 0.7873 | 3 | 3 | ARD Other Noncurrent Assets |
| 368 | `pv20_a_ard_prepaid_exp_and_other` | MATRIX | 0.5007 | 1 | 1 | ARD Prepaid Expenses and Other |
| 369 | `pv20_a_ard_property_plant_equip_net` | MATRIX | 0.8897 | 4 | 3 | ARD Property Plant & Equipment - Net |
| 370 | `pv20_a_ard_tot_liab_and_shareholder_eqy` | MATRIX | 0.992 | 1 | 1 | ARD Total Liabilities and Shareholders Equity |
| 371 | `pv20_a_ard_tot_liabilities` | MATRIX | 0.9377 | 1 | 1 | ARD Total Liabilities |
| 372 | `pv20_a_ard_total_current_liabilities` | MATRIX | 0.836 | 2 | 2 | ARD Total Current Liabilities |
| 373 | `pv20_a_ard_total_shareholders_equity` | MATRIX | 1 | 5 | 5 | ARD Total Shareholders Equity |
| 374 | `pv20_a_ard_treasury_shares_num` | MATRIX | 0.3607 | 1 | 1 | ARD Treasury Shares (Number) |
| 375 | `pv20_a_ardr_property_plant_equip_net` | MATRIX | 0.7497 | 2 | 2 | ARD Ref Property Plant & Equipment - Net |
| 376 | `pv20_a_fundamental_entry_dt` | MATRIX | 1 | 2 | 2 | Fundamental Data Entry Date |
| 377 | `pv20_a_latest_period_end_dt_full_record` | MATRIX | 1 | 3 | 3 | Latest Period End Date from Full Records |
| 378 | `pv20_aftercons_difference_86` | VECTOR | 1 | 2 | 2 | Difference in consensus estimates after an event. |
| 379 | `pv20_aftercons_high_87` | VECTOR | 1 | 1 | 1 | Highest consensus estimate after an event. |
| 380 | `pv20_aftercons_low_88` | VECTOR | 1 | 2 | 2 | Lowest consensus estimate after an event. |
| 381 | `pv20_aftercons_mean_89` | VECTOR | 1 | 0 | 0 | Mean consensus estimate after an event. |
| 382 | `pv20_aftercons_median_90` | VECTOR | 1 | 1 | 1 | Median consensus estimate after an event. |
| 383 | `pv20_aftercons_numitems_91` | VECTOR | 1 | 3 | 3 | Number of items in the consensus after an event. |
| 384 | `pv20_aftercons_percentage_92` | VECTOR | 1 | 0 | 0 | Percentage change in consensus estimates after an event. |
| 385 | `pv20_aftercons_stddev_93` | VECTOR | 1 | 0 | 0 | Standard deviation of consensus estimates after an event. |
| 386 | `pv20_afterest_difference_96` | VECTOR | 1 | 2 | 2 | Difference in estimates after an event. |
| 387 | `pv20_afterest_percentage_97` | VECTOR | 1 | 2 | 2 | Percentage change in estimates after an event. |
| 388 | `pv20_afterest_value_99` | VECTOR | 1 | 0 | 0 | Value of estimates after an event. |
| 389 | `pv20_ard_acc_oth_comprehensive_inc` | MATRIX | 0.833 | 3 | 3 | ARD Accumulated Other Comprehensive Income |
| 390 | `pv20_ard_accounts_payable_trade` | MATRIX | 0.7383 | 1 | 1 | ARD Accounts Payable - Trade |
| 391 | `pv20_ard_accrued_exp_and_other` | MATRIX | 0.2673 | 2 | 2 | ARD Accrued Expenses and Other |
| 392 | `pv20_ard_additional_paid_in_capital` | MATRIX | 0.9153 | 1 | 1 | ARD Additional Paid In Capital |
| 393 | `pv20_ard_cash_and_equivalents` | MATRIX | 0.9593 | 14 | 6 | ARD Cash and Equivalents |
| 394 | `pv20_ard_deferred_income_taxes_liab` | MATRIX | 0.4803 | 2 | 2 | ARD Deferred Income Taxes (Liabilities) |
| 395 | `pv20_ard_inventory` | MATRIX | 0.513 | 2 | 2 | ARD Inventories |
| 396 | `pv20_ard_lt_debt` | MATRIX | 0.6293 | 1 | 1 | ARD Long Term Debt |
| 397 | `pv20_ard_other_current_assets` | MATRIX | 0.3987 | 3 | 3 | ARD Other Current Assets |
| 398 | `pv20_ard_shares_authorized` | MATRIX | 0.9127 | 5 | 5 | ARD Shares Authorized |
| 399 | `pv20_ard_shares_outstanding` | MATRIX | 0.8427 | 1 | 1 | ARD Shares Outstanding |
| 400 | `pv20_ard_tot_noncurrent_liabilities` | MATRIX | 0.6183 | 2 | 2 | ARD Total Noncurrent Liabilities |
| 401 | `pv20_ard_total_cur_assets` | MATRIX | 0.8343 | 3 | 3 | ARD Total Current Assets |
| 402 | `pv20_ard_total_noncurrent_assets` | MATRIX | 0.6277 | 1 | 1 | ARD Total Non-Current Assets |
| 403 | `pv20_ardr_current_portion_of_lt_debt` | MATRIX | 0.282 | 1 | 1 | ARD Ref Current Portion of Long-Term Debt |
| 404 | `pv20_ardr_deferred_income_taxes_liab` | MATRIX | 0.6057 | 2 | 2 | ARD Ref Deferred Income Taxes (Liabilities) |
| 405 | `pv20_ardr_finished_good` | MATRIX | 0.325 | 1 | 1 | ARD Ref Finished Goods |
| 406 | `pv20_ardr_goodwll` | MATRIX | 0.581 | 1 | 1 | ARD Ref Goodwill |
| 407 | `pv20_ardr_other_gross_fixed_assets` | MATRIX | 0.2677 | 1 | 1 | ARD Ref Other Gross Fixed Assets |
| 408 | `pv20_ardr_other_intangible_asset` | MATRIX | 0.4573 | 2 | 2 | ARD Ref Other Intangible Assets |
| 409 | `pv20_ardr_property_plant_equip_gross` | MATRIX | 0.475 | 1 | 1 | ARD Ref Property Plant & Equipment - Gross |
| 410 | `pv20_ardr_retained_earn_acc_deficit` | MATRIX | 0.9743 | 1 | 1 | ARD Ref Retained Earnings (Accumulated Deficit) |
| 411 | `pv20_beforecons_high_100` | VECTOR | 1 | 1 | 1 | Highest consensus estimate before an event. |
| 412 | `pv20_beforecons_low_101` | VECTOR | 1 | 0 | 0 | Lowest consensus estimate before an event. |
| 413 | `pv20_beforecons_mean_102` | VECTOR | 1 | 0 | 0 | Mean consensus estimate before an event. |
| 414 | `pv20_beforecons_median_103` | VECTOR | 1 | 3 | 3 | Median consensus estimate before an event. |
| 415 | `pv20_beforecons_numitems_104` | VECTOR | 1 | 0 | 0 | Number of items in the consensus before an event. |
| 416 | `pv20_beforecons_numitems_orig_105` | VECTOR | 1 | 1 | 1 | Original number of items in the consensus before an event. |
| 417 | `pv20_beforecons_stddev_106` | VECTOR | 1 | 0 | 0 | Standard deviation of consensus estimates before an event. |
| 418 | `pv20_beforeest_value_110` | VECTOR | 1 | 1 | 1 | Value of estimates before an event. |
| 419 | `pv20_beta125` | MATRIX | 0.5 | 4 | 4 | Beta coefficient calculated over a 125-day period. |
| 420 | `pv20_beta250` | MATRIX | 0.5 | 3 | 3 | Beta coefficient calculated over a 250-day period. |
| 421 | `pv20_beta60` | MATRIX | 0.5 | 5 | 5 | Beta coefficient calculated over a 60-day period. |
| 422 | `pv20_bottom` | MATRIX | 1 | 5 | 4 | Bottom score for the USA Universe Score dataset. |
| 423 | `pv20_category_111` | VECTOR | 1 | 0 | 0 | Category classification |
| 424 | `pv20_cneutret_1d_neutrets` | MATRIX | 1 | 13 | 8 | Neutralized returns for a 1-day period. |
| 425 | `pv20_cneutret_group1davgret` | MATRIX | 1 | 2 | 2 | Group average neutralized returns for a 1-day period. |
| 426 | `pv20_cneutret_groupndavgret` | MATRIX | 1 | 3 | 3 | Group average neutralized returns for an N-day period. |
| 427 | `pv20_cneutret_nd_rets` | MATRIX | 1 | 3 | 3 | Neutralized returns for an N-day period. |
| 428 | `pv20_companyname` | MATRIX | 0.892 | 1 | 1 | Company Name |
| 429 | `pv20_country_code` | MATRIX | 0.892 | 1 | 1 | ISO country code for the data. |
| 430 | `pv20_cusip` | MATRIX | 0.892 | 5 | 5 | 9-digit CUSIP Code for US and Canadian securities. For other securities, this value be replaced with NA |
| 431 | `pv20_dmgrhchenrpret_sector` | GROUP | 0.5 | 13 | 4 | Sector classification for the data. |
| 432 | `pv20_dr_aret_1` | MATRIX | 0.5 | 5 | 5 | Absolute return over a 1-day period. |
| 433 | `pv20_dr_aret_20` | MATRIX | 0.5 | 2 | 2 | Absolute return over a 20-day period. |
| 434 | `pv20_dr_aret_250` | MATRIX | 0.5 | 12 | 7 | Absolute return over a 250-day period. |
| 435 | `pv20_dr_aret_5` | MATRIX | 0.5 | 2 | 2 | Absolute return over a 5-day period. |
| 436 | `pv20_dr_aret_50` | MATRIX | 0.5 | 21 | 6 | Absolute return over a 50-day period. |
| 437 | `pv20_dr_chaikin_1_5` | MATRIX | 0.5 | 4 | 4 | Chaikin oscillator value over a 1-5 day period. |
| 438 | `pv20_dr_chaikin_5_20` | MATRIX | 0.5 | 4 | 4 | Chaikin oscillator value over a 5-20 day period. |
| 439 | `pv20_dr_codhml_1` | MATRIX | 0.5 | 18 | 8 | Coefficient of dispersion for high minus low prices over a 1-day period. |
| 440 | `pv20_dr_skewret_15` | MATRIX | 0.5 | 6 | 5 | Skewness of returns over a 15-day period. |
| 441 | `pv20_dr_skewret_6` | MATRIX | 0.5 | 3 | 3 | Skewness of returns over a 6-day period. |
| 442 | `pv20_dr_vola_120` | MATRIX | 0.5 | 19 | 10 | Volatility of returns over a 120-day period. |
| 443 | `pv20_dr_vola_20` | MATRIX | 0.5 | 3 | 3 | Volatility of returns over a 20-day period. |
| 444 | `pv20_dr_vola_250` | MATRIX | 0.5 | 2 | 2 | Volatility of returns over a 250-day period. |
| 445 | `pv20_dr_vola_30` | MATRIX | 0.5 | 4 | 3 | Volatility of returns over a 30-day period. |
| 446 | `pv20_dr_vola_40` | MATRIX | 0.5 | 5 | 4 | Volatility of returns over a 40-day period. |
| 447 | `pv20_dr_vola_5` | MATRIX | 0.5 | 2 | 2 | Volatility of returns over a 5-day period. |
| 448 | `pv20_dr_vola_60` | MATRIX | 0.5 | 2 | 2 | Volatility of returns over a 60-day period. |
| 449 | `pv20_dr_volret_1` | MATRIX | 0.5 | 3 | 3 | Volatility of returns for a 1-day period. |
| 450 | `pv20_dr_volsignret_1` | MATRIX | 0.5 | 9 | 8 | Signed volatility of returns for a 1-day period. |
| 451 | `pv20_dr_volvola_20` | MATRIX | 0.5 | 15 | 9 | Volatility of volatility over a 20-day period. |
| 452 | `pv20_ebitda_expected_report_period` | VECTOR | 0.943 | 2 | 2 | ebitda expected report period |
| 453 | `pv20_ebitda_market_status` | VECTOR | 0.943 | 0 | 0 | Market Status |
| 454 | `pv20_ebt_indicator_1_feature0` | MATRIX | 0.897 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [mean_flash] |
| 455 | `pv20_ebt_indicator_1_feature1` | MATRIX | 0.8774 | 0 | 0 | Median consensus IBES pre-tax profit (EBT) estimate for Fiscal Year 1 as observed 3 months prior |
| 456 | `pv20_ebt_indicator_1_feature10` | MATRIX | 0.8883 | 2 | 2 | Indicator 1, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 457 | `pv20_ebt_indicator_1_feature11` | MATRIX | 0.8883 | 1 | 1 | Indicator 1, Feature 11 from IBES Pre-tax Profit heuristics |
| 458 | `pv20_ebt_indicator_1_feature12` | MATRIX | 0.8969 | 1 | 1 | Feature 12 from Indicator 1 in IBES Pre-tax Profit module |
| 459 | `pv20_ebt_indicator_1_feature2` | MATRIX | 0.8883 | 0 | 0 | Median consensus IBES pre-tax profit (EBT) estimate for Fiscal Year 1 as observed 4 weeks prior |
| 460 | `pv20_ebt_indicator_1_feature3` | MATRIX | 0.791 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 461 | `pv20_ebt_indicator_1_feature4` | MATRIX | 0.791 | 2 | 2 | Feature 4 from Indicator 1 in IBES Pre-tax Profit module |
| 462 | `pv20_ebt_indicator_1_feature5` | MATRIX | 0.791 | 0 | 0 | Feature 5 from Indicator 1 in IBES Pre-tax Profit module |
| 463 | `pv20_ebt_indicator_1_feature6` | MATRIX | 0.7924 | 0 | 0 | Indicator 1, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 464 | `pv20_ebt_indicator_1_feature7` | MATRIX | 0.8774 | 2 | 2 | Feature 7 from Indicator 1 in IBES Pre-tax Profit module |
| 465 | `pv20_ebt_indicator_1_feature8` | MATRIX | 1 | 2 | 2 | Indicator 1, Feature 8 from IBES Pre-tax Profit heuristics |
| 466 | `pv20_ebt_indicator_1_feature9` | MATRIX | 0.897 | 2 | 2 | Feature 9 from Indicator 1 in IBES Pre-tax Profit module |
| 467 | `pv20_ebt_indicator_2_feature0` | MATRIX | 0.8992 | 0 | 0 | Mean of the latest flash IBES EBT estimates across analysts for Fiscal Year 2 horizon |
| 468 | `pv20_ebt_indicator_2_feature1` | MATRIX | 0.872 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [median 3 months ago] |
| 469 | `pv20_ebt_indicator_2_feature10` | MATRIX | 0.8846 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 470 | `pv20_ebt_indicator_2_feature11` | MATRIX | 0.8846 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 471 | `pv20_ebt_indicator_2_feature12` | MATRIX | 0.899 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 472 | `pv20_ebt_indicator_2_feature2` | MATRIX | 0.8846 | 0 | 0 | Median across analysts of IBES EBT estimates as of four weeks ago for Fiscal Year 2 horizon |
| 473 | `pv20_ebt_indicator_2_feature3` | MATRIX | 0.7872 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 474 | `pv20_ebt_indicator_2_feature4` | MATRIX | 0.7872 | 3 | 3 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 475 | `pv20_ebt_indicator_2_feature5` | MATRIX | 0.7872 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 476 | `pv20_ebt_indicator_2_feature6` | MATRIX | 0.7891 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 477 | `pv20_ebt_indicator_2_feature7` | MATRIX | 0.872 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 478 | `pv20_ebt_indicator_2_feature8` | MATRIX | 1 | 7 | 4 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 479 | `pv20_ebt_indicator_2_feature9` | MATRIX | 0.8992 | 16 | 5 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 480 | `pv20_ebt_indicator_3_feature0` | MATRIX | 0.887 | 2 | 2 | Heuristically extracted IBES Pre-tax Profit (EBT) feature: Indicator 3, feature 0; Fiscal Year 3; mean of flas |
| 481 | `pv20_ebt_indicator_3_feature1` | MATRIX | 0.8359 | 1 | 1 | Median consensus IBES pre-tax profit (EBT) estimate for Fiscal Year 3 as observed 3 months prior |
| 482 | `pv20_ebt_indicator_3_feature10` | MATRIX | 0.8554 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 483 | `pv20_ebt_indicator_3_feature11` | MATRIX | 0.8554 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 484 | `pv20_ebt_indicator_3_feature12` | MATRIX | 0.8867 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 485 | `pv20_ebt_indicator_3_feature2` | MATRIX | 0.8554 | 0 | 0 | Median consensus IBES pre-tax profit (EBT) estimate for Fiscal Year 3 as observed 4 weeks prior |
| 486 | `pv20_ebt_indicator_3_feature3` | MATRIX | 0.7004 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 487 | `pv20_ebt_indicator_3_feature4` | MATRIX | 0.7004 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 488 | `pv20_ebt_indicator_3_feature5` | MATRIX | 0.7004 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 489 | `pv20_ebt_indicator_3_feature6` | MATRIX | 0.7025 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 490 | `pv20_ebt_indicator_3_feature7` | MATRIX | 0.8359 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 491 | `pv20_ebt_indicator_3_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 492 | `pv20_ebt_indicator_3_feature9` | MATRIX | 0.887 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 493 | `pv20_ebt_indicator_4_feature0` | MATRIX | 0.7222 | 0 | 0 | Indicator 4, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 494 | `pv20_ebt_indicator_4_feature1` | MATRIX | 0.5936 | 1 | 1 | Feature 1 from Indicator 4 in IBES Pre-tax Profit module |
| 495 | `pv20_ebt_indicator_4_feature10` | MATRIX | 0.6214 | 0 | 0 | Feature number 10 for indicator 4 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 496 | `pv20_ebt_indicator_4_feature11` | MATRIX | 0.6214 | 1 | 1 | Indicator 4, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 497 | `pv20_ebt_indicator_4_feature12` | MATRIX | 0.722 | 0 | 0 | Indicator 4, Feature 12 extracted heuristically from IBES Pre-tax Profit modules |
| 498 | `pv20_ebt_indicator_4_feature2` | MATRIX | 0.6214 | 0 | 0 | Indicator 4, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 499 | `pv20_ebt_indicator_4_feature3` | MATRIX | 0.3443 | 1 | 1 | Feature 3 from Indicator 4 in IBES Pre-tax Profit module |
| 500 | `pv20_ebt_indicator_4_feature4` | MATRIX | 0.3443 | 1 | 1 | Indicator 4, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 501 | `pv20_ebt_indicator_4_feature5` | MATRIX | 0.3443 | 0 | 0 | Feature 5 from Indicator 4 in IBES Pre-tax Profit module |
| 502 | `pv20_ebt_indicator_4_feature6` | MATRIX | 0.3482 | 2 | 2 | Feature 6 from Indicator 4 in IBES Pre-tax Profit module |
| 503 | `pv20_ebt_indicator_4_feature7` | MATRIX | 0.5936 | 1 | 1 | Indicator 4, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 504 | `pv20_ebt_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator 4 in IBES Pre-tax Profit module |
| 505 | `pv20_ebt_indicator_4_feature9` | MATRIX | 0.7222 | 1 | 1 | Feature 9 from Indicator 4 in IBES Pre-tax Profit module |
| 506 | `pv20_ebt_indicator_6_feature0` | MATRIX | 0.8517 | 1 | 1 | Mean of the latest flash IBES EBT estimates across analysts for Quarter 1 horizon (next fiscal quarter) |
| 507 | `pv20_ebt_indicator_6_feature1` | MATRIX | 0.8338 | 36 | 20 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [median 3 months ago] |
| 508 | `pv20_ebt_indicator_6_feature10` | MATRIX | 0.8479 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 509 | `pv20_ebt_indicator_6_feature11` | MATRIX | 0.8479 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 510 | `pv20_ebt_indicator_6_feature2` | MATRIX | 0.8479 | 5 | 5 | Median across analysts of IBES EBT estimates as of four weeks ago for Quarter 1 horizon |
| 511 | `pv20_ebt_indicator_6_feature3` | MATRIX | 0.708 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 512 | `pv20_ebt_indicator_6_feature4` | MATRIX | 0.708 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 513 | `pv20_ebt_indicator_6_feature6` | MATRIX | 0.7105 | 6 | 6 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 514 | `pv20_ebt_indicator_6_feature7` | MATRIX | 0.8338 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 515 | `pv20_ebt_indicator_6_feature8` | MATRIX | 1 | 18 | 11 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 516 | `pv20_ebt_indicator_6_feature9` | MATRIX | 0.8517 | 3 | 3 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 517 | `pv20_ebt_indicator_7_feature0` | MATRIX | 0.8501 | 3 | 3 | Heuristically extracted IBES Pre-tax Profit (EBT) feature: Indicator 7, feature 0; Quarter 2; mean of flash es |
| 518 | `pv20_ebt_indicator_7_feature10` | MATRIX | 0.8437 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 519 | `pv20_ebt_indicator_7_feature11` | MATRIX | 0.8437 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 520 | `pv20_ebt_indicator_7_feature12` | MATRIX | 0.8496 | 4 | 4 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 521 | `pv20_ebt_indicator_7_feature2` | MATRIX | 0.8437 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [median 4 weeks ago] |
| 522 | `pv20_ebt_indicator_7_feature3` | MATRIX | 0.6992 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 523 | `pv20_ebt_indicator_7_feature4` | MATRIX | 0.6992 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 524 | `pv20_ebt_indicator_7_feature5` | MATRIX | 0.6992 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 525 | `pv20_ebt_indicator_7_feature6` | MATRIX | 0.7027 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 526 | `pv20_ebt_indicator_7_feature7` | MATRIX | 0.8274 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 527 | `pv20_ebt_indicator_7_feature8` | MATRIX | 1 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 528 | `pv20_ebt_indicator_7_feature9` | MATRIX | 0.8501 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 529 | `pv20_ebt_indicator_8_feature10` | MATRIX | 0.8389 | 5 | 5 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 530 | `pv20_ebt_indicator_8_feature11` | MATRIX | 0.8389 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 531 | `pv20_ebt_indicator_8_feature12` | MATRIX | 0.8462 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 532 | `pv20_ebt_indicator_8_feature2` | MATRIX | 0.8389 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [median 4 weeks ago] |
| 533 | `pv20_ebt_indicator_8_feature3` | MATRIX | 0.6831 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 534 | `pv20_ebt_indicator_8_feature9` | MATRIX | 0.8466 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 535 | `pv20_ebt_indicator_9_feature0` | MATRIX | 0.8438 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [mean_flash] |
| 536 | `pv20_ebt_indicator_9_feature1` | MATRIX | 0.7874 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [median 3 months ago] |
| 537 | `pv20_ebt_indicator_9_feature10` | MATRIX | 0.8206 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 538 | `pv20_ebt_indicator_9_feature11` | MATRIX | 0.8206 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 539 | `pv20_ebt_indicator_9_feature12` | MATRIX | 0.8432 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 540 | `pv20_ebt_indicator_9_feature3` | MATRIX | 0.6446 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 541 | `pv20_ebt_indicator_9_feature6` | MATRIX | 0.6476 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 542 | `pv20_ebt_indicator_9_feature7` | MATRIX | 0.7874 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 543 | `pv20_ebt_indicator_9_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 544 | `pv20_ebt_indicator_n_feature10` | MATRIX | 0.7891 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 545 | `pv20_ebt_indicator_n_feature3` | MATRIX | 0.6041 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 546 | `pv20_ebt_indicator_n_feature4` | MATRIX | 0.6041 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 547 | `pv20_ebt_indicator_n_feature5` | MATRIX | 0.6041 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 548 | `pv20_ebt_indicator_n_feature7` | MATRIX | 0.7655 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 549 | `pv20_ebt_indicator_n_feature8` | MATRIX | 1 | 4 | 4 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 550 | `pv20_ebt_indicator_n_feature9` | MATRIX | 0.8164 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 551 | `pv20_ebt_indicator_o_feature0` | MATRIX | 0.793 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [mean_flash] |
| 552 | `pv20_ebt_indicator_o_feature1` | MATRIX | 0.7452 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [median 3 months ago] |
| 553 | `pv20_ebt_indicator_o_feature10` | MATRIX | 0.7697 | 3 | 3 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 554 | `pv20_ebt_indicator_o_feature2` | MATRIX | 0.7697 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit (EBT) feature: Indicator O, feature 2; Quarter 6; median as of 4 w |
| 555 | `pv20_ebt_indicator_o_feature5` | MATRIX | 0.559 | 10 | 9 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 556 | `pv20_ebt_indicator_o_feature6` | MATRIX | 0.5628 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 557 | `pv20_ebt_indicator_p_feature0` | MATRIX | 0.7766 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit (EBT) feature: Indicator P, feature 0; Quarter 7; mean of flash es |
| 558 | `pv20_ebt_indicator_p_feature1` | MATRIX | 0.707 | 2 | 2 | Heuristically extracted IBES Pre-tax Profit (EBT) feature: Indicator P, feature 1; Quarter 7; median as of 3 m |
| 559 | `pv20_ebt_indicator_p_feature10` | MATRIX | 0.7457 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 560 | `pv20_ebt_indicator_p_feature11` | MATRIX | 0.7457 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 561 | `pv20_ebt_indicator_p_feature12` | MATRIX | 0.7747 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 562 | `pv20_ebt_indicator_p_feature2` | MATRIX | 0.7457 | 0 | 0 | Median across analysts of IBES EBT estimates as of four weeks ago for Quarter 7 horizon |
| 563 | `pv20_ebt_indicator_p_feature3` | MATRIX | 0.5047 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 564 | `pv20_ebt_indicator_p_feature5` | MATRIX | 0.5047 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 565 | `pv20_ebt_indicator_p_feature6` | MATRIX | 0.5104 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 566 | `pv20_ebt_indicator_p_feature7` | MATRIX | 0.707 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 567 | `pv20_ebt_indicator_q_feature0` | MATRIX | 0.754 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit (EBT) feature: Indicator Q, feature 0; Quarter 8; mean of flash es |
| 568 | `pv20_ebt_indicator_q_feature10` | MATRIX | 0.6998 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 569 | `pv20_ebt_indicator_q_feature11` | MATRIX | 0.6998 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 570 | `pv20_ebt_indicator_q_feature12` | MATRIX | 0.7532 | 3 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 571 | `pv20_ebt_indicator_q_feature2` | MATRIX | 0.6998 | 4 | 4 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [median 4 weeks ago] |
| 572 | `pv20_ebt_indicator_q_feature3` | MATRIX | 0.3929 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 573 | `pv20_ebt_indicator_q_feature4` | MATRIX | 0.3929 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 574 | `pv20_ebt_indicator_q_feature5` | MATRIX | 0.3929 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 575 | `pv20_ebt_indicator_q_feature7` | MATRIX | 0.646 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 576 | `pv20_ebt_indicator_q_feature9` | MATRIX | 0.754 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 577 | `pv20_eps_indicator_0_feature0` | MATRIX | 0.7928 | 0 | 0 | Heuristically derived predictive feature 0 from IBES EPS for Long Term Growth; mean_flash aggregation |
| 578 | `pv20_eps_indicator_0_feature1` | MATRIX | 0.7659 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [median 3 months |
| 579 | `pv20_eps_indicator_0_feature10` | MATRIX | 0.7799 | 0 | 0 | Heuristically extracted feature 10 from indicator 0 in the IBES Earnings per Share module for Long Term Growth |
| 580 | `pv20_eps_indicator_0_feature11` | MATRIX | 0.7799 | 0 | 0 | Feature extracted from IBES EPS module, Long Term Growth estimate, non-trivial feature |
| 581 | `pv20_eps_indicator_0_feature3` | MATRIX | 0.5414 | 0 | 0 | Feature from IBES Earnings per Share module, Long Term Growth, non-trivial feature |
| 582 | `pv20_eps_indicator_0_feature6` | MATRIX | 0.5642 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [Non-trivial fea |
| 583 | `pv20_eps_indicator_0_feature7` | MATRIX | 0.7659 | 0 | 0 | Feature extracted from IBES EPS module, Long Term Growth estimate, non-trivial feature |
| 584 | `pv20_eps_indicator_1_feature0` | MATRIX | 0.9694 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [mean_flash] |
| 585 | `pv20_eps_indicator_1_feature1` | MATRIX | 0.9548 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [median 3 months ag |
| 586 | `pv20_eps_indicator_1_feature10` | MATRIX | 0.9641 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 587 | `pv20_eps_indicator_1_feature11` | MATRIX | 0.9641 | 3 | 3 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 588 | `pv20_eps_indicator_1_feature12` | MATRIX | 0.9693 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 589 | `pv20_eps_indicator_1_feature2` | MATRIX | 0.9641 | 1 | 1 | Heuristically extracted predictive feature from IBES EPS modules for Fiscal Year 1; median EPS estimate as of  |
| 590 | `pv20_eps_indicator_1_feature3` | MATRIX | 0.9229 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 591 | `pv20_eps_indicator_1_feature4` | MATRIX | 0.9229 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 592 | `pv20_eps_indicator_1_feature5` | MATRIX | 0.9229 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 593 | `pv20_eps_indicator_1_feature6` | MATRIX | 0.9243 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 594 | `pv20_eps_indicator_1_feature7` | MATRIX | 0.9548 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 595 | `pv20_eps_indicator_1_feature8` | MATRIX | 1 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 596 | `pv20_eps_indicator_1_feature9` | MATRIX | 0.9694 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 1] [Non-trivial featur |
| 597 | `pv20_eps_indicator_2_feature0` | MATRIX | 0.9699 | 2 | 2 | Flash mean of IBES analyst EPS estimates for Fiscal Year 2, heuristically extracted for US equities |
| 598 | `pv20_eps_indicator_2_feature1` | MATRIX | 0.9523 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [median 3 months ag |
| 599 | `pv20_eps_indicator_2_feature10` | MATRIX | 0.9628 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 600 | `pv20_eps_indicator_2_feature11` | MATRIX | 0.9628 | 1 | 1 | Heuristically extracted feature 11 from indicator 2 in the IBES Earnings per Share module for Fiscal Year 2 (n |
| 601 | `pv20_eps_indicator_2_feature12` | MATRIX | 0.9698 | 3 | 3 | Heuristically extracted feature 12 from indicator 2 in the IBES Earnings per Share module for Fiscal Year 2 (n |
| 602 | `pv20_eps_indicator_2_feature2` | MATRIX | 0.9628 | 0 | 0 | Heuristically extracted predictive feature from IBES EPS modules for Fiscal Year 2; median EPS estimate as of  |
| 603 | `pv20_eps_indicator_2_feature3` | MATRIX | 0.9203 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 604 | `pv20_eps_indicator_2_feature4` | MATRIX | 0.9203 | 4 | 4 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 605 | `pv20_eps_indicator_2_feature5` | MATRIX | 0.9203 | 4 | 4 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 606 | `pv20_eps_indicator_2_feature6` | MATRIX | 0.9213 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 607 | `pv20_eps_indicator_2_feature7` | MATRIX | 0.9523 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 608 | `pv20_eps_indicator_2_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 609 | `pv20_eps_indicator_2_feature9` | MATRIX | 0.9699 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 2] [Non-trivial featur |
| 610 | `pv20_eps_indicator_3_feature0` | MATRIX | 0.9647 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [mean_flash] |
| 611 | `pv20_eps_indicator_3_feature1` | MATRIX | 0.9236 | 0 | 0 | Heuristically extracted predictive feature from IBES EPS modules for Fiscal Year 3; median EPS estimate as of  |
| 612 | `pv20_eps_indicator_3_feature10` | MATRIX | 0.941 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 613 | `pv20_eps_indicator_3_feature11` | MATRIX | 0.941 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 614 | `pv20_eps_indicator_3_feature12` | MATRIX | 0.9646 | 0 | 0 | Heuristically extracted feature 12 from indicator 3 in the IBES Earnings per Share module for Fiscal Year 3 (n |
| 615 | `pv20_eps_indicator_3_feature2` | MATRIX | 0.941 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [median 4 weeks ago |
| 616 | `pv20_eps_indicator_3_feature3` | MATRIX | 0.8467 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 617 | `pv20_eps_indicator_3_feature4` | MATRIX | 0.8467 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 618 | `pv20_eps_indicator_3_feature5` | MATRIX | 0.8467 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 619 | `pv20_eps_indicator_3_feature6` | MATRIX | 0.8489 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 620 | `pv20_eps_indicator_3_feature7` | MATRIX | 0.9236 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 621 | `pv20_eps_indicator_3_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 3] [Non-trivial featur |
| 622 | `pv20_eps_indicator_3_feature9` | MATRIX | 0.9647 | 0 | 0 | Heuristically extracted feature 9 from indicator 3 in the IBES Earnings per Share module for Fiscal Year 3 (no |
| 623 | `pv20_eps_indicator_4_feature0` | MATRIX | 0.8473 | 0 | 0 | IBES EPS predictive feature (Indicator 4) for Fiscal Year 4; mean_flash (mean of flash estimates) |
| 624 | `pv20_eps_indicator_4_feature1` | MATRIX | 0.7038 | 3 | 3 | IBES EPS predictive feature (Indicator 4) for Fiscal Year 4; median 3 months ago (median consensus from 3 mont |
| 625 | `pv20_eps_indicator_4_feature10` | MATRIX | 0.7411 | 2 | 2 | Feature number 10 for indicator 4 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 626 | `pv20_eps_indicator_4_feature11` | MATRIX | 0.7411 | 1 | 1 | Indicator 4, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 627 | `pv20_eps_indicator_4_feature12` | MATRIX | 0.847 | 1 | 1 | Heuristically extracted feature 12 from indicator 4 in the IBES Earnings per Share module for Fiscal Year 4 (n |
| 628 | `pv20_eps_indicator_4_feature2` | MATRIX | 0.7411 | 0 | 0 | IBES EPS predictive feature (Indicator 4) for Fiscal Year 4; median 4 weeks ago (median consensus from four we |
| 629 | `pv20_eps_indicator_4_feature3` | MATRIX | 0.4536 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 4] [Non-trivial featur |
| 630 | `pv20_eps_indicator_4_feature4` | MATRIX | 0.4536 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 4] [Non-trivial featur |
| 631 | `pv20_eps_indicator_4_feature5` | MATRIX | 0.4536 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 4] [Non-trivial featur |
| 632 | `pv20_eps_indicator_4_feature6` | MATRIX | 0.458 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 4] [Non-trivial featur |
| 633 | `pv20_eps_indicator_4_feature7` | MATRIX | 0.7038 | 1 | 1 | Indicator 4, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 634 | `pv20_eps_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Fiscal Year 4] [Non-trivial featur |
| 635 | `pv20_eps_indicator_4_feature9` | MATRIX | 0.8473 | 0 | 0 | Feature 9 from Indicator 4 in IBES Pre-tax Profit module |
| 636 | `pv20_eps_indicator_6_feature0` | MATRIX | 0.9536 | 0 | 0 | Heuristically extracted predictive feature from IBES EPS modules for Quarter 1; statistic: mean of flash estim |
| 637 | `pv20_eps_indicator_6_feature1` | MATRIX | 0.9387 | 9 | 9 | Heuristically derived predictive feature from IBES Earnings per Share estimates for Quarter 1; median value as |
| 638 | `pv20_eps_indicator_6_feature10` | MATRIX | 0.9492 | 3 | 3 | Feature 10 for Indicator 6 extracted heuristically from IBES Pre-tax Profit modules for Fiscal Year 4 |
| 639 | `pv20_eps_indicator_6_feature12` | MATRIX | 0.9534 | 4 | 4 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 1] [Non-trivial feature] |
| 640 | `pv20_eps_indicator_6_feature2` | MATRIX | 0.9492 | 10 | 7 | Heuristically derived predictive feature from IBES Earnings per Share estimates for Quarter 1; median value as |
| 641 | `pv20_eps_indicator_6_feature7` | MATRIX | 0.9387 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 1] [Non-trivial feature] |
| 642 | `pv20_eps_indicator_6_feature8` | MATRIX | 1 | 50 | 33 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 1] [Non-trivial feature] |
| 643 | `pv20_eps_indicator_7_feature0` | MATRIX | 0.9549 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 2] [mean_flash] |
| 644 | `pv20_eps_indicator_7_feature1` | MATRIX | 0.9386 | 0 | 0 | Heuristically extracted predictive feature from IBES EPS modules for Quarter 2; statistic: median as of 3 mont |
| 645 | `pv20_eps_indicator_7_feature11` | MATRIX | 0.9497 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 2] [Non-trivial feature] |
| 646 | `pv20_eps_indicator_7_feature12` | MATRIX | 0.9546 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 2] [Non-trivial feature] |
| 647 | `pv20_eps_indicator_7_feature2` | MATRIX | 0.9497 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 2] [median 4 weeks ago] |
| 648 | `pv20_eps_indicator_7_feature6` | MATRIX | 0.8928 | 0 | 0 | Heuristically extracted feature 6 from indicator 7 in the IBES Earnings per Share module for Quarter 2 (non-tr |
| 649 | `pv20_eps_indicator_8_feature1` | MATRIX | 0.9323 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [median 3 months ago] |
| 650 | `pv20_eps_indicator_8_feature10` | MATRIX | 0.946 | 0 | 0 | Heuristically extracted feature 10 from indicator 8 in the IBES Earnings per Share module for Quarter 3 (non-t |
| 651 | `pv20_eps_indicator_8_feature11` | MATRIX | 0.946 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [Non-trivial feature] |
| 652 | `pv20_eps_indicator_8_feature12` | MATRIX | 0.9524 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [Non-trivial feature] |
| 653 | `pv20_eps_indicator_8_feature2` | MATRIX | 0.946 | 0 | 0 | Heuristically extracted feature 2 from indicator 8 in the IBES Earnings per Share module for Quarter 3, comput |
| 654 | `pv20_eps_indicator_8_feature3` | MATRIX | 0.8809 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [Non-trivial feature] |
| 655 | `pv20_eps_indicator_8_feature4` | MATRIX | 0.8809 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [Non-trivial feature] |
| 656 | `pv20_eps_indicator_8_feature6` | MATRIX | 0.8839 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [Non-trivial feature] |
| 657 | `pv20_eps_indicator_8_feature7` | MATRIX | 0.9323 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 3] [Non-trivial feature] |
| 658 | `pv20_eps_indicator_9_feature1` | MATRIX | 0.9237 | 0 | 0 | Heuristically derived predictive feature from IBES Earnings per Share estimates for Quarter 4; median value as |
| 659 | `pv20_eps_indicator_9_feature11` | MATRIX | 0.9411 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 4] [Non-trivial feature] |
| 660 | `pv20_eps_indicator_9_feature12` | MATRIX | 0.9531 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 4] [Non-trivial feature] |
| 661 | `pv20_eps_indicator_9_feature2` | MATRIX | 0.9411 | 0 | 0 | Heuristically extracted predictive feature from IBES EPS modules for Quarter 4; statistic: median as of 4 week |
| 662 | `pv20_eps_indicator_9_feature3` | MATRIX | 0.8619 | 3 | 3 | Heuristically extracted feature 3 from indicator 9 in the IBES Earnings per Share module for Quarter 4 (non-tr |
| 663 | `pv20_eps_indicator_9_feature5` | MATRIX | 0.8619 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 4] [Non-trivial feature] |
| 664 | `pv20_eps_indicator_9_feature6` | MATRIX | 0.865 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 4] [Non-trivial feature] |
| 665 | `pv20_eps_indicator_9_feature7` | MATRIX | 0.9237 | 1 | 1 | Heuristically extracted feature 7 from indicator 9 in the IBES Earnings per Share module for Quarter 4 (non-tr |
| 666 | `pv20_eps_indicator_9_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 4] [Non-trivial feature] |
| 667 | `pv20_eps_indicator_9_feature9` | MATRIX | 0.9537 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 4] [Non-trivial feature] |
| 668 | `pv20_eps_indicator_n_feature1` | MATRIX | 0.9111 | 0 | 0 | Median IBES EPS estimate for Quarter 5 as of 3 months ago |
| 669 | `pv20_eps_indicator_n_feature12` | MATRIX | 0.9449 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 5] [Non-trivial feature] |
| 670 | `pv20_eps_indicator_n_feature2` | MATRIX | 0.9288 | 0 | 0 | Median IBES EPS estimate for Quarter 5 as of 4 weeks ago |
| 671 | `pv20_eps_indicator_n_feature3` | MATRIX | 0.8384 | 2 | 1 | Heuristically extracted feature 3 from indicator N in the IBES Earnings per Share module for Quarter 5 (non-tr |
| 672 | `pv20_eps_indicator_n_feature5` | MATRIX | 0.8384 | 2 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 5] [Non-trivial feature] |
| 673 | `pv20_eps_indicator_n_feature6` | MATRIX | 0.8423 | 4 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 5] [Non-trivial feature] |
| 674 | `pv20_eps_indicator_n_feature7` | MATRIX | 0.9111 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 5] [Non-trivial feature] |
| 675 | `pv20_eps_indicator_n_feature8` | MATRIX | 1 | 8 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 5] [Non-trivial feature] |
| 676 | `pv20_eps_indicator_o_feature10` | MATRIX | 0.917 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 6] [Non-trivial feature] |
| 677 | `pv20_eps_indicator_o_feature12` | MATRIX | 0.9364 | 0 | 0 | Heuristically extracted feature 12 from indicator O in the IBES Earnings per Share module for Quarter 6 (non-t |
| 678 | `pv20_eps_indicator_o_feature3` | MATRIX | 0.7976 | 0 | 0 | Heuristically extracted feature 3 from indicator O in the IBES Earnings per Share module for Quarter 6 (non-tr |
| 679 | `pv20_eps_indicator_o_feature5` | MATRIX | 0.7976 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 6] [Non-trivial feature] |
| 680 | `pv20_eps_indicator_o_feature8` | MATRIX | 1 | 5 | 4 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 6] [Non-trivial feature] |
| 681 | `pv20_eps_indicator_p_feature0` | MATRIX | 0.9247 | 0 | 0 | Heuristically derived predictive feature 0 from IBES EPS for Quarter 7; mean_flash aggregation |
| 682 | `pv20_eps_indicator_p_feature1` | MATRIX | 0.8642 | 3 | 3 | Heuristically extracted feature 1 from indicator P in the IBES Earnings per Share module for Quarter 7, comput |
| 683 | `pv20_eps_indicator_p_feature10` | MATRIX | 0.9005 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 7] [Non-trivial feature] |
| 684 | `pv20_eps_indicator_p_feature12` | MATRIX | 0.9244 | 2 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 7] [Non-trivial feature] |
| 685 | `pv20_eps_indicator_p_feature2` | MATRIX | 0.9005 | 0 | 0 | Heuristically derived predictive feature 2 from IBES EPS for Quarter 7; median measured 4 weeks ago |
| 686 | `pv20_eps_indicator_p_feature4` | MATRIX | 0.7368 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 7] [Non-trivial feature] |
| 687 | `pv20_eps_indicator_p_feature6` | MATRIX | 0.7462 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 7] [Non-trivial feature] |
| 688 | `pv20_eps_indicator_p_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 7] [Non-trivial feature] |
| 689 | `pv20_eps_indicator_q_feature0` | MATRIX | 0.9121 | 1 | 1 | Heuristically extracted predictive feature from IBES EPS modules for Quarter 8; statistic: mean of flash estim |
| 690 | `pv20_eps_indicator_q_feature10` | MATRIX | 0.8626 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 691 | `pv20_eps_indicator_q_feature11` | MATRIX | 0.8626 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 692 | `pv20_eps_indicator_q_feature12` | MATRIX | 0.9113 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 693 | `pv20_eps_indicator_q_feature3` | MATRIX | 0.628 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 694 | `pv20_eps_indicator_q_feature4` | MATRIX | 0.628 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 695 | `pv20_eps_indicator_q_feature5` | MATRIX | 0.628 | 1 | 1 | Heuristically extracted feature 5 from indicator Q in the IBES Earnings per Share module for Quarter 8 (non-tr |
| 696 | `pv20_eps_indicator_q_feature6` | MATRIX | 0.6358 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 697 | `pv20_eps_indicator_q_feature7` | MATRIX | 0.8188 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 698 | `pv20_eps_indicator_q_feature8` | MATRIX | 1 | 3 | 2 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 699 | `pv20_eps_indicator_q_feature9` | MATRIX | 0.9121 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 8] [Non-trivial feature] |
| 700 | `pv20_fincharts_fundaimage4image` | VECTOR | 0.8903 | 0 | 0 | Image data for USA Fincharts. |
| 701 | `pv20_fiscalend_112` | VECTOR | 1 | 2 | 1 | Fiscal year-end date for the forecast. |
| 702 | `pv20_fiscalyear_113` | VECTOR | 1 | 2 | 2 | Fiscal year associated with the forecast. |
| 703 | `pv20_forecasttype_115` | VECTOR | 1 | 2 | 1 | Type of forecast (e.g., earnings, revenue). |
| 704 | `pv20_fx_conversion` | MATRIX | 1 | 1 | 1 | FX conversion rate for the specified currency. |
| 705 | `pv20_gp_bet_industry_cap_top3000_1_20` | MATRIX | 0.5 | 2 | 2 | Beta of industry capitalization for top 3000 securities over a 1-20 day period. |
| 706 | `pv20_gp_bet_industry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Beta of industry capitalization for top 3000 securities over a 1-5 day period. |
| 707 | `pv20_gp_bet_subindustry_cap_top2000_1_20` | MATRIX | 0.5 | 1 | 1 | Beta of subindustry capitalization for top 2000 securities over a 1-20 day period. |
| 708 | `pv20_gp_bet_subindustry_cap_top2000_1_5` | MATRIX | 0.5 | 0 | 0 | Beta of subindustry capitalization for top 2000 securities over a 1-5 day period. |
| 709 | `pv20_gp_bet_subindustry_cap_top3000_1_20` | MATRIX | 0.5 | 0 | 0 | Beta of subindustry capitalization for top 3000 securities over a 1-20 day period. |
| 710 | `pv20_gp_bet_subindustry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Beta of subindustry capitalization for top 3000 securities over a 1-5 day period. |
| 711 | `pv20_gp_bet_subindustry_cap_top3000_1_60` | MATRIX | 0.5 | 0 | 0 | Beta of subindustry capitalization for top 3000 securities over a 1-60 day period. |
| 712 | `pv20_gp_cor_industry_cap_top3000_1_20` | MATRIX | 0.5 | 0 | 0 | Correlation of industry capitalization for top 3000 securities over a 1-20 day period. |
| 713 | `pv20_gp_cor_industry_cap_top3000_1_5` | MATRIX | 0.5 | 1 | 1 | Correlation of industry capitalization for top 3000 securities over a 1-5 day period. |
| 714 | `pv20_gp_cor_subindustry_cap_top2000_1_20` | MATRIX | 0.5 | 0 | 0 | Correlation of subindustry capitalization for top 2000 securities over a 1-20 day period. |
| 715 | `pv20_gp_cor_subindustry_cap_top2000_1_5` | MATRIX | 0.5 | 0 | 0 | Correlation of subindustry capitalization for top 2000 securities over a 1-5 day period. |
| 716 | `pv20_gp_cor_subindustry_cap_top3000_1_20` | MATRIX | 0.5 | 0 | 0 | Correlation of subindustry capitalization for top 3000 securities over a 1-20 day period. |
| 717 | `pv20_gp_cor_subindustry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Correlation of subindustry capitalization for top 3000 securities over a 1-5 day period. |
| 718 | `pv20_gp_cor_subindustry_cap_top3000_1_60` | MATRIX | 0.5 | 1 | 1 | Correlation of subindustry capitalization for top 3000 securities over a 1-60 day period. |
| 719 | `pv20_gp_rbet_industry_cap_top3000_1_20` | MATRIX | 0.5 | 0 | 0 | Relative beta of industry capitalization for top 3000 securities over a 1-20 day period. |
| 720 | `pv20_gp_rbet_industry_cap_top3000_1_5` | MATRIX | 0.5 | 11 | 2 | Relative beta of industry capitalization for top 3000 securities over a 1-5 day period. |
| 721 | `pv20_gp_rbet_subindustry_cap_top2000_1_20` | MATRIX | 0.5 | 0 | 0 | Relative beta of subindustry capitalization for top 2000 securities over a 1-20 day period. |
| 722 | `pv20_gp_rbet_subindustry_cap_top2000_1_5` | MATRIX | 0.5 | 0 | 0 | Relative beta of subindustry capitalization for top 2000 securities over a 1-5 day period. |
| 723 | `pv20_gp_rbet_subindustry_cap_top3000_1_20` | MATRIX | 0.5 | 1 | 1 | Relative beta of subindustry capitalization for top 3000 securities over a 1-20 day period. |
| 724 | `pv20_gp_rbet_subindustry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Relative beta of subindustry capitalization for top 3000 securities over a 1-5 day period. |
| 725 | `pv20_gp_rbet_subindustry_cap_top3000_1_60` | MATRIX | 0.5 | 0 | 0 | Relative beta of subindustry capitalization for top 3000 securities over a 1-60 day period. |
| 726 | `pv20_gp_ret_industry_cap_top3000_1_20` | MATRIX | 0.5 | 0 | 0 | Returns of industry capitalization for top 3000 securities over a 1-20 day period. |
| 727 | `pv20_gp_ret_industry_cap_top3000_1_5` | MATRIX | 0.5 | 1 | 1 | Returns of industry capitalization for top 3000 securities over a 1-5 day period. |
| 728 | `pv20_gp_ret_subindustry_cap_top2000_1_20` | MATRIX | 0.5 | 2 | 1 | Returns of subindustry capitalization for top 2000 securities over a 1-20 day period. |
| 729 | `pv20_gp_ret_subindustry_cap_top2000_1_5` | MATRIX | 0.5 | 1 | 1 | Returns of subindustry capitalization for top 2000 securities over a 1-5 day period. |
| 730 | `pv20_gp_ret_subindustry_cap_top3000_1_20` | MATRIX | 0.5 | 2 | 2 | Returns of subindustry capitalization for top 3000 securities over a 1-20 day period. |
| 731 | `pv20_gp_ret_subindustry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Returns of subindustry capitalization for top 3000 securities over a 1-5 day period. |
| 732 | `pv20_gp_ret_subindustry_cap_top3000_1_60` | MATRIX | 0.5 | 1 | 1 | Returns of subindustry capitalization for top 3000 securities over a 1-60 day period. |
| 733 | `pv20_gp_tvr_industry_cap_top3000_1_20` | MATRIX | 0.5 | 9 | 3 | Turnover ratio of industry capitalization for top 3000 securities over a 1-20 day period. |
| 734 | `pv20_gp_tvr_industry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Turnover ratio of industry capitalization for top 3000 securities over a 1-5 day period. |
| 735 | `pv20_gp_tvr_subindustry_cap_top2000_1_20` | MATRIX | 0.5 | 0 | 0 | Turnover ratio of subindustry capitalization for top 2000 securities over a 1-20 day period. |
| 736 | `pv20_gp_tvr_subindustry_cap_top2000_1_5` | MATRIX | 0.5 | 0 | 0 | Turnover ratio of subindustry capitalization for top 2000 securities over a 1-5 day period. |
| 737 | `pv20_gp_tvr_subindustry_cap_top3000_1_20` | MATRIX | 0.5 | 0 | 0 | Turnover ratio of subindustry capitalization for top 3000 securities over a 1-20 day period. |
| 738 | `pv20_gp_tvr_subindustry_cap_top3000_1_5` | MATRIX | 0.5 | 0 | 0 | Turnover ratio of subindustry capitalization for top 3000 securities over a 1-5 day period. |
| 739 | `pv20_gp_tvr_subindustry_cap_top3000_1_60` | MATRIX | 0.5 | 1 | 1 | Turnover ratio of subindustry capitalization for top 3000 securities over a 1-60 day period. |
| 740 | `pv20_gps_indicator_1_feature0` | MATRIX | 0.9572 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [mean_flash] |
| 741 | `pv20_gps_indicator_1_feature1` | MATRIX | 0.9409 | 0 | 0 | Indicator 1, Feature 1 extracted heuristically from IBES Pre-tax Profit modules |
| 742 | `pv20_gps_indicator_1_feature10` | MATRIX | 0.9506 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 743 | `pv20_gps_indicator_1_feature11` | MATRIX | 0.9506 | 0 | 0 | Indicator 1, Feature 11 from IBES Pre-tax Profit heuristics |
| 744 | `pv20_gps_indicator_1_feature12` | MATRIX | 0.9571 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 745 | `pv20_gps_indicator_1_feature2` | MATRIX | 0.9506 | 0 | 0 | Indicator 1, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 746 | `pv20_gps_indicator_1_feature3` | MATRIX | 0.8993 | 0 | 0 | Feature 3 from Indicator 1 in IBES Pre-tax Profit module |
| 747 | `pv20_gps_indicator_1_feature4` | MATRIX | 0.8993 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 748 | `pv20_gps_indicator_1_feature5` | MATRIX | 0.8993 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 749 | `pv20_gps_indicator_1_feature6` | MATRIX | 0.9012 | 0 | 0 | Indicator 1, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 750 | `pv20_gps_indicator_1_feature7` | MATRIX | 0.9409 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 751 | `pv20_gps_indicator_1_feature8` | MATRIX | 1 | 3 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 752 | `pv20_gps_indicator_1_feature9` | MATRIX | 0.9572 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 753 | `pv20_gps_indicator_2_feature0` | MATRIX | 0.9584 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [mean_flash] |
| 754 | `pv20_gps_indicator_2_feature1` | MATRIX | 0.9372 | 5 | 5 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [median 3 months ago] |
| 755 | `pv20_gps_indicator_2_feature10` | MATRIX | 0.9484 | 1 | 1 | Feature 10 from Indicator 2 in IBES Pre-tax Profit heuristics |
| 756 | `pv20_gps_indicator_2_feature11` | MATRIX | 0.9484 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 757 | `pv20_gps_indicator_2_feature12` | MATRIX | 0.9583 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 758 | `pv20_gps_indicator_2_feature2` | MATRIX | 0.9484 | 0 | 0 | Feature 2 from Indicator 2 in IBES Pre-tax Profit module |
| 759 | `pv20_gps_indicator_2_feature3` | MATRIX | 0.8949 | 0 | 0 | Indicator 2, Feature 3 extracted heuristically from IBES Pre-tax Profit modules |
| 760 | `pv20_gps_indicator_2_feature4` | MATRIX | 0.8949 | 0 | 0 | Indicator 2, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 761 | `pv20_gps_indicator_2_feature5` | MATRIX | 0.8949 | 0 | 0 | Indicator 2, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 762 | `pv20_gps_indicator_2_feature6` | MATRIX | 0.8963 | 0 | 0 | Feature 6 from Indicator 2 in IBES Pre-tax Profit module |
| 763 | `pv20_gps_indicator_2_feature7` | MATRIX | 0.9372 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 764 | `pv20_gps_indicator_2_feature8` | MATRIX | 1 | 5 | 5 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 765 | `pv20_gps_indicator_2_feature9` | MATRIX | 0.9584 | 2 | 2 | Indicator 2, Feature 9 extracted heuristically from IBES Pre-tax Profit modules |
| 766 | `pv20_gps_indicator_3_feature0` | MATRIX | 0.9445 | 0 | 0 | Indicator 3, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 767 | `pv20_gps_indicator_3_feature1` | MATRIX | 0.8815 | 1 | 1 | Indicator 3, Feature 1 from IBES Pre-tax Profit heuristics |
| 768 | `pv20_gps_indicator_3_feature10` | MATRIX | 0.9062 | 0 | 0 | Indicator 3, Feature 10 from IBES Pre-tax Profit heuristics |
| 769 | `pv20_gps_indicator_3_feature11` | MATRIX | 0.9062 | 0 | 0 | Indicator 3, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 770 | `pv20_gps_indicator_3_feature12` | MATRIX | 0.9444 | 2 | 2 | Indicator 3, Feature 12 from IBES Pre-tax Profit heuristics |
| 771 | `pv20_gps_indicator_3_feature2` | MATRIX | 0.9062 | 0 | 0 | Indicator 3, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 772 | `pv20_gps_indicator_3_feature3` | MATRIX | 0.762 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 773 | `pv20_gps_indicator_3_feature4` | MATRIX | 0.762 | 0 | 0 | Feature 4 from Indicator 3 in IBES Pre-tax Profit module |
| 774 | `pv20_gps_indicator_3_feature5` | MATRIX | 0.762 | 0 | 0 | Indicator 3, Feature 5 from IBES Pre-tax Profit heuristics |
| 775 | `pv20_gps_indicator_3_feature6` | MATRIX | 0.7653 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 776 | `pv20_gps_indicator_3_feature7` | MATRIX | 0.8815 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 777 | `pv20_gps_indicator_3_feature8` | MATRIX | 1 | 1 | 1 | Indicator 3, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 778 | `pv20_gps_indicator_3_feature9` | MATRIX | 0.9445 | 0 | 0 | Feature 9 from Indicator 3 in IBES Pre-tax Profit module |
| 779 | `pv20_gps_indicator_4_feature0` | MATRIX | 0.7598 | 0 | 0 | Indicator 4, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 780 | `pv20_gps_indicator_4_feature1` | MATRIX | 0.6132 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [median 3 months ago] |
| 781 | `pv20_gps_indicator_4_feature10` | MATRIX | 0.646 | 0 | 0 | Feature number 10 for indicator 4 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 782 | `pv20_gps_indicator_4_feature11` | MATRIX | 0.646 | 0 | 0 | Indicator 4, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 783 | `pv20_gps_indicator_4_feature12` | MATRIX | 0.7597 | 0 | 0 | Indicator 4, Feature 12 extracted heuristically from IBES Pre-tax Profit modules |
| 784 | `pv20_gps_indicator_4_feature2` | MATRIX | 0.646 | 0 | 0 | Median IBES Pre-tax Profit estimate for Fiscal Year 4 as of 4 weeks ago |
| 785 | `pv20_gps_indicator_4_feature3` | MATRIX | 0.3582 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 786 | `pv20_gps_indicator_4_feature4` | MATRIX | 0.3582 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 787 | `pv20_gps_indicator_4_feature5` | MATRIX | 0.3582 | 0 | 0 | Feature 5 from Indicator 4 in IBES Pre-tax Profit module |
| 788 | `pv20_gps_indicator_4_feature6` | MATRIX | 0.3611 | 2 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 789 | `pv20_gps_indicator_4_feature7` | MATRIX | 0.6132 | 0 | 0 | Indicator 4, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 790 | `pv20_gps_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator 4 in IBES Pre-tax Profit module |
| 791 | `pv20_gps_indicator_4_feature9` | MATRIX | 0.7598 | 0 | 0 | Feature 9 from Indicator 4 in IBES Pre-tax Profit module |
| 792 | `pv20_gps_indicator_6_feature1` | MATRIX | 0.9178 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [median 3 months ago] |
| 793 | `pv20_gps_indicator_6_feature10` | MATRIX | 0.9294 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 794 | `pv20_gps_indicator_6_feature2` | MATRIX | 0.9294 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [median 4 weeks ago] |
| 795 | `pv20_gps_indicator_6_feature5` | MATRIX | 0.8611 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 796 | `pv20_gps_indicator_6_feature6` | MATRIX | 0.8645 | 3 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 797 | `pv20_gps_indicator_6_feature7` | MATRIX | 0.9178 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 798 | `pv20_gps_indicator_6_feature8` | MATRIX | 1 | 11 | 11 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 799 | `pv20_gps_indicator_6_feature9` | MATRIX | 0.9345 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 800 | `pv20_gps_indicator_7_feature0` | MATRIX | 0.9331 | 3 | 3 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [mean_flash] |
| 801 | `pv20_gps_indicator_7_feature10` | MATRIX | 0.9272 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 802 | `pv20_gps_indicator_7_feature11` | MATRIX | 0.9272 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 803 | `pv20_gps_indicator_7_feature12` | MATRIX | 0.9327 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 804 | `pv20_gps_indicator_7_feature2` | MATRIX | 0.9272 | 5 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [median 4 weeks ago] |
| 805 | `pv20_gps_indicator_7_feature3` | MATRIX | 0.8528 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 806 | `pv20_gps_indicator_7_feature4` | MATRIX | 0.8528 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 807 | `pv20_gps_indicator_7_feature5` | MATRIX | 0.8528 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 808 | `pv20_gps_indicator_7_feature7` | MATRIX | 0.915 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 809 | `pv20_gps_indicator_7_feature9` | MATRIX | 0.9331 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 810 | `pv20_gps_indicator_8_feature1` | MATRIX | 0.9077 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [median 3 months ago] |
| 811 | `pv20_gps_indicator_8_feature11` | MATRIX | 0.9238 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 812 | `pv20_gps_indicator_8_feature12` | MATRIX | 0.9314 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 813 | `pv20_gps_indicator_8_feature3` | MATRIX | 0.8397 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 814 | `pv20_gps_indicator_8_feature7` | MATRIX | 0.9077 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 815 | `pv20_gps_indicator_8_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 816 | `pv20_gps_indicator_8_feature9` | MATRIX | 0.9318 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 817 | `pv20_gps_indicator_9_feature1` | MATRIX | 0.8936 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [median 3 months ago] |
| 818 | `pv20_gps_indicator_9_feature10` | MATRIX | 0.9141 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 819 | `pv20_gps_indicator_9_feature11` | MATRIX | 0.9141 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 820 | `pv20_gps_indicator_9_feature12` | MATRIX | 0.9296 | 3 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 821 | `pv20_gps_indicator_9_feature5` | MATRIX | 0.8076 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 822 | `pv20_gps_indicator_9_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 823 | `pv20_gps_indicator_9_feature9` | MATRIX | 0.9302 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 824 | `pv20_gps_indicator_n_feature10` | MATRIX | 0.8967 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 825 | `pv20_gps_indicator_n_feature11` | MATRIX | 0.8967 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 826 | `pv20_gps_indicator_n_feature2` | MATRIX | 0.8967 | 1 | 1 | Heuristically extracted predictive feature 2 from the IBES Pre-tax Profit module (Indicator N) for Quarter 5;  |
| 827 | `pv20_gps_indicator_n_feature3` | MATRIX | 0.7657 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 828 | `pv20_gps_indicator_n_feature4` | MATRIX | 0.7657 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 829 | `pv20_gps_indicator_n_feature5` | MATRIX | 0.7657 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 830 | `pv20_gps_indicator_n_feature6` | MATRIX | 0.7731 | 3 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 831 | `pv20_gps_indicator_n_feature7` | MATRIX | 0.8772 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 832 | `pv20_gps_indicator_n_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 833 | `pv20_gps_indicator_n_feature9` | MATRIX | 0.9184 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 834 | `pv20_gps_indicator_o_feature0` | MATRIX | 0.9021 | 1 | 1 | Heuristically extracted predictive feature 0 from the IBES Pre-tax Profit module (Indicator O) for Quarter 6;  |
| 835 | `pv20_gps_indicator_o_feature1` | MATRIX | 0.8505 | 0 | 0 | Heuristically extracted predictive feature 1 from the IBES Pre-tax Profit module (Indicator O) for Quarter 6;  |
| 836 | `pv20_gps_indicator_o_feature10` | MATRIX | 0.8773 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 837 | `pv20_gps_indicator_o_feature11` | MATRIX | 0.8773 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 838 | `pv20_gps_indicator_o_feature12` | MATRIX | 0.9017 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 839 | `pv20_gps_indicator_o_feature2` | MATRIX | 0.8773 | 0 | 0 | Heuristically extracted predictive feature 2 from the IBES Pre-tax Profit module (Indicator O) for Quarter 6;  |
| 840 | `pv20_gps_indicator_o_feature3` | MATRIX | 0.7008 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 841 | `pv20_gps_indicator_o_feature5` | MATRIX | 0.7008 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 842 | `pv20_gps_indicator_o_feature6` | MATRIX | 0.7098 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 843 | `pv20_gps_indicator_o_feature7` | MATRIX | 0.8505 | 2 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 844 | `pv20_gps_indicator_o_feature9` | MATRIX | 0.9021 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 845 | `pv20_gps_indicator_p_feature0` | MATRIX | 0.8875 | 1 | 1 | Heuristically extracted predictive feature 0 from the IBES Pre-tax Profit module (Indicator P) for Quarter 7;  |
| 846 | `pv20_gps_indicator_p_feature10` | MATRIX | 0.8493 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 847 | `pv20_gps_indicator_p_feature2` | MATRIX | 0.8493 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [median 4 weeks ago] |
| 848 | `pv20_gps_indicator_p_feature4` | MATRIX | 0.6043 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 849 | `pv20_gps_indicator_p_feature5` | MATRIX | 0.6043 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 850 | `pv20_gps_indicator_p_feature6` | MATRIX | 0.6157 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 851 | `pv20_gps_indicator_p_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 852 | `pv20_gps_indicator_q_feature0` | MATRIX | 0.8617 | 1 | 1 | IBES predictive indicator for Pre-tax Profit, Quarter 8; mean of flash estimates |
| 853 | `pv20_gps_indicator_q_feature11` | MATRIX | 0.7809 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 854 | `pv20_gps_indicator_q_feature2` | MATRIX | 0.7809 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [median 4 weeks ago] |
| 855 | `pv20_gps_indicator_q_feature7` | MATRIX | 0.7123 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 856 | `pv20_gps_indicator_q_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 857 | `pv20_gps_indicator_q_feature9` | MATRIX | 0.8617 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 858 | `pv20_group_all` | MATRIX | 1 | 2 | 2 | Aggregated group factor for all securities. |
| 859 | `pv20_image_iv2image` | VECTOR | 1 | 3 | 3 | Image associated |
| 860 | `pv20_indicator_0_feature0_121` | MATRIX | 0.8253 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [mean_flash] |
| 861 | `pv20_indicator_0_feature10` | MATRIX | 0.808 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [Non-trivial fea |
| 862 | `pv20_indicator_0_feature11_124` | MATRIX | 0.808 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [Non-trivial fea |
| 863 | `pv20_indicator_0_feature1_123` | MATRIX | 0.7943 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [median 3 months |
| 864 | `pv20_indicator_0_feature3` | MATRIX | 0.5253 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [Non-trivial fea |
| 865 | `pv20_indicator_0_feature6_122` | MATRIX | 0.5467 | 0 | 0 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [Non-trivial fea |
| 866 | `pv20_indicator_0_feature7_120` | MATRIX | 0.7943 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Long Term Growth] [Non-trivial fea |
| 867 | `pv20_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 868 | `pv20_indicator_8_feature5` | MATRIX | 0.902 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 869 | `pv20_indicator_n_feature12` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Earnings per Share] [Quarter 5] [Non-trivial feature] |
| 870 | `pv20_industry` | GROUP | 0.5 | 5 | 2 | Industry classification for USA data. |
| 871 | `pv20_industrysd` | MATRIX | 0.5 | 2 | 2 | Standard deviation of industry returns for USA data. |
| 872 | `pv20_industrysdw` | MATRIX | 0.5 | 12 | 4 | Weighted standard deviation of industry returns for USA data. |
| 873 | `pv20_industryw` | MATRIX | 0.5 | 18 | 3 | Weighted industry returns for USA data. |
| 874 | `pv20_interimperiodend_116` | VECTOR | 1 | 1 | 1 | End date of the interim period |
| 875 | `pv20_interimperiodnum_117` | VECTOR | 1 | 0 | 0 | Number of the interim period |
| 876 | `pv20_label` | MATRIX | 0.8903 | 5 | 5 | Label associated with USA Finchcharts Funda data. |
| 877 | `pv20_label2` | MATRIX | 0.9843 | 76 | 54 | Secondary label for USA Finchcharts SFunda data. |
| 878 | `pv20_label3` | MATRIX | 0.9843 | 117 | 83 | Tertiary label for USA Finchcharts SFunda data. |
| 879 | `pv20_label5` | MATRIX | 0.9843 | 92 | 61 | Fifth label for USA Finchcharts SFunda data. |
| 880 | `pv20_market` | GROUP | 0.5 | 4 | 4 | Market classification for USA data. |
| 881 | `pv20_marketsd` | MATRIX | 0.5 | 7 | 3 | Standard deviation of market returns for USA data. |
| 882 | `pv20_marketsdw` | MATRIX | 0.5 | 3 | 3 | Weighted standard deviation of market returns for USA data. |
| 883 | `pv20_marketw` | MATRIX | 0.5 | 4 | 4 | Weighted market returns for USA data. |
| 884 | `pv20_mktcap` | MATRIX | 0.892 | 6 | 3 | Market Cap |
| 885 | `pv20_negvol250` | MATRIX | 1 | 3 | 2 | Negative volatility over a 250-day period. |
| 886 | `pv20_net_indicator_1_feature0` | MATRIX | 0.9663 | 1 | 1 | Indicator 1, Feature 0 from IBES Pre-tax Profit heuristics |
| 887 | `pv20_net_indicator_1_feature1` | MATRIX | 0.951 | 0 | 0 | Median across analysts of IBES pre-tax profit (EBT) estimates for Fiscal Year 1 as of 3 months ago |
| 888 | `pv20_net_indicator_1_feature10` | MATRIX | 0.9601 | 0 | 0 | Indicator 1, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 889 | `pv20_net_indicator_1_feature11` | MATRIX | 0.9601 | 1 | 1 | Indicator 1, Feature 11 from IBES Pre-tax Profit heuristics |
| 890 | `pv20_net_indicator_1_feature12` | MATRIX | 0.9663 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 891 | `pv20_net_indicator_1_feature2` | MATRIX | 0.9601 | 0 | 0 | Indicator 1, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 892 | `pv20_net_indicator_1_feature3` | MATRIX | 0.9151 | 1 | 1 | Feature 3 from Indicator 1 in IBES Pre-tax Profit module |
| 893 | `pv20_net_indicator_1_feature4` | MATRIX | 0.9151 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 894 | `pv20_net_indicator_1_feature5` | MATRIX | 0.9151 | 3 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 895 | `pv20_net_indicator_1_feature6` | MATRIX | 0.9164 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 896 | `pv20_net_indicator_1_feature7` | MATRIX | 0.951 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 897 | `pv20_net_indicator_1_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 898 | `pv20_net_indicator_1_feature9` | MATRIX | 0.9663 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 899 | `pv20_net_indicator_2_feature0` | MATRIX | 0.967 | 0 | 0 | Latest flash mean across analysts of IBES pre-tax profit (EBT) estimates for Fiscal Year 2 |
| 900 | `pv20_net_indicator_2_feature1` | MATRIX | 0.9475 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [median 3 months ago] |
| 901 | `pv20_net_indicator_2_feature10` | MATRIX | 0.9582 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 902 | `pv20_net_indicator_2_feature11` | MATRIX | 0.9582 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 903 | `pv20_net_indicator_2_feature12` | MATRIX | 0.967 | 4 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 904 | `pv20_net_indicator_2_feature2` | MATRIX | 0.9582 | 0 | 0 | Median across analysts of IBES pre-tax profit (EBT) estimates for Fiscal Year 2 as of 4 weeks ago |
| 905 | `pv20_net_indicator_2_feature3` | MATRIX | 0.9124 | 1 | 1 | Indicator 2, Feature 3 extracted heuristically from IBES Pre-tax Profit modules |
| 906 | `pv20_net_indicator_2_feature4` | MATRIX | 0.9124 | 0 | 0 | Indicator 2, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 907 | `pv20_net_indicator_2_feature5` | MATRIX | 0.9124 | 0 | 0 | Indicator 2, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 908 | `pv20_net_indicator_2_feature6` | MATRIX | 0.9138 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 909 | `pv20_net_indicator_2_feature7` | MATRIX | 0.9475 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 910 | `pv20_net_indicator_2_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 2] [Non-trivial feature] |
| 911 | `pv20_net_indicator_2_feature9` | MATRIX | 0.967 | 2 | 2 | Indicator 2, Feature 9 extracted heuristically from IBES Pre-tax Profit modules |
| 912 | `pv20_net_indicator_3_feature0` | MATRIX | 0.9582 | 0 | 0 | Latest flash mean across analysts of IBES pre-tax profit (EBT) estimates for Fiscal Year 3 |
| 913 | `pv20_net_indicator_3_feature1` | MATRIX | 0.9121 | 0 | 0 | Indicator 3, Feature 1 from IBES Pre-tax Profit heuristics |
| 914 | `pv20_net_indicator_3_feature10` | MATRIX | 0.9301 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 915 | `pv20_net_indicator_3_feature11` | MATRIX | 0.9301 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 916 | `pv20_net_indicator_3_feature12` | MATRIX | 0.9582 | 11 | 10 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 917 | `pv20_net_indicator_3_feature2` | MATRIX | 0.9301 | 2 | 2 | Median across analysts of IBES Pre-tax Profit estimates for forecast fiscal year 3 (FY3) as of 4 weeks ago |
| 918 | `pv20_net_indicator_3_feature3` | MATRIX | 0.8234 | 0 | 0 | Feature 3 from Indicator 3 in IBES Pre-tax Profit module |
| 919 | `pv20_net_indicator_3_feature4` | MATRIX | 0.8234 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 920 | `pv20_net_indicator_3_feature5` | MATRIX | 0.8234 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 921 | `pv20_net_indicator_3_feature6` | MATRIX | 0.8259 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 922 | `pv20_net_indicator_3_feature7` | MATRIX | 0.9121 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 3] [Non-trivial feature] |
| 923 | `pv20_net_indicator_3_feature8` | MATRIX | 1 | 0 | 0 | Indicator 3, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 924 | `pv20_net_indicator_3_feature9` | MATRIX | 0.9582 | 0 | 0 | Feature 9 from Indicator 3 in IBES Pre-tax Profit module |
| 925 | `pv20_net_indicator_4_feature0` | MATRIX | 0.8253 | 0 | 0 | Latest flash mean across analysts of IBES pre-tax profit (EBT) estimates for Fiscal Year 4 |
| 926 | `pv20_net_indicator_4_feature1` | MATRIX | 0.6795 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [median 3 months ago] |
| 927 | `pv20_net_indicator_4_feature10` | MATRIX | 0.7138 | 2 | 2 | Feature number 10 for indicator 4 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 928 | `pv20_net_indicator_4_feature11` | MATRIX | 0.7138 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 929 | `pv20_net_indicator_4_feature12` | MATRIX | 0.8253 | 0 | 0 | Indicator 4, Feature 12 extracted heuristically from IBES Pre-tax Profit modules |
| 930 | `pv20_net_indicator_4_feature2` | MATRIX | 0.7138 | 0 | 0 | Indicator 4, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 931 | `pv20_net_indicator_4_feature3` | MATRIX | 0.428 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 932 | `pv20_net_indicator_4_feature4` | MATRIX | 0.428 | 0 | 0 | Indicator 4, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 933 | `pv20_net_indicator_4_feature5` | MATRIX | 0.428 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 934 | `pv20_net_indicator_4_feature6` | MATRIX | 0.433 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 935 | `pv20_net_indicator_4_feature7` | MATRIX | 0.6795 | 0 | 0 | Indicator 4, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 936 | `pv20_net_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator 4 in IBES Pre-tax Profit module |
| 937 | `pv20_net_indicator_4_feature9` | MATRIX | 0.8253 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 938 | `pv20_net_indicator_6_feature1` | MATRIX | 0.9267 | 6 | 6 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [median 3 months ago] |
| 939 | `pv20_net_indicator_6_feature12` | MATRIX | 0.9442 | 2 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 940 | `pv20_net_indicator_6_feature2` | MATRIX | 0.9383 | 1 | 1 | Median across analysts of IBES Pre-tax Profit estimates for forecast quarter 1 (Q1) as of 4 weeks ago |
| 941 | `pv20_net_indicator_6_feature3` | MATRIX | 0.8715 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 942 | `pv20_net_indicator_6_feature4` | MATRIX | 0.8715 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 943 | `pv20_net_indicator_6_feature6` | MATRIX | 0.874 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 944 | `pv20_net_indicator_6_feature7` | MATRIX | 0.9267 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 945 | `pv20_net_indicator_6_feature9` | MATRIX | 0.9443 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 946 | `pv20_net_indicator_7_feature1` | MATRIX | 0.9224 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [median 3 months ago] |
| 947 | `pv20_net_indicator_7_feature10` | MATRIX | 0.9361 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 948 | `pv20_net_indicator_7_feature12` | MATRIX | 0.943 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 949 | `pv20_net_indicator_7_feature2` | MATRIX | 0.9361 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [median 4 weeks ago] |
| 950 | `pv20_net_indicator_7_feature3` | MATRIX | 0.8636 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 951 | `pv20_net_indicator_7_feature4` | MATRIX | 0.8636 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 952 | `pv20_net_indicator_7_feature5` | MATRIX | 0.8636 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 953 | `pv20_net_indicator_7_feature6` | MATRIX | 0.8665 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 954 | `pv20_net_indicator_7_feature7` | MATRIX | 0.9224 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 955 | `pv20_net_indicator_7_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 956 | `pv20_net_indicator_7_feature9` | MATRIX | 0.9433 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 957 | `pv20_net_indicator_8_feature12` | MATRIX | 0.9408 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 958 | `pv20_net_indicator_8_feature2` | MATRIX | 0.9317 | 1 | 1 | Median IBES pre-tax profit (EBT) estimate for Quarter 3 as of 4 weeks ago |
| 959 | `pv20_net_indicator_8_feature6` | MATRIX | 0.8525 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 960 | `pv20_net_indicator_8_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 961 | `pv20_net_indicator_9_feature0` | MATRIX | 0.9387 | 0 | 0 | Mean of flash IBES pre-tax profit estimates for Quarter 4 |
| 962 | `pv20_net_indicator_9_feature1` | MATRIX | 0.9018 | 0 | 0 | Median across analysts of IBES Pre-tax Profit estimates for forecast quarter 4 (Q4) as of 3 months ago |
| 963 | `pv20_net_indicator_9_feature10` | MATRIX | 0.9221 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 964 | `pv20_net_indicator_9_feature12` | MATRIX | 0.9383 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 965 | `pv20_net_indicator_9_feature4` | MATRIX | 0.8158 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 966 | `pv20_net_indicator_9_feature6` | MATRIX | 0.8186 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 967 | `pv20_net_indicator_9_feature7` | MATRIX | 0.9018 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 968 | `pv20_net_indicator_9_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 969 | `pv20_net_indicator_n_feature0` | MATRIX | 0.9282 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [mean_flash] |
| 970 | `pv20_net_indicator_n_feature1` | MATRIX | 0.8825 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [median 3 months ago] |
| 971 | `pv20_net_indicator_n_feature10` | MATRIX | 0.9044 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 972 | `pv20_net_indicator_n_feature2` | MATRIX | 0.9044 | 0 | 0 | Median IBES pre-tax profit estimate for Quarter 5 as of 4 weeks ago |
| 973 | `pv20_net_indicator_n_feature3` | MATRIX | 0.7756 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 974 | `pv20_net_indicator_n_feature4` | MATRIX | 0.7756 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 975 | `pv20_net_indicator_n_feature5` | MATRIX | 0.7756 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 976 | `pv20_net_indicator_n_feature6` | MATRIX | 0.7787 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 977 | `pv20_net_indicator_n_feature7` | MATRIX | 0.8825 | 5 | 5 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 978 | `pv20_net_indicator_n_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 979 | `pv20_net_indicator_n_feature9` | MATRIX | 0.9282 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 980 | `pv20_net_indicator_o_feature12` | MATRIX | 0.9104 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 981 | `pv20_net_indicator_o_feature2` | MATRIX | 0.8832 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [median 4 weeks ago] |
| 982 | `pv20_net_indicator_o_feature3` | MATRIX | 0.7112 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 983 | `pv20_net_indicator_o_feature5` | MATRIX | 0.7112 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 984 | `pv20_net_indicator_o_feature6` | MATRIX | 0.7156 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 985 | `pv20_net_indicator_o_feature7` | MATRIX | 0.8542 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 986 | `pv20_net_indicator_o_feature9` | MATRIX | 0.9114 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 987 | `pv20_net_indicator_p_feature12` | MATRIX | 0.8942 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 988 | `pv20_net_indicator_p_feature2` | MATRIX | 0.8536 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [median 4 weeks ago] |
| 989 | `pv20_net_indicator_p_feature3` | MATRIX | 0.6289 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 990 | `pv20_net_indicator_p_feature4` | MATRIX | 0.6289 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 991 | `pv20_net_indicator_p_feature8` | MATRIX | 1 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 992 | `pv20_net_indicator_p_feature9` | MATRIX | 0.8952 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 993 | `pv20_net_indicator_q_feature0` | MATRIX | 0.8696 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [mean_flash] |
| 994 | `pv20_net_indicator_q_feature1` | MATRIX | 0.7353 | 0 | 0 | Median IBES pre-tax profit estimate for Quarter 8 as of 3 months ago |
| 995 | `pv20_net_indicator_q_feature10` | MATRIX | 0.7932 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 996 | `pv20_net_indicator_q_feature11` | MATRIX | 0.7932 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 997 | `pv20_net_indicator_q_feature2` | MATRIX | 0.7932 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [median 4 weeks ago] |
| 998 | `pv20_net_indicator_q_feature4` | MATRIX | 0.487 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 999 | `pv20_net_indicator_q_feature5` | MATRIX | 0.487 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1000 | `pv20_net_indicator_q_feature6` | MATRIX | 0.4939 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1001 | `pv20_net_indicator_q_feature7` | MATRIX | 0.7353 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1002 | `pv20_opr_indicator_1_feature0` | MATRIX | 0.7434 | 0 | 0 | Indicator 1, Feature 0 from IBES Pre-tax Profit heuristics |
| 1003 | `pv20_opr_indicator_1_feature1` | MATRIX | 0.6933 | 0 | 0 | Indicator 1, Feature 1 extracted heuristically from IBES Pre-tax Profit modules |
| 1004 | `pv20_opr_indicator_1_feature10` | MATRIX | 0.7039 | 0 | 0 | Indicator 1, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1005 | `pv20_opr_indicator_1_feature11` | MATRIX | 0.7039 | 0 | 0 | Indicator 1, Feature 11 from IBES Pre-tax Profit heuristics |
| 1006 | `pv20_opr_indicator_1_feature12` | MATRIX | 0.743 | 1 | 1 | Feature 12 from Indicator 1 in IBES Pre-tax Profit module |
| 1007 | `pv20_opr_indicator_1_feature2` | MATRIX | 0.7039 | 0 | 0 | Indicator 1, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1008 | `pv20_opr_indicator_1_feature3` | MATRIX | 0.5092 | 0 | 0 | Feature 3 from Indicator 1 in IBES Pre-tax Profit module |
| 1009 | `pv20_opr_indicator_1_feature4` | MATRIX | 0.5092 | 0 | 0 | Feature 4 from Indicator 1 in IBES Pre-tax Profit module |
| 1010 | `pv20_opr_indicator_1_feature5` | MATRIX | 0.5092 | 0 | 0 | Feature 5 from Indicator 1 in IBES Pre-tax Profit module |
| 1011 | `pv20_opr_indicator_1_feature6` | MATRIX | 0.5168 | 0 | 0 | Indicator 1, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 1012 | `pv20_opr_indicator_1_feature7` | MATRIX | 0.6933 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1013 | `pv20_opr_indicator_1_feature8` | MATRIX | 1 | 0 | 0 | Indicator 1, Feature 8 from IBES Pre-tax Profit heuristics |
| 1014 | `pv20_opr_indicator_1_feature9` | MATRIX | 0.7434 | 0 | 0 | Feature 9 from Indicator 1 in IBES Pre-tax Profit module |
| 1015 | `pv20_opr_indicator_2_feature0` | MATRIX | 0.7361 | 3 | 1 | Indicator 2, Feature 0 from IBES Pre-tax Profit heuristics |
| 1016 | `pv20_opr_indicator_2_feature1` | MATRIX | 0.669 | 0 | 0 | Feature 1 from Indicator 2 in IBES Pre-tax Profit module |
| 1017 | `pv20_opr_indicator_2_feature10` | MATRIX | 0.6835 | 0 | 0 | Indicator 2, Feature 10 from IBES Pre-tax Profit heuristics |
| 1018 | `pv20_opr_indicator_2_feature11` | MATRIX | 0.6835 | 0 | 0 | Indicator 2, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1019 | `pv20_opr_indicator_2_feature12` | MATRIX | 0.7359 | 0 | 0 | Feature 12 from Indicator 2 in IBES Pre-tax Profit module |
| 1020 | `pv20_opr_indicator_2_feature2` | MATRIX | 0.6835 | 1 | 1 | Feature 2 from Indicator 2 in IBES Pre-tax Profit module |
| 1021 | `pv20_opr_indicator_2_feature3` | MATRIX | 0.4993 | 0 | 0 | Indicator 2, Feature 3 extracted heuristically from IBES Pre-tax Profit modules |
| 1022 | `pv20_opr_indicator_2_feature4` | MATRIX | 0.4993 | 0 | 0 | Indicator 2, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 1023 | `pv20_opr_indicator_2_feature5` | MATRIX | 0.4993 | 0 | 0 | Indicator 2, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1024 | `pv20_opr_indicator_2_feature6` | MATRIX | 0.5047 | 0 | 0 | Feature 6 from Indicator 2 in IBES Pre-tax Profit module |
| 1025 | `pv20_opr_indicator_2_feature7` | MATRIX | 0.669 | 1 | 1 | Indicator 2, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 1026 | `pv20_opr_indicator_2_feature8` | MATRIX | 1 | 0 | 0 | Indicator 2, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1027 | `pv20_opr_indicator_2_feature9` | MATRIX | 0.7361 | 0 | 0 | Indicator 2, Feature 9 extracted heuristically from IBES Pre-tax Profit modules |
| 1028 | `pv20_opr_indicator_3_feature0` | MATRIX | 0.6773 | 0 | 0 | Indicator 3, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1029 | `pv20_opr_indicator_3_feature1` | MATRIX | 0.5544 | 0 | 0 | Indicator 3, Feature 1 from IBES Pre-tax Profit heuristics |
| 1030 | `pv20_opr_indicator_3_feature10` | MATRIX | 0.5807 | 1 | 1 | Indicator 3, Feature 10 from IBES Pre-tax Profit heuristics |
| 1031 | `pv20_opr_indicator_3_feature11` | MATRIX | 0.5807 | 0 | 0 | Indicator 3, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1032 | `pv20_opr_indicator_3_feature12` | MATRIX | 0.6772 | 2 | 2 | Indicator 3, Feature 12 from IBES Pre-tax Profit heuristics |
| 1033 | `pv20_opr_indicator_3_feature2` | MATRIX | 0.5807 | 0 | 0 | Indicator 3, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1034 | `pv20_opr_indicator_3_feature3` | MATRIX | 0.372 | 0 | 0 | Feature 3 from Indicator 3 in IBES Pre-tax Profit module |
| 1035 | `pv20_opr_indicator_3_feature4` | MATRIX | 0.372 | 0 | 0 | Feature 4 from Indicator 3 in IBES Pre-tax Profit module |
| 1036 | `pv20_opr_indicator_3_feature5` | MATRIX | 0.372 | 0 | 0 | Indicator 3, Feature 5 from IBES Pre-tax Profit heuristics |
| 1037 | `pv20_opr_indicator_3_feature6` | MATRIX | 0.3774 | 0 | 0 | Indicator 3, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 1038 | `pv20_opr_indicator_3_feature7` | MATRIX | 0.5544 | 0 | 0 | Feature 7 from Indicator 3 in IBES Pre-tax Profit module |
| 1039 | `pv20_opr_indicator_3_feature8` | MATRIX | 1 | 3 | 1 | Indicator 3, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1040 | `pv20_opr_indicator_3_feature9` | MATRIX | 0.6773 | 1 | 1 | Feature 9 from Indicator 3 in IBES Pre-tax Profit module |
| 1041 | `pv20_opr_indicator_4_feature0` | MATRIX | 0.4413 | 0 | 0 | Indicator 4, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1042 | `pv20_opr_indicator_4_feature1` | MATRIX | 0.3026 | 0 | 0 | Feature 1 from Indicator 4 module |
| 1043 | `pv20_opr_indicator_4_feature10` | MATRIX | 0.33 | 0 | 0 | Feature number 10 for indicator 4 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 1044 | `pv20_opr_indicator_4_feature11` | MATRIX | 0.33 | 0 | 0 | Indicator 4, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1045 | `pv20_opr_indicator_4_feature12` | MATRIX | 0.4413 | 0 | 0 | Indicator 4, Feature 12 extracted heuristically from IBES Pre-tax Profit modules |
| 1046 | `pv20_opr_indicator_4_feature2` | MATRIX | 0.33 | 11 | 7 | Indicator 4, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1047 | `pv20_opr_indicator_4_feature7` | MATRIX | 0.3026 | 0 | 0 | Indicator 4, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 1048 | `pv20_opr_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator 4 in IBES Pre-tax Profit module |
| 1049 | `pv20_opr_indicator_4_feature9` | MATRIX | 0.4413 | 0 | 0 | Feature 9 from Indicator 4 in IBES Pre-tax Profit module |
| 1050 | `pv20_opr_indicator_6_feature0` | MATRIX | 0.6542 | 0 | 0 | Indicator 6, Feature 0 (specific heuristic or metric from IBES module) |
| 1051 | `pv20_opr_indicator_6_feature1` | MATRIX | 0.6264 | 0 | 0 | Indicator 6, Feature 1 extracted heuristically from IBES Pre-tax Profit modules |
| 1052 | `pv20_opr_indicator_6_feature2` | MATRIX | 0.6441 | 2 | 2 | Feature 2 from Indicator 6 in IBES Pre-tax Profit module |
| 1053 | `pv20_opr_indicator_6_feature3` | MATRIX | 0.4303 | 0 | 0 | Feature 3 from Indicator 6 in IBES Pre-tax Profit module |
| 1054 | `pv20_opr_indicator_6_feature5` | MATRIX | 0.4303 | 0 | 0 | Indicator 6, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1055 | `pv20_opr_indicator_6_feature7` | MATRIX | 0.6264 | 0 | 0 | Feature 7 from Indicator 6 in IBES Pre-tax Profit module |
| 1056 | `pv20_opr_indicator_6_feature8` | MATRIX | 1 | 0 | 0 | Indicator 6, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1057 | `pv20_opr_indicator_6_feature9` | MATRIX | 0.6542 | 0 | 0 | Feature 9 from Indicator 6 in IBES Pre-tax Profit module |
| 1058 | `pv20_opr_indicator_7_feature0` | MATRIX | 0.6412 | 0 | 0 | Indicator 7, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1059 | `pv20_opr_indicator_7_feature10` | MATRIX | 0.6331 | 0 | 0 | Indicator 7, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1060 | `pv20_opr_indicator_7_feature11` | MATRIX | 0.6331 | 0 | 0 | Feature 11 from Indicator 7 in IBES Pre-tax Profit module |
| 1061 | `pv20_opr_indicator_7_feature2` | MATRIX | 0.6331 | 0 | 0 | Indicator 7, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1062 | `pv20_opr_indicator_7_feature3` | MATRIX | 0.4215 | 0 | 0 | Feature number 3 for Indicator 7 extracted heuristically from IBES modules of Pre-tax Profit for Quarter 3 (me |
| 1063 | `pv20_opr_indicator_7_feature4` | MATRIX | 0.4215 | 0 | 0 | Feature 4 from Indicator 7 in IBES Pre-tax Profit module |
| 1064 | `pv20_opr_indicator_7_feature5` | MATRIX | 0.4215 | 0 | 0 | Indicator 7, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1065 | `pv20_opr_indicator_7_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1066 | `pv20_opr_indicator_7_feature9` | MATRIX | 0.6412 | 0 | 0 | Feature 9 of Indicator 7 extracted from IBES modules of Pre-tax Profit |
| 1067 | `pv20_opr_indicator_8_feature0` | MATRIX | 0.6331 | 1 | 1 | Feature 0 from Indicator 8 in IBES Pre-tax Profit module |
| 1068 | `pv20_opr_indicator_8_feature1` | MATRIX | 0.5921 | 0 | 0 | Feature 1 from Indicator 8 in IBES Pre-tax Profit module |
| 1069 | `pv20_opr_indicator_8_feature10` | MATRIX | 0.62 | 0 | 0 | Indicator 8, Feature 10 from IBES Pre-tax Profit heuristics |
| 1070 | `pv20_opr_indicator_8_feature12` | MATRIX | 0.6329 | 0 | 0 | Feature 12 from Indicator 8 in IBES Pre-tax Profit module |
| 1071 | `pv20_opr_indicator_8_feature3` | MATRIX | 0.4105 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit predictive feature: Indicator 8, Feature 3, targeting Quarter 3 (n |
| 1072 | `pv20_opr_indicator_8_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator 8 in IBES Pre-tax Profit module |
| 1073 | `pv20_opr_indicator_9_feature0` | MATRIX | 0.6264 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [mean_flash] |
| 1074 | `pv20_opr_indicator_9_feature1` | MATRIX | 0.5617 | 0 | 0 | Feature 1 from Indicator 9 module |
| 1075 | `pv20_opr_indicator_9_feature10` | MATRIX | 0.5901 | 0 | 0 | Indicator 9, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1076 | `pv20_opr_indicator_9_feature11` | MATRIX | 0.5901 | 0 | 0 | Indicator 9, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1077 | `pv20_opr_indicator_9_feature12` | MATRIX | 0.6264 | 0 | 0 | Feature 12 from Indicator 9 in IBES Pre-tax Profit module |
| 1078 | `pv20_opr_indicator_9_feature2` | MATRIX | 0.5901 | 0 | 0 | Feature 2 from Indicator 9 in IBES module of Pre-tax Profit |
| 1079 | `pv20_opr_indicator_9_feature4` | MATRIX | 0.3832 | 0 | 0 | Indicator 9, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 1080 | `pv20_opr_indicator_9_feature7` | MATRIX | 0.5617 | 0 | 0 | Indicator 9, Feature 7 from IBES Pre-tax Profit heuristics |
| 1081 | `pv20_opr_indicator_n_feature0` | MATRIX | 0.5969 | 0 | 0 | Mean of flash (preliminary) IBES pre-tax profit estimates for Quarter 5 |
| 1082 | `pv20_opr_indicator_n_feature11` | MATRIX | 0.5527 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 1083 | `pv20_opr_indicator_n_feature2` | MATRIX | 0.5527 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [median 4 weeks ago] |
| 1084 | `pv20_opr_indicator_n_feature3` | MATRIX | 0.3363 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit predictive feature: Indicator N, Feature 3, targeting Quarter 5 (n |
| 1085 | `pv20_opr_indicator_n_feature4` | MATRIX | 0.3363 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit predictive feature: Indicator N, Feature 4, targeting Quarter 5 (n |
| 1086 | `pv20_opr_indicator_n_feature9` | MATRIX | 0.5969 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 1087 | `pv20_opr_indicator_o_feature0` | MATRIX | 0.559 | 0 | 0 | IBES Pre-tax Profit predictive feature: Indicator O, Feature 0, targeting Quarter 6, computed as the mean of f |
| 1088 | `pv20_opr_indicator_o_feature1` | MATRIX | 0.4913 | 0 | 0 | Median IBES pre-tax profit estimate for Quarter 6, snapshot 3 months ago |
| 1089 | `pv20_opr_indicator_o_feature10` | MATRIX | 0.5186 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1090 | `pv20_opr_indicator_o_feature11` | MATRIX | 0.5186 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1091 | `pv20_opr_indicator_o_feature12` | MATRIX | 0.5589 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1092 | `pv20_opr_indicator_o_feature2` | MATRIX | 0.5186 | 0 | 0 | IBES Pre-tax Profit predictive feature: Indicator O, Feature 2, targeting Quarter 6, computed as the median of |
| 1093 | `pv20_opr_indicator_o_feature7` | MATRIX | 0.4913 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit predictive feature: Indicator O, Feature 7, targeting Quarter 6 (n |
| 1094 | `pv20_opr_indicator_o_feature8` | MATRIX | 1 | 3 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1095 | `pv20_opr_indicator_o_feature9` | MATRIX | 0.559 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1096 | `pv20_opr_indicator_p_feature0` | MATRIX | 0.5323 | 0 | 0 | Mean of flash (preliminary) IBES pre-tax profit estimates for Quarter 7 |
| 1097 | `pv20_opr_indicator_p_feature1` | MATRIX | 0.4343 | 0 | 0 | IBES Pre-tax Profit predictive feature: Indicator P, Feature 1, targeting Quarter 7, computed as the median of |
| 1098 | `pv20_opr_indicator_p_feature11` | MATRIX | 0.484 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1099 | `pv20_opr_indicator_p_feature12` | MATRIX | 0.5322 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1100 | `pv20_opr_indicator_p_feature2` | MATRIX | 0.484 | 0 | 0 | IBES Pre-tax Profit predictive feature: Indicator P, Feature 2, targeting Quarter 7, computed as the median of |
| 1101 | `pv20_opr_indicator_p_feature7` | MATRIX | 0.4343 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1102 | `pv20_opr_indicator_p_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1103 | `pv20_opr_indicator_p_feature9` | MATRIX | 0.5323 | 0 | 0 | Heuristically extracted IBES Pre-tax Profit predictive feature: Indicator P, Feature 9, targeting Quarter 7 (n |
| 1104 | `pv20_opr_indicator_q_feature0` | MATRIX | 0.4989 | 0 | 0 | Mean of flash (preliminary) IBES pre-tax profit estimates for Quarter 8 |
| 1105 | `pv20_opr_indicator_q_feature1` | MATRIX | 0.3009 | 0 | 0 | IBES Pre-tax Profit predictive feature: Indicator Q, Feature 1, targeting Quarter 8, computed as the median of |
| 1106 | `pv20_opr_indicator_q_feature11` | MATRIX | 0.3862 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1107 | `pv20_opr_indicator_q_feature2` | MATRIX | 0.3862 | 0 | 0 | IBES Pre-tax Profit predictive feature: Indicator Q, Feature 2, targeting Quarter 8, computed as the median of |
| 1108 | `pv20_opr_indicator_q_feature7` | MATRIX | 0.3009 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1109 | `pv20_opr_indicator_q_feature8` | MATRIX | 1 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1110 | `pv20_opr_indicator_q_feature9` | MATRIX | 0.4989 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1111 | `pv20_pre_indicator_1_feature0` | MATRIX | 0.9598 | 14 | 4 | Indicator 1, Feature 0 from IBES Pre-tax Profit heuristics |
| 1112 | `pv20_pre_indicator_1_feature1` | MATRIX | 0.9429 | 2 | 2 | Indicator 1, Feature 1 extracted heuristically from IBES Pre-tax Profit modules |
| 1113 | `pv20_pre_indicator_1_feature10` | MATRIX | 0.9527 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1114 | `pv20_pre_indicator_1_feature11` | MATRIX | 0.9527 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1115 | `pv20_pre_indicator_1_feature12` | MATRIX | 0.9598 | 2 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 1, Feature 12 – Fiscal Year 1; non-trivial |
| 1116 | `pv20_pre_indicator_1_feature2` | MATRIX | 0.9527 | 0 | 0 | Indicator 1, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1117 | `pv20_pre_indicator_1_feature3` | MATRIX | 0.8962 | 0 | 0 | Feature 3 from Indicator 1 in IBES Pre-tax Profit module |
| 1118 | `pv20_pre_indicator_1_feature4` | MATRIX | 0.8962 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1119 | `pv20_pre_indicator_1_feature5` | MATRIX | 0.8962 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 1, Feature 5 – Fiscal Year 1; non-trivial |
| 1120 | `pv20_pre_indicator_1_feature6` | MATRIX | 0.8982 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1121 | `pv20_pre_indicator_1_feature7` | MATRIX | 0.9429 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1122 | `pv20_pre_indicator_1_feature8` | MATRIX | 1 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 1, Feature 8 – Fiscal Year 1; non-trivial |
| 1123 | `pv20_pre_indicator_1_feature9` | MATRIX | 0.9598 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 1] [Non-trivial feature] |
| 1124 | `pv20_pre_indicator_2_feature0` | MATRIX | 0.9604 | 1 | 1 | Indicator 2, Feature 0 from IBES Pre-tax Profit heuristics |
| 1125 | `pv20_pre_indicator_2_feature1` | MATRIX | 0.9399 | 0 | 0 | Feature 1 from Indicator 2 in IBES Pre-tax Profit module |
| 1126 | `pv20_pre_indicator_2_feature10` | MATRIX | 0.9509 | 0 | 0 | Indicator 2, Feature 10 from IBES Pre-tax Profit heuristics |
| 1127 | `pv20_pre_indicator_2_feature11` | MATRIX | 0.9509 | 0 | 0 | Indicator 2, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1128 | `pv20_pre_indicator_2_feature12` | MATRIX | 0.9604 | 1 | 1 | Feature 12 from Indicator 2 in IBES Pre-tax Profit module |
| 1129 | `pv20_pre_indicator_2_feature2` | MATRIX | 0.9509 | 0 | 0 | Feature 2 from Indicator 2 in IBES Pre-tax Profit module |
| 1130 | `pv20_pre_indicator_2_feature3` | MATRIX | 0.8921 | 2 | 2 | Indicator 2, Feature 3 extracted heuristically from IBES Pre-tax Profit modules |
| 1131 | `pv20_pre_indicator_2_feature4` | MATRIX | 0.8921 | 0 | 0 | Indicator 2, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 1132 | `pv20_pre_indicator_2_feature5` | MATRIX | 0.8921 | 3 | 3 | Indicator 2, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1133 | `pv20_pre_indicator_2_feature6` | MATRIX | 0.8937 | 0 | 0 | Feature 6 from Indicator 2 in IBES Pre-tax Profit module |
| 1134 | `pv20_pre_indicator_2_feature7` | MATRIX | 0.9399 | 0 | 0 | Indicator 2, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 1135 | `pv20_pre_indicator_2_feature8` | MATRIX | 1 | 0 | 0 | Indicator 2, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1136 | `pv20_pre_indicator_2_feature9` | MATRIX | 0.9604 | 5 | 5 | Indicator 2, Feature 9 extracted heuristically from IBES Pre-tax Profit modules |
| 1137 | `pv20_pre_indicator_3_feature0` | MATRIX | 0.9492 | 0 | 0 | Indicator 3, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1138 | `pv20_pre_indicator_3_feature1` | MATRIX | 0.8972 | 0 | 0 | Indicator 3, Feature 1 from IBES Pre-tax Profit heuristics |
| 1139 | `pv20_pre_indicator_3_feature10` | MATRIX | 0.9171 | 1 | 1 | Indicator 3, Feature 10 from IBES Pre-tax Profit heuristics |
| 1140 | `pv20_pre_indicator_3_feature11` | MATRIX | 0.9171 | 0 | 0 | Indicator 3, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1141 | `pv20_pre_indicator_3_feature12` | MATRIX | 0.9492 | 0 | 0 | Indicator 3, Feature 12 from IBES Pre-tax Profit heuristics |
| 1142 | `pv20_pre_indicator_3_feature2` | MATRIX | 0.9171 | 0 | 0 | Indicator 3, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1143 | `pv20_pre_indicator_3_feature3` | MATRIX | 0.7909 | 1 | 1 | Feature 3 from Indicator 3 in IBES Pre-tax Profit module |
| 1144 | `pv20_pre_indicator_3_feature4` | MATRIX | 0.7909 | 0 | 0 | Feature 4 from Indicator 3 in IBES Pre-tax Profit module |
| 1145 | `pv20_pre_indicator_3_feature5` | MATRIX | 0.7909 | 0 | 0 | Indicator 3, Feature 5 from IBES Pre-tax Profit heuristics |
| 1146 | `pv20_pre_indicator_3_feature6` | MATRIX | 0.7933 | 0 | 0 | Indicator 3, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 1147 | `pv20_pre_indicator_3_feature7` | MATRIX | 0.8972 | 1 | 1 | Feature 7 from Indicator 3 in IBES Pre-tax Profit module |
| 1148 | `pv20_pre_indicator_3_feature8` | MATRIX | 1 | 0 | 0 | Indicator 3, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1149 | `pv20_pre_indicator_3_feature9` | MATRIX | 0.9492 | 0 | 0 | Feature 9 from Indicator 3 in IBES Pre-tax Profit module |
| 1150 | `pv20_pre_indicator_4_feature0` | MATRIX | 0.7801 | 0 | 0 | US predictive IBES Pre-tax Profit: heuristically extracted Indicator 4 Feature 0 for Fiscal Year 4 (mean of fl |
| 1151 | `pv20_pre_indicator_4_feature1` | MATRIX | 0.621 | 0 | 0 | US predictive IBES Pre-tax Profit: heuristically extracted Indicator 4 Feature 1 for Fiscal Year 4 (median con |
| 1152 | `pv20_pre_indicator_4_feature10` | MATRIX | 0.6587 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1153 | `pv20_pre_indicator_4_feature11` | MATRIX | 0.6587 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1154 | `pv20_pre_indicator_4_feature12` | MATRIX | 0.7801 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1155 | `pv20_pre_indicator_4_feature2` | MATRIX | 0.6587 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [median 4 weeks ago] |
| 1156 | `pv20_pre_indicator_4_feature3` | MATRIX | 0.3699 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1157 | `pv20_pre_indicator_4_feature4` | MATRIX | 0.3699 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1158 | `pv20_pre_indicator_4_feature5` | MATRIX | 0.3699 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 4, Feature 5 – Fiscal Year 4; non-trivial |
| 1159 | `pv20_pre_indicator_4_feature6` | MATRIX | 0.374 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1160 | `pv20_pre_indicator_4_feature7` | MATRIX | 0.621 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1161 | `pv20_pre_indicator_4_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1162 | `pv20_pre_indicator_4_feature9` | MATRIX | 0.7801 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 4, Feature 9 – Fiscal Year 4; non-trivial |
| 1163 | `pv20_pre_indicator_6_feature10` | MATRIX | 0.9225 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1164 | `pv20_pre_indicator_6_feature11` | MATRIX | 0.9225 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1165 | `pv20_pre_indicator_6_feature12` | MATRIX | 0.9286 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1166 | `pv20_pre_indicator_6_feature2` | MATRIX | 0.9225 | 0 | 0 | Heuristic feature from IBES Pre-tax Profit for Quarter 1 horizon; median estimate as of 4 weeks ago |
| 1167 | `pv20_pre_indicator_6_feature4` | MATRIX | 0.8343 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1168 | `pv20_pre_indicator_6_feature5` | MATRIX | 0.8343 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 6, Feature 5 – Quarter 1; non-trivial |
| 1169 | `pv20_pre_indicator_6_feature6` | MATRIX | 0.8396 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1170 | `pv20_pre_indicator_6_feature7` | MATRIX | 0.9092 | 26 | 13 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1171 | `pv20_pre_indicator_6_feature8` | MATRIX | 1 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1172 | `pv20_pre_indicator_6_feature9` | MATRIX | 0.9287 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 1] [Non-trivial feature] |
| 1173 | `pv20_pre_indicator_7_feature0` | MATRIX | 0.927 | 1 | 1 | US predictive IBES Pre-tax Profit: heuristically extracted Indicator 7 Feature 0 for Quarter 2 (mean of flash  |
| 1174 | `pv20_pre_indicator_7_feature1` | MATRIX | 0.9042 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [median 3 months ago] |
| 1175 | `pv20_pre_indicator_7_feature11` | MATRIX | 0.9193 | 3 | 3 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1176 | `pv20_pre_indicator_7_feature3` | MATRIX | 0.8249 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1177 | `pv20_pre_indicator_7_feature4` | MATRIX | 0.8249 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1178 | `pv20_pre_indicator_8_feature0` | MATRIX | 0.9238 | 0 | 0 | US predictive IBES Pre-tax Profit: heuristically extracted Indicator 8 Feature 0 for Quarter 3 (mean of flash  |
| 1179 | `pv20_pre_indicator_8_feature10` | MATRIX | 0.915 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1180 | `pv20_pre_indicator_8_feature11` | MATRIX | 0.915 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1181 | `pv20_pre_indicator_8_feature12` | MATRIX | 0.9237 | 1 | 1 | Feature 12 from Indicator 8 in the IBES Pre-tax Profit module |
| 1182 | `pv20_pre_indicator_8_feature2` | MATRIX | 0.915 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 8, Feature 2 – Quarter 3; median 4 weeks ago |
| 1183 | `pv20_pre_indicator_8_feature3` | MATRIX | 0.8089 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1184 | `pv20_pre_indicator_8_feature5` | MATRIX | 0.8089 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1185 | `pv20_pre_indicator_8_feature6` | MATRIX | 0.816 | 2 | 2 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 8, Feature 6 – Quarter 3; non-trivial |
| 1186 | `pv20_pre_indicator_8_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1187 | `pv20_pre_indicator_9_feature0` | MATRIX | 0.921 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 9, Feature 0 – Quarter 4; mean_flash |
| 1188 | `pv20_pre_indicator_9_feature1` | MATRIX | 0.8827 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator 9, Feature 1 – Quarter 4; median 3 months ago |
| 1189 | `pv20_pre_indicator_9_feature10` | MATRIX | 0.9047 | 1 | 1 | Indicator 9, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1190 | `pv20_pre_indicator_9_feature11` | MATRIX | 0.9047 | 0 | 0 | Indicator 9, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1191 | `pv20_pre_indicator_9_feature2` | MATRIX | 0.9047 | 0 | 0 | Feature 2 from Indicator 9 in the IBES module of Pre-tax Profit |
| 1192 | `pv20_pre_indicator_9_feature3` | MATRIX | 0.7757 | 0 | 0 | Feature 3 from Indicator 9 in the IBES Pre-tax Profit module |
| 1193 | `pv20_pre_indicator_9_feature6` | MATRIX | 0.7808 | 1 | 1 | Indicator 9, Feature 6 from IBES Pre-tax Profit heuristics |
| 1194 | `pv20_pre_indicator_9_feature7` | MATRIX | 0.8827 | 1 | 1 | Indicator 9, Feature 7 from IBES Pre-tax Profit heuristics |
| 1195 | `pv20_pre_indicator_9_feature8` | MATRIX | 1 | 0 | 0 | Indicator 9, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1196 | `pv20_pre_indicator_9_feature9` | MATRIX | 0.921 | 1 | 1 | Feature 9 from Indicator 9 in the IBES Pre-tax Profit module |
| 1197 | `pv20_pre_indicator_n_feature1` | MATRIX | 0.8629 | 0 | 0 | Feature 1 from Indicator N in the IBES module of Pre-tax Profit |
| 1198 | `pv20_pre_indicator_n_feature10` | MATRIX | 0.8843 | 0 | 0 | Heuristically extracted Feature 10 from Indicator N in the IBES Pre-tax Profit SAL module, Fiscal Year 2, non- |
| 1199 | `pv20_pre_indicator_n_feature2` | MATRIX | 0.8843 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator N, Feature 2 – Quarter 5; median 4 weeks ago |
| 1200 | `pv20_pre_indicator_n_feature5` | MATRIX | 0.7358 | 1 | 1 | Heuristically extracted Feature 5 from Indicator N in the IBES Pre-tax Profit SAL module, Quarter 1, non-trivi |
| 1201 | `pv20_pre_indicator_n_feature7` | MATRIX | 0.8629 | 11 | 4 | Feature 7 of Indicator N in the IBES Pre-tax Profit module |
| 1202 | `pv20_pre_indicator_n_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator N in the IBES module of Pre-tax Profit |
| 1203 | `pv20_pre_indicator_o_feature10` | MATRIX | 0.8638 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1204 | `pv20_pre_indicator_o_feature11` | MATRIX | 0.8638 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1205 | `pv20_pre_indicator_o_feature12` | MATRIX | 0.8885 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator O, Feature 12 – Quarter 6; non-trivial |
| 1206 | `pv20_pre_indicator_o_feature2` | MATRIX | 0.8638 | 0 | 0 | US predictive IBES Pre-tax Profit: heuristically extracted Indicator O Feature 2 for Quarter 6 (median consens |
| 1207 | `pv20_pre_indicator_o_feature3` | MATRIX | 0.6674 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1208 | `pv20_pre_indicator_o_feature4` | MATRIX | 0.6674 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1209 | `pv20_pre_indicator_o_feature5` | MATRIX | 0.6674 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator O, Feature 5 – Quarter 6; non-trivial |
| 1210 | `pv20_pre_indicator_o_feature6` | MATRIX | 0.6748 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator O, Feature 6 – Quarter 6; non-trivial |
| 1211 | `pv20_pre_indicator_o_feature7` | MATRIX | 0.8342 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1212 | `pv20_pre_indicator_o_feature8` | MATRIX | 1 | 0 | 0 | IBES Pre-tax Profit predictive feature (heuristic): Indicator O, Feature 8 – Quarter 6; non-trivial |
| 1213 | `pv20_pre_indicator_p_feature0` | MATRIX | 0.8719 | 0 | 0 | US predictive IBES Pre-tax Profit: heuristically extracted Indicator P Feature 0 for Quarter 7 (mean of flash  |
| 1214 | `pv20_pre_indicator_p_feature1` | MATRIX | 0.7894 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [median 3 months ago] |
| 1215 | `pv20_pre_indicator_p_feature11` | MATRIX | 0.8336 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator P, Feature 11 – Quarter 7; non-trivial |
| 1216 | `pv20_pre_indicator_p_feature12` | MATRIX | 0.8717 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1217 | `pv20_pre_indicator_p_feature2` | MATRIX | 0.8336 | 1 | 1 | Median of IBES pre-tax profit estimates as of 4 weeks ago for Quarter 7 |
| 1218 | `pv20_pre_indicator_p_feature4` | MATRIX | 0.5921 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator P, Feature 4 – Quarter 7; non-trivial |
| 1219 | `pv20_pre_indicator_p_feature5` | MATRIX | 0.5921 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1220 | `pv20_pre_indicator_p_feature6` | MATRIX | 0.6014 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1221 | `pv20_pre_indicator_p_feature7` | MATRIX | 0.7894 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1222 | `pv20_pre_indicator_p_feature9` | MATRIX | 0.8719 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1223 | `pv20_pre_indicator_q_feature10` | MATRIX | 0.7771 | 1 | 1 | IBES Pre-tax Profit predictive feature (heuristic): Indicator Q, Feature 10 – Quarter 8; non-trivial |
| 1224 | `pv20_pre_indicator_q_feature12` | MATRIX | 0.8429 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1225 | `pv20_pre_indicator_q_feature4` | MATRIX | 0.4426 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1226 | `pv20_pre_indicator_q_feature7` | MATRIX | 0.7087 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1227 | `pv20_pre_indicator_q_feature8` | MATRIX | 1 | 0 | 0 | Predictive indicator from the IBES Quarter module (Indicator Q, feature 8): flash mean consensus (mean_flash)  |
| 1228 | `pv20_prob` | MATRIX | 0.8903 | 0 | 0 | Probability score associated with USA Finchcharts Funda data. |
| 1229 | `pv20_prob2` | MATRIX | 0.9843 | 0 | 0 | Secondary probability score for USA Finchcharts SFunda data. |
| 1230 | `pv20_prob3` | MATRIX | 0.9843 | 0 | 0 | Tertiary probability score for USA Finchcharts SFunda data. |
| 1231 | `pv20_prob5` | MATRIX | 0.9843 | 1 | 1 | Fifth probability score for USA Finchcharts SFunda data. |
| 1232 | `pv20_q_1_announcement_dt` | MATRIX | 1 | 0 | 0 | Latest Full Earnings Report Date |
| 1233 | `pv20_q_1_ard_accrued_expenses` | MATRIX | 0.4077 | 6 | 4 | ARD Accrued Expenses |
| 1234 | `pv20_q_1_ard_accts_receivable_trade` | MATRIX | 0.7427 | 0 | 0 | ARD Accounts Receivable - Trade |
| 1235 | `pv20_q_1_ard_allow_for_doubtful_accts` | MATRIX | 0.2953 | 0 | 0 | ARD Allowance For Doubtful Accounts |
| 1236 | `pv20_q_1_ard_common_stock` | MATRIX | 0.9423 | 0 | 0 | ARD Common Stock |
| 1237 | `pv20_q_1_ard_current_portion_of_lt_debt` | MATRIX | 0.3183 | 0 | 0 | ARD Current Portion of Long-Term Debt |
| 1238 | `pv20_q_1_ard_deferred_inc_tax_asset_lt` | MATRIX | 0.357 | 0 | 0 | ARD Deferred Income Tax Asset (Long-Term) |
| 1239 | `pv20_q_1_ard_income_tax_accrued_payable` | MATRIX | 0.2543 | 0 | 0 | ARD Income Taxes Accrued/Payable |
| 1240 | `pv20_q_1_ard_oth_noncurrent_liabilities` | MATRIX | 0.8423 | 0 | 0 | ARD Other Noncurrent Liabilities |
| 1241 | `pv20_q_1_ard_other_current_liabilities` | MATRIX | 0.4477 | 2 | 2 | ARD Other Current Liabilities |
| 1242 | `pv20_q_1_ard_other_intangible_asset` | MATRIX | 0.612 | 0 | 0 | ARD Other Intangible Assets |
| 1243 | `pv20_q_1_ard_other_noncurrent_asset` | MATRIX | 0.7883 | 1 | 1 | ARD Other Noncurrent Assets |
| 1244 | `pv20_q_1_ard_property_plant_equip_net` | MATRIX | 0.8877 | 0 | 0 | ARD Property Plant & Equipment - Net |
| 1245 | `pv20_q_1_ard_tot_liab_and_shareholder_eqy` | MATRIX | 0.9887 | 0 | 0 | ARD Total Liabilities and Shareholders Equity |
| 1246 | `pv20_q_1_ard_tot_liabilities` | MATRIX | 0.954 | 0 | 0 | ARD Total Liabilities |
| 1247 | `pv20_q_1_ard_total_current_liabilities` | MATRIX | 0.835 | 0 | 0 | ARD Total Current Liabilities |
| 1248 | `pv20_q_1_ard_total_shareholders_equity` | MATRIX | 1 | 2 | 2 | ARD Total Shareholders Equity |
| 1249 | `pv20_q_1_ard_treasury_shares_num` | MATRIX | 0.3567 | 1 | 1 | ARD Treasury Shares (Number) |
| 1250 | `pv20_q_1_fundamental_entry_dt` | MATRIX | 1 | 1 | 1 | Fundamental Data Entry Date |
| 1251 | `pv20_q_1_latest_period_end_dt_full_record` | MATRIX | 1 | 0 | 0 | Latest Period End Date from Full Records |
| 1252 | `pv20_q_2_ard_share_out_from_front_cover` | MATRIX | 0.9143 | 0 | 0 | ARD Shares Outstanding From The Front Cover |
| 1253 | `pv20_q_2_ardr_additional_paid_in_capital` | MATRIX | 0.891 | 0 | 0 | ARD Ref Additional Paid In Capital |
| 1254 | `pv20_q_2_ardr_common_stock` | MATRIX | 0.9057 | 1 | 1 | ARD Ref Common Stock |
| 1255 | `pv20_q_2_ardr_deferred_inc_tax_asset_lt` | MATRIX | 0.2643 | 0 | 0 | ARD Ref Deferred Income Tax Asset (LT) |
| 1256 | `pv20_q_2_ardr_furniture_machinery_equip` | MATRIX | 0.4747 | 0 | 0 | ARD Ref Furniture/Machinery/Equipment |
| 1257 | `pv20_q_2_ardr_inventory` | MATRIX | 0.36 | 0 | 0 | ARD Ref Inventories |
| 1258 | `pv20_q_2_ardr_par_value` | MATRIX | 0.8007 | 1 | 1 | ARD Ref Par Value |
| 1259 | `pv20_q_2_ardr_property_plant_equip_net` | MATRIX | 0.5443 | 0 | 0 | ARD Ref Property Plant & Equipment - Net |
| 1260 | `pv20_q_2_ardr_raw_material` | MATRIX | 0.2983 | 0 | 0 | ARD Ref Raw Materials |
| 1261 | `pv20_q_2_ardr_shares_outstanding` | MATRIX | 0.781 | 1 | 1 | ARD Ref Shares Outstanding |
| 1262 | `pv20_q_2_ardr_total_shareholders_equity` | MATRIX | 0.9717 | 0 | 0 | ARD Ref Total Shareholders Equity |
| 1263 | `pv20_q_2_fundamental_entry_dt` | MATRIX | 1 | 2 | 2 | Fundamental Data Entry Date |
| 1264 | `pv20_q_2_latest_period_end_dt_full_record` | MATRIX | 1 | 0 | 0 | Latest Period End Date from Full Records |
| 1265 | `pv20_q_ard_allow_for_doubtful_accts` | MATRIX | 0.2953 | 0 | 0 | ARD Allowance For Doubtful Accounts |
| 1266 | `pv20_q_ard_goodwll` | MATRIX | 0.6713 | 0 | 0 | ARD Goodwill |
| 1267 | `pv20_q_ard_other_current_liabilities` | MATRIX | 0.4477 | 0 | 0 | ARD Other Current Liabilities |
| 1268 | `pv20_q_ard_other_intangible_asset` | MATRIX | 0.612 | 4 | 2 | ARD Other Intangible Assets |
| 1269 | `pv20_q_ard_other_noncurrent_asset` | MATRIX | 0.7883 | 0 | 0 | ARD Other Noncurrent Assets |
| 1270 | `pv20_q_ard_prepaid_exp_and_other` | MATRIX | 0.5077 | 0 | 0 | ARD Prepaid Expenses and Other |
| 1271 | `pv20_q_ardr_common_stock` | MATRIX | 0.9057 | 0 | 0 | ARD Ref Common Stock |
| 1272 | `pv20_q_ardr_inventory` | MATRIX | 0.36 | 0 | 0 | ARD Ref Inventories |
| 1273 | `pv20_q_ardr_par_value` | MATRIX | 0.8007 | 0 | 0 | ARD Ref Par Value |
| 1274 | `pv20_q_ardr_total_shareholders_equity` | MATRIX | 0.9717 | 0 | 0 | ARD Ref Total Shareholders Equity |
| 1275 | `pv20_receivetime_119` | VECTOR | 1 | 0 | 0 | Time when the forecast data was received. |
| 1276 | `pv20_relation` | VECTOR | 0.837 | 0 | 0 | Relationship link between entities in the USA dataset. |
| 1277 | `pv20_relinv_top1000_0_inverted` | VECTOR | 0.3514 | 1 | 1 | Indicates whether the relationship is inverted for the top 1000 securities (set 0). |
| 1278 | `pv20_relinv_top1000_0_related` | VECTOR | 0.3514 | 0 | 0 | Indicates related entities for the top 1000 securities (set 0). |
| 1279 | `pv20_relinv_top1000_1_inverted` | VECTOR | 0.3514 | 2 | 2 | Indicates whether the relationship is inverted for the top 1000 securities (set 1). |
| 1280 | `pv20_relinv_top1000_1_related` | VECTOR | 0.3514 | 1 | 1 | Indicates related entities for the top 1000 securities (set 1). |
| 1281 | `pv20_relinv_top2000_0_inverted` | VECTOR | 0.6798 | 2 | 1 | Indicates whether the relationship is inverted for the top 2000 securities (set 0). |
| 1282 | `pv20_relinv_top2000_0_related` | VECTOR | 0.6798 | 0 | 0 | Indicates related entities for the top 2000 securities (set 0). |
| 1283 | `pv20_relinv_top2000_1_inverted` | VECTOR | 0.6798 | 0 | 0 | Indicates whether the relationship is inverted for the top 2000 securities (set 1). |
| 1284 | `pv20_relinv_top2000_1_related` | VECTOR | 0.6798 | 1 | 1 | Indicates related entities for the top 2000 securities (set 1). |
| 1285 | `pv20_ret` | MATRIX | 0.9843 | 232 | 137 | Returns for USA Finchcharts SFunda data. |
| 1286 | `pv20_returns1` | MATRIX | 0.5 | 27 | 17 | Returns over a 1-day period. |
| 1287 | `pv20_returns10` | MATRIX | 0.5 | 2 | 2 | Embargoed rolling 10-day FX return, vendor-provided and compliant with regime, masking, and embargo rules; rep |
| 1288 | `pv20_returns100` | MATRIX | 0.5 | 3 | 2 | 100-day returns value for the asset |
| 1289 | `pv20_returns100_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 100-day returns value |
| 1290 | `pv20_returns10_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 10-day returns value |
| 1291 | `pv20_returns120` | MATRIX | 0.5 | 1 | 1 | Embargoed rolling return over the past 120 calendar days for the relevant FX rate; vendor-calculated and not t |
| 1292 | `pv20_returns120_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 120-day returns value |
| 1293 | `pv20_returns15` | MATRIX | 0.5 | 0 | 0 | Embargoed rolling return for the currency or currency pair over the past 15 days, calculated according to the  |
| 1294 | `pv20_returns150` | MATRIX | 0.5 | 2 | 2 | 150-day returns value for the asset |
| 1295 | `pv20_returns150_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 150-day returns value |
| 1296 | `pv20_returns15_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 15-day returns value |
| 1297 | `pv20_returns180` | MATRIX | 0.5 | 1 | 1 | Embargoed rolling return over the past 180 days for the currency pair or FX instrument; cumulative or compound |
| 1298 | `pv20_returns180_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 180-day returns value |
| 1299 | `pv20_returns1_t` | MATRIX | 0.5 | 0 | 0 | Total returns over a 1-day period. |
| 1300 | `pv20_returns2` | MATRIX | 0.5 | 13 | 7 | 2-day returns value for the asset |
| 1301 | `pv20_returns20` | MATRIX | 0.5 | 1 | 1 | Precomputed embargoed 20-day rolling return of the FX rate, incorporating regimes and masking; provided as-is  |
| 1302 | `pv20_returns200` | MATRIX | 0.5 | 1 | 1 | 200-day returns value (variant 42) |
| 1303 | `pv20_returns200_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 200-day returns value |
| 1304 | `pv20_returns20_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 20-day returns value |
| 1305 | `pv20_returns25` | MATRIX | 0.5 | 1 | 1 | Embargoed rolling foreign exchange (FX) return over a 25-day period |
| 1306 | `pv20_returns250` | MATRIX | 0.5 | 1 | 1 | 250-day returns value for the asset |
| 1307 | `pv20_returns250_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 250-day returns value |
| 1308 | `pv20_returns252` | MATRIX | 0.5 | 1 | 1 | Embargoed point-in-time rolling return over the prior 252 trading days (approximately one year), computed unde |
| 1309 | `pv20_returns252_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 252-day returns value |
| 1310 | `pv20_returns25_t` | MATRIX | 0.5 | 0 | 0 | Return value corresponding to a 25-day lookback or lag period, type T |
| 1311 | `pv20_returns2_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 2-day returns value |
| 1312 | `pv20_returns3` | MATRIX | 0.5 | 1 | 1 | 3-day returns value for the asset |
| 1313 | `pv20_returns30` | MATRIX | 0.5 | 1 | 1 | 30-day total return; cumulative return over the past 30 trading days (typically computed as log or simple retu |
| 1314 | `pv20_returns300` | MATRIX | 0.5 | 1 | 1 | 300-day returns value for the asset |
| 1315 | `pv20_returns300_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 300-day returns value |
| 1316 | `pv20_returns30_t` | MATRIX | 0.5 | 0 | 0 | Trailing 30-day return percentage |
| 1317 | `pv20_returns3_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 3-day returns value |
| 1318 | `pv20_returns4` | MATRIX | 0.5 | 0 | 0 | 4-day returns value for the asset |
| 1319 | `pv20_returns40` | MATRIX | 0.5 | 0 | 0 | Embargoed vendor-calculated rolling FX return over 40 calendar days, aligned with current regime, masking, and |
| 1320 | `pv20_returns40_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 40-day returns value |
| 1321 | `pv20_returns4_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 4-day returns value |
| 1322 | `pv20_returns5` | MATRIX | 0.5 | 0 | 0 | 5-day returns value (variant 98) |
| 1323 | `pv20_returns50` | MATRIX | 0.5 | 0 | 0 | Embargoed 50-period rolling return in FX rate, expressed as percent change, computed under bbo delay/embargo r |
| 1324 | `pv20_returns500` | MATRIX | 0.5 | 0 | 0 | 500-day returns value for the asset |
| 1325 | `pv20_returns500_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 500-day returns value |
| 1326 | `pv20_returns50_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 50-day returns value |
| 1327 | `pv20_returns5_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 5-day returns value |
| 1328 | `pv20_returns60` | MATRIX | 0.5 | 1 | 1 | Embargoed rolling 60-day FX return provided by the vendor, incorporating embargo, regime, and masking rules; n |
| 1329 | `pv20_returns60_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 60-day returns value |
| 1330 | `pv20_returns70` | MATRIX | 0.5 | 0 | 0 | Embargoed rolling return over the past 70 calendar days for the relevant currency or currency pair, calculated |
| 1331 | `pv20_returns70_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 70-day returns value |
| 1332 | `pv20_returns75` | MATRIX | 0.5 | 0 | 0 | 75-day returns value (variant 100) |
| 1333 | `pv20_returns750` | MATRIX | 0.5 | 3 | 2 | Embargoed rolling return over a 750-day period for the FX instrument, calculated by the vendor and aligned wit |
| 1334 | `pv20_returns750_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 750-day returns value |
| 1335 | `pv20_returns75_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 75-day returns value |
| 1336 | `pv20_returns90` | MATRIX | 0.5 | 0 | 0 | Embargoed rolling foreign exchange (FX) return over the past 90 calendar days, computed in line with regime, m |
| 1337 | `pv20_returns90_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for 90-day returns value |
| 1338 | `pv20_returns_group` | MATRIX | 1 | 1 | 1 | Group classification for USA Ad Astra returns. |
| 1339 | `pv20_returns_t` | MATRIX | 0.5 | 0 | 0 | Timestamp for returns value |
| 1340 | `pv20_revere_group_5_3_sector` | GROUP | 0.9989 | 14 | 5 | Sector classification for USA Revere group 5_3. |
| 1341 | `pv20_revere_hierarchy_min100_corr21_513_v1_sector` | GROUP | 0.6778 | 5 | 4 | No field description |
| 1342 | `pv20_revere_hierarchy_min100_corr21_513_v2_sector` | GROUP | 0.7153 | 9 | 1 | Sector classification for USA Revere hierarchy |
| 1343 | `pv20_revere_hierarchy_min100_corr21_v1_sector` | GROUP | 0.7026 | 18 | 2 | Industry sector identifier/code for each company as-of-date in the USA Revere hierarchy overlay (min100, 21-da |
| 1344 | `pv20_revere_hierarchy_min100_corr21_v2_sector` | GROUP | 0.7557 | 4 | 2 | Sector classification for USA Revere hierarchy |
| 1345 | `pv20_revere_hierarchy_min15_sector` | GROUP | 0.7036 | 8 | 2 | Industry sector identifier/classification for securities within the USA Revere hierarchy (min15 variant), wher |
| 1346 | `pv20_revere_hierarchy_min2_top2000_sector` | GROUP | 0.7036 | 11 | 2 | Industry sector identifier (Revere sector code) for U.S. equities in the USA_revere_hierarchy_min2_top2000 uni |
| 1347 | `pv20_revere_hierarchy_min4_sector` | GROUP | 0.7036 | 13 | 3 | Point-in-time integer code for the Revere sector classification of each USA instrument in the revere_hierarchy |
| 1348 | `pv20_revere_hierarchy_min50_sector` | GROUP | 0.7036 | 5 | 1 | Point-in-time Revere industry sector code (integer) for each U.S. security in the USA_revere_hierarchy_min50 m |
| 1349 | `pv20_revere_hierarchy_min6_sector` | GROUP | 0.7036 | 6 | 2 | Point-in-time Revere sector classification code (integer) for US securities; decode using the module’s sector  |
| 1350 | `pv20_revere_rha2_min30_sector` | GROUP | 0.7041 | 10 | 4 | Sector classification for USA Revere hierarchy |
| 1351 | `pv20_ro_rd` | MATRIX | 0.5 | 1 | 1 | Operating return for the dataset. |
| 1352 | `pv20_sal_indicator_1_feature0` | MATRIX | 0.9674 | 1 | 1 | Indicator 1, Feature 0 from IBES Pre-tax Profit heuristics |
| 1353 | `pv20_sal_indicator_1_feature1` | MATRIX | 0.9525 | 0 | 0 | Indicator 1, Feature 1 extracted heuristically from IBES Pre-tax Profit modules |
| 1354 | `pv20_sal_indicator_1_feature10` | MATRIX | 0.9618 | 0 | 0 | Indicator 1, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1355 | `pv20_sal_indicator_1_feature11` | MATRIX | 0.9618 | 0 | 0 | Indicator 1, Feature 11 from IBES Pre-tax Profit heuristics |
| 1356 | `pv20_sal_indicator_1_feature12` | MATRIX | 0.9525 | 1 | 1 | Feature 12 from Indicator 1 in IBES Pre-tax Profit module |
| 1357 | `pv20_sal_indicator_1_feature2` | MATRIX | 0.9618 | 0 | 0 | Indicator 1, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1358 | `pv20_sal_indicator_1_feature3` | MATRIX | 0.9057 | 0 | 0 | Feature 3 from Indicator 1 in IBES Pre-tax Profit module |
| 1359 | `pv20_sal_indicator_1_feature4` | MATRIX | 0.9057 | 0 | 0 | Feature 4 from Indicator 1 in IBES Pre-tax Profit module |
| 1360 | `pv20_sal_indicator_1_feature5` | MATRIX | 0.9057 | 0 | 0 | Feature 5 from Indicator 1 in IBES Pre-tax Profit module |
| 1361 | `pv20_sal_indicator_1_feature6` | MATRIX | 0.907 | 0 | 0 | Indicator 1, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 1362 | `pv20_sal_indicator_1_feature7` | MATRIX | 0.9525 | 1 | 1 | Feature 7 from Indicator 1 module |
| 1363 | `pv20_sal_indicator_1_feature8` | MATRIX | 1 | 1 | 1 | Indicator 1, Feature 8 from IBES Pre-tax Profit heuristics |
| 1364 | `pv20_sal_indicator_1_feature9` | MATRIX | 0.9674 | 2 | 2 | Feature 9 from Indicator 1 in IBES Pre-tax Profit module |
| 1365 | `pv20_sal_indicator_2_feature0` | MATRIX | 0.968 | 0 | 0 | Indicator 2, Feature 0 from IBES Pre-tax Profit heuristics |
| 1366 | `pv20_sal_indicator_2_feature1` | MATRIX | 0.9494 | 1 | 1 | Feature 1 from Indicator 2 in IBES Pre-tax Profit module |
| 1367 | `pv20_sal_indicator_2_feature10` | MATRIX | 0.9599 | 0 | 0 | Indicator 2, Feature 10 from IBES Pre-tax Profit heuristics |
| 1368 | `pv20_sal_indicator_2_feature11` | MATRIX | 0.9599 | 0 | 0 | Indicator 2, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1369 | `pv20_sal_indicator_2_feature12` | MATRIX | 0.9576 | 1 | 1 | Feature 12 from Indicator 2 in IBES Pre-tax Profit module |
| 1370 | `pv20_sal_indicator_2_feature2` | MATRIX | 0.9599 | 1 | 1 | Feature 2 from Indicator 2 in IBES Pre-tax Profit module |
| 1371 | `pv20_sal_indicator_2_feature3` | MATRIX | 0.9062 | 2 | 2 | Indicator 2, Feature 3 extracted heuristically from IBES Pre-tax Profit modules |
| 1372 | `pv20_sal_indicator_2_feature4` | MATRIX | 0.9062 | 3 | 3 | Indicator 2, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 1373 | `pv20_sal_indicator_2_feature5` | MATRIX | 0.9062 | 1 | 1 | Indicator 2, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1374 | `pv20_sal_indicator_2_feature6` | MATRIX | 0.9078 | 1 | 1 | Feature 6 from Indicator 2 in IBES Pre-tax Profit module |
| 1375 | `pv20_sal_indicator_2_feature7` | MATRIX | 0.9494 | 2 | 2 | Indicator 2, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 1376 | `pv20_sal_indicator_2_feature8` | MATRIX | 1 | 22 | 16 | Indicator 2, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1377 | `pv20_sal_indicator_2_feature9` | MATRIX | 0.968 | 0 | 0 | Indicator 2, Feature 9 extracted heuristically from IBES Pre-tax Profit modules |
| 1378 | `pv20_sal_indicator_3_feature0` | MATRIX | 0.9621 | 1 | 1 | Indicator 3, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1379 | `pv20_sal_indicator_3_feature1` | MATRIX | 0.9204 | 0 | 0 | Indicator 3, Feature 1 from IBES Pre-tax Profit heuristics |
| 1380 | `pv20_sal_indicator_3_feature10` | MATRIX | 0.9374 | 0 | 0 | Indicator 3, Feature 10 from IBES Pre-tax Profit heuristics |
| 1381 | `pv20_sal_indicator_3_feature11` | MATRIX | 0.9374 | 0 | 0 | Indicator 3, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1382 | `pv20_sal_indicator_3_feature12` | MATRIX | 0.9548 | 1 | 1 | Indicator 3, Feature 12 from IBES Pre-tax Profit heuristics |
| 1383 | `pv20_sal_indicator_3_feature2` | MATRIX | 0.9374 | 0 | 0 | Indicator 3, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1384 | `pv20_sal_indicator_3_feature3` | MATRIX | 0.832 | 0 | 0 | Feature 3 from Indicator 3 in IBES Pre-tax Profit module |
| 1385 | `pv20_sal_indicator_3_feature4` | MATRIX | 0.832 | 0 | 0 | Feature 4 from Indicator 3 in IBES Pre-tax Profit module |
| 1386 | `pv20_sal_indicator_3_feature5` | MATRIX | 0.832 | 1 | 1 | Indicator 3, Feature 5 from IBES Pre-tax Profit heuristics |
| 1387 | `pv20_sal_indicator_3_feature6` | MATRIX | 0.8356 | 0 | 0 | Indicator 3, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 1388 | `pv20_sal_indicator_3_feature7` | MATRIX | 0.9204 | 0 | 0 | Feature 7 from Indicator 3 in IBES Pre-tax Profit module |
| 1389 | `pv20_sal_indicator_3_feature8` | MATRIX | 1 | 3 | 3 | Indicator 3, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1390 | `pv20_sal_indicator_3_feature9` | MATRIX | 0.9621 | 0 | 0 | Feature 9 from Indicator 3 in IBES Pre-tax Profit module |
| 1391 | `pv20_sal_indicator_4_feature0` | MATRIX | 0.855 | 0 | 0 | Indicator 4, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1392 | `pv20_sal_indicator_4_feature1` | MATRIX | 0.7289 | 0 | 0 | Feature 1 from Indicator 4 module |
| 1393 | `pv20_sal_indicator_4_feature10` | MATRIX | 0.757 | 0 | 0 | Feature number 10 for indicator 4 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 1394 | `pv20_sal_indicator_4_feature11` | MATRIX | 0.757 | 0 | 0 | Indicator 4, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1395 | `pv20_sal_indicator_4_feature12` | MATRIX | 0.8503 | 0 | 0 | Indicator 4, Feature 12 extracted heuristically from IBES Pre-tax Profit modules |
| 1396 | `pv20_sal_indicator_4_feature2` | MATRIX | 0.757 | 0 | 0 | Indicator 4, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1397 | `pv20_sal_indicator_4_feature3` | MATRIX | 0.4734 | 0 | 0 | Feature 3 from Indicator 4 in IBES Pre-tax Profit module |
| 1398 | `pv20_sal_indicator_4_feature4` | MATRIX | 0.4734 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Fiscal Year 4] [Non-trivial feature] |
| 1399 | `pv20_sal_indicator_4_feature5` | MATRIX | 0.4734 | 0 | 0 | Feature 5 from Indicator 4 in IBES Pre-tax Profit module |
| 1400 | `pv20_sal_indicator_4_feature6` | MATRIX | 0.4813 | 0 | 0 | Feature 6 from Indicator 4 in IBES Pre-tax Profit module |
| 1401 | `pv20_sal_indicator_4_feature7` | MATRIX | 0.7289 | 0 | 0 | Indicator 4, Feature 7 extracted heuristically from IBES Pre-tax Profit modules |
| 1402 | `pv20_sal_indicator_4_feature8` | MATRIX | 1 | 0 | 0 | Feature 8 from Indicator 4 in IBES Pre-tax Profit module |
| 1403 | `pv20_sal_indicator_4_feature9` | MATRIX | 0.855 | 0 | 0 | Feature 9 from Indicator 4 in IBES Pre-tax Profit module |
| 1404 | `pv20_sal_indicator_6_feature10` | MATRIX | 0.9453 | 0 | 0 | Feature number 10 for indicator 6 extracted heuristically from IBES modules of Pre-tax Profit for Fiscal Year  |
| 1405 | `pv20_sal_indicator_6_feature11` | MATRIX | 0.9453 | 0 | 0 | Indicator 6, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1406 | `pv20_sal_indicator_6_feature2` | MATRIX | 0.9453 | 1 | 1 | Feature 2 from Indicator 6 in IBES Pre-tax Profit module |
| 1407 | `pv20_sal_indicator_6_feature4` | MATRIX | 0.8686 | 5 | 5 | Feature 4 from Indicator 6 in IBES Pre-tax Profit module |
| 1408 | `pv20_sal_indicator_6_feature5` | MATRIX | 0.8686 | 0 | 0 | Indicator 6, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1409 | `pv20_sal_indicator_6_feature6` | MATRIX | 0.871 | 2 | 2 | Feature 6 from Indicator 6 in IBES Pre-tax Profit module |
| 1410 | `pv20_sal_indicator_6_feature8` | MATRIX | 1 | 279 | 102 | Indicator 6, Feature 8 extracted heuristically from IBES Pre-tax Profit modules |
| 1411 | `pv20_sal_indicator_7_feature0` | MATRIX | 0.9489 | 0 | 0 | Indicator 7, Feature 0 extracted heuristically from IBES Pre-tax Profit modules |
| 1412 | `pv20_sal_indicator_7_feature1` | MATRIX | 0.9316 | 0 | 0 | Feature 1 from Indicator 7 in IBES Pre-tax Profit module |
| 1413 | `pv20_sal_indicator_7_feature10` | MATRIX | 0.9433 | 1 | 1 | Indicator 7, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1414 | `pv20_sal_indicator_7_feature11` | MATRIX | 0.9433 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1415 | `pv20_sal_indicator_7_feature12` | MATRIX | 0.9308 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1416 | `pv20_sal_indicator_7_feature2` | MATRIX | 0.9433 | 2 | 2 | Indicator 7, Feature 2 extracted heuristically from IBES Pre-tax Profit modules |
| 1417 | `pv20_sal_indicator_7_feature3` | MATRIX | 0.8642 | 2 | 2 | Feature number 3 for indicator 7 extracted heuristically from IBES modules of Pre-tax Profit for Quarter 3 (me |
| 1418 | `pv20_sal_indicator_7_feature5` | MATRIX | 0.8642 | 0 | 0 | Indicator 7, Feature 5 extracted heuristically from IBES Pre-tax Profit modules |
| 1419 | `pv20_sal_indicator_7_feature6` | MATRIX | 0.867 | 1 | 1 | Feature 6 from Indicator 7 in IBES Pre-tax Profit module |
| 1420 | `pv20_sal_indicator_7_feature8` | MATRIX | 1 | 2 | 2 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1421 | `pv20_sal_indicator_7_feature9` | MATRIX | 0.9489 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 2] [Non-trivial feature] |
| 1422 | `pv20_sal_indicator_8_feature1` | MATRIX | 0.9258 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [median 3 months ago] |
| 1423 | `pv20_sal_indicator_8_feature10` | MATRIX | 0.9404 | 0 | 0 | Indicator 8, Feature 10 from IBES Pre-tax Profit heuristics |
| 1424 | `pv20_sal_indicator_8_feature11` | MATRIX | 0.9404 | 0 | 0 | Indicator 8, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1425 | `pv20_sal_indicator_8_feature12` | MATRIX | 0.9309 | 24 | 12 | Feature 12 from Indicator 8 in IBES Pre-tax Profit module |
| 1426 | `pv20_sal_indicator_8_feature2` | MATRIX | 0.9404 | 0 | 0 | Feature number 2 for indicator 8 extracted heuristically from IBES modules of Pre-tax Profit for Quarter 1 |
| 1427 | `pv20_sal_indicator_8_feature3` | MATRIX | 0.8564 | 3 | 3 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1428 | `pv20_sal_indicator_8_feature4` | MATRIX | 0.8564 | 2 | 2 | Indicator 8, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 1429 | `pv20_sal_indicator_8_feature6` | MATRIX | 0.8589 | 0 | 0 | Indicator 8, Feature 6 extracted heuristically from IBES Pre-tax Profit modules |
| 1430 | `pv20_sal_indicator_8_feature7` | MATRIX | 0.9258 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1431 | `pv20_sal_indicator_8_feature9` | MATRIX | 0.948 | 4 | 4 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 3] [Non-trivial feature] |
| 1432 | `pv20_sal_indicator_9_feature10` | MATRIX | 0.9341 | 0 | 0 | Indicator 9, Feature 10 extracted heuristically from IBES Pre-tax Profit modules |
| 1433 | `pv20_sal_indicator_9_feature11` | MATRIX | 0.9341 | 0 | 0 | Indicator 9, Feature 11 extracted heuristically from IBES Pre-tax Profit modules |
| 1434 | `pv20_sal_indicator_9_feature12` | MATRIX | 0.9312 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 1435 | `pv20_sal_indicator_9_feature3` | MATRIX | 0.8354 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 4] [Non-trivial feature] |
| 1436 | `pv20_sal_indicator_9_feature4` | MATRIX | 0.8354 | 0 | 0 | Indicator 9, Feature 4 extracted heuristically from IBES Pre-tax Profit modules |
| 1437 | `pv20_sal_indicator_9_feature6` | MATRIX | 0.8372 | 0 | 0 | Indicator 9, Feature 6 from IBES Pre-tax Profit heuristics |
| 1438 | `pv20_sal_indicator_9_feature7` | MATRIX | 0.9156 | 2 | 2 | Indicator 9, Feature 7 from IBES Pre-tax Profit heuristics |
| 1439 | `pv20_sal_indicator_n_feature0` | MATRIX | 0.9375 | 0 | 0 | Mean of IBES flash (most recent) pre-tax profit estimates for forecast Quarter 5 |
| 1440 | `pv20_sal_indicator_n_feature11` | MATRIX | 0.9181 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 1441 | `pv20_sal_indicator_n_feature3` | MATRIX | 0.8025 | 1 | 1 | Feature 3 of Indicator N in IBES Pre-tax Profit module |
| 1442 | `pv20_sal_indicator_n_feature4` | MATRIX | 0.8025 | 4 | 4 | Feature 4 of Indicator N extracted from IBES modules of Pre-tax Profit |
| 1443 | `pv20_sal_indicator_n_feature5` | MATRIX | 0.8025 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 1444 | `pv20_sal_indicator_n_feature6` | MATRIX | 0.8059 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 5] [Non-trivial feature] |
| 1445 | `pv20_sal_indicator_n_feature7` | MATRIX | 0.8987 | 0 | 0 | Feature 7 of Indicator N in IBES Pre-tax Profit module |
| 1446 | `pv20_sal_indicator_n_feature8` | MATRIX | 1 | 22 | 11 | Feature 8 from Indicator N in IBES module of Pre-tax Profit |
| 1447 | `pv20_sal_indicator_o_feature0` | MATRIX | 0.9241 | 0 | 0 | Indicator O, feature 0 extracted from IBES modules of Pre-tax Profit |
| 1448 | `pv20_sal_indicator_o_feature10` | MATRIX | 0.9035 | 0 | 0 | Feature 10 from Indicator O in IBES module of Pre-tax Profit |
| 1449 | `pv20_sal_indicator_o_feature11` | MATRIX | 0.9035 | 0 | 0 | IBES predictive indicator from module O, feature 11 related to Pre-tax Profit for Fiscal Year 1 |
| 1450 | `pv20_sal_indicator_o_feature12` | MATRIX | 0.9084 | 20 | 5 | Feature 12 from Indicator O in IBES module of Pre-tax Profit |
| 1451 | `pv20_sal_indicator_o_feature2` | MATRIX | 0.9035 | 0 | 0 | Median IBES Pre-tax Profit estimate as of 4 weeks ago for Quarter 6 (feature 2) |
| 1452 | `pv20_sal_indicator_o_feature4` | MATRIX | 0.7579 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 6] [Non-trivial feature] |
| 1453 | `pv20_sal_indicator_o_feature5` | MATRIX | 0.7579 | 0 | 0 | Feature 5 of Indicator O in IBES Pre-tax Profit module |
| 1454 | `pv20_sal_indicator_o_feature6` | MATRIX | 0.7627 | 0 | 0 | Feature 6 of Indicator O in IBES Pre-tax Profit module |
| 1455 | `pv20_sal_indicator_o_feature9` | MATRIX | 0.9241 | 0 | 0 | Feature 9 from Indicator O in IBES module of Pre-tax Profit |
| 1456 | `pv20_sal_indicator_p_feature1` | MATRIX | 0.8438 | 4 | 3 | Feature 1 of Indicator P in IBES Pre-tax Profit module |
| 1457 | `pv20_sal_indicator_p_feature10` | MATRIX | 0.8852 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1458 | `pv20_sal_indicator_p_feature11` | MATRIX | 0.8852 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1459 | `pv20_sal_indicator_p_feature2` | MATRIX | 0.8852 | 1 | 1 | IBES predictive indicator from module P, feature 2 related to Pre-tax Profit for Quarter 6 |
| 1460 | `pv20_sal_indicator_p_feature3` | MATRIX | 0.6888 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1461 | `pv20_sal_indicator_p_feature5` | MATRIX | 0.6888 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1462 | `pv20_sal_indicator_p_feature7` | MATRIX | 0.8438 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1463 | `pv20_sal_indicator_p_feature8` | MATRIX | 1 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1464 | `pv20_sal_indicator_p_feature9` | MATRIX | 0.912 | 1 | 1 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 7] [Non-trivial feature] |
| 1465 | `pv20_sal_indicator_q_feature0` | MATRIX | 0.8982 | 0 | 0 | IBES Pre-tax Profit Quarter 8 mean flash estimate (Indicator Q, feature 0) |
| 1466 | `pv20_sal_indicator_q_feature1` | MATRIX | 0.7862 | 0 | 0 | Median IBES Pre-tax Profit estimate as of 3 months ago for Quarter 8 (feature 1) |
| 1467 | `pv20_sal_indicator_q_feature10` | MATRIX | 0.8358 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1468 | `pv20_sal_indicator_q_feature11` | MATRIX | 0.8358 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1469 | `pv20_sal_indicator_q_feature12` | MATRIX | 0.8859 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1470 | `pv20_sal_indicator_q_feature5` | MATRIX | 0.566 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1471 | `pv20_sal_indicator_q_feature9` | MATRIX | 0.8982 | 0 | 0 | [Features heuristically extracted from ibes modules of Pre-tax Profit] [Quarter 8] [Non-trivial feature] |
| 1472 | `pv20_score` | MATRIX | 0.892 | 48 | 23 | Score for the dataset |
| 1473 | `pv20_sector` | MATRIX | 0.892 | 0 | 0 | Sector Name |
| 1474 | `pv20_sectorsd` | MATRIX | 0.5 | 0 | 0 | Standard deviation of sector returns for USA data. |
| 1475 | `pv20_sectorsdw` | MATRIX | 0.5 | 1 | 1 | Weighted standard deviation of sector returns for USA data. |
| 1476 | `pv20_sectorw` | MATRIX | 0.5 | 0 | 0 | Weighted sector returns for USA data. |
| 1477 | `pv20_tsvol` | MATRIX | 1 | 0 | 0 | Time-series volatility for USA Universe Score data. |
| 1478 | `pv20_usd_fx_conversion` | MATRIX | 0.5 | 0 | 0 | USD-based FX conversion rate for the given currency, i.e., the rate to convert between the base currency and U |
| 1479 | `pv20_vol250` | MATRIX | 1 | 2 | 2 | Volatility over a 250-day period for USA Universe Score data. |
| 1480 | `pv20_vol_252` | MATRIX | 1 | 2 | 2 | Volatility over a 252-day period. |
| 1481 | `pv20_volume_group` | MATRIX | 1 | 6 | 2 | Group classification for USA Ad Astra volume data. |
| 1482 | `pv20_vret` | MATRIX | 0.5 | 12 | 5 | Volatility of returns for USA DmgrJyaoUtop1 data. |
| 1483 | `pv20_weight` | VECTOR | 0.837 | 2 | 2 | Weight assigned to relationships in the USA Re_Llink dataset. |
| 1484 | `realized_volatility_250d` | MATRIX | 1 | 1 | 1 | Realized volatility calculated over the past 250 trading days. |
| 1485 | `returns_clipped_03` | MATRIX | 1 | 7 | 6 | Returns with extreme values clipped at the 0.3 threshold. |
| 1486 | `sal_6_feature0_predictor` | MATRIX | 0.9496 | 13 | 3 | Predictive feature 0 from indicator group 6 in the SAL model. |
| 1487 | `sal_6_feature12_predictor` | MATRIX | 0.9304 | 1 | 1 | Predictive feature 12 from indicator group 6 in the SAL model. |
| 1488 | `sal_6_feature1_predictor` | MATRIX | 0.9341 | 2 | 2 | Predictive feature 1 from indicator group 6 in the SAL model. |
| 1489 | `sal_6_feature3_predictor` | MATRIX | 0.8686 | 0 | 0 | Predictive feature 3 from indicator group 6 in the SAL model. |
| 1490 | `sal_6_feature7_predictor` | MATRIX | 0.9341 | 1 | 1 | Predictive feature 7 from indicator group 6 in the SAL model. |
| 1491 | `sal_6_feature9_predictor` | MATRIX | 0.9496 | 1 | 1 | Predictive feature 9 from indicator group 6 in the SAL model. |
| 1492 | `sal_7_feature4_predictor` | MATRIX | 0.8642 | 0 | 0 | Predictive feature 4 from indicator group 7 in the SAL model. |
| 1493 | `sal_7_feature7_predictor` | MATRIX | 0.9316 | 1 | 1 | Predictive feature 7 from indicator group 7 in the SAL model. |
| 1494 | `sal_8_feature0_predictor` | MATRIX | 0.948 | 3 | 3 | Predictive feature 0 from indicator group 8 in the SAL model. |
| 1495 | `sal_8_feature5_predictor` | MATRIX | 0.8564 | 1 | 1 | Predictive feature 5 from indicator group 8 in the SAL model. |
| 1496 | `sal_8_feature8_predictor` | MATRIX | 1 | 0 | 0 | Predictive feature 8 from indicator group 8 in the SAL model. |
| 1497 | `sal_9_feature0_predictor` | MATRIX | 0.9477 | 2 | 1 | Predictive feature 0 from indicator group 9 in the SAL model. |
| 1498 | `sal_9_feature1_predictor` | MATRIX | 0.9156 | 0 | 0 | Predictive feature 1 from indicator group 9 in the SAL model. |
| 1499 | `sal_9_feature2_predictor` | MATRIX | 0.9341 | 0 | 0 | Predictive feature 2 from indicator group 9 in the SAL model. |
| 1500 | `sal_9_feature5_predictor` | MATRIX | 0.8354 | 0 | 0 | Predictive feature 5 from indicator group 9 in the SAL model. |
| 1501 | `sal_9_feature8_predictor` | MATRIX | 1 | 0 | 0 | Predictive feature 8 from indicator group 9 in the SAL model. |
| 1502 | `sal_9_feature9_predictor` | MATRIX | 0.9477 | 0 | 0 | Predictive feature 9 from indicator group 9 in the SAL model. |
| 1503 | `sal_n_feature10_predictor` | MATRIX | 0.9181 | 0 | 0 | Predictive feature 10 from indicator group N in the SAL model. |
| 1504 | `sal_n_feature12_predictor` | MATRIX | 0.9216 | 0 | 0 | Predictive feature 12 from indicator group N in the SAL model. |
| 1505 | `sal_n_feature1_predictor` | MATRIX | 0.8987 | 0 | 0 | Predictive feature 1 from indicator group N in the SAL model. |
| 1506 | `sal_n_feature2_predictor` | MATRIX | 0.9181 | 0 | 0 | Predictive feature 2 from indicator group N in the SAL model. |
| 1507 | `sal_n_feature9_predictor` | MATRIX | 0.9375 | 0 | 0 | Predictive feature 9 from indicator group N in the SAL model. |
| 1508 | `sal_o_feature1_predictor` | MATRIX | 0.8801 | 0 | 0 | Predictive feature 1 from indicator group O in the SAL model. |
| 1509 | `sal_o_feature3_predictor` | MATRIX | 0.7579 | 0 | 0 | Predictive feature 3 from indicator group O in the SAL model. |
| 1510 | `sal_o_feature7_predictor` | MATRIX | 0.8801 | 0 | 0 | Predictive feature 7 from indicator group O in the SAL model. |
| 1511 | `sal_o_feature8_predictor` | MATRIX | 1 | 1 | 1 | Predictive feature 8 from indicator group O in the SAL model. |
| 1512 | `sal_p_feature0_predictor` | MATRIX | 0.912 | 1 | 1 | Predictive feature 0 from indicator group P in the SAL model. |
| 1513 | `sal_p_feature12_predictor` | MATRIX | 0.8976 | 0 | 0 | Predictive feature 12 from indicator group P in the SAL model. |
| 1514 | `sal_p_feature4_predictor` | MATRIX | 0.6888 | 0 | 0 | Predictive feature 4 from indicator group P in the SAL model. |
| 1515 | `sal_p_feature6_predictor` | MATRIX | 0.6966 | 0 | 0 | Predictive feature 6 from indicator group P in the SAL model. |
| 1516 | `sal_q_feature2_predictor` | MATRIX | 0.8358 | 0 | 0 | Quantitative predictive feature number 2 from the SAL model. |
| 1517 | `sal_q_feature3_predictor` | MATRIX | 0.566 | 0 | 0 | Quantitative predictive feature number 3 from the SAL model. |
| 1518 | `sal_q_feature4_predictor` | MATRIX | 0.566 | 0 | 0 | Quantitative predictive feature number 4 from the SAL model. |
| 1519 | `sal_q_feature6_predictor` | MATRIX | 0.5728 | 1 | 1 | Quantitative predictive feature number 6 from the SAL model. |
| 1520 | `sal_q_feature7_predictor` | MATRIX | 0.7862 | 1 | 1 | Quantitative predictive feature number 7 from the SAL model. |
| 1521 | `sal_q_feature8_predictor` | MATRIX | 1 | 0 | 0 | Quantitative predictive feature number 8 from the SAL model. |
| 1522 | `slippage_estimate_035` | MATRIX | 1 | 4 | 1 | Estimated transaction slippage using method 035. |
| 1523 | `slippage_estimate_055` | MATRIX | 1 | 2 | 2 | Estimated transaction slippage using method 055. |
| 1524 | `specific_return_adv_usd` | MATRIX | 1 | 1 | 1 | Specific return for securities filtered by average daily value in USD. |
| 1525 | `specific_return_crowding_notliquim` | MATRIX | 0.756 | 1 | 1 | Specific return for securities in the NotLiquiM crowding subset. |
| 1526 | `specific_return_crowding_top1000` | MATRIX | 0.3567 | 0 | 0 | Specific return for securities in the top 1000 by crowding metric. |
| 1527 | `specific_return_crowding_top3000_equal_weight` | MATRIX | 1 | 1 | 1 | Specific return for top 3000 assets with equal weighting, crowding adjusted. |
| 1528 | `specific_return_crowding_top500` | MATRIX | 0.1805 | 1 | 1 | Specific return for securities in the top 500 by crowding metric. |
| 1529 | `specific_return_crowding_topsp500` | MATRIX | 0.1982 | 0 | 0 | Specific return for securities in the top S&P 500 by crowding metric. |
| 1530 | `specific_return_gemtr_adv_allfactors_usd` | MATRIX | 0.9628 | 10 | 9 | Specific return using advanced GEMTR methodology with all factors in USD. |
| 1531 | `specific_return_gemtr_equal_allfactors_usd` | MATRIX | 0.9628 | 5 | 4 | Specific return using equal weighting GEMTR methodology with all factors in USD. |
| 1532 | `specific_return_us_notliquim` | MATRIX | 0.7548 | 0 | 0 | Specific return for US securities in the NotLiquiM subset. |
| 1533 | `specific_return_us_top200` | MATRIX | 0.0739 | 0 | 0 | Specific return for US securities in the top 200 subset. |
| 1534 | `specific_return_usd_equal_weight` | MATRIX | 1 | 2 | 2 | Specific return calculated with equal weighting in USD terms. |
| 1535 | `spread35_slippage1_estimate` | MATRIX | 1 | 1 | 1 | Estimated slippage using a spread of 35 basis points and method 1. |
| 1536 | `ss_top500_specific_return` | MATRIX | 0.1802 | 0 | 0 | Specific return for the top 500 assets by single stock measure. |
| 1537 | `subindustry_market_cap_top3000_1_20` | MATRIX | 0.9846 | 0 | 0 | Market capitalization for subindustry within top 3000 assets, range 1 to 20. |
| 1538 | `subindustry_top2000_1_20` | MATRIX | 1 | 0 | 0 | Indicator for membership in the top 20 subindustries by market cap within the top 2000 securities. |
| 1539 | `subindustry_top2000_1_5` | MATRIX | 1 | 0 | 0 | Indicator for membership in the top 5 subindustries by market cap within the top 2000 securities. |
| 1540 | `subindustry_top3000_1_5` | MATRIX | 1 | 1 | 1 | Indicator for membership in the top 5 subindustries by market cap within the top 3000 securities. |
| 1541 | `subindustry_top3000_1_60` | MATRIX | 1 | 0 | 0 | Indicator for membership in the top 60 subindustries by market cap within the top 3000 securities. |
| 1542 | `time_series_volatility` | MATRIX | 1 | 4 | 1 | Volatility calculated using a time series approach. |
| 1543 | `transaction_cost_estimate_alt1` | MATRIX | 1 | 0 | 0 | Alternative estimate of trading cost or slippage for a transaction. |
| 1544 | `uber_beta_dol_60_value` | MATRIX | 1 | 2 | 2 | Beta value calculated over a 60-day window using dollar returns. |
| 1545 | `uber_slippage_estimate` | MATRIX | 1 | 4 | 4 | Estimated transaction cost slippage using the Uber methodology. |
| 1546 | `universe_score_bottom` | MATRIX | 1 | 0 | 0 | Indicator for securities in the bottom segment of the universe score ranking. |
| 1547 | `vix_adjusted_return` | MATRIX | 1 | 2 | 2 | Asset return normalized by volatility index level. |
| 1548 | `volatility_120d` | MATRIX | 1 | 21 | 7 | Annualized volatility calculated over the past 120 trading days. |
| 1549 | `volatility_20d` | MATRIX | 1 | 6 | 3 | Annualized volatility calculated over the past 20 trading days. |
| 1550 | `volatility_40d` | MATRIX | 1 | 3 | 3 | Volatility of the asset calculated over a 40-day window. |
| 1551 | `volatility_60d` | MATRIX | 1 | 1 | 1 | Annualized volatility calculated over the past 60 trading days. |
| 1552 | `vwap_to_open_return` | MATRIX | 0.9998 | 5 | 4 | Return from last volume-weighted average price to open price. |
