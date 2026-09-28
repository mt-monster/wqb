# EUR · fundamental23 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：EUR / fundamental23；波次 247, 248, 249, 250；去重后 18 条已完成回测，14 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=247,248,249,250。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOPCS1600 | SUBINDUSTRY | 4 | 0.08 | 2014-01-01 | 2023-12-31 |

最高 Sharpe 候选：`78NoOeVx`，Sharpe=1.67，同条 Fitness=1.06，Prod=0.7432。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `accounts_payable_4` | MATRIX / 0.8426 / 7 | [Quarterly] Accounts Payable | 1 | -0.49 / -0.18 (`E5pVZA8P`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `accounts_receivable_total_5` | MATRIX / 0.8734 / 8 | Total accounts receivable as of the reporting date. | 1 | 0.46 / 0.14 (`KPNmKRZE`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `accrued_accounts_receivable` | MATRIX / 0.8283 / 4 | [Quarterly] Accounts Receivable - Trade, Net | 2 | -0.49 / -0.18 (`E5pVZA8P`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `accrued_assets_total` | MATRIX / 0.8284 / 2 | Total accrued assets as of the reporting date. | 1 | -0.87 / -0.39 (`ZYbmRLz3`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `accrued_cash_equivalents` | MATRIX / 0.8672 / 5 | [Quarterly] Cash & Equivalents | 5 | 1.41 / 0.85 (`npdAxjwd`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `accrued_interest_payable` | MATRIX / 0.8909 / 4 | Interest expense that has been accrued but not yet paid. | 1 | -0.29 / -0.08 (`O0NJ1vV1`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `assets_total_2` | MATRIX / 0.9361 / 7 | Total assets held by the company. | 6 | 1.67 / 1.06 (`78NoOeVx`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd23_debt_issuance` | MATRIX / 0.8347 / 1 | debt issuance | 1 | 0.75 / 0.32 (`RRbAjO0g`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd23_tot_inventory` | MATRIX / 0.8994 / 0 | total inventory. | 1 | -0.28 / -0.08 (`gJbWYzdM`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `investment_cash_expenditures` | MATRIX / 0.7439 / 0 | purchase of fixed assets. | 1 | 1.38 / 0.8 (`O0NJQLwq`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `operating_cashflow` | MATRIX / 0.7555 / 4 | Net cash generated from operating activities during the period. | 8 | 1.67 / 1.06 (`78NoOeVx`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `total_financing_cash_flow` | MATRIX / 0.9323 / 1 | [Quarterly] Cash from Financing Activities | 10 | 1.67 / 1.06 (`78NoOeVx`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `total_income_after_taxes` | MATRIX / 0.9363 / 0 | Total income after all taxes have been deducted. | 1 | 0.55 / 0.19 (`WjbLEmzd`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `trade_receivables_current` | MATRIX / 0.8733 / 0 | [Quarterly] Total Receivables, Net | 1 | -0.28 / -0.08 (`gJbWYzdM`) | 仅为所列搭配中的结果；不能推断独立贡献 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 247 | `2rwj1kWY` | 1.42 | 0.85 | 2.2 | 2.01 | 0.75 | 0.71 | 0.7879 | 未核实 |
| 247 | `WjbLEmzd` | 0.55 | 0.19 | 0.27 | 2.08 | 0.17 | 0.19 | 未核实 | 未核实 |
| 247 | `KPNmKRZE` | 0.46 | 0.14 | -0.2 | 2.51 | 0.5 | 0.21 | 未核实 | 未核实 |
| 247 | `gJbWYzdM` | -0.28 | -0.08 | -0.11 | 1.81 | -0.15 | -0.58 | 未核实 | 未核实 |
| 247 | `O0NJ1vV1` | -0.29 | -0.08 | 0.19 | 1.37 | -0.31 | -0.32 | 未核实 | 未核实 |
| 247 | `E5pVZA8P` | -0.49 | -0.18 | -0.75 | 1.29 | -0.52 | -0.24 | 未核实 | 未核实 |
| 247 | `wpZ98VGY` | -0.76 | -0.33 | -1.19 | 1.55 | -0.54 | -0.26 | 未核实 | 未核实 |
| 247 | `ZYbmRLz3` | -0.87 | -0.39 | -0.86 | 1.51 | -0.7 | -0.36 | 未核实 | 未核实 |
| 248 | `npdAxjwd` | 1.41 | 0.85 | 2.09 | 2.09 | 0.78 | 0.71 | 0.7762 | 未核实 |
| 248 | `O0NJQLwq` | 1.38 | 0.8 | 2.25 | 1.9 | 0.86 | 0.74 | 0.7411 | 未核实 |
| 248 | `RRbAjO0g` | 0.75 | 0.32 | 1.36 | 1.9 | 0.64 | 0.41 | 未核实 | 未核实 |
| 248 | `e7b6kY86` | -0.03 | 0 | -0.14 | 2.53 | -0.14 | -0.46 | 未核实 | 未核实 |
| 249 | `wpZ9mr9Q` | 1.51 | 0.96 | 1.92 | 1.94 | 0.76 | 0.69 | 0.7957 | 未核实 |
| 249 | `KPNm01m8` | 0.38 | 0.12 | 0.98 | 2.05 | 0.13 | 0.23 | 未核实 | 未核实 |
| 250 | `78NoOeVx` | 1.67 | 1.06 | 2.42 | 2.09 | 0.92 | 0.73 | 0.7432 | 未核实 |
| 250 | `rKOdkZX9` | 1.61 | 1.09 | 1.7 | 1.13 | 0.93 | 1.05 | 未核实 | 未核实 |
| 250 | `GrbgVZv0` | 1.16 | 0.71 | 2.24 | 1.84 | 0.75 | 0.56 | 未核实 | 未核实 |
| 250 | `JjNPl6Lj` | 0.24 | 0.05 | 0.48 | 2.79 | 0.07 | -0.2 | 未核实 | 未核实 |

### 原式与局部失败证据

**2rwj1kWY（wave 247）**

```text
reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(operating_cashflow,252)))))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**WjbLEmzd（wave 247）**

```text
rank(divide(ts_backfill(operating_cashflow,252),abs(ts_backfill(total_income_after_taxes,252))))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**KPNmKRZE（wave 247）**

```text
reverse(rank(ts_delta(divide(ts_backfill(accounts_receivable_total_5,252),ts_backfill(accrued_cash_equivalents,252)),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**gJbWYzdM（wave 247）**

```text
reverse(rank(divide(ts_backfill(fnd23_tot_inventory,252),ts_backfill(trade_receivables_current,252))))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**O0NJ1vV1（wave 247）**

```text
reverse(rank(divide(ts_backfill(accrued_interest_payable,252),ts_backfill(accrued_cash_equivalents,252))))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**E5pVZA8P（wave 247）**

```text
rank(divide(ts_backfill(accounts_payable_4,252),ts_backfill(accrued_accounts_receivable,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**wpZ98VGY（wave 247）**

```text
reverse(rank(divide(ts_backfill(accrued_accounts_receivable,252),ts_backfill(accrued_cash_equivalents,252))))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**ZYbmRLz3（wave 247）**

```text
rank(divide(ts_backfill(accrued_cash_equivalents,252),ts_backfill(accrued_assets_total,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**npdAxjwd（wave 248）**

```text
group_neutralize(reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(operating_cashflow,252))))),bucket(rank(divide(ts_backfill(accrued_cash_equivalents,252),ts_backfill(assets_total_2,252))),range="0,1,0.2"))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS。

**O0NJQLwq（wave 248）**

```text
reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(investment_cash_expenditures,252)))))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**RRbAjO0g（wave 248）**

```text
reverse(rank(divide(ts_backfill(fnd23_debt_issuance,252),abs(ts_backfill(operating_cashflow,252)))))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**e7b6kY86（wave 248）**

```text
reverse(rank(ts_delta(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(operating_cashflow,252))),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**wpZ9mr9Q（wave 249）**

```text
subtract(0,rank(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(assets_total_2,252))))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE。

**KPNm01m8（wave 249）**

```text
if_else(greater(ts_backfill(operating_cashflow,252),0),-rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(operating_cashflow,252)))),0)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**78NoOeVx（wave 250）**

```text
vector_neut(reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(assets_total_2,252)))),rank(divide(ts_backfill(operating_cashflow,252),ts_backfill(assets_total_2,252))))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**rKOdkZX9（wave 250）**

```text
reverse(rank(ts_mean(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(assets_total_2,252)),252)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**GrbgVZv0（wave 250）**

```text
vector_neut(reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(operating_cashflow,252))))),rank(ts_backfill(assets_total_2,252)))
```

已存检查失败：LOW_ROBUST_UNIVERSE_SHARPE。

**JjNPl6Lj（wave 250）**

```text
reverse(rank(ts_zscore(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(assets_total_2,252)),252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

复盘日期：2026-09-24。本任务已完成 wave247–250：8＋4＋2＋4＝18条，0个完整合格 Regular。Mode B2四机制对照已完成；78NoOeVx的Prod已核实为0.7432，不合格；rKOdkZX9查询超时，相关性仍未知。

### 输入与证据质量

S1目录2332字段（2318 MATRIX、14 VECTOR）；实际14字段均为 MATRIX、users≤9。固定 EUR / TOPCS1600 / D1 / SUBINDUSTRY / decay4 / truncation0.08 / maxTrade ON / nanHandling ON，FULL 2014–2023。季度财务项按252日回填，同公司内部先做比率，最后截面排名。

本地缺完整分布体检包，门禁明确采用 warn，并在台账记录。字段 coverage 元数据与后续中性设置诊断是两种口径，不能据此宣称完整分布体检通过。

**名称不是语义证据**：未采用 `free_cash_flow`，因为平台描述实际为 Other Financing Cash Flow；`free_cash_flow_value` 描述为 Financing Cash Flow Items。不能将它们解释成自由现金流。`accrued_assets_total` 描述也不足以直接等同标准文献中的会计应计额。

### 首探八个机制：仅融资依赖值得继续

| 字段或组合 | 本轮假设 | S / F | 经验与行动 |
|---|---|---|---|
| `total_financing_cash_flow / abs(operating_cashflow)` 取反 | 外部融资依赖较低 | 1.42 / .85 | 唯一首探达到 Mode B 资格；Prod .7879，不可提交 |
| `operating_cashflow / abs(total_income_after_taxes)` | 税后利润的现金兑现 | .55 / .19 | 概念合理不代表数据实现有效；淘汰该比率结构 |
| `accounts_receivable_total_5 / accrued_cash_equivalents` 年度变化取反 | 回款占用恶化 | .46 / .14 | 增量方向微弱，2Y −.20；不继续增强 |
| `fnd23_tot_inventory / trade_receivables_current` 取反 | 存货相对客户欠款膨胀 | −.28 / −.08 | 资产构成并不直接等于销售放缓；原假设未被支持 |
| `accrued_interest_payable / accrued_cash_equivalents` 取反 | 未付利息相对现金压力 | −.29 / −.08 | 应付利息字段并非利息费用或利息覆盖倍数；不能混用 |
| `accounts_payable_4 / accrued_accounts_receivable` | 供应商信用抵消客户占款 | −.49 / −.18 | 融资便利与支付困难可能混合；仅确认当前比率失败 |
| `accrued_accounts_receivable / accrued_cash_equivalents` 取反 | 应收款挤占现金 | −.76 / −.33 | 负向但绝对强度不足，不能靠翻号直接升为强候选 |
| `accrued_cash_equivalents / accrued_assets_total` | 现金支撑资产 | −.87 / −.39 | 本轮持有更多现金未带来正向收益；不推出“现金越少越好”的普遍规则 |

### Mode B1：六个预先定义的概念

父因子 `2rwj1kWY` 满足 S≥1.25、F≥.8；因此优化资格成立。wave248和249共同完成这一周期，不能算成两次独立成功迭代。

| 改动 | 字段角色 | S / F | Prod | 结论 |
|---|---|---|---|---|
| 用 `assets_total_2` 作分母 | 资产规模标准化融资强度 | 1.51 / .96 | .7957 | 强度最好但相关性更高；Sub .76低于.80，Robust .69低于.70；RA四项失败 |
| 以 `accrued_cash_equivalents / assets_total_2` 分五组 | 现金储备是分组轴，主腿冻结 | 1.41 / .85 | .7762 | 有限降相关，不足以跨过.7；不值得扫分组边界 |
| 用 `abs(investment_cash_expenditures)` 作分母 | 固定资产购置支出标准化融资 | 1.38 / .80 | .7411 | 相关性改善最多；Sub .86、Robust .74，但主指标仍低；最有价值的未完成线索 |
| 分子改 `fnd23_debt_issuance` | 只看债务发行而非全部融资 | .75 / .32 | 未测 | 债务发行不能保留总融资主腿的强度；淘汰 |
| 原融资/经营现金比年度变化 | 由融资水平改成融资变化 | −.03 / 0 | 未测 | 水平信息的收益没有转移到年度变化；淘汰 |
| `operating_cashflow > 0` 才给原始信号 | 经营现金生成状态门控 | .38 / .12 | 未测 | 正现金流限制破坏了强度；不能继续以该弱结果增强 |

**最重要的结论**：提高 Sharpe、降低生产相关性、改善子宇宙是不同目标。不能把资产分母的1.51 Sharpe和资本开支分母的.7411相关性拼成一个不存在的候选。四个已测强候选的 Prod 全部≥.7。

### 字段实测诊断：支持什么、不支持什么

两核心字段以 NONE / decay0 / nanHandling OFF / maxTrade OFF 做研究诊断，不计入18条因子回测。

| 计数代理 | 融资现金流 | 经营现金流 | 含义边界 |
|---|---:|---:|---|
| 原始有效多空合计 | 1246 | 1256 | 名义1600池约78%；是模拟摘要代理，不是逐日原始覆盖率 |
| 非零计数 | 1247 | 1256 | 未见大规模零值占据的证据 |
| 66日窗口内变化计数 | 968 | 988 | 不是全体每天更新，仍要保留稀疏更新认知 |
| 年均值正值计数 | 466 | 348 | 经营现金正负状态混合明显，abs分母丢失符号状态 |
| 截面一倍标准差内计数 | 1194 | 1235 | 不能反推完整偏度、峰度；保留rank防尺度极端 |
| 绝对值超过自身年均绝对值4倍 | 26 | 16 | 无量纲异常代理；不是金额范围或分位点 |

旧示例中的 `ts_median`、`scale_down` 本次不可用；失败/取消诊断不算已完成证据。绝对金额阈值出现单位警告，已改无量纲比值，禁止把 CSPrice 单位解释成美元金额。

### 跨年与提交边界

父因子2017、2020年为负，2022年贡献累计PnL约32.37%；并非每年稳定。未完成邻域参数稳健性、完整Self审计和提交判定，不能写成可提交。部分历史review的 `failed_checks=[]` 与当前Regular口径不一致；平台详情核查确认父因子仍有LOW_SHARPE/LOW_FITNESS。

### 下一轮应读取的经验

1. 保留总融资现金流主腿；低users未避免0.74–0.80的生产相关性墙。
2. 不重复现金正值门控、债务发行替换和年度delta；这些结构已经给出弱证据。
3. Mode B2 盈利暴露剥离 `78NoOeVx` S1.67/F1.06、年度融资均态 `rKOdkZX9` S1.61/F1.09，提供IS强度线索；换手率2.09%/1.13%、RN Fitness .57/.52未达本战役口径。前者平台Prod=0.7432仍失败，后者360秒查询超时；两者不能宣称独立性合格。
4. 规模暴露剥离 `GrbgVZv0` S1.16/F.71且Robust .56<.7；自身历史zscore `JjNPl6Lj` S.24/F.05。两者不足以支持后续参数扫描。波250完整原式与逐项指标见上方证据块。
5. 若连续合规概念周期仍受阻，按优化skill资格与周期边界处理；不能加权混合、跨PV×MODEL，不能偷换D0。

来源：DB `review_247/248/249/250`、`s6_verdict_247/248/249/250`、`field_diagnostics_f23_financing_20260924`、`catalog_fundamental23`、已存平台相关性；原始机制文档位于 `reports/eur_d1_20260924_*`。理论背景是[流动性管理与融资约束论文](https://arxiv.org/abs/1411.7670)，上述欧股收益解释属于本任务待检验推论，非论文结论。
