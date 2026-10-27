# other553 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other553` |
| 名称 | Financial Opinion Mining |
| 类别 | SENTIMENT |
| 数据字段数(平台) | 73 |
| 覆盖率 | 0.5458 |
| 平台已有 alpha | 326 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.4 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset focuses on financial opinion mining from various text-based sources such as earnings calls, news, and social media. It aims to extract potential signals by performing deep analysis, considering financial characteristics and correlations among different data sources. The methodology involves advanced feature extraction, sentiment scoring using word embeddings, semi-supervised/transfer learning for adapting sentiment across data, and time-series value prediction through multi-source embedding. The dataset is designed to cover opinion mining tasks including sentiment analysis, company grouping, and value prediction, ultimately seeking to uncover valuable insights from the complete event timeline across diverse text data.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **73** |
| 类型分布 | VECTOR×40　MATRIX×33 |
| 平均覆盖率 | **0.546** |
| 覆盖率区间 | 0.27 ~ 0.97 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 10 | 13.7% |
| 中 (0.70–0.90) | 3 | 4.1% |
| 低 (0.50–0.70) | 24 | 32.9% |
| 稀疏 (<0.50) | 36 | 49.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 60 | 82.2% |
| UNTESTED | 13 | 17.8% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 13 / UNUSABLE 60 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 30 | 0.51 | oth553_horizon、oth553_p_avgsentlen、oth553_p_wordcnt |
| 修正与预期 | 23 | 0.62 | oth553_est_estvalue、oth553_est_analyst、oth553_sal_analyst |
| 价量与波动 | 6 | 0.60 | oth553_ptgvalue、oth553_preptgvalue、oth553_ptg_yearspeakcnt |
| 盈利与财务 | 6 | 0.45 | oth553_sal_question_ratio、oth553_sal_wordcnt、oth553_sal_answer_ratio |
| 情绪与新闻 | 5 | 0.49 | oth553_tncgen_p、oth553_tncgen_a、oth553_tncgen_q |
| 持仓与资金流 | 3 | 0.51 | oth553_p_avgnumericpos、oth553_a_avgnumericpos、oth553_q_avgnumericpos |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth553_est_estvalue` | VECTOR | 0.971 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of current estimates. |
| 2 | `oth553_est_analyst` | VECTOR | 0.971 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing estimates. |
| 3 | `oth553_sal_analyst` | VECTOR | 0.962 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing sales estimates. |
| 4 | `oth553_sal_estvalue` | VECTOR | 0.960 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of current sales estimates. |
| 5 | `oth553_est_preestvalue` | VECTOR | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of current estimates. |
| 6 | `oth553_sal_preestvalue` | VECTOR | 0.942 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of current sales estimates. |
| 7 | `oth553_horizon` | VECTOR | 0.934 | 其他 | 0 | — | — | — | UNTESTED | Time horizon for the data point. |
| 8 | `oth553_ptgvalue` | VECTOR | 0.934 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of the current price target. |
| 9 | `oth553_ptg_analyst` | VECTOR | 0.934 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing price target estimates. |
| 10 | `oth553_preptgvalue` | VECTOR | 0.915 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of the previous price target. |
| 11 | `oth553_recvalue` | VECTOR | 0.842 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the current recommendation. |
| 12 | `oth553_rec_analyst` | VECTOR | 0.840 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing recommendation estimates. |
| 13 | `oth553_prerecvalue` | VECTOR | 0.747 | 修正与预期 | 0 | — | — | — | UNTESTED | Value of the previous recommendation. |
| 14 | `oth553_p_avgsentlen` | MATRIX | 0.529 | 其他 | 0 | — | — | — | UNUSABLE | Average sentence length in financial text. |
| 15 | `oth553_p_wordcnt` | MATRIX | 0.529 | 其他 | 0 | — | — | — | UNUSABLE | Total word count in financial text. |
| 16 | `oth553_p_polycnt` | MATRIX | 0.529 | 其他 | 0 | — | — | — | UNUSABLE | Count of polysyllabic words in financial text. |
| 17 | `oth553_p_poscnt` | MATRIX | 0.529 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive terms in financial text. |
| 18 | `oth553_tncgen_p` | MATRIX | 0.529 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | General negative sentiment count. |
| 19 | `oth553_p_avgnumericpos` | MATRIX | 0.528 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Average numerical position in financial text. |
| 20 | `oth553_p_numericcnt` | MATRIX | 0.528 | 其他 | 0 | — | — | — | UNUSABLE | Count of numerical values in financial text. |
| 21 | `oth553_p_passiveratio` | MATRIX | 0.527 | 其他 | 0 | — | — | — | UNUSABLE | Ratio of passive voice in financial text. |
| 22 | `oth553_tncrecnu_p` | MATRIX | 0.526 | 其他 | 0 | — | — | — | UNUSABLE | Data field for financial opinion mining. |
| 23 | `oth553_a_avgsentlen` | MATRIX | 0.517 | 其他 | 0 | — | — | — | UNUSABLE | Average sentence length in financial text. |
| 24 | `oth553_a_wordcnt` | MATRIX | 0.517 | 其他 | 0 | — | — | — | UNUSABLE | Total word count in financial text. |
| 25 | `oth553_tncgen_a` | MATRIX | 0.517 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | General negative sentiment count. |
| 26 | `oth553_a_polycnt` | MATRIX | 0.517 | 其他 | 0 | — | — | — | UNUSABLE | Count of polysyllabic words in financial text. |
| 27 | `oth553_a_poscnt` | MATRIX | 0.517 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive terms in financial text. |
| 28 | `oth553_tncrecnu_a` | MATRIX | 0.516 | 其他 | 0 | — | — | — | UNUSABLE | Data field for financial opinion mining. |
| 29 | `oth553_a_avgnumericpos` | MATRIX | 0.515 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Average numerical position in financial text. |
| 30 | `oth553_a_numericcnt` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | Count of numerical values in financial text. |
| 31 | `oth553_p_blamecnt` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | Count of blame-related terms in financial text. |
| 32 | `oth553_a_passiveratio` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | Ratio of passive voice in financial text. |
| 33 | `oth553_est_yearspeakcnt` | VECTOR | 0.513 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of speeches related to estimates within the year. |
| 34 | `oth553_sal_yearspeakcnt` | VECTOR | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Count of speeches related to sales within the year. |
| 35 | `oth553_p_invblamecnt` | MATRIX | 0.503 | 其他 | 0 | — | — | — | UNUSABLE | Count of blame-related terms in financial text. |
| 36 | `oth553_q_avgsentlen` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Average sentence length in financial text. |
| 37 | `oth553_q_wordcnt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total word count in financial text. |
| 38 | `oth553_tncgen_q` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | General negative sentiment count. |
| 39 | `oth553_q_polycnt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Count of polysyllabic words in financial text. |
| 40 | `oth553_a_blamecnt` | MATRIX | 0.499 | 其他 | 0 | — | — | — | UNUSABLE | Count of blame-related terms in financial text. |
| 41 | `oth553_tncrecnu_q` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Data field for financial opinion mining. |
| 42 | `oth553_q_poscnt` | MATRIX | 0.498 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive terms in financial text. |
| 43 | `oth553_q_avgnumericpos` | MATRIX | 0.495 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Average numerical position in financial text. |
| 44 | `oth553_q_numericcnt` | MATRIX | 0.495 | 其他 | 0 | — | — | — | UNUSABLE | Count of numerical values in financial text. |
| 45 | `oth553_q_passiveratio` | MATRIX | 0.491 | 其他 | 0 | — | — | — | UNUSABLE | Ratio of passive voice in financial text. |
| 46 | `oth553_ptg_yearspeakcnt` | VECTOR | 0.475 | 价量与波动 | 0 | — | — | — | UNUSABLE | Count of speeches related to price targets within the year. |
| 47 | `oth553_est_isprevspeak` | VECTOR | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Indicator if there was previous speech related to estimates. |
| 48 | `oth553_est_question_ratio` | VECTOR | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of questions in earnings call transcripts related to estimates. |
| 49 | `oth553_est_wordcnt` | VECTOR | 0.473 | 修正与预期 | 0 | — | — | — | UNUSABLE | Word count in earnings call transcripts related to estimates. |
| 50 | `oth553_est_tncgen` | VECTOR | 0.472 | 修正与预期 | 0 | — | — | — | UNUSABLE | Negative sentiment count related to estimates. |
| 51 | `oth553_est_answer_ratio` | VECTOR | 0.469 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of answers in earnings call transcripts related to estimates. |
| 52 | `oth553_sal_isprevspeak` | VECTOR | 0.467 | 其他 | 0 | — | — | — | UNUSABLE | Indicator if there was previous speech related to sales. |
| 53 | `oth553_sal_question_ratio` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of questions in earnings call transcripts related to sales. |
| 54 | `oth553_sal_wordcnt` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Word count in earnings call transcripts related to sales. |
| 55 | `oth553_sal_tncgen` | VECTOR | 0.466 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment count related to sales. |
| 56 | `oth553_a_invblamecnt` | MATRIX | 0.466 | 其他 | 0 | — | — | — | UNUSABLE | Count of blame-related terms in financial text. |
| 57 | `oth553_sal_answer_ratio` | VECTOR | 0.463 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of answers in earnings call transcripts related to sales. |
| 58 | `oth553_est_poscnt` | VECTOR | 0.463 | 修正与预期 | 0 | — | — | — | UNUSABLE | Positive sentiment count related to estimates. |
| 59 | `oth553_sal_poscnt` | VECTOR | 0.457 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment count related to sales. |
| 60 | `oth553_ptg_isprevspeak` | VECTOR | 0.426 | 价量与波动 | 0 | — | — | — | UNUSABLE | Indicator if there was previous speech related to price targets. |
| 61 | `oth553_ptg_question_ratio` | VECTOR | 0.426 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of questions in earnings call transcripts related to price targets. |
| 62 | `oth553_ptg_wordcnt` | VECTOR | 0.426 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Word count in earnings call transcripts related to price targets. |
| 63 | `oth553_ptg_tncgen` | VECTOR | 0.425 | 价量与波动 | 0 | — | — | — | UNUSABLE | Negative sentiment count related to price targets. |
| 64 | `oth553_ptg_answer_ratio` | VECTOR | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of answers in earnings call transcripts related to price targets. |
| 65 | `oth553_q_blamecnt` | MATRIX | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Count of blame-related terms in financial text. |
| 66 | `oth553_ptg_poscnt` | VECTOR | 0.411 | 价量与波动 | 0 | — | — | — | UNUSABLE | Positive sentiment count related to price targets. |
| 67 | `oth553_rec_yearspeakcnt` | VECTOR | 0.351 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of speeches related to recommendations within the year. |
| 68 | `oth553_q_invblamecnt` | MATRIX | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Count of blame-related terms in financial text. |
| 69 | `oth553_rec_isprevspeak` | VECTOR | 0.274 | 修正与预期 | 0 | — | — | — | UNUSABLE | Indicator if there was previous speech related to recommendations. |
| 70 | `oth553_rec_question_ratio` | VECTOR | 0.274 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of questions in earnings call transcripts related to recommendations. |
| 71 | `oth553_rec_wordcnt` | VECTOR | 0.274 | 修正与预期 | 0 | — | — | — | UNUSABLE | Word count in earnings call transcripts related to recommendations. |
| 72 | `oth553_rec_tncgen` | VECTOR | 0.273 | 修正与预期 | 0 | — | — | — | UNUSABLE | Negative sentiment count related to recommendations. |
| 73 | `oth553_rec_answer_ratio` | VECTOR | 0.270 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of answers in earnings call transcripts related to recommendations. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-SNT26-ATTENTION-FITNESS-CEILING`（None）family=sentiment26 网站流行度/投资者注意力族：{"dataset": "sentiment26", "evidence": {"LL9d1JO9": "注意力水平 relpopularity08：S0.90/F0.45/2Y1.75 PASS/TVR0.0929/returns0.0319/longCount1061，仅 2 项 FAIL", "N1QRr0YE": "注意力广度动量 totaldomains：S0.09 无信号", "ZY0Kn563": "top10% 集中度：S-0.84（镜像后 +0.84 仍不达线）"}, "math_proof": "turnover 0.0929 已低于公式下限 0.125，分母钉死 → Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.90*0.505 = 0.455，实测 0.45 已贴天花板。即使 Sharpe 达 1.

