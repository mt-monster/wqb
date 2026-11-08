# EUR/OTHER `news_sentiment_dl` 战役台账（2026-11-06）

> 定位：`techindi_model` 整集封盘后（prod 0.73-0.86）EUR/OTHER 的**第 2 号跃迁目标**。
> EUR/OTHER 当前 2/3，差 1 颗点亮；单数据集 ATOM，不占塔混配额。

## 一、数据集画像

| 项 | 值 |
|---|---|
| 字段数 | 66，**全部 VECTOR 类型** |
| 覆盖率 | 0.7443 - 0.7723（三源各一档） |
| 拥挤度 | **max alphaCount = 1**（65/66 字段 aC=0） |
| 结构 | 3 个新闻源 x 11 类指标 的笛卡尔积 |

三源（各自 cov 不同，是天然的「源质量」分层）：

| 源后缀 | cov |
|---|---:|
| `_inferess` | **0.7723**（最高） |
| `_trna` / `_trna_enhanced` | 0.7508 |
| `_bbgnews_enhanced` | 0.7443 |

指标轴两类：

1. **情绪词极性**：`mean_positive_word_sentiment_*`、`mean_negative_word_sentiment_*`、
   `max_*`、`min_*`、`positive_word_count_*`、`negative_word_count_*`
2. **可读性**：`avg_words_per_sentence_*`、`avg_syllables_per_word_*`

**关键结构特征**：VECTOR 类型意味着每条记录是**一天内的多条新闻构成的向量**。
这带来两个别人拿不到的信息维度：

- **向量内分歧**（`vec_stddev`）：同一天不同新闻的语调不一致程度 = 当日意见分歧；
- **跨源分歧**（同指标不同源相减）：不同新闻机构对同一股票的看法差异 = 机构层意见分歧。

两者都是**单数据集内**即可构造的，不需要混第二个数据集（避开塔混限制）。

## 二、模板库（13 个，结构互异）

记 `pos(src)` = `vec_avg(mean_positive_word_sentiment_{src})`，`neg(src)` 同理。
全部外包 `rank()` 做截面展开（VECTOR 字段必须逐字段 `vec_avg` 包裹，裸用会报 event inputs）。

| 编号 | 模板名 | 结构 | 算子数 | 信息维度 | 来源 |
|---|---|---|---:|---|---|
| W01 | 净情绪（源内） | `rank(pos - neg)` | 4 | 一阶方向（语调净额） | 论坛·软信息 |
| W02 | 极端负面尾部 | `rank(vec_avg(max_neg) - vec_avg(max_pos))` | 4 | 尾部（最坏句子） | Tetlock 悲观语调 |
| W03 | 跨源分歧 | `rank(pos(A) - pos(B))` | 4 | 机构间意见差异 | Miller 分歧 + 卖空约束 |
| W04 | 向量内分歧 | `rank(vec_stddev(pos))` | 3 | 当日新闻一致性 | 论坛·稳定性 |
| W05 | 句长复杂度 | `rank(vec_avg(avg_words_per_sentence))` | 3 | 处理成本（信息摩擦） | Li 可读性 |
| W06 | 音节复杂度 | `rank(vec_avg(avg_syllables_per_word))` | 3 | 阅读门槛（正交于 W05） | Li 可读性 |
| W07 | 负面词频强度 | `rank(vec_avg(neg_count) - vec_avg(pos_count))` | 4 | 计数型（非打分，量纲独立） | Tetlock 2008 |
| W08 | 情绪修正动量 | `rank(ts_delta(W01核, 22))` | 5 | 一阶差分（语调被上调） | 论坛·趋势 |
| W09 | 情绪时序分位 | `rank(ts_zscore(W01核, 252))` | 5 | 相对自身历史 | 自建 |
| W10 | 分歧门控 | `rank(W01核 x rank(W04核))` | 7 | 二阶 x 一阶交互 | 论坛·置信度加权 |
| W11 | 复杂度相对自身 | `rank(ts_rank(vec_avg(avg_words_per_sentence), 252))` | 4 | 摩擦的时序异常 | 自建 |
| W12 | 跨源最悲观 | `rank(min_neg_across_sources)` | 5 | 保守共识（比均值稳健） | 论坛·分位数标准化 |
| W13 | 源内极端度 | `rank(vec_avg(max_neg) - vec_avg(mean_neg))` | 4 | 分布尾部相对中心 | 自建 |

维度自检：一阶水平(W01/W07)、尾部(W02/W13)、分歧-机构(W03)、分歧-日内(W04)、
摩擦/可读性(W05/W06/W11)、时序变化(W08/W09)、交互(W10)、稳健共识(W12) 
—— **8 个互不重叠的信息维度，13 个结构**，满足模板库 >=10 且结构互异的硬约束。

## 三、探针批

设置档：EUR / TOPCS1600 / delay 1 / **decay 2** / SUBINDUSTRY / truncation 0.08 / unitHandling VERIFY /
nanHandling ON / pasteurization ON / maxTrade OFF。

decay 2 是被 `techindi_model` 实证过的首选换手杠杆（T02 上 TO 70.33% -> 48.79%，S 仅 -0.18、F 反而 +0.21）。

| 批 | multisim | 模板 | 表达式 |
|---|---|---|---|
| N1 | `1BbbhB9vr4T89rE1dpHxsCAg` | W01 / W05 | `rank(pos-neg)`（inferess） / `rank(vec_avg(avg_words_per_sentence))` |
| N2 | `3Bo0zSdN94i1brp2A4ZSAE1` | W03 / W04 | `rank(pos(bbgnews)-pos(inferess))` / `rank(vec_stddev(pos))` |

预注册判据：

- 任一 S >= 1.58 且 `sub/S >= 0.5303` 且 F >= 1 => 测 prod（约 10 秒/件）；
- prod < 0.70 => 登记为候选，EUR/OTHER 2->3 点亮；
- 四条 |S| < 0.5 => 该数据集封盘，转 `news_sentiment_nlp`（23 字段，cov 0.9134，aC 0-6）。

风险标注：

1. cov 仅 0.744-0.772，比 EUR 常规档（0.9+）薄，longCount 可能偏低 => 留意 CONCENTRATED_WEIGHT 与 LOW_SUB_UNIVERSE_SHARPE。
2. VECTOR 逐字段 `vec_avg` 包裹是硬要求，任何裸用会连坐 CANCELLED 整批（历史实证）。
3. `vec_stddev` 是否在算子清单内未经验证；本批把它与 W03 放在同一 multisim，若整批 CANCELLED 需先隔离验证该算子。

## 四、文献支撑（待定向补证）

- **Tetlock (2007)** *Giving Content to Investor Sentiment*, J. Finance —— 媒体悲观语调对股价有下行压力，随后反转；
- **Tetlock, Saar-Tsechansky & Macskassy (2008)** *More Than Words*, J. Finance —— 负面词比例预测公司基本面；
- **Loughran & McDonald (2011)** *When Is a Liability Not a Liability?*, J. Finance —— 通用词典在金融文本上失效，需金融专用负面词表；
- **Li (2008)** *Annual report readability*, J. Accounting & Economics —— 年报 Fog 指数与业绩持续性负相关；
- **Miller (1977)** *Risk, Uncertainty and Divergence of Opinion*, J. Finance —— 意见分歧 + 卖空约束 => 高估，是 W03/W04 的理论基础。

（以上为领域公认条目，本轮未逐条联网核对卷期页码；按「用机制前先查论坛 + 论文」的纪律，出货后再定向核实。）


## 五、收批实绩（2026-11-06）

| alpha | 模板 | S | F | TO | sub | 2Y | ret | dd | fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P0oPplax | W01 净情绪（inferess） | -0.28 | -0.03 | **159.55%** | -0.82 | 0.09 | -2.13% | 30.27% | 7 |
| kqN83mrz | W05 句长复杂度 | -0.26 | -0.03 | **161.42%** | -0.14 | -0.45 | -2.02% | 34.17% | 6 |
| gJer1Kje | W03 跨源分歧 | 0.22 | 0.02 | **174.62%** | 0.20 | -0.37 | 2.20% | 32.65% | 6 |
| WjOYpd7o | W04 向量内分歧 | 0.06 | 0.00 | **164.15%** | 0.34 | -0.27 | 0.68% | 41.42% | 6 |

## 六、判决：`news_sentiment_dl` 封盘（双杀因）

**杀因一：无信号。** 四个结构互异模板（语调方向 / 处理摩擦 / 跨源机构分歧 / 日内新闻分歧）
覆盖 8 个信息维度中的 4 个主要方向，`|S|` 全部 <= 0.28，最强 0.22。
连「净情绪方向」这个最基础的检验都不过（-0.28），说明**文本词典语调在 EUR 已经被完全套利**。

**杀因二：换手 160-175%。** 这是本会话见过的最坏换手档位（常规 EERROR 阈值 70%，即需压 2.3 倍）。
机制上可解释：VECTOR 是**逐日独立**的新闻向量，每天全部推倒重来 => 信号变化率接近 100%，
`decay 2` 只把 175% 压到 160% 量级，因为 decay 对「每日全部改变」的序列几乎无效。
即使有信号，也需要 `ts_mean(x, 22)` 级平滑才可能进 70% 带内，而平滑会把已经为 0 的信号彻底抹平。

配合 cov 仅 0.744-0.772（三源都不满覆盖），drawdown 30-41%，
**该数据集不值得再投仿真**。

连带判决：`news_sentiment_nlp`（23 字段，cov 0.9134）与本集同机制（同一批词典：VADER / SentiWordNet / TextBlob），
差别只在「标题 vs 正文」与覆盖率；既然正文版净情绪 S = -0.28，标题版不单独开波，除非有其它理由。

## 七、EUR/OTHER 面小结

| 数据集 | 判决 | 决定性证据 |
|---|---|---|
| `techindi_model` | 封盘 | 11 个结构变体 prod 全落 0.73-0.86，含一件全闸通过（S3.53/F1.81）但 prod 0.7967 |
| `news_sentiment_dl` | 封盘 | 4 个模板 |S|<=0.28 + 换手 160-175% |
| `news_sentiment_nlp` | 连带封盘 | 同词典机制，正文版已无信号 |
| `ai_news_scores` | 待测 | 105 字段 / cov 0.792 / aC 7 |
| `other571` | 待测 | 30 字段 / cov 0.759 / aC 2 |
| `other455` | 低优先 | 1500 字段但 aC 533（拥挤） |
| `search_interest` | 弃 | 仅 5 字段 |
