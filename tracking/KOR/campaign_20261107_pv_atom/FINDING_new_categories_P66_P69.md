# 未开采类别开荒第一批：quant_factor_lib / price_signal_dl / ai_equity_alpha（2026-11-07）

来源：`reference/kor_dataset_ranking.json` 筛出 54 个未开采且 usableFieldCount≥8 的候选，按「低拥挤 + 高覆盖」取前几个。

## 1. quant_factor_lib（model · 32 VECTOR · cov 0.68–0.88 · aC 0–6）——判死

Cassie 信用风险 / 破产预测因子库（Altman Z、Merton 距离违约、Ohlson O、9m/1y/2y 破产压力分、债务比率）。
扫描 10 条（统一几何 `subtract(0.5, group_rank(ts_mean(vec_avg(F),22),sector))`）：

| alpha | 字段 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| kqN9bkoK | cassie_score（综合信用分） | 0.74 | 0.42 | 0.049 | 0.14 |
| d5Wvg8Ov | insolvency_stress_1y | 0.66 | 0.34 | 0.050 | 0.50 |
| leA1k687 | cassie_impliedalpha | 0.55 | 0.26 | 0.052 | 0.20 |
| 2rAeQqlZ | altman_zscore | 0.46 | 0.24 | 0.060 | 0.58 |
| 其余 6 条 | merton / ohlson / chs_default / debt_equity / ocf_currliab / short_longterm | \|S\|≤0.46 | | | 多为负 |

**判定：死。** 最高 |S| 0.74，且 TO 只有 0.05（信息更新极慢、季度级），与 1.58 线相距太远。
「破产风险异象」在 KOR 这个 10 年窗内不成立。

## 2. price_signal_dl（model · 28 MATRIX · cov 0.955–0.9937 · aC 0–62）——信号弱，降级

4 族 × 7 指标：`normalized_trend_indicator_*` / `normalized_volume_indicator_*` / `raw_trend_indicator_*` / `raw_volume_indicator_*`。
其中 22 个字段 aC ≤ 2（几乎无人用）。

**（a）P66 十字段扫描：10/10 全部失败**，返回 `No alpha_id in sim response`。
**（b）P68 诊断（3 条，全部成功）**：把 `ts_backfill` 去掉就正常 ⇒ **失败由 `ts_backfill(F,5)` 叠加在该数据集上触发**，不是字段不可仿真。

| 表达式 | S | F | TO | 2Y |
|---|---:|---:|---:|---:|
| 裸字段 `raw_trend_indicator_1` | 0.40 | 0.14 | 0.266 | 0.87 |
| `group_rank(field, sector)` | 0.28 | 0.07 | 0.255 | 0.54 |
| `subtract(0.5, group_rank(ts_mean(field,22),sector))` | 0.24 | 0.06 | 0.205 | −0.11 |

**判定：信号弱（本族最强字段裸用也只有 S 0.40），降级为低优先。** 与 aC 总量 9 的「无人开采」现状一致。

## 3. 工具坑候选（待二次确认）

`ts_backfill` 与部分 model 类 MATRIX 字段组合会导致**整批子仿真无 alpha 返回**（harvest 报 `No alpha_id in sim response`，expression 为空串）。
排查顺序：先把 `ts_backfill` 去掉做最小复现，再用 `validate_expressions` 确认字段合法（本例字段合法）。

## 4. ai_equity_alpha（model · 582 VECTOR · cov 1.0 · aC 53）——扫描中（P69）

字段族结构（582 个）：debt_to_equity_ratio_metric ×20 / cashflow_trend_analysis ×14 / shareholder_yield_metric ×13 /
correlation_risk_factor ×10 / forecast_yield_metric ×10 / fund_flow_prediction_metric ×10 / intrinsic_valuation_estimate ×10 /
shareholder_treatment_metric ×10 / accounting_forensics_factor ×7 / earnings_quality_score ×7 / information_opacity_score ×8 / buzz_intensity_score ×8 …

P69 取 10 个跨族代表字段做统一几何扫描。