# risk72 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `risk72` |
| 名称 | Specific return of extended factors |
| 类别 | RISK |
| 数据字段数(平台) | 40 |
| 覆盖率 | 0.6023 |
| 平台已有 alpha | 39 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.0 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive global coverage of analyst earnings estimates, company-issued guidance, and actual reported financials for over 60,000 companies. It includes both detailed and consensus forecasts for key financial metrics such as EPS, revenue, cash flow, and dividends, as well as analyst recommendations and price targets. The data is updated daily and includes historical records, point-in-time snapshots, and restated values to avoid look-ahead and survivorship bias. Industry classification is available via TRBC, and the dataset supports granular analysis by region, sector, and fiscal period. By tracking estimate revisions, consensus trends, and the relationship between guidance and market expectations, this dataset is highly valuable for predicting price movements aroun

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **40** |
| 类型分布 | MATRIX×34　VECTOR×6 |
| 平均覆盖率 | **0.602** |
| 覆盖率区间 | 0.15 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 11 | 27.5% |
| 中 (0.70–0.90) | 2 | 5.0% |
| 低 (0.50–0.70) | 14 | 35.0% |
| 稀疏 (<0.50) | 13 | 32.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 21 | 52.5% |
| DEAD | 10 | 25.0% |
| UNTESTED | 9 | 22.5% |

- 已实测字段：**10** 个（25%），best_sharpe 最高 **0.91**，中位 0.02

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 29 | 0.60 | top1200_equity_residualized_return_nogroup、top1200_equity_residualized_return_nocountry、top2500_equity_residualized_return |
| 价量与波动 | 11 | 0.62 | rsk72_top1200_dsrt、cfg2_top600_residual_return、cfg2_top1200_residual_return |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `rsk72_top1200_dsrt` | MATRIX | 1.000 | 价量与波动 | 2 | 0.91 | 1.65 | 0.91 | DEAD | Daily reproducible specific returns in % units |
| 2 | `cfg2_top600_residual_return` | MATRIX | 0.525 | 价量与波动 | 2 | 0.32 | -0.44 | 0.33 | DEAD | Daily matrix of residual (idiosyncratic) stock returns for the EUR TOP600 universe, in percent units, after neutralizing |
| 3 | `top1200_equity_residualized_return_nogroup` | MATRIX | 0.525 | 盈利与财务 | 1 | 0.06 | 0.52 | 0.06 | DEAD | Specific return for the top 1200 equities without group-based adjustments. |
| 4 | `top1200_equity_residualized_return_nocountry` | MATRIX | 0.525 | 盈利与财务 | 1 | 0.03 | 0.41 | 0.02 | DEAD | Specific return for the top 1200 equities without country-based adjustments. |
| 5 | `top2500_equity_residualized_return` | MATRIX | 1.000 | 盈利与财务 | 1 | 0.02 | -1.05 | — | DEAD | Specific return for the top 2500 equities in the selected universe. |
| 6 | `top2500_equity_residualized_return_nocountry` | MATRIX | 1.000 | 盈利与财务 | 3 | 0.00 | -0.53 | -0.13 | DEAD | Specific return for the top 2500 equities without country-based adjustments. |
| 7 | `ats_top1200_equity_residualized_return` | MATRIX | 0.525 | 盈利与财务 | 1 | -0.03 | 0.51 | -0.01 | DEAD | Specific return for the top 1200 equities in the ATS universe. |
| 8 | `top1200_equity_residualized_return` | MATRIX | 0.525 | 盈利与财务 | 2 | -0.04 | 0.30 | -0.08 | DEAD | Specific return for the top 1200 equities in the selected universe. |
| 9 | `eur_equity_minvol1m_residual_return_crats` | MATRIX | 0.541 | 盈利与财务 | 1 | -0.07 | -0.30 | — | DEAD | Residualized return for EUR equities with minimum 1M volume in the CRATS configuration. |
| 10 | `cfg2_top1200_residual_return` | MATRIX | 1.000 | 价量与波动 | 1 | -0.22 | 0.23 | — | DEAD | Daily matrix of residual (idiosyncratic) stock returns for the EUR TOP1200 universe, in percent units, after neutralizin |
| 11 | `cfg2_top1200_replicator1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | First replicator value for the top 1200 equity universe using configuration 2. |
| 12 | `cfg2_top1200_replicator2` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Second replicator value for the top 1200 equity universe using configuration 2. |
| 13 | `cfg2_top600_replicator1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | First replicator value for the top 600 equity universe using configuration 2. |
| 14 | `cfg2_top600_replicator2` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Second replicator value for the top 600 equity universe using configuration 2. |
| 15 | `cfg2_top800_replicator1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | First replicator value for the top 800 equity universe using configuration 2. |
| 16 | `cfg2_top800_replicator2` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Second replicator value for the top 800 equity universe using configuration 2. |
| 17 | `top2500_equity_residualized_return_nogroup` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Specific return for the top 2500 equities without group-based adjustments. |
| 18 | `rsk72_top800_dsrt` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily reproducible specific returns in % units |
| 19 | `cfg2_top800_residual_return` | MATRIX | 0.713 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily matrix of residual (idiosyncratic) stock returns for the EUR TOP800 universe, in percent units, after neutralizing |
| 20 | `ecs_top1200_residual_return_cfg2` | MATRIX | 0.583 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily reproducible specific returns (idiosyncratic residual returns) for equities in the EQY_ECS_TOP1200 Europe universe |
| 21 | `ecs_top1600_residual_return_cfg2` | MATRIX | 0.583 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily reproducible specific returns (idiosyncratic residual returns) for equities in the EQY_ECS_TOP1600 Europe universe |
| 22 | `ecs_top800_residual_return_cfg2` | MATRIX | 0.578 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily reproducible specific returns (idiosyncratic residual returns) for equities in the EQY_ECS_TOP800 Europe universe |
| 23 | `epp_equity_minvol1m_residual_return` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Residualized return for EPP equities with minimum 1M trading volume. |
| 24 | `epp_equity_minvol1m_residual_return_crats` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Residualized return for EPP equities with minimum 1M volume in the CRATS configuration. |
| 25 | `eur_equity_minvol1m_residual_return` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Residualized return for EUR equities with minimum 1M trading volume. |
| 26 | `rsk72_top600_dsrt` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily reproducible specific returns in % units |
| 27 | `ecs_top1600_equity_residualized_return` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 1600 equities in the ECS universe. |
| 28 | `eur_equity_minvol1m_residual_return_validated` | MATRIX | 0.473 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Residualized return for EUR equities with minimum 1M volume, validated for current day. |
| 29 | `ecs_top1200_equity_residualized_return` | MATRIX | 0.447 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 1200 equities in the ECS universe. |
| 30 | `ats_top800_equity_residualized_return` | MATRIX | 0.339 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 800 equities in the ATS universe. |
| 31 | `top800_equity_residualized_return` | MATRIX | 0.339 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 800 equities in the selected universe. |
| 32 | `top800_equity_residualized_return_nocountry` | MATRIX | 0.339 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 800 equities without country-based adjustments. |
| 33 | `top800_equity_residualized_return_nogroup` | MATRIX | 0.339 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 800 equities without group-based adjustments. |
| 34 | `ecs_top400_residual_return_cfg2` | MATRIX | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily reproducible specific returns (idiosyncratic residual returns) for equities in the EQY_ECS_TOP400 Europe universe |
| 35 | `ecs_top800_equity_residualized_return` | MATRIX | 0.303 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 800 equities in the ECS universe. |
| 36 | `top600_equity_residualized_return` | MATRIX | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 600 equities in the selected universe. |
| 37 | `top600_equity_residualized_return_nocountry` | MATRIX | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 600 equities without country-based adjustments. |
| 38 | `top600_equity_residualized_return_nogroup` | MATRIX | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 600 equities without group-based adjustments. |
| 39 | `top600_reproducible_specific_return` | MATRIX | 0.250 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily reproducible specific (idiosyncratic) returns for the AMR TOP600 universe from the MFM1 risk model with D1 lag, i. |
| 40 | `ecs_top400_equity_residualized_return` | MATRIX | 0.152 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Specific return for the top 400 equities in the ECS universe. |

## 六、本地回测证据

- 本地累计回测 **16** 条；其中 `ra_failed_checks` 为空的 **8** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `2rwlLGNb` | 0.91 | 0.48 | 1.65 | 0.91 | 0.15 | ["LOW_SHARPE | 230 | `divide(abs(subtract(rsk72_top1200_dsrt, cfg2_top800_residual_return)), add(abs(rsk72_top12` |
| `LLN718dn` | 0.51 | 0.19 | 0.72 | 0.53 | 0.15 | ["LOW_SHARPE | 230 | `divide(abs(subtract(rsk72_top1200_dsrt, ecs_top800_residual_return_cfg2)), add(abs(rsk72_t` |
| `rKOjl0Pj` | 0.32 | 0.11 | -0.44 | 0.33 | 0.17 | ["LOW_SHARPE | 230 | `divide(cfg2_top600_residual_return, add(abs(cfg2_top1200_residual_return), 0.0001))` |
| `omLql6jk` | 0.06 | 0.01 | 0.52 | 0.06 | 0.13 | ["LOW_SHARPE | 230 | `divide(subtract(ts_mean(top1200_equity_residualized_return_nogroup, 5), ts_mean(top1200_eq` |
| `levjl8nl` | 0.03 | 0.00 | 0.41 | 0.02 | 0.13 | ["LOW_SHARPE | 230 | `divide(subtract(ts_mean(top1200_equity_residualized_return_nocountry, 5), ts_mean(top1200_` |
| `j23RGEkk` | 0.02 | — | -1.05 | — | — | 0 | 104 | `reverse(rank(ts_delta(top2500_equity_residualized_return, 5)))` |
| `6XrV08LP` | 0.00 | 0.00 | -0.85 | -0.13 | — | 0 | 104 | `add(multiply(rank(ts_mean(top2500_equity_residualized_return_nocountry, 66)), 0.4), multip` |
| `E5plEmGr` | -0.03 | 0.00 | 0.51 | -0.01 | 0.13 | ["LOW_SHARPE | 230 | `divide(subtract(ts_mean(ats_top1200_equity_residualized_return, 5), ts_mean(ats_top1200_eq` |
| `gJQOGANM` | -0.04 | — | -0.53 | — | — | 0 | 104 | `rank(ts_mean(top2500_equity_residualized_return_nocountry, 66))` |
| `qMWrG1RK` | -0.04 | — | 0.30 | — | — | 0 | 104 | `subtract(rank(ts_mean(top1200_equity_residualized_return, 22)), rank(group_sum(ts_mean(top` |
| `A10ZzWXW` | -0.07 | -0.01 | -0.30 | — | — | 0 | 104 | `rank(ts_mean(eur_equity_minvol1m_residual_return_crats, 66))` |
| `j2Aj0V6E` | -0.08 | -0.01 | 0.29 | -0.08 | 0.13 | ["LOW_SHARPE | 230 | `divide(subtract(ts_mean(top1200_equity_residualized_return, 5), ts_mean(top1200_equity_res` |
| `LL9azjve` | -0.22 | — | 0.23 | — | — | 0 | 104 | `subtract(rank(ts_mean(cfg2_top1200_residual_return, 22)), rank(ts_mean(cfg2_top800_residua` |
| `58zlOGk5` | -0.25 | -0.08 | -0.82 | -0.25 | 0.17 | ["LOW_SHARPE | 230 | `divide(cfg2_top600_residual_return, add(abs(ecs_top1200_residual_return_cfg2), 0.0001))` |
| `0mR3glVr` | -0.27 | — | -1.14 | — | — | 0 | 104 | `rank(ts_covariance(ts_delta(ts_backfill(top2500_equity_residualized_return_nocountry, 22),` |

## 七、判死记录（sealed dead_end）

- `EUR-risk72-wave104-all-fail`（2026-09-03）family=risk72 residualized return family：{"alpha_ids": ["6XrV08LP", "zqY6GMnG", "A10ZzWXW", "gJQOGANM", "j23RGEkk", "LL9azjve", "0mR3glVr", "qMWrG1RK"], "avg_sharpe": -0.11, "best_sharpe": 0.02, "dataset": "risk72", "failed_checks": ["LOW_SHARPE", "LOW_FITNESS", "LOW_SUB_UNIVERSE_SHARPE", "LOW_2Y_SHARPE"], "failure_reason": "all_samples_negative_or_zero_sharpe", "mode_b_qualification": "failed (best sharpe=0.02 < 1.25)", "reason": "risk7
- `EUR-RISK72-RESIDUAL-RETURN-WEAK`（2026-09-23T18:17:24）family=risk72 equity_residualized_return 残差族（cfg2/ecs/ats × top1200/top2500 残差价差）：{"family": "risk72 equity_residualized_return 残差族（cfg2/ecs/ats × top1200/top2500 残差价差）", "reason": "wave230 8 探针全灭：best sharpe 0.91 / fitness 0.48，2Y 1.65 但 LOW_ROBUST_UNIVERSE_SHARPE；未达 Mode B 资格线 1.25（D4）→ 判死。2 条 group_cartesian_product/group_count 单位错误被自动隔离。RISK 塔剩余候选：risk68(fields=5 仅条件腿)/risk62(crowded 10665) 均不进白名单。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "s

