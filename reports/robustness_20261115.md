# 稳健性审计 · 2026-11-15

## `bla2k0Jq` — USA / D1 / OTHER（用户 13:46 明确点名提交）

**结论：CONDITIONAL（无 REJECT 硬标记，放行提交）** — 台账 `robustness_bla2k0Jq`（USA）已落。

### 0 基本面

| 项 | 值 |
|---|---|
| 表达式 | `tail(group_rank(ts_mean(vec_avg(opinion_score_delta), 22), industry), lower=0.1, upper=0.9, newval=0)` |
| 数据集 | `social_sent_score`（USA / VECTOR / category OTHER / coverage .6394 / 3 fields） |
| settings | USA, TOP3000, delay 1, decay 3, SUBINDUSTRY, truncation .08, 2014-01-01~2023-12-31 |
| 指标 | S 1.80 / F 1.25 / TO 14.44% / Ret 6.94% / DD 3.40% / margin 9.61bp / 2Y 1.63 / sub 0.90 / S÷2Y 1.104 |
| 算子数 | 4（tail, group_rank, ts_mean, vec_avg）≤ 8 ✓ |
| 信号语义 | 舆情/观点分数的变化经 22 日平滑后，在行业内做横截面排序；保留 10%–90% 分位、截去两端极值 → 押注「观点改善尚未被价格充分吸收」的行业内相对强弱。单数据源单腿，非混腿，Step 1.2 三问不适用。 |

### 1 B.0 WebDataScope failed-count 门

`get_alpha_details`：`failed_ra_count=0` / `failed_ppa_count=0` / `ra_failed=false` / `ppa_failed=false`；
`checks.fail=[]`（0）；`checks.pass` 8 项含 `LOW_SHARPE`、`LOW_FITNESS`、`LOW_2Y_SHARPE`、`LOW_SUB_UNIVERSE_SHARPE`、`CONCENTRATED_WEIGHT`、`MATCHES_PYRAMID`；
`checks.warning` 3 项 = `CLUSTER_TEST`(1.3 / 1.58)、`MATCHES_COMPETITION`、`MATCHES_THEMES`（后两项属评奖资格，非 RA 硬闸）。
⇒ Failed = 0 且无阻拦项，继续 B/C。`submit_verdict --alpha-id bla2k0Jq` = `UNVERIFIABLE_404`（exit 10，非 1/BLOCKED），Failed RA=0。

### 2 B.2 逐年归因（`get_alpha_yearly_stats`，IS）

| 年 | Sharpe | Returns | DD | margin(bp) | long/short | 备注 |
|---|---:|---:|---:|---:|---:|---|
| 2014–2017 | 0.00 | 0 | 0 | 0 | 0/0 | 数据集无持仓，PnL 起点 2018-05-09 |
| 2018 | 1.50 | 4.07% | 1.31% | 7.32 | 302/1518 | 半年有效 |
| 2019 | 2.43 | 8.60% | 2.02% | 15.4 | 577/2255 | |
| 2020 | 1.35 | 6.44% | 3.40% | 7.94 | 412/2437 | 全期最大回撤年 |
| 2021 | 2.03 | 8.56% | 1.71% | 11.6 | 438/2509 | 近 3 年 |
| 2022 | 2.49 | 9.29% | 1.42% | 12.8 | 439/2573 | 近 3 年最强 |
| 2023 | 0.61 | 2.05% | 2.40% | 2.88 | 440/2586 | 近 3 年最弱，衰减主因 |

`get_alpha_pnl`：累计 PnL 自 2018-05 单调上行至 3.94M（2023-09），2023Q4 走平至 3.87M，无 >2× 全期平均 DD 的季度；risk-neutralized 与 investability-constrained 两条 PnL 与主曲线同向且始终为正贡献。逐股分解不可得 ⇒ Top-5 集中度不判（skill 允许）。

### 3 B.4 相关性（`check_correlation(refresh=false)`，48h 缓存政策）

- prod **0.5138**，`from_cache=true` / `source=platform_sync` / `provisional=false` / `cached_at 2026-11-15T03:01:52`（10.8h，<48h）⇒ 按用户 11-14 明令**直接过闸、不回源**；直方图 0.5–0.6 桶 3 颗，非单钉，余量 .186。
- self **0.2094**（OS 池 141 + 排除 PPAC 5；top `KmP73gj` .2094）⇒ 远低于 .7。
- `all_passed=true`。

### 4 B.5 边际贡献 / 方案 D（`performance_comparison`，EQUITY:USA:1:POWER_POOL）

| | before | after | Δ |
|---|---:|---:|---:|
| Sharpe | 5.25 | 5.33 | **+0.08** |
| Fitness | 3.82 | 3.88 | **+0.06** |
| Returns | 6.62% | 6.63% | +0.0001 |
| Turnover | 9.14% | 9.56% | +0.0042 |
| Drawdown | 0.83% | 0.62% | −0.0021 |
| PnL | 6,600,622 | 6,610,569 | +9,947 |

硬闸（ΔSharpe<0 或 ΔFitness<0）**不触发**；配对判据需 ΔReturns<0 ∧ (ΔTO>0 ∨ ΔDD>0)，本件 ΔReturns **+0.0001** 为正 ⇒ **方案 D 放行**（与 11-15 清单一致）。

### 5 Phase C 反过拟合闸（逐项）

| 检查项 | 实测 | 判定 |
|---|---|---|
| failed-count | 0，无 PENDING | PASS |
| Recent-3yr 强度（主） | 均值 1.71 ≥ 1.58，三年皆 >0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.468（总体 std 口径） | CONDITIONAL 带 |
| 衰减比 | 0.61/1.80 = 0.339 | CONDITIONAL 带 |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.49/0.61 = 4.082 | CONDITIONAL 带 |
| 全历史早年 | 2014–2017 无数据（非疲软） | 软标记，**绝不 REJECT** |
| Sub-universe | `LOW_SUB_UNIVERSE_SHARPE` PASS（0.90） | PASS |
| 算子数 | 4（≤5） | PASS / 无软标记 |
| Margin @ turnover | 9.61bp @ 14.44% TVR | PASS |
| Top-5 集中度 | 逐股 PnL 不可得 | 不判 |
| 经济可解释性 | 一句话可写（见 §0） | PASS |

**无单个 REJECT 硬标记** ⇒ 不判死。3 项落 CONDITIONAL 标警带（集中在同一成因：2023 年 S 0.61 衰减），按如实口径 verdict = `CONDITIONAL`。
参照：11-14 `pwaQ0bx3`（CV .44 / max-min 3.42）判 PASS 并带软标记；11-13 `Wjl8Z20O`（连续弱年 + CV .604）判 CONDITIONAL。本件介于两者之间，取更保守的 CONDITIONAL。

### 6 处置

- `submit_verdict` 对 CONDITIONAL「不改判」，节点 Step 1 仅拦 `REJECT`；Step 1.5 认台账已有记录为「审计已跑过」。
- 用户 2026-11-15 13:46 明确点名「提交 bla2k0Jq」⇒ 不再重复索取确认，按提交链走预检 → POST → 核验。
- **软标记如实带入三段式 description**（Phase D 第 3 条），供一年后 OS 复盘时可读：2023 衰减、CV/衰减比/max-min 三项标警带、数据自 2018-05 起非十年全覆盖。
- 风险口径：prod 余量 .186（非贴线）、self .2094、方案 D 放行、平台 RA 全闸 PASS、S/2Y 1.104（项目规则 <1.3 属健康，非过生命周期）；CONDITIONAL 的唯一实质隐忧是最后一个 IS 年转弱，属**已知且已披露**的 OS 风险，不构成提交前否决。
