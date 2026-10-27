# news_transformer_scores — USA / TOP3000 / D1 字段画像

> 平台抓取：2026-10-23，`get_datasets(search="news_transformer_scores")` + `get_datafields(dataset_id=...)`（315 行全量）。
> 本文所有数字均取自该次平台返回，不是估计。
> ⚠ 原始抓取落在本机临时缓存里（宿主会话私有目录，跨机不可用、也不应写进文档）；
> **重跑画像请直接取数**：`get_datafields(region=USA, universe=TOP3000, delay=1, dataset_id="news_transformer_scores")`。

## 0. 数据集头

| 项 | 值 |
|---|---|
| id / 名称 | `news_transformer_scores` / Transformer Based News Sentiment Scores |
| category | `sentiment`（SENTIMENT 塔，**本季未点亮**） |
| 覆盖率 | **0.7773**（数据集级；字段级只有 3 个取值，见 §2） |
| 字段数 | **315**，全部 `MATRIX`（**无 VECTOR ⇒ 不需要也不允许 `vec_*`**） |
| userCount | 136 |
| alphaCount | **279**（≈ 0.89 条/字段，低拥挤；但字段级分布极不均，见 §3） |
| valueScore / multiplier | 5 / 1.4（PPA_PASS 档） |
| 频率 | 日频（每条为"当日某时段新闻"的聚合）；D1 下三个时段都只作**前一日**信息使用 |
| 字段 id 前缀 | `negative_sentiment_*` / `positive_sentiment_*` / `neutral_sentiment_*` —— **不含数据集名**，必须按 `dataset_id` 查 |

## 1. 结构：一个完整的 7 × 3 × 3 × 5 全因子

315 = **7 个统计量** × **3 个极性** × **3 个时段** × **5 个措辞变体**（同一概念由供应商用 5 种字段名重复发布）。

| 统计量族 | 语义（来自字段 description） | 字段数 |
|---|---|---|
| `avg` | 该时段全部新闻的情绪均值（0–1 归一） | 45 |
| `sd` | 该时段新闻情绪的**离散度**（跨文章分歧） | 45 |
| `ci_top` | 均值的近似 95% 置信区间**上界** | 45 |
| `ci_floor` | 均值的近似 95% 置信区间**下界** | 45 |
| `min` | 该时段新闻情绪的**最小值**（最负面的一篇 / 对 positive 字段即最不正面） | 45 |
| `peak` | 该时段新闻情绪的**最大值** | 45 |
| `typical` | 该时段情绪的**中位数** | 45 |

> 更正一条早期误记：不是"15 个统计量"，是 **7 个统计量 × 5 个措辞变体**。每个 (极性, 时段) 单元恰好
> **35 个字段 = 7 × 5**，实测 9 个单元全部整 35（`_tmp_nts_cov.py` 的 cell 计数）。

## 2. 时段：覆盖率就是时段标识（100% 可靠）

字段级覆盖率**只有 4 个取值**，且与 description 的时段措辞完全一一对应：

| 覆盖率 | 字段数 | 时段 | description 关键词 |
|---|---|---|---|
| **0.8810** | 105 | **pre**（盘前） | "pre-market" |
| 0.7586 / 0.7585 | 63 + 42 = **105** | **main**（常规时段） | "main (regular-hours) session" / "during the trading session" |
| **0.6923** | 105 | **post**（盘后） | "post-market" |

交叉核验（`_tmp_nts_cov.py`）：按 description 判时段 vs 按覆盖率判时段，
`pre 105/105`、`main 97/97`、`post 104/104` 一致，只有 9 个字段 description **没写时段措辞**
（如 `negative_sentiment_confidence_floor_7`、`positive_sentiment_mean_value_2`），
它们的覆盖率仍精确落在 main（0.758×8）/ post（0.6923×1）档 —— **用覆盖率补判，零歧义**。

**可复用结论**：这个数据集的字段名 / 编号**不能**用来判时段，覆盖率可以。数值后缀是供应商内部编号，
跨极性不一致（证据见 §4）。

## 3. alphaCount 的分布：49% 的火力压在盘前，盘后是白空间

| 时段 | 字段数 | alphaCount 合计 | 占比 | 零 alpha 字段 |
|---|---|---|---|---|
| pre | 105 | **187** | 49.3% | 46 / 105 |
| main | 105 | 105 | 27.7% | 49 / 105 |
| post | 105 | **82** | 21.6% | 65 / 105 |
| （时段未标注） | — | 5 | 1.3% | 5 |
| 合计 | 315 | 379 | 100% | **165（52.4%）** |

- 全数据集 **165 / 315（52.4%）字段 alphaCount = 0**，其中 **46 个覆盖率 0.881（盘前）** ——
  即"最好时段 × 最空字段"这一格是白空间最集中处。
- 盘前 `negative avg` 是最拥挤的单点（aC 42）；盘后几乎无人用（aC 82 分散在 105 字段上）。
- **D1 语义提醒**：delay 1 下三个时段都是"前一日"信息，**不存在"盘后不可用"的问题**；
  盘后恰恰是**离次日开盘最近**的一段。所以"盘后白空间"不是数据缺陷，是选股口径上的真实缺口。

## 4. ⚠ 数值后缀不是时段键（踩过的坑，务必先读 description）

同后缀在不同极性下指向不同时段，实测反例：

| 字段 | 后缀 | 实际时段 | 覆盖率 |
|---|---|---|---|
| `negative_sentiment_average_10` | `_10` | **main** | 0.7586 |
| `positive_sentiment_average_10` | `_10` | **post** | 0.6923 |
| `negative_sentiment_average_12` | `_12` | **pre** | 0.881 |
| `positive_sentiment_average_pre5` | `_pre5` | pre | 0.881 |
| `positive_sentiment_standard_deviation_post` | `_post` | post | 0.6923 |

⇒ 建表达式前必须做两件事之一：读 description 关键词，或按覆盖率定档（§2）。
只按后缀猜 = 拿"盘后正向情绪"当"主时段正向情绪"，机制解释会整体错位。

## 5. 波 88 采用的 11 个字段（全部 description + 覆盖率双证）

| 字段 | 时段 | 统计量 | 极性 | cov | aC |
|---|---|---|---|---|---|
| `negative_sentiment_average_12` | pre | avg | neg | 0.881 | 42 |
| `negative_sentiment_average_10` | main | avg | neg | 0.7586 | 19 |
| `negative_sentiment_average_post` | post | avg | neg | 0.6923 | 2 |
| `positive_sentiment_average_pre5` | pre | avg | pos | 0.881 | 8 |
| `negative_sentiment_average_pre5` | pre | avg | neg | 0.881 | 10 |
| `negative_sentiment_standard_deviation_6` | pre | sd | neg | 0.881 | **0** |
| `positive_sentiment_standard_deviation_post` | post | sd | pos | 0.6923 | 7 |
| `negative_sentiment_confidence_top` | pre | ci_top | neg | 0.881 | 3 |
| `negative_sentiment_confidence_floor` | pre | ci_floor | neg | 0.881 | 5 |
| `negative_sentiment_peak_value` | pre | peak | neg | 0.881 | 2 |
| `negative_sentiment_typical_value` | pre | typical | neg | 0.881 | 1 |

## 6. 两个结构性可用点

### 6.1 CI 宽度 = 3.92/√n ⇒ 文章数的免费代理

字段 description 原文给出的是"mean ± 1.96 × std / sqrt(number of items)"。因此

```
width  = confidence_top − confidence_floor        （同一时段、同一措辞变体，必须配对）
width / sd = 2 × 1.96 / sqrt(n) = 3.92 / sqrt(n)
n ≈ (3.92 × sd / width)^2
```

这就是**唯一一个能表达"这只股票当天有几条新闻"的量**（数据集不直接发布 count 字段），
且 `ci_*` 与 `sd` 全部在 aC 0–5 的白空间。

- 用途：`trade_when` 的**注意力 / 可靠性门**——只在报道充分（n 大）的股票上交易情绪水平，
  避免"一条新闻定生死"的噪声样本。
- 门槛换算：`width/sd < 1.0` ⇒ n > 15.4；`< 0.7` ⇒ n > 31.4。
- ⚠ 配对纪律：`top` 与 `floor` 必须来自**同一时段同一变体**（例如都用 `_pre5` 系列或都用无后缀系列），
  跨时段配对算出来的是垃圾。波 88 用的是无后缀一对（`confidence_top` / `confidence_floor`），两者均 cov 0.881。

### 6.2 NaN → 0 语义陷阱（nanHandling=ON）

战役设置 `nanHandling=ON` ⇒ **没有新闻的日子该字段变成 0**。
对 `negative_sentiment_*`，0 意味着"负面情绪为零"= 看起来最好 ⇒ 纯水平腿会系统性做多"当天没新闻"的股票。

- 盘前覆盖率 0.881 ⇒ 约 12% 的零质量，不足以毁掉信号，但会污染多空两端的分位。
- 表达式层**难以检测**"原始是 NaN 还是真是 0"（`is_nan` 在 nanHandling 之后通常已看不到 NaN）。
  稳健做法：
  1. **极性差** `subtract(positive, negative)` —— 无新闻日两者同为 0，差值 0，落在中位，天然免疫（波 88 a7）；
  2. **同族比值 / 差值**（peak − typical，同一天同一批文章）—— 0 只在无新闻时同时为 0，差值仍 0；
  3. 需要完全隔离时单独起一批 `nanHandling=OFF` 的对照（尚未做，见 §9）。

## 7. 机制族（波 88 覆盖 4 个 + 1 个门控）

| 族 | 机制假设 | 字段 | 波 88 臂 |
|---|---|---|---|
| M1 水平反转 | 盘前/盘中负面语气在次日开盘未完全定价 ⇒ 负语气做多 | 三时段 `negative avg` | a1 / a2 / a3 |
| M1' 正向对照 | 正向语气应给出同向（做多高正向）——若符号相反则说明是"关注度"而非"语气" | `positive avg pre5` | a4 |
| M2 分歧溢价 | 同一批新闻内部语气越分裂（sd 高），信息不确定性越高 ⇒ 模糊厌恶折价，未来补涨 | `neg sd pre` / `pos sd post` | a5 / a6 |
| M3 净语气 | `pos − neg`，消灭中性质量与无新闻质量，直接是"多空天平" | pre5 一对 | a7 |
| M4 意外 | 负面语气相对**自身 22 日历史**的 z 分数（不是横截面 z，避免长尾爆掉） | `neg avg pre` | a8 |
| M4' 单篇驱动 | `peak − typical`：一天的语气被**一篇**极端文章拉动时，日度均值不可信 ⇒ 反向 | peak / typical（pre） | a9 |
| M5 注意力门控 | 只用报道充分的名字（§6.1） | CI 宽/sd 比值 | b1 (n>15) / b2 (n>31) |

符号约定：负面字段一律 `multiply(-1, …)` 再 `group_rank(…, subindustry)`，使**正值 = 做多**。

## 8. 波 88 发批记录（2026-10-23）

- 批次：`tracking/USA/runs/usa_nts_w88a.txt`（9 臂，机制族）＋ `usa_nts_w88b.txt`（2 臂，门控）
- spec：`tracking/USA/runs/usa_nts_w88_spec.json`；表达式快照：`logs/_w88_exprs.json`
- 设置：USA / TOP3000 / D1 / REGULAR / `decay 5` / `nanHandling ON` / `truncation 0.08` / 2014-01-01→2023-12-31 / `SUBINDUSTRY`
- 预检：算子 REGULAR 白名单 ✓（无幽灵算子）；315 字段存在性 ✓；语法 ✓；元数 11/11 ✓；平台 `validate_expressions` → `valid=true, unknown_fields=[]`
- 形状多样性：2 族（S5 ×7, S9 ×4）—— **低于 ≥3 族的准则，已知缺口**。
  取舍：首波目标是**机制归因**（同一骨架只换核，隔离字段效应）；算子壳替换留到胜出机制的波 2，避免首波就把
  "机制差异"和"算子差异"混在一起。
- 安全设计：`trade_when + less` 是这个数据集上的**新语法形态**，单独一个 parent 发（`w88b`），
  避免一条语法错连坐 9 条机制臂。

## 9. 未决问题 / 下一波要回答的

1. **盘后是否真的更肥**：post 时段 alphaCount 最低（82/105 字段），但信息最新。波 88 a3（post 水平）
   与 a1/a2 的三时段阶梯就是直接检验；若 post 明显强于 pre，下一波整体迁到 post。
2. **nanHandling=OFF 对照**：确认 §6.2 的零质量到底吃掉了多少夏普。这是设置层实验，需单独一批。
3. **措辞变体的重复度**：5 个变体应是同一概念的复制，但覆盖率有 0.7586 / 0.7585 的细微差异。
   若某变体系统性更好（如 `_pre5` 系），说明供应商后处理不同，值得作为独立核再测一次。
4. **CI 宽度的方向**：n 大 ⇒ 情绪更可信；但也可能 n 大 = 大市值/高关注 = 已被定价。
   a/b 的对比会同时带出"规模效应"与"可靠性效应"，需要 `cap` 分层做一次识别。

## 10. 跨数据集可复用结论

1. **字段族全景因子化**：遇到 300+ 字段的数据集，先数"统计量 × 极性 × 时段 × 变体"。若是整因子且
   覆盖率按时段分层，覆盖率本身就是分类键 —— 比按名字猜可靠得多，且一次就能算出白空间在哪一格。
2. **供应商数值后缀不可信**：同名后缀在不同极性下指向不同时段（§4）。任何"按编号推语义"的做法，
   在这个数据集上 100% 错位。
3. **CI 上下界是免费的样本量代理**：只要供应商发布 CI，`（上界−下界）/ 标准差` 就给出 `2z/√n`。
   这是构造"注意力/可靠性门控"的合法来源，不需要 count 字段。
4. **NaN→0 在"负面情绪"字段上是方向性污染**：0 不是中性，是"最好"。极性差 / 同族差值这类构造
   天然免疫，优先用；纯水平腿必须配门控或 nanHandling 对照。
