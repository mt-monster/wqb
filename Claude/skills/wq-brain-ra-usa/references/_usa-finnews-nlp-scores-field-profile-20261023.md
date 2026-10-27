# finnews_nlp_scores（Transformer Based Financial News Scores）字段画像与八机制判决（USA / D1 / TOP3000，2026-10-23）

> 用途：`finnews_nlp_scores` 在 USA/D1 的**全字段梳理 + 首波八机制回测裁决**。
> 本档按「字段画像 → 机制设计 → 回测结果 → 归因 → 判决」组织；§4 起为实测，指标一律经
> MCP `get_alpha_details` 直取（harness 内置解析对 raw shape 取不到 2Y / SUB / RA，不作数）。
> **本档不含提交动作；任何提交都必须用户明确确认（红线）。**

---

## 0. 数据集坐标（`get_datasets` / `get_datafields` 2026-10-23 实测）

| 项 | 值 | 备注 |
|---|---|---|
| dataset id | `finnews_nlp_scores` | "Transformer Based Financial News Scores" |
| 区域 / 延迟 | USA / D1 | 全程固定，未换区 |
| 类别 / 塔位 | `other` | 八臂 `pyramid_short` 全为 `other` ⇒ **USA/D1/OTHER ×1.4** |
| 可见字段 | **105**（`sharpe_filter_applied=true`，`sharpe_filter_removed=0`） | 全部 **MATRIX** |
| 覆盖率 | **1.000**（105/105 字段） | ⚠ 见 §2.2：这个读数本身是疑点 |
| 数据集拥挤度 | userCount **39** / alphaCount **61** | 低拥挤（对比 pv1 219 万 / fundamental6 86 万） |
| 字段拥挤度 | uC 0–10 / aC 0–13 | **67/105 字段 aC = 0**；最挤 `average_negative_sentiment_score_3`（uC 10 / aC 13） |
| 金字塔乘数 | **1.4**（平台 live） | DB `datasets` 行写 1.7，为 2026-08-26 旧快照，**以平台 live 为准** |
| valueScore / tier | 6 / `PPA_PASS` | DB 缓存值；PPA 门槛未在本轮复核 |
| 数据来源 | Dow Jones Newswires（道琼斯新闻专线）文章级情绪的打分聚合 | 描述逐字段确认 |

**为什么开这个数据集**：波 56 `news_sentiment_nlp`（earnings 塔）六机制全灭、波 61 `ds339`
TOP2000 八臂全灭之后，`other` 塔里**字段数最完整、覆盖 1.0、且平台使用量极低（aC 61）** 的
新闻情绪集只剩它。它是「DJ Newswires 多版本文本分数」这一族里**唯一带置信区间与离散度字段**
的成员，理论上比纯 mean 分数多两个信息维度（不确定性、尾部）。

---

## 1. 字段目录：7 统计族 × 3 极性 × 5~6 变体 = 105

### 1.1 命名结构

```
<stat>_<polarity>_sentiment[_score]_<variant>
  stat     ∈ average | median | maximum | minimum | stddev | lower_confidence | upper_confidence
  polarity ∈ positive | negative | neutral
  variant  ∈ _1 … _6（每个 stat×polarity 组合各 5 个，唯一 6 个的是 max/min/stddev 三族中的部分组合）
```

字段名里 `_sentiment_score` 与 `_sentiment` 两种写法混用（`maximum_*` / `minimum_*` / `stddev_*`
用 `_sentiment_score`，置信区间族用 `_sentiment`），但**语义一致**，不影响表达式引用。

### 1.2 统计族含义

| 族 | 含义 | 经济学解读 |
|---|---|---|
| `average_*` | 当日该股全部文章极性分的**均值** | 净语调水平（最常被引用的 Tetlock 型变量） |
| `median_*` | 当日极性分的**中位数** | 抗单篇极端稿件的稳健中枢；与均值之差 = 偏度代理 |
| `maximum_*` | 当日**最好/最坏**一篇文章 | 尾部/极端报道冲击 |
| `minimum_*` | 当日**最差**一篇文章（按极性） | 尾部（与 maximum 方向相反的另一侧） |
| `stddev_*` | 当日文章极性分的**标准差** | 分歧度 / 不确定性（分析师式 disagreement 的新闻版） |
| `lower_confidence_*` | 当日均值 **95% CI 下界** | 置信下界；与上界配对可得区间宽度与位置 |
| `upper_confidence_*` | 当日均值 **95% CI 上界** | 置信上界 |

**关键结构事实**：`positive` / `negative` / `neutral` 是**三个独立的 [0,1] 分数**，不是一条有符号分数。
所以「净语调」必须自己组装成 `positive − negative`（本波 A 臂即如此）。

### 1.3 变体语义（逐字段 description 归纳）

| 变体 | description 措辞 | 判读 |
|---|---|---|
| `_1` | "across **all mapped** Dow Jones Newswires stories for the stock on that day" | 基线语料（全量映射） |
| `_2` | "… linked to the stock on that day **(GLOBAL, variant 2, D1)**" | 平台显式标注的**独立变体/口径**（全局 feed v2） |
| `_3` | "across Dow Jones Newswires stories **linked to** the stock on that day" / "among **those** stories" | 另一条关联口径 |
| `_4` | "across **stories mapped to** the stock on that day" | 再次换措辞的映射口径 |
| `_5` | "score **(0–1)** … for a given stock and day" | 强调归一化区间的口径 |
| `_6` | "**observed among** … stories for the stock on that day" | 只在 max/min/stddev 部分组合出现 |

**判读（重要）**：六个变体的 description 是**近义改写**，没有给出可区分的语料/模型差异
（唯一明说的是 `_2` = GLOBAL, variant 2）。因此它们更像**同一构造的并行摄取/派生版本**，
而不是六个经济含义不同的信号。⇒ **变体之间的一致性差异（cross-variant divergence）才是本集
唯一可能的新信息维度**，而这正是本轮未测的那一项（见 §5.2）。

### 1.4 完整字段矩阵（105/105，单元格 = `uC/aC`，`—` = 该组合不存在此变体）

| stat × polarity | `_1` | `_2` | `_3` | `_4` | `_5` | `_6` |
|---|---|---|---|---|---|---|
| average_positive | 3/3 | 0/0 | 6/6 | 1/2 | 0/0 | — |
| average_negative | 2/4 | 0/0 | **10/13** | 2/3 | 0/0 | — |
| average_neutral | 0/0 | 0/0 | 1/1 | 1/1 | 0/0 | — |
| median_positive | 1/1 | 1/1 | 0/0 | 0/0 | 0/0 | — |
| median_negative | 2/2 | 1/1 | 0/0 | 1/2 | 0/0 | — |
| median_neutral | 2/3 | 0/0 | 0/0 | 0/0 | 0/0 | — |
| maximum_positive | — | 0/0 | 0/0 | 2/2 | 0/0 | 0/0 |
| maximum_negative | — | 0/0 | 0/0 | 0/0 | 0/0 | 1/**8** |
| maximum_neutral | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | — |
| minimum_positive | — | 0/0 | 1/2 | 3/3 | 0/0 | 0/0 |
| minimum_negative | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | — |
| minimum_neutral | 1/1 | 0/0 | 1/1 | 0/0 | 0/0 | — |
| stddev_positive | — | 0/0 | 0/0 | 0/0 | 1/2 | 0/0 |
| stddev_negative | 0/0 | 1/1 | 0/0 | 0/0 | 0/0 | — |
| stddev_neutral | — | 0/0 | 0/0 | 1/1 | 0/0 | 0/0 |
| lower_confidence_positive | 0/0 | 2/2 | 0/0 | 0/0 | 1/1 | — |
| lower_confidence_negative | 1/1 | 1/1 | 1/1 | 0/0 | 1/1 | — |
| lower_confidence_neutral | 0/0 | 1/1 | 0/0 | 0/0 | 0/0 | — |
| upper_confidence_positive | 1/1 | 0/0 | 0/0 | 0/0 | 1/1 | — |
| upper_confidence_negative | 1/1 | 0/0 | 1/1 | 2/2 | 1/1 | — |
| upper_confidence_neutral | 0/0 | 1/1 | 0/0 | 0/0 | 0/0 | — |

**结构不齐点（照实记录，别按 `_1.._6` 想当然）**：`maximum_positive` / `maximum_negative` /
`minimum_positive` / `stddev_positive` / `stddev_neutral` 这五个组合**缺 `_1`**，只有 `_2.._6`；
`maximum_neutral` / `minimum_negative` / `minimum_neutral` / `stddev_negative` **没有 `_6`**。
写表达式前必须按本表取字段，不能机械拼 `stat_polarity_1`。

---

## 2. 六个画像维度

### 2.1 字段类型与形态

- **全部 105 个字段都是 `MATRIX`**（面板可直接进 `ts_*` / `group_*` / `rank`），无 VECTOR、无 GROUP。
  ⇒ 不需要 `vec_*` 聚合，省掉一整类错误形态。
- 单值语义，日频对齐；D1 下**当日映射**（同一交易日发布的 DJ Newswires 稿件聚成当日值）。

### 2.2 覆盖率：1.000 的读法与疑点

105/105 字段平台上报 `coverage = 1`。对「日频新闻情绪聚合」这一形态，**满覆盖本身可疑**：

- 真实新闻流是稀疏事件：不是每只股票每天都有 DJ 稿件。若覆盖真是 1.0，说明**无新闻日被填了缺省值**
  （最可能是中性 0.5 或 0）。
- 若确实如此，则每个字段的截面离散度集中在有新闻的那一小部分股票上，其余全是同一个常数。
  `group_rank` 会把常数块排到中间，**机械压低 IC 与 Sharpe** —— 这与 §4 八臂全部归零的形态一致。
- **未验证**，判据也便宜：抽一个字段算「等于众数的股票-日占比」，> 90% 即坐实为填零/填中性。
  本波未做（不追溯），记为后续若重开此集的第一项检查。

### 2.3 更新频率

- 日频（D1），与新闻发布同步；周末/节假日无更新。
- 变体 `_2` 明确标 `(GLOBAL, variant 2, D1)`，其余变体未标延迟，**按同一日频处理**。
- 因为日频且当天映射，`ts_backfill(x, 66)` 只是补零星缺口，不会改变信号形状（八臂统一用了 66）。

### 2.4 取值范围

| 族 | 值域 | 依据 |
|---|---|---|
| `average_*` / `median_*` | [0, 1] | 极性分本身在 [0,1] |
| `maximum_*` / `minimum_*` | [0, 1] | 文章极性分的极值 |
| `lower_/upper_confidence_*` | [0, 1] | 均值的 95% CI 界，落在同区间内 |
| `stddev_*` | [0, 0.5] | 有界变量的标准差，最大 0.5 |

⇒ **无负值、无长尾爆炸**，不需要 `ts_rank` 之类强制转换；但也不含「方向」，方向必须由
`positive − negative` 或 `negative` 取负来构造。

### 2.5 分布特征（结构性推断，非实测）

- 极性分在 [0,1] 且多数文章接近中性 ⇒ **单字段截面右偏、质量堆在低端**；
- `stddev_*` 大量为 0（当日只有 1 篇稿件时标准差无定义/为 0）；
- 置信区间宽度 ∝ `stddev / sqrt(n)` ⇒ **宽度同时编码了分歧度与报道量**，两者混在一起；
  这正是 D 臂（宽度）与 H 臂（宽度变化）的设计依据，也是它们失败的可能原因之一（变量不纯）。

### 2.6 可用性

| 维度 | 判读 |
|---|---|
| 可直接进表达式 | 是（MATRIX、无缺失形态问题） |
| 需预处理 | `ts_backfill` 补缺口即可；无需 `vec_*`、无需 `bucket` |
| 拥挤度 | **很低**（aC 中位 0，最大 13）—— 但 §4 证明「不挤 ≠ 有信号」 |
| 子集可用性 | `_1` 与 `_3` 是唯二有人用过的变体；`_2/_4/_5/_6` 几乎零使用 |
| 作为 ATOM 独立源 | **不可用**（§4 判决） |
| 作为组合腿 | 不推荐（同族七集已证伪，见 §6.2） |

---

## 3. 拥挤度明细（可用性佐证）

- **38/105 字段有 alpha 使用记录，67/105 为 0**；uC 为 0 的有 66 个。
- 全表 alphaCount 合计仅 **80** 次引用（含重复计入不同字段），与 pv1 的 219 万不在一个量级。
- 头部集中：`average_negative_sentiment_score_3`（uC 10 / aC 13）、`maximum_negative_sentiment_score_6`
  （uC 1 / aC 8）、`average_positive_sentiment_score_3`（6/6）。
  ⇒ 已有使用者几乎都停在**「负向均值水平」**这一条最直觉的腿上，且最多做到 13 个 alpha。
- `_2` 变体（GLOBAL variant 2）在 average 族里**全部 0/0** ⇒ 完全没人用过，但本波 C/D/H 用了
  `stddev_*_2` 与 `upper/lower_confidence_*_1`，结果同样归零。

---

## 4. 八机制设计与回测结果

**公共设置**：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / truncation 0.08 / nanHandling ON /
2014-01-01 … 2023-12-31 / 壳层统一 `group_rank(…, subindustry)`。

| 臂 | 机制 | 表达式核心 | alpha | S | F | 2Y | SUB (limit) | TO | RA fail |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| A_net_tone | 净语调水平 | `positive_1 − negative_1`，5 日均值 | `E5VN1eVr` | 0.23 | 0.04 | −0.31 | −0.14 (0.10) | 15.6% | 4 |
| B_neg_only | 负向单边 | `−ts_mean(negative_1, 5)` | `JjPoqv8E` | −0.08 | −0.01 | −0.12 | −0.28 (−0.03) | 14.7% | 4 |
| G_abs_tone_rev | 语调幅度反转 | `−ts_mean(abs(pos₁−neg₁), 5)` | `P0MxNLgL` | −0.07 | −0.01 | 0.34 | −0.11 (−0.03) | 15.5% | 4 |
| C_disagreement | 分歧度（std 和） | `−ts_mean(stddev_pos₂ + stddev_neg₂, 5)` | `rKd9Yxr9` | −0.47 | −0.13 | −0.19 | −0.04 (PASS) | 15.8% | 3 |
| D_conf_width | 置信区间宽度 | `−ts_mean(upper_neg₁ − lower_neg₁, 5)` | `MP0dWWga` | −0.59 | −0.18 | −0.49 | −0.36 (−0.26) | 15.7% | 4 |
| H_coverage_shock | 覆盖激增（Δ22 宽度） | `−ts_mean(ts_delta(width, 22), 5)` | `ZYmg5oK0` | 0.05 | 0.00 | 0.65 | 0.09 (PASS) | 19.3% | 3 |
| E_tone_skew | 语调偏度（均值−中位） | `ts_mean(avg_pos₁ − med_pos₁, 22)` | `wp93m58Q` | **0.45** | 0.13 | 0.54 | 0.36 (PASS) | 9.1% | 3 |
| F_neg_extreme | 最坏报道极端 | `−ts_mean(minimum_negative_1, 5)` | `JjPowWPm` | 0.13 | 0.02 | 0.10 | −0.05 (0.06) | 15.0% | 4 |

**max S = 0.45 < 0.8 ⇒ 预注册判据命中，不做任何参数扫描**（预注册见交付日志 §K：
0.8 以下不许扫窗口/设置）。数据集作为独立 ATOM 源判死。

**多空/风险读数**：八臂 long:short 均在 1522:1541 ~ 1600:1459（≈1:1），
`risk_neutralized_sharpe` 六负（−0.17 ~ −0.83）两微正（0.04 / 0.20），
`CLUSTER_TEST` 全在 −0.31 ~ 0.32（limit 1.58）。

---

## 5. 归因（逐条排除「壳层/成本/拥挤」解释）

1. **不是字段没变化**：多空比≈1:1 ⇒ `group_rank` 有真实截面离散，字段不是常量、覆盖没塌。
   归零来自「有差异但无预测力」，不是「没差异」。
2. **不是交易成本**：TO 9.1%–19.3%，全部在 `LOW_TURNOVER` / `HIGH_TURNOVER` 的 PASS 区间，
   离 70% 上限很远；换手不是瓶颈。
3. **不是中性化吃掉信号**：`risk_neutralized_sharpe` 与原始 Sharpe 同号同量级地弱 ⇒ 信号在原始层
   就不存在，不在中性化后丢失。
4. **不是与已提交池撞车**：`CLUSTER_TEST` 全部远低于 1.58 ⇒ 这批是「新但无用」，不是「有用但重复」。
   （对照波 61 的 B0：S 1.99 只卡 self —— 那才是「有用但重复」的形态。）
5. **不是单一机制选错**：四个互不相同的机制簇同时归零 —— 语调水平（A/B）、不确定性（C/D/H）、
   尾部（F）、偏度（E）。文献上最能打的两条（Tetlock 语调、注意力冲击）都没起来。
6. **不是差一口气**：最好一臂（E，S 0.45）距 1.58 差 3.5 倍，F 0.13 / 2Y 0.54 同样远离，
   不是「某一闸单独卡住」。

### 5.1 本轮未测的两处设计缺口（照实记录，不追溯、不补跑）

- **语调一阶差分**：Tetlock (2007) 的核心变量是 pessimism **innovation**（语调的变化/冲击），
  而 A/B 测的是**水平**（5 日均值）。语调水平高度持续，差分后才是新闻流冲击。本波无任何臂测差分。
- **跨变体分歧**：`_1.._6` 六组变体之间的分歧（不同 feed 对同一事件的语调差异）没测；
  C 臂测的是**单变体内** `stddev`（同一 feed 内的估计离散）。后者更像「模型不确定性」，
  前者才是「信息分歧」。做它需要 12 字段多项式组装，算子数与成本都高。
- 这两条是「若日后重开此集」的唯二入口；**在此之前不要再拿它开波**。

---

## 6. 判决

### 6.1 本集

**`finnews_nlp_scores` 在 USA/D1 不产出 ATOM 候选**（8 臂 max S 0.45）。
正式封存（`seal_dead_end`）留待 S6：封存闸 fail-closed 要求论坛取证结论，本轮未做该集的论坛检索，
不能凭空 seal。候选键名建议 `USA-FINNEWS-NLP-SCORES-NO-SIGNAL`。

### 6.2 族级结论（比单集判决更重要）

「**情绪类文本分数**」这一族在 USA/D1 已连续七集证伪，本集是第八个：

| 数据集（塔） | 探针数 | 最好结果 | 出处 |
|---|---:|---|---|
| `news_sentiment_transfer`（sentiment） | 16 | max S 0.50；六臂 2Y 为负；TO 0.89–1.18% 卡 LOW_TURNOVER | `_usa-news-sentiment-transfer-field-profile-20261020.md` |
| `news_sentiment_dl`（other） | 10 | max S 0.63 | 同上 §5.1 |
| `ai_news_scores`（other） | 8 | max \|S\| 0.48 | 同上 §5.1 |
| `sentiment21`（sentiment） | — | max \|S\| 0.58 + HIGH_TURNOVER 1.44–1.58 | 同上 §5.1 |
| `mmp_nlp_sentiment`（other） | 24 | 0 条 ra_clean | 同上 §5.1 |
| `event_sentiment_signals` / `earningscall_embed` | — | 全灭 / 判死 | 同上 §5.1 + `dead_end` |
| `news_sentiment_nlp`（other，波 56） | 6 机制 | 全灭 | 交付日志 §H |
| **`finnews_nlp_scores`（other，波 62）** | **8 机制** | **max S 0.45** | 本档 §4 |

⇒ **同塔的 `nlp_news_scores`（OTHER，84f，aC 51）不再作为波 63 的 fallback**。
它是这一族的第九个成员（同为 Transformer 文本分数、同 cov 0.90 量级、同塔同乘数），
先验上比本集更差（字段更少、无置信区间族），**为它单独开波是重复已证伪的路径**。

---

## 7. 复现与索引

- 回测产物：8 个 alpha id 见 §4 表；表达式原文见 `backtest_results.code` /
  `expressions`（wave = `s2_finnews_nlp_scores_d1`）。
- 设置：`region=USA, universe=TOP3000, delay=1, decay=5, neutralization=SUBINDUSTRY,
  truncation=0.08, nanHandling=ON, unitHandling=VERIFY, startDate=2014-01-01, endDate=2023-12-31`。
- 交付日志：`_usa-atom-delivery-log-20261020.md` §K（预注册）/ §L（八臂收官）/ §M（fallback 退役 + 选区决策）。
- 本档与交付日志的分工：本档是**字段画像 + 单集判决**的可复用资产；交付日志是**战役时序**。
