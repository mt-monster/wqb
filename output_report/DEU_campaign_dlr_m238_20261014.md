# DEU 战役报告：潜力榜前列数据集（WANL35–38，40 条）

**区域**：DEU / TOP500 / delay=1　**数据集**：`dl_riskfree_returns`（OTHER）、`model238`（MODEL）、`model264`（MODEL）、`analyst7`（ANALYST）
**协议**：严格按探针 SOP（第 0 步零成本筛选 → 双结构 × 跨概念族 → 读数三分法 → 定向升级 → 收口）
**结论**：**50 条合规表达式、5 批（含收口批 WANL39），未产出可提交 alpha。** 全战役最高 S = **1.18**（dlr 概率桶线，2Y 0.41）、最高 2Y = **1.66**（m238 偏好变化线，S 0.81）——**两条线剖面互补、各自封顶**，跨不过双闸 ⇒ 4 个数据集判死。

---

## 一、第 0 步筛选（零成本）与目标选定

平台字段语义核验（`/data-fields`）——**发现三个全新机制**：

| 数据集 | 机制语义 | 可用字段 | 历史最优 S（含多腿） | 已验证单字段 S |
|---|---|---|---|---|
| **`dl_riskfree_returns`** | **未来收益分位桶的 log 概率**（`probability_label{K}_{N}quantile_{D}day_ohlcv`）/ 桶索引（`quantile_label_{N}bucket_{D}day_ohlcv`） | 57 | 2.16 | **0.87** |
| **`model238`** | **偏好/筛选排名 0–100**（`global/regional_change_in_preference_rank`、`mdl238_*_screening_rank`） | 22 | 1.86 | 未测（历史行全是简写复合式） |
| **`model264`** | **技术指标趋势概率**（`mdl264_1l_*`，380 字段，78% α=0） | 380 | 1.94 | 未测 |
| `analyst7` | 分析师估计水平/计数（355 可用，16% 探测） | 355 | 1.04 | 0.40 |

**⇒ 选定前两个为主攻**（机制最新、单信号历史上限最高），`model264`/`analyst7` 各出 1 条做机制探针（符合 SOP 的「跨数据集但聚焦」）。

## 二、外部文献依据（用户要求）

| 文献 | 结论 | 与本战役的关系 |
|---|---|---|
| **Bai & Pukthuanthong (arXiv 2108.02283)**「ML Classification and Portfolio Allocation」 | 多分类器预测**收益状态概率**，多空 Sharpe **1.67（VW）/ 3.35（EW）**，年化 alpha 29–48% | 支撑 `dl_riskfree_returns` 的机制；另指出「**机器不确定性（预测概率本身）降低预测力**」 |
| **「Automated stock picking using random forests」(J. Empirical Finance 2023)** | 用 **outperformance probability** 排序，多空 Sharpe 最高 **1.95**、六因子 alpha 21.79%；**但明确写道「单个技术指标不太可能预测收益」**——收益来自 **180 个指标的模型组合** | 支撑 `model264` 机制；**同时解释了我们的null 结果**：合规单信号框架**不允许组合多指标**（禁混信号），因此无法复制文献的收益来源 |
| Chen et al. (2020, JBFA)（前轮已引） | 分析师修正动量与 PFRD 正相关 | 支撑 `model238` 的 preference-change（修正类机制） |

**⇒ 关键判断**：文献里 ML 概率类 alpha 的收益，主要来自**多指标模型组合**；在「禁混信号」的合规单信号框架下，其收益来源被结构性切断——这预判了本战役的天花板。

## 三、实测（4 批 40 条）

### 3.1 WANL35：双结构 × 跨族探针（10 条）

| 字段 | F 框架 | C 核心 |
|---|---|---|
| `global_change_in_preference_rank`（m238） | **+0.44** | — |
| `regional_change_in_preference_rank`（m238） | **+0.40** | +0.16 |
| `probability_label0_5quantile_60day_ohlcv_2`（dlr） | **−0.49** | −0.42 |
| `est_12m_bps_lowerednum_4wks`（analyst7） | — | **−0.53** |
| `probability_label3_5quantile_5day_ohlcv_2` / `quantile_label_3bucket_60day` / `mdl264_1l_ist` / `mdl264_1l_lda` | ≤0.26 | ≤0.15 |

**读数**：全部 |S| ≤0.53；**F 框架 > C 核心**（与 starmine 相反）；dlr 概率与 analyst7 下调数量**一致负向** ⇒ 方向取反即正向信号。

### 3.2 WANL36：方向修正 + 定向升级（10 条）

| 变体 | S | F | 2Y |
|---|---|---|---|
| **`dlr F quantile_label_1bucket_20day_ohlcv`** | **1.13** | 0.48 | 0.35 |
| **`m238 F ts_delta(global_chgpref, 66)`** | **0.67** | 0.26 | **1.41** |
| `dlr F reverse(prob0_5q_60d)` | 0.49 | 0.15 | 0.08 |
| `m238 F global_chgpref w2=252` | 0.47 | 0.16 | 0.51 |
| 其余 6 条 | ≤0.44 | — | — |

**⇒ 首次进入 SOP 的「1.0–1.58 结构升级带」**（1.13），触发定向升级。

### 3.3 WANL37：1.0–1.58 带升级（10 条）

| 变体 | S | 2Y |
|---|---|---|
| dlr Q1 × w2=252 / 176 | **1.09 / 1.09** | 0.29 / 0.31 |
| m238 delta66(GC) | 0.67 | **1.41** |
| m238 delta66(RC) | 0.60 | **1.36** |
| dlr F × Q3(60d) / industry / delta66 | ≤0.99 | ≤0.63 |

### 3.4 WANL38：收口（10 条）

| 变体 | S | 2Y |
|---|---|---|
| **`dlr F zscore × Q1`** | **1.18**（本战役最高 S） | 0.41 |
| dlr F bucket0.1 × Q1 | 1.14 | 0.44 |
| **`m238 F delta66 + industry`** | **0.81** | **1.66 ✅**（过 2Y 闸） |
| m238 F delta66 + bucket0.1 | 0.63 | 1.34 |
| dlr F delta20(Q1) | 0.98 | 0.96 |

### 3.5 WANL39：收口批（剩余概念族，10 条）

补齐 `model238` 的**三个未探族**（筛选排名 / 同业集中度 / 机构偏好）+ `dl_riskfree_returns` 未探分位族：

| 变体 | S | F | 2Y | TO |
|---|---|---|---|---|
| **`C core × global_screening_factor_alignment_rank`** | **0.99** | **0.73**（全战役最高 F） | 0.49 | 0.100 |
| `F × mdl238_global_screening_rank` | 0.97 | 0.64 | 0.54 | 0.145 |
| `F × global_screening_factor_alignment_rank` | 0.97 | 0.64 | 0.54 | 0.145 |
| `F × ts_delta(mdl238_global_screening_rank, 66)` | 0.95 | 0.52 | **0.95** | 0.185 |
| `F × regional_screening_factor_alignment_rank` | 0.94 | 0.61 | 0.65 | 0.146 |
| `F × regional_institutional_preference_rank` | 0.82 | 0.44 | 0.53 | 0.177 |
| 同业集中度族（`global/regional_peer_investment_concentration_rank`、`mdl238_region_owner_rank`） | −0.09 ~ −0.14 | — | — | — |
| `F × probability_label1_4quantile_5day_ohlcv_2` | −0.27 | — | — | — |

**⇒ 收口结论：`model238` 的「筛选排名」族是全战役最强读数（S 0.94–0.99 / F 0.52–0.73 / TO 0.10–0.19），但 S 仍未破 1.0、2Y 未破 1.0 ⇒ 不进入升级带，按 SOP 判死。**

## 四、裁定：两条线互补，跨不过双闸
| 线 | 最好 S | 对应 2Y | 缺口 |
|---|---|---|---|
| **`dlr` 概率桶线**（`quantile_label_1bucket_20day_ohlcv`） | **1.18** | 0.41 | S 差 0.40、**2Y 差 1.17** |
| **`m238` 偏好变化线**（`ts_delta(global_chgpref,66)` + industry 轴） | 0.81 | **1.66 ✅** | **S 差 0.77**（2Y 已过） |

**两条线在 15 种窗/轴/算子/桶粒度变体下各自封顶，且剖面互补**——`dlr` 的高 S 集中在近年（2Y 低），`m238` 的 2Y 强但整体 S 弱。**没有任何合规结构同时满足 S≥1.58 与 2Y≥1.58。**

**⇒ 判死依据（符合 SOP 判死三条件）**：
1. 已用**两个**已验证结构（F 框架赢、C 核心输）；
2. 已覆盖**跨概念族**字段（概率桶 / 桶索引 / 偏好变化 / 筛选排名 / 技术趋势概率 / 分析师计数）；
3. 已在 1.0–1.58 带做**窗/轴/算子/粒度四维升级**，仍无法同时抬双闸。

**根因（文献支持）**：ML 概率类因子的收益来自**多指标模型组合**（文献 180 指标随机森林），而合规单信号框架禁止跨字段组合 ⇒ **该机制在本框架下不可兑现**。

## 五、本轮全部产出与落盘

- **台账**：wave `WANL35`–`WANL38`（DEU 累计 **349 条 / 38 波**）
- **可提交 alpha：0 颗**（本批 4 个数据集判死）
- 工具链：`potential_scan.py` 扫描 → SOP 四闸 → 双结构探针 → 三分法读数 → 定向升级 → 收口，全流程可复现

---

## 八、PV 类别专项收口（WANL41，2026-10-14）

### 8.1 PV 全类别清点（16 个数据集）

| 数据集 | 平台覆盖 | 字段 | 性质 | 判定 |
|---|---|---|---|---|
| `pv29` | 1.0 | 50 | **纯 GROUP 轴**（`industry_grouping_level*`） | 仅作轴 |
| `pv30` | 0.727 | 285（180 个 GROUP 轴） | **纯 GROUP 轴**（`factor1-4_group*_top*`） | 仅作轴 |
| `pattern_scores` | 0.989 | 504 | 形态相似度信号 | 三轮判死（历史 50 条 + WANL12/33/34） |
| **`pv109`** | 0.467 | 26 | **字段级核验：0 个 cov≥0.6 字段** | 规则排除（本次补齐审计缺口） |
| `pv1`/`pv13`/`pv17`/`pv20`/`pv47`/`pv71`/`pv103`/`pv106`/`pv132`/`pv173`/`continuation_score`/`intraday_pv_feats` | **0** | 1–681 | **DEU 无数据** | 不可用 |

### 8.2 WANL41：pv30 因子轴 × 四个近失候选（10 条）

**这是 PV 数据集在本框架下的唯一合法用法（作分组轴）**——本会话此前只试过 `oth455` 轴（曾把 starmine 抬 +0.84）。

| 变体 | S | F | TO | 对照（无 pv30 轴） |
|---|---|---|---|---|
| `dlrQ1 + factor1轴 + bucket` | 1.18 | 0.50 | 0.289 | 1.18（**无变化**） |
| `m238GSFA + factor1轴 + subindustry` | 0.97 | 0.69 | 0.064 | 0.99 / F0.73（**略降**） |
| `dlrQ1 + factor3轴 + subindustry` | 0.87 | 0.39 | 0.214 | 1.18（**降**） |
| `m238Δ66 + factor1/f2/f3轴` | 0.44–0.70 | — | — | 0.81（**降**） |
| `rv + factor2轴` | 0.66 | — | — | 0.90（**降**） |

**全闸核验（pv30 是 GROUP 轴 ⇒ 触发严格 `IS_LADDER_SHARPE`）**：
- `pwvY0wJ3`（m238GSFA+f1轴）：**ladder 0.79**（需 1.58）、sub 0.32、**prod 0.7146 > 0.7 失败**
- `LL5VeL61`（dlrQ1+f3轴）：**ladder 0.49**

**⇒ 三条结论：**
1. **pv30 因子轴对近失候选无增益**（0 变化或下降）——与 `oth455` 轴的 +0.84 形成对照，**再次确认轴增益是「字段×轴」特异的**；
2. **GROUP 轴会把 2Y 检查从宽松（`LOW_2Y_SHARPE`）切换为严格（`IS_LADDER_SHARPE`）**，实测该批 ladder 仅 0.49–0.79 ⇒ **轴换取的严格闸代价无法承受**；
3. **PV 类别的最后一面（轴用法）已封闭。**

### 8.3 PV 终局

**PV 塔（DEU 未点亮 ✅）在 DEU 无可用信号面**：`pattern_scores` 三轮判死、`pv29`/`pv30` 作轴无增益、`pv109` 无可用字段、其余 12 个数据集 DEU 无数据。**本类别可提交产出 = 0 颗。**
