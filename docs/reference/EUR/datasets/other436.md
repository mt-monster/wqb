# other436 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other436` |
| 名称 | Dividend model |
| 类别 | OTHER |
| 数据字段数(平台) | 3 |
| 覆盖率 | 0.4461 |
| 平台已有 alpha | 72 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset identifies and predicts companies most likely to reduce, suspend, or terminate their dividend payments, focusing on so-called "dividend laggards." Leveraging a global factor library and machine learning algorithms, the model analyzes historical and real-time data to flag firms at risk of dividend cuts, which often precede significant share price declines and continued underperformance. By providing early warning signals on potential dividend reductions, the dataset is valuable for investors seeking to avoid downside risk, implement short strategies, or optimize portfolio yield, especially during periods of economic stress when dividend suspensions become more prevalent.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **3** |
| 类型分布 | VECTOR×3 |
| 平均覆盖率 | **0.446** |
| 覆盖率区间 | 0.45 ~ 0.45 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 3 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 3 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 3 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 2 | 0.45 | oth436_disc、oth436_divyld |
| 宏观与行业 | 1 | 0.45 | oth436_mktcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth436_disc` | VECTOR | 0.446 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Model output: predicted probability (between 0 and 1) that the company will cut, suspend, or terminate its dividend |
| 2 | `oth436_divyld` | VECTOR | 0.446 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividend yield for the company (likely annualized, may be trailing or forward; only available for updates) |
| 3 | `oth436_mktcap` | VECTOR | 0.446 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Market capitalization of the company (likely in USD or local currency, not explicitly defined) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

