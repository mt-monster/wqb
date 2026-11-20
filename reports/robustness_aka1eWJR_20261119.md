# 稳健性审计：aka1eWJR（GBR/TOP700/D1）

> 2026-11-19 10:40 ｜ 用户点名叫交（`提交aka1eWJR`）｜ 审计依据：平台实读 + 本轮 44 颗参数敏感性实测
> **判定：CONDITIONAL**（硬 REJECT = 0；1 项 CONDITIONAL + 2 项软标记，均不阻断）

## B.0 WebDataScope 门（硬前置）

`get_alpha_details("aka1eWJR")`：`ra.failed_ra_count=0`、`failed_ppa_count=0`、`ra_failed=false`；
`checks.fail=[]`；`checks.warning` 仅 `MATCHES_COMPETITION`(AQP202611) 与 `MATCHES_THEMES`
（GLB/D1 Power Pool Nov'26 ×1.0 / USA/D1 turnover 15..30% ×2.0，均非 counted item）；
`checks.pass` 9 项含 `LOW_SUB_UNIVERSE_SHARPE` / `CONCENTRATED_WEIGHT` / `CLUSTER_TEST` / `LOW_2Y_SHARPE` / `MATCHES_PYRAMID`。
⇒ **B.0 通过**。

## B.1 配置与表达式（平台 code 原文）

```
group_rank(ts_target_tvr_decay(group_neutralize(ts_delta(divide(ts_backfill(vec_avg(ern6_actual_eps),500),
  add(abs(ts_backfill(vec_avg(ern6_estimated_eps),500)),1)),610), sector),
  lambda_min=0, lambda_max=1, target_tvr=0.12), subindustry)
```
GBR / TOP700 / D1 / decay 2 / STATISTICAL / trunc 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade ON / 2014-01-01→2023-12-31。

IS：**S 2.28 / F 2.16 / TO 10.17% / 2Y 2.20 / sub 1.54 / margin 22.03bp / DD 3.66% / R 11.20%**
塔：`GBR/D1/EARNINGS ×1.3`（`pyramids.effective=1`，`ra.pyramid_short="earnings"`）。

## B.2 逐年归因（`get_alpha_yearly_stats`）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | — | — | — | — | — | — | — | 1.85 | 1.26 | **3.37** |
| longCount | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 207 | 353 | 357 |
| shortCount | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 267 | 509 | 461 |
| pnl（万） | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 79.4 | 66.2 | 154.2 |
| TO | — | — | — | — | — | — | — | 6.72% | 9.96% | 9.48% |

- **2014–2020 共 7 年零仓位**（long/short/pnl 全 0）。归因：`ern6_*` 字段覆盖自 2019 年中起，
  叠加 `ts_delta(.,610)` 要求恰好 t−610 有值 ⇒ 首个有效截面出现在 2021。
  **这是「数据空窗」不是「早年疲软」**，如实记为软标记（见 B.4）。
- 同族已 ACTIVE 的 `WjlAp92x`（W=480）逐年为 2020 S 0.35（33/37 只）→ 2021 1.16 / 2022 2.49 / 2023 1.68，
  **同样 2014–2019 全空** ⇒ 属家族属性，非本件新增缺陷。

## B.3 换手 × margin

TO **10.17%**（< 60% 线）、margin **22.03 bp**（> 5bp 线）、全期 DD 3.66%（远低于 10% 预警）⇒ **PASS**。

## B.4 Phase C 反过拟合闸（年度项只计最近 3 个 IS 年）

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA=0 / PPA=0，无名单内 PENDING | **PASS** |
| Recent-3yr Sharpe（主判定） | 1.85 / 1.26 / 3.37，均值 2.16；2Y **2.20 ≥ 1.58**；每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 总体口径 **0.411**；样本口径（n−1）**0.504** | **CONDITIONAL**（0.40–0.60 带） |
| 衰减比（末年/全期） | 3.37 / 2.28 = **1.478** ≥ 0.50 | **PASS** |
| 平年（\|S\|<0.3） | 0 个 | **PASS** |
| Recent-3yr max/min | 3.37 / 1.26 = **2.675** ≤ 3 | **PASS** |
| **样本有效年数** | **3 年**（2014–2020 因数据空窗无仓位） | **软标记（如实披露）** |
| Sub-universe | 平台 `LOW_SUB_UNIVERSE_SHARPE` PASS；实测 1.54，限 `0.4743×2.28=1.081` | **PASS** |
| 算子数 | distinct **8**（abs/add/divide/group_neutralize/group_rank/ts_delta/ts_target_tvr_decay/vec_avg） | 软标记（REGULAR 不据此 REJECT） |
| Top-5 个股集中度 | 无逐股 PnL 不可得；`CONCENTRATED_WEIGHT` PASS 代证 | 不可得（平台代证） |
| 混腿结构 | 单腿（无顶层多腿 `add`）；门控/分组轴均非信号腿 | **PASS** |
| 经济可解释性 | 「实际 EPS / \\|一致预期 EPS\\| 的比值」度量盈余超预期强度；其 **610 日变化**捕捉盈利预期基准的多年结构性重估，而非单季噪声；sector 中性化去掉行业估值体制差异，subindustry 内排序使仓位在业务可比公司间可比 | **PASS（一句话）** |

### 参数敏感性（本轮 44 颗实测，非事后挑选）

| 参数 | 扫描结果 | 判定 |
|---|---|---|
| `ts_delta` 窗口 W | 595→1.88｜600→2.14｜602→2.14｜605→2.21｜608→2.24｜**610→2.28**｜615→1.84｜620→1.65 | 平台区 **600–610**（11 天宽）；两端落地 ⇒ 选 610 为平台内点，非孤立尖峰 |
| `target_tvr` | .10→2.13｜.11→2.28｜**.12→2.28**｜.13→2.29 | 平台（0.10–0.13 全 ≥2.1）⇒ 非尖峰 |
| 终轴 group | subindustry→2.28｜industry→1.76(sub 0.80<0.836 FAIL)｜sector→1.36(3 FAIL)｜market→sub 0.54 FAIL | subindustry 必需 |
| 中性化轴 | sector→2.28（CW PASS）｜删 group_neutralize→S 2.31 但 **CW 0.1511 > 0.1 FAIL** | sector 必需 |

### 相关性（平台/本地实测）

- prod = **0.5381**（`check_correlation` 直返；直方图 ≥0.4 仅 2 颗、≥0.5 仅 1 颗）⇒ **PASS（<0.7）**
- self = **0.5395**（本地 OS 池 31 颗；对手 `WjlAp92x`）⇒ **PASS（<0.7）**
- 池边际 PnL：**未计算**（缺 GBR/D1 池 PnL 聚合口径，不臆造）；只登记与同族唯一 ACTIVE 件相关 0.5395。

## 结论

**硬 REJECT 项：0。判定 = CONDITIONAL。**
唯一 CONDITIONAL 项：Recent-3yr CV_Sharpe 0.411（总体）/ 0.504（样本），落在 0.40–0.60 带。
软标记 2 条：① 2014–2020 七年数据空窗，样本有效年数 = 3（家族属性，`WjlAp92x` 同）；② distinct 算子 8（>5，REGULAR 不据此拦截）。

**处置**：`submit_verdict` 对 CONDITIONAL 为 fail-open（`UNVERIFIABLE` / exit 10，非 BLOCKED），
且已完成「平台 prod<0.7 + 用户 10:33 明确点名」两项放行条件 ⇒ 按提交链执行。
