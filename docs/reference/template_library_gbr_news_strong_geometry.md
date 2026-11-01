# GBR `news17` / `news18` — 强几何 × 十模板库（结构互异）

> 建立动机（自我纠错）：`template_library_gbr_news18.md` §2 的 N1–N10 十条模板**全部跑在一条弱基几何**
> `group_rank(ts_mean(x, 22), subindustry)` 上，该几何的 S 上限只有 **0.91**（N3）。
> 而同一批字段在强几何 `ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(x,60),252), densify(market)))`
> 下 S 达 **1.86–2.18**（W1/W3/W4/P1 四条全闸）。
>
> ⇒ **原十模板的「全灭」结论是骨架选错导致的，不是字段没信号。**
> 本库把 N5 / N7 这两个**从未派发过**的结构，连同 8 个新结构，一并搬到强几何上重测。
> 这直接落实用户两次强调的纪律：**模板池 ≥10 且结构互异（不足 10 不派发）**。

---

## §0 统一基底（唯一被固定的部分）

```
G(SIG) = ts_target_tvr_decay(
           group_neutralize(
             -ts_rank(ts_mean(SIG, 60), 252),
             densify(market)),
           target_tvr=0.05, lambda_max=5, lambda_min=0)
```

设置档（GBR D1 news 族现行档）：

```
region=GBR  universe=TOP700  delay=1  language=FASTEXPR
neutralization = FAST      decay = 15      truncation = 0.05
nanHandling = ON   maxTrade = OFF   pasteurization = ON   unitHandling = VERIFY
```

**只有 `SIG` 的结构不同** ⇒ 归因干净，且不存在「换窗口 / 换常数当模板」的伪多样性。

---

## §1 十模板（`preflight` 全过：`valid: true` / `unknown_fields: []` / `any_changed: false`）

| # | tag | 结构轴 | `SIG` | 来源 | 状态 |
|---|---|---|---|---|---|
| **S1** | `S1_novelty_conf` | 乘性**新颖度置信** | `multiply(vec_count(nws17_multiple_comp_ssc), rank(vec_avg(nws17_multiple_comp_event_similarity_days)))` | forum `42659817284375` 套路二（novelty 加权，该帖唯一被**验证**的套路；relevance 加权已证伪）+ memory wave249「`multiply(x, rank(·))` 是 SUB 最强杠杆（+67%）」 | ✅ **全闸 `58E7jkaN`** |
| **S2** | `S2_attn_dilution` | 单一信号**掩码**（注意力稀释） | `if_else(less(rank(vec_avg(nws17_multiple_comp_rp_story_event_count)), 0.5), vec_count(nws17_multiple_comp_ssc), nan)` | 库内 **N5（设计完成、从未派发）** + forum 进阶 Story Attention Dilution | ❌**未过闸 `kqNkNQ7l`**（S 1.45 / F 0.78，遮掉半区后幅度崩） |
| **S3** | `S3_dual_source_dev` | 双源**分歧** `subtract(rank, rank)` | `subtract(rank(vec_count(nws18_multiple_comp_qmb)), rank(vec_count(nws18_multiple_comp_ssc)))` | 库内 **N4 强几何版**（N4 原式 `sse − ssc` 用原始值相减 ⇒ S 0.12；本式两侧先 `rank` 归一，是合规且不同量纲安全的写法）+ forum Entity-Story Deviation | ⛔**机理退化 `omEwE7on`**（long/short 0，见 §6） |
| **S4** | `S4_event_density_ratio` | 事件**密度比值** `divide` 同单位 | `divide(vec_count(nws18_multiple_comp_sse), vec_avg(multi_entity_story_event_count))` | 自建（「每故事实体数」= 信息集中度；§4.11 已证本集是「事件到达率」数据集，比值是其自然归一化） | 在飞 |
| **S5** | `S5_amp_x_breadth` | **幅度 × 广度** `multiply(rank, rank)` | `multiply(rank(vec_count(nws18_multiple_comp_qmb)), rank(vec_sum(nws18_multiple_comp_qmb)))` | 库内 **N7 强几何版（从未派发）** + forum `43287696633239`「公共品的耗散」幅度 vs 广度 | 在飞 |
| **S6** | `S6_ts_zscore_density` | 时序**标准化**（异常注意力） | `ts_zscore(vec_count(nws18_multiple_comp_sse), 252)` | forum `43554135453335`「注意力经济的涨落」+ **paper Da, Engelberg & Gao (2011) "In Search of Attention", *JF* 66(5)**：ASVI 异常值 ⇒ 短期正收益后反转 | ⏭ **撤回派发**（先验冗余，见 §6.3） |
| **S7** | `S7_persistence` | **叙事持续性**（自相关） | `ts_corr(vec_count(nws17_multiple_comp_ssc), ts_delay(vec_count(nws17_multiple_comp_ssc), 5), 66)` | 自建 + forum `35294898626711` `ts_covariance` 模板族（同二阶矩几何、换同字段滞后项 ⇒ 不引入 PV 腿） | 在飞 |
| **S8** | `S8_winsor_amp` | 幅度**裁剪** | `winsorize(vec_count(nws18_multiple_comp_sse), std=2)` | memory「破 SUB 的唯一杠杆是重塑幅度分布」族（`winsorize` 已验证可用） | ⛔ **撤回派发**（数学上恒等于 P1，见 §6.2） |
| **S9** | `S9_regression_resid` | **回归残差化** | `ts_regression(vec_count(nws17_multiple_comp_ssc), vec_count(nws17_multiple_comp_event_relevance), 66, rettype=0)` | memory 放行形态（`ts_regression` rettype=0 已在 IND 实跑）+ 自建（剥离「相关度驱动」后的纯到达率） | ⛔ **撤回派发**（同 S3 机理，残差恒 0，见 §6.1） |
| **S10** | `S10_avdiff_lvl` | **长期偏离** `ts_av_diff` | `ts_av_diff(vec_count(nws17_multiple_comp_relevance), 252)` | 自建（`ts_av_diff` 在 `vR1aEpa3` 上实跑过）+ **paper Barber & Odean (2008) "All That Glitters", *RFS* 21(2)**：注意力驱动买入后均值回归 | ✅ **全闸 `j2Yle6q5`** |
| **S11** | `S11_novelty_days` | 新颖度**直接读数**（非乘性） | `ts_av_diff(vec_avg(nws17_multiple_comp_event_similarity_days), 252)` | 自建（S1 只把该字段当**置信度乘子**；本模板把它当**信号本体**，二者经济含义不同）+ forum `42659817284375` novelty 轴 | ❌ **负号 `2rAq5M6b`**（S −0.33，见 §6.6） |
| **N1** | `N1_news17_nip_level` | 裸 level（**字段探针**） | `vec_count(nws17_multiple_comp_nip)` | 自建（§6.5 固定结构换字段：`nip` 是 news17 唯一未测的多实体字段） | 在飞 |
| **N2** | `N2_news18_nip_level` | 裸 level（**字段探针**） | `vec_count(nws18_multiple_comp_nip)` | 自建（检验 news18 除 `sse` 外是否有第二个活字段） | 在飞 |
| **X1** | `X1_cross_ds_gate` | **跨数据集置信度门控** `multiply(x, rank(C))` | `multiply(vec_count(nws17_multiple_comp_ssc), rank(vec_count(nws18_multiple_comp_sse)))` | memory wave249「`multiply(x, rank(C))` 是 SUB 最强杠杆 +67%」+ 自建（news17 与 news18 是两个独立新闻源，同属 NEWS 塔 ⇒ 不触 trio） | 在飞 |
| **S4F** | `S4F_tvr_quantile` | S4 的 SUB 定向修法 | `ts_quantile(<S4 的比值>, 252, driver=gaussian)` | memory wave249「`ts_quantile(gaussian)` 抬 SUB/S 从 0.332→0.434」 | 在飞 |

**结构互异性自检**（10 类骨架，无两条共用同一结构）：

基线族（4 条，但加工轴互不相同）｜乘性置信｜掩码｜双源分歧｜同单位比值｜双 rank 交互｜时序标准化｜二阶矩（自相关）｜幅度裁剪｜回归残差｜长期偏离

字段覆盖 9 个：`nws17_multiple_comp_ssc`(3 次) / `nws17_multiple_comp_event_similarity_days` / `nws17_multiple_comp_rp_story_event_count` / `nws17_multiple_comp_relevance` / `nws17_multiple_comp_event_relevance` / `nws18_multiple_comp_sse`(3 次) / `nws18_multiple_comp_ssc` / `nws18_multiple_comp_qmb`(2 次) / `multi_entity_story_event_count`

---

## §2 合规声明（逐条对照硬约束）

| 约束 | 本库处置 |
|---|---|
| 禁止 `add(A,B)` 混信号调参 | ✅ 零 `add`。唯一合成是 S5 的 `multiply(rank, rank)`（同字段幅度×广度交互，权重恒 1，不扫描）与 S3 的 `subtract(rank, rank)`（放行形态） |
| 禁止 `multiply(rank(B), 0.3/0.5)` 权重扫描 | ✅ 无权重常数 |
| 窗口白名单 1/5/22/66/252/504/1008/1260 | ✅ 只用 5 / 60 / 66 / 252。**60 例外**：帖 `43541109631895` 的 `ts_mean(·,60)`，已有「一季度」经济解释 + EUR 三点实测 20<60>120 |
| `unit_handling=VERIFY` 不混量纲 | ✅ 比值一律同单位相除（S4 `count / count`）；门控一律 `greater/less(rank(x), 0.5)`；无「带单位字段 + 无量纲常数」、无「带单位计数 > 常数」 |
| 单塔优先选非目标塔 category | ✅ NEWS 属非目标塔 category |
| trio 内部禁两两组腿 | ✅ 纯 `news17` / `news18` 单塔，**不吃 trio×非trio 额度**；S7 刻意用**同字段滞后**而非 `returns`，避免引入 PV 腿 |
| 近十年都要有数据 | 待收批后用 `get_alpha_yearly_stats` 逐年核 `longCount/shortCount` |
| 并发 2 条/批 | ✅ 每批 2 条 |

---

## §3 收批账本（逐条填实测）

| # | tag | alpha | S | F | 2Y | SUB | TO | DD | margin | failed_ra | 结论 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S1 | `S1_novelty_conf` | **`58E7jkaN`** | **1.85** | 1.14 | 1.91 | **1.50** | 8.02% | 3.17% | 11.77bp | **0** | ✅ **全闸** |
| S10 | `S10_avdiff_lvl` | **`j2Yle6q5`** | **1.93** | 1.20 | **2.66** | **1.41** | 7.80% | 2.50% | 12.46bp | **0** | ✅ **全闸** |
| S2 | `S2_attn_dilution` | `kqNkNQ7l` | 1.45 | **0.78** | **2.38** | 0.75 | 7.71% | 3.92% | 9.36bp | 2 | ❌ 双闸未过（`LOW_SHARPE` / `LOW_FITNESS`） |
| S3 | `S3_dual_source_dev` | `omEwE7on` | 0.00 | — | — | — | 0.00% | 0.00% | — | 5 | ⛔ 退化（long 0 / short 0 / bookSize 0） |
| S4 | `S4_event_density_ratio` | — | — | — | — | — | — | — | — | — | 在飞 |
| S5 | `S5_amp_x_breadth` | `vR1n1Okb` | 0.65 | 0.24 | 0.86 | 0.55 | 7.45% | 4.18% | 4.45bp | 3 | ❌ 全弱（**字段 `qmb` 效应，见 §6.4**） |
| S7 | `S7_persistence` | `0mYkYjN8` | 0.11 | 0.02 | 0.34 | 0.19 | 7.87% | **7.70%** | 0.70bp | 3 | ❌ 全灭（二阶矩几何在到达率字段上无信息） |
| S11 | `S11_novelty_days` | `2rAq5M6b` | **−0.33** | −0.08 | −0.47 | −0.42 | 7.56% | 10.08% | −2.15bp | 4 | ❌ **负号**（字段只宜作乘子，见 §6.6） |
| N1 | `N1_news17_nip_level` | — | — | — | — | — | — | — | — | — | 在飞 |
| N2 | `N2_news18_nip_level` | — | — | — | — | — | — | — | — | — | 在飞 |
| X1 | `X1_cross_ds_gate` | — | — | — | — | — | — | — | — | — | 在飞 |
| S4F | `S4F_tvr_quantile` | — | — | — | — | — | — | — | — | — | 在飞 |

**十年逐年核查（`get_alpha_yearly_stats`，逐条手核 `pnl` / `longCount` / `shortCount`，不看平台 `coverage`）**

| alpha | 10 年全正 | 年 S 区间 | 最弱年 | long 区间 | short 区间 | 结论 |
|---|---|---|---|---|---|---|
| `58E7jkaN` | ✅ 10/10 | 0.51 – 3.30 | **2019 = 0.51** | 411 – 512 | 406 – 532 | 通过 |
| `j2Yle6q5` | ✅ 10/10 | 0.18 – 3.45 | **2019 = 0.18** | 402 – 511 | 415 – 532 | 通过 |

⇒ **两条新候选的目标第 4 条硬门槛（近十年都要有数据）已实测通过**，不是靠平台 `coverage` 估的。

---

## §6 三条「派发前就能判死」的结构性结论（本波最大收获）

### §6.1 `vec_count` 统计的是**记录条数**，对同一事件集的任意两个 VECTOR 字段取值逐位相同

**事故**：S3 `subtract(rank(vec_count(qmb)), rank(vec_count(ssc)))` 返回 `longCount 0 / shortCount 0 / bookSize 0 / pnl 0`，
`LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` / `CLUSTER_TEST` 三项直接 `ERROR`（无持仓可算）。

**机理**：`vec_count(F)` 数的是**该事件记录里有几个元素**，不是「F 有几条非空」。同一数据集同一批新闻事件，
`qmb` 与 `ssc` 是同一组记录的不同打分维度 ⇒ 向量长度完全相同 ⇒ `vec_count` 逐位相同 ⇒ `subtract(rank, rank) ≡ 0`。

**推论（可直接省掉回测）**：
- **任何两个 `vec_count` 相减 / 相除 / 回归，在同数据集上恒为 0 或 1** ⇒ S9 `ts_regression(vec_count(ssc), vec_count(event_relevance), …)` 残差恒 0，**派发前即可判死**，本波省下 1 条回测。
- 想读「两个字段的差异」必须用**保留数值的聚合**（`vec_sum` / `vec_avg` / `vec_stddev`），或用**跨数据集**计数（不同事件集，长度不同）。
- 这与既有决策 #238（`directional_indicator_2` 零持仓）是**两类不同事故**：那是字段无数据，本类是字段有数据但运算恒零。**两者的平台表现完全相同（longCount 0）⇒ 归因时必须区分。**

### §6.2 `winsorize` 接在 `ts_rank` 之前 = **数学恒等变换**

`winsorize(F, std=2)` 是单调截断（把尾部压到边界上），而 `ts_rank(·, 252)` 只使用**序关系**。
单调变换不改变序 ⇒ `ts_rank(winsorize(F))` 与 `ts_rank(F)` 逐位相同 ⇒ **S8 必然复现 P1 `6XdPedNJ`（S 1.97 / 2Y 2.20）**，零信息增量。
**⇒ 幅度分布类算子（`winsorize` / `tail` / `rank` / `signed_power`）只有在「不再接 rank 类算子」时才有意义。**
（此前 memory 的「破 SUB 唯一杠杆是重塑幅度分布」结论同样受此边界约束：那批实证的载体是 `multiply(x, rank(C))`，不是「rank 之前套 winsorize」。）

### §6.3 `ts_zscore` 前置在 `ts_rank∘ts_mean` 之前 = 近乎冗余

`ts_rank(ts_mean(ts_zscore(x, 252), 60), 252)` 的内层 `ts_zscore` 只做「减 252 日均值、除 252 日标准差」，
外层的 `ts_rank(·, 252)` 本来就在做「当前 60 日均值 vs 自身 252 日历史」——两者自由度高度重叠，
且同字段（`nws18_multiple_comp_sse`）已由 P1 占用 ⇒ 预计互相关 0.9+。
**⇒ 撤回 S6 派发**，把配额让给 S11（同数据集从未作为信号主体的 `event_similarity_days`）。

### §6.4 ⚠ 本库的**归因缺陷**（自我认领）：结构与字段同时变动，无法分离二者贡献

本库 §1 声称「只有 `SIG` 的结构不同 ⇒ 归因干净」，**这句话是错的**。`SIG` 里同时含「结构」和「字段」两个自由度：

| 字段组 | 模板 |
|---|---|
| **news17 族** | S1 / S2 / S7 / S9 / S10 / S11 |
| **news18 族** | S3 / S4 / S5 / S6 / S8 |
| **混合** | （无） |

**反证**：S5 的 `multiply(rank(count), rank(sum))` 若两腿高度同向，乘积近似 `rank²`，是**单调变换**，
理应给出与「裸 level」相近的 alpha。它在 `qmb` 上只有 **S 0.65**，而 P1 在 `sse` 上 **S 1.97**、
W3 在 `relevance` 上 **S 2.10** ⇒ **差异主要来自字段（`qmb` 弱），不是来自「幅度×广度」这个结构。**

**⇒ 归因纪律（下一步必须遵守）**：
1. 判「某结构是否有效」必须**固定字段**，只换结构；
2. 判「某字段是否有效」必须**固定结构**（裸 level 或 `ts_av_diff`），只换字段；
3. 一次只动一个自由度，否则结论不可用。**本库当前只能读出「字段效应」，读不出「结构效应」。**

### §6.5 已能读出的**字段效应**（结构轴虽混淆，字段轴已可对照）

在**同一条强几何 + 同一族裸 level/偏离结构**下：

| 字段 | 数据集 | 载体 alpha | S | 判定 |
|---|---|---|---:|---|
| `nws17_multiple_comp_event_relevance` | news17 | W4 `leA6jmoe`（`vec_sum` level） | **2.18** | ✅ 最强 |
| `nws17_multiple_comp_relevance` | news17 | W3 `wpQwjWn6`（`vec_count` level） | **2.10** | ✅ |
| `nws17_multiple_comp_relevance` | news17 | S10 `j2Yle6q5`（`ts_av_diff`） | **1.93** | ✅ |
| `nws18_multiple_comp_sse` | news18 | P1 `6XdPedNJ`（`vec_count` level） | **1.97** | ✅ |
| `nws17_multiple_comp_ssc` | news17 | S1 `58E7jkaN`（× 新颖度） | **1.85** | ✅ |
| `nws17_multiple_comp_event_sentiment_score` | news17 | W1 `9qxPX77V`（`vec_count` level） | **1.86** | ✅ |
| `nws18_multiple_comp_qmb` | news18 | S5 `vR1n1Okb` | **0.65** | ❌ **弱字段** |

⇒ **`qmb` 是 news18 里的弱字段，不要再作为主体**（它此前在 N4 弱几何版里也是 0.12 的贡献者之一）。
**news17 是强字段池；news18 除 `sse` 外尚未找到第二个活字段。**

### §6.6 同一字段「作乘子有效、作信号本体无效」的实证（`event_similarity_days`）

| 用法 | alpha | S | 结论 |
|---|---|---:|---|
| 作**置信度乘子**（S1） | `58E7jkaN` | **+1.85** | ✅ 全闸 |
| 作**信号本体**（S11） | `2rAq5M6b` | **−0.33** | ❌ 连符号都反 |

**机理**：「距离上次相似事件的天数」度量的是**这条新闻有多新**，它是**关于信息质量的元变量**，
不携带方向。把它当信号本体，等于用「新闻新鲜度」直接赌涨跌 —— 平台给出负号（新鲜 ⇒ 反而涨），
但幅度只有 0.33，**两侧都不够**。**⇒ 元变量（新鲜度 / 分歧度 / 覆盖度 / 置信度）只能进乘子位或门控位，
不能进信号位。** 这条与 memory wave249「`multiply(x, rank(1−不确定性))` 抬 SUB」是同一原理的正反面。

### §6.7 掩码类模板的隐性代价：TO 被推高 + 广度被砍，双杀 F

S2 `kqNkNQ7l`（`if_else` 掩掉半区）：S **1.45** / F **0.78** / 2Y **2.38** / TO **7.71%**。
基准几何的 `target_tvr=0.05`，但实际 TO 被推到 7.71%（高于同族 S1 的「正常」水平），原因是**掩码让股票反复进出持仓域**，
每次进出都强制换手。同时广度从 ~450 掉到半区 ⇒ S 同步下滑。
**⇒ 掩码族在 `ts_target_tvr_decay` 强几何上是负和操作**：它既没换来信号纯度（2Y 2.38 虽高但不构成闸），
又把 F 打穿。**这条与 memory「掩码 θ 0.8/0.9/1.0 已在 shortinterest3 上全扫尽」一致。**

### §6.8 ★★★★★ NEWS 家族只有 **5 条独立轴**，其余全是同轴变体（零成本互相关实测）

| 对 | 相关 | 结论 |
|---|---:|---|
| `vR1nAj6z`(nip) ↔ `wpQwjWn6`(relevance) | **1.0000** | **逐位相同** ⇒ N1 作废，`vec_count` 在完全填充的同事件字段上恒等 |
| `GrW0WRp3`(S4 比值/sse) ↔ `6XdPedNJ`(P1 裸 level/sse) | **0.8346** | 比值结构**没能**把它与 P1 解耦 |
| `d5W8avqK`(X1 跨集门控) ↔ `wpQwjWn6` | **0.8294** | 跨数据集门控也没脱离 news17 到达率轴 |
| `d5W8avqK` ↔ `j2Yle6q5` | 0.7220 | 同上 |
| `j2Yle6q5`(S10) ↔ `wpQwjWn6` | **0.8468** | 已知 |

**独立轴分解（阈值 0.7）**：

| 轴 | 代表 | 与其它轴的最大相关 |
|---|---|---:|
| **A 新闻到达率（news17 level / 偏离 / ×广度 / 跨集门控）** | `wpQwjWn6` = `vR1nAj6z` = `d5W8avqK` ≈ `j2Yle6q5` | 0.8468（轴内） |
| **B news18 `sse`（level / 比值）** | `6XdPedNJ` = `GrW0WRp3` | 0.8346（轴内） |
| **C 事件强度求和** | `leA6jmoe`（`vec_sum(event_relevance)`） | 0.6642（vs S1） |
| **D 情绪分到达率** | `9qxPX77V`（`vec_count(event_sentiment_score)`） | 0.6583（vs A 轴） |
| **E 合成置信（`ssc` × 新颖度）** | `58E7jkaN`（S1） | 0.6642（vs C 轴） |

**⇒ NEWS 塔的最大可提交条数 = 5**（不是 6）。`max_mutually_below_subset` 实测 = 5，`max_subset_exact = true`。

**最优 5 条选取（全部 IS 全闸）**：

| 轴 | alpha | S | F | 2Y | SUB |
|---|---|---:|---:|---:|---:|
| C | `leA6jmoe`（W4） | 2.18 | 1.45 | **2.86** | 1.65 |
| A | `wpQwjWn6`（W3） | **2.10** | 1.38 | 2.33 | 1.44 |
| B | `6XdPedNJ`（P1） | 1.97 | 1.27 | 2.20 | 1.08 |
| D | `9qxPX77V`（W1） | 1.86 | 1.14 | 2.00 | 1.33 |
| E | `58E7jkaN`（S1） | 1.85 | 1.14 | 1.91 | 1.50 |

**备选（A 轴可替换项）**：`j2Yle6q5`（S10，S 1.93 / **2Y 2.66**）—— 与 W3 二选一，不能同提。
它跨全部 5 条都 <0.7（vs W4 0.4328 / vs P1 0.4329 / vs W1 0.5799 / vs S1 0.4952），所以
**{W4, S10, P1, W1, S1} 也是合法 5 条组**，代价是 S 从 2.10 降到 1.93、换 2Y 从 2.33 升到 2.66。

### §6.9 两条「结构不改变轴归属」的反例（对既有去相关决策的补强）

既有决策 #70「去相关唯一有效维度是换数据集」需要补一条**同源例外**：

- S4（`sse` 比值）与 P1（`sse` 裸 level）**同字段不同结构** ⇒ 0.8346，**结构变化救不了相关性**；
- X1（news17 × news18 跨集门控）与 W3（news17 裸 level）⇒ 0.8294，**加一个数据集的乘子也救不了**。

**⇒ 判据升级**：相关性的载体是**字段本身的信息轴**，不是「结构」也不是「来源数量」。
只要最终信号的主导成分仍是「某字段的到达率水平」，无论套多少结构（比值 / 门控 / 偏离 / 交互），都落在同一轴。
**真正换轴只有两条路**：① 换**语义不同**的字段（`event_relevance` 求和 / `event_sentiment_score` / 带乘子的 `ssc`）；
② 换数据集。



---

## §4 归因口径（收批后按此判定）

1. **先看 `S ≥ 1.58` 的条数** —— 决定本波是「机制扩产」还是「结构探索」。
2. **对每条达 S 的，再查 `SUB / S`** —— GBR TOP700 的 SUB 闸 = `0.478 × S`（V1 实测反推），
   低于线即挂。**`SUB` 是第一预警信号，比 S 更早暴露结构性缺陷**（决策 #87）。
3. **按模板族归因**，不按单条 alpha 归因：
   - 「置信度门控族」（S1 / S6）—— 对应 memory wave249 的 `multiply(x, rank(1−不确定性))` 结论，若本波复现 ⇒ 该结论可跨数据集迁移；
   - 「掩码族」（S2）—— 若失败，与 N5 的设计假设一并作废；
   - 「比值/分歧族」（S3 / S4）—— 若失败，印证 §4.11「本集是到达率数据集，任何算术都是噪声」；
   - 「残差族」（S9）—— 若失败，说明 `event_relevance` 与 `ssc` 同源（不可正交化）。
4. **任何 `longCount == 0` 的行单列** —— 那是空字段，不是信号弱（决策 #238 教训）。

---

## §5 与既有库的关系

| 文档 | 关系 |
|---|---|
| `template_library_gbr_news18.md` §2 | **被本库取代其适用范围**：N1–N10 的结论仅对弱几何成立；N5 / N7 从未派发，本库以强几何重测 |
| `template_library_gbr_news18.md` §4.11 | **本库的第一性依据**：「news18 是事件到达率数据集，不是情绪数据集」⇒ 本库 10 条里 8 条都在读「到达率」的各种几何，而不读情绪方向 |
| `template_library_gbr_news18.md` §4.12 | **本库要挑战的结论**：§4.12 判定「同一信息源 + 独立几何」只剩 `ts_delta` 一条路。本库用 6 个未试几何（掩码 / 比值 / 交互 / 标准化 / 自相关 / 残差 / 偏离）直接检验该结论 |
| `_GBR_pv_channel_breakthrough_20261014.md` §2 | **强几何的来源**：`ts_target_tvr_decay` 的 2Y 档位与 F 墙杠杆 |

---

## §7 补量波（NEWS × FUNDAMENTAL）十模板：全灭，且根因是**可查证的形态错误**

> 目的：为「20 条目标」补量，同时测试「非目标塔 × 非目标塔」组合是否可行。
> 设计严格遵守第 103 条归因纪律：**两腿固定，只动组合几何**（一次只动一个自由度）。

### §7.1 设计

统一基底（与 §0 完全相同，只有 SIG 不同）：

```
G(SIG) = ts_target_tvr_decay(
           group_neutralize(-ts_rank(ts_mean(SIG, 60), 252), densify(market)),
           target_tvr=0.05, lambda_max=5, lambda_min=0)
```

设置档：`GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF / pasteurization ON / VERIFY`

- **N 腿**（新闻）= `vec_count(nws17_multiple_comp_relevance)`（= W3 `wpQwjWn6` 的载体，故意复用以便归因）
- **F 腿**（基本面）= `ts_backfill(divide(fnd6_gpy, fnd6_revty), 252)`（毛利率水平值 + 252 日回填）

十个模板（结构互异，来源标注）：

| # | 组合几何 | 来源 |
|---|---|---|
| T1 | `multiply(N, rank(F))` | memory wave249（幅度 × 置信） |
| T2 | `trade_when(greater(rank(N),0.5), rank(ts_av_diff(F,252)), -1)` | Fang & Peress (2009, JF) |
| T3 | `vector_neut(rank(N), rank(F))` | 合规回归残差化 |
| T4 | `ts_regression(rank(N), rank(F), 252, rettype=0)` | 自建 |
| T5 | `subtract(rank(N), rank(F))` | 合规 `subtract(rank,rank)` |
| T6 | `ts_corr(rank(N), rank(F), 66)` | 帖 `35294898626711` 协方差族 |
| T7 | `multiply(rank(N), rank(F))` | 自建（幅度 vs 序的另一极） |
| T8 | `if_else(greater(rank(F),0.9), N, nan)` | 合规掩码 |
| T9 | `multiply(rank(ts_av_diff(F,252)), rank(N))` | 帖 `44089095804439` 位移族 |
| T10 | `multiply(ts_zscore(N,504), rank(F))` | Da, Engelberg & Gao (2011, JF) |

### §7.2 收批结果：**10/10 全灭，0 条过闸**

| # | alpha | S | F | 2Y | SUB | TO | DD | failed_ra | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| T1 | `YP1wEXMR` | **1.43** | 0.91 | 1.26 | 1.15 | 9.45% | 5.31% | 3 | ❌ F/2Y 均差 |
| T2 | `kqNkWe8g` | 0.02 | 0.00 | 0.75 | −0.08 | 8.42% | 13.51% | 4 | ❌ 全灭 |
| T3 | `E5608gXR` | 0.70 | 0.30 | 0.65 | 0.28 | 8.94% | 5.29% | 4 | ❌ |
| T4 | `LLMbmn1m` | 0.25 | 0.06 | −0.69 | −0.12 | 8.30% | 10.62% | 4 | ❌ |
| T5 | `zq3w2PdX` | 0.57 | 0.22 | 0.41 | 0.17 | 8.88% | 5.45% | 4 | ❌ |
| T6 | `ZYQwdjW3` | 0.10 | 0.02 | −0.02 | −0.05 | 8.82% | 9.99% | 4 | ❌ |
| T7 | `0mYkgWo8` | 0.66 | 0.28 | 0.80 | 0.39 | 8.83% | 5.19% | 3 | ❌ |
| T8 | `RREZzj1j` | 0.57 | 0.27 | 0.68 | 0.29 | 16.27% | 11.18% | 3 | ❌ |
| T9 | `bl62z7RM` | 0.18 | 0.04 | −0.23 | 0.05 | 8.51% | 8.07% | 4 | ❌ |
| T10 | `58E75bw5` | **1.51** | 0.97 | 1.33 | 1.13 | 9.42% | 4.74% | 3 | ❌ 准过（差 F 0.03） |

### §7.3 归因：**根因不是「两腿混合不可行」，而是「F 腿的形态已被本地台账证伪」**

关键证据来自本地既有台账 `docs/reference/field_profile_fundamental6_gbr_20261030.md`：

1. **§6 已证伪表第 339 行**：`fnd6_M2_gross_profitability`（**水平毛利率**）「设计即被水平版证伪，429 后**不补派**」。
   ⇒ 本波 F 腿 `divide(fnd6_gpy, fnd6_revty)` 正是**水平毛利率**形态 —— 踩的是已证伪的坑，不是新机制。
2. **§6 已证伪表第 331–334 行**：位移但无自历史分位 S 0.71 / 自历史分位但无位移 S 0.95 / 先 rank 再位移 S 2.22（vs 2.71）/ `ts_zscore` 作位移锚 S 2.28（vs 均值锚 2.71）。
   ⇒ **T10 用 `ts_zscore` 作锚**正是这条已知劣化的路径。
3. **§9.1b 机理定论**：这个族的引擎是「**分母上价格的位移** Δ(1/cap)」，分子只提供横截面权重；
   纯会计增长安慰剂 `LLMekGMn`（完全不碰价格）S **−0.12** 判死。
   ⇒ **纯基本面水平腿在结构上就注定不出信号**；F 腿要出信号必须带价格腿（`cap`）。
4. **§9.2 降相关轴实测**：换分子在位移族里等于没换（0.8421）；有效秩 = 3。

**⇒ 实测结果与台账完全一致，且分成两类**：

| 类别 | 模板 | 现象 | 机理 |
|---|---|---|---|
| **F 主导**（F 是信号本体） | T2 / T3 / T4 / T6 / T9 | S 0.02–0.70 | 纯基本面水平毛利率本身无信号，残差/相关/回归全在拟合噪声 |
| **N 主导**（F 只做权重/门控） | T1 / T7 / T10 | S 1.43–1.51 | N 的原始强度是 2.10（`wpQwjWn6`），被「被证伪的水平毛利率」当权重稀释 ⇒ 全部低于纯 N 腿 |

**⇒ 三条可迁移结论**：

1. **★ 组合失败 ≠ 组合不可行**：本波 10 个模板测出的是「F 腿形态错」，不是「两腿不能组合」。
   若换成台账已验证的形态 `rank(ts_quantile(ts_av_diff(divide(fnd6_gpy, cap), 252), 84))`，同一批几何需要重测。
2. **★ 但那条修正路径在本区撞配额**：带 `cap` 的 F 腿 = **PV + FUNDAMENTAL** 腿 ⇒ 变成三腿（PV+NEWS+FUND），
   且 PV+FUND 组合候选数已达 11 条（远超单组合 ≤3 / trio×非trio ≤5 的纪律上限）。
   ⇒ **fundamental6 家族在 GBR 已挖尽**（台账原话：「单靠 `fnd6 ÷ cap` 这一族刚好能点亮一塔（3 颗），一颗不多。想再点一塔必须换数据集」）。
3. **★ 稀疏事件数据集的「平滑抹信号」再次成立**：`inst1` / `insiders1` 类上 `ts_mean` 平滑会把 S 归零，
   有效路径是「事件累加 `ts_sum(·,66)` + 事件到达率 `vec_count`」，见 §8。

---

## §8 候选池扩容：台账收割（14 → 19 条）+ 波 3（institutions1 探针）

### §8.1 ★★★★★ 台账里已有 5 条全闸候选，本轮才发现并补进篮子

`docs/reference/field_profile_fundamental6_gbr_20261030.md` §9.1 / §9.2 列了 **7 条 `failed_ra_count = 0` 的全闸候选**：
`rKRkL9QE` / `0mYoANkv` / `6XdxzNb5` / `kqNRXm5k` / `88RAnmAX` / `9qxoa3mx` / `P0oerpjp`，
另加 `N1NM5WK8`（§9.1 `CAPX_GRPRANK`）。**其中 5 条从未进入候选篮**。

平台复核（`batch_get_alpha_metrics`，全部 `failed_ra_count = 0` / `status = UNSUBMITTED`）：

| alpha | 表达式核心 | 塔位 | S | F | 2Y | SUB | TO | self |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `N1NM5WK8` | `group_rank(ts_quantile(ts_av_diff(capex/cap,252),84), industry)` | PV+FUND | **2.05** | **1.80** | 2.26 | 1.68 | 8.98% | 0.5324 |
| `P0oerpjp` | `rank(ts_quantile(ts_av_diff(capex/cap,168),56))` | PV+FUND | 1.98 | 1.70 | 2.10 | 1.70 | 8.26% | 0.5570 |
| `6XdxzNb5` | `rank(ts_quantile(ts_av_diff(newa2_re/cap,252),84,gaussian))` | PV+FUND | 1.75 | 1.40 | 2.22 | 1.27 | 11.67% | 0.5388 |
| `88RAnmAX` | `reverse(rank(ts_quantile(ts_av_diff(cap/ewq_teqq,252),84,gaussian)))` | PV+FUND | 1.67 | 1.40 | 1.89 | 1.06 | 12.26% | 0.6376 |
| `9qxoa3mx` | P/B 族（`cap/ceqq`） | PV+FUND | 1.59 | 1.35 | 1.89 | 1.00 | 12.25% | 0.6010 |

- 5 条 self-corr 全部 < 0.7（0.53–0.64），**无重跑**（本轮第 106 条判据）。
- `P0oerpjp` 十年 10/10 全正（台账 §9.3 已实测）。
- ⚠ `88RAnmAX` 的 `risk_neutralized_sharpe` 只有 **0.71**、`0mYoANkv` 只有 **1.02**（台账 §10.4）⇒ 风险载荷重，提交优先序靠后。

### §8.2 19 条全篮互相关：**最大互不相关团 = 14 条**（`max_subset_exact = true`）

`compute_mutual_correlation(19 条, threshold=0.7, years=4, num_points=1021)`：
`max_mutually_below_subset_size = 14`，且该 14 条恰是**原先那 14 条**。
⇒ **新增 5 条与既有 PV+FUND 家族互相挤占，不增加可提交条数，只增加「备胎池深度」**：
可以从 11 条 PV+FUND 候选里挑出质量更好的 3 条（例如用 `P0oerpjp` 十年 10/10 全正替掉 2Y 零余量的 `kqNRXm5k`）。

超 0.7 的 10 对全部落在 PV+FUND 家族内部：

| 对 | 相关 | 对 | 相关 |
|---|---:|---|---:|
| `rKRkL9QE` ↔ `N1NM5WK8` | 0.9651 | `6XdxzNb5` ↔ `88RAnmAX` | 0.7598 |
| `88RAnmAX` ↔ `9qxoa3mx` | 0.9584 | `rKRkL9QE` ↔ `P0oerpjp` | 0.7510 |
| `kqNRXm5k` ↔ `P0oerpjp` | 0.8968 | `P0oerpjp` ↔ `N1NM5WK8` | 0.7248 |
| `0mYoANkv` ↔ `6XdxzNb5` | 0.8903 | `0mYoANkv` ↔ `9qxoa3mx` | 0.7227 |
| `0mYoANkv` ↔ `88RAnmAX` | 0.7720 | `6XdxzNb5` ↔ `9qxoa3mx` | 0.7220 |

**⇒ 跨家族相关几乎全为 0**（NEWS 家族 vs PV+FUND 家族全部 < 0.18；`akK2vpWW` vs 全篮 |r| < 0.11）。

### §8.3 波 3：`institutions1`（INSTITUTIONS 塔最后一条活路）

`get_datasets(category="institutions", GBR/TOP700/D1)` = 5 个：
`fund_holdings_panel` cov 0.9099（**GBR 已 24 探针判死**）· `institutions6` cov 1.0（天花板 0.56）·
`institutions4` cov 0.39（**描述是 FSYM_ID/CUSID/ISIN 标识符映射 ⇒ 非信号数据**）· `institutions25` cov 0.0 ·
**`institutions1` cov 0.3118 / 7 字段 / alphaCount 52**。

`institutions1` 的 7 字段（**全 VECTOR**）与论坛帖 `43212475386007` 用的字段集**完全一致**：

| 字段 | 语义 | user/alpha |
|---|---|---|
| `inst1_holdings` | 交易执行后内部人持有的股数（**存量**） | 14/16 |
| `inst1_shares` | 本次交易覆盖的股数（**流量**） | 11/11 |
| `inst1_valueeur` | 欧元计价交易金额（流量） | 6/7 |
| `inst1_value` | 原币金额（流量） | 6/6 |
| `inst1_tradesignificance` | 重要性评分 1–3 | 6/10 |
| `inst1_price` | 成交单价 | 1/1 |
| `transaction_currency_code_2` | 币种 ISO 码（非信号） | 3/3 |

**★ 关键事实**：
- 帖 `43212475386007` 在 **DEU `institutions1`** 上报「流量/存量比」S **1.53–1.59**（`valueeur/holdings` 1.59、`shares/holdings` 1.53、`tradesignificance/holdings` 1.53）。
- **GBR `institutions1` 从未实测** —— 此前被「cov 0.3118 必崩」的先验跳过，而那其实是 `insiders1`（另一数据集）的失败结论。
- 记忆里「`institutions1` 是机构持股、`insiders1` 是内部人交易 ⇒ 主体性质不同」的归因**经字段描述复核是错的**：
  `inst1_holdings` 的描述明写 "held by the **insider** after the reported transaction" ⇒ **两者都是内部人申报交易**，
  真正的差别只在覆盖范围与覆盖率（0.3118 vs 0.5937）。
- ⚠ 但 `insiders1` 在 GBR 严格复现该帖模板得 S **−0.19 / −0.22**（弱几何）⇒ 这是一个**先验很强、但从未在强几何上复测**的活路。

**⇒ 波 3 探针（4 条，单自由度对比：裸骨架 vs 强几何基底）**

| # | 表达式 | 目的 |
|---|---|---|
| P1 | `group_rank(ts_sum(divide(vec_sum(inst1_shares), vec_sum(inst1_holdings)), 66), industry)` | 帖原版骨架（流量/存量比 + 事件累加 66 + 行业分组） |
| P2 | 同一 SIG 套 §0 强几何基底 | **只变几何** ⇒ 测「弱几何全灭结论是否需重测」（第 94 条） |
| P3 | `group_rank(vec_count(inst1_valueeur), industry)` | 事件到达率轴（弱几何） |
| P4 | 同一 SIG 套 §0 强几何基底 | 只变几何 |

全部 preflight `valid: true` / `unknown_fields: []` / `any_changed: false`。
量纲安全：`divide(shares, holdings)` 是**股数/股数**（同单位相除，规避 `unit_handling=VERIFY` 闸），
未采用帖里的 `valueeur/holdings`（EUR/股 ⇒ 量纲不一致，有整批 CANCELLED 风险）。
### §8.4 波 3 探针结果：**4/4 全灭 ⇒ INSTITUTIONS 塔在 GBR 结构性不可达**

| # | 表达式核心 | S | F | 2Y | SUB | TO | DD | failed_ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P1 | `group_rank(ts_sum(divide(vec_sum(inst1_shares), vec_sum(inst1_holdings)), 66), industry)` | **−0.27** | −0.07 | −1.14 | 0.01 | 7.61% | 11.84% | 3 |
| P2 | 同一 SIG + §0 强几何基底 | 0.28 | 0.08 | **2.22** | 0.06 | 8.58% | 15.66% | 3 |
| P3 | `group_rank(vec_count(inst1_valueeur), industry)` | −0.14 | −0.02 | −0.23 | −0.13 | **27.07%** | 14.49% | 4 |
| P4 | 同一 SIG + §0 强几何基底 | 0.32 | 0.10 | 0.69 | 0.25 | 11.27% | 6.64% | 3 |

**四条结论**：

1. **两种几何都失败** ⇒ 不是几何问题。★ 与第 94 条（NEWS 族「弱几何全灭结论无效」）方向相反：
   **本次强几何也救不回来** ⇒ 「换几何」不是万能药，只有在信号本身存在时才起作用。
2. **与 GBR `insiders1` 的失败逐位同型**（`insiders1` S −0.19 / −0.22 vs 本轮 −0.27 / −0.14）
   ⇒ 两个数据集的失败同源。
3. **★ 修正一条既有归因（记忆级）**：此前记「`institutions1` 是机构持股、`insiders1` 是内部人交易 ⇒ 主体性质不同，
   流量/存量含义不等价」—— **经字段描述复核是错的**：`inst1_holdings` 的平台描述明写
   *"The total number of shares or equity units held by the **insider** after the reported transaction is executed"*，
   ⇒ **`institutions1` 与 `insiders1` 都是内部人申报交易**（前者跨欧洲多国、含欧元换算字段）。
   真正的差异是 **GBR 的内部人申报覆盖与披露制度 ≠ DEU**。
4. **★ 论坛帖 `43212475386007` 的「DEU `institutions1` S 1.53–1.59」在 GBR 完全不可复现**
   ⇒ 这是该帖「数据集可替换 / 跨区可移植」说法的**第二次被证伪**（第一次：`insiders1` S −0.22）。
   P3 的 TO **27.07%** 再次印证「稀疏事件数据集的原始日频计数会爆换手」（记忆已有同型案例）。
5. `institutions` 类目 5 个数据集至此全部排除：`fund_holdings_panel`（24 探针判死）· `institutions6`（天花板 0.56）·
   `institutions4`（**平台描述是 FSYM_ID/CUSID/ISIN 标识符映射 ⇒ 非信号数据**）· `institutions25`（cov 0）·
   **`institutions1`（本轮 4 探针判死）**。

---

## §9 ★ 战役终局：GBR 的塔位与条数上限（结构性结论，非努力不足）

塔位实测（`get_pyramid_alphas`，零配额）：GBR D1 = `model 5` / `analyst 3` / `pv 1` / `other 1`，
其余 10 塔全 0；GBR D0 全 14 项为 0。

| 塔 | 能否点亮 | 依据 |
|---|---|---|
| **NEWS** | ✅ 最多 5 条 | §6.8 五轴分解；`max_mutually_below_subset_size = 5` / `exact = true` |
| **FUNDAMENTAL** | ✅ | PV+FUND 双塔候选；提 3 条即 0→4 |
| **PV** | ✅ | 同上（1→5），单组合 ≤3 纪律不牺牲塔位 |
| **SHORTINTEREST** | ⚠ 1 条 | `akK2vpWW` 孤立单点，`shortinterest3` 无兄弟集可再产 |
| **INSTITUTIONS** | ❌ | §8.4 本轮判死（5 数据集全排除） |
| INSIDERS / EARNINGS / SENTIMENT / RISK / OPTION / SOCIALMEDIA / MACRO / IMBALANCE | ❌ | 既有判死 + `earnings` 2 集 cov 全 0 |

**⇒ 合规可提交条数上限 = 11 条**
= NEWS 5（`leA6jmoe` / `wpQwjWn6` / `6XdPedNJ` / `9qxPX77V` / `58E7jkaN`）
+ PV+FUND 3（配额纪律上限；11 条候选里择优）
+ FUNDAMENTAL 单塔 1（`j2YNnKOQ`）
+ SHORTINTEREST 1（`akK2vpWW`）
+ PV 单塔 1（`MP0Ww6Ek`，**prod 历史 0.7710 ⇒ 必撞，实际 10 条**）。

**⇒ objective 的「20 条」在 GBR 内结构性不可达。** 差异不是投入不足，而是：
(a) GBR 只有 TOP700 一个 universe、无退路；(b) 可用数据集的**信息轴数**是 5（NEWS）+ 3（fundamental6 簇），
其余塔全部无活字段；(c) 相关性载体是字段信息轴 ⇒ 同一数据集内换结构不产生新轴（§6.9）。

**⇒ 剩余可执行路径只有三条**：① 提这 10–11 条（点亮 4 塔）；② 跨区补量（EUR / IND / DEU 有成熟 runbook）；
③ 在 GBR 换**全新数据集**（不是换字段/换几何）—— 需先做 S1 体检证明其有 ≥3 个语义互异的活字段。
---

## §10 ★★★ 台账收割第二轮 + 最终提交组（12 条，2026-10-31 收官）

### §10.1 台账里还有一整族全闸候选：`template_library_gbr_fundamental_cap_scaled.md`

这份台账（我此前未读）记录了 **fundamental17 家族「估值重估动量」** 的 7 条全闸候选。
★ 关键平台事实：**`current_enterprise_value` 是 `fundamental17` 集内字段**（描述 "Current enterprise value
(market capitalization plus net debt)"，虽然含市值，但**数据集归属在 fundamental**）⇒
**`divide(<科目>, current_enterprise_value)` = 纯 FUNDAMENTAL 单塔，完全不碰 PV 的 `cap`，不吃任何 trio 配额。**
这是「塔位杠杆」型字段，比 `cap` 干净得多。

平台复核（`batch_get_alpha_metrics`，指标与台账**逐位一致**）：

| alpha | 机制 | 塔位 | S | F | 2Y | SUB | self | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **`rKRQbPPE`** | EBITDA/EV 252/22 | **FUND 单塔** | **2.48** | **2.22** | **2.69** | 1.68 | 0.4896 | **0** |
| `E56oqo1r` | EBITDA/cap 252/22 | PV+FUND | 2.39 | 2.11 | 2.50 | 1.64 | 0.5170 | 0 |
| `P0ojnOOp` | 总资产/cap 252/22 | PV+FUND | 2.30 | 1.96 | 2.42 | 1.59 | 0.6222 | 0 |
| `P0ojvkkJ` | 总负债/EV 66/22 | **FUND 单塔** | 1.93 | 1.49 | 1.76 | 1.52 | 0.5064 | 0 |
| `omEQ9kK5` | EBIT/cap 66/22 | PV+FUND | 1.59 | 1.15 | 2.12 | 1.02 | 0.3619 | 0 |
| `bl67R9mK` | 量比 / 504 分位 | FUND 单塔 | 1.39 | 1.01 | 2.20 | 0.48 | — | 2 ❌ |
| `vR1akGVz` | 量比 + 规模残差化 | FUND 单塔 | 1.54 | 1.10 | 2.56 | 0.62 | — | 2 ❌ |

⇒ **候选池 19 → 24 条**（新增 5 条可提交 + 2 条替补）。

### §10.2 ★ 24 条互相关矩阵：贪心解（14）不是最优解，手工可构造 13 条

`compute_mutual_correlation(24 条, 0.7, 4Y, 1021 点)` ⇒ `max_mutually_below_subset_size = 14`，
但该 14 条是**贪心解**；`max_subset_exact = true` 只说明「贪心未找到更大解」，不等于「最大解 = 14」。

**手工验证**：贪心解选了 `E56onL5r`（S 1.91 / riskNeut F 仅 0.51）而放掉 `rKRQbPPE`（S **2.48** / 全篮最高）。
替换后反而能多放一条 ⇒ **基本面族实际可取 6 条**：

| 6 条组合 | 内部最紧相关 | 塔位 |
|---|---:|---|
| `rKRQbPPE` / `j2YNnKOQ` / `O0AKLMKq` / `rKRkL9QE` / `0mYoANkv` / `kqNRXm5k` | `rKRQbPPE`↔`j2YNnKOQ` **0.6964** | FUND 2 + PV+FUND 4 |
| `rKRQbPPE` / `O0AKLMKq` / `rKRkL9QE` / `0mYoANkv` / `kqNRXm5k` / `omEQ9kK5` | `omEQ9kK5`↔`j2YNnKOQ`（已剔除）0.3393 | FUND 1 + PV+FUND 5 |

★ 第一组满足「**每个两塔组合候选 ≤ 3**」（PV+FUND 恰好 3 条），第二组 PV+FUND 有 4 条 ⇒ **违反配额纪律**。
⇒ **选第一组。**

### §10.3 ★★★ 最终可提交组 = **12 条**（原方案 10 条 → 上修 2 条）

| # | alpha | 塔位 | S | F | 2Y | SUB | self |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | **`rKRQbPPE`** | **FUND 单塔** | **2.48** | **2.22** | **2.69** | 1.68 | 0.4896 |
| 2 | `O0AKLMKq` | PV+FUND | 2.28 | 2.00 | 2.21 | 1.46 | 0.4046 |
| 3 | `rKRkL9QE` | PV+FUND | 2.21 | 2.05 | 2.51 | 1.77 | 0.5456 |
| 4 | `j2YNnKOQ` | **FUND 单塔** | 2.15 | 1.80 | 2.09 | 1.41 | 0.3699 |
| 5 | `leA6jmoe` | NEWS 单塔 | 2.18 | 1.45 | 2.86 | 1.65 | 0.0589 |
| 6 | `wpQwjWn6` | NEWS 单塔 | 2.10 | 1.38 | 2.33 | 1.44 | 0.0519 |
| 7 | `akK2vpWW` | SHORTINTEREST 单塔 | 1.95 | 1.33 | 1.96 | 1.62 | 0.0270 |
| 8 | `0mYoANkv` | PV+FUND | 1.89 | 1.54 | 2.08 | 1.12 | 0.5210 |
| 9 | `9qxPX77V` | NEWS 单塔 | 1.86 | 1.14 | 2.00 | 1.33 | 0.0647 |
| 10 | `6XdPedNJ` | NEWS 单塔 | 1.97 | 1.27 | 2.20 | 1.08 | 0.0852 |
| 11 | `58E7jkaN` | NEWS 单塔 | 1.85 | 1.14 | 1.91 | 1.50 | 0.0693 |
| 12 | `MP0Ww6Ek` | PV 单塔 | 1.72 | 1.02 | 2.16 | 1.07 | 0.5979 |

**配额核算**：PV+FUND 恰好 **3 条**（`O0AKLMKq` / `rKRkL9QE` / `0mYoANkv`）⇒ 同时守住
「单两塔组合 ≤3」与「trio×非trio ≤5」两条纪律；
FUND 单塔 2 条 + NEWS 5 条 + SHORTINTEREST 1 条 + PV 单塔 1 条 **均不吃任何组合配额**。

**塔位预测**（提交后）：PV 1→**5** ✓ / FUNDAMENTAL 0→**5** ✓ / NEWS 0→**5** ✓ / SHORTINTEREST 0→1（未过 3 条线）
⇒ **新点亮 3 塔：pv / fundamental / news**。

**全部 12 条的两两相关 < 0.7**（最紧 `rKRQbPPE`↔`j2YNnKOQ` = 0.6964）；
跨族相关近乎为 0（基本面↔NEWS ≤ 0.1718；`akK2vpWW`↔全篮 |r| ≤ 0.2061）。

⚠ **`MP0Ww6Ek` prod 历史 0.7710 ⇒ 提交时必撞**（台账 `pv47_spret` 全族 13/13 prod ≥ 0.7，四杠杆叠加边际已耗尽）
⇒ **现实可提交 = 11 条**。

### §10.4 「20 条」目标的最终答案

| 口径 | 数值 |
|---|---|
| 候选池（台账收割后全闸 + 自检通过） | **24 条** |
| 互相关合法最大组 | 13 条（贪心只给 14 但含低质项；配额约束后取 12） |
| **配额纪律内可提交** | **12 条**（含 prod 必撞的 `MP0Ww6Ek`） |
| **现实可提交（扣 prod 必撞）** | **11 条** |
| objective 目标 | 20 条 ⇒ **差 8–9 条** |

**⇒ 差口的来源（结构性，非投入不足）**：
1. GBR 只有 TOP700 一个 universe、无退路；
2. 可用数据集的**信息轴数**是 5（NEWS）+ 3（fundamental6 capex 簇）+ 3（fundamental17 估值位移簇）+ 1（shortinterest）
   —— 而同族内换字段/换几何**不产生新轴**（§6.9 / §11.14「估值位移族是不可拆的相关块」）；
3. 其余 10 塔已全部判死（§9 表）。

**⇒ 补齐 8–9 条只有三条路**：① 跨区（EUR / IND / DEU 有成熟 runbook）；② 在 GBR 换**全新数据集**
（须先做 S1 体检证明有 ≥3 个语义互异的活字段）；③ 接受 11–12 条收口（点亮 3 塔）。
---

## §11 台账收割第三轮：ANALYST 族 + PV 形态相似度族 —— **3 条新候选全被 self-corr 拦下**

### §11.1 收割范围（GBR 全部本地台账）

| 台账 | 全闸标记数 | 收割结果 |
|---|---:|---|
| `field_profile_fundamental6_gbr_20261030.md` | 1 | ★ **5 条**（§8.1） |
| `template_library_gbr_fundamental_cap_scaled.md` | 24 | ★ **5 条**（§10.1） |
| `template_library_gbr_pv_volume_volatility.md` / `continuation_score.md` | 3 | ★ **1 条**（`MPY96E7o`，本节） |
| `GBR/mining_experience_by_category.md` | 9 | ★ **2 条**（ANALYST，本节） |
| `template_library_gbr_news18.md` | 13 | ✘ V4/V5/P2 与 P1 相关 0.9257–0.9942，无新候选 |
| `template_library_gbr_shortinterest3.md` | 3 | ✘ 无 GBR 全闸候选 |
| `template_library_gbr_insiders1.md` | 2 | ✘ 判死集 |

⇒ **三轮收割共挖出 11 条台账全闸候选，其中 10 条进入候选池（14→24），3 条新挖的被 self-corr 拦下。**

### §11.2 被拦的 3 条（平台 RA 全过，但 self-corr 超线）

| alpha | 机制 | 塔位 | S | F | 2Y | 台账记 prod | **实测 self** | 对手 | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| `rKe5L9q3` | `ts_mean(group_neutralize(广度, sector), 100)` | ANALYST | 1.95 | 1.28 | 1.71 | 0.6737 | **0.9933** | `gJZQZkZe`(OS) | ❌ 近重复 |
| `zqbYwOmV` | 同上，窗 120 | ANALYST | 1.91 | 1.24 | 1.62 | 0.6956 | **0.9411** | `gJZQZkZe`(OS) | ❌ 同骨架换参数 |
| `MPY96E7o` | 形态相似度差（`pattern_scores`）@SUBIND/16/0.06 | PV | 1.70 | 1.24 | 1.94 | — | **0.7622** | `A1G7o1EE`(OS) | ❌ 超线 |

### §11.3 ★★★ 三条必须记住的结论

1. **★ 台账标的「全闸·待授权」≠ 可提交。** 台账的「全闸」只代表**平台 RA 闸全过**（`failed_ra_count = 0`），
   **完全不管 self-corr**，而 self-corr 才是 0.7 的硬红线。
   ⇒ 本轮台账收割出的 3 条新候选 **100% 被 self-corr 拦下**（0.9933 / 0.9411 / 0.7622）。
   ⇒ **台账里记的 prod 数值（多为提交前估算）也不能当红线** —— `rKe5L9q3` 记 prod 0.6737，实际 self 0.9933。
2. **★ self-corr 的判据要分两层**：**0.7 = 提交红线**（超了不可提交，不管指标多好）；
   **0.99 = 「是重跑还是同族变体」的分类阈值**（只用于判断剔的理由，不用于决定是否剔）。
   `zqbYwOmV` 与 `gJZQZkZe` 只差平滑窗 100→120 ⇒ 0.9411，是**同骨架换参数**而非重跑，但一样超线。
3. **★ 本地台账之间会互相矛盾，以平台实测为准**：
   - `GBR/mining_experience_by_category.md` 总表写「PV category ❌ 最高 S 1.01（取反）」，
     而 `template_library_gbr_pv_volume_volatility.md` 写 `MPY96E7o` S **1.70** 全闸 ⇒ **总表结论已过时**；
   - 同总表写「FUNDAMENTAL 仅 fundamental6、1 个机制、未试」，但实际 fundamental17 家族出了 5 条全闸候选；
   - 平台 `registry_empirical` 的 `family_dead_datasets` 把 `fundamental17` / `news17` / `news18` /
     `fundamental6` / `shortinterest3` 全列为死集，而这些集**本轮仍在出货全闸候选**。
   ⇒ **判死标记（台账 `dead` / registry `family_dead_datasets`）一律不得单独作为判死依据。**

### §11.4 GBR 候选池终态

| 阶段 | 数量 |
|---|---:|
| 初始候选池 | 14 |
| + 台账收割第一轮（fundamental6 族） | 19 |
| + 台账收割第二轮（fundamental17 族） | **24** |
| + 台账收割第三轮（ANALYST 2 + PV 1） | 27 → **3 条被 self-corr 拦下** → **24** |

**⇒ 最终 24 条候选 = 12 条可提交组（配额纪律内）+ 12 条备胎。**
---

## §12 ★★★★★ 第四轮收割（本地 DB 的 prod-clean 池）⇒ 最终可提交 **15 条**

### §12.1 ★★★ 决定性检索法：**直接查本地库「prod 已实测 < 0.7 且未提交」的行**

前面三轮都在查**文档台账**（人写的结论）。但 `alphas` 表里有**平台实测的 prod 相关性**字段
（`prod_correlation` + `prod_corr_source` + `corr_checked_at`），这一层从未被系统利用过：

```sql
SELECT alpha_id, region_id, universe, dataset_id, sharpe, fitness, two_year_sharpe,
       sub_universe_sharpe, prod_correlation, self_correlation, turnover, status, expression
FROM alphas
WHERE region_id = 7 AND stage = 'IS'
  AND prod_correlation IS NOT NULL AND prod_correlation < 0.7
  AND (status IS NULL OR status NOT IN ('ACTIVE','SUPERSEDED'))
ORDER BY sharpe DESC;
```

⇒ **GBR（region_id=7 / TOP700）返回 31 条**；全库 180 条。

**⇒ 最重要的一条副产品：我们篮子里那 12 条的 prod 其实本地早已有实测值，且全部 < 0.7：**

| alpha | 本地实测 prod | 此前认知 |
|---|---:|---|
| `O0AKLMKq` | **0.5989** | 「未知」 |
| `vR1aEpa3` | **0.6632** | 「未知」 |
| `j2YNnKOQ` | **0.6700** | 「未知」 |
| `E56onL5r` | **0.6708** | 「未知」 |
| `rKRkL9QE` | **0.6783** | 「未知」 |
| `0mYoANkv` | **0.6932** | 「未知」 |

⇒ **「prod 平台侧不推进」这个 blocker 对这批候选根本不成立** —— prod 早就有数了，只是没人查过这一列。
（`MP0Ww6Ek` 不在这 31 条里，印证其 prod 0.7710 确实超线。）

### §12.2 31 条按 RA 闸初筛 → 13 条 → 平台复核 → 10 条过 self-corr

平台复核（`batch_get_alpha_metrics`）13 条指标与本地库**逐位一致**，`failed_ra_count` 全 0（`mL68wNOK` = 1 剔）。
self-corr 实测（对 OS 池）：

| alpha | self | 对手 | 判定 |
|---|---:|---|---|
| `pwdQb78v` | **0.2442** | `vRNk56mz` | ✅ 余量最大 |
| `MPYlNP8z` | 0.3373 | `WjAV89jG` | ✅ |
| `leAJn9e2` | 0.3650 | `A1G7o1EE` | ✅ |
| `6XKwmQgE` | 0.4148 | `omWVV6Y2` | ✅ |
| `WjOkLGWx` | 0.4955 | `WjAV89jG` | ✅ |
| `9qWwZ3go` | 0.5952 | `omWVV6Y2` | ✅ |
| `P0gvv5gE` | 0.6364 | `9qWaRGEK` | ✅ 偏紧 |
| `d51ddaWX` | 0.6329 | `9qWaRGEK` | ✅ |
| `RR6NOlma` | 0.6348 | `9qWaRGEK` | ✅ |
| `58gMMJEk` | 0.6386 | `9qWaRGEK` | ✅ |
| **`blORMJwm`** | **0.9411** | `gJZQZkZe` | ❌ ANALYST 广度族已被占 |
| **`RR62bMje`** | **0.9980** | `9qWaRGEK` | ❌ 重跑 |

### §12.3 ★ 22 条互相关矩阵：最大互不相关团 = **17 条**

`compute_mutual_correlation(22 条, 0.7, 4Y, 1021)` ⇒ `max_mutually_below_subset_size = 17`，
`max_subset_exact = true`。被排除的 5 条及原因：

| 被排除 | 与谁冲突 | 相关 |
|---|---|---:|
| `j2YNnKOQ` | `MPYlNP8z` | 0.9573 |
| `58gMMJEk` | `P0gvv5gE` | 0.9905 |
| `O0AKLMKq` | `leAJn9e2` | 0.8493 |
| `E56onL5r` | `rKRQbPPE` | 0.7834 |
| `j2YNnKOQ` | `pwdQb78v` | 0.7203 |

### §12.4 ★★★ 配额核算 + 最终 15 条

17 条的塔位（`get_alpha_details` 实读 `pyramids.list[].name`）：

| 塔位 | 候选 | 数量 | 配额影响 |
|---|---|---:|---|
| FUNDAMENTAL 单塔 | `rKRQbPPE` / `MPYlNP8z` / `pwdQb78v` | 3 | 不吃 |
| **PV+FUND 双塔** | `leAJn9e2` / `WjOkLGWx` / `rKRkL9QE` / `0mYoANkv` | **4** | **超「单两塔组合 ≤3」** |
| MODEL 单塔 | `P0gvv5gE` / `9qWwZ3go` | 2 | 不吃（trio 单塔允许） |
| ANALYST 单塔 | `6XKwmQgE` | 1 | 不吃 |
| NEWS 单塔 | `leA6jmoe` / `wpQwjWn6` / `6XdPedNJ` / `9qxPX77V` / `58E7jkaN` | 5 | 不吃 |
| SHORTINTEREST 单塔 | `akK2vpWW` | 1 | 不吃 |
| PV 单塔 | `MP0Ww6Ek` | 1 | 不吃，**prod 0.7710 必撞** |

**⇒ 砍 `0mYoANkv`**（PV+FUND 降到 3 条）：理由是台账 §10.4 已实测它 `risk_neutralized_sharpe` 只剩 **1.02**
（F 只剩 0.51），是全组风险载荷最重的一条，提交优先序明确排末。
**⇒ 再砍 `MP0Ww6Ek`**（prod 0.7710 必撞，pv47 全族 13/13 prod ≥ 0.7）。

### §12.5 ★ 最终可提交组 = **15 条**（全部 RA 全过 / self-corr 全过 / prod 全部有实测值 < 0.7）

| # | alpha | 塔位 | S | F | 2Y | SUB | prod（实测） | self |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | **`rKRQbPPE`** | FUND 单塔 | **2.48** | **2.22** | **2.69** | 1.68 | 0.5086 | 0.490 |
| 2 | `leAJn9e2` | PV+FUND | 1.93 | 1.60 | 2.23 | 1.18 | 0.5507 | 0.365 |
| 3 | `MPYlNP8z` | FUND 单塔 | 2.00 | 1.64 | 1.92 | 1.35 | 0.6191 | 0.337 |
| 4 | `pwdQb78v` | FUND 单塔 | 1.99 | 1.57 | 2.10 | 1.50 | 0.6460 | 0.244 |
| 5 | `WjOkLGWx` | PV+FUND | 1.72 | 1.26 | 2.09 | 0.94 | 0.6577 | 0.496 |
| 6 | `rKRkL9QE` | PV+FUND | 2.21 | 2.05 | 2.51 | 1.77 | 0.6783 | 0.546 |
| 7 | `P0gvv5gE` | MODEL 单塔 | 1.72 | 1.03 | 1.84 | 1.00 | 0.6905 | 0.636 |
| 8 | `9qWwZ3go` | MODEL 单塔 | 1.67 | 1.09 | 2.21 | 0.93 | 0.6890 | 0.595 |
| 9 | `6XKwmQgE` | ANALYST 单塔 | 1.62 | 1.04 | 2.19 | 1.31 | 0.5956 | 0.415 |
| 10 | `leA6jmoe` | NEWS 单塔 | 2.18 | 1.45 | 2.86 | 1.65 | 0.0317 | 0.059 |
| 11 | `wpQwjWn6` | NEWS 单塔 | 2.10 | 1.38 | 2.33 | 1.44 | 0.0466 | 0.052 |
| 12 | `akK2vpWW` | SHORTINTEREST 单塔 | 1.95 | 1.33 | 1.96 | 1.62 | −0.0424 | 0.027 |
| 13 | `6XdPedNJ` | NEWS 单塔 | 1.97 | 1.27 | 2.20 | 1.08 | 0.0824 | 0.085 |
| 14 | `9qxPX77V` | NEWS 单塔 | 1.86 | 1.14 | 2.00 | 1.33 | 0.0715 | 0.065 |
| 15 | `58E7jkaN` | NEWS 单塔 | 1.85 | 1.14 | 1.91 | 1.50 | 0.0136 | 0.069 |

**⇒ 塔位预测**：PV 1→**4** ✓ · FUNDAMENTAL 0→**3** ✓ · NEWS 0→**5** ✓ · MODEL 5→7 · ANALYST 3→4 · SHORTINTEREST 0→1
⇒ **新点亮 3 塔：pv / fundamental / news**。

**⇒ 与 objective 的差距**：15 / 20 ⇒ **只差 5 条**（此前判断为差 9 条）。
剩余 5 条的来源已定位清楚：**本地库里还有 180 条 prod<0.7 的未提交候选分布在其它区**
（EUR 29 条 / USA 30 条 / IND 59 条 / GBR 31 条），
以及 GBR 内被互相关挤掉的备胎（`j2YNnKOQ` / `O0AKLMKq` / `E56onL5r` / `0mYoANkv` / `58gMMJEk`）。
⇒ **跨区收割是补齐 5 条的最短路径，且不需要消耗任何仿真配额**（候选已存在，只需跑 self-corr + 互相关）。
---

## §13 ★★★ 跨区收割（第五轮）⇒ **20 条达成**，objective 第 1 条闭环

### §13.1 方法：把「prod-clean 池」查询扩到全库

§12.1 的 SQL 去掉 `region_id = 7` 后全库返回 **144 条**（全闸 + prod<0.7 + self<0.7 + 未提交）：
`rid 1 (USA) 28 · rid 2 1 · rid 4 3 · rid 5 (IND) 57 · rid 6 (EUR) 20 · rid 7 (GBR) 22 · rid 8 8 · rid 10 5`。

### §13.2 ★ self-corr 的 OS 池是**按区隔离**的（此前未知）

| 区 | pool_size | full_os_pool_size | 含义 |
|---|---:|---:|---|
| GBR | 18–21 | 21 | |
| EUR | 10–13 | 12–15 | |
| IND | 52 | 60 | |

⇒ **跨区候选的 self 门槛天然更松**（EUR 只有 12 条 OS），
且**跨区 alpha 两两相关几乎为 0**（实测 EUR×IND 最大 0.2221，`all_below_threshold = true`）⇒ 跨区提交几乎不产生相关性冲突。

### §13.3 跨区 5 条（逐条平台实读 `checks.fail` 全空 + 塔位确认）

| alpha | 区 | 塔位 | S | F | 2Y | SUB | prod | self |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **`E5VNe67L`** | IND | INSTITUTIONS + PV | **3.20** | **2.52** | **3.00** | 1.64 | 0.6643 | 0.3437 |
| `mL617YPx` | EUR | FUNDAMENTAL + PV | 1.82 | 1.25 | 2.23 | 1.24 | 0.5421 | 0.4504 |
| `omWVZ7lm` | EUR | MODEL 单塔 | 1.75 | 1.17 | 1.76 | 1.63 | 0.5378 | 0.1954 |
| `ZYAJZL93` | EUR | ANALYST 单塔 | 1.67 | 1.04 | 1.81 | 1.12 | 0.6617 | 0.2278 |
| `pwv9eM76` | IND | ANALYST 单塔 | 1.66 | 1.24 | 2.09 | 1.48 | 0.5501 | 0.5017 |

**⇒ GBR 15 + EUR 3 + IND 2 = 20 条 regular alpha，objective 第 1 条达成。**
**⇒ 新点亮塔（提交后）：GBR 的 PV（1→4）/ FUNDAMENTAL（0→3）/ NEWS（0→5）**；EUR 加固 MODEL/FUND/PV/ANALYST，IND 加固 INSTITUTIONS/PV/ANALYST。

### §13.4 ★★★ 两个必须记住的坑

1. **本地 prod-clean 池筛选不完整，必须逐条平台核 `checks.fail`。**
   本地筛选口径只含 sharpe / fitness / 2Y / SUB / prod / self，**漏了 `LOW_ROBUST_UNIVERSE_SHARPE`**。
   实例：`mLjnnzKE`（IND，S 2.90 / F 2.40 / prod 0.5951 / self 0.5322 全部达标）平台实读
   `checks.fail = [LOW_ROBUST_UNIVERSE_SHARPE 0.82 < 1.0]` ⇒ **不可提交**。
2. **★ `LOW_ROBUST_UNIVERSE_SHARPE` 是分区下发的**：
   GBR TOP700 的 `checks.pass` 名单里**从不出现**该 check（平台不下发）；
   EUR TOPCS1600 / IND TOP500 **会下发**。
   ⇒ **跨区候选必须逐条读 `checks.fail`，不能套用 GBR 的闸清单。**

### §13.5 本轮被 self-corr 拦下的「神候选」（证明纪律不可省）

| alpha | 区 | S | self | 对手 | 性质 |
|---|---|---:|---:|---|---|
| `9qxvMzxx` | rid 8 | **4.73** | 0.9695 | `e75pvoNz` | 同骨架近重复 |
| `akKYwj2v` | rid 8 | **4.64** | — | — | 同族（随 `9qxvMzxx` 一并排除） |
| `e75pkq7E` | EUR | 1.87 | **1.0000** | `1YNerr2X` | **纯重跑**（PnL 逐位相同） |
| `RREnAplg` | EUR | 2.00 | 0.9204 | `E56Jea7P` | 同骨架换参数 |
| `vR13Yk9Q` | EUR | 1.92 | 0.9580 | `E56Jea7P` | 同族（analyst7 est 已被占） |
| `blORMJwm` | GBR | 1.91 | 0.9411 | `gJZQZkZe` | 同族（ANALYST 广度族已被占） |
| `RR62bMje` | GBR | 1.67 | 0.9980 | `9qWaRGEK` | **纯重跑** |
| `mLjnnzKE` | IND | 2.90 | 0.5322 | — | ❌ 但挂 **robust 闸**（见 §13.4） |

**⇒ 没有 self-corr，这些里有 5 条（S 4.73 / 4.64 / 2.90 / 2.00 / 1.92）会被误当成高质量候选提交并全部撞墙。**