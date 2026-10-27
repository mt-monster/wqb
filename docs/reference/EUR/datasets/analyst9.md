# analyst9 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst9` |
| 名称 | Analyst Estimate Daily Data |
| 类别 | ANALYST |
| 数据字段数(平台) | 111 |
| 覆盖率 | 0.6166 |
| 平台已有 alpha | 78 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RIC) and Bloomberg Identifiers (BBID), facilitating cross-platform security identification. It is sourced from both Bloomberg and Refinitiv, ensuring broad coverage and accuracy. The mapping enables users to link securities across different data providers and trading systems, which is essential for portfolio management, trade reconciliation, and data integration tasks. While not directly predictive of price movements, the dataset is crucial for ensuring data consistency and enabling the use of multiple datasets in quantitative research and trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **111** |
| 类型分布 | VECTOR×106　MATRIX×5 |
| 平均覆盖率 | **0.617** |
| 覆盖率区间 | 0.22 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 4 | 3.6% |
| 中 (0.70–0.90) | 26 | 23.4% |
| 低 (0.50–0.70) | 74 | 66.7% |
| 稀疏 (<0.50) | 7 | 6.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 63 | 56.8% |
| UNTESTED | 42 | 37.8% |
| DEAD | 6 | 5.4% |

- 已实测字段：**6** 个（5%），best_sharpe 最高 **1.01**，中位 0.17

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 107 | 0.61 | anl9_daily_numup、eps_consensus_estimate_value、anl9_consensusanalysis_dataitemvalue |
| 其他 | 3 | 0.62 | anl9_sdetail_effectivetime、anl9_scaleconversionflag、anl9_sdetail_dataitemvalue |
| 宏观与行业 | 1 | 0.97 | base_currency_conversion_indicator |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl9_daily_numup` | VECTOR | 0.553 | 修正与预期 | 2 | 1.01 | 1.63 | 0.75 | DEAD | Count of upward revisions among analysts included in the consensus |
| 2 | `anl9_sdetail_effectivetime` | VECTOR | 0.442 | 其他 | 2 | 0.24 | 0.73 | 0.32 | DEAD | The time of calculation |
| 3 | `eps_consensus_estimate_value` | VECTOR | 0.565 | 修正与预期 | 1 | 0.17 | 0.55 | 0.24 | DEAD | Lookup index identifying the consensus category/type for the estimate |
| 4 | `anl9_consensusanalysis_dataitemvalue` | VECTOR | 0.559 | 修正与预期 | 2 | 0.17 | 1.27 | 0.45 | DEAD | Numeric consensus estimate value for the specified data item |
| 5 | `anl9_daily_numupunfiltered` | VECTOR | 0.553 | 修正与预期 | 1 | 0.08 | 0.54 | 0.43 | DEAD | Total number of analysts whose estimates were revised upward, including those excluded from the consensus |
| 6 | `anl9_sconsensusv2span_incomenetincome_dataitemvalue` | VECTOR | 0.750 | 修正与预期 | 2 | -0.32 | 0.66 | -0.08 | DEAD | Value of the DataItem |
| 7 | `anl9_recommendationbrokeroptioncode` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | [di][recommendationScaleId] = Recommendation code received from the contributing broker |
| 8 | `anl9_scaleconversionflag` | MATRIX | 0.974 | 其他 | 0 | — | — | — | UNTESTED | [di][idx of dataItemIx] |
| 9 | `base_currency_conversion_indicator` | MATRIX | 0.974 | 宏观与行业 | 0 | — | — | — | UNTESTED | Flag indicating currency conversion capability |
| 10 | `anl9_recommendationnumericvalue` | MATRIX | 0.971 | 修正与预期 | 0 | — | — | — | UNTESTED | Standardized S&P Capital IQ broker recommendation on a 1–5 scale (6 = Not Available) |
| 11 | `anl9_estanalystmap` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Human-readable name/description of the analyst corresponding to estimateAnalystIx |
| 12 | `anl9_sconsensusv2span_incomeothers_dataitemvalue` | VECTOR | 0.816 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 13 | `anl9_sconsensusv2span_incomeeps_dataitemvalue` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 14 | `anl9_sconsensusv2span_incomeothers_splitfactor` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Split factor |
| 15 | `anl9_sconsensusv2span_incomeebt_dataitemvalue` | VECTOR | 0.801 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 16 | `anl9_sconsensusv2span_others_dataitemvalue` | VECTOR | 0.796 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 17 | `anl9_sconsensusv2span_incomeothers_effectivetime` | VECTOR | 0.790 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 18 | `anl9_sconsensusv2span_incomeothers_totime` | VECTOR | 0.788 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 19 | `anl9_sconsensusv2span_balancesheet_dataitemvalue` | VECTOR | 0.788 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 20 | `anl9_sconsensusv2span_incomeeps_effectivetime` | VECTOR | 0.786 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 21 | `anl9_sconsensusv2span_incomeeps_totime` | VECTOR | 0.784 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 22 | `anl9_sconsensusv2span_balancesheet_splitfactor` | VECTOR | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Split factor |
| 23 | `anl9_sconsensusv2span_others_totime` | VECTOR | 0.779 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 24 | `anl9_sconsensusv2span_others_splitfactor` | VECTOR | 0.778 | 修正与预期 | 0 | — | — | — | UNTESTED | Split factor |
| 25 | `anl9_sconsensusv2span_incomeebt_effectivetime` | VECTOR | 0.772 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 26 | `anl9_sconsensusv2span_others_effectivetime` | VECTOR | 0.769 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 27 | `anl9_sconsensusv2span_incomeebt_totime` | VECTOR | 0.769 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 28 | `anl9_sconsensusv2span_balancesheet_effectivetime` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 29 | `anl9_sconsensusv2span_balancesheet_totime` | VECTOR | 0.742 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 30 | `anl9_sconsensusv2span_incomenetincome_effectivetime` | VECTOR | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 31 | `anl9_sconsensusv2span_incomenetincome_totime` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 32 | `anl9_sconsensusv2span_cashflowstatement_dataitemvalue` | VECTOR | 0.729 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 33 | `anl9_sconsensusanalysis_dataitemvalue` | VECTOR | 0.716 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the DataItem |
| 34 | `anl9_sconsensusv2span_incomeebt_splitfactor` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Split factor |
| 35 | `anl9_sconsensusv2span_cashflowstatement_splitfactor` | VECTOR | 0.712 | 修正与预期 | 0 | — | — | — | UNTESTED | Split factor |
| 36 | `anl9_sconsensusv2span_cashflowstatement_effectivetime` | VECTOR | 0.699 | 修正与预期 | 0 | — | — | — | UNTESTED | The time of calculation |
| 37 | `anl9_sconsensusv2span_cashflowstatement_totime` | VECTOR | 0.689 | 修正与预期 | 0 | — | — | — | UNTESTED | The time an estimate ends |
| 38 | `anl9_sconsensusv2span_incomenetincome_splitfactor` | VECTOR | 0.654 | 修正与预期 | 0 | — | — | — | UNTESTED | Split factor |
| 39 | `anl9_revisions_effectivetime` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Time when the revision snapshot/estimate was calculated |
| 40 | `anl9_s_numanalystall` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Total number of contributing analysts, including those excluded from the consensus |
| 41 | `anl9_s_numanalysts` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts whose estimates are included in the consensus for the revision period |
| 42 | `anl9_s_numdn` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of downward revisions included in the consensus during the specified revision period |
| 43 | `anl9_s_numdownunfiltered` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Total analysts with downward revisions, including those excluded from the consensus |
| 44 | `anl9_s_numnochangeunfiltered` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Total number of no-change revisions, without exclusions |
| 45 | `anl9_s_numnochg` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of revisions with no change in the consensus (included analysts) over the period |
| 46 | `anl9_s_numup` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of upward revisions included in the consensus during the specified revision period |
| 47 | `anl9_s_numupunfiltered` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Total analysts with upward revisions, including those excluded from the consensus |
| 48 | `revision_consensus_value_revisions` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer code identifying the consensus estimate category for the metric/period, joinable to a consensus lookup |
| 49 | `anl9_consensusv2span_dataitemvalue` | VECTOR | 0.587 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the estimated metric |
| 50 | `anl9_consensusv2span_effectivetime` | VECTOR | 0.587 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intraday time when the consensus estimate became effective/was calculated (start time of the span) |
| 51 | `anl9_consensusv2span_splitfactor` | VECTOR | 0.587 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjustment factor for corporate actions (e.g., stock splits) to maintain comparability of values |
| 52 | `anl9_consensusv2span_totime` | VECTOR | 0.587 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intraday time when the estimate’s validity period ends |
| 53 | `span_consensus_estimate_value` | VECTOR | 0.587 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus value for estimates in the span module. |
| 54 | `anl9_consensusv2span_incomeothers_dataitemvalue` | VECTOR | 0.578 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric consensus estimate value for the specified data item |
| 55 | `anl9_consensusv2span_incomeothers_effectivetime` | VECTOR | 0.578 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intra-day time when the consensus estimate became effective (time of calculation) |
| 56 | `anl9_consensusv2span_incomeothers_splitfactor` | VECTOR | 0.578 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjustment factor for corporate actions (e.g., stock splits) applied to maintain comparability of estimates |
| 57 | `anl9_consensusv2span_incomeothers_totime` | VECTOR | 0.578 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intra-day time when the estimate’s validity period ends |
| 58 | `income_other_consensus_value` | VECTOR | 0.578 | 修正与预期 | 0 | — | — | — | UNUSABLE | <baseModule>.ConsensusIdIx idx |
| 59 | `anl9_confirmtime` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intraday time of the most recent confirmation of the current estimate |
| 60 | `anl9_detail_dataitemvalue` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the estimated metric |
| 61 | `anl9_detail_effectivetime` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Time of day when the estimate became effective (start time of validity) |
| 62 | `anl9_detail_totime` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | End time of the estimate’s validity period (intraday) |
| 63 | `anl9_estimatetime` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intra-day time at which the estimate was recorded/issued |
| 64 | `anl9_isexcluded` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating the estimate is excluded from consensus/analysis due to data quality rules |
| 65 | `anl9_parentflag` | VECTOR | 0.571 | 修正与预期 | 0 | — | — | — | UNUSABLE | Entity consolidation flag: 0=consolidated entity estimate, 1=parent-only entity estimate |
| 66 | `anl9_consensusv2span_incomeebt_dataitemvalue` | VECTOR | 0.570 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimate value for the specified metric (Income before taxes/EBT) |
| 67 | `anl9_consensusv2span_incomeebt_effectivetime` | VECTOR | 0.570 | 修正与预期 | 0 | — | — | — | UNUSABLE | Start time-of-day when this consensus Income Before Taxes (EBT) estimate became effective |
| 68 | `anl9_consensusv2span_incomeebt_splitfactor` | VECTOR | 0.570 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjustment factor for corporate actions (e.g., stock splits) applied to maintain estimate comparability |
| 69 | `anl9_consensusv2span_incomeebt_totime` | VECTOR | 0.570 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intraday time when the consensus estimate record stops being effective (end of the validity window) |
| 70 | `ebt_consensus_estimate_value` | VECTOR | 0.570 | 修正与预期 | 0 | — | — | — | UNUSABLE | <baseModule>.ConsensusIdIx idx |
| 71 | `anl9_consensusv2span_incomeeps_dataitemvalue` | VECTOR | 0.565 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric consensus estimate value for the specified data item |
| 72 | `anl9_consensusv2span_incomeeps_effectivetime` | VECTOR | 0.565 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intra-day time when the estimate becomes effective or is calculated |
| 73 | `anl9_consensusv2span_incomeeps_splitfactor` | VECTOR | 0.565 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio used to unadjust per-share EPS estimates for stock splits that occur after the estimate’s EffectiveDate |
| 74 | `anl9_consensusv2span_incomeeps_totime` | VECTOR | 0.565 | 修正与预期 | 0 | — | — | — | UNUSABLE | End time when the estimate’s validity window ends |
| 75 | `anl9_consensusanalysis_effectivetime` | VECTOR | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intra-day time when the consensus estimate calculation became effective |
| 76 | `anl9_isnmflag` | VECTOR | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating the estimate is not meaningful (NM) |
| 77 | `consensus_analysis_value` | VECTOR | 0.559 | 修正与预期 | 0 | — | — | — | UNUSABLE | <baseModule>.ConsensusIdIx idx |
| 78 | `anl9_consensusv2span_incomenetincome_dataitemvalue` | VECTOR | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the consensus net income estimate |
| 79 | `anl9_consensusv2span_incomenetincome_effectivetime` | VECTOR | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | Start time (intra-day) when the consensus estimate span becomes valid |
| 80 | `anl9_consensusv2span_incomenetincome_splitfactor` | VECTOR | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio used to unadjust per-share data for stock splits that occur after the estimate’s EffectiveDate |
| 81 | `anl9_consensusv2span_incomenetincome_totime` | VECTOR | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intra-day time marking when the estimate’s validity period ends |
| 82 | `net_income_consensus_value` | VECTOR | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | Index identifier for the consensus estimate category from the base module’s ConsensusId lookup |
| 83 | `anl9_consensusv2span_balancesheet_dataitemvalue` | VECTOR | 0.556 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the balance sheet data item consensus estimate in the specified currency and scale |
| 84 | `anl9_consensusv2span_balancesheet_effectivetime` | VECTOR | 0.556 | 修正与预期 | 0 | — | — | — | UNUSABLE | The time of calculation |
| 85 | `anl9_consensusv2span_balancesheet_splitfactor` | VECTOR | 0.556 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjustment factor applied to account for corporate actions (e.g., stock splits) to keep estimates comparable |
| 86 | `anl9_consensusv2span_balancesheet_totime` | VECTOR | 0.556 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intraday time when the estimate ceased to be effective |
| 87 | `balancesheet_consensus_value` | VECTOR | 0.556 | 修正与预期 | 0 | — | — | — | UNUSABLE | Integer index referencing the consensus category in the module’s consensus lookup table |
| 88 | `anl9_daily_numanalystall` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts contributing estimates for the company, including those excluded from the consensus |
| 89 | `anl9_daily_numanalysts` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts whose estimates are included in the consensus for the revision period |
| 90 | `anl9_daily_numdn` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of downward revisions among analysts included in the consensus |
| 91 | `anl9_daily_numdownunfiltered` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts whose estimates were revised downward, including those excluded from the consensus |
| 92 | `anl9_daily_numnochangeunfiltered` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts that did not change their estimates, including those excluded from the consensus |
| 93 | `anl9_daily_numnochg` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of revisions with no change among analysts included in the consensus |
| 94 | `anl9_revisiondaily_effectivetime` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Time when the revision metrics were calculated or became effective |
| 95 | `revision_consensus_value` | VECTOR | 0.553 | 修正与预期 | 0 | — | — | — | UNUSABLE | Index key referencing the consensus estimate category in the ConsensusId lookup |
| 96 | `anl9_consensusv2span_others_dataitemvalue` | VECTOR | 0.539 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the estimate for the specified data item |
| 97 | `anl9_consensusv2span_others_effectivetime` | VECTOR | 0.539 | 修正与预期 | 0 | — | — | — | UNUSABLE | Time of day when the estimate/calculation became effective or was calculated |
| 98 | `anl9_consensusv2span_others_splitfactor` | VECTOR | 0.539 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio used to unadjust per-share estimates for stock splits occurring after the estimate’s EffectiveDate |
| 99 | `anl9_consensusv2span_others_totime` | VECTOR | 0.539 | 修正与预期 | 0 | — | — | — | UNUSABLE | Time of day when the estimate’s validity ended |
| 100 | `other_metric_consensus_value` | VECTOR | 0.539 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus value for other financial metric estimates. |
| 101 | `anl9_consensusv2span_cashflowstatement_dataitemvalue` | VECTOR | 0.536 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric consensus estimate value for the specified data item |
| 102 | `anl9_consensusv2span_cashflowstatement_effectivetime` | VECTOR | 0.536 | 修正与预期 | 0 | — | — | — | UNUSABLE | Start/effective time when the estimate became valid or was calculated |
| 103 | `anl9_consensusv2span_cashflowstatement_splitfactor` | VECTOR | 0.536 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjustment factor for corporate actions such as stock splits applied to normalize estimates |
| 104 | `anl9_consensusv2span_cashflowstatement_totime` | VECTOR | 0.536 | 修正与预期 | 0 | — | — | — | UNUSABLE | End time of the estimate's validity window |
| 105 | `cashflow_consensus_estimate_value` | VECTOR | 0.536 | 修正与预期 | 0 | — | — | — | UNUSABLE | Integer index identifying the consensus estimate category or type, joinable to ConsensusIdIx |
| 106 | `anl9_sdetail_dataitemvalue` | VECTOR | 0.458 | 其他 | 0 | — | — | — | UNUSABLE | Value of the DataItem |
| 107 | `anl9_sdetail_totime` | VECTOR | 0.435 | 修正与预期 | 0 | — | — | — | UNUSABLE | The time an estimate ends |
| 108 | `anl9_guidancev2span_dataitemvalue` | VECTOR | 0.219 | 修正与预期 | 0 | — | — | — | UNUSABLE | Numeric value of the estimate/guidance for the specified data item |
| 109 | `anl9_guidancev2span_effectivetime` | VECTOR | 0.219 | 修正与预期 | 0 | — | — | — | UNUSABLE | Intraday start time when the guidance estimate becomes effective |
| 110 | `anl9_guidancev2span_splitfactor` | VECTOR | 0.219 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjustment factor applied to estimate values for corporate actions such as stock splits |
| 111 | `guidance_consensus_value` | VECTOR | 0.219 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus value for company guidance estimates. |

## 六、本地回测证据

- 本地累计回测 **27** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `9qWqEoJe` | 1.01 | 0.69 | 0.30 | 0.75 | 0.12 | ["LOW_SHARPE | 261 | `divide(subtract(ts_backfill(vec_sum(anl9_daily_numup),5), ts_backfill(vec_sum(anl9_daily_n` |
| `XgbnZ6oX` | 0.82 | 0.59 | 1.63 | 0.47 | 0.07 | ["LOW_SHARPE | 213 | `divide(subtract(ts_backfill(vec_sum(anl9_daily_numup),5), ts_backfill(vec_sum(anl9_daily_n` |
| `WjejL1QG` | 0.40 | 0.26 | 0.76 | 0.13 | 0.10 | ["LOW_SHARPE | 261 | `divide(subtract(ts_backfill(quantity_institutional_shares_acquired,66), ts_backfill(market` |
| `rKeKdAN3` | 0.40 | 0.14 | 0.50 | 0.41 | 0.08 | ["LOW_SHARPE | 261 | `divide(ts_av_diff(ts_sum(subtract(avg_buy_shares,avg_sell_shares),22), 252), add(ts_std_de` |
| `ZYAYmP3x` | 0.39 | 0.24 | 0.65 | 0.01 | 0.13 | ["LOW_SHARPE | 261 | `divide(subtract(ts_backfill(quantity_institutional_shares_acquired,66), ts_backfill(quanti` |
| `88P8vAzo` | 0.36 | 0.12 | -0.12 | 0.40 | 0.02 | ["LOW_SHARPE | 261 | `divide(divide(ts_sum(avg_secondary_top_buy_shares,126), add(ts_sum(avg_top_buy_shares,126)` |
| `LLZL5k8v` | 0.34 | 0.11 | -0.40 | 0.38 | 0.03 | ["LOW_SHARPE | 261 | `divide(divide(ts_sum(avg_secondary_top_buy_shares,126), add(ts_sum(total_secondary_top_buy` |
| `7868oJvv` | 0.33 | 0.10 | 0.48 | 0.35 | 0.08 | ["LOW_SHARPE | 261 | `divide(ts_av_diff(ts_sum(subtract(avg_buy_shares,avg_secondary_sell_shares),22), 252), add` |
| `XgJgRmra` | 0.29 | 0.13 | 0.10 | 0.37 | 0.01 | ["LOW_SHARPE | 261 | `divide(aggregate_equity_value_all_owners, aggregate_share_count_all_owners)` |
| `blOl8pvM` | 0.24 | 0.07 | -0.27 | -0.02 | 0.38 | ["LOW_SHARPE | 261 | `group_count(vec_avg(anl9_sdetail_effectivetime), sector)` |
| `j2A0kmrE` | 0.19 | 0.08 | 0.73 | 0.32 | 0.19 | ["LOW_SHARPE | 213 | `group_count(vec_avg(anl9_sdetail_effectivetime), sector)` |
| `6Xj96Oe5` | 0.17 | 0.07 | 0.55 | 0.24 | 0.07 | ["LOW_SHARPE | 213 | `divide(subtract(ts_backfill(vec_avg(eps_consensus_estimate_value),22), ts_delay(ts_backfil` |
| `gJbMNp8l` | 0.17 | 0.07 | 1.27 | 0.45 | 0.07 | ["LOW_SHARPE | 213 | `divide(ts_delta(ts_backfill(vec_avg(anl9_consensusanalysis_dataitemvalue), 22), 22), add(d` |
| `d5b0JLRE` | 0.08 | 0.03 | 0.54 | 0.43 | 0.16 | ["LOW_SHARPE | 213 | `divide(add(vec_sum(anl9_daily_numupunfiltered), vec_sum(anl9_daily_numdownunfiltered)), ad` |
| `P0g0Mvz7` | 0.08 | 0.01 | 1.38 | 0.03 | 0.02 | ["LOW_SHARPE | 261 | `days_from_last_change(sign(subtract(market_value_institutional_shares_acquired, market_val` |

## 七、判死记录（sealed dead_end）

- `EUR-ANALYST9-COLD-ZERO-YIELD`（2026-09-22）family=一致预期修正标准化劾量 / 预期陈旧度 / 修正广度：{"dataset": "analyst9", "evidence": {"alpha_count": 76, "best_alpha": "XgbnZ6oX", "best_sharpe": 0.82, "two_year_sharpe_of_best": 1.63}, "failure_mode": "LOW_SHARPE + LOW_FITNESS + LOW_ROBUST_UNIVERSE_SHARPE（1/7 除首条外全加 CONCENTRATED_WEIGHT）", "mechanism": "一致预期修正标准化劾量 / 预期陈旧度 days_from_last_change / 修正广度 numup÷numdn", "note": "未调 seal_dead_end：本波 candidates=0，salvage 沉降无有效残值", "rule": "本区该集不再投槽位；同机

