# USA / fundamental93 字段画像（S1 级 · 2026-10-30）

> 数据集元数据：**Earnings Tax Data** / 46 字段 / cov 0.6309 / userCount 45 / alphaCount 86 / **valueScore 4.0** / pyramidMultiplier 1.1
> 区域 USA / D1 / TOP3000 ｜ 类别 fundamental ｜ 塔位：FUNDAMENTAL（当前计数 0）
> **本画像结论：这是 USA fundamental 塔里「低相关红利」最强的一个集，全部字段几乎零使用。**

---

## 1. 为什么选 fundamental93（而不是 fundamental17）

| 候选 | 处置 | 理由 |
|---|---|---|
| `fundamental93` | ✅ **本波靶** | 46 字段**全部** userCount ≤ 12、alphaCount ≤ 21（部分为 0）⇒ **几乎零使用 ⇒ prod 天然低相关**；机制 = 应计质量因子（Sloan 1996），**完全正交于**估值（registry 判死）与成长（wave270 实测方向反转） |
| `fundamental17` | ⏸ 已开波但信号弱 | wave270 实测：成长/质量族 10 模板 \|S\| ≤ 0.46，且**方向与论坛帖相反**；字段多但拥挤度中等（aCnt 34967） |
| `fundamental91` | ⏸ 待侦察 | 407 字段 / cov .6051 / uCnt 197 / aCnt 496 —— 命名体系未知（`search="margin"` 返 0），但拥挤度低，值得下一波 |
| `fundamental6` | ❌ 极拥挤 | aCnt 881064（994 alpha/字段）⇒ prod 撞墙风险极高 |
| `fundamental2` | ❌ 极拥挤 | aCnt 144800 |
| `fundamental67` / `fundamental22` | ❌ 黑名单 | 前瞻 label 泄漏 / 语义不透明（见 fundamental17 画像 §1） |

---

## 2. 机制：应计质量因子（Sloan 1996 accruals anomaly）

**学术依据**：Sloan (1996)《Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Earnings?》——
会计应计（accruals = 净利润 − 经营现金流）越高，盈利的可持续性越低，市场对这类盈利**过度乐观**；
低应计（高现金含量）公司的盈利更持久 ⇒ **做多低应计 / 做空高应计**。

**为何这条路值得开**：
1. **正交性**：应计质量与估值（valuation-momentum 已由 `USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL` 判死）、与成长（wave270 实测 USA 反向）都不同族 ⇒ 不会撞同一个 prod 池；
2. **冷门**：全部字段 uCnt ≤ 12 / aCnt ≤ 21 ⇒ 低相关红利未折旧（论坛帖 43153154839831 的作者原话：「冷门字段的低相关红利会折旧」⇒ 用就要趁早）；
3. **基本面慢变量天然过 CW 闸**：wave270 实测 10/10 过 CONCENTRATED_WEIGHT + LOW_TURNOVER + HIGH_TURNOVER。

---

## 3. 字段结构画像（本集是「同一比率的多种聚合统计」设计）

设 X ∈ {accruals, expense, liability}（应计 / 递延税费用 / 递延税负债），每个比率族都有一组：

| 字段后缀 | 含义 | accruals | expense | liability |
|---|---|---|---|---|
| `_d1_current_t` | 当前值相对 LTM 窗口的 **Z-score**：(current − mean)/std | cov .3379 ★核心 | cov .5834 | cov .5445 |
| `_d1_dts` | LTM 窗口**标准差**（二阶矩） | cov .4363 | cov .6876 | cov .7158 |
| `_d1_mean` | LTM 窗口**均值**（水平） | cov .4569 | cov .7838 | cov .7415 |
| `_d1_max` | LTM 窗口**最大值** | cov .4569 | cov .7838 | cov .7415 |
| `_d1_min` | LTM 窗口**最小值** | cov .4569 | cov .7838 | cov .7415 |
| `_d1_length` | 窗口内**观测数**（数据可得性 ⇒ 本身是披露质量代理） | cov **.9274** | cov .9155 | cov .9273 |
| `*_d1_asset_change` | 资产同比变化比 | cov **.9006** | cov .8949 | cov .9005 |

**另有 16 个「税收应计 / 递延税比率」字段**（命名 `fnd93_tax_accruals_XX` / `fnd93_deferred_tax_expense_XX` / `fnd93_deferred_tax_liability_XX`，XX = 分母组 × 候选序号）：

| 字段 | cov | uCnt | aCnt | 说明 |
|---|---:|---:|---:|---|
| `fnd93_tax_accruals_11` | .4147 | 1 | 1 | **税收应计 = tax expense − cash tax paid ÷ 分母组1候选1** ★ 最接近「现金含量」原始定义 |
| `fnd93_tax_accruals_13` | .4027 | 3 | 3 | 同上，分母组1候选3 |
| `fnd93_tax_accruals_51` | .3468 | 2 | 4 | 分母组5候选1 |
| `fnd93_tax_accruals_41` | .3276 | 1 | 3 | 分母组4候选1 |
| `fnd93_tax_accruals_21/22/23/31/12` | .3159–.4136 | 0 | 0 | uCnt 0 ⇒ 无人用过 |
| `fnd93_deferred_tax_expense_11` | .8476 | 1 | 1 | 递延税费用比（分母组1候选1）★ 覆盖好 |
| `fnd93_deferred_tax_expense_12` | .8440 | 1 | 1 | 同上候选2 ★ 覆盖好 |
| `fnd93_deferred_tax_expense_31` | .8228 | 0 | 0 | 分母组3候选1 ★ 覆盖好且无人用过 |
| `fnd93_deferred_tax_expense_21` | .7306 | 3 | 4 | 分母组2候选1 |
| `fnd93_deferred_tax_expense_22` | .7248 | 2 | 2 | 分母组2候选2 |
| `fnd93_deferred_tax_expense_51` | .6422 | 0 | 0 | 分母组5候选1 |
| `fnd93_deferred_tax_expense_41` | .6120 | 0 | 0 | 分母组4候选1 |
| `fnd93_deferred_tax_liability_11/12` | .7150 | 2/1 | 2/1 | 递延税负债比（分母组1）|
| `fnd93_deferred_tax_liability_13` | .6979 | 0 | 0 | ★ 覆盖 .70 且无人用过 |
| `fnd93_deferred_tax_liability_31` | .7068 | 0 | 0 | ★ 覆盖 .71 且无人用过 |
| `fnd93_deferred_tax_liability_51` | .5744 | 3 | 4 | 分母组5候选1 |
| `fnd93_deferred_tax_liability_21/22/23/41` | .5591–.6112 | 0–1 | 0–1 | 覆盖较低 |

---

## 4. 覆盖门槛核对（用户要求「近十年都有数据」，门槛 = longCount+shortCount ≥ 0.35 × 3000 = 1050）

| 覆盖档 | 字段 | 处置 |
|---|---|---|
| **≥ 0.89（可作主线）** | `accrualsratio_d1_asset_change` (.9006)、`liability_d1_asset_change` (.9005)、`expense_d1_asset_change` (.8949)、`accruals_d1_length` (.9274)、`liability_d1_length` (.9273)、`expense_d1_length` (.9155)、`deferred_tax_expense_11` (.8476)、`_12` (.8440)、`_31` (.8228) | 可作主线位 |
| 0.61–0.79（探针位） | `expense_d1_current_t` (.5834)、`liability_d1_current_t` (.5445)、`expense_d1_dts` (.6876)、`liability_d1_dts` (.7158)、`expense_d1_mean/max/min` (.7838)、`liability_d1_mean/max/min` (.7415)、`deferred_tax_liability_11/12` (.7150)、`_13` (.6979)、`_31` (.7068) | 探针位 |
| < 0.50（仅探索） | `accruals_d1_current_t` (.3379)、`accruals_d1_dts` (.4363)、`accruals_d1_mean/max/min` (.4569)、全部 `tax_accruals_*` (.3159–.4147) | 只做机制确认，不作主线 |

⚠️ `accruals_d1_current_t` 是**机制上最核心**的字段（应计 Z-score）但 cov 仅 .3379 ⇒ **wave272 把它放主线位只为验证机制方向**，若覆盖导致 longCount < 1050，则后续波次改用 `accrualsratio_d1_asset_change`（cov .9006）作主载体。

---

## 5. wave272 模板分配（10 个结构互异模板）

| 模板 | 机制 | 字段 | 经济含义 |
|---|---|---|---|
| T01 | 应计 Z-score 取负 + 行业内标准化 | `accruals_d1_current_t` | 核心机制验证（做多低应计） |
| T02 | 资产变化比取负 + 行业内标准化 | `accrualsratio_d1_asset_change` | 覆盖最好载体 |
| T03 | 递延税费用 Z-score 取负 | `expense_d1_current_t` | 应计的另一代理 |
| T04 | 递延税负债 Z-score 取负 | `liability_d1_current_t` | 应计的另一代理 |
| T05 | 税收应计取负 | `tax_accruals_11` | 最接近「现金含量」原始定义 |
| T06 | 二阶矩轴：应计波动取负 | `accruals_d1_dts` | 高波动应计 = 低质量 |
| T07 | 水平轴：LTM 均值应计取负 | `accruals_d1_mean` | 应计水平 |
| T08 | 极值轴：LTM 最大应计取负 | `accruals_d1_max` | 应计极值 |
| T09 | 纯时序轴（无 group_*） | `accrualsratio_d1_asset_change` + ts_rank 252 | 检验纯时序动量 |
| T10 | 双机制：应计 Z-score × 递延税费用（vector_neut 残差化，非乘积） | `accruals_d1_current_t` + `expense_d1_asset_change` | 两个质量代理正交 |

---

## 6. 派发前必查清单

1. **本地既有台账三查**：`grep -r "fundamental93" docs/ reports/ Claude/skills/`（本集是首次开波，历史无记录）；
2. **逐条读 description 三分类** —— 本集 46 字段描述全部可读、**无 future / forward-looking / label / prediction 字样**（已逐条核对 46 条）⇒ 无前瞻泄漏风险；
3. **算子签名闸**（已过 10/10）；
4. **VECTOR 预检**（已过：`valid: true` / `any_changed: false` / 9 字段全 MATRIX / `vector_fields: []`）；
5. **覆盖门槛**：收批后逐条核对 `longCount + shortCount ≥ 1050`，不达标的字段在该波内直接标为不可用。

---

## 7. 跨数据集 / 跨区经验迁移记录（wave270 → wave272）

- **wave270 实测**：论坛「成长外推反转」机制在 USA **方向相反**（10 模板 7 个 S 为负）⇒ 论坛机制的方向声明不可信，必须实测；
- 但 wave270 的**质量族（利润率改善）也为负** ⇒ 与「成长外推」同向 ⇒ 两个独立机制族同向 ⇒ **USA 基本面存在「坏消息偏误」**（市场对基本面改善定价过度，后续反转）。若 wave272 的应计因子（做多低应计）也是负的，则三个机制族同向 ⇒ **USA 基本面整体是「好消息已被定价」的格局**，后续所有 fundamental 模板的方向假设都应按「取负」起手。
- **wave270 的 `ts_quantile(gaussian)` 替代 `ts_median` 失败**（TO 从 4.77% 暴涨到 22.03%）⇒ 本波不用 ts_quantile，只用 `ts_backfill` + `group_zscore` / `ts_rank`。
