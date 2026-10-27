# other567 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other567` |
| 名称 | Employee Review Data |
| 类别 | OTHER |
| 数据字段数(平台) | 224 |
| 覆盖率 | 0.4665 |
| 平台已有 alpha | 83 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between two major financial security identifiers: RIC (Reuters Instrument Code) and Bloomberg ID. By linking these identifiers, the dataset enables seamless integration and cross-referencing of securities data from different financial data providers. This is particularly useful for analysts and portfolio managers who need to reconcile, aggregate, or validate security-level information across platforms. While not directly predictive of price movements, accurate identifier mapping is essential for ensuring data integrity in multi-source quantitative models, risk management systems, and trading operations.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **224** |
| 类型分布 | VECTOR×224 |
| 平均覆盖率 | **0.467** |
| 覆盖率区间 | 0.23 ~ 0.62 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 134 | 59.8% |
| 稀疏 (<0.50) | 90 | 40.2% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 172 | 76.8% |
| UNTESTED | 52 | 23.2% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 52 / UNUSABLE 172 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 102 | 0.45 | oth567_deltaprimary_city_283、oth567_deltaprimary_sic_279、oth567_deltaprimary_state_296 |
| 风险与质量 | 41 | 0.45 | oth567score_career_advancement_194、oth567score_company_size_174、oth567score_compensation_177 |
| 元数据与非信号 | 22 | 0.60 | oth567_deltaprimary_exchange_300、oth567_deltaprimary_gvkey_282、oth567_deltaprimary_isin_288 |
| 情绪与新闻 | 22 | 0.40 | benefits_perks_sentiment、career_advancement_sentiment_score、company_size_sentiment_score |
| 持仓与资金流 | 11 | 0.48 | oth567_deltaatlas_month_284、oth567atlas_month_210、oth567asm_185 |
| 修正与预期 | 8 | 0.48 | oth567_trend_deltarating_recommend_to_friend_306、oth567_trendrating_recommend_to_friend_222、oth567_individualrating_recommend_to_friend_196 |
| 搜索与替代数据 | 7 | 0.44 | oth567_trend_deltarating_ceo_281、oth567_trendrating_ceo_219、oth567_individualrating_ceo_188 |
| 宏观与行业 | 6 | 0.51 | oth567_deltaprimary_country_298、oth567primary_country_215、oth567country_201 |
| 交易与微观结构 | 5 | 0.61 | oth567_deltaprimary_ticker_301、oth567_trend_deltaticker_305、oth567_trendticker_205 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth567_deltaatlas_month_284` | VECTOR | 0.625 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The month and year of the position (At MCD level we have converted to date so added {dd} to month field |
| 2 | `oth567_deltaprimary_city_283` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | City |
| 3 | `oth567_deltaprimary_country_298` | VECTOR | 0.625 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country |
| 4 | `oth567_deltaprimary_exchange_300` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Exchange Name |
| 5 | `oth567_deltaprimary_gvkey_282` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | gv_key |
| 6 | `oth567_deltaprimary_isin_288` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | ISIN code |
| 7 | `oth567_deltaprimary_naics_278` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Naics Code |
| 8 | `oth567_deltaprimary_sedol_293` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | sedol |
| 9 | `oth567_deltaprimary_sic_279` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | sic |
| 10 | `oth567_deltaprimary_state_296` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | State |
| 11 | `oth567_deltaprimary_ticker_301` | VECTOR | 0.625 | 交易与微观结构 | 0 | — | — | — | UNTESTED | ticker |
| 12 | `oth567_kic_280` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | CIK number |
| 13 | `oth567_primary_cusip_294` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | CUSIP number |
| 14 | `oth567_primary_lei_299` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | LEI code |
| 15 | `oth567_primary_linkedin_url_303` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | Company LinkedIn URL (parent company |
| 16 | `oth567_trend_deltaatlas_unit_name_289` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Atlas unit name |
| 17 | `oth567_trend_deltacompany_292` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Company name |
| 18 | `oth567_trend_deltarating_overall_290` | VECTOR | 0.625 | 其他 | 0 | — | — | — | UNTESTED | overall rating of company (integer values 1 to 5 |
| 19 | `oth567_trend_deltasedol_285` | VECTOR | 0.625 | 元数据与非信号 | 0 | — | — | — | UNTESTED | This refers to the SEDOL |
| 20 | `oth567_trend_deltaticker_305` | VECTOR | 0.625 | 交易与微观结构 | 0 | — | — | — | UNTESTED | This refers to the ticker |
| 21 | `oth567_trend_deltarating_business_outlook_295` | VECTOR | 0.624 | 其他 | 0 | — | — | — | UNTESTED | business outlook rating (positive |
| 22 | `oth567_trend_deltarating_career_opportunities_297` | VECTOR | 0.624 | 其他 | 0 | — | — | — | UNTESTED | rating of career opportunities (1 to 5 |
| 23 | `oth567_trend_deltarating_compensation_and_benefits_307` | VECTOR | 0.624 | 其他 | 0 | — | — | — | UNTESTED | rating of employee compensation and benefits (1 to 5 |
| 24 | `oth567_trend_deltarating_culture_and_values_277` | VECTOR | 0.624 | 其他 | 0 | — | — | — | UNTESTED | rating of company culture and values (integer values 1 to 5 |
| 25 | `oth567_trend_deltarating_recommend_to_friend_306` | VECTOR | 0.624 | 修正与预期 | 0 | — | — | — | UNTESTED | indicates whether reviewer would recommend a friend to the company (positive |
| 26 | `oth567_trend_deltarating_senior_leadership_286` | VECTOR | 0.624 | 其他 | 0 | — | — | — | UNTESTED | rating of senior management (1 to 5 |
| 27 | `oth567_trend_deltarating_work_life_balance_291` | VECTOR | 0.624 | 其他 | 0 | — | — | — | UNTESTED | rating of work-life balance (1 to 5 |
| 28 | `oth567_trend_deltarating_diversity_and_inclusion_304` | VECTOR | 0.619 | 其他 | 0 | — | — | — | UNTESTED | rating of company diversity and inclusion (integer values 1 to 5 |
| 29 | `oth567_trend_deltarating_ceo_281` | VECTOR | 0.607 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | approval rating of the CEO (approve |
| 30 | `oth567_trendatlas_unit_name_226` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Atlas unit name |
| 31 | `oth567_trendcompany_220` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Company name |
| 32 | `oth567_trendrating_overall_228` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | overall rating of company (integer values 1 to 5 |
| 33 | `oth567_trendsedol_225` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | This refers to the SEDOL |
| 34 | `oth567_trendticker_205` | VECTOR | 0.603 | 交易与微观结构 | 0 | — | — | — | UNTESTED | This refers to the ticker |
| 35 | `oth567atlas_month_210` | VECTOR | 0.603 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The month and year of the position (At MCD level we have converted to date so added {dd} to month field |
| 36 | `oth567primary_city_223` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | City |
| 37 | `oth567primary_country_215` | VECTOR | 0.603 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country |
| 38 | `oth567primary_exchange_230` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Exchange Name |
| 39 | `oth567primary_gvkey_227` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | gv_key |
| 40 | `oth567primary_isin_216` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | ISIN code |
| 41 | `oth567primary_naics_208` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Naics Code |
| 42 | `oth567primary_sedol_211` | VECTOR | 0.603 | 元数据与非信号 | 0 | — | — | — | UNTESTED | sedol |
| 43 | `oth567primary_sic_217` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | sic |
| 44 | `oth567primary_state_213` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | State |
| 45 | `oth567primary_ticker_207` | VECTOR | 0.603 | 交易与微观结构 | 0 | — | — | — | UNTESTED | ticker |
| 46 | `oth567_trendrating_career_opportunities_206` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | rating of career opportunities (1 to 5 |
| 47 | `oth567_trendrating_compensation_and_benefits_229` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | rating of employee compensation and benefits (1 to 5 |
| 48 | `oth567_trendrating_culture_and_values_209` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | rating of company culture and values (integer values 1 to 5 |
| 49 | `oth567_trendrating_senior_leadership_224` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | rating of senior management (1 to 5 |
| 50 | `oth567_trendrating_work_life_balance_214` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | rating of work-life balance (1 to 5 |
| 51 | `oth567_trendrating_business_outlook_212` | VECTOR | 0.602 | 其他 | 0 | — | — | — | UNTESTED | business outlook rating (positive |
| 52 | `oth567_trendrating_recommend_to_friend_222` | VECTOR | 0.602 | 修正与预期 | 0 | — | — | — | UNTESTED | indicates whether reviewer would recommend a friend to the company (positive |
| 53 | `oth567_trendrating_diversity_and_inclusion_221` | VECTOR | 0.596 | 其他 | 0 | — | — | — | UNUSABLE | rating of company diversity and inclusion (integer values 1 to 5 |
| 54 | `oth567_trendrating_ceo_219` | VECTOR | 0.581 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | approval rating of the CEO (approve |
| 55 | `oth567_individualatlas_unit_name_189` | VECTOR | 0.573 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Atlas unit name |
| 56 | `oth567_individualcompany_168` | VECTOR | 0.573 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Company name |
| 57 | `oth567_individualrating_business_outlook_193` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | business outlook rating (positive |
| 58 | `oth567_individualrating_ceo_188` | VECTOR | 0.573 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | approval rating of the CEO (approve |
| 59 | `oth567_individualrating_overall_172` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | overall rating of company (integer values 1 to 5 |
| 60 | `oth567_individualrating_recommend_to_friend_196` | VECTOR | 0.573 | 修正与预期 | 0 | — | — | — | UNUSABLE | indicates whether reviewer would recommend a friend to the company (positive |
| 61 | `oth567_individualsedol_163` | VECTOR | 0.573 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | This refers to the SEDOL |
| 62 | `oth567_individualticker_184` | VECTOR | 0.573 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | This refers to the ticker |
| 63 | `oth567_review_summary_161` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | title of review |
| 64 | `oth567asm_185` | VECTOR | 0.573 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | MSA of position |
| 65 | `oth567country_201` | VECTOR | 0.573 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The name of the country |
| 66 | `oth567job_category_180` | VECTOR | 0.573 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Aggregated new position role with 7 discrete levels |
| 67 | `oth567region_181` | VECTOR | 0.573 | 宏观与行业 | 0 | — | — | — | UNUSABLE | This refers to the region |
| 68 | `oth567review_cons_158` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | negative review of company |
| 69 | `oth567review_featured_175` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | indicates whether review is featured on company page |
| 70 | `oth567review_iscovid19_192` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | indicates whether review mentions the covid19 pandemic |
| 71 | `oth567review_pros_182` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | positive review of company |
| 72 | `oth567reviewer_current_job_203` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | indicates whether the reviewer is a current or former employee |
| 73 | `oth567reviewer_employment_status_162` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | indicates employment type of reviewer (freelance |
| 74 | `oth567role_k50_199` | VECTOR | 0.573 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Aggregated previous position role with 50 discrete levels |
| 75 | `oth567score_career_advancement_194` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score for career advancement |
| 76 | `oth567score_company_size_174` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company size score |
| 77 | `oth567score_compensation_177` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Compensation score |
| 78 | `oth567score_coworkers_159` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score of coworkers |
| 79 | `oth567score_culture_173` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Culture score |
| 80 | `oth567score_diversity_and_inclusion_167` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score for diversity and inclusion |
| 81 | `oth567score_innovation_technology_164` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | score_innovation_technology |
| 82 | `oth567score_management_166` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Management score |
| 83 | `oth567score_mentorship_187` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mentorship score |
| 84 | `oth567score_onboarding_179` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Onboarding scores |
| 85 | `oth567score_perks_165` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score for perks |
| 86 | `oth567score_remote_work_178` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Remote work scores |
| 87 | `oth567score_work_life_balance_195` | VECTOR | 0.573 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score of work life balance |
| 88 | `oth567state_169` | VECTOR | 0.573 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | state of position |
| 89 | `oth567reviewer_length_of_employment_157` | VECTOR | 0.573 | 其他 | 0 | — | — | — | UNUSABLE | number of years the reviewer worked at the company |
| 90 | `oth567_individualrating_career_opportunities_191` | VECTOR | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | rating of career opportunities (1 to 5 |
| 91 | `oth567_individualrating_compensation_and_benefits_200` | VECTOR | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | rating of employee compensation and benefits (1 to 5 |
| 92 | `oth567_individualrating_culture_and_values_176` | VECTOR | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | rating of company culture and values (integer values 1 to 5 |
| 93 | `oth567_individualrating_senior_leadership_155` | VECTOR | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | rating of senior management (1 to 5 |
| 94 | `oth567_individualrating_work_life_balance_190` | VECTOR | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | rating of work-life balance (1 to 5 |
| 95 | `oth567_individualrating_diversity_and_inclusion_160` | VECTOR | 0.563 | 其他 | 0 | — | — | — | UNUSABLE | rating of company diversity and inclusion (integer values 1 to 5 |
| 96 | `oth567review_count_helpful_198` | VECTOR | 0.557 | 其他 | 0 | — | — | — | UNUSABLE | number of users who found the review helpful |
| 97 | `oth567review_advice_171` | VECTOR | 0.544 | 其他 | 0 | — | — | — | UNUSABLE | reviewer's advice to management |
| 98 | `avg_business_outlook_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company month average business outlook rating on a 1 to 5 scale higher is more positive |
| 99 | `avg_career_growth_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company-month average employee rating of career opportunities on a 1–5 scale |
| 100 | `avg_ceo_approval_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Average CEO approval rating from reviews (scale mapped, e.g., 1–5) |
| 101 | `avg_culture_values_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company-level average review rating for culture and values (1–5) |
| 102 | `avg_diversity_inclusion_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company-month average rating of diversity and inclusion on a 1–5 scale |
| 103 | `avg_overall_company_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Rolling average overall company rating from employee reviews at the company-month level (scale roughly 1–5) |
| 104 | `avg_pay_and_benefits_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company-level average review rating of compensation and benefits (1–5) |
| 105 | `avg_recommend_to_peer_score` | VECTOR | 0.528 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average score indicating whether reviewers would recommend the company to a friend for the period (typically 1–5, compan |
| 106 | `avg_senior_management_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company-level average review rating of senior leadership (1–5) |
| 107 | `avg_work_life_balance_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company-level average review rating of work-life balance (1–5) |
| 108 | `benefits_perks_sentiment` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Text-derived score reflecting sentiment about company perks and benefits |
| 109 | `career_advancement_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Text-derived score for career advancement opportunities |
| 110 | `career_growth_rating` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of career opportunities (1 to 5) |
| 111 | `company_size_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Topic score related to company size or employee count derived from review text (scale varies) |
| 112 | `compensation_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Numeric score reflecting perceived compensation competitiveness |
| 113 | `coworkers_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Text-derived sentiment score about coworkers/peer environment |
| 114 | `culture_values_rating` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Rating of company culture and values (typically 1–5 at review level) |
| 115 | `diversity_inclusion_rating` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of diversity and inclusion (1 to 5) |
| 116 | `diversity_inclusion_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Text-derived sentiment score on diversity and inclusion |
| 117 | `employment_duration_years` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Number of years the reviewer worked at the company |
| 118 | `innovation_technology_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score for innovation and technology discussed in the review text |
| 119 | `leadership_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score related to management |
| 120 | `mentorship_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Text-derived mentorship sentiment score |
| 121 | `negative_feedback_text` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Cons/negative comments text provided by the reviewer |
| 122 | `onboarding_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score about onboarding experiences |
| 123 | `overall_company_rating` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s overall rating of the company on a 1–5 scale |
| 124 | `remote_work_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score indicating remote work friendliness or experience reflected in the review text |
| 125 | `remuneration_benefits_score` | VECTOR | 0.528 | 风险与质量 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of compensation and benefits (1 to 5) |
| 126 | `review_helpful_count` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Number of users who marked the review as helpful |
| 127 | `review_positive_comments` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Free-text section listing the pros or positive aspects of the company |
| 128 | `review_title_summary` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Title or short summary of the review |
| 129 | `review_unhelpful_count` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Number of users who marked the review as not helpful |
| 130 | `senior_management_rating` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of senior leadership on a 1–5 scale |
| 131 | `suggestion_to_management` | VECTOR | 0.528 | 修正与预期 | 0 | — | — | — | UNUSABLE | Free-text advice or recommendations to management provided by the reviewer |
| 132 | `work_life_balance_rating` | VECTOR | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of work-life balance (1 to 5) |
| 133 | `work_life_balance_sentiment_score` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Text-derived sentiment score regarding work-life balance |
| 134 | `workplace_culture_sentiment` | VECTOR | 0.528 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score about company culture |
| 135 | `oth567review_count_not_helpful_156` | VECTOR | 0.463 | 其他 | 0 | — | — | — | UNUSABLE | number of users who found the review unhelpful |
| 136 | `oth567_deltaatlas_month` | VECTOR | 0.345 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | The month and year of the position (At MCD level we have converted to date so added {dd} to month field |
| 137 | `oth567_trend_deltarating_business_outlook` | VECTOR | 0.345 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Rolling yearly average business outlook rating or approval |
| 138 | `oth567_trend_deltarating_career_opportunities` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Rating of career opportunities on a 1–5 scale |
| 139 | `oth567_trend_deltarating_ceo` | VECTOR | 0.345 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Rolling yearly average CEO approval rating (share approving or approval level) |
| 140 | `oth567_trend_deltarating_compensation_and_benefits` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Rating of employee compensation and benefits on a 1–5 scale |
| 141 | `oth567_trend_deltarating_culture_and_values` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Average rating of culture and values (1–5 scale) in the trend period |
| 142 | `oth567_trend_deltarating_diversity_and_inclusion` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Rating of company diversity and inclusion on a 1–5 scale |
| 143 | `oth567_trend_deltarating_overall` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Rolling yearly average overall rating at the company-month level on a 1 to 5 scale |
| 144 | `oth567_trend_deltarating_recommend_to_friend` | VECTOR | 0.345 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average rating for likelihood to recommend the company to a friend (trend, 1–5 scale) |
| 145 | `oth567_trend_deltarating_senior_leadership` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Average rating of senior leadership (1–5 scale) in the trend period |
| 146 | `oth567_trend_deltarating_work_life_balance` | VECTOR | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Average employee rating of work-life balance on a 1–5 scale at the company-month level |
| 147 | `oth567_deltaasm_241` | VECTOR | 0.343 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | MSA of position |
| 148 | `oth567_deltacountry_262` | VECTOR | 0.343 | 宏观与行业 | 0 | — | — | — | UNUSABLE | The name of the country |
| 149 | `oth567_deltajob_category_271` | VECTOR | 0.343 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Aggregated new position role with 7 discrete levels |
| 150 | `oth567_deltaregion_247` | VECTOR | 0.343 | 宏观与行业 | 0 | — | — | — | UNUSABLE | This refers to the region |
| 151 | `oth567_deltareview_cons_260` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | negative review of company |
| 152 | `oth567_deltareview_featured_267` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | indicates whether review is featured on company page |
| 153 | `oth567_deltareview_iscovid19_263` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | indicates whether review mentions the covid19 pandemic |
| 154 | `oth567_deltareview_pros_258` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | positive review of company |
| 155 | `oth567_deltareviewer_current_job_264` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | indicates whether the reviewer is a current or former employee |
| 156 | `oth567_deltareviewer_employment_status_237` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | indicates employment type of reviewer (freelance |
| 157 | `oth567_deltarole_k50_272` | VECTOR | 0.343 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Aggregated previous position role with 50 discrete levels |
| 158 | `oth567_deltascore_career_advancement_270` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score for career advancement |
| 159 | `oth567_deltascore_company_size_252` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Company size score |
| 160 | `oth567_deltascore_compensation_233` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Compensation score |
| 161 | `oth567_deltascore_coworkers_265` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score of coworkers |
| 162 | `oth567_deltascore_culture_239` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Culture score |
| 163 | `oth567_deltascore_diversity_and_inclusion_244` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score for diversity and inclusion |
| 164 | `oth567_deltascore_innovation_technology_242` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | score_innovation_technology |
| 165 | `oth567_deltascore_management_253` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Management score |
| 166 | `oth567_deltascore_mentorship_256` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mentorship score |
| 167 | `oth567_deltascore_onboarding_266` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Onboarding scores |
| 168 | `oth567_deltascore_perks_240` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score for perks |
| 169 | `oth567_deltascore_remote_work_235` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Remote work scores |
| 170 | `oth567_deltascore_work_life_balance_274` | VECTOR | 0.343 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score of work life balance |
| 171 | `oth567_deltastate_245` | VECTOR | 0.343 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | state of position |
| 172 | `oth567_individual_deltaatlas_unit_name_259` | VECTOR | 0.343 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Atlas unit name |
| 173 | `oth567_individual_deltarating_business_outlook_257` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | business outlook rating (positive |
| 174 | `oth567_individual_deltarating_ceo_234` | VECTOR | 0.343 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | approval rating of the CEO (approve |
| 175 | `oth567_individual_deltarating_overall_238` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | overall rating of company (integer values 1 to 5 |
| 176 | `oth567_individual_deltarating_recommend_to_friend_251` | VECTOR | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | indicates whether reviewer would recommend a friend to the company (positive |
| 177 | `oth567_deltareview_count_helpful_254` | VECTOR | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | number of users who found the review helpful |
| 178 | `oth567_deltareviewer_length_of_employment_273` | VECTOR | 0.339 | 其他 | 0 | — | — | — | UNUSABLE | number of years the reviewer worked at the company |
| 179 | `oth567_individual_deltarating_career_opportunities_275` | VECTOR | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | rating of career opportunities (1 to 5 |
| 180 | `oth567_individual_deltarating_compensation_and_benefits_269` | VECTOR | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | rating of employee compensation and benefits (1 to 5 |
| 181 | `oth567_individual_deltarating_culture_and_values_232` | VECTOR | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | rating of company culture and values (integer values 1 to 5 |
| 182 | `oth567_individual_deltarating_senior_leadership_276` | VECTOR | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | rating of senior management (1 to 5 |
| 183 | `oth567_individual_deltarating_work_life_balance_236` | VECTOR | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | rating of work-life balance (1 to 5 |
| 184 | `oth567_individual_deltarating_diversity_and_inclusion_248` | VECTOR | 0.331 | 其他 | 0 | — | — | — | UNUSABLE | rating of company diversity and inclusion (integer values 1 to 5 |
| 185 | `oth567_deltareview_advice_255` | VECTOR | 0.310 | 其他 | 0 | — | — | — | UNUSABLE | reviewer?s advice to management |
| 186 | `oth567_trendrating_business_outlook` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average business outlook rating (typically 1–5 or normalized) |
| 187 | `oth567_trendrating_career_opportunities` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average rating of career opportunities (1–5 scale) at the company-month level |
| 188 | `oth567_trendrating_ceo` | VECTOR | 0.303 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Average CEO approval/effectiveness rating (typically on a 1–5 scale) |
| 189 | `oth567_trendrating_compensation_and_benefits` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average review rating of compensation and benefits on a 1–5 scale |
| 190 | `oth567_trendrating_culture_and_values` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average rating of culture and values (1–5 scale) at the company-month level |
| 191 | `oth567_trendrating_diversity_and_inclusion` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average review rating of diversity and inclusion on a 1–5 scale |
| 192 | `oth567_trendrating_overall` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average overall company rating from reviews (1–5 scale) at the company-month level |
| 193 | `oth567_trendrating_recommend_to_friend` | VECTOR | 0.303 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average rating of likelihood to recommend the company to a friend (1–5 scale or normalized) |
| 194 | `oth567_trendrating_senior_leadership` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average review rating of senior leadership on a 1–5 scale |
| 195 | `oth567_trendrating_work_life_balance` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Average review rating of work-life balance on a 1–5 scale |
| 196 | `oth567atlas_month` | VECTOR | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Vendor atlas month key for the record’s period (month-year, used to align trends) |
| 197 | `oth567_deltareview_count_not_helpful_249` | VECTOR | 0.255 | 其他 | 0 | — | — | — | UNUSABLE | number of users who found the review unhelpful |
| 198 | `oth567_individualrating_career_opportunities` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Rating of career opportunities on a 1–5 scale |
| 199 | `oth567_individualrating_compensation_and_benefits` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Per-review rating of compensation and benefits on a 1–5 scale |
| 200 | `oth567_individualrating_culture_and_values` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer rating of company culture and values on a 1 to 5 scale |
| 201 | `oth567_individualrating_diversity_and_inclusion` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of company diversity and inclusion on a 1–5 scale |
| 202 | `oth567_individualrating_overall` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Overall company rating given in the review on a 1–5 scale |
| 203 | `oth567_individualrating_senior_leadership` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Employee’s rating of senior leadership/senior management on a 1–5 scale |
| 204 | `oth567_individualrating_work_life_balance` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s rating of work-life balance, typically 1 to 5 |
| 205 | `oth567_review_summary` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Title or headline of the review |
| 206 | `oth567review_advice` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Reviewer’s advice to management in free text |
| 207 | `oth567review_cons` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Raw textual content of the cons or negatives highlighted by the reviewer |
| 208 | `oth567review_count_helpful` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Count of users who marked the review as helpful |
| 209 | `oth567review_count_not_helpful` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Count of users who marked the review as not helpful |
| 210 | `oth567review_pros` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Free-text pros or positive aspects of the company noted by the reviewer |
| 211 | `oth567reviewer_length_of_employment` | VECTOR | 0.226 | 其他 | 0 | — | — | — | UNUSABLE | Number of years the reviewer worked at the company |
| 212 | `oth567score_career_advancement` | VECTOR | 0.226 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score reflecting perceived career advancement and growth opportunities |
| 213 | `oth567score_company_size` | VECTOR | 0.226 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model-derived score related to company size or perceptions of company scale |
| 214 | `oth567score_compensation` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score related to compensation from the review text |
| 215 | `oth567score_coworkers` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived score reflecting sentiment about coworkers or peer environment in the review |
| 216 | `oth567score_culture` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived culture sentiment score from the review text |
| 217 | `oth567score_diversity_and_inclusion` | VECTOR | 0.226 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model-derived topic score for diversity and inclusion |
| 218 | `oth567score_innovation_technology` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived sentiment score for innovation and technology topics in the review text (real-valued, can be negative or p |
| 219 | `oth567score_management` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived management sentiment score from the review text |
| 220 | `oth567score_mentorship` | VECTOR | 0.226 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model-derived score reflecting mentorship quality or experience |
| 221 | `oth567score_onboarding` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived onboarding sentiment score from the review text |
| 222 | `oth567score_perks` | VECTOR | 0.226 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model-derived score representing company perks and benefits |
| 223 | `oth567score_remote_work` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived score indicating sentiment about remote work |
| 224 | `oth567score_work_life_balance` | VECTOR | 0.226 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Model-derived score reflecting work-life balance sentiment |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-O567-COVERAGE-STRUCTURAL`（None）family=None：{"dataset": "other567", "evidence": "wave135 5 条全灭：longCount 0-13 远低于 80 最低要求，CW 全 FAIL。员工评价数据在 EUR TOP2500 覆盖率极低（0.5277），大部分股票无有效信号。数据覆盖率的结构性问题，不是信号问题。", "reason": "other567 员工评价数据在 EUR D1 判死：覆盖率极低导致 longCount 不足，CW 墙结构性不可破", "region": "EUR", "rule": "Leave other567 在 EUR。员工评价数据在 EUR 市场覆盖率不足，无法形成有效横截面分散。", "wave": 135}

