# DEU ATOM 战役 · Wave 18/19 判决记录（2026-11-12）

> region=DEU / universe=TOP500 / delay=1 / SUBINDUSTRY / decay 4 / trunc 0.08 / 2014-01-01~2023-12-31
> 硬闸：S≥1.58 · F≥1.0 · 2Y≥1.58 · 0.01≤TO≤0.7 · sub_u≥0.474×S · RA失败=0 · self<0.7 · prod<0.7

---

## 一、Wave 18：`model238` 机构持仓 Smart Holdings → **判死**

批次 `1Bkz32eKH4mNcaY1hF28lttn`，10/10 REJECT。

数据集：cov 0.8552 / 22 字段全 MATRIX / ac 130 / uc ——。
两组字段：13 个 `mdl238_*`（**cov 1.0**，rank 1–100）+ 7 个无前缀 `*_rank`（cov ≈0.71，normalized 0–100）。
语义四维：Smart Holdings 总分（global/region/sector/industry/country 五层级）、Change Component（动量）、Owner/crowding rank（拥挤度反向，100=最拥挤）、Screening/style-fit。

| # | 模板 | alpha | S | F | **2Y** | TO | **sub_u** | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| M1 | 水平 `group_rank(ts_mean(mdl238_global_rank,22),industry)` | e75EdpXE | 1.10 | 0.80 | 0.59 | 0.0604 | **0.32** | 4 |
| M2 | 变化动量 global_change | wpQWnx8p | 1.03 | 0.70 | **0.95** | 0.0950 | **0.21** | 4 |
| M3 | 拥挤度反转 `-owner_rank` | zq3eP6vX | 0.19 | 0.06 | −0.23 | 0.0295 | 0.00 | 4 |
| M4 | 异窗 132/11（第五次验证） | E56xgWZr | **1.16** | **0.87** | 0.64 | 0.0532 | 0.24 | 4 |
| M5 | 全球−行业层级差 66 | 1YN0abqz | −0.46 | −0.21 | −0.42 | 0.0432 | −0.27 | 4 |
| M6 | 偏好 × 风格契合 multiply 22 | 88RXa9mv | 1.11 | 0.82 | 0.66 | 0.0521 | **0.38** | 4 |
| M7 | 加仓 − 拥挤度 22 | YP1Y2Kjo | 0.76 | 0.46 | 0.36 | 0.0764 | 0.04 | 4 |
| M8 | 行业排名季度变化 ts_delta 66 | bl6AoZlZ | 0.71 | 0.39 | 0.79 | 0.0935 | 0.14 | 4 |
| M9 | 三层级等权广度 | omEZ35mv | 1.03 | 0.73 | 0.52 | 0.0608 | 0.26 | 4 |
| M10 | 动量时序 z 分数 252 | 9qxka1qr | 0.77 | 0.45 | −0.18 | 0.1014 | 0.29 | 4 |

**四结论**

1. **S 上限 1.16 / 2Y 上限 0.95** —— 双低，0/10 有机会推过闸。M4 异窗骨架仍是全场最强（1.16 vs 同字段水平 1.10，+5%），但增幅远小于历史（132/11 在别的集合能 +21%），说明**该字段本身信息量稀薄，骨架救不回来**。
2. **★ `sub_universe_sharpe` 是本次真正的判死依据，不是 S**：10 条里 9 条 sub_u ≤0.38，而闸线是 0.474×S（M1 需 0.52 实际 0.32、M4 需 0.55 实际 0.24、M6 需 0.53 实际 0.38）——**全部只有闸线的 43%–72%**。这意味着信号在大票上成立、在小票上几乎消失，是**规模依赖型伪信号**，不是可交易的截面 alpha。
3. **拥挤度维度的方向是错的**：M3 `-owner_rank`（低拥挤溢价）S **0.19**，M7「加仓−拥挤度」S 0.76 弱于纯加仓类。⇒ DEU TOP500 上「机构拥挤度」不构成收益定价因子，与 USA 文献（拥挤度反转）不一致，属区域特性。
4. **层级差/层级一致性结构再灭**：M5 `global − industry` **−0.46**（全波最差）。这是「跨层级做差」几何的**第 3 次证伪**（前两次见 analyst93 subtract 分歧度 0.21 / model28 M10 0.25），彻底弃用。

**元规律修订（重要）**：model238 的 13 个主字段都是 **cov 1.0 的 rank 字段**，完全符合「✅ 预加工字段」判据，却只到 S 1.16。
⇒ **「预加工字段」是必要不充分条件**。必须叠加第二条：**该字段的横截面必须真的在动**（见下节 ★★★）。

---

## 二、Wave 19：`model28` StarMine 结构性信用风险 / Merton → **判死**

批次 `3lojyg4dv5fZ9JWO2PLXbF0`，10/10 REJECT。

数据集：cov 0.8105 / 25 字段全 MATRIX / ac 53。7 个 `*_rank` 字段 **cov 1.0**（违约概率百分位排名，越高越安全）；cov 0.68 组含 `pd_pct`、`distance_to_default`、`leverage`、`asset_drift_pct`、`asset_volatility_pct`。
经济学依据：Merton (1974)、Campbell/Hilscher/Szilagyi (2008) 困境风险异象、Vassalou & Xing (2004)、Avramov et al. (2013)。

| # | 模板 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| M1 | ★论坛逆方差（pd_pct, w5, decay30） | vR1Pe02r | **0.00** | 0.00 | 0.01 | 0.0212 | 0.06 | 4 |
| M2 | 信用排名水平 global_rank 22 | O0Agbe8R | **0.02** | 0.00 | 0.10 | 0.0227 | 0.12 | 3 |
| M3 | 违约距离 DD 22 | vR1Pe02b | **0.01** | 0.00 | 0.13 | 0.0227 | 0.11 | 3 |
| M4 | 资产漂移 asset_drift_percent 22 | O0AgbeJ1 | **0.90** | 0.71 | 0.45 | 0.0334 | 0.45 | 3 |
| M5 | 杠杆反向 `-leverage` 22 | 88RXaAvq | −0.06 | −0.01 | **−1.04** | 0.0186 | 0.22 | 3 |
| M6 | ★论坛逆方差迁移到 DD（w22, decay30） | 0mY5eojK | **−0.01** | 0.00 | −0.03 | 0.0335 | 0.02 | 4 |
| M7 | 异窗 132/11 | npvrZ0Ad | **−0.02** | 0.00 | 0.07 | 0.0226 | 0.11 | 3 |
| M8 | 风险恶化动量 `-ts_delta(pd_pct,66)` | A1VEg6QE | **0.67** | 0.42 | 0.14 | 0.0527 | 0.39 | 3 |
| M9 | 资产波动率反向 | 9qxkaoxq | −0.17 | −0.06 | 0.63 | 0.0224 | −0.18 | 4 |
| M10 | 全球−行业层级一致性 66 | 6XdNaxdP | 0.25 | 0.09 | 0.11 | 0.0279 | 0.20 | 3 |

**五结论**

1. **★★★ 最刺眼的事实：7 个 cov=1.0 的 `*_rank` 字段，S 全部落在 −0.02 ~ 0.02。** 这不是「alpha 弱」的数值，这是**精确的 0**。技术上只有两种可能：(a) 字段在 DEU TOP500 内跨截面上近似常数（rank 全部相同 ⇒ group_rank 后全 0.5 ⇒ 中性化后全 0）；(b) 字段与行业中性化后的方向正交且噪声主导。结合 M2/M3/M7 三条不同几何（水平 / DD / 异窗）全部命中 0.00–0.02，**判 (a)：该族字段在 DEU 上退化**。
   ⇒ **新增判读口诀：cov=1.0 的字段跑出 |S|≤0.05，是「字段退化」而非「信号弱」，应在 1 条探针后直接封盘，不要继续换几何。**
2. **★论坛「逆方差加权」模板在 DEU 彻底失效**：M1 S **0.00** / M6 S **−0.01**（USA 同模板 S 1.63 / 2Y 1.61 / prod 0.54）。**但这是「分母吃得下的分子本身是 0」，不是模板被证伪** —— M1 的分子 `pd_pct` 水平在全波里唯一一次单独出场的 M8（delta 形式）也只有 0.67，水平形式无信号。因此结论应写：**逆方差模板尚未在 DEU 得到真正检验，需等一个有水平信号的字段再试一次**（下次遇到 S≥1.2 的候选时，用它做 2Y 增幅器，而不是拿它当救火队）。
3. **全波唯一有料的是 `asset_drift_percent`（S 0.90）**：Merton 模型里资产漂移 = 资产收益率漂移项，是唯一带「方向性预期收益」含义的字段，其余（PD 排名 / DD / 杠杆 / 波动率）都是**风险度量而非收益预测**。⇒ 印证旧记忆「2Y 由字段定」：风险度量类字段在 DEU 无论怎么变换几何都出不了 S。
4. **`leverage` 的 2Y = −1.04 是全战役最差 2Y**：杠杆反向在 DEU 是**反向有效且近年来彻底反转**（2014–2021 有效、2022–2023 崩）。与 sentiment33 的「S/2Y 符号相反」同型，属**半程有效信号**，按既有口径判死。
5. **M4 是唯一「sub_u 达标」的件**（0.45 vs 闸线 0.474×0.90=0.43）—— 但 S 0.90 离 1.58 太远，无推进价值。

---

## 三、★★★ 跨波元规律修订：预加工字段 × 横截面活性 双条件

Wave 17 沉淀的「只选平台预加工字段」（percent/score/rank/ratio/index/rating/relative/normalized/change）在 Wave 18/19 被**部分推翻**：

| 数据集 | 字段类型 | 是否满足「预加工」判据 | 实测 S 上限 | 判决 |
|---|---|---|---:|---|
| model238 | `mdl238_*_rank`（rank 1–100，cov 1.0） | ✅ 是 | 1.16 | 判死 |
| model28 | `*_global_rank` / `*_industry_rank`（cov 1.0） | ✅ 是 | **0.02** | 判死（字段退化） |
| predictive_starmine | `mean_estimate_change_pct_*`（**change percent**） | ✅ 是 | 1.70 | **出货 2 颗** |
| analyst93 | `anl93_recprofitabilityprev_estimator_profitability2`（评分） | ✅ 是 | 1.59 | **出货 1 颗** |
| shortinterest3 | `shrt3_bar`（1–10 评级） | ✅ 是 | 1.59 | **出货 1 颗** |

**修正后的双条件判据（选集第一道筛，取代旧的单条件）**

```text
条件 A（形式）：字段名/描述含 percent / score / rank / ratio / index / rating / relative / normalized / change
条件 B（活性）：该字段在目标区域内**跨截面上真的在动**。
```

**条件 B 的廉价检验法（新增，成本 = 1 条 alpha）**：
用一个最朴素的几何打探针 —— `group_rank(ts_mean(F, 22), industry)`（2 个算子）。

- `S ≥ 1.0` ⇒ 字段有活性，进入深挖（异窗骨架 / 双腿 / 逆方差…）。
- `0.3 ≤ S < 1.0` ⇒ 弱活性，只值得试 1–2 个最强骨架（异窗 132/11），不成就封盘。
- `|S| ≤ 0.05` ⇒ **字段退化**（近常数），**立即封盘整个字段族**，一条都不要再加。
- `S` 为负且 |S| 大 ⇒ 方向反了，反向即正信号，正常处理。

**为什么这条重要**：Wave 18 用了 10 条模板才确认 model238 无料，Wave 19 用了 10 条才确认 model28 的 rank 族退化。若先前置 1 条探针，两波可省 18 条回测（≈72 分钟平台队列）。**从下一波起，每个新数据集先派 1–2 条朴素探针，不直接上 10 模板。**

---

## 四、当前交付状态（不变）

**合格（全闸通过）6 颗，全 UNSUBMITTED**：

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | prod | 严格 ATOM |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | SENTIMENT | 2.05 | 1.71 | 2.53 | 0.147 | 0.6935 | ✗ 双集 |
| 2 | E56pROb9 | model216 + predictive_starmine | MODEL | 1.79 | 1.70 | 2.03 | 0.067 | 0.6859 | ✗ **违禁混 MODEL+MODEL** |
| 3 | QPvzNNGG | predictive_starmine | MODEL | 1.70 | 1.30 | 2.18 | 0.155 | 0.6777 | ✓ |
| 4 | LLMzYrZe | predictive_starmine | MODEL | 1.61 | 1.16 | 1.69 | 0.153 | 0.6697 | ✓ |
| 5 | MPY9VNY9 | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.036 | 0.5986 | ✓ |
| 6 | QPv6jLvX | analyst93 | ANALYST | 1.59 | 1.52 | 2.01 | 0.0411 | 0.6615 | ✓ |

严格单数据集 ATOM = **4 颗**；剔除违禁 E56pROb9 后合格件 = **5 颗**。

---

## 五、已判死数据集计数更新

- 有数据（cov>0）且已开波判死/判弱：**43 个**（本段 +2：model238 / model28）
- cov=0 判死：**44 个**
- 累计判死：**87 个**

---

## 六、剩余候选（未开波）

| 数据集 | cov | 字段数 | ac | 备注 |
|---|---:|---:|---:|---|
| **model30** | 0.5694 | 14 | 179 | StarMine SmartEstimate EPS，`surprise_prediction_*` 是偏离**百分比** ✅；**Wave 20 已派发** |
| pv109 | —— | —— | —— | PV 塔，需先查字段是否含预加工量 |
| institutions4 / institutions1 | —— | —— | —— | 机构持仓，与 model238 同族风险高 |
| order_book_imbalance | —— | —— | —— | 微观结构量，❌ 类（计数/金额）风险高 |
| stock_cluster_dl | —— | —— | —— | 聚类标签，`_class` 型分辨率低 |
| model313 / model262 / model182 / model162 / model140 / model144 | —— | —— | —— | 未勘察 |
| other545 | —— | —— | —— | 未勘察 |

---

## 七、Wave 20 设计（model30 · StarMine SmartEstimate EPS 预测）

数据集：cov **0.5694** / 14 字段全 MATRIX / ac 179。核心 ✅ 字段 `star_new_eps_surprise_prediction_{12m,fq1,fq2,fy1,fy2}`（SmartEstimate 相对共识均值偏离**百分比**；`fq1` ac 3/uc 2、`fq2` ac 0/uc 0 **近乎 virgin**）；原始 EPS 水平 `star_new_eps_smart_estimate_*` 需相除归一化；`star_new_eps_analyst_number_*` 是计数 ❌。

| # | 模板 | 表达式 |
|---|---|---|
| M1 | 水平（**探针**） | `group_rank(ts_mean(star_new_eps_surprise_prediction_12m, 22), industry)` |
| M2 | 异窗 132/11（★第五次验证） | `group_rank(add(rank(ts_mean(...,132)), rank(ts_mean(...,11))), industry)` |
| M3 | 期限结构 FY1−FY2 | `group_rank(subtract(ts_mean(_fy1,22), ts_mean(_fy2,22)), industry)` |
| M4 | ★论坛逆方差（第 2 次真正检验） | `ts_decay_linear(divide(group_rank(F,industry), add(0.001, multiply(ts_std_dev(F,22), ts_std_dev(F,22)))), 30)` |
| M5 | 幅度 × 覆盖广度 multiply | `group_rank(ts_mean(multiply(rank(_fy1), rank(star_new_eps_analyst_number_fy1)),22), industry)` |
| M6 | 预期修正动量 ts_delta 66 | `group_rank(ts_delta(ts_mean(_12m,22),66), industry)` |
| M7 | 预期 EPS 增长率 | `group_rank(ts_mean(divide(star_new_eps_smart_estimate_fy2, star_new_eps_smart_estimate_fy1),22), industry)` |
| M8 | 低覆盖溢价（反向计数） | `-group_rank(ts_mean(star_new_eps_analyst_number_fy1,22), industry)` |
| M9 | 三腿广度（幅度+期限+增长） | `group_rank(ts_mean(add(add(rank(_12m), rank(_fy1)), rank(divide(eps_fy2, eps_fy1))),22), industry)` |
| M10 | 非线性 signed_power 3 | `group_rank(ts_mean(signed_power(_fy2, 3),22), industry)` |

派发批次：`3dE4AC15657mc32vveAFtm6`

**预判**：`surprise_prediction` 与已出货的 predictive_starmine `mean_estimate_change_pct` 同属「分析师预期偏离百分比」族，**互相关可能偏高**。若 M1 探针 S≥1.0，收割后必须立刻跑 `compute_mutual_correlation` 对 QPvzNNGG / LLMzYrZe 验证，不达标即视为同颗换皮。
