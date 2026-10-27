# news29 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news29` |
| 名称 | Significant Developments Data |
| 类别 | NEWS |
| 数据字段数(平台) | 12 |
| 覆盖率 | 0.6888 |
| 平台已有 alpha | 68 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides concise, real-time summaries of major company news and market-moving events, systematically tagged by topic and significance. Covering a wide range of event types—such as mergers, acquisitions, product launches, regulatory actions, earnings guidance, and management changes—it enables users to filter out noise and focus on impactful developments. Each event is categorized by importance and topic, allowing for integration into quantitative models and historical trend analysis. By tracking and analyzing these significant corporate events, researchers and investors can better anticipate price movements, identify event-driven trading opportunities, and enhance alpha generation strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **12** |
| 类型分布 | VECTOR×12 |
| 平均覆盖率 | **0.693** |
| 覆盖率区间 | 0.30 ~ 0.77 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 10 | 83.3% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 2 | 16.7% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 7 | 58.3% |
| DEAD | 2 | 16.7% |
| UNUSABLE | 2 | 16.7% |
| DEAD_STATIC | 1 | 8.3% |

- 已实测字段：**3** 个（25%），best_sharpe 最高 **0.25**，中位 0.03

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 元数据与非信号 | 6 | 0.68 | event_tertiary_topic_code、nws29_topic1、event_secondary_topic_code |
| 情绪与新闻 | 4 | 0.77 | nws29_full_frontpage、company_event_headline_text_full、company_event_description_text_full |
| 其他 | 1 | 0.77 | nws29_significance |
| 搜索与替代数据 | 1 | 0.37 | nws29_topic2 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `nws29_full_frontpage` | VECTOR | 0.756 | 情绪与新闻 | 2 | 0.25 | 0.63 | 0.15 | DEAD | Binary indicator (1/0) for whether the event/news was featured on Reuters front page |
| 2 | `event_tertiary_topic_code` | VECTOR | 0.756 | 元数据与非信号 | 1 | 0.03 | 0.22 | 0.16 | DEAD | Third-level event topic/category code (integer), for further sub-classification, must decode |
| 3 | `company_event_headline_text_full` | VECTOR | 0.773 | 情绪与新闻 | 1 | 0.00 | — | — | DEAD_STATIC | The complete headline or summary text for a company event or news item. |
| 4 | `company_event_description_text_full` | VECTOR | 0.773 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The full narrative or detailed description of a company event or news story. |
| 5 | `nws29_frontpage` | VECTOR | 0.773 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Flag indicating if the news item was featured on a Reuters front-page story (1 = yes, 0 = no) |
| 6 | `nws29_significance` | VECTOR | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Level of importance for the development (1 = High, 2 = Medium, 3 = Low) |
| 7 | `nws29_topic1` | VECTOR | 0.773 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Main topic code or parent category of the development |
| 8 | `event_secondary_topic_code` | VECTOR | 0.756 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Code representing the second-tier subcategory of the event; must be decoded via overlay |
| 9 | `nws29_full_significance` | VECTOR | 0.756 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Event importance level code: High, Medium, Low relevance to market (must decode) |
| 10 | `nws29_full_topic1` | VECTOR | 0.756 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Code representing the main category of the event; must be decoded via overlay (e.g. M&A, regulatory, etc.) |
| 11 | `nws29_topic2` | VECTOR | 0.371 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second-tier topic code linked (mapped) to the parent topic |
| 12 | `company_event_structured_fields_full` | VECTOR | 0.296 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | All structured data fields and tags associated with a company event, including topics, codes, and attributes. |

## 六、本地回测证据

- 本地累计回测 **4** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `omLqLnoJ` | 0.25 | 0.12 | 0.63 | 0.15 | 0.19 | ["LOW_SHARPE | 244 | `group_count(vec_avg(nws29_full_frontpage), sector)` |
| `MPa7ab08` | 0.03 | 0.01 | 0.22 | 0.16 | 0.20 | ["LOW_SHARPE | 244 | `divide(vec_avg(event_tertiary_topic_code), add(vec_avg(event_secondary_topic_code), 1))` |
| `wpZjZ5Ql` | 0.00 | — | — | — | 0.00 | ["LOW_SHARPE | 244 | `group_neutralize(ts_kurtosis(divide(ts_backfill(vec_avg(company_event_headline_text_full),` |
| `KPN7NnJj` | -0.19 | -0.08 | -0.47 | 0.12 | 0.22 | ["LOW_SHARPE | 244 | `group_mean(vec_avg(nws29_full_frontpage), vec_avg(nws29_full_topic1), sector)` |

## 七、判死记录（sealed dead_end）

- `EUR-NEWS29-WEAK`（2026-09-23T18:56:06）family=news29 主题显著性族（nws29_topic/significance VECTOR）：{"family": "news29 主题显著性族（nws29_topic/significance VECTOR）", "reason": "wave244 4 探针全灭 best /sharpe/=0.25（另 4 条 group_rank 单位错误被隔离）→ fast_kill 判死。NEWS 族五集全灭。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:56:06", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

