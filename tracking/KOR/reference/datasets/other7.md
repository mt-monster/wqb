# other7 — Archive News Data / Benzinga 新闻微观结构（KOR / TOP600 / D1）

> 画像：2026-11-17 · `get_datafields(dataset_id=other7, region=KOR, universe=TOP600, delay=1, filter_sharpe=false, 不传 max_fields)`。
> 三重对账：`count=11 == platform_count=11`，`complete=true`。全字段 11/11。
> 归属：平台 `category=news`（**未点亮塔**），但 `id` 前缀 other → 记 `category=news` 归类；与 SOP 附录「OTHER 禁内部组腿」无关（本集不与其它 OTHER 集组腿）。

## 1. 字段全表（11 个，全 VECTOR，coverage 全 0.2938）

| 字段 | aC | description / 机制 |
|---|---:|---|
| `oth7_prob_pos` | 3 | 新闻情绪为正的概率（三分类概率和=1）|
| `oth7_prob_neg` | 2 | 负向概率 |
| `oth7_prob_ntr` | 2 | 中性概率 |
| `oth7_sentiment` | 0 | 三值情绪 1/0/−1 |
| `oth7_confidence` | 5 | 情绪分类置信度 |
| `oth7_novelty` | 2 | 1=新故事，≥2=24h 内旧故事的链接 |
| `oth7_relevance` | 0 | 与公司相关度 1.00=primary |
| `oth7_headlineonly` | 10 | T=仅标题 / F=有正文（**头部字段 aC10**）|
| `oth7_automessage` | 5 | 定时批量发布标记 |
| `oth7_timestamp` | 1 | 发布时间戳（只作时点，不作信号）|
| `oth7_marketimpactscore` | 5 | **未来 1 分钟**风险调整收益估计 ⇒ **D1 未来函数，禁作信号** |

## 2. 头部质量先验（铁律 0.1）

头部 = `headlineonly` aC10（是否仅标题）⇒ 最强经济轴是**新闻呈现形式**，不是情绪方向本身。
⇒ 方向纠偏：优先测「仅标题 vs 有正文」的信息含量差，再用 prob_pos/neg 作辅腿；不要一上来就打纯情绪。

## 3. 预处理决策（0.3 五问）

- 类型全 VECTOR → `vec_avg` 聚合；
- coverage 0.2938 <0.4 → `ts_backfill` 门控，`trade_when` 优于裸 rank；
- 概率三分类和=1 → 用 `subtract(rank(pos), rank(neg))` 价差，禁三腿相加；
- 频率事件驱动 [inferred]，窗口 252d；
- 近十年须 `get_alpha_yearly_stats` 逐年验证。

## 4. 已试记录

W3 批次 `1SGVimgGm5hx9pZiLyKtmh3`（2026-11-17）：10 条 = prob_pos/neg 单腿 / 价差 / novelty / confidence 加权 / headlineonly / relevance；读数待收批。
