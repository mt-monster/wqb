# ASI · continuation_score 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：ASI / continuation_score；波次 s2_model28_d1；去重后 1 条已完成回测，1 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=该数据集全部已回测波次。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | MINVOL1M | SUBINDUSTRY | 未核实 | 未核实 | 未核实 | 未核实 |

最高 Sharpe 候选：`2rmEKjRx`，Sharpe=0.08，同条 Fitness=0.01，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `upward_scallop_similarity_median` | MATRIX / 1.0 / 5 | Median similarity score for ascending scallop pattern. | 1 | 0.08 / 0.01 (`2rmEKjRx`) | 仅为所列搭配中的结果；不能推断独立贡献 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s2_model28_d1 | `2rmEKjRx` | 0.08 | 0.01 | 0.4 | 4.51 | 0.18 | 未核实 | 未核实 | 未核实 |

### 原式与局部失败证据

**2rmEKjRx（wave s2_model28_d1）**

```text
ts_target_tvr_decay(group_rank(ts_mean(upward_scallop_similarity_median, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ASI_JPN_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO, LOW_ROBUST_UNIVERSE_RETURNS, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

待结合原式、字段语义与平台核查补充；机器统计不自动生成因果结论。
