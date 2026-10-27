# model25 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model25` |
| 名称 | Earnings Quality |
| 类别 | MODEL |
| 数据字段数(平台) | 417 |
| 覆盖率 | 0.5954 |
| 平台已有 alpha | 1318 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive stock ranking model that integrates both valuation and momentum factors. It combines intrinsic and relative valuation metrics with analyst estimate revisions and price momentum signals, offering percentile ranks at global, regional, sector, and industry levels. The model leverages historical performance data, including decile spread returns, to identify stocks with attractive value and strong momentum characteristics. By blending these factors, the dataset helps investors and quantitative researchers predict future price movements and construct portfolios that are more likely to outperform market benchmarks. Its multi-factor approach is particularly useful for screening, backtesting, and systematic investment strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **417** |
| 类型分布 | MATRIX×417 |
| 平均覆盖率 | **0.595** |
| 覆盖率区间 | 0.26 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 87 | 20.9% |
| 中 (0.70–0.90) | 15 | 3.6% |
| 低 (0.50–0.70) | 218 | 52.3% |
| 稀疏 (<0.50) | 97 | 23.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 299 | 71.7% |
| UNTESTED | 118 | 28.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 118 / UNUSABLE 299 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 183 | 0.57 | mdl25_01v、mdl25_8v、mdl25_22v |
| 其他 | 162 | 0.58 | mdl25_cbv421_7v、mdl25_pcv421_02v、mdl25_pcv421_03v |
| 价量与波动 | 54 | 0.73 | mdl25_cbv421_01v、mdl25_cbv421_11v、mdl25_cbv421_21v |
| 宏观与行业 | 15 | 0.60 | mdl25_cbv421_6v、mdl25_pcv421_01v、mdl25_pcv421_11v |
| 持仓与资金流 | 2 | 0.75 | mdl25_cbv421_02v、mdl25_eq_cb_v4_2_1_v20 |
| 风险与质量 | 1 | 0.89 | operating_efficiency_component_raw_score |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl25_cbv421_01v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average Traded Volume |
| 2 | `mdl25_cbv421_02v` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Data-Through Date (Fundamental) Current |
| 3 | `mdl25_cbv421_11v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average Traded Volume (Local Currency) |
| 4 | `mdl25_cbv421_21v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average Traded Volume (USD) |
| 5 | `mdl25_cbv421_6v` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Market Cap (Local Currency) |
| 6 | `mdl25_cbv421_7v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Market Cap (USD) |
| 7 | `mdl25_cbv421_8v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-week High Price |
| 8 | `mdl25_cbv421_9v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-week Low Price |
| 9 | `mdl25_pcv421_01v` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change Relative to Industry Benchmark (%) |
| 10 | `mdl25_pcv421_02v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to JSE All Share (%) |
| 11 | `mdl25_pcv421_03v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to Russell Midcap (%) |
| 12 | `mdl25_pcv421_11v` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change Relative to Country Benchmark (%) |
| 13 | `mdl25_pcv421_12v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to MSCI EAFE (%) |
| 14 | `mdl25_pcv421_13v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to S&P 400 (%) |
| 15 | `mdl25_pcv421_21v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to ASX 100 (%) |
| 16 | `mdl25_pcv421_22v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to MSCI EMF (%) |
| 17 | `mdl25_pcv421_23v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to S&P 500 (%) |
| 18 | `mdl25_pcv421_31v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to ASX 200 (%) |
| 19 | `mdl25_pcv421_32v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to MSCI Europe (%) |
| 20 | `mdl25_pcv421_33v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to S&P 600 (%) |
| 21 | `mdl25_pcv421_41v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to ASX 300 (%) |
| 22 | `mdl25_pcv421_42v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to MSCI Pac ex JP (%) |
| 23 | `mdl25_pcv421_43v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to TOPIX (%) |
| 24 | `mdl25_pcv421_51v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to ASX All Ord (%) |
| 25 | `mdl25_pcv421_52v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to MSCI World (%) |
| 26 | `mdl25_pcv421_53v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to TSX Composite (%) |
| 27 | `mdl25_pcv421_5v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price Change (%) |
| 28 | `mdl25_pcv421_61v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to CAC 40 (%) |
| 29 | `mdl25_pcv421_62v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to R1000 Growth (%) |
| 30 | `mdl25_pcv421_6v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change from 52-week High Price (ratio) |
| 31 | `mdl25_pcv421_71v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to DJ STOXX 600 (%) |
| 32 | `mdl25_pcv421_72v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to R1000 Value (%) |
| 33 | `mdl25_pcv421_7v` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change from 52-week Low Price (ratio) |
| 34 | `mdl25_pcv421_81v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to FTSE 100 (%) |
| 35 | `mdl25_pcv421_82v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to Russell 1000 (%) |
| 36 | `mdl25_pcv421_8v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Diff from 50-day Moving Average (%) |
| 37 | `mdl25_pcv421_91v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to Hang Seng (%) |
| 38 | `mdl25_pcv421_92v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change Relative to Russell 2000 (%) |
| 39 | `mdl25_pcv421_9v` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Diff from 200-day Moving Average (%) |
| 40 | `mdl25_01v` | MATRIX | 0.981 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Accruals - Period End Date |
| 41 | `mdl25_8v` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Accruals |
| 42 | `mdl25_22v` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Raw Earnings Quality |
| 43 | `mdl25_6v` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality Region Rank |
| 44 | `mdl25_history_11v` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality Region Rank Current |
| 45 | `mdl25_history_01v` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality Raw Current |
| 46 | `mdl25_history_9v` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality Region |
| 47 | `mdl25_vrv421_31v` | MATRIX | 0.979 | 其他 | 0 | — | — | — | UNTESTED | Enterprise Value (EV) |
| 48 | `mdl25_rov421_71v` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adj. Net Op. Asset Turnover - Last Year |
| 49 | `mdl25_81v` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Operating Efficiency - Period End Date |
| 50 | `mdl25_61v` | MATRIX | 0.975 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Operating Efficiency |
| 51 | `mdl25_history_31v` | MATRIX | 0.975 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Component Current |
| 52 | `mdl25_vrv421_8v` | MATRIX | 0.974 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Sales |
| 53 | `mdl25_rov421_81v` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adj. Net Op. Asset Turnover - 1 FY Difference |
| 54 | `mdl25_vrv421_61v` | MATRIX | 0.972 | 其他 | 0 | — | — | — | UNTESTED | EV/Sales |
| 55 | `mdl25_vrv421_5v` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Book |
| 56 | `mdl25_rov421_12v` | MATRIX | 0.970 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Adj. Net Op. Assets (%) - Last Year |
| 57 | `mdl25_rpv421_31v` | MATRIX | 0.966 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average Historical Operating Margin 5-Year |
| 58 | `mdl25_rov421_22v` | MATRIX | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Adj. Net Op. Assets (%) - 1 FY Difference |
| 59 | `mdl25_vrv421_71v` | MATRIX | 0.961 | 宏观与行业 | 0 | — | — | — | UNTESTED | FCF Yield (%) |
| 60 | `mdl25_rpv421_41v` | MATRIX | 0.960 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diff from Average Hist Operating Margin 5-Year |
| 61 | `mdl25_41v` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Cash Flow - Period End Date |
| 62 | `short_term_momentum_percentile` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile score for short-term price momentum. |
| 63 | `industry_momentum_percentile_2` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile score for price momentum relative to industry peers. |
| 64 | `mdl25_isv421_7v` | MATRIX | 0.950 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average Historical Revenue Growth 5-Year |
| 65 | `mid_term_momentum_percentile` | MATRIX | 0.948 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile score for mid-term price momentum. |
| 66 | `mdl25_isv421_8v` | MATRIX | 0.948 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diff from Average Hist Revenue Growth 5-Year |
| 67 | `value_momentum_global_percentile` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Global percentile ranking for value-momentum score. |
| 68 | `value_momentum_global_rank_float` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Global value-momentum percentile score as a floating-point value. |
| 69 | `value_momentum_region_percentile` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Region-relative percentile ranking for value-momentum score. |
| 70 | `value_momentum_region_rank_float` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Region-relative value-momentum percentile score as a floating-point value. |
| 71 | `value_momentum_sector_percentile` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Sector-relative percentile ranking for value-momentum score. |
| 72 | `value_momentum_sector_rank_float` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Sector-relative value-momentum percentile score as a floating-point value. |
| 73 | `mdl25_vrv421_91v` | MATRIX | 0.943 | 其他 | 0 | — | — | — | UNTESTED | CFO/EV (%) |
| 74 | `mdl25_vrv421_81v` | MATRIX | 0.939 | 其他 | 0 | — | — | — | UNTESTED | FCF/EV (%) |
| 75 | `mdl25_vrv421_41v` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | EV/EBITDA |
| 76 | `value_momentum_industry_percentile` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative percentile ranking for value-momentum score. |
| 77 | `value_momentum_industry_rank_float` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative value-momentum percentile score as a floating-point value. |
| 78 | `mdl25_history_21v` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accruals Component Current |
| 79 | `mdl25_21v` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Cash Flow |
| 80 | `long_term_momentum_percentile` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile score for long-term price momentum. |
| 81 | `global_momentum_percentile` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | Global percentile ranking for price momentum score. |
| 82 | `regional_momentum_percentile` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile score for price momentum relative to region. |
| 83 | `mdl25_vrv421_01v` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Sales - 1 FY Difference (%) |
| 84 | `mdl25_vrv421_9v` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Sales - 1 FY Difference |
| 85 | `mdl25_7v` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality Region Rank - 1 Day Difference |
| 86 | `mdl25_isv421_11v` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average Historical EBITDA Growth 5-Year |
| 87 | `mdl25_isv421_21v` | MATRIX | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diff from Average Hist EBITDA Growth 5-Year |
| 88 | `mdl25_71v` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Operating Efficiency - 1 Day Difference |
| 89 | `mdl25_vrv421_11v` | MATRIX | 0.895 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/CFO |
| 90 | `operating_efficiency_component_percentile` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile score for operating efficiency factors in the earnings quality model. |
| 91 | `operating_efficiency_component_raw_score` | MATRIX | 0.891 | 风险与质量 | 0 | — | — | — | UNTESTED | Raw percentile score for operating efficiency component before normalization. |
| 92 | `exclusions_component_percentile` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile score for exclusions-based factors in the earnings quality model. |
| 93 | `accruals_component_raw_score` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | Raw percentile score for accruals component before normalization. |
| 94 | `earnings_quality_raw_score` | MATRIX | 0.869 | 盈利与财务 | 0 | — | — | — | UNTESTED | Raw region-relative percentile ranking before normalization for earnings quality. |
| 95 | `mdl25_rpv421_7v` | MATRIX | 0.857 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average Historical Gross Margin - 5-Year |
| 96 | `mdl25_rpv421_8v` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diff from Average Hist Gross Margin - 5-Year |
| 97 | `mdl25_9v` | MATRIX | 0.842 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Accruals - 1 Day Difference |
| 98 | `mdl25_isv421_92v` | MATRIX | 0.827 | 其他 | 0 | — | — | — | UNTESTED | Average Historical EPS Growth 5-Year |
| 99 | `mdl25_isv421_03v` | MATRIX | 0.826 | 其他 | 0 | — | — | — | UNTESTED | Diff from Average Hist EPS Growth 5-Year |
| 100 | `mdl25_vrv421_21v` | MATRIX | 0.815 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/FCF |
| 101 | `mdl25_31v` | MATRIX | 0.721 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality by Cash Flow - 1 Day Difference |
| 102 | `mdl25_15v` | MATRIX | 0.707 | 其他 | 0 | — | — | — | UNTESTED | Pension Expense - Last Year |
| 103 | `mdl25_cbv421_12v` | MATRIX | 0.688 | 其他 | 0 | — | — | — | UNTESTED | Period End Date - Last Qtr |
| 104 | `mdl25_cbv421_32v` | MATRIX | 0.688 | 其他 | 0 | — | — | — | UNTESTED | New Filing Received Date - Last Qtr |
| 105 | `mdl25_cbv421_03v` | MATRIX | 0.685 | 其他 | 0 | — | — | — | UNTESTED | Consolidated Financials Flag - Last Qtr |
| 106 | `mdl25_bsv421_8v` | MATRIX | 0.677 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted Average Net Operating Assets - Last Qtr |
| 107 | `mdl25_bsv421_7v` | MATRIX | 0.654 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average Net Operating Assets - Last Qtr |
| 108 | `mdl25_cbv421_22v` | MATRIX | 0.651 | 其他 | 0 | — | — | — | UNTESTED | Company Filing Date - Last Qtr |
| 109 | `mdl25_bsv421_01v` | MATRIX | 0.631 | 其他 | 0 | — | — | — | UNTESTED | Book Value - Last Qtr |
| 110 | `mdl25_bsv421_5v` | MATRIX | 0.628 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Assets - Last Qtr |
| 111 | `mdl25_rlevv421_7v` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt to Equity - Last Qtr |
| 112 | `mdl25_rdv421_11v` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leverage (Assets/Equity) - Last Qtr |
| 113 | `mdl25_rlevv421_5v` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assets to Equity - Last Qtr |
| 114 | `mdl25_rlevv421_9v` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-Term Debt to Total Capital - Last Qtr (%) |
| 115 | `mdl25_vrv421_6v` | MATRIX | 0.619 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Book - 1 Qtr Difference |
| 116 | `mdl25_vrv421_7v` | MATRIX | 0.619 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Book - 1 Qtr Difference (%) |
| 117 | `mdl25_bsv421_9v` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted Average Net Operating Assets - 1 Qtr Difference (%) |
| 118 | `mdl25_isv421_5v` | MATRIX | 0.605 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue - Last Qtr |
| 119 | `mdl25_rliqv421_7v` | MATRIX | 0.562 | 其他 | 0 | — | — | — | UNUSABLE | Current Ratio - Last Qtr |
| 120 | `mdl25_isv421_62v` | MATRIX | 0.525 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends Per Share - Last Qtr |
| 121 | `mdl25_bsv421_11v` | MATRIX | 0.509 | 其他 | 0 | — | — | — | UNUSABLE | BV / Share - Last Qtr |
| 122 | `mdl25_eq_bs_v4_2_1_v10` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Book value at the end of the last fiscal quarter |
| 123 | `mdl25_eq_bs_v4_2_1_v11` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Book value per share at the end of the most recent fiscal quarter |
| 124 | `mdl25_eq_bs_v4_2_1_v12` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in book value per share (absolute) |
| 125 | `mdl25_eq_bs_v4_2_1_v13` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percentage change in book value per share |
| 126 | `mdl25_eq_bs_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total assets at the end of the last fiscal quarter |
| 127 | `mdl25_eq_bs_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percentage change in total assets |
| 128 | `mdl25_eq_bs_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average net operating assets in the last quarter |
| 129 | `mdl25_eq_bs_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted average net operating assets in the last quarter |
| 130 | `mdl25_eq_bs_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percentage change in adjusted average net operating assets |
| 131 | `mdl25_eq_cb_v4_2_1_v10` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average Traded Volume |
| 132 | `mdl25_eq_cb_v4_2_1_v11` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average Traded Volume (Local Currency) |
| 133 | `mdl25_eq_cb_v4_2_1_v12` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average Traded Volume (USD) |
| 134 | `mdl25_eq_cb_v4_2_1_v20` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Data-Through Date (Fundamental) Current |
| 135 | `mdl25_eq_cb_v4_2_1_v21` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Period End Date - Last Qtr |
| 136 | `mdl25_eq_cb_v4_2_1_v22` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Company Filing Date - Last Qtr |
| 137 | `mdl25_eq_cb_v4_2_1_v23` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Date a new filing was received for the last quarter |
| 138 | `mdl25_eq_cb_v4_2_1_v30` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Indicator whether last quarter financials are consolidated |
| 139 | `mdl25_eq_cb_v4_2_1_v6` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Market Cap (Local Currency) |
| 140 | `mdl25_eq_cb_v4_2_1_v7` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Cap (USD) |
| 141 | `mdl25_eq_cb_v4_2_1_v8` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | 52-week High Price |
| 142 | `mdl25_eq_cb_v4_2_1_v9` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | 52-week Low Price |
| 143 | `mdl25_eq_cfs_v4_2_1_v10` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percentage change in cash flow from investing activities |
| 144 | `mdl25_eq_cfs_v4_2_1_v11` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash flow from financing activities for the most recent fiscal quarter |
| 145 | `mdl25_eq_cfs_v4_2_1_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percentage change in cash flow from financing activities |
| 146 | `mdl25_eq_cfs_v4_2_1_v13` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow (FCF) for the last fiscal quarter |
| 147 | `mdl25_eq_cfs_v4_2_1_v14` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in free cash flow (FCF) |
| 148 | `mdl25_eq_cfs_v4_2_1_v15` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Capital expenditures for the most recent fiscal quarter |
| 149 | `mdl25_eq_cfs_v4_2_1_v16` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in capital expenditures (Capex) |
| 150 | `mdl25_eq_cfs_v4_2_1_v19` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Excess cash margin percentage for the last fiscal quarter |
| 151 | `mdl25_eq_cfs_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash flow for the last fiscal quarter |
| 152 | `mdl25_eq_cfs_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in total cash flow (absolute) |
| 153 | `mdl25_eq_cfs_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash flow from operations for the most recent fiscal quarter |
| 154 | `mdl25_eq_cfs_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percentage change in cash flow from operations |
| 155 | `mdl25_eq_cfs_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash flow from investing activities for the most recent fiscal quarter |
| 156 | `mdl25_eq_history_v10` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality Raw Current |
| 157 | `mdl25_eq_history_v11` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality Region Rank Current |
| 158 | `mdl25_eq_history_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals Component Current |
| 159 | `mdl25_eq_history_v13` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow Component Current |
| 160 | `mdl25_eq_history_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality Region |
| 161 | `mdl25_eq_is_v4_2_1_v10` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in EBITDA |
| 162 | `mdl25_eq_is_v4_2_1_v11` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average EBITDA growth over the past five years |
| 163 | `mdl25_eq_is_v4_2_1_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation from the 5-year average EBITDA growth |
| 164 | `mdl25_eq_is_v4_2_1_v13` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Percentage change in operating expenses from the prior quarter |
| 165 | `mdl25_eq_is_v4_2_1_v14` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBIT for the most recently reported fiscal quarter |
| 166 | `mdl25_eq_is_v4_2_1_v15` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in EBIT |
| 167 | `mdl25_eq_is_v4_2_1_v16` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income from continuing operations for the most recent quarter |
| 168 | `mdl25_eq_is_v4_2_1_v17` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in net income from continuing operations |
| 169 | `mdl25_eq_is_v4_2_1_v18` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Special items amount for the last fiscal quarter |
| 170 | `mdl25_eq_is_v4_2_1_v24` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income for the most recently reported fiscal quarter |
| 171 | `mdl25_eq_is_v4_2_1_v25` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in net income |
| 172 | `mdl25_eq_is_v4_2_1_v26` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends per share for the most recent quarter |
| 173 | `mdl25_eq_is_v4_2_1_v27` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in dividends per share (absolute amount) |
| 174 | `mdl25_eq_is_v4_2_1_v29` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Average EPS growth over the past five years |
| 175 | `mdl25_eq_is_v4_2_1_v30` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Deviation from the 5-year average EPS growth |
| 176 | `mdl25_eq_is_v4_2_1_v31` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from continuing operations for the most recent quarter |
| 177 | `mdl25_eq_is_v4_2_1_v32` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in basic EPS from continuing operations (absolute amount) |
| 178 | `mdl25_eq_is_v4_2_1_v33` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in basic EPS from continuing operations |
| 179 | `mdl25_eq_is_v4_2_1_v34` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from discontinued operations and extraordinary items for the last fiscal quarter |
| 180 | `mdl25_eq_is_v4_2_1_v35` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from discontinued operations and extraordinary items, quarter-over-quarter difference (absolute) |
| 181 | `mdl25_eq_is_v4_2_1_v37` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from total operations for the most recent quarter |
| 182 | `mdl25_eq_is_v4_2_1_v38` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from total operations, quarter-over-quarter difference (absolute) |
| 183 | `mdl25_eq_is_v4_2_1_v39` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from total operations, quarter-over-quarter difference (percent) |
| 184 | `mdl25_eq_is_v4_2_1_v43` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from continuing operations for the most recent quarter |
| 185 | `mdl25_eq_is_v4_2_1_v44` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from continuing operations, quarter-over-quarter difference (absolute) |
| 186 | `mdl25_eq_is_v4_2_1_v45` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from continuing operations, quarter-over-quarter difference (percent) |
| 187 | `mdl25_eq_is_v4_2_1_v46` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from discontinued operations and extraordinary items for the most recent quarter |
| 188 | `mdl25_eq_is_v4_2_1_v47` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from discontinued operations and extraordinary items, quarter-over-quarter difference (absolute) |
| 189 | `mdl25_eq_is_v4_2_1_v48` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from total operations for the most recent quarter |
| 190 | `mdl25_eq_is_v4_2_1_v49` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from total operations, quarter-over-quarter difference (absolute) |
| 191 | `mdl25_eq_is_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue for the most recently reported fiscal quarter |
| 192 | `mdl25_eq_is_v4_2_1_v50` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from total operations, quarter-over-quarter difference (percent) |
| 193 | `mdl25_eq_is_v4_2_1_v51` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Pension Expense - Last Year |
| 194 | `mdl25_eq_is_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in revenue |
| 195 | `mdl25_eq_is_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average revenue growth over the past five years |
| 196 | `mdl25_eq_is_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation from the 5-year average revenue growth |
| 197 | `mdl25_eq_is_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA for the most recently reported fiscal quarter |
| 198 | `mdl25_eq_pc_v4_2_1_v10` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Change Relative to Industry Benchmark (%) |
| 199 | `mdl25_eq_pc_v4_2_1_v11` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Change Relative to Country Benchmark (%) |
| 200 | `mdl25_eq_pc_v4_2_1_v12` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to ASX 100 (%) |
| 201 | `mdl25_eq_pc_v4_2_1_v13` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to ASX 200 (%) |
| 202 | `mdl25_eq_pc_v4_2_1_v14` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to ASX 300 (%) |
| 203 | `mdl25_eq_pc_v4_2_1_v15` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to ASX All Ord (%) |
| 204 | `mdl25_eq_pc_v4_2_1_v16` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to CAC 40 (%) |
| 205 | `mdl25_eq_pc_v4_2_1_v17` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to DJ STOXX 600 (%) |
| 206 | `mdl25_eq_pc_v4_2_1_v18` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to FTSE 100 (%) |
| 207 | `mdl25_eq_pc_v4_2_1_v19` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to Hang Seng (%) |
| 208 | `mdl25_eq_pc_v4_2_1_v20` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to JSE All Share (%) |
| 209 | `mdl25_eq_pc_v4_2_1_v21` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to MSCI EAFE (%) |
| 210 | `mdl25_eq_pc_v4_2_1_v22` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to MSCI EMF (%) |
| 211 | `mdl25_eq_pc_v4_2_1_v23` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to MSCI Europe (%) |
| 212 | `mdl25_eq_pc_v4_2_1_v24` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to MSCI Pac ex JP (%) |
| 213 | `mdl25_eq_pc_v4_2_1_v25` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to MSCI World (%) |
| 214 | `mdl25_eq_pc_v4_2_1_v26` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to R1000 Growth (%) |
| 215 | `mdl25_eq_pc_v4_2_1_v27` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to R1000 Value (%) |
| 216 | `mdl25_eq_pc_v4_2_1_v28` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to Russell 1000 (%) |
| 217 | `mdl25_eq_pc_v4_2_1_v29` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to Russell 2000 (%) |
| 218 | `mdl25_eq_pc_v4_2_1_v30` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to Russell Midcap (%) |
| 219 | `mdl25_eq_pc_v4_2_1_v31` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to S&P 400 (%) |
| 220 | `mdl25_eq_pc_v4_2_1_v32` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to S&P 500 (%) |
| 221 | `mdl25_eq_pc_v4_2_1_v33` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to S&P 600 (%) |
| 222 | `mdl25_eq_pc_v4_2_1_v34` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to TOPIX (%) |
| 223 | `mdl25_eq_pc_v4_2_1_v35` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Change Relative to TSX Composite (%) |
| 224 | `mdl25_eq_pc_v4_2_1_v5` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price Change (%) |
| 225 | `mdl25_eq_pc_v4_2_1_v6` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Change from 52-week High Price (ratio) |
| 226 | `mdl25_eq_pc_v4_2_1_v7` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Change from 52-week Low Price (ratio) |
| 227 | `mdl25_eq_pc_v4_2_1_v8` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diff from 50-day Moving Average (%) |
| 228 | `mdl25_eq_pc_v4_2_1_v9` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Diff from 200-day Moving Average (%) |
| 229 | `mdl25_eq_rd_v4_2_1_v10` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Pretax ROA (%) |
| 230 | `mdl25_eq_rd_v4_2_1_v11` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Leverage ratio (Assets/Equity) for the last reported quarter |
| 231 | `mdl25_eq_rd_v4_2_1_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Leverage (Assets/Equity) |
| 232 | `mdl25_eq_rd_v4_2_1_v13` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Return on Equity (%) for the last reported quarter |
| 233 | `mdl25_eq_rd_v4_2_1_v14` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Pretax ROE (%) |
| 234 | `mdl25_eq_rd_v4_2_1_v15` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on Equity (%) for the last reported quarter |
| 235 | `mdl25_eq_rd_v4_2_1_v16` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in ROE (%) |
| 236 | `mdl25_eq_rd_v4_2_1_v17` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Retention for the last reported quarter |
| 237 | `mdl25_eq_rd_v4_2_1_v18` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Earnings Retention |
| 238 | `mdl25_eq_rd_v4_2_1_v19` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Reinvestment Rate (%) for the last reported quarter |
| 239 | `mdl25_eq_rd_v4_2_1_v20` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Reinvestment Rate (%) |
| 240 | `mdl25_eq_rd_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Asset Turnover for the last reported quarter |
| 241 | `mdl25_eq_rd_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Asset Turnover (last quarter vs prior quarter) |
| 242 | `mdl25_eq_rd_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) for the last reported quarter |
| 243 | `mdl25_eq_rd_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Pretax Margin (%) |
| 244 | `mdl25_eq_rd_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Return on Assets (%) for the last reported quarter |
| 245 | `mdl25_eq_rlev_v4_2_1_v10` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Long-Term Debt to Total Capital percentage |
| 246 | `mdl25_eq_rlev_v4_2_1_v11` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Debt to EBITDA ratio for the most recent quarter ((Total Debt minus Cash) divided by EBITDA) |
| 247 | `mdl25_eq_rlev_v4_2_1_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in Net Debt to EBITDA |
| 248 | `mdl25_eq_rlev_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets to Equity ratio for the most recent quarter (Total Assets divided by Shareholders' Equity) |
| 249 | `mdl25_eq_rlev_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in the Assets to Equity ratio |
| 250 | `mdl25_eq_rlev_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt to Equity ratio for the most recent quarter (Total Debt divided by Shareholders' Equity) |
| 251 | `mdl25_eq_rlev_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in the Debt to Equity ratio |
| 252 | `mdl25_eq_rlev_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Debt as a percentage of Total Capital for the most recent quarter |
| 253 | `mdl25_eq_rliq_v4_2_1_v11` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash Cycle - Last Qtr |
| 254 | `mdl25_eq_rliq_v4_2_1_v12` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash Cycle - 1 Qtr Difference |
| 255 | `mdl25_eq_rliq_v4_2_1_v5` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quick Ratio - Last Qtr |
| 256 | `mdl25_eq_rliq_v4_2_1_v6` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quick Ratio - 1 Qtr Difference |
| 257 | `mdl25_eq_rliq_v4_2_1_v7` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Current Ratio - Last Qtr |
| 258 | `mdl25_eq_rliq_v4_2_1_v8` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Current Ratio - 1 Qtr Difference |
| 259 | `mdl25_eq_rliq_v4_2_1_v9` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Times Interest Earned - Last Qtr |
| 260 | `mdl25_eq_ro_v4_2_1_v10` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inventory turnover for the last fiscal quarter |
| 261 | `mdl25_eq_ro_v4_2_1_v11` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in inventory turnover |
| 262 | `mdl25_eq_ro_v4_2_1_v12` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Average inventory days (days inventory outstanding) for the last fiscal quarter |
| 263 | `mdl25_eq_ro_v4_2_1_v13` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in average inventory days (DIO) |
| 264 | `mdl25_eq_ro_v4_2_1_v14` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Working capital to sales ratio for the last fiscal quarter |
| 265 | `mdl25_eq_ro_v4_2_1_v15` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in working capital to sales ratio |
| 266 | `mdl25_eq_ro_v4_2_1_v16` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net operating asset turnover for the last fiscal quarter |
| 267 | `mdl25_eq_ro_v4_2_1_v17` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net operating asset turnover for the last fiscal year |
| 268 | `mdl25_eq_ro_v4_2_1_v18` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year change in adjusted net operating asset turnover |
| 269 | `mdl25_eq_ro_v4_2_1_v19` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on net operating assets (RNOA) percentage for the last fiscal quarter |
| 270 | `mdl25_eq_ro_v4_2_1_v20` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in return on net operating assets (RNOA) percentage |
| 271 | `mdl25_eq_ro_v4_2_1_v21` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on adjusted net operating assets percentage for the last fiscal year |
| 272 | `mdl25_eq_ro_v4_2_1_v22` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year change in return on adjusted net operating assets percentage |
| 273 | `mdl25_eq_ro_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in net operating asset turnover |
| 274 | `mdl25_eq_ro_v4_2_1_v6` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Accounts receivable turnover for the last fiscal quarter |
| 275 | `mdl25_eq_ro_v4_2_1_v7` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in accounts receivable turnover |
| 276 | `mdl25_eq_ro_v4_2_1_v8` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Average accounts receivable days (days sales outstanding) for the last fiscal quarter |
| 277 | `mdl25_eq_ro_v4_2_1_v9` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter change in average accounts receivable days (DSO) |
| 278 | `mdl25_eq_rp_v4_2_1_v10` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA Margin (%) - 1 Quarter Difference |
| 279 | `mdl25_eq_rp_v4_2_1_v11` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Margin (%) - Last Quarter |
| 280 | `mdl25_eq_rp_v4_2_1_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Margin (%) - 1 Quarter Difference |
| 281 | `mdl25_eq_rp_v4_2_1_v13` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average Historical Operating Margin 5-Year |
| 282 | `mdl25_eq_rp_v4_2_1_v14` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diff from Average Hist Operating Margin 5-Year |
| 283 | `mdl25_eq_rp_v4_2_1_v15` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) - Last Quarter |
| 284 | `mdl25_eq_rp_v4_2_1_v16` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) - 1 Quarter Difference |
| 285 | `mdl25_eq_rp_v4_2_1_v17` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective Tax Rate (%) - Last Quarter |
| 286 | `mdl25_eq_rp_v4_2_1_v18` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective Tax Rate (%) - 1 Quarter Difference |
| 287 | `mdl25_eq_rp_v4_2_1_v19` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Margin (%) - Last Quarter |
| 288 | `mdl25_eq_rp_v4_2_1_v20` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Margin (%) - 1 Quarter Difference |
| 289 | `mdl25_eq_rp_v4_2_1_v5` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Margin (%) - Last Quarter |
| 290 | `mdl25_eq_rp_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Margin (%) - 1 Quarter Difference |
| 291 | `mdl25_eq_rp_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average Historical Gross Margin - 5-Year |
| 292 | `mdl25_eq_rp_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diff from Average Hist Gross Margin - 5-Year |
| 293 | `mdl25_eq_rp_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA Margin (%) - Last Quarter |
| 294 | `mdl25_eq_v4_2_1_v10` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Accruals - Period End Date |
| 295 | `mdl25_eq_v4_2_1_v12` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Cash Flow |
| 296 | `mdl25_eq_v4_2_1_v13` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Cash Flow - 1 Day Difference |
| 297 | `mdl25_eq_v4_2_1_v14` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Cash Flow - Period End Date |
| 298 | `mdl25_eq_v4_2_1_v16` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Operating Efficiency |
| 299 | `mdl25_eq_v4_2_1_v17` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Operating Efficiency - 1 Day Difference |
| 300 | `mdl25_eq_v4_2_1_v18` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Operating Efficiency - Period End Date |
| 301 | `mdl25_eq_v4_2_1_v22` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Raw Earnings Quality |
| 302 | `mdl25_eq_v4_2_1_v6` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality Region Rank |
| 303 | `mdl25_eq_v4_2_1_v7` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality Region Rank - 1 Day Difference |
| 304 | `mdl25_eq_v4_2_1_v8` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Accruals |
| 305 | `mdl25_eq_v4_2_1_v9` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Quality by Accruals - 1 Day Difference |
| 306 | `mdl25_eq_vr_v4_2_1_v10` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Year-over-year percent change in price-to-sales ratio |
| 307 | `mdl25_eq_vr_v4_2_1_v11` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-cash-from-operations ratio |
| 308 | `mdl25_eq_vr_v4_2_1_v12` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-free-cash-flow ratio |
| 309 | `mdl25_eq_vr_v4_2_1_v13` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Enterprise Value (EV) |
| 310 | `mdl25_eq_vr_v4_2_1_v14` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Enterprise value to EBITDA ratio (EV/EBITDA) |
| 311 | `mdl25_eq_vr_v4_2_1_v15` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in EV/EBITDA |
| 312 | `mdl25_eq_vr_v4_2_1_v16` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Enterprise value to sales ratio (EV/Sales) |
| 313 | `mdl25_eq_vr_v4_2_1_v17` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow yield (FCF divided by market cap), percent |
| 314 | `mdl25_eq_vr_v4_2_1_v18` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow to enterprise value (FCF/EV), percent |
| 315 | `mdl25_eq_vr_v4_2_1_v19` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash from operations to enterprise value (CFO/EV), percent |
| 316 | `mdl25_eq_vr_v4_2_1_v5` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-book ratio (market price per share divided by book value per share) |
| 317 | `mdl25_eq_vr_v4_2_1_v6` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter absolute change in price-to-book ratio |
| 318 | `mdl25_eq_vr_v4_2_1_v7` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quarter-over-quarter percent change in price-to-book ratio |
| 319 | `mdl25_eq_vr_v4_2_1_v8` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-sales ratio |
| 320 | `mdl25_eq_vr_v4_2_1_v9` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Year-over-year absolute change in price-to-sales ratio |
| 321 | `mdl25_isv421_42v` | MATRIX | 0.492 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Income - Last Qtr |
| 322 | `mdl25_rdv421_7v` | MATRIX | 0.490 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) - Last Qtr |
| 323 | `mdl25_rpv421_51v` | MATRIX | 0.490 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) - Last Qtr |
| 324 | `mdl25_rpv421_71v` | MATRIX | 0.482 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective Tax Rate (%) - Last Qtr |
| 325 | `mdl25_isv421_61v` | MATRIX | 0.481 | 其他 | 0 | — | — | — | UNUSABLE | NI from Cont. Ops - Last Qtr |
| 326 | `mdl25_73v` | MATRIX | 0.479 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Total Ops - Last Qtr |
| 327 | `mdl25_84v` | MATRIX | 0.478 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Total Ops - Last Qtr |
| 328 | `mdl25_rpv421_91v` | MATRIX | 0.478 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Margin (%) - Last Qtr |
| 329 | `mdl25_34v` | MATRIX | 0.476 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Continuing Ops - Last Qtr |
| 330 | `mdl25_64v` | MATRIX | 0.475 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Disc Ops & XO - Last Qtr |
| 331 | `mdl25_isv421_41v` | MATRIX | 0.475 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBIT - Last Qtr |
| 332 | `mdl25_rdv421_31v` | MATRIX | 0.474 | 其他 | 0 | — | — | — | UNUSABLE | Pretax ROE (%) - Last Qtr |
| 333 | `mdl25_isv421_9v` | MATRIX | 0.474 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA - Last Qtr |
| 334 | `mdl25_rliqv421_5v` | MATRIX | 0.473 | 其他 | 0 | — | — | — | UNUSABLE | Quick Ratio - Last Qtr |
| 335 | `mdl25_rpv421_11v` | MATRIX | 0.472 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Margin (%) - Last Qtr |
| 336 | `mdl25_rlevv421_11v` | MATRIX | 0.471 | 盈利与财务 | 0 | — | — | — | UNUSABLE | (Total Debt - Cash) / EBITDA - Last Qtr |
| 337 | `mdl25_rpv421_9v` | MATRIX | 0.470 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA Margin (%) - Last Qtr |
| 338 | `mdl25_isv421_13v` | MATRIX | 0.468 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Continuing Ops - Last Qtr |
| 339 | `mdl25_isv421_43v` | MATRIX | 0.467 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Disc Ops & XO - Last Qtr |
| 340 | `mdl25_rlevv421_8v` | MATRIX | 0.462 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt to Equity - 1 Qtr Difference |
| 341 | `mdl25_bsv421_6v` | MATRIX | 0.462 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Assets - 1 Qtr Difference (%) |
| 342 | `mdl25_rdv421_21v` | MATRIX | 0.461 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Leverage (Assets/Equity) - 1 Qtr Difference |
| 343 | `mdl25_rlevv421_6v` | MATRIX | 0.461 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets to Equity - 1 Qtr Difference |
| 344 | `mdl25_rov421_61v` | MATRIX | 0.461 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Op. Asset Turnover - Last Qtr |
| 345 | `mdl25_rlevv421_01v` | MATRIX | 0.459 | 盈利与财务 | 0 | — | — | — | UNUSABLE | % Long-Term Debt to Total Capital - 1 Qtr Difference |
| 346 | `mdl25_rov421_91v` | MATRIX | 0.450 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on Net Op. Assets (%) - Last Qtr |
| 347 | `mdl25_rdv421_51v` | MATRIX | 0.449 | 其他 | 0 | — | — | — | UNUSABLE | ROE (%) - Last Qtr |
| 348 | `mdl25_rdv421_5v` | MATRIX | 0.445 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Asset Turnover - Last Qtr |
| 349 | `mdl25_rdv421_9v` | MATRIX | 0.444 | 其他 | 0 | — | — | — | UNUSABLE | Pretax ROA (%) - Last Qtr |
| 350 | `mdl25_rpv421_5v` | MATRIX | 0.426 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Margin (%) - Last Qtr |
| 351 | `mdl25_vrv421_51v` | MATRIX | 0.426 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EV/EBITDA - 1 Qtr Difference (%) |
| 352 | `mdl25_cfsv421_31v` | MATRIX | 0.413 | 其他 | 0 | — | — | — | UNUSABLE | FCF - Last Qtr |
| 353 | `mdl25_cfsv421_7v` | MATRIX | 0.413 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow from Ops - Last Qtr |
| 354 | `mdl25_isv421_6v` | MATRIX | 0.411 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue - 1 Qtr Difference (%) |
| 355 | `mdl25_cfsv421_9v` | MATRIX | 0.410 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow from Investing - Last Qtr |
| 356 | `mdl25_cfsv421_5v` | MATRIX | 0.409 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Cash Flow - Last Qtr |
| 357 | `mdl25_cfsv421_11v` | MATRIX | 0.408 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow from Financing - Last Qtr |
| 358 | `mdl25_isv421_52v` | MATRIX | 0.408 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Income - 1 Qtr Difference (%) |
| 359 | `mdl25_isv421_71v` | MATRIX | 0.407 | 其他 | 0 | — | — | — | UNUSABLE | NI from Cont. Ops - 1 Qtr Difference (%) |
| 360 | `mdl25_rdv421_8v` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) - 1 Qtr Difference |
| 361 | `mdl25_rpv421_61v` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pretax Margin (%) - 1 Qtr Difference |
| 362 | `mdl25_rpv421_81v` | MATRIX | 0.406 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective Tax Rate (%) - 1 Qtr Difference |
| 363 | `mdl25_rpv421_02v` | MATRIX | 0.405 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Margin (%) - 1 Qtr Difference |
| 364 | `mdl25_cfsv421_91v` | MATRIX | 0.404 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Excess Cash Margin (%) - Last Qtr |
| 365 | `mdl25_rdv421_41v` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Pretax ROE (%) - Chg 1 Qtr |
| 366 | `mdl25_83v` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Total Ops - 1 Qtr Difference |
| 367 | `mdl25_cfsv421_41v` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | FCF - 1 Qtr Difference (%) |
| 368 | `mdl25_cfsv421_8v` | MATRIX | 0.402 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow from Ops - 1 Qtr Difference (%) |
| 369 | `mdl25_93v` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Total Ops - 1 Qtr Difference (%) |
| 370 | `mdl25_rliqv421_8v` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Current Ratio - 1 Qtr Difference |
| 371 | `mdl25_05v` | MATRIX | 0.401 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Total Ops - 1 Qtr Difference (%) |
| 372 | `mdl25_94v` | MATRIX | 0.401 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Total Ops - 1 Qtr Difference |
| 373 | `mdl25_44v` | MATRIX | 0.401 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Continuing Ops - 1 Qtr Difference |
| 374 | `mdl25_54v` | MATRIX | 0.401 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Continuing Ops - 1 Qtr Difference (%) |
| 375 | `mdl25_74v` | MATRIX | 0.401 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS from Disc Ops & XO - 1 Qtr Difference |
| 376 | `mdl25_cfsv421_01v` | MATRIX | 0.399 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow from Investing - 1 Qtr Difference (%) |
| 377 | `mdl25_cfsv421_6v` | MATRIX | 0.399 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Cash Flow - 1 Qtr Difference |
| 378 | `mdl25_isv421_51v` | MATRIX | 0.399 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBIT - 1 Qtr Difference (%) |
| 379 | `mdl25_isv421_31v` | MATRIX | 0.398 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expenses - 1 Qtr Difference (%) |
| 380 | `mdl25_isv421_01v` | MATRIX | 0.398 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA - 1 Qtr Difference (%) |
| 381 | `mdl25_rdv421_61v` | MATRIX | 0.398 | 其他 | 0 | — | — | — | UNUSABLE | ROE (%) - 1 Qtr Difference |
| 382 | `mdl25_rlevv421_21v` | MATRIX | 0.398 | 盈利与财务 | 0 | — | — | — | UNUSABLE | (Total Debt - Cash) / EBITDA - Chg 1 Qtr |
| 383 | `mdl25_bsv421_21v` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | BV / Share - 1 Qtr Difference |
| 384 | `mdl25_bsv421_31v` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | BV/Share - 1 Qtr Difference (%) |
| 385 | `mdl25_rpv421_21v` | MATRIX | 0.397 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Margin (%) - 1 Qtr Difference |
| 386 | `mdl25_rdv421_01v` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Pretax ROA (%) - 1 Qtr Difference |
| 387 | `mdl25_rpv421_01v` | MATRIX | 0.397 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDA Margin (%) - 1 Qtr Difference |
| 388 | `mdl25_rdv421_6v` | MATRIX | 0.397 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Asset Turnover - 1 Qtr Difference |
| 389 | `mdl25_rdv421_71v` | MATRIX | 0.397 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Retention - Last Qtr |
| 390 | `mdl25_isv421_23v` | MATRIX | 0.394 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Continuing Ops - 1 Qtr Difference |
| 391 | `mdl25_isv421_33v` | MATRIX | 0.394 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Continuing Ops - 1 Qtr Difference (%) |
| 392 | `mdl25_isv421_53v` | MATRIX | 0.394 | 其他 | 0 | — | — | — | UNUSABLE | Basic EPS from Disc Ops & XO - 1 Qtr Difference |
| 393 | `mdl25_cfsv421_21v` | MATRIX | 0.393 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Flow from Financing - 1 Qtr Difference (%) |
| 394 | `mdl25_rliqv421_11v` | MATRIX | 0.392 | 其他 | 0 | — | — | — | UNUSABLE | Cash Cycle - Last Qtr |
| 395 | `mdl25_rov421_41v` | MATRIX | 0.388 | 其他 | 0 | — | — | — | UNUSABLE | WC/Sales - Last Qtr |
| 396 | `mdl25_rov421_6v` | MATRIX | 0.386 | 价量与波动 | 0 | — | — | — | UNUSABLE | A/R Turnover - Last Qtr |
| 397 | `mdl25_rov421_8v` | MATRIX | 0.385 | 其他 | 0 | — | — | — | UNUSABLE | Avg. A/R Days - Last Qtr |
| 398 | `mdl25_rov421_5v` | MATRIX | 0.385 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Op. Asset Turnover - 1 Qtr Difference |
| 399 | `mdl25_rov421_02v` | MATRIX | 0.382 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on Net Operating Assets (%) - 1 Qtr Difference |
| 400 | `mdl25_isv421_72v` | MATRIX | 0.369 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends Per Share - 1 Qtr Difference |
| 401 | `mdl25_rdv421_91v` | MATRIX | 0.367 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Reinvestment Rate (%) - Last Qtr |
| 402 | `mdl25_rpv421_6v` | MATRIX | 0.360 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Margin (%) - 1 Qtr Difference |
| 403 | `mdl25_rliqv421_21v` | MATRIX | 0.352 | 其他 | 0 | — | — | — | UNUSABLE | Cash Cycle - 1 Qtr Difference |
| 404 | `mdl25_rov421_51v` | MATRIX | 0.351 | 其他 | 0 | — | — | — | UNUSABLE | WC/Sales - 1 Qtr Difference |
| 405 | `mdl25_rov421_7v` | MATRIX | 0.347 | 价量与波动 | 0 | — | — | — | UNUSABLE | A/R Turnover - 1 Qtr Difference |
| 406 | `mdl25_rov421_9v` | MATRIX | 0.346 | 其他 | 0 | — | — | — | UNUSABLE | Avg. A/R Days - 1 Qtr Difference |
| 407 | `mdl25_cfsv421_51v` | MATRIX | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Capex - Last Qtr |
| 408 | `mdl25_rliqv421_6v` | MATRIX | 0.331 | 其他 | 0 | — | — | — | UNUSABLE | Quick Ratio - 1 Qtr Difference |
| 409 | `mdl25_cfsv421_61v` | MATRIX | 0.331 | 其他 | 0 | — | — | — | UNUSABLE | Capex - 1 Qtr Difference (%) |
| 410 | `mdl25_rdv421_81v` | MATRIX | 0.312 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Retention - 1 Qtr Difference |
| 411 | `mdl25_rov421_01v` | MATRIX | 0.306 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inv Turnover - Last Qtr |
| 412 | `mdl25_rov421_21v` | MATRIX | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Avg Inventory Days - Last Qtr |
| 413 | `mdl25_rdv421_02v` | MATRIX | 0.304 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Reinvestment Rate (%) - 1 Qtr Difference |
| 414 | `mdl25_rov421_11v` | MATRIX | 0.280 | 价量与波动 | 0 | — | — | — | UNUSABLE | Inv Turnover - 1 Qtr Difference |
| 415 | `mdl25_rov421_31v` | MATRIX | 0.280 | 其他 | 0 | — | — | — | UNUSABLE | Avg Inventory Days - 1 Qtr Difference |
| 416 | `mdl25_isv421_81v` | MATRIX | 0.267 | 其他 | 0 | — | — | — | UNUSABLE | Special Items - Last Qtr |
| 417 | `mdl25_rliqv421_9v` | MATRIX | 0.262 | 其他 | 0 | — | — | — | UNUSABLE | Times Interest Earned - Last Qtr |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

