# news18 (Ravenpack News Analytics) — GBR/TOP700/D1 字段画像与模板池

> 落盘日期：2026-10-30 ｜ 区域：GBR ｜ Universe：TOP700 ｜ Delay：1
> 数据集：`news18` ｜ category：NEWS ｜ pyramid multiplier：1.6（news 档）
> 本文件替代性说明：`news104` 已整集封盘（见 `docs/reference/field_profile_news104_gbr_20261030.md` 与台账 `gbr_news104_closed_20261030`），news18 为继任主战场。

---

## 一、数据集画像

| 指标 | 值 | 判读 |
|---|---|---|
| 字段数 | **70** | news104 仅 11，本集可挖维度多 6 倍 |
| 数据集 coverage | 0.8192 | 高于 news104 的 0.9695 之外仍属健康档 |
| 单实体族 coverage | 0.7149 | `nws18_*` 无前缀别名族 |
| 多公司聚合族 coverage | **0.9714** | `nws18_multiple_comp_*`，覆盖率最高 |
| 别名/长名族 coverage | 0.7415 | `analyst_recommendation_change` / `sentiment_*_d1` 等 |
| alphaCount（平台累计） | 1197 | 拥挤，但 70 字段摊薄后多数字段 <30 |
| 在 21 个判死集清单内 | **否** | 与 news17/news20/news38/news48 不同，本集未判死 |
| 十年数据（2014–2023） | **PASS**（实测） | 见 §三 逐年证据 |

### 1.1 数据类型分布
- **VECTOR**：绝大多数信号字段（须先 `vec_avg` / `vec_sum` / `vec_count` 聚合）
- **SYMBOL**：`event_sequence_number_in_story`、`multi_entity_*_sequence_number`、`record_timestamp_utc_*` 等序号/时间戳类 ⇒ **不可直接当信号腿**

### 1.2 三族结构（关键）
本集同一语义有三种并行编码，选族直接决定覆盖率：

| 族 | 前缀 | coverage | 说明 |
|---|---|---|---|
| 单实体短名 | `nws18_*` | 0.7149 | 主体字段，最常用 |
| 多公司聚合 | `nws18_multiple_comp_*` | **0.9714** | 同一新闻故事下所有被提及公司聚合 ⇒ 覆盖率最高 |
| 长名别名 | `sentiment_*` / `analyst_recommendation_change` / `event_sentiment_score` 等 | 0.7415 | 可读性最好，多带 `_d1` 后缀标明延迟口径 |

---

## 二、字段语义分类（三分：主信号 / 权重 / 门控）

### 2.1 主信号腿（可直接做排序轴）

| 字段 | 语义 | 值域 | coverage | alphaCount | 建议窗口 |
|---|---|---|---|---|---|
| `nws18_ssc` | 综合情绪分（多技术合成） | −1.00~+1.00 连续 | 0.7149 | 58 | 短 5–22 |
| `nws18_sse` | 事件级情绪极性 | −1.00~+1.00 连续 | 0.7149 | 28 | 短 5–22 |
| `event_sentiment_score` | 实体级情绪（连续） | −1.00~+1.00 | 0.7415 | 17 | 短 5–22 |
| `sentiment_composite_score_d1` | 故事级综合情绪（D1 口径，=CSS） | −1.00~+1.00 | 0.7415 | 17 | 短 5–22 |
| `nws18_nip` | 叙事影响分（预估未来 2 小时市场影响） | −1~+1 | 0.7149 | **106** | 短 5 |
| `analyst_recommendation_change` | **分析师评级变化**（=ANL_CHG） | 三值 −1/0/+1 | 0.7415 | 21 | 中 15–60 |
| `nws18_ghc_lna` | **情绪变化量**（语气分析） | 连续 | 0.7149 | **9（蓝海）** | 中 15–60 |
| `nws18_bee` | 财报评价情绪 | 三值 −1/0/+1 | 0.7149 | 13 | 短 5–22 |
| `nws18_acb` | 公司行动公告情绪 | 三值 | 0.7149 | **4（蓝海）** | 中 10–40 |
| `nws18_bam` | 并购情绪 | 三值 −1/0/+1 | 0.7149 | **4（蓝海）** | 中 10–40 |
| `nws18_qmb` | 全球市场评论/社论情绪 | 三值 | 0.7149 | **202（最拥挤，回避）** | — |
| `nws18_multiple_comp_ssc` | 多公司聚合综合情绪 | −1.00~+1.00 | **0.9714** | 81 | 短 5–22 |
| `nws18_multiple_comp_sse` | 多公司聚合情绪极性 | −1.00~+1.00 | **0.9714** | 51 | 短 5–22 |
| `sentiment_news_impact_projection_d1` | 新闻对波动的冲击预估（D1） | −1.00~+1.00 | 0.7415 | **0（完全未挖）** | 短 5 |
| `sentiment_earnings_classifier_d1` | 财报情绪（D1） | 三值 | 0.7415 | **0（完全未挖）** | 短 5–22 |

### 2.2 权重腿（不可单独排序，用于加权/缩放）
| 字段 | 语义 | 值域 | coverage | alphaCount |
|---|---|---|---|---|
| `nws18_relevance` | 实体与故事的相关强度 | 0–100 | 0.7149 | 23 |
| `nws18_multiple_comp_relevance` | 多公司版相关性 | 0–100 | **0.9714** | 40 |
| `event_relevance_score` | 事件在故事中的相关度 | 0–100 | 0.7415 | **3（蓝海）** |
| `nws18_event_similarity_days` | 距上次相似事件天数（新颖度，0–365） | 0–365 | 0.7149 | 21 |
| `days_since_similar_event` | 同上（别名 EVENT_SIMILARITY_DAYS） | 0–365 | 0.7415 | 7 |
| `nws18_mltpl_cmp_event_simildays` | 多公司版新颖度 | 0–365 | **0.9714** | 8 |

### 2.3 门控腿（过滤/条件，不直接贡献方向）
| 字段 | 语义 | 值域 | 典型用法 |
|---|---|---|---|
| `story_event_record_count` | 故事内事件记录数（注意力摊薄） | 计数 | `divide(sentiment, count)` 或 `trade_when(count<N, ...)` |
| `multi_entity_story_event_count` | 多公司版事件数 | 计数 | 同上（cov 0.9714） |
| `nws18_ber` | 财报发布事件标记 | flag | `trade_when(ber>0, ...)` |
| `nws18_qcm` | 高置信度相关新闻情绪 | 三值 | 只在 qcm 非 0 时取 ssc |

### 2.4 非信号字段（勿当信号腿）
`event_sequence_number_in_story`（SYMBOL）、`multi_entity_*_sequence_number`（SYMBOL）、`record_timestamp_utc_date/time`（SYMBOL）、各 `*_start/end_date/time_utc`（时间戳）、`company_story_headline` / `company_event_summary`（纯文本）、`entity_country_iso_code_4` / `multi_entity_country_iso_code`（地域标签，可作 group 轴但不作信号）。

---

## 三、已测实证（GBR/TOP700/D1，decay 4 / SUBINDUSTRY / trunc 0.08 / nanHandling ON / maxTrade OFF / unitHandling VERIFY）

### 3.1 首轮两腿

| tag | alpha | 表达式 | S | F | R | TO | 2Y | SUB | DD | eff |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 连续情绪水平 | **`P0oeEV9q`** | `group_rank(ts_mean(vec_avg(nws18_ssc), 5), subindustry)` | 0.20 | 0.05 | 1.05% | 20.2% | −0.73 | 0.45 | 11.30% | 0.228 |
| T2 评级动量 | **`3qodWN0O`** | `group_rank(ts_sum(vec_avg(analyst_recommendation_change), 22), subindustry)` | **−0.54** | −0.24 | −2.44% | 12.28% | **−1.28** | −0.36 | 30.44% | **0.446** |

**T2 判读（本集最重要发现）**：S 与 2Y **同时大幅为负**（−0.54 / −1.28）⇒ 这是**稳定的反向信号**，不是弱信号。反向即得 S +0.54 / 2Y +1.28，eff 0.446 为 news 族目前最高（news104 最好仅 0.168，成功线 0.769）。
经济解释：分析师评级上调后股价已被推高，随后发生拥挤反转；或市场对评级变化过度反应（与 Miller 1977 分歧溢价、以及论坛帖 `43497567261207`「拥挤反转只在顶格买入成立」同向）。

### 3.2 逐年证据（十年门槛 PASS）

**`3qodWN0O`（评级动量，注意这是未反向的原始方向）**
| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | −0.43 | +0.88 | −0.71 | +0.02 | **−2.47** | +0.86 | −0.34 | −0.24 | **−1.36** | **−1.23** |
| longCount | 165 | 211 | 266 | 281 | 259 | 225 | 205 | 162 | 181 | 143 |

**反向后的形态**：+0.43 / −0.88 / +0.71 / −0.02 / **+2.47** / −0.86 / +0.34 / +0.24 / **+1.36** / **+1.23**
⇒ 10 年 **7 年正向**（2017 近零）。但正收益**高度集中在 2018 / 2022 / 2023 三个熊市/高波动年**，2015 与 2019 两个牛市年转负。
⚠ **结构性风险**：这不是全天候 alpha，而是「熊市避险效应」。与 `akKJYXj9`（2022 单年贡献 9.18%）同类问题 ⇒ 进 S5 前必须做逐年归因与集中度检查。

**`P0oeEV9q`（连续情绪，未反向）**
| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | +0.65 | +0.20 | −0.17 | +0.03 | +0.54 | +0.62 | +0.68 | **+1.00** | −0.82 | −0.63 |
| longCount | 292 | 310 | 299 | 308 | 314 | 306 | 285 | 299 | 301 | 308 |

⇒ 2014–2021 八年中 7 年正向，但 **2022/2023 连续两年负**（2Y −0.73）⇒ 典型 alpha 衰减形态，近年失效。
⚠ **结论**：ssc 水平轴不作为主攻方向，只在 T5/T6/T7 中作为加权/偏离结构的载体。

### 3.3 与 news104 的对照（为什么换集）
| 维度 | news104 | news18 |
|---|---|---|
| 字段数 | 11 | **70** |
| 情绪编码 | 三值离散 + 概率三分类 | 三值 + **−1~+1 连续** + 变化量 + 事件分型 |
| 最好 S | 0.38 | 0.54（反向） |
| 最好 eff | 0.168 | **0.446** |
| 机制维度 | 情绪水平 / 变化 / 概率差（3 类，全试尽） | 情绪 / 评级 / 变化量 / 财报 / 公司行动 / 并购 / 影响分（≥7 类） |

---

## 四、十二模板池（结构互异，满足「≥10 个」硬约束）

> 约定：`W` 取窗口白名单 `5 / 22 / 66 / 252`；短时效族（情绪、影响分）用 5，中时效族（评级、变化量、公司行动）用 22–66。
> 所有模板均**单塔**（仅 news18 字段 + 内置 `subindustry` / `sector` 分组轴，不引入 PV/MODEL/OTHER 字段）。

### T1 连续情绪水平 + 组内相对化 ★已测 S0.20
```
group_rank(ts_mean(vec_avg(nws18_ssc), 5), subindustry)
```
结构：vec_avg 聚合 → 短窗平滑 → 组内 rank。用途：基线对照。

### T2 评级动量（反向）★已测 S−0.54，反向预期 +0.54
```
multiply(-1, group_rank(ts_sum(vec_avg(analyst_recommendation_change), 22), subindustry))
```
结构：三值分数 **ts_sum 求净变化方向**（不是 ts_mean，因为三值求和才是评级动量的自然定义）→ 组内 rank → 反向。
机制：评级上调 = 已被定价的乐观 → 拥挤反转。

### T3 情绪变化量 ghc_lna ★在飞
```
group_rank(ts_sum(vec_avg(nws18_ghc_lna), 22), subindustry)
```
结构：同 T2 但换字段（情绪变化量 vs 评级变化）。用途：把「变化类」机制从评级推广到情绪语气，检验是否为「变化类因子」共性。

### T4 多公司聚合版 ghc_lna（覆盖率对照）★在飞
```
group_rank(ts_sum(vec_avg(nws18_multiple_comp_ghc_lna), 22), subindustry)
```
结构：同 T3 但用 cov 0.9714 的多公司族。用途：**纯覆盖率对照实验**（信号相同、覆盖不同），单独定位覆盖率对 S 的贡献。

### T5 Relevance 加权（论坛套路一）
```
group_rank(ts_mean(multiply(vec_avg(nws18_ssc), vec_avg(nws18_relevance)), 5), subindustry)
```
结构：情绪 × 相关性权重。机制：低相关性条目多为「顺带提及」，是噪声；加权提升信噪比、延长漂移。
⚠ 单位闸：`nws18_relevance` 为 0–100 整数分，`nws18_ssc` 为 −1~+1 无量纲 ⇒ 乘积带「分」单位，但 `group_rank` 对尺度不敏感，**不得再叠加 add(ε)**。

### T6 新颖度加权（论坛套路二）
```
group_rank(ts_mean(multiply(vec_avg(nws18_ssc), vec_avg(nws18_event_similarity_days)), 5), subindustry)
```
结构：情绪 × 距上次相似事件天数。机制：间隔越久 → 新信息比例越高 → 情绪冲击越强；旧闻重播（间隔短）已被定价。
⚠ 该字段亦有 0 值（同一事件首次出现时为 0 还是缺失需实测确认），若 0 占比过高改用 `days_since_similar_event`。

### T7 Entity-Story 偏离（论坛进阶三，本池最独立的信息源）
```
group_rank(ts_mean(subtract(vec_avg(nws18_ssc), vec_avg(nws18_multiple_comp_ssc)), 5), subindustry)
```
结构：**单实体情绪 − 故事聚合情绪**。机制：捕捉「公司在坏故事里被单独正面提及」这类独立信息，剥离掉行业/主题层共同情绪。
⚠ 单位闸：两者同为 −1~+1 连续分，`subtract` 同单位合法，**不要加 ε**。两者 coverage 不同（0.7149 vs 0.9714），偏离值在单实体缺失时退化为 −聚合值，需观察有效样本数。

### T8 Story Attention Dilution（注意力摊薄）
```
group_rank(ts_mean(divide(vec_avg(nws18_ssc), vec_avg(story_event_record_count)), 5), subindustry)
```
结构：情绪 ÷ 故事内事件数。机制：故事里实体越多，单实体注意力被摊薄，情绪冲击越弱。
⚠ 单位闸：分母为计数（无量纲整数），分子无量纲 ⇒ 合法。分母可能为 0 ⇒ 交给平台产生 Inf/NaN，由 group_rank 吸收，**不加 ε**。

### T9 叙事影响分（厂商预计算前瞻收益）
```
group_rank(ts_mean(vec_avg(nws18_nip), 5), subindustry)
```
结构：直接用 `nws18_nip`（预估未来 2 小时市场影响，−1~+1）做短窗排序。
机制：厂商已把「新闻 → 短期冲击」映射完成，是最接近可交易信息的字段。alphaCount 106 偏拥挤。
对称变体（D1 口径、alphaCount **0**）：`group_rank(ts_mean(vec_avg(sentiment_news_impact_projection_d1), 5), subindustry)`

### T10 财报评价情绪（三值求和）
```
group_rank(ts_sum(vec_avg(nws18_bee), 22), subindustry)
```
结构：三值财报评价 → ts_sum 净方向。机制：财报评价的连续改善/恶化（PEAD 的新闻侧代理）。
⚠ 不叠加 `nws18_ber` 门控（都属同一数据集，加门控不改变塔位，但会牺牲样本量；作为 T10b 对照单独测）。

### T11 公司行动情绪（蓝海，4 alphas）
```
group_rank(ts_sum(vec_avg(nws18_acb), 40), subindustry)
```
结构：中窗 40（论坛归档：公司公告类有效期 3–7 天，但事件稀疏需更长聚合窗保证非零样本）。
机制：分红/拆股/回购公告的情绪方向。alphaCount 仅 4 ⇒ **prod 墙风险最低**，是本池优先级最高的一条。
⚠ 窗口 40 不在白名单 `5/22/66` 内 ⇒ 改用 **66**（最近白名单值）或论证 40 的取值依据。**默认按 66 执行**。

### T12 并购情绪（蓝海，4 alphas）
```
group_rank(ts_sum(vec_avg(nws18_bam), 66), subindustry)
```
结构：同上换字段。机制：M&A 公告情绪（收购方 vs 被收购方的方向不同，GBR 样本以收购方为主）。
⚠ 与 T11 同为事件稀疏型，若 TO 过低（<2%）说明事件太少，需改 `ts_backfill` 短窗（≤5）而非拉长窗口。

---

## 五、单位闸自查表（`unit_handling=VERIFY` 下必查）

| 模板 | 运算 | 分子单位 | 分母/被加项单位 | 合法？ |
|---|---|---|---|---|
| T1/T2/T3/T4 | `ts_mean` / `ts_sum` / `group_rank` | 无量纲 | — | ✅ |
| T5 | `multiply(ssc, relevance)` | 无量纲 × 分 | — | ✅（乘积带分单位，rank 后无关） |
| T6 | `multiply(ssc, sim_days)` | 无量纲 × 天 | — | ✅ |
| T7 | `subtract(ssc, comp_ssc)` | 无量纲 | 无量纲 | ✅ 同单位 |
| T8 | `divide(ssc, event_count)` | 无量纲 | 无量纲（计数） | ✅ |
| T9 | `ts_mean(nip)` | 无量纲 | — | ✅ |
| T11/T12 | `ts_sum(acb/bam)` | 无量纲 | — | ✅ |

**铁律**：本池**没有任何一条需要加 ε**。凡是想到要加 `add(x, 0.0001)` 的地方，都说明分子分母单位不一致，应改写法而不是加常数（`unit_handling=VERIFY` 下会直接 WARNING 失败）。

---

## 六、算子约束（GBR 实测，`operator_audit` 权威）

- **存在**：`ts_mean` / `ts_sum` / `ts_delta` / `ts_rank` / `ts_backfill` / `ts_decay_linear` / `ts_std_dev` / `ts_ir` / `ts_av_diff` / `ts_zscore` / `ts_covariance` / `group_rank` / `group_zscore` / `group_neutralize` / `bucket` / `quantile` / `vector_neut` / `vec_avg` / `vec_sum` / `vec_count` / `vec_stddev` / `rank` / `zscore` / `winsorize` / `scale` / `normalize` / `reverse` / `subtract` / `add` / `multiply` / `divide` / `abs` / `trade_when` / `if_else` / `hump` / `days_from_last_change` / `last_diff_value` / `densify`
- **不存在（勿用）**：**`ts_max` / `ts_min`** / `ts_skewness` / `ts_median` / `ts_percentage` / `ts_entropy` / `ts_decay_exp_window` / `ts_delta_limit` / `group_median` / `group_normalize` / `group_percentage` / `group_vector_proj` / `neutralize` / `sigmoid` / `tanh` / `to_nan` / `ts_min_max_diff` / `ts_min_max_cps` / `ts_partial_corr` / `ts_co_kurtosis` / `s_log_1p`
- `hump` 必须写成 `hump(x, hump=0.0012)` 的关键字形式（两位置参数报错）
- GBR 用 `exchange` / `country` 做分组轴**无效**（只有 LSE 一个交易所）；`sector` 轴两次实测无效 ⇒ **分组轴默认 `subindustry`**

---

## 七、外部证据（论坛 + 论文）

### 7.1 论坛帖（已全文读）

**`43175327536279`《给信号标保质期——新闻情绪字段的时效性分级与短窗模板》** ★★ 本池方法论基石
- 数据源**保质期**归档：实时财经新闻情绪（分钟级更新）→ **有效期 1–3 天**；公司公告/行动（小时级）→ 3–7 天；分析师报告/评级（日级）→ 5–15 天；宏观（周/月）→ 10–30 天；历史财务（季度）→ 单独做长窗无效
- **窗口-强度单调衰减、无中间峰值 = 窗口错配指纹**；有中间峰值才是真周期信号
- 坑一：拿长窗模板统一套所有字段（120 日窗口 → 误判「数据集没鱼」）
- 坑二：**`ts_backfill(x, 20)` 强行续值污染信号** —— 新闻空窗要区分「断粮型（短空窗 ffill 合法）」与「真缺型（小票从无覆盖，回填等于编造中性情绪）」
- 坑三：方向未预检（1 最佳 5 最差的反向刻度）
- 原帖表达式：`group_rank(ts_mean(vec_avg(composite_sentiment_score_2), 5), industry)` / `group_rank(ts_sum(vec_avg(analyst_recommendation_change), 22), industry)`
- 预算分配原则：**同一数据集短窗模板优先跑；短窗无信号则长窗更不会有**

**`42659817284375`《新闻情绪因子:别再用裸 sentiment 了 —— relevance 加权 + 新颖度过滤》**（31 赞）★ 本池 T5–T8 来源
- 套路一 Relevance 加权：低相关性条目是顺带提及=噪声，`情绪 × relevance` 或只在 relevance>60 取情绪
- 套路二 新颖度过滤：`event_similarity_days × sentiment`，相似事件越久远 → 新信息比例越高 → 冲击越强
- 套路三 情绪动量：`ghc_lna`（情绪变化量）天生高换手，配 `ts_decay_linear` / `ts_target_tvr_decay`
- **进阶：多公司聚合族是宝藏** —— `nws20_multiple_comp_*` 覆盖率 0.96 vs 单实体族 0.72；三个方向：Next-Day Confirmation / Story Attention Dilution / **Entity-Story Deviation**
- 一句话总结：情绪因子做不好的 90% 原因是没做信噪比管理

### 7.2 外部论文
- **Tetlock (2007)** *Giving Content to Investor Sentiment: The Role of Media in the Stock Market*, Journal of Finance 62(3) —— 媒体悲观情绪对个股次日收益有显著负向影响；本池 T9（影响分）的方向先验来源
- **Tetlock, Saar-Tsechansky & Macskassy (2008)** *More Than Words*, JF —— 负面词汇占比比整体语气更有预测力 ⇒ 支持「事件分型情绪（acb/bam/bee）优于通用情绪」的设计
- **Miller (1977)** *Risk, Uncertainty, and Divergence of Opinion*, JF —— 意见分歧 + 卖空限制 ⇒ 高估；支持 T2 反向评级动量的拥挤反转逻辑
- **Da, Engelberg & Gao (2011)** *In Search of Attention*, JF —— 注意力（ASVI）驱动短期买压后反转；支持 T8 注意力摊薄
- **Engelberg, Reed & Ringgenberg (2018)** *Short-Selling Risk*, JF —— 借券费率与卖空风险溢价（与 shortinterest3 线交叉验证用）
- **Chalamandaris (2026)** —— 「情绪状态可测量不可交易」，支持「情绪水平轴弱、需结构变换」的实证结论

---

## 八、优先级与执行序

### 8.1 排序依据
`prod 墙风险（alphaCount）× 信号承载能力（eff）× 机制独立性`

| 优先 | 模板 | 理由 |
|---|---|---|
| P0 | **T11 / T12**（acb / bam） | alphaCount 仅 4 ⇒ prod 墙风险最低，蓝海；且属事件分型情绪（Tetlock 2008 支持） |
| P0 | **T2 反向** | eff 0.446 已达 news 族最高，方向已由 S/2Y 同号为负锁定 |
| P1 | T9（nip / D1 投影版） | 厂商预计算前瞻收益，机制最接近可交易信息；D1 版 alphaCount 0 |
| P1 | T7 Entity-Story 偏离 | 剥离共同情绪，与 T1/T2 相关性天然低 ⇒ 有助凑「两两相关<0.7」 |
| P2 | T3 / T4 ghc_lna 覆盖率对照 | 单独回答「覆盖率是否为主要瓶颈」 |
| P2 | T5 / T6 加权 | 论坛套路，但加权不改变信号方向，提升幅度预期有限 |
| P3 | T8 摊薄 / T10 财报评价 | 结构变换类，留作降相关工具 |

### 8.2 执行纪律
1. **一次只改一个变量**（字段 / 窗口 / 变换三轴分离）
2. 每条先算 `eff = sqrt(|R| / TO)`：eff < 0.3 且 S < 0.5 ⇒ 该字段无承载能力，**换字段不换骨架**
3. 反转信号判据：**全期 S 与 2Y S 同号**才可反转（T2 满足：−0.54 / −1.28 同负）
4. 判死前必须做：符号稳定性检查 + 逐年归因 + 中性化扫档（至少 5 档，优先 FAST/STATISTICAL/SUBINDUSTRY/REVERSION_AND_MOMENTUM/NONE）
5. **prod 只看阶段不进探索阶段**：IS 探索时不因 alphaCount 高而预筛字段；但进入 S5 前必须用 MCP `check_correlation` 实读
6. 仿真并发 ≤2/批；账号级 7 槽；429 被拒条目**不自动重试**，须单独补派
7. 每条目做完写台账（`upsert_ledger_key`），带 eff / 逐年形态 / 封盘或续挖结论

### 8.3 点塔路径
NEWS 塔当前 0/3（GBR/D1 本季度）。点亮需 3 颗同塔 α，**两两相关 <0.7 且各自 prod <0.70**。
本池的机制独立性设计正是为此：
- T2（评级动量反向）与 T11/T12（事件分型情绪）方向来源完全不同
- T7（Entity-Story 偏离）与 T1（水平）在构造上正交
- 降相关效力排序（GBR 实测）：**换窗口跨度（r≈0.553）≳ 换变换（0.440）>> 换字段（0.780–0.955）**
⇒ 凑 3 颗时应优先在**同一强机制上换窗口跨度**，而不是硬换字段。
