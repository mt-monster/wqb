# model37 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model37` |
| 名称 | Text Mining Data |
| 类别 | MODEL |
| 数据字段数(平台) | 87 |
| 覆盖率 | 0.6978 |
| 平台已有 alpha | 769 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset delivers a quantitative assessment of corporate credit risk by systematically analyzing the language used in news articles, conference call transcripts, corporate filings, and broker research reports. By leveraging advanced natural language processing and proprietary scoring algorithms, it generates default probabilities, implied credit ratings, and percentile risk ranks for publicly traded companies. The model captures early warning signals of financial distress and credit deterioration that may not be immediately evident in traditional financial ratios, making it a powerful tool for predicting adverse price movements, managing credit exposure, and enhancing multi-factor investment strategies. Its ability to anticipate defaults and downgrades ahead of market consensus provide

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **87** |
| 类型分布 | MATRIX×87 |
| 平均覆盖率 | **0.698** |
| 覆盖率区间 | 0.41 ~ 0.73 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 73 | 83.9% |
| 低 (0.50–0.70) | 8 | 9.2% |
| 稀疏 (<0.50) | 6 | 6.9% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 81 | 93.1% |
| UNUSABLE | 6 | 6.9% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 81 / UNUSABLE 6 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 26 | 0.65 | credit_model_structural_letter_grade_float、credit_risk_global_percentile_score、credit_risk_global_percentile_score_float_2 |
| 宏观与行业 | 21 | 0.72 | credit_risk_country_percentile_score、credit_risk_country_percentile_score_float_2、credit_risk_country_percentile_score_float_4 |
| 情绪与新闻 | 14 | 0.71 | mdl37_t12m_news_count、mdl37_t12m_news_count_d1、mdl37_t1m_news_count |
| 盈利与财务 | 9 | 0.68 | balance_sheet_language_score、mdl37_income、mdl37_income_d1 |
| 元数据与非信号 | 7 | 0.73 | mdl37_t12m_filings_count_d1、mdl37_t12m_tr_cnt_d1、mdl37_t1m_filings_count_d1 |
| 搜索与替代数据 | 6 | 0.73 | mdl37_t12m_brc、mdl37_t12m_brc_d1、mdl37_t1m_brc |
| 其他 | 4 | 0.73 | mdl37_t12m_filings_count、mdl37_t12m_tr_cnt、mdl37_t1m_filings_count |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `credit_model_structural_letter_grade_float` | MATRIX | 0.730 | 风险与质量 | 0 | — | — | — | UNTESTED | Credit rating grade inferred from the structural risk model, as a floating point value. |
| 2 | `balance_sheet_language_score` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language related to how the company structures its debt, stock, and accounts; higher scores i |
| 3 | `credit_risk_country_percentile_score` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank from 1 to 100 by country of the company’s 1-year default probability, where higher values indicate safer |
| 4 | `credit_risk_country_percentile_score_float_2` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | The 0–100 float percentile rank, by country, of the company’s 1‑year default probability; higher values indicate lower r |
| 5 | `credit_risk_country_percentile_score_float_4` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 percentile rank by country of the company’s 1-year default probability; higher scores indicate lower risk |
| 6 | `credit_risk_country_percentile_score_float_5` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 scaled percentile rank of the company’s 1-year default probability by country; higher values indicate lower |
| 7 | `credit_risk_global_percentile_score` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 percentile rank of the company’s 1-year default probability based on the StarMine Text Mining Credit Risk M |
| 8 | `credit_risk_global_percentile_score_float_2` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global peer percentile rank of 1-year PD scaled 0–100; higher value indicates safer credit |
| 9 | `credit_risk_global_percentile_score_float_4` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Float 0–100 scaled global percentile rank of the company’s 1-year default probability; higher values indicate safer cred |
| 10 | `credit_risk_global_percentile_score_float_5` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global peer-relative safety rank scaled 0–100 (percentile) based on text-mined credit risk; higher = safer globally |
| 11 | `credit_risk_region_percentile_score` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | 1–100 percentile rank of the company’s 1-year default probability among firms in the same region; higher scores indicate |
| 12 | `credit_risk_region_percentile_score_float_2` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regional peer-relative safety rank expressed as a 0–100 percentile (higher = safer) |
| 13 | `credit_risk_region_percentile_score_float_4` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 percentile rank within the same region of the company’s 1-year default probability; higher scores indicate l |
| 14 | `credit_risk_region_percentile_score_float_5` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | The 0–100 scaled regional percentile rank (higher = safer) of the company’s 1-year default probability |
| 15 | `default_probability_percent` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Probability of default over the next 1-year period, expressed as a decimal fraction (e.g., 0.005) |
| 16 | `legal_obligation_language_score` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language regarding the company’s agreements with partners or financiers; higher scores indica |
| 17 | `mdl37_country_rank` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | The 1-100 percentile rank, by country, of a company’s 1-year default probability; higher scores indicate lower risk |
| 18 | `mdl37_country_rank_d1` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | 1–100 percentile rank of the company’s 1-year default probability within its country; higher scores indicate lower likel |
| 19 | `mdl37_global_rank` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | The global 1-100 percentile rank of a company’s 1-year default probability; higher scores indicate lower risk |
| 20 | `mdl37_global_rank_d1` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 percentile rank of the company’s 1-year default probability based on the StarMine Text Mining model; higher |
| 21 | `mdl37_income` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | The global 1-100 rank based on language related to the company’s earnings and profitability; higher scores indicate lowe |
| 22 | `mdl37_income_d1` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language about earnings and profitability; higher score indicates lower income-related risk |
| 23 | `mdl37_legal` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language regarding the company’s agreements with partners or financers; higher scores indicat |
| 24 | `mdl37_legal_d1` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language regarding the company’s agreements with partners or financiers; higher scores indica |
| 25 | `mdl37_pd_pct` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | The decimal probability that the company will default over the next 1 year (higher = higher risk) |
| 26 | `mdl37_pd_pct_d1` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | One-year probability of default from the Text Mining Credit Risk model, expressed as a decimal fraction (e.g., 0.005 = 0 |
| 27 | `mdl37_region_rank` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | The 1-100 percentile rank, among firms in the same region, of a company’s 1-year default probability; higher scores indi |
| 28 | `mdl37_region_rank_d1` | MATRIX | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | 1–100 percentile rank of the company’s 1-year default probability within its region; higher scores indicate lower likeli |
| 29 | `mdl37_structural` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language related to how the company structures its debt, stock, and accounts; higher scores i |
| 30 | `mdl37_structural_d1` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language about how the company structures its debt, stock, and accounts; higher scores indica |
| 31 | `mdl37_t12m_brc` | MATRIX | 0.726 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | The number of broker research documents within the trailing 12 months |
| 32 | `mdl37_t12m_brc_d1` | MATRIX | 0.726 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Number of broker research documents within the trailing 12 months before the Data-Through Date |
| 33 | `mdl37_t12m_filings_count` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | The number of regulatory filing documents within the trailing 12 months |
| 34 | `mdl37_t12m_filings_count_d1` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of filing documents within the trailing 12 months before the Data-Through Date |
| 35 | `mdl37_t12m_news_count` | MATRIX | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of news documents within the trailing 12 months |
| 36 | `mdl37_t12m_news_count_d1` | MATRIX | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of relevant news documents over the trailing 12 months prior to the data-through date |
| 37 | `mdl37_t12m_tr_cnt` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | The number of transcript documents within the trailing 12 months |
| 38 | `mdl37_t12m_tr_cnt_d1` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of transcript documents within the trailing 12 months before the Data-Through Date |
| 39 | `mdl37_t1m_brc` | MATRIX | 0.726 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | The number of broker research documents within the trailing 1 month |
| 40 | `mdl37_t1m_brc_d1` | MATRIX | 0.726 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Number of broker research documents within the trailing 30 days before the Data-Through Date |
| 41 | `mdl37_t1m_filings_count` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | The number of filing documents within the trailing 1 month |
| 42 | `mdl37_t1m_filings_count_d1` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of filing documents within the trailing 30 days before the Data-Through Date |
| 43 | `mdl37_t1m_news_count` | MATRIX | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of news documents within the trailing 1 month |
| 44 | `mdl37_t1m_news_count_d1` | MATRIX | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news documents within the trailing 30 days before the Data-Through Date |
| 45 | `mdl37_t1m_tr_cnt` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | The number of transcript documents within the trailing 1 month |
| 46 | `mdl37_t1m_tr_cnt_d1` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of transcript documents within the trailing 30 days before the Data-Through Date |
| 47 | `profitability_language_score` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language related to the company’s earnings and profitability; higher scores indicate lower cr |
| 48 | `recent_broker_research_document_count` | MATRIX | 0.726 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | The number of broker research documents within the trailing 30 days before the Data-Through Date |
| 49 | `recent_filings_document_count` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of filing documents within the 30 days prior to the Data-Through Date |
| 50 | `recent_news_document_count` | MATRIX | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news documents within the 30 days prior to the Data-Through Date |
| 51 | `recent_transcript_document_count` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of earnings call transcript documents in the trailing 30 days before the Data-Through Date |
| 52 | `yearly_broker_research_document_count` | MATRIX | 0.726 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Number of broker research documents within the 12 months prior to the Data-Through Date |
| 53 | `yearly_filings_document_count` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of filing documents within the 12 months prior to the Data-Through Date |
| 54 | `yearly_news_document_count` | MATRIX | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of news documents within the trailing 12 months before the Data-Through Date |
| 55 | `yearly_transcript_document_count` | MATRIX | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of transcript documents within the trailing 12 months before the Data-Through Date |
| 56 | `external_event_language_score` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language about market conditions or third parties materially impacting the company; higher sc |
| 57 | `mdl37_external` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language about market conditions or third parties affecting the company; higher scores indica |
| 58 | `mdl37_external_d1` | MATRIX | 0.726 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank based on language about market conditions or third parties affecting the company; higher scores indica |
| 59 | `credit_risk_sector_percentile_score_2` | MATRIX | 0.725 | 宏观与行业 | 0 | — | — | — | UNTESTED | 1–100 percentile rank of the company’s 1-year default probability among firms in the same region and TRBC Economic Secto |
| 60 | `mdl37_sector_rank` | MATRIX | 0.725 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) of the company’s 1-year default probability relative to peers in the same region and TRBC Econom |
| 61 | `mdl37_sector_rank_d1` | MATRIX | 0.725 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1–100) of the company’s 1-year default probability relative to peers in the same region and TRBC Econom |
| 62 | `credit_risk_industry_percentile_score` | MATRIX | 0.720 | 宏观与行业 | 0 | — | — | — | UNTESTED | 1–100 percentile rank of 1-year default probability within the same region and TRBC Industry Group; higher scores indica |
| 63 | `credit_risk_industry_percentile_score_float_2` | MATRIX | 0.720 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry peer-relative safety rank expressed as a 0–100 percentile (higher = safer) |
| 64 | `credit_risk_industry_percentile_score_float_4` | MATRIX | 0.720 | 宏观与行业 | 0 | — | — | — | UNTESTED | Float 0–100 percentile rank within the same region and TRBC Industry Group of the company’s 1-year default probability; |
| 65 | `credit_risk_industry_percentile_score_float_5` | MATRIX | 0.720 | 宏观与行业 | 0 | — | — | — | UNTESTED | The 0–100 scaled percentile rank (higher = safer) versus peers in the same region and industry |
| 66 | `mdl37_industry_rank` | MATRIX | 0.720 | 宏观与行业 | 0 | — | — | — | UNTESTED | The 1-100 percentile rank, among firms in the same region and TRBC Industry Group, of a company’s 1-year default probabi |
| 67 | `mdl37_industry_rank_d1` | MATRIX | 0.720 | 宏观与行业 | 0 | — | — | — | UNTESTED | 1–100 percentile rank of the company’s 1-year default probability within its region and TRBC Industry Group; higher scor |
| 68 | `credit_risk_news_component_score` | MATRIX | 0.715 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global 1–100 rank of a company’s credit riskiness based on textual data in Reuters news articles from the StarMine Text |
| 69 | `credit_risk_news_component_score_float_2` | MATRIX | 0.715 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Float-scaled (0–100) News-based credit risk component score from the StarMine Text Mining Credit Risk Model using Reuter |
| 70 | `credit_risk_news_component_score_float_4` | MATRIX | 0.715 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News source component score scaled 0–100 from text-mined credit signals; higher values indicate more favorable/safer cre |
| 71 | `credit_risk_news_component_score_float_5` | MATRIX | 0.715 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News component score scaled 0–100 reflecting credit tone/signal from news; higher = safer/more positive |
| 72 | `mdl37_news` | MATRIX | 0.715 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The global 1-100 rank of a company's credit riskiness based on textual data in Reuters news articles; higher scores indi |
| 73 | `mdl37_news_d1` | MATRIX | 0.715 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global 1–100 rank of credit riskiness based on Reuters news text; higher scores indicate lower risk (safer) |
| 74 | `credit_risk_broker_research_component_score` | MATRIX | 0.668 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank of credit riskiness based on textual data in broker research documents; higher scores indicate lower r |
| 75 | `credit_risk_broker_research_component_score_float_2` | MATRIX | 0.668 | 风险与质量 | 0 | — | — | — | UNTESTED | Float-scaled (0–100) broker research component score from the StarMine Text Mining Credit Risk Model; higher values indi |
| 76 | `credit_risk_broker_research_component_score_float_4` | MATRIX | 0.668 | 风险与质量 | 0 | — | — | — | UNTESTED | Float 0–100 scaled global rank of credit risk based on broker research text; higher scores indicate lower risk |
| 77 | `credit_risk_broker_research_component_score_float_5` | MATRIX | 0.668 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Broker research component score scaled 0–100 reflecting credit tone/signal from broker reports; higher = safer/more posi |
| 78 | `mdl37_broker_research` | MATRIX | 0.668 | 风险与质量 | 0 | — | — | — | UNTESTED | The global 1-100 rank of a company's credit riskiness based on textual data in broker research documents; higher scores |
| 79 | `mdl37_broker_research_d1` | MATRIX | 0.668 | 风险与质量 | 0 | — | — | — | UNTESTED | Global 1–100 rank of credit riskiness based on broker research text; higher scores indicate lower risk (safer) |
| 80 | `mdl37_index_rating` | MATRIX | 0.661 | 情绪与新闻 | 0 | — | — | — | UNTESTED | probability of default by quantitatively analyzing textual content including transcripts, news, filings, and research |
| 81 | `mdl37_structural_rating` | MATRIX | 0.661 | 盈利与财务 | 0 | — | — | — | UNTESTED | rating indicating probability of default based on structural leverage, asset volatility, and asset drift |
| 82 | `credit_risk_transcripts_component_score_float_5` | MATRIX | 0.410 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings call transcripts component score scaled 0–100 reflecting credit tone/signal; higher = safer/more positive |
| 83 | `mdl37_credit_textscore` | MATRIX | 0.410 | 风险与质量 | 0 | — | — | — | UNUSABLE | The global 1-100 rank of a company's credit riskiness based on textual data in StreetEvents conference call transcripts; |
| 84 | `credit_risk_transcripts_component_score` | MATRIX | 0.410 | 风险与质量 | 0 | — | — | — | UNUSABLE | Global 1–100 rank of a company’s credit riskiness based on textual data in StreetEvents conference call transcripts from |
| 85 | `credit_risk_transcripts_component_score_float_2` | MATRIX | 0.410 | 风险与质量 | 0 | — | — | — | UNUSABLE | The 0–100 scaled transcripts-based component score from the StarMine Text Mining Credit Risk Model based on conference c |
| 86 | `credit_risk_transcripts_component_score_float_4` | MATRIX | 0.410 | 风险与质量 | 0 | — | — | — | UNUSABLE | Float 0–100 scaled global rank based on textual data in conference call transcripts; higher scores indicate lower risk |
| 87 | `mdl37_credit_textscore_d1` | MATRIX | 0.410 | 风险与质量 | 0 | — | — | — | UNUSABLE | Global 1–100 rank of credit riskiness based on StreetEvents conference call transcripts; higher scores indicate lower ri |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

