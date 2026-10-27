# news46 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news46` |
| 名称 | Relevant News Analytics Data |
| 类别 | NEWS |
| 数据字段数(平台) | 30 |
| 覆盖率 | 0.9382 |
| 平台已有 alpha | 256 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg Identifiers (BBID) and Refinitiv Instrument Codes (RIC), enabling seamless cross-referencing of securities across Bloomberg and Refinitiv platforms. It is essential for integrating and reconciling data from multiple financial data vendors, supporting accurate security identification in research, trading, and portfolio management systems. While not directly predictive of price movements, this mapping is crucial for ensuring data integrity and consistency when combining datasets for quantitative analysis, backtesting, or multi-source signal generation.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **30** |
| 类型分布 | VECTOR×19　MATRIX×11 |
| 平均覆盖率 | **0.938** |
| 覆盖率区间 | 0.70 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 26 | 86.7% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 4 | 13.3% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 24 | 80.0% |
| DEAD | 6 | 20.0% |

- 已实测字段：**6** 个（20%），best_sharpe 最高 **1.04**，中位 0.13

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 16 | 0.89 | mws46_ravenpack_mean_ssc、mws46_ravenpack_sum_nip、mws46_ravenpack_mean_ens |
| 其他 | 6 | 0.98 | mws46_ravenpack_sum_story_count、mws46_ens_elapsed、mws46_g_ens_elapsed |
| 风险与质量 | 4 | 1.00 | mws46_elw、mws46_ens、mws46_g_ens |
| 元数据与非信号 | 2 | 1.00 | mws46_ens_key、mws46_ens_key_off |
| 宏观与行业 | 2 | 1.00 | mws46_mcr、mws46_mcv |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mws46_ravenpack_sum_story_count` | MATRIX | 0.908 | 其他 | 3 | 1.04 | — | — | DEAD | Sum of story counts over the aggregation window |
| 2 | `mws46_ravenpack_mean_ssc` | MATRIX | 0.908 | 情绪与新闻 | 6 | 0.42 | 0.96 | 0.72 | DEAD | Mean Composite Sentiment Score (0–100) summarizing the overall news tone for the entity by combining multiple sentiment |
| 3 | `mws46_ravenpack_sum_nip` | MATRIX | 0.908 | 情绪与新闻 | 1 | 0.13 | -0.66 | 0.14 | DEAD | A score (0-100) representing the expected market impact of a news flash over the subsequent two-hour period, varying by |
| 4 | `mws46_ravenpack_mean_ens` | MATRIX | 0.698 | 情绪与新闻 | 6 | -0.01 | -0.45 | 0.19 | DEAD | Mean Event Novelty Score (0–100) indicating how new or unique the news is within a 24-hour window across stories in the |
| 5 | `mws46_ravenpack_mean_nip` | MATRIX | 0.908 | 情绪与新闻 | 1 | -0.19 | 0.60 | -0.40 | DEAD | Mean News Impact Projections score (0–100) estimating the short-term market impact of associated news over the next two |
| 6 | `mws46_ravenpack_sum_relevance` | MATRIX | 0.908 | 情绪与新闻 | 1 | -0.25 | -1.86 | -0.39 | DEAD | A score (0-100) that reflects how strongly the entity is connected to the news story, with higher values showing higher |
| 7 | `mws46_elw` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Word and phrase detection score |
| 8 | `mws46_ens` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Event Novelty Score (0–100) measuring the uniqueness or freshness of the story |
| 9 | `mws46_ens_elapsed` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Elapsed time in milliseconds since the first story in the event novelty chain |
| 10 | `mws46_ens_key` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | An alphanumeric identifier that provides a way to chain or relate stories about the same categorized event for the same |
| 11 | `mws46_ens_key_off` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | An alphanumeric identifier that provides a way to chain or relate stories about the same categorized event for the same |
| 12 | `mws46_ess` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Event Sentiment Score (0–100) based on the tone of the news |
| 13 | `mws46_g_ens` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Global Event Novelty Score (0–100) indicating how new a story is within a 24-hour window across all providers |
| 14 | `mws46_g_ens_elapsed` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Elapsed time in milliseconds since the first story in the global novelty chain across providers |
| 15 | `mws46_mce` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Event information |
| 16 | `mws46_mcp` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Projections, corporate news score |
| 17 | `mws46_mcr` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reports on corporate actions score |
| 18 | `mws46_mcv` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Venture, corporate, mergers and acquisitions score |
| 19 | `mws46_news_type` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Type of news story (e.g., formal, rumor, opinion, legal), codebook-based |
| 20 | `mws46_nip` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News Impact Projections score (0–100) estimating market impact over the next two hours |
| 21 | `mws46_relevance` | VECTOR | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Relevance score (0–100) indicating the importance of the story to the entity |
| 22 | `mws46_ssc` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite Sentiment Score for the story or entity (0–100) |
| 23 | `mws46_story_count` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Story count |
| 24 | `mws46_story_index` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Story index |
| 25 | `mws46_time` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Publication time of the news story |
| 26 | `mws46_ravenpack_mean_relevance` | MATRIX | 0.908 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean relevance score (0–100) indicating how central the entity is to the news; 100 means the entity is a primary focus |
| 27 | `mws46_ravenpack_sum_ssc` | MATRIX | 0.908 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A composite sentiment score (0-100) for a news story, calculated by aggregating multiple sentiment analysis methods |
| 28 | `mws46_ravenpack_mean_ess` | MATRIX | 0.698 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean Event Sentiment Score (0–100) measuring news sentiment for the entity based on proxies sampled from news; values ab |
| 29 | `mws46_ravenpack_sum_ens` | MATRIX | 0.698 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A novelty score (0-100) indicating how "new" or original a news story is within a 24-hour time frame among a set of stor |
| 30 | `mws46_ravenpack_sum_ess` | MATRIX | 0.698 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular news sentiment score (0-100) indicating positive or negative financial/economic sentiment for a given entity, |

## 六、本地回测证据

- 本地累计回测 **15** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `KPNmK6ON` | 0.42 | 0.13 | 0.36 | 0.42 | 0.10 | ["LOW_SHARPE | 245 | `rank(ts_delta(ts_backfill(mws46_ravenpack_mean_ssc,252),252))` |
| `LLN5P6N9` | 0.33 | 0.10 | 0.96 | 0.72 | 0.08 | ["LOW_SHARPE | 245 | `subtract(rank(ts_backfill(mws46_ravenpack_mean_ssc,252)),rank(ts_backfill(mws46_ravenpack_` |
| `GrbWGOOG` | 0.13 | 0.02 | -0.66 | 0.14 | 0.08 | ["LOW_SHARPE | 257 | `trade_when(greater(mws46_ravenpack_sum_nip,0),rank(divide(mws46_ravenpack_sum_ssc,mws46_ra` |
| `j2AY6nKW` | 0.11 | 0.02 | -0.68 | 0.27 | 0.02 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ssc, 66), industry)` |
| `wpZQa5k6` | 0.10 | 0.02 | -0.95 | 0.30 | 0.02 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ssc, 66), subindustry)` |
| `omLo1v62` | -0.01 | 0.00 | -0.45 | 0.19 | 0.08 | ["LOW_SHARPE | 245 | `rank(ts_delta(ts_backfill(mws46_ravenpack_mean_ens,252),252))` |
| `58zEpL1X` | -0.03 | 0.00 | -0.81 | 0.03 | 0.03 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ens, 66), industry)` |
| `6XjdpRQL` | -0.04 | 0.00 | -1.06 | 0.01 | 0.03 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ens, 66), subindustry)` |
| `YPb1vNo6` | -0.10 | -0.02 | -0.64 | 0.16 | 0.04 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ssc, 22), subindustry)` |
| `kqoNPn6l` | -0.14 | -0.03 | -0.59 | 0.10 | 0.04 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ssc, 22), industry)` |
| `vRrOK9ra` | -0.19 | -0.04 | 0.60 | -0.40 | 0.08 | ["LOW_SHARPE | 245 | `subtract(rank(ts_backfill(mws46_ravenpack_mean_nip,252)),rank(ts_backfill(mws46_ravenpack_` |
| `omLENWWJ` | -0.25 | -0.13 | -1.86 | -0.39 | 0.10 | ["LOW_SHARPE | 257 | `trade_when(greater(mws46_ravenpack_sum_relevance,0),rank(divide(mws46_ravenpack_sum_ens,mw` |
| `O0NAGnjJ` | -0.39 | -0.13 | -0.80 | -0.23 | 0.05 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ens, 22), subindustry)` |
| `3qXopEOP` | -0.41 | -0.14 | -0.79 | -0.19 | 0.05 | ["LOW_SHARPE | 257 | `group_rank(ts_mean(mws46_ravenpack_mean_ens, 22), industry)` |
| `wpZ981Yd` | -0.46 | -0.15 | -1.04 | -0.54 | 0.06 | ["LOW_SHARPE | 245 | `subtract(rank(ts_backfill(mws46_ravenpack_mean_ens,252)),rank(ts_backfill(mws46_ravenpack_` |

## 七、判死记录（sealed dead_end）

- `EUR-W245-news46-mechanisms-D1`（2026-09-24T20:06:11）family=news46_cashless_news_mechanism_probe：{"family": "news46_cashless_news_mechanism_probe", "reason": "EUR TOPCS1600 D1 本轮5条概念原式 max S=0.42, max /S/=0.46; 无 S>=1.25 且 F>=0.8，停止本轮机制增强。仅封存所测机制，不宣称全数据集无效。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-24T20:06:11", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

