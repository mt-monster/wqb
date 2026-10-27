# model77 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model77` |
| 名称 | Analysts' Factor Model |
| 类别 | MODEL |
| 数据字段数(平台) | 150 |
| 覆盖率 | 0.7826 |
| 平台已有 alpha | 294 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset is a comprehensive library of quantitative alpha factors and multi-factor models designed to predict equity price movements across global markets. It includes over 350 stock selection signals spanning value, momentum, quality, growth, risk, liquidity, sentiment, and industry-specific factors, with coverage across developed, emerging, and frontier markets. The dataset provides factor definitions, cross-sectional rankings, and performance analytics, enabling users to identify key drivers of returns and construct robust, diversified investment models. By systematically evaluating fundamental, technical, and specialty signals, the dataset helps investors uncover persistent sources of excess return and improve portfolio performance through data-driven stock selection and risk manag

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **829** |
| 类型分布 | MATRIX×829 |
| 平均覆盖率 | **0.783** |
| 覆盖率区间 | 0.41 ~ 0.89 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 673 | 81.2% |
| 低 (0.50–0.70) | 152 | 18.3% |
| 稀疏 (<0.50) | 4 | 0.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 805 | 97.1% |
| UNUSABLE | 24 | 2.9% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 805 / UNUSABLE 24 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 384 | 0.78 | mdl77_qvm_rueavq_mvd、mdl77_qvm_rueavq_ve、mdl77_eur_qvm_rueavq_mvd |
| 价量与波动 | 207 | 0.80 | mdl77_qvm_pricemorank_qmaeur、mdl77_pmm_eur_composite、mdl77_pmm_indrelrtn4w_ |
| 修正与预期 | 101 | 0.80 | mdl77_qvm_eur_composite、mdl77_qvm_rue_amq、mdl77_qvm_rue_avq |
| 其他 | 72 | 0.78 | mdl77_dvm_dvm_eur_composite、mdl177_global_aci、mdl177_global_acp |
| 风险与质量 | 21 | 0.75 | mdl177_global_beta、mdl177_global_capacq、mdl177_qvm_balshtrank_qvaeur |
| 情绪与新闻 | 21 | 0.71 | mdl177_gsg_shortsentimentfactor_act_util、mdl177_gsg_shortsentimentfactor_benchmark_fee、mdl177_gsg_shortsentimentfactor_conc_ratio |
| 宏观与行业 | 19 | 0.79 | mdl177_global_cashburnrate、mdl177_global_curindbp_、mdl177_global_epschgetr |
| 搜索与替代数据 | 3 | 0.78 | mdl177_global_app、mdl177_global_rdsale、mdl77_rdsale |
| 持仓与资金流 | 1 | 0.79 | mdl77_ceroe |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl77_qvm_eur_composite` | MATRIX | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Momentum Analyst (EUR): It is defined as the aggregate of the Value Analyst (50%) and Momentum Analyst (50%) Ranks. |
| 2 | `mdl77_qvm_pricemorank_qmaeur` | MATRIX | 0.891 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Momentum Rank: It is defined as the equal weighted average of the 24-Month Active Return, 6-Month Active Return, 50-200 Day Stock Pric |
| 3 | `mdl77_qvm_rue_amq` | MATRIX | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Momentum Analyst: It is defined as the aggregate of the Price Momentum (50%), Estimate Revision (30%), and Earnings and Expected Growth (20% |
| 4 | `mdl77_pmm_eur_composite` | MATRIX | 0.891 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Momentum Model Composite |
| 5 | `mdl77_qvm_rue_avq` | MATRIX | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Analyst: It is defined as the score based on a strategy that selects for stocks in a universe of stocks by comparing different financi |
| 6 | `mdl77_qvm_rueavq_mvd` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Valuation Rank: It is defined as the aggregate of the Financial Statement Rank (40%) and Earnings Valuation Rank (60%). |
| 7 | `mdl77_qvm_rueavq_ve` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal-weighted composite of financial ratios based on a company's profits. |
| 8 | `mdl77_pmm_indrelrtn4w_` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week Industry Relative Return: It is defined as a stock's return in the last 4 weeks minus the average of the comparable returns of all st |
| 9 | `mdl77_pmm_indrelrtn5d_` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock's return in the last 5 days minus the average of the comparable returns of all stocks in the same industry, then deflated by the stand |
| 10 | `mdl77_eur_qvm_rue_amq` | MATRIX | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Momentum Analyst: It is defined as the aggregate of the Price Momentum (50%), Estimate Revision (30%), and Earnings and Expected Growth (20% |
| 11 | `mdl77_eur_qvm_pricemorank_qmaeur` | MATRIX | 0.888 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Momentum Rank: It is defined as the equal-weighted average of the 24-Month Active Return, 6-Month Active Return, 50-200 Day Stock Pric |
| 12 | `mdl77_eur_qvm_rue_avq` | MATRIX | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Analyst: It is defined as the score based on a strategy that selects for stocks in a universe of stocks by comparing different financi |
| 13 | `mdl77_eur_qvm_rueavq_mvd` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Valuation Rank: It is defined as the aggregate of the Financial Statement Rank (40%) and Earnings Valuation Rank (60%). |
| 14 | `mdl77_qvm_estrevrank_qmaeur` | MATRIX | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate Revision Rank: It is defined as the equal-weighted average of the Net Number of Fiscal Y1 Revisions, Standard Deviation of FY1 EPS  |
| 15 | `mdl77_eur_qvm_rueavq_ve` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal weighted composite of financial ratios based on company's profits. |
| 16 | `mdl77_eur_pmmm_indrelrtn5d_` | MATRIX | 0.888 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock's return in the last 5 days minus the average of the comparable returns of all stocks in the same industry, then deflated by the stand |
| 17 | `mdl77_eur_pmm_indrelrtn4w_` | MATRIX | 0.888 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week Industry Relative Return: It is defined as a stock's return in the last 4 weeks minus the average of the comparable returns of all st |
| 18 | `mdl77_eur_pmmm_indrelrtn4w_` | MATRIX | 0.888 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week Industry Relative Return: It is defined as a stock's return in the last 4 weeks minus the average of the comparable returns of all st |
| 19 | `mdl77_emm_eur_composite` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Momentum Model Composite |
| 20 | `mdl77_emm_fc_numrevy1` | MATRIX | 0.887 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Number ofRevisions for Fiscal Year 1: It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less  |
| 21 | `mdl77_pmm_actrtn6m` | MATRIX | 0.886 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-7 to month t-1. |
| 22 | `mdl77_eur_qvm_estrevrank_qmaeur` | MATRIX | 0.885 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate Revision Rank: It is defined as the equal-weighted average of the Net Number of Fiscal Y1 Revisions, Standard Deviation of FY1 EPS  |
| 23 | `mdl77_emm_fc_rev3y2` | MATRIX | 0.885 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts: It is defined as the change in the current mean consensus earnings estimate for fiscal year 2 less that o |
| 24 | `mdl77_eur_emm_fc_numrevy1` | MATRIX | 0.885 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Number ofRevisions for Fiscal Year 1: It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less  |
| 25 | `mdl77_qvm_mgtlev_qvaeur` | MATRIX | 0.885 | 盈利与财务 | 0 | — | — | — | UNTESTED | Liquidity and Leverage Rank: It is defined as the equal weighted average of Tobin Q, Change in Operating Liability Leverage and Interest Cov |
| 26 | `mdl77_pmm_p50_200ratio` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio: It is defined as the moving average of a stock's prices in the last 50 days divided by the moving average of i |
| 27 | `mdl77_eur_pmm_actrtn6m` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-7 to month t-1. |
| 28 | `mdl77_eur_pmmm_actrtn6m` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-7 to month t-1. |
| 29 | `mdl77_qvm_mgteff_qvaeur` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal weighted average of the Change in Net Operating Assets, Net Income Per Employee, Return on Equity and 1-yr Change in Price-adj TTM |
| 30 | `mdl77_dvm_dvm_eur_composite` | MATRIX | 0.883 | 其他 | 0 | — | — | — | UNTESTED | Deep Value Model Composite |
| 31 | `mdl77_rvm_eur_composite` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model composite based on an asset's worth that takes into account the value of similar assets. |
| 32 | `mdl77_eur_emm_fc_rev3y2` | MATRIX | 0.883 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts: It is defined as the change in the current mean consensus earnings estimate for fiscal year 2 less that o |
| 33 | `mdl77_dvm_roe` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity: It is defined as the trailing 12-month income before extra items divided by the average of common equity in the same perio |
| 34 | `mdl77_rvm_roe` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity: It is defined as the trailing 12-month income before extra items divided by the average of common equity in the same perio |
| 35 | `mdl77_dvm_past` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Total Assets: It is defined as a stock's month-end trading price divided by the most recent quarterly reported total assets per sha |
| 36 | `mdl77_eur_qvm_mgtlev_qvaeur` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Liquidity and Leverage Rank: It is defined as the equal-weighted average of Tobin Q, Change in Operating Liability Leverage, and Interest Co |
| 37 | `mdl77_qvm_balshtrank_qvaeur` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank: It is defined as the equal-weighted average of the Book-to-Price, Cash-to-Price, and Total Assets-to-Price Rank |
| 38 | `mdl77_qvm_finstmtrank_qvaeur` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial Statement Rank: It is defined as the equal-weighted composite of the Income Statement, Balance Sheet Strength, and TTM Operating C |
| 39 | `mdl77_qvm_incstmtrank_qvaeur` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Statement Rank: It is defined as the equal-weighted composite of the TTM Growth Flow-to-Price and TTM EBITDA-to-Enterprise Value Rank |
| 40 | `mdl77_rvm_psmtt` | MATRIX | 0.882 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Sales-to-Price: It is defined as the most recently reported trailing 12-month sales per share for a stock deflated by its month-end trad |
| 41 | `mdl77_dvm_pfgmtt` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 42 | `mdl77_rvm_pfgmtt` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 43 | `mdl77_qvm_gwthrank_qmaeur` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings and Expected Growth Rank |
| 44 | `mdl77_eur_pmm_p50_200ratio` | MATRIX | 0.881 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio: It is defined as the moving average of a stock's prices in the last 50 days divided by the moving average of i |
| 45 | `mdl77_eur_pmmm_p50_200ratio` | MATRIX | 0.881 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio: It is defined as the moving average of a stock's prices in the last 50 days divided by the moving average of i |
| 46 | `mdl77_eur_qvm_mgteff_qvaeur` | MATRIX | 0.881 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal-weighted average of the Change in Net Operating Assets, Net Income Per Employee, Return on Equity, and 1-yr Change in Price-adj TT |
| 47 | `mdl77_rvm_pe_wt` | MATRIX | 0.880 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwar |
| 48 | `mdl77_dvm_pe_wt` | MATRIX | 0.880 | 修正与预期 | 0 | — | — | — | UNTESTED | Time-Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwar |
| 49 | `mdl77_pmm_rationalalpha` | MATRIX | 0.880 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha: It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 50 | `mdl77_eur_rvm_roe` | MATRIX | 0.880 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity: It is defined as the trailing 12-month income before extra items divided by the average of common equity in the same perio |
| 51 | `mdl77_eur_dvm_roe` | MATRIX | 0.880 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity: It is defined as the trailing 12-month income before extra items divided by the average of common equity in the same perio |
| 52 | `mdl77_pmm_slope52wp` | MATRIX | 0.880 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52-Week Price Trend Line: It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52- |
| 53 | `mdl77_eur_qvm_balshtrank_qvaeur` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank: It is defined as the equal-weighted average of the Book-to-Price, Cash-to-Price, and Total Assets-to-Price Rank |
| 54 | `mdl77_eur_qvm_finstmtrank_qvaeur` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial Statement Rank: It is defined as the equal weighted composite of the Income Statement, Balance Sheet Strength and TTM Operating Ca |
| 55 | `mdl77_eur_dvm_past` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Total Assets: It is defined as a stock's month-end trading price divided by the most recent quarterly reported total assets per sha |
| 56 | `mdl77_eur_qvm_incstmtrank_qvaeur` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Statement Rank: It is defined as the equal-weighted composite of the TTM Growth Flow-to-Price and TTM EBITDA-to-Enterprise Value Rank |
| 57 | `mdl77_eur_rvm_psmtt` | MATRIX | 0.879 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Sales-to-Price: It is defined as the most recently reported trailing 12-month sales per share for a stock deflated by its month-end trad |
| 58 | `mdl77_eur_dvm_pfgmtt` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 59 | `mdl77_eur_rvm_pfgmtt` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 60 | `mdl77_eur_qvm_gwthrank_qmaeur` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings and Expected Growth Rank |
| 61 | `mdl77_dvm_pfcfmtt` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 62 | `mdl77_rvm_pfcfmtt` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 63 | `mdl77_pmm_relpricestrength_` | MATRIX | 0.878 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month Relative Price Strength: It is defined as a stock's 12-month relative price strength (PS) minus the PSs of all st |
| 64 | `mdl77_rvm_capacq` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Acquisition Ratio: It is defined as the trailing 12-month operating cash flow less than the trailing 12-month cash dividends and the |
| 65 | `mdl77_eur_dvm_pe_wt` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwar |
| 66 | `mdl77_eur_rvm_pe_wt` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwar |
| 67 | `mdl77_eur_pmm_rationalalpha` | MATRIX | 0.877 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha: It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 68 | `mdl77_eur_pmmm_rationalalpha` | MATRIX | 0.877 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha: It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 69 | `mdl77_eur_pmm_slope52wp` | MATRIX | 0.877 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52 Week Price Trend Line: It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52- |
| 70 | `mdl77_eur_pmmm_slope52wp` | MATRIX | 0.877 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52-Week Price Trend Line: It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52- |
| 71 | `mdl77_eur_dvm_pfcfmtt` | MATRIX | 0.876 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 72 | `mdl77_eur_rvm_pfcfmtt` | MATRIX | 0.876 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 73 | `mdl77_eur_pmm_relpricestrength_` | MATRIX | 0.875 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month Relative Price Strength: It is defined as a stock's 12-month relative price strength (PS) minus the PSs of all st |
| 74 | `mdl77_eur_pmmm_relpricestrength_` | MATRIX | 0.875 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month Relative Price Strength: It is defined as a stock's 12-month relative price-strength (PS) minus the PSs of all st |
| 75 | `mdl77_eur_rvm_capacq` | MATRIX | 0.875 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Acquisition Ratio: It is defined as the trailing 12-month operating cash flow less the trailing 12-month cash dividends and then div |
| 76 | `mdl77_emm_pspeghc` | MATRIX | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the most recently reported trailing 12-month earnings per share and that of 4 quarters ago for a stock, deflated by i |
| 77 | `mdl77_eur_emm_pspeghc` | MATRIX | 0.868 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the most recently reported trailing 12-month earnings per share and that of 4 quarters ago for a stock deflated by it |
| 78 | `mdl77_emm_fc_stdevfy1epsp` | MATRIX | 0.868 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY1 EPS Estimates-to-Price: It is defined as the standard deviation of a stock's analysts' individual forecasts for fiscal year 1 |
| 79 | `mdl77_eur_emm_fc_stdevfy1epsp` | MATRIX | 0.865 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY1 EPS Estimates-to-Price: It is defined as the standard deviation of a stock's analysts' individual forecasts for fiscal year 1 |
| 80 | `mdl77_pmm_actrtn24m` | MATRIX | 0.858 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-25 to month t-1. |
| 81 | `mdl77_emm_chg3yepsp` | MATRIX | 0.856 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month earnings per share and that of 12 quarters ago for a stock divided by its month-end trading pri |
| 82 | `mdl77_eur_pmm_actrtn24m` | MATRIX | 0.856 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-25 to month t-1. |
| 83 | `mdl77_eur_pmmm_actrtn24m` | MATRIX | 0.856 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-25 to month t-1. |
| 84 | `mdl77_eur_emm_chg3yepsp` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month earnings per share and that of 12 quarters ago for a stock divided by its month-end trading pri |
| 85 | `mdl77_emm_mrspe_cf` | MATRIX | 0.846 | 修正与预期 | 0 | — | — | — | UNTESTED | The 3-month change in analysts' median earnings forecast for a stock's fiscal 1 scaled by the current mean estimate. |
| 86 | `global_cash_to_liabilities_ratio` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash and equivalents to current liabilities, calculated using a fixed method for global coverage. |
| 87 | `mdl177_global_aci` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Abnormal capital investment |
| 88 | `mdl177_global_acp` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Average collection period: TTM accounts receivable × 365 divided by TTM sales |
| 89 | `mdl177_global_acqmul` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition multiple; most recent quarterly invested capital divided by trailing 12-month EBITDA |
| 90 | `mdl177_global_actrtn12m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-month active return with a 1-month lag |
| 91 | `mdl177_global_actrtn18m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 18-month active return with a one-month lag percent change in stock price from month t-19 to t-1 |
| 92 | `mdl177_global_actrtn1m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-month active return; percent change in stock price from month t-1 to t |
| 93 | `mdl177_global_actrtn24m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Active return over the past 24 months with a 1-month lag (price change from t-25 to t-1) |
| 94 | `mdl177_global_actrtn2m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 2-month active return; percent change in stock price from month t-2 to t |
| 95 | `mdl177_global_actrtn36m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 36-month active return |
| 96 | `mdl177_global_actrtn3m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-month active return; percent change in stock price from month t-3 to t |
| 97 | `mdl177_global_actrtn60m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 60‑month active return with a 1‑month lag (price change from t‑61 to t‑1) |
| 98 | `mdl177_global_actrtn6m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Six-month active return; percent change in stock price over the last six months |
| 99 | `mdl177_global_actrtn9m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 9-month active return with a 1-month lag; percent change in price from month t-10 to t-1 |
| 100 | `mdl177_global_alpha60m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month alpha: intercept from regression of the stock’s monthly returns against the S&P 500 over the last 60 months |
| 101 | `mdl177_global_app` | MATRIX | 0.845 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Average payable period: trailing 12-month accounts payable × 365 divided by trailing 12-month cost of goods sold |
| 102 | `mdl177_global_aqi` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset Quality Index : It is defined as the year-over-year change of 1 minus the ratio of current assets plus PP&E divided by total assets |
| 103 | `mdl177_global_aspanratio` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock's quarterly operating assets minus its operating liabilities deflated by the lagged total assets |
| 104 | `mdl177_global_astcomp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset Composition; total current assets from the most recent quarter divided by total assets from the most recent quarter |
| 105 | `mdl177_global_astto` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover ratio (trailing 12-month sales divided by most recent total assets) |
| 106 | `mdl177_global_bdi` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Baltic Dry Index (global shipping and freight activity index) |
| 107 | `mdl177_global_beta` | MATRIX | 0.845 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta coefficient measuring the stock’s sensitivity to market movements |
| 108 | `mdl177_global_betasigma` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of beta and sigma; adjusted 60-month beta multiplied by 60-month volatility of monthly returns |
| 109 | `mdl177_global_booklev` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book leverage: total assets divided by book equity |
| 110 | `mdl177_global_bp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-price ratio |
| 111 | `mdl177_global_capacq` | MATRIX | 0.845 | 风险与质量 | 0 | — | — | — | UNTESTED | Capital acquisition ratio (management quality measure) |
| 112 | `mdl177_global_capexast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month capital expenditures divided by total assets |
| 113 | `mdl177_global_capexsale` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Trailing 12-month capital expenditures divided by trailing 12-month sales |
| 114 | `mdl177_global_cashburnrate` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rate at which a company burns cash; lower values indicate better long-term cash generation |
| 115 | `mdl177_global_cashc` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Cash conversion cycle; average inventory days plus collection days minus payable days |
| 116 | `mdl177_global_cashp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash and equivalents per share divided by share price |
| 117 | `mdl177_global_cashratio` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash to current liabilities ratio |
| 118 | `mdl177_global_cashsale` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-sales; average cash and equivalents over the trailing 12 months divided by trailing 12-month sales |
| 119 | `mdl177_global_cashsev` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Total cash and equivalents divided by enterprise value |
| 120 | `mdl177_global_ccd` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow debt coverage ratio: operating cash flow minus dividends divided by interest-bearing debt |
| 121 | `mdl177_global_cfita` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12‑month cash flow from investing divided by average total assets |
| 122 | `mdl177_global_cfleverage` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Leverage: total liabilities divided by trailing 12-month operating cash flow |
| 123 | `mdl177_global_cfroi` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Return on Invested Capital: trailing 12-month cash flow divided by average invested capital |
| 124 | `mdl177_global_cg3ysales` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | 3-year compound annual sales growth per share over the last 12 quarters |
| 125 | `mdl177_global_chg3ycfast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year change in the cash flow-to-assets ratio |
| 126 | `mdl177_global_chg3ycfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in price-adjusted trailing 12-month cash flow per share |
| 127 | `mdl177_global_chg3yepsast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3‑year change in assets‑adjusted trailing 12‑month EPS |
| 128 | `mdl177_global_chg3yepsp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Three-year change in price-adjusted TTM EPS, current EPS minus EPS 12 quarters ago divided by price |
| 129 | `mdl177_global_chg3yfcfast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in assets-adjusted TTM free cash flow (current minus 12 quarters ago, scaled by assets) |
| 130 | `mdl177_global_chg3yfcfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in price-adjusted trailing 12-month free cash flow; current FCF minus FCF 12 quarters ago, divided by price |
| 131 | `mdl177_global_chg3yocfast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in assets-adjusted trailing 12-month operating cash flow |
| 132 | `mdl177_global_chg3yocfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the the trailing 12-month operating cash flow per share and that of 12-quarters ago for a stock divided by its tradin |
| 133 | `mdl177_global_chg6malpha18m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 18-Month Alpha : It is defined as the 6-month change in a stock's 18-month alpha, which equals the intercept from  |
| 134 | `mdl177_global_chg6mltg` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Six-month percent change in long-term growth forecasts |
| 135 | `mdl177_global_chgalpha12m` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Change in 12‑month alpha (regression intercept) over the last 6 months |
| 136 | `mdl177_global_chgalpha36m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Six-month change in the 36-month regression alpha of stock returns versus the market |
| 137 | `mdl177_global_chgars` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in accounts receivable as a percentage of sales |
| 138 | `mdl177_global_chgcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in assets-adjusted trailing 12-month cash flow; difference in TTM cash flow over the last year scaled by assets |
| 139 | `mdl177_global_chgcfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | One-year change in price-adjusted trailing 12-month cash flow per share; difference over last year divided by price |
| 140 | `mdl177_global_chgeps` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share |
| 141 | `mdl177_global_chgepsp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | One-year change in price-adjusted TTM EPS (difference over last year divided by price) |
| 142 | `mdl177_global_chgfcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Chg in Assets-adj TTM Free Cash Flow : It is defined as the the trailing 12-month free cash flow minus 4 quarter ago trailing 12-month  |
| 143 | `mdl177_global_chgfcfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | One-year change in price-adjusted TTM free cash flow (difference over last year divided by price) |
| 144 | `mdl177_global_chgis` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | 1‑year change in quarterly inventory‑to‑sales ratio |
| 145 | `mdl177_global_chgnoa` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year‑over‑year change in net operating assets |
| 146 | `mdl177_global_chgnpm` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net profit margin |
| 147 | `mdl177_global_chgocf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in assets-adjusted trailing 12-month operating cash flow |
| 148 | `mdl177_global_chgocfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in price-adjusted TTM operating cash flow |
| 149 | `mdl177_global_chgollev` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage; difference over 4 quarters |
| 150 | `mdl177_global_chgopm` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating profit margin; difference over the last four quarters |
| 151 | `mdl177_global_chgreccast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accounts receivable to current assets ratio |
| 152 | `mdl177_global_chgsgasale` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Change in quarterly SG&A expenses relative to sales; difference in SG&A-to-sales ratios |
| 153 | `mdl177_global_chgshare` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Change in shares outstanding |
| 154 | `mdl177_global_chgvolpre4y` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 4‑year change in average trading volume (6‑month moving average of monthly turnover) |
| 155 | `mdl177_global_cogsinvt` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Change in TTM COGS vsInventory Level : It is defined as the absolute value of the difference between the yearly percent change in trailing 1 |
| 156 | `mdl177_global_covol` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month trading volume trend; slope of the regression line of the last 60 months’ trading volume |
| 157 | `mdl177_global_curindbp_` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry‑relative book‑to‑market ratio |
| 158 | `mdl177_global_curindcfp_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative trailing 12-month cash flow-to-price ratio |
| 159 | `mdl177_global_curinddivp_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry‑relative trailing 12‑month dividend yield |
| 160 | `mdl177_global_curindebitdap_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative TTM EBITDA-to-price; EBITDA-to-price minus industry average, deflated by industry standard deviation |
| 161 | `mdl177_global_curindep_` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative TTM EPS-to-price ratio |
| 162 | `mdl177_global_curindfcfp_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative trailing 12-month free cash flow to price ratio |
| 163 | `mdl177_global_curindocfp_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative trailing 12-month operating cash flow-to-price ratio |
| 164 | `mdl177_global_curindocfta_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative TTM operating cash flow-to-total assets (standardized vs industry) |
| 165 | `mdl177_global_curindsp_` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative trailing 12-month sales to price ratio |
| 166 | `mdl177_global_curratio` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio (current assets divided by current liabilities) |
| 167 | `mdl177_global_cvpre90dp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | CV of Prior 90-Day Closing Prices : It is defined as the standard deviation of a stock's last 90 days closing prices divided by the mean of  |
| 168 | `mdl177_global_cvvolp20d` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-Day Volume Volatility to Price Volatility : It is defined as the coefficient of variation of the last 20 days of closing prices divided b |
| 169 | `mdl177_global_de` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt-to-equity; most recent long-term debt divided by total book equity |
| 170 | `mdl177_global_debtcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt-to-cash flow; total interest-bearing debt divided by trailing 12-month cash flow |
| 171 | `mdl177_global_dfl` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | The sum of the trailing 12-month pretax income and the trailing 12-month interest expense divided by the trailing 12-month pretax income. |
| 172 | `mdl177_global_div5yg` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year dividend growth rate |
| 173 | `mdl177_global_divcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends-to-cash flow ratio (TTM dividends divided by cash flow) |
| 174 | `mdl177_global_divcov` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend coverage ratio, trailing 12 month operating earnings divided by dividends |
| 175 | `mdl177_global_divyield` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield |
| 176 | `mdl177_global_dpcapex` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Absolute difference between percent change in depreciation and capital expenditure (TTM) |
| 177 | `mdl177_global_ebitdaev` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA divided by enterprise value |
| 178 | `mdl177_global_ebitdap` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Price : It is defined as the trailing 12-month earnings before interest, taxes, depreciation and amortization for a company di |
| 179 | `mdl177_global_epschgetr` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS from Change in Effective Tax Rate : It is defined as the trailing 12-month pre-tax income per share times the difference between most re |
| 180 | `mdl177_global_equityto` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity turnover ratio (sales divided by average book equity) |
| 181 | `mdl177_global_fc_curindfwdep_` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Industry‑relative next 4‑quarter EPS estimates‑to‑price ratio |
| 182 | `mdl177_global_fc_cvfy1eps` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of FY1 EPS estimates |
| 183 | `mdl177_global_fc_cvfy2eps` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | FY2 EPS forecast dispersion: standard deviation of analyst estimates divided by the mean |
| 184 | `mdl177_global_fc_dypeg` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of the dividend-yield–adjusted PEG ratio |
| 185 | `mdl177_global_fc_ebop` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Edwards-Bell-Ohlson model value-to-price; intrinsic value from EBO model divided by market price |
| 186 | `mdl177_global_fc_egp` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Inverse of PEG ratio: next 4-quarter earnings estimate times long-term growth rate, scaled by price |
| 187 | `mdl177_global_fc_epsrm` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision magnitude: 3-month change in median FY1 consensus EPS estimate, scaled |
| 188 | `mdl177_global_fc_estep` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leading 12-month median earnings yield |
| 189 | `mdl177_global_fc_f12mepssev` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Forward 12-month EPS-to-enterprise value ratio |
| 190 | `mdl177_global_fc_fcfp` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward free cash flow to price using next four-quarter estimates plus depreciation minus capex |
| 191 | `mdl177_global_fc_fcfroey1p` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Product of TTM free cash flow yield and forward ROE; TTM FCF per share times next four-quarter earnings forecast divided by most recent book |
| 192 | `mdl177_global_fc_fwdep` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-month mean earnings yield; next four quarters’ mean EPS estimate divided by price |
| 193 | `mdl177_global_fc_fwdroe` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward return on equity: next four-quarter earnings estimate divided by recent common equity |
| 194 | `mdl177_global_fc_hlep` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision confidence: sum of 3-month changes in highest and lowest FY1 EPS estimates, scaled |
| 195 | `mdl177_global_fc_numest` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing FY1 earnings estimates |
| 196 | `mdl177_global_fc_numrevy1` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Net number of revenue estimate revisions for fiscal year 1 |
| 197 | `mdl177_global_fc_pdy` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted dividend yield |
| 198 | `mdl177_global_fc_rel5yfwdep` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year relative forward earnings yield, current next four-quarter earnings-to-price versus its five-year average |
| 199 | `mdl177_global_fc_rev3y1` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY1 EPS forecasts; change in current FY1 forecast versus three months ago, scaled |
| 200 | `mdl177_global_fc_rev3y2` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY2 EPS forecasts; change in FY2 earnings forecast since three months ago, scaled by price |
| 201 | `mdl177_global_fc_rev6` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month revision in EPS estimates |
| 202 | `mdl177_global_fc_stdevfy1epsp` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY1 EPS estimates scaled by price |
| 203 | `mdl177_global_fc_stdevfy2epsp` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY2 EPS estimates scaled by price |
| 204 | `mdl177_global_fc_y2aepsg` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Two-year ahead EPS growth: forecast EPS for fiscal year 2 minus year 1, scaled by price |
| 205 | `mdl177_global_fcfequity` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month free cash flow to equity |
| 206 | `mdl177_global_fcfroi` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow Return on Investment |
| 207 | `mdl177_global_fcfsale` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-TTM Sales : It is defined as the trailing 12-month free cash flow divided by the trailing 12-month sales. |
| 208 | `mdl177_global_ff10mrtn` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French Momentum : It is defined as the percent change in a stock's price from month t-12 to month t-2. |
| 209 | `mdl177_global_fixastto` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fixed assets turnover; trailing 12-month sales divided by total fixed assets |
| 210 | `mdl177_global_flowratio` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow Ratio: (current assets minus cash and equivalents) divided by (current liabilities minus short-term debt) |
| 211 | `mdl177_global_gear` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital gearing ratio: long-term debt divided by total assets minus current liabilities |
| 212 | `mdl177_global_high52w` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-week high ratio: month-end price divided by the highest monthly close in the past 12 months |
| 213 | `mdl177_global_indrelcroe_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry‑adjusted quarterly return on equity |
| 214 | `mdl177_global_indrelrecd_` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted Doubtful Account Receivables; asset-adjusted annual doubtful receivables minus industry mean |
| 215 | `mdl177_global_indrelrtn4w_` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative 4-week return, stock return minus industry average scaled by industry standard deviation |
| 216 | `mdl177_global_indrelrtn5d_` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day industry-relative return; stock return over the last 5 days minus industry average, scaled by industry standard deviation |
| 217 | `mdl177_global_intcov` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Interest coverage ratio |
| 218 | `mdl177_global_invast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inventory to total assets ratio |
| 219 | `mdl177_global_invto` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Inventory Turnover Ratio : It is defined as the trailing 12-month cost of goods sold divided by the average of inventory in the same period. |
| 220 | `mdl177_global_lagegp` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Lagged inverse PEG ratio |
| 221 | `mdl177_global_liqcoeff` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity Coefficient : It is the slope of the regression between the monthly stock trading turnover ratio (X) and the contemporary monthly  |
| 222 | `mdl177_global_ltg` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long-term growth rate forecast (I/B/E/S) |
| 223 | `mdl177_global_milliq` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock illiquidity |
| 224 | `mdl177_global_mktcappera` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Market capitalization per covering analyst |
| 225 | `mdl177_global_mktlev` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock's total market value plus the most recent reported quarterly book debt then divided by the market value. |
| 226 | `mdl177_global_navp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Asset Value to Price : It is defined as the most recent book value of net assets per share (NAV) by the closing priceNAV is calculated i |
| 227 | `mdl177_global_ncfeps` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM EPS vsOper Cash Flows : It is defined as the absolute value of the difference between the yearly percent change in trailing 12 |
| 228 | `mdl177_global_netcashp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Cash to Equity : It is defined as most recently reported quarterly cash & equivalents less the long-term debt and current debt for a sto |
| 229 | `mdl177_global_netdebt` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt: total debt minus cash and cash equivalents |
| 230 | `mdl177_global_nfaldebt` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net fixed assets to long-term debt |
| 231 | `mdl177_global_niper` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee; net income divided by number of employees |
| 232 | `mdl177_global_nlassets` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural logarithm of total assets |
| 233 | `mdl177_global_nlmktcap` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of market capitalization |
| 234 | `mdl177_global_nlprice` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural logarithm of closing price |
| 235 | `mdl177_global_nlsales` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of trailing twelve months sales |
| 236 | `mdl177_global_nlvolcap` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Net monthly liquidity volatility based on market-cap liquidity and risk |
| 237 | `mdl177_global_nnastp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net current assets-to-price ratio |
| 238 | `mdl177_global_noato` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating asset turnover |
| 239 | `mdl177_global_nopatmargin` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating profit after tax margin |
| 240 | `mdl177_global_npm` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin |
| 241 | `mdl177_global_ocfast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow to assets |
| 242 | `mdl177_global_ocfmargin` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow margin, operating cash flow divided by revenue |
| 243 | `mdl177_global_ocfratio` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow Ratio : It is defined as a stock's most recently reported quarterly cash flow from operations divided by its current lia |
| 244 | `mdl177_global_ocfroi` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow return on invested capital |
| 245 | `mdl177_global_ollev` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Liability Leverage; ratio of operating liabilities to operating assets, indicating reliance on supplier financing |
| 246 | `mdl177_global_opincltd` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM Oper Income vsLT Debt : It is defined as the difference between the yearly percent change in operating income and the yearly p |
| 247 | `mdl177_global_oplev` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Operating Leverage : It is defined as the percent change in the trailing 12-month operating income from previous quarter divided by the perc |
| 248 | `mdl177_global_opmb` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit Margin |
| 249 | `mdl177_global_p50_200ratio` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of the 50-day moving average price to the 200-day moving average price |
| 250 | `mdl177_global_past` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-total assets ratio |
| 251 | `mdl177_global_pctabv260low` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage above the lowest trading price in the last 260 trading days |
| 252 | `mdl177_global_pctchg3ycf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing 12-month cash flow over 3 years |
| 253 | `mdl177_global_pctchg3yeps` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year growth in trailing-twelve-month earnings per share |
| 254 | `mdl177_global_pctchg3yfcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year percent change in TTM free cash flow |
| 255 | `mdl177_global_pctchg3yocf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing 12-month operating cash flow over 3 years |
| 256 | `mdl177_global_pctchgastto` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | One-year change in asset turnover ratio |
| 257 | `mdl177_global_pctchgcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in trailing 12-month cash flow |
| 258 | `mdl177_global_pctchgeps` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | One-year growth in trailing twelve month earnings per share |
| 259 | `mdl177_global_pctchgfcf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in free cash flow (historical growth) |
| 260 | `mdl177_global_pctchgocf` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in trailing 12-month operating cash flow |
| 261 | `mdl177_global_pctchgqtrast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in total assets |
| 262 | `mdl177_global_pctchgqtrsales` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year percent change in quarterly sales |
| 263 | `mdl177_global_pcurlia` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities-to-price |
| 264 | `mdl177_global_perg` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG Ratio : It is defined as the stock price divided by the leading 12-month consensus earnings forecast, scaled by the averag |
| 265 | `mdl177_global_pinoa` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax return on net operating assets |
| 266 | `mdl177_global_pr_1536` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 15/36 Week Stock Price Ratio : It is defined as the moving average of a stock's prices in last 15-week divided by the moving average of its  |
| 267 | `mdl177_global_pr_30w75w` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 30-75 week stock price ratio; moving average of last 30 weeks’ prices divided by last 75 weeks’ prices |
| 268 | `mdl177_global_qr` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Quick ratio |
| 269 | `mdl177_global_rationalalpha` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha : It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from  |
| 270 | `mdl177_global_ratrev6m` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Six-month average change in analyst recommendations (street rating revision) |
| 271 | `mdl177_global_rdsale` | MATRIX | 0.845 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | R&D intensity (research and development expense divided by sales) |
| 272 | `mdl177_global_reinrate` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate (proportion of earnings/cash reinvested into the business) |
| 273 | `mdl177_global_rel5ybp` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Five-year relative book-to-market measure |
| 274 | `mdl177_global_rel5ycfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year relative TTM cash flow to price |
| 275 | `mdl177_global_rel5ydivp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative TTM dividend yield |
| 276 | `mdl177_global_rel5yebitdap` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative TTM EBITDA-to-price measure |
| 277 | `mdl177_global_rel5yep` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year relative TTM earnings-to-price ratio |
| 278 | `mdl177_global_rel5yfcfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year Relative TTM Free Cash Flow-to-Price |
| 279 | `mdl177_global_rel5yocfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative TTM Operating Cash Flow-to-Price |
| 280 | `mdl177_global_rel5ysp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative trailing sales-to-price ratio |
| 281 | `mdl177_global_relpricestrength_` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength |
| 282 | `mdl177_global_reoa` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings to total assets ratio |
| 283 | `mdl177_global_rerror60m` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Regression residual error from a 60-month CAPM regression |
| 284 | `mdl177_global_revper` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee |
| 285 | `mdl177_global_roa` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets |
| 286 | `mdl177_global_roe` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity |
| 287 | `mdl177_global_roic` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on Invested Capital |
| 288 | `mdl177_global_rsi26w` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 26-week relative price strength, recent weekly close divided by weekly close 26 weeks ago |
| 289 | `mdl177_global_rtn2nd6m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Return over the second 6-month period (momentum) |
| 290 | `mdl177_global_rtn39w` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-week return with a 4-week lag |
| 291 | `mdl177_global_saleeps` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM Sales vsEPS : It is defined as the absolute value of the difference between the yearly percent change in trailing 12-month sal |
| 292 | `mdl177_global_saleg5y` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Five-year sales growth |
| 293 | `mdl177_global_salegpm` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in QTR Sales vsGross Margin : It is defined as the difference between the yearly change in most recent reported quarterly sales and t |
| 294 | `mdl177_global_salerec` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to accounts receivable |
| 295 | `mdl177_global_sga` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Selling, General, and Administrative expenses |
| 296 | `mdl177_global_sigma` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of returns (volatility) |
| 297 | `mdl177_global_skew90cortn` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day stock daily excess returns |
| 298 | `mdl177_global_skew90drtn` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of daily stock returns over the past 90 days |
| 299 | `mdl177_global_slope52wp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 52-week price trend line |
| 300 | `mdl177_global_slope66wp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 66-week price trend line (4-week lagged slope from least squares regression of last 66 weekly prices) |
| 301 | `mdl177_global_stockrating` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Consensus Rating : It is defined as the consensus recommendation for a company. |
| 302 | `mdl177_global_surp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings surprise: actual EPS minus forecast, scaled by price |
| 303 | `mdl177_global_susgrowth` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sustainable growth rate |
| 304 | `mdl177_global_swc` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-trailing 12-month sales |
| 305 | `mdl177_global_tobinq` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin’s Q ratio: market value of equity plus debt divided by total assets |
| 306 | `mdl177_global_totalcov` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total coverage ratio: TTM operating income before depreciation divided by annualized cash dividends plus interest expense |
| 307 | `mdl177_global_totalsaleg` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly trailing twelve-month total sales growth rate |
| 308 | `mdl177_global_tstalp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year price momentum indicator |
| 309 | `mdl177_global_ttmaccu` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month accruals (earnings quality measure) |
| 310 | `mdl177_global_ttmcapexp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing twelve month capital expenditures divided by price |
| 311 | `mdl177_global_ttmcfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month cash flow from operations |
| 312 | `mdl177_global_ttmepa` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | An indicator that standardizes and compares relative share price between time periods and among companies. |
| 313 | `mdl177_global_ttmepb` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | The company's performance in trailing 1-year before taking into account of non-recurring gain or loss.stock divided by its month-end trading |
| 314 | `mdl177_global_ttmfcfev` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Enterprise Value : It is defined as the trailing 12-month free cash flow (FCF) for a stock scaled by its enterprise va |
| 315 | `mdl177_global_ttmfcfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve month free cash flow to price |
| 316 | `mdl177_global_ttmgfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month growth flow-to-price ratio (GAAP earnings plus R&D scaled by market value) |
| 317 | `mdl177_global_ttmocfp` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12‑month operating cash flow‑to‑price |
| 318 | `mdl177_global_ttmpiqp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month pre-tax income per share scaled by price |
| 319 | `mdl177_global_ttmsaleev` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Trailing twelve months Sales-to-Enterprise Value ratio |
| 320 | `mdl177_global_ttmsp` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-price ratio |
| 321 | `mdl177_global_tw_ep` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield : This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwa |
| 322 | `mdl177_global_uap` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Unexpected change in accounts payable |
| 323 | `mdl177_global_uar` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Unexpected accounts receivable |
| 324 | `mdl177_global_udep` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Unexpected change in depreciation |
| 325 | `mdl177_global_uinv` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Unexpected change in inventory level |
| 326 | `mdl177_global_var24m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Value at Risk : It is defined as the minimum of a stock's monthly price return in last 20-month period. |
| 327 | `mdl177_global_varresirtn` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month residual return variance (idiosyncratic volatility) |
| 328 | `mdl177_global_visiratio` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Visibility Ratio: most recent daily trading volume divided by average daily trading volume over the last 50 trading days |
| 329 | `mdl177_global_volpre6m` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | The 6 month moving average of average monthly turnover ratio. |
| 330 | `mdl177_global_volto` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading turnover ratio |
| 331 | `mdl177_global_wcacc` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital accruals (earnings quality measure) |
| 332 | `mdl177_global_wcast` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital to total assets ratio |
| 333 | `mdl177_global_wcinv` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working Capital to Inventory : It is defined as the most recent quarterly reported working capital divided by the inventoryWorking capital i |
| 334 | `mdl177_global_yoychgaa` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Accruals to Assets : It is defined as the trailing 12-month income before extra items less the trailing 12-month operating cash fl |
| 335 | `mdl177_global_yoychgcr` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio |
| 336 | `mdl177_global_yoychgda` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year Change in Leverage : It is defined as the difference between the most recent reported quarterly total liabilities as a percen |
| 337 | `mdl177_global_yoychggpm` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin |
| 338 | `mdl177_global_yoychgroa` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets |
| 339 | `mdl77_eur_emm_mrspe_cf` | MATRIX | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | The 3-month change in analysts' median earnings forecast for a stock's fiscal 1 scaled by the current mean estimate. |
| 340 | `mdl177_qvm_balshtrank_qvaeur` | MATRIX | 0.843 | 风险与质量 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank |
| 341 | `mdl177_qvm_dvm_qvaeur` | MATRIX | 0.843 | 风险与质量 | 0 | — | — | — | UNTESTED | Valuation Rank |
| 342 | `mdl177_qvm_estrevrank_qmaeur` | MATRIX | 0.843 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate Revision Rank |
| 343 | `mdl177_qvm_ev_qvaeur` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Valuation Rank |
| 344 | `mdl177_qvm_finstmtrank_qvaeur` | MATRIX | 0.843 | 风险与质量 | 0 | — | — | — | UNTESTED | Financial Statement Rank |
| 345 | `mdl177_qvm_gwthrank_qmaeur` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings and  Expected Growth Rank |
| 346 | `mdl177_qvm_incstmtrank_qvaeur` | MATRIX | 0.843 | 风险与质量 | 0 | — | — | — | UNTESTED | Income Statement Rank |
| 347 | `mdl177_qvm_mgteff_qvaeur` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability &  Earnings Quality Rank |
| 348 | `mdl177_qvm_mgtlev_qvaeur` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity and Leverage Rank |
| 349 | `mdl177_qvm_pricemorank_qmaeur` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Momentum Rank |
| 350 | `mdl177_qvm_qma_eur` | MATRIX | 0.843 | 修正与预期 | 0 | — | — | — | UNTESTED | Momentum Analyst |
| 351 | `mdl177_qvm_qva_eur` | MATRIX | 0.843 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Analyst |
| 352 | `mdl177_pmm_actrtn24m_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month active return with a 1-month lag: percent change in stock price from month t-25 to t-1 |
| 353 | `mdl177_pmm_actrtn24m_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month active return with one-month lag: percent change in stock price from month t-25 to t-1 |
| 354 | `mdl177_pmm_actrtn6m_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag : It is defined the percent change in price for a stock from month t-7 to month t-1. |
| 355 | `mdl177_pmm_actrtn6m_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag : It is defined the percent change in price for a stock from month t-7 to month t-1. |
| 356 | `mdl177_pmm_indrelrtn4w_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 4-week return: stock’s 4-week return minus its industry average, scaled by the industry’s standard deviation |
| 357 | `mdl177_pmm_indrelrtn4w_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative 4-week return: stock’s 4-week return minus its industry average, scaled by the industry’s return standard deviation |
| 358 | `mdl177_pmm_indrelrtn5d_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 5-day return: stock’s 5-day return minus its industry average, scaled by the industry’s standard deviation |
| 359 | `mdl177_pmm_p50_200ratio_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio : It is defined as the moving average of a stock's prices in last 50 days divided by the moving average of its  |
| 360 | `mdl177_pmm_p50_200ratio_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of the 50-day moving average to the 200-day moving average of the stock price, indicating short- versus long-term trend alignment |
| 361 | `mdl177_pmm_rationalalpha_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha : It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from  |
| 362 | `mdl177_pmm_rationalalpha_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha : It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from  |
| 363 | `mdl177_pmm_relpricestrength_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength: stock’s 12-month price strength minus the industry average, scaled by industry standard  |
| 364 | `mdl177_pmm_relpricestrength_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength: stock’s 12-month price strength minus the industry average, deflated by the industry sta |
| 365 | `mdl177_pmm_slope52wp_2` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 52-week price trend line, typically from a regression of price on time, indicating trend direction and strength over the past y |
| 366 | `mdl177_pmm_slope52wp_3` | MATRIX | 0.843 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52 Week Price Trend Line : It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52 |
| 367 | `mdl177_emm_chg3yepsp_2` | MATRIX | 0.841 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-year change in trailing-twelve-month EPS, current TTM EPS minus TTM EPS 12 quarters ago, divided by stock price |
| 368 | `mdl177_emm_chgepsp_2` | MATRIX | 0.841 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year change in trailing-twelve-month EPS over the last year, divided by stock price |
| 369 | `mdl177_emm_fc_dypeg_2` | MATRIX | 0.841 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of the dividend-yield-adjusted PEG ratio |
| 370 | `mdl177_emm_fc_epsrm` | MATRIX | 0.841 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Revision Magnitude: 3-month change in the median FY1 consensus EPS estimate, scaled |
| 371 | `mdl177_emm_fc_numrevy1` | MATRIX | 0.841 | 修正与预期 | 0 | — | — | — | UNTESTED | Net # of Revisions for Fiscal Year 1 : It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less the |
| 372 | `mdl177_emm_fc_rev3y2_2` | MATRIX | 0.841 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month change in FY2 consensus EPS forecast, scaled by price |
| 373 | `mdl177_emm_fc_stdevfy1epsp_2` | MATRIX | 0.841 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY1 EPS Estimates-to-Price |
| 374 | `mdl177_dvm_chgollev` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage over the last four quarters |
| 375 | `mdl177_dvm_ebitdaev` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month EBITDA to Enterprise Value |
| 376 | `mdl177_dvm_past` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Total Assets ratio |
| 377 | `mdl177_dvm_roe` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity |
| 378 | `mdl177_dvm_ttmfcfp` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month Free Cash Flow to Price ratio |
| 379 | `mdl177_dvm_ttmgfp` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month Growth Flow-to-Price ratio, defined as last four quarters GAAP earnings plus R&D expenses scaled by market value |
| 380 | `mdl177_dvm_tw_ep` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield (earnings-to-price ratio with time weighting) |
| 381 | `mdl177_rvm_capacq` | MATRIX | 0.840 | 其他 | 0 | — | — | — | UNTESTED | Capital Acquisition Ratio |
| 382 | `mdl177_rvm_ebitdaev` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA-to-Enterprise Value ratio based on trailing twelve months |
| 383 | `mdl177_rvm_roe` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity (net income divided by shareholders’ equity) |
| 384 | `mdl177_rvm_ttmfcfp` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month Free Cash Flow-to-Price |
| 385 | `mdl177_rvm_ttmgfp` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price : It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tr |
| 386 | `mdl177_rvm_ttmsp` | MATRIX | 0.840 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month Sales-to-Price (inverse of P/S) |
| 387 | `mdl177_rvm_tw_ep` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield (earnings-to-price ratio) |
| 388 | `mdl177_sensitivityfactor_apsales` | MATRIX | 0.836 | 宏观与行业 | 0 | — | — | — | UNTESTED | Proportion of company sales from the Asia-Pacific region |
| 389 | `mdl177_sensitivityfactor_ceroe` | MATRIX | 0.836 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Earnings Return on Equity |
| 390 | `mdl177_sensitivityfactor_crp` | MATRIX | 0.836 | 价量与波动 | 0 | — | — | — | UNTESTED | Credit Risk Premium: change in yield spread between Moody's BAA and AAA bond indices (CRP_t − CRP_t−1) |
| 391 | `mdl177_sensitivityfactor_da` | MATRIX | 0.836 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt to total assets leverage ratio |
| 392 | `mdl177_sensitivityfactor_emeasales` | MATRIX | 0.836 | 宏观与行业 | 0 | — | — | — | UNTESTED | Proportion of company sales from the Europe, Middle East and Africa region |
| 393 | `mdl177_sensitivityfactor_hs` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | Housing Starts: percentage change in new residential housing units ((HS_t / HS_t−1) − 1) × 100 |
| 394 | `mdl177_sensitivityfactor_inflation` | MATRIX | 0.836 | 宏观与行业 | 0 | — | — | — | UNTESTED | Inflation Sensitivity |
| 395 | `mdl177_sensitivityfactor_ip` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | Industrial Production: percentage change in industrial output ((IP_t / IP_t−1) − 1) × 100 |
| 396 | `mdl177_sensitivityfactor_lasales` | MATRIX | 0.836 | 宏观与行业 | 0 | — | — | — | UNTESTED | Proportion of company sales from the Latin America region |
| 397 | `mdl177_sensitivityfactor_nasales` | MATRIX | 0.836 | 宏观与行业 | 0 | — | — | — | UNTESTED | Proportion of company sales from the North America region |
| 398 | `mdl177_sensitivityfactor_oilprice` | MATRIX | 0.836 | 价量与波动 | 0 | — | — | — | UNTESTED | Beta coefficient measuring the stock’s sensitivity to oil price changes |
| 399 | `mdl177_sensitivityfactor_usd` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | US Dollar Value Sensitivity |
| 400 | `mdl177_sensitivityfactor_vix` | MATRIX | 0.836 | 价量与波动 | 0 | — | — | — | UNTESTED | CBOE Volatility Index (market volatility measure) |
| 401 | `mdl177_sensitivityfactor_yieldsprd` | MATRIX | 0.836 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity to the yield curve slope (beta to yield spread) |
| 402 | `mdl177_pmm_pmm_eur_composite_alt` | MATRIX | 0.830 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Momentum (EUR) |
| 403 | `mdl177_qvm_dvm_qvaeur_alt` | MATRIX | 0.830 | 风险与质量 | 0 | — | — | — | UNTESTED | Valuation Rank |
| 404 | `mdl177_qvm_pricemorank_qmaeur_alt` | MATRIX | 0.830 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Momentum Rank |
| 405 | `mdl177_qvm_qma_eur_alt` | MATRIX | 0.830 | 修正与预期 | 0 | — | — | — | UNTESTED | Momentum Analyst |
| 406 | `mdl177_qvm_qva_eur_alt` | MATRIX | 0.830 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Analyst |
| 407 | `mdl177_qvm_qvm_eur_composite_alt` | MATRIX | 0.830 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Momentum Analyst (EUR) |
| 408 | `mdl177_qvm_ev_qvaeur_alt` | MATRIX | 0.830 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Valuation Rank |
| 409 | `mdl177_pmm_indrelrtn5d__alt` | MATRIX | 0.830 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day Industry Relative Return: stock return over the last 5 trading days minus the industry average, scaled by the industry standard deviat |
| 410 | `mdl177_pmm_indrelrtn4w_alt` | MATRIX | 0.830 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week Industry Relative Return: stock return over the last 4 weeks minus the industry average, scaled by the industry standard deviation |
| 411 | `mdl177_emm_emm_eur_composite_alt` | MATRIX | 0.829 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Momentum (EUR) |
| 412 | `mdl177_emm_fc_numrevy1_alt` | MATRIX | 0.829 | 修正与预期 | 0 | — | — | — | UNTESTED | Net # of Revisions for Fiscal Year 1 : It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less the |
| 413 | `mdl177_emm_fc_rev3y2_alt` | MATRIX | 0.827 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY2 EPS forecasts: change in FY2 consensus earnings since three months ago, scaled by price |
| 414 | `mdl177_qvm_mgtlev_qvaeur_alt` | MATRIX | 0.826 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity and leverage rank for Developed Europe (as defined in VMMEUR) |
| 415 | `mdl177_qvm_estrevrank_qmaeur_alt` | MATRIX | 0.826 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate Revision Rank |
| 416 | `mdl177_qvm_mgteff_qvaeur_alt` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability &  Earnings Quality Rank |
| 417 | `mdl177_qvm_balshtrank_qvaeur_alt` | MATRIX | 0.826 | 风险与质量 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank |
| 418 | `mdl177_qvm_finstmtrank_qvaeur_alt` | MATRIX | 0.826 | 风险与质量 | 0 | — | — | — | UNTESTED | Financial Statement Rank |
| 419 | `mdl177_dvm_dvm_eur_composite_alt` | MATRIX | 0.826 | 其他 | 0 | — | — | — | UNTESTED | Deep Value Europe Model Composite |
| 420 | `mdl177_dvm_past_alt` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Total Assets ratio |
| 421 | `mdl177_dvm_ttmgfp_alt` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price ratio (TTM GAAP earnings plus R&D expenses scaled by market value) |
| 422 | `mdl177_qvm_incstmtrank_qvaeur_alt` | MATRIX | 0.826 | 风险与质量 | 0 | — | — | — | UNTESTED | Income Statement Rank |
| 423 | `mdl177_rvm_rvm_eur_composite_alt` | MATRIX | 0.826 | 其他 | 0 | — | — | — | UNTESTED | Relative Value (EUR) |
| 424 | `mdl177_rvm_ttmgfp_alt` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months Growth Flow-to-Price ratio, defined as last four quarters GAAP earnings plus R&D scaled by market value |
| 425 | `mdl177_rvm_ttmsp_alt` | MATRIX | 0.826 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing twelve months Sales-to-Price ratio |
| 426 | `mdl177_pmm_actrtn6m_alt` | MATRIX | 0.826 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag : It is defined the percent change in price for a stock from month t-7 to month t-1. |
| 427 | `mdl177_qvm_gwthrank_qmaeur_alt` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings and  Expected Growth Rank |
| 428 | `mdl177_emm_chgepsp_alt` | MATRIX | 0.825 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year change in price-adjusted TTM EPS: EPS difference over the last year, divided by price |
| 429 | `mdl177_dvm_ttmfcfp_alt` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing Twelve Month Free Cash Flow to Price |
| 430 | `mdl177_rvm_ttmfcfp_alt` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months Free Cash Flow-to-Price ratio |
| 431 | `mdl77_emm_fc_dypeg` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of Dividend Yield-adjusted PEG: It is defined as the reciprocal of a stock's forward 12-month P/E ratio divided by the total grow |
| 432 | `mdl177_pmm_p50_200ratio_alt` | MATRIX | 0.823 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio : It is defined as the moving average of a stock's prices in last 50 days divided by the moving average of its  |
| 433 | `mdl177_dvm_roe_alt` | MATRIX | 0.823 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity |
| 434 | `mdl177_rvm_roe_alt` | MATRIX | 0.823 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity |
| 435 | `mdl177_dvm_tw_ep_alt` | MATRIX | 0.822 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield |
| 436 | `mdl177_rvm_tw_ep_alt` | MATRIX | 0.822 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield : This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwa |
| 437 | `mdl77_eur_emm_fc_dypeg` | MATRIX | 0.822 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of Dividend Yield-adjusted PEG: It is defined as the reciprocal of a stock's forward 12-month P/E ratio divided by the total grow |
| 438 | `mdl177_pmm_rationalalpha_alt` | MATRIX | 0.820 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha : It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from  |
| 439 | `mdl177_pmm_slope52wp_alt` | MATRIX | 0.820 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52 Week Price Trend Line : It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52 |
| 440 | `mdl177_pmm_relpricestrength_alt` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month Relative Price Strength: stock’s 12-month price strength minus industry average, scaled by industry standard devi |
| 441 | `deep_value_europe_composite_score` | MATRIX | 0.818 | 宏观与行业 | 0 | — | — | — | UNTESTED | Composite deep value signal for the EUR region (Deep Value EUR Model composite score) |
| 442 | `ebitda_to_enterprise_value_ratio_2` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month EBITDA to enterprise value ratio |
| 443 | `operating_liability_leverage_change` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage over the last four quarters (difference in operating liability leverage) |
| 444 | `price_to_total_assets_ratio` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-total assets ratio |
| 445 | `return_on_equity_ratio_3` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity (profitability relative to shareholders’ equity) |
| 446 | `time_weighted_earnings_yield` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield |
| 447 | `ttm_free_cash_flow_to_price` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months free cash flow to price ratio |
| 448 | `ttm_growth_flow_to_price` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month Growth Flow-to-Price ratio: last four quarters GAAP earnings plus R&D scaled by market value |
| 449 | `mdl177_rvm_capacq_alt` | MATRIX | 0.818 | 其他 | 0 | — | — | — | UNTESTED | Capital Acquisition Ratio |
| 450 | `mdl177_emm_chg3yepsp_alt` | MATRIX | 0.816 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-year change in price-adjusted TTM EPS: current TTM EPS minus EPS 12 quarters ago, divided by price |
| 451 | `mdl177_emm_fc_stdevfy1epsp_alt` | MATRIX | 0.815 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY1 EPS Estimates-to-Price |
| 452 | `mdl177_pmm_actrtn24m_alt` | MATRIX | 0.804 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month active return with 1-month lag: percent change in stock price from month t-25 to t-1 |
| 453 | `mdl77_ad` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt to Total Assets: It is defined as the most recently reported total debt divided by total assets. |
| 454 | `mdl77_dvm_chgollev` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Operating Liability Leverage: It is defined as the current quarter operating liability leverage less the operating liability lever |
| 455 | `mdl77_eur_dvm_chgollev` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Operating Liability Leverage: It is defined as the current quarter operating liability leverage less the operating liability lever |
| 456 | `mdl177_gsg_shortsentimentfactor_act_util` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Actual utilization rate of lendable shares; percentage of inventory currently on loan |
| 457 | `mdl177_gsg_shortsentimentfactor_benchmark_fee` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Implied loan rate (benchmark borrowing fee) for the stock in securities lending |
| 458 | `mdl177_gsg_shortsentimentfactor_conc_ratio` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Conc Ratio |
| 459 | `mdl177_gsg_shortsentimentfactor_days_to_cover` | MATRIX | 0.796 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of trading days required to cover short interest based on average daily volume |
| 460 | `mdl177_gsg_shortsentimentfactor_dmd_conc` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Concentration of borrow demand value across counterparties in securities lending |
| 461 | `mdl177_gsg_shortsentimentfactor_dmd_supply` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Demand-to-supply ratio in securities lending (borrow demand divided by lend supply) |
| 462 | `mdl177_gsg_shortsentimentfactor_inv_conc` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Concentration of lending inventory value among lenders |
| 463 | `mdl177_gsg_shortsentimentfactor_lend_supply` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total quantity of shares available to lend (lending supply) |
| 464 | `mdl177_gsg_shortsentimentfactor_onloan_conc` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Concentration of shares currently on loan across counterparties |
| 465 | `mdl177_gsg_shortsentimentfactor_sht_int` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Short interest; total shares sold short or currently on loan |
| 466 | `mdl177_gsg_shortsentimentfactor_util` | MATRIX | 0.796 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Utilization rate; share of lendable stock currently on loan |
| 467 | `mdl77_rvm_ebitdaev` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value: It is defined as the trailing 12-month earnings before interest, taxes, depreciation, and amortization for a |
| 468 | `mdl77_dvm_ebitdaev` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value: It is defined as the trailing 12-month earnings before interest, taxes, depreciation, and amortization for a |
| 469 | `mdl177_emm_fc_epsrm_alt` | MATRIX | 0.794 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Revision Magnitude: 3-month change in the median FY1 consensus EPS estimate, scaled |
| 470 | `mdl77_dsu` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | The beta coefficient estimated by a multiple regression of returns on several macroeconomic aspects over 60 months. |
| 471 | `mdl77_inflation` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | The beta coefficient estimated by a multiple regression of returns on several macroeconomic aspects over 60 months. |
| 472 | `mdl77_oilprice` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | The beta coefficient estimated by a multiple regression of returns on several macroeconomic aspects over 60 months. |
| 473 | `mdl77_pi` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Industrial Production Sensitivity: It is defined as the beta coefficient to Change in Industrial Production, which is estimated by a 60-mont |
| 474 | `mdl77_prc` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Credit Risk Premium Sensitivity: It is defined as the beta coefficient to Change in Credit Risk Premium, which is estimated by a 60-month mu |
| 475 | `mdl77_sh` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Housing Starts Sensitivity: It is defined as the beta coefficient to Change in Housing Starts, which is estimated by a 60-month multiple reg |
| 476 | `mdl77_xiv` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Market Volatility Sensitivity: It is defined as the beta coefficient to change in market volatility, which is estimated by a 60-month multip |
| 477 | `mdl77_yieldsprd` | MATRIX | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Yield Curve Slope Sensitivity: It is defined as the beta coefficient to Change in Slope of Term Structure, which is estimated by a 60-month  |
| 478 | `mdl77_eur_dvm_ebitdaev` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value: It is defined as the trailing 12-month earnings before interest, taxes, depreciation, and amortization for a |
| 479 | `mdl77_eur_rvm_ebitdaev` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value: It is defined as the trailing 12-month earnings before interest, taxes, depreciation, and amortization for a |
| 480 | `mdl77_ceroe` | MATRIX | 0.786 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The trailing 12-month funds from operations divided by the average of the current and previous year |
| 481 | `mdl177_dvm_chgollev_alt` | MATRIX | 0.783 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Operating Liability Leverage over 4 quarters |
| 482 | `mdl177_dvm_ebitdaev_alt` | MATRIX | 0.776 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value ratio |
| 483 | `mdl177_rvm_ebitdaev_alt` | MATRIX | 0.776 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months EBITDA-to-Enterprise Value ratio |
| 484 | `mdl77_nlmktcap` | MATRIX | 0.764 | 其他 | 0 | — | — | — | UNTESTED | Natural Logarithm of Market Capitalization: It is defined as the natural logarithm of the cubic of a stock's total market value. |
| 485 | `mdl77_nlprice` | MATRIX | 0.764 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural Logarithm of Closing Price: It is defined as the natural logarithm of the cubic of a stock's unadjusted closing price. |
| 486 | `mdl77_volto` | MATRIX | 0.764 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading Turnover Ratio: It is defined as the monthly total trading volume divided by the most recently reported total outstanding shares. |
| 487 | `mdl77_actrtn1m` | MATRIX | 0.764 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Month Active Return: It is defined as the percent change in price for a stock from month t-1 to month t. |
| 488 | `mdl77_milliq` | MATRIX | 0.764 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock Illiquidity: It is defined as the monthly average of the daily absolute return to the daily dollar trading volume ratio. |
| 489 | `mdl77_actrtn2m` | MATRIX | 0.763 | 价量与波动 | 0 | — | — | — | UNTESTED | 2-Month Active Return: It is defined as the percent change in price for a stock from month t-2 to month t. |
| 490 | `mdl77_eur_global_indrelrtn4w_` | MATRIX | 0.762 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-Week Industry Relative Return: It is defined as a stock's return in the last 4 weeks minus the average of the comparable returns of all st |
| 491 | `mdl77_visiratio` | MATRIX | 0.762 | 价量与波动 | 0 | — | — | — | UNTESTED | The Visibility Ratio: It equals a stock's most recent daily trading volume divided by the average daily trading volume in the previous 50 tr |
| 492 | `mdl77_cvvolp20d` | MATRIX | 0.761 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-Day Volume Volatility to Price Volatility: It is defined as the coefficient of variation of the last 20 days of closing prices divided by |
| 493 | `mdl77_actrtn3m` | MATRIX | 0.761 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-Month Active Return: It is defined as the percent change in price for a stock from month t-3 to month t. |
| 494 | `mdl77_nlassets` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural Logarithm of Total Assets: It is defined as the natural logarithm of the most recent quarterly reported total assets. |
| 495 | `mdl77_booklev` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book Leverage: It is defined as the most recently reported quarterly total assets divided by the book equity. |
| 496 | `mdl77_ed` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term Debt-to-Equity: It is defined as the most recently reported total long-term debt divided by total book equity. |
| 497 | `mdl77_aor` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets: It is defined as the trailing 12-month income before extra items divided by the average of total assets in the same period |
| 498 | `mdl77_astto` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assets Turnover Ratio: It is defined as the trailing 12-month sales divided by the most recently reported quarterly assets. |
| 499 | `mdl77_equityto` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | The trailing 12-month sales divided by the average of trailing 12-month reported book equity. |
| 500 | `mdl77_noato` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Operating Asset Turnover: It is defined as trailing-12-month sales divided by the last 4-quarters average net operating assets, which eq |
| 501 | `mdl77_global_pvan` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Asset Value to Price: It is defined as the most recent book value of net assets per share (NAV) by the closing price. NAV is calculated  |
| 502 | `mdl77_stockrating` | MATRIX | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Consensus Rating: It is defined as the consensus recommendation for a company. |
| 503 | `mdl77_eur_global_past` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Total Assets: It is defined as a stock's month-end trading price divided by the most recent quarterly reported total assets per sha |
| 504 | `mdl77_eur_global_pe_wt` | MATRIX | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwar |
| 505 | `mdl77_gspea2y_cf` | MATRIX | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-Year Ahead EPS Growth: It is defined as the most recent consensus earnings forecast for fiscal year 2 minus the consensus earnings forecas |
| 506 | `mdl77_mktcappera` | MATRIX | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Stock's current market cap divided by the number of analysts providing Fiscal Year 1 earnings estimates. |
| 507 | `mdl77_pedwf_cf` | MATRIX | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-Month Mean Earnings Yield: It is defined as the next 4-quarter's mean consensus earnings estimate divided by the price. |
| 508 | `mdl77_fc_numest` | MATRIX | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | The number of analysts' earnings estimates for fiscal year 1 for a stock. |
| 509 | `mdl77_netdebt` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Ratio: It is defined as the net debt divided by the sum of the net debt, preferred stock and common stock, where net debt equals th |
| 510 | `mdl77_fc_estep` | MATRIX | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Leading 12-Month Median Earnings Yield: It is defined as the next fiscal year median consensus earnings estimate divided by trading price. |
| 511 | `mdl77_pb` | MATRIX | 0.759 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-Market: It is defined as the most recently reported book value per share for a stock deflated by its month-end trading price. |
| 512 | `mdl77_pd09erpvc` | MATRIX | 0.759 | 价量与波动 | 0 | — | — | — | UNTESTED | CV of Prior 90-Day Closing Prices: It is defined as the standard deviation of a stock's last 90 days closing prices divided by the mean of t |
| 513 | `mdl77_fc_curindfwdep_` | MATRIX | 0.758 | 修正与预期 | 0 | — | — | — | UNTESTED | Industry Relative Leading 4-QTRs EPS to Price: It is defined as a stock's next 4-quarter's analysts consensus earnings estimates-to-price ra |
| 514 | `mdl77_skew90cortn` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-Day Stock Daily Excess Returns: It is defined as the skewness of the distribution of a stock's daily excess (compared to the  |
| 515 | `mdl77_skew90drtn` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-Day Stock Daily Returns: It is defined as the skewness (measure of lack of symmetry) of the distribution of a stock's daily p |
| 516 | `mdl77_yoychgda` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year Change in Leverage: It is defined as the difference between the most recent reported quarterly total liabilities as a percent |
| 517 | `mdl77_bpemtt` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | The company's performance in trailing 1-year before taking into account non-recurring gain or loss, divided by its month-end trading price. |
| 518 | `mdl77_eur_global_psmtt` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Sales-to-Price: It is defined as the most recently reported trailing 12-month sales per share for a stock deflated by its month-end trad |
| 519 | `mdl77_pqipmtt` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | The most recent trailing 12-month operating and non-operating income per share before provisions for income taxes and minority interest for  |
| 520 | `mdl77_apemtt` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | An indicator that standardizes and compares relative share price between time periods and among companies. |
| 521 | `mdl77_mpn` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin: It is defined as the most recently reported quarterly net income after tax divided by the corresponding quarterly sales. |
| 522 | `mdl77_ttmsaleev` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Sales-to-Enterprise Value: It is defined as the trailing 12-month sales for a stock divided by the most recent enterprise value (EV). EV |
| 523 | `mdl77_curindbp_` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry Relative Book-to-Market: It is defined as a stock's current book-to-price ratio (BP) less the average of the BPs of all stocks in t |
| 524 | `mdl77_eur_global_fc_numrevy1` | MATRIX | 0.758 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Number ofRevisions for Fiscal Year 1: It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less  |
| 525 | `mdl77_eur_global_pfgmtt` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 526 | `mdl77_speghc` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Change in Assets-adj TTM EPS: It is defined as the trailing 12-month earnings per share before extra items (EPS) minus 4 quarters ago E |
| 527 | `mdl77_yoychgroa` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | Yearly Change in Return on Assets: It is defined as the most recent trailing 12-month income before extra items as a percentage of total ass |
| 528 | `mdl77_curindsp_` | MATRIX | 0.758 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry Relative TTM Sales-to-Price: It is defined as a stock's trailing 12-month sales-to-price ratio (SP) less the average of the SPs of  |
| 529 | `mdl77_nlsales` | MATRIX | 0.758 | 其他 | 0 | — | — | — | UNTESTED | Natural Logarithm of TTM Sales: It is defined as the natural logarithm of the cubic of a company's trailing 12-month sales. |
| 530 | `mdl77_curindep_` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM EPS-to-Price: It is defined as a stock's trailing 12-month earnings per share before extra items-to-price ratio (EP) l |
| 531 | `mdl77_pctchgastto` | MATRIX | 0.757 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Change in Asset Turnover Ratio: It is defined as the percent change in the most recent asset turnover ratio as compared to that of 4 qu |
| 532 | `mdl77_volpre6m` | MATRIX | 0.757 | 价量与波动 | 0 | — | — | — | UNTESTED | The 6-month moving average of average monthly turnover ratio. |
| 533 | `mdl77_fixastto` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | The trailing 12-month sales divided by the average of the total fixed assets in the same period. |
| 534 | `mdl77_capexast` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Expenditure-to-Total Assets: It is defined as trailing 12-month capital expenditures divided by the total assets from the most recen |
| 535 | `mdl77_vesspem21f_cf` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward 12-M EPS-to-Enterprise Value: It is defined as the consensus forward 12-month earnings per share forecast divided by the sum of mark |
| 536 | `mdl77_gear` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Gearing Ratio: It is defined as the long-term debt divided by the difference between total assets and current liability. |
| 537 | `mdl77_w62isr` | MATRIX | 0.755 | 价量与波动 | 0 | — | — | — | UNTESTED | 26-Week Relative Price Strength: It is defined as a stock's most recent weekly closing price divided by its weekly closing price 26 weeks ag |
| 538 | `mdl77_mktlev` | MATRIX | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock's total market value plus the most recent reported quarterly book debt then divided by the market value. |
| 539 | `mdl77_fc_rev3y1` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | The change in the analysts' projection on company's performance for fiscal year 1 less that of 3 months ago, deflated by its price. |
| 540 | `mdl77_eur_global_fc_rev3y2` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts: It is defined as the change in the current mean consensus earnings estimate for fiscal year 2 less that o |
| 541 | `mdl77_eur_global_actrtn6m` | MATRIX | 0.754 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-7 to month t-1. |
| 542 | `mdl77_capexsale` | MATRIX | 0.754 | 其他 | 0 | — | — | — | UNTESTED | TTM Capital Expenditures-to-Sales: It is defined as trailing 12-month capital expenditures divided by trailing 12-month sales. |
| 543 | `mdl77_eur_global_pspeghc` | MATRIX | 0.754 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the most recently reported trailing 12-month earnings per share and that of 4 quarters ago for a stock deflated by it |
| 544 | `mdl77_ttmcapexp` | MATRIX | 0.754 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM Capital Expenditures-to-Price: It is defined as the trailing 12-month capital expenditures per share for a stock divided by its trading  |
| 545 | `mdl77_lagegp` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | Lagged Inverse of PEG Ratio: It is defined as the trailing 12-month earnings per share before extraordinary items times the change in yearly |
| 546 | `mdl77_pctchgqtrast` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Change in Total Assets: It is defined as the growth in the most recent reported quarterly total assets per share as compared to that of |
| 547 | `mdl77_eur_global_roe` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity: It is defined as the trailing 12-month income before extra items divided by the average of common equity in the same perio |
| 548 | `mdl77_high52w` | MATRIX | 0.753 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-Week High: It is defined as the month-end price divided by the highest monthly closing price in the past 12 months. |
| 549 | `mdl77_lfd` | MATRIX | 0.753 | 其他 | 0 | — | — | — | UNTESTED | The sum of the trailing 12-month pretax income and the trailing 12-month interest expense divided by the trailing 12-month pretax income. |
| 550 | `mdl77_indrelcroe_` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock's lagged quarterly return on equity (ROE) minus the average of the ROEs of all stocks in the same industry deflated by the standard de |
| 551 | `mdl77_roic` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Invested Capital: It is defined as the trailing 12-month net income and interest expenses divided by the average reported invested |
| 552 | `mdl77_totalsaleg` | MATRIX | 0.752 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly TTM Total Sales Growth Rate: It is defined as the percent change in a company's trailing 12-month total sales (TOTSALE) as compared t |
| 553 | `mdl77_6351_rp` | MATRIX | 0.752 | 价量与波动 | 0 | — | — | — | UNTESTED | 15/36 Week Stock Price Ratio: It is defined as the moving average of a stock's prices in the last 15 weeks divided by the moving average of  |
| 554 | `mdl77_pelh_cf` | MATRIX | 0.752 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Revision Confidence: It is defined as the sum of the 3-month change in the highest and lowest FY1 earnings estimate, scaled by month- |
| 555 | `mdl77_pctabv260low` | MATRIX | 0.752 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Above Last 260-Day Lowest Trading Price: It is defined as a stock's current closing price divided by its lowest daily low price in the |
| 556 | `mdl77_divyield` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Dividend Yield: It is defined as the trailing 12-month dividends per share for a stock divided by its month-end trading price. |
| 557 | `mdl77_mpnghc` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Yr Change in Net Profit Margin: It is defined as the most recent quarterly net profit margin (NPM) minus the NPM 4 quarters ago. Net profi |
| 558 | `mdl77_pctchgqtrsales` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | 1-Yr Change in Sales: It is defined as the growth in the most recent reported quarterly sales per share as compared to 4 quarters ago. |
| 559 | `mdl177_emm_fc_dypeg_alt` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of the dividend yield–adjusted PEG ratio |
| 560 | `mdl77_curinddivp_` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Dividend Yield: It is defined as a stock's trailing 12-month dividend yield (DivYield) less the average of the DivYiel |
| 561 | `mdl77_actrtn9m` | MATRIX | 0.750 | 价量与波动 | 0 | — | — | — | UNTESTED | 9-Month Active Return with 1-Month Lag: It is defined as a stock's price percent change from month t-10 to month t-1. |
| 562 | `mdl77_tobinq` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin q: It is defined as the market value of equity (E) plus debt (D) divided by assets (A), or (E + D)/A. D is measured using book values. |
| 563 | `mdl77_fc_fwdroe` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward Return on Equity: It is defined as a stock's analysts' earnings estimates for the next 4 quarters divided by its most recent reporte |
| 564 | `mdl77_eur_global_p50_200ratio` | MATRIX | 0.750 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-200 Day Stock Price Ratio: It is defined as the moving average of a stock's prices in the last 50 days divided by the moving average of i |
| 565 | `mdl77_ratrev6m` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Street Rating Revision: It is defined as the 6-month average of the change in the average analyst recommendation tracked by |
| 566 | `mdl77_w93ntr` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-Week Return with 4-Week Lag: It is defined as a stock's price change from week t-43 to week t-4. |
| 567 | `mdl77_aoer` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained Earnings-to-Total Assets: It is defined as the reported cumulative retained earnings from the most recent quarter deflated by repor |
| 568 | `mdl77_nlvolcap` | MATRIX | 0.747 | 价量与波动 | 0 | — | — | — | UNTESTED | The natural logarithm of the quotient of the trailing 1-year average of the monthly volume to the trailing 1-year average of monthly market  |
| 569 | `mdl77_chgshare` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Percent Change in Shares Outstanding: It is defined as the percent change in a company's current number of outstanding shares as compared to |
| 570 | `mdl77_niper` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income per Employee: It is defined as the income after taxes for the trailing 12 months divided by the number of employees at the end of |
| 571 | `mdl77_revper` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per Employee: It is defined as the trailing 12-month total sales divided by the number of employees at the end of the last reported  |
| 572 | `mdl77_cfita` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Cash Flow from Investment to Total Assets: It is defined as the trailing 12-month cash flow from the investing portion of the cash flow  |
| 573 | `mdl77_ocfast` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow to Assets: It is defined as the trailing 12-month net cash flow from operations divided by the average total assets. |
| 574 | `mdl77_ttmaccu` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting Accruals: It is defined as the difference between the trailing 12-month net income and the trailing 12-month operating cash flow  |
| 575 | `mdl77_ntrm01ff` | MATRIX | 0.745 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French Momentum: It is defined as the percent change in a stock's price from month t-12 to month t-2. |
| 576 | `mdl77_curindocfta_` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Oper Cash Flow-to-Total Assets: It is defined as a stock's trailing 12-month operating cash flow-to-total assets ratio |
| 577 | `mdl77_m6dn2ntr` | MATRIX | 0.745 | 价量与波动 | 0 | — | — | — | UNTESTED | Second Preceding 6-Month Return: It is defined as the percent change in a stock's price from month t-12 to month t-7. |
| 578 | `mdl77_reinrate` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment Rate: It is defined as the trailing 12-month earnings per share before extra items less the trailing 12-month dividends per sha |
| 579 | `mdl77_susgrowth` | MATRIX | 0.745 | 宏观与行业 | 0 | — | — | — | UNTESTED | The maximum growth rate a firm can sustain without having to increase financial leverage. |
| 580 | `mdl77_fc_stdevfy1epsp` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY1 EPS Estimates-to-Price: It is defined as the standard deviation of analyst forecasts for fiscal year 1 earnings scaled by the |
| 581 | `mdl77_tstalp` | MATRIX | 0.744 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-Year Price Momentum Indicator: It is defined as: (CORREL*(260-2)^.5)/(1-CORREL^2)^.5. CORREL is the correlation coefficient between the na |
| 582 | `mdl77_fc_stdevfy2epsp` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Std Dev of FY2 EPS Estimates-to-Price: It is defined as the standard deviation of analyst forecasts for fiscal year 2 earnings scaled by clo |
| 583 | `mdl77_bmpo` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit Margin: It is defined as the most recently reported quarterly operating income divided by the corresponding quarterly sales |
| 584 | `mdl77_eur_global_slope52wp` | MATRIX | 0.744 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 52-Week Price Trend Line: It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 52- |
| 585 | `mdl77_actrtn12m` | MATRIX | 0.743 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-Month Active Return with 1-month Lag: It is defined as the percent change in price for a stock from month t-13 to month t-1. |
| 586 | `mdl77_pfcomtt` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Operating Cash Flow-to-Price: It is defined as the trailing 12-month operating cash flow per share for a stock divided by its trading pr |
| 587 | `mdl77_eur_global_pfcfmtt` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 588 | `mdl77_fcfroi` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow Return on Invested Capital: It is defined as the trailing 12-month free cash flow divided by the average invested capital in  |
| 589 | `mdl77_ocfmargin` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow Profit Margin: It is defined as the trailing 12-month cash flow from operations scaled by the trailing 12-month sales. |
| 590 | `mdl77_eur_global_relpricestrength_` | MATRIX | 0.743 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-Month Relative Price Strength: It is defined as a stock's 12-month relative price strength (PS) minus the PSs of all st |
| 591 | `mdl77_fcfsale` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-TTM Sales: It is defined as the trailing 12-month free cash flow divided by the trailing 12-month sales. |
| 592 | `mdl77_curindocfp_` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Oper Cash Flow-to-Price: It is defined as a stock's trailing 12-month operating cash flow-to-price ratio (OCFP) less t |
| 593 | `mdl77_ebitdap` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Price: It is defined as the trailing 12-month earnings before interest, taxes, depreciation and amortization for a company div |
| 594 | `mdl77_curindebitdap_` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM EBITDA-to-Price: It is defined as a stock's trailing 12-month EBITDA-to-price ratio (EBITDAP) less the average of the  |
| 595 | `mdl77_curindfcfp_` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Free Cash Flow-to-Price: It is defined as a stock's trailing 12-month free cash flow-to-price ratio (FCFP) less the av |
| 596 | `mdl77_surp` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | Real Earnings Surprise: It is defined as the difference between the actual earnings per share and consensus forecasts prior to the announcem |
| 597 | `mdl77_ebitdaev` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value: It is defined as the trailing 12-month earnings before interest, taxes, depreciation, and amortization for a |
| 598 | `mdl77_chg3yepsast` | MATRIX | 0.740 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Change in Assets-adj TTM EPS: It is defined as the trailing 12-month earnings per share before extra items (EPS) minus the EPS 12-quart |
| 599 | `mdl77_fcfequity` | MATRIX | 0.739 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow to Equity: It is defined as the trailing 12-month free cash flow divided by the average book equity value in the same per |
| 600 | `mdl77_vefcfmtt` | MATRIX | 0.739 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Enterprise Value: It is defined as the trailing 12-month free cash flow (FCF) for a stock scaled by its enterprise val |
| 601 | `mdl77_eur_global_rationalalpha` | MATRIX | 0.739 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha: It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 602 | `mdl77_slope66wp` | MATRIX | 0.738 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of 66 Week Price Trend Line: It is defined as the 4-week lagged slope coefficient of the least squares regression line of the last 66- |
| 603 | `mdl77_fc_fcfroey1p` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Product of TTM FCF Yield and Forward ROE: It is defined as the trailing 12-month free cash flow per share multiplied by the next 4-quarter c |
| 604 | `mdl77_eur_global_chg3yepsp` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month earnings per share and that of 12 quarters ago for a stock divided by its month-end trading pri |
| 605 | `mdl77_fcoghc` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Chg in Assets-adj TTM Oper Cash Flow: It is defined as the most recently reported trailing 12-month operating cash flow minus 4 quarter |
| 606 | `mdl77_yoychgaa` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Accruals to Assets: It is defined as the trailing 12-month income before extra items less the trailing 12-month operating cash flo |
| 607 | `mdl77_fcfghc` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Chg in Assets-adj TTM Free Cash Flow: It is defined as the trailing 12-month free cash flow minus 4 quarters ago trailing 12-month free |
| 608 | `mdl77_cfroi` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Return on Invested Capital: It is defined as the trailing 12-month cash flow divided by the average invested capital in the same p |
| 609 | `mdl77_fc_rev6` | MATRIX | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Averaged Last 6-M EPS Revisions for FY1: It is defined as the average of prior 6-month monthly changes in a stock's consensus analysts' earn |
| 610 | `mdl77_w57w03_rp` | MATRIX | 0.736 | 价量与波动 | 0 | — | — | — | UNTESTED | 30-75 Week Stock Price Ratio: It is defined as the moving average of a stock's prices in the last 30 weeks divided by the moving average of  |
| 611 | `mdl77_mpoghc` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Change in Operating Profit Margin: It is defined as the most recent quarterly operating profit margin minus that of 4 quarters ago. Ope |
| 612 | `mdl77_pfcmtt` | MATRIX | 0.735 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Cash Flow-to-Price: It is defined as the trailing 12-month cash flows per share for a stock scaled by its trading price. Cash flow is de |
| 613 | `mdl77_curindcfp_` | MATRIX | 0.735 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry Relative TTM Cash Flow-to-Price: It is defined as a stock's trailing 12-month cash flow-to-price ratio (CFP) less the average of th |
| 614 | `mdl77_capacq` | MATRIX | 0.734 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital Acquisition Ratio: It is defined as the trailing 12-month operating cash flow less the trailing 12-month cash dividends and then div |
| 615 | `mdl77_chgalpha12m` | MATRIX | 0.734 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 12-Month Alpha: It is defined as the 6-month change in a stock's 12-month alpha, which equals the intercept from t |
| 616 | `mdl77_eur_global_mrspe_cf` | MATRIX | 0.734 | 修正与预期 | 0 | — | — | — | UNTESTED | The 3-month change in analysts' median earnings forecast for a stock's fiscal 1 scaled by the current mean estimate. |
| 617 | `mdl77_pfcoghc` | MATRIX | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the most recently reported trailing 12-month operating cash flow per share and that of 4 quarters ago for a stock div |
| 618 | `mdl77_actrtn18m` | MATRIX | 0.732 | 价量与波动 | 0 | — | — | — | UNTESTED | 18-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-19 to month t-1. |
| 619 | `mdl77_pfcfghc` | MATRIX | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month free cash flow per share and that of 4 quarters ago for a stock divided by its trading price. |
| 620 | `mdl77_eur_global_indrelrtn5d_` | MATRIX | 0.731 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock's return in the last 5 days minus the average of the comparable returns of all stocks in the same industry, then deflated by the stand |
| 621 | `mdl77_lumqca` | MATRIX | 0.731 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition Multiple: It is defined as the most recent quarterly reported invested capital divided by the trailing 12-month EBITDA. |
| 622 | `mdl77_ocfroi` | MATRIX | 0.731 | 盈利与财务 | 0 | — | — | — | UNTESTED | Oper Cash Flow Return on Invested Capital: It is defined as the trailing 12-month operating cash flow divided by the average invested capita |
| 623 | `mdl77_voctni` | MATRIX | 0.731 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interest Coverage: It is defined as the most recently reported quarterly operating income before depreciation divided by the quarterly long- |
| 624 | `mdl77_debtcf` | MATRIX | 0.730 | 盈利与财务 | 0 | — | — | — | UNTESTED | The sum of the most recent reported long-term debt and short-term interest-bearing debt divided by the trailing 12-month cash flow. |
| 625 | `mdl77_pfcf_cf` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward Free Cash Flow-to-Price: It is defined as the next 4 quarters' mean consensus earnings estimate plus trailing 12-month depreciation  |
| 626 | `mdl77_fcghc` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-Year Change in Assets-Adj TTM Cash Flow: It is defined as the trailing 12-month cash flow minus comparable trailing 12-month cash flow fro |
| 627 | `mdl177_vmm_chgepsp` | MATRIX | 0.729 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year change in price-adjusted trailing twelve-month EPS; difference in TTM EPS over the last year divided by price |
| 628 | `mdl177_vmm_chgnoa` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net operating assets, including debt, equity, and cash |
| 629 | `mdl177_vmm_fc_rev3y2` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Second fiscal year forecast revision: change in analysts’ estimates for the second fiscal year ahead |
| 630 | `mdl177_vmm_indrelrtn5d_` | MATRIX | 0.729 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day industry-relative return: stock’s return over the last five days minus the industry average, standardized by the industry’s standard d |
| 631 | `mdl177_vmm_rationalalpha` | MATRIX | 0.729 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha signal using rationally decaying weights on past returns |
| 632 | `mdl177_vmm_ttmfcfp` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month free cash flow to price |
| 633 | `mdl177_vmm_ttmgfp` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month growth flow-to-price ratio (last four quarters GAAP earnings plus R&D expenses scaled by market value) |
| 634 | `mdl177_vmm_tw_ep` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield |
| 635 | `mdl177_eur_incstmtrank_qaveur` | MATRIX | 0.729 | 风险与质量 | 0 | — | — | — | UNTESTED | Income Statement Rank |
| 636 | `mdl177_eur_mgteff_qvaeur` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability &  Earnings Quality Rank |
| 637 | `mdl177_qva_balshtrank_qvaeur` | MATRIX | 0.729 | 风险与质量 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank |
| 638 | `mdl177_qva_evrank_qvaeur` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Valuation Rank |
| 639 | `mdl177_qva_finstmtrank_qvaeur` | MATRIX | 0.729 | 风险与质量 | 0 | — | — | — | UNTESTED | Financial Statement Rank |
| 640 | `mdl177_qva_incstmtrank_qvaeur` | MATRIX | 0.729 | 风险与质量 | 0 | — | — | — | UNTESTED | Income Statement Rank |
| 641 | `mdl177_qva_mgteff_qvaeur` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability &  Earnings Quality Rank |
| 642 | `mdl177_qva_mgtlev_qvaeur` | MATRIX | 0.729 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity and leverage rank within the EUR Value Momentum model (VMMEUR) |
| 643 | `mdl177_qva_qva_eur_composite` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Value Analyst (EUR) |
| 644 | `mdl177_qva_vmm_eur_composite` | MATRIX | 0.729 | 价量与波动 | 0 | — | — | — | UNTESTED | Value Momentum EUR model composite score |
| 645 | `mdl77_spe1yfvc_cf` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | FY1 EPS Estimates Dispersion: It is defined as the standard deviation of analyst earnings estimates for fiscal year 1 divided by the mean co |
| 646 | `mdl77_oplev` | MATRIX | 0.728 | 其他 | 0 | — | — | — | UNTESTED | Operating Leverage: It is defined as the percent change in the trailing 12-month operating income from the previous quarter divided by the p |
| 647 | `mdl77_spe2yfvc_cf` | MATRIX | 0.728 | 修正与预期 | 0 | — | — | — | UNTESTED | FY2 EPS Forecast Dispersion: It is defined as the standard deviation of analyst earnings estimates for fiscal year 2 divided by the mean con |
| 648 | `mdl77_pctchgeps` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percent change in a stock's most recent trailing 12-month earnings per share before extra items as compared to itself 4 quarters ago. |
| 649 | `mdl77_pedu` | MATRIX | 0.725 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Change in Depreciation: It is defined as the difference between the trailing 12-month depreciation expenses and the expected leve |
| 650 | `mdl77_liqcoeff` | MATRIX | 0.724 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity Coefficient: It is the slope of the regression between the monthly stock trading turnover ratio (X) and the contemporary monthly s |
| 651 | `mdl77_cfleverage` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Leverage: It is defined as the total liabilities divided by the trailing 12-month operating cash flow. |
| 652 | `mdl77_pfcghc` | MATRIX | 0.723 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month cash flow per share and that of 12 quarters ago for a stock divided by its trading price. |
| 653 | `mdl77_chg6malpha18m` | MATRIX | 0.723 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 18-Month Alpha: It is defined as the 6-month change in a stock's 18-month alpha, which equals the intercept from t |
| 654 | `mdl77_m42rav` | MATRIX | 0.723 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Value at Risk: It is defined as the minimum of a stock's monthly price return in the last 20-month period. |
| 655 | `mdl77_saleeps` | MATRIX | 0.722 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM Sales vs EPS: It is defined as the absolute value of the difference between the yearly percent change in trailing 12-month sal |
| 656 | `mdl77_global_nopatmargin` | MATRIX | 0.722 | 盈利与财务 | 0 | — | — | — | UNTESTED | NOPAT Margin: It is defined as: (Net Income + Interest Expense*(1-Effective Tax Rate))/Net Sales. All items are for trailing 12-month. Effec |
| 657 | `mdl77_eur_global_actrtn24m` | MATRIX | 0.721 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-25 to month t-1. |
| 658 | `mdl77_ica` | MATRIX | 0.716 | 其他 | 0 | — | — | — | UNTESTED | Abnormal Capital Investment: It is defined as the change in a firm's most recent trailing 12-month capital investment intensity compared to  |
| 659 | `mdl77_gtl` | MATRIX | 0.716 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-Term Growth Rate Estimates: It is defined as the consensus long-term growth forecast. It generally represents an expected annual increa |
| 660 | `mdl77_pge_cf` | MATRIX | 0.715 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimates on the next 1 year average earnings scaled by company's prospects on growth and its stock price. |
| 661 | `mdl77_pctchgocf` | MATRIX | 0.715 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Growth in TTM Oper Cash Flow: It is defined as the percent change of a stock's most recent trailing 12-month operating cash flow per sh |
| 662 | `mdl77_epschgetr` | MATRIX | 0.714 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS from Change in Effective Tax Rate: It is defined as the trailing 12-month pre-tax income per share times the difference between most rec |
| 663 | `mdl77_nfaldebt` | MATRIX | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Fixed Assets to Long-term Debt: It is defined as the most recent quarterly reported net fixed assets divided by the total long-term debt |
| 664 | `mdl77_pctchgcf` | MATRIX | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Growth in TTM Cash Flow: It is defined as the percent change in a stock's most recent trailing 12-month cash flow per share (CF) as com |
| 665 | `mdl77_global_totalcov` | MATRIX | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Coverage: It equals (Cash Flow from Operations + Interest Paid + Tax Paid)/(Interest + Principal Paid). |
| 666 | `mdl77_chg3yocfast` | MATRIX | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Change in Assets-adj TTM Oper Cash Flow: It is defined as the most recently reported trailing 12-month operating cash flow (OCF) minus  |
| 667 | `mdl77_chg3yfcfast` | MATRIX | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Chg in Assets-adj TTM Free Cash Flow: It is defined as the trailing 12-month free cash flow minus 12 quarters ago trailing 12-month fre |
| 668 | `mdl77_eur_global_fc_dypeg` | MATRIX | 0.706 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of Dividend Yield-adjusted PEG: It is defined as the reciprocal of a stock's forward 12-month P/E ratio divided by the total grow |
| 669 | `mdl77_gsg_shortsentimentfactor_benchmark_fee` | MATRIX | 0.704 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Benchmark fee |
| 670 | `mdl77_pctchg3yeps` | MATRIX | 0.704 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percent change in a stock's most recent trailing 12-month earnings per share as compared to itself 12 quarters ago. |
| 671 | `mdl77_cg3ysales` | MATRIX | 0.703 | 宏观与行业 | 0 | — | — | — | UNTESTED | The geometric growth rate of the trailing 12-month sales per share in the last 12 quarters. |
| 672 | `mdl77_chg3ycfast` | MATRIX | 0.701 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Change in Assets-adj TTM Cash Flow: It is defined as the most recently reported trailing 12-month operating cash flow minus 12 quarters |
| 673 | `mdl77_gtlm6ghc` | MATRIX | 0.700 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-M Change in Long-term Growth Estimates: It is defined as the percent change in the most recent mean consensus long-term growth forecast as |
| 674 | `mdl77_pfcoy3ghc` | MATRIX | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month operating cash flow per share and that of 12 quarters ago for a stock divided by its trading pr |
| 675 | `mdl77_pfcfy3ghc` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Change in Price-Adj TTM FCF: It is defined as the difference between the most recently reported trailing 12-month free cash flow per sh |
| 676 | `mdl77_actrtn36m` | MATRIX | 0.699 | 价量与波动 | 0 | — | — | — | UNTESTED | 36-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-37 to month t-1. |
| 677 | `mdl77_saleg5y` | MATRIX | 0.699 | 其他 | 0 | — | — | — | UNTESTED | 5-yr Sales Growth: It is defined as the difference between the trailing 12-month sales per share (SALE) and the SALE 20 quarters ago and the |
| 678 | `mdl77_spefcn` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM EPS vs. Oper Cash Flows: It is defined as the absolute value of the difference between the yearly percent change in trailing 1 |
| 679 | `mdl77_emeasales` | MATRIX | 0.694 | 其他 | 0 | — | — | — | UNTESTED | EMEA Sales Exposure: It is defined as the annual aggregate sales for EMEA as reported by the company divided by total annual sales. |
| 680 | `mdl77_ollev` | MATRIX | 0.694 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Liability Leverage: It is defined as 1 minus the ratio of (short-term debt + long-term debt + common equity + preferred equity - c |
| 681 | `mdl77_opincltd` | MATRIX | 0.693 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in TTM Oper Income vs LT Debt: It is defined as the difference between the yearly percent change in operating income and the yearly p |
| 682 | `mdl77_pfcy3ghc` | MATRIX | 0.692 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the trailing 12-month cash flow per share and that of 12 quarters ago comparable trailing 12-month cash flow for a st |
| 683 | `mdl77_eur_global_chgollev` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Operating Liability Leverage: It is defined as the current quarter operating liability leverage less the operating liability lever |
| 684 | `mdl77_chgalpha36m` | MATRIX | 0.689 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-Month Nominal Change in 36-Month Alpha: It is defined as the 6-month change in a stock's 36-month alpha, which equals the intercept from t |
| 685 | `mdl77_gsg_shortsentimentfactor_onloan_conc` | MATRIX | 0.689 | 情绪与新闻 | 0 | — | — | — | UNTESTED | On loan concentration |
| 686 | `mdl77_gsg_shortsentimentfactor_dmd_conc` | MATRIX | 0.688 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Demand Concentration |
| 687 | `mdl77_nasales` | MATRIX | 0.687 | 其他 | 0 | — | — | — | UNTESTED | North America Sales Exposure: It is defined as the annual aggregate sales for North America as reported by the company divided by total annu |
| 688 | `mdl77_dcc` | MATRIX | 0.686 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Cash Flow Debt Coverage Ratio: It is defined as the most recently reported quarterly cash flow from operations less the cash dividen |
| 689 | `mdl77_gsg_shortsentimentfactor_inv_conc` | MATRIX | 0.685 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Inventory concentration |
| 690 | `mdl77_gsg_shortsentimentfactor_conc_ratio` | MATRIX | 0.681 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Concentration ratio |
| 691 | `mdl77_global_pctchg3yocf` | MATRIX | 0.681 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Growth in TTM Oper Cash Flow: It is defined as the percent change in a stock's most recent trailing 12-month operating cash flow per sh |
| 692 | `mdl77_pctchg3ycf` | MATRIX | 0.679 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percent change in a stock's most recent trailing 12-month cash flow per share as compared to itself 12 quarters ago. |
| 693 | `mdl77_dpcapex` | MATRIX | 0.676 | 其他 | 0 | — | — | — | UNTESTED | Change in TTM Depreciation vs CapEx: It is defined as the absolute value of the difference between the yearly percent change in trailing 12- |
| 694 | `mdl77_cashp` | MATRIX | 0.670 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash-to-Price: It is defined as the most recently reported cash and equivalents per share of a company divided by the trading price. |
| 695 | `mdl77_cashsev` | MATRIX | 0.670 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash to Enterprise Value: It is defined as the total cash & equivalents divided by the sum of the market value of common equity and book val |
| 696 | `mdl77_eur_global_chgnoa` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Net Operating Assets: It is defined as the year-over-year change of net operating assets to total assets, where net operating asse |
| 697 | `mdl77_aspanratio` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock's quarterly operating assets minus its operating liabilities deflated by the lagged total assets |
| 698 | `mdl77_cashsale` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | The mean value of company's assets in the trailing 1-year divided by the trailing 1-year revenues. |
| 699 | `mdl77_pca` | MATRIX | 0.668 | 其他 | 0 | — | — | — | UNTESTED | Average Collection Period: It is defined as the average of the trailing 12-month reported accounts receivable times 365 and then divided by  |
| 700 | `mdl77_netcashp` | MATRIX | 0.666 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Cash to Equity: It is defined as most recently reported quarterly cash & equivalents less the long-term debt and current debt for a stoc |
| 701 | `mdl77_covol` | MATRIX | 0.666 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Trading Volume Trend: It is defined as the slope of the least squares regression line of the last 60 months of monthly trading volu |
| 702 | `mdl77_rau` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Change in Accounts Receivable: It is defined as the difference between current accounts receivable and the expected level of acco |
| 703 | `mdl77_invast` | MATRIX | 0.664 | 盈利与财务 | 0 | — | — | — | UNTESTED | The current inventory level deflated by the total assets from the most recent quarter. |
| 704 | `mdl77_global_chgars` | MATRIX | 0.664 | 其他 | 0 | — | — | — | UNTESTED | 1-yr Change in Acct Receivable as Percentage ofSales: It is defined as the change between the last reported accounts receivable as a percent |
| 705 | `mdl77_salerec` | MATRIX | 0.664 | 其他 | 0 | — | — | — | UNTESTED | Change in TTM Sales vs Accounts Receivable: It is defined as the difference between the yearly percent change in trailing 12-month sales and |
| 706 | `mdl77_vmm_vmm_eur_composite` | MATRIX | 0.663 | 价量与波动 | 0 | — | — | — | UNTESTED | Score based on valuation momentum |
| 707 | `mdl77_qva_qva_eur_composite` | MATRIX | 0.663 | 宏观与行业 | 0 | — | — | — | UNTESTED | It is defined as the Score based on a strategy that selects for stocks in a universe of stocks by comparing different financial metrics as a |
| 708 | `mdl77_qva_rueavq_mvd` | MATRIX | 0.663 | 盈利与财务 | 0 | — | — | — | UNTESTED | Valuation Rank: It is defined as the aggregate of the Financial Statement Rank (40%) and Earnings Valuation Rank (60%). |
| 709 | `mdl77_qva_vmm_eur_composite` | MATRIX | 0.663 | 价量与波动 | 0 | — | — | — | UNTESTED | Score based on valuation momentum |
| 710 | `mdl77_eur_mgteff_qvaeur` | MATRIX | 0.663 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal weighted average of the Change in Net Operating Assets, Net Income Per Employee, Return on Equity and 1-yr Change in Price-adj TTM |
| 711 | `mdl77_qva_evrank_qvaeur` | MATRIX | 0.663 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal-weighted composite of financial ratios based on a company's profits. |
| 712 | `mdl77_qva_mgtlev_qvaeur` | MATRIX | 0.663 | 盈利与财务 | 0 | — | — | — | UNTESTED | Liquidity and Leverage Rank: It is defined as the equal-weighted average of Tobin Q, Change in Operating Liability Leverage, and Interest Co |
| 713 | `mdl77_qva_mgteff_qvaeur` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal weighted average of the Change in Net Operating Assets, Net Income Per Employee, Return on Equity and 1-yr Change in Price-adj TTM |
| 714 | `mdl77_vmm_pe_wt` | MATRIX | 0.662 | 修正与预期 | 0 | — | — | — | UNTESTED | Time-Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a twelve-month forwar |
| 715 | `mdl77_eur_balshtrank_qvaeur` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank: It is defined as the equal weighted average of the Book-to-Price, Cash-to-Price and Total Assets-to-Price Ranks |
| 716 | `mdl77_eur_incstmtrank_qaveur` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Statement Rank: It is defined as the equal-weighted composite of the TTM Growth Flow-to-Price and TTM EBITDA-to-Enterprise Value Rank |
| 717 | `mdl77_vmm_pfgmtt` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 718 | `mdl77_global_cashburnrate` | MATRIX | 0.662 | 宏观与行业 | 0 | — | — | — | UNTESTED | Cash Burn Rate: It is defined as: -(Cash From Operations + Cash from Investments)/(Cash + Short-term Investments). |
| 719 | `mdl77_qva_balshtrank_qvaeur` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank: It is defined as the equal-weighted average of the Book-to-Price, Cash-to-Price, and Total Assets-to-Price Rank |
| 720 | `mdl77_qva_finstmtrank_qvaeur` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial Statement Rank: It is defined as the equal-weighted composite of the Income Statement, Balance Sheet Strength, and TTM Operating C |
| 721 | `mdl77_qva_incstmtrank_qvaeur` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Statement Rank: It is defined as the equal-weighted composite of the TTM Growth Flow-to-Price and TTM EBITDA-to-Enterprise Value Rank |
| 722 | `mdl77_vmm_fc_rev3y2` | MATRIX | 0.661 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts: It is defined as the change in a stock's current analysts mean earnings estimate for fiscal year 2 less t |
| 723 | `mdl77_eur_qva_qva_eur_composite` | MATRIX | 0.661 | 宏观与行业 | 0 | — | — | — | UNTESTED | It is defined as the score based on a strategy that selects stocks in a universe of stocks by comparing different financial metrics as a rat |
| 724 | `mdl77_eur_qva_vmm_eur_composite` | MATRIX | 0.661 | 价量与波动 | 0 | — | — | — | UNTESTED | Score based on valuation momentum |
| 725 | `mdl77_eur_eur_mgteff_qvaeur` | MATRIX | 0.661 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal weighted average of the Change in Net Operating Assets, Net Income Per Employee, Return on Equity and 1-yr Change in Price-adj TTM |
| 726 | `mdl77_eur_qva_evrank_qvaeur` | MATRIX | 0.661 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal-weighted composite of financial ratios based on a company's profits. |
| 727 | `mdl77_eur_qva_mgtlev_qvaeur` | MATRIX | 0.661 | 盈利与财务 | 0 | — | — | — | UNTESTED | Liquidity and Leverage Rank: It is defined as the equal-weighted average of Tobin Q, Change in Operating Liability Leverage, and Interest Co |
| 728 | `mdl77_eur_qva_mgteff_qvaeur` | MATRIX | 0.661 | 盈利与财务 | 0 | — | — | — | UNTESTED | The equal-weighted average of the Change in Net Operating Assets, Net Income Per Employee, Return on Equity, and 1-yr Change in Price-adj TT |
| 729 | `mdl77_eur_vmm_pe_wt` | MATRIX | 0.660 | 修正与预期 | 0 | — | — | — | UNTESTED | Time Weighted Earnings Yield: This factor uses a time-weighted combination of FY1 and FY2 earnings estimates to create a 12-month forward ea |
| 730 | `mdl77_eur_eur_incstmtrank_qaveur` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Statement Rank: It is defined as the equal weighted composite of the TTM Growth Flow-to-Price and TTM EBITDA-to-Enterprise Value Rank |
| 731 | `mdl77_eur_vmm_pfgmtt` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Growth Flow-to-Price: It is defined as the sum of trailing 12-month growth flow value per share for a stock divided by its month-end tra |
| 732 | `mdl77_eur_qva_balshtrank_qvaeur` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank: It is defined as the equal weighted average of the Book-to-Price, Cash-to-Price, and Total Assets-to-Price Rank |
| 733 | `mdl77_eur_qva_finstmtrank_qvaeur` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial Statement Rank: It is defined as the equal-weighted composite of the Income Statement, Balance Sheet Strength, and TTM Operating C |
| 734 | `mdl77_eur_qva_incstmtrank_qvaeur` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Statement Rank: It is defined as the equal-weighted composite of the TTM Growth Flow-to-Price and TTM EBITDA-to-Enterprise Value Rank |
| 735 | `mdl77_vmm_pfcfmtt` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 736 | `mdl77_beta` | MATRIX | 0.660 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Beta: It is defined as 0.67 times the 60-month beta plus 0.33. Beta is the covariance between a stock's monthly return and the mont |
| 737 | `mdl77_eur_vmm_fc_rev3y2` | MATRIX | 0.659 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in FY2 EPS Forecasts: It is defined as the change in a stock's current analysts' mean earnings estimate for fiscal year 2 less  |
| 738 | `mdl77_vmm_pspeghc` | MATRIX | 0.659 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the most recently reported trailing 12-month earnings per share and that of 4 quarters ago for a stock deflated by it |
| 739 | `mdl77_eur_vmm_pfcfmtt` | MATRIX | 0.658 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM Free Cash Flow-to-Price: It is defined as the trailing 12-month free cash flow per share for a stock divided by its month-end trading pr |
| 740 | `mdl77_vmm_indrelrtn5d_` | MATRIX | 0.658 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock's return in the last 5 days minus the average of the comparable returns of all stocks in the same industry, then deflated by the stand |
| 741 | `mdl77_eur_vmm_pspeghc` | MATRIX | 0.657 | 盈利与财务 | 0 | — | — | — | UNTESTED | The difference between the most recently reported trailing 12-month earnings per share and that of 4 quarters ago for a stock, deflated by i |
| 742 | `mdl77_sighc` | MATRIX | 0.657 | 其他 | 0 | — | — | — | UNTESTED | 1-yr Chg in QTR Inventory as Percentage ofSales: It is defined as the most recently reported inventory as a percentage of trailing 12-month  |
| 743 | `mdl77_vmm_rationalalpha` | MATRIX | 0.657 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha: It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 744 | `mdl77_eur_vmm_indrelrtn5d_` | MATRIX | 0.656 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock's return in the last 5 days minus the average of the comparable returns of all stocks in the same industry, then deflated by the stand |
| 745 | `mdl77_eur_vmm_rationalalpha` | MATRIX | 0.655 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha: It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from a |
| 746 | `mdl77_rerror60m` | MATRIX | 0.654 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression Error of 60-Month CAPM: It is defined as the standard error of the slope of the least squares regression line for a stock's last  |
| 747 | `mdl77_sigma` | MATRIX | 0.654 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock Return Volatility: It is defined as the standard deviation of a stock's monthly returns in the prior 60 months. |
| 748 | `mdl77_alpha60m` | MATRIX | 0.654 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Alpha: It is defined as the intercept of the regression line which best fits a stock's monthly price return against the S&P 500 ind |
| 749 | `mdl77_betasigma` | MATRIX | 0.654 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of Beta and Sigma: It is defined as the product of the adjusted 60-month Beta and 60-month Sigma (standard deviation of monthly pric |
| 750 | `mdl77_actrtn60m` | MATRIX | 0.653 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-Month Active Return with 1-Month Lag: It is defined as the percent change in price for a stock from month t-61 to month t-1. |
| 751 | `mdl77_chgvolpre4y` | MATRIX | 0.652 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-Year Change in the Average Trading Volume: It is defined as the change in the most recent 6-month moving average of monthly turnover ratio |
| 752 | `mdl77_perg` | MATRIX | 0.652 | 修正与预期 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG Ratio: It is defined as the stock price divided by the leading 12-month consensus earnings forecast, scaled by the average |
| 753 | `mdl77_fc_ebop` | MATRIX | 0.651 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock's valuation based on a model deflated by its month-end trading price. The model measures a firm's intrinsic value by comparing generat |
| 754 | `mdl77_pctchgfcf` | MATRIX | 0.650 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-yr Growth in TTM Free Cash Flow: It is defined as the percent change in a stock's most recent trailing 12-month free cash flow per share ( |
| 755 | `mdl77_salegpm` | MATRIX | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in QTR Sales vs Gross Margin: It is defined as the difference between the yearly change in most recent reported quarterly sales and t |
| 756 | `mdl77_yoychggpm` | MATRIX | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Yearly Change in Gross Profit Margin: It is defined as the most recent quarterly reported gross profit margin minus the margin for the same  |
| 757 | `mdl77_gsg_shortsentimentfactor_act_util` | MATRIX | 0.646 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Account Utility |
| 758 | `mdl77_fc_rel5yfwdep` | MATRIX | 0.645 | 修正与预期 | 0 | — | — | — | UNTESTED | 5-yr Relative Leading 12-Month Earnings Yield: It is defined as a stock's current next 4 quarters' consensus analyst earnings forecasts-to-p |
| 759 | `mdl177_eur_balshtrank_qvaeur_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank |
| 760 | `mdl177_qva_balshtrank_qvaeur_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Balance Sheet Strength Rank |
| 761 | `mdl177_qva_dvm_qvaeur_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Cross-sectional valuation rank for European equities in the QVA model, measuring cheapness based on valuation metrics |
| 762 | `mdl177_qva_finstmtrank_qvaeur_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Financial Statement Rank |
| 763 | `mdl177_qva_qva_eur_composite_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall composite score for the QSG QVA Europe model, aggregating its subranks into a single signal |
| 764 | `mdl177_eur_incstmtrank_qaveur_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Income Statement Rank |
| 765 | `mdl177_eur_mgteff_qvaeur_alt` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability &  Earnings Quality Rank |
| 766 | `mdl177_qva_incstmtrank_qvaeur_alt` | MATRIX | 0.640 | 风险与质量 | 0 | — | — | — | UNTESTED | Income Statement Rank |
| 767 | `mdl177_qva_mgteff_qvaeur_alt` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability &  Earnings Quality Rank |
| 768 | `mdl177_qva_mgtlev_qvaeur_alt` | MATRIX | 0.640 | 价量与波动 | 0 | — | — | — | UNTESTED | Cross-sectional liquidity and leverage rank for European equities in the QVA/VMM framework, with lower leverage and stronger liquidity ranki |
| 769 | `mdl177_qva_vmm_eur_composite_alt` | MATRIX | 0.640 | 价量与波动 | 0 | — | — | — | UNTESTED | Value Momentum Europe Model composite score |
| 770 | `mdl177_vmm_vmm_eur_composite_alt` | MATRIX | 0.640 | 价量与波动 | 0 | — | — | — | UNTESTED | Composite Value Momentum Model score for Europe |
| 771 | `mdl177_qva_evrank_qvaeur_alt` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Valuation Rank |
| 772 | `mdl177_vmm_ttmgfp_alt` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve month growth flow-to-price ratio last four quarters GAAP earnings plus R and D scaled by market value |
| 773 | `mdl177_vmm_chgepsp_alt` | MATRIX | 0.640 | 价量与波动 | 0 | — | — | — | UNTESTED | One-year change in price-adjusted trailing twelve month EPS divided by price |
| 774 | `mdl177_vmm_ttmfcfp_alt` | MATRIX | 0.639 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve month free cash flow to price ratio |
| 775 | `mdl77_rel5ybp` | MATRIX | 0.639 | 其他 | 0 | — | — | — | UNTESTED | 5-Yr Relative Book-to-Market: It is defined as a stock's current book-to-market ratio (BP) minus the average of the BPs in the last 60 month |
| 776 | `mdl177_vmm_tw_ep_alt` | MATRIX | 0.638 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield |
| 777 | `mdl77_rel5yep` | MATRIX | 0.638 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-yr Relative TTM Earnings-to-Price: It is defined as a stock's current trailing 12-month earnings per share before extra items-to-price rat |
| 778 | `mdl177_vmm_indrelrtn5d_alt` | MATRIX | 0.637 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day industry-relative return standardized by industry standard deviation |
| 779 | `mdl77_ydp_cf` | MATRIX | 0.637 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted Dividend Yield: It is defined as an assumed payout ratio multiplied by the next 4-quarter consensus earnings estimate divided by t |
| 780 | `mdl77_rel5ysp` | MATRIX | 0.637 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-yr Relative TTM Sales-to-Price: It is defined as a stock's current trailing 12-month sales-to-price ratio (SP) minus the average of the SP |
| 781 | `mdl177_vmm_fc_rev3y2_alt` | MATRIX | 0.637 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-M Revision in  FY2 EPS Forecasts |
| 782 | `mdl77_divcov` | MATRIX | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Company's trailing 1-year profits scaled by its annual dividends. |
| 783 | `mdl77_gsg_shortsentimentfactor_days_to_cover` | MATRIX | 0.636 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Days to Cover |
| 784 | `mdl77_rdsale` | MATRIX | 0.636 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | R&D Intensity: It is defined as the average of the research & development expenses in the trailing 12 months deflated by the sum of total sa |
| 785 | `mdl77_apsales` | MATRIX | 0.635 | 其他 | 0 | — | — | — | UNTESTED | Asia-Pacific Sales Exposure: It is defined as the annual aggregate sales for Asia-Pacific as reported by the company divided by total annual |
| 786 | `mdl77_vniu` | MATRIX | 0.634 | 其他 | 0 | — | — | — | UNTESTED | The difference of inventory between present and expected levels. |
| 787 | `mdl177_vmm_rationalalpha_alt` | MATRIX | 0.633 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational Decay Alpha : It evaluates stocks based on their historical 12-month market (S&P 500) adjusted excess return (the Y intercept from  |
| 788 | `mdl77_o_gsg_shortsentimentfactor_dmd_supply` | MATRIX | 0.629 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Demand Supply |
| 789 | `mdl77_lasales` | MATRIX | 0.624 | 其他 | 0 | — | — | — | UNTESTED | Latin America Sales Exposure: It is defined as the annual aggregate sales for Latin America as reported by the company divided by total annu |
| 790 | `mdl77_varresirtn` | MATRIX | 0.616 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-Month Residual Return Variance: It is defined as the variance of a stock's monthly residual return in the last 24 months. The monthly res |
| 791 | `mdl77_pctchg3yfcf` | MATRIX | 0.612 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-yr Growth in TTM Free Cash Flow: It is defined as the percent change in a stock's most recent trailing 12-month free cash flow per share ( |
| 792 | `mdl77_gsg_shortsentimentfactor_util` | MATRIX | 0.607 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Utility |
| 793 | `mdl77_astcomp` | MATRIX | 0.604 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset Composition: It is defined as the total current assets from the most recent quarter divided by the total assets from the most recent q |
| 794 | `mdl77_curratio` | MATRIX | 0.604 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio: It is defined as the reported current assets from most recent quarter divided by the current liabilities from most recent qua |
| 795 | `mdl77_pcurlia` | MATRIX | 0.604 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Liabilities-to-Price: It is defined as a stock's most recently reported quarterly current liabilities per share divided by its closi |
| 796 | `mdl77_cashratio` | MATRIX | 0.604 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash & Equivalents-to-Current Liabilities: It is defined as the most recently reported quarterly cash & equivalents divided by current liabi |
| 797 | `mdl77_rel5yebitdap` | MATRIX | 0.603 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-yr Relative TTM EBITDA-to-Price: It is defined as a stock's current trailing 12-month EBITDA per share-to-price ratio (EBITDAP) minus the  |
| 798 | `mdl77_wcast` | MATRIX | 0.603 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working Capital-to-Total Assets: It is defined as the average working capital in the trailing 12 months divided by the average total assets  |
| 799 | `mdl77_rq` | MATRIX | 0.602 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio: It is defined as the current assets less inventories from the most recent quarter divided by the total current liabilities from |
| 800 | `mdl77_flowratio` | MATRIX | 0.602 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow Ratio: It is defined as the difference between current assets and cash & equivalents divided by the difference between current liabilit |
| 801 | `mdl77_nnastp` | MATRIX | 0.602 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Current Assets-to-Price: It is defined as the current assets per share minus total liabilities per share divided by the price. |
| 802 | `mdl77_yoychgcr` | MATRIX | 0.601 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year Change in Current Ratio: It is defined as the most recent reported quarterly current ratio and the current ratio for the same |
| 803 | `mdl77_global_cws` | MATRIX | 0.601 | 其他 | 0 | — | — | — | UNTESTED | Working Capital-to-Trailing 12-Month Sales: It is defined as the average of working capital for the trailing 12 months divided by the total  |
| 804 | `mdl77_pinoa` | MATRIX | 0.601 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Return on Net Operating Assets: It is defined as the trailing 12-month operating income after depreciation divided by the average net |
| 805 | `mdl77_chgreccast` | MATRIX | 0.600 | 盈利与财务 | 0 | — | — | — | UNTESTED | YOY Chg in Acct Receivable to Current Assets: It is defined as the percent change in the most recent quarterly reported accounts receivable  |
| 806 | `mdl77_rel5yfcfp` | MATRIX | 0.600 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-yr Relative TTM Free Cash Flow-to-Price: It is defined as a stock's current trailing 12-month free cash flow-to-price ratio (FCFP) minus t |
| 807 | `mdl77_rel5yocfp` | MATRIX | 0.599 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-yr Relative TTM Oper Cash Flow-to-Price: It is defined as a stock's current trailing 12-month operating cash flow-to-price ratio (OCFP) mi |
| 808 | `mdl77_iqa` | MATRIX | 0.597 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Asset Quality Index: It is defined as the year-over-year change of 1 minus the ratio of current assets plus PP&E divided by total assets |
| 809 | `mdl77_ocfratio` | MATRIX | 0.597 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Cash Flow Ratio: It is defined as a stock's most recently reported quarterly cash flow from operations divided by its current liab |
| 810 | `mdl77_ppa` | MATRIX | 0.594 | 其他 | 0 | — | — | — | UNUSABLE | Average Payable Period: It is defined as the average of the trailing 12-month accounts payable times 365 divided by the trailing 12-month co |
| 811 | `mdl77_rel5ycfp` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-yr Relative TTM Cash Flow-to-Price: It is defined as a stock's current trailing 12-month cash flow-to-price ratio (CFP) minus the average  |
| 812 | `mdl77_div5yg` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-Year Dividend Growth Rate: It is defined as the 5-year growth in dividends |
| 813 | `mdl77_global_pau` | MATRIX | 0.590 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Unexpected Change in Accounts Payable: It is defined as the difference between current accounts payable and the expected level of accounts p |
| 814 | `mdl77_cashc` | MATRIX | 0.589 | 其他 | 0 | — | — | — | UNUSABLE | Cash Cycle: It is defined as the average inventory days plus the average collection days minus the average payable days. |
| 815 | `mdl77_vmm_chgnoa` | MATRIX | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in Net Operating Assets: It is defined as the year-over-year change of net operating assets to total assets, where net operating asse |
| 816 | `mdl77_eur_vmm_chgnoa` | MATRIX | 0.582 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in Net Operating Assets: It is defined as the year-over-year change of net operating assets to total assets, where net operating asse |
| 817 | `mdl77_otvni` | MATRIX | 0.582 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inventory Turnover Ratio: It is defined as the trailing 12-month cost of goods sold divided by the average of inventory in the same period. |
| 818 | `mdl77_cogsinvt` | MATRIX | 0.577 | 其他 | 0 | — | — | — | UNUSABLE | Change in TTM COGS vs Inventory Level: It is defined as the absolute value of the difference between the yearly percent change in trailing 1 |
| 819 | `mdl77_divcf` | MATRIX | 0.576 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends-to-Cash Flow: It is defined as the trailing 12-month cash dividends divided by the trailing 12-month cash flow. Cash dividends rep |
| 820 | `mdl77_rel5ydivp` | MATRIX | 0.572 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-yr Relative TTM Dividend Yield: It is defined as a stock's current dividend yield (DivYield) minus the average of the DivYields in the las |
| 821 | `mdl177_vmm_chgnoa_alt` | MATRIX | 0.570 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year change in net operating assets including debt equity and cash |
| 822 | `mdl77_gsg_shortsentimentfactor_tni_ths` | MATRIX | 0.567 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Short Interest Ratio |
| 823 | `mdl77_ags` | MATRIX | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | SG&A Expenses-to-Sales: It is defined as the trailing 12-month selling, general management, and administration expenses divided by the trail |
| 824 | `mdl77_vnicw` | MATRIX | 0.558 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Working Capital to Inventory: It is defined as the most recent quarterly reported working capital divided by the inventory. Working capital  |
| 825 | `mdl77_chgsgasale` | MATRIX | 0.536 | 其他 | 0 | — | — | — | UNUSABLE | Change in QTR SG&A Expenses vs Sales: It is defined as the difference between the yearly change in quarterly Selling, General and Administra |
| 826 | `mdl77_idb` | MATRIX | 0.480 | 其他 | 0 | — | — | — | UNUSABLE | Basic Defensive Interval: It measures how many days that a company can cover its daily operating expenses (cost of goods sold and SG&A) by o |
| 827 | `mdl77_ccacw` | MATRIX | 0.463 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Working Capital Accruals: It equals to: Increase in Accounts Receivables + Increase in Inventory + Decrease in Accounts Payable and Accrued  |
| 828 | `mdl77_gsg_shortsentimentfactor_lend_supply` | MATRIX | 0.446 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Lend supply |
| 829 | `mdl77_indrelrecd_` | MATRIX | 0.409 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-adjusted Doubtful Account Receivables: It is defined as a stock's asset-adjusted annual doubtful receivables minus the average of t |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

