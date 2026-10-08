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

| verdict | 数量 | 占比 | 含义 |
|---|---:|---:|---|
| UNUSABLE | 17,460 | 77.62% | 覆盖率 <0.6（DEU 大量字段 cov=0.0，结构性不可用） |
| UNTESTED | 3,196 | 14.21% | 可用但从未回测过（本轮重点，见 §6） |
| AXIS_ONLY | 1,390 | 6.18% | GROUP 类型，只能做分组轴 |
| DEAD | 358 | 1.59% | 已测，最好单信号 S < 1.10 |
| DEAD_STATIC | 34 | 0.15% | 已测，换手中位 <0.03（静态属性，任何骨架都无用） |
| DEAD_TURNOVER | 19 | 0.08% | 已测，换手中位 >0.70（HIGH_TURNOVER 闸直接拒） |
| DEAD_COUNT | 6 | 0.03% | 「2Y 有 S 无」形态（家数/参与量类） |
| **WEAK** | **29** | 0.13% | 最好单信号 S ∈ [1.10, 1.58) |
| **ALIVE** | **2** | 0.01% | 最好单信号 S ≥ 1.58 |

**关键口径**：
- **已测 448 个**（31 活/弱 + 417 判死）＝ 全域的 **1.99%**；未测 3,196 ＝ **14.21%**。
- **可寻址池 = 3,644 个**（已测 448 + 未测 3,196），这是 DEU 全部的剩余活动空间。
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