# continuation_score — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `continuation_score` |
| 名称 | Price Chart Continuation Pattern Similarity |
| 类别 | PV |
| 数据字段数(平台) | 560 |
| 覆盖率 | 0.9924 |
| 平台已有 alpha | 35 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily, per-stock similarity scores that measure how closely a stock’s price chart matches well-known continuation-style technical patterns, such as flags, pennants, rectangles, channels, scallops, staircases, cup-and-handle, and gap formations. The scores are derived by comparing chart-image embeddings to a curated library of canonical continuation patterns using advanced machine learning techniques. Multiple summary statistics (mean, median, max, dynamic, etc.) are available across different time horizons and regions, enabling flexible analysis. These similarity scores can be used to identify stocks likely to resume their current trend after consolidation, support trend-following strategies, and enhance alpha generation by confirming or filtering trading signals. The

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **560** |
| 类型分布 | MATRIX×560 |
| 平均覆盖率 | **0.992** |
| 覆盖率区间 | 0.98 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 560 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 545 | 97.3% |
| DEAD | 15 | 2.7% |

- 已实测字段：**15** 个（3%），best_sharpe 最高 **0.56**，中位 0.02

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 560 | 0.99 | bull_pennant_95th_similarity_h40、bull_flag_mid_similarity_h40、downward_scallop_recent_similarity_h40 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `bull_pennant_95th_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 4 | 0.56 | -0.79 | — | DEAD | 95th percentile similarity score for the bullish pennant pattern (40-day horizon). |
| 2 | `bull_flag_mid_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 2 | 0.39 | -0.29 | — | DEAD | Median similarity score for the bullish flag pattern (40-day horizon). |
| 3 | `downward_scallop_recent_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 1 | 0.28 | 0.11 | — | DEAD | Similarity score for the most recent downward scallop pattern (40-day horizon). |
| 4 | `ascending_staircase_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 1 | 0.19 | 0.48 | — | DEAD | 95th percentile similarity score for ascending staircase pattern. |
| 5 | `ascending_channel_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 1 | 0.13 | 0.83 | — | DEAD | Standard deviation of similarity scores for ascending channel pattern. |
| 6 | `bear_cup_handle_95th_similarity` | MATRIX | 0.998 | 风险与质量 | 1 | 0.12 | 0.60 | — | DEAD | 95th percentile similarity score for the inverse cup and handle pattern. |
| 7 | `ascending_channel_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 1 | 0.05 | -1.11 | — | DEAD | Highest similarity score to the ascending channel pattern over a 40-week horizon. |
| 8 | `bear_rectangle_95th_similarity` | MATRIX | 0.998 | 风险与质量 | 1 | 0.02 | 0.62 | — | DEAD | 95th percentile similarity score for the bearish rectangle pattern. |
| 9 | `gap_up_continuation_similarity_average` | MATRIX | 0.994 | 风险与质量 | 1 | -0.07 | 0.14 | — | DEAD | Average similarity score for upward gap continuation pattern. |
| 10 | `cup_handle_recent_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 1 | -0.13 | -0.42 | — | DEAD | Similarity score for the most recent cup and handle pattern (40-day horizon). |
| 11 | `ascending_channel_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 1 | -0.14 | — | — | DEAD | Similarity score for ascending channel pattern focusing on recent data. |
| 12 | `bearish_rectangle_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 1 | -0.18 | -0.41 | — | DEAD | 95th percentile similarity score for bearish rectangle pattern. |
| 13 | `cup_handle_similarity_average` | MATRIX | 0.994 | 风险与质量 | 1 | -0.22 | — | — | DEAD | Average similarity score for cup and handle pattern. |
| 14 | `descending_channel_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 3 | -0.38 | -0.07 | — | DEAD | Standard deviation of similarity scores for descending channel pattern. |
| 15 | `median_upward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 3 | -0.50 | -0.76 | — | DEAD | Median similarity score to upward gap continuation pattern over 60 days. |
| 16 | `avg_similarity_ascending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the ascending channel pattern. |
| 17 | `avg_similarity_ascending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the ascending staircase pattern. |
| 18 | `avg_similarity_bearish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish flag pattern. |
| 19 | `avg_similarity_bearish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish pennant pattern. |
| 20 | `avg_similarity_bearish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish rectangle pattern. |
| 21 | `avg_similarity_bullish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bullish rectangle pattern. |
| 22 | `avg_similarity_continuation_gap_down` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the continuation gap down pattern. |
| 23 | `avg_similarity_descending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the descending channel pattern. |
| 24 | `avg_similarity_inverse_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the inverse cup and handle pattern. |
| 25 | `avg_similarity_inverse_dead_cat_recovery` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the inverse dead cat bounce pattern. |
| 26 | `avg_similarity_inverted_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the inverted ascending scallop pattern. |
| 27 | `bear_pennant_95th_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the bearish pennant pattern (40-day horizon). |
| 28 | `bear_pennant_recent_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent bearish pennant pattern (40-day horizon). |
| 29 | `bear_rectangle_mid_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the bearish rectangle pattern. |
| 30 | `bear_rectangle_similarity_dispersion` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the bearish rectangle pattern. |
| 31 | `bull_flag_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the bullish flag pattern (40-day horizon). |
| 32 | `bull_flag_min_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the bullish flag pattern (40-day horizon). |
| 33 | `bull_flag_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the bullish flag pattern (40-day horizon). |
| 34 | `bull_flag_recent_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent bullish flag pattern (40-day horizon). |
| 35 | `bull_flag_similarity_dispersion_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the bullish flag pattern (40-day horizon). |
| 36 | `bull_pennant_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the bullish pennant pattern (40-day horizon). |
| 37 | `bull_pennant_min_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the bullish pennant pattern (40-day horizon). |
| 38 | `bull_pennant_similarity_dispersion_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the bullish pennant pattern (40-day horizon). |
| 39 | `bull_rectangle_95th_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the bullish rectangle pattern. |
| 40 | `cup_handle_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the cup and handle pattern (40-day horizon). |
| 41 | `cup_handle_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the cup and handle pattern (40-day horizon). |
| 42 | `cup_handle_similarity_dispersion_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the cup and handle pattern (40-day horizon). |
| 43 | `downward_channel_95th_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the descending channel pattern (40-day horizon). |
| 44 | `downward_channel_min_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the descending channel pattern (40-day horizon). |
| 45 | `downward_channel_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the descending channel pattern (40-day horizon). |
| 46 | `downward_channel_similarity_dispersion_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the descending channel pattern (40-day horizon). |
| 47 | `downward_gap_mid_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the downward gap pattern (40-day horizon). |
| 48 | `downward_gap_min_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the downward gap pattern. |
| 49 | `downward_gap_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the downward gap pattern (40-day horizon). |
| 50 | `downward_gap_recent_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent downward gap pattern. |
| 51 | `downward_gap_similarity_dispersion_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the downward gap pattern (40-day horizon). |
| 52 | `downward_scallop_95th_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the downward scallop pattern (40-day horizon). |
| 53 | `downward_scallop_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the downward scallop pattern (40-day horizon). |
| 54 | `downward_scallop_min_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the downward scallop pattern (40-day horizon). |
| 55 | `downward_staircase_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the downward staircase pattern (40-day horizon). |
| 56 | `downward_staircase_mid_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the downward staircase pattern (40-day horizon). |
| 57 | `downward_staircase_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the downward staircase pattern (40-day horizon). |
| 58 | `downward_staircase_recent_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent downward staircase pattern (40-day horizon). |
| 59 | `drop_after_rise_95th_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the inverse dead cat bounce pattern. |
| 60 | `drop_after_rise_recent_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent inverse dead cat bounce pattern. |
| 61 | `drop_after_rise_similarity_dispersion` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the inverse dead cat bounce pattern. |
| 62 | `flipped_downward_scallop_avg_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the inverted downward scallop pattern. |
| 63 | `flipped_downward_scallop_mid_similarity_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the inverted downward scallop pattern. |
| 64 | `flipped_upward_scallop_min_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the inverted upward scallop pattern. |
| 65 | `flipped_upward_scallop_similarity_dispersion` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the inverted upward scallop pattern. |
| 66 | `median_similarity_ascending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the ascending channel pattern. |
| 67 | `median_similarity_ascending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the ascending staircase pattern. |
| 68 | `median_similarity_bearish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bearish flag pattern. |
| 69 | `median_similarity_bearish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bearish pennant pattern. |
| 70 | `median_similarity_bullish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bullish pennant pattern. |
| 71 | `median_similarity_bullish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bullish rectangle pattern. |
| 72 | `median_similarity_continuation_gap_up` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the continuation gap up pattern. |
| 73 | `median_similarity_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the cup and handle pattern. |
| 74 | `median_similarity_dead_cat_bounce` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the dead cat bounce pattern. |
| 75 | `median_similarity_descending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the descending channel pattern. |
| 76 | `median_similarity_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the descending scallop pattern. |
| 77 | `median_similarity_inverse_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the inverse cup and handle pattern. |
| 78 | `median_similarity_inverse_dead_cat_recovery` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the inverse dead cat bounce pattern. |
| 79 | `median_similarity_inverted_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the inverted ascending scallop pattern. |
| 80 | `min_similarity_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the ascending scallop pattern. |
| 81 | `min_similarity_bearish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the bearish flag pattern. |
| 82 | `min_similarity_bearish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the bearish pennant pattern. |
| 83 | `min_similarity_bearish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the bearish rectangle pattern. |
| 84 | `min_similarity_bullish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the bullish rectangle pattern. |
| 85 | `min_similarity_continuation_gap_up` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the continuation gap up pattern. |
| 86 | `min_similarity_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the cup and handle pattern. |
| 87 | `min_similarity_descending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the descending staircase pattern. |
| 88 | `min_similarity_inverse_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the inverse cup and handle pattern. |
| 89 | `min_similarity_inverse_dead_cat_recovery` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the inverse dead cat bounce pattern. |
| 90 | `min_similarity_inverted_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the inverted descending scallop pattern. |
| 91 | `peak_similarity_ascending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the ascending channel pattern. |
| 92 | `peak_similarity_bearish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the bearish flag pattern. |
| 93 | `peak_similarity_bearish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the bearish pennant pattern. |
| 94 | `peak_similarity_bearish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the bearish rectangle pattern. |
| 95 | `peak_similarity_bullish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the bullish pennant pattern. |
| 96 | `peak_similarity_bullish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the bullish rectangle pattern. |
| 97 | `peak_similarity_dead_cat_bounce` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the dead cat bounce pattern. |
| 98 | `peak_similarity_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the descending scallop pattern. |
| 99 | `peak_similarity_inverse_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the inverse cup and handle pattern. |
| 100 | `peak_similarity_inverse_dead_cat_recovery` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the inverse dead cat bounce pattern. |
| 101 | `peak_similarity_inverted_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the inverted ascending scallop pattern. |
| 102 | `peak_similarity_inverted_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the inverted descending scallop pattern. |
| 103 | `quantile95_similarity_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the ascending scallop pattern. |
| 104 | `quantile95_similarity_ascending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the ascending staircase pattern. |
| 105 | `quantile95_similarity_bearish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bearish flag pattern. |
| 106 | `quantile95_similarity_bullish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bullish flag pattern. |
| 107 | `quantile95_similarity_continuation_gap_down` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the continuation gap down pattern. |
| 108 | `quantile95_similarity_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the cup and handle pattern. |
| 109 | `quantile95_similarity_dead_cat_bounce` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the dead cat bounce pattern. |
| 110 | `quantile95_similarity_descending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the descending staircase pattern. |
| 111 | `quantile95_similarity_inverted_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the inverted ascending scallop pattern. |
| 112 | `quantile95_similarity_inverted_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the inverted descending scallop pattern. |
| 113 | `rebound_after_drop_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the dead cat bounce pattern (40-day horizon). |
| 114 | `rebound_after_drop_min_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the dead cat bounce pattern. |
| 115 | `recent_similarity_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the ascending scallop pattern. |
| 116 | `recent_similarity_ascending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the ascending staircase pattern. |
| 117 | `recent_similarity_bearish_flag_pattern` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the bearish flag pattern. |
| 118 | `recent_similarity_bearish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the bearish rectangle pattern. |
| 119 | `recent_similarity_bullish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the bullish pennant pattern. |
| 120 | `recent_similarity_bullish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the bullish rectangle pattern. |
| 121 | `recent_similarity_dead_cat_bounce` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the dead cat bounce pattern. |
| 122 | `recent_similarity_descending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the descending channel pattern. |
| 123 | `recent_similarity_inverse_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the inverse cup and handle pattern. |
| 124 | `recent_similarity_inverted_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the inverted ascending scallop pattern. |
| 125 | `recent_similarity_inverted_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the inverted descending scallop pattern. |
| 126 | `stddev_similarity_ascending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the ascending channel pattern. |
| 127 | `stddev_similarity_ascending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the ascending scallop pattern. |
| 128 | `stddev_similarity_bearish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bearish flag pattern. |
| 129 | `stddev_similarity_bearish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bearish pennant pattern. |
| 130 | `stddev_similarity_bullish_rectangle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bullish rectangle pattern. |
| 131 | `stddev_similarity_continuation_gap_up` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the continuation gap up pattern. |
| 132 | `stddev_similarity_dead_cat_bounce` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the dead cat bounce pattern. |
| 133 | `stddev_similarity_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the descending scallop pattern. |
| 134 | `stddev_similarity_descending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the descending staircase pattern. |
| 135 | `stddev_similarity_inverse_cup_handle` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the inverse cup and handle pattern. |
| 136 | `stddev_similarity_inverted_descending_scallop` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the inverted descending scallop pattern. |
| 137 | `upward_channel_95th_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the ascending channel pattern. |
| 138 | `upward_channel_min_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the ascending channel pattern (40-day horizon). |
| 139 | `upward_channel_recent_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent ascending channel pattern. |
| 140 | `upward_gap_95th_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the upward gap pattern. |
| 141 | `upward_gap_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the upward gap pattern (40-day horizon). |
| 142 | `upward_gap_peak_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the upward gap pattern. |
| 143 | `upward_gap_recent_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent upward gap pattern. |
| 144 | `upward_scallop_avg_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the upward scallop pattern (40-day horizon). |
| 145 | `upward_scallop_mid_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the upward scallop pattern (40-day horizon). |
| 146 | `upward_scallop_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the upward scallop pattern (40-day horizon). |
| 147 | `upward_staircase_min_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the ascending staircase pattern (40-day horizon). |
| 148 | `upward_staircase_peak_similarity_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the ascending staircase pattern (40-day horizon). |
| 149 | `upward_staircase_similarity_dispersion_h40` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the ascending staircase pattern (40-day horizon). |
| 150 | `ascending_staircase_similarity_median_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the ascending staircase pattern over a 60-day horizon. |
| 151 | `ascending_staircase_similarity_minimum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the ascending staircase pattern over a 60-day horizon. |
| 152 | `avg_similarity_bullish_flag` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bullish flag pattern. |
| 153 | `avg_similarity_continuation_gap_up` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the continuation gap up pattern. |
| 154 | `avg_similarity_inverted_ascending_scallop_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the inverted ascending scallop pattern. |
| 155 | `bearish_pennant_similarity_95th_percentile_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bearish pennant pattern over a 60-day horizon. |
| 156 | `bearish_pennant_similarity_maximum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the bearish pennant pattern over a 60-day horizon. |
| 157 | `bearish_rectangle_similarity_average_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish rectangle pattern over a 60-day horizon. |
| 158 | `bullish_flag_similarity_maximum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the bullish flag pattern over a 60-day horizon. |
| 159 | `bullish_flag_similarity_median_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bullish flag pattern over a 60-day horizon. |
| 160 | `bullish_rectangle_similarity_dynamic_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the bullish rectangle pattern over a 60-day horizon. |
| 161 | `bullish_rectangle_similarity_maximum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the bullish rectangle pattern over a 60-day horizon. |
| 162 | `cup_and_handle_similarity_maximum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the cup and handle pattern over a 60-day horizon. |
| 163 | `descending_scallop_similarity_95th_percentile_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the descending scallop pattern over a 60-day horizon. |
| 164 | `descending_scallop_similarity_dynamic_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the descending scallop pattern over a 60-day horizon. |
| 165 | `descending_scallop_similarity_maximum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the descending scallop pattern over a 60-day horizon. |
| 166 | `descending_staircase_similarity_95th_percentile_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the descending staircase pattern over a 60-day horizon. |
| 167 | `descending_staircase_similarity_minimum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the descending staircase pattern over a 60-day horizon. |
| 168 | `dynamic_ascending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to ascending channel pattern. |
| 169 | `dynamic_ascending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to ascending staircase pattern. |
| 170 | `dynamic_bear_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to bearish flag pattern. |
| 171 | `dynamic_bear_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to bearish rectangle pattern. |
| 172 | `dynamic_bull_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to bullish flag pattern. |
| 173 | `dynamic_bull_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to bullish pennant pattern. |
| 174 | `dynamic_cup_handle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to cup-and-handle pattern. |
| 175 | `dynamic_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to dead cat bounce pattern. |
| 176 | `dynamic_descending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to descending channel pattern. |
| 177 | `dynamic_descending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to descending staircase pattern. |
| 178 | `dynamic_downward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to downward gap continuation pattern. |
| 179 | `dynamic_inverse_cup_handle_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to inverse cup-and-handle pattern. |
| 180 | `dynamic_inverse_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to inverse dead cat bounce pattern. |
| 181 | `dynamic_inverted_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to inverted ascending scallop pattern. |
| 182 | `dynamic_upward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent-bar weighted similarity score to upward gap continuation pattern. |
| 183 | `gap_down_continuation_similarity_maximum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the downward gap continuation pattern over a 60-day horizon. |
| 184 | `inverse_cup_and_handle_similarity_average_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the inverse cup and handle pattern over a 60-day horizon. |
| 185 | `inverse_dead_cat_bounce_similarity_minimum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the inverse dead cat bounce pattern over a 60-day horizon. |
| 186 | `inverted_descending_scallop_similarity_95th_percentile_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the inverted descending scallop pattern over a 60-day horizon. |
| 187 | `inverted_descending_scallop_similarity_minimum_h60` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the inverted descending scallop pattern over a 60-day horizon. |
| 188 | `max_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to ascending scallop pattern over 60 days. |
| 189 | `max_ascending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to ascending staircase pattern over 60 days. |
| 190 | `max_bear_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to bearish rectangle pattern over 60 days. |
| 191 | `max_bull_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to bullish pennant pattern over the 60-day horizon. |
| 192 | `max_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to dead cat bounce pattern over 60 days. |
| 193 | `max_descending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to descending channel pattern over 60 days. |
| 194 | `max_inverse_cup_handle_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to inverse cup-and-handle pattern over 60 days. |
| 195 | `max_inverse_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to inverse dead cat bounce pattern over 60 days. |
| 196 | `max_inverted_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to inverted ascending scallop pattern over 60 days. |
| 197 | `max_inverted_descending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to inverted descending scallop pattern over 60 days. |
| 198 | `max_upward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to upward gap continuation pattern over 60 days. |
| 199 | `mean_ascending_channel_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to ascending channel pattern over the 60-day horizon. |
| 200 | `mean_ascending_scallop_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to ascending scallop pattern over the 60-day horizon. |
| 201 | `mean_ascending_staircase_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to ascending staircase pattern over the 60-day horizon. |
| 202 | `mean_bear_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to bearish flag pattern over the 60-day horizon. |
| 203 | `mean_bear_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to bearish pennant pattern over the 60-day horizon. |
| 204 | `mean_bull_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to bullish pennant pattern over the 60-day horizon. |
| 205 | `mean_bull_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to bullish rectangle pattern over the 60-day horizon. |
| 206 | `mean_cup_handle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to cup-and-handle pattern over the 60-day horizon. |
| 207 | `mean_dead_cat_bounce_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to dead cat bounce pattern over the 60-day horizon. |
| 208 | `mean_descending_channel_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to descending channel pattern over the 60-day horizon. |
| 209 | `mean_descending_scallop_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to descending scallop pattern over the 60-day horizon. |
| 210 | `mean_descending_staircase_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to descending staircase pattern over the 60-day horizon. |
| 211 | `mean_downward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to downward gap continuation pattern over the 60-day horizon. |
| 212 | `mean_inverse_dead_cat_bounce_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to inverse dead cat bounce pattern over the 60-day horizon. |
| 213 | `mean_inverted_descending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to inverted descending scallop pattern over the 60-day horizon. |
| 214 | `median_ascending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to ascending channel pattern over 60 days. |
| 215 | `median_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to ascending scallop pattern over 60 days. |
| 216 | `median_bear_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to bearish flag pattern over the 60-day horizon. |
| 217 | `median_bear_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to bearish rectangle pattern over 60 days. |
| 218 | `median_bull_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to bullish rectangle pattern over 60 days. |
| 219 | `median_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to dead cat bounce pattern over 60 days. |
| 220 | `median_descending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to descending channel pattern over 60 days. |
| 221 | `median_descending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to descending scallop pattern over 60 days. |
| 222 | `median_descending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to descending staircase pattern over 60 days. |
| 223 | `median_downward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to downward gap continuation pattern over 60 days. |
| 224 | `median_inverse_cup_handle_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to inverse cup-and-handle pattern over 60 days. |
| 225 | `median_inverted_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to inverted ascending scallop pattern over 60 days. |
| 226 | `median_inverted_descending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to inverted descending scallop pattern over 60 days. |
| 227 | `median_similarity_bearish_pennant_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bearish pennant pattern. |
| 228 | `median_similarity_bullish_pennant_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bullish pennant pattern. |
| 229 | `median_similarity_cup_handle_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the cup and handle pattern. |
| 230 | `median_similarity_inverse_dead_cat_recovery_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the inverse dead cat bounce pattern. |
| 231 | `min_ascending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to ascending channel pattern over 60 days. |
| 232 | `min_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to ascending scallop pattern over 60 days. |
| 233 | `min_bear_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to bearish pennant pattern over 60 days. |
| 234 | `min_bear_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to bearish rectangle pattern over 60 days. |
| 235 | `min_bull_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to bullish flag pattern over 60 days. |
| 236 | `min_bull_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to bullish pennant pattern over 60 days. |
| 237 | `min_bull_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to bullish rectangle pattern over 60 days. |
| 238 | `min_cup_handle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to cup-and-handle pattern over 60 days. |
| 239 | `min_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to dead cat bounce pattern over 60 days. |
| 240 | `min_descending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to descending channel pattern over 60 days. |
| 241 | `min_descending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to descending scallop pattern over 60 days. |
| 242 | `min_downward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to downward gap continuation pattern over 60 days. |
| 243 | `min_inverse_cup_handle_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to inverse cup-and-handle pattern over 60 days. |
| 244 | `min_inverted_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to inverted ascending scallop pattern over 60 days. |
| 245 | `min_similarity_bearish_flag_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to the bearish flag pattern. |
| 246 | `min_upward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score to upward gap continuation pattern over 60 days. |
| 247 | `peak_similarity_ascending_channel_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the ascending channel pattern. |
| 248 | `peak_similarity_bearish_flag_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the bearish flag pattern. |
| 249 | `peak_similarity_descending_staircase` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score to the descending staircase pattern. |
| 250 | `quantile95_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to ascending scallop pattern over 60 days. |
| 251 | `quantile95_ascending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to ascending staircase pattern over 60 days. |
| 252 | `quantile95_bear_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to bearish rectangle pattern over 60 days. |
| 253 | `quantile95_bull_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to bullish flag pattern over 60 days. |
| 254 | `quantile95_bull_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to bullish rectangle pattern over 60 days. |
| 255 | `quantile95_cup_handle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to cup-and-handle pattern over 60 days. |
| 256 | `quantile95_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to dead cat bounce pattern over 60 days. |
| 257 | `quantile95_descending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to descending channel pattern over 60 days. |
| 258 | `quantile95_downward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to downward gap continuation pattern over 60 days. |
| 259 | `quantile95_inverse_cup_handle_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to inverse cup-and-handle pattern over 60 days. |
| 260 | `quantile95_inverted_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to inverted ascending scallop pattern over 60 days. |
| 261 | `quantile95_similarity_ascending_channel` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the ascending channel pattern. |
| 262 | `quantile95_similarity_bearish_flag_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bearish flag pattern. |
| 263 | `quantile95_similarity_bullish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bullish pennant pattern. |
| 264 | `quantile95_similarity_inverse_dead_cat_recovery` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the inverse dead cat bounce pattern. |
| 265 | `quantile95_upward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to upward gap continuation pattern over 60 days. |
| 266 | `recent_similarity_ascending_scallop_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the ascending scallop pattern. |
| 267 | `recent_similarity_bearish_pennant` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the bearish pennant pattern. |
| 268 | `recent_similarity_inverted_descending_scallop_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Most recent similarity score to the inverted descending scallop pattern. |
| 269 | `stddev_ascending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to ascending channel pattern over 60 days. |
| 270 | `stddev_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to ascending scallop pattern over 60 days. |
| 271 | `stddev_ascending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to ascending staircase pattern over 60 days. |
| 272 | `stddev_bear_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to bearish flag pattern over 60 days. |
| 273 | `stddev_bear_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to bearish pennant pattern over 60 days. |
| 274 | `stddev_bear_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to bearish rectangle pattern over 60 days. |
| 275 | `stddev_bull_flag_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to bullish flag pattern over 60 days. |
| 276 | `stddev_bull_pennant_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to bullish pennant pattern over 60 days. |
| 277 | `stddev_bull_rectangle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to bullish rectangle pattern over 60 days. |
| 278 | `stddev_cup_handle_similarity_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to cup-and-handle pattern over 60 days. |
| 279 | `stddev_dead_cat_bounce_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to dead cat bounce pattern over 60 days. |
| 280 | `stddev_descending_channel_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to descending channel pattern over 60 days. |
| 281 | `stddev_descending_staircase_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to descending staircase pattern over 60 days. |
| 282 | `stddev_downward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to downward gap continuation pattern over 60 days. |
| 283 | `stddev_inverse_cup_handle_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to inverse cup-and-handle pattern over 60 days. |
| 284 | `stddev_inverted_ascending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to inverted ascending scallop pattern over 60 days. |
| 285 | `stddev_inverted_descending_scallop_similarity` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to inverted descending scallop pattern over 60 days. |
| 286 | `stddev_similarity_descending_scallop_2` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the descending scallop pattern. |
| 287 | `stddev_similarity_inverse_dead_cat_recovery` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the inverse dead cat bounce pattern. |
| 288 | `stddev_upward_gap_continuation_score` | MATRIX | 0.998 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to upward gap continuation pattern over 60 days. |
| 289 | `ascending_channel_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for ascending channel pattern. |
| 290 | `ascending_channel_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for ascending channel pattern. |
| 291 | `ascending_scallop_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for ascending scallop pattern. |
| 292 | `ascending_scallop_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for ascending scallop pattern. |
| 293 | `ascending_scallop_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for ascending scallop pattern. |
| 294 | `ascending_scallop_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for ascending scallop pattern. |
| 295 | `ascending_scallop_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for ascending scallop pattern. |
| 296 | `ascending_staircase_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for ascending staircase pattern. |
| 297 | `ascending_staircase_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for ascending staircase pattern. |
| 298 | `ascending_staircase_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for ascending staircase pattern. |
| 299 | `ascending_staircase_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for ascending staircase pattern. |
| 300 | `bear_cup_handle_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent inverse cup and handle pattern. |
| 301 | `bear_flag_min_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the bearish flag pattern. |
| 302 | `bear_flag_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent bearish flag pattern. |
| 303 | `bear_pennant_avg_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the bearish pennant pattern. |
| 304 | `bear_rectangle_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the bearish rectangle pattern. |
| 305 | `bearish_flag_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bearish flag pattern. |
| 306 | `bearish_flag_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for bearish flag pattern. |
| 307 | `bearish_flag_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bearish flag pattern. |
| 308 | `bearish_flag_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bearish flag pattern. |
| 309 | `bearish_flag_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for bearish flag pattern. |
| 310 | `bearish_pennant_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for bearish pennant pattern. |
| 311 | `bearish_pennant_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bearish pennant pattern. |
| 312 | `bearish_pennant_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bearish pennant pattern. |
| 313 | `bearish_pennant_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for bearish pennant pattern. |
| 314 | `bearish_pennant_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for bearish pennant pattern. |
| 315 | `bearish_pennant_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for bearish pennant pattern emphasizing recent bars. |
| 316 | `bearish_rectangle_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bearish rectangle pattern. |
| 317 | `bearish_rectangle_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for bearish rectangle pattern. |
| 318 | `bearish_rectangle_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bearish rectangle pattern. |
| 319 | `bearish_rectangle_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for bearish rectangle pattern. |
| 320 | `bearish_rectangle_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for bearish rectangle pattern focusing on recent bars. |
| 321 | `bull_flag_mid_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the bullish flag pattern. |
| 322 | `bull_flag_min_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the bullish flag pattern. |
| 323 | `bull_flag_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the bullish flag pattern. |
| 324 | `bull_flag_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent bullish flag pattern. |
| 325 | `bull_pennant_95th_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the bullish pennant pattern. |
| 326 | `bull_rectangle_avg_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the bullish rectangle pattern. |
| 327 | `bullish_flag_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bullish flag pattern. |
| 328 | `bullish_flag_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for bullish flag pattern. |
| 329 | `bullish_flag_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for bullish flag pattern. |
| 330 | `bullish_pennant_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bullish pennant pattern. |
| 331 | `bullish_pennant_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for bullish pennant pattern. |
| 332 | `bullish_pennant_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bullish pennant pattern. |
| 333 | `bullish_pennant_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bullish pennant pattern. |
| 334 | `bullish_pennant_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for bullish pennant pattern. |
| 335 | `bullish_pennant_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for bullish pennant pattern emphasizing recent bars. |
| 336 | `bullish_rectangle_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for bullish rectangle pattern. |
| 337 | `bullish_rectangle_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bullish rectangle pattern. |
| 338 | `bullish_rectangle_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bullish rectangle pattern. |
| 339 | `bullish_rectangle_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for bullish rectangle pattern. |
| 340 | `bullish_rectangle_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for bullish rectangle pattern. |
| 341 | `bullish_rectangle_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for bullish rectangle pattern focusing on recent bars. |
| 342 | `cup_handle_95th_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the cup and handle pattern. |
| 343 | `cup_handle_mid_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the cup and handle pattern. |
| 344 | `cup_handle_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the cup and handle pattern. |
| 345 | `cup_handle_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for cup and handle pattern. |
| 346 | `cup_handle_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for cup and handle pattern. |
| 347 | `cup_handle_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for cup and handle pattern emphasizing recent bars. |
| 348 | `dead_cat_bounce_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for dead cat bounce pattern. |
| 349 | `dead_cat_bounce_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for dead cat bounce pattern. |
| 350 | `dead_cat_bounce_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for dead cat bounce pattern. |
| 351 | `dead_cat_bounce_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for dead cat bounce pattern. |
| 352 | `dead_cat_bounce_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for dead cat bounce pattern. |
| 353 | `dead_cat_bounce_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for dead cat bounce pattern emphasizing recent data. |
| 354 | `descending_channel_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for descending channel pattern. |
| 355 | `descending_channel_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for descending channel pattern. |
| 356 | `descending_channel_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for descending channel pattern. |
| 357 | `descending_channel_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for descending channel pattern focusing on recent bars. |
| 358 | `descending_scallop_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for descending scallop pattern. |
| 359 | `descending_scallop_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for descending scallop pattern. |
| 360 | `descending_staircase_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for descending staircase pattern. |
| 361 | `descending_staircase_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for descending staircase pattern. |
| 362 | `descending_staircase_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for descending staircase pattern. |
| 363 | `descending_staircase_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for descending staircase pattern. |
| 364 | `downward_channel_min_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the descending channel pattern. |
| 365 | `downward_channel_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the descending channel pattern. |
| 366 | `downward_gap_mid_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the downward gap pattern. |
| 367 | `downward_gap_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the downward gap pattern. |
| 368 | `downward_gap_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the downward gap pattern. |
| 369 | `downward_scallop_avg_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the downward scallop pattern. |
| 370 | `downward_scallop_min_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the downward scallop pattern. |
| 371 | `downward_scallop_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the downward scallop pattern. |
| 372 | `downward_scallop_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent downward scallop pattern. |
| 373 | `downward_scallop_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the downward scallop pattern. |
| 374 | `downward_staircase_95th_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for the downward staircase pattern. |
| 375 | `downward_staircase_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent downward staircase pattern. |
| 376 | `downward_staircase_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the downward staircase pattern. |
| 377 | `drop_after_rise_avg_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the inverse dead cat bounce pattern. |
| 378 | `flipped_downward_scallop_mid_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the inverted downward scallop pattern. |
| 379 | `flipped_upward_scallop_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the inverted upward scallop pattern. |
| 380 | `flipped_upward_scallop_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent inverted upward scallop pattern. |
| 381 | `gap_down_continuation_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for downward gap continuation pattern. |
| 382 | `gap_down_continuation_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for downward gap continuation pattern. |
| 383 | `gap_down_continuation_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for downward gap continuation pattern. |
| 384 | `gap_down_continuation_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for downward gap continuation pattern focusing on recent bars. |
| 385 | `gap_up_continuation_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for upward gap continuation pattern. |
| 386 | `gap_up_continuation_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for upward gap continuation pattern. |
| 387 | `gap_up_continuation_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for upward gap continuation pattern. |
| 388 | `gap_up_continuation_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for upward gap continuation pattern. |
| 389 | `gap_up_continuation_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for upward gap continuation pattern focusing on recent bars. |
| 390 | `inverse_cup_handle_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for inverse cup and handle pattern. |
| 391 | `inverse_cup_handle_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for inverse cup and handle pattern. |
| 392 | `inverse_cup_handle_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for inverse cup and handle pattern. |
| 393 | `inverse_cup_handle_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for inverse cup and handle pattern. |
| 394 | `inverse_cup_handle_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for inverse cup and handle pattern. |
| 395 | `inverse_cup_handle_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for inverse cup and handle pattern. |
| 396 | `inverse_dead_cat_bounce_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for inverse dead cat bounce pattern. |
| 397 | `inverse_dead_cat_bounce_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for inverse dead cat bounce pattern. |
| 398 | `inverse_dead_cat_bounce_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for inverse dead cat bounce pattern. |
| 399 | `inverse_dead_cat_bounce_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for inverse dead cat bounce pattern. |
| 400 | `inverse_dead_cat_bounce_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for inverse dead cat bounce pattern. |
| 401 | `inverse_dead_cat_bounce_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for inverse dead cat bounce pattern focusing on recent bars. |
| 402 | `inverted_ascending_scallop_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for inverted ascending scallop pattern. |
| 403 | `inverted_ascending_scallop_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for inverted ascending scallop pattern. |
| 404 | `inverted_ascending_scallop_similarity_middle` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for inverted ascending scallop pattern. |
| 405 | `inverted_ascending_scallop_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for inverted ascending scallop pattern. |
| 406 | `inverted_ascending_scallop_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for inverted ascending scallop pattern. |
| 407 | `inverted_descending_scallop_similarity_average` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for inverted descending scallop pattern. |
| 408 | `inverted_descending_scallop_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for inverted descending scallop pattern. |
| 409 | `inverted_descending_scallop_similarity_maximum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for inverted descending scallop pattern. |
| 410 | `inverted_descending_scallop_similarity_minimum` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for inverted descending scallop pattern. |
| 411 | `inverted_descending_scallop_similarity_percentile_95` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score for inverted descending scallop pattern. |
| 412 | `inverted_descending_scallop_similarity_recent` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for inverted descending scallop pattern focusing on recent bars. |
| 413 | `rebound_after_drop_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the dead cat bounce pattern. |
| 414 | `upward_channel_avg_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for the ascending channel pattern. |
| 415 | `upward_channel_min_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the ascending channel pattern. |
| 416 | `upward_channel_peak_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for the ascending channel pattern. |
| 417 | `upward_gap_mid_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for the upward gap pattern. |
| 418 | `upward_scallop_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent upward scallop pattern. |
| 419 | `upward_scallop_similarity_dispersion` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for the upward scallop pattern. |
| 420 | `upward_staircase_min_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for the ascending staircase pattern. |
| 421 | `upward_staircase_recent_similarity` | MATRIX | 0.994 | 风险与质量 | 0 | — | — | — | UNTESTED | Similarity score for the most recent ascending staircase pattern. |
| 422 | `ascending_channel_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the ascending channel pattern over a 40-week horizon. |
| 423 | `ascending_scallop_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the ascending scallop pattern over a 40-week horizon. |
| 424 | `ascending_scallop_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the ascending scallop pattern over a 40-week horizon. |
| 425 | `ascending_scallop_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the ascending scallop pattern over a 40-week horizon. |
| 426 | `ascending_staircase_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the ascending staircase pattern over a 40-week horizon. |
| 427 | `ascending_staircase_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the ascending staircase pattern over a 40-week horizon. |
| 428 | `ascending_staircase_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the ascending staircase pattern over a 40-week horizon. |
| 429 | `bearish_flag_pattern_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for bearish flag pattern. |
| 430 | `bearish_flag_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bearish flag pattern over a 40-week horizon. |
| 431 | `bearish_flag_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish flag pattern over a 40-week horizon. |
| 432 | `bearish_flag_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the bearish flag pattern over a 40-week horizon. |
| 433 | `bearish_flag_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bearish flag pattern over a 40-week horizon. |
| 434 | `bearish_flag_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the bearish flag pattern over a 40-week horizon. |
| 435 | `bearish_flag_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bearish flag pattern over a 40-week horizon. |
| 436 | `bearish_pennant_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for bearish pennant pattern. |
| 437 | `bearish_pennant_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish pennant pattern over a 40-week horizon. |
| 438 | `bearish_pennant_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the bearish pennant pattern over a 40-week horizon. |
| 439 | `bearish_pennant_similarity_maximum_2` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bearish pennant pattern. |
| 440 | `bearish_pennant_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bearish pennant pattern. |
| 441 | `bearish_pennant_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the bearish pennant pattern over a 40-week horizon. |
| 442 | `bearish_pennant_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bearish pennant pattern over a 40-week horizon. |
| 443 | `bearish_rectangle_pattern_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for bearish rectangle pattern. |
| 444 | `bearish_rectangle_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for bearish rectangle pattern. |
| 445 | `bearish_rectangle_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the bearish rectangle pattern over a 40-week horizon. |
| 446 | `bearish_rectangle_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bearish rectangle pattern. |
| 447 | `bearish_rectangle_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bearish rectangle pattern over a 40-week horizon. |
| 448 | `bearish_rectangle_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the bearish rectangle pattern over a 40-week horizon. |
| 449 | `bearish_rectangle_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bearish rectangle pattern over a 40-week horizon. |
| 450 | `bullish_flag_pattern_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bullish flag pattern. |
| 451 | `bullish_flag_pattern_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for bullish flag pattern. |
| 452 | `bullish_flag_pattern_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bullish flag pattern. |
| 453 | `bullish_flag_pattern_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for bullish flag pattern. |
| 454 | `bullish_flag_pattern_similarity_minimum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for bullish flag pattern. |
| 455 | `bullish_flag_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bullish flag pattern over a 40-week horizon. |
| 456 | `bullish_flag_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bullish flag pattern over a 40-week horizon. |
| 457 | `bullish_pennant_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the bullish pennant pattern over a 40-week horizon. |
| 458 | `bullish_pennant_similarity_average_2` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bullish pennant pattern. |
| 459 | `bullish_pennant_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the bullish pennant pattern over a 40-week horizon. |
| 460 | `bullish_pennant_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the bullish pennant pattern over a 40-week horizon. |
| 461 | `bullish_pennant_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bullish pennant pattern over a 40-week horizon. |
| 462 | `bullish_pennant_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the bullish pennant pattern over a 40-week horizon. |
| 463 | `bullish_pennant_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bullish pennant pattern over a 40-week horizon. |
| 464 | `bullish_rectangle_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for bullish rectangle pattern. |
| 465 | `bullish_rectangle_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for bullish rectangle pattern. |
| 466 | `bullish_rectangle_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for bullish rectangle pattern. |
| 467 | `bullish_rectangle_similarity_maximum_2` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for bullish rectangle pattern. |
| 468 | `bullish_rectangle_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the bullish rectangle pattern over a 40-week horizon. |
| 469 | `bullish_rectangle_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the bullish rectangle pattern over a 40-week horizon. |
| 470 | `bullish_rectangle_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the bullish rectangle pattern over a 40-week horizon. |
| 471 | `cup_and_handle_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the cup and handle pattern over a 40-week horizon. |
| 472 | `cup_and_handle_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the cup and handle pattern over a 40-week horizon. |
| 473 | `cup_and_handle_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the cup and handle pattern over a 40-week horizon. |
| 474 | `cup_and_handle_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the cup and handle pattern over a 40-week horizon. |
| 475 | `cup_handle_pattern_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for cup-and-handle pattern. |
| 476 | `cup_handle_pattern_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for cup-and-handle pattern. |
| 477 | `cup_handle_pattern_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for cup-and-handle pattern. |
| 478 | `dead_cat_bounce_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the dead cat bounce pattern over a 40-week horizon. |
| 479 | `dead_cat_bounce_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the dead cat bounce pattern over a 40-week horizon. |
| 480 | `dead_cat_bounce_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the dead cat bounce pattern over a 40-week horizon. |
| 481 | `dead_cat_bounce_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the dead cat bounce pattern over a 40-week horizon. |
| 482 | `dead_cat_bounce_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for dead cat bounce pattern. |
| 483 | `dead_cat_bounce_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the dead cat bounce pattern over a 40-week horizon. |
| 484 | `dead_cat_bounce_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the dead cat bounce pattern over a 40-week horizon. |
| 485 | `descending_channel_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the descending channel pattern over a 40-week horizon. |
| 486 | `descending_channel_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the descending channel pattern over a 40-week horizon. |
| 487 | `descending_channel_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the descending channel pattern over a 40-week horizon. |
| 488 | `descending_channel_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the descending channel pattern over a 40-week horizon. |
| 489 | `descending_channel_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the descending channel pattern over a 40-week horizon. |
| 490 | `descending_scallop_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the descending scallop pattern over a 40-week horizon. |
| 491 | `descending_scallop_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the descending scallop pattern over a 40-week horizon. |
| 492 | `descending_scallop_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the descending scallop pattern over a 40-week horizon. |
| 493 | `descending_scallop_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the descending scallop pattern over a 40-week horizon. |
| 494 | `descending_staircase_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the descending staircase pattern over a 40-week horizon. |
| 495 | `descending_staircase_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the descending staircase pattern over a 40-week horizon. |
| 496 | `descending_staircase_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the descending staircase pattern over a 40-week horizon. |
| 497 | `descending_staircase_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the descending staircase pattern over a 40-week horizon. |
| 498 | `descending_staircase_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the descending staircase pattern over a 40-week horizon. |
| 499 | `downward_channel_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for downward channel patterns. |
| 500 | `downward_channel_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for downward channel pattern. |
| 501 | `downward_scallop_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for descending scallop pattern. |
| 502 | `downward_scallop_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for descending scallop pattern. |
| 503 | `downward_scallop_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for descending scallop pattern. |
| 504 | `downward_staircase_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for descending staircase pattern. |
| 505 | `downward_staircase_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for descending staircase pattern. |
| 506 | `gap_down_continuation_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the downward gap continuation pattern over a 40-week horizon. |
| 507 | `gap_down_continuation_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the downward gap continuation pattern over a 40-week horizon. |
| 508 | `gap_down_continuation_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the downward gap continuation pattern over a 40-week horizon. |
| 509 | `gap_down_continuation_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the downward gap continuation pattern over a 40-week horizon. |
| 510 | `gap_up_continuation_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the upward gap continuation pattern over a 40-week horizon. |
| 511 | `gap_up_continuation_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the upward gap continuation pattern over a 40-week horizon. |
| 512 | `gap_up_continuation_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the upward gap continuation pattern over a 40-week horizon. |
| 513 | `gap_up_continuation_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the upward gap continuation pattern over a 40-week horizon. |
| 514 | `gap_up_continuation_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the upward gap continuation pattern over a 40-week horizon. |
| 515 | `gap_up_continuation_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the upward gap continuation pattern over a 40-week horizon. |
| 516 | `inverse_cup_and_handle_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the inverse cup and handle pattern over a 40-week horizon. |
| 517 | `inverse_cup_and_handle_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the inverse cup and handle pattern over a 40-week horizon. |
| 518 | `inverse_dead_cat_bounce_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the inverse dead cat bounce pattern over a 40-week horizon. |
| 519 | `inverse_dead_cat_bounce_similarity_minimum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Lowest similarity score to the inverse dead cat bounce pattern over a 40-week horizon. |
| 520 | `inverted_ascending_scallop_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the inverted ascending scallop pattern over a 40-week horizon. |
| 521 | `inverted_ascending_scallop_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the inverted ascending scallop pattern over a 40-week horizon. |
| 522 | `inverted_ascending_scallop_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the inverted ascending scallop pattern over a 40-week horizon. |
| 523 | `inverted_descending_scallop_similarity_95th_percentile_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile similarity score to the inverted descending scallop pattern over a 40-week horizon. |
| 524 | `inverted_descending_scallop_similarity_average_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score to the inverted descending scallop pattern over a 40-week horizon. |
| 525 | `inverted_descending_scallop_similarity_dynamic_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Recent similarity score to the inverted descending scallop pattern over a 40-week horizon. |
| 526 | `inverted_descending_scallop_similarity_maximum_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Highest similarity score to the inverted descending scallop pattern over a 40-week horizon. |
| 527 | `inverted_descending_scallop_similarity_median_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score to the inverted descending scallop pattern over a 40-week horizon. |
| 528 | `inverted_descending_scallop_similarity_stdev_h40w` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores to the inverted descending scallop pattern over a 40-week horizon. |
| 529 | `inverted_downward_scallop_similarity_minimum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for inverted descending scallop pattern. |
| 530 | `inverted_upward_scallop_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for inverted ascending scallop pattern. |
| 531 | `inverted_upward_scallop_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for inverted ascending scallop pattern. |
| 532 | `inverted_upward_scallop_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for inverted ascending scallop pattern. |
| 533 | `inverted_upward_scallop_similarity_minimum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for inverted ascending scallop pattern. |
| 534 | `reverse_cup_handle_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for inverse cup-and-handle pattern. |
| 535 | `reverse_cup_handle_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for inverse cup-and-handle pattern. |
| 536 | `reverse_cup_handle_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for inverse cup-and-handle pattern. |
| 537 | `reverse_cup_handle_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for inverse cup-and-handle pattern. |
| 538 | `reverse_cup_handle_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for inverse cup-and-handle pattern. |
| 539 | `reverse_dead_cat_bounce_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for inverse dead cat bounce pattern. |
| 540 | `reverse_dead_cat_bounce_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for inverse dead cat bounce pattern. |
| 541 | `reverse_dead_cat_bounce_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for inverse dead cat bounce pattern. |
| 542 | `reverse_dead_cat_bounce_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for inverse dead cat bounce pattern. |
| 543 | `reverse_dead_cat_bounce_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for inverse dead cat bounce pattern. |
| 544 | `trend_gap_down_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for downward gap continuation pattern. |
| 545 | `trend_gap_down_similarity_minimum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for downward gap continuation pattern. |
| 546 | `trend_gap_down_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for downward gap continuation pattern. |
| 547 | `trend_gap_up_similarity_minimum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for upward gap continuation pattern. |
| 548 | `upward_channel_similarity_95th_percentile` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | 95th percentile of similarity scores for upward channel pattern. |
| 549 | `upward_channel_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for upward channel pattern. |
| 550 | `upward_channel_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for upward channel pattern. |
| 551 | `upward_channel_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for upward channel pattern. |
| 552 | `upward_channel_similarity_minimum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Minimum similarity score for upward channel pattern. |
| 553 | `upward_scallop_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for ascending scallop pattern. |
| 554 | `upward_scallop_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for ascending scallop pattern. |
| 555 | `upward_scallop_similarity_median` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Median similarity score for ascending scallop pattern. |
| 556 | `upward_scallop_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for ascending scallop pattern. |
| 557 | `upward_staircase_pattern_similarity_average` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Average similarity score for upward staircase pattern. |
| 558 | `upward_staircase_pattern_similarity_dynamic` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Dynamic similarity score for upward staircase pattern. |
| 559 | `upward_staircase_pattern_similarity_maximum` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Maximum similarity score for upward staircase pattern. |
| 560 | `upward_staircase_pattern_similarity_standard_deviation` | MATRIX | 0.979 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of similarity scores for upward staircase pattern. |

## 六、本地回测证据

- 本地累计回测 **81** 条；其中 `ra_failed_checks` 为空的 **10** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `XgWxwWRl` | 2.09 | 1.49 | — | — | 0.07 | 0 | 180 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `le8Y68K2` | 2.07 | 1.46 | — | — | 0.07 | 0 | 180 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `YP5OG79M` | 2.06 | 1.45 | — | — | 0.07 | 0 | 174 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_earni` |
| `E5vMJG5P` | 2.02 | 1.41 | — | — | 0.07 | 0 | 175 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `om6X2QnJ` | 2.02 | 1.40 | — | — | 0.07 | 0 | 176 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `QP3Aemnw` | 1.99 | 1.37 | — | — | 0.07 | 0 | 176 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `LL9weOn2` | 1.97 | 1.35 | — | — | 0.07 | ["IS_LADDER_ | 176 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `j23Jl38Z` | 1.97 | 1.36 | — | — | 0.07 | ["IS_LADDER_ | 180 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `P0ZbrZMW` | 1.93 | 1.32 | — | — | 0.07 | ["IS_LADDER_ | 180 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |
| `1YxRVxZR` | 1.91 | 1.31 | — | — | 0.07 | 0 | 180 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_ebitd` |
| `1YxRmbpR` | 1.91 | 1.31 | — | — | 0.06 | 0 | 184 | `rank(ts_decay_linear(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surpris` |
| `E5vMr2bL` | 1.91 | 1.32 | — | — | 0.06 | ["LOW_SUB_UN | 186A | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_ebitd` |
| `YP5OZXQW` | 1.87 | 1.22 | — | — | 0.07 | 0 | 176 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_fy1_earnings_4` |
| `pwPkONwo` | 1.84 | 1.23 | — | — | 0.07 | 0 | 175 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_ebitd` |
| `QP3AemEw` | 1.72 | 1.11 | — | — | 0.06 | ["IS_LADDER_ | 176 | `rank(group_neutralize(subtract(subtract(rank(ts_backfill(predicted_surprise_pct_f12m_reven` |

## 七、判死记录（sealed dead_end）

- `EUR-W169-FASTPV-SPREAD-REVERSED-DEAD`（None）family=None：{"evidence": "wave169 8/8 全负 Sharpe(-0.27~-1.11)：le89bMrx(median_upward_gap-ebitda4)S-1.11、le89bM0x(group_zscore纯快腿)S-0.91、zqY01rWR(vwap_twap)S-0.71、0mR60j8q(corr_high_low)S-0.67+turnover1.88撞HIGH_TURNOVER、npKQMAWz(ascending_channel)S-0.44、LL9rA5RM(形态价差)S-0.51、883YdvnW(corr_bid_ask)S-0.27+CW、9qVmLEJd(cup_handle)S-0.37", "family": "continuation_score/intraday_pv_feats 快腿 - predicted_surprise 慢腿 价差骨
- `EUR-W170-FASTPV-NEGATED-WEAK-DEAD`（None）family=None：{"evidence": "wave170 8/8 全 failed_ra：ZY0MGkpx(median_upward_gap取负)S1.11/fit0.42/SUB0.58/LADDER0.67、YP5JqXpM(cup_handle)S0.37、kqVOle38(ascending)S0.44、akLwvXd9(形态价差)S0.51、d5OoLe0X(dead_cat_recovery)S0.58、A10mKqPY(dynamic_cup)S0.0、1YxPE6dz(bearish_flag)S0.17、58QeWNO5(dead_cat_bounce)S0.1", "family": "predicted_surprise 慢 - continuation_score 快(取负同向) 价差", "finding": "方向修正生效(wave169 -1.11→wave170 +1.
- `EUR-CONTINUATION-COMPOSITE-WEAK`（2026-08-23）family=continuation_score chart-similarity composites：{"region": "EUR", "dataset": "continuation_score", "rule": "After composite round (bull-bear subtract, group_rank, ts_av_diff, ts_corr) max /sharpe/ 0.44. Not worth another probe round.", "evidence": {"wave": 31, "n": 8, "max_abs_sharpe": 0.44, "best": "Xg7k2Jr1 ts_av_diff inverse_cup"}, "wave": 31}

