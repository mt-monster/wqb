# model182 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model182` |
| 名称 | Geographic network based model |
| 类别 | MODEL |
| 数据字段数(平台) | 7 |
| 覆盖率 | 0.4381 |
| 平台已有 alpha | 1 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset contains daily momentum signals derived from networks of economically and fundamentally linked companies, spanning multiple regions and market segments. It combines seven distinct network-based momentum factors—such as business segment, geographic, analyst coverage, executive/board membership, innovation, supply chain, and shipping relationships—into a composite model using risk parity optimization. The resulting signals are designed to deliver stronger performance and lower downside risk than traditional price momentum, with demonstrated diversification benefits and high risk-adjusted returns. By capturing information spillovers and lead-lag effects across related firms, this dataset provides powerful predictive insights for systematic equity strategies, helping investors ide

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **7** |
| 类型分布 | VECTOR×7 |
| 平均覆盖率 | **0.438** |
| 覆盖率区间 | 0.44 ~ 0.44 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 7 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 7 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 7 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 3 | 0.44 | mdl182_geom_6m、mdl182_m6_msb、mdl182_omen |
| 修正与预期 | 2 | 0.44 | mdl182_ebmearningsrevision、mdl182_m6_mna |
| 宏观与行业 | 1 | 0.44 | mdl182_industry |
| 其他 | 1 | 0.44 | mdl182_mktcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl182_ebmearningsrevision` | VECTOR | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Momentum score based on key executive and board membership network, specifically related to earnings revision activity |
| 2 | `mdl182_geom_6m` | VECTOR | 0.438 | 价量与波动 | 0 | — | — | — | UNUSABLE | Geographic Momentum score, reflecting momentum linked to geographic exposures and co-movements over a 6-month lookback |
| 3 | `mdl182_industry` | VECTOR | 0.438 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Daily point-in-time sub-industry classification of the company, used for sector or industry groupings and neutralization purposes |
| 4 | `mdl182_m6_mna` | VECTOR | 0.438 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sell-side Analyst Network Momentum score, indicating momentum effects propagated via analyst linkages over a 6-month lookback |
| 5 | `mdl182_m6_msb` | VECTOR | 0.438 | 价量与波动 | 0 | — | — | — | UNUSABLE | Business Segment Momentum score, measuring momentum based on business segment linkages over a 6-month lookback |
| 6 | `mdl182_mktcap` | VECTOR | 0.438 | 其他 | 0 | — | — | — | UNUSABLE | Market capitalization of the company in USD |
| 7 | `mdl182_omen` | VECTOR | 0.438 | 价量与波动 | 0 | — | — | — | UNUSABLE | Composite network momentum score that combines multiple network-based momentum sub-factors for the company |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

