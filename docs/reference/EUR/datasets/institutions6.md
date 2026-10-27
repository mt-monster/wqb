# institutions6 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `institutions6` |
| 名称 | Institutions and Beneficial Stake Ownership |
| 类别 | INSTITUTIONS |
| 数据字段数(平台) | 11 |
| 覆盖率 | 0.9915 |
| 平台已有 alpha | 94 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive information on global equity ownership by institutions, mutual funds, and beneficial stakeholders. It includes current and historical holdings data from over 50,000 portfolios and companies across 70 countries, with more than 10 years of history. Key fields cover shares held, percent of shares outstanding, report dates, aggregated statistics, and investor profiles. The dataset enables analysis of institutional buying and selling activity, ownership concentration, and changes in major holders, which are critical for understanding market sentiment, liquidity, and potential price movements. By tracking shifts in institutional positions and identifying new or reduced stakes, investors and researchers can anticipate trends, detect accumulation or distribution

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **11** |
| 类型分布 | MATRIX×11 |
| 平均覆盖率 | **0.991** |
| 覆盖率区间 | 0.93 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 11 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 6 | 54.5% |
| DEAD_STATIC | 3 | 27.3% |
| DEAD | 2 | 18.2% |

- 已实测字段：**5** 个（45%），best_sharpe 最高 **0.45**，中位 0.32

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 8 | 0.99 | quantity_institutional_shares_acquired、count_institutional_buyers_security、aggregate_share_count_institutions |
| 盈利与财务 | 2 | 1.00 | aggregate_equity_value_all_owners、aggregate_equity_value_institutions |
| 其他 | 1 | 1.00 | aggregate_share_count_all_owners |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `quantity_institutional_shares_acquired` | MATRIX | 0.998 | 持仓与资金流 | 3 | 0.45 | 0.76 | 0.13 | DEAD | Total number of shares of the security purchased by institutional investors during the reporting period |
| 2 | `aggregate_equity_value_all_owners` | MATRIX | 0.998 | 盈利与财务 | 2 | 0.36 | 0.37 | 0.37 | DEAD_STATIC | Aggregate dollar value of shares of the security held by all owners, with duplication between child and parent owners re |
| 3 | `aggregate_equity_value_institutions` | MATRIX | 0.998 | 盈利与财务 | 2 | 0.32 | 0.47 | 0.29 | DEAD_STATIC | Aggregate dollar value of shares of the security currently held by all institutional investors at the reporting date |
| 4 | `aggregate_share_count_all_owners` | MATRIX | 0.998 | 其他 | 2 | 0.00 | 0.09 | -0.11 | DEAD | Aggregate number of shares of the security held by all owners, with duplication between child and parent owners removed |
| 5 | `count_institutional_buyers_security` | MATRIX | 0.998 | 持仓与资金流 | 2 | -0.67 | 0.19 | -0.74 | DEAD_STATIC | Number of institutional investors who purchased shares of the security during the reporting period |
| 6 | `aggregate_share_count_institutions` | MATRIX | 0.998 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total number of shares of the security currently held by all institutional investors at the reporting date |
| 7 | `count_institutional_holders_security` | MATRIX | 0.998 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of institutional investors currently holding shares (with holdings greater than zero) for the security at the rep |
| 8 | `count_institutional_sellers_security` | MATRIX | 0.998 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of institutional investors who sold shares of the security during the reporting period |
| 9 | `market_value_institutional_shares_acquired` | MATRIX | 0.998 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Aggregate dollar value of shares of the security purchased by institutional investors during the reporting period |
| 10 | `quantity_institutional_shares_disposed` | MATRIX | 0.997 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total number of shares of the security sold by institutional investors during the reporting period |
| 11 | `market_value_institutional_shares_disposed` | MATRIX | 0.931 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Aggregate dollar value of shares of the security sold by institutional investors during the reporting period |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `MPaQJqbn` | 0.45 | 0.28 | 0.58 | 0.10 | 0.06 | ["LOW_SHARPE | 216 | `divide(subtract(ts_backfill(quantity_institutional_shares_acquired,66), ts_backfill(quanti` |
| `d5b0NgnE` | 0.36 | 0.17 | 0.37 | 0.30 | 0.01 | ["LOW_SHARPE | 216 | `divide(aggregate_equity_value_all_owners, aggregate_share_count_all_owners)` |
| `KPN9Wqng` | 0.32 | 0.10 | 0.47 | 0.29 | 0.01 | ["LOW_SHARPE | 216 | `divide(aggregate_equity_value_institutions, aggregate_equity_value_all_owners)` |
| `xA3kJ9Pg` | 0.19 | 0.05 | 1.44 | 0.15 | 0.01 | ["LOW_SHARPE | 216 | `days_from_last_change(sign(subtract(market_value_institutional_shares_acquired, market_val` |
| `WjbGvnaG` | 0.19 | 0.05 | 1.44 | 0.15 | 0.01 | ["LOW_SHARPE | 216 | `days_from_last_change(sign(subtract(market_value_institutional_shares_acquired, quantity_i` |
| `pwRl9o1x` | -0.30 | -0.16 | -0.64 | -0.11 | 0.18 | ["LOW_SHARPE | 216 | `group_count(aggregate_share_count_all_owners, sector)` |
| `wpZl0On2` | -0.67 | -0.35 | 0.19 | -0.75 | 0.02 | ["LOW_SHARPE | 216 | `divide(add(count_institutional_buyers_security, count_institutional_sellers_security), add` |
| `E5pE9Yq1` | -0.73 | -0.39 | 0.12 | -0.74 | 0.03 | ["LOW_SHARPE | 216 | `divide(add(count_institutional_buyers_security, count_institutional_sellers_security), cou` |

## 七、判死记录（sealed dead_end）

- `EUR-INST6-INSTITUTIONS-TOWER-EXHAUSTED`（None）family=institutions6 机构持股聚合（净流向/存量/动量三机制）：{"dataset": "institutions6", "evidence": {"d5ORZ8NX": "持股存量水平：S0.09/F0.02/TVR0.014/returns0.0052/longCount1417", "kqVZPRJK": "净买家数：S0.18/F0.05/TVR0.038/returns0.0089/longCount1326/2Y-1.71", "xAYdNXjW": "买入金额动量：S0.30/F0.07/TVR0.086/returns0.0065/longCount1350"}, "math_proof": "Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.30*sqrt(0.0089/0.125) = 0.080；即使 Sharpe 达 1.58 也仅 0.42，要 Fitness>=
- `EUR-INSTITUTIONS6-COLD-ZERO-YIELD`（2026-09-22）family=机构持有人广度比例 / 机构权益占比 / 买入-卖出股数差：{"dataset": "institutions6", "evidence": {"alpha_count": 71, "best_abs_sharpe": 0.45, "best_fitness": 0.28, "coverage": 0.9915}, "failure_mode": "LOW_SHARPE / LOW_FITNESS / LOW_2Y_SHARPE / LOW_ROBUST_UNIVERSE_SHARPE (+ CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE)", "mechanism": "机构持有人广度比例（buyers+sellers/holders）、机构权益占比、买入-卖出股数差经 ts_corr 标准化", "note": "另命中平台 UNITS：subtract(market_value_*, quantity_*) 金额

