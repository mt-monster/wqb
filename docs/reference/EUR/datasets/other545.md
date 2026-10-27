# other545 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other545` |
| 名称 | Linked Firms Momentum Data |
| 类别 | OTHER |
| 数据字段数(平台) | 4 |
| 覆盖率 | 0.5424 |
| 平台已有 alpha | 14 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive set of network-based momentum signals for global equities, combining traditional price momentum with advanced network analytics derived from business segments, geographic regions, analyst coverage, executive connections, innovation linkages, supply chain, and shipping data. The model leverages natural language processing on regulatory filings to identify economic linkages between companies, enhancing the predictive power and diversification of momentum strategies. By integrating multiple uncorrelated momentum factors and optimizing risk allocation, the dataset offers robust signals with higher risk-adjusted returns and lower drawdowns than conventional momentum approaches. Investors and analysts can use these insights to construct diversified portfolio

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **4** |
| 类型分布 | VECTOR×4 |
| 平均覆盖率 | **0.542** |
| 覆盖率区间 | 0.54 ~ 0.54 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 4 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 4 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 4 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 3 | 0.54 | oth545_mpd、oth545_pln_omen、oth545_score |
| 其他 | 1 | 0.54 | oth545_mktcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth545_mktcap` | VECTOR | 0.542 | 其他 | 0 | — | — | — | UNUSABLE | Market capitalization of the company in US dollars |
| 2 | `oth545_mpd` | VECTOR | 0.542 | 价量与波动 | 0 | — | — | — | UNUSABLE | Score based on dynamic price momentum, capturing advanced or machine-learned price momentum of the stock |
| 3 | `oth545_pln_omen` | VECTOR | 0.542 | 价量与波动 | 0 | — | — | — | UNUSABLE | Score based on NLP-derived network momentum using text-mined linkages |
| 4 | `oth545_score` | VECTOR | 0.542 | 价量与波动 | 0 | — | — | — | UNUSABLE | Final composite NEMO 2.0 model score aggregated from seven network momentum signals |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

