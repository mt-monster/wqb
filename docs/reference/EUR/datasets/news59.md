# news59 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news59` |
| 名称 | Corporate Events Data |
| 类别 | NEWS |
| 数据字段数(平台) | 2 |
| 覆盖率 | 0.9505 |
| 平台已有 alpha | 62 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides concise, near real-time summaries of significant, market-moving company news events, intelligently tagged by topic and significance. Covering a wide range of event types—such as M&A, product launches, regulatory actions, earnings guidance, officer changes, and more—it filters out noise to focus on developments most likely to impact market prices. Each event is categorized by importance and topic, enabling integration into quantitative models and event-driven strategies. The dataset’s structured, timely, and comprehensive coverage of major corporate events makes it a valuable resource for predicting price movements and conducting event studies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **2** |
| 类型分布 | VECTOR×2 |
| 平均覆盖率 | **0.951** |
| 覆盖率区间 | 0.95 ~ 0.95 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 2 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 2 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 2 | 0.95 | mws59_event_fiscal_year、mws59_event_time_value |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mws59_event_fiscal_year` | VECTOR | 0.951 | 其他 | 0 | — | — | — | UNTESTED | Fiscal year in which the event takes place |
| 2 | `mws59_event_time_value` | VECTOR | 0.951 | 其他 | 0 | — | — | — | UNTESTED | Scheduled time of the event in UTC (if MarketTime is specified); integer value |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

