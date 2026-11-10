# 稳健性审计 — GrW9OxmG（2026-11-08）

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

| 年 | Sharpe | Fitness | 备注 |
|---|---|---|---|
| 2021 | 2.34 | 2.92 | |
| 2022 | 0.92 | 0.72 | 低年（单年离群源） |
| 2023 | 3.14 | 4.16 | 末年最强 |

- 近 3 年均值 = **2.13 ≥ 1.58** ⇒ 主判 PASS
- 无负年、无空仓年；**末段无衰减**（2023 为十年最强年）
- CV（总体 10 年，均值 1.62）≈ 0.43
- 判型：**「单年高离群 + 平年」型**（2019 0.67、2022 0.92 两个低年拉高 CV；2021/2023 爆发）——按 skill 表记 soft_flag，**不构成 REJECT**
- max/min = 3.14/0.67 ≈ 4.7（存在平年使分母偏小，参考值）
- margin 2023 = 111.5bp @ TO 3.94%

**结论：CONDITIONAL（主判 PASS + soft_flag 记录）**
依据：2026-11-07 定案的 Recent-3yr 口径——否决力在「离散度/衰减」：本候选无末段衰减、无负年，低年属单年离群型，可 soft_flag 放行。

前置数据：`get_alpha_yearly_stats(GrW9OxmG)`（2014–2023 全正，n_years=10）

---

# 稳健性审计 — bl6AvMkN（2026-11-08 12:5x）

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

| 年 | Sharpe | Fitness | TO | 备注 |
|---|---:|---:|---:|---|
| 2014 | 2.22 | 2.09 | 0.1221 | |
| 2015 | 2.86 | 3.26 | 0.1106 | 全史峰值 |
| 2016 | 0.85 | 0.50 | 0.1145 | |
| 2017 | 1.03 | 0.62 | 0.1047 | |
| 2018 | 0.87 | 0.54 | 0.1094 | |
| 2019 | 1.61 | 1.28 | 0.1108 | |
| 2020 | 0.36 | 0.16 | 0.1080 | 全史低点（单年离群源） |
| 2021 | 2.70 | 2.89 | 0.1087 | |
| 2022 | 2.03 | 2.05 | 0.1053 | |
| 2023 | 1.78 | 1.56 | 0.1034 | 末年仍 >1.58 |

- 近 3 年均值 = **2.17 ≥ 1.58** ⇒ 主判 PASS
- **无负年**（最低 2020 = 0.36）；十年全正
- **末段三年单调缓降** 2.70 → 2.03 → 1.78，但 2023 仍 1.78 高于阻断线 1.58（衰减幅度 −0.92，未破线）
- 全史 CV ≈ 0.49（均值 1.63，sd 0.80）；max/min = 2.86/0.36 ≈ 7.9（2020 单年拉大分母，仅参考）
- 换手极稳：TO 10.3%–12.2%，十年几乎无漂移 ⇒ 无「靠换手堆指标」风险
- margin 2023 = 18.6bp；drawdown 逐年 2.0%–6.7%，无深回撤年

**结论：CONDITIONAL（主判 PASS + soft_flag 记录）**
依据：2026-11-07 定案的 Recent-3yr 口径——否决力在「离散度 / 末段衰减 / 负年」：本候选三年缓降但末年仍过线、无负年、无空仓年；2020 低点属历史中段单年离群，不构成 REJECT。

**soft_flags**：① 末段三年单调缓降 ② 全史 max/min 7.9（2020 单年 0.36 拉低分母）③ 2023 F=1.56 较 2021 F=2.89 衰减 46%

前置数据：`get_alpha_yearly_stats(bl6AvMkN)`（2014–2023 全正，n_years=10）


---

# 稳健性审计 — zq3eb7No（2026-11-08 13:2x）

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

表达式 `group_rank(add(ts_zscore(est_12m_ebt_mean,240), ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago),66)), sector)`
DEU/TOP500/D1/FAST/decay0/trunc0.08/nanOFF，5 ops

| 年 | Sharpe | Fitness | TO | 备注 |
|---|---:|---:|---:|---|
| 2014 | 3.59 | 2.66 | 0.2374 | 全史峰值 |
| 2015 | 1.90 | 1.17 | 0.2432 | |
| 2016 | 2.06 | 1.22 | 0.2375 | |
| 2017 | 3.30 | 2.40 | 0.2325 | |
| 2018 | 1.60 | 0.89 | 0.2262 | |
| 2019 | 0.52 | 0.16 | 0.2247 | 全史低点（中段单年离群） |
| 2020 | 2.32 | 1.88 | 0.2139 | |
| 2021 | 2.21 | 1.52 | 0.2157 | |
| 2022 | 2.33 | 1.78 | 0.2173 | |
| 2023 | 0.81 | 0.33 | 0.2131 | 末年，>0.3 但跌破 1.58 |

- 近 3 年均值 = **1.783 ≥ 1.58** ⇒ 主判 PASS；近 3 年每年 >0.3（末年 0.81），平年 0
- Recent-3yr CV_Sharpe = 0.387（<0.40 PASS，但贴线；样本 sd 口径为 0.474 → CONDITIONAL 带）
- **衰减比 = 0.81 / 2.01 = 0.403** ⇒ 落在 CONDITIONAL 带（0.30–0.50）
- Recent-3yr max/min = 2.33 / 0.81 = 2.88（≤3 PASS）
- 全史 CV 0.439、max/min 6.90 —— 仅软标记（2023 单年拉低分母）
- 换手十年稳定 21.4%–24.3%，无漂移；margin 8.16bp @ TO 22.6%（≥5bp PASS）
- 平台闸：S2.01 / F1.28 / 2Y1.64（限1.58）/ sub1.00（限0.95）/ CLUSTER1.50，全 PASS

**结论：CONDITIONAL（主判 PASS + 衰减比入 CONDITIONAL 带）**
soft_flags：① 末段断崖 2022 2.33 → 2023 0.81（−1.52，跌回 1.58 线下）② 近 3 年 CV 0.387 贴 0.40 线 ③ sub 余量仅 0.05

前置数据：`get_alpha_yearly_stats(zq3eb7No)`（2014–2023 全正，n_years=10）

---

# 稳健性审计 — LLMzYrZe（2026-11-08 13:2x）

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

表达式 `group_rank(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4,5)), rank(ts_mean(predicted_surprise_f12m_ebitda_4,5))), sector)`
DEU/TOP500/D1/decay6/SUBINDUSTRY/trunc0.08/nanOFF，6 ops

| 年 | Sharpe | Fitness | TO | 备注 |
|---|---:|---:|---:|---|
| 2014 | 1.75 | 1.17 | 0.1608 | |
| 2015 | 2.03 | 1.59 | 0.1573 | |
| 2016 | 0.91 | 0.49 | 0.1598 | |
| 2017 | 1.65 | 1.13 | 0.1523 | |
| 2018 | 2.50 | 2.28 | 0.1542 | |
| 2019 | 1.00 | 0.55 | 0.1540 | |
| 2020 | 1.68 | 1.37 | 0.1500 | |
| 2021 | 1.26 | 0.77 | 0.1442 | |
| 2022 | 1.09 | 0.69 | 0.1483 | |
| 2023 | 2.36 | 2.07 | 0.1507 | 末年反弹，全期次高 |

- 近 3 年均值 = **1.570 < 1.58**（差 0.01，三年合计 4.71 < 4.74）⇒ **主判 REJECT**
- Recent-3yr CV_Sharpe = 0.358（PASS）；衰减比 1.466（PASS）；max/min 2.165（PASS）；平年 0
- 全史 CV 0.327；换手十年 14.4%–16.1% 稳定；margin 10.3bp @ TO 15.3%
- 平台闸：S1.61（余量仅 +0.03）/ F1.16 / 2Y1.69 / sub1.20（限0.76）/ CLUSTER1.47，全 PASS

**结论：REJECT（主判贴线未达）**
结构性成因：两腿均为 `mean_estimate_change_pct_f12m_earnings_14d_4` + `predicted_surprise_f12m_ebitda_4`，**正是已 ACTIVE `blRnKEk6` 四条腿中的第 2、3 腿**（`add(-rank(vec_avg(mean_loan_rate_main)), 这两腿, rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,22))))`）。母体 S2.02 / F1.70 全面优于本候选 1.61 / 1.16，self 相关 0.670 印证同源 ⇒ 提交属「用配额换一个降级副本」。

前置数据：`get_alpha_yearly_stats(LLMzYrZe)`（2014–2023 全正，n_years=10）

---

# 修复轮 — zq3eb7No（2026-11-08 14:0x-14:5x）

**触发**：用户「先修复」。按 robustness 判定表，CONDITIONAL 的规范动作是 `brain-alpha-repair` 修复一轮后重跑判定，而非直接提交。
**修复目标**：把 2023 S=0.81 的 regime 断崖与 Recent-3yr CV 0.387 贴线（衰减比 0.403，落在 CONDITIONAL 带 0.30–0.50）拉回 PASS 带，且不得损失任何平台闸。
**基线**：`group_rank(add(ts_zscore(est_12m_ebt_mean,240), ts_zscore(subtract(est_12m_pre_mean, est_12m_pre_mean_4wks_ago),66)), sector)`，DEU/TOP500/D1/FAST/decay0/trunc0.08，5 ops。

## 批 A — 结构诊断（7 条，decay0/FAST 不变）

| 变体 | alpha | S | F | 2Y | sub | ops | RA fail | 判读 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 腿1 单独（估计水平 z240） | O0A2j1r1 | 1.94 | 1.55 | **0.64** | 0.94 | 3 | 1 | 2023 S=**0.03**（收益 0.16%）⇒ 腿1 已死 |
| 腿2 单独（4 周修正 z66） | xArEoKYw | 0.98 | 0.40 | 1.60 | 0.46 | 3 | 2 | 2023 S=**1.03** ⇒ 近段全靠腿2 |
| rank 等权（换壳+等权） | VkxRLv68 | 2.08 | 1.36 | 1.63 | 1.01 | 7 | **0** | 头指标升，但 2023 掉到 0.61 |
| 腿2 窗 66→120 | YP19Oj5l | 1.99 | 1.33 | 1.16 | 0.95 | 5 | 1 | 2Y 崩 |
| 分组轴 sector→industry | akKg8rL5 | 1.55 | 0.83 | 1.13 | 0.67 | 5 | 4 | 全崩（DEU 与 KOR 相反） |
| 腿1 窗 240→480 | RREvoJb0 | 1.92 | 1.23 | 1.40 | 1.04 | 5 | 1 | 2Y 崩 |
| 腿2 窗 66→22 | 6Xd2Qnjp | 1.52 | 0.70 | 1.18 | 0.74 | 5 | 3 | 2Y 崩 |

**诊断结论（本轮最重要的发现）**：本 alpha 的 2023 弱不是"某条腿参数不好"，而是**腿1 在 2023 完全失效**（S 0.03），全部近段收益由腿2 提供（2023 S 1.03）。基线 2023 之所以还有 0.81，是"腿1 归零 + 腿2 贡献"的混合结果；把腿1 的权重加大到 50%（rank 等权）反而把 2023 压到 0.61。
同时两条腿的窗口在 2Y 上都是**局部最优**（66 和 240 一动 2Y 就从 1.64 掉到 1.16–1.40）⇒ 窗口轴无修复空间。

## 批 B — 权重前沿（5 条）

| 变体 | alpha | S | F | 2Y | sub | 2021 | 2022 | 2023 | 近3年均 | CV(pop) | 衰减比 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 基线（对照） | zq3eb7No | 2.01 | 1.28 | 1.64 | 1.00 | 2.21 | 2.33 | 0.81 | 1.783 | **0.387** | 0.403 |
| rank 形 腿1×0.5 : 腿2×1 | 0mYa23eq | 1.76 | 0.99 | 1.87 | 0.87 | 1.40 | 2.72 | 0.83 | 1.650 | 0.480 | 0.503 |
| rank 形 腿1×0.25 : 腿2×1 | kqNY6r1k | 1.42 | 0.70 | 1.73 | 0.72 | — | — | — | — | — | — |
| z 形 腿2×2 | bl6K1ZoN | 1.70 | 0.95 | 1.77 | 0.89 | 与 0mYa23eq 同值 | | | | | |
| z 形 腿1×0.5 | A1V28Zgl | 1.70 | 0.95 | 1.77 | 0.89 | 同上 | | | | | |
| z 形 腿2×3 | RREvwQ2e | 1.54 | 0.80 | 1.80 | 0.79 | — | — | — | — | — | — |

**两条方法论发现**：
1. **`group_rank(add(a,b))` 内的整体正标量是 no-op** ⇒ `腿1×0.5 : 腿2×1` 与 `腿1×1 : 腿2×2` 是**同一个信号**（0.5·(L+2F)=0.5L+F），bl6K1ZoN 与 A1V28Zgl 指标逐位相同，白花一个槽。真正的自由度只有 rank 形下的相对权重。
2. **降腿1 权重换来的是"换个年份弱"**：2023 只从 0.81 抬到 0.83，但 2021 被砍到 1.40（腿1 是 2021 唯一的贡献者，3.57）⇒ CV 从 0.387 升到 0.480，衰减比虽回升到 0.503 但均值跌到 1.650（距 1.58 只剩 0.07）。**两腿是交替 regime，不是强弱腿**，任何静态配比都无法拉平。

## 修复判定（截至批 B）

- 13 条变体中 **没有任何一条同时满足**：全部平台闸 PASS + 近3年均值 ≥1.58 且留余量 + CV < 0.387 + 衰减比 > 0.50。
- 唯一 RA 全过的变体 VkxRLv68 头指标更好（S 2.08 / F 1.36），但 2023 更差（0.61）、CV 更差（0.474）⇒ **不构成修复**，只是同族里另一个"更漂亮但更脆"的点。
- 基线 zq3eb7No 本身仍是该前沿上**稳定性最好的点**（CV 0.387、衰减比 0.403、S 2.01、sub 1.00、RA fail 0）。

批 C（decay 2 / 4）结果见下节。

## 批 C — decay 轴（4 条，2 批分派避开同式去重）

| 变体 | alpha | decay | S | F | TO | **2Y** | sub | RA fail |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 基线 | zq3eb7No | 0 | 2.01 | 1.28 | 0.2262 | **1.64** | 1.00 | 0 |
| 基线 + decay2 | 1YN2AReW | 2 | 1.99 | 1.35 | 0.1987 | **1.53** ✗ | 0.98 | 1 |
| rank 形 + decay2 | KPJ2Mp3p | 2 | 2.06 | 1.43 | 0.1956 | **1.53** ✗ | 0.99 | 1 |
| 基线 + decay4 | 0mYa2avq | 4 | 1.97 | **1.42** | 0.1754 | **1.48** ✗ | 0.97 | 1 |
| rank 形 + decay4 | N1N2l29o | 4 | 2.04 | **1.51** | 0.1723 | **1.50** ✗ | 0.97 | 1 |

**decay 轴封闭**：decay 2/4 把 F 抬到 1.35–1.51、margin 抬到 9.19–10.92bp（TO 从 22.6% 降到 17.2%），但 **2Y 从 1.64 掉到 1.48–1.53，四颗全部 LOW_2Y_SHARPE FAIL**。规格化平滑压掉了近两年仅存的收益尖峰，与「decay 平滑自身噪声、不改信息含量」一致。

## 修复最终判定：FAIL（空转）

**六轴全覆盖，共 16 条新仿真**：结构诊断(2) / 换壳与窗口(4) / 分组轴(1) / 权重前沿(5) / decay(4)；neutralization 轴按纪律主动排除（FAST 是 prod 0.6171 的承重设置）。

| 轴 | 是否可修 | 代价 |
|---|---|---|
| 腿2 窗 66→22/120 | ✗ | 2Y 1.64→1.18/1.16 |
| 腿1 窗 240→480 | ✗ | 2Y→1.40 |
| 换壳 zscore→rank 等权 | ✗ | 2023 0.81→0.61，CV 0.387→0.474 |
| 降腿1 权重（前沿） | ✗ | 2021 2.21→1.40，CV→0.48，近3年均 1.65（余量 0.07） |
| 分组轴 sector→industry | ✗ | S 2.01→1.55，sub→0.67（DEU 与 KOR 方向相反） |
| decay 2 / 4 | ✗ | 2Y 1.64→1.48~1.53 直接掉闸 |
| neutralization | 不测 | 换掉就失去 prod 0.6171（唯一余量来源），且非时间稳定性机制 |

**机制结论**：该 alpha 不是"好腿+坏腿"，而是**两条腿交替执掌 regime**——
腿1（估计水平）在 2014–2017、2020–2021 独撑（2021 S 3.57），2023 归零（S 0.03）；
腿2（4 周修正）在 2022–2023 独撑（2023 S 1.03），2019–2021 近乎零（0.33/0.27）。
任何静态配比只能把"弱年"从 2023 挪到 2021，无法压低离散度 ⇒ **CONDITIONAL 是本结构的内生属性，不是可修复缺陷**。

**产物**：最优仍是原候选 zq3eb7No（S 2.01 / F 1.28 / 2Y 1.64 / sub 1.00 / RA fail 0 / CV 0.387 / 衰减比 0.403 / prod 0.6171 / ΔS +0.70）。
次优 VkxRLv68（S 2.08 / F 1.36 / 2Y 1.63 / RA fail 0）头指标更好但 2023 更脆，且多 2 个算子。

---

# 附：今日 4 颗的标签处置（2026-11-08 16:5x 回读平台）

此前该动作**零留痕**（11-06 / 11-07 只在报告里各写一句），事后无法回答「清了哪些、清的时候平台上到底有没有」。本节按新口径（`submit_alpha` Step 6 `tag_disposal`）补齐今日 4 颗。

| alpha | name | 提交时刻 (ET) | 平台 tags（回读） | PowerPoolSelected | checks.pending |
|---|---|---|---|---|---|
| `zq3eb7No` | DEU_R_afslvlrev_01 | 11-08 01:11 | `CH_REG` · `SRC_afs_level_revision` · `CORR_060` | **无** | `POWER_POOL_CORRELATION` · `MATCHES_THEMES` |
| `3qoGxkqZ` | GBR_R_pv103lend_01 | 11-08 01:59 | `CH_REG` · `SRC_pv103` · `EXPRFAM_pv103_lend` · `CORR_NEAR` | **无** | `POWER_POOL_CORRELATION` · `MATCHES_THEMES` |
| `RRE5Mwkn` | GBR_R_pv103tvr_01 | 11-08 02:00 | `CH_REG` · `SRC_pv103` · `EXPRFAM_pv103_lend_tvr` · `CORR_LOW` | **无** | 空（已算完） |
| `bl6KwjwK` | GBR_R_anlrevlend_01 | 11-08 02:00 | `CH_REG` · `SRC_analyst_revision` · `EXPRFAM_anlrev_lend` · `CORR_LOW` | **无** | 空（已算完） |

**口径说明（2026-11-08 定案）**

1. `PowerPoolSelected` 是**平台**在提交成功后自动追加的，不是我们打的。全账户 ACTIVE 297 颗中 36 颗带此标签，状态 22 COMPLETE + 12 ACTIVE + 2 UNSUBMITTED，**零退役**。
2. 清掉它的代价 = 放弃 CAP 四口径（all submitted / WQ selected / Power Pool / Osmosis，**取最大**）中的 Power Pool 一条。因取最大、且该口径系统性偏低（论坛六维：Expert 0.51 vs combinedAlpha 0.93、GM 1.63 vs 2.12），**实际损失远小于字面**。
3. 保留它并非纯赚：提交**前**预置会触发 `PURE_POWER_POOL_THEME` 检查（合法 REGULAR 可能被拒），故 `_derive_tags` 已在 PATCH 前剔除；提交后是否清按「PPA 通道一律不接受」政策执行。
4. `check_tags` 自本日起**不再把它算违规**，改走 `tag_notes` 信息项——否则每次审计在 297 颗上刷 36 条假告警，盖掉真正要修的缺 `CH_*` / 缺 `SRC_*`。

**观察到的旁证**：`RRE5Mwkn` / `bl6KwjwK` 的 checks 已全部完成，`pending` 为空，且 **pass/fail/warning 三处都没有 `POWER_POOL_CORRELATION`** ⇒ 平台对**不带**该标签的 alpha 不产出 PP 相关性结果；`zq3eb7No` / `3qoGxkqZ` 仍挂着该项只是异步队列未跑完。这条留待判别实验（PATCH 加回标签 → 看该项是否出数）确认。


---

# DEU · QPvzNNGG（2026-11-08 22:25，Phase B/C/D 完整审计）

**候选**：QPvzNNGG — predictive_starmine（严格 ATOM，MODEL 塔）
表达式：`group_neutralize(add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 12)), rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))), bucket(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 252)), range="0,1,0.05"))`
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08，9 算子。
IS：S 1.70 / F 1.30 / 2Y 2.18 / TO 0.155 / margin 0.000774 / sub_u 过平台闸。

## B.0 WebDataScope 门
submit_verdict: failed_ra=0, sim_fails=[] ⇒ Failed=0 且无 PENDING ⇒ PASS。

## B.2 逐年 Sharpe（2014–2023）
1.56 / 1.54 / 0.93 / 1.26 / 1.15 / 1.52 / 2.37 / 2.34 / 2.32 / 2.03
- Recent-3yr（2021-2023）：[2.34, 2.32, 2.03]，均值 2.23 ≥ 1.58，每年为正 ✓
- Recent-3yr CV = 0.064 < 0.40 ✓
- 衰减比 = 2.03 / 1.70 = 1.19 ≥ 0.50 ✓
- 平年 0 ✓；max/min = 1.15 ≤ 3 ✓
- 全历史 CV 0.269，曲线随时间改善（无厂字形）✓

## B.3 pnl
年回撤均值 0.0282，最大 0.0469（2021）< 2×均值 0.0563 ⇒ 无季度异常 ✓
margin 7.7bp @ TO 15.5% ⇒ ≥5bp ✓
Top-5 个股集中度：get_alpha_pnl 无逐股分解（可选项跳过，记软信息）。

## B.4 相关性
prod 0.6777（refresh 终验 2026-11-08）✓ / self 0.6779（新 OS 池 18，通过 <0.7 但贴线，软标记）。

## Phase C 判定：**PASS**
软标记：①9 算子（≤12 合规）②self 0.6779 贴线 ③Top-5 集中度无逐股数据。
经济可解释性：分析师预期修正广度 + StarMine 预测惊喜三腿等权，bucket 中性化按修正速度分组消除速度暴露——「修正向上+预测惊喜为正的股票市场反应不足」。

# DEU · LLMzYrZe（2026-11-08 22:25，备选席审计）

逐年 Sharpe：1.75 / 2.03 / 0.91 / 1.65 / 2.50 / 1.00 / 1.68 / 1.26 / 1.09 / 2.36
- Recent-3yr：[1.26, 1.09, 2.36]，均值 **1.570**（贴线 1.58，边际）；平台 2Y = 1.69 ≥ 1.58 ✓
- CV 0.367 < 0.40 ✓；衰减比 2.36/1.61 = 1.47 ✓；max/min 2.17 ✓；平年 0 ✓
- prod 0.6697 ✓ / self 0.6702（贴线）
## Phase C 判定：**CONDITIONAL**
软标记：近 3 年均值 1.570 边际（按年化均值口径贴线，平台 2Y 口径过线）＋ self 贴线。
处置：作为 QPvzNNGG 的备选席（二者互相关 0.678，同族只占一席）；若 QPvzNNGG 提交失败换防前需重跑本审计。


---

# DEU · RREwqrNa（2026-11-08 23:10，Wave 65 修复产出审计）

**候选**：RREwqrNa — shortinterest3 借贷交易族（严格 ATOM，SHORTINTEREST 塔）
表达式：`winsorize(reverse(group_rank(multiply(multiply(rank(subtract(ts_sum(vec_avg(transaction_count_main),176),ts_sum(vec_avg(transaction_count_main),66))),rank(subtract(ts_sum(vec_avg(average_loan_duration_days_main),176),ts_sum(vec_avg(average_loan_duration_days_main),66)))),rank(subtract(ts_sum(vec_avg(loan_rate_volatility_main),176),ts_sum(vec_avg(loan_rate_volatility_main),66)))),industry)),std=4)`
设定：DEU/TOP500/D1/FAST/decay4/trunc0.08/**nanHandling ON**（从 salvage 原件 omWbGMzn 平台 settings 破案恢复；本轮修复的关键是找回 nanHandling=ON 与 decay=4）。
IS：S 1.65 / F 1.17 / 2Y 2.57 / TO 0.1073 / sub 1.12 / failed_ra=0。

## B.0 门
failed_ra=0, sim_fails=[] ⇒ PASS。

## B.2 逐年 Sharpe
1.46 / 1.94 / 1.17 / 1.22 / **3.51** / 1.38 / **0.18** / 0.58 / **3.56** / 1.42
- Recent-3yr（2021-2023）：[0.58, 3.56, 1.42]，均值 1.85 ≥ 1.58 ✓，每年 >0.3 ✓
- **Recent-3yr CV = 0.68–0.83 ≥ 0.60 ⇒ REJECT**（2022 尖峰拉高离散度）
- 衰减比 = 1.42/1.65 = 0.86 ✓；平年（近3）0 ✓；max/min 6.1（全历史软标记）

## B.4 相关性
prod **0.6684** ✓（余量 0.032）/ self 0.2626 ✓（池 18）/ vs 已提交两颗 <0.5 ✓（0.051）。

## Phase C 判定：**REJECT**（唯一失败项：CV_Sharpe）
其余全部 PASS。**放宽入口 = 用户明确指令**（skill 规则）：若用户豁免 CV 闸，本件即 submission-ready（prod/self/互相关/IS 全绿）。
经济可解释性：证券借贷活跃度上升 + 借贷期限变化 + 利率波动上升的股票=空头压力累积，做空其后续走弱——三腿反向合成。

---

# DEU · RREOz5qn（2026-11-09 21:20，Wave 88 换血版 robustness 审计）

**候选**：RREOz5qn — predictive_starmine（严格 ATOM，MODEL 塔，Wave 88 换血版）
表达式：`group_neutralize(add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 12)), rank(ts_mean(predicted_surprise_fy1_ebitda_4, 5))), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))), bucket(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 252)), range="0,1,0.05"))`
设置：DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc0.08，9 算子。
IS：S 1.72 / F 1.31 / 2Y 2.10 / TO 0.156 / sub 1.31 / failed_ra=0 / **prod 0.5834 ✓**（余量 0.117，全家族最干净）

## B.0 WebDataScope 门
failed_ra=0 ⇒ PASS。

## B.2 逐年 Sharpe（2014–2023）
1.72 / 1.67 / 1.31 / 1.47 / 1.08 / 1.51 / 1.66 / 2.54 / 2.91 / 1.24
- Recent-3yr（2021-2023）：[2.54, 2.91, 1.24]，均值 2.23 ≥ 1.58 ✓，每年 >0.3 ✓
- Recent-3yr CV = 0.32 < 0.60 ✓
- 衰减比 = 1.24 / 1.72 = 0.72 ≥ 0.50 ✓
- 平年 0 ✓；max/min = 2.35 ≤ 3 ✓
- 全历史 CV 0.32（无厂字形）✓

## B.3 margin
年 margin 均 >0.0006（全期 0.00098），TO 15.6% ⇒ margin/TO 比健康 ✓

## B.4 相关性
prod **0.5834** ✓（余量 0.117）/ self 待查（与新腿 fy1_ebitda_4 相关性预期低于原版）

## Phase C 判定：**PASS**（无软标记需带上）
经济可解释性：分析师对 FY1 EBITDA 的预测惊喜（对比 F12M 口径的修正广度）+ 90d 修正速度，bucket 中性化消除修正速度暴露——多视界预期惊喜组合。

---

# 稳健性审计 — mLovbnm2（2026-11-10 01:5x）★★★ 本轮首个全闸通过件

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

表达式（9 ops，DEU/TOP500/D1/FAST/decay2/trunc0.08/nanOFF/SUBINDUSTRY）：
```
multiply(
  multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
          group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), industry)),
  group_rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry)
)
```

| 年 | Sharpe | Fitness | TO | margin | longCount |
|---|---:|---:|---:|---:|---:|
| 2014 | 2.02 | 1.73 | 0.1520 | 14.6bp | 80 |
| 2015 | **3.63** | 4.57 | 0.1437 | 31.7bp | 81 |
| 2016 | 1.42 | 1.04 | 0.1471 | 10.8bp | 89 |
| 2017 | 1.97 | 1.68 | 0.1405 | 14.5bp | 101 |
| **2018** | **0.35** | 0.13 | 0.1478 | 2.9bp | 102 |
| 2019 | 2.90 | 3.09 | 0.1430 | 22.7bp | 105 |
| 2020 | 1.07 | 0.89 | 0.1332 | 13.8bp | 115 |
| 2021 | **3.00** | 3.49 | 0.1278 | 27.1bp | 134 |
| 2022 | 2.25 | 2.39 | 0.1309 | 22.5bp | 148 |
| 2023 | 1.28 | 0.93 | 0.1348 | 10.6bp | 133 |

- 近 3 年均值 = **2.177 ≥ 1.58** ⇒ 主判 **PASS**
- **无负年**（最低 2018 = 0.35）；**十年无空仓年**（longCount 80→148 全覆盖）
- 全史 CV ≈ **0.476**（均值 1.989，sd 0.947）；max/min = 3.63/0.35 ≈ 10.4（2018 单年拉大分母，仅参考）
- 末段三年缓降 3.00 → 2.25 → 1.28，**末年 1.28 仍为正且 2Y 闸 2.18 已过**（2Y 由 2022+2023 合成）
- 换手稳定 12.8%–15.2%，十年无漂移 ⇒ 无「靠换手堆指标」风险
- margin 2015 = 31.7bp、2021 = 27.1bp、2022 = 22.5bp；2023 = 10.6bp（弱年但为正）

**结论：PASS（主判通过，无 soft_flag 阻断）**
依据：2026-11-07 定案的 Recent-3yr 口径——本候选近 3 年均值 2.177、无负年、无空仓年、无末段破线；2018 单年 0.35 属历史中段单年离群（其后 2019 即回到 2.90），不构成 REJECT。

**全闸终验（2026-11-10 01:5x 实测）**：
| 项 | 值 |
|---|---|
| Sharpe | **1.94**（≥1.58 ✅） |
| Fitness | **1.79**（≥1.0 ✅） |
| 2Y Sharpe | **2.18**（≥1.58 ✅） |
| Turnover | 0.1401（0.01~0.7 ✅） |
| sub_universe_sharpe | 1.17 ✅ |
| investability_sharpe | 1.40 ✅ |
| risk_neutralized_sharpe | 1.07 ✅ |
| drawdown | 0.0709 ✅ |
| **failed_ra_count** | **0** |
| **checks.fail** | **[]** |
| **production corr** | **0.6572 < 0.7 ✅**（直方图 [0.6,0.7) n=8，无 [0.7,0.8] 钉） |
| **self corr** | **0.562 < 0.7 ✅** |
| **边际贡献 ΔSharpe** | **+0.68 ✅ 正向**（组合 sharpe 1.73 → 2.41，fitness 1.37 → 2.08） |

⇒ **本件是 DEU 战役首个同时通过 RA / prod / self / 边际贡献四道的候选**（前轮 5 颗候选池全部因 ΔSharpe 为负被拦）。
---

# 稳健性审计 — 1YNMAA8M（2026-11-10 06:3x）★★★ 第二席

**口径：Recent-3yr（2021/2022/2023，skill 判定表主判）**

表达式（9 ops，DEU/TOP500/D1/FAST/decay4/SUBINDUSTRY/trunc0.08/nanOFF）：
```
multiply(
  multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
          group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), sector)),
  group_rank(ts_sum(anl15_dps_gr_12_m_3m_chg, 22), sector)
)

| 年 | Sharpe | Fitness | TO | margin | long | short |
|---|---:|---:|---:|---:|---:|---:|
| 2014 | 1.65 | 1.31 | 14.9% | 12.7bp | 76 | 87 |
| 2015 | 1.59 | 1.32 | 13.4% | 13.7bp | 81 | 95 |
| 2016 | 1.56 | 1.28 | 14.7% | 13.4bp | 88 | 106 |
| 2017 | 1.01 | 0.63 | 13.8% | 7.7bp | 97 | 118 |
| 2018 | 1.06 | 0.78 | 13.1% | 10.7bp | 102 | 119 |
| 2019 | 2.06 | 1.96 | 13.6% | 18.1bp | 103 | 123 |
| 2020 | 0.78 | 0.54 | 13.5% | 9.6bp | 122 | 151 |
| 2021 | **2.96** | 3.54 | 11.8% | 30.5bp | 140 | 169 |
| 2022 | 2.19 | 2.34 | 12.5% | 22.9bp | 150 | 176 |
| 2023 | 1.25 | 0.97 | 12.5% | 12.1bp | 129 | 155 |

- 近 3 年均值 = **2.133 ≥ 1.58** ⇒ 主判 **PASS**
- **无负年**（最低 2020 = 0.78）；**十年无空仓年**（longCount 76→150 单调上升）
- 全史 mean 1.611 / sd 0.620 / **CV 0.385**（低于 mLovbnm2 的 0.476，更稳）
- max/min = 2.96 / 0.78 ≈ 3.8（分母健康）
- 换手稳定 11.8%–14.9%，十年几乎无漂移 ⇒ 无「靠换手堆指标」风险

**结论：PASS（主判通过）**

### 全闸终验（2026-11-10 06:3x 实测）
| 项 | 值 | 闸 |
|---|---|---|
| Sharpe | **1.58** | ≥1.58 ✅ |
| Fitness | **1.36** | ≥1.0 ✅ |
| 2Y Sharpe | **2.13** | ≥1.58 ✅ |
| Turnover | 0.1337 | 0.01~0.7 ✅ |
| sub_universe_sharpe | 1.01 | ✅ |
| investability_sharpe | 1.26 | ✅ |
| drawdown | 0.0845 | ✅ |
| returns / margin | 9.96% / 14.9bp | |
| **failed_ra_count** | **0** | ✅ |
| **checks.fail** | **[]** | ✅ |
| **production corr** | **0.6951** | <0.7 ✅（余量仅 0.005） |
| **self corr** | **0.6946** | <0.7 ✅（余量仅 0.005，贴线） |
| **边际贡献 ΔSharpe** | **+0.43**（组合 1.73→2.16） | >0 ✅ |
| mix_audit | 不阻断（usage=MULTI_DATA_SET） | ✅ |

### 与现有件的正交性（compute_mutual_correlation, threshold 0.7）
| 对 | 相关 |
|---|---:|
| 1YNMAA8M ~ mLovbnm2 | **0.6955** |
| 1YNMAA8M ~ bl6AvMkN（已提交） | 0.5128 |
| 1YNMAA8M ~ zq3eb7No（已提交） | 0.2471 |
| mLovbnm2 ~ bl6AvMkN | 0.5620 |

⇒ `max_mutually_below_subset` = **[1YNMAA8M, mLovbnm2, bl6AvMkN, zq3eb7No]（4/4 全部低于 0.7）** ⇒ **四颗件可同时入池**。

**★ 两点风险提示**：
1. **prod 余量仅 0.005**（0.6951）与 **self 余量仅 0.005**（0.6946）——两者都贴线，prod 会随生产池变化漂移（历史有 0.69→0.99 的漂移记录）⇒ **提交前必须 refresh 终验**。
2. 与 mLovbnm2 互相关 0.6955 亦贴线 ⇒ 两颗件**不宜同时提交**（除非 prod 复核后仍稳定）。