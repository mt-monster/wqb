# earningscall_sentiment — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `earningscall_sentiment` |
| 名称 | Multi Aspect Earnings Call Sentiment |
| 类别 | OTHER |
| 数据字段数(平台) | 167 |
| 覆盖率 | 0.5061 |
| 平台已有 alpha | 4800 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides advanced, multi-aspect sentiment analysis of earnings call transcripts for thousands of public companies across the US and Europe. Using state-of-the-art natural language processing and knowledge distillation from large language models, it evaluates sentiment across key financial dimensions such as asset utilization, profitability, leverage, valuation, and cash flow. The transcripts are segmented into presentation, question, and answer sections, with chunk-wise and summary sentiment scores available for each. Binary indicators and relevance scores help filter for the most impactful segments. By quantifying positive, negative, and neutral sentiment at granular and summary levels, the dataset enables investors and researchers to detect shifts in management tone, analyst

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **167** |
| 类型分布 | MATRIX×144　VECTOR×23 |
| 平均覆盖率 | **0.506** |
| 覆盖率区间 | 0.48 ~ 0.51 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 147 | 88.0% |
| 稀疏 (<0.50) | 20 | 12.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 167 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 167 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 96 | 0.51 | assetutilization_negative_score、assetutilization_neutral_score、assetutilization_positive_score |
| 情绪与新闻 | 33 | 0.50 | count_negative_leverage_answer、count_negative_leverage_presentation、count_negative_valuation_presentation |
| 其他 | 19 | 0.51 | answer_chunk_count、count_negative_leverage_question、count_negative_leverage_summary |
| 风险与质量 | 19 | 0.51 | chunk_relevance_z0_flag、chunk_relevance_z1_flag、chunk_relevance_z2_flag |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `answer_chunk_count` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Total number of semantic chunks in the Answers section of the conference call (per stock-date event) |
| 2 | `assetutilization_negative_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Negative probability score for asset utilization statements in the chunk |
| 3 | `assetutilization_neutral_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Neutral probability score for asset utilization statements in the chunk |
| 4 | `assetutilization_positive_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Positive probability score for asset utilization statements in the chunk |
| 5 | `assetutilization_sentiment_polarity` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Signed net sentiment polarity for asset utilization in the chunk (approximately −1 to +1) |
| 6 | `cashflow_negative_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Negative probability score for cash flow statements in the chunk |
| 7 | `cashflow_neutral_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Neutral probability score for cash flow statements in the chunk |
| 8 | `cashflow_positive_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Positive probability score for cash flow statements in the chunk |
| 9 | `cashflow_sentiment_polarity` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Signed net sentiment polarity for cash flow in the chunk (approximately −1 to +1) |
| 10 | `chunk_relevance_z0_flag` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Indicator if the chunk relevance z-score is above 0 (1 if above, 0 otherwise) |
| 11 | `chunk_relevance_z1_flag` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Indicator if the chunk relevance z-score is above 1 (1 if above, 0 otherwise) |
| 12 | `chunk_relevance_z2_flag` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Indicator if the chunk relevance z-score is above 2 (1 if above, 0 otherwise) |
| 13 | `count_negative_assetutilization_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as negative for asset utilization |
| 14 | `count_negative_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of negative sentiment chunks about asset utilization in the presentation section of the conference call (USA, D1 delay) |
| 15 | `count_negative_assetutilization_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as negative for asset utilization-related content |
| 16 | `count_negative_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as negative for asset utilization across the entire conference call (ALL sections) |
| 17 | `count_negative_cashflow_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as negative for cash flow |
| 18 | `count_negative_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of negative sentiment chunks about cash flow in the presentation section of the conference call (USA, D1 delay) |
| 19 | `count_negative_cashflow_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as negative for cash flow-related content |
| 20 | `count_negative_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as negative for cash flow across the entire conference call (ALL sections) |
| 21 | `count_negative_leverage_answer` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of chunks in the Answers section with negative sentiment regarding leverage (per stock-date event) |
| 22 | `count_negative_leverage_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of semantic chunks in the Presentation (P) section of the conference call that exhibit negative leverage sentiment for the given stock |
| 23 | `count_negative_leverage_question` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Count of chunks labeled negative on the leverage axis in the Q&A section of the conference call (USA, D1 lag) |
| 24 | `count_negative_leverage_summary` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks classified as negative for leverage across the entire conference call (ALL sections) |
| 25 | `count_negative_profitability_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks in the Answers section with negative sentiment regarding profitability (per stock-date event) |
| 26 | `count_negative_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of negative sentiment chunks about profitability in the presentation section of the conference call (USA, D1 delay) |
| 27 | `count_negative_profitability_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks labeled negative on the profitability axis in the Q&A section of the conference call (USA, D1 lag) |
| 28 | `count_negative_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as negative for profitability across the entire conference call (ALL sections) |
| 29 | `count_negative_valuation_answer` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as negative for valuation |
| 30 | `count_negative_valuation_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of negative sentiment chunks about valuation in the presentation section of the conference call (USA, D1 delay) |
| 31 | `count_negative_valuation_question` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as negative for valuation-related content |
| 32 | `count_negative_valuation_summary` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks classified as negative for valuation across the entire conference call (ALL sections) |
| 33 | `count_neutral_assetutilization_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as neutral for asset utilization |
| 34 | `count_neutral_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of neutral sentiment chunks about asset utilization in the presentation section of the conference call (USA, D1 delay) |
| 35 | `count_neutral_assetutilization_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as neutral for asset utilization-related content |
| 36 | `count_neutral_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks with neutral sentiment related to asset utilization across the entire call (all sections) |
| 37 | `count_neutral_cashflow_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as neutral for cash flow |
| 38 | `count_neutral_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of neutral sentiment chunks about cash flow in the presentation section of the conference call (USA, D1 delay) |
| 39 | `count_neutral_cashflow_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as neutral for cash flow-related content |
| 40 | `count_neutral_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as neutral for cash flow across the entire conference call (ALL sections) |
| 41 | `count_neutral_leverage_answer` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of chunks in the Answers section with neutral sentiment regarding leverage (per stock-date event) |
| 42 | `count_neutral_leverage_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of neutral sentiment chunks about leverage in the presentation section of the conference call (USA, D1 delay) |
| 43 | `count_neutral_leverage_question` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as neutral for leverage-related content |
| 44 | `count_neutral_leverage_summary` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks classified as neutral for leverage across the entire conference call (ALL sections) |
| 45 | `count_neutral_profitability_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as neutral for profitability |
| 46 | `count_neutral_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of neutral sentiment chunks about profitability in the presentation section of the conference call (USA, D1 delay) |
| 47 | `count_neutral_profitability_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks labeled neutral on the profitability axis in the Q&A section of the conference call (USA, D1 lag) |
| 48 | `count_neutral_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as neutral for profitability across the entire conference call (ALL sections) |
| 49 | `count_neutral_valuation_answer` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as neutral for valuation |
| 50 | `count_neutral_valuation_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of neutral sentiment chunks about valuation in the presentation section of the conference call (USA, D1 delay) |
| 51 | `count_neutral_valuation_question` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks in the Q&A section classified as neutral regarding valuation for the conference call |
| 52 | `count_neutral_valuation_summary` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks classified as neutral for valuation across the entire conference call (ALL sections) |
| 53 | `count_positive_assetutilization_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as positive for asset utilization |
| 54 | `count_positive_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of positive sentiment chunks about asset utilization in the presentation section of the conference call (USA, D1 delay) |
| 55 | `count_positive_assetutilization_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks labeled positive on the asset utilization axis in the Q&A section of the conference call (USA, D1 lag) |
| 56 | `count_positive_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as positive for asset utilization across the entire conference call (ALL sections) |
| 57 | `count_positive_cashflow_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as positive for cash flow |
| 58 | `count_positive_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of semantic chunks in the Presentation (P) section of the conference call that exhibit positive cash flow sentiment for the given stoc |
| 59 | `count_positive_cashflow_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of chunks in the Q&A section classified as positive for cash flow-related content |
| 60 | `count_positive_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as positive for cash flow across the entire conference call (ALL sections) |
| 61 | `count_positive_leverage_answer` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as positive for leverage |
| 62 | `count_positive_leverage_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of positive sentiment chunks about leverage in the presentation section of the conference call (USA, D1 delay) |
| 63 | `count_positive_leverage_question` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Count of chunks labeled positive on the leverage axis in the Q&A section of the conference call (USA, D1 lag) |
| 64 | `count_positive_leverage_summary` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks classified as positive for leverage across the entire conference call (ALL sections) |
| 65 | `count_positive_profitability_answer` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as positive for profitability |
| 66 | `count_positive_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of positive sentiment chunks about profitability in the presentation section of the conference call (USA, D1 delay) |
| 67 | `count_positive_profitability_question` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks in the Q&A section classified as positive regarding profitability for the conference call |
| 68 | `count_positive_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of chunks classified as positive for profitability across the entire conference call (ALL sections) |
| 69 | `count_positive_valuation_answer` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of semantic chunks in the Answers section classified as positive for valuation |
| 70 | `count_positive_valuation_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of positive sentiment chunks about valuation in the presentation section of the conference call (USA, D1 delay) |
| 71 | `count_positive_valuation_question` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Number of chunks in the Q&A section classified as positive regarding valuation for the conference call |
| 72 | `count_positive_valuation_summary` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of chunks with positive sentiment related to valuation across the entire call (all sections) |
| 73 | `leverage_negative_score` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Negative probability score for leverage statements in the chunk |
| 74 | `leverage_neutral_score` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Neutral probability score for leverage statements in the chunk |
| 75 | `leverage_positive_score` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Positive probability score for leverage statements in the chunk |
| 76 | `leverage_sentiment_polarity` | VECTOR | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Signed net sentiment polarity for leverage in the chunk (approximately −1 to +1) |
| 77 | `mean_negative_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average negative probability score for asset utilization across the entire conference call (ALL sections) |
| 78 | `mean_negative_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average negative probability score for cash flow across the entire conference call (ALL sections) |
| 79 | `mean_negative_leverage_summary` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Average negative probability score for leverage across the entire conference call (ALL sections) |
| 80 | `mean_negative_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average negative probability score for profitability across the entire conference call (ALL sections) |
| 81 | `mean_negative_valuation_summary` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average negative sentiment score for valuation-related chunks across the entire call (all sections) |
| 82 | `mean_neutral_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average neutral probability score for asset utilization across the entire conference call (ALL sections) |
| 83 | `mean_neutral_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average neutral probability score for cash flow across the entire conference call (ALL sections) |
| 84 | `mean_neutral_leverage_summary` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average neutral sentiment score for leverage-related chunks across the entire call (all sections) |
| 85 | `mean_neutral_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average neutral probability score for profitability across the entire conference call (ALL sections) |
| 86 | `mean_neutral_valuation_summary` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Average neutral probability score for valuation across the entire conference call (ALL sections) |
| 87 | `mean_polarity_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for asset utilization across the entire conference call (ALL sections), D1-lag summary |
| 88 | `mean_polarity_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for cash flow across the entire conference call (ALL sections), D1-lag summary |
| 89 | `mean_polarity_leverage_summary` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average signed polarity score for leverage-related chunks across the entire conference call (ALL sections), D1-lag summary |
| 90 | `mean_polarity_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for profitability across chunks in the entire call (all sections) |
| 91 | `mean_polarity_valuation_summary` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average signed polarity score for valuation across the entire conference call (ALL sections), D1-lag summary |
| 92 | `mean_positive_assetutilization_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average positive probability score for asset utilization across the entire conference call (ALL sections) |
| 93 | `mean_positive_cashflow_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average positive probability score for cash flow across the entire conference call (ALL sections) |
| 94 | `mean_positive_leverage_summary` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average positive sentiment score for leverage-related chunks across the entire call (all sections) |
| 95 | `mean_positive_profitability_summary` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average positive probability score for profitability across the entire conference call (ALL sections) |
| 96 | `mean_positive_valuation_summary` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Average positive probability score for valuation across the entire conference call (ALL sections) |
| 97 | `presentation_chunk_count` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Total number of chunks in the presentation section of the conference call (USA, D1 delay) |
| 98 | `profitability_negative_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Negative probability score for profitability statements in the chunk |
| 99 | `profitability_neutral_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Neutral probability score for profitability statements in the chunk |
| 100 | `profitability_positive_score` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Positive probability score for profitability statements in the chunk |
| 101 | `profitability_sentiment_polarity` | VECTOR | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Signed net sentiment polarity for profitability in the chunk (approximately −1 to +1) |
| 102 | `question_chunk_count` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Total number of chunks in the Q&A section of the conference call |
| 103 | `summary_chunk_count` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Total number of semantic chunks in the conference call (ALL sections) for the event |
| 104 | `valuation_negative_score` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Negative probability score for valuation statements in the chunk |
| 105 | `valuation_neutral_score` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Neutral probability score for valuation statements in the chunk |
| 106 | `valuation_positive_score` | VECTOR | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Positive probability score for valuation statements in the chunk |
| 107 | `valuation_sentiment_polarity` | VECTOR | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Signed net sentiment polarity for valuation in the chunk (approximately −1 to +1) |
| 108 | `mean_negative_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of negative probability scores for asset utilization statements in the presentation section (USA, D1 delay) |
| 109 | `mean_negative_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of negative probability scores for cash flow statements in the presentation section (USA, D1 delay) |
| 110 | `mean_negative_leverage_presentation` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean of negative probability scores for leverage statements in the presentation section (USA, D1 delay) |
| 111 | `mean_negative_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of negative probability scores for profitability statements in the presentation section (USA, D1 delay) |
| 112 | `mean_negative_valuation_presentation` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean of negative probability scores for valuation statements in the presentation section (USA, D1 delay) |
| 113 | `mean_neutral_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of neutral probability scores for asset utilization statements in the presentation section (USA, D1 delay) |
| 114 | `mean_neutral_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of neutral probability scores for cash flow statements in the presentation section (USA, D1 delay) |
| 115 | `mean_neutral_leverage_presentation` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean of neutral probability scores for leverage statements in the presentation section (USA, D1 delay) |
| 116 | `mean_neutral_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean neutral sentiment intensity score for profitability across all chunks in the Presentation (P) section for the given stock-date (D1-lag) |
| 117 | `mean_neutral_valuation_presentation` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean of neutral probability scores for valuation statements in the presentation section (USA, D1 delay) |
| 118 | `mean_polarity_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for asset utilization statements in the presentation section (USA, D1 delay) |
| 119 | `mean_polarity_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for cash flow statements in the presentation section (USA, D1 delay) |
| 120 | `mean_polarity_leverage_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average signed polarity score (negative to positive) for leverage across all chunks in the Presentation (P) section for the given stock-date |
| 121 | `mean_polarity_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score (negative to positive) for profitability across all chunks in the Presentation (P) section for the given stock |
| 122 | `mean_polarity_valuation_presentation` | MATRIX | 0.511 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average signed polarity score (negative to positive) for valuation across all chunks in the Presentation (P) section for the given stock-dat |
| 123 | `mean_positive_assetutilization_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of positive probability scores for asset utilization statements in the presentation section (USA, D1 delay) |
| 124 | `mean_positive_cashflow_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of positive probability scores for cash flow statements in the presentation section (USA, D1 delay) |
| 125 | `mean_positive_leverage_presentation` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean of positive probability scores for leverage statements in the presentation section (USA, D1 delay) |
| 126 | `mean_positive_profitability_presentation` | MATRIX | 0.511 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of positive probability scores for profitability statements in the presentation section (USA, D1 delay) |
| 127 | `mean_positive_valuation_presentation` | MATRIX | 0.511 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean of positive probability scores for valuation statements in the presentation section (USA, D1 delay) |
| 128 | `mean_negative_assetutilization_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the negative sentiment probability scores for asset utilization-related statements in the Answers section |
| 129 | `mean_negative_cashflow_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the negative sentiment probability scores for cash flow-related statements in the Answers section |
| 130 | `mean_negative_leverage_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of the negative sentiment probability scores for leverage-related statements in the Answers section |
| 131 | `mean_negative_profitability_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the negative sentiment probability scores for profitability-related statements in the Answers section |
| 132 | `mean_negative_valuation_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of the negative sentiment probability scores for valuation-related statements in the Answers section |
| 133 | `mean_neutral_assetutilization_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the neutral sentiment probability scores for asset utilization-related statements in the Answers section |
| 134 | `mean_neutral_cashflow_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the neutral sentiment probability scores for cash flow-related statements in the Answers section |
| 135 | `mean_neutral_leverage_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average neutral sentiment magnitude for leverage-related content in the Answers section of the conference call (per stock-date event, D1 del |
| 136 | `mean_neutral_profitability_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the neutral sentiment probability scores for profitability-related statements in the Answers section |
| 137 | `mean_neutral_valuation_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of the neutral sentiment probability scores for valuation-related statements in the Answers section |
| 138 | `mean_polarity_assetutilization_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for asset utilization–related statements in the Answers section of the conference call |
| 139 | `mean_polarity_cashflow_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for cash flow–related statements in the Answers section of the conference call |
| 140 | `mean_polarity_leverage_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average signed polarity score for leverage-related statements in the Answers section of the conference call |
| 141 | `mean_polarity_profitability_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average signed polarity score for profitability-related statements in the Answers section of the conference call |
| 142 | `mean_polarity_valuation_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average signed polarity score for valuation-related content in the Answers section |
| 143 | `mean_positive_assetutilization_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the positive sentiment probability scores for asset utilization-related statements in the Answers section |
| 144 | `mean_positive_cashflow_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the positive sentiment probability scores for cash flow-related statements in the Answers section |
| 145 | `mean_positive_leverage_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of the positive sentiment probability scores for leverage-related statements in the Answers section |
| 146 | `mean_positive_profitability_answer` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the positive sentiment probability scores for profitability-related statements in the Answers section |
| 147 | `mean_positive_valuation_answer` | MATRIX | 0.502 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average positive sentiment magnitude for valuation-related content in the Answers section of the conference call (per stock-date event, D1 d |
| 148 | `mean_negative_assetutilization_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level negative sentiment probability scores for asset utilization-related content in the Q&A section of the conference call |
| 149 | `mean_negative_cashflow_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average negative sentiment score for cash flow-related content in the Q&A section of the conference call (USA, D1 lag) |
| 150 | `mean_negative_leverage_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level negative sentiment probability scores for leverage-related content in the Q&A section of the conference call |
| 151 | `mean_negative_profitability_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level negative sentiment probability scores for profitability-related content in the Q&A section of the conference call |
| 152 | `mean_negative_valuation_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level negative sentiment probability scores for valuation-related content in the Q&A section of the conference call |
| 153 | `mean_neutral_assetutilization_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level neutral sentiment probability scores for asset utilization-related content in the Q&A section of the conference call |
| 154 | `mean_neutral_cashflow_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean neutral probability score for cash flow-related chunks in the Q&A section of the conference call |
| 155 | `mean_neutral_leverage_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level neutral sentiment probability scores for leverage-related content in the Q&A section of the conference call |
| 156 | `mean_neutral_profitability_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean neutral probability score for profitability-related chunks in the Q&A section of the conference call |
| 157 | `mean_neutral_valuation_question` | MATRIX | 0.476 | 风险与质量 | 0 | — | — | — | UNUSABLE | Mean neutral probability score for valuation-related chunks in the Q&A section of the conference call |
| 158 | `mean_polarity_assetutilization_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level signed polarity scores (negative to positive) for asset utilization-related content in the Q&A section of the confere |
| 159 | `mean_polarity_cashflow_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level signed polarity scores (negative to positive) for cash flow-related content in the Q&A section of the conference call |
| 160 | `mean_polarity_leverage_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level signed polarity scores (negative to positive) for leverage-related content in the Q&A section of the conference call |
| 161 | `mean_polarity_profitability_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level signed polarity scores (negative to positive) for profitability-related content in the Q&A section of the conference  |
| 162 | `mean_polarity_valuation_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level signed polarity scores (negative to positive) for valuation-related content in the Q&A section of the conference call |
| 163 | `mean_positive_assetutilization_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level positive sentiment probability scores for asset utilization-related content in the Q&A section of the conference call |
| 164 | `mean_positive_cashflow_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level positive sentiment probability scores for cash flow-related content in the Q&A section of the conference call |
| 165 | `mean_positive_leverage_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level positive sentiment probability scores for leverage-related content in the Q&A section of the conference call |
| 166 | `mean_positive_profitability_question` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of chunk-level positive sentiment probability scores for profitability-related content in the Q&A section of the conference call |
| 167 | `mean_positive_valuation_question` | MATRIX | 0.476 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average of chunk-level positive sentiment probability scores for valuation-related content in the Q&A section of the conference call |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

