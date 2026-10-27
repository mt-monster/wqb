# risk60 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `risk60` |
| 名称 | Securities Lending Insight Data |
| 类别 | RISK |
| 数据字段数(平台) | 5 |
| 覆盖率 | 0.8168 |
| 平台已有 alpha | 662 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.0 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RIC) and Bloomberg Identifiers (BBID) for global securities. It enables seamless integration and reconciliation of security data across different financial platforms and data sources. By facilitating accurate cross-referencing, the dataset supports portfolio management, trade processing, and data aggregation tasks. While not directly predictive of price movements, it is essential for ensuring data integrity and consistency when combining datasets for quantitative research, risk analysis, and multi-source analytics.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **5** |
| 类型分布 | VECTOR×5 |
| 平均覆盖率 | **0.817** |
| 覆盖率区间 | 0.82 ~ 0.82 |
| 更新频率（推断） | 低频（季/年） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 5 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| DEAD | 2 | 40.0% |
| UNTESTED | 2 | 40.0% |
| WEAK | 1 | 20.0% |

- 已实测字段：**3** 个（60%），best_sharpe 最高 **1.36**，中位 1.08

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 2 | 0.82 | rsk60_offer、rsk60_last |
| 风险与质量 | 1 | 0.82 | rsk60_crowding |
| 价量与波动 | 1 | 0.82 | lending_fee_bid_rate |
| 交易与微观结构 | 1 | 0.82 | rsk60_datatime |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `rsk60_offer` | VECTOR | 0.817 | 持仓与资金流 | 13 | 1.36 | 2.77 | 0.97 | WEAK | Composite borrow fee (annualized) paid by the short seller |
| 2 | `rsk60_last` | VECTOR | 0.817 | 持仓与资金流 | 1 | 1.08 | 1.60 | 0.75 | DEAD | Most recent borrow/lend rate observed at the snapshot time |
| 3 | `rsk60_crowding` | VECTOR | 0.817 | 风险与质量 | 2 | 0.47 | 0.67 | 0.25 | DEAD | Signed daily indicator of shorting activity (positive = increased shorting/crowding, negative = covering/decrowding) |
| 4 | `lending_fee_bid_rate` | VECTOR | 0.817 | 价量与波动 | 0 | — | — | — | UNTESTED | Composite lending fee (annualized) at which long inventory is lent |
| 5 | `rsk60_datatime` | VECTOR | 0.817 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Vendor timestamp in HHMMSS for the snapshot, used to order intraday prints |

## 六、本地回测证据

- 本地累计回测 **16** 条；其中 `ra_failed_checks` 为空的 **11** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `58z71A7k` | 1.36 | 1.12 | 2.77 | 0.90 | 0.03 | 0 | 207 | `multiply(-1, winsorize(ts_mean(vec_avg(rsk60_offer), 5), std=4))` |
| `P02rbYqp` | 1.21 | 0.83 | 2.23 | 0.97 | 0.03 | 0 | 207 | `multiply(-1, quantile(ts_mean(vec_avg(rsk60_offer), 5)))` |
| `O0NwjMqv` | 1.16 | 0.80 | 2.17 | 0.97 | 0.03 | 0 | 207 | `multiply(-1, signed_power(subtract(rank(ts_mean(vec_avg(rsk60_offer), 5)), 0.5), 2))` |
| `zq8wE2wV` | 1.15 | 0.71 | 1.93 | 0.93 | 0.03 | 0 | 207 | `group_rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 5)), country)` |
| `LLNbwepn` | 1.13 | 0.73 | 2.03 | 0.97 | 0.04 | 0 | 206 | `rank(multiply(-1, ts_mean(subtract(vec_avg(rsk60_offer), vec_avg(lending_fee_bid_rate)), 5` |
| `RRbZoXrn` | 1.12 | 0.71 | 2.06 | 0.93 | 0.03 | 0 | 206 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 5)))` |
| `kqokMWk8` | 1.12 | 0.74 | 2.48 | 0.83 | 0.03 | 0 | 207 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 4)))` |
| `pwRJkMox` | 1.12 | 0.70 | 1.90 | 0.92 | 0.03 | 0 | 207 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 22)))` |
| `wpZwA6lp` | 1.09 | 0.63 | 2.04 | 0.86 | 0.03 | 0 | 206 | `group_rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 5)), subindustry)` |
| `zq8wE2QV` | 1.08 | 0.66 | 1.60 | 0.75 | 0.04 | 0 | 207 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_last), 5)))` |
| `E5p0M3Er` | 1.01 | 0.59 | 1.79 | 0.87 | 0.02 | 0 | 206 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 66)))` |
| `P02rbepx` | 0.87 | 0.42 | 1.47 | 0.56 | 0.05 | ["LOW_SHARPE | 206 | `rank(multiply(-1, ts_zscore(ts_backfill(vec_avg(rsk60_offer), 5), 252)))` |
| `omLwXJvv` | 0.75 | 0.39 | 1.18 | 0.47 | 0.04 | ["LOW_SHARPE | 207 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_offer), 6)))` |
| `WjbwRkgo` | 0.63 | 0.24 | 1.60 | 0.42 | 0.07 | ["LOW_SHARPE | 206 | `rank(multiply(-1, ts_delta(ts_mean(vec_avg(rsk60_offer), 5), 22)))` |
| `wpZwA6Rp` | 0.47 | 0.17 | 0.67 | 0.25 | 0.10 | ["LOW_SHARPE | 206 | `rank(multiply(-1, ts_mean(vec_avg(rsk60_crowding), 5)))` |

## 七、判死记录（sealed dead_end）

- `EUR-RISK60-BORROW-FEE-PROD-WALL`（2026-09-19）family=risk60 securities lending borrow fee level (rsk60_offer / rsk60_last / bid-offer spread)：{"id": "EUR-RISK60-BORROW-FEE-PROD-WALL", "dataset": "risk60", "waves": [206, 207], "universe": "TOPCS1600", "signal": "-borrow fee (short constraint), 5d mean; variants: raw winsorized, quantile, signed_power, country group_rank, COUNTRY neut, 22d, rsk60_last, TOP2500", "is_metrics": "best 58z71A7k multiply(-1, winsorize(ts_mean(vec_avg(rsk60_offer),5),std=4)) S1.36 F1.12 tvr0.026 2Y2.77 sub0.90;

