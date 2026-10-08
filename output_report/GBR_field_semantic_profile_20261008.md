# GBR 字段画像 · description 驱动语义重做版（全 category）

> 区域：**GBR / D1 / TOP700 / EQUITY**　｜　执行：2026-10-08
> 依据用户指令：「**用 description 确认语义的方式重新对 GBR 所有 category 进行字段画像，并在这个过程中不断自我审查**」
> 新工具：**`tools/fields/field_semantic_type.py`**（description 优先的语义分类器，产物表 `field_semantic_type`）
> 与既有 `field_profile.py` 的分工：**前者判「这个字段是什么量」，后者判「测出来强不强」**；两者交叉才给出正确的机制→骨架映射。

---

## 一、为什么必须用 description 重做

`field_profile.py` 的 9 类 verdict 中，**只有 `DEAD_COUNT` 是名字驱动的**（`COUNT_PAT.search(字段名)`）。
经审计，该规则有三类错误（详见 §六 自审日志 #0），已在同日修正为 **description 驱动**。
但更根本的问题是：**verdict 只回答「强不强」，不回答「是什么量」** —— 而骨架选择完全取决于「是什么量」。

**全库量化证据：GBR 15,522 个字段中，名字与其 description 语义冲突的有 1,470 个 = 9.5%。**

---

## 二、语义类型体系（description 驱动，共 19 类）

| sem_type | 判据（description 侧） | 骨架建议 | GBR 字段数 |
|---|---|---|---:|
| `unknown` | 领域专有复合量，无通用量词 | **须人工读描述**，勿按名字拍骨架 | **3,512** |
| `score` | score / index / rating | 分值型：水平 → 先 rank | 1,921 |
| `count` | number of / count of / how many / breadth | **计数型：先 `group_neutralize` 去共同成分，勿直接 `ts_*`** | 1,813 |
| `ratio` | ratio / percentage / fraction / per share / margin / churn rate | 比率型：直用 | 1,681 |
| `level_amount` | dollar value / price / total value / USD | 水平型：先 `rank`/`scale` | 1,346 |
| `percentile` | percentile / quantile / z-score / standardized / rank (1-100) | 分位型：直用或 `ts_quantile` | 1,002 |
| `probability` | probability / odds / confidence level | 比率型：`rank`/`group_zscore` 直用 | 893 |
| `revision_change` | revision / change in / delta / growth / momentum | 变化型：`ts_delta`/`ts_rank` | 844 |
| `sentiment` | sentiment / tone / polarity / classifier | 情绪型：水平 → `ts_delta`/`ts_rank` | 537 |
| `estimate_level` | estimate of / analyst estimate / consensus / expected(forward\\|fiscal) | 水平型：`ts_delta` 取修正 | 467 |
| `dispersion` | standard deviation / volatility / kurtosis / skewness / CV | **★比率型：`divide(x, ts_mean(x))` 或 `ts_std_dev`** | 416 |
| `cluster_label` | cluster assignment / grouping level | **只作分组轴**（GROUP / `bucket` 包装） | 322 |
| `identifier` | ISO code / currency code / ticker / numeric code | **禁用（标识）** | 255 |
| `temporal_meta` | UTC / timestamp / start\\|end time / elapsed / announced | **禁用（时间元数据）** | 148 |
| `indicator_name` | RSI / MACD / Williams %R / Chaikin / Bollinger / ATR / OBV … | **技术指标：直用或先 rank（勿按名字猜）** | 119 |
| `correlation` | correlation between | 比率型：直用 | 111 |
| `direction` | increase / decrease / upward / falling / higher | 方向型：rank 后直用（注意符号） | 69 |
| `novelty_time` | days since / how new / novelty / recency / age of | **★时效型：`reverse(rank(ts_arg_max(x,w)))`** | 37 |
| `text` | headline / summary text | **禁用（文本）** | 29 |

> 19 类中 **5 类为非信号**（`cluster_label` 作轴，另 4 类禁用）：合计 **754 个字段** —— 这些字段**无论测出什么 S 都不该用**。

---

## 三、语义类型 × platform category 矩阵

| category | unknown | score | count | level_amt | ratio | pctile | prob | revision | sentiment | est_level | dispersion | cluster | ident | temporal | indicator | corr | direction | novelty | text | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MODEL | 554 | 565 | 629 | 519 | 1105 | 758 | 509 | 557 | 76 | 138 | 63 | 2 | 9 | 1 | — | 3 | — | 3 | — | 5,335 |
| OTHER | 1375 | 359 | 246 | 283 | 46 | 118 | 417 | 32 | 252 | 3 | 21 | 255 | 53 | 17 | — | — | — | 16 | 8 | 3,515 |
| ANALYST | 271 | 179 | 591 | 196 | 195 | 4 | 5 | 109 | 68 | 338 | 115 | — | 127 | 45 | — | — | 5 | 4 | — | 2,239 |
| PV | 519 | 675 | 9 | 218 | 150 | 117 | — | 106 | — | 18 | 173 | 65 | 14 | 1 | 108 | — | 3 | — | — | 2,165 |
| FUNDAMENTAL | 587 | 67 | 90 | 209 | 137 | 3 | — | 68 | 4 | 7 | 43 | — | 15 | 2 | — | — | — | — | — | 1,238 |
| NEWS | 100 | 52 | 56 | 39 | 26 | — | 7 | 4 | 83 | 1 | 5 | — | 29 | 59 | — | — | — | 17 | 16 | 491 |
| SENTIMENT | 21 | 39 | 134 | — | — | 2 | — | — | 60 | — | 2 | — | — | 13 | — | — | — | — | 5 | 276 |
| INSTITUTIONS | 3 | 7 | 35 | 12 | 7 | — | — | 1 | — | — | — | — | 1 | — | — | — | — | 3 | — | 66 |
| INSIDERS | 19 | 1 | 3 | 24 | 1 | — | — | — | — | — | — | — | 2 | — | — | — | — | — | — | 50 |
| RISK | 23 | — | — | 7 | 5 | — | — | — | — | — | 3 | — | — | 1 | — | — | 1 | — | — | 40 |
| SHORTINTEREST | 12 | 1 | 6 | 3 | — | — | — | — | — | — | 3 | — | — | — | — | — | — | — | — | 25 |
| EARNINGS | 14 | — | — | 3 | — | — | 3 | — | 3 | — | — | — | 1 | 1 | — | — | — | — | — | 25 |
| OPTION | 3 | — | — | 11 | 3 | — | — | 2 | — | — | 2 | — | 1 | — | — | — | 1 | — | — | 22 |
| SOCIALMEDIA | 6 | 1 | 4 | — | — | — | — | — | 6 | — | — | — | 2 | 1 | — | — | — | — | — | 20 |
| MACRO | 5 | — | 7 | — | — | — | — | — | — | — | — | — | 1 | — | — | — | — | — | — | 13 |
| IMBALANCE | — | 1 | — | 1 | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | 2 |
> 空格 = 0。为可读性省略 0 值列 `text`/`indicator`/`corr` 等的部分单元格。

**读法（三条结构性事实）**：
1. **`count` 是 ANALYST(591) / SENTIMENT(134) / INSTITUTIONS(35) 的主语义** —— 家数/参与量类信号。
2. **`ratio`+`percentile` 是 MODEL(1863) 的主语义** —— 估值比值与分位。
3. **`unknown` 集中在 OTHER(1375) / FUNDAMENTAL(587) / PV(519)** —— 这些是**领域专有复合量**（如「airline's fuel consumption per available seat mile」），**没有通用量词 ⇒ 必须逐条读描述定骨架**（这也解释了为何这些类在本区长期做不出东西：骨架无从匹配）。

---

## 四、逐 category 画像（description 确认）

| category | 字段 | ALIVE | WEAK | UNTESTED | 语义构成（top5） | **ALIVE 的语义** | 未测池主语义 |
|---|---:|---:|---:|---:|---|---|---|
| **MODEL** | 5,335 | **29** | 15 | 1,087 | ratio 1105 / pctile 758 / count 629 / revision 557 / unknown 554 | **ratio 17, pctile 7**, level 2, prob 2 | count 264 / ratio 237 / prob 227 |
| **ANALYST** | 2,239 | **17** | 13 | 387 | count 591 / est_level 338 / unknown 271 / ratio 195 / score 179 | **count 10**, est_level 3, ratio 2 | **count 202 / est_level 111** |
| **PV** | 2,165 | 3 | 0 | 511 | score 675 / unknown 519 / level 220 / dispersion 173 / ratio 150 | score 1 / ratio 1 / unknown 1 | **score 329** / dispersion 71 / pctile 71 |
| **SENTIMENT** | 276 | 0 | 1 | 5 | **count 134** / sentiment 60 / score 39 | — | — |
| **NEWS** | 491 | 0 | 1 | 180 | unknown 100 / **sentiment 83** / temporal 59 / count 56 / score 52 | — | temporal 43 / **sentiment 43** / score 34 |
| **INSTITUTIONS** | 66 | 0 | 2 | 3 | **count 35** / level 12 | — | — |
| **FUNDAMENTAL** | 1,238 | 0 | 0 | 40 | **unknown 587** / level 209 / ratio 137 / count 90 | — | unknown 36 |
| **OTHER** | 3,515 | 0 | 2 | 350 | **unknown 1375** / prob 417 / score 359 / level 283 / **cluster 255** | — | score 145 / level 108 |
| **INSIDERS** | 50 | 0 | 0 | 0 | level 24 / unknown 19 | — | — |
| **RISK** | 40 | 0 | 0 | 3 | unknown 23 / level 7 / ratio 5 | — | — |
| **SHORTINTEREST** | 25 | 0 | 0 | 12 | unknown 12 / count 6 / dispersion 3 | — | — |
| **EARNINGS** | 25 | 0 | 0 | 0 | unknown 14 / level 3 / prob 3 / sentiment 3 | — | — |
| **OPTION** | 22 | 0 | 0 | 0 | level 11 / unknown 3 / ratio 3 / dispersion 2 | — | — |
| **SOCIALMEDIA** | 20 | 0 | 0 | 0 | unknown 6 / sentiment 6 / count 4 | — | — |
| **MACRO** | 13 | 0 | 0 | 0 | count 7 / unknown 5 | — | — |
| **IMBALANCE** | 2 | 0 | 0 | 0 | level 1 / score 1 | — | — |

### 4.1 全局：ALIVE / WEAK 的语义分布（description 确认）

```
ALIVE（49）：count=10  ratio=9  level_amount=9  percentile=9  estimate_level=4  probability=3
             unknown=2  sentiment=1  revision_change=1  score=1
WEAK（34）：count=9  estimate_level=8  level_amount=5  probability=5  unknown=2
             score=2  revision_change=1  ratio=1  sentiment=1
```

**★ 结论：本区全部 83 个活/弱字段只落在 10 类语义上，且前三类占 62%**
（`count` 19 + `ratio` 10 + `level_amount` 14 = 43/83）。
**⇒ 「能出东西的量类型」在本区高度收敛：计数型 / 比率型 / 水平型。**

**★ 未测池的语义分布与产出语义高度重合**：
- ANALYST 未测 387 中 `count=202` —— **但 count 已被证明是本区最强语义**（ALIVE 10 个），
  且已产出候选全部集中在 `analyst7` 的家数族 ⇒ **增量空间存在但同族拥挤（prod 0.76–0.86）**。
- PV 未测 511 中 `score=329` —— PV 的 `score`（形态相似度分）**从未系统开采**，是本区最大的「语义未测块」。

---

## 五、★ 名字/描述冲突：名字会骗人的直接证据（ALIVE/WEAK 中）

| 字段 | 名字像 | 实为 | description 证据 |
|---|---|---|---|
| `predictive_starmine.smest_price_ratio_*`（8 个，含 4 个 ALIVE） | ratio | **ratio**（修正后正确） | "price-to-revenue **ratio**" —— 修正前因 `\bprice\b` 在句首被误判为 level_amount |
| `model28.mdl28_sm_structural_credit_structural_pd_pct`（ALIVE） | ratio | **probability** | "Estimated 1-year **probability** of default expressed a…" |
| `dl_riskfree_returns.probability_label1_2quantile_5day_ohlcv` | percentile | **probability** | "**Log-probability** (log-softmax) that the…" |
| `analyst_earnings_ibes.volume_weighted_avg_price_dlr1` | dispersion | **level_amount** | "**volume-weighted average price**, D1-delayed…" |
| `model38.star_val_sector_rank` | percentile | **percentile**（修正后） | "…valuation **rank (1-100)**" ⇒ 分位而非分值 |
| `MODEL.short_term_price_change` | （看不出） | **indicator_name** | 描述竟是 "**Williams %R**" |
| `MODEL.cumulative_money_flow_volume_adjusted` | （看不出） | **indicator_name** | 描述竟是 "**Relative Strength (RSI)**" |
| `MODEL.liquidity_money_flow_alignment` | （看不出） | **indicator_name** | 描述是 "**Relative Turnover (RTN63D)**" |

**⇒ 最后三例是「名字与描述毫无对应」的极端情形**：若按名字选骨架，必然错配量类型。

---

## 六、★★★ 自我审查日志（本次任务的迭代记录）

> 用户要求「在这个过程中不断自我审查有什么地方可以改进」。以下是每轮发现 + 修正，**含我自己修错的一次**。

| # | 发现 | 影响 | 处置 |
|---|---|---|---|
| **#0** | `field_profile.py` 的 `DEAD_COUNT` 是**名字驱动**；`count` 无词边界 ⇒ 误匹配 `country`/`accounts`；`*_surprisenum` 语义实为「参与家数」而非「方向性修正家数」；反向漏杀 `oth47_organic_keywords`（描述 "Count of…"） | 4 个字段判级错误 | ✅ 改为 **description 驱动**（`COUNT_DESC_PAT` 且非 `COUNT_DESC_NEG`），DEAD_COUNT 4→5；`--all-regions` 重建通过 |
| **#0b** | 我**第一次修错**：只加词边界 `\bcount\b` ⇒ `count_50bps`（`_` 属 `\w`）与 `_numup` 全失配，**DEAD_COUNT 4→0 是假象** | 若未复核会留下更差版本 | ✅ 复核时发现并改为 description 驱动 |
| **#1** | 规则**固定优先级**≠语义主次：`est_12m_gps_raisednum_4wks` 描述以 "**Number of** … earnings **per share**" 开头，主量是「家数」，却被排在前的 `ratio`(per share) 抢先 | 大量「数量 + per share」字段被误判为 ratio | ✅ 改为「**取描述中最靠前的主量词**」（earliest-match）；**~1,000 个字段重新归类**（ratio 2242→1374） |
| **#2** | earliest-match 对**复合名词**失效：`price-to-revenue ratio` 的主量词在**词尾**，但 `\bprice\b` 在句首 ⇒ 8 个 `smest_price_ratio_*`（含 4 个 ALIVE）被判 level_amount | 直接影响含 ALIVE 的判级 | ✅ 新增**复合表述优先层**（`X-to-Y ratio` / `price-earnings` 等）；复查 8 个字段全部归位 `ratio` |
| **#3** | `estimate_level` 的 `expected` 过于泛化：`mdl28_..._asset_drift_percent` 描述 "**Expected** annualized **percent change**" 实为变化率，却被判估计水平 | 语义错判 | ✅ 收紧为 `expect(ed)?\s+(annual\|forward\|fiscal\|\d\|the next)` |
| **#4** | `unknown` 达 3,601（23%），其中**全部有描述** ⇒ 是**规则缺口**而非数据缺口 | 覆盖率不足 | ✅ 抽样定位缺口 |
| **#5** | 缺口暴露**两类新语义**：① 技术指标名（`short_term_price_change` = "Williams %R"、`cumulative_money_flow_volume_adjusted` = "RSI"）② 方向型（"Increase/Decrease in …"）；另行业比率表述（churn rate / margin / calculated by dividing）未覆盖 | 漏掉「名字与描述最脱节」的一类字段 | ✅ 新增 `indicator_name`(119) + `direction`(69)，扩展 ratio / temporal_meta；unknown 3,601→3,512 |

### 仍未解决 / 建议继续改进（诚实列出）

| # | 问题 | 现状 | 建议 |
|---|---|---|---|
| **I1** | `unknown` 仍 **3,512（22.6%）**，集中在 OTHER/FUNDAMENTAL/PV | 这些是**领域专有复合量**（无通用量词） | **不要强行套量词**；应引入 **LLM 逐条读 description 定骨架**（或建「行业子类」规则）。当前标记为「须人工读描述」是诚实的 |
| **I2** | `DEAD_TURNOVER`（`to_med>0.70`）是**骨架属性**而非字段属性 —— 换手可由 `ts_decay_linear`/`ts_target_tvr_decay` 压低，且该判据下 **7 个字段的 `n_tests` 全为 1**（单次测量） | 可能误杀 | 建议**降级为提示**（与 `DEAD_COUNT` 同类问题）；**未经用户确认我不敢擅自改判级** |
| **I3** | `DEAD_STATIC`（`to_med<0.03`）同理可能受骨架影响，但**静态性更接近字段本质**（常数场不随骨架变） | 相对可信 | 保留，但把 `n_tests=1` 者单独标「低置信」 |
| **I4** | 本分类器只看**单字段描述**，未利用 **`field_group`** 与**族内一致性** | 同族字段可能被分到不同 sem_type | 建议加「族级投票」校正 |
| **I5** | 语义类型与**产出强度**的统计关联尚未建模 | 只做了交叉表 | 可回归：`sem_type → P(ALIVE)`，用于**开波前按语义配额** |
| **I6** | 非信号类（cluster/identifier/temporal/text）共 **754 个字段**，画像是否已把它们排除在候选池外？ | 画像按 S 判级，未按语义排除 | 建议在 `s1_semantic_*` 层硬排除，避免浪费探针 |

---

## 七、结论与可执行建议

1. **画像已按 description 重做完毕**：19 类语义 × 16 个 category，全 15,522 字段；新工具 `tools/fields/field_semantic_type.py`（可 `--build`/`--report`，区域通用）。
2. **产出语义高度收敛**：83 个活/弱字段只落在 10 类语义上，**前三类（count / ratio / level_amount）占 62%** ⇒ **本区能出东西的量类型就这三类**。
3. **语义 × category 的可行动指引**：
   - **ANALYST**：`count`（未测 202）是唯一被证明有效的语义 —— 但同族 prod 已达 0.76–0.86；
   - **PV**：`score` 未测 **329** 个 —— **本区最大且未被系统开采的语义块**（形态相似度分）；
   - **FUNDAMENTAL / OTHER**：`unknown` 为主（587 / 1375）⇒ **必须先解决「读描述定骨架」才能开波**，否则必做无用功；
   - **非信号 754 个**（cluster/identifier/temporal/text）应从候选池排除。
4. **纪律固化**（已写入 skill `_field-profile-playbook.md §7`）：类型/机制归类**以 description 为准**；名字正则只用于缩小候选；**关键词出现 ≠ 语义成立**；反向也要查。
5. **本报告的自审日志本身是产出**：6 轮迭代中我**自己修错 1 次**（#0b）、发现规则设计缺陷 3 次（#1/#2/#3）、定位数据缺口 1 次（#4/#5）—— 说明「description 驱动」不是一次替换名字正则就能完成的，需要**按真实描述迭代规则**。


---

## 十三、按修正方案实测：`ent`（企业价值）指标 —— 全负，并暴露命中率的盲区

### 13.1 执行
按 §十二 修正后的结论（扫 UNTESTED ∩ 非MODEL ∩ 高命中语义），GBR 内**唯一真空白**是
`analyst7` 的 **`ent`（Enterprise Value）** 指标（14 个未测字段），发 Wave 21（8 条）：

| 骨架（按 sem_type 选） | 表达式要素 | S | 2Y |
|---|---|---:|---:|
| 计数型①：净修正家数 | `ent_raised_1wk − ent_lowered_1wk` | −0.95 | −1.39 |
| 计数型① | `ent_raisednum_1mth − ent_lowerednum_1mth` | −0.92 | −1.03 |
| 计数型① | `ent_raisednum_4wks − ent_lowerednum_4wks` | **−1.03** | −1.32 |
| 计数型②：覆盖度 | `ent_num`（水平） | −0.50 | 0.33 |
| 计数型② | `ts_delta(ent_num,22)` | −0.30 | 0.40 |
| 计数型② | `ent_num − ent_num_4wks_ago` | −0.37 | −0.78 |
| 水平型：估计修正 | `ts_delta(ent_mean,66)` | −0.61 | 0.16 |
| 水平型 | `ts_delta(ent_median,66)` | −0.55 | 0.41 |

**⇒ 8/8 全负且同向**（反向最高 +1.03 < 1.58）⇒ **`ent` 指标在 GBR 是「反向 + 弱」**。

### 13.2 ★★★ 第 7 轮自审：命中率缺少「底层指标」维度

**预测失败**：§十二 我算出 `count` 的 P(ALIVE｜已测)=13%，据此预期 `ent` 有机会 —— **未兑现**。

**根因**：命中率按 `sem_type` 汇总，但**同一 sem_type 内、不同底层指标的方向可以相反**：

| 指标 | sem_type | 骨架 | 方向 |
|---|---|---|---|
| `est_12m_pre_*`（税前利润）净修正家数 | `count` | 同一套 | **正（S1.96，已提交）** |
| `est_12m_ent_*`（企业价值）净修正家数 | `count` | 同一套 | **负（−0.95 ~ −1.03）** |

⇒ **改进项：命中率必须按 `(sem_type × 指标族)` 二维统计**，而不是只按 sem_type。
⇒ 这也为「**跨族不可类比**」增加了一个新维度：**不仅强度不可类比，方向也可能翻转**。

### 13.3 GBR 的 count 语义矿至此正式见底

- `analyst7` 的 count 未测 187 个中，**唯一完全未碰的指标 `ent` 已试并全负**；
  其余指标（`pre/net/ebi/ebt/sal/cps/gps/dps/bps/tbv/roa/opr/nav/grm/csh/ndt/ner/prr`）**战役均已碰过**。
- 叠加 §十（analyst7 家数族 prod 0.76–0.86）⇒ **GBR 非 MODEL 的 count 语义 = 既 prod 饱和、又无新指标。**

### 13.4 本区出口封死的完整清单（五类形态，每类均有实测证据）

| 形态 | 判据 | GBR 实例 | 实测结论 |
|---|---|---|---|
| **A prod 墙** | IS 全过、prod > 0.70 | `analyst7` 家数族、`pv47` 反转族 | 15 颗候选全被挡（0.756–0.856） |
| **B 2Y 塌** | IS 强、2Y ≪ 1.58 | `analyst_factor_signals`、`analyst9` | 换骨架/压 TO 均无效 |
| **C 低于闸线** | S/F 不足 | `analyst47`（F 0.97） | 降 TO 手段穷尽 |
| **D「2Y 稳、S 弱」** | 2Y ≥ 1.58、S ≤ 1.0 | `nws18_bee`、`nws20_ber`、`oth47_organic_traffic` | 换骨架后仍 ≤ 0.88 |
| **E 同 sem_type 反向** ★新 | 同量型同骨架、方向翻转 | `ent`（企业价值）vs `pre`（税前利润） | 全负，反向仍 < 1.58 |

**⇒ GBR 在「不跨区 + 不放开 MODEL」约束下，语义层出口已逐个验证为封死。正确动作是「收口 + 跨区」。**


---

## 十四、★ 全 sem_type 扫测（62 条 / 8 波 / 17 类）—— 结论与自我纠错

### 14.1 目的
现有 `P(ALIVE|sem_type)` 是**混杂估计**（大多数已测字段用同一套 house 骨架）。本扫描给**每个 sem_type 配其匹配骨架**、并直接在**未测字段**上实测，以得到干净的「语义 → 产出率」。

### 14.2 结果（按中位 S 排序，n=2~4）

| sem_type | n | 中位S | 最好S | 序号语义 | 判读 |
|---|---:|---:|---:|---|---|
| identifier | 4 | **0.65** | 0.67 | **无** | **spurious**（ISO 代码按字母序 rank 无经济含义） |
| **ratio** | 4 | **0.50** | **0.76** | 有 | **有效语义第一** |
| text | 4 | 0.45 | 0.61 | 无 | spurious |
| cluster_label | 2 | 0.30 | 0.92 | 无 | spurious |
| **percentile** | 4 | 0.23 | 0.72 | 有 | 有效语义第二 |
| revision_change | 4 | 0.11 | 0.24 | 有 | 弱 |
| estimate_level | 3 | 0.10 | 0.29 | 有 | 弱 |
| **count** | 4 | **0.08** | 0.22 | 有 | **垫底区** |
| temporal_meta | 4 | 0.06 | 0.54 | 无 | spurious |
| sentiment | 4 | 0.05 | 0.57 | 有 | 弱 |
| novelty_time / unknown / score / direction | 2~4 | ≤0 | ≤0.81 | 有 | 无效 |
| dispersion / probability / **level_amount** | 4 | −0.41 / −0.51 / **−0.59** | ≤−0.12 | 有 | **反效** |

**62 条中 S≥1.58 = 0 个；|S|≥1.0 = 2 个（均负）。**

### 14.3 三条结论

1. **`identifier` / `text` / `cluster_label` 中位最高，但 S 是 spurious**（无 ordinal 语义 ⇒ rank 出的序无意义）。
   ⇒ **不可作信号**；同时**修正我此前「非信号 754 个应从候选池硬排除」的表述** ——
   正确表述是「不可作信号，**且必须靠 description 才能判定它无序号语义**」。
2. **有序号语义的类，排序 = `ratio`(0.50) > `percentile`(0.23) > `revision_change`(0.11) > `estimate_level`(0.10) > `count`(0.08) > `sentiment`(0.05) ≫ 其余**
   ⇒ `ratio`/`percentile` 依然排前（与 §十二方向一致），**但 `count` 落到垫底区**。
3. **`level_amount`（−0.59）与 `probability`（−0.51）反效** ⇒ 「水平型先标准化」不足以救活。

### 14.4 ★★★★ 自我纠错：我在同一天内第二次栽在 selection bias

**§十二 我算出 `count` 非 MODEL 命中率 13%，据此建议「count 是唯一有量的机会（期望 27.3）」—— 该建议错误。**
实测未测 `count` 配匹配骨架后**中位 S 仅 0.08**。

**根因**：命中率的分母（已测 count 字段）**不是随机样本** —— 它们是历史上**被刻意挑选**（有信号迹象）才去测的。
`count` 的 10.6% 命中率绝大部分来自 `analyst7` 那批被优选过的家数族字段，**不代表语义本身的能力**。

> **★ 硬纪律（新增）**
> **在「已测字段」上计算的任何命中率/产出率，不得用于预测「未测字段」的产出** —— 已测集合是被优选过的样本。
> **估计未测池产出率的唯一可靠做法 = 直接测未测字段（配匹配骨架）**，即本次所做。
> 同日内两次同源错误：§十二 被 `score` 的**未测数量**误导；本节被 `count` 的**已测命中率**误导。

### 14.5 本次扫描的真实价值

**62 条（8 波）就把「GBR 非 MODEL 未测池 2,578 个字段值不值得挖」用证据回答了：不值得。**
若盲挖（每波 8 条）需 **≈322 波**。
⇒ **「语义抽样扫测」应固化为每个新区域的第 0 步**：先花 8 波探明语义产出率，再决定是否开战役。
