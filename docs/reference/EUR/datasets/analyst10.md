# analyst10 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst10` |
| 名称 | Performance-Weighted Analyst Estimates |
| 类别 | ANALYST |
| 数据字段数(平台) | 961 |
| 覆盖率 | 0.7695 |
| 平台已有 alpha | 1433 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset applies an enhanced version of the StarMine SmartEstimate model to a broad universe of stocks and financial metrics, leveraging analyst estimate data from IBES. It calculates a performance score for each analyst based on their historical forecasting accuracy and incorporates the recency of their estimates. By combining these two factors, the model generates "smart estimates" that are more predictive than simple consensus means. The dataset includes modules for analyst innovation, outlier handling, and time-series feature generation, making it a robust tool for identifying which analyst forecasts are likely to be most accurate. This can help investors and researchers anticipate earnings surprises and price movements, as changes in smart estimates often precede market reactions.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **961** |
| 类型分布 | MATRIX×841　VECTOR×120 |
| 平均覆盖率 | **0.769** |
| 覆盖率区间 | 0.25 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 506 | 52.7% |
| 中 (0.70–0.90) | 113 | 11.8% |
| 低 (0.50–0.70) | 92 | 9.6% |
| 稀疏 (<0.50) | 250 | 26.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 629 | 65.5% |
| UNUSABLE | 325 | 33.8% |
| DEAD | 7 | 0.7% |

- 已实测字段：**7** 个（1%），best_sharpe 最高 **0.64**，中位 0.53

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 891 | 0.77 | anl10_netfy1_pred_surps_v1_620、anl10_salfy1_pred_surps_v1_533、anl10_netinnovate_increase_fy1 |
| 盈利与财务 | 40 | 0.76 | anl10_ebtinnovation_score_fy1、anl10_dpsff、anl10_ebiff_7 |
| 风险与质量 | 16 | 0.70 | anl10_salinnovation_score_fy1、anl10_salinnovation_score_fy2、anl10_preinnovation_score_fy2 |
| 其他 | 9 | 0.94 | anl10_cpxff、anl10_cshff_760、anl10_ndtff |
| 价量与波动 | 5 | 0.70 | anl10_prrff、anl10_prrinnovation_score_fy1、anl10_prrinnovation_score_fy2 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl10_netfy1_pred_surps_v1_620` | MATRIX | 1.000 | 修正与预期 | 1 | 0.64 | 0.17 | 0.52 | DEAD | Predicted surprise version 1 for net income for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 2 | `anl10_salfy1_pred_surps_v1_533` | MATRIX | 1.000 | 修正与预期 | 1 | 0.58 | 0.79 | 0.54 | DEAD | Predicted surprise version 1 for sales for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 3 | `anl10_netinnovate_increase_fy1` | MATRIX | 0.998 | 修正与预期 | 1 | 0.55 | -0.39 | 0.37 | DEAD | Number of analysts with innovative positive revisions for net income FY1 |
| 4 | `anl10_ebtinnovation_score_fy1` | MATRIX | 0.920 | 盈利与财务 | 1 | 0.53 | -0.07 | 0.40 | DEAD | Innovation score for earnings before tax FY1 (innovate_increase - innovate_decrease) |
| 5 | `anl10_ebtfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 2 | 0.49 | -0.14 | 0.63 | DEAD | Predicted surprise version 1 for earnings before tax for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 6 | `anl10_ebtrevise_ratio_to_close_fy1` | MATRIX | 0.920 | 修正与预期 | 1 | 0.31 | -0.08 | 0.19 | DEAD | Ratio of delta consensus to adjusted close for earnings before tax FY1 |
| 7 | `anl10_prefy1_pred_surps_v1_474` | MATRIX | 1.000 | 修正与预期 | 1 | 0.29 | 0.25 | 0.10 | DEAD | Predicted surprise version 1 for pre-tax or preliminary for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 8 | `anl10_cpxff` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Capital expenditures - field format |
| 9 | `anl10_cpxfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for capital expenditures FY1 |
| 10 | `anl10_cpxfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for capital expenditures for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 11 | `anl10_cpxfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for capital expenditures for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 12 | `anl10_cpxfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for capital expenditures for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 13 | `anl10_cpxfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for capital expenditures for FY1 |
| 14 | `anl10_cpxfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for capital expenditures for FY1 |
| 15 | `anl10_cpxfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for capital expenditures for FY1 |
| 16 | `anl10_cpxfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for capital expenditures FY2 |
| 17 | `anl10_cpxfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for capital expenditures for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 18 | `anl10_cpxfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for capital expenditures for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 19 | `anl10_cpxfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for capital expenditures for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 20 | `anl10_cpxfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for capital expenditures for FY2 |
| 21 | `anl10_cpxfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for capital expenditures for FY2 |
| 22 | `anl10_cpxfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for capital expenditures for FY2 |
| 23 | `anl10_cpxsmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for capital exp |
| 24 | `anl10_cpxsmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for capital exp |
| 25 | `anl10_cpxsmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for capital exp |
| 26 | `anl10_cpxsmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for capital exp |
| 27 | `anl10_cshff_760` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Ff 760 for cash or cash equivalents |
| 28 | `anl10_dpsff` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends per share - field format |
| 29 | `anl10_dpsfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for dividends per share FY1 |
| 30 | `anl10_dpsfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for dividends per share for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 31 | `anl10_dpsfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for dividends per share for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 32 | `anl10_dpsfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for dividends per share for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 33 | `anl10_dpsfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for dividends per share for FY1 |
| 34 | `anl10_dpsfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for dividends per share for FY1 |
| 35 | `anl10_dpsfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for dividends per share for FY1 |
| 36 | `anl10_dpsfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for dividends per share FY2 |
| 37 | `anl10_dpsfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for dividends per share for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 38 | `anl10_dpsfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for dividends per share for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 39 | `anl10_dpsfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for dividends per share for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 40 | `anl10_dpsfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for dividends per share for FY2 |
| 41 | `anl10_dpsfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for dividends per share for FY2 |
| 42 | `anl10_dpsfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for dividends per share for FY2 |
| 43 | `anl10_dpspast_det_analyst_287` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for dividends per share estimates |
| 44 | `anl10_dpspast_det_anntime_291` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for dividends per share estimates |
| 45 | `anl10_dpspast_det_estage_292` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of dividends per share estimates in days |
| 46 | `anl10_dpspast_det_estflag_289` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for dividends per share |
| 47 | `anl10_dpspast_det_estvalue_293` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for dividends per share |
| 48 | `anl10_dpspast_det_excflag_290` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for dividends per share estimates |
| 49 | `anl10_dpspast_det_indicator_295` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for dividends per share estimates |
| 50 | `anl10_dpssmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for dividends p |
| 51 | `anl10_dpssmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for dividends p |
| 52 | `anl10_dpssmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for dividends p |
| 53 | `anl10_dpssmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for dividends p |
| 54 | `anl10_ebiff_7` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ff 7 for earnings before interest |
| 55 | `anl10_ebify1_consensus_17` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before interest FY1 |
| 56 | `anl10_ebify1_pred_surps_v0_12` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for earnings before interest for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 57 | `anl10_ebify1_pred_surps_v1_18` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for earnings before interest for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 58 | `anl10_ebify1_pred_surps_v2_36` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for earnings before interest for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 59 | `anl10_ebify1_smart_ests_v0_15` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for earnings before interest for FY1 |
| 60 | `anl10_ebify1_smart_ests_v1_1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for earnings before interest for FY1 |
| 61 | `anl10_ebify1_smart_ests_v2_25` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for earnings before interest for FY1 |
| 62 | `anl10_ebify2_consensus_39` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before interest FY2 |
| 63 | `anl10_ebify2_pred_surps_v0_5` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for earnings before interest for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 64 | `anl10_ebify2_pred_surps_v1_2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for earnings before interest for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 65 | `anl10_ebify2_pred_surps_v2_23` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for earnings before interest for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 66 | `anl10_ebify2_smart_ests_v0_6` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for earnings before interest for FY2 |
| 67 | `anl10_ebify2_smart_ests_v1_11` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for earnings before interest for FY2 |
| 68 | `anl10_ebify2_smart_ests_v2_14` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for earnings before interest for FY2 |
| 69 | `anl10_ebipast_det_analyst_722` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for earnings before interest estimates |
| 70 | `anl10_ebipast_det_anntime_723` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for earnings before interest estimates |
| 71 | `anl10_ebipast_det_estage_717` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of earnings before interest estimates in days |
| 72 | `anl10_ebipast_det_estflag_724` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for earnings before interest |
| 73 | `anl10_ebipast_det_estvalue_719` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for earnings before interest |
| 74 | `anl10_ebipast_det_excflag_715` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for earnings before interest estimates |
| 75 | `anl10_ebipast_det_indicator_716` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for earnings before interest estimates |
| 76 | `anl10_ebismun_1qf_20` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 77 | `anl10_ebismun_1yf_4` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 78 | `anl10_ebismun_2qf_30` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 79 | `anl10_ebismun_2yf_13` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 80 | `anl10_ebtff` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before tax - field format |
| 81 | `anl10_ebtfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before tax FY1 |
| 82 | `anl10_ebtfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for earnings before tax for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 83 | `anl10_ebtfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for earnings before tax for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 84 | `anl10_ebtfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for earnings before tax for FY1 |
| 85 | `anl10_ebtfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for earnings before tax for FY1 |
| 86 | `anl10_ebtfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for earnings before tax for FY1 |
| 87 | `anl10_ebtfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before tax FY2 |
| 88 | `anl10_ebtfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for earnings before tax for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 89 | `anl10_ebtfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for earnings before tax for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 90 | `anl10_ebtfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for earnings before tax for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 91 | `anl10_ebtfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for earnings before tax for FY2 |
| 92 | `anl10_ebtfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for earnings before tax for FY2 |
| 93 | `anl10_ebtfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for earnings before tax for FY2 |
| 94 | `anl10_ebtsmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 95 | `anl10_ebtsmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 96 | `anl10_ebtsmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 97 | `anl10_ebtsmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for earnings be |
| 98 | `anl10_gpsff_444` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ff 444 for gross profit per share |
| 99 | `anl10_gpsfy1_consensus_449` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross profit per share FY1 |
| 100 | `anl10_gpsfy1_pred_surps_v0_417` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for gross profit per share for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 101 | `anl10_gpsfy1_pred_surps_v1_423` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for gross profit per share for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 102 | `anl10_gpsfy1_pred_surps_v2_418` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for gross profit per share for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 103 | `anl10_gpsfy1_smart_ests_v0_437` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for gross profit per share for FY1 |
| 104 | `anl10_gpsfy1_smart_ests_v1_414` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for gross profit per share for FY1 |
| 105 | `anl10_gpsfy1_smart_ests_v2_430` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for gross profit per share for FY1 |
| 106 | `anl10_gpsfy2_consensus_421` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross profit per share FY2 |
| 107 | `anl10_gpsfy2_pred_surps_v0_424` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for gross profit per share for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 108 | `anl10_gpsfy2_pred_surps_v1_426` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for gross profit per share for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 109 | `anl10_gpsfy2_pred_surps_v2_448` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for gross profit per share for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 110 | `anl10_gpsfy2_smart_ests_v0_447` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for gross profit per share for FY2 |
| 111 | `anl10_gpsfy2_smart_ests_v1_441` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for gross profit per share for FY2 |
| 112 | `anl10_gpsfy2_smart_ests_v2_415` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for gross profit per share for FY2 |
| 113 | `anl10_gpspast_det_analyst_305` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for gross profit per share estimates |
| 114 | `anl10_gpspast_det_anntime_298` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for gross profit per share estimates |
| 115 | `anl10_gpspast_det_estage_300` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of gross profit per share estimates in days |
| 116 | `anl10_gpspast_det_estflag_299` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for gross profit per share |
| 117 | `anl10_gpspast_det_estvalue_303` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for gross profit per share |
| 118 | `anl10_gpspast_det_excflag_302` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for gross profit per share estimates |
| 119 | `anl10_gpspast_det_indicator_297` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for gross profit per share estimates |
| 120 | `anl10_gpssmun_1qf_429` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross profi |
| 121 | `anl10_gpssmun_1yf_438` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross profi |
| 122 | `anl10_gpssmun_2qf_413` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross profi |
| 123 | `anl10_gpssmun_2yf_420` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross profi |
| 124 | `anl10_grmff_606` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ff 606 for gross margin |
| 125 | `anl10_navff` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value - field format |
| 126 | `anl10_navfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net asset value FY1 |
| 127 | `anl10_navfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for net asset value for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 128 | `anl10_navfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for net asset value for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 129 | `anl10_navfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for net asset value for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 130 | `anl10_navfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for net asset value for FY1 |
| 131 | `anl10_navfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for net asset value for FY1 |
| 132 | `anl10_navfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for net asset value for FY1 |
| 133 | `anl10_navfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net asset value FY2 |
| 134 | `anl10_navfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for net asset value for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 135 | `anl10_navfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for net asset value for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 136 | `anl10_navfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for net asset value for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 137 | `anl10_navfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for net asset value for FY2 |
| 138 | `anl10_navfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for net asset value for FY2 |
| 139 | `anl10_navfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for net asset value for FY2 |
| 140 | `anl10_navpast_det_analyst_244` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for net asset value estimates |
| 141 | `anl10_navpast_det_anntime_245` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for net asset value estimates |
| 142 | `anl10_navpast_det_estage_236` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of net asset value estimates in days |
| 143 | `anl10_navpast_det_estflag_237` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for net asset value |
| 144 | `anl10_navpast_det_estvalue_240` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for net asset value |
| 145 | `anl10_navpast_det_excflag_242` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for net asset value estimates |
| 146 | `anl10_navpast_det_indicator_241` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for net asset value estimates |
| 147 | `anl10_navsmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net asset v |
| 148 | `anl10_navsmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net asset v |
| 149 | `anl10_navsmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net asset v |
| 150 | `anl10_navsmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net asset v |
| 151 | `anl10_ndtff` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Date - field format |
| 152 | `anl10_ndtfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for date FY1 |
| 153 | `anl10_ndtfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for date for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 154 | `anl10_ndtfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for date for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 155 | `anl10_ndtfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for date for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 156 | `anl10_ndtfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for date for FY1 |
| 157 | `anl10_ndtfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for date for FY1 |
| 158 | `anl10_ndtfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for date for FY1 |
| 159 | `anl10_ndtfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for date FY2 |
| 160 | `anl10_ndtfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for date for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 161 | `anl10_ndtfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for date for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 162 | `anl10_ndtfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for date for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 163 | `anl10_ndtfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for date for FY2 |
| 164 | `anl10_ndtfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for date for FY2 |
| 165 | `anl10_ndtfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for date for FY2 |
| 166 | `anl10_ndtsmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for date |
| 167 | `anl10_ndtsmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for date |
| 168 | `anl10_ndtsmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for date |
| 169 | `anl10_ndtsmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for date |
| 170 | `anl10_nerff` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net earnings rate - field format |
| 171 | `anl10_nerfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net earnings rate FY1 |
| 172 | `anl10_nerfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for net earnings rate for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 173 | `anl10_nerfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for net earnings rate for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 174 | `anl10_nerfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for net earnings rate for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 175 | `anl10_nerfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for net earnings rate for FY1 |
| 176 | `anl10_nerfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for net earnings rate for FY1 |
| 177 | `anl10_nerfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for net earnings rate for FY1 |
| 178 | `anl10_nerfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net earnings rate FY2 |
| 179 | `anl10_nerfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for net earnings rate for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 180 | `anl10_nerfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for net earnings rate for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 181 | `anl10_nerfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for net earnings rate for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 182 | `anl10_nerfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for net earnings rate for FY2 |
| 183 | `anl10_nerfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for net earnings rate for FY2 |
| 184 | `anl10_nerfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for net earnings rate for FY2 |
| 185 | `anl10_nerpast_det_analyst` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for net earnings rate estimates |
| 186 | `anl10_nerpast_det_anntime` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for net earnings rate estimates |
| 187 | `anl10_nerpast_det_estage` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of net earnings rate estimates in days |
| 188 | `anl10_nerpast_det_estflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for net earnings rate |
| 189 | `anl10_nerpast_det_estvalue` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for net earnings rate |
| 190 | `anl10_nerpast_det_excflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for net earnings rate estimates |
| 191 | `anl10_nerpast_det_indicator` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for net earnings rate estimates |
| 192 | `anl10_nersmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net earning |
| 193 | `anl10_nersmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net earning |
| 194 | `anl10_nersmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net earning |
| 195 | `anl10_nersmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net earning |
| 196 | `anl10_netff_622` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ff 622 for net income |
| 197 | `anl10_netfy1_consensus_653` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net income FY1 |
| 198 | `anl10_netfy1_pred_surps_v0_623` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for net income for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 199 | `anl10_netfy1_pred_surps_v2_648` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for net income for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 200 | `anl10_netfy1_smart_ests_v0_647` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for net income for FY1 |
| 201 | `anl10_netfy1_smart_ests_v1_638` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for net income for FY1 |
| 202 | `anl10_netfy1_smart_ests_v2_621` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for net income for FY1 |
| 203 | `anl10_netfy2_consensus_633` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net income FY2 |
| 204 | `anl10_netfy2_pred_surps_v0_631` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for net income for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 205 | `anl10_netfy2_pred_surps_v1_635` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for net income for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 206 | `anl10_netfy2_pred_surps_v2_626` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for net income for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 207 | `anl10_netfy2_smart_ests_v0_634` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for net income for FY2 |
| 208 | `anl10_netfy2_smart_ests_v1_636` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for net income for FY2 |
| 209 | `anl10_netfy2_smart_ests_v2_641` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for net income for FY2 |
| 210 | `anl10_netpast_det_analyst` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for net income estimates |
| 211 | `anl10_netpast_det_anntime` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for net income estimates |
| 212 | `anl10_netpast_det_estage` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of net income estimates in days |
| 213 | `anl10_netpast_det_estflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for net income |
| 214 | `anl10_netpast_det_estvalue` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for net income |
| 215 | `anl10_netpast_det_excflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for net income estimates |
| 216 | `anl10_netpast_det_indicator` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for net income estimates |
| 217 | `anl10_netsmun_1qf_637` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net income |
| 218 | `anl10_netsmun_1yf_632` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net income |
| 219 | `anl10_netsmun_2qf_646` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net income |
| 220 | `anl10_netsmun_2yf_652` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for net income |
| 221 | `anl10_oprff_188` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ff 188 for operating profit |
| 222 | `anl10_preff_466` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Ff 466 for pre-tax or preliminary |
| 223 | `anl10_prefy1_consensus_451` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for pre-tax or preliminary FY1 |
| 224 | `anl10_prefy1_pred_surps_v0_476` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for pre-tax or preliminary for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 225 | `anl10_prefy1_pred_surps_v2_475` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for pre-tax or preliminary for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 226 | `anl10_prefy1_smart_ests_v0_462` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for pre-tax or preliminary for FY1 |
| 227 | `anl10_prefy1_smart_ests_v1_471` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for pre-tax or preliminary for FY1 |
| 228 | `anl10_prefy1_smart_ests_v2_463` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for pre-tax or preliminary for FY1 |
| 229 | `anl10_prefy2_consensus_481` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for pre-tax or preliminary FY2 |
| 230 | `anl10_prefy2_pred_surps_v0_459` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for pre-tax or preliminary for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 231 | `anl10_prefy2_pred_surps_v1_485` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for pre-tax or preliminary for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 232 | `anl10_prefy2_pred_surps_v2_489` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for pre-tax or preliminary for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 233 | `anl10_prefy2_smart_ests_v0_482` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for pre-tax or preliminary for FY2 |
| 234 | `anl10_prefy2_smart_ests_v1_456` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for pre-tax or preliminary for FY2 |
| 235 | `anl10_prefy2_smart_ests_v2_484` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for pre-tax or preliminary for FY2 |
| 236 | `anl10_prepast_det_analyst` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for pre-tax or preliminary estimates |
| 237 | `anl10_prepast_det_anntime` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for pre-tax or preliminary estimates |
| 238 | `anl10_prepast_det_estage` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of pre-tax or preliminary estimates in days |
| 239 | `anl10_prepast_det_estflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for pre-tax or preliminary |
| 240 | `anl10_prepast_det_estvalue` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for pre-tax or preliminary |
| 241 | `anl10_prepast_det_excflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for pre-tax or preliminary estimates |
| 242 | `anl10_prepast_det_indicator` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for pre-tax or preliminary estimates |
| 243 | `anl10_presmun_1qf_452` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for pre-tax or |
| 244 | `anl10_presmun_1yf_487` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for pre-tax or |
| 245 | `anl10_presmun_2qf_478` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for pre-tax or |
| 246 | `anl10_presmun_2yf_470` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for pre-tax or |
| 247 | `anl10_prrff` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price return ratio - field format |
| 248 | `anl10_prrfy1_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for price return ratio FY1 |
| 249 | `anl10_prrfy1_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for price return ratio for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 250 | `anl10_prrfy1_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for price return ratio for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 251 | `anl10_prrfy1_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for price return ratio for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 252 | `anl10_prrfy1_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for price return ratio for FY1 |
| 253 | `anl10_prrfy1_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for price return ratio for FY1 |
| 254 | `anl10_prrfy1_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for price return ratio for FY1 |
| 255 | `anl10_prrfy2_consensus` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for price return ratio FY2 |
| 256 | `anl10_prrfy2_pred_surps_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for price return ratio for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 257 | `anl10_prrfy2_pred_surps_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for price return ratio for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 258 | `anl10_prrfy2_pred_surps_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for price return ratio for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 259 | `anl10_prrfy2_smart_ests_v0` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for price return ratio for FY2 |
| 260 | `anl10_prrfy2_smart_ests_v1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for price return ratio for FY2 |
| 261 | `anl10_prrfy2_smart_ests_v2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for price return ratio for FY2 |
| 262 | `anl10_prrpast_det_analyst_225` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for price return ratio estimates |
| 263 | `anl10_prrpast_det_anntime_223` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for price return ratio estimates |
| 264 | `anl10_prrpast_det_estage_222` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of price return ratio estimates in days |
| 265 | `anl10_prrpast_det_estflag_224` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for price return ratio |
| 266 | `anl10_prrpast_det_estvalue_220` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for price return ratio |
| 267 | `anl10_prrpast_det_excflag_218` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for price return ratio estimates |
| 268 | `anl10_prrpast_det_indicator_219` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for price return ratio estimates |
| 269 | `anl10_prrsmun_1qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for price retur |
| 270 | `anl10_prrsmun_1yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for price retur |
| 271 | `anl10_prrsmun_2qf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for price retur |
| 272 | `anl10_prrsmun_2yf` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for price retur |
| 273 | `anl10_salff_538` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Ff 538 for sales |
| 274 | `anl10_salfy1_consensus_559` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for sales FY1 |
| 275 | `anl10_salfy1_pred_surps_v0_532` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for sales for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 276 | `anl10_salfy1_pred_surps_v2_546` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for sales for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 277 | `anl10_salfy1_smart_ests_v0_558` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for sales for FY1 |
| 278 | `anl10_salfy1_smart_ests_v1_561` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for sales for FY1 |
| 279 | `anl10_salfy1_smart_ests_v2_543` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for sales for FY1 |
| 280 | `anl10_salfy2_consensus_562` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for sales FY2 |
| 281 | `anl10_salfy2_pred_surps_v0_552` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for sales for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 282 | `anl10_salfy2_pred_surps_v1_553` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for sales for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 283 | `anl10_salfy2_pred_surps_v2_550` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for sales for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 284 | `anl10_salfy2_smart_ests_v0_535` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for sales for FY2 |
| 285 | `anl10_salfy2_smart_ests_v1_542` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for sales for FY2 |
| 286 | `anl10_salfy2_smart_ests_v2_566` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for sales for FY2 |
| 287 | `anl10_salpast_det_analyst` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for sales estimates |
| 288 | `anl10_salpast_det_anntime` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for sales estimates |
| 289 | `anl10_salpast_det_estage` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of sales estimates in days |
| 290 | `anl10_salpast_det_estflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for sales |
| 291 | `anl10_salpast_det_estvalue` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for sales |
| 292 | `anl10_salpast_det_excflag` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for sales estimates |
| 293 | `anl10_salpast_det_indicator` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for sales estimates |
| 294 | `anl10_salsmun_1qf_537` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for sales |
| 295 | `anl10_salsmun_1yf_560` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for sales |
| 296 | `anl10_salsmun_2qf_541` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for sales |
| 297 | `anl10_salsmun_2yf_570` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for sales |
| 298 | `anl10_smartest_tbv_ff` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Ff 1469 for tangible book value |
| 299 | `anl10_tbvff` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Tangible book value - field format |
| 300 | `tbv_estimate_actual_update_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator if tangible book value per share smart estimate was updated based on actual results. |
| 301 | `tbv_estimate_performance_update_flag` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator if tangible book value per share smart estimate was updated based on analyst performance. |
| 302 | `anl10_netinnovate_decrease_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for net income FY1 |
| 303 | `anl10_netinnovation_score_fy1` | MATRIX | 0.998 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for net income FY1 (innovate_increase - innovate_decrease) |
| 304 | `anl10_netnormal_decrease_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for net income FY1 |
| 305 | `anl10_netnormal_increase_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for net income FY1 |
| 306 | `anl10_netrevise_ratio_to_close_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for net income FY1 |
| 307 | `anl10_netrevise_ratio_to_consensus_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net income FY1 |
| 308 | `anl10_netrevise_value_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for net income FY1 (difference between old and current updated value) |
| 309 | `anl10_salinnovate_decrease_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for sales FY1 |
| 310 | `anl10_salinnovate_increase_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for sales FY1 |
| 311 | `anl10_salinnovation_score_fy1` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for sales FY1 (innovate_increase - innovate_decrease) |
| 312 | `anl10_salnormal_decrease_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for sales FY1 |
| 313 | `anl10_salnormal_increase_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for sales FY1 |
| 314 | `anl10_netinnovate_decrease_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for net income FY2 |
| 315 | `anl10_netinnovate_increase_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for net income FY2 |
| 316 | `anl10_netinnovation_score_fy2` | MATRIX | 0.998 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for net income FY2 (innovate_increase - innovate_decrease) |
| 317 | `anl10_netnormal_decrease_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for net income FY2 |
| 318 | `anl10_netnormal_increase_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for net income FY2 |
| 319 | `anl10_netrevise_ratio_to_close_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for net income FY2 |
| 320 | `anl10_netrevise_ratio_to_consensus_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net income FY2 |
| 321 | `anl10_netrevise_value_fy2` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for net income FY2 (difference between old and current updated value) |
| 322 | `anl10_salrevise_ratio_to_close_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for sales FY1 |
| 323 | `anl10_salrevise_ratio_to_consensus_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for sales FY1 |
| 324 | `anl10_salrevise_value_fy1` | MATRIX | 0.998 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for sales FY1 (difference between old and current updated value) |
| 325 | `anl10_salinnovate_decrease_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for sales FY2 |
| 326 | `anl10_salinnovate_increase_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for sales FY2 |
| 327 | `anl10_salinnovation_score_fy2` | MATRIX | 0.996 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for sales FY2 (innovate_increase - innovate_decrease) |
| 328 | `anl10_salnormal_decrease_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for sales FY2 |
| 329 | `anl10_salnormal_increase_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for sales FY2 |
| 330 | `anl10_salrevise_ratio_to_close_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for sales FY2 |
| 331 | `anl10_salrevise_ratio_to_consensus_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for sales FY2 |
| 332 | `anl10_salrevise_value_fy2` | MATRIX | 0.996 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for sales FY2 (difference between old and current updated value) |
| 333 | `anl10_ebiinnovate_decrease_fy1` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for earnings before interest FY1 |
| 334 | `anl10_ebiinnovate_increase_fy1` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for earnings before interest FY1 |
| 335 | `anl10_ebiinnovation_score_fy1` | MATRIX | 0.995 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for earnings before interest FY1 (innovate_increase - innovate_decrease) |
| 336 | `anl10_ebinormal_decrease_fy1` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for earnings before interest FY1 |
| 337 | `anl10_ebinormal_increase_fy1` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for earnings before interest FY1 |
| 338 | `anl10_preinnovate_decrease_fy2` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for pre-tax or preliminary FY2 |
| 339 | `anl10_preinnovate_increase_fy2` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for pre-tax or preliminary FY2 |
| 340 | `anl10_preinnovation_score_fy2` | MATRIX | 0.995 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for pre-tax or preliminary FY2 (innovate_increase - innovate_decrease) |
| 341 | `anl10_prenormal_decrease_fy2` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for pre-tax or preliminary FY2 |
| 342 | `anl10_prenormal_increase_fy2` | MATRIX | 0.995 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for pre-tax or preliminary FY2 |
| 343 | `anl10_ebiinnovate_decrease_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for earnings before interest FY2 |
| 344 | `anl10_ebiinnovate_increase_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for earnings before interest FY2 |
| 345 | `anl10_ebiinnovation_score_fy2` | MATRIX | 0.994 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for earnings before interest FY2 (innovate_increase - innovate_decrease) |
| 346 | `anl10_ebinormal_decrease_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for earnings before interest FY2 |
| 347 | `anl10_ebinormal_increase_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for earnings before interest FY2 |
| 348 | `anl10_ebirevise_ratio_to_close_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for earnings before interest FY1 |
| 349 | `anl10_ebirevise_ratio_to_consensus_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before interest FY1 |
| 350 | `anl10_ebirevise_value_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for earnings before interest FY1 (difference between old and current updated value) |
| 351 | `anl10_preinnovate_decrease_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for pre-tax or preliminary FY1 |
| 352 | `anl10_preinnovate_increase_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for pre-tax or preliminary FY1 |
| 353 | `anl10_preinnovation_score_fy1` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for pre-tax or preliminary FY1 (innovate_increase - innovate_decrease) |
| 354 | `anl10_prenormal_decrease_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for pre-tax or preliminary FY1 |
| 355 | `anl10_prenormal_increase_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for pre-tax or preliminary FY1 |
| 356 | `anl10_prerevise_ratio_to_close_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for pre-tax or preliminary FY1 |
| 357 | `anl10_prerevise_ratio_to_close_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for pre-tax or preliminary FY2 |
| 358 | `anl10_prerevise_ratio_to_consensus_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for pre-tax or preliminary FY1 |
| 359 | `anl10_prerevise_ratio_to_consensus_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for pre-tax or preliminary FY2 |
| 360 | `anl10_prerevise_value_fy1` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for pre-tax or preliminary FY1 (difference between old and current updated value) |
| 361 | `anl10_prerevise_value_fy2` | MATRIX | 0.994 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for pre-tax or preliminary FY2 (difference between old and current updated value) |
| 362 | `anl10_ebirevise_ratio_to_close_fy2` | MATRIX | 0.993 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for earnings before interest FY2 |
| 363 | `anl10_ebirevise_ratio_to_consensus_fy2` | MATRIX | 0.993 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before interest FY2 |
| 364 | `anl10_ebirevise_value_fy2` | MATRIX | 0.993 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for earnings before interest FY2 (difference between old and current updated value) |
| 365 | `anl10_ebtpast_det_analyst` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for earnings before tax estimates |
| 366 | `anl10_ebtpast_det_anntime` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for earnings before tax estimates |
| 367 | `anl10_ebtpast_det_estage` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of earnings before tax estimates in days |
| 368 | `anl10_ebtpast_det_estflag` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for earnings before tax |
| 369 | `anl10_ebtpast_det_estvalue` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for earnings before tax |
| 370 | `anl10_ebtpast_det_excflag` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for earnings before tax estimates |
| 371 | `anl10_ebtpast_det_indicator` | VECTOR | 0.986 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for earnings before tax estimates |
| 372 | `anl10_dpsinnovate_decrease_fy2` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for dividends per share FY2 |
| 373 | `anl10_dpsinnovate_increase_fy2` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for dividends per share FY2 |
| 374 | `anl10_dpsinnovation_score_fy2` | MATRIX | 0.983 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for dividends per share FY2 (innovate_increase - innovate_decrease) |
| 375 | `anl10_dpsnormal_decrease_fy2` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for dividends per share FY2 |
| 376 | `anl10_gpsinnovate_decrease_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for gross profit per share FY1 |
| 377 | `anl10_gpsinnovate_increase_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for gross profit per share FY1 |
| 378 | `anl10_gpsinnovation_score_fy1` | MATRIX | 0.983 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for gross profit per share FY1 (innovate_increase - innovate_decrease) |
| 379 | `anl10_gpsnormal_decrease_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for gross profit per share FY1 |
| 380 | `anl10_gpsnormal_increase_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for gross profit per share FY1 |
| 381 | `anl10_gpsrevise_ratio_to_close_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for gross profit per share FY1 |
| 382 | `anl10_gpsrevise_ratio_to_consensus_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross profit per share FY1 |
| 383 | `anl10_gpsrevise_value_fy1` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for gross profit per share FY1 (difference between old and current updated value) |
| 384 | `anl10_oprsmun_1qf_193` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for operating p |
| 385 | `anl10_oprsmun_1yf_215` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for operating p |
| 386 | `anl10_oprsmun_2qf_176` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for operating p |
| 387 | `anl10_oprsmun_2yf_203` | MATRIX | 0.983 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for operating p |
| 388 | `anl10_gpsinnovate_decrease_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for gross profit per share FY2 |
| 389 | `anl10_gpsinnovate_increase_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for gross profit per share FY2 |
| 390 | `anl10_gpsinnovation_score_fy2` | MATRIX | 0.982 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for gross profit per share FY2 (innovate_increase - innovate_decrease) |
| 391 | `anl10_gpsnormal_decrease_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for gross profit per share FY2 |
| 392 | `anl10_gpsnormal_increase_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for gross profit per share FY2 |
| 393 | `anl10_gpsrevise_ratio_to_close_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for gross profit per share FY2 |
| 394 | `anl10_gpsrevise_ratio_to_consensus_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross profit per share FY2 |
| 395 | `anl10_gpsrevise_value_fy2` | MATRIX | 0.982 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for gross profit per share FY2 (difference between old and current updated value) |
| 396 | `anl10_dpsinnovate_decrease_fy1` | MATRIX | 0.981 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for dividends per share FY1 |
| 397 | `anl10_dpsinnovate_increase_fy1` | MATRIX | 0.981 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for dividends per share FY1 |
| 398 | `anl10_dpsinnovation_score_fy1` | MATRIX | 0.981 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for dividends per share FY1 (innovate_increase - innovate_decrease) |
| 399 | `anl10_nerinnovate_decrease_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for net earnings rate FY1 |
| 400 | `anl10_nerinnovate_increase_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for net earnings rate FY1 |
| 401 | `anl10_nerinnovation_score_fy1` | MATRIX | 0.968 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for net earnings rate FY1 (innovate_increase - innovate_decrease) |
| 402 | `anl10_nernormal_decrease_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for net earnings rate FY1 |
| 403 | `anl10_nernormal_increase_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for net earnings rate FY1 |
| 404 | `anl10_nerrevise_ratio_to_close_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for net earnings rate FY1 |
| 405 | `anl10_nerrevise_ratio_to_consensus_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net earnings rate FY1 |
| 406 | `anl10_nerrevise_value_fy1` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for net earnings rate FY1 (difference between old and current updated value) |
| 407 | `anl10_nerinnovate_decrease_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for net earnings rate FY2 |
| 408 | `anl10_nerinnovate_increase_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for net earnings rate FY2 |
| 409 | `anl10_nerinnovation_score_fy2` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for net earnings rate FY2 (innovate_increase - innovate_decrease) |
| 410 | `anl10_nernormal_decrease_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for net earnings rate FY2 |
| 411 | `anl10_nernormal_increase_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for net earnings rate FY2 |
| 412 | `anl10_nerrevise_ratio_to_close_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for net earnings rate FY2 |
| 413 | `anl10_nerrevise_ratio_to_consensus_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net earnings rate FY2 |
| 414 | `anl10_nerrevise_value_fy2` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for net earnings rate FY2 (difference between old and current updated value) |
| 415 | `anl10_prrinnovate_decrease_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for price return ratio FY1 |
| 416 | `anl10_prrinnovate_increase_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for price return ratio FY1 |
| 417 | `anl10_prrinnovation_score_fy1` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Innovation score for price return ratio FY1 (innovate_increase - innovate_decrease) |
| 418 | `anl10_prrnormal_decrease_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for price return ratio FY1 |
| 419 | `anl10_prrnormal_increase_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for price return ratio FY1 |
| 420 | `anl10_prrrevise_ratio_to_close_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for price return ratio FY1 |
| 421 | `anl10_prrrevise_ratio_to_consensus_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for price return ratio FY1 |
| 422 | `anl10_prrrevise_value_fy1` | MATRIX | 0.953 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for price return ratio FY1 (difference between old and current updated value) |
| 423 | `anl10_grmsmun_1qf_610` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross margi |
| 424 | `anl10_grmsmun_1yf_595` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross margi |
| 425 | `anl10_grmsmun_2qf_585` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross margi |
| 426 | `anl10_grmsmun_2yf_592` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for gross margi |
| 427 | `anl10_prrinnovate_decrease_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for price return ratio FY2 |
| 428 | `anl10_prrinnovate_increase_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for price return ratio FY2 |
| 429 | `anl10_prrinnovation_score_fy2` | MATRIX | 0.951 | 价量与波动 | 0 | — | — | — | UNTESTED | Innovation score for price return ratio FY2 (innovate_increase - innovate_decrease) |
| 430 | `anl10_prrnormal_decrease_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for price return ratio FY2 |
| 431 | `anl10_prrnormal_increase_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for price return ratio FY2 |
| 432 | `anl10_prrrevise_ratio_to_close_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for price return ratio FY2 |
| 433 | `anl10_prrrevise_ratio_to_consensus_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for price return ratio FY2 |
| 434 | `anl10_prrrevise_value_fy2` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for price return ratio FY2 (difference between old and current updated value) |
| 435 | `anl10_cpxpast_det_analyst_710` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for capital expenditures estimates |
| 436 | `anl10_cpxpast_det_anntime_714` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for capital expenditures estimates |
| 437 | `anl10_cpxpast_det_estage_705` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of capital expenditures estimates in days |
| 438 | `anl10_cpxpast_det_estflag_711` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for capital expenditures |
| 439 | `anl10_cpxpast_det_estvalue_706` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for capital expenditures |
| 440 | `anl10_cpxpast_det_excflag_709` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for capital expenditures estimates |
| 441 | `anl10_cpxpast_det_indicator_708` | VECTOR | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for capital expenditures estimates |
| 442 | `anl10_navinnovate_decrease_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for net asset value FY1 |
| 443 | `anl10_navinnovate_increase_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for net asset value FY1 |
| 444 | `anl10_navinnovation_score_fy1` | MATRIX | 0.949 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for net asset value FY1 (innovate_increase - innovate_decrease) |
| 445 | `anl10_navnormal_decrease_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for net asset value FY1 |
| 446 | `anl10_navnormal_increase_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for net asset value FY1 |
| 447 | `anl10_navrevise_ratio_to_close_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for net asset value FY1 |
| 448 | `anl10_navrevise_ratio_to_consensus_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net asset value FY1 |
| 449 | `anl10_navrevise_value_fy1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for net asset value FY1 (difference between old and current updated value) |
| 450 | `anl10_navinnovate_decrease_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for net asset value FY2 |
| 451 | `anl10_navinnovate_increase_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for net asset value FY2 |
| 452 | `anl10_navinnovation_score_fy2` | MATRIX | 0.948 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for net asset value FY2 (innovate_increase - innovate_decrease) |
| 453 | `anl10_navnormal_decrease_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for net asset value FY2 |
| 454 | `anl10_navnormal_increase_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for net asset value FY2 |
| 455 | `anl10_navrevise_ratio_to_close_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for net asset value FY2 |
| 456 | `anl10_navrevise_ratio_to_consensus_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for net asset value FY2 |
| 457 | `anl10_navrevise_value_fy2` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for net asset value FY2 (difference between old and current updated value) |
| 458 | `anl10_ndtpast_det_analyst_729` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for date estimates |
| 459 | `anl10_ndtpast_det_anntime_728` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for date estimates |
| 460 | `anl10_ndtpast_det_estage_734` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of date estimates in days |
| 461 | `anl10_ndtpast_det_estflag_725` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for date |
| 462 | `anl10_ndtpast_det_estvalue_731` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for date |
| 463 | `anl10_ndtpast_det_excflag_726` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for date estimates |
| 464 | `anl10_ndtpast_det_indicator_732` | VECTOR | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for date estimates |
| 465 | `anl10_grmfy1_consensus_609` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross margin FY1 |
| 466 | `anl10_grmfy1_pred_surps_v0_588` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for gross margin for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 467 | `anl10_grmfy1_pred_surps_v1_601` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for gross margin for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 468 | `anl10_grmfy1_pred_surps_v2_603` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for gross margin for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 469 | `anl10_grmfy1_smart_ests_v0_611` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for gross margin for FY1 |
| 470 | `anl10_grmfy1_smart_ests_v1_581` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for gross margin for FY1 |
| 471 | `anl10_grmfy1_smart_ests_v2_584` | MATRIX | 0.937 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for gross margin for FY1 |
| 472 | `anl10_grmfy2_consensus_587` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross margin FY2 |
| 473 | `anl10_grmfy2_pred_surps_v0_590` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for gross margin for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 474 | `anl10_grmfy2_pred_surps_v1_602` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for gross margin for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 475 | `anl10_grmfy2_pred_surps_v2_577` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for gross margin for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 476 | `anl10_grmfy2_smart_ests_v0_578` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for gross margin for FY2 |
| 477 | `anl10_grmfy2_smart_ests_v1_604` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for gross margin for FY2 |
| 478 | `anl10_grmfy2_smart_ests_v2_605` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for gross margin for FY2 |
| 479 | `anl10_ebtinnovate_decrease_fy1` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for earnings before tax FY1 |
| 480 | `anl10_ebtinnovate_decrease_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for earnings before tax FY2 |
| 481 | `anl10_ebtinnovate_increase_fy1` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for earnings before tax FY1 |
| 482 | `anl10_ebtinnovate_increase_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for earnings before tax FY2 |
| 483 | `anl10_ebtinnovation_score_fy2` | MATRIX | 0.920 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for earnings before tax FY2 (innovate_increase - innovate_decrease) |
| 484 | `anl10_ebtnormal_decrease_fy1` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for earnings before tax FY1 |
| 485 | `anl10_ebtnormal_decrease_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for earnings before tax FY2 |
| 486 | `anl10_ebtnormal_increase_fy1` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for earnings before tax FY1 |
| 487 | `anl10_ebtnormal_increase_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for earnings before tax FY2 |
| 488 | `anl10_ebtrevise_ratio_to_close_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for earnings before tax FY2 |
| 489 | `anl10_ebtrevise_ratio_to_consensus_fy1` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before tax FY1 |
| 490 | `anl10_ebtrevise_ratio_to_consensus_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for earnings before tax FY2 |
| 491 | `anl10_ebtrevise_value_fy1` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for earnings before tax FY1 (difference between old and current updated value) |
| 492 | `anl10_ebtrevise_value_fy2` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for earnings before tax FY2 (difference between old and current updated value) |
| 493 | `anl10_oprfy1_consensus_212` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for operating profit FY1 |
| 494 | `anl10_oprfy1_pred_surps_v0_177` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for operating profit for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 495 | `anl10_oprfy1_pred_surps_v1_184` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for operating profit for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 496 | `anl10_oprfy1_pred_surps_v2_191` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for operating profit for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 497 | `anl10_oprfy1_smart_ests_v0_192` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for operating profit for FY1 |
| 498 | `anl10_oprfy1_smart_ests_v1_189` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for operating profit for FY1 |
| 499 | `anl10_oprfy1_smart_ests_v2_213` | MATRIX | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for operating profit for FY1 |
| 500 | `anl10_dpsrevise_ratio_to_close_fy2` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for dividends per share FY2 |
| 501 | `anl10_dpsrevise_ratio_to_consensus_fy2` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for dividends per share FY2 |
| 502 | `anl10_dpsrevise_value_fy2` | MATRIX | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for dividends per share FY2 (difference between old and current updated value) |
| 503 | `anl10_tbvsmun_1qf` | MATRIX | 0.904 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for tangible bo |
| 504 | `anl10_tbvsmun_1yf` | MATRIX | 0.904 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for tangible bo |
| 505 | `anl10_tbvsmun_2qf` | MATRIX | 0.904 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for tangible bo |
| 506 | `anl10_tbvsmun_2yf` | MATRIX | 0.904 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for tangible bo |
| 507 | `anl10_cshsmun_1qf_765` | MATRIX | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for cash or cas |
| 508 | `anl10_cshsmun_1yf_795` | MATRIX | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for cash or cas |
| 509 | `anl10_cshsmun_2qf_783` | MATRIX | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for cash or cas |
| 510 | `anl10_cshsmun_2yf_788` | MATRIX | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Sample/analyst number - indicating how many analysts contributed to that particular estimate or forecast for cash or cas |
| 511 | `anl10_tbvfy1_consensus` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for tangible book value FY1 |
| 512 | `anl10_tbvfy1_pred_surps_v0` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for tangible book value for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 513 | `anl10_tbvfy1_pred_surps_v1` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for tangible book value for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 514 | `anl10_tbvfy1_pred_surps_v2` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for tangible book value for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 515 | `anl10_tbvfy1_smart_ests_v0` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for tangible book value for FY1 |
| 516 | `anl10_tbvfy1_smart_ests_v1` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for tangible book value for FY1 |
| 517 | `anl10_tbvfy1_smart_ests_v2` | MATRIX | 0.897 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for tangible book value for FY1 |
| 518 | `anl10_dpsrevise_ratio_to_close_fy1` | MATRIX | 0.895 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for dividends per share FY1 |
| 519 | `anl10_dpsrevise_ratio_to_consensus_fy1` | MATRIX | 0.895 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for dividends per share FY1 |
| 520 | `anl10_dpsrevise_value_fy1` | MATRIX | 0.895 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for dividends per share FY1 (difference between old and current updated value) |
| 521 | `anl10_cshfy1_consensus_787` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for cash or cash equivalents FY1 |
| 522 | `anl10_cshfy1_pred_surps_v0_779` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for cash or cash equivalents for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 523 | `anl10_cshfy1_pred_surps_v1_775` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for cash or cash equivalents for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 524 | `anl10_cshfy1_pred_surps_v2_756` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for cash or cash equivalents for FY1 (calculated as (smart_ests - consensus)/consensus) |
| 525 | `anl10_cshfy1_smart_ests_v0_773` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for cash or cash equivalents for FY1 |
| 526 | `anl10_cshfy1_smart_ests_v1_764` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for cash or cash equivalents for FY1 |
| 527 | `anl10_cshfy1_smart_ests_v2_759` | MATRIX | 0.893 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for cash or cash equivalents for FY1 |
| 528 | `anl10_cshfy2_consensus_758` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for cash or cash equivalents FY2 |
| 529 | `anl10_cshfy2_pred_surps_v0_766` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for cash or cash equivalents for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 530 | `anl10_cshfy2_pred_surps_v1_763` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for cash or cash equivalents for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 531 | `anl10_cshfy2_pred_surps_v2_785` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for cash or cash equivalents for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 532 | `anl10_cshfy2_smart_ests_v0_777` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for cash or cash equivalents for FY2 |
| 533 | `anl10_cshfy2_smart_ests_v1_786` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for cash or cash equivalents for FY2 |
| 534 | `anl10_cshfy2_smart_ests_v2_792` | MATRIX | 0.892 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for cash or cash equivalents for FY2 |
| 535 | `anl10_ndtinnovate_decrease_fy1` | MATRIX | 0.876 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for date FY1 |
| 536 | `anl10_ndtinnovate_increase_fy1` | MATRIX | 0.876 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for date FY1 |
| 537 | `anl10_ndtinnovation_score_fy1` | MATRIX | 0.876 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for date FY1 (innovate_increase - innovate_decrease) |
| 538 | `anl10_ndtnormal_decrease_fy1` | MATRIX | 0.876 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for date FY1 |
| 539 | `anl10_ndtnormal_increase_fy1` | MATRIX | 0.876 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for date FY1 |
| 540 | `anl10_ndtrevise_ratio_to_close_fy1` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for date FY1 |
| 541 | `anl10_ndtrevise_ratio_to_consensus_fy1` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for date FY1 |
| 542 | `anl10_ndtrevise_value_fy1` | MATRIX | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for date FY1 (difference between old and current updated value) |
| 543 | `anl10_ndtinnovate_decrease_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for date FY2 |
| 544 | `anl10_ndtinnovate_increase_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for date FY2 |
| 545 | `anl10_ndtinnovation_score_fy2` | MATRIX | 0.874 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for date FY2 (innovate_increase - innovate_decrease) |
| 546 | `anl10_ndtnormal_decrease_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for date FY2 |
| 547 | `anl10_ndtnormal_increase_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for date FY2 |
| 548 | `anl10_ndtrevise_ratio_to_close_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for date FY2 |
| 549 | `anl10_ndtrevise_ratio_to_consensus_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for date FY2 |
| 550 | `anl10_ndtrevise_value_fy2` | MATRIX | 0.874 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for date FY2 (difference between old and current updated value) |
| 551 | `anl10_tbvfy2_consensus` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for tangible book value FY2 |
| 552 | `anl10_tbvfy2_pred_surps_v0` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for tangible book value for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 553 | `anl10_tbvfy2_pred_surps_v1` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for tangible book value for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 554 | `anl10_tbvfy2_pred_surps_v2` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for tangible book value for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 555 | `anl10_tbvfy2_smart_ests_v0` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for tangible book value for FY2 |
| 556 | `anl10_tbvfy2_smart_ests_v1` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for tangible book value for FY2 |
| 557 | `anl10_tbvfy2_smart_ests_v2` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for tangible book value for FY2 |
| 558 | `anl10_cpxinnovate_decrease_fy1` | MATRIX | 0.846 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for capital expenditures FY1 |
| 559 | `anl10_cpxinnovate_increase_fy1` | MATRIX | 0.846 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for capital expenditures FY1 |
| 560 | `anl10_cpxinnovation_score_fy1` | MATRIX | 0.846 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for capital expenditures FY1 (innovate_increase - innovate_decrease) |
| 561 | `anl10_cpxnormal_decrease_fy1` | MATRIX | 0.846 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for capital expenditures FY1 |
| 562 | `anl10_cpxnormal_increase_fy1` | MATRIX | 0.846 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for capital expenditures FY1 |
| 563 | `anl10_cpxrevise_ratio_to_close_fy1` | MATRIX | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for capital expenditures FY1 |
| 564 | `anl10_cpxrevise_ratio_to_consensus_fy1` | MATRIX | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for capital expenditures FY1 |
| 565 | `anl10_cpxrevise_value_fy1` | MATRIX | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for capital expenditures FY1 (difference between old and current updated value) |
| 566 | `anl10_cpxinnovate_decrease_fy2` | MATRIX | 0.838 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for capital expenditures FY2 |
| 567 | `anl10_cpxinnovate_increase_fy2` | MATRIX | 0.838 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for capital expenditures FY2 |
| 568 | `anl10_cpxinnovation_score_fy2` | MATRIX | 0.838 | 风险与质量 | 0 | — | — | — | UNTESTED | Innovation score for capital expenditures FY2 (innovate_increase - innovate_decrease) |
| 569 | `anl10_cpxnormal_decrease_fy2` | MATRIX | 0.838 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for capital expenditures FY2 |
| 570 | `anl10_cpxnormal_increase_fy2` | MATRIX | 0.838 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for capital expenditures FY2 |
| 571 | `anl10_cpxrevise_ratio_to_close_fy2` | MATRIX | 0.836 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for capital expenditures FY2 |
| 572 | `anl10_cpxrevise_ratio_to_consensus_fy2` | MATRIX | 0.836 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for capital expenditures FY2 |
| 573 | `anl10_cpxrevise_value_fy2` | MATRIX | 0.836 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for capital expenditures FY2 (difference between old and current updated value) |
| 574 | `anl10_oprfy2_consensus_185` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for operating profit FY2 |
| 575 | `anl10_oprfy2_pred_surps_v0_209` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 0 for operating profit for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 576 | `anl10_oprfy2_pred_surps_v1_182` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 1 for operating profit for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 577 | `anl10_oprfy2_pred_surps_v2_187` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise version 2 for operating profit for FY2 (calculated as (smart_ests - consensus)/consensus) |
| 578 | `anl10_oprfy2_smart_ests_v0_210` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 0 value for operating profit for FY2 |
| 579 | `anl10_oprfy2_smart_ests_v1_201` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 1 value for operating profit for FY2 |
| 580 | `anl10_oprfy2_smart_ests_v2_214` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Smart estimates version 2 value for operating profit for FY2 |
| 581 | `anl10_grmpast_det_analyst_802` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for gross margin estimates |
| 582 | `anl10_grmpast_det_anntime_796` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for gross margin estimates |
| 583 | `anl10_grmpast_det_estage_799` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of gross margin estimates in days |
| 584 | `anl10_grmpast_det_estflag_801` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for gross margin |
| 585 | `anl10_grmpast_det_estvalue_803` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for gross margin |
| 586 | `anl10_grmpast_det_excflag_805` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for gross margin estimates |
| 587 | `anl10_grmpast_det_indicator_798` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for gross margin estimates |
| 588 | `anl10_smartest_tbv_fq1_nums` | MATRIX | 0.758 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts contributing Fiscal Quarter 1 forecasts (coverage) |
| 589 | `anl10_smartest_tbv_fq2_nums` | MATRIX | 0.758 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts contributing Fiscal Quarter 2 forecasts (coverage) |
| 590 | `anl10_smartest_tbv_fy1_nums` | MATRIX | 0.758 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts contributing Fiscal Year 1 forecasts (coverage) |
| 591 | `anl10_smartest_tbv_fy2_nums` | MATRIX | 0.758 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of analysts contributing Fiscal Year 2 forecasts (coverage), aligned to the D1 regime |
| 592 | `anl10_smartest_tbv_fy1_consensus` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor IBES consensus estimate for the TBV item for fiscal year 1 at D1 |
| 593 | `anl10_smartest_tbv_fy1_pred_surps_v0` | MATRIX | 0.754 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for fiscal year 1, version v0 (raw model), D1-aligned |
| 594 | `anl10_smartest_tbv_fy1_pred_surps_v1` | MATRIX | 0.754 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for fiscal year 1, version v1 (stabilized), D1-aligned |
| 595 | `anl10_smartest_tbv_fy1_pred_surps_v2` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise (version v2) for fiscal year 1 TBV relative to D1 consensus |
| 596 | `anl10_smartest_tbv_fy1_smart_ests_v0` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Proprietary SmartEstimate for Fiscal Year 1, version v0 (raw) |
| 597 | `anl10_smartest_tbv_fy1_smart_ests_v1` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Proprietary SmartEstimate for Fiscal Year 1, version v1 (stabilized) |
| 598 | `anl10_smartest_tbv_fy1_smart_ests_v2` | MATRIX | 0.754 | 修正与预期 | 0 | — | — | — | UNTESTED | Proprietary SmartEstimate for fiscal year 1, version v2 (refined/smoothed), D1-aligned |
| 599 | `anl10_smartest_tbv_fy2_consensus` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor IBES consensus estimate for the TBV item for fiscal year 2 at D1 |
| 600 | `anl10_smartest_tbv_fy2_pred_surps_v0` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted earnings surprise for fiscal year 2, version v0 (raw model), D1-aligned |
| 601 | `anl10_smartest_tbv_fy2_pred_surps_v1` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | Predicted surprise for the TBV item for fiscal year 2 at D1, version v1 (processed), measured relative to the D1 consens |
| 602 | `anl10_smartest_tbv_fy2_pred_surps_v2` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | Predicted surprise for fiscal year 2 (version 2), aligned to the D1 regime |
| 603 | `anl10_smartest_tbv_fy2_smart_ests_v0` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Proprietary SmartEstimate for Fiscal Year 2, version v0 (raw) |
| 604 | `anl10_smartest_tbv_fy2_smart_ests_v1` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Proprietary SmartEstimate for Fiscal Year 2, version v1 (stabilized) |
| 605 | `anl10_smartest_tbv_fy2_smart_ests_v2` | MATRIX | 0.741 | 修正与预期 | 0 | — | — | — | UNTESTED | Proprietary SmartEstimate for Fiscal Year 2, version v2 (refined/smoothed) |
| 606 | `anl10_tbvpast_det_analyst` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for tangible book value estimates |
| 607 | `anl10_tbvpast_det_anntime` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for tangible book value estimates |
| 608 | `anl10_tbvpast_det_estage` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of tangible book value estimates in days |
| 609 | `anl10_tbvpast_det_estflag` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for tangible book value |
| 610 | `anl10_tbvpast_det_estvalue` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for tangible book value |
| 611 | `anl10_tbvpast_det_excflag` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for tangible book value estimates |
| 612 | `anl10_tbvpast_det_indicator` | VECTOR | 0.720 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for tangible book value estimates |
| 613 | `anl10_cshpast_det_analyst` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst ID for cash or cash equivalents estimates |
| 614 | `anl10_cshpast_det_anntime` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Announce time for cash or cash equivalents estimates |
| 615 | `anl10_cshpast_det_estage` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Age of cash or cash equivalents estimates in days |
| 616 | `anl10_cshpast_det_estflag` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate flag for cash or cash equivalents |
| 617 | `anl10_cshpast_det_estvalue` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate value for cash or cash equivalents |
| 618 | `anl10_cshpast_det_excflag` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Exclusion flag for cash or cash equivalents estimates |
| 619 | `anl10_cshpast_det_indicator` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for cash or cash equivalents estimates |
| 620 | `anl10_grminnovate_decrease_fy1` | MATRIX | 0.660 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for gross margin FY1 |
| 621 | `anl10_grminnovate_increase_fy1` | MATRIX | 0.660 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for gross margin FY1 |
| 622 | `anl10_grminnovation_score_fy1` | MATRIX | 0.660 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for gross margin FY1 (innovate_increase - innovate_decrease) |
| 623 | `anl10_grmnormal_decrease_fy1` | MATRIX | 0.660 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for gross margin FY1 |
| 624 | `anl10_grmnormal_increase_fy1` | MATRIX | 0.660 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for gross margin FY1 |
| 625 | `anl10_grmrevise_ratio_to_close_fy1` | MATRIX | 0.657 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for gross margin FY1 |
| 626 | `anl10_grmrevise_ratio_to_consensus_fy1` | MATRIX | 0.657 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross margin FY1 |
| 627 | `anl10_grmrevise_value_fy1` | MATRIX | 0.657 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for gross margin FY1 (difference between old and current updated value) |
| 628 | `anl10_grminnovate_decrease_fy2` | MATRIX | 0.656 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative negative revisions for gross margin FY2 |
| 629 | `anl10_grminnovate_increase_fy2` | MATRIX | 0.656 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with innovative positive revisions for gross margin FY2 |
| 630 | `anl10_grminnovation_score_fy2` | MATRIX | 0.656 | 盈利与财务 | 0 | — | — | — | UNTESTED | Innovation score for gross margin FY2 (innovate_increase - innovate_decrease) |
| 631 | `anl10_grmnormal_decrease_fy2` | MATRIX | 0.656 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal negative revisions for gross margin FY2 |
| 632 | `anl10_grmnormal_increase_fy2` | MATRIX | 0.656 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts with normal positive revisions for gross margin FY2 |
| 633 | `anl10_grmrevise_ratio_to_close_fy2` | MATRIX | 0.652 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of delta consensus to adjusted close for gross margin FY2 |
| 634 | `anl10_grmrevise_ratio_to_consensus_fy2` | MATRIX | 0.652 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus estimate value for gross margin FY2 |
| 635 | `anl10_grmrevise_value_fy2` | MATRIX | 0.652 | 修正与预期 | 0 | — | — | — | UNTESTED | Delta consensus for gross margin FY2 (difference between old and current updated value) |
| 636 | `historical_estimate_currency_tangible_book_value` | VECTOR | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency in which a past analyst estimate for tangible book value was reported. |
| 637 | `anl10_cshinnovate_decrease_fy1` | MATRIX | 0.589 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for cash or cash equivalents FY1 |
| 638 | `anl10_cshinnovate_increase_fy1` | MATRIX | 0.589 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for cash or cash equivalents FY1 |
| 639 | `anl10_cshinnovation_score_fy1` | MATRIX | 0.589 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for cash or cash equivalents FY1 (innovate_increase - innovate_decrease) |
| 640 | `anl10_cshnormal_decrease_fy1` | MATRIX | 0.589 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for cash or cash equivalents FY1 |
| 641 | `anl10_cshnormal_increase_fy1` | MATRIX | 0.589 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for cash or cash equivalents FY1 |
| 642 | `anl10_cshrevise_ratio_to_close_fy1` | MATRIX | 0.588 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for cash or cash equivalents FY1 |
| 643 | `anl10_cshrevise_ratio_to_consensus_fy1` | MATRIX | 0.588 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for cash or cash equivalents FY1 |
| 644 | `anl10_cshrevise_value_fy1` | MATRIX | 0.588 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for cash or cash equivalents FY1 (difference between old and current updated value) |
| 645 | `anl10_cshinnovate_decrease_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for cash or cash equivalents FY2 |
| 646 | `anl10_cshinnovate_increase_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for cash or cash equivalents FY2 |
| 647 | `anl10_cshinnovation_score_fy2` | MATRIX | 0.586 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for cash or cash equivalents FY2 (innovate_increase - innovate_decrease) |
| 648 | `anl10_cshnormal_decrease_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for cash or cash equivalents FY2 |
| 649 | `anl10_cshnormal_increase_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for cash or cash equivalents FY2 |
| 650 | `anl10_cshrevise_ratio_to_close_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for cash or cash equivalents FY2 |
| 651 | `anl10_cshrevise_ratio_to_consensus_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for cash or cash equivalents FY2 |
| 652 | `anl10_cshrevise_value_fy2` | MATRIX | 0.586 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for cash or cash equivalents FY2 (difference between old and current updated value) |
| 653 | `anl10_salfq1_consensus_547` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for sales Q1 |
| 654 | `anl10_salfq1_pred_surps_v0_545` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for sales for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 655 | `anl10_salfq1_pred_surps_v1_557` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for sales for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 656 | `anl10_salfq1_pred_surps_v2_569` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for sales for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 657 | `anl10_salfq1_smart_ests_v0_565` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for sales for Q1 |
| 658 | `anl10_salfq1_smart_ests_v1_536` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for sales for Q1 |
| 659 | `anl10_salfq1_smart_ests_v2_534` | MATRIX | 0.583 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for sales for Q1 |
| 660 | `anl10_tbvinnovate_decrease_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for tangible book value FY1 |
| 661 | `anl10_tbvinnovate_increase_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for tangible book value FY1 |
| 662 | `anl10_tbvinnovation_score_fy1` | MATRIX | 0.559 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for tangible book value FY1 (innovate_increase - innovate_decrease) |
| 663 | `anl10_tbvnormal_decrease_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for tangible book value FY1 |
| 664 | `anl10_tbvnormal_increase_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for tangible book value FY1 |
| 665 | `anl10_tbvrevise_ratio_to_close_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for tangible book value FY1 |
| 666 | `anl10_tbvrevise_ratio_to_consensus_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for tangible book value FY1 |
| 667 | `anl10_tbvrevise_value_fy1` | MATRIX | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for tangible book value FY1 (difference between old and current updated value) |
| 668 | `anl10_oprpast_det_analyst` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst ID for operating profit estimates |
| 669 | `anl10_oprpast_det_anntime` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Announce time for operating profit estimates |
| 670 | `anl10_oprpast_det_estage` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Age of operating profit estimates in days |
| 671 | `anl10_oprpast_det_estflag` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimate flag for operating profit |
| 672 | `anl10_oprpast_det_estvalue` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimate value for operating profit |
| 673 | `anl10_oprpast_det_excflag` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Exclusion flag for operating profit estimates |
| 674 | `anl10_oprpast_det_indicator` | VECTOR | 0.552 | 修正与预期 | 0 | — | — | — | UNUSABLE | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1, 50=fy2) for operating profit estimates |
| 675 | `anl10_tbvinnovate_decrease_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for tangible book value FY2 |
| 676 | `anl10_tbvinnovate_increase_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for tangible book value FY2 |
| 677 | `anl10_tbvinnovation_score_fy2` | MATRIX | 0.549 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for tangible book value FY2 (innovate_increase - innovate_decrease) |
| 678 | `anl10_tbvnormal_decrease_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for tangible book value FY2 |
| 679 | `anl10_tbvnormal_increase_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for tangible book value FY2 |
| 680 | `anl10_tbvrevise_ratio_to_close_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for tangible book value FY2 |
| 681 | `anl10_tbvrevise_ratio_to_consensus_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for tangible book value FY2 |
| 682 | `anl10_tbvrevise_value_fy2` | MATRIX | 0.549 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for tangible book value FY2 (difference between old and current updated value) |
| 683 | `anl10_ebifq1_consensus_32` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before interest Q1 |
| 684 | `anl10_ebifq1_pred_surps_v0_40` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for earnings before interest for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 685 | `anl10_ebifq1_pred_surps_v1_29` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for earnings before interest for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 686 | `anl10_ebifq1_pred_surps_v2_9` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for earnings before interest for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 687 | `anl10_ebifq1_smart_ests_v0_21` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for earnings before interest for Q1 |
| 688 | `anl10_ebifq1_smart_ests_v1_16` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for earnings before interest for Q1 |
| 689 | `anl10_ebifq1_smart_ests_v2_19` | MATRIX | 0.541 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for earnings before interest for Q1 |
| 690 | `anl10_netfq1_consensus_613` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net income Q1 |
| 691 | `anl10_netfq1_pred_surps_v0_619` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for net income for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 692 | `anl10_netfq1_pred_surps_v1_640` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for net income for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 693 | `anl10_netfq1_pred_surps_v2_614` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for net income for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 694 | `anl10_netfq1_smart_ests_v0_618` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for net income for Q1 |
| 695 | `anl10_netfq1_smart_ests_v1_651` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for net income for Q1 |
| 696 | `anl10_netfq1_smart_ests_v2_628` | MATRIX | 0.529 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for net income for Q1 |
| 697 | `anl10_analyst_innovation_tbv_innovate_decrease_fy1` | MATRIX | 0.502 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for tangible book value FY1 |
| 698 | `anl10_analyst_innovation_tbv_innovate_increase_fy1` | MATRIX | 0.502 | 修正与预期 | 0 | — | — | — | UNUSABLE | Increase in innovation forecast for fiscal year 1 |
| 699 | `anl10_analyst_innovation_tbv_innovation_score_fy1` | MATRIX | 0.502 | 修正与预期 | 0 | — | — | — | UNUSABLE | Innovation score for fiscal year 1 |
| 700 | `anl10_analyst_innovation_tbv_normal_decrease_fy1` | MATRIX | 0.502 | 修正与预期 | 0 | — | — | — | UNUSABLE | Normal decrease in data for fiscal year 1 |
| 701 | `anl10_analyst_innovation_tbv_normal_increase_fy1` | MATRIX | 0.502 | 修正与预期 | 0 | — | — | — | UNUSABLE | Normal increase forecast for fiscal year 1 |
| 702 | `anl10_analyst_innovation_tbv_revise_ratio_to_close_fy1` | MATRIX | 0.501 | 修正与预期 | 0 | — | — | — | UNUSABLE | Revised ratio to close in fiscal year 1 |
| 703 | `anl10_analyst_innovation_tbv_revise_ratio_to_consensus_fy1` | MATRIX | 0.501 | 修正与预期 | 0 | — | — | — | UNUSABLE | Revision ratio to consensus forecast for the first fiscal year |
| 704 | `anl10_analyst_innovation_tbv_revise_value_fy1` | MATRIX | 0.501 | 修正与预期 | 0 | — | — | — | UNUSABLE | Revised value in fiscal year 1 |
| 705 | `anl10_det_full_tbv_past_det_analyst` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Unique identifier for the analyst issuing the estimate |
| 706 | `anl10_det_full_tbv_past_det_anntime` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Time of day the analyst report/forecast was announced |
| 707 | `anl10_det_full_tbv_past_det_estage` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Age of tangible book value estimates in days |
| 708 | `anl10_det_full_tbv_past_det_estflag` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Validity flag of the per-analyst estimate at the event; 0 = valid, non-zero = invalid or masked |
| 709 | `anl10_det_full_tbv_past_det_estvalue` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the analyst’s estimate at the event date |
| 710 | `anl10_det_full_tbv_past_det_excflag` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating analyst exclusion or regime break at that event (0=active, non-zero=excluded) |
| 711 | `anl10_det_full_tbv_past_det_indicator` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Code indicating the type of analyst event (for example, new estimate, revision, initiation) |
| 712 | `anl10_analyst_innovation_tbv_innovate_decrease_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Innovation decrease in fiscal year 2 |
| 713 | `anl10_analyst_innovation_tbv_innovate_increase_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Increase in innovation forecast for fiscal year 2 |
| 714 | `anl10_analyst_innovation_tbv_innovation_score_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst innovation/originality score for fiscal year 2 (FY2) forecasts, D1-aligned measure of forecast quality and leade |
| 715 | `anl10_analyst_innovation_tbv_normal_decrease_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Normal decrease in data for fiscal year 2 |
| 716 | `anl10_analyst_innovation_tbv_normal_increase_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Normal increase forecast for fiscal year 2 |
| 717 | `anl10_analyst_innovation_tbv_revise_ratio_to_close_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Revised ratio to close in fiscal year 2 |
| 718 | `anl10_analyst_innovation_tbv_revise_ratio_to_consensus_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Revision ratio to consensus forecast for the second fiscal year |
| 719 | `anl10_analyst_innovation_tbv_revise_value_fy2` | MATRIX | 0.499 | 修正与预期 | 0 | — | — | — | UNUSABLE | Revised value in fiscal year 2 |
| 720 | `anl10_nerfq1_consensus` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net earnings rate Q1 |
| 721 | `anl10_nerfq1_pred_surps_v0` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for net earnings rate for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 722 | `anl10_nerfq1_pred_surps_v1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for net earnings rate for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 723 | `anl10_nerfq1_pred_surps_v2` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for net earnings rate for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 724 | `anl10_nerfq1_smart_ests_v0` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for net earnings rate for Q1 |
| 725 | `anl10_nerfq1_smart_ests_v1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for net earnings rate for Q1 |
| 726 | `anl10_nerfq1_smart_ests_v2` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for net earnings rate for Q1 |
| 727 | `anl10_salinnovate_decrease_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for sales Q1 |
| 728 | `anl10_salinnovate_increase_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for sales Q1 |
| 729 | `anl10_salinnovation_score_fq1` | MATRIX | 0.481 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for sales Q1 (innovate_increase - innovate_decrease) |
| 730 | `anl10_salnormal_decrease_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for sales Q1 |
| 731 | `anl10_salnormal_increase_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for sales Q1 |
| 732 | `anl10_salrevise_ratio_to_close_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for sales Q1 |
| 733 | `anl10_salrevise_ratio_to_consensus_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for sales Q1 |
| 734 | `anl10_salrevise_value_fq1` | MATRIX | 0.481 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for sales Q1 (difference between old and current updated value) |
| 735 | `anl10_prefq1_consensus_490` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for pre-tax or preliminary Q1 |
| 736 | `anl10_prefq1_pred_surps_v0_477` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for pre-tax or preliminary for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 737 | `anl10_prefq1_pred_surps_v1_468` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for pre-tax or preliminary for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 738 | `anl10_prefq1_pred_surps_v2_467` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for pre-tax or preliminary for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 739 | `anl10_prefq1_smart_ests_v0_457` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for pre-tax or preliminary for Q1 |
| 740 | `anl10_prefq1_smart_ests_v1_454` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for pre-tax or preliminary for Q1 |
| 741 | `anl10_prefq1_smart_ests_v2_488` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for pre-tax or preliminary for Q1 |
| 742 | `anl10_ebtfq1_consensus` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before tax Q1 |
| 743 | `anl10_ebtfq1_pred_surps_v0` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for earnings before tax for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 744 | `anl10_ebtfq1_pred_surps_v1` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for earnings before tax for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 745 | `anl10_ebtfq1_pred_surps_v2` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for earnings before tax for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 746 | `anl10_ebtfq1_smart_ests_v0` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for earnings before tax for Q1 |
| 747 | `anl10_ebtfq1_smart_ests_v1` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for earnings before tax for Q1 |
| 748 | `anl10_ebtfq1_smart_ests_v2` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for earnings before tax for Q1 |
| 749 | `anl10_salfq2_consensus_540` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for sales Q2 |
| 750 | `anl10_salfq2_pred_surps_v0_549` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for sales for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 751 | `anl10_salfq2_pred_surps_v1_539` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for sales for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 752 | `anl10_salfq2_pred_surps_v2_551` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for sales for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 753 | `anl10_salfq2_smart_ests_v0_555` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for sales for Q2 |
| 754 | `anl10_salfq2_smart_ests_v1_567` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for sales for Q2 |
| 755 | `anl10_salfq2_smart_ests_v2_556` | MATRIX | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for sales for Q2 |
| 756 | `anl10_gpsfq1_consensus_446` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for gross profit per share Q1 |
| 757 | `anl10_gpsfq1_pred_surps_v0_422` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for gross profit per share for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 758 | `anl10_gpsfq1_pred_surps_v1_440` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for gross profit per share for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 759 | `anl10_gpsfq1_pred_surps_v2_427` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for gross profit per share for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 760 | `anl10_gpsfq1_smart_ests_v0_425` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for gross profit per share for Q1 |
| 761 | `anl10_gpsfq1_smart_ests_v1_409` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for gross profit per share for Q1 |
| 762 | `anl10_gpsfq1_smart_ests_v2_436` | MATRIX | 0.457 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for gross profit per share for Q1 |
| 763 | `anl10_netfq2_consensus_625` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net income Q2 |
| 764 | `anl10_netfq2_pred_surps_v0_642` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for net income for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 765 | `anl10_netfq2_pred_surps_v1_644` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for net income for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 766 | `anl10_netfq2_pred_surps_v2_645` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for net income for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 767 | `anl10_netfq2_smart_ests_v0_629` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for net income for Q2 |
| 768 | `anl10_netfq2_smart_ests_v1_615` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for net income for Q2 |
| 769 | `anl10_netfq2_smart_ests_v2_630` | MATRIX | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for net income for Q2 |
| 770 | `anl10_ebiinnovate_decrease_fq1` | MATRIX | 0.436 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for earnings before interest Q1 |
| 771 | `anl10_ebiinnovate_increase_fq1` | MATRIX | 0.436 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for earnings before interest Q1 |
| 772 | `anl10_ebiinnovation_score_fq1` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for earnings before interest Q1 (innovate_increase - innovate_decrease) |
| 773 | `anl10_ebinormal_decrease_fq1` | MATRIX | 0.436 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for earnings before interest Q1 |
| 774 | `anl10_ebinormal_increase_fq1` | MATRIX | 0.436 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for earnings before interest Q1 |
| 775 | `anl10_ebirevise_ratio_to_close_fq1` | MATRIX | 0.435 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for earnings before interest Q1 |
| 776 | `anl10_ebirevise_ratio_to_consensus_fq1` | MATRIX | 0.435 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before interest Q1 |
| 777 | `anl10_ebirevise_value_fq1` | MATRIX | 0.435 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for earnings before interest Q1 (difference between old and current updated value) |
| 778 | `anl10_netinnovate_decrease_fq1` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for net income Q1 |
| 779 | `anl10_netinnovate_increase_fq1` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for net income Q1 |
| 780 | `anl10_netinnovation_score_fq1` | MATRIX | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for net income Q1 (innovate_increase - innovate_decrease) |
| 781 | `anl10_netnormal_decrease_fq1` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for net income Q1 |
| 782 | `anl10_netnormal_increase_fq1` | MATRIX | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for net income Q1 |
| 783 | `anl10_ebifq2_consensus_10` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before interest Q2 |
| 784 | `anl10_ebifq2_pred_surps_v0_37` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for earnings before interest for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 785 | `anl10_ebifq2_pred_surps_v1_34` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for earnings before interest for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 786 | `anl10_ebifq2_pred_surps_v2_26` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for earnings before interest for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 787 | `anl10_ebifq2_smart_ests_v0_38` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for earnings before interest for Q2 |
| 788 | `anl10_ebifq2_smart_ests_v1_3` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for earnings before interest for Q2 |
| 789 | `anl10_ebifq2_smart_ests_v2_27` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for earnings before interest for Q2 |
| 790 | `anl10_netrevise_ratio_to_close_fq1` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for net income Q1 |
| 791 | `anl10_netrevise_ratio_to_consensus_fq1` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net income Q1 |
| 792 | `anl10_netrevise_value_fq1` | MATRIX | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for net income Q1 (difference between old and current updated value) |
| 793 | `anl10_prrfq1_consensus` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for price return ratio Q1 |
| 794 | `anl10_prrfq1_pred_surps_v0` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for price return ratio for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 795 | `anl10_prrfq1_pred_surps_v1` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for price return ratio for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 796 | `anl10_prrfq1_pred_surps_v2` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for price return ratio for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 797 | `anl10_prrfq1_smart_ests_v0` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for price return ratio for Q1 |
| 798 | `anl10_prrfq1_smart_ests_v1` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for price return ratio for Q1 |
| 799 | `anl10_prrfq1_smart_ests_v2` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for price return ratio for Q1 |
| 800 | `anl10_gpsfq2_consensus_416` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for gross profit per share Q2 |
| 801 | `anl10_gpsfq2_pred_surps_v0_434` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for gross profit per share for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 802 | `anl10_gpsfq2_pred_surps_v1_439` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for gross profit per share for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 803 | `anl10_gpsfq2_pred_surps_v2_435` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for gross profit per share for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 804 | `anl10_gpsfq2_smart_ests_v0_431` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for gross profit per share for Q2 |
| 805 | `anl10_gpsfq2_smart_ests_v1_428` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for gross profit per share for Q2 |
| 806 | `anl10_gpsfq2_smart_ests_v2_412` | MATRIX | 0.409 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for gross profit per share for Q2 |
| 807 | `anl10_nerinnovate_decrease_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for net earnings rate Q1 |
| 808 | `anl10_nerinnovate_increase_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for net earnings rate Q1 |
| 809 | `anl10_nerinnovation_score_fq1` | MATRIX | 0.394 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for net earnings rate Q1 (innovate_increase - innovate_decrease) |
| 810 | `anl10_nernormal_decrease_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for net earnings rate Q1 |
| 811 | `anl10_nernormal_increase_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for net earnings rate Q1 |
| 812 | `anl10_nerrevise_ratio_to_close_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for net earnings rate Q1 |
| 813 | `anl10_nerrevise_ratio_to_consensus_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net earnings rate Q1 |
| 814 | `anl10_nerrevise_value_fq1` | MATRIX | 0.394 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for net earnings rate Q1 (difference between old and current updated value) |
| 815 | `anl10_nerfq2_consensus` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net earnings rate Q2 |
| 816 | `anl10_nerfq2_pred_surps_v0` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for net earnings rate for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 817 | `anl10_nerfq2_pred_surps_v1` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for net earnings rate for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 818 | `anl10_nerfq2_pred_surps_v2` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for net earnings rate for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 819 | `anl10_nerfq2_smart_ests_v0` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for net earnings rate for Q2 |
| 820 | `anl10_nerfq2_smart_ests_v1` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for net earnings rate for Q2 |
| 821 | `anl10_nerfq2_smart_ests_v2` | MATRIX | 0.391 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for net earnings rate for Q2 |
| 822 | `anl10_gpsinnovate_decrease_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for gross profit per share Q1 |
| 823 | `anl10_gpsinnovate_increase_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for gross profit per share Q1 |
| 824 | `anl10_gpsinnovation_score_fq1` | MATRIX | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for gross profit per share Q1 (innovate_increase - innovate_decrease) |
| 825 | `anl10_gpsnormal_decrease_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for gross profit per share Q1 |
| 826 | `anl10_gpsnormal_increase_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for gross profit per share Q1 |
| 827 | `anl10_gpsrevise_ratio_to_close_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for gross profit per share Q1 |
| 828 | `anl10_gpsrevise_ratio_to_consensus_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for gross profit per share Q1 |
| 829 | `anl10_gpsrevise_value_fq1` | MATRIX | 0.384 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for gross profit per share Q1 (difference between old and current updated value) |
| 830 | `anl10_salinnovate_decrease_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for sales Q2 |
| 831 | `anl10_salinnovate_increase_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for sales Q2 |
| 832 | `anl10_salinnovation_score_fq2` | MATRIX | 0.382 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for sales Q2 (innovate_increase - innovate_decrease) |
| 833 | `anl10_salnormal_decrease_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for sales Q2 |
| 834 | `anl10_salnormal_increase_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for sales Q2 |
| 835 | `anl10_salrevise_ratio_to_close_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for sales Q2 |
| 836 | `anl10_salrevise_ratio_to_consensus_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for sales Q2 |
| 837 | `anl10_salrevise_value_fq2` | MATRIX | 0.382 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for sales Q2 (difference between old and current updated value) |
| 838 | `anl10_preinnovate_decrease_fq1` | MATRIX | 0.377 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for pre-tax or preliminary Q1 |
| 839 | `anl10_preinnovate_increase_fq1` | MATRIX | 0.377 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for pre-tax or preliminary Q1 |
| 840 | `anl10_preinnovation_score_fq1` | MATRIX | 0.377 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for pre-tax or preliminary Q1 (innovate_increase - innovate_decrease) |
| 841 | `anl10_prenormal_decrease_fq1` | MATRIX | 0.377 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for pre-tax or preliminary Q1 |
| 842 | `anl10_prenormal_increase_fq1` | MATRIX | 0.377 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for pre-tax or preliminary Q1 |
| 843 | `anl10_prerevise_ratio_to_close_fq1` | MATRIX | 0.376 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for pre-tax or preliminary Q1 |
| 844 | `anl10_prerevise_ratio_to_consensus_fq1` | MATRIX | 0.376 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for pre-tax or preliminary Q1 |
| 845 | `anl10_prerevise_value_fq1` | MATRIX | 0.376 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for pre-tax or preliminary Q1 (difference between old and current updated value) |
| 846 | `anl10_ebtfq2_consensus` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before tax Q2 |
| 847 | `anl10_ebtfq2_pred_surps_v0` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for earnings before tax for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 848 | `anl10_ebtfq2_pred_surps_v1` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for earnings before tax for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 849 | `anl10_ebtfq2_pred_surps_v2` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for earnings before tax for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 850 | `anl10_ebtfq2_smart_ests_v0` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for earnings before tax for Q2 |
| 851 | `anl10_ebtfq2_smart_ests_v1` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for earnings before tax for Q2 |
| 852 | `anl10_ebtfq2_smart_ests_v2` | MATRIX | 0.375 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for earnings before tax for Q2 |
| 853 | `anl10_ebtinnovate_decrease_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for earnings before tax Q1 |
| 854 | `anl10_ebtinnovate_increase_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for earnings before tax Q1 |
| 855 | `anl10_ebtinnovation_score_fq1` | MATRIX | 0.373 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for earnings before tax Q1 (innovate_increase - innovate_decrease) |
| 856 | `anl10_ebtnormal_decrease_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for earnings before tax Q1 |
| 857 | `anl10_ebtnormal_increase_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for earnings before tax Q1 |
| 858 | `anl10_ebtrevise_ratio_to_close_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for earnings before tax Q1 |
| 859 | `anl10_ebtrevise_ratio_to_consensus_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before tax Q1 |
| 860 | `anl10_ebtrevise_value_fq1` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for earnings before tax Q1 (difference between old and current updated value) |
| 861 | `anl10_prefq2_consensus_461` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for pre-tax or preliminary Q2 |
| 862 | `anl10_prefq2_pred_surps_v0_450` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for pre-tax or preliminary for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 863 | `anl10_prefq2_pred_surps_v1_479` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for pre-tax or preliminary for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 864 | `anl10_prefq2_pred_surps_v2_453` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for pre-tax or preliminary for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 865 | `anl10_prefq2_smart_ests_v0_469` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for pre-tax or preliminary for Q2 |
| 866 | `anl10_prefq2_smart_ests_v1_483` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for pre-tax or preliminary for Q2 |
| 867 | `anl10_prefq2_smart_ests_v2_460` | MATRIX | 0.371 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for pre-tax or preliminary for Q2 |
| 868 | `anl10_netinnovate_decrease_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for net income Q2 |
| 869 | `anl10_netinnovate_increase_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for net income Q2 |
| 870 | `anl10_netinnovation_score_fq2` | MATRIX | 0.343 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for net income Q2 (innovate_increase - innovate_decrease) |
| 871 | `anl10_netnormal_decrease_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for net income Q2 |
| 872 | `anl10_netnormal_increase_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for net income Q2 |
| 873 | `anl10_netrevise_ratio_to_close_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for net income Q2 |
| 874 | `anl10_netrevise_ratio_to_consensus_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net income Q2 |
| 875 | `anl10_netrevise_value_fq2` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for net income Q2 (difference between old and current updated value) |
| 876 | `anl10_prrinnovate_decrease_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for price return ratio Q1 |
| 877 | `anl10_prrinnovate_increase_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for price return ratio Q1 |
| 878 | `anl10_prrinnovation_score_fq1` | MATRIX | 0.338 | 价量与波动 | 0 | — | — | — | UNUSABLE | Innovation score for price return ratio Q1 (innovate_increase - innovate_decrease) |
| 879 | `anl10_prrnormal_decrease_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for price return ratio Q1 |
| 880 | `anl10_prrnormal_increase_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for price return ratio Q1 |
| 881 | `anl10_prrrevise_ratio_to_close_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for price return ratio Q1 |
| 882 | `anl10_prrrevise_ratio_to_consensus_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for price return ratio Q1 |
| 883 | `anl10_prrrevise_value_fq1` | MATRIX | 0.338 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for price return ratio Q1 (difference between old and current updated value) |
| 884 | `anl10_ebiinnovate_decrease_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for earnings before interest Q2 |
| 885 | `anl10_ebiinnovate_increase_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for earnings before interest Q2 |
| 886 | `anl10_ebiinnovation_score_fq2` | MATRIX | 0.336 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for earnings before interest Q2 (innovate_increase - innovate_decrease) |
| 887 | `anl10_ebinormal_decrease_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for earnings before interest Q2 |
| 888 | `anl10_ebinormal_increase_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for earnings before interest Q2 |
| 889 | `anl10_ebirevise_ratio_to_close_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for earnings before interest Q2 |
| 890 | `anl10_ebirevise_ratio_to_consensus_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before interest Q2 |
| 891 | `anl10_ebirevise_value_fq2` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for earnings before interest Q2 (difference between old and current updated value) |
| 892 | `anl10_prrfq2_consensus` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for price return ratio Q2 |
| 893 | `anl10_prrfq2_pred_surps_v0` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for price return ratio for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 894 | `anl10_prrfq2_pred_surps_v1` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for price return ratio for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 895 | `anl10_prrfq2_pred_surps_v2` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for price return ratio for Q2 (calculated as (smart_ests - consensus)/consensus) |
| 896 | `anl10_prrfq2_smart_ests_v0` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for price return ratio for Q2 |
| 897 | `anl10_prrfq2_smart_ests_v1` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for price return ratio for Q2 |
| 898 | `anl10_prrfq2_smart_ests_v2` | MATRIX | 0.333 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for price return ratio for Q2 |
| 899 | `anl10_gpsinnovate_decrease_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for gross profit per share Q2 |
| 900 | `anl10_gpsinnovate_increase_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for gross profit per share Q2 |
| 901 | `anl10_gpsinnovation_score_fq2` | MATRIX | 0.323 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for gross profit per share Q2 (innovate_increase - innovate_decrease) |
| 902 | `anl10_gpsnormal_decrease_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for gross profit per share Q2 |
| 903 | `anl10_gpsnormal_increase_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for gross profit per share Q2 |
| 904 | `anl10_gpsrevise_ratio_to_close_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for gross profit per share Q2 |
| 905 | `anl10_gpsrevise_ratio_to_consensus_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for gross profit per share Q2 |
| 906 | `anl10_gpsrevise_value_fq2` | MATRIX | 0.323 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for gross profit per share Q2 (difference between old and current updated value) |
| 907 | `anl10_oprinnovate_decrease_fy1` | MATRIX | 0.321 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for operating profit FY1 |
| 908 | `anl10_oprinnovate_increase_fy1` | MATRIX | 0.321 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for operating profit FY1 |
| 909 | `anl10_oprinnovation_score_fy1` | MATRIX | 0.321 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for operating profit FY1 (innovate_increase - innovate_decrease) |
| 910 | `anl10_oprnormal_decrease_fy1` | MATRIX | 0.321 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for operating profit FY1 |
| 911 | `anl10_oprnormal_increase_fy1` | MATRIX | 0.321 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for operating profit FY1 |
| 912 | `anl10_oprrevise_ratio_to_close_fy1` | MATRIX | 0.320 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for operating profit FY1 |
| 913 | `anl10_oprrevise_ratio_to_consensus_fy1` | MATRIX | 0.320 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for operating profit FY1 |
| 914 | `anl10_oprrevise_value_fy1` | MATRIX | 0.320 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for operating profit FY1 (difference between old and current updated value) |
| 915 | `anl10_nerinnovate_decrease_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for net earnings rate Q2 |
| 916 | `anl10_nerinnovate_increase_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for net earnings rate Q2 |
| 917 | `anl10_nerinnovation_score_fq2` | MATRIX | 0.310 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for net earnings rate Q2 (innovate_increase - innovate_decrease) |
| 918 | `anl10_nernormal_decrease_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for net earnings rate Q2 |
| 919 | `anl10_nernormal_increase_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for net earnings rate Q2 |
| 920 | `anl10_nerrevise_ratio_to_close_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for net earnings rate Q2 |
| 921 | `anl10_nerrevise_ratio_to_consensus_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for net earnings rate Q2 |
| 922 | `anl10_nerrevise_value_fq2` | MATRIX | 0.310 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for net earnings rate Q2 (difference between old and current updated value) |
| 923 | `anl10_ebtinnovate_decrease_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for earnings before tax Q2 |
| 924 | `anl10_ebtinnovate_increase_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for earnings before tax Q2 |
| 925 | `anl10_ebtinnovation_score_fq2` | MATRIX | 0.287 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for earnings before tax Q2 (innovate_increase - innovate_decrease) |
| 926 | `anl10_ebtnormal_decrease_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for earnings before tax Q2 |
| 927 | `anl10_ebtnormal_increase_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for earnings before tax Q2 |
| 928 | `anl10_ebtrevise_ratio_to_close_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for earnings before tax Q2 |
| 929 | `anl10_ebtrevise_ratio_to_consensus_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for earnings before tax Q2 |
| 930 | `anl10_ebtrevise_value_fq2` | MATRIX | 0.287 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for earnings before tax Q2 (difference between old and current updated value) |
| 931 | `anl10_preinnovate_decrease_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for pre-tax or preliminary Q2 |
| 932 | `anl10_preinnovate_increase_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for pre-tax or preliminary Q2 |
| 933 | `anl10_preinnovation_score_fq2` | MATRIX | 0.286 | 风险与质量 | 0 | — | — | — | UNUSABLE | Innovation score for pre-tax or preliminary Q2 (innovate_increase - innovate_decrease) |
| 934 | `anl10_prenormal_decrease_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for pre-tax or preliminary Q2 |
| 935 | `anl10_prenormal_increase_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for pre-tax or preliminary Q2 |
| 936 | `anl10_prerevise_ratio_to_close_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for pre-tax or preliminary Q2 |
| 937 | `anl10_prerevise_ratio_to_consensus_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for pre-tax or preliminary Q2 |
| 938 | `anl10_prerevise_value_fq2` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for pre-tax or preliminary Q2 (difference between old and current updated value) |
| 939 | `anl10_oprinnovate_decrease_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for operating profit FY2 |
| 940 | `anl10_oprinnovate_increase_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for operating profit FY2 |
| 941 | `anl10_oprinnovation_score_fy2` | MATRIX | 0.278 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Innovation score for operating profit FY2 (innovate_increase - innovate_decrease) |
| 942 | `anl10_oprnormal_decrease_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for operating profit FY2 |
| 943 | `anl10_oprnormal_increase_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for operating profit FY2 |
| 944 | `anl10_oprrevise_ratio_to_close_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for operating profit FY2 |
| 945 | `anl10_oprrevise_ratio_to_consensus_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for operating profit FY2 |
| 946 | `anl10_oprrevise_value_fy2` | MATRIX | 0.278 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for operating profit FY2 (difference between old and current updated value) |
| 947 | `anl10_prrinnovate_decrease_fq2` | MATRIX | 0.266 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative negative revisions for price return ratio Q2 |
| 948 | `anl10_prrinnovate_increase_fq2` | MATRIX | 0.266 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with innovative positive revisions for price return ratio Q2 |
| 949 | `anl10_prrinnovation_score_fq2` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | Innovation score for price return ratio Q2 (innovate_increase - innovate_decrease) |
| 950 | `anl10_prrnormal_decrease_fq2` | MATRIX | 0.266 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal negative revisions for price return ratio Q2 |
| 951 | `anl10_prrnormal_increase_fq2` | MATRIX | 0.266 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts with normal positive revisions for price return ratio Q2 |
| 952 | `anl10_prrrevise_ratio_to_close_fq2` | MATRIX | 0.265 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of delta consensus to adjusted close for price return ratio Q2 |
| 953 | `anl10_prrrevise_ratio_to_consensus_fq2` | MATRIX | 0.265 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for price return ratio Q2 |
| 954 | `anl10_prrrevise_value_fq2` | MATRIX | 0.265 | 修正与预期 | 0 | — | — | — | UNUSABLE | Delta consensus for price return ratio Q2 (difference between old and current updated value) |
| 955 | `anl10_ndtfq1_consensus` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate value for date Q1 |
| 956 | `anl10_ndtfq1_pred_surps_v0` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 0 for date for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 957 | `anl10_ndtfq1_pred_surps_v1` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 1 for date for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 958 | `anl10_ndtfq1_pred_surps_v2` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise version 2 for date for Q1 (calculated as (smart_ests - consensus)/consensus) |
| 959 | `anl10_ndtfq1_smart_ests_v0` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 0 value for date for Q1 |
| 960 | `anl10_ndtfq1_smart_ests_v1` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 1 value for date for Q1 |
| 961 | `anl10_ndtfq1_smart_ests_v2` | MATRIX | 0.252 | 修正与预期 | 0 | — | — | — | UNUSABLE | Smart estimates version 2 value for date for Q1 |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `e7bg5EOz` | 0.64 | 0.24 | 0.17 | 0.52 | 0.04 | ["LOW_SHARPE | 209 | `rank(ts_mean(anl10_netfy1_pred_surps_v1_620, 5))` |
| `A1NYVEPY` | 0.58 | 0.20 | 0.79 | 0.54 | 0.04 | ["LOW_SHARPE | 209 | `rank(ts_mean(anl10_salfy1_pred_surps_v1_533, 5))` |
| `78N0LlnO` | 0.55 | 0.22 | -0.39 | 0.37 | 0.06 | ["LOW_SHARPE | 209 | `rank(subtract(ts_mean(anl10_netinnovate_increase_fy1, 22), ts_mean(anl10_netinnovate_decre` |
| `pwRod3Kq` | 0.53 | 0.21 | -0.07 | 0.40 | 0.05 | ["LOW_SHARPE | 209 | `rank(ts_mean(anl10_ebtinnovation_score_fy1, 22))` |
| `LLNqM3pa` | 0.49 | 0.16 | -0.14 | 0.63 | 0.04 | ["LOW_SHARPE | 209 | `rank(ts_mean(anl10_ebtfy1_pred_surps_v1, 5))` |
| `KPNqJZ9g` | 0.37 | 0.10 | -0.39 | 0.49 | 0.03 | ["LOW_SHARPE | 209 | `rank(ts_decay_linear(anl10_ebtfy1_pred_surps_v1, 22))` |
| `O0NqAgxp` | 0.31 | 0.10 | -0.08 | 0.19 | 0.06 | ["LOW_SHARPE | 209 | `rank(ts_mean(anl10_ebtrevise_ratio_to_close_fy1, 22))` |
| `78N0Llw5` | 0.29 | 0.07 | 0.25 | 0.10 | 0.04 | ["LOW_SHARPE | 209 | `rank(ts_mean(anl10_prefy1_pred_surps_v1_474, 5))` |

## 七、判死记录（sealed dead_end）

- `EUR-DLRF-EUROHLCMA-TURNOVER-FITNESS-WALL`（None）family=dl_riskfree_returns eur_ohlc_ma EUR 专用模型族 × 跨期分位数差：{"d4_verdict": "未达资格线（最强 Sharpe 1.48>=1.25 但 Fitness 0.36<0.8）→ 判死，不进 near_pool、不发 Mode B 增强波", "dataset": "dl_riskfree_returns", "evidence": {"78ZnxblZ": "L4-L0@50d-5d tsv22 S0.82/F0.17/2Y0.03 3FAIL（拉长窗口反而更差）", "E5veaQKm": "L3-L0@50d-5d S1.13/F0.27/2Y0.87 fail=[]", "O0rxnea7": "L4-L0@50d-5d S0.84/F0.16/2Y-0.03 3FAIL", "ZY0Klv83": "L3-L1@50d-5d S1.30/F0.30/2Y1.22 prod0.3751 fail=[]", "akLENZa5": "
- `EUR-ANALYST10-PREDICTED-SURPRISE-DEAD`（2026-09-19）family=analyst10 performance-weighted estimates (predicted surprise EBT/net/pretax/sales, innovation counts, revision ratio)：{"id": "EUR-ANALYST10-PREDICTED-SURPRISE-DEAD", "dataset": "analyst10", "wave": 209, "universe": "TOPCS1600", "evidence": "8 probes /S/<=0.64: net FY1 pred surprise 0.64 (2Y 0.17), sales 0.58, innovation counts 0.55, EBT pred surprise 0.49 (2Y -0.14), revision/close 0.31, pretax 0.29", "verdict": "SmartEstimate-style predicted surprise has no EUR signal at D1 (unlike ASI model30 3.28); analyst tow

