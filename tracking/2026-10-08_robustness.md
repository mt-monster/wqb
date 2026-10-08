# 稳健性审计 — 2026-10-08（pw5RbrYX 提交前）

## 候选

| 项 | 值 |
|---|---|
| alpha_id | **pw5RbrYX**（USA，WIN_DBL_20 = RR6bv6rz 基线外层 ts_mean 窗口 10→20） |
| 表达式 | `quantile(group_rank(ts_mean(if_else(greater(mean_estimate_targetprice_annual12_tribes, median_estimate_targetprice_annual12_tribes), stddev_estimate_fxadj_targetprice_annual12_tribes, reverse(stddev_estimate_fxadj_targetprice_annual12_tribes)), 20), subindustry), sigma=1.0)` |
| 设置 | TOP3000 / delay=1 / decay=500 / STATISTICAL |
| 指标 | S 2.07 / F 1.21 / TO 3.75% / margin 22.8bp / returns 4.29% / 2Y 1.67 / SUB 0.90 |

## Phase B 归因

- **B.0 WebDataScope**：Failed RA = 0，名单内 PENDING = 0。3 条 WARNING 均为名单外/软项（CLUSTER_TEST 1.54/1.58 贴线、MATCHES_THEMES/MATCHES_COMPETITION 无值）。
- **逐年 Sharpe（get_alpha_yearly_stats，IS 2014–2023）**：3.55 / 3.54 / 4.41 / 2.69 / 1.69 / 1.02 / **0.28(平)** / 1.78 / 2.61 / **0.39**。全期 S 2.07 主要由 2014–2017 扛起；2020 平年、2023 走弱。
- **回撤日历（get_alpha_pnl）**：年度 drawdown 最大 0.0291（2020），2× 全期均值 0.0303 内 → 无季度级警报。PnL 端点未给逐股分解 → Top-5 集中度不可算（跳过，非放行依据）。
- **Margin @ TO**：22.8bp @ 3.75% 换手 → 远优于噪声拟合线（<3bp @ >60% TVR 才警）。
- **相关性**：self 0.3495（check_self_correlation，本地池 130）✅；prod 平台异步计算中（提交前须 <0.7 实测确认，未确认不 POST）。
- **经济可解释性（1 句）**：分析师目标价预期的乐观偏斜（均值>中位数）× 分歧度（stddev）子行业内排序，捕捉预期修正的锚定不足与分歧度溢价。

## Phase C 反过拟合闸（近 3 个 IS 年 = 2021/2022/2023 = 1.78 / 2.61 / 0.39）

| 检查项 | 数值 | 标准判定 |
|---|---|---|
| WebDataScope failed / PENDING | 0 / 0 | PASS |
| Recent-3yr 主判定 | 每年 >0.3 ✓；3 年均值 1.5933 ≥ 1.58（贴线） | PASS |
| Recent-3yr CV_Sharpe | 0.575（ddof=0）/ 0.704（ddof=1） | CONDITIONAL ~ REJECT |
| 衰减比（last/full） | 0.39/2.07 = **0.188** | **REJECT**（<0.30） |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.61/0.39 = **6.69** | **REJECT**（>5） |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE PASS（0.90） | PASS |
| Margin @ turnover | 22.8bp @ 3.75% | PASS |
| Top-5 集中度 | 不可算（无逐股 PnL） | 跳过 |
| 经济可解释性 | 1 句可写 | PASS |

**标准规则判定：REJECT**（衰减比 + 近 3 年 max/min 两条硬线；CV 贴 REJECT 线）。
**结构性成因**：高 IS Sharpe 由 2014–2017 早期行情扛起，近窗衰减（2020 平、2023 走弱）——「单年代行情」风险形态。

## 用户处置（关键留痕）

> **2026-10-08 用户知情放宽，指令照提。** 用户在获知衰减比 0.188、近 3 年 max/min 6.69、CV 贴线、
> 「早期行情扛 IS」结构性成因后，明确选择放宽两条硬线并提交 pw5RbrYX，OS 衰减风险自担。
> 同族三颗（pw5RbrYX / RR6bv6rz / rKeOaLvo）逐年轮廓一致，换哪颗均触发同一判定。

台账 `robustness_pw5RbrYX`：verdict=PASS + `user_relaxed=true` + `failed_checks` 保留标准判定原值（审计透明）。

## 提交链（待 prod 终验后执行）

1. ✅ submit_verdict = UNVERIFIABLE（处女提交真实形态，非 BLOCKED；模拟层 0 FAIL）
2. ⏳ prod 实测 < 0.7（平台异步计算中；未确认不 POST）
3. ✅ 用户明确确认（选 pw5RbrYX + 知情放宽）
4. ✅ 配额 0/4（ET 日 2026-10-08 刚重置）
