
## omoK1A5m（USA / analyst_factor_signals）— 2026-10-19 14:10

**表达式**
```
quantile(group_rank(hump(ts_backfill(winsorize(ts_av_diff(eps_q1_estimate_qoq_growth, 252), std=4), 756), hump=0.01), subindustry))
```
settings：USA / TOP3000 / D1 / decay=1 / RAM / trunc=0.08 / pasteurization=ON / nanHandling=ON

**顶层指标**：S 2.05 ｜ F 1.24 ｜ 2Y 1.79 ｜ SUB 0.93 ｜ TO 0.0365 ｜ margin 25.25bp ｜ CW PASS ｜ CLUSTER 1.45(WARN)
**相关性**：prod **0.6489** ✓ ｜ self **0.4793** ✓

### Phase B 逐年（2014–2023）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | 2.63 | 2.71 | 3.62 | 2.03 | 2.13 | 1.13 | **−0.01** | 3.16 | 2.69 | **0.60** |

### Phase C 判定

| 检查 | 值 | 阈值 | 结果 |
|---|---:|---|---|
| Failed RA | 0 | =0 | PASS |
| Recent-3yr Sharpe | 均值 2.15，每年>0.3 | ≥1.58 且每年>0.3 | PASS |
| CV_Sharpe（近3年） | **0.518** | <0.40 | **CONDITIONAL** |
| 衰减比（2023/全期） | **0.293** | ≥0.50 | **REJECT** |
| max/min（近3年） | **5.27** | ≤3 | **REJECT** |
| 平年（近3年） | 0 | 0 | PASS |
| SUB | 0.93 | PASS | PASS |
| Margin@TO | 25.25bp @ 3.65% | ≥5bp | PASS |
| 算子数 | 6 | 软标记 | 软标记（>5） |
| 经济可解释性 | 分析师一致预期 Q1 EPS 环比增长率的异常变化（横截面行业内排序），市场对"增长率"变化反应不足 | 一句话可写 | PASS |

**审计 verdict：REJECT**（衰减比 0.293 < 0.30；近 3 年 max/min 5.27 > 5；CV 0.518 落 CONDITIONAL 带）

### 处置

用户 2026-10-19 14:06 明确指令「提交 omoK1A5m」。已向用户如实报告上述两个 REJECT 级标记
（2023 年 Sharpe 0.60，信号衰减）后，按用户指令走 `force=True` 路径提交（留痕）。
台账 `robustness_omoK1A5m` 记 verdict=REJECT + failed_checks，不掩盖审计结论。

## akVnvzX5（USA / analyst_factor_signals，偏度族）— 2026-10-19 19:30

**表达式**
```
quantile(group_rank(hump(ts_backfill(winsorize(group_neutralize(ts_zscore(eps_y1_estimate_skewness, 315), industry), std=4), 252), hump=0.01), subindustry))
```
settings：USA / TOP3000 / D1 / decay=1 / RAM / trunc=0.08（7 算子）

**顶层**：S 1.83 ｜ F 1.06 ｜ 2Y 1.87 ｜ SUB 0.95 ｜ TO 0.0346 ｜ margin 24.02bp ｜ CW PASS ｜ CLUSTER 1.04
**相关性**：prod **0.6594** ✓ ｜ self **0.5694** ✓（对 omoK1A5m 0.569）

### 逐年 Sharpe（2014–2023）
3.93 / 2.56 / 1.43 / 1.07 / **0.47** / 1.92 / 0.95 / **2.40** / 2.25 / **1.35**

### Phase C 判定

| 检查 | 值 | 阈值 | 结果 |
|---|---:|---|---|
| Failed RA | 0 | =0 | PASS |
| Recent-3yr Sharpe | 均值 2.00，每年 >0.3 | ≥1.58 且每年>0.3 | **PASS** |
| CV_Sharpe（近3年） | **0.232** | <0.40 | **PASS** |
| 衰减比（2023/全期） | **0.738** | ≥0.50 | **PASS** |
| max/min（近3年） | **1.78** | ≤3 | **PASS** |
| 平年（近3年） | 0 | 0 | PASS |
| SUB | 0.95 | PASS | PASS |
| Margin@TO | 24.02bp @ 3.46% | ≥5bp | PASS |
| 算子数 | 7 | 软标记 | 软标记（>5） |
| 经济可解释性 | 分析师预期分布的**偏度异常**：预期右偏（乐观分歧）= 后续跑输；与"增长率"机制正交 | 一句话可写 | PASS |

**审计 verdict：PASS**（唯一软标记：算子数 7 > 5）

用户 2026-10-19 19:26 明令提交，审计 PASS 后直接走平台 POST。
