# fundamental3 字段画像（USA / TOP3000 / D1）

> 生成日期：2026-10-31
> 数据来源：平台 `get_datafields`（dataset_id=fundamental3, region=USA, universe=TOP3000, delay=1）
> 平台字段总数：**788**；本次完整解析 **400** 条（含 `_fast_d1` 副本）；剔除 `_fast_d1` 后**基字段 201 个**
> 全部字段类型：**MATRIX 100%**（另 `fnd3_revision_number` / `fnd3_value` 为平台侧 VECTOR，落在同一数据集的另两个 dataset_id 变体里）
> 本文档对应波次：wave296–301（72 条 USA 回测）

---

## 0. 一句话结论

**fundamental3 是「传统财报三大报表」型数据集**（资产 / 负债 / 利润 / 现金），字段全是**季频或年频的存量与流量**。
它**不含分析师预期、不含 XBRL 修订行为、不含分数量化因子**（那是 `fundamental110` 的地盘）。

**在本数据集上唯一站住的机制是「加速度 + 组内相对化」**：

```
group_rank(ts_zscore(subtract(ts_mean(F, 252), ts_mean(F, 504)), 252), subindustry)
```

平台全闸通过（fRA=0）3 颗（wave300），最佳 `QPvjeWZp` S 1.69 / F 1.04 / 2Y 1.60 / TO 1.39%。
但 **prod 全部超线**（0.7463–0.8904），机制本体在生产池已被大量覆盖。

---

## 1. 数据集级画像

| 项 | 值 | 说明 |
|---|---|---|
| platform field count | 788 | 全量 |
| 本次解析 | 400 | `max_fields=400` 拉取上限 |
| 基字段（去 `_fast_d1`） | 201 | `_fast_d1` = 平台的**快速更新副本**，不是「预期版」 |
| 类型 | MATRIX × 400 | 无 GROUP、无 VECTOR（在本 dataset_id 下） |
| coverage 中位数 | 0.7527 | p25 0.4981 / p75 0.8085 / max 0.8502 |
| coverage ≥0.80 的字段 | 66 | 主流口径（资产、收入、EPS、现金流） |
| coverage 0.60–0.70 | 16 | 成本类、股本变动类（窄） |
| coverage <0.60 | 64 | 递延/一次性/衍生项（窄到不能单独做信号） |
| category | FUNDAMENTAL | 塔位 multiplier 1.1 |
| alpha_count（DB） | 75 | 平台侧 alphaCount 普遍 100–600（见 §4） |

### ★ 关键认知：`_fast_d1` 不是「预期」

wave296 曾用 `_fast_d1` 与非 fast 版做差分来构造「盈利意外」，结果 longCount 塌到 10–16 ⇒ CONCENTRATED_WEIGHT 0.5 必挂，12 条全灭。

**`_fast_d1` 只是同一份数据的快速更新副本**（覆盖率几乎相同：0.8065 vs 0.8064），跨版本差分没有任何「预期」信息。

⇒ **盈利意外必须用「同一字段时间变化」或「分析师预期 vs 实际」**。后者在本数据集里没有，只能走前者。

---

## 2. 字段族结构

### 2.1 前缀族（201 基字段）

| 前缀 | 数量 | 含义 | 覆盖度特征 |
|---|---|---|---|
| `fnd3_a_` | 67 | 年度（annual）原始口径 | 中高 0.70–0.85 |
| `fnd3_aacctadj_` | 62 | 年度 + 会计调整 | 中高，最干净 |
| `annual_` | 32 | 年度（另一套命名，长名字） | 0.68–0.83 |
| `fnd3_q_` | 29 | 季度（quarterly） | 0.60–0.85 |
| `current_` / `unearned_` / `other` | 11 | 流动项、递延收入、杂项 | 0.25–0.36，**很窄** |

**同一指标通常有 4 个版本**（例：EPS 有 `annual_basic_eps_value` / `fnd3_a_epsbasic` / `fnd3_aacctadj_epsbasic` / `fnd3_q_epsbasic`），
外加各自的 `_fast_d1` ⇒ **8 个变体**。这是本数据集最大的「假多样性」陷阱。

### 2.2 语义族（201 基字段，按关键词归类）

| 语义族 | 数量 | 代表字段 | 可用性 |
|---|---|---|---|
| 资产负债 | 61 | `fnd3_a_assets` / `fnd3_a_liabilities` / `fnd3_a_equity` | ★ 存量，**水平信号强、加速度弱** |
| 利润 / 税 | 39 | `fnd3_a__earbeforetaxes` / `annual_ebit_total` / `fnd3_a_ebitda` | ★★ 流量，**加速度强** |
| 现金 / 流动 | 20 | `annual_operating_cashflow_amount` / `annual_cash_change_amount` | ★★ 流量，冷门（ac 2–12） |
| 收入 / 销售 | 16 | `fnd3_a_revenue` / `fnd3_aacctadj_revenue` / `annual_sales_total` | ★★★ **最优主腿** |
| 股本 / 稀释 | 14 | `fnd3_a_avgdiluted_sha` / `annual_avg_diluted_shares_count` | ★★ 稀释股数本身是好因子 |
| 费用 / 利息 | 13 | `annual_sga_cost_total` | ★★ 费用控制力 |
| 每股口径 EPS | 10 | `annual_basic_eps_value` / `fnd3_a_epsdiluted` | ★★ 会计噪音大 |
| 成本 / 毛利 | 8 | `fnd3_a_costofrevenue` / `fnd3_aacctadj_grossprofit` | ★★★ 成本占比加速度最强 |
| 股东 / 回报 | 3 | `annual_retained_earnings_total` | ★ 冷门 |

---

## 3. 角色底账：字段按「信号角色」分类

### 3.1 主腿候选（流量项，季频连续更新 ⇒ 加速度信号最强）

实测排序（wave300，同骨架 `group_rank(ts_zscore(subtract(ts_mean(F,252),ts_mean(F,504)),252),subindustry)`）：

| 字段 | S | F | 2Y | prod | 备注 |
|---|---|---|---|---|---|
| `fnd3_aacctadj_revenue` | **1.69** | **1.04** | 1.60 | 0.8441 | ★★ fRA=0 |
| `fnd3_a_revenue` | 1.68 | 1.03 | 1.60 | — | ★★ fRA=0 |
| `fnd3_a_costofrevenue` | 1.67 | 1.03 | **1.85** | 0.8260 | ★★ fRA=0 |
| `fnd3_aacctadj_grossprofit` | 1.49 | 0.88 | 1.83 | — | 近闸 |
| `annual_accounts_receivable_total` | 1.50 | 0.86 | 1.48 | — | 近闸 |
| `fnd3_a_epsdiluted` | 1.17 | 0.65 | 1.50 | — | 近闸（+ts_rank 后 S 1.40/F 0.88/2Y 1.67） |
| `annual_basic_eps_value` | 1.35 | 0.71 | 1.32 | **0.7463** | ★ **prod 最空（桶 5284）** |
| `fnd3_q_revenue` | 1.30 | 0.77 | 0.68 | — | 季度口径 2Y 塌 |
| `fnd3_q_grossprofit` | 1.27 | 0.74 | 0.74 | — | 同上 |

**规律：流量项 > 存量项；年度口径 > 季度口径；会计调整 > 原始。**

### 3.2 辅助腿 / 条件腿（存量项、窄覆盖项）

| 字段 | cov | ac | 角色 |
|---|---|---|---|
| `fnd3_a_assets` | 0.831 | **627** | 规模代理 ⇒ **组合腿做规模中性化**，但本身太拥挤（prod 必高） |
| `fnd3_a_liabilities` | 0.830 | 229 | 杠杆 ⇒ 条件腿 |
| `fnd3_a_equity` | 0.831 | 336 | 账面价值 ⇒ 价值腿（但 ac 336 ⇒ 拥挤） |
| `fnd3_a_avgdiluted_sha` | 0.742 | 155 | 稀释股数变化 ⇒ 稀释效应因子（经典机制） |
| `annual_retained_earnings_total` | 0.797 | 2 | ★ 极冷门（ac 2）+ 高覆盖 ⇒ **未开发靶子** |
| `annual_ebit_total` | 0.825 | 1 | ★★ **极冷门（ac 1）** ⇒ 未开发靶子 |
| `annual_total_debt_amount` | 0.753 | 1 | ★★ 极冷门 ⇒ 未开发靶子 |
| `annual_operating_cashflow_amount` | 0.826 | 12 | ★★ 冷门 + 高覆盖 ⇒ 未开发靶子 |
| `annual_sga_cost_total` | 0.786 | 5 | ★★ 费用控制力，未开发 |
| `annual_gross_capex_total` | 0.788 | 7 | ★★ 资本开支强度，未开发 |
| `annual_additional_paid_in_capital` | 0.770 | 14 | ★ 股份支付，未开发 |
| `annual_equity_compensation_expense` | 0.675 | 12 | ★ 股权激励，未开发 |

### 3.3 禁用清单（覆盖太窄，做主腿必挂 CONCENTRATED_WEIGHT）

| 字段 | cov | 原因 |
|---|---|---|
| `annual_unearned_revenue_total` | 0.335 | longCount 会塌到 30–40 |
| `unearned_revenue_balance` | 0.363 | 同上 |
| `current_unearned_revenue_total` | 0.259 | 同上 |
| `annual_accrued_liabilities_change` | — | 窄 |
| `annual_intangible_assets_excl_goodwill` | — | 窄 |
| `annual_minority_interest_net_income` | — | 窄 |

---

## 4. 拥挤度台账（平台 alphaCount，USD 财报族通用）

### 4.1 高拥挤（ac ≥ 100）⇒ 单腿做 prod 必高

| 字段 | ac | uc | cov |
|---|---|---|---|
| `fnd3_a_assets` | **627** | 105 | 0.831 |
| `fnd3_a_capex` | 370 | 71 | 0.796 |
| `fnd3_aacctadj_accpayable` | 352 | 70 | 0.756 |
| `fnd3_a_equity` | 336 | 89 | 0.831 |
| `fnd3_aequitybeforenci` | 288 | 80 | 0.828 |
| `fnd3_aacctadjequity` | 270 | 88 | 0.830 |
| `fnd3_a_add_paid_cap` | 263 | 64 | 0.770 |
| `fnd3_a_accpayable` | 238 | 70 | 0.761 |
| `fnd3_a_liabilities` | 229 | 97 | 0.830 |
| `fnd3_a_retained_ear` | 220 | 75 | 0.797 |
| `fnd3_a_dnc` | 219 | 96 | 0.803 |
| `fnd3_a__earbeforetaxes` | 210 | 68 | 0.825 |
| `fnd3_aacctadjequitybeforenci` | 208 | 61 | 0.827 |
| `fnd3_a_ope_cf` | 186 | 68 | 0.826 |
| `fnd3_a_ebitda` | 182 | 51 | 0.823 |
| `fnd3_a_grossprofit` | 171 | 65 | 0.807 |
| `fnd3_aaccadj_nicdis_ope` | 165 | 60 | 0.825 |
| `fnd3_q_capex` | 164 | 58 | 0.759 |
| `fnd3_q_cash` | 161 | 60 | 0.849 |
| `fnd3_a_avgdiluted_sha` | 155 | 62 | 0.742 |
| `fnd3_aacctadj_currentliabilities` | 153 | 71 | 0.810 |
| `fnd3_q__inc_tax` | 153 | 44 | 0.728 |

### 4.2 冷门靶子（ac ≤ 25 且 cov ≥ 0.6）⇒ **优先开发**

| 字段 | ac | cov | 建议机制 |
|---|---|---|---|
| `annual_ebit_total` | **1** | 0.825 | EBIT 加速度（经营盈利趋势） |
| `annual_total_debt_amount` | **1** | 0.753 | 杠杆变化加速度（去杠杆股） |
| `annual_ebitda_total` | 2 | 0.823 | EBITDA 加速度 |
| `annual_retained_earnings_total` | 2 | 0.797 | 留存收益累积（复利能力） |
| `annual_net_income_total` | 3 | 0.827 | 净利润加速度（不同于 EPS，无股本噪音） |
| `annual_earnings_before_tax_total` | 4 | 0.825 | 税前利润加速度 |
| `annual_financing_cashflow_amount` | 4 | 0.825 | 融资现金流加速度 |
| `annual_sga_cost_total` | 5 | 0.786 | 费用率加速度（经营杠杆） |
| `annual_cost_of_sales_total` | 5 | 0.686 | 成本加速度（原始口径对照） |
| `annual_avg_diluted_shares_count` | 6 | 0.742 | 稀释股数加速度（回购/增发） |
| `annual_gross_capex_total` | 7 | 0.788 | 资本开支加速度（再投资强度） |
| `annual_cash_change_amount` | 8 | 0.767 | 现金变化加速度 |
| `annual_current_liabilities_total` | 9 | 0.816 | 流动负债加速度 |
| `annual_operating_cashflow_amount` | 12 | 0.826 | 经营现金流加速度（质量） |
| `annual_equity_compensation_expense` | 12 | 0.675 | 股权激励费用率 |
| `annual_basic_eps_value` | 14 | 0.806 | ★ 已验证：prod 最空（桶 5284） |
| `annual_gross_profit_total` | 14 | 0.807 | 毛利加速度 |
| `annual_additional_paid_in_capital` | 14 | 0.770 | 股份支付 |
| `annual_receivables_change_amount` | 15 | 0.661 | 应收变化 |
| `annual_sales_total` | 17 | 0.808 | 营收加速度（长名版本） |
| `annual_accounts_receivable_total` | 23 | 0.739 | 应收加速度 |

---

## 5. 本数据集的三条数据脾气（实测总结）

### 脾气 1：`_fast_d1` 是陷阱，不是增量
同覆盖率副本，跨版本差分必崩 longCount。**别把它当预期版**。

### 脾气 2：必须序数化（group_rank），不能幅度化
同内层下：`group_rank` S 1.08 > `group_zscore` S 0.14 > `group_neutralize` S −0.24。
- `group_zscore` 保留极端幅度 ⇒ 少数极端财报股主导组合 ⇒ TO 3.82%（最高）且 S 崩。
- `group_neutralize` 扣掉组均值 ⇒ 把「行业盈利周期」这个真实 alpha 源也扣掉 ⇒ 符号翻转。
- `group_scale` S 0.16、`ts_quantile` S 0.13 ⇒ **只有 group_rank 一条能活**。

### 脾气 3：`nanHandling` 是本数据集的头号杠杆
`batch_create_simulations` 默认 `nan_handling=OFF`。同一批设置轴：

| 中性化轴 | OFF（wave299） | ON（wave300） |
|---|---|---|
| SUBINDUSTRY（基线） | 1.35 | 1.35 |
| INDUSTRY | **−0.33** | **1.36** |
| STATISTICAL | 0.18 | 1.12 |
| SLOW_AND_FAST | 0.15 | 1.03 |

季频财报缺失率高，OFF 会让缺失票以伪值进截面 ⇒ 信号被稀释。
⇒ **本数据集任何批次必须显式 `nanHandling=ON`**。

---

## 6. 已验证机制模板库（wave296–301，10 个结构互异模板）

| # | 模板 | 表达式骨架 | 最佳实测 | 归属 |
|---|---|---|---|---|
| T1 | 裸 zscore + delta | `ts_zscore(ts_delta(ts_backfill(X,120),252),252)` | S 0.09 | ✘ 判死 |
| T2 | 裸 zscore + av_diff | `ts_zscore(ts_av_diff(...),252)` | S −0.55 | ✘ 判死 |
| T3 | 变化率保护（UNITS） | `ts_zscore(divide(ts_delta(...), max(abs(x),1)),252)` | S 0.19 + UNITS | ✘ 判死 |
| T4 | 变化 + group_rank | `group_rank(ts_zscore(ts_delta(...),252),subindustry)` | S 1.08 | ★ 弱 |
| T5 | 加速度 + group_rank | `group_rank(ts_zscore(subtract(ts_mean(X,252),ts_mean(X,504)),252),subindustry)` | **S 1.69 / F 1.04** | ★★★ 主干 |
| T6 | 二阶矩 + group_rank | `group_rank(ts_zscore(ts_std_dev(ts_delta(...),252/504),252),subindustry)` | S 1.27 / F 0.80 | ★★ 但 prod 0.9277 |
| T7 | 加速度 + tail | `tail(winsorize(group_rank(accel),std=2),0.22,0.78,0.5)` | S 1.34 / dd 0.036 | ★★ 降 dd |
| T8 | 加速度 + ts_rank | `group_rank(ts_rank(ts_zscore(accel,252),252),subindustry)` | S 1.40 / F 0.88 / 2Y 1.67 | ★★★ 提 returns |
| T9 | 成本占比加速度 | `group_rank(ts_zscore(subtract(ts_mean(cost/rev,252),ts_mean(cost/rev,504)),252),subindustry)` | **S 1.57 / F 1.01** | ★★★ 新本体 |
| T10 | 增长加速度（三阶） | `group_rank(ts_zscore(subtract(accel_252_504, accel_504_1008),252),subindustry)` | S 1.56 / F 0.98 | ★★★ 近闸 |

---

## 7. 平台闸线与破闸公式（USA/D1，实测）

```
LOW_SHARPE            1.58
LOW_FITNESS           1.0
LOW_2Y_SHARPE         1.58
LOW_SUB_UNIVERSE_SHARPE = 0.435 × S     ← 随 S 线性上涨，不是固定值
HIGH_TURNOVER         0.7
CONCENTRATED_WEIGHT   0.1
```

**★ fitness 公式（三次交叉验证全部吻合）**：
```
fitness ≈ S × √( returns / max(TO, 0.125) )
```
- `QPvjeWZp`：1.69 × √(0.0472/0.125) = 1.039 ≈ 实测 1.04 ✔
- `Xg9LqNGb`：1.67 × √(0.0480/0.125) = 1.035 ≈ 实测 1.03 ✔
- `omEv2aKE`：1.25 × √(0.0566/0.125) = 0.841 ≈ 实测 0.84 ✔

⇒ **本族 TO 恒 < 12.5% ⇒ 分母恒为 0.125 地板 ⇒ 提换手永远提不了 fitness**。
⇒ **破 fitness 只有两条路：① 提 S ② 提 returns**。
⇒ **提 returns 的最省手段 = 换中性化轴**（`INDUSTRY` 比 `SUBINDUSTRY` returns +15%，不动表达式）。

---

## 8. prod 拥挤度实测（直方图 0.6–0.7 桶条数）

| alpha | 机制 | prod | 0.6–0.7 桶 | 判定 |
|---|---|---|---|---|
| `rKRLvjad` | EPS 加速度 | **0.7463** | **5284** | ★ 最空，有余量 |
| `2rARdWvY` | EPS 加速度 + tail | 0.7728 | 9574 | tail 在财报族**不降 prod** |
| `Xg9LqNGb` | 成本加速度 | 0.8260 | 11106 | 中等 |
| `QPvjeWZp` | 营收加速度 | 0.8441 | 14509 | 偏挤 |
| `58E9NGNz` | 成本占比加速度 | 0.8904 | 41567 | 挤 |
| `vR19g6d3` | 二阶矩 std_dev | **0.9277** | **63530** | ✘ 饱和，判死 |

**⇒ 结论：加速度机制整体比二阶矩冷门；EPS 腿比营收/成本腿冷门。**

---

## 9. 平移指引（换到其它数据集时）

1. **信号字段语义含 count / intensity / value / shares / revenue（原始强度、流量）** ⇒ 可试加速度骨架。
2. **语义含 ratio（平台预聚合比值）** ⇒ 免试（`insider_feats` 已实测全灭）。
3. **窗口用 252（年同比）为主、504（两年）作外层基准**；66 窗 TO 翻倍、22 窗触发 SUB 闸。
4. **必须序数化**：`group_rank` 唯一可用；`group_zscore` / `group_scale` / `group_neutralize` / `ts_quantile` 全灭。
5. **`nanHandling=ON` 必显式传**（季频数据集通则）。
6. **流量项 > 存量项；年度口径 > 季度口径；会计调整 > 原始。**
7. **加速度骨架禁序数化/缩尾（幅度必须保留）**；但 `tail` 可加在外层降 dd。

---

## 10. 未开发靶子（下一波候选）

按「冷门 × 高覆盖 × 有经济含义」排序，全部在 FUNDAMENTAL 塔内、仍属 ATOM 单数据集：

1. **`annual_ebit_total`（ac 1, cov 0.825）** —— EBIT 加速度：经营盈利趋势，最干净
2. **`annual_operating_cashflow_amount`（ac 12, cov 0.826）** —— 经营现金流加速度：盈利质量
3. **`annual_total_debt_amount`（ac 1, cov 0.753）** —— 杠杆变化加速度：去杠杆股
4. **`annual_retained_earnings_total`（ac 2, cov 0.797）** —— 留存收益累积：复利能力
5. **`annual_sga_cost_total`（ac 5, cov 0.786）** —— 费用率加速度：经营杠杆
6. **`annual_gross_capex_total`（ac 7, cov 0.788）** —— 资本开支加速度：再投资强度
7. **`annual_avg_diluted_shares_count`（ac 6, cov 0.742）** —— 稀释股数加速度：回购效应
8. **`annual_net_income_total`（ac 3, cov 0.827）** —— 净利润加速度：无股本噪音版 EPS

**外加 `fundamental110`（XBRL 修订行为，26 字段全 VECTOR）** 是完全独立的机制维度：
`revision_number` / `preliminary` / `original_value` / `value` ⇒ **财报重述强度**，
有 Fama-French 会计稳健性学术支撑，且平台 alphaCount 低（17–52）。
