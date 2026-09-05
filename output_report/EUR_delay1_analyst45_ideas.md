# analyst45 Feature Engineering Analysis Report

**Dataset**: analyst45
**Region**: EUR
**Delay**: 1


- **Dataset**: `analyst45`
- **Category**: `analyst`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 61
- **Generated**: 2026-09-04T02:10:30.678477

---

## Executive Summary

本数据集提供 61 个字段（MATRIX 0 / VECTOR 61 / GROUP 0），覆盖 `analyst` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Field Type | Operator Adaptation | Description |
|---|---|---|---|---|---|
| `anl45_ad_rel_ret_per` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Average daily index relative return percentage |
| `anl45_ad_ret_per` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Average daily percent return over the idea’s lifetime |
| `anl45_ang_inv` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time-weighted average investment |
| `anl45_avg_dur` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Average age of the idea limited to the selected period |
| `anl45_avg_initial_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Average share price weighted by volume of each share purchase |
| `anl45_avg_initial_prc_wfee` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The avg initial price adjusted to include fee payment when fees are applied |
| `anl45_beta` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | A measure of the volatility or systematic risk of a security compared to the market, updated monthly based on last 20 mo |
| `anl45_bias_weighted_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Non-Functional |
| `anl45_bm_exchange_rate` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Exchange rate by which the benchmark will be measured |
| `anl45_bm_fx_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | FX return made by the benchmark due to currency movements |
| `anl45_bm_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Return of the benchmark index |
| `anl45_bm_ret_wo_fx` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Benchmark’s return excluding foreign exchange effects (raw benchmark return) |
| `anl45_closed_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Price at which the idea was closed |
| `anl45_current_inv` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Current investment amount, including increases and partial closures |
| `anl45_days_since_inception` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Number of trading days since the idea was submitted |
| `anl45_idea_count` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Number of ideas in a group, useful when grouping ideas |
| `anl45_index_period_end_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Benchmark or index end price for the selected performance period |
| `anl45_index_period_start_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Benchmark or index start price for the selected performance period |
| `anl45_index_ret_per` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Return percentage had the investment been made in the selected index |
| `anl45_initial_inv` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Initial investment amount allocated to the idea |
| `anl45_inv_exchange_rate` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Exchange rate between stock and investment currencies, typically the FX rate on the period end date |
| `anl45_jensensalpha` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Risk-adjusted performance measure representing return over market |
| `anl45_latest_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The current price of the stock in the idea |
| `anl45_net_market_exposure` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Difference in fractional total value between long and short ideas (net market exposure) |
| `anl45_new_value` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | New value set for the stop-loss percent, target price, or capital allocation |
| `anl45_old_value` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Previous value of the stop-loss percent, target price, or capital allocation before the latest change |
| `anl45_period_end_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Close price on day at end of selected period |
| `anl45_period_start_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Close price on day before start of selected period |
| `anl45_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The price given to the investment change |
| `anl45_prc_change_per_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Percent change in stock price since previous close of day price |
| `anl45_prc_change_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Change in stock price since previous day close |
| `anl45_prev_close_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Last available close price for the stock |
| `anl45_probability` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Tag giving a quantitative measure of conviction |
| `anl45_real_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Realized return from closed portions of the idea since inception |
| `anl45_real_ret_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Increase in realized return since the previous market close |
| `anl45_real_value` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Monetary value of the realized (closed) portion of the idea |
| `anl45_rel_index_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Difference in return percentage between the idea and the comparative index |
| `anl45_rel_index_ret_per` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Difference in return percentage between the idea and the comparative index |
| `anl45_rel_ret_per_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Relative return percentage today |
| `anl45_rel_ret_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Increase in realised return since last market close |
| `anl45_ret_per_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Percentage return since last market close |
| `anl45_ret_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Increase in realised return since last market close |
| `anl45_risk_free_rate` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The unrealised return on an open idea |
| `anl45_stock_ret_per` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Net total return from all ideas since the previous market close |
| `anl45_stock_ret_per_relative` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Average daily return percentage had the investment been made in the relative benchmark index |
| `anl45_target_prc` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Author’s stated likely exit price for the idea |
| `anl45_time` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Approximate time horizon for the idea |
| `anl45_tot_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Sum of realised and unrealised returns |
| `anl45_tot_ret_per` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Total return as a percentage of average investment |
| `anl45_tot_ret_wo_fx` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Total return excluding any foreign exchange effects |
| `anl45_transaction_charge` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Transaction fee charged for the idea (in calculation currency) |
| `anl45_treynor_ratio` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | A ratio that measures returns earned in excess of that which could have been earned on a riskless investment (such as th |
| `anl45_unreal_ret` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Unrealized return on the open idea (mark-to-market) |
| `anl45_unreal_ret_today` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Increase in unrealised return since the last market close |
| `anl45_unreal_value` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Unrealised value of an open idea |
| `benchmark_currency_code` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Currency of the benchmark |
| `conversion_rate_summary` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Exchange rate between investment and performance currencies |
| `currency_gain_percentage` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | FX-driven return expressed as a percentage of the invested amount |
| `currency_gain_value` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Return generated from variations in foreign exchange |
| `investment_currency_code` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Currency of the investment |
| `security_trading_currency_3` | VECTOR | 100% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Currency in which the security is traded |

## 字段-算子适配表（Field-Operator Adaptation）

| Field Type | Valid Operators | Forbidden Operators | Example |
|---|---|---|---|
| 连续数值型 | `ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression` | `ts_std_dev`（波动率无预测力）、`ts_max_diff`（加速脉冲失效） | `rank(ts_mean(surprise, 22))` |
| 分类型（quantile_label/rank） | `rank/group_rank/ts_backfill` | `ts_mean`（分类平均无意义）、`ts_zscore`（非连续分布） | `rank(ts_backfill(quantile_label, 66))` |
| 概率型（prob_class） | `rank/subtract/if_else` | `ts_mean`（概率平均稀释信号）、`ts_delta`（概率变化噪声大） | `rank(prob_class1) - rank(prob_class0)` |
| 计数型（count/usd） | `ts_sum/trade_when/ts_backfill` | `ts_delta`（计数变化=已反应）、`ts_max_diff`（加速脉冲失效） | `trade_when(count > 0, rank(x), NaN)` |
| 比率型（to_price/ratio） | `rank/group_zscore/group_neutralize` | `ts_mean`（比率平均无意义）、`ts_delta`（比率变化噪声） | `group_zscore(ratio, industry)` |
| VECTOR 型 | `vec_avg/vec_sum/vec_stddev/vec_range` + `ts_mean/ts_delta/rank` | 直接用 `ts_mean`（必须先聚合） | `rank(ts_mean(vec_avg(sentiment), 22))` |

## 字段解构（Field Deconstruction）

### `anl45_ad_rel_ret_per`（VECTOR）
- **测什么**：Average daily index relative return percentage
- **覆盖率**：1.0
- **字段名语义**：`anl45_ad_rel_ret_per` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_ad_ret_per`（VECTOR）
- **测什么**：Average daily percent return over the idea’s lifetime
- **覆盖率**：1.0
- **字段名语义**：`anl45_ad_ret_per` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_ang_inv`（VECTOR）
- **测什么**：Time-weighted average investment
- **覆盖率**：1.0
- **字段名语义**：`anl45_ang_inv` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_avg_dur`（VECTOR）
- **测什么**：Average age of the idea limited to the selected period
- **覆盖率**：1.0
- **字段名语义**：`anl45_avg_dur` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_avg_initial_prc`（VECTOR）
- **测什么**：Average share price weighted by volume of each share purchase
- **覆盖率**：1.0
- **字段名语义**：`anl45_avg_initial_prc` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_avg_initial_prc_wfee`（VECTOR）
- **测什么**：The avg initial price adjusted to include fee payment when fees are applied
- **覆盖率**：1.0
- **字段名语义**：`anl45_avg_initial_prc_wfee` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_beta`（VECTOR）
- **测什么**：A measure of the volatility or systematic risk of a security compared to the market, updated monthly based on last 20 months
- **覆盖率**：1.0
- **字段名语义**：`anl45_beta` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `anl45_bias_weighted_ret`（VECTOR）
- **测什么**：Non-Functional
- **覆盖率**：1.0
- **字段名语义**：`anl45_bias_weighted_ret` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：对 VECTOR/GROUP 字段先截面聚合再中性化
- vec_ 向量包装：61 个 VECTOR 字段需用 vec_* 算子读取

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-makeSomeGem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。

**Concept**: anl45_ad_rel_ret_per 长期水平稳定（Q1）
- **Mechanism**: ts_mean 度量字段长期水平，rank 截面归一化
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank(ts_mean({anl45_ad_rel_ret_per}, 66))`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per 变化动量（Q2）
- **Mechanism**: ts_delta 捕捉 21 日变化率，rank 截面归一化
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank(ts_delta({anl45_ad_rel_ret_per}, 21))`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per 截面离群（Q3）
- **Mechanism**: zscore 识别截面离群，rank 归一化
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank(zscore({anl45_ad_rel_ret_per}))`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per × anl45_ad_ret_per 交互（Q4）
- **Mechanism**: 两字段各自 ts_zscore 中性化后 multiply 合成
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank(multiply(ts_zscore({anl45_ad_rel_ret_per}, 66), ts_zscore({anl45_ad_ret_per}, 66)))`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per 结构占比（Q5）
- **Mechanism**: divide 构造比例关系，rank 截面归一化
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank(divide({anl45_ad_rel_ret_per}, {anl45_ad_ret_per}))`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per 累积衰减（Q6）
- **Mechanism**: ts_decay_linear 累积记忆衰减，rank 归一化
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank(ts_decay_linear({anl45_ad_rel_ret_per}, 21))`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per 截面相对定位（Q7）
- **Mechanism**: ts_backfill 稀疏回填 + group_rank 行业内相对定位
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `group_rank(ts_backfill({anl45_ad_rel_ret_per}, 66), industry)`
- **Direction**: High → long

**Concept**: anl45_ad_rel_ret_per 本质直取（Q8）
- **Mechanism**: 第一性原理直取原始字段，rank 截面归一化
- **Fields Used**: `anl45_ad_rel_ret_per`, `anl45_ad_ret_per`
- **Implementation Example**: `rank({anl45_ad_rel_ret_per})`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
anl45_ad_rel_ret_per
anl45_ad_ret_per
anl45_ang_inv
anl45_avg_dur
anl45_avg_initial_prc
anl45_avg_initial_prc_wfee
anl45_beta
anl45_bias_weighted_ret
anl45_bm_exchange_rate
anl45_bm_fx_ret
anl45_bm_ret
anl45_bm_ret_wo_fx
anl45_closed_prc
anl45_current_inv
anl45_days_since_inception
anl45_idea_count
anl45_index_period_end_prc
anl45_index_period_start_prc
anl45_index_ret_per
anl45_initial_inv
anl45_inv_exchange_rate
anl45_jensensalpha
anl45_latest_prc
anl45_net_market_exposure
anl45_new_value
anl45_old_value
anl45_period_end_prc
anl45_period_start_prc
anl45_prc
anl45_prc_change_per_today
anl45_prc_change_today
anl45_prev_close_prc
anl45_probability
anl45_real_ret
anl45_real_ret_today
anl45_real_value
anl45_rel_index_ret
anl45_rel_index_ret_per
anl45_rel_ret_per_today
anl45_rel_ret_today
anl45_ret_per_today
anl45_ret_today
anl45_risk_free_rate
anl45_stock_ret_per
anl45_stock_ret_per_relative
anl45_target_prc
anl45_time
anl45_tot_ret
anl45_tot_ret_per
anl45_tot_ret_wo_fx
anl45_transaction_charge
anl45_treynor_ratio
anl45_unreal_ret
anl45_unreal_ret_today
anl45_unreal_value
benchmark_currency_code
conversion_rate_summary
currency_gain_percentage
currency_gain_value
investment_currency_code
security_trading_currency_3
```

*Report generated: 2026-09-04T02:10:30.678477*