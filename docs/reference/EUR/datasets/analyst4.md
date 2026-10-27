# analyst4 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst4` |
| 名称 | Analyst Estimate Data for Equity |
| 类别 | ANALYST |
| 数据字段数(平台) | 776 |
| 覆盖率 | 0.6638 |
| 平台已有 alpha | 3083 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides intraday updates of consensus financial estimates, actuals, and company guidance for over 16,000 global companies, sourced from more than 800 contributing brokers. It includes multiple daily delta files per region, allowing users to track real-time changes in analyst expectations for key financial metrics such as EPS, sales, dividends, cash flow, and industry-specific items. The dataset also offers daily historical consensus timelines, enabling analysis of estimate revisions, surprises, and trends. By capturing the latest market sentiment and analyst forecasts, this data is highly valuable for predicting price movements, identifying earnings momentum, and responding to market-moving events as they unfold.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **776** |
| 类型分布 | MATRIX×565　VECTOR×211 |
| 平均覆盖率 | **0.664** |
| 覆盖率区间 | 0.16 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 171 | 22.0% |
| 中 (0.70–0.90) | 212 | 27.3% |
| 低 (0.50–0.70) | 138 | 17.8% |
| 稀疏 (<0.50) | 255 | 32.9% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 439 | 56.6% |
| UNUSABLE | 337 | 43.4% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 439 / UNUSABLE 337 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 353 | 0.70 | anl4_cff_flag、anl4_cfi_flag、anl4_fcfps_flag |
| 其他 | 251 | 0.60 | anl4_af_median_eps、anl4_sadaf_ptp_high、anl4_sadaf_ptp_low |
| 盈利与财务 | 163 | 0.69 | anl4_af_eps_high、anl4_af_eps_low、anl4_af_eps_mean |
| 搜索与替代数据 | 5 | 0.38 | anl4_sadaf_rd_exp_high、anl4_sadaf_rd_exp_low、anl4_sadaf_rd_exp_mean |
| 宏观与行业 | 2 | 0.86 | anl4_fs_actual_af_v4_nd_currency、actuals_reporting_currency |
| 风险与质量 | 2 | 0.77 | anl4_basicdetailrec_ratingvalue、anl4_eaz2lrec_ratingvalue |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl4_cff_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow From Financing Activities - forecast type (revision/new/...) |
| 2 | `anl4_cfi_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow From Investing - forecast type (revision/new/...) |
| 3 | `anl4_fcfps_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Free cash flow per share - forecast type (revision/new/...) |
| 4 | `anl4_ffo_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Funds from Operation - forecast type (revision/new/...) |
| 5 | `anl4_rd_exp_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Research and Development Expense - forecast type (revision/new/...) |
| 6 | `anl4_tbve_ft` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share - forecast type (revision/new/...) |
| 7 | `anl4_fcf_flag` | MATRIX | 0.991 | 修正与预期 | 0 | — | — | — | UNTESTED | Free cash flow - forecast type (revision/new/...) |
| 8 | `anl4_ptpr_flag` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Reported Pretax income - forecast type (revision/new/...) |
| 9 | `anl4_gric_flag` | MATRIX | 0.979 | 修正与预期 | 0 | — | — | — | UNTESTED | Gross income - forecast type (revision/new/...) |
| 10 | `anl4_cfo_flag` | MATRIX | 0.978 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow From Operations - forecast type (revision/new/...) |
| 11 | `anl4_capex_flag` | MATRIX | 0.976 | 修正与预期 | 0 | — | — | — | UNTESTED | Capital Expenditures - forecast type (revision/new/...) |
| 12 | `anl4_af_eps_high` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share - The highest estimation |
| 13 | `anl4_af_eps_low` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share - The lowest estimation |
| 14 | `anl4_af_eps_mean` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share - mean of estimations |
| 15 | `anl4_af_eps_number` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share - number of estimations |
| 16 | `anl4_af_median_eps` | MATRIX | 0.965 | 其他 | 0 | — | — | — | UNTESTED | EPS - aggregation on estimations, 50th-percentile |
| 17 | `anl4_af_div_high` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - The highest estimation |
| 18 | `anl4_af_div_low` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - The lowest value among forecasts |
| 19 | `anl4_af_div_mean` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - average of estimations |
| 20 | `anl4_af_div_median` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - median of estimations |
| 21 | `anl4_af_div_number` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - number of estimations |
| 22 | `anl4_sadaf_netprofit_high` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- The highest estimation |
| 23 | `anl4_sadaf_netprofit_low` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- The lowest estimation |
| 24 | `anl4_sadaf_netprofit_mean` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- mean of estimations |
| 25 | `anl4_sadaf_netprofit_median` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- median of estimations |
| 26 | `anl4_sadaf_netprofit_number` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- number of estimations |
| 27 | `anl4_qf_cfps_flag` | MATRIX | 0.964 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - forecast type (revision/new/...) |
| 28 | `sales_estimate_average_2` | MATRIX | 0.964 | 修正与预期 | 0 | — | — | — | UNTESTED | Average value of broker estimates for sales. |
| 29 | `sales_estimate_count_3` | MATRIX | 0.964 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of broker estimates for sales. |
| 30 | `sales_estimate_maximum_2` | MATRIX | 0.964 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest value among broker estimates for sales. |
| 31 | `sales_estimate_median` | MATRIX | 0.964 | 修正与预期 | 0 | — | — | — | UNTESTED | Median value of broker estimates for sales. |
| 32 | `sales_estimate_minimum_2` | MATRIX | 0.964 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest value among broker estimates for sales. |
| 33 | `anl4_sadaf_ebit_high` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - The highest estimation |
| 34 | `anl4_sadaf_ebit_low` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - The lowest estimation |
| 35 | `anl4_sadaf_ebit_mean` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - mean of estimations |
| 36 | `anl4_sadaf_ebit_median` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - median of estimations |
| 37 | `anl4_sadaf_ebit_number` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - number of estimations |
| 38 | `anl4_tot_gw_ft` | MATRIX | 0.960 | 修正与预期 | 0 | — | — | — | UNTESTED | Total Goodwill - forecast type (revision/new/...) |
| 39 | `anl4_sadaf_ptp_high` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Pretax income- The highest estimation |
| 40 | `anl4_sadaf_ptp_low` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Pretax income- The lowest estimation |
| 41 | `anl4_sadaf_ptp_mean` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Pretax income- mean of estimations |
| 42 | `anl4_sadaf_ptp_median` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Pretax income- median of estimations |
| 43 | `anl4_sadaf_ptp_number` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Pretax income- number of estimations |
| 44 | `shareholders_equity_estimate_average_af` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Average value of broker estimates for shareholders' equity (annual frequency). |
| 45 | `shareholders_equity_estimate_count_af` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of broker estimates for shareholders' equity (annual frequency). |
| 46 | `shareholders_equity_estimate_maximum` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest value among broker estimates for shareholders' equity. |
| 47 | `shareholders_equity_estimate_median` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Median value of broker estimates for shareholders' equity. |
| 48 | `shareholders_equity_estimate_minimum_af` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest value among broker estimates for shareholders' equity (annual frequency). |
| 49 | `anl4_sadaf_epsa_high` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - The highest estimation |
| 50 | `anl4_sadaf_epsa_low` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - The lowest estimation |
| 51 | `anl4_sadaf_epsa_mean` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - average of estimations |
| 52 | `anl4_sadaf_epsa_median` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - median of estimations |
| 53 | `anl4_sadaf_epsa_number` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - number of estimations |
| 54 | `anl4_qf_div_flag` | MATRIX | 0.956 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend - forecast type (revision/new/...), per share |
| 55 | `anl4_sadaf_epsr_high` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | GAAP Earnings per share - The highest estimation |
| 56 | `anl4_sadaf_epsr_low` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | GAAP Earnings per share - The lowest estimation |
| 57 | `anl4_sadaf_epsr_mean` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | GAAP Earnings per share - mean of estimations |
| 58 | `anl4_sadaf_epsr_number` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | GAAP Earnings per share - number of estimations |
| 59 | `anl4_sadaf_median_epsreported` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | GAAP Earnings per share - median of estimations |
| 60 | `anl4_fs_detail_estimate_basic_af_v4_nd_currency` | VECTOR | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code in which the estimate is reported |
| 61 | `anl4_sadaf_netprofita_high` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted net income- The highest estimation |
| 62 | `anl4_sadaf_netprofita_low` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted net income- The lowest estimation |
| 63 | `anl4_sadaf_netprofita_mean` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted net income- mean of estimations |
| 64 | `anl4_sadaf_netprofita_median` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted net income- median of estimations |
| 65 | `anl4_sadaf_netprofita_number` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted net income- number of estimations |
| 66 | `anl4_epsr_flag` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | GAAP Earnings - estimation type (revision/new/...), per share |
| 67 | `anl4_adjusted_netincome_ft` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted net income - forecast type (revision/new/...) |
| 68 | `anl4_epsa_flag` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - forecast type (revision/new/...) |
| 69 | `anl4_fs_detail_estimates_basic_af_nd_eps_high` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share - highest estimate |
| 70 | `anl4_fs_detail_estimates_basic_af_nd_eps_low` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share - lowest estimate |
| 71 | `anl4_fs_detail_estimates_basic_af_nd_eps_mean` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share - mean of estimates |
| 72 | `anl4_fs_detail_estimates_basic_af_nd_eps_median` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share - median (50th percentile) of estimates |
| 73 | `anl4_fs_detail_estimates_basic_af_nd_eps_number` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share - number of estimates |
| 74 | `anl4_fs_detail_estimates_basic_af_nd_div_high` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share - highest estimate |
| 75 | `anl4_fs_detail_estimates_basic_af_nd_div_low` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share - lowest estimate |
| 76 | `anl4_fs_detail_estimates_basic_af_nd_div_mean` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share - average of estimates |
| 77 | `anl4_fs_detail_estimates_basic_af_nd_div_median` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share - median of estimates |
| 78 | `anl4_fs_detail_estimates_basic_af_nd_div_number` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share - number of estimates |
| 79 | `anl4_fs_detail_estimate_af_v4_nd_estimate` | VECTOR | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Current analyst estimate value for the item and fiscal period |
| 80 | `anl4_fs_detail_estimates_advanced_af_nd_netprofit_high` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit, highest estimate |
| 81 | `anl4_fs_detail_estimates_advanced_af_nd_netprofit_low` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit, lowest estimate |
| 82 | `anl4_fs_detail_estimates_advanced_af_nd_netprofit_mean` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit, mean estimate |
| 83 | `anl4_fs_detail_estimates_advanced_af_nd_netprofit_median` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit, median estimate |
| 84 | `anl4_fs_detail_estimates_advanced_af_nd_netprofit_number` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit, number of estimates |
| 85 | `anl4_fs_detail_estimates_basic_af_nd_sales_high` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for sales revenue |
| 86 | `anl4_fs_detail_estimates_basic_af_nd_sales_low` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for sales revenue |
| 87 | `anl4_fs_detail_estimates_basic_af_nd_sales_mean` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of analyst estimates for sales revenue |
| 88 | `anl4_fs_detail_estimates_basic_af_nd_sales_median` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for sales revenue |
| 89 | `anl4_fs_detail_estimates_basic_af_nd_sales_number` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for sales revenue |
| 90 | `anl4_fs_detail_estimate_basic_af_v4_nd_estimate` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Current estimate value reported by the broker/analyst for the item and period |
| 91 | `anl4_fs_detail_estimates_advanced_af_nd_ebit_high` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual estimate for EBIT |
| 92 | `anl4_fs_detail_estimates_advanced_af_nd_ebit_low` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual estimate for EBIT |
| 93 | `anl4_fs_detail_estimates_advanced_af_nd_ebit_mean` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual estimates for EBIT |
| 94 | `anl4_fs_detail_estimates_advanced_af_nd_ebit_median` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual estimates for EBIT |
| 95 | `anl4_fs_detail_estimates_advanced_af_nd_ebit_number` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst annual estimates for EBIT |
| 96 | `anl4_sadaf_bvps_high` | MATRIX | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Book value - the highest estimation, per share |
| 97 | `anl4_sadaf_bvps_low` | MATRIX | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Book value - the lowest estimation, per share |
| 98 | `anl4_sadaf_bvps_mean` | MATRIX | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Book value per share - average of estimations |
| 99 | `anl4_sadaf_bvps_median` | MATRIX | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Book value per share - Median value among forecasts |
| 100 | `anl4_sadaf_bvps_number` | MATRIX | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Book value per share - number of estimations |
| 101 | `anl4_fs_detail_estimate_af_v4_nd_previosestimate` | VECTOR | 0.947 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value from this analyst before the current revision |
| 102 | `anl4_fs_detail_estimates_advanced_af_nd_ptp_high` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income, highest analyst estimate |
| 103 | `anl4_fs_detail_estimates_advanced_af_nd_ptp_low` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income, lowest analyst estimate |
| 104 | `anl4_fs_detail_estimates_advanced_af_nd_ptp_mean` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income, mean of analyst estimates |
| 105 | `anl4_fs_detail_estimates_advanced_af_nd_ptp_median` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income, median of analyst estimates |
| 106 | `anl4_fs_detail_estimates_advanced_af_nd_ptp_number` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income, number of analyst estimates |
| 107 | `anl4_fs_detail_estimate_basic_af_v4_nd_previosestimate` | VECTOR | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value from the same broker/analyst prior to this revision |
| 108 | `anl4_fs_actual_af_v4_nd_currency` | VECTOR | 0.944 | 宏观与行业 | 0 | — | — | — | UNTESTED | Home currency of the instrument in which the actual value is reported |
| 109 | `anl4_fs_detail_estimates_advanced_af_nd_sh_equity_high` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual estimate for Shareholders' Equity |
| 110 | `anl4_fs_detail_estimates_advanced_af_nd_sh_equity_low` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual estimate for Shareholders' Equity |
| 111 | `anl4_fs_detail_estimates_advanced_af_nd_sh_equity_mean` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual estimates for Shareholders' Equity |
| 112 | `anl4_fs_detail_estimates_advanced_af_nd_sh_equity_median` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual estimates for Shareholders' Equity |
| 113 | `anl4_fs_detail_estimates_advanced_af_nd_sh_equity_number` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst annual estimates for Shareholders' Equity |
| 114 | `anl4_fs_detail_estimates_advanced_af_nd_epsa_high` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate of adjusted EPS excluding extraordinary items and stock option expenses for the annual period |
| 115 | `anl4_fs_detail_estimates_advanced_af_nd_epsa_low` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate of adjusted EPS excluding extraordinary items and stock option expenses for the annual period |
| 116 | `anl4_fs_detail_estimates_advanced_af_nd_epsa_mean` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates of adjusted EPS excluding extraordinary items and stock option expenses for the annual period |
| 117 | `anl4_fs_detail_estimates_advanced_af_nd_epsa_median` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates of adjusted EPS excluding extraordinary items and stock option expenses for the annual period |
| 118 | `anl4_fs_detail_estimates_advanced_af_nd_epsa_number` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates of adjusted EPS excluding extraordinary items and stock option expenses for the annual period |
| 119 | `anl4_fs_detail_lt_v4_nd_estimate` | VECTOR | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Current estimate value reported by the analyst |
| 120 | `anl4_fs_detail_estimates_advanced_af_nd_epsr_high` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate of reported (GAAP) earnings per share for the annual period |
| 121 | `anl4_fs_detail_estimates_advanced_af_nd_epsr_low` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate of reported (GAAP) earnings per share for the annual period |
| 122 | `anl4_fs_detail_estimates_advanced_af_nd_epsr_mean` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates of reported (GAAP) earnings per share for the annual period |
| 123 | `anl4_fs_detail_estimates_advanced_af_nd_epsr_median` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates of reported (GAAP) earnings per share for the annual period |
| 124 | `anl4_fs_detail_estimates_advanced_af_nd_epsr_number` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates of reported (GAAP) earnings per share for the annual period |
| 125 | `anl4_sadaf_totassets_high` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Assets - The highest estimation |
| 126 | `anl4_sadaf_totassets_low` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Assets - The lowest estimation |
| 127 | `anl4_sadaf_totassets_mean` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Assets - mean of estimations |
| 128 | `anl4_sadaf_totassets_median` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Assets - median of estimations |
| 129 | `anl4_sadaf_totassets_number` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Assets - number of estimations |
| 130 | `anl4_fs_detail_rec_v4_nd_estimate` | VECTOR | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendation value/rating provided by the broker/analyst |
| 131 | `anl4_ebitda_flag` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation and amortization - forecast type (revision/new/...) |
| 132 | `anl4_fs_detail_estimates_advanced_af_nd_netprofita_high` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit Attributable, highest estimate |
| 133 | `anl4_fs_detail_estimates_advanced_af_nd_netprofita_low` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit Attributable, lowest estimate |
| 134 | `anl4_fs_detail_estimates_advanced_af_nd_netprofita_mean` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit Attributable, mean estimate |
| 135 | `anl4_fs_detail_estimates_advanced_af_nd_netprofita_median` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit Attributable, median estimate |
| 136 | `anl4_fs_detail_estimates_advanced_af_nd_netprofita_number` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit Attributable, number of estimates |
| 137 | `anl4_fs_detail_lt_v4_nd_previosestimate` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value prior to the latest revision |
| 138 | `anl4_fs_detail_estimates_advanced_af_nd_bvps_high` | MATRIX | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate of book value per share for the annual period |
| 139 | `anl4_fs_detail_estimates_advanced_af_nd_bvps_low` | MATRIX | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate of book value per share for the annual period |
| 140 | `anl4_fs_detail_estimates_advanced_af_nd_bvps_mean` | MATRIX | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates of book value per share for the annual period |
| 141 | `anl4_fs_detail_estimates_advanced_af_nd_bvps_median` | MATRIX | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates of book value per share for the annual period |
| 142 | `anl4_fs_detail_estimates_advanced_af_nd_bvps_number` | MATRIX | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates of book value per share for the annual period |
| 143 | `anl4_fs_detail_estimates_advanced_af_nd_totassets_high` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest individual analyst estimate for Total Assets for the annual forecast period |
| 144 | `anl4_fs_detail_estimates_advanced_af_nd_totassets_low` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest individual analyst estimate for Total Assets for the annual forecast period |
| 145 | `anl4_fs_detail_estimates_advanced_af_nd_totassets_mean` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for Total Assets for the annual forecast period |
| 146 | `anl4_fs_detail_estimates_advanced_af_nd_totassets_median` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for Total Assets for the annual forecast period |
| 147 | `anl4_fs_detail_estimates_advanced_af_nd_totassets_number` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates for Total Assets for the annual forecast period |
| 148 | `anl4_netprofit_flag` | MATRIX | 0.925 | 修正与预期 | 0 | — | — | — | UNTESTED | Net profit - forecast type (revision/new/...) |
| 149 | `anl4_totassets_flag` | MATRIX | 0.923 | 修正与预期 | 0 | — | — | — | UNTESTED | Total Assets - forecast type (revision/new/...) |
| 150 | `anl4_sadaf_ebitda_high` | MATRIX | 0.914 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation and amortization - The highest estimation |
| 151 | `anl4_sadaf_ebitda_low` | MATRIX | 0.914 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation and amortization - The lowest estimation |
| 152 | `anl4_sadaf_ebitda_mean` | MATRIX | 0.914 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation and amortization - mean of estimations |
| 153 | `anl4_sadaf_ebitda_number` | MATRIX | 0.914 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation and amortization - number of estimations |
| 154 | `anl4_sadaf_medianepsbfam` | MATRIX | 0.914 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation and amortization - median of estimations |
| 155 | `anl4_af_div_flag` | MATRIX | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend - forecast type (revision/new/...), per share |
| 156 | `anl4_netdebt_flag` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Net debt - forecast type (revision/new/...) |
| 157 | `anl4_sadaf_netdebt_high` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt- The highest estimation |
| 158 | `anl4_sadaf_netdebt_low` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt- The lowest estimation |
| 159 | `anl4_sadaf_netdebt_mean` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt- mean of estimations |
| 160 | `anl4_sadaf_netdebt_median` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt- median of estimations |
| 161 | `anl4_sadaf_netdebt_number` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt- number of estimations |
| 162 | `anl4_af_eps_flag` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | EPS - forecast type (revision/new/...) |
| 163 | `anl4_ptp_flag` | MATRIX | 0.903 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income - forecast type (revision/new/...) |
| 164 | `anl4_fsdtlestmtbasicafv4_item` | VECTOR | 0.902 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 165 | `anl4_bvps_flag` | MATRIX | 0.902 | 修正与预期 | 0 | — | — | — | UNTESTED | Book value per share - forecast type (revision/new/...) |
| 166 | `anl4_fs_detail_estimates_advanced_af_nd_ebitda_high` | MATRIX | 0.901 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual estimate for EBITDA |
| 167 | `anl4_fs_detail_estimates_advanced_af_nd_ebitda_low` | MATRIX | 0.901 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual estimate for EBITDA |
| 168 | `anl4_fs_detail_estimates_advanced_af_nd_ebitda_mean` | MATRIX | 0.901 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual estimates for EBITDA |
| 169 | `anl4_fs_detail_estimates_advanced_af_nd_ebitda_median` | MATRIX | 0.901 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual estimates for EBITDA |
| 170 | `anl4_fs_detail_estimates_advanced_af_nd_ebitda_number` | MATRIX | 0.901 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst annual estimates for EBITDA |
| 171 | `anl4_fsdtlestmtafv4_item` | VECTOR | 0.901 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 172 | `anl4_fsdetailrecv4_item` | VECTOR | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 173 | `anl4_sadaf_cfo_high` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Operations - The highest value among forecasts |
| 174 | `anl4_sadaf_cfo_low` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Operations - The lowest estimation |
| 175 | `anl4_sadaf_cfo_mean` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Operations - mean of estimations |
| 176 | `anl4_sadaf_cfo_median` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Operations - median of estimations |
| 177 | `anl4_sadaf_cfo_number` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Operations - number of estimations |
| 178 | `anl4_sadaf_ptpr_high` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Reported Pretax income- The highest estimation |
| 179 | `anl4_sadaf_ptpr_low` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Reported Pretax income- The lowest estimation |
| 180 | `anl4_sadaf_ptpr_mean` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Reported Pretax income- mean of estimations |
| 181 | `anl4_sadaf_ptpr_median` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Reported Pretax income- median of estimations |
| 182 | `anl4_sadaf_ptpr_number` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Reported Pretax income- number of estimations |
| 183 | `anl4_fs_detail_estimates_advanced_af_nd_netdebt_high` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual estimate for Net Debt |
| 184 | `anl4_fs_detail_estimates_advanced_af_nd_netdebt_low` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual estimate for Net Debt |
| 185 | `anl4_fs_detail_estimates_advanced_af_nd_netdebt_mean` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual estimates for Net Debt |
| 186 | `anl4_fs_detail_estimates_advanced_af_nd_netdebt_median` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual estimates for Net Debt |
| 187 | `anl4_fs_detail_estimates_advanced_af_nd_netdebt_number` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst annual estimates for Net Debt |
| 188 | `anl4_fsdetailltv4_item` | VECTOR | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 189 | `anl4_sadaf_capex_high` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Capital Expenditures - The highest estimation |
| 190 | `anl4_sadaf_capex_low` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Capital Expenditures - The lowest estimation |
| 191 | `anl4_sadaf_capex_mean` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Capital Expenditures - mean of estimations |
| 192 | `anl4_sadaf_capex_number` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Capital Expenditures - number of estimations |
| 193 | `anl4_sadaf_median_capexp` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Capital Expenditures - median of estimations |
| 194 | `anl4_sadaf_totgw_high` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Total Goodwill - The highest estimation |
| 195 | `anl4_sadaf_totgw_low` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Total Goodwill - The lowest estimation |
| 196 | `anl4_sadaf_totgw_mean` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Total Goodwill - mean of estimations |
| 197 | `anl4_sadaf_totgw_median` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Total Goodwill - median of estimations |
| 198 | `anl4_sadaf_totgw_number` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Total Goodwill - number of estimations |
| 199 | `anl4_qf_eps_flag` | MATRIX | 0.884 | 修正与预期 | 0 | — | — | — | UNTESTED | EPS - forecast type (revision/new/...) |
| 200 | `anl4_fs_actual_af_v4_nd_actual` | VECTOR | 0.884 | 其他 | 0 | — | — | — | UNTESTED | Reported actual value for the financial item |
| 201 | `anl4_fs_detail_estimates_advanced_af_nd_cfo_high` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow from Operations, highest estimate |
| 202 | `anl4_fs_detail_estimates_advanced_af_nd_cfo_low` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow from Operations, lowest estimate |
| 203 | `anl4_fs_detail_estimates_advanced_af_nd_cfo_mean` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow from Operations, mean estimate |
| 204 | `anl4_fs_detail_estimates_advanced_af_nd_cfo_median` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow from Operations, median estimate |
| 205 | `anl4_fs_detail_estimates_advanced_af_nd_cfo_number` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow from Operations, number of estimates |
| 206 | `anl4_fs_detail_estimates_advanced_af_nd_ptpr_high` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual reported pretax income |
| 207 | `anl4_fs_detail_estimates_advanced_af_nd_ptpr_low` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual reported pretax income |
| 208 | `anl4_fs_detail_estimates_advanced_af_nd_ptpr_mean` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analysts’ annual reported pretax income forecasts |
| 209 | `anl4_fs_detail_estimates_advanced_af_nd_ptpr_median` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analysts’ annual reported pretax income forecasts |
| 210 | `anl4_fs_detail_estimates_advanced_af_nd_ptpr_number` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates for annual reported pretax income |
| 211 | `anl4_sadaf_fcf_high` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow- aggregation on estimations, max |
| 212 | `anl4_sadaf_fcf_low` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow- The lowest estimation |
| 213 | `anl4_sadaf_fcf_mean` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow- mean of estimations |
| 214 | `anl4_sadaf_fcf_median` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow- aggregation on estimations, 50th-percentile |
| 215 | `anl4_sadaf_fcf_number` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow- number of estimations |
| 216 | `anl4_flag_erbfintax` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - forecast type (revision/new/...) |
| 217 | `anl4_fs_detail_estimates_advanced_af_nd_capex_high` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate of Capital Expenditures for the upcoming fiscal year |
| 218 | `anl4_fs_detail_estimates_advanced_af_nd_capex_low` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate of Capital Expenditures for the upcoming annual fiscal period |
| 219 | `anl4_fs_detail_estimates_advanced_af_nd_capex_mean` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for Capital Expenditures for the annual forecast |
| 220 | `anl4_fs_detail_estimates_advanced_af_nd_capex_median` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for Capital Expenditures for the annual forecast |
| 221 | `anl4_fs_detail_estimates_advanced_af_nd_capex_number` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for Capital Expenditures on an annual basis |
| 222 | `anl4_af_cfps_high` | MATRIX | 0.873 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow - The highest estimation, per share |
| 223 | `anl4_af_cfps_low` | MATRIX | 0.873 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - The lowest estimation |
| 224 | `anl4_af_cfps_mean` | MATRIX | 0.873 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - average of estimations |
| 225 | `anl4_af_cfps_median` | MATRIX | 0.873 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - Median value among forecasts |
| 226 | `anl4_af_cfps_number` | MATRIX | 0.873 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - number of estimations |
| 227 | `anl4_fs_actual_basic_af_v4_nd_actual` | VECTOR | 0.873 | 其他 | 0 | — | — | — | UNTESTED | Reported actual value of the financial item for the annual period |
| 228 | `anl4_fs_detail_estimates_advanced_af_nd_totgw_high` | MATRIX | 0.873 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for Total Goodwill for the annual forecast period |
| 229 | `anl4_fs_detail_estimates_advanced_af_nd_totgw_low` | MATRIX | 0.873 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for Total Goodwill for the annual forecast period |
| 230 | `anl4_fs_detail_estimates_advanced_af_nd_totgw_mean` | MATRIX | 0.873 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for Total Goodwill for the annual forecast period |
| 231 | `anl4_fs_detail_estimates_advanced_af_nd_totgw_median` | MATRIX | 0.873 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for Total Goodwill for the annual forecast period |
| 232 | `anl4_fs_detail_estimates_advanced_af_nd_totgw_number` | MATRIX | 0.873 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for Total Goodwill for the annual forecast period |
| 233 | `anl4_fsactualbasicafv4_item` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 234 | `anl4_fsactualafv4_item` | VECTOR | 0.869 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 235 | `anl4_fs_detail_estimates_advanced_af_nd_fcf_high` | MATRIX | 0.865 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual free cash flow |
| 236 | `anl4_fs_detail_estimates_advanced_af_nd_fcf_low` | MATRIX | 0.865 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual free cash flow |
| 237 | `anl4_fs_detail_estimates_advanced_af_nd_fcf_mean` | MATRIX | 0.865 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for annual free cash flow |
| 238 | `anl4_fs_detail_estimates_advanced_af_nd_fcf_median` | MATRIX | 0.865 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts for annual free cash flow |
| 239 | `anl4_fs_detail_estimates_advanced_af_nd_fcf_number` | MATRIX | 0.865 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual free cash flow |
| 240 | `anl4_bac1conaf_item` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 241 | `anl4_basicconaf_down` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Number of lower estimations |
| 242 | `anl4_basicconaf_high` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | The highest estimation |
| 243 | `anl4_basicconaf_low` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | The lowest estimation |
| 244 | `anl4_basicconaf_mean` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Mean of estimations |
| 245 | `anl4_basicconaf_median` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Median of estimations |
| 246 | `anl4_basicconaf_numest` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | The number of forecasts counted in aggregation |
| 247 | `anl4_basicconaf_pu` | VECTOR | 0.863 | 其他 | 0 | — | — | — | UNTESTED | The number of upper estimations |
| 248 | `anl4_ady_down` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | Number of lower estimations |
| 249 | `anl4_ady_high` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | The highest estimation |
| 250 | `anl4_ady_low` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | The lowest estimation |
| 251 | `anl4_ady_mean` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | Mean of estimations |
| 252 | `anl4_ady_median` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | Median of estimations |
| 253 | `anl4_ady_numest` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | The number of forecasts counted in aggregation |
| 254 | `anl4_ady_pu` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | The number of upper estimations |
| 255 | `anl4_cuo1conaf_item` | VECTOR | 0.862 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 256 | `anl4_fs_detail_estimates_basic_af_nd_cfps_high` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - highest estimate |
| 257 | `anl4_fs_detail_estimates_basic_af_nd_cfps_low` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - lowest estimate |
| 258 | `anl4_fs_detail_estimates_basic_af_nd_cfps_mean` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - average of estimates |
| 259 | `anl4_fs_detail_estimates_basic_af_nd_cfps_median` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - median of estimates |
| 260 | `anl4_fs_detail_estimates_basic_af_nd_cfps_number` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - number of estimates |
| 261 | `anl4_fs_detail_estimate_advanced_saf_v4_nd_estimate` | VECTOR | 0.852 | 修正与预期 | 0 | — | — | — | UNTESTED | Current estimate value provided by the analyst |
| 262 | `anl4_fsactualbasicafv4_actual` | VECTOR | 0.850 | 其他 | 0 | — | — | — | UNTESTED | Announced financial data |
| 263 | `anl4_af_cfps_flag` | MATRIX | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Cash Flow Per Share - forecast type (revision/new/...) |
| 264 | `anl4_fs_detail_estimate_basic_saf_v4_nd_estimate` | VECTOR | 0.843 | 修正与预期 | 0 | — | — | — | UNTESTED | Current estimate value provided by the broker/analyst |
| 265 | `anl4_fsactualafv4_actual` | VECTOR | 0.843 | 其他 | 0 | — | — | — | UNTESTED | Announced financial data |
| 266 | `anl4_bac1conlt_item` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 267 | `anl4_basicconlt_down` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | Number of lower estimations |
| 268 | `anl4_basicconlt_high` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | The highest estimation |
| 269 | `anl4_basicconlt_low` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | The lowest estimation |
| 270 | `anl4_basicconlt_mean` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | Mean of estimations |
| 271 | `anl4_basicconlt_median` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | Median of estimations |
| 272 | `anl4_basicconlt_numest` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | The number of forecasts counted in aggregation |
| 273 | `anl4_basicconlt_pu` | VECTOR | 0.839 | 其他 | 0 | — | — | — | UNTESTED | The number of upper estimations |
| 274 | `anl4_bac1detailaf_item` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 275 | `anl4_baz1_bk` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 276 | `anl4_baz1_person` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 277 | `anl4_baz1_estvalue` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 278 | `anl4_bac1detailrec_item` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 279 | `anl4_basicdetailrec_bk` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 280 | `anl4_basicdetailrec_person` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 281 | `anl4_baz1_prevval` | VECTOR | 0.837 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of financial item |
| 282 | `anl4_basicdetailrec_ratingvalue` | VECTOR | 0.835 | 风险与质量 | 0 | — | — | — | UNTESTED | Score on the given instrument |
| 283 | `anl4_ads1detailaf_bk` | VECTOR | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 284 | `anl4_ads1detailaf_person` | VECTOR | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 285 | `anl4_cuo1detailaf_item` | VECTOR | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 286 | `anl4_ads1detailaf_estvalue` | VECTOR | 0.833 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 287 | `anl4_ads1detailaf_prevval` | VECTOR | 0.832 | 其他 | 0 | — | — | — | UNTESTED | The Previous Estimation of Financial Item |
| 288 | `anl4_fs_detail_estimate_advanced_saf_v4_nd_previosestimate` | VECTOR | 0.831 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value for the financial item |
| 289 | `anl4_sadaf_fcfps_high` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share- The highest estimation |
| 290 | `anl4_sadaf_fcfps_low` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share- The lowest estimation |
| 291 | `anl4_sadaf_fcfps_mean` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share- mean of estimations |
| 292 | `anl4_sadaf_fcfps_median` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow- summary on estimations, 50th-percentile, per share |
| 293 | `anl4_sadaf_fcfps_number` | MATRIX | 0.824 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share- number of estimations |
| 294 | `anl4_fs_detail_estimate_basic_saf_v4_nd_previosestimate` | VECTOR | 0.821 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value prior to the current revision |
| 295 | `anl4_sadaf_gric_high` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Gross income- The highest estimation |
| 296 | `anl4_sadaf_gric_low` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Gross income- The lowest estimation |
| 297 | `anl4_sadaf_gric_mean` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Gross income- mean of estimations |
| 298 | `anl4_sadaf_gric_median` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Gross income- median of estimations |
| 299 | `anl4_sadaf_gric_number` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Gross income- number of estimations |
| 300 | `anl4_sadaf_cfi_high` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Investing - The highest estimation |
| 301 | `anl4_sadaf_cfi_low` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Investing - The lowest estimation |
| 302 | `anl4_sadaf_cfi_mean` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Investing - mean of estimations |
| 303 | `anl4_sadaf_cfi_median` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Investing - median of estimations |
| 304 | `anl4_sadaf_cfi_number` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Investing - number of estimations |
| 305 | `anl4_bac1conrec_item` | VECTOR | 0.814 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 306 | `anl4_buy` | VECTOR | 0.814 | 修正与预期 | 0 | — | — | — | UNTESTED | The number of recommendations to long the instrument |
| 307 | `anl4_hold` | VECTOR | 0.814 | 修正与预期 | 0 | — | — | — | UNTESTED | The number of recommendations not clear about short or long the instrument |
| 308 | `anl4_mark` | VECTOR | 0.814 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendation consensus score |
| 309 | `anl4_norec` | VECTOR | 0.814 | 修正与预期 | 0 | — | — | — | UNTESTED | The number of brokers with no recommendation |
| 310 | `anl4_sadaf_cff_high` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Financing - The highest of forecasted values |
| 311 | `anl4_sadaf_cff_low` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Financing - The lowest estimation |
| 312 | `anl4_sadaf_cff_mean` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Financing - mean of estimations |
| 313 | `anl4_sadaf_cff_median` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Financing Activities - Median value among forecasts |
| 314 | `anl4_sadaf_cff_number` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow From Financing - number of estimations |
| 315 | `anl4_total_rec` | VECTOR | 0.814 | 修正与预期 | 0 | — | — | — | UNTESTED | The total number of recommendations |
| 316 | `anl4_under` | VECTOR | 0.814 | 修正与预期 | 0 | — | — | — | UNTESTED | The number of Underweight recommendations |
| 317 | `anl4_fs_detail_estimates_advanced_af_nd_fcfps_high` | MATRIX | 0.811 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual free cash flow per share |
| 318 | `anl4_fs_detail_estimates_advanced_af_nd_fcfps_low` | MATRIX | 0.811 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual free cash flow per share |
| 319 | `anl4_fs_detail_estimates_advanced_af_nd_fcfps_mean` | MATRIX | 0.811 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for annual free cash flow per share |
| 320 | `anl4_fs_detail_estimates_advanced_af_nd_fcfps_median` | MATRIX | 0.811 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts for annual free cash flow per share |
| 321 | `anl4_fs_detail_estimates_advanced_af_nd_fcfps_number` | MATRIX | 0.811 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual free cash flow per share |
| 322 | `anl4_fs_detail_estimates_advanced_af_nd_grossincome_high` | MATRIX | 0.808 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual estimate for Gross Income |
| 323 | `anl4_fs_detail_estimates_advanced_af_nd_grossincome_low` | MATRIX | 0.808 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual estimate for Gross Income |
| 324 | `anl4_fs_detail_estimates_advanced_af_nd_grossincome_mean` | MATRIX | 0.808 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual estimates for Gross Income |
| 325 | `anl4_fs_detail_estimates_advanced_af_nd_grossincome_median` | MATRIX | 0.808 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual estimates for Gross Income |
| 326 | `anl4_fs_detail_estimates_advanced_af_nd_grossincome_number` | MATRIX | 0.808 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst annual estimates for Gross Income |
| 327 | `anl4_fs_detail_estimates_advanced_af_nd_cfi_high` | MATRIX | 0.806 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual cash flow from investing |
| 328 | `anl4_fs_detail_estimates_advanced_af_nd_cfi_low` | MATRIX | 0.806 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual cash flow from investing |
| 329 | `anl4_fs_detail_estimates_advanced_af_nd_cfi_mean` | MATRIX | 0.806 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for annual cash flow from investing |
| 330 | `anl4_fs_detail_estimates_advanced_af_nd_cfi_median` | MATRIX | 0.806 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts for annual cash flow from investing |
| 331 | `anl4_fs_detail_estimates_advanced_af_nd_cfi_number` | MATRIX | 0.806 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual cash flow from investing |
| 332 | `anl4_bac1detaillt_item` | VECTOR | 0.806 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 333 | `anl4_basicdetaillt_bk` | VECTOR | 0.806 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 334 | `anl4_basicdetaillt_person` | VECTOR | 0.806 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 335 | `anl4_basicdetaillt_estvalue` | VECTOR | 0.805 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 336 | `anl4_fs_detail_estimates_advanced_af_nd_cff_high` | MATRIX | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual cash flow from financing |
| 337 | `anl4_fs_detail_estimates_advanced_af_nd_cff_low` | MATRIX | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual cash flow from financing |
| 338 | `anl4_fs_detail_estimates_advanced_af_nd_cff_mean` | MATRIX | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates for annual cash flow from financing |
| 339 | `anl4_fs_detail_estimates_advanced_af_nd_cff_median` | MATRIX | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts for annual cash flow from financing |
| 340 | `anl4_fs_detail_estimates_advanced_af_nd_cff_number` | MATRIX | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual cash flow from financing |
| 341 | `anl4_basicdetaillt_prevval` | VECTOR | 0.801 | 其他 | 0 | — | — | — | UNTESTED | The Previous Estimation of Financial Item |
| 342 | `anl4_fs_detail_estimate_advanced_qf_v4_nd_estimate` | VECTOR | 0.779 | 修正与预期 | 0 | — | — | — | UNTESTED | Current broker-provided estimate value for the specified item and period |
| 343 | `anl4_dez1basicafv4_est` | VECTOR | 0.778 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 344 | `anl4_dez1basicafv4_preest` | VECTOR | 0.778 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of finanicial item |
| 345 | `estimate_value_currency_code` | VECTOR | 0.778 | 修正与预期 | 0 | — | — | — | UNTESTED | Home currency of instrument |
| 346 | `anl4_dez1afv4_est` | VECTOR | 0.778 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 347 | `anl4_dez1afv4_preest` | VECTOR | 0.778 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of finanicial item |
| 348 | `anl4_basicafv4_actual` | VECTOR | 0.777 | 其他 | 0 | — | — | — | UNTESTED | Announced financial data for the annual period. |
| 349 | `actuals_reporting_currency` | VECTOR | 0.776 | 宏观与行业 | 0 | — | — | — | UNTESTED | Home currency of instrument |
| 350 | `anl4_afv4_actual` | VECTOR | 0.776 | 其他 | 0 | — | — | — | UNTESTED | Announced financial data |
| 351 | `anl4_fs_detail_estimate_basic_qf_v4_nd_currency` | VECTOR | 0.776 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code in which the estimate is reported |
| 352 | `anl4_detailrecv4_est` | VECTOR | 0.775 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimation value for recommendation detail |
| 353 | `previous_recommendation_value` | VECTOR | 0.775 | 修正与预期 | 0 | — | — | — | UNTESTED | The previous estimation of financial item for recommendation |
| 354 | `anl4_detailltv4_est` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Long term estimation value |
| 355 | `anl4_detailltv4_preest` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of financial item |
| 356 | `anl4_fs_detail_estimate_basic_qf_v4_nd_estimate` | VECTOR | 0.769 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated value |
| 357 | `anl4_fsdtlestmtadvsafv4_item` | VECTOR | 0.767 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 358 | `anl4_fs_detail_estimate_advanced_qf_v4_nd_previosestimate` | VECTOR | 0.761 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value prior to the latest revision |
| 359 | `anl4_fs_detail_estimate_basic_qf_v4_nd_previosestimate` | VECTOR | 0.752 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous estimate value before the current revision |
| 360 | `sales_estimate_average_quarterly` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - mean of estimations |
| 361 | `sales_estimate_count_quarterly` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - number of estimations |
| 362 | `sales_estimate_maximum_quarterly` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - The highest estimation |
| 363 | `sales_estimate_median_quarterly` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - median of estimations |
| 364 | `sales_estimate_minimum_quarterly` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - The lowest estimation |
| 365 | `anl4_fs_detail_estimates_basic_qf_v4_nd_sales_high` | MATRIX | 0.727 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - the highest estimation |
| 366 | `anl4_fs_detail_estimates_basic_qf_v4_nd_sales_low` | MATRIX | 0.727 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - the lowest estimation |
| 367 | `anl4_fs_detail_estimates_basic_qf_v4_nd_sales_mean` | MATRIX | 0.727 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - mean of estimations |
| 368 | `anl4_fs_detail_estimates_basic_qf_v4_nd_sales_median` | MATRIX | 0.727 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - median of estimations |
| 369 | `anl4_fs_detail_estimates_basic_qf_v4_nd_sales_number` | MATRIX | 0.727 | 修正与预期 | 0 | — | — | — | UNTESTED | Sales - number of estimations |
| 370 | `anl4_dei3laf_item` | VECTOR | 0.724 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 371 | `anl4_eaz2laf_bk` | VECTOR | 0.724 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 372 | `anl4_eaz2laf_person` | VECTOR | 0.724 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 373 | `anl4_dei3lrec_item` | VECTOR | 0.722 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 374 | `anl4_eaz2lrec_bk` | VECTOR | 0.722 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 375 | `anl4_eaz2lrec_person` | VECTOR | 0.722 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 376 | `anl4_dei2laf_item` | VECTOR | 0.715 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 377 | `anl4_eaz1laf_bk` | VECTOR | 0.715 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 378 | `anl4_eaz1laf_person` | VECTOR | 0.715 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 379 | `anl4_eaz2laf_estvalue` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 380 | `anl4_eaz2laf_prevval` | VECTOR | 0.710 | 其他 | 0 | — | — | — | UNTESTED | The Previous Estimation of Financial Item |
| 381 | `anl4_eaz2lrec_ratingvalue` | VECTOR | 0.704 | 风险与质量 | 0 | — | — | — | UNTESTED | Score on the given instrument |
| 382 | `anl4_eaz1laf_estvalue` | VECTOR | 0.704 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 383 | `anl4_eaz1laf_prevval` | VECTOR | 0.702 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of financial item |
| 384 | `anl4_fsdtlestmtbasicsafv4_item` | VECTOR | 0.675 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 385 | `anl4_dei3llt_item` | VECTOR | 0.667 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 386 | `anl4_eaz2llt_bk` | VECTOR | 0.667 | 其他 | 0 | — | — | — | UNTESTED | Broker name (int) |
| 387 | `anl4_eaz2llt_person` | VECTOR | 0.667 | 其他 | 0 | — | — | — | UNTESTED | Broker Id |
| 388 | `anl4_dez1advancedsafv4_est` | VECTOR | 0.660 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 389 | `anl4_dez1advancedsafv4_preest` | VECTOR | 0.660 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of finanicial item |
| 390 | `anl4_eaz2llt_estvalue` | VECTOR | 0.655 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 391 | `anl4_dez1basicsafv4_est` | VECTOR | 0.654 | 其他 | 0 | — | — | — | UNTESTED | Estimation value |
| 392 | `anl4_dez1basicsafv4_preest` | VECTOR | 0.654 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of finanicial item |
| 393 | `anl4_fs_actual_basic_qf_v4_nd_actual` | VECTOR | 0.649 | 其他 | 0 | — | — | — | UNTESTED | Reported actual value for the item |
| 394 | `anl4_eaz2llt_prevval` | VECTOR | 0.649 | 其他 | 0 | — | — | — | UNTESTED | The previous estimation of financial item |
| 395 | `anl4_af_div_std` | MATRIX | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share - std of estimations |
| 396 | `anl4_fsactualbasicqfv4_item` | VECTOR | 0.646 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 397 | `anl4_af_dts_spe` | MATRIX | 0.645 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share - std of estimations |
| 398 | `anl4_adz_ebit_high` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - The highest estimation |
| 399 | `anl4_adz_ebit_low` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - The lowest estimation |
| 400 | `anl4_adz_ebit_mean` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - mean of estimations |
| 401 | `anl4_adz_ebit_median` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - median of estimations |
| 402 | `anl4_adz_ebit_number` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - number of estimations |
| 403 | `anl4_fs_detail_estimates_basic_af_nd_div_std` | MATRIX | 0.639 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share - standard deviation of estimates |
| 404 | `anl4_sadaf_dts_aspe` | MATRIX | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share adjusted by excluding extraordinary items and stock option expenses - std of estimations |
| 405 | `anl4_fs_detail_estimates_basic_af_nd_eps_std` | MATRIX | 0.635 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings per share - standard deviation of estimates |
| 406 | `sales_estimate_standard_deviation_2` | MATRIX | 0.634 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of broker estimates for sales. |
| 407 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_high` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - The highest estimation |
| 408 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_low` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes low estimate |
| 409 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_mean` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate of EBIT (Earnings Before Interest and Taxes) |
| 410 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_median` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of EBIT estimates |
| 411 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_number` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - number of estimations |
| 412 | `shareholders_equity_estimate_standard_deviation` | MATRIX | 0.631 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of broker estimates for shareholders' equity. |
| 413 | `anl4_fsdtlestmtadvancedqfv4_item` | VECTOR | 0.630 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 414 | `anl4_sadaf_netprofit_std` | MATRIX | 0.629 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- std of estimations |
| 415 | `anl4_basicqfv4_actual` | VECTOR | 0.629 | 其他 | 0 | — | — | — | UNTESTED | Announced financial data |
| 416 | `anl4_sadaf_ebit_std` | MATRIX | 0.628 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes - std of estimations |
| 417 | `anl4_fs_detail_estimates_advanced_af_nd_epsa_std` | MATRIX | 0.627 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates of adjusted EPS excluding extraordinary items and stock option expenses for the annual period |
| 418 | `anl4_sadaf_dts_rspe` | MATRIX | 0.625 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported Earnings per share - standard deviation of estimations |
| 419 | `anl4_fsdtlestmtbasicqfv4_item` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | Financial item |
| 420 | `anl4_fs_detail_estimates_basic_af_nd_sales_std` | MATRIX | 0.625 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of sales revenue estimates |
| 421 | `anl4_sadaf_dts_ptp` | MATRIX | 0.622 | 其他 | 0 | — | — | — | UNTESTED | Pretax income- std of estimations |
| 422 | `anl4_fs_detail_estimates_advanced_af_nd_sh_equity_std` | MATRIX | 0.622 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst annual estimates for Shareholders' Equity |
| 423 | `anl4_fs_detail_estimates_advanced_af_nd_netprofit_std` | MATRIX | 0.620 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit, standard deviation of estimates |
| 424 | `anl4_adz_netprofit_high` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- The highest estimation |
| 425 | `anl4_adz_netprofit_low` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- The lowest estimation |
| 426 | `anl4_adz_netprofit_mean` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- mean of estimations |
| 427 | `anl4_adz_netprofit_median` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- median of estimations |
| 428 | `anl4_adz_netprofit_number` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit- number of estimations |
| 429 | `anl4_fs_detail_estimates_advanced_af_nd_ebit_std` | MATRIX | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst annual estimates for EBIT |
| 430 | `anl4_fs_detail_estimates_advanced_af_nd_epsr_std` | MATRIX | 0.616 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates of reported (GAAP) earnings per share for the annual period |
| 431 | `anl4_fs_detail_estimates_advanced_af_nd_ptp_std` | MATRIX | 0.613 | 修正与预期 | 0 | — | — | — | UNTESTED | Pretax income, standard deviation of analyst estimates |
| 432 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofit_high` | MATRIX | 0.610 | 修正与预期 | 0 | — | — | — | UNTESTED | Net profit - the highest estimation |
| 433 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofit_low` | MATRIX | 0.610 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest estimate of Net Profit |
| 434 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofit_mean` | MATRIX | 0.610 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate of Net Profit |
| 435 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofit_median` | MATRIX | 0.610 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of Net Profit estimates |
| 436 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofit_number` | MATRIX | 0.610 | 修正与预期 | 0 | — | — | — | UNTESTED | Net profit - number of estimations |
| 437 | `anl4_sadaf_netprofita_std` | MATRIX | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted net income- std of estimations |
| 438 | `anl4_sadaf_dts_spvb` | MATRIX | 0.605 | 其他 | 0 | — | — | — | UNTESTED | Book value per share - std of estimations |
| 439 | `anl4_fs_detail_estimates_advanced_af_nd_netprofita_std` | MATRIX | 0.601 | 修正与预期 | 0 | — | — | — | UNTESTED | Net Profit Attributable, standard deviation of estimates |
| 440 | `anl4_fsactualqfv4_item` | VECTOR | 0.596 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 441 | `anl4_fs_detail_estimates_advanced_af_nd_bvps_std` | MATRIX | 0.596 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates of book value per share for the annual period |
| 442 | `anl4_qfv4_eps_high` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - The highest estimation |
| 443 | `anl4_qfv4_eps_low` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - The lowest estimation |
| 444 | `anl4_qfv4_eps_mean` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - mean of estimations |
| 445 | `anl4_qfv4_eps_number` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - number of estimations |
| 446 | `anl4_qfv4_median_eps` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - median of estimations |
| 447 | `anl4_dez1basicqfv4_est` | VECTOR | 0.593 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 448 | `anl4_dez1basicqfv4_preest` | VECTOR | 0.593 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of finanicial item |
| 449 | `estimate_value_currency_code_qtr` | VECTOR | 0.593 | 修正与预期 | 0 | — | — | — | UNUSABLE | Home currency of instrument |
| 450 | `anl4_adz_ptp_high` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Pretax income- The highest estimation |
| 451 | `anl4_adz_ptp_low` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Pretax income- The lowest estimation |
| 452 | `anl4_adz_ptp_mean` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Pretax income- mean of estimations |
| 453 | `anl4_adz_ptp_median` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Pretax income- median of estimations |
| 454 | `anl4_adz_ptp_number` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Pretax income- number of estimations |
| 455 | `anl4_qfv4_actual` | VECTOR | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Announced financial data |
| 456 | `anl4_dez1advancedqfv4_est` | VECTOR | 0.588 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 457 | `anl4_dez1advancedqfv4_preest` | VECTOR | 0.588 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of finanicial item |
| 458 | `anl4_fs_detail_estimates_basic_qf_v4_nd_eps_high` | MATRIX | 0.585 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share - highest estimation |
| 459 | `anl4_fs_detail_estimates_basic_qf_v4_nd_eps_low` | MATRIX | 0.585 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share - lowest estimation |
| 460 | `anl4_fs_detail_estimates_basic_qf_v4_nd_eps_mean` | MATRIX | 0.585 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share - mean of estimations |
| 461 | `anl4_fs_detail_estimates_basic_qf_v4_nd_eps_median` | MATRIX | 0.585 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share - 50th percentile (median) of estimations |
| 462 | `anl4_fs_detail_estimates_basic_qf_v4_nd_eps_number` | MATRIX | 0.585 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share - number of estimations |
| 463 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptp_high` | MATRIX | 0.581 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate of Pretax Income |
| 464 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptp_low` | MATRIX | 0.581 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pretax income - the lowest estimation |
| 465 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptp_mean` | MATRIX | 0.581 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate of Pretax Income |
| 466 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptp_median` | MATRIX | 0.581 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate of Pretax Income |
| 467 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptp_number` | MATRIX | 0.581 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Pretax Income estimates |
| 468 | `anl4_sadaf_dts_ofc` | MATRIX | 0.581 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - std of estimations |
| 469 | `anl4_fs_actual_qf_v4_nd_actual` | VECTOR | 0.580 | 其他 | 0 | — | — | — | UNUSABLE | Reported actual value for the specified item |
| 470 | `anl4_af_cfps_value` | MATRIX | 0.577 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow Per Share - announced financial value |
| 471 | `anl4_sadaf_ebitda_std` | MATRIX | 0.577 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - std of estimations |
| 472 | `anl4_sadaf_totassets_std` | MATRIX | 0.574 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - std of estimations |
| 473 | `anl4_fs_detail_estimates_advanced_af_nd_cfo_std` | MATRIX | 0.572 | 修正与预期 | 0 | — | — | — | UNUSABLE | Cash Flow from Operations, standard deviation of estimates |
| 474 | `anl4_sadaf_netdebt_std` | MATRIX | 0.572 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net debt- std of estimations |
| 475 | `anl4_fs_detail_estimates_advanced_af_nd_ebitda_std` | MATRIX | 0.568 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst annual estimates for EBITDA |
| 476 | `anl4_fs_detail_estimates_advanced_af_nd_totassets_std` | MATRIX | 0.566 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for Total Assets for the annual forecast period |
| 477 | `anl4_fs_detail_estimates_advanced_af_nd_netdebt_std` | MATRIX | 0.564 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst annual estimates for Net Debt |
| 478 | `anl4_sadaf_dts_fcf` | MATRIX | 0.549 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow- std of estimations |
| 479 | `anl4_sadaf_capex_std` | MATRIX | 0.545 | 其他 | 0 | — | — | — | UNUSABLE | Capital Expenditures - std of estimations |
| 480 | `anl4_fsactualbasicqfv4_actual` | VECTOR | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Announced financial data |
| 481 | `anl4_fs_detail_estimates_advanced_af_nd_fcf_std` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for annual free cash flow |
| 482 | `anl4_adz_ebitda_high` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - The highest estimation |
| 483 | `anl4_adz_ebitda_low` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - The lowest estimation |
| 484 | `anl4_adz_ebitda_mean` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - mean of estimations |
| 485 | `anl4_adz_ebitda_number` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - number of estimations |
| 486 | `anl4_adz_medianepsbfam` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - median of estimations |
| 487 | `anl4_fs_detail_estimates_advanced_af_nd_capex_std` | MATRIX | 0.537 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for Capital Expenditures on an annual basis |
| 488 | `anl4_adz_netdebt_high` | MATRIX | 0.534 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net debt- The highest estimation |
| 489 | `anl4_adz_netdebt_low` | MATRIX | 0.534 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net debt- The lowest estimation |
| 490 | `anl4_adz_netdebt_mean` | MATRIX | 0.534 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net debt- mean of estimations |
| 491 | `anl4_adz_netdebt_median` | MATRIX | 0.534 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net debt- median of estimations |
| 492 | `anl4_adz_netdebt_number` | MATRIX | 0.534 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net debt- number of estimations |
| 493 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebitda_high` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate of EBITDA |
| 494 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebitda_low` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization low estimate |
| 495 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebitda_mean` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate of EBITDA |
| 496 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebitda_median` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of EBITDA estimates |
| 497 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebitda_number` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBITDA estimates |
| 498 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netdebt_high` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate of Net Debt |
| 499 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netdebt_low` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Net Debt lowest estimate |
| 500 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netdebt_mean` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of Net Debt estimates |
| 501 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netdebt_median` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Net Debt median of estimates |
| 502 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netdebt_number` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Net debt - number of estimations |
| 503 | `anl4_adz_netprofita_high` | MATRIX | 0.510 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net income- The highest estimation |
| 504 | `anl4_adz_netprofita_low` | MATRIX | 0.510 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net income- The lowest estimation |
| 505 | `anl4_adz_netprofita_mean` | MATRIX | 0.510 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net income- mean of estimations |
| 506 | `anl4_adz_netprofita_median` | MATRIX | 0.510 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net income- median of estimations |
| 507 | `anl4_adz_netprofita_number` | MATRIX | 0.510 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net income- number of estimations |
| 508 | `anl4_fs_guidance_af_v4_nd_estimate` | VECTOR | 0.508 | 修正与预期 | 0 | — | — | — | UNUSABLE | Point guidance estimate value for the item |
| 509 | `anl4_fs_guidance_af_v4_nd_maxguidance` | VECTOR | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Maximum value of the company’s annual guidance range for the item |
| 510 | `anl4_fs_guidance_af_v4_nd_minguidance` | VECTOR | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Minimum value of the company’s annual guidance range for the item |
| 511 | `anl4_bac1actualqf_item` | VECTOR | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 512 | `anl4_adz_epsa_high` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted by excluding extraordinary items and stock option expenses - The highest estimation |
| 513 | `anl4_adz_epsa_low` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted by excluding extraordinary items and stock option expenses - The lowest estimation |
| 514 | `anl4_adz_epsa_mean` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted by excluding extraordinary items and stock option expenses - average of estimations |
| 515 | `anl4_adz_epsa_median` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted by excluding extraordinary items and stock option expenses - median of estimations |
| 516 | `anl4_adz_epsa_number` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted by excluding extraordinary items and stock option expenses - number of estimations |
| 517 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofita_high` | MATRIX | 0.503 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted Net Income highest estimate |
| 518 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofita_low` | MATRIX | 0.503 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted net income - lowest estimate |
| 519 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofita_mean` | MATRIX | 0.503 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted Net Income mean of estimates |
| 520 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofita_median` | MATRIX | 0.503 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of Adjusted Net Profit (Net Profit Attributable) estimates |
| 521 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofita_number` | MATRIX | 0.503 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Net Profit Attributable estimates |
| 522 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsa_high` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | High estimate of Earnings Per Share (Actual) |
| 523 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsa_low` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted (excluding extraordinary items and stock option expenses) - lowest estimate |
| 524 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsa_mean` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted by excluding extraordinary items and stock option expenses - average of estimations |
| 525 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsa_median` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate of Earnings Per Share (Actual) |
| 526 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsa_number` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share adjusted (excluding extraordinary items and stock option expenses) - number of estimations |
| 527 | `selling_general_admin_expense_estimate_average` | MATRIX | 0.494 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average value of broker estimates for selling, general, and administrative expenses. |
| 528 | `selling_general_admin_expense_estimate_count` | MATRIX | 0.494 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of broker estimates for selling, general, and administrative expenses. |
| 529 | `selling_general_admin_expense_estimate_maximum` | MATRIX | 0.494 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest value among broker estimates for selling, general, and administrative expenses. |
| 530 | `selling_general_admin_expense_estimate_median` | MATRIX | 0.494 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of broker estimates for selling, general, and administrative expenses. |
| 531 | `selling_general_admin_expense_estimate_minimum` | MATRIX | 0.494 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest value among broker estimates for selling, general, and administrative expenses. |
| 532 | `quarterly_shareholders_equity_high` | MATRIX | 0.492 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest value of shareholders’ equity estimate for the quarter. |
| 533 | `quarterly_shareholders_equity_median` | MATRIX | 0.492 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of shareholders’ equity estimate for the quarter. |
| 534 | `shareholders_equity_estimate_average` | MATRIX | 0.492 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average value of broker estimates for shareholders' equity. |
| 535 | `shareholders_equity_estimate_count` | MATRIX | 0.492 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of broker estimates for shareholders' equity. |
| 536 | `shareholders_equity_estimate_minimum` | MATRIX | 0.492 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest value among broker estimates for shareholders' equity. |
| 537 | `anl4_af_dts_spfc` | MATRIX | 0.491 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow Per Share - std of estimations |
| 538 | `anl4_fs_detail_estimates_advanced_af_nd_sga_high` | MATRIX | 0.487 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest individual analyst estimate for Selling, General and Administrative expenses for the annual forecast period |
| 539 | `anl4_fs_detail_estimates_advanced_af_nd_sga_low` | MATRIX | 0.487 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest individual analyst estimate for Selling, General and Administrative expenses for the annual forecast period |
| 540 | `anl4_fs_detail_estimates_advanced_af_nd_sga_mean` | MATRIX | 0.487 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of analyst estimates for Selling, General and Administrative expenses for the annual forecast period |
| 541 | `anl4_fs_detail_estimates_advanced_af_nd_sga_median` | MATRIX | 0.487 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates for Selling, General and Administrative expenses for the annual forecast period |
| 542 | `anl4_fs_detail_estimates_advanced_af_nd_sga_number` | MATRIX | 0.487 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing analyst estimates for Selling, General and Administrative expenses for the annual forecast period |
| 543 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_sh_equity_high` | MATRIX | 0.485 | 修正与预期 | 0 | — | — | — | UNUSABLE | High estimate for Shareholder Equity |
| 544 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_sh_equity_low` | MATRIX | 0.485 | 修正与预期 | 0 | — | — | — | UNUSABLE | Low estimate for Shareholder Equity |
| 545 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_sh_equity_mean` | MATRIX | 0.485 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate for Shareholder Equity |
| 546 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_sh_equity_median` | MATRIX | 0.485 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate of Shareholders' Equity |
| 547 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_sh_equity_number` | MATRIX | 0.485 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for Shareholders’ Equity |
| 548 | `anl4_fs_detail_estimates_basic_af_nd_cfps_std` | MATRIX | 0.484 | 修正与预期 | 0 | — | — | — | UNUSABLE | Cash Flow Per Share - standard deviation of estimates |
| 549 | `anl4_cuo1actualqf_item` | VECTOR | 0.480 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 550 | `anl4_bac1detailqf_item` | VECTOR | 0.472 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 551 | `anl4_basicdetailqf_bk` | VECTOR | 0.472 | 其他 | 0 | — | — | — | UNUSABLE | Broker name (int) |
| 552 | `anl4_basicdetailqf_person` | VECTOR | 0.472 | 其他 | 0 | — | — | — | UNUSABLE | Broker Id |
| 553 | `anl4_basicdetailqf_estvalue` | VECTOR | 0.472 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 554 | `anl4_sadaf_tbvps_high` | MATRIX | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Tangible Book Value per Share - The highest estimation |
| 555 | `anl4_sadaf_tbvps_low` | MATRIX | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Tangible Book Value per Share - The lowest estimation |
| 556 | `anl4_sadaf_tbvps_mean` | MATRIX | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Tangible Book Value per Share - mean of estimations |
| 557 | `anl4_sadaf_tbvps_median` | MATRIX | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Tangible Book Value per Share - median of estimations |
| 558 | `anl4_sadaf_tbvps_number` | MATRIX | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Tangible Book Value per Share - number of estimations |
| 559 | `anl4_adxqf_down` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Number of lower estimations |
| 560 | `anl4_adxqf_high` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | The highest estimation |
| 561 | `anl4_adxqf_low` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | The lowest estimation |
| 562 | `anl4_adxqf_mean` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Mean of estimations |
| 563 | `anl4_adxqf_median` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Median of estimations |
| 564 | `anl4_adxqf_numest` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | The number of forecasts counted in aggregation |
| 565 | `anl4_adxqf_pu` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | The number of upper estimations |
| 566 | `anl4_cuo1conqf_item` | VECTOR | 0.471 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 567 | `anl4_bac1conqf_item` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 568 | `anl4_basicconqf_down` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | Number of lower estimations |
| 569 | `anl4_basicconqf_high` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | The highest estimation |
| 570 | `anl4_basicconqf_low` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | The lowest estimation |
| 571 | `anl4_basicconqf_mean` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | Mean of estimations |
| 572 | `anl4_basicconqf_median` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | Median of estimations |
| 573 | `anl4_basicconqf_numest` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | The number of forecasts counted in aggregation |
| 574 | `anl4_basicconqf_pu` | VECTOR | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | The number of upper estimations |
| 575 | `anl4_fs_detail_estimates_advanced_af_nd_tbvps_high` | MATRIX | 0.464 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate of tangible book value per share for the annual period |
| 576 | `anl4_fs_detail_estimates_advanced_af_nd_tbvps_low` | MATRIX | 0.464 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate of tangible book value per share for the annual period |
| 577 | `anl4_fs_detail_estimates_advanced_af_nd_tbvps_mean` | MATRIX | 0.464 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of analyst estimates of tangible book value per share for the annual period |
| 578 | `anl4_fs_detail_estimates_advanced_af_nd_tbvps_median` | MATRIX | 0.464 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates of tangible book value per share for the annual period |
| 579 | `anl4_fs_detail_estimates_advanced_af_nd_tbvps_number` | MATRIX | 0.464 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates of tangible book value per share for the annual period |
| 580 | `anl4_basicdetailqf_prevval` | VECTOR | 0.463 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of financial item |
| 581 | `anl4_sadaf_dts_spfcf` | MATRIX | 0.461 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow per share- std of estimations |
| 582 | `anl4_fsactualqfv4_actual` | VECTOR | 0.460 | 其他 | 0 | — | — | — | UNUSABLE | Announced financial data |
| 583 | `anl4_sadaf_dts_rptp` | MATRIX | 0.458 | 其他 | 0 | — | — | — | UNUSABLE | Reported Pretax income- std of estimations |
| 584 | `anl4_adz_totassets_high` | MATRIX | 0.456 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - The highest estimation |
| 585 | `anl4_adz_totassets_low` | MATRIX | 0.456 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - The lowest estimation |
| 586 | `anl4_adz_totassets_mean` | MATRIX | 0.456 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - mean of estimations |
| 587 | `anl4_adz_totassets_median` | MATRIX | 0.456 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - median of estimations |
| 588 | `anl4_adz_totassets_number` | MATRIX | 0.456 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - number of estimations |
| 589 | `anl4_fs_detail_estimates_advanced_af_nd_fcfps_std` | MATRIX | 0.454 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for annual free cash flow per share |
| 590 | `anl4_adz_bvps_high` | MATRIX | 0.454 | 其他 | 0 | — | — | — | UNUSABLE | Book value - the highest estimation, per share |
| 591 | `anl4_adz_bvps_low` | MATRIX | 0.454 | 其他 | 0 | — | — | — | UNUSABLE | Book value - the lowest estimation, per share |
| 592 | `anl4_adz_bvps_mean` | MATRIX | 0.454 | 其他 | 0 | — | — | — | UNUSABLE | Book value per share - average of estimations |
| 593 | `anl4_adz_bvps_median` | MATRIX | 0.454 | 其他 | 0 | — | — | — | UNUSABLE | Book value per share - Median value among forecasts |
| 594 | `anl4_adz_bvps_number` | MATRIX | 0.454 | 其他 | 0 | — | — | — | UNUSABLE | Book value per share - number of estimations |
| 595 | `anl4_fs_detail_estimates_advanced_af_nd_ptpr_std` | MATRIX | 0.451 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analysts’ annual reported pretax income forecasts |
| 596 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totassets_high` | MATRIX | 0.449 | 修正与预期 | 0 | — | — | — | UNUSABLE | High estimate for Total Assets |
| 597 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totassets_low` | MATRIX | 0.449 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest estimate of Total Assets |
| 598 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totassets_mean` | MATRIX | 0.449 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate for Total Assets |
| 599 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totassets_median` | MATRIX | 0.449 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate for Total Assets |
| 600 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totassets_number` | MATRIX | 0.449 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Total Assets estimates |
| 601 | `anl4_sadaf_gric_std` | MATRIX | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | Gross income- std of estimations |
| 602 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_bvps_high` | MATRIX | 0.447 | 修正与预期 | 0 | — | — | — | UNUSABLE | Book Value per Share highest estimate |
| 603 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_bvps_low` | MATRIX | 0.447 | 修正与预期 | 0 | — | — | — | UNUSABLE | Book value per share - the lowest estimation |
| 604 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_bvps_mean` | MATRIX | 0.447 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of Book Value Per Share estimates |
| 605 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_bvps_median` | MATRIX | 0.447 | 修正与预期 | 0 | — | — | — | UNUSABLE | Book value per share - median value among forecasts |
| 606 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_bvps_number` | MATRIX | 0.447 | 修正与预期 | 0 | — | — | — | UNUSABLE | Book value per share - number of estimations |
| 607 | `anl4_ads1detailqf_bk` | VECTOR | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | Broker name (int) |
| 608 | `anl4_ads1detailqf_person` | VECTOR | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | Broker Id |
| 609 | `anl4_cuo1detailqf_item` | VECTOR | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 610 | `anl4_ads1detailqf_estvalue` | VECTOR | 0.446 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 611 | `anl4_ads1detailqf_prevval` | VECTOR | 0.442 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of financial item |
| 612 | `anl4_fs_detail_estimates_advanced_af_nd_grossincome_std` | MATRIX | 0.441 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst annual estimates for Gross Income |
| 613 | `anl4_sadaf_dts_ifc` | MATRIX | 0.438 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Investing - std of estimations |
| 614 | `anl4_adz_epsr_high` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | GAAP Earnings per share - The highest estimation |
| 615 | `anl4_adz_epsr_low` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | GAAP Earnings per share - The lowest estimation |
| 616 | `anl4_adz_epsr_mean` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | GAAP Earnings per share - mean of estimations |
| 617 | `anl4_adz_epsr_number` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | GAAP Earnings per share - number of estimations |
| 618 | `anl4_adz_median_epsreported` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | GAAP Earnings per share - median of estimations |
| 619 | `anl4_sadaf_dts_ffc` | MATRIX | 0.434 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Financing - std of estimations |
| 620 | `anl4_fs_detail_estimates_advanced_af_nd_cfi_std` | MATRIX | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for annual cash flow from investing |
| 621 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsr_high` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate of GAAP EPS |
| 622 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsr_low` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest estimate of GAAP EPS |
| 623 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsr_mean` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | GAAP earnings per share mean of estimates |
| 624 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsr_median` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate of GAAP EPS |
| 625 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_epsr_number` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | GAAP Earnings per share - number of estimations |
| 626 | `anl4_fs_detail_estimates_advanced_af_nd_cff_std` | MATRIX | 0.428 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for annual cash flow from financing |
| 627 | `anl4_sadaf_totgw_std` | MATRIX | 0.424 | 其他 | 0 | — | — | — | UNUSABLE | Total Goodwill - std of estimations |
| 628 | `anl4_bac1actualqf_actual` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Announced financial data |
| 629 | `anl4_fs_detail_estimates_advanced_af_nd_totgw_std` | MATRIX | 0.418 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for Total Goodwill for the annual forecast period |
| 630 | `anl4_ads1consaf_down` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Number of lower estimations |
| 631 | `anl4_ads1consaf_high` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | The highest estimation |
| 632 | `anl4_ads1consaf_low` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | The lowest estimation |
| 633 | `anl4_ads1consaf_mean` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Mean of estimations |
| 634 | `anl4_ads1consaf_median` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Median of estimations |
| 635 | `anl4_ads1consaf_numest` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | The number of forecasts counted in aggregation |
| 636 | `anl4_ads1consaf_pu` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | The number of upper estimations |
| 637 | `anl4_cuo1consaf_item` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 638 | `sales_estimate_stddev_quarterly` | MATRIX | 0.405 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of Sales estimations |
| 639 | `anl4_fs_detail_estimates_basic_qf_v4_nd_sales_std` | MATRIX | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of Sales estimations |
| 640 | `anl4_sadaf_rd_exp_high` | MATRIX | 0.376 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and Development Expense- The highest estimation |
| 641 | `anl4_sadaf_rd_exp_low` | MATRIX | 0.376 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and Development Expense- The lowest estimation |
| 642 | `anl4_sadaf_rd_exp_mean` | MATRIX | 0.376 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and Development Expense- mean of estimations |
| 643 | `anl4_sadaf_rd_exp_median` | MATRIX | 0.376 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and Development Expense- median of estimations |
| 644 | `anl4_sadaf_rd_exp_number` | MATRIX | 0.376 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and Development Expense- number of estimations |
| 645 | `anl4_adz_ptpr_high` | MATRIX | 0.373 | 其他 | 0 | — | — | — | UNUSABLE | Reported Pretax income- The highest estimation |
| 646 | `anl4_adz_ptpr_low` | MATRIX | 0.373 | 其他 | 0 | — | — | — | UNUSABLE | Reported Pretax income- The lowest estimation |
| 647 | `anl4_adz_ptpr_mean` | MATRIX | 0.373 | 其他 | 0 | — | — | — | UNUSABLE | Reported Pretax income- mean of estimations |
| 648 | `anl4_adz_ptpr_median` | MATRIX | 0.373 | 其他 | 0 | — | — | — | UNUSABLE | Reported Pretax income- median of estimations |
| 649 | `anl4_adz_ptpr_number` | MATRIX | 0.373 | 其他 | 0 | — | — | — | UNUSABLE | Reported Pretax income- number of estimations |
| 650 | `anl4_cuo1actualqf_actual` | VECTOR | 0.372 | 其他 | 0 | — | — | — | UNUSABLE | Announced financial data |
| 651 | `anl4_fs_detail_estimates_advanced_af_nd_rd_exp_high` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest individual analyst estimate for Research and Development expense for the annual forecast period |
| 652 | `anl4_fs_detail_estimates_advanced_af_nd_rd_exp_low` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest individual analyst estimate for Research and Development expense for the annual forecast period |
| 653 | `anl4_fs_detail_estimates_advanced_af_nd_rd_exp_mean` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of analyst estimates for Research and Development expense for the annual forecast period |
| 654 | `anl4_fs_detail_estimates_advanced_af_nd_rd_exp_median` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates for Research and Development expense for the annual forecast period |
| 655 | `anl4_fs_detail_estimates_advanced_af_nd_rd_exp_number` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing analyst estimates for Research and Development expense for the annual forecast period |
| 656 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptpr_high` | MATRIX | 0.367 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate of reported pretax income |
| 657 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptpr_low` | MATRIX | 0.367 | 修正与预期 | 0 | — | — | — | UNUSABLE | Reported pretax income - the lowest estimation |
| 658 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptpr_mean` | MATRIX | 0.367 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of reported pretax income estimates |
| 659 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptpr_median` | MATRIX | 0.367 | 修正与预期 | 0 | — | — | — | UNUSABLE | Reported Pretax income- median of estimations |
| 660 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptpr_number` | MATRIX | 0.367 | 修正与预期 | 0 | — | — | — | UNUSABLE | Reported pretax income - number of estimations |
| 661 | `anl4_cuo1actualsaf_item` | VECTOR | 0.363 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 662 | `anl4_adz_gric_high` | MATRIX | 0.358 | 其他 | 0 | — | — | — | UNUSABLE | Gross income- The highest estimation |
| 663 | `anl4_adz_gric_low` | MATRIX | 0.358 | 其他 | 0 | — | — | — | UNUSABLE | Gross income- The lowest estimation |
| 664 | `anl4_adz_gric_mean` | MATRIX | 0.358 | 其他 | 0 | — | — | — | UNUSABLE | Gross income- mean of estimations |
| 665 | `anl4_adz_gric_median` | MATRIX | 0.358 | 其他 | 0 | — | — | — | UNUSABLE | Gross income- median of estimations |
| 666 | `anl4_adz_gric_number` | MATRIX | 0.358 | 其他 | 0 | — | — | — | UNUSABLE | Gross income- number of estimations |
| 667 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_grossincome_high` | MATRIX | 0.353 | 修正与预期 | 0 | — | — | — | UNUSABLE | Gross income - highest estimate |
| 668 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_grossincome_low` | MATRIX | 0.353 | 修正与预期 | 0 | — | — | — | UNUSABLE | Gross income - the lowest estimation |
| 669 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_grossincome_mean` | MATRIX | 0.353 | 修正与预期 | 0 | — | — | — | UNUSABLE | Gross income - mean of estimations |
| 670 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_grossincome_median` | MATRIX | 0.353 | 修正与预期 | 0 | — | — | — | UNUSABLE | Gross income - median of estimations |
| 671 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_grossincome_number` | MATRIX | 0.353 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for Gross Income |
| 672 | `anl4_afv4_maxguidance` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Max guidance value |
| 673 | `anl4_afv4_minguidance` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Min guidance value |
| 674 | `anl4_guiafv4_est` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 675 | `previous_guidance_value_annual` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of finanicial item |
| 676 | `anl4_bac1consaf_item` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 677 | `anl4_basicconsaf_down` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Number of lower estimations |
| 678 | `anl4_basicconsaf_high` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | The highest estimation |
| 679 | `anl4_basicconsaf_low` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | The lowest estimation |
| 680 | `anl4_basicconsaf_mean` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Mean of estimations |
| 681 | `anl4_basicconsaf_median` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | Median of estimations |
| 682 | `anl4_basicconsaf_numest` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | The number of forecasts counted in aggregation |
| 683 | `anl4_basicconsaf_pu` | VECTOR | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | The number of upper estimations |
| 684 | `anl4_bac1actualsaf_item` | VECTOR | 0.350 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 685 | `anl4_adz_ebit_std` | MATRIX | 0.341 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest and taxes - std of estimations |
| 686 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebit_std` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of EBIT estimates |
| 687 | `anl4_qfv4_div_high` | MATRIX | 0.328 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend per share - The highest estimation |
| 688 | `anl4_qfv4_div_low` | MATRIX | 0.328 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend per share - The lowest estimation |
| 689 | `anl4_qfv4_div_mean` | MATRIX | 0.328 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend per share - mean of estimations |
| 690 | `anl4_qfv4_div_median` | MATRIX | 0.328 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend per share - median of estimations |
| 691 | `anl4_qfv4_div_number` | MATRIX | 0.328 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend - number of estimations |
| 692 | `anl4_fs_detail_estimates_basic_qf_v4_nd_div_high` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Dividend per share - highest estimation |
| 693 | `anl4_fs_detail_estimates_basic_qf_v4_nd_div_low` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Dividend per share - lowest estimation |
| 694 | `anl4_fs_detail_estimates_basic_qf_v4_nd_div_mean` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Dividend per share - average of estimations |
| 695 | `anl4_fs_detail_estimates_basic_qf_v4_nd_div_median` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Dividend per share - median of estimations |
| 696 | `anl4_fs_detail_estimates_basic_qf_v4_nd_div_number` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Dividend per share - number of estimations |
| 697 | `anl4_adz_netprofit_std` | MATRIX | 0.321 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net profit- std of estimations |
| 698 | `anl4_ads1detailsaf_bk` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Broker name (int) |
| 699 | `anl4_ads1detailsaf_person` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Broker Id |
| 700 | `anl4_cuo1detailsaf_item` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 701 | `anl4_ads1detailsaf_estvalue` | VECTOR | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 702 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_netprofit_std` | MATRIX | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of Net Profit estimates |
| 703 | `anl4_adz_totgw_high` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | Total Goodwill - The highest estimation |
| 704 | `anl4_adz_totgw_low` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | Total Goodwill - The lowest estimation |
| 705 | `anl4_adz_totgw_mean` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | Total Goodwill - mean of estimations |
| 706 | `anl4_adz_totgw_median` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | Total Goodwill - median of estimations |
| 707 | `anl4_adz_totgw_number` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | Total Goodwill - number of estimations |
| 708 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totgw_high` | MATRIX | 0.311 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total Goodwill highest estimate |
| 709 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totgw_low` | MATRIX | 0.311 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest estimate of Total Goodwill |
| 710 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totgw_mean` | MATRIX | 0.311 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total Goodwill - mean of estimations |
| 711 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totgw_median` | MATRIX | 0.311 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total Goodwill - median of estimations |
| 712 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_totgw_number` | MATRIX | 0.311 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total Goodwill - number of estimations |
| 713 | `anl4_adz_cfo_high` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - The highest value among forecasts |
| 714 | `anl4_adz_cfo_low` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - The lowest estimation |
| 715 | `anl4_adz_cfo_mean` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - mean of estimations |
| 716 | `anl4_adz_cfo_median` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - median of estimations |
| 717 | `anl4_adz_cfo_number` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - number of estimations |
| 718 | `anl4_dei3lqf_item` | VECTOR | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 719 | `anl4_eaz2lqf_bk` | VECTOR | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Broker name (int) |
| 720 | `anl4_eaz2lqf_person` | VECTOR | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Broker Id |
| 721 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_cfo_high` | MATRIX | 0.303 | 修正与预期 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - highest value among forecasts |
| 722 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_cfo_low` | MATRIX | 0.303 | 修正与预期 | 0 | — | — | — | UNUSABLE | Cash Flow From Operations - the lowest estimation |
| 723 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_cfo_mean` | MATRIX | 0.303 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of Cash Flow from Operations estimates |
| 724 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_cfo_median` | MATRIX | 0.303 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate of Cash Flow from Operations |
| 725 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_cfo_number` | MATRIX | 0.303 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Cash Flow from Operations estimates |
| 726 | `anl4_ads1detailsaf_prevval` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of financial item |
| 727 | `anl4_dei2lqf_item` | VECTOR | 0.292 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 728 | `anl4_eaz1lqf_bk` | VECTOR | 0.292 | 其他 | 0 | — | — | — | UNUSABLE | Broker name (int) |
| 729 | `anl4_eaz1lqf_person` | VECTOR | 0.292 | 其他 | 0 | — | — | — | UNUSABLE | Broker Id |
| 730 | `free_cash_flow_estimate_count` | MATRIX | 0.290 | 修正与预期 | 0 | — | — | — | UNUSABLE | Free cash flow- number of estimations |
| 731 | `free_cash_flow_estimate_median` | MATRIX | 0.290 | 修正与预期 | 0 | — | — | — | UNUSABLE | Free cash flow- aggregation on estimations, 50th-percentile |
| 732 | `quarterly_free_cash_flow_high` | MATRIX | 0.290 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow- aggregation on estimations, max |
| 733 | `quarterly_free_cash_flow_low` | MATRIX | 0.290 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow- The lowest estimation |
| 734 | `quarterly_free_cash_flow_mean` | MATRIX | 0.290 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow- mean of estimations |
| 735 | `capital_expenditure_estimate_average` | MATRIX | 0.288 | 修正与预期 | 0 | — | — | — | UNUSABLE | Capital Expenditures - mean of estimations |
| 736 | `capital_expenditure_estimate_count` | MATRIX | 0.288 | 修正与预期 | 0 | — | — | — | UNUSABLE | Capital Expenditures - number of estimations |
| 737 | `quarterly_capex_high_value` | MATRIX | 0.288 | 其他 | 0 | — | — | — | UNUSABLE | Capital Expenditures - The highest estimation |
| 738 | `quarterly_capex_low_value` | MATRIX | 0.288 | 其他 | 0 | — | — | — | UNUSABLE | Capital Expenditures - The lowest estimation |
| 739 | `quarterly_capex_median_value` | MATRIX | 0.288 | 其他 | 0 | — | — | — | UNUSABLE | Capital Expenditures - median of estimations |
| 740 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_fcf_high` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | High estimate of Free Cash Flow |
| 741 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_fcf_low` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest estimate of Free Cash Flow |
| 742 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_fcf_mean` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Free cash flow - mean of estimations |
| 743 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_fcf_median` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate of Free Cash Flow |
| 744 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_fcf_number` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for Free Cash Flow |
| 745 | `anl4_eaz2lqf_estvalue` | VECTOR | 0.286 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 746 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_capex_high` | MATRIX | 0.284 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate of Capital Expenditures |
| 747 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_capex_low` | MATRIX | 0.284 | 修正与预期 | 0 | — | — | — | UNUSABLE | Low estimate of Capital Expenditure |
| 748 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_capex_mean` | MATRIX | 0.284 | 修正与预期 | 0 | — | — | — | UNUSABLE | Capital Expenditures - mean of estimations |
| 749 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_capex_median` | MATRIX | 0.284 | 修正与预期 | 0 | — | — | — | UNUSABLE | Capital Expenditures - median of estimations |
| 750 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_capex_number` | MATRIX | 0.284 | 修正与预期 | 0 | — | — | — | UNUSABLE | Capital Expenditures - number of estimations |
| 751 | `anl4_eaz2lqf_prevval` | VECTOR | 0.277 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of financial item |
| 752 | `anl4_cuo1actualaf_item` | VECTOR | 0.276 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 753 | `anl4_eaz1lqf_estvalue` | VECTOR | 0.274 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 754 | `anl4_adz_dts_ptp` | MATRIX | 0.274 | 其他 | 0 | — | — | — | UNUSABLE | Pretax income- std of estimations |
| 755 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ptp_std` | MATRIX | 0.270 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of Pretax Income estimates |
| 756 | `anl4_eaz1lqf_prevval` | VECTOR | 0.266 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of financial item |
| 757 | `anl4_bac1detailsaf_item` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 758 | `anl4_basicdetailsaf_bk` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Broker name (int) |
| 759 | `anl4_basicdetailsaf_person` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Broker Id |
| 760 | `anl4_basicdetailsaf_estvalue` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Estimation value |
| 761 | `anl4_bac1actualaf_item` | VECTOR | 0.263 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 762 | `anl4_fsguidanceafv4_item` | VECTOR | 0.261 | 其他 | 0 | — | — | — | UNUSABLE | Financial item |
| 763 | `anl4_fsguidanceafv4_maxguidance` | VECTOR | 0.261 | 其他 | 0 | — | — | — | UNUSABLE | Maximum guidance value |
| 764 | `anl4_fsguidanceafv4_minguidance` | VECTOR | 0.261 | 其他 | 0 | — | — | — | UNUSABLE | Min guidance value |
| 765 | `quarterly_ebitda_standard_deviation` | MATRIX | 0.257 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation and amortization - std of estimations |
| 766 | `anl4_fs_detail_estimate_advanced_1qf_v4_nd_ebitda_std` | MATRIX | 0.254 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of EBITDA estimates |
| 767 | `anl4_cuo1actualaf_actual` | VECTOR | 0.251 | 其他 | 0 | — | — | — | UNUSABLE | Announced financial data |
| 768 | `anl4_af_eps_value` | MATRIX | 0.251 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Per Share - Actual Value |
| 769 | `anl4_basicdetailsaf_prevval` | VECTOR | 0.251 | 其他 | 0 | — | — | — | UNUSABLE | The previous estimation of financial item |
| 770 | `actual_sales_value_annual` | MATRIX | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Sales - Actual Value |
| 771 | `anl4_fs_actuals_basic_af_nd_sales_value` | MATRIX | 0.174 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sales/Revenue actual value for the annual period |
| 772 | `anl4_af_div_value` | MATRIX | 0.173 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend - Actual value |
| 773 | `anl4_fs_actuals_basic_af_nd_eps_value` | MATRIX | 0.172 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Per Share actual value for the annual period |
| 774 | `anl4_fs_actuals_basic_af_nd_div_value` | MATRIX | 0.171 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend actual value for the annual period |
| 775 | `anl4_qfv4_dts_spe` | MATRIX | 0.161 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - standard deviation of estimations |
| 776 | `anl4_fs_detail_estimates_basic_qf_v4_nd_eps_std` | MATRIX | 0.161 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings per share - standard deviation of estimations |

## 六、本地回测证据

- 本地累计回测 **96** 条；其中 `ra_failed_checks` 为空的 **96** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `pwv7veWX` | 1.72 | 1.18 | -0.01 | 0.64 | 0.11 | 0 | w634i | `multiply(signed_power(group_rank(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wks_a` |
| `GrgoOe1x` | 1.70 | 1.15 | -0.05 | 0.64 | 0.10 | 0 | w628 | `signed_power(group_rank(ts_backfill(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wk` |
| `1YjgZze6` | 1.70 | 1.16 | -0.04 | 0.64 | 0.10 | 0 | w628 | `signed_power(group_rank(ts_backfill(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wk` |
| `1YjgZzk6` | 1.60 | 0.78 | 0.42 | 1.02 | 0.24 | 0 | w628 | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `qMEX0692` | 1.60 | 0.78 | 0.40 | 1.03 | 0.24 | 0 | w628 | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `78odnGvx` | 1.59 | 0.77 | 0.53 | 1.01 | 0.24 | 0 | w618 | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `ZYmonN28` | 1.56 | 0.75 | 0.47 | 1.00 | 0.24 | 0 | w616 | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `MP0x3LMa` | 1.52 | 1.05 | 0.12 | 0.65 | 0.06 | 0 | w628 | `signed_power(group_rank(ts_backfill(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_3mt` |
| `vROm2v8w` | 1.52 | 1.05 | 0.09 | 0.65 | 0.06 | 0 | w628 | `signed_power(group_rank(ts_backfill(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_3mt` |
| `E5VKem8G` | 1.51 | 0.72 | 0.40 | 0.99 | 0.23 | 0 | w618 | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `E5VKem8L` | 1.50 | 0.69 | 0.37 | 0.97 | 0.24 | 0 | w618 | `signed_power(group_rank(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estimate), vec_avg` |
| `zqrWRA61` | 1.49 | 0.83 | 0.56 | 0.89 | 0.20 | 0 | w619 | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `2rjKmKM8` | 1.49 | 0.69 | 0.76 | 1.06 | 0.22 | 0 | w627c | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `6XAEpvzK` | 1.47 | 0.93 | 0.63 | 0.91 | 0.14 | 0 | w620b | `signed_power(group_rank(ts_backfill(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_nd_estima` |
| `omoYN5Mn` | 1.44 | 0.91 | 0.48 | 0.87 | 0.13 | 0 | w620a | `ts_target_tvr_decay(signed_power(group_rank(divide(subtract(vec_avg(anl4_fs_detail_lt_v4_n` |

## 七、判死记录（sealed dead_end）

- `EUR-ANL11-ESG-SLOWVAR-LONGCOUNT`（None）family=analyst11 ESG 评分体系（三支柱 + 行业排名 + 改善动量）：{"critical_lesson": "★ coverage 元数据虚报（缺陷#3 第4次坐实）：catalog 报 cov=0.9123/0.9087，实际回测 longCount 仅 51-52（占 TOP2500 的 2%）。选数据集时不能信 catalog coverage，必须用 1-2 条探针实测 longCount。", "dataset": "analyst11", "evidence": {"1YxzzPmQ": "ESG 绝对水平 rank(overall_sustainability_score_2)：S-0.68/F-0.13/TVR0.0985/longCount 52/CW FAIL", "A1077x7l": "行业内排名 rank(reverse(anl11_esgreg_industryrnk))：S-0.25/F-0.03/longCount 51/C
- `EUR-ANL45-TRADE-IDEAS-WEAK`（2026-08-25）family=analyst45 VECTOR trade-idea residual x v_rev/wedge：{"best": {"alpha": "78jwwme2", "fitness": 0.31, "sharpe": 0.71}, "reason": "Wave61 seven analyst45 trade-idea slows (probability/jensen/exposure/age/count/rel-return/PnL) x v_rev/wedge. Max S0.71. Differentiated but far from cheap gate. Do not Mode A. Do not reuse leftover anl45 price/FX/time fields.", "rule": "Do not reuse analyst45 trade-idea vec_avg residuals as 0.30 slow legs with v_rev/fallin
- `EUR-analyst45-RET-WEAK`（2026-09-04）family=analyst45 return/benchmark fields：{"best_2y": 0.43, "best_alpha": "RRVn5GV1", "best_fitness": 0.16, "best_sharpe": 0.38, "dataset": "analyst45", "evidence": "wave117 9 条全灭：收益类字段（ad_rel_ret/jensensalpha/tot_ret）全负，ad_ret_per S0.38 弱；conversion_rate_summary 无数据；benchmark_currency_code 弱信号；if_else/trade_when 条件逻辑无效", "id": "EUR-analyst45-RET-WEAK", "reason": "analyst45 收益/基准类字段在 EUR TOP2500 无正向预测力；收益类字段全负或弱，条件逻辑无效", "region": "EUR", 
- `EUR-NONMODEL-TOWER-CEILING`（2026-09-11）family=non_model_tower_sparse_event_sentiment_analyst：{"datasets": [{"dataset": "news54", "max_sharpe": 0.4, "reason": "mws54_factor semi-annual+单边恒正+稀疏", "tower": "news"}, {"dataset": "news_sentiment_nlp", "max_sharpe": 0.39, "reason": "情绪信号弱,净极性turnover1.24高超手", "tower": "other"}, {"dataset": "analyst45", "max_sharpe": 0.32, "reason": "分析师想法表现弱,zscore/delta turnover1.5+", "tower": "analyst"}], "evidence": "三塔回测全灭,S0 calibrate预警与实测完全一致(news0.50→0.40
- `EUR-CREDIT-DEFAULT-ANALYST81-MODEL52`（2026-10-19）family=credit_default：{"batch": "2tRfk57w04Tob49Lqt0jIG2", "best_abs_sharpe": 0.42, "coverage": {"analyst81": 0.2402, "model52": 0.1986}, "date": "2026-10-19", "decision_table": "D15（8 探针无 S >= 0.5 即判死）", "family": "credit_default", "field_trap": "anl81_class / cr_class 用打乱序数的编码（9=AAA,5=AA,4=A,1=BBB,2=BB,3=B,7=CCC,8=CC,6=C,10=D），任何单调算子（rank/zscore/ts_rank）在其上无意义，只能当分组或条件变量。", "id": "EUR-CREDIT-DEFAULT-ANALYST81-MODEL52

