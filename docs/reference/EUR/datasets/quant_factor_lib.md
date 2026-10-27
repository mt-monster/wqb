# quant_factor_lib — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `quant_factor_lib` |
| 名称 | Multi-Domain Quantitative Factor Library |
| 类别 | MODEL |
| 数据字段数(平台) | 126 |
| 覆盖率 | 0.5117 |
| 平台已有 alpha | 4 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset is a comprehensive library of quantitative factors designed for stock selection and risk modeling across global equities. It integrates hundreds of signals derived from regulatory filings, institutional ownership, sector-specific metrics, technical indicators, sentiment analysis, patent data, and alternative sources. The factors span multiple domains, including banking, technology, real estate, health care, and energy, and leverage both numerical and textual data using advanced techniques such as natural language processing and network analysis. By providing diverse, uncorrelated signals and sector-specific insights, the dataset enables investors and researchers to enhance alpha generation, improve risk management, and develop robust predictive models for price movements in va

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **126** |
| 类型分布 | VECTOR×126 |
| 平均覆盖率 | **0.512** |
| 覆盖率区间 | 0.34 ~ 0.79 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 19 | 15.1% |
| 低 (0.50–0.70) | 13 | 10.3% |
| 稀疏 (<0.50) | 94 | 74.6% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 97 | 77.0% |
| UNTESTED | 29 | 23.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 29 / UNUSABLE 97 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 72 | 0.45 | qfl_nlp_calltranscript_global_dist_cos_mgmt_qa、qfl_nlp_calltranscript_global_num_exec_female、qfl_nlp_calltranscript_global_num_exec_male |
| 修正与预期 | 22 | 0.46 | qfl_cassie_model_merton、qfl_nlp_calltranscript_global_num_que_buyside、qfl_nlp_calltranscript_global_num_que_sellside |
| 盈利与财务 | 15 | 0.70 | qfl_cassie_convention_debt_mktcapital、qfl_cassie_convention_current_ratio、qfl_cassie_convention_ocf_currliab |
| 风险与质量 | 10 | 0.69 | qfl_cassie_qes_cassie_prelimcomposite、qfl_cassie_qes_cassie_score、qfl_cassie_model_altman_zscore |
| 其他 | 3 | 0.72 | qfl_cassie_mktcap、qfl_cassie_convention_quick_ratio、qfl_cassie_qes_alter_distance_insolvency_1y |
| 宏观与行业 | 3 | 0.60 | qfl_cassie_qes_alter_moderate_insolvency_stress_1y、qfl_cassie_qes_alter_moderate_insolvency_stress_2y、qfl_cassie_qes_alter_moderate_insolvency_stress_9m |
| 价量与波动 | 1 | 0.71 | qfl_cassie_qes_cassie_impliedalpha |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `qfl_cassie_qes_cassie_prelimcomposite` | VECTOR | 0.785 | 风险与质量 | 0 | — | — | — | UNTESTED | Preliminary composite score from the credit risk model. |
| 2 | `qfl_cassie_qes_cassie_score` | VECTOR | 0.785 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite credit risk score from the CASSIE model. |
| 3 | `qfl_cassie_convention_debt_mktcapital` | VECTOR | 0.785 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to market capitalization. |
| 4 | `qfl_cassie_mktcap` | VECTOR | 0.785 | 其他 | 0 | — | — | — | UNTESTED | Total market value of a company's outstanding shares. |
| 5 | `qfl_cassie_convention_current_ratio` | VECTOR | 0.784 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio measuring a company's ability to pay short-term liabilities. |
| 6 | `qfl_cassie_convention_ocf_currliab` | VECTOR | 0.784 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of operating cash flow to current liabilities. |
| 7 | `qfl_cassie_convention_quick_ratio` | VECTOR | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Quick ratio measuring a company's ability to meet short-term obligations. |
| 8 | `qfl_cassie_model_altman_zscore` | VECTOR | 0.783 | 风险与质量 | 0 | — | — | — | UNTESTED | Altman Z-Score indicating probability of bankruptcy. |
| 9 | `qfl_cassie_convention_longdebt_equity` | VECTOR | 0.782 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of long-term debt to equity for a company. |
| 10 | `qfl_cassie_model_ohlson_oscore` | VECTOR | 0.781 | 风险与质量 | 0 | — | — | — | UNTESTED | Ohlson O-Score indicating probability of default or bankruptcy. |
| 11 | `qfl_cassie_model_merton` | VECTOR | 0.780 | 修正与预期 | 0 | — | — | — | UNTESTED | Distance to default as estimated by the Merton model. |
| 12 | `qfl_cassie_qes_alter_debt_weighted_duration` | VECTOR | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average maturity of debt, weighted by principal amounts. |
| 13 | `qfl_cassie_convention_cng_longdebt_equity` | VECTOR | 0.776 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of long-term debt to equity over a period. |
| 14 | `qfl_cassie_qes_alter_revolver_debt` | VECTOR | 0.775 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total amount of revolving debt outstanding. |
| 15 | `qfl_cassie_model_chs_default` | VECTOR | 0.760 | 风险与质量 | 0 | — | — | — | UNTESTED | Score from the CHS model predicting likelihood of default. |
| 16 | `qfl_cassie_convention_debt_equity` | VECTOR | 0.719 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total equity for a company. |
| 17 | `qfl_cassie_qes_cassie_impliedalpha` | VECTOR | 0.715 | 价量与波动 | 0 | — | — | — | UNTESTED | Implied alpha or expected excess return derived from credit risk models. |
| 18 | `qfl_cassie_convention_longdebt_capital` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of long-term debt to total capital. |
| 19 | `qfl_cassie_convention_debt_capital` | VECTOR | 0.704 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total capital for a company. |
| 20 | `qfl_cassie_qes_alter_debt_weighted_interest_rate` | VECTOR | 0.601 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average interest rate on debt, weighted by principal amounts. |
| 21 | `qfl_cassie_qes_alter_short_longterm_debt_ratio` | VECTOR | 0.601 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of short-term debt to long-term debt. |
| 22 | `qfl_cassie_qes_alter_extreme_insolvency_stress_1y` | VECTOR | 0.601 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating extreme insolvency risk projected one year ahead. |
| 23 | `qfl_cassie_qes_alter_extreme_insolvency_stress_9m` | VECTOR | 0.601 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating extreme insolvency risk projected nine months ahead. |
| 24 | `qfl_cassie_qes_alter_insolvency_stress_1y` | VECTOR | 0.601 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating the level of insolvency risk projected one year ahead. |
| 25 | `qfl_cassie_qes_alter_insolvency_stress_2y` | VECTOR | 0.601 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating the level of insolvency risk projected two years ahead. |
| 26 | `qfl_cassie_qes_alter_insolvency_stress_9m` | VECTOR | 0.601 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating the level of insolvency risk projected nine months ahead. |
| 27 | `qfl_cassie_qes_alter_moderate_insolvency_stress_1y` | VECTOR | 0.601 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score indicating moderate insolvency risk projected one year ahead. |
| 28 | `qfl_cassie_qes_alter_moderate_insolvency_stress_2y` | VECTOR | 0.601 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score indicating moderate insolvency risk projected two years ahead. |
| 29 | `qfl_cassie_qes_alter_moderate_insolvency_stress_9m` | VECTOR | 0.601 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score indicating moderate insolvency risk projected nine months ahead. |
| 30 | `qfl_cassie_qes_alter_growth_shortterm_debt` | VECTOR | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Growth rate of short-term debt over a specified period. |
| 31 | `qfl_cassie_qes_alter_distance_insolvency_1y` | VECTOR | 0.580 | 其他 | 0 | — | — | — | UNUSABLE | Distance to insolvency threshold projected one year ahead. |
| 32 | `qfl_cassie_qes_alter_shortterm_debt_ratio` | VECTOR | 0.567 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of short-term debt to total debt. |
| 33 | `qfl_nlp_calltranscript_global_dist_cos_mgmt_qa` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cosine distance measuring similarity between management presentation and Q&A sections. |
| 34 | `qfl_nlp_calltranscript_global_num_exec_female` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of female executives present at the event. |
| 35 | `qfl_nlp_calltranscript_global_num_exec_male` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of male executives present at the event. |
| 36 | `qfl_nlp_calltranscript_global_num_que_buyside` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of questions asked by buy-side analysts during the event. |
| 37 | `qfl_nlp_calltranscript_global_num_que_sellside` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of questions asked by sell-side analysts during the event. |
| 38 | `qfl_nlp_calltranscript_global_num_sellside_anlst` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of sell-side analysts present at the event. |
| 39 | `qfl_nlp_calltranscript_global_pre_ceo_count_pos_adj` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adjectives used by CEO in presentations. |
| 40 | `qfl_nlp_calltranscript_global_pre_ceo_count_pos_adv` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adverbs used by CEO in presentations. |
| 41 | `qfl_nlp_calltranscript_global_pre_ceo_count_pos_prepo` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of positive prepositions used by the CEO in the presentation section. |
| 42 | `qfl_nlp_calltranscript_global_pre_ceo_count_pos_pron` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive pronouns used by CEO in presentations. |
| 43 | `qfl_nlp_calltranscript_global_pre_ceo_count_words` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total number of words spoken by CEO in presentations. |
| 44 | `qfl_nlp_calltranscript_global_pre_ceo_hd_neg` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for CEO presentations using the Harvard dictionary. |
| 45 | `qfl_nlp_calltranscript_global_pre_ceo_hd_pos` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for CEO presentations using the Harvard dictionary. |
| 46 | `qfl_nlp_calltranscript_global_pre_oth_count_pos_adj` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adjectives used by other executives in presentations. |
| 47 | `qfl_nlp_calltranscript_global_pre_oth_count_pos_adv` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adverbs used by other executives in presentations. |
| 48 | `qfl_nlp_calltranscript_global_pre_oth_count_pos_prepo` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive prepositions used by other executives in presentations. |
| 49 | `qfl_nlp_calltranscript_global_pre_oth_count_pos_pron` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive pronouns used by other executives in presentations. |
| 50 | `qfl_nlp_calltranscript_global_pre_oth_count_words` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total number of words spoken by other executives in presentations. |
| 51 | `qfl_nlp_calltranscript_global_pre_oth_hd_neg` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for other executives' presentations using the Harvard dictionary. |
| 52 | `qfl_nlp_calltranscript_global_pre_oth_hd_pos` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for other executives' presentations using the Harvard dictionary. |
| 53 | `qfl_nlp_calltranscript_global_qa_ceo_count_pos_adj` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adjectives used by CEO in Q&A responses. |
| 54 | `qfl_nlp_calltranscript_global_qa_ceo_count_pos_adv` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adverbs used by CEO in Q&A responses. |
| 55 | `qfl_nlp_calltranscript_global_qa_ceo_count_pos_prepo` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive prepositions used by CEO in Q&A responses. |
| 56 | `qfl_nlp_calltranscript_global_qa_ceo_count_pos_pron` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of positive pronouns used by the CEO during Q&A sessions. |
| 57 | `qfl_nlp_calltranscript_global_qa_ceo_count_words` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total number of words spoken by CEO in Q&A responses. |
| 58 | `qfl_nlp_calltranscript_global_qa_ceo_hd_neg` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for CEO responses in Q&A using the Harvard dictionary. |
| 59 | `qfl_nlp_calltranscript_global_qa_ceo_hd_pos` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for CEO Q&A responses using the Harvard dictionary. |
| 60 | `qfl_nlp_calltranscript_global_qa_oth_count_pos_adj` | VECTOR | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of positive adjectives used by non-executive speakers during the Q&A session of an earnings call. |
| 61 | `qfl_nlp_calltranscript_global_qa_oth_count_pos_adv` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adverbs used by other executives in Q&A. |
| 62 | `qfl_nlp_calltranscript_global_qa_oth_count_pos_prepo` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive prepositions used by other executives in Q&A. |
| 63 | `qfl_nlp_calltranscript_global_qa_oth_count_pos_pron` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive pronouns used by other executives in Q&A. |
| 64 | `qfl_nlp_calltranscript_global_qa_oth_count_words` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total number of words spoken by other executives in Q&A. |
| 65 | `qfl_nlp_calltranscript_global_qa_oth_hd_neg` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for other executives' Q&A responses using the Harvard dictionary. |
| 66 | `qfl_nlp_calltranscript_global_qa_oth_hd_pos` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for other executives' Q&A responses using the Harvard dictionary. |
| 67 | `qfl_nlp_calltranscript_global_qa_rest_count_pos_adj` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adjectives used by remaining participants in Q&A. |
| 68 | `qfl_nlp_calltranscript_global_qa_rest_count_pos_adv` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive adverbs used by other participants during Q&A sessions. |
| 69 | `qfl_nlp_calltranscript_global_qa_rest_count_pos_prepo` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive prepositions used by remaining participants in Q&A. |
| 70 | `qfl_nlp_calltranscript_global_qa_rest_count_pos_pron` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive pronouns used by remaining participants in Q&A. |
| 71 | `qfl_nlp_calltranscript_global_qa_rest_count_words` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total number of words spoken by remaining participants in Q&A. |
| 72 | `qfl_nlp_calltranscript_global_qa_rest_hd_neg` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for remaining participants in Q&A using the Harvard dictionary. |
| 73 | `qfl_nlp_calltranscript_global_qa_rest_hd_pos` | VECTOR | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for remaining participants in Q&A using the Harvard dictionary. |
| 74 | `qfl_nlp_calltranscript_global_qa_sell_count_pos_adj` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of positive adjectives used by sell-side analysts in Q&A. |
| 75 | `qfl_nlp_calltranscript_global_qa_sell_count_pos_adv` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of positive adverbs used by sell-side analysts in Q&A. |
| 76 | `qfl_nlp_calltranscript_global_qa_sell_count_pos_prepo` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of positive prepositions used by sell-side analysts in Q&A. |
| 77 | `qfl_nlp_calltranscript_global_qa_sell_count_pos_pron` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of positive pronouns used by sell-side analysts in Q&A. |
| 78 | `qfl_nlp_calltranscript_global_qa_sell_count_words` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of words spoken by sell-side analysts during Q&A sessions. |
| 79 | `qfl_nlp_calltranscript_global_qa_sell_hd_neg` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Negative sentiment score for sell-side analyst Q&A using the Harvard dictionary. |
| 80 | `qfl_nlp_calltranscript_global_qa_sell_hd_pos` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Positive sentiment score for sell-side analyst Q&A using the Harvard dictionary. |
| 81 | `qfl_nlp_calltranscript_global_total_anlst` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts present at the event. |
| 82 | `qfl_nlp_calltranscript_global_all_avg_rating` | VECTOR | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average rating given by all analysts present at the event. |
| 83 | `qfl_nlp_calltranscript_global_qa_oth_lm2_cum_neg` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative negative sentiment for other executives' Q&A using Loughran-McDonald dictionary. |
| 84 | `qfl_nlp_calltranscript_global_qa_oth_lm2_cum_pos` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative positive sentiment for other executives' Q&A using Loughran-McDonald dictionary. |
| 85 | `qfl_nlp_calltranscript_global_qa_oth_read_cl` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of other executives' Q&A using the Coleman-Liau index. |
| 86 | `qfl_nlp_calltranscript_global_qa_oth_read_dc` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of other executives' Q&A using the Dale-Chall formula. |
| 87 | `qfl_nlp_calltranscript_global_qa_oth_read_fog` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of other executives' Q&A using the FOG index. |
| 88 | `qfl_nlp_calltranscript_global_qa_oth_vader_neg` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for other executives' Q&A responses using VADER. |
| 89 | `qfl_nlp_calltranscript_global_qa_oth_vader_pos` | VECTOR | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for other executives' Q&A responses using VADER. |
| 90 | `qfl_nlp_calltranscript_global_pre_oth_lm2_cum_neg` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative negative sentiment score (LM2 dictionary) for other speakers in the presentation section. |
| 91 | `qfl_nlp_calltranscript_global_pre_oth_lm2_cum_pos` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative positive sentiment for other executives' presentations using Loughran-McDonald dictionary. |
| 92 | `qfl_nlp_calltranscript_global_pre_oth_read_cl` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of other executives' presentations using the Coleman-Liau index. |
| 93 | `qfl_nlp_calltranscript_global_pre_oth_read_dc` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of other executives' presentations using the Dale-Chall formula. |
| 94 | `qfl_nlp_calltranscript_global_pre_oth_read_fog` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of other executives' presentations based on the FOG index. |
| 95 | `qfl_nlp_calltranscript_global_pre_oth_vader_neg` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for other executives' presentations using VADER. |
| 96 | `qfl_nlp_calltranscript_global_pre_oth_vader_pos` | VECTOR | 0.438 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for other executives' presentations using VADER. |
| 97 | `qfl_nlp_calltranscript_global_qa_rest_lm2_cum_neg` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative negative sentiment score (LM2 dictionary) for other participants during Q&A. |
| 98 | `qfl_nlp_calltranscript_global_qa_rest_lm2_cum_pos` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative positive sentiment for remaining participants in Q&A using Loughran-McDonald dictionary. |
| 99 | `qfl_nlp_calltranscript_global_qa_rest_read_cl` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of remaining participants' Q&A using the Coleman-Liau index. |
| 100 | `qfl_nlp_calltranscript_global_qa_rest_read_dc` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of remaining participants' Q&A using the Dale-Chall formula. |
| 101 | `qfl_nlp_calltranscript_global_qa_rest_read_fog` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of remaining participants' Q&A using the FOG index. |
| 102 | `qfl_nlp_calltranscript_global_qa_rest_vader_neg` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for remaining participants in Q&A using VADER. |
| 103 | `qfl_nlp_calltranscript_global_qa_rest_vader_pos` | VECTOR | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score (VADER) for other participants during Q&A sessions. |
| 104 | `qfl_nlp_calltranscript_global_qa_sell_lm2_cum_neg` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Cumulative negative sentiment score (LM2 dictionary) for sell-side analysts during Q&A. |
| 105 | `qfl_nlp_calltranscript_global_qa_sell_lm2_cum_pos` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Cumulative positive sentiment for sell-side analyst Q&A using Loughran-McDonald dictionary. |
| 106 | `qfl_nlp_calltranscript_global_qa_sell_read_cl` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Readability score of sell-side analyst Q&A using the Coleman-Liau index. |
| 107 | `qfl_nlp_calltranscript_global_qa_sell_read_dc` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Readability score of sell-side analyst Q&A using the Dale-Chall formula. |
| 108 | `qfl_nlp_calltranscript_global_qa_sell_read_fog` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Readability score of sell-side analyst Q&A using the FOG index. |
| 109 | `qfl_nlp_calltranscript_global_qa_sell_vader_neg` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Negative sentiment score for sell-side analyst Q&A using VADER. |
| 110 | `qfl_nlp_calltranscript_global_qa_sell_vader_pos` | VECTOR | 0.410 | 修正与预期 | 0 | — | — | — | UNUSABLE | Positive sentiment score for sell-side analyst Q&A using VADER. |
| 111 | `qfl_nlp_calltranscript_global_pre_ceo_lm2_cum_neg` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative negative sentiment for CEO presentations using Loughran-McDonald dictionary. |
| 112 | `qfl_nlp_calltranscript_global_pre_ceo_lm2_cum_pos` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative positive sentiment score (LM2 dictionary) for the CEO in the presentation section. |
| 113 | `qfl_nlp_calltranscript_global_pre_ceo_read_cl` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of CEO presentations using the Coleman-Liau index. |
| 114 | `qfl_nlp_calltranscript_global_pre_ceo_read_dc` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of CEO presentations using the Dale-Chall formula. |
| 115 | `qfl_nlp_calltranscript_global_pre_ceo_read_fog` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of CEO presentations based on the FOG index. |
| 116 | `qfl_nlp_calltranscript_global_pre_ceo_vader_neg` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for CEO presentations using VADER. |
| 117 | `qfl_nlp_calltranscript_global_pre_ceo_vader_pos` | VECTOR | 0.409 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for CEO presentations using VADER. |
| 118 | `qfl_nlp_calltranscript_global_qa_ceo_lm2_cum_neg` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative negative sentiment for CEO Q&A responses using Loughran-McDonald dictionary. |
| 119 | `qfl_nlp_calltranscript_global_qa_ceo_lm2_cum_pos` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Cumulative positive sentiment for CEO Q&A responses using Loughran-McDonald dictionary. |
| 120 | `qfl_nlp_calltranscript_global_qa_ceo_read_cl` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of CEO Q&A responses using the Coleman-Liau index. |
| 121 | `qfl_nlp_calltranscript_global_qa_ceo_read_dc` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of CEO Q&A responses using the Dale-Chall formula. |
| 122 | `qfl_nlp_calltranscript_global_qa_ceo_read_fog` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Readability score of CEO responses in Q&A based on the FOG index. |
| 123 | `qfl_nlp_calltranscript_global_qa_ceo_vader_neg` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score for CEO Q&A responses using VADER. |
| 124 | `qfl_nlp_calltranscript_global_qa_ceo_vader_pos` | VECTOR | 0.402 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for CEO Q&A responses using VADER. |
| 125 | `qfl_nlp_calltranscript_global_avg_rating` | VECTOR | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean rating assigned by analysts during the event. |
| 126 | `qfl_nlp_calltranscript_global_rating_diff` | VECTOR | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between the highest and lowest analyst ratings for the event. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

