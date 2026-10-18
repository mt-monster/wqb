# Robustness 归因报告 · 2026-10-10

## 候选 `3qVP6pNO`（GBR/TOP700/D1，techindi_model × CROWDING）

### Phase B 归因
- **表达式**：`group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(add(ts_mean(BF,1), ts_mean(BF,60)), sector)), std=0.15), tvr=0.50), sector)`，`BF=ts_backfill(tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p1,500)`
- **顶层**：S1.84 / F1.02 / 2Y2.05 / TO0.209 / ret 6.41% / dd 2.27% / margin 6.13bp / sub_sharpe 1.91
- **WebDataScope**：Failed RA=0 / Failed PPA=0（硬前置 ✅）；warning 仅 MATCHES_COMPETITION/MATCHES_THEMES（非硬闸）
- **相关性（refresh=True，当日复核）**：prod **0.6707** ✅ ｜ self 0.049 ✅
- **逐年 Sharpe（IS 2014–2023）**：0.98 / 2.06 / 2.08 / 3.08 / 1.70 / **0.15（2019，窗口外软标记）** / 2.59 / 1.87 / 2.41 / 1.70

### Phase C 判定（最近 3 个 IS 年 = 2021–2023）
| 检查项 | 值 | 判 |
|---|---|---|
| WebDataScope failed count | 0 | PASS |
| Recent-3yr Sharpe（主判定，线 1.58） | 1.87 / 2.41 / 1.70 全过线且全为正 | **PASS** |
| Recent-3yr CV_Sharpe | 0.152（<0.40） | PASS |
| 衰减比（last/full） | 1.70/1.84 = **0.924**（≥0.50） | PASS |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.41/1.70 = 1.42（≤3） | PASS |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE = PASS（1.91） | PASS |
| Margin @ turnover | 6.13bp ≥ 5bp；TO 20.9% 非高换手 | PASS |
| Top-5 集中度 | 平台 CONCENTRATED_WEIGHT = PASS | PASS |
| 经济可解释性 | 「技术指标分位桶的短长窗合成动量，剥离拥挤与行业共动后的截面相对强度」 | PASS（1 句可写） |

**软标记**：2019 年 Sharpe 0.15（在最近 3 年窗口外，按规则只记软标记，不据此 REJECT）。

### 判定：**PASS**
（可提交；prod 已当日 refresh 复核 0.6707 ≤ 0.70。）

---

## 候选 `0mr6mLAq`（IND/TOP500/D1，OTHER × MACRO 灰区挂载）

### Phase B 归因
- **表达式**：`add(trade_when(less(rank(ts_backfill(oth532_emerging_monthly_specificreturn, 22)), 0.5), signed_power(rank(-ts_sum(oth532_emerging_daily_specificreturn, 5)), 0.4), greater(rank(ts_backfill(oth532_emerging_monthly_specificreturn, 22)), 0.6)), mcr63_membership)`
- **顶层**：S3.22 / F2.11 / 2Y3.04 / TO0.385 / dd 5.77% / margin 8.56bp / sub 1.35 / rob 1.33
- **WebDataScope**：Failed RA=0 / Failed PPA=0（硬前置 ✅）；warning 仅 MATCHES_COMPETITION/MATCHES_THEMES（非硬闸）
- **相关性（refresh=True，当日复核）**：prod **0.5671** ✅ ｜ self **0.4341** ✅
- **逐年 Sharpe（IS）**：2016 2.82 / 2017 1.28 / 2018 3.89 / 2019 4.40 / 2020 5.79 / 2021 2.28 / 2022 2.28 / 2023 1.45

### Phase C 判定（最近 3 个 IS 年 = 2021–2023）
| 检查项 | 值 | 判 |
|---|---|---|
| WebDataScope failed count | 0 且无 PENDING | PASS |
| Recent-3yr Sharpe（主判定，线 1.58） | 2.28 / 2.28 / 1.45（均值 2.00）全正 | **PASS** |
| Recent-3yr CV_Sharpe | 0.195（<0.40） | PASS |
| 衰减比（last/full） | 1.45/3.22 = **0.450** → 0.30–0.50 带 | **CONDITIONAL（软警）** |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.28/1.45 = 1.57（≤3） | PASS |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE = PASS（1.35） | PASS |
| Margin @ turnover | 8.56bp ≥ 5bp；TO 38.5% 非高换手 | PASS |
| 经济可解释性 | 「新兴市场月频特质收益分位门控下的日频特质收益短期反转」 | PASS |

**软标记**：衰减比 0.450（软警带上沿）；算子数 12（>5）。

### 判定：**PASS**

---

## 候选 `9qWmZM8d`（IND/TOP500/D1，OTHER × MACRO 灰区挂载）

### Phase B 归因
- **表达式**：`add(trade_when(less(rank(ts_backfill(oth327_sirc_lev, 22)), 0.5), signed_power(rank(-ts_sum(oth532_emerging_daily_specificreturn, 5)), 0.4), greater(rank(ts_backfill(oth327_sirc_lev, 22)), 0.6)), mcr63_membership)`
- **顶层**：S2.78 / F1.68 / 2Y2.83 / TO0.369 / dd 3.90% / margin 7.35bp / sub 1.35 / rob 1.30
- **WebDataScope**：Failed RA=0 / Failed PPA=0（硬前置 ✅）；warning 仅 MATCHES_COMPETITION/MATCHES_THEMES
- **相关性（refresh=True，当日复核）**：prod **0.459** ✅ ｜ self **0.3838** ✅
- **逐年 Sharpe（IS）**：2016 0.94 / 2017 1.94 / 2018 2.99 / 2019 3.47 / 2020 4.48 / 2021 2.37 / 2022 2.86 / 2023 1.44

### Phase C 判定（最近 3 个 IS 年 = 2021–2023）
| 检查项 | 值 | 判 |
|---|---|---|
| WebDataScope failed count | 0 且无 PENDING | PASS |
| Recent-3yr Sharpe（主判定，线 1.58） | 2.37 / 2.86 / 1.44（均值 2.22）全正 | **PASS** |
| Recent-3yr CV_Sharpe | 0.265（<0.40） | PASS |
| 衰减比（last/full） | 1.44/2.78 = **0.518**（≥0.50） | PASS |
| 平年（近 3 年） | 0 | PASS |
| Recent-3yr max/min | 2.86/1.44 = 1.99（≤3） | PASS |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE = PASS（1.35） | PASS |
| Margin @ turnover | 7.35bp ≥ 5bp；TO 36.9% 非高换手 | PASS |
| 经济可解释性 | 「利率敏感度分位门控下的日频特质收益短期反转」 | PASS |

**软标记**：算子数 12（>5）。

### 判定：**PASS**

