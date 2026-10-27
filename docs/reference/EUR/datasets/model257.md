# model257 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model257` |
| 名称 | International sentiment analysis NLP model |
| 类别 | MODEL |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.323 |
| 平台已有 alpha | 5 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages advanced natural language processing and machine learning techniques to extract sentiment and behavioral signals from global corporate filings, including annual and interim reports, management discussions, and risk disclosures. By analyzing textual data across multiple regions and languages, it generates predictive scores and similarity metrics that can be used to identify potential stock selection opportunities. The dataset’s breadth and depth enable investors to detect shifts in management tone, risk outlook, and strategic direction, which are often precursors to price movements. Its integration of deep learning models and multilingual sentiment dictionaries makes it a powerful tool for forecasting returns and enhancing portfolio diversification.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | MATRIX×8 |
| 平均覆盖率 | **0.323** |
| 覆盖率区间 | 0.18 ~ 0.40 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 8 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 8 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 8 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 4 | 0.35 | mdl257_eu_score、mdl257_lm_nnc、mdl257_eu_lm_nnc |
| 其他 | 2 | 0.24 | annual_report_language_similarity_eu、interim_filing_language_similarity_eu |
| 盈利与财务 | 1 | 0.40 | mdl257_eu_sentiment_ml |
| 情绪与新闻 | 1 | 0.32 | mdl257_sentiment_ml |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl257_eu_score` | MATRIX | 0.398 | 风险与质量 | 0 | — | — | — | UNUSABLE | Composite GINA alpha score for the security, capturing various qualitative and quantitative factors as modeled by Wolfe's process |
| 2 | `mdl257_eu_sentiment_ml` | MATRIX | 0.398 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Machine learning-based sentiment score derived from analysis of regulatory filings and behavioral features |
| 3 | `mdl257_lm_nnc` | MATRIX | 0.336 | 风险与质量 | 0 | — | — | — | UNUSABLE | CNN ML model score |
| 4 | `mdl257_eu_lm_nnc` | MATRIX | 0.335 | 风险与质量 | 0 | — | — | — | UNUSABLE | Score derived from convolutional neural network models trained on annual regulatory reports |
| 5 | `mdl257_score` | MATRIX | 0.321 | 风险与质量 | 0 | — | — | — | UNUSABLE | GINA model score |
| 6 | `mdl257_sentiment_ml` | MATRIX | 0.321 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment model score |
| 7 | `annual_report_language_similarity_eu` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Year-over-year textual similarity metric for companies' annual reports, measuring changes or stability in language/content |
| 8 | `interim_filing_language_similarity_eu` | MATRIX | 0.176 | 其他 | 0 | — | — | — | UNUSABLE | Year-over-year textual similarity metric for consecutive interim (quarterly or half-year) regulatory filings of a company, used to assess th |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

