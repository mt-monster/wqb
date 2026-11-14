# 稳健性审计 · d5a2aO7v（DEU / TOP500 / D1）

- 审计时间：2026-11-13 12:5x（GMT+8）
- 表达式：`subtract(group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings), 110), 252), sector), group_rank(ts_delta(vec_avg(shrt3_bar), 220), sector))`
- 设置：DEU / TOP500 / delay 1 / decay 8 / SUBINDUSTRY / truncation 0.08 / nanHandling ON / 2014-01-01 ~ 2023-12-31
- 顶层指标：S 1.66 / F 1.36 / TO .0947 / returns 8.45% / DD 5.11% / margin 17.86bp / 2Y 2.58 / sub 0.92 / ladder PASS / investability 1.40

## B.0 硬前置

- Failed RA = 0，Failed PPA = 0，`checks.fail = []`
- 名单内 PENDING = 0（`submit_verdict.pending_gate_names = []`）⇒ 通过 B.0 / B.0a

## B.1–B.2 逐年统计

| 年 | Sharpe | Returns | DD | Fitness | TO |
|---|---|---|---|---|---|
| 2014 | 2.01 | 9.65% | 2.15% | 1.77 | .1110 |
| 2015 | 1.29 | 6.92% | 1.94% | 0.96 | .1037 |
| 2016 | 1.26 | 7.25% | 4.11% | 0.96 | .1022 |
| 2017 | 0.61 | 2.40% | 2.01% | 0.27 | .0991 |
| 2018 | 1.29 | 6.95% | 3.30% | 0.96 | .0928 |
| 2019 | 2.64 | 11.25% | 1.48% | 2.50 | .0898 |
| 2020 | 1.45 | 8.07% | 3.15% | 1.17 | .0888 |
| 2021 | 1.00 | 5.37% | 3.71% | 0.66 | .0871 |
| 2022 | 2.51 | 14.51% | 2.77% | 2.70 | .0874 |
| 2023 | 2.71 | 12.17% | 1.80% | 2.67 | .0846 |

- 10/10 年 Sharpe 为正，最弱年 2017 = 0.61
- 近 3 年（2021–2023）均值 **2.07** ≥ 1.58 ✓；每年 > 0.3 ✓
- 衰减比 = 2.71 / 1.66 = **1.63** ≥ 0.30 ✓
- 近 3 年 CV = 0.763 / 2.073 = **0.37** < 0.60 ✓
- 全历史 Sharpe 单调性：无持续衰减（2021 低点后连续两年抬升）

## B.3 PnL 体检

- 换手 .0947 < 60% 且 margin 17.86bp > 3bp ⇒ 无「噪声拟合」标记
- 逐年最大回撤 4.11%（2016），全期 5.11% ⇒ 无单年极端回撤
- 逐季回撤抽样未做（`/alphas/{id}/pnl` 该 id 返回 records=[]，平台侧未落 PnL 序列）→ 软标记
- 逐股集中度无接口取数 → 未评估（软标记）

## B.4 相关性（本 id 实测）

- prod（POWER_POOL 池）**0.5451** < 0.7 ✓（源 prod_peek，checked_at 2026-11-13 12:34，age 0.31h）
- self **0.5450** < 0.7 ✓（池 17 / 全 OS 20，最近 xArzm3Mn 0.5450）
- 说明：12:5x 发起 refresh=True 终验时平台返回 `correlation_busy`（另一会话占单并发槽，holder=`corr:get_production_correlation(0mPvKgJ1)`），未取得新值；判闸用 0.31h 的预读值，距红线 0.155

## B.5 边际贡献

- `performance_comparison`：before S 1.73 → after S 2.37，**ΔSharpe +0.64**（分区 `EQUITY:DEU:1:POWER_POOL`）
- 同分区内为正向分散贡献；跨分区不可横比（常规 `:1` 分区另测）

## C 判定

**PASS** —— 近 3 年强度、逐年正收益、衰减比、CV、换手/margin 五项全部通过；软标记仅 2017 早年 0.61 与「逐季回撤/集中度未取数」。

软标记：`2017 sharpe 0.61（早年）`、`逐季回撤未抽样`、`逐股集中度未评估`、`prod 终验遇 busy（用 0.31h 预读值）`。
