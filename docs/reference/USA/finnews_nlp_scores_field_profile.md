# USA · `finnews_nlp_scores` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 105 |
| 平台声明数 `platform_count` | 105 |
| 返回 `count` | 105 |
| 是否完整 `complete` | True |
| 类型分布 | {'MATRIX': 105} |
| 平均 coverage | 1.0000 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| ≥0.90（可直接做尽） | 105 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 零竞争 | 68 |
| 低拥挤（≤50 alpha） | 37 |

零竞争字段（`userCount==0`）：**68** / 105；描述带单位标注：0

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 未归类 | 105 | `average_negative_sentiment_score_1`, `average_negative_sentiment_score_2`, `average_negative_sentiment_score_3`, `average_negative_sentiment_score_4` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 84 |
| forecast | 21 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `lower_confidence` | 15 |
| `upper_confidence` | 15 |
| `average_negative` | 5 |
| `average_neutral` | 5 |
| `average_positive` | 5 |
| `maximum_negative` | 5 |
| `maximum_neutral` | 5 |
| `maximum_positive` | 5 |
| `median_negative` | 5 |
| `median_neutral` | 5 |
| `median_positive` | 5 |
| `minimum_negative` | 5 |
| `minimum_neutral` | 5 |
| `minimum_positive` | 5 |
| `stddev_negative` | 5 |

## 5 候选短名单（Top 25，按打分排序）

打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `median_negative_sentiment_score_3` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median of negative polarity scores across Dow Jones Newswires stories linked to the stock… |
| 2 | `median_negative_sentiment_score_5` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median negative sentiment score (0–1) across Dow Jones Newswires stories linked to the st… |
| 3 | `median_neutral_sentiment_score_2` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median neutral sentiment polarity score across Dow Jones Newswires stories linked to the … |
| 4 | `median_neutral_sentiment_score_3` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median of neutral polarity scores across Dow Jones Newswires stories linked to the stock … |
| 5 | `median_neutral_sentiment_score_4` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median of neutral sentiment (polarity) scores across stories mapped to the stock on that … |
| 6 | `median_neutral_sentiment_score_5` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median neutral sentiment score (0–1) across Dow Jones Newswires stories linked to the sto… |
| 7 | `median_positive_sentiment_score_3` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median of positive polarity scores across Dow Jones Newswires stories linked to the stock… |
| 8 | `median_positive_sentiment_score_4` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median of positive sentiment (polarity) scores across stories mapped to the stock on that… |
| 9 | `median_positive_sentiment_score_5` | MATRIX | 1.000 | 0 | 0 | 未归类 | forecast | 70.0 | Median positive sentiment score (0–1) across Dow Jones Newswires stories linked to the st… |
| 10 | `average_negative_sentiment_score_2` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average (mean) negative sentiment polarity score across Dow Jones Newswires stories linke… |
| 11 | `average_negative_sentiment_score_3` | MATRIX | 1.000 | 10 | 13 | 未归类 | forecast | 65.0 | Mean negative polarity score across Dow Jones Newswires stories linked to the stock on th… |
| 12 | `average_negative_sentiment_score_4` | MATRIX | 1.000 | 2 | 3 | 未归类 | forecast | 65.0 | Mean negative sentiment (polarity) score across stories mapped to the stock on that day |
| 13 | `average_negative_sentiment_score_5` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average negative sentiment score (0–1) across Dow Jones Newswires stories linked to the s… |
| 14 | `average_neutral_sentiment_score_1` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average (mean) neutral sentiment score across all mapped Dow Jones Newswires stories for … |
| 15 | `average_neutral_sentiment_score_2` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average (mean) neutral sentiment polarity score across Dow Jones Newswires stories linked… |
| 16 | `average_neutral_sentiment_score_3` | MATRIX | 1.000 | 1 | 1 | 未归类 | forecast | 65.0 | Mean neutral polarity score across Dow Jones Newswires stories linked to the stock on tha… |
| 17 | `average_neutral_sentiment_score_4` | MATRIX | 1.000 | 1 | 1 | 未归类 | forecast | 65.0 | Mean neutral sentiment (polarity) score across stories mapped to the stock on that day |
| 18 | `average_neutral_sentiment_score_5` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average neutral sentiment score (0–1) across Dow Jones Newswires stories linked to the st… |
| 19 | `average_positive_sentiment_score_2` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average (mean) positive sentiment polarity score across Dow Jones Newswires stories linke… |
| 20 | `average_positive_sentiment_score_3` | MATRIX | 1.000 | 6 | 6 | 未归类 | forecast | 65.0 | Mean positive polarity score across Dow Jones Newswires stories linked to the stock on th… |
| 21 | `average_positive_sentiment_score_4` | MATRIX | 1.000 | 1 | 2 | 未归类 | forecast | 65.0 | Mean positive sentiment (polarity) score across stories mapped to the stock on that day |
| 22 | `average_positive_sentiment_score_5` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Average positive sentiment score (0–1) across Dow Jones Newswires stories linked to the s… |
| 23 | `lower_confidence_negative_sentiment_4` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Lower bound of the 95% confidence interval for the mean negative sentiment (polarity) sco… |
| 24 | `lower_confidence_neutral_sentiment_1` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Lower 95% confidence bound for the daily mean neutral sentiment score (polarity in [0,1])… |
| 25 | `lower_confidence_neutral_sentiment_3` | MATRIX | 1.000 | 0 | 0 | 未归类 | - | 65.0 | Lower 95% confidence bound for the mean neutral polarity score for the stock that day |

---

## 6 结构解读与实测结论（人工补充，2026-10-28）

> 第 1–5 节由脚本机械生成，对新闻情绪词汇无法分族（105 字段全「未归类」），
> 且把 `_1.._5` 变体误当独立前缀族。真正可用的结构在下面这一节。

### 6.1 真实结构 = 7 聚合 × 3 极性 × 5–6 变体

字段名严格是 `{聚合统计}_{极性}_{变体}`，**但 confidence 族缺 `_score` 后缀**，这是最容易写错的点：

| 聚合统计 | 命名形态 | 变体 |
|---|---|---|
| `average` / `median` | `average_{neg\|neutral\|positive}_sentiment_score_{1..5}` | 1–5（全） |
| `maximum` | `maximum_negative_sentiment_score_{2..6}` / `..._neutral_..._{1..5}` / `..._positive_..._{2..6}` | 缺 1（neg/pos）|
| `minimum` | `minimum_negative_sentiment_score_{1..5}` / `..._neutral_..._{1..5}` / `..._positive_..._{2..6}` | 缺 1（pos）|
| `stddev` | `stddev_negative_sentiment_score_{1..5}` / `..._neutral_..._{2..6}` / `..._positive_..._{2..6}` | 缺 1（neu/pos）|
| `lower_confidence` / `upper_confidence` | `{lower\|upper}_confidence_{neg\|neutral\|positive}_sentiment_{1..5}` | **无 `_score`** |

合计 15+15+15+15+15+15+15 = **105**。
`stddev_positive_sentiment_score_1` **不存在**（preflight 判 `unknown_fields`），同类缺口还有
`maximum_neutral_sentiment_score_6` / `stddev_neutral_sentiment_score_1` 等——**写表达式前必须逐字段核**。

### 6.2 变体的语义标签（来自 description）

| 变体 | 标签 | 含义差异 |
|---|---|---|
| `_1` | *across all mapped stories* | 全量映射口径 |
| `_2` | *GLOBAL, variant 2, D1* | 另一套全局口径，与 `_1/_3` 非同源 |
| `_3` | *stories linked to the stock on that day* | 使用者最多（`average_negative_3` 有 10 用户 / 13 alpha）＝事实上的标准口径 |
| `_4` | *stories mapped to the stock on that day* | 与 `_3` 描述几乎同义，疑为不同版本 |
| `_5` | *score (0–1)* | **量纲不同**（概率型，取值 [0,1]），不可与其它变体做差 |
| `_6` | *observed among stories for the stock* | 仅 max/min/stddev 有 |

⇒ **跨变体做 `subtract` 是口径混用**；同变体内做差才是同源差分。`_5` 因量纲特殊，只宜做组内 rank。

### 6.3 拥挤度结构（本数据集最大的优势）

- **68 / 105 字段 `userCount == 0`**（零竞争），37 字段属低拥挤（≤50 alpha）
- 最高拥挤字段仅 `average_negative_sentiment_score_3`（13 alpha）
- 对比：`news12` 179,938 / `insiders3` 33,843 / `analyst7` 82,056
- 全字段 `coverage = 1.0`、类型全 MATRIX、无 VECTOR

### 6.4 机制假设与实测（波 143，decay0 / STATISTICAL / TOP3000 / trunc0.08 / `market` 分组轴）

| # | 机制 | 表达式骨架 | S | F | TO | 2Y |
|---|---|---|---|---|---|---|
| F1 | 分歧度（Miller 1977：分歧→高估→负收益） | `group_rank(subtract(lower_confidence_positive_sentiment_3, upper_confidence_positive_sentiment_3), market)` | −1.46 | −0.24 | 110.9% | −1.69 |
| F2 | 净极性水平（PEAD 式漂移） | `group_rank(subtract(average_positive_sentiment_score_3, average_negative_sentiment_score_3), market)` | **0.03** | 0.00 | 111.1% | 0.68 |
| F3 | 语气离散度（分歧度第二度量） | `group_rank(reverse(stddev_positive_sentiment_score_5), market)` | −1.33 | −0.21 | 110.9% | −1.55 |
| F4 | 单日最强负向（尾部事件） | `group_rank(maximum_negative_sentiment_score_6, market)` | −0.58 | −0.07 | 105.3% | 0.50 |

**三条结论（与 `event_return_model` 的信息结构正相反）：**

1. **一阶矩无效、二阶矩有效。** 净极性 `S = 0.03`（等价于纯噪声），而两个分歧度指标
   `|S| > 1.3`。新闻情绪的价值全在「意见分散程度」，不在「看多看空」。
2. **分歧度符号与美国样本反向。** F1/F3 都强烈为负 ⇒ 翻正后
   **置信宽度 `S +1.46 / 2Y +1.69`**、**语气离散度 `S +1.33 / 2Y +1.55`**。
   即「分歧越大 → 未来收益越高」，与 Miller 高估假说的方向相反。
   数学上 `group_rank(−x) = 1 − group_rank(x)`，去均值后权重精确反号，故翻正后的指标
   **可直接由已跑结果取负得到，无需重跑**。
   ⚠ 待核混杂：95% CI 宽度 = `3.92·σ/√n`，因此「宽度大」同时可能是「当日新闻条数少」；
   F2 净极性≈0 说明信号不像单纯的「有无新闻」，但该混杂尚未用「新闻条数」字段（本集未提供）独立证伪。
3. **共同病灶是 TO ≈ 110%。** `fitness = S·√(R/max(TO,0.125))`，在 TO=1.10 下
   F=1.0 需 `R≈52%`（S 取 1.46），**数学上不可能达标** ⇒ 任何后续实验的第一优先级都是压换手。
   按波 142 的实测结论，**优先用表达式层 `ts_mean`，不要用设置层 `decay`**（同 TO 档位下
   `ts_mean` 给 S +49% / F +88%）。

### 6.5 尚未使用的字段族（留待后续）

- `median_*` 全族（15 字段，本身是抗极值的极性估计，可做 F2 的稳健替代）
- `minimum_*` 全族（15 字段，尾部乐观/悲观，与 `maximum_*` 镜像）
- `*_neutral_*` 全族（占 35 字段，测试「无方向信息 = 无催化剂」假设）
- `_2` 变体的 GLOBAL 口径（与 `_1/_3` 非同源，可做同机制跨口径稳健性验证）
