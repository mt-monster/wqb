# KOR RISK / INSIDERS 字段画像与实测台账（2026-11-07）

数据来源：本轮 MCP 实读 `get_datasets(region=KOR,delay=1,universe=TOP600)` 全量 185 集 + `get_datafields` 逐集字段。

## 0. 重要工具坑：get_datasets 的 category 过滤与 theme 缺省

- `get_datasets(category="RISK")` / `category="risk"` 一律返回 `count=0`，即使加 `theme="true"` 也一样。
- 可行做法：**不传 category 拉全量（KOR/TOP600/D1 = 185 集），本地按返回体的 `category` 字段过滤**。
- KOR 类别分布：other 26 / model 57 / analyst 17 / pv 18 / fundamental 17 / news 24 / risk 7 / sentiment 6 / shortinterest 3 / insiders 2 / macro 2 / institutions 2 / earnings 1 / imbalance 1 / socialmedia 2。

## 1. KOR RISK 类 7 集全览

| dataset | name | fields | alphaCount | userCount | coverage | 状态 |
|---|---|---:|---:|---:|---:|---|
| risk70 | Multi-Factor Model | 96 | 8018 | 1230 | 0.9798 | 已出 1 颗 omERn83n (S1.62) |
| risk88 | Other Multi-Factor Risk Models | 64 | 1418 | 495 | 0.9727 | 本轮 P49 已测 |
| risk68 | Forecast Data | 5 | 770 | 347 | 0.9914 | 本轮 P52 已测 |
| risk59 | Securities Lending & Short Market Dynamics | 16 | 564 | 222 | 0.9806 | 本轮 P50 已测 |
| risk72 | Specific return of extended factors | 5 | 402 | 164 | 0.6246 | 本轮 P52 已测 |
| risk71 | Daily Specific Return Profiling | 7 | 349 | 152 | 0.6658 | 本轮 P52 已测 |
| risk60 | Securities Lending Insight | 5 | 211 | 83 | 1.0 | 本轮 P51 重测（旧判死为语法错） |

## 2. KOR INSIDERS 类 2 集 + 语义相关 3 集

| dataset | name | category | fields | alphaCount | userCount | coverage | 状态 |
|---|---|---|---:|---:|---:|---:|---|
| insiders5 | Corporate Insider Trading Activities | insiders | 53 | 5027 | 820 | 0.8918 | 已出 1 颗 RRE9NkVj (S1.76) |
| insiders1 | Global Insider Trading Data | insiders | 9 | 549 | 202 | 0.3526 | 未测（本轮已画像） |
| model244 | Insider Transaction Analytics | model | 30 | 17 | 11 | 0.4589 | 未测（aC 极低） |
| other83 | Insider Transaction Analytics | model | 15 | 171 | 33 | 0.375 | 未测 |
| model68 | Risk-Alleviated Momentum Scores | model | 4 | 27 | 15 | 0.8499 | 未测 |

## 3. 逐集字段清单

### risk88 — Other Multi-Factor Risk Models (MATRIX, cov0.967-1.0)（53 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `rsk88_mfm_ase1_dsrt` | MATRIX | 0.967 | 297 | 163 |
| `rsk88_mfm_ase1_ind_advertising` | MATRIX | 0.967 | 31 | 21 |
| `rsk88_mfm_ase1_ind_agriculture` | MATRIX | 0.967 | 70 | 23 |
| `rsk88_mfm_ase1_ind_airlines` | MATRIX | 0.967 | 41 | 21 |
| `rsk88_mfm_ase1_ind_banks` | MATRIX | 0.967 | 28 | 11 |
| `rsk88_mfm_ase1_ind_beverages` | MATRIX | 0.967 | 13 | 11 |
| `rsk88_mfm_ase1_ind_biotechnology` | MATRIX | 0.967 | 12 | 10 |
| `rsk88_mfm_ase1_ind_buildingmaterials` | MATRIX | 0.967 | 17 | 10 |
| `rsk88_mfm_ase1_ind_chemicals` | MATRIX | 0.967 | 15 | 13 |
| `rsk88_mfm_ase1_ind_commercialservices` | MATRIX | 0.967 | 9 | 8 |
| `rsk88_mfm_ase1_ind_cosmetics_personalcare` | MATRIX | 0.967 | 9 | 8 |
| `rsk88_mfm_ase1_ind_distribution_wholesale` | MATRIX | 0.967 | 6 | 6 |
| `rsk88_mfm_ase1_ind_diversifiedfinanserv` | MATRIX | 0.967 | 9 | 9 |
| `rsk88_mfm_ase1_ind_electric` | MATRIX | 0.967 | 19 | 16 |
| `rsk88_mfm_ase1_ind_energy_alternatesources` | MATRIX | 0.967 | 4 | 4 |
| `rsk88_mfm_ase1_ind_entertainment` | MATRIX | 0.967 | 16 | 8 |
| `rsk88_mfm_ase1_ind_environmentalcontrol` | MATRIX | 0.967 | 5 | 5 |
| `rsk88_mfm_ase1_ind_food` | MATRIX | 0.967 | 9 | 9 |
| `rsk88_mfm_ase1_ind_gas` | MATRIX | 0.967 | 15 | 9 |
| `rsk88_mfm_ase1_ind_hand_machinetools` | MATRIX | 0.967 | 10 | 9 |
| `rsk88_mfm_ase1_ind_homebuilders` | MATRIX | 0.967 | 15 | 10 |
| `rsk88_mfm_ase1_ind_homefurnishings` | MATRIX | 0.967 | 12 | 7 |
| `rsk88_mfm_ase1_ind_householdproducts_wares` | MATRIX | 0.967 | 3 | 3 |
| `rsk88_mfm_ase1_ind_insurance` | MATRIX | 0.967 | 3 | 3 |
| `rsk88_mfm_ase1_ind_investmentcompanies` | MATRIX | 0.967 | 3 | 2 |
| `rsk88_mfm_ase1_ind_iron_steel` | MATRIX | 0.967 | 8 | 4 |
| `rsk88_mfm_ase1_ind_leisuretime` | MATRIX | 0.967 | 7 | 6 |
| `rsk88_mfm_ase1_ind_lodging` | MATRIX | 0.967 | 14 | 6 |
| `rsk88_mfm_ase1_ind_machinery_diversified` | MATRIX | 0.967 | 13 | 9 |
| `rsk88_mfm_ase1_ind_media` | MATRIX | 0.967 | 7 | 4 |
| `rsk88_mfm_ase1_ind_metalfabricate_hardware` | MATRIX | 0.967 | 12 | 6 |
| `rsk88_mfm_ase1_ind_mining` | MATRIX | 0.967 | 12 | 7 |
| `rsk88_mfm_ase1_ind_miscellaneousmanufactur` | MATRIX | 0.967 | 37 | 14 |
| `rsk88_mfm_ase1_ind_officefurnishings` | MATRIX | 0.967 | 12 | 12 |
| `rsk88_mfm_ase1_ind_pharmaceuticals` | MATRIX | 0.967 | 7 | 5 |
| `rsk88_mfm_ase1_ind_realestate` | MATRIX | 0.967 | 13 | 9 |
| `rsk88_mfm_ase1_ind_retail` | MATRIX | 0.967 | 11 | 8 |
| `rsk88_mfm_ase1_ind_semiconductors` | MATRIX | 0.967 | 12 | 7 |
| `rsk88_mfm_ase1_ind_shipbuilding` | MATRIX | 0.967 | 9 | 6 |
| `rsk88_mfm_ase1_ind_software` | MATRIX | 0.967 | 10 | 10 |
| `rsk88_mfm_ase1_ind_telecommunications` | MATRIX | 0.967 | 15 | 13 |
| `rsk88_mfm_ase1_ind_transportation` | MATRIX | 0.967 | 16 | 10 |
| `rsk88_mfm_ase1_market` | MATRIX | 1 | 12 | 9 |
| `rsk88_mfm_ase1_ri_beta` | MATRIX | 1 | 39 | 26 |
| `rsk88_mfm_ase1_ri_divyield` | MATRIX | 1 | 73 | 53 |
| `rsk88_mfm_ase1_ri_growth` | MATRIX | 1 | 85 | 54 |
| `rsk88_mfm_ase1_ri_leverage` | MATRIX | 1 | 30 | 22 |
| `rsk88_mfm_ase1_ri_momentum` | MATRIX | 1 | 53 | 35 |
| `rsk88_mfm_ase1_ri_nonlsize` | MATRIX | 1 | 34 | 26 |
| `rsk88_mfm_ase1_ri_size` | MATRIX | 1 | 52 | 31 |
| `rsk88_mfm_ase1_ri_value` | MATRIX | 1 | 247 | 121 |
| `rsk88_mfm_ase1_ri_volatility` | MATRIX | 1 | 98 | 67 |
| `rsk88_mfm_ase1_srisk` | MATRIX | 0.967 | 102 | 65 |

### risk71 — Daily Specific Return Profiling (MATRIX, cov0.36-0.91)（6 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `asi_top1000_liquidity_dsrt` | MATRIX | 0.3785 | 8 | 8 |
| `asi_top1500_liquidity_dsrt` | MATRIX | 0.5879 | 21 | 20 |
| `residualized_return_asia_minvol1m` | MATRIX | 0.908 | 37 | 26 |
| `residualized_return_asia_top1100_liquid` | MATRIX | 0.3601 | 5 | 4 |
| `rsk71_eqy_asi_supported_minvol1m_dsrt` | MATRIX | 0.7592 | 158 | 63 |
| `rsk71_eqy_xjpci_supported_minvol1m_dsrt` | MATRIX | 0.7592 | 156 | 59 |

### risk72 — Specific return of extended factors (MATRIX, cov0.35-0.76)（5 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `rsk72_asi_top1000_eqy_dsrt` | MATRIX | 0.3534 | 89 | 33 |
| `rsk72_asi_top1500_eqy_dsrt` | MATRIX | 0.5426 | 82 | 35 |
| `rsk72_asi_top2000_eqy_dsrt` | MATRIX | 0.7085 | 132 | 88 |
| `rsk72_eqy_asi_supported_minvol1m_dsrt` | MATRIX | 0.7592 | 91 | 46 |
| `rsk72_eqy_xjpci_supported_minvol1m_dsrt` | MATRIX | 0.7592 | 92 | 41 |

### risk68 — Forecast Data (MATRIX, cov1.0)（3 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `rsk68_beta` | MATRIX | 1 | 74 | 39 |
| `rsk68_weight_dadv` | MATRIX | 1 | 95 | 54 |
| `rsk68_weight_volatility_short` | MATRIX | 1 | 525 | 265 |

### risk60 — Securities Lending Insight (VECTOR event, cov1.0)（5 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `lending_fee_bid_rate` | VECTOR | 1 | 8 | 6 |
| `rsk60_crowding` | VECTOR | 1 | 57 | 31 |
| `rsk60_datatime` | VECTOR | 1 | 62 | 25 |
| `rsk60_last` | VECTOR | 1 | 89 | 29 |
| `rsk60_offer` | VECTOR | 1 | 55 | 30 |

### risk59 — Securities Lending & Short Market Dynamics (VECTOR, cov0.9806)（16 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `rsk59_bid_rate` | VECTOR | 0.9806 | 56 | 30 |
| `rsk59_crowded_score` | VECTOR | 0.9806 | 18 | 18 |
| `rsk59_daystocover10day` | VECTOR | 0.9806 | 104 | 58 |
| `rsk59_daystocover30day` | VECTOR | 0.9806 | 49 | 28 |
| `rsk59_daystocover90day` | VECTOR | 0.9806 | 35 | 22 |
| `rsk59_dtcdailychg` | VECTOR | 0.9806 | 34 | 24 |
| `rsk59_dtcweeklychg` | VECTOR | 0.9806 | 44 | 22 |
| `rsk59_indicativeavailability` | VECTOR | 0.9806 | 122 | 45 |
| `rsk59_last_rate` | VECTOR | 0.9806 | 14 | 10 |
| `rsk59_offer_rate` | VECTOR | 0.9806 | 28 | 17 |
| `rsk59_s3utilization` | VECTOR | 0.9806 | 67 | 38 |
| `rsk59_short_interest` | VECTOR | 0.9806 | 40 | 25 |
| `rsk59_short_momentum` | VECTOR | 0.9806 | 13 | 9 |
| `rsk59_shortinterestnotional` | VECTOR | 0.9806 | 33 | 16 |
| `rsk59_shortinterestpct` | VECTOR | 0.9806 | 25 | 16 |
| `rsk59_squeeze_risk` | VECTOR | 0.9806 | 58 | 32 |

### model68 — Risk-Alleviated Momentum Scores (VECTOR, cov0.85)（4 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `mdl68_mktcap` | VECTOR | 0.8499 | 1 | 1 |
| `mdl68_ram` | VECTOR | 0.8499 | 6 | 4 |
| `mdl68_raw` | VECTOR | 0.8499 | 2 | 2 |
| `mdl68_score` | VECTOR | 0.8499 | 18 | 10 |

### model244 — Insider Transaction Analytics (VECTOR, cov0.459)（29 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `company_market_value_eur_tw` | VECTOR | 0.459 | 0 | 0 |
| `company_market_value_local_tw` | VECTOR | 0.459 | 0 | 0 |
| `company_market_value_usd_tw` | VECTOR | 0.459 | 0 | 0 |
| `company_total_shares_tw` | VECTOR | 0.459 | 0 | 0 |
| `firm_sentiment_score_tw` | VECTOR | 0.459 | 0 | 0 |
| `highest_trade_unit_price` | VECTOR | 0.4589 | 0 | 0 |
| `highest_trade_unit_price_tw` | VECTOR | 0.459 | 0 | 0 |
| `insider_hierarchy_rank_tw` | VECTOR | 0.459 | 1 | 1 |
| `insider_post_trade_holdings_tw` | VECTOR | 0.459 | 0 | 0 |
| `mdl244_company_sentiment` | VECTOR | 0.4589 | 0 | 0 |
| `mdl244_insider_holdings` | VECTOR | 0.4589 | 1 | 1 |
| `mdl244_insider_level` | VECTOR | 0.4589 | 1 | 1 |
| `mdl244_market_cap` | VECTOR | 0.4589 | 0 | 0 |
| `mdl244_market_cap_usd` | VECTOR | 0.4589 | 1 | 1 |
| `mdl244_revision` | VECTOR | 0.4589 | 3 | 1 |
| `mdl244_share_count` | VECTOR | 0.4589 | 3 | 3 |
| `mdl244_shares_outstanding` | VECTOR | 0.4589 | 0 | 0 |
| `mdl244_timestamp_utc` | VECTOR | 0.4589 | 0 | 0 |
| `mdl244_transaction_significance` | VECTOR | 0.4589 | 1 | 1 |
| `mdl244_transaction_unit_price` | VECTOR | 0.4589 | 0 | 0 |
| `mdl244_transaction_value` | VECTOR | 0.4589 | 2 | 2 |
| `mdl244_transaction_value_eur` | VECTOR | 0.4589 | 0 | 0 |
| `mdl244_transaction_value_usd` | VECTOR | 0.4589 | 3 | 3 |
| `trade_importance_rank_tw` | VECTOR | 0.459 | 0 | 0 |
| `trade_unit_price_tw` | VECTOR | 0.459 | 0 | 0 |
| `trade_value_eur_tw` | VECTOR | 0.459 | 0 | 0 |
| `trade_value_local_currency_tw` | VECTOR | 0.459 | 0 | 0 |
| `trade_value_usd_tw` | VECTOR | 0.459 | 0 | 0 |
| `transaction_share_quantity_tw` | VECTOR | 0.459 | 2 | 2 |

### other83 — Insider Transaction Analytics (VECTOR, cov0.25-0.42)（15 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `oth83_company_sentiment` | VECTOR | 0.2536 | 25 | 6 |
| `oth83_insider_holdings` | VECTOR | 0.4216 | 23 | 7 |
| `oth83_insider_level` | VECTOR | 0.4242 | 19 | 8 |
| `oth83_market_cap` | VECTOR | 0.2813 | 6 | 2 |
| `oth83_market_cap_eur` | VECTOR | 0.281 | 22 | 6 |
| `oth83_market_cap_usd` | VECTOR | 0.281 | 27 | 7 |
| `oth83_revision` | VECTOR | 0.4242 | 10 | 4 |
| `oth83_share_count` | VECTOR | 0.4242 | 49 | 16 |
| `oth83_shares_outstanding` | VECTOR | 0.2881 | 23 | 6 |
| `oth83_timestamp_utc` | VECTOR | 0.4242 | 2 | 2 |
| `oth83_transaction_significance` | VECTOR | 0.4242 | 5 | 2 |
| `oth83_transaction_unit_price` | VECTOR | 0.4242 | 21 | 8 |
| `oth83_transaction_value` | VECTOR | 0.4242 | 39 | 11 |
| `oth83_transaction_value_eur` | VECTOR | 0.4242 | 60 | 12 |
| `oth83_transaction_value_usd` | VECTOR | 0.4242 | 33 | 11 |

### insiders1 — Global Insider Trading Data (VECTOR, cov0.3526)（9 字段）

| field | type | coverage | alphaCount | userCount |
|---|---|---:|---:|---:|
| `insd1_gvkey` | VECTOR | 0.3526 | 178 | 55 |
| `insd1_holdings` | VECTOR | 0.3526 | 57 | 32 |
| `insd1_price` | VECTOR | 0.3526 | 45 | 30 |
| `insd1_shares` | VECTOR | 0.3526 | 112 | 72 |
| `insd1_tradesignificance` | VECTOR | 0.3526 | 40 | 27 |
| `insd1_value` | VECTOR | 0.3526 | 107 | 59 |
| `insd1_valueeur` | VECTOR | 0.3526 | 45 | 34 |
| `max_trade_price` | VECTOR | 0.3526 | 5 | 5 |
| `transaction_currency_code` | VECTOR | 0.3526 | 15 | 10 |
