# insider_trx_matrix — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `insider_trx_matrix` |
| 名称 | Global Insider Transaction Aggregates |
| 类别 | OTHER |
| 数据字段数(平台) | 33 |
| 覆盖率 | 0.6109 |
| 平台已有 alpha | 42 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a structured matrix of aggregated insider transaction data across global markets, utilizing advanced filtering and smart aggregation techniques. It captures detailed information on insider trades, including buy and sell activity, transaction types, insider roles, and trade significance, organized by region and time delay. By consolidating and summarizing insider trading patterns, the dataset enables researchers and investors to identify potential signals of future price movements, such as cluster buying or selling by key executives. The aggregation and enhancement of raw insider data into a matrix format make it easier to analyze trends, detect anomalies, and generate predictive signals for alpha generation, supporting both event-driven and quantitative investment str

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **33** |
| 类型分布 | MATRIX×33 |
| 平均覆盖率 | **0.611** |
| 覆盖率区间 | 0.61 ~ 0.61 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 33 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 25 | 75.8% |
| DEAD | 6 | 18.2% |
| DEAD_STATIC | 2 | 6.1% |

- 已实测字段：**8** 个（24%），best_sharpe 最高 **1.40**，中位 0.74

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 16 | 0.61 | total_buy_transaction_count、total_top_buy_transaction_count、mean_buy_transaction_count |
| 价量与波动 | 16 | 0.61 | usd_direct_signal_value_2、usd_top_primary_signal_value、usd_direct_signal_value_1 |
| 风险与质量 | 1 | 0.61 | directional_indicator_score |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `total_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 2 | 1.40 | -0.39 | 0.28 | DEAD_STATIC | Sum of insider buy activity across all purchase events for the stock on D0 in the base OGE module (proprietary intensity |
| 2 | `total_top_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 6 | 0.79 | 0.94 | 0.62 | DEAD | Sum of high-confidence (“Top”) insider buy activity on D0 |
| 3 | `mean_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 1 | 0.75 | 0.42 | 0.60 | DEAD | Average per event of insider buy activity across all purchase events on D0 in the base OGE module |
| 4 | `mean_top_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 2 | 0.74 | 0.21 | 0.58 | DEAD | Average per event of high-confidence (“Top”) insider buy activity on D0 |
| 5 | `usd_direct_signal_value_2` | MATRIX | 0.615 | 价量与波动 | 2 | 0.42 | 0.41 | -0.08 | DEAD | Sum USD value of shares bought directly by directors with significant trades |
| 6 | `usd_top_primary_signal_value` | MATRIX | 0.615 | 价量与波动 | 1 | 0.39 | 0.54 | 0.13 | DEAD | Mean USD value of shares bought by executives with significant trades |
| 7 | `directional_indicator_score` | MATRIX | 0.607 | 风险与质量 | 1 | -0.32 | 0.65 | -0.37 | DEAD | Score indicating the net direction of aggregated transactions. |
| 8 | `total_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 1 | -0.38 | -0.44 | -0.49 | DEAD_STATIC | Sum of insider sell activity across all sale events for the stock on D0 in the base OGE module (proprietary intensity un |
| 9 | `usd_direct_signal_value_1` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares bought directly by directors with significant trades |
| 10 | `usd_direct_signal_value_3` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares sold directly by directors with significant trades |
| 11 | `usd_direct_signal_value_4` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares sold directly by directors with significant trades |
| 12 | `usd_primary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares bought by directors with significant trades |
| 13 | `usd_quaternary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares sold by directors with significant trades |
| 14 | `usd_secondary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares bought by directors with significant trades |
| 15 | `usd_tertiary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares sold by directors with significant trades |
| 16 | `usd_top_direct_signal_value_1` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares bought directly by executives with significant trades |
| 17 | `usd_top_direct_signal_value_2` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares bought directly by executives with significant trades |
| 18 | `usd_top_direct_signal_value_3` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares sold directly by executives with significant trades |
| 19 | `usd_top_direct_signal_value_4` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares sold directly by executives with significant trades |
| 20 | `usd_top_quaternary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares sold by executives with significant trades |
| 21 | `usd_top_secondary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum USD value of shares bought by executives with significant trades |
| 22 | `usd_top_tertiary_signal_value` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean USD value of shares sold by executives with significant trades |
| 23 | `mean_secondary_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average per event of insider buy activity using aggregation recipe 2 on D0 |
| 24 | `mean_secondary_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average per event of insider sell activity using aggregation recipe 2 on D0 |
| 25 | `mean_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average per event of insider sell activity across all sale events on D0 in the base OGE module |
| 26 | `mean_top_secondary_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average per event of high-confidence (“Top”) insider buy activity using aggregation recipe 2 on D0 |
| 27 | `mean_top_secondary_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average per event of high-confidence (“Top”) insider sell activity using the alternative aggregation recipe 2 on D0 |
| 28 | `mean_top_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average per event of high-confidence (“Top”) insider sell activity on D0 |
| 29 | `total_secondary_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Sum of insider buy activity across all events using aggregation recipe 2 on D0 |
| 30 | `total_secondary_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Sum of insider sell activity across all events using aggregation recipe 2 on D0 |
| 31 | `total_top_secondary_buy_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Sum of high-confidence (“Top”) insider buy activity using aggregation recipe 2 on D0 |
| 32 | `total_top_secondary_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Sum of high-confidence (“Top”) insider sell activity using aggregation recipe 2 on D0 |
| 33 | `total_top_sell_transaction_count` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Sum of high-confidence (“Top”) insider sell activity on D0 |

## 六、本地回测证据

- 本地累计回测 **15** 条；其中 `ra_failed_checks` 为空的 **15** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `3q9r2R1Z` | 0.79 | 0.32 | 0.48 | 0.62 | 0.04 | 0 | 105 | `add(multiply(rank(ts_sum(total_top_buy_transaction_count, 22)), 0.5), multiply(rank(ts_sum` |
| `om65klJk` | 0.77 | 0.30 | 0.24 | 0.59 | 0.03 | 0 | 105 | `rank(ts_sum(total_top_buy_transaction_count, 66))` |
| `88392QJz` | 0.77 | 0.31 | 0.24 | 0.59 | 0.03 | 0 | 105 | `subtract(rank(ts_sum(total_top_buy_transaction_count, 66)), rank(group_sum(ts_sum(total_to` |
| `d5OVr9wj` | 0.75 | 0.30 | 0.42 | 0.60 | 0.04 | 0 | 106 | `add(multiply(0.6, rank(ts_sum(mean_buy_transaction_count, 66))), multiply(0.4, rank(ts_sum` |
| `wpYxkNgd` | 0.74 | 0.29 | 0.21 | 0.58 | 0.03 | 0 | 106 | `rank(ts_sum(mean_top_buy_transaction_count, 66))` |
| `9qV12rdq` | 0.53 | 0.19 | 0.94 | 0.36 | 0.15 | 0 | 105 | `rank(ts_delta(ts_sum(total_top_buy_transaction_count, 66), 5))` |
| `1YxbAGEJ` | 0.43 | 0.14 | -0.08 | 0.24 | 0.04 | 0 | 106 | `subtract(rank(ts_sum(total_top_buy_transaction_count, 66)), rank(ts_sum(total_top_sell_tra` |
| `LL9a21ze` | 0.42 | 0.12 | 0.41 | -0.08 | 0.03 | 0 | 105 | `subtract(rank(ts_sum(ts_backfill(usd_direct_signal_value_2, 66), 66)), rank(ts_sum(ts_back` |
| `XgWQOnv8` | 0.39 | 0.11 | 0.54 | 0.13 | 0.03 | 0 | 105 | `rank(ts_mean(ts_backfill(usd_top_primary_signal_value, 22), 66))` |
| `58Q0dGWJ` | 0.31 | 0.07 | -0.39 | 0.28 | 0.02 | 0 | 106 | `trade_when(ts_sum(total_buy_transaction_count, 22) > 0, rank(ts_sum(total_top_buy_transact` |
| `d5OVr9wg` | 0.19 | 0.04 | 0.46 | 0.41 | 0.11 | 0 | 106 | `rank(ts_delta(ts_sum(total_top_buy_transaction_count, 126), 10))` |
| `npKRX2md` | 0.05 | 0.01 | -0.45 | -0.08 | 0.07 | 0 | 105 | `rank(ts_covariance(ts_delta(ts_backfill(usd_direct_signal_value_2, 22), 5), ts_delta(ts_ba` |
| `qMWrJ5Z1` | -0.32 | -0.08 | 0.65 | -0.37 | 0.08 | 0 | 106 | `rank(ts_mean(directional_indicator_score, 66))` |
| `0mR32GW1` | -0.38 | -0.10 | -0.44 | -0.49 | 0.03 | 0 | 106 | `trade_when(ts_sum(total_sell_transaction_count, 22) > 0, rank(ts_max_diff(ts_sum(total_top` |
| `3q9rvGWP` | -0.43 | -0.13 | -0.09 | -0.34 | 0.04 | 0 | 106 | `rank(ts_max_diff(ts_sum(mean_top_buy_transaction_count, 22), 66))` |

## 七、判死记录（sealed dead_end）

- `EUR-risk72-wave104-all-fail`（2026-09-03）family=risk72 residualized return family：{"alpha_ids": ["6XrV08LP", "zqY6GMnG", "A10ZzWXW", "gJQOGANM", "j23RGEkk", "LL9azjve", "0mR3glVr", "qMWrG1RK"], "avg_sharpe": -0.11, "best_sharpe": 0.02, "dataset": "risk72", "failed_checks": ["LOW_SHARPE", "LOW_FITNESS", "LOW_SUB_UNIVERSE_SHARPE", "LOW_2Y_SHARPE"], "failure_reason": "all_samples_negative_or_zero_sharpe", "mode_b_qualification": "failed (best sharpe=0.02 < 1.25)", "reason": "risk7
- `EUR-insider_trx_matrix-WEAK-DRIFT`（2026-09-03）family=insider：{"category": "Other", "dataset": "insider_trx_matrix", "evidence": "wave105 7/7 + wave106 8/8 全 FAIL；最佳 Sharpe 0.75-0.79 但 2Y 全崩 <0.5、RNS 1.56-1.62 依赖单骨架", "pattern": "buy 漂移方向稳（S~0.75-0.8 方向对但强度不足）；ts_delta/ts_max_diff 加速脉冲全负或弱（事件突增=已反应/反转）；sell/directional/usd 变体无增益；事件稀疏 long 818-1525 vs short 778-2035 极端不对称", "preprocessing_note": "count 字段点质量集中 0 需 ts_sum/trade_when；usd 先 rank 消规模；无事件日 0/NA 混合
- `EUR-ai_news_scores-ADVANCED-NEG`（2026-09-03）family=ai_news_scores advanced stats：{"category": "Other", "dataset": "ai_news_scores", "evidence": "wave108 首探 8/8 FAIL；CI 带宽精度 -0.34、恐慌尖峰反转 -0.37(CW 0.356 集中)、共识漂移 -0.54(2Y -2.63) 3/3 全负；ts_max_diff×median 契约双槽 +0.02/-0.68；neg 方向族 IS 全负（B 槽 trade_when 2Y+1.00 例外）", "not_dead": "pos 水平×强度加权 JjxZjGwE(0.6×ts_mean avg66 + 0.4×ts_mean max5) IS+0.27/2Y+0.72/subU+0.31/TVR 0.059 唯一全维正，已 salvage → 与 wave107 xAY8ZlJN(2Y 0.83) 形成跨数据集复现线索：pos 
- `EUR-INSIDER-AGG-MATRIX-COLD-ZERO-YIELD`（2026-09-22）family=内部人买入股数比例与二级买入广度：{"dataset": "insider_agg_matrix", "evidence": {"alpha_count": 114, "best_abs_sharpe": 0.53, "best_positive_sharpe": 0.3}, "failure_mode": "LOW_SHARPE / LOW_FITNESS / LOW_ROBUST_UNIVERSE_SHARPE / LOW_2Y_SHARPE + 多数 CONCENTRATED_WEIGHT", "mechanism": "内部人买入股数比例与二级买入广度（avg_secondary_top_buy_shares / total_top_buy_shares，126 长窗）", "rule": "命中 EUR profile fast_kill（新集 8 探针无 /S/>=0.5）；INSIDERS 塔另一集 insi

