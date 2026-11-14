# 稳健性评估 — O0W0w3P7（EUR / TOP2500 / D1 / MARKET）

- 评估时间：2026-11-11 02:5x（本地）
- 表达式：`group_rank(ts_rank(ts_sum(vec_avg(mws46_story_count), 5), 110), group_cartesian_product(sector, country))`
- 设置：`EUR · TOP2500 · delay=1 · decay=1 · neutralization=MARKET · truncation=0.08 · nanHandling=ON`
- 算子数：5（group_rank / ts_rank / ts_sum / vec_avg / group_cartesian_product）
- 塔归属：`EUR/D1/NEWS`（multiplier 1.4）；当季计数 1 → 交后 2（**未点亮**，需 ≥3）
- 主题：`MATCHES_THEMES` PENDING 命中 `GLB/D1 Power Pool Nov'26`（multiplier 1.0）；WARNING 命中 `USA/D1 turnover 15…30% Theme`

## 1 逐年稳定性（IS 2014–2023，MCP get_alpha_yearly_stats）

| 年 | Sharpe | Fitness | TO | Returns | DD |
|---|---|---|---|---|---|
| 2014 | 2.27 | 0.77 | 0.2852 | 0.0329 | 0.0060 |
| 2015 | 2.95 | 1.26 | 0.2830 | 0.0515 | 0.0114 |
| 2016 | 2.87 | 1.29 | 0.3114 | 0.0634 | 0.0106 |
| 2017 | 2.26 | 0.79 | 0.3108 | 0.0377 | 0.0099 |
| 2018 | 1.80 | 0.58 | 0.2851 | 0.0301 | 0.0074 |
| 2019 | 1.97 | 0.67 | 0.2743 | 0.0320 | 0.0086 |
| 2020 | 3.38 | 1.86 | 0.2754 | 0.0832 | 0.0100 |
| 2021 | 2.83 | 1.23 | 0.2655 | 0.0500 | 0.0086 |
| 2022 | 3.55 | 1.91 | 0.2685 | 0.0777 | 0.0066 |
| 2023 | 3.06 | 1.34 | 0.2725 | 0.0521 | 0.0063 |

- 逐年 Sharpe 全正：10/10；最低 1.80（2018），仍 ≥1.58 闸
- mean = 2.694，std = 0.561，**CV = 0.208**（阈值 0.60 → 通过，余量 0.39）
- TO 区间 0.2655–0.3114，无跳变；DD 最大 0.0114（0.68×年化收益量级）
- 无单年塌陷、无趋势衰减（后 4 年均值 3.21 > 前 4 年均值 2.59）

## 2 闸门现状（is.checks，17 条，FAIL 0）

| 闸 | 值 | 限 | 判定 | 余量 |
|---|---|---|---|---|
| LOW_SHARPE | 2.72 | 1.58 | PASS | +1.14 |
| LOW_FITNESS | 1.15 | 1.00 | PASS | **+0.15** |
| LOW_2Y_SHARPE | 3.31 | 1.58 | PASS | +1.73 |
| LOW_SUB_UNIVERSE_SHARPE | 1.41 | 1.41 | PASS | **≈0（显示同位）** |
| CLUSTER_TEST | 2.08 | 1.58 | PASS | +0.50 |
| HIGH/LOW_TURNOVER | 0.2832 | 0.70/0.01 | PASS | 充裕 |
| CONCENTRATED_WEIGHT | — | — | PASS | — |
| SELF_CORRELATION | 0.0789（本地） | 0.70 | PASS | +0.62 |
| PROD_CORRELATION | 0.6403（平台实测 02:24） | 0.70 | PASS | **+0.06** |

## 3 结论

**verdict = PASS**，软标记 2 项：
- `SUB_UNIVERSE_ZERO_MARGIN`：sub 1.41 / limit 1.41，实际余量 <0.005（IS 静态，提交时不会变，但无缓冲）
- `FITNESS_THIN`：F 1.15，余量 +0.15

failed_checks：无。

## 4 备查：本族结构扫描（同日 14 条仿真实测，见 §op-min 报告）

轴/向量/窗口/归一/decay 五类变体中，**仅原式 sub 闸 PASS**；其余 sub/S 比全部 < 0.518 门槛。
⇒ 该结构已达局部最优，无压缩空间。
