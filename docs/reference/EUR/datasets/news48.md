# news48 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news48` |
| 名称 | Global Media News Data |
| 类别 | NEWS |
| 数据字段数(平台) | 22 |
| 覆盖率 | 0.6326 |
| 平台已有 alpha | 28 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset analyzes over 100,000 daily press releases and regulatory disclosures from major global newswires and distribution networks. It provides structured event and sentiment scores, novelty and impact metrics, and detailed entity mapping for companies, sectors, and geographies. By quantifying the sentiment, novelty, and relevance of news events, the dataset enables investors and researchers to identify market-moving information, anticipate volatility, and generate alpha through event-driven and sentiment-based trading strategies. Its comprehensive coverage and real-time updates make it a valuable resource for predicting price movements based on the latest corporate and regulatory news.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **22** |
| 类型分布 | VECTOR×22 |
| 平均覆盖率 | **0.633** |
| 覆盖率区间 | 0.63 ~ 0.63 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 22 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 22 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 13 | 0.63 | nws48_acb、nws48_bam、nws48_ens |
| 其他 | 4 | 0.63 | nws48_ens_elapsed、nws48_g_ens_elapsed、nws48_g_ens_similarity_gap |
| 盈利与财务 | 3 | 0.63 | nws48_bee、nws48_ber、nws48_qmb |
| 风险与质量 | 1 | 0.63 | nws48_aes |
| 修正与预期 | 1 | 0.63 | nws48_ghc_lna |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `nws48_acb` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score representing news sentiment of a story focusing on corporate action announcements |
| 2 | `nws48_aes` | VECTOR | 0.633 | 风险与质量 | 0 | — | — | — | UNTESTED | Aggregate score (0-100) of positive event ratio vs. all non-neutral events for an entity over a 91-day rolling window |
| 3 | `nws48_bam` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score representing news sentiment for stories about venture activity, company events, mergers, acquisitions, and takeove |
| 4 | `nws48_bee` | VECTOR | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sentiment score for stories about earnings evaluations |
| 5 | `nws48_ber` | VECTOR | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score representing news sentiment specializing in earnings release announcements |
| 6 | `nws48_ens` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Event Novelty Score (0–100) representing how new or unique the news story is within a 24-hour window |
| 7 | `nws48_ens_elapsed` | VECTOR | 0.633 | 其他 | 0 | — | — | — | UNTESTED | Number of milliseconds between the first and current story in an event novelty chain |
| 8 | `nws48_ens_similarity_gap` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of days since a similar story was detected; measures time gap between current news and last similar event |
| 9 | `nws48_ess` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Event Sentiment Score: score (0-100) measuring news sentiment for an entity in the story, higher is more positive |
| 10 | `nws48_g_ens` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global Event Novelty Score (0–100) across all providers, measuring how "new" a news story is within a 24-hour window |
| 11 | `nws48_g_ens_elapsed` | VECTOR | 0.633 | 其他 | 0 | — | — | — | UNTESTED | Number of milliseconds between the first and current story in a global event novelty chain |
| 12 | `nws48_g_ens_similarity_gap` | VECTOR | 0.633 | 其他 | 0 | — | — | — | UNTESTED | Number of days since the last similar globally-detected story; measures time gap between globally similar events |
| 13 | `nws48_ghc_lna` | VECTOR | 0.633 | 修正与预期 | 0 | — | — | — | UNTESTED | Numerical score representing analyst recommendation changes |
| 14 | `nws48_nip` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score (0–100) quantifying projected market impact of a news flash over the next two hours |
| 15 | `nws48_qcm` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Multi-classifier sentiment score for equities, reflecting aggregate tone for the most relevant companies in the story |
| 16 | `nws48_qep` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score representing sentiment in global equities news, specializing in positive and negative identification |
| 17 | `nws48_qmb` | VECTOR | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score representing sentiment for editorials/commentaries specifically on equity markets |
| 18 | `nws48_relevance` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score (0-100) indicating how strongly related the entity is to the news story, with higher values showing greater releva |
| 19 | `nws48_rp_story_event_count` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the total entity records published per news story; essentially, the number of distinct entities involved in t |
| 20 | `nws48_rp_story_event_index` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Order of the entity record within a news story, shows the position of the entity |
| 21 | `nws48_ssc` | VECTOR | 0.633 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment score between 0 and 100 representing the overall sentiment of the news story |
| 22 | `nws48_vea` | VECTOR | 0.633 | 其他 | 0 | — | — | — | UNTESTED | Count of non-neutral events for an entity over a 91-day rolling window |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS48-INSPECT-GATE-WALL`（2026-09-23T18:56:06）family=news48 ENS 情绪分族：{"family": "news48 ENS 情绪分族", "reason": "news48 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pregate 修复前无供给。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:56:06", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

