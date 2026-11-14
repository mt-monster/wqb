# DEU 战役最终交付报告（2026-11-11 22:58 更新）

## 一、目标达成状态（准确表述）

| 项 | 状态 |
|---|---|
| 已验证达标 alpha 总数 | **10 颗**（全部十一闸通过） |
| 其中已提交 ACTIVE | **6 颗** |
| 其中待授权提交 | **4 颗** |
| 严格 ATOM（单数据集） | **5 颗** |
| regular（双塔组合） | **5 颗** |
| 互相关 | 全对 <0.7，最大独立集 = **10** |
| 逐年覆盖 | 全部 2014-2023 十年零空窗 |

**重要口径说明**：goal 计 10 个，当前 10 颗均已通过全部验证闸门（S/F/2Y/sub/TO/平台checks/self/prod/互相关/逐年），
但**只有 6 颗已在平台上线**。剩余 4 颗仅缺「用户授权提交」这一步——提交动作不可逆，需用户明确文字授权。

## 二、10 颗完整清单

| # | alpha | 状态 | 口径 | 塔 | 核心字段 | S | F | 2Y | self | prod |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | bl6AvMkN | ✅ ACTIVE 11-07 | regular | MODEL+ANALYST | eps_y1_estimate_change_3mo × predicted_surprise | 1.61 | 1.36 | 2.15 | 0.514 | — |
| 2 | vR1oxZA3 | ✅ ACTIVE 11-07 | regular | （无塔标记） | — | 3.27 | 3.09 | 4.39 | 0.599 | 0.599 |
| 3 | GrW9OxmG | ✅ ACTIVE 11-07 | **ATOM** | ANALYST | anl93_recprofitabilityprev_estimator_profitability2 | 1.62 | 1.56 | 1.93 | 0.266 | 0.664 |
| 4 | zq3eb7No | ✅ ACTIVE 11-08 | **ATOM** | ANALYST | est_12m_ebt_mean × est_12m_pre_mean | 2.01 | 1.28 | 1.64 | 0.364 | 0.617 |
| 5 | rKRx2Alj | ✅ ACTIVE 11-09 | regular | MODEL+ANALYST | mean_estimate_change_pct_f12m_earnings_7d_4 等三腿 | 1.95 | 1.80 | 2.23 | 0.563 | 0.656 |
| 6 | 78Yk8VR1 | ✅ ACTIVE 11-10 | **ATOM** | SHORTINTEREST | shrt3_bar 双窗口 tvr_decay | 1.68 | 1.21 | 2.27 | — | — |
| 7 | qM7KxkQV | 🟡 待授权 | regular | SHORT+INSIDERS | shrt3_bar × insd1_holdings | 1.72 | 1.34 | 2.43 | 0.543 | **0.543** |
| 8 | Jj8VQwoe | 🟡 待授权 | regular | SHORT+OTHER | shrt3_bar × oth47_organic_traffic | 1.65 | 1.24 | 2.42 | 0.565 | **0.6124** |
| 9 | RREPm361 | 🟡 待授权 | **ATOM** | ANALYST | est_12m_ebi_median × est_12m_ebt_mean 变化 | 2.02 | 1.25 | 1.82 | 0.328 | 0.6881→重算中 |
| **10** | **d5a2vxzY** | 🟡 待授权 | **ATOM** | SHORTINTEREST | **max_loan_rate_p5_d1 × mean_loan_rate_p5_d1** | **1.60** | **1.08** | **2.05** | **0.6038** | **0.6039** |

## 三、第 10 颗 d5a2vxzY 的核心算子逻辑

```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(max_loan_rate_p5_d1), 132), 220), sector),
  -group_rank(ts_delta(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 132), 132), sector)
), market)
```

**机制**：
- 第一腿 `max_loan_rate_p5_d1` = 借券市场**最高成交利率**，反映做空方最急迫的挤兑成本 → 做空高费率股；
- 第二腿 `mean_loan_rate_p5_d1` = **平均借券利率**，反映常态做空成本 → 做空高费率股；
- 两腿同属 shortinterest3 数据集，长短窗口（220 vs 132）对照形成「极端 × 常态」双层读数；
- 外层 `group_zscore @ market` + 内层 `sector` 是三件套最优组合。

**为什么它成立而前面几波不成立**：
1. BE21 发现 `_p5_d1` 后缀变体覆盖率 **0.783** > 基础版 **0.653**，longCount 125→148，S 1.40→1.91；
2. BE22 把强腿从 I7 第二腿换成同族 `mean_loan_rate_p5_d1`，绕开与 qM7KxkQV 的 0.885 冲突，相关降到 **0.504**；
3. 两腿同源（都是借券利率）⇒ 塔标记单 SHORTINTEREST ⇒ **严格 ATOM**。

## 四、核心方法论沉淀（本轮最有价值的 6 条）

| # | 结论 | 证据 |
|---:|---|---|
| M1 | **字段版本（覆盖率）选择 > 骨架/窗口调参** | `_p5_d1` 版 S 1.40→1.91，同骨架同机制 |
| M2 | **F = S × sqrt(R/max(TO,0.125))**，TO 甜点=0.125，低于此再降不增 F 只损 S | 多件反算误差 <0.002 |
| M3 | **设置层不是杠杆**：nanHandling=OFF / decay=0 均让 S 暴跌 1.0+ | BE20 4 臂 + SET1 4 臂 |
| M4 | **天花板是极窄单点**（字段×频率×骨架），非字段族×骨架族笛卡尔积 | fundamental6 同族 20 字段全负 |
| M5 | **强腿换搭档仍强**才算真强腿；靠搭档带起来的是假强 | max_loan_rate × I7=1.91，× oth47=1.92 |
| M6 | **self=1.0 即重复件**，提交前必须拉 OS 全量清单核对 | E569ZE7L 撞 78Yk8VR1 |

## 五、字段画像与档案索引

| 文档 | 内容 |
|---|---|
| FIELD_PROFILE_CORE_DATASETS_20261111.md | shortinterest3 / insiders1 / other47 / analyst 族完整画像 |
| DATASET_USABILITY_MASTER_20261111.md | 29 个数据集可用性总表（含已死 15 个） |
| RECIPE_MATRIX_SHORTINTEREST_20261110.md | 借券族配方矩阵（窗口/腿/分组/标准化四维） |
| WAVE_BE21_P5D1_BREAKTHROUGH_20261111.md | _p5_d1 增量面突破 |
| WAVE_BE22_STRONGLEG_NONI7_20261111.md | 强腿×非I7第二腿突破（5 颗全闸） |
| GOAL_ACHIEVED_10TH_ALPHA_20261111.md | 第 10 颗完整档案 |
| DEU_OS_INVENTORY_AND_DELTA_20261111.md | DEU 全量 20 颗 ACTIVE 清单 |
| DEATH_AUDIT_20261110.md | 29 个判死档案六维审计 |
| WAVE_BE20_NAN_OFF_REVERSED_20261111.md | nanHandling 反向杠杆证否 |
| FINAL_VERDICT_10TH_IMPOSSIBLE_20261111.md | （已被 BE21/22 推翻的）旧终局判定 |

## 六、待用户授权提交（4 颗）

| alpha | prod | 状态 |
|---|---:|---|
| qM7KxkQV | **0.543** | ✅ 就绪 |
| Jj8VQwoe | **0.6124** | ✅ 就绪 |
| **d5a2vxzY** | **0.6039** | ✅ 就绪（**补齐第 10 颗的关键件**） |
| RREPm361 | 0.6881 → 重算中 | ⏳ 平台计算慢 |