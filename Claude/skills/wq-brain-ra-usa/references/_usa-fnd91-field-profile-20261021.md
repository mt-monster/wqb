# fundamental91（Quantitative Filings Data）字段画像 · 字段八问

> 命名：`_usa-<字段前缀>-field-profile-<asOf>.md`，前缀 = 平台字段前缀 **fnd91**
> **as_of**：2026-10-21 ｜ 状态：**探针进行中**（见 §4）
> 上游选区依据：`_usa-fnd21-field-profile-20261021.md` §0 全 23 个 USA Fundamental 数据集排序 + fnd21 封存后的 §10 去向

---

## §0 为什么是 fnd91

### 0.1 承接关系

| 项 | fnd21（已封存） | fnd91（本集） |
|---|---|---|
| 内容 | ESG **news** 分数（新闻派生的情绪） | **8-K 申报文本**解析（SEC filings 文本分析） |
| 与平台生产池关系 | 异源（news vs value/quality） | **更异源**：文本披露特征，平台池以数值基本面为主 |
| 字段结构 | 142 字段，同一族三时间尺度 | 407 字段，**46 基础字段 + 341 分节字段** |
| 已投入 | 3 波 / 18 条 / 7 机制 / **0 过闸** | 本文件起算 |

**选它的三条硬理由**：

1. **内容异源**：8-K 文本分析属 **disclosure / text-as-data** 家族，与 value / quality / momentum / analyst 全部异源。论坛实证定律「PC 是数据源内容决定的，不是构造决定的」（`36680834830743`）⇒ 这是结构性降 PC 的杠杆，不是靠算子调出来的。
2. **字段量可穷尽且结构清楚**：407 字段看似多，但 **46 个基础字段覆盖全部机制面**（sentiment / readability / size / numeric / topic / lag），其余 341 个是 13 个申报**分节（cat0–cat14）**的同一套指标复刻 —— 即「1 套机制 × 13 个节」。与 fnd21 的「24 主题 × 3 层」同构，但基础层更小、更可控。
3. **自带一个 fnd21 没有的机制**：`metric0/*` 与 `metric1/*` 是**披露文本相似度** —— 当前申报 vs **上一季**（metric0）、vs **去年同季**（metric1），"higher means more similar"。这是 Brown & Tucker (2011) 的 year-over-year MD&A modification 口径，直接测「这次财报的措辞是不是换了」——**信息含量的直接代理**，而不是从价格反推。

### 0.2 一处必须承认的排序偏离

§0 原表把 fnd91 列为「备选（字段量大）」而把 fnd22（ESG 14 字段）排在前面。实际取数后改判 fnd91 优先，理由：fnd22 全 VECTOR 且描述不可读、14 字段撑不起一套机制；fnd91 在**字段可读性**上远胜（每个字段都有明确语义），而「字段量大」的顾虑被 §1.2 的结构发现消解 —— **341 个分节字段是 26 个基础字段的 13 次重复**，不是 341 个独立假设。

---

## §1 字段全景（407 platform / 395 过 sharpe 过滤 / **46 基础 + 341 分节 + 35 另名前缀**）

### ① 是什么
SEC **8-K**（当期重大事件报告）的文本解析。每个字段是「该申报**当日**的文本度量」，按向量（一次申报可能含多个 8-K item）返回。`fnd91_period` = 该申报覆盖的**财季末日期** ⇒ 数据本质是**季度事件 + 日频传播**。

### ② 类型
**全部 VECTOR（395/395）**。⇒ 任何标量算子前必须先聚合。本批统一 `vec_avg`（文本分数的 item 均值）；Wave 2 起按 fnd21 实证加 `vec_max` / `vec_min` 对照。

### ③ 覆盖（三档，界限极清晰）

| 档 | cov | 字段 |
|---|---:|---|
| 满档 | **0.8664** | `measure_0..4`、`numeric_count`、`readability_0..2`、`sentiment1_0`、`sentiment2_0`、`8k_kic`(标识符) |
| 次档 | **0.8658** | `sentiment1_1..9`、`sentiment2_3/4` |
| 主题档 | 0.57–0.86 | `topic_0..19`（20 个主题暴露度，逐主题不同） |
| 申报层 | **0.6578** | `doccount`、`kic`(标识符)、`period`(日期)、`filing_availability_lag_days` |
| 质量旗 | 0.6430 | `valid_mapping`（1=映射可信 / 0=不可信，**不是信号**） |

覆盖中位数 0.640，51 字段 <0.4（全在分节层）。**基础层 46 字段里只有 2 个低于 0.64**（`topic_0` 0.640 / `topic_1` 0.574）⇒ 基础层几乎无低覆盖风险，无需 backfill 兜底。

### ④ 更新频率（本集最关键的结构事实）

- 名义：**季度**（`period` = 财季末）；
- 实际：**申报事件驱动** —— 值只在 8-K 落地日变，其余交易日按最近一次申报传播；
- `filing_availability_lag_days` = 财季末到 file-as-of 日的天数（cov 0.658）⇒ **披露时滞本身是一个独立信号**。

⇒ 后果：`ts_delta` / `ts_zscore` 在两次申报之间恒为 0，信号是**稀疏事件型**。这决定了 §2 的设计骨架（Change 必须配 `ts_backfill` 把事件后漂移窗口拉长），也预埋了 §3 的幅度风险（事件稀疏 ⇒ 换手低 ⇒ 收益可能低 ⇒ F 公式卡死，fnd21 同型死法）。

### ⑤ 量纲 / 分布（未做 Labs 直读，只做机制判读）

- **计数型**：`measure_0`(句数) / `measure_1`(音节) / `measure_2`(复杂词) / `measure_3`(长词) / `measure_4`(总词数) / `numeric_count` / `sentiment1_0`(过滤后词数) → **取值为正整数，强右偏，随公司规模/申报长度漂移**。⇒ 单独用是「公司规模」代理，**必须比值化**（`numeric_count / measure_4`、`*_pos / sentiment1_0`）。
- **分数型**：`sentiment1_1..9`（三模型 × 正/负/中性）与 `sentiment2_0` → 若为计数则同样需除以 `sentiment1_0`；描述写 "score" 的按分数处理。**本批对两者都做了归一化防错**。
- **可读性**：`readability_0/1/2` 描述未逐条给出（`readability_<0,1,2>`）。分节版描述明确 `sentiment2_3` = **Flesch-Kincaid**、`sentiment2_4` = **Gunning Fog** ⇒ 基础 `readability_*` 极可能是同一组指标（Flesch Reading Ease / FK / Fog）。**方向未定，故 Wave 1 同时测正反两号**（见 A1/A2）。
- **相似度**：`metric0/1_*` 范围应是 [0,1]，**越高越相似**（描述明写），方向已定。
- **主题暴露**：`topic_*` 为暴露度分数，方向未定（取决于主题）。

### ⑥ 可用性
- ✅ 基础层 46 字段全部可用、覆盖足够、aC 低（`sentiment2_0` aC 23 / `measure_3` aC 23 / `readability_0` aC 15 为最高档；**大量字段 aC 0–7**）。
- ⛔ **不可作信号**：`8k_kic` / `kic`（SEC CIK 标识符）、`period`（日期）、`valid_mapping`（质量旗，只可作 `trade_when` 门控或弃用）。
- ⚠ **拥挤点**：`topic_4`（uC 34 / aC 64）、`topic_18`（uC 33 / aC 41）—— 这两个主题已被反复用，**不作首选**；选 `topic_17`(aC 4) / `topic_14`(aC 6) 这类低拥挤主题。
- ⚠ **分节层 341 字段**：aC 几乎全为 0（未开发），但覆盖 0.31–0.66 且命名有**三套不统一前缀**（`fnd91_catN_*` / `catN_primary_*` / `catN_section_metric1_*_value`）。同一逻辑字段在不同节可能换名 ⇒ **直接引用前必须回 `get_datafields` 核字面 id**（本文件已用真 id，不再靠推断）。

### ⑦ 命名拆解

```
fnd91_<family>_<index>                     基础层（46）
fnd91_cat<N>_<family>_<index>              分节层（13 节 × 26 字段）
cat<N>_primary_sentiment_score<i>          分节层「另名」前缀（35 个，无 fnd91_）
cat<N>_section_metric1_<i>_value           分节层相似度「另名」前缀
```

| family | 含义 | 量 |
|---|---|---:|
| `sentiment1_0..9` | 模型 1/2/3 各出 正/负/中性 三分数 + `_0` 过滤后词数 | 10 |
| `sentiment2_0/3/4` | 家族 2 正分 + 2 个复杂度（FK / Fog） | 3 |
| `readability_0..2` | 可读性三指标 | 3 |
| `measure_0..4` | 句数 / 音节 / 复杂词 / 长词 / 总词数 | 5 |
| `numeric_count` / `doccount` | 数字个数 / 附件数 | 2 |
| `topic_0..19` | 20 个预定义主题暴露度 | 20 |
| `metric0_*` | 相似度：当前 vs **上一季** | 3/节 |
| `metric1_*` | 相似度：当前 vs **去年同季** | 3/节 |
| `filing_availability_lag_days` | 财季末 → 申报可用日 | 1 |
| `cnt0..5` / `*_feature_count*` | 分节 POS 词性计数 | 6/节 |

**13 个分节（cat0–cat14，缺 cat9）**：cat6（cov 0.305–0.354）与 cat10（0.320–0.370）覆盖最差，**不作独立信号**；cat11/cat13/cat14 覆盖 0.58–0.66 最好。

### 1.1 基础层 46 字段全表（按覆盖降序）

| 字段 | cov | uC | aC | 机制含义 |
|---|---:|---:|---:|---|
| `fnd91_measure_0` | 0.8664 | 6 | 7 | 句数 |
| `fnd91_measure_1` | 0.8664 | 7 | 8 | 音节数 |
| `fnd91_measure_2` | 0.8664 | 3 | 6 | 复杂词数 |
| `fnd91_measure_3` | 0.8664 | 19 | 23 | 长词数 |
| `fnd91_measure_4` | 0.8664 | 4 | 7 | 总词数 |
| `fnd91_numeric_count` | 0.8664 | 3 | 3 | 数字个数 |
| `fnd91_readability_0/1/2` | 0.8664 | 14/2/11 | 15/2/15 | 可读性（疑 FRE / FK / Fog） |
| `fnd91_sentiment1_0` | 0.8664 | 1 | 2 | 过滤后词数（**归一化分母**） |
| `fnd91_sentiment1_1/2/3` | 0.8658 | 7/3/2 | 7/3/2 | 模型 1 正 / 负 / 中性 |
| `fnd91_sentiment1_4/5/6` | 0.8658 | 4/2/8 | 4/2/13 | 模型 2 正 / 负 / 中性 |
| `fnd91_sentiment1_7/8/9` | 0.8658 | 1/1/4 | 3/1/7 | 模型 3 正 / 负 / 中性 |
| `fnd91_sentiment2_0` | 0.8664 | 20 | 23 | 家族 2 正分（**最拥挤的基础情绪字段**） |
| `fnd91_sentiment2_3/4` | 0.8658 | 3/8 | 4/10 | FK / Gunning Fog |
| `fnd91_topic_0..19` | 0.57–0.86 | 0–34 | 0–64 | 20 主题暴露度 |
| `fnd91_doccount` | 0.6578 | 1 | 1 | 附件数 |
| `filing_availability_lag_days` | 0.658 | 12 | 12 | 披露时滞（天） |
| `fnd91_valid_mapping` | 0.6430 | 0 | 0 | 映射质量旗（**非信号**） |
| `fnd91_kic` / `8k_kic` | 0.658/0.866 | 0/13 | 0/16 | SEC CIK（**标识符**） |
| `fnd91_period` | 0.6578 | 1 | 1 | 财季末日期（**日期**） |

### 1.2 分节层（341 字段）—— 关键结构发现

| 节 | n | cov | aC | 判读 |
|---|---:|---|---|---|
| cat0 | 26 | 0.586–0.655 | 0–5 | 覆盖尚可、完全未开发 |
| cat1 | 27 | 0.541–0.616 | 0–**15** | `metric0_0` aC 15，**本集最拥挤的分节字段** |
| cat2 | 27 | 0.579–0.649 | 0–2 | 空白 |
| cat3 | 26 | 0.587–0.656 | 0–5 | 空白 |
| cat4 | 27 | 0.541–0.613 | 0–4 | 空白 |
| cat5 | 27 | 0.492–0.572 | 0–2 | 覆盖偏低 |
| **cat6** | 26 | **0.305–0.354** | 0–1 | **覆盖最差 ⇒ 不作独立信号** |
| cat7 | 27 | 0.581–0.652 | 0–1 | 空白 |
| cat8 | 26 | 0.586–0.655 | 0–13 | `metric1_1` aC 13（相似度已被用） |
| **cat10** | 25 | **0.320–0.370** | 0–7 | **覆盖最差 ⇒ 不作独立信号** |
| cat11 | 26 | 0.576–0.645 | 0–3 | 覆盖好、空白 |
| cat12 | 27 | 0.508–0.576 | 0–2 | 空白 |
| cat13 | 25 | 0.589–0.658 | 0–5 | 覆盖最好、空白 |
| cat14 | 6 | 0.658 | 0–4 | 只有 POS 计数，无情绪/相似度 |

**取舍**：分节层**不进 Wave 1**。理由不是覆盖（多数够 0.6），而是**机制重复** —— 同一套 sentiment/readability 在 13 个节上各算一次，先用基础层定位「哪类机制活着」，再决定往哪个节下沉。这与 fnd21 的「先核心族后子主题」同一顺序。

---

## §2 机制假设（映射到 6 桶）

| 桶 | 机制 | 经济叙事 | 字段 | 本批表达式 |
|---|---|---|---|---|
| **Level** | 文本可读性 | 披露越晦涩（Fog/FK 越高）⇒ 坏消息被藏 ⇒ 后续负收益（Li 2008） | `readability_0/2` | A1 / A2 |
| **Level** | 净语气 | 8-K 正负词差 ⇒ 公告后漂移（Loughran-McDonald） | `sentiment1_4/5` ÷ `sentiment1_0` | B1 |
| **Level（对照）** | 量化密度 | 数字占比越高 ⇒ 披露越具体（不是空话） | `numeric_count / measure_4` | C1 |
| **Level** | 披露时滞 | 越晚报 ⇒ 治理越差（或坏消息拖延） | `filing_availability_lag_days` | D1 |
| **Level** | 主题暴露 | 增发（Dilution）主题暴露高 ⇒ 稀释预期 | `topic_17` | E1 |
| **Change** | 晦涩度跳变 | 同一公司可读性突变 ⇒ 文本在掩盖或披露新东西 | `readability_2` Δ22 + backfill 66 | A3 |
| **Change** | 语气变化 | 语气环比改善 ⇒ 资金流 | 净语气 Δ66 + backfill 66 | B2 |
| **Surprise** | 语气相对自身历史 | 本次申报语气 z 分（预期差） | `sentiment2_0` z252 | B3 |
| **Event-conditioned** | 只在异常冗长日暴露 | 异常长度 = 异常披露 ⇒ 才值得交易 | `measure_4` z252 > 1 门控 A1 | F1 |

**结构选择说明**：
- **Level 占 5 条**看似偏多，但每一条是**不同字段族**（可读性 / 情绪 / 量化密度 / 时滞 / 主题），不是同一机制的重复壳 —— 与 fnd21 Wave1 的「8 条 7 机制」同密度。
- **相似度（`metric0/1`）故意不进 Wave 1**：它是本集最有价值但最贵的机制（需先确定哪一节有信息），留到 Wave 2 单独立批，避免 Wave 1 被 13 个节的选节问题拖散。**这一条是预先声明的取舍，不是遗漏。**
- 每条方向不确定的候选（可读性）**同时测正反号**（A1 负号 / A2 正号），而不是事后补反号变体。

---

## §3 预注册探针批（10 条，2026-10-21）

固定设置：USA / TOP3000 / D1 / decay 5 / truncation 0.08 / maxTrade OFF / pasteurization ON /
unitHandling VERIFY / nanHandling ON / **SUBINDUSTRY**。多模拟 `40husSiw52U9Vkp9HWQ8vA`。
预检：`preflight_expressions` → `valid=true`，`unknown_fields=[]`（`fnd91_measure_4` 因平台分页失败未复核，已由 `get_datafields` 直读确认存在）。

| # | 表达式 | 桶 |
|---|---|---|
| A1 | `group_rank(-vec_avg(fnd91_readability_2), industry)` | Level（晦涩=坏） |
| A2 | `group_rank(vec_avg(fnd91_readability_0), industry)` | Level（可读=好，A1 的反号对照） |
| A3 | `group_rank(ts_backfill(ts_delta(vec_avg(fnd91_readability_2), 22), 66), industry)` | Change |
| B1 | `group_rank((vec_avg(fnd91_sentiment1_4) - vec_avg(fnd91_sentiment1_5)) / vec_avg(fnd91_sentiment1_0), industry)` | Level |
| B2 | `group_rank(ts_backfill(ts_delta((vec_avg(fnd91_sentiment1_4) - vec_avg(fnd91_sentiment1_5)) / vec_avg(fnd91_sentiment1_0), 66), 66), industry)` | Change |
| B3 | `group_rank(ts_zscore(vec_avg(fnd91_sentiment2_0), 252), industry)` | Surprise |
| C1 | `group_rank(vec_avg(fnd91_numeric_count) / vec_avg(fnd91_measure_4), industry)` | Level（对照） |
| D1 | `group_rank(-vec_avg(filing_availability_lag_days), industry)` | Level |
| E1 | `group_rank(-vec_avg(fnd91_topic_17), industry)` | Level |
| F1 | `trade_when(ts_zscore(vec_avg(fnd91_measure_4), 252) > 1, group_rank(-vec_avg(fnd91_readability_2), industry), -1)` | Event-conditioned |

### 3.1 预注册判死线（先写后测，不许事后挪动）

- **数据集级**：10 条全部 `S < 1.58` **且** 最强 `S < 1.0` ⇒ 判 fnd91 无信号（数据集级封存需再补 8 统计族）；
- **机制级**：某桶最强 `S < 0.9` ⇒ 该桶在本数据集上封存，不再换壳重试；
- **幅度线（fnd21 教训前置）**：若 10 条 **全部 `returns < 4.0%`**，即使 S 尚可也判「结构性幅度不足」—— 因为 `F = S·√(ret/0.125)` 在 S 1.58 时需要 ret ≥ 5.0%，幅度不够时 S 再高也过不了 F；
- **升格**：任一 `S ≥ 1.58 ∧ F ≥ 1.0 ∧ 2Y ≥ 1.58 ∧ fail=0` ⇒ 立刻 `check_correlation(refresh=True)`；
- **中性化轴（用户 2026-10-21 明确指令：「exchange 也要考虑不要漏了」）**：
  ⚠ **平台事实（实测，2026-10-21）**：**`EXCHANGE` 不是合法中性化取值**。`create_multi_simulation` 传 `neutralization="EXCHANGE"` 直接 400，返回合法集：
  `STATISTICAL / SUBINDUSTRY / INDUSTRY / FAST / SLOW / CROWDING / NONE / MARKET / SECTOR / REVERSION_AND_MOMENTUM / SLOW_AND_FAST / COUNTRY`。
  ⇒ exchange 轴只能通过**分组**表达（`group_rank(x, exchange)`），不能通过中性化表达。已按此改成 Wave 2b 独立探针（2 条，等 W2 让出槽位后发），
  与 `group_rank(x, industry)` 直接对照 —— 这是「同表达式、只换分组轴」的干净 A/B。
  参照口径仍按 fnd21 §9：MARKET 把幅度换回来、Sharpe 还回去 ⇒ 中性化/分组是**「幅度 ↔ Sharpe」的权衡轴**，不是 Sharpe 的杠杆，必须实测。

---

### 3.2 Wave 2 预注册（10 + 2 条，2026-10-21）

**触发**：§4 显示 Level / Change / Event 三桶全灭、Surprise 仅反号存活（|S| 1.05），而 §2 明确声明「相似度机制留到 Wave 2」。
故 Wave 2 **只打两张牌**：① 唯一未测的机制族 = 披露相似度（`metric0/1`）；② 唯一有方向的桶 = Surprise 反号，并补 `vec_max` / 66d 两个轴。

| # | 表达式 | 桶 | 动机 |
|---|---|---|---|
| G1 | `group_rank(vec_avg(fnd91_cat13_metric0_0), industry)` | Level（相似度） | 高相似度 = 模板化披露 = 无信息 |
| G2 | `group_rank(-vec_avg(fnd91_cat13_metric0_0), industry)` | Change | 低相似度 = 实质改写 = 有信息（Brown-Tucker 口径） |
| G3 | `group_rank(-vec_avg(fnd91_cat13_metric1_0), industry)` | Change | 对**去年同季**改写，剔除季节性 |
| G4 | `group_rank(-(vec_avg(fnd91_cat13_metric0_0)+vec_avg(fnd91_cat8_metric0_0)+vec_avg(fnd91_cat0_metric0_0)+vec_avg(fnd91_cat7_metric0_0)+vec_avg(fnd91_cat11_metric0_0)), industry)` | Change | 5 节合成（cat0/7/8/11/13 覆盖最高的节），降单节噪声 | <!-- lint:counterexample: 同一文档案五节变更量合并（同形态） -->
| G5 | 同 G4 但 `metric1`（YoY） | Change | 同上，跨年口径 |
| G6 | `group_rank(-vec_max(fnd91_cat13_metric0_0), industry)` | Change | `vec_max` 轴（fnd21 实证最优聚合） |
| H1 | `group_rank(-ts_zscore(vec_avg(fnd91_sentiment2_0), 252), industry)` | Surprise | B3 反号（唯一 |S| ≥ 1.0 的方向） |
| H2 | `group_rank(-ts_zscore(vec_max(fnd91_sentiment2_0), 252), industry)` | Surprise | 同上 × `vec_max` |
| H3 | `group_rank(-ts_zscore(vec_avg(fnd91_sentiment2_0), 66), industry)` | Surprise | 同上 × 66d 窗（fnd21 的甜区） |
| K1 | `trade_when(vec_avg(fnd91_cat13_metric0_0) < 0.85, group_rank(-ts_zscore(vec_avg(fnd91_sentiment2_0), 252), industry), -1)` | Event-conditioned | 只在**文本实质改写**的日子交易情绪 z 分 |
| **X1/X2** | `group_rank(vec_avg(fnd91_readability_0), exchange)` / `group_rank(-vec_avg(fnd91_readability_2), exchange)` | Level | 用户指令的 exchange 轴（分组形态），与 A2/A1 直接对照 |

**⚠ 原 Wave 2 判死线已被 §4.2 的覆盖率混淆推翻，不得执行**（「在 NaN 块污染下测出的 <0.9」不是机制结论）。
封存判据顺延为下面的 Wave 3 判死线。

### §3.3 Wave 3 预注册（覆盖修补 × exchange 轴，6 条；2026-10-21）

设置同上（USA/TOP3000/D1/decay 5/trunc 0.08/SUBINDUSTRY）。**先过结构判据再读 S。**

| # | 表达式 | 目的 |
|---|---|---|
| R1 | `group_rank(vec_avg(fnd91_readability_2), exchange)` | 用户指令的 exchange 轴（无 backfill，与 R2 成 A/B） |
| R2 | `group_rank(vec_avg(fnd91_readability_2), industry)` | industry 对照（= Wave 1 A1 的反号，预期 +0.75） |
| R3 | `group_rank(ts_backfill(vec_avg(fnd91_readability_2), 252), exchange)` | exchange + 覆盖修补 |
| R4 | `group_rank(ts_backfill(vec_avg(fnd91_readability_2), 252), industry)` | industry + 覆盖修补（R3/R4 的 A/B） |
| R5 | `group_rank(-ts_zscore(ts_backfill(vec_avg(fnd91_sentiment2_0), 252), 252), industry)` | Surprise 反号 + 修补（拆穿 B3 的 1.05） |
| R6 | `group_rank(-ts_backfill(vec_avg(fnd91_cat13_metric0_0), 252), industry)` | 相似度 + 修补（G1–G6 的 CW 全挂是否可救） |

**零成本先看的两条结构判据**（先于任何 S 解释）：
① 取反后 `longCount/shortCount` 是否近似对调 —— 不对调 ⇒ 读数仍是缺失块产物，作废；
② `CW` 是否降到 <10%、`TO` 是否落回 5–30% —— 不落 ⇒ Level 壳在本字段上结构性不可提交。

**Wave 3 判死线**：
- `R5` 加 backfill 后 `|S| < 0.9` ⇒ **「语气逆向」正式封存**（B3/R2 的 1.05 是缺失块 + 噪声）；
- `R6` 加 backfill 后 `|S| < 0.9` ⇒ **相似度机制封存**；
- `R3/R4` 与 `R1/R2` 的差 = backfill 的净贡献；`R1` 显著劣于 `R2` ⇒ **记「USA 上 exchange 分组稀释信号」**（用户轴已尽责测过，不再第三次）；
- 六条最强 `|S| < 1.0` ⇒ **fnd91 数据集级封存**（累计 26 条 / 0 过闸），转 §0 roster 下一候选并写明理由。
**升格线**：任一 `S ≥ 1.58 ∧ F ≥ 1.0 ∧ 2Y ≥ 1.58 ∧ fail=0` ⇒ 立刻 `check_correlation(refresh=True)`。

---

## §4 实测结果 · Wave 1（multisim `40husSiw52U9Vkp9HWQ8vA`，2026-10-21）

| # | alpha | S | F | 2Y | SUB | TO | ret | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A1 可读性 Fog 负 | `JjPNaggE` | **−0.75** | −0.16 | −0.59 | 0.02 | 56.6% | −2.66% | FAIL ×3 |
| A2 可读性 FRE 正 | `akVbmAAO` | **−0.58** | −0.11 | −0.14 | 0.00 | 56.6% | −2.04% | FAIL ×3 |
| A3 可读性 Δ22 | `rKdOaJb3` | **−0.82** | −0.38 | −1.70 | −0.03 | **4.7%** | −2.72% | FAIL ×3 |
| B1 净语气 Level | `pwvRbVnj` | −0.49 | −0.09 | 0.14 | −0.13 | 56.5% | −1.76% | FAIL ×3 |
| B2 净语气 Δ66 | `E5VpngqP` | −0.54 | −0.19 | −1.67 | 0.11 | **4.4%** | −1.53% | FAIL ×3 |
| B3 语气 z252 | `WjLbra9d` | **−1.05** | −0.26 | −1.09 | −0.22 | 56.4% | −3.59% | FAIL ×3（**反号 = +1.05**） |
| C1 量化密度 | `bl8b0ov6` | −0.52 | −0.09 | 0.36 | −0.01 | 56.6% | −1.81% | FAIL ×3 |
| D1 披露时滞 | `9qEj5aRq` | −0.09 | −0.01 | −0.08 | −0.17 | 65.3% | −0.99% | FAIL ×5（含 **CW 49.6%**） |
| E1 增发主题 | `ZYmbV2oj` | 0.05 | 0.00 | 0.37 | 0.49 | 57.8% | 0.21% | FAIL ×3 |
| F1 冗长门控 | `e76bMdr6` | 0.00 | 0.00 | −0.85 | −0.33 | **2.3%** | 0.00% | FAIL ×4（几乎零持仓） |

### §4.2 实测结果 · Wave 2（multisim `q4zMr3l64Egaxml8WC1zID`，2026-10-21）

| # | alpha | 表达式要点 | S | F | 2Y | SUB | TO | CW | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| G1 | `JjPNaAWm` | `group_rank(vec_avg(cat13_metric0_0), industry)` | −0.17 | −0.03 | −0.14 | −0.26 | 65.3% | **49.5%** | FAIL ×5 |
| G2 | `LL5Novm2` | G1 反号 | −0.44 | −0.12 | −0.41 | −0.18 | 65.4% | **49.6%** | FAIL ×4 |
| G3 | `e76bMYGg` | `-metric1`（YoY） | −0.17 | −0.03 | −0.17 | −0.17 | 65.4% | **49.6%** | FAIL ×5 |
| G4 | `Grgbj2zG` | 5 分节 QoQ 合成反号 | −0.31 | −0.07 | −0.34 | −0.24 | 65.3% | **49.6%** | FAIL ×5 |
| G5 | `omoLjbrm` | 5 分节 YoY 合成反号 | −0.17 | −0.03 | −0.28 | 0.03 | 65.5% | **49.6%** | FAIL ×4 |
| G6 | `0mjXZV6p` | `-vec_max(metric0)` | −0.43 | −0.12 | −0.39 | −0.20 | 65.4% | **49.6%** | FAIL ×5 |
| H1 | `vROr7EPw` | **B3 的精确反号** `-ts_zscore(sentiment2_0,252)` | **−0.11** | −0.01 | +0.50 | 0.12 | 56.8% | pass | FAIL ×3 |
| H2 | `WjLbrZJG` | 同上 × `vec_max` | −0.27 | −0.04 | +0.23 | −0.05 | 56.8% | pass | FAIL ×3 |
| H3 | `j2eAkpOO` | 同上 × 66d 窗 | −0.32 | −0.05 | −0.25 | −0.06 | 56.4% | pass | FAIL ×3 |
| K1 | `9qEj5e2o` | `trade_when(metric0<0.85, H1, -1)` | −0.34 | −0.13 | 0.14 | 0.07 | **1.36%** | 50.0% | FAIL ×4 |

**Wave 2 的核心发现（比 S 值重要）：B3 的 −1.05 不是情绪信号，是「缺失值块」的覆盖率赌注。**
H1 是 B3 的逐字反号，两者持仓结构却几乎不变（long/short `677/2361` vs `685/2353`，TO 56.4% vs 56.8%）——
真正的符号反转会把 long/short 对调，实际没有。机制：`group_rank` 把 **NaN 排到组内最低档**，
而 `-NaN` 仍是 NaN ⇒ **取反只翻转「有值那一侧」的信号，翻不动缺失块**。该块占约 1/3 的票，
在 1000 只票的组内被压到 rank≈0 ⇒ 结构性做空缺失票 ⇒ 既贡献了 S 的绝大部分，也解释了
G1–G6 全部 `CW = 49.6%`（2015-01-20 一次集中在缺失块上）。

⇒ **可复用铁律（本集最重要的一条）**：覆盖率 < 1 的字段上直接 `group_rank` / `rank`，
测到的是「覆盖率赌注 + 真信号」的混合物，且**反号实验在结构上无法拆开它**。
判据：取反后 `longCount/shortCount` 不近似对调 ⇒ 该族读数作废，先做覆盖修补再谈方向。
处置：`ts_backfill(x, 252)` 把最后一份申报值向后携带，把覆盖率补到 ~1，再 rank。

⇒ 同时解释 **G1–G6 全在 CW 上挂掉**（相似度族读数同样作废，不能据此封存相似度机制）——
Wave 3 必须带 backfill 重测。

### §4.3 实测结果 · Wave 3（multisim `6N5WZ1cW4nybgi1gm51r6vr`，2026-10-21）—— 覆盖修补 + exchange 轴

| # | alpha | 表达式 | S | F | 2Y | SUB | TO | long/short | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| R1 | `xA13Z89W` | `group_rank(vec_avg(readability_2), exchange)` | −0.40 | −0.06 | 0.09 | 0.09 | 56.7% | 690/2356 | FAIL ×3 |
| R2 | `O0JN3PkY` | `group_rank(vec_avg(readability_2), industry)` | −0.34 | −0.05 | 0.11 | −0.12 | 56.5% | 670/2371 | FAIL ×3 |
| R3 | `0mjXJ3d8` | `group_rank(ts_backfill(vec_avg(readability_2),252), exchange)` | **+0.37** | 0.12 | 0.51 | 0.18 | **6.03%** | 1469/1582 | FAIL ×3 |
| R4 | `A1QNAZbX` | `group_rank(ts_backfill(vec_avg(readability_2),252), industry)` | **+0.37** | 0.12 | 0.44 | 0.16 | **6.36%** | 1455/1596 | FAIL ×3 |
| R5 | `ZYmbJ3lZ` | `group_rank(-ts_zscore(ts_backfill(vec_avg(sentiment2_0),252),252), industry)` | **+0.65** | 0.27 | 0.30 | 0.46 | 7.40% | 1439/1607 | FAIL ×3 |
| R6 | `wp9ZrxzQ` | `group_rank(-ts_backfill(vec_avg(cat13_metric0_0),252), industry)` | +0.19 | 0.04 | −0.55 | 0.16 | 2.49% | 1439/1611 | FAIL ×3 |

**三条结论（定性，已足以封存）：**

1. **覆盖率混淆被实验证实，且 `ts_backfill` 是解药（可复用）。** 同一表达式加不加 backfill，结构完全变样：

   | 指标 | 无 backfill（R2） | 加 backfill（R4） |
   |---|---:|---:|
   | TO | 56.5% | **6.36%** |
   | long/short | 670 / 2371（**严重偏空**） | 1455 / 1596（平衡） |
   | S | −0.34 | **+0.37** |

   56% 换手本身就是「日频传播的 level 字段」+「NaN 块每天随成分调整进出」的指纹。
   backfill 后持仓结构正常、换手落回 USA review 带（0.05–0.30）——**注意：这也是本集唯一一次 TO 合规**。

2. **符号不自洽证实了「取反翻不动缺失块」**：Wave 1 的 A1（`-readability_2`）= −0.75，
   Wave 3 的 R2（`+readability_2`）= −0.34 —— **两者符号相同**。一个表达式与它的取反同号，
   在无混淆时不可能发生。⇒ 该族的全部无 backfill 读数**一律作废**，不能用来判方向。

3. **真实幅度远低于闸**：去掉混淆后最强的 R5 = **+0.65**（语气逆向 + 修补），
   可读性 R3/R4 = +0.37，相似度 R6 = +0.19。⇒ B3 的 **1.05 中约 0.4 是缺失块、其余是噪声**，
   与 §5 第 9 条的「拥挤字段残差」判断一致。

4. **exchange 轴（用户指令）已尽责测过，无增益**：R1 vs R2（−0.40 vs −0.34）、
   R3 vs R4（+0.37 vs +0.37）——**exchange 分组与 industry 分组等价**，既不更好也不更差。
   ⇒ 在 USA TOP3000 上，exchange 作为分组维度可替代 industry 使用，但**不提供额外的正交性**；
   且 `EXCHANGE` 不是合法中性化（§3.1），**exchange 轴的可动用形态到此为止**。

---

## §5 归因（Wave 1 → Wave 2 的因果链）

1. **Level 桶 6 条全灭，最强 |S| 0.75** ⇒ 按预注册机制级判死线**封存 Level**。8-K 文本的**水平量**（可读性 / 语气 / 量化密度 / 时滞 / 主题暴露）在 USA TOP3000 上不构成主信号。与 fnd21 的 Level 死法**同型**（两次独立数据集的 Level 全灭 ⇒ 可复用结论：文本/分数类数据的**水平量**在 USA 已被定价或本就无信息，**不要再用 Level 开波**）。
2. **可读性方向被证伪，且两个指标互证**：A1 反号 = +0.75、A2 反号 = +0.58 —— 两者**同号为正**，即「**越晦涩（Fog 高 / FRE 低）⇒ 收益越高**」。方向与 Li (2008) 的「晦涩 ⇒ 坏」相反。解读：8-K 的文本复杂度主要代理**事件本身的复杂度**（并购/重组/减值这类需要长篇解释的事件），不是「藏坏消息」。⇒ 这是一个**真实但方向反直觉**的机制，幅度 0.58–0.75，够不上闸；且**不能靠换壳放大**（换壳只会得到 0.6–0.7 的同一族）。
3. **Change 桶全灭且 2Y 崩坏**：A3 2Y −1.70、B2 2Y −1.67，明显弱于全期。⇒ 文本「变化量」在近两年**失效（符号反转）**，不是稳定的 alpha 源。**这条比 S 值更重要**：即使全期 S 修到 1.58，2Y 也会挡死。
4. **Event-conditioned 结构性无效（不是参数问题）**：F1 把换手压到 2.34%、收益 0 —— `ts_zscore(measure_4,252) > 1` 命中的样本太少，等于长期空仓。**机制结论：8-K 的「长度异常」不构成可交易的事件窗口**（8-K 本就是事件报告，长度分布在事件日之间没有足够对比度）。
5. **Surprise 是唯一有方向的桶**：B3 反号后 S +1.05 / 2Y +1.09 / SUB 0.22 / ret +3.59%。方向含义：**8-K 语气越正面（相对自身历史）⇒ 未来收益越差** —— 与「管理层在申报里过度正面表述 ⇒ 后续回吐」一致，也是 Loughran-McDonald 口径下 filing-level 的**逆向**用法。但 ret 3.59% < F 所需的 5.0%（S 1.58 时），**幅度不足**，只够当 Wave 2 的种子。
6. **换手结构异常（本集最重要的结构发现）**：所有 **level 型 TO ≈ 56%**，而 **delta 型只有 4.4–4.7%**。若字段真是季度阶梯，level 型的 rank 也应阶梯化 ⇒ 实测反驳了「纯季度」假设：**这些字段在 BRAIN 侧是日频传播的**，只有 `ts_delta` 因为在两次申报之间恒为 0 才低换手。⇒ 后果：level 型即使找到信号，56% 的换手也远出 USA review 带（0.05–0.30），成本会吃掉大部分收益。
7. **filing lag 不可用**：CW 49.6%（2015-01-20），分布过于集中（多数为同一值），任何 rank 都会挤在少数票上。
8. **topic_17 是「小盘局部」而非主信号**：全局 S 0.05 但 SUB 0.49 —— 与 institutions18 的 STATISTICAL 形态同源（全市场无信号、子宇宙有），不能当 ATOM 主信号。
9. **B3 的 1.05 未必是信号**：`sentiment2_0` 是**最拥挤**的基础情绪字段（aC 23 / uC 20），1.05 可能只是**行业 × 规模的残差**。Wave 2 用 `vec_max` 与 66d 窗做稳健性交叉，若三轴都停在 1.0–1.1 ⇒ 判噪声上限。

---

## §6 裁定（2026-10-21）

**fnd91（8-K 文本解析）＝ 数据集级封存。** 三波共 **26 条**（W1 10 + W2 10 + W3 6），**0 条过 RA 闸**，
最强为去混淆后的 R5 `ZYmbJ3lZ`（S +0.65 / F 0.27 / 2Y 0.30 / SUB 0.46 / TO 7.40%），
距闸线（S 1.58 / F 1.0 / 2Y 1.58）差 0.9 以上，**不是修壳能补的距离**。

**逐机制裁定**（六桶全覆盖，无遗漏）：

| 桶 | 条数 | 最强 | 裁定 |
|---|---:|---:|---|
| Level | 9 | 0.75（无 backfill，已作废）/ 0.37（R3/R4） | **封存**：文本水平量在 USA 已定价；与 fnd21 同型 |
| Change | 2 | 0.82（2Y −1.70） | **封存**：2Y 崩坏，近两年符号反转 |
| Surprise | 5 | **0.65**（R5 去混淆后） | **封存**：原 1.05 含约 0.4 缺失块成分 |
| Dispersion | 0 | — | 本集无分歧度字段族（`readability`/`sentiment` 均为单值），**结构性不可测** |
| Event-conditioned | 2 | 0.34（TO 1.36%） | **封存**：8-K 长度异常不是可交易事件窗 |
| Propagation | 0 | — | 本集无跨资产字段，**结构性不可测** |

**可复用结论（已写入本档案，供其它文本类数据集直接套用）：**

1. **覆盖率混淆律**：覆盖率 < 1 的字段直接 `rank` / `group_rank`，测到的是「覆盖率赌注 + 真信号」的混合物。
   **诊断三件套**：① 取反后 `longCount/shortCount` 不近似对调；② TO 高达 50%+ 且 long/short 严重偏空；
   ③ CW 在某一日集中到 40%+。**满足任一条 ⇒ 该族读数的方向解释一律作废**。
   **解药**：`ts_backfill(x, 252)` 后重测（本集实测 TO 56.5% → 6.36%、long/short 670/2371 → 1455/1596）。
2. **exchange 分组 ≈ industry 分组**（USA TOP3000）：R1 vs R2、R3 vs R4 两组成对实验差值为 0.06 / 0.00。
   `EXCHANGE` 不是合法中性化 ⇒ **exchange 轴只有分组一种形态，且不提供额外正交性**。
3. **文本类数据在 USA 的幅度天花板**：fnd91 去混淆后最强 0.65、fnd21 三波最强 < 1.0 ⇒
   两个独立文本数据集互证。**文本类 dataset 不再作为主信号来源开新波**。

**换数据集的理由（满足「仅在确实无计可施时才更换」）**：六桶中四个已实测封存、两个结构性不可测，
26 条 0 过闸，最强候选差闸线 0.93 且方向不稳健 ⇒ 本集已无未测的合理路径。

**DB 侧状态**：§6 是业务裁定；`seal_dead_end` 目前仍被论坛取证闸 fail-closed 拦着（本集判死依据是
26 条回测而非论坛检索），故 **DB registry 尚未落 dead_end**。要在 DB 侧封存，需先补一次
`forum_recon`（问题：8-K 文本可读性 / 语气在美股是否已有 alpha）或由用户批准 `force_seal=True`。

