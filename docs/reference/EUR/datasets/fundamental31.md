# fundamental31 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental31` |
| 名称 | — |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 366 |
| 覆盖率 | 0.8714 |
| 平台已有 alpha | 7146 |
| valueScore | 2 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

（平台目录未返回描述）

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **366** |
| 类型分布 | MATRIX×366 |
| 平均覆盖率 | **0.871** |
| 覆盖率区间 | 0.58 ~ 0.95 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 188 | 51.4% |
| 中 (0.70–0.90) | 170 | 46.4% |
| 低 (0.50–0.70) | 8 | 2.2% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 364 | 99.5% |
| UNUSABLE | 2 | 0.5% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 364 / UNUSABLE 2 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 197 | 0.87 | fnd31_booklev、fnd31_nlassets、fnd31_ed |
| 价量与波动 | 73 | 0.89 | fnd31_nlprice、fnd31_qsg2_additionalfactor_unfiltered_rqi_rd、fnd31_milliq |
| 修正与预期 | 54 | 0.89 | fnd31_stockrating、fnd31_fc_estep、fnd31_mktcappera |
| 其他 | 33 | 0.83 | fnd31_nlmktcap、fnd31_nlsales、fnd31_capexsale |
| 宏观与行业 | 7 | 0.88 | fnd31_qsg2_additionalfactor_unfiltered_irttmsalesev、fnd31_totalsaleg、fnd31_cg3ysales |
| 风险与质量 | 1 | 0.80 | fnd31_o_additionalfactor4_ohlsonscore |
| 搜索与替代数据 | 1 | 0.72 | fnd31_rdsale |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd31_nlmktcap` | MATRIX | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Natural Logarithm of Market Capitalization. It is defined as the natural logarithm of the cubic of a stock's total market value. |
| 2 | `fnd31_nlprice` | MATRIX | 0.948 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural Logarithm of Closing Price. It is defined as the natural logarithm of the cube of a stock's unadjusted closing price. |
| 3 | `fnd31_qsg2_additionalfactor_unfiltered_rqi_rd` | MATRIX | 0.948 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Month Stock Return Interquartile Range. It is defined as the interquartile range of a stock's daily total return over the trailing one mon |
| 4 | `fnd31_milliq` | MATRIX | 0.948 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock Illiquidity. It is defined as the monthly average of the daily absolute return to the daily dollar trading volume ratio. |
| 5 | `fnd31_actrtn1m` | MATRIX | 0.948 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-2 to month t-1. |
| 6 | `fnd31_qsg2_additionalfactor_unfiltered_dtsm1_rd` | MATRIX | 0.948 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Month Realized Stock Return Volatility. It is defined as the standard deviation of a stock's daily total return over the trailing one mont |
| 7 | `fnd31_volto` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading Turnover Ratio. It is defined as the monthly total trading volume divided by the most recently reported total outstanding shares. |
| 8 | `fnd31_actrtn2m` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | 2-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-3 to month t-1. |
| 9 | `fnd31_visiratio` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | The Visibility Ratio. It equals a stock's most recent daily trading volume divided by the average daily trading volume in the previous 50 tr |
| 10 | `fnd31_indrelrtn5d_` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day Industry Relative Return. It is defined as a stock's return in the last 5 days minus the average of the comparable returns of all stoc |
| 11 | `fnd31_indrelrtn4w_` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week Industry Relative Return. It is defined as a stock's return in the last 4 weeks minus the average of the comparable returns of all st |
| 12 | `fnd31_booklev` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book Leverage. It is defined as the most recently reported quarterly total assets divided by the book equity. |
| 13 | `fnd31_nlassets` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural Logarithm of Total Assets. It is defined as the natural logarithm of the most recent quarterly reported total assets. |
| 14 | `fnd31_actrtn3m` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-4 to month t-1. |
| 15 | `fnd31_ed` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term Debt-to-Equity. It is defined as the most recently reported total long-term debt divided by total book equity. |
| 16 | `fnd31_aor` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets. It is defined as the trailing 12-month income before extra items divided by the average of total assets in the same period |
| 17 | `fnd31_astto` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assets Turnover Ratio. It is defined as the trailing 12-month sales divided by the most recently reported quarterly assets. |
| 18 | `fnd31_equityto` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity Turnover Ratio. It is defined as the trailing 12-month sales divided by the average of trailing 12-month reported book equity. |
| 19 | `fnd31_noato` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Operating Asset Turnover. It is defined as trailing-12-month sales divided by the last 4-quarters average net operating assets, which eq |
| 20 | `fnd31_pvan` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Asset Value to Price. It is defined as the most recent book value of net assets per share (NAV) by the closing price. NAV is calculated  |
| 21 | `fnd31_stockrating` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Consensus Rating. It is defined as the consensus recommendation for a company. |
| 22 | `fnd31_cfita` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Cash Flow from Investment to Total Assets. It is defined as the trailing 12-month cash flow from the investing portion of the cash flow  |
| 23 | `fnd31_ocfast` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow to Assets. It is defined as the trailing 12-month net cash flow from operations divided by the average total assets. |
| 24 | `fnd31_past` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Total Assets. It is defined as a stock's trading price divided by the most recent quarterly reported total assets per share. |
| 25 | `fnd31_ttmaccu` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting Accruals. It is defined as the difference between the trailing 12-month net income and the trailing 12-month operating cash flow  |
| 26 | `fnd31_pb` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-Market. It is defined as the most recently reported book value per share for a stock deflated by its trading price. |
| 27 | `fnd31_fc_estep` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-Month Median Earnings Yield. It is defined as the next fiscal year median consensus earnings estimate divided by trading price. |
| 28 | `fnd31_mktcappera` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Market Cap per Analyst. It is defined as a stock's current market cap divided by the number of analysts providing Fiscal Year 1 earnings est |
| 29 | `fnd31_ocfroi` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Oper Cash Flow Return on Invested Capital. It is defined as the trailing 12-month operating cash flow divided by the average invested capita |
| 30 | `fnd31_pedwf_cf` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-Month Mean Earnings Yield. It is defined as the next 4 quarters' mean consensus earnings estimate divided by the price. |
| 31 | `fnd31_fc_numest` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of Analyst Coverage. It is defined as the number of analysts' earnings estimates for fiscal year 1 for a stock. |
| 32 | `fnd31_gspea2y_cf` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-Year Ahead EPS Growth. It is defined as the most recent consensus earnings forecast for fiscal year 2 minus the consensus earnings forecas |
| 33 | `fnd31_yoychgda` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year Change in Leverage. It is defined as the difference between the most recent reported quarterly total liabilities as a percent |
| 34 | `fnd31_cvvolp20d` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-Day Volume Volatility to Price Volatility. It is defined as the coefficient of variation of the last 20 days of closing prices divided by |
| 35 | `fnd31_pe_wt` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield. This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a 12-month forward ea |
| 36 | `fnd31_apemtt` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EPS after Extra Items-to-Price. It is defined as the most recently reported trailing 12-month earnings per share after extraordinary ite |
| 37 | `fnd31_bpemtt` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EPS before Extra Items-to-Price. It is defined as the most recently reported trailing 12-month earnings per share before extraordinary i |
| 38 | `fnd31_pqipmtt` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Pretax Income-to-Price. It is defined as the most recent trailing 12-month operating and nonoperating income per share before provisions |
| 39 | `fnd31_psmtt` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Sales-to-Price. It is defined as the most recently reported trailing 12-month sales per share for a stock, deflated by its trading price |
| 40 | `fnd31_qsg2_additionalfactor_unfiltered_rp` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability Ratio. It is defined as the latest reported quarterly operating income divided by 12-Month lagged total assets. |
| 41 | `fnd31_ttmsaleev` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Sales-to-Enterprise Value. It is defined as the trailing 12-month sales for a stock divided by the most recent enterprise value (EV). EV |
| 42 | `fnd31_pfgmtt` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price. It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its trading price |
| 43 | `fnd31_qsg2_additionalfactor_unfiltered_cpgspea2y` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-Year Ahead EPS Growth Percentage Change. It is defined as a stock's most recent consensus analysts' earnings forecast for fiscal year 2 mi |
| 44 | `fnd31_curindocfta_` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Oper Cash Flow-to-Total Assets. It is defined as a stock's trailing 12-month operating cash flow-to-total assets ratio |
| 45 | `fnd31_curindbp_` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry Relative Book-to-Market. It is defined as a stock's current book-to-price ratio (BP) less the average of the BPs of all stocks in t |
| 46 | `fnd31_yoychgroa` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Yearly Change in Return on Assets. It is defined as the most recent trailing 12-month income before extra items as a percentage of total ass |
| 47 | `fnd31_netdebt` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Ratio. It is defined as the net debt divided by the sum of the net debt, preferred stock, and common stock, where net debt equals t |
| 48 | `fnd31_pfcomtt` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Operating Cash Flow-to-Price. It is defined as the trailing 12-month operating cash flow per share for a stock divided by its trading pr |
| 49 | `fnd31_speghc` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Year Change in Assets-Adjusted TTM EPS. It is defined as the trailing 12-month earnings per share before extra items (EPS) minus 4 quarter |
| 50 | `fnd31_pfcfmtt` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price. It is defined as the trailing 12-month free cash flow per share for a stock divided by its trading price. Free  |
| 51 | `fnd31_qsg2_additionalfactor_unfiltered_chg12mtotdebt` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | 12-Month Change in Total Debt. It is defined as the 12-month relative change in total debt, where total debt is the sum of long-term and sho |
| 52 | `fnd31_high52w` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-Week High. It is defined as the month-end price divided by the highest monthly closing price in the past 12 months. |
| 53 | `fnd31_pctabv260low` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Above Last 260-day Lowest Trading Price. It is defined as a stock's current closing price divided by its lowest daily low price in las |
| 54 | `fnd31_curindsp_` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry Relative TTM Sales-to-Price. It is defined as a stock's trailing 12-month sales-to-price ratio (SP) less the average of the SPs of  |
| 55 | `fnd31_fc_numrevy1` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Net # of Revisions for Fiscal Year 1. It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less the  |
| 56 | `fnd31_pd09erpvc` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | CV of Prior 90-Day Closing Prices. It is defined as the standard deviation of a stock's last 90 days closing prices divided by the mean of t |
| 57 | `fnd31_curindep_` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM EPS-to-Price. It is defined as a stock's trailing 12-month earnings per share before extra items-to-price ratio (EP) l |
| 58 | `fnd31_fc_curindfwdep_` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | It is defined as a stock's next 4-quarter's analysts consensus earnings estimates-to-price ratio (FwdEP) less the average of the FwdEPs of a |
| 59 | `fnd31_skew90cortn` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-Day Stock Daily Excess Returns. It is defined as the skewness of the distribution of a stock's daily excess (compared to the  |
| 60 | `fnd31_skew90drtn` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-Day Stock Daily Returns. It is defined as the skewness (measure of lack of symmetry) of the distribution of a stock's daily p |
| 61 | `fnd31_qsg2_additionalfactor_unfiltered_irttmsalesev` | MATRIX | 0.942 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-relative TTM Sales to Enterprise Value. It is defined as a stock's trailing 12-month sales-to-enterprise (SEV) value less the avera |
| 62 | `fnd31_fcfroi` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow Return on Invested Capital. It is defined as the trailing 12-month free cash flow divided by the average invested capital in  |
| 63 | `fnd31_qsg2_additionalfactor_unfiltered_vefcomtt` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Operating Cash Flow-to-Enterprise Value. It is defined as the trailing 12-month operating cash flow per share for a stock divided by its |
| 64 | `fnd31_capexast` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Expenditure-to-Total Assets. It is defined as trailing 12-month capital expenditures divided by the total assets from the most recen |
| 65 | `fnd31_fcoghc` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Chg in Assets-adj TTM Oper Cash Flow. It is defined as the most recently reported trailing 12-month operating cash flow minus 4 quarter |
| 66 | `fnd31_pspeghc` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Change in Price-adj TTM EPS. It is defined as the difference between the most recently reported trailing 12-month earnings per share an |
| 67 | `fnd31_curindocfp_` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Oper Cash Flow-to-Price. It is defined as a stock's trailing 12-month operating cash flow-to-price ratio (OCFP) less t |
| 68 | `fnd31_yoychgaa` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Accruals to Assets. It is defined as the trailing 12-month income before extra items less the trailing 12-month operating cash flo |
| 69 | `fnd31_curindfcfp_` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Free Cash Flow-to-Price. It is defined as a stock's trailing 12-month free cash flow-to-price ratio (FCFP) less the av |
| 70 | `fnd31_pctchgastto` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Change in Asset Turnover Ratio. It is defined as the percent change in the most recent asset turnover ratio as compared to that of 4 qu |
| 71 | `fnd31_fcfghc` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Chg in Assets-adj TTM Free Cash Flow. It is defined as the trailing 12-month free cash flow minus 4 quarters ago trailing 12-month free |
| 72 | `fnd31_ttmcapexp` | MATRIX | 0.940 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Capital Expenditures-to-Price. It is defined as the trailing 12-month capital expenditures per share for a stock divided by its trading  |
| 73 | `fnd31_divyield` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Dividend Yield. It is defined as the trailing 12-month dividends per share for a stock divided by its trading price. |
| 74 | `fnd31_gear` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Gearing Ratio. It is defined as the long-term debt divided by the difference between total assets and current liability. |
| 75 | `fnd31_pctchgqtrast` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Yr Change in Total Assets. It is defined as the growth in the most recent reported quarterly total assets per share as compared to that of |
| 76 | `fnd31_vefcfmtt` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Enterprise Value. It is defined as the trailing 12-month free cash flow (FCF) for a stock scaled by its enterprise val |
| 77 | `fnd31_fixastto` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fixed Assets Turnover Ratio. It is defined as the trailing 12-month sales divided by the average of the total fixed assets in the same perio |
| 78 | `fnd31_vesspem21f_cf` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward 12-M EPS-to-Enterprise Value. It is defined as the consensus forward 12-month earnings per share forecast divided by the sum of mark |
| 79 | `fnd31_volpre6m` | MATRIX | 0.940 | 价量与波动 | 0 | — | — | — | UNTESTED | Average Trading Volume in Preceding 6-Month. It is defined as the 6-month moving average of average monthly turnover ratio, which equals the |
| 80 | `fnd31_aoer` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained Earnings-to-Total Assets. It is defined as the reported cumulative retained earnings from the most recent quarter deflated by repor |
| 81 | `fnd31_mktlev` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market Leverage. It is defined as a stock's total market value plus the most recent reported quarterly book debt then divided by the market  |
| 82 | `fnd31_mpn` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin. It is defined as the most recently reported quarterly net income after tax divided by the corresponding quarterly sales. |
| 83 | `fnd31_fcfsale` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-TTM Sales. It is defined as the trailing 12-month free cash flow divided by the trailing 12-month sales. |
| 84 | `fnd31_nlsales` | MATRIX | 0.939 | 其他 | 0 | — | — | — | UNTESTED | Natural Logarithm of TTM Sales. It is defined as the natural logarithm of the cubic of a company's trailing 12-month sales. |
| 85 | `fnd31_ocfmargin` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow Profit Margin. It is defined as the trailing 12-month cash flow from operations scaled by the trailing 12-month sales. |
| 86 | `fnd31_qsg2_additionalfactor_unfiltered_earnshortfall` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Shortfall. It is defined as the difference between reported accounting earnings and free cash flow, scaled by average assets. |
| 87 | `fnd31_w62isr` | MATRIX | 0.939 | 价量与波动 | 0 | — | — | — | UNTESTED | 26-Week Relative Price Strength. It is defined as a stock's most recent weekly closing price divided by its weekly closing price 26 weeks ag |
| 88 | `fnd31_curinddivp_` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Dividend Yield. It is defined as a stock's trailing 12-month dividend yield (DivYield) less the average of the DivYiel |
| 89 | `fnd31_qsg2_additionalfactor_unfiltered_numrevy2` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | Net # of Revisions for Fiscal Year 2. It is defined as the weighted average of the number of FY2 analyst earnings forecasts raised less the  |
| 90 | `fnd31_fcfequity` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow to Equity. It is defined as the trailing 12-month free cash flow divided by the average book equity value in the same per |
| 91 | `fnd31_fc_rev3y1` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY1 EPS Forecasts. It is defined as the change in the current mean consensus earnings estimate for fiscal year 1 less that o |
| 92 | `fnd31_fc_rev3y2` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts. It is defined as the change in the current mean consensus earnings estimate for fiscal year 2 less that o |
| 93 | `fnd31_pfcoghc` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Chg in Price-adj TTM Oper Cash Flow. It is defined as the difference between the most recently reported trailing 12-month operating cas |
| 94 | `fnd31_pfcfghc` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Yr Chg in Price-Adj TTM Free Cash Flow. It is defined as the difference between the trailing 12-month free cash flow per share and that of |
| 95 | `fnd31_capexsale` | MATRIX | 0.937 | 其他 | 0 | — | — | — | UNTESTED | TTM Capital Expenditures-to-Sales. It is defined as trailing 12-month capital expenditures divided by trailing 12-month sales. |
| 96 | `fnd31_actrtn6m` | MATRIX | 0.937 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-7 to month t-1. |
| 97 | `fnd31_cfroi` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Return on Invested Capital. It is defined as the trailing 12-month cash flow divided by the average invested capital in the same p |
| 98 | `fnd31_totalsaleg` | MATRIX | 0.937 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly TTM Total Sales Growth Rate. It is defined as the percent change in a company's trailing 12-month total sales (TOTSALE) as compared t |
| 99 | `fnd31_fc_fcfroey1p` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Product of TTM FCF Yield and Forward ROE. It is defined as the trailing 12-month free cash flow per share multiplied by the next 4-quarter c |
| 100 | `fnd31_pfcmtt` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Cash Flow-to-Price. It is defined as the trailing 12-month cash flows per share for a stock scaled by its trading price. Cash flow is de |
| 101 | `fnd31_fcghc` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Year Change in Assets-Adj TTM Cash Flow. It is defined as the trailing 12-month cash flow minus comparable trailing 12-month cash flow fro |
| 102 | `fnd31_qsg2_additionalfactor_unfiltered_yoychgroeart` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Yearly Change in ROE - Arithmetic Difference. It is defined as the yearly arithmetic change in the ratio of trailing-twelve-month earnings b |
| 103 | `fnd31_curindcfp_` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Cash Flow-to-Price. It is defined as a stock's trailing 12-month cash flow-to-price ratio (CFP) less the average of th |
| 104 | `fnd31_lagegp` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Lagged Inverse of PEG Ratio. It is defined as the trailing 12-month earnings per share before extraordinary items times the change in yearly |
| 105 | `fnd31_lfd` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Financial Leverage. It is defined as the sum of the trailing 12-month pretax income and the trailing 12-month interest expense divided by th |
| 106 | `fnd31_roic` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Invested Capital. It is defined as the trailing 12-month net income and interest expenses divided by the average reported invested |
| 107 | `fnd31_6351_rp` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | 15/36 Week Stock Price Ratio. It is defined as the moving average of a stock's prices in the last 15 weeks divided by the moving average of  |
| 108 | `fnd31_qsg2_additionalfactor_unfiltered_adpmoc` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leverage Composition. The most recent reported DA divided by the DA of the previous quarter. (DA = quarterly total liabilities as a percenta |
| 109 | `fnd31_pelh_cf` | MATRIX | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Revision Confidence. It is defined as the sum of the 3-month change in the highest and lowest FY1 earnings estimate, scaled by month- |
| 110 | `fnd31_roe` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity. It is defined as the trailing 12-month income before extra items divided by the average of common equity in the same perio |
| 111 | `fnd31_pctchgqtrsales` | MATRIX | 0.934 | 其他 | 0 | — | — | — | UNTESTED | 1-yr Change in Sales. It is defined as the growth in the most recent reported quarterly sales per share as compared to 4 quarters ago. |
| 112 | `fnd31_qsg2_additionalfactor_unfiltered_ttmopincev` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Operating Income to Enterprise Value. It is defined as the trailing 12-month operating income (before depreciation and amortization) div |
| 113 | `fnd31_indrelcroe_` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted Quarterly Return on Equity. It is defined as a stock's lagged quarterly return on equity (ROE) minus the average of the RO |
| 114 | `fnd31_actrtn9m` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | 9-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-10 to month t-1. |
| 115 | `fnd31_tobinq` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin q. It is defined as the market value of equity (E) plus debt (D) divided by assets (A), or (E + D)/A. D is measured using book values. |
| 116 | `fnd31_mpnghc` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Yr Change in Net Profit Margin. It is defined as the most recent quarterly net profit margin (NPM) minus the NPM 4 quarters ago. Net profi |
| 117 | `fnd31_p50_200ratio` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio. It is defined as the moving average of a stock's prices in last 50 days divided by the moving average of its p |
| 118 | `fnd31_ratrev6m` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Rating Revision. It is defined as the 6-month average of the monthly change in the average analyst recommendation. |
| 119 | `fnd31_fc_fwdroe` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward Return on Equity. It is defined as a stock's analysts' earnings estimates for the next four quarters divided by its most recent repo |
| 120 | `fnd31_w93ntr` | MATRIX | 0.932 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-Week Return with 4-week Lag. It is defined as a stock's price change from week t-43 to week t-4. |
| 121 | `fnd31_ebitdap` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Price. It is defined as the trailing 12-month earnings before interest, taxes, depreciation and amortization for a company div |
| 122 | `fnd31_curindebitdap_` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM EBITDA-to-Price. It is defined as a stock's trailing 12-month EBITDA-to-price ratio (EBITDAP) less the average of the  |
| 123 | `fnd31_ebitdaev` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value. It is defined as the trailing 12-month earnings before interest, taxes, depreciation, and amortization for a |
| 124 | `fnd31_capacq` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Acquisition Ratio. It is defined as the trailing 12-month operating cash flow less the trailing 12-month cash dividends and then div |
| 125 | `fnd31_pfcghc` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Yr Change in Price-adj TTM Cash Flow. It is defined as the difference between the trailing 12-month cash flow per share and that of 12 qua |
| 126 | `fnd31_pedu` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Change in Depreciation. It is defined as the difference between the trailing 12-month depreciation expenses and the expected leve |
| 127 | `fnd31_pfcf_cf` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward Free Cash Flow-to-Price. It is defined as the next 4 quarters' mean consensus earnings estimate plus trailing 12-month depreciation  |
| 128 | `fnd31_qsg2_additionalfactor_unfiltered_ps_wt` | MATRIX | 0.930 | 价量与波动 | 0 | — | — | — | UNTESTED | Time Weighted Sales Yield. It is defined as the time-weighted sales per share for FY1 and FY2 divided by its price. |
| 129 | `fnd31_nlvolcap` | MATRIX | 0.930 | 价量与波动 | 0 | — | — | — | UNTESTED | Average Monthly Trading Volume-to-Market Cap. It is defined as the natural logarithm of the quotient of the trailing 12-month average of the |
| 130 | `fnd31_bmpo` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit Margin. It is defined as the most recently reported quarterly operating income divided by the corresponding quarterly sales |
| 131 | `fnd31_chgshare` | MATRIX | 0.930 | 其他 | 0 | — | — | — | UNTESTED | Percent Change in Shares Outstanding. It is defined as the percent change in a company's current number of outstanding shares as compared to |
| 132 | `fnd31_qsg2_additionalfactor_unfiltered_psdwf` | MATRIX | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-Month Sales Yield. It is defined as the FY1 estimate of sales value per share divided by its trading price. |
| 133 | `fnd31_m6dn2ntr` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Second Preceding 6-month Return. It is defined as the percent change in a stock's price from month t-12 to month t-7. |
| 134 | `fnd31_ntrm01ff` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French Momentum. It is defined as the percent change in a stock's price from month t-12 to month t-2. |
| 135 | `fnd31_tstalp` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Year Price Momentum Indicator. It is defined as: (CORREL*(260-2)^.5)/(1-CORREL^2)^.5. CORREL is the correlation coefficient between the na |
| 136 | `fnd31_susgrowth` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sustainable Growth Rate. It is the maximum growth rate a firm can sustain without having to increase financial leverage. It is defined as: R |
| 137 | `fnd31_reinrate` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment Rate. It is defined as the trailing 12-month earnings per share before extra items less the trailing 12-month dividends per sha |
| 138 | `fnd31_slope52wp` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52-Week Price Trend Line. It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52- |
| 139 | `fnd31_qsg2_additionalfactor_unfiltered_pbdwf` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | Leading 12-Month Book Yield. It is defined as the average quarterly forward-looking book value per share divided by close price. |
| 140 | `fnd31_actrtn12m` | MATRIX | 0.926 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-13 to month t-1. |
| 141 | `fnd31_chg3yepsast` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Change in Assets-adj TTM EPS. It is defined as the trailing 12-month earnings per share before extra items (EPS) minus the EPS 12 qua |
| 142 | `fnd31_relpricestrength_` | MATRIX | 0.926 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month Relative Price Strength. It is defined as a stock's 12-month relative price-strength (PS) minus the PSs of all st |
| 143 | `fnd31_chg3yepsp` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Change in Price-adj TTM EPS. It is defined as the difference between the trailing 12-month earnings per share and that of 12 quarters a |
| 144 | `fnd31_niper` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income per Employee. It is defined as the income after taxes for the trailing 12 months divided by the number of employees at the end of |
| 145 | `fnd31_revper` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per Employee. It is defined as the trailing 12-month total sales divided by the number of employees at the end of the last reported  |
| 146 | `fnd31_rationalalpha` | MATRIX | 0.924 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha. It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 147 | `fnd31_chg3yocfast` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Change in Assets-adj TTM Oper Cash Flow. It is defined as the most recently reported trailing 12-month operating cash flow (OCF) minus  |
| 148 | `fnd31_surp` | MATRIX | 0.921 | 修正与预期 | 0 | — | — | — | UNTESTED | Real Earnings Surprise. It is defined as the difference between the actual earnings per share and consensus forecasts prior to the announcem |
| 149 | `fnd31_mpoghc` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Year Change in Operating Profit Margin. It is defined as the most recent quarterly operating profit margin minus that of 4 quarters ago. O |
| 150 | `fnd31_chg3yfcfast` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Chg in Assets-adj TTM Free Cash Flow. It is defined as the trailing 12-month free cash flow minus 12-quarters ago trailing 12-month fre |
| 151 | `fnd31_slope66wp` | MATRIX | 0.921 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 66-Week Price Trend Line. It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 66- |
| 152 | `fnd31_fc_stdevfy1epsp` | MATRIX | 0.921 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY1 EPS Estimates-to-Price. It is defined as the standard deviation of analyst forecasts for fiscal year 1 earnings, scaled by cl |
| 153 | `fnd31_fc_stdevfy2epsp` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY2 EPS Estimates-to-Price. It is defined as the standard deviation of analyst forecasts for fiscal year 2 earnings scaled by clo |
| 154 | `fnd31_w57w03_rp` | MATRIX | 0.919 | 价量与波动 | 0 | — | — | — | UNTESTED | 30-75 Week Stock Price Ratio. It is defined as the moving average of a stock's prices in the last 30 weeks divided by the moving average of  |
| 155 | `fnd31_qsg2_additionalfactor_unfiltered_pbwt` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Book Yield. It is defined as the time-weighted average of book value per share estimates in fiscal year 1 and fiscal year 2 di |
| 156 | `fnd31_chgalpha12m` | MATRIX | 0.917 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 12-Month Alpha. It is defined as the 6-month change in a stock's 12-month alpha, which equals the intercept from t |
| 157 | `fnd31_qsg2_additionalfactor_unfiltered_tw_ebitdaev` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time Weighted EBITDA/EV. It is defined as the time-weighted EBITDA/Enterprise Value for FY1 and FY2. |
| 158 | `fnd31_qsg2_additionalfactor_unfiltered_fwdebitdaev` | MATRIX | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-Month EBITDA/EV. It is defined as the FY1 estimate of EBITDA/Enterprise Value. |
| 159 | `fnd31_actrtn18m` | MATRIX | 0.915 | 价量与波动 | 0 | — | — | — | UNTESTED | 18-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-19 to month t-1. |
| 160 | `fnd31_chg3ycfast` | MATRIX | 0.915 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Change in Assets-Adjusted TTM Cash Flow. It is defined as the most recently reported trailing 12-month operating cash flow minus the  |
| 161 | `fnd31_debtcf` | MATRIX | 0.914 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term Debt-to-Cash Flow. It is defined as the sum of the most recent reported long-term debt and short-term interest-bearing debt divide |
| 162 | `fnd31_fc_rev6` | MATRIX | 0.914 | 修正与预期 | 0 | — | — | — | UNTESTED | Averaged Last 6-M EPS Revisions for FY1. It is defined as the average of prior 6-month monthly changes in a stock's consensus analysts earni |
| 163 | `fnd31_pfcoy3ghc` | MATRIX | 0.913 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Change in Price-Adjusted TTM Operating Cash Flow. It is defined as the difference between the trailing 12-month operating cash flow p |
| 164 | `fnd31_qsg2_additionalfactor_unfiltered_yen` | MATRIX | 0.913 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings Yield. It is defined as the average of three normalized earnings calculated by ROE, NPM and EPS FY2, scaled by price. |
| 165 | `fnd31_pfcfy3ghc` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Change in Price-Adjusted TTM FCF. It is defined as the difference between the most recently reported trailing 12-month free cash flow |
| 166 | `fnd31_qsg2_additionalfactor_unfiltered_rev3my1std` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY1 EPS Forecasts: Dispersion Relative. It is defined as the change in a stock's current analysts' mean earnings estimate fo |
| 167 | `fnd31_qsg2_additionalfactor_unfiltered_rev3my2std` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts: Dispersion Relative. It is defined as the change in a stock's current analysts' mean earnings estimate fo |
| 168 | `fnd31_qsg2_additionalfactor_unfiltered_pcwt` | MATRIX | 0.911 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Cash Yield. It is defined as the time-weighted average of cash flows per share estimates in fiscal year 1 and fiscal year 2 di |
| 169 | `fnd31_nopatmargin` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | NOPAT Margin. It is defined as: (Net Income + Interest Expense*(1-Effective Tax Rate))/Net Sales. All items are for trailing 12-month. Effec |
| 170 | `fnd31_qsg2_additionalfactor_unfiltered_slope4qeps5y` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | Slope of 5-yr TTM EPS Trend Line. It is defined as the slope coefficient between monthly dates and the corresponding trailing 12-month earni |
| 171 | `fnd31_qsg2_additionalfactor_unfiltered_y5speq4rqsr` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | R Sqr of 5-yr TTM EPS Trend Line. It is defined as the slope coefficient between monthly dates and the corresponding trailing 12-month earni |
| 172 | `fnd31_liqcoeff` | MATRIX | 0.909 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity Coefficient. It is the slope of the regression between the monthly stock trading turnover ratio (X) and the contemporary monthly s |
| 173 | `fnd31_voctni` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interest Coverage. It is defined as the most recently reported quarterly operating income before depreciation divided by the quarterly long- |
| 174 | `fnd31_pctchgocf` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Year Growth in TTM Oper Cash Flow. It is defined as the percent change of a stock's most recent trailing 12-month operating cash flow per  |
| 175 | `fnd31_pctchgcf` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Growth in TTM Cash Flow. It is defined as the percent change in a stock's most recent trailing 12-month cash flow per share (CF) as com |
| 176 | `fnd31_cfleverage` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Leverage. It is defined as the total liabilities divided by the trailing 12-month operating cash flow. |
| 177 | `fnd31_oplev` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Operating Leverage. It is defined as the percent change in the trailing 12-month operating income from the previous quarter divided by the p |
| 178 | `fnd31_pfcy3ghc` | MATRIX | 0.906 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Yr Change in Price-Adj TTM Cash Flow. It is defined as the difference between the trailing 12-month cash flow per share and that of 12 qua |
| 179 | `fnd31_qsg2_additionalfactor_unfiltered_fc_y2repsg` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-Year Projected EPS Growth. It is defined as a stock's most recent consensus analysts' earnings forecast for fiscal year 2 minus the most r |
| 180 | `fnd31_qsg2_additionalfactor_unfiltered_pcdwf` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leading 12-Month Cash Yield. It is defined as the average quarterly forward-looking cash flows per share divided by close price. |
| 181 | `fnd31_chg6malpha18m` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 18-Month Alpha. It is defined as the 6-month change in a stock's 18-month alpha, which equals the intercept from t |
| 182 | `fnd31_m42rav` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Value at Risk. It is defined as the minimum of a stock's monthly price return in the last 20-month period. |
| 183 | `fnd31_cg3ysales` | MATRIX | 0.904 | 宏观与行业 | 0 | — | — | — | UNTESTED | 3-yr Compound Annual Sales Growth. It is defined as the geometric growth rate of the trailing 12-month sales per share in the last 12 quarte |
| 184 | `fnd31_lumqca` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition Multiple. It is defined as the most recent quarterly reported invested capital divided by the trailing 12-month EBITDA. |
| 185 | `fnd31_epschgetr` | MATRIX | 0.903 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS from Change in Effective Tax Rate. It is defined as the trailing 12-month pre-tax income per share times the difference between the most |
| 186 | `fnd31_actrtn24m` | MATRIX | 0.903 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-25 to month t-1. |
| 187 | `fnd31_totalcov` | MATRIX | 0.902 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Coverage. It equals (Cash Flow from Operations + Interest Paid + Tax Paid)/(Interest + Principal Paid). |
| 188 | `fnd31_ica` | MATRIX | 0.901 | 其他 | 0 | — | — | — | UNTESTED | Abnormal Capital Investment. It is defined as the change in a firm's most recent trailing 12-month capital investment intensity compared to  |
| 189 | `fnd31_spe1yfvc_cf` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | FY1 EPS Estimates Dispersion. It is defined as the standard deviation of analyst earnings estimates for fiscal year 1 divided by the mean co |
| 190 | `fnd31_spe2yfvc_cf` | MATRIX | 0.896 | 修正与预期 | 0 | — | — | — | UNTESTED | FY2 EPS Forecast Dispersion. It is defined as the standard deviation of analyst earnings estimates for fiscal year 2 divided by the mean con |
| 191 | `fnd31_pctchgeps` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Growth in TTM Earnings per Share. It is defined as the percent change in a stock's most recent trailing 12-month earnings per share bef |
| 192 | `fnd31_qsg2_additionalfactor_unfiltered_yoychgroepct` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Yearly Change in ROE - Percentage Method. It is defined as the yearly percentage change in the ratio of trailing-twelve-month earnings befor |
| 193 | `fnd31_qsg2_additionalfactor_unfiltered_pu` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Profitability. It is defined as the difference between realized profitability and the expected one, which is calculated from a re |
| 194 | `fnd31_mrspe_cf` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Revision Magnitude. It is defined as the 3-month change in the median FY1 consensus earnings forecast, scaled by the current mean ear |
| 195 | `fnd31_qsg2_additionalfactor_unfiltered_ebitdadebt` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA to long-term Debt. It is defined as a stock's trailing 12-month EBITDA divided by the most recently reported total long-term debt |
| 196 | `fnd31_qsg2_additionalfactor_unfiltered_fc_fqsurstd` | MATRIX | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Most Recent Quarterly Earnings Surprise. It is defined as a stock's most recent quarterly earnings surprise (actual fiscal quarter EPS less  |
| 197 | `fnd31_ollev` | MATRIX | 0.890 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Liability Leverage. It is defined as 1 minus the ratio of (short-term debt + long-term debt + common equity + preferred equity - c |
| 198 | `fnd31_qsg2_additionalfactor_unfiltered_chgqtrepssurp` | MATRIX | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Real Earnings Surprise. It is defined as the change in quarterly earnings surprise (Actual EPS - Consensus Estimate EPS), scaled b |
| 199 | `fnd31_chgollev` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Operating Liability Leverage. It is defined as the current quarter operating liability leverage less the operating liability lever |
| 200 | `fnd31_pctchg3ycf` | MATRIX | 0.885 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Growth in TTM Cash Flow. It is defined as the percent change in a stock's most recent trailing 12-month cash flow per share (CF) as com |
| 201 | `fnd31_pctchg3yocf` | MATRIX | 0.885 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Growth in TTM Operating Cash Flow. It is defined as the percent change in a stock's most recent trailing 12-month operating cash flow |
| 202 | `fnd31_saleeps` | MATRIX | 0.884 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM Sales vs. EPS. It is defined as the absolute value of the difference between the yearly percent change in trailing 12-month sa |
| 203 | `fnd31_spefcn` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM EPS vs. Oper Cash Flows. It is defined as the absolute value of the difference between the yearly percent change in trailing 1 |
| 204 | `fnd31_pctchg3yeps` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Growth in TTM Earnings per Share. It is defined as the percent change in a stock's most recent trailing 12-month earnings per share (EP |
| 205 | `fnd31_saleg5y` | MATRIX | 0.882 | 其他 | 0 | — | — | — | UNTESTED | 5-yr Sales Growth. It is defined as the difference between the trailing 12-month sales per share (SALE) and the SALE 20 quarters ago and the |
| 206 | `fnd31_gtl` | MATRIX | 0.880 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-Term Growth Rate Estimates. It is defined as the consensus long-term growth forecast. It generally represents an expected annual increa |
| 207 | `fnd31_pge_cf` | MATRIX | 0.880 | 修正与预期 | 0 | — | — | — | UNTESTED | Inverse of PEG Ratio. It is defined as a company's next 4-quarter mean earnings estimate multiplied by the mean long-term growth rate foreca |
| 208 | `fnd31_qsg2_additionalfactor_unfiltered_60dsigma` | MATRIX | 0.880 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock Return Volatility. It is defined as the standard deviation of a stock's monthly returns in the prior 60 days. |
| 209 | `fnd31_actrtn36m` | MATRIX | 0.876 | 价量与波动 | 0 | — | — | — | UNTESTED | 36-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-37 to month t-1. |
| 210 | `fnd31_qsg2_additionalfactor_unfiltered_y5speq4vc` | MATRIX | 0.874 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stability of 5-yr TTM Earnings per Share. It is defined as the standard deviation of the last 20-Month trailing 12-month earnings per share  |
| 211 | `fnd31_nfaldebt` | MATRIX | 0.872 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Fixed Assets to Long-term Debt. It is defined as the most recent quarterly reported net fixed assets divided by the total long-term debt |
| 212 | `fnd31_qsg2_additionalfactor_unfiltered_coreepsp` | MATRIX | 0.867 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Core Earnings-to-Price. It is defined as the trailing 12-month earnings per share from operations for a stock deflated by its trading pr |
| 213 | `fnd31_grahamnum` | MATRIX | 0.867 | 其他 | 0 | — | — | — | UNTESTED | Graham Number = Sqrt(22.5 x EPS x BVPS). |
| 214 | `fnd31_chgalpha36m` | MATRIX | 0.864 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 36-Month Alpha. It is defined as the 6-month change in a stock's 36-month alpha, which equals the intercept from t |
| 215 | `fnd31_fc_dypeg` | MATRIX | 0.863 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of Dividend Yield-adjusted PEG. It is defined as the reciprocal of a stock's forward 12-month P/E ratio divided by the total grow |
| 216 | `fnd31_qsg2_additionalfactor_unfiltered_fqsurstd60dlag` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | 60-Day Lagged Quarterly Earnings Surprise. It is defined as the most recent actual fiscal quarter EPS less the consensus earnings estimate 6 |
| 217 | `fnd31_qsg2_additionalfactor_unfiltered_ebitdadebtchg` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA to long-term Debt. It is defined as the yearly change in a stock's trailing 12-month EBITDA divided by the most recently reported |
| 218 | `fnd31_gtlm6ghc` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-M Change in Long-term Growth Estimates. It is defined as the percent change in the most recent mean consensus long-term growth forecast as |
| 219 | `equity_cds_spread_to_dividend_ratio` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model-based residual capturing divergence between equity price and CDS spread, adjusted by the strength of the cross-asset relationship |
| 220 | `fnd31_60dsigma` | MATRIX | 0.858 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return volatility measured as the standard deviation of returns over the prior 60 days |
| 221 | `fnd31_adpmoc` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Comprehensive debt-to-assets ratio: sum of long-term debt, short-term debt, underfunded pension liabilities, operating lease obligations, an |
| 222 | `issuer_default_risk_score` | MATRIX | 0.858 | 价量与波动 | 0 | — | — | — | UNTESTED | Market-implied credit risk measured by CDS spread levels; lower values indicate lower risk |
| 223 | `three_month_credit_revision` | MATRIX | 0.858 | 修正与预期 | 0 | — | — | — | UNTESTED | Three-month change in CDS spreads indicating credit risk revisions; decreases reflect improving credit |
| 224 | `trend_of_credit_spread_subtraction` | MATRIX | 0.858 | 价量与波动 | 0 | — | — | — | UNTESTED | Difference between the 5-year CDS spread and the 1-year CDS spread (5Y minus 1Y); lower slope is preferred |
| 225 | `fnd31_ebitdadebt` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA-to-Debt ratio (trailing-twelve-month EBITDA divided by current total debt), indicating leverage and cash flow coverage |
| 226 | `fnd31_ebitdadebtchg` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in the EBITDA-to-debt ratio (change in TTM EBITDA divided by total debt), indicating improvement or deterioration in d |
| 227 | `fnd31_qsg2_additionalfactor_unfiltered_avg10yep` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cyclically Adjusted Earnings-to-Price. It is defined as the average earnings of the stock over the past 10 years, divided by its current pri |
| 228 | `fnd31_qsg2_additionalfactor_unfiltered_capexdeplink` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Expenditures to Depreciation Linkage. It is defined as the absolute value of the difference between ranked (1-1000) quarterly capita |
| 229 | `fnd31_dcc` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Cash Flow Debt Coverage Ratio. It is defined as the most recently reported quarterly cash flow from operations less the cash dividen |
| 230 | `fnd31_qsg2_additionalfactor_unfiltered_rev6fy2` | MATRIX | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Averaged Last 6-M EPS Revisions for FY2. It is defined as the average of prior 6-month monthly changes in a stock's consensus analysts earni |
| 231 | `fnd31_cashp` | MATRIX | 0.851 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash-to-Price. It is defined as the most recently reported cash and equivalents per share of a company divided by trading price. |
| 232 | `fnd31_cashsev` | MATRIX | 0.851 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash to Enterprise Value. It is defined as the total cash & equivalents divided by the sum of the market value of common equity and book val |
| 233 | `fnd31_aspanratio` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Attention Span Ratio. It is defined as a stock's quarterly operating assets minus its operating liabilities, deflated by the lagged total as |
| 234 | `fnd31_cashburnrate` | MATRIX | 0.850 | 宏观与行业 | 0 | — | — | — | UNTESTED | Cash Burn Rate. It is defined as: -(Cash From Operations + Cash from Investments)/(Cash + Short-term Investments). |
| 235 | `fnd31_chgnoa` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Net Operating Assets. It is defined as the year-over-year change of net operating assets to total assets, where net operating asse |
| 236 | `fnd31_dpcapex` | MATRIX | 0.849 | 其他 | 0 | — | — | — | UNTESTED | Change in TTM Depreciation vs. CapEx. It is defined as the absolute value of the difference between the yearly percent change in trailing 12 |
| 237 | `fnd31_qsg2_additionalfactor_unfiltered_twepsrev` | MATRIX | 0.848 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Revision. It is defined as the 6-month average of the time-weighted sum of the FY1 and FY2 earnings estimate revision |
| 238 | `fnd31_cashsale` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-Sales. It is defined as the average cash & equivalents in the trailing 12 months divided by the trailing 12-month sales. |
| 239 | `fnd31_covol` | MATRIX | 0.847 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Trading Volume Trend. It is defined as the slope of the least squares regression line of the last 60 months of monthly trading volu |
| 240 | `fnd31_pca` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | Average Collection Period. It is defined as the average of the trailing 12-month reported accounts receivable times 365 and then divided by  |
| 241 | `fnd31_opincltd` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM Oper Income vs. LT Debt. It is defined as the difference between the yearly percent change in operating income and the yearly  |
| 242 | `fnd31_netcashp` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Cash to Equity. It is defined as the most recently reported quarterly cash & equivalents less the long-term debt and current debt for a  |
| 243 | `fnd31_invast` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inventory-to-Total Assets. It is defined as the current inventory level deflated by the total assets from the most recent quarter. |
| 244 | `fnd31_qsg2_additionalfactor_unfiltered_twepsstdrev` | MATRIX | 0.846 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Revision Dispersion. It is defined as the 6-month average of the time-weighted sum of the FY1 and FY2 earnings estima |
| 245 | `fnd31_rau` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Change in Accounts Receivable. It is defined as the difference between current accounts receivable and the expected level of acco |
| 246 | `fnd31_salerec` | MATRIX | 0.843 | 其他 | 0 | — | — | — | UNTESTED | Change in TTM Sales vs. Accounts Receivable. It is defined as the difference between the yearly percent change in trailing 12-month sales an |
| 247 | `fnd31_chgars` | MATRIX | 0.842 | 其他 | 0 | — | — | — | UNTESTED | 1-yr Chg in Acct Receivable as % of Sales. It is defined as the change between the last reported accounts receivable as a percentage of trai |
| 248 | `fnd31_qsg2_additionalfactor_unfiltered_chginvavgast` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Inventory to Average Assets. It is defined as the 12-month change in the quarterly total inventories scaled by the average of asse |
| 249 | `fnd31_pctchgfcf` | MATRIX | 0.839 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Growth in TTM Free Cash Flow. It is defined as the percent change in a stock's most recent trailing 12-month free cash flow per share ( |
| 250 | `fnd31_sighc` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | 1-yr Chg in QTR Inventory as % of Sales. It is defined as the most recently reported inventory as a percentage of trailing 12-month sales mi |
| 251 | `fnd31_qsg2_additionalfactor_unfiltered_apg` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Gross Profit to Assets. It is defined as the TTM (Sales-COGS)/ Total Assets. |
| 252 | `fnd31_beta` | MATRIX | 0.832 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Beta. It is defined as 0.67 times the 60-month beta plus 0.33. Beta is the covariance between a stock's monthly return and the mont |
| 253 | `fnd31_qsg2_additionalfactor_unfiltered_mpg` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Gross Profit Margin. It is defined as the TTM (Sales-COGS)/Sales. |
| 254 | `fnd31_qsg2_additionalfactor_unfiltered_apgghcy1` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Year Change in Gross Profit to Assets. It is defined as the Year on Year Change in Gross Profit to Assets. |
| 255 | `fnd31_salegpm` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in QTR Sales vs. Gross Margin. It is defined as the difference between the yearly change in most recent reported quarterly sales and  |
| 256 | `fnd31_qsg2_additionalfactor_unfiltered_pbroeresidual` | MATRIX | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Book Return-on-Equity Combination (PB-ROE). An adjustment to the classic price-to-book model incorporating firm growth, based on a  |
| 257 | `fnd31_yoychggpm` | MATRIX | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Yearly Change In Gross Profit Margin. It is defined as the most recent quarterly reported gross profit margin minus the margin for the same  |
| 258 | `fnd31_fc_rel5yfwdep` | MATRIX | 0.823 | 修正与预期 | 0 | — | — | — | UNTESTED | 5-Yr Relative Leading 12-Month Earnings Yield. It is defined as a stock's current next 4-quarter's consensus analyst earnings forecasts-to-p |
| 259 | `fnd31_fc_ebop` | MATRIX | 0.823 | 盈利与财务 | 0 | — | — | — | UNTESTED | Edwards-Bell-Ohlson Value-to-Price. It is defined as a stock's valuation based on the Edwards-Bell-Ohlson (EBO) model deflated by its tradin |
| 260 | `fnd31_qsg2_additionalfactor_unfiltered_md` | MATRIX | 0.821 | 其他 | 0 | — | — | — | UNTESTED | Distress Measure. It is defined as the financial distress model employed by Campbell, Hilscher and Szilagyi (2008) and Chen and Zhang (2009) |
| 261 | `fnd31_chgvolpre4y` | MATRIX | 0.821 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-Year Change in the Average Trading Volume. It is defined as the change in the most recent 6-month moving average of monthly turnover ratio |
| 262 | `fnd31_rerror60m` | MATRIX | 0.820 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression Error of 60-Month CAPM. It is defined as the standard error of the slope of the least squares regression line for a stock's last  |
| 263 | `fnd31_sigma` | MATRIX | 0.820 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock Return Volatility. It is defined as the standard deviation of a stock's monthly returns in the prior 60 months. |
| 264 | `fnd31_alpha60m` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Alpha. It is defined as the intercept of the regression line which best fits a stock's monthly price return against the S&P 500 ind |
| 265 | `fnd31_betasigma` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of Beta and Sigma. It is defined as the product of the adjusted 60-month Beta and 60-month Sigma (standard deviation of monthly pric |
| 266 | `fnd31_actrtn60m` | MATRIX | 0.817 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Active Return with 1-Month Lag. It is defined as a stock's price percent change from month t-61 to month t-1. |
| 267 | `fnd31_pctchg3yfcf` | MATRIX | 0.810 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Growth in TTM Free Cash Flow. It is defined as the percent change in a stock's most recent trailing 12-month free cash flow per share ( |
| 268 | `fnd31_qsg2_additionalfactor_unfiltered_apgghcy3` | MATRIX | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Change in Gross Profit to Assets. It is defined as the 3-year on year change in gross profit to assets. |
| 269 | `fnd31_vniu` | MATRIX | 0.806 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Change in Inventory Level. It is defined as the difference between the current inventory level and the expected level of inventor |
| 270 | `fnd31_rel5ybp` | MATRIX | 0.801 | 其他 | 0 | — | — | — | UNTESTED | 5-yr Relative Book-to-Market. It is defined as a stock's current book-to-market ratio (BP) minus the average of the BPs in the last 60 month |
| 271 | `fnd31_rel5yep` | MATRIX | 0.800 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-Year Relative TTM Earnings-to-Price. It is defined as a stock's current trailing 12-month earnings per share before extra items-to-price r |
| 272 | `fnd31_rel5ysp` | MATRIX | 0.798 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-Yr Relative TTM Sales-to-Price. It is defined as a stock's current trailing 12-month sales-to-price ratio (SP) minus the average of the SP |
| 273 | `fnd31_qsg2_additionalfactor_unfiltered_mpgghcy3` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-Year Change in Gross Profit Margin. It is defined as the 3-year on year change in gross profit margin. |
| 274 | `fnd31_o_additionalfactor4_apg` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing-twelve-month gross profit to total assets ratio (gross profit divided by total assets) |
| 275 | `fnd31_o_additionalfactor4_apgghcy1` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit to assets ratio |
| 276 | `fnd31_o_additionalfactor4_apgghcy3` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year change in gross profit to assets ratio |
| 277 | `fnd31_o_additionalfactor4_capexdeplink` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Capital Expenditures to Depreciation Linkage |
| 278 | `fnd31_o_additionalfactor4_chg12mtotdebt` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in total debt over the last 12 months |
| 279 | `fnd31_o_additionalfactor4_chginvavgast` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in inventories scaled by average assets |
| 280 | `fnd31_o_additionalfactor4_chgqtrepssurp` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Real Earnings Surprise |
| 281 | `fnd31_o_additionalfactor4_coreepsp` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month core earnings per share divided by price; excludes extraordinary items |
| 282 | `fnd31_o_additionalfactor4_cpgspea2y` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Two-year ahead EPS growth percentage: (FY2 EPS − FY1 EPS) divided by FY1 EPS |
| 283 | `fnd31_o_additionalfactor4_divgp` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends paid over the trailing twelve months divided by gross profit (shareholder payout to gross profit) |
| 284 | `fnd31_o_additionalfactor4_dtsm1_rd` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Realized volatility of daily stock returns over the past month (standard deviation) |
| 285 | `fnd31_o_additionalfactor4_earningstorpedo` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Torpedo |
| 286 | `fnd31_o_additionalfactor4_earnshortfall` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Shortfall |
| 287 | `fnd31_o_additionalfactor4_fc_fqsurstd` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Standardized most recent quarterly earnings surprise: actual EPS minus consensus, scaled by forecast dispersion |
| 288 | `fnd31_o_additionalfactor4_fc_y2repsg` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | 2-Year Projected EPS Growth |
| 289 | `fnd31_o_additionalfactor4_fqsurstd60dlag` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized quarterly earnings surprise measured with a 60-day lag |
| 290 | `fnd31_o_additionalfactor4_fwdebitdaev` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward next 12 months EBITDA divided by enterprise value |
| 291 | `fnd31_o_additionalfactor4_irttmsalesev` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-relative ratio of trailing twelve month sales to enterprise value |
| 292 | `fnd31_o_additionalfactor4_md` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Distress Measure |
| 293 | `fnd31_o_additionalfactor4_mpg` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing-twelve-month gross profit margin (gross profit divided by sales) |
| 294 | `fnd31_o_additionalfactor4_mpgghcy3` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM gross profit margin over the past three years, measured as the 3-year year-on-year change in GPM |
| 295 | `fnd31_o_additionalfactor4_numrevy2` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Net # of Revisions for Fiscal Year 2 |
| 296 | `fnd31_o_additionalfactor4_ohlsonscore` | MATRIX | 0.795 | 风险与质量 | 0 | — | — | — | UNTESTED | Ohlson O-score estimating bankruptcy/distress risk from financial ratios |
| 297 | `fnd31_o_additionalfactor4_pbdwf` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Forward next 12 months book value per share divided by stock price (forward book yield) |
| 298 | `fnd31_o_additionalfactor4_pbroeresidual` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Book Return-on-Equity Combination (PB-ROE) |
| 299 | `fnd31_o_additionalfactor4_pbwt` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | Time-weighted blend of forward book yield |
| 300 | `fnd31_o_additionalfactor4_pcdwf` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward next 12 months cash flow per share divided by stock price (forward cash yield) |
| 301 | `fnd31_o_additionalfactor4_pcwt` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted blend of forward cash flow yield |
| 302 | `fnd31_o_additionalfactor4_ps_wt` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Time-weighted blend of current and forward sales to price yield |
| 303 | `fnd31_o_additionalfactor4_psdwf` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Forward next 12 months sales divided by stock price (forward sales yield) |
| 304 | `fnd31_o_additionalfactor4_pu` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Profitability |
| 305 | `fnd31_o_additionalfactor4_rev3my1std` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Three-month change in FY1 EPS estimates scaled by analyst dispersion |
| 306 | `fnd31_o_additionalfactor4_rev3my2std` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Three-month change in FY2 EPS estimates scaled by analyst dispersion |
| 307 | `fnd31_o_additionalfactor4_rev6fy2` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Average FY2 EPS estimate revisions over the past six months |
| 308 | `fnd31_o_additionalfactor4_rp` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability ratio: operating income scaled by total assets (QSG convention) |
| 309 | `fnd31_o_additionalfactor4_rqi_rd` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Month Stock Return Interquartile Range |
| 310 | `fnd31_o_additionalfactor4_slope4qeps5y` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Slope of the linear trend line for rolling four-quarter TTM EPS over the past five years |
| 311 | `fnd31_o_additionalfactor4_ttmopincev` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Trailing twelve month operating income divided by enterprise value |
| 312 | `fnd31_o_additionalfactor4_tw_ebitdaev` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted blend of current and forward EBITDA to enterprise value |
| 313 | `fnd31_o_additionalfactor4_twepsrev` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Time-weighted measure of analysts’ EPS estimate revisions (e.g., FY1/FY2) |
| 314 | `fnd31_o_additionalfactor4_twepsstdrev` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Revision Dispersion |
| 315 | `fnd31_o_additionalfactor4_vefcomtt` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months operating cash flow divided by enterprise value |
| 316 | `fnd31_o_additionalfactor4_y5speq4rqsr` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | R-squared of the linear trend line fitted to rolling four-quarter TTM EPS over the past five years |
| 317 | `fnd31_o_additionalfactor4_y5speq4vc` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Coefficient of variation of rolling four-quarter TTM EPS over the past five years, measuring stability |
| 318 | `fnd31_o_additionalfactor4_yen` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized earnings yield (standardized inverse of price-to-earnings) |
| 319 | `fnd31_o_additionalfactor4_yoychgroeart` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year absolute change in return on equity, using arithmetic difference |
| 320 | `fnd31_o_additionalfactor4_yoychgroepct` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percentage change in return on equity |
| 321 | `fnd31_perg` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG Ratio. It is defined as the stock price divided by the leading 12-month consensus earnings forecast, scaled by the average |
| 322 | `fnd31_o_additionalfactor3_avg10yep` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average 10 year economic profit |
| 323 | `fnd31_rel5yfcfp` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-yr Relative TTM Free Cash Flow-to-Price. It is defined as a stock's current trailing 12-month free cash flow-to-price ratio (FCFP) minus t |
| 324 | `fnd31_rel5yocfp` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-yr Relative TTM Oper Cash Flow-to-Price. It is defined as a stock's current trailing 12-month operating cash flow-to-price ratio (OCFP) mi |
| 325 | `fnd31_varresirtn` | MATRIX | 0.780 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Residual Return Variance. It is defined as the variance of a stock's monthly residual return in the last 24 months. The monthly res |
| 326 | `fnd31_rel5ycfp` | MATRIX | 0.774 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-Yr Relative TTM Cash Flow-to-Price. It is defined as a stock's current trailing 12-month cash flow-to-price ratio (CFP) minus the average  |
| 327 | `fnd31_rel5yebitdap` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-yr Relative TTM EBITDA-to-Price. It is defined as a stock's current trailing 12-month EBITDA per share-to-price ratio (EBITDAP) minus the  |
| 328 | `fnd31_astcomp` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset Composition. It is defined as the total current assets from the most recent quarter divided by the total assets from the most recent q |
| 329 | `fnd31_cashratio` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash & Equivalents-to-Current Liabilities. It is defined as the most recently reported quarterly cash & equivalents divided by current liabi |
| 330 | `fnd31_curratio` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio: It is defined as the reported current assets from the most recent quarter divided by the current liabilities from the most re |
| 331 | `fnd31_pcurlia` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Liabilities-to-Price. It is defined as a stock's most recently reported quarterly current liabilities per share divided by its closi |
| 332 | `fnd31_ocfratio` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow Ratio. It is defined as a stock's most recently reported quarterly cash flow from operations divided by its current liab |
| 333 | `fnd31_nnastp` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Current Assets-to-Price. It is defined as the current assets per share minus total liabilities per share divided by the price. |
| 334 | `fnd31_rq` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio. It is defined as the current assets less inventories from the most recent quarter divided by the total current liabilities from |
| 335 | `fnd31_flowratio` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow Ratio. It is defined as the difference between current assets and cash & equivalents divided by the difference between current liabilit |
| 336 | `fnd31_wcast` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working Capital-to-Total Assets. It is defined as the average working capital in the trailing 12 months divided by the average total assets  |
| 337 | `fnd31_yoychgcr` | MATRIX | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year Change in Current Ratio. It is defined as the most recent reported quarterly current ratio and the current ratio for the same |
| 338 | `fnd31_chgreccast` | MATRIX | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | YOY Change in Accounts Receivable to Current Assets. It is defined as the percent change in the most recent quarterly reported accounts rece |
| 339 | `fnd31_qsg2_additionalfactor_unfiltered_ohlsonscore` | MATRIX | 0.762 | 价量与波动 | 0 | — | — | — | UNTESTED | Ohlson Bankruptcy Score. It is a model assessing a company's probability of bankruptcy by considering firm size, capital structure, financia |
| 340 | `fnd31_pinoa` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Return on Net Operating Assets. It is defined as the trailing 12-month operating income after depreciation divided by the average net |
| 341 | `fnd31_cws` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Working Capital-to-Trailing 12-Month Sales. It is defined as the average of working capital for the trailing 12 months divided by the total  |
| 342 | `fnd31_iqa` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset Quality Index. It is defined as the year-over-year change of 1 minus the ratio of current assets plus PP&E divided by total assets. |
| 343 | `fnd31_altmanz` | MATRIX | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Altman Z Score = 1.2* (Current Assets - Current Liabilities)/TA + 1.4*Retained Earnings/TA + 3.3*Earnings before Interest and Taxes/TA + 0.6 |
| 344 | `fnd31_ydp_cf` | MATRIX | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted Dividend Yield. It is defined as an assumed payout ratio multiplied by the next 4-quarter consensus earnings estimate divided by t |
| 345 | `fnd31_ppa` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Average Payable Period. It is defined as the average of the trailing 12-month accounts payable times 365 divided by the trailing 12-month co |
| 346 | `fnd31_divcov` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend Coverage Ratio. It is defined as a company's trailing 12-month earnings from operations divided by the amount of its indicated annu |
| 347 | `fnd31_qsg_additionalfactor_adpmoc` | MATRIX | 0.747 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leverage Composition. The most recent reported DA divided by the DA of the previous quarter. (DA = quarterly total liabilities as a percenta |
| 348 | `fnd31_pau` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Change in Accounts Payable. It is defined as the difference between current accounts payable and the expected level of accounts p |
| 349 | `fnd31_cashc` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | Cash Cycle. It is defined as the average inventory days plus the average collection days minus the average payable days. |
| 350 | `fnd31_ags` | MATRIX | 0.740 | 其他 | 0 | — | — | — | UNTESTED | SG&A Expenses-to-Sales. It is defined as the trailing 12-month selling, general management, and administration expenses divided by the trail |
| 351 | `fnd31_qsg2_additionalfactor_unfiltered_earningstorpedo` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings Torpedo. It is defined as Next 4 Quarter EPS Estimate + TTM Real Earnings Surprise/TTM EPS where TTM Earnings Surprise = Actual EPS |
| 352 | `fnd31_otvni` | MATRIX | 0.727 | 价量与波动 | 0 | — | — | — | UNTESTED | Inventory Turnover Ratio. It is defined as the trailing 12-month cost of goods sold divided by the average of inventory in the same period. |
| 353 | `fnd31_div5yg` | MATRIX | 0.721 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-Year Dividend Growth Rate. It is defined as the 5-year growth in dividends. |
| 354 | `fnd31_cogsinvt` | MATRIX | 0.719 | 其他 | 0 | — | — | — | UNTESTED | Change in TTM COGS vs. Inventory Level. It is defined as the absolute value of the difference between the yearly percent change in trailing  |
| 355 | `fnd31_rel5ydivp` | MATRIX | 0.719 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-Yr Relative TTM Dividend Yield. It is defined as a stock's current dividend yield (DivYield) minus the average of the DivYields in the las |
| 356 | `fnd31_qsg_additionalfactor2_ebitdadebt` | MATRIX | 0.717 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA to long-term Debt. It is defined as a stock's trailing 12-month EBITDA divided by the most recently reported total long-term debt |
| 357 | `fnd31_rdsale` | MATRIX | 0.716 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | R&D Intensity. It is defined as the average of the research & development expenses in the trailing 12 months, deflated by the sum of total s |
| 358 | `fnd31_chgsgasale` | MATRIX | 0.708 | 其他 | 0 | — | — | — | UNTESTED | Change in QTR SG&A Expenses vs. Sales. It is defined as the difference between the yearly change in quarterly Selling, General and Administr |
| 359 | `fnd31_vnicw` | MATRIX | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working Capital to Inventory. It is defined as the most recent quarterly reported working capital divided by the inventory. Working capital  |
| 360 | `fnd31_qsg_additionalfactor2_ebitdadebtchg` | MATRIX | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA to long-term Debt. It is defined as the yearly change in a stock's trailing 12-month EBITDA divided by the most recently reported |
| 361 | `fnd31_divcf` | MATRIX | 0.682 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends- to-Cash Flow. It is defined as the trailing 12-month cash dividends divided by the trailing 12-month cash flow. Cash dividends re |
| 362 | `fnd31_qsg_additionalfactor_60dsigma` | MATRIX | 0.659 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock Return Volatility. It is defined as the standard deviation of a stock's monthly returns in the prior 60 days. |
| 363 | `fnd31_idb` | MATRIX | 0.658 | 其他 | 0 | — | — | — | UNTESTED | Basic Defensive Interval. It measures how many days that a company can cover its daily operating expenses (cost of goods sold and SG&A) by o |
| 364 | `fnd31_ccacw` | MATRIX | 0.603 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working Capital Accruals. It equals: Increase in Accounts Receivables + Increase in Inventory + Decrease in Accounts Payable and Accrued Lia |
| 365 | `fnd31_qsg2_additionalfactor_unfiltered_divgp` | MATRIX | 0.586 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Shareholder Payout to Gross Profit. It is defined as total dividends paid divided by (revenue - cost of goods sold). |
| 366 | `fnd31_indrelrecd_` | MATRIX | 0.579 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-adjusted Doubtful Account Receivables. It is defined as a stock's asset-adjusted annual doubtful receivables minus the average of t |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

