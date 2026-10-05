# ASI · model28 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：ASI / model28；波次 s2_model28_d1；去重后 5 条已完成回测，5 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=全部（分设置展示）；waves=该数据集全部已回测波次。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | MINVOL1M | SUBINDUSTRY | 未核实 | 未核实 | 未核实 | 未核实 |

最高 Sharpe 候选：`88PALvra`，Sharpe=0.54，同条 Fitness=0.27，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `continuation_downward_wedge_dynamic_similarity` | 未核实 / 未核实 / 未核实 | 未核实 | 1 | -0.34 / -0.1 (`N1VMOe6e`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `mdl28_sm_structural_credit_structural_distance_to_default` | MATRIX / 0.9737 / 0 | Number of standard deviations by which the firm's estimated asset value exceeds the default threshold; higher numbers me | 1 | 0.49 / 0.25 (`vR20mOzz`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `mdl28_sm_structural_credit_structural_pd_pct` | MATRIX / 0.9737 / 0 | Estimated 1-year probability of default expressed as a percentage for the company | 1 | 0.49 / 0.25 (`d51qQK7X`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `upward_scallop_similarity_median` | 未核实 / 未核实 / 未核实 | 未核实 | 1 | 0.08 / 0.01 (`2rmEKjRx`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |
| `v_shape_continuation_bottom_median_similarity_40d` | 未核实 / 未核实 / 未核实 | 未核实 | 1 | 0.54 / 0.27 (`88PALvra`) | 仅为所列搭配中的结果；不能推断独立贡献；本地目录缺字段元数据 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s2_model28_d1 | `88PALvra` | 0.54 | 0.27 | 0.38 | 4.88 | 0.37 | 未核实 | 未核实 | 未核实 |
| s2_model28_d1 | `N1VMOe6e` | -0.34 | -0.1 | -0.64 | 5.16 | -0.39 | 未核实 | 未核实 | 未核实 |
| s2_model28_d1 | `2rmEKjRx` | 0.08 | 0.01 | 0.4 | 4.51 | 0.18 | 未核实 | 未核实 | 未核实 |
| s2_model28_d1 | `d51qQK7X` | 0.49 | 0.25 | 0.9 | 1.35 | 0.53 | 未核实 | 未核实 | 未核实 |
| s2_model28_d1 | `vR20mOzz` | 0.49 | 0.25 | 0.9 | 1.36 | 0.53 | 未核实 | 未核实 | 未核实 |

### 原式与局部失败证据

**88PALvra（wave s2_model28_d1）**

```text
ts_target_tvr_decay(group_rank(ts_mean(v_shape_continuation_bottom_median_similarity_40d, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ASI_JPN_SHARPE, LOW_2Y_SHARPE。

**N1VMOe6e（wave s2_model28_d1）**

```text
ts_target_tvr_decay(group_rank(ts_mean(continuation_downward_wedge_dynamic_similarity, 22), country), lambda_min=0, lambda_max=1, target_tvr=0.05)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_SUB_UNIVERSE_SHARPE, LOW_ASI_JPN_SHARPE, LOW_2Y_SHARPE。

**2rmEKjRx（wave s2_model28_d1）**

```text
ts_target_tvr_decay(group_rank(ts_mean(upward_scallop_similarity_median, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ASI_JPN_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO, LOW_ROBUST_UNIVERSE_RETURNS, LOW_2Y_SHARPE。

**d51qQK7X（wave s2_model28_d1）**

```text
ts_target_tvr_decay(group_rank(reverse(ts_mean(ts_backfill(mdl28_sm_structural_credit_structural_pd_pct, 252), 22)), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ASI_JPN_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO, LOW_ROBUST_UNIVERSE_RETURNS, LOW_2Y_SHARPE。

**vR20mOzz（wave s2_model28_d1）**

```text
ts_target_tvr_decay(group_rank(ts_mean(ts_backfill(mdl28_sm_structural_credit_structural_distance_to_default, 252), 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_ASI_JPN_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO, LOW_ROBUST_UNIVERSE_RETURNS, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

待结合原式、字段语义与平台核查补充；机器统计不自动生成因果结论。
