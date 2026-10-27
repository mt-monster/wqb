# socialmedia12 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `socialmedia12` |
| 名称 | Sentiment Data for Equity |
| 类别 | SOCIALMEDIA |
| 数据字段数(平台) | 6 |
| 覆盖率 | 0.7836 |
| 平台已有 alpha | 1079 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset aggregates and analyzes social media posts and news articles related to financial markets, covering thousands of sources and several years of historical data. It quantifies market sentiment and buzz for individual assets, sectors, and indices using advanced natural language processing and machine learning techniques. The data includes sentiment scores, buzz indicators, and trading signals, which are statistically validated and can be used to identify shifts in market mood, anticipate volatility, and generate actionable buy/sell signals. By monitoring real-time and historical sentiment, traders and analysts can enhance their price movement predictions and improve portfolio performance through timely, data-driven decisions.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **6** |
| 类型分布 | VECTOR×4　MATRIX×2 |
| 平均覆盖率 | **0.784** |
| 覆盖率区间 | 0.75 ~ 0.85 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 6 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 6 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 2 | 0.75 | entity_employee_count、entity_profile_summary |
| 价量与波动 | 1 | 0.85 | scl12_buzz |
| 情绪与新闻 | 1 | 0.85 | scl12_sentiment |
| 宏观与行业 | 1 | 0.75 | entity_sector_name |
| 盈利与财务 | 1 | 0.75 | entity_total_revenue |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `scl12_buzz` | MATRIX | 0.850 | 价量与波动 | 0 | — | — | — | UNTESTED | relative sentiment volume |
| 2 | `scl12_sentiment` | MATRIX | 0.850 | 情绪与新闻 | 0 | — | — | — | UNTESTED | sentiment |
| 3 | `entity_employee_count` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Number of employees in the entity (e.g., company, index, person) |
| 4 | `entity_profile_summary` | VECTOR | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Description of the company from snapshot data |
| 5 | `entity_sector_name` | VECTOR | 0.751 | 宏观与行业 | 0 | — | — | — | UNTESTED | Business sector or industry classification for the entity |
| 6 | `entity_total_revenue` | VECTOR | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue of the company |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

