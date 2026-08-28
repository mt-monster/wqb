# GEM dry-run 提示词成品 v3 — KOR model25 D1 TOP600

> 2026-08-25，字段目录紧凑化改版后重新生成。链路同 v1/v2：真实平台数据 + DB KB priors，
> 仅跳过 call_moonshot。

## 体积对比

| 块 | 旧 | 新 | 节省 |
|---|---|---|---|
| allowed_operators（v2 已改） | 14987 chars（repr） | 12970 chars | 13.5% |
| user prompt（v3：字段目录去 indent + 纯文本行） | 95658 chars | 48915 chars | 48.9% |
| system prompt 全长 | 26,325 chars（v1） | 24407 chars | — |

## 新字段目录格式（前 4 行 + 头部）

```text
{"instructions": {"output_format": "Markdown Concept blocks only (no SKILL dump, no code fences around the whole report).", "implementation_examples": "Each Implementation Example must be a template with {variable} placeholders. Bind placeholders to the distinctive suffix of the 2–3 fields named in **Fields**. Do not emit a generic {score}/{value}/{field} that matches the whole catalog.", "no_code_fences": true, "do_not_invent_placeholders": true, "min_multi_field_concepts": 3}, "dataset_context": {"dataset_id": "model25", "dataset_name": "Earnings Quality", "dataset_description": "This dataset provides a comprehensive stock ranking model that integrates both valuation and momentum factors. It combines intrinsic and relative valuation metrics with analyst estimate revisions and price momentum signals, offering percentile ranks at global, regional, sector, and industry levels. The model leverages historical performance data, including decile spread returns, to identify stocks with attractive value and strong momentum characteristics. By blending these factors, the dataset helps investors and quantitative researchers predict future price movements and construct portfolios that are more likely to outperform market benchmarks. Its multi-factor approach is particularly useful for screening, backtesting, and systematic investment strategies.", "category": "model", "region": "KOR", "delay": 1, "universe": "TOP600", "field_count": 554}, "field_format": "fields are listed one per line after this JSON header as: field_id :: description [cov=x.xx]; all fields type=MATRIX"}

analyst_recommendation_score_5 :: Score reflecting changes in analyst buy, hold, or sell recommendations.  [cov=1.00]
analyst_revision_composite_score :: Composite score summarizing analyst estimate revisions across all components.  [cov=1.00]
analyst_revision_model_score :: Overall score from the analyst revision model for a security.  [cov=1.00]
...（共 554 行字段）
```

截断时按 coverage 降序保留（原为任意 head 减半），头部 field_format 会注明
"catalog truncated to top K of N fields by coverage"。

## SYSTEM PROMPT（全文）

```text
You design WorldQuant BRAIN Regular Alpha CONCEPTS, not field×operator wrappers.

For EACH concept, answer in this order before writing a template:
1. Mechanism: who vs who / what surprise / what risk is priced
2. Why it should predict next-period returns in THIS region
3. Exact field ids from the provided list (2–3 fields, not a suffix token)
4. Direction: high value means long or short
5. Failure mode: when this collapses into a crowded residual

FORBIDDEN:
- rank({field}) or ts_zscore({field}, N) as a standalone concept
- "for each field, wrap with an operator"
- placeholders that are only the last token of every field
- inventing field ids

REQUIRED (at least 8 concepts, of which at least 3 are multi-field):
- disagreement / residual / change-vs-level / intensity-weighted
- If a win recipe is provided, emit 1 concept that follows that mix shape
  using THIS dataset's fields as one leg (still {placeholder} syntax)

OUTPUT each idea as:
**Concept**: <mechanism name>
- **Mechanism**: <1–2 sentences>
- **Fields**: `field_id_1`, `field_id_2`
- **Implementation Example**: `rank(subtract(ts_backfill({field_suffix_1}, 66), ts_backfill({field_suffix_2}, 66)))`
- **Direction**: ...
- **Why not crowded**: ...

Implementation Example MUST be a Python format template using {variable}.
{variable} should be the distinctive suffix of the intended field (or the full id
if short). Do not emit a generic {score}/{value}/{field} that matches everything.


Economic primitives for this category:
- industry residual: group_zscore so the factor is not the sector bet
- quality minus yield: a slow fundamental residual, not the raw score
- invert only when the economic story is crowding or mean-reversion
- never ship a lone rank(model_score) as a concept
Win recipes (copy the MECHANISM, replace the legs with this dataset's fields):
- 评级修正×SH 跨数据集跨周期混合: skeleton=rank(add(multiply(2, rank(change_6m_rating_revision)), rank(short_horizon_hedge3_quantile1_5d_pred))); evidence=registry KOR-RATING-REV-SH-MIX-WIN；88lr21xo / A1lb2KpR; settings=TOP600 D1 STATISTICAL decay4 trunc0.08
- PV 主导 + 表达式层 sector 中性化: skeleton=model25 global_value_momentum_percentile_float 等 PV/模型字段，设置 STATISTICAL + group_neutralize(sector); evidence=registry KOR-W113-PVDOM-SECTOR-WIN；wpjJK60l; settings=None
- T-KB-01 慢×快跨周期混合: skeleton=rank(add(multiply(w_s, rank(SLOW_FIELD)), multiply(w_f, rank(FAST_FIELD)))); iron_law=必须跨周期/跨数据源；同周期互混零增量
- T-KB-02 镜像反转翻案: skeleton=subtract(0, rank(x)) 或 scale(-rank(x)); iron_law=探针批 |sh|≥1.0 强负 → 下一批必做镜像反转，不是判死
Do NOT emit concepts in these dead families:
- value/quality 与评级修正在本区 book 已饱和（KOR-VALUE-QUALITY-SEEDS / KOR-MLPROJ-RATING-SH-SATURATED prod 0.897-0.929）
- 稀疏事件流 CW 墙：论坛/行为/AI equity 三族 CW 0.85-1.0 结构性 FAIL
- 情感族全灭（news_sentiment_transfer / news79）
- 图表形态三连死（chart_cnn / continuation / pattern_scores 首探）
- 模型预测类二次动量是噪声；MSM 5d 组合族 fitness 天花板 0.99 / 2y 1.24
- 配方家族扩展天花板：主导腿不变时 SELF ≥0.9 可设计前预判（wave104/E10 四次实证）
- other455 三连死（group cluster / network embedding / revision cluster）
- T-KB-01 慢×快跨周期混合: 同周期慢信号互混全灭（LT）
- T-KB-06 多期限共识加权: MSM 5d 组合族 fitness 0.99 / 2y 1.24 天花板（短周期单数据集边界）
- T-KB-07 四向价值结构: 移植全灭 0.32-0.60（PREDSTARMINE-VALUE-DEAD）
- T-KB-09 【负模板】单字段裸探针: 10+ 数据集首探 max|sh| 0.2-0.52
- T-KB-10 【负模板】稀疏事件流: 论坛/行为/AI equity 三族 CW 0.85-1.0

"allowed_operators": [
{"name": "add", "category": "Arithmetic", "definition": "add(x, y, filter = false), x + y", "description": "Adds two or more inputs element wise. Set filter=true to treat NaNs as 0 before summing."},
{"name": "multiply", "category": "Arithmetic", "definition": "multiply(x ,y, ... , filter=false), x * y", "description": "Multiplies two or more inputs element wise. Set filter=true to treat NaNs as 0 before multiplication"},
{"name": "sign", "category": "Arithmetic", "definition": "sign(x)", "description": "Returns the sign of a number: +1 for positive, -1 for negative, and 0 for zero. If the input is NaN, returns NaN. Input: Value of 7 instruments at day t: (2, -3…"},
{"name": "subtract", "category": "Arithmetic", "definition": "subtract(x, y, filter=false), x - y", "description": "Subtracts inputs left to right: x ? y ? … Supports two or more inputs. Set filter=true to treat NaNs as 0 before subtraction."},
{"name": "pasteurize", "category": "Arithmetic", "definition": "pasteurize(x)", "description": "Set to NaN if x is INF or if the underlying instrument is not in the Alpha universe. This operator may help reduce outliers. Input: Value of 7 instruments at da…"},
{"name": "log", "category": "Arithmetic", "definition": "log(x)", "description": "Calculates the natural logarithm of the input value. Commonly used to transform data that has positive values."},
{"name": "max", "category": "Arithmetic", "definition": "max(x, y, ..)", "description": "Maximum value of all inputs. At least 2 inputs are required"},
{"name": "abs", "category": "Arithmetic", "definition": "abs(x)", "description": "Returns the absolute value of a number, removing any negative sign."},
{"name": "divide", "category": "Arithmetic", "definition": "divide(x, y), x / y", "description": "Returns x divided by y (x / y). Note: dividing by zero raises an error; to avoid it, use divide(x, add(y, 0.0001)); adding a small epsilon to the denominator pr…"},
{"name": "min", "category": "Arithmetic", "definition": "min(x, y ..)", "description": "Minimum value of all inputs. At least 2 inputs are required"},
{"name": "signed_power", "category": "Arithmetic", "definition": "signed_power(x, y)", "description": "x raised to the power of y such that final result preserves sign of x"},
{"name": "inverse", "category": "Arithmetic", "definition": "inverse(x)", "description": "Returns the reciprocal of x (1 / x). Note: errors when x = 0; to avoid it, use inverse(add(x, 0.0001)); adding a small epsilon prevents divide-by-zero errors."},
{"name": "sqrt", "category": "Arithmetic", "definition": "sqrt(x)", "description": "Returns the non-negative square root of x. Equivalent to power(x, 0.5). Note: for x < 0 the result is undefined; to retain the sign of x, use signed_power(x, 0.…"},
{"name": "reverse", "category": "Arithmetic", "definition": "reverse(x)", "description": "- x"},
{"name": "power", "category": "Arithmetic", "definition": "power(x, y)", "description": "Returns x raised to the power of y (x ^ y). Note: power(x, y) can drop the sign of x when y is non-integer; use signed_power(x, y) to preserve the sign of x."},
{"name": "densify", "category": "Arithmetic", "definition": "densify(x)", "description": "Converts a grouping field of many buckets into lesser number of only available buckets so as to make working with grouping fields computationally efficient"},
{"name": "or", "category": "Logical", "definition": "or(input1, input2)", "description": "Returns 1 if either input is true (either input1 or input2 has a value of 1), otherwise it returns 0."},
{"name": "and", "category": "Logical", "definition": "and(input1, input2)", "description": "Returns 1 ('true') if both inputs are 1 ('true'). Otherwise, returns 0 ('false')."},
{"name": "not", "category": "Logical", "definition": "not(x)", "description": "Returns the logical negation of x. Returns 0 when x is 1 (‘true’) and 1 when x is 0 (‘false’)."},
{"name": "is_nan", "category": "Logical", "definition": "is_nan(input)", "description": "If (input == NaN) return 1 else return 0"},
{"name": "less", "category": "Logical", "definition": "input1 < input2", "description": "Returns 1 ('true') if input1 is a smaller than input2. Otherwise, returns 0 ('false')."},
{"name": "equal", "category": "Logical", "definition": "input1 == input2", "description": "Returns 1 ('true') if input1 and input2 are the same. Otherwise, returns 0 ('false')."},
{"name": "greater", "category": "Logical", "definition": "input1 > input2", "description": "Returns 1 ('true') if input1 is a larger than input2. Otherwise, returns 0 ('false')."},
{"name": "if_else", "category": "Logical", "definition": "if_else(input1, input2, input 3)", "description": "The if_else operator returns one of two values based on a condition. If the condition is true, it returns the first value; if false, it returns the second value…"},
{"name": "not_equal", "category": "Logical", "definition": "input1!= input2", "description": "Returns 1 ('true') if input1 and input2 are different numbers. Otherwise, returns 0 ('false')."},
{"name": "less_equal", "category": "Logical", "definition": "input1 <= input2", "description": "Returns 1 ('true') if input1 is a smaller or the same as input2. Otherwise, returns 0 ('false')."},
{"name": "greater_equal", "category": "Logical", "definition": "input1 >= input2", "description": "Returns 1 ('true') if input1 is a larger or the same as input2. Otherwise, returns 0 ('false')."},
{"name": "ts_corr", "category": "Time Series", "definition": "ts_corr(x, y, d)", "description": "Calculates the Pearson correlation between two variables, x and y, over the past d days, showing how closely they move together."},
{"name": "ts_returns", "category": "Time Series", "definition": "ts_returns (x, d, mode = 1)", "description": "Returns the relative change in the x value"},
{"name": "ts_product", "category": "Time Series", "definition": "ts_product(x, d)", "description": "Returns the product of the values of x over the past d days. Useful for calculating geometric means and compounding returns or growth rates."},
{"name": "ts_std_dev", "category": "Time Series", "definition": "ts_std_dev(x, d)", "description": "Calculates the standard deviation of a data series x over the past d days, measuring how much the values deviate from their mean during that period."},
{"name": "ts_backfill", "category": "Time Series", "definition": "ts_backfill(x,lookback = d, k=1)", "description": "Replaces missing (NaN) values in a time series with the most recent valid value from a specified lookback window, improving data coverage and reducing risk from…"},
{"name": "days_from_last_change", "category": "Time Series", "definition": "days_from_last_change(x)", "description": "Calculates the number of days since the last change in the value of a given variable."},
{"name": "last_diff_value", "category": "Time Series", "definition": "last_diff_value(x, d)", "description": "Returns the most recent value of x from the past d days that is different from the current value of x."},
{"name": "ts_step", "category": "Time Series", "definition": "ts_step(1)", "description": "Returns a counter of days, incrementing by one each day."},
{"name": "ts_sum", "category": "Time Series", "definition": "ts_sum(x, d)", "description": "Sum values of x for the past d days."},
{"name": "ts_av_diff", "category": "Time Series", "definition": "ts_av_diff(x, d)", "description": "Calculates the difference between a value and its mean over a specified period, ignoring NaN values in the mean calculation. In short, it returns x – ts_mean(x,…"},
{"name": "ts_kurtosis", "category": "Time Series", "definition": "ts_kurtosis(x, d)", "description": "Returns kurtosis of x for the last d days"},
{"name": "ts_mean", "category": "Time Series", "definition": "ts_mean(x, d)", "description": "Calculates the simple average (mean) value of a variable x over the past d days."},
{"name": "ts_arg_max", "category": "Time Series", "definition": "ts_arg_max(x, d)", "description": "Returns the number of days since the maximum value occurred in the last d days of a time series. If today's value is the maximum, returns 0; if it was yesterday…"},
{"name": "ts_ir", "category": "Time Series", "definition": "ts_ir(x, d)", "description": "Return information ratio ts_mean(x, d) / ts_std_dev(x, d)"},
{"name": "ts_delay", "category": "Time Series", "definition": "ts_delay(x, d)", "description": "Returns the value of a variable x from d days ago. Use this operator to access historical data points by specifying the desired time lag in days."},
{"name": "ts_quantile", "category": "Time Series", "definition": "ts_quantile(x,d, driver=\"gaussian\" )", "description": "Calculates the ts_rank of the input and transforms it using the inverse cumulative distribution function (quantile function) of a specified probability distribu…"},
{"name": "ts_count_nans", "category": "Time Series", "definition": "ts_count_nans(x ,d)", "description": "Counts the number of missing (NaN) values in a data series over a specified number of days."},
{"name": "ts_covariance", "category": "Time Series", "definition": "ts_covariance(y, x, d)", "description": "Calculates the covariance between two time-series variables, y and x, over the past d days. Useful for measuring how two variables move together within a specif…"},
{"name": "ts_decay_linear", "category": "Time Series", "definition": "ts_decay_linear(x, d, dense = false)", "description": "Applies a linear decay to time-series data over a set number of days, smoothing the data by averaging recent values and reducing the impact of older or missing…"},
{"name": "ts_arg_min", "category": "Time Series", "definition": "ts_arg_min(x, d)", "description": "Returns the number of days since the minimum value occurred in a time series over the past d days. If today's value is the minimum, returns 0; if it was yesterd…"},
{"name": "ts_regression", "category": "Time Series", "definition": "ts_regression(y, x, d, lag = 0, rettype = 0)", "description": "Returns various parameters related to regression function"},
{"name": "ts_max_diff", "category": "Time Series", "definition": "ts_max_diff(x, d)", "description": "Returns x - ts_max(x, d)"},
{"name": "kth_element", "category": "Time Series", "definition": "kth_element(x, d, k, ignore=“NaN”)", "description": "Returns the K-th value from a time series by looking back over a specified number of (‘d’) days, with the option to ignore certain values. Commonly used for bac…"},
{"name": "hump", "category": "Time Series", "definition": "hump(x, hump = 0.01)", "description": "Limits amount and magnitude of changes in input (thus reducing turnover)"},
{"name": "ts_delta", "category": "Time Series", "definition": "ts_delta(x, d)", "description": "Calculates the difference between a value and its delayed version over a specified period. Useful for measuring changes or momentum in time-series data."},
{"name": "ts_target_tvr_decay", "category": "Time Series", "definition": "ts_target_tvr_decay(x, lambda_min=0, lambda_max=1, target_tvr=0.1)", "description": "Tune \"ts_decay\" to have a turnover equal to a certain target, with optimization weight range between lambda_min, lambda_max"},
{"name": "ts_target_tvr_hump", "category": "Time Series", "definition": "ts_target_tvr_hump(x, lambda_min=0, lambda_max=1, target_tvr=0.1)", "description": "Tune \"hump\" to have a turnover equal to a certain target with optimization weight range between lambda_min, lambda_max."},
{"name": "winsorize", "category": "Cross Sectional", "definition": "winsorize(x, std=4)", "description": "Winsorize limits values in a data to within a specified number of standard deviations from the mean, reducing the impact of extreme outliers. Note: recommended…"},
{"name": "quantile", "category": "Cross Sectional", "definition": "quantile(x, driver = gaussian, sigma = 1.0)", "description": "Ranks and shifts a vector of Alpha values, then applies a chosen statistical distribution (gaussian, cauchy, or uniform) to reduce outliers. The sigma parameter…"},
{"name": "bucket", "category": "Transformational", "definition": "bucket(rank(x), range=“0, 1, 0.1”, skipBoth=False, NaNGroup=False) or bucket(rank(x), buckets = “2,5,6,7,10”, skipBoth=False, NaNGroup=False)", "description": "The bucket operator creates custom groups by dividing data into buckets (ranges) based on ranked values of any data field. These buckets can then be used with g…"},
{"name": "tail", "category": "Transformational", "definition": "tail(x, lower = 0, upper = 0, newval = 0)", "description": "If (x > lower AND x < upper) return newval, else return x. Lower, upper, newval should be constants"},
{"name": "trade_when", "category": "Transformational", "definition": "trade_when(x, y, z)", "description": "The trade_when operator changes Alpha values only when a specific condition is met, keeps previous values otherwise, and can close positions by assigning NaN un…"}
]
"allowed_placeholders": ["percentile", "rank_float", "momentum_percentile", "percentile_float", "price_momentum_percentile", "credit_risk_percentile", "ratio_percentile", "risk_percentile", "value_momentum_percentile_float", "value_momentum_percentile", "momentum_percentile_float", "ratio_percentile_float", "industry_rank_float", "region_rank_float", "industry_percentile", "relative_valuation_percentile_float", "term_price_momentum_percentile", "relative_valuation_percentile", "valuation_percentile_float", "term_momentum_percentile", "sector_rank_float", "global_rank_float", "valuation_percentile", "region_percentile", "sector_percentile", "relative_score", "global_rank", "region_rank", "sector_rank", "five_year_eps_growth_rate", "year_eps_growth_rate_iv", "intrinsic_value_industry_percentile", "relative_score_float_2", "year_eps_growth_rate", "eps_growth_rate_iv", "value_industry_percentile", "relative_score_backfill", "relative_score_float", "eps_growth_rate", "growth_rate_iv", "score_float_2", "eps_cagr_3", "projection_currency", "global_percentile", "component_score", "score_backfill", "industry_rank", "country_rank", "score_float", "growth_rate", "combined_pd", "float_2", "rate_iv", "year_10", "year_11", "ratio_2", "year_4", "rate_2", "cagr_3", "year_3", "year_6", "year_8", "currency", "backfill", "earnings", "intrinsic_value_sector_percentile_float", "to_intrinsic_value_industry_percentile", "to_intrinsic_value_sector_percentile", "intrinsic_value_industry_rank_float", "book_value_relative_score_backfill", "ccr_credit_combined_industry_rank", "intrinsic_value_region_rank_float", "intrinsic_value_sector_rank_float", "ccr_credit_combined_country_rank", "ccr_credit_combined_global_rank", "starmine_ccr_credit_combined_pd", "ccr_credit_combined_region_rank", "ccr_credit_combined_sector_rank", "state_annual_dividend_per_share", "to_ebitda_relative_score_float", "to_sales_relative_score_float", "state_dividend_payout_ratio_2", "yield_relative_score_float_2", "ratio_relative_score_float_2", "to_book_value_relative_score", "state_earnings_growth_rate_2", "quality_score_change_1_day", "to_intrinsic_value_ratio_4", "dividend_per_share_year_10", "dividend_per_share_year_11", "dividend_per_share_year_15", "dividend_per_share_year_1", "dividend_per_share_year_2", "dividend_per_share_year_3", "dividend_per_share_year_4", "dividend_per_share_year_6", "dividend_per_share_year_8", "dividend_per_share_year_9", "implied_10yr_eps_cagr_3", "implied_10yr_eps_cagr_4", "implied_5yr_eps_cagr_3", "intrinsicvalue_industry_rank_float", "dividends_sum_projection_currency", "intrinsic_value_region_percentile", "intrinsic_value_sector_percentile", "risk_default_probability_percent", "intrinsicvalue_region_rank_float", "cashflow_ratio_percentile_float", "earnings_ratio_percentile_float", "yield_relative_score_backfill", "ebitda_ratio_percentile_float", "credit_combined_industry_rank", "value_relative_score_backfill", "value_sector_percentile_float", "valuation_industry_rank_float", "sales_ratio_percentile_float", "credit_combined_country_rank", "momentum_industry_rank_float", "ebitda_relative_score_float", "price_momentum_percentile_4", "credit_combined_global_rank", "credit_combined_region_rank", "credit_combined_sector_rank", "valuation_global_rank_float", "valuation_region_rank_float", "valuation_sector_rank_float", "sales_relative_score_float", "state_dividend_payout_rate", "momentum_global_rank_float", "momentum_region_rank_float", "momentum_sector_rank_float", "valuation_discount_rate_2", "value_industry_rank_float", "book_value_relative_score", "dividend_yield_rank_float", "price_cashflow_rank_float", "annual_dividend_per_share", "to_ebitda_relative_score", "to_sales_relative_score", "value_region_rank_float", "value_sector_rank_float", "intrinsic_value_ratio_4", "dividend_payout_ratio_2", "yield_relative_score_2", "ccr_credit_combined_pd", "earnings_growth_rate_2", "price_book_rank_float", "score_change_1_day", "forward_pe_ratio_2", "forward_pe_ratio_3", "per_share_year_10", "per_share_year_11", "per_share_year_15", "per_share_year_1", "per_share_year_2", "per_share_year_3", "per_share_year_4", "per_share_year_6", "per_share_year_8", "per_share_year_9", "10yr_eps_cagr_3", "10yr_eps_cagr_4", "5yr_eps_cagr_3", "valuation_industry_percentile", "momentum_industry_percentile", "default_probability_percent", "valuation_global_percentile", "valuation_region_percentile", "valuation_sector_percentile", "efficiency_component_score", "intrinsicvalue_region_rank", "intrinsicvalue_sector_rank", "momentum_global_percentile", "momentum_region_percentile", "momentum_sector_percentile", "revisions_preferred_score", "revisions_secondary_score", "value_projection_currency", "cashflow_ratio_percentile", "earnings_ratio_percentile", "revision_composite_score", "revision_percentile_rank", "revisions_revenue_score", "sum_projection_currency", "ebitda_ratio_percentile", "value_region_percentile", "value_sector_percentile", "sector_percentile_float", "to_intrinsicvalue_ratio", "recommendation_score_5", "yield_percentile_float", "sales_ratio_percentile", "combined_industry_rank", "quality_score_current", "ebitda_relative_score", "momentum_percentile_4", "momentum_percentile_2", "combined_country_rank", "book_ratio_percentile", "state_earnings_growth", "revision_model_score", "rate_valuation_model", "sales_relative_score", "combined_global_rank", "combined_region_rank", "combined_sector_rank", "value_relative_score", "dividend_payout_rate", "state_year_dividends", "price_cashflow_rank", "cashflow_rank_float", "price_earnings_rank", "state_year_earnings", "credit_combined_pd", "buyback_yield_rank", "ccr_implied_rating", "dividend_per_share", "quality_score_raw", "ccr_industry_rank", "relative_score_2", "yield_rank_float", "ccr_country_rank", "discount_rate_2", "earnings_fy10_4", "earnings_fy11_3", "earnings_fy12_3", "earnings_fy14_3", "earnings_fy15_3", "book_rank_float", "ccr_combined_pd", "ccr_global_rank", "ccr_region_rank", "ccr_sector_rank", "eq_history_v10", "eq_history_v11", "eq_history_v12", "eq_history_v13", "earnings_fy1_3", "earnings_fy2_3", "earnings_fy3_4", "earnings_fy4_4", "earnings_fy5_4", "earnings_fy6_4", "earnings_fy7_3", "earnings_fy8_4", "earnings_fy9_3", "payout_ratio_2", "10yr_eps_cagr", "eq_history_v9", "value_ratio_4", "share_year_10", "share_year_11", "share_year_15", "growth_rate_2", "change_1_day", "share_year_1", "share_year_2", "share_year_3", "share_year_4", "share_year_6", "share_year_8", "share_year_9", "base_year_4", "eq_rlev_v10", "eq_rlev_v11", "eq_rlev_v12", "eq_rliq_v10", "eq_rliq_v11", "eq_rliq_v12", "eps_year_10", "eps_year_11", "eps_year_12", "eps_year_13", "eps_cagr_4", "eq_cfs_v10", "eq_cfs_v11", "eq_cfs_v12", "eq_cfs_v13", "eq_cfs_v14", "eq_cfs_v15", "eq_cfs_v16", "eq_cfs_v17", "eq_cfs_v18", "eq_cfs_v19", "eq_rlev_v5", "eq_rlev_v6", "eq_rlev_v7", "eq_rlev_v8", "eq_rlev_v9", "eq_rliq_v5", "eq_rliq_v6", "eq_rliq_v7", "eq_rliq_v8", "eq_rliq_v9", "eps_year_3", "eps_year_6", "eps_year_7", "eps_year_8", "pe_ratio_2", "pe_ratio_3"]

REGION PRIORS (empirical knowledge from prior campaigns in KOR - treat as strong hints for directionality and field selection):
---
    - "分析师评级修正 × SH（shortinterest/holders）混合（2 颗 ACTIVE 实证）"
---
- 白名单只留：绿榜（analyst/insiders/pv）+ status=untried 新集；
- 金字塔配额冲突时**优先 analyst 族上提**（实证有效面），tier_note 标 `pyramid_quota_kor`；
- 红榜数据集一律不进白名单，即使用户点名——先提示死路 rule 出处（matrix 硬规则 2）。
- 四大红灯族 + GLB emotion：生成阶段直接排除，不抱"换参数复活"幻想。
- 事件类数据集（earnings 等）：优先生成 `ts_event_*` 裸 rank 表达式，且预设 CW 必查。

CRITICAL OUTPUT RULES (to ensure implement_idea.py can generate expressions):
- Every Implementation Example MUST be a Python format template using {variable}.
- Every {variable} MUST come from the allowed_placeholders list provided in user content.
- When you implement ideas, ONLY use operators from allowed_operators provided.
- Do NOT include dataset codes/prefixes/horizons in {variable} (suffix-only).
- If you show raw field ids in tables, use backticks `like_this`, NOT {braces}.
- Include these metadata lines verbatim somewhere near the top:
  **Dataset**: <dataset_id>
  **Region**: <region>
  **Delay**: <delay>
```

## USER PROMPT（全文：紧凑 JSON 头 + 字段行）

```text
{"instructions": {"output_format": "Markdown Concept blocks only (no SKILL dump, no code fences around the whole report).", "implementation_examples": "Each Implementation Example must be a template with {variable} placeholders. Bind placeholders to the distinctive suffix of the 2–3 fields named in **Fields**. Do not emit a generic {score}/{value}/{field} that matches the whole catalog.", "no_code_fences": true, "do_not_invent_placeholders": true, "min_multi_field_concepts": 3}, "dataset_context": {"dataset_id": "model25", "dataset_name": "Earnings Quality", "dataset_description": "This dataset provides a comprehensive stock ranking model that integrates both valuation and momentum factors. It combines intrinsic and relative valuation metrics with analyst estimate revisions and price momentum signals, offering percentile ranks at global, regional, sector, and industry levels. The model leverages historical performance data, including decile spread returns, to identify stocks with attractive value and strong momentum characteristics. By blending these factors, the dataset helps investors and quantitative researchers predict future price movements and construct portfolios that are more likely to outperform market benchmarks. Its multi-factor approach is particularly useful for screening, backtesting, and systematic investment strategies.", "category": "model", "region": "KOR", "delay": 1, "universe": "TOP600", "field_count": 554}, "field_format": "fields are listed one per line after this JSON header as: field_id :: description [cov=x.xx]; all fields type=MATRIX"}

analyst_recommendation_score_5 :: Score reflecting changes in analyst buy, hold, or sell recommendations.  [cov=1.00]
analyst_revision_composite_score :: Composite score summarizing analyst estimate revisions across all components.  [cov=1.00]
analyst_revision_model_score :: Overall score from the analyst revision model for a security.  [cov=1.00]
analyst_revision_percentile_rank :: Percentile rank of a security based on analyst revision model output.  [cov=1.00]
analyst_revisions_preferred_score :: Score reflecting analyst estimate revisions and predicted surprises for preferred earnings measures.  [cov=1.00]
analyst_revisions_revenue_score :: Score reflecting analyst estimate revisions and predicted surprises for revenue.  [cov=1.00]
analyst_revisions_secondary_score :: Score reflecting analyst estimate revisions for secondary earnings measures such as EBITDA.  [cov=1.00]
buyback_yield_percentile :: Percentile ranking for share buyback yield.  [cov=1.00]
buyback_yield_percentile_float :: Percentile ranking for share buyback yield as a float.  [cov=1.00]
buyback_yield_relative_score_float_2 :: Relative score for share buyback yield as a floating-point value.  [cov=1.00]
cagr_base_year_4 :: Base year used for calculating compound annual growth rates in projections.  [cov=0.82]
country_credit_risk_percentile :: Percentile rank of a company's credit risk compared to country peers.  [cov=1.00]
credit_risk_default_probability_percent :: Estimated probability of default for a company over the next year, expressed as a percent.  [cov=1.00]
discount_rate_valuation_model :: Discount rate used in intrinsic value calculation.  [cov=0.82]
discounted_dividends_sum_projection_currency :: Sum of discounted future dividends in the currency used for projections.  [cov=0.82]
dividend_yield_relative_score_2 :: Relative score for dividend yield compared to global peers.  [cov=0.74]
dividend_yield_relative_score_backfill :: Relative score for dividend yield compared to global peers (backfill version).  [cov=0.74]
earnings_quality_score_change_1_day :: Change in the earnings quality region rank over one day.  [cov=1.00]
earnings_quality_score_current :: Current region-relative percentile ranking for earnings quality.  [cov=1.00]
earnings_quality_score_raw :: Raw region-relative percentile ranking for earnings quality before normalization.  [cov=1.00]
ev_ebitda_ratio_percentile :: Percentile ranking for enterprise value to EBITDA ratio.  [cov=1.00]
ev_ebitda_ratio_percentile_float :: Percentile ranking for enterprise value to EBITDA ratio as a float.  [cov=1.00]
ev_sales_ratio_percentile :: Percentile ranking for enterprise value to sales ratio.  [cov=1.00]
ev_sales_ratio_percentile_float :: Percentile ranking for enterprise value to sales ratio as a float.  [cov=1.00]
ev_to_ebitda_relative_score :: Relative score for enterprise value to EBITDA ratio compared to global peers.  [cov=1.00]
ev_to_ebitda_relative_score_float :: Relative score for enterprise value to EBITDA ratio as a floating-point value.  [cov=1.00]
ev_to_sales_relative_score :: Relative score for enterprise value to sales ratio compared to global peers.  [cov=1.00]
ev_to_sales_relative_score_float :: Relative score for enterprise value to sales ratio as a floating-point value.  [cov=1.00]
exclusions_component_score :: Percentile score for exclusions-based factors in the earnings quality model.  [cov=1.00]
forward_10yr_eps_cagr :: Compound annual growth rate of earnings per share over the next 10 years.  [cov=0.82]
forward_five_year_eps_growth_rate :: Compound annual growth rate of projected earnings per share over the next five years.  [cov=0.82]
forward_five_year_eps_growth_rate_iv :: Compound annual growth rate of projected earnings per share over the next five years from intrinsic value model.  [cov=0.82]
forward_ten_year_eps_growth_rate_iv :: Compound annual growth rate of projected earnings per share over the next ten years from intrinsic value model.  [cov=0.82]
global_credit_risk_percentile :: Global percentile rank of a company's credit risk score.  [cov=1.00]
global_momentum_percentile :: Global percentile ranking for price momentum score.  [cov=1.00]
global_price_momentum_percentile_4 :: Global percentile ranking for a stock's price momentum score.  [cov=1.00]
global_value_momentum_percentile :: Global percentile ranking for a stock's value-momentum score.  [cov=1.00]
global_value_momentum_percentile_float :: Global value-momentum percentile score as a floating-point value.  [cov=1.00]
industry_credit_risk_percentile :: Industry-relative percentile rank of a company's credit risk score.  [cov=1.00]
industry_momentum_percentile_2 :: Percentile score for price momentum relative to industry peers.  [cov=1.00]
industry_price_momentum_percentile :: Percentile rank for price momentum compared to industry peers.  [cov=1.00]
industry_relative_valuation_percentile :: Percentile ranking of a stock's relative valuation score compared to industry peers.  [cov=1.00]
industry_relative_valuation_percentile_float :: Industry-relative valuation percentile score as a floating-point value.  [cov=1.00]
industry_value_momentum_percentile :: Industry-relative value-momentum percentile score.  [cov=1.00]
industry_value_momentum_percentile_float :: Industry-relative value-momentum percentile score as a floating-point value.  [cov=1.00]
intrinsic_valuation_discount_rate_2 :: Discount rate used in the intrinsic valuation model for present value calculations.  [cov=0.82]
intrinsic_value_projection_currency :: Intrinsic value of the company expressed in the projection currency.  [cov=0.82]
long_term_momentum_percentile :: Percentile score for long-term price momentum.  [cov=1.00]
long_term_price_momentum_percentile :: Percentile rank for price momentum over a long-term horizon, such as twelve months.  [cov=1.00]
market_implied_10yr_eps_cagr_3 :: Compound annual growth rate of earnings per share implied by market price over 10 years.  [cov=0.82]
market_implied_10yr_eps_cagr_4 :: Compound annual growth rate of earnings per share implied by market price over 10 years.  [cov=0.82]
market_implied_5yr_eps_cagr_3 :: Compound annual growth rate of earnings per share implied by market price over 5 years.  [cov=0.82]
market_implied_five_year_eps_growth_rate :: Five-year compound annual growth rate of earnings implied by the current market price.  [cov=0.82]
mdl25_01v :: Earnings Quality by Accruals - Period End Date  [cov=0.97]
mdl25_05v :: Diluted EPS from Total Ops - 1 Qtr Difference (%)  [cov=0.83]
mdl25_15v :: Pension Expense - Last Year  [cov=0.58]
mdl25_21v :: Earnings Quality by Cash Flow  [cov=0.96]
mdl25_22v :: Raw Earnings Quality  [cov=0.97]
mdl25_31v :: Earnings Quality by Cash Flow - 1 Day Difference  [cov=0.96]
mdl25_34v :: Diluted EPS from Continuing Ops - Last Qtr  [cov=0.86]
mdl25_41v :: Earnings Quality by Cash Flow - Period End Date  [cov=0.97]
mdl25_44v :: Diluted EPS from Continuing Ops - 1 Qtr Difference  [cov=0.83]
mdl25_54v :: Diluted EPS from Continuing Ops - 1 Qtr Difference (%)  [cov=0.83]
mdl25_61v :: Earnings Quality by Operating Efficiency  [cov=0.97]
mdl25_64v :: Diluted EPS from Disc Ops & XO - Last Qtr  [cov=0.86]
mdl25_6v :: Earnings Quality Region Rank  [cov=0.97]
mdl25_71v :: Earnings Quality by Operating Efficiency - 1 Day Difference  [cov=0.97]
mdl25_73v :: Basic EPS from Total Ops - Last Qtr  [cov=0.80]
mdl25_74v :: Diluted EPS from Disc Ops & XO - 1 Qtr Difference  [cov=0.83]
mdl25_7v :: Earnings Quality Region Rank - 1 Day Difference  [cov=0.97]
mdl25_81v :: Earnings Quality by Operating Efficiency - Period End Date  [cov=0.97]
mdl25_83v :: Basic EPS from Total Ops - 1 Qtr Difference  [cov=0.78]
mdl25_84v :: Diluted EPS from Total Ops - Last Qtr  [cov=0.86]
mdl25_8v :: Earnings Quality by Accruals  [cov=0.96]
mdl25_93v :: Basic EPS from Total Ops - 1 Qtr Difference (%)  [cov=0.78]
mdl25_94v :: Diluted EPS from Total Ops - 1 Qtr Difference  [cov=0.83]
mdl25_9v :: Earnings Quality by Accruals - 1 Day Difference  [cov=0.96]
mdl25_bs_01v :: Book Value - Last Qtr  [cov=0.83]
mdl25_bs_11v :: BV / Share - Last Qtr  [cov=0.80]
mdl25_bs_21v :: BV / Share - 1 Qtr Difference  [cov=0.77]
mdl25_bs_31v :: BV / Share - 1 Qtr Difference (%)  [cov=0.77]
mdl25_bs_41v :: Accum Depr / Gross FA - Last Qtr  [cov=0.67]
mdl25_bs_51v :: Accum Depr / Gross FA - 1 Qtr Difference  [cov=0.57]
mdl25_bs_5v :: Total Assets - Last Qtr  [cov=0.83]
mdl25_bs_61v :: Accum Depr / Gross FA - 1 Qtr Difference (%)  [cov=0.56]
mdl25_bs_6v :: Total Assets - 1 Qtr Difference (%)  [cov=0.79]
mdl25_bs_71v :: Allowance for Doubtful Accts - Last Qtr  [cov=0.69]
mdl25_bs_7v :: Average Net Operating Assets - Last Qtr  [cov=0.83]
mdl25_bs_81v :: Allowance for Doubtful Accts - 1 Qtr Difference (%)  [cov=0.62]
mdl25_bs_8v :: Adjusted Average Net Operating Assets - Last Qtr  [cov=0.83]
mdl25_bs_91v :: Unearned Revenue - 1 Qtr Difference (%)  [cov=0.68]
mdl25_bs_9v :: Adjusted Average Net Operating Assets - 1 Qtr Difference (%)  [cov=0.79]
mdl25_cb_01v :: Average Traded Volume  [cov=0.99]
mdl25_cb_02v :: Data-Through Date (Fundamental) Current  [cov=0.99]
mdl25_cb_11v :: Average Traded Volume (Local Currency)  [cov=0.99]
mdl25_cb_12v :: Period End Date - Last Qtr  [cov=0.84]
mdl25_cb_21v :: Average Traded Volume (USD)  [cov=0.99]
mdl25_cb_22v :: Company Filing Date - Last Qtr  [cov=0.87]
mdl25_cb_32v :: New Filing Received Date - Last Qtr  [cov=0.83]
mdl25_cb_6v :: Market Cap (Local Currency)  [cov=0.99]
mdl25_cb_7v :: Market Cap (USD)  [cov=0.99]
mdl25_cb_8v :: 52-week High Price  [cov=0.99]
mdl25_cb_9v :: 52-week Low Price  [cov=0.99]
mdl25_cfs_01v :: Cash Flow from Investing - 1 Qtr Difference (%)  [cov=0.78]
mdl25_cfs_11v :: Cash Flow from Financing - Last Qtr  [cov=0.79]
mdl25_cfs_21v :: Cash Flow from Financing - 1 Qtr Difference (%)  [cov=0.74]
mdl25_cfs_31v :: FCF - Last Qtr  [cov=0.80]
mdl25_cfs_41v :: FCF - 1 Qtr Difference (%)  [cov=0.78]
mdl25_cfs_51v :: Capex - Last Qtr  [cov=0.79]
mdl25_cfs_5v :: Total Cash Flow - Last Qtr  [cov=0.80]
mdl25_cfs_61v :: Capex - 1 Qtr Difference (%)  [cov=0.77]
mdl25_cfs_6v :: Total Cash Flow - 1 Qtr Difference  [cov=0.78]
mdl25_cfs_71v :: CF Working Capital - Last Qtr  [cov=0.48]
mdl25_cfs_7v :: Cash Flow from Ops - Last Qtr  [cov=0.80]
mdl25_cfs_81v :: CF Working Capital - 1 Qtr Difference (%)  [cov=0.45]
mdl25_cfs_8v :: Cash Flow from Ops - 1 Qtr Difference (%)  [cov=0.78]
mdl25_cfs_91v :: Excess Cash Margin (%) - Last Qtr  [cov=0.79]
mdl25_cfs_9v :: Cash Flow from Investing - Last Qtr  [cov=0.80]
mdl25_eq_bs_v10 :: Book Value - Last Qtr  [cov=1.00]
mdl25_eq_bs_v11 :: BV / Share - Last Qtr  [cov=1.00]
mdl25_eq_bs_v12 :: BV / Share - 1 Qtr Difference  [cov=1.00]
mdl25_eq_bs_v13 :: BV / Share - 1 Qtr Difference (%)  [cov=1.00]
mdl25_eq_bs_v14 :: Accum Depr / Gross FA - Last Qtr  [cov=0.87]
mdl25_eq_bs_v15 :: Accum Depr / Gross FA - 1 Qtr Difference  [cov=0.73]
mdl25_eq_bs_v16 :: Accum Depr / Gross FA - 1 Qtr Difference (%)  [cov=0.73]
mdl25_eq_bs_v17 :: Allowance for Doubtful Accts - Last Qtr  [cov=0.91]
mdl25_eq_bs_v18 :: Allowance for Doubtful Accts - 1 Qtr Difference (%)  [cov=0.82]
mdl25_eq_bs_v19 :: Unearned Revenue - 1 Qtr Difference (%)  [cov=0.91]
mdl25_eq_bs_v5 :: Total Assets - Last Qtr  [cov=1.00]
mdl25_eq_bs_v6 :: Total Assets - 1 Qtr Difference (%)  [cov=1.00]
mdl25_eq_bs_v7 :: Average Net Operating Assets - Last Qtr  [cov=1.00]
mdl25_eq_bs_v8 :: Adjusted Average Net Operating Assets - Last Qtr  [cov=1.00]
mdl25_eq_bs_v9 :: Adjusted Average Net Operating Assets - 1 Qtr Difference (%)  [cov=1.00]
mdl25_eq_cb_v10 :: Average Traded Volume  [cov=0.50]
mdl25_eq_cb_v11 :: Average Traded Volume (Local Currency)  [cov=0.50]
mdl25_eq_cb_v12 :: Average Traded Volume (USD)  [cov=0.50]
mdl25_eq_cb_v20 :: Data-Through Date (Fundamental) Current  [cov=0.50]
mdl25_eq_cb_v21 :: Period End Date - Last Quarter  [cov=1.00]
mdl25_eq_cb_v22 :: Company Filing Date - Last Quarter  [cov=1.00]
mdl25_eq_cb_v23 :: New Filing Received Date - Last Quarter  [cov=1.00]
mdl25_eq_cb_v6 :: Market Cap (Local Currency)  [cov=0.50]
mdl25_eq_cb_v7 :: Market Cap (USD)  [cov=0.50]
mdl25_eq_cb_v8 :: 52-week High Price  [cov=0.50]
mdl25_eq_cb_v9 :: 52-week Low Price  [cov=0.50]
mdl25_eq_cfs_v10 :: Cash flow from investing activities, quarter-over-quarter percentage change  [cov=1.00]
mdl25_eq_cfs_v11 :: Cash flow from financing activities, last reported quarter  [cov=1.00]
mdl25_eq_cfs_v12 :: Cash flow from financing activities, quarter-over-quarter percentage change  [cov=1.00]
mdl25_eq_cfs_v13 :: Free cash flow (FCF), last reported quarter  [cov=1.00]
mdl25_eq_cfs_v14 :: Free cash flow (FCF), quarter-over-quarter percentage change  [cov=1.00]
mdl25_eq_cfs_v15 :: Capital expenditures (Capex), last reported quarter  [cov=1.00]
mdl25_eq_cfs_v16 :: Capital expenditures (Capex), quarter-over-quarter percentage change  [cov=1.00]
mdl25_eq_cfs_v17 :: Cash flow related to working capital, last reported quarter  [cov=0.75]
mdl25_eq_cfs_v18 :: Cash flow related to working capital, quarter-over-quarter percentage change  [cov=0.66]
mdl25_eq_cfs_v19 :: Excess cash margin percentage, last reported quarter  [cov=1.00]
mdl25_eq_cfs_v5 :: Total cash flow, last reported quarter  [cov=1.00]
mdl25_eq_cfs_v6 :: Total cash flow, quarter-over-quarter absolute difference  [cov=1.00]
mdl25_eq_cfs_v7 :: Cash flow from operating activities, last reported quarter  [cov=1.00]
mdl25_eq_cfs_v8 :: Cash flow from operating activities, quarter-over-quarter percentage change  [cov=1.00]
mdl25_eq_cfs_v9 :: Cash flow from investing activities, last reported quarter  [cov=1.00]
mdl25_eq_history_v10 :: Earnings Quality Raw Current  [cov=0.50]
mdl25_eq_history_v11 :: Earnings Quality Region Rank Current  [cov=0.50]
mdl25_eq_history_v12 :: Accruals Component Current  [cov=0.50]
mdl25_eq_history_v13 :: Cash Flow Component Current  [cov=0.50]
mdl25_eq_history_v9 :: Earnings Quality Region  [cov=0.50]
mdl25_eq_is_v10 :: Quarter-over-quarter percentage change in EBITDA  [cov=1.00]
mdl25_eq_is_v11 :: Average Historical EBITDA Growth over 5 Years  [cov=0.50]
mdl25_eq_is_v12 :: Difference from Average Historical EBITDA Growth over 5 Years  [cov=0.50]
mdl25_eq_is_v13 :: Quarter-over-quarter percentage change in operating expenses  [cov=1.00]
mdl25_eq_is_v14 :: EBIT for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v15 :: Quarter-over-quarter percentage change in EBIT  [cov=1.00]
mdl25_eq_is_v16 :: Net income from continuing operations for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v17 :: Quarter-over-quarter percentage change in net income from continuing operations  [cov=1.00]
mdl25_eq_is_v18 :: Special items amount in the most recent fiscal quarter  [cov=0.93]
mdl25_eq_is_v19 :: Quarter-over-quarter percentage change in special items  [cov=0.83]
mdl25_eq_is_v24 :: Net income for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v25 :: Quarter-over-quarter percentage change in net income  [cov=1.00]
mdl25_eq_is_v26 :: Dividends per share for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v27 :: Quarter-over-quarter absolute change in dividends per share  [cov=1.00]
mdl25_eq_is_v28 :: Quarter-over-quarter percentage change in dividends per share  [cov=0.36]
mdl25_eq_is_v29 :: Average Historical EPS Growth over 5 Years  [cov=0.50]
mdl25_eq_is_v30 :: Difference from average historical EPS growth (5-year)  [cov=0.50]
mdl25_eq_is_v31 :: Basic EPS from continuing operations for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v32 :: Quarter-over-quarter absolute change in basic EPS from continuing operations  [cov=1.00]
mdl25_eq_is_v33 :: Quarter-over-quarter percentage change in basic EPS from continuing operations  [cov=1.00]
mdl25_eq_is_v34 :: Basic EPS from discontinued operations and extraordinary items for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v35 :: Basic EPS from discontinued operations and extraordinary items - 1 quarter difference  [cov=1.00]
mdl25_eq_is_v37 :: Basic EPS from Total Operations - Last Quarter  [cov=1.00]
mdl25_eq_is_v38 :: Basic EPS from Total Operations - 1 Quarter Difference  [cov=1.00]
mdl25_eq_is_v39 :: Basic EPS from total operations - 1 quarter difference (%)  [cov=1.00]
mdl25_eq_is_v43 :: Diluted EPS from continuing operations - last quarter  [cov=1.00]
mdl25_eq_is_v44 :: Diluted EPS from continuing operations - 1 quarter difference  [cov=1.00]
mdl25_eq_is_v45 :: Diluted EPS from continuing operations - 1 quarter difference (%)  [cov=1.00]
mdl25_eq_is_v46 :: Diluted EPS from Discontinued Operations and Extraordinary Items - Last Quarter  [cov=1.00]
mdl25_eq_is_v47 :: Diluted EPS from discontinued operations and extraordinary items - 1 quarter difference  [cov=1.00]
mdl25_eq_is_v48 :: Diluted EPS from Total Operations - Last Quarter  [cov=1.00]
mdl25_eq_is_v49 :: Diluted EPS from Total Operations - 1 Quarter Difference  [cov=1.00]
mdl25_eq_is_v5 :: Total revenue recognized in the most recent fiscal quarter  [cov=1.00]
mdl25_eq_is_v50 :: Diluted EPS from total operations - 1 quarter difference (%)  [cov=1.00]
mdl25_eq_is_v51 :: Pension Expense - Last Year  [cov=0.50]
mdl25_eq_is_v6 :: Quarter-over-quarter percentage change in revenue  [cov=1.00]
mdl25_eq_is_v7 :: Average Historical Revenue Growth over 5 Years  [cov=0.50]
mdl25_eq_is_v8 :: Difference from average historical revenue growth (5-year)  [cov=0.50]
mdl25_eq_is_v9 :: EBITDA for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_rd_v10 :: Pretax ROA (%) - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v11 :: Leverage (Assets/Equity) - Last Qtr  [cov=1.00]
mdl25_eq_rd_v12 :: Leverage (Assets/Equity) - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v13 :: Pretax ROE (%) - Last Qtr  [cov=1.00]
mdl25_eq_rd_v14 :: Pretax ROE (%) - Chg 1 Qtr  [cov=1.00]
mdl25_eq_rd_v15 :: ROE (%) - Last Qtr  [cov=1.00]
mdl25_eq_rd_v16 :: ROE (%) - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v17 :: Earnings Retention - Last Qtr  [cov=1.00]
mdl25_eq_rd_v18 :: Earnings Retention - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v19 :: Reinvestment Rate (%) - Last Qtr  [cov=1.00]
mdl25_eq_rd_v20 :: Reinvestment Rate (%) - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v5 :: Asset Turnover - Last Qtr  [cov=1.00]
mdl25_eq_rd_v6 :: Asset Turnover - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v7 :: Pretax Margin (%) - Last Qtr  [cov=1.00]
mdl25_eq_rd_v8 :: Pretax Margin (%) - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rd_v9 :: Pretax ROA (%) - Last Qtr  [cov=1.00]
mdl25_eq_rlev_v10 :: Quarter-over-quarter change in long-term debt to total capital percentage  [cov=1.00]
mdl25_eq_rlev_v11 :: Net debt (total debt minus cash) divided by EBITDA for the most recent quarter  [cov=1.00]
mdl25_eq_rlev_v12 :: Quarter-over-quarter change in net debt to EBITDA ratio  [cov=1.00]
mdl25_eq_rlev_v5 :: Ratio of total assets to shareholders’ equity for the most recent quarter  [cov=1.00]
mdl25_eq_rlev_v6 :: Quarter-over-quarter change in the assets-to-equity ratio (current quarter minus prior quarter)  [cov=1.00]
mdl25_eq_rlev_v7 :: Ratio of total debt to shareholders’ equity for the most recent quarter  [cov=1.00]
mdl25_eq_rlev_v8 :: Quarter-over-quarter change in the debt-to-equity ratio (current quarter minus prior quarter)  [cov=1.00]
mdl25_eq_rlev_v9 :: Long-term debt as a percentage of total capital for the most recent quarter  [cov=1.00]
mdl25_eq_rliq_v10 :: Quarter-over-quarter change in times interest earned (current quarter minus prior)  [cov=0.92]
mdl25_eq_rliq_v11 :: Cash conversion cycle (days) for the most recent quarter  [cov=1.00]
mdl25_eq_rliq_v12 :: Quarter-over-quarter change in cash conversion cycle (days) (current quarter minus prior)  [cov=1.00]
mdl25_eq_rliq_v5 :: Quick ratio (acid-test) for the most recent reported quarter  [cov=1.00]
mdl25_eq_rliq_v6 :: Quarter-over-quarter change in quick ratio (current quarter minus prior)  [cov=1.00]
mdl25_eq_rliq_v7 :: Current ratio for the most recent reported quarter  [cov=1.00]
mdl25_eq_rliq_v8 :: Quarter-over-quarter change in current ratio (current quarter minus prior)  [cov=1.00]
mdl25_eq_rliq_v9 :: Times interest earned (interest coverage ratio) for the most recent quarter  [cov=0.96]
mdl25_eq_ro_v10 :: Inv Turnover - Last Qtr  [cov=0.99]
mdl25_eq_ro_v11 :: Inv Turnover - 1 Qtr Difference  [cov=0.97]
mdl25_eq_ro_v12 :: Avg Inventory Days - Last Qtr  [cov=0.99]
mdl25_eq_ro_v13 :: Avg Inventory Days - 1 Qtr Difference  [cov=0.97]
mdl25_eq_ro_v14 :: WC/Sales - Last Qtr  [cov=1.00]
mdl25_eq_ro_v15 :: WC/Sales - 1 Qtr Difference  [cov=1.00]
mdl25_eq_ro_v16 :: Net Op. Asset Turnover - Last Qtr  [cov=1.00]
mdl25_eq_ro_v17 :: Adj. Net Op. Asset Turnover - Last Year  [cov=0.50]
mdl25_eq_ro_v18 :: Adj. Net Op. Asset Turnover - 1 FY Difference  [cov=0.50]
mdl25_eq_ro_v19 :: Return on Net Op. Assets (%) - Last Qtr  [cov=1.00]
mdl25_eq_ro_v20 :: Return on Net Operating Assets (%) - 1 Qtr Difference  [cov=1.00]
mdl25_eq_ro_v21 :: Return on Adj. Net Op. Assets (%) - Last Year  [cov=0.50]
mdl25_eq_ro_v22 :: Return on Adj. Net Op. Assets (%) - 1 FY Difference  [cov=0.50]
mdl25_eq_ro_v5 :: Net Op. Asset Turnover - 1 Qtr Difference  [cov=1.00]
mdl25_eq_ro_v6 :: A/R Turnover - Last Qtr  [cov=1.00]
mdl25_eq_ro_v7 :: A/R Turnover - 1 Qtr Difference  [cov=1.00]
mdl25_eq_ro_v8 :: Avg. A/R Days - Last Qtr  [cov=1.00]
mdl25_eq_ro_v9 :: Avg. A/R Days - 1 Qtr Difference  [cov=1.00]
mdl25_eq_rp_v10 :: Quarter-over-quarter change in EBITDA margin percentage  [cov=1.00]
mdl25_eq_rp_v11 :: Operating margin percentage for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_rp_v12 :: Quarter-over-quarter change in operating margin percentage  [cov=1.00]
mdl25_eq_rp_v13 :: Five-year average operating margin percentage  [cov=0.50]
mdl25_eq_rp_v14 :: Difference between current operating margin and its five-year average  [cov=0.50]
mdl25_eq_rp_v15 :: Pretax margin percentage for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_rp_v16 :: Quarter-over-quarter change in pretax margin percentage  [cov=1.00]
mdl25_eq_rp_v17 :: Effective tax rate for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_rp_v18 :: Quarter-over-quarter change in effective tax rate  [cov=1.00]
mdl25_eq_rp_v19 :: Net profit margin percentage for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_rp_v20 :: Quarter-over-quarter change in net profit margin percentage  [cov=1.00]
mdl25_eq_rp_v5 :: Gross margin percentage for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_rp_v6 :: Quarter-over-quarter change in gross margin percentage  [cov=1.00]
mdl25_eq_rp_v7 :: Five-year average gross margin percentage  [cov=0.50]
mdl25_eq_rp_v8 :: Difference between current gross margin and its five-year average  [cov=0.50]
mdl25_eq_rp_v9 :: EBITDA margin percentage for the most recent fiscal quarter  [cov=1.00]
mdl25_eq_v10 :: Earnings Quality by Accruals - Period End Date  [cov=0.50]
mdl25_eq_v12 :: Earnings Quality by Cash Flow  [cov=0.50]
mdl25_eq_v13 :: Earnings Quality by Cash Flow - 1 Day Difference  [cov=0.50]
mdl25_eq_v14 :: Earnings Quality by Cash Flow - Period End Date  [cov=0.50]
mdl25_eq_v16 :: Earnings Quality by Operating Efficiency  [cov=0.50]
mdl25_eq_v17 :: Earnings Quality by Operating Efficiency - 1 Day Difference  [cov=0.50]
mdl25_eq_v18 :: Earnings Quality by Operating Efficiency - Period End Date  [cov=0.50]
mdl25_eq_v22 :: Raw Earnings Quality  [cov=0.50]
mdl25_eq_v6 :: Earnings Quality Region Rank  [cov=0.50]
mdl25_eq_v7 :: Earnings Quality Region Rank - 1 Day Difference  [cov=0.50]
mdl25_eq_v8 :: Earnings Quality by Accruals  [cov=0.50]
mdl25_eq_v9 :: Earnings Quality by Accruals - 1 Day Difference  [cov=0.50]
mdl25_eq_vr_v10 :: Price/Sales - 1 FY Difference (%)  [cov=0.50]
mdl25_eq_vr_v11 :: Price/CFO  [cov=0.50]
mdl25_eq_vr_v12 :: Price/FCF  [cov=0.50]
mdl25_eq_vr_v13 :: Enterprise Value (EV)  [cov=0.50]
mdl25_eq_vr_v14 :: EV/EBITDA  [cov=0.50]
mdl25_eq_vr_v15 :: EV/EBITDA - 1 Qtr Difference (%)  [cov=0.96]
mdl25_eq_vr_v16 :: EV/Sales  [cov=0.50]
mdl25_eq_vr_v17 :: FCF Yield (%)  [cov=0.50]
mdl25_eq_vr_v18 :: FCF/EV (%)  [cov=0.50]
mdl25_eq_vr_v19 :: CFO/EV (%)  [cov=0.50]
mdl25_eq_vr_v5 :: Price/Book  [cov=0.50]
mdl25_eq_vr_v6 :: Price/Book - 1 Qtr Difference  [cov=1.00]
mdl25_eq_vr_v7 :: Price/Book - 1 Qtr Difference (%)  [cov=1.00]
mdl25_eq_vr_v8 :: Price/Sales  [cov=0.50]
mdl25_eq_vr_v9 :: Price/Sales - 1 FY Difference  [cov=0.50]
mdl25_history_01v :: Earnings Quality Raw Current  [cov=0.97]
mdl25_history_11v :: Earnings Quality Region Rank Current  [cov=0.97]
mdl25_history_21v :: Accruals Component Current  [cov=0.96]
mdl25_history_31v :: Cash Flow Component Current  [cov=0.97]
mdl25_history_9v :: Earnings Quality Region  [cov=0.97]
mdl25_is_01v :: EBITDA - 1 Qtr Difference (%)  [cov=0.77]
mdl25_is_03v :: Diff from Average Hist EPS Growth 5-Year  [cov=0.75]
mdl25_is_11v :: Average Historical EBITDA Growth 5-Year  [cov=0.84]
mdl25_is_13v :: Basic EPS from Continuing Ops - Last Qtr  [cov=0.80]
mdl25_is_21v :: Diff from Average Hist EBITDA Growth 5-Year  [cov=0.84]
mdl25_is_23v :: Basic EPS from Continuing Ops - 1 Qtr Difference  [cov=0.77]
mdl25_is_31v :: Operating Expenses - 1 Qtr Difference (%)  [cov=0.78]
mdl25_is_33v :: Basic EPS from Continuing Ops - 1 Qtr Difference (%)  [cov=0.77]
mdl25_is_41v :: EBIT - Last Qtr  [cov=0.80]
mdl25_is_42v :: Net Income - Last Qtr  [cov=0.80]
mdl25_is_43v :: Basic EPS from Disc Ops & XO - Last Qtr  [cov=0.80]
mdl25_is_51v :: EBIT - 1 Qtr Difference (%)  [cov=0.78]
mdl25_is_52v :: Net Income - 1 Qtr Difference (%)  [cov=0.77]
mdl25_is_53v :: Basic EPS from Disc Ops & XO - 1 Qtr Difference  [cov=0.77]
mdl25_is_5v :: Revenue - Last Qtr  [cov=0.80]
mdl25_is_61v :: NI from Cont. Ops - Last Qtr  [cov=0.80]
mdl25_is_62v :: Dividends Per Share - Last Qtr  [cov=0.79]
mdl25_is_6v :: Revenue - 1 Qtr Difference (%)  [cov=0.77]
mdl25_is_71v :: NI from Cont. Ops - 1 Qtr Difference (%)  [cov=0.77]
mdl25_is_72v :: Dividends Per Share - 1 Qtr Difference  [cov=0.76]
mdl25_is_7v :: Average Historical Revenue Growth 5-Year  [cov=0.91]
mdl25_is_81v :: Special Items - Last Qtr  [cov=0.59]
mdl25_is_8v :: Diff from Average Hist Revenue Growth 5-Year  [cov=0.91]
mdl25_is_91v :: Special Items - 1 Qtr Difference (%)  [cov=0.51]
mdl25_is_92v :: Average Historical EPS Growth 5-Year  [cov=0.75]
mdl25_is_9v :: EBITDA - Last Qtr  [cov=0.80]
mdl25_rd_01v :: Pretax ROA (%) - 1 Qtr Difference  [cov=0.75]
mdl25_rd_02v :: Reinvestment Rate (%) - 1 Qtr Difference  [cov=0.73]
mdl25_rd_11v :: Leverage (Assets/Equity) - Last Qtr  [cov=0.83]
mdl25_rd_21v :: Leverage (Assets/Equity) - 1 Qtr Difference  [cov=0.79]
mdl25_rd_31v :: Pretax ROE (%) - Last Qtr  [cov=0.80]
mdl25_rd_41v :: Pretax ROE (%) - Chg 1 Qtr  [cov=0.77]
mdl25_rd_51v :: ROE (%) - Last Qtr  [cov=0.78]
mdl25_rd_5v :: Asset Turnover - Last Qtr  [cov=0.78]
mdl25_rd_61v :: ROE (%) - 1 Qtr Difference  [cov=0.75]
mdl25_rd_6v :: Asset Turnover - 1 Qtr Difference  [cov=0.75]
mdl25_rd_71v :: Earnings Retention - Last Qtr  [cov=0.79]
mdl25_rd_7v :: Pretax Margin (%) - Last Qtr  [cov=0.80]
mdl25_rd_81v :: Earnings Retention - 1 Qtr Difference  [cov=0.75]
mdl25_rd_8v :: Pretax Margin (%) - 1 Qtr Difference  [cov=0.77]
mdl25_rd_91v :: Reinvestment Rate (%) - Last Qtr  [cov=0.77]
mdl25_rd_9v :: Pretax ROA (%) - Last Qtr  [cov=0.78]
mdl25_rlev_01v :: % Long-Term Debt to Total Capital - 1 Qtr Difference  [cov=0.79]
mdl25_rlev_11v :: (Total Debt - Cash) / EBITDA - Last Qtr  [cov=0.80]
mdl25_rlev_21v :: (Total Debt - Cash) / EBITDA - Chg 1 Qtr  [cov=0.77]
mdl25_rlev_5v :: Assets to Equity - Last Qtr  [cov=0.83]
mdl25_rlev_6v :: Assets to Equity - 1 Qtr Difference  [cov=0.79]
mdl25_rlev_7v :: Debt to Equity - Last Qtr  [cov=0.83]
mdl25_rlev_8v :: Debt to Equity - 1 Qtr Difference  [cov=0.79]
mdl25_rlev_9v :: Long-Term Debt to Total Capital - Last Qtr (%)  [cov=0.83]
mdl25_rliq_01v :: Times Interest Earned - 1 Qtr Difference  [cov=0.61]
mdl25_rliq_11v :: Cash Cycle - Last Qtr  [cov=0.78]
mdl25_rliq_21v :: Cash Cycle - 1 Qtr Difference  [cov=0.74]
mdl25_rliq_5v :: Quick Ratio - Last Qtr  [cov=0.74]
mdl25_rliq_6v :: Quick Ratio - 1 Qtr Difference  [cov=0.70]
mdl25_rliq_7v :: Current Ratio - Last Qtr  [cov=0.78]
mdl25_rliq_8v :: Current Ratio - 1 Qtr Difference  [cov=0.74]
mdl25_rliq_9v :: Times Interest Earned - Last Qtr  [cov=0.66]
mdl25_ro_01v :: Inv Turnover - Last Qtr  [cov=0.69]
mdl25_ro_02v :: Return on Net Operating Assets (%) - 1 Qtr Difference  [cov=0.77]
mdl25_ro_11v :: Inv Turnover - 1 Qtr Difference  [cov=0.66]
mdl25_ro_12v :: Return on Adj. Net Op. Assets (%) - Last Year  [cov=0.98]
mdl25_ro_21v :: Avg Inventory Days - Last Qtr  [cov=0.69]
mdl25_ro_22v :: Return on Adj. Net Op. Assets (%) - 1 FY Difference  [cov=0.96]
mdl25_ro_31v :: Avg Inventory Days - 1 Qtr Difference  [cov=0.66]
mdl25_ro_41v :: WC/Sales - Last Qtr  [cov=0.73]
mdl25_ro_51v :: WC/Sales - 1 Qtr Difference  [cov=0.70]
mdl25_ro_5v :: Net Op. Asset Turnover - 1 Qtr Difference  [cov=0.77]
mdl25_ro_61v :: Net Op. Asset Turnover - Last Qtr  [cov=0.80]
mdl25_ro_6v :: A/R Turnover - Last Qtr  [cov=0.77]
mdl25_ro_71v :: Adj. Net Op. Asset Turnover - Last Year  [cov=0.98]
mdl25_ro_7v :: A/R Turnover - 1 Qtr Difference  [cov=0.74]
mdl25_ro_81v :: Adj. Net Op. Asset Turnover - 1 FY Difference  [cov=0.97]
mdl25_ro_8v :: Avg. A/R Days - Last Qtr  [cov=0.77]
mdl25_ro_91v :: Return on Net Op. Assets (%) - Last Qtr  [cov=0.80]
mdl25_ro_9v :: Avg. A/R Days - 1 Qtr Difference  [cov=0.74]
mdl25_rp_01v :: EBITDA Margin (%) - 1 Qtr Difference  [cov=0.77]
mdl25_rp_02v :: Net Margin (%) - 1 Qtr Difference  [cov=0.77]
mdl25_rp_11v :: Operating Margin (%) - Last Qtr  [cov=0.80]
mdl25_rp_21v :: Operating Margin (%) - 1 Qtr Difference  [cov=0.77]
mdl25_rp_31v :: Average Historical Operating Margin 5-Year  [cov=0.95]
mdl25_rp_41v :: Diff from Average Hist Operating Margin 5-Year  [cov=0.95]
mdl25_rp_51v :: Pretax Margin (%) - Last Qtr  [cov=0.80]
mdl25_rp_5v :: Gross Margin (%) - Last Qtr  [cov=0.76]
mdl25_rp_61v :: Pretax Margin (%) - 1 Qtr Difference  [cov=0.77]
mdl25_rp_6v :: Gross Margin (%) - 1 Qtr Difference  [cov=0.74]
mdl25_rp_71v :: Effective Tax Rate (%) - Last Qtr  [cov=0.80]
mdl25_rp_7v :: Average Historical Gross Margin - 5-Year  [cov=0.91]
mdl25_rp_81v :: Effective Tax Rate (%) - 1 Qtr Difference  [cov=0.77]
mdl25_rp_8v :: Diff from Average Hist Gross Margin - 5-Year  [cov=0.90]
mdl25_rp_91v :: Net Margin (%) - Last Qtr  [cov=0.80]
mdl25_rp_9v :: EBITDA Margin (%) - Last Qtr  [cov=0.80]
mdl25_starmine_ccr_credit_combined_country_rank :: Percentile rank of the combined credit risk score within the company’s country, where a higher rank indicates lower credit risk among country peers  [cov=1.00]
mdl25_starmine_ccr_credit_combined_global_rank :: Percentile rank (1–100) of the firm’s combined CCR credit risk score within the global universe, where higher rank indicates lower default risk  [cov=1.00]
mdl25_starmine_ccr_credit_combined_industry_rank :: Percentile rank of the combined credit risk score within the company’s industry, where a higher rank indicates lower credit risk among industry peers  [cov=1.00]
mdl25_starmine_ccr_credit_combined_pd :: Credit risk score  [cov=1.00]
mdl25_starmine_ccr_credit_combined_region_rank :: Percentile rank of the combined credit risk score within the region, where a higher rank indicates lower credit risk among regional peers  [cov=1.00]
mdl25_starmine_ccr_credit_combined_sector_rank :: Percentile rank of the combined credit risk score within the company’s sector, where a higher rank indicates lower credit risk among sector peers  [cov=1.00]
mdl25_vr_01v :: Price/Sales - 1 FY Difference (%)  [cov=0.91]
mdl25_vr_11v :: Price/CFO  [cov=0.82]
mdl25_vr_21v :: Price/FCF  [cov=0.65]
mdl25_vr_31v :: Enterprise Value (EV)  [cov=0.98]
mdl25_vr_41v :: EV/EBITDA  [cov=0.91]
mdl25_vr_51v :: EV/EBITDA - 1 Qtr Difference (%)  [cov=0.71]
mdl25_vr_5v :: Price/Book  [cov=0.98]
mdl25_vr_61v :: EV/Sales  [cov=0.98]
mdl25_vr_6v :: Price/Book - 1 Qtr Difference  [cov=0.82]
mdl25_vr_71v :: FCF Yield (%)  [cov=0.97]
mdl25_vr_7v :: Price/Book - 1 Qtr Difference (%)  [cov=0.82]
mdl25_vr_81v :: FCF/EV (%)  [cov=0.96]
mdl25_vr_8v :: Price/Sales  [cov=0.98]
mdl25_vr_91v :: CFO/EV (%)  [cov=0.96]
mdl25_vr_9v :: Price/Sales - 1 FY Difference  [cov=0.91]
mid_term_momentum_percentile :: Percentile score for mid-term price momentum.  [cov=1.00]
mid_term_price_momentum_percentile :: Percentile rank for price momentum over a mid-term horizon, such as six months.  [cov=1.00]
operating_efficiency_component_score :: Percentile score for operating efficiency factors in the earnings quality model.  [cov=1.00]
pe_ratio_relative_score_float_2 :: Relative score for price-to-earnings ratio as a floating-point value.  [cov=1.00]
price_book_ratio_percentile :: Percentile ranking for price to book value ratio.  [cov=1.00]
price_cashflow_ratio_percentile :: Percentile ranking for price to cash flow ratio.  [cov=1.00]
price_cashflow_ratio_percentile_float :: Percentile ranking for price to cash flow ratio as a float.  [cov=1.00]
price_earnings_ratio_percentile :: Percentile ranking for price to earnings ratio.  [cov=1.00]
price_earnings_ratio_percentile_float :: Percentile ranking for price to earnings ratio as a float.  [cov=1.00]
price_intrinsic_value_industry_percentile :: Industry-relative percentile ranking for price to intrinsic value ratio.  [cov=0.77]
price_intrinsic_value_industry_rank_float :: Industry-relative percentile score for price to intrinsic value ratio as a float.  [cov=0.77]
price_intrinsic_value_region_percentile :: Region-relative percentile ranking for price to intrinsic value ratio.  [cov=0.82]
price_intrinsic_value_region_rank_float :: Region-relative percentile score for price to intrinsic value ratio as a float.  [cov=0.82]
price_intrinsic_value_sector_rank_float :: Sector-relative percentile score for price to intrinsic value ratio as a float.  [cov=0.82]
price_intrinsicvalue_industry_rank_float :: Precise industry-relative ranking of the ratio of current price to intrinsic value.  [cov=0.77]
price_intrinsicvalue_region_rank :: Region-relative ranking of the ratio of current price to intrinsic value.  [cov=0.82]
price_intrinsicvalue_region_rank_float :: Precise region-relative ranking of the ratio of current price to intrinsic value.  [cov=0.82]
price_intrinsicvalue_sector_rank :: Sector-relative ranking of the ratio of current price to intrinsic value.  [cov=0.82]
price_to_book_value_relative_score :: Relative score for the price-to-book value ratio compared to global peers.  [cov=1.00]
price_to_book_value_relative_score_backfill :: Relative score for price-to-book value ratio compared to global peers (backfill version).  [cov=1.00]
price_to_intrinsic_value_industry_percentile :: Percentile ranking of a stock's price to intrinsic value ratio compared to industry peers.  [cov=0.77]
price_to_intrinsic_value_ratio_4 :: Ratio of current share price to calculated intrinsic value.  [cov=0.82]
price_to_intrinsic_value_sector_percentile :: Percentile ranking of a stock's price to intrinsic value ratio compared to sector peers.  [cov=0.82]
price_to_intrinsic_value_sector_percentile_float :: Sector-relative price to intrinsic value percentile score as a floating-point value.  [cov=0.82]
price_to_intrinsicvalue_ratio :: Ratio of current share price to estimated intrinsic value.  [cov=0.82]
proj_dividends_fy12 :: Projected dividends per share for fiscal year 12.  [cov=0.82]
proj_dividends_fy13 :: Projected dividends per share for fiscal year 13.  [cov=0.82]
proj_dividends_fy14 :: Projected dividends per share for fiscal year 14.  [cov=0.82]
proj_dividends_fy5 :: Projected dividends per share for fiscal year 5.  [cov=0.82]
proj_dividends_fy7 :: Projected dividends per share for fiscal year 7.  [cov=0.82]
proj_earnings_fy1 :: Projected earnings for fiscal year 1 based on model estimates.  [cov=0.82]
proj_earnings_fy13 :: Projected earnings for fiscal year 13 based on model estimates.  [cov=0.82]
proj_earnings_fy14 :: Projected earnings for fiscal year 14 based on model estimates.  [cov=0.82]
proj_earnings_fy15 :: Projected earnings for fiscal year 15 based on model estimates.  [cov=0.82]
proj_earnings_fy2 :: Projected earnings for fiscal year 2 based on model estimates.  [cov=0.82]
proj_earnings_fy4 :: Projected earnings for fiscal year 4 based on model estimates.  [cov=0.82]
proj_earnings_fy5 :: Projected earnings for fiscal year 5 based on model estimates.  [cov=0.82]
proj_earnings_fy9 :: Projected earnings for fiscal year 9 based on model estimates.  [cov=0.82]
projected_dividend_fy1 :: Projected dividend per share for fiscal year 1.  [cov=1.00]
projected_dividend_fy10 :: Projected dividend per share for fiscal year 10.  [cov=0.82]
projected_dividend_fy11 :: Projected dividend per share for fiscal year 11.  [cov=0.82]
projected_dividend_fy12 :: Projected dividend per share for fiscal year 12.  [cov=0.82]
projected_dividend_fy13 :: Projected dividend per share for fiscal year 13.  [cov=0.82]
projected_dividend_fy14 :: Projected dividend per share for fiscal year 14.  [cov=0.82]
projected_dividend_fy15 :: Projected dividend per share for fiscal year 15.  [cov=0.82]
projected_dividend_fy2 :: Projected dividend per share for fiscal year 2.  [cov=0.82]
projected_dividend_fy3 :: Projected dividend per share for fiscal year 3.  [cov=0.82]
projected_dividend_fy4 :: Projected dividend per share for fiscal year 4.  [cov=0.82]
projected_dividend_fy5 :: Projected dividend per share for fiscal year 5.  [cov=0.82]
projected_dividend_fy6 :: Projected dividend per share for fiscal year 6.  [cov=0.82]
projected_dividend_fy7 :: Projected dividend per share for fiscal year 7.  [cov=0.82]
projected_dividend_fy8 :: Projected dividend per share for fiscal year 8.  [cov=0.82]
projected_dividend_fy9 :: Projected dividend per share for fiscal year 9.  [cov=0.82]
projected_dividend_per_share_year_1 :: Estimated dividend per share for fiscal year 1 based on model projections.  [cov=1.00]
projected_dividend_per_share_year_10 :: Estimated dividend per share for fiscal year 10 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_11 :: Estimated dividend per share for fiscal year 11 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_15 :: Estimated dividend per share for fiscal year 15 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_2 :: Estimated dividend per share for fiscal year 2 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_3 :: Estimated dividend per share for fiscal year 3 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_4 :: Estimated dividend per share for fiscal year 4 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_6 :: Estimated dividend per share for fiscal year 6 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_8 :: Estimated dividend per share for fiscal year 8 based on model projections.  [cov=0.82]
projected_dividend_per_share_year_9 :: Estimated dividend per share for fiscal year 9 based on model projections.  [cov=0.82]
projected_earnings_fy10_4 :: Projected earnings per share for fiscal year 10.  [cov=0.82]
projected_earnings_fy11_3 :: Projected earnings per share for fiscal year 11.  [cov=0.82]
projected_earnings_fy12_3 :: Projected earnings per share for fiscal year 12.  [cov=0.82]
projected_earnings_fy14_3 :: Projected earnings per share for fiscal year 14.  [cov=0.82]
projected_earnings_fy15_3 :: Projected earnings per share for fiscal year 15.  [cov=0.82]
projected_earnings_fy1_3 :: Projected earnings per share for fiscal year 1.  [cov=0.82]
projected_earnings_fy2_3 :: Projected earnings per share for fiscal year 2.  [cov=0.82]
projected_earnings_fy3_4 :: Projected earnings per share for fiscal year 3.  [cov=0.82]
projected_earnings_fy4_4 :: Projected earnings per share for fiscal year 4.  [cov=0.82]
projected_earnings_fy5_4 :: Projected earnings per share for fiscal year 5.  [cov=0.82]
projected_earnings_fy6_4 :: Projected earnings per share for fiscal year 6.  [cov=0.82]
projected_earnings_fy7_3 :: Projected earnings per share for fiscal year 7.  [cov=0.82]
projected_earnings_fy8_4 :: Projected earnings per share for fiscal year 8.  [cov=0.82]
projected_earnings_fy9_3 :: Projected earnings per share for fiscal year 9.  [cov=0.82]
projected_eps_year_10 :: Estimated earnings per share for fiscal year 10 based on model projections.  [cov=0.82]
projected_eps_year_11 :: Estimated earnings per share for fiscal year 11 based on model projections.  [cov=0.82]
projected_eps_year_12 :: Estimated earnings per share for fiscal year 12 based on model projections.  [cov=0.82]
projected_eps_year_13 :: Estimated earnings per share for fiscal year 13 based on model projections.  [cov=0.82]
projected_eps_year_3 :: Estimated earnings per share for fiscal year 3 based on model projections.  [cov=0.82]
projected_eps_year_6 :: Estimated earnings per share for fiscal year 6 based on model projections.  [cov=0.82]
projected_eps_year_7 :: Estimated earnings per share for fiscal year 7 based on model projections.  [cov=0.82]
projected_eps_year_8 :: Estimated earnings per share for fiscal year 8 based on model projections.  [cov=0.82]
region_credit_risk_percentile :: Region-relative percentile rank of a company's credit risk score.  [cov=1.00]
region_price_momentum_percentile :: Region-relative percentile ranking for a stock's price momentum score.  [cov=1.00]
region_relative_valuation_percentile :: Percentile ranking of a stock's relative valuation score compared to region peers.  [cov=1.00]
region_relative_valuation_percentile_float :: Region-relative valuation percentile score as a floating-point value.  [cov=1.00]
region_value_momentum_percentile :: Region-relative value-momentum percentile score.  [cov=1.00]
region_value_momentum_percentile_float :: Region-relative value-momentum percentile score as a floating-point value.  [cov=1.00]
regional_momentum_percentile :: Percentile score for price momentum relative to region.  [cov=1.00]
relative_valuation_global_percentile :: Global percentile ranking for relative valuation score.  [cov=1.00]
relative_valuation_global_rank_float :: Global relative valuation percentile score as a floating-point value.  [cov=1.00]
relative_valuation_industry_percentile :: Industry-relative percentile ranking for relative valuation score.  [cov=1.00]
relative_valuation_industry_rank_float :: Industry-relative relative valuation percentile score as a float.  [cov=1.00]
relative_valuation_region_percentile :: Region-relative percentile ranking for relative valuation score.  [cov=1.00]
relative_valuation_region_rank_float :: Region-relative relative valuation percentile score as a float.  [cov=1.00]
relative_valuation_sector_percentile :: Sector-relative percentile ranking for relative valuation score.  [cov=1.00]
relative_valuation_sector_rank_float :: Sector-relative relative valuation percentile score as a float.  [cov=1.00]
relval_buyback_yield_rank :: Global ranking for share buyback yield within the relative value model.  [cov=1.00]
relval_dividend_yield_rank_float :: Precise global ranking for dividend yield within the relative value model.  [cov=0.74]
relval_global_rank :: Global ranking of a security in the relative value model.  [cov=1.00]
relval_global_rank_float :: Precise global ranking of a security in the relative value model.  [cov=1.00]
relval_price_book_rank_float :: Precise global ranking for price-to-book ratio within the relative value model.  [cov=1.00]
relval_price_cashflow_rank :: Global ranking for price-to-cash flow ratio within the relative value model.  [cov=1.00]
relval_price_cashflow_rank_float :: Precise global ranking for price-to-cash flow ratio within the relative value model.  [cov=1.00]
relval_price_earnings_rank :: Global ranking for price-to-earnings ratio within the relative value model.  [cov=1.00]
sector_credit_risk_percentile :: Sector-relative percentile rank of a company's credit risk score.  [cov=1.00]
sector_relative_valuation_percentile :: Percentile ranking of a stock's relative valuation score compared to sector peers.  [cov=1.00]
sector_relative_valuation_percentile_float :: Sector-relative valuation percentile score as a floating-point value.  [cov=1.00]
sector_value_momentum_percentile :: Sector-relative value-momentum percentile score.  [cov=1.00]
sector_value_momentum_percentile_float :: Sector-relative value-momentum percentile score as a floating-point value.  [cov=1.00]
short_term_momentum_percentile :: Percentile score for short-term price momentum.  [cov=1.00]
short_term_price_momentum_percentile :: Percentile rank for price momentum over a short-term horizon, such as three months or one week.  [cov=1.00]
star_ccr_combined_pd :: Credit risk score  [cov=0.96]
star_ccr_country_rank :: Credit risk rank in the country  [cov=0.96]
star_ccr_global_rank :: Credit risk rank  [cov=0.96]
star_ccr_implied_rating :: Agency-equivalent credit rating implied by the estimate forward 1-year default probability  [cov=0.96]
star_ccr_industry_rank :: Credit Risk Rank in the Industry  [cov=0.96]
star_ccr_region_rank :: Credit risk rank in the region  [cov=0.96]
star_ccr_sector_rank :: Credit risk rank in the sector  [cov=0.96]
steady_state_annual_dividend_per_share :: Long-term expected annual dividend per share in the model's steady state.  [cov=0.82]
steady_state_dividend_payout_rate :: Long-term dividend payout rate assumed in valuation model.  [cov=0.82]
steady_state_dividend_payout_ratio_2 :: Long-term expected ratio of dividends paid out relative to earnings.  [cov=0.82]
steady_state_earnings :: Estimated earnings in the steady-state year of the projection model.  [cov=0.82]
steady_state_earnings_growth :: Projected long-term growth rate of earnings in the steady-state period.  [cov=0.82]
steady_state_earnings_growth_rate_2 :: Long-term earnings growth rate assumed in valuation model.  [cov=0.82]
steady_state_year_dividends :: Annual dividend per share assumed in steady-state valuation.  [cov=0.82]
steady_state_year_earnings :: Annual earnings per share assumed in steady-state valuation.  [cov=0.82]
value_momentum_global_percentile :: Global percentile ranking for value-momentum score.  [cov=1.00]
value_momentum_global_rank_float :: Global value-momentum percentile score as a floating-point value.  [cov=1.00]
value_momentum_industry_percentile :: Industry-relative percentile ranking for value-momentum score.  [cov=1.00]
value_momentum_industry_rank_float :: Industry-relative value-momentum percentile score as a floating-point value.  [cov=1.00]
value_momentum_region_percentile :: Region-relative percentile ranking for value-momentum score.  [cov=1.00]
value_momentum_region_rank_float :: Region-relative value-momentum percentile score as a floating-point value.  [cov=1.00]
value_momentum_sector_percentile :: Sector-relative percentile ranking for value-momentum score.  [cov=1.00]
value_momentum_sector_rank_float :: Sector-relative value-momentum percentile score as a floating-point value.  [cov=1.00]
warranted_forward_pe_ratio_2 :: Forward 12-month price to earnings ratio warranted by valuation model.  [cov=0.82]
warranted_forward_pe_ratio_3 :: Model-implied forward price-to-earnings ratio for the next twelve months.  [cov=0.82]
```
