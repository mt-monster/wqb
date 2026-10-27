# USA · `fundamental2` 字段画像与机制簇（as_of 2026-10-21）

> 数据集：`fundamental2`（XBRL **footnote** 级明细，非主表科目）
> 平台口径：USA / TOP3000 / Delay 1；`platform_count = 766` 字段，全部 `MATRIX`
> 本地预筛（WebDataScope sharpe filter）：保留 **57**，剔除 **709**（`sharpe_filter_removed=709`）
> 图例：cov = `coverage`，uc = `userCount`，aC = `alphaCount`

## 1. 数据集级判据

| 指标 | 读数 | 判读 |
|---|---|---|
| 字段数 | 766（本地可筛 57） | 全字段 ATOM **不可行**（见 §5） |
| 覆盖率 | 0.2593 – 0.7058（中位 ≈0.45） | 全部低于 0.75，**必须显式 `ts_backfill`**；< 0.40 的字段单独标记 |
| 类型 | 100% MATRIX | 无 VECTOR，无需 `vec_*` 聚合 |
| 拥挤度 | aC 中位 ≈ 500；最大 24304（`fn_liab_fair_val_l1_a`，uc 19893） | **整体低拥挤**；`fn_liab_fair_val_l1_a` / `fn_oth_income_loss_fx_transaction_and_tax_translation_adj_a`（aC 15681）/ `fn_accrued_liab_a`（aC 7599）属局部拥挤，只作**辅助腿**不作主信号 |
| 更新频率 | `_a` = 年报（4 次/年）；`_q` = 季报 | 慢变量 → 换手天然低（实测待填），需注意 TO 下限 1% 与 fitness 的 `max(TO,0.125)` 地板 |
| 金字塔 | `USA/D1/FUNDAMENTAL` | 本战役的 fundamental 族；非未点亮塔（见 §5 备注） |

**与 `fnd67` / `fnd93` 的差异**：那两个是主表科目（资产/收入/现金流），已被 USA 的 value/quality 饱和族覆盖；
`fundamental2` 是 **footnote 披露项**（补偿计划、租赁承诺、税项递延、公允价值层级、信贷额度），
机制上属于 **会计质量 / 隐性杠杆 / 稀释压力**，不是 value/quality 重定价，**不受「book/value 145 颗同族 ACTIVE」直接封杀**。

## 2. 字段八族（本地可筛 57 字段归类）

| # | 族 | 代表字段（cov） | 经济机制 | aC 拥挤度 |
|---|---|---|---|---|
| A | **股权激励 / 稀释** | `fn_comp_options_grants_a` (0.6394) · `fn_comp_not_rec_q` (0.3782) · `fn_comp_non_opt_grants_a` (0.6128) · `fn_incremental_shares_attributable_to_share_based_payment_a` (0.368) · `fnd2_a_eplsbvdcpcstnrgprg` (0.3321 摊销期) | 未确认补偿 = 未来必然发生的费用 + 股本稀释（Pontiff & Woodgate 2008 发行异象；SBC 作为隐性薪酬） | 低（70–1483） |
| B | **应计 / 营运资本** | `fn_accrued_liab_a` (0.3934) · `fn_accrued_liab_curr_q` (0.3403) · `fn_prepaid_expense_a` (0.5118) · `fn_employee_related_liab_q` (0.3552) | Sloan (1996) 应计异象：应计部分持续性低，市场高估 | 中（535–7599） |
| C | **公允价值层级** | `fn_assets_fair_val_l3_q` (0.3813) · `fn_assets_fair_val_q` (0.3347) · `fn_assets_fair_val_l1_q` (0.3838) · `fn_liab_fair_val_l1_a` (0.3604) | Level 3 占比 = 模型定价 / 信息不透明（Riedl & Serafeim 2011） | L1 负债极高（24304）⇒ 只作分母 |
| D | **经营租赁隐性杠杆** | `fn_op_lease_rent_exp_a` (0.6377) · `fnd2_oprlsfmpdcurr` (0.6378) · `fn_op_lease_min_pay_due_in_5y_a` (0.617) · `fnd2_a_lhdiprtsg` (0.3317) | ASC 842 前的表外负债；租金强度 = 未入表的类债务 | 低（631–2561） |
| E | **税负 / 递延税** | `fn_eff_income_tax_rate_continuing_operations_a` (0.4545) · `fn_def_income_tax_expense_a` (0.6422) · `fn_def_tax_assets_liab_net_a` (0.7058) · `fn_def_tax_liab_q` (0.4532) · `fnd2_itxreclstatelocalitxes` (0.3361) · `fn_excess_tax_benefit_from_share_based_comp_fin_activities_a` (0.3858) | Desai & Dharmapala (2009)：有效税率低于法定 = 税收筹划创造价值；递延税负债累积 = 未来税负 / 盈余质量 | 低（123–1495） |
| F | **信贷额度 / 流动性** | `fn_line_of_credit_facility_amount_out_q` (0.4787) · `fn_line_of_credit_facility_max_borrowing_capacity_q` (0.5014) · `fn_repayments_of_lines_of_credit_q` (0.4483) · `fn_proceeds_from_lt_debt_q` (0.2884) | 已提取 / 授信额度 = 流动性约束与银行监控强度（Diamond 1991） | 低（138–1099） |
| G | **养老金 / 离职后福利** | `fnd2_dbplanchgbnfolintcst` (0.2593) | 设定受益计划义务变动 = 折现率假设的隐性利润操纵 | 低（74）但 cov 太低 |
| H | **其他综合收益 / 外币折算** | `fn_oth_income_loss_fx_transaction_and_tax_translation_adj_a` (0.426) · `fn_accum_oth_income_loss_net_of_tax_a` (0.6936) · `fn_oth_income_loss_available_for_sale_securities_adj_of_tax_q` (0.3261) | OCI 累积 = 未落损益的估值变动，回归时存在滞后修正 | FX 项 aC 15681 偏拥挤 |

### 覆盖度分档（决定预处理强度）

| 档 | 区间 | 字段（本批拟用） | 处置 |
|---|---|---|---|
| 高 | ≥ 0.60 | `fn_comp_options_grants_a` (0.64) · `fn_op_lease_rent_exp_a` (0.64) · `fnd2_oprlsfmpdcurr` (0.64) · `fn_entity_common_stock_shares_out_q` (0.686) · `fn_def_tax_assets_liab_net_a` (0.706) | `ts_backfill(x, 66)` 足够 |
| 中 | 0.40 – 0.60 | `fn_eff_income_tax_rate..._a` (0.45) · `fn_prepaid_expense_a` (0.51) · `fn_line_of_credit_facility_amount_out_q` (0.48) · `..._max_borrowing_capacity_q` (0.50) | `ts_backfill(x, 66)` + 避免再做跨字段相乘（覆盖率会乘起来） |
| 低 | < 0.40 | `fn_comp_not_rec_q` (0.378) · `fn_accrued_liab_a` (0.393) · `fn_assets_fair_val_l3_q` (0.381) · `fnd2_dbplanbnchg...` (0.259) | 必须显式 backfill；**只在 ETL 硬门允许下使用**，且不参与「三字段以上相乘」 |

## 3. 归一化分母的选择（本数据集内的硬约束）

footnote 项多为**绝对金额**（美元），直接跨公司比较等于比较规模。本数据集内可用的分母只有三类：

| 分母 | 字段（cov） | 适用 | 代价 |
|---|---|---|---|
| **股本** | `fn_entity_common_stock_shares_out_q` (0.6857) | 每股化（per-share）：补偿、租金、应计 | 与股价相关，跨截面残留价格效应（`group_rank` 后影响有限） |
| **公允价值资产** | `fn_assets_fair_val_q` (0.3347) | 仅 C 族（L3/L1 占比） | cov 低，除完只剩 ≈0.33 |
| **授信额度** | `fn_line_of_credit_facility_max_borrowing_capacity_q` (0.5014) | 仅 F 族（已提取比例） | 语义唯一正确，天然无量纲 |

**禁止**：用 `fundamental2` 之外的资产总额字段做分母（会把「混信号」争议引进来，且 ATOM 口径破裂）。
绝对值字段（`fn_def_tax_assets_liab_net_a` 等）**只做 `ts_*` 差分/时序标准化后使用**，不裸取截面水平。

## 4. 机制簇 ATOM 口径（为什么不是全 766 字段）

全字段 ATOM 要求「一个数据集除国家/交易所/行业外全部字段进同一条表达式」——766 个字段的表达式长度超出
FASTEXPR 限长，且 709 个字段已被本地 sharpe 预筛剔除（无有效读数）。
因此本数据集采用 **机制簇 ATOM**：在选定机制族内**不漏字段**。本批覆盖 5 个机制族中的 5 组代表字段，
每族内部后续补齐（例如 A 族还有 `fn_comp_non_opt_grants_a` / `fn_incremental_shares...` 待补）。
**交付时必须写明「ATOM 范围 = 机制簇 X 的全部字段」**，不得声称是全数据集 ATOM。

## 5. 批 1 设计（2026-10-21，8 条探针）

设置：USA / TOP3000 / **Delay 1** / decay 5 / **SUBINDUSTRY** / trunc 0.08 / nanHandling ON。
统一形状 `-group_rank(<TS 预处理>, subindustry)`：族内「数值越高越差」，故取负号；`group_rank` 做行业内标准化。

| # | tag | 表达式核心 | 族 | 桶 | 方向假设 |
|---|---|---|---|---|---|
| 1 | A1 | `ts_delta(ts_backfill(grants_a / shares_out, 66), 252)` | A 稀释 | Change | 授予率上升 = 稀释加速 ⇒ 负 |
| 2 | A2 | `ts_backfill(comp_not_rec_q / shares_out, 66)` | A 稀释 | Level | 未确认补偿负担 = 未来费用 ⇒ 负 |
| 3 | B1 | `ts_delta(ts_backfill(accrued_liab_a / shares_out, 66), 252)` | B 应计 | Change | 应计累积 ⇒ 负（Sloan） |
| 4 | B2 | `ts_delta(ts_backfill(prepaid_expense_a / shares_out, 66), 252)` | B 应计 | Change | 预付增长 = 现金流出资本化 ⇒ 负 |
| 5 | D1 | `ts_backfill(lease_rent_exp_a / shares_out, 66)` | D 表外杠杆 | Level | 租金强度 = 类债务 ⇒ 负 |
| 6 | D2 | `ts_delta(ts_backfill(oprlsfmpdcurr / shares_out, 66), 252)` | D 表外杠杆 | Change | 未来租金承诺上升 ⇒ 负 |
| 7 | E1 | `ts_backfill(fn_eff_income_tax_rate..._a, 66)` | E 税负 | Level | 高 ETR = 无税收筹划 ⇒ 负 |
| 8 | F1 | `ts_backfill(amount_out_q / max_borrowing_capacity_q, 66)` | F 流动性 | Level | 额度提取率高 = 流动性紧 ⇒ 负 |

桶覆盖：Level 4 / Change 4（≥3 桶满足）；无 VECTOR ⇒ `vec_*` 条不适用。
形状：`-group_rank(ts_backfill(...))` 与 `-group_rank(ts_delta(ts_backfill(...)))` 两种（批内形状多样性由闸 6 判）。
主候选后续各出反号变体（`+group_rank`）一组，用于识别「原方向已被定价」。

### 回测结果（批 1：8 条，2026-10-21）

| # | tag | alpha | S | F | TO | ret | 2Y | SUB | rns | 结论 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | A1 授予率Δ | `leMKOggx` | **−0.84** | −0.46 | 1.46% | −3.68% | −1.42 | −0.53 | −0.15 | 反向：正向为 **+0.84** |
| 2 | A2 未确认补偿 | `0mjr36wk` | **−0.79** | −0.34 | 0.94%❌ | −2.30% | −0.92 | −0.27 | −0.27 | 反向：正向 **+0.79**；TO 破 1% |
| 3 | B1 应计负债Δ | `RRA6nW3g` | **−1.00** | −0.51 | 1.25% | −3.23% | −1.29 | −0.25 | −0.23 | 反向：正向 **+1.00**（全批最强） |
| 4 | B2 预付Δ | `88vPd9zV` | **−0.99** | −0.51 | 1.38% | −3.27% | −1.53 | −0.23 | −0.47 | 反向：正向 **+0.99** |
| 5 | D1 租金水平 | `e76QwN3O` | **−0.95** | −0.61 | 0.83%❌ | −5.18% | −1.15 | −0.62 | −0.50 | 反向：正向 **+0.95**；TO 破 1% |
| 6 | D2 未来租金Δ | `GrgOAXKx` | **−0.91** | −0.49 | 1.52% | −3.64% | −1.25 | −0.51 | −0.11 | 反向：正向 **+0.91** |
| 7 | E1 有效税率 | `N1eVml6q` | −0.60 | −0.25 | 1.01% | −2.20% | −1.04 | −0.54 | −0.11 | 反向：正向 **+0.60** |
| 8 | F1 额度提取率 | `A1QvMY3d` | −0.57 | −0.23 | 1.06% | −2.05% | −0.88 | −0.17 | **+0.09** | 反向：正向 **+0.57**；`rns` 已为正 ⇒ 剥离风格后几乎无残留 |

**核心归因（批 1 全 8 条收齐）**：**八条独立机制族（A1/A2/B1/B2/D1/D2/E1/F1）S 无一例外为负，强度 −0.57…−1.00**
⇒ ① 这不是偶发，是**方向性结论**：USA 2014–2023 里「高股权激励 / 高租金强度 / 应计累积 / 高预付款」的公司**跑赢**，
教科书方向（稀释折价、表外杠杆折价、应计异象）在本期**反转**。② 与文献一致：应计异象在 2003 年后显著衰减
（Green-Hand-Soliman 2011；Lewellen 2010）；SBC 高的公司集中在科技/成长，租金高的集中在轻资产连锁 —— 两者都是**成长溢价**，
不是会计质量溢价。③ `rns` 全在 −0.11…−0.50，换成正向也仅 +0.11…+0.50 ⇒ **剥离风格后剩余有限**，
这几族在本期的定位是「风格腿」而非「特异 alpha」。
④ 两个族的 TO **低于 1% 下限**（A2 0.94% / D1 0.83%）⇒ 年报级慢变量在本形态下连交易频率都不达标。

### 回测结果（批 2：反向 + 机制簇补全，2026-10-21）

设计：把批 1 的负号翻正（`+group_rank`），对 A / D 两族做**机制簇内补全**（A3 非期权授予、D3 五年期最低租金），
并用 `quantile()` 与 `industry` 分组测两个形状杠杆。5 条首轮提交成功，3 条撞 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`（429）待补发。

| # | tag | alpha | S | F | TO | ret | 2Y | SUB | rns | 结论 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | A1r 授予率Δ正向 | `d5K1AeA2` | +0.84 | +0.46 | 1.46% | +3.68% | 1.42 | 0.53 | 0.15 | 与批 1 A1 的 −0.84 **逐位对称** ⇒ 纯符号翻转，无新信息 |
| 2 | A1r + `quantile` | `6XAKvqlJ` | +0.86 | +0.49 | 1.50% | +4.05% | 1.37 | 0.54 | 0.17 | `quantile()` 仅 **+0.02** |
| 3 | A3 非期权授予 | `wp9bMmpl` | +0.96 | +0.56 | 1.09% | +4.25% | 0.39 | 0.41 | 0.51 | 同簇换字段 +0.12（0.84→0.96），但 2Y 崩到 0.39 |
| 4 | D1r 租金正向 | `QPYKLJXG` | +0.95 | +0.61 | 0.83%❌ | +5.18% | 1.15 | 0.62 | 0.50 | 与批 1 D1 的 −0.95 对称 |
| 5 | D1r + `quantile` | `ZYmAe3kx` | **+0.97** | +0.64 | 0.85%❌ | +5.44% | 1.18 | 0.65 | 0.52 | **全数据集最高 S**；`quantile` 仍只 +0.02 |

### 封存结论（2026-10-21，批 1+批 2 共 13 条收齐）

- **机制上限 = +0.97**（`ZYmAe3kx`，D1 + `quantile`）；B1/B2 的正向按对称推得 ≈+1.0，实测最高仍是 0.97。
  距 USA/D1 的 1.58 线 **0.61**，远超任何单自由度杠杆的实测增益上界（本文档与 playbook 记录的 +0.2…+0.4）。
- **已实测的三个杠杆**：`quantile()` **+0.02**；同簇换字段（A1→A3）**+0.12**；符号翻转 **±0**（逐位对称）。
  剩下的分组改 `industry` 与 D2/D3 补全共 3 条撞 429 未发 —— **不补发**：分组只改风格暴露方向，
  补全最多把 0.97 抬到 ≈1.0，距线仍 0.58。
- **`rns` 0.50–0.52（正向）** ⇒ 剥离风格后只剩一半；本数据集全部机制的正确读法是**风格腿**（成长/轻资产溢价），
  不是可独立提交的特异 alpha。
- **换手**：D1/D1q 0.83%/0.85% 低于平台 `LOW_TURNOVER` 1% 下限（`config` `turnover_range=(0.01,0.70)`），
  即最强那一支即使 S 达标也会被换手闸拦。
- **判定：`fundamental2` 封存**。它是 USA 最后一个未开采的 Fundamental 数据集；封存后 USA 侧
  「未判死 × 可开采」的 Fundamental 库存归零，剩余缺口只能来自新机制（新季度数据集 / 已封存族的正交重构）。

## 6. 风险与前置判据

- **Fitness 墙**：慢变量 TO 低，`F = S·sqrt(ret / max(TO, 0.125))`，TO < 12.5% 后 F 只由 `S·sqrt(ret)` 决定。
  S 1.6 需要 ret ≥ 6.25% 才到 F 1.0。**低 TO 不等于高 F**，必须看 `returns` 绝对值。
- **已点亮塔**：`USA/D1/FUNDAMENTAL` 类别归属需用 `get_pyramid_alphas` 复核；若已点亮，本批只作 REGULAR 交付，
  不占塔位。
- **数据滞后**：footnote 项在 10-K/10-Q 中披露，平台按 `delay=1` 起可用；`_a` 字段一年只变 4 次，
  `ts_delta(..., 252)` 实际是「上一份年报 vs 这一年」，极慢 —— 若 S 可接受但 TO 太低（<1%）将被 `LOW_TURNOVER` 拦。
- **不做**：不用 `fn_liab_fair_val_l1_a`（aC 24304）当主信号；不与其它数据集字段相加（禁混信号）。
