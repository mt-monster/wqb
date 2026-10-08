# 稳健性审计 — KPrGMXZ8（USA / D1 / TOP3000）2026-10-07

> 流程：brain-alpha-robustness Phase B→C→D。checked_at = 2026-10-07T12:36:58+08:00

## 0. 候选档案（get_alpha_details）

- code: `group_rank(ts_zscore(mean_estimate_targetprice_annual12_tribes,175),subindustry)`
- settings: USA / TOP3000 / EQUITY / delay 1 / **decay 500** / STATISTICAL / truncation 0.08 /
  pasteurization ON / nanHandling ON / maxTrade OFF / maxPosition OFF（IS 2014-01-01 → 2023-12-31）
- metrics: S 1.95 / F 1.26 / 2Y 1.70 / SUB 1.06 / TO 0.059 / returns 0.052 /
  margin 0.001764（17.64bp）/ DD 0.0769 / L 1664 / S 1462 / pnl 5,194,131 /
  investability S 2.14 / F 1.43
- status: UNSUBMITTED / stage IS

## B.0 WebDataScope 资格门（硬前置）

- Failed RA = 0、Failed PPA = 0（`submit_verdict` 权威口径，`wqb.config.compute_webdata_failed_counts` 单源）
- **名单内 PENDING = 0**：`checks.pending` 6 项（SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION /
  REGULAR_SUBMISSION / POWER_POOL_CORRELATION / MATCHES_THEMES）与代码单源名单
  `RA_CHECK_NAMES`(18) / `PPA_CHECK_NAMES`(7) 逐一比对，**均不在名单内** ⇒ 不计失败、也不构成「待复查」
- warning 3 项（CLUSTER_TEST 0.84 / MATCHES_COMPETITION / MATCHES_THEMES）不在 RA 名单 ⇒ 不计失败
  （且 CLUSTER_TEST 本就只进 warning，不进 `ra_failed_checks`）
- **B.0 → PASS**

## B.0a 体检硬门（field_inspect_gate USA/analyst_consensus）

- `enforced（降级包 coverage-only）：校验 1/1 条，违规 0 条` —— 规则 1（低覆盖须 ts_backfill）实查通过
- 规则 2/3/5/6（偏度/厚尾/稀疏事件/窗口频率）因降级包缺 skewness/kurtosis/distribution_shape/frequency 未生效，如实记录；
  表达式外层自带 `group_rank`，形态上天然满足 rank 类规则
- **B.0a → PASS**（附注：包为降级包）

## B.1–B.5 归因

### 逐年（get_alpha_yearly_stats，2014–2023）

| 年 | Sharpe | returns | DD | 年 | Sharpe | returns | DD |
|---|---|---|---|---|---|---|---|
| 2014 | 3.65 | 6.22% | 0.84% | 2019 | 1.73 | 4.07% | 1.39% |
| 2015 | 4.76 | 9.64% | 0.84% | 2020 | **−1.17** | −3.93% | 6.78% |
| 2016 | 2.82 | 5.41% | 1.29% | 2021 | 2.22 | 9.08% | 2.76% |
| 2017 | 2.38 | 4.72% | 0.95% | 2022 | 2.50 | 8.06% | 2.06% |
| 2018 | 2.51 | 5.85% | 0.99% | 2023 | 0.69 | 1.90% | 1.94% |

- 近 3 IS 年（2021/2022/2023）：**2.22 / 2.50 / 0.69**；10 年 9 正 1 负（2020 −1.17）
- 衰减比 = 0.69 / 1.95 = **0.35**；Recent-3yr CV_Sharpe = 0.795/1.803 = **0.44**；max/min = 2.50/0.69 = **3.62**

### PnL（get_alpha_pnl）

- 2,494 个交易日聚合序列（降采样展示），期末累计 5,166,184（investability 口径 5,528,179）
- 主回撤期：2020-02（3,658,827）→ 2020-12-31（3,251,578）≈ −407k，与 2020 单年 −363,594 一致；2021 起修复
- 逐股 PnL 不可得 ⇒ Top-5 集中度不可计算；持仓 3,126 只（L 1664 + S 1462），结构上极度分散

### 相关性（check_correlation，refresh=True 提交前实测）

- **prod max 0.6540 PASS**（红线 0.7，余量 0.046）；直方图 [0.5,0.6)=403、[0.6,0.7)=3 ⇒ 顶部孤岛形态，非拥挤带
- **self max 0.4281 PASS**（self 池 130 / full_os 133，Top1 `gdx066J` 0.428）
- all_passed = true

### 池贡献（performance_comparison，partition EQUITY:USA:1:POWER_POOL）

- before：S 4.28 / F 2.91 / pnl 5,743,133 / returns 5.76% / TO 9.33%
- after：S **4.37** / F **2.94** / pnl 5,627,744 / returns 5.64% / TO 8.64%
- **边际贡献为正**（S +0.09、F +0.03）⇒ 无软标记
- 审计范围说明：stats.before/after 全量、yearlyStats 逐年行已读取；日频 PnL 数组（同质累计序列）读取头尾抽验，未逐行通读

## Phase C 反过拟合闸

| 检查项 | 实测 | 档位 |
|---|---|---|
| WebDataScope failed count | Failed RA 0 / PPA 0，名单内 PENDING 0 | **PASS** |
| Recent-3yr Sharpe（主判定） | 平台 2Y 1.70 ≥ 1.58；近 3 年 2.22/2.50/0.69 均 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 0.44 | CONDITIONAL·软 |
| 衰减比 | 0.35 | CONDITIONAL·软 |
| 平年（近 3 年） | 0 | **PASS** |
| Recent-3yr max/min Sharpe | 3.62 | CONDITIONAL·软 |
| 全历史早年疲软 | 早年强（2014-15 S 3.65/4.76）；2020 单年 −1.17、2023 走弱 | 信息性（绝不 REJECT） |
| Sub-universe | LOW_SUB_UNIVERSE_SHARPE = PASS（SUB 1.06，比值 0.544 ≥ 0.431 线） | **PASS** |
| 算子数 | 2（group_rank + ts_zscore）≤ 5 | **PASS** |
| Margin @ turnover | 17.64bp @ TO 5.9%（≥ 5bp） | **PASS** |
| Top-5 集中度 | 不可计算（无逐股 PnL）；3,126 只持仓 | 结构无集中风险，记录不可得 |
| 经济可解释性 | 分析师 12 个月一致目标价的修正强度（175d z-score）在 subindustry 内取相对值——市场对分析师预期修正反应不足 | **PASS** |
| 参数稳健（附加证据） | 同表达式 decay 200→500 单调改善，d450–d500 平台期（S 1.94–1.95 / prod 0.654–0.659）⇒ 非刀锋参数点 | 正面 |

## 判定：**PASS（带 CONDITIONAL 软标记）**

- `failed_checks`: []（无任何 REJECT 档）
- `soft_flags`:
  - recent3yr_cv_sharpe_0.44_conditional
  - decay_ratio_0.35_conditional
  - recent3yr_maxmin_3.6_conditional
  - weak_2023_S0.69
  - single_negative_year_2020_-1.17
  - inspect_pack_degraded_rules_2_3_5_6_inactive
  - top5_concentration_uncomputable
- 软标记来源集中在「2023 走弱 + 2020 单年亏损」的近年形态；主判定（近 3 年聚合 2Y 1.70 与逐年全正）、
  sub-universe、prod/self 实测、池贡献边际均为正面。按 Phase D.3，软标记将带入提交 description。
