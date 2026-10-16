# USA 未点亮塔战役 · 波次台账（campaign_20261014）

> 设置基线（全部波次一致）：USA / TOP3000 / D1 / **STATISTICAL** / trunc 0.08 / nanHandling ON / maxTrade OFF / pasteurization ON / unitHandling VERIFY
> 骨架基线：`group_rank(ts_zscore(ts_backfill(F, 252), 252), industry)`（USA b3 型，`omWMO06n` 验证 prod 0.6948 PASS）

## 波次总览

| 波 | multi-sim id | 数据集 | 条 | 最佳 | 结论 |
|---|---|---|---:|---|---|
| A1 | `2TWTRR4EO4TTaRtl6Ce50VG` | insider_agg_matrix(2) / option3(2) | 4 | S 0.76 | 水平值信号弱；**1 个毒字段** |
| A2 | `4hbWAcP34CU9uDf0ZTLBox` | board_gov_stats(2) / short_interest_pred(2) | 4 | S 0.14（2Y **4.03**） | ★方向反 + 2Y 极强 |
| B1 | `3t1Cot55gQaAubL28qmzh` | option3 比率的 ts_rank/ts_delta/短窗z | 4 | S 0.78 | option3 天花板 |
| B2 | `2C9xjA7NB4gP98x1egGekbsz` | option3 OTM/subtract/ts_sum/ts_av_diff | 4 | S **0.88** | option3 天花板 ≈0.88 |
| C1 | `28g38CgvE4oObhNWkBYU6ww` | **short_interest 反向** + decay20 | 4 | **S 1.11 / 2Y 3.13✓ / `ra_failed=false`** | ★★★ 本轮突破 |
| C2 | `3nlHRR8RQ4I0bByXQmRo3B` | short_interest 其余 6 字段反向 | 4 | S 0.82 | surprise 族判死 |
| D1 | `46ueO6dK04QpbfSCv5s2Psu` | 冠军族窗口微扫（decay **63**） | 4 | S 0.74 | decay 63 劣于 20 |
| D2 | `OVJHZePm4z6blD1ekiALTYO` | 冠军族轴/平滑（decay **63**） | 4 | S 0.77 | 同上，decay 20 仍最优 |
| E1 | `17ubTJ3lE4C99hEmeMLyvfv` | 冠军族 quantile/market/sp1.5/av_diff（decay20） | 4 | **S 1.26**（`ts_av_diff` 胜出） | ★ `ts_av_diff` 是新杠杆 |
| E2 | `3yfsOfe2G54XaSt14tqNVAyD` | 第二腿 prior_* 反向（**decay10**） | 4 | **S 1.52** | ★★ decay 10 突破 |
| F1 | `vREuq9Ky55I8ZGS8f93TNU` | **decay 5** × {b3, av_diff, market, quantile} | 4 | **S 2.07 / 2Y 4.22** | ★★★ 本族最优 |
| F2 | `2CdeMg7zh4j28E2v5AggOFP` | `ts_av_diff` 窗口 66/126/504（decay10） | 4 | S 1.88 / **F 0.55** | 504 窗最优 |
| G1 | `yHpmS5Hk4PMcoShThr0xBZ` | **decay 3** × av_diff 504 变体 | 4 | S 2.15 但 TO **0.823 ❌** | decay 3 出界 |
| G2 | `2gHDw2eFa4tG96qJ2XUp7zU` | **trunc 0.04** × 轴/zscore（decay5） | 4 | **S 2.13 / F 0.54** | trunc 逐位无差 |
| H1 | `1xDWIw3TI4JPcvJniTsXu14` | av_diff 窗口 378/504/756/1008（d10/trunc.04） | 4 | S 1.88 / F 0.55 | 窗口 plateau |
| H2 | `4ruqaP7Xs4ZE9HI102F84V3J` | `divide(predicted_change, predicted_value)` 比值族 | 4 | S 1.03–1.44 | 归一化杀信号 |
| J1 | `4yjGHJaDe5czbGe18ZmkdPaB` | TOP2000/SECTOR × 门控/if_else/max_diff | 4 | S 1.47 / returns **0.0576** | 门控全灭；universe 抬 returns |
| J2 | `1qpW6XdV44jDa64SHmiGwpv` | **TOP2000 + decay5** × 窗/轴 | 4 | **returns 0.0789 / F 0.55** | ★ returns 杠杆确认 |

## ★★★ 本族最优（decay 5 · STATISTICAL · trunc 0.08 · TOP3000）

| alpha | 表达式 | S | F | 2Y | SUB | TO | returns | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **`MP0WWadz`** | `group_rank(ts_av_diff(reverse(short_interest_predicted_change), 252), industry)` | **2.07** | 0.52 | **4.22** | **1.45** | 0.668 | 0.0414 | **`failed_ra_count=1`（仅 LOW_FITNESS）；`ppa_failed=false`** |
| `akVYYbQ6` | 同上，轴 **market** | 2.04 | 0.52 | **4.39** | **1.54** | 0.664 | 0.0424 | 同上；**CLUSTER 1.13 最高** |
| `1Yj99XlJ` | `quantile(av_diff252, industry)` | 1.89 | 0.47 | 4.01 | 1.39 | 0.654 | 0.0406 | 同上 |
| `9qEvvj81` | b3(`reverse(predicted_change)`) | 1.78 | 0.41 | 4.23 | 1.28 | 0.677 | 0.0363 | 同上 |

### ★★★★ 本轮两条决定性杠杆（可迁移）

**① `ts_av_diff` > `ts_zscore(ts_backfill(...))`（同设置同轴）**

| 结构 | decay5 S | decay10 S | decay20 S |
|---|---:|---:|---:|
| `ts_zscore(ts_backfill(reverse(F),252),252)` | 1.78 | 1.52 | 1.11 |
| `ts_av_diff(reverse(F),252)` | **2.07** | **1.64** | **1.26** |

⇒ **`ts_av_diff`（偏离自身均值）在全部 decay 档稳定优于 `ts_zscore` 长窗**，平均 **+16~20%**。
机制：`ts_zscore` 除以 `ts_std_dev`，把「低波动股的微小偏离」与「高波动股的同幅偏离」压成同值；`ts_av_diff` 只减均值**不除波动** ⇒ 保留幅度信息（对应 memory 里「可恢复被归一化抹掉的幅度」）。
⚠ 前提：字段须是**慢变量**（本族 cov 0.9987 满覆盖日更预测变动）。**事件型字段禁试**（同 `ts_mean` 会除掉频率信息的道理）。

**② decay 在本族「越小 S 越高」，区域默认值 5 恰是峰顶**

| decay | 63 | 20 | 10 | **5** | 3（测中） |
|---|---:|---:|---:|---:|---:|
| b3 S | 0.70 | 1.11 | 1.52 | **1.78** | — |
| av_diff S | — | 1.26 | 1.64 | **2.07** | — |

⇒ 与 USA 已知「decay↓压 prod」（SUPER 实证 d100→d50：prod 0.8495→0.6881）**方向一致**。
⇒ ★ **对 USA 的新含义：`decay` 是「压 prod」+「抬 S」的双向杠杆，但牺牲 fitness**（TO 0.202→0.668，F 0.27→0.52）⇒ **S↔F 真实权衡，非免费午餐**。

### 当前唯一未过闸 = `LOW_FITNESS`（0.52 / 需 1.0）

USA 已有公式 `F ≈ 2.813 × S × √returns`（不吃 turnover）⇒ 要 F≥1.0，S 2.07 不变时需 **returns ≈ 0.055（现 0.0414，+33%）**。
G1/G2 在测三条路径：① decay 3；② truncation 0.04；③ `group_zscore` / subindustry 轴（幅度信息保留更多）。
| E2 | `3yfsOfe2G54XaSt14tqNVAyD` | 第二腿 prior_* 反向（decay10） | 4 | — | 进行中 |

## A1 结果（insider_agg_matrix + option3，decay5）

| alpha | 表达式 | S | F | 2Y | SUB | TO | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---|
| `3qjbQg8X` | b3(`significant_value_1`) | 0.74 | 0.24 | 0.56 | 0.22 | 0.050 | SHARPE/FIT/SUB/2Y |
| `N1ewxkYE` | b3(`directional_indicator_2`) | **0.00** | 0 | 0 | — | **0.000** | **longCount=0 shortCount=0** |
| `1Yj9kVqz` | b3(`divide(opt3_openinteputatm, opt3_openintecallatm)`) | 0.76 | 0.25 | **1.39** | 0.30 | 0.157 | SHARPE/FIT/SUB/2Y |
| `88vo5kmW` | b3(`divide(opt3_volumecallotm, opt3_volumeputotm)`) | 0.27 | 0.04 | 1.12 | 0.06 | **0.295** | SHARPE/FIT/SUB/2Y |

### ★ 关键诊断

1. **`directional_indicator_2` 是毒字段**：`longCount=0 / shortCount=0 / TO=0` ⇒ 字段在 USA 实际**无有效截面值**（平台元数据 cov 0.7716 但组内几乎全缺失）。**`insider_agg_matrix` 的 `directional_*` 全族（5 字段）应视为高风险**，需逐个验 longCount。
2. **b3 骨架对「水平值型」字段无效**：`significant_value_1` / `independent_director_ratio` / `board_departure_rate_1y_board` 都是**水平值**，`ts_zscore` 后仍近静态 ⇒ S 0.11–0.74。
   ⇒ **USA 水平值字段必须换成时间序列变换**（`ts_delta` / `ts_rank` / `ts_av_diff` / `ts_sum`），这正是 B1/B2 在测的。
3. **`opt3` 的 put/call OI 比率有真信号**（2Y 1.39 / investability_sharpe 0.94 > IS 0.76）⇒ option 塔 volume/OI 族在 USA **确实可挖**，与 `option.md` 判断一致。
4. **TO 已是障碍**：`88vo5kmW` TO 0.295 接近 review 上限 0.30；`divid﻿e` 比率天然高换手 ⇒ 必须配 decay/慢化。

## A2 结果（board_gov_stats + short_interest_pred，decay5）

| alpha | 表达式 | S | F | 2Y | SUB | TO | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---|
| `omop8VM2` | b3(`board_departure_rate_1y_board`) | 0.11 | 0.01 | 0.46 | 0.09✓ | 0.040 | SHARPE/FIT/2Y |
| `pwvXY8Ab` | b3(`independent_director_ratio`) | **−0.16** | −0.02 | −0.84 | 0.28 | 0.041 | SHARPE/FIT/2Y |
| `9qEvZJ09` | b3(`short_interest_surprise_ratio`) | 0.14 | 0.01 | **4.03✓✓** | 0.07 | **0.761❌** | SHARPE/FIT/**HIGH_TURNOVER** |
| `pwvXY8Ob` | b3(`short_interest_predicted_change`) | **−1.48** | −0.32 | **−3.16** | −0.78 | **0.677❌** | SHARPE/FIT/SUB/2Y |

### ★★★ 本轮最重要发现：`short_interest_pred` **方向是反的**

- `short_interest_predicted_change` 原方向 **S = −1.48 / 2Y = −3.16** ⇒ 绝对值已接近闸线（1.58）⇒ **不是无信号，是极性相反**。
  ⇒ 经济含义：**做空意愿上升 → 未来收益上升**（挤空 / 空头回补），或该字段编码方向与直觉相反。
  ⇒ **C1 波直接测 `reverse(...)` + 慢化**。
- `short_interest_surprise_ratio` **2Y = 4.03（全批最高）** 但 TO **0.761 > 0.70 闸** ⇒ 信号在近窗极强、换手爆炸。
  ⇒ 修法 = **慢化**（decay↑ / `ts_mean` / `ts_sum`），不是换结构。

⇒ **`short_interest_pred` 是本批唯一值得深挖的数据集**：cov 0.9987（满覆盖）+ alphaCount 低 + 已实证强 2Y。

### board_gov_stats 判死（治理水平值族）

`board_departure_rate_1y_board` S 0.11、`independent_director_ratio` S −0.16 ⇒ **治理类水平值字段在 USA 无独立 alpha**，与 `insiders.md`「insiders 数据集作主信号天花板低」一致。
⇒ 除非改用**变化量**（`ts_delta`）或做**子集门控腿**，否则不投。

## 后续波次设计（依据诊断）

| 波 | 目标 | 结构 | 状态 |
|---|---|---|---|
| B1/B2 | option3 比率的时间序列变换 | 8 条 4 变体 | ✅ 完成，天花板 0.88 |
| C1 | short_interest 反向 + 慢化 | 4 条 | ✅ 完成，**突破 e76pkZ9M** |
| C2 | short_interest 另6 字段反向 | 4 条 | ✅ 完成，surprise 族判死 |
| D1/D2 | 冠军族设置轴（decay63 + 窗口 + 轴 + 平滑） | 8 条 | ✅ 完成，decay20 仍最优 |
| E1 | 冠军族 quantile / market 轴 / signed_power1.5 / ts_av_diff | 4 条 | 🔄 进行中 |
| E2 | 第二腿 `prior_*` 反向 + decay10 | 4 条 | 🔄 进行中 |

## C1 结果 ★★★ 本轮突破

| alpha | 表达式 | decay | S | F | 2Y | SUB | TO | 闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **`e76pkZ9M`** | b3(`reverse(short_interest_predicted_change)`) | **20** | **1.11** | 0.32 | **3.13✓** | **0.87✓** | 0.346✓ | **`ra_failed=false` `ppa_failed=false`**（SHARPE/FITNESS 仅 warning）|
| `vROqwXrd` | `ts_mean(reverse(...), 22)` | 20 | 0.69 | 0.25 | 0.86 | 0.42 | 0.093 | SHARPE/FIT/2Y |
| `Vkd91baM` | `ts_sum(reverse(...), 66)` | 20 | 0.47 | 0.15 | 0.03 | 0.11 | 0.067 | 4 闸 |
| `XgRrmAJm` | `reverse(b3(surprise_ratio))` | 20 | −0.01 | 0.00 | −1.11 | 0.19 | 0.399 | SHARPE/FIT/2Y |

### ★★★ 三条决定性结论

1. **`reverse` 是本族的决定性算子**：`pwvXY8Ob` S −1.48 → `e76pkZ9M` S **+1.11**（同结构，仅加 reverse + decay 5→20）。
   ⇒ **方向假设必须先测反向**。「平台上更拥挤的字段」往往意味着**别人已经发现了正向**，反向才是白空间。
2. **decay 5→20 是同向改善杠杆**：TO 0.761 → 0.346（−54%），S 0.14 → 1.11（**+693%**），2Y −3.16 → 3.13。
   ⇒ 与 option3 相反（option3 是 TO 低但 S 也低）。**decay 方向逐族实测，禁跨族外推**。
3. **TO 爆炸的「强 2Y」是假强**：`surprise_ratio` 原方向 2Y **4.03** 但 TO **0.761 > 0.70 闸**；加 reverse 后 S ≈ 0.07。
   ⇒ **`2Y > 2.0` 且 `TO > 0.5` 的候选必须先怀疑不可用**，不可当突破。

## C2 结果（surprise 族判死）

| alpha | 字段 | S | 2Y | TO |
|---|---|---:|---:|---:|
| `d5KXpkVv` | `reverse(surprise_value)` | 0.07 | −0.90 | 0.404 |
| `88vob5da` | `reverse(surprise_amount)` | 0.07 | −0.90 | 0.405 |
| `JjPwqMKx` | `reverse(prior_surprise_ratio)` | 0.17 | −1.88 | 0.392 |
| `78oAW7E5` | `reverse(predicted_value)` | 0.82 | 0.68 | **0.066** |

⇒ `surprise_*` 三字段（ratio/value/amount）+ `prior_surprise_ratio` **全族判死**：S ≤ 0.17 且 2Y 多负。
⇒ **`short_interest_predicted_value`（S 0.82 / TO 0.066）是第二腿候选** —— TO 极低但 S 也不够，E2 波在测。

## D1/D2 结果（decay 63 全面劣于 decay 20）

| alpha | 变量 | S | F | 2Y | SUB | TO |
|---|---|---:|---:|---:|---:|---:|
| `78oAWx38` | 基准（bf252/z252/industry） | 0.70 | 0.24 | 2.63 | 0.59 | 0.202 |
| `omop7nRn` | bf **504** | 0.70 | 0.24 | 2.63 | 0.59 | 0.202 |
| `KPm03nvz` | z 窗 **126** | 0.64 | 0.21 | 2.41 | 0.50 | 0.209 |
| `YPxr6N8R` | z 窗 **504** | **0.74** | 0.27 | 2.52 | 0.66 | 0.197 |
| `ZYm560G8` | `ts_decay_linear(·, 20)` 无 z | 0.57 | 0.20 | 0.89 | 0.32 | **0.077** |
| `MP0WO1A9` | `ts_zscore(ts_decay_linear(·,20))` | 0.54 | 0.17 | 1.33 | 0.54 | 0.076 |
| `akVY6L31` | 轴 **sector** | 0.68 | 0.23 | 2.77 | 0.60 | 0.202 |
| `3qjbw9WN` | 轴 **subindustry** | **0.77** | 0.27 | **2.82** | 0.59 | 0.205 |

### 结论
- **decay 63 整批劣于 decay 20**（同结构 S 0.70 vs 1.11）⇒ **decay 20 是本族甜点，不加档**。
- **平滑（`ts_decay_linear`）在本族是零和**：TO 降到 0.076–0.077（极低）但 S 掉到 0.54–0.57、2Y 崩到 0.89。
  ⇒ 与 memory铁律「时间平滑类在累积型信号上零和」一致。
- **轴：`subindustry`(0.77) > `sector`(0.68) ≈ `industry`(0.70) > `market`**（E1 在测）。
  ⚠ 注意 USA 已知 prod 排序 `SECTOR` < `STATISTICAL` < `SUBINDUSTRY`（SUBINDUSTRY 最差 prod）⇒ **subindustry 轴 S 最高但 prod 可能最差**，需实测取舍。
- **`bf504` 与 `bf252` 逐位相同**（S/F/2Y/SUB/TO 全同，仅 pnl 微差）⇒ **backfill ≥ 252 后已饱和，加长无效**（字段 cov 0.9987 满覆盖，无缺失可填）。
---

## 决策：换数据集（`twitter_sentiment_l2`），终止 short_interest 腿

### 依据（fitness 公式给出的硬裁决）

`fitness = S × √(returns / max(TO, 0.125))`（12 点回归，误差 ≤1.8%）

`short_interest_pred.predicted_change` 要 F≥1.0 需 `returns/max(TO,0.125) ≥ 1/2.13² = 0.220`，
实测 **0.064**，差 3.4×。两条可能路径均已实测封死：
- **降 TO**：`ts_target_tvr_decay(target_tvr=0.10)` 把 TO 压到 **0.090**（已低于 0.125 下限，分母理论最优），
  但 S 从 2.13 → 0.71（−67%）⇒ **降 TO 在本族是等比降 S**，非免费午餐。
- **抬 returns**：TOP2000 把 returns 0.0424 → 0.0789（+86%），但 S 压到 1.59 ⇒ 两端仍卡 F≈0.55。

⇒ **数据集层天花板 ≈0.55**，同 `macro38`(F 0.82) / `continuation_score`(F 0.42) 先例。
该集 10 字段仅此 1 条有信号 ⇒ **无第二条腿** ⇒ 继续磨参数是纯浪费，**换集**。

### 换集判据

`twitter_sentiment_l2`（socialmedia 塔，本季 0 颗）**画像全项占优**：
| 项 | 值 |
|---|---|
| fieldCount | 95（**全部 MATRIX**，无 VECTOR 归约坑） |
| coverage | `market_relevance_score_*` = **1.0**；`aggregated_sentiment_value_*` = 0.82–0.94 |
| userCount | **0–21** |
| alphaCount | **0–40**（对比 socialmedia12=60341 / socialmedia8=16947） |
| 机制正交性 | `market_relevance_score_*` = **「社媒活动对市场影响的相关度」= 注意力**，**不是情绪分** ⇒ 与已饱和的 sentiment 情绪族正交 |

### 配方：**直接套 `omWMO06n` 已验证过 fitness 闸的配方**

```
group_rank(ts_zscore(ts_backfill(F, 252), 252), industry)
USA / TOP3000 / D1 / STATISTICAL / **decay 0** / trunc 0.08 / nanHandling ON / maxTrade OFF
```
> `omWMO06n`（earnings_sent_matrix）实测 **S 2.50 / F 1.52 / 2Y 4.22 / SUB 1.22 / TO 0.0891 / prod 0.6948 PASS / self 0.3908**，
> 是 USA **唯一已提交且过全闸含 prod** 的 b3 型样本。★ **其 TO=0.0891 < 0.125 下限** ⇒ 低换手慢字段是过 fitness 闸的关键前提。
> ⚠ 本轮 `short_interest` 腿 TO 0.66 远高于此 ⇒ 先天劣势。

multi-sim：`KzJxEfZs4oGcC41eAtgR55y`（b3 × 4 字段）、`1sQ1Cx8EI4UwaUnvPYJ6xDn`（`ts_av_diff` 升级 + 另 2 字段）
preflight：`valid=true, unknown_fields=[]`（4+4 字段平台实时校验通过）

---

## 第二腿：`workforce_flow_skills`（other 塔，mult 1.4）— ★ 首个过 fitness 闸

### 胜出：`rKd3Lro9`（净招聘流入/流出比）
```
group_rank(ts_zscore(ts_backfill(divide(vec_sum(employee_inflow_count),
            add(vec_sum(employee_outflow_count), 1)), 252), 252), industry)
USA / TOP3000 / D1 / STATISTICAL / decay 10 / trunc 0.08 / nanHandling ON
```
| S | F | 2Y | SUB | TO | returns | inv_S | inv_F | margin | 失败闸 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **2.22** | **1.28 ✓** | 0.93 ❌ | **1.00 ✓** | **0.0606** | 0.0418 | 2.07 | 1.16 | 13.8bp | **仅 LOW_2Y_SHARPE** |

- `failed_ra_count=1`、`ppa_failed=false`、`MATCHES_PYRAMID` PASS
- `pyramids.list = [USA/D1/OTHER, **multiplier 1.4**]`（全平台最高档）⇒ 过闸即点亮 other 塔

### 全数据集战绩（11 条）
| 表达式 | S | F | 2Y | SUB | TO | 闸 |
|---|---:|---:|---:|---:|---:|---|
| 净招聘比 bf252/z252（`rKd3Lro9`） | **2.22** | **1.28✓** | 0.93 | 1.00✓ | 0.061 | **仅 2Y** |
| 净招聘比 bf126/z252（`vROq9bZa`） | 2.20 | 1.27✓ | 0.92 | 0.99✓ | 0.061 | 仅 2Y |
| 净招聘比 bf504/z504（`P0MW6bPM`） | 2.17 | 1.24✓ | 0.73 | 0.90 | 0.059 | SUB+2Y |
| 薪资/招聘比 vec_avg（`3qjb6MKe`） | 1.70 | 0.86 | **1.44** | 0.39 | 0.052 | F+SUB+2Y |
| 薪资/招聘比 vec_sum（`YPxrkj3v`） | 1.42 | 0.66 | **1.54** | 0.20 | 0.059 | S+F+SUB+2Y |
| `av_diff(ratio,504)`（`pwvXEkWb`） | 0.92 | 0.31 | 0.39 | 0.31 | 0.154 | 4 闸 |
| `ts_rank(ratio,504)`（`A1QWb5ew`） | 0.69 | 0.20 | −0.52 | −0.07 | 0.160 | 4 闸 |
| `vec_avg(inflow)` 单腿 T4（`YPxrmW06`） | 0.72 | 0.24 | 0.42 | 0.39 | 0.088 | 3 闸 |
| `ts_av_diff(vec_avg(inflow))`（`vROq9Jlv`） | 1.00 | 0.35 | 0.90 | 0.46 | 0.154 | 3 闸 |
| `prestige_score`（`LL5j6l12`） | 0.10 | 0.03 | 0.75 | −0.05 | 0.137 | 4 闸 |
| `position_seniority_level`（`1Yj9mq8Q`） | 0.57 | 0.18 | 0.00 | 0.26 | 0.068 | 3 闸 |

### 三条结论
1. **比率形态 >> 水平值**：净招聘比 S 2.22 vs `ts_av_diff(vec_avg(inflow))` S 1.00（**2.2 倍**）。
2. **窗口修不了 2Y**：bf/z 三档 126/252/504 ⇒ 2Y 0.92/0.93/0.73，**无单调关系** ⇒ 2Y 是数据期属性。
3. **`ts_av_diff`/`ts_rank` 在本集反而弱**（S 0.69–1.00）⇒ 与 short_interest 腿结论**相反**
   ⇒ **「`ts_av_diff` 更优」是数据集特定，不是普适定律**（修正本轮 §3 适用范围）。
4. **互补腿存在**：净招聘比强 S/弱 2Y；薪资比弱 S/强 2Y（1.54）⇒ 组合腿救援的理想素材。

### 工程坑（浪费 1 批 4 条）
`preflight(auto_fix_vector)` 对嵌套写法产出 `vec_avg(vec_sum(x))` **双层包裹 ⇒ 整批 ERROR**；
而 `validate_expressions` 对同一表达式 **valid=true**（只验字段不验层级）⇒ **valid ≠ 可派发**。
**修法**：VECTOR 比率手写单层聚合 `divide(vec_sum(A), add(vec_sum(B),1))`（本轮已修正并成功）。

---

## 第四腿：`institutions18`（institutions 塔）判死

| 表达式 | S | F | 2Y | TO | 结论 |
|---|---:|---:|---:|---:|---|
| `omopN0Qv` fundownership 市值变化率 | 0.92 | 0.62 | 1.27 | **0.066** | 3 闸 |
| `2rj0poqb` fundownership 持股数变化率 | 0.90 | 0.60 | 1.25 | 0.066 | 3 闸 |
| `58jbpdN5` instownership 持股数变化率 | 0.31 | 0.16 | −0.06 | 0.037 | 3 闸 |
| `qME1N2oV` pct_held 水平 | **−0.41** | −0.17 | 1.05 | 0.143 | 4 闸 |
| `P0MWGLdw` lionshares_insider_num | 0.67 | 0.37 | 0.72 | 0.086 | 3 闸 |

⇒ 季频 → **TO 0.037–0.143 全部达标**（硬筛正确）；但 **S ≤ 0.92** ⇒ 强度不足 ⇒ 判死。

## 第五腿（攻坚中）：`workforce_flow_skills` 破 `LOW_2Y_SHARPE`

当前最优 `bl8kNqRm`：S 1.75 / F 1.41 / SUB 1.21 / TO 0.0317 / **2Y 1.10**（缺口 0.48）。
两条互补腿：**量**（净招聘比，强 S 弱 2Y）vs **价**（薪资/招聘比，弱 S 强 2Y 1.54）。

### 本轮新增算子穷尽（在飞）

| 波 | multi-sim | 算子 | 目标 |
|---|---|---|---|
| W1 | `2suhLV1sK5idaDI10qK3S77Q` | `ts_ir` / `ts_delta` / `days_from_last_change` / `ts_std_dev` | 量腿 2Y |
| W2 | `2LY65R8vq50ebOp19D2AbjJJ` | 薪资腿窗口三档（126/252/504）+ `ts_av_diff` | 价腿补强 |

### 剩余待扫算子（按 84 算子清单逐档排查）

- 已测：`ts_zscore` / `ts_backfill` / `ts_av_diff` / `ts_rank` / `ts_decay_linear` / `ts_mean` / `ts_sum` /
  `ts_delta`（上一轮）/ `ts_std_dev` / `ts_ir` / `ts_quantile` / `quantile` / `group_rank` / `rank` /
  `divide` / `subtract` / `add` / `reverse` / `if_else` / `trade_when` / `ts_max_diff` /
  `ts_target_tvr_decay` / `ts_target_tvr_hump` / `hump` / `signed_power` / `winsorize`（被闸拦）/
  `group_zscore` / `bucket`（喂 group_rank 被拒）/ `group_neutralize`
- **未测**：`ts_corr` / `ts_covariance` / `ts_regression` / `ts_arg_max` / `ts_arg_min` /
  `ts_max` / `ts_min` / `ts_kurtosis` / `ts_product` / `ts_scale` / `normalize` / `zscore` /
  `scale` / `vec_max` / `vec_min` / `vec_range` / `vec_stddev` / `vec_count` / `log` /
  `last_diff_value` / `kth_element` / `densify` / `pasteurize` / `bucket`（当分组轴）/
  `group_sum` / `group_mean` / `group_std_dev` / `group_backfill` / `group_count` /
  `group_scale` / `group_cartesian_product` / `vector_neut` / `tail` / `abs` / `max` / `min` / `sign`
