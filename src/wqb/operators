统计了7个REGULAR Alpha（每天前4个），在你可用的运算符中，共有14种运算符被使用，69种运算符未被使用。
'-'有两种含义分别是substract和revers, 此处统一为substrac

Category	Definition	Count	Scope	Level
Arithmetic	add(x, y, filter = false), x + y	2	COMBO,REGULAR,SELECTION	base
Arithmetic	multiply(x ,y, ... , filter=false), x * y	2	COMBO,REGULAR,SELECTION	base
Arithmetic	sign(x)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	subtract(x, y, filter=false), x - y	6	COMBO,REGULAR,SELECTION	base
Arithmetic	pasteurize(x)	0	COMBO,REGULAR	genius
Arithmetic	log(x)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	max(x, y, ..)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	abs(x)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	divide(x, y), x / y	0	COMBO,REGULAR,SELECTION	base
Arithmetic	min(x, y ..)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	signed_power(x, y)	2	COMBO,REGULAR,SELECTION	base
Arithmetic	inverse(x)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	sqrt(x)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	reverse(x)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	power(x, y)	0	COMBO,REGULAR,SELECTION	base
Arithmetic	densify(x)	0	COMBO,REGULAR	base
Logical	or(input1, input2)	0	COMBO,REGULAR,SELECTION	base
Logical	and(input1, input2)	0	COMBO,REGULAR,SELECTION	base
Logical	not(x)	0	COMBO,REGULAR,SELECTION	base
Logical	is_nan(input)	0	COMBO,REGULAR,SELECTION	base
Logical	input1 < input2	0	COMBO,REGULAR,SELECTION	base
Logical	input1 == input2	0	COMBO,REGULAR,SELECTION	base
Logical	input1 > input2	0	COMBO,REGULAR,SELECTION	base
Logical	if_else(input1, input2, input 3)	0	COMBO,REGULAR,SELECTION	base
Logical	input1!= input2	0	COMBO,REGULAR,SELECTION	base
Logical	input1 <= input2	0	COMBO,REGULAR,SELECTION	base
Logical	input1 >= input2	0	COMBO,REGULAR,SELECTION	base
Time Series	ts_corr(x, y, d)	0	COMBO,REGULAR	base
Time Series	ts_zscore(x, d)	7	COMBO,REGULAR	base
Time Series	ts_returns (x, d, mode = 1)	0	COMBO,REGULAR	genius
Time Series	ts_product(x, d)	0	COMBO,REGULAR	base
Time Series	ts_std_dev(x, d)	0	COMBO,REGULAR	base
Time Series	ts_backfill(x,lookback = d, k=1)	9	COMBO,REGULAR	base
Time Series	days_from_last_change(x)	0	COMBO,REGULAR	base
Time Series	last_diff_value(x, d)	0	COMBO,REGULAR	base
Time Series	ts_scale(x, d, constant = 0)	0	COMBO,REGULAR	base
Time Series	ts_step(1)	0	COMBO,REGULAR	base
Time Series	ts_sum(x, d)	0	COMBO,REGULAR	base
Time Series	ts_av_diff(x, d)	0	COMBO,REGULAR	base
Time Series	ts_kurtosis(x, d)	0	COMBO,REGULAR	genius
Time Series	ts_mean(x, d)	4	COMBO,REGULAR	base
Time Series	ts_arg_max(x, d)	0	COMBO,REGULAR	base
Time Series	ts_rank(x, d, constant = 0)	1	COMBO,REGULAR	base
Time Series	ts_ir(x, d)	0	COMBO,REGULAR	genius
Time Series	ts_delay(x, d)	0	COMBO,REGULAR	base
Time Series	ts_quantile(x,d, driver="gaussian" )	0	COMBO,REGULAR	base
Time Series	ts_count_nans(x ,d)	0	COMBO,REGULAR	base
Time Series	ts_covariance(y, x, d)	0	COMBO,REGULAR	base
Time Series	ts_decay_linear(x, d, dense = false)	1	COMBO,REGULAR	base
Time Series	ts_arg_min(x, d)	0	COMBO,REGULAR	base
Time Series	ts_regression(y, x, d, lag = 0, rettype = 0)	0	COMBO,REGULAR	base
Time Series	ts_max_diff(x, d)	0	COMBO,REGULAR	genius
Time Series	kth_element(x, d, k, ignore=“NaN”)	0	COMBO,REGULAR	base
Time Series	hump(x, hump = 0.01)	0	COMBO,REGULAR	base
Time Series	ts_delta(x, d)	0	COMBO,REGULAR	base
Time Series	ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)	0	COMBO,REGULAR	genius
Time Series	ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)	0	COMBO,REGULAR	genius
Cross Sectional	winsorize(x, std=4)	0	COMBO,REGULAR	base
Cross Sectional	rank(x, rate=2)	6	COMBO,REGULAR	base
Cross Sectional	zscore(x)	0	COMBO,REGULAR	base
Cross Sectional	scale(x, scale=1, longscale=1, shortscale=1)	4	COMBO,REGULAR	base
Cross Sectional	normalize(x, useStd = false, limit = 0.0)	0	COMBO,REGULAR	base
Cross Sectional	quantile(x, driver = gaussian, sigma = 1.0)	0	COMBO,REGULAR	base
Vector	vec_min(x)	0	COMBO,REGULAR	genius
Vector	vec_count(x)	0	COMBO,REGULAR	genius
Vector	vec_sum(x)	0	COMBO,REGULAR	base
Vector	vec_max(x)	0	COMBO,REGULAR	genius
Vector	vec_avg(x)	2	COMBO,REGULAR	base
Vector	vec_stddev(x)	0	COMBO,REGULAR	genius
Vector	vec_range(x)	0	COMBO,REGULAR	genius
Transformational	bucket(rank(x), range=“0, 1, 0.1”, skipBoth=False, NaNGroup=False) or bucket(rank(x), buckets = “2,5,6,7,10”, skipBoth=False, NaNGroup=False)	0	COMBO,REGULAR	base
Transformational	tail(x, lower = 0, upper = 0, newval = 0)	0	COMBO,REGULAR	genius
Transformational	trade_when(x, y, z)	0	COMBO,REGULAR	base
Group	group_mean(x, weight, group)	0	COMBO,REGULAR	base
Group	group_rank(x, group)	3	COMBO,REGULAR	base
Group	group_backfill(x, group, d, std = 4.0)	0	COMBO,REGULAR	base
Group	group_scale(x, group)	0	COMBO,REGULAR	base
Group	group_count(x, group)	0	COMBO,REGULAR	genius
Group	group_zscore(x, group)	2	COMBO,REGULAR	base
Group	group_std_dev(x, group)	0	COMBO,REGULAR	genius
Group	group_sum(x, group)	0	COMBO,REGULAR	genius
Group	group_neutralize(x, group)	0	COMBO,REGULAR	base
Group	group_cartesian_product(g1, g2)	0	COMBO,REGULAR	genius
