# DEU ATOM 正交挖掘 · 段 C 台账（2026-11-08）

> 承接 `segment_verdict_20261108b.md`。本段核心事件：**pattern_scores / fundamental6 / other532 三集判死**
> + **发现 `model` category 尚有 45 个数据集、其中 15+ 个高覆盖未测**（策略级转向）。
> 目标不变：DEU 交付 10 颗 ATOM REGULAR；当前合格 5/10（严格单数据集 3/10）。

---

## 一、本段判死清单（3 个目标）

### 1. `pattern_scores`（PV 塔）判死

批次 `y2tyaePx5dEcBzO5M2MuNx`，10 条全 COMPLETE，基线设置（TOP500/D1/SUBINDUSTRY/decay4/trunc0.08）。

| alpha | 模板（经济含义） | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| LLM3LzQM | 上升三角 max−mean（形态强度离散） | −0.11 | −0.02 | −0.07 | 0.2145 |
| e75E7GXd | 上升三角 mean60−mean120（窗口分歧） | **0.09** | 0.02 | **−0.85** | 0.1682 |
| GrW9rz23 | V 型底 − V 型顶（反转 vs 持续） | −0.04 | −0.01 | 0.32 | 0.0883 |
| j2YO2G79 | 上升三角 std（形态不稳定度） | −0.08 | −0.01 | −0.64 | 0.0956 |
| 2rAer635 | 突破缺口 up−down q95 | −0.10 | −0.02 | 0.17 | 0.1987 |
| 1YN0YKrk | 上升三角 dynamic−mean | −0.24 | −0.06 | 0.04 | 0.2228 |
| A1VE1zXl | 普通缺口 up−down（缺口回补） | −0.20 | −0.06 | 0.04 | 0.0872 |
| E56x5z9P | 上行突破缺口 − 下行突破缺口 | −0.17 | −0.04 | 0.10 | 0.1486 |
| 3qoJqPKO | 对称三角 up−down | −0.39 | −0.17 | 0.02 | 0.1091 |
| 6XdNX065 | 下降楔形 − 上升楔形（最强单条） | **−0.46** | −0.18 | −0.07 | 0.1411 |

**prescreen 10/10 REJECT。全部 |S| ≤ 0.46，绝对值最大 0.46。**
即使整体翻符号，上限也只有 0.46，距 1.58 差 1.12。

**判死理由（结构性）**：
- 数据集画像看似极优：coverage **0.9888**、504 字段、ac 仅 **277**、单字段 ac 0–7（大量 virgin）。
- 但 10 个独立形态族（缺口回补 / 楔形 / V 型 / 对称三角 / 上升三角 / 突破缺口）**无一超过 0.5**，
  且方向不一致（6 负 4 正），这是**纯噪声分布**的特征，不是「方向选错」。
- 结论：`pattern_scores` 的 simscore 在 DEU 截面上的**跨股区分度不足**（同类形态相似度对多数票都接近），
  导致 rank 之后近似随机。这是数据生成机制的问题，任何算子几何都补不上。

**⇒ PV 塔在 DEU 仍为 0 颗已提交，且再次确认 PV 类数据集不可用**（此前 techindi_model cov=0、risk88 cov=0）。

**★ 再次验证记忆条目「覆盖率 ≠ 信号强度」**：
- news_sentiment_transfer（KOR）cov 0.9654 → S 0.04
- **pattern_scores（DEU）cov 0.9888 → S ≤ 0.46**（本段新增第二例）
- 高覆盖只能作「防空窗」下限筛，绝不能当信号质量先验。

### 2. `fundamental6`（FUNDAMENTAL 塔）判死

批次 `1kd8OJ7vo4mz9GeV4X88u62`，10 条全 COMPLETE，基线设置。

| alpha | 模板（学术出处） | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| 2rAe81qN | ROE = ibq/seqq | **0.90** | **0.62** | 0.77 | 0.0266 |
| leA1pLJ2 | 毛利率 = ewq_gpq/atq（Novy-Marx 2013） | 0.60 | 0.37 | **1.53** | 0.0233 |
| zq3eKvQE | 存货强度变化（−Δ invtq/saleq 252d） | 0.53 | 0.33 | 0.73 | 0.0492 |
| Vkxe1vKA | 应计 = (iby−oancf)/atq（Sloan 1996） | 0.32 | 0.14 | 0.30 | 0.0268 |
| RREPjJqj | 现金转换率 = oancf/iby | 0.20 | 0.07 | 0.04 | 0.0296 |
| e75Ekl8J | 杠杆 = ltq/atq | 0.06 | 0.01 | −0.58 | 0.0170 |
| vR1PwKaA | 资产增长异象（−Δ atq 252d, CGS 2008） | 0.01 | 0.00 | 1.00 | 0.0331 |
| xAr5OKwW | 研发强度 = xrd/revt | −0.05 | −0.01 | 0.61 | 0.0136 |
| e75EklgO | 留存收益/权益 = re/seqq | −0.11 | −0.03 | 1.00 | 0.0184 |
| Vkxe1vEw | 营运资本强度 = wcap/atq | −0.34 | −0.16 | −0.93 | 0.0198 |

10/10 REJECT。**S 上限 0.90，代价是 TO 只有 0.014–0.049（极慢）。**

**判死理由**：
- `fundamental6` 是 DEU **唯一**有数据的基本面数据集（其余 fundamental17/72/89/90/93/1/86/alpha_factor_lib/digital_ad_spend 全 cov=0；fundamental22 仅 1 字段；fundamental45 cov 0.269）。
- 10 个经典学术因子（毛利、应计、资产增长、ROE、研发、杠杆、留存收益、营运资本、存货）**无一过 1.0**。
  这不是模板缺漏——这批模板本身就是 Fama-French / QMJ / Sloan 的核心因子集。
- TO 0.02 量级说明信号几乎不动，DEU 的会计信息被充分定价（德国是价值投资传统最深的欧洲市场之一）。

**⇒ FUNDAMENTAL 塔在 DEU 彻底封盘。**

**★ 副产物（重要）**：出现了「S 低但 2Y 高」的**反向背离**型字段（leA1pLJ2 S0.60/2Y1.53、vR1pWKaA S0.01/2Y1.00、
e75EklgO S−0.11/2Y1.00）。这与段 B 在 institutions6/risk60 上看到的一致。
⇒ **DEU 必须双过线（S ≥ 1.58 且 2Y ≥ 1.58），不能用 2Y 高反推机制成立**。

### 3. `other532`（OTHER 塔 · 特异收益）判死

批次 `3hExt87rZ4tA8HzjxN129MP`，10 条全 COMPLETE，基线设置。

| alpha | 模板（学术出处） | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| A1VEjbZE | 特异收益加速度 −Δ(Σ22, 66)（最强） | **0.77** | 0.38 | **1.05** | 0.1818 |
| qMLV9dK2 | 中期特异动量 Σ252−Σ22（Blitz 2011） | 0.26 | 0.10 | −0.01 | 0.0661 |
| gJeGnR7m | 短期特异反转 −Σ5（Lehmann 1990） | 0.23 | 0.04 | −0.05 | **0.4036** |
| akKGjl6v | 双风险模型分歧度（global−emerging） | 0.09 | 0.02 | 0.50 | 0.0599 |
| 1YN0kLkz | 峰均比（上行均值/波动） | 0.03 | 0.00 | 0.16 | 0.1036 |
| 58EYn9o6 | 特异风险调整动量 | −0.09 | −0.02 | 0.51 | 0.0559 |
| 1YN0kLeK | 时序分位 ts_rank 252 | −0.09 | −0.01 | −1.23 | **0.9350** |
| N1N8x6xE | 日/月口径分歧 | −0.12 | −0.01 | −1.39 | 0.0932 |
| bl6AGMGZ | 彩票 MAX（Bali 2011，用 max(x,0)+ts_mean 替代 blocked 的 ts_max） | −0.12 | −0.03 | 0.47 | 0.1279 |
| O0AgQk0p | 低特异波动异象（Ang 2006） | −0.18 | −0.06 | 0.64 | 0.0293 |

10/10 REJECT。**S 上限 0.77（特异收益加速度），距 1.58 差 0.81。**

**判死理由**：
- `other532` 是 DEU other 类最高覆盖（cov 0.9714，global/emerging 双风险模型特异收益 + 特异波动）。
- 特异收益本身已是 Barra 风格因子残差 ⇒ 理论上最接近「纯 alpha 残差」，且与情绪/修正/做空三维天然正交。
- 但 10 个经典特异收益因子（短期反转、中期动量、低特异波动、MAX 彩票、峰均比、加速度、风险调整动量）
  **全部 ≤ 0.77**，说明 DEU 的特异收益维度同样被充分套利。
- 唯一亮点 `A1VEjbZE`：2Y 1.05 > S 0.77 且 **drawdown 仅 0.086（全段最低）**，方向为正（特异收益在加速）。
  可作为「低回撤备件」，但 S 不足，不能作为交付件。

**⇒ OTHER 塔在 DEU（other532 路径）封盘。**

---

## 二、★★★ 策略级转向：`model` category 尚有 45 个数据集、15+ 个高覆盖未测

**这是本段最重要的发现，直接改变后续选集策略。**

此前选集只在 pv / fundamental / other / macro / imbalance / option 六类里扫描（每类仅 1–2 个可用数据集），
得出「DEU 信号空间只剩 3 维」的悲观结论。**本段查 `model` category 发现它包含 45 个数据集**，
其中一大批具备「高覆盖 + 低拥挤 + valueScore ≥5」的组合，且从未测过：

| 数据集 | 名称 | coverage | 字段 | userCount | alphaCount | valueScore |
|---|---|---:|---:|---:|---:|---:|
| `analyst_earnings_ibes` | Global Analyst Earnings Forecasts | **0.9978** | 42 | 130 | 317 | 4 |
| `model264` | Predictive DL models（已用 mdl264） | 0.9973 | 380 | 121 | 217 | 5 |
| **`model53`** | **Creditworthiness Risk Measure** | **0.905** | 22 | **11** | **15** | **6** |
| **`model238`** | **SmartHoldings（预测机构持股变化）** | **0.8552** | 22 | 95 | 155 | 5 |
| `model36` | SmartRatios | **0.8488** | 20 | 53 | 69 | 5 |
| `model28` | Structural Credit Risk | **0.8105** | 25 | 43 | 55 | 5 |
| **`model106`** | Analysts rating model | **0.7878** | 14 | 26 | 41 | **6** |
| `model216` | Analyst Revisions（已用） | 0.7121 | 45 | 366 | 663 | 3 |
| `model250` | Nonlinear adaptive model | 0.6407 | 20 | 108 | 138 | 4 |
| `model25` | Earnings Quality | 0.6064 | 217 | 747 | 2035 | 3（拥挤） |
| `model26` | Analyst Revisions | 0.5778 | 548 | 495 | 944 | 4 |
| `model30` | EPS Estimate Model | 0.5694 | 14 | 130 | 198 | 4 |
| `model109` | Fundamentals + Technical | 0.529 | 544 | 154 | 283 | 4 |
| `multifactor_return_pred` | Multi Factor Market Return Predictions | 0.5187 | 648 | 164 | 407 | 5 |
| **`model144`** | **Stock Selection DL（统计套利/均值回复）** | 0.4861 | 2 | **7** | **9** | **6** |
| `model307` | Global Sales Allocation | 0.4333 | 11 | 3 | 13 | 6 |
| `model313` | Intangible Asset Factors | 0.4072 | 4 | 4 | 4 | 6 |
| `model262` | DNN prediction of fundamentals | 0.3949 | 159 | 21 | 34 | 6 |
| `model140` | Sensitivity to Inflation Change | 0.3814 | 3 | 3 | 3 | 6 |

同时 model 类还有大量 cov=0 已判死的（ai_factor_transfer / analyst_revision_horizons / chart_cnn_alpha /
global_seasonal_model / model110 / model135 / model138 / model139 / model141 / model16 / model239 /
model252 / model257 / model27 / model29 / model32 / model37 / model38 / model68 / model77 /
multi_source_model / option_chart_model / quant_factor_lib）。

**教训**：`get_datasets` 必须**逐个 category 穷举**，不能凭前 6 个 category 的结果推断全表。
`model` 一类就占了全 DEU 数据集的近三分之一（45 / 约 150），漏扫它等于漏掉最大的矿脉。

---

## 三、本段新开数据集画像

### 3.1 `model53` — Creditworthiness Risk Measure（信用风险/违约概率）★ 全新维度

coverage 0.905 / 22 字段 / uc 11 / ac 15（近乎 virgin）/ valueScore 6。两套模型 + 一个利差：

**JC7 模型违约概率**（cov 0.8734，10 个期限）：
```
annualized_pd_{1_month,3_month,6_month,1_year,2_year,3_year,4_year,5_year,7_year,10_year}_jc7
```

**Kamakura Merton 结构模型 v5（MS5）违约概率**（cov 0.9259，同 10 个期限）：
```
mdl53_ms5_{1month,3month,6month,1year,2year,3year,4year,5year,7year,10year}
```

**隐含信用利差**（cov 0.916）：`mdl53_implied_spreads`（basis points）
辅助：`data_observation_date_4`（SYMBOL，cov 1.0）

**学术依据**：**Campbell, Hilscher & Szilagyi (2008) "In Search of Distress Risk"** ——
高违约概率公司的收益**异常地低**（困境异象），与朴素「风险越高收益越高」相反 ⇒ 符号取负（做空高 PD）。

**10 模板设计（已 preflight 全绿）**：
```text
1  -group_rank(annualized_pd_1_year_jc7, sector)                                    困境异象基线（1 年 PD）
2  -group_rank(annualized_pd_1_month_jc7, sector)                                   最短期限 PD（近端违约压力）
3  -group_rank(subtract(annualized_pd_1_month_jc7, annualized_pd_10_year_jc7), sector)  PD 期限结构斜率（近端隆起=临危）
4  -group_rank(mdl53_implied_spreads, sector)                                       信用利差水平
5  -group_rank(ts_delta(mdl53_implied_spreads, 22), sector)                          利差走阔（信用恶化）
6  group_rank(subtract(rank(annualized_pd_1_year_jc7), rank(mdl53_ms5_1year)), sector)  JC7 vs MS5 双模型分歧
7  -group_rank(ts_std_dev(annualized_pd_1_year_jc7, 66), sector)                     信用质量不稳定度
8  -group_rank(ts_delta(annualized_pd_1_year_jc7, 66), sector)                       PD 恶化速度
9  -group_rank(divide(rank(mdl53_implied_spreads), rank(annualized_pd_1_year_jc7)), sector)  利差/PD 错配
10 -group_rank(ts_zscore(mdl53_implied_spreads, 252), sector)                        利差相对自身历史的分位
```

### 3.2 `model238` — SmartHoldings（预测机构持股变化）★ 流量型，优先级最高

coverage 0.8552 / 22 字段 / uc 95 / ac 155 / valueScore 5。
**10 个 `mdl238_*` 字段覆盖率全部 = 1.0**（1–100 排名），另 12 个是 0–100 归一化（cov 0.71）。

核心字段：
```
mdl238_global_change_rank    cov 1.0  机构持股倾向的近期变化（动量）/ 全球排名   ← 流量信号，最核心
mdl238_global_rank           cov 1.0  机构持股倾向水平
mdl238_global_owner_rank     cov 1.0  同伴拥挤/容量风险（100=最拥挤）
mdl238_industry_rank         cov 1.0  业内排名
mdl238_sector_rank           cov 1.0  板块内排名
mdl238_region_rank / _country_rank / _global_screening_rank / _region_change_rank / _region_owner_rank  cov 1.0
global_institutional_preference_rank / global_change_in_preference_rank / industry_relative_investment_rank 等  cov 0.71
```

**为什么优先级最高**：DEU 已证明**流量型**信号（Wikipedia 浏览、做空持仓、分析师修正）
能出 1.59–2.05，而结构性慢信号（基本面、信用、形态）全部 ≤ 1.0。
`mdl238_global_change_rank` 是「预测的机构持股变化动量」= 纯流量。

**10 模板设计（已 preflight 全绿）**：
```text
1  group_rank(mdl238_global_change_rank, sector)                               机构持股变化动量
2  -group_rank(mdl238_global_owner_rank, sector)                               拥挤度反转
3  group_rank(mdl238_global_rank, sector)                                      机构持股倾向水平
4  group_rank(subtract(mdl238_global_change_rank, mdl238_global_owner_rank), sector)  变化−拥挤 净吸引力
5  group_rank(ts_delta(mdl238_global_change_rank, 22), sector)                 变化动量的一阶差分
6  -group_rank(ts_mean(mdl238_global_owner_rank, 66), sector)                  持续拥挤的容量风险
7  group_rank(divide(mdl238_global_change_rank, mdl238_global_owner_rank), sector)  变化/拥挤比
8  group_rank(subtract(mdl238_global_rank, mdl238_industry_rank), sector)       全球 vs 行业相对分歧
9  group_rank(mdl238_global_screening_rank, sector)                            风格契合度
10 group_rank(ts_rank(mdl238_global_change_rank, 252), sector)                 变化动量的历史分位
```

### 3.3 `other699` — Individual Investor Transactions（散户/社交组合交易流水）

coverage 0.506 / **7 字段全 VECTOR** / ac 0–4（近乎 virgin）/ TipRanks 用户组合交易。
`oth699_sharestraded` = 带符号成交股数（买正卖负，已拆股调整）。

**v1 连坐事故**：第 5 条写 `vec_sum(subtract(oth699_newnumofshares, oth699_prevnumofshares))`
⇒ **整批 10 条全 CANCELLED**。根因：`vec_*` 全是**单参数**算子（`vec_min/vec_count/vec_sum/vec_max/vec_avg/vec_stddev/vec_range`），
**两个 VECTOR 字段之间不能直接做 subtract/multiply 等向量算术**，必须先各自 `vec_*` 聚合成标量再做标量运算。

**v2 已改**：`vec_sum(subtract(A,B))` → `ts_sum(divide(vec_avg(A), vec_avg(B)), 22)`，10 条重派 `2HCNpScVz5bKaGtBNbsN3zX`。

**10 模板（v2）**：
```text
1  -group_rank(ts_sum(vec_sum(oth699_sharestraded), 22), sector)                                          短期净流入反转
2  -group_rank(divide(ts_sum(vec_sum(oth699_sharestraded), 22), ts_sum(vec_sum(oth699_newnumofshares), 22)), sector)  净流/持仓规模
3  -group_rank(ts_sum(vec_count(oth699_sharestraded), 22), sector)                                        交易笔数强度（散户关注度）
4  -group_rank(divide(ts_sum(vec_sum(oth699_sharestraded), 22), ts_sum(vec_count(oth699_sharestraded), 22)), sector)  单笔平均规模（大单强度）
5  -group_rank(ts_sum(divide(vec_avg(oth699_sharestraded), vec_avg(oth699_prevnumofshares)), 22), sector)   相对持仓变动  ← v1 事故点已修
6  group_rank(subtract(vec_avg(oth699_priortransactionnumber), vec_avg(oth699_priordistincttradingdays)), sector)  经验−广度背离
7  group_rank(vec_avg(oth699_priordistincttradingdays), sector)                                           用户广度
8  -group_rank(ts_std_dev(vec_sum(oth699_sharestraded), 66), sector)                                      净流波动率
9  -group_rank(ts_delta(ts_sum(vec_sum(oth699_sharestraded), 22), 22), sector)                            净流加速度
10 -group_rank(ts_rank(vec_sum(oth699_sharestraded), 252), sector)                                        净流时序分位
```

### 3.4 `insider_trx_matrix` — 内部人交易（33 字段全 MATRIX，无 VECTOR 负担）

coverage 0.5344（多数）/ 0.5207（USD 系列）；**`directional_indicator_score` cov = 1.0**（全表唯一满覆盖，uc 12 / ac 15）。

字段语义（★ `usd_*` 的编号约定，与已死的 insider_matrix 一致）：
```
_1 = 买入 mean    _2 = 买入 sum    _3 = 卖出 mean    _4 = 卖出 sum
usd_primary   = 董事买入 mean      usd_secondary   = 董事买入 sum
usd_tertiary  = 董事卖出 mean      usd_quaternary  = 董事卖出 sum
usd_top_*     = 高管（executives）子集，编号约定同上
total_*_transaction_count  = 累计强度（专有单位，D0 事件聚合）
mean_*_transaction_count   = 单事件平均强度
```
★ 单位陷阱：`usd_*` 是 `Unit[CSPrice:1]`，**不得与无量纲常数做 add**；两个 USD 字段相减/相除合法。

**10 模板（已 preflight 全绿，全部按论坛结论设计）**：
```text
1  group_rank(ts_sum(total_buy_transaction_count, 22), sector)                                             全体买入强度
2  group_rank(ts_sum(total_top_buy_transaction_count, 22), sector)                                        高管买入强度 ★论坛首选
3  group_rank(divide(ts_sum(total_top_buy_transaction_count, 22), ts_sum(total_buy_transaction_count, 22)), sector)  高管占比（层级信息）
4  group_rank(divide(ts_sum(total_buy_transaction_count, 22), add(ts_sum(total_buy_transaction_count, 22), ts_sum(total_sell_transaction_count, 22))), sector)  买压纯度
5  group_rank(divide(ts_sum(total_top_buy_transaction_count, 22), add(ts_sum(total_top_buy_transaction_count, 22), ts_sum(total_top_sell_transaction_count, 22))), sector)  高管买压纯度
6  group_rank(divide(ts_sum(total_top_buy_transaction_count, 22), ts_sum(mean_top_buy_transaction_count, 22)), sector)  高管买入事件数（集群）
7  group_rank(ts_sum(usd_top_secondary_signal_value, 22), sector)                                         高管买入 USD 累计
8  group_rank(divide(ts_sum(usd_top_secondary_signal_value, 22), ts_sum(usd_secondary_signal_value, 22)), sector)  高管 USD 占比
9  group_rank(ts_mean(directional_indicator_score, 22), sector)                                           现成净方向分水平
10 group_rank(ts_delta(directional_indicator_score, 22), sector)                                          净方向边际变化
```

---

## 四、论坛检索结论：insider 机制（5 条可复用）

检索词 `insider trading 内幕交易 高管增持 insider 数据集 alpha 模板 方向`，命中 10 帖，5 条可用：

1. **《春江水暖鸭先知：insider_agg_matrix 内部人交易观察》**（WL27618，**29 赞**）
   - 「增持信号」的纯度和胜率**显著高于**「减持信号」⇒ **只用买入腿，不要买−卖净值**
   - **多人协同更可信**：单一董事小额增持可能只是例行合规展示；董事长、总经理等多位核心高管**集中增持**，信号置信度倍增
   - **关注相对金额占比**：增持金额占该高管年薪/身家的比例，比绝对金额更说明心态
   - ⇒ 直接对应模板 2/3/5/6/8

2. **《风险共担的力量：insiders1 数据集的深层意蕴》**（WL27618，**29 赞**）
   - `insiders1` 记录**欧洲主流市场**高管申报的持仓动态（与 DEU 直接相关，cov 0.5343 / 8 VECTOR，尚未测）

3. **《【Alpha Idea】高管买入还是买压本身？——一次被自己对照组证伪的"内部人异常买入"挖掘》**（FF56620，**43 赞**）
   - 真正含私有信息的交易集中在 **CEO/CFO 等核心高管**，且**多人同期集群买入是最强信号**
   - 外部投资者只看 Form 4 汇总，全体内部人被聚合成一个数字，「谁在买」的**层级信息被粗化**
     ⇒ 市场对**高管层级**买入系统性反应不足
   - ⇒ 直接对应模板 2/3/5/6/8（必须把 top/executive 子集单独拿出来）

4. **《【Alpha Idea】高管净买入强度在 AMR 市场的因子化尝试》**（XF30004）
   - 已知坑：**稀疏内部人数据容易触发 `CONCENTRATED_WEIGHT`**
   - 方向从「买入波动形态」拧到「**净买入强度**」

5. **《【Alpha Idea】同源披露节奏差：insider × institution 残差对冲的周频化思路》**（LK39823，**57 赞**）
   - 需 cross-join insider × institution 两套数据 ⇒ **与单数据集 ATOM 冲突，本轮不采用**

---

## 五、本段新增工具坑（3 条）

### 5.1 ★ `ts_max` 被 toolkit 静态门禁拦截（DEU）

`create_multi_simulation` 直接整批拒绝：
```text
[INACCESSIBLE_OP] ts_max 平台不可访问，用已验证等价算子替换
passed: 8 / total: 10
```
`ts_max` 不在既有幽灵算子黑名单（`ts_entropy` / `ts_skewness` / `ts_percentage` / `ts_decay_exp_window`）里，
是 toolkit `gate.py` 的 `INACCESSIBLE_OP` 静态表新增项。
**等价替代**：彩票/MAX 类机制改用 `ts_mean(max(x, 0), d)`（`max` 逐元素算子已验证可用，`mLox6Mg2` 在用）。

### 5.2 ★★ VECTOR 字段之间不能直接做向量算术（连坐 10 条）

`vec_*` 全部是**单参数**算子（从算子目录逐条确认）：
```text
vec_min(x)   vec_count(x)   vec_sum(x)   vec_max(x)   vec_avg(x)   vec_stddev(x)   vec_range(x)
```
写 `vec_sum(subtract(oth699_newnumofshares, oth699_prevnumofshares))` ⇒ **整批 10 条全 CANCELLED**。
**铁律**：每个 VECTOR 字段必须**各自**先过 `vec_*` 聚合成标量，之后才能做 subtract / multiply / divide。
**判读**：multisim 顶层 status = `ERROR` 且全部 children = `CANCELLED` ⇒ 典型连坐，不是数据问题，先查表达式语法/类型。

### 5.3 `get_datasets` 必须逐 category 穷举

本段才发现 `model` category 有 **45 个**数据集。此前只查了 pv / fundamental / other / macro / imbalance / option
（每类 1–2 个可用），差点得出「DEU 只剩 3 维」的错误结论。
**已查 category 清单**：pv / fundamental / other / macro / imbalance / option / insiders(2) / socialmedia(2) /
earnings(2) / sentiment(3) / model(45)。
**未查**：analyst / news / institutions / risk / shortinterest / pv 完整表（部分已通过 field 反查）。

**socialmedia 类结论**：socialmedia12 cov=0（死）、socialmedia39 cov 0.2748 / 1 字段（GROUP 型 co-search 对，只可当分组轴）。
**earnings 类结论**：earnings6 cov=0、earnings_sent_matrix cov=0 ⇒ 双双判死（与段 A 一致）。

---

## 六、策略修正：单腿水平模板在 DEU 的天花板 ≈ 1.0

本段 4 个数据集共 40 条 alpha（pattern_scores / fundamental6 / other532 / institutions6），
最佳 S 分别是 0.46 / 0.90 / 0.77 / 0.56 —— **全部 ≤ 1.0**。

而 DEU 已交付的 5 颗（S 1.59–2.05）**全部是多腿/多层结构**：

| alpha | 结构特征 |
|---|---|
| QPvzNNGG S1.70 | **3 腿** earnings 修正 + `bucket(rank(...), range="0,1,0.05")` 自定义分组 |
| LLMzYrZe S1.61 | **2 腿** earnings 修正 |
| E56pROb9 S1.79 | **2 腿 + 双层 group_neutralize**（subindustry 套 subindustry） |
| mLox6Mg2 S2.05 | `vector_neut` + `ts_quantile(driver=gaussian)` + `ts_ir`（非线性和波动率标准化） |
| MPY9VNY9 S1.59 | **两视界 rank 相乘** + `ts_target_tvr_decay(target_tvr=0.03)` |

**⇒ 后续波次策略调整**：
1. **首波（10 条）继续做单腿探针**——目的是测「这个数据集有没有信号」，不是出货。
2. 只要首波出现 ≥1 条 S ≥ 0.8 且 F ≥ 0.4 的单腿，就**立刻进二波做多腿组合/非线性变换**，
   而不是在单腿里继续换窗口（换窗口 = 换参数，不产生 S 跃升）。
3. 首波全 ≤ 0.6 ⇒ 直接封盘，不进二波。
4. 「S 不够就加第二条腿」此时**合法**（记忆里「组腿是稀释」说的是强弱腿混合；
   这里加的是**同机制不同视界**的等强腿，QPvzNNGG/LLMzYrZe 已验证有效）。

---

## 七、当前状态汇总

### 合格 5 颗（全闸通过，全部 UNSUBMITTED）

| # | alpha | 数据集 | 塔 | S | F | 2Y | TO | self | prod |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | SENTIMENT | 2.05 | 1.71 | 2.53 | 0.147 | 0.030 | 0.6935 |
| 2 | E56pROb9 | model216 + predictive_starmine | MODEL | 1.79 | 1.70 | 2.03 | 0.067 | 0.600 | 0.6859 |
| 3 | QPvzNNGG | predictive_starmine | MODEL | 1.70 | 1.30 | 2.18 | 0.155 | 0.678 | 0.6777 |
| 4 | LLMzYrZe | predictive_starmine | MODEL | 1.61 | 1.16 | 1.69 | 0.153 | 0.670 | 0.6697 |
| 5 | MPY9VNY9 | shortinterest3 | SHORTINTEREST | 1.59 | 1.26 | 2.36 | 0.036 | 0.270 | 0.5986 |

严格单数据集 ATOM = 3 颗（QPvzNNGG / LLMzYrZe / MPY9VNY9）。**缺口 5 颗。**

### 互相关天花板 = 5（精确解，段 B 结论仍成立）
```
max_mutually_below_subset = [LLMzYrZe, mLox6Mg2, MPY9VNY9, E56pROb9, QPvzNNGG]
max_mutually_below_subset_size = 5
max_subset_exact = true
```
备用池 6 颗（wpQYNvZp / Vkx3MjW8 / Xg9WNVvl / A1Vvqded / QPveY7Kg / npvwXA8l）**无一可加入**。
⇒ 5 颗缺口必须来自**全新维度**。

### 在飞 / 待派

| 批次 | 数据集 | 条数 | 状态 |
|---|---|---:|---|
| OTH699-A | other699 | 10 | 在飞 `2HCNpScVz5bKaGtBNbsN3zX`（v2，v1 连坐已修） |
| INSIDER-A | insider_trx_matrix | 10 | 在飞 `lp83wc5h4PZ9yvemG6VXnw` |
| MODEL238-A | model238 | 10 | **预检全绿，待槽（优先级最高）** |
| MODEL53-A | model53 | 10 | **预检全绿，待槽** |

### DEU 数据集判死累计（本段 +3）

**cov = 0 型（13 个）**：event_ml_signals(104) / risk72(31) / socialmedia12(18) / earnings6(18) /
earnings_sent_matrix(7) / risk68(5) / risk71(10) / institutions25(24) / macro27(13) / imbalance5(2) /
option1(22) / techindi_model(399) / risk88(单字段)

**有数据但无信号型（7 个/族）**：
- `institutions6` S≤0.56（INSTITUTIONS 塔封盘，三数据集全灭）
- `institutions1` cov 0.2289 已判死
- `risk60` S≤1.0（两波 16 条）
- `predictive_starmine` revenue 族 S≤0.79（容量到顶 3 颗）
- `analyst93` / `insider_matrix`(eur_*) / `nws18`（段 A 判死）
- **`pattern_scores` S≤0.46（本段）**
- **`fundamental6` S≤0.90（本段）**
- **`other532` S≤0.77（本段）**

---

## 八、下一步

1. 收割 OTH699-A（other699 v2）→ 判「散户组合流水」维度是否成立。
2. 收割 INSIDER-A（insider_trx_matrix）→ 判「内部人买入」维度是否成立（论坛三条高赞结论的直接检验）。
3. 槽位释放后按优先级派 **MODEL238-A**（机构持股变化动量，cov 1.0 字段）→ **MODEL53-A**（信用风险/困境异象）。
4. 后续候选池（按优先级）：`model144`(cov 0.486/2 字段/均值回复，最正交) > `model106`(cov 0.788/vs6/ac41) >
   `model36`(cov 0.849) > `model28`(cov 0.811) > `analyst_earnings_ibes`(cov 0.998，但与已用修正族可能高相关) >
   `model313`/`model307`(小字段数) > `insiders1`(8 VECTOR) > `insider_agg_matrix`(34 字段，论坛帖 #1 主角)。
5. 每批收割后按「单腿 S ≥ 0.8 且 F ≥ 0.4 才进二波」的判据决定是否深挖，否则封盘换集。
