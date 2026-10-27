# model26 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model26` |
| 名称 | Analyst Revisions |
| 类别 | MODEL |
| 数据字段数(平台) | 671 |
| 覆盖率 | 0.7478 |
| 平台已有 alpha | 2613 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBIDs) and Reuters Instrument Codes (RICs), facilitating cross-platform security identification and integration. It is essential for linking and harmonizing data from Bloomberg and Reuters sources, enabling seamless data aggregation, analysis, and reconciliation across different financial systems. While not directly predictive of price movements, accurate identifier mapping is crucial for ensuring data integrity in multi-source quantitative research, portfolio management, and trading operations.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **671** |
| 类型分布 | MATRIX×671 |
| 平均覆盖率 | **0.748** |
| 覆盖率区间 | 0.13 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 280 | 41.7% |
| 中 (0.70–0.90) | 217 | 32.3% |
| 低 (0.50–0.70) | 37 | 5.5% |
| 稀疏 (<0.50) | 137 | 20.4% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 533 | 79.4% |
| UNUSABLE | 138 | 20.6% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 533 / UNUSABLE 138 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 508 | 0.73 | mdl26_arm_recommendations、mdl26_arm_revisions、mdl26_arm_score |
| 盈利与财务 | 76 | 0.68 | mdl26_arm_revenue、mdl26_smahistory_revenue、mdl26_rm_rm_prfrrd_rnngs_cmpnnt |
| 风险与质量 | 27 | 0.89 | mdl26_smahistory_score、mdl26_arm_arm_global_rank、mdl26_arm_arm_score_5 |
| 其他 | 26 | 0.91 | mdl26_market_cap_u、mdl26_preferred、mdl26_days_since_last_report |
| 宏观与行业 | 19 | 0.91 | mdl26_arm_arm_country_rank、mdl26_market_cap_l、country_rank_score_float |
| 价量与波动 | 13 | 0.96 | mdl26_high_price_52、mdl26_low_price_52、mdl26_traded_volume |
| 情绪与新闻 | 2 | 0.74 | country_percentile_rank_model_score、global_percentile_rank_score |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl26_arm_recommendations` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | recommendations |
| 2 | `mdl26_arm_revenue` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | revenue |
| 3 | `mdl26_arm_revisions` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | revisions |
| 4 | `mdl26_arm_score` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Overall ARM composite score (Analyst Revisions Score) for the security, expressed as a regional percentile rank where higher is better |
| 5 | `mdl26_smahistory_revisions` | MATRIX | 0.989 | 修正与预期 | 0 | — | — | — | UNTESTED | Model history revisions |
| 6 | `mdl26_smahistory_score` | MATRIX | 0.989 | 风险与质量 | 0 | — | — | — | UNTESTED | Model history score |
| 7 | `mdl26_smahistory_recommendations` | MATRIX | 0.981 | 修正与预期 | 0 | — | — | — | UNTESTED | Model history recommendations |
| 8 | `mdl26_smahistory_revenue` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Model history revenue |
| 9 | `mdl26_arm_arm_country_rank` | MATRIX | 0.971 | 宏观与行业 | 0 | — | — | — | UNTESTED | country rank (i.e. relative score) |
| 10 | `mdl26_arm_arm_global_rank` | MATRIX | 0.971 | 风险与质量 | 0 | — | — | — | UNTESTED | global rank (i.e. relative score) |
| 11 | `mdl26_arm_arm_score_5` | MATRIX | 0.971 | 风险与质量 | 0 | — | — | — | UNTESTED | score for avg of days: 5 |
| 12 | `mdl26_rm_nlyst_rvsns_scr` | MATRIX | 0.971 | 修正与预期 | 0 | — | — | — | UNTESTED | analyst revisions score |
| 13 | `mdl26_rm_rm_prfrrd_rnngs_cmpnnt` | MATRIX | 0.971 | 盈利与财务 | 0 | — | — | — | UNTESTED | preferred earnings component i.e. portion of final score |
| 14 | `mdl26_arm_arm_score_change_30` | MATRIX | 0.967 | 风险与质量 | 0 | — | — | — | UNTESTED | score change for days: 30 |
| 15 | `mdl26_arm_arm_revenue_component` | MATRIX | 0.961 | 盈利与财务 | 0 | — | — | — | UNTESTED | revenue component i.e. portion of final score |
| 16 | `count_analysts_lower_earnings_est_next_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their earnings estimate for Fiscal Quarter 2 in the past 14 days |
| 17 | `count_analysts_lower_earnings_est_next_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their earnings estimate for Fiscal Quarter 2 in the past 7 days |
| 18 | `count_analysts_lower_ebitda_est_next_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their EBITDA estimate for Fiscal Quarter 2 in the past 14 days |
| 19 | `count_analysts_lower_ebitda_est_next_qtr_30d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their EBITDA estimate for Fiscal Quarter 2 in the past 30 days |
| 20 | `count_analysts_lower_ebitda_est_next_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their EBITDA estimate for Fiscal Quarter 2 in the past 7 days |
| 21 | `count_analysts_lower_ebitda_est_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down EBITDA estimates for Fiscal Quarter 1 over the past 14 days |
| 22 | `count_analysts_lower_ebitda_est_qtr_30d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down EBITDA estimates for Fiscal Quarter 1 over the past 30 days |
| 23 | `count_analysts_lower_ebitda_est_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down EBITDA estimates for Fiscal Quarter 1 over the past 7 days |
| 24 | `count_analysts_lower_revenue_est_next_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Quarter 2 in the past 7 days |
| 25 | `count_analysts_raise_earnings_est_next_qtr_14d` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 2 earnings estimates in the past 14 days |
| 26 | `count_analysts_raise_earnings_est_next_qtr_30d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 2 earnings estimates in the past 30 days |
| 27 | `count_analysts_raise_earnings_est_next_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 2 earnings estimates in the past 7 days |
| 28 | `count_analysts_raise_earnings_est_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 earnings estimates in the past 14 days |
| 29 | `count_analysts_raise_earnings_est_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 earnings estimates in the past 7 days |
| 30 | `count_analysts_raise_ebitda_est_next_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Quarter 2 over the past 14 days |
| 31 | `count_analysts_raise_ebitda_est_next_qtr_30d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Quarter 2 over the past 30 days |
| 32 | `count_analysts_raise_ebitda_est_next_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Quarter 2 over the past 7 days |
| 33 | `count_analysts_raise_ebitda_est_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 EBITDA estimates in the past 14 days |
| 34 | `count_analysts_raise_ebitda_est_qtr_30d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 EBITDA estimates in the past 30 days |
| 35 | `count_analysts_raise_ebitda_est_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 EBITDA estimates in the past 7 days |
| 36 | `count_analysts_raise_revenue_est_next_qtr_14d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Quarter 2 over the past 14 days |
| 37 | `count_analysts_raise_revenue_est_next_qtr_30d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Quarter 2 over the past 30 days |
| 38 | `count_analysts_raise_revenue_est_next_qtr_7d_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Quarter 2 over the past 7 days |
| 39 | `mdl26_nnlyst_rvsng_dwn_fq1_rnngs_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for Fiscal Quarter 1 over the past 14 days |
| 40 | `mdl26_nnlyst_rvsng_dwn_fq1_rnngs_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for Fiscal Quarter 1 over the past 7 days |
| 41 | `mdl26_nnlyst_rvsng_dwn_fq1_rvn_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Quarter 1 in the past 14 days |
| 42 | `mdl26_nnlyst_rvsng_dwn_fq1_rvn_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Quarter 1 in the past 30 days |
| 43 | `mdl26_nnlyst_rvsng_dwn_fq1_rvn_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Quarter 1 in the past 7 days |
| 44 | `mdl26_nnlyst_rvsng_dwn_fq2_rnngs_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their earnings estimate for Fiscal Quarter 2 in the past 30 days |
| 45 | `mdl26_nnlyst_rvsng_dwn_fq2_rvn_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Quarter 2 in the past 14 days |
| 46 | `mdl26_nnlyst_rvsng_dwn_fq2_rvn_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Quarter 2 in the past 30 days |
| 47 | `mdl26_nnlyst_rvsng_dwn_fy1_btd_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their EBITDA estimate for Fiscal Year 1 in the past 14 days |
| 48 | `mdl26_nnlyst_rvsng_dwn_fy1_btd_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their EBITDA estimate for Fiscal Year 1 in the past 30 days |
| 49 | `mdl26_nnlyst_rvsng_dwn_fy1_btd_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their EBITDA estimate for Fiscal Year 1 in the past 7 days |
| 50 | `mdl26_nnlyst_rvsng_dwn_fy1_rnngs_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their earnings estimate for Fiscal Year 1 in the past 14 days |
| 51 | `mdl26_nnlyst_rvsng_dwn_fy1_rnngs_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their earnings estimate for Fiscal Year 1 in the past 30 days |
| 52 | `mdl26_nnlyst_rvsng_dwn_fy1_rnngs_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their earnings estimate for Fiscal Year 1 in the past 7 days |
| 53 | `mdl26_nnlyst_rvsng_dwn_fy1_rvn_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Year 1 in the past 14 days |
| 54 | `mdl26_nnlyst_rvsng_dwn_fy1_rvn_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Year 1 in the past 30 days |
| 55 | `mdl26_nnlyst_rvsng_dwn_fy1_rvn_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of sell-side analysts who lowered their revenue estimate for Fiscal Year 1 in the past 7 days |
| 56 | `mdl26_nnlyst_rvsng_p_fq1_rvn_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 revenue estimates in the past 14 days |
| 57 | `mdl26_nnlyst_rvsng_p_fq1_rvn_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 revenue estimates in the past 30 days |
| 58 | `mdl26_nnlyst_rvsng_p_fq1_rvn_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 revenue estimates in the past 7 days |
| 59 | `mdl26_nnlyst_rvsng_p_fy1_btd_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 1 over the past 14 days |
| 60 | `mdl26_nnlyst_rvsng_p_fy1_btd_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 1 over the past 30 days |
| 61 | `mdl26_nnlyst_rvsng_p_fy1_btd_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 1 over the past 7 days |
| 62 | `mdl26_nnlyst_rvsng_p_fy1_rnngs_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 1 over the past 14 days |
| 63 | `mdl26_nnlyst_rvsng_p_fy1_rnngs_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 1 over the past 30 days |
| 64 | `mdl26_nnlyst_rvsng_p_fy1_rnngs_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 1 over the past 7 days |
| 65 | `mdl26_nnlyst_rvsng_p_fy1_rvn_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Year 1 over the past 14 days |
| 66 | `mdl26_nnlyst_rvsng_p_fy1_rvn_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Year 1 over the past 30 days |
| 67 | `mdl26_nnlyst_rvsng_p_fy1_rvn_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Year 1 over the past 7 days |
| 68 | `mdl26_nnlyst_rvsng_p_fy2_btd_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 2 over the past 14 days |
| 69 | `mdl26_nnlyst_rvsng_p_fy2_btd_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 2 over the past 30 days |
| 70 | `mdl26_nnlyst_rvsng_p_fy2_btd_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 2 over the past 7 days |
| 71 | `mdl26_nnlyst_rvsng_p_fy2_rnngs_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 2 over the past 14 days |
| 72 | `mdl26_nnlyst_rvsng_p_fy2_rnngs_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 2 over the past 30 days |
| 73 | `mdl26_nnlyst_rvsng_p_fy2_rnngs_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 2 over the past 7 days |
| 74 | `mdl26_nnlyst_rvsng_p_fy2_rvn_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Year 2 over the past 14 days |
| 75 | `mdl26_nnlyst_rvsng_p_fy2_rvn_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Year 2 over the past 30 days |
| 76 | `mdl26_nnlyst_rvsng_p_fy2_rvn_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up revenue estimates for Fiscal Year 2 over the past 7 days |
| 77 | `mdl26_num_downgrades_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades in the past 14 days |
| 78 | `mdl26_num_downgrades_60` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades in the past 60 days |
| 79 | `mdl26_num_downgrades_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades in the past 7 days |
| 80 | `mdl26_num_downgrades_90` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades in the past 90 days |
| 81 | `mdl26_num_upgrades_14` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades in the past 14 days |
| 82 | `mdl26_num_upgrades_60` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades in the past 60 days |
| 83 | `mdl26_num_upgrades_7` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades in the past 7 days |
| 84 | `mdl26_num_upgrades_90` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades in the past 90 days |
| 85 | `mdl26_sm_nnlyst_rvsng_dwn_fq1_rnngs_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for Fiscal Quarter 1 over the past 30 days |
| 86 | `mdl26_sm_nnlyst_rvsng_p_fq1_rnngs_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their Fiscal Quarter 1 earnings estimates in the past 30 days |
| 87 | `mdl26_sma_arm_new_activity_flag` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating new ARM-related analyst activity |
| 88 | `mdl26_sma_days_since_last_report` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of model days since the last analyst report or estimate activity |
| 89 | `mdl26_sma_num_downgrades_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades in the past 30 days |
| 90 | `mdl26_sma_num_upgrades_30` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades in the past 30 days |
| 91 | `mdl26_high_price_52` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest price recorded in the past 52 weeks |
| 92 | `mdl26_low_price_52` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | low price 52 days |
| 93 | `mdl26_traded_volume` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | traded volume (in 1000s) |
| 94 | `mdl26_traded_volume_l` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | traded volume (in 1000s)-Local Currency |
| 95 | `mdl26_traded_volume_u` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | traded volume (in 1000s)-USD |
| 96 | `mdl26_rm_rm_rcmmndtns_cmpnnt` | MATRIX | 0.959 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendations component i.e., portion of final score |
| 97 | `mdl26_market_cap_l` | MATRIX | 0.956 | 宏观与行业 | 0 | — | — | — | UNTESTED | Market capitalization in local currency |
| 98 | `mdl26_market_cap_u` | MATRIX | 0.956 | 其他 | 0 | — | — | — | UNTESTED | Market capitalization in USD |
| 99 | `mdl26_mstchg_pct_fy1_rnngs_7` | MATRIX | 0.956 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for Fiscal Year 1 over the past 7 days |
| 100 | `mdl26_preferred` | MATRIX | 0.956 | 其他 | 0 | — | — | — | UNTESTED | preferred |
| 101 | `mdl26_rank` | MATRIX | 0.956 | 风险与质量 | 0 | — | — | — | UNTESTED | Time series of the security’s percentile rank of the overall ARM score within its universe |
| 102 | `mdl26_revisions` | MATRIX | 0.956 | 修正与预期 | 0 | — | — | — | UNTESTED | revisions |
| 103 | `mdl26_score` | MATRIX | 0.956 | 风险与质量 | 0 | — | — | — | UNTESTED | Time series of the overall ARM composite score (1–100) for the security |
| 104 | `analyst_revision_primary_earnings_score` | MATRIX | 0.955 | 修正与预期 | 0 | — | — | — | UNTESTED | Score component reflecting analyst revisions and surprises in the primary earnings measure. |
| 105 | `country_rank_score_float` | MATRIX | 0.955 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score representing the country-based ranking for a stock. |
| 106 | `global_percentile_score_float` | MATRIX | 0.955 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank of the overall ARM signal, expressed as a floating-point value |
| 107 | `mdl26_sm_nlyst_rvsns_scr` | MATRIX | 0.955 | 修正与预期 | 0 | — | — | — | UNTESTED | Composite ARM percentile score indicating strength of analyst estimate and recommendation revisions for the stock |
| 108 | `mdl26_sm_rm_prfrrd_rnngs_cmpnnt` | MATRIX | 0.955 | 盈利与财务 | 0 | — | — | — | UNTESTED | Preferred earnings subcomponent of the ARM score (portion of final score, scaled 1–100) |
| 109 | `mdl26_sma_arm_country_rank` | MATRIX | 0.955 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-level percentile rank of the ARM signal (integer 1–100) |
| 110 | `mdl26_sma_arm_global_rank` | MATRIX | 0.955 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank of the ARM signal (integer 1–100) |
| 111 | `mdl26_sma_arm_score_5` | MATRIX | 0.955 | 风险与质量 | 0 | — | — | — | UNTESTED | Five-day average of the composite ARM score |
| 112 | `region_rank_decimal_score` | MATRIX | 0.955 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region-specific relative rank of the ARM signal, expressed in decimal form |
| 113 | `region_score_float` | MATRIX | 0.955 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score representing the region-based ranking for a stock. |
| 114 | `mdl26_arm_score_change_1` | MATRIX | 0.955 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 1 day |
| 115 | `mdl26_arm_score_change_3` | MATRIX | 0.955 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 3 days |
| 116 | `mdl26_mstchg_pct_fy1_rnngs_14` | MATRIX | 0.955 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for Fiscal Year 1 over the past 14 days |
| 117 | `mdl26_mstchg_pct_f12m_rnngs_7` | MATRIX | 0.955 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month earnings estimate over the last 7 days |
| 118 | `mdl26_arm_score_change_7` | MATRIX | 0.955 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 7 days |
| 119 | `mdl26_mstchg_pct_f12m_rnngs_14` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month earnings estimate over the last 14 days |
| 120 | `is_parent_entity_flag` | MATRIX | 0.954 | 宏观与行业 | 0 | — | — | — | UNTESTED | Indicator whether the company is a parent/consolidated reporting entity in a corporate group (1=yes, 0=no) |
| 121 | `mdl26_arm_new_activity_flag` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating newly detected analyst activity or revisions impacting ARM on this date; 1 = new activity present, 0 = none |
| 122 | `mdl26_bld_stmt_flg_fq1_rnngs` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating whether the current fiscal quarter 1 earnings estimate is bold (significantly different from consensus) |
| 123 | `mdl26_days_since_last_report` | MATRIX | 0.954 | 其他 | 0 | — | — | — | UNTESTED | Model days since last report |
| 124 | `mdl26_nm_ngtv_bld_stmts_fq1_rnngs` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of negative bold (significantly below consensus) estimates for fiscal quarter 1 earnings |
| 125 | `mdl26_nm_pstv_bld_stmts_fq1_rnngs` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of positive bold estimates for fiscal quarter 1 earnings |
| 126 | `mdl26_nm_stm_nlysts_fq1_rnngs` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates included in the SmartEstimate for FQ1 earnings |
| 127 | `mdl26_nnlyst_rvsng_dwn_fq1_rnngs_30` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their Fiscal Quarter 1 earnings estimates in the last 30 days |
| 128 | `mdl26_nnlyst_rvsng_p_fq1_rnngs_30` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their Fiscal Quarter 1 earnings estimates in the last 30 days |
| 129 | `mdl26_prsprise_flag_fq1_earnings` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating the predicted surprise status such as positive, negative, or neutral for fiscal quarter 1 earnings |
| 130 | `primary_earnings_measure_type` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | The earnings measure used as the primary basis for ARM analysis and surprises (e.g., EPS, FFO) |
| 131 | `star_arm_rec_ndown_30` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analyst rating downgrades in the last 30 days |
| 132 | `star_arm_rec_nup_30` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analyst rating upgrades in the last 30 days |
| 133 | `suspect_data_indicator_any_earnings` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator flag showing whether any earnings-related data (across forecast/reporting periods) is considered suspect; 1 = suspect, 0 = not sus |
| 134 | `suspect_data_indicator_model` | MATRIX | 0.954 | 其他 | 0 | — | — | — | UNTESTED | Indicator that the ARM calculation/data for this record are suspect (1=flagged, 0=clean) |
| 135 | `suspect_data_indicator_quarter1_earnings` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator that FQ1 earnings data are suspect (1=flagged, 0=clean) |
| 136 | `mdl26_mstchg_pct_fy1_rnngs_30` | MATRIX | 0.954 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for Fiscal Year 1 over the past 30 days |
| 137 | `mdl26_mstchg_pct_fy1_rvn_7` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst revenue estimates for Fiscal Year 1 over the past 7 days |
| 138 | `star_arm_rec_days_since_new` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of calendar days since the most recent new analyst recommendation was issued |
| 139 | `mdl26_mstchg_pct_f12m_rnngs_30` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month earnings estimate over the last 30 days |
| 140 | `mdl26_chng_frm_52wk_hgh_prc` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage price change from the 52-week high price |
| 141 | `mdl26_chng_frm_52wk_lw_prc` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage change from the 52-week low price to the current price |
| 142 | `mdl26_dff_frm_200dy_mvng_vrg` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Difference between the current price and the 200-day moving average price |
| 143 | `mdl26_dff_frm_50dy_mvng_vrg` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Difference between the current price and the 50-day moving average price |
| 144 | `mdl26_mstchg_pct_fy1_rvn_14` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst revenue estimates for Fiscal Year 1 over the past 14 days |
| 145 | `mdl26_chng_rltv_t_cc_40_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to CAC 40 index over 30 days |
| 146 | `mdl26_chng_rltv_t_dj_stxx_600_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to DJ STOXX 600 index over 30 days |
| 147 | `mdl26_chng_rltv_t_fts_100_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to FTSE 100 index over 30 days |
| 148 | `mdl26_chng_rltv_t_hng_sng_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to Hang Seng index over 30 days |
| 149 | `mdl26_chng_rltv_t_js_ll_shr_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to JSE All Share index over 30 days |
| 150 | `mdl26_chng_rltv_t_msc_f_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to MSCI EAFE index over 30 days |
| 151 | `mdl26_chng_rltv_t_msc_mf_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to MSCI Emerging Markets Free index over 30 days |
| 152 | `mdl26_chng_rltv_t_msc_pc_x_jp_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to MSCI Pacific excluding Japan index over 30 days |
| 153 | `mdl26_chng_rltv_t_msc_rp_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to MSCI Europe index over 30 days |
| 154 | `mdl26_chng_rltv_t_r1000_grwth_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to Russell 1000 Growth index over 30 days |
| 155 | `mdl26_chng_rltv_t_rssll_2000_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to Russell 2000 index over 30 days |
| 156 | `mdl26_chng_rltv_t_rssll_mdcp_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to Russell Midcap index over 30 days |
| 157 | `mdl26_chng_rltv_t_sp_400_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to S&P 400 index over 30 days |
| 158 | `mdl26_chng_rltv_t_sp_500_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to S&P 500 index over 30 days |
| 159 | `mdl26_chng_rltv_t_sp_600_30` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | The stock’s 30-day percentage price change minus the S&P 600 index’s 30-day percentage change |
| 160 | `mdl26_chng_rltv_t_sx_100_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to ASX 100 index over 30 days |
| 161 | `mdl26_chng_rltv_t_sx_200_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to ASX 200 index over 30 days |
| 162 | `mdl26_chng_rltv_t_sx_300_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to ASX 300 index over 30 days |
| 163 | `mdl26_chng_rltv_t_sx_ll_rd_30` | MATRIX | 0.952 | 其他 | 0 | — | — | — | UNTESTED | Change relative to ASX All Ordinaries over 30 days |
| 164 | `mdl26_chng_rltv_t_tpx_30` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock’s 30-day percentage price change minus the TOPIX index’s 30-day percentage change |
| 165 | `mdl26_chng_rltv_t_tsx_cmpst_30` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock’s 30-day percentage price change minus the TSX Composite index’s 30-day percentage change |
| 166 | `mdl26_price_change_30` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage price change over the last 30 trading days |
| 167 | `mdl26_mstchg_pct_f12m_rvn_7` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month revenue estimate over the last 7 days |
| 168 | `mdl26_sma_arm_score_change_30` | MATRIX | 0.952 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 30 days |
| 169 | `mdl26_revenue` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | Revenue component of ARM history capturing analyst revenue estimate revisions |
| 170 | `analyst_revision_revenue_score_d1` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | Score component reflecting analyst revisions and surprises in company revenue (daily version). |
| 171 | `mdl26_sma_arm_revenue_component` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | Revenue subcomponent of the ARM score, reflecting revenue-related analyst signals (scaled as a component score) |
| 172 | `mdl26_mstchg_pct_f12m_rvn_14` | MATRIX | 0.952 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month revenue estimate over the last 14 days |
| 173 | `mdl26_mstchg_pct_fy1_rvn_30` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst revenue estimates for Fiscal Year 1 over the past 30 days |
| 174 | `mdl26_mstchg_pct_fy1_rnngs_60` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for Fiscal Year 1 over the past 60 days |
| 175 | `mdl26_chng_rltv_t_cntry_bnchmrk_30` | MATRIX | 0.951 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentage change relative to the country benchmark over the last 30 trading days |
| 176 | `mdl26_chng_rltv_t_ndstry_bnchmrk_30` | MATRIX | 0.951 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentage change relative to the industry benchmark over the last 30 trading days |
| 177 | `mdl26_prsprise_fy1_earnings` | MATRIX | 0.951 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted earnings surprise amount for Fiscal Year 1 |
| 178 | `mdl26_prsprise_pct_fy1_earnings` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal year 1 earnings (Predicted Surprise %) |
| 179 | `mdl26_smartestimate_fy1_earnings` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for earnings for Fiscal Year 1 |
| 180 | `mdl26_p_yld_pct_stm_f12m` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage earnings divided by price based on SmartEstimate for the next 12 months |
| 181 | `mdl26_prsprise_fy2_earnings` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the StarMine SmartEstimate and the mean consensus for fiscal year 2 earnings (Predicted Surprise amount) |
| 182 | `mdl26_prsprise_pct_fy2_earnings` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal year 2 earnings (Predicted Surprise %) |
| 183 | `mdl26_smartestimate_fy2_earnings` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for earnings for Fiscal Year 2 |
| 184 | `mdl26_mstchg_pct_f12m_rvn_30` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for the next 12 months over the last 30 days |
| 185 | `mdl26_mstchg_pct_f12m_rnngs_60` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month earnings estimate over the last 60 days |
| 186 | `mdl26_p_yld_pct_stm_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage earnings divided by price based on SmartEstimate for the current fiscal year FY1 |
| 187 | `mdl26_arm_score_change_60` | MATRIX | 0.949 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 60 days |
| 188 | `mdl26_prsprise_f12m_earnings` | MATRIX | 0.949 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise (actual minus predicted value) for trailing 12 months earnings |
| 189 | `mdl26_prsprise_pct_f12m_earnings` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted percentage earnings surprise for the next 12 months (SmartEstimate versus mean consensus) |
| 190 | `mdl26_stm_f12m_rnngs` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for forward 12 months earnings |
| 191 | `mdl26_p_yld_pct_stm_fy2` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings-to-Price yield percentage based on StarMine SmartEstimate for Fiscal Year 2 |
| 192 | `mdl26_rcmmndtn_mn_chng_7` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 7 days |
| 193 | `mdl26_arm_arm_country_rank_2` | MATRIX | 0.948 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country rank (relative percentile score) of the ARM signal |
| 194 | `mdl26_arm_arm_global_rank_2` | MATRIX | 0.948 | 风险与质量 | 0 | — | — | — | UNTESTED | Global rank (relative percentile score) of the ARM signal |
| 195 | `mdl26_arm_arm_score_5_2` | MATRIX | 0.948 | 风险与质量 | 0 | — | — | — | UNTESTED | Five-day average of the ARM score |
| 196 | `mdl26_rm_nlyst_rvsns_scr_2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst revisions score (headline ARM composite) |
| 197 | `mdl26_rm_rm_prfrrd_rnngs_cmpnnt_2` | MATRIX | 0.948 | 盈利与财务 | 0 | — | — | — | UNTESTED | Preferred earnings component portion of the final ARM score |
| 198 | `region_percentile_rank_decimal` | MATRIX | 0.948 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region rank expressed in decimal form within the ARM system |
| 199 | `star_arm_country_rank` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Country-level percentile rank of the ARM signal (higher means stronger revisions vs country peers) |
| 200 | `star_arm_global_rank` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Global percentile rank of the ARM signal (higher means stronger revisions vs global peers) |
| 201 | `star_arm_pref_earnings_score` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentile sub-score for the company’s preferred earnings metric revisions used by ARM; contributes to the overall ARM score |
| 202 | `star_arm_region_rank_decimal` | MATRIX | 0.948 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regional percentile rank expressed as a decimal between 0 and 1 for the ARM signal |
| 203 | `star_arm_score` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Headline ARM composite score summarizing analyst estimate and recommendation revisions |
| 204 | `star_arm_score_5` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Five-day moving average of the ARM composite (Analyst Revisions) score |
| 205 | `mdl26_mstchg_pct_fy1_rvn_60` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst revenue estimates for Fiscal Year 1 over the past 60 days |
| 206 | `mdl26_mstchg_pct_fy1_rnngs_90` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for Fiscal Year 1 over the past 90 days |
| 207 | `mdl26_mn_stmt_prc_rt_f12m_rvn` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using the mean consensus estimate for forward 12 months revenue |
| 208 | `mdl26_rcmmndtn_mn_chng_14` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 14 days |
| 209 | `mdl26_mn_stmt_prc_rt_fy1_rvn` | MATRIX | 0.947 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using the mean consensus estimate for Fiscal Year 1 |
| 210 | `mdl26_mn_stmt_prc_rt_fy2_rvn` | MATRIX | 0.947 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using the mean consensus estimate for Fiscal Year 2 |
| 211 | `mdl26_mstchg_pct_f12m_rvn_60` | MATRIX | 0.947 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for the next 12 months over the last 60 days |
| 212 | `mdl26_mstchg_pct_f12m_rnngs_90` | MATRIX | 0.947 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month earnings estimate over the last 90 days |
| 213 | `mdl26_arm_score_change_90` | MATRIX | 0.946 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 90 days |
| 214 | `mdl26_sm_rcmmndtn_mn_chng_30` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 30 days |
| 215 | `mdl26_prsprise_fy2_revenue` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the StarMine SmartEstimate and the mean consensus for fiscal year 2 revenue (Predicted Surprise amount) |
| 216 | `mdl26_prsprise_pct_fy2_revenue` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal year 2 revenue (Predicted Surprise %) |
| 217 | `mdl26_smartestimate_fy2_revenue` | MATRIX | 0.946 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for revenue for Fiscal Year 2 |
| 218 | `mdl26_prsprise_fy1_revenue` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted revenue surprise amount for fiscal year 1 |
| 219 | `mdl26_prsprise_pct_fy1_revenue` | MATRIX | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal year 1 revenue (Predicted Surprise %) |
| 220 | `mdl26_smartestimate_fy1_revenue` | MATRIX | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for revenue for Fiscal Year 1 |
| 221 | `mdl26_mstchg_pct_fy1_rvn_90` | MATRIX | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst revenue estimates for Fiscal Year 1 over the past 90 days |
| 222 | `mdl26_arm_arm_score_change_30_2` | MATRIX | 0.945 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM score over the last 30 days |
| 223 | `star_arm_score_change_1m` | MATRIX | 0.945 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM composite score over the last 30 days |
| 224 | `mdl26_arm_arm_revenue_component_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue component portion of the final ARM score |
| 225 | `star_arm_revenue_score` | MATRIX | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentile sub-score for revenue estimate revisions; contributes to the overall ARM score |
| 226 | `mdl26_prsprise_f12m_revenue` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted revenue surprise amount for the next 12 months |
| 227 | `mdl26_prsprise_pct_f12m_revenue` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted percentage revenue surprise for the next 12 months (SmartEstimate versus mean consensus) |
| 228 | `mdl26_smartestimate_f12m_revenue` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for forward 12 months revenue |
| 229 | `mdl26_mstchg_pct_f12m_rvn_90` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for the next 12 months over the last 90 days |
| 230 | `mdl26_rcmmndtn_mn_chng_60` | MATRIX | 0.943 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 60 days |
| 231 | `mdl26_smrtst_grwth_nxt_yrths_yr_rvn` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate ratio of next year’s to this year’s revenue |
| 232 | `mdl26_ep_yield_smartestimate_fy1` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield (earnings-to-price ratio) for next fiscal year based on StarMine SmartEstimate, expressed as a percentage |
| 233 | `mdl26_stm_prc_rt_f12m_rvn` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using StarMine SmartEstimate for forward 12 months revenue |
| 234 | `mdl26_yld_stm_fy1_rnngs` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend yield percentage estimated using StarMine SmartEstimate for fiscal year 1 |
| 235 | `mdl26_recommendations` | MATRIX | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendations component of ARM history capturing analyst recommendation changes and momentum |
| 236 | `analyst_recommendation_score_component` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Score component reflecting changes in analyst buy/sell/hold recommendations. |
| 237 | `mdl26_sm_rm_rcmmndtns_cmpnnt` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendations subcomponent score contributing to the overall ARM score |
| 238 | `star_arm_rec_mean_prior7` | MATRIX | 0.941 | 修正与预期 | 0 | — | — | — | UNTESTED | The mean analyst recommendation as of 7 calendar days ago |
| 239 | `mdl26_ep_industry_percentile_fy1` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank within industry of the Fiscal Year 1 earnings yield (E/P) |
| 240 | `mdl26_ep_sector_percentile_fy1` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank within sector of the Fiscal Year 1 earnings yield (E/P) |
| 241 | `mdl26_rcmmndtn_mn_chng_90` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 90 days |
| 242 | `mdl26_stm_prc_rt_fy2_rvn` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using StarMine SmartEstimate for Fiscal Year 2 |
| 243 | `mdl26_yld_ndstry_prcntl_fy1_rnngs` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Industry percentile ranking of the dividend yield based on FY1 estimates |
| 244 | `mdl26_yld_sctr_prcntl_fy1_rnngs` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Sector percentile ranking of the dividend yield based on FY1 estimates |
| 245 | `mdl26_mdn_hstrcl_f12m_prc_rt_rnngs` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median historical forward 12-month price-to-earnings ratio for the company |
| 246 | `mdl26_median_historical_f12m_pe` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median historical Price-to-Earnings ratio for the last twelve months |
| 247 | `mdl26_stm_prc_rt_fy1_rvn` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using StarMine SmartEstimate for Fiscal Year 1 |
| 248 | `star_arm_rec_mean_change30` | MATRIX | 0.939 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the average analyst recommendation over the past 30 calendar days |
| 249 | `mdl26_actual_last_y_revenue` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual revenue reported for the most recent fiscal year |
| 250 | `mdl26_blndd_grwth_rt_smrtstmt` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | blended growth rate smartestimate |
| 251 | `mdl26_blndd_grwth_ndstry_prcntl` | MATRIX | 0.936 | 宏观与行业 | 0 | — | — | — | UNTESTED | blended growth industry percentile |
| 252 | `mdl26_blndd_grwth_sctr_prcntl` | MATRIX | 0.936 | 宏观与行业 | 0 | — | — | — | UNTESTED | blended growth sector percentile |
| 253 | `mdl26_sma_actual_last_y_earnings` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual earnings reported for the most recent fiscal year |
| 254 | `mdl26_srprs_pct_lst_y_rvn` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage surprise for last year revenue: (actual minus predicted) divided by predicted, expressed as a percentage |
| 255 | `mdl26_srprs_pct_lst_y_rnngs` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage surprise for last year earnings: (actual minus predicted) divided by predicted, expressed as a percentage |
| 256 | `star_arm_recommendations_score` | MATRIX | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentile sub-score capturing analyst recommendation momentum; contributes to the overall ARM score |
| 257 | `mdl26_rm_rm_rcmmndtns_cmpnnt_2` | MATRIX | 0.933 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendations component portion of the final ARM score |
| 258 | `mdl26_forward_pe_mean_fy2` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on the mean consensus estimate for the next fiscal year FY2 |
| 259 | `mdl26_mn_stmt_prc_rt_fy2_rnngs` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the mean consensus estimate for Fiscal Year 2 |
| 260 | `mdl26_actual_last_y_earnings` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual earnings reported for the most recent fiscal year |
| 261 | `mdl26_frwrd_p_stm_fy2` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on StarMine SmartEstimate for the next fiscal year FY2 |
| 262 | `mdl26_stm_prc_rt_fy2_rnngs` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using StarMine SmartEstimate for Fiscal Year 2 |
| 263 | `mdl26_surprise_last_y_earnings` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings surprise for the last fiscal year, calculated as actual minus predicted |
| 264 | `mdl26_forward_pe_mean_f12m` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on the mean consensus estimate for the next 12 months |
| 265 | `mdl26_mn_stmt_prc_rt_f12m_rnngs` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the mean consensus estimate for forward 12 months earnings |
| 266 | `mdl26_smrtst_grwth_ths_yrlst_yr_rvn` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate ratio of this year’s to last year’s revenue |
| 267 | `mdl26_60dy_srprs_lst_y_rnngs` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | 60day surprise (actual value - predicted value) last YEAR earnings |
| 268 | `mdl26_frwrd_p_stm_f12m` | MATRIX | 0.921 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on StarMine SmartEstimate for the next 12 months |
| 269 | `mdl26_stm_prc_rt_f12m_rnngs` | MATRIX | 0.921 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using StarMine SmartEstimate for forward 12 months earnings |
| 270 | `mdl26_dffrnc_frm_hstrcl_p` | MATRIX | 0.918 | 盈利与财务 | 0 | — | — | — | UNTESTED | difference from historical (Price/Earnings ratio) |
| 271 | `mdl26_dffrnc_frm_hstrcl_prc_rt_rnngs` | MATRIX | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Percent difference between the current P/E and the company’s historical median P/E |
| 272 | `mdl26_rm_rm_scndry_rnngs_cmpnnt` | MATRIX | 0.915 | 盈利与财务 | 0 | — | — | — | UNTESTED | secondary earnings component i.e. portion of final score |
| 273 | `mdl26_sm_mn_stmt_prc_rt_fy1_rnngs` | MATRIX | 0.911 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the mean consensus estimate for Fiscal Year 1 |
| 274 | `mdl26_sma_forward_pe_mean_fy1` | MATRIX | 0.911 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on the mean consensus estimate for the current fiscal year FY1 |
| 275 | `mdl26_smrtst_grwth_f24mf12m_rnngs` | MATRIX | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Expected earnings growth from forward 12 months to forward 24 months based on SmartEstimate |
| 276 | `mdl26_sm_frwrd_p_stm_fy1` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price to earnings ratio based on StarMine SmartEstimate for the current fiscal year FY1 |
| 277 | `mdl26_sm_smrtst_grwth_nxt_yrths_yr_rnngs` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate ratio of next year’s to this year’s earnings |
| 278 | `mdl26_sm_stm_prc_rt_fy1_rnngs` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using StarMine SmartEstimate for Fiscal Year 1 |
| 279 | `mdl26_forward_pe_mean_fy1` | MATRIX | 0.904 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio using the mean analyst EPS estimate for Fiscal Year 1 |
| 280 | `mdl26_mn_stmt_prc_rt_fy1_rnngs` | MATRIX | 0.904 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst estimate Price-to-Earnings ratio for FY1 |
| 281 | `mdl26_frwrd_p_stm_fy1` | MATRIX | 0.898 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio using StarMine SmartEstimate for Fiscal Year 1 EPS |
| 282 | `mdl26_stm_prc_rt_fy1_rnngs` | MATRIX | 0.898 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on the StarMine SmartEstimate for FY1 earnings |
| 283 | `mdl26_smrtst_grwth_nxt_yrths_yr_rnngs` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Expected earnings growth from this fiscal year to next fiscal year based on the StarMine SmartEstimate |
| 284 | `mdl26_grwth_nxt_yr_ndstry_prcntl_rnngs` | MATRIX | 0.896 | 修正与预期 | 0 | — | — | — | UNTESTED | Industry percentile rank of next fiscal year’s earnings growth (SmartEstimate) |
| 285 | `mdl26_grwth_nxt_yr_sctr_prcntl_rnngs` | MATRIX | 0.896 | 修正与预期 | 0 | — | — | — | UNTESTED | Sector percentile rank of next fiscal year’s earnings growth (SmartEstimate) |
| 286 | `mdl26_mstchg_pct_fy1_btd_7` | MATRIX | 0.884 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst EBITDA estimates for Fiscal Year 1 over the past 7 days |
| 287 | `mdl26_secondary` | MATRIX | 0.883 | 其他 | 0 | — | — | — | UNTESTED | secondary |
| 288 | `analyst_revision_secondary_earnings_score` | MATRIX | 0.883 | 修正与预期 | 0 | — | — | — | UNTESTED | Score component reflecting analyst revisions and surprises in the secondary earnings measure. |
| 289 | `mdl26_mstchg_pct_fy1_btd_14` | MATRIX | 0.883 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst EBITDA estimates for Fiscal Year 1 over the past 14 days |
| 290 | `mdl26_sm_rm_scndry_rnngs_cmpnnt` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Secondary earnings component contributing to the final ARM score |
| 291 | `mdl26_mstchg_pct_f12m_btd_7` | MATRIX | 0.883 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month EBITDA estimate over the last 7 days |
| 292 | `mdl26_mstchg_pct_f12m_btd_14` | MATRIX | 0.881 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month EBITDA estimate over the last 14 days |
| 293 | `mdl26_mstchg_pct_fy1_btd_30` | MATRIX | 0.881 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst EBITDA estimates for Fiscal Year 1 over the past 30 days |
| 294 | `star_arm_rec_days_since_2lv_change` | MATRIX | 0.881 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of days since a two-level change in analyst recommendation occurred |
| 295 | `mdl26_mstchg_pct_f12m_btd_30` | MATRIX | 0.879 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month EBITDA estimate over the last 30 days |
| 296 | `mdl26_mstchg_pct_fy1_btd_60` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst EBITDA estimates for Fiscal Year 1 over the past 60 days |
| 297 | `mdl26_prsprise_fy2_ebitda` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the StarMine SmartEstimate and the mean consensus for fiscal year 2 EBITDA (Predicted Surprise amount) |
| 298 | `mdl26_prsprise_pct_fy2_ebitda` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal year 2 EBITDA (Predicted Surprise %) |
| 299 | `mdl26_smartestimate_fy2_ebitda` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for EBITDA for Fiscal Year 2 |
| 300 | `mdl26_prsprise_fy1_ebitda` | MATRIX | 0.877 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise (actual minus predicted) for Fiscal Year 1 EBITDA |
| 301 | `mdl26_prsprise_pct_fy1_ebitda` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal year 1 EBITDA (Predicted Surprise %) |
| 302 | `mdl26_smartestimate_fy1_ebitda` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for EBITDA for Fiscal Year 1 |
| 303 | `mdl26_rm_rm_scndry_rnngs_cmpnnt_2` | MATRIX | 0.876 | 盈利与财务 | 0 | — | — | — | UNTESTED | Secondary earnings component portion of the final ARM score |
| 304 | `star_arm_secondary_earnings_score` | MATRIX | 0.876 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentile sub-score for the secondary earnings metric revisions; contributes to the overall ARM score |
| 305 | `mdl26_mstchg_pct_f12m_btd_60` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month EBITDA estimate over the last 60 days |
| 306 | `mdl26_prsprise_f12m_ebitda` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the StarMine SmartEstimate and the mean consensus for forward 12 months EBITDA (Predicted Surprise amount) |
| 307 | `mdl26_prsprise_pct_f12m_ebitda` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted percentage EBITDA surprise for the next 12 months (SmartEstimate versus mean consensus) |
| 308 | `mdl26_smartestimate_f12m_ebitda` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted consensus) for forward 12 months EBITDA |
| 309 | `mdl26_lt_grwth_ndstry_prcntl` | MATRIX | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry percentile rank of long-term growth |
| 310 | `mdl26_lt_grwth_sctr_prcntl` | MATRIX | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector percentile rank of long-term growth |
| 311 | `mdl26_mstchg_pct_fy1_btd_90` | MATRIX | 0.873 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst EBITDA estimates for Fiscal Year 1 over the past 90 days |
| 312 | `mdl26_sma_last_fiscal_year_pe` | MATRIX | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price to earnings ratio using earnings from the last completed fiscal year |
| 313 | `mdl26_mstchg_pct_f12m_btd_90` | MATRIX | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage change in the consensus mean forward 12 month EBITDA estimate over the last 90 days |
| 314 | `mdl26_smrtst_grwth_f12mt12m_rnngs` | MATRIX | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Expected earnings growth from trailing 12 months to forward 12 months based on SmartEstimate |
| 315 | `mdl26_mn_stmt_prc_rt_f12m_btd` | MATRIX | 0.867 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using the mean consensus estimate for forward 12 months EBITDA |
| 316 | `mdl26_mn_stmt_prc_rt_fy2_btd` | MATRIX | 0.867 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using the mean consensus estimate for Fiscal Year 2 |
| 317 | `mdl26_sm_smrtst_grwth_ths_yrlst_yr_rnngs` | MATRIX | 0.867 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate ratio of this year’s to last year’s earnings |
| 318 | `mdl26_last_fiscal_year_pe` | MATRIX | 0.864 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the last fiscal year’s actual earnings |
| 319 | `star_arm_rec_days_since_newsell` | MATRIX | 0.862 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of calendar days since the latest new Sell recommendation was issued for the stock |
| 320 | `mdl26_mn_stmt_prc_rt_fy1_btd` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using the mean consensus estimate for Fiscal Year 1 |
| 321 | `mdl26_smrtst_grwth_ths_yrlst_yr_rnngs` | MATRIX | 0.859 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings growth from last fiscal year to this fiscal year based on the StarMine SmartEstimate |
| 322 | `mdl26_stm_prc_rt_f12m_btd` | MATRIX | 0.859 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using StarMine SmartEstimate for forward 12 months EBITDA |
| 323 | `mdl26_stm_prc_rt_fy2_btd` | MATRIX | 0.859 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using StarMine SmartEstimate for Fiscal Year 2 |
| 324 | `mdl26_grwth_ths_yr_ndstry_prcntl_rnngs` | MATRIX | 0.859 | 修正与预期 | 0 | — | — | — | UNTESTED | Industry percentile rank of this fiscal year’s earnings growth (SmartEstimate) |
| 325 | `mdl26_grwth_ths_yr_sctr_prcntl_rnngs` | MATRIX | 0.859 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank versus sector peers of expected earnings growth for the current fiscal year higher indicates faster expected growth |
| 326 | `mdl26_smrtst_grwth_nxt_yrths_yr_btd` | MATRIX | 0.854 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate ratio of next year’s to this year’s EBITDA |
| 327 | `mdl26_stm_prc_rt_fy1_btd` | MATRIX | 0.852 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using StarMine SmartEstimate for Fiscal Year 1 |
| 328 | `mdl26_actual_last_y_ebitda` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual EBITDA reported for the most recent fiscal year |
| 329 | `mdl26_surprise_pct_last_y_ebitda` | MATRIX | 0.830 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage surprise for last year EBITDA: (actual minus predicted) divided by predicted, expressed as a percentage |
| 330 | `mdl26_5yr_hstrcl_grwth_rt` | MATRIX | 0.824 | 宏观与行业 | 0 | — | — | — | UNTESTED | 5year historical growth rate |
| 331 | `mdl26_smrtst_pg_ndstry_prcntl_f12m` | MATRIX | 0.813 | 修正与预期 | 0 | — | — | — | UNTESTED | Industry percentile ranking of the PEG ratio based on SmartEstimate and forward 12-month growth |
| 332 | `mdl26_smrtst_pg_sctr_prcntl_f12m` | MATRIX | 0.813 | 修正与预期 | 0 | — | — | — | UNTESTED | Sector percentile ranking of the PEG ratio based on SmartEstimate and forward 12-month growth |
| 333 | `mdl26_peg_mean_fy1` | MATRIX | 0.809 | 修正与预期 | 0 | — | — | — | UNTESTED | PEG ratio computed using forward FY1 P/E from mean estimates and the corresponding growth estimate |
| 334 | `mdl26_peg_smartestimate_fy1` | MATRIX | 0.808 | 修正与预期 | 0 | — | — | — | UNTESTED | (Price/Earnings-to-growth) smartestimate FYEAR1 |
| 335 | `mdl26_smrtst_grwth_ths_yrlst_yr_btd` | MATRIX | 0.794 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate ratio of this year’s to last year’s EBITDA |
| 336 | `analyst_recommendation_upgrades_count_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the past 30 days |
| 337 | `analysts_count_revising_down_quarter1_earnings_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for Fiscal Quarter 1 over the last 7 days |
| 338 | `analysts_count_revising_down_year1_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their earnings estimates for the current fiscal year (FY1) in the past 14 days |
| 339 | `analysts_count_revising_down_year1_ebitda_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their EBITDA estimates for the current fiscal year (FY1) in the past 14 days |
| 340 | `analysts_count_revising_up_quarter2_earnings_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ2 earnings estimates in the past 30 days |
| 341 | `analysts_count_revising_up_year2_ebitda_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their FY2 EBITDA estimates in the past 14 days |
| 342 | `count_analyst_downward_revision_next_quarter_ebitda_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their EBITDA estimates for fiscal quarter 2 (FQ2) in the past 30 days |
| 343 | `count_analyst_downward_revision_quarter_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts lowering FQ1 earnings estimates in the past 14 days |
| 344 | `count_analyst_downward_revision_quarter_ebitda_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their FQ1 EBITDA estimates in the past 14 days |
| 345 | `count_analyst_downward_revision_quarter_ebitda_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered Fiscal Quarter 1 EBITDA estimates over the past 7 days |
| 346 | `count_analyst_downward_revision_quarter_revenue_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for the next fiscal quarter (FQ1) in the past 30 days |
| 347 | `count_analyst_downward_revision_quarter_revenue_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for the next fiscal quarter (FQ1) in the past 7 days |
| 348 | `count_analyst_downward_revision_year_ebitda_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their EBITDA estimates for the current fiscal year (FY1) in the past 30 days |
| 349 | `count_analyst_downward_revision_year_ebitda_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their EBITDA estimates for the current fiscal year (FY1) in the past 7 days |
| 350 | `count_analyst_downward_revision_year_revenue_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for the current fiscal year (FY1) in the past 30 days |
| 351 | `count_analyst_recommendation_downgrades_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the past 14 days |
| 352 | `count_analyst_recommendation_downgrades_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the past 30 days |
| 353 | `count_analyst_recommendation_downgrades_60d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the past 60 days |
| 354 | `count_analyst_recommendation_downgrades_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the past 7 days |
| 355 | `count_analyst_recommendation_downgrades_90d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation downgrades over the past 90 days |
| 356 | `count_analyst_recommendation_upgrades_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the past 14 days |
| 357 | `count_analyst_recommendation_upgrades_60d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the past 60 days |
| 358 | `count_analyst_recommendation_upgrades_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the past 7 days |
| 359 | `count_analyst_recommendation_upgrades_90d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst recommendation upgrades over the past 90 days |
| 360 | `count_analyst_upward_revision_next_quarter_ebitda_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up FQ2 EBITDA estimates in the last 14 days |
| 361 | `count_analyst_upward_revision_next_quarter_revenue_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised FQ2 revenue estimates in the past 30 days |
| 362 | `count_analyst_upward_revision_next_quarter_revenue_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts raising FQ2 revenue estimates in the past 7 days |
| 363 | `count_analyst_upward_revision_next_year_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised Fiscal Year 2 earnings estimates over the past 14 days |
| 364 | `count_analyst_upward_revision_next_year_ebitda_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up EBITDA estimates for Fiscal Year 2 over the last 30 days |
| 365 | `count_analyst_upward_revision_next_year_revenue_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up Fiscal Year 2 revenue estimates over the last 7 days |
| 366 | `count_analyst_upward_revision_quarter_earnings_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised Fiscal Quarter 1 earnings estimates in the last 30 days |
| 367 | `count_analyst_upward_revision_quarter_revenue_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ1 revenue estimates over the last 14 days |
| 368 | `count_analyst_upward_revision_quarter_revenue_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised Fiscal Quarter 1 revenue estimates over the past 7 days |
| 369 | `count_analyst_upward_revision_year_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their Fiscal Year 1 earnings estimates over the last 14 days |
| 370 | `count_analyst_upward_revision_year_earnings_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FY1 earnings estimates in the last 7 days |
| 371 | `count_analyst_upward_revision_year_ebitda_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts raising FY1 EBITDA estimates in the past 14 days |
| 372 | `count_analyst_upward_revision_year_revenue_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their FY1 revenue estimates in the past 14 days |
| 373 | `count_analyst_upward_revision_year_revenue_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up Fiscal Year 1 revenue estimates over the last 7 days |
| 374 | `count_analysts_lower_curr_qtr_earnings_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down earnings estimates for Fiscal Quarter 1 over the last 30 days |
| 375 | `count_analysts_lower_curr_qtr_ebitda_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising down EBITDA estimates for Fiscal Quarter 1 over the last 30 days |
| 376 | `count_analysts_lower_curr_qtr_revenue_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for the next fiscal quarter (FQ1) in the past 14 days |
| 377 | `count_analysts_lower_earnings_est_next_qtr_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their earnings estimates for fiscal quarter 2 (FQ2) in the past 30 days |
| 378 | `count_analysts_lower_earnings_est_next_qtr_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their earnings estimates for fiscal quarter 2 (FQ2) in the past 7 days |
| 379 | `count_analysts_lower_earnings_est_year_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their earnings estimates for the current fiscal year (FY1) in the past 7 days |
| 380 | `count_analysts_lower_ebitda_est_next_qtr_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their EBITDA estimates for fiscal quarter 2 (FQ2) in the past 14 days |
| 381 | `count_analysts_lower_next_year_earnings_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their earnings estimates for the current fiscal year (FY1) in the past 30 days |
| 382 | `count_analysts_lower_next_year_revenue_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for the current fiscal year (FY1) in the past 14 days |
| 383 | `count_analysts_lower_qtr2_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their earnings estimates for fiscal quarter 2 (FQ2) in the past 14 days |
| 384 | `count_analysts_lower_qtr2_ebitda_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their EBITDA estimates for fiscal quarter 2 (FQ2) in the past 7 days |
| 385 | `count_analysts_lower_qtr2_revenue_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for fiscal quarter 2 (FQ2) in the past 30 days |
| 386 | `count_analysts_lower_qtr2_revenue_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for fiscal quarter 2 (FQ2) in the past 7 days |
| 387 | `count_analysts_lower_revenue_est_next_qtr_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for fiscal quarter 2 (FQ2) in the past 14 days |
| 388 | `count_analysts_lower_revenue_est_year_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who lowered their revenue estimates for the current fiscal year (FY1) in the past 7 days |
| 389 | `count_analysts_raise_curr_qtr_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their Fiscal Quarter 1 earnings estimates over the last 14 days |
| 390 | `count_analysts_raise_curr_qtr_ebitda_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised Fiscal Quarter 1 EBITDA estimates over the past 14 days |
| 391 | `count_analysts_raise_curr_qtr_ebitda_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FQ1 EBITDA estimates in the last 30 days |
| 392 | `count_analysts_raise_earnings_est_qtr_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Quarter 1 over the last 7 days |
| 393 | `count_analysts_raise_ebitda_est_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised Fiscal Quarter 1 EBITDA estimates over the past 7 days |
| 394 | `count_analysts_raise_ebitda_est_next_qtr_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised Fiscal Quarter 2 EBITDA estimates in the past 30 days |
| 395 | `count_analysts_raise_ebitda_est_next_qtr_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised Fiscal Quarter 2 EBITDA estimates over the past 7 days |
| 396 | `count_analysts_raise_next_year_earnings_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their earnings estimates for Fiscal Year 1 (FY1) in the past 30 calendar days |
| 397 | `count_analysts_raise_next_year_ebitda_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised Fiscal Year 1 EBITDA estimates over the past 30 days |
| 398 | `count_analysts_raise_next_year_ebitda_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up FY1 EBITDA estimates in the last 7 days |
| 399 | `count_analysts_raise_next_year_revenue_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FY1 revenue estimates over the last 30 days |
| 400 | `count_analysts_raise_qtr2_earnings_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up Fiscal Quarter 2 earnings estimates over the last 14 days |
| 401 | `count_analysts_raise_qtr2_earnings_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Quarter 2 over the last 7 days |
| 402 | `count_analysts_raise_revenue_est_next_qtr_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up FQ2 revenue estimates in the last 14 days |
| 403 | `count_analysts_raise_revenue_est_qtr_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised Fiscal Quarter 1 revenue estimates in the past 30 days |
| 404 | `count_analysts_raise_year2_earnings_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts who raised their earnings estimates for Fiscal Year 2 (FY2) in the past 30 calendar days |
| 405 | `count_analysts_raise_year2_earnings_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts revising up earnings estimates for Fiscal Year 2 over the last 7 days |
| 406 | `count_analysts_raise_year2_ebitda_7d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised their FY2 EBITDA estimates over the last 7 days |
| 407 | `count_analysts_raise_year2_revenue_14d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who raised FY2 revenue estimates in the past 14 days |
| 408 | `count_analysts_raise_year2_revenue_30d` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts who revised up Fiscal Year 2 revenue estimates over the last 30 days |
| 409 | `new_model_activity_indicator` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating newly detected activity or updates in the StarMine ARM dataset for the company since the prior day |
| 410 | `avg_pct_change_estimate_next_year_earnings_7d` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 earnings estimates over the last 7 days |
| 411 | `avg_pct_change_earnings_est_year_14d` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in earnings estimates for Fiscal Year 1 over the last 14 days |
| 412 | `country_percentile_rank_model_score` | MATRIX | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Country-level percentile rank of the ARM headline signal (1–100) |
| 413 | `country_percentile_rank_score` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Country-level percentile rank of the ARM signal 1–100, higher indicates stronger revision prospects |
| 414 | `global_percentile_rank_score` | MATRIX | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global percentile rank of the ARM headline signal (1–100) |
| 415 | `global_percentile_score` | MATRIX | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank of the ARM composite signal (1–100, higher = better) |
| 416 | `region_rank_score_decimal` | MATRIX | 0.744 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region-specific relative rank of the ARM signal expressed as a decimal percentile |
| 417 | `region_score_component` | MATRIX | 0.744 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score component reflecting the regional ranking of the stock. |
| 418 | `score_analyst_estimate_revisions` | MATRIX | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Composite StarMine ARM percentile score reflecting the direction, breadth, and momentum of analyst estimate revisions |
| 419 | `score_avg_5d` | MATRIX | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | ARM score averaged over the past 5 days |
| 420 | `score_component_primary_earnings` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Preferred earnings component portion of the final ARM score |
| 421 | `score_component_primary_earnings_float` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | ARM preferred earnings component percentile score |
| 422 | `model_score_delta_3d` | MATRIX | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the StarMine ARM score over the last 3 days |
| 423 | `score_delta_1d` | MATRIX | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the ARM composite score over the last 1 day |
| 424 | `score_change_model_7d` | MATRIX | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the StarMine ARM composite score over the last 7 days |
| 425 | `avg_pct_change_estimate_next_year_earnings_30d` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in earnings estimates for Fiscal Year 1 over the last 30 days |
| 426 | `avg_pct_change_estimate_12m_earnings_7d` | MATRIX | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next 12 months earnings estimates over the last 7 days |
| 427 | `avg_pct_change_estimate_12m_earnings_14d` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next 12 months (F12M) earnings consensus estimates over the past 14 days |
| 428 | `score_change_model_30d` | MATRIX | 0.742 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the StarMine ARM composite score over the last 30 days |
| 429 | `avg_pct_change_estimate_next_year_earnings_60d` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 earnings estimates over the last 60 days |
| 430 | `avg_pct_change_earnings_est_12m_30d` | MATRIX | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next-12-months earnings estimates over the last 30 days |
| 431 | `avg_pct_change_revenue_est_year_7d` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Average percentage change in Fiscal Year 1 revenue estimates over the last 7 days |
| 432 | `avg_pct_change_estimate_next_year_revenue_14d` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 revenue estimates over the last 14 days |
| 433 | `avg_pct_change_estimate_year_revenue_30d` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 revenue estimates over the last 30 days |
| 434 | `model_score_delta_60d` | MATRIX | 0.741 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the StarMine ARM composite score over the last 60 days |
| 435 | `analyst_revision_revenue_score` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | ARM revenue component percentile score reflecting revenue-related estimate revisions |
| 436 | `revenue_revision_score_3` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Revenue component portion of the final ARM score expressed as a percentile 1–100 |
| 437 | `avg_estimate_change_pct_year1_earnings_90d` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in earnings estimates for Fiscal Year 1 over the last 90 days |
| 438 | `avg_pct_change_estimate_12m_earnings_60d` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for the next 12 months over the last 60 days |
| 439 | `avg_pct_change_estimate_12m_revenue_7d` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in forward 12-month revenue estimates over the last 7 days |
| 440 | `avg_pct_change_estimate_forward_revenue_14d` | MATRIX | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next 12 months revenue estimates over the last 14 days |
| 441 | `avg_pct_change_revenue_est_year_60d` | MATRIX | 0.739 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 revenue consensus estimates over the past 60 days |
| 442 | `avg_pct_change_estimate_12m_revenue_30d` | MATRIX | 0.739 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for the next 12 months over the last 30 days |
| 443 | `score_delta_90d` | MATRIX | 0.738 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the StarMine ARM score over the last 90 days |
| 444 | `avg_pct_change_earnings_est_12m_90d` | MATRIX | 0.738 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst earnings estimates for the next 12 months over the last 90 days |
| 445 | `price_to_mean_revenue_ratio_12m` | MATRIX | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean price-to-revenue estimate ratio for forward 12 months |
| 446 | `avg_estimate_change_pct_year1_revenue_90d` | MATRIX | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 revenue estimates over the last 90 days |
| 447 | `avg_pct_change_estimate_forward_revenue_60d` | MATRIX | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for the next 12 months over the last 60 days |
| 448 | `earnings_to_price_yield_smartest_12m` | MATRIX | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings yield percentage based on the StarMine SmartEstimate for the next 12 months |
| 449 | `price_to_mean_estimate_ratio_next_year_revenue` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using the mean (consensus) estimate for Fiscal Year 1 revenue |
| 450 | `price_to_mean_estimate_ratio_year2_revenue` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean price-to-revenue ratio for FY2 |
| 451 | `expected_surprise_year_earnings` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted earnings surprise amount for Fiscal Year 1 |
| 452 | `forecasted_surprise_pct_next_year_earnings` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the SmartEstimate and the mean consensus for Fiscal Year 1 earnings |
| 453 | `weighted_estimate_next_year_earnings` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted analyst consensus) for next fiscal year (FY1) earnings |
| 454 | `forecasted_surprise_earnings_next_year` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted earnings surprise amount for fiscal year 2 (SmartEstimate minus consensus mean) |
| 455 | `pct_expected_surprise_next_year_earnings` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percentage earnings surprise for Fiscal Year 2, i.e., SmartEstimate versus mean consensus as a percent of the mean |
| 456 | `weighted_estimate_next_year_earnings_2` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted analyst consensus) for the following fiscal year (FY2) earnings |
| 457 | `earnings_to_price_yield_smartest_next_year` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings-to-price yield percentage based on SmartEstimate for Fiscal Year 1 |
| 458 | `avg_pct_change_estimate_12m_revenue_90d` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in revenue estimates for the next 12 months over the last 90 days |
| 459 | `earnings_to_price_yield_smartest_year2` | MATRIX | 0.734 | 修正与预期 | 0 | — | — | — | UNTESTED | Earnings-to-Price yield percentage based on StarMine SmartEstimate for Fiscal Year 2 |
| 460 | `expected_surprise_forward_earnings_12m` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the SmartEstimate and the mean consensus for forward 12 months earnings |
| 461 | `forecasted_surprise_pct_earnings_12m` | MATRIX | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted surprise percentage for trailing 12 months earnings (actual minus predicted) |
| 462 | `weighted_estimate_12m_earnings` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine weighted consensus estimate for forward 12 months earnings |
| 463 | `avg_change_analyst_recommendation_7d` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 7 days |
| 464 | `avg_change_analyst_recommendation_14d` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 14 days |
| 465 | `forecasted_surprise_pct_year2_revenue` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percentage revenue surprise for Fiscal Year 2, i.e., SmartEstimate versus mean consensus as a percent of the mean |
| 466 | `forecasted_surprise_year2_revenue` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted revenue surprise amount for Fiscal Year 2 |
| 467 | `weighted_estimate_year2_revenue` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted analyst consensus) for the following fiscal year (FY2) revenue |
| 468 | `pct_expected_surprise_year_revenue` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percentage revenue surprise for Fiscal Year 1 (SmartEstimate vs mean consensus) |
| 469 | `predicted_surprise_pct_year1_revenue` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted revenue surprise amount for Fiscal Year 1 (SmartEstimate minus mean consensus) |
| 470 | `weighted_estimate_next_year_revenue` | MATRIX | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted analyst consensus) for next fiscal year (FY1) revenue |
| 471 | `avg_change_analyst_recommendation_30d` | MATRIX | 0.728 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 30 days |
| 472 | `reported_revenue_last_fiscal_year` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual revenue reported for the most recent fiscal year |
| 473 | `price_to_smartest_forward_revenue_ratio` | MATRIX | 0.728 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using StarMine SmartEstimate for forward 12 months revenue |
| 474 | `avg_change_analyst_recommendation_60d` | MATRIX | 0.727 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 60 days |
| 475 | `forecasted_surprise_12m_revenue` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted revenue surprise amount for forward 12 months |
| 476 | `forecasted_surprise_pct_12m_revenue` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted percentage revenue surprise for the next 12 months |
| 477 | `weighted_estimate_forward_12m_revenue` | MATRIX | 0.726 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine weighted consensus estimate for forward 12 months revenue |
| 478 | `price_to_smartest_estimate_ratio_year2_revenue` | MATRIX | 0.725 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using the StarMine SmartEstimate for Fiscal Year 2 revenue |
| 479 | `avg_change_analyst_recommendation_90d` | MATRIX | 0.725 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the mean analyst recommendation over the past 90 days |
| 480 | `price_to_smartest_estimate_ratio_next_year_revenue` | MATRIX | 0.724 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-revenue ratio using the StarMine SmartEstimate for Fiscal Year 1 revenue |
| 481 | `growth_rate_estimate_next_vs_current_year_revenue` | MATRIX | 0.724 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate for revenue, comparing next fiscal year to this fiscal year |
| 482 | `reported_earnings_last_fiscal_year` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual earnings reported for the most recent fiscal year |
| 483 | `pct_surprise_reported_revenue_previous_year` | MATRIX | 0.724 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise for the last year’s revenue, calculated as actual reported minus consensus estimate, expressed as a percent of the conse |
| 484 | `pct_surprise_reported_earnings_previous_year` | MATRIX | 0.723 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise for the last year’s earnings, calculated as actual reported minus consensus estimate, expressed as a percent of the cons |
| 485 | `recommendation_change_score` | MATRIX | 0.722 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendations component portion of the final ARM score expressed as a percentile 1–100 |
| 486 | `recommendation_change_score_component` | MATRIX | 0.722 | 修正与预期 | 0 | — | — | — | UNTESTED | ARM recommendations component percentile score reflecting recommendation momentum |
| 487 | `forward_pe_ratio_mean_year2` | MATRIX | 0.718 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on mean analyst estimates for Fiscal Year 2 |
| 488 | `price_to_mean_estimate_next_year_earnings_ratio` | MATRIX | 0.718 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean price-to-earnings estimate ratio for Fiscal Year 2 |
| 489 | `forward_pe_ratio_mean_12m` | MATRIX | 0.714 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on mean analyst estimates for the next 12 months (F12M) |
| 490 | `price_to_mean_earnings_ratio_12m` | MATRIX | 0.714 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean price-to-earnings estimate ratio for the next 12 months |
| 491 | `growth_rate_estimate_current_vs_prior_year_revenue` | MATRIX | 0.710 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate for revenue, comparing this fiscal year to last fiscal year |
| 492 | `forward_pe_ratio_smartest_year2` | MATRIX | 0.710 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on StarMine SmartEstimate for Fiscal Year 2 |
| 493 | `price_to_smartest_earnings_ratio_next_year` | MATRIX | 0.710 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the SmartEstimate for Fiscal Year 2 earnings |
| 494 | `forward_pe_ratio_smartest_12m` | MATRIX | 0.707 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on the SmartEstimate for the next 12 months |
| 495 | `price_to_smartest_estimate_ratio_12m_earnings` | MATRIX | 0.707 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio for the next 12 months based on the SmartEstimate of forward 12-month earnings |
| 496 | `forward_pe_ratio_mean_year` | MATRIX | 0.702 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on mean analyst estimates for Fiscal Year 1 |
| 497 | `price_to_mean_earnings_ratio_year` | MATRIX | 0.702 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the mean (consensus) estimate for Fiscal Year 1 earnings |
| 498 | `forward_pe_ratio_smartest_next_year` | MATRIX | 0.692 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward price-to-earnings ratio based on StarMine SmartEstimate for Fiscal Year 1 |
| 499 | `price_to_smartest_estimate_ratio_next_year_earnings` | MATRIX | 0.692 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using the StarMine SmartEstimate for Fiscal Year 1 earnings |
| 500 | `avg_pct_change_estimate_year_ebitda_7d` | MATRIX | 0.692 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in Fiscal Year 1 EBITDA estimates over the last 7 days |
| 501 | `avg_pct_change_estimate_next_year_ebitda_14d` | MATRIX | 0.691 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 EBITDA consensus estimates over the past 14 days |
| 502 | `secondary_earnings_score` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | Secondary earnings component portion of the final ARM score expressed as a percentile 1–100 |
| 503 | `secondary_earnings_score_component` | MATRIX | 0.691 | 修正与预期 | 0 | — | — | — | UNTESTED | Score component reflecting revisions and surprises in secondary earnings measures. |
| 504 | `smartest_growth_rate_next_vs_current_year_earnings` | MATRIX | 0.691 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate growth rate for earnings, comparing next fiscal year to this fiscal year |
| 505 | `avg_pct_change_estimate_year_ebitda_30d` | MATRIX | 0.690 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in FY1 EBITDA consensus estimates over the past 30 days |
| 506 | `avg_estimate_change_pct_f12m_ebitda_7d` | MATRIX | 0.690 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in analyst EBITDA estimates for the next 12 months over the last 7 days |
| 507 | `avg_pct_change_ebitda_est_12m_14d` | MATRIX | 0.689 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next 12 months (F12M) EBITDA estimates over the last 14 days |
| 508 | `avg_pct_change_estimate_12m_ebitda_30d` | MATRIX | 0.688 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in forward 12-month EBITDA estimates over the last 30 days |
| 509 | `avg_pct_change_estimate_year_ebitda_60d` | MATRIX | 0.688 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in the consensus EBITDA estimate for Fiscal Year 1 (next fiscal year) over the last 60 days |
| 510 | `avg_pct_change_estimate_year_ebitda_90d` | MATRIX | 0.685 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in Fiscal Year 1 EBITDA estimates over the last 90 days |
| 511 | `avg_pct_change_estimate_12m_ebitda_60d` | MATRIX | 0.685 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next 12 months (F12M) EBITDA estimates over the last 60 days |
| 512 | `avg_pct_change_ebitda_est_12m_90d` | MATRIX | 0.682 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean percentage change in next 12 months EBITDA estimates over the last 90 days |
| 513 | `expected_surprise_year_ebitda` | MATRIX | 0.680 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the SmartEstimate and the mean consensus for Fiscal Year 1 EBITDA |
| 514 | `pct_expected_surprise_year_ebitda` | MATRIX | 0.680 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted percentage surprise for FY1 EBITDA, i.e., (SmartEstimate − mean) / mean |
| 515 | `weighted_estimate_next_year_ebitda` | MATRIX | 0.680 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (proprietary weighted analyst consensus) for next fiscal year (FY1) EBITDA |
| 516 | `pct_expected_surprise_next_year_ebitda` | MATRIX | 0.680 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted percentage EBITDA surprise for FY2 (SmartEstimate vs mean) |
| 517 | `predicted_surprise_pct_year2_ebitda` | MATRIX | 0.680 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine predicted EBITDA surprise amount for Fiscal Year 2 (SmartEstimate minus mean consensus) |
| 518 | `weighted_estimate_next_year_ebitda_2` | MATRIX | 0.680 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate consensus for FY2 EBITDA |
| 519 | `expected_surprise_forward_ebitda_12m` | MATRIX | 0.677 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the SmartEstimate and the mean consensus for forward 12 months EBITDA |
| 520 | `forecasted_surprise_pct_ebitda_12m` | MATRIX | 0.677 | 盈利与财务 | 0 | — | — | — | UNTESTED | StarMine predicted percentage EBITDA surprise for the next 12 months (F12M) |
| 521 | `weighted_estimate_12m_ebitda` | MATRIX | 0.677 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine weighted consensus estimate for forward 12 months EBITDA |
| 522 | `price_to_mean_estimate_ratio_12m_ebitda` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean price-to-EBITDA estimate ratio for the next 12 months |
| 523 | `price_to_mean_estimate_ratio_year2_ebitda` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean price-to-EBITDA estimate ratio for Fiscal Year 2 |
| 524 | `mean_estimate_to_price_ratio_year1_ebitda` | MATRIX | 0.667 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean price-to-EBITDA ratio for FY1 |
| 525 | `price_to_smartest_forward_ebitda_ratio` | MATRIX | 0.663 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using StarMine SmartEstimate for forward 12 months EBITDA |
| 526 | `pe_ratio_previous_fiscal_year` | MATRIX | 0.663 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio using earnings from the last completed fiscal year |
| 527 | `price_to_smartest_next_year_ebitda_ratio` | MATRIX | 0.662 | 修正与预期 | 0 | — | — | — | UNTESTED | Price-to-EBITDA ratio using the StarMine SmartEstimate for Fiscal Year 2 EBITDA |
| 528 | `price_to_smartest_ebitda_ratio_year` | MATRIX | 0.655 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate price-to-EBITDA ratio for FY1 |
| 529 | `smartest_growth_ebitda_next_vs_this_year` | MATRIX | 0.655 | 修正与预期 | 0 | — | — | — | UNTESTED | Growth rate of EBITDA from this fiscal year to next fiscal year based on the SmartEstimate |
| 530 | `growth_rate_estimate_current_vs_prior_year_earnings` | MATRIX | 0.654 | 修正与预期 | 0 | — | — | — | UNTESTED | Model SmartEstimate earnings growth (this year versus last year) |
| 531 | `reported_ebitda_previous_year` | MATRIX | 0.649 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual EBITDA reported for the most recent fiscal year |
| 532 | `pct_surprise_reported_ebitda_previous_year` | MATRIX | 0.647 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage surprise for the last year’s EBITDA, calculated as actual reported minus consensus estimate, expressed as a percent of the consen |
| 533 | `growth_rate_estimate_current_vs_prior_year_ebitda` | MATRIX | 0.607 | 修正与预期 | 0 | — | — | — | UNTESTED | Growth rate of EBITDA from last fiscal year to this fiscal year based on the SmartEstimate |
| 534 | `mdl26_actual_last_q_revenue` | MATRIX | 0.515 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual revenue reported for the most recent fiscal quarter |
| 535 | `mdl26_srprs_pct_lst_q_rvn` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage surprise for last quarter revenue: (actual minus predicted) divided by predicted, expressed as a percentage |
| 536 | `mdl26_prsprise_fq1_revenue` | MATRIX | 0.463 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between the StarMine SmartEstimate and the mean consensus for fiscal quarter 1 revenue (Predicted Surprise amount) |
| 537 | `mdl26_prsprise_pct_fq1_revenue` | MATRIX | 0.463 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage revenue surprise for the next fiscal quarter (SmartEstimate versus mean consensus) |
| 538 | `mdl26_smartestimate_fq1_revenue` | MATRIX | 0.463 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted consensus) for fiscal quarter 1 revenue |
| 539 | `mdl26_mstchg_pct_fq1_rvn_7` | MATRIX | 0.453 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 7 days |
| 540 | `mdl26_mstchg_pct_fq1_rvn_14` | MATRIX | 0.441 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 14 days |
| 541 | `mdl26_mstchg_pct_fq1_rvn_30` | MATRIX | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 30 days |
| 542 | `mdl26_divisor_fq1_earnings` | MATRIX | 0.407 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scaling divisor used in calculations for FQ1 earnings |
| 543 | `mdl26_mstchg_pct_fq1_rnngs_7` | MATRIX | 0.406 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 7 days |
| 544 | `mdl26_prsprise_pct_fq1_earnings` | MATRIX | 0.406 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage earnings surprise for the next fiscal quarter (SmartEstimate versus mean consensus) |
| 545 | `mdl26_sm_stm_fq1_rnngs` | MATRIX | 0.406 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted consensus) for fiscal quarter 1 earnings |
| 546 | `mdl26_sma_prsprise_fq1_earnings` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted earnings surprise amount for fiscal quarter 1 |
| 547 | `mdl26_mstchg_pct_fq1_rvn_60` | MATRIX | 0.404 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 60 days |
| 548 | `mdl26_sma_actual_last_q_earnings` | MATRIX | 0.403 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual earnings reported for the most recent fiscal quarter |
| 549 | `mdl26_mn_stmt_prr_fq1_rnngs_7` | MATRIX | 0.402 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean FQ1 earnings estimate as of 7 days prior |
| 550 | `mdl26_nm_mn_nlysts_prr_fq1_rnngs_7` | MATRIX | 0.402 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts contributing to the mean FQ1 earnings estimate 7 days prior |
| 551 | `mdl26_mstchg_pct_fq1_rnngs_14` | MATRIX | 0.401 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 14 days |
| 552 | `mdl26_prsprise_fq1_earnings` | MATRIX | 0.401 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted earnings surprise amount for fiscal quarter 1, i.e., SmartEstimate minus consensus mean |
| 553 | `mdl26_prsprise_per_fq1_earnings` | MATRIX | 0.401 | 盈利与财务 | 0 | — | — | — | UNUSABLE | predicted surprise (actual value - predicted value) per FQTR1 earnings |
| 554 | `mdl26_smartestimate_fq1_earnings` | MATRIX | 0.401 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate for fiscal Q1 earnings |
| 555 | `mdl26_stdv_stm_nlysts_fq1_rnngs` | MATRIX | 0.401 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates contributing to the FQ1 earnings SmartEstimate |
| 556 | `mdl26_actual_last_q_earnings` | MATRIX | 0.398 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual earnings reported for the most recent fiscal quarter |
| 557 | `mdl26_stm_prr_fq1_rnngs_7` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | The StarMine SmartEstimate for Fiscal Quarter 1 earnings as of seven days prior |
| 558 | `mdl26_mstchg_pct_fq1_rnngs_30` | MATRIX | 0.393 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 30 days |
| 559 | `mdl26_srprs_pct_lst_q_rnngs` | MATRIX | 0.391 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage surprise for last quarter earnings: (actual minus predicted) divided by predicted, expressed as a percentage |
| 560 | `mdl26_mstchg_pct_fq1_rvn_90` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 90 days |
| 561 | `mdl26_hgh_stmt_prr_fq1_rnngs_30` | MATRIX | 0.390 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest earnings estimate for Fiscal Quarter 1 recorded 30 days prior |
| 562 | `mdl26_lw_stmt_prr_fq1_rnngs_30` | MATRIX | 0.390 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest earnings estimate for Fiscal Quarter 1 recorded 30 days prior |
| 563 | `mdl26_mstchg_pct_fq2_rvn_7` | MATRIX | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 2 over the last 7 days |
| 564 | `mdl26_hgh_stmt_chng_fq1_rnngs_30` | MATRIX | 0.388 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the highest FQ1 earnings estimate over the past 30 days |
| 565 | `mdl26_lw_stmt_chng_fq1_rnngs_30` | MATRIX | 0.388 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the lowest FQ1 earnings estimate over the past 30 days |
| 566 | `mdl26_mstchg_fq1_rnngs_30` | MATRIX | 0.388 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the mean earnings estimate for Fiscal Quarter 1 over the last 30 days |
| 567 | `mdl26_prsprise_fq2_revenue` | MATRIX | 0.387 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted revenue surprise amount for Fiscal Quarter 2 |
| 568 | `mdl26_prsprise_pct_fq2_revenue` | MATRIX | 0.387 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal quarter 2 revenue (Predicted Surprise %) |
| 569 | `mdl26_smartestimate_fq2_revenue` | MATRIX | 0.387 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted consensus) for revenue for Fiscal Quarter 2 |
| 570 | `mdl26_surprise_last_q_earnings` | MATRIX | 0.387 | 修正与预期 | 0 | — | — | — | UNUSABLE | Earnings surprise for the last reported quarter calculated as actual minus predicted estimate |
| 571 | `mdl26_mstchg_pct_fq2_rvn_14` | MATRIX | 0.386 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 2 over the last 14 days |
| 572 | `mdl26_mstchg_pct_fq1_rnngs_60` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 60 days |
| 573 | `reported_revenue_last_quarter` | MATRIX | 0.380 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual revenue reported for the most recent fiscal quarter |
| 574 | `mdl26_stm_chng_fq1_rnngs_30` | MATRIX | 0.379 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the SmartEstimate for FQ1 earnings over the past 30 days |
| 575 | `mdl26_mstchg_pct_fq2_rvn_30` | MATRIX | 0.377 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in analyst revenue estimates for Fiscal Quarter 2 over the past 30 days |
| 576 | `mdl26_mstchg_pct_fq2_rnngs_7` | MATRIX | 0.374 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 7 days |
| 577 | `mdl26_mstchg_pct_fq1_rnngs_90` | MATRIX | 0.374 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 90 days |
| 578 | `mdl26_mstchg_pct_fq2_rnngs_14` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 14 days |
| 579 | `mdl26_prsprise_fq2_earnings` | MATRIX | 0.370 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted earnings surprise amount for Fiscal Quarter 2 |
| 580 | `mdl26_prsprise_pct_fq2_earnings` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal quarter 2 earnings (Predicted Surprise %) |
| 581 | `mdl26_smartestimate_fq2_earnings` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted consensus) for earnings for Fiscal Quarter 2 |
| 582 | `mdl26_mstchg_pct_fq2_rnngs_30` | MATRIX | 0.362 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 30 days |
| 583 | `mdl26_mstchg_pct_fq2_rvn_60` | MATRIX | 0.361 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in analyst revenue estimates for Fiscal Quarter 2 over the past 60 days |
| 584 | `mdl26_60dy_srprs_lst_q_rnngs` | MATRIX | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 60day surprise (actual value - predicted value) last QTR earnings |
| 585 | `mdl26_prsprise_fq1_ebitda` | MATRIX | 0.355 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between the StarMine SmartEstimate and the mean consensus for fiscal quarter 1 EBITDA (Predicted Surprise amount) |
| 586 | `mdl26_prsprise_pct_fq1_ebitda` | MATRIX | 0.355 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage EBITDA surprise for the next fiscal quarter (SmartEstimate versus mean consensus) |
| 587 | `mdl26_smartestimate_fq1_ebitda` | MATRIX | 0.355 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted consensus) for fiscal quarter 1 EBITDA |
| 588 | `mdl26_actual_last_q_ebitda` | MATRIX | 0.355 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual EBITDA reported for the most recent fiscal quarter |
| 589 | `mdl26_mstchg_pct_fq2_rnngs_60` | MATRIX | 0.347 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 60 days |
| 590 | `mdl26_surprise_pct_last_q_ebitda` | MATRIX | 0.346 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage surprise for last quarter EBITDA: (actual minus predicted) divided by predicted, expressed as a percentage |
| 591 | `mdl26_mstchg_pct_fq1_btd_7` | MATRIX | 0.345 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 7 days |
| 592 | `mdl26_mstchg_pct_fq2_rvn_90` | MATRIX | 0.344 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in analyst revenue estimates for Fiscal Quarter 2 over the past 90 days |
| 593 | `mdl26_avrevsn_fq1_earnings_30` | MATRIX | 0.334 | 修正与预期 | 0 | — | — | — | UNUSABLE | average revision FQTR1 earnings: 30 days |
| 594 | `mdl26_stmt_dffsn_fq1_rnngs_30` | MATRIX | 0.334 | 修正与预期 | 0 | — | — | — | UNUSABLE | Measure of dispersion (variability) among analysts’ earnings estimates for Fiscal Quarter 1 over the past 30 days |
| 595 | `mdl26_mstchg_pct_fq1_btd_14` | MATRIX | 0.332 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 14 days |
| 596 | `mdl26_mstchg_pct_fq2_rnngs_90` | MATRIX | 0.332 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 90 days |
| 597 | `pct_surprise_reported_revenue_previous_quarter` | MATRIX | 0.328 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage surprise for the last quarter’s revenue, calculated as actual reported minus consensus estimate, expressed as a percent of the co |
| 598 | `expected_surprise_quarter_revenue` | MATRIX | 0.319 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted revenue surprise amount for Fiscal Quarter 1 |
| 599 | `pct_expected_surprise_quarter_revenue` | MATRIX | 0.319 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage revenue surprise for Fiscal Quarter 1 |
| 600 | `weighted_estimate_curr_qtr_revenue` | MATRIX | 0.319 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine weighted consensus estimate for Fiscal Quarter 1 revenue |
| 601 | `mdl26_sma_trailing_4_quarter_pe` | MATRIX | 0.316 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price to earnings ratio using earnings from the most recent four reported quarters |
| 602 | `mdl26_mstchg_pct_fq1_btd_30` | MATRIX | 0.314 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 30 days |
| 603 | `mdl26_trailing_4_quarter_pe` | MATRIX | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price-to-earnings ratio using the sum of earnings per share over the most recent four reported quarters |
| 604 | `mdl26_7dy_mn_chng_flg_fq1_rnngs` | MATRIX | 0.309 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 7day mean change flag FQTR1 earnings |
| 605 | `avg_pct_change_estimate_quarter_revenue_7d` | MATRIX | 0.309 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 7 days |
| 606 | `mdl26_mstchg_pct_fq1_btd_60` | MATRIX | 0.299 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 60 days |
| 607 | `avg_pct_change_estimate_quarter_revenue_14d` | MATRIX | 0.298 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 14 days |
| 608 | `mdl26_mstchg_pct_fq1_btd_90` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 90 days |
| 609 | `mdl26_mstchg_pct_fq2_btd_7` | MATRIX | 0.284 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 7 days |
| 610 | `avg_pct_change_estimate_curr_qtr_revenue_30d` | MATRIX | 0.283 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 30 days |
| 611 | `mdl26_prsprise_fq2_ebitda` | MATRIX | 0.283 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between the StarMine SmartEstimate and the mean consensus for fiscal quarter 2 EBITDA (Predicted Surprise amount) |
| 612 | `mdl26_prsprise_pct_fq2_ebitda` | MATRIX | 0.283 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage difference between the StarMine SmartEstimate and the mean consensus for fiscal quarter 2 EBITDA (Predicted Surprise %) |
| 613 | `mdl26_smartestimate_fq2_ebitda` | MATRIX | 0.283 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted consensus) for EBITDA for Fiscal Quarter 2 |
| 614 | `mdl26_mstchg_pct_fq2_btd_14` | MATRIX | 0.280 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 14 days |
| 615 | `reported_earnings_previous_quarter` | MATRIX | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual earnings reported for the most recent fiscal quarter |
| 616 | `star_arm_rec_change_flag` | MATRIX | 0.274 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating whether the mean recommendation changed over the last 7 days |
| 617 | `mdl26_mstchg_pct_fq2_btd_30` | MATRIX | 0.272 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 30 days |
| 618 | `avg_estimate_change_pct_quarter1_revenue_60d` | MATRIX | 0.271 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 60 days |
| 619 | `expected_surprise_quarter_earnings` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted earnings surprise amount for FQ1 (SmartEstimate minus consensus mean) |
| 620 | `forecasted_surprise_pct_earnings_qtr` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage earnings surprise for FQ1 (SmartEstimate vs mean) |
| 621 | `weighted_estimate_quarter_earnings` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine weighted consensus estimate for Fiscal Quarter 1 earnings |
| 622 | `avg_pct_change_estimate_quarter_earnings_7d` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 7 days |
| 623 | `avg_pct_change_earnings_est_qtr_14d` | MATRIX | 0.265 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 14 days |
| 624 | `actual_vs_predicted_earnings_surprise_pct_lastq` | MATRIX | 0.263 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage surprise for the last quarter’s earnings, calculated as actual reported minus consensus estimate, expressed as a percent of the c |
| 625 | `avg_pct_change_revenue_est_qtr_90d` | MATRIX | 0.262 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 1 over the last 90 days |
| 626 | `avg_pct_change_earnings_est_qtr_30d` | MATRIX | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 30 days |
| 627 | `mdl26_mstchg_pct_fq2_btd_60` | MATRIX | 0.258 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 60 days |
| 628 | `avg_pct_change_estimate_qtr2_revenue_7d` | MATRIX | 0.258 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in FQ2 revenue estimates over the last 7 days |
| 629 | `forecasted_surprise_curr_qtr2_revenue` | MATRIX | 0.256 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted revenue surprise amount for Fiscal Quarter 2 (SmartEstimate minus mean consensus) |
| 630 | `forecasted_surprise_pct_qtr2_revenue` | MATRIX | 0.256 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage revenue surprise for Fiscal Quarter 2 |
| 631 | `weighted_estimate_next_quarter_revenue` | MATRIX | 0.256 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted analyst consensus) for Fiscal Quarter 2 revenue |
| 632 | `avg_pct_change_estimate_next_quarter_revenue_14d` | MATRIX | 0.255 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in revenue estimates for Fiscal Quarter 2 over the last 14 days |
| 633 | `mdl26_dsnc_clstr_bgn_fq1_rnngs` | MATRIX | 0.254 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of days since the current revision cluster for Fiscal Quarter 1 earnings began |
| 634 | `mdl26_dsnc_clstr_dtctd_fq1_rnngs` | MATRIX | 0.254 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of days since a revision cluster was detected for fiscal quarter 1 earnings |
| 635 | `avg_pct_change_earnings_est_qtr_60d` | MATRIX | 0.253 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 60 days |
| 636 | `mdl26_mn_f_rvsnclstr_nlysts_fq1_rnngs` | MATRIX | 0.253 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average revision amount among analysts in the detected revision cluster for Fiscal Quarter 1 earnings |
| 637 | `mdl26_nm_rvsnclstr_nlysts_fq1_rnngs` | MATRIX | 0.253 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of analysts included in the current revision cluster for Fiscal Quarter 1 earnings |
| 638 | `mdl26_stdv_rvsnclstr_nlysts_fq1_rnngs` | MATRIX | 0.253 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of revision amounts among analysts in the revision cluster for Fiscal Quarter 1 earnings |
| 639 | `avg_pct_change_estimate_qtr2_revenue_30d` | MATRIX | 0.249 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in Fiscal Quarter 2 revenue estimates over the last 30 days |
| 640 | `reported_ebitda_last_quarter` | MATRIX | 0.247 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual EBITDA reported for the most recent fiscal quarter |
| 641 | `avg_pct_change_estimate_quarter_earnings_90d` | MATRIX | 0.246 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 1 over the last 90 days |
| 642 | `forecasted_surprise_ebitda_qtr` | MATRIX | 0.245 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted EBITDA surprise amount for Fiscal Quarter 1 (SmartEstimate minus mean consensus) |
| 643 | `forecasted_surprise_pct_curr_qtr_ebitda` | MATRIX | 0.245 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage EBITDA surprise for Fiscal Quarter 1 |
| 644 | `weighted_estimate_curr_qtr_ebitda` | MATRIX | 0.245 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine weighted consensus estimate for Fiscal Quarter 1 EBITDA |
| 645 | `avg_pct_change_estimate_qtr2_earnings_7d` | MATRIX | 0.244 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 7 days |
| 646 | `avg_pct_change_estimate_next_quarter_earnings_14d` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 14 days |
| 647 | `expected_surprise_next_quarter_earnings` | MATRIX | 0.242 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted earnings surprise amount for Fiscal Quarter 2 |
| 648 | `pct_expected_surprise_next_quarter_earnings` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage earnings surprise for Fiscal Quarter 2 (SmartEstimate vs mean consensus) |
| 649 | `weighted_estimate_next_quarter_earnings` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (weighted consensus) for Fiscal Quarter 2 earnings |
| 650 | `actual_vs_predicted_ebitda_surprise_pct_lastq` | MATRIX | 0.239 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage surprise for the last quarter’s EBITDA, calculated as actual reported minus consensus estimate, expressed as a percent of the con |
| 651 | `avg_pct_change_estimate_next_quarter_revenue_60d` | MATRIX | 0.238 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in FQ2 revenue estimates over the last 60 days |
| 652 | `avg_pct_change_estimate_curr_qtr_ebitda_7d` | MATRIX | 0.237 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 7 days |
| 653 | `avg_pct_change_estimate_qtr2_earnings_30d` | MATRIX | 0.236 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 30 days |
| 654 | `avg_estimate_change_pct_quarter1_ebitda_14d` | MATRIX | 0.227 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 14 days |
| 655 | `avg_pct_change_estimate_qtr2_revenue_90d` | MATRIX | 0.226 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in FQ2 revenue estimates over the last 90 days |
| 656 | `avg_pct_change_estimate_qtr2_earnings_60d` | MATRIX | 0.225 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 60 days |
| 657 | `avg_pct_change_estimate_quarter_ebitda_30d` | MATRIX | 0.215 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 30 days |
| 658 | `avg_pct_change_estimate_qtr2_earnings_90d` | MATRIX | 0.214 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in earnings estimates for Fiscal Quarter 2 over the last 90 days |
| 659 | `pe_ratio_trailing_4q_2` | MATRIX | 0.207 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Price-to-earnings ratio using earnings from the most recent four reported quarters |
| 660 | `avg_pct_change_estimate_quarter_ebitda_60d` | MATRIX | 0.205 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 1 over the last 60 days |
| 661 | `avg_pct_change_estimate_curr_qtr_ebitda_90d` | MATRIX | 0.197 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in FQ1 EBITDA estimates over the last 90 days |
| 662 | `avg_pct_change_estimate_next_quarter_ebitda_7d` | MATRIX | 0.194 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 7 days |
| 663 | `expected_surprise_next_quarter_ebitda` | MATRIX | 0.193 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted EBITDA surprise amount for Fiscal Quarter 2 |
| 664 | `pct_expected_surprise_next_quarter_ebitda` | MATRIX | 0.193 | 盈利与财务 | 0 | — | — | — | UNUSABLE | StarMine predicted percentage EBITDA surprise for Fiscal Quarter 2 |
| 665 | `weighted_estimate_qtr2_ebitda` | MATRIX | 0.193 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (proprietary weighted analyst consensus) for Fiscal Quarter 2 EBITDA |
| 666 | `avg_pct_change_estimate_next_quarter_ebitda_14d` | MATRIX | 0.191 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 14 days |
| 667 | `avg_pct_change_estimate_next_quarter_ebitda_30d` | MATRIX | 0.185 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 30 days |
| 668 | `avg_estimate_change_pct_quarter2_ebitda_60d` | MATRIX | 0.175 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 60 days |
| 669 | `avg_pct_change_ebitda_est_next_qtr_90d` | MATRIX | 0.165 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 90 days |
| 670 | `avg_pct_change_ebitda_est_next_qtr_90d_d1` | MATRIX | 0.165 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean percentage change in EBITDA estimates for Fiscal Quarter 2 over the last 90 days |
| 671 | `mdl26_dsnc_lst_ps_prnnncmnt` | MATRIX | 0.134 | 其他 | 0 | — | — | — | UNUSABLE | Number of days since the company’s last positive pre-announcement |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

