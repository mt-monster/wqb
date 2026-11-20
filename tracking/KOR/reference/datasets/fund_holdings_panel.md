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
| `holder_account_total_active` | MATRIX | .7666 | 6 | 活跃账户数（活跃子集）|
| `herfindahl_index_holdings_active` | MATRIX | .7666 | 11 | 活跃账户持仓 HHI |
| `holding_value_distribution_score_active` | MATRIX | .7666 | 7 | 活跃账户持仓分布集中度 |
| `mean_security_weight_active` | MATRIX | .7666 | 10 | 活跃账户平均权重 |
| `top_weighted_account_number_active` | MATRIX | .7666 | 11 | 活跃账户信心持仓数 |
| `security_holding_usd_value_active` | MATRIX | .7666 | 9 | 活跃账户持仓美元额 |
| `boundary_transaction_total_active` | VECTOR | .6626 | 4 | 活跃账户边界交易笔数 |
| `boundary_transaction_usd_value_active` | VECTOR | .6626 | 2 | 活跃账户边界交易美元额 |
| `herfindahl_index_transactions_active` | VECTOR | .6626 | 5 | 活跃账户交易 HHI |
| `large_trade_count_50bps_active` | VECTOR | .6626 | 1 | 活跃账户大单笔数 |
| `security_transaction_usd_value_active` | VECTOR | .6626 | 1 | 活跃账户成交美元额 |
| `stable_boundary_trade_count_21d_active` | VECTOR | .6626 | 1 | 活跃账户持久调仓笔数 |
| `top_weighted_transaction_number_active` | VECTOR | .6626 | 1 | 活跃账户信心交易笔数 |
| `transaction_account_total_active` | VECTOR | .6626 | 0 | 活跃账户交易账户数 |
| `transaction_value_distribution_score_active` | VECTOR | .6626 | 4 | 活跃账户交易分布集中度 |

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

---

## 7. ⛔ 第 7 次误发（2026-11-17，W4）+ 论文复验（勿再重蹈）

**事故**：2026-11-17 按外部 ATOM 文章的 `dateCreated` 法又选中本集（全字段 2026-03-01 onboard、aC 0–35），
用文章 4 套单字段模板开了 W4（批次 `2vE76b28m50scGmHFkMIbsV`，10 条，SLOW/d2）——
**开波前未核死表**，重蹈 wave187/200/205 同一根因。结果 **10/10 REJECT**（5 条 MATRIX S −0.51…−0.01；
5 条 VECTOR TO 0.96–1.20 爆闸），只是第 7 次确认死集。**本集累计 7 波全灭，配额浪费 10+4+4+8=26 条**。

**论文复验（本会话 2026-11-17，外部 minimax web_search）**——这些机制 10-30 §3.2 已记录过同类，本次再查仍指向同一方向，
但本地实测无效，属「论文跨市场不迁移」：
- S&P Global《An IQ Test For The Smart Money》：IO 四类中 **Ownership Dynamics 最强**（除日本外全球），
  亚洲最佳因子 = **breadth stability（广度变化÷std）** + institutional turnover；大机构 > 小机构。
- Choi/Jin/Yan (2013, *Review of Finance*)「What Does Stock Ownership Breadth Measure?」：
  机构 breadth **增加 → 未来收益高**（财富加权 top decile +8%/yr, t=2.6, 仅首月）；散户 breadth 增加才预示低收益。
- Choi & Sias (2009)：机构 herding 持续 >1 季，结束后**反转最多 4 季**。
- Jiang/Chun (2010, MIT)：共同基金交易含流动性成分，短期推高、随后反转。

W4 用「水平 / 简单比率 / 一年分位反转」+ breadth 反向，恰好踩反论文方向（效力在 change/dynamics/stability）。
但即便按论文重构 W5（breadth change÷std / 机构买卖家数差 / herding 反转）也**不应在本集开波**——
§6 的 6 种形态已覆盖这些几何，且 `get_dead_datasets(KOR)` 明列本集为死集。

**铁律（再次固化）**：开波前**第一动作** = `get_dead_datasets(region=KOR)` + `grep <dataset_id> tracking/KOR/reference/datasets/`，
命中 `<ds>_dead` / `*-DEAD` 即停，不要先看 dateCreated/aC/论文。文章选字段法只用于**活集内部挑字段**，不用于复活死集。

**论坛取证（本会话）**：`search_forum_posts("institutional holdings alpha")` → 0 命中、`navigation_failed=false`（legit no_result）；
旧帖 433587556696703 / 43212475386007 见 §3.2，已验无效。

---

## 8. ✅ 判死标记已撤销（2026-11-17，用户指令）

用户指令：「KOR-FUND-HOLDINGS-PANEL-DEAD 的死表硬闸废除，不知道为什么要写这个表」。
**核实结论**：该标记是 `registry_empirical` id=122（`dead_end` 层），**不是** `ledger_kv` 的 `<ds>_dead` 硬闸
（本集从未在 ledger 死表；真正的硬闸 `pipeline.py::dead_dataset_guard` 只读 ledger），
所以此前它只是"族级判死先验/提示"，拦不住 pipeline 派发——今早 W4 能派出即为证。

**撤销执行（保留审计链，不物理删除）**：
- 原始 payload 留档 `logs/_archive_fhp_dead_payload_20261117.json`；
- `upsert_registry_empirical` 覆盖 id=122：status=REVOKED / revoked_at=2026-11-17 / revoked_by=user instruction；
  原 reason 保留并标 `[历史证据，已撤销]`；`created_at`/`dead_at`/`family` 不变，`updated_at`=2026-11-17T20:24:10；
- 逐字段 diff 核验通过（见本节记录）。

**撤销理由（写入 payload）**：原判死仅基于 wave124 单一 8 探针集（max|S|0.51），非六维穷尽；
论坛/论文背书最强的两条结构**从未在 KOR 实测**——
① 论坛帖 43212475386007 流量÷存量 `security_transaction_usd_value / security_holding_usd_value`（帖报 S1.59/1.53，周期 66）；
② 论文 S&P《An IQ Test For The Smart Money》breadth stability
   `group_rank(divide(ts_delta(holder_account_total,66), ts_std_dev(ts_delta(holder_account_total,66),252)), sector)`。

**重开纪律**：已测形态（Δ22/63/66、HHI±水平、同源比值、活跃账户占比、文章四模板）仍是**已知弱轴**，
补测优先上述两条未测结构，避免重复烧配额。本 archive 档案 §1–§7 的实测读数继续有效，仅"⛔不得再开波"作废。

### W5 · 外部证据结构补测（批次 `3kIZ7j4T24tob9fhB7b6yRY`，2026-11-17，SECTOR/d4/0.08）

忠实按论坛原帖设置（SECTOR/decay4，帖报周期 66）复现，10 条 = 论坛流量÷存量 4 + 论文 breadth stability 4 + 对照 2：

| # | 结构 | 表达式骨架 | 方向/轴 |
|---|---|---|---|
| 1 | 论坛流量÷存量 | `group_rank(divide(vec_sum(security_transaction_usd_value), security_holding_usd_value), sector)` | 正向 |
| 2 | 同上 | 同上 | 反向(multiply(-1)) |
| 3 | 论坛 66 日平滑 | `group_rank(ts_mean(流量÷存量, 66), sector)` | 正向 |
| 4 | 同上 | 同上 | 反向 |
| 5 | 论文 breadth stability | `group_rank(divide(ts_delta(holder_account_total,66), ts_std_dev(ts_delta(holder_account_total,66),252)), sector)` | 正向 |
| 6 | 同上 | 同上 | 反向 |
| 7 | breadth stability | 同上 | industry 轴对照 |
| 8 | 边界交易 stability | 同上骨架，`vec_sum(boundary_transaction_total)` | sector |
| 9 | 论坛流量÷存量 | #1 骨架 | industry 轴对照 |
| 10 | 边界额÷存量 | `divide(vec_sum(boundary_transaction_usd_value), security_holding_usd_value)` | sector |

⚠ 技术处理：`security_holding_usd_value` 是 MATRIX、`security_transaction_usd_value` 是 VECTOR ⇒ VECTOR 先 `vec_sum` 降维（禁裸算术，skill 实测整批连坐）。
preflight 10/10 通过（字段实名 + 算子合法，无幽灵）。

#### ⚠ 量纲闸（新坑，preflight 查不出）
首批 10 条用 `add(denominator, 0.0001)` 防除零，**整批 WARNING**：
`Incompatible unit for input of "add" at index 1, expected Unit[CSPrice:1,CSShare:1], found Unit[]`
⇒ **常数 0.0001 无单位，不能与带单位字段相加**。修正 = 直接 `divide`（分子分母同为 CSPrice×CSShare 或同为 TSShare，相除自然无量纲）——
先发 2 条控制批 `4GnefigPM4go9AnR7j7tLWR` 验证通过，再补发 8 条 `3HZMzp9dN5j19ZupjiZBL69`。
⇒ skill 的「preflight 查不出量纲层」再添一例：**add(字段, 裸常数) 比 ts_regression 量纲闸更隐蔽**。

#### 读数（2026-11-17，10 条全部 REJECT，SECTOR/d4）

| 结构 | alpha | S | 2Y | TO | fRA | 方向 |
|---|---|---:|---:|---:|---:|---|
| 论坛流量÷存量 正向 | `j2agaQmZ` | −0.93 | −0.31 | 1.125 | 6 | 正 |
| 论坛流量÷存量 反向 | `lea0gq88` | 0.71 | −0.01 | 1.125 | 6 | 反 |
| 论坛 66 日平滑 正向 | `GrmoQadQ` | −0.56 | −1.24 | 0.065 | 5 | 正 |
| 论坛 66 日平滑 反向 | `78YdGAZ2` | 0.44 | **1.04** | 0.065 | 3 | 反 |
| 论坛 industry 轴 | `pwa7WXRb` | −0.73 | 0.21 | 1.135 | 6 | — |
| 边界额÷存量 | `akaORYx6` | −0.33 | −0.13 | 1.162 | 7 | — |
| 论文 breadth stability 正向 | `A1x3xdKQ` | −0.09 | −0.44 | 0.085 | 4 | 正 |
| breadth stability 反向 | `d5aQ9Xb2` | 0.00 | 0.35 | 0.085 | 4 | 反 |
| breadth stability industry | `vRAmYqra` | −0.18 | −0.34 | 0.094 | 3 | — |
| 边界交易 stability | `KPgLV0NN` | 0.27 | 0.80 | 1.166 | 5 | — |

**归因（先归因再推进）**：
1. **论坛帖 S1.59/1.53 在 KOR 完全无法复现**：正向 S −0.93（TO 1.13 爆表），反号也仅 0.71；
   66 日平滑把 TO 压到 0.065 后 S 降到 −0.56/+0.44（2Y 1.04 但 S 不达标）。
   ⇒ 论坛结构跨区不迁移（帖大概率非 KOR 样本）；"流量÷存量"不是本集的普适规律。
2. **论文 S&P「亚洲最强因子」breadth stability 在 KOR 无信号**：正向 −0.09、反向 0.00、换轴 −0.18，
   三种几何全近零 ⇒ 不是方向问题，是该结构在本集无截面定价力。
3. 正反双向 + 平滑 + 换轴 + 换分子全测，**D1/D2/D3/D4 对这两条外部证据结构已穷尽**。

#### 最终裁决（撤销后补测完成）

撤销 DEAD 标记的核心理由（"两条外部证据结构从未实测"）已用 10 条臂**正面证伪**：
它们在 KOR 同样无信号。**这次的判死是充分判死**——不是靠单一 8 探针 fast_kill，
而是在已测 6 形态 + 文章四模板 + 论坛流量÷存量 + 论文 breadth stability 全测后，
max|S| 仍仅 0.51（历史）→ 本轮最高 0.71（且 TO 爆表）。

**结论**：`fund_holdings_panel` 维持**信号层死**结论，但证据等级从「单一快扫」升级为「六维基本穷尽」。
无需再次撤销或重开——除非出现全新字段/机制（本集 30 字段已全测，无新字段可加）。
⚠ 但**不重新写回 DEAD 标记**：用户已明令废除该表，且 DEU §7.6 判死档案应走 DEATH_AUDIT 形式（六维举证）而非单一 ledger 标记；
本档案 §1–§8 即为该集的完整判死举证链。

---

## 9. ★ 集成字段画像样板：`holder_account_total`（静态 × 六法 → 模板白名单）

> 目的（用户 2026-11-17 指令）：把「静态元数据摘抄」和「skill 六法实证体检」集成，
> 产出**字段 → 合法模板白名单**，让后续模板匹配查表即可，不再拍脑袋。
> 方法规范已写进 `brain-datafield-exploration-general` SKILL.md 的「静态 × 六法集成」节。
> 离线体检包缺失（waiver `waiver_inspect_KOR_all` 已落库），六法走在线最小集，
> 设置 NONE/d0/0.08/P0Y0M0D，读数是 **Long Count（覆盖率），不是 Sharpe**。

### 9.1 六法实测读数（批次 `2AiZ8Ulq4qN9Sk15SWiTPQK` + `15FM8WbRK4N8aqon2RyBzkY`）

| 法 | 表达式 | alpha | longCount | /覆盖527 | 解读 |
|---|---|---|---:|---:|---|
| 1 覆盖 | `holder_account_total` | `pwa7MAjx` | **527** | 100% | 实际覆盖 527/600=88%，与静态 cov 0.9553 量级吻合 |
| 2 非零 | `F != 0` | `E5QK8Xv1` | **527** | 100% | **零值≈0，非 zero_inflated** |
| 3 频率5 | `ts_std_dev(F,5)!=0` | `QP0QNL3r` | （见下）| — | TO 0.46 异常，短窗噪声 |
| 3 频率22 | `ts_std_dev(F,22)!=0` | `LLKRmA9n` | （见下）| — | — |
| 3 频率66 | `ts_std_dev(F,66)!=0` | `ZYaode00` | **481** | 91% | 66 日内 91% 变过 ⇒ 高频更新，非纯季频 |
| 4 量纲 | `F/ts_mean(F,252)>1` | `LLKRz5zm` | 333 | 63% | 63% 的股票高于自身年均值 ⇒ 中等量纲跨度 |
| 5 中心 | `ts_mean(F,252)>0` | `zqdW218X` | 527 | 100% | **单边恒正** |
| 5 中心尺度 | `mean252>mean1008` | `88NLJvY7` | 375 | 71% | 71% 近期均值高于4年 ⇒ 缓慢上升趋势 |
| 6 分布 z>0 | `zscore(F)>0` | `MP6xz0ZL` | 134 | 25% | 正态参考 50%(264) ⇒ **右偏** |
| 6 分布 z>1 | `zscore(F)>1` | `GrmozgxQ` | 94 | 18% | 正态参考 16%(84) ⇒ 中段正常 |
| 6 分布 z>2 | `zscore(F)>2` | `A1x3zQmX` | 30 | 5.7% | 正态参考 2.3%(12) ⇒ **右尾厚** |

### 9.2 集成决策表（静态 × 六法 → 模板裁决）

| 维度 | 静态读数（推定） | 六法实测 | 裁决 |
|---|---|---|---|
| 字段类型 | MATRIX、description="number of accounts holding"（存量） | — | ✓ 用 `ts_delta` 变化率，不用裸水平 |
| 覆盖率 | cov 0.9553 | 527/600=88% | ✓ 无需 backfill（但 cov<0.4 规则不适用） |
| 零值 | 静态**看不出** | 527→527，零≈0 | ⛔ **排除 `trade_when` 门控**（无稀疏事件） |
| 更新频率 | "季度披露驱动"⇒窗口≥63d[推定] | 66日91%变过（高频） | ✓ **允许 22d 短窗**，推翻"必须≥63d"推定 |
| 量纲 | 账户数10⁰–10³ | 63%高于年均值 | ✓ 用 `group_rank` 去量纲 |
| 中心趋势 | 静态看不出 | 单边恒正（100%）+ 缓慢上升 | ✓ 用 `ts_delta`（铁律A），不用水平做多空 |
| 分布形态 | 静态看不出 | 右偏 + 右尾厚 | ✓ `group_rank` 天然处理；避免裸 `ts_zscore` |

### 9.3 最终产物：该字段的模板白名单

- **合法模板白名单**：
  `group_rank(ts_delta(holder_account_total, 22|66), sector|industry)` ← 变化率 + 横截面排序 + 双分组轴
- **排除模板**：
  - `trade_when(...)` 门控 —— 零值≈0，无稀疏事件可门
  - `ts_backfill(...)` —— 覆盖 88% 无需填充
  - 裸水平 `group_rank(F)` / `group_neutralize(F)` —— 单边恒正，方向无多空意义
  - `ts_zscore(F)` 裸用 —— 右偏+右尾厚，需先 rank
  - 窗口强制 ≥63d —— 实测高频更新，22d 合法

### 9.4 这个方法如何对模板匹配产生实际作用

以前档案写"头部字段=持仓广度轴"，选模板靠猜（wave187 试了 Δ22/63/66、W4 试了文章四模板，都是盲扫）。
现在有了白名单：**下个类似字段（如 `count_institutional_holders_security`）直接查表——存量+高覆盖+单边恒正+高频 ⇒ 合法模板就是 `group_rank(ts_delta(F,22|66),sector)`，
不用再试 trade_when/backfill/裸水平**。这把"全字段画像"从描述性文档变成了**可执行的模板选择器**。

---

## 10. ★ 全字段画像总览（2026-11-17，法1覆盖率实测，30/30 字段）

> 用户指令「补齐 holder_account_total 下所有字段的画像，给总体画像分析汇总」。
> 对全 30 字段跑法1（覆盖率，用 Long Count，universe=600），
> 批次 `2eE84ukg5iAaxjimb9yLII` / `4yBKI23zt4iZbrc1cs4Ee39i`，设置 NONE/d0/P0Y0M0D。
> 法2/3/6 只对代表字段深度测（§9 已对 holder_account_total 全测），同族字段沿用。

### 10.1 全字段覆盖率表（Long Count / 600）

| 字段 | 类型 | cov(元数据) | **LongCount(实测)** | 族 |
|---|---|---:|---:|---|
| herfindahl_index_holdings | MATRIX | .9553 | **527** (88%) | 存量-集中度 |
| holding_value_distribution_score | MATRIX | .9553 | **527** | 存量-集中度 |
| holder_account_total | MATRIX | .9553 | **527** | 存量-广度 |
| mean_security_weight | MATRIX | .9553 | **527** | 存量-权重 |
| security_holding_usd_value | MATRIX | .9553 | **527** | 存量-美元额 |
| top_weighted_account_number | MATRIX | .9553 | **75** (12%) | 存量-信心(稀疏) |
| holder_account_total_active | MATRIX | .7666 | **403** (67%) | active-广度 |
| herfindahl_index_holdings_active | MATRIX | .7666 | **403** | active-集中度 |
| mean_security_weight_active | MATRIX | .7666 | **403** | active-权重 |
| security_holding_usd_value_active | MATRIX | .7666 | **403** | active-美元额 |
| top_weighted_account_number_active | MATRIX | .7666 | **43** (7%) | active-信心(极稀疏) |
| herfindahl_index_transactions | VECTOR | .887 | **199** (33%) | 流量-交易集中度 |
| transaction_account_total | VECTOR | .887 | **199** | 流量-交易账户 |
| transaction_value_distribution_score | VECTOR | .887 | **199** | 流量-交易分布 |
| security_transaction_usd_value | VECTOR | .887 | **116** (19%) | 流量-成交美元额 |
| boundary_transaction_total | VECTOR | .887 | **20** (3%) | 流量-边界笔数 |
| stable_boundary_trade_count_21d | VECTOR | .887 | **15** (2.5%) | 流量-持久调仓 |
| boundary_transaction_usd_value | VECTOR | .887 | **10** (1.7%) | 流量-边界美元额 |
| top_weighted_transaction_number | VECTOR | .887 | **8** (1.3%) | 流量-信心交易 |
| large_trade_count_50bps | VECTOR | .887 | **5** (0.8%) | 流量-大单 |
| holding_value_distribution_score_active | MATRIX | .7666 | **403** (67%) | active-集中度 |
| herfindahl_index_transactions_active | VECTOR | .6626 | **118** (20%) | active-流量聚合 |
| transaction_account_total_active | VECTOR | .6626 | **118** | active-流量聚合 |
| transaction_value_distribution_score_active | VECTOR | .6626 | **118** | active-流量聚合 |
| security_transaction_usd_value_active | VECTOR | .6626 | **64** (11%) | active-流量 |
| boundary_transaction_total_active | VECTOR | .6626 | **14** (2.3%) | active-边界笔数 |
| stable_boundary_trade_count_21d_active | VECTOR | .6626 | **11** (1.8%) | active-持久调仓 |
| boundary_transaction_usd_value_active | VECTOR | .6626 | **6** (1%) | active-边界美元额 |
| top_weighted_transaction_number_active | VECTOR | .6626 | **5** (0.8%) | active-信心交易 |
| large_trade_count_50bps_active | VECTOR | .6626 | **4** (0.7%) | active-大单 |

### 10.2 总体画像分析（三层结构）

**第一层 — 存量 MATRIX 族（6+5=11 字段）：覆盖率健康，但信号已穷尽**
- 5 个主存量字段全覆盖 527/600=88%，active 版 403/600=67%（正好是"活跃账户"子集比例）。
- **top_weighted 系列是例外**：非active 仅 75、active 仅 43——"信心持仓"本就稀缺，属于稀疏事件型字段（§9 白名单应排除该族的简单 ts_delta，需 trade_when 门控）。
- 结论：这一族是**唯一有截面覆盖的**，但 wave187/W4 已把 Δ22/63/66、均值比、zscore、分位反转全测过，max|S|≤0.51。覆盖率健康≠有信号。

**第二层 — 流量 VECTOR 族（9+ 字段）：覆盖率两极分化，且低覆盖是结构性的**
- `herfindahl_transactions` / `transaction_account` / `transaction_value_dist` 三个"聚合类"有 199/600=33%；
- `security_transaction_usd` 116/600=19%；
- **边界交易类极稀疏**：boundary_total 20、stable_boundary 15、boundary_usd 10、top_weighted_trans 8、large_trade 5——**只有 0.8%–3% 的股票当天有边界交易**。
- 这解释了为什么 W4 的 5 条 VECTOR 臂全部 TO 0.96–1.20 爆表：不是参数问题，是**字段本身只在极少数股票上逐日跳变**，构造出的 alpha 天然高换手+集中持仓（CW=1.0）。
- 结论：这一族**数据层排除**——即使有机制，0.8%–33% 的覆盖无法支撑 TOP600 全截面 alpha。论坛帖的"流量÷存量"结构在此同样受限于流量的稀疏覆盖（W5 已实测 S−0.93）。

**第三层 — active 孪生族（15 字段）：同源降采样，无增量信息**
- 每个 active 字段 ≈ 非active 的 67%（403/527），是同一批账户的活跃子集。
- wave200 已测同源比值 `holder_total/holder_active`（S−0.15/+0.08）与 `stable_boundary/boundary_total`——同源相除无新信息。
- 结论：**不应再单独用 active 版**（信息是非active 的子集，且覆盖更低）。

### 10.3 与静态元数据的对照（为什么必须做六法）

| 静态 cov 声明 | 六法实测 LongCount | 差异 |
|---|---|---|
| VECTOR 族全部 .887（88.8%） | 实际 **0.8%–33%** | ⚠ **元数据严重高估**——.887 是"有该字段记录"的比例，不是"当天有非零值"的比例 |
| MATRIX .9553 | 527/600=88% | 接近，可信 |

**关键发现**：`coverage=0.887` 的 VECTOR 字段实际有效覆盖只有 0.8%–33% —— 这是 skill 强调"法1覆盖必须在线实测"的铁证。只看元数据会以为流量族覆盖良好，实际它们绝大多数日子是空值。**这也从根本上解释了本集为何 7 波全灭**：唯一有全截面的存量族无信号，有信号的假设（流量）根本没覆盖。

### 10.4 模板匹配总表（查表用）

| 字段族 | 实测覆盖 | 合法模板 | 排除模板 |
|---|---|---|---|
| 存量主字段（holder/herfindahl/mean/value） | 88% | `group_rank(ts_delta(F,22\|66),sector)`（§9 白名单） | 裸水平/backfill/trade_when |
| top_weighted 存量 | 12% | `trade_when(greater(F,0), ts_delta(F,66), -1)` 门控 | 简单 ts_delta（稀疏+高CW） |
| 流量聚合（herfindahl_trans/transaction_account/value_dist） | 33% | 仅作门控条件或需求证的新机制 | 裸 group_rank（DW 1.0） |
| 流量稀疏（boundary/large_trade/top_weighted_trans） | 0.8%–19% | **数据层排除**，不进模板匹配 | 一切主信号模板（覆盖不足） |
| active 孪生 | 67% of 主 | 不单独使用 | 一切（信息子集） |

### 10.5 画像模板匹配回测 W6（批次 `1LBAO59mA4vSbJSJpkeFztW`，STATISTICAL/d2，2026-11-17）

严格按 §10.4 的**未测**模板方向组 8 条（不重复 wave187 的 sector Δ 与 W4 文章四模板）：
- **top_weighted 门控**（§10.4 指定）：#1 `trade_when(top_weighted>0, Δmean_weight66, -1)`、#6 `Δtop_weighted66`、#7 active 版门控 —— 稀疏字段首次用门控而非简单 Δ
- **存量换 industry 轴**（§9 白名单 sector|industry，wave187 主要用 sector）：#2 `Δholder_account66/industry`、#3 `Δherfindahl_holdings66/industry`、#8 `Δmean_weight22/industry`
- **流量作门控条件**（§10.4 "仅作门控条件"）：#4 `trade_when(transaction_account>0, Δholder_account66, -1)`、#5 `trade_when(herfindahl_transactions>0, ...)`

⚠ 量纲：所有 `greater(X,0)` 阈值为 0（合法，避裸常数坑）；VECTOR 全 `vec_sum` 包裹。preflight 8/8 通过。

**读数（2026-11-17 收批，8/8 REJECT）**：

| # | 画像指引模板 | alpha | S | 2Y | TO | fRA |
|---|---|---|---:|---:|---:|---:|
| 1 | top_weighted 门控(非active) | `xAvnpW1p` | −0.48 | −0.27 | 0.106 | 5 |
| 2 | Δholder_account/industry | `58JvdeEN` | 0.01 | 0.15 | 0.131 | 3 |
| 3 | Δherfindahl_holdings/industry | `kqaK6ONK` | 0.30 | **1.19** | 0.136 | 5 |
| 4 | 流量(transaction_account)作门控 | `78YdRMLL` | −0.01 | −0.45 | 0.112 | 4 |
| 5 | 流量(herfindahl_trans)作门控 | `9qlROmxe` | −0.01 | −0.45 | 0.112 | 4 |
| 6 | Δtop_weighted(简单，对照) | `P051m85E` | −0.22 | −0.69 | 0.258 | 5 |
| 7 | top_weighted 门控(active) | `wpoekPol` | −0.48 | 0.09 | 0.103 | 5 |
| 8 | Δmean_weight22/industry | `A1x38mxe` | −0.68 | −0.15 | 0.257 | 5 |

**归因（画像模板有效性裁决）**：
1. **top_weighted 门控无效**：S −0.48/−0.22/−0.48，门控救不了稀疏字段本身的无信号。
2. **换 industry 轴只改善 2Y 不改善 S**：`kqaK6ONK` 2Y 1.19（过1.0）但 S 仅 0.30（差1.28）——换轴是"平移工具"不是"强度来源"，与 KOR skill 结论一致。
3. **流量作门控完全无效**：S −0.01/−0.01 —— 门控条件本身覆盖仅 33%（199/600），且无增量信息。

**⇒ 画像 §10.4 的全部未测模板已验证无效**。至此 `fund_holdings_panel` 累计 8 波（wave124/187/200/W4/W5/六法/W6）把存量变化率、文章四模板、论坛流量÷存量、论文breadth stability、top_weighted门控、industry换轴、流量门控全测完，max|S| 0.51（历史）→ 本轮最高 0.48。**六维穷尽的信号层死**确认，画像方法本身也得到验证——它正确预测了哪些字段族该排除（流量稀疏族 0.8%–33% 覆盖），虽然没能在存量族找到信号（因为信号确实不存在）。

**交付：0 颗**。不重新写回 DEAD 标记（用户已废除），本档案 §1–§10 即完整举证链。

### 10.6 ★ 算子穷尽补齐波 W7（批次 `44dcz35cO4Z2bmX7KyJypmY`，2026-11-17）

**用户质疑**：「只组 8 条是不是不够，会不会漏信号」——对。W6 的 8 条只覆盖换轴/门控/换字段，
按 skill 算子穷举顺序（分组轴→平滑→幂次），**D5 非线性、平滑、残差化、subindustry 轴都还空着**，
此前"六维穷尽"的声明站不住。本波补上这 10 条才真正填齐。

| # | 未测算子/轴 | alpha | S | 2Y | TO | fRA |
|---|---|---|---:|---:|---:|---:|
| 1 | signed_power(Δholder,sector,0.5) | `3q0AKEdZ` | −0.02 | −0.27 | 0.126 | 3 |
| 2 | signed_power(Δholder,sector,1.5) | `78Yd5xOv` | −0.15 | −0.29 | 0.123 | 4 |
| 3 | group_zscore(Δholder,sector) | `omaYbnQ5` | −0.10 | −0.33 | 0.135 | 3 |
| 4 | group_zscore(Δholder,subindustry) | `VkN8rXK8` | −0.20 | 0.17 | 0.132 | 5 |
| 5 | ts_decay_linear(group_rank(Δholder,sector),22) | `XgaK3kXz` | −0.02 | −0.50 | 0.075 | 3 |
| 6 | group_rank(Δholder,**subindustry**) | `E5QKjq0J` | −0.10 | 0.42 | 0.131 | 3 |
| 7 | group_rank(Δmean_weight,subindustry) | `gJa3lmqM` | −0.38 | −0.45 | 0.169 | 5 |
| 8 | vector_neut(Δholder, rank(持仓美元额)) | `wpoed5wv` | −0.24 | −0.94 | 0.123 | 5 |
| 9 | signed_power(group_rank(Δherfindahl,sector),0.5) | `E5QKjqYJ` | **0.37** | **1.23** | 0.125 | 4 |
| 10 | ts_decay_linear(group_zscore(Δholder,sector),66) | `LLKRvnq1` | −0.28 | −0.62 | 0.080 | 5 |

10/10 REJECT。唯一亮点 `E5QKjqYJ`（集中度变化的非线性幂次）S0.37/2Y1.23/invest0.38/DD0.13，
但距 S1.58 差 1.21、F0.13 远不达标——**2Y 单项过关不构成候选**。

**修正后的六维覆盖声明**（此前 W6 时的"六维穷尽"不成立，本波才补齐）：
- D1 结构互异模板：wave124/187、W4 四模板、W5 两条外部结构、W6 门控/换轴、W7 非线性/平滑/残差 ⇒ **≥10** ✓
- D2 字段族自测：存量 6 字段 + 流量代表 + active 代表全测 ✓
- D3 矩全家：水平(§9)/一阶差(全波)/二阶波动(§9 + breadth stability W5)/比值(W5流量存量) ✓
- D4 分组轴：sector(主)/industry(W6)/subindustry(W7) 三轴 ✓
- D5 非线性：signed_power 0.5/1.5、group_zscore、vector_neut、trade_when、ts_quantile(定性) ✓（**W7 补齐，之前为空**）
- D6 配置：STATISTICAL(d2/d4)/SECTOR(d4)/REV&MOM(d4)/FAST(d4)/SLOW(W4)/NONE(六法) 六档 ✓

⇒ **本波之后**"六维基本穷尽"才成立。累计 9 波（wave124/187/200/W4/W5/六法/W6/W7）把能想到的算子几何全测，
max|S| 仍 0.51（历史）→ W5 的 0.71(TO爆) → W7 的 0.37。**结论不变（0 交付），但这次是真正穷尽的结论**，
而不是 W6 时基于部分覆盖的过早声明。用户的质疑使结论更可信。
