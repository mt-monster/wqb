# Robustness 审计报告 — 2026-11-03

## kqNZKN5K — PASS

**表达式**: `ts_rank(ts_mean(subtract(vec_sum(nws17_multiple_comp_event_sentiment_score), vec_sum(nws17_multiple_comp_relevance)),60),252)`
**区域**: GBR / TOP700 / FAST / delay=1 / decay=15 / truncation=0.05 / pasteurization=ON
**算子数**: 5

### Phase B 归因

| 项目 | 值 |
|---|---|
| IS 全期 Sharpe | 1.91 |
| IS 全期 Fitness | 1.18 |
| 2Y Sharpe | 1.99 |
| Sub-universe Sharpe | 1.51 |
| Self Correlation | 0.623 (< 0.7) |
| Prod Correlation | 0.623 (< 0.7) |
| WebDataScope Failed | 0 |
| PENDING | 0 |

### 逐年统计 (2014–2023)

| 年 | Sharpe | Returns | Drawdown | Margin(bp) | TO | Fitness |
|---|---|---|---|---|---|---|
| 2014 | 2.22 | 5.10% | 1.43% | 10.2 | 10.0% | 1.42 |
| 2015 | 3.36 | 7.57% | 0.90% | 15.8 | 9.6% | 2.61 |
| 2016 | 2.27 | 5.42% | 2.12% | 11.5 | 9.4% | 1.49 |
| 2017 | 2.51 | 4.48% | 0.72% | 9.8 | 9.1% | 1.50 |
| 2018 | 1.13 | 2.87% | 1.20% | 5.7 | 10.1% | 0.54 |
| 2019 | 0.60 | 1.48% | 2.28% | 3.0 | 9.9% | 0.21 |
| 2020 | 2.03 | 6.11% | 1.64% | 12.1 | 10.1% | 1.42 |
| 2021 | 1.45 | 3.84% | 2.17% | 7.6 | 10.1% | 0.80 |
| 2022 | 1.58 | 4.55% | 1.70% | 9.1 | 10.0% | 0.95 |
| 2023 | 2.53 | 6.44% | 1.00% | 12.8 | 10.1% | 1.82 |

### Phase C 反过拟合闸

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope Failed | 0 | PASS |
| Recent-3yr Sharpe | 1.85 ≥ 1.58 | PASS |
| 近 3 年每年为正 | 1.45/1.58/2.53 全 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.26 < 0.40 | PASS |
| 衰减比 | 2.53/1.91 = 1.32 ≥ 0.50 | PASS |
| 平年 | 0 | PASS |
| max/min 比 | 2.53/1.45 = 1.75 ≤ 3 | PASS |
| Sub-universe | PASS | PASS |
| Margin @ TO | 12.8bp @ 10.1% | PASS |
| 算子数 | 5（软标记，≤5 无风险） | PASS |
| 经济可解释性 | 事件情绪-相关性利差，60日平滑，252日截面排序 | PASS |

### 判定

**PASS** — 全部硬闸通过，无 CONDITIONAL 或 REJECT 项。

### 软标记

- 无

---

## 1YNzwl6k — PASS

**表达式**: `rank(ts_zscore(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 504), 22))`
**区域**: GBR / TOP700 / FAST / delay=1 / decay=15 / truncation=0.05 / pasteurization=ON
**算子数**: 4

### Phase B 归因

| 项目 | 值 |
|---|---|
| IS 全期 Sharpe | 1.73 |
| IS 全期 Fitness | 1.06 |
| 2Y Sharpe | 2.30 |
| Sub-universe Sharpe | 1.36 |
| Self Correlation | 0.125 (< 0.7) |
| Prod Correlation | 0.519 (< 0.7) |
| WebDataScope Failed | 0 |
| PENDING | 0 |

### 逐年统计 (2014–2023)

| 年 | Sharpe | Returns | Drawdown | Margin(bp) | TO | Fitness |
|---|---|---|---|---|---|---|
| 2014 | 2.12 | 5.87% | 2.95% | 7.7 | 15.3% | 1.32 |
| 2015 | 2.79 | 8.74% | 2.03% | 11.8 | 14.8% | 2.15 |
| 2016 | 2.51 | 9.03% | 1.71% | 11.1 | 16.2% | 1.87 |
| 2017 | 0.46 | 1.12% | 1.49% | 1.5 | 15.0% | 0.13 |
| 2018 | 1.89 | 5.90% | 1.27% | 7.6 | 15.5% | 1.17 |
| 2019 | -0.01 | -0.04% | 2.22% | -0.0 | 15.5% | -0.00 |
| 2020 | 0.86 | 3.56% | 2.94% | 4.4 | 16.1% | 0.40 |
| 2021 | 1.86 | 6.22% | 1.36% | 8.6 | 14.5% | 1.22 |
| 2022 | 2.94 | 11.54% | 1.65% | 14.4 | 16.0% | 2.49 |
| 2023 | 1.58 | 5.72% | 2.97% | 7.3 | 15.6% | 0.96 |

### Phase C 反过拟合闸

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope Failed | 0 | PASS |
| Recent-3yr Sharpe | 2.13 ≥ 1.58 | PASS |
| 近 3 年每年为正 | 1.86/2.94/1.58 全 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.28 < 0.40 | PASS |
| 衰减比 | 1.58/1.73 = 0.91 ≥ 0.50 | PASS |
| 平年 | 0 | PASS |
| max/min 比 | 2.94/1.58 = 1.86 ≤ 3 | PASS |
| Sub-universe | PASS | PASS |
| Margin @ TO | 7.3bp @ 15.6% | PASS |
| 算子数 | 4（软标记，≤5 无风险） | PASS |
| 经济可解释性 | NI/EV 价值比率，504日平滑，22日标准化，截面排序 | PASS |

### 判定

**PASS** — 全部硬闸通过，无 CONDITIONAL 或 REJECT 项。

### 软标记

- 无

---

## JjeGEzaE — PASS（d5W0RQZv 的 prod 修复变体）

**表达式**: `trade_when(rank(ts_mean(ern3_pre_reptime, 22)) > 0.7, signed_power(subtract(group_rank(single_bucket_5day_return_estimate_ohlcv_img, country), 0.5), 0.3), 0)`
**区域**: GLB / MINVOL1M / FAST / delay=1 / decay=10 / truncation=0.08 / pasteurization=ON / nanHandling=OFF
**算子数**: 6

### Phase B 归因

| 项目 | 值 |
|---|---|
| IS 全期 Sharpe | 2.42 |
| IS 全期 Fitness | 1.38 |
| 2Y Sharpe | 2.58 |
| Sub-universe Sharpe | 1.16 |
| Self Correlation | 0.568 (< 0.7) |
| Prod Correlation | 0.690 (< 0.7) |
| WebDataScope Failed | 0 |
| PENDING | 0 |

### 逐年统计 (2014–2023)

| 年 | Sharpe | Returns | Drawdown | Margin(bp) | TO | Fitness |
|---|---|---|---|---|---|---|
| 2014 | 0.74 | 2.25% | 2.92% | 2.4 | 18.5% | 0.26 |
| 2015 | 4.18 | 6.80% | 0.71% | 10.7 | 12.7% | 3.06 |
| 2016 | 4.94 | 6.87% | 0.39% | 11.1 | 12.4% | 3.66 |
| 2017 | 2.27 | 2.45% | 0.83% | 5.2 | 9.4% | 1.00 |
| 2018 | 4.51 | 6.65% | 0.66% | 14.3 | 9.3% | 3.29 |
| 2019 | 2.30 | 2.80% | 0.58% | 7.7 | 7.2% | 1.09 |
| 2020 | 0.28 | 0.42% | 1.29% | 1.2 | 6.9% | 0.05 |
| 2021 | 2.80 | 5.01% | 1.78% | 14.3 | 7.0% | 1.77 |
| 2022 | 3.69 | 5.35% | 0.69% | 14.9 | 7.2% | 2.41 |
| 2023 | 1.31 | 1.66% | 1.33% | 4.7 | 7.1% | 0.48 |

### Phase C 反过拟合闸

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope Failed | 0 | PASS |
| Recent-3yr Sharpe | 2.60 ≥ 1.58 | PASS |
| 近 3 年每年为正 | 2.80/3.69/1.31 全 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.38 < 0.40 | PASS |
| 衰减比 | 1.31/2.42 = 0.54 ≥ 0.50 | PASS |
| 平年 | 0 | PASS |
| max/min 比 | 3.69/1.31 = 2.82 ≤ 3 | PASS |
| Sub-universe | PASS | PASS |
| Margin @ TO | 4.7bp @ 7.1% | PASS |
| 算子数 | 6（软标记） | PASS |
| 经济可解释性 | 预报时间门控+国家级5日回报估计的保号平方根 | PASS |

### 判定

**PASS** — 全部硬闸通过，无 CONDITIONAL 或 REJECT 项。

### 软标记

- 算子数 6（>5 提示过拟合风险，但 REGULAR 不因此 REJECT）