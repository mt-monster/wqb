# KOR / fund_holdings_panel（基金持仓与申赎面板，MATRIX+VECTOR）

> 塔：**institutions**（KOR/D1 未点亮，乘数 **1.4**）
> 画像日期 2026-10-30 · 数据源 `mcp__wqb-db__get_field_catalog`（30 字段，全量）
> 区域：KOR / TOP600 / Delay=1

---

## 1. 字段全表（按覆盖 × αC 排序）

| 字段 | 类型 | cov | αC | 经济含义 |
|---|---|---|---|---|
| `herfindahl_index_holdings` | MATRIX | **.9553** | **10** | 持仓权重 HHI（0–1），持有人集中度 |
| `holding_value_distribution_score` | MATRIX | **.9553** | 8 | 持仓市值在账户间分布集中度，**拥挤度代理** |
| `holder_account_total` | MATRIX | **.9553** | 6 | 持有该 ISIN 的机构/基金账户数 = **持仓广度** |
| `mean_security_weight` | MATRIX | **.9553** | 6 | 持有人平均组合权重（占各自 AUM） |
| `top_weighted_account_number` | MATRIX | **.9553** | 4 | 把该股当「信心持仓」（前 30% 权重）的账户数 |
| `security_holding_usd_value` | MATRIX | **.9553** | 1 | 全体账户持仓美元市值 |
| `boundary_transaction_total` | VECTOR | .887 | **11** | **边界交易笔数**（新开仓 + 完全清仓），本表 αC 最高 |
| `stable_boundary_trade_count_21d` | VECTOR | .887 | 3 | 前 21 个工作日在该股无边界交易的账户所发生的边界交易 ⇒ **持久性调仓** |
| `security_transaction_usd_value` | VECTOR | .887 | 2 | 当日成交美元额 |
| `boundary_transaction_usd_value` | VECTOR | .887 | 2 | 边界交易美元额 |
| `transaction_value_distribution_score` | VECTOR | .887 | 2 | 当日成交额在账户间集中度（0–1） |
| `top_weighted_transaction_number` | VECTOR | .887 | 2 | 「信心持仓」相关交易笔数 |
| `herfindahl_index_transactions` | VECTOR | .887 | 1 | 成交额跨账户 HHI |
| `transaction_account_total` | VECTOR | .887 | 0 | 当日交易的账户数 |
| `large_trade_count_50bps` | VECTOR | .887 | 0 | 单笔 > 基金 AUM 0.5% 的大单笔数 |
| `*_active`（8 个同构孪生） | M/V | .6626–.7666 | 1–7 | **仅「活跃账户」子集**重算：`herfindahl_index_holdings_active`(αC 7)、`top_weighted_account_number_active`(6)、`mean_security_weight_active`(3) |

⚠ **`_active` 后缀 = 活跃账户子集**（覆盖 .6626–.7666）。同名字段两版**信息同源但样本不同**：
全量版覆盖高、`_active` 版噪声低但会丢 25% 的名字。**同一波内不要同时扫两版**（同族窗口谱 = 死轴纪律）。

---

## 2. 五问画像

| 问 | 读数 | 结论 |
|---|---|---|
| **时间维度** | 持仓类（HHI / 账户数 / 权重）为**存量**；`boundary_transaction_*` / `security_transaction_usd_value` 为**流量** | 存量 ⇒ `ts_delta`（铁律 A）；流量 ⇒ 可直接水平用 |
| **相对性** | HHI / 分布分数为 **0–1 有界比值**；账户数 / 笔数为**计数** | 有界比值 ⇒ `rank`/`ts_rank`；计数 ⇒ `rank` 前先 `ts_mean` 降噪 |
| **被定价的是谁** | **主动型共同基金与机构账户**的申赎与调仓（13F 式多头披露，45 天申报滞后） | 见 §3 A-2 |
| **有无博弈** | 有：**拥挤**（HHI 高）本身就是流动性风险；且 KOR 有长期卖空限制历史 | 需 `sector` 组内归一（产业内拥挤度不同） |
| **事件性** | 非事件型：既有日频面板（.9553），也有稀疏的边界交易（VECTOR，很多名字为 0） | 面板主体**禁 `trade_when`**；仅边界交易支路可门控 |

**量纲**：HHI/分布分数 0–1 无量纲；账户数 10⁰–10³；美元额 10⁶–10¹⁰ ⇒ **必须先去量纲**（`rank`/`group_rank`），禁裸水平入式。

**更新频率**：持仓类为**季度披露驱动**（13F 45 天滞后）⇒ **窗口 ≥ 63d**，短窗会被 NaN 与前视污染；
成交/边界交易为**日频**。

**十年覆盖**：`institutions6` 描述明确 "more than 10 years of history"；`fund_holdings_panel` 覆盖 .9553 且为面板型 ⇒ 待 wave 187 收批后按 `get_alpha_yearly_stats` 逐年核（用户约束 #4）。

---

## 3. ① → ② 接线

### 3.1 A-2 收益来源声明（硬门）

| 声明项 | 内容 |
|---|---|
| **谁在被定价** | 主动型基金的**申赎流**与**调仓决策**。13F 式披露只含多头、45 天滞后，且基金账户的边界交易（新开仓/清仓）是**真实的信心变化**，不是价格噪声 |
| **为什么会被错** | ① **注意力摩擦**：披露滞后 45 天 + 覆盖 600 只股票，散户与量化拥挤在价格类因子上 ⇒ 持仓广度信息在 1–2 个月内未被充分定价（Chen-Hong-Stein 2002 的 short-sales-constraint 版本在 KOR 尤其成立：KOR 2020-03→2021-05、2023-11→2025-03 两轮**全面禁卖空**）② **forced selling**：HHI 高的股票在基金赎回时被强制卖出，价格压力随后反转（Coval-Stafford 2007） |
| **错了多久修复** | **22–66 交易日**（一个披露周期 + 一个季度调仓） |
| **预期方向** | 持仓**广度 ↑**（账户数增）⇒ 后续收益 **↑**；持仓**集中度 ↑**（HHI 增）⇒ 后续收益 **↓**；**持久性边界交易**（`stable_boundary_trade_count_21d`）⇒ 知情加仓 ⇒ 收益 **↑** |

### 3.2 双通道取证

**通道 A｜BRAIN 论坛**
- `433587556696703`（23 票）「机构参与『新鲜度门』」：用 `institutions6` 的 `count_institutional_buyers_security`——「本季度增持该公司的机构数量（活跃买方流，13F 式披露，慢变但真实知情）」，方向为**做多增持广度**。⇒ 与本表 `holder_account_total` / `top_weighted_account_number` 同机制。
- `43212475386007`（25 票）「从社区来到社区去」：明确给出 fund_holdings_panel 的**流量/存量对**——`security_transaction_usd_value / security_holding_usd_value`、`quantity/holdings`、`trade_significance/holdings`，**同号，S 1.59 / 1.53**；并给**事件周期 = 66（季度）**。⇒ 窗口取 **63/66**，且「流量 ÷ 存量」是本表已验证的结构。

**通道 B｜外部论文**
- Chen, Hong & Stein (2002, *JF*) "Breadth of Ownership and Stock Returns"：卖空约束绑定时，**广度上升预测未来收益上升**。KOR 有真实卖空禁令史 ⇒ 适用性强（本区制度契合，非照搬）。
- Coval & Stafford (2007, *JFE*) "Asset Fire Sales (and Purchases) in Equity Markets"：基金流驱动的价格压力，**后续反转**。
- Gompers & Metrick (2001, *JF*) 机构羊群：机构持仓变化含信息但慢变。

**裁决**：A、B **指向同一机制**（机构持仓广度 / 流量）⇒ ⭐ 优先组装。A 给窗口（66）与流量÷存量结构，B 给方向句与持有期（22–66d）。

⚠ **不可迁移标记**：Chen-Hong-Stein 样本为 USA 小盘、NYSE/AMEX；KOR 为 TOP600 大盘、制度不同 ⇒ 只作**假说**，必须本区实测。

---

## 4. Wave 187 候选（首波 probe，**15 条**，全 ATOM）

> 设计纪律：存量 ⇒ `ts_delta`（铁律 A）；季频 ⇒ 窗口 ≥63；计数 ⇒ 先 `ts_mean` 后 `rank`；VECTOR ⇒ 先 `vec_sum`；方向按铁律 B 正反各留一条。
> **本波不碰**：`_active` 孪生版（同族窗口谱死轴）、`security_holding_usd_value` 裸水平（价格×份额混淆）、多字段相加（混信号）。
>
> ⚠ **口径校正（2026-10-30 03:30）**：DB 里 wave 187 实际落库 **15 条**——首轮 02:39 写入的 8 条中，
> 只有 `ts_delta(holder_account_total, 22)` 与本表 F2 指纹相同被 upsert 更新，其余 7 条作为**补充诊断腿**保留。
> 它们不是冗余：F9/F13 是窗口谱对照，F10/F11/F12 是**水平 vs 变化率**对照，F15 是 F3 的**符号反向**（铁律 B），
> F14 是唯一一条 VECTOR 交易面腿。**本表以 DB 为准**（pipeline 只读 DB），下表 15 行 = 实际派发集。

| # | 表达式 | 机制支路 | 预期 |
|---|---|---|---|
| F1 | `group_rank(ts_delta(holder_account_total, 63), sector)` | 持仓广度变化（Chen-Hong-Stein） | S 正 |
| F2 | `group_rank(ts_delta(holder_account_total, 22), sector)` | 同上短窗对照（Q 披露内的加速） | 弱于 F1 |
| F3 | `group_rank(multiply(-1, ts_delta(herfindahl_index_holdings, 63)), sector)` | 去集中化 = 广度扩散 | S 正 |
| F4 | `group_rank(multiply(-1, herfindahl_index_holdings), sector)` | 拥挤度水平（Coval-Stafford） | S 正 |
| F5 | `group_rank(ts_delta(mean_security_weight, 63), sector)` | 持有人平均权重 ↑ = 信心加仓 | S 正 |
| F6 | `group_rank(ts_delta(top_weighted_account_number, 63), sector)` | 信心持仓账户数 ↑ | S 正 |
| F7 | `group_rank(ts_delta(holding_value_distribution_score, 63), sector)` | 市值分布集中度变化（对照 F3，检验 HHI vs 分布分数的信息差） | 待测 |
| F8 | `reverse(group_rank(ts_delta(holder_account_total, 63), sector))` | **铁律 B 反向**：因截断×decay 非对称，反向未必精确反号 | 待测 |
| F9 | `group_rank(ts_delta(holder_account_total, 66), sector)` | 窗口谱对照（66 vs 63；**若两者读数逐位相同则窗口为死轴**） | ≈F1 |
| F10 | `reverse(group_rank(holding_value_distribution_score, sector))` | **水平型** + 反向：检验「分布分数」是存量还是流量 | 待测 |
| F11 | `group_rank(holding_value_distribution_score, sector)` | **水平型**正向（F10 的对侧腿，铁律 B） | 待测 |
| F12 | `group_rank(top_weighted_account_number, sector)` | 信心持仓账户数**水平**（F6 的存量版对照） | 待测 |
| F13 | `group_rank(ts_delta(mean_security_weight, 22), sector)` | 短窗信心加仓（Q 披露内加速；F5 的 22 窗对照） | 弱于 F5 |
| F14 | `group_rank(vec_sum(stable_boundary_trade_count_21d), sector)` | **唯一交易面腿**：边界成交笔数（VECTOR ⇒ `vec_sum` 降维） | 待测（CW 风险） |
| F15 | `group_rank(ts_delta(herfindahl_index_holdings, 66), sector)` | **F3 的符号反向**（集中化而非去集中化），铁律 B | 待测 |

**门控支路留到 wave 188**（不在首波）：`trade_when(greater(vec_sum(boundary_transaction_total), 0), ...)` —— 事件日集中是 KOR 事件类数据通病（CW 1.0），首波先测面板主体，避免 CW 噪声掩盖真实信号。

---

## 5. 提交层风险（预登记）

| 风险 | 判据 |
|---|---|
| **2Y 闸 1.58** | 本表收益来自季度披露，**慢变** ⇒ 结构上利于 2Y（同 `earnings3` 的 `next_interval` 先例），但需逐年核 |
| **Turnover** | `ts_delta(·, 63)` 换手低（季度变化）⇒ 大概率落在 LOW_TURNOVER 侧；TO < .125 时 Fitness 用 .125 分母，**对 F 有利** |
| **CW** | 面板主体（.9553 覆盖）不应出现 CW；若 CW 高说明因子退化成少数名字 |
| **DATA_DIVERSITY** | 单数据集 ATOM ⇒ 该项大概率 PASS，但 KOR 塔内 institutions 已有 94 αC，`MATCHES_PYRAMID` 需实测 |

---

## 6. 实测记录

| 波次 | 状态 | 备注 |
|---|---|---|
| 124 | **CLOSED FAIL（判死）** | 8/8 RED，max\|S\|=0.51 ⇒ `KOR-FUND-HOLDINGS-PANEL-DEAD`（"do not probe fund_holdings_panel again; event-aggregate flow fields here are noise"） |
| 187 | **CLOSED FAIL（误发第 1 次）** | 15 式过门禁、实际只发出 4 腿（`holder_account_total` Δ22/Δ66、`holding_value_distribution_score` ±）：S 0.28 / −0.04 / −0.17 / −0.03，max\|S\|=0.28。**CW 全过（含 2014 早期点）** ⇒ 反证 wave186 的 CW 失败是 earnings3 早期覆盖薄的伪影，不是本区通病 |
| **200** | **CLOSED FAIL（误发第 2 次）** | 4 腿 = 两条**同源比值**（`stable_boundary_trade_count_21d / boundary_transaction_total`、`holder_account_total / holder_account_total_active`）各正反两向，`hump(..., 0.003)` 包裹：`O0AK3qaJ` −0.15 / `58ENX3WX` +0.08 / `bl67wvMq` −0.32 / `mLoevZA6` +0.25；max\|S\|=**0.32**，TO **.0626–.0851 全部落在获胜带 .075–.136 内** ⇒ **不是换手问题，是机制缺失**（同源比值也没救回来）。两次误发的根因见 `unlit_towers_roadmap_20261030.md` §4「流程禁区」：priors 死名单被 `MAX_DEADENDS=12` 截断，闸看不见本集的死条目（已修） |

**结论（写给未来的自己）**：本集 **6 个不同机制形态**（账户数变化 Δ22/Δ66、持股市值分布分数 ±水平、边界成交/总笔数比值 ±、活跃账户占比 ±、流通/持仓比值）**全部 \|S\| ≤ 0.51**，且换手始终在获胜带内 ⇒ **不是参数问题也不是换手问题，是 KOR 账户级持仓聚合本身无截面信息**。⛔ 不得再开波；任何"新角度"先核对 `KOR-FUND-HOLDINGS-PANEL-DEAD` 原文。
