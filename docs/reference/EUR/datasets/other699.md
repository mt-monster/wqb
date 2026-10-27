# other699 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other699` |
| 名称 | Individual Investor Transactions Data |
| 类别 | OTHER |
| 数据字段数(平台) | 7 |
| 覆盖率 | 0.2732 |
| 平台已有 alpha | 246 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset captures detailed transaction-level activity from over 81,000 individual retail users, including actions such as opening, closing, and adjusting positions, as well as watchlist modifications. It includes granular information on trade execution, portfolio types, user engagement metrics, and asset identifiers, updated frequently to reflect real-time investor behavior. By analyzing patterns in retail trading flows, sector allocations, and geographic distributions, this dataset offers valuable insights into sentiment shifts and crowd-driven market dynamics, which can be leveraged to anticipate short-term price movements and identify emerging trends in equity markets.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **7** |
| 类型分布 | VECTOR×7 |
| 平均覆盖率 | **0.273** |
| 覆盖率区间 | 0.27 ~ 0.27 |
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
| 持仓与资金流 | 2 | 0.27 | oth699_newnumofshares、oth699_prevnumofshares |
| 其他 | 2 | 0.27 | oth699_priordistincttradingdays、oth699_priortransactionnumber |
| 宏观与行业 | 1 | 0.27 | oth699_aggsplitfactor |
| 风险与质量 | 1 | 0.27 | oth699_executiontimestamp |
| 价量与波动 | 1 | 0.27 | oth699_sharestraded |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth699_aggsplitfactor` | VECTOR | 0.273 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Aggregate split adjustment factor applied to share counts to reflect corporate actions |
| 2 | `oth699_executiontimestamp` | VECTOR | 0.273 | 风险与质量 | 0 | — | — | — | UNUSABLE | Timestamp when TipRanks recorded/logged the event (YYYYMMDDhhmmss, UTC) |
| 3 | `oth699_newnumofshares` | VECTOR | 0.273 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Shares held in the position after the transaction, split‑adjusted in V2 |
| 4 | `oth699_prevnumofshares` | VECTOR | 0.273 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Shares held in the position before the transaction, split‑adjusted in V2 |
| 5 | `oth699_priordistincttradingdays` | VECTOR | 0.273 | 其他 | 0 | — | — | — | UNUSABLE | Number of distinct prior trading days with user transactions before this event |
| 6 | `oth699_priortransactionnumber` | VECTOR | 0.273 | 其他 | 0 | — | — | — | UNUSABLE | Count of transactions the user made before this event in the portfolio |
| 7 | `oth699_sharestraded` | VECTOR | 0.273 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of shares transacted in the event (positive buy, negative sell; split-adjusted) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

