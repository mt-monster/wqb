# model30 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model30` |
| 名称 | EPS Estimate Model |
| 类别 | MODEL |
| 数据字段数(平台) | 77 |
| 覆盖率 | 0.713 |
| 平台已有 alpha | 257 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides detailed metrics on analyst earnings estimate revisions, including proprietary weighted forecasts, predicted surprises, and consensus estimates. It captures the frequency, direction, and magnitude of analyst revisions, as well as the accuracy of individual analysts. By tracking changes in earnings expectations and identifying clusters of fresh versus stale revisions, the dataset offers valuable insights into market sentiment and potential price movements. Investors and quantitative researchers can leverage these signals to anticipate earnings surprises and identify stocks likely to outperform or underperform, making it a powerful tool for forecasting short-term and medium-term price trends.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **77** |
| 类型分布 | MATRIX×73　SYMBOL×4 |
| 平均覆盖率 | **0.713** |
| 覆盖率区间 | 0.24 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 31 | 40.3% |
| 中 (0.70–0.90) | 22 | 28.6% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 24 | 31.2% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 53 | 68.8% |
| UNUSABLE | 24 | 31.2% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 53 / UNUSABLE 24 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 60 | 0.69 | mdl30_new_numnly_fy1_eps、mdl30_new_numnly_fy2_eps、mdl30_new_smartestimate_f12m_eps |
| 其他 | 17 | 0.81 | mdl30_new_psprise_pct_f12m_eps、mdl30_new_psprise_pct_fy1_eps、star_eps_surprise_prediction_12m |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl30_new_numnly_fy1_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of SmartEstimate Analysts FY1 EPS |
| 2 | `mdl30_new_numnly_fy2_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of SmartEstimate Analysts FY2 EPS |
| 3 | `mdl30_new_smartestimate_f12m_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate F12M EPS |
| 4 | `mdl30_new_smartestimate_fy1_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate FY1 EPS |
| 5 | `mdl30_new_smartestimate_fy2_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate FY2 EPS |
| 6 | `star_eps_analyst_number_fy1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of SmartEstimate Analysts FY1 EPS |
| 7 | `star_eps_analyst_number_fy2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of SmartEstimate Analysts FY2 EPS |
| 8 | `star_eps_smart_estimate_12m` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate F12M EPS |
| 9 | `star_eps_smart_estimate_fy1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate FY1 EPS |
| 10 | `star_eps_smart_estimate_fy2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | SmartEstimate FY2 EPS |
| 11 | `mdl30_new_psprise_pct_f12m_eps` | MATRIX | 0.990 | 其他 | 0 | — | — | — | UNTESTED | Predicted Surprise % F12M EPS |
| 12 | `mdl30_new_psprise_pct_fy1_eps` | MATRIX | 0.990 | 其他 | 0 | — | — | — | UNTESTED | Predicted Surprise % FY1 EPS |
| 13 | `star_eps_surprise_prediction_12m` | MATRIX | 0.990 | 其他 | 0 | — | — | — | UNTESTED | Predicted Surprise % F12M EPS |
| 14 | `star_eps_surprise_prediction_fy1` | MATRIX | 0.990 | 其他 | 0 | — | — | — | UNTESTED | Predicted Surprise % FY1 EPS |
| 15 | `mdl30_new_psprise_pct_fy2_eps` | MATRIX | 0.989 | 其他 | 0 | — | — | — | UNTESTED | Predicted Surprise % FY2 EPS |
| 16 | `star_eps_surprise_prediction_fy2` | MATRIX | 0.989 | 其他 | 0 | — | — | — | UNTESTED | Predicted Surprise % FY2 EPS |
| 17 | `mdl30_parent_flag_d1` | MATRIX | 0.961 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the entity is a parent company where 1 indicates parent and 0 otherwise |
| 18 | `star_eps_analyst_number_fq1_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the SmartEstimate for EPS for fiscal quarter 1 |
| 19 | `star_eps_analyst_number_fq2_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the SmartEstimate for EPS for fiscal quarter 2 |
| 20 | `star_eps_analyst_number_fy1_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the SmartEstimate for EPS for fiscal year 1 |
| 21 | `star_eps_analyst_number_fy2_d1` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the SmartEstimate for EPS for fiscal year 2 |
| 22 | `d1_fy1_period_end_date` | SYMBOL | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Period end date for first fiscal year in d1 module. |
| 23 | `d1_fy2_period_end_date` | SYMBOL | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Period end date for second fiscal year in d1 module. |
| 24 | `star_eps_smart_estimate_fy1_d1` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of EPS for fiscal year 1 |
| 25 | `star_eps_surprise_prediction_fy1_d1` | MATRIX | 0.951 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the SmartEstimate and the consensus mean for EPS for fiscal year 1 |
| 26 | `star_eps_smart_estimate_fy2_d1` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of EPS for fiscal year 2 |
| 27 | `star_eps_surprise_prediction_fy2_d1` | MATRIX | 0.950 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the SmartEstimate and the consensus mean for EPS for fiscal year 2 |
| 28 | `star_eps_smart_estimate_12m_d1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate of EPS for the forward 12 months |
| 29 | `star_eps_surprise_prediction_12m_d1` | MATRIX | 0.949 | 修正与预期 | 0 | — | — | — | UNTESTED | Percentage difference between the SmartEstimate and the consensus mean for EPS for the forward 12 months |
| 30 | `d1_fq1_period_end_date` | SYMBOL | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Period end date for first fiscal quarter in d1 module. |
| 31 | `d1_fq2_period_end_date` | SYMBOL | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Period end date for second fiscal quarter in d1 module. |
| 32 | `is_parent_company_flag` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Indicator whether the entity is a parent company (1 = parent, 0 = otherwise) |
| 33 | `mdl30_numnly_fq1_eps` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Quarter 1 |
| 34 | `mdl30_numnly_fq2_eps` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Quarter 2 |
| 35 | `mdl30_numnly_fy1_eps` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Year 1 |
| 36 | `mdl30_numnly_fy2_eps` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Year 2 |
| 37 | `parent_company_indicator` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Indicator if the entity is a parent company (1 parent, 0 otherwise) |
| 38 | `star_new_eps_analyst_number_fq1` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Quarter 1 |
| 39 | `star_new_eps_analyst_number_fq2` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Quarter 2 |
| 40 | `star_new_eps_analyst_number_fy1` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Year 1 |
| 41 | `star_new_eps_analyst_number_fy2` | MATRIX | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts included in the StarMine SmartEstimate for EPS for Fiscal Year 2 |
| 42 | `mdl30_psprise_pct_fy1_eps` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percent surprise in EPS for Fiscal Year 1 (SmartEstimate versus consensus mean) |
| 43 | `mdl30_smartestimate_fy1_eps` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Year 1 |
| 44 | `star_new_eps_smart_estimate_fy1` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Year 1 |
| 45 | `star_new_eps_surprise_prediction_fy1` | MATRIX | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise percentage for EPS for Fiscal Year 1, as the deviation of SmartEstimate from the consensus mean |
| 46 | `mdl30_psprise_pct_fy2_eps` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percent surprise in EPS for Fiscal Year 2 (SmartEstimate versus consensus mean) |
| 47 | `mdl30_smartestimate_fy2_eps` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Year 2 |
| 48 | `star_new_eps_smart_estimate_fy2` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Year 2 |
| 49 | `star_new_eps_surprise_prediction_fy2` | MATRIX | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise percentage for EPS for Fiscal Year 2, as the deviation of SmartEstimate from the consensus mean |
| 50 | `mdl30_psprise_pct_f12m_eps` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted percent surprise in EPS for forward 12 months (SmartEstimate versus consensus mean) |
| 51 | `mdl30_smartestimate_f12m_eps` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (analyst-weighted) EPS forecast for Forward 12 Months |
| 52 | `star_new_eps_smart_estimate_12m` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartEstimate (analyst-weighted) EPS forecast for the forward 12 months |
| 53 | `star_new_eps_surprise_prediction_12m` | MATRIX | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted surprise percentage for EPS over the forward 12 months, as the deviation of SmartEstimate from the consensus mean |
| 54 | `mdl30_new_psprise_pct_fq1_eps` | MATRIX | 0.418 | 其他 | 0 | — | — | — | UNUSABLE | Predicted Surprise % FQ1 EPS |
| 55 | `star_eps_surprise_prediction_fq1` | MATRIX | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Predicted Surprise % FQ1 EPS |
| 56 | `mdl30_new_numnly_fq1_eps` | MATRIX | 0.417 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of SmartEstimate Analysts FQ1 EPS |
| 57 | `mdl30_new_smartestimate_fq1_eps` | MATRIX | 0.417 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate FQ1 EPS |
| 58 | `star_eps_analyst_number_fq1` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of SmartEstimate Analysts FQ1 EPS |
| 59 | `star_eps_smart_estimate_fq1` | MATRIX | 0.416 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate FQ1 EPS |
| 60 | `star_eps_smart_estimate_fq1_d1` | MATRIX | 0.406 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate of EPS for fiscal quarter 1 |
| 61 | `star_eps_surprise_prediction_fq1_d1` | MATRIX | 0.406 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage difference between the SmartEstimate and the consensus mean for EPS for fiscal quarter 1 |
| 62 | `star_eps_surprise_prediction_fq2` | MATRIX | 0.375 | 其他 | 0 | — | — | — | UNUSABLE | Predicted Surprise % FQ2 EPS |
| 63 | `star_eps_analyst_number_fq2` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of SmartEstimate Analysts FQ2 EPS |
| 64 | `star_eps_smart_estimate_fq2` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate FQ2 EPS |
| 65 | `mdl30_new_psprise_pct_fq2_eps` | MATRIX | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Predicted Surprise % FQ2 EPS |
| 66 | `star_eps_smart_estimate_fq2_d1` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate of EPS for fiscal quarter 2 |
| 67 | `star_eps_surprise_prediction_fq2_d1` | MATRIX | 0.370 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage difference between the SmartEstimate and the consensus mean for EPS for fiscal quarter 2 |
| 68 | `mdl30_new_numnly_fq2_eps` | MATRIX | 0.369 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of SmartEstimate Analysts FQ2 EPS |
| 69 | `mdl30_new_smartestimate_fq2_eps` | MATRIX | 0.369 | 修正与预期 | 0 | — | — | — | UNUSABLE | SmartEstimate FQ2 EPS |
| 70 | `mdl30_psprise_pct_fq1_eps` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted percent surprise in EPS for Fiscal Quarter 1 (SmartEstimate versus consensus mean) |
| 71 | `mdl30_smartestimate_fq1_eps` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Quarter 1 |
| 72 | `star_new_eps_smart_estimate_fq1` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Quarter 1 |
| 73 | `star_new_eps_surprise_prediction_fq1` | MATRIX | 0.269 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise percentage for EPS for Fiscal Quarter 1, as the deviation of SmartEstimate from the consensus mean |
| 74 | `mdl30_psprise_pct_fq2_eps` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted percent surprise in EPS for Fiscal Quarter 2 (SmartEstimate versus consensus mean) |
| 75 | `mdl30_smartestimate_fq2_eps` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Quarter 2 |
| 76 | `star_new_eps_smart_estimate_fq2` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | StarMine SmartEstimate (analyst-weighted) EPS forecast for Fiscal Quarter 2 |
| 77 | `star_new_eps_surprise_prediction_fq2` | MATRIX | 0.242 | 修正与预期 | 0 | — | — | — | UNUSABLE | Predicted surprise percentage for EPS for Fiscal Quarter 2, as the deviation of SmartEstimate from the consensus mean |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-ANALYST10-PREDICTED-SURPRISE-DEAD`（2026-09-19）family=analyst10 performance-weighted estimates (predicted surprise EBT/net/pretax/sales, innovation counts, revision ratio)：{"id": "EUR-ANALYST10-PREDICTED-SURPRISE-DEAD", "dataset": "analyst10", "wave": 209, "universe": "TOPCS1600", "evidence": "8 probes /S/<=0.64: net FY1 pred surprise 0.64 (2Y 0.17), sales 0.58, innovation counts 0.55, EBT pred surprise 0.49 (2Y -0.14), revision/close 0.31, pretax 0.29", "verdict": "SmartEstimate-style predicted surprise has no EUR signal at D1 (unlike ASI model30 3.28); analyst tow

