---
name: brain-alpha-research-news-sentiment
layer: L1
description: "新闻/情绪类数据集研究：字段 5 家族分类、6 桶配对框架、Tier A 数据集组合。当任务涉及 news/sentiment 数据集挖掘、字段分类、6 桶框架或 Tier A 组合选集时使用。触发词：新闻数据集 / 情绪数据集 / 5 家族 / 6 桶 / Tier A。"
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究 — 新闻/情绪（News/Sentiment）

## 触发场景

本 skill 适用于：新闻/情绪数据集研究、字段分类、6 桶配对框架、Tier A 数据集组合选集。

## 工作流

### 1. 新闻/情绪 5 家族分类 + 6 桶框架（2026-04-23 起硬闸）

当目标数据集属于 `news`/`sentiment`/`socialmedia` 类别（或 id 以 `news`/`nws`/`sentiment`/`snt` 开头）时，用 [`src/wqb/research/news_field_classifier.py`](src/wqb/research/news_field_classifier.py) 把每个候选字段分到恰好一个家族：

(a) **direction（方向）** — 带符号的情绪/语气；
(b) **attention（关注度）** — relevance/volume/提及计数；
(c) **dispersion（分歧度）** — 标准差、新颖度、不确定性、分歧；
(d) **event_type（事件类型）** — 主题代码、显著性标记、交易类型、日内/头版标记；
(e) **peer_context（同侪上下文）** — 预聚合的同侪值。

关键词规则与逐数据集覆盖（news12/news29/news73/news94）在分类器模块内。分类法缓存于 `data/field_taxonomy/<region>_<dataset>.json`。

家族按 [`reference/news_bucket_field_map.md`](docs/reference/news_bucket_field_map.md) §4 配成 6 桶——**每批禁止 3 个字段同家族**，且 Event / Dispersion / Propagation 三桶是高优先三元组。

研究方向见 [`reference/news_sentiment_playbook.md`](docs/reference/news_sentiment_playbook.md)——描述的是动机与设计目标，不是公式。

覆盖 <0.4 的字段必须显式 `ts_backfill` / `group_backfill` 或直接弃用——裸用会产生 5-10 只股票集中持仓的 alpha，即使 IS 指标好看也会挂 CONCENTRATED_WEIGHT。

### 2. news12 数据集专项补充（2026-04-21）

news12 在 USA/D1 **没有语气/极性标量**——它是新闻事件驱动的价格反应微结构数据集（RavenPack 风格 `news_pct_*min`、`news_max_up/dn_ret`、`news_ton_last`、`news_vol_stddev` 等）。

通用五家族分类法适用但需重映射：
- R（反应）→ direction
- A（关注度/量）→ attention
- V（区间/波动上下文）→ dispersion
- M（微观结构/上下文）→ event_type（news12 无真正事件代码；用 `nws12_mainz_vol_ratio` / `atrratio` 作合成触发器）
- T（反应时长）→ event_type

完整 R/A/V/M/T 字段表见 [`reference/news.md`](docs/reference/news.md)。

合法配对桶遵循 6 桶框架——news12 的反应中心 motif（M1–M6）映射：M1/M3 → surprise，M2 → event，M4 → surprise 或 change，M5 → event，M6 → event。

### 3. Tier A 数据集组合核对（2026-04-23）

任何新闻类挖掘任务先查 [`reference/news_dataset_portfolio.md`](docs/reference/news_dataset_portfolio.md)。

冷启动任务路由到 Tier A（fieldCount ≥ 50 且 alphaCount/fieldCount ≤ 5 且 pyramidMultiplier ≥ 1.2）：
`news_transformer_scores` / `sentiment22` / `sentiment23` / `event_return_model` / `news94` / `news29` / `news73` / `news23` / `news59` / `creator_signal_perf` / `twitter_sentiment_l2`。

Tier B（`news12` 120K α、`news18` 40K α、`socialmedia12` 43K α）已饱和——挖掘前必须向用户标注，需要高度非对称结构才能压 ProdCorr < 0.70。

平台倍率变化时用 `wqb news-refresh-portfolio` 刷新组合。

## 验证清单

1. 确认字段分类使用 5 家族分类法。
2. 确认 6 桶框架生效（≥3 桶/批、≥1 HIGH、≥2 vec_op、shape_variety≥2）。
3. 确认冷启动任务优先路由 Tier A 数据集。
