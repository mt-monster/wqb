# DEU ATOM 战役 · Wave 20/21/22 判决记录（2026-11-12 续）

> region=DEU / universe=TOP500 / delay=1 / SUBINDUSTRY / decay 4 / trunc 0.08 / 2014-01-01~2023-12-31
> 硬闸：S≥1.58 · F≥1.0 · 2Y≥1.58 · 0.01≤TO≤0.7 · sub_u≥0.474×S · RA失败=0 · self<0.7 · prod<0.7

---

## 一、Wave 20：`model30` StarMine SmartEstimate EPS 预测 → **判弱（保留为增量腿候选）**

批次 `3dE4AC15657mc32vveAFtm6`，10/10 REJECT（但**指标结构是弱数据集里最好的**）。

数据集：cov **0.5694** / 14 字段全 MATRIX / ac 179。核心 ✅ 字段 `star_new_eps_surprise_prediction_{12m,fq1,fq2,fy1,fy2}`（SmartEstimate 相对共识均值偏离**百分比**）；原始 EPS 水平 `star_new_eps_smart_estimate_*`；计数 `star_new_eps_analyst_number_*` ❌。

| # | 模板 | alpha | S | F | **2Y** | TO | **sub_u** | failed |
|---|---|---|---:|---:|---:|---:|---:|---:|
| M1 | 水平 `surprise_prediction_12m` 22 | YP1Y25JJ | 0.77 | 0.48 | 1.16 | 0.0573 | 0.61 | 3 |
| M2 | 异窗 132/11 | d5WvEOvg | 0.84 | 0.55 | 1.01 | 0.0545 | 0.56 | 3 |
| M3 | 期限结构 FY1−FY2 | e75Ed9EN | −0.06 | −0.01 | **−0.89** | 0.0651 | −0.21 | 4 |
| M4 | ★逆方差（w22/decay30） | bl6AoRKl | 0.77 | 0.48 | 1.00 | 0.0502 | 0.63 | 4 |
| M5 | 幅度 × 覆盖广度 multiply | O0Agbr2b | 0.33 | 0.13 | 1.16 | 0.0497 | 0.06 | 4 |
| M6 | 预期修正动量 ts_delta 66 | LLM3g929 | 0.23 | 0.08 | 0.24 | 0.0731 | −0.11 | 4 |
| M7 | 预期 EPS 增长率 fy2/fy1 | YP1Y25O6 | −0.07 | −0.01 | −0.38 | 0.0379 | −0.22 | 4 |
| M8 | 低覆盖溢价 `-analyst_number_fy1` | bl6AoRgM | 0.11 | 0.03 | −0.68 | 0.0350 | 0.04 | 4 |
| M9 | 三腿广度（幅度+期限+增长） | xAr5PYob | 0.88 | 0.57 | 1.08 | 0.0570 | 0.50 | 3 |
| M10 | 非线性 `signed_power(_fy2,3)` | gJeLRQ50 | **0.98** | 0.68 | **1.28** | 0.0606 | **0.74** | 3 |

**五结论**

1. **★ 2Y 上限 1.28 = 全战役所有「弱数据集」里最高**（对比 model216 1.01 / dl_riskfree 1.22 / shortinterest3 0.99）。10 条里 5 条 2Y > 1.0。**该数据集的价值在 2Y 而不在 S。**
2. **★ 首个 sub_u 达标的弱数据集**：gJeLRQ50 sub_u **0.74** vs 闸线 0.474×0.98=0.465（超 59%）；全波 8/10 条 sub_u 达标。对比 model238（sub_u 只到闸线的 43–72%）这是质的差别 ⇒ **信号在大票小票上都成立，是真截面 alpha 而非规模依赖伪信号**。
3. **★ `investability_sharpe` 系统性高于 `sharpe`**：YP1Y25JJ 1.11 vs 0.77、gJeLRQ50 1.19 vs 0.98、xAr5PYob 1.03 vs 0.88 ⇒ **在可投资子集上信号更强**，与 model238（investability 全面低于 sharpe）完全相反。这是「真信号」的又一个标记。
4. **期限结构族第 5 次证伪**（M3 S −0.06 / 2Y **−0.89**）。连同 model216(FY1−FY2 0.49)、model28(M10 0.25)、sentiment33(净极性差)、analyst93(分歧度 0.21) ⇒ 该几何在 DEU **已 5 次全灭，彻底封盘**。
5. **非线性放大是有效杠杆**：gJeLRQ50 = `signed_power(_fy2, 3)` S 0.98 > 水平 0.77（+27%），是全波最好。**`signed_power(·,3)` 值得作为通用 S 放大器**（p>1 放大尾部、p<1 压缩）。

**角色判定**：model30 = **增量腿**（同 model216 / model264），角色 = 提 2Y 不提 S。但因 model30 属 MODEL 塔，与 predictive_starmine（MODEL）组合**违反禁混集合** ⇒ **本战役无法使用**。

---

## 二、★★★ Wave 21：`predictive_starmine` 换不相交字段对 → **判死（本段最重要的负面结论）**

批次 `1rwrMognO4SW9nCFk5HZK8m`，10/10 REJECT。

**动机**：该集 631 字段中有 120 个 `mean_estimate_change_pct_*` + 61 个 `predicted_surprise_*`，而已交付件只用了 **3 条腿**（`f12m_earnings_14d_4` / `f12m_ebitda_90d_3` / `predicted_surprise_f12m_ebitda_4`）。按「同数据集换不相交字段对可出多颗 ATOM」的既有经验，本波全部改用 **fq1/fq2/fy1/fy2 期限 + revenue 口径**，与已交付件腿集合**零交集**。

| # | 模板 | 字段 | alpha | S | F | 2Y | sub_u |
|---|---|---|---|---:|---:|---:|---:|
| M1 | 水平探针 | `predicted_surprise_pct_fq2_earnings_5` | npvrZQ18 | **0.27** | 0.10 | 0.16 | 0.40 |
| M2 | 异窗 132/11 | 同上 | omEZ3r1J | 0.36 | 0.14 | 0.95 | 0.27 |
| M3 | 双腿 add 22 | `fq2_revenue_60d_7` + `pct_fy2_revenue_4` | O0AgbV1d | 0.07 | 0.01 | −0.88 | 0.00 |
| M4 | 双腿异窗交叉 | 同上 | 58EYae8N | 0.34 | 0.13 | −0.57 | 0.11 |
| M5 | ★逆方差 | `pct_fq2_earnings_5` | kqN91OqK | **0.06** | 0.01 | −0.01 | 0.06 |
| M6 | 动量 ts_delta 66 | `fq1_revenue_60d_5` | d5WvEo5v | 0.38 | 0.15 | 0.07 | 0.39 |
| M7 | 时序 z 252 | `pct_fq2_earnings_5` | 78LlaMW5 | 0.17 | 0.06 | 0.25 | 0.22 |
| M8 | multiply 双确认 | `fq2_revenue_60d_7` × `pct_fy2_revenue_4` | 1YN0aP96 | −0.04 | −0.01 | −0.95 | −0.16 |
| M9 | 三腿广度 | `fq1_revenue_60d_5`+`pct_fy1_earnings_5`+`pct_fq2_earnings_5` | QPv62gJG | **0.76** | 0.42 | 0.54 | 0.80 |
| M10 | 非线性 | `signed_power(pct_fy1_earnings_5,3)` | YP1Y2Jro | 0.60 | 0.28 | 0.12 | 0.29 |

**对照（同数据集、同几何、只用已交付的 f12m 腿）**：QPvzNNGG **S 1.70** / LLMzYrZe **S 1.61**。

**四结论**

1. **★★★ S 从 1.70 掉到 0.27（水平探针）—— 同一数据集、同一算子几何、只换字段，S 蒸发 84%。** 这不是「新字段弱」，是**新字段无信号**。
2. **★★★ 结论：`predictive_starmine` 也只有 1 个可交易信号维度** —— 即 **f12m（forward 12-month）业绩预期修正 + 其超预期**这三条腿。全部 `fq1/fq2/fy1/fy2` 期限（200+ 字段）与 revenue 口径 **在 DEU 全部无效**。
   机理：DEU TOP500 的卖方覆盖集中在年度 12 个月前瞻口径；季度（fq）与更远年度（fy2）口径覆盖稀疏、含噪，横截面上不构成定价信息。
3. **★ 推翻「换不相交字段对可出多颗 ATOM」的普适性**：该经验来自 KOR `analyst10`（利润/规模/股东回报/预测四个**语义族**互不相交）。本波只在**同一语义族（分析师预期）内换期限**，属「结构位移不足」⇒ **判据应升级为：换字段必须是换「语义族」，不能只换「期限/口径」**。
4. **逆方差模板第 3 次失效**（M5 S 0.06）。三次的失败原因一致：**分子本身无信号**（wave19 的 pd_pct 水平、wave21 的 pct_fq2_earnings_5）。⇒ 逆方差不是提 S 工具，只是**在已有 S 的件上做 2Y 平滑**的候选杠杆，用之前必须先确认分子单独出件 S ≥1.2。

---

## 三、★★★ Wave 22：`sentiment27` 非 relpopularity 字段 → **判死**

批次 `eGPuCgJk58Y9PnGR1LNoXH`，10/10 REJECT。

数据集：cov **0.9022**（全区覆盖最高之一）/ 18 字段，其中 13 个可用 VECTOR。已交付 mLox6Mg2 只用 `snl27_relpopularity08`。本波全部改用**其余字段**（与已交付件腿集合零交集）。

| # | 模板 | 字段 | alpha | S | F | 2Y | sub_u |
|---|---|---|---|---:|---:|---:|---:|
| M1 | 水平探针 | `snl27_top50pctrankingavg` | ZYQNjY9x | −0.12 | −0.03 | −0.40 | −0.62 |
| M2 | kurtosis 反向 | `snl27_kurtosis` | Jjernjkx | −0.34 | −0.13 | −0.15 | 0.17 |
| M3 | skewness 反向 | `snl27_skewness` | j2YOn2JO | **−0.67** | −0.35 | −0.72 | −1.13 |
| M4 | 异窗 132/11 | `top50pctrankingavg` | RREPNRwn | −0.12 | −0.03 | −0.43 | −0.51 |
| M5 | ★逆方差 | `top50pctrankingavg` | O0Agn0Xp | −0.26 | −0.15 | −0.42 | −0.02 |
| M6 | multiply 双确认 | `top50pctrankingavg` × `kurtosis` | 0mY5Am26 | −0.18 | −0.05 | 0.28 | −0.57 |
| M7 | 动量 ts_delta 66 | `top50pctrankingavg` | GrW9nrjP | 0.10 | 0.02 | −0.88 | −0.35 |
| M8 | 时序 z 252 | `kurtosis` | LLM3nLon | −0.29 | −0.09 | −0.67 | 0.33 |
| M9 | 三腿广度 | `top50pctrankingavg`+`kurtosis`+`avgranking` | P0oKn0Lx | −0.10 | −0.02 | −0.13 | −0.48 |
| M10 | 非线性 | `signed_power(skewness,3)` | pwd3nw2q | **0.57** | 0.27 | 0.43 | **0.91** |

**对照（同数据集、只用已交付字段）**：mLox6Mg2（`snl27_relpopularity08` + `snt7_all_languages_views`）**S 2.05** / 2Y 2.53。

**四结论**

1. **★ 10 条里 9 条为负**（S −0.67 ~ +0.57）。同一数据集、cov 0.9022、换字段后整体翻负 ⇒ `sentiment27` 也**只有 1 个可交易信号维度** = `relpopularity08`（**预加工复合相对热度评分**）。
2. **★★★ 这条最锋利：`relpopularity08` 有效（2.05）而 `top50pctrankingavg`/`avgranking`/`kurtosis`/`skewness` 全部无效（−0.67~0.57）** —— 它们是**同一个底层数据的四种加工方式**：
   - `relpopularity08` / `relpopularity1` = **复合相对热度评分**（平台跨域加权合成）✅
   - `top50pctranking` / `top75pctranking` / `avgranking` / `topranking` / `snt27_rank` = **原始 Tranco 排名或其分位数截断** ❌
   - `kurtosis` / `skewness` = **分布形状矩** ❌
   ⇒ **「预加工 × 活性」双条件判据被强化为三条件：预加工 ✅ × 横截面活性 ✅ × 平台已做跨域/跨源合成 ✅。** 第三条件是本波新发现的：原始排名即使做了分位数归一化仍然无效，因为「域排名的分位数」不含跨域聚合信息。
3. **分布形状矩（kurtosis/skewness）第 4 次证伪**：M2 −0.34 / M3 −0.67 / M8 −0.29 / M10 仅 0.57。连同短借费率分散度、analyst93 分歧度、model28 层级差 ⇒ **所有「离散度/形状」几何在 DEU 一律封盘**。
4. **逆方差第 4 次失效**（M5 −0.26），同样因分子无信号。

---

## 四、★★★ 本段总结出的「数据集容量判据」（跨波元规律，取代旧口径）

把 Wave 15–22 全部 40 条 alpha 与已交付件并置，得到一条能解释**全部** 87 个数据集判死原因的判据：

> **在 DEU（TOP500 小宇宙）上，一个数据集通常只有 1 个可交易信号维度；且该维度必须是「平台已做跨域/跨源合成的预加工评分或百分比」。**

| 数据集 | 唯一有效维度 | 同集其余字段实测 |
|---|---|---|
| predictive_starmine | `f12m` 预期修正百分比 + 超预期（3 腿） | 200+ 个 fq/fy/revenue 字段 S ≤0.76 |
| analyst93 | `profitability2`（推荐盈利性评分） | 30+ 字段 −0.16~1.36，内部互相关 0.89–0.99 |
| shortinterest3 | `shrt3_bar`（1–10 评级） | 24 个原始借券字段 S −0.38~0.61 |
| sentiment27 | `relpopularity08`（复合相对热度） | 12 字段 S −0.67~0.57 |
| sentiment7 | `all_languages_views` | 仅 2 个可用字段，`views` 同源 |
| model238 | 无（最接近的是 `global_rank` S 1.16） | 22 字段全线 sub_u 不足 |
| model28 | 无（7 个 cov1.0 rank 字段 **S≈0.00**） | 退化字段 |
| model30 | 无（最好的 `signed_power(_fy2,3)` S 0.98） | 2Y 1.28 尚可，S 不足 |
| model216 / model264 / dl_riskfree | 无 | 2Y 上限 1.01 / — / 1.22 |

**推论（决定后续排期）**：
- 严格单数据集 ATOM 在 DEU 的**理论上限 ≈ 5–6 颗**（每个有效数据集 1 颗），而非 10 颗。
- 当前已有 4 颗严格 ATOM（QPvzNNGG / LLMzYrZe / MPY9VNY9 / QPv6jLvX），其中 QPvzNNGG 与 LLMzYrZe **共用腿**（self 0.678，只差一线），实质是 1 颗 + 1 个近重复。
- **要凑到 10 颗，只有两条路**：(a) 找到 5–6 个全新的「有唯一有效维度」数据集（命中率当前 0/46）；(b) 放宽「单数据集」口径，改用双数据集组合。

---

## 五、在飞（本段派发）

| 波次 | 数据集 | 批次 | 核心机制 |
|---|---|---|---|
| **Wave 23** | `institutions6`（cov **1.0** / 11 字段 / ac **270**） | `1HH5N7aFq5gBavw1gFfWRhpw` | 披露计数→**广度比**（buyers/holders）；含 KOR 已验冠军骨架 `trade_when(ts_arg_max(HOLDERS,90)<33, signed_power(ts_quantile(BUYERS/ts_mean(HOLDERS,72),840,gaussian),1.6), -1)` |
| **Wave 24** | `analyst_factor_signals`（cov 0.60 / 108 字段 / ac **1575**） | `1ViKkJc9W4QobFfiJbOFxDu` | `*_revision_magnitude`（缩放修正幅度）+ `*_estimate_change_3mo`（3 个月预期变化）；三口径 eps/revenue/netprofit |

**为什么挑这两个**：`deu_ds_cov.csv` 里 `alphaCount`（平台已有 alpha 数）是「该集有信号」的最强旁证 —— institutions6 是 270/11 字段 = 24.5 颗/字段，analyst_factor_signals 是 1575/108 = 14.6 颗/字段，均远高于已判死集的个位数。**选集新口径：优先 ac/字段数 > 10 的数据集。**
