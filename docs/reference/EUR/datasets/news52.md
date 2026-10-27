# news52 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news52` |
| 名称 | Conference call data |
| 类别 | NEWS |
| 数据字段数(平台) | 24 |
| 覆盖率 | 0.4698 |
| 平台已有 alpha | 34 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a mapping between Bloomberg IDs (BBID) and Reuters Instrument Codes (RIC), facilitating cross-referencing of securities across major financial data platforms. It is essential for data integration, enabling seamless linking of market data, corporate actions, and analytics from Bloomberg and Refinitiv sources. While not directly predictive of price movements, it is a foundational resource for researchers and portfolio managers who require accurate and consistent security identifiers for multi-source data analysis, backtesting, and operational workflows.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **24** |
| 类型分布 | MATRIX×18　VECTOR×6 |
| 平均覆盖率 | **0.470** |
| 覆盖率区间 | 0.38 ~ 0.50 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 24 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 24 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 24 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 13 | 0.50 | mws52_chars_in_presentation、mws52_chars_in_qa、mws52_expirationtime |
| 搜索与替代数据 | 3 | 0.38 | mws52_occurence、mws52_occurence_presentation、mws52_occurence_qa |
| 持仓与资金流 | 3 | 0.38 | mws52_position、mws52_position_presentation、mws52_position_qa |
| 价量与波动 | 2 | 0.50 | mws52_questions_in_presentation、mws52_questions_in_qa |
| 修正与预期 | 1 | 0.50 | mws52_conference_call_participants |
| 宏观与行业 | 1 | 0.50 | mws52_corporate_participants |
| 盈利与财务 | 1 | 0.50 | mws52_eventtype |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mws52_chars_in_presentation` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of characters in the presentation section |
| 2 | `mws52_chars_in_qa` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of characters in the Q&A section |
| 3 | `mws52_conference_call_participants` | MATRIX | 0.498 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of non-corporate participants (analysts, third parties) in the conference call |
| 4 | `mws52_corporate_participants` | MATRIX | 0.498 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of representatives from the company (issuer) participating in the conference call |
| 5 | `mws52_eventtype` | MATRIX | 0.498 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Type/category of the conference call event (e.g., earnings call, guidance update, etc.) |
| 6 | `mws52_expirationtime` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Time when the event or record is considered expired or no longer current |
| 7 | `mws52_lastuptime` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Time when the record was last updated |
| 8 | `mws52_paragraphs_in_presentation` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of paragraphs in the presentation section of the conference call |
| 9 | `mws52_pparagraphs_in_qa` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of paragraphs in the Q&A section of the conference call |
| 10 | `mws52_questions_in_presentation` | MATRIX | 0.498 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of questions asked during the presentation section of the conference call |
| 11 | `mws52_questions_in_qa` | MATRIX | 0.498 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of questions asked in the Q&A section of the conference call |
| 12 | `mws52_sentences_in_presentation` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of sentences in the presentation section of the conference call |
| 13 | `mws52_sentences_in_qa` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of sentences in the Q&A section of the conference call |
| 14 | `mws52_starttime` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Time the conference call event started |
| 15 | `mws52_talks_in_presentation` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of talks (distinct speaker turns or interventions) in the presentation section of the conference call |
| 16 | `mws52_talks_in_qa` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of individual talks in the Q&A section of the conference call |
| 17 | `mws52_words_in_presentation` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of words in the presentation section of the conference call |
| 18 | `mws52_words_in_qa` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Number of words in the Q&A section of the conference call |
| 19 | `mws52_occurence` | VECTOR | 0.385 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Total number of times the keyword appeared in both the presentation and Q&A sections of the conference call |
| 20 | `mws52_occurence_presentation` | VECTOR | 0.385 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Number of times the keyword appeared specifically in the presentation section of the conference call |
| 21 | `mws52_occurence_qa` | VECTOR | 0.385 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Number of times the keyword appeared specifically in the Q&A section of the conference call |
| 22 | `mws52_position` | VECTOR | 0.383 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | List of absolute positions (indices) where each keyword appears across the entire conference call (including both presentation and Q&A secti |
| 23 | `mws52_position_presentation` | VECTOR | 0.383 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | List of absolute positions (indices) where the keyword appears specifically within the presentation section of the transcript |
| 24 | `mws52_position_qa` | VECTOR | 0.383 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | List of absolute positions (indices) where the keyword appears specifically within the Q&A section of the transcript |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

