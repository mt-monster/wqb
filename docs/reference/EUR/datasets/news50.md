# news50 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news50` |
| 名称 | Web News Analytics Data |
| 类别 | NEWS |
| 数据字段数(平台) | 37 |
| 覆盖率 | 0.8227 |
| 平台已有 alpha | 145 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Reuters Instrument Codes (RIC), facilitating cross-referencing of securities across Bloomberg and Refinitiv platforms. It is primarily used for data integration, enabling seamless linkage of market data, pricing, and analytics from different vendors. While not directly predictive of price movements, accurate identifier mapping is essential for consolidating datasets, ensuring data quality, and supporting multi-source quantitative research and trading strategies. This mapping is particularly valuable for portfolio managers, analysts, and data engineers who require reliable security identification for backtesting, risk analysis, and operational workflows.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **37** |
| 类型分布 | VECTOR×37 |
| 平均覆盖率 | **0.823** |
| 覆盖率区间 | 0.78 ~ 0.92 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 11 | 29.7% |
| 中 (0.70–0.90) | 26 | 70.3% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 36 | 97.3% |
| DEAD | 1 | 2.7% |

- 已实测字段：**1** 个（3%），best_sharpe 最高 **-0.42**，中位 -0.42

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 13 | 0.80 | mws50_category、mws50_acb、mws50_bam |
| 其他 | 9 | 0.87 | mws50_product_key、mws50_evaluation_method、mws50_type |
| 风险与质量 | 4 | 0.79 | mws50_aes、mws50_ens、mws50_g_ens |
| 元数据与非信号 | 3 | 0.87 | mws50_ens_key、mws50_g_ens_key、mws50_time |
| 盈利与财务 | 3 | 0.83 | mws50_maturity、mws50_bee、mws50_ber |
| 修正与预期 | 1 | 0.79 | mws50_ghc_lna |
| 搜索与替代数据 | 1 | 0.91 | mws50_property |
| 宏观与行业 | 1 | 0.79 | mws50_country_code |
| 持仓与资金流 | 1 | 0.79 | mws50_rp_story_event_index |
| 价量与波动 | 1 | 0.79 | mws50_vea |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mws50_ghc_lna` | VECTOR | 0.786 | 修正与预期 | 1 | -0.42 | -1.19 | -0.58 | DEAD | Score representing changes in analyst recommendations |
| 2 | `mws50_product_key` | VECTOR | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Identifies which subscription package contains the record |
| 3 | `mws50_category` | VECTOR | 0.908 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A unique tag to label, identify, and recognize a particular type and property of an entity-specific news event |
| 4 | `mws50_ens_key` | VECTOR | 0.908 | 元数据与非信号 | 0 | — | — | — | UNTESTED | An alphanumeric identifier that provides a way to chain or relate stories about the same categorized event for the same |
| 5 | `mws50_evaluation_method` | VECTOR | 0.908 | 其他 | 0 | — | — | — | UNTESTED | A period of time used to measure changes from previous levels in an event. |
| 6 | `mws50_g_ens_key` | VECTOR | 0.908 | 元数据与非信号 | 0 | — | — | — | UNTESTED | An alphanumeric identifier that provides a way to chain or relate stories about the same categorized event for the same |
| 7 | `mws50_maturity` | VECTOR | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | For events related to debt, this named attribute indicates the period of time for which a financial instrument remains o |
| 8 | `mws50_property` | VECTOR | 0.908 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | A named attribute of an event such as an entity, role, or string extracted from a matched event type. When applicable, t |
| 9 | `mws50_type` | VECTOR | 0.908 | 其他 | 0 | — | — | — | UNTESTED | A class of events, the constituents of which share similar characteristics |
| 10 | `mws50_sub_type` | VECTOR | 0.908 | 其他 | 0 | — | — | — | UNTESTED | A subdivision of a particular class of events |
| 11 | `mws50_group` | VECTOR | 0.908 | 其他 | 0 | — | — | — | UNTESTED | A collection of related events. |
| 12 | `mws50_topic` | VECTOR | 0.905 | 其他 | 0 | — | — | — | UNTESTED | A subject or theme of events detected |
| 13 | `mws50_acb` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score representing sentiment according to the corporate actions classifier |
| 14 | `mws50_aes` | VECTOR | 0.786 | 风险与质量 | 0 | — | — | — | UNTESTED | Score from 0 to 100 measuring the ratio of positive to total non-neutral events over a rolling 91-day window within the |
| 15 | `mws50_bam` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score representing sentiment according to the mergers and acquisitions classifier |
| 16 | `mws50_bee` | VECTOR | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings evaluations sentiment score from the BEE classifier |
| 17 | `mws50_ber` | VECTOR | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings releases sentiment score from the BER classifier specialized in earnings release news |
| 18 | `mws50_country_code` | VECTOR | 0.786 | 宏观与行业 | 0 | — | — | — | UNTESTED | Two-character ISO-3166 country code associated with the entity (companies by incorporation, currencies by central bank; |
| 19 | `mws50_ens` | VECTOR | 0.786 | 风险与质量 | 0 | — | — | — | UNTESTED | Event Novelty Score (0–100) indicating how new the story is within a 24-hour window for this package |
| 20 | `mws50_ens_elapsed` | VECTOR | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Milliseconds elapsed between the first story and the current story within the event novelty chain for this package (firs |
| 21 | `mws50_ens_similarity_gap` | VECTOR | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Number of days since a similar story was detected in this RPNA edition, from 0.00000 to 100.00000 where 100.00000 means |
| 22 | `mws50_ess` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Granular sentiment score from 0 to 100 for the entity in the story; higher values indicate more positive short-term fina |
| 23 | `mws50_g_ens` | VECTOR | 0.786 | 风险与质量 | 0 | — | — | — | UNTESTED | Global event novelty score from 0 to 100 indicating how new the story is within a 24 hour window across providers |
| 24 | `mws50_g_ens_elapsed` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Milliseconds elapsed between the first and current story in the global event novelty chain across all news providers |
| 25 | `mws50_g_ens_similarity_gap` | VECTOR | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Number of days since a similar story was detected across all product editions |
| 26 | `mws50_news_type` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Code classifying the type of news story or document (e.g., news, press release), per module codebook |
| 27 | `mws50_nip` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News Impact Projections score (0–100) estimating market impact over the following two hours, conditional on time of arri |
| 28 | `mws50_qcm` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Multi-classifier for equities sentiment score combining outputs from BMQ, BEE, BCA, and ANL-CHG, applied to the most rel |
| 29 | `mws50_qep` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | PEQ classifier score for global equities sentiment based on words/phrases in the article |
| 30 | `mws50_qmb` | VECTOR | 0.786 | 风险与质量 | 0 | — | — | — | UNTESTED | Editorials & Commentary classifier score for the story (equities package) |
| 31 | `mws50_relevance` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score from 0 to 100 indicating how strongly the entity is related to the news story, with 100 meaning the entity plays a |
| 32 | `mws50_rp_story_event_count` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of entity records (events) published by RavenPack for the given news story |
| 33 | `mws50_rp_story_event_index` | VECTOR | 0.786 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ordinal position of the entity record within a story, less than or equal to RP_STORY_EVENT_COUNT |
| 34 | `mws50_ssc` | VECTOR | 0.786 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite sentiment score from 0 to 100 representing overall story sentiment |
| 35 | `mws50_time` | VECTOR | 0.786 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time component of the record timestamp |
| 36 | `mws50_vea` | VECTOR | 0.786 | 价量与波动 | 0 | — | — | — | UNTESTED | Aggregate Event Volume over the past 91 days for an entity, counting non-neutral events (ESS ≠ 50) from qualifying news |
| 37 | `mws50_position_name` | VECTOR | 0.777 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The position held by an individual within the entity involved in a specific news event. |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `O0NJ152b` | 0.32 | 0.08 | -0.74 | 0.26 | 0.04 | ["LOW_SHARPE | 246 | `group_rank(ts_backfill(vec_avg(mws50_aes),252),subindustry)` |
| `rKOd1rM9` | 0.31 | 0.08 | 1.05 | 0.25 | 0.07 | ["LOW_SHARPE | 246 | `trade_when(greater(ts_delta(ts_backfill(vec_avg(mws50_vea),252),252),0),rank(ts_backfill(v` |
| `RRbAJkoa` | 0.22 | 0.05 | 0.62 | -0.10 | 0.13 | ["LOW_SHARPE | 246 | `subtract(rank(ts_backfill(vec_avg(mws50_bee),252)),rank(ts_backfill(vec_avg(mws50_ber),252` |
| `WjbLEWxO` | 0.16 | 0.03 | -0.24 | 0.01 | 0.08 | ["LOW_SHARPE | 246 | `group_rank(ts_backfill(vec_avg(mws50_bam),252),subindustry)` |
| `kqoJxLY6` | 0.15 | 0.03 | 1.01 | 0.09 | 0.13 | ["LOW_SHARPE | 246 | `rank(ts_delta(ts_backfill(vec_avg(mws50_acb),252),252))` |
| `9qjEzA3x` | -0.42 | -0.14 | -1.19 | -0.58 | 0.09 | ["LOW_SHARPE | 246 | `subtract(rank(ts_backfill(vec_avg(mws50_ghc_lna),252)),rank(ts_backfill(vec_avg(mws50_ssc)` |
| `npdA1O5w` | -0.50 | -0.18 | -1.43 | -0.45 | 0.10 | ["LOW_SHARPE | 246 | `subtract(rank(ts_backfill(vec_avg(mws50_qcm),252)),rank(ts_backfill(vec_avg(mws50_ssc),252` |
| `e7b6lqZl` | -0.52 | -0.17 | 0.61 | -0.50 | 0.09 | ["LOW_SHARPE | 246 | `subtract(rank(ts_backfill(vec_avg(mws50_nip),252)),rank(ts_backfill(vec_avg(mws50_ess),252` |

## 七、判死记录（sealed dead_end）

- `EUR-W246-news50-mechanisms-D1`（2026-09-24T20:06:11）family=news50_cashless_news_mechanism_probe：{"family": "news50_cashless_news_mechanism_probe", "reason": "EUR TOPCS1600 D1 本轮8条概念原式 max S=0.32, max /S/=0.52; 无 S>=1.25 且 F>=0.8，停止本轮机制增强。仅封存所测机制，不宣称全数据集无效。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-24T20:06:11", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

