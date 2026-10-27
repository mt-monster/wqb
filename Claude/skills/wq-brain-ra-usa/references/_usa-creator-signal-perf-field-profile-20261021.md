# creator_signal_perf 字段画像（2026-10-21）

> 数据集：`creator_signal_perf`（USA / TOP3000 / D1）｜平台类别 **socialmedia**（组合分组 News-Sentiment）｜**未点亮塔**（`get_pyramid_alphas` 实测 socialmedia=0）。
> 字段目录：`tracking/USA/reference/usa_creator_signal_perf_fields.json`（`tools/scan_fields.py` 实测 `platform_count=102 / complete=True`）。
> 正文按「字段八问」组织（`MEMORY.md` §7）。

## 1. 八问 ①–④：类型 / 覆盖 / 频率 / 分布

| 问 | 实测 |
|---|---|
| ① 类型 | **102/102 全 VECTOR**（无 MATRIX 标量）⇒ 任何表达式必须先 `vec_*(x)` 聚合，再进标量算子；未聚合直接 `rank(field)` 会报类型错 |
| ② 覆盖 | min **0.6014** ／ 中位 **0.6525** ／ max **0.8145**；≥0.76 共 13 个，其余集中在 0.60–0.65 |
| ③ 频率 | 待批 1 实测反推：字段为「预测/组合表现的聚合快照」，若 TO 落 <1% 说明是周/月频，需改短窗 Δ 或降 decay；若 TO 健康则按日频处理 |
| ④ 分布 | 无平台 min/max 元数据；字段多为**收益率（%）、比率（0–1）、计数**三类。收益率类须 `winsorize(std=4)` 防极值；比率类可 `group_rank` 直接截面化 |

## 2. 八问 ⑤：拥挤度与字段族地图

- **数据集级拥挤度**：alphaCount **155** ／ userCount **87**（USA 属低拥挤档，对照 analyst_consensus 3/4 位数千级）。
- **字段级拥挤度**：alphaCount 中位 **1**、max **12**（`recent_prediction_success_trend_asset`）；userCount min **0** max **10**，**31 个字段 userCount=0**（真空白）。

| 族 | 字段数 | 代表字段（cov / aC / uC） | 经济含义 |
|---|---:|---|---|
| A 聚合组合收益（crowd 组合自身 PnL） | 8 | `aggregate_large_target_long_horizon_return`(0.767/11/10)；`aggregate_small_target_quick_horizon_gain`(0.652/6/6)；`aggregate_large_target_long_horizon_return_2`(0.652/5/5) | — |
| B 资产级预测统计 | 35 | `asset_short_predictions_count`(0.602/5/5)；`asset_current_market_price`(0.646/4/4)；`asset_long_predictions_count_2`(0.652/4/4) | — |
| C 账户级跨资产统计 | 17 | `overall_correct_long_predictions_count`(0.602/3/3)；`overall_aggregate_portfolio_return`(0.602/2/2)；`overall_prediction_success_rate`(0.767/2/2) | — |
| D 牛市条件收益 | 8 | `bull_market_small_target_quick_horizon_return_2`(0.815/3/3)；`bull_market_large_target_long_horizon_return_2`(0.652/2/1)；`bull_market_medium_target_mid_horizon_return`(0.767/2/1) | — |
| E 熊市条件收益 | 8 | `bear_market_large_target_long_horizon_return_2`(0.652/2/2)；`bear_market_small_target_quick_horizon_gain`(0.652/2/2)；`bear_market_aggregate_portfolio_gain`(0.652/1/1) | — |
| F 多头信号组合收益 | 8 | `long_signals_small_target_quick_horizon_return`(0.602/3/2)；`long_signals_large_target_extended_horizon_return`(0.602/2/1)；`long_signals_large_target_extended_horizon_return_2`(0.652/2/2) | — |
| G 空头信号组合收益 | 8 | `short_signals_large_target_long_horizon_return_2`(0.652/5/4)；`short_signals_medium_target_mid_horizon_return_2`(0.652/4/3)；`short_signals_aggregate_portfolio_return_2`(0.815/1/1) | — |
| H 方向偏置 | 7 | `short_bias_prediction_ratio_overall_2`(0.815/4/3)；`long_bias_prediction_ratio_overall`(0.646/1/1)；`long_prediction_success_rate_overall_2`(0.652/1/1) | — |
| I 近期成功率趋势 | 3 | `recent_prediction_success_trend_asset`(0.652/12/3)；`recent_prediction_success_trend_overall`(0.602/1/1)；`recent_prediction_success_trend_overall_2`(0.652/0/0) | — |

## 3. 八问 ⑥：机制假设（批 1 的设计依据）

**数据集语义**：第三方「创作者/账户」平台的预测与组合表现，按资产聚合。VECTOR 维 = 覆盖该资产的创作者集合。

| 机制 | 假设（可证伪） | 文献 | 首选字段 | 方向 |
|---|---|---|---|---|
| **M1 crowd 技能动量（hot-hand）** | 近期在该资产上赚钱的 crowd 组合，短期继续跑赢 —— 创作者技能在短窗有持续性 | Hendricks/Patel/Zeckhauser 1993（hot hands）；Hong & Stein 1999（渐进扩散） | `aggregate_small_target_quick_horizon_return` Δ22 / `asset_recent_prediction_success_trend` | 正 |
| **M2 创作者分歧（Miller 高估）** | 创作者预测准确度的**截面离散度**高 = 分歧大 ⇒ 该资产被高估、后续收益低 | Miller 1977；Diether/Malloy/Scherbina 2002 | `vec_stddev(asset_prediction_accuracy_score)` 归一后 | 负 |
| **M3 方向偏置反转** | 创作者多头占比越高 ⇒ 群体过度看多 ⇒ 后续跑输（散户情绪反向） | Barber/Odean/Zhu 2009；Da/Engelberg/Gao 2011 | `asset_long_prediction_ratio` 水平与 Δ22 | 负 |
| **M4 技能不对称（熊市技能）** | 熊市仍赚钱的 crowd 才是真技能；牛市收益是 beta。熊−牛 差值高的资产后续更强 | Treynor 1965（beta vs alpha）；Kosowski 2006（bootstrap 技能） | `bear_market_aggregate_portfolio_return − bull_market_*` | 正 |
| **M5 覆盖创作者质量** | 覆盖该资产的创作者**整体历史成功率**越高 ⇒ 该资产被「聪明 crowd」选中 ⇒ 后续更强 | Chen/De/Hu/Hwang 2014（社交平台内容预测力） | `overall_prediction_success_rate`（vec_avg） | 正 |

**不采用的族**：`asset_current_market_price`（价格本身，prod 必撞已有价量池）；`*_2` 重复字段族（与基名同描述、仅覆盖微差，视为同一信息的第二口径，批 2 才做口径对照）。

## 4. 八问 ⑦：用法规则（两阶段 / 覆盖 / 窗口）

1. **两阶段强制**：`vec_avg / vec_stddev / vec_max / vec_min / vec_range` 先落地为标量，再进 `ts_backfill` 与横截面算子。
2. **覆盖 < 0.7 ⇒ `ts_backfill(x, 252)`**；不要用 756（本集是快变量，长回填会把 TO 压到地板）。
3. **窗口只取 `config.STANDARD_WINDOWS`**（1/5/22/66/252/504/1008/1260）；Δ 首选 22，慢腿 66。
4. **收益率类先 `winsorize(std=4)`**，比率类先 `group_rank`。
5. **截面中性化**：区域缺省 SUBINDUSTRY；批 2 再测 INDUSTRY / MARKET 档（设置是强度闸，跨档不可比）。

## 5. 八问 ⑧：判死口径（先注册后回测）

- **批 1（8 探针）**：任一机制条数 ≥2 且最高 |S| < **1.0** ⇒ 该机制封存；
- 全批 8/8 且 `max|S| < 1.0` ⇒ 数据集判弱（`USA-CREATOR-SIGNAL-PERF-WEAK`），不发第 2 批；
- 出现 1–2 闸不过 ⇒ **先 `tools/gate_attribution.py` 归因，禁止盲扫**；
- 全 IS 闸通过 ⇒ `check_correlation(refresh=True)` 实测 prod/self，按 D0-P 处置（prod ≥0.75 判死）。

## 6. 全字段底表（102，按族排序）

| # | id | cov | aC | uC | 族 | 描述 |
|---:|---|---:|---:|---:|---|---|
| 1 | `aggregate_large_target_long_horizon_return` | 0.7668 | 11 | 10 | A | Aggregate portfolio return using large price targets and extended timeframes. |
| 2 | `aggregate_large_target_long_horizon_return_2` | 0.6525 | 5 | 5 | A | Aggregate portfolio return using large price targets and extended timeframes. |
| 3 | `aggregate_medium_target_mid_horizon_return` | 0.6463 | 2 | 2 | A | Aggregate portfolio return using medium price targets and mid-range timeframes. |
| 4 | `aggregate_medium_target_mid_horizon_return_2` | 0.6525 | 0 | 0 | A | Aggregate portfolio return using medium price targets and mid-range timeframes. |
| 5 | `aggregate_prediction_accuracy_score` | 0.6463 | 4 | 4 | A | Weighted score reflecting overall prediction accuracy and volume. |
| 6 | `aggregate_prediction_accuracy_score_2` | 0.6525 | 3 | 2 | A | Weighted score reflecting overall prediction accuracy and volume. |
| 7 | `aggregate_small_target_quick_horizon_gain` | 0.6525 | 6 | 6 | A | Portfolio return using small price targets and short time horizons across all assets. |
| 8 | `aggregate_small_target_quick_horizon_return` | 0.6463 | 1 | 1 | A | Aggregate portfolio return using small price targets and short timeframes. |
| 9 | `asset_aggregate_portfolio_return` | 0.6015 | 1 | 1 | B | Total percentage return for an asset using all price and time targets. |
| 10 | `asset_aggregate_portfolio_return_2` | 0.6525 | 1 | 1 | B | Total percentage return for an asset using all price and time targets. |
| 11 | `asset_correct_long_predictions_count` | 0.6463 | 3 | 3 | B | Number of correct long-biased predictions for a specific asset. |
| 12 | `asset_correct_long_predictions_count_2` | 0.6525 | 2 | 2 | B | Number of correct long-biased predictions for a specific asset. |
| 13 | `asset_correct_short_predictions_count` | 0.6015 | 2 | 2 | B | Number of correct short-biased predictions for a specific asset. |
| 14 | `asset_correct_short_predictions_count_2` | 0.6525 | 0 | 0 | B | Number of correct short-biased predictions for a specific asset. |
| 15 | `asset_current_market_price` | 0.6463 | 4 | 4 | B | Current market price of the asset at the time of prediction. |
| 16 | `asset_current_market_price_2` | 0.6525 | 2 | 1 | B | Current market price of the asset at the time of prediction. |
| 17 | `asset_large_target_long_horizon_return` | 0.6463 | 1 | 1 | B | Percentage return for an asset using large price targets and extended timeframes. |
| 18 | `asset_large_target_long_horizon_return_2` | 0.6525 | 1 | 1 | B | Percentage return for an asset using large price targets and extended timeframes. |
| 19 | `asset_long_prediction_ratio` | 0.6015 | 3 | 3 | B | Proportion of long-biased predictions out of total predictions for an asset. |
| 20 | `asset_long_prediction_ratio_2` | 0.6525 | 2 | 2 | B | Proportion of long-biased predictions out of total predictions for an asset. |
| 21 | `asset_long_prediction_success_rate` | 0.6463 | 2 | 2 | B | Ratio of correct long-biased predictions to total long predictions for an asset. |
| 22 | `asset_long_prediction_success_rate_2` | 0.6525 | 2 | 2 | B | Ratio of correct long-biased predictions to total long predictions for an asset. |
| 23 | `asset_long_predictions_count` | 0.6015 | 1 | 1 | B | Total number of long-biased predictions made for a specific asset. |
| 24 | `asset_long_predictions_count_2` | 0.6525 | 4 | 4 | B | Total number of long-biased predictions made for a specific asset. |
| 25 | `asset_medium_target_mid_horizon_return` | 0.6015 | 1 | 1 | B | Percentage return for an asset using medium price targets and mid-range timeframes. |
| 26 | `asset_medium_target_mid_horizon_return_2` | 0.6525 | 0 | 0 | B | Percentage return for an asset using medium price targets and mid-range timeframes. |
| 27 | `asset_prediction_accuracy_score` | 0.6015 | 0 | 0 | B | Weighted score reflecting prediction accuracy and volume for an asset. |
| 28 | `asset_prediction_accuracy_score_2` | 0.6525 | 2 | 2 | B | Weighted score reflecting prediction accuracy and volume for an asset. |
| 29 | `asset_prediction_confidence_ratio` | 0.6463 | 1 | 1 | B | Ratio of current confidence score to the maximum confidence score for an asset. |
| 30 | `asset_prediction_confidence_ratio_2` | 0.6525 | 0 | 0 | B | Ratio of current confidence score to the maximum confidence score for an asset. |
| 31 | `asset_prediction_success_rate` | 0.6463 | 0 | 0 | B | Ratio of correct predictions to total predictions for an asset. |
| 32 | `asset_prediction_success_rate_2` | 0.6525 | 1 | 1 | B | Ratio of correct predictions to total predictions for an asset. |
| 33 | `asset_recent_prediction_success_trend` | 0.6015 | 1 | 1 | B | Recent success rate of predictions for a specific asset. |
| 34 | `asset_short_prediction_ratio` | 0.6463 | 0 | 0 | B | Proportion of short-biased predictions out of total predictions for an asset. |
| 35 | `asset_short_prediction_ratio_2` | 0.8145 | 2 | 2 | B | Proportion of short-biased predictions out of total predictions for an asset. |
| 36 | `asset_short_prediction_success_rate` | 0.6015 | 0 | 0 | B | Ratio of correct short-biased predictions to total short predictions for an asset. |
| 37 | `asset_short_predictions_count` | 0.6015 | 5 | 5 | B | Total number of short-biased predictions made for a specific asset. |
| 38 | `asset_short_predictions_count_2` | 0.6525 | 3 | 3 | B | Total number of short-biased predictions made for a specific asset. |
| 39 | `asset_short_signals_success_ratio` | 0.6525 | 2 | 2 | B | Ratio of correct short position predictions to total short predictions for a specific asset. |
| 40 | `asset_small_target_quick_horizon_return` | 0.6015 | 2 | 2 | B | Percentage return for an asset using small price targets and short timeframes. |
| 41 | `asset_small_target_quick_horizon_return_2` | 0.6525 | 1 | 1 | B | Percentage return for an asset using small price targets and short timeframes. |
| 42 | `asset_total_predictions_count` | 0.6463 | 1 | 1 | B | Total number of predictions made for a specific asset. |
| 43 | `asset_total_predictions_count_2` | 0.6525 | 3 | 3 | B | Total number of predictions made for a specific asset. |
| 44 | `overall_aggregate_portfolio_return` | 0.6015 | 2 | 2 | C | Aggregate percentage return using all price and time targets across all assets. |
| 45 | `overall_aggregate_portfolio_return_2` | 0.6525 | 0 | 0 | C | Aggregate percentage return using all price and time targets across all assets. |
| 46 | `overall_correct_long_predictions_count` | 0.6015 | 3 | 3 | C | Number of correct long-biased predictions across all assets. |
| 47 | `overall_correct_long_predictions_count_2` | 0.6525 | 0 | 0 | C | Number of correct long-biased predictions across all assets. |
| 48 | `overall_correct_short_predictions_count` | 0.7668 | 1 | 1 | C | Number of correct short-biased predictions across all assets. |
| 49 | `overall_correct_short_predictions_count_2` | 0.6525 | 0 | 0 | C | Number of correct short-biased predictions across all assets. |
| 50 | `overall_long_predictions_count` | 0.6463 | 1 | 1 | C | Total number of long-biased predictions made by an account across all assets. |
| 51 | `overall_long_predictions_count_2` | 0.6525 | 0 | 0 | C | Total number of long-biased predictions made by an account across all assets. |
| 52 | `overall_long_signals_ratio` | 0.6525 | 1 | 1 | C | Ratio of long position predictions to total predictions made across all assets. |
| 53 | `overall_prediction_confidence_ratio` | 0.7668 | 0 | 0 | C | Ratio of current overall confidence score to the maximum possible score. |
| 54 | `overall_prediction_confidence_ratio_2` | 0.6525 | 1 | 1 | C | Ratio of current overall confidence score to the maximum possible score. |
| 55 | `overall_prediction_success_rate` | 0.7668 | 2 | 2 | C | Ratio of correct predictions to total predictions across all assets. |
| 56 | `overall_prediction_success_rate_2` | 0.6525 | 0 | 0 | C | Ratio of correct predictions to total predictions across all assets. |
| 57 | `overall_short_predictions_count` | 0.6463 | 0 | 0 | C | Total number of short-biased predictions made by an account across all assets. |
| 58 | `overall_short_signals_count` | 0.6525 | 0 | 0 | C | Total number of short position predictions made across all assets by an account. |
| 59 | `overall_signals_count` | 0.6525 | 0 | 0 | C | Total number of predictions made by an account across all assets. |
| 60 | `overall_total_predictions_count` | 0.6014 | 2 | 2 | C | Total number of predictions made by an account across all assets. |
| 61 | `bull_market_aggregate_portfolio_return` | 0.6463 | 1 | 1 | D | Total portfolio return during periods of rising asset prices. |
| 62 | `bull_market_aggregate_portfolio_return_2` | 0.8145 | 1 | 1 | D | Total portfolio return during periods of rising asset prices. |
| 63 | `bull_market_large_target_long_horizon_return` | 0.6015 | 0 | 0 | D | Portfolio return during bull markets using large price targets and extended timeframes. |
| 64 | `bull_market_large_target_long_horizon_return_2` | 0.6525 | 2 | 1 | D | Portfolio return during bull markets using large price targets and extended timeframes. |
| 65 | `bull_market_medium_target_mid_horizon_return` | 0.7668 | 2 | 1 | D | Portfolio return during bull markets using medium price targets and mid-range timeframes. |
| 66 | `bull_market_medium_target_mid_horizon_return_2` | 0.6525 | 2 | 2 | D | Portfolio return during bull markets using medium price targets and mid-range timeframes. |
| 67 | `bull_market_small_target_quick_horizon_return` | 0.6015 | 0 | 0 | D | Portfolio return during bull markets using small price targets and short timeframes. |
| 68 | `bull_market_small_target_quick_horizon_return_2` | 0.8145 | 3 | 3 | D | Portfolio return during bull markets using small price targets and short timeframes. |
| 69 | `bear_market_aggregate_portfolio_gain` | 0.6525 | 1 | 1 | E | Aggregate percentage return for all positions during bear market periods. |
| 70 | `bear_market_aggregate_portfolio_return` | 0.6015 | 0 | 0 | E | Total portfolio return during periods of declining asset prices. |
| 71 | `bear_market_large_target_long_horizon_return` | 0.6015 | 0 | 0 | E | Portfolio return during bear markets using large price targets and extended timeframes. |
| 72 | `bear_market_large_target_long_horizon_return_2` | 0.6525 | 2 | 2 | E | Portfolio return during bear markets using large price targets and extended timeframes. |
| 73 | `bear_market_medium_target_mid_horizon_return` | 0.6015 | 0 | 0 | E | Portfolio return during bear markets using medium price targets and mid-range timeframes. |
| 74 | `bear_market_medium_target_mid_horizon_return_2` | 0.6525 | 0 | 0 | E | Portfolio return during bear markets using medium price targets and mid-range timeframes. |
| 75 | `bear_market_small_target_quick_horizon_gain` | 0.6525 | 2 | 2 | E | Portfolio return for small price targets and quick timeframes during bear market periods. |
| 76 | `bear_market_small_target_quick_horizon_return` | 0.6015 | 0 | 0 | E | Portfolio return during bear markets using small price targets and short timeframes. |
| 77 | `long_signals_aggregate_portfolio_return` | 0.6015 | 1 | 1 | F | Total portfolio return using only long-biased signals. |
| 78 | `long_signals_aggregate_portfolio_return_2` | 0.6525 | 1 | 1 | F | Total portfolio return using only long-biased signals. |
| 79 | `long_signals_large_target_extended_horizon_return` | 0.6015 | 2 | 1 | F | Total return from long-biased signals with large price targets and long time horizons. |
| 80 | `long_signals_large_target_extended_horizon_return_2` | 0.6525 | 2 | 2 | F | Total return from long-biased signals with large price targets and long time horizons. |
| 81 | `long_signals_medium_target_mid_horizon_return` | 0.6463 | 0 | 0 | F | Portfolio return from long-biased signals with medium price targets and mid-range timeframes. |
| 82 | `long_signals_medium_target_mid_horizon_return_2` | 0.8145 | 2 | 2 | F | Portfolio return from long-biased signals with medium price targets and mid-range timeframes. |
| 83 | `long_signals_small_target_quick_horizon_return` | 0.6015 | 3 | 2 | F | Portfolio return from long-biased signals with small price targets and short timeframes. |
| 84 | `long_signals_small_target_quick_horizon_return_2` | 0.6525 | 2 | 2 | F | Portfolio return from long-biased signals with small price targets and short timeframes. |
| 85 | `short_signals_aggregate_portfolio_return` | 0.7668 | 0 | 0 | G | Total portfolio return using only short-biased signals. |
| 86 | `short_signals_aggregate_portfolio_return_2` | 0.8145 | 1 | 1 | G | Total portfolio return using only short-biased signals. |
| 87 | `short_signals_large_target_long_horizon_return` | 0.6463 | 1 | 1 | G | Portfolio return from short-biased signals with large price targets and extended timeframes. |
| 88 | `short_signals_large_target_long_horizon_return_2` | 0.6525 | 5 | 4 | G | Portfolio return from short-biased signals with large price targets and extended timeframes. |
| 89 | `short_signals_medium_target_mid_horizon_return` | 0.6015 | 1 | 1 | G | Portfolio return from short-biased signals with medium price targets and mid-range timeframes. |
| 90 | `short_signals_medium_target_mid_horizon_return_2` | 0.6525 | 4 | 3 | G | Portfolio return from short-biased signals with medium price targets and mid-range timeframes. |
| 91 | `short_signals_small_target_quick_horizon_return` | 0.7668 | 0 | 0 | G | Portfolio return from short-biased signals with small price targets and short timeframes. |
| 92 | `short_signals_small_target_quick_horizon_return_2` | 0.6525 | 1 | 1 | G | Portfolio return from short-biased signals with small price targets and short timeframes. |
| 93 | `long_bias_prediction_ratio_overall` | 0.6463 | 1 | 1 | H | Proportion of long-biased predictions out of all predictions for an account. |
| 94 | `long_prediction_success_rate_overall` | 0.6463 | 0 | 0 | H | Ratio of correct long-biased predictions to total long predictions across all assets. |
| 95 | `long_prediction_success_rate_overall_2` | 0.6525 | 1 | 1 | H | Ratio of correct long-biased predictions to total long predictions across all assets. |
| 96 | `short_bias_prediction_ratio_overall` | 0.6463 | 1 | 1 | H | Proportion of short-biased predictions out of all predictions for an account. |
| 97 | `short_bias_prediction_ratio_overall_2` | 0.8145 | 4 | 3 | H | Proportion of short-biased predictions out of all predictions for an account. |
| 98 | `short_prediction_success_rate_overall` | 0.6015 | 0 | 0 | H | Ratio of correct short-biased predictions to total short predictions across all assets. |
| 99 | `short_prediction_success_rate_overall_2` | 0.6525 | 0 | 0 | H | Ratio of correct short-biased predictions to total short predictions across all assets. |
| 100 | `recent_prediction_success_trend_asset` | 0.6525 | 12 | 3 | I | Recent trend of successful predictions for a specific asset, based on the last nine signals. |
| 101 | `recent_prediction_success_trend_overall` | 0.6015 | 1 | 1 | I | Measure of recent prediction success across all assets for an account. |
| 102 | `recent_prediction_success_trend_overall_2` | 0.6525 | 0 | 0 | I | Recent trend of successful predictions across all assets, based on the last nine signals. |

---

## 7. 批 1 实测（2026-10-21）与数据集判弱

回测设置：USA / TOP3000 / D1 / decay 5 / SUBINDUSTRY / truncation 0.08 / nanHandling ON / maxTrade OFF，
区间 2014-01-01 → 2023-12-31；multisim `lUTJ8bIw4X08N215STbytjR`，8/8 COMPLETE、0 ERROR。
平台 `LOW_SHARPE` / `LOW_2Y_SHARPE` 的 limit 均为 **1.58**（harvest 原样读数，不是 1.25）。

| # | 机制 | alpha | S | F | TO | 2Y | SUB | rns | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | M1a 关注度动量 Δ22（小目标/短周期） | `LL5N7RrM` | **0.99** | 0.41 | 0.136 | 0.28 | 0.30 | 1.01 | S/F/SUB/2Y |
| 2 | M1b 关注度动量 Δ66（大目标/长周期） | `9qEjXRkq` | 0.84 | 0.35 | 0.110 | 1.09 | 0.65 | 0.47 | S/F/2Y |
| 3 | M1c 胜率趋势水平 | `0mjXw85K` | 0.41 | 0.16 | 0.075 | −1.02 | 0.08 | 1.11 | S/F/SUB/2Y |
| 4 | M2a 创作者分歧（负向） | `78oNjdlv` | −0.16 | −0.04 | 0.047 | 0.95 | −0.12 | −0.39 | S/F/SUB/2Y |
| 5 | M2b 创作者分歧（正向镜像） | `e76bzrWd` | 0.16 | 0.04 | 0.047 | −0.95 | 0.12 | 0.39 | S/F/2Y |
| 6 | M3a 多头偏置反转（水平） | `qMExjXwO` | −0.96 | −0.40 | 0.080 | 1.38 | −0.67 | −0.94 | S/F/SUB/2Y |
| 7 | M3b 多头偏置反转（Δ22） | `1YjXwgRk` | −0.78 | −0.30 | 0.132 | 1.04 | −0.61 | −0.61 | S/F/SUB/2Y |
| 8 | M4 熊市技能不对称 | `WjLb7gRP` | 0.69 | 0.24 | 0.095 | **−2.41** | 0.33 | 0.52 | S/F/2Y |

**判据触发（§5 第二、三条）**：全批 8 条 **max |S| = 0.99 < 1.0** ⇒
**数据集判弱，封存 `USA-CREATOR-SIGNAL-PERF-WEAK`，不发第 2 批。**

**归因（不是"再扫一遍"）**：
1. **信号强度结构性不足**：最强的 M1a 直接刻画"创作者技能动量"，也只有 0.99；离 1.25 差 26%，
   不是壳层能补的量级。TO 5–14% 说明信号本身慢，不是换手吃掉了收益。
2. **rns 高而 S 低 = 有真信号但太弱**：M1a rns 1.01、M1c 1.11 ⇒ 剥离风格后仍有残余，
   但绝对收益不足；M2 分歧 rns −0.39~0.39 ⇒ 纯噪声。
3. **方向信息存在、但不可交易**：M3 两个方向（水平 −0.96 / Δ22 −0.78）与 2Y（1.38 / 1.04）符号相反
   ⇒ 多头偏置在近两年被定价，全期是反转、近期是动量，regime 不稳定。
   M4 2Y −2.41 是同一件事的更极端版本（熊市技能溢价近年彻底翻转）。
4. **数据滞后吃掉时效**：字段本身就是 7/28/84/364 天前的窗口合计，最短也是 7 天滞后，
   注意力信号的衰减期通常 1–5 天 ⇒ 机制与数据频率不匹配。这是数据集属性，不可修。
5. **不做的事**：不换聚合（三处 vec/标量面已无信息）、不磨窗口、不加壳层救 S（低于闸 26% 时属盲扫）。

**可复用结论**：`creator_signal_perf` 这类"预测结果统计"字段（胜率 / 偏置 / 分歧）是**慢状态量**，
在 USA/D1 上只能做出 S≈1 的弱信号；以后再遇到同族数据集（预测结果聚合类），
先看字段滞后是否 ≥7 天，是则直接跳过，不要用掉一整批配额。
