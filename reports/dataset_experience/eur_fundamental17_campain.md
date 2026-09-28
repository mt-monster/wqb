# EUR · fundamental17 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：EUR / fundamental17；波次 251, 252；去重后 14 条已完成回测，13 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=251,252。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOPCS1600 | SUBINDUSTRY | 4 | 0.08 | 2014-01-01 | 2023-12-31 |

最高 Sharpe 候选：`N1aeg3pp`，Sharpe=1.18，同条 Fitness=0.8，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `annual_net_income_available_common` | MATRIX / 0.7495 / 3 | Net income available to common shareholders for the most recent fiscal year | 2 | 1.13 / 0.75 (`QPbYaMlK`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `annual_normalized_net_income_common` | MATRIX / 0.7495 / 1 | Normalized net income available to common shareholders for the most recent fiscal year (excludes unusual/one-time items) | 3 | 1.18 / 0.8 (`N1aeg3pp`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_8_ttmgrosmgn` | MATRIX / 0.6326 / 1 | Gross margin - trailing 12 months | 1 | 0.65 / 0.27 (`rKOdJ0Oa`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_a2netmrgn` | MATRIX / 0.7451 / 7 | Net Profit Margin % - 2nd historical fiscal year | 1 | 0.4 / 0.13 (`rKOdJ0ea`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_agrosmgn` | MATRIX / 0.638 / 1 | Gross Margin - 1st historical fiscal year | 1 | 0.33 / 0.09 (`78NoaG6Z`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_aniac` | MATRIX / 0.7495 / 1 | Net income available to common shareholders for the most recent fiscal year | 1 | 0.58 / 0.23 (`88jvaGR7`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_ata` | MATRIX / 0.7509 / 5 | Total assets - most recent fiscal year | 4 | 1.18 / 0.8 (`N1aeg3pp`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_atachg` | MATRIX / 0.7484 / 1 | Year-over-year percentage change in total assets for the most recent fiscal year | 1 | -0.16 / -0.03 (`KPNmXVg8`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_qgrosmgn` | MATRIX / 0.6031 / 5 | Gross Margin - most recent quarter | 1 | 0.33 / 0.09 (`78NoaG6Z`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_tcpngmpna` | MATRIX / 0.7464 / 0 | Net Profit Margin % - 1st historical fiscal year | 1 | 0.4 / 0.13 (`rKOdJ0ea`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_ttmrecturn` | MATRIX / 0.6533 / 0 | Receivables turnover - trailing 12 months | 2 | 0.26 / 0.07 (`88jvaYzq`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `fnd17_ttmsga2rev` | MATRIX / 0.6117 / 0 | SG&A expenses / net sales - trailing 12 month | 3 | 0.65 / 0.27 (`rKOdJ0Oa`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `ttm_net_income_per_employee` | MATRIX / 0.6813 / 0 | Net income per employee over the trailing 12 months | 2 | 0.8 / 0.42 (`2rwjaWK5`) | 仅为所列搭配中的结果；不能推断独立贡献 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 251 | `N1aeg3pp` | 1.18 | 0.8 | 0.43 | 1.13 | 0.78 | 0.98 | 未核实 | 未核实 |
| 251 | `2rwjaWK5` | 0.8 | 0.42 | -0.3 | 1.0 | 0.53 | 0.48 | 未核实 | 未核实 |
| 251 | `rKOdJ0Oa` | 0.65 | 0.27 | -0.03 | 1.06 | 0.1 | 0.24 | 未核实 | 未核实 |
| 251 | `88jvaGR7` | 0.58 | 0.23 | 0.08 | 1.21 | 0.86 | 0.93 | 未核实 | 未核实 |
| 251 | `rKOdJ0ea` | 0.4 | 0.13 | -0.44 | 1.39 | 0.26 | 0.01 | 未核实 | 未核实 |
| 251 | `78NoaG6Z` | 0.33 | 0.09 | -0.34 | 1.81 | 0.02 | -0.15 | 未核实 | 未核实 |
| 251 | `GrbgMQgo` | 0.32 | 0.09 | -0.11 | 1.52 | 0.2 | -0.15 | 未核实 | 未核实 |
| 251 | `88jvaYzq` | 0.26 | 0.07 | -1.07 | 1.25 | -0.18 | -0.37 | 未核实 | 未核实 |
| 251 | `QPbY2WYp` | 0.2 | 0.04 | -0.38 | 2.11 | -0.12 | -0.13 | 未核实 | 未核实 |
| 251 | `vRrOe6Lb` | 0.11 | 0.02 | 0.53 | 1.06 | 0.12 | 0.44 | 未核实 | 未核实 |
| 251 | `KPNmXVg8` | -0.16 | -0.03 | 1.19 | 1.18 | -0.25 | 0.13 | 未核实 | 未核实 |
| 251 | `npdAZ6va` | -0.21 | -0.05 | 0.02 | 1.64 | -0.21 | -0.25 | 未核实 | 未核实 |
| 252 | `QPbYaMlK` | 1.13 | 0.75 | 0.47 | 1.12 | 0.71 | 0.9 | 未核实 | 未核实 |
| 252 | `6XjAw7Y7` | -0.5 | -0.17 | -0.64 | 1.33 | 0.07 | -0.08 | 未核实 | 未核实 |

### 原式与局部失败证据

**N1aeg3pp（wave 251）**

```text
rank(divide(ts_backfill(annual_normalized_net_income_common,252),ts_backfill(fnd17_ata,252)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**2rwjaWK5（wave 251）**

```text
group_rank(ts_backfill(ttm_net_income_per_employee,252),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**rKOdJ0Oa（wave 251）**

```text
group_rank(subtract(ts_backfill(fnd17_8_ttmgrosmgn,252),ts_backfill(fnd17_ttmsga2rev,252)),industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**88jvaGR7（wave 251）**

```text
rank(divide(subtract(ts_backfill(annual_normalized_net_income_common,252),ts_backfill(fnd17_aniac,252)),ts_backfill(fnd17_ata,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE。

**rKOdJ0ea（wave 251）**

```text
group_rank(subtract(ts_backfill(fnd17_tcpngmpna,252),ts_backfill(fnd17_a2netmrgn,252)),industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**78NoaG6Z（wave 251）**

```text
group_rank(subtract(ts_backfill(fnd17_qgrosmgn,252),ts_backfill(fnd17_agrosmgn,252)),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**GrbgMQgo（wave 251）**

```text
group_rank(ts_delta(ts_backfill(ttm_net_income_per_employee,252),252),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**88jvaYzq（wave 251）**

```text
group_rank(ts_backfill(fnd17_ttmrecturn,252),industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**QPbY2WYp（wave 251）**

```text
group_rank(ts_delta(ts_backfill(fnd17_ttmrecturn,252),252),industry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**vRrOe6Lb（wave 251）**

```text
reverse(group_rank(ts_backfill(fnd17_ttmsga2rev,252),industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**KPNmXVg8（wave 251）**

```text
reverse(group_rank(ts_mean(ts_backfill(fnd17_atachg,252),66),subindustry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**npdAZ6va（wave 251）**

```text
reverse(group_rank(ts_delta(ts_backfill(fnd17_ttmsga2rev,252),252),industry))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**QPbYaMlK（wave 252）**

```text
rank(divide(ts_backfill(annual_net_income_available_common,252),ts_backfill(fnd17_ata,252)))
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**6XjAw7Y7（wave 252）**

```text
rank(divide(subtract(ts_backfill(annual_normalized_net_income_common,252),ts_backfill(annual_net_income_available_common,252)),ts_backfill(fnd17_ata,252)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

2026-09-24，wave251：8个预定义主假设＋4个配对水平对照，全部完成，0错误，0个完整合格，0个符合Mode B资格。字段含义以上表平台描述为准。

### 对照带来的信息

| 机制及字段 | 主假设 S/F/2Y | 水平对照 S/F/2Y | 实证与后续边界 |
|---|---|---|---|
| 人均盈利 `ttm_net_income_per_employee` | .32/.09/-.11 | .80/.42/-.30 | 年度变化降低IS强度；水平仍弱，且2Y为负，不继续窗口扩展 |
| 应收周转 `fnd17_ttmrecturn` | .20/.04/-.38 | .26/.07/-1.07 | 两式都弱；水平Sharpe略高但2Y更差，不能解释为全面改善 |
| 费用负担 `fnd17_ttmsga2rev` | -.21/-.05/.02 | .11/.02/.53 | 负费用变化劣于低费用水平；两式仍不达标，不自动改成高费用方向 |
| 盈利调整差额 `annual_normalized_net_income_common`、`fnd17_aniac`，分母 `fnd17_ata` | .58/.23/.08 | 1.18/.80/.43 | 续查发现原差额式有UNITS警告，不能作为干净对照；先查清报告利润口径，再判断会计调整机制 |

原8条主假设最高Sharpe仅.65，新增对照把本轮可观察最高值提高到1.18，说明固定8条会漏掉有信息价值的基线。但新增4条没有产生合格Alpha；选波优化已证明的是实验信息更完整，尚未证明可提交率提高。

### 其余字段的已测边界

- `fnd17_8_ttmgrosmgn`减`fnd17_ttmsga2rev`：留存经营利润率近似值S.65/F.27，Sub仅.10；两项会计指标相减并没有在本设置下提供稳定排序。不可把该近似值直接称为平台报告的经营利润率。
- `fnd17_qgrosmgn`减`fnd17_agrosmgn`：季度与历史年度毛利率差S.33/F.09；频率不一致，需先有财报日期/季节性证据再重开，不能简单叠加更多短窗。
- `fnd17_tcpngmpna`减`fnd17_a2netmrgn`：两历史财年的净利率改善S.40/F.13，2Y-.44；不是最新季度业绩冲击，停止本轮差额结构。
- `fnd17_atachg`：66日均值后的保守资产增长S-.16/F-.03；平滑已有同比变化字段未见优势，不用反转方向制造新假设。

所有12条换手率为1.00%–2.11%，低于本战役5%下限；最佳候选N1aeg3pp的S1.18低于Mode B资格线1.25，2Y.43亦弱。平台详情已复核其LOW_SHARPE、LOW_FITNESS、LOW_2Y_SHARPE失败。表中局部空失败列表不等于通过；无需为这些弱候选消耗昂贵的Prod/Self核查。

### 下一轮读取规则

1. 将这12个已测结构登记为本设置下的失败实验；不把fundamental17、12个字段或48条未测变体整体判死。
2. 48条延后项由`wave_meta_251.selection_audit`保留来源与理由。只有独立机制、必要对照或新数据质量证据才重开；单纯换窗口/包装不能推翻本次结论。
3. 该数据集暂不进入参数增强波，但保留未解决的研究问题。重访时先读取本文件，并说明新实验能区分什么旧实验无法回答的问题；有明确测量缺陷时可做一次预注册的最小纠错复验。

### 2026-09-24 用户追问后的续查

平台重新核实88jvaGR7：subtract第一项预期Unit[TSPrice:1]、第二项为Unit[]。因此撤回“差额机制被有效对照否定”的解释；目前只能确认该原式未达标。N1aeg3pp本身无此警告，但仍不符合Mode B和提交资格。

| IS年份 | 标准化利润水平 Sharpe | 原差额式 Sharpe（有单位警告） |
|---|---:|---:|
| 2014 | 2.17 | 1.14 |
| 2015 | 1.92 | -.05 |
| 2016 | 1.49 | .71 |
| 2017 | -1.01 | -.63 |
| 2018 | 3.71 | 2.39 |
| 2019 | 2.22 | .57 |
| 2020 | -1.00 | -1.00 |
| 2021 | 2.74 | 2.58 |
| 2022 | -.08 | -.16 |
| 2023 | 1.42 | .49 |

标准化利润水平7/10年为正、2023回升，值得研究留存；近3年仍含负年，2Y .43、RN Sharpe .53、TVR1.13%是反证。年度统计来自同一IS样本，不能视为独立重复验证，也不能声称提升显著。两式多空摘要均473/531，只能说明摘要计数一致，不能证明逐日持仓掩码相同。

`research_leads_w251`保存这些证据，与near/ready分开。wave252预注册两条纠错对照：用已实查的`annual_net_income_available_common`补报告利润/资产基线，并修复原差额式；复用N1aeg3pp，不改变其他设置。GEM、身份清单、门禁及两条回测均已完成，平台详情确认两条无UNITS警告。详见[复验设计与结果](../eur_d1_20260924_fundamental17_measurement_repair.md)。

| 盈利口径 | Alpha | Sharpe | Fitness | 2Y Sharpe | RN Sharpe | 换手率 |
|---|---|---:|---:|---:|---:|---:|
| 标准化净利润/资产（复用251） | N1aeg3pp | 1.18 | .80 | .43 | .53 | 1.13% |
| 报告净利润/资产（252） | QPbYaMlK | 1.13 | .75 | .47 | .52 | 1.12% |
| 修正后的标准化减报告利润/资产（252） | 6XjAw7Y7 | -.50 | -.17 | -.64 | -.59 | 1.33% |

两种利润水平的观察结果相近；标准化处理仅高.05 Sharpe，未做显著性检验，不能认定剔除一次性项目提供独立收益。正确口径的差额式仍弱，停止该结构的窗口扩展及事后翻号。两条新式的多空摘要为475/529与495/509；无单位警告不等于逐日覆盖一致。

`annual_net_income_available_common`可用于本次平台认可的差额运算，但不能据此认定所有同名旧字段等价。QPbYaMlK实时详情仍有LOW_SHARPE、LOW_FITNESS、LOW_2Y_SHARPE；自动证据块中其局部空失败列表不是通过证据。复验没有产生Mode B或提交资格。

盈利水平的研究问题保留：RN及近2Y偏弱的来源是什么，是否存在有独立经济依据的盈利定义。追加模拟预算目前为0；只有新的诊断证据或独立机制才重开，不能重复把同一口径问题称为纠错。252仅关闭两条精确表达式在本设置下的实验，未判死整个数据集。S6任务`campaign_EUR_S6_20260924_230900`成功，自动证据已更新为14条、13字段。
