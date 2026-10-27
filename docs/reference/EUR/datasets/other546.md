# other546 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other546` |
| 名称 | Institutional Network Analysis Dataset |
| 类别 | OTHER |
| 数据字段数(平台) | 13 |
| 覆盖率 | 0.381 |
| 平台已有 alpha | 13 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive set of network-based momentum signals, constructed from multiple economic and textual networks such as business segments, geographic exposure, analyst coverage, executive links, patent innovation, supply chain, and shipping networks. Enhanced with natural language processing of company filings and EDGAR log-based relationships, the composite model aggregates these diverse factors using a risk parity approach. The resulting signals are designed to be less correlated with traditional momentum, offering improved risk-adjusted returns and lower drawdowns. This dataset is valuable for quantitative investors seeking to predict price movements by capturing complex inter-company relationships and alternative sources of momentum beyond price trends.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **13** |
| 类型分布 | VECTOR×13 |
| 平均覆盖率 | **0.381** |
| 覆盖率区间 | 0.30 ~ 0.43 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 13 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 13 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 13 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 7 | 0.38 | oth546_busnet_common、oth546_busnet_strength、oth546_executivenet_common |
| 修正与预期 | 3 | 0.43 | oth546_analystnet_common、oth546_from_analyst、oth546_to_analyst |
| 风险与质量 | 2 | 0.33 | oth546_risknet_strength、oth546_mdanet_strength |
| 情绪与新闻 | 1 | 0.33 | oth546_nlpbusnet_strength |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth546_busnet_common` | VECTOR | 0.433 | 其他 | 0 | — | — | — | UNUSABLE | Count of business or geographic segments that are shared between the two companies |
| 2 | `oth546_busnet_strength` | VECTOR | 0.433 | 其他 | 0 | — | — | — | UNUSABLE | Correlation metric quantifying similarity in business segment reporting between the two companies in the pair |
| 3 | `oth546_analystnet_common` | VECTOR | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts that cover both the primary and peer company (shared analyst coverage) |
| 4 | `oth546_from_analyst` | VECTOR | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts covering the primary company |
| 5 | `oth546_to_analyst` | VECTOR | 0.429 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analysts covering the peer (secondary) company |
| 6 | `oth546_executivenet_common` | VECTOR | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Number of executives and board members (current or former) shared between the primary and peer companies |
| 7 | `oth546_from_freq` | VECTOR | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Number of executives and board members associated with the primary company |
| 8 | `oth546_qerf_ot` | VECTOR | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Number of executives and board members associated with the peer company |
| 9 | `oth546_nlpbusnet_strength` | VECTOR | 0.329 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Textual similarity score between the business section filings of the two companies, reflecting how closely related they are based on NLP ana |
| 10 | `oth546_risknet_strength` | VECTOR | 0.329 | 风险与质量 | 0 | — | — | — | UNUSABLE | Similarity score or correlation of Risk Factor section text between the primary and peer companies, indicating how similar their disclosed r |
| 11 | `oth546_mdanet_strength` | VECTOR | 0.328 | 风险与质量 | 0 | — | — | — | UNUSABLE | Similarity score based on Management Discussion & Analysis (MD&A) filing text, indicating business operation similarity between the two comp |
| 12 | `oth546_geonet_common` | VECTOR | 0.304 | 其他 | 0 | — | — | — | UNUSABLE | Number of shared geographic segments between primary and peer companies |
| 13 | `oth546_geonet_strength` | VECTOR | 0.304 | 其他 | 0 | — | — | — | UNUSABLE | Correlation measure between geographic segment presence vectors of the two companies; reflects geographic similarity |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

