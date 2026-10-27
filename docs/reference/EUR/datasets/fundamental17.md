# fundamental17 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental17` |
| 名称 | Direct Fundamental Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 523 |
| 覆盖率 | 0.7054 |
| 平台已有 alpha | 3513 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

The FactSet Fundamental dataset provides comprehensive annual and interim financial statement data, ratios, and per-share metrics for global equities, with coverage starting from 1980 for developed markets and the 1990s for emerging markets. The dataset includes restated data from 2004 onward, ensuring historical accuracy and comparability. Key fields cover balance sheet, income statement, and cash flow items, as well as detailed breakdowns of assets, liabilities, equity, revenues, expenses, and key performance indicators. FactSet’s symbology enables robust cross-referencing with other datasets. This dataset is valuable for quantitative and fundamental analysis, backtesting, and model development, as it allows researchers to track company financial health, valuation, and performance over t

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **523** |
| 类型分布 | MATRIX×523 |
| 平均覆盖率 | **0.705** |
| 覆盖率区间 | 0.39 ~ 0.81 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 354 | 67.7% |
| 低 (0.50–0.70) | 160 | 30.6% |
| 稀疏 (<0.50) | 9 | 1.7% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 468 | 89.5% |
| UNUSABLE | 46 | 8.8% |
| DEAD_STATIC | 9 | 1.7% |

- 已实测字段：**9** 个（2%），best_sharpe 最高 **1.18**，中位 0.40

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 315 | 0.70 | annual_normalized_net_income_common、annual_net_income_available_common、ttm_net_income_per_employee |
| 其他 | 84 | 0.69 | fnd17_ttmsga2rev、fnd17_float、fnd17_mktcap |
| 价量与波动 | 62 | 0.72 | fnd17_ttmrecturn、daily_volume_to_shares_outstanding、fnd17_3_reptoprcexrate |
| 宏观与行业 | 59 | 0.74 | fnd17_2v320_reptoprcexrate、fnd17_2v320_usdtorepexrate、fnd17_10_reptoprcexrate |
| 风险与质量 | 3 | 0.71 | fnd17_beta_up、fnd17_beta_down、fnd17_beta |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `annual_normalized_net_income_common` | MATRIX | 0.750 | 盈利与财务 | 3 | 1.18 | 0.43 | 0.86 | DEAD_STATIC | Normalized net income available to common shareholders for the most recent fiscal year (excludes unusual/one-time items) |
| 2 | `annual_net_income_available_common` | MATRIX | 0.750 | 盈利与财务 | 1 | 1.13 | 0.47 | 0.71 | DEAD_STATIC | Net income available to common shareholders for the most recent fiscal year |
| 3 | `ttm_net_income_per_employee` | MATRIX | 0.681 | 盈利与财务 | 2 | 0.80 | -0.11 | 0.53 | DEAD_STATIC | Net income per employee over the trailing 12 months |
| 4 | `fnd17_8_ttmgrosmgn` | MATRIX | 0.633 | 盈利与财务 | 1 | 0.65 | -0.03 | 0.10 | DEAD_STATIC | Gross margin - trailing 12 months |
| 5 | `fnd17_tcpngmpna` | MATRIX | 0.746 | 盈利与财务 | 1 | 0.40 | -0.44 | 0.26 | DEAD_STATIC | Net Profit Margin % - 1st historical fiscal year |
| 6 | `fnd17_qgrosmgn` | MATRIX | 0.603 | 盈利与财务 | 1 | 0.33 | -0.34 | 0.02 | DEAD_STATIC | Gross Margin - most recent quarter |
| 7 | `fnd17_ttmrecturn` | MATRIX | 0.653 | 价量与波动 | 2 | 0.26 | -0.38 | -0.12 | DEAD_STATIC | Receivables turnover - trailing 12 months |
| 8 | `fnd17_ttmsga2rev` | MATRIX | 0.612 | 其他 | 2 | 0.11 | 0.53 | 0.12 | DEAD_STATIC | SG&A expenses / net sales - trailing 12 month |
| 9 | `fnd17_atachg` | MATRIX | 0.748 | 盈利与财务 | 1 | -0.16 | 1.19 | -0.25 | DEAD_STATIC | Year-over-year percentage change in total assets for the most recent fiscal year |
| 10 | `fnd17_2v320_reptoprcexrate` | MATRIX | 0.808 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base currency exchange rate |
| 11 | `fnd17_2v320_usdtorepexrate` | MATRIX | 0.808 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to USD exchange rate |
| 12 | `current_enterprise_value` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current enterprise value (market capitalization plus net debt) |
| 13 | `daily_volume_to_shares_outstanding` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily trading volume as a percentage of shares outstanding |
| 14 | `fnd17_10_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base currency exchange rate |
| 15 | `fnd17_10_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to USD exchange rate |
| 16 | `fnd17_1_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base/pricing currency exchange rate |
| 17 | `fnd17_1_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to USD |
| 18 | `fnd17_20_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to base currency |
| 19 | `fnd17_20_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency to USD exchange rate |
| 20 | `fnd17_2_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base currency exchange rate |
| 21 | `fnd17_2_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to USD exchange rate |
| 22 | `fnd17_3_reptoprcexrate` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Exchange rate from the company’s reporting currency to the dataset’s base price currency |
| 23 | `fnd17_3_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from USD to reporting currency |
| 24 | `fnd17_4_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to base currency |
| 25 | `fnd17_4_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency to USD exchange rate |
| 26 | `fnd17_5_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base currency exchange rate |
| 27 | `fnd17_5_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency to USD exchange rate |
| 28 | `fnd17_6_reptoprcexrate` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to base/price currency |
| 29 | `fnd17_6_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to USD |
| 30 | `fnd17_7_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from the company’s reporting currency to the dataset’s base/pricing currency |
| 31 | `fnd17_7_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from the reporting currency to USD |
| 32 | `fnd17_8_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base currency exchange rate |
| 33 | `fnd17_8_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency to USD exchange rate |
| 34 | `fnd17_9_reptoprcexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to base currency exchange rate |
| 35 | `fnd17_9_usdtorepexrate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting Currency to USD exchange rate |
| 36 | `fnd17_dvolshsout` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily trading volume as a percentage of shares outstanding |
| 37 | `fnd17_ev_cur` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Enterprise Value (market capitalization plus net debt) |
| 38 | `fnd17_float` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Public float (shares available for trading) |
| 39 | `fnd17_mktcap` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Market capitalization |
| 40 | `fnd17_shsout` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding, current |
| 41 | `fnd17_vol10davg` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume - avg. trading volume for the last ten days |
| 42 | `fnd17_vol1dprc` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume - 1 Day % Change |
| 43 | `market_capitalization_value_5` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Current market capitalization |
| 44 | `pricing_currency_code_4` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base currency |
| 45 | `pricing_currency_code_emi1` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Code for the security’s price currency (base currency for price fields) |
| 46 | `pricing_currency_code_ras1` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base currency |
| 47 | `pricing_currency_code_ras10` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | base currency |
| 48 | `pricing_currency_code_ras2` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base currency |
| 49 | `pricing_currency_code_ras20` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base currency |
| 50 | `pricing_currency_code_ras3` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base currency used for pricing in this dataset |
| 51 | `pricing_currency_code_ras4` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Base currency used for price or market values |
| 52 | `pricing_currency_code_ras5` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base currency |
| 53 | `pricing_currency_code_ras6` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | base currency |
| 54 | `pricing_currency_code_ras8` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | base currency |
| 55 | `pricing_currency_code_ras9` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Base (price) currency |
| 56 | `pricing_currency_code_rasv2ff` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Base/pricing currency code |
| 57 | `public_float_shares` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Free float shares, in millions |
| 58 | `rep_to_pricing_fx_rate_emi1` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to base/pricing currency |
| 59 | `reporting_currency_code_11` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency |
| 60 | `reporting_currency_code_ras1` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company’s reporting currency code |
| 61 | `reporting_currency_code_ras10` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency |
| 62 | `reporting_currency_code_ras2` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency |
| 63 | `reporting_currency_code_ras20` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency of the company's financial statements |
| 64 | `reporting_currency_code_ras3` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency code |
| 65 | `reporting_currency_code_ras4` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company’s financial reporting currency |
| 66 | `reporting_currency_code_ras5` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency |
| 67 | `reporting_currency_code_ras6` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency of the company |
| 68 | `reporting_currency_code_ras8` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency |
| 69 | `reporting_currency_code_ras9` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reporting currency of the company’s financials |
| 70 | `reporting_currency_code_rasv2ff` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Company’s reporting currency code |
| 71 | `reporting_to_pricing_fx_rate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate converting the company’s reporting currency into the base/pricing currency |
| 72 | `reporting_to_pricing_fx_rate_2` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate from reporting currency to the base pricing currency |
| 73 | `shares_outstanding_current` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding – current, in millions |
| 74 | `shares_outstanding_emi1` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Current total shares outstanding |
| 75 | `ten_day_avg_volume` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trading volume over the last 10 days |
| 76 | `usd_to_reporting_currency_fx` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate to convert USD into the company’s reporting currency (USD to reporting) |
| 77 | `usd_to_reporting_fx_rate` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | USD to Reporting Currency exchange rate |
| 78 | `usd_to_reporting_fx_rate_emi1` | MATRIX | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate used to convert USD to reporting currency for this module. |
| 79 | `fnd17_annperiods` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Number of historical periods - Annual |
| 80 | `fnd17_chpctpricewtd` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Week-to-date price percent change |
| 81 | `fnd17_gihn` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-month high price |
| 82 | `fnd17_nlow` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-month low price |
| 83 | `fnd17_nprice` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Closing price or last bid |
| 84 | `fnd17_pr1dayprc` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent change in the stock price for the most recent trading day |
| 85 | `fnd17_pr5dayprc` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent change in the stock price over the last 5 trading days |
| 86 | `twelve_month_high_price` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | 12 month high price |
| 87 | `fnd17_chpctpricemtd` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Month-to-date price percent change |
| 88 | `fnd17_netdebt_a` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt (total debt minus cash and equivalents) for the last fiscal year |
| 89 | `fnd17_tcpkw40rp` | MATRIX | 0.751 | 价量与波动 | 0 | — | — | — | UNTESTED | Four-week price percent change |
| 90 | `annual_common_equity_value` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity (book value) for the most recent fiscal year |
| 91 | `annual_total_assets_value` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets for the most recent fiscal year |
| 92 | `annual_total_liabilities_value` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities for the most recent fiscal year |
| 93 | `annual_total_shareholder_equity` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total shareholders’ equity for the most recent fiscal year |
| 94 | `annual_total_shareholders_equity` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholders' equity - most recent fiscal year |
| 95 | `fnd17_ata` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets - most recent fiscal year |
| 96 | `fnd17_atotce` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity (book value) - most recent fiscal year |
| 97 | `fnd17_lta` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities - most recent fiscal year |
| 98 | `fnd17_shsoutabs` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding on the balance sheet, most recent fiscal year |
| 99 | `annual_book_value_per_share` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value (common equity) per share for the most recent fiscal year |
| 100 | `fnd17_atanbvps` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Tangible book value per share for the most recent fiscal year |
| 101 | `fnd17_spvba` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value of common equity per share for the most recent fiscal year |
| 102 | `fnd17_atotd2ast` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to total assets for the most recent fiscal year |
| 103 | `fnd17_hsca` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Cash and cash equivalents at fiscal year-end |
| 104 | `cash_per_share` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Cash per share for the most recent fiscal year |
| 105 | `fnd17_chpctpriceqtd` | MATRIX | 0.750 | 价量与波动 | 0 | — | — | — | UNTESTED | Quarter-to-date price percent change |
| 106 | `fnd17_sphsca` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Cash per share - most recent fiscal year |
| 107 | `annual_ebit` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes for the most recent fiscal year |
| 108 | `fnd17_aebit` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes for the most recent fiscal year |
| 109 | `annual_ebitda_amount` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA for the most recent fiscal year |
| 110 | `annual_ebitda_value` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation, and amortization for the year. |
| 111 | `annual_revenue_value` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue (total sales) for the most recent fiscal year |
| 112 | `annual_total_revenue` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue for the most recent fiscal year |
| 113 | `fnd17_aebitd` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA for the most recent fiscal year |
| 114 | `fnd17_priceavg50day` | MATRIX | 0.750 | 价量与波动 | 0 | — | — | — | UNTESTED | Average price of the last 50 days |
| 115 | `annual_earnings_before_tax` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes for the most recent fiscal year |
| 116 | `annual_net_income_incl_extraordinary` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income including extraordinary items for the most recent fiscal year |
| 117 | `annual_net_income_to_common` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common for the most recent fiscal year |
| 118 | `annual_normalized_net_income_to_common` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized net income available to common for the most recent fiscal year |
| 119 | `annual_revenue_per_share` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual revenue per share for the most recent fiscal year |
| 120 | `fnd17_abepsxclxo` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share excluding extraordinary items for the most recent fiscal year |
| 121 | `fnd17_aebtnorm` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized earnings before taxes for the most recent fiscal year |
| 122 | `fnd17_aepsinclxo` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share including extraordinary items for the most recent fiscal year |
| 123 | `fnd17_aepsnorm` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | EPS normalized - most recent fiscal year |
| 124 | `fnd17_ani` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income (earnings after taxes) for the most recent fiscal year |
| 125 | `fnd17_aniac` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common shareholders for the most recent fiscal year |
| 126 | `fnd17_aniacinclx` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common including extraordinary items for the most recent fiscal year |
| 127 | `fnd17_aniacnorm` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized net income available to common (excludes unusual/one-time items) for the most recent fiscal year |
| 128 | `fnd17_aniexclxor` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income excluding extraordinary items for the most recent fiscal year |
| 129 | `fnd17_aninorm` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes excluding unusual or one-time items for the most recent fiscal year |
| 130 | `fnd17_arevps` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per share for the most recent fiscal year |
| 131 | `fnd17_qtrperiods` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Number of historical quarterly periods available for the company |
| 132 | `fnd17_roxlcxspea` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share excluding extraordinary items for the most recent fiscal year |
| 133 | `fnd17_shsboutavg` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding Basic - average, most recent fiscal year |
| 134 | `fnd17_shsoutavg` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding - average, most recent fiscal year |
| 135 | `fnd17_tbea` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes for the most recent fiscal year |
| 136 | `net_income_after_tax_2` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes for the most recent fiscal year |
| 137 | `net_income_incl_extra_items` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income including extraordinary items for the period. |
| 138 | `net_income_incl_extraordinary` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income including extraordinary items for the most recent fiscal year |
| 139 | `normalized_ebt` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized earnings before taxes for the most recent fiscal year |
| 140 | `normalized_net_income` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized net income after taxes for the most recent fiscal year (excludes unusual/one-time items) |
| 141 | `fnd17_mvolshsout` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | Monthly trading volume as a percentage of shares outstanding |
| 142 | `fnd17_vol1davg` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume - 1 Day Average |
| 143 | `fnd17_vol3mavg` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume - avg. trading volume for the last 3 months |
| 144 | `one_day_avg_volume` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | Average daily trading volume over the last 91 days. |
| 145 | `fnd17_rtcpkw40rp` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | Four-week price percent change relative to the S&P 500 |
| 146 | `fnd17_aebitd2` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA for the previous fiscal year |
| 147 | `fnd17_cainq` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common shareholders for the most recent quarter |
| 148 | `fnd17_inq` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income (earnings after taxes) for the most recent quarter |
| 149 | `fnd17_qebit` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes for the most recent quarter |
| 150 | `fnd17_tbeq` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes for the most recent quarter |
| 151 | `quarterly_earnings_before_tax_4` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes for the most recent quarter |
| 152 | `quarterly_ebit_value` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT for the most recent quarter |
| 153 | `quarterly_net_income_3` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income (earnings after taxes) for the most recent quarter |
| 154 | `quarterly_net_income_available_common` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common shareholders for the most recent quarter (including adjustments), in reporting currency ( |
| 155 | `quarterly_net_income_to_common` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common for the most recent quarter |
| 156 | `quarterly_net_income_value` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings after taxes for the most recent quarter |
| 157 | `fnd17_fcf1a` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow - most recent fiscal year |
| 158 | `fnd17_rhsfcf1a` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share for the most recent fiscal year |
| 159 | `fnd17_shboutavgq` | MATRIX | 0.748 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding basic, average, most recent quarter |
| 160 | `fnd17_shsoutavgq` | MATRIX | 0.748 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding, average, most recent quarter |
| 161 | `quarterly_avg_shares_outstanding` | MATRIX | 0.748 | 其他 | 0 | — | — | — | UNTESTED | Average shares outstanding for the most recent quarter |
| 162 | `fnd17_tcpkw31rp` | MATRIX | 0.748 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent change in the stock price over the last 13 weeks |
| 163 | `fnd17_oxlcxspebq` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share excluding extraordinary items for the most recent quarter |
| 164 | `fnd17_qepsinclxo` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share including extraordinary items for the most recent quarter |
| 165 | `fnd17_roxlcxspeq` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share excluding extraordinary items for the most recent quarter |
| 166 | `quarterly_basic_eps_excl_extraordinary_2` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share excluding extraordinary items for the most recent quarter |
| 167 | `quarterly_eps_excl_extraordinary_2` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share excluding extraordinary items for the most recent quarter |
| 168 | `quarterly_eps_incl_extraordinary_2` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share including extraordinary items for the most recent quarter |
| 169 | `fnd17_6_anrhsfcfq` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter (not annualized) |
| 170 | `fnd17_6_rhsfcfq` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter (annualized) |
| 171 | `fnd17_ataxpd` | MATRIX | 0.748 | 其他 | 0 | — | — | — | UNTESTED | Income taxes paid in the most recent fiscal year |
| 172 | `fnd17_rhsfcf2a` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share for the fiscal year prior to the most recent (FCF divided by average shares outstanding) |
| 173 | `fnd17_anichg` | MATRIX | 0.747 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percentage change in net income |
| 174 | `fnd17_ghcspea` | MATRIX | 0.747 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percent change in annual earnings per share compared to the previous fiscal year |
| 175 | `annual_price_to_sales_ratio` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio for the most recent fiscal year |
| 176 | `fnd17_apr2rev` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to sales - most recent fiscal year |
| 177 | `fnd17_aptmgnpct` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax margin - 1st historical fiscal year |
| 178 | `fnd17_aebitdmg` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITD Margin - most recent fiscal year |
| 179 | `fnd17_ltq` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities, most recent quarter |
| 180 | `fnd17_qrev` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue for the most recent quarter |
| 181 | `fnd17_qrevps` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue/share - most recent quarter (annualized) |
| 182 | `fnd17_qrevpsna` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue/share - most recent quarter (not annualized) |
| 183 | `fnd17_qtanbvdolr` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Tangible book value in dollars, most recent quarter |
| 184 | `fnd17_qtotce` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity (book value) - most recent quarter |
| 185 | `fnd17_qtotse` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholders' equity - most recent quarter |
| 186 | `fnd17_shsoutbs` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding on the balance sheet, most recent quarter |
| 187 | `interim_net_debt_value` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt (LFI definition) |
| 188 | `net_debt_interim` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt (total debt minus cash and equivalents) for the interim period. |
| 189 | `quarterly_common_equity_value` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity book value for the most recent quarter |
| 190 | `quarterly_revenue_per_share_4` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per share for the most recent quarter |
| 191 | `quarterly_revenue_per_share_nonannualized_2` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per share for the most recent quarter (not annualized) |
| 192 | `quarterly_revenue_value` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue for the most recent quarter |
| 193 | `quarterly_total_assets_2` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets for the most recent quarter |
| 194 | `quarterly_total_assets_3` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets for the most recent quarter |
| 195 | `quarterly_total_liabilities_4` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities for the most recent quarter |
| 196 | `quarterly_total_liabilities_5` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities, most recent quarter |
| 197 | `quarterly_total_revenue_3` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total revenue for the most recent quarter |
| 198 | `quarterly_total_shareholder_equity_3` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total shareholders' equity for the most recent quarter |
| 199 | `quarterly_total_shareholders_equity` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholders’ equity for the most recent quarter |
| 200 | `fnd17_qtanbvps` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Tangible book value per share for the most recent quarter |
| 201 | `fnd17_spvbq` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value (common equity) per share for the most recent quarter |
| 202 | `quarterly_book_value_per_share_4` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value per share (common equity) for the most recent quarter |
| 203 | `quarterly_book_value_per_share_5` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Book value per share for the most recent quarter |
| 204 | `fnd17_3_ev2ebitda_cur` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by ebitda, current |
| 205 | `fnd17_rtcpkw31rp` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative (S&P500) price percent change - 13 week |
| 206 | `quarterly_total_debt_4` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt for the most recent quarter |
| 207 | `fnd17_qtaxpd` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Income taxes paid in the most recent quarter |
| 208 | `fnd17_qtotd2ast` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to total assets for the most recent quarter |
| 209 | `quarterly_debt_to_assets_ratio` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt to Total Assets ratio for the most recent quarter |
| 210 | `quarterly_taxes_paid_3` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Income taxes paid during the most recent quarter |
| 211 | `fnd17_qtotltd` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt (total), most recent quarter |
| 212 | `fnd17_a2netmrgn` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin % - 2nd historical fiscal year |
| 213 | `fnd17_aptmgnpct2` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin - 2nd historical fiscal year |
| 214 | `fnd17_ebitda2ev` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA divided by Enterprise Value, current |
| 215 | `fnd17_tcpngmpoa` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating margin - 1st historical fiscal year |
| 216 | `annual_revenue_change_percent` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percent change in annual revenue |
| 217 | `fnd17_arevchg` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percentage change in revenue |
| 218 | `fnd17_tcpkw62rp` | MATRIX | 0.744 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent change in the stock price over the last 26 weeks |
| 219 | `fnd17_prytdpct` | MATRIX | 0.744 | 价量与波动 | 0 | — | — | — | UNTESTED | Year-to-date price percent change |
| 220 | `fnd17_priceavg150day` | MATRIX | 0.744 | 价量与波动 | 0 | — | — | — | UNTESTED | Average price of the last 150 days |
| 221 | `one_fifty_day_avg_price` | MATRIX | 0.744 | 价量与波动 | 0 | — | — | — | UNTESTED | 150 day average price |
| 222 | `fnd17_cainmtt` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common shareholders over the trailing twelve months |
| 223 | `fnd17_inmtt` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes over the trailing 12 months |
| 224 | `fnd17_lcxspebmtt` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | EPS Basic excluding extraordinary items - trailing 12 months |
| 225 | `fnd17_tbemtt` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes over the trailing 12 months |
| 226 | `fnd17_ttmebit` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT over the trailing 12 months |
| 227 | `fnd17_ttmepsincx` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | EPS including extraordinary items - trailing 12 months |
| 228 | `fnd17_xlcxspemtt` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | EPS excluding extraordinary items - trailing 12 months |
| 229 | `ttm_basic_eps_excl_extraordinary` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Basic EPS excluding extraordinary items over the trailing 12 months |
| 230 | `ttm_earnings_before_tax_value` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes over the trailing 12 months |
| 231 | `ttm_eps_excl_extraordinary` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | EPS excluding extraordinary items over the trailing 12 months |
| 232 | `ttm_net_income` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes over the trailing twelve months |
| 233 | `ttm_net_income_available_to_common` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common over the trailing 12 months |
| 234 | `ttm_net_income_to_common` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common over the trailing 12 months |
| 235 | `ttm_net_income_value` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes over the trailing 12 months |
| 236 | `fnd17_qcash` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Cash and cash equivalents for the most recent quarter |
| 237 | `quarterly_cash_and_equivalents_2` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Cash and cash equivalents for the most recent quarter |
| 238 | `fnd17_ebitda2ev_a` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA to enterprise value using last fiscal year EBITDA and current enterprise value |
| 239 | `fnd17_sphscq` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Cash and equivalents per share for the most recent quarter |
| 240 | `fnd17_ttmdivshr` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share - trailing 12 months |
| 241 | `fnd17_2tcpngmpoa` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin - 2nd historical fiscal year |
| 242 | `fnd17_6_2rhsfcfq` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter, 1 year ago |
| 243 | `fnd17_qpr2rev` | MATRIX | 0.743 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to sales - most recent quarter |
| 244 | `fnd17_tcpngmpnq` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin % - most recent quarter |
| 245 | `fnd17_tcpngmtpq` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax margin - most recent quarter |
| 246 | `quarterly_pretax_margin_percent_4` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit margin for the most recent quarter |
| 247 | `quarterly_price_to_sales_ratio_4` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to revenue per share for the most recent quarter. |
| 248 | `fnd17_qebitd` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA for the most recent quarter |
| 249 | `quarterly_ebitda_value` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA for the most recent quarter |
| 250 | `fnd17_prytdpctr` | MATRIX | 0.742 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative (S&P500) price percent change - Year to Date |
| 251 | `fnd17_rtcpkw62rp` | MATRIX | 0.742 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative (S&P500) price percent change - 26 week |
| 252 | `fnd17_ttmtaxpd` | MATRIX | 0.742 | 其他 | 0 | — | — | — | UNTESTED | Taxes paid over the trailing 12 months; units: millions |
| 253 | `fnd17_ttmrev` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue over the trailing 12 months; units: millions |
| 254 | `fnd17_ttmrevps` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue/share - trailing 12 month |
| 255 | `ttm_revenue_per_share` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per share over the trailing 12 months |
| 256 | `ttm_total_revenue` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total revenue over the trailing 12 months |
| 257 | `ttm_total_revenue_value` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total revenue over the trailing twelve months |
| 258 | `fnd17_6_2anrhsfcfq` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter - 1 (not annualized) |
| 259 | `fnd17_mttbshs` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding basic, average trailing 12 months |
| 260 | `fnd17_mttshs` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding - average trailing 12 month |
| 261 | `fnd17_priceavg200day` | MATRIX | 0.741 | 价量与波动 | 0 | — | — | — | UNTESTED | Average price of the last 200 days |
| 262 | `two_hundred_day_avg_price` | MATRIX | 0.741 | 价量与波动 | 0 | — | — | — | UNTESTED | 200 day average price |
| 263 | `fnd17_rhsfca` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share for the most recent fiscal year (as defined by the dataset; divided by average shares outstanding) |
| 264 | `fnd17_tcpngmpoq` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating margin - most recent quarter |
| 265 | `quarterly_operating_margin_percent_4` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating margin for the most recent quarter (percent) |
| 266 | `annual_debt_to_equity_ratio` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to equity ratio for the most recent fiscal year |
| 267 | `fnd17_2rhsfca` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share for the prior fiscal year (as defined by the dataset; divided by average shares outstanding) |
| 268 | `fnd17_aprice2bk` | MATRIX | 0.741 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-book ratio for the most recent fiscal year |
| 269 | `fnd17_atotd2eq` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to shareholders’ equity for the most recent fiscal year |
| 270 | `fnd17_altd2eq` | MATRIX | 0.740 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term Debt to Equity: long-term debt divided by total shareholders’ equity |
| 271 | `annual_net_income_change_percent` | MATRIX | 0.739 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income change percentage from the quarter one year ago |
| 272 | `fnd17_nichngyr` | MATRIX | 0.739 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in net income for the most recent quarter versus the same quarter a year ago |
| 273 | `fnd17_ngmpnmtt` | MATRIX | 0.739 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin % - trailing 12 month |
| 274 | `fnd17_ngmtpmtt` | MATRIX | 0.739 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax margin over the trailing 12 months |
| 275 | `fnd17_ttmpr2rev` | MATRIX | 0.739 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to sales - trailing 12 month |
| 276 | `fnd17_rygnhcspe` | MATRIX | 0.739 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year percent change in EPS for the most recent quarter compared to the same quarter last year |
| 277 | `fnd17_shsoutbs2` | MATRIX | 0.738 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding on the balance sheet, most recent quarter one year ago |
| 278 | `fnd17_ttmebitd` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA over the trailing 12 months |
| 279 | `quarterly_common_equity_1y_ago` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity (book value) as of the most recent quarter one year ago |
| 280 | `ttm_ebitda_value` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA over the trailing 12 months |
| 281 | `fnd17_ttmebitdps` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITD per share - trailing 12 months |
| 282 | `fnd17_0_fcfq` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow - most recent quarter |
| 283 | `fnd17_fcfq` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow for the most recent quarter |
| 284 | `fnd17_aroepct` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average equity for the most recent fiscal year |
| 285 | `fnd17_spdq` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend - most recent quarter |
| 286 | `fnd17_ttmopmgn` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating margin over the trailing 12 months |
| 287 | `fnd17_atmtt` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets, trailing twelve months |
| 288 | `fnd17_qtachg` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year over year percent change in total assets as of one year ago |
| 289 | `ttm_total_assets_value` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets - trailing 12 months |
| 290 | `fnd17_price2bk` | MATRIX | 0.736 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-book ratio based on the most recent quarter |
| 291 | `fnd17_qtotd2eq` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to shareholder equity ratio for the most recent quarter |
| 292 | `quarterly_debt_to_equity_ratio` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt to Total Equity ratio for the most recent quarter |
| 293 | `quarterly_debt_to_equity_ratio_2` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt to Total Equity ratio for the most recent quarter |
| 294 | `fnd17_qe2dtlq` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt to shareholder equity ratio for the most recent quarter |
| 295 | `fnd17_lcxspebmtp` | MATRIX | 0.736 | 其他 | 0 | — | — | — | UNTESTED | EPS Basic excluding extraordinary items - prior trailing 12 months |
| 296 | `fnd17_ptmepsincx` | MATRIX | 0.736 | 其他 | 0 | — | — | — | UNTESTED | EPS including extraordinary items - prior trailing 12 month |
| 297 | `fnd17_xlcxspemtp` | MATRIX | 0.736 | 其他 | 0 | — | — | — | UNTESTED | EPS excluding extraordinary items - prior trailing 12 month |
| 298 | `fnd17_ttmebitdmg` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITD Margin - trailing 12 month |
| 299 | `fnd17_tcpkw25rp` | MATRIX | 0.736 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent change in the stock price over the last 52 weeks |
| 300 | `fnd17_yragoprc1` | MATRIX | 0.736 | 价量与波动 | 0 | — | — | — | UNTESTED | Price - year ago |
| 301 | `fnd17_revchngyr` | MATRIX | 0.735 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in revenue for the most recent quarter versus the same quarter a year ago |
| 302 | `revenue_change_year_ago_quarter` | MATRIX | 0.735 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in revenue compared to the same quarter last year. |
| 303 | `fnd17_ptmrev` | MATRIX | 0.734 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue for the prior trailing twelve months |
| 304 | `prior_ttm_total_revenue` | MATRIX | 0.734 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total revenue for the prior trailing twelve months |
| 305 | `fnd17_tcpaormtt` | MATRIX | 0.734 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average assets over the trailing 12 months (percentage) |
| 306 | `fnd17_rtcpkw25rp` | MATRIX | 0.734 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative (S&P500) price percent change - 52 week |
| 307 | `fnd17_nichngin` | MATRIX | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in net income versus the prior quarter |
| 308 | `fnd17_ebitda2ev_ttm` | MATRIX | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of EBITDA to enterprise value for the trailing twelve months (current) |
| 309 | `fnd17_epschngin` | MATRIX | 0.733 | 其他 | 0 | — | — | — | UNTESTED | Percent change in EPS from the prior quarter |
| 310 | `fnd17_mtpbshs` | MATRIX | 0.733 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding basic, average prior trailing 12 months |
| 311 | `fnd17_mtpshs` | MATRIX | 0.733 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding, average prior trailing 12 months |
| 312 | `capital_spending_per_share` | MATRIX | 0.731 | 其他 | 0 | — | — | — | UNTESTED | Capital spending per share for the most recent fiscal year |
| 313 | `fnd17_acapspps` | MATRIX | 0.731 | 其他 | 0 | — | — | — | UNTESTED | Capital Spending per share - most recent fiscal year |
| 314 | `fnd17_ngmpnmtp` | MATRIX | 0.731 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin % - prior trailing 12 month |
| 315 | `fnd17_beta_up` | MATRIX | 0.729 | 风险与质量 | 0 | — | — | — | UNTESTED | Upside beta calculated during up-market periods |
| 316 | `fnd17_revchngin` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in revenue versus the immediately preceding quarter |
| 317 | `revenue_change_prior_quarter` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue change percentage for the prior quarter |
| 318 | `fnd17_2qe2dtlq` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt to equity ratio for the most recent quarter one year ago |
| 319 | `fnd17_qtotd2eq2` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to shareholder equity ratio for the most recent quarter, measured one year ago |
| 320 | `quarterly_debt_to_equity_ratio_1y_ago` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt to Total Equity ratio as of the same quarter one year ago |
| 321 | `fnd17_ttmnichg` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing 12-month net income versus the prior TTM |
| 322 | `fnd17_ghcspemtt` | MATRIX | 0.728 | 其他 | 0 | — | — | — | UNTESTED | Percent change in trailing-twelve-month EPS versus the prior trailing-twelve-month period |
| 323 | `fnd17_tcpaorq` | MATRIX | 0.727 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average assets for the most recent quarter (annualized) |
| 324 | `fnd17_revgrpct` | MATRIX | 0.727 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year revenue growth rate (percent) |
| 325 | `fnd17_20_ev2ebitda_cur` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by EBITDA, current-period valuation multiple |
| 326 | `fnd17_ev2ebitda_cur` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by EBITDA, current |
| 327 | `fnd17_ttmroepct` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average equity - trailing 12 month |
| 328 | `fnd17_ttmrevchg` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in revenue, trailing 12 months over trailing 12 months |
| 329 | `ttm_revenue_change_percent` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue change percentage, TTM versus prior TTM |
| 330 | `fnd17_ptmpr2rev` | MATRIX | 0.720 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to sales - prior trailing 12 month |
| 331 | `fnd17_beta_down` | MATRIX | 0.720 | 风险与质量 | 0 | — | — | — | UNTESTED | Downside beta calculated during down-market periods |
| 332 | `fnd17_tcpaormtp` | MATRIX | 0.719 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average assets for the prior trailing twelve months |
| 333 | `fnd17_qroepct` | MATRIX | 0.718 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average equity for the most recent quarter (annualized) |
| 334 | `quarterly_return_on_equity_percent_3` | MATRIX | 0.718 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average equity for the most recent quarter (annualized, percent) |
| 335 | `fnd17_price2bk2` | MATRIX | 0.717 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Book - most recent quarter, 1 year ago |
| 336 | `fnd17_fcfmtt` | MATRIX | 0.716 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow - trailing 12 months |
| 337 | `annual_debt_to_total_capital` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt capital for the most recent fiscal year |
| 338 | `fnd17_debtcap_a` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-capitalization ratio for the last fiscal year |
| 339 | `fnd17_altd2ast` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt to total assets for the most recent fiscal year |
| 340 | `fnd17_altdps` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt per share for the most recent fiscal year |
| 341 | `fnd17_atotd2cap` | MATRIX | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to total capital percentage, most recent fiscal year |
| 342 | `fnd17_altd2cap` | MATRIX | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term Debt to Total Capital: long-term debt divided by total capital (short-term debt + current portion of long-term |
| 343 | `fnd17_aastturn` | MATRIX | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover - most recent fiscal year |
| 344 | `fnd17_ptmroepct` | MATRIX | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average equity for the prior trailing twelve months |
| 345 | `interim_debt_to_capital_ratio` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt capital (LFI definition) |
| 346 | `interim_debt_to_total_capital` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total capital for the most recent interim period. |
| 347 | `fnd17_qltd2ast` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt to total assets for the most recent quarter |
| 348 | `fnd17_spdtlq` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | LT debt/share - most recent quarter |
| 349 | `fnd17_qtotd2cap` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total capital for the most recent quarter |
| 350 | `fnd17_qltd2cap` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt to total capital ratio for the most recent quarter (total capital includes short-term debt, current porti |
| 351 | `fnd17_aniperemp` | MATRIX | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee for the most recent fiscal year |
| 352 | `fnd17_arevperemp` | MATRIX | 0.705 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee - most recent fiscal year |
| 353 | `fnd17_adivshr` | MATRIX | 0.702 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - most recent fiscal year |
| 354 | `fnd17_10_anrhsfcfq` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter (not annualized) |
| 355 | `fnd17_10_rhsfcfq` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter (annualized) |
| 356 | `fnd17_anrhsfcfq` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share for the most recent quarter, not annualized |
| 357 | `fnd17_rhsfcfq` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share for the most recent quarter, annualized |
| 358 | `fnd17_10_2rhsfcfq` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter, 1 year ago |
| 359 | `fnd17_2rhsfcfq` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter, 1 year ago |
| 360 | `fnd17_anrhsfcq` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share for the most recent quarter, not annualized |
| 361 | `fnd17_rhsfcq` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share for the most recent quarter, annualized |
| 362 | `quarterly_cash_flow_per_share_4` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share for the most recent quarter annualized |
| 363 | `fnd17_10_2anrhsfcfq` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter - 1 (not annualized) |
| 364 | `fnd17_2anrhsfcfq` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow per share - most recent quarter - 1 (not annualized) |
| 365 | `fnd17_rhsfcmtt` | MATRIX | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow per share - trailing 12 month |
| 366 | `fnd17_2anrhsfcq` | MATRIX | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow per share - most recent quarter - 1 (not annualized) |
| 367 | `fnd17_ttmastturn` | MATRIX | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover - trailing 12 months |
| 368 | `fnd17_2rhsfcq` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow per share - most recent quarter, 1 year ago |
| 369 | `fnd17_aroa5yavg` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year average return on average assets |
| 370 | `fnd17_margin5yr` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin - 5 year average |
| 371 | `fnd17_ry5ngmtp` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin - 5 year average |
| 372 | `fnd17_aebitd5yr` | MATRIX | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITD Margin - 5 year average |
| 373 | `fnd17_arecvbl` | MATRIX | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Receivables - most recent fiscal year |
| 374 | `fnd17_ry5ngmpo` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin - 5 year average |
| 375 | `fnd17_spfcrpa` | MATRIX | 0.694 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price to Cash Flow per share - most recent fiscal year |
| 376 | `fnd17_rhsfcfmtt` | MATRIX | 0.693 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share over the trailing 12 months |
| 377 | `fnd17_beta` | MATRIX | 0.692 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta |
| 378 | `fnd17_rhsfcmtp` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow per share - prior trailing 12 month |
| 379 | `fnd17_qastturn` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover ratio for the most recent quarter, annualized |
| 380 | `fnd17_qcapspps` | MATRIX | 0.690 | 其他 | 0 | — | — | — | UNTESTED | Capital Spending per share - most recent quarter |
| 381 | `fnd17_revtrendgr` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year revenue growth rate |
| 382 | `revenue_five_year_cagr` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year revenue growth rate |
| 383 | `fnd17_revps5ygr` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year growth rate of revenue per share |
| 384 | `fnd17_aroe5yavg` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year average return on average equity |
| 385 | `fnd17_qniperemp` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income per employee - most recent quarter (annualized) |
| 386 | `fnd17_qrevperemp` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee - most recent quarter (annualized) |
| 387 | `quarterly_net_income_per_employee_4` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee for the most recent quarter (annualized) |
| 388 | `quarterly_net_income_per_employee_value` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee for the most recent quarter annualized |
| 389 | `quarterly_revenue_per_employee_4` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee for the most recent quarter, annualized |
| 390 | `enterprise_value_to_revenue` | MATRIX | 0.684 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current enterprise value to revenue ratio (EV/Revenue) |
| 391 | `fnd17_aroipct` | MATRIX | 0.684 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on investment for the most recent fiscal year |
| 392 | `fnd17_ev2rev_cur` | MATRIX | 0.684 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by revenue, current |
| 393 | `fnd17_asga2rev` | MATRIX | 0.682 | 其他 | 0 | — | — | — | UNTESTED | SG&A expenses / net sales - most recent fiscal year |
| 394 | `fnd17_ttmniperem` | MATRIX | 0.681 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income per employee - trailing 12 months |
| 395 | `fnd17_ttmrevpere` | MATRIX | 0.681 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee - trailing 12 months |
| 396 | `ttm_net_income_per_employee_value` | MATRIX | 0.681 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee over the trailing 12 months |
| 397 | `ttm_revenue_per_employee` | MATRIX | 0.681 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee over the trailing 12 months |
| 398 | `fnd17_pehigh` | MATRIX | 0.681 | 其他 | 0 | — | — | — | UNTESTED | High value of P/E excluding extraordinary items |
| 399 | `fnd17_pelow` | MATRIX | 0.681 | 其他 | 0 | — | — | — | UNTESTED | Low value of P/E excluding extraordinary items |
| 400 | `fnd17_bvtrendgr` | MATRIX | 0.680 | 宏观与行业 | 0 | — | — | — | UNTESTED | Five-year compound annual growth rate of book value per share |
| 401 | `fnd17_apenorm` | MATRIX | 0.679 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized price-to-earnings ratio for the most recent fiscal year |
| 402 | `fnd17_arecturn` | MATRIX | 0.677 | 价量与波动 | 0 | — | — | — | UNTESTED | Receivables turnover - most recent fiscal year |
| 403 | `annual_current_assets_value` | MATRIX | 0.676 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current assets for the most recent fiscal year |
| 404 | `annual_current_liabilities` | MATRIX | 0.676 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities for the most recent fiscal year |
| 405 | `fnd17_acurast` | MATRIX | 0.676 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets for the most recent fiscal year |
| 406 | `fnd17_acurliab` | MATRIX | 0.676 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities - most recent fiscal year |
| 407 | `fnd17_acurratio` | MATRIX | 0.676 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio for the most recent fiscal year (current assets divided by current liabilities) |
| 408 | `fnd17_awcappspr` | MATRIX | 0.676 | 价量与波动 | 0 | — | — | — | UNTESTED | Working capital per share divided by price, most recent fiscal year |
| 409 | `fnd17_qtaxrate` | MATRIX | 0.676 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective tax rate for the most recent quarter |
| 410 | `fnd17_adeprescfz` | MATRIX | 0.675 | 其他 | 0 | — | — | — | UNTESTED | Accumulated depreciation, most recent fiscal year |
| 411 | `fnd17_ttmcapspps` | MATRIX | 0.673 | 其他 | 0 | — | — | — | UNTESTED | Capital Spending per share - trailing 12 months |
| 412 | `fnd17_qcurast` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current assets - most recent quarter |
| 413 | `quarterly_current_assets_4` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current assets for the most recent quarter |
| 414 | `fnd17_qcurliab` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities - most recent quarter |
| 415 | `quarterly_current_liabilities_4` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities for the most recent quarter |
| 416 | `fnd17_qcurratio` | MATRIX | 0.671 | 其他 | 0 | — | — | — | UNTESTED | Current ratio for the most recent quarter |
| 417 | `fnd17_csptrendgr` | MATRIX | 0.671 | 宏观与行业 | 0 | — | — | — | UNTESTED | Five year compound annual growth rate of capital spending |
| 418 | `fnd17_qwcappspr` | MATRIX | 0.671 | 价量与波动 | 0 | — | — | — | UNTESTED | Working capital per share divided by current price for the most recent quarter |
| 419 | `quarterly_working_capital_per_share_to_price_3` | MATRIX | 0.671 | 价量与波动 | 0 | — | — | — | UNTESTED | Working capital per share divided by current price (most recent quarter) |
| 420 | `fnd17_ttmroipct` | MATRIX | 0.671 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on investment - trailing 12 month |
| 421 | `fnd17_qrevstrt` | MATRIX | 0.670 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate for the most recent quarter; 100 minus payout ratio, percent of earnings retained |
| 422 | `fnd17_ataxrate` | MATRIX | 0.668 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective tax rate for the most recent fiscal year |
| 423 | `fnd17_ataxrate2` | MATRIX | 0.664 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective tax rate for the prior fiscal year |
| 424 | `fnd17_qcurratio2` | MATRIX | 0.664 | 其他 | 0 | — | — | — | UNTESTED | Current ratio - most recent quarter, 1 year ago |
| 425 | `fnd17_qroipct` | MATRIX | 0.664 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on investment for the most recent quarter (annualized) |
| 426 | `fnd17_spfcrpq` | MATRIX | 0.663 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price to Cash Flow per share - most recent quarter |
| 427 | `fnd17_ttmtaxrate` | MATRIX | 0.663 | 宏观与行业 | 0 | — | — | — | UNTESTED | Tax rate - trailing 12 month |
| 428 | `fnd17_ttmpehigh` | MATRIX | 0.662 | 其他 | 0 | — | — | — | UNTESTED | P/E excluding extraordinary items high, trailing 12 months |
| 429 | `fnd17_ttmpelow` | MATRIX | 0.662 | 其他 | 0 | — | — | — | UNTESTED | P/E excluding extraordinary items low, trailing 12 months |
| 430 | `fnd17_qpayratio` | MATRIX | 0.661 | 盈利与财务 | 0 | — | — | — | UNTESTED | Payout ratio for the most recent quarter |
| 431 | `fnd17_arevstrt` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate for the most recent fiscal year, defined as 100 minus the payout ratio (percent of earnings retained) |
| 432 | `fnd17_apeexclxor` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio excluding extraordinary items for the most recent fiscal year |
| 433 | `fnd17_spfcrpmtt` | MATRIX | 0.657 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price to Cash Flow per share - trailing 12 month |
| 434 | `fnd17_roxlcniep` | MATRIX | 0.657 | 其他 | 0 | — | — | — | UNTESTED | P/E including extraordinary items, trailing twelve months |
| 435 | `fnd17_ttmrevstrt` | MATRIX | 0.656 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reinvestment rate over the trailing 12 months |
| 436 | `fnd17_peexclxor` | MATRIX | 0.655 | 其他 | 0 | — | — | — | UNTESTED | P/E excluding extraordinary items, trailing twelve months |
| 437 | `fnd17_ttmpayrat` | MATRIX | 0.655 | 盈利与财务 | 0 | — | — | — | UNTESTED | Payout ratio over the trailing 12 months, defined as cash dividends as a percent of earnings |
| 438 | `fnd17_roxlcxebep` | MATRIX | 0.653 | 其他 | 0 | — | — | — | UNTESTED | Basic P/E excluding extraordinary items, trailing twelve months |
| 439 | `fnd17_apayratio` | MATRIX | 0.649 | 盈利与财务 | 0 | — | — | — | UNTESTED | Payout ratio for the most recent fiscal year |
| 440 | `fnd17_acogs` | MATRIX | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Cost of goods sold for the most recent fiscal year |
| 441 | `fnd17_apayratio2` | MATRIX | 0.643 | 盈利与财务 | 0 | — | — | — | UNTESTED | Payout ratio for the prior fiscal year |
| 442 | `fnd17_qrecturn` | MATRIX | 0.643 | 价量与波动 | 0 | — | — | — | UNTESTED | Receivables turnover - most recent quarter (annualized) |
| 443 | `fnd17_spfcrpmtp` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price to Cash Flow per share - prior trailing 12 month |
| 444 | `fnd17_ppeexclxor` | MATRIX | 0.640 | 其他 | 0 | — | — | — | UNTESTED | P/E excluding extraordinary items, prior trailing twelve months |
| 445 | `fnd17_oxlcxebepp` | MATRIX | 0.639 | 其他 | 0 | — | — | — | UNTESTED | Basic P/E excluding extraordinary items, prior trailing twelve months |
| 446 | `fnd17_agrosmgn` | MATRIX | 0.638 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin - 1st historical fiscal year |
| 447 | `fnd17_agrosmgn2` | MATRIX | 0.638 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin - 2nd historical fiscal year |
| 448 | `fnd17_aroi5yravg` | MATRIX | 0.636 | 价量与波动 | 0 | — | — | — | UNTESTED | Five-year average return on investment |
| 449 | `fnd17_ataxrat5yr` | MATRIX | 0.629 | 宏观与行业 | 0 | — | — | — | UNTESTED | Five-year average effective tax rate |
| 450 | `fnd17_adiv5yavg` | MATRIX | 0.618 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share 5-year average |
| 451 | `fnd17_divnq` | MATRIX | 0.612 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend - next quarterly declared |
| 452 | `fnd17_cftrendgr` | MATRIX | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year compound annual growth rate of cash flow |
| 453 | `fnd17_atanbvdolr` | MATRIX | 0.611 | 其他 | 0 | — | — | — | UNTESTED | Tangible book value in dollars, most recent fiscal year |
| 454 | `fnd17_atotse` | MATRIX | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholders' equity - most recent fiscal year |
| 455 | `fnd17_qsga2rev` | MATRIX | 0.611 | 其他 | 0 | — | — | — | UNTESTED | SG&A expenses / net sales - most recent quarter |
| 456 | `fnd17_atotd` | MATRIX | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt - most recent fiscal year |
| 457 | `fnd17_atotltd` | MATRIX | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt (total) - most recent fiscal year |
| 458 | `fnd17_arev` | MATRIX | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total revenue (sales) for the most recent fiscal year |
| 459 | `annual_net_income_excl_extraordinary` | MATRIX | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income excluding extraordinary items for the most recent fiscal year |
| 460 | `fnd17_aniinclxor` | MATRIX | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income including extraordinary items for the most recent fiscal year |
| 461 | `annual_avg_shares_outstanding` | MATRIX | 0.610 | 其他 | 0 | — | — | — | UNTESTED | Average shares outstanding for the most recent fiscal year |
| 462 | `annual_basic_eps_excl_extraordinary` | MATRIX | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share excluding extraordinary items for the most recent fiscal year |
| 463 | `fnd17_atq` | MATRIX | 0.609 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets - most recent quarter |
| 464 | `fnd17_netdebt_i` | MATRIX | 0.609 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt (total debt minus cash and equivalents) for the latest interim period |
| 465 | `quarterly_common_equity_4` | MATRIX | 0.609 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity (book value) for the most recent quarter |
| 466 | `fnd17_qtotd` | MATRIX | 0.608 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt - most recent quarter |
| 467 | `fnd17_aroapct` | MATRIX | 0.608 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on average assets for the most recent fiscal year |
| 468 | `fnd17_divnqpdt` | MATRIX | 0.608 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend - next quarterly pay date |
| 469 | `fnd17_divnqxdt` | MATRIX | 0.608 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend - next quarterly ex-date |
| 470 | `fnd17_histrelpe` | MATRIX | 0.606 | 盈利与财务 | 0 | — | — | — | UNTESTED | Historical relative price-to-earnings ratio |
| 471 | `fnd17_qcogs` | MATRIX | 0.606 | 其他 | 0 | — | — | — | UNTESTED | Cost of goods sold for the most recent quarter |
| 472 | `fnd17_ttmcogs` | MATRIX | 0.605 | 其他 | 0 | — | — | — | UNTESTED | Cost of goods sold over the trailing 12 months |
| 473 | `ttm_earnings_before_tax` | MATRIX | 0.605 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before taxes over the trailing twelve months |
| 474 | `fnd17_gvay5dly` | MATRIX | 0.603 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield - 5 year average |
| 475 | `fnd17_20_ttmgrosmgn` | MATRIX | 0.602 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross margin for the trailing 12 months |
| 476 | `fnd17_ttmgrosmgn` | MATRIX | 0.602 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross margin over the trailing 12 months |
| 477 | `fnd17_qtotce2` | MATRIX | 0.601 | 盈利与财务 | 0 | — | — | — | UNTESTED | Common equity (book value), most recent quarter one year ago |
| 478 | `fnd17_qdebteps` | MATRIX | 0.599 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt service to earnings per share ratio for the most recent quarter |
| 479 | `fnd17_revtrend10` | MATRIX | 0.596 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ten-year revenue growth rate |
| 480 | `fnd17_ttmdebteps` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt Service to EPS - trailing 12 months |
| 481 | `fnd17_gmntrendgr` | MATRIX | 0.591 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Five-year growth rate of gross margin |
| 482 | `fnd17_payout5yr` | MATRIX | 0.588 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Five-year average payout ratio |
| 483 | `fnd17_nigrpct` | MATRIX | 0.588 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Growth rate % - net income |
| 484 | `fnd17_tcprgspe` | MATRIX | 0.588 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Three-year compound annual growth rate of earnings per share |
| 485 | `fnd17_gvary5ep` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Five-year average P/E excluding extraordinary items |
| 486 | `fnd17_pxepedmtt` | MATRIX | 0.587 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation expense from statement of cash flows - trailing 12 months |
| 487 | `fnd17_adebteps` | MATRIX | 0.587 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt service to earnings per share ratio for the most recent fiscal year |
| 488 | `fnd17_adivchg` | MATRIX | 0.587 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year percentage change in annual dividends per share |
| 489 | `fnd17_grosmgn5yr` | MATRIX | 0.586 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Margin - 5 year average |
| 490 | `fnd17_voctniq` | MATRIX | 0.581 | 其他 | 0 | — | — | — | UNUSABLE | Interest coverage ratio for the most recent quarter |
| 491 | `fnd17_debtcap_i` | MATRIX | 0.580 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt-to-capitalization ratio for the latest interim period |
| 492 | `fnd17_aquickrati` | MATRIX | 0.571 | 其他 | 0 | — | — | — | UNUSABLE | Quick ratio for the most recent fiscal year: (cash + short-term investments + accounts receivable) divided by current li |
| 493 | `fnd17_ttmintcov` | MATRIX | 0.563 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest coverage ratio (EBIT divided by interest expense) over the trailing 12 months |
| 494 | `fnd17_qinventory` | MATRIX | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | Inventory for the most recent quarter |
| 495 | `fnd17_qquickrati` | MATRIX | 0.559 | 其他 | 0 | — | — | — | UNUSABLE | Quick ratio for the most recent quarter |
| 496 | `fnd17_apr2tanbk` | MATRIX | 0.559 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price to Tangible Book - most fiscal year |
| 497 | `fnd17_lbvcerq` | MATRIX | 0.558 | 其他 | 0 | — | — | — | UNUSABLE | Receivables - most recent quarter |
| 498 | `quarterly_accounts_receivable` | MATRIX | 0.558 | 其他 | 0 | — | — | — | UNUSABLE | Receivables (accounts receivable) for the most recent quarter |
| 499 | `fnd17_npmtrendgr` | MATRIX | 0.558 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Five-year growth rate of net profit margin |
| 500 | `fnd17_aintcov` | MATRIX | 0.556 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest coverage ratio for the most recent fiscal year, calculated as EBIT divided by interest expense |
| 501 | `fnd17_ptmintcov` | MATRIX | 0.556 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest coverage for the prior trailing 12 months, defined as EBIT divided by interest expense |
| 502 | `fnd17_pr2tanbk` | MATRIX | 0.555 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price to Tangible Book - most recent quarter |
| 503 | `fnd17_adepexp` | MATRIX | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation expense from statement of cash flows - most recent fiscal year |
| 504 | `fnd17_ainvturn` | MATRIX | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inventory turnover - most recent fiscal year |
| 505 | `fnd17_qquickrat2` | MATRIX | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Quick ratio for the most recent quarter one year ago |
| 506 | `fnd17_epstrendgr` | MATRIX | 0.553 | 宏观与行业 | 0 | — | — | — | UNUSABLE | EPS growth rate over the past 5 years |
| 507 | `fnd17_nitrendgr` | MATRIX | 0.553 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Five-year compound annual growth rate of net income |
| 508 | `fnd17_aintexpz` | MATRIX | 0.547 | 其他 | 0 | — | — | — | UNUSABLE | Total interest expense for the most recent fiscal year |
| 509 | `fnd17_spfcfrpmtt` | MATRIX | 0.546 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price to Free Cash Flow per Share - trailing 12 months |
| 510 | `fnd17_dai` | MATRIX | 0.546 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend rate, indicated annual |
| 511 | `fnd17_yield` | MATRIX | 0.546 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend yield - indicated annual dividend divided by closing price |
| 512 | `fnd17_spfcfrpa` | MATRIX | 0.542 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price to Free Cash Flow per Share - most recent fiscal year |
| 513 | `fnd17_divgrpct` | MATRIX | 0.524 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Three-year compound annual growth rate of dividends per share |
| 514 | `fnd17_ttminvturn` | MATRIX | 0.502 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inventory turnover - trailing 12 months |
| 515 | `fnd17_div` | MATRIX | 0.498 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends paid from the statement of cash flows - most recent fiscal year |
| 516 | `fnd17_divtrendgr` | MATRIX | 0.497 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Five-year compound annual growth rate of dividends per share |
| 517 | `fnd17_qinvturn` | MATRIX | 0.493 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inventory turnover - most recent quarter (annualized) |
| 518 | `fnd17_epstrend10` | MATRIX | 0.484 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ten-year compound annual growth rate of earnings per share |
| 519 | `fnd17_pxepedq` | MATRIX | 0.482 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation expense from the statement of cash flows - most recent quarter |
| 520 | `fnd17_ainventory` | MATRIX | 0.451 | 其他 | 0 | — | — | — | UNUSABLE | Inventory - most recent fiscal year |
| 521 | `fnd17_divtrend10` | MATRIX | 0.435 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ten-year compound annual growth rate of dividends per share |
| 522 | `fnd17_ttmintexp` | MATRIX | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | Interest expense over the trailing 12 months |
| 523 | `fnd17_zpxetniq` | MATRIX | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | Total interest expense for the most recent quarter |

## 六、本地回测证据

- 本地累计回测 **14** 条；其中 `ra_failed_checks` 为空的 **2** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `N1aeg3pp` | 1.18 | 0.80 | 0.43 | 0.78 | 0.01 | 0 | 251 | `rank(divide(ts_backfill(annual_normalized_net_income_common,252),ts_backfill(fnd17_ata,252` |
| `QPbYaMlK` | 1.13 | 0.75 | 0.47 | 0.71 | 0.01 | 0 | 252 | `rank(divide(ts_backfill(annual_net_income_available_common,252),ts_backfill(fnd17_ata,252)` |
| `2rwjaWK5` | 0.80 | 0.42 | -0.30 | 0.53 | 0.01 | ["LOW_SHARPE | 251 | `group_rank(ts_backfill(ttm_net_income_per_employee,252),subindustry)` |
| `rKOdJ0Oa` | 0.65 | 0.27 | -0.03 | 0.10 | 0.01 | ["LOW_SHARPE | 251 | `group_rank(subtract(ts_backfill(fnd17_8_ttmgrosmgn,252),ts_backfill(fnd17_ttmsga2rev,252))` |
| `88jvaGR7` | 0.58 | 0.23 | 0.08 | 0.86 | 0.01 | ["LOW_SHARPE | 251 | `rank(divide(subtract(ts_backfill(annual_normalized_net_income_common,252),ts_backfill(fnd1` |
| `rKOdJ0ea` | 0.40 | 0.13 | -0.44 | 0.26 | 0.01 | ["LOW_SHARPE | 251 | `group_rank(subtract(ts_backfill(fnd17_tcpngmpna,252),ts_backfill(fnd17_a2netmrgn,252)),ind` |
| `78NoaG6Z` | 0.33 | 0.09 | -0.34 | 0.02 | 0.02 | ["LOW_SHARPE | 251 | `group_rank(subtract(ts_backfill(fnd17_qgrosmgn,252),ts_backfill(fnd17_agrosmgn,252)),subin` |
| `GrbgMQgo` | 0.32 | 0.09 | -0.11 | 0.20 | 0.02 | ["LOW_SHARPE | 251 | `group_rank(ts_delta(ts_backfill(ttm_net_income_per_employee,252),252),subindustry)` |
| `88jvaYzq` | 0.26 | 0.07 | -1.07 | -0.18 | 0.01 | ["LOW_SHARPE | 251 | `group_rank(ts_backfill(fnd17_ttmrecturn,252),industry)` |
| `QPbY2WYp` | 0.20 | 0.04 | -0.38 | -0.12 | 0.02 | ["LOW_SHARPE | 251 | `group_rank(ts_delta(ts_backfill(fnd17_ttmrecturn,252),252),industry)` |
| `vRrOe6Lb` | 0.11 | 0.02 | 0.53 | 0.12 | 0.01 | ["LOW_SHARPE | 251 | `reverse(group_rank(ts_backfill(fnd17_ttmsga2rev,252),industry))` |
| `KPNmXVg8` | -0.16 | -0.03 | 1.19 | -0.25 | 0.01 | ["LOW_SHARPE | 251 | `reverse(group_rank(ts_mean(ts_backfill(fnd17_atachg,252),66),subindustry))` |
| `npdAZ6va` | -0.21 | -0.05 | 0.02 | -0.21 | 0.02 | ["LOW_SHARPE | 251 | `reverse(group_rank(ts_delta(ts_backfill(fnd17_ttmsga2rev,252),252),industry))` |
| `6XjAw7Y7` | -0.50 | -0.17 | -0.64 | 0.07 | 0.01 | ["LOW_SHARPE | 252 | `rank(divide(subtract(ts_backfill(annual_normalized_net_income_common,252),ts_backfill(annu` |

## 七、判死记录（sealed dead_end）

- `EUR-W251-FUNDAMENTAL17-QUALITY-PROBE`（2026-09-24）family=fundamental17 operating-quality changes and matched levels：{"dataset": "fundamental17", "wave": 251, "delay": 1, "universe": "TOPCS1600", "settings": "SUBINDUSTRY decay4 truncation.08", "scope": "12 exact expressions in selection_w251 only; not entire dataset", "best_alpha": "N1aeg3pp", "best_sharpe": 1.18, "same_alpha_fitness": 0.8, "two_year_sharpe": 0.43, "reason": "No candidate reaches joint Sharpe>=1.25 and Fitness>=.8; slow turnover 1.00%-2.11%; lev
- `EUR-W252-FUNDAMENTAL17-MEASUREMENT-RETEST`（2026-09-24）family=fundamental17 reported earnings level and accounting adjustment：{"dataset": "fundamental17", "wave": 252, "delay": 1, "universe": "TOPCS1600", "scope": "2 exact selection_w252 expressions and current settings only", "evidence": [{"alpha_id": "QPbYaMlK", "role": "reported_income_level", "sharpe": 1.13, "fitness": 0.75, "two_year_sharpe": 0.47, "rn_sharpe": 0.52, "turnover": 0.0112, "sub_sharpe": 0.71, "robust_sharpe": 0.9, "units_warning": false, "failed_ra": [

