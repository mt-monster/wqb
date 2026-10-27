# pattern_scores — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `pattern_scores` |
| 名称 | Chart Pattern Similarity Scores |
| 类别 | PV |
| 数据字段数(平台) | 504 |
| 覆盖率 | 0.9924 |
| 平台已有 alpha | 27 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily similarity scores that quantify how closely a stock’s recent price chart matches a range of canonical bilateral technical patterns, such as triangles, wedges, V-formations, and gap structures. By leveraging advanced image-based embeddings of OHLC (Open, High, Low, Close) data, the dataset compares current price action to a curated library of reference patterns, producing scores for each pattern and aggregation method (mean, max, quantile, etc.) across multiple time horizons and global regions. These similarity scores help researchers and traders identify when a stock is exhibiting chart formations that historically precede significant price moves, either as continuations or reversals. The dataset is particularly valuable for developing and validating quantitativ

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **504** |
| 类型分布 | MATRIX×504 |
| 平均覆盖率 | **0.992** |
| 覆盖率区间 | 0.98 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 504 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 499 | 99.0% |
| DEAD | 5 | 1.0% |

- 已实测字段：**5** 个（1%），best_sharpe 最高 **0.03**，中位 -0.03

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 359 | 0.99 | median_similarity_breakaway_gap_upward、mean_similarity_breakaway_gap_upward、max_similarity_breakaway_gap_upward |
| 价量与波动 | 145 | 1.00 | dynamic_similarity_reversal_v_bottom、dynamic_similarity_reversal_v_bottom_pattern、continuation_downward_wedge_max_similarity_40d |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `median_similarity_breakaway_gap_upward` | MATRIX | 0.998 | 风险与质量 | 1 | 0.03 | -0.06 | — | DEAD | Median similarity score to an upward breakaway gap pattern. |
| 2 | `mean_similarity_breakaway_gap_upward` | MATRIX | 0.998 | 风险与质量 | 1 | 0.01 | -0.04 | — | DEAD | Average similarity score to an upward breakaway gap pattern. |
| 3 | `max_similarity_breakaway_gap_upward` | MATRIX | 0.998 | 风险与质量 | 4 | -0.03 | 0.12 | — | DEAD | Maximum similarity score to an upward breakaway gap pattern. |
| 4 | `dynamic_similarity_reversal_v_bottom` | MATRIX | 0.998 | 价量与波动 | 1 | -0.15 | 0.24 | — | DEAD | Dynamic similarity score for a V-shaped reversal pattern at the bottom. |
| 5 | `dynamic_similarity_reversal_v_bottom_pattern` | MATRIX | 0.979 | 价量与波动 | 1 | -0.77 | -0.24 | — | DEAD | Dynamically weighted similarity score for the reversal V-bottom chart pattern. |
| 6 | `continuation_downward_wedge_max_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a continuation-style falling wedge pattern over a 40-day window. |
| 7 | `continuation_downward_wedge_median_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a continuation-style falling wedge pattern over a 40-day window. |
| 8 | `continuation_downward_wedge_quantile95_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a continuation-style falling wedge pattern over a 40-day windo |
| 9 | `continuation_upward_wedge_max_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a continuation-style rising wedge pattern over a 40-day window. |
| 10 | `continuation_upward_wedge_quantile95_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a continuation-style rising wedge pattern over a 40-day window |
| 11 | `downward_gap_break_max_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a strong downward price gap pattern over a 40-day window. |
| 12 | `downward_gap_break_mean_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a strong downward price gap pattern over a 40-day window. |
| 13 | `downward_gap_break_quantile95_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a strong downward price gap pattern over a 40-day window. |
| 14 | `downward_wedge_quantile95_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a falling wedge pattern over a 40-day window. |
| 15 | `dynamic_similarity_asc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for ascending triangle pattern, emphasizing recent bars. |
| 16 | `dynamic_similarity_asc_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for a downward-oriented ascending triangle pattern, emphasizing recent bars. |
| 17 | `dynamic_similarity_breakaway_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for a downward breakaway gap pattern, emphasizing recent bars. |
| 18 | `dynamic_similarity_common_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for a common downward gap pattern, emphasizing recent bars. |
| 19 | `dynamic_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for a common upward gap pattern, emphasizing recent bars. |
| 20 | `dynamic_similarity_continuation_falling_wedge_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for continuation falling wedge pattern, emphasizing recent bars. |
| 21 | `dynamic_similarity_continuation_rising_wedge_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for continuation rising wedge pattern, emphasizing recent bars. |
| 22 | `dynamic_similarity_continuation_v_bottom_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for continuation V-bottom pattern, emphasizing recent data. |
| 23 | `dynamic_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for continuation V-top pattern, emphasizing recent bars. |
| 24 | `dynamic_similarity_desc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for descending triangle pattern, emphasizing recent bars. |
| 25 | `dynamic_similarity_desc_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for upward-oriented descending triangle pattern, emphasizing recent bars. |
| 26 | `dynamic_similarity_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for falling wedge pattern, emphasizing recent bars. |
| 27 | `dynamic_similarity_reversal_v_top` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Dynamic similarity score for a V-shaped reversal pattern at the top. |
| 28 | `dynamic_similarity_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score emphasizing recent bars for rising wedge pattern. |
| 29 | `dynamic_similarity_sym_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for a downward-biased symmetrical triangle pattern. |
| 30 | `dynamic_similarity_sym_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for an upward-biased symmetrical triangle pattern. |
| 31 | `max_reversal_v_bottom_similarity_score` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest similarity score to a bottom reversal V-shaped pattern. |
| 32 | `max_similarity_asc_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a downward-oriented ascending triangle pattern. |
| 33 | `max_similarity_common_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a common downward gap pattern. |
| 34 | `max_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a common upward gap pattern. |
| 35 | `max_similarity_continuation_v_bottom` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a continuation V-bottom pattern. |
| 36 | `max_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a continuation V-top pattern. |
| 37 | `max_similarity_desc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a descending triangle pattern. |
| 38 | `max_similarity_desc_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to an upward-oriented descending triangle pattern. |
| 39 | `max_similarity_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a falling wedge pattern. |
| 40 | `max_similarity_reversal_v_top` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score to a V-shaped reversal pattern at the top. |
| 41 | `max_similarity_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a rising wedge pattern. |
| 42 | `max_similarity_sym_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a downward-biased symmetrical triangle pattern. |
| 43 | `max_similarity_sym_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to an upward-biased symmetrical triangle pattern. |
| 44 | `mean_similarity_asc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to an ascending triangle pattern. |
| 45 | `mean_similarity_asc_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a downward-oriented ascending triangle pattern. |
| 46 | `mean_similarity_common_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a common downward gap pattern. |
| 47 | `mean_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a common upward gap pattern. |
| 48 | `mean_similarity_continuation_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a continuation falling wedge pattern. |
| 49 | `mean_similarity_continuation_rising_wedge_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a continuation rising wedge pattern. |
| 50 | `mean_similarity_continuation_v_bottom` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a continuation V-bottom pattern. |
| 51 | `mean_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a continuation V-top pattern. |
| 52 | `mean_similarity_desc_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to an upward-oriented descending triangle pattern. |
| 53 | `mean_similarity_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a falling wedge pattern. |
| 54 | `mean_similarity_reversal_v_top` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score to a V-shaped reversal pattern at the top. |
| 55 | `mean_similarity_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a rising wedge pattern. |
| 56 | `mean_similarity_sym_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to an upward-biased symmetrical triangle pattern. |
| 57 | `median_asc_triangle_downward_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for a downward breakout variant of ascending triangle. |
| 58 | `median_similarity_asc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to an ascending triangle pattern. |
| 59 | `median_similarity_breakaway_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a downward breakaway gap pattern. |
| 60 | `median_similarity_common_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a common downward gap pattern. |
| 61 | `median_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a common upward gap pattern. |
| 62 | `median_similarity_continuation_rising_wedge_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a continuation rising wedge pattern. |
| 63 | `median_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a continuation V-top pattern. |
| 64 | `median_similarity_desc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a descending triangle pattern. |
| 65 | `median_similarity_desc_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to an upward-oriented descending triangle pattern. |
| 66 | `median_similarity_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a falling wedge pattern. |
| 67 | `median_similarity_reversal_v_bottom` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score to a V-shaped reversal pattern at the bottom. |
| 68 | `median_similarity_reversal_v_top` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score to a V-shaped reversal pattern at the top. |
| 69 | `median_similarity_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a rising wedge pattern. |
| 70 | `median_similarity_sym_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a downward-biased symmetrical triangle pattern. |
| 71 | `min_ascending_triangle_similarity_metric` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score for an ascending triangle pattern. |
| 72 | `min_similarity_asc_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a downward-oriented ascending triangle pattern. |
| 73 | `min_similarity_breakaway_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a downward breakaway gap pattern. |
| 74 | `min_similarity_common_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a common downward gap pattern. |
| 75 | `min_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a common upward gap pattern. |
| 76 | `min_similarity_continuation_falling_wedge_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a continuation falling wedge pattern. |
| 77 | `min_similarity_continuation_rising_wedge_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a continuation rising wedge pattern. |
| 78 | `min_similarity_continuation_v_bottom` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a continuation V-bottom pattern. |
| 79 | `min_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a continuation V-top pattern. |
| 80 | `min_similarity_desc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a descending triangle pattern. |
| 81 | `min_similarity_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a falling wedge pattern. |
| 82 | `min_similarity_reversal_v_bottom` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score to a V-shaped reversal pattern at the bottom. |
| 83 | `min_similarity_reversal_v_top` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score to a V-shaped reversal pattern at the top. |
| 84 | `min_similarity_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a rising wedge pattern. |
| 85 | `min_similarity_sym_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a downward-biased symmetrical triangle pattern. |
| 86 | `min_similarity_sym_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to an upward-biased symmetrical triangle pattern. |
| 87 | `quantile95_rising_wedge_similarity_value` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for a rising wedge chart pattern. |
| 88 | `quantile95_similarity_asc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to an ascending triangle pattern. |
| 89 | `quantile95_similarity_asc_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a downward-oriented ascending triangle pattern. |
| 90 | `quantile95_similarity_breakaway_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to an upward breakaway gap pattern. |
| 91 | `quantile95_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a common upward gap pattern. |
| 92 | `quantile95_similarity_continuation_v_bottom` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a continuation V-bottom pattern. |
| 93 | `quantile95_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a continuation V-top pattern. |
| 94 | `quantile95_similarity_desc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a descending triangle pattern. |
| 95 | `quantile95_similarity_desc_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to an upward-oriented descending triangle pattern. |
| 96 | `quantile95_similarity_reversal_v_bottom` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a V-shaped reversal pattern at the bottom. |
| 97 | `quantile95_similarity_reversal_v_top` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a V-shaped reversal pattern at the top. |
| 98 | `quantile95_similarity_sym_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a downward-biased symmetrical triangle pattern. |
| 99 | `quantile95_similarity_sym_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to an upward-biased symmetrical triangle pattern. |
| 100 | `regular_downward_gap_quantile95_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a typical downward gap pattern over a 40-day window. |
| 101 | `std_similarity_asc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for ascending triangle pattern. |
| 102 | `std_similarity_asc_triangle_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for downward-oriented ascending triangle pattern. |
| 103 | `std_similarity_breakaway_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for downward breakaway gap pattern. |
| 104 | `std_similarity_breakaway_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for upward breakaway gap pattern. |
| 105 | `std_similarity_common_gap_downward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for common downward gap pattern. |
| 106 | `std_similarity_common_gap_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for common upward gap pattern. |
| 107 | `std_similarity_continuation_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for continuation falling wedge pattern. |
| 108 | `std_similarity_continuation_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for continuation rising wedge pattern. |
| 109 | `std_similarity_continuation_v_bottom` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for continuation V-bottom pattern. |
| 110 | `std_similarity_continuation_v_top` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for continuation V-top pattern. |
| 111 | `std_similarity_desc_triangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for descending triangle pattern. |
| 112 | `std_similarity_desc_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for upward-oriented descending triangle pattern. |
| 113 | `std_similarity_falling_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for falling wedge pattern. |
| 114 | `std_similarity_rising_wedge` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for rising wedge pattern. |
| 115 | `std_similarity_sym_triangle_upward` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for upward-biased symmetrical triangle pattern. |
| 116 | `symmetry_triangle_downward_mean_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a downward breakout symmetrical triangle pattern over a 40-day window. |
| 117 | `symmetry_triangle_downward_std_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a downward breakout symmetrical triangle pattern over a |
| 118 | `symmetry_triangle_upward_median_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching an upward breakout symmetrical triangle pattern over a 40-day window. |
| 119 | `trendline_convergence_max_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a rising support and flat resistance pattern over a 40-day window. |
| 120 | `trendline_divergence_mean_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a falling support and flat resistance pattern over a 40-day window. |
| 121 | `trendline_divergence_upward_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching an upward breakout variant of falling support and flat resistance. |
| 122 | `upward_gap_break_dynamic_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a strong upward price gap pattern over a 40-day window. |
| 123 | `upward_gap_break_min_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a strong upward price gap pattern over a 40-day window. |
| 124 | `v_shape_continuation_bottom_median_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a V-shaped continuation at the bottom pattern over a 40-day window. |
| 125 | `v_shape_reversal_bottom_mean_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a V-shaped reversal at the bottom pattern over a 40-day window. |
| 126 | `v_shape_reversal_bottom_std_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a V-shaped reversal at the bottom pattern over a 40-day |
| 127 | `v_shape_reversal_top_std_similarity_40d` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a V-shaped reversal at the top pattern over a 40-day wi |
| 128 | `asc_triangle_down_min_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to downward breakout ascending triangle pattern over 60-day window. |
| 129 | `asc_triangle_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to ascending triangle pattern over 60-day window. |
| 130 | `asc_triangle_median_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to ascending triangle pattern over 60-day window. |
| 131 | `asc_triangle_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to ascending triangle pattern over 60-day window. |
| 132 | `breakaway_gap_down_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to downward breakaway gap pattern over 60-day window. |
| 133 | `breakaway_gap_down_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to downward breakaway gap pattern over 60-day window. |
| 134 | `breakaway_gap_down_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to downward breakaway gap pattern over 60-day window. |
| 135 | `breakaway_gap_up_dynamic_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to upward breakaway gap pattern over 60-day window. |
| 136 | `breakaway_gap_up_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to upward breakaway gap pattern over 60-day window. |
| 137 | `breakaway_gap_up_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to upward breakaway gap pattern over 60-day window. |
| 138 | `breakaway_gap_up_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to upward breakaway gap pattern over 60-day window. |
| 139 | `common_gap_down_min_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to common gap down pattern over 60-day window. |
| 140 | `common_gap_down_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to common gap down pattern over 60-day window. |
| 141 | `common_gap_up_max_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to common gap up pattern over 60-day window. |
| 142 | `common_gap_up_median_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to common gap up pattern over 60-day window. |
| 143 | `common_gap_up_min_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to common gap up pattern over 60-day window. |
| 144 | `common_gap_up_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to common gap up pattern over 60-day window. |
| 145 | `cont_falling_wedge_min_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to continuation falling wedge pattern over 60-day window. |
| 146 | `cont_falling_wedge_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to continuation falling wedge pattern over 60-day window. |
| 147 | `cont_rising_wedge_dynamic_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to continuation rising wedge pattern over 60-day window. |
| 148 | `cont_rising_wedge_median_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to continuation rising wedge pattern over 60-day window. |
| 149 | `cont_rising_wedge_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to continuation rising wedge pattern over 60-day window. |
| 150 | `cont_rising_wedge_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to continuation rising wedge pattern over 60-day window. |
| 151 | `cont_v_bottom_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to continuation V-bottom pattern over 60-day window. |
| 152 | `cont_v_bottom_median_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to continuation V-bottom pattern over 60-day window. |
| 153 | `cont_v_bottom_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to continuation V-bottom pattern over 60-day window. |
| 154 | `cont_v_top_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to continuation V-top pattern over 60-day window. |
| 155 | `continuation_downward_wedge_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a continuation-style falling wedge pattern. |
| 156 | `continuation_downward_wedge_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a continuation-style falling wedge pattern. |
| 157 | `continuation_downward_wedge_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a continuation-style falling wedge pattern. |
| 158 | `continuation_downward_wedge_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a continuation-style falling wedge pattern. |
| 159 | `continuation_downward_wedge_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a continuation-style falling wedge pattern. |
| 160 | `continuation_upward_wedge_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a continuation-style rising wedge pattern. |
| 161 | `continuation_upward_wedge_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a continuation-style rising wedge pattern. |
| 162 | `continuation_upward_wedge_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a continuation-style rising wedge pattern. |
| 163 | `desc_triangle_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to descending triangle pattern over 60-day window. |
| 164 | `desc_triangle_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to descending triangle pattern over 60-day window. |
| 165 | `desc_triangle_std_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to descending triangle pattern over 60-day window. |
| 166 | `desc_triangle_up_dynamic_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to upward breakout descending triangle pattern over 60-day window. |
| 167 | `desc_triangle_up_min_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to upward breakout descending triangle pattern over 60-day window. |
| 168 | `desc_triangle_up_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to upward breakout descending triangle pattern over 60-day window. |
| 169 | `downward_gap_break_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a strong downward price gap pattern. |
| 170 | `downward_gap_break_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a strong downward price gap pattern. |
| 171 | `downward_gap_break_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a strong downward price gap pattern. |
| 172 | `downward_gap_break_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a strong downward price gap pattern. |
| 173 | `downward_wedge_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a falling wedge pattern. |
| 174 | `downward_wedge_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a falling wedge pattern. |
| 175 | `downward_wedge_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a falling wedge pattern. |
| 176 | `downward_wedge_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a falling wedge pattern. |
| 177 | `downward_wedge_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a falling wedge pattern. |
| 178 | `falling_wedge_dynamic_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to falling wedge pattern over 60-day window. |
| 179 | `falling_wedge_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to falling wedge pattern over 60-day window. |
| 180 | `regular_downward_gap_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a typical downward gap pattern. |
| 181 | `regular_downward_gap_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a typical downward gap pattern. |
| 182 | `regular_downward_gap_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a typical downward gap pattern. |
| 183 | `regular_downward_gap_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a typical downward gap pattern. |
| 184 | `regular_downward_gap_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a typical downward gap pattern. |
| 185 | `regular_upward_gap_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a typical upward gap pattern. |
| 186 | `regular_upward_gap_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a typical upward gap pattern. |
| 187 | `regular_upward_gap_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a typical upward gap pattern. |
| 188 | `reversal_v_bottom_median_simscore_lookback60` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score to V-bottom reversal pattern over 60-day window. |
| 189 | `reversal_v_top_max_simscore_lookback60` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score to V-top reversal pattern over 60-day window. |
| 190 | `reversal_v_top_median_simscore_lookback60` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score to V-top reversal pattern over 60-day window. |
| 191 | `reversal_v_top_min_simscore_lookback60` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score to V-top reversal pattern over 60-day window. |
| 192 | `rising_wedge_median_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to rising wedge pattern over 60-day window. |
| 193 | `rising_wedge_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to rising wedge pattern over 60-day window. |
| 194 | `symm_triangle_down_dynamic_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to downward symmetrical triangle pattern over 60-day window. |
| 195 | `symm_triangle_down_max_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to downward symmetrical triangle pattern over 60-day window. |
| 196 | `symm_triangle_down_mean_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to downward symmetrical triangle pattern over 60-day window. |
| 197 | `symm_triangle_down_median_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to downward symmetrical triangle pattern over 60-day window. |
| 198 | `symm_triangle_down_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to downward symmetrical triangle pattern over 60-day window. |
| 199 | `symm_triangle_up_dynamic_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to upward symmetrical triangle pattern over 60-day window. |
| 200 | `symm_triangle_up_q95_simscore_lookback60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to upward symmetrical triangle pattern over 60-day window. |
| 201 | `symmetry_triangle_downward_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a downward breakout symmetrical triangle pattern. |
| 202 | `symmetry_triangle_downward_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a downward breakout symmetrical triangle pattern. |
| 203 | `symmetry_triangle_upward_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching an upward breakout symmetrical triangle pattern. |
| 204 | `symmetry_triangle_upward_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching an upward breakout symmetrical triangle pattern. |
| 205 | `symmetry_triangle_upward_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching an upward breakout symmetrical triangle pattern. |
| 206 | `symmetry_triangle_upward_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching an upward breakout symmetrical triangle pattern. |
| 207 | `symmetry_triangle_upward_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching an upward breakout symmetrical triangle pattern. |
| 208 | `trendline_convergence_downward_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a downward breakout variant of rising support and flat resistance. |
| 209 | `trendline_convergence_downward_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a downward breakout variant of rising support and flat resistance. |
| 210 | `trendline_convergence_downward_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a downward breakout variant of rising support and flat resistance. |
| 211 | `trendline_convergence_downward_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a downward breakout variant of rising support and flat resistance. |
| 212 | `trendline_convergence_downward_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a downward breakout variant of rising support and flat resista |
| 213 | `trendline_convergence_downward_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a downward breakout variant of rising support and flat |
| 214 | `trendline_convergence_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a rising support and flat resistance pattern. |
| 215 | `trendline_convergence_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a rising support and flat resistance pattern. |
| 216 | `trendline_convergence_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a rising support and flat resistance pattern. |
| 217 | `trendline_convergence_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a rising support and flat resistance pattern. |
| 218 | `trendline_divergence_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a falling support and flat resistance pattern. |
| 219 | `trendline_divergence_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a falling support and flat resistance pattern. |
| 220 | `trendline_divergence_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a falling support and flat resistance pattern. |
| 221 | `trendline_divergence_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a falling support and flat resistance pattern. |
| 222 | `trendline_divergence_upward_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching an upward breakout variant of falling support and flat resistance. |
| 223 | `trendline_divergence_upward_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching an upward breakout variant of falling support and flat resistance. |
| 224 | `trendline_divergence_upward_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching an upward breakout variant of falling support and flat resistance. |
| 225 | `trendline_divergence_upward_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching an upward breakout variant of falling support and flat |
| 226 | `upward_gap_break_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a strong upward price gap pattern. |
| 227 | `upward_gap_break_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a strong upward price gap pattern. |
| 228 | `upward_gap_break_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a strong upward price gap pattern. |
| 229 | `upward_wedge_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a rising wedge pattern. |
| 230 | `upward_wedge_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a rising wedge pattern. |
| 231 | `upward_wedge_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a rising wedge pattern. |
| 232 | `upward_wedge_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a rising wedge pattern. |
| 233 | `upward_wedge_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a rising wedge pattern. |
| 234 | `v_shape_continuation_bottom_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a V-shaped continuation at the bottom pattern. |
| 235 | `v_shape_continuation_bottom_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a V-shaped continuation at the bottom pattern. |
| 236 | `v_shape_continuation_bottom_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a V-shaped continuation at the bottom pattern. |
| 237 | `v_shape_continuation_bottom_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a V-shaped continuation at the bottom pattern. |
| 238 | `v_shape_continuation_top_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a V-shaped continuation at the top pattern. |
| 239 | `v_shape_continuation_top_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a V-shaped continuation at the top pattern. |
| 240 | `v_shape_continuation_top_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a V-shaped continuation at the top pattern. |
| 241 | `v_shape_continuation_top_median_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for price chart matching a V-shaped continuation at the top pattern. |
| 242 | `v_shape_continuation_top_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a V-shaped continuation at the top pattern. |
| 243 | `v_shape_continuation_top_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a V-shaped continuation at the top pattern. |
| 244 | `v_shape_reversal_bottom_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a V-shaped reversal at the bottom pattern. |
| 245 | `v_shape_reversal_bottom_max_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for price chart matching a V-shaped reversal at the bottom pattern. |
| 246 | `v_shape_reversal_bottom_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a V-shaped reversal at the bottom pattern. |
| 247 | `v_shape_reversal_bottom_min_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for price chart matching a V-shaped reversal at the bottom pattern. |
| 248 | `v_shape_reversal_bottom_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a V-shaped reversal at the bottom pattern. |
| 249 | `v_shape_reversal_bottom_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a V-shaped reversal at the bottom pattern. |
| 250 | `v_shape_reversal_top_dynamic_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Adaptive similarity score for price chart matching a V-shaped reversal at the top pattern. |
| 251 | `v_shape_reversal_top_mean_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for price chart matching a V-shaped reversal at the top pattern. |
| 252 | `v_shape_reversal_top_quantile95_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for price chart matching a V-shaped reversal at the top pattern. |
| 253 | `v_shape_reversal_top_std_similarity` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for price chart matching a V-shaped reversal at the top pattern. |
| 254 | `adaptive_similarity_upward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the upward breakaway gap pattern over a 120-day window. |
| 255 | `asc_triangle_down_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to downward breakout ascending triangle pattern over 120-day window. |
| 256 | `asc_triangle_down_std_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to downward breakout ascending triangle pattern over 120-day window. |
| 257 | `asc_triangle_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to ascending triangle pattern over 120-day window. |
| 258 | `asc_triangle_max_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to ascending triangle pattern over 120-day window. |
| 259 | `asc_triangle_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to ascending triangle pattern over 120-day window. |
| 260 | `asc_triangle_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to ascending triangle pattern over 120-day window. |
| 261 | `avg_similarity_continuation_rising_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the continuation-flavored rising wedge pattern over a 120-day window. |
| 262 | `avg_similarity_downward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the downward breakaway gap pattern over a 120-day window. |
| 263 | `avg_similarity_falling_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the falling support and flat resistance triangle pattern over a 120-day window. |
| 264 | `avg_similarity_falling_wedge_pattern_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the falling wedge chart pattern over a 120-day window. |
| 265 | `avg_similarity_rising_wedge_pattern_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the rising wedge chart pattern over a 120-day window. |
| 266 | `avg_similarity_upward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the upward breakaway gap pattern over a 120-day window. |
| 267 | `avg_similarity_upward_symmetrical_triangle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the symmetrical triangle pattern with upward breakout bias. |
| 268 | `avg_similarity_v_continuation_top` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the V-shaped continuation pattern at the top. |
| 269 | `avg_similarity_v_reversal_bottom_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for the V-shaped reversal pattern at the bottom over a 120-day window. |
| 270 | `breakaway_gap_down_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to downward breakaway gap pattern over 120-day window. |
| 271 | `breakaway_gap_down_std_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to downward breakaway gap pattern over 120-day window. |
| 272 | `breakaway_gap_up_max_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to upward breakaway gap pattern over 120-day window. |
| 273 | `breakaway_gap_up_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to upward breakaway gap pattern over 120-day window. |
| 274 | `common_gap_down_max_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to common gap down pattern over 120-day window. |
| 275 | `common_gap_down_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to common gap down pattern over 120-day window. |
| 276 | `common_gap_down_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to common gap down pattern over 120-day window. |
| 277 | `common_gap_down_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to common gap down pattern over 120-day window. |
| 278 | `common_gap_down_q95_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to common gap down pattern over 120-day window. |
| 279 | `common_gap_up_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to common gap up pattern over 120-day window. |
| 280 | `cont_falling_wedge_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to continuation falling wedge pattern over 120-day window. |
| 281 | `cont_falling_wedge_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to continuation falling wedge pattern over 120-day window. |
| 282 | `cont_falling_wedge_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to continuation falling wedge pattern over 120-day window. |
| 283 | `cont_falling_wedge_std_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to continuation falling wedge pattern over 120-day window. |
| 284 | `cont_rising_wedge_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to continuation rising wedge pattern over 120-day window. |
| 285 | `cont_rising_wedge_std_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to continuation rising wedge pattern over 120-day window. |
| 286 | `cont_v_bottom_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to continuation V-bottom pattern over 120-day window. |
| 287 | `cont_v_top_max_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to continuation V-top pattern over 120-day window. |
| 288 | `cont_v_top_q95_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to continuation V-top pattern over 120-day window. |
| 289 | `desc_triangle_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to descending triangle pattern over 120-day window. |
| 290 | `desc_triangle_q95_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to descending triangle pattern over 120-day window. |
| 291 | `desc_triangle_up_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to upward breakout descending triangle pattern over 120-day window. |
| 292 | `desc_triangle_up_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to upward breakout descending triangle pattern over 120-day window. |
| 293 | `desc_triangle_up_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to upward breakout descending triangle pattern over 120-day window. |
| 294 | `desc_triangle_up_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to upward breakout descending triangle pattern over 120-day window. |
| 295 | `desc_triangle_up_q95_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to upward breakout descending triangle pattern over 120-day window. |
| 296 | `dynamic_similarity_continuation_rising_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the continuation-flavored rising wedge pattern over a 120-day window. |
| 297 | `dynamic_similarity_downward_ascending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the downward breakout variant of the ascending triangle pattern over a 120-day window. |
| 298 | `dynamic_similarity_downward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the typical downward gap pattern over a 120-day window. |
| 299 | `dynamic_similarity_falling_support_flat_resistance` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the falling support and flat resistance triangle pattern. |
| 300 | `dynamic_similarity_upward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the typical upward gap pattern over a 120-day window. |
| 301 | `dynamic_similarity_upward_symmetrical_triangle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the symmetrical triangle pattern with upward breakout bias. |
| 302 | `dynamic_similarity_v_continuation_bottom_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the V-shaped continuation pattern at the bottom over a 120-day window. |
| 303 | `dynamic_similarity_v_continuation_top_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the V-shaped continuation pattern at the top over a 120-day window. |
| 304 | `dynamic_similarity_v_reversal_bottom_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the V-shaped reversal pattern at the bottom over a 120-day window. |
| 305 | `falling_wedge_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to falling wedge pattern over 120-day window. |
| 306 | `falling_wedge_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to falling wedge pattern over 120-day window. |
| 307 | `falling_wedge_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to falling wedge pattern over 120-day window. |
| 308 | `max_similarity_continuation_falling_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the continuation-flavored falling wedge pattern over a 120-day window. |
| 309 | `max_similarity_continuation_rising_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the continuation-flavored rising wedge pattern over a 120-day window. |
| 310 | `max_similarity_downward_ascending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the downward breakout variant of the ascending triangle pattern over a 120-day window. |
| 311 | `max_similarity_downward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the downward breakaway gap pattern over a 120-day window. |
| 312 | `max_similarity_downward_symmetrical_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the symmetrical triangle pattern with downward breakout bias over a 120-day window. |
| 313 | `max_similarity_falling_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the falling support and flat resistance triangle pattern over a 120-day window. |
| 314 | `max_similarity_falling_wedge_pattern` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the falling wedge chart pattern. |
| 315 | `max_similarity_rising_wedge_pattern_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the rising wedge chart pattern over a 120-day window. |
| 316 | `max_similarity_upward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the typical upward gap pattern over a 120-day window. |
| 317 | `max_similarity_upward_descending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the upward breakout variant of the descending triangle pattern over a 120-day window. |
| 318 | `max_similarity_upward_symmetrical_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the symmetrical triangle pattern with upward breakout bias over a 120-day window. |
| 319 | `max_similarity_v_continuation_bottom` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the V-shaped continuation pattern at the bottom. |
| 320 | `max_similarity_v_reversal_bottom_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for the V-shaped reversal pattern at the bottom over a 120-day window. |
| 321 | `median_similarity_downward_ascending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the downward breakout variant of the ascending triangle pattern over a 120-day window. |
| 322 | `median_similarity_downward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the downward breakaway gap pattern over a 120-day window. |
| 323 | `median_similarity_falling_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the falling support and flat resistance triangle pattern over a 120-day window. |
| 324 | `median_similarity_rising_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the rising support and flat resistance triangle pattern over a 120-day window. |
| 325 | `median_similarity_upward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the typical upward gap pattern over a 120-day window. |
| 326 | `median_similarity_v_continuation_bottom_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the V-shaped continuation pattern at the bottom over a 120-day window. |
| 327 | `median_similarity_v_continuation_top_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the V-shaped continuation pattern at the top over a 120-day window. |
| 328 | `min_similarity_continuation_falling_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the continuation-flavored falling wedge pattern over a 120-day window. |
| 329 | `min_similarity_continuation_rising_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the continuation-flavored rising wedge pattern over a 120-day window. |
| 330 | `min_similarity_downward_ascending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the downward breakout variant of the ascending triangle pattern over a 120-day window. |
| 331 | `min_similarity_downward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the downward breakaway gap pattern over a 120-day window. |
| 332 | `min_similarity_upward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the upward breakaway gap pattern over a 120-day window. |
| 333 | `min_similarity_upward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the typical upward gap pattern over a 120-day window. |
| 334 | `min_similarity_upward_symmetrical_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the symmetrical triangle pattern with upward breakout bias over a 120-day window. |
| 335 | `min_similarity_v_continuation_bottom_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the V-shaped continuation pattern at the bottom over a 120-day window. |
| 336 | `min_similarity_v_continuation_top` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the V-shaped continuation pattern at the top. |
| 337 | `quantile95_similarity_continuation_falling_wedge_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the continuation-flavored falling wedge pattern over a 120-day window. |
| 338 | `quantile95_similarity_continuation_rising_wedge` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the continuation-flavored rising wedge pattern. |
| 339 | `quantile95_similarity_downward_ascending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the downward breakout variant of the ascending triangle pattern over a 120-day wind |
| 340 | `quantile95_similarity_downward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the downward breakaway gap pattern over a 120-day window. |
| 341 | `quantile95_similarity_falling_wedge_pattern` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the falling wedge chart pattern. |
| 342 | `quantile95_similarity_rising_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the rising support and flat resistance triangle pattern over a 120-day window. |
| 343 | `quantile95_similarity_rising_wedge_pattern_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the rising wedge chart pattern over a 120-day window. |
| 344 | `quantile95_similarity_upward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the upward breakaway gap pattern over a 120-day window. |
| 345 | `quantile95_similarity_upward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the typical upward gap pattern over a 120-day window. |
| 346 | `quantile95_similarity_upward_symmetrical_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the symmetrical triangle pattern with upward breakout bias over a 120-day window. |
| 347 | `quantile95_similarity_v_continuation_bottom_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the V-shaped continuation pattern at the bottom over a 120-day window. |
| 348 | `quantile95_similarity_v_reversal_bottom_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the V-shaped reversal pattern at the bottom over a 120-day window. |
| 349 | `quantile95_similarity_v_reversal_top_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the V-shaped reversal pattern at the top over a 120-day window. |
| 350 | `reversal_v_bottom_median_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score to V-bottom reversal pattern over 120-day window. |
| 351 | `reversal_v_bottom_min_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score to V-bottom reversal pattern over 120-day window. |
| 352 | `reversal_v_top_dynamic_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Dynamic similarity score to V-top reversal pattern over 120-day window. |
| 353 | `reversal_v_top_max_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score to V-top reversal pattern over 120-day window. |
| 354 | `reversal_v_top_mean_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean similarity score to V-top reversal pattern over 120-day window. |
| 355 | `reversal_v_top_median_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score to V-top reversal pattern over 120-day window. |
| 356 | `reversal_v_top_min_simscore_lookback120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score to V-top reversal pattern over 120-day window. |
| 357 | `rising_wedge_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to rising wedge pattern over 120-day window. |
| 358 | `rising_wedge_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to rising wedge pattern over 120-day window. |
| 359 | `rising_wedge_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to rising wedge pattern over 120-day window. |
| 360 | `stddev_similarity_downward_common_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the typical downward gap pattern over a 120-day window. |
| 361 | `stddev_similarity_falling_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the falling support and flat resistance triangle pattern over a 120-day wind |
| 362 | `stddev_similarity_falling_wedge_pattern_2` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the falling wedge chart pattern. |
| 363 | `stddev_similarity_rising_support_flat_resistance_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the rising support and flat resistance triangle pattern over a 120-day windo |
| 364 | `stddev_similarity_rising_wedge_pattern_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the rising wedge chart pattern over a 120-day window. |
| 365 | `stddev_similarity_upward_breakaway_gap_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the upward breakaway gap pattern over a 120-day window. |
| 366 | `stddev_similarity_upward_common_gap` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the typical upward gap pattern. |
| 367 | `stddev_similarity_upward_descending_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the upward breakout variant of the descending triangle pattern over a 120-da |
| 368 | `stddev_similarity_upward_symmetrical_triangle_120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the symmetrical triangle pattern with upward breakout bias over a 120-day wi |
| 369 | `stddev_similarity_v_continuation_bottom` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the V-shaped continuation pattern at the bottom. |
| 370 | `stddev_similarity_v_continuation_top` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the V-shaped continuation pattern at the top. |
| 371 | `stddev_similarity_v_reversal_bottom_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the V-shaped reversal pattern at the bottom over a 120-day window. |
| 372 | `stddev_similarity_v_reversal_top_120` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the V-shaped reversal pattern at the top over a 120-day window. |
| 373 | `symm_triangle_down_dynamic_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to downward symmetrical triangle pattern over 120-day window. |
| 374 | `symm_triangle_down_mean_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score to downward symmetrical triangle pattern over 120-day window. |
| 375 | `symm_triangle_down_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to downward symmetrical triangle pattern over 120-day window. |
| 376 | `symm_triangle_down_min_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to downward symmetrical triangle pattern over 120-day window. |
| 377 | `symm_triangle_down_q95_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to downward symmetrical triangle pattern over 120-day window. |
| 378 | `symm_triangle_down_std_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to downward symmetrical triangle pattern over 120-day window. |
| 379 | `symm_triangle_up_median_simscore_lookback120` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to upward symmetrical triangle pattern over 120-day window. |
| 380 | `adaptive_similarity_upward_gap_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score emphasizing recent bars for the upward breakaway gap pattern. |
| 381 | `avg_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the continuation-flavored falling wedge pattern. |
| 382 | `avg_similarity_downward_price_gap_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for the downward breakaway gap chart pattern. |
| 383 | `avg_similarity_downward_symmetrical_triangle` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the symmetrical triangle pattern with downward breakout bias. |
| 384 | `avg_similarity_falling_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the falling wedge chart pattern. |
| 385 | `avg_similarity_rising_support_flat_resistance` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the rising support and flat resistance triangle pattern. |
| 386 | `avg_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the rising wedge chart pattern. |
| 387 | `avg_similarity_upward_breakaway_gap` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the upward breakaway gap chart pattern. |
| 388 | `avg_similarity_v_reversal_bottom` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Average similarity score for the V-shaped reversal pattern at the bottom. |
| 389 | `dynamic_similarity_ascending_triangle_down` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the ascending triangle down chart pattern. |
| 390 | `dynamic_similarity_ascending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the ascending triangle chart pattern. |
| 391 | `dynamic_similarity_breakaway_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the breakaway gap down chart pattern. |
| 392 | `dynamic_similarity_common_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the common gap down chart pattern. |
| 393 | `dynamic_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the continuation falling wedge chart pattern. |
| 394 | `dynamic_similarity_continuation_rising_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the continuation rising wedge chart pattern. |
| 395 | `dynamic_similarity_continuation_v_bottom` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the continuation V-bottom chart pattern. |
| 396 | `dynamic_similarity_descending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the descending triangle chart pattern. |
| 397 | `dynamic_similarity_falling_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the falling wedge chart pattern. |
| 398 | `dynamic_similarity_reversal_v_top_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the reversal V-top chart pattern. |
| 399 | `dynamic_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the rising wedge chart pattern. |
| 400 | `dynamic_similarity_symmetrical_triangle_down` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the symmetrical triangle down chart pattern. |
| 401 | `dynamic_similarity_symmetrical_triangle_up` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamically weighted similarity score for the symmetrical triangle up chart pattern. |
| 402 | `dynamic_similarity_upward_common_gap` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Dynamic similarity score for the typical upward gap pattern in price charts. |
| 403 | `max_similarity_ascending_triangle_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the ascending triangle down chart pattern. |
| 404 | `max_similarity_breakaway_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the breakaway gap up chart pattern. |
| 405 | `max_similarity_common_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the common gap down chart pattern. |
| 406 | `max_similarity_common_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the common gap up chart pattern. |
| 407 | `max_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the continuation falling wedge chart pattern. |
| 408 | `max_similarity_continuation_rising_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the continuation rising wedge chart pattern. |
| 409 | `max_similarity_continuation_v_bottom_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the continuation V-bottom chart pattern. |
| 410 | `max_similarity_downward_symmetrical_triangle` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the symmetrical triangle pattern with downward breakout bias. |
| 411 | `max_similarity_reversal_v_bottom_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for the reversal V-bottom chart pattern. |
| 412 | `max_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the rising wedge chart pattern. |
| 413 | `max_similarity_symmetrical_triangle_up` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the symmetrical triangle up chart pattern. |
| 414 | `max_similarity_v_continuation_top` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the V-shaped continuation pattern at the top. |
| 415 | `max_similarity_v_reversal_top` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum similarity score for the V-shaped reversal pattern at the top. |
| 416 | `mean_similarity_ascending_triangle_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score for the ascending triangle down chart pattern. |
| 417 | `mean_similarity_common_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score for the common gap down chart pattern. |
| 418 | `mean_similarity_continuation_rising_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score for the continuation rising wedge chart pattern. |
| 419 | `mean_similarity_continuation_v_bottom_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score for the continuation V-bottom chart pattern. |
| 420 | `mean_similarity_descending_triangle_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score for the descending triangle up chart pattern. |
| 421 | `mean_similarity_reversal_v_top_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean similarity score for the reversal V-top chart pattern. |
| 422 | `mean_similarity_symmetrical_triangle_up` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Mean similarity score for the symmetrical triangle up chart pattern. |
| 423 | `median_similarity_ascending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the ascending triangle chart pattern. |
| 424 | `median_similarity_breakaway_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the breakaway gap down chart pattern. |
| 425 | `median_similarity_breakaway_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the breakaway gap up chart pattern. |
| 426 | `median_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the continuation falling wedge chart pattern. |
| 427 | `median_similarity_continuation_rising_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the continuation rising wedge chart pattern. |
| 428 | `median_similarity_continuation_v_bottom_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the continuation V-bottom chart pattern. |
| 429 | `median_similarity_continuation_v_top_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the continuation V-top chart pattern. |
| 430 | `median_similarity_descending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the descending triangle chart pattern. |
| 431 | `median_similarity_descending_triangle_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the descending triangle up chart pattern. |
| 432 | `median_similarity_downward_symmetrical_triangle` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the symmetrical triangle pattern with downward breakout bias. |
| 433 | `median_similarity_falling_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the falling wedge chart pattern. |
| 434 | `median_similarity_reversal_v_bottom_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for the reversal V-bottom chart pattern. |
| 435 | `median_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the rising wedge chart pattern. |
| 436 | `median_similarity_upward_symmetrical_triangle` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the symmetrical triangle pattern with upward breakout bias. |
| 437 | `median_similarity_v_reversal_top` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Median similarity score for the V-shaped reversal pattern at the top. |
| 438 | `min_similarity_ascending_triangle_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the ascending triangle down chart pattern. |
| 439 | `min_similarity_ascending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the ascending triangle chart pattern. |
| 440 | `min_similarity_breakaway_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the breakaway gap down chart pattern. |
| 441 | `min_similarity_breakaway_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the breakaway gap up chart pattern. |
| 442 | `min_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the continuation-flavored falling wedge pattern. |
| 443 | `min_similarity_continuation_rising_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the continuation rising wedge chart pattern. |
| 444 | `min_similarity_continuation_v_bottom_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the continuation V-bottom chart pattern. |
| 445 | `min_similarity_descending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the descending triangle chart pattern. |
| 446 | `min_similarity_descending_triangle_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the descending triangle up chart pattern. |
| 447 | `min_similarity_downward_symmetrical_triangle` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the symmetrical triangle pattern with downward breakout bias. |
| 448 | `min_similarity_falling_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the falling wedge chart pattern. |
| 449 | `min_similarity_reversal_v_top_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for the reversal V-top chart pattern. |
| 450 | `min_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the rising wedge chart pattern. |
| 451 | `min_similarity_symmetrical_triangle_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the symmetrical triangle up chart pattern. |
| 452 | `min_similarity_v_reversal_bottom` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum similarity score for the V-shaped reversal pattern at the bottom. |
| 453 | `quantile95_similarity_ascending_triangle_down` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the ascending triangle down chart pattern. |
| 454 | `quantile95_similarity_breakaway_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the breakaway gap down chart pattern. |
| 455 | `quantile95_similarity_common_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the common gap down chart pattern. |
| 456 | `quantile95_similarity_common_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the common gap up chart pattern. |
| 457 | `quantile95_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the continuation-flavored falling wedge pattern. |
| 458 | `quantile95_similarity_continuation_v_top_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the continuation V-top chart pattern. |
| 459 | `quantile95_similarity_descending_triangle_up` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the descending triangle up chart pattern. |
| 460 | `quantile95_similarity_falling_support_flat_resistance` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the falling support and flat resistance triangle pattern. |
| 461 | `quantile95_similarity_reversal_v_bottom_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the reversal V-bottom chart pattern. |
| 462 | `quantile95_similarity_reversal_v_top_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the reversal V-top chart pattern. |
| 463 | `quantile95_similarity_rising_support_flat_resistance` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the rising support and flat resistance triangle pattern. |
| 464 | `quantile95_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the rising wedge chart pattern. |
| 465 | `quantile95_similarity_symmetrical_triangle_down` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the symmetrical triangle down chart pattern. |
| 466 | `quantile95_similarity_symmetrical_triangle_up` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the symmetrical triangle up chart pattern. |
| 467 | `quantile95_similarity_v_continuation_bottom` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the V-shaped continuation pattern at the bottom. |
| 468 | `simscore_asc_triangle_down_median_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a down-breakout ascending triangle pattern over a 40-week window. |
| 469 | `simscore_asc_triangle_max_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to an ascending triangle pattern over a 40-week window. |
| 470 | `simscore_break_gap_down_max_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a breakaway gap down pattern over a 40-week window. |
| 471 | `simscore_break_gap_up_q95_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a breakaway gap up pattern over a 40-week window. |
| 472 | `simscore_common_gap_down_median_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a common gap down pattern over a 40-week window. |
| 473 | `simscore_common_gap_down_min_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a common gap down pattern over a 40-week window. |
| 474 | `simscore_common_gap_up_avg_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a common gap up pattern over a 40-week window. |
| 475 | `simscore_common_gap_up_median_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to a common gap up pattern over a 40-week window. |
| 476 | `simscore_common_gap_up_min_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a common gap up pattern over a 40-week window. |
| 477 | `simscore_cont_rising_wedge_q95_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a continuation rising wedge pattern over a 40-week window. |
| 478 | `simscore_cont_vtop_avg_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a continuation V-top pattern over a 40-week window. |
| 479 | `simscore_cont_vtop_dyn_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to a continuation V-top pattern over a 40-week window. |
| 480 | `simscore_cont_vtop_min_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to a continuation V-top pattern over a 40-week window. |
| 481 | `simscore_desc_triangle_avg_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to a descending triangle pattern over a 40-week window. |
| 482 | `simscore_desc_triangle_max_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a descending triangle pattern over a 40-week window. |
| 483 | `simscore_desc_triangle_up_dyn_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score to an up-breakout descending triangle pattern over a 40-week window. |
| 484 | `simscore_desc_triangle_up_max_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to an up-breakout descending triangle pattern over a 40-week window. |
| 485 | `simscore_falling_wedge_max_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to a falling wedge pattern over a 40-week window. |
| 486 | `simscore_falling_wedge_q95_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to a falling wedge pattern over a 40-week window. |
| 487 | `simscore_symm_triangle_down_stddev_40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to a down-breakout symmetrical triangle pattern over a 40-week window. |
| 488 | `stddev_similarity_breakaway_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the breakaway gap down chart pattern. |
| 489 | `stddev_similarity_breakaway_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the breakaway gap up chart pattern. |
| 490 | `stddev_similarity_common_gap_down_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the common gap down chart pattern. |
| 491 | `stddev_similarity_common_gap_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the common gap up chart pattern. |
| 492 | `stddev_similarity_continuation_falling_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the continuation falling wedge chart pattern. |
| 493 | `stddev_similarity_continuation_rising_wedge` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the continuation rising wedge chart pattern. |
| 494 | `stddev_similarity_continuation_v_bottom_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the continuation V-bottom chart pattern. |
| 495 | `stddev_similarity_continuation_v_top_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the continuation V-top chart pattern. |
| 496 | `stddev_similarity_descending_triangle_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the descending triangle chart pattern. |
| 497 | `stddev_similarity_descending_triangle_up_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the descending triangle up chart pattern. |
| 498 | `stddev_similarity_downward_ascending_triangle` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the downward breakout variant of the ascending triangle pattern. |
| 499 | `stddev_similarity_falling_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the falling wedge chart pattern. |
| 500 | `stddev_similarity_reversal_v_bottom_pattern` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the reversal V-bottom chart pattern. |
| 501 | `stddev_similarity_rising_support_flat_resistance` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the rising support and flat resistance pattern. |
| 502 | `stddev_similarity_rising_wedge_pattern` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the rising wedge chart pattern. |
| 503 | `stddev_similarity_symmetrical_triangle_up` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the symmetrical triangle up chart pattern. |
| 504 | `stddev_similarity_v_reversal_top` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the V-shaped reversal pattern at the top. |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `2rOd1gw6` | 0.03 | 0.00 | -0.06 | — | 0.10 | ["LOW_SHARPE | 123 | `quantile(subtract(ts_backfill(median_similarity_breakaway_gap_upward, 66), ts_backfill(ada` |
| `JjxKVANO` | 0.01 | 0.00 | -0.04 | — | 0.10 | ["LOW_SHARPE | 123 | `quantile(subtract(ts_backfill(mean_similarity_breakaway_gap_upward, 66), ts_backfill(adapt` |
| `ZY0GR8bZ` | -0.03 | 0.00 | 0.12 | — | 0.10 | ["LOW_SHARPE | 123 | `quantile(subtract(ts_backfill(max_similarity_breakaway_gap_upward, 66), ts_backfill(adapti` |
| `P0Z9JRgM` | -0.03 | 0.00 | 0.01 | — | 0.11 | ["LOW_SHARPE | 123 | `ts_covariance(ts_backfill(max_similarity_breakaway_gap_upward, 66), ts_backfill(avg_simila` |
| `A10KRpvd` | -0.15 | -0.03 | 0.24 | — | 0.14 | ["LOW_SHARPE | 123 | `quantile(add(multiply(0.4, ts_av_diff(ts_backfill(dynamic_similarity_reversal_v_bottom, 12` |
| `E5vJZjp9` | -0.29 | -0.08 | -0.11 | — | 0.12 | ["LOW_SHARPE | 123 | `quantile(subtract(ts_backfill(max_similarity_breakaway_gap_upward, 66), ts_backfill(avg_si` |
| `npKV1jPE` | -0.40 | -0.14 | -0.09 | — | 0.35 | ["LOW_SHARPE | 123 | `group_sum(ts_backfill(max_similarity_breakaway_gap_upward, 66), industry)` |
| `rK5X1qeo` | -0.77 | -0.30 | -0.24 | — | 0.13 | ["LOW_SHARPE | 123 | `quantile(add(multiply(0.4, ts_av_diff(ts_backfill(dynamic_similarity_reversal_v_bottom_pat` |

## 七、判死记录（sealed dead_end）

- `EUR-pattern_scores-wave83-skeleton-fail`（None）family=None：{"avg_fitness": -0.16, "avg_sharpe": -0.5, "dataset": "pattern_scores", "failed_checks": ["LOW_SHARPE", "LOW_FITNESS", "LOW_SUB_UNIVERSE_SHARPE", "LOW_2Y_SHARPE"], "failure_reason": "all_samples_negative_sharpe", "mode_b_qualification": "failed (best sharpe=-0.21 < 1.25)", "region": "EUR", "sample_count": 6, "settings": {"decay": 4, "delay": 1, "neutralization": "SUBINDUSTRY", "universe": "TOP2500
- `EUR-pattern_scores-BREAKAWAY-GAP-WEAK`（None）family=None：{"region": "EUR", "dataset": "pattern_scores", "family": "EUR-pattern_scores-BREAKAWAY-GAP-WEAK", "reason": "breakaway_gap \u5b57\u6bb5\u65cf\u4fe1\u53f7\u5f31\uff0c8 \u6761\u5168\u706d\uff0c\u6700\u9ad8 Sharpe 0.03", "wave": "123", "source": "wave123_s4"}
- `EUR-PATTERN-BREAKAWAY-RESID-WEAK`（2026-08-23）family=pattern_scores breakaway residual alone：{"dataset": "pattern_scores", "example_id": "mLjqbk0X", "max_sharpe": 0.71, "reason": "Breakaway-gap residual/invert max S0.71 F0.29. PV pyramid but weak as standalone. Wj71Q12o used gap as 0.60 mix with FCF; gap-only residual is not a RA path. Do not clone Wj71Q12o mix.", "wave": 35}
- `EUR-STAR-GAP-FACTOR-NEUT-WEAK`（2026-08-25）family=predictive_starmine surprise x common_gap_up factor neutralization：{"dataset": "predictive_starmine,pattern_scores", "id": "EUR-STAR-GAP-FACTOR-NEUT-WEAK", "max_sharpe": 1.79, "note": "STAT/CROWDING/FAST/SLOW/SAF/RAM on winning ts_delta10 mix; FAST F0.92 2Y1.54 ladder fail; do not retry factor neut to lift RN", "reason": "factor neutralization kills F vs SUBINDUSTRY, does not produce RN>1", "wave": 76}
- `EUR-STAR-PV-ASCT-TREND-WEAK`（2026-08-25）family=pattern_scores asc_triangle / support-resistance / trendline / regular gap as fast legs：{"dataset": "pattern_scores", "id": "EUR-STAR-PV-ASCT-TREND-WEAK", "max_sharpe": 1.46, "note": "mix with surprise 22d; best asc_triangle_down S1.46 F0.75; do not retry these PV families as fast legs", "reason": "unused PV families weak vs common_gap_up winner", "wave": 77}
- `EUR-STAR-ARM-LEFTOVER-WEAK`（2026-08-25）family=starmine ARM preferred/revenue/score-change/region-global as slow; regular_upward_gap as fast：{"dataset": "predictive_starmine,pattern_scores", "id": "EUR-STAR-ARM-LEFTOVER-WEAK", "max_sharpe": 1.55, "note": "best ARM score change 30d S1.55 F0.78; regular_upward_gap S1.04; do not retry ARM leftover or regular_upward_gap", "reason": "weaker than surprise x common_gap_up", "wave": 79}
- `EUR-shortinterest6-CHANGE-OWNER-WEAK`（2026-09-03）family=shortinterest6 change/owner component：{"best_2y": 1.15, "best_alpha": "YP5GKerl", "best_sharpe": 1.24, "contract_ops": "ts_covariance/group_sum 双槽失效（S-0.20/-0.27）", "dataset": "shortinterest6", "direction": "change 正向（S1.24）、owner 反向（S-0.07 原始，镜像+0.07）", "evidence": "wave109 9 条全灭：change/owner 组件（ts_zscore/ts_rank/ts_ir/rank 差值）最高 Sharpe 1.24 未达 1.58 硬闸", "not_dead": "0.40 minority slow mix × 0.60 pattern_scores 快腿（win recipe）未测，short
- `EUR-shortinterest6-PATTERN-MIX-PROD`（2026-09-03）family=shortinterest6 × pattern_scores win mix：{"best_2y": 2.22, "best_alpha": "O0rEaKwR", "best_sharpe": 1.63, "evidence": "wave110 10 条：2 条全硬闸通过（O0rEaKwR S1.63/F1.07/2Y2.22、JjxZKRmn S1.71/F1.11/2Y2.10）但 prod_corr 0.7404/0.7655 超 0.7 硬闸", "not_dead": "win recipe 结构有效（Sharpe 突破 1.58），但 star_hold 家族与 pattern_scores 快腿组合 prod 墙 0.74-0.77；需 Mode B 换字段组合（如换慢腿字段或快腿字段）或镜像稀释破墙", "reason": "star_hold 家族与 pattern_scores 快腿组合 prod_corr 0.74-0.77 超 0.7 硬
- `EUR-shortinterest6-PATTERN-FAST-LEG-PROD`（2026-09-03）family=shortinterest6 × pattern_scores fast leg variants：{"best_2y": 1.53, "best_alpha": "rK5vmoMJ", "best_sharpe": 1.38, "evidence": "wave111 9 条：Mode B 换 pattern_scores 快腿字段（breakaway_gap_up/common_gap_up max/min/q95/dynamic）最高 Sharpe 1.38 未达 1.58 硬闸", "not_dead": "shortinterest6 慢腿与其他数据集快腿（非 pattern_scores）组合未测；但 pattern_scores 快腿与 star_hold 慢腿组合 prod 墙 0.74-0.90 已确认", "reason": "star_hold 家族与任何 pattern_scores 快腿组合 prod_corr 必超 0.7（wave110 0.74-0.77）

