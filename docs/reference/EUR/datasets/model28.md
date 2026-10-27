# model28 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model28` |
| 名称 | Structural Credit Risk Model |
| 类别 | MODEL |
| 数据字段数(平台) | 83 |
| 覆盖率 | 0.8708 |
| 平台已有 alpha | 104 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Refinitiv Identification Codes (RIC) for financial securities. It enables users to cross-reference and integrate data from Bloomberg and Refinitiv platforms, facilitating seamless data aggregation, reconciliation, and analysis across systems. While not directly predictive of price movements, accurate identifier mapping is essential for linking datasets, ensuring data integrity, and supporting multi-source quantitative research, portfolio management, and risk analysis workflows.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **83** |
| 类型分布 | MATRIX×83 |
| 平均覆盖率 | **0.871** |
| 覆盖率区间 | 0.75 ~ 0.97 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 57 | 68.7% |
| 中 (0.70–0.90) | 26 | 31.3% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 83 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 41 | 0.87 | star_cr_leverage、default_risk_country_percentile_d1、default_risk_region_percentile_d1 |
| 盈利与财务 | 17 | 0.85 | star_cr_asset_drift_pct、star_cr_asset_volatility_pct、star_cr_pd_pct |
| 修正与预期 | 15 | 0.89 | star_cr_implied_rating、model_based_letter_grade_d1、star_cr_dist_to_default |
| 风险与质量 | 10 | 0.87 | default_risk_global_percentile_d1、star_cr_global_rank、mdl28_sm_structural_multiple_credit_structural_global_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `star_cr_implied_rating` | MATRIX | 0.970 | 修正与预期 | 0 | — | — | — | UNTESTED | Agency.equivalent credit rating implied by the current estimated forward 1.year SCR default probability.,,, |
| 2 | `star_cr_leverage` | MATRIX | 0.941 | 宏观与行业 | 0 | — | — | — | UNTESTED | The current 1-100 percentile rank, among other firms in the same region and industry, of a company's 1.year default prob |
| 3 | `star_cr_asset_drift_pct` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-100 rank of the annualized rate of change of the market value of the firm’s assets |
| 4 | `star_cr_asset_volatility_pct` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | annualized volatility of the market value of the firm’s assets |
| 5 | `default_risk_country_percentile_d1` | MATRIX | 0.930 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same country (d1 version). |
| 6 | `default_risk_global_percentile_d1` | MATRIX | 0.930 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood compared to all companies worldwide (d1 version). |
| 7 | `default_risk_region_percentile_d1` | MATRIX | 0.930 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same geographic region (d1 version). |
| 8 | `model_based_letter_grade_d1` | MATRIX | 0.930 | 修正与预期 | 0 | — | — | — | UNTESTED | Agency-style rating derived from model-estimated default probability (d1 version). |
| 9 | `star_cr_country_rank` | MATRIX | 0.930 | 宏观与行业 | 0 | — | — | — | UNTESTED | "The current 1-100 percentile rank, by country, of a company's 1.year default probability based on the Structural Compon |
| 10 | `star_cr_dist_to_default` | MATRIX | 0.930 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of standard deviations difference between the market value of the firm's assets and its estimated default point., |
| 11 | `star_cr_global_rank` | MATRIX | 0.930 | 风险与质量 | 0 | — | — | — | UNTESTED | "The current global 1-100 percentile rank of a company's 1-year default probability based on the Structural Component of |
| 12 | `star_cr_pd_pct` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | A percentage that indicates the probability,that the company will go bankrupt, or default on its debt obligations, over |
| 13 | `star_cr_region_rank` | MATRIX | 0.930 | 宏观与行业 | 0 | — | — | — | UNTESTED | "The current 1-100 percentile rank, among other firms in the same region, of a company's 1.year default probability base |
| 14 | `default_risk_sector_percentile_d1` | MATRIX | 0.929 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same economic sector (d1 version). |
| 15 | `star_cr_sector_rank` | MATRIX | 0.929 | 宏观与行业 | 0 | — | — | — | UNTESTED | "The current 1-100 percentile rank, among other firms in the same region and industrial sector, of a company's 1.year de |
| 16 | `mdl28_sm_structural_multiple_credit_structural_leverage` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of the default point to the market value of the firm's assets, lower values indicate lower default risk |
| 17 | `mdl28_sm_structural_nd__credit_structural_leverage` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of default point (liability threshold) to estimated asset value, measuring financial leverage and risk |
| 18 | `mdl28_sm_structural__credit_structural_leverage` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of the estimated default threshold to the firm's asset value, representing financial leverage; higher means more r |
| 19 | `default_risk_industry_percentile_d1` | MATRIX | 0.924 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same industry group (d1 version). |
| 20 | `star_cr_industry_rank` | MATRIX | 0.924 | 宏观与行业 | 0 | — | — | — | UNTESTED | "The current 1-100 percentile rank, among other firms in the same region and industry, of a company's 1.year default pro |
| 21 | `mdl28_sm_structural_multiple_credit_structural_asset_volatility_percent` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Annualized asset value volatility percentage as estimated by the structural credit risk model |
| 22 | `mdl28_sm_structural_nd_credit_structural_asset_drift_pct` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected annualized percent change in company asset value, reflecting asset growth or contraction |
| 23 | `mdl28_sm_structural_nd_credit_structural_asset_volatility_pct` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized volatility of company asset value in percent |
| 24 | `mdl28_sm_structural_multiple_credit_structural_asset_drift_percent` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected annualized percent change (drift) in asset value under the structural credit risk model |
| 25 | `mdl28_sm_structural_credit_structural_asset_drift_pct` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized rate of change (percentage drift) in the market value of the firm’s assets |
| 26 | `mdl28_sm_structural_credit_structural_asset_volatility_pct` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized volatility (percentage) of the market value of the firm’s assets |
| 27 | `mdl28_sm_structural_multiple_credit_structural_country_rank` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the firm's default probability among companies in the same country, higher value means lower |
| 28 | `mdl28_sm_structural_multiple_credit_structural_distance_to_default` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of standard deviations between the market value of the firm's assets and its estimated default point |
| 29 | `mdl28_sm_structural_multiple_credit_structural_global_rank` | MATRIX | 0.917 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank (1-100) of firm's default probability among all companies worldwide, higher means lower risk |
| 30 | `mdl28_sm_structural_multiple_credit_structural_pd_percent` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated forward 1-year probability of default, expressed as a percentage, from StarMine model |
| 31 | `mdl28_sm_structural_multiple_credit_structural_region_rank` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of firm's default probability among companies in the same region, higher means lower risk |
| 32 | `mdl28_sm_structural_nd_credit_structural_country_rank` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1-100 percentile rank of the firm's 1-year default probability within its country; higher scores indicate lower |
| 33 | `mdl28_sm_structural_nd_credit_structural_country_rank_float` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-specific percentile rank (float, 1-100) of 1-year default probability |
| 34 | `mdl28_sm_structural_nd_credit_structural_distance_to_default` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of standard deviations that the company’s estimated asset value exceeds the default threshold according to the st |
| 35 | `mdl28_sm_structural_nd_credit_structural_global_rank` | MATRIX | 0.917 | 风险与质量 | 0 | — | — | — | UNTESTED | Current global 1-100 percentile rank of the firm's 1-year default probability; higher rank means less likely to default |
| 36 | `mdl28_sm_structural_nd_credit_structural_global_rank_float` | MATRIX | 0.917 | 风险与质量 | 0 | — | — | — | UNTESTED | Global percentile rank (float, 1-100) of 1-year default probability; higher means lower risk |
| 37 | `mdl28_sm_structural_nd_credit_structural_pd_pct` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated 12-month forward probability of default for the firm, expressed as a percentage (0–100%), higher means greater |
| 38 | `mdl28_sm_structural_nd_credit_structural_region_rank` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1-100 percentile rank for the firm's 1-year default probability among regional peers; a higher rank means lower |
| 39 | `mdl28_sm_structural_nd_credit_structural_region_rank_float` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Region-specific percentile rank (float, 1-100) of 1-year default probability |
| 40 | `mdl28_sm_structural_credit_structural_country_rank` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of a company's 1-year default probability within the country; higher scores indicate lower risk |
| 41 | `mdl28_sm_structural_credit_structural_country_rank_float` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100, floating-point) of a company's 1-year default probability within the same country; higher means |
| 42 | `mdl28_sm_structural_credit_structural_distance_to_default` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of standard deviations by which the firm's estimated asset value exceeds the default threshold; higher numbers me |
| 43 | `mdl28_sm_structural_credit_structural_global_rank` | MATRIX | 0.917 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of a company's 1-year default probability among all global firms; higher scores mean less risk o |
| 44 | `mdl28_sm_structural_credit_structural_global_rank_float` | MATRIX | 0.917 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (1-100, floating-point) of a company's 1-year default probability among all global firms; higher means l |
| 45 | `mdl28_sm_structural_credit_structural_pd_pct` | MATRIX | 0.917 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated 1-year probability of default expressed as a percentage for the company |
| 46 | `mdl28_sm_structural_credit_structural_region_rank` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of a company's 1-year default probability among firms in the same region; higher values mean low |
| 47 | `mdl28_sm_structural_credit_structural_region_rank_float` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100, floating-point) of a company's 1-year default probability among regional firms; higher means les |
| 48 | `mdl28_sm_structural_multiple_credit_structural_sector_rank` | MATRIX | 0.916 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of firm's default probability among companies in the same sector and region, higher means safer |
| 49 | `mdl28_sm_structural_nd_credit_structural_sector_rank` | MATRIX | 0.916 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1-100 percentile rank of the firm's 1-year default probability within its region and industrial sector; higher s |
| 50 | `mdl28_sm_structural_nd_credit_structural_sector_rank_float` | MATRIX | 0.916 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-specific percentile rank (float, 1-100) of 1-year default probability |
| 51 | `mdl28_sm_structural_credit_structural_sector_rank` | MATRIX | 0.915 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of a company's 1-year default probability among firms in the same region and sector; higher mean |
| 52 | `mdl28_sm_structural_credit_structural_sector_rank_float` | MATRIX | 0.915 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-relative percentile rank (1-100, floating) of 1-year default probability; higher is less risk |
| 53 | `mdl28_sm_structural_multiple_credit_structural_industry_rank_` | MATRIX | 0.911 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of firm's default probability among companies in the same industry group, higher means lower ris |
| 54 | `mdl28_sm_structural_nd_credit_structural_industry_rank` | MATRIX | 0.911 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1-100 percentile rank of the firm's 1-year default probability within its region and industry group; higher scor |
| 55 | `mdl28_sm_structural_nd_credit_structural_industry_rank_float` | MATRIX | 0.911 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-specific percentile rank (float, 1-100) of 1-year default probability |
| 56 | `mdl28_sm_structural_credit_structural_industry_rank` | MATRIX | 0.911 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of a company's 1-year default probability among firms in the same region and industry; higher va |
| 57 | `mdl28_sm_structural_credit_structural_industry_rank_float` | MATRIX | 0.911 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-relative percentile rank (1-100, floating) of 1-year default probability; higher is less risk |
| 58 | `default_threshold_to_asset_ratio` | MATRIX | 0.765 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio comparing the default threshold to total asset value (original version). |
| 59 | `leverage_ratio_to_assets` | MATRIX | 0.765 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio comparing the default threshold to total asset value. |
| 60 | `asset_drift_rate_pct` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized rate of change in asset value used in default modeling (original version). |
| 61 | `annualized_asset_drift_pct` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized rate of change in asset value used in default modeling. |
| 62 | `asset_volatility_annualized_pct` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized volatility of asset value used in default modeling (original version). |
| 63 | `annualized_asset_volatility_pct` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized volatility of asset value used in default modeling. |
| 64 | `country_default_risk_percentile_float` | MATRIX | 0.760 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same country (float version). |
| 65 | `country_default_risk_percentile_v1` | MATRIX | 0.760 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same country (original version). |
| 66 | `default_probability_one_year_pct` | MATRIX | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated probability of default over the next year, expressed as a percent (original version). |
| 67 | `default_risk_global_percentile_v1` | MATRIX | 0.760 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood compared to all companies worldwide (original version). |
| 68 | `distance_to_default_standard_deviation` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of standard deviations between asset value and default threshold (original version). |
| 69 | `global_default_risk_percentile_v1` | MATRIX | 0.760 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood compared to all companies globally (original version). |
| 70 | `model_based_letter_grade_v1` | MATRIX | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Agency-style rating derived from model-estimated default probability (original version). |
| 71 | `region_default_risk_percentile_float` | MATRIX | 0.760 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same region (float version). |
| 72 | `region_default_risk_percentile_v1` | MATRIX | 0.760 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same region (original version). |
| 73 | `country_default_risk_percentile` | MATRIX | 0.760 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same country. |
| 74 | `distance_to_default_stddev` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of standard deviations between asset value and default threshold. |
| 75 | `global_default_risk_percentile` | MATRIX | 0.760 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood compared to all companies globally. |
| 76 | `one_year_default_probability_pct` | MATRIX | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated probability of default over the next year, expressed as a percent. |
| 77 | `region_default_risk_percentile` | MATRIX | 0.760 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same region. |
| 78 | `sector_default_risk_percentile_float` | MATRIX | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same sector (float version). |
| 79 | `sector_default_risk_percentile_v1` | MATRIX | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same sector (original version). |
| 80 | `sector_default_risk_percentile` | MATRIX | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same sector. |
| 81 | `industry_default_risk_percentile_float` | MATRIX | 0.755 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same industry (float version). |
| 82 | `industry_default_risk_percentile_v1` | MATRIX | 0.755 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same industry (original version). |
| 83 | `industry_default_risk_percentile` | MATRIX | 0.755 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank of default likelihood within the same industry. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS38-CONCEPT-WEAK`（2026-08-25）family=news38 densified tone/polarity/relevance concepts：{"dataset": "news38", "id": "EUR-NEWS38-CONCEPT-WEAK", "reason": "Wave64 56 exprs / 7 concept slots (tone invert, pos-neg score/freq, relevance-gated tone, relevance-heat, related_num, analytics-score). Max S0.61 F0.20 (ak7dLe55). Heat slot max S0.53 F0.36. No cheap-gate. Slow-leg /S/<1 so do not mix PV.", "rule": "Leave news38 standalone densify concepts. Do not mix v_rev/wedge. Skip news54 times
- `EUR-STAR-REVCOUNT-ARM-WEAK`（2026-08-25）family=starmine revision counts / ARM rec-activity：{"dataset": "predictive_starmine", "id": "EUR-STAR-REVCOUNT-ARM-WEAK", "reason": "Wave72 56 exprs on unused upgrade/up/down revision counts + ARM recommendations/new-activity. Max S0.97 F0.30 (arm_new_activity_flag_2 ts_delta). Do not mix PV (/S/<1). Leave RelVal EV/EBITDA and revision-breadth.", "rule": "Do not reuse starmine revision counts or ARM rec/activity as slow legs. Do not deepen RelVal 
- `EUR-STAR-REC-SMEST-WEAK`（2026-08-25）family=starmine rec mean change / smest levels：{"dataset": "predictive_starmine", "id": "EUR-STAR-REC-SMEST-WEAK", "reason": "Wave73 rec mean change max S0.90 but 2021-23 Sharpe ~0.15 collapse. smest F12M/FY1 levels max S0.76 TVR often <2%. Last-year surprise ak7d0ZKR S1.04 F0.40 TVR2.1% 2Y=0.95 RN0.38 — /S/>=1 and 2Y not accident; salvage as slow mix leg. Do not deepen rec-change or smest levels. Leave model28 credit.", "rule": "Do not reuse 

