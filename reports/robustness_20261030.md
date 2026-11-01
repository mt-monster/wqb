# Robustness 归因报告 — 2026-10-30

## j2YNnKOQ（GBR / TOP700 / D1 / INDUSTRY / decay10 / trunc0.05）— CONDITIONAL

**表达式**：`rank(ts_quantile(ts_av_diff(divide(quarterly_ebit_value, current_enterprise_value), 504), 22, driver=gaussian))`

**状态**：IS 未提交｜S 2.15 / F 1.80 / 2Y 2.09 / sub 1.41 / TO 0.1537 / self 0.3699 / prod 0.67（refresh 实测）

### 逐年 Sharpe（2014–2023，十年全有数据）
| 年 | Sharpe | PnL(¥) | margin | 年 | Sharpe | PnL(¥) | margin |
|---|---|---|---|---|---|---|---|
| 2014 | 2.27 | 809,006 | 0.00106 | 2019 | 1.24 | 576,063 | 0.00071 |
| 2015 | 1.61 | 719,217 | 0.00092 | 2020 | 2.80 | 2,122,684 | 0.00281 |
| 2016 | 3.70 | 1,853,901 | 0.00222 | 2021 | 1.81 | 940,204 | 0.00125 |
| 2017 | 1.98 | 684,848 | 0.00088 | 2022 | 1.22 | 791,806 | 0.00095 |
| 2018 | 2.38 | 961,929 | 0.00119 | 2023 | 3.03 | 1,711,491 | 0.00212 |

### 近窗判定（最近 3 个 IS 年 = 2021/2022/2023）
| 检查项 | 值 | 判定 |
|---|---|---|
| Recent-3yr Sharpe | 1.81+1.22+3.03 = **6.06**（≥1.58，每年>0.3） | ✅ PASS |
| 衰减比（2023/全期） | 3.03/2.15 = **1.41**（≥0.50） | ✅ PASS |
| CV_Sharpe | **0.457**（0.40–0.60） | ⚠️ CONDITIONAL |
| max/min Sharpe | 3.03/1.22 = **2.48**（≤3） | ✅ PASS |
| 平年（最近 3 年） | 0 | ✅ PASS |
| Sub-universe | LOW_SUB_UNIVERSE_SHARPE = 1.41 PASS | ✅ PASS |
| 算子数 | 4（≤5，无过拟合标记） | ✅ PASS |
| Margin @ turnover | ~0.0014（≈14bp，TO 15%）≥5bp | ✅ PASS |
| Top-5 集中度 | PnL 曲线下采样，无逐股分解 → 未评估 | ⚠️ 软标记 |
| 经济可解释性 | EBIT/EV 盈利收益率偏离 1 年均值 → 均值回归，市场反应不足 | ✅ PASS |

### 判定
**CONDITIONAL**（唯一软标记：CV_Sharpe 0.457 落在 0.40–0.60 区间；2022 弱年 1.22 但仍为正）。
按用户指令（点名免查prod提交）进入提交；与 E56oYEkL 先例一致。

---

## 58E7jkaN（GBR / TOP700 / D1 / FAST / decay15 / trunc0.05 / nan ON）— CONDITIONAL

**表达式**：`ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(multiply(vec_count(nws17_multiple_comp_ssc), rank(vec_avg(nws17_multiple_comp_event_similarity_days))), 60), 252), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)`

**状态**：IS 未提交｜S 1.85 / F 1.14 / 2Y 1.91 / sub 1.50 / TO 0.0802 / self 0.0693 / prod 0.5611（refresh 实测）

### 逐年 Sharpe（2014–2023，十年全有数据）
| 年 | Sharpe | PnL(¥) | margin | 年 | Sharpe | PnL(¥) | margin |
|---|---|---|---|---|---|---|---|
| 2014 | 1.65 | 398,767 | 0.00091 | 2019 | 0.51 | 127,397 | 0.00031 |
| 2015 | 3.19 | 823,529 | 0.00196 | 2020 | 1.67 | 503,942 | 0.00128 |
| 2016 | 1.69 | 435,125 | 0.00107 | 2021 | 1.64 | 440,572 | 0.00104 |
| 2017 | 3.30 | 607,600 | 0.00160 | 2022 | 0.98 | 293,562 | 0.00069 |
| 2018 | 1.52 | 406,749 | 0.00097 | 2023 | 2.99 | 835,322 | 0.00198 |

### 近窗判定（最近 3 个 IS 年 = 2021/2022/2023）
| 检查项 | 值 | 判定 |
|---|---|---|
| Recent-3yr Sharpe | 1.64+0.98+2.99 = **5.61**（≥1.58，每年>0.3） | ✅ PASS |
| 衰减比（2023/全期） | 2.99/1.85 = **1.62**（≥0.50） | ✅ PASS |
| CV_Sharpe | **0.548**（0.40–0.60） | ⚠️ CONDITIONAL |
| max/min Sharpe | 2.99/0.98 = **3.05**（3–5） | ⚠️ CONDITIONAL |
| 平年（最近 3 年） | 0 | ✅ PASS |
| Sub-universe | LOW_SUB_UNIVERSE_SHARPE = 1.50 PASS | ✅ PASS |
| 算子数 | 9（>5，过拟合软标记） | ⚠️ 软标记 |
| Margin @ turnover | ~0.00118（≈12bp，TO 8%）≥5bp | ✅ PASS |
| Top-5 集中度 | PnL 曲线下采样，无逐股分解 → 未评估 | ⚠️ 软标记 |
| 经济可解释性 | 新闻关注度×事件相似度的 252 日时序反转 | ✅ PASS |

### 判定
**CONDITIONAL**（软标记：CV_Sharpe 0.548 + max/min 3.05 + 算子数 9）。
按用户指令（免查prod提交）进入提交；与 j2YNnKOQ / E56oYEkL 先例一致。
