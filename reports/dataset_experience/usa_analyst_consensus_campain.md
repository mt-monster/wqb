# USA · analyst_consensus 因子挖掘经验

<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照

- 范围：USA / analyst_consensus；波次 usa_targetprice_scan_20261007；去重后 54 条已完成回测，3 个实用字段。
- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。
- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。
- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。
- 筛选：delay=1；waves=该数据集全部已回测波次。

| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |
|---|---|---|---|---|---|---|
| 1 | TOP3000 | INDUSTRY | 未核实 | 未核实 | 未核实 | 未核实 |
| 1 | TOP3000 | NONE | 未核实 | 未核实 | 未核实 | 未核实 |
| 1 | TOP3000 | SECTOR | 未核实 | 未核实 | 未核实 | 未核实 |
| 1 | TOP3000 | STATISTICAL | 未核实 | 未核实 | 未核实 | 未核实 |
| 1 | TOP3000 | SUBINDUSTRY | 未核实 | 未核实 | 未核实 | 未核实 |

最高 Sharpe 候选：`wpbagVMY`，Sharpe=2.03，同条 Fitness=1.36，Prod=未核实。

## 字段证据与使用经验

| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |
|---|---|---|---:|---|---|
| `mean_estimate_fxadj_targetprice_annual12_tribes` | MATRIX / 0.9592 / 5 | Mean (consensus) target price estimate after currency and split adjustment | 1 | 1.57 / 0.83 (`XgJo60Ra`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `mean_estimate_targetprice_annual12_tribes` | MATRIX / 0.9592 / 11 | Mean (consensus average) of analyst target price estimates | 52 | 2.03 / 1.36 (`wpbagVMY`) | 仅为所列搭配中的结果；不能推断独立贡献 |
| `median_estimate_targetprice_annual12_tribes` | MATRIX / 0.9592 / 2 | Median of analyst target price estimates | 1 | 1.6 / 0.86 (`0mrpvZ08`) | 仅为所列搭配中的结果；不能推断独立贡献 |

## 已完成候选逐条记录

| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| usa_targetprice_scan_20261007 | `vR2NgnVQ` | 1.62 | 0.87 | 1.61 | 6.06 | 0.74 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `JjQGKYME` | 1.59 | 0.85 | 1.53 | 5.91 | 0.73 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `786z90gQ` | 1.69 | 0.93 | 1.67 | 6.09 | 0.8 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `O08GaxNb` | 1.58 | 0.84 | 1.55 | 5.87 | 0.71 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `pw5NOW63` | 1.62 | 0.87 | 1.54 | 5.99 | 0.76 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `YPMvqlbw` | 1.6 | 0.85 | 1.55 | 5.83 | 0.71 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `6XKpONWE` | 1.57 | 0.83 | 1.3 | 5.61 | 0.73 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `0mrpvZ08` | 1.6 | 0.86 | 1.46 | 5.92 | 0.72 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `GrOGJjNG` | 1.58 | 0.84 | 1.44 | 5.76 | 0.73 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `XgJo60Ra` | 1.57 | 0.83 | 1.48 | 5.94 | 0.71 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `0mrpvO8K` | 2.01 | 1.34 | 1.62 | 6.99 | 0.66 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `2rmpbe36` | 2.02 | 1.35 | 1.63 | 6.95 | 0.68 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `9qWp0PG2` | 2.02 | 1.35 | 1.63 | 6.86 | 0.72 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `O08GawAg` | 2.02 | 1.35 | 1.62 | 6.77 | 0.76 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `wpbagVMY` | 2.03 | 1.36 | 1.58 | 6.58 | 0.79 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `MP3GWneM` | 1.98 | 1.31 | 1.5 | 7.23 | 0.61 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `O08GPNg1` | 1.99 | 1.32 | 1.54 | 7.15 | 0.62 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `RR6mnWNz` | 2 | 1.33 | 1.57 | 7.09 | 0.63 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `A1vGMMZE` | 2.01 | 1.34 | 1.6 | 7.04 | 0.64 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `1YZp5vmW` | 0.84 | 0.6 | 0.84 | 1.59 | 0.52 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `gJZ8zwLm` | 0.69 | 1 | 0.01 | 0.73 | 0.59 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `YPMvdmlw` | 0.89 | 0.65 | 0.86 | 1.47 | 0.55 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `GrOGvE5o` | 0.78 | 0.53 | 0.83 | 1.67 | 0.49 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `pw5NOxw3` | 1.7 | 0.95 | 1.66 | 6.1 | 0.85 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `58gpWgxM` | 1.71 | 0.96 | 1.6 | 6.1 | 0.89 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `GrOGJGE0` | 1.73 | 0.99 | 1.55 | 6.09 | 0.93 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `A1vGK5xY` | 1.58 | 0.89 | 0.96 | 6.18 | 0.69 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `9qWp0elK` | 1.64 | 0.93 | 1.27 | 6.18 | 0.75 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `MP3GmEV9` | 1.71 | 0.99 | 1.55 | 6.18 | 0.8 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `npPNb9kx` | 1.77 | 1.03 | 1.73 | 6.17 | 0.8 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `KPrGR3Y1` | 1.75 | 1 | 1.7 | 6.13 | 0.9 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `3qVpWZWZ` | 1.73 | 0.99 | 1.74 | 6.15 | 0.83 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `1YZp5xzk` | 1.77 | 1.03 | 1.71 | 6.17 | 0.8 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `ZYAELArZ` | 1.76 | 1.03 | 1.68 | 6.17 | 0.79 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `1YZp5ZKk` | 1.74 | 1.01 | 1.64 | 6.17 | 0.79 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `MP3GAg59` | 1.78 | 1.04 | 1.75 | 6.17 | 0.81 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `JjQGLzgm` | 1.78 | 1.04 | 1.76 | 6.17 | 0.81 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `xAbNaprJ` | 1.78 | 1.04 | 1.76 | 6.17 | 0.81 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `d51Zwrr2` | 1.77 | 1.03 | 1.76 | 6.16 | 0.82 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `KPrGR1kg` | 1.75 | 1.02 | 1.66 | 6.17 | 0.78 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `qM0NZ72P` | 1.76 | 1.02 | 1.76 | 6.14 | 0.78 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `akx13a0W` | 1.78 | 1.04 | 1.71 | 6.18 | 0.81 | 未核实 | 未核实 | 未核实 |
| usa_targetprice_scan_20261007 | `9qWpQlO9` | 1.78 | 1.05 | 1.69 | 6.19 | 0.82 | 未核实 | 0.6982 | 0.4087 |
| usa_targetprice_scan_20261007 | `YPMvZZvv` | 1.79 | 1.06 | 1.68 | 6.2 | 0.83 | 未核实 | 0.6958 | 0.4106 |
| usa_targetprice_scan_20261007 | `1YZpv1bK` | 1.79 | 1.06 | 1.66 | 6.2 | 0.83 | 未核实 | 0.6934 | 0.4122 |
| usa_targetprice_scan_20261007 | `O08GeKx1` | 1.8 | 1.07 | 1.65 | 6.2 | 0.84 | 未核实 | 0.6911 | 0.4137 |
| usa_targetprice_scan_20261007 | `E5RGoOX1` | 1.81 | 1.09 | 1.65 | 6.19 | 0.86 | 未核实 | 0.6869 | 0.4163 |
| usa_targetprice_scan_20261007 | `XgJoXm50` | 1.84 | 1.12 | 1.68 | 6.16 | 0.88 | 未核实 | 0.6823 | 0.4191 |
| usa_targetprice_scan_20261007 | `1YZp6EP6` | 1.86 | 1.14 | 1.7 | 6.13 | 0.91 | 未核实 | 0.6783 | 0.4214 |
| usa_targetprice_scan_20261007 | `58gp1wdz` | 1.89 | 1.18 | 1.72 | 6.09 | 0.94 | 未核实 | 0.6738 | 0.4237 |
| usa_targetprice_scan_20261007 | `rKe2woad` | 1.92 | 1.21 | 1.73 | 6.04 | 0.98 | 未核实 | 0.6697 | 0.4253 |
| usa_targetprice_scan_20261007 | `KPrGp2G8` | 1.93 | 1.23 | 1.72 | 6.0 | 1.01 | 未核实 | 0.6649 | 0.4268 |
| usa_targetprice_scan_20261007 | `KPrGMEe1` | 1.94 | 1.24 | 1.71 | 5.94 | 1.04 | 未核实 | 0.6593 | 0.4277 |
| usa_targetprice_scan_20261007 | `KPrGMXZ8` | 1.95 | 1.26 | 1.7 | 5.9 | 1.06 | 未核实 | 0.654 | 0.4281 |

### 原式与局部失败证据

**vR2NgnVQ（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,300),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**JjQGKYME（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**786z90gQ（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**O08GaxNb（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,425),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**pw5NOW63（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,350),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**YPMvqlbw（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,450),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**6XKpONWE（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,600),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**0mrpvZ08（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(median_estimate_targetprice_annual12_tribes,400),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**GrOGJjNG（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,500),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**XgJo60Ra（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_fxadj_targetprice_annual12_tribes,400),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**0mrpvO8K（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**2rmpbe36（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**9qWp0PG2（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**O08GawAg（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**wpbagVMY（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**MP3GWneM（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**O08GPNg1（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**RR6mnWNz（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**A1vGMMZE（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,400),market)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**1YZp5vmW（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**gJZ8zwLm（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**YPMvdmlw（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**GrOGvE5o（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**pw5NOxw3（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**58gpWgxM（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**GrOGJGE0（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,250),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**A1vGK5xY（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,100),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**9qWp0elK（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,125),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**MP3GmEV9（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,150),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**npPNb9kx（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**KPrGR3Y1（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,225),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**3qVpWZWZ（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,200),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**1YZp5xzk（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,172),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**ZYAELArZ（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,170),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**1YZp5ZKk（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,160),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**MP3GAg59（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,178),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**JjQGLzgm（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,180),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**xAbNaprJ（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,182),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**d51Zwrr2（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,185),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**KPrGR1kg（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,165),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**qM0NZ72P（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**akx13a0W（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**9qWpQlO9（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**YPMvZZvv（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**1YZpv1bK（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**O08GeKx1（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**E5RGoOX1（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**XgJoXm50（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**1YZp6EP6（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**58gp1wdz（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**rKe2woad（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**KPrGp2G8（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**KPrGMEe1（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

**KPrGMXZ8（wave usa_targetprice_scan_20261007）**

```text
group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)
```

已存检查失败：未记录失败项；仍须按完整 Regular 标准核查。

### 读取限制

- JjNRAw1j delay 未知，不能归入 D1
- zq8XxM0O delay 未知，不能归入 D1
- 9qjgevmx delay 未知，不能归入 D1
<!-- END WQB DATASET EVIDENCE -->

## 人工机制复盘

> 证据来源分层：**实测** = 平台回测/`get_alpha_details`/`check_correlation`/submit_verdict 输出；
> **反算** = 由实测数据拟合的公式；**推论** = 因果解释。三者逐条标注，不混用。

### 1. 范围与设置

- **新增回测**：wave `usa_targetprice_scan_20261007`，54 条探针（`tmp_probe_conc.py` 单条 POST、逐条 checkpoint：
  `tracking/USA/candidates/probe_<tag>.json`），执行时间 2026-10-06 ~ 10-07。子族：champ_d45~d240（market 轴 × 窗口 400）9 条、
  acs8_d120 10 条、sub250 3 条、subw（窗口 100–225）6 条、neut（中性化轴）4 条、win175（窗口 160–185）8 条、
  z175（decay 160–500）14 条。
- **历史复核**：`probe_flash_eps_20260919`（3 条）为更早的 eps 探针，未纳入本节机制结论。
- **只读研究**：`get_datafields` 白空间盘点、prod 相关性直方图、`performance_comparison` 池贡献。
- **固定设置**：USA / TOP3000 / EQUITY / delay 1 / truncation 0.08 / pasteurization ON / nanHandling ON /
  maxTrade OFF / maxPosition OFF / IS 2014-01-01→2023-12-31。扫描轴 = 窗口 W × decay D × 分组轴 × 中性化。
- **落台产物**：`KPrGMXZ8`（decay 500）经用户逐字授权提交，`USA_R_anltp_sub_01`，status ACTIVE，
  dateSubmitted 2026-10-07T00:39:38-04:00，os.startDate 2024-01-01。

### 2. 字段经验

- **`mean_estimate_targetprice_annual12_tribes`**（主信号，54 条中 44 条使用）：分析师 12 个月一致目标价均值，
  状态量/连续型，适合 `ts_zscore`。本战役唯一走到提交的字段。
- **事件量字段禁 `ts_zscore`（实测报错）**：`mean_estimate_eps_annual12`、`max_estimate_current_period_revenue_annual12`
  报 `ERROR Operator ts_zscore does not support event inputs`；要么换算子（`ts_rank`/截面），要么换字段。
- **表达式字段名无数据集前缀**（写 `mean_estimate_targetprice_annual12_tribes`，不带 `analyst_consensus.`）。
- **合法分组名**：`market` / `subindustry` / `industry` / `sector` / `country`；`region` 非法（整批拒绝）。
- **白空间（只读研究，2026-10-07）**：全数据集 3424 字段，累计仅探约 21 个；`get_datafields(search="consensus")`
  100 字段几乎全 `alphaCount=0` 且 `sharpe_filter_removed=0`。高覆盖零使用清单（coverage/αCount）：
  `mean_estimate_current_period_revenue_annual12`(0.9751/0)、`mean_estimate_net2`(0.9742/0)、
  `mean_estimate_ebit_annual12_2`(0.9632/0)、`mean_estimate_reportednet_annual12_2`(0.9589/0)、
  `mean_estimate_pretax_annual12_2`(0.9431/0)、`mean_estimate_eps_annual12`(0.9521/38)、
  `mean_estimate_epsreported_annual12`(0.9433/3)、`median_estimate_revenue_quarterly16`(0.9248/0)、
  `mean_estimate_ebit_quarterly16_tribes`(0.8967/0)、`mean_estimate_ebitda_quarterly16`(0.7905/0)、
  `mean_estimate_fcf_annual12`(0.7902/8)、`mean_estimate_cogs_annual12_tribes`(0.7479/0)。
- **名称与语义**：`*_tribes` 后缀是聚合层级标记，非独立机制；annual12/quarterly16 是**期限**维度
  （wave 用「期限梯度」时是可用的结构自由度，见 §4 待验证区）。

### 3. 机制对照（同一候选逐条列，不跨候选拼最好指标）

**A. z175 族 decay 扫描（`group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)`，实测）**

| decay | alpha_id | S | F | 2Y | SUB | TO | prod | self |
|---|---|---|---|---|---|---|---|---|
| 500 | **KPrGMXZ8（已提交）** | 1.95 | 1.26 | 1.70 | 1.06 | 0.059 | 0.6540 | 0.4281 |
| 450 | KPrGMEe1 | 1.94 | 1.24 | 1.71 | 1.04 | — | 0.6593 | 0.4277 |
| 400 | KPrGp2G8 | 1.93 | 1.23 | 1.72 | 1.01 | — | 0.6649 | 0.4268 |
| 360 | rKe2woad | 1.92 | 1.21 | 1.73 | 0.98 | — | 0.6697 | 0.4253 |
| 300 | 1YZp6EP6 | 1.86 | 1.14 | 1.70 | 0.91 | — | 0.6783 | 0.4214 |
| 250 | E5RGoOX1 | 1.81 | 1.09 | 1.65 | 0.86 | — | 0.6869 | 0.4163 |
| 200 | 9qWpQlO9 | 1.78 | 1.05 | 1.69 | 0.82 | — | 0.6982 | 0.4087 |
| 180 | npPNb9kx | 1.77 | 1.03 | 1.73 | 0.80 | 0.062 | 0.7032 ❌ | 0.4043 |

（330/275/230/220/210 中间点见 DB `usa_targetprice_scan_20261007`，趋势单调不重复列。）
**结论（实测）**：decay 在该族上是「六指标 + prod + 稳健性」同向改善的单一杠杆，且 TO 0.062→0.059 几乎不变
（非平滑惰性化）——与「平滑类算子抬高 prod」的跨区经验**相反**，该经验在本族不适用。
**prod 余量**：0.046（d500）随 decay 递减到 −0.0032（d180）。2020 单年 −1.17（d500）、2023 0.69；10 年 9 正。

**B. 分组轴对照（N1 = 同表达式 w250 subindustry vs 其他轴，实测）**
subindustry 是唯一 SUB PASS 的轴；market/industry/sector 要么 SUB 失败要么 S 塌。
但**先浅后深的教训**：d30 时 subindustry S 1.54–1.56 < 1.58，一度误判「subindustry 救不了」；
与高 decay 组合后 S 抬升速度反超 market 轴（+8.3% vs +2.5%）。**扫参数必须扫到斜率拐过去为止。**

**C. 中性化轴对照（实测，全灭）**：STATISTICAL 之外，SUBINDUSTRY→S 0.78 / INDUSTRY→0.84 /
SECTOR→0.89 / NONE→0.69，2Y 全 FAIL ⇒ STATISTICAL 是唯一选择。

**D. 窗口轴对照（win175 8 点 + z175 曲线，实测）**：z170/172/175/178 @ d180 prod 全 0.703±0.0002
⇒ **窗口微调对 prod 谷无效**；prod 破线只靠 decay。窗口对 S 的影响：100–225 平缓，175 附近最优。

**E. 两个反算公式（由实测数据拟合，非平台文档）**
- **SUB 是比值闸**：`LOW_SUB_UNIVERSE_SHARPE.limit ≈ 0.431 × S`（8 个数据点反算全吻合）⇒ 真判据 SUB/S ≥ 0.431。
- **Fitness**：`F ≈ 2.813 × S × √returns`（2 点精确校验）⇒ F 不吃 turnover，提 S 或 returns 即可。

**F. CLUSTER_TEST 非硬闸（实测）**：0.45–0.84 全部只进 `checks.warning`，不进 `ra.failed_ra_checks`。
**G. 池贡献（performance_comparison，实测）**：before S 4.28/F 2.91 → after S 4.37/F 2.94，边际为正。
**H. 提交链路（实测）**：POST 201 async → 240s 未翻 → 补发一次 → 403 `ALREADY_SUBMITTED` → ACTIVE。
**I. prod 直方图判读（实测）**：d180 的 [0.6,0.7)=0 + [0.7,0.8)=1 是「谷/孤岛」形态（可救）；
右移拥挤带形态则调参无用——看形态不只看 max。

### 4. 后续决策

**有效线索（已兑现）**
- 目标价一致预期水平的 175d z-score + subindustry 组内排序 + decay 500 ⇒ 1 颗 ACTIVE（本族唯一出口）。
- decay 单调改善、SUB 比值闸、fitness 公式、窗口对 prod 无效 —— 全部可迁作**方法论**（跨区用前须重验数值）。

**已失败结构（跳过，不重复尝试）**
- 同结构换字段复刻本族 ⇒ self 0.82–0.93 复制品锁死（跨区实证）；**一条腿只出一颗**，11 个 decay 备选不再提。
- 中性化轴扫描（4 种全灭）；窗口微调破 prod（0.0002 级无效）；market/industry/sector 分组轴。
- 事件量字段 × `ts_zscore`（算子层拒绝，非参数问题）。
- 浅 decay（≤90）+ 短窗组合：S 结构性 < 1.58。

**待验证区（只有假设，未回测，不得记为有效）**
- **期限梯度**：`subtract(rank(mean_estimate_*_quarterly16), rank(mean_estimate_*_annual12))` ——
  EUR `analyst_revision_horizons` 上已成立（S 1.57/F 1.02，wave361）；**迁移到 USA 是假设**，跨区禁类比符号与幅度。
- 修正动量：`ts_delta(mean_estimate_*, D)` / 修正幅度 z-score（水平族的机制变体，须 self 实测防复制品）。
- 分歧度（std/mean）、surprise（实际 vs 一致）、白空间 12 字段（§2 清单）。
- **重新开启本族第二颗的条件**：换机制（非换字段）+ 对 `KPrGMXZ8` self 实测 < 0.7。

**下一批建议配比**（8–12 条）：期限梯度 3–4（annual12×quarterly16 组合）、修正动量 3（状态量字段）、
白空间字段直探 3–4（先 ts_zscore 状态量、事件量换 `ts_rank`）。发批走单条 POST + checkpoint，conc ≤ 7。

### 5. 边界

- **IS 不是 OS**：KPrGMXZ8 的 OS 期自 2024-01-01 起，尚无任何 OS 表现；IS 的 1.95 不预测 OS（跨区经验期望 OS ≈ 0.32×IS）。
- **冷门 ≠ 低相关**：`alphaCount=0` 只说明没人用过；prod/self 必须实测（本战役 prod 0.654 是提交时快照）。
- **空失败列表 ≠ Regular 全通过**：`checks.pending`（SELF/PROD/REGULAR_SUBMISSION 等）在名单外不计卡，
  但也不构成放行依据；配额唯一权威 = 提交时 `quota_gate` / POST 403 读数（quota_status 已三次误报）。
- **已知软标记随 KPrGMXZ8 提交**：衰减比 0.35、Recent-3yr CV 0.44、2023 走弱（S 0.69）、2020 单年亏损——
  OS 复盘时先看这几项是否兑现成真衰减。
- **因果解释只标推论**：「分析师目标价修正被市场缓慢消化」是**推论**，本节其余均为实测或反算。
- 证据块中 margin/returns/drawdown 多为「未核实」：探针 checkpoint 只存 S/F/T/sub/y2；
  全量指标仅冠军与 prod 曲线族有（`get_alpha_details` 实测）。机器统计不自动生成因果结论。

---

## 6. 第二波机制拓展实测（2026-10-07 续挖，26 条回测：v1 11 + v2 10 + v3 11 + decay 9 + v3b 5）

### 6.1 ★★★ 字段类型铁律：MATRIX vs VECTOR（本波最大工程发现）
- **平台字段 `type` 分 MATRIX / VECTOR，与"事件量"错误直接对应**：VECTOR 字段裸用任何常规算子
  （`rank`/`ts_zscore`/`ts_rank`/`ts_delta`，截面时序全算）⇒ 秒拒 `"Operator X does not support event inputs"`。
- **唯一出路 = `vec_*` 聚合**（`vec_avg`/`vec_sum`/`vec_min`/`vec_max`/`vec_stddev`/`vec_range`/`vec_count`）裹成标量再进常规算子。
- **本数据集类型地图**：`targetprice_annual12_tribes` 全族 11 字段 = **MATRIX**（冠军可用 ts_zscore 即因此）；
  `mean_estimate_*` / `stddev_*` / `*_prior_*` 快照 / `mean_forecast_actual_*` / `mean_surprise_value_*`（含 `_tribes` 后缀的 surprise）
  = **VECTOR**。**后缀判类型会翻车，必须查 `get_datafields` 的 `type` 字段。**
- 工程坑：`POST /simulations` 单条必须裸 dict（数组包装 = multi-sim 语义 ⇒ 400）；`preflight_expressions`/`fix_vector_fields`
  的类型拉取可能退化（`any_changed:false` 漏包）⇒ **手包 `vec_*` + 本地 VECTOR-wrap 硬校验**最稳。
- **decay 平台硬上限 512**（d700 ⇒ `settings.decay: Ensure this value is less than or equal to 512`）。

### 6.2 三族机制判决（d300 基线 + decay 扫描 d400/500/512 + 杠杆试验）
**TG 期限梯度（quarterly16 − annual12 分位差）：判死。** S 0.4–1.1 全灭（TG_EPS 0.4/TG_REV 1.1/TG_EBIT 0.84）。
EUR `analyst_revision_horizons` 的期限梯度**不迁移到 USA**（跨区禁类比实证再次成立）。

**RM 修正动量（`ts_delta(vec_avg(FA共识),63)`）：S/2Y 极强但双堵，机制性无解。**
- RM_EPS d500 `0mrwRL2G`：S 1.72✓ F 1.09✓ **2Y 2.18✓**，仅卡 SUB（0.44 vs limit 0.74）；
  但 **prod 0.7514✗**（[0.7,0.8) 孤峰 n=1）。SUB/S=0.26 远低于比值线 0.431 ⇒ 大票（子宇宙）里修正幅度小、信号弱，**结构性**。
- decay 300→500 SUB 只 0.35→0.44（z175 族同区间 SUB→1.06）⇒ **decay 修不动机制性 SUB 缺口**。
- `group_zscore` 换 `group_rank` ⇒ S 1.72→0.85 塌（非保序杠杆在此为破坏性）；TOP1000 ⇒ S 0.97 塌（信号活在中小票）。
- RM_NP 同型（S 1.4/2Y 2.02/SUB 0.44）⇒ **RM 族整体判死（REGULAR 闸下）**，但 2Y 特性记录在案。

**TP 分歧族（targetprice MATRIX 族新机制）：唯一残留希望，IS 强度结构性 cap。**
- TP_SKEW d500 `786jN81v`（mean−median 缺口）：S 1.54/F 0.80/2Y 1.45 **三项全在下沿**（差 2.5%/20%/8%），
  SUB 1.13✓ **prod 0.548✓ self 0.372✓**（池 130，非复制品）。三个杠杆全无效：
  `signed_power(x,1.5)` **no-op**（★ **group_rank 内层单调变换不改排序 ⇒ 保序变换全是空转**——幂次要用在 scale-sensitive 位置才有效）；
  fxadj 换版 1.53；decay 512 1.54。**结论：S≈1.54 是机制 cap。**
- TP_DISP（stddev 分歧度 zscore）d300 `2rmll1db`：S 1.73✓ 但 F 0.97/2Y 1.06/SUB 0.51 三项挂，
  prod 0.640✓ self 0.373✓。decay 曲线反走（d400 1.71/d500 1.67）⇒ d300 即峰。
- TP_SPREAD/TP_REV/TP_CNT 中庸（S 1.25–1.44）；DS_RANGE（vec_range 分歧）S 0.7 弱。

### 6.3 本波后续决策
- **可提交候选：0 颗**。最近 = TP_SKEW d500（corr 双过、SUB 强、IS 三项 cap）。
- **重开条件**：TP_SKEW 族若能找到**非保序**增强（改权重几何/分组内 zscore 化/换 group 轴）或新分歧字段族，
  且对 `KPrGMXZ8` + `786jN81v` 双 self < 0.7，可再试；RM/TG 族不再投入。
- 26 条已全部入 `mining_ledger`（SIM_OK）与 DB wave `usa_amech_v3_20261007`/`usa_amech_v3b_20261007`。

---

## 7. 786jN81v 破闸专项（2026-10-07，文献+论坛驱动，26 条回测）

**起点** `786jN81v` = `group_rank(subtract(rank(mean_targetprice), rank(median_targetprice)), subindustry)`，S 1.54/F 0.80/2Y 1.45 三闸全挂（SUB 1.13/prod 0.548/self 0.372 已过）。

### 7.1 灵感来源（外部，非凭空调参）
- 论坛（WQ BRAIN 中文）：目标价**水平**无信息；有信息的是「变化趋势」与「与行业中位数偏离度的收窄/发散」。
- **Meng (2014, UNC)**：偏度×分歧度**交互定价**——正偏时分歧↑⇒收益↑，负偏时相反。
- **Steffen & Zhang (Yale)**：分析师**延迟下调**（staleness）+ 高离散×高上行 ⇒ 未来负收益。
- **PHBS**：含**时序**变化的离散度预测力显著强于纯截面。
- **算子对账**：平台 103 个算子，此前仅用 7 个 ⇒ 差集取出 `ts_std_dev/abs/days_from_last_change/divide/if_else/reverse/ts_mean/ts_rank/winsorize`。

### 7.2 结果（USA/TOP3000/D1/STATISTICAL/trunc0.08，decay 500）
| 候选 | 机制 | S | F | T | 2Y | SUB(limit) | prod/self | 卡点 |
|---|---|---|---|---|---|---|---|---|
| `npPdporE` TP_IF | 偏度方向×离散（if_else） | 1.87 | 1.04 | 0.038 | 1.61✓ | 0.78(0.81) | **0.547/0.331 ✓** | SUB 差 0.03 |
| `RR6bRmpa` TSR250 | 偏度时序排名 | 1.74 | 1.04 | 0.054 | 2.13✓ | 0.73(0.75) | — | SUB 差 0.02 |
| `omWLpmqn` TSR125 | 短窗时序排名 | **1.91** | **1.27** | 0.063 | **2.49✓** | 0.64(0.83) | — | SUB 崩 |
| `RR6bQeda` TSR175 | 中窗时序排名 | 1.86 | 1.18 | 0.058 | 2.43✓ | 0.69(0.81) | — | SUB 崩 |
| `wpbZmwXx` IF_M60 | IF+ts_mean60 | 1.91 | 1.03 | 0.034 | 1.37✗ | **0.84✓** | — | 只卡 2Y |
| `786NbK62` IF_M45 | IF+ts_mean45 | **1.94** | 1.06 | 0.035 | 1.43✗ | 0.85✓ | — | 只卡 2Y |
| `E5RpWlRK` IF_M20 / `Vk0agOdM` IF_M10 | IF+轻平滑 | 1.92/1.89 | 1.06/1.04 | 0.036 | 1.50/1.52✗ | 0.83✓/0.82✓ | — | 只卡 2Y |
| **`GrObPoGQ` STALE_REV** | **目标价陈旧度反向** | 1.70 | 1.05 | 0.055 | 1.77✓ | 0.75✓ | **prod 0.7738 ✗** | **failed_ra_count=0** |
| `9qWjqgJ9` STALE（未取反） | 陈旧度正向 | −1.70 | −1.05 | 0.055 | — | — | — | 方向反了 |

### 7.3 ★ 方法论结论
1. **ts_mean 平滑窗口 = SUB↔2Y 的权衡旋钮**（实测单调）：M0 SUB 0.78✗/2Y 1.61✓ → M10 0.82✓/1.52✗ → M45 0.85✓/1.43✗。
   **两侧都差一点点但没有交叉点**（M0 需 SUB +0.026，M10 需 2Y +0.06；2Y 塌得比 SUB 长得快）⇒ **TP_IF 族在当前设置空间内无解**。
2. **SUB 门限随 S 涨**（limit≈0.431×S）⇒ 单纯提 S 会同步抬高 SUB 线：TSR125 的 S 1.91 反而 SUB 崩到 0.64/0.83。
3. **staleness 反向 = 本战役第二颗 RA 全过候选（failed_ra_count=0）**，机制与 Yale 文献完全吻合；
   但 **prod 0.7738**（[0.7,0.8) n=3、上一桶 n=61 = 非孤岛）⇒ 该机制已被人做过。
4. 引入 `close` 做价格归一化（TP_UPDSP）反而把信号打掉（S 0.99）——目标价类信号**不要做价格归一化**。
5. 相关性已实测通过的组合：`npPdporE` prod 0.547/self 0.331（随时可进提交流程，只差 SUB）。

### 7.4 后续
- **TP_IF 族**：设设置空间已穷尽（decay 300/400/500/512、ts_mean 0/10/15/20/30/45/60 全扫）⇒ **判停**。
- **staleness 族**：RA 全过，唯一卡点 prod 0.774 ⇒ 若要救，需**换载体**（其它数据集/其它区域的"陈旧度"字段）或
  换 staleness 的构造（`last_diff_value` / `ts_count_nans` / `days_from_last_change` 作用于其它目标价统计量）。
- 提交纪律不变：**零自动提交**，用户逐次授权；`npPdporE` 若后续找到 SUB 解法，prod/self 已备。

### 7.5 ★★ SUB 破闸专项（2026-10-08）——TP_IF 族复活，`RR6bv6rz` 全闸通过

**触发**：用户令破 `npPdporE` 的 SUB 闸（0.78 vs 0.81）。论坛深读 YW79016（hump 帖 50 票/35 评）+ XB37939（案例帖 37 票）+ JL23335/HY22845/M10 评论实证。

**微批 1（exprs_usa_tpsubfix.json，9 条）全灭，但定调边界**：
- signed_power 三档（XB37939 配方）：y=0.5 抬 S→2.12 但 SUB 纹丝不动（0.77）比值反降 0.363；y=2/1.5 杀 S——**提 S 杠杆全被 `limit=0.433×S` 吃掉**。
- hump=0.005 冻死（S 1.0）、ts_target_tvr_hump 比值崩到 0.301——**低 TO(0.038) 慢信号禁 hump 族**（论坛边界全命中）。
- `vector_neut(…, rank(volume*close))` 塌（S 0.83）——**小票倾斜就是利润来源**，剥离即死（病根实证）。
- LIQ_IF（if_else 硬切流动性分组衰减，合规版）比值 0.417→0.424 微升；M5 补齐窗口刀刃（SUB 0.80/2Y 1.57，仍无交叉）。

**微批 2（exprs_usa_tpsubfix2.json，6 条）决胜**：
| 变体 | id | S | SUB/limit | 2Y | SUB/S | 判 |
|---|---|---|---|---|---|---|
| **M10Q** `quantile(GR(ts_mean(core,10)), sigma=1.0)` | **`RR6bv6rz`** | **2.04** | **0.89/0.88✓** | **1.71✓** | **0.436** | **failed_ra=0，prod 0.592✓ self 0.357✓** |
| M10SP07 | N1Va2VNg | 2.06 | 0.83/0.89✗ | 1.53 | 0.403 | 提 S 被线吃 |
| M10NORM | akxbg1gO | 1.90 | 0.83/0.82✓ | 1.53⚠ | 0.437 | 只卡 2Y(warning) |
| M10AVD `ts_av_diff(core,22)` | WjebxVWQ | 1.89 | 0.75/0.82✗ | **1.96** | 0.397 | 2Y 专项杠杆 |
| M10RANK plain rank | E5Rp2RVL | 0.03 | — | — | — | 塌方 |

**★ 方法论（推翻 7.3/7.4 的「TP_IF 判停」）**：
1. **破 SUB 的终结技是「分布变换」不是「强度/平滑杠杆」**：`quantile(x, sigma=1.0)` 高斯重映射一步同时抬 SUB（0.82→0.89）与 2Y（1.52→1.71），比值 0.434→0.436 越线；signed_power/hump/ts_target_tvr 全是后者，被 `limit≈0.433×S` 同步吃掉。XB37939「换分布变换才过」的正解 = quantile，非 signed_power（其配方不可迁移）。
2. **SUB 闸判定一律用比值 SUB/S ≥ 0.433（USA）**，绝对值无意义。
3. `ts_av_diff(x,22)` = 2Y 专项杠杆（1.52→1.96 实证，HY22845「补近年」成立），可做 2Y 救援腿。
4. **group_rank(subindustry) 是 TP 分歧度族承重结构**（plain rank 塌到 S 0.03），禁换。
5. 「SUB↔2Y 刀刃无交叉」仅在**平滑窗口轴**内成立；跨到分布变换轴即破——判「族内无解」前必须把算子差集扫到分布变换类（quantile/normalize/winsorize）。

**提交候选**：`RR6bv6rz`（USA/TOP3000/D1/STATISTICAL/decay500，USA/D1/ANALYST 塔 ×1.2）——S2.04/F1.20/TO0.0382/ret4.32%/margin22.6bp，CLUSTER_TEST 1.56(warn)。**零自动提交，待用户授权**。同族近亲约束：与 npPdporE/GrObPoGQ 同核，若 RR6bv6rz 提交，同族只出这 1 颗。
