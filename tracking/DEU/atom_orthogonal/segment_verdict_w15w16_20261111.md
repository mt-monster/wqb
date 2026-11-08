# DEU ATOM 战役 · Wave 15（model216）/ Wave 16（shortinterest3）判决
> region=DEU / TOP500 / D1 / SUBINDUSTRY / decay4 / trunc0.08 / nan OFF / pasteurize ON / unit VERIFY
> 判死闸：S≥1.58、F≥1.0、2Y≥1.58、0.01≤TO≤0.7、sub_u≥0.474×S、failed_ra=0
> 生成时间：2026-11-11

---

## 一、Wave 15：`model216` 纯单数据集（ARM 修正模型）→ **判弱**

批次 `12XoP3g4w5dH8Mkd6bhq01O` · 10/10 REJECT · 数据集 cov 0.7121 / 45 字段全 VECTOR / ac 629 / uc 349

### 模板库与结果全表

| # | 模板 | 机制 | 算子 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `group_rank(ts_mean(vec_avg(preferredblendedrevisionfy1percent),22),industry)` | 修正幅度水平（月窗） | 3 | mLoQxpg2 | 1.17 | 0.89 | 0.64 | 0.0521 | 0.62 | 3 |
| 2 | 同字段 132/11 两腿异窗 `add` | **冠军骨架** | 6 | O0Ag5OrR | **1.41** | **1.19** | **1.01** | 0.0509 | 0.83 | 2 |
| 3 | `subtract(FY1,FY2)` | 期限结构 | 5 | Jjer5qNE | 0.49 | 0.23 | 0.56 | 0.0607 | 0.64 | 3 |
| 4 | `subtract(FQ1,FY1)` | 季度/年度差 | 5 | qMLVm8xA | 0.07 | 0.01 | 0.38 | 0.0793 | −0.45 | 4 |
| 5 | `subtract(rank(preferred,66),rank(revenue,66))` | 利润 vs 营收修正差 | 6 | VkxeYVab | 0.79 | 0.46 | 0.79 | 0.0468 | 0.75 | 3 |
| 6 | `add(add(pref,sec),rev)` 同窗 | 三度量等权广度 | 5 | leA1RdKx | 1.13 | 0.86 | 0.57 | 0.0515 | 0.52 | 4 |
| 7 | `group_rank(ts_mean(vec_avg(recommendationblendedrevisionpercent),22),industry)` | 推荐评级修正独立腿 | 3 | omEZ97W6 | 0.09 | 0.02 | −0.71 | 0.0602 | 0.29 | 3 |
| 8 | `rank(ts_mean(vec_avg(armindustry1rank),22))` | ARM 预归一化排名（不加轴） | 3 | vR1PJ82b | 1.06 | 0.82 | 0.50 | 0.0426 | 0.72 | 3 |
| 9 | `multiply(rank(pref,22),rank(armglobal1rank,66))` | 修正 × ARM 双视角一致 | 6 | VkxeYVdJ | 1.31 | 1.08 | 0.64 | 0.0453 | 0.65 | 2 |
| 10 | `subtract(rank(pref,66),rank(sec,66))` | preferred vs secondary 分歧 | 6 | MPYV5O0k | 0.20 | 0.06 | 0.16 | 0.0602 | 0.26 | 3 |

### 四结论

1. **★ 2Y 天花板 = 1.01**，比 dl_riskfree（1.22）还低。10 条 2Y 分布 0.64 / 1.01 / 0.56 / 0.38 / 0.79 / 0.57 / −0.71 / 0.50 / 0.64 / 0.16 —— **即使 S 用杠杆推到 1.58，2Y 也过不了阻断线**。与 dl_riskfree 完全同一死法。
2. **★ 两腿异窗 132/11 第五次被证实是最强骨架**（1.41 vs 同字段水平 1.17，提升 21%），但提升幅度不足以跨过 1.58。
3. **期限结构族全灭**（0.49 / 0.07 / 0.20）—— 与 starmine 广度族 `zq3eoe6V` −0.31、`RREPaPWn` −0.36 一致。**期限结构 / 分歧度在 DEU 第 4 次被证伪，不要再试。**
4. **推荐评级类第 3 次证伪**（omEZ97W6 S 0.09 / 2Y −0.71；前两次 DRF recommendation 0.02、starmine recommendation_mean_change −0.02）。
5. **`multiply` 不杀信号**（VkxeYVdJ 1.31 > 单腿 1.17）—— 与旧记忆「multiply 死路」相反，DEU 上双视角乘积可用。

### E56pROb9 的 2Y 来源归因
`E56pROb9` S 1.79 / 2Y 2.03 = model216 腿 + starmine 腿。本波证明：**model216 单腿 2Y 只 0.64–1.01，E56pROb9 的 2Y 2.03 几乎全部来自 starmine 腿**。⇒ model216 = **增量腿**（角色与 model264 完全一致）。

---

## 二、Wave 16：`shortinterest3` 借券市场第二字段群 → **判死**

批次 `YVzh54q54QS94n1hf8kM0w8` · 10/10 REJECT · 24 个未用字段（与 MPY9VNY9 的 `shrt3_bar` 腿不相交）

### 模板库与结果全表

| # | 模板 | 机制 | 算子 | alpha | S | F | 2Y | TO | sub_u | failed |
|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `-group_rank(ts_mean(vec_avg(mean_loan_rate_p5_d1),22),industry)` | 借券费率水平（做空成本） | 3 | P0oKXXEW | **0.61** | 0.34 | 0.94 | 0.0651 | 0.31 | 3 |
| 2 | `-group_rank(ts_delta(ts_mean(vec_avg(mean_loan_rate_p5_d1),22),66),industry)` | 费率上升（压力累积） | 4 | 78LlKKVZ | 0.12 | 0.03 | −0.16 | 0.0981 | 0.18 | 3 |
| 3 | `-(max−min)/mean` 费率分散度 | 借券市场摩擦 / 异质信念 | 7 | QPv655dp | −0.09 | −0.02 | 0.26 | 0.1038 | −0.11 | 4 |
| 4 | `-group_rank(借出股数 22d/252d,industry)` | short interest ratio | 6 | ZYQNWWZZ | 0.23 | 0.07 | 0.79 | 0.0643 | −0.18 | 4 |
| 5 | `-group_rank(ts_av_diff(ts_mean(loaned_market_value_usd,22),132),industry)` | 借出美元规模偏离 | 5 | WjOJWWkN | −0.07 | −0.01 | 0.23 | 0.0691 | −0.52 | 4 |
| 6 | `-group_rank(ts_mean(vec_avg(average_loan_duration_days),22),industry)` | 借券期限（做空者持有意图） | 3 | N1N855M7 | 0.18 | 0.05 | 0.11 | 0.0613 | 0.41 | 3 |
| 7 | `-multiply(rank(loan_rate_volatility),rank(mean_loan_rate))` | 双条件（紧张 + 不稳定） | 7 | wpQWJJ6Q | 0.59 | 0.32 | 0.93 | 0.0750 | 0.38 | 3 |
| 8 | `group_rank(交易笔数 22d/252d,industry)` | 借券活动升温 | 6 | 78LlKKO2 | −0.36 | −0.14 | −1.13 | 0.0628 | 0.08 | 3 |
| 9 | `-add(rank(main费率,132),rank(main费率,11))` | 费率 132/11 两腿异窗（冠军骨架） | 6 | vR1PJJ0Q | 0.50 | 0.26 | **0.99** | 0.0694 | 0.54 | 3 |
| 10 | `subtract(rank(费率,66),rank(规模比))` | 供给端紧张 vs 供给充足背离 | 11 | 9qxkAAg1 | −0.38 | −0.16 | −0.56 | 0.0599 | −0.28 | 4 |

### 五结论

1. **★ 24 个原始借券字段全灭（S −0.38 ~ 0.61）**，而同数据集唯一出货字段 `shrt3_bar`（1-10 预加工评级）S 1.59 / 2Y 2.36 ⇒ **shortinterest3 只有 1 个可交易信号维度**。
2. **费率水平 0.61 是全组最强** ⇒ 做空成本确实有微弱截面预测力，但量级不到 40%。
3. **借券市场的「量」维度无信息**：借出美元规模 −0.07、借出股数 0.23、交易笔数 −0.36、借券期限 0.18。卖方供给量不预测收益（与 Drechsler & Drechsler 2016 shorting premium 在 TOP500 小池子上失效一致）。
4. **费率分散度 −0.09** ⇒ 异质信念几何第 3 次证伪（前两次：starmine 广度 `RREPaPWn` 2Y −1.77、news104 情绪一致性 −0.23）。
5. **2Y 分布 0.11 ~ 0.99，仍全部 < 1.58**。本段三波（Wave 14/15/16）共 30 条 alpha，**2Y 超过 1.58 的一条都没有**。

---

## 三、★★★ 跨波元规律（本段最重要发现，直接改选集策略）

把 DEU 全部已出货件的字段与全部已判死字段摆在一起看：

| 已出货 | 字段性质 | 已判死 | 字段性质 |
|---|---|---|---|
| QPvzNNGG / LLMzYrZe | `mean_estimate_change_pct_*`（平台算好的修正**百分比**） | starmine 广度族 | `analyst_upward_revision_count`（**计数**） |
| QPv6jLvX | `anl93_recprofitabilityprev_estimator_profitability2`（平台算好的推荐**盈利性评分**） | shortinterest3 24 字段 | `mean_loan_rate` / `loaned_share_count` / `transaction_count`（**水平 / 计数**） |
| MPY9VNY9 | `shrt3_bar`（1-10 借券需求**评级**） | model264 纯单集 | `_class`（归一化分档，但被压掉了符号与幅度） |
| mLox6Mg2 | `snt7_all_languages_views` + `snl27_relpopularity08`（平台算好的**相对关注度**） | dl_riskfree | `probability_*`（**水平概率**） |
| E56pROb9 | `mdl216_preferredblendedrevisionfy1percent`（**百分比**） | model216 其余 35 字段 | `arm*_score` / `arm*_1rank` 之外的原始项 |

**规律：DEU（TOP500 小宇宙）上，只有平台预加工的「复合评分 / 百分比 / 相对值」字段能出货；原始的水平、计数、天数、金额字段全部失败。**

机理：TOP500 只有 500 只票，微观结构量（借券费率 0.1–50%、交易笔数 1–500、分析师家数 1–20）的横截面差异被个股规模与流动性噪声淹没；平台预加工字段已经做过截面标准化 + 跨源聚合，把规模效应剥掉了。

**可移植判据（写进选集第一道筛）**：
- ✅ 优先数据集：字段描述含 `percent` / `score` / `rank` / `ratio` / `index` / `rating` / `relative` / `normalized` / `change`
- ❌ 次优先（只在没有 ✅ 时才碰）：字段描述含 `count` / `number of` / `total` / `average` / `days` / `amount` / `usd` / `price`
- 本判据可解释此前 38 个数据集判死中的 30+ 个。

---

## 四、Wave 17（在飞）：`sentiment33` 新闻情感极性

批次 `19ocKH1OY4BaaRbOFwGoNjQ` · 数据集 cov 0.3221 / **255 个字段全 VECTOR** / ac 45

### 数据集结构与已出货姊妹对比
- `sentiment7`（cov 0.7418 / 3 字段 / ac 94）→ 已出货 mLox6Mg2 S 2.05 / 2Y 2.53，用的是 `all_languages_views`（**关注度**）
- `sentiment27`（cov 0.9038 / 18 字段 / ac 324）→ 已出货 mLox6Mg2 第二腿 `relpopularity08`（**相对流行度**）
- **`sentiment33` = 情感极性**（pos / neg / neut / obj 分数），与关注度是**不同机制面**，不是同数据集变体 ⇒ 不触发 self-corr 墙

### 字段族结构（5 套 NLP 方法 × 5 个关键词窗口 fkw1..fkw5）
- `method_1_*` = **计数**（positive token count）+ `valid_tokens_total`（总词数）
- `method_2_*` / `method_3_*` / `method_4_*` = **0–1 加权平均分数**（预加工，符合第三节 ✅ 判据）
  - 各有 `_filtered_pos/neg/obj`（额外 NLP 过滤，更干净）+ 无过滤 `_pos/neg/obj`
  - **注意：method_2/3/4 没有 `_neut`，只有 method_1 有**
- `method_5/6/7/9` = 纯计数无极性（按判据 ❌，本波不用）
- `sentiment_model7_score1` / `model9_score4/5` = 单一模型计数
- `group_level_3/5_count` = 层级关键词计数；`valid_tokens_total` = 总词数；`median/max_token_length` = 文本长度

### 10 模板（结构互异，算子全 ≤12）

| # | 模板 | 机制 | 算子 | 按第三节判据预判 |
|---|---|---|---:|---|
| T1 | `group_rank(ts_mean(m3f_pos − m3f_neg, 22), industry)` | 净极性差（NLP 过滤分数版） | 7 | ✅ 分数 |
| T2 | `group_rank(ts_mean((m1_pos − m1_neg)/valid_tokens, 22), industry)` | 计数型净极性占比 | 10 | ❌ 计数 |
| T3 | `group_rank(ts_mean(m3_pos/(m3_pos+m3_neg), 22), industry)` | 正情绪占比（比率几何） | 10 | ✅ 分数 |
| T4 | `group_rank(add(rank(ts_mean(m3f_pos,132)), rank(ts_mean(m3f_neg,11))), industry)` | 长窗正 vs 短窗负（异窗骨架） | 11 | ✅ 分数 |
| T5 | `group_rank(ts_delta(ts_mean(m4_pos − m4_neg,22),66), industry)` | method_4 情绪动量 | 9 | ✅ 分数 |
| T6 | `group_rank((m3f_pos−m3f_neg) − (m3_pos−m3_neg), industry)` | NLP 过滤增量（二阶差分） | 12 | ✅ 分数 |
| T7 | `group_rank(ts_mean(m2_pos+m3_pos+m4_pos,22), industry)` | 跨方法正情绪共识 | 10 | ✅ 分数 |
| T8 | `group_rank(ts_mean((m2f_pos−m2f_neg)×valid_tokens,22), industry)` | 情绪 × 信息量交互 | 10 | ✅ 分数 |
| T9 | `group_rank(ts_mean(group_level_5_count/valid_tokens,22), industry)` | 层级事件强度（腿与情感不相交） | 7 | ❌ 计数 |
| T10 | `group_rank(ts_mean(signed_power(m3f_pos−m3f_neg,3),22), industry)` | 极端情绪三次方放大 | 9 | ✅ 分数 |

窗口全部标准：11（半月）/ 22（月）/ 66（季）/ 132（半年）。
全部单数据集 ⇒ 严格 ATOM，不触发禁混集合。

### 风险
cov 0.3221 ⇒ 67% 股票无值，TOP500 里约 163 只有数据。已用 `ts_backfill(vec_avg(X), 22)` 补覆盖（mLox6Mg2 用同一手法）。若结果出现大面积低 sub_universe，需加长 backfill 到 66。

---

## 五、本段战果汇总

| 波次 | 数据集 | 塔 | 判据 | 最高 S | 最高 2Y | 判决 |
|---|---|---|---:|---:|---:|---|
| Wave 15 | model216 | MODEL | 10/10 REJECT | 1.41 | 1.01 | **判弱**（增量腿） |
| Wave 16 | shortinterest3 | SHORTINTEREST | 10/10 REJECT | 0.61 | 0.99 | **判死**（仅 shrt3_bar 有效） |
| Wave 17 | sentiment33 | SENTIMENT | 在飞 | — | — | — |

**累计**：严格单数据集 ATOM 合格 4 颗；合格件 6 颗（含 1 颗违 MODEL+MODEL 禁混的 E56pROb9，剔除后 5 颗）。缺口 6 颗。

**本段新增判死**：model216（弱）、shortinterest3 的 24 个原始字段（死）。累计有数据判死 ≈40 个数据集。
