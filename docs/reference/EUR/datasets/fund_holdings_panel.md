# fund_holdings_panel — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fund_holdings_panel` |
| 名称 | Global Institutional Fund Holdings |
| 类别 | INSTITUTIONS |
| 数据字段数(平台) | 30 |
| 覆盖率 | 0.8805 |
| 平台已有 alpha | 35 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily, account-level insights into the holdings and transactions of major institutional investors, including mutual funds, ETFs, asset managers, pension funds, and insurance companies. It features detailed tables on daily trades, holdings, and the size of the investment account panel, with metrics such as conviction holdings, boundary trades, significant transactions, and concentration measures. By tracking changes in institutional ownership, trade activity, and portfolio concentration, the dataset enables users to identify shifts in market sentiment, detect accumulation or liquidation trends, and assess the impact of large fund movements on individual securities. These insights are valuable for predicting price movements, understanding liquidity dynamics, and generat

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **30** |
| 类型分布 | VECTOR×30 |
| 平均覆盖率 | **0.880** |
| 覆盖率区间 | 0.84 ~ 0.92 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 15 | 50.0% |
| 中 (0.70–0.90) | 15 | 50.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 21 | 70.0% |
| DEAD | 9 | 30.0% |

- 已实测字段：**9** 个（30%），best_sharpe 最高 **0.42**，中位 0.07

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 16 | 0.89 | holding_value_distribution_score_active、holder_account_total_active、herfindahl_index_holdings |
| 价量与波动 | 6 | 0.89 | large_trade_count_50bps_active、stable_boundary_trade_count_21d_active、herfindahl_index_transactions |
| 其他 | 5 | 0.86 | herfindahl_index_transactions_active、security_transaction_usd_value_active、transaction_account_total_active |
| 风险与质量 | 1 | 0.84 | transaction_value_distribution_score_active |
| 元数据与非信号 | 1 | 0.91 | transaction_account_total |
| 盈利与财务 | 1 | 0.86 | mean_security_weight_active |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `large_trade_count_50bps_active` | VECTOR | 0.843 | 价量与波动 | 2 | 0.42 | 0.63 | — | DEAD | Count of transactions with transaction value greater than 0.5% of the fund’s AUM |
| 2 | `holding_value_distribution_score_active` | VECTOR | 0.857 | 持仓与资金流 | 2 | 0.19 | 1.26 | — | DEAD | Concentration of holdings value across accounts; higher values indicate more crowding among holders |
| 3 | `transaction_value_distribution_score_active` | VECTOR | 0.843 | 风险与质量 | 2 | 0.19 | 0.87 | — | DEAD | Concentration index (0 to 1) measuring how the transaction value is distributed across transacting accounts |
| 4 | `herfindahl_index_transactions_active` | VECTOR | 0.843 | 其他 | 1 | 0.14 | -0.32 | — | DEAD | Herfindahl-Hirschman Index concentration measure based on distribution of transaction value across accounts |
| 5 | `holder_account_total_active` | VECTOR | 0.857 | 持仓与资金流 | 2 | 0.07 | -0.64 | — | DEAD | Number of distinct accounts holding this ISIN on the date |
| 6 | `stable_boundary_trade_count_21d_active` | VECTOR | 0.843 | 价量与波动 | 1 | 0.06 | -0.43 | — | DEAD | Count of boundary transactions from fund accounts with no prior boundary transaction in the past 21 weekdays for the sec |
| 7 | `security_transaction_usd_value_active` | VECTOR | 0.843 | 其他 | 1 | 0.02 | 0.34 | — | DEAD | Dollar value of transactions in USD |
| 8 | `transaction_account_total_active` | VECTOR | 0.843 | 其他 | 2 | 0.01 | 0.77 | — | DEAD | Number of accounts that transacted the security |
| 9 | `boundary_transaction_usd_value_active` | VECTOR | 0.843 | 其他 | 1 | -0.21 | -0.55 | — | DEAD | Dollar value of boundary transactions in USD |
| 10 | `herfindahl_index_holdings` | VECTOR | 0.918 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Herfindahl-Hirschman Index of holdings concentration based on account weights |
| 11 | `holder_account_total` | VECTOR | 0.918 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of distinct investment accounts or funds holding the ISIN on the date |
| 12 | `holding_value_distribution_score` | VECTOR | 0.918 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Concentration of holdings value across accounts, a custom crowding metric |
| 13 | `mean_security_weight` | VECTOR | 0.918 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Average portfolio weight of the security across only the accounts that hold it, measured as a share of each fund’s AUM ( |
| 14 | `security_holding_usd_value` | VECTOR | 0.918 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total USD value of shares held in the ISIN across all accounts |
| 15 | `top_weighted_account_number` | VECTOR | 0.918 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of accounts for which the ISIN is a conviction holding (top 30% by portfolio weight) |
| 16 | `boundary_transaction_total` | VECTOR | 0.908 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of boundary transactions (new position initiations or complete liquidations) across all fund accounts on the date |
| 17 | `boundary_transaction_usd_value` | VECTOR | 0.908 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total USD value of boundary transactions (entries into new positions or complete liquidations) across all accounts on th |
| 18 | `herfindahl_index_transactions` | VECTOR | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Herfindahl-Hirschman Index of trade value concentration across transacting accounts (0 to 1, higher means more concentra |
| 19 | `large_trade_count_50bps` | VECTOR | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of transactions where the trade value exceeds 0.5% of the respective fund’s AUM |
| 20 | `security_transaction_usd_value` | VECTOR | 0.908 | 其他 | 0 | — | — | — | UNTESTED | Dollar value of transactions in USD |
| 21 | `stable_boundary_trade_count_21d` | VECTOR | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Count of boundary transactions by accounts that had no boundary trade in the same security in the prior 21 weekdays (ind |
| 22 | `top_weighted_transaction_number` | VECTOR | 0.908 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of transactions in securities that were conviction holdings as of the prior or current day across all accounts |
| 23 | `transaction_account_total` | VECTOR | 0.908 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of distinct accounts that transacted the security on the date |
| 24 | `transaction_value_distribution_score` | VECTOR | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Index from 0 to 1 measuring how the day’s trade value is distributed across transacting accounts (higher means more conc |
| 25 | `herfindahl_index_holdings_active` | VECTOR | 0.857 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Herfindahl-Hirschman Index of holdings weights across accounts (0 to 1) |
| 26 | `mean_security_weight_active` | VECTOR | 0.857 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average portfolio weight of this ISIN across accounts that hold it, as a share of each account’s assets |
| 27 | `security_holding_usd_value_active` | VECTOR | 0.857 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total dollar value in USD of shares held in this ISIN |
| 28 | `top_weighted_account_number_active` | VECTOR | 0.857 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of fund accounts for which the security is a conviction holding (within the top 30% of AUM by weight) |
| 29 | `boundary_transaction_total_active` | VECTOR | 0.843 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of boundary transactions across fund accounts (introductions of new positions or complete liquidations) |
| 30 | `top_weighted_transaction_number_active` | VECTOR | 0.843 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of conviction transactions across fund accounts, where a conviction transaction is one in a security that was par |

## 六、本地回测证据

- 本地累计回测 **14** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `E5vpjORL` | 0.42 | 0.12 | 0.63 | — | 0.22 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(divide(vec_sum(large_trade_count_50bps_active), vec_sum(holder_account_total_active))` |
| `j23ApzeO` | 0.40 | 0.11 | 0.63 | — | 0.22 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(divide(vec_sum(large_trade_count_50bps_active), vec_sum(transaction_account_total_act` |
| `XgWb3ma0` | 0.19 | 0.05 | 0.90 | — | 0.14 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(multiply(-1, subtract(vec_avg(holding_value_distribution_score_active), vec_avg(trans` |
| `xAY3LOln` | 0.19 | 0.05 | 0.87 | — | 0.15 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(multiply(-1, subtract(vec_avg(transaction_value_distribution_score_active), vec_avg(t` |
| `MP1aEWPr` | 0.14 | 0.02 | -0.32 | — | 0.19 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(subtract(vec_avg(herfindahl_index_transactions_active), vec_avg(herfindahl_index_hold` |
| `RRVbOjed` | 0.08 | 0.01 | 1.26 | — | 0.01 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `winsorize(rank(multiply(-1, subtract(vec_avg(holding_value_distribution_score_active), vec` |
| `xAY3L6ON` | 0.07 | 0.01 | -0.64 | — | 0.09 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(ts_zscore(ts_delta(vec_sum(holder_account_total_active), 22), 252))` |
| `blRbmkGp` | 0.06 | 0.01 | -0.43 | — | 0.22 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(ts_zscore(divide(vec_sum(stable_boundary_trade_count_21d_active), add(vec_sum(boundar` |
| `pwPR2Yxq` | 0.04 | 0.00 | -0.77 | — | 0.17 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `ts_zscore(multiply(-1, subtract(vec_avg(transaction_value_distribution_score_active), vec_` |
| `O0rNLY07` | 0.02 | 0.00 | 0.34 | — | 0.27 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(reverse(ts_zscore(divide(vec_sum(security_transaction_usd_value_active), add(vec_sum(` |
| `78ZN57L5` | 0.01 | 0.00 | 0.77 | — | 0.15 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `group_rank(group_zscore(ts_av_diff(vec_avg(transaction_account_total_active), 22), bucket(` |
| `Vk6ar1xY` | -0.11 | -0.02 | -0.66 | — | 0.11 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(group_zscore(ts_av_diff(vec_avg(holder_account_total_active), 22), bucket(rank(vec_av` |
| `akLb0Yr5` | -0.21 | -0.03 | -0.55 | — | 0.22 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(reverse(ts_zscore(divide(vec_sum(boundary_transaction_usd_value_active), add(vec_sum(` |
| `P0Z2RWQK` | -0.30 | -0.05 | -0.91 | — | 0.27 | ["LOW_SHARPE | s2_fund_holdings_panel_d1 | `rank(ts_zscore(ts_delta(vec_sum(transaction_account_total_active), 22), 252))` |

## 七、判死记录（sealed dead_end）

- `EUR-FHP-INSTITUTIONS-WEAK`（None）family=None：{"dataset": "fund_holdings_panel", "evidence": "wave136 3 条全灭：Sharpe -0.39~0.40 远低于 1.58。机构持仓数据在 EUR D1 信号弱。institutions 塔唯一可用数据集判死。", "reason": "fund_holdings_panel 机构持仓在 EUR D1 判死：信号弱", "region": "EUR", "rule": "Leave fund_holdings_panel 在 EUR。institutions 塔在 EUR D1 无可挖数据集。", "wave": 136}
- `EUR-INST6-INSTITUTIONS-TOWER-EXHAUSTED`（None）family=institutions6 机构持股聚合（净流向/存量/动量三机制）：{"dataset": "institutions6", "evidence": {"d5ORZ8NX": "持股存量水平：S0.09/F0.02/TVR0.014/returns0.0052/longCount1417", "kqVZPRJK": "净买家数：S0.18/F0.05/TVR0.038/returns0.0089/longCount1326/2Y-1.71", "xAYdNXjW": "买入金额动量：S0.30/F0.07/TVR0.086/returns0.0065/longCount1350"}, "math_proof": "Fitness_upper = Sharpe_max * sqrt(returns_max/0.125) = 0.30*sqrt(0.0089/0.125) = 0.080；即使 Sharpe 达 1.58 也仅 0.42，要 Fitness>=

