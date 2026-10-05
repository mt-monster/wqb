# ASI · pv13 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：ASI / pv13；波次 s2_pv13_d1；去重后 6 条已完成回测，4 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=全部（分设置展示）；waves=该数据集全部已回测波次。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | MINVOL1M | SUBINDUSTRY | 6 | 0.08 | 未核实 | 未核实 |

最高 Sharpe 候选：`A1v638gQ`，Sharpe=1.17，同条 Fitness=1.28，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `customer_revenue_share_percent` | VECTOR / 0.3831 / 1 | Percentage of company revenue attributed to a specific customer. | 1 | 0.19 / 0.05 (`e7QArZnJ`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `exposure_estimation_confidence_score` | VECTOR / 0.9656 / 5 | Confidence score indicating reliability of the estimated exposure value. | 2 | -0.11 / -0.02 (`1YZvgAnX`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `exposure_estimation_precision_score` | VECTOR / 0.9656 / 4 | Precision or error range for the estimated exposure value. | 2 | 0.53 / 0.61 (`leKx0PQe`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |
| `region_exposure_percent_maximum` | VECTOR / 0.9656 / 1 | Maximum estimated percentage of company revenue attributed to a region. | 2 | 1.17 / 1.28 (`A1v638gQ`) | 仅为所列搭配中的结果；不能推断独立贡献；须先聚合为 MATRIX |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s2_pv13_d1 | `1YZvgAnX` | -0.11 | -0.02 | 0.11 | 0.85 | -0.49 | 未核实 | 未核实 | 未核实 |
| s2_pv13_d1 | `leKx0PQe` | 0.53 | 0.61 | 0.56 | 2.91 | 0.39 | 未核实 | 未核实 | 未核实 |
| s2_pv13_d1 | `mL6OXWrx` | -0.48 | -0.17 | -1.21 | 0.88 | -0.61 | 未核实 | 未核实 | 未核实 |
| s2_pv13_d1 | `A1v638gQ` | 1.17 | 1.28 | 1.28 | 3.09 | 1.27 | 未核实 | 未核实 | 未核实 |
| s2_pv13_d1 | `3qVdAvaN` | -0.21 | -0.06 | 0.24 | 0.73 | -0.43 | 未核实 | 未核实 | 未核实 |
| s2_pv13_d1 | `e7QArZnJ` | 0.19 | 0.05 | 0.11 | 0.98 | 0.24 | 未核实 | 未核实 | 未核实 |

### 原式与局部失败证据

**1YZvgAnX（wave s2_pv13_d1）**

```text
ts_target_tvr_decay(multiply(group_rank(winsorize(ts_mean(vec_avg(exposure_estimation_confidence_score), 22), std=4), subindustry), group_rank(ts_mean(ts_backfill(vec_avg(exposure_estimation_confidence_score), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_ASI_JPN_SHARPE, LOW_2Y_SHARPE。

**leKx0PQe（wave s2_pv13_d1）**

```text
ts_target_tvr_decay(multiply(group_rank(winsorize(ts_mean(vec_avg(exposure_estimation_precision_score), 22), std=4), subindustry), group_rank(ts_mean(ts_backfill(vec_sum(region_exposure_percent_maximum), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, CONCENTRATED_WEIGHT, LOW_ASI_JPN_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO, LOW_ROBUST_UNIVERSE_RETURNS, LOW_2Y_SHARPE。

**mL6OXWrx（wave s2_pv13_d1）**

```text
ts_target_tvr_decay(multiply(group_rank(winsorize(ts_mean(vec_avg(exposure_estimation_precision_score), 22), std=4), subindustry), group_rank(ts_mean(ts_backfill(vec_avg(exposure_estimation_precision_score), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_ASI_JPN_SHARPE, LOW_2Y_SHARPE。

**A1v638gQ（wave s2_pv13_d1）**

```text
ts_target_tvr_decay(multiply(group_rank(reverse(ts_mean(ts_backfill(vec_avg(region_exposure_percent_maximum), 252), 66)), subindustry), group_rank(ts_mean(ts_backfill(vec_avg(region_exposure_percent_maximum), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)
```

已存检查失败：LOW_SHARPE, CONCENTRATED_WEIGHT, LOW_ASI_JPN_SHARPE, LOW_2Y_SHARPE。

**3qVdAvaN（wave s2_pv13_d1）**

```text
rank(ts_mean(vec_avg(exposure_estimation_confidence_score), 22))
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_SUB_UNIVERSE_SHARPE, LOW_ASI_JPN_SHARPE, LOW_2Y_SHARPE。

**e7QArZnJ（wave s2_pv13_d1）**

```text
ts_target_tvr_decay(group_rank(reverse(ts_mean(ts_backfill(vec_avg(customer_revenue_share_percent), 252), 66)), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.028)
```

已存检查失败：LOW_SHARPE, LOW_FITNESS, LOW_TURNOVER, LOW_ASI_JPN_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO, LOW_ROBUST_UNIVERSE_RETURNS, LOW_2Y_SHARPE。

<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

待结合原式、字段语义与平台核查补充；机器统计不自动生成因果结论。
