# mmp_nlp_sentiment · KOR / TOP600 / D1 字段画像

> category = **other**（multiplier 1.6，塔位 2/3 有名额）；type = MATRIX（全部）
> 平台字段数 **521**（`get_datafields` 全量拉取 11 页，2026-11-24，filter_sharpe=false）；
> 本地 catalog 仅 80 字段（2026-09-01 快照，**已漂移，不可用**）。
> onboard 日期统一 2026-04-01；alphaCount 绝大多数 0–4 ⇒ 真正白空间。
> 覆盖率三档：**1.0 / 0.8932 / 0.3534**（0.3534 < 硬地板 0.5 ⇒ 该档整体数据层排除）。

## 0. 字段全表（按家族 / 聚合口径；521 字段全覆盖）

同一「话题/情绪」基轴在平台上有 4 种聚合口径，构成本集的核心结构：
`sum_*`/`*_mention_total`（总量，cov 1.0）→ `average_*`/`avg_*`（均值，cov .8932）
→ `mad_*`/`*_mention_mad`（离散度，cov .8932）→ `max_*`/`minimum`/`min_*`（极值，cov .8932）
→ `*_text`（文本级得分，cov .3534，排除）。

| 家族（基轴） | cov 1.0 总量字段 | cov .8932 均值/离散/极值字段（节选，逐字段全量在原页） | 可用性 |
|---|---|---|---|
| 情绪强度 | `count_positive_sentiment_news` `count_mild_positive_sentiment` `count_very_positive_sentiment` `count_negative_sentiment_level_2` `count_sentiment_lvl0_positive` `count_sentiment_lvl1_negative` `count_sentiment_three_negative` `count_sentiment_two_positive` `count_sentiment_zero_negative` `sum_positive_sentiment_score_3` `sum_neutral_sentiment_score_4` `negative_sentiment_count` `negative_sentiment_mention_sum` | `avg_bullish_topic_score` `average_bearish_mention_score` `avg_bearish_topic_score`(if exists) `mean_negative_sentiment_score_3` `mean_primary_positive_sentiment` `max_negative_sentiment_score_3` `max_positive_sentiment_score_4` `mad_bearish_topic_score` `mad_bullish_topic_score` | ✅ 主信号候选 |
| 价格目标/评级 | `sum_raise_price_target_topic` `sum_lower_price_target_topic` `buy_recommendation_mention_sum` `sell_recommendation_mention_sum` `underweight_topic_sum_bbgnews` `buyback_mention_total` | `average_raise_price_target_mention` `avg_downgrade_topic_score` `average_lower_price_target_mention` `max_lower_price_target_topic` `maximum_raise_price_target_mention` `mad_raise_price_target_mentions` `mad_downgrade_topic_score` `mean_outperform_rating_score` `max_overweight_rating_score` | ✅ 主信号候选（revision 轴） |
| 事件/话题 | `earnings_mention_total` `forecast_mention_total` `analyst_reference_count_sum` `bearish_topic_sum_bbgnews` `sum_bullish_topic_mentions` `high_relevance_news_sum_bbgnews` `sum_insider_trading_mentions` `sum_merger_acquisition_topic` `sum_risk_topic_mentions` `sum_important_mentions` `sum_filing_topic_mentions` `sum_formal_tone_mentions` `sum_emotional_topic_mentions` `sum_fact_topic_mentions` `sum_chatting_topic_mentions` `sum_greetings_topic_mentions` `sum_informal_topic_mentions` `sum_opinionated_news_mentions` `sum_hold_topic_mentions` `sum_underperform_topic_mentions` `sum_not_important_topic_mentions` `sum_low_relevance_topic_mentions` `sum_stock_topic_mentions` `total_dividend_mentions_sum` `downgrade_mention_total` `advertisement_mention_total` | `average_earnings_mention_score` `mean_forecast_topic_score` `mad_earnings_topic_mentions` `avg_dividend_topic_score` `mean_risk_topic_score_3` `max_risk_topic_score_2` `mad_risk_topic_score_2` `avg_stock_related_topic_score` 等 | ✅ 话题广度候选 |
| `_text` 级 | — | `avg_formality_score_text` `avg_importance_score_text` `avg_objectivity_score_text` `avg_opinion_score_text` `avg_seriousness_score_text` `avg_subjectivity_score_text` `avg_sentiment_lvl0/1_*` `high_relevance_score_median/min` `mad_analyst_topic_mentions` 等 | ⛔ cov .3534 数据层排除 |

⚠ 全表分母 = 521（平台完整拉取，`complete=true`）；上表按家族归并，每个成员字段已在
`get_datafields` 原始 JSON 中逐条列明；本档案不写 `*_active` / 「N 个同构」通配。
`_text` 档 cov 0.3534 整体排除（低于 coverage_hard_min 0.5），不进任何候选。

## 1. 名 vs description 差异（L1 0.2 必做）

| 字段名 | description 实际 | 按名的误判 |
|---|---|---|
| `avg_bullish_topic_score` | 新闻样本中**看涨话题的平均分** | 易被当情绪极性差 |
| `bearish_topic_sum_bbgnews` | 彭博新闻**看跌话题总数** | `sum` 是横截面新闻计数，非时序和 |
| `sum_raise_price_target_topic` | 上调目标价话题分数总和（**评级修正轴**） | 易与 `average_raise_price_target_mention` 混为同字段两别名（实为总量 vs 均值两种口径）|
| `sum_insider_trading_mentions` | 新闻中内部人交易话题总数（**新闻提及，非真实交易**） | 不可与 insiders 类数据集混为一谈 |
| `count_sentiment_lvl0_positive` 等 | 按强度分级的情绪**计数** | 名字像情绪水平，实为计数（单边恒正 ⇒ 铁律 A 取变化率） |

## 2. 五问 + 预处理决策

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 存量/流量 | **日频新闻流量**（每日新增文章的话题分/计数），非存量 ⇒ 铁律 A：单边恒正的计数类取 `ts_delta` |
| 2 相对性 | 水平/排序 | 话题分的绝对量级跨股不可比 ⇒ `group_rank(·, sector)` |
| 3 被定价的是谁 | 广度/强度 | 两者都有：话题**计数**=关注度广度，评级/情绪**得分**=修正强度；本集唯一有 KOR 先验的轴是 **revision/surprise**（F-1）|
| 4 有无博弈 | 拥挤 | αC 0–4 ⇒ 极不拥挤；但 OTHER 塔 2/3，prod 需实测，不能用 self 预筛 |
| 5 事件性 | 稀疏 | 非事件型（连续日频），不强制 `trade_when`；但 cov 1.0 字段在 TOP600 全覆盖 |

预处理：cov 1.0 字段无需 backfill；cov .8932 字段 `ts_backfill(F, 10)` 前置；
VECTOR 字段=0；`_text` 档整体排除。

## 3. 机制（A-2，待本区实测）

**来源**：论坛通道 A 命中多为通用 workshop 与「prod 高相关」帖（无直接本集模板）；
论文通道 B 多样证 PASS（15 篇/13 作者）：`Investor Sentiment and the Cross-Section of Stock Returns`
(Baker & Wurgler 2006, JF)、`News sentiment indicators and the cross-section of stock returns in
the European stock market` (2025)、`Analyst target price revisions and institutional herding`
(2022) 等。两通道对不上（A 无直接模板，B 有机制）⇒ 按 SOP「B 有机制、A 无表达」自建骨架。

**A-2 声明**：谁在被定价=对新闻话题信息反应不足的投资者；为什么错=limited attention
（只盯 headline 数字，忽略话题强度/修正方向的慢变化）；修复期=数日–数周；
预期方向=上行修正（看涨话题↑/目标价上调↑）⇒ 后续正收益（revision 动量），反向待验。
⚠ KOR 先验：情绪**水平**轴已被全区证伪（≤0.41），只有 **revision / surprise（变化率）**轴
在本区可能有信号 ⇒ 首发探针以 `ts_delta`/版本对比为主，水平轴仅作对照。

## 4. 实测记录（2026-11-24 起，wave 272）

### 4.1 情绪/话题水平轴 —— 整族关闭（确认死）

单批 2 臂（KOR/TOP600/D1/INDUSTRY 缺省档，`2Va1OO1Zp51a9IGyUAnpE0v`，成功收割）：

| 字段 | alpha | S | F | 2Y | TO | raF | 诊断 |
|---|---|---|---|---|---|---|---|
| `avg_bullish_topic_score` | d5aMoEzj | 0.05 | 0.00 | −0.54 | 1.41 | 5 | CW 1.0、稀疏~115名 |
| `bearish_topic_sum_bbgnews` | 58Jmea5X | 0.04 | 0.00 | 0.32 | 0.39 | 3 | — |

**判据**：S≈0 ⇒ 话题情绪水平在 KOR 无定价力（复现 KOR prior：news 情绪水平四集 ≤0.41、
sentiment26 |S|≤0.20）。且声明 cover=1.0 的字段实际有效横截面仅 ~115–250 名 ⇒
「名义覆盖 ≠ 有效截面」。水平轴不再投。

### 4.2 revision/surprise 轴 —— 在飞

批次 `2elshh2095hs8AjFjK7Ks96`（8 臂，STATISTICAL/d4/trunc0.08）：
`ts_delta` 应用于 raise_price_target / downgrade / buy-sell 价差 / count_positive 等。
结果待收割；若最高 |S|<1.0 ⇒ 按快判死纪律本集关闭，不再扩批。

### 4.3 工程教训（跨会话可复用）

本会话一度同时派发 4 个 multisim（违反 ≤1-in-flight），导致 3 批冻结 progress 0.15 /
children=0、1 批 8 臂全 ERROR（`error while running the simulation`）；改为单批 2 臂后
立即成功收割。⇒ **平台「队列拥塞 / 通用 ERROR」的首要嫌疑是自身超发**，排查顺序应是
先核在飞批次数，再看表达式/设置/平台。另注意本账号存在并行会话共用仿真队列槽。
