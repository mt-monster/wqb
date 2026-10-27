# predictive_starmine — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `predictive_starmine` |
| 名称 | Predictive Analyst-Company Signal Set |
| 类别 | MODEL |
| 数据字段数(平台) | 638 |
| 覆盖率 | 0.798 |
| 平台已有 alpha | 100 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides predictive signals specifically designed for advanced analyst and company relationship modeling, leveraging deep learning on company relations and analyst estimate data. It enhances traditional analyst revision and valuation models by integrating both company-to-company (Revere) and analyst-to-company (IBES) information, resulting in higher quality and broader coverage signals, especially for global equities. The dataset includes modules that generate forward-looking signals based on changes in analyst sentiment, earnings revisions, and valuation metrics, all informed by the underlying network of business relationships. These predictive signals can be used to anticipate future price movements by capturing both direct analyst actions and the economic linkages between c

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **638** |
| 类型分布 | MATRIX×638 |
| 平均覆盖率 | **0.798** |
| 覆盖率区间 | 0.41 ~ 0.97 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 273 | 42.8% |
| 中 (0.70–0.90) | 251 | 39.3% |
| 低 (0.50–0.70) | 86 | 13.5% |
| 稀疏 (<0.50) | 28 | 4.4% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 529 | 82.9% |
| UNUSABLE | 90 | 14.1% |
| DEAD | 8 | 1.3% |
| ALIVE | 5 | 0.8% |
| DEAD_STATIC | 4 | 0.6% |
| WEAK | 2 | 0.3% |

- 已实测字段：**19** 个（3%），best_sharpe 最高 **2.09**，中位 0.97
- ★ ALIVE（历史测出 S≥闸线）字段 **5** 个：`predicted_surprise_pct_f12m_revenue_4`(S 2.09)、`predicted_surprise_pct_f12m_earnings_5`(S 2.06)、`predicted_surprise_pct_f12m_ebitda_5`(S 1.91)、`predicted_surprise_fy1_earnings_4`(S 1.87)、`surprise_pct_last_quarter_earnings_4`(S 1.71)

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 413 | 0.79 | surprise_pct_last_year_earnings_3、surprise_pct_last_quarter_earnings_4、surprise_pct_last_year_ebitda_2 |
| 盈利与财务 | 168 | 0.80 | predicted_surprise_pct_f12m_revenue_4、predicted_surprise_pct_f12m_earnings_5、predicted_surprise_pct_f12m_ebitda_5 |
| 价量与波动 | 25 | 0.85 | rel_val_p_book_component_score_3、rel_val_p_book_component_score_31、price_to_intrinsic_value_ratio_3 |
| 宏观与行业 | 18 | 0.92 | iv_forward_5yr_eps_cagr_3、rel_val_region_rank_score_4、rel_val_region_rank_score_41 |
| 风险与质量 | 7 | 0.89 | rel_val_pe_component_score_31、rel_val_pe_component_score_3、rel_val_global_rank_score_3 |
| 其他 | 6 | 0.82 | iv_cagr_base_year_3、cagr_base_year_projection、eq_vr_dlra1_operating_efficiency_component_2 |
| 持仓与资金流 | 1 | 0.78 | eq_vr_dlra2_cashflow_component_change |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `predicted_surprise_pct_f12m_revenue_4` | MATRIX | 0.930 | 盈利与财务 | 15 | 2.09 | 1.55 | 1.29 | ALIVE | Predicted percentage revenue surprise over the next 12 months (F12M) |
| 2 | `predicted_surprise_pct_f12m_earnings_5` | MATRIX | 0.935 | 盈利与财务 | 18 | 2.06 | 2.07 | 1.32 | ALIVE | Predicted percentage surprise in net earnings over the forward 12 months |
| 3 | `predicted_surprise_pct_f12m_ebitda_5` | MATRIX | 0.897 | 盈利与财务 | 19 | 1.91 | 1.55 | 1.12 | ALIVE | Predicted percentage earnings surprise for EBITDA over the next 12 months |
| 4 | `predicted_surprise_fy1_earnings_4` | MATRIX | 0.937 | 盈利与财务 | 1 | 1.87 | — | — | ALIVE | Predicted earnings surprise for Fiscal Year 1 (absolute) |
| 5 | `surprise_pct_last_year_earnings_3` | MATRIX | 0.929 | 修正与预期 | 13 | 1.81 | 2.14 | 1.42 | WEAK | Percentage surprise in earnings for the last fiscal year reported compared to consensus |
| 6 | `surprise_pct_last_quarter_earnings_4` | MATRIX | 0.600 | 修正与预期 | 1 | 1.71 | — | — | ALIVE | Percentage surprise (actual minus estimated) in earnings for the most recent reported quarter |
| 7 | `surprise_pct_last_year_ebitda_2` | MATRIX | 0.876 | 修正与预期 | 2 | 1.70 | 2.05 | 1.30 | DEAD | Percentage surprise in EBITDA for the last fiscal year relative to prior estimates |
| 8 | `predicted_surprise_fq2_earnings_5` | MATRIX | 0.584 | 盈利与财务 | 1 | 1.51 | — | — | WEAK | StarMine predicted earnings surprise amount for fiscal quarter 2 |
| 9 | `actual_last_year_earnings_3` | MATRIX | 0.930 | 盈利与财务 | 2 | 1.39 | 1.22 | 1.30 | DEAD | Actual earnings reported for the last fiscal year |
| 10 | `eq_vr_dlra1_cashflow_component` | MATRIX | 0.772 | 盈利与财务 | 2 | 0.97 | 1.10 | — | DEAD_STATIC | Price to Free Cash Flow (P/FCF) ratio (relation-value adjusted) |
| 11 | `predicted_surprise_f12m_ebitda_4` | MATRIX | 0.897 | 盈利与财务 | 9 | 0.71 | — | — | DEAD | Predicted surprise in EBITDA over the next 12 months (F12M) |
| 12 | `eq_vr_dlra1_accruals_component` | MATRIX | 0.782 | 盈利与财务 | 3 | 0.52 | 0.28 | — | DEAD | Price to Book (P/B) ratio (relation-value adjusted) |
| 13 | `smest_f12m_earnings_5` | MATRIX | 0.935 | 修正与预期 | 2 | 0.47 | -0.18 | — | DEAD | SmartEstimate of earnings for the next 12 months (F12M) |
| 14 | `smest_f12m_ebitda_5` | MATRIX | 0.897 | 修正与预期 | 1 | 0.41 | 0.39 | — | DEAD_STATIC | SmartEstimate of EBITDA for the next 12 months |
| 15 | `iv_forward_5yr_eps_cagr_3` | MATRIX | 0.912 | 宏观与行业 | 1 | 0.31 | -0.90 | — | DEAD_STATIC | Compound annual growth rate of EPS from current to Year 5 projected by SmartGrowth |
| 16 | `smest_f12m_revenue_4` | MATRIX | 0.930 | 修正与预期 | 1 | 0.27 | 0.01 | — | DEAD_STATIC | SmartEstimate of revenue for the next 12 months (F12M) |
| 17 | `iv_cagr_base_year_3` | MATRIX | 0.912 | 其他 | 3 | 0.18 | -0.28 | — | DEAD | Base year used for CAGR calculations in the intrinsic value model |
| 18 | `eq_vr_dlra1_accruals_component_change` | MATRIX | 0.726 | 盈利与财务 | 2 | -0.07 | -0.13 | — | DEAD | Price to Book (P/B) ratio quarter-over-quarter change (level difference), 1 quarter difference (relation-value adjusted) |
| 19 | `eq_vr_dlra2_accruals_component` | MATRIX | 0.782 | 盈利与财务 | 1 | -0.11 | -1.08 | — | DEAD | Price/Book |
| 20 | `rel_val_pe_component_score_31` | MATRIX | 0.972 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for P/E component |
| 21 | `rel_val_pe_component_score_3` | MATRIX | 0.971 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the P/E component in the Relative Valuation model |
| 22 | `rel_val_p_book_component_score_3` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the Price-to-Book component of the Relative Valuation model |
| 23 | `rel_val_p_book_component_score_31` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (floating point) of the Price-to-Book component in the relative valuation model |
| 24 | `rel_val_global_rank_score_3` | MATRIX | 0.970 | 风险与质量 | 0 | — | — | — | UNTESTED | Current overall percentile rank (floating-point) in the Relative Valuation model |
| 25 | `rel_val_global_rank_score_31` | MATRIX | 0.970 | 风险与质量 | 0 | — | — | — | UNTESTED | Current percentile rank (floating-point) in the overall Relative Valuation Model |
| 26 | `rel_val_region_rank_score_4` | MATRIX | 0.970 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region-relative percentile rank (floating-point) in the Relative Valuation model |
| 27 | `rel_val_region_rank_score_41` | MATRIX | 0.970 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current regional percentile rank (floating-point) in the Relative Valuation Model |
| 28 | `iv_projected_dividends_fy1_3` | MATRIX | 0.969 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 1 dividends per share estimate (DPS) |
| 29 | `projected_dividends_fy1_3` | MATRIX | 0.969 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 1 |
| 30 | `rel_val_sector_rank_score_3` | MATRIX | 0.969 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-relative percentile rank (floating-point) in the Relative Valuation model |
| 31 | `rel_val_sector_rank_score_31` | MATRIX | 0.969 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector percentile rank (floating-point) within the Relative Valuation model |
| 32 | `rel_val_industry_rank_score_3` | MATRIX | 0.963 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-relative percentile rank (floating-point) in the Relative Valuation model |
| 33 | `rel_val_industry_rank_score_31` | MATRIX | 0.963 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry percentile rank (floating-point) in the Relative Valuation Model |
| 34 | `rel_val_buyback_yield_component_score_3` | MATRIX | 0.959 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the buyback yield component in the Relative Valuation model |
| 35 | `rel_val_buyback_yield_component_score_31` | MATRIX | 0.959 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the Buyback Yield component in the Relative Valuation model |
| 36 | `analyst_downgrade_count_14d_2` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst rating downgrades aggregated over the last 14 days |
| 37 | `analyst_downgrade_count_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst downgrades over the last 30 days |
| 38 | `analyst_downgrade_count_60d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 60 days |
| 39 | `analyst_downgrade_count_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 7 days |
| 40 | `analyst_downgrade_count_90d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 90 days |
| 41 | `analyst_downward_revision_count_fq1_earnings_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised earnings estimates downward for fiscal quarter 1 over the last 14 days |
| 42 | `analyst_downward_revision_count_fq1_earnings_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for fiscal quarter 1, aggregated over the last 30 days |
| 43 | `analyst_downward_revision_count_fq1_earnings_7d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised earnings estimates downward for fiscal quarter 1 over the last 7 days |
| 44 | `analyst_downward_revision_count_fq1_ebitda_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their FQ1 EBITDA estimates downward over the last 14 days |
| 45 | `analyst_downward_revision_count_fq1_ebitda_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their EBITDA estimates for fiscal quarter 1 over the last 30 days |
| 46 | `analyst_downward_revision_count_fq1_revenue_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their revenue estimates for fiscal quarter 1, aggregated over the last 14 days |
| 47 | `analyst_downward_revision_count_fq1_revenue_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their revenue estimates for fiscal quarter 1 over the last 30 days |
| 48 | `analyst_downward_revision_count_fq1_revenue_7d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their revenue estimates for fiscal quarter 1 over the last 7 days |
| 49 | `analyst_downward_revision_count_fq2_earnings_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their earnings estimates for Fiscal Quarter 2, aggregated over the last 14 days |
| 50 | `analyst_downward_revision_count_fq2_earnings_30d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their earnings estimates for fiscal quarter 2 over the last 30 days |
| 51 | `analyst_downward_revision_count_fq2_ebitda_30d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising their EBITDA estimates downward for fiscal quarter 2 over the last 30 days |
| 52 | `analyst_downward_revision_count_fq2_revenue_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their FQ2 revenue estimates over the last 14 days |
| 53 | `analyst_downward_revision_count_fq2_revenue_30d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their revenue estimates for fiscal quarter 2, aggregated over the last 30 days |
| 54 | `analyst_downward_revision_count_fy1_earnings_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their FY1 earnings estimates over the last 14 days |
| 55 | `analyst_downward_revision_count_fy1_earnings_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates downward for fiscal year 1, aggregated over the last 30 days |
| 56 | `analyst_downward_revision_count_fy1_earnings_7d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for fiscal year 1, aggregated over the last 7 days |
| 57 | `analyst_downward_revision_count_fy1_ebitda_14d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their FY1 EBITDA estimates over the last 14 days |
| 58 | `analyst_downward_revision_count_fy1_ebitda_30d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised EBITDA estimates downward for fiscal year 1 over the last 30 days |
| 59 | `analyst_downward_revision_count_fy1_ebitda_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down EBITDA estimates for fiscal year 1, aggregated over the last 7 days |
| 60 | `analyst_downward_revision_count_fy1_revenue_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their fiscal year 1 revenue estimates downward over the last 14 days |
| 61 | `analyst_downward_revision_count_fy1_revenue_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down revenue estimates for fiscal year 1 over the last 30 days |
| 62 | `analyst_downward_revision_count_fy1_revenue_7d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their FY1 revenue estimates over the last 7 days |
| 63 | `analyst_upgrade_count_14d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst upgrades over the last 14 days |
| 64 | `analyst_upgrade_count_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the last 30 days |
| 65 | `analyst_upgrade_count_60d_2` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the last 60 days |
| 66 | `analyst_upgrade_count_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the last 7 days |
| 67 | `analyst_upgrade_count_90d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst upgrades over the last 90 days |
| 68 | `analyst_upward_revision_count_fq1_earnings_14d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ1 earnings estimates over the last 14 days |
| 69 | `analyst_upward_revision_count_fq1_earnings_30d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their earnings estimates upward for fiscal quarter 1 over the last 30 days |
| 70 | `analyst_upward_revision_count_fq1_ebitda_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates upward for fiscal quarter 1, aggregated over the last 14 days |
| 71 | `analyst_upward_revision_count_fq1_ebitda_30d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ1 EBITDA estimates over the last 30 days |
| 72 | `analyst_upward_revision_count_fq1_revenue_14d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upward for fiscal quarter 1 over the last 14 days |
| 73 | `analyst_upward_revision_count_fq1_revenue_30d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for fiscal quarter 1, aggregated over the last 30 days |
| 74 | `analyst_upward_revision_count_fq1_revenue_7d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimate for fiscal quarter 1 over the last 7 days |
| 75 | `analyst_upward_revision_count_fq2_earnings_14d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ2 earnings estimates over the last 14 days |
| 76 | `analyst_upward_revision_count_fq2_earnings_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ2 earnings estimates over the last 30 days |
| 77 | `analyst_upward_revision_count_fq2_ebitda_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for fiscal quarter 2, aggregated over the last 30 days |
| 78 | `analyst_upward_revision_count_fq2_revenue_14d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upwards for fiscal quarter 2, aggregated over the last 14 days |
| 79 | `analyst_upward_revision_count_fq2_revenue_30d_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upward for fiscal quarter 2 over the last 30 days |
| 80 | `analyst_upward_revision_count_fy1_earnings_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upwards for Fiscal Year 1, aggregated over the last 14 days |
| 81 | `analyst_upward_revision_count_fy1_earnings_30d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FY1 earnings estimates over the last 30 days |
| 82 | `analyst_upward_revision_count_fy1_earnings_7d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for fiscal year 1, aggregated over the last 7 days |
| 83 | `analyst_upward_revision_count_fy1_ebitda_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimate for fiscal year 1 over the last 14 days |
| 84 | `analyst_upward_revision_count_fy1_ebitda_30d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimate for fiscal year 1 over the last 30 days |
| 85 | `analyst_upward_revision_count_fy1_ebitda_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates upward for fiscal year 1 over the last 7 days |
| 86 | `analyst_upward_revision_count_fy1_revenue_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FY1 revenue estimates over the last 14 days |
| 87 | `analyst_upward_revision_count_fy1_revenue_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upward for fiscal year 1 over the last 30 days |
| 88 | `analyst_upward_revision_count_fy1_revenue_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upwards for fiscal year 1, aggregated over the last 7 days |
| 89 | `analyst_upward_revision_count_fy2_earnings_14d_5` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised earnings estimates upward for fiscal year 2 over the last 14 days |
| 90 | `analyst_upward_revision_count_fy2_earnings_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their earnings estimates upward for fiscal year 2 (FY2) over the last 30 days |
| 91 | `analyst_upward_revision_count_fy2_earnings_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upward for fiscal year 2 over the last 7 days |
| 92 | `analyst_upward_revision_count_fy2_ebitda_14d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates upward for fiscal year 2 over the last 14 days |
| 93 | `analyst_upward_revision_count_fy2_ebitda_30d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their EBITDA estimates upward for fiscal year 2 over the last 30 days |
| 94 | `analyst_upward_revision_count_fy2_ebitda_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates upward for fiscal year 2 over the last 7 days |
| 95 | `analyst_upward_revision_count_fy2_revenue_14d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FY2 revenue estimates over the last 14 days |
| 96 | `analyst_upward_revision_count_fy2_revenue_30d` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for fiscal year 2, aggregated over the last 30 days |
| 97 | `analyst_upward_revision_count_fy2_revenue_7d_4` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upwards for fiscal year 2, aggregated over the last 7 days |
| 98 | `arm_new_activity_flag_2` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating new activity detected by the Analyst Revisions Model (ARM) |
| 99 | `days_since_last_report_3` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of days since the last analyst report |
| 100 | `mean_estimate_change_pct_fy1_earnings_7d_4` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal year 1 over the last 7 days |
| 101 | `analyst_revisions_score_2` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Overall score from the Analyst Revisions Model (ARM) |
| 102 | `arm_country_rank_score_3` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model country rank represented as a floating-point value |
| 103 | `arm_global_rank_score` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model global percentile rank expressed as a floating-point value |
| 104 | `arm_preferred_earnings_component_score` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Preferred earnings revisions component score in the Analyst Revisions Model, expressed as a floating point value |
| 105 | `arm_region_rank_decimal_2` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Decimal regional rank in the Analyst Revisions Model |
| 106 | `arm_score_5pt_scale_2` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model (ARM) score representing 5-day change |
| 107 | `mean_estimate_change_pct_fy1_earnings_14d_5` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal year 1 over the last 14 days |
| 108 | `arm_score_change_1d_2` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model (ARM) score over the last 1 day |
| 109 | `arm_score_change_3d_21` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model (ARM) score over the last 3 days |
| 110 | `arm_score_change_7d_3` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model (ARM) score over the last 7 days |
| 111 | `mean_estimate_change_pct_fy1_earnings_30d_4` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for fiscal year 1 (FY1), aggregated over the last 30 days |
| 112 | `mean_estimate_change_pct_f12m_earnings_7d_4` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for the next 12 months (F12M), aggregated over the last 7 days |
| 113 | `arm_score_change_30d_4` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the Analyst Revisions Model (ARM) score over the last 30 days |
| 114 | `mean_estimate_change_pct_f12m_earnings_14d_4` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for the next 12 months (F12M) over the last 14 days |
| 115 | `mean_estimate_change_pct_fy1_earnings_60d_4` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for fiscal year 1 (FY1), aggregated over the last 60 days |
| 116 | `mean_estimate_change_pct_f12m_earnings_30d_5` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for the forward 12 months, aggregated over the last 30 days |
| 117 | `mean_estimate_change_pct_fy1_revenue_7d_5` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimate for fiscal year 1, aggregated over the last 7 days |
| 118 | `mean_estimate_change_pct_fy1_revenue_14d_5` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal year 1 over the last 14 days |
| 119 | `recommendation_mean_change_7d_2` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 7 days |
| 120 | `recommendation_mean_change_14d_2` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 14 days |
| 121 | `arm_score_change_60d_3` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model score over the last 60 days |
| 122 | `mean_estimate_change_pct_fy1_revenue_30d_5` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal year 1 over the last 30 days |
| 123 | `arm_revenue_component_score_3` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Revenue component of the Analyst Revisions Model expressed as a float |
| 124 | `recommendation_mean_change_30d_5` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 30 days |
| 125 | `mean_estimate_change_pct_f12m_earnings_60d_4` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for the next 12 months over the last 60 days |
| 126 | `mean_estimate_change_pct_fy1_earnings_90d_3` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal year 1 over the last 90 days |
| 127 | `mean_estimate_change_pct_f12m_revenue_7d_4` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the next 12 months over the last 7 days |
| 128 | `mean_estimate_change_pct_f12m_revenue_14d` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean revenue estimate for the next 12 months (F12M), aggregated over the last 14 days |
| 129 | `mean_estimate_change_pct_fy1_revenue_60d_4` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal year 1 over the last 60 days |
| 130 | `mean_estimate_change_pct_f12m_revenue_30d_5` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean revenue estimate for the next 12 months over the last 30 days |
| 131 | `recommendation_mean_change_60d_2` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 60 days |
| 132 | `mean_estimate_price_ratio_f12m_revenue_5` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price to revenue ratio for the next 12 months (F12M) |
| 133 | `arm_score_change_90d_3` | MATRIX | 0.939 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the Analyst Revisions Model (ARM) score over the last 90 days |
| 134 | `mean_estimate_change_pct_f12m_earnings_90d` | MATRIX | 0.939 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for the next 12 months (F12M) over the last 90 days |
| 135 | `mean_estimate_price_ratio_fy1_revenue_5` | MATRIX | 0.939 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-revenue ratio for fiscal year 1 (FY1) |
| 136 | `ep_yield_pct_smest_f12m` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on SmartEstimate for the next 12 months (F12M) |
| 137 | `mean_estimate_change_pct_f12m_revenue_60d_4` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean revenue estimate for the next 12 months (F12M), aggregated over the last 60 days |
| 138 | `mean_estimate_change_pct_fy1_revenue_90d_5` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimate for fiscal year plus 1, aggregated over the last 90 days |
| 139 | `mean_estimate_price_ratio_fy2_revenue_4` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-revenue ratio for fiscal year 2 (FY2) |
| 140 | `recommendation_mean_change_90d_2` | MATRIX | 0.938 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 90 days |
| 141 | `predicted_surprise_pct_fy1_earnings_5` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for fiscal year 1 (FY1) |
| 142 | `smest_fy1_earnings_4` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of earnings for FY1 |
| 143 | `predicted_surprise_fy2_earnings_4` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for Fiscal Year 2 (absolute) |
| 144 | `predicted_surprise_pct_fy2_earnings_4` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for fiscal year 2 (FY2) |
| 145 | `smest_fy2_earnings_4` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of earnings for fiscal year 2 |
| 146 | `ep_yield_pct_smest_fy1_3` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on the SmartEstimate for FY1 |
| 147 | `ep_yield_pct_smest_fy2_3` | MATRIX | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on SmartEstimate for fiscal year 2 (FY2) |
| 148 | `mean_estimate_change_pct_f12m_revenue_90d_5` | MATRIX | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the forward 12 months, aggregated over the last 90 days |
| 149 | `arm_recommendations_component_score_3` | MATRIX | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Floating-point component score for analyst recommendations within the Analyst Revisions Model (ARM) |
| 150 | `predicted_surprise_f12m_earnings_5` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for the next 12 months |
| 151 | `predicted_surprise_fy2_revenue_3` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted revenue surprise for fiscal year 2 |
| 152 | `predicted_surprise_pct_fy2_revenue_4` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted revenue surprise for fiscal year 2 (FY2), expressed as a percentage |
| 153 | `smest_fy2_revenue_3` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of revenue for fiscal year 2 |
| 154 | `actual_last_year_revenue_2` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual revenue reported for the most recently completed fiscal year |
| 155 | `smest_price_ratio_f12m_revenue_5` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-revenue ratio for the next 12 months (F12M) |
| 156 | `predicted_surprise_fy1_revenue_4` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise in revenue for fiscal year 1 (FY1) |
| 157 | `predicted_surprise_pct_fy1_revenue_4` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage revenue surprise for fiscal year 1 |
| 158 | `smest_fy1_revenue` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of revenue for fiscal year 1 |
| 159 | `smest_price_ratio_fy2_revenue_3` | MATRIX | 0.930 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-revenue ratio for fiscal year 2 (FY2) |
| 160 | `predicted_surprise_f12m_revenue_4` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise in revenue over the next 12 months (F12M) |
| 161 | `smest_price_ratio_fy1_revenue_4` | MATRIX | 0.930 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate-based price-to-revenue ratio for fiscal year 1 (FY1) |
| 162 | `forward_pe_mean_fy2_3` | MATRIX | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean forward price-to-earnings ratio estimate for fiscal year 2 |
| 163 | `mean_estimate_price_ratio_fy2_earnings_4` | MATRIX | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price to earnings ratio for fiscal year 2 (FY2) |
| 164 | `smest_growth_next_vs_this_yr_revenue_4` | MATRIX | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth ratio of revenue for next fiscal year compared to this fiscal year |
| 165 | `surprise_pct_last_year_revenue_4` | MATRIX | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise in revenue for the last year actual versus estimated |
| 166 | `forward_pe_mean_f12m_4` | MATRIX | 0.928 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on mean estimates for the next 12 months |
| 167 | `mean_estimate_price_ratio_f12m_earnings_5` | MATRIX | 0.928 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-earnings ratio over the next 12 months |
| 168 | `forward_pe_smest_fy2` | MATRIX | 0.923 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on SmartEstimate for fiscal year 2 (FY2) |
| 169 | `smest_price_ratio_fy2_earnings_4` | MATRIX | 0.923 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate-based price-to-earnings ratio for fiscal year 2 (FY2) |
| 170 | `forward_pe_smest_f12m_4` | MATRIX | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on SmartEstimate for the next 12 months |
| 171 | `smest_price_ratio_f12m_earnings_4` | MATRIX | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-earnings ratio for the forward 12 months |
| 172 | `forward_pe_mean_fy1_3` | MATRIX | 0.921 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on mean FY1 earnings estimates |
| 173 | `mean_estimate_price_ratio_fy1_earnings_4` | MATRIX | 0.921 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price to earnings ratio for fiscal year 1 (FY1) |
| 174 | `smest_growth_this_vs_last_yr_revenue_3` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate of revenue comparing this year to last year |
| 175 | `forward_pe_smest_fy1_3` | MATRIX | 0.914 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on the StarMine SmartEstimate for FY1 |
| 176 | `smest_price_ratio_fy1_earnings_4` | MATRIX | 0.914 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-earnings ratio for fiscal year 1 (FY1) |
| 177 | `smest_growth_next_vs_this_yr_earnings_5` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth comparing next fiscal year’s earnings to this fiscal year’s earnings |
| 178 | `intrinsic_valuation_discount_rate` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Discount rate used in the intrinsic valuation model |
| 179 | `intrinsic_value_projection_currency_3` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | The intrinsic value calculated in a specified projection currency |
| 180 | `intrinsic_value_projection_currency_4` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Intrinsic value calculated in the specified projection currency |
| 181 | `iv_discount_rate_3` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Discount rate used in the valuation model |
| 182 | `iv_projected_dividends_fy10_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 10 dividends per share estimate (DPS) |
| 183 | `iv_projected_dividends_fy11_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 11 dividends per share estimate (DPS) |
| 184 | `iv_projected_dividends_fy12_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 12 dividends per share estimate (DPS) |
| 185 | `iv_projected_dividends_fy13` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 13 dividends per share estimate (DPS) |
| 186 | `iv_projected_dividends_fy13_2` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 13 |
| 187 | `iv_projected_dividends_fy14` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 14 dividends per share estimate (DPS) |
| 188 | `iv_projected_dividends_fy15_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 15 dividends per share estimate (DPS) |
| 189 | `iv_projected_dividends_fy2_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected dividends per share (DPS) for fiscal year 2 |
| 190 | `iv_projected_dividends_fy3_2` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 3 dividends per share estimate (DPS) |
| 191 | `iv_projected_dividends_fy4_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 4 dividends per share estimate (DPS) |
| 192 | `iv_projected_dividends_fy5_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 5 dividends per share estimate (DPS) |
| 193 | `iv_projected_dividends_fy5_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 5 |
| 194 | `iv_projected_dividends_fy6_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 6 dividends per share estimate (DPS) |
| 195 | `iv_projected_dividends_fy7_2` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 7 dividends per share estimate (DPS) |
| 196 | `iv_projected_dividends_fy8_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 8 dividends per share estimate (DPS) |
| 197 | `iv_projected_dividends_fy8_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 8 |
| 198 | `iv_projected_dividends_fy9_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 9 dividends per share estimate (DPS) |
| 199 | `iv_projected_dividends_fy9_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 9 |
| 200 | `iv_projected_earnings_fy10_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for FY10 |
| 201 | `iv_projected_earnings_fy11_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for FY11 |
| 202 | `iv_projected_earnings_fy11_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 11 used in the intrinsic value model |
| 203 | `iv_projected_earnings_fy12_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for FY12 |
| 204 | `iv_projected_earnings_fy12_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted EPS projection for fiscal year 12 |
| 205 | `iv_projected_earnings_fy13_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings per share (EPS) projection for fiscal year 13 |
| 206 | `iv_projected_earnings_fy14_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected earnings per share for fiscal year 14 used in the intrinsic value model |
| 207 | `iv_projected_earnings_fy15_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected EPS for fiscal year 15 used in the intrinsic value model |
| 208 | `iv_projected_earnings_fy15_5` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 15 used in the intrinsic value model |
| 209 | `iv_projected_earnings_fy1_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings per share (EPS) projection for fiscal year 1 |
| 210 | `iv_projected_earnings_fy1_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 1 used in the intrinsic value model |
| 211 | `iv_projected_earnings_fy2_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings per share (EPS) projection for fiscal year 2 |
| 212 | `iv_projected_earnings_fy3_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected earnings per share for fiscal year 3 used in the intrinsic value model |
| 213 | `iv_projected_earnings_fy4_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for FY4 |
| 214 | `iv_projected_earnings_fy5_2` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings per share (EPS) projection for fiscal year 5 |
| 215 | `iv_projected_earnings_fy6_2` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for FY6 |
| 216 | `iv_projected_earnings_fy7_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected earnings per share for fiscal year 7 used in the intrinsic value model |
| 217 | `iv_projected_earnings_fy7_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 7 used in the intrinsic value model |
| 218 | `iv_projected_earnings_fy8_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings per share (EPS) projection for fiscal year 8 |
| 219 | `iv_projected_earnings_fy9_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected EPS for fiscal year 9 used in the intrinsic value model |
| 220 | `iv_projected_earnings_fy9_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted EPS projection for fiscal year 9 |
| 221 | `iv_steady_state_dividend_payout_rate_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend payout rate at steady state |
| 222 | `iv_steady_state_growth_earnings_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of earnings at steady state |
| 223 | `iv_steady_state_year_dividends_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year in which dividends reach steady state in the model |
| 224 | `iv_steady_state_year_dividends_4` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year in which the company reaches steady-state dividends in the projection |
| 225 | `iv_steady_state_year_earnings_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year in which earnings growth reaches steady state in the model |
| 226 | `projected_dividends_fy10` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted dividends per share for fiscal year 10 in the intrinsic value model. |
| 227 | `projected_dividends_fy10_dlr1` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 10 |
| 228 | `projected_dividends_fy11` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted dividends per share for fiscal year 11 in the intrinsic value model. |
| 229 | `projected_dividends_fy11_dlr1` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 11 |
| 230 | `projected_dividends_fy12` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted dividends per share for fiscal year 12 in the intrinsic value model. |
| 231 | `projected_dividends_fy12_dlr1` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 12 dividends per share estimate (DPS) |
| 232 | `projected_dividends_fy14_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 14 |
| 233 | `projected_dividends_fy15_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 15 |
| 234 | `projected_dividends_fy2_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 2 |
| 235 | `projected_dividends_fy3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted dividends per share for fiscal year 3 in the intrinsic value model. |
| 236 | `projected_dividends_fy3_dlr1` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 3 dividends per share estimate (DPS) |
| 237 | `projected_dividends_fy4_3` | MATRIX | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 4 dividends per share estimate (DPS) |
| 238 | `projected_dividends_fy6_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 6 |
| 239 | `projected_dividends_fy7_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share (DPS) projection for fiscal year 7 |
| 240 | `projected_earnings_fy10_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 10 used in the intrinsic value model |
| 241 | `projected_earnings_fy13_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted EPS projection for fiscal year 13 |
| 242 | `projected_earnings_fy14` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted earnings per share for fiscal year 14 in the intrinsic value model. |
| 243 | `projected_earnings_fy14_dlr1` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted EPS projection for fiscal year 14 |
| 244 | `projected_earnings_fy2` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted earnings per share for fiscal year 2 in the intrinsic value model. |
| 245 | `projected_earnings_fy2_dlr1` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 2 used in the intrinsic value model |
| 246 | `projected_earnings_fy3_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 3 used in the intrinsic value model |
| 247 | `projected_earnings_fy4_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 4 used in the intrinsic value model |
| 248 | `projected_earnings_fy5_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 5 used in the intrinsic value model |
| 249 | `projected_earnings_fy6_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted earnings projection for fiscal year 6 used in the intrinsic value model |
| 250 | `projected_earnings_fy8_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted EPS projection for fiscal year 8 |
| 251 | `steady_state_annual_earnings_projection` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year in which the company reaches steady-state earnings growth in the projection |
| 252 | `steady_state_dividend_payout_ratio` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assumed dividend payout rate at steady state |
| 253 | `steady_state_earnings_growth_rate` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assumed earnings growth rate at steady state |
| 254 | `cagr_base_year_projection` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | Base year used for the CAGR calculations in the intrinsic value model |
| 255 | `forward_10yr_eps_cagr_projection` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Forward 10-year EPS compound annual growth rate from SmartGrowth |
| 256 | `forward_5yr_eps_cagr_projection` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate of EPS from current to year 5 projected by the SmartGrowth model |
| 257 | `iv_forward_10yr_eps_cagr_3` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Projected 10-year forward EPS compound annual growth rate from the SmartGrowth model |
| 258 | `iv_warranted_f12m_pe_3` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Warranted forward 12-month price-to-earnings (P/E) ratio |
| 259 | `price_to_intrinsic_value_ratio_3` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Intrinsic Value ratio |
| 260 | `price_to_intrinsic_value_region_rank_3` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Intrinsic Value Region Rank as float |
| 261 | `warranted_forward_pe_ratio` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Warranted forward 12-month price-to-earnings ratio |
| 262 | `price_to_intrinsic_value_ratio_2` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Intrinsic Value ratio |
| 263 | `price_to_intrinsic_value_region_rank_4` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Region-relative percentile rank (floating-point) of the Price to Intrinsic Value ratio |
| 264 | `price_to_intrinsic_value_sector_rank_2` | MATRIX | 0.911 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (floating point) of the price-to-intrinsic-value ratio within the sector |
| 265 | `price_to_intrinsic_value_sector_rank_4` | MATRIX | 0.911 | 价量与波动 | 0 | — | — | — | UNTESTED | Sector-relative percentile rank (floating-point) of the price to intrinsic value ratio |
| 266 | `iv_market_implied_10yr_eps_cagr_3` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Market-implied compound annual growth rate of EPS over 10 years based on current market price |
| 267 | `iv_market_implied_10yr_eps_cagr_4` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Market-implied compound annual growth rate of EPS over 10 years based on current price |
| 268 | `iv_market_implied_5yr_eps_cagr_3` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Market-implied compound annual growth rate of EPS over 5 years based on current market price |
| 269 | `market_implied_5yr_eps_cagr` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | Compound annual growth rate for earnings per share over five years implied by the current market price. |
| 270 | `market_implied_5yr_eps_cagr_dlr1` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Market-implied 5-year EPS compound annual growth rate based on current price |
| 271 | `mean_estimate_change_pct_fy1_ebitda_7d_4` | MATRIX | 0.909 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean FY1 EBITDA estimate over the last 7 days |
| 272 | `mean_estimate_change_pct_fy1_ebitda_14d_5` | MATRIX | 0.908 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean EBITDA estimate for fiscal year 1, aggregated over the last 14 days |
| 273 | `arm_secondary_earnings_component_score_3` | MATRIX | 0.908 | 修正与预期 | 0 | — | — | — | UNTESTED | Secondary earnings component in the Analyst Revisions Model (floating point value) |
| 274 | `mean_estimate_change_pct_fy1_ebitda_30d_4` | MATRIX | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean FY1 EBITDA estimate over the last 30 days |
| 275 | `mean_estimate_change_pct_f12m_ebitda_7d_4` | MATRIX | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean EBITDA estimate over the next 12 months (F12M), aggregated over the last 7 days |
| 276 | `mean_estimate_change_pct_f12m_ebitda_14d_4` | MATRIX | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the forward 12 months, aggregated over the last 14 days |
| 277 | `mean_estimate_change_pct_fy1_ebitda_60d` | MATRIX | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean FY1 EBITDA estimate over the last 60 days |
| 278 | `mean_estimate_change_pct_f12m_ebitda_30d_4` | MATRIX | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean EBITDA estimate over the next 12 months (F12M), aggregated over the last 30 days |
| 279 | `mean_estimate_change_pct_f12m_ebitda_60d_4` | MATRIX | 0.903 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months over the last 60 days |
| 280 | `mean_estimate_change_pct_fy1_ebitda_90d_3` | MATRIX | 0.903 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean EBITDA estimate for fiscal year 1 (FY1), aggregated over the last 90 days |
| 281 | `rel_val_dividend_yield_component_score_31` | MATRIX | 0.903 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for Dividend Yield component |
| 282 | `rel_val_dividend_yield_component_score_3` | MATRIX | 0.903 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the Dividend Yield component of the Relative Valuation model |
| 283 | `mean_estimate_change_pct_f12m_ebitda_90d_3` | MATRIX | 0.901 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months over the last 90 days |
| 284 | `predicted_surprise_fy1_ebitda_4` | MATRIX | 0.900 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise in EBITDA for fiscal year 1 |
| 285 | `predicted_surprise_pct_fy1_ebitda` | MATRIX | 0.900 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for EBITDA in fiscal year 1 |
| 286 | `smest_fy1_ebitda_4` | MATRIX | 0.900 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of EBITDA for fiscal year 1 |
| 287 | `predicted_surprise_fy2_ebitda_5` | MATRIX | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted EBITDA surprise for fiscal year 2 |
| 288 | `predicted_surprise_pct_fy2_ebitda_4` | MATRIX | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted EBITDA surprise for fiscal year 2 (FY2), expressed as a percentage |
| 289 | `smest_fy2_ebitda_4` | MATRIX | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of EBITDA for fiscal year 2 |
| 290 | `mean_estimate_price_ratio_f12m_ebitda_4` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price to EBITDA ratio for the next 12 months (F12M) |
| 291 | `mean_estimate_price_ratio_fy2_ebitda_4` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-EBITDA ratio for fiscal year 2 |
| 292 | `trailing_pe_last_fiscal_year_2` | MATRIX | 0.896 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-Earnings ratio for the last fiscal year |
| 293 | `mean_estimate_price_ratio_fy1_ebitda_5` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-EBITDA ratio for Fiscal Year 1 |
| 294 | `smest_growth_this_vs_last_yr_earnings_2` | MATRIX | 0.890 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth comparing this year to last year for earnings |
| 295 | `smest_price_ratio_f12m_ebitda_4` | MATRIX | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Price to EBITDA ratio for the next 12 months based on SmartEstimate |
| 296 | `smest_price_ratio_fy2_ebitda_6` | MATRIX | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-EBITDA ratio for fiscal year 2 |
| 297 | `smest_price_ratio_fy1_ebitda_6` | MATRIX | 0.884 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-EBITDA ratio for fiscal year 1 (FY1) |
| 298 | `smest_growth_next_vs_this_yr_ebitda_5` | MATRIX | 0.882 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth comparing next year to this year for EBITDA |
| 299 | `actual_last_year_ebitda_2` | MATRIX | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual EBITDA reported for the last fiscal year |
| 300 | `rel_val_ev_ebitda_component_score_3` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the EV/EBITDA component of the Relative Valuation model |
| 301 | `rel_val_ev_ebitda_component_score_31` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for EV/EBITDA component |
| 302 | `smest_growth_this_vs_last_yr_ebitda_4` | MATRIX | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth comparing this year’s EBITDA to last year’s EBITDA |
| 303 | `price_to_intrinsic_value_industry_rank_3` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry percentile rank (floating-point) of Price to Intrinsic Value |
| 304 | `price_to_intrinsic_value_industry_rank_4` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative percentile rank (floating-point) of Price to Intrinsic Value |
| 305 | `rel_val_ev_sales_component_score_3` | MATRIX | 0.799 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the EV/Sales component of the Relative Valuation model |
| 306 | `rel_val_ev_sales_component_score_31` | MATRIX | 0.799 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for EV/Sales component |
| 307 | `rel_val_p_cf_component_score_3` | MATRIX | 0.798 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for the Price-to-Cash-Flow component of the Relative Valuation model |
| 308 | `rel_val_p_cf_component_score_31` | MATRIX | 0.798 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for Price/Cash Flow component |
| 309 | `eq_vr_dlra1_operating_efficiency_component_2` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Enterprise Value (EV) (relation-value adjusted) |
| 310 | `eq_vr_dlra2_operating_efficiency_component` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Enterprise Value (EV) |
| 311 | `eq_vr_dlra3_v13` | MATRIX | 0.782 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v13 from the third version of the enhanced earnings quality and valuation mo |
| 312 | `eq_vr_dlra3_new_region_rank` | MATRIX | 0.782 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile ranking of the combined earnings quality and valuation score relative to all companies in the same region. |
| 313 | `eq_vr_dlra1_operating_efficiency_component` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Sales (P/S) ratio (relation-value adjusted) |
| 314 | `eq_vr_dlra1_region_rank_change` | MATRIX | 0.782 | 宏观与行业 | 0 | — | — | — | UNTESTED | Enterprise Value to Sales (EV/Sales) ratio (relation-value adjusted) |
| 315 | `eq_vr_dlra2_v16` | MATRIX | 0.782 | 其他 | 0 | — | — | — | UNTESTED | EV/Sales |
| 316 | `eq_vr_dlra2_v8` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Sales |
| 317 | `eq_vr_dlra3_v8` | MATRIX | 0.782 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v8 from the third version of the enhanced earnings quality and valuation mod |
| 318 | `eq_vr_dlra3_v16` | MATRIX | 0.781 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v16 from the third version of the enhanced earnings quality and valuation mo |
| 319 | `eq_vr_dlra1_cashflow_component_change_2` | MATRIX | 0.781 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow Yield (%) (relation-value adjusted) |
| 320 | `eq_vr_dlra2_cashflow_component_change` | MATRIX | 0.781 | 持仓与资金流 | 0 | — | — | — | UNTESTED | FCF Yield (%) |
| 321 | `eq_vr_dlra3_v17` | MATRIX | 0.781 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v17 from the third version of the enhanced earnings quality and valuation mo |
| 322 | `eq_vr_dlra1_exclusions_component` | MATRIX | 0.780 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Sales ratio year-over-year change (%), 1 fiscal year difference (relation-value adjusted) |
| 323 | `eq_vr_dlra1_region_rank` | MATRIX | 0.780 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Sales (P/S) ratio year-over-year change (level difference), 1 fiscal year difference (relation-value adjusted) |
| 324 | `eq_vr_dlra2_exclusions_component` | MATRIX | 0.780 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Sales - 1 FY Difference (%) |
| 325 | `eq_vr_dlra2_region_rank` | MATRIX | 0.780 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Sales - 1 FY Difference |
| 326 | `eq_vr_dlra3_v10` | MATRIX | 0.780 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v10 from the third version of the enhanced earnings quality and valuation mo |
| 327 | `eq_vr_dlra3_v9` | MATRIX | 0.780 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v9 from the third version of the enhanced earnings quality and valuation mod |
| 328 | `eq_vr_dlra1_cashflow_component_change` | MATRIX | 0.780 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow to Enterprise Value (%) (relation-value adjusted) |
| 329 | `eq_vr_dlra1_score` | MATRIX | 0.780 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow from Operations to Enterprise Value (%) (relation-value adjusted) |
| 330 | `eq_vr_dlra2_region_rank_change` | MATRIX | 0.780 | 宏观与行业 | 0 | — | — | — | UNTESTED | FCF/EV (%) |
| 331 | `eq_vr_dlra2_score` | MATRIX | 0.780 | 风险与质量 | 0 | — | — | — | UNTESTED | CFO/EV (%) |
| 332 | `eq_vr_dlra3_v18` | MATRIX | 0.779 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v18 from the third version of the enhanced earnings quality and valuation mo |
| 333 | `eq_vr_dlra3_v19` | MATRIX | 0.779 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v19 from the third version of the enhanced earnings quality and valuation mo |
| 334 | `eq_vr_dlra1_operating_efficiency_change` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise Value to EBITDA (EV/EBITDA) ratio (relation-value adjusted) |
| 335 | `eq_vr_dlra2_operating_efficiency_change` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | EV/EBITDA |
| 336 | `eq_vr_dlra3_v14` | MATRIX | 0.777 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v14 from the third version of the enhanced earnings quality and valuation mo |
| 337 | `eq_vr_dlra1_raw_score` | MATRIX | 0.775 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price to Cash Flow from Operations (P/CFO) ratio (relation-value adjusted) |
| 338 | `eq_vr_dlra2_raw_score` | MATRIX | 0.775 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/CFO |
| 339 | `eq_vr_dlra3_v11` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v11 from the third version of the enhanced earnings quality and valuation mo |
| 340 | `eq_vr_dlra2_cashflow_component` | MATRIX | 0.772 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/FCF |
| 341 | `eq_vr_dlra3_v12` | MATRIX | 0.769 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v12 from the third version of the enhanced earnings quality and valuation mo |
| 342 | `analyst_downgrade_count_14d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst downgrades over the last 14 days |
| 343 | `analyst_downgrade_count_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 30 days |
| 344 | `analyst_downgrade_count_60d_4` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 60 days |
| 345 | `analyst_downgrade_count_7d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 7 days |
| 346 | `analyst_downgrade_count_90d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the last 90 days |
| 347 | `analyst_downward_revision_count_fq1_earnings_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered FQ1 earnings estimates in the last 14 days |
| 348 | `analyst_downward_revision_count_fq1_earnings_30d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered FQ1 earnings estimates over the last 30 days |
| 349 | `analyst_downward_revision_count_fq1_earnings_7d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates downward for fiscal quarter 1 (FQ1) over the last 7 days |
| 350 | `analyst_downward_revision_count_fq1_ebitda_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their EBITDA estimates for fiscal quarter 1 over the last 14 days |
| 351 | `analyst_downward_revision_count_fq1_ebitda_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates downward for fiscal quarter 1 (FQ1) over the last 30 days |
| 352 | `analyst_downward_revision_count_fq1_revenue_14d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising downward their revenue estimates for fiscal quarter 1, aggregated over the last 14 days |
| 353 | `analyst_downward_revision_count_fq1_revenue_30d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down their revenue estimates for fiscal quarter 1 over the last 30 days |
| 354 | `analyst_downward_revision_count_fq1_revenue_7d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down their revenue estimates for fiscal quarter 1 over the last 7 days |
| 355 | `analyst_downward_revision_count_fq2_earnings_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their fiscal quarter 2 earnings estimates downward over the last 14 days |
| 356 | `analyst_downward_revision_count_fq2_earnings_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their earnings estimates for fiscal quarter 2 (FQ2) over the last 30 days |
| 357 | `analyst_downward_revision_count_fq2_ebitda_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down EBITDA estimates for fiscal quarter 2 over the last 30 days |
| 358 | `analyst_downward_revision_count_fq2_revenue_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their revenue estimates for fiscal quarter 2 (FQ2) over the last 14 days |
| 359 | `analyst_downward_revision_count_fq2_revenue_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their revenue estimates for fiscal quarter 2 over the last 30 days |
| 360 | `analyst_downward_revision_count_fy1_earnings_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their earnings estimates for fiscal year 1 (FY1) over the last 14 days |
| 361 | `analyst_downward_revision_count_fy1_earnings_30d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down their earnings estimates for fiscal year 1 over the last 30 days |
| 362 | `analyst_downward_revision_count_fy1_earnings_7d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their earnings estimates for fiscal year 1 (FY1) over the last 7 days |
| 363 | `analyst_downward_revision_count_fy1_ebitda_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down their EBITDA estimate for fiscal year 1 over the last 14 days |
| 364 | `analyst_downward_revision_count_fy1_ebitda_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates downward for fiscal year 1 over the last 30 days |
| 365 | `analyst_downward_revision_count_fy1_ebitda_7d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down their EBITDA estimates for fiscal year 1, aggregated over the last 7 days |
| 366 | `analyst_downward_revision_count_fy1_revenue_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down revenue estimates for fiscal year 1 over the last 14 days |
| 367 | `analyst_downward_revision_count_fy1_revenue_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down revenue estimates for fiscal year 1 over the last 30 days |
| 368 | `analyst_downward_revision_count_fy1_revenue_7d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who lowered their revenue estimates for fiscal year 1 (FY1) over the last 7 days |
| 369 | `analyst_upgrade_count_14d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst upgrades over the last 14 days |
| 370 | `analyst_upgrade_count_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst upgrades over the last 30 days |
| 371 | `analyst_upgrade_count_60d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst upgrades over the last 60 days |
| 372 | `analyst_upgrade_count_7d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the last 7 days |
| 373 | `analyst_upgrade_count_90d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the last 90 days |
| 374 | `analyst_upward_revision_count_fq1_earnings_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upward for fiscal quarter 1 (FQ1) over the last 14 days |
| 375 | `analyst_upward_revision_count_fq1_earnings_30d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upward for fiscal quarter 1 (FQ1) over the last 30 days |
| 376 | `analyst_upward_revision_count_fq1_ebitda_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their EBITDA estimates for fiscal quarter 1 (FQ1) over the last 14 days |
| 377 | `analyst_upward_revision_count_fq1_ebitda_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for fiscal quarter 1, aggregated over the last 30 days |
| 378 | `analyst_upward_revision_count_fq1_revenue_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their revenue estimates for fiscal quarter 1 over the last 14 days |
| 379 | `analyst_upward_revision_count_fq1_revenue_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upward for fiscal quarter 1 (FQ1) over the last 30 days |
| 380 | `analyst_upward_revision_count_fq1_revenue_7d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their revenue estimates for fiscal quarter 1 over the last 7 days |
| 381 | `analyst_upward_revision_count_fq2_earnings_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upward for fiscal quarter 2 (FQ2) over the last 14 days |
| 382 | `analyst_upward_revision_count_fq2_earnings_30d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised their fiscal quarter 2 earnings estimates upward over the last 30 days |
| 383 | `analyst_upward_revision_count_fq2_ebitda_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who increased their EBITDA estimates for fiscal quarter 2 over the last 30 days |
| 384 | `analyst_upward_revision_count_fq2_revenue_14d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising revenue estimates upward for fiscal quarter 2 (FQ2) over the last 14 days |
| 385 | `analyst_upward_revision_count_fq2_revenue_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their revenue estimates for fiscal quarter 2 (FQ2) over the last 30 days |
| 386 | `analyst_upward_revision_count_fy1_earnings_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upward for fiscal year 1 (FY1) over the last 14 days |
| 387 | `analyst_upward_revision_count_fy1_earnings_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising earnings estimates upward for fiscal year 1 (FY1) over the last 30 days |
| 388 | `analyst_upward_revision_count_fy1_earnings_7d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who increased their earnings estimates for fiscal year 1 over the last 7 days |
| 389 | `analyst_upward_revision_count_fy1_ebitda_14d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates upward for fiscal year 1 (FY1) over the last 14 days |
| 390 | `analyst_upward_revision_count_fy1_ebitda_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their EBITDA estimates for fiscal year 1 over the last 30 days |
| 391 | `analyst_upward_revision_count_fy1_ebitda_7d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their EBITDA estimates for fiscal year 1 (FY1) over the last 7 days |
| 392 | `analyst_upward_revision_count_fy1_revenue_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who increased their revenue estimates for fiscal year 1 over the last 14 days |
| 393 | `analyst_upward_revision_count_fy1_revenue_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up their revenue estimates for fiscal year 1 over the last 30 days |
| 394 | `analyst_upward_revision_count_fy1_revenue_7d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up their revenue estimates for fiscal year 1, aggregated over the last 7 days |
| 395 | `analyst_upward_revision_count_fy2_earnings_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised earnings estimates upward for fiscal year 2 (FY2) over the last 14 days |
| 396 | `analyst_upward_revision_count_fy2_earnings_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up their earnings estimates for fiscal year 2 over the last 30 days |
| 397 | `analyst_upward_revision_count_fy2_earnings_7d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up their earnings estimates for fiscal year 2, aggregated over the last 7 days |
| 398 | `analyst_upward_revision_count_fy2_ebitda_14d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising EBITDA estimates upward for fiscal year 2 (FY2) over the last 14 days |
| 399 | `analyst_upward_revision_count_fy2_ebitda_30d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their EBITDA estimates for fiscal year 2 over the last 30 days |
| 400 | `analyst_upward_revision_count_fy2_ebitda_7d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for fiscal year 2 over the last 7 days |
| 401 | `analyst_upward_revision_count_fy2_revenue_14d_7` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for fiscal year 2 over the last 14 days |
| 402 | `analyst_upward_revision_count_fy2_revenue_30d_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who increased their revenue estimates for fiscal year 2 over the last 30 days |
| 403 | `analyst_upward_revision_count_fy2_revenue_7d_5` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up their revenue estimates for fiscal year 2, aggregated over the last 7 days |
| 404 | `arm_new_activity_flag_6` | MATRIX | 0.756 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating new activity detected by the Analyst Revisions Model |
| 405 | `days_since_last_report_7` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | Number of days since the last report was issued |
| 406 | `recommendation_mean_change_7d_7` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 7 days |
| 407 | `recommendation_mean_change_14d_5` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 14 days |
| 408 | `recommendation_mean_change_30d_6` | MATRIX | 0.753 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 30 days |
| 409 | `recommendation_mean_change_60d_7` | MATRIX | 0.753 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 60 days |
| 410 | `recommendation_mean_change_90d_6` | MATRIX | 0.753 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean change in analyst recommendations over the last 90 days |
| 411 | `actual_last_year_revenue_4` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual revenue reported for the last fiscal year |
| 412 | `mean_estimate_change_pct_fy1_revenue_7d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean FY1 revenue estimate over the last 7 days |
| 413 | `mean_estimate_change_pct_fy1_revenue_14d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal year 1 over the last 14 days |
| 414 | `mean_estimate_change_pct_f12m_revenue_7d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the next 12 months (F12M), aggregated over the last 7 days |
| 415 | `mean_estimate_change_pct_fy1_earnings_7d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal year 1 over the last 7 days |
| 416 | `mean_estimate_change_pct_fy1_revenue_30d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal year 1 (FY1) over the last 30 days |
| 417 | `mean_estimate_price_ratio_f12m_revenue_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-revenue ratio for the next 12 months |
| 418 | `analyst_revisions_score_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Composite score reflecting analyst revisions activity |
| 419 | `arm_country_rank_score_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model rank at the country level represented as a floating-point value |
| 420 | `arm_global_rank_score_3` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model global rank as a floating-point value |
| 421 | `arm_preferred_earnings_component_score_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Preferred earnings component of the Analyst Revisions Model expressed as a floating-point value |
| 422 | `arm_region_rank_decimal_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model regional rank expressed as a decimal |
| 423 | `arm_score_5pt_scale_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model five-day change score |
| 424 | `arm_score_change_1d_3` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model score over the last 1 day |
| 425 | `mean_estimate_change_pct_f12m_revenue_14d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the next 12 months over the last 14 days |
| 426 | `mean_estimate_change_pct_fy1_earnings_14d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percent change in the consensus mean FY1 earnings estimate over the last 14 days |
| 427 | `mean_estimate_price_ratio_fy1_revenue_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-revenue ratio for fiscal year 1 |
| 428 | `arm_score_change_3d_2` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the Analyst Revisions Model (ARM) score over the last 3 days |
| 429 | `arm_score_change_7d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the Analyst Revisions Model (ARM) score over the last 7 days |
| 430 | `mean_estimate_change_pct_f12m_earnings_7d_5` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for the next 12 months, aggregated over the last 7 days |
| 431 | `mean_estimate_change_pct_f12m_earnings_14d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for the next 12 months (F12M), aggregated over the last 14 days |
| 432 | `mean_estimate_change_pct_f12m_revenue_30d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the next 12 months (F12M), aggregated over the last 30 days |
| 433 | `mean_estimate_change_pct_fy1_earnings_30d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for fiscal year 1 over the last 30 days |
| 434 | `mean_estimate_change_pct_fy1_revenue_60d_5` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean revenue estimate for fiscal year 1 over the last 60 days |
| 435 | `mean_estimate_price_ratio_fy2_revenue_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-revenue ratio for fiscal year 2 |
| 436 | `arm_revenue_component_score_4` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Revisions Model (ARM) revenue component score represented as a floating-point value |
| 437 | `arm_score_change_30d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model score over the last 30 days |
| 438 | `mean_estimate_change_pct_f12m_earnings_30d_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for the next 12 months over the last 30 days |
| 439 | `mean_estimate_change_pct_fy1_earnings_60d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal year 1 (FY1) over the last 60 days |
| 440 | `mean_estimate_change_pct_fy1_revenue_90d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal year 1 over the last 90 days |
| 441 | `mean_estimate_change_pct_f12m_revenue_60d_7` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the next 12 months (F12M) over the last 60 days |
| 442 | `surprise_pct_last_year_revenue_6` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise in last fiscal year’s reported revenue versus consensus |
| 443 | `arm_score_change_60d_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the Analyst Revisions Model (ARM) score over the last 60 days |
| 444 | `mean_estimate_change_pct_fy1_earnings_90d_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal year 1 over the last 90 days |
| 445 | `ep_yield_pct_smest_f12m_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on SmartEstimate for the next 12 months |
| 446 | `mean_estimate_change_pct_f12m_earnings_60d_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean earnings estimate for the next 12 months, aggregated over the last 60 days |
| 447 | `mean_estimate_change_pct_f12m_revenue_90d_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for the next 12 months (F12M), aggregated over the last 90 days |
| 448 | `predicted_surprise_fy1_earnings_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for fiscal year 1 (FY1) |
| 449 | `predicted_surprise_fy1_revenue_5` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted revenue surprise for fiscal year 1 |
| 450 | `predicted_surprise_fy2_earnings_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for fiscal year 2 (FY2) |
| 451 | `predicted_surprise_fy2_revenue_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted revenue surprise for fiscal year 2 |
| 452 | `predicted_surprise_pct_fy1_earnings_7` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for fiscal year 1 (FY1) |
| 453 | `predicted_surprise_pct_fy1_revenue_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percentage surprise in revenue for fiscal year 1 relative to consensus |
| 454 | `predicted_surprise_pct_fy2_earnings_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for fiscal year 2 (FY2) |
| 455 | `predicted_surprise_pct_fy2_revenue_5` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage revenue surprise for fiscal year 2 |
| 456 | `smest_fy1_earnings_5` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of earnings for fiscal year 1 |
| 457 | `smest_fy1_revenue_4` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of revenue for fiscal year 1 |
| 458 | `smest_fy2_earnings_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of earnings for fiscal year 2 |
| 459 | `smest_fy2_revenue_5` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of revenue for fiscal year 2 |
| 460 | `smest_price_ratio_f12m_revenue_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate-based price-to-revenue ratio for the next 12 months |
| 461 | `actual_last_year_earnings_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual earnings reported for the last fiscal year |
| 462 | `arm_score_change_90d_4` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in Analyst Revisions Model score over the last 90 days |
| 463 | `ep_yield_pct_smest_fy1_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on SmartEstimate for fiscal year 1 |
| 464 | `ep_yield_pct_smest_fy2_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on SmartEstimate for fiscal year 2 (FY2) |
| 465 | `mean_estimate_change_pct_f12m_earnings_90d_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for the next 12 months (F12M) over the last 90 days |
| 466 | `predicted_surprise_f12m_earnings_7` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise over the next 12 months |
| 467 | `predicted_surprise_f12m_revenue_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted revenue surprise over the next 12 months (F12M) |
| 468 | `predicted_surprise_pct_f12m_earnings_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage surprise in net earnings over the next 12 months (F12M) |
| 469 | `predicted_surprise_pct_f12m_revenue_6` | MATRIX | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted revenue surprise percentage for the next 12 months (F12M) |
| 470 | `smest_f12m_earnings_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of earnings for the next 12 months |
| 471 | `smest_f12m_revenue_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of revenue for the next 12 months (F12M) |
| 472 | `smest_price_ratio_fy1_revenue_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-revenue ratio for fiscal year 1 |
| 473 | `smest_growth_next_vs_this_yr_revenue_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate projected revenue growth from this fiscal year to next fiscal year |
| 474 | `smest_price_ratio_fy2_revenue_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-revenue ratio for fiscal year 2 |
| 475 | `surprise_pct_last_year_earnings_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise in earnings for the last fiscal year relative to consensus |
| 476 | `forward_pe_mean_fy2_7` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio using mean analyst estimates for fiscal year 2 |
| 477 | `mean_estimate_price_ratio_fy2_earnings_5` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-earnings ratio for fiscal year 2 |
| 478 | `forward_pe_mean_f12m_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean forward price-to-earnings ratio based on estimates for the next 12 months |
| 479 | `mean_estimate_price_ratio_f12m_earnings_6` | MATRIX | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-earnings ratio for the next 12 months (forward 12M) |
| 480 | `forward_pe_mean_fy1_5` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean forward price-to-earnings ratio based on fiscal year 1 (FY1) estimates |
| 481 | `forward_pe_smest_fy2_7` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on SmartEstimate for fiscal year 2 |
| 482 | `mean_estimate_price_ratio_fy1_earnings_6` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-earnings ratio for fiscal year 1 |
| 483 | `smest_price_ratio_fy2_earnings_7` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-earnings ratio for fiscal year 2 |
| 484 | `forward_pe_smest_f12m_6` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on SmartEstimate for the next 12 months (F12M) |
| 485 | `smest_growth_this_vs_last_yr_revenue_7` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate comparing this year’s revenue to last year’s revenue |
| 486 | `smest_price_ratio_f12m_earnings_7` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-earnings ratio for the next 12 months (F12M) |
| 487 | `arm_recommendations_component_score_6` | MATRIX | 0.748 | 修正与预期 | 0 | — | — | — | UNTESTED | Floating-point score for the analyst recommendations component within the Analyst Revisions Model (ARM) |
| 488 | `forward_pe_smest_fy1_5` | MATRIX | 0.748 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on SmartEstimate for fiscal year 1 |
| 489 | `smest_price_ratio_fy1_earnings_7` | MATRIX | 0.748 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-earnings ratio for fiscal year 1 |
| 490 | `smest_growth_next_vs_this_yr_earnings_6` | MATRIX | 0.748 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate comparing next fiscal year’s earnings to this year’s earnings |
| 491 | `trailing_pe_last_fiscal_year_6` | MATRIX | 0.747 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio for the last completed fiscal year |
| 492 | `smest_growth_this_vs_last_yr_earnings_6` | MATRIX | 0.745 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate for earnings comparing this year to last year |
| 493 | `mean_estimate_change_pct_fy1_ebitda_7d_7` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for fiscal year 1 (FY1), aggregated over the last 7 days |
| 494 | `mean_estimate_change_pct_fy1_ebitda_14d_7` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for fiscal year 1 over the last 14 days |
| 495 | `mean_estimate_change_pct_f12m_ebitda_7d_7` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months (F12M) over the last 7 days |
| 496 | `mean_estimate_change_pct_fy1_ebitda_30d_6` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for fiscal year 1 over the last 30 days |
| 497 | `mean_estimate_change_pct_f12m_ebitda_14d_7` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months over the last 14 days |
| 498 | `arm_secondary_earnings_component_score_7` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Secondary earnings component value in the Analyst Revisions Model (float) |
| 499 | `mean_estimate_change_pct_fy1_ebitda_60d_6` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for fiscal year 1 (FY1) over the last 60 days |
| 500 | `mean_estimate_change_pct_f12m_ebitda_30d_7` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months over the last 30 days |
| 501 | `mean_estimate_price_ratio_f12m_ebitda_6` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-EBITDA ratio for the next 12 months (forward 12 months) |
| 502 | `mean_estimate_change_pct_fy1_ebitda_90d_4` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for fiscal year 1, aggregated over the last 90 days |
| 503 | `mean_estimate_price_ratio_fy2_ebitda_5` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-EBITDA ratio for fiscal year 2 |
| 504 | `mean_estimate_change_pct_f12m_ebitda_60d_5` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months (F12M) over the last 60 days |
| 505 | `mean_estimate_price_ratio_fy1_ebitda_7` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimated price-to-EBITDA ratio for fiscal year 1 (FY1) |
| 506 | `predicted_surprise_fy1_ebitda_6` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted EBITDA surprise for fiscal year 1 |
| 507 | `predicted_surprise_pct_fy1_ebitda_5` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage surprise in EBITDA for fiscal year 1 |
| 508 | `smest_fy1_ebitda_6` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of EBITDA for fiscal year 1 |
| 509 | `predicted_surprise_fy2_ebitda_7` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for EBITDA in fiscal year 2 |
| 510 | `predicted_surprise_pct_fy2_ebitda_7` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage EBITDA surprise for fiscal year 2 (FY2) |
| 511 | `smest_fy2_ebitda_7` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of EBITDA for fiscal year 2 (FY2) |
| 512 | `mean_estimate_change_pct_f12m_ebitda_90d_6` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean EBITDA estimate for the next 12 months (F12M) over the last 90 days |
| 513 | `predicted_surprise_f12m_ebitda_6` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for EBITDA over the next 12 months (F12M) |
| 514 | `predicted_surprise_pct_f12m_ebitda_7` | MATRIX | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage surprise in EBITDA over the next 12 months (F12M) |
| 515 | `smest_f12m_ebitda_6` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of EBITDA for the next 12 months |
| 516 | `smest_price_ratio_f12m_ebitda_7` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-EBITDA ratio for the next 12 months (F12M) |
| 517 | `smest_price_ratio_fy2_ebitda_7` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-EBITDA ratio for fiscal year 2 |
| 518 | `actual_last_year_ebitda_7` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual EBITDA reported for the last fiscal year |
| 519 | `smest_price_ratio_fy1_ebitda_7` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate price-to-EBITDA ratio for fiscal year 1 |
| 520 | `smest_growth_next_vs_this_yr_ebitda_6` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate projected EBITDA growth from this fiscal year to next fiscal year |
| 521 | `surprise_pct_last_year_ebitda_6` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage EBITDA surprise in the last fiscal year relative to estimates |
| 522 | `smest_growth_this_vs_last_yr_ebitda_5` | MATRIX | 0.734 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate-based growth rate of EBITDA from last year to this year |
| 523 | `eq_vr_dlra1_operating_efficiency_component_change` | MATRIX | 0.726 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to Book (P/B) ratio quarter-over-quarter change (%), 1 quarter difference (relation-value adjusted) |
| 524 | `eq_vr_dlra2_accruals_component_change` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price/Book - 1 Quarter Difference |
| 525 | `eq_vr_dlra2_v7` | MATRIX | 0.726 | 价量与波动 | 0 | — | — | — | UNTESTED | Price/Book - 1 Quarter Difference (%) |
| 526 | `actual_last_quarter_revenue_3` | MATRIX | 0.705 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual revenue reported in the most recent fiscal quarter |
| 527 | `eq_vr_dlra1_exclusions_component_change` | MATRIX | 0.677 | 盈利与财务 | 0 | — | — | — | UNTESTED | EV/EBITDA quarter-over-quarter change (%), 1 quarter difference (relation-value adjusted) |
| 528 | `eq_vr_dlra2_exclusions_component_change` | MATRIX | 0.677 | 盈利与财务 | 0 | — | — | — | UNTESTED | EV/EBITDA - 1 Quarter Difference (%) |
| 529 | `eq_vr_dlra3_new_sector_diff` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Difference between a company's combined earnings quality and valuation score and the sector median in the region. |
| 530 | `eq_vr_dlra3_v7` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Custom model output or component labeled as v7 from the third version of the enhanced earnings quality and valuation mod |
| 531 | `surprise_pct_last_quarter_revenue` | MATRIX | 0.662 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise in revenue for the last reported quarter compared to consensus |
| 532 | `predicted_surprise_fq1_revenue_4` | MATRIX | 0.653 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise in revenue for Fiscal Quarter 1 |
| 533 | `predicted_surprise_pct_fq1_revenue_4` | MATRIX | 0.653 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted revenue surprise for fiscal quarter 1 (FQ1), expressed as a percentage |
| 534 | `smest_fq1_revenue_5` | MATRIX | 0.653 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate of revenue for the upcoming fiscal quarter 1 |
| 535 | `mean_estimate_change_pct_fq1_revenue_7d_4` | MATRIX | 0.644 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean FQ1 revenue estimate over the last 7 days |
| 536 | `mean_estimate_change_pct_fq1_revenue_14d` | MATRIX | 0.636 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal quarter 1 over the last 14 days |
| 537 | `mean_estimate_change_pct_fq1_revenue_30d_4` | MATRIX | 0.624 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean revenue estimate for fiscal quarter 1 over the last 30 days |
| 538 | `actual_last_quarter_revenue_6` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual revenue reported in the most recent fiscal quarter |
| 539 | `mean_estimate_change_pct_fq1_revenue_60d_5` | MATRIX | 0.613 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean revenue estimate for fiscal quarter 1 (FQ1), aggregated over the last 60 days |
| 540 | `actual_last_quarter_earnings_3` | MATRIX | 0.610 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual earnings reported in the most recently reported quarter |
| 541 | `mean_estimate_change_pct_fq1_earnings_7d_4` | MATRIX | 0.608 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal quarter 1 over the last 7 days |
| 542 | `predicted_surprise_fq1_earnings_5` | MATRIX | 0.607 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for fiscal quarter 1 (absolute) |
| 543 | `predicted_surprise_pct_fq1_earnings` | MATRIX | 0.607 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for net earnings for Fiscal Quarter 1 |
| 544 | `smest_fq1_earnings_5` | MATRIX | 0.607 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of net earnings for fiscal quarter 1 |
| 545 | `mean_estimate_change_pct_fq1_earnings_14d_5` | MATRIX | 0.605 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal quarter 1 (FQ1) over the last 14 days |
| 546 | `mean_estimate_change_pct_fq1_revenue_90d_3` | MATRIX | 0.604 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for fiscal quarter 1 over the last 90 days |
| 547 | `mean_estimate_change_pct_fq2_revenue_7d_4` | MATRIX | 0.601 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in mean revenue estimate for fiscal quarter 2 over the last 7 days |
| 548 | `mean_estimate_change_pct_fq1_earnings_30d_5` | MATRIX | 0.601 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the mean earnings estimate for fiscal quarter 1 over the last 30 days |
| 549 | `predicted_surprise_fq2_revenue_3` | MATRIX | 0.600 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted revenue surprise amount for fiscal quarter 2 |
| 550 | `predicted_surprise_pct_fq2_revenue_3` | MATRIX | 0.600 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage revenue surprise for fiscal quarter 2 |
| 551 | `smest_fq2_revenue_4` | MATRIX | 0.600 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate for revenue in fiscal quarter 2 (FQ2) |
| 552 | `mean_estimate_change_pct_fq2_revenue_14d_4` | MATRIX | 0.598 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for fiscal quarter 2, aggregated over the last 14 days |
| 553 | `mean_estimate_change_pct_fq1_earnings_60d_4` | MATRIX | 0.595 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1 over the last 60 days |
| 554 | `mean_estimate_change_pct_fq2_revenue_30d_4` | MATRIX | 0.593 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 2, aggregated over the last 30 days |
| 555 | `eq_vr_dlra3_new_sector_median` | MATRIX | 0.590 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median value of the earnings quality and valuation score within the sector for the current region. |
| 556 | `mean_estimate_change_pct_fq1_earnings_90d_3` | MATRIX | 0.588 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1 over the last 90 days |
| 557 | `mean_estimate_change_pct_fq2_earnings_7d_4` | MATRIX | 0.587 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2, aggregated over the last 7 days |
| 558 | `mean_estimate_change_pct_fq2_earnings_14d_4` | MATRIX | 0.585 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2, aggregated over the last 14 days |
| 559 | `predicted_surprise_pct_fq2_earnings_5` | MATRIX | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage earnings surprise for fiscal quarter 2 |
| 560 | `smest_fq2_earnings_4` | MATRIX | 0.584 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate of earnings for fiscal quarter 2 |
| 561 | `mean_estimate_change_pct_fq2_revenue_60d_5` | MATRIX | 0.582 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 2 over the last 60 days |
| 562 | `mean_estimate_change_pct_fq2_earnings_30d_5` | MATRIX | 0.579 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 2 over the last 30 days |
| 563 | `surprise_pct_last_quarter_revenue_7` | MATRIX | 0.576 | 修正与预期 | 0 | — | — | — | UNUSABLE | Actual revenue surprise percentage for the last reported quarter versus consensus |
| 564 | `actual_last_quarter_ebitda_3` | MATRIX | 0.574 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual EBITDA reported for the most recent fiscal quarter |
| 565 | `mean_estimate_change_pct_fq2_revenue_90d_4` | MATRIX | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for fiscal quarter 2, aggregated over the last 90 days |
| 566 | `predicted_surprise_fq1_ebitda_4` | MATRIX | 0.571 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted EBITDA surprise amount for fiscal quarter 1 (FQ1) |
| 567 | `predicted_surprise_pct_fq1_ebitda_3` | MATRIX | 0.571 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage EBITDA surprise for fiscal quarter 1 |
| 568 | `smest_fq1_ebitda_4` | MATRIX | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate for EBITDA for fiscal quarter 1 |
| 569 | `mean_estimate_change_pct_fq2_earnings_60d_4` | MATRIX | 0.569 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for fiscal quarter 2 over the last 60 days |
| 570 | `predicted_surprise_fq1_revenue_7` | MATRIX | 0.567 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted revenue surprise amount for fiscal quarter 1 |
| 571 | `predicted_surprise_pct_fq1_revenue_6` | MATRIX | 0.567 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage revenue surprise for fiscal quarter 1 |
| 572 | `smest_fq1_revenue_7` | MATRIX | 0.567 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate of revenue for fiscal quarter 1 |
| 573 | `surprise_pct_last_quarter_ebitda_4` | MATRIX | 0.565 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage surprise (actual minus estimated) for EBITDA in the most recent reported quarter |
| 574 | `mean_estimate_change_pct_fq1_ebitda_7d_4` | MATRIX | 0.563 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1, aggregated over the last 7 days |
| 575 | `mean_estimate_change_pct_fq1_revenue_7d_6` | MATRIX | 0.561 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 1 over the last 7 days |
| 576 | `mean_estimate_change_pct_fq2_earnings_90d` | MATRIX | 0.557 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for fiscal quarter 2 over the last 90 days |
| 577 | `mean_estimate_change_pct_fq1_revenue_14d_7` | MATRIX | 0.554 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 1 over the last 14 days |
| 578 | `mean_estimate_change_pct_fq1_ebitda_14d_4` | MATRIX | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1 over the last 14 days |
| 579 | `trailing_pe_last_4q` | MATRIX | 0.550 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Model’s trailing four quarters price-to-earnings ratio |
| 580 | `mean_estimate_change_pct_fq1_revenue_30d_6` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 1 (FQ1) over the last 30 days |
| 581 | `mean_estimate_change_pct_fq1_ebitda_30d` | MATRIX | 0.540 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1, aggregated over the last 30 days |
| 582 | `actual_last_quarter_earnings_7` | MATRIX | 0.533 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual earnings reported in the most recently reported quarter |
| 583 | `mean_estimate_change_pct_fq1_ebitda_60d` | MATRIX | 0.528 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1 over the last 60 days |
| 584 | `mean_estimate_change_pct_fq1_revenue_60d_6` | MATRIX | 0.524 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in mean revenue estimate for fiscal quarter 1 over the last 60 days |
| 585 | `mean_estimate_change_pct_fq1_earnings_7d_7` | MATRIX | 0.520 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1, aggregated over the last 7 days |
| 586 | `predicted_surprise_fq1_earnings_6` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted surprise in earnings for fiscal quarter 1 |
| 587 | `predicted_surprise_pct_fq1_earnings_5` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage earnings surprise for fiscal quarter 1 (FQ1) |
| 588 | `smest_fq1_earnings_6` | MATRIX | 0.519 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate of earnings for fiscal quarter 1 (FQ1) |
| 589 | `mean_estimate_change_pct_fq1_ebitda_90d_3` | MATRIX | 0.518 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean EBITDA estimate for fiscal quarter 1 over the last 90 days |
| 590 | `mean_estimate_change_pct_fq1_earnings_14d_6` | MATRIX | 0.517 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1 (FQ1), aggregated over the last 14 days |
| 591 | `mean_estimate_change_pct_fq2_ebitda_7d_4` | MATRIX | 0.515 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 2, aggregated over the last 7 days |
| 592 | `predicted_surprise_fq2_ebitda_3` | MATRIX | 0.513 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted EBITDA surprise amount for fiscal quarter 2 |
| 593 | `predicted_surprise_pct_fq2_ebitda_4` | MATRIX | 0.513 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage EBITDA surprise for fiscal quarter 2 |
| 594 | `smest_fq2_ebitda_3` | MATRIX | 0.513 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate for EBITDA for fiscal quarter 2 (FQ2) |
| 595 | `mean_estimate_change_pct_fq2_ebitda_14d_4` | MATRIX | 0.512 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 2, aggregated over the last 14 days |
| 596 | `mean_estimate_change_pct_fq1_revenue_90d_6` | MATRIX | 0.512 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 1 over the last 90 days |
| 597 | `mean_estimate_change_pct_fq1_earnings_30d_6` | MATRIX | 0.511 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1 over the last 30 days |
| 598 | `mean_estimate_change_pct_fq2_revenue_7d_6` | MATRIX | 0.511 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 2 over the last 7 days |
| 599 | `predicted_surprise_fq2_revenue_5` | MATRIX | 0.508 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted revenue surprise amount for fiscal quarter 2 |
| 600 | `predicted_surprise_pct_fq2_revenue_5` | MATRIX | 0.508 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage revenue surprise for fiscal quarter 2 |
| 601 | `smest_fq2_revenue_7` | MATRIX | 0.508 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate of revenue for fiscal quarter 2 |
| 602 | `mean_estimate_change_pct_fq2_revenue_14d_5` | MATRIX | 0.508 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for fiscal quarter 2 over the last 14 days |
| 603 | `actual_last_quarter_ebitda_7` | MATRIX | 0.508 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual EBITDA reported for the most recent fiscal quarter |
| 604 | `surprise_pct_last_quarter_earnings_6` | MATRIX | 0.507 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage earnings surprise in the most recently reported quarter compared to estimates |
| 605 | `mean_estimate_change_pct_fq2_ebitda_30d_4` | MATRIX | 0.505 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean EBITDA estimate for fiscal quarter 2 (FQ2) over the last 30 days |
| 606 | `mean_estimate_change_pct_fq1_earnings_60d_6` | MATRIX | 0.504 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1 (FQ1) over the last 60 days |
| 607 | `predicted_surprise_fq1_ebitda_6` | MATRIX | 0.504 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted EBITDA surprise amount for fiscal quarter 1 (difference between actual and consensus) |
| 608 | `predicted_surprise_pct_fq1_ebitda_6` | MATRIX | 0.504 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage EBITDA surprise for fiscal quarter 1 (FQ1) |
| 609 | `smest_fq1_ebitda_7` | MATRIX | 0.504 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate of EBITDA for fiscal quarter 1 |
| 610 | `mean_estimate_change_pct_fq2_revenue_30d_6` | MATRIX | 0.501 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean revenue estimate for fiscal quarter 2 (FQ2) over the last 30 days |
| 611 | `mean_estimate_change_pct_fq2_earnings_7d_5` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for fiscal quarter 2 over the last 7 days |
| 612 | `mean_estimate_change_pct_fq1_ebitda_7d_6` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1 over the last 7 days |
| 613 | `mean_estimate_change_pct_fq1_earnings_90d_6` | MATRIX | 0.497 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 1 aggregated over the last 90 days |
| 614 | `mean_estimate_change_pct_fq2_earnings_14d_5` | MATRIX | 0.496 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 2 over the last 14 days |
| 615 | `surprise_pct_last_quarter_ebitda_6` | MATRIX | 0.496 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage surprise for last quarter EBITDA (actual minus expected) |
| 616 | `predicted_surprise_fq2_earnings_6` | MATRIX | 0.494 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted surprise amount for fiscal quarter 2 earnings |
| 617 | `predicted_surprise_pct_fq2_earnings_7` | MATRIX | 0.494 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage earnings surprise for fiscal quarter 2 (FQ2) |
| 618 | `smest_fq2_earnings_7` | MATRIX | 0.494 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate consensus for fiscal quarter 2 earnings |
| 619 | `mean_estimate_change_pct_fq2_ebitda_60d_4` | MATRIX | 0.492 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2, aggregated over the last 60 days |
| 620 | `mean_estimate_change_pct_fq2_earnings_30d_7` | MATRIX | 0.491 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean earnings estimate for fiscal quarter 2 (FQ2) over the last 30 days |
| 621 | `mean_estimate_change_pct_fq1_ebitda_14d_6` | MATRIX | 0.491 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1 over the last 14 days |
| 622 | `mean_estimate_change_pct_fq2_revenue_60d_7` | MATRIX | 0.490 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for fiscal quarter 2 over the last 60 days |
| 623 | `mean_estimate_change_pct_fq2_earnings_60d_5` | MATRIX | 0.482 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean analyst earnings estimate for fiscal quarter 2, aggregated over the last 60 days |
| 624 | `mean_estimate_change_pct_fq2_ebitda_90d_4` | MATRIX | 0.479 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 2 over the last 90 days |
| 625 | `mean_estimate_change_pct_fq1_ebitda_30d_6` | MATRIX | 0.478 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1 over the last 30 days |
| 626 | `mean_estimate_change_pct_fq2_revenue_90d_5` | MATRIX | 0.478 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in analysts’ revenue estimates for fiscal quarter 2 over the last 90 days |
| 627 | `mean_estimate_change_pct_fq2_earnings_90d_4` | MATRIX | 0.472 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for fiscal quarter 2 over the last 90 days |
| 628 | `mean_estimate_change_pct_fq1_ebitda_60d_5` | MATRIX | 0.464 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in mean EBITDA estimate for fiscal quarter 1 over the last 60 days |
| 629 | `trailing_4_quarter_pe_7` | MATRIX | 0.458 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price-to-earnings ratio based on the trailing four quarters |
| 630 | `mean_estimate_change_pct_fq1_ebitda_90d_6` | MATRIX | 0.453 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for fiscal quarter 1 over the last 90 days |
| 631 | `mean_estimate_change_pct_fq2_ebitda_7d_6` | MATRIX | 0.447 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean EBITDA estimate for fiscal quarter 2 over the last 7 days |
| 632 | `mean_estimate_change_pct_fq2_ebitda_14d_6` | MATRIX | 0.444 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the mean EBITDA estimate for fiscal quarter 2 (FQ2) over the last 14 days |
| 633 | `predicted_surprise_fq2_ebitda_7` | MATRIX | 0.444 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted EBITDA surprise amount for fiscal quarter 2 |
| 634 | `predicted_surprise_pct_fq2_ebitda_6` | MATRIX | 0.444 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Predicted percentage EBITDA surprise for fiscal quarter 2 (FQ2) |
| 635 | `smest_fq2_ebitda_4` | MATRIX | 0.444 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate for EBITDA for fiscal quarter 2 |
| 636 | `mean_estimate_change_pct_fq2_ebitda_30d_5` | MATRIX | 0.436 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in mean EBITDA estimate for fiscal quarter 2 over the last 30 days |
| 637 | `mean_estimate_change_pct_fq2_ebitda_60d_6` | MATRIX | 0.424 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percent change in the consensus mean FQ2 EBITDA estimate over the last 60 days |
| 638 | `mean_estimate_change_pct_fq2_ebitda_90d_5` | MATRIX | 0.411 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percent change in the consensus mean FQ2 EBITDA estimate over the last 90 days |

## 六、本地回测证据

- 本地累计回测 **38** 条；其中 `ra_failed_checks` 为空的 **38** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `gJj1nxLM` | 1.81 | 1.04 | 2.13 | 1.42 | 0.10 | 0 | 112 | `add(multiply(0.4, rank(ts_mean(surprise_pct_last_year_earnings_3, 22))), multiply(0.6, ran` |
| `E5vXYWgG` | 1.77 | 1.08 | 2.07 | 1.32 | 0.10 | 0 | 112 | `add(multiply(0.4, rank(ts_mean(predicted_surprise_pct_f12m_earnings_5, 66))), multiply(0.6` |
| `0mR093K1` | 1.70 | 0.94 | 2.05 | 1.30 | 0.09 | 0 | 112 | `add(multiply(0.4, rank(ts_mean(surprise_pct_last_year_ebitda_2, 22))), multiply(0.6, rank(` |
| `KPOjqdXp` | 1.70 | 1.02 | 1.55 | 1.12 | 0.10 | 0 | 112 | `add(multiply(0.4, rank(ts_mean(predicted_surprise_pct_f12m_ebitda_5, 66))), multiply(0.6, ` |
| `78ZE0bxx` | 1.65 | 0.95 | 1.55 | 1.29 | 0.10 | 0 | 112 | `add(multiply(0.4, rank(ts_mean(predicted_surprise_pct_f12m_revenue_4, 66))), multiply(0.6,` |
| `rKjlpaRj` | 1.39 | 0.77 | 1.22 | 1.30 | 0.10 | 0 | 112 | `add(multiply(0.4, rank(ts_mean(actual_last_year_earnings_3, 22))), multiply(0.6, rank(ts_d` |
| `2rObQzJw` | 1.35 | 0.71 | 1.45 | 1.35 | 0.12 | 0 | 112 | `add(multiply(0.4, group_sum(ts_zscore(surprise_pct_last_year_earnings_3, 22), industry)), ` |
| `d5OAgVnv` | 1.29 | 0.62 | 1.48 | 0.96 | 0.10 | 0 | 112 | `add(multiply(0.4, rank(subtract(ts_mean(surprise_pct_last_year_earnings_3, 22), ts_mean(su` |
| `vRk3xMdG` | 1.29 | 0.63 | 2.14 | 1.09 | 0.11 | 0 | 112 | `add(multiply(0.4, rank(ts_covariance(surprise_pct_last_year_earnings_3, surprise_pct_last_` |
| `9qVLwrOK` | 1.21 | 0.52 | 1.26 | — | 0.03 | 0 | 113 | `rank(multiply(rank(ts_mean(surprise_pct_last_year_earnings_3, 22)), rank(ts_mean(surprise_` |
| `rK5va2oE` | 0.97 | 0.43 | 1.10 | — | 0.02 | 0 | 121 | `rank(ts_mean(eq_vr_dlra1_cashflow_component, 66))` |
| `883dzV2l` | 0.84 | 0.19 | -0.70 | — | 0.35 | 0 | 113 | `add(multiply(0.4, rank(ts_mean(predicted_surprise_pct_f12m_earnings_5, 66))), multiply(0.6` |
| `YP5G3QkW` | 0.69 | 0.26 | 0.76 | — | 0.04 | 0 | 121 | `trade_when(ts_count_nans(eq_vr_dlra1_cashflow_component, 22) < 5, rank(eq_vr_dlra1_cashflo` |
| `akLqde86` | 0.65 | 0.11 | -0.41 | — | 0.43 | 0 | 113 | `add(multiply(0.4, rank(ts_mean(surprise_pct_last_year_ebitda_2, 22))), multiply(0.6, rank(` |
| `XgW5Z1L1` | 0.52 | 0.12 | 0.28 | — | 0.16 | 0 | 121 | `rank(multiply(ts_zscore(eq_vr_dlra1_accruals_component, 66), ts_zscore(eq_vr_dlra1_cashflo` |

## 七、判死记录（sealed dead_end）

- `EUR-M354-VALUATION-YIELD-WEAK`（2026-08-25）family=model354 group valuation yield concepts：{"dataset": "model354", "id": "EUR-M354-VALUATION-YIELD-WEAK", "reason": "Wave66 56 exprs / 7 slots (FY2/NTM EY, FCF/CFO/div yield, sales/EV, FY1-LTM disagreement). Max S0.26 F0.07 (KP7bgexN). Many TVR 2-4%. No cheap-gate. Do not mix PV.", "rule": "Leave model354 standalone valuation densify. Next unused whitelist: ml_factor_proj low-competition non-return MATRIX concepts (not NEWS, not news54, no
- `EUR-MLFP-0ALPHA-OPS-WEAK`（2026-08-25）family=ml_factor_proj 0-alpha coverage/rating/CCC/capex：{"dataset": "ml_factor_proj", "id": "EUR-MLFP-0ALPHA-OPS-WEAK", "reason": "Wave67 56 exprs / 7 slots. Max S0.70 F0.23 (E5lwN5WJ abnormal capex ts_delta). Rating 0.47, CCC 0.41. No cheap-gate. Do not mix PV.", "rule": "Leave this ml_factor_proj ops/coverage family. Do not replay Wave9 EPS/price/FCF ranks. Next: predictive_starmine high-coverage fields unused in Wave21 ARM/RelVal/surprise ranks.", "
- `EUR-STAR-RELVAL-EVEBITDA-2Y-DEAD`（2026-08-25）family=starmine RelVal EV/EBITDA ts_delta × v_rev/wedge：{"dataset": "predictive_starmine", "id": "EUR-STAR-RELVAL-EVEBITDA-2Y-DEAD", "reason": "Wave68 naked rank(ts_delta(rel_val_ev_ebitda_component_score_3,5)) S1.09 2Y=0.10. Wave69 win mix mLj81962 S1.34 F0.77 TVR9.6% prod 0.645 OK but 2Y=0.02 IS_LADDER. Year-regime accident. self 0.64 vs 78jdv6b1.", "rule": "Leave RelVal EV/EBITDA ts_delta family. Do not deepen v_rev/wedge on this slow. Do not clone 
- `EUR-STAR-REVCOUNT-ARM-WEAK`（2026-08-25）family=starmine revision counts / ARM rec-activity：{"dataset": "predictive_starmine", "id": "EUR-STAR-REVCOUNT-ARM-WEAK", "reason": "Wave72 56 exprs on unused upgrade/up/down revision counts + ARM recommendations/new-activity. Max S0.97 F0.30 (arm_new_activity_flag_2 ts_delta). Do not mix PV (/S/<1). Leave RelVal EV/EBITDA and revision-breadth.", "rule": "Do not reuse starmine revision counts or ARM rec/activity as slow legs. Do not deepen RelVal 
- `EUR-STAR-REC-SMEST-WEAK`（2026-08-25）family=starmine rec mean change / smest levels：{"dataset": "predictive_starmine", "id": "EUR-STAR-REC-SMEST-WEAK", "reason": "Wave73 rec mean change max S0.90 but 2021-23 Sharpe ~0.15 collapse. smest F12M/FY1 levels max S0.76 TVR often <2%. Last-year surprise ak7d0ZKR S1.04 F0.40 TVR2.1% 2Y=0.95 RN0.38 — /S/>=1 and 2Y not accident; salvage as slow mix leg. Do not deepen rec-change or smest levels. Leave model28 credit.", "rule": "Do not reuse 
- `EUR-STAR-GAP-FACTOR-NEUT-WEAK`（2026-08-25）family=predictive_starmine surprise x common_gap_up factor neutralization：{"dataset": "predictive_starmine,pattern_scores", "id": "EUR-STAR-GAP-FACTOR-NEUT-WEAK", "max_sharpe": 1.79, "note": "STAT/CROWDING/FAST/SLOW/SAF/RAM on winning ts_delta10 mix; FAST F0.92 2Y1.54 ladder fail; do not retry factor neut to lift RN", "reason": "factor neutralization kills F vs SUBINDUSTRY, does not produce RN>1", "wave": 76}
- `EUR-STAR-ACTUAL-UPGDNG-ARMCOUNTRY-WEAK`（2026-08-25）family=starmine actual EPS/revenue and upgrade/downgrade and ARM country as slow legs：{"dataset": "predictive_starmine", "id": "EUR-STAR-ACTUAL-UPGDNG-ARMCOUNTRY-WEAK", "max_sharpe": 1.56, "note": "mix with common_gap_up ts_delta10; best actual_last_year_earnings S1.56 F0.85; weaker than surprise slow", "reason": "new slows dilute winning surprise x gap mix", "wave": 78}
- `EUR-STAR-ARM-LEFTOVER-WEAK`（2026-08-25）family=starmine ARM preferred/revenue/score-change/region-global as slow; regular_upward_gap as fast：{"dataset": "predictive_starmine,pattern_scores", "id": "EUR-STAR-ARM-LEFTOVER-WEAK", "max_sharpe": 1.55, "note": "best ARM score change 30d S1.55 F0.78; regular_upward_gap S1.04; do not retry ARM leftover or regular_upward_gap", "reason": "weaker than surprise x common_gap_up", "wave": 79}
- `EUR-predictive_starmine-NEWS-MIX-WEAK`（2026-09-04）family=predictive_starmine × news73 sentiment mix：{"best_2y": 1.26, "best_alpha": "9qVLwrOK", "best_fitness": 0.52, "best_sharpe": 1.21, "dataset": "predictive_starmine × news73", "evidence": "wave113 11 条全灭：MODEL×NEWS 配方（surprise 慢腿 × nws73 情绪快腿）整体弱信号，最强候选 S1.21/F0.52/2Y1.26 未达 Mode B 资格线；news73 字段在 EUR TOP2500 覆盖不足或信号弱", "id": "EUR-predictive_starmine-NEWS-MIX-WEAK", "reason": "MODEL×NEWS 跨集混合弱信号：surprise 与 news73 sentiment 相关性不足，组合后 IS 衰减；11 条
- `EUR-predictive_starmine-EQVR-WEAK`（2026-09-04）family=predictive_starmine eq_vr_dlra1 accruals/cashflow：{"best_2y": 1.1, "best_alpha": "rK5va2oE", "best_fitness": 0.43, "best_sharpe": 0.97, "dataset": "predictive_starmine", "evidence": "wave121 9 条：2 条近闸（rK5va2oE S0.97/F0.43/2Y1.10、YP5G3QkW S0.69/F0.26/2Y0.76）但 F<0.8 未达 Mode B 线；eq_vr_dlra1_cashflow_component 有效但强度不足；accruals - cashflow subtract 全负", "id": "EUR-predictive_starmine-EQVR-WEAK", "reason": "predictive_starmine eq_vr_dlra1 族在 EUR TOP2500
- `EUR-predictive_starmine-SMEST-IV-WEAK`（2026-09-04）family=predictive_starmine smest/iv family：{"best_2y": 0.39, "best_alpha": "2rObgmYY", "best_fitness": 0.08, "best_sharpe": 0.47, "dataset": "predictive_starmine", "evidence": "wave122 9 条全灭：smest/iv 族在 EUR TOP2500 整体弱信号，最强 S0.47/F0.08/2Y-0.18 远低于 Mode B 线；if_else 唯一正信号但强度不足；iv_cagr 全负", "id": "EUR-predictive_starmine-SMEST-IV-WEAK", "reason": "predictive_starmine smest/iv 族在 EUR D1 无正向预测力；9 条中 8 条负或弱，1 条 S0.47 弱；if_else 条件逻辑唯一正信号但强度不足", "

