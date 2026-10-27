# news76 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news76` |
| 名称 | Textual News Feed Data |
| 类别 | NEWS |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.7245 |
| 平台已有 alpha | 105 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Refinitiv Instrument Codes (RICs) and Bloomberg identifiers for equity securities. It enables users to cross-reference securities across two major financial data platforms, facilitating data integration, validation, and aggregation from multiple sources. While not directly predictive of price movements, this mapping is essential for researchers and analysts who need to merge datasets, ensure data consistency, and perform multi-source analytics, which can indirectly enhance the accuracy and breadth of quantitative models and trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | VECTOR×8 |
| 平均覆盖率 | **0.724** |
| 覆盖率区间 | 0.72 ~ 0.73 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 8 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 8 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 4 | 0.73 | mws76_classnum、mws76_confidence、mws76_score |
| 风险与质量 | 2 | 0.72 | company_analytics_previous_score、company_analytics_score_value |
| 元数据与非信号 | 1 | 0.73 | mws76_timeofarrival |
| 宏观与行业 | 1 | 0.73 | mws76_version |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mws76_classnum` | VECTOR | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Numeric classification label for the specified newswire or story |
| 2 | `mws76_confidence` | VECTOR | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-entity confidence values aligned with Score sentiment uses 0 to 100 MMN uses 0 to 1 probability of market move |
| 3 | `mws76_score` | VECTOR | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Per-entity analytics score array: sentiment uses -1 negative 0 neutral 1 positive; MMN and MMN_1STPASS are 1 for tagged entities |
| 4 | `mws76_timeofarrival` | VECTOR | 0.726 | 元数据与非信号 | 0 | — | — | — | UNTESTED | UTC timestamp when the story was first created in Bloomberg systems |
| 5 | `mws76_version` | VECTOR | 0.726 | 宏观与行业 | 0 | — | — | — | UNTESTED | Version number of the underlying analytics model used to generate the record |
| 6 | `news_story_title` | VECTOR | 0.726 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Story headline text subject to entitlements |
| 7 | `company_analytics_previous_score` | VECTOR | 0.719 | 风险与质量 | 0 | — | — | — | UNTESTED | Numeric value representing the previously assigned analytics score |
| 8 | `company_analytics_score_value` | VECTOR | 0.719 | 风险与质量 | 0 | — | — | — | UNTESTED | Deprecated analytics value field; always 0 and no longer used |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

