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

---

## §14 ★★★ C 轴窗口谷判决 + 第 10 席读数（2026-11-02 21:14 实测）

### §14.1 C 轴（`nws17_multiple_comp_event_relevance` 事件强度求和族）prod 三读数

骨架：`ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_sum(nws17_multiple_comp_event_relevance), 60), W), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)`

| 变体 | W | S | F | 2Y | self | **prod（实测）** | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| 基线 `leA6jmoe` | 252 | 2.18 | 1.45 | 2.86 | 0.634* | **0.7077** | 压线不过 |
| **L1 `mLob5Yj5`** | **504** | **2.21** | **1.49** | **2.75** | ~~0.634~~ **0.7975 ✗** | **0.676** | ~~全闸过，可提交~~ **self 超线判死（§14.5）** |
| L2 `ZYQnEpwZ` | 126 | 1.87 | 1.14 | — | 0.606 | **0.6535 ✓** | 全闸过，同腿备援（一腿只提 1 颗，取 L1） |
| 壳变体 `88R7j2Nz`（-ts_zscore） | 252 | — | — | — | — | 0.7212 | 否 |

（*基线 self 读数与 L1 相近；以逐条实读为准。）

**谷向判决 = 拉长（252→504）**：prod 0.7077→0.676 过线，且 S/F/2Y 全部不降反稳（S 2.18→2.21）。**技术结论保留**。

~~⇒ GBR NEWS 塔 3/3 点亮：58E7jkaN + MPYq0819 + mLob5Yj5~~ **★ 2026-11-03 修正：此塔位声明作废（§14.5）。**`MPYq0819` self=1.0000、`mLob5Yj5` self=0.7975、`ZYQnEpwZ` self=0.9983 三杀——**C 轴 `nws17_multiple_comp_event_relevance` 整腿判死**（MPYq0819 孪生体已进 OS 池）。NEWS 塔当前 **1/3**（仅 `58E7jkaN`）。

### §14.2 第 10 席 E3（GLB `d5W0RQZv`）prod = 0.7023

`trade_when(rank(ts_mean(ern3_pre_reptime, 22)) > 0.7, signed_power(subtract(group_rank(single_bucket_5day_return_estimate_ohlcv_img, country), 0.5), 0.5), 0)`
（GLB/MINVOL1M/D1/FAST/decay 10/trunc 0.08/nan OFF/maxTrade OFF）

- prod **0.7023** ≥ 0.70 ⇒ 红线不过；但 **n[0.7,0.8)=1 浅钉（max<0.75）⇒ 按 2026-11-02 纪律不判死**，进归因破墙队列。
- 破墙动作已备：**窗口谷探针 gate 窗 22→5 / 22→60（一长一短定谷向）**，已过 validate_expressions 预检；
  派发连续被 429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED 挡（sim 槽被兄弟会话占满），**待槽释放后派发**。

### §14.3 prod 读数方法备忘（实测耗时）

| alpha | prod | 平台计算耗时 |
|---|---:|---:|
| `d5W0RQZv` | 0.7023 | 414.8s |
| `ZYQnEpwZ` | 0.6535 | 608.0s |

### §14.4 ★ w180 干净档补测（21:25）⇒ 第 10 席就位

| alpha | 区/塔 | S | F | prod | self | checks.fail | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| **`bl6qldJ6`** | GLB/D1/OTHER+SENTIMENT | **2.59** | 1.02 | **0.5421** | **0.277** | **[]** | **第 10 席，全闸过** |
| `omWAZWME` | GLB | 2.13 | 1.07 | 0.7618 | 0.327 | [] | prod 灰区浅钉 n=1 → 破墙队列 |
| `vR1qGlaz` | GLB | 2.60 | 1.25 | 0.7554 | 0.310 | [] | prod 灰区浅钉 n=2 → 破墙队列 |

`bl6qldJ6` 表达式：`trade_when(rank(ts_mean(snt21_2neg_conf_low_394, 22)) > 0.7, signed_power(subtract(group_rank(predicted_third_quantile_one_day_return_4, exchange), 0.5), 0.5), rank(ts_mean(snt21_2neg_conf_low_394, 22)) < 0.6)`
（snt21 情绪门控 + predicted_third_quantile 信号腿，与 E3 的 ern3 门控不同机制面）

~~⇒ 10 regular 清点：篮内 8 + mLob5Yj5 + bl6qldJ6 = 10 条全闸过候选~~ **★ 2026-11-03 修正（§14.5）**：`MPYq0819`（篮内）与 `mLob5Yj5` 双双 self 判死 ⇒ 清点改为 **篮内 6 + `bl6qldJ6` = 7 条 self 干净可提交**，塔修复候选 `wpQwjWn6`/`6XdPedNJ`/`9qxPX77V`（self 全干净）过 prod 后可补至 10。
| `mLob5Yj5` | 0.676 | 581.8s |

⇒ 账号级 prod 槽单并发 + 竞争者滚动占队时，单条读数 400–600s 是常态；轮询预算按 1500s/条设。

### §14.5 ★★★ 2026-11-03 修正：self 复测（OS 池 18→26 后翻转）与 NEWS 塔重判

用户指出「三颗无法点亮，因 MPYq0819 与 mLob5Yj5 的 self 不过」——实测坐实。OS 池扩容后逐条重测（`corr_check.py --types self`，本地 PnL 分区实测）：

| alpha | 塔/腿 | self（新） | 此前读数 | 判定 |
|---|---|---:|---:|---|
| `MPYq0819` | NEWS / C 轴 event_relevance | **1.0000 ✗** | 0.3398 | **判死：孪生体已进 OS 池** |
| `mLob5Yj5` | NEWS / C 轴 W504 | **0.7975 ✗** | 0.634 | 判死（对 OS 中 MPYq0819 孪生体） |
| `ZYQnEpwZ` | NEWS / C 轴 W126 | **0.9983 ✗** | 0.606 | 判死（同上） |
| `wpQwjWn6` | NEWS / nws17_comp_relevance | 0.5614 ✓ | — | 干净，待 prod |
| `6XdPedNJ` | NEWS / nws18_comp_sse | 0.3538 ✓ | — | 干净，待 prod |
| `9qxPX77V` | NEWS / nws17_event_sentiment | 0.5720 ✓ | — | 干净，待 prod |
| `vR1aEpa3`/`O0AKLMKq`/`0mYoANkv`/`P0gvv5gE`/`WjOkLGWx`/`9qWwZ3go` | 篮内 6 条 | 0.4229–0.6364 全 ✓ | — | 干净（`P0gvv5gE` 0.6364 贴线，提交前重测） |
| `bl6qldJ6` | GLB/OTHER+SENT | 0.2775 ✓ | 0.277 | 干净 |

**机理**：mLob5Yj5(0.7975) 与 ZYQnEpwZ(0.9983) 的新 self 值**恰好等于它们此前对 MPYq0819 的互相关**（0.7975 / 0.9983）⇒ OS 池新增的那条就是 MPYq0819 的孪生（MPYq0819 本身仍 UNSUBMITTED）。**整条 C 轴 `nws17_multiple_comp_event_relevance` 腿被占死，三变体全灭，不再做该腿任何窗口变体。**

**NEWS 塔修复路径评估（2026-11-03 00:36 prod 实测，逐条更新）**：

| 候选 | 字段腿 | self | **prod（实测）** | 判定 |
|---|---|---:|---:|---|
| `wpQwjWn6` | nws17_multiple_comp_relevance | 0.5614 ✓ | **1.0 ✗** | **判死（生产池克隆级）** |
| `6XdPedNJ` | nws18_multiple_comp_sse | 0.3538 ✓ | **1.0 ✗** | **判死（生产池克隆级）** |
| `9qxPX77V` | nws17_multiple_comp_event_sentiment_score | 0.5720 ✓ | **0.9399 ✗** | **判死**（00:43 收官） |

（四条两两互相关此前已实测全 <0.7，max `wpQwjWn6`↔`9qxPX77V` 0.6583——但 prod 被杀。）

★ 三条 prod 全灭（1.0 / 1.0 / 0.9399），且彼此互相关 <0.7 ⇒ **生产池里存在该家族多个不同字段变体的克隆**，与 §9「强壳变体 prod≈1.0」一致：**GBR NEWS 的 `ts_target_tvr_decay(vec_count(nws*),…)` 家族已被生产池全面占死，三条全部深度超线（非浅钉，不做破墙）**。C 轴（唯一曾 prod<0.7 的腿）又被 OS 孪生体占死 ⇒ **NEWS 塔修复在 nws17/18 家族内已无活腿，必须换纯新数据集/新机制腿**。NEWS 塔终局 = **1/3**（仅 `58E7jkaN`）。

**教训**：**self 读数只在测量当刻有效**——OS 池是活的（本例 18→26），任何候选在提交动作前必须重测 self，历史 self 列不得直接引用放行。

### §14.6 ★★ 2026-11-03 01:30 第三腿数据集轮换：news38 判死、news20 在途

**塔位口径修正**：本节权威账 = 平台 `recommend_datasets.category_summary` —— NEWS **2/3 差 1**（`58E7jkaN` + `A1VPlR3l` 两颗 nws17 系 ACTIVE，后者 11-02 由兄弟会话提交、即 MPYq0819 的 C 轴孪生体）。§14.5 末「终局 1/3」是发现 `A1VPlR3l` 入池前的旧表述，以 2/3 为准。

**news38（`story_analytics_*` 3 个 VECTOR 字段）两轮 12 模板全灭 ⇒ 数据集判死**：

| 轮 | 模板（节选） | 实测 S | 说明 |
|---|---|---:|---|
| 一 | T1 `vec_count` 注意力 | −0.72 | 负号 = 注意力→高估→反转迹象，但幅度不够 |
| 一 | T3/T4/T5/T7 | −0.33 / 0.00 / 0.24 / −0.46 | 全灭；T7 2Y 0.95 唯一弱迹象 |
| 二 | T2r 比值 / T10 zscore / T11 稀疏 | 0.46 / 0.36 / 0.15 | 最高 0.46，距 S 闸 1.58 差 3 倍 |
| 二 | T6 流量 / T8 衰减 / T9 尾部 / T12 价量 | 无 PnL / −0.12 / −0.05 / −0.37 | 全灭 |

- T2（原始版）死于 event-vector `multiply` 算子禁区，T2r 改比值绕过后仍死。
- **T1inv 不补派**：T1 = −0.72，取反数学上限 +0.72，离闸差一倍，省一个 sim 槽。
- 归因：`story_analytics_*` 三字段是「故事级聚合注意力」，信噪比在 GBR TOP700 日频上不足以单腿过闸（对照 §6.8：NEWS 家族独立轴稀缺）。

**news20（`nws20_*` 46 字段，论坛帖 42659817284375 六机制 × 12 模板）**：
- 上次 MCP `batch_create_simulations` 超时实际只落 **2/12**：W1 `9qx7P09r`（relevance 门控，S 0.03）/ W2 `Jjev0KpE`（新颖度水平，S 0.22），均死且 `nanHandling=OFF`（非战役标准，但距闸太远不重跑）。
- W3–W12 十模板 01:29 经 `batch_simulator.py` 补派（nan ON / decay15 / FAST / trunc0.05，预检 `valid:true` 8 字段全存在），两个批父 `1BBh1Wdv74tfcA5RosVs3MZ` / `xFdJeaiN4Qlc16UhfUvBbg` 在途。
- 判据不变：**10 条全灭则 news20 判死**，NEWS 第三腿再转其他 news 数据集；有达标件（S≥1.58 / F≥1.0 / checks.fail=[]）即进 self+prod 四审争塔腿。

**备胎侦察（01:32，S0 层全扫 + 论坛机制）**：GBR 共 18 个 news 数据集，**coverage>0 仅 6 个**——news17/18（家族判死）、news38（判死）、news20（在途）外，**活备胎只剩 news50（`mws50_*` 37 字段/361 alphas/覆盖 0.69）与 news104（11 字段/388 alphas/覆盖 0.97）**，其余 12 个覆盖为 0 直接出局。

- **news50 字段结构 = news20 同族**（ssc/ens/ghc_lna/relevance/rp_story_event_* 全同名前缀换 mws50_），但多两套独有族：**新颖度家族**（`ens_elapsed` 时间链、`ens_similarity_gap` 相似故事间隔、`g_ens*` 全球级）与**分类器族**（`qcm/qep/qmb/vea`、`nip` 新闻影响预测 2h）。
- **论坛机制源（启用前侦察已补）**：`Data Idea系列3：Global News Data_news48`（16 赞，WL13229）逐字段分析的正是同一数据包，4 个特征工程方案可迁移：① overall_news_sentiment=9 情绪场均值 ② sentiment_novelty_ratio=(ssc+ess)/(ens+g_ens) ③ action_earnings_sentiment_diff=(acb+bam)−(bee+ber) ④ relative_event_novelty=ens/…（新颖度相对化）。字段级 alphaCount 仅 3–65，拥挤度低。
- 若 news20 判死：news50 模板池 = 论坛 4 方案 + W1–W12 移植（前缀替换）+ ens_similarity_gap/nip/qcm-qep-qmb 离散度等新骨架，凑满 10 互异模板再派发。

**news50 十模板池（01:37 设计 + 预检 `valid:true`，15 字段全存在；草案存 `results/_n50_pool_draft.json`，news20 收批后按结果微调再派发）**：

| # | 骨架 | 来源 | 常数取值理由 |
|---|---|---|---|
| N1 | 5 情绪分类器均值（ssc/ess/qcm/qep/qmb）→ ts_mean60 → group_rank(industry) | 论坛 news48 方案1（9→5 精简） | 5=分类器数；60=季窗 |
| N2 | 情绪/新颖度比 (ssc+ess)/(ens+g_ens+1) → ts_mean22 | 论坛方案2 | +1 防零；22=月窗 |
| N3 | 行动−盈利情绪差 (acb+bam)−(bee+ber) → ts_mean60 | 论坛方案3 | 主题分裂价差 |
| N4 | 相对新颖度 ens/(g_ens+1) → ts_mean22 | 论坛方案4 | 实体独家度 vs 全网 |
| N5 | `nip` 新闻影响预测（2h）水平 → ts_mean5 | 自建 | 5=日窗，抓影响预测快变量 |
| N6 | 陈旧度反转 −rank(ens_similarity_gap/100 → ts_mean22) | 自建 | /100 归一 0–100 刻度；反转方向先验 |
| N7 | 社论−市场情绪差 (qmb−qep) → ts_mean60 | 自建 | 知情评论 vs 背景新闻分裂 |
| N8 | 积极事件占比动量 ts_delta(ts_mean(aes,22),22) | 自建 | 一阶差分=事件态势变化 |
| N9 | nip>50 门控 × 情绪快线 ssc ts_mean5 | 自建 | 50=0–100 刻度中点=有实质影响才交易 |
| N10 | ens_elapsed<86,400,000ms（24h 链内）门控 × 情绪变化 ts_delta5 | 自建 | 8640 万 ms=ens 的 24h 窗本体 |

- 结构互异轴：多分类器均值 / 比值 / 主题价差 / 相对化 / 影响预测水平 / 陈旧度反转 / 评论-新闻价差 / 事件占比一阶差分 / 影响确认门控 / 事件链时效门控（几何、矩、门控轴均不同，非换窗变体）。
- 全部避开 event-vector `multiply` 禁区与裸 `rank(sentiment)` 禁令（均为 ts 平滑 + group_rank 几何）；时间窗 5/22/60 全在白名单。

### §14.8 ★★ 2026-11-03 01:45 news20 判死（12/12 全灭）⇒ news50 开火

**news20（nws20_*）全 12 模板实测**（W1–W12，nan ON，01:29–01:44 两批收齐）：

| 模板 | 骨架 | alpha | S |
|---|---|---|---:|
| W5 | 注意力稀释 ssc/故事数 | Vkx3E9n8 | **0.59**（最高） |
| W8 | 慢平滑情绪（252） | ZYQKx5qQ | 0.57 |
| W7 | 次日确认门控 | 9qx7KvbV | 0.35 |
| W4 | ghc_lna 情绪动量 | xArdQ6aJ | 0.31 |
| W2 | 新颖度水平 | Jjev0KpE | 0.22 |
| W3 | 新颖度门控 | zq3RjMzG | 0.18 |
| W11 | 偏离尾部壳 | qML6dLZO | 0.11 |
| W6 | 实体-故事偏离 | E56eb7YK | 0.09 |
| W9 | 新颖度差分 | O0AxkAv1 | 0.04 |
| W1 | relevance 门控 | 9qx7P09r | 0.03 |
| **W10** | **vec_count 故事广度** | WjOVdOmd | **−0.22** |
| W12 | 情绪离散 | bl6dMaQr | −0.53 |

- **判死**：两数据集（news38 12 模板 + news20 12 模板）同形态——原始情绪/新颖度水平族只有 S≈0.1–0.6 量级，距闸 1.58 差 3 倍。
- **注意力密度路线在 news 族整体封死**：news38 T1 `vec_count(metric_value)` = −0.72、news20 W10 `vec_count(rp_story_event_index)` = −0.22，两处同向为负 ⇒ 注意力反转方向（T1inv/W10inv）数学上限仅 +0.72/+0.22，都够不到闸。两颗 ACTIVE 塔腿（nws17 `event_relevance` 求和族）的高 S 不可复制到其他 news 字段族。
- **转产**：news50（N1–N10）已于 01:45 派发（`bg_e7c6c4c9`，批任务落 `results/_n50_status.csv`），差异化希望押在**未测过的机制面**：`nip` 影响预测（N5/N9）、新颖度交互比值（N2/N4）、陈旧度反转（N6）、事件占比动量（N8）。

### §14.9 ★★★ 2026-11-03 01:48 news104 侦察 + 十模板池预检就绪（最后备胎）

**news104（`nws104_*` 11 字段，覆盖 0.97，字段级 alphaCount 仅 10–21）= 全场最锐利的机制面**：
- **`marketimpactscore`**：数据自带「风险调整后 1 分钟前瞻收益」预测值——唯一一个**直接表达预期收益**的 news 字段；
- **`prob_pos/prob_neg/prob_ntr`** 完整情绪概率分布（比三元 `sentiment` 锐利）+ **`confidence`** 情绪置信度；
- **数据质量轴**：`automessage` 机器人消息 / `headlineonly` 浅信息 / `novelty` 新旧故事 / `relevance` 公司聚焦度。
- 论坛无 news104 专属模板帖（`search_forum_posts` 只返回 news54/news48 通用帖），骨架以文献机制 + 自建为主。

**A1–A10 模板池（01:48 预检 `valid:true` 9 字段全存在，草案 `results/_n104_pool_draft.json`）**：A1 影响预测水平 / A2 影响预测修正（PEAD 漂移先验）/ A3 概率分布情绪差 / A4 置信度×情绪（衰减校正，文献先验）/ A5 新颖度反转 / A6 机器人消息门控×影响预测 / A7 中性概率水平（不确定性溢价先验）/ A8 高置信门控×分布情绪快线 / A9 影响×聚焦度（归因加权）/ A10 情绪意外（ts_zscore，surprise≠level 文献先验）。常数：5/22/60 窗在白名单；0.7=置信分类惯例阈值；0.5=automessage 标记占比中点。
- **开火顺序**：news50 收批后若灭 → 立即派 A1–A10；若 news50 活 → news104 仍值得派（为 10 regular 目标补充候选量，机制面与 news50 正交）。

### §14.10 ★★★★★ 2026-11-03 01:52 塔位计数机制实锤：双数据集 alpha 同时点亮两个塔

平台 `get_alpha_details` 实读两个样本：

| alpha | 引用数据集 | `pyramids.effective` | 塔节点 |
|---|---|---:|---|
| `bl6qldJ6` | snt21 + 预测分位（双） | **2** | `GLB/D1/OTHER` + `GLB/D1/SENTIMENT` |
| `rKRkL9QE` | fnd6 + `cap`（本战役已提交） | **2** | `GBR/D1/PV` + `GBR/D1/FUNDAMENTAL` |

**结论**：alpha 的塔归属 = 表达式引用到的**全部 category**（逐个挂节点、各带 multiplier），与权威账吻合（rKRkL9QE 正是 PV 2/3 与 FUND 2/3 各计一票）。

**⇒ NEWS 塔备用路线（若 news50/104 单数据集全灭）**：构建「**news 字段作门控 + 强信号腿**」的双数据集 alpha——news 侧不需要 S≥1.58，只需进表达式挂上 NEWS 节点；S 由强腿扛。例形状：`trade_when(greater(ts_mean(vec_avg(nws104_confidence),22),0.5), <已验证强信号族>, 0)`。

**设计红线**：① 强腿族不得与提交簿/待篮同族（否则 self 撞死）；② 只用 gate 形态不用 `add(A,B)` 混信号；③ 塔混配额：NEWS×FUND/ANALYST 等非 trio 组合各 ≤3，NEWS×PV/OTHER/MODEL 计 trio×非trio ≤5；④ 提交后必须回读 `category_summary` 验证 NEWS 计数真的 +1（计数归属是推定，pyramid 双节点是实锤）。**该路线产物非 ATOM**（双数据集），10 regular 计数可入但优先级低于单数据集件。

**★ 2026-11-03 02:05 用户指示：该路线搁置**——「先不考虑门控 / 先不考虑用门控点 NEWS 塔」。NEWS 塔第三腿**只走单数据集 news 路线**（news50 → news104 → 继续轮换），门控挂塔不启用。§14.10 的塔位计数机制结论仍然有效（rKRkL9QE PV+FUND 双挂是实锤），仅「用门控挂 NEWS 塔」的应暂不执行。

### §14.11 ★★★★ 2026-11-03 02:05 news50 判死（10/10 全灭）+ news104 波在途

**news50 收批终表**（N10 补齐，全 10 条 COMPLETE）：

| tag | alpha_id | S | 机制 |
|---|---|---:|---|
| N9 | `0mYMQEXr` | **0.74** | nip>50 门控 × ssc 情绪快线（全场三波最高） |
| N1 | `2rANZLd6` | 0.58 | 分类器合成密度(qcm/qep/qmb/ssc/ess) |
| N10 | `GrWe8xaP` | 0.45 | ens_elapsed<24h 新鲜度门控 × ssc 变化 |
| N3 | `88Re6Qq7` | 0.02 | acb+bam−bee−ber 多空差 |
| N7 | `bl6dPqRm` | 0.08 | qmb−qep 分类器分歧 |
| N2 | `d5WR70w2` | −0.34 | (ssc+ess)/(ens+g_ens+1) 相对强度 |
| N4 | `78LnXbKb` | −0.43 | ens/(g_ens+1) ensemble 一致性 |
| N8 | `1YNzmdXm` | −0.21 | aes 情绪变化 |
| N5 | `vR1vzMJv` | −0.49 | nip 影响预测水平 |
| N6 | `gJe9POo0` | −0.93 | 相似度缺口反转 |

**判死依据**：10 个结构互异模板（论坛迁移 4 机制 + ens 新颖度族 + 分类器族 + 影响预测族）全灭，max S 0.74 距闸 1.58 差 0.84；与 news38（12 模板）、news20（12 模板）合计 **34 模板全灭**。N9 确认「nip 影响预测字段信息在条件侧」（作信号 −0.49，作门控抬到 0.74）——但门控路线已搁置，该洞察留档备用。

**news50→news104 轮换**：A1–A10（`results/_n104_pool_draft.json`）已派发（batch bg_2fb7e02a），机制与 news20/50 正交（impact 预测水平/修正、prob_pos−neg 概率差、置信加权、不确定性溢价、impact×relevance 交互），字段级 alphaCount 仅 10–21。判据同前：达标件（S≥1.58/F≥1.0/checks.fail=[]）进 self+prod 四审争塔腿。

### §14.12 ★★★★ 2026-11-03 02:05 news17 备胎侦察（news104 全灭时的第二波战场）

**两颗 ACTIVE 塔腿的精确表达式**（自遮蔽面 = 这两个机制不可再碰，self 必撞）：

| alpha | 表达式 | S/F/TO |
|---|---|---|
| `A1VPlR3l` | `ts_target_tvr_decay(-ts_rank(ts_mean(vec_sum(nws17_multiple_comp_event_relevance),60),120), target_tvr=0.05, lambda_max=5, lambda_min=0)` | 1.88/1.15/0.079 |
| `58E7jkaN` | `ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws17_multiple_comp_ssc), rank(vec_avg(nws17_multiple_comp_event_similarity_days))),60),252), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)` | — |

**★ 注**：58E7jkaN 用了 `vec_count(ssc)` 注意力密度×相似度交互——vec_count 族在 news38/news20 全灭，但在 news17 是出货机制。**「某机制族全灭」只在同一数据集内成立，跨数据集不迁移**（与 §14.x「子族粒度」判据同源）。

**news17 字段库存**（get_datafields 实读 48 字段，平台 alphaCount 极低=未拥挤）：

- **已占用（禁碰）**：`multiple_comp_event_relevance`（A1VPlR3l）、`multiple_comp_ssc`×`multiple_comp_event_similarity_days`（58E7jkaN）
- **低拥挤候选（alphaCount≤7）**：`multiple_comp_bam`(4)、`multiple_comp_ber`(3)、`multiple_comp_qcm`(3)、`multiple_comp_qmb`(4)、`multiple_comp_headline`(3)、`multiple_comp_rp_story_event_index`(0)、`multiple_comp_event_end_time_utc`(0)、`ghc_lna`(7)、`qmb`(7)、`timestamp_utc_time`(7)、`bam`(6)、`qcm`(6)
- **中拥挤**：`event_similarity_days`(23)、`nip`(30)、`event_sentiment_score`(34)、`ssc`(25)、`relevance`(22)

**设计方向（若 news104 全灭再启用）**：① 只用低拥挤字段组机制，避开两条 ACTIVE 腿的字段×几何组合；② 几何可借鉴两腿已验证的外层 `ts_rank(·,60/120/252)` + 内层 `vec_sum`/`vec_count`×交互，但换字段族（如 bam−ber 多空差求和、qcm/qmb 分类器、rp_story_event_index 稀疏索引）；③ 必须过 self 0.7 对 OS 池（含两腿）；④ 波次模板池 ≥10 互异 + 论坛/论文来源标注后才派发。

### §14.13 ★★★★ 2026-11-03 02:15 news104 判死（10/10 全灭）+ news17 波 M1–M10 在途

**news104 收批终表**（全 10 条 COMPLETE，S 区间 −0.42 ~ 0.28）：

| tag | alpha_id | S | 机制 |
|---|---|---:|---|
| A3_prob_spread | `3qoenRMP` | **0.28** | prob_pos−prob_neg 概率差 |
| A6_auto_gate_impact | `3qoenR06` | **0.28** | automessage 门控 × impact |
| A10_sent_surprise | `1YNznjp6` | 0.24* | （0.24/−0.04 区间内） |
| A4_conf_weighted | `qML6mlLE` | 0.24 | 情绪×置信加权 |
| A9_impact_relevance | `zq3RP6Xo` | 0.25 | impact×relevance |
| A1_impact_level | `9qx7Arz9` | 0.19 | impact 水平 |
| A5_novelty_reversal | `9qx7Arxe` | 0.21 | 新颖度反转 |
| A8_hi_conf_spread | `YP1g2KZR` | 0.16 | 高置信门控 × 概率差 |
| A2_impact_revision | `RRE1k8Jb` | −0.05 | impact 修正 |
| A7_uncertainty | `QPv92keK` | −0.42 | 不确定性溢价 |

**判死依据**：impact 预测机制（news104 数据自带「风险调整后 1 分钟前瞻收益」预测）**作信号、作门控双失败**——news50 N9 的「条件侧信息」洞察未能跨数据集迁移（gate×impact 仅 0.28，比 N9 的 0.74 差一个量级）。news 族累计 **44 模板全灭**（news38 12 + news20 12 + news50 10 + news104 10）。

**⇒ 新结论：news 数据集在 GBR 的信号只在 news17 子族出现过**（两颗 ACTIVE 塔腿均为 nws17 字段）。其余集的「情绪水平/动量/新颖度/影响预测」机制全灭。

### §14.14 ★★★★ 2026-11-03 02:15 news17 波 M1–M10 模板池（paper+forum+自建，0 门控）

**模板池**（全单数据集 ATOM，0 个 trade_when，预检 10/10 valid + 字段全存在；表达式见 `results/_n17_pool_draft.json`，派发批 bg_26a2a6f4）：

| # | 机制 | 结构 | 来源 |
|---|---|---|---|
| M1 | 情绪动量·子行业 | fast 5日均 × subindustry | **paper《The Momentum of News》**（Wang/Zhang/Zhu 2018，forum 18641983716503，实证年化 7.45%） |
| M2 | 慢几何情绪求和 | vec_sum × ts_rank(·,252) | paper + 两腿慢几何 |
| M3 | bam−ber 多空对比 | 对比差 × 慢秩 | forum《Data Idea 系列3 news48》多空方案迁移 |
| M4 | qcm−qmb 分类器分歧 | 分类器差 × industry | forum news48 |
| M5 | 稀疏索引首动者 | rp_story_event_index（alphaCount=0）| 自建 |
| M6 | 新闻强度变化反转 | ts_delta 变化矩 | 自建 |
| M7 | 事件新颖度水平 | similarity_days × 慢秩 | 自建 |
| M8 | relevance 加权情绪 | 比值加权 × 慢秩 | forum《relevance 加权+新颖度过滤》 |
| M9 | 多公司头条密度 | vec_count × 慢秩 | 自建（58E7jkaN 密度思想换字段族） |
| M10 | 时戳新鲜度 | event_end_time 水平 × industry | 自建 |

**设计红线执行**：避开两 ACTIVE 腿字段×几何（`multiple_comp_event_relevance` 求和、`ssc密度×similarity` 交互）；全用低拥挤字段（alphaCount 0–16）；窗口全白名单（5/22/60/252）；无 bucket 轴；无裸 rank(sentiment)（M1 带 5 日均+子行业中性）。

**判据**：达标件（S≥1.58/F≥1.0/checks.fail=[]）进 self+prod 四审争塔腿；若 10 全灭则 news17 第二波换几何（极值选择 if_else / 窗口谷）再试，之后判 news 域整体封盘、回报用户裁定。

### §14.15 ★★★★ 2026-11-03 02:30 news17 波 1 终局（10/10 原向全灭，两颗取反火种）+ 波 2 在途

**波 1 终表**（M1–M10 全 COMPLETE）：

| 模板 | alpha_id | S | 备注 |
|---|---|---:|---|
| M9 头条密度 | `N1NRnzkg` | **−1.79** | ★取反 **+1.79/F 1.08 双过闸线**——54 模板首个取反双过线机制 |
| M2 慢几何情绪求和 | `mLoVqbw9` | −1.32 | ★取反 +1.32（与 A1VPlR3l 同构形状） |
| M5 稀疏索引 | `rKRPblkE` | 0.43 | 最高正向，弱 |
| M4 分类器分歧 | `akKENn39` | 0.35 | 弱 |
| M3 多空对比 | `1YNzodkJ` | 0.25 | 弱 |
| M7 新颖度 | `RRE1NzXo` | 0.16 | 弱 |
| M8 relevance 加权 | `88ReOJgo` | 0.14 | 弱 |
| M1 paper 情绪动量 | `MPYLbQPz` | −0.16 | 论文机制 GBR 反向 |
| M10 时戳新鲜度 | `QPv9nRaw` | −0.41 | 死 |
| M6 强度变化反转 | `MPYLbQwa` | −0.04 | 死 |

**核心发现**：news17 的信号方向 = **慢新闻聚合的反向（contrarian）**——A1VPlR3l 出货形状本身是取反（relevance-sum），M2/M9 原向均为深负、取反即过线。波 2 十二模板（`results/_n17b_pool_draft.json`，已预检 12/12 valid，批 bg_2a2f19ca 在途）全部围绕「取反 + 强壳 + 窗口谷」展开：W1–W4 = M2 翻转 × 裸/强壳 × 外窗 66/120/252；W5–W8 = 裸族/变化矩/对比差/非线性尾部；W9/W10 = M5/M4 装强壳；**W11/W12 = M9 翻转裸/强壳（头号种子，上限 +1.79）**。

**⚠ 四审预警**：W11/W12 的 `vec_count(nws17_multiple_comp_headline)` 撞 58E7jkaN 生产池克隆族（nws17/18 vec_count 家族 prod 1.0/1.0/0.9399 实测），**prod 大概率死、只当 S 确认器**；W2–W4 的 sentiment-sum 族需实测 self 对 A1VPlR3l（relevance-sum 同构）。真正可提交的塔腿最可能出自「取反机制 × 非克隆字段族」的组合。

### §14.16 ★★★★★ 2026-11-03 02:44 news17 波 2 终盘：contrarian 论题实锤，3 颗候选四审 3/4 全过

**波 2 终表**（12/12 COMPLETE）——**M2/M9 取反系列全部兑现理论值**：

| alpha | 模板 | S | F | 2Y | sub | fRA | self | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `LLMdk8ne` | **W12 = M9 翻转+强壳** | **2.10** | **1.38** | 2.33 | 1.44 | **0** | 0.56 | ★ prod 待测（塔腿头号） |
| `akKEoRA5` | W11 = M9 翻转裸 | 1.79 | 1.08 | 2.03 | 1.49 | **0** | 0.46 | ★ prod 待测 |
| `rKRPAWv9` | W2 = M2 翻转+强壳 252 | 1.76 | 1.07 | 1.89 | 1.40 | **0** | 0.40 | ★ prod 测量中 |
| `P0oOv1dL` | W3 = M2 翻转+强壳 120 | 1.65 | 0.96 | 1.74 | 1.41 | 1 | 0.46 | ✗ F 差 0.04 + fRA 1 |
| `3qoezgmz` | W4 = M2 翻转+强壳 66 | 1.49 | 0.84 | 1.54 | 1.16 | 3 | 0.43 | ✗ fRA 3 |
| `O0Axoo37` | W8 = 非线性尾部 | 1.17 | 0.58 | — | — | — | — | ✗ |
| `LLMdkRA9` | W1 = M2 翻转裸 | 1.32 | 0.68 | 1.56 | 1.34 | 3 | 0.34 | ✗ fRA 3 |
| `vR1vddQA` | W9 = M5 装强壳 | 0.32 | 0.08 | — | — | — | — | ✗ |
| `58EkMGaz` | W10 = 分类器差强壳 | 0.12 | 0.02 | — | — | — | — | ✗ |
| `e75xLeM6` | W6 = 变化矩翻转 | −0.56 | −0.15 | — | — | — | — | ✗ |
| `P0oOvjL7` | W5 = 裸族翻转（W5 之前单独跑的） | 1.30* | 0.74* | — | — | — | — | ✗ |
| `78LnJJpQ` | W7 = 温度计−关注差 | −1.91 | −1.18 | — | — | — | — | ✗（取反 +1.91 未测，候选库存） |

**三条实证规律**：
1. **窗口谷（M2 族）**：外窗 252→120→66 = S 1.76→1.65→1.49，252 最优；壳增益 ≈ +0.44（1.32→1.76）。
2. **M9 头条密度翻转是全库最强 news 机制**：裸 1.79 → 强壳 **2.10**（M9 原向 −1.79 精确翻转验证）。
3. **★ 克隆族预判修正**：`vec_count(multiple_comp_headline)` 对塔腿 58E7jkaN（`vec_count(multiple_comp_ssc)×similarity`）的 self 仅 0.46/0.56——**头条密度 ≠ 故事情绪密度，属不同 PnL 家族**；历史 prod 1.0/1.0/0.9399 的是 sse/ssc 近邻变体。判「vec_count 家族克隆」必须落到字段对，不能按算子一刀切。

**待办**：prod 三连测（账号单并发排队：rKRPAWv9 → LLMdk8ne → akKEoRA5）；全过 0.7 红线者进提交待报用户授权；W7 取反（+1.91 理论）留作下波库存。

### §14.17 ★★★★★ 2026-11-03 02:49 W7-neg 双探针新纪录 + self 判死线首次收割 + prod 排队

**W7-neg 实测**（理论 +1.91 双双精确兑现）：`mLoVXokK`（+强壳）S **2.30/F 1.58/2Y 2.50/sub 1.59/fRA 0** = 强度之王，但 **self 0.735 超 0.7 红线判死**（撞 OS 池——对比差含 relevance-sum，与 A1VPlR3l 取反族近亲）；`kqNZKN5K`（裸）S 1.91/F 1.18/2Y 1.99/sub 1.51/fRA 0/**self 0.62 过线** = 活件。

**当前 prod 待决四活件**（全部五闸+RA+self 已过）：`kqNZKN5K`(1.91) / `LLMdk8ne`(2.10) / `akKEoRA5`(1.79) / `rKRPAWv9`(1.76)。rKRPAWv9 prod 首刷 45 轮超时（平台未落缓存），串行刷新链已发（kqNZKN5K→LLMdk8ne→akKEoRA5→rKRPAWv9）。

**★ 教训**：壳会放大与 OS 池的 PnL 相关性——同信号裸版 self 0.62、壳版 0.735。**self 临界件先测裸版**，壳版只在裸版 self 有余量时上。

### §14.18 ★★★★★ 2026-11-03 03:05 11 颗互相关最大团：篮子精确 = 10 席闭合，唯一裁位 akKEoRA5

**实测**（`compute_mutual_correlation`，11 颗 = 4 活件 + 待篮 7 条，threshold 0.7 / 4Y / 1023 点，本地 PnL 免费）：

| 关键读数 | 值 | 含义 |
|---|---:|---|
| 唯一超线对 | **LLMdk8ne ↔ akKEoRA5 = 0.8902** | 同字段同窗（headline 密度 60/252）裸/壳对 = 同一腿 |
| 次高对 | kqNZKN5K ↔ akKEoRA5 0.6757 / kqNZKN5K ↔ LLMdk8ne 0.5909 | 均 <0.7 过线 |
| 壳变体对 | LLMdk8ne ↔ rKRPAWv9 = **0.2896** | headline vs 情绪求和 = 异字段，强壳下仍互异 |
| 待篮内部最高 | vR1aEpa3 ↔ O0AKLMKq 0.6566 | 全 <0.7 |
| news 四件 ↔ 待篮 7 条 | 全 ≤ 0.12 | 两篮完全正交 |

**判决（一腿一票）**：`max_mutually_below_subset`（精确解）= **10 席** = LLMdk8ne + kqNZKN5K + rKRPAWv9 + 待篮 7 条（vR1aEpa3 / O0AKLMKq / 0mYoANkv / P0gvv5gE / WjOkLGWx / 9qWwZ3go / bl6qldJ6）。**裁掉 akKEoRA5**（同腿留强：LLMdk8ne S 2.10 > 1.79；akKEoRA5 转为 LLMdk8ne 的 prod 失败备胎）。

⇒ **「10 个 regular」目标的篮子形状就此闭合**：若 10 席全过提交前终验（prod<0.7 + self 重测 + fRA=0），即达标；NEWS 塔第 3 腿由 LLMdk8ne（或任一 news17 活件）点亮 3/3。

**prod 现况（03:05）**：串行链 bg_70e7ab4d 进行中——kqNZKN5K 45 轮耗尽 unknown（首刷超时、平台未落缓存，与 rKRPAWv9 同款），LLMdk8ne 在算（8/45），链尾 akKEoRA5 + rKRPAWv9。**耗尽者待 inflight 标记 300s 过期后补刷**；prod 是终验项，缺它不改篮子形状。

**★ 教训**：裸/壳对（同字段同窗）互相关 0.89——**强壳不产生新腿**，只换形态；同机制想进篮必须换字段（LLMdk8ne↔rKRPAWv9 换字段后 0.29）。

### §14.19 ★★★★★ 2026-11-03 03:10 prod peek 四读数破局：LLMdk8ne 族 prod 判死，篮子收缩为 9 席

**工具路径**：`tools/prod_wait.py <id> --peek --tries 2`（§四2 第②段，无锁只读）在刷新链轮询全 unknown 的僵局下直接读回平台已算值——corr_check 的 45 轮轮询窗口（450s）盖不住平台首算，但值其实在平台上，peek 一次就到。

| 候选 | 族 | prod | 判定 |
|---|---|---:|---|
| `LLMdk8ne` | 头条密度 contrarian（壳） | **1.0** | ✗ 深钉判死（≥0.8；生产池家族克隆） |
| `akKEoRA5` | 同族（裸） | **0.8901** | ✗ 同族连坐（与 LLMdk8ne 互相关 0.89 实证同腿） |
| `kqNZKN5K` | 温度计−关注对比差（裸） | **0.6227** | ★ 过线（<0.7 严格） |
| `rKRPAWv9` | 情绪求和 contrarian（壳） | **0.3998** | ★ 过线（极干净） |

**实证规律**：①「self 干净 ≠ prod 干净」——LLMdk8ne self 0.56 / prod 1.0，头条密度 contrarian 在**全账号生产池**里有克隆（58E7jkaN 的 ssc 族不是它，克隆来自外部提交者）；②**prod 判死半径 = 家族**——headline 族两颗全灭，逃无可逃；③peek 的 value 语义与放行线一致（<0.7 严格）。

**篮子现状 = 9 席**（kqNZKN5K + rKRPAWv9 + 待篮 7 条，互相关全 <0.7，kqNZKN5K↔rKRPAWv9 = 0.35）；NEWS 塔 3/3 由任一 news17 活件点亮。**缺第 10 席** ⇒ news17 未触碰字段补席波（§14.20）。

### §14.20 ★★★★ 2026-11-03 03:25 补席波 B1–B10 派发（news17 未触碰机制，10 互异模板）

**目标**：篮子 9 席 → 补第 10 席。**纪律**：0 门控、单数据集 news17、窗口白名单、论坛先行（`search_forum_posts` 检出 RM49262「ts_covariance 情绪模板」与「新闻四维度」帖；web_search 402 仍停，论文先验取自分析师修正漂移 / 投资者注意力文献常识）。

**字段语义**（get_datafields 实读）：`ber`=分析师升降级分（ANL-CHG，−1/0/1）、`bam`=公司行动情绪（BCA）、`acb`=盈利情绪、`ghc_lna`=多分类器综合语气、`rp_story_event_count`=每稿事件数（新闻广度）、`qep`=词典情绪、`qmb`=M&A 情绪。**全部未测机制**（news50 的 nip 判死不迁移到 news17，S 判死半径=单数据集）。

| # | 模板 | 结构轴 | 来源 | 方向 |
|---|---|---|---|---|
| B1 | `ts_rank(ts_mean(vec_sum(nws17_ber),60),252)` | 分析师修正漂移（动量对照） | paper | +动量 |
| B2 | B1 取反 + 全强壳 | 出货公式移植 | 自建 | contrarian |
| B3 | `-ts_rank(ts_mean(vec_sum(nws17_bam),60),252)` | 公司行动情绪裸矩 | 自建 | contrarian |
| B4 | `-ts_rank(ts_delta(ts_mean(vec_sum(nws17_acb),22),22),252)` | 一阶变化矩 | 自建 | contrarian |
| B5 | `ghc_lna` 取反 + 全强壳 | 综合语气 + 出货公式 | 自建 | contrarian |
| B6 | `-ts_rank(ts_delta(ts_mean(vec_sum(nws17_rp_story_event_count),5),22),252)` | 新闻流量加速度（注意力） | paper | contrarian |
| B7 | `-ts_rank(ts_mean(multiply(vec_sum(nws17_qep), rank(vec_avg(nws17_event_similarity_days))),60),252)` | 情绪×新颖度交互 | 自建 | contrarian |
| B8 | `ts_corr(ts_mean(vec_sum(nws17_qep),22), ts_mean(vec_count(nws17_qep),22), 60)` | 语气-覆盖对齐（corr 几何） | forum RM49262 | 自然 |
| B9 | `-ts_rank(ts_mean(vec_avg(nws17_qmb),60),252)` | per-story 归一矩（vec_avg） | 自建 | contrarian |
| B10 | `-group_rank(signed_power(ts_mean(vec_sum(nws17_ghc_lna),60),3), industry)` | 非线性尾部 × 分组轴 | 自建 | contrarian |

**预检**：validate_expressions `valid:true`，8 字段全存在（qep 分页告警已由 get_datafields 实证豁免）。**派发**：`results/_n17c_list.json` → batch_simulator 批 3 并发 2，任务 `bg_f92225f6`，收批 `results/_n17c_status.csv`。

**归因预案**：按模板编号归因；出线者先过四审（五闸+fRA+self），再跑互相关（对 9 席篮子 + 同波彼此）解最大团补位。B5/B10 同字段异几何预期互高，只留一；B1 为方向对照，深负则其取反版即 B2 族。

### §14.21 ★★★★★ 2026-11-03 03:39 直方图归因判决 + pwdQb78v 破墙波 R1–R12（10 席救援线）

**背景**：第 10 席锁定 `pwdQb78v` 破墙救援（NI/EV 收益率趋势，S 1.99/F 1.57/2Y 2.10，prod 0.7205 浅钉）。prod_wait.py peek 已扩展为存直方图（`records` 分箱 [low,high,n]；平台 prod 端点**不含对手 ID**，直方图即 11-02 判据的「钉数与深度」）。

**直方图归因（03:39 实测）**：

| 候选 | [0.7,0.8) | [0.6,0.7) | [0.5,0.6) | 形态 | 判决 |
|---|---|---|---|---|---|
| `pwdQb78v` | **n=1**（0.7205） | 4 | 11 | 主体集中 [-0.1,0.3]，稀疏尾 | **浅钉单点碰撞 → 救援主目标** |
| `E56onL5r` | n=1（0.7033） | **43** | **638** | [0.3,0.7] 厚尾 1.1 万颗 | **主题拥挤（Rev/EV 生产池成片）→ 降级二备** |

**修正**：`rKRkL9QE` 当日 prod **0.6783 ✓ 过线**（10-31 读数仍有效）——它死在 self（OS 池孪生翻死），此前「prod 漂死」认定有误。

**方法论调和（skill vs 11-02 规则）**：`wq-window-valley-break-prod-wall` 实证（KOR 16/16 零例外）**n=1 单钉靠窗口位移永远过不了**（谷底卡 0.7019–0.7031，永差 0.002–0.003）；11-02 规则「n=1 不判死、归因后破墙」依然成立，但**破墙主杠杆 = 算子/几何换面**（改变 PnL 形状躲单点碰撞），窗口谷只留一个对照臂（R12）。两轴同看（prod 轴 + 2Y/换手轴，skill 跨区反例）。

**12 臂设计**（基线 `rank(ts_quantile(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 504), 22, driver=gaussian))`；每臂一个独立杠杆面；来源=自建+pack 经济机制+skill）：

| # | 杠杆面 | 结构 |
|---|---|---|
| R1 | 换分母 EV→cap | `rank(ts_quantile(ts_av_diff(divide(NI, cap), 504), 22, driver=gaussian))` |
| R2 | 换矩 水平→22 日动量 | `rank(ts_delta(divide(NI, EV), 22))` |
| R3 | 换矩 60 日动量平滑 | `rank(ts_mean(ts_delta(divide(NI, EV), 60), 22))` |
| R4 | 残差化 EV 溢价 | `vector_neut(base, rank(divide(EV, cap)))` |
| R5 | 算子替换 ts_rank 几何 | `rank(ts_rank(ts_av_diff(divide(NI, EV), 504), 22))` |
| R6 | 算子替换 ts_zscore 几何 | `rank(ts_zscore(ts_av_diff(divide(NI, EV), 504), 22))` |
| R7 | 分组轴 subindustry 组内秩 | `group_rank(base_quantile, subindustry)` |
| R8 | 尾部放大壳（无外层 rank） | `signed_power(subtract(base, 0.5), 3)` |
| R9 | 换分母+换矩 EP 季动量 | `rank(ts_delta(divide(NI, cap), 60))` |
| R10 | 双窗差（趋势加速度） | `subtract(base, rank(ts_quantile(ts_av_diff(divide(NI, EV), 252), 22, driver=gaussian)))` |
| R11 | subindustry 中性壳（改权重面） | `group_neutralize(base, subindustry)` |
| R12 | 窗口谷对照（skill 判死臂，W 504→428） | `rank(ts_quantile(ts_av_diff(divide(NI, EV), 428), 22, driver=gaussian))` |

**预检**：validate_expressions（GBR/TOP700/D1）**12/12 字段存在**（platform_field_count=3）；`gaussian` 为命名参数值误报（基线本体带 driver=gaussian 成功仿真 S 1.99 为实证）。**派发**：`results/_pwd_rescue_list.json`（三键契约）→ batch_simulator 批 3 并发 2，任务 `bg_e581fd16`，收批 `results/_pwd_rescue_status.csv`。臂↔表达式映射 `results/_pwd_rescue_arms_map.json`。

**归因预案**：出线者过四审（五闸+fRA+self）→ prod<0.7 预锁（peek 收值）→ 互相关 vs 9 席篮解最大团。**同族只提 1 颗**（skill 陷阱 1：谷内变体 self 互撞）；R8/R11 是基线壳（与基线同腿 ~0.89），只用于验证「形状改变是否降 prod」，不计独立席位。

**9 席篮当日 prod 快照（03:47–03:52 peek，`results/_basket9_prod_snapshot_20261103.json`）**：9/9 全 <0.7，但**贴线三件**——`0mYoANkv` 0.6932（厚尾 [0.5,0.7)=662）、`P0gvv5gE` 0.6905、`9qWwZ3go` 0.6890（中尾 208）；`WjOkLGWx` 0.6577 虽有余量但主题厚尾（[0.5,0.7)=886，与降级的 E56onL5r 同级）；`bl6qldJ6` 0.5421 / `rKRPAWv9` 0.3998 最干净。**含义**：①提交序=干净件先行，贴线件在其当轮 refresh 终验后立提；②破墙波 R1–R12 出线者兼任贴线件的**替补库**（不只补第 10 席）；③prod 快照只在测量当刻有效。

### §14.22 ★★★★★ 2026-11-03 03:53 R6 四审全过 → 第 10 席锁定 `1YNzwl6k`，10 席篮子凑齐

**R6（ts_zscore 几何换面）四审实测**：

| 审 | 读数 | 线 | 判 |
|---|---|---|---|
| 五闸 | S **1.73** / F **1.06** / 2Y **2.30** / TO 15.4% / sub-univ 1.36 / returns 5.78% | S≥1.58, F≥1.0, 2Y 分档 | ✅ |
| fRA | **failed_ra_count = 0** | WARNING 级也算失败 | ✅ |
| prod | **0.5188**，直方图 **[0.7,0.8) n=0**、[0.5,0.7) 仅 3 颗 | <0.7 严格 | ✅ 余量 0.18 |
| self | **0.1246** | <0.7 严格 | ✅ 余量 0.58 |

**互相关**：R6 对 9 席全部 ≤0.0895（近乎正交）；`compute_mutual_correlation` 10 颗精确解 `max_mutually_below_subset_size=10`（max_pair 仍是 vR1aEpa3↔O0AKLMKq 0.6566）。**10 席一腿一票成立**。

**破墙战役归因定稿**：基线 pwdQb78v（ts_quantile-gaussian 几何）prod 0.7205 n=1 单钉；12 臂里唯一活口 R6 = 同信号**几何换面 ts_quantile→ts_zscore**（S 1.99→1.73 仅损 0.26），prod 0.7205→**0.5188 且 n→0**——钉子挂在 quantile 几何的权重剖面上，zscore 尾部权重不同整个绕开。窗口谷对照臂 R12（1.47）证实窗口位移非活路（skill 16/16 一致）。**浅钉 n=1 破墙首选杠杆 = 同信号几何换面，而非窗口位移**。

**10 席终表**：kqNZKN5K(0.62) / rKRPAWv9(0.40) / bl6qldJ6(0.54) / O0AKLMKq(0.60) / vR1aEpa3(0.66) / WjOkLGWx(0.66) / P0gvv5gE(0.69⚠) / 0mYoANkv(0.69⚠) / 9qWwZ3go(0.69⚠) / **1YNzwl6k(0.52)**。NEWS 塔 3/3 由 kqNZKN5K 或 rKRPAWv9 提交点亮（单数据集 news，无门控）。**待用户提交授权**（不可逆）：授权后按「干净件先行→贴线件当轮 refresh 立提」逐条终验提交。




## §15 ★★★★★ 2026-11-03 13:0x 跨区迁移：GBR NEWS 模板总结 → 其它 region 挖 regular

> 新目标（用户改写）：「GBR 的 NEWS 的模板可以总结一下，在其它 region 的 NEWS 的 category 下挖掘 regular alpha 吗」
> 完整交付：`docs/reference/gbr_news_template_summary_and_cross_region_migration_20261103.md`（Part A 模板总结 / Part B 迁移地图 / Part C CHN 首波）。

### §15.1 GBR NEWS 模板的可迁移提炼（8 条教训 + 5 轴）

- **5 条独立轴**（NEWS 塔容量上限 = 5，不是 6）：A 新闻到达率 / B sse 强度 / C 事件强度求和 / D 情绪分到达率 / E 合成置信。
- **换轴只有两条路**：换语义不同字段、换数据集。**换结构救不了相关性**（载体 = 字段信息轴）。
- 8 条教训：L1 相关性载体=信息轴 / L2 强几何 vs 弱几何（同字段 S 0.91→1.86+）/ L3 vec_count 对满填充字段是恒等变换 / L4 winsorize∘ts_rank 与 ts_zscore 前置是恒等/冗余 / L5 二阶矩几何在到达率字段上无信息 / L6 同字段当乘子有效当本体无效（novelty：S1.85 vs −0.33）/ L7 掩码类双杀（TO↑+广度↓⇒F崩）/ L8 裸 rank(sentiment) 禁用。

### §15.2 ★ 全平台 NEWS 数据集存量盘点（14 region 实拉）

⚠ **universe 必须用各区 default_universe**（`src/wqb/config.py`）：给 EUR/ASI/CHN/IND/JPN/KOR/TWN/HKG/DEU/MEA/AMR/GBR 传 TOP3000 会**返回空**（不是没数据，是 universe 非法）。第一次普查只扫出 USA/GLB 就是这个坑。

| region | universe | NEWS 集数 | 备注 |
|---|---|---:|---|
| USA | TOP3000 | 26 | news18 aC 60336 重饱和 |
| GLB | TOP3000 | 15 | |
| EUR | TOP2500 | 20 | |
| ASI | MINVOL1M | 22 | |
| IND | TOP500 | 22 | |
| KOR | TOP600 | 24 | **news 塔已全清点 24 集，只剩 news20 一条缝** |
| HKG | TOP800 | 24 | |
| DEU | TOP500 | 17 | **news 6 集已做模板池+剖面** |
| **CHN** | TOP2000U | 9 | **★★★★ 处女区：aC 3–7，valueScore 5–6，字段级 aC≈0** |
| AMR | TOP600 | 28 | news29 aC=5 / news84 aC=25 / news85 aC=35 |
| **JPN / TWN / MEA** | — | **0** | **平台无 NEWS 数据集**（迁移禁区，别再查） |

### §15.3 ★ CHN 首波（news46，12 模板）设计要点

- **选靶 CHN/news46**：cov **1.0**（全 CHN 最优）/ 数据集 aC=7 / 字段级 aC 0–4 / valueScore **6** / 37 字段全 VECTOR；CHN/D1 **全 14 塔 0/3**（含 news=0）。
- **CHN 严闸 = LOW_SHARPE 2.07**（比 GBR 1.58 严；CHN 既往 S1.45 即判死）。
- **CHN 三条死路警告（`tracking/CHN/config/cells.json`）**：① 禁「rank(x) 负 Sharpe 就取负镜像」⇒ 反向腿必须换结构；② **`ts_backfill` 会破坏事件条件性**（把信号换掉而非平滑）⇒ CHN 禁 backfill；③ 换手 <20% 硬要求。
- **设置档**：CHN/TOP2000U/D1/SUBINDUSTRY/decay4/truncation0.08/VERIFY/nanHandling OFF/pasteurization ON/maxTrade OFF/FASTEXPR（`tracking/CHN/config/settings.json` 既有档，未沿用 GBR 的 FAST）。
- **CHN 分组字段**：`industry` / `market` / `exchange` / `country` / `currency` + 大量 `china_*_pca_component*` / `method*_cluster*`；⚠ `country` 是单一国家（A 股）⇒ `group_neutralize(·, densify(country))` 无效，用 `densify(market)`。
- **12 模板**：C1 密度反转 / C2 nip×returns 相关 / C3 nip×returns 协方差 / C4 双情绪通道协方差 / C5 新颖度×相关性乘性 / C6 注意力稀释比值 / C7 **时间链年龄 elapsed**（GBR 从未测）/ C8 **故事链位序 index**（GBR 从未测）/ C9 **实体-故事偏离** / C10 **全球vs本地新颖度差** / C11 **社论观点分 mce**（GBR 从未测）/ C12 **冲击-相关价差**。
- **塔混核算**：纯 news46 单数据集单塔 ⇒ 不触 trio 禁混；仅 C2/C3 引入 `returns`（PV 腿）⇒ PV×NEWS 的 trio×非trio 组合**全波 ≤5**，此处占 2，且不得再引入 MODEL/OTHER 腿。
- **preflight 全过**：`valid=true` / 12 表达式 / `unknown_fields=[]`（10 个 `mws46_*` + builtin `returns`）。

### §15.4 ★ 第二/三靶位（下一波候选，已拉字段画像）

- **HKG/news36**（cov 0.81，数据集 aC=50，**字段级 aC 0–14**）：43 字段。机制面最厚——① 正负情绪**置信**（`mws36_sentiment_positive_confidence` / `negative_confidence` / `phrase_*` / `words_*` 四组计数）② **novelty 三件套**（`mws36_novelty` / `novelty_newest_span` / `novelty_oldest_span` 毫秒时间链）③ **归一分母**（`mws36_total_words` / `token_count_total` / `negative_word_count`）④ 相关度（`mws36_relevance` / `entity_relevance_score`）⑤ 事件置信（`main_event_certainty` / `mws36_key_event_confidence`）⑥ 故事间隔四件套（earliest/newest/recent/oldest_story_time_gap）。⇒ **词数归一分母 + 正负置信比**是 GBR 完全没测过的结构。
- **AMR/news73**（cov 0.79，数据集 aC=27，字段级 aC 0–5）：22 字段全是 Dow Jones 分情绪——① **per-entity 部分分**（`nws73_entitiessent_*partscr` 9 路：certainty/fear/findown/finhype/finup/finvolatile/negative/positive/uncertainty）② **story-level 全局分**（`nws73_globalsent_*score` 9 路对应）③ 实体识别表（`entitiescounter` / `djnindustry` / `djnsubject`）。⇒ **「实体分 vs 故事分」的双层结构天然承载 GBR C9 偏离模板**，且 **fear / uncertainty / finhype 三路是 GBR 五轴里完全没有的新轴**。
- **AMR/news85**（cov 0.926，aC 35，字段级 aC 0–6）：情绪**分布形状**族（skewness / median / peak / sum + sentiment1/sentiment2 双通道），对应 forum 帖 43554159658647「情绪通道非对称：涨跌反应差」。
- **AMR/news29**（cov 0.545，aC 5，字段级 aC 0–2）：`nws29_frontpage`（Reuters 头版标记）+ `nws29_significance`（1=高/2=中/3=低）⇒ **媒体重视度轴**，但只有 2 个可用数值字段，机制面薄 ⇒ 三备。
- **排除**：DEU/news29（cov=0）、DEU/news38（仅 3 字段且 `story_analytics_*` 是 CHN news38 同名字段但 DEU 只有 3 个）、HKG/news23（是 VC/PE 交易数据集不是情绪，cov 0.33）。

### §15.5 ★★★★★ CHN news46 首批 12 条实测（2026-11-03 13:12–13:19，全部 COMPLETE）

设置：CHN/TOP2000U/D1/SUBINDUSTRY/decay4/trunc0.08/VERIFY/nanHandling OFF/pasteurization ON/maxTrade OFF/FASTEXPR；壳 `ts_target_tvr_decay(target_tvr=0.05)`。

| tag | alpha | S | F | TO | 判读 |
|---|---|---:|---:|---:|---|
| C1 密度反转 `vec_count(story_count)` | `YP1vNmg6` | 0.18 | 0.05 | 5.6% | 弱（逐年 S 0.84/1.40/−0.85 有残响） |
| C2 nip×returns 相关 | `LLMGn6d9` | −0.69 | −0.40 | 6.2% | 负（EUR 正向不跨区） |
| C3 nip×returns 协方差 | `e753n2gp` | −0.51 | −0.25 | 5.7% | 负，与 C2 同机制面 |
| C4 双情绪通道协方差 | `npvNnzYz` | −0.46 | −0.25 | **4.1%** | 负 + TO 低于 CHN 闸下限 5% |
| C5 **GBR S1 全闸结构直移植** | `MPYGbpe9` | **0.03** | 0.00 | 6.8% | ★ 关键证据：几何/字段都没错 |
| C6 注意力稀释比值 | `npvNnge3` | −0.30 | −0.11 | 5.8% | 弱负 |
| C7 时间链年龄 `ens_elapsed` | `leAW7jb2` | −0.37 | −0.17 | 5.9% | 弱负 |
| C8 故事链位序 `story_index` | `akK1N7q1` | **−0.76** | −0.45 | 5.3% | 本批最强负；CHN 禁取负镜像 ⇒ 需换结构 |
| C9 实体-故事偏离 | `9qxp9W3r` | **0.00** | — | **0.0%** | ⛔ **退化**（long/short=0）⇒ `mws46_ess` 与 `mws46_storyid_ess` 逐位相同（GBR L5 重演） |
| C10 全球vs本地新颖度差 | `P0oGngbx` | −0.35 | −0.17 | 9.1% | 弱负（TO 最高，差结构未换手） |
| C11 社论观点分 `mce` | `d5WZnazJ` | 0.25 | 0.09 | 5.9% | 本批最正 |
| C12 冲击-相关价差 | `KPJGngQx` | −0.84 | −0.55 | 5.9% | 本批最强负 |

**逐年覆盖核验**（`get_alpha_yearly_stats` 实测 3 条）⇒ 全 10/10 年有 pnl + longCount 15–40 ⇒ **无 leading-gap / 无连续空窗**。

**归因判决**：12 条无一过 CHN 严闸（S≥2.07）。但 **C5 = GBR 全闸结构直移植仅 0.03** 是决定性证据 ⇒ **几何与字段语义都没错，错在「设置档 + 壳」**（GBR 全闸件全在 FAST+decay15 出货、TO 8%；CHN 既有档 SUBINDUSTRY+decay4、TO 塌到 4–7%）。

**⇒ 立即派 2×6 因子 A/B 波**（C1–C6 × {FAST15+壳, BASE+裸}）：一次跑出「档位贡献」与「壳贡献」的可分离归因。**单档低 S 不构成判死依据**（与「FAST/SLOW 档必须 A/B」同族铁律）。

**字段语义核验（移植前必做，已验 2 例）**：
- CHN/news46：`mws46_ess`（Event Sentiment Score）与 `mws46_storyid_ess`（同字段的 story 层）**是同一口径的两层** ⇒ C9 差值恒 0。⇒ **forum 双通道模板（96 赞）要求的是「正/负」两通道**，news46 并不具备。
- CHN/news38：`mws38_positive_score` / `mws38_negative_score` / `mws38_positive_freq` / `mws38_negative_freq` **确为真·正负双通道** ⇒ 双通道模板在 news38 才成立，已派第三波（E1–E12）。

**CHN news 塔既有死因核验（不传染）**：`tracking/CHN/config/cells.json` 三条死路全部锁在**结构层**——① `market_news_sent` 情绪-关注度价差（robust 子宇宙墙 + 严闸 2.07 双重卡死）② `news_sentiment_enriched` 语调族（`ts_backfill` 破坏事件条件性）③ **禁止「rank(x) 负 Sharpe 就取负镜像」**。⇒ 死因针对具体字段族，**news46/news38 全新字段族不受传染**；但「取负镜像」这条在 news38 反向腿上同样适用。
