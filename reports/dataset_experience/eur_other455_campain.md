# EUR · other455 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：EUR / other455；波次 253；去重后 4 条已完成回测，2 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=253。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOPCS1600 | SUBINDUSTRY | 4 | 0.08 | 2014-01-01 | 2023-12-31 |

最高 Sharpe 候选：`j2Aej6Le`，Sharpe=0.32，同条 Fitness=0.1，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5` | GROUP / 0.8691 / 0 | D1-lagged KMeans cluster label (k=5) based on the seed 1 latent embedding from the EUR customer Node2Vec (P10,Q200) | 4 | 0.32 / 0.1 (`j2Aej6Le`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `returns` | 未核实 / 未核实 / 未核实 | 未核实 | 4 | 0.32 / 0.1 (`j2Aej6Le`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 253 | `j2Aej6Le` | 0.32 | 0.1 | 未核实 | 7.55 | 0.21 | 0.42 | 未核实 | 未核实 |
| 253 | `O0NJ7GK1` | 0.16 | 0.04 | 未核实 | 7.03 | 0.22 | 0.32 | 未核实 | 未核实 |
| 253 | `xA31jNal` | 0 | 0 | 未核实 | 5.8 | -0.22 | -0.26 | 未核实 | 未核实 |
| 253 | `gJbWj8vv` | 0 | 0 | 未核实 | 5.8 | 0.22 | 0.26 | 未核实 | 未核实 |

### 原式与局部失败证据

**j2Aej6Le（wave 253）**

```text
rank(group_mean(ts_sum(returns,22),1,densify(oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, IS_LADDER_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE。

**O0NJ7GK1（wave 253）**

```text
rank(subtract(group_mean(ts_sum(returns,22),1,densify(oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5)),ts_sum(returns,22)))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, IS_LADDER_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE。

**xA31jNal（wave 253）**

```text
if_else(greater(group_count(returns,densify(oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5)),0),rank(ts_sum(returns,22)),0)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, IS_LADDER_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE。

**gJbWj8vv（wave 253）**

```text
if_else(greater(group_count(returns,densify(oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5)),0),reverse(rank(ts_sum(returns,22))),0)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, IS_LADDER_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

### 字段角色与实验边界

2026-09-24实查：other455有1500字段（1200 GROUP、300 MATRIX）。本波只使用`oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5`作为分组轴；w1是随机种子1，k5是5组，不能把标签数值当强弱分数。其描述明确EUR客户网络、D1滞后；coverage .8691、userCount0、alphaCount0。冷门不等于已验证信号。

`returns`来自辅助数据集pv1，平台已确认MATRIX、coverage1、userCount714、alphaCount1798、日收益。上方自动块只读取主数据集目录，故其元数据显示“未核实”；此处补充跨集真实来源，不把returns误归other455。独立使用经验见[eur_pv1_campain.md](eur_pv1_campain.md)。

固定22日、seed1/k5、EUR/TOPCS1600/D1/SUBINDUSTRY/decay4/truncation.08。selection_w253预先指定2主假设＋2对照，4/4执行；不扫描参数。网络同簇不等于直接客户，group_mean包含自身；历史网络PIT和逐日标签稳定性未获得证据。

### 实测配对与诊断

| 角色 / Alpha | S / F | 2年阶梯S | 风险中性S | 多/空数量 | 结论 |
|---|---|---:|---:|---:|---|
| 网络共同收益 / j2Aej6Le | .32 / .10 | .76 | -.07 | 639 / 614 | 原始强度弱，风险中性后转负 |
| 自身动量对照 / xA31jNal | .00 / .00 | .43 | .08 | 736 / 762 | 本轮基线无强度 |
| 网络相对滞后 / O0NJ7GK1 | .16 / .04 | .29 | .07 | 624 / 628 | 补涨假设弱 |
| 自身反转对照 / gJbWj8vv | -.00 / -.00 | -.43 | -.08 | 762 / 736 | 与动量对照镜像 |

2年阶梯数值来自实时MCP的`IS_LADDER_SHARPE year=2`；S4缓存中的`two_year_sharpe`为空，自动块沿用DB空值。本次在`s6_verdict_253`保留实时数值及来源，不将UNKNOWN当实测零，也不掩盖S4读取口径缺口。

两条网络式的平均多空数量合计1253/1252，对照为1498。`group_count>0`未形成可证明一致的有效持仓掩码，Sharpe差异不能作干净的网络增量归因；参数相同并不保证比较口径相同。四条均返回`REVERSION_COMPONENT`和`CLUSTER_TEST`警告，未见UNITS警告；模拟已产生Alpha且已收割，不是四个执行ERROR。主假设均4项RA失败；动量对照5项、反转对照4项。Prod/Self未测，因为廉价质量前置已明显失败。

### 下一轮应复用和避开的经验

- GROUP应作为group_mean/group_count等算子的分组参数；GEM已禁止对GROUP生成rank(label)/ts_delta(label)自动孤儿。densify原生GROUP标识符的语法兼容已修复，输出仍不能作为数值信号。
- 本波否定范围仅为上述固定的网络月收益结构。没有判死整集、所有嵌入字段或其它经济机制。
- 不扩w2/w3、k10/k20或窗口网格。`research_leads_w253`保留掩码、自身贡献和PIT问题，剩余模拟预算0；新证据和独立机制才能重新立项。
- 不能把.00→.32当增强资格，更不能仅凭冷门分组或能在平台运行就宣称存在Alpha。

来源：`selection_w253`、`review_253`、`s6_verdict_253`、`research_leads_w253`；实际模拟批`3GdY8S8yn4sg9kVr2gnHy93`，S4/S6任务均成功。当前完整合格0。
