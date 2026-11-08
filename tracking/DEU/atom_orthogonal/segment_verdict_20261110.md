# DEU ATOM 战役 — 2026-11-10 段判决书

> region 固定 DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF / pasteurization ON / unitHandling VERIFY / maxTrade OFF
> 硬闸：S ≥ 1.58、F ≥ 1.0、2Y ≥ 1.58、0.01 ≤ TO ≤ 0.7、sub_u ≥ 0.474×S、RA failed = 0、self < 0.7、prod < 0.7

---

## 一、本段判死的三个数据集

### 1.1 `predictive_starmine` — arm_* 推荐评分族（批次 `11HjrjgT94vvbuLPsrqn67h`，10/10 REJECT）

| alpha | 表达式 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| pwd3rmpo | `trade_when(arm_new_activity_flag_2>0, arm_score_change_7d_3, 0)` | **0.50** | 0.20 | **1.36** | 0.1772 |
| LLM3aW3M | `group_rank(arm_global_rank_score, sector)` | 0.39 | 0.16 | −1.10 | 0.0819 |
| JjerEq2E | 三分量 add（rec+rev+pref_earnings） | 0.36 | 0.15 | −1.25 | 0.0873 |
| O0AgPO2R | `country_rank_score − global_rank_score` | 0.25 | 0.06 | 0.00 | 0.2675 |
| gJeLO6dl | `group_rank(arm_score_change_30d_4)` | 0.04 | 0.00 | 0.07 | 0.2513 |
| KPJZd3Z1 | `rec_component − revenue_component` | −0.05 | −0.01 | −0.91 | 0.1222 |
| qMLVr8wA | `group_rank(arm_score_5pt_scale_2)` | −0.42 | −0.18 | −1.01 | 0.0922 |
| N1N8m08o | `7d − 90d` 评分变化差 | −0.36 | −0.08 | −0.56 | 0.3487 |
| E56xW1LR | `group_rank(arm_score_change_7d_3)` | −0.48 | −0.10 | −0.53 | 0.4745 |
| 2rAezMeJ | 7d+30d+90d 三分量 add | −0.07 | −0.01 | 0.35 | 0.3084 |

**判死依据**：`arm_*` 族（ARM 分析师推荐评分）在 DEU 无信号，天花板 S 0.50。
**关键否证**：`arm_global_rank_score` / `arm_score_change_{1d,3d,60d}` 等 **uc0 / ac0 的 virgin 字段依然 S 0.36–0.39** ⇒ 「零拥挤」不等于「有信号」，覆盖率/拥挤度只能作下限筛。

### 1.2 `predictive_starmine` — analyst 升降级计数族（批次 `Waq6LgTi5hqaQMj4FbScNY`，10/10 REJECT）

| alpha | 表达式 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| E56xWJkm | 14d+90d 双视界净值比 add | **0.79** | 0.44 | **1.46** | 0.1280 |
| LLM3aJg1 | `upgrade_60d − downgrade_60d` | 0.72 | 0.39 | 0.59 | 0.1053 |
| VkxejJ2M | 60d 净值比 `(up−dn)/(up+dn+1)` | 0.70 | 0.38 | 0.59 | 0.1060 |
| 2rAezdJP | 60d 净值比 @bucket(upgrade_7d) 中性化 | 0.65 | 0.35 | 0.85 | 0.1161 |
| 78Llb9xQ | `group_rank(analyst_revisions_score_2)` | 0.41 | 0.17 | −1.11 | 0.0824 |
| gJeLOpmg | `ts_av_diff(analyst_revisions_score_2, 66)` | 0.32 | 0.11 | 1.14 | 0.1367 |
| xAr58geN | `ts_rank(analyst_revisions_score_2, 252)` | 0.30 | 0.10 | 1.13 | 0.1234 |
| N1N8m9AX | 14d 净值比 | 0.22 | 0.05 | 0.51 | 0.2547 |
| JjerEKgA | `upgrade_60d / (downgrade_60d+1)` | 0.09 | 0.02 | 1.02 | 0.0838 |
| j2YORmnQ | `rank(7d 净) − rank(90d 净)` | −0.75 | −0.37 | −1.33 | 0.1569 |

**判死依据**：升降级计数族天花板 S 0.79，距 1.58 缺 50%。
⚠️ `j2YORmnQ` 反向说明 **短期(7d)净值 − 长期(90d)净值 是反向信号**（短视界过热 → 反转），而 14d+90d 同向叠加是正向（`E56xWJkm` S0.79 / 2Y1.46 是本族最优）。

### 1.3 ★ `predictive_starmine` 整体结论（重要战略收敛）

两条辅助族（arm 评分、analyst 计数）接连全灭后，可以判定：
**`predictive_starmine` 的威力几乎全部来自 `mean_estimate_change_pct_*` + `predicted_surprise_*` 这一对结构**（已交付 QPvzNNGG S1.70 / LLMzYrZe S1.61 / E56pROb9 S1.79）。
- 其余 4 个腿族（analyst count / arm / ep_yield / actual）信号羸弱。
- ⇒ **EP-ACTUAL-A 预检全绿但那 2 个族（ep_yield 估值 + actual 实绩）大概率同弱，降级不派**。
- ⇒ 不要再在 ps 上找第 3、4 颗互不共腿的 ATOM；该集容量实质为 2 颗（已交付）。

### 1.4 `model36` SmartRatios 信用风险族（批次 `1RjoIb4qV4DAbJ6bE5SZipZ`，10/10 REJECT）

| alpha | 表达式 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| xAr58Y3N | `ts_mean(5因子分位和, 22)` 5-factor 复合 | **0.53** | 0.28 | −0.88 | 0.0249 |
| 0mY53Rrv | `ts_rank(star_sr_global_rank_d1, 252)` | 0.52 | 0.26 | 0.41 | 0.0960 |
| vR1PMk2A | `ts_mean(credit_risk_* 4因子和, 22)` 替代族 | 0.51 | 0.27 | −0.68 | 0.0247 |
| N1N8mQaX | `ts_mean(star_sr_global_rank_d1, 22)` | 0.50 | 0.26 | −0.68 | 0.0244 |
| **mLoQRgmx** | **`group_rank(star_sr_global_rank_d1, sector)` 裸水平对照** | 0.46 | 0.23 | −0.75 | **0.0354** |
| 6XdNVrA7 | `ts_decay_linear(star_sr_global_rank_d1, 22)` | 0.47 | 0.23 | −0.71 | 0.0263 |
| 3qoJr9XN | `industr_rank − global_rank` 分位差 | 0.34 | 0.14 | 0.08 | 0.0721 |
| QPv6k3Kp | `star_sr_global − credit_risk_leverage` | 0.22 | 0.07 | −0.17 | 0.0275 |
| d5WvVObY | `star_sr_profitability − star_sr_leverage` | 0.11 | 0.03 | 0.70 | 0.0231 |
| j2YOR38Z | `ts_av_diff(star_sr_global_rank_d1, 66)` | 0.11 | 0.03 | −0.87 | 0.1142 |

**判死依据**：信用风险/违约概率因子在 DEU 无预测力，天花板 S 0.53，且 2Y 多为负（−0.68 ~ −0.88）。
**★ 有价值的副产物（修正既有假设）**：裸水平对照 `mLoQRgmx` 的 **TO = 0.0354**，证明 `_d1` 后缀字段是**真正的慢变量**——model106 那种「直接 rank 必产生 TO 0.80」的问题**不适用于所有 `_d1` 字段**，不能一概而论。model106 顶格换手是其评分字段被日频重算的个体问题，不是 `_d1` 的共性。

---

## 二、★ `model264` 字段画像（380 字段，DEU 覆盖率最高的数据集）

调用：`get_datafields(region=DEU, delay=1, universe=TOP500, dataset_id=model264, filter_sharpe=false)` → 380 字段 / 8 页。

### 2.1 结构：三层命名族

| 族 | 数量 | 语义 | coverage | 说明 |
|---|---:|---|---:|---|
| `mdl264_<X>_class` | **95** | 预测趋势类别枚举（**1=跌 / 2=中性 / 3=涨**） | **1.0** | argmax 结果，仅 3 值 |
| `mdl264_<X>_l1` | 36 | P(未来趋势为跌) | 0.9962–0.9966 | 连续概率 |
| `mdl264_<X>_l2` | 36 | P(中性) | 同上 | 连续概率 |
| `mdl264_<X>_l3` | **36** | **P(涨) = 模型预测上涨概率** | 同上 | ★ 主力信号源 |
| `mdl264_1l_<X>` | 59 | 早期「1 层」版，仅 P(跌) | 0.9938–0.9966 | 与 `_l1` 同义但覆盖的指标不同 |

**值域全部落在 0~1**（概率）。

### 2.2 具备完整 `l1/l2/l3` 的 36 个指标，按经济学族分组

**① 分析师预期修正族（15）** — `es_*`，最高信号先验
```
es_ebit_{fy1_d1m, fy1_r1m, ntm_r1m}
es_ebitda_{fy1_d1m, fy1_r1m, ntm_r1m}
es_roe_{fy1_d1m, fy1_r1m, ntm_r1m}
es_sale_{fy1_d1m, fy1_r1m, ntm_r1m}
es_vol_r1m  es_disp  es_sur_decay
```
> 语义：`*_l3` = 模型预测「FY1 EPS/EBITDA/ROE/Sales 修正方向」将上行的概率 ⇒ **概率化的修正动量**。
> `d1m` = 1M diffusion（升降比例扩散），`r1m` = 1M revision（修正幅度），`ntm` = NTM（未来 12 个月）。

**② 估值质量族（10）**
```
bookp  bookp_fy1  psale  div_payout  divyld_bb
payable_to  eps_disp  tstk  ext_fin_noa  fincf
```

**③ 风险流动性族（7）**
```
amihud（非流动性）  abn_volm（异常成交量）  vol_vo_p_1m（量价比波动）
lottery（MAX 彩票因子）  hilomid  float_to（流通换手）  eps_sur_decay
```

**④ 新闻情绪族（3）**
```
news_abno_sent_1d（异常情绪）  news_abno_vol_1d（异常新闻量 z）  news_sentvol_1d（新闻条数）
```

**⑤ 技术指标族（互补，主要在 `_class` 与 `_1l` 中）**
```
macd  trix  cci  clv  cmf  co  dpo  emv  atr  adl  mfi  mi  nvi  obv
ppo  pvo  so  tsi  vi  vpt  wr  lottery  ma_15_36  ma_30_75
```

### 2.3 拥挤度
`userCount` 多为 **0–5**，`alphaCount` 多为 **0–62**（最高 `mdl264_1l_57_03_am` ac62）。DEU 侧几乎无人使用。

### 2.4 ★★ 命名坑（已踩一次，整批 10 条全 ERROR）
```
✗ 错：group_rank(es_ebit_fy1_r1m_l3, sector)          → unknown variable
✓ 对：group_rank(mdl264_es_ebit_fy1_r1m_l3, sector)   → valid
```
`get_datafields` 返回的 `id` **已含 `mdl264_` 前缀**，「指标名」只是我剥离后的展示形式。凡 `mdl264_*` 字段一律写全 id。
> 交付的备用件 `wpQYNvZp` / `Vkx3MjW8` 用的是 `mdl264_div_payout_class` / `mdl264_amihud_class`（带前缀），所以能跑。

---

## 三、★★ 论坛方法论：model264 的正确模板（可直接复用）

**帖子**：《理解模板与数据集：我将搜索空间缩小10万倍！》TL53163，130 赞 27 评，2025-08-27
`https://support.worldquantbrain.com/hc/en-us/community/posts/34478018977687`

### 3.1 核心模板
> 「mdl264 数据集的字段都是对于未来趋势的预测，模板的思路是**将多个预测信号累加，得到一个更强、更稳定的信号**。」

### 3.2 五条硬结论

1. **只用 `add`，禁止直接 `multiply` 三数相乘**
   值域 0~1，三数相乘结果差距最高可达**千倍** ⇒ 权重集中、CONCENTRATED_WEIGHT 风险。若必须用 `multiply`，要先套 `rank` / `zscore`。

2. **同类型字段相加才有意义**
   字段分四类预测（涨 / 跌 / 中性 / …），**跨类型相加无意义**。必须先按 description 关键词分类再组合。
   ⇒ 落地：`_l3`（P涨）只能与 `_l3` 相加，不能与 `_l1`（P跌）直接相加；`l3 − l1` 属于「净方向」变换，需明确当作另一种模板。

3. **同类字段相关性 > 0.7 ⇒ 每类只需 1–3 个代表字段**
   219 个下行趋势字段经 AI 按经济学维度分成 **13 类**，每类保留 3 个代表（按裸字段回测 Sharpe 排序），得 39 字段 ⇒ C(39,3)=9139 个表达式（原始 C(2036,3)≈14 亿）。

4. **先裸字段回测筛 |S| ≥ 0.5**
   弱字段 = 该预测本身不准，直接剔除（2036 → 707 字段）。作者另注：现在回测受限，这一步可跳过，改用 description 分类。

5. **产出率参考**：1 万次回测 → **500+ 可交（未相关性剪枝）**，其中 **2 颗 RA**。

### 3.3 尚未被验证的线索（评论 AK76468）
> 「或许将**枚举类型的趋势预测字段用于分组**也是个不错的选择呢！」

`_class` 字段是 1/2/3 枚举，天然适合作 `group_neutralize` / `group_rank` 的 group 轴，或 `bucket()` 的输入。**本次 MODEL264-B 首次实测该几何。**

### 3.4 风险提示（评论 DS48533，需监控）
- 「虽然是同数据集，但会不会也算混信号」⇒ 全部腿来自单一数据集（ATOM），不占塔混配额，形式上合规；但 OS 稳定性仍需观察。
- 「正趋势 − 负趋势 + 正趋势」「正×正×正」「负×负×正」等变体值得试。

---

## 四、MODEL264 批次模板库（20 个结构互异模板，满足 ≥10 硬约束）

### 4.1 MODEL264-A `DzD2ZaAZ4EeciAddYhVxxB` — 4 腿族平衡探测

| # | 模板 | 族 | 结构 / 矩 | 算子数 |
|---|---|---|---|---:|
| 1 | `group_rank(_es_ebit_fy1_r1m_l3, sector)` | REV | 单腿水平（基线） | 2 |
| 2 | 4 腿 `add` 共识复合 | REV | 水平·同类型累加（论坛正典） | 5 |
| 3 | 4 腿 `(l3−l1)` 净方向累加 | REV | 方向矩（期望类别） | 9 |
| 4 | `ntm_l3 − fy1_l3` 视界价差 | REV | 跨视界一阶差 | 4 |
| 5 | 4 腿估值 `add` 复合（bookp/bookp_fy1/psale/divyld_bb） | VALUE | 水平·跨指标 | 5 |
| 6 | `ts_av_diff(3 腿估值和, 66)` | VALUE | 时序一阶差分（动量） | 3 |
| 7 | `amihud_l3 − vol_vo_p_1m_l3` | RISK | 跨机制价差（非流动性 vs 波动） | 3 |
| 8 | `float_to_l3 − lottery_l3` | RISK | 跨机制价差（换手 vs 彩票需求） | 3 |
| 9 | 3 腿新闻 `add` 复合 | NEWS | 水平·同类型 | 5 |
| 10 | `div_payout_l3 − payable_to_l3` | QUALITY | 股东回报 vs 供应链 | 3 |

### 4.2 MODEL264-B `4vN9pv1g14qr9f2KeEeAo32` — 新颖几何（论坛未验证）

| # | 模板 | 结构 / 矩 | 算子数 |
|---|---|---|---:|
| 1 | `group_neutralize(group_rank(es_ebit_fy1_r1m_l3, sector), es_ebit_fy1_r1m_class)` | **枚举 `_class` 作分组轴**（二级中性化） | 3 |
| 2 | `group_rank(es_ebit_fy1_r1m_class, sector)` | 枚举值直接当有序信号 | 2 |
| 3 | 三 `_class` `add` 共识（1/2/3 求和） | 枚举和·离散共识度 | 5 |
| 4 | 三腿 `rank` 和 @ `bucket(rank(es_ebit_fy1_r1m_l3), 0.2)` | 分桶中性化 + 预 rank 防权重集中 | 8 |
| 5 | `trade_when(class > 2, group_rank(l3), -1)` | **条件门控**：模型看涨才交易 | 4 |
| 6 | `trade_when(class < 2, -group_rank(l3), -1)` | 条件门控反向（只空看跌） | 4 |
| 7 | `signed_power(l3−l1, 2)` | 非线性放大（尾部扩张） | 4 |
| 8 | `multiply(l3−l1, es_sale_fy1_r1m_l3)` | 置信度加权交互（非线性·双边） | 5 |
| 9 | `ts_rank(es_ebit_fy1_r1m_l3, 252)` | 时序分位（1 年百分位） | 3 |
| 10 | `group_rank(l3−l1, es_ebit_fy1_r1m_class)` | 净方向 × 枚举分桶 rank | 4 |

---

## 五、DEU 判死数据集累计台账（本段后 +3）

| 数据集 | category | cov | 判死依据 |
|---|---|---:|---|
| `model106` | MODEL | 0.7878 | 10/10 TO=0.8004 顶格，S≤0.62 |
| `dl_riskfree_returns` | OTHER | 0.7147 | 累计 30 条，S 天花板 1.39，eff 天花板 0.34（需 0.40） |
| `news104` | NEWS | 0.9630 | 10 模板全灭，S≤0.49 |
| `analyst44` | ANALYST | 0.5802 | 10 模板全灭，S≤0.34 |
| `analyst48` | ANALYST | 0.7879 | 7 字段全指数级元数据 |
| **`model36`** | MODEL | 0.8488 | **10/10 REJECT，S≤0.53，2Y −0.68~−0.88** |
| `predictive_starmine`（arm 族） | MODEL | 0.7903 | arm_* 10/10，S≤0.50 |
| `predictive_starmine`（count 族） | MODEL | 0.7903 | analyst count 10/10，S≤0.79 |
| `model238` | MODEL | — | 10/10 REVIEW 但 S≤1.26、2Y≤1.15、sub_u/S≤0.39，四闸无法同时满足 |

（此前已判死：other699 / insider_trx_matrix / model53 / pattern_scores / fundamental6 / other532 / news18 / news50 / analyst93 / risk60 / institutions1 / institutions6 / insider_matrix + 13 个 cov=0 数据集）

---

## 六、当前交付状态

**合格 5 颗**（全闸通过、全部 UNSUBMITTED）：

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | self | prod | ATOM? |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | SENTIMENT | 2.05 | 1.71 | 2.53 | 0.147 | 0.030 | 0.6935 | ✗ 双集 |
| 2 | E56pROb9 | model216 + predictive_starmine | MODEL | 1.79 | 1.70 | 2.03 | 0.067 | 0.600 | 0.6859 | ✗ 双集 |
| 3 | QPvzNNGG | predictive_starmine | MODEL | 1.70 | 1.30 | 2.18 | 0.155 | 0.678 | 0.6777 | ✓ |
| 4 | LLMzYrZe | predictive_starmine | MODEL | 1.61 | 1.16 | 1.69 | 0.153 | 0.670 | 0.6697 | ✓ |
| 5 | MPY9VNY9 | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.036 | 0.270 | 0.5986 | ✓ |

严格单数据集 ATOM = **3 颗**，缺口 **7 颗**。
互相关天花板 = **5**（`max_subset_exact=true`），备用池 6 颗数学上无一可加入。

---

## 七、下一步队列

1. **在飞**：MODEL264-A `DzD2ZaAZ4EeciAddYhVxxB` + MODEL264-B `4vN9pv1g14qr9f2KeEeAo32`（两槽满）
2. **高优先备选**：`shortinterest3` 第 2 颗 ATOM — 25 字段中已交付件只用 `shrt3_bar`，剩余 **24 字段全未使用**（8 度量 × 3 变体：`average_loan_duration_days` / `loan_rate_volatility` / `loaned_market_value_usd` / `loaned_share_count` / `max_loan_rate` / `mean_loan_rate` / `min_loan_rate` / `transaction_count`），且 `_p5_d1` 变体覆盖率 0.7833 > base 0.6683
3. **待画像**：`model28`（Structural Credit Risk，cov 0.8105 / 25 字段）/ `news17`（cov 0.7906 / 48 字段）/ `news20`（cov 0.7729 / 46 字段）/ `insider_agg_matrix`（cov 0.5617 / 34 字段）
4. **降级不派**：EP-ACTUAL-A（ps 的 ep_yield + actual 族，按 §1.3 结论）
5. **MODEL238-C/D**：已预检全绿，仅在 model264 全线失败时回退使用
