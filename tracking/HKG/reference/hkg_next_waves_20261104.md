# HKG 待派发波次（2026-11-04，已预检通过，可直接 create_multi_simulation）

> 阻塞原因：W17 / W18 两个 multisim 卡在 progress 0.15、无子仿真，占满 2 个并发槽（再派发返回 429 CONCURRENT_SIMULATION_LIMIT_EXCEEDED）。
> 槽位释放后按下面顺序发，最多 2 批并行。所有表达式均已 `preflight_expressions` 通过（valid=true, unknown_fields=[]）。

## 提交状态（未提交任何一颗）

PV 塔三件套已在 self 闸上完全安全：4 颗候选与 4 颗历史已提交 alpha **两两全部 < 0.5**（唯一 > 0.5 的一对是历史自身 `gJZ6pONl~E5R1AA39` 0.6112）。

| 顺位 | alpha | S | F | 2Y | sub | self | prod | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `2rAlGNk6` | 1.97 | 2.18 | 2.10 | 2.05 | 0.137 | **0.5245** | 可提交 |
| 2 | `RRE7vM2e` | 1.80 | 1.50 | 1.74 | 1.24 | 0.192 | **0.6172** | 可提交 |
| 3 | `MPY18MVr` | 2.34 | 2.50 | 2.30 | 2.28 | <0.5 | 待测 | 卡 prod 槽 |
| 3' | `qMLjw8nA` | 2.34 | 2.29 | 1.96 | 1.91 | <0.5 | 待测 | 卡 prod 槽 |

三颗齐发即点亮 HKG/D1/PV（本季 0/3）。

## W19：PV × ANALYST（双塔，压缩版，10 条）

目的：ANALYST 单独天花板 1.30，借 PV 抬过 1.58；成功后同时计入 PV + ANALYST 两塔。
压缩手法：用 `ts_zscore(·,126)` 替代 `divide(ts_mean(·,126), ts_std_dev(·,126))`，把单表达式从 ~700 字符压到 ≤258，规避长表达式导致的初始化挂起。

```
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252)))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_high_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252)))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_vwap_return_60m_post_open, mean_vwap_return_60m_pre_close_2), 126), industry)), rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252)))), sector)
trade_when(greater(rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252))), 0.5), reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), -1)
trade_when(greater(rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252))), 0.7), group_zscore(ts_zscore(subtract(mean_vwap_return_60m_post_open, mean_vwap_return_60m_pre_close_2), 126), industry), -1)
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), rank(ts_delta(anl39_epschngin, 22))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_high_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), rank(divide(ts_mean(anl39_epschngin, 66), ts_std_dev(anl39_epschngin, 252)))), sector)
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), signed_power(rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252))), 0.5)), sector)
trade_when(greater(rank(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252))), 0.3), group_zscore(ts_zscore(subtract(mean_high_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry), -1)
group_rank(multiply(ts_zscore(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), 252), ts_zscore(divide(anl39_epschngin, ts_std_dev(anl39_epschngin, 252)), 252)), sector)
```

## W20：PV × SHORTINTEREST（双塔，10 条）

目的：历史 HKG 的 `PV+SHORTINTEREST` 曾达 S 1.72（`gJQZOXrg`/`WjPPjVQd`）；SHORTINTEREST 单塔本季 0/3。
融券腿用 `loan_utilization_ratio`（cov 0.9302）/ `mean_loan_rate_main` / `borrow_activity_score`。

```
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), rank(group_rank(ts_mean(loan_utilization_ratio, 66), sector))), sector)
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), rank(group_rank(ts_mean(mean_loan_rate_main, 66), sector))), sector)
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), rank(group_rank(ts_mean(borrow_activity_score, 66), sector))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_high_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), rank(group_rank(ts_mean(loan_utilization_ratio, 66), sector))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_vwap_return_60m_post_open, mean_vwap_return_60m_pre_close_2), 126), industry)), rank(group_rank(ts_mean(loan_utilization_ratio, 66), sector))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_vwap_return_60m_post_open, mean_vwap_return_60m_pre_close_2), 126), industry)), rank(group_rank(ts_mean(borrow_activity_score, 66), sector))), sector)
trade_when(greater(rank(group_rank(ts_mean(borrow_activity_score, 66), sector)), 0.5), reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), -1)
trade_when(greater(rank(group_rank(ts_mean(loan_utilization_ratio, 66), sector)), 0.5), group_zscore(ts_zscore(subtract(mean_vwap_return_60m_post_open, mean_vwap_return_60m_pre_close_2), 126), industry), -1)
group_rank(multiply(rank(reverse(group_zscore(ts_zscore(subtract(mean_last_trade_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry))), rank(ts_delta(group_rank(ts_mean(loan_utilization_ratio, 66), sector), 22))), sector)
group_rank(multiply(rank(group_zscore(ts_zscore(subtract(mean_high_price_return_30m_pre_close_2, mean_vwap_return_30m_pre_close_2), 126), industry)), rank(divide(loaned_share_count, available_share_count))), sector)
```

## 派发设置（固定档）

```json
{"region":"HKG","universe":"TOP800","delay":1,"decay":4,"neutralization":"SECTOR",
 "truncation":0.08,"unit_handling":"VERIFY","nan_handling":"ON","pasteurization":"ON",
 "max_trade":"OFF","language":"FASTEXPR","instrument_type":"EQUITY"}
```

## 后续候选池（未派发，需新机制设计）

- `shortinterest5`（Daily Price Limit Data，3 字段 cov 1.0，ac 5–11）：价格限制触发事件。
- `insiders5`（1 字段 cov 0.999）/ `insiders1`（9 字段 cov 0.4538）。
- `other532`（Specific Returns，2 字段 VECTOR cov 1.0）：特质收益反转。
- `other543`（港交所 CCASS 持股穿透，cov 0.784–1.0）：南下资金持股变动。
- `dl_riskfree_returns`（OTHER，57 字段 cov 0.6514）：ASI 最强族，HKG 未验。
