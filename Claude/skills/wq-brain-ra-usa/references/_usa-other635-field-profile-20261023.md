# USA / D1 `other635` 字段画像与机制台账（2026-10-23）

> **定位**：USA 未点亮塔补挖第 2 个数据集（`risk60` 判 prod 死后接续）。
> 平台类别 **OTHER（×1.4，0 颗 ACTIVE ⇒ 未点亮）**，满足「已点亮塔不作主数据集」用户规则（2026-09-19 定案）。
> 数据集级事实全部来自本地台账 `data/wqb.db`（`datasets` / `fields` / `expressions`）与平台
> `validate_expressions`（`field_exists` 实测），标注「未实测」的项不得当作已知。

## 1. 为什么选它（S0 选集理由，按用户规则先剔已亮塔）

同轮只读扫描（`logs/_tmp_unlit_variant_scan.py`，判据：USA/D1、排除 ANALYST 与 MODEL、
字段数 ≥ 4、按平台 `alpha_count` 升序）产出 44 个未点亮候选。`other635` 在其中同时满足四条：

| 判据 | 事实 | 为什么重要 |
|---|---|---|
| 塔位 | `datasets.category = OTHER`，该塔 0 颗 ACTIVE（`campaign_intel pyramid --region USA --delay 1` 实测快照） | 用户硬规则：已亮塔只作组腿辅助 |
| 拥挤度 | 数据集 aC **18**；三个情绪字段 aC 分别 **1 / 0 / 0** | 两个情绪字段在生产池里**零条** alpha 用过 |
| 结构 | 9 字段 = **三套平行供应商管线** × 三指标（字符数 / 词数 / 情绪） | 可造「跨供应商分歧」，即 ai_equity 实测 prod 0.64–0.69 的那类结构 |
| 覆盖 | 0.9929（三套管线分别 1.0 / 0.9993 / 0.9795） | VECTOR 但覆盖率接近满格，不属稀疏事件族 |

⚠ **aC 低不保证 prod 低**：`risk60` 的反例证明决定 prod 的是**机制拥挤度**而非数据集拥挤度（见
`_usa-risk60-field-profile-20261023.md` §7.2：aC 168 的字段 prod 0.9917）。因此本数据集的价值主张
不在「冷门」，而在**结构**——分歧构造在生产池里是稀有的（ai_equity 5 颗实测 0.64–0.69）。

## 2. 字段画像总表（9 字段，全 VECTOR）

| # | 字段 | 类型 | 覆盖 | 平台 aC | uC | 语义（平台原文） |
|---|---|---|---:|---:|---:|---|
| 1 | `oth635_sentiment` | VECTOR | 1.0000 | 1 | 1 | **Neural-derived** sentiment score for the event/title in [-1,1]（0 = 中性） |
| 2 | `headline_sentiment_score` | VECTOR | 0.9993 | **0** | 0 | Numerical sentiment score for the news headline, negative→positive |
| 3 | `headline_sentiment_score_benzinga` | VECTOR | 0.9795 | **0** | 0 | Sentiment in [-1,1]，negative = negative tone |
| 4 | `oth635_char_count` | VECTOR | 1.0000 | 1 | 1 | Unicode chars in `decode_title`（含空白，按码点计） |
| 5 | `headline_character_count` | VECTOR | 0.9993 | 9 | 7 | Chars in headline，**不含空格** |
| 6 | `headline_character_count_benzinga` | VECTOR | 0.9795 | 1 | 1 | Chars in `decode_title`，含空白（码点计） |
| 7 | `oth635_words_count` | VECTOR | 1.0000 | **0** | 0 | Tokens in `purify_title`（空白切分） |
| 8 | `headline_word_count` | VECTOR | 0.9993 | 5 | 1 | Words in headline/title |
| 9 | `headline_word_count_benzinga` | VECTOR | 0.9795 | **0** | 0 | Token count of `purify_title` |

**三套平行管线的识别依据**（不是猜的，是三组同名异前缀字段的语义对齐）：

| 管线 | 情绪 | 字符数 | 词数 | 推测来源 |
|---|---|---|---|---|
| A `oth635_*` | `oth635_sentiment`（**neural**） | `oth635_char_count` | `oth635_words_count` | 数据集自有、神经模型打分 |
| B `headline_*` | `headline_sentiment_score` | `headline_character_count` | `headline_word_count` | 另一供应商（词典式） |
| C `headline_*_benzinga` | `headline_sentiment_score_benzinga` | `headline_character_count_benzinga` | `headline_word_count_benzinga` | Benzinga |

**覆盖梯度 1.0 > 0.9993 > 0.9795** 与三套管线的覆盖面一致（自有 ≥ 供应商 B ≥ Benzinga），
是「三条独立数据源」的直接证据，而非同一序列的三次改名。

## 3. 数据类型与更新特征

- **全 VECTOR**：每条记录是当日该股的**多条标题**的向量，必须先聚合。
  `vec_avg` = 当日标题均值，`vec_max` = 当日最极端标题。**禁止**直接对 VECTOR 用 `ts_backfill` /
  `ts_*` / `group_*`——实测会整批 CANCELLED（见 `_usa-risk60-field-profile-20261023.md` §4 同源纪律）。
- **更新频率**：事件驱动（标题级），D1 快照；`delay = 1`。空值日以 0 或 NaN 体现（平台 side 未实测）。
- **分布**：情绪值域 [-1, 1]（`oth635_sentiment` 明示，另两个同量纲）；字符数 / 词数为正整数。
  ⚠ **「0 = 无新闻」与「0 = 中性」不可区分**——这是本数据集最重要的分布陷阱：
  分歧类构造里 `abs(a−b)=0` 同时代表「两供应商一致」与「当日无新闻」，会稀释信号。
  波 1 的 A10（词典间分歧）就是为测这一点设的控制臂。
- **可用性**：USA / TOP3000 / D1 **字段存在性已实测**（`validate_expressions` →
  `field_exists` 三项缓存命中，`unknown_fields = []`）。

## 4. 历史开采状况

`expressions` 表（region=USA, dataset=other635）：**12 条全部 `dropped`，无一条进入回测**。

```
quantile(rank(ts_backfill(vec_avg(oth635_sentiment), 66)))
quantile(subtract(ts_backfill(vec_avg(oth635_char_count), 66), ts_backfill(vec_avg(oth635_sentiment), 66)))
quantile(-ts_arg_max(ts_backfill(vec_avg(oth635_char_count), 66), 20))
quantile(-ts_arg_max(ts_backfill(vec_avg(oth635_sentiment), 66), 10))
...（共 12 条，2026-08-25）
```

这批是「字符数 − 情绪」「argmax 位置」之类的无机制拼接，且外壳 `quantile(...)` 缺参数
（`quantile` 仅支持 1 参数，见项目记忆），**从未真正验证过本数据集**。
⇒ 本数据集的**情绪分歧机制此前零回测**，不构成经验资产，也不构成判死证据。

## 5. 机制设计与波 1 预登记

### 5.1 三个候选机制

| 代号 | 构造 | 经济学假设 | 先验强度 |
|---|---|---|---|
| **H-disp** | `-ts_mean(abs(s_A − s_B), 22)` | 供应商分歧 = 信息不确定性 ⇒ 不确定性溢价（做空高分歧） | 中高（文献：分析师/预测分歧溢价；此处为机器打分歧） |
| **H-sign** | `±ts_mean(s_neural − s_lexicon, 22)` | 神经模型读到词典漏掉的语境（否定、反讽、条件句）⇒ 有符号差是私有信息 | 中（方向须双向对照） |
| **H-level** | `±ts_backfill(vec_avg(s), 66)` | 情绪水平本身（risk60 壳：原始水平不加 rank） | 中（情绪是最拥挤的机制之一，prod 风险高） |

### 5.2 波 1 十臂（`tracking/USA/runs/usa_oth635_w1.txt`）

设置：**USA / TOP3000 / D1 / MARKET / decay 8 / trunc 0.08 / nanHandling ON / 2014-01-01..2023-12-31**
（与 risk60 波 2A 冠军同设置，便于跨数据集比较形状效应）。
multisim：`28H7VC1qb4G49m3loRegYq`。

| # | 臂 | 机制 |
|---|---|---|
| A1 | `-ts_mean(abs(s_neural − s_dj), 22)` | H-disp（神经 vs 主供应商） |
| A2 | `-ts_mean(abs(s_neural − s_bz), 22)` | H-disp（神经 vs Benzinga） |
| A3 | `-ts_mean(两两差之和, 22)` | H-disp 三供应商总分歧 |
| A4 | `+ts_mean(s_neural − s_bz, 22)` | H-sign + |
| A5 | `-ts_mean(s_neural − s_bz, 22)` | H-sign −（方向对照） |
| A6 | `+ts_backfill(vec_avg(s_neural), 66)` | H-level + |
| A7 | `-ts_backfill(vec_avg(s_neural), 66)` | H-level −（方向对照） |
| A8 | `-group_zscore(ts_mean(abs(s_neural − s_dj), 22), sector)` | H-disp 壳层对照 |
| A9 | `-ts_backfill(vec_avg(s_bz), 66)` | 供应商对照（aC=0 字段） |
| A10 | `-ts_mean(abs(s_dj − s_bz), 22)` | **控制臂**：两词典之间的分歧（同源则应 ≈0） |

**预登记判据（发批前写死）**：`RA 全过`（含 `S ≥ 1.58`、`F ≥ 1.0`、`SUB/S ≥ 0.435`）；
任一条过闸 ⇒ **立即做 prod 探针**，不先做同族扩展，避免重演 risk60「16 臂全过 RA 却 prod 0.9917」。
A10 若 `S` 与 A1/A2 同量级，说明分歧构造只是在测「有无新闻」而非「供应商分歧」，H-disp 需重解释。

### 5.3 波 1 实测（2026-10-23 收批，10/10）

| 臂 | 机制 | alpha | S | F | TO | RET | 2Y | SUB | SUB/S | RN |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A10 | 词典间分歧 − | `RRAlMPra` | **−0.86** | −0.42 | 12.98% | −3.1% | −0.64 | −0.70 | 0.814 | **−0.71** |
| A3 | 三供应商总分歧 − | `KPm53ZnN` | −0.60 | −0.26 | 13.16% | −2.5% | −0.26 | −0.42 | 0.700 | **−0.77** |
| A1 | 神经 vs 主供应商分歧 − | `E5V81xg9` | −0.43 | −0.15 | 12.41% | −1.5% | −0.03 | −0.20 | 0.465 | −0.26 |
| A2 | 神经 vs Benzinga 分歧 − | `LL5mW3n6` | −0.39 | −0.14 | 12.95% | −1.6% | −0.20 | −0.23 | 0.590 | −0.60 |
| A8 | 分歧 sector-zscore | `MP0eOVkz` | −0.38 | −0.12 | 12.59% | −1.2% | 0.26 | −0.12 | 0.316 | −0.19 |
| A6 | 水平 +（神经） | `O0JMOgob` | −0.24 | −0.05 | 26.86% | −1.2% | −0.55 | −0.32 | 1.333 | 0.25 |
| A9 | 水平 −（Benzinga） | `2rjXMeK8` | −0.23 | −0.08 | 12.29% | −1.4% | 0.25 | 0.12 | −0.52 | −0.42 |
| A5 | 有符号分歧 − | `qMEY8Vg1` | 0.10 | 0.02 | 13.45% | 0.6% | −0.65 | 0.07 | 0.700 | −0.19 |
| A4 | 有符号分歧 + | `leM5d17N` | −0.10 | −0.02 | 13.45% | −0.6% | 0.65 | −0.07 | 0.700 | 0.19 |
| A7 | 水平 −（神经） | `gJWg6LxQ` | 0.24 | 0.05 | 26.86% | 1.2% | 0.55 | 0.32 | 1.333 | −0.25 |

**最强臂 |S| = 0.86（A10），距 1.58 差 1.8 倍 —— 判死。** 五条归因（按证据强度排序）：

1. **方向是统一反的**：5 个分歧臂**全为负**（−0.38…−0.86）⇒ 取反后 `+分歧` 全为正（0.38…0.86）。
   即在美国新闻场景，**供应商分歧越大，未来收益越高**（分歧 ≈ 新闻事件强度/关注度，带动量性质），
   「不确定性溢价 ⇒ 做空高分歧」的教科书先验在本数据集上**方向反了**。
2. **A10 是全波最强臂，说明分歧是真实信息**：两个词典供应商的分歧（−0.86）大于神经 vs 词典（−0.43），
   ⇒ ① 三套管线**确非重复序列**（控制臂假设成立，`abs(a−b)` 不为 0）；② 词典式打分的实现差异比
   「神经 vs 词典」的模型差异携带更多信息。
3. **但有符号分歧无信息**：A4/A5 = ±0.10，`2Y` 在正负之间整体翻转（−0.65 / +0.65），
   ⇒ 神经−词典的**方向差**不是信号（H-sign 判否）。差分的**绝对值**有信息、**符号**没有。
4. **自相关风险暴露**：分歧臂 `RN` = −0.60…−0.77，`risk_neutralized_sharpe` 与 S 同量级，
   ⇒ 这不是异象 alpha，是**风格暴露**（≈ 关注度/波动率风格）。这解释了为什么它够不到 1.58。
5. **水平臂在 66 日平滑下≈0**（±0.24，TO 27%）：新闻情绪衰减远快于 66 日，长窗把信号洗掉。
   若改短窗，换手会飙过 60% 且 F 仍受制于 S —— 属于「换窗不改上限」，不投入。

**与 ai_equity 分歧结构的对照（本波最重要的跨数据集结论）**：

> ai_equity 的分歧（`predicted_earnings_surprise_2 − _3`）能到 S 2.19–2.67、prod 0.64–0.69，
> 因为**两条腿都是对同一目标的高信息量预测**，差分提取的是「模型私有信息的不一致」。
> 本数据集把同一构造用在**新闻情绪分类器**上：差分提取的是「分词器/词典的标注差异」，
> 其经济含义退化为**新闻强度**——所以方向反了、RN 塌到风格、上限 0.86。
> **判据（可复用）**：分歧构造要求两条腿都是**对收益的预测**，而不是**对文本的打分**。

## 5.4 裁决：停投（2026-10-23）

- 情绪三字段（`oth635_sentiment` / `headline_sentiment_score` / `headline_sentiment_score_benzinga`）
  **停投**：三机制（disp / sign / level）全部实测，最强 0.86 且为风格暴露。
- 长度四字段（`char_count` × 2 / `words_count` × 2）**不投入**：attention 代理是文本类最拥挤的
  特征族，且本数据集已验证「文本类差分 = 风格」；追加回测只会重复 0.5–0.9 的结局。
- 本数据集**不产出交付件**，塔位 OTHER 仍为 0 颗 ACTIVE（未点亮状态未被消耗）。

---

## 6. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-other635-field-profile-20261023.md`
- 波 1：`tracking/USA/runs/usa_oth635_w1.txt` / `usa_oth635_w1_spec.json`，
  multisim `28H7VC1qb4G49m3loRegYq`，结果落 `backtest_results` wave=`oth635_w1`
- 选集扫描：`logs/_tmp_unlit_variant_scan.py`（只读，44 个未点亮候选按 aC 升序）
- 前置判死记录：`_usa-risk60-field-profile-20261023.md` §7.2（prod 0.9917 + other143 0.8658）
- 交付报告：`output_report/USA_regular_alpha_delivery_20261021.md`（§8 起为未点亮塔补挖段）
