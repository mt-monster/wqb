# news85 · KOR/D1/TOP600 字段画像与机制库

> 数据集：`news85`（RavenPack Web headlines 的**情绪分布形状**类，非平均情绪类）
> 区域/宇宙/Delay：KOR / TOP600 / D1 · 塔位：**news（未点亮 0/3）** · 倍率 ×1.6
> 建档：2026-10-30 · 状态：画像完成，**未开波**（排在 news31 之后）
> 覆盖率 .6325 · 字段 23（全部取到，`sharpe_filter_removed=0`）· 平台 alphaCount **52**

---

## §0 数据集选择：为什么是它，而不是 news50 / news7

| 候选 | cov | 字段 | 平台 aC | 判断 |
|---|---|---|---|---|
| news79 | .8563 | 85 | **899** | ⛔ 判死（`news79_dead`） |
| news18 | .5709 | 29 | 1012 | 饱和，跳过 |
| news7 | .6327 | 56 | 372 | 注意力/提及频率，中等饱和 |
| news50 | .6254 | 81 | 113 | 备选，未画像 |
| **news85** | **.6325** | **23** | **52** | ✅ 选它 |

选它的三条理由：

1. **字段级几乎无人碰**：23 个字段的 `alphaCount` 区间 **0–8**（不是 0–200），
   其中 `sentiment1_distribution_skewness` / `sentiment1_raw_score` / `sentiment2_raw_score` /
   `sentiment2_central_tendency` 四个字段 **αC=0，从未被任何人用过**。
2. **字段形态不是「平均情绪」**：全是**当日多条新闻情绪分布的统计量**（均值 / 中位数 / 最大 / 最小 / 偏度 / 条数）。
   而 KOR news 塔已判死的 `news79`/`news46` 走的正是「平均情绪 / 事件计数」老轴 ⇒ **本集提供的是新的截面形状轴**。
3. **机制与文献直接对上**（见 §2）：分歧度（disagreement）、极端情绪非对称（extreme sentiment asymmetry）都是
   有实证支持的**横截面定价因子**，不是「新闻多就看涨」的直觉。

---

## §0.1 字段质量先验（alphaCount 降序，全 23 字段）

| # | 字段 | 类型 | cov | aC | uC | description 要点（原文语义） |
|---|---|---|---|---|---|---|
| 1 | `aggregate_sentiment_total` | MATRIX | .6325 | **8** | 8 | 当日全部命中标题的 base 通道正向情绪概率**求和**（净正向情绪流量） |
| 2 | `sentiment1_average_value` | MATRIX | .6325 | 7 | 6 | 通道1 情绪的**日均值**，∈[0,1] |
| 3 | `headline_item_count` | MATRIX | .6325 | 5 | 5 | 当日命中标题的**原始条数** |
| 4 | `normalized_headline_count` | MATRIX | .6325 | 5 | 3 | 标题条数按参考/均值归一 |
| 5 | `peak_sentiment_value` | MATRIX | .6325 | 5 | 3 | 当日 base 通道情绪的**最大值** |
| 6 | `sentiment2_average_value` | MATRIX | .6325 | 5 | 4 | 通道2 情绪日均值 |
| 7 | `sentiment_overall_average` | MATRIX | .6325 | 5 | 4 | base 通道情绪日均值 |
| 8 | `sentiment_distribution_skewness` | MATRIX | .6325 | **4** | 4 | base 通道情绪在当日各标题间的 **Fisher 偏度** |
| 9 | `sentiment_overall_median` | MATRIX | .6325 | 2 | 2 | base 通道情绪中位数 |
| 10 | `sentiment_overall_minimum` | MATRIX | .6325 | 2 | 2 | base 通道情绪**最小值** |
| 11 | `mws85_sentiment` | VECTOR | .6325 | 2 | 2 | 逐条标题的正向情绪概率（需 `vec_avg` 等降维） |
| 12 | `sentiment1_aggregate_total` | MATRIX | .6325 | 2 | 1 | 通道1 情绪求和 |
| 13 | `sentiment1_highest_score` | MATRIX | .6325 | 3 | 3 | 通道1 **最大值** |
| 14 | `sentiment1_lowest_score` | MATRIX | .6325 | 3 | 3 | 通道1 **最小值** |
| 15 | `sentiment1_median_value` | MATRIX | .6325 | 2 | 2 | 通道1 中位数 |
| 16 | `sentiment2_aggregate_total` | MATRIX | .6325 | 1 | 1 | 通道2 情绪求和 |
| 17 | `sentiment2_highest_score` | MATRIX | .6325 | 2 | 2 | 通道2 最大值 |
| 18 | `sentiment2_lowest_score` | MATRIX | .6325 | 2 | 2 | 通道2 最小值 |
| 19 | `sentiment2_distribution_skewness` | MATRIX | .6325 | 2 | 2 | 通道2 偏度 |
| 20 | `sentiment1_distribution_skewness` | MATRIX | .6325 | **0** | 0 | 通道1 偏度 —— **全库无人用过** |
| 21 | `sentiment1_raw_score` | VECTOR | .6325 | **0** | 0 | 逐条通道1 情绪向量 —— **无人用过** |
| 22 | `sentiment2_raw_score` | VECTOR | .6325 | **0** | 0 | 逐条通道2 情绪向量 —— **无人用过** |
| 23 | `sentiment2_central_tendency` | MATRIX | .6325 | **0** | 0 | 通道2 中位数 —— **无人用过** |

⚠ **通道约定**：`sentiment1_*` / `sentiment2_*` / 无前缀（base）是**三条独立情绪通道**（TRNA-like 概率的三个口径）。
按 KOR 铁律「一条腿只出 1 颗」，**同一机制下不许把三通道拼成四条腿当四个信号**——这是同一条腿的三种度量。

---

## §0.2 六族分类（按 description，不按字段名）

| 族 | 字段 | 经济含义 | 状态 |
|---|---|---|---|
| **F1 情绪水平** | `sentiment_overall_average` / `_median` / `sentiment1_average_value` / `sentiment2_average_value` / `sentiment1_median_value` / `sentiment2_central_tendency` | 当日平均语气 | ⚠ **KOR news 塔已因「平均情绪」族判死两集**（news79/news46）⇒ 降级，不作主机制 |
| **F2 情绪极值** | `sentiment1_highest_score` / `_lowest_score` / `sentiment2_highest_score` / `_lowest_score` / `peak_sentiment_value` / `sentiment_overall_minimum` | 当日最好/最坏一条标题的语气 | ⭐ **主机制候选**（文献支撑最强，见 §2） |
| **F3 分歧度** | `sentiment_distribution_skewness` / `sentiment1_distribution_skewness` / `sentiment2_distribution_skewness` | 当日标题间语气的**不对称分散** | ⭐ **主机制候选**（两个通道偏度 αC 0/2，未被用过） |
| **F4 注意力/流量** | `headline_item_count` / `normalized_headline_count` / `aggregate_sentiment_total` / `sentiment1_aggregate_total` / `sentiment2_aggregate_total` | 当日新闻条数与情绪总量 | KOR 已判死 `news79` 的计数轴 ⇒ **只作解耦项/门控**，不单独当信号 |
| **F5 逐条原始分布** | `mws85_sentiment` / `sentiment1_raw_score` / `sentiment2_raw_score`（VECTOR） | 每条标题一个值 | 可 `vec_avg`/`vec_max`/`vec_min` 降维；**三个 raw 有两个 αC=0** |
| **F6 时延** | （无时间戳字段） | — | 本集**没有** `timestamp` 类字段 ⇒ 无 F5 时延族（对比 news31 有三个时间戳） |

### 名 vs description 差异（按名分类会踩的三个坑）

| 字段名像什么 | description 实际是什么 | 误判后果 |
|---|---|---|
| `aggregate_sentiment_total` 像「平均情绪」 | 是 **sum**（净流量），量纲随条数缩放 | 直接 `rank` 会变成「新闻多 = 情绪高」的条数代理 |
| `peak_sentiment_value` 像「峰值情绪」 | 是**当日多条中的 max**，只与最乐观一条有关 | 当成「整体情绪」会丢掉全部其它标题的信息 |
| `sentiment_distribution_skewness` 像「情绪偏度」 | 是**跨标题**的 Fisher 偏度（不是时间序列偏度） | 用 `ts_skewness` 之类重算等于重复造轮子且丢截面含义 |

---

## §0.3 字段画像五问 + 预处理决策

| 问 | 答 | 决定的算子 |
|---|---|---|
| **测什么** | 当日多条新闻的情绪**分布形状**（中心/极值/偏度）与**条数** | 中心⇒水平；极值⇒极值化；偏度⇒水平；条数⇒只作解耦/门控 |
| **怎么测** | 情绪概率 ∈[0,1] 有界；条数 ∈ℕ 无界 | 有界量 ⇒ `2*ts_rank-1` 居中或 `ts_zscore`；**条数必须先去量纲/归一** |
| **时间维度** | 日频事件型（非事件日 = 空/NaN） | ⛔ 高频输入 ⇒ **禁长窗 ts_rank**（KOR w41 实证日频长窗 S 从 -0.03 掉到 -0.20）；须先 `ts_mean`/`ts_decay_linear` 聚合 |
| **为何存在** | 平台把逐条标题情绪聚合成日度形状量，供做分歧度/极值研究 | 与 §2 文献的 disagreement / extreme sentiment 口径一致 |
| **可靠性** | 截面 cov .6325；**时间覆盖未知**（论坛三处警告 sentiment 类前几年无数据） | ⛔ 必须先跑 §4 十年核验，未过则本集降级 |

**预处理决策**：

| 读到的体征 | 决策 |
|---|---|
| cov .6325（>0.4） | 不必强制 backfill；但事件稀疏日仍需 `ts_backfill(F, 22)` 做短补 |
| 日频、非事件日空 | 先 `ts_mean(F, 5)` 或 `ts_decay_linear(F, 10)` 聚合再入 `ts_rank` |
| 有界 [0,1] | `signed_power(multiply(2, ts_rank(F, 252)), -1) ...` 形式居中；或直接 `group_zscore` |
| 偏度字段（可正可负） | 直接 `group_rank`/`group_zscore`，**不取 `ts_delta`**（偏度本身已是无量纲） |
| 条数（无界） | 只作 `trade_when` 门控或作 `ts_corr` 的一条腿，**禁单独 rank 当信号** |
| VECTOR | 先 `vec_avg` / `vec_max` / `vec_min` 降维 |

---

## §1 概念块（A-3，供 GEM / 后续波消费）

**Concept**: 极端坏消息的定价延迟（当日最悲观的一条决定后续漂移，而均值被中性稿稀释）
- **Fields Used**: `sentiment1_lowest_score`, `sentiment_overall_minimum`, `sentiment2_lowest_score`
- **Definition**: 取当日**最悲观那条**标题的情绪概率（截面 min），与市场其余部分比较；不取均值。
- **Logical Meaning**: 被定价的是**注意力稀缺下的坏消息吸收速度**——散户与本地媒体对负面信息反应不足
  （negativity bias 的镜像：坏消息传播慢但持续），机构在事件日之后 1–4 周逐步重定价。
  错在「均值口径把一条极坏标题和十条中性标题平均成同一个数」，两者后续漂移完全不同。
- **Directionality**: 当日最悲观情绪越低（min 越小）⇒ 后续 1–4 周相对**跑输**；反向腿需实测。
- **Boundary Conditions**: 单条新闻日（min = mean = max，无截面形状信息）失效；停牌/无覆盖日 NaN；
  极端行情（2020-03）尾部主导，逐年 S 必须分年核。
- **Expected Exposure**: `sentiment`
- **Implementation Example**: `group_rank(ts_mean(ts_backfill(sentiment1_lowest_score, 22), 5), sector)`
  ⚠ 方向必须正反各测（铁律 B）；文献预测**正极值腿更强**，故本腿预期弱于正极值腿。

**Concept**: 当日标题间的语气分歧度（disagreement ⇒ 后续负收益，不确定性主导时）
- **Fields Used**: `sentiment1_distribution_skewness`, `sentiment_distribution_skewness`
- **Definition**: 当日多条标题情绪分布的 Fisher 偏度；极端正值 = 少数极乐观标题拉高分布。
- **Logical Meaning**: 被定价的是**信念分散度**：分歧大 ⇒ 卖空约束下高估（Miller 1977）⇒ 后续负收益。
  错在「分歧是私有信息，无法直接被观测」，而日内跨标题偏度是它唯一的公开代理。
- **Directionality**: 偏度越大（少数极端乐观标题主导）⇒ 后续 1–3 个月**跑输**；不确定性主导区制下成立。
- **Boundary Conditions**: 当日只有 1–2 条标题时偏度不可估（缺失或噪声）；区制依赖（乐观主导时符号翻转，
  见 §2 文献的双重排序结论）⇒ **必须正反各测 + 多年份分年核**。
- **Expected Exposure**: `sentiment`
- **Implementation Example**: `group_zscore(ts_mean(ts_backfill(sentiment1_distribution_skewness, 22), 5), sector)`

---

## §2 双通道取证

### 通道 A｜BRAIN 论坛

检索式：`news sentiment dispersion skewness disagreement`（10 条命中，逐条读 1 篇正文 + 24 条评论）。

| 帖 | 内容 | 对本波的用法 |
|---|---|---|
| `37140180319127` Community Leader · MCP七十二变模板之 news-sentiment 点塔 | 模板 `group_zscore(-ts_corr(<news/>, <sentiment/>, <days/>), <group/>)`，机制 = **注意力 × 情绪的解耦**（成交量/条数 vs 情绪的相关性）。评论 24 条，多人实测：JY16044「跑了 1000 条 0 可用」、JX39934「GLB 低 universe 没信号」、CF26088/LU53797/HX55085 **三处独立警告「sentiment 类前几年没有数据/没有信号」** | ⭐ **单数据集版本可用**：在同集内部做 `-ts_corr(headline_item_count, sentiment_overall_average, N)` = 条数与语气解耦，不需要跨数据集、不涉混信号。⚠ 三处「前几年无数据」警告直接命中用户硬要求 #4 ⇒ §4 必须先核十年 |
| `33554030316183` Data Idea系列2：News Sentiment Data_news54 | 讲 news54 的 sentiment 用法，news54 已被字段级否决（唯一数值字段 cov .2449） | ❌ 不可迁移 |
| 其余 7 条 | 均为新闻/情绪类通用模板，未涉及**分布形状**（偏度/极差/极值） | — |

**可靠性判定**：`found=true`，但**本集特有的「分布形状」机制在论坛无直接帖**（`no_result`，不是判死依据，
按 `recon_evidence` 契约记为检索可靠完成的无命中）。⇒ 形态靠通道 B 自建。

### 通道 B｜外部金融研究

| 文献 | 机制句 | 方向 + 持有期 | 适用域与警示 |
|---|---|---|---|
| **News-based investor disagreement and stock returns**（*Review of Accounting Studies*, 2025） | 从新闻构建 **optimism-uncertainty score**；分歧度与未来收益的关系**随区制翻转**：乐观效应主导时为正、不确定性效应主导时为负 | 1–3 个月；双重排序下高-低收益差 3.01%–4.10%（t 1.79–1.97） | 美股大样本 ⇒ **KOR 只作假说**；⚠ 符号区制依赖 ⇒ 铁律 B 正反必测 |
| **An Extreme Firm-Specific News Sentiment Asymmetry Based Trading Strategy**（TRNA 2003–2014） | 用 **sentiment shock score + trend score** 度量个股极端正/负情绪；存在最优信号区 | 极端情绪冲击后有**长期持续**效应；**极端正向情绪的预测力强于极端负向** | 13 年 TRNA 样本；⚠ 反向不对称结论要本区复验，不可照搬「正极值更强」 |
| **Investor disagreement from social media**（*J. Business Research* 2018, 166–178） | 意见分歧指标 ⇒ 收益影响**在牛/熊市符号相反**；分歧↑ ⇒ 成交量↑（全区制成立） | 同期至数周 | StockTwits/美股；⚠ 仅支持「分歧→成交量」，不直接支持「分歧→收益」 |
| **News sentiment and the investor fear gauge** | VIX 变动与新闻情绪负相关且**不对称**：坏消息后 VIX 反应更大 | 日频 | 市场级而非个股级 ⇒ 只作机制旁证 |

### 双通道裁决

- **A 有模板（注意力×情绪解耦），B 有机制但无该模板**（B 讲的是极值与分歧度，A 讲的是解耦）⇒ 两条都可组装：
  M3（解耦）来自 A，M1/M2（极值/分歧）来自 B，**互不冲突**。
- **B 有机制、A 无对应表达** ⇒ 按 ②.b/②.c **自建骨架**，用 B 的方向句定形态，用 A 的经验定「日频要先聚合」。
- ⚠ **文献偏误登记**：三篇 B 都是美股；KOR 小宇宙、散户占比高、卖空受限更严（Miller 1977 的机制**更强**而非更弱）
  ⇒ 方向可借，**幅度与符号必须本区实测**。
- ⚠ **论坛负面复现登记**：「1000 条 0 可用」「GLB 无信号」意味着该族成功率低 ⇒ **本波只投 1 波 4 腿探针，
  不预先承诺深挖**；读数不合格即按铁律 F 停手，不逐档扫参。

---

## §3 实测记录（待回填）

| 波 | alpha | 机制 | S | 2Y | Fit | TO | 结论 |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | 待开波 |

## §4 近十年数据核验（用户硬要求 #4）— 待回填

- 触发原因：论坛 **三处独立警告**「sentiment 类前几年没有数据/信号」（CF26088 / LU53797 / HX55085）。
- 判定方式：首波任一条的 `get_alpha_yearly_stats`，**2014–2023 每年必须有非零 longCount/shortCount**；
  任一整年空白 ⇒ 本集降级（不得作为 60 颗的主数据集；必要时把回测起点后移并如实登记）。
- 结论：**待回填**。
