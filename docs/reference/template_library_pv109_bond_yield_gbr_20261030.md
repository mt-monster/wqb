# pv109（公司债收益率/信用利差）GBR 模板库 — 2026-10-30

## 0. 数据集事实（平台实读，非缓存）

| 项 | 值 | 来源 |
|---|---|---|
| dataset_id | `pv109` | `get_datafields` |
| category | PV（⇒ 金字塔塔位 = **PV**） | dataset id 前缀 + 字段语义 |
| region / universe / delay | GBR / TOP700 / D1 | `get_datafields` 参数 |
| 字段数 | **26，全部 VECTOR 类型** | `get_datafields(max_fields=80)` |
| 覆盖率 | **0.3319（全 26 字段一致）** | 同上 |
| 历史回测 | **全库 0 条**（`alphas` 表 `dataset_id LIKE '%pv109%'` 与表达式含 `yield_to_maturity`/`bond_coupon` 均为空） | 本地库 `wqb.db` |

**⇒ 结论：这是 GBR 侧唯一「高机制价值 + 零历史试错」的处女地数据集。**
机制与当前 10 条篮子（分析师修正 / 基本面 Δ / 模型分 / 概率分）**完全正交**，
对 self-corr 与 prod 都是新增自由度。

### 0.1 字段分档（按可否直接参与运算）

| 档 | 字段 | 维度 | 处理约定 |
|---|---|---|---|
| **A · 无量纲收益率/比率（首选）** | `midpoint_yield_to_maturity`、`bid_side_yield_to_maturity`、`ask_side_yield_to_maturity`、`midpoint_conversion_yield`、`bid_side_conversion_yield`、`ask_side_conversion_yield`、`bond_coupon_rate`、`current_coupon_rate` | % | 同单位可相减；最后统一 `rank()` 收口 |
| **B · 价格（同单位可相除）** | `midpoint_trade_price`、`initial_issue_price`、`last_traded_price`、`lowest_ask_price`、`highest_bid_price`、`redemption_value_amount`、`minimum_bond_denomination`、`minimum_trade_increment` | 货币 | **只做比值**（价/价）；不可与常数比较或相加 |
| **C · 金额/数量（必须先 `rank()` 或相除）** | `face_value_amount`、`pv109_amt_issued`、`pv109_amt_outstanding`、`total_traded_volume` | 货币/张数 | `vec_sum` 后必须 `rank()`；**禁 `add(·, ε)`** |
| **D · 编码/日期（禁作信号）** | `bond_maturity_structure`、`coupon_type_description`、`coupon_payment_frequency`、`interest_day_count_basis`、`pv109_maturity`、`pv109_announce_dt` | 代码/日期 | 只能当条件（`greater`/`less`），或直接不用 |

### 0.2 三条硬约束（GBR + VECTOR + VERIFY）

1. 所有 26 字段都是 **VECTOR** ⇒ 任何标量算子（`ts_*`/`rank`/`divide`/`subtract`）外层必须先包 `vec_avg` / `vec_sum` / `vec_stddev` / `vec_max` / `vec_min` / `vec_count`。
2. `unit_handling=VERIFY` ⇒ **不能给带单位字段加无量纲常数**；比值一律同单位相除，**不要用 ε**（`add(vec_sum(x), 0.0001)` 必挂）。
3. 覆盖率仅 0.3319 ⇒ 每条候选都要额外看 `LOW_SUB_UNIVERSE_SHARPE`（GBR/TOP700/D1 的 limit = **0.4743 × sharpe**）与 `LOW_ROBUST_UNIVERSE_SHARPE`（limit 0.7）。

---

## 1. 十个结构互异模板

> 编号 P1–P10。「结构差异」落在 **信息加工方式（水平 / 一阶差分 / 二阶 / 截面离散度 / 相对比值）+ 字段家族 + 分组轴** 上，
> 不是换窗口或换常数。

| # | 模板 | 表达式骨架 | 经济机制 | 方向先验 | 来源 |
|---|---|---|---|---|---|
| **P1** | 信用利差**水平**截面排序 | `rank(ts_backfill(vec_avg(midpoint_yield_to_maturity), 66))` | Merton (1974) 距离违约：YTM 高 = 杠杆/违约风险高。风险补偿 vs 困境折价方向待实测 | **待定（探针首要目的）** | paper：Merton 1974；Campbell-Hilscher-Szilagyi 2008 RFS |
| **P2** | 信用利差**动量**（Δ 一季） | `rank(ts_delta(ts_backfill(vec_avg(midpoint_yield_to_maturity), 66), 66))` | 利差走阔 = 信用恶化前瞻 ⇒ 未来股票收益**负**。利差变化含增量信息、水平不含 | **负**（表达式取负号更可能为正收益） | paper：Chordia-Shivakumar 2005 JF；Gilchrist-Zakrajšek 2012 AER |
| **P3** | 买卖价差（**流动性/不确定性**） | `rank(subtract(ts_backfill(vec_avg(ask_side_yield_to_maturity), 66), ts_backfill(vec_avg(bid_side_yield_to_maturity), 66)))` | 报价价差 = 非流动性溢价（Amihud 2002）。宽价差 ⇒ 要求更高收益 | **正**（非流动性溢价） | paper：Amihud 2002 JFM；Dick-Nielsen-Feldhütter-Lando 2012 JFE |
| **P4** | 债券**折价率**（市价 / 发行价） | `rank(divide(ts_backfill(vec_avg(midpoint_trade_price), 66), ts_backfill(vec_avg(initial_issue_price), 66)))` | 深度折价 = 折价债券（distressed debt）⇒ 权益困境风险高 | **负**（折价深 ⇒ 未来收益低） | paper：Campbell-Hilscher-Szilagyi 2008；自建定价结构 |
| **P5** | 同一发行人**多债收益率离散度** | `rank(vec_stddev(midpoint_yield_to_maturity))` | 资本结构复杂度 / 债券间定价分歧 ⇒ 不确定性折价 | **负** | 自建（Merton 多债扩展）+ 论坛 `43244714809367`「vec_stddev 作分歧度」 |
| **P6** | **债务扩张**（存量变动） | `rank(ts_delta(ts_backfill(vec_sum(pv109_amt_outstanding), 252), 252))` | 杠杆上升 ⇒ 负向（杠杆异象 / trade-off theory） | **负** | paper：Bhandari 1988 JF；Modigliani-Miller 权衡理论 |
| **P7** | 债券**成交活跃度**（关注度溢出） | `rank(ts_mean(vec_sum(total_traded_volume), 66))` | 债券市场关注度向权益溢出；高成交 = 信息进入价格 | **正**（关注度） | paper：Gervais-Kaniel-Mingelgrin 2001 JF（注意力） |
| **P8** | **票息率**水平（历史遗留信用质量） | `rank(ts_delta(ts_backfill(vec_avg(bond_coupon_rate), 252), 252))` | 高票息 = 发行时高风险的粘性印记；变化极慢 ⇒ 天然低换手 | **正**（高票息高风险 ⇒ 风险补偿） | 自建（sticky signal，专攻换手闸） |
| **P9** | **赎回价 / 面值**（条款价值） | `rank(divide(vec_avg(redemption_value_amount), vec_avg(face_value_amount)))` | 赎回条款溢价反映发行人对提前赎回的定价，跨发行人可比 | **正** | 自建（合同条款定价） |
| **P10** | 行业内**相对信用利差** | `group_rank(ts_backfill(vec_avg(midpoint_yield_to_maturity), 66), sector)` | 同 sector 共享宏观敞口，行业内相对利差剥离行业 beta，只留个体信用 | **待定** | 自建（P1 的行业中性变体）；论坛 `31365517513495` 分组口径 |

### 1.1 模板间独立性自评（避免伪多样性）

- P1/P10 是同一字段的**未分组 vs 分组**版本 ⇒ 相关性预计 **0.6–0.9**，同时进池只为回答「行业中性是否必要」，不作两条独立收益源。
- P2 与 P1 用同一字段但**信息加工相反**（水平 vs 一阶差分），慢变序列下相关性通常 0.1–0.3 ⇒ 可并存。
- P3（ask−bid）、P5（`vec_stddev`）、P9（条款比值）是**真正互不相关的三支**，各自用不同字段家族。
- P6/P7 共用 `vec_sum` 但一个是存量变化、一个是流量水平，且字段不同（`amt_outstanding` vs `total_traded_volume`）。
- P4/P9 都是价格比值，但一个是「市价 vs 发行价」（困境），一个是「赎回价 vs 面值」（条款），分子分母语义完全不同。

### 1.2 换手预判（省回测配额）

债券数据**季度更新**，YTM/coupon 类字段本身粘性极高 ⇒ P1/P5/P8/P9/P10 预计 TO < 10%（可直接过 `HIGH_TURNOVER` 0.70 硬闸）。
P2（`ts_delta` 66）与 P6（`ts_delta` 252）是**唯一两个会产生换手的模板**，若 TO 超标按既定顺序治理：
**① 先扫平台 `decay ∈ {4,6,8,10,12}`（同 TO 下 S 最高）② 再上 `ts_target_tvr_decay` ③ 最后才动表达式**。
——该优先级已由 ISA/GBR 多族实证（平台 decay 同 TO 下 S 高 26%、2Y 高 12%、R 高 24%）。

---

## 2. 首波探针选择与理由

**派发 P1 + P2（同一 `midpoint_yield_to_maturity` 字段的水平 vs 动量）**，理由：

1. 处女地首波的核心问题不是「哪个模板最优」，而是**「水平有没有信号」+「变化有没有增量」**——P1/P2 一次回答两个问题。
2. 若 P1 有效而 P2 无效 ⇒ 该字段是**慢变量价值型**，后续优先 P8/P9/P10 的低换手路线。
3. 若 P2 有效而 P1 无效 ⇒ 该字段是**信用动量型**，后续优先 P6/P4 的差分路线，并把 P2 的窗口做 22/66/252 梯度。
4. 若两者都 < 闸的 40%（即 S < 0.63）⇒ 该字段家族判死，转到 P3（不同字段家族，唯一还能救的角度）。

**设置**：`STATISTICAL` + `decay 4` + `trunc 0.08` + `maxTrade ON` + `nanHandling ON` + `pasteurization ON` + `unitHandling VERIFY`
（与 GBR PV/MODEL/other 族已验设置一致）。

---

## 3. 已完成的零成本闸

| 检查 | 结果 |
|---|---|
| `preflight_expressions`（10 条） | `valid: true`、`unknown_fields: []`、`unknown_soft: []` |
| `operator_audit` | `safe: true`、`violations: []`（无幽灵算子） |
| 幽灵/不可访问算子 | 表达式中**不含** `ts_max`/`ts_min`（本账号 ERROR）及 19 个幽灵算子 |
| trio 塔混 | `pv109` 是**纯 PV 单数据集** = 单塔 alpha，**不触碰**「PV/MODEL/OTHER 两两禁混」，**不吃** trio×非trio 的 5 条配额 |

---

## 4. 待补

- 近十年数据核验：探针出货后，对候选跑 `get_alpha_yearly_stats` 逐年核 `longCount` / `pnl`，**不看平台 `coverage`**。
- 论坛/论文补查：`pv109` 暂无论坛直接模板（本次 `search_forum_posts` 检索词未命中债券类目），机制层依赖上述 Merton / Chordia-Shivakumar / Amihud / Campbell 四篇。
- 若 P1–P10 全灭，判死依据按「最大 S / 闸 1.58」比值写台账，并注明覆盖率 0.3319 是可能的结构性原因（不是模板问题）。
