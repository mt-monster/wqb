# DEU 全面字段画像 v3 —— 资源地图与新机制发现（2026-10-13）

**区域**：DEU / TOP500 / delay=1　**平台实时**：**172 数据集**　**金字塔**：D1 已点亮 institutions=1 / model=1 / other=2 / **analyst=1（由本轮 `2rjrMZ25` 点亮）** / fundamental=1
**方法**：平台全量数据集 × 本地「已挖」台账交叉 → 未点亮类别终局复核 → 已点亮类别未开采清单 → 字段级语义核验 → 新机制假设 + 学术佐证 → 探针实测。

---

## 一、资源地图（全量 172 数据集）

### 1.1 三层结构

| 层 | 内容 | 状态 |
|---|---|---|
| **无数据区** | `earnings6`/`option1`/`macro27`/`socialmedia12`/`imbalance5` 及大池子 `pv20`(681)/`intraday_pv_feats`(585)/`continuation_score`(560)/`news23`(116)/`pv173`/`risk72` | **DEU 每字段覆盖率 = 0.0**（换宇宙 TOP200/100/1000 与 delay=0 均无效）⇒ 不可用 |
| **未点亮有数据区** | 19 个（news104/18/20/17/50、sentiment27/7、risk88/60、shortinterest3、insider_agg_matrix/insiders1、pv29/pv30/pattern_scores、pv109、socialmedia39、sentiment33、news38） | **全部实测判死**（本轮 WANL7/8/12/24/26：跨类别 39 字段 max S 0.64，news104 全新概念 max S 0.26） |
| **已点亮未开采区** | **11 个**（见 §1.2） | 本轮新前沿 |

### 1.2 已点亮类别 × 从未开采 × 覆盖≥0.45（按平台价值分排序）

| 数据集 | 类别 | 字段 | 覆盖 | α数 | 用户数 | 价值分 | 语义 |
|---|---|---|---|---|---|---|---|
| **`other532`** | other | 8 | **0.856** | 37 | 25 | 6.0 | **Barra 残差收益**（描述误标为「标识符映射」，字段实为 `specificreturn`/`idiosyncratic_return`） |
| `analyst48` | analyst | 7 | 0.788 | 4 | 2 | 6.0 | 元数据/计数族（历史判死） |
| **`model106`** | model | 14 | 0.788 | 21 | 15 | 6.0 | **晨星式评级**（stars 0-4 / global_evaluation −2~+2 / fnb / rv） |
| `insider_matrix` | other | 33 | 0.548 | 73 | 51 | 6.0 | 内部人矩阵（仅 1 字段 cov≥0.6：`director_intensity_score`） |
| `stock_cluster_dl` | other | 5 | 0.453 | 8 | 6 | 6.0 | DL 图表聚类（PCA 特征，轴性质） |
| `other47` | other | 18 | 0.577 | 42 | 30 | 5.0 | Web Intelligence（organic_traffic 已测 0.15） |
| `model109` | model | 544 | 0.529 | 162 | 85 | 5.0 | 274 因子大池 |
| `multifactor_return_pred` | model | 648 | 0.519 | 258 | 110 | 5.0 | 多因子预测大池 |
| `model26` / `model30` / `model144` | model | 548/14/2 | 0.578/0.569/0.486 | 585/133/7 | 290/86/6 | 4.0 | estimate 族 WEAK / StarMine 水平量已死 / — |

---

## 二、★ 新机制发现（本轮最重要的画像产出）

### 2.1 `other532` = 残差动量的标准输入

字段语义（平台 description 核验）：
> `oth532_global_daily_specificreturn`：**Realized stock-specific return (idiosyncratic residual from the Barra risk model)**，cov **0.964**；
> `oth532_emerging_daily_specificreturn`：同上，cov **0.971**。

⇒ 这正是 **残差动量（residual momentum）** 的输入。学术依据（外部检索）：
- **Blitz, Huij & Martens (2011, Journal of Empirical Finance)**：以残差收益替代总收益排序，**Sharpe 约为普通动量 2 倍（0.90 vs 0.45）**、更稳定、崩溃风险更低；经典构造 = **12-1 跳月累积残差（剔除最近 1 个月）**，可再除以残差波动率做风险调整。
- Chaves (2012)：21 个发达国家均有效；Blitz, Hanauer & Vidojevic (2017)：不被传统动量因子吸收。
- **DEU 从未测过该机制**（本会话 27 波 233 条全部围绕「预期变化率」与已否证族）。

### 2.2 `model106` = 评级变化事件

`mdl106_stars`（0–4 星）、`mdl106_global_evaluation`（−2~+2 综合评分，cov **1.0**）、`mdl106_fnb`（坏消息因子，越高越差）、`mdl106_rv`（估值 −2~+2）。评级变化 = 稀疏事件 ⇒ 适配五层配方（`ts_sum` 累积 + 双窗差分）。

---

## 三、算子覆盖审计（84 算子，本轮新增使用）

| 大类 | 本轮新增实证 |
|---|---|
| Time Series | `ts_sum`（累积/跳月差分）、`ts_delta`、`ts_zscore`、`ts_backfill`、`ts_mean`、`ts_decay_linear` |
| Arithmetic | `subtract`（同字段双窗差分 = 单信号结构化，合规）、`reverse`（方向杠杆） |
| Group | `group_rank` / `group_zscore` / `group_neutralize` + `bucket`（桶轴） |
| Vector | `vec_avg` / `vec_max`（聚合独立杠杆） |
| Cross Sectional | `rank` / `quantile` / `winsorize` |
| 待用 | `ts_ir`（风险调整动量的候选）、`divide`（除以残差波动率 = Blitz 风险调整版）、`hump`、`tail`、`signed_power`、`ts_quantile`、`group_cartesian_product` |

---

## 四、实测（WANL27–30，40 条）

### 4.1 WANL27：残差动量（`other532`）——**判死**

| 结构 | S | TO |
|---|---|---|
| 6m 累积 `ts_sum(126)` | **0.36** | 0.154 |
| `ts_zscore(252)` / 框架(1/210) / `ts_delta(120)` | 0.33 / 0.30 / 0.29 | **0.76**（超 0.7 换手闸） |
| 跳月动量 `sum(210)−sum(21)`（Blitz 经典） | 0.08 | 0.180 |
| 12m 累积 / 五层 252-120 差分 / EM / EU | ≤0.03 或 −0.58 | 0.14–0.75 |

⇒ **残差动量在 DEU 无信号**（max 0.36）；且日频残差的短窗结构换手 0.75+ 直接撞闸。Blitz (2011) 的机制在德国大盘不成立（与前人「动量在德国弱」一致）。

### 4.2 WANL28/29：评级（`model106`）——**发现真信号但够不到闸**

| 结构 | S | F | 2Y |
|---|---|---|---|
| **`mdl106_rv`（估值评分）× 框架(1/210)** | **0.90** | 0.64 | **1.67** |
| `mdl106_rv` × 框架 +winsorize4 / w2=252 | 0.90 / 0.89 | 0.64 / 0.62 | 1.67 / **1.75** |
| `mdl106_stars` × `ts_delta(66)`（**评级变化**） | **0.77** | 0.39 | 0.37 |
| `mdl106_rv` × DEU核心 / industry / oth455 | 0.66–0.70 / 0.39 / 0.31 | — | — |
| `mdl106_rv` reverse | **−0.90**（完全对称） | — | — |

**三条结论：**
1. **`rv` 是继「预期变化率」之后 DEU 第二个有真信号的机制**（估值评分水平量，单调有效——reverse 精确 −0.90）。但结构天花板 ≈**0.90**（10 种结构实测），距 1.58 还差 0.68；F 0.64 距 1.0 差 0.36。
2. **DEU 核心结构在 rv 上反而有害**（0.66–0.70 vs 0.90）——**第三次实证「结构最优性逐字段」**（框架赢：eps_y1；核心赢：starmine；都不行：rv/残差动量）。
3. 评级变化（`ts_delta(stars,66)` 0.77）方向有效但 2Y 弱（0.37）。

### 4.3 WANL30：中性化杠杆（`rv` @ MARKET）——**反向**

| 变体 @ MARKET | S | @SUBINDUSTRY |
|---|---|---|
| rv 框架(1/210) | 0.53 | **0.90** |
| rv 框架 w2=252 / +winsorize / 单窗66 / w2=120 | 0.53–0.54 | 0.80–0.90 |
| 其余（w1=22 / subindustry / delta252 / bucket0.1 / w2=504） | ≤0.51 | ≤0.90 |

⇒ **粗中性化（MARKET）反而把 S 从 0.90 砍到 0.53**：`rv` 的信号部分来自行业内相对估值，市场中性化把它洗掉了。SUBINDUSTRY 已是最优档，**中性化杠杆用尽**。

---

## 五、终局裁定

### 5.1 本轮新机制全谱（WANL27–30，40 条）

| 机制 | 数据集 | 最好读数 | 判定 |
|---|---|---|---|
| 残差动量（Blitz 2011） | `other532`（Barra 残差收益，cov 0.97） | S 0.36（且框架变体 TO 0.76 撞闸） | **判死** |
| 估值评分水平量 | `model106.mdl106_rv`（cov 1.0） | **S 0.90 / F 0.64 / 2Y 1.67**（10+10 结构全谱实测） | **强但够不到闸**（差 0.68/0.36） |
| 评级变化 | `mdl106_stars` × `ts_delta(66)` | S 0.77 / 2Y 0.37 | 不够 |
| 坏消息因子 / DL 聚类 / 内部人强度 | `fnb` / `stock_cluster_dl` / `insider_matrix` | ≤0.05 | 判死 |

### 5.2 DEU 全域最终资源表（273 条合规表达式 / 30 波实证）

| 机制/字段 | 天花板 | 状态 |
|---|---|---|
| **预期变化率（`eps_y1_estimate_change_3mo`）** | **S1.77 / F1.61 / 2Y1.83** | **已提交 ACTIVE（`2rjrMZ25`）** —— DEU 唯一过闸者 |
| 同腿变体（框架/HYBRID/核心/桶粒度/starmine） | 1.51–1.81 | 与已提交者相关 0.986–0.999，**永久封存** |
| `netprofit_y1_estimate_change_3mo` | 1.42 | 差 0.16，全结构用尽 |
| **`mdl106_rv`（估值评分）** | **0.90** | 第二机制，全杠杆用尽（含中性化） |
| `ts_delta(stars,66)` 评级变化 | 0.77 | 2Y 不够 |
| 残差动量 / news 事件族 / sentiment / shortinterest / insiders / pattern_scores | ≤0.64 | 判死 |
| earnings / option / macro / socialmedia / imbalance | — | **DEU 无数据** |

### 5.3 结论

**「挖掘 10 个可提交 regular alpha」在 DEU 不可达成** —— 这已不是配方问题，而是**资源事实**：
1. 全 DEU 172 数据集中，携带过闸信号的机制**只有 1 个**（标准化预期变化率），其唯一载体字段已提交（`2rjrMZ25` ACTIVE）；
2. 第二强的独立机制（`mdl106_rv` 估值评分）天花板 0.90，距闸差 0.68，30 种结构/轴/聚合/中性化组合全部实测封顶；
3. 未点亮类别 19 个有覆盖数据集全部判死；其余类别在 DEU 无数据。

**⇒ 在不换 region 的约束下，DEU 的可提交产出已 100% 兑现（1/1）。要继续产出，必须换区域（EUR/GBR/USA 等有 15+ 类未点亮塔与更全的数据授权）。**

---

## 六、全量对账（2026-10-13 补，WANL31 后定案）

**问题**：「所有数据集都分析过吗？」→ 台账对账后补测了最后漏网，现答案为**是**。

| 类 | 数量 | 明细 |
|---|---|---|
| **A 已实测** | 41 | 32（台账可查）+ 9（本会话实测但台账 dataset 列缺失：model106/model30/news104/news17/news50/other532/risk88/model26/other47 部分） |
| **B 语义判死（无需回测）** | 2 | `analyst48`（7 字段全是 index 代码/计数元数据）；`insider_matrix.director_intensity_score`（平台描述明写 **"timing/bookkeeping indicator for internal sequence logging"** = 记账指示器） |
| **C 漏网补测（WANL31）** | 10 字段 | `other47` 8 字段（搜索流量族，max S 0.22）、`fundamental22.fnd22_value`（ESG KPI，**S 0.50 / 2Y 1.01**）、`stock_cluster_dl` PCA 特征（0.10）——全部不够闸 |
| **D 无可用字段（cov<0.6）** | 147 | 无数据 / GROUP 轴专用（pv29/pv30/other455）/ 低覆盖（model109/multifactor_return_pred 等） |

**WANL31 明细**：`fnd22_value` 0.50、`oth47_rank` ±0.22、`paid_search_visitors` −0.37、`oth47_organic_keywords` 0.01、PCA 特征 0.10 ⇒ **全部远低于 1.58 闸**。

**⇒ 283 条合规表达式 / 31 波后，DEU 全部 172（平台）/193（本地台账）数据集均已分析完毕，无遗漏。可提交产出 = 1 颗（已 ACTIVE）。**

---

## 七、方法论复核：「探针太少导致找不到信号？」（用户质疑的实证检验）

### 7.1 质疑成立的部分（两个真实缺口）

**① 结构缺口（已证实）**：WANL14 用「A 级框架」杀掉 10 个 starmine 字段，但框架对 starmine 是**错误结构**（同字段框架 0.97 → DEU 核心 1.81，差 0.84）。那些字段从未用正确结构重测。
**② 字段覆盖缺口**：大池子探测率低——`model26` 11/398（3%）、`pattern_scores` 34/504（7%）、`starmine` ~50/583（9%）、`analyst7` 68/425（16%）。若信号稀疏（<1% 字段携带），10 字段探针确实可能漏。

### 7.2 补测实证（WANL32：错杀字段 × 正确结构）

| 字段（cov 0.973、α=0 真空白） | DEU 核心下 S | 2Y |
|---|---|---|
| `analyst_downward_revision_count_fy1_revenue_7d_5`（反向） | **0.90** | **−0.38**（信号集中在早年） |
| `model26.mdl26_revisions` | 0.75 | 0.96 |
| `analyst_upward_revision_count_fq1_revenue_30d` | 0.40 | 0.67 |
| `revenue_revision_score_3`（cov 1.0、α=0） | 0.34 | 0.37 |
| 其余 6 个 up/down count 字段 | ≤0.28 | ≤0.37 |

⇒ **用正确结构重测后无一接近 1.58**；最强的 0.90 还因 2Y=−0.38（早衰）不可用。**「错杀」假设被数据否定。**

### 7.3 为什么「探针少」不是主因（三条结构性论据）

1. **机制是字段族属性，不是单字段属性**：同机制族内字段高度相关（eps_y1 ↔ starmine 同机制字段 PnL 0.991；analyst 9 个 change 字段在正确结构下 1.30–1.81）⇒ 族内有信号时，任一字段的正确结构都会显现——不存在「只有第 400 个字段才有」的稀疏模式。revision count 家族 10 个字段齐测（0.11–0.90）互相印证。
2. **平台竞争度证据**：唯一过闸候选 prod=0.651 ⇒ 平台已存在大量同机制 alpha；α=0 的字段族（revision counts）实测 0.11–0.40 ⇒ 「零竞争」确因无信号。
3. **结构空间已双向覆盖**：两种已验证结构（框架/DEU 核心）× 全部机制族都测过；rv/残差动量/评级变化在两种结构下一致失败。无法排除「存在第三种神奇结构」，但其先验已被 12 次「结构切换无改善」的实测压低。

### 7.4 残余不确定性（诚实声明）

结构空间是 84 算子的组合空间，**无法数学证明**「不存在某结构让 rv/别的字段到 1.58」。但继续在 DEU 扫结构的边际期望，显著低于**换区域复用已验证结构挖未点亮塔**（那里有 15+ 类未点亮塔和完整数据授权）。

**⇒ 终值：293 条 / 32 波。DEU 结论不变：唯一可提交 = `2rjrMZ25`（已 ACTIVE）。**
