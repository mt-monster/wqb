# WQ BRAIN 算子清单 × 已提交 Alpha 算子使用审计（2026-09-30）

- 算子清单来源：`docs/reference/operators_catalog.json`（平台实况快照 2026-09-07，103 个），与 `data/operators_verified.json` （2026-09-04 探针，103 live）一致。
- 已提交 alpha 口径：`submission_ledger` ∪ `platform_status∈(ACTIVE,DECOMMISSIONED)`，共 **235** 条；使用足迹（全部回测过）**9336** 条。
- 已提交集中用过 **45/103** 个算子；未用 **58** 个（其中 21 个连回测足迹都未出现）。


## 一、完整算子清单（按平台 category 分组）


### Arithmetic（16 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `abs` | `abs(x)` | Returns the absolute value of a number, removing any negative sign. | COMBO,REGULAR,SELECTION |
| `add` | `add(x, y, filter = false), x + y` | Adds two or more inputs element wise. Set filter=true to treat NaNs as 0 before summing. | COMBO,REGULAR,SELECTION |
| `densify` | `densify(x)` | Converts a grouping field of many buckets into lesser number of only available buckets so as to make working with grouping fields computationally efficient | COMBO,REGULAR |
| `divide` | `divide(x, y), x / y` | Returns x divided by y (x / y). Note: dividing by zero raises an error; to avoid it, use divide(x, add(y, 0.0001)); adding a small epsilon to the denominator prevents divide-by-zero errors. | COMBO,REGULAR,SELECTION |
| `inverse` | `inverse(x)` | Returns the reciprocal of x (1 / x). Note: errors when x = 0; to avoid it, use inverse(add(x, 0.0001)); adding a small epsilon prevents divide-by-zero errors. | COMBO,REGULAR,SELECTION |
| `log` | `log(x)` | Calculates the natural logarithm of the input value. Commonly used to transform data that has positive values. | COMBO,REGULAR,SELECTION |
| `max` | `max(x, y, ..)` | Maximum value of all inputs. At least 2 inputs are required | COMBO,REGULAR,SELECTION |
| `min` | `min(x, y ..)` | Minimum value of all inputs. At least 2 inputs are required | COMBO,REGULAR,SELECTION |
| `multiply` | `multiply(x ,y, ... , filter=false), x * y` | Multiplies two or more inputs element wise. Set filter=true to treat NaNs as 0 before multiplication | COMBO,REGULAR,SELECTION |
| `pasteurize` | `pasteurize(x)` | Set to NaN if x is INF or if the underlying instrument is not in the Alpha universe. This operator may help reduce outliers.  Input: Value of 7 instruments at day t: (2, 3, 5, INF, 3, 8, 10), where value 10 does not belong in Alpha universe Output: (2, 3, 5, NaN, 3, 8, NaN) | COMBO,REGULAR |
| `power` | `power(x, y)` | Returns x raised to the power of y (x ^ y). Note: power(x, y) can drop the sign of x when y is non-integer; use signed_power(x, y) to preserve the sign of x. | COMBO,REGULAR,SELECTION |
| `reverse` | `reverse(x)` |  - x | COMBO,REGULAR,SELECTION |
| `sign` | `sign(x)` | Returns the sign of a number: +1 for positive, -1 for negative, and 0 for zero. If the input is NaN, returns NaN.  Input: Value of 7 instruments at day t: (2, -3, 5, 6, 3, NaN, -10) Output: (1, -1, 1, 1, 1, NaN, -1) | COMBO,REGULAR,SELECTION |
| `signed_power` | `signed_power(x, y)` | x raised to the power of y such that final result preserves sign of x | COMBO,REGULAR,SELECTION |
| `sqrt` | `sqrt(x)` | Returns the non-negative square root of x. Equivalent to power(x, 0.5). Note: for x < 0 the result is undefined; to retain the sign of x, use signed_power(x, 0.5) instead. | COMBO,REGULAR,SELECTION |
| `subtract` | `subtract(x, y, filter=false), x - y` | Subtracts inputs left to right: x ? y ? … Supports two or more inputs. Set filter=true to treat NaNs as 0 before subtraction. | COMBO,REGULAR,SELECTION |

### Cross Sectional（6 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `normalize` | `normalize(x, useStd = false, limit = 0.0)` | Centers a daily cross section by subtracting the market mean; optionally divide by the cross sectional standard deviation and clamp the result to [?limit, +limit]. NaNs are ignored in mean/std. | COMBO,REGULAR |
| `quantile` | `quantile(x, driver = gaussian, sigma = 1.0)` | Ranks and shifts a vector of Alpha values, then applies a chosen statistical distribution (gaussian, cauchy, or uniform) to reduce outliers. The sigma parameter controls the scale of the output. | COMBO,REGULAR |
| `rank` | `rank(x, rate=2)` | Ranks the values of the input x among all instruments, returning numbers evenly spaced between 0.0 and 1.0. Useful for normalizing data and reducing the impact of outliers. | COMBO,REGULAR |
| `scale` | `scale(x, scale=1, longscale=1, shortscale=1)` | Scales the input so that the sum of absolute values across all instruments equals a specified book size. Allows separate scaling for long and short positions using optional parameters. | COMBO,REGULAR |
| `winsorize` | `winsorize(x, std=4)` | Winsorize limits values in a data to within a specified number of standard deviations from the mean, reducing the impact of extreme outliers. Note: recommended std values range from 2 to 5: std = 2, 3, 4, 5 removes approximately 4.5%, 0.27%, 0.01%, and 0.0001% of extreme values, respectively (higher std removes fewer extremes). | COMBO,REGULAR |
| `zscore` | `zscore(x)` | Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean | COMBO,REGULAR |

### Group（11 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `combo_a` ⚠SUPER专属 | `combo_a(alpha, nlength = 250, mode = 'algo1')` | Combines multiple alpha signals into a single weighted output by balancing each alpha's historical return with its variability over the most recent nlength days.  The parameter mode selects one of the several weighted approaches (algo1, algo2, algo3), each of which handles the tradeoff between performance and stability differently. | COMBO |
| `group_backfill` | `group_backfill(x, group, d, std = 4.0)` | Fills missing (NaN) values for instruments within the same group by calculating a winsorized mean of all non-NaN values over the past d days. The winsorized mean is computed by trimming extreme values based on a specified standard deviation multiplier (std, default 4.0). | COMBO,REGULAR |
| `group_cartesian_product` | `group_cartesian_product(g1, g2)` | Merge two groups into one group. If originally there are len_1 and len_2 group indices in g1 and g2, there will be len_1 * len_2 indices in the new group. | COMBO,REGULAR |
| `group_count` | `group_count(x, group)` | Gives the number of instruments in the same group (e.g. sector) which have valid values of x. For example, x=1 gives the number of instruments in each group (without regard for whether any particular field has valid data). This operator improves weight coverage and may help to reduce drawdown risk. | COMBO,REGULAR |
| `group_mean` | `group_mean(x, weight, group)` | Calculates the harmonic mean of a data field within each specified group. | COMBO,REGULAR |
| `group_neutralize` | `group_neutralize(x, group)` | Neutralizes Alpha values within each specified group by subtracting the group mean from each value. Groups can be industry, sector, country, or any custom grouping. | COMBO,REGULAR |
| `group_rank` | `group_rank(x, group)` | Ranks each element within its group based on the input field, assigning a value between 0.0 and 1.0. This helps compare items within the same group, such as stocks in the same industry. | COMBO,REGULAR |
| `group_scale` | `group_scale(x, group)` | Normalizes values within each group to a range between 0 and 1, making data comparable across different groups. | COMBO,REGULAR |
| `group_std_dev` | `group_std_dev(x, group)` | All elements in group equals to the standard deviation of the group. | COMBO,REGULAR |
| `group_sum` | `group_sum(x, group)` | Sum of x for all instruments in the same group. | COMBO,REGULAR |
| `group_zscore` | `group_zscore(x, group)` | Calculates the Z-score of each value within its group, showing how far each value is from the group mean in terms of standard deviations. Useful for comparing values relative to their group. | COMBO,REGULAR |

### Logical（11 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `and` | `and(input1, input2)` | Returns 1 ('true') if both inputs are 1 ('true'). Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `equal` | `input1 == input2` | Returns 1 ('true') if input1 and input2 are the same. Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `greater` | `input1 > input2` | Returns 1 ('true') if input1 is a larger than input2. Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `greater_equal` | `input1 >= input2` | Returns 1 ('true') if input1 is a larger or the same as input2. Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `if_else` | `if_else(input1, input2, input 3)` | The if_else operator returns one of two values based on a condition. If the condition is true, it returns the first value; if false, it returns the second value. | COMBO,REGULAR,SELECTION |
| `is_nan` | `is_nan(input)` | If (input == NaN) return 1 else return 0 | COMBO,REGULAR,SELECTION |
| `less` | `input1 < input2` | Returns 1 ('true') if input1 is a smaller than input2. Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `less_equal` | `input1 <= input2` | Returns 1 ('true') if input1 is a smaller or the same as input2. Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `not` | `not(x)` | Returns the logical negation of x. Returns 0 when x is 1 (‘true’) and 1 when x is 0 (‘false’). | COMBO,REGULAR,SELECTION |
| `not_equal` | `input1!= input2` | Returns 1 ('true') if input1 and input2 are different numbers. Otherwise, returns 0 ('false'). | COMBO,REGULAR,SELECTION |
| `or` | `or(input1, input2)` | Returns 1 if either input is true (either input1 or input2 has a value of 1), otherwise it returns 0. | COMBO,REGULAR,SELECTION |

### Reduce（14 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `reduce_avg` | `reduce_avg(input, threshold=0)` | Average of non-NAN elements of d(..., :). Threshold: Minimum required number of valid (non-nan) values. If there is not enough valid values, then the output is nan. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_choose` | `reduce_choose(input, nth, ignoreNan=true)` | Choose the 'nth' element in the array, return NAN if not found. Threshold: nth="<the Nth element>" (Required) ignoreNan="true\|false" (Default: true) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_count` | `reduce_count(input, threshold)` | Count the number of element of d(..., :) > threshold. threshold=<float> *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_ir` | `reduce_ir(input)` | IR of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_kurtosis` | `reduce_kurtosis(input)` | Kurtosis of values in the array ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix.  If input matrix is (D x N), output matrix (D x 1)  If input matrix is (D x N X N), output matrix (D x N X 1)  The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_max` | `reduce_max(input)` | Maximum of elements of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_min` | `reduce_min(input)` | Minimum of elements of d(..., :) ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix.  If input matrix is (D x N), output matrix (D x 1)  If input matrix is (D x N X N), output matrix (D x N X 1)  The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_norm` | `reduce_norm(input)` | Absolute sum of number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_percentage` | `reduce_percentage(input, percentage=0.5)` | Return the value of percentage in the sorted array: e.g., median value when percentage=0.5. Threshold: percentage="<value between 0 and 1>" (Default: 0.5) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_powersum` | `reduce_powersum(input, constant=2, precise=false)` | Sum of power, sum(power(x, constant)). Threshold: precise, whether calculate power precise if constant greater than 4, default false constant=<integer value>, default:2 *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_range` | `reduce_range(input)` | Return the range of values in the array, return NAN if no valid value *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_skewness` | `reduce_skewness(input)` | Skewness of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_stddev` | `reduce_stddev(input, threshold=0)` | Standard deviation of values in the array. Threshold: Minimum required percentage of valid (non-nan) values. If there is not enough valid values, then the output is NAN. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |
| `reduce_sum` | `reduce_sum(input)` | Sum the number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | COMBO |

### Special（3 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `in` | `in` | in | SELECTION |
| `self_corr` ⚠SUPER专属 | `self_corr(input)` | Taking an input matrix of (D x N) with lookback="K", producing an output matrix of (D x N x N), where each output(di, j, k) refers to correlation of input(di-K:di, j) and input(di-K:di, k). Outputs (D x N x N) from the input of (D x N) | COMBO |
| `universe_size` ⚠SUPER专属 | `universe_size` | universe_size | SELECTION |

### Time Series（30 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `days_from_last_change` | `days_from_last_change(x)` | Calculates the number of days since the last change in the value of a given variable. | COMBO,REGULAR |
| `hump` | `hump(x, hump = 0.01)` | Limits amount and magnitude of changes in input (thus reducing turnover) | COMBO,REGULAR |
| `kth_element` | `kth_element(x, d, k, ignore=“NaN”)` | Returns the K-th value from a time series by looking back over a specified number of (‘d’) days, with the option to ignore certain values. Commonly used for backfilling missing data. | COMBO,REGULAR |
| `last_diff_value` | `last_diff_value(x, d)` | Returns the most recent value of x from the past d days that is different from the current value of x. | COMBO,REGULAR |
| `ts_arg_max` | `ts_arg_max(x, d)` | Returns the number of days since the maximum value occurred in the last d days of a time series. If today's value is the maximum, returns 0; if it was yesterday, returns 1, and so on. | COMBO,REGULAR |
| `ts_arg_min` | `ts_arg_min(x, d)` | Returns the number of days since the minimum value occurred in a time series over the past d days. If today's value is the minimum, returns 0; if it was yesterday, returns 1, and so on. | COMBO,REGULAR |
| `ts_av_diff` | `ts_av_diff(x, d)` | Calculates the difference between a value and its mean over a specified period, ignoring NaN values in the mean calculation. In short, it returns x – ts_mean(x, d) with NaNs ignored. | COMBO,REGULAR |
| `ts_backfill` | `ts_backfill(x,lookback = d, k=1)` | Replaces missing (NaN) values in a time series with the most recent valid value from a specified lookback window, improving data coverage and reducing risk from missing data. | COMBO,REGULAR |
| `ts_corr` | `ts_corr(x, y, d)` | Calculates the Pearson correlation between two variables, x and y, over the past d days, showing how closely they move together. | COMBO,REGULAR |
| `ts_count_nans` | `ts_count_nans(x ,d)` | Counts the number of missing (NaN) values in a data series over a specified number of days. | COMBO,REGULAR |
| `ts_covariance` | `ts_covariance(y, x, d)` | Calculates the covariance between two time-series variables, y and x, over the past d days. Useful for measuring how two variables move together within a specified historical window. | COMBO,REGULAR |
| `ts_decay_linear` | `ts_decay_linear(x, d, dense = false)` | Applies a linear decay to time-series data over a set number of days, smoothing the data by averaging recent values and reducing the impact of older or missing data. | COMBO,REGULAR |
| `ts_delay` | `ts_delay(x, d)` | Returns the value of a variable x from d days ago. Use this operator to access historical data points by specifying the desired time lag in days. | COMBO,REGULAR |
| `ts_delta` | `ts_delta(x, d)` | Calculates the difference between a value and its delayed version over a specified period. Useful for measuring changes or momentum in time-series data. | COMBO,REGULAR |
| `ts_ir` | `ts_ir(x, d)` | Return information ratio ts_mean(x, d) / ts_std_dev(x, d) | COMBO,REGULAR |
| `ts_kurtosis` | `ts_kurtosis(x, d)` | Returns kurtosis of x for the last d days | COMBO,REGULAR |
| `ts_max_diff` | `ts_max_diff(x, d)` | Returns x - ts_max(x, d) | COMBO,REGULAR |
| `ts_mean` | `ts_mean(x, d)` | Calculates the simple average (mean) value of a variable x over the past d days. | COMBO,REGULAR |
| `ts_product` | `ts_product(x, d)` | Returns the product of the values of x over the past d days. Useful for calculating geometric means and compounding returns or growth rates. | COMBO,REGULAR |
| `ts_quantile` | `ts_quantile(x,d, driver="gaussian" )` | Calculates the ts_rank of the input and transforms it using the inverse cumulative distribution function (quantile function) of a specified probability distribution (default: Gaussian/normal). This helps to normalize or reshape the distribution of your data over a rolling window. | COMBO,REGULAR |
| `ts_rank` | `ts_rank(x, d, constant = 0)` | Ranks the value of a variable for each instrument over a specified number of past days, returning the rank of the current value (optionally adjusted by a constant). Useful for normalizing time-series data and highlighting relative performance over time. | COMBO,REGULAR |
| `ts_regression` | `ts_regression(y, x, d, lag = 0, rettype = 0)` | Returns various parameters related to regression function | COMBO,REGULAR |
| `ts_returns` | `ts_returns (x, d, mode = 1)` | Returns the relative change in the x value | COMBO,REGULAR |
| `ts_scale` | `ts_scale(x, d, constant = 0)` | Scales a time series to a 0–1 range based on its minimum and maximum values over a specified period, with an optional constant shift. | COMBO,REGULAR |
| `ts_std_dev` | `ts_std_dev(x, d)` | Calculates the standard deviation of a data series x over the past d days, measuring how much the values deviate from their mean during that period. | COMBO,REGULAR |
| `ts_step` | `ts_step(1)` | Returns a counter of days, incrementing by one each day. | COMBO,REGULAR |
| `ts_sum` | `ts_sum(x, d)` | Sum values of x for the past d days. | COMBO,REGULAR |
| `ts_target_tvr_decay` | `ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)` | Tune "ts_decay" to have a turnover equal to a certain target, with optimization weight range between lambda_min, lambda_max | COMBO,REGULAR |
| `ts_target_tvr_hump` | `ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)` | Tune "hump" to have a turnover equal to a certain target with optimization weight range between lambda_min, lambda_max. | COMBO,REGULAR |
| `ts_zscore` | `ts_zscore(x, d)` | Calculates the Z-score of a time series, showing how far today's value is from the recent average, measured in standard deviations. Useful for standardizing and comparing values over time. | COMBO,REGULAR |

### Transformational（4 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `bucket` | `bucket(rank(x), range=“0, 1, 0.1”, skipBoth=False, NaNGroup=False)
or
bucket(rank(x), buckets = “2,5,6,7,10”, skipBoth=False, NaNGroup=False)` | The bucket operator creates custom groups by dividing data into buckets (ranges) based on ranked values of any data field. These buckets can then be used with group operators like group_neutralize, group_rank, group_zscore etc. | COMBO,REGULAR |
| `generate_stats` ⚠SUPER专属 | `generate_stats(alpha)` | The generate_stats() operator calculates Alpha statistics for each day in the IS period. It takes an input of selected Alphas with shape = (A x D x I). It outputs daily statistics for each Alpha with shape = (S x D x A), where S is the number of statistics calculated. | COMBO |
| `tail` | `tail(x, lower = 0, upper = 0, newval = 0)` | If (x > lower AND x < upper) return newval, else return x. Lower, upper, newval should be constants | COMBO,REGULAR |
| `trade_when` | `trade_when(x, y, z)` | The trade_when operator changes Alpha values only when a specific condition is met, keeps previous values otherwise, and can close positions by assigning NaN under an exit condition. It is useful for reducing turnover and controlling when trades are executed. | COMBO,REGULAR |

### Vector（8 个）

| 算子 | 定义/签名 | 功能描述 | 适用场景 |
|---|---|---|---|
| `vec_avg` | `vec_avg(x)` | Calculates the mean (average) of all elements in a vector field for each instrument and date, converting vector data to a single matrix value. | COMBO,REGULAR |
| `vec_count` | `vec_count(x)` | Number of elements in vector field x | COMBO,REGULAR |
| `vec_max` | `vec_max(x)` | Maximum value form vector field x | COMBO,REGULAR |
| `vec_min` | `vec_min(x)` | Minimum value form vector field x | COMBO,REGULAR |
| `vec_range` | `vec_range(x)` | Difference between maximum and minimum element in vector field x | COMBO,REGULAR |
| `vec_stddev` | `vec_stddev(x)` | Standard Deviation of vector field x | COMBO,REGULAR |
| `vec_sum` | `vec_sum(x)` | Calculates the sum of all values in a vector field. | COMBO,REGULAR |
| `vector_neut` | `vector_neut(a, b)` | Vector orthogonalization: removes the component of vector a in the direction of vector b, i.e., a - (a·b)b. Used to neutralize exposure to a specific factor or direction (e.g., market cap, sector). | COMBO,REGULAR |


## 二、已提交 alpha 的算子使用统计

| 算子 | 提交集使用次数 | 全足迹使用次数 |
|---|---|---|
| `rank` | 116 | 4159 |
| `ts_mean` | 101 | 2434 |
| `group_rank` | 72 | 2456 |
| `ts_std_dev` | 63 | 404 |
| `add` | 55 | 1561 |
| `ts_backfill` | 50 | 2105 |
| `multiply` | 50 | 1146 |
| `subtract` | 43 | 2442 |
| `group_neutralize` | 38 | 247 |
| `vec_avg` | 36 | 1849 |
| `abs` | 35 | 429 |
| `vector_neut` | 35 | 131 |
| `bucket` | 32 | 269 |
| `ts_sum` | 31 | 232 |
| `ts_zscore` | 27 | 908 |
| `ts_rank` | 27 | 507 |
| `trade_when` | 21 | 609 |
| `divide` | 20 | 1957 |
| `group_mean` | 17 | 35 |
| `ts_delta` | 16 | 1212 |
| `ts_decay_linear` | 15 | 1105 |
| `signed_power` | 14 | 504 |
| `greater` | 11 | 310 |
| `or` | 10 | 159 |
| `and` | 10 | 175 |
| `log` | 9 | 63 |
| `less` | 8 | 210 |
| `group_zscore` | 6 | 556 |
| `quantile` | 4 | 420 |
| `scale` | 4 | 29 |
| `sign` | 4 | 155 |
| `normalize` | 3 | 8 |
| `reverse` | 2 | 400 |
| `is_nan` | 2 | 5 |
| `if_else` | 2 | 233 |
| `winsorize` | 2 | 259 |
| `densify` | 2 | 17 |
| `ts_arg_max` | 2 | 79 |
| `ts_delay` | 2 | 17 |
| `vec_sum` | 2 | 238 |
| `vec_max` | 1 | 38 |
| `ts_av_diff` | 1 | 305 |
| `ts_corr` | 1 | 281 |
| `ts_ir` | 1 | 69 |
| `hump` | 1 | 136 |


## 三、未使用算子清单（提交集，58 个）

> 口径提示：SUPER 的 selection/combo 字符串不存入 `alphas.expression`（实测 6 颗 SUPER 该列为空），故 `combo_a`/`generate_stats`/`self_corr`/`universe_size`/`reduce_max` 的「未使用」是统计假象——它们已在 SUPER 组合串中实装（见 MEMORY §3 的 KOR SA 配方）。

| 算子 | category | 功能 | 全足迹是否用过 |
|---|---|---|---|
| `combo_a` | Group | Combines multiple alpha signals into a single weighted output by balancing each alpha's historical return with its variability over the most recent nlength days.  The parameter mode selects one of the several weighted approaches (algo1, algo2, algo3), each of which handles the tradeoff between performance and stability differently. | SUPER 组合串已用（本表不覆盖）（SUPER专属） |
| `days_from_last_change` | Time Series | Calculates the number of days since the last change in the value of a given variable. | 用过 |
| `equal` | Logical | Returns 1 ('true') if input1 and input2 are the same. Otherwise, returns 0 ('false'). | 用过 |
| `generate_stats` | Transformational | The generate_stats() operator calculates Alpha statistics for each day in the IS period. It takes an input of selected Alphas with shape = (A x D x I). It outputs daily statistics for each Alpha with shape = (S x D x A), where S is the number of statistics calculated. | SUPER 组合串已用（本表不覆盖）（SUPER专属） |
| `greater_equal` | Logical | Returns 1 ('true') if input1 is a larger or the same as input2. Otherwise, returns 0 ('false'). | **从未使用** |
| `group_backfill` | Group | Fills missing (NaN) values for instruments within the same group by calculating a winsorized mean of all non-NaN values over the past d days. The winsorized mean is computed by trimming extreme values based on a specified standard deviation multiplier (std, default 4.0). | 用过 |
| `group_cartesian_product` | Group | Merge two groups into one group. If originally there are len_1 and len_2 group indices in g1 and g2, there will be len_1 * len_2 indices in the new group. | 用过 |
| `group_count` | Group | Gives the number of instruments in the same group (e.g. sector) which have valid values of x. For example, x=1 gives the number of instruments in each group (without regard for whether any particular field has valid data). This operator improves weight coverage and may help to reduce drawdown risk. | 用过 |
| `group_scale` | Group | Normalizes values within each group to a range between 0 and 1, making data comparable across different groups. | 用过 |
| `group_std_dev` | Group | All elements in group equals to the standard deviation of the group. | 用过 |
| `group_sum` | Group | Sum of x for all instruments in the same group. | 用过 |
| `in` | Special | in | **从未使用** |
| `inverse` | Arithmetic | Returns the reciprocal of x (1 / x). Note: errors when x = 0; to avoid it, use inverse(add(x, 0.0001)); adding a small epsilon prevents divide-by-zero errors. | 用过 |
| `kth_element` | Time Series | Returns the K-th value from a time series by looking back over a specified number of (‘d’) days, with the option to ignore certain values. Commonly used for backfilling missing data. | **从未使用** |
| `last_diff_value` | Time Series | Returns the most recent value of x from the past d days that is different from the current value of x. | 用过 |
| `less_equal` | Logical | Returns 1 ('true') if input1 is a smaller or the same as input2. Otherwise, returns 0 ('false'). | **从未使用** |
| `max` | Arithmetic | Maximum value of all inputs. At least 2 inputs are required | 用过 |
| `min` | Arithmetic | Minimum value of all inputs. At least 2 inputs are required | 用过 |
| `not` | Logical | Returns the logical negation of x. Returns 0 when x is 1 (‘true’) and 1 when x is 0 (‘false’). | **从未使用** |
| `not_equal` | Logical | Returns 1 ('true') if input1 and input2 are different numbers. Otherwise, returns 0 ('false'). | 用过 |
| `pasteurize` | Arithmetic | Set to NaN if x is INF or if the underlying instrument is not in the Alpha universe. This operator may help reduce outliers.  Input: Value of 7 instruments at day t: (2, 3, 5, INF, 3, 8, 10), where value 10 does not belong in Alpha universe Output: (2, 3, 5, NaN, 3, 8, NaN) | 用过 |
| `power` | Arithmetic | Returns x raised to the power of y (x ^ y). Note: power(x, y) can drop the sign of x when y is non-integer; use signed_power(x, y) to preserve the sign of x. | 用过 |
| `reduce_avg` | Reduce | Average of non-NAN elements of d(..., :). Threshold: Minimum required number of valid (non-nan) values. If there is not enough valid values, then the output is nan. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_choose` | Reduce | Choose the 'nth' element in the array, return NAN if not found. Threshold: nth="<the Nth element>" (Required) ignoreNan="true\|false" (Default: true) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_count` | Reduce | Count the number of element of d(..., :) > threshold. threshold=<float> *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_ir` | Reduce | IR of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_kurtosis` | Reduce | Kurtosis of values in the array ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix.  If input matrix is (D x N), output matrix (D x 1)  If input matrix is (D x N X N), output matrix (D x N X 1)  The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_max` | Reduce | Maximum of elements of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | SUPER 组合串已用（本表不覆盖） |
| `reduce_min` | Reduce | Minimum of elements of d(..., :) ***Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix.  If input matrix is (D x N), output matrix (D x 1)  If input matrix is (D x N X N), output matrix (D x N X 1)  The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_norm` | Reduce | Absolute sum of number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_percentage` | Reduce | Return the value of percentage in the sorted array: e.g., median value when percentage=0.5. Threshold: percentage="<value between 0 and 1>" (Default: 0.5) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_powersum` | Reduce | Sum of power, sum(power(x, constant)). Threshold: precise, whether calculate power precise if constant greater than 4, default false constant=<integer value>, default:2 *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_range` | Reduce | Return the range of values in the array, return NAN if no valid value *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_skewness` | Reduce | Skewness of values in the array *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_stddev` | Reduce | Standard deviation of values in the array. Threshold: Minimum required percentage of valid (non-nan) values. If there is not enough valid values, then the output is NAN. 0 means no limit.threshold (Default: 0) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `reduce_sum` | Reduce | Sum the number of element of d(..., :) *** Takes an input 2-D or 3-D matrix with user-defined reducer, producing an output matrix. *If input matrix is (D x N), output matrix (D x 1) *If input matrix is (D x N X N), output matrix (D x N X 1) *The defined function is applied on the last dimension : output(I) = reduce(input(I, 0:N)). | **从未使用** |
| `self_corr` | Special | Taking an input matrix of (D x N) with lookback="K", producing an output matrix of (D x N x N), where each output(di, j, k) refers to correlation of input(di-K:di, j) and input(di-K:di, k). Outputs (D x N x N) from the input of (D x N) | SUPER 组合串已用（本表不覆盖）（SUPER专属） |
| `sqrt` | Arithmetic | Returns the non-negative square root of x. Equivalent to power(x, 0.5). Note: for x < 0 the result is undefined; to retain the sign of x, use signed_power(x, 0.5) instead. | **从未使用** |
| `tail` | Transformational | If (x > lower AND x < upper) return newval, else return x. Lower, upper, newval should be constants | 用过 |
| `ts_arg_min` | Time Series | Returns the number of days since the minimum value occurred in a time series over the past d days. If today's value is the minimum, returns 0; if it was yesterday, returns 1, and so on. | 用过 |
| `ts_count_nans` | Time Series | Counts the number of missing (NaN) values in a data series over a specified number of days. | 用过 |
| `ts_covariance` | Time Series | Calculates the covariance between two time-series variables, y and x, over the past d days. Useful for measuring how two variables move together within a specified historical window. | 用过 |
| `ts_kurtosis` | Time Series | Returns kurtosis of x for the last d days | 用过 |
| `ts_max_diff` | Time Series | Returns x - ts_max(x, d) | 用过 |
| `ts_product` | Time Series | Returns the product of the values of x over the past d days. Useful for calculating geometric means and compounding returns or growth rates. | **从未使用** |
| `ts_quantile` | Time Series | Calculates the ts_rank of the input and transforms it using the inverse cumulative distribution function (quantile function) of a specified probability distribution (default: Gaussian/normal). This helps to normalize or reshape the distribution of your data over a rolling window. | 用过 |
| `ts_regression` | Time Series | Returns various parameters related to regression function | 用过 |
| `ts_returns` | Time Series | Returns the relative change in the x value | 用过 |
| `ts_scale` | Time Series | Scales a time series to a 0–1 range based on its minimum and maximum values over a specified period, with an optional constant shift. | 用过 |
| `ts_step` | Time Series | Returns a counter of days, incrementing by one each day. | **从未使用** |
| `ts_target_tvr_decay` | Time Series | Tune "ts_decay" to have a turnover equal to a certain target, with optimization weight range between lambda_min, lambda_max | 用过 |
| `ts_target_tvr_hump` | Time Series | Tune "hump" to have a turnover equal to a certain target with optimization weight range between lambda_min, lambda_max. | 用过 |
| `universe_size` | Special | universe_size | SUPER 组合串已用（本表不覆盖）（SUPER专属） |
| `vec_count` | Vector | Number of elements in vector field x | 用过 |
| `vec_min` | Vector | Minimum value form vector field x | 用过 |
| `vec_range` | Vector | Difference between maximum and minimum element in vector field x | 用过 |
| `vec_stddev` | Vector | Standard Deviation of vector field x | 用过 |
| `zscore` | Cross Sectional | Z-score is a numerical measurement that describes a value's relationship to the mean of a group of values. Z-score is measured in terms of standard deviations from the mean | 用过 |


## 四、等价平替建议（功能一致、可直接/近直接替换）

说明：A ↔ B 表示双向可换；每行附替换注意点。「已用/未用」以提交集为准，便于双向查阅：既可查『我没用过的算子能平替我哪个惯用算子』（去同质化、降 self-corr），也可查『未用算子本身等价于我已用的谁』（判断是否真缺能力）。

| 算子 A | 平替 B | A 状态 | B 状态 | 替换说明与注意事项 |
|---|---|---|---|---|
| `ts_mean` | `ts_decay_linear` | 已用 | 已用 | 同为时序平滑；decay 线性衰减加权（近重远轻）。同窗口可直接换；换手通常略升、对近期更敏感。 |
| `ts_mean` | `ts_sum` | 已用 | 已用 | ts_sum(x,n)/n 即 ts_mean；需要显式分母时用。 |
| `ts_zscore` | `ts_rank` | 已用 | 已用 | 同为时序自归一化；ts_rank 输出 (0,1) 均匀分布、抗离群，ts_zscore 保留幅度但怕肥尾。 |
| `ts_zscore` | `ts_quantile` | 已用 | 未用 | ts_quantile(x,n) 返回过去 n 日分位，抗极端值更强；语义与 ts_rank 接近。 |
| `zscore` | `rank` | 未用 | 已用 | 同为截面标准化；rank 均匀化抗离群，zscore 保留相对幅度。外层常再接 rank/scale。 |
| `group_zscore` | `group_rank` | 已用 | 已用 | 组内标准化的两种形态；group_rank 组内均匀分布，对厚尾字段更稳。 |
| `ts_ir` | `divide(ts_mean, ts_std_dev)` | 已用 | 已用 | IR 定义即 mean/std，手写等价；分母近 0 时手写版需 +0.001 防爆。 |
| `ts_delta` | `subtract(x, ts_delay(x,n))` | 已用 | 已用 | 逐字等价。 |
| `ts_returns` | `divide(ts_delta(x,n), ts_delay(x,n))` | 未用 | 已用 | 近等价（百分比变动）；分母为 0/近 0 时注意。 |
| `ts_av_diff` | `subtract(x, ts_mean(x,n))` | 已用 | 已用 | 逐字等价（对均值的偏离）。 |
| `signed_power` | `sqrt` | 已用 | 未用 | x>=0 时 signed_power(x,0.5)=sqrt(x)；含负值数据必须用 signed_power 保号。 |
| `signed_power` | `power` | 已用 | 未用 | power(x,a) 不保号（负底数非整数幂出 NaN）；有符号字段一律 signed_power。 |
| `reverse` | `multiply(x, -1)` | 已用 | 已用 | 逐字等价（取负）。reverse 更可读。 |
| `inverse` | `divide(1, x)` | 未用 | 已用 | 逐字等价；x=0 均出 inf，建议配合 pasteurize。 |
| `sqrt` | `power(x, 0.5)` | 未用 | 未用 | x>=0 等价；含负值改 signed_power。 |
| `max` | `if_else(greater_equal(a,b), a, b)` | 未用 | 已用 | 逐元素等价；min 同理反向。 |
| `winsorize` | `tail` | 已用 | 未用 | 同为削峰：winsorize 按 std 倍数截断，tail 按分位/阈值；参数语义不同，换后需重调阈值。 |
| `group_neutralize` | `vector_neut` | 已用 | 已用 | 中性化两条路：按组去均值 vs 对向量回归取残差；vector_neut 更外科手术式，需给目标向量。 |
| `pasteurize` | `ts_backfill` | 未用 | 已用 | 数据卫生：pasteurize 清 inf/NaN（置 NaN 由平台处理）；ts_backfill 用历史值回填。目的相同、机制不同。 |
| `pasteurize` | `densify` | 未用 | 已用 | densify 把稀疏字段变稠密（前向填充语义）；与 pasteurize 常串联使用。 |
| `trade_when` | `if_else(cond, x, nan)` | 已用 | 已用 | 门控两形态：trade_when 有持仓状态（entry/exit 之间维持），if_else 是每日无状态掩码。trade_when 能改变换手结构（实证可过 CONCENTRATED_WEIGHT）。 |
| `hump` | `ts_target_tvr_hump` | 已用 | 未用 | 换手控制一族：hump 限制相邻日仓位变动；ts_target_tvr_hump 直接锚定目标换手。 |
| `ts_corr` | `ts_covariance` | 已用 | 未用 | 相关 vs 协方差，差一个标准化分母；语义等价、量纲不同。 |
| `quantile` | `bucket` | 已用 | 已用 | 同为离散化分桶；参数语义（分位驱动）略有差异。 |
| `vec_avg` | `reduce_avg` | 已用 | 未用 | 向量规约近似互换（vec_* 面向 vector 字段，reduce_* 通用）；同族 vec_max/min/sum ↔ reduce_max/min/sum。 |
| `scale` | `normalize` | 已用 | 已用 | 截面整形：scale 使 sum(|x|)=定值（权重塑形），normalize 去均值（可选除 std≈zscore）；目的不同勿盲换。 |
| `group_mean` | `group_sum` | 已用 | 未用 | 组内聚合，差一个组计数分母；group_sum/group_count=group_mean。 |
| `ts_arg_max` | `ts_arg_min` | 已用 | 未用 | 孪生：arg_max(reverse(x))=arg_min(x)。 |
| `less` | `greater` | 已用 | 已用 | 孪生比较：less(a,b)=greater(b,a)；less_equal/greater_equal 同理。 |
| `and` | `or` | 已用 | 已用 | 德摩根：and(a,b)=not(or(not a,not b))；条件组合时互换。 |


## 五、已提交 alpha 的惯用表达式模式（算子嵌套 bigram Top12）

| 排名 | 模式（外层←内层） | 次数 | 典型示例 |
|---|---|---|---|
| 1 | `multiply( rank( … ) )` | 59 | `add(multiply(rank(subtract(vec_avg(analyst_net_income_raised_count_one_week),vec_avg(analyst_net_income_downwa…` |
| 2 | `rank( ts_mean( … ) )` | 48 | `((rank(ts_delta(divide(ts_backfill(vec_avg(fnd72_pit_or_is_q_ebitda),120),ts_backfill(vec_avg(fnd72_pit_or_bs_…` |
| 3 | `ts_mean( ts_std_dev( … ) )` | 34 | `((rank(ts_delta(divide(ts_backfill(vec_avg(fnd72_pit_or_is_q_ebitda),120),ts_backfill(vec_avg(fnd72_pit_or_bs_…` |
| 4 | `abs( ts_mean( … ) )` | 34 | `group_rank(divide(subtract(ts_backfill(vec_avg(mean_flash_estimate_pretax_annual12), 22), ts_mean(ts_backfill(…` |
| 5 | `bucket( rank( … ) )` | 32 | `rank(group_neutralize(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_earnings_5, 22)), rank(long_term_f…` |
| 6 | `ts_std_dev( abs( … ) )` | 31 | `trade_when(greater(volume, adv20), trade_when(greater(ts_std_dev(divide(ts_backfill(shrt55_ss_shares,22),ts_ba…` |
| 7 | `ts_std_dev( vector_neut( … ) )` | 31 | `trade_when(greater(volume, adv20), trade_when(greater(ts_std_dev(divide(ts_backfill(shrt55_ss_shares,22),ts_ba…` |
| 8 | `add( multiply( … ) )` | 29 | `add(multiply(rank(subtract(vec_avg(analyst_net_income_raised_count_one_week),vec_avg(analyst_net_income_downwa…` |
| 9 | `group_neutralize( group_neutralize( … ) )` | 28 | `add(add(group_neutralize(quantile(subtract(ts_backfill(fnd86_earnings_score,66),ts_backfill(fnd86_price_moment…` |
| 10 | `add( add( … ) )` | 27 | `add(multiply(rank(subtract(vec_avg(analyst_net_income_raised_count_one_week),vec_avg(analyst_net_income_downwa…` |
| 11 | `group_neutralize( bucket( … ) )` | 26 | `add(add(group_neutralize(quantile(subtract(ts_backfill(fnd86_earnings_score,66),ts_backfill(fnd86_price_moment…` |
| 12 | `ts_mean( rank( … ) )` | 25 | `((rank(ts_delta(divide(ts_backfill(vec_avg(fnd72_pit_or_is_q_ebitda),120),ts_backfill(vec_avg(fnd72_pit_or_bs_…` |
