# GBR × `institutions6` 模板库与判死账本

> 区域：**GBR**｜宇宙：**TOP700**（该区唯一）｜延迟：**D1**｜类别：`institutions`｜倍率：**1.4**
> 期间：2026-10-31｜口径：`REGULAR / GBR / TOP700 / D1 / FAST / decay 15 / trunc 0.05 / nanHandling ON / maxTrade OFF / pasteurization ON / unitHandling VERIFY`
> **结论：本数据集在 GBR 上纯单塔不可出货（4 探针天花板 S 0.56）⇒ INSTITUTIONS 塔结构不可达点亮。**

---

## §0 为什么挑这个数据集

GBR D1 塔位表实测：`model=5` / `analyst=3` / `pv=1` / `other=1` / `news=0` / **`institutions=0`** / 其余全 0。
`institutions6` 是**全 GBR 唯一还有高覆盖数据集的未点亮塔位**：

| 属性 | 值 | 判读 |
|---|---|---|
| coverage | **1.0**（11 字段全部 1.0） | 满足决策 #76 的「≥0.96 才不崩」硬要求 |
| 字段类型 | **全部 MATRIX** | 无需 `vec_*` 折叠，无 VECTOR 折叠噪声 |
| alphaCount | 881 / userCount 393 | 平台已充分挖掘 |
| 倍率 | 1.4 | 高于 SHORTINTEREST 的 1.2 |

`institutions` 类目在 GBR 共 5 个数据集，其中 **3 个零覆盖或低覆盖**（`institutions25` cov 0 / `institutions1` 0.3118 / `institutions4` 0.39），`fund_holdings_panel`（0.9099）已 24 探针判死 ⇒ **`institutions6` 是唯一载体，无兄弟数据集可换**。

---

## §1 字段清单（11 个，全 MATRIX，4 个语义族）

| 语义族 | 字段 | userCount / alphaCount |
|---|---|---|
| **流量·广度**（家数） | `count_institutional_buyers_security` | 108 / 159 |
| | `count_institutional_sellers_security` | **136 / 193**（全集最高） |
| | `count_institutional_holders_security` | 66 / 89 |
| **流量·规模**（股数） | `quantity_institutional_shares_acquired` | 98 / 131 |
| | `quantity_institutional_shares_disposed` | 65 / 87 |
| **流量·价值**（金额） | `market_value_institutional_shares_acquired` | 69 / 107 |
| | `market_value_institutional_shares_disposed` | 59 / 78（最低） |
| **存量** | `aggregate_share_count_institutions` | 80 / 113 |
| | `aggregate_equity_value_institutions` | 89 / 117 |
| | `aggregate_share_count_all_owners` | 85 / 128 |
| | `aggregate_equity_value_all_owners` | 72 / 91 |

**语义结构**：`acquired/disposed` 是**季度汇总的净变化**（不是逐笔事件），`aggregate_*` 是**季度持仓快照**。全表是「季度披露 + 季内前向填充」的慢变量。

---

## §2 GBR 探针账本（4 条，全灭；天花板 S 0.56）

| # | 骨架 | alpha | S | F | 2Y | SUB | TO | DD | failed_ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| T1 | **流量/存量比·家数**：`ts_rank(ts_sum(divide(buyers−sellers, holders), 66), 252)` | `wpQwZ626` | **0.56** | 0.20 | 0.82 | **−0.08** | 7.60% | 6.27% | 4 |
| T2 | **流量/存量比·股数**：`ts_rank(ts_sum(divide(qty_acq−qty_dis, agg_share_inst), 66), 252)` | `E560pEgP` | 0.42 | 0.12 | −0.13 | 0.31 | 7.13% | 6.02% | 3 |
| T3 | **流量/存量比·家数，纯横截面**：`group_rank(divide(buyers−sellers, holders), subindustry)` | `0mYkXEop` | −0.22 | −0.05 | −1.58 | −0.23 | 7.68% | 13.64% | 4 |

全部套 `ts_target_tvr_decay(group_neutralize(…, densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)` 外壳。

### 2.1 三条读法

1. **T1 的 SUB −0.08 是决定性的** —— 子宇宙里完全没有信号。机构持仓数据天生偏大盘：小票的 `holders`（持仓机构家数）接近零或缺失，分母不稳 ⇒ 信号只存在于大票，而大票已被充分定价。
2. **T3 比 T1 更差（−0.22 vs 0.56）⇒ 推翻了「季度填充值毁了时序分位」的假设。** 派 T1 时我预判「季度数据 + 日频前向填充 ⇒ `ts_rank` 大面积并列 ⇒ 时序分位失真」，并设计 T3（纯横截面 `group_rank`）来隔离这个因素。T3 更差说明**病根不在加工层，而在信号本身不存在**。这是「加工层调参无法修复信号缺失」的又一实证。
3. **天花板 0.56 与 IND 独立测出的 `|S| ≤ 0.58` 精确吻合** —— 两个区域、两套设置、不同宇宙，结论一致 ⇒ 不是 GBR 特例。

---

## §3 跨区证据：IND 已把这条路走完（8 类机制证伪 + ATOM 上限 1.10）

来源：`reports/ind_institutions6_alpha_delivery_20261023.md` + `docs/reference/IND/institutions6_field_profile.md`。

### 3.1 §2.2 已证伪清单（IND 24 条，全部 `|S| ≤ 0.58`）—— **本表应作排除表用**

| 机制 | 代表表达式 | 实测 | 与 GBR 本轮的关系 |
|---|---|---|---|
| 原始净流量 | `rank(acq_q − dis_q)` | S ≤ 0.58 | ← **T1/T2 命中**（净差 ÷ 存量） |
| 买入广度 | `rank((buyers−sellers)/(buyers+sellers+1))` | S ≤ 0.58 | ← **T3 命中**（净差 ÷ 持仓家数，near-duplicate） |
| 换手/churn | `rank((buyers+sellers)/holders)` | S ≤ 0.58 | 同族 |
| 机构占比水平 | `rank(share_inst/share_all)` | S ≤ 0.58 | 水平量被 size 主导 |
| 净价差（成交价） | `rank(mv/qty_acq − mv/qty_dis)` | S ≤ 0.58 | 价差方向无信息 |
| 时序相关 | `rank(−ts_corr(ts_zscore(flow,63), returns, 252))` | S 0.34–0.49 | 相关结构不稳 |
| 反向残差 | `rank(−ts_regression(flow, returns, rettype=0))` | S −0.13~0.13 | 方向必须固定「returns 对 F」 |
| 增长门 | `greater(ts_delta(F))` | S 0.49–0.58 | 论坛结论跨区复现失败 |

### 3.2 唯一有效的模板必须吃 PV 额度

IND 黄金模板（10 颗全过闸，S 2.81–3.20，设置 `decay 126 / STATISTICAL / trunc 0.08`）：

```
rank( -ts_regression( ts_zscore(returns, 252), ts_zscore(<F>, 252), 252, rettype=0 ) )
```

**但它含 `returns`（PV 内置字段）⇒ 每一条都是 PV+INSTITUTIONS 双塔**（IND 报告 §2.6：`atom_flag=combined` / `atom_n_datasets=2`，明确**不是 ATOM**）。

- 走这条路要占用 **trio × 非trio 额度**（PV 属 trio），该额度**全局上限 5，GBR 已用 4（4 条 PV+FUNDAMENTAL）⇒ 只剩 1**。
- 而点亮 INSTITUTIONS 塔需要 **3 条互相关 < 0.7** 的 alpha。IND 实测：交付 10 颗 avg 相关 0.723 / max 0.953，**两两 < 0.70 的最大子集只有 3 颗**，且那 3 颗同样含 `returns`。
- ⇒ **即使额度充足，也要消耗 3 个额度换 3 条**；现实只剩 1 个 ⇒ **不可能**。

### 3.3 ATOM-only 上限（IND §2.4 实测）

`region='IND' AND dataset='institutions6' AND atom_flag='atom'` 共 46 条 / 40 唯一表达式：
**S 最高 1.10、平均 0.07、最低 −1.06；S ≥ 1.25 的 0 条。**
最高 S 已低于平台 `LOW_SHARPE` 线 ⇒ 无需查 F/2Y 即可判不合格。

**GBR 本轮 4 条（天花板 0.56）与之同向且更低** ⇒ 纯单塔路线在两个区都被封死。

---

## §4 塔位判决：INSTITUTIONS 塔**结构不可达点亮**

三根支柱全部齐备：

| 支柱 | 证据 |
|---|---|
| ① 纯单塔上不去 | IND 46 条 ATOM-only S max **1.10**；GBR 4 条天花板 **0.56** |
| ② `returns` 残差版吃 trio 额度，额度不够 | 需 3 条，GBR 仅剩 **1** 个 trio×非trio 名额 |
| ③ 无兄弟数据集可换 | `institutions` 类目 5 个：3 个零/低覆盖、`fund_holdings_panel` 24 探针判死 |

**⇒ 不要再为「点亮 INSTITUTIONS」投入任何批位。**

---

## §5 可复用教训

1. **★★★★★ 「流量/存量比」模板的前提是「流量必须是事件型流量」。** 论坛帖 `43212475386007`（DEU `institutions1` S 1.59）成功的载体是**逐笔内部人申报**（离散事件）；`institutions6` 的 `acquired/disposed` 是**季度汇总净变化**，没有「事件」概念 ⇒ 模板前提不成立。这是该模板的**第三次失败**（DEU 成功 → GBR `insiders1` S −0.22 → GBR `institutions6` S 0.56）。
2. **★★★★ 覆盖率高 ≠ 信号大。** `institutions6` cov 1.0、11 字段、alphaCount 881，是「数据完整」的典范，但 alphaCount 高恰恰说明**被挖尽了**。判断数据集可打性时，`coverage` 只排除「太薄」，**不能预测「有货」**。
3. **★★★ 加工层调参无法修复信号缺失。** T1（时序分位）0.56 vs T3（纯横截面）−0.22 —— 换加工层只改变噪声，不制造信号。当同一机制在两种几何下都不成立时，应立刻换机制而不是换算子。
4. **★★★ SUB 是第一预警信号。** T1 的 SUB −0.08（远低于 SUB/S 门槛）在 S 还有 0.56 时就已提示「信号只在子宇宙外」——机构持仓数据的小票缺失是结构性原因，不是调参能解决的。
5. **★★★★★ 派发前必须 grep 本地台账。** 本轮 T1/T2/T3 三条全部落在 IND §2.2 的已证伪清单上，白烧 3 个批位。若动笔前先 `grep -r "institutions6" docs reports Claude/skills`，这 3 条一条都不会派。

---

## §6 存档索引

| 内容 | 路径 |
|---|---|
| 本文 | `docs/reference/template_library_gbr_institutions6.md` |
| IND 交付报告（黄金模板 + ATOM 上限） | `reports/ind_institutions6_alpha_delivery_20261023.md` |
| IND 字段画像（§2.2 已证伪清单） | `docs/reference/IND/institutions6_field_profile.md` |
| GBR 塔位现状 | `mcp__wq-brain-http__get_pyramid_alphas` |
| 本轮 4 条探针 | 平台 alpha：`wpQwZ626` / `E560pEgP` / `0mYkXEop`（+ T1 前置 preflight 2 条未派） |
