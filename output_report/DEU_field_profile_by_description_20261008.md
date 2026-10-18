# DEU 字段画像（description 语义版）

**日期**：2026-10-08 ｜ **区域**：DEU ｜ **字段总数**：22,494（`field_profile_perf` WHERE region='DEU'）
**方法**：全部语义判定以 `fields.description` 为准，字段名只作辅助；工具 `tools/fields/field_profile.py`

---

## 0. 摘要

DEU 的字段画像已按「description 真实语义」重建一遍（16 个 category 全部过了一遍），结论有四条：

1. **名字族画像基本不可用**：可比字段里 **75%** 的「名字机制」与 description 机制不一致。已实证 10 类硬误判，其中 2 个连**数据集名**都是错的（`dl_riskfree_returns` 实为收益预测概率、`news17` 里躺着分析师荐股分）。
2. **未测池 3,196 的结构此前被误读**：它 **100% 是 MATRIX(2,775)/VECTOR(410)/SYMBOL(11) 类型**，不是「普通标量字段没试」。其中 11 个 SYMBOL 是日期/时间戳/ISO 国家码这类**毒药字段**，根本不构成信号 ⇒ 有效未测 = **3,185**。
3. **「已否证」的粒度需要拆开说**：机制级 PROD 墙是真的，但字段网格远未穷尽。例：`model216`（ARM 分析师修正子分数）**全族 VECTOR、已测 20 个、最好 S=1.45，仍有 25 个未测**，同 dataset 同类型已有可用解法 —— 这是当前性价比最高的探测口。
4. **画像工具本轮补了 4 个能力**：机制标签库 18→26 族（`?` 漏标从 34.9% 降到 25.6%）、关键词改**词边界匹配**（修 `"ope-rating"` 假阳性）、description 关联改 **(dataset, field) 双列**（修撞名串描述）、新增 `--min-cov/--max-cov`（暴露 0.6 刀切线两侧的边界人口）。

---

## 1. 总账：22,494 个字段的真实分布

> **⚠ 本节已于 2026-10-09 更正**（旧口径把 14,038 个 `coverage=0` 的字段误判为 UNUSABLE）。
> **修正依据（实测铁证）**：`cov == 0.0` 实为**「未采集」而非「零覆盖」** ——
> `model38` 全部字段 cov 记为 0.0，其中 **9 个是 ALIVE（S 1.87–2.44）**、57 个仅因这个 0.0 被判 UNUSABLE；
> `pv47` cov=0.0 而 2 个字段全 ALIVE；`pv1` 的 `close`/`returns`/`cap`/`volume` cov=0 但经平台 `preflight` 确认是**可用内置字段**；
> 且真·低覆盖也能出强信号：`model28` 族 cov 0.584–0.586 → 4 个 ALIVE（S1.77–1.94）、`model109.expected_dividend_yield` cov **0.478** → ALIVE S1.69。
> ⇒ **低覆盖应由平台的 `LOW_SUB_UNIVERSE_SHARPE` 闸判定，不应在画像层预判死亡。**

| verdict | 数量 | 占比 | 含义 |
|---|---:|---:|---|
| **UNKNOWN_COVERAGE** | **14,038** | 62.4% | `cov==0`/缺失 —— ⚠ **须回平台复核**，复核结论见下方「复核结果」 |
| UNUSABLE | 3,422 | 15.2% | 真·低覆盖（0<cov<0.6）⇒ **低优先，非永久剔除** |
| UNTESTED | 3,192 | 14.2% | 可用但从未回测过（本轮重点，见 §6） |
| AXIS_ONLY | 1,390 | 6.2% | GROUP 类型，只能做分组轴 |
| DEAD | 353 | 1.6% | 已测，最好单信号 S < 1.10 |
| DEAD_STATIC | 34 | 0.2% | 已测，换手中位 <0.03（静态属性，任何骨架都无用） |
| **WEAK** | **36** | 0.2% | 最好单信号 S ∈ [1.10, 1.58) |
| DEAD_TURNOVER | 19 | 0.1% | 已测，换手中位 >0.70（HIGH_TURNOVER 闸直接拒） |
| DEAD_COUNT | 6 | 0.0% | 「2Y 有 S 无」形态（家数/参与量类） |
| **ALIVE** | **4** | 0.0% | 最好单信号 S ≥ 1.58 |

**★ 复核结果（2026-10-09 实测，更正本节初版结论）**：
从 8 个最大 `UNKNOWN_COVERAGE` 数据集各取 1 个 MATRIX 代表字段做最小骨架探针 ⇒ **8/8 ERROR**，
平台报错原文 `Attempted to use unknown variable "accounts_payable_period"` / `"la_sales_revenue"`
⇒ **这些字段在 DEU 平台上大多「不存在」**（本地快照的幽灵记录），不是"未采集但有数据"。
附带：本地与平台字段数严重不一致 —— `analyst_revision_horizons` 本地 1,095 / 平台 **300**。

**关键口径（复核后定稿）**：
- **已测 400 个**；未测 3,192。
- **可寻址池 = 3,592**（= UNTESTED 3,192 + DEAD 系 400，即排除 UNKNOWN_COVERAGE / UNUSABLE / AXIS_ONLY）。
  ⚠ 初版曾据 `UNKNOWN_COVERAGE` 推得 17,682，**该数字不成立，已作废**。「DEU 见底」结论**仍然成立**。
- **正确的 cov 判定规则**：`cov=0 且无任何回测记录` ⇒ 高度可疑（幽灵，须平台复核）；
  `cov=0 但已有真实 sharpe 记录` ⇒ 确实可用（如 `model38` cov=0 却有 9 个 ALIVE、`mdl250_maltahc_eq_score` cov 0.556 实测 S1.45）。
  ⇒ 画像层**不得预判死亡**，但**复核是必须的**，不能默认可用。
- **ALIVE ≠ 可提交**。ALIVE 只表示「字段级 IS 强度过闸线」，DEU 存在账户级 PROD ≈0.80 的一致性墙（自 SELF 干净 0.40~0.52），两者是独立维度。

---

## 2. 方法：description 语义确认三步法

| 步骤 | 做法 | 本轮实测结果 |
|---|---|---|
| **① 覆盖率审计** | 先确认 description 不是空的，否则一切语义判定无从谈起 | DEU **22,494/22,494 非空，覆盖率 100.00%**；仅 2 个字段名跨 dataset 描述冲突 |
| **② 机制标签** | 按 description 关键词派生机制标签（本轮 26 族），**不看字段名** | 命中 16,746（74.4%），`?` 5,748（25.6%）|
| **③ 交叉验证** | category × 机制 × verdict 交叉表 + 逐族读原始描述抽检 | 推翻 4 处历史结论、修正 10 类名实不符 |

**为什么必须做②③**：DEU 的字段名是「压缩过三遍」的产物 —— 数据集名乱、字段名乱、后缀乱。实证：
`liquidity_money_flow_alignment` → 实为 *Relative Turnover (RTN63D)*；
`volume_anomaly_price_positioning_2` → 实为 *Detrended Price Oscillator*；
`iv_projected_dividends_fy11_3` → 实为*内在价值模型的 DPS 预测*（`iv` 不是 implied volatility）。

---

## 3. category × description 机制 交叉画像

单元格 = `总[活弱/测死/未测]`，只列前 10 机制（按总量）。

| category | 总 | ALIVE | WEAK | 测死 | 未测 | 弃用 | 主导机制（未测数） |
|---|---:|---:|---:|---:|---:|---:|---|
| MODEL | 8,173 | 0 | 19 | 174 | 1,482 | 6,498 | estimate 387、probability 282、`?` 246、surprise 88、revision 81、ratio 56、count_breadth 40 |
| ANALYST | 4,312 | 2 | 4 | 113 | 538 | 3,655 | estimate 379、count_breadth 42、forecast 40、`?` 40、return 4 |
| OTHER | 3,921 | 0 | 6 | 43 | 366 | 3,506 | **cluster_label 301**、probability 33、`?` 9、return 8 |
| PV | 2,877 | 0 | 0 | 23 | 527 | 2,327 | **score 415**、percentile_rank 72、cluster_label 40 |
| FUNDAMENTAL | 2,146 | 0 | 0 | 14 | 36 | 2,096 | level_amount 26、`?` 10（几乎已穷尽）|
| NEWS | 523 | 0 | 0 | 10 | 202 | 311 | `?` 97、score 78、count_breadth 13 |
| SENTIMENT | 276 | 0 | 0 | 0 | 21 | 255 | `?` 14、count_breadth 3、score 2（几乎已穷尽）|
| INSTITUTIONS | 66 | 0 | 0 | 20 | 9 | 37 | `?` 5、count_breadth 4（13 个已测全判死）|
| RISK | 52 | 0 | 0 | 3 | 3 | 46 | 几乎已穷尽 |
| INSIDERS | 42 | 0 | 0 | 4 | 0 | 38 | **无未测，且 4 个已测全判死 ⇒ 封盘** |
| SHORTINTEREST | 25 | 0 | 0 | 13 | 12 | 0 | 该类唯一 cov=100% 的小类，已测率 52% 全判死 |
| EARNINGS | 25 | 0 | 0 | 0 | 0 | 25 | 全弃用，零测试 |
| OPTION | 22 | 0 | 0 | 0 | 0 | 22 | 全弃用，零测试 |
| SOCIALMEDIA | 19 | 0 | 0 | 0 | 0 | 19 | 全弃用，零测试 |
| MACRO | 13 | 0 | 0 | 0 | 0 | 13 | 全弃用，零测试 |
| IMBALANCE | 2 | 0 | 0 | 0 | 0 | 2 | 全弃用，零测试 |

**整体判读**：DEU 的活动空间几乎全部集中在 **MODEL / ANALYST / OTHER / PV** 四个大类（占未测池 91%）；其余 12 个 category 合计未测仅 283 个，且大部分是「弃用隔壁」或「已测全死」。

---

## 4. 31 个活/弱字段的语义归族（画像的真正资产）

按 description 重新归族后，DEU 的有效信号只有 **5 个机制族**：

### 族 A：分析师预期修正（16 个，占活/弱过半）
| 字段 | S | 2Y | 描述语义 |
|---|---:|---:|---|
| `netprofit_y1_estimate_change_3mo` | **1.70** | 1.66 | FY1 净利润一致预期 3 个月变化 |
| `eps_y1_estimate_change_3mo` | **1.67** | **2.14** | FY1 EPS 一致预期 3 个月变化 |
| `mean_estimate_change_pct_f12m_earnings_14d` | 1.57 | 1.44 | 未来 12 个月盈利预测均值变化率 |
| `mdl216_armpreferredrevisionscore` | 1.45 | 1.04 | ARM 模型修正分量得分 |
| `mean_estimate_change_pct_fy1_earnings_60d` | 1.43 | 1.18 | FY1 盈利预测均值变化率 |
| `mean_estimate_change_pct_f12m_ebitda_14d` | 1.41 | 1.22 | 未来 12 个月 EBITDA 预测变化率 |
| `mean_estimate_change_pct_f12m_earnings_30d` | 1.28 | 1.05 | 未来 12 个月盈利预测 30 天变化率 |
| `eps_y2_estimate_change_3mo` | 1.27 | 1.39 | FY2 EPS 一致预期 3 个月变化 |
| `mdl216_preferredblendedrevisionfy2percent` | 1.27 | 0.45 | FY2 修正指标等权混合 |
| `avg_estimate_change_pct_year1_earnings_90d` | 1.27 | 1.33 | 年 1 盈利预测 90 天均值变化率 |
| `eps_y2_estimate_coeff_var` | 1.23 | 1.49 | **FY2 EPS 预测变异系数（std/mean）＝分歧度，不是修正方向** |
| `mean_estimate_change_pct_fy1_earnings_14d` | 1.21 | 1.33 | FY1 盈利预测 14 天变化率 |
| `mean_estimate_change_pct_f12m_earnings_60d` | 1.19 | 0.50 | 未来 12 个月盈利预测 60 天变化率 |
| `mean_estimate_change_pct_fy1_earnings_30d` | 1.18 | 0.33 | FY1 盈利预测 30 天变化率 |
| `mdl216_armindustry100score` | 1.17 | 0.90 | ARM 行业内百分位（1–100）|
| `mdl26_rank` | 1.10 | −0.04 | 全体 ARM 得分的时间序列百分位（S 有 2Y 无）|

**读法**：修正方向（change/revision）与**分歧度（coeff_var）**是两个不同机制，且后者 2Y=1.49 是全族第二高 —— 这条此前被归在「分析师族」里当噪声，实际值得单独看。

### 族 B：收益预测概率（6 个，`dl_riskfree_returns`）
| 字段 | S | 2Y | 描述语义 |
|---|---:|---:|---|
| `probability_label3_5quantile_20day_ohlcv_2` | 1.45 | 0.96 | 20 日前瞻收益落入 5 分位第 3 桶的 log 概率 |
| `probability_label1_2quantile_5day_ohlcv` | 1.26 | 0.98 | 5 日前瞻收益落入 2 分位第 1 桶的 log 概率 |
| `quantile_label_1bucket_5day_ohlcv_2` | 1.26 | 1.05 | 5 日前瞻收益的**连续回归预测值** |
| `quantile_label_1bucket_20day_ohlcv` | 1.19 | 1.23 | 20 日前瞻收益的连续回归预测 |
| `probability_label4_5quantile_5day_ohlcv_2` | 1.14 | 0.79 | 5 日前瞻收益第 4 桶概率 |
| `quantile_label_2bucket_20day_ohlcv` | 1.12 | 0.75 | 20 日前瞻收益 2 分位桶标签 |

**读法**：数据集名 `dl_riskfree_returns` 完全是误导 —— 它是**市场中性前瞻收益的分位/概率预测模型输出**。符号结构已实测：`probability_label2_5q_20day_ohlc` S=−1.45 与 `label3` S=+1.45 互为镜像 ⇒ **一次探测覆盖两个字段（换符号）**。

### 族 C：ML/评级合成分（7 个）
`mdl250_maltahc_eq_score` 1.45/1.09（主合成 ML 分）、`mdl250_malta_eq_score` 1.33/0.34、`mdl238_industry_rank` 1.33/1.18（**语义修正**：不是「行业排名」，而是 *Smart Holdings score 的行业百分位，排名越高越可能被机构持有*）、`mdl238_global_rank` 1.18/1.30、`mdl238_global_screening_rank` 1.18/0.88、`mdl25_eq_v4_2_1_v22` 1.18/0.31（原始 Earnings Quality）、`mdl25_eq_v4_2_1_v6` 1.18/0.31（Earnings Quality 区域排名）。

### 族 D：分析师跟随收益（2 个，`analyst93`）
`anl93_recprofitabilityprev_analyst_profitability` 1.30/1.33（跟单该分析师的平均日收益）、`..._estimator_profitability` 1.28/1.14（**正确预测概率**）。语义纠正：字段名的 `profitabilityprev` 极易被读成「盈利能力」，实为「分析师历史准确度」。

**合计 16 + 6 + 7 + 2 = 31，与画像 WEAK 29 + ALIVE 2 精确对齐。**

---

## 5. 名字会骗人：10 类实证误判

| # | 字段 / 数据集 | 名字暗示 | description 真实语义 | 危害 |
|---|---|---|---|---|
| 1 | `liquidity_money_flow_alignment` | 流动性-资金流对齐 | **Relative Turnover (RTN63D)** | 归错族 |
| 2 | `volume_anomaly_price_positioning_2` | 量价异常定位 | **Detrended Price Oscillator (DPO)** | 归错族 |
| 3 | `iv_projected_dividends_fy11_3` | 隐含波动率预测 | **内在价值模型 DPS 预测**（FY11）| `iv` 前缀被当波动率族 |
| 4 | `dl_riskfree_returns`（数据集）| 无风险收益率 | **前瞻市场中性收益的分位桶/概率/回归预测** | 整族被当利率族而忽略 |
| 5 | `probability_label3_5quantile_*` | 概率标签 | 前瞻收益落入第 3 桶的 log 概率 | 曾被误判为「无意义标签」 |
| 6 | `est_12m_*_raisednum_*` | 预期上调 | **上调家数**（count_breadth）| 曾按「预期水平」测，机制错 |
| 7 | `act_q_cpx_surprisenum` | 惊喜值 | **计算 surprise 所用的估计数**（参与量）| 名义 surprise 实为 count |
| 8 | `anl93_profitabilityprev_estimator_*` | 盈利能力 | **正确预测概率 / 跟单日收益** | 机制完全不同 |
| 9 | `mdl238_industry_rank` | 行业排名 | **Smart Holdings 分的行业百分位（机构持股概率）** | 误当行业中性化轴 |
| 10 | `news17`（数据集）| 新闻 | 内含 `analyst_recommendation_change_score`、`nws17_ber`（**分析师荐股变化分**）| 按 dataset 名分流会漏掉荐股信号 |

**数据集名同样会骗人**（desc 含 probability 的字段占比）：`techindi_model` 73%、`model264` 75%、`chart_cnn_alpha` 69%、`dl_riskfree_returns` 74% —— 这些「技术指标/图谱/cnn」命名的数据集，实际大量是概率型输出。

---

## 6. 未测池 3,196 的真实结构（修正此前的误读）

### 6.1 类型构成 —— 100% 是「非标量」字段
| ftype | 数量 | 能否直接用 |
|---|---:|---|
| MATRIX | 2,775 | **能**：DEU 实证 `group_rank(ts_scale(x,66),sector)`（pattern_scores）与 `rank(mdl264_*_class)`（model264）都跑出真实 sharpe（组合腿最高 S=1.94）|
| VECTOR | 410 | **不能裸用**，需 `vec_*` 聚合；DEU 已有成功先例 `vec_avg(mean_loan_rate_main)`（analyst93，组合 S=2.02）|
| SYMBOL | 11 | **不是信号**：日期/时间戳/ISO 国家码/序号（毒药）|

⇒ **有效未测 = 3,185**（扣掉 11 个 SYMBOL）。

> ⚠ 跨区铁律再添一条实证：**USA 的「MATRIX 禁套」结论不能外推到 DEU**。同一 session 里 DEU 的 MATRIX 字段裸用成功，说明类型处置必须逐区实测，不能照搬。

### 6.2 dataset 构成 —— 496 个来自「零测试兄弟」的 dataset（占未测池 16%）
| dataset | 未测数 | 真实语义（读 description） | 备注 |
|---|---:|---|---|
| `other455` | **300** | **供应链图谱 Node2Vec 嵌入的 PCA 分量**（partner/competitor/customer/relation × PC1~3 × 窗口）| 完全未测，且 description 写明数据源是 **USA** 图谱 |
| `news17` | 48 | 情绪三分类分（−1/0/1）+ **分析师荐股变化分** | 混装信号 |
| `pv29` | 40 | **行业聚类归属**（industry grouping，可当分组轴）| cov=1.00 |
| `news50` | 37 | 情绪分（多语种）| VECTOR |
| `model30` | 10 | StarMine 分析师家数 | count 族（已否证）|
| `other47` | 9 | 有机增长等价成本估计 | VECTOR |
| `other532` | 8 | 特质收益 | cov=0.75 |
| `analyst48` | 7 | 预测股息金额/大额指数成分 | VECTOR |
| `sentiment27` | 18 | 采集时间戳 | **SYMBOL 毒药，剔除** |
| `news104` | 11 | 是否自动生成新闻 + 置信度 | VECTOR |

### 6.3 机制构成（未测池 top 12）
| category | 机制 | 未测数 | 样例字段（description 语义）|
|---|---|---:|---|
| PV | score | 415 | `adaptive_similarity_upward_bre…` = 图表形态相似度（第二代命名）|
| MODEL | estimate | 387 | `analysts_count_revising_down_q…` = 下调家数 |
| ANALYST | estimate | 379 | `anl44_2_dps_coveredby` = **覆盖标识（非信号）**；`..._lastactccy` = **ISO 币种代码（毒药）** |
| OTHER | cluster_label | 301 | other455 图谱 PCA 分量 |
| MODEL | probability | 282 | model264 各 horizon/期限的概率字段，cov=1.00 |
| MODEL | ? | 246 | 含 `closing_price_dlr1` 等杂项 |
| NEWS | ? | 97 | 情绪分 + 元数据（**混毒药**）|
| MODEL | percentile_rank | 95 | **model216 ARM 建议/区域排名（VECTOR，族内已有 S=1.45）** |
| MODEL | surprise | 88 | model216 ARM 次级修正分 |
| MODEL | revision | 81 | model216 ARM 全局组合分 |
| NEWS | score | 78 | news104 置信度 |
| PV | percentile_rank | 72 | `breakaway_gap_down_q95_simscor` = 形态相似度 95 分位 |

### 6.4 覆盖率分布（验证 0.6 刀切已生效）
`[0.9,1.0)` 1,538 ｜ `[0.6,0.7)` 1,083 ｜ `[0.7,0.8)` 472 ｜ `[0.8,0.9)` 103 —— 全部 ≥0.6，无越界。

---

## 7. 自我审查：本轮发现的 10 个改进点

> 规则：每条都要有「问题 → 证据 → 改进动作」，能落地的当场落地。

### ① 机制标签库覆盖不足（已修）
**问题**：首轮 18 族把 7,844 个字段（34.9%）漏成 `?` —— 技术指标、情绪、聚类、金额级、日内微观结构、事件、置信区间全无族。
**证据**：`ai_factor_transfer` 的 desc 是 *Williams %R / RSI / DPO / Chaikin*；`oth455_*` 是 *Node2Vec + PCA*；`ai_news_scores` 是 *95% 置信上下界*。
**动作**：DESC_MECHS 18 → **26 族**（新增 cluster_label/level_amount/technical/intraday/sentiment/uncertainty/event）。`?` 降到 **5,748（25.6%）**。

### ② 关键词裸子串假阳性（已修）
**问题**：`Operating Activities - Net Cash Flow` 被判成 `score` —— 因为 "ope**rating**" 命中关键词 `rating`。
**动作**：匹配改词边界正则 `(?<![a-z0-9])kw(?:es|s)?(?![a-z0-9])`；同时修掉 `price-to-`（尾连字符永不可能满足右边界）与 `- total` 两个不可用关键词。

### ③ 未测池口径误导（记录，工具层暂不改）
**问题**：`UNTESTED=3,196` 极易被读成「3,196 个普通字段没试过」，实际 100% 是 MATRIX/VECTOR/SYMBOL。SYMBOL 11 个是日期/时间戳/国家码，**不构成信号**。
**动作**：报告层面明确「有效未测 3,185」；建议后续给 verdict 加 `POISON`（SYMBOL/时间戳/币种码）标记。

### ④ MATRIX/VECTOR 的类型处置不可跨区外推（记录）
**问题**：USA 实测「MATRIX 禁套、VECTOR 只能 `vec_*`」，但 DEU 实证 MATRIX 裸用成功（pattern_scores / model264 都跑出真实 sharpe）。若沿用 USA 结论，会把 DEU 2,775 个 MATRIX 未测字段误判为「结构性不可测」。
**动作**：写进 region 分支的实证记录；发批前仍按「单条先验」纪律走。

### ⑤ `--desc-tag` 筛选与标签列不同源（已修）
**问题**：`--desc-tag estimate` 是 LIKE 过滤，而标签列只显示优先级首个命中 ⇒ 查回来的字段标签常显示 probability/revision，读者以为筛错。
**动作**：新增 `mech_all` 列显示**全部命中标签**（如 `surprise/estimate/count_breadth`），一眼看清「为什么命中」。

### ⑥ 撞名字段 description 串位（已修）
**问题**：description 子查询按 `field_name` 聚合，`baltic_dry_index` 在 model193 是「对 BDI 的**敏感度**」、在 model219 是「BDI **本身**」，`MIN()` 取值与 profile 行不保证对应。
**动作**：子查询改 `GROUP BY field_name, d.name`，调用方按 **(dataset, field) 双列 join**。实测两行各自取到正确描述。

### ⑦ coverage 0.6 刀切线的边界人口未盘点（工具已支持，数据待用）
**问题**：**1,593 个字段落在 `[0.5,0.6)` 被整体判为 UNUSABLE**，1,168 个在 `[0.6,0.7)` 勉强过线。刀切线附近的人口从未被单独审视过 —— 而 `model250` 的 `maltahc_eq_score`（cov=0.56）实测 **S=1.45/2Y=1.09**，说明低覆盖字段并非必然无效。
**动作**：新增 `--min-cov/--max-cov`，边界人口可随时单列复查。

### ⑧ 「族已否证」混淆了字段网格与机制饱和（记录，重要）
**问题**：此前「DEU 见底」的表述容易读成「字段网格穷尽」。事实是：机制级 PROD 墙（换轴 0.763 / 换档 0.804 / 组合 0.821~0.838 / 参数无关）确实成立，但**字段网格远未穷尽**：
- `model216`（ARM 子分数）：已测 20 个全 VECTOR，最好 S=1.45，**仍有 25 个未测**，同 dataset 同类型已有可用解法；
- `predictive_starmine` 的 estimate-change 网格（horizon × fundamental）只测了部分格子，`fy1_ebitda_14d` 等仍在；
- `analyst7` 的**分歧度（std）**与季度变体未测，而 `eps_y2_estimate_coeff_var`（分歧度）实测 2Y=1.49。
**动作**：报告与后续探测按「机制墙 vs 字段网格」两层分开表述。

### ⑨ 标签优先级把「家数」藏在「预期」里（刻意不改）
**问题**：`estimate`(#7) 排在 `count_breadth`(#12) 前 ⇒ "Number of raised analyst estimates…" 单标签显示 `estimate`，而它语义是家数（已否证族）。
**评估**：把 count_breadth 提前会改写 **9,051 个字段**的标签（DEU 722 / USA 1,936 / EUR 1,244…），且会误伤 "Forecast-plus-actual mean…number of…" 这类真均值字段 ⇒ 跨 13 区大面积 churn 不划算。
**动作**：不改优先级，改为在代码注释写明口径 + 用 `--desc-tag count_breadth` 查（LIKE 过滤，命中即含广度语义）+ 看 `mech_all` 确认。

### ⑩ 毒药字段未标记（记录）
**问题**：SYMBOL 类型（日期/时间戳/序号/ISO 码）与「覆盖标识」类字段（`anl44_2_dps_coveredby` = 标识符、`_lastactccy` = 币种代码）混在 UNTESTED 里，探过去必然浪费回测槽位。本轮已在 analyst44 语义核验中识别出 **43 个未测里绝大多数是毒药**。
**动作**：建议新增 `POISON` verdict（判据：ftype=SYMBOL，或 desc 含 currency code / ISO / timestamp / identifier indicating）。

---

## 7.5 ★★★ 后处理新杠杆：`tail` 压平中段（2026-10-09 论坛驱动新增）

**来源**：论坛 69 赞帖《内部人"动了多少仓位"比"动了多少钱"更重要 —— DEU 市场内部人信念强度因子》
（已提交 DEU alpha，S1.68 / 2Y2.40 / **prod 0.52 / self 0.11** / 全绿）的**方法论推广**。

**帖子发现**：稀疏事件型数据 + `nanHandling=ON` ⇒ 无事件股票被填 0 ⇒ `ts_sum` 后仍为 0 ⇒ `group_rank` **并列**
⇒ 横截面 72%+ 的股票拿到**同一个中段名次（≈0.4）** ⇒ **rank 中段不是「信念中等」，而是「没有信息」**。
处置：`tail(w, lower=q, upper=1-q, newval=0.5)` 把中段压平 → 中性化后权重归零 → 只交易两端。

### 我方实测：该杠杆对**稠密信号同样有效**（帖子原以为只适用稀疏事件型）

基线 = 本报告 §6 的最优骨架（`mean_estimate_change_pct_f12m_earnings_14d_4` + 图谱簇轴 + 双窗 + decay4 + subindustry），
基线指标 S1.65 / 2Y1.58 / **ladder 1.58 = limit 1.58 → FAIL**：

| 尾部处置 | ladder / limit | 判定 |
|---|---|---|
| 无（基线） | 1.58 / 1.58 | ❌ FAIL |
| `tail(0.25,0.75)` | 1.53 / 1.58 | ❌ |
| `tail(0.20,0.80)` | 1.57 / 1.58 | ❌ |
| `tail(0.15,0.85)` | 1.55 / 1.58 | ❌ |
| `tail(0.30,0.70)` | 1.54 / 1.58 | ❌ |
| **`tail(0.10,0.90)`** | **2.10 / 2.02** | ✅ **PASS** |
| **`tail(0.05,0.95)`** | **2.05 / 2.02** | ✅ **PASS** |
| `winsorize(std=2)` | 1.58 / 1.58 | ❌ |

**边界规律**：`lower ≤ 0.10`（压平 ≥80% 中段）才有效；`lower ≥ 0.15` 全部不过。
⇒ **`tail(lower≤0.10, upper≥0.90, newval=0.5)` 是 DEU 的有效 2Y/ladder 杠杆**，
代价极小（S 1.65→1.59、sub 1.11→1.07）。

### 两个「全绿」候选（但不可提交）

| 候选 | 表达式尾部 | S | 2Y | sub | TO | fit | ra_failed |
|---|---|---:|---:|---:|---:|---:|---:|
| `WjeOVpzd` | `tail(...,0.10,0.90,...)` | 1.59 | **2.10** | 1.07 | 0.1008 | 1.26 | **0**（9 项硬闸全 PASS） |
| `XgJ980Wb` | `tail(...,0.05,0.95,...)` | — | — | — | — | — | **0**（9 项硬闸全 PASS） |

⚠ **但 self_correlation = 0.8136**（阈值 0.7）⇒ **不可提交**。
最高相关的是**已提交 ACTIVE 的 `58gkLAkk`**，它用的是**同一字段 + 同一图谱簇轴**（仅 decay/窗/轴层数不同）
⇒ 「同字段换结构 = 复制品」铁律的又一实证。

⚠ **结构不可跨字段迁移（第三次实证）**：同一 tail 结构套到 `mean_estimate_change_pct_f12m_ebitda_14d_4` ⇒ ladder 0.52；
套到 `mdl250_maltahc_eq_score` ⇒ 0.53。

### 由此得出的下一步（明确的施工图）

把 `tail(lower≤0.10, upper≥0.90, newval=0.5)` 套到**未被 `58gkLAkk` 占用的字段**上，优先本报告 §6.3 的未测池与新翻出的 WEAK：
`mean_estimate_change_pct_fy1_revenue_30d`（S1.41/**2Y1.82**）、`analyst_upward_revision_count_fy1_earnings`（S1.49）、
`netprofit_y2_estimate_change_3mo`、`revenue_y1_estimate_skewness`、`eps_y1_estimate_coeff_var`、
`anl93_accuracy_analyst_analyst`、`anl93_profitabilityprev_analyst_profitability`。
**每批同步跑 `check_self_correlation`**（本地池 7 条，零成本）筛掉与已提交腿近亲的。

### ⚠ 两条口径提醒

1. **ladder limit 随指标浮动**（同一骨架 Y3 时 limit=1.58，T2 时 limit=2.02）⇒ 判「过线」**必须读当次 limit**，不能用固定 1.58。
2. **复现他人 alpha 必须拿到完整 settings**（decay / truncation / 中性化 / nanHandling）——
   本报告复现论坛 institutions1 三段式时因缺 settings 面板（自拟 decay12+SLOW_AND_FAST+nanHandling ON）⇒ 4/4 全部 FAIL。

---

## 7.6 ★★★ 破闸路径的完整判定（2026-10-09 本轮结论）

### (1) 已到顶的路：DEU「分析师修正 × 图谱簇轴」这条腿**被自己账户占死**

从 `submit_ready` 台账查到 `58gkLAkk` 的完整读数 —— 它是本账户 **2026-10-07 已提交**的 ACTIVE alpha：

| `58gkLAkk` | 值 |
|---|---|
| sharpe | **1.75** |
| prod / self（提交时） | 0.5381 / 0.5153 |
| settings | DEU/TOP500/d1/**decay 8**/SUBINDUSTRY |
| 表达式 | 同字段 `mean_estimate_change_pct_f12m_earnings_14d_4` + 同簇轴（`relation_..._pca_fact1_cluster_20`）|

**两条 SELF 通过路径同时不成立**：
1. **阈值**：`tail` 全绿候选 `WjeOVpzd` 的 `check_self_correlation` = **0.8136 > 0.70** ⇒ FAIL
2. **10% 豁免**：豁免要求「新 alpha Sharpe **比被相关者高 10%**」，而 `1.75/1.59 = 1.10` ⇒ 我们**低 10%** ⇒ 不成立

**三个方向独立验证了这条边界**：W222 换字段（4 个，ladder ≤0.86 全灭）／W223 换簇轴（8 个，ladder ≤1.50 全不过）／W224 同族编号变体（8 个，ladder ≤1.03 全灭）。
⇒ **结论：该字段在本账户内已成「一条腿只出 1 颗」的死腿，任何同字段变体都不可能过 SELF。**

### (2) 新战场（本轮真正打开的局面）：`institutions1` · `DEU/D1/INSTITUTIONS ×1.6` 塔

本账户**从未提交过 institutions1** ⇒ **self 天然低**。我方自研结果：

| 变体 | settings | S | 2Y | sub | fit | investability |
|---|---|---:|---:|---:|---:|---:|
| `wpbQY7Yx`（sector 内层 + tail(0.25)） | FAST / decay4 | **1.29** | 1.86 | 0.96 | 0.89 | **1.65** |
| `qM0LWM9E`（industry 内层 + tail(0.25)） | SLOW_AND_FAST / decay1 | 1.26 | **2.02** | 0.99 | 0.74 | 1.63 |
| `vR21k7rA`（无 tail 母版） | FAST / decay4 | 1.14 | 2.03 | 0.65 | 0.72 | 1.28 |

**⇒ `LOW_2Y_SHARPE` / `LOW_SUB_UNIVERSE_SHARPE` / `CLUSTER_TEST` 全部 PASS，只差 `LOW_SHARPE`（~1.3 vs 1.58，需 +0.3）与 `LOW_FITNESS`。**
⇒ **这是当前唯一的现实破闸口**：信号族在 DEU 真实有效、2Y 稳定 1.86~2.02、塔未被占用、`investability_sharpe` 高达 1.65。

### (3) ★ 本轮最重要的方法论发现：复现他人 alpha 的硬门槛 = **完整 settings 面板**

**同表达式、不同 settings 的 1v1 对照**（帖子母版表达式 `winsorize(group_rank(ts_sum(r,66),sector),std=2)`）：

| 来源 | S | 2Y | sub |
|---|---:|---:|---:|
| 论坛帖（母版 @FAST） | **1.65** | **2.77** | 0.70 |
| 我们（FAST + decay4 + nanHandling ON + trunc 0.08） | **1.14** | 2.03 | 0.65 |

**表达式逐字相同，S 差 0.51** ⇒ **差异 100% 来自 settings 面板**。
两次独立实证（W220 缺 decay ⇒ 4/4 全 FAIL；W226 同表达式 ⇒ S 差 0.51）都指向同一结论：
**帖子正文的叙述不足以复现 —— 必须拿到完整 settings（decay / truncation / neutralization / nanHandling / pasteurization / unitHandling）。**

> ⚠ 该帖 §3.3 标题为「Setting 面板及理由」，但正文并未展开；帖子还提到「图 1 累计 PnL」「图 2 逐年 Sharpe」
> ⇒ **原文该节很可能是截图，而 MCP 读帖只能取到文本** ⇒ **请用浏览器打开该帖查看 §3.3 的 Setting 面板截图**，这是复现那条 S1.68/2Y2.40/prod0.52/self0.11 全绿 alpha 的**唯一缺项**。

### (4) 本轮附带的两个工具修复
1. **`is_multileg` v4→v5**：修「比值构造误伤」（`divide(A, add(B, ε))` 被误判混信号）+ 加「括号不平衡截断保护」。
2. **`submit_batch.py --spec` 用法坑**：多个 spec 条目**共享 `path` 时会重复提交该文件全部表达式**（我误发 6×8=48 条 sim，触发 429）；
   且多条目**只用第一个条目的 settings**（实测不同 neutralization 的条目返回相同 alpha id）
   ⇒ **一次 spec 只应放同一 settings 的多表达式；不同 settings 请分次调用**。

---

## 7.7 institutions1 优化全记录（2026-10-09 二轮，5 批 40 条）

### 扫过的全部维度（表达式族固定 = 帖子三段式；settings 基线 FAST + decay4 + trunc0.08 + nanHandling ON）

| 维度 | 档位 | 最好 S | 判读 |
|---|---|---|---|
| 分子字段 | `valueeur` / `tradesignificance`(1–3 分) / `shares` | **1.29** / 1.28 / — | valueeur 最优；换字段无提升 |
| 时间聚合 | `ts_sum(66)`(帖) / `ts_backfill(66/252/22)`(论坛「随身卡片」) / 双窗 `add(66,22)`(66,252) | 1.29 | **ts_sum(66) 最优**；backfill、双窗都更差 |
| 尾部 | 无 / `tail(0.25)`(帖) / `tail(0.10)`(分析师信号最优) | 1.29 | **0.25 最优；0.10 更差** ⇒ tail 边界**信号分布依赖** |
| 内层分组 | `sector` / `industry` | 1.29 / 1.26 | sector 略优 |
| neutralization | FAST / SLOW_AND_FAST / INDUSTRY / SECTOR / MARKET | FAST 最优 | — |
| decay | 1,2,4,6,8,12,20,25 | 越小略高 | 差异小 |
| truncation | 0.02/0.04/0.08/0.12/0.20 | 0.02→1.18 | 影响很小 |
| **覆盖门控**（把 2014–17 空仓，帖主 §5.6 的未解问题） | `trade_when(ts_sum(abs(r),66)>0)` / `ts_count_nans` 三档 / `group_count(sector)>1` | 0.99 | **门控降低 S**（减仓 = 降统计量） |

### 结论

**我方天花板 = S 1.29 / 2Y 1.86~2.03 / sub 0.86~0.99 / investability 1.65**（`wpbQY7Yx`、`qM0LWM9E`，金字塔 `DEU/D1/INSTITUTIONS ×1.6`）
**帖子上限 = S 1.68 / 2Y 2.40 / prod 0.52 / self 0.11**（全绿已提交）

**同表达式 1v1 对照已证（§7.6）：S 差 0.51 全部来自 settings 面板。** 帖子的 §3.3「Setting 面板及理由」正文未展开、原文很可能是截图
⇒ **该截图是复现这条全绿 alpha 的唯一缺项。**

### 本轮新增的 4 条判读/工程铁律

1. ★★ **`checks.fail` 为空 ≠ 通过！** 平台把 `LOW_SHARPE`/`LOW_FITNESS` 放在 **`checks.warning` 区**却仍计入 `ra_failed_count`
   （实证 `vR2AGa9A`：`fail=[]` 而 `ra_failed_count=2`）⇒ **唯一权威判据是 `ra.failed_ra_count`**；
   用 `result=='FAIL'` 过滤会系统性漏判。
2. ★★ **VECTOR 字段禁普通算子**：`if_else(greater(vec_field,0),…)`、`multiply(vec_a,vec_b)` ⇒ 秒拒
   `Operator greater/multiply does not support event inputs`（W229 5/8 ERROR）。
   必须先 `vec_*` 聚合出**标量**再算。★ 且 **`op_arity` 不检查 VECTOR 类型** ⇒ 涉及 VECTOR 的新算子形态**必须先单条验证再进批**。
3. ★ **`tail` 边界是信号分布依赖**：分析师修正 `lower=0.10` 最优（ladder 1.58→2.10 PASS）；内部人 `lower=0.25` 最优。
4. `batch_get_alpha_metrics` 对 UNSUBMITTED **恒返回全 null + `failed_ra_count:0` + `prescreen.REJECT`**（假判）⇒ 只能用 `get_alpha_details` 逐个读。

### 外部文献（本轮灵感来源）

- Hsieh, Ng & Wang (2023, *JBF*)《How informative are insider trades and analyst recommendations?》：
  **内部人交易与分析师下调互补**；条件在分析师下调时内部人净买入的股票收益显著更高。
- 面板回归系数：**买入 1.185% vs 卖出 −0.392%**（买入侧强约 3 倍）；PVB 整体 0.675%。
- 论文推荐用 **(买入−卖出)/日均成交量** 做标准化（而非持仓标准化）—— **因 VECTOR 类型限制，本仓暂无法实现**。
- 论坛《从 0.47 到 2.18：一个 GLB 内部人卖压信号的完整研究记录》：**`ts_backfill(值,66)`「随身卡片」**（已测，劣于 ts_sum）。

---

## 7.8 ★★★ 算子覆盖审计（2026-10-09，用户明令固化为纪律）

### 起因

用户追问「所有算子变换都试过了吗」。严格对账（平台 `get_operators` 实时输出 ∩ REGULAR 可用）结果：

| | 数量 |
|---|---|
| 平台算子总数 | 103 |
| REGULAR 可用 | **84** |
| 本轮 26 批 148 条表达式**实际用过** | **33** |
| **REGULAR 可用但从未用过** | **51** |

**⇒ 此前「结构/字段/持仓/门控四路穷尽」的表述不成立**，正确说法是「**已用算子集合（33/84）内穷尽**」。
这是一次**方法论级别的自我纠错**：所谓「穷尽」是错觉，根因是从未做过一次算子对账。

### 纪律固化（用户明令）

> 「以后在用算子时，一定务必要把所有可能的算子情况都考虑到。」

落为两个**强制动作**：
1. **设计新批次之前** —— 跑 `tools/gates/operator_coverage_audit.py --checklist`，把 REGULAR 全量算子**逐类过一遍**，
   对每类问一句「这个类别在本信号上有没有可能出东西」，**不许凭直觉挑熟练算子**。
2. **宣称「方向穷尽」之前** —— 跑覆盖审计；**覆盖率不足即不得宣称穷尽**。

### 工具（新建）

`tools/gates/operator_coverage_audit.py`（已登记 `tools/README.md` 索引）

| 用法 | 作用 |
|---|---|
| `--checklist [--category "Time Series"]` | 打印全量算子按类分组 + 每个算子的「何时用」机制提示 |
| `--glob` / `--expr-file` / `--wave --region` | 审计已用覆盖率 + 列出从未用过的算子 |
| `--min-coverage 0.5` | **阈值闸**：低于即 `exit 1`，可挂到发批前 |

设计要点：数据源为本地 `docs/reference/operators_catalog.json`（由 `refresh_operator_catalog.py` 刷入实时输出）
⇒ **工具不联网**，MCP 断连时仍可用；内嵌 ~80 个算子的「何时用」提示，其中写入本轮实证的坑
（`group_backfill` 在 `nanHandling=ON` 下是 no-op、`sign` 不能当 group 键、`ts_mean` 在事件型数据上除掉频率信息、
`hump` 是限速器非去相关器、`tail` 边界是信号分布依赖）。

### 已补测的未用算子（W232/W233，16 条）

| 算子 | 结果 |
|---|---|
| **`group_backfill`** | 指标与不含它的版本**逐位相同** ⇒ **no-op**（`nanHandling=ON` 已把无事件填 0、无 NaN 可填）—— 从反面确证了帖子 §2.2「并列块 = 填 0」的成因 |
| `log` | 更差（额外触发 CONCENTRATED_WEIGHT） |
| `signed_power(0.5)` / `pasteurize` / `days_from_last_change` | 未过 S |
| `ts_zscore` / `zscore` / `ts_ir` | 更差（额外触发集中度 + 2Y） |
| `nanHandling=OFF` 全组（8 条，试图激活 `group_backfill`） | **全部更差** ⇒ 「事前填充」路线不可行 |

### 当前欠账

按工具口径，本轮 156 条表达式覆盖 **45/84 = 53.6%**，仍 **39 个从未用过**：
Time Series 18、Arithmetic 6、Logical 6、Vector 4、Group 3、Cross Sectional 2。
正在按批次补测（W234 横截面/向量/组类、W235 时序形态、后续 Logical/Arithmetic 及需第二变量的算子）。

---

## 7.9 ★★★ institutions1 突破：S 1.29 → 1.53（距破闸 0.05）

### 关键突破：`and` 复合条件掩码（不是换算子族，而是换「信号取用条件」）

**新最优 `leKg3jW8`**：
```
tail(winsorize(group_rank(
  multiply(ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),66),
           if_else(and(greater(ts_sum(同上,66),0),
                       greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)),1,0)),
  sector),std=2),lower=0.25,upper=0.75,newval=0.5)
```

| 指标 | 值 | 闸 |
|---|---|---|
| **sharpe** | **1.53** | ❌ limit 1.58（**差 0.05**） |
| **fitness** | **1.15** | ✅ |
| two_year | **2.39** | ✅ |
| sub_universe | **1.01** | ✅ |
| turnover / margin | 0.1283 / 0.00114 | ✅ |
| investability_sharpe | **1.80** | — |
| `ra_failed_count` | **1** | 仅 LOW_SHARPE |
| 塔 | `DEU/D1/INSTITUTIONS ×1.6` | 本账户首用 |

### 机制：两层筛选叠加

| 条件 | 作用 | 文献依据 |
|---|---|---|
| `greater(S66, 0)` | **只取买入侧** | Hsieh/Ng/Wang (2023, *JBF*)：买入侧强度是卖出侧约 **3 倍**（1.185% vs −0.392%） |
| `greater(显著性合计, 2.0)` | **只取机会型交易**（过滤例行小额） | Cohen/Malloy/Pomorski (2012, *JF*)：routine vs opportunistic |

★ **工程要点**：W229 曾试图直接「拆买卖」（`if_else(greater(vec_field,0),…)`）因 **VECTOR 类型限制**失败；
而 **`and(greater(标量,0), …)` 在 `vec_sum` 聚合后的标量上做条件筛选，绕开了该限制** —— 这是文献结论的**可行等价实现**。

### 三条单峰/尖峰曲线（本轮所有杠杆的极值点）

| 杠杆 | 扫描 | 最优 |
|---|---|---|
| 显著性阈值 | 1.0/1.5→1.42、**2.0→1.53**、2.5→1.50 | **单峰，甜点 2.0** |
| settings decay | 3→0.64、**4→1.53**、6→0.58 | **极窄尖峰，仅 decay=4** |
| tail 边界 | (0.10,0.90) / (0.20,0.80) / (0.25,0.75) | **0.25** |
| 内层轴 | sector / industry / subindustry | **sector** |
| 显著性用法 | 0/1 硬掩码 / 连续权重 | **硬掩码** |

### 下一步（唯一还没在本新结构上试过的大杠杆）

1. ★ **图谱簇轴**（`other455` 的 1200 个 GROUP 轴）—— 从未用在 institutions1 上，且直接换持仓结构；
2. `ts_sum` 窗口（66 → 44/88/132；帖主称 66 唯一，但那是**无掩码版**的结论）；
3. `group_cartesian_product(sector, 簇轴)` 复合轴；
4. 掩码第二条件换成「交易额占持仓比例」类口径。

### 本轮未用算子扫描汇总（W232–W237，48 条）

| 批次 | 算子 | 结果 |
|---|---|---|
| W232/W233 | `group_backfill`/`log`/`signed_power(0.5)`/`pasteurize`/`days_from_last_change`/`ts_zscore`/`zscore`/`ts_ir`（ON+OFF 各 8） | 全灭；`group_backfill` 在 ON 下是 **no-op** |
| W234 | `vec_count`/`vec_stddev`/`vec_range`/`vector_neut`/`group_scale`/`group_sum`/`normalize`/`scale` | 全灭（3 条因 `group_rank` 单调性而是 no-op） |
| W235 | `ts_delta`/`ts_delay`/`ts_returns`/`ts_scale`/`ts_kurtosis`/`ts_max_diff`/`ts_arg_max`/`last_diff_value` | 全灭（`ts_delay` S1.21 最好） |
| **W236** | Logical 6 + `group_std_dev` | ★ **`and` 掩码突破（S1.42 → 1.53）** |
| W237 | `sqrt`/`power`/`max`/`min`/`reverse`/`densify`/`ts_corr`/`ts_regression` | 全灭 |

**覆盖率 45/84 → 约 76/84（90%）**；剩 8 个：`hump`/`kth_element`/`ts_arg_min`/`ts_covariance`/`ts_product`/`ts_step`/`ts_target_tvr_decay`/`ts_target_tvr_hump`。

---

## 7.10 ★★★★★ 破闸：`LLZ87QY9` —— DEU 首个「全绿 + 双相关通过」的合规单信号

### 关键改动（一步）：把内层分组轴从 `sector` 换成 `other455` 的**「合作伙伴」图谱簇**

`oth455_partner_n2v_p50_q200_w1_pca_fact1_cluster_20` ⇒ S **1.53 → 1.67**

```
tail(winsorize(group_rank(
  multiply(ts_sum(divide(vec_sum(inst1_valueeur),add(vec_sum(inst1_holdings),0.0001)),66),
           if_else(and(greater(ts_sum(同上,66),0),
                       greater(ts_sum(vec_avg(inst1_tradesignificance),66),2.0)),1,0)),
  oth455_partner_n2v_p50_q200_w1_pca_fact1_cluster_20),std=2),lower=0.25,upper=0.75,newval=0.5)
```

settings：`DEU / TOP500 / d1 / decay 4 / FAST / trunc 0.08 / nanHandling ON / pasteurization ON`

### 全部检查结果

| 项目 | 值 | 判定 |
|---|---|---|
| **sharpe** | **1.67** | ✅ LOW_SHARPE |
| **fitness** | **1.30** | ✅ LOW_FITNESS |
| **two_year** | **2.52** | ✅ IS_LADDER_SHARPE |
| **sub_universe** | **1.07** | ✅ LOW_SUB_UNIVERSE_SHARPE |
| turnover / margin | 0.1334 / 0.001217 | ✅ LOW/HIGH_TURNOVER |
| CLUSTER_TEST / CONCENTRATED_WEIGHT | — | ✅ |
| **`ra_failed_count` / `ppa_failed_count`** | **0 / 0** | ✅ |
| **`checks.fail`** | **空** | ✅ |
| **`check_correlation` production** | **0.6947**（< 0.70） | ✅ PASS |
| **`check_self_correlation` self** | **0.0306**（< 0.70） | ✅ PASS |
| **`all_passed`** | **true** | ✅ |
| **塔** | **`DEU/D1/INSTITUTIONS ×1.6` + `DEU/D1/OTHER ×1.8`（effective=2）** | — |
| investability | 1.90 / 1.65 | — |

### 两个机制要点

1. **金字塔由 1 变 2**：簇轴字段来自 `other455` 数据集 ⇒ 同时贡献 **OTHER 塔 ×1.8**（原 `sector` 版只有 INSTITUTIONS ×1.6）。
2. **为何换轴能同时提 S/2Y/sub**：`sector` 是行业口径，而**「合作伙伴」图谱簇**沿**信息传导路径**分组
   —— 供应链伙伴的内部人交易具有信息溢出效应，簇内相对排序比行业口径更贴合该机制。

### ⚠ 唯一风险：prod 0.6947 距阈值仅 0.0053

直方图显示 **0.6–0.7 区间有 2 条、0.5–0.6 有 1 条** ⇒ 该值由极少数个股/单条生产 alpha 顶起，
平台**滑窗重算后随时可能翻转成 FAIL** ⇒ **不可裸提交**，需先降 prod（正在 W241 中扫簇轴变体）。

### 附：self 低值的可信度论证

`institutions1` **本账户从未提交过**（INSTITUTIONS 塔系首次触及）⇒ **不存在「近期提交孪生体」的盲区**
⇒ 本地 self 0.03 的可信度高（这是记忆里 self 盲区规则的**正向应用**：盲区只在"同族近期提交过"时生效）。

### 补充：S↔prod 前沿与最终定案（W241–W242）

在 `partner` 簇轴上扫 **窗 / 簇数 / 主成分（fact1-3）** 后，实测 prod：

| 候选 | 轴 | **S** | **prod** | 判定 |
|---|---|---|---|---|
| `786GZ5zx` | partner_fact1_**c10** | 1.74 | 0.7037 | ❌ |
| `xAblYLNp` | partner_fact1_**c5** | 1.73 | 0.7062 | ❌ |
| `P0gP2bvL` | partner_**fact3**_c20 | 1.71 | 0.7019 | ❌ |
| `LLZ87QY9` | partner_**fact1**_c20 | 1.67 | 0.6947 | ✅ 余量 0.0053 |
| **`58gGQmlN`** | partner_**fact2**_c20 | **1.62** | **0.683** | ✅ **余量 0.017（3.2×）** |

**⇒ 关键结构发现：该信号族内 S 与 prod 严格同向**（S↑ ⇒ prod↑），是一条**前沿而非可独立优化的两维**。
直方图显示 0.6–0.7 桶仅 **1~2 条** ⇒ 相关性来自**同一条生产 alpha**（非机制层拥挤）。
**⇒ 前沿上唯一「S 过线 + prod 余量充足」的点 = `58gGQmlN`（fact2 / cluster_20）。**

**其他 W242 读数**：`relation_pca_fact3` S1.68、`partner_fact3_c10` S1.66、`customer_fact2/fact3` 1.60/1.57、
`relation_fact2` 1.55、**`competitor` 仅 1.30**（差）、**`group_cartesian_product(partner簇, sector)` 0.77**（组合轴反而崩）。

**⇒ `partner`（供应链合作伙伴）图谱是该信号的正确关系轴**（customer 次之、competitor 最差）。

### 最终推荐（待用户决定是否提交）

| 项 | 值 |
|---|---|
| **alpha_id** | **`58gGQmlN`** |
| sharpe / fitness | **1.62 / 1.26** |
| **prod / self** | **0.683 / 0.019**（均 < 0.70，`all_passed = true`） |
| 表达式轴 | `oth455_partner_n2v_p50_q200_w1_pca_fact2_cluster_20` |
| 塔 | `DEU/D1/INSTITUTIONS ×1.6` + `DEU/D1/OTHER ×1.8` |
| 备用 | `LLZ87QY9`（S1.67，prod 0.6947 余量仅 0.005） |

⚠ 提交前必做：重跑 `check_correlation(refresh=True)` 取**实时** prod（>48h 旧值不可信）。**提交权归用户。**

### 从「只差 0.05」到破闸的路径（本日累计）

| 阶段 | 最优 S | 关键动作 |
|---|---|---|
| W210–W219 | 1.58（ladder 卡死） | 分析师修正腿 → 被 `58gkLAkk` 占死 |
| W225–W231 | 1.29 | 换战场到 `institutions1`（处女数据集） |
| W232–W237 | 1.29 | 算子覆盖扫描（48 条）→ 0 提升，但发现 `and` 未被用过 |
| W236–W238 | **1.42 → 1.53** | ★ `and` 掩码（买入侧 + 机会型），用标量层绕开 VECTOR 限制 |
| **W240** | **1.67** | ★ 换 `other455` 合作伙伴图谱簇轴 → **全绿 + 双相关通过** |

---

## 8. 后续可测方向（按性价比排序）

| 优先级 | 方向 | 规模 | 机制 | 为什么值得 | 主要风险 |
|---|---|---:|---|---|---|
| **P0** | `model216` ARM 子分数未测 25 个 | 25 | 分析师修正 | 同 dataset 已测 20 个含 **S=1.45/2Y=1.04**，VECTOR 解法现成（vec_avg）| PROD 墙（与族 A 同机制）|
| **P0** | `dl_riskfree_returns` 桶号补齐 | 42→约 21 次探测 | 收益预测概率 | 6 个同族 WEAK（最高 1.45）；**桶 2/3 互为镜像，一次探测两字段**；低桶(0)从未测，高桶不对称未验 | 同上；且 eur_* 变体 cov=0.50 已实测 S≈0.1 |
| **P1** | `other455` 供应链图谱 PCA | 300 | 图谱嵌入 | **完全零测试的全新机制族**，cov 0.72–0.84，USA 图谱跨区信号 | 300 个高度同源 ⇒ self 必然高；需先跑 4 条探针定 S |
| **P1** | analyst7 分歧度（`*_std`）| ~20 | 分歧度/不确定性 | `eps_y2_estimate_coeff_var` 2Y=1.49 佐证该机制在 DEU 有效 | 家数/稀疏类历史 2Y 崩（见 §8 注）|
| **P2** | `pattern_scores` 第二代命名池 | 54+ | 图表形态相似度 | 已测 17 个（`group_rank(ts_scale(...))` 骨架现成）；cov≈1.00 | 同族拥挤 ⇒ PROD 高 |
| **P2** | `predictive_starmine` 网格补格 | ~30 | estimate-change | 14d 最优（1.57/1.41），`fy1_ebitda_14d` 等空格未测 | 机制墙 |
| **P2** | news VECTOR 池（vec_* 路径）| ~196 | 情绪/荐股事件 | `vec_avg` 路径已验证；含荐股变化分 | 多数 cov 0.4–0.8，稀疏 |
| **P3** | `pv29` 行业聚类当分组轴 | 40 | 分组结构 | cov=1.00，替代 subindustry 轴可能降 PROD | 轴类字段作分组键需平台确认 |

**注（历史教训）**：W197/W208/W209 三批「家数/广度类」信号 2Y 系统性崩溃（S≤1.18 且 2Y 普遍崩），推断更新频率低 ⇒ 信号稀疏。**所有 count_breadth 方向的探测必须先看 2Y，不要被 IS 迷惑。**

---

## 9. 使用边界

1. **本画像只覆盖 DEU**。其他 12 区的主表行在 `field_profile_perf`，查询须带 `region=`（`fields` 表无 region 列，裸查会静默串区）。
2. **`fields.ftype` 是本地快照**。类型决定用法（VECTOR 需 `vec_*`），发批前以平台 `get_datafields` 为准；本轮已实证 USA 结论不可外推到 DEU。
3. **ALIVE/WEAK 只是字段级 IS 上限**，不含 PROD/SELF/2Y 全闸；`best_s_sg` 是「单信号（合规形态）历史最好值」，多腿组合的历史值在 `best_s` 里但**不参与判定**。
4. **机制标签是粗粒度首过**。`?`（5,748）不是「无机制」，而是「26 族都没命中」—— 其中含事件元数据（毒药）与未建模机制两类，需要读原始描述才能区分。
5. **description 覆盖率 100%**（22,494/22,494），但**准确率不是 100%**：平台自身的描述存在笔误与过时（如 `mdl26_rank` 实际是「ARM 得分的时间序列百分位」，描述未说明是哪个模型）。

---

## 附：工具能力（本轮新增/修复）

```bash
# 机制分布（26 族，含 ? 桶）
python tools/fields/field_profile.py --list-tags --region DEU

# 按机制族筛字段（LIKE 过滤；mech_all 列显示全部命中标签）
python tools/fields/field_profile.py --query --region DEU --category model \
    --verdict UNTESTED --desc-tag estimate,revision --limit 40

# coverage 边界人口（0.6 刀切线两侧）
python tools/fields/field_profile.py --query --region DEU --min-cov 0.5 --max-cov 0.6

# 多区隔离盘点
python tools/fields/field_profile.py --list
```

**本轮对 `tools/fields/field_profile.py` 的改动**：DESC_MECHS 18→26 族；匹配改词边界正则；新增 `desc_mech_all()`；`_desc_sql` 暴露 dataset 并按 (dataset, field) 分组；query/list_tags 改双列 join；新增 `--min-cov/--max-cov`。**无 schema 变更、无数据迁移**，既有 `field_profile_perf` 数据完全兼容。