# analyst15 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst15` |
| 名称 | Earnings forecasts |
| 类别 | ANALYST |
| 数据字段数(平台) | 1744 |
| 覆盖率 | 0.511 |
| 平台已有 alpha | 911 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides bottom-up aggregated earnings forecasts and related financial metrics at the country, sector, industry, and index levels, covering 56 countries and major international indices with history back to 1985. It includes consensus analyst estimates for key measures such as EPS, revenue, book value, cash flow, dividends, P/E ratios, and long-term growth, all calendarized and available in local and common currencies. The data is structured to support global asset allocation, cross-border valuation, sector and industry analysis, and derivatives research. By tracking changes in consensus, estimate revisions, and aggregated sentiment, the dataset enables investors to identify under- or overvalued markets, monitor macro and sector trends, and anticipate shifts in market sentiment

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **1744** |
| 类型分布 | MATRIX×1744 |
| 平均覆盖率 | **0.511** |
| 覆盖率区间 | 0.50 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 31 | 1.8% |
| 中 (0.70–0.90) | 12 | 0.7% |
| 低 (0.50–0.70) | 1701 | 97.5% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 1701 | 97.5% |
| UNTESTED | 43 | 2.5% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 43 / UNUSABLE 1701 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 654 | 0.50 | anl15_bps_gr_12_m_ests、anl15_bps_gr_12_m_ests_dn、anl15_bps_gr_12_m_ests_up |
| 盈利与财务 | 640 | 0.51 | ebg_sector_12mo_marketcap_percent、ebg_sector_18mo_marketcap_percent、ebg_sector_fy2_marketcap_percent |
| 宏观与行业 | 312 | 0.52 | group_government_bond_yield、sector_12mo_marketcap_percent、sector_18mo_marketcap_percent |
| 其他 | 117 | 0.52 | group_12mo_marketcap_percent、group_18mo_marketcap_percent、group_fy2_marketcap_percent |
| 价量与波动 | 21 | 0.50 | anl15_ebg_gr_12_m_mktcap、anl15_ebg_gr_cal_fy1_mktcap、anl15_ebg_gr_cal_fy2_mktcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `ebg_sector_12mo_marketcap_percent` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector based on twelve-month forward data using earnings before goodwill. |
| 2 | `ebg_sector_18mo_marketcap_percent` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector based on eighteen-month forward data using earnings before goodwill. |
| 3 | `ebg_sector_fy2_marketcap_percent` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector in calendarized fiscal year 2 based on earnings before goodwill. |
| 4 | `ebg_sector_fy3_marketcap_percent` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector in calendarized fiscal year 3 based on earnings before goodwill. |
| 5 | `ebg_sector_government_bond_yield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The yield on a local 10-year government bond for the sector's region, based on earnings before goodwill. |
| 6 | `ebg_sector_longterm_growth_marketcap_percent` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector based on long-term growth forecasts using earnings before goodwill. |
| 7 | `group_12mo_marketcap_percent` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group based on twelve-month forward data. |
| 8 | `group_18mo_marketcap_percent` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group based on eighteen-month forward data. |
| 9 | `group_fy2_marketcap_percent` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group in calendarized fiscal year 2. |
| 10 | `group_fy3_marketcap_percent` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group in calendarized fiscal year 3. |
| 11 | `group_government_bond_yield` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The yield on a local 10-year government bond for the group's region. |
| 12 | `sector_12mo_marketcap_percent` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector based on twelve-month forward data. |
| 13 | `sector_18mo_marketcap_percent` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector based on eighteen-month forward data. |
| 14 | `sector_aggregate_currency_code` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The currency in which sector-level aggregate data is reported. |
| 15 | `sector_bookvalue_currency_code_nogics` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The currency in which sector-level book value per share is reported (non-GICS version). |
| 16 | `sector_cashflow_currency_code_nogics` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The currency in which sector-level cash flow per share is reported (non-GICS version). |
| 17 | `sector_dividend_currency_code_nogics` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The currency in which sector-level dividend per share is reported (non-GICS version). |
| 18 | `sector_ebg_currency_code` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The currency in which sector-level earnings per share before goodwill is reported. |
| 19 | `sector_ebt_currency_code` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The currency in which sector-level earnings before tax is reported. |
| 20 | `sector_fy2_marketcap_percent` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector in calendarized fiscal year 2. |
| 21 | `sector_fy3_marketcap_percent` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector in calendarized fiscal year 3. |
| 22 | `sector_government_bond_yield` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The yield on a local 10-year government bond for the sector's region. |
| 23 | `sector_longterm_growth_marketcap_percent` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the sector based on long-term growth forecasts. |
| 24 | `sector_sales_currency_code` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The currency in which sector-level sales are reported. |
| 25 | `ebg_group_12mo_marketcap_percent` | MATRIX | 0.967 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group based on twelve-month forward data using earnings before goodwill. |
| 26 | `ebg_group_18mo_marketcap_percent` | MATRIX | 0.967 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group based on eighteen-month forward data using earnings before goodwill. |
| 27 | `ebg_group_fy2_marketcap_percent` | MATRIX | 0.967 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group in calendarized fiscal year 2 based on earnings before goodwill. |
| 28 | `ebg_group_government_bond_yield` | MATRIX | 0.967 | 盈利与财务 | 0 | — | — | — | UNTESTED | The yield on a local 10-year government bond for the group's region, based on earnings before goodwill. |
| 29 | `ebg_group_fy3_marketcap_percent` | MATRIX | 0.966 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group in calendarized fiscal year 3 based on earnings before goodwill. |
| 30 | `group_longterm_growth_marketcap_percent` | MATRIX | 0.950 | 其他 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group based on long-term growth forecasts. |
| 31 | `ebg_group_longterm_growth_marketcap_percent` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the group based on long-term growth forecasts using earnings before goodwill. |
| 32 | `industry_12mo_marketcap_percent` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry based on twelve-month forward data. |
| 33 | `industry_fy2_marketcap_percent` | MATRIX | 0.890 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization represented by the industry in calendarized fiscal year 2. |
| 34 | `industry_18mo_marketcap_percent` | MATRIX | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry based on eighteen-month forward data. |
| 35 | `industry_government_bond_yield` | MATRIX | 0.888 | 宏观与行业 | 0 | — | — | — | UNTESTED | The yield on a local 10-year government bond for the industry's region. |
| 36 | `industry_fy3_marketcap_percent` | MATRIX | 0.885 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization represented by the industry in calendarized fiscal year 3. |
| 37 | `ebg_industry_12mo_marketcap_percent` | MATRIX | 0.812 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry based on twelve-month forward data using earnings before goodwill. |
| 38 | `ebg_industry_18mo_marketcap_percent` | MATRIX | 0.812 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry based on eighteen-month forward data using earnings before goodwill. |
| 39 | `ebg_industry_fy2_marketcap_percent` | MATRIX | 0.812 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry in calendarized fiscal year 2 based on earnings before goodwill. |
| 40 | `ebg_industry_government_bond_yield` | MATRIX | 0.812 | 盈利与财务 | 0 | — | — | — | UNTESTED | The yield on a local 10-year government bond for the industry's region, based on earnings before goodwill. |
| 41 | `ebg_industry_fy3_marketcap_percent` | MATRIX | 0.809 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry in calendarized fiscal year 3 based on earnings before goodwill. |
| 42 | `industry_longterm_growth_marketcap_percent` | MATRIX | 0.800 | 宏观与行业 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry based on long-term growth forecasts. |
| 43 | `ebg_industry_longterm_growth_marketcap_percent` | MATRIX | 0.757 | 盈利与财务 | 0 | — | — | — | UNTESTED | The percentage of market capitalization for the industry based on long-term growth forecasts using earnings before goodwill. |
| 44 | `anl15_bps_gr_12_m_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in forward 12-month BPS forecasts using a constant sample, aggregated at the group level |
| 45 | `anl15_bps_gr_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward earnings forecasts, aggregated at the group level |
| 46 | `anl15_bps_gr_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward earnings forecasts, using a constant sample, aggregated at the group level in AMR |
| 47 | `anl15_bps_gr_12_m_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean book value per share(BPS) estimation within GICS group grouping. |
| 48 | `anl15_bps_gr_12_m_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level number of companies whose 12-month forward mean BPS was lowered since last month |
| 49 | `anl15_bps_gr_12_m_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level number of companies with raised 12-month forward mean EPS since last month |
| 50 | `anl15_bps_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates within GICS group grouping. |
| 51 | `anl15_bps_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level pro-rated number of 12-month forward BPS estimates lowered since last month |
| 52 | `anl15_bps_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level pro-rated number of 12-month forward estimates raised since last month |
| 53 | `anl15_bps_gr_12_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted 12 month forward year over year growth of book value per share(BPS) estimation aggregated within GICS group grouping. |
| 54 | `anl15_bps_gr_12_m_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted average of 12 month forward book value per share(BPS) estimation aggregated within GICS group grouping. |
| 55 | `anl15_bps_gr_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average Price/Earnings ratio based on 12-month forward earnings |
| 56 | `anl15_bps_gr_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of 12-month forward earnings forecasts, aggregated at the group level in Europe |
| 57 | `anl15_bps_gr_12_m_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The total of 12 month forward book value per share(BPS) estimation aggregated within GICS group grouping. |
| 58 | `anl15_bps_gr_12_m_tr_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted average of 12 month trailing book value per share(BPS) aggregated within GICS group grouping. |
| 59 | `anl15_bps_gr_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in the 18-month forward earnings forecasts, using a constant sample, aggregated at the group level for the |
| 60 | `anl15_bps_gr_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 18-month forward earnings forecasts, using a constant sample, aggregated at the group level for t |
| 61 | `anl15_bps_gr_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecasts, using a constant sample, aggregated at the group level in AMR |
| 62 | `anl15_bps_gr_18_m_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a 18 month forward mean book value per share(BPS) estimation within GICS group grouping. |
| 63 | `anl15_bps_gr_18_m_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean book value per share(BPS) estimation has been lowered from last month within GICS gr |
| 64 | `anl15_bps_gr_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose 18-month forward consensus mean earnings was raised since last month, aggregated at group level |
| 65 | `anl15_bps_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of 18-month forward BPS estimates, aggregated at the group level for the Americas |
| 66 | `anl15_bps_gr_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with negative revision over the trailing 18 months, aggregated at the group level for Asia |
| 67 | `anl15_bps_gr_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with positive revision for the 18-month forward period, aggregated at the group level in AMR |
| 68 | `anl15_bps_gr_18_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted 18 month forward year over year growth of book value per share(BPS) estimation aggregated within GICS group grouping. |
| 69 | `anl15_bps_gr_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of 18-month forward BPS consensus forecasts, aggregated at group level |
| 70 | `anl15_bps_gr_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18 month forward EPS estimation aggregated within GICS group grouping. |
| 71 | `anl15_bps_gr_18_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted average standard deviation of 18-month forward EPS forecasts |
| 72 | `anl15_bps_gr_18_m_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The total of 18 month forward book value per share(BPS) estimation aggregated within GICS group grouping. |
| 73 | `anl15_bps_gr_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted year-over-year growth in earnings for calendarized Fiscal Year 0, percent change weighted by shares |
| 74 | `anl15_bps_gr_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 0 aggregated at the group level |
| 75 | `anl15_bps_gr_cal_fy0_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The total of book value per share(BPS) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 76 | `anl15_bps_gr_cal_fy0_val` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted average of book value per share(BPS) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 77 | `anl15_bps_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in earnings forecasts for calendarized Fiscal Year 1, using a constant sample, aggregated at group level |
| 78 | `anl15_bps_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in earnings forecasts for calendarized Fiscal Year 1 using a constant sample aggregated at group level |
| 79 | `anl15_bps_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Six month percent change for calendarized Fiscal Year 1 aggregated at group level |
| 80 | `anl15_bps_gr_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates (coverage count) contributing to the FY1 BPS consensus at the group level, globally |
| 81 | `anl15_bps_gr_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of estimates for calendarized Fiscal Year 1, aggregated at group level |
| 82 | `anl15_bps_gr_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted year-over-year growth in earnings for calendarized Fiscal Year 1 |
| 83 | `anl15_bps_gr_cal_fy1_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted average BPS for calendarized Fiscal Year 1 |
| 84 | `anl15_bps_gr_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 1 aggregated at group level |
| 85 | `anl15_bps_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level weighted average standard deviation of consensus BPS forecasts for calendarized Fiscal Year 1 |
| 86 | `anl15_bps_gr_cal_fy1_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The total of book value per share(BPS) estimation for the calendarized one fiscal year aggregated within GICS group grouping. |
| 87 | `anl15_bps_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in calendarized Fiscal Year 2 BPS forecasts, using a constant sample |
| 88 | `anl15_bps_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY2 BPS forecasts, using a constant sample, at the group level in the AMR region |
| 89 | `anl15_bps_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in earnings forecasts for calendarized Fiscal Year 2, using a constant sample |
| 90 | `anl15_bps_gr_cal_fy2_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized two fiscal year book value per share(BPS) estimation within GICS group grouping. |
| 91 | `anl15_bps_gr_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of estimates for the calendarized FY2 BPS period |
| 92 | `anl15_bps_gr_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 2, aggregated at group level |
| 93 | `anl15_bps_gr_cal_fy2_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average calendarized FY2 book value per share (BPS) forecast at the group level for the Americas |
| 94 | `anl15_bps_gr_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 2 at the group level in AMR |
| 95 | `anl15_bps_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 2, aggregated at group level |
| 96 | `anl15_bps_gr_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 2 period (sum of EPS times shares), aggregated at the group level in AMR |
| 97 | `anl15_bps_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 3 BPS forecasts using a constant sample aggregated at the group level for Japa |
| 98 | `anl15_bps_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in forecasts for calendarized Fiscal Year 3 using a constant sample aggregated at the group level |
| 99 | `anl15_bps_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 earnings forecasts (constant-sample), aggregated at the group level |
| 100 | `anl15_bps_gr_cal_fy3_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized three fiscal year book value per share(BPS) estimation within GICS group grouping. |
| 101 | `anl15_bps_gr_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized Fiscal Year 3 aggregated at the group level |
| 102 | `anl15_bps_gr_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 3, aggregated at the group level for Asia |
| 103 | `anl15_bps_gr_cal_fy3_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized Fiscal Year 3, aggregated at the group level in AMR |
| 104 | `anl15_bps_gr_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average price/earnings ratio based on calendarized Fiscal Year 3 forecasts |
| 105 | `anl15_bps_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GIC |
| 106 | `anl15_bps_gr_cal_fy3_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total sum of Fiscal Year 3 estimates aggregated at group level |
| 107 | `anl15_bps_gr_fy1_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies for which book value per share(BPS) estimation for the calendarized one fiscal year has been lowered from last month |
| 108 | `anl15_bps_gr_fy1_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies for which book value per share(BPS) estimation for the calendarized one fiscal year has been raised from last month  |
| 109 | `anl15_bps_gr_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates lowered since last month aggregated at group level |
| 110 | `anl15_bps_gr_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates raised since last month, aggregated at the group level in AMR |
| 111 | `anl15_bps_gr_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose FY2 consensus BPS has been lowered since last month |
| 112 | `anl15_bps_gr_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of companies whose calendarized FY2 consensus BPS was raised since last month |
| 113 | `anl15_bps_gr_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 estimates lowered since last month aggregated at group level |
| 114 | `anl15_bps_gr_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level count of Fiscal Year 2 BPS (book value per share) estimates that were revised upward since last month |
| 115 | `anl15_bps_gr_fy3_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level number of companies for which the calendarized Fiscal Year 3 mean has been lowered since last month |
| 116 | `anl15_bps_gr_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 BPS consensus has been raised since last month at the group level |
| 117 | `anl15_bps_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates that were revised downward since last month, aggregated at the group level for Asia |
| 118 | `anl15_bps_gr_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of calendarized FY3 estimates raised since last month |
| 119 | `anl15_bps_ind_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted one-month percent change in 12-month forward BPS forecasts |
| 120 | `anl15_bps_ind_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward earnings forecasts, aggregated at industry level |
| 121 | `anl15_bps_ind_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward earnings forecasts aggregated at industry level |
| 122 | `anl15_bps_ind_12_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean book value per share(BPS) estimation within GICS industry grouping. |
| 123 | `anl15_bps_ind_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a lowered forward 12-month BPS consensus since last month at the industry level |
| 124 | `anl15_bps_ind_12_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level number of companies whose 12-month forward mean BPS was raised since last month |
| 125 | `anl15_bps_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 12-month period, aggregated at the industry level in Europe |
| 126 | `anl15_bps_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward estimates lowered since last month aggregated at the industry level |
| 127 | `anl15_bps_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro‑rated number of 12‑month forward estimates raised since last month at the industry level |
| 128 | `anl15_bps_ind_12_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted 12 month forward year over year growth of book value per share(BPS) estimation aggregated within GICS industry grouping. |
| 129 | `anl15_bps_ind_12_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month EPS aggregated at the industry level |
| 130 | `anl15_bps_ind_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 12-month forward earnings, aggregated at the industry level in AMR |
| 131 | `anl15_bps_ind_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of forward 12-month BPS forecasts aggregated at the industry level for Japan |
| 132 | `anl15_bps_ind_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for forward 12 months aggregated at industry level |
| 133 | `anl15_bps_ind_12_m_tr_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of 12 month trailing book value per share(BPS) aggregated within GICS industry grouping. |
| 134 | `anl15_bps_ind_18_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted one-month percent change in the 18-month forward BPS consensus, using a constant sample |
| 135 | `anl15_bps_ind_18_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted three‑month percent change in 18‑month forward BPS forecasts (constant sample) |
| 136 | `anl15_bps_ind_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 18-month forward earnings forecasts, using a constant sample, aggregated at industry level |
| 137 | `anl15_bps_ind_18_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a 18 month forward mean book value per share(BPS) estimation within GICS industry grouping. |
| 138 | `anl15_bps_ind_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a lowered 18-month forward BPS consensus since last month at the industry level |
| 139 | `anl15_bps_ind_18_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean book value per share(BPS) estimation has been raised from last month within GICS ind |
| 140 | `anl15_bps_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of estimates contributing to the 18-month forward BPS horizon |
| 141 | `anl15_bps_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates which have been lowered since last month within GICS industry grouping. |
| 142 | `anl15_bps_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates which have been raised since last month within GICS industry grouping. |
| 143 | `anl15_bps_ind_18_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted 18 month forward year over year growth of book value per share(BPS) estimation aggregated within GICS industry grouping. |
| 144 | `anl15_bps_ind_18_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average forward 18-month EPS aggregated at the industry level |
| 145 | `anl15_bps_ind_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18 month forward EPS estimation aggregated within GICS industry grouping. |
| 146 | `anl15_bps_ind_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Global industry-level weighted average standard deviation of 18-month forward BPS forecasts across constituent companies (as-of-date) |
| 147 | `anl15_bps_ind_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for forward 18 months aggregated at industry level |
| 148 | `anl15_bps_ind_cal_fy0_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Year-over-year growth for the current calendarized fiscal year aggregated at the industry level |
| 149 | `anl15_bps_ind_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted average Price/Earnings ratio for calendarized Fiscal Year 0 |
| 150 | `anl15_bps_ind_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 0 period (sum of EPS times shares), aggregated at the industry level in AMR |
| 151 | `anl15_bps_ind_cal_fy0_val` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of book value per share(BPS) estimation for the current calendarized fiscal year aggregated within GICS industry groupi |
| 152 | `anl15_bps_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in earnings forecasts for calendarized Fiscal Year 1 using a constant sample aggregated at industry level |
| 153 | `anl15_bps_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY1 consensus forecasts aggregated at the industry level (constant sample) |
| 154 | `anl15_bps_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted six-month percent change in calendarized FY1 BPS forecasts (constant sample) |
| 155 | `anl15_bps_ind_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates (coverage count) contributing to the FY1 BPS consensus at the industry level, globally |
| 156 | `anl15_bps_ind_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of estimates for calendarized Fiscal Year 1, aggregated at the industry level in AMR |
| 157 | `anl15_bps_ind_cal_fy1_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth for calendarized Fiscal Year 1 aggregated at industry level |
| 158 | `anl15_bps_ind_cal_fy1_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average consensus BPS for calendarized Fiscal Year 1 at the industry level in the AMR region |
| 159 | `anl15_bps_ind_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 1 aggregated at industry level |
| 160 | `anl15_bps_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 1, aggregated at the industry level in AMR |
| 161 | `anl15_bps_ind_cal_fy1_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total of book value per share(BPS) estimation for the calendarized one fiscal year aggregated within GICS industry grouping. |
| 162 | `anl15_bps_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY2 consensus forecasts aggregated at the industry level (constant sample) |
| 163 | `anl15_bps_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in forecasts for calendarized Fiscal Year 2 using a constant sample aggregated at the industry level |
| 164 | `anl15_bps_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted six-month percent change in earnings forecasts for calendarized Fiscal Year 2 (constant sample) |
| 165 | `anl15_bps_ind_cal_fy2_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized two fiscal year book value per share(BPS) estimation within GICS industry grouping. |
| 166 | `anl15_bps_ind_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the calendarized Fiscal Year 2 BPS period, aggregated at industry level |
| 167 | `anl15_bps_ind_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 2 aggregated at industry level |
| 168 | `anl15_bps_ind_cal_fy2_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for the calendarized Fiscal Year 2 period, aggregated at the industry level for Asia |
| 169 | `anl15_bps_ind_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 2, aggregated at the industry level in Europe |
| 170 | `anl15_bps_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation (dispersion) of calendarized FY2 BPS forecasts, aggregated at the industry level for the Americas |
| 171 | `anl15_bps_ind_cal_fy2_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total of book value per share(BPS) estimation for the calendarized two fiscal year aggregated within GICS industry grouping. |
| 172 | `anl15_bps_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted one-month percent change in calendarized FY3 BPS consensus, using a constant sample |
| 173 | `anl15_bps_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY3 BPS forecasts, using a constant sample, at the industry level in the AMR region |
| 174 | `anl15_bps_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted six month percent change of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GICS  |
| 175 | `anl15_bps_ind_cal_fy3_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized three fiscal year book value per share(BPS) estimation within GICS industry grouping. |
| 176 | `anl15_bps_ind_cal_fy3_ests` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total number of calendarized three fiscal year book value per share(BPS) estimation within GICS industry grouping. |
| 177 | `anl15_bps_ind_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GICS ind |
| 178 | `anl15_bps_ind_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average BPS for calendarized Fiscal Year 3, aggregated at the industry level |
| 179 | `anl15_bps_ind_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted average Price/Earnings ratio for calendarized Fiscal Year 3 |
| 180 | `anl15_bps_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted average standard deviation of consensus BPS forecasts for calendarized Fiscal Year 3 |
| 181 | `anl15_bps_ind_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for calendarized Fiscal Year 3 aggregated at industry level |
| 182 | `anl15_bps_ind_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which book value per share(BPS) estimation for the calendarized one fiscal year has been lowered from last month |
| 183 | `anl15_bps_ind_fy1_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which book value per share(BPS) estimation for the calendarized one fiscal year has been raised from last month  |
| 184 | `anl15_bps_ind_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates lowered since last month aggregated at industry level |
| 185 | `anl15_bps_ind_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates raised since last month aggregated at industry level |
| 186 | `anl15_bps_ind_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of companies whose calendarized FY2 consensus BPS was lowered since last month |
| 187 | `anl15_bps_ind_fy2_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which calendarized Fiscal Year 2 mean has been raised from last month aggregated at industry level |
| 188 | `anl15_bps_ind_fy2_ests_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total number of book value per share(BPS) estimation for the calendarized two fiscal year which have been lowered since last month withi |
| 189 | `anl15_bps_ind_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of Fiscal Year 2 estimates raised since last month |
| 190 | `anl15_bps_ind_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose FY3 consensus BPS has been lowered since last month |
| 191 | `anl15_bps_ind_fy3_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level number of companies for which calendarized Fiscal Year 3 mean was raised since last month |
| 192 | `anl15_bps_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates lowered since last month, aggregated at the industry level in AMR |
| 193 | `anl15_bps_ind_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates raised since last month, aggregated at industry level |
| 194 | `anl15_bps_s_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted one-month percent change in 12-month forward BPS forecasts |
| 195 | `anl15_bps_s_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted three-month percent change in 12-month forward earnings forecasts |
| 196 | `anl15_bps_s_12_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted six month percent change of 12 month forward book value per share(BPS) estimation aggregated within GICS sector grouping. |
| 197 | `anl15_bps_s_12_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean book value per share(BPS) estimation within GICS sector grouping. |
| 198 | `anl15_bps_s_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with lowered 12-month forward consensus mean since last month aggregated at the sector level |
| 199 | `anl15_bps_s_12_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with forward 12-month mean BPS raised since last month, aggregated at the sector level |
| 200 | `anl15_bps_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 12-month BPS period, aggregated at the sector level in China |
| 201 | `anl15_bps_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level pro-rated number of 12-month forward estimates lowered since last month |
| 202 | `anl15_bps_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level pro-rated number of 12-month forward estimates raised since last month |
| 203 | `anl15_bps_s_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth in earnings aggregated at sector level |
| 204 | `anl15_bps_s_12_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average forward 12-month BPS |
| 205 | `anl15_bps_s_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 12-month forward earnings, aggregated at the sector level in AMR |
| 206 | `anl15_bps_s_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average standard deviation of 12-month forward BPS forecasts |
| 207 | `anl15_bps_s_12_m_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total of 12 month forward book value per share(BPS) estimation aggregated within GICS sector grouping. |
| 208 | `anl15_bps_s_12_m_tr_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of 12 month trailing book value per share(BPS) aggregated within GICS sector grouping. |
| 209 | `anl15_bps_s_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward earnings forecasts using a constant sample aggregated at sector level |
| 210 | `anl15_bps_s_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted three-month percent change in the 18-month forward earnings forecasts, using a constant sample |
| 211 | `anl15_bps_s_18_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted six‑month percent change in 18‑month forward BPS forecasts (constant sample) |
| 212 | `anl15_bps_s_18_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a 18 month forward mean book value per share(BPS) estimation within GICS sector grouping. |
| 213 | `anl15_bps_s_18_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level number of companies whose 18-month forward mean BPS was lowered since last month |
| 214 | `anl15_bps_s_18_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with raised 18-month forward mean EPS since last month, aggregated at the sector level in AMR |
| 215 | `anl15_bps_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates within GICS sector grouping. |
| 216 | `anl15_bps_s_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates which have been lowered since last month within GICS sector grouping. |
| 217 | `anl15_bps_s_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with positive revision for the 18-month forward period, aggregated at the sector level in AMR |
| 218 | `anl15_bps_s_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted forward 18-month growth in earnings, aggregated at the sector level for Asia |
| 219 | `anl15_bps_s_18_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average forward 18 months EPS aggregated at sector level |
| 220 | `anl15_bps_s_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted average Price/Earnings ratio based on 18‑month forward earnings |
| 221 | `anl15_bps_s_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward BPS forecasts, aggregated at the sector level for the Americas |
| 222 | `anl15_bps_s_18_m_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total of 18 month forward book value per share(BPS) estimation aggregated within GICS sector grouping. |
| 223 | `anl15_bps_s_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 0, aggregated at sector level |
| 224 | `anl15_bps_s_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted average Price/Earnings ratio for calendarized Fiscal Year 0 |
| 225 | `anl15_bps_s_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for calendarized Fiscal Year 0 (sum of EPS times shares), aggregated at the sector level for Asia |
| 226 | `anl15_bps_s_cal_fy0_val` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of book value per share(BPS) estimation for the current calendarized fiscal year aggregated within GICS sector grouping |
| 227 | `anl15_bps_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in earnings forecasts for calendarized Fiscal Year 1 using a constant sample aggregated at sector level |
| 228 | `anl15_bps_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in earnings forecasts for calendarized Fiscal Year 1 using a constant sample aggregated at sector level |
| 229 | `anl15_bps_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in earnings forecasts for calendarized Fiscal Year 1 using a constant sample aggregated at sector level |
| 230 | `anl15_bps_s_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates (coverage count) contributing to the FY1 BPS consensus at the sector level, globally |
| 231 | `anl15_bps_s_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of Fiscal Year 1 estimates aggregated at sector level |
| 232 | `anl15_bps_s_cal_fy1_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth for calendarized Fiscal Year 1 aggregated at sector level |
| 233 | `anl15_bps_s_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for the calendarized Fiscal Year 1 period, aggregated at the sector level in AMR |
| 234 | `anl15_bps_s_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 1 aggregated at sector level |
| 235 | `anl15_bps_s_cal_fy1_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 1 |
| 236 | `anl15_bps_s_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 1 period, aggregated at sector level |
| 237 | `anl15_bps_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | One month percent change for calendarized Fiscal Year 2 aggregated at sector level |
| 238 | `anl15_bps_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY2 BPS forecasts, using a constant sample, at the sector level in the AMR region |
| 239 | `anl15_bps_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in earnings forecasts for calendarized Fiscal Year 2, using a constant sample, aggregated at the sector le |
| 240 | `anl15_bps_s_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for calendarized Fiscal Year 2 book value per share at the sector level |
| 241 | `anl15_bps_s_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of individual analyst BPS estimates contributing to the calendarized FY2 consensus across sector constituents |
| 242 | `anl15_bps_s_cal_fy2_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth for calendarized Fiscal Year 2 aggregated at the sector level |
| 243 | `anl15_bps_s_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level weighted average consensus BPS forecast for calendarized Fiscal Year 2 |
| 244 | `anl15_bps_s_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 2, aggregated at sector level |
| 245 | `anl15_bps_s_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of forecasts for calendarized Fiscal Year 2 aggregated at the sector level |
| 246 | `anl15_bps_s_cal_fy2_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total of book value per share(BPS) estimation for the calendarized two fiscal year aggregated within GICS sector grouping. |
| 247 | `anl15_bps_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in earnings forecasts for calendarized Fiscal Year 3, using a constant sample, aggregated at sector level |
| 248 | `anl15_bps_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted three-month percent change in calendarized FY3 BPS forecasts, using a constant sample |
| 249 | `anl15_bps_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted six-month percent change in calendarized FY3 BPS forecasts (constant sample) |
| 250 | `anl15_bps_s_cal_fy3_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized three fiscal year book value per share(BPS) estimation within GICS sector grouping. |
| 251 | `anl15_bps_s_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 BPS estimates, aggregated at the sector level for the Americas |
| 252 | `anl15_bps_s_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GICS sec |
| 253 | `anl15_bps_s_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GICS sector grouping. |
| 254 | `anl15_bps_s_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 3 aggregated at sector level |
| 255 | `anl15_bps_s_cal_fy3_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GIC |
| 256 | `anl15_bps_s_cal_fy3_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The total of book value per share(BPS) estimation for the calendarized three fiscal year aggregated within GICS sector grouping. |
| 257 | `anl15_bps_s_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with calendarized Fiscal Year 1 mean lowered from last month aggregated at sector level |
| 258 | `anl15_bps_s_fy1_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which book value per share(BPS) estimation for the calendarized one fiscal year has been raised from last month  |
| 259 | `anl15_bps_s_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of earnings estimates lowered for Fiscal Year 1 since last month |
| 260 | `anl15_bps_s_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates raised since last month aggregated at sector level |
| 261 | `anl15_bps_s_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose FY2 consensus BPS has been lowered since last month |
| 262 | `anl15_bps_s_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose calendarized FY2 BPS consensus increased versus last month |
| 263 | `anl15_bps_s_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of fiscal year 2 estimates lowered since last month |
| 264 | `anl15_bps_s_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 BPS estimates raised since last month, aggregated at the sector level |
| 265 | `anl15_bps_s_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean estimate has been lowered since last month, aggregated at the sector level |
| 266 | `anl15_bps_s_fy3_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which book value per share(BPS) estimation for the calendarized three fiscal year has been raised from last mont |
| 267 | `anl15_bps_s_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of calendarized Fiscal Year 3 estimates lowered since last month |
| 268 | `anl15_bps_s_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates that have been raised since last month at the sector level |
| 269 | `anl15_cps_gr_12_m_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in 12-month forward CPS forecasts |
| 270 | `anl15_cps_gr_12_m_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted three-month percent change in 12-month forward CPS forecasts |
| 271 | `anl15_cps_gr_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in forward 12-month cash flow per share forecasts |
| 272 | `anl15_cps_gr_12_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level consensus for the trailing 12-month forward period |
| 273 | `anl15_cps_gr_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group with the 12‑month forward CPS consensus mean lowered since last month |
| 274 | `anl15_cps_gr_12_m_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level number of companies with raised 12-month forward mean CPS since last month |
| 275 | `anl15_cps_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of analyst estimates contributing to the 12-month forward CPS (pro-rated) |
| 276 | `anl15_cps_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level pro-rated number of forward 12-month cash flow per share estimates lowered since last month |
| 277 | `anl15_cps_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level pro-rated number of 12-month forward estimates raised since last month |
| 278 | `anl15_cps_gr_12_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted 12-month forward year-over-year growth in CPS |
| 279 | `anl15_cps_gr_12_m_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average forward 12 months CPS at the group level |
| 280 | `anl15_cps_gr_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 12-month forward EPS estimation aggregated within GICS group grouping. |
| 281 | `anl15_cps_gr_12_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward CPS forecasts at the group level |
| 282 | `anl15_cps_gr_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward cash flow per share (CPS) estimation aggregated within GICS group grouping. |
| 283 | `anl15_cps_gr_12_m_tr_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12 months CPS aggregated at the group level (Global) |
| 284 | `anl15_cps_gr_18_m_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in the 18-month forward CPS forecasts (constant sample) at the group level |
| 285 | `anl15_cps_gr_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted three-month percent change in 18-month forward cash flow per share forecasts, using a constant sample |
| 286 | `anl15_cps_gr_18_m_6m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 18-month forward CPS forecasts at the group level, using a constant sample |
| 287 | `anl15_cps_gr_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of CPS estimates (coverage) for the 18-month forward horizon at the group level for the global universe |
| 288 | `anl15_cps_gr_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with the 18-month forward mean CPS estimate lowered since last month at the group level for the global universe |
| 289 | `anl15_cps_gr_18_m_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies with raised 18‑month forward mean CPS since last month, aggregated at the group level |
| 290 | `anl15_cps_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of estimates for the trailing 18-month period |
| 291 | `anl15_cps_gr_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with negative revision over the trailing 18-month period, aggregated at the group level |
| 292 | `anl15_cps_gr_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of 18-month forward cash flow per share estimates with positive revisions since last month |
| 293 | `anl15_cps_gr_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18‑month forward growth in cash flow per share at the industry group level |
| 294 | `anl15_cps_gr_18_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average 18-month forward cash flow per share at the group level in China |
| 295 | `anl15_cps_gr_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18-month forward EPS estimation aggregated within GICS group grouping. |
| 296 | `anl15_cps_gr_18_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward CPS forecasts, aggregated at the group level in China |
| 297 | `anl15_cps_gr_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward cash flow per share (CPS) estimation aggregated within GICS group grouping. |
| 298 | `anl15_cps_gr_cal_fy0_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year growth in CPS for calendarized Fiscal Year 0 (current year), aggregated at the group level |
| 299 | `anl15_cps_gr_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average price to earnings ratio for calendarized Fiscal Year 0 |
| 300 | `anl15_cps_gr_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share(CPS) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 301 | `anl15_cps_gr_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of cash flow per share (CPS) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 302 | `anl15_cps_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in calendarized Fiscal Year 1 CPS forecasts, using a constant sample |
| 303 | `anl15_cps_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Three-month weighted percent change in calendarized FY1 consensus CPS, aggregated at the group level in China |
| 304 | `anl15_cps_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in calendarized FY1 cash flow per share forecasts, using a constant sample |
| 305 | `anl15_cps_gr_cal_fy1_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 1 fiscal year cash flow per share (CPS) estimation within GICS group grouping. |
| 306 | `anl15_cps_gr_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level total number of analyst CPS estimates for calendarized Fiscal Year 1 in Asia |
| 307 | `anl15_cps_gr_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of cash flow per share (CPS) estimation for the calendarized 1-fiscal-year aggregated within GICS group g |
| 308 | `anl15_cps_gr_cal_fy1_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of cash flow per share (CPS) estimation for the calendarized 1 fiscal year aggregated within GICS group grouping. |
| 309 | `anl15_cps_gr_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings (P/E) ratio for calendarized Fiscal Year 1 at the group level |
| 310 | `anl15_cps_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of cash flow per share (CPS) estimation for the calendarized 1 fiscal year aggregated within GICS gr |
| 311 | `anl15_cps_gr_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 1 fiscal year aggregated within GICS group grouping. |
| 312 | `anl15_cps_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in calendarized FY2 cash flow per share forecasts, using a constant sample |
| 313 | `anl15_cps_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 2 CPS consensus at the group level, using a constant sample |
| 314 | `anl15_cps_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in calendarized Fiscal Year 2 CPS forecasts using a constant sample |
| 315 | `anl15_cps_gr_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal year cash flow per share (CPS) estimation within GICS group grouping. |
| 316 | `anl15_cps_gr_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of estimates contributing to the calendarized FY2 CPS consensus |
| 317 | `anl15_cps_gr_cal_fy2_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year growth in CPS for calendarized Fiscal Year 2, aggregated at the group level |
| 318 | `anl15_cps_gr_cal_fy2_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average CPS for calendarized FY2 at the group level |
| 319 | `anl15_cps_gr_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings (P/E) ratio for the calendarized Fiscal Year 2 period at the group level |
| 320 | `anl15_cps_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY2 CPS forecasts at the group level |
| 321 | `anl15_cps_gr_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 2 fiscal years aggregated within GICS group grouping. |
| 322 | `anl15_cps_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 3 CPS forecasts (constant sample) at the group level |
| 323 | `anl15_cps_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted three-month percent change in calendarized Fiscal Year 3 CPS forecasts, using a constant sample |
| 324 | `anl15_cps_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in earnings forecasts for calendarized Fiscal Year 3 (constant sample) |
| 325 | `anl15_cps_gr_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level consensus estimate for calendarized Fiscal Year 3 CPS |
| 326 | `anl15_cps_gr_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst CPS estimates for calendarized Fiscal Year 3 at the group level |
| 327 | `anl15_cps_gr_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of cash flow per share (CPS) estimation for the calendarized 3 fiscal years aggregated within GICS group  |
| 328 | `anl15_cps_gr_cal_fy3_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average CPS for calendarized Fiscal Year 3 at the group level |
| 329 | `anl15_cps_gr_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 3 fiscal years aggregated within GICS group grouping. |
| 330 | `anl15_cps_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of cash flow per share (CPS) estimation for the calendarized 3 fiscal years aggregated within GICS g |
| 331 | `anl15_cps_gr_cal_fy3_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level total for calendarized FY3 based on CPS, i.e., aggregate of per-company CPS×shares |
| 332 | `anl15_cps_gr_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose calendarized FY1 cash flow per share (CPS) consensus mean has been lowered since last month |
| 333 | `anl15_cps_gr_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which cash flow per share (CPS) estimation for the calendarized 1 fiscal year has been raised from last month wi |
| 334 | `anl15_cps_gr_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 CPS estimates lowered since last month at the group level |
| 335 | `anl15_cps_gr_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of FY1 cash flow per share estimates raised since last month |
| 336 | `anl15_cps_gr_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 consensus (mean) has been lowered since last month at the group level |
| 337 | `anl15_cps_gr_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group with calendarized Fiscal Year 2 consensus mean raised since last month in China |
| 338 | `anl15_cps_gr_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of Fiscal Year 2 estimates lowered since last month |
| 339 | `anl15_cps_gr_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of calendarized Fiscal Year 2 CPS estimates raised since last month |
| 340 | `anl15_cps_gr_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean consensus has been lowered since last month, aggregated at group level |
| 341 | `anl15_cps_gr_fy3_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean CPS has been raised since last month, aggregated at the group level |
| 342 | `anl15_cps_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates lowered since last month at the group level |
| 343 | `anl15_cps_gr_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 CPS estimates raised since last month, aggregated at group level |
| 344 | `anl15_cps_ind_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted one-month percent change in forward 12-month cash flow per share forecasts |
| 345 | `anl15_cps_ind_12_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in forward 12-month CPS consensus forecasts (constant-sample), aggregated at the industry level |
| 346 | `anl15_cps_ind_12_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward forecasts, aggregated at industry level, using a constant sample |
| 347 | `anl15_cps_ind_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean cash flow per share (CPS) estimation within GICS industry grouping. |
| 348 | `anl15_cps_ind_12_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Americas industry-level number of companies with lowered 12-month forward mean CPS since last month |
| 349 | `anl15_cps_ind_12_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the industry with raised 12-month forward mean CPS since last month |
| 350 | `anl15_cps_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the 12-month forward CPS at the industry level |
| 351 | `anl15_cps_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level pro-rated number of 12-month forward CFPS estimates that were lowered since last month in Europe |
| 352 | `anl15_cps_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level pro-rated number of 12‑month forward CPS estimates raised since last month |
| 353 | `anl15_cps_ind_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth in earnings, aggregated at the industry level |
| 354 | `anl15_cps_ind_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average 12-month forward cash flow per share at the industry level in China |
| 355 | `anl15_cps_ind_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 12-month forward EPS estimation aggregated within GICS industry grouping. |
| 356 | `anl15_cps_ind_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward CPS forecasts at the industry level |
| 357 | `anl15_cps_ind_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward cash flow per share (CPS) estimation aggregated within GICS industry grouping. |
| 358 | `anl15_cps_ind_12_m_tr_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12 months CPS aggregated at the industry level (Global) |
| 359 | `anl15_cps_ind_18_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in the 18-month forward CPS forecasts (constant sample) at the industry level |
| 360 | `anl15_cps_ind_18_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted three-month percent change in 18-month forward CPS forecasts using a constant sample |
| 361 | `anl15_cps_ind_18_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted six-month percent change in the 18-month forward CPS forecasts, using a constant sample |
| 362 | `anl15_cps_ind_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of CPS estimates (coverage) for the 18-month forward horizon at the industry level for the global universe |
| 363 | `anl15_cps_ind_18_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with lowered 18‑month forward mean CPS since last month, aggregated at the industry level |
| 364 | `anl15_cps_ind_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with the 18-month forward mean CPS estimate raised since last month at the industry level for the global universe |
| 365 | `anl15_cps_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for 18-month forward cash flow per share aggregated at the industry level in the USA |
| 366 | `anl15_cps_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with negative revision over the trailing 18 months at the industry level |
| 367 | `anl15_cps_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with positive revision over the trailing 18-month period, aggregated at the industry level |
| 368 | `anl15_cps_ind_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18‑month forward growth in cash flow per share at the industry level |
| 369 | `anl15_cps_ind_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average 18-month forward cash flow per share (CPS) consensus forecast at the industry level for the global universe |
| 370 | `anl15_cps_ind_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level price to earnings ratio based on 18-month forward earnings |
| 371 | `anl15_cps_ind_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward CPS forecasts at the industry level for the global universe |
| 372 | `anl15_cps_ind_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward cash flow per share (CPS) estimation aggregated within GICS industry grouping. |
| 373 | `anl15_cps_ind_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 0, aggregated at the industry level |
| 374 | `anl15_cps_ind_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 0, aggregated at industry level |
| 375 | `anl15_cps_ind_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share(CPS) estimation for the current calendarized fiscal year aggregated within GICS industry grouping. |
| 376 | `anl15_cps_ind_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of cash flow per share (CPS) estimation for the current calendarized fiscal year aggregated within GICS industry groupi |
| 377 | `anl15_cps_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY1 CPS forecasts at the industry level, using a constant sample |
| 378 | `anl15_cps_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted three-month percent change in earnings forecasts for calendarized Fiscal Year 1 (constant sample) |
| 379 | `anl15_cps_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 6-month percent change of cash flow per share (CPS) estimation for the calendarized 1 fiscal year aggregated within GICS indust |
| 380 | `anl15_cps_ind_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level consensus (mean) CPS estimate for calendarized FY1 |
| 381 | `anl15_cps_ind_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level total number of calendarized Fiscal Year 1 CPS estimates |
| 382 | `anl15_cps_ind_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted year-over-year growth in cash flow per share for calendarized Fiscal Year 1 |
| 383 | `anl15_cps_ind_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average CPS for calendarized Fiscal Year 1 at the industry level |
| 384 | `anl15_cps_ind_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 1, aggregated at industry level |
| 385 | `anl15_cps_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY1 CPS forecasts at the industry level |
| 386 | `anl15_cps_ind_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 1 fiscal year aggregated within GICS industry grouping. |
| 387 | `anl15_cps_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 2 forecasts, aggregated at industry level, using a constant sample |
| 388 | `anl15_cps_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 2 CPS forecasts (constant sample) at the industry level |
| 389 | `anl15_cps_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Six-month percent change in consensus cash-flow-per-share forecasts for calendarized Fiscal Year 2, aggregated at the industry level for the |
| 390 | `anl15_cps_ind_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level consensus estimate for calendarized Fiscal Year 2 CPS |
| 391 | `anl15_cps_ind_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of estimates for the calendarized FY2 cash flow per share period |
| 392 | `anl15_cps_ind_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of cash flow per share (CPS) estimation for the calendarized 2 fiscal years aggregated within GICS indust |
| 393 | `anl15_cps_ind_cal_fy2_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted average cash flow per share for calendarized Fiscal Year 2 |
| 394 | `anl15_cps_ind_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings (P/E) ratio for the calendarized Fiscal Year 2 period at the industry level |
| 395 | `anl15_cps_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of cash flow per share (CPS) estimation for the calendarized 2 fiscal years aggregated within GICS i |
| 396 | `anl15_cps_ind_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 2 fiscal years aggregated within GICS industry grouping. |
| 397 | `anl15_cps_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one‑month percent change in CPS forecasts for calendarized Fiscal Year 3 using a constant sample, aggregated at the industry level |
| 398 | `anl15_cps_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted three-month percent change in calendarized Fiscal Year 3 cash flow per share (CPS) forecasts for Asia, using a const |
| 399 | `anl15_cps_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized fiscal year 3 CPS consensus forecasts aggregated at the industry level (Global) |
| 400 | `anl15_cps_ind_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus (mean) CPS for calendarized FY3, aggregated at the industry level in China |
| 401 | `anl15_cps_ind_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized FY3 CPS at the industry level |
| 402 | `anl15_cps_ind_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted year-over-year growth in earnings for calendarized Fiscal Year 3 |
| 403 | `anl15_cps_ind_cal_fy3_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average consensus CPS estimate for calendarized Fiscal Year 3 at the industry level |
| 404 | `anl15_cps_ind_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 3 fiscal years aggregated within GICS industry groupi |
| 405 | `anl15_cps_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of cash flow per share (CPS) estimation for the calendarized three fiscal years aggregated within GI |
| 406 | `anl15_cps_ind_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 3 fiscal year aggregated within GICS industry grouping. |
| 407 | `anl15_cps_ind_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level count of companies whose calendarized FY1 consensus cash flow per share has been lowered since last month |
| 408 | `anl15_cps_ind_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which cash flow per share (CPS) estimation for the calendarized 1 fiscal year has been raised from last month wi |
| 409 | `anl15_cps_ind_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 CPS estimates lowered since last month at the industry level |
| 410 | `anl15_cps_ind_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of Fiscal Year 1 estimates raised since last month |
| 411 | `anl15_cps_ind_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 mean consensus has been lowered since last month, aggregated at industry level |
| 412 | `anl15_cps_ind_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of companies for which the calendarized Fiscal Year 2 mean (consensus) has been raised since last month |
| 413 | `anl15_cps_ind_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 CPS estimates lowered since last month at the industry level |
| 414 | `anl15_cps_ind_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of FY2 cash flow per share estimates raised since last month |
| 415 | `anl15_cps_ind_fy3_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean CPS has been lowered since last month, aggregated at the industry level |
| 416 | `anl15_cps_ind_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 consensus mean has been raised since last month, aggregated at the industry lev |
| 417 | `anl15_cps_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates lowered since last month, aggregated at industry level |
| 418 | `anl15_cps_ind_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates raised since last month, aggregated at industry level |
| 419 | `anl15_cps_s_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward CPS forecasts at the sector level |
| 420 | `anl15_cps_s_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 12-month forward earnings forecasts (constant sample), aggregated at the sector level |
| 421 | `anl15_cps_s_12_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted six-month percent change in 12-month forward CPS forecasts |
| 422 | `anl15_cps_s_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean cash flow per share (CPS) estimation within GICS sector grouping. |
| 423 | `anl15_cps_s_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with lowered 12-month forward CPS consensus since last month at the sector level |
| 424 | `anl15_cps_s_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of companies with raised forward 12-month consensus cash flow per share since last month |
| 425 | `anl15_cps_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of estimates for the trailing 12-month forward period |
| 426 | `anl15_cps_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level pro-rated number of 12-month forward CPS estimates lowered since last month |
| 427 | `anl15_cps_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level pro-rated number of 12-month forward CPS estimates raised since last month |
| 428 | `anl15_cps_s_12_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted 12-month forward year-over-year growth in CPS |
| 429 | `anl15_cps_s_12_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month CPS at the sector level |
| 430 | `anl15_cps_s_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted average price-to-earnings ratio based on 12-month forward earnings |
| 431 | `anl15_cps_s_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward cash flow per share forecasts at the sector level in China |
| 432 | `anl15_cps_s_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward cash flow per share (CPS) estimation aggregated within GICS sector grouping. |
| 433 | `anl15_cps_s_12_m_tr_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12 months CPS aggregated at the sector level (Global) |
| 434 | `anl15_cps_s_18_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward CPS forecasts at the sector level, using a constant sample |
| 435 | `anl15_cps_s_18_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three‑month percent change in the 18‑month forward CPS consensus using a constant sample at the sector level |
| 436 | `anl15_cps_s_18_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level weighted six-month percent change in the 18-month forward cash flow per share (CPS) consensus, using a constant sample |
| 437 | `anl15_cps_s_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of CPS estimates (coverage) for the 18-month forward horizon at the sector level for the global universe |
| 438 | `anl15_cps_s_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with the 18-month forward mean CPS estimate lowered since last month at the sector level for the global universe |
| 439 | `anl15_cps_s_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with the 18-month forward mean CPS estimate raised since last month at the sector level for the global universe |
| 440 | `anl15_cps_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 18-month forward period, aggregated at the sector level |
| 441 | `anl15_cps_s_18_m_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 442 | `anl15_cps_s_18_m_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 443 | `anl15_cps_s_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18‑month forward growth in cash flow per share at the sector level |
| 444 | `anl15_cps_s_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average 18-month forward cash flow per share (CPS) consensus forecast at the sector level for the global universe |
| 445 | `anl15_cps_s_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings (P/E) ratio based on 18‑month forward earnings at the sector level |
| 446 | `anl15_cps_s_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward CPS forecasts, aggregated at the sector level in China |
| 447 | `anl15_cps_s_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward cash flow per share (CPS) estimation aggregated within GICS sector grouping. |
| 448 | `anl15_cps_s_cal_fy0_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in CPS for calendarized Fiscal Year 0 at the sector level |
| 449 | `anl15_cps_s_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 0, aggregated at sector level |
| 450 | `anl15_cps_s_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the current calendarized fiscal year aggregated within GICS sector grouping. |
| 451 | `anl15_cps_s_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of cash flow per share (CPS) estimation for the current calendarized fiscal year aggregated within GICS sector grouping |
| 452 | `anl15_cps_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY1 CPS forecasts, using a constant sample, aggregated at the sector level for Europe |
| 453 | `anl15_cps_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted three-month percent change in calendarized Fiscal Year 1 CPS forecasts using a constant sample |
| 454 | `anl15_cps_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY1 CPS forecasts at the sector level, using a constant sample |
| 455 | `anl15_cps_s_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level consensus estimate for calendarized Fiscal Year 1 |
| 456 | `anl15_cps_s_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 CPS estimates at the sector level |
| 457 | `anl15_cps_s_cal_fy1_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in CPS for calendarized Fiscal Year 1 at the sector level |
| 458 | `anl15_cps_s_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average CPS for the calendarized Fiscal Year 1 period aggregated at the sector level |
| 459 | `anl15_cps_s_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 1 fiscal year aggregated within GICS sector grouping. |
| 460 | `anl15_cps_s_cal_fy1_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average standard deviation of CPS forecasts for calendarized Fiscal Year 1 |
| 461 | `anl15_cps_s_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 1 fiscal year aggregated within GICS sector grouping. |
| 462 | `anl15_cps_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | One-month percent change for calendarized Fiscal Year 2 forecasts at the sector level, aggregated globally |
| 463 | `anl15_cps_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three‑month percent change in calendarized FY2 CPS forecasts at the sector level, using a constant sample |
| 464 | `anl15_cps_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted six-month percent change in calendarized Fiscal Year 2 CPS forecasts using a constant sample |
| 465 | `anl15_cps_s_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal year cash flow per share (CPS) estimation within GICS sector grouping. |
| 466 | `anl15_cps_s_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of estimates for calendarized Fiscal Year 2 |
| 467 | `anl15_cps_s_cal_fy2_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted year-over-year growth in CPS for calendarized Fiscal Year 2 |
| 468 | `anl15_cps_s_cal_fy2_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted average cash flow per share for calendarized Fiscal Year 2 |
| 469 | `anl15_cps_s_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized FY2 at the sector level |
| 470 | `anl15_cps_s_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 2 |
| 471 | `anl15_cps_s_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 2 fiscal years aggregated within GICS sector grouping. |
| 472 | `anl15_cps_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted one-month percent change in calendarized Fiscal Year 3 CPS forecasts using a constant sample |
| 473 | `anl15_cps_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three‑month percent change in calendarized FY3 CPS forecasts at the sector level, using a constant sample |
| 474 | `anl15_cps_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted six-month percent change in calendarized Fiscal Year 3 CPS forecasts, using a constant sample |
| 475 | `anl15_cps_s_cal_fy3_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 3 fiscal year cash flow per share (CPS) estimation within GICS sector grouping. |
| 476 | `anl15_cps_s_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized Fiscal Year 3, aggregated at sector level |
| 477 | `anl15_cps_s_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year growth in CPS for calendarized Fiscal Year 3, aggregated at the sector level |
| 478 | `anl15_cps_s_cal_fy3_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of cash flow per share (CPS) estimation for the calendarized 3 fiscal years aggregated within GICS sector grouping. |
| 479 | `anl15_cps_s_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 3, aggregated at sector level |
| 480 | `anl15_cps_s_cal_fy3_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY3 CPS forecasts at the sector level |
| 481 | `anl15_cps_s_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of cash flow per share (CPS) estimation for the calendarized 3 fiscal years aggregated within GICS sector grouping. |
| 482 | `anl15_cps_s_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 1 CPS consensus was lowered since last month at the sector level |
| 483 | `anl15_cps_s_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which cash flow per share (CPS) estimation for the calendarized 1 fiscal year has been raised from last month wi |
| 484 | `anl15_cps_s_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 cash flow per share estimates revised downward since last month at the sector level |
| 485 | `anl15_cps_s_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 1 CPS estimates revised upward since last month at the sector level |
| 486 | `anl15_cps_s_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 consensus (mean) has been lowered since last month at the sector level |
| 487 | `anl15_cps_s_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level count of companies in Europe whose FY2 consensus mean CFPS was raised since last month |
| 488 | `anl15_cps_s_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 CPS estimates lowered since last month at the sector level |
| 489 | `anl15_cps_s_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 estimates raised since last month at the sector level |
| 490 | `anl15_cps_s_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of companies whose calendarized FY3 CPS consensus decreased since last month |
| 491 | `anl15_cps_s_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of companies with calendarized Fiscal Year 3 consensus raised since last month |
| 492 | `anl15_cps_s_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates lowered since last month, aggregated at sector level |
| 493 | `anl15_cps_s_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates raised since last month, aggregated at sector level |
| 494 | `anl15_dps_gr_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 1-month percent change of 12-month forward dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 495 | `anl15_dps_gr_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 3-month percent change of 12-month forward dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 496 | `anl15_dps_gr_12_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in the 12-month forward dividend per share (DPS) consensus for USA constituents |
| 497 | `anl15_dps_gr_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean dividend per share (DPS) estimation within GICS group grouping. |
| 498 | `anl15_dps_gr_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month DPS consensus decreased over the past month at the group level for USA |
| 499 | `anl15_dps_gr_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month DPS consensus increased over the past month at the group level for USA |
| 500 | `anl15_dps_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12-month forward pro-rated total number of estimates within GICS group grouping. |
| 501 | `anl15_dps_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward DPS estimates lowered since last month at the group level |
| 502 | `anl15_dps_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward estimates raised since last month, aggregated at group level |
| 503 | `anl15_dps_gr_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 12-month forward year-over-year growth of dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 504 | `anl15_dps_gr_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month dividends per share (DPS) at the group level for USA |
| 505 | `anl15_dps_gr_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price‑to‑earnings ratio based on 12‑month forward earnings aggregated at the group level |
| 506 | `anl15_dps_gr_12_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward EPS forecasts, aggregated at group level |
| 507 | `anl15_dps_gr_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 508 | `anl15_dps_gr_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12-month dividends per share (DPS) at the group level for USA |
| 509 | `anl15_dps_gr_18_m_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the group level |
| 510 | `anl15_dps_gr_18_m_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the group level |
| 511 | `anl15_dps_gr_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 6-month percent change of 18-month forward dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 512 | `anl15_dps_gr_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean dividend per share (DPS) estimation within GICS group grouping. |
| 513 | `anl15_dps_gr_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18-month forward mean dividend per share (DPS) estimation has been lowered from last month within GICS gro |
| 514 | `anl15_dps_gr_18_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18-month forward mean dividend per share (DPS) estimation has been raised from last month within GICS grou |
| 515 | `anl15_dps_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the forward 18-month period at the group level |
| 516 | `anl15_dps_gr_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of DPS estimates with negative revisions over the trailing 18‑month period, aggregated at the global group level |
| 517 | `anl15_dps_gr_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of DPS estimates with positive revisions over the trailing 18‑month period, aggregated at the global group level |
| 518 | `anl15_dps_gr_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 18-month forward year-over-year growth of dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 519 | `anl15_dps_gr_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level weighted average of the 18-month forward dividend per share (DPS) consensus for USA constituents |
| 520 | `anl15_dps_gr_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings (P/E) ratio based on 18-month forward EPS, aggregated at group level |
| 521 | `anl15_dps_gr_18_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted average standard deviation of 18-month forward DPS forecasts across USA constituents |
| 522 | `anl15_dps_gr_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward dividend per share (DPS) estimation aggregated within GICS group grouping. |
| 523 | `anl15_dps_gr_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of dividend per share (DPS) estimation for the current calendarized fiscal year aggregated within GICS gr |
| 524 | `anl15_dps_gr_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average price-to-earnings ratio for calendarized Fiscal Year 0 |
| 525 | `anl15_dps_gr_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 526 | `anl15_dps_gr_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of dividend per share (DPS) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 527 | `anl15_dps_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the group level in the USA |
| 528 | `anl15_dps_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the group level in the US |
| 529 | `anl15_dps_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the group level in the USA |
| 530 | `anl15_dps_gr_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level count of contributing analyst estimates (coverage) for the FY1 DPS consensus |
| 531 | `anl15_dps_gr_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of FY1 DPS analyst estimates aggregated at the group level in Europe |
| 532 | `anl15_dps_gr_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS group gr |
| 533 | `anl15_dps_gr_cal_fy1_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS group grouping. |
| 534 | `anl15_dps_gr_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings (P/E) ratio for calendarized Fiscal Year 1, aggregated at sector level |
| 535 | `anl15_dps_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS gro |
| 536 | `anl15_dps_gr_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS group grouping. |
| 537 | `anl15_dps_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | One-month percent change in the calendarized FY2 dividends per share (DPS) consensus at the group aggregation for USA, weighted using a cons |
| 538 | `anl15_dps_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 3-month percent change of dividend per share (DPS) estimation for the calendarized 2 fiscal years aggregated within GICS group  |
| 539 | `anl15_dps_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 6-month percent change of dividend per share (DPS) estimation for the calendarized 2 fiscal year aggregated within GICS group g |
| 540 | `anl15_dps_gr_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus DPS estimate for calendarized Fiscal Year 2 at the subindustry level |
| 541 | `anl15_dps_gr_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst DPS estimates for calendarized FY2 across USA companies in the industry group |
| 542 | `anl15_dps_gr_cal_fy2_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in DPS for calendarized FY2 across USA companies in the industry group |
| 543 | `anl15_dps_gr_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average DPS consensus for calendarized Fiscal Year 2 at the group level in the USA |
| 544 | `anl15_dps_gr_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 2 fiscal years aggregated within GICS group grouping. |
| 545 | `anl15_dps_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 2 fiscal years aggregated within GICS gr |
| 546 | `anl15_dps_gr_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 2 fiscal year aggregated within GICS group grouping. |
| 547 | `anl15_dps_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in calendarized Fiscal Year 3 dividend per share forecasts, using a constant sample |
| 548 | `anl15_dps_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized fiscal year 3 dividends per share (DPS) consensus at the group level for USA, using poin |
| 549 | `anl15_dps_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized fiscal year 3 dividends per share (DPS) consensus at the group level for USA, using point- |
| 550 | `anl15_dps_gr_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count for calendarized FY3 dividends per share (DPS) at the group aggregation for USA (number of companies with an FY3 DP |
| 551 | `anl15_dps_gr_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst DPS estimates for calendarized Fiscal Year 3 at the group level |
| 552 | `anl15_dps_gr_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS group g |
| 553 | `anl15_dps_gr_cal_fy3_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average calendarized FY3 dividends per share (DPS) consensus at the group aggregation for USA, computed point-in-time with as-of-da |
| 554 | `anl15_dps_gr_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 3 fiscal years aggregated within GICS group grouping. |
| 555 | `anl15_dps_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS gr |
| 556 | `anl15_dps_gr_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS group grouping. |
| 557 | `anl15_dps_gr_fy1_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which Dividend Per Share (DPS) estimation for the calendarized 1 fiscal year has been lowered from last month wi |
| 558 | `anl15_dps_gr_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which dividend per share (DPS) estimation for the calendarized 1 fiscal year has been raised from last month wit |
| 559 | `anl15_dps_gr_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY1 DPS estimates lowered since last month at the group level |
| 560 | `anl15_dps_gr_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of FY1 DPS estimates raised since last month in China |
| 561 | `anl15_dps_gr_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of USA companies in the industry group whose calendarized FY2 DPS consensus (mean) has been lowered since last month |
| 562 | `anl15_dps_gr_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose calendarized FY2 DPS consensus has been revised up since last month (breadth of upward revisions) in  |
| 563 | `anl15_dps_gr_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual FY2 DPS estimates that were revised downward since last month across USA companies in the industry group |
| 564 | `anl15_dps_gr_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual FY2 DPS estimates that were revised upward since last month across USA companies in the industry group |
| 565 | `anl15_dps_gr_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 dividends per share (DPS) consensus has been lowered since last month at the group aggregation fo |
| 566 | `anl15_dps_gr_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 dividends per share (DPS) consensus has been raised since last month at the group aggregation for |
| 567 | `anl15_dps_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 DPS estimates that were lowered since last month, aggregated at the group level in the Americas |
| 568 | `anl15_dps_gr_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of calendarized Fiscal Year 3 DPS estimates raised since last month |
| 569 | `anl15_dps_ind_12_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one‑month percent change in the 12‑month forward DPS consensus, using a constant sample, at the industry level |
| 570 | `anl15_dps_ind_12_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted three-month percent change in the 12-month forward dividend per share (DPS) consensus for USA constituents |
| 571 | `anl15_dps_ind_12_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted six-month percent change in the 12-month forward dividend per share (DPS) consensus for USA constituents |
| 572 | `anl15_dps_ind_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean dividend per share (DPS) estimation within GICS industry grouping. |
| 573 | `anl15_dps_ind_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month DPS consensus decreased over the past month at the industry level for USA |
| 574 | `anl15_dps_ind_12_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12-month forward mean dividend per share (DPS) estimation has been raised from last month within GICS indu |
| 575 | `anl15_dps_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 12-month period aggregated at the industry level |
| 576 | `anl15_dps_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward estimates lowered since last month, aggregated at industry level |
| 577 | `anl15_dps_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward DPS estimates raised since last month at the industry level in the Americas |
| 578 | `anl15_dps_ind_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 12-month forward year-over-year growth of dividend per share (DPS) estimation aggregated within GICS industry grouping. |
| 579 | `anl15_dps_ind_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month dividends per share (DPS) at the industry level for USA |
| 580 | `anl15_dps_ind_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average Price to Earnings ratio based on 12-month forward earnings, aggregated at industry level |
| 581 | `anl15_dps_ind_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 12-month forward dividend per share (DPS) estimation aggregated within GICS industry grouping. |
| 582 | `anl15_dps_ind_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward dividend per share (DPS) estimation aggregated within GICS industry grouping. |
| 583 | `anl15_dps_ind_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12-month dividends per share (DPS) at the industry level for USA |
| 584 | `anl15_dps_ind_18_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the industry level |
| 585 | `anl15_dps_ind_18_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the industry level |
| 586 | `anl15_dps_ind_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 6-month percent change of 18-month forward dividend per share (DPS) estimation aggregated within GICS industry grouping. |
| 587 | `anl15_dps_ind_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean dividend per share (DPS) estimation within GICS industry grouping. |
| 588 | `anl15_dps_ind_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18-month forward mean dividend per share (DPS) estimation has been lowered from last month within GICS ind |
| 589 | `anl15_dps_ind_18_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level number of companies whose 18-month forward mean DPS was raised since last month |
| 590 | `anl15_dps_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the forward 18-month period at the industry level |
| 591 | `anl15_dps_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of DPS estimates with negative revisions over the trailing 18‑month period, aggregated at the global industry level |
| 592 | `anl15_dps_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of 18-month forward DPS estimates raised (positive revisions) since last month at the industry level in the Americas |
| 593 | `anl15_dps_ind_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 18-month forward year-over-year growth of dividend per share (DPS) estimation aggregated within GICS industry grouping. |
| 594 | `anl15_dps_ind_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted average of the 18-month forward dividend per share (DPS) consensus for USA constituents |
| 595 | `anl15_dps_ind_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18‑month forward earnings aggregated at the industry level |
| 596 | `anl15_dps_ind_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted average standard deviation of 18-month forward DPS forecasts across USA constituents |
| 597 | `anl15_dps_ind_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward dividend per share (DPS) estimation aggregated within GICS industry grouping. |
| 598 | `anl15_dps_ind_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted year-over-year growth in dividends per share for calendarized Fiscal Year 0 |
| 599 | `anl15_dps_ind_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted average price-to-earnings ratio for calendarized Fiscal Year 0 |
| 600 | `anl15_dps_ind_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the current calendarized fiscal year aggregated within GICS industry grouping. |
| 601 | `anl15_dps_ind_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of dividend per share(DPS) estimation for the current calendarized fiscal year aggregated within GICS industry grouping |
| 602 | `anl15_dps_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the industry level in the U |
| 603 | `anl15_dps_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the industry level in the |
| 604 | `anl15_dps_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the industry level in the U |
| 605 | `anl15_dps_ind_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus DPS estimate for calendarized Fiscal Year 1 at the industry level |
| 606 | `anl15_dps_ind_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level total number of analyst DPS estimates for calendarized Fiscal Year 1 |
| 607 | `anl15_dps_ind_cal_fy1_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in DPS consensus for calendarized Fiscal Year 1 at the industry level in the USA |
| 608 | `anl15_dps_ind_cal_fy1_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS industry grouping. |
| 609 | `anl15_dps_ind_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings (P/E) ratio for calendarized Fiscal Year 1, aggregated at sector level |
| 610 | `anl15_dps_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS ind |
| 611 | `anl15_dps_ind_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 1 period, aggregated at industry level |
| 612 | `anl15_dps_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | One-month percent change in the calendarized FY2 dividends per share (DPS) consensus at the industry aggregation for USA, weighted using a c |
| 613 | `anl15_dps_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Three-month percent change in the calendarized FY2 dividends per share (DPS) consensus at the industry aggregation for USA, weighted using a |
| 614 | `anl15_dps_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Six-month percent change in the calendarized FY2 dividends per share (DPS) consensus at the industry aggregation for USA, weighted using a c |
| 615 | `anl15_dps_ind_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus DPS estimate for calendarized Fiscal Year 2 at the subindustry level |
| 616 | `anl15_dps_ind_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst DPS estimates for calendarized FY2 across USA companies in the industry |
| 617 | `anl15_dps_ind_cal_fy2_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in DPS for calendarized FY2 across USA companies in the industry |
| 618 | `anl15_dps_ind_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average DPS consensus for calendarized Fiscal Year 2 at the industry level in the USA |
| 619 | `anl15_dps_ind_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average Price/Earnings ratio for calendarized FY2 across USA companies in the industry |
| 620 | `anl15_dps_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 2 fiscal years aggregated within GICS in |
| 621 | `anl15_dps_ind_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 2 fiscal year aggregated within GICS industry grouping. |
| 622 | `anl15_dps_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY3 DPS forecasts (constant sample) at the industry level in the Americas |
| 623 | `anl15_dps_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized fiscal year 3 dividends per share (DPS) consensus at the industry level for USA, using p |
| 624 | `anl15_dps_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized fiscal year 3 dividends per share (DPS) consensus at the industry level for USA, using poi |
| 625 | `anl15_dps_ind_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count for calendarized FY3 dividends per share (DPS) at the industry aggregation for USA (number of companies with an FY3 |
| 626 | `anl15_dps_ind_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of dividend per share estimates for calendarized Fiscal Year 3 aggregated at industry level in China |
| 627 | `anl15_dps_ind_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in DPS for calendarized Fiscal Year 3 at the industry level in the Americas |
| 628 | `anl15_dps_ind_cal_fy3_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of dividend per share (DPS) estimation for the calendarized 3 fiscal year aggregated within GICS industry grouping. |
| 629 | `anl15_dps_ind_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings (P/E) ratio for calendarized Fiscal Year 3, aggregated at industry level |
| 630 | `anl15_dps_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS in |
| 631 | `anl15_dps_ind_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS industry grouping. |
| 632 | `anl15_dps_ind_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level number of companies whose calendarized FY1 mean DPS was lowered since last month |
| 633 | `anl15_dps_ind_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which dividend per share (DPS) estimation for the calendarized 1 fiscal year has been raised from last month wit |
| 634 | `anl15_dps_ind_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 1 DPS estimates lowered since last month aggregated at the industry level |
| 635 | `anl15_dps_ind_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY1 DPS analyst estimates revised upward over the past month, aggregated at the industry level in Europe |
| 636 | `anl15_dps_ind_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of USA companies in the industry whose calendarized FY2 DPS consensus (mean) has been lowered since last month |
| 637 | `anl15_dps_ind_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose calendarized FY2 DPS consensus has been revised up since last month (breadth of upward revisions)  |
| 638 | `anl15_dps_ind_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual FY2 DPS estimates that were revised downward since last month across USA companies in the industry |
| 639 | `anl15_dps_ind_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual FY2 DPS estimates that were revised upward since last month across USA companies in the industry |
| 640 | `anl15_dps_ind_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 dividends per share (DPS) consensus has been lowered since last month at the industry aggregation |
| 641 | `anl15_dps_ind_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 dividends per share (DPS) consensus has been raised since last month at the industry aggregation  |
| 642 | `anl15_dps_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of calendarized FY3 DPS estimates lowered since last month |
| 643 | `anl15_dps_ind_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of calendarized FY3 DPS estimates raised since last month in China |
| 644 | `anl15_dps_s_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted one-month percent change in 12-month forward dividend per share forecasts |
| 645 | `anl15_dps_s_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 3-month percent change of 12-month forward dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 646 | `anl15_dps_s_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 6-month percent change of 12-month forward dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 647 | `anl15_dps_s_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean dividend per share (DPS) estimation within GICS sector grouping. |
| 648 | `anl15_dps_s_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month DPS consensus decreased over the past month at the sector level for USA |
| 649 | `anl15_dps_s_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month DPS consensus increased over the past month at the sector level for USA |
| 650 | `anl15_dps_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of 12-month forward DPS estimates (pro-rated total) in China |
| 651 | `anl15_dps_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward number of DPS estimates lowered since last month at the sector level in the Americas |
| 652 | `anl15_dps_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of forward 12-month DPS estimates raised since last month, aggregated at the sector level in the Americas |
| 653 | `anl15_dps_s_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 12-month forward year-over-year growth of dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 654 | `anl15_dps_s_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month dividends per share (DPS) at the sector level for USA |
| 655 | `anl15_dps_s_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price‑to‑earnings ratio based on 12‑month forward earnings aggregated at the sector level |
| 656 | `anl15_dps_s_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 12-month forward dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 657 | `anl15_dps_s_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 658 | `anl15_dps_s_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12-month dividends per share (DPS) at the sector level for USA |
| 659 | `anl15_dps_s_18_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the sector level |
| 660 | `anl15_dps_s_18_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the sector level |
| 661 | `anl15_dps_s_18_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 18-month forward DPS forecasts, using a constant sample, aggregated at the sector level |
| 662 | `anl15_dps_s_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean dividend per share (DPS) estimation within GICS sector grouping. |
| 663 | `anl15_dps_s_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18-month forward mean dividend per share (DPS) estimation has been lowered from last month within GICS sec |
| 664 | `anl15_dps_s_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose 18-month forward DPS consensus mean increased since last month at the sector level in the Americas |
| 665 | `anl15_dps_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the 18-month forward DPS consensus, aggregated at the sector level |
| 666 | `anl15_dps_s_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of DPS estimates with negative revisions over the trailing 18‑month period, aggregated at the global sector level |
| 667 | `anl15_dps_s_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of DPS estimates with positive revisions over the trailing 18‑month period, aggregated at the global sector level |
| 668 | `anl15_dps_s_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 18-month forward year-over-year growth of dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 669 | `anl15_dps_s_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level weighted average of the 18-month forward dividend per share (DPS) consensus for USA constituents |
| 670 | `anl15_dps_s_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18-month forward EPS estimation aggregated within GICS sector grouping. |
| 671 | `anl15_dps_s_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average standard deviation of 18-month forward DPS forecasts across USA constituents |
| 672 | `anl15_dps_s_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward dividend per share (DPS) estimation aggregated within GICS sector grouping. |
| 673 | `anl15_dps_s_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of dividend per share (DPS) estimation for the current calendarized fiscal year aggregated within GICS se |
| 674 | `anl15_dps_s_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price-to-Earnings ratio for the current calendarized fiscal year aggregated at sector level |
| 675 | `anl15_dps_s_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 0 period (sum of EPS times shares), aggregated at sector level |
| 676 | `anl15_dps_s_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of dividend per share (DPS) estimation for the current calendarized fiscal year aggregated within GICS sector grouping. |
| 677 | `anl15_dps_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the sector level in the USA |
| 678 | `anl15_dps_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the sector level in the U |
| 679 | `anl15_dps_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in DPS consensus forecasts for calendarized Fiscal Year 1 (constant sample) at the sector level in the USA |
| 680 | `anl15_dps_s_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level count of contributing analyst estimates (coverage) for the FY1 DPS consensus |
| 681 | `anl15_dps_s_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of Fiscal Year 1 estimates, aggregated at sector level |
| 682 | `anl15_dps_s_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted year-over-year growth in dividend per share for calendarized Fiscal Year 1 |
| 683 | `anl15_dps_s_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average DPS for calendarized Fiscal Year 1 in Japan |
| 684 | `anl15_dps_s_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings (P/E) ratio for calendarized Fiscal Year 1, aggregated at sector level |
| 685 | `anl15_dps_s_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS sec |
| 686 | `anl15_dps_s_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 1 fiscal year aggregated within GICS sector grouping. |
| 687 | `anl15_dps_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY2 DPS consensus forecasts using a constant sample, aggregated at the sector level for US |
| 688 | `anl15_dps_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Three-month percent change in the calendarized FY2 dividends per share (DPS) consensus at the sector aggregation for USA, weighted using a c |
| 689 | `anl15_dps_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Six-month percent change in the calendarized FY2 dividends per share (DPS) consensus at the sector aggregation for USA, weighted using a con |
| 690 | `anl15_dps_s_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus DPS estimate for calendarized Fiscal Year 2 at the subindustry level |
| 691 | `anl15_dps_s_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst DPS estimates for calendarized FY2 across USA companies in the sector |
| 692 | `anl15_dps_s_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of dividend per share (DPS) estimation for the calendarized 2 fiscal years aggregated within GICS sector  |
| 693 | `anl15_dps_s_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average DPS consensus for calendarized Fiscal Year 2 at the sector level in the USA |
| 694 | `anl15_dps_s_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average Price/Earnings ratio for calendarized FY2 across USA companies in the sector |
| 695 | `anl15_dps_s_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 2 fiscal year aggregated within GICS sec |
| 696 | `anl15_dps_s_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 2 fiscal years aggregated within GICS sector grouping. |
| 697 | `anl15_dps_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY3 DPS forecasts (constant sample) at the sector level in the Americas |
| 698 | `anl15_dps_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in earnings forecasts for calendarized Fiscal Year 3, using a constant sample, aggregated at sector leve |
| 699 | `anl15_dps_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized fiscal year 3 dividends per share (DPS) consensus at the sector level for USA, using point |
| 700 | `anl15_dps_s_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count for calendarized FY3 dividends per share (DPS) at the sector aggregation for USA (number of companies with an FY3 D |
| 701 | `anl15_dps_s_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of analyst DPS estimates for calendarized Fiscal Year 3 |
| 702 | `anl15_dps_s_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted year-over-year growth in dividend per share for calendarized Fiscal Year 3 |
| 703 | `anl15_dps_s_cal_fy3_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average calendarized FY3 dividends per share (DPS) consensus at the sector aggregation for USA, computed point-in-time with as-of-d |
| 704 | `anl15_dps_s_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 3 fiscal years aggregated within GICS sector grouping |
| 705 | `anl15_dps_s_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS se |
| 706 | `anl15_dps_s_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of dividend per share (DPS) estimation for the calendarized 3 fiscal years aggregated within GICS sector grouping. |
| 707 | `anl15_dps_s_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which calendarized Fiscal Year 1 mean has been lowered since last month, aggregated at sector level |
| 708 | `anl15_dps_s_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which dividend per share (DPS) estimation for the calendarized 1 fiscal year has been raised from last month wit |
| 709 | `anl15_dps_s_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 DPS estimates lowered since last month at the sector level in the Americas |
| 710 | `anl15_dps_s_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of FY1 DPS estimates raised since last month in China |
| 711 | `anl15_dps_s_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of USA companies in the sector whose calendarized FY2 DPS consensus (mean) has been lowered since last month |
| 712 | `anl15_dps_s_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose calendarized FY2 DPS consensus has been revised up since last month (breadth of upward revisions) in |
| 713 | `anl15_dps_s_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual FY2 DPS estimates that were revised downward since last month across USA companies in the sector |
| 714 | `anl15_dps_s_fy2_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 715 | `anl15_dps_s_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 dividends per share (DPS) consensus has been lowered since last month at the sector aggregation f |
| 716 | `anl15_dps_s_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY3 dividends per share (DPS) consensus has been raised since last month at the sector aggregation fo |
| 717 | `anl15_dps_s_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 DPS estimates that were lowered since last month, aggregated at the sector level in the Americas |
| 718 | `anl15_dps_s_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of calendarized FY3 DPS estimates raised since last month |
| 719 | `anl15_ebg_gr_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward EPS forecasts, aggregated at the industry group level for Europe |
| 720 | `anl15_ebg_gr_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward EPS forecasts, aggregated at the industry group level for Europe |
| 721 | `anl15_ebg_gr_12_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward EPS forecasts, aggregated at the industry group level for Europe |
| 722 | `anl15_ebg_gr_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 723 | `anl15_ebg_gr_12_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12 month forward mean earnings per share before goodwill(EBG) estimation has been lowered from last month  |
| 724 | `anl15_ebg_gr_12_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12 month forward mean earnings per share before goodwill(EBG) estimation has been raised from last month w |
| 725 | `anl15_ebg_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates within GICS group grouping. |
| 726 | `anl15_ebg_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward earnings estimates that were lowered since last month, aggregated at the industry group level for Europ |
| 727 | `anl15_ebg_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates which have been raised since last month within GICS group grouping. |
| 728 | `anl15_ebg_gr_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 12 month forward year over year growth of earnings per share before goodwill(EBG) estimation aggregated within GICS group group |
| 729 | `anl15_ebg_gr_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12 months EPS (earnings per share) at the group level for Europe |
| 730 | `anl15_ebg_gr_12_m_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS group grouping with a 12 month forward mean price estimation. |
| 731 | `anl15_ebg_gr_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward EPS, aggregated at the industry group level for Europe |
| 732 | `anl15_ebg_gr_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 12 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS group  |
| 733 | `anl15_ebg_gr_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12 month forward earnings estimation aggregated within GICS group grouping. |
| 734 | `anl15_ebg_gr_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12 months EPS (earnings per share) at the group level for Europe |
| 735 | `anl15_ebg_gr_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the group level for Europe |
| 736 | `anl15_ebg_gr_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the group level for Europe |
| 737 | `anl15_ebg_gr_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the group level for Europe |
| 738 | `anl15_ebg_gr_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 18 month forward mean earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 739 | `anl15_ebg_gr_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean earnings per share before goodwill(EBG) estimation has been lowered from last month  |
| 740 | `anl15_ebg_gr_18_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean earnings per share before goodwill(EBG) estimation has been raised from last month w |
| 741 | `anl15_ebg_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates within GICS group grouping. |
| 742 | `anl15_ebg_gr_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates with negative revisions over the trailing 18 months, aggregated at the group level for Europe |
| 743 | `anl15_ebg_gr_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates with positive revisions over the trailing 18 months, aggregated at the group level for Europe |
| 744 | `anl15_ebg_gr_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18-month forward earnings growth, aggregated at the group level for Europe |
| 745 | `anl15_ebg_gr_18_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 18 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS group grouping. |
| 746 | `anl15_ebg_gr_18_m_mktcap` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies included in the aggregate with an 18-month forward mean, aggregated at the group level for Europe |
| 747 | `anl15_ebg_gr_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18-month forward earnings, aggregated at the group level for Europe |
| 748 | `anl15_ebg_gr_18_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 18 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS group  |
| 749 | `anl15_ebg_gr_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18 month forward earnings estimation aggregated within GICS group grouping. |
| 750 | `anl15_ebg_gr_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of earnings per share before goodwill(EBG) estimation for the current calendarized fiscal year aggregated |
| 751 | `anl15_ebg_gr_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the current calendarized fiscal ye |
| 752 | `anl15_ebg_gr_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 753 | `anl15_ebg_gr_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the current calendarized fiscal year aggregated within GICS g |
| 754 | `anl15_ebg_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the group leve |
| 755 | `anl15_ebg_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the group le |
| 756 | `anl15_ebg_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the group leve |
| 757 | `anl15_ebg_gr_cal_fy1_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized one fiscal year earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 758 | `anl15_ebg_gr_cal_fy1_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized one fiscal year earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 759 | `anl15_ebg_gr_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year growth in the EBG earnings measure for calendarized Fiscal Year 1, aggregated and weighted at the group level for Europe |
| 760 | `anl15_ebg_gr_cal_fy1_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year aggregated within GICS group |
| 761 | `anl15_ebg_gr_cal_fy1_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS group grouping with a calendarized one fiscal year mean price estim |
| 762 | `anl15_ebg_gr_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year a |
| 763 | `anl15_ebg_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year aggregate |
| 764 | `anl15_ebg_gr_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized one fiscal year aggregated within GICS group grouping. |
| 765 | `anl15_ebg_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted one month percent change of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated  |
| 766 | `anl15_ebg_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted three month percent change of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregate |
| 767 | `anl15_ebg_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted six month percent change of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated  |
| 768 | `anl15_ebg_gr_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized two fiscal year earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 769 | `anl15_ebg_gr_cal_fy2_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized two fiscal year earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 770 | `anl15_ebg_gr_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated wit |
| 771 | `anl15_ebg_gr_cal_fy2_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated within GICS group |
| 772 | `anl15_ebg_gr_cal_fy2_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS group grouping with a calendarized two fiscal year mean price estim |
| 773 | `anl15_ebg_gr_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 2, aggregated at the group level for Europe |
| 774 | `anl15_ebg_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregate |
| 775 | `anl15_ebg_gr_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized two fiscal year aggregated within GICS group grouping. |
| 776 | `anl15_ebg_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the group level for Europe |
| 777 | `anl15_ebg_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the group level for Europe |
| 778 | `anl15_ebg_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the group level for Europe |
| 779 | `anl15_ebg_gr_cal_fy3_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized three fiscal year earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 780 | `anl15_ebg_gr_cal_fy3_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized three fiscal year earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 781 | `anl15_ebg_gr_cal_fy3_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year earnings growth based on calendarized FY3 consensus, aggregated at the group level for Europe |
| 782 | `anl15_ebg_gr_cal_fy3_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year aggregated within GICS gro |
| 783 | `anl15_ebg_gr_cal_fy3_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS group grouping with a calendarized three fiscal year mean price est |
| 784 | `anl15_ebg_gr_cal_fy3_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average Price-to-Earnings ratio based on calendarized FY3 EPS consensus, aggregated at the group level for Europe |
| 785 | `anl15_ebg_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year aggrega |
| 786 | `anl15_ebg_gr_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized three fiscal year aggregated within GICS group grouping. |
| 787 | `anl15_ebg_gr_div_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which indicated annual dividend data is available within GICS group grouping. |
| 788 | `anl15_ebg_gr_divyld` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average dividend yield (based on Indicated Annual Dividend) for the group aggregate in Europe |
| 789 | `anl15_ebg_gr_fy1_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year has been lowered f |
| 790 | `anl15_ebg_gr_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year has been raised fr |
| 791 | `anl15_ebg_gr_fy1_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year which have been lowered since la |
| 792 | `anl15_ebg_gr_fy1_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year which have been raised since las |
| 793 | `anl15_ebg_gr_fy2_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year has been lowered f |
| 794 | `anl15_ebg_gr_fy2_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year has been raised fr |
| 795 | `anl15_ebg_gr_fy2_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year which have been lowered since la |
| 796 | `anl15_ebg_gr_fy2_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year which have been raised since las |
| 797 | `anl15_ebg_gr_fy3_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year has been lowered |
| 798 | `anl15_ebg_gr_fy3_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year has been raised  |
| 799 | `anl15_ebg_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 analyst estimates revised downward since the prior month, aggregated at the group level for Europe |
| 800 | `anl15_ebg_gr_fy3_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year which have been raised since l |
| 801 | `anl15_ebg_gr_hist_eps_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted annual EPS growth rate over the past five years (loglinear regression of last five years of annual EPS) for the group aggregate in  |
| 802 | `anl15_ebg_gr_ltg_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in long-term growth (LTG) forecasts at the group level for Europe |
| 803 | `anl15_ebg_gr_ltg_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in long-term growth (LTG) forecasts at the group level for Europe |
| 804 | `anl15_ebg_gr_ltg_6m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in long-term growth (LTG) forecasts at the group level for Europe |
| 805 | `anl15_ebg_gr_ltg_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a long term growth earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 806 | `anl15_ebg_gr_ltg_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies whose long-term growth (LTG) median has been lowered since last month at the group level within the Europe aggregation |
| 807 | `anl15_ebg_gr_ltg_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies whose long-term growth (LTG) median has been raised since last month at the group level within the Europe aggregation |
| 808 | `anl15_ebg_gr_ltg_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of long term growth earnings per share before goodwill(EBG) estimation within GICS group grouping. |
| 809 | `anl15_ebg_gr_ltg_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth (LTG) estimates that were revised downward since last month, aggregated at the group level for Europe |
| 810 | `anl15_ebg_gr_ltg_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual long-term growth (LTG) estimates raised since last month at the group level within the Europe aggregation |
| 811 | `anl15_ebg_gr_ltg_mdn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of long term growth earnings per share before goodwill(EBG) estimation aggregated within GICS group grouping. |
| 812 | `anl15_ebg_gr_ltg_mktcap` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies with long-term growth (LTG) forecasts at the group level for Europe |
| 813 | `anl15_ebg_gr_ltg_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of long term growth earnings per share before goodwill(EBG) estimation aggregated within GICS group  |
| 814 | `anl15_ebg_gr_prc` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Weighted average price per share for companies in the group aggregate in Europe |
| 815 | `anl15_ebg_ind_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward EPS forecasts, aggregated at the industry level for Europe |
| 816 | `anl15_ebg_ind_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward EPS forecasts, aggregated at the industry level for Europe |
| 817 | `anl15_ebg_ind_12_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward EPS forecasts, aggregated at the industry level for Europe |
| 818 | `anl15_ebg_ind_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 819 | `anl15_ebg_ind_12_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12 month forward mean earnings per share before goodwill(EBG) estimation has been lowered from last month  |
| 820 | `anl15_ebg_ind_12_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12 month forward mean earnings per share before goodwill(EBG) estimation has been raised from last month w |
| 821 | `anl15_ebg_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates within GICS industry grouping. |
| 822 | `anl15_ebg_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward earnings estimates that were lowered since last month, aggregated at the industry level for Europe |
| 823 | `anl15_ebg_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates which have been raised since last month within GICS industry grouping. |
| 824 | `anl15_ebg_ind_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 12 month forward year over year growth of earnings per share before goodwill(EBG) estimation aggregated within GICS industry gr |
| 825 | `anl15_ebg_ind_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12 months EPS (earnings per share) at the industry level for Europe |
| 826 | `anl15_ebg_ind_12_m_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS industry grouping with a 12 month forward mean price estimation. |
| 827 | `anl15_ebg_ind_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward EPS, aggregated at the industry level for Europe |
| 828 | `anl15_ebg_ind_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 12 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS indust |
| 829 | `anl15_ebg_ind_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12 month forward earnings estimation aggregated within GICS industry grouping. |
| 830 | `anl15_ebg_ind_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12 months EPS (earnings per share) at the industry level for Europe |
| 831 | `anl15_ebg_ind_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 832 | `anl15_ebg_ind_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the industry level for Europ |
| 833 | `anl15_ebg_ind_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 834 | `anl15_ebg_ind_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 18 month forward mean earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 835 | `anl15_ebg_ind_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean earnings per share before goodwill(EBG) estimation has been lowered from last month  |
| 836 | `anl15_ebg_ind_18_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean earnings per share before goodwill(EBG) estimation has been raised from last month w |
| 837 | `anl15_ebg_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates within GICS industry grouping. |
| 838 | `anl15_ebg_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates with negative revisions over the trailing 18 months, aggregated at the industry level for Europe |
| 839 | `anl15_ebg_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates with positive revisions over the trailing 18 months, aggregated at the industry level for Europe |
| 840 | `anl15_ebg_ind_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18-month forward earnings growth, aggregated at the industry level for Europe |
| 841 | `anl15_ebg_ind_18_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 18 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS industry grouping. |
| 842 | `anl15_ebg_ind_18_m_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies included in the aggregate with an 18-month forward mean, aggregated at the industry level for Europ |
| 843 | `anl15_ebg_ind_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18-month forward earnings, aggregated at the industry level for Europe |
| 844 | `anl15_ebg_ind_18_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 18 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS indust |
| 845 | `anl15_ebg_ind_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18 month forward earnings estimation aggregated within GICS industry grouping. |
| 846 | `anl15_ebg_ind_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of earnings per share before goodwill(EBG) estimation for the current calendarized fiscal year aggregated |
| 847 | `anl15_ebg_ind_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the current calendarized fiscal ye |
| 848 | `anl15_ebg_ind_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level total earnings for calendarized Fiscal Year 0 (sum of EPS times shares across constituents) |
| 849 | `anl15_ebg_ind_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the current calendarized fiscal year aggregated within GICS i |
| 850 | `anl15_ebg_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the industry l |
| 851 | `anl15_ebg_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the industry |
| 852 | `anl15_ebg_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the industry l |
| 853 | `anl15_ebg_ind_cal_fy1_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized one fiscal year earnings per share before goodwill(EBG) estimation within GICS industry grouping |
| 854 | `anl15_ebg_ind_cal_fy1_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized one fiscal year earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 855 | `anl15_ebg_ind_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year growth in the EBG earnings measure for calendarized Fiscal Year 1, aggregated and weighted at the industry level for Europe |
| 856 | `anl15_ebg_ind_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted average EPS for the calendarized Fiscal Year 1 period |
| 857 | `anl15_ebg_ind_cal_fy1_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS industry grouping with a calendarized one fiscal year mean price es |
| 858 | `anl15_ebg_ind_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year a |
| 859 | `anl15_ebg_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year aggregate |
| 860 | `anl15_ebg_ind_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized one fiscal year aggregated within GICS industry grouping. |
| 861 | `anl15_ebg_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percentage change in FY2 earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 862 | `anl15_ebg_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percentage change in FY2 earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 863 | `anl15_ebg_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percentage change in FY2 earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 864 | `anl15_ebg_ind_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized two fiscal year earnings per share before goodwill(EBG) estimation within GICS industry grouping |
| 865 | `anl15_ebg_ind_cal_fy2_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized two fiscal year earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 866 | `anl15_ebg_ind_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated wit |
| 867 | `anl15_ebg_ind_cal_fy2_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated within GICS indus |
| 868 | `anl15_ebg_ind_cal_fy2_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS industry grouping with a calendarized two fiscal year mean price es |
| 869 | `anl15_ebg_ind_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized Fiscal Year 2, aggregated at the industry level for Europe |
| 870 | `anl15_ebg_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregate |
| 871 | `anl15_ebg_ind_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized two fiscal year aggregated within GICS industry grouping. |
| 872 | `anl15_ebg_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 873 | `anl15_ebg_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 874 | `anl15_ebg_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the industry level for Europe |
| 875 | `anl15_ebg_ind_cal_fy3_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized three fiscal year earnings per share before goodwill(EBG) estimation within GICS industry groupi |
| 876 | `anl15_ebg_ind_cal_fy3_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized three fiscal year earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 877 | `anl15_ebg_ind_cal_fy3_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year earnings growth based on calendarized FY3 consensus, aggregated at the industry level for Europe |
| 878 | `anl15_ebg_ind_cal_fy3_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year aggregated within GICS ind |
| 879 | `anl15_ebg_ind_cal_fy3_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS industry grouping with a calendarized three fiscal year mean price  |
| 880 | `anl15_ebg_ind_cal_fy3_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average Price-to-Earnings ratio based on calendarized FY3 EPS consensus, aggregated at the industry level for Europe |
| 881 | `anl15_ebg_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year aggrega |
| 882 | `anl15_ebg_ind_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized three fiscal year aggregated within GICS industry grouping. |
| 883 | `anl15_ebg_ind_div_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which indicated annual dividend data is available within GICS industry grouping. |
| 884 | `anl15_ebg_ind_divyld` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average dividend yield (based on Indicated Annual Dividend) for the industry aggregate in Europe |
| 885 | `anl15_ebg_ind_fy1_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year has been lowered f |
| 886 | `anl15_ebg_ind_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year has been raised fr |
| 887 | `anl15_ebg_ind_fy1_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year which have been lowered since la |
| 888 | `anl15_ebg_ind_fy1_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year which have been raised since las |
| 889 | `anl15_ebg_ind_fy2_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year has been lowered f |
| 890 | `anl15_ebg_ind_fy2_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year has been raised fr |
| 891 | `anl15_ebg_ind_fy2_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year which have been lowered since la |
| 892 | `anl15_ebg_ind_fy2_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year which have been raised since las |
| 893 | `anl15_ebg_ind_fy3_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year has been lowered |
| 894 | `anl15_ebg_ind_fy3_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year has been raised  |
| 895 | `anl15_ebg_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 analyst estimates revised downward since the prior month, aggregated at the industry level for Europe |
| 896 | `anl15_ebg_ind_fy3_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year which have been raised since l |
| 897 | `anl15_ebg_ind_hist_eps_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted annual EPS growth rate over the past five years (loglinear regression of last five years of annual EPS) for the industry aggregate  |
| 898 | `anl15_ebg_ind_ltg_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in long-term growth (LTG) forecasts at the industry level for Europe |
| 899 | `anl15_ebg_ind_ltg_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in long-term growth (LTG) forecasts at the industry level for Europe |
| 900 | `anl15_ebg_ind_ltg_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in long-term growth (LTG) forecasts at the industry level for Europe |
| 901 | `anl15_ebg_ind_ltg_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a long term growth earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 902 | `anl15_ebg_ind_ltg_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies whose long-term growth (LTG) median has been lowered since last month at the industry level within the Europe aggregatio |
| 903 | `anl15_ebg_ind_ltg_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies whose long-term growth (LTG) median has been raised since last month at the industry level within the Europe aggregation |
| 904 | `anl15_ebg_ind_ltg_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of long term growth earnings per share before goodwill(EBG) estimation within GICS industry grouping. |
| 905 | `anl15_ebg_ind_ltg_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth (LTG) estimates that were revised downward since last month, aggregated at the industry level for Europe |
| 906 | `anl15_ebg_ind_ltg_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual long-term growth (LTG) estimates raised since last month at the industry level within the Europe aggregation |
| 907 | `anl15_ebg_ind_ltg_mdn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of long term growth earnings per share before goodwill(EBG) estimation aggregated within GICS industry grouping. |
| 908 | `anl15_ebg_ind_ltg_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies with long-term growth (LTG) forecasts at the industry level for Europe |
| 909 | `anl15_ebg_ind_ltg_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of long term growth earnings per share before goodwill(EBG) estimation aggregated within GICS indust |
| 910 | `anl15_ebg_ind_prc` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Weighted average price per share for companies in the industry aggregate in Europe |
| 911 | `anl15_ebg_s_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward EPS forecasts, aggregated at the sector level for Europe |
| 912 | `anl15_ebg_s_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward EPS forecasts, aggregated at the sector level for Europe |
| 913 | `anl15_ebg_s_12_m_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward EPS forecasts, aggregated at the sector level for Europe |
| 914 | `anl15_ebg_s_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12 month forward mean earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 915 | `anl15_ebg_s_12_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12 month forward mean earnings per share before goodwill(EBG) estimation has been lowered from last month  |
| 916 | `anl15_ebg_s_12_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 12 month forward mean earnings per share before goodwill(EBG) estimation has been raised from last month w |
| 917 | `anl15_ebg_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates within GICS sector grouping. |
| 918 | `anl15_ebg_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates which have been lowered since last month within GICS sector grouping. |
| 919 | `anl15_ebg_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12 month forward pro-rated total number of estimates which have been raised since last month within GICS sector grouping. |
| 920 | `anl15_ebg_s_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 12 month forward year over year growth of earnings per share before goodwill(EBG) estimation aggregated within GICS sector grou |
| 921 | `anl15_ebg_s_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12 months EPS (earnings per share) at the sector level for Europe |
| 922 | `anl15_ebg_s_12_m_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS sector grouping with a 12 month forward mean price estimation. |
| 923 | `anl15_ebg_s_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward EPS, aggregated at the sector level for Europe |
| 924 | `anl15_ebg_s_12_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 12 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS sector |
| 925 | `anl15_ebg_s_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12 month forward earnings estimation aggregated within GICS sector grouping. |
| 926 | `anl15_ebg_s_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12 months EPS (earnings per share) at the sector level for Europe |
| 927 | `anl15_ebg_s_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 928 | `anl15_ebg_s_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 929 | `anl15_ebg_s_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 930 | `anl15_ebg_s_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 18 month forward mean earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 931 | `anl15_ebg_s_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean earnings per share before goodwill(EBG) estimation has been lowered from last month  |
| 932 | `anl15_ebg_s_18_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which 18 month forward mean earnings per share before goodwill(EBG) estimation has been raised from last month w |
| 933 | `anl15_ebg_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates within GICS sector grouping. |
| 934 | `anl15_ebg_s_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates with negative revisions over the trailing 18 months, aggregated at the sector level for Europe |
| 935 | `anl15_ebg_s_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 18 month forward pro-rated total number of estimates which have been raised since last month within GICS sector grouping. |
| 936 | `anl15_ebg_s_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18-month forward earnings growth, aggregated at the sector level for Europe |
| 937 | `anl15_ebg_s_18_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 18 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS sector grouping. |
| 938 | `anl15_ebg_s_18_m_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies included in the aggregate with an 18-month forward mean, aggregated at the sector level for Europe |
| 939 | `anl15_ebg_s_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18-month forward earnings, aggregated at the sector level for Europe |
| 940 | `anl15_ebg_s_18_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of 18 month forward earnings per share before goodwill(EBG) estimation aggregated within GICS sector |
| 941 | `anl15_ebg_s_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18 month forward earnings estimation aggregated within GICS sector grouping. |
| 942 | `anl15_ebg_s_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of earnings per share before goodwill(EBG) estimation for the current calendarized fiscal year aggregated |
| 943 | `anl15_ebg_s_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the current calendarized fiscal ye |
| 944 | `anl15_ebg_s_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level total earnings for calendarized Fiscal Year 0 (sum of EPS times shares across constituents) |
| 945 | `anl15_ebg_s_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the current calendarized fiscal year aggregated within GICS s |
| 946 | `anl15_ebg_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the sector lev |
| 947 | `anl15_ebg_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the sector l |
| 948 | `anl15_ebg_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 1 EBG earnings forecasts using a constant sample, aggregated at the sector lev |
| 949 | `anl15_ebg_s_cal_fy1_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized one fiscal year earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 950 | `anl15_ebg_s_cal_fy1_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized one fiscal year earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 951 | `anl15_ebg_s_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted year over year growth of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year aggregated wit |
| 952 | `anl15_ebg_s_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average EPS for the calendarized Fiscal Year 1 period |
| 953 | `anl15_ebg_s_cal_fy1_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS sector grouping with a calendarized one fiscal year mean price esti |
| 954 | `anl15_ebg_s_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year a |
| 955 | `anl15_ebg_s_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year aggregate |
| 956 | `anl15_ebg_s_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized one fiscal year aggregated within GICS sector grouping. |
| 957 | `anl15_ebg_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percentage change in FY2 earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 958 | `anl15_ebg_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percentage change in FY2 earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 959 | `anl15_ebg_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percentage change in FY2 earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 960 | `anl15_ebg_s_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized two fiscal year earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 961 | `anl15_ebg_s_cal_fy2_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized two fiscal year earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 962 | `anl15_ebg_s_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year earnings growth for calendarized Fiscal Year 2, aggregated at the sector level for Europe |
| 963 | `anl15_ebg_s_cal_fy2_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregated within GICS secto |
| 964 | `anl15_ebg_s_cal_fy2_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS sector grouping with a calendarized two fiscal year mean price esti |
| 965 | `anl15_ebg_s_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year a |
| 966 | `anl15_ebg_s_cal_fy2_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year aggregate |
| 967 | `anl15_ebg_s_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized two fiscal year aggregated within GICS sector grouping. |
| 968 | `anl15_ebg_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 969 | `anl15_ebg_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 970 | `anl15_ebg_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 earnings forecasts (constant sample), aggregated at the sector level for Europe |
| 971 | `anl15_ebg_s_cal_fy3_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized three fiscal year earnings per share before goodwill(EBG) estimation within GICS sector grouping |
| 972 | `anl15_ebg_s_cal_fy3_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of calendarized three fiscal year earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 973 | `anl15_ebg_s_cal_fy3_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year earnings growth based on calendarized FY3 consensus, aggregated at the sector level for Europe |
| 974 | `anl15_ebg_s_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized Fiscal Year 3, aggregated at the sector level for Europe |
| 975 | `anl15_ebg_s_cal_fy3_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS sector grouping with a calendarized three fiscal year mean price es |
| 976 | `anl15_ebg_s_cal_fy3_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average Price-to-Earnings ratio based on calendarized FY3 EPS consensus, aggregated at the sector level for Europe |
| 977 | `anl15_ebg_s_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year aggrega |
| 978 | `anl15_ebg_s_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized three fiscal year aggregated within GICS sector grouping. |
| 979 | `anl15_ebg_s_div_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which indicated annual dividend data is available within GICS sector grouping. |
| 980 | `anl15_ebg_s_divyld` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average dividend yield (based on Indicated Annual Dividend) for the sector aggregate in Europe |
| 981 | `anl15_ebg_s_fy1_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year has been lowered f |
| 982 | `anl15_ebg_s_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year has been raised fr |
| 983 | `anl15_ebg_s_fy1_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year which have been lowered since la |
| 984 | `anl15_ebg_s_fy1_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized one fiscal year which have been raised since las |
| 985 | `anl15_ebg_s_fy2_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year has been lowered f |
| 986 | `anl15_ebg_s_fy2_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year has been raised fr |
| 987 | `anl15_ebg_s_fy2_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year which have been lowered since la |
| 988 | `anl15_ebg_s_fy2_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized two fiscal year which have been raised since las |
| 989 | `anl15_ebg_s_fy3_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year has been lowered |
| 990 | `anl15_ebg_s_fy3_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year has been raised  |
| 991 | `anl15_ebg_s_fy3_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year which have been lowered since  |
| 992 | `anl15_ebg_s_fy3_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of earnings per share before goodwill(EBG) estimation for the calendarized three fiscal year which have been raised since l |
| 993 | `anl15_ebg_s_hist_eps_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted annual EPS growth rate over the past five years (loglinear regression of last five years of annual EPS) for the sector aggregate in |
| 994 | `anl15_ebg_s_ltg_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in long-term growth (LTG) forecasts at the sector level for Europe |
| 995 | `anl15_ebg_s_ltg_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in long-term growth (LTG) forecasts at the sector level for Europe |
| 996 | `anl15_ebg_s_ltg_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in long-term growth (LTG) forecasts at the sector level for Europe |
| 997 | `anl15_ebg_s_ltg_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a long term growth earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 998 | `anl15_ebg_s_ltg_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies whose long-term growth (LTG) median has been lowered since last month at the sector level within the Europe aggregation |
| 999 | `anl15_ebg_s_ltg_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies whose long-term growth (LTG) median has been raised since last month at the sector level within the Europe aggregation |
| 1000 | `anl15_ebg_s_ltg_ests` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total number of long term growth earnings per share before goodwill(EBG) estimation within GICS sector grouping. |
| 1001 | `anl15_ebg_s_ltg_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual long-term growth (LTG) estimates lowered since last month at the sector level within the Europe aggregation |
| 1002 | `anl15_ebg_s_ltg_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual long-term growth (LTG) estimates raised since last month at the sector level within the Europe aggregation |
| 1003 | `anl15_ebg_s_ltg_mdn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of long term growth earnings per share before goodwill(EBG) estimation aggregated within GICS sector grouping. |
| 1004 | `anl15_ebg_s_ltg_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies with long-term growth (LTG) forecasts at the sector level for Europe |
| 1005 | `anl15_ebg_s_ltg_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of long term growth earnings per share before goodwill(EBG) estimation aggregated within GICS sector |
| 1006 | `anl15_ebg_s_prc` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Weighted average price per share for companies in the sector aggregate in Europe |
| 1007 | `anl15_ebt_gr_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward earnings forecasts at the group level |
| 1008 | `anl15_ebt_gr_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward EBT forecasts at the industry group level |
| 1009 | `anl15_ebt_gr_12_m_6m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted six-month percent change in 12-month forward EBT forecasts in the Americas |
| 1010 | `anl15_ebt_gr_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean earnings before tax (EBT) estimation within GICS group grouping. |
| 1011 | `anl15_ebt_gr_12_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of companies with lowered 12-month forward mean earnings since last month at the group level |
| 1012 | `anl15_ebt_gr_12_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of companies with raised 12-month forward mean earnings since last month at the group level |
| 1013 | `anl15_ebt_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of estimates for the forward 12-month period |
| 1014 | `anl15_ebt_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward EBT estimates lowered since last month at the group level |
| 1015 | `anl15_ebt_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level pro‑rated number of 12‑month forward individual estimates raised since last month |
| 1016 | `anl15_ebt_gr_12_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth in EBT, aggregated at the group level |
| 1017 | `anl15_ebt_gr_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 12-month forward earnings before tax (EBT) estimation aggregated within GICS group grouping. |
| 1018 | `anl15_ebt_gr_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 12-month forward EPS estimation aggregated within GICS group grouping. |
| 1019 | `anl15_ebt_gr_12_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward EBT forecasts aggregated at the group level |
| 1020 | `anl15_ebt_gr_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the forward 12-month period, aggregated at the group level for the Americas |
| 1021 | `anl15_ebt_gr_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 12-month trailing earnings before tax (EBT) aggregated within GICS group grouping. |
| 1022 | `anl15_ebt_gr_18_m_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward EBT forecasts using a constant sample at the group level |
| 1023 | `anl15_ebt_gr_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted three‑month percent change in 18‑month forward earnings forecasts, using a constant sample |
| 1024 | `anl15_ebt_gr_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecasts, using a constant sample, aggregated at group level |
| 1025 | `anl15_ebt_gr_18_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean earnings before tax (EBT) estimation within GICS group grouping. |
| 1026 | `anl15_ebt_gr_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Global industry group-level number of constituent companies whose 18-month forward mean EBT estimate was revised down since last month |
| 1027 | `anl15_ebt_gr_18_m_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies with raised 18-month forward mean EPS since last month, aggregated at the group level for the Americas |
| 1028 | `anl15_ebt_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 18-month period at the group level |
| 1029 | `anl15_ebt_gr_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates with negative revisions over the trailing 18-month period at the group level |
| 1030 | `anl15_ebt_gr_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with positive revision for the trailing 18-month period at the group level |
| 1031 | `anl15_ebt_gr_18_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted 18-month forward growth in EBT at the group level |
| 1032 | `anl15_ebt_gr_18_m_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted average 18-month forward EBT forecast |
| 1033 | `anl15_ebt_gr_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18-month forward EPS estimation aggregated within GICS group grouping. |
| 1034 | `anl15_ebt_gr_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Global industry group-level weighted average standard deviation (dispersion) of 18-month forward EBT forecasts |
| 1035 | `anl15_ebt_gr_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the forward 18-month period, aggregated at the group level for the Americas |
| 1036 | `anl15_ebt_gr_cal_fy0_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted year-over-year growth in EBT for the current calendarized fiscal year (FY0) |
| 1037 | `anl15_ebt_gr_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the current calendarized fiscal year aggregated within GICS group grou |
| 1038 | `anl15_ebt_gr_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings before tax (EBT) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 1039 | `anl15_ebt_gr_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of Earnings Before Tax (EBT) estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 1040 | `anl15_ebt_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in calendarized FY1 EBT forecasts, using a constant sample |
| 1041 | `anl15_ebt_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 1 earnings forecasts (constant sample) at the group level |
| 1042 | `anl15_ebt_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in earnings forecasts for calendarized Fiscal Year 1 (constant sample), aggregated at the group level for  |
| 1043 | `anl15_ebt_gr_cal_fy1_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 1 fiscal year earnings before tax (EBT) estimation within GICS group grouping. |
| 1044 | `anl15_ebt_gr_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level total number of analyst estimates for calendarized FY1 in the Americas |
| 1045 | `anl15_ebt_gr_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 1 at the group level |
| 1046 | `anl15_ebt_gr_cal_fy1_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average EBT forecast for calendarized Fiscal Year 1 at the group level in Japan |
| 1047 | `anl15_ebt_gr_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average price-to-earnings ratio for calendarized Fiscal Year 1 |
| 1048 | `anl15_ebt_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY1 EBT forecasts at group level |
| 1049 | `anl15_ebt_gr_cal_fy1_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total EBT for calendarized fiscal year 1 aggregated at the group level |
| 1050 | `anl15_ebt_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in FY2 EBT forecasts at the industry group level |
| 1051 | `anl15_ebt_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in earnings forecasts for calendarized Fiscal Year 2, using a constant sample, aggregated at group level |
| 1052 | `anl15_ebt_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted six‑month percent change in calendarized Fiscal Year 2 EBT forecasts (constant sample) at the group level in Japan |
| 1053 | `anl15_ebt_gr_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal year earnings before tax (EBT) estimation within GICS group grouping. |
| 1054 | `anl15_ebt_gr_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates for calendarized Fiscal Year 2 at the group level |
| 1055 | `anl15_ebt_gr_cal_fy2_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in EBT for calendarized Fiscal Year 2 at the group level |
| 1056 | `anl15_ebt_gr_cal_fy2_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average calendarized Fiscal Year 2 EBT forecast at the group level |
| 1057 | `anl15_ebt_gr_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average price-to-earnings ratio for calendarized Fiscal Year 2 |
| 1058 | `anl15_ebt_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized Fiscal Year 2 EBT forecasts at the group level |
| 1059 | `anl15_ebt_gr_cal_fy2_total` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total EBT for calendarized fiscal year 2 aggregated at the group level |
| 1060 | `anl15_ebt_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in earnings forecasts for calendarized Fiscal Year 3, using a constant sample, aggregated at group level |
| 1061 | `anl15_ebt_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 3 EBT forecasts using a constant sample at the group level |
| 1062 | `anl15_ebt_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted six‑month percent change in earnings forecasts for calendarized Fiscal Year 3, using a constant sample |
| 1063 | `anl15_ebt_gr_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count (number of estimates) for calendarized Fiscal Year 3 EBT at the group level |
| 1064 | `anl15_ebt_gr_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY3 EBT estimates aggregated at the group level |
| 1065 | `anl15_ebt_gr_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 3 at the group level |
| 1066 | `anl15_ebt_gr_cal_fy3_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average EBT for calendarized Fiscal Year 3 at group level |
| 1067 | `anl15_ebt_gr_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized three fiscal years aggregated within GICS group group |
| 1068 | `anl15_ebt_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of consensus Fiscal Year 3 EBT (earnings before tax) forecasts aggregated at the group level |
| 1069 | `anl15_ebt_gr_cal_fy3_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level total sum of calendarized FY3 EBT estimates (as-of-date aggregation) |
| 1070 | `anl15_ebt_gr_fy1_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings before tax (EBT) estimation for the calendarized 1 fiscal year has been lowered from last month w |
| 1071 | `anl15_ebt_gr_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings before tax (EBT) estimation for the calendarized 1 fiscal year has been raised from last month wi |
| 1072 | `anl15_ebt_gr_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY1 EBT estimates lowered since last month at the group level |
| 1073 | `anl15_ebt_gr_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 EBT estimates raised since last month at the group level |
| 1074 | `anl15_ebt_gr_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 EBT consensus mean was lowered since last month at the group level in Japan |
| 1075 | `anl15_ebt_gr_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized FY2 consensus EBT (mean) has been raised since last month at the group level |
| 1076 | `anl15_ebt_gr_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 2 EBT estimates lowered since last month at the group level |
| 1077 | `anl15_ebt_gr_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level number of Fiscal Year 2 individual estimates raised since last month |
| 1078 | `anl15_ebt_gr_fy3_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean has been lowered since last month, aggregated at group level |
| 1079 | `anl15_ebt_gr_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which calendarized Fiscal Year 3 EBT consensus has been raised since last month at the group level |
| 1080 | `anl15_ebt_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 EBT estimates that have been lowered since last month at the group level |
| 1081 | `anl15_ebt_gr_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 EBT estimates raised since last month at the group level |
| 1082 | `anl15_ebt_ind_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward EBT forecasts using a constant sample at the industry level |
| 1083 | `anl15_ebt_ind_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward EBT forecasts aggregated at the industry level |
| 1084 | `anl15_ebt_ind_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted 6-month percent change of 12-month forward earnings before tax (EBT) estimation aggregated within GICS industry grouping. |
| 1085 | `anl15_ebt_ind_12_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus for the trailing 12-month period at the industry level in China (EBT) |
| 1086 | `anl15_ebt_ind_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of companies whose 12-month forward consensus EBT was lowered since last month |
| 1087 | `anl15_ebt_ind_12_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with raised 12-month forward mean EBT since last month at the industry level |
| 1088 | `anl15_ebt_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst estimates for 12-month forward EBT at the industry level |
| 1089 | `anl15_ebt_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level pro-rated number of forward 12-month EBT estimates that were lowered since last month |
| 1090 | `anl15_ebt_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward EBT estimates raised since last month at the industry level in China |
| 1091 | `anl15_ebt_ind_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted 12‑month forward year‑over‑year growth in earnings |
| 1092 | `anl15_ebt_ind_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month earnings forecast at the industry level |
| 1093 | `anl15_ebt_ind_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 12-month forward EPS estimation aggregated within GICS industry grouping. |
| 1094 | `anl15_ebt_ind_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward EBT forecasts at the industry level |
| 1095 | `anl15_ebt_ind_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for forward 12 months at the industry level |
| 1096 | `anl15_ebt_ind_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 12-month trailing earnings before tax (EBT) aggregated within GICS industry grouping. |
| 1097 | `anl15_ebt_ind_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward earnings forecasts (constant sample) at the industry level |
| 1098 | `anl15_ebt_ind_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted three‑month percent change in 18‑month forward earnings forecasts, using a constant sample |
| 1099 | `anl15_ebt_ind_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecasts, using a constant sample, aggregated at industry level |
| 1100 | `anl15_ebt_ind_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count (number of estimates) for the 18-month forward EBT horizon at the industry level |
| 1101 | `anl15_ebt_ind_18_m_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of companies with lowered 18-month forward mean earnings since last month at the industry level |
| 1102 | `anl15_ebt_ind_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose 18‑month forward mean EBT consensus was raised since last month |
| 1103 | `anl15_ebt_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates for the trailing 18-month period at the industry level |
| 1104 | `anl15_ebt_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of forward 18‑month EBT estimates that were lowered since last month at the industry level in Japan |
| 1105 | `anl15_ebt_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with positive revision for the trailing 18-month period at the industry level |
| 1106 | `anl15_ebt_ind_18_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted 18-month forward growth in EBT at the industry level |
| 1107 | `anl15_ebt_ind_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Global industry-level weighted average 18-month forward earnings-before-tax (EBT) estimate (consensus) |
| 1108 | `anl15_ebt_ind_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18-month forward EPS estimation aggregated within GICS industry grouping. |
| 1109 | `anl15_ebt_ind_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward EBT forecasts at the industry level |
| 1110 | `anl15_ebt_ind_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the forward 18-month period, aggregated at industry level |
| 1111 | `anl15_ebt_ind_cal_fy0_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Year-over-year growth in calendarized FY0 (current year) EBT at the industry level |
| 1112 | `anl15_ebt_ind_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the current calendarized fiscal year aggregated within GICS industry g |
| 1113 | `anl15_ebt_ind_cal_fy0_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total calendarized FY0 EBT at the industry level |
| 1114 | `anl15_ebt_ind_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings before tax (EBT) estimation for the current calendarized fiscal year aggregated within GICS industry groupi |
| 1115 | `anl15_ebt_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted one-month percent change in calendarized FY1 EBT forecasts, using a constant sample, in the Americas |
| 1116 | `anl15_ebt_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 1 earnings forecasts (constant sample) at the industry level |
| 1117 | `anl15_ebt_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY1 EBT forecasts (constant sample) at the industry level |
| 1118 | `anl15_ebt_ind_cal_fy1_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 1 fiscal year earnings before tax (EBT) estimation within GICS industry grouping. |
| 1119 | `anl15_ebt_ind_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 EBT estimates at the industry level |
| 1120 | `anl15_ebt_ind_cal_fy1_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in EBT consensus forecasts for calendarized Fiscal Year 1, aggregated at the industry level globally |
| 1121 | `anl15_ebt_ind_cal_fy1_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level weighted average consensus EBT forecast for calendarized FY1 |
| 1122 | `anl15_ebt_ind_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted average price-to-earnings ratio for calendarized Fiscal Year 1 |
| 1123 | `anl15_ebt_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EBT forecasts for calendarized Fiscal Year 1 at the industry level in China |
| 1124 | `anl15_ebt_ind_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings before tax (EBT) estimation for the calendarized 1 fiscal year aggregated within GICS industry grouping. |
| 1125 | `anl15_ebt_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted one-month percent change in calendarized FY2 EBT forecasts, using a constant sample, in the Americas |
| 1126 | `anl15_ebt_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in earnings forecasts for calendarized Fiscal Year 2, using a constant sample, aggregated at industry le |
| 1127 | `anl15_ebt_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 2 EBT forecasts using a constant sample at the industry level |
| 1128 | `anl15_ebt_ind_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for calendarized FY2 EBT at the industry level |
| 1129 | `anl15_ebt_ind_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized Fiscal Year 2 EBT estimates aggregated at the industry level |
| 1130 | `anl15_ebt_ind_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 2, aggregated at the industry level for the Americas |
| 1131 | `anl15_ebt_ind_cal_fy2_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EBT for calendarized Fiscal Year 2 at industry level |
| 1132 | `anl15_ebt_ind_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 2 fiscal years aggregated within GICS industry groupi |
| 1133 | `anl15_ebt_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized Fiscal Year 2 EBT forecasts at the industry level |
| 1134 | `anl15_ebt_ind_cal_fy2_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total sum of calendarized Fiscal Year 2 EBT estimates aggregated at the industry level |
| 1135 | `anl15_ebt_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level weighted one‑month percent change in earnings forecasts for calendarized Fiscal Year 3, using a constant sample |
| 1136 | `anl15_ebt_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY3 EBT forecasts at industry level, using a constant sample |
| 1137 | `anl15_ebt_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted six-month percent change in calendarized FY3 EBT forecasts, using a constant sample, in the Americas |
| 1138 | `anl15_ebt_ind_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count (number of estimates) for calendarized Fiscal Year 3 EBT at the industry level |
| 1139 | `anl15_ebt_ind_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates for calendarized Fiscal Year 3 at the industry level |
| 1140 | `anl15_ebt_ind_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted year-over-year growth in EBT for calendarized FY3 |
| 1141 | `anl15_ebt_ind_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average calendarized FY3 EBT forecast (mean) at the industry level |
| 1142 | `anl15_ebt_ind_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 3 fiscal years aggregated within GICS industry groupi |
| 1143 | `anl15_ebt_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of earnings before tax (EBT) estimation for the calendarized 3 fiscal years aggregated within GICS i |
| 1144 | `anl15_ebt_ind_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for calendarized Fiscal Year 3, aggregated at industry level |
| 1145 | `anl15_ebt_ind_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with calendarized Fiscal Year 1 mean lowered since last month at the industry level |
| 1146 | `anl15_ebt_ind_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings before tax (EBT) estimation for the calendarized 1 fiscal year has been raised from last month wi |
| 1147 | `anl15_ebt_ind_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 EBT estimates lowered since last month at the industry level |
| 1148 | `anl15_ebt_ind_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EBT estimates for Fiscal Year 1 that were revised upward over the past month for the specified industry within the America |
| 1149 | `anl15_ebt_ind_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose calendarized Fiscal Year 2 EBT consensus mean has been revised downward since last month |
| 1150 | `anl15_ebt_ind_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 consensus mean has been raised since last month at the industry level in China  |
| 1151 | `anl15_ebt_ind_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 EBT estimates lowered since last month at the industry level |
| 1152 | `anl15_ebt_ind_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 2 EBT estimates raised since last month at the industry level |
| 1153 | `anl15_ebt_ind_fy3_cos_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings before tax (EBT) estimation for the calendarized 3 fiscal year has been lowered from last month w |
| 1154 | `anl15_ebt_ind_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized FY3 EBT consensus has been raised since last month at the industry level |
| 1155 | `anl15_ebt_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 EBT estimates that have been lowered since last month at the industry level |
| 1156 | `anl15_ebt_ind_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 EBT estimates that have been raised since last month at the industry level |
| 1157 | `anl15_ebt_s_12_m_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward EBT forecasts at the sector level |
| 1158 | `anl15_ebt_s_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward EBT forecasts aggregated at the sector level |
| 1159 | `anl15_ebt_s_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward earnings forecasts at the sector level |
| 1160 | `anl15_ebt_s_12_m_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean earnings before tax (EBT) estimation within GICS sector grouping. |
| 1161 | `anl15_ebt_s_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose 12-month forward consensus EBT (mean) was lowered since last month |
| 1162 | `anl15_ebt_s_12_m_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of companies in the sector with raised 12-month forward mean earnings since last month |
| 1163 | `anl15_ebt_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 12-month period at the sector level in China (EBT) |
| 1164 | `anl15_ebt_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward EBT estimates lowered since last month at the sector level in China |
| 1165 | `anl15_ebt_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of forward 12-month estimates that have been raised since last month, aggregated at the sector level for the Americas |
| 1166 | `anl15_ebt_s_12_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth in EBT at the sector level |
| 1167 | `anl15_ebt_s_12_m_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month earnings-before-tax (EBT) forecast at the sector level in China |
| 1168 | `anl15_ebt_s_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 12-month forward earnings at the sector level |
| 1169 | `anl15_ebt_s_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward EBT forecasts aggregated at the sector level |
| 1170 | `anl15_ebt_s_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward earnings before tax (EBT) estimation aggregated within GICS sector grouping. |
| 1171 | `anl15_ebt_s_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of 12-month trailing earnings before tax (EBT) aggregated within GICS sector grouping. |
| 1172 | `anl15_ebt_s_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward earnings forecasts (constant sample) at the sector level |
| 1173 | `anl15_ebt_s_18_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 18-month forward EBT forecasts using a constant sample at the sector level |
| 1174 | `anl15_ebt_s_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 18-month forward earnings forecasts (constant sample) at the sector level |
| 1175 | `anl15_ebt_s_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus coverage count (number of estimates) for the 18-month forward EBT horizon at the sector level |
| 1176 | `anl15_ebt_s_18_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies with lowered 18-month forward mean EBT since last month at the sector level |
| 1177 | `anl15_ebt_s_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector with 18-month forward EBT consensus raised since last month |
| 1178 | `anl15_ebt_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates for the trailing 18-month period at the sector level |
| 1179 | `anl15_ebt_s_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates with negative revisions over the trailing 18-month period at the sector level |
| 1180 | `anl15_ebt_s_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of EBT estimates with positive revisions over the trailing 18-month period at the sector level |
| 1181 | `anl15_ebt_s_18_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted 18-month forward growth in EBT at the sector level |
| 1182 | `anl15_ebt_s_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Global sector-level weighted average 18-month forward earnings-before-tax (EBT) estimate (consensus) |
| 1183 | `anl15_ebt_s_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18-month forward EPS estimation aggregated within GICS sector grouping. |
| 1184 | `anl15_ebt_s_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Global sector-level weighted average standard deviation (dispersion) of 18-month forward EBT forecasts |
| 1185 | `anl15_ebt_s_18_m_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level aggregate total EBT forecast over the next 18 months |
| 1186 | `anl15_ebt_s_cal_fy0_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Year-over-year growth rate in current calendarized Fiscal Year 0 EBT at the sector level |
| 1187 | `anl15_ebt_s_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the current calendarized fiscal year aggregated within GICS sector gro |
| 1188 | `anl15_ebt_s_cal_fy0_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total EBT for the current calendarized fiscal year (FY0) at the sector level |
| 1189 | `anl15_ebt_s_cal_fy0_val` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average of earnings before tax (EBT) estimation for the current calendarized fiscal year aggregated within GICS sector grouping |
| 1190 | `anl15_ebt_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY1 EBT forecasts at sector level, using a constant sample |
| 1191 | `anl15_ebt_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 1 EBT forecasts using a constant sample at the sector level |
| 1192 | `anl15_ebt_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 1 EBT forecasts at the sector level, using a constant sample |
| 1193 | `anl15_ebt_s_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus EBT estimate for calendarized Fiscal Year 1 at the sector level |
| 1194 | `anl15_ebt_s_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level total number of calendarized FY1 EBT estimates |
| 1195 | `anl15_ebt_s_cal_fy1_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted year-over-year growth rate of EBT for calendarized Fiscal Year 1 |
| 1196 | `anl15_ebt_s_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EBT forecast for calendarized Fiscal Year 1 at the sector level in China |
| 1197 | `anl15_ebt_s_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average forward price-to-earnings ratio based on FY1 forecasts at the sector level (calendarized) |
| 1198 | `anl15_ebt_s_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized Fiscal Year 1 Earnings Before Tax forecasts at the sector level |
| 1199 | `anl15_ebt_s_cal_fy1_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total calendarized Fiscal Year 1 EBT aggregated at the sector level |
| 1200 | `anl15_ebt_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY2 EBT forecasts at the sector level (constant sample) |
| 1201 | `anl15_ebt_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted three‑month percent change in earnings forecasts for calendarized Fiscal Year 2, using a constant sample |
| 1202 | `anl15_ebt_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 2 EBT forecasts using a constant sample at the sector level |
| 1203 | `anl15_ebt_s_cal_fy2_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal years earnings before tax (EBT) estimation within GICS sector grouping. |
| 1204 | `anl15_ebt_s_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY2 EBT estimates aggregated at the sector level |
| 1205 | `anl15_ebt_s_cal_fy2_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year growth in calendarized FY2 EBT, aggregated at the sector level |
| 1206 | `anl15_ebt_s_cal_fy2_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EBT for calendarized Fiscal Year 2 at sector level |
| 1207 | `anl15_ebt_s_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 2 fiscal year aggregated within GICS sector grouping. |
| 1208 | `anl15_ebt_s_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized Fiscal Year 2 EBT forecasts at the sector level |
| 1209 | `anl15_ebt_s_cal_fy2_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total EBT for the calendarized Fiscal Year 2 period at the sector level in Japan |
| 1210 | `anl15_ebt_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY3 EBT forecasts (constant sample) at the sector level |
| 1211 | `anl15_ebt_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized Fiscal Year 3 earnings forecasts (constant sample), aggregated at the sector level for t |
| 1212 | `anl15_ebt_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 EBT forecasts at the sector level (constant sample) |
| 1213 | `anl15_ebt_s_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus EBT estimate for calendarized Fiscal Year 3 at the sector level |
| 1214 | `anl15_ebt_s_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for calendarized FY3 EBT at the sector level |
| 1215 | `anl15_ebt_s_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year growth in calendarized FY3 EBT at the sector level |
| 1216 | `anl15_ebt_s_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average calendarized Fiscal Year 3 EBT forecast at the sector level |
| 1217 | `anl15_ebt_s_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on EPS estimation for the calendarized 3 fiscal years aggregated within GICS sector grouping |
| 1218 | `anl15_ebt_s_cal_fy3_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average standard deviation of calendarized Fiscal Year 3 EBT forecasts in China |
| 1219 | `anl15_ebt_s_cal_fy3_total` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total aggregated calendarized Fiscal Year 3 EBT across companies at the sector level |
| 1220 | `anl15_ebt_s_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 1 EBT consensus mean was lowered since last month at the sector level in Japan |
| 1221 | `anl15_ebt_s_fy1_cos_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which earnings before tax (EBT) estimation for the calendarized 1 fiscal year has been raised from last month wi |
| 1222 | `anl15_ebt_s_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 EBT estimates lowered since last month at the sector level |
| 1223 | `anl15_ebt_s_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of Fiscal Year 1 EBT estimates raised since last month |
| 1224 | `anl15_ebt_s_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose calendarized Fiscal Year 2 EBT consensus mean has been revised downward since last month |
| 1225 | `anl15_ebt_s_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 EBT consensus mean was raised since last month at the sector level in Japan |
| 1226 | `anl15_ebt_s_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 EBT estimates lowered since last month at the sector level in China |
| 1227 | `anl15_ebt_s_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 2 estimates raised since last month, aggregated at the sector level for the Americas |
| 1228 | `anl15_ebt_s_fy3_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean has been lowered since last month, aggregated at sector level |
| 1229 | `anl15_ebt_s_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of companies whose FY3 consensus EBT was raised since last month |
| 1230 | `anl15_ebt_s_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 EBT estimates that have been lowered since last month at the sector level |
| 1231 | `anl15_ebt_s_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 EBT estimates that have been raised since last month at the sector level |
| 1232 | `anl15_gr_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward earnings forecasts at the group level (constant sample) |
| 1233 | `anl15_gr_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward earnings forecasts for the group |
| 1234 | `anl15_gr_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward earnings forecasts for the group |
| 1235 | `anl15_gr_12_m_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean EPS estimation within GICS group grouping. |
| 1236 | `anl15_gr_12_m_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies in the group with the 12-month forward mean EPS lowered since last month |
| 1237 | `anl15_gr_12_m_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose 12-month forward mean EPS was raised since last month |
| 1238 | `anl15_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the group’s forward 12‑month period |
| 1239 | `anl15_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of forward 12-month EPS estimates that were lowered since last month for the group |
| 1240 | `anl15_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward estimates raised since last month at the group level |
| 1241 | `anl15_gr_12_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year EPS growth at the group level |
| 1242 | `anl15_gr_12_m_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average forward 12‑month EPS at the group level |
| 1243 | `anl15_gr_12_m_mktcap` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies in the group that have a 12-month forward EPS mean |
| 1244 | `anl15_gr_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted average price-to-earnings ratio based on 12-month forward EPS |
| 1245 | `anl15_gr_12_m_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward EPS forecasts at the group level |
| 1246 | `anl15_gr_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward earnings estimation aggregated within GICS group grouping. |
| 1247 | `anl15_gr_12_m_tr_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12-month EPS, aggregated at the group level |
| 1248 | `anl15_gr_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward earnings forecasts, using a constant sample, aggregated at the group level |
| 1249 | `anl15_gr_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the 18-month forward earnings forecasts at the group level, using a constant sample |
| 1250 | `anl15_gr_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six‑month percent change in the forward 18‑month earnings forecast, constant sample, at the group level |
| 1251 | `anl15_gr_18_m_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean EPS estimation within GICS group grouping. |
| 1252 | `anl15_gr_18_m_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies for which 18-month forward mean EPS estimation has been lowered from last month within GICS group grouping. |
| 1253 | `anl15_gr_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group that raised their 18‑month forward mean earnings estimate since last month |
| 1254 | `anl15_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for the 18-month forward period in the group |
| 1255 | `anl15_gr_18_m_ests_dn` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1256 | `anl15_gr_18_m_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1257 | `anl15_gr_18_m_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted 18-month forward year-over-year growth of EPS estimation aggregated within GICS group grouping. |
| 1258 | `anl15_gr_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level weighted average 18-month forward EPS consensus estimate |
| 1259 | `anl15_gr_18_m_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the industry group that have an 18-month forward mean forecast |
| 1260 | `anl15_gr_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18‑month forward earnings at the group level |
| 1261 | `anl15_gr_18_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18‑month forward earnings forecasts for the group |
| 1262 | `anl15_gr_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the forward 18 months for companies in the group |
| 1263 | `anl15_gr_cal_fy0_gro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted year-over-year growth of EPS estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 1264 | `anl15_gr_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized FY0 at the industry group level |
| 1265 | `anl15_gr_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 1266 | `anl15_gr_cal_fy0_val` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted average of EPS estimation for the current calendarized fiscal year aggregated within GICS group grouping. |
| 1267 | `anl15_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY1 earnings forecasts for the group, using a constant sample |
| 1268 | `anl15_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY1 earnings forecasts at the group level (constant sample) |
| 1269 | `anl15_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY1 earnings forecasts for the group, using a constant sample |
| 1270 | `anl15_gr_cal_fy1_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 1 fiscal year EPS estimation within GICS group grouping. |
| 1271 | `anl15_gr_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the calendarized Fiscal Year 1 period, aggregated at the group level |
| 1272 | `anl15_gr_cal_fy1_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 1 at the group level |
| 1273 | `anl15_gr_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized FY1 for the industry group |
| 1274 | `anl15_gr_cal_fy1_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS group grouping with a calendarized 1 fiscal year mean price estimat |
| 1275 | `anl15_gr_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on calendarized Fiscal Year 1 EPS at the group level |
| 1276 | `anl15_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 1, aggregated at the group level |
| 1277 | `anl15_gr_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized 1 fiscal year aggregated within GICS group grouping. |
| 1278 | `anl15_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY2 earnings forecasts at the group level (constant sample) |
| 1279 | `anl15_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the calendarized FY2 earnings forecast for the industry group, using a constant sample |
| 1280 | `anl15_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 2 earnings forecasts using a constant sample, aggregated at the group level |
| 1281 | `anl15_gr_cal_fy2_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal year EPS estimation within GICS group grouping. |
| 1282 | `anl15_gr_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized FY2 at the group level |
| 1283 | `anl15_gr_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year earnings growth for calendarized FY2 at the group level |
| 1284 | `anl15_gr_cal_fy2_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average EPS for the calendarized Fiscal Year 2 period, aggregated at the group level |
| 1285 | `anl15_gr_cal_fy2_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS group grouping with a calendarized 2 fiscal year mean price estimat |
| 1286 | `anl15_gr_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized FY2 at the industry group level |
| 1287 | `anl15_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 2 at the group level |
| 1288 | `anl15_gr_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 2 period for the group |
| 1289 | `anl15_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Group-level weighted one-month percent change in calendarized FY3 earnings forecasts using a constant sample |
| 1290 | `anl15_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY3 earnings forecasts at the group level (constant sample) |
| 1291 | `anl15_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 earnings forecasts for the group, using a constant sample |
| 1292 | `anl15_gr_cal_fy3_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 3 fiscal year EPS estimation within GICS group grouping. |
| 1293 | `anl15_gr_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the calendarized FY3 consensus for the industry group |
| 1294 | `anl15_gr_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year earnings growth for calendarized Fiscal Year 3 at the group level |
| 1295 | `anl15_gr_cal_fy3_mean` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized Fiscal Year 3 at the group level |
| 1296 | `anl15_gr_cal_fy3_mktcap` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies in the group with a calendarized Fiscal Year 3 mean estimate |
| 1297 | `anl15_gr_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average Price/Earnings ratio based on calendarized FY3 EPS at the group level |
| 1298 | `anl15_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of EPS estimation for the calendarized 3 fiscal year aggregated within GICS group grouping. |
| 1299 | `anl15_gr_cal_fy3_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total sum of calendarized Fiscal Year 3 earnings/estimates aggregated at the group level |
| 1300 | `anl15_gr_div_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which indicated annual dividend data is available within GICS group grouping. |
| 1301 | `anl15_gr_divyld` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average dividend yield aggregated within GICS group grouping. |
| 1302 | `anl15_gr_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose calendarized Fiscal Year 1 consensus mean was lowered since last month |
| 1303 | `anl15_gr_fy1_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies for which EPS estimation for the calendarized 1 fiscal year has been raised from last month within GICS group groupi |
| 1304 | `anl15_gr_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 earnings estimates lowered since last month, aggregated at the group level |
| 1305 | `anl15_gr_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates raised since last month at the group level |
| 1306 | `anl15_gr_fy2_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the industry group whose calendarized FY2 mean has been lowered since last month |
| 1307 | `anl15_gr_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose calendarized FY2 mean estimate was raised since last month |
| 1308 | `anl15_gr_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 analyst estimates lowered since last month in the group |
| 1309 | `anl15_gr_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY2 estimates raised since last month in the group |
| 1310 | `anl15_gr_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose calendarized Fiscal Year 3 consensus mean was lowered since last month |
| 1311 | `anl15_gr_fy3_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the industry group for which the calendarized FY3 mean has been raised since last month |
| 1312 | `anl15_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates lowered since last month at the group level |
| 1313 | `anl15_gr_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 3 estimates raised since last month at the group level |
| 1314 | `anl15_gr_hist_eps_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted annual EPS growth rate over the past five years for the group, from a loglinear regression of the last five years of annual EPS |
| 1315 | `anl15_gr_ltg_1m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in long-term growth forecasts for the group |
| 1316 | `anl15_gr_ltg_3m_chg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the long-term growth forecast at the group level |
| 1317 | `anl15_gr_ltg_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six‑month percent change in the long‑term growth (LTG) consensus for the group, using a constant sample |
| 1318 | `anl15_gr_ltg_cos` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The number of companies with a long-term growth EPS estimation within GICS group grouping. |
| 1319 | `anl15_gr_ltg_cos_dn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies in the group for which the long-term growth (LTG) median was lowered since last month |
| 1320 | `anl15_gr_ltg_cos_up` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Number of companies in the group whose long-term growth median was raised since last month |
| 1321 | `anl15_gr_ltg_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates (consensus coverage) for the group |
| 1322 | `anl15_gr_ltg_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates lowered since last month in the group |
| 1323 | `anl15_gr_ltg_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Long‑Term Growth estimates that were raised since last month at the group level |
| 1324 | `anl15_gr_ltg_mdn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Weighted median long-term growth forecast for the group |
| 1325 | `anl15_gr_ltg_mktcap` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies with long-term growth forecasts in the group |
| 1326 | `anl15_gr_ltg_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Group-level standard deviation of long-term growth estimates |
| 1327 | `anl15_gr_prc` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The weighted average price aggregated within GICS group grouping. |
| 1328 | `anl15_ind_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward earnings forecasts for the industry |
| 1329 | `anl15_ind_12_m_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted 3-month percent change of 12-month forward EPS estimation aggregated within GICS industry grouping. |
| 1330 | `anl15_ind_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward earnings forecasts at the industry level |
| 1331 | `anl15_ind_12_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean EPS estimation within GICS industry grouping. |
| 1332 | `anl15_ind_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose 12-month forward consensus EPS was lowered since last month |
| 1333 | `anl15_ind_12_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the industry with 12-month forward mean EPS raised since last month |
| 1334 | `anl15_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The 12-month forward pro-rated total number of estimates within GICS industry grouping. |
| 1335 | `anl15_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward estimates that have been lowered since last month for the industry |
| 1336 | `anl15_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of 12-month forward estimates raised since last month, aggregated at the industry level |
| 1337 | `anl15_ind_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 12‑month forward year‑over‑year earnings growth at the industry level |
| 1338 | `anl15_ind_12_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average 12-month forward EPS at the industry level |
| 1339 | `anl15_ind_12_m_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the industry with a 12-month forward mean EPS |
| 1340 | `anl15_ind_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward earnings for the industry |
| 1341 | `anl15_ind_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of forward 12-month EPS forecasts for the industry |
| 1342 | `anl15_ind_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 12-month forward earnings estimation aggregated within GICS industry grouping. |
| 1343 | `anl15_ind_12_m_tr_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12-month EPS for the industry |
| 1344 | `anl15_ind_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one‑month percent change in the forward 18‑month earnings forecast, constant sample, at the industry level |
| 1345 | `anl15_ind_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three‑month percent change in the forward 18‑month earnings forecast, constant sample, at the industry level |
| 1346 | `anl15_ind_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward earnings forecast for the industry, using a constant sample |
| 1347 | `anl15_ind_18_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean EPS estimation within GICS industry grouping. |
| 1348 | `anl15_ind_18_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose forward 18-month mean EPS was lowered since last month |
| 1349 | `anl15_ind_18_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which 18-month forward mean EPS estimation has been raised from last month within GICS industry grouping. |
| 1350 | `anl15_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for the trailing 18-month forward period at the industry level |
| 1351 | `anl15_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Industry-level number of estimates with negative revision over the trailing 18-month period |
| 1352 | `anl15_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates revised up for the forward 18‑month horizon at the industry level since the prior period |
| 1353 | `anl15_ind_18_m_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted 18-month forward year-over-year growth of EPS estimation aggregated within GICS industry grouping. |
| 1354 | `anl15_ind_18_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of 18 month forward EPS estimation aggregated within GICS industry grouping. |
| 1355 | `anl15_ind_18_m_mktcap` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies in the industry that have an 18‑month forward mean estimate |
| 1356 | `anl15_ind_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18‑month forward earnings at the industry level |
| 1357 | `anl15_ind_18_m_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18‑month forward earnings forecasts for the industry |
| 1358 | `anl15_ind_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of 18-month forward earnings estimation aggregated within GICS industry grouping. |
| 1359 | `anl15_ind_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-over-year growth in earnings for the current calendarized fiscal year (FY0), aggregated at the industry level |
| 1360 | `anl15_ind_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on calendarized FY0 forecasts for the industry |
| 1361 | `anl15_ind_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the current calendarized fiscal year aggregated within GICS industry grouping. |
| 1362 | `anl15_ind_cal_fy0_val` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized FY0 for the industry, calculated using shares and EPS weights |
| 1363 | `anl15_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 1 earnings forecasts, using a constant sample, aggregated at the industry leve |
| 1364 | `anl15_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized FY1 EPS forecasts for the industry, using a constant sample |
| 1365 | `anl15_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 1 EPS forecasts for the industry, using a constant sample |
| 1366 | `anl15_ind_cal_fy1_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 1 fiscal year EPS estimation within GICS industry grouping. |
| 1367 | `anl15_ind_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized FY1 at the industry level |
| 1368 | `anl15_ind_cal_fy1_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year EPS growth for calendarized Fiscal Year 1 aggregated at the industry level |
| 1369 | `anl15_ind_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized Fiscal Year 1 at the industry level |
| 1370 | `anl15_ind_cal_fy1_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level total market capitalization of companies with calendarized FY1 mean |
| 1371 | `anl15_ind_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 1 at the industry level |
| 1372 | `anl15_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY1 earnings forecasts for the industry |
| 1373 | `anl15_ind_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 1 period, aggregated at the industry level |
| 1374 | `anl15_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | One-month percent change in Fiscal Year 2 earnings forecasts, aggregated at the industry level |
| 1375 | `anl15_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the calendarized Fiscal Year 2 earnings forecast for the industry, using a constant sample |
| 1376 | `anl15_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 2 earnings forecasts, using a constant sample, aggregated at the industry leve |
| 1377 | `anl15_ind_cal_fy2_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal year EPS estimation within GICS industry grouping. |
| 1378 | `anl15_ind_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst estimates contributing to the calendarized Fiscal Year 2 consensus for the industry |
| 1379 | `anl15_ind_cal_fy2_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year EPS growth for calendarized Fiscal Year 2 aggregated at the industry level |
| 1380 | `anl15_ind_cal_fy2_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for the calendarized Fiscal Year 2 period at the industry level |
| 1381 | `anl15_ind_cal_fy2_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies in the industry that have a calendarized Fiscal Year 2 EPS mean |
| 1382 | `anl15_ind_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average Price/Earnings ratio for the calendarized Fiscal Year 2 period, aggregated at the industry level |
| 1383 | `anl15_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-level weighted average standard deviation of calendarized FY2 EPS forecasts |
| 1384 | `anl15_ind_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 2 period at the industry level |
| 1385 | `anl15_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one‑month percent change in calendarized Fiscal Year 3 earnings forecasts, constant sample, at the industry level |
| 1386 | `anl15_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three‑month percent change in the industry’s calendarized FY3 earnings forecast, using a constant sample |
| 1387 | `anl15_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized FY3 earnings forecasts for the industry, using a constant sample |
| 1388 | `anl15_ind_cal_fy3_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 3 fiscal year EPS estimation within GICS industry grouping. |
| 1389 | `anl15_ind_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for calendarized Fiscal Year 3 at the industry level |
| 1390 | `anl15_ind_cal_fy3_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in calendarized FY3 EPS for the industry |
| 1391 | `anl15_ind_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for calendarized Fiscal Year 3 at the industry level |
| 1392 | `anl15_ind_cal_fy3_mktcap` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies in the industry with a calendarized Fiscal Year 3 mean estimate |
| 1393 | `anl15_ind_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized FY3 at the industry level |
| 1394 | `anl15_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average standard deviation of EPS estimation for the calendarized 3 fiscal year aggregated within GICS industry grouping. |
| 1395 | `anl15_ind_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Industry-level total earnings for calendarized FY3 |
| 1396 | `anl15_ind_div_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which indicated annual dividend data is available within GICS industry grouping. |
| 1397 | `anl15_ind_divyld` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average dividend yield based on the indicated annual dividend for the industry |
| 1398 | `anl15_ind_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 1 mean was lowered since last month, aggregated at the industry level |
| 1399 | `anl15_ind_fy1_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which EPS estimation for the calendarized 1 fiscal year has been raised from last month within GICS industry gro |
| 1400 | `anl15_ind_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY1 earnings estimates lowered since last month for the industry |
| 1401 | `anl15_ind_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 estimates that were raised since last month in the industry |
| 1402 | `anl15_ind_fy2_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose calendarized Fiscal Year 2 mean EPS was lowered since last month |
| 1403 | `anl15_ind_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the industry whose calendarized Fiscal Year 2 consensus was raised since last month |
| 1404 | `anl15_ind_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY2 EPS estimates lowered since last month for the industry |
| 1405 | `anl15_ind_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 estimates raised since last month in the industry |
| 1406 | `anl15_ind_fy3_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 3 mean was lowered since last month, aggregated at the industry level |
| 1407 | `anl15_ind_fy3_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which EPS estimation for the calendarized 3 fiscal year has been raised from last month within GICS industry gro |
| 1408 | `anl15_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized FY3 estimates lowered since last month at the industry level |
| 1409 | `anl15_ind_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 analyst estimates raised since last month at the industry level |
| 1410 | `anl15_ind_hist_eps_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted annual EPS growth rate over the past five years based on a loglinear regression at the industry level |
| 1411 | `anl15_ind_ltg_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in long-term growth (LTG) forecasts, aggregated at the industry level |
| 1412 | `anl15_ind_ltg_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in long-term growth (LTG) forecasts at the industry level |
| 1413 | `anl15_ind_ltg_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in long-term growth forecasts for the industry |
| 1414 | `anl15_ind_ltg_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a long-term growth EPS estimation within GICS industry grouping. |
| 1415 | `anl15_ind_ltg_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which long-term growth EPS estimation has been lowered from last month within GICS industry grouping. |
| 1416 | `anl15_ind_ltg_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the long-term growth consensus was raised since last month at the industry level |
| 1417 | `anl15_ind_ltg_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long‑term growth estimates (consensus), aggregated at the industry level |
| 1418 | `anl15_ind_ltg_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates lowered since last month for the industry |
| 1419 | `anl15_ind_ltg_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates raised since last month at the industry level |
| 1420 | `anl15_ind_ltg_mdn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of long-term growth EPS estimation aggregated within GICS industry grouping. |
| 1421 | `anl15_ind_ltg_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization of companies with long-term growth (LTG) forecasts, aggregated at the industry level |
| 1422 | `anl15_ind_ltg_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of long-term growth (LTG) estimates for the industry |
| 1423 | `anl15_ind_prc` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Weighted average share price of companies in the industry |
| 1424 | `anl15_s_12_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one‑month percent change in the sector’s 12‑month forward earnings forecasts, using a constant sample |
| 1425 | `anl15_s_12_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward earnings forecasts at the sector level (constant sample) |
| 1426 | `anl15_s_12_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 12-month forward earnings forecasts for the sector |
| 1427 | `anl15_s_12_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a 12-month forward mean EPS estimation within GICS sector grouping. |
| 1428 | `anl15_s_12_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the sector with a lower 12-month forward mean EPS since last month |
| 1429 | `anl15_s_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose 12-month forward consensus EPS was raised since last month |
| 1430 | `anl15_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the 12-month forward period for the sector |
| 1431 | `anl15_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of 12-month forward estimates lowered since last month at the sector level |
| 1432 | `anl15_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pro-rated number of forward 12-month earnings estimates raised since last month for the sector |
| 1433 | `anl15_s_12_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year earnings growth at the sector level |
| 1434 | `anl15_s_12_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average forward 12-month EPS for the sector |
| 1435 | `anl15_s_12_m_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the sector with a 12‑month forward mean |
| 1436 | `anl15_s_12_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on forward 12-month EPS for the sector |
| 1437 | `anl15_s_12_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward EPS forecasts at the sector level |
| 1438 | `anl15_s_12_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total forward 12‑month earnings for the sector |
| 1439 | `anl15_s_12_m_tr_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average trailing 12-month EPS for the sector |
| 1440 | `anl15_s_18_m_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 18-month forward earnings forecasts for the sector, using a constant sample |
| 1441 | `anl15_s_18_m_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three‑month percent change in the forward 18‑month earnings forecast, constant sample, at the sector level |
| 1442 | `anl15_s_18_m_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in 18-month forward earnings forecasts for the sector, using a constant sample |
| 1443 | `anl15_s_18_m_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with an 18-month forward mean EPS estimation within GICS sector grouping. |
| 1444 | `anl15_s_18_m_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the sector with 18-month forward mean EPS lowered since last month |
| 1445 | `anl15_s_18_m_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose forward 18-month mean EPS was raised since last month |
| 1446 | `anl15_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for the 18-month forward period in the sector |
| 1447 | `anl15_s_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates with negative revisions for the sector’s 18‑month forward period |
| 1448 | `anl15_s_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level number of estimates with positive revision over the trailing 18-month period |
| 1449 | `anl15_s_18_m_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted 18‑month forward earnings growth for the sector |
| 1450 | `anl15_s_18_m_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average 18-month forward EPS at the sector level |
| 1451 | `anl15_s_18_m_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the sector with an 18‑month forward mean |
| 1452 | `anl15_s_18_m_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The weighted average price/earnings ratio based on 18-month forward EPS estimation aggregated within GICS sector grouping. |
| 1453 | `anl15_s_18_m_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward EPS forecasts, aggregated at the sector level |
| 1454 | `anl15_s_18_m_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the forward 18‑month horizon at the sector level |
| 1455 | `anl15_s_cal_fy0_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year earnings growth for calendarized Fiscal Year 0 at the sector level |
| 1456 | `anl15_s_cal_fy0_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for the current calendarized fiscal year (FY0) at the sector level |
| 1457 | `anl15_s_cal_fy0_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the current calendarized fiscal year aggregated within GICS sector grouping. |
| 1458 | `anl15_s_cal_fy0_val` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Sector-level weighted average EPS for calendarized FY0 |
| 1459 | `anl15_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in earnings forecasts for calendarized Fiscal Year 1 using a constant sample at the sector level |
| 1460 | `anl15_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sector-level weighted three-month percent change in calendarized FY1 earnings forecasts using a constant sample |
| 1461 | `anl15_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six‑month percent change in calendarized Fiscal Year 1 earnings forecasts, constant sample, at the sector level |
| 1462 | `anl15_s_cal_fy1_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 1 fiscal year EPS estimation within GICS sector grouping. |
| 1463 | `anl15_s_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized Fiscal Year 1 estimates aggregated at the sector level |
| 1464 | `anl15_s_cal_fy1_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in calendarized FY1 EPS for the sector |
| 1465 | `anl15_s_cal_fy1_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS for the calendarized Fiscal Year 1 period, aggregated at the sector level |
| 1466 | `anl15_s_cal_fy1_mktcap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | The total market capitalization for the companies aggregated within GICS sector grouping with a calendarized 1 fiscal year mean price estima |
| 1467 | `anl15_s_cal_fy1_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 1 at the sector level |
| 1468 | `anl15_s_cal_fy1_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EPS forecasts for calendarized Fiscal Year 1 at the sector level |
| 1469 | `anl15_s_cal_fy1_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total earnings for the calendarized Fiscal Year 1 period at the sector level |
| 1470 | `anl15_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized FY2 EPS forecasts for the sector, using a constant sample |
| 1471 | `anl15_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the calendarized FY2 earnings forecast for the sector, using a constant sample |
| 1472 | `anl15_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in calendarized Fiscal Year 2 EPS forecasts for the sector, using a constant sample |
| 1473 | `anl15_s_cal_fy2_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 2 fiscal year EPS estimation within GICS sector grouping. |
| 1474 | `anl15_s_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized Fiscal Year 2 at the sector level |
| 1475 | `anl15_s_cal_fy2_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year‑over‑year earnings growth for calendarized Fiscal Year 2 at the sector level |
| 1476 | `anl15_s_cal_fy2_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS forecast for calendarized FY2 for the sector |
| 1477 | `anl15_s_cal_fy2_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the sector with a calendarized Fiscal Year 2 mean |
| 1478 | `anl15_s_cal_fy2_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio for calendarized FY2 at the sector level |
| 1479 | `anl15_s_cal_fy2_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized Fiscal Year 2 EPS forecasts for the sector |
| 1480 | `anl15_s_cal_fy2_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized 2 fiscal year aggregated within GICS sector grouping. |
| 1481 | `anl15_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized Fiscal Year 3 earnings forecasts, using a constant sample, aggregated at the sector level |
| 1482 | `anl15_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Three-month percent change in calendarized Fiscal Year 3 earnings forecasts, aggregated at the sector level |
| 1483 | `anl15_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted six‑month percent change in the sector’s calendarized FY3 earnings forecast, using a constant sample |
| 1484 | `anl15_s_cal_fy3_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a calendarized 3 fiscal year EPS estimation within GICS sector grouping. |
| 1485 | `anl15_s_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of estimates for calendarized Fiscal Year 3 at the sector level |
| 1486 | `anl15_s_cal_fy3_gro` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth in earnings for calendarized Fiscal Year 3, aggregated at the sector level |
| 1487 | `anl15_s_cal_fy3_mean` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average EPS forecast for calendarized FY3 at the sector level |
| 1488 | `anl15_s_cal_fy3_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the sector with a calendarized Fiscal Year 3 mean |
| 1489 | `anl15_s_cal_fy3_pe` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio for calendarized Fiscal Year 3 at the sector level |
| 1490 | `anl15_s_cal_fy3_st_dev` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of EPS forecasts for calendarized FY3 at the sector level |
| 1491 | `anl15_s_cal_fy3_total` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The total of earnings estimation for the calendarized 3 fiscal year aggregated within GICS sector grouping. |
| 1492 | `anl15_s_div_cos` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The number of companies for which indicated annual dividend data is available within GICS sector grouping. |
| 1493 | `anl15_s_divyld` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average dividend yield based on indicated annual dividend for the sector |
| 1494 | `anl15_s_fy1_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which EPS estimation for the calendarized one fiscal year has been lowered from last month within GICS sector gr |
| 1495 | `anl15_s_fy1_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which EPS estimation for the calendarized 1 fiscal year has been raised from last month within GICS sector group |
| 1496 | `anl15_s_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 earnings estimates lowered since last month, aggregated at the sector level |
| 1497 | `anl15_s_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 1 analyst estimates raised since last month in the sector |
| 1498 | `anl15_s_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose calendarized Fiscal Year 2 consensus mean was lowered since last month |
| 1499 | `anl15_s_fy2_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which the calendarized Fiscal Year 2 mean was raised since last month, aggregated at the sector level |
| 1500 | `anl15_s_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Fiscal Year 2 estimates lowered since last month, aggregated at the sector level |
| 1501 | `anl15_s_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of FY2 earnings estimates raised since last month for the sector |
| 1502 | `anl15_s_fy3_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies for which EPS estimation for the calendarized 3 fiscal years has been lowered from last month within GICS sector gro |
| 1503 | `anl15_s_fy3_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the sector whose calendarized FY3 mean EPS was raised since last month |
| 1504 | `anl15_s_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of calendarized Fiscal Year 3 estimates lowered since last month at the sector level |
| 1505 | `anl15_s_fy3_ests_up` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 1506 | `anl15_s_hist_eps_gro` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted annual EPS growth rate over the past five years for the sector, from a loglinear regression of the last five years of annual EPS |
| 1507 | `anl15_s_ltg_1m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in long-term growth forecasts for the sector |
| 1508 | `anl15_s_ltg_3m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in long-term growth (LTG) forecasts, aggregated at the sector level |
| 1509 | `anl15_s_ltg_6m_chg` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the long-term growth forecast at the sector level |
| 1510 | `anl15_s_ltg_cos` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The number of companies with a long-term growth EPS estimation within GICS sector grouping. |
| 1511 | `anl15_s_ltg_cos_dn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies for which the long-term growth median has been lowered since last month at the sector level |
| 1512 | `anl15_s_ltg_cos_up` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of companies in the sector for which the Long‑Term Growth (LTG) median was raised since last month |
| 1513 | `anl15_s_ltg_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates (consensus) for the sector |
| 1514 | `anl15_s_ltg_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates lowered since last month at the sector level |
| 1515 | `anl15_s_ltg_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth estimates raised since last month for the sector |
| 1516 | `anl15_s_ltg_mdn` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The weighted average of long-term growth EPS estimation aggregated within GICS sector grouping. |
| 1517 | `anl15_s_ltg_mktcap` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total market capitalization for companies in the sector with long-term growth forecasts |
| 1518 | `anl15_s_ltg_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of Long‑Term Growth estimates at the sector level |
| 1519 | `anl15_s_prc` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Weighted average price per share for companies in the sector, as of the date |
| 1520 | `anl15_sal_gr_12_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward revenue (sales) estimates aggregated within the GICS group |
| 1521 | `anl15_sal_gr_12_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change of the 12-month forward revenue (SAL) estimate aggregated within GICS group grouping |
| 1522 | `anl15_sal_gr_12_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change of the 12-month forward revenue (SAL) estimate aggregated within GICS group grouping |
| 1523 | `anl15_sal_gr_12_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a forward 12-month mean revenue (SAL) estimate within the GICS group grouping |
| 1524 | `anl15_sal_gr_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month mean revenue (SAL) estimate has decreased since last month within the GICS group grouping |
| 1525 | `anl15_sal_gr_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month mean revenue (SAL) estimate has increased since last month within the GICS group grouping |
| 1526 | `anl15_sal_gr_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates within the GICS group |
| 1527 | `anl15_sal_gr_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates that have been lowered since last month within the GICS group |
| 1528 | `anl15_sal_gr_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates that have been raised since last month within the GICS group |
| 1529 | `anl15_sal_gr_12_m_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth of revenue (sales) estimates aggregated within the GICS group |
| 1530 | `anl15_sal_gr_12_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of forward 12-month revenue (SAL) estimates, aggregated within the GICS group grouping |
| 1531 | `anl15_sal_gr_12_m_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward EPS estimates aggregated within the GICS group |
| 1532 | `anl15_sal_gr_12_m_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward revenue (sales) estimates aggregated within the GICS group |
| 1533 | `anl15_sal_gr_12_m_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total forward 12-month revenue (SAL) estimate, aggregated within the GICS group grouping |
| 1534 | `anl15_sal_gr_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average of trailing 12-month revenue (SAL), aggregated within the GICS group grouping |
| 1535 | `anl15_sal_gr_18_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS group grouping |
| 1536 | `anl15_sal_gr_18_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS group grouping |
| 1537 | `anl15_sal_gr_18_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward consensus revenue (SAL) estimate aggregated at the GICS group level, using a const |
| 1538 | `anl15_sal_gr_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with an 18-month forward mean revenue (SAL) estimate within GICS group grouping |
| 1539 | `anl15_sal_gr_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the 18-month forward mean revenue (SAL) estimate has been lowered since last month within GICS group grouping |
| 1540 | `anl15_sal_gr_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the 18-month forward mean revenue (SAL) estimate has been raised since last month within GICS group grouping |
| 1541 | `anl15_sal_gr_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates aggregated within the GICS group grouping |
| 1542 | `anl15_sal_gr_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates that have been lowered since last month within the GICS group grouping |
| 1543 | `anl15_sal_gr_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates that have been raised since last month within the GICS group grouping |
| 1544 | `anl15_sal_gr_18_m_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted 18 month forward year-over-year growth of revenue (SAL) estimates aggregated within the GICS group grouping |
| 1545 | `anl15_sal_gr_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of the 18-month forward revenue (SAL) estimate aggregated within GICS group grouping |
| 1546 | `anl15_sal_gr_18_m_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18 month forward EPS estimates aggregated within the GICS group grouping |
| 1547 | `anl15_sal_gr_18_m_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward revenue (SAL) estimates aggregated within GICS group grouping |
| 1548 | `anl15_sal_gr_18_m_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total of the 18-month forward revenue (SAL) estimate aggregated within GICS group grouping |
| 1549 | `anl15_sal_gr_cal_fy0_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue (SAL) estimates for the current calendarized fiscal year aggregated within the GICS group grouping |
| 1550 | `anl15_sal_gr_cal_fy0_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on EPS estimates for the current calendarized fiscal year aggregated within the GICS group group |
| 1551 | `anl15_sal_gr_cal_fy0_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for the current calendarized fiscal year aggregated within the GICS group grouping |
| 1552 | `anl15_sal_gr_cal_fy0_val` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for the current calendarized fiscal year aggregated within the GICS group grouping |
| 1553 | `anl15_sal_gr_cal_fy1_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS group level |
| 1554 | `anl15_sal_gr_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS group level |
| 1555 | `anl15_sal_gr_cal_fy1_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS group level |
| 1556 | `anl15_sal_gr_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized one fiscal year revenue (SAL) estimate within the GICS group grouping |
| 1557 | `anl15_sal_gr_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates within the GICS industry group |
| 1558 | `anl15_sal_gr_cal_fy1_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue estimates for calendarized fiscal year 1 at the GICS group level |
| 1559 | `anl15_sal_gr_cal_fy1_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for the calendarized one fiscal year (FY1) aggregated within the GICS group grouping |
| 1560 | `anl15_sal_gr_cal_fy1_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on calendarized FY1 EPS estimates aggregated within the GICS industry group |
| 1561 | `anl15_sal_gr_cal_fy1_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY1 revenue (Sales) estimates aggregated within the GICS industry group |
| 1562 | `anl15_sal_gr_cal_fy1_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for the calendarized one fiscal year (FY1) aggregated within the GICS group grouping |
| 1563 | `anl15_sal_gr_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS industry group level |
| 1564 | `anl15_sal_gr_cal_fy2_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS industry group level |
| 1565 | `anl15_sal_gr_cal_fy2_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS industry group level |
| 1566 | `anl15_sal_gr_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized fiscal year 2 revenue estimate in the GICS group |
| 1567 | `anl15_sal_gr_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 within the GICS group grouping |
| 1568 | `anl15_sal_gr_cal_fy2_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS group grouping |
| 1569 | `anl15_sal_gr_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue estimate for calendarized fiscal year 2 at the GICS group level |
| 1570 | `anl15_sal_gr_cal_fy2_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on EPS estimates for calendarized Fiscal Year 2 aggregated within the GICS group grouping |
| 1571 | `anl15_sal_gr_cal_fy2_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS group grouping |
| 1572 | `anl15_sal_gr_cal_fy2_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue estimate for calendarized fiscal year 2 at the GICS group level |
| 1573 | `anl15_sal_gr_cal_fy3_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS group |
| 1574 | `anl15_sal_gr_cal_fy3_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the consensus revenue (SAL) forecast for calendarized fiscal year 3 (FY3), aggregated at the GICS gro |
| 1575 | `anl15_sal_gr_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the consensus revenue (SAL) forecast for calendarized fiscal year 3 (FY3), aggregated at the GICS group |
| 1576 | `anl15_sal_gr_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized Fiscal Year 3 revenue (SAL) estimate, aggregated at the GICS industry group level |
| 1577 | `anl15_sal_gr_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for calendarized FY3 at the group level |
| 1578 | `anl15_sal_gr_cal_fy3_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS group |
| 1579 | `anl15_sal_gr_cal_fy3_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for calendarized Fiscal Year 3, aggregated at the GICS industry group level |
| 1580 | `anl15_sal_gr_cal_fy3_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on calendarized fiscal year 3 EPS estimates aggregated within the GICS group |
| 1581 | `anl15_sal_gr_cal_fy3_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS group |
| 1582 | `anl15_sal_gr_cal_fy3_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for calendarized Fiscal Year 3, aggregated at the GICS industry group level |
| 1583 | `anl15_sal_gr_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY1 revenue (Sales) estimate was lowered since last month within the GICS industry group |
| 1584 | `anl15_sal_gr_fy1_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY1 revenue (Sales) estimate was raised since last month within the GICS industry group |
| 1585 | `anl15_sal_gr_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates that were lowered since last month within the GICS industry group |
| 1586 | `anl15_sal_gr_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates that were raised since last month within the GICS industry group |
| 1587 | `anl15_sal_gr_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the revenue (SAL) estimate for calendarized Fiscal Year 2 has been lowered since last month within the GICS gr |
| 1588 | `anl15_sal_gr_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized fiscal year 2 revenue estimate increased versus last month in the GICS group |
| 1589 | `anl15_sal_gr_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 that have been lowered since last month within the GICS group groupin |
| 1590 | `anl15_sal_gr_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 that have been raised since last month within the GICS group grouping |
| 1591 | `anl15_sal_gr_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 3 revenue (SAL) consensus has been lowered since last month, aggregated at the GICS indus |
| 1592 | `anl15_sal_gr_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 3 revenue (SAL) consensus has been raised since last month, aggregated at the GICS indust |
| 1593 | `anl15_sal_gr_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates that have been lowered since last month within the GICS group |
| 1594 | `anl15_sal_gr_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates that have been raised since last month within the GICS group |
| 1595 | `anl15_sal_ind_12_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward revenue (sales) estimates aggregated within the GICS industry |
| 1596 | `anl15_sal_ind_12_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change of the 12-month forward revenue (SAL) estimate aggregated within GICS industry grouping |
| 1597 | `anl15_sal_ind_12_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change of the 12-month forward revenue (SAL) estimate aggregated within GICS industry grouping |
| 1598 | `anl15_sal_ind_12_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a forward 12-month mean revenue (SAL) estimate within the GICS industry grouping |
| 1599 | `anl15_sal_ind_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month mean revenue (SAL) estimate has decreased since last month within the GICS industry grouping |
| 1600 | `anl15_sal_ind_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month mean revenue (SAL) estimate has increased since last month within the GICS industry grouping |
| 1601 | `anl15_sal_ind_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates within the GICS industry |
| 1602 | `anl15_sal_ind_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates that have been lowered since last month within the GICS industry |
| 1603 | `anl15_sal_ind_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates that have been raised since last month within the GICS industry |
| 1604 | `anl15_sal_ind_12_m_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth of revenue (sales) estimates aggregated within the GICS industry |
| 1605 | `anl15_sal_ind_12_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of forward 12-month revenue (SAL) estimates, aggregated within the GICS industry grouping |
| 1606 | `anl15_sal_ind_12_m_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward EPS estimates aggregated within the GICS industry |
| 1607 | `anl15_sal_ind_12_m_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward revenue (sales) estimates aggregated within the GICS industry |
| 1608 | `anl15_sal_ind_12_m_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total forward 12-month revenue (SAL) estimate, aggregated within the GICS industry grouping |
| 1609 | `anl15_sal_ind_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average of trailing 12-month revenue (SAL), aggregated within the GICS industry grouping |
| 1610 | `anl15_sal_ind_18_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS industry grouping |
| 1611 | `anl15_sal_ind_18_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS industry grouping |
| 1612 | `anl15_sal_ind_18_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the 18-month forward consensus revenue (SAL) estimate aggregated at the GICS industry level, using a co |
| 1613 | `anl15_sal_ind_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with an 18-month forward mean revenue (SAL) estimate within GICS industry grouping |
| 1614 | `anl15_sal_ind_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the 18-month forward mean revenue (SAL) estimate has been lowered since last month within GICS industry groupi |
| 1615 | `anl15_sal_ind_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the 18-month forward mean revenue (SAL) estimate has been raised since last month within GICS industry groupin |
| 1616 | `anl15_sal_ind_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates aggregated within the GICS industry grouping |
| 1617 | `anl15_sal_ind_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates that have been lowered since last month within the GICS industry grouping |
| 1618 | `anl15_sal_ind_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates that have been raised since last month within the GICS industry grouping |
| 1619 | `anl15_sal_ind_18_m_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted 18 month forward year-over-year growth of revenue (SAL) estimates aggregated within the GICS industry grouping |
| 1620 | `anl15_sal_ind_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of the 18-month forward revenue (SAL) estimate aggregated within GICS industry grouping |
| 1621 | `anl15_sal_ind_18_m_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18 month forward EPS estimates aggregated within the GICS industry grouping |
| 1622 | `anl15_sal_ind_18_m_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward revenue (SAL) estimates aggregated within GICS industry grouping |
| 1623 | `anl15_sal_ind_18_m_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total of the 18-month forward revenue (SAL) estimate aggregated within GICS industry grouping |
| 1624 | `anl15_sal_ind_cal_fy0_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue (SAL) estimates for the current calendarized fiscal year aggregated within the GICS industry group |
| 1625 | `anl15_sal_ind_cal_fy0_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on EPS estimates for the current calendarized fiscal year aggregated within the GICS industry gr |
| 1626 | `anl15_sal_ind_cal_fy0_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for the current calendarized fiscal year aggregated within the GICS industry grouping |
| 1627 | `anl15_sal_ind_cal_fy0_val` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for the current calendarized fiscal year aggregated within the GICS industry grouping |
| 1628 | `anl15_sal_ind_cal_fy1_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS industry level |
| 1629 | `anl15_sal_ind_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS industry level |
| 1630 | `anl15_sal_ind_cal_fy1_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS industry level |
| 1631 | `anl15_sal_ind_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized one fiscal year revenue (SAL) estimate within the GICS industry grouping |
| 1632 | `anl15_sal_ind_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst estimates for calendarized FY1 at the industry level |
| 1633 | `anl15_sal_ind_cal_fy1_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue estimates for calendarized fiscal year 1 at the GICS industry level |
| 1634 | `anl15_sal_ind_cal_fy1_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for the calendarized one fiscal year (FY1) aggregated within the GICS industry grouping |
| 1635 | `anl15_sal_ind_cal_fy1_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on calendarized FY1 EPS estimates aggregated within the GICS industry |
| 1636 | `anl15_sal_ind_cal_fy1_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY1 revenue (Sales) estimates aggregated within the GICS industry |
| 1637 | `anl15_sal_ind_cal_fy1_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for the calendarized one fiscal year (FY1) aggregated within the GICS industry grouping |
| 1638 | `anl15_sal_ind_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS industry level |
| 1639 | `anl15_sal_ind_cal_fy2_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS industry level |
| 1640 | `anl15_sal_ind_cal_fy2_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS industry level |
| 1641 | `anl15_sal_ind_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized fiscal year 2 revenue estimate in the GICS industry |
| 1642 | `anl15_sal_ind_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 within the GICS industry grouping |
| 1643 | `anl15_sal_ind_cal_fy2_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS industry grouping |
| 1644 | `anl15_sal_ind_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue estimate for calendarized fiscal year 2 at the GICS industry level |
| 1645 | `anl15_sal_ind_cal_fy2_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on EPS estimates for calendarized Fiscal Year 2 aggregated within the GICS industry grouping |
| 1646 | `anl15_sal_ind_cal_fy2_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS industry grouping |
| 1647 | `anl15_sal_ind_cal_fy2_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue estimate for calendarized fiscal year 2 at the GICS industry level |
| 1648 | `anl15_sal_ind_cal_fy3_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS industry |
| 1649 | `anl15_sal_ind_cal_fy3_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in the consensus revenue (SAL) forecast for calendarized fiscal year 3 (FY3), aggregated at the GICS ind |
| 1650 | `anl15_sal_ind_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the consensus revenue (SAL) forecast for calendarized fiscal year 3 (FY3), aggregated at the GICS indus |
| 1651 | `anl15_sal_ind_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized Fiscal Year 3 revenue (SAL) estimate, aggregated at the GICS industry level |
| 1652 | `anl15_sal_ind_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for calendarized FY3 at the industry level |
| 1653 | `anl15_sal_ind_cal_fy3_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS industry |
| 1654 | `anl15_sal_ind_cal_fy3_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for calendarized Fiscal Year 3, aggregated at the GICS industry level |
| 1655 | `anl15_sal_ind_cal_fy3_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on calendarized fiscal year 3 EPS estimates aggregated within the GICS industry |
| 1656 | `anl15_sal_ind_cal_fy3_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS industry |
| 1657 | `anl15_sal_ind_cal_fy3_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for calendarized Fiscal Year 3, aggregated at the GICS industry level |
| 1658 | `anl15_sal_ind_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY1 revenue (Sales) estimate was lowered since last month within the GICS industry |
| 1659 | `anl15_sal_ind_fy1_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY1 revenue (Sales) estimate was raised since last month within the GICS industry |
| 1660 | `anl15_sal_ind_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates that were lowered since last month within the GICS industry |
| 1661 | `anl15_sal_ind_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates that were raised since last month within the GICS industry |
| 1662 | `anl15_sal_ind_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the revenue (SAL) estimate for calendarized Fiscal Year 2 has been lowered since last month within the GICS in |
| 1663 | `anl15_sal_ind_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized fiscal year 2 revenue estimate increased versus last month in the GICS industry |
| 1664 | `anl15_sal_ind_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 that have been lowered since last month within the GICS industry grou |
| 1665 | `anl15_sal_ind_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 that have been raised since last month within the GICS industry group |
| 1666 | `anl15_sal_ind_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 3 revenue (SAL) consensus has been lowered since last month, aggregated at the GICS indus |
| 1667 | `anl15_sal_ind_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 3 revenue (SAL) consensus has been raised since last month, aggregated at the GICS indust |
| 1668 | `anl15_sal_ind_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates that have been lowered since last month within the GICS industry |
| 1669 | `anl15_sal_ind_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates that have been raised since last month within the GICS industry |
| 1670 | `anl15_sal_s_12_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in 12-month forward revenue (sales) estimates aggregated within the GICS sector |
| 1671 | `anl15_sal_s_12_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in 12-month forward revenue (sales) estimates aggregated within the GICS sector |
| 1672 | `anl15_sal_s_12_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change of the 12-month forward revenue (SAL) estimate aggregated within GICS sector grouping |
| 1673 | `anl15_sal_s_12_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a forward 12-month mean revenue (SAL) estimate within the GICS sector grouping |
| 1674 | `anl15_sal_s_12_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month mean revenue (SAL) estimate has decreased since last month within the GICS sector grouping |
| 1675 | `anl15_sal_s_12_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose forward 12-month mean revenue (SAL) estimate has increased since last month within the GICS sector grouping |
| 1676 | `anl15_sal_s_12_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates within the GICS sector |
| 1677 | `anl15_sal_s_12_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates that have been lowered since last month within the GICS sector |
| 1678 | `anl15_sal_s_12_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 12-month forward pro-rated total number of revenue (sales) estimates that have been raised since last month within the GICS sector |
| 1679 | `anl15_sal_s_12_m_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted 12-month forward year-over-year growth of revenue (sales) estimates aggregated within the GICS sector |
| 1680 | `anl15_sal_s_12_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of forward 12-month revenue (SAL) estimates, aggregated within the GICS sector grouping |
| 1681 | `anl15_sal_s_12_m_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price-to-earnings ratio based on 12-month forward EPS estimates aggregated within the GICS sector |
| 1682 | `anl15_sal_s_12_m_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 12-month forward revenue (sales) estimates aggregated within the GICS sector |
| 1683 | `anl15_sal_s_12_m_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total forward 12-month revenue (SAL) estimate, aggregated within the GICS sector grouping |
| 1684 | `anl15_sal_s_12_m_tr_mean` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Weighted average of trailing 12-month revenue (SAL), aggregated within the GICS sector grouping |
| 1685 | `anl15_sal_s_18_m_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS sector grouping |
| 1686 | `anl15_sal_s_18_m_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS sector grouping |
| 1687 | `anl15_sal_s_18_m_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six month percent change of 18 month forward revenue (SAL) estimates aggregated within the GICS sector grouping |
| 1688 | `anl15_sal_s_18_m_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with an 18-month forward mean revenue (SAL) estimate within GICS sector grouping |
| 1689 | `anl15_sal_s_18_m_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the 18-month forward mean revenue (SAL) estimate has been lowered since last month within GICS sector grouping |
| 1690 | `anl15_sal_s_18_m_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the 18-month forward mean revenue (SAL) estimate has been raised since last month within GICS sector grouping |
| 1691 | `anl15_sal_s_18_m_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates aggregated within the GICS sector grouping |
| 1692 | `anl15_sal_s_18_m_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates that have been lowered since last month within the GICS sector grouping |
| 1693 | `anl15_sal_s_18_m_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | 18 month forward pro-rated total number of estimates that have been raised since last month within the GICS sector grouping |
| 1694 | `anl15_sal_s_18_m_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted 18 month forward year-over-year growth of revenue (SAL) estimates aggregated within the GICS sector grouping |
| 1695 | `anl15_sal_s_18_m_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average of the 18-month forward revenue (SAL) estimate aggregated within GICS sector grouping |
| 1696 | `anl15_sal_s_18_m_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on 18 month forward EPS estimates aggregated within the GICS sector grouping |
| 1697 | `anl15_sal_s_18_m_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of 18-month forward revenue (SAL) estimates aggregated within GICS sector grouping |
| 1698 | `anl15_sal_s_18_m_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total of the 18-month forward revenue (SAL) estimate aggregated within GICS sector grouping |
| 1699 | `anl15_sal_s_cal_fy0_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue (SAL) estimates for the current calendarized fiscal year aggregated within the GICS sector groupin |
| 1700 | `anl15_sal_s_cal_fy0_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on EPS estimates for the current calendarized fiscal year aggregated within the GICS sector grou |
| 1701 | `anl15_sal_s_cal_fy0_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for the current calendarized fiscal year aggregated within the GICS sector grouping |
| 1702 | `anl15_sal_s_cal_fy0_val` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for the current calendarized fiscal year aggregated within the GICS sector grouping |
| 1703 | `anl15_sal_s_cal_fy1_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS sector level |
| 1704 | `anl15_sal_s_cal_fy1_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS sector level |
| 1705 | `anl15_sal_s_cal_fy1_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in revenue estimates for calendarized fiscal year 1 at the GICS sector level |
| 1706 | `anl15_sal_s_cal_fy1_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized one fiscal year revenue (SAL) estimate within the GICS sector grouping |
| 1707 | `anl15_sal_s_cal_fy1_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sector-level total number of calendarized Fiscal Year 1 estimates |
| 1708 | `anl15_sal_s_cal_fy1_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of calendarized FY1 revenue (Sales) estimates aggregated within the GICS sector |
| 1709 | `anl15_sal_s_cal_fy1_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for the calendarized one fiscal year (FY1) aggregated within the GICS sector grouping |
| 1710 | `anl15_sal_s_cal_fy1_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on calendarized FY1 EPS estimates aggregated within the GICS sector |
| 1711 | `anl15_sal_s_cal_fy1_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized FY1 revenue (Sales) estimates aggregated within the GICS sector |
| 1712 | `anl15_sal_s_cal_fy1_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for the calendarized one fiscal year (FY1) aggregated within the GICS sector grouping |
| 1713 | `anl15_sal_s_cal_fy2_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS sector grouping |
| 1714 | `anl15_sal_s_cal_fy2_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS sector level |
| 1715 | `anl15_sal_s_cal_fy2_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in revenue (SAL) estimates for calendarized Fiscal Year 2, aggregated at the GICS sector level |
| 1716 | `anl15_sal_s_cal_fy2_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized fiscal year 2 revenue estimate in the GICS sector |
| 1717 | `anl15_sal_s_cal_fy2_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 within the GICS sector grouping |
| 1718 | `anl15_sal_s_cal_fy2_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS sector grouping |
| 1719 | `anl15_sal_s_cal_fy2_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue estimate for calendarized fiscal year 2 at the GICS sector level |
| 1720 | `anl15_sal_s_cal_fy2_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on EPS estimates for calendarized Fiscal Year 2 aggregated within the GICS sector grouping |
| 1721 | `anl15_sal_s_cal_fy2_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of revenue (SAL) estimates for calendarized Fiscal Year 2 aggregated within the GICS sector grouping |
| 1722 | `anl15_sal_s_cal_fy2_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue estimate for calendarized fiscal year 2 at the GICS sector level |
| 1723 | `anl15_sal_s_cal_fy3_1m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted one-month percent change in calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS sector |
| 1724 | `anl15_sal_s_cal_fy3_3m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted three-month percent change in calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS sector |
| 1725 | `anl15_sal_s_cal_fy3_6m_chg` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted six-month percent change in the consensus revenue (SAL) forecast for calendarized fiscal year 3 (FY3), aggregated at the GICS secto |
| 1726 | `anl15_sal_s_cal_fy3_cos` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies with a calendarized Fiscal Year 3 revenue (SAL) estimate, aggregated at the GICS sector level |
| 1727 | `anl15_sal_s_cal_fy3_ests` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates within the GICS sector |
| 1728 | `anl15_sal_s_cal_fy3_gro` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted year-over-year growth of calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS sector |
| 1729 | `anl15_sal_s_cal_fy3_mean` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average revenue (SAL) estimate for calendarized Fiscal Year 3, aggregated at the GICS sector level |
| 1730 | `anl15_sal_s_cal_fy3_pe` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average price/earnings ratio based on calendarized fiscal year 3 EPS estimates aggregated within the GICS sector |
| 1731 | `anl15_sal_s_cal_fy3_st_dev` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Weighted average standard deviation of calendarized fiscal year 3 revenue (sales) estimates aggregated within the GICS sector |
| 1732 | `anl15_sal_s_cal_fy3_total` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total revenue (SAL) estimate for calendarized Fiscal Year 3, aggregated at the GICS sector level |
| 1733 | `anl15_sal_s_fy1_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY1 revenue (Sales) estimate was lowered since last month within the GICS sector |
| 1734 | `anl15_sal_s_fy1_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized FY1 revenue (Sales) estimate was raised since last month within the GICS sector |
| 1735 | `anl15_sal_s_fy1_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates that were lowered since last month within the GICS sector |
| 1736 | `anl15_sal_s_fy1_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized FY1 revenue (Sales) estimates that were raised since last month within the GICS sector |
| 1737 | `anl15_sal_s_fy2_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies for which the revenue (SAL) estimate for calendarized Fiscal Year 2 has been lowered since last month within the GICS se |
| 1738 | `anl15_sal_s_fy2_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized fiscal year 2 revenue estimate increased versus last month in the GICS sector |
| 1739 | `anl15_sal_s_fy2_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 that have been lowered since last month within the GICS sector groupi |
| 1740 | `anl15_sal_s_fy2_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of revenue (SAL) estimates for calendarized Fiscal Year 2 that have been raised since last month within the GICS sector groupin |
| 1741 | `anl15_sal_s_fy3_cos_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 3 revenue (SAL) consensus has been lowered since last month, aggregated at the GICS secto |
| 1742 | `anl15_sal_s_fy3_cos_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of companies whose calendarized Fiscal Year 3 revenue (SAL) consensus has been raised since last month, aggregated at the GICS sector |
| 1743 | `anl15_sal_s_fy3_ests_dn` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates that have been lowered since last month within the GICS sector |
| 1744 | `anl15_sal_s_fy3_ests_up` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of calendarized fiscal year 3 revenue (sales) estimates that have been raised since last month within the GICS sector |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

