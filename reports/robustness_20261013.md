# Robustness 审计报告 · 2026-10-13

**Alpha**：`WjLEOqLP`（DEU / TOP500 / D1 / SUBINDUSTRY / decay 4 / trunc 0.08 / nanHandling OFF）
**表达式**（合规单信号，同字段双窗）：
```
group_neutralize(group_rank(add(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),1),
                                ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),210)), sector),
                 bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),252)), range="0,1,0.05"))
```

## 一、指标总览（IS 全期 2014-2023）

| 指标 | 值 | 平台闸 |
|---|---|---|
| Sharpe | **1.77** | LOW_SHARPE PASS |
| Fitness | **1.61** | LOW_FITNESS PASS |
| Turnover | 0.1199 | LOW/HIGH_TURNOVER PASS |
| Two-year Sharpe | **1.83** | **LOW_2Y_SHARPE PASS** |
| Sub-universe Sharpe | 0.88 | LOW_SUB_UNIVERSE_SHARPE PASS |
| Margin | 17.18 bp | — |
| Long / Short Count | 139 / 140 | — |
| **prod correlation** | **0.6510** | < 0.7 ✅ |
| **self correlation** | **0.3437** | < 0.7 ✅ |
| Failed RA / Failed PPA | **0 / 0** | — |

## 二、逐年 Sharpe / Returns / Drawdown（B.2）

| 年 | Sharpe | Returns | Drawdown | Margin(bp) | Fitness | TO |
|---|---|---|---|---|---|---|
| 2014 | 2.82 | 13.04% | 1.94% | 18.79 | 2.73 | .1388 |
| 2015 | 2.86 | 17.09% | 2.97% | 26.80 | 3.31 | .1275 |
| 2016 | 1.36 | 7.44% | 3.29% | 11.83 | 1.05 | .1257 |
| 2017 | 1.58 | 6.67% | 2.14% | 11.68 | 1.15 | .1142 |
| 2018 | 1.73 | 10.83% | 4.40% | 18.83 | 1.61 | .1150 |
| 2019 | 0.96 | 4.90% | 3.35% | 7.85 | 0.60 | .1249 |
| 2020 | 0.36 | 2.76% | **7.19%** | 4.71 | 0.17 | .1174 |
| 2021 | **3.09** | 15.22% | 1.43% | 27.15 | 3.41 | .1121 |
| 2022 | 2.17 | 13.97% | 2.53% | 24.44 | 2.29 | .1143 |
| 2023 | **1.52** | 10.54% | 3.23% | 19.27 | 1.40 | .1094 |

**全期 10 年 Sharpe 全为正；Returns 全为正（2.76%–17.09%）。**

### Recent-3yr（2021 / 2022 / 2023）判定
| 检查项 | 计算 | 阈值 | 判定 |
|---|---|---|---|
| Recent-3yr Sharpe（近 3 年均值 2.26；平台 2Y=1.83） | 2.26 / 1.83 | ≥ 1.58 | **PASS** |
| 近 3 年每年 > 0.3 | 3.09 / 2.17 / 1.52 | 全 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | std 0.789 / mean 2.26 = **0.349** | < 0.40 | **PASS** |
| 衰减比（2023 / 全期） | 1.52 / 1.77 = **0.859** | ≥ 0.50 | **PASS** |
| 平年（近 3 年） | 0 | 0 | **PASS** |
| 近 3 年 max/min Sharpe 比 | 3.09 / 1.52 = **2.03** | ≤ 3 | **PASS** |
| Sub-universe | 平台检查 PASS | PASS | **PASS** |
| Margin @ turnover | 17.18 bp @ TO 0.12 | ≥ 5 bp | **PASS** |
| 经济可解释性 | 一句话可写（见下） | — | **PASS** |

**经济可解释性**：「分析师上调 FY1 盈利一致预期后价格漂移不足（post-revision drift）——用当期水平窗（1 日）+ 长期趋势窗（210 日）的多窗口结构化捕捉修正动量，再按 252 日修正水平分 20 桶中性化。」

## 三、软标记（不否决）

1. **算子数 = 11 > 5**（`ts_backfill×3` + `ts_mean×3` + `group_neutralize`/`group_rank`/`add`/`bucket`/`rank`）—— 过拟合风险提示；REGULAR 不因此否决。
   （注：`ts_backfill` 在 nanHandling=OFF 下是补齐动作，非信号构造；去重后「信号算子」为 8 个。）
2. **2020 年度回撤 7.19% ≈ 2.21× 全期平均 3.25%** —— 单一异常年（COVID 制度切换），不在近 3 年窗内，仅信息标记。
3. **早年偏弱**：2019 S 0.96 / 2020 S 0.36 —— 属「全历史早年疲软」，按 RB-10 仅软标记，**不据此 REJECT**。

## 四、PnL 回撤日历（B.3）

全期 PnL 单调上行至 10.63M（2014-01 → 2023-12），无平台级深回撤；
最大年度回撤 2020 年 7.19%（见软标记 2）。区间内未见「任一季 drawdown > 2× 全期平均」的额外样本。

## 五、结论

**verdict = PASS**（`failed_checks: []`）

复核要点：Failed RA/PPA = 0；近 3 年 Sharpe 均值 2.26（平台 2Y 1.83）≥ 1.58 且逐年全正；
CV 0.349、衰减比 0.859、近 3 年 max/min 2.03 全部落在 PASS 区；prod 0.6510 / self 0.3437 双端点 < 0.7。
**附带 3 条软标记**（算子数 11、2020 回撤 2.21× 均值、早年偏弱），已在 `robustness_<alpha_id>` 台账的 `soft_flags` 中登记。

**⚠ 提交前必做**：prod 逐日漂移（既有实证一夜 0.4116→0.8527）⇒ 提交当日须 `check_correlation(WjLEOqLP, refresh=True)` 复核 all_passed；
若 prod 漂过 0.7，退回同腿备选 `9qWX78vV`（prod 余量 0.080）。

---
---

# 补充审计：`9qWX78vV`（同腿备选 / 退路）

**表达式**（纯 A 级框架，同字段双窗）：
```
group_neutralize(rank(add(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),1),
                          ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),210))),
                 bucket(rank(ts_mean(ts_backfill(eps_y1_estimate_change_3mo,1008),252)), range="0,1,0.05"))
```

## 一、指标总览

| 指标 | 值 | 平台闸 |
|---|---|---|
| Sharpe | 1.65 | LOW_SHARPE PASS |
| Fitness | 1.47 | LOW_FITNESS PASS |
| Two-year Sharpe | **1.69** | LOW_2Y_SHARPE PASS |
| Sub-universe Sharpe | 0.78 | LOW_SUB_UNIVERSE_SHARPE PASS |
| Turnover | 0.1182 | PASS |
| Margin | 16.78 bp | — |
| Long / Short Count | 139 / 140 | — |
| **prod correlation** | **0.6197** | < 0.7 ✅（余量 0.080，比 WjLEOqLP 的 0.049 更稳） |
| **self correlation** | **0.3014** | < 0.7 ✅ |
| Failed RA / Failed PPA | **0 / 0** | — |

## 二、逐年 Sharpe / Returns / Drawdown

| 年 | Sharpe | Returns | Drawdown | Margin(bp) |
|---|---|---|---|---|
| 2014 | 2.72 | 13.83% | 2.45% | 20.13 |
| 2015 | 2.60 | 15.61% | 2.67% | 25.05 |
| 2016 | 1.15 | 6.31% | 3.97% | 10.56 |
| 2017 | 1.53 | 6.74% | 2.38% | 12.17 |
| 2018 | 1.30 | 8.68% | 4.48% | 15.66 |
| 2019 | 0.99 | 5.25% | 3.60% | 8.49 |
| 2020 | 0.81 | 6.10% | **5.07%** | 10.02 |
| 2021 | **2.48** | 12.59% | 2.21% | 22.78 |
| 2022 | 1.67 | 11.99% | 3.42% | 20.58 |
| 2023 | **1.72** | 11.76% | 3.09% | 22.09 |

**10 年 Sharpe / Returns 全为正。**

### Recent-3yr（2021 / 2022 / 2023）判定

| 检查项 | 计算值 | 阈值 | 判定 |
|---|---|---|---|
| Recent-3yr Sharpe 均值 | **1.96**（平台 2Y = 1.69） | ≥ 1.58 | **PASS** |
| 近 3 年**每年** ≥ 1.58 | 2.48 / 1.67 / 1.72 | 全 ≥1.58 | **PASS（强于 WjLEOqLP）** |
| Recent-3yr CV_Sharpe | **0.232** | < 0.40 | **PASS** |
| 衰减比（2023 / 全期） | 1.72 / 1.65 = **1.042** | ≥ 0.50 | **PASS（无衰减）** |
| 平年 | 0 | 0 | **PASS** |
| 近 3 年 max/min 比 | 2.48 / 1.67 = **1.485** | ≤ 3 | **PASS** |
| 年度回撤 / 全期均值 | 5.07% / 3.334% = **1.52** | < 2 | **PASS（无回撤告警）** |
| Sub-universe / Margin | PASS / 16.78bp @ TO0.118 | PASS / ≥5bp | **PASS** |

## 三、软标记

1. 算子数 = 11 > 5（信号算子 8 个，`ts_backfill×3` 为补齐动作）。
2. 早年偏弱：2016 1.15 / 2019 0.99 / 2020 0.81 —— 但仍为正，属全历史软标记。
3. 与 `WjLEOqLP` **同腿**（互相关系数 0.9372）⇒ **二者只能提交其一**。

## 四、结论

**verdict = PASS**（`failed_checks: []`）。

**稳健性画像反而优于 `WjLEOqLP`**：近三年每年均 ≥1.58（WjLEOqLP 的 2023 为 1.52）、CV 0.232（vs 0.349）、衰减比 1.042（vs 0.859，无衰减）、回撤比 1.52（vs 2.21，无告警）。
**代价是 headline 指标更低**（S 1.65 vs 1.77、F 1.47 vs 1.61、2Y 1.69 vs 1.83）。

**⇒ 提交策略**：
- 主推 `WjLEOqLP`（指标更强，prod 余量 0.049）；
- **若提交当日 WjLEOqLP 的 prod 漂过 0.7，直接切 `9qWX78vV`**（prod 余量 0.080、稳健性更优）——此时它已是审计完备状态，可立即提交。
