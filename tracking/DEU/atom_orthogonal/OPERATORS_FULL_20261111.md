# 平台算子全集（103 个，get_operators 实测 2026-11-11）

## Arithmetic（16）

| 算子 | 签名 |
|---|---|
| `abs` | `abs(x)` |
| `add` | `add(x, y, filter = false), x + y` |
| `densify` | `densify(x)` |
| `divide` | `divide(x, y), x / y` |
| `inverse` | `inverse(x)` |
| `log` | `log(x)` |
| `max` | `max(x, y, ..)` |
| `min` | `min(x, y ..)` |
| `multiply` | `multiply(x ,y, ... , filter=false), x * y` |
| `pasteurize` | `pasteurize(x)` |
| `power` | `power(x, y)` |
| `reverse` | `reverse(x)` |
| `sign` | `sign(x)` |
| `signed_power` | `signed_power(x, y)` |
| `sqrt` | `sqrt(x)` |
| `subtract` | `subtract(x, y, filter=false), x - y` |

## Cross Sectional（7）

| 算子 | 签名 |
|---|---|
| `normalize` | `normalize(x, useStd = false, limit = 0.0)` |
| `quantile` | `quantile(x, driver = gaussian, sigma = 1.0)` |
| `rank` | `rank(x, rate=2)` |
| `scale` | `scale(x, scale=1, longscale=1, shortscale=1)` |
| `vector_neut` | `vector_neut(x, y)` |
| `winsorize` | `winsorize(x, std=4)` |
| `zscore` | `zscore(x)` |

## Group（11）

| 算子 | 签名 |
|---|---|
| `combo_a` | `combo_a(alpha, nlength = 250, mode = 'algo1')` |
| `group_backfill` | `group_backfill(x, group, d, std = 4.0)` |
| `group_cartesian_product` | `group_cartesian_product(g1, g2)` |
| `group_count` | `group_count(x, group)` |
| `group_mean` | `group_mean(x, weight, group)` |
| `group_neutralize` | `group_neutralize(x, group)` |
| `group_rank` | `group_rank(x, group)` |
| `group_scale` | `group_scale(x, group)` |
| `group_std_dev` | `group_std_dev(x, group)` |
| `group_sum` | `group_sum(x, group)` |
| `group_zscore` | `group_zscore(x, group)` |

## Logical（11）

| 算子 | 签名 |
|---|---|
| `and` | `and(input1, input2)` |
| `equal` | `input1 == input2` |
| `greater` | `input1 > input2` |
| `greater_equal` | `input1 >= input2` |
| `if_else` | `if_else(input1, input2, input 3)` |
| `is_nan` | `is_nan(input)` |
| `less` | `input1 < input2` |
| `less_equal` | `input1 <= input2` |
| `not` | `not(x)` |
| `not_equal` | `input1!= input2` |
| `or` | `or(input1, input2)` |

## Reduce（14）

| 算子 | 签名 |
|---|---|
| `reduce_avg` | `reduce_avg(input, threshold=0)` |
| `reduce_choose` | `reduce_choose(input, nth, ignoreNan=true)` |
| `reduce_count` | `reduce_count(input, threshold)` |
| `reduce_ir` | `reduce_ir(input)` |
| `reduce_kurtosis` | `reduce_kurtosis(input)` |
| `reduce_max` | `reduce_max(input)` |
| `reduce_min` | `reduce_min(input)` |
| `reduce_norm` | `reduce_norm(input)` |
| `reduce_percentage` | `reduce_percentage(input, percentage=0.5)` |
| `reduce_powersum` | `reduce_powersum(input, constant=2, precise=false)` |
| `reduce_range` | `reduce_range(input)` |
| `reduce_skewness` | `reduce_skewness(input)` |
| `reduce_stddev` | `reduce_stddev(input, threshold=0)` |
| `reduce_sum` | `reduce_sum(input)` |

## Special（3）

| 算子 | 签名 |
|---|---|
| `in` | `in` |
| `self_corr` | `self_corr(input)` |
| `universe_size` | `universe_size` |

## Time Series（30）

| 算子 | 签名 |
|---|---|
| `days_from_last_change` | `days_from_last_change(x)` |
| `hump` | `hump(x, hump = 0.01)` |
| `kth_element` | `kth_element(x, d, k, ignore=“NaN”)` |
| `last_diff_value` | `last_diff_value(x, d)` |
| `ts_arg_max` | `ts_arg_max(x, d)` |
| `ts_arg_min` | `ts_arg_min(x, d)` |
| `ts_av_diff` | `ts_av_diff(x, d)` |
| `ts_backfill` | `ts_backfill(x,lookback = d, k=1)` |
| `ts_corr` | `ts_corr(x, y, d)` |
| `ts_count_nans` | `ts_count_nans(x ,d)` |
| `ts_covariance` | `ts_covariance(y, x, d)` |
| `ts_decay_linear` | `ts_decay_linear(x, d, dense = false)` |
| `ts_delay` | `ts_delay(x, d)` |
| `ts_delta` | `ts_delta(x, d)` |
| `ts_ir` | `ts_ir(x, d)` |
| `ts_kurtosis` | `ts_kurtosis(x, d)` |
| `ts_max_diff` | `ts_max_diff(x, d)` |
| `ts_mean` | `ts_mean(x, d)` |
| `ts_product` | `ts_product(x, d)` |
| `ts_quantile` | `ts_quantile(x,d, driver="gaussian" )` |
| `ts_rank` | `ts_rank(x, d, constant = 0)` |
| `ts_regression` | `ts_regression(y, x, d, lag = 0, rettype = 0)` |
| `ts_returns` | `ts_returns (x, d, mode = 1)` |
| `ts_scale` | `ts_scale(x, d, constant = 0)` |
| `ts_std_dev` | `ts_std_dev(x, d)` |
| `ts_step` | `ts_step(1)` |
| `ts_sum` | `ts_sum(x, d)` |
| `ts_target_tvr_decay` | `ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)` |
| `ts_target_tvr_hump` | `ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)` |
| `ts_zscore` | `ts_zscore(x, d)` |

## Transformational（4）

| 算子 | 签名 |
|---|---|
| `bucket` | `bucket(rank(x), range=“0, 1, 0.1”, skipBoth=False, NaNGroup=False)
or
bucket(rank(x), buckets = “2,5,6,7,10”, skipBoth` |
| `generate_stats` | `generate_stats(alpha)` |
| `tail` | `tail(x, lower = 0, upper = 0, newval = 0)` |
| `trade_when` | `trade_when(x, y, z)` |

## Vector（7）

| 算子 | 签名 |
|---|---|
| `vec_avg` | `vec_avg(x)` |
| `vec_count` | `vec_count(x)` |
| `vec_max` | `vec_max(x)` |
| `vec_min` | `vec_min(x)` |
| `vec_range` | `vec_range(x)` |
| `vec_stddev` | `vec_stddev(x)` |
| `vec_sum` | `vec_sum(x)` |
