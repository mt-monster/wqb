# analyst14 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst14` |
| 名称 | Estimations of Key Fundamentals |
| 类别 | ANALYST |
| 数据字段数(平台) | 121 |
| 覆盖率 | 0.5 |
| 平台已有 alpha | 270 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily, regionally split files containing detailed and consensus analyst estimates for key financial metrics such as revenue, EBITDA, EPS, dividends, and price targets for publicly traded companies worldwide. It includes individual analyst and broker forecasts, consensus calculations (mean, median, high, low, standard deviation), and actuals, along with metadata on fiscal periods, reporting currencies, and company identifiers. The dataset is highly granular, supporting point-in-time analysis and backtesting, and is essential for identifying earnings surprises, revisions, and trends in analyst sentiment. By tracking changes in consensus and individual estimates, users can anticipate price movements driven by earnings releases, analyst upgrades/downgrades, and shifts in 

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **121** |
| 类型分布 | MATRIX×121 |
| 平均覆盖率 | **0.500** |
| 覆盖率区间 | 0.50 ~ 0.50 |
| 更新频率（推断） | 低频（季/年） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 121 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 121 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 121 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 105 | 0.50 | anl14_actvalue_ebit_fp0、anl14_actvalue_ebitda_fp0、anl14_actvalue_eps_fp0 |
| 价量与波动 | 6 | 0.50 | rtk_ptg_high、rtk_ptg_low、rtk_ptg_mean |
| 修正与预期 | 5 | 0.50 | anl14_buy、anl14_hold、anl14_outperform |
| 其他 | 5 | 0.50 | anl14_curperiodnum、anl14_curperiodtype、anl14_cursharesoutstanding |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl14_actvalue_ebit_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Before Interest & Taxes - recent last quarter |
| 2 | `anl14_actvalue_ebitda_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Before Interest, Taxes, Depreciation & Amortization - recent last quarter |
| 3 | `anl14_actvalue_eps_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share - recent last quarter |
| 4 | `anl14_actvalue_epsrep_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported Earnings Per Share - recent last quarter |
| 5 | `anl14_actvalue_ntp_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Profit - recent last quarter |
| 6 | `anl14_actvalue_ntprep_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported Net Profit - recent last quarter |
| 7 | `anl14_actvalue_ptp_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax profit - recent last quarter |
| 8 | `anl14_actvalue_ptprep_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported pretax profit - recent last quarter |
| 9 | `anl14_actvalue_revenue_fp0` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue - recent last quarter |
| 10 | `anl14_buy` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of recommendations to buy - |
| 11 | `anl14_curperiodnum` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of period - |
| 12 | `anl14_curperiodtype` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Type of Period - |
| 13 | `anl14_cursharesoutstanding` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Current Share Outstanding - |
| 14 | `anl14_high_ebit_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of earnings before interest & taxes - upcoming quarter |
| 15 | `anl14_high_ebit_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Highest Estimation of Earnings Before Interest & Taxes - upcoming 2 quarters |
| 16 | `anl14_high_ebitda_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of earnings before interest, taxes, depreciation & amortization - upcoming quarter |
| 17 | `anl14_high_eps_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of Earnings Per Share - upcoming quarter |
| 18 | `anl14_high_eps_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of Earnings Per Share - upcoming 2 quarters |
| 19 | `anl14_high_epsrep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of reported earnings per share - upcoming quarter |
| 20 | `anl14_high_epsrep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Highest Estimation of Reported Earnings Per Share - upcoming 2 quarters |
| 21 | `anl14_high_ntp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Highest Estimation of Net Profit - Upcoming Quarter |
| 22 | `anl14_high_ntp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of Net Profit - upcoming 2 quarters |
| 23 | `anl14_high_ntprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Highest Estimation of Reported Net Profit - upcoming quarter |
| 24 | `anl14_high_ntprep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Highest Estimation of Reported Net Profit - Upcoming 2 Quarters |
| 25 | `anl14_high_ptp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Highest Estimation of Pretax Profit - upcoming quarter |
| 26 | `anl14_high_ptp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of pretax profit - upcoming 2 quarters |
| 27 | `anl14_high_ptprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of reported pretax profit - upcoming quarter |
| 28 | `anl14_high_revenue_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of Revenue - upcoming quarter |
| 29 | `anl14_high_revenue_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The highest estimation of revenue - upcoming 2 quarters |
| 30 | `anl14_hold` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Num of recommendations to hold - |
| 31 | `anl14_low_ebit_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of earnings before interest & taxes - upcoming quarter |
| 32 | `anl14_low_ebit_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest estimation of Earnings Before Interest & Taxes - upcoming 2 quarters |
| 33 | `anl14_low_ebitda_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of Earnings Before Interest, Taxes, Depreciation & Amortization - upcoming quarter |
| 34 | `anl14_low_eps_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of earnings per share - upcoming quarter |
| 35 | `anl14_low_eps_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest Estimation of Earnings Per Share - Upcoming 2 Quarters |
| 36 | `anl14_low_epsrep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest Estimation of Reported Earnings Per Share - Upcoming Quarter |
| 37 | `anl14_low_epsrep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest Estimation of Reported Earnings Per Share - upcoming 2 quarters |
| 38 | `anl14_low_ntp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of net profit - upcoming quarter |
| 39 | `anl14_low_ntp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of net profit - upcoming 2 quarters |
| 40 | `anl14_low_ntprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of reported net profit - upcoming quarter |
| 41 | `anl14_low_ntprep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest Estimation of Reported Net Profit - upcoming 2 quarters |
| 42 | `anl14_low_ptp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest Estimation of Pretax Profit - upcoming quarter |
| 43 | `anl14_low_ptp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of pretax profit - upcoming 2 quarters |
| 44 | `anl14_low_ptprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The Lowest Estimation of Reported Pretax Profit - Upcoming Quarter |
| 45 | `anl14_low_revenue_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of revenue - upcoming quarter |
| 46 | `anl14_low_revenue_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The lowest estimation of Revenue - upcoming 2 quarters |
| 47 | `anl14_mean_ebit_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of Earnings Before Interest & Taxes - upcoming quarter |
| 48 | `anl14_mean_ebit_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of earnings before interest & taxes - upcoming 2 quarters |
| 49 | `anl14_mean_ebitda_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Earnings Before Interest, Taxes, Depreciation & Amortization - upcoming quarter |
| 50 | `anl14_mean_eps_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of earnings per share - upcoming quarter |
| 51 | `anl14_mean_eps_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Earnings Per Share - upcoming 2 quarters |
| 52 | `anl14_mean_epsrep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Reported Earnings Per Share - upcoming quarter |
| 53 | `anl14_mean_epsrep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of reported earnings per share - upcoming 2 quarters |
| 54 | `anl14_mean_ntp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Net Profit - upcoming quarter |
| 55 | `anl14_mean_ntp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of net profit - upcoming 2 quarters |
| 56 | `anl14_mean_ntprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of reported net profit - upcoming quarter |
| 57 | `anl14_mean_ntprep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Reported Net Profit - upcoming 2 quarters |
| 58 | `anl14_mean_ptp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of pretax profit - upcoming quarter |
| 59 | `anl14_mean_ptp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of pretax profit - upcoming 2 quarters |
| 60 | `anl14_mean_ptprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of estimations of reported pretax profit - upcoming quarter |
| 61 | `anl14_mean_revenue_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Revenue - Upcoming Quarter |
| 62 | `anl14_mean_revenue_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of Estimations of Revenue - upcoming 2 quarters |
| 63 | `anl14_meanrating` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Mean of rating - |
| 64 | `anl14_median_ebit_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Earnings Before Interest & Taxes - Upcoming Quarter |
| 65 | `anl14_median_ebit_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Earnings Before Interest & Taxes - Upcoming 2 Quarters |
| 66 | `anl14_median_ebitda_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Earnings Before Interest, Taxes, Depreciation & Amortization - upcoming quarter |
| 67 | `anl14_median_eps_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Earnings Per Share - upcoming quarter |
| 68 | `anl14_median_eps_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of estimations of earnings per share - upcoming 2 quarters |
| 69 | `anl14_median_epsrep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Reported Earnings Per Share - upcoming quarter |
| 70 | `anl14_median_epsrep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of estimations of reported earnings per share - upcoming 2 quarters |
| 71 | `anl14_median_ntp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of estimations of net profit - upcoming quarter |
| 72 | `anl14_median_ntp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of estimations of net profit - upcoming 2 quarters |
| 73 | `anl14_median_ntprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Reported Net Profit - upcoming quarter |
| 74 | `anl14_median_ntprep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Reported Net Profit - upcoming 2 quarters |
| 75 | `anl14_median_ptp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of estimations of pretax profit - upcoming quarter |
| 76 | `anl14_median_ptp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Pretax Profit - upcoming 2 quarters |
| 77 | `anl14_median_ptprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Reported Pretax Profit - upcoming quarter |
| 78 | `anl14_median_revenue_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of estimations of revenue - upcoming quarter |
| 79 | `anl14_median_revenue_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of Estimations of Revenue - upcoming 2 quarters |
| 80 | `anl14_numofests_ebit_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Earnings Before Interest & Taxes - upcoming quarter |
| 81 | `anl14_numofests_ebit_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Earnings Before Interest & Taxes - upcoming 2 quarters |
| 82 | `anl14_numofests_ebitda_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Earnings Before Interest, Taxes, Depreciation & Amortization - upcoming quarter |
| 83 | `anl14_numofests_eps_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Earnings Per Share - upcoming quarter |
| 84 | `anl14_numofests_eps_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of estimations of earnings per share - upcoming 2 quarters |
| 85 | `anl14_numofests_epsrep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of estimations of reported earnings per share - upcoming quarter |
| 86 | `anl14_numofests_epsrep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Reported Earnings Per Share - upcoming 2 quarters |
| 87 | `anl14_numofests_ntp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Net Profit - upcoming quarter |
| 88 | `anl14_numofests_ntp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Net Profit - upcoming 2 quarters |
| 89 | `anl14_numofests_ntprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Reported Net Profit - Upcoming Quarter |
| 90 | `anl14_numofests_ntprep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Reported Net Profit - upcoming 2 quarters |
| 91 | `anl14_numofests_ptp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of estimations of Pretax Profit - upcoming quarter |
| 92 | `anl14_numofests_ptp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Pretax Profit - Upcoming 2 Quarters |
| 93 | `anl14_numofests_ptprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of estimations of Reported Pretax Profit - upcoming quarter |
| 94 | `anl14_numofests_revenue_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of Estimations of Revenue - upcoming quarter |
| 95 | `anl14_numofests_revenue_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Num of estimations of revenue - upcoming 2 quarters |
| 96 | `anl14_outperform` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Num of recommendations on being outperform of this stock |
| 97 | `anl14_sell` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of recommendations to sell |
| 98 | `anl14_stddev_ebit_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Earnings Before Interest & Taxes - upcoming quarter |
| 99 | `anl14_stddev_ebit_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of Earnings Before Interest & Taxes - upcoming 2 quarters |
| 100 | `anl14_stddev_ebitda_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Earnings Before Interest, Taxes, Depreciation & Amortization - upcoming quarter |
| 101 | `anl14_stddev_eps_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of earnings per share - upcoming quarter |
| 102 | `anl14_stddev_eps_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Earnings Per Share - Upcoming 2 Quarters |
| 103 | `anl14_stddev_epsrep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of reported earnings per share - upcoming quarter |
| 104 | `anl14_stddev_epsrep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Reported Earnings Per Share - Upcoming 2 Quarters |
| 105 | `anl14_stddev_ntp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Net Profit - Upcoming Quarter |
| 106 | `anl14_stddev_ntp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of net profit - upcoming 2 quarters |
| 107 | `anl14_stddev_ntprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Reported Net Profit - upcoming quarter |
| 108 | `anl14_stddev_ntprep_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Reported Net Profit - upcoming 2 quarters |
| 109 | `anl14_stddev_ptp_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of pretax profit - upcoming quarter |
| 110 | `anl14_stddev_ptp_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of pretax profit - upcoming 2 quarters |
| 111 | `anl14_stddev_ptprep_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Reported Pretax Profit - upcoming quarter |
| 112 | `anl14_stddev_revenue_fp1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard Deviation of Estimations of Revenue - Upcoming Quarter |
| 113 | `anl14_stddev_revenue_fp2` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of estimations of revenue - upcoming 2 quarters |
| 114 | `anl14_underperform` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Num of recommendations of being underperform for this stock |
| 115 | `anl14_xrefmap` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Reference Map to Stock - |
| 116 | `rtk_ptg_high` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The highest of Price Target - |
| 117 | `rtk_ptg_low` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The Lowest of Price Target |
| 118 | `rtk_ptg_mean` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Mean of Price Target - |
| 119 | `rtk_ptg_median` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Median of price target |
| 120 | `rtk_ptg_number` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Num of Price Target - |
| 121 | `rtk_ptg_stddev` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Standard Deviation of Price Target |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-ANALYST14-F-GATE-CEILING`（2026-10-19）family=analyst14：{"dataset": "analyst14", "dead_at": "2026-10-19", "evidence_batch": "multisim 4yoX6GgIi4rab6uYMfspQkX (Batch K), 10/10 complete, 0 errors, harvested 2026-10-19", "evidence_fields": "get_datafields(EUR, analyst14, TOP2500, delay 1, filter_sharpe=False) => 121 fields, all MATRIX, coverage uniformly stamped 0.5 (dataset-level stamp, not per-field measurement)", "family": "analyst14", "id": "EUR-ANALY

