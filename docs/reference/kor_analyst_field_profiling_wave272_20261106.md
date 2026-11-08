# KOR Analyst 字段画像 · wave272 双集（2026-11-06）

> 用途：wave272 的字段侧依据。配套数据集扫描 → `docs/reference/kor_analyst_dataset_scan_20261106.md`。
> 派生原始 JSON：`tracking/KOR/reference/field_profile/kor_analyst_factor_signals_fields_current.json` / `..._analyst_base_ref_fields_current.json`。
> 平台口径：KOR / TOP600 / D1；`get_datafields` 全量翻页（`complete:true`，无截断）。

## 一、analyst_factor_signals（59 字段，全 MATRIX，cov 均值 0.577）

**类型**：MATRIX 59 —— 直接可用，**不需要 vec_\* 包裹**（这是它与 base_ref 最大的工程差别）。
**刷新频率**：3 个月窗口的预计算修正量（`*_change_3mo`）⇒ 事实上的**月度级慢变量**，单靠水平值 TO 会很低。

| 语义族 | 字段数 | 平均 cov | 代表字段 |
|---|---:|---:|---|
| **已实现真值** | 2 | 0.401 | `eps_actual_q1_qoq_growth` / `eps_actual_q1_yoy_growth` |
| **修正趋势** | 6 | 0.492 | `eps_estimate_trend_slope_1yr` / `eps_estimate_trend_slope_2yr` / `eps_estimate_trend_slope_3yr` / `revenue_estimate_trend_slope_1yr` |
| **修正动量** | 8 | 0.728 | `eps_q1_estimate_change_1mo` / `eps_revision_magnitude` / `eps_y1_estimate_change_3mo` / `eps_y2_estimate_change_3mo` |
| **预期增长/增速** | 6 | 0.520 | `eps_q1_estimate_qoq_growth` / `eps_q1_estimate_yoy_growth` / `eps_q2_estimate_qoq_growth` / `revenue_q1_estimate_qoq_growth` |
| **其他** | 6 | 0.484 | `eps_q1_estimate_sequential` / `eps_trailing_4q_estimate` / `revenue_estimate_volatility_adj_2yr` / `revenue_estimate_zscore` |
| **预期分歧/分布形态** | 15 | 0.566 | `eps_q1_estimate_skewness` / `eps_q2_estimate_skewness` / `eps_y1_estimate_asymmetry` / `eps_y1_estimate_coeff_var` |
| **盈余惊喜** | 4 | 0.503 | `eps_surprise_mean_diff` / `eps_surprise_stddev` / `revenue_surprise_mean_diff` / `revenue_surprise_stddev` |
| **预期增长** | 8 | 0.605 | `eps_y1_cagr_2yr` / `eps_y1_cagr_3yr` / `eps_y1_cagr_4yr` / `eps_y1_cagr_5yr` |
| **预期水平** | 4 | 0.777 | `eps_y1_consensus_value` / `eps_y2_consensus_value` / `revenue_y1_consensus_value` / `revenue_y2_consensus_value` |

**关键字段参数**：
- `eps_y1_estimate_change_3mo` cov 0.786 / aC 54 —— FY1 EPS 一致预期 3 个月变化，本集拥挤度最高字段。
- `eps_revision_magnitude` cov 0.786 / aC 34 —— 修正幅度（Street revision magnitude）。
- `eps_y1_estimate_coeff_var` cov 0.575 / aC 1 —— FY1 预期离散系数（分歧度），几乎零拥挤。
- `eps_y1_estimate_skewness` cov 0.797 / aC 3 —— 预期分布偏度。
- `eps_surprise_stddev` cov 0.427 / aC 2 —— 历史惊喜波动。

**语义陷阱（写进纪律）**：
1. `*_y1_consensus_value` 的 description 是 "Forecast FY1 EPS **growth rate**"，不是 EPS 绝对水平 ⇒ 它已经是一个增速，别再拿它去减 y2 求"增长"。
2. `*_cagr_*` 是**预测期内的复合增速**，随时间缓慢漂移，与 `change_3mo` 相关性高但不是同一信息：前者是水平，后者是变动。

## 二、analyst_base_ref（14 字段，VECTOR 10 / MATRIX 4，cov 均值 0.732）

**类型**：事件型 VECTOR（每个标的每期一条「共识 vs 实际」记录），**必须 `vec_avg` 降维**；直接 `rank(vector)` 会整批拒。
**语义**：这是全 KOR analyst 面**唯一的 SUE 专集** —— 同时给出共识均值/中位/高低/标准差/家数与实际值。

| 字段 | 类型 | cov | aC | 用法 |
|---|---|---:|---:|---|
| `consensus_surprise_percentage` | VECTOR | 0.668 | 27 | 主信号：惊喜百分比（共识与实际之差，已归一） |
| `consensus_vs_actual_diff` | VECTOR | 0.668 | 8 | 绝对惊喜（与上面差一个分母，可做尺度稳健性对照） |
| `consensus_stddev_estimate` | VECTOR | 0.668 | **0** | 分析师分歧度（零拥挤） |
| `num_estimates_consensus` | VECTOR | 0.668 | **0** | 覆盖家数（零拥挤） |
| `consensus_mean_estimate` | VECTOR | 0.668 | 1 | 预期水平，做归一化分母 |
| `consensus_high_estimate` / `low_estimate` | VECTOR | 0.668 | 2 / 3 | 预期区间 → 区间宽度/均值 = 分歧度 |
| `reported_actual_value` | VECTOR | 0.668 | **0** | 实际值（可与共识配对造第 2 个惊喜口径） |
| `last_close_price` | MATRIX | 1.000 | 12 | 归一化分母（点对点复权价） |
| `split_adjustment_factor` | MATRIX | 0.568 | 15 | 拆股因子，纯工程字段 |
| `consensus_median_estimate` | VECTOR | 0.668 | 6 | 中位数共识（抗异常值版本） |

**语义陷阱**：
1. `consensus_surprise_percentage` 是**逐事件**惊喜，一个标的同期可能有多条（EPS / 营收 / 分红等 `actual_category`）。`vec_avg` 等于把这些口径**等权平均**，必须先声明这一点（不是纯 EPS 惊喜）。
2. `num_estimates_consensus` 的 `vec_avg` 是「多事件口径的平均家数」，做覆盖广度时它的变化量比水平值干净。
