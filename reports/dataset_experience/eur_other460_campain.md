# EUR · other460 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：EUR / other460；波次 254；去重后 8 条已完成回测，8 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=254。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOPCS1600 | SUBINDUSTRY | 4 | 0.08 | 2014-01-01 | 2023-12-31 |

最高 Sharpe 候选：`npdAPkk3`，Sharpe=0.07，同条 Fitness=0.01，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `oth460_1l_dlts` | MATRIX / 1.0 / 1 | The probability that the future trend of 'Total Debt' will fall | 2 | -0.36 / -0.11 (`E5pVR0om`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_3l_dlts` | MATRIX / 1.0 / 0 | The probability that the future trend of 'Total Debt' will move up | 1 | -0.37 / -0.11 (`JjNPQ0Yl`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_es_sale_ntm_r1m_l1` | MATRIX / 1.0 / 0 | The probability that the future trend of 'NTM revenue revision, 1M' will fall | 1 | 0.05 / 0.01 (`vRrO2nxQ`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_es_sale_ntm_r1m_l3` | MATRIX / 1.0 / 1 | The probability that the future trend of NTM Revenue Revision, 1M" will be move-up" | 2 | 0.07 / 0.01 (`npdAPkk3`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_fincf_l1` | MATRIX / 1.0 / 0 | The probability that the future trend of Financing Activities Net Cash Flow" will be fall" | 2 | -0.39 / -0.12 (`P02MgrrW`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_fincf_l3` | MATRIX / 1.0 / 0 | The probability that the future trend of Financing Activities Net Cash Flow" will be move-up" | 1 | -0.45 / -0.15 (`akbVx2M1`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_sopi_l1` | MATRIX / 1.0 / 0 | The probability that the future trend of Operating Income" will fall" | 1 | -0.5 / -0.17 (`9qjEWPP2`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `oth460_sopi_l3` | MATRIX / 1.0 / 0 | The probability that the future trend of Operating Income" will be move-up" | 2 | -0.5 / -0.17 (`akbVx2X2`) | 仅为所列搭配中的结果；不能推断独立贡献 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 254 | `npdAPkk3` | 0.07 | 0.01 | -0.1 | 4.33 | -0.14 | 0.05 | 未核实 | 未核实 |
| 254 | `vRrO2nxQ` | 0.05 | 0.01 | -0.07 | 4.29 | -0.17 | 0.01 | 未核实 | 未核实 |
| 254 | `E5pVR0om` | -0.36 | -0.11 | -0.44 | 3.31 | -0.12 | -0.29 | 未核实 | 未核实 |
| 254 | `JjNPQ0Yl` | -0.37 | -0.11 | -0.44 | 3.32 | -0.13 | -0.3 | 未核实 | 未核实 |
| 254 | `P02MgrrW` | -0.39 | -0.12 | -0.89 | 2.22 | -0.11 | -0.33 | 未核实 | 未核实 |
| 254 | `akbVx2M1` | -0.45 | -0.15 | -0.91 | 2.21 | -0.15 | -0.38 | 未核实 | 未核实 |
| 254 | `akbVx2X2` | -0.5 | -0.17 | -0.62 | 4.14 | -0.31 | -0.55 | 未核实 | 未核实 |
| 254 | `9qjEWPP2` | -0.5 | -0.17 | -0.63 | 4.14 | -0.32 | -0.55 | 未核实 | 未核实 |

### 原式与局部失败证据

**npdAPkk3（wave 254）**

```text
group_rank(oth460_es_sale_ntm_r1m_l3,subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**vRrO2nxQ（wave 254）**

```text
group_rank(subtract(oth460_es_sale_ntm_r1m_l3,oth460_es_sale_ntm_r1m_l1),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**E5pVR0om（wave 254）**

```text
group_rank(oth460_1l_dlts,subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**JjNPQ0Yl（wave 254）**

```text
group_rank(subtract(oth460_1l_dlts,oth460_3l_dlts),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**P02MgrrW（wave 254）**

```text
group_rank(oth460_fincf_l1,subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**akbVx2M1（wave 254）**

```text
group_rank(subtract(oth460_fincf_l1,oth460_fincf_l3),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**akbVx2X2（wave 254）**

```text
group_rank(oth460_sopi_l3,subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

**9qjEWPP2（wave 254）**

```text
group_rank(subtract(oth460_sopi_l3,oth460_sopi_l1),subindustry)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

2026-09-25完成wave254，真实批`2bn6JB5X64wD9XUtNXf5ziY`八条全部COMPLETE，0执行错误。S4任务`campaign_EUR_S4_20260925_001414`、S6任务`campaign_EUR_S6_20260925_001633`均成功。完整合格0，Mode B资格0，未正式提交Alpha。

### 数据与字段的使用边界

平台将other460归入MODEL金字塔，不能按other前缀猜类别。1393个字段均为MATRIX；本轮八个字段coverage=1、users为0或1，这是2026-09-25元数据快照，不能证明预测收益或低相关性。model264字段表高度类似，不应作为一个新的独立信息来源重做同一批。

| 字段 | 本轮角色与经验 |
|---|---|
| `oth460_sopi_l3` | 经营利润上升概率，既作单侧基线又作概率差正向项；两式S均-.50，不支持利润改善概率直接带来正向股票收益 |
| `oth460_sopi_l1` | 经营利润下降概率，仅作为差额项；扣除后没有观察到改善，不能据此判死该字段的其他用途 |
| `oth460_1l_dlts` | 总债务下降概率，单侧S-.36；降债不等同盈利改善，未获得增强资格 |
| `oth460_3l_dlts` | 总债务上升概率，差额式的对立项；加入后S-.37，未提供值得扩展的表现 |
| `oth460_fincf_l1` | 融资活动净现金流下降概率，单侧S-.39；方向不能唯一映射为回购或偿债，也可能包含融资受限 |
| `oth460_fincf_l3` | 融资活动净现金流上升概率，差额对立项；差额S-.45/RN-.34，比单侧S-.39/RN-.24弱 |
| `oth460_es_sale_ntm_r1m_l3` | NTM收入预期1M修正的上升概率，单侧S.07/F.01；“1M”属于目标标签，不是已核实预测期限 |
| `oth460_es_sale_ntm_r1m_l1` | 同目标下降概率，仅用于差额；差额S.05/F.01，近期与风险中性指标未形成强信号 |

### 配对结果

方向概率差和单侧对照使用相同设置与分组，不增加平滑、回填或时间窗口。

| 经济问题 | 概率差Alpha | 单侧Alpha | Sharpe（差/单） | Fitness（差/单） | 2Y（差/单） | RN Sharpe（差/单） |
|---|---|---|---:|---:|---:|---:|
| 经营利润改善 | `9qjEWPP2` | `akbVx2X2` | -.50 / -.50 | -.17 / -.17 | -.63 / -.62 | -.16 / -.16 |
| 债务下降 | `JjNPQ0Yl` | `E5pVR0om` | -.37 / -.36 | -.11 / -.11 | -.44 / -.44 | -.24 / -.24 |
| 融资依赖下降 | `akbVx2M1` | `P02MgrrW` | -.45 / -.39 | -.15 / -.12 | -.91 / -.89 | -.34 / -.24 |
| 收入预期修正改善 | `vRrO2nxQ` | `npdAPkk3` | .05 / .07 | .01 / .01 | -.07 / -.10 | .06 / .06 |

八条longCount+shortCount均为1498，没有UNITS警告；每日样本集合与配对差异显著性仍未检验。两年值来自平台LOW_2Y_SHARPE，均为负。每条仍有4或5个RA检查失败，另有CLUSTER_TEST等警告；COMPLETE只表示模拟完成。Prod/Self未核实，不能当作0相关。因所有|S|<1，prod-first按规则未发昂贵相关性查询。

### 该停止什么、保留什么

关闭这八条已测结构在EUR/TOPCS1600/D1/SUBINDUSTRY/decay4下的自动扩展；不反号、不扫窗口，不判死1393字段的整个数据集。最高|S|仅.50，翻号也没有足够的现有强度证据。

GEM实际生成56条，`selection_w254`精确选入8条；48条自动平滑、窗口和分组变体留在延后审计，未回测不等于失败。“8条”由四组研究问题推导，不是覆盖整个机会集的固定上限。

`research_leads_w254`保留三个问题：上下行概率是否近似单调变换；供应商的预测期限、校准与PIT；是否存在经济含义不同的新目标。当前预算0，不进入near/ready。重新开启需新的供应商或原始数据证据支持具体有界纠错，或完成新机制的S0/S1论证；不能仅因原池还有48条便自动回测。

设计与完整过程见[other460概率探针](../eur_d1_20260925_other460_probability_probe.md)，权威结论为DB `s6_verdict_254`及`EUR-W254-OTHER460-FORWARD-PROBABILITY-PAIRS`。
