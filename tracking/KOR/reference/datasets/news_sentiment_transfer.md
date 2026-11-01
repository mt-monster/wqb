# news_sentiment_transfer · KOR/D1/TOP600 字段画像与机制库

> 快照日：2026-10-30（平台 `get_datafields` + DB catalog 实测，非推测）
> 归属塔：**KOR / D1 / SENTIMENT**（平台 `get_pyramid_alphas` 实测 **0/3 未点亮**，乘数 **1.6**）
> 数据集级事实：coverage **0.9654** / 23 字段（18 MATRIX + 5 VECTOR）/ userCount 1–23 / alphaCount 1–29 / valueScore 4
> 与它同塔的候选与拒选理由见 §0。

---

## §0 为什么是它（同乘数候选横向对照）

| dataset | cov | fields | alphaCount | 判定 | 依据 |
|---|---|---|---|---|---|
| **news_sentiment_transfer** | **0.9654** | 23 | 1–29 | ✅ **选中** | 高覆盖 + 极低饱和 + 字段族完整（水平/极值/偏度/注意力/双通道） |
| news104 | 0.2671 | 11 | 85 | ❌ 拒 | cov 0.2671 < 0.40 ⇒ 触发 KOR 策略规则「CW 先查覆盖率，<40% **换集**」；且只 11 字段、全 VECTOR |
| news54 | 0.6914 | 40 | 43 | ❌ 拒 | **字段级画像后否决**：40 字段全是事件日历元数据（`*_announcement_time` / `*_entry_time` / `*_last_update_time` / `*_headline` / `*_situation` / `*_cancelledflag` / `*_fiscalyear`），唯一数值量 `mws54_factor` cov 仅 **0.2449** ⇒ 无可连续定价的经济量，coverage/字段数好看但**无机制** |
| news50 | 0.6254 | 81 | 113 | 备选 | 未做字段级画像，留作 news 塔二轮 |
| news85 | 0.6325 | 23 | 52 | 备选 | 论坛有「涨跌反应差」非对称帖（post#10），二轮可测 |
| news38 | 0.7971 | 45 | 227 | 备选 | 覆盖最好但饱和 227，排在后面 |

⚠ **教训（写给自己）**：`coverage × fieldCount` 排序会选中 news54 这种「全是时间戳和文本」的数据集。
**字段级 description 是硬前置**，不能先按数据集级指标排队再去画像——那等于把配额交给统计量。

---

## §0.1 质量先验 TOP（按 alphaCount 降序，同分按 userCount）

| # | field | type | cov | users | alphas | 所在族 |
|---|---|---|---|---|---|---|
| 1 | `news_article_count` | MATRIX | .9654 | 23 | 29 | 注意力 |
| 2 | `primary_sentiment_average` | MATRIX | .9654 | 23 | 27 | 水平-主通道 |
| 3 | `secondary_sentiment_average` | MATRIX | .9654 | 18 | 18 | 水平-副通道 |
| 4 | `secondary_sentiment_middle_value` | MATRIX | .9654 | 16 | 16 | 极值/中位 |
| 5 | `secondary_sentiment_minimum` | MATRIX | .9654 | 13 | 15 | 极值 |
| 6 | `sentiment_score_average` | MATRIX | .9654 | 12 | 14 | 水平-综合 |
| 7 | `news_sentiment_score` | VECTOR | .9654 | 13 | 13 | 水平-综合（向量） |
| 8 | `sentiment_score_median` | MATRIX | .9654 | 10 | 11 | 极值/中位 |
| 9 | `sentiment_score_minimum` | MATRIX | .9654 | 10 | 11 | 极值 |
| 10 | `primary_sentiment_value` | VECTOR | .9654 | 8 | 10 | 水平-主通道（向量） |

**头部指向的轴 = 情绪水平（主/副通道均值）+ 新闻计数（注意力）** ⇒ 与拟挖方向（水平扩散 / 注意力门控）**一致**，方向不偏。
⚠ 头部 `alphaCount` 最高仅 29（对比 news59 的 2396、news18 的 1012）⇒ **该集几乎没有被挖过**，白空间真实存在。

## §0.2 字段分类（**以 description 为准，禁按字段名**）

| 族 | 字段 | 经济含义（来自 description） | 形态 |
|---|---|---|---|
| **F1 情绪水平·综合** | `sentiment_score_average` / `news_sentiment_score`(V) / `total_sentiment_score` / `sentiment_score_median` | 实体在区间内的平均/总/中位情绪 | MATRIX 可直用；VECTOR 需 `vec_avg` |
| **F2 情绪水平·双通道** | `primary_sentiment_average/value`(V) / `secondary_sentiment_average/value`(V) | primary = 主情绪分；secondary = 副情绪分 ⇒ **两套同构通道**，天然价差结构 | MATRIX + VECTOR |
| **F3 极值/分布** | `sentiment_score_maximum/minimum/middle_value`、`primary_sentiment_maximum/minimum/middle_value`、`secondary_*` 同构 | 区间内最强/最弱/中位情绪 | MATRIX |
| **F4 分歧/偏度** | `sentiment_distribution_skewness_2` / `primary_sentiment_skewness_2` / `secondary_sentiment_skewness_2` | 情绪分布的偏度（统计量，非原始情绪） | MATRIX |
| **F5 注意力** | `news_article_count` / `normalized_news_article_count` | 覆盖该实体的新闻条数（原值 / 跨实体归一） | MATRIX |

**名 vs description 差异表（被漏掉的资产）**：
- `primary` vs `secondary` 看着像"重要/次要"，description 只说"main / secondary sentiment score" ⇒ **不能当质量梯度用**，只能当**两条独立通道**（真正的资产是二者的**价差**）。
- `*_skewness_2` 后缀 `_2` 无文档解释 ⇒ **不假设它是第二版**，按 description 只当"偏度统计量"。
- `total_sentiment_score` 与 `sentiment_score_average` 同族但量纲不同（和 vs 均值）⇒ **只取一个进概念**，避免同一信息两条腿。
- `normalized_news_article_count` 与 `news_article_count` 是**归一化前后**，机制相同 ⇒ 只取一。

## §0.3 五问 + 预处理决策

| 五问 | 答案 | ⇒ 预处理 |
|---|---|---|
| 时间维度 | 情绪分是**区间聚合存量**（average/median/max），不是单日流量 | 水平可用；**变化率仍走 `ts_delta`**（铁律 A 的适用面是"单边恒正"，情绪有界对称 ⇒ 水平做多空合规） |
| 相对性 | 跨实体可比（已归一） | `rank` / `group_rank` 截面比较；`*_average` 可直接用 |
| 被定价的是谁 | 卖方/媒体的**语调**，定价方是**有限注意力的散户** | 强度型 + 广度型都有（F5 = 广度，F1 = 强度） |
| 有无博弈 | 有：分歧（F4）+ 注意力（F5）⇒ Miller 高估路径 | 分歧腿必须配**可投资性**考虑（KOR 已锁 TOP600，仅需 CW 处理） |
| 事件性 | `news_article_count` 可能零膨胀（无新闻日） | **门控**：`trade_when` / `if_else`，**禁裸 rank** |

**预处理决策**：
- cov **.9654 ⇒ 不需要 `ts_backfill`**（这是本集相对 news104 的核心优势）。
- **VECTOR 5 个必须先 `vec_avg`** 才能进常规算子。
- 更新频率：新闻日频 ⇒ **短窗 5–22 为主**，慢平滑 ≤ 66（论坛实证：新闻情绪短窗 5–22 有效）。
- KOR 设置先验实测：`neutralization=STATISTICAL`（14.6%，n=205 最优格）+ `decay=4` ⇒ 本轮沿用。
- **CW 唯一破法（KOR 实测）**：`hump(subtract(·, 0.5), hump=0.003)` —— 居中必须放在 `hump` **内层**，缺一不可。

---

## §1 机制库（A-3 概念块 ×5，双通道取证）

### M1 · 语调慢扩散（正向新闻定价更慢）
**Concept**: 新闻语调的改善被市场**渐进**吸收，正向语调的扩散慢于负向（论文实测方向句）。
- **Fields Used**: `sentiment_score_average`
- **Definition**: 实体区间平均情绪分，慢平滑后做截面排序。
- **Logical Meaning**: 谁被定价 = 媒体语调；为什么错 = **有限注意力 + 卖空约束**使正向消息扩散慢（负向消息被更快定价）；修复期 = 2–6 周。
- **Directionality**: **正向**（语调越高，未来 2–6 周相对收益越高）。⚠ 铁律 B：**必须同时测反向**，因为 KOR 是散户主导市场，情绪可能整体反转。
- **Boundary Conditions**: 新闻断档（article_count=0）期无信息；语调极值可能是一次性脉冲。
- **Expected Exposure**: sentiment
- **Implementation Example**: `hump(subtract(rank(ts_decay_linear(sentiment_score_average, 22)), 0.5), hump=0.003)`

### M2 · 分歧溢价（Miller 高估）
**Concept**: 同一实体的情绪分布越分散，说明意见分歧越大；在卖空受限市场里分歧 ⇒ **高估** ⇒ 后续负收益。
- **Fields Used**: `sentiment_score_maximum`, `sentiment_score_minimum`
- **Definition**: 区间情绪极差 = max − min（分歧的极差代理）；亦可用 `sentiment_distribution_skewness_2` 单独作偏度腿。
- **Logical Meaning**: 谁被定价 = 意见分歧；为什么错 = Miller(1977)：看空者无法卖空 ⇒ 价格只反映乐观者 ⇒ 分歧越大越高估；修复期 = 数周至一季。
- **Directionality**: **反向**（分歧越大，后续收益越低）。
- **Boundary Conditions**: KOR 卖空制度受限 ⇒ 机制先验成立；但若分歧主要来自**新闻条数**（只 1 条新闻时 max=min）需配注意力下限。
- **Expected Exposure**: sentiment
- **Implementation Example**: `hump(subtract(0.5, rank(divide(subtract(sentiment_score_maximum, sentiment_score_minimum), add(abs(sentiment_score_average), 0.01)))), hump=0.003)`

### M3 · 注意力门控反向（新闻密度 = 短期过热）
**Concept**: 新闻条数激增 = 散户注意力过载 ⇒ 短期过热，语调此时**反向**（噪声交易者主导）。
- **Fields Used**: `news_article_count`, `sentiment_score_average`
- **Definition**: 当 `news_article_count` 处于截面高位（注意力异常）时，才允许做情绪反向；否则不持仓。
- **Logical Meaning**: 谁被定价 = 注意力冲击下的散户；为什么错 = 信息超载导致短期流动性/情绪定价失真；修复期 = 3–10 日。
- **Directionality**: **反向**（高注意力 + 高语调 ⇒ 后续跌）。
- **Boundary Conditions**: 注意力低的样本不参与（`-1` 不持仓）；注意 KOR TOP600 的新闻覆盖不均。
- **Expected Exposure**: sentiment
- **Implementation Example**: `hump(subtract(trade_when(greater(rank(news_article_count), 0.7), 0.5, 0.0), group_rank(sentiment_score_average, sector)), hump=0.003)`

### M4 · 语调修正（变化型信号）
**Concept**: 语调的**变化**（而非水平）携带新信息；论坛实证变化型情绪天生高换手，需衰减平滑。
- **Fields Used**: `sentiment_score_average`
- **Definition**: 5 日语调变化量，再做 `ts_decay_linear` 降换手。
- **Logical Meaning**: 谁被定价 = 语调修正；为什么错 = 修正被渐进确认（分析师/媒体跟随滞后）；修复期 = 1–4 周。
- **Directionality**: **正向**（语调改善 ⇒ 继续跑赢）。
- **Boundary Conditions**: 换手天然高，须 `ts_decay_linear`；若 TO > 0.7 直接失格。
- **Expected Exposure**: sentiment
- **Implementation Example**: `hump(subtract(rank(ts_decay_linear(ts_delta(sentiment_score_average, 5), 10)), 0.5), hump=0.003)`

### M5 · 双通道背离（primary vs secondary）
**Concept**: 主情绪分与副情绪分是两条独立提取通道；二者**背离**时（一条乐观一条悲观）说明信息矛盾 ⇒ 不确定性折价。
- **Fields Used**: `primary_sentiment_average`, `secondary_sentiment_average`
- **Definition**: 两通道均值之差（**同数据集、单一经济含义 = 情绪通道背离**，属合规价差结构，不是混信号）。
- **Logical Meaning**: 谁被定价 = 两套 NLP 通道的解读差；为什么错 = 信息矛盾期市场高估确定性；修复期 = 2–4 周。
- **Directionality**: **反向**（背离绝对值越大越该低配）或**正向**（副通道是增量信息）。⚠ 两条都要测（铁律 B）。
- **Boundary Conditions**: 若两通道相关系数 ~1 则该腿退化为噪声，需先做一次相关性体检。
- **Expected Exposure**: sentiment
- **Implementation Example**: `hump(subtract(rank(primary_sentiment_average), rank(secondary_sentiment_average)), hump=0.003)`

---

## §2 双通道取证记录（2026-10-30）

**通道 A · BRAIN 论坛**
- `post 42659817284375`「新闻情绪因子:别再用裸 sentiment 了 —— relevance 加权 + 新颖度过滤」（31 票）：
  ① 裸情绪分直接排序 Sharpe 波动大；② **水平类情绪适合慢速平滑后截面排序**，**变化类情绪天生高换手**，须配 `ts_decay_linear`；
  ③ 聚合族覆盖率（0.96）远高于单实体族（0.72）——本集 cov .9654 正属聚合族。
- 「【sentiment模板】帮助点 sentiment 塔」：正/负面情绪分的**标准差**衡量舆论分歧度 ⇒ M2 的分歧腿来源。
- 「【Alpha模板】情绪数据中用 ts_covariance 构建 alpha 模板」（52 票）：`-ts_covariance(负面情绪, 正面情绪, d)` ⇒ 正负通道背离可做 M5 的备选实现。
- 「【Alpha Idea】给信号标保质期」：新闻情绪短窗 **5–22**，与 §0.3 的窗口决策一致。

**通道 B · 外部论文**
- *News sentiment indicators and the cross-section of stock returns*（Int. Rev. Econ. & Finance, 2025）：**正向新闻被定价的速度慢于负向新闻**；情绪在截面上是被定价因子 ⇒ M1 的方向句来源（且**天然要求非对称**，勿假设正负对称）。
- *News-based investor disagreement and stock returns*（Review of Accounting Studies, 2025）：分歧指标彼此相关性极低（2–8%），**各自捕捉不同维度且可预测性不同** ⇒ M2 不能用单一代理定论，需极差 + 偏度两条都测。
- *What does investors' online divergence of opinion tell us…*（JBR, 2018）：分歧对收益的影响**不对称**——牛市期负、熊市期正；分歧推高成交量 ⇒ M2 在 KOR（散户主导）应预期**负向为主**，但要记录牛熊分段归因。
- Baker & Wurgler (2006/2007)：情绪对**难套利、高主观估值**股票影响更大 ⇒ M3 的注意力门控应偏向小市值/高波动段（KOR 已锁 TOP600，仅需 CW 处理）。

**裁决**：A、B 在「水平慢扩散 + 分歧溢价 + 短窗」三点**指向同一机制** ⇒ 优先组装（M1/M2/M4）；
M3 与 M5 是**B 有机制、A 有零散表达** ⇒ 自建骨架，降优先级但仍测（各 1 条）。

---

## §3 待测表达式与实测记录

见 `tracking/KOR/reference/datasets/news_sentiment_transfer.md` §3（wave 203 起逐条回写；表格列 = 表达式 / alpha_id / S / 2Y / F / TO / subU / CW / 结论）。

| wave | 腿 | 机制 | 表达式（截断） | alpha | S | 2Y | F | TO | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| 203 | 待填 | | | | | | | | |
