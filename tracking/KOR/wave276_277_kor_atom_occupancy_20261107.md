# KOR ATOM 挖掘 · wave276 证伪 + OS 池占用图谱 + wave277 设计

日期：2026-11-07 · 区域：KOR / TOP600 / D1 · 目标：10 颗 ATOM（单数据集）REGULAR alpha

---

## 一、wave276 判死：**设置配方不可跨表达式移植**（本轮最重要的负结果）

wave276 试图把已提交 alpha `e73Rw8qg`（S1.62 / prod0.51）的设置配方
（**decay16 / SECTOR / trunc0.04 / nan OFF / maxTrade ON**）整体搬到 wave274 的表达式上。

| 臂 | 表达式 | 设置 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| wave274-P2 `QPvWKYOw` | `group_rank(vec_avg(eps_estimate_4wk_change),sector)` | d4 / t0.08 / **nan ON** | **1.24** | 0.97 | 0.0946 | 1.88 |
| wave276-R1 `N1NKe1Lw` | **同一表达式** | d16 / t0.04 / **nan OFF** | **0.54** | 0.27 | 0.0834 | 0.76 |

**结论**：同一表达式只改设置，S 从 1.24 塌到 0.54（−57%）。`e73Rw8qg` 的配方不是「数据集级最优设置」，
而是**与它那两个字段（`anl44_second_en_eps_value` + `pretaxprofit_estimates_down_4w`）耦合的表达式级设置**。

wave276 其余 4 臂同样全灭（S −0.31 ~ 0.54，prescreen 5/5 REJECT），
其中 R5 `RRE5ARlb` 用 `bps_consensus_change_percent`+`ffops_4week_consensus_change` 得 S −0.31 / DD 0.94，
说明**两条慢速百分比修正腿相加 = 纯噪声且回撤失控**。

> **纪律**：不要再从单条已提交 alpha 反推「通用配方」。设置必须在**目标表达式自己身上**做标定，
> 且 `nan_handling` 与字段覆盖率强耦合（cov 1.0 的 VECTOR 用 ON，cov<0.8 的用 OFF）。

## 二、★ 真正的约束不是 S，是**已提交池占用**

`9qxGWend`（S1.48 / F1.26 / 2Y1.74 / sub1.50）实测：

```
check_self_correlation → max 0.7328 > 0.7 ⇒ FAIL
  RRA2eE70 = 0.7328   ← 撞在这个已提交 alpha 上
  9qjGvaWe = 0.5434
  self pool = 29（不含 PPA），full OS pool = 43，PPA 14
```

`RRA2eE70`（S1.64 / prod0.66 / 已提交）表达式：
```
trade_when(greater(volume, ts_mean(volume,6)),
           signed_power(group_rank(winsorize(rank(ts_backfill(eps_y1_estimate_change_3mo,55)), std=0.26), sector), 4.0), -1)
```
⇒ **`eps_y1_estimate_change_3mo` 已被占用**，而它正是 `9qxGWend` 的第二腿。

同时核对字段归属：`eps_revision_magnitude` 与 `eps_y1_estimate_change_3mo` **都不在 analyst44**
（analyst44 字段快照 540 个里查无此名）⇒ `9qxGWend` 是**跨数据集**的，本来就不是 ATOM，不进入交付。

**⇒ 剩余 10 颗 ATOM 的第一约束是「字段与机制必须落在 OS 池白空间」，不是「先把 S 打上去」。**

## 三、KOR 已提交池全表（32 条 REGULAR / OS，2026-11-07 实测）

| alpha | S | F | TO | self | prod | 塔 | 字段 | 设置 |
|---|---:|---:|---:|---:|---:|---|---|---|
| `KPNo2lgl` | 2.57 | 2.09 | 0.208 | 0.361 | 0.550 | SHORTINTEREST | shrt38_invactsell/buy | SLOW_AND_FAST d30 t0.02 nanON |
| `omLjG1M5` | 2.28 | 2.17 | 0.122 | 0.068 | 0.570 | SHORTINTEREST | 同上 | SLOW_AND_FAST d30 t0.02 nanON |
| `O08kz5Mv` | 2.16 | 1.65 | 0.183 | 0.239 | 0.697 | SHORTINTEREST | shrt38_accum_* | STATISTICAL d4 t0.08 nanOFF |
| `A1NXddRw` | 2.11 | 1.81 | 0.129 | 0.655 | 0.655 | FUNDAMENTAL | oth466_is_ptx_inc_norm_q, bs_assets_tot_q | STATISTICAL d4 t0.08 nanOFF |
| `pwvndZJ3` | 2.09 | 1.44 | 0.221 | 0.459 | 0.641 | SHORTINTEREST | shrt38_invactnet_buy_amt | INDUSTRY d1 t0.04 nanON |
| `gJZ7AvZO` | 2.06 | 1.75 | 0.125 | 0.641 | 0.641 | FUNDAMENTAL | oth466_is_ptx_inc_norm_q, bs_eq_tot_q | STATISTICAL d4 t0.08 nanOFF |
| `rKdK2vLE` | 2.04 | 1.08 | 0.415 | 0.416 | 0.670 | SHORTINTEREST | shrt38_invactsell/buy | SECTOR d4 t0.08 nanON |
| `wpjJK60l` | 1.91 | 1.07 | 0.286 | 0.548 | 0.699 | MODEL | global_value_momentum_percentile_float, price_volume_quantile1_20d_pred | STATISTICAL d4 t0.08 nanOFF |
| `gJjnXv8g` | 1.90 | 1.59 | 0.067 | 0.072 | **0.786** | OTHER | buy_sell_ratio_all_250d_filled, buy_sell_tx_count_ratio_all_60d_filled | STATISTICAL d4 t0.08 nanON |
| `d5KJLqEw` | 1.87 | 1.28 | 0.172 | 0.305 | 0.563 | SHORTINTEREST+**ANALYST** | shrt38_sell/buy + **eps_estimate_4wk_change**(bucket 轴) | SLOW_AND_FAST d18 t0.02 nanON |
| `xA16pzQJ` | 1.86 | 2.19 | 0.027 | 0.231 | 0.698 | PV+OTHER | oth695_import_value_4 | MARKET d4 t0.08 nanON |
| `A1lb2KpR` | 1.83 | 1.14 | 0.218 | 0.671 | 0.674 | MODEL+OTHER | change_6m_rating_revision, short_horizon_hedge3_q1_5d | STATISTICAL d4 t0.08 nanOFF |
| `wpZkk1Mp` | 1.80 | 1.35 | 0.137 | 0.187 | 0.648 | FUNDAMENTAL | oth466_is_consol_net_inc_q, disc_oper_q, bs_assets_tot_q | STATISTICAL d4 t0.08 nanOFF |
| `0mrnWojG` | 1.79 | 1.40 | 0.129 | 0.624 | 0.684 | FUNDAMENTAL | oth466_is_net_inc_basic_q, bs_assets_curr_q | STATISTICAL d4 t0.08 nanOFF |
| `WjPEg2zd` | 1.78 | 1.64 | 0.119 | 0.431 | **0.730** | PV+ANALYST | **eps_estimate_4wk_change** + pv106_lastspreadbp | SECTOR d4 t0.08 nanON |
| `88lr21xo` | 1.77 | 1.40 | 0.125 | 0.357 | 0.568 | MODEL+OTHER | change_6m_rating_revision, hedge3 | STATISTICAL d4 t0.08 nanOFF |
| `RRAG0WMb` | 1.76 | 1.43 | 0.084 | 0.173 | 0.696 | MODEL | mdl138_4idpqc | REVERSION_AND_MOMENTUM d1 t0.15 nanOFF |
| `vRrQ5Npr` | 1.76 | 1.18 | 0.175 | 0.570 | 0.570 | SHORTINTEREST | shrt38_invactsell/buy | SLOW_AND_FAST d30 t0.02 nanON |
| `zq87zzqO` | 1.76 | 1.38 | 0.136 | 0.655 | 0.662 | FUNDAMENTAL | oth466_is_oper_inc_q, is_int_exp_net_q, bs_assets_tot_q | STATISTICAL d4 t0.08 nanOFF |
| `zqYaZ2gO` | 1.76 | 1.64 | 0.117 | 0.365 | **0.820** | PV+ANALYST | anl25_target_prc_med / close | INDUSTRY d4 t0.08 nanON |
| `0mre68gv` | 1.75 | 1.46 | 0.148 | 0.687 | 0.687 | MODEL | short_term_hedge_signal_5d_q5, seasonal_5d_quantile1_pred | SECTOR d6 t0.08 nanOFF |
| `WjAxxZVk` | 1.72 | 1.54 | 0.112 | — | 0.700 | MODEL | short_horizon_hedge3_q1_5d, seasonal_quantile1_20d | SECTOR d6 t0.08 nanOFF |
| `JjGwjd5E` | 1.70 | 1.64 | 0.128 | 0.177 | **0.826** | PV+ANALYST | anl39_spvbq + slippage_at_spread_20 | SECTOR d12 t0.04 nanOFF |
| `pwjpKGJ3` | 1.65 | 1.38 | 0.105 | 0.081 | 0.576 | OTHER | buy_sell_tx_count_ratio_all_60d, buy_sell_ratio_top20_250d | STATISTICAL d10 t0.08 nanOFF |
| `RRA2eE70` | 1.64 | 1.31 | 0.093 | 0.462 | 0.664 | PV+**ANALYST** | **eps_y1_estimate_change_3mo** | INDUSTRY d1 t0.04 nanON |
| `gJZR9XNm` | 1.63 | 1.32 | 0.137 | 0.505 | 0.655 | MODEL | short_term_hedge_signal_5d_q1, seasonal_adjusted_return_20d | SECTOR d6 t0.08 nanOFF |
| `KP78pLWk` | 1.63 | 1.04 | 0.228 | 0.510 | 0.633 | **ANALYST** | **anl44_second_en_eps_value** + **eps_estimate_4wk_change** | INDUSTRY d12 t0.08 nanON |
| `e73Rw8qg` | 1.62 | 1.24 | 0.166 | 0 | **0.510** | **ANALYST** | **anl44_second_en_eps_value** + **pretaxprofit_estimates_down_4w** | SECTOR d16 t0.04 nanOFF |
| `xAY86Mkl` | 1.61 | 0.75 | 0.550 | 0.254 | 0.540 | OTHER | oth496_aftercons_percentage | SECTOR d2 t0.08 nanOFF |
| `ZY0R0mL8` | 1.59 | 1.25 | 0.096 | 0.097 | 0.600 | **ANALYST** | **anl10_smartest_sal/pre_fy1_pred_surps_v0/v1** | SECTOR d2 t0.08 nanON |
| `WjP1ZwMj` | 1.28 | 1.01 | 0.047 | 0.257 | **0.797** | FUNDAMENTAL | fnd94_rt_capex_sales_q, rt_net_mgn_q | SUBINDUSTRY d0 t0.08 nanOFF |

**关键读数**
- `prod` 白空间（<0.70）已被 24 条占据；剩余可插入的 prod 余量极薄，且**新 alpha 必须自证 prod<0.70**。
- `self` 最高到 0.687（`0mre68gv`），说明池内本身已相当拥挤。
- **SHORTINTEREST（shrt38）8 条、FUNDAMENTAL（oth466/fnd94）6 条、MODEL 6 条** 是三大占用重镇。
- **ANALYST 塔只有 3 条纯 analyst 字段的 alpha**：`e73Rw8qg`(1.62)、`KP78pLWk`(1.63)、`ZY0R0mL8`(1.59) —— 且三条都过闸（fail=[]）。

## 四、三条 KOR analyst ATOM 成功范式（可直接复用的骨架，**不是**设置）

| alpha | 骨架 | 字段对 | 设置 |
|---|---|---|---|
| `e73Rw8qg` | `add(ts_rank(vec_avg(A),50), -ts_rank(vec_avg(B),22))` | anl44_second_en_eps_value(水平) + pretaxprofit_estimates_down_4w(下修家数) | SECTOR d16 t0.04 nanOFF |
| `KP78pLWk` | `add(ts_rank(vec_avg(A),50), rank(vec_avg(B)))` | anl44_second_en_eps_value(水平) + eps_estimate_4wk_change(修正) | INDUSTRY d12 t0.08 nanON |
| `ZY0R0mL8` | `add(w1·signed_power(ts_rank(A,66),2.5), w2·group_rank(rank(ts_decay_linear(B,5)),industry))` | anl10 sal_fy1_surps_v0 + pre_fy1_surps_v1 | SECTOR d2 t0.08 nanON |

**共性**：
1. 核心归一化器是 **`ts_rank`（时间维分位）**，不是 `group_rank`（横截面）—— 与我最强的 `9qxGWend`（group_rank×group_rank）不同族。
2. **两条腿互补**：一条「水平/水平分位」，一条「修正/情绪/家数」；不是同一字段的两个窗口。
3. 聚类字段（`anl44_second_en_eps_value` aC=104、`pretaxprofit_estimates_down_4w` aC=43）反而是赢家 —— **拥挤 ≠ 无信号，拥挤 = 信号肥沃**。
4. decay 跨度 2–16、trunc 0.04–0.08、nan ON/OFF 都有成功案例 ⇒ 设置自由度大，**骨架与字段对才是决定项**。

## 五、analyst44 字段占用盘点

**已占用**（不得再用作主腿）：`anl44_second_en_eps_value`(aC104)、`pretaxprofit_estimates_down_4w`(aC43)、`eps_estimate_4wk_change`(aC5)、`eps_y1_estimate_change_3mo`(不在本集)。

**净字段（VECTOR，cov 1.0，aC 0–3）**：
`ffops_4week_consensus_change`(0)、`net_debt_4week_up_revisions`(0)、`net_debt_4week_down_revisions`(0)、`bps_4week_consensus_change`(0)、`bps_consensus_change_percent`(0)、`eps_estimate_stddev`(0)、`anl44_best_dps_hi`(0)、`anl44_best_dps_stddev`(0)、`pretaxprofit_change_percent`(1)、`sales_estimate_change_percent`(1)、`anl44_best_dps_lo`(1)、`eps_gaap_estimate_4wk_change`(1)、`roe_4week_consensus_change`(3)。

另可从预检 `vector_fields` 白名单扩容（尚未测过、命名成体系）：
`anl44_best_eps_hi/lo/median/stddev`、`anl44_best_eps_4wk_chg/up/dn`、`anl44_best_dps_4wk_chg/up/dn`、
`bps_estimate_standard_deviation`、`ffops_estimate_standard_deviation`、`pretaxprofit_estimate_stddev`、
`roe_estimate_standard_deviation`、`sales_estimate_standard_deviation_3`、`net_debt_estimate_stddev`、
`eps_estimate_4wk_down_count`、`eps_gaap_estimate_4wk_up/down_count`、`bps_num_estimates_up/down_4w`、
`ffops_num_estimates_up/down_4w`、`roe_num_estimates_up/down_4w`、`pretaxprofit_estimates_up_4w`、
`sales_upward_revisions_4w`、`sales_downward_revisions_4w`、`roa/roe/pretaxprofit_to_sales_ratio`、
`price_to_earnings_ratio_estimate`、`price_to_book_value_per_share_ratio`、`price_to_cashflow_per_share_ratio`。

> 大白空间 = **分歧度族（stddev × 7 种口径）** 与 **家数族（num_estimates_up/down × 6 种口径）** —— 这两族在 OS 池里**一条都没出现**。

## 六、wave277 设计（10 条 / 2 批，maxTrade **OFF**）

统一设置：**SECTOR / decay 12 / trunc 0.04 / nan ON / maxTrade OFF / unit VERIFY**
（decay+trunc 抄 `e73Rw8qg`，nan 翻 ON 因为全部 cov 1.0；不抄 nanOFF，wave276 已证明它在此类字段上有害）

### 批 A `3Cpkiy2th5kfaGdt4CIVbQ0`（5 条：分歧交互 + 骨架换腿）
| # | 模板 | 表达式 |
|---|---|---|
| A1 | 单位分歧修正（T1） | `group_rank(divide(vec_avg(eps_estimate_4wk_change), vec_avg(eps_estimate_stddev)), sector)` |
| A2 | 全净字段版单位分歧（T1'） | `group_rank(divide(vec_avg(ffops_4week_consensus_change), vec_avg(anl44_best_dps_stddev)), sector)` |
| A3 | 水平 × 股息下限（T2，e73 骨架换腿） | `add(ts_rank(vec_avg(anl44_second_en_eps_value),50), -ts_rank(vec_avg(anl44_best_dps_lo),22))` |
| A4 | 干净二阶差分（T3） | `group_rank(ts_delta(vec_avg(bps_4week_consensus_change),22), sector)` |
| A5 | e73 骨架换第二腿（T4） | `add(ts_rank(vec_avg(eps_estimate_4wk_change),50), -ts_rank(vec_avg(net_debt_4week_up_revisions),22))` |

### 批 B `40yFJz7VH4DJaytgA0DehI5`（5 条：家数族 + 分歧带 + 一致性）
| # | 模板 | 表达式 |
|---|---|---|
| B1 | 债务修正净额（T5，家数族） | `add(ts_rank(vec_avg(net_debt_4week_down_revisions),50), -ts_rank(vec_avg(net_debt_4week_up_revisions),22))` |
| B2 | 股息预期带（T6） | `add(ts_rank(vec_avg(anl44_best_dps_hi),50), -ts_rank(vec_avg(anl44_best_dps_lo),22))` |
| B3 | 双修正共振（T7） | `add(ts_rank(vec_avg(pretaxprofit_change_percent),50), ts_rank(vec_avg(roe_4week_consensus_change),22))` |
| B4 | 股息分歧形状（T8） | `group_rank(divide(subtract(vec_avg(anl44_best_dps_hi), vec_avg(anl44_best_dps_lo)), vec_avg(anl44_best_dps_stddev)), sector)` |
| B5 | 修正一致性（T9，**被闸后替换**） | `group_rank(ts_corr(vec_avg(eps_estimate_4wk_change), vec_avg(sales_estimate_change_percent), 66), sector)` |

**B5 被静态闸拦下的记录**：原稿移植 `ZY0R0mL8` 的 `add(0.6·leg1, 0.4·leg2)` 被
`toolkit_static` 判 `[POISON] 命中毒模式 weighted_leg_mix_func_prefix`，整批拒绝。
⇒ **加权混腿在本工作区一律禁**（与用户「禁 add(A,B) 等权双腿」纪律同源），
已改用 `ts_corr` 一致性骨架（结构不同，不混腿）。

## 七、纪律沉淀

1. **设置不可移植**：A 表达式上的最优设置，搬到 B 表达式可能把 S 砍半（实测 −57%）。设置必须在目标表达式上标定。
2. **先测 self 相关性再谈 S**：S1.48 的候选 self 0.73 直接判死，省掉后续所有算力。
   `check_self_correlation` 是纯本地计算，不占平台相关性槽，应当作为 **S≥1.3 候选的第一道筛**。
3. **字段归属必须先查快照**：`eps_revision_magnitude`/`eps_y1_estimate_change_3mo` 不在 analyst44，
   我此前把它们当同集字段用，导致「ATOM」判定错误、跨集混字段。
4. **拥挤字段（aC 40–104）是赢家聚集地**：三条 analyst ATOM 全用 `anl44_second_en_eps_value`(aC104)
   或 `pretaxprofit_estimates_down_4w`(aC43)。aC=0 的净字段反而长期停在 S≤1.1。
5. **白空间假设**：分歧度族（stddev×7）与家数族（num_up/down×6）在 32 条 OS 池里零占用 —— wave277 的 A1/A2/B1/B4 即为此假设的首次检验。

---

## 八、论坛 + 文献取证（启用分歧度族 / 家数族前按要求查证）

**论坛（BRAIN 中文社区，检索「分析师 分歧 预期修正」/「revision breadth analyst count」）**

| 帖 | 要点 | 对本轮的直接支持 |
|---|---|---|
| 【因子灵感】分析师预期修正，怎样分离方向与参与广度（XH93773, 29 赞） | 「少数观点的大幅调整」与「多数观点的小幅同向调整」对应**不同的信息过程**；先在 CN/JPN 验证，需核对覆盖数及更新时间，防止少量高覆盖公司主导 | 正是 `magnitude` vs `breadth` 二分；也提示 **coverage 与更新时间必须核**（对应我 nan/覆盖率闸） |
| 【Alpha Idea】分析师盈利预期修正广度（ZZ43261, 36 赞 5 评） | 「修正的幅度」容易被一两个极端预测带偏；**「修正的广度」——多少分析师上调/下调——更能反映一致预期的方向性变化** | 直接支持 B1（净债务下修/上修家数）与家数族白空间假设 |
| 分析师数据的正确打开方式:预期差与修正（WL27618, 30 赞） | 「绝对水平不重要，变化才重要」；市场早已消化水平，有信息量的是「预期往哪动」 | 支持把 `change`/`revision` 而非 `level` 当主腿 |
| 【Alpha灵感】分析师预测分歧度——从一致预期的收敛中寻找Alpha | 从一致预期的收敛过程找 alpha | 支持 A1（修正 / 分歧度）与 A2、B4 |

**文献（web 检索）**

| 论文 | 结论 | 用法 |
|---|---|---|
| *Investor disagreement and state-dependent mispricing: New evidence on the analyst dispersion anomaly* | 分歧度异常是**状态依赖**的：高分歧在卖空受限/高散户参与状态下定价错误更大 | 解释为何分歧度信号在 KOR（散户占比高、卖空受限）可能强于美股 |
| *The forecast dispersion anomaly revisited: Time-series forecast dispersion and the cross-section of stock returns* | 区分**横截面分歧**与**时序分歧**，时序分歧的预测力更稳 | ⇒ 分歧度不该只用横截面 stddev，应做 `ts_rank`/`ts_delta` 版本（wave278 T4/T5 采用） |
| *What Drives the Dispersion Anomaly?* (Min, Qiu, Roh) | 分歧度异常主要来自**套利限制 + 卖空成本**，而非纯风险补偿 | 方向先验：高分歧 → 后续低收益（**空高分歧**），A1 的「修正/分歧」正号与之相容 |

**取证结论**：三个机制（分歧度、修正广度、创新/羊群分解）都有论坛 + 学术双重支撑，不是凭直觉设骨架。

## 九、wave278 预设计：analyst10「创新 / 羊群分解」白空间（OS 池零占用）

`analyst10` 640 字段，含一套**分析师创新分解**：同一目标（pre / sal / dps）× FY1/FY2 × 四象限
`innovate_increase` / `innovate_decrease`（创新性修正家数）与 `normal_increase` / `normal_decrease`（羊群修正家数），
外加 `innovation_score`、`revise_value`、`revise_ratio_to_consensus`。
**32 条 OS 池里这套字段一条都没出现** —— 唯一用到的 anl10 字段是 `smartest_sal/pre_fy1_pred_surps`（`ZY0R0mL8`）。

精确字段（全部 MATRIX，无需 vec_*）：
- `anl10_analyst_innovation_pre_innovate_increase_fy1`(cov .6551, aC1) / `_decrease_fy1`(cov .6551, aC12)
- `anl10_analyst_innovation_pre_normal_increase_fy1`(aC1) / `_normal_decrease_fy1`(aC2)
- `anl10_analyst_innovation_pre_innovation_score_fy1`(cov .6551, aC13) / `_fy2`(cov .6284, aC2)
- `anl10_preinnovation_score_fy1_7809`(cov .6417, aC19)
- `anl10_prerevise_ratio_to_consensus_fy1_7803`(cov .6733, aC16) / `_fy2_7804`(aC1) / `_fq1_7817`(aC0)
- `anl10_smartest_sal_fy2_pred_surps_v1`(cov .8326, aC11) / `anl10_smartest_sal_fq1_pred_surps_v0`(aC10)
- `anl10_smartest_ebi_fy1_pred_surps_v0`(cov .9523, aC12) / `anl10_smartest_net_fy1_pred_surps_v1`(aC10)

12 个结构互异模板（差异落在骨架 / 矩 / 期限 / 分组轴 / 非线性）：

| # | 模板 | 骨架 | 结构差异点 |
|---|---|---|---|
| T1 | 创新净广度 | `group_rank(subtract(inc,dec),sector)` | 家数差（一阶） |
| T2 | 创新超额 vs 羊群 | `subtract(group_rank(subtract(inc,dec),sector), group_rank(subtract(ninc,ndec),sector))` | 同源价差（基本面裁定放行） |
| T3 | 创新动量 | `group_rank(ts_delta(subtract(inc,dec),22),sector)` | 二阶差分 |
| T4 | 创新分数时序分位 | `ts_rank(anl10_analyst_innovation_pre_innovation_score_fy1,66)` | 时序分位（文献：时序分歧更稳） |
| T5 | 期限斜率 | `subtract(ts_rank(score_fy1,50), ts_rank(score_fy2,22))` | FY1−FY2 期限结构 |
| T6 | 共识偏离水平 | `group_rank(anl10_prerevise_ratio_to_consensus_fy1_7803,sector)` | 水平（revise/consensus 比） |
| T7 | 共识偏离期限结构 | `subtract(rank(rr_fy1), rank(rr_fy2))` | 期限 × 横截面 |
| T8 | FY2 迟滞 surprise | `group_rank(anl10_smartest_sal_fy2_pred_surps_v1,sector)` | 换期限（OS 池只有 FY1） |
| T9 | FY1/FY2 surprise 斜率 | `subtract(group_rank(sal_fy2, sector), group_rank(sal_fy1, sector))` | 两期限同源价差 |
| T10 | 销量×利润创新背离 | `subtract(group_rank(sal_net,sector), group_rank(pre_net,sector))` | 跨目标（sal vs pretax）背离 |
| T11 | 羊群反转 | `group_rank(subtract(ndec,ninc),sector)` | 反向（羊群下修少=好） |
| T12 | 事件门控 | `trade_when(greater(subtract(inc,dec),0), group_rank(subtract(inc,dec),sector), -1)` | 门控（只在有创新上修时下注） |

**nan 处理分歧（必须实测）**：cov 0.63–0.67 的 MATRIX 字段，
nan ON 把「无数据」填 0（对**家数字段**语义正确：0 个创新修正；对**连续分数**语义错误：0 分 = 与共识持平）。
⇒ 计划拆两批对照：家数族（T1/T2/T3/T10/T11）用 nan ON，连续分数族（T4–T9）用 nan ON + `ts_backfill(x,66)` 兜底，
用同一机制的两组读数直接量出 nan 口径的影响。

## 十、wave279 预设计：三集「从没测过」的白空间（S1 扫描表复核后重排优先级）

`docs/reference/kor_analyst_dataset_scan_20261106.md` 的 17 集表里，有三个集**历史回测次数为 0–3**，
而我把前几波全押在 `analyst44`（42 次）与 `analyst10`（105 次）上 —— 拥挤度选错了方向。重排如下：

| 数据集 | 字段数 | aC=0 字段 | 历史回测 | 为什么值得打 |
|---|---:|---:|---:|---|
| `analyst9` | 48 | 9 | **0** | 教科书级**修正广度原语**：`daily_numup`(aC11)/`daily_numdn`(7)/`daily_numupunfiltered`(8)/`daily_numdownunfiltered`(10)/`daily_numanalysts`(1)/`daily_numanalystall`(0)，日频刷新。论坛 36 赞帖的「广度优于幅度」正是它 |
| `analyst_base_ref` | 14 | 3 | **0** | 唯一**惊喜专集**：`consensus_surprise_percentage`(aC27)、`consensus_vs_actual_diff`(8)，且 `consensus_stddev_estimate`(aC0)、`num_estimates_consensus`(aC0)、`reported_actual_value`(aC0) 全未被用 |
| `analyst_consensus` | 2343 | **2147** | **0–3** | 白空间王，把 consensus 与 actual 全对齐；revision/surprise 面几乎空白（待后续波） |

**wave279 表达式（已预检 valid，unknown=[]）**

analyst9（VECTOR，cov 0.4433 ⇒ nan 口径是生死项）：
| # | 模板 | 表达式 |
|---|---|---|
| U1 | 净广度 | `group_rank(subtract(vec_avg(anl9_daily_numup), vec_avg(anl9_daily_numdn)), sector)` |
| U2 | 广度占分析师总数（归一） | `group_rank(divide(subtract(vec_avg(anl9_daily_numup), vec_avg(anl9_daily_numdn)), vec_avg(anl9_daily_numanalysts)), sector)` |
| U3 | 广度动量 | `group_rank(ts_delta(subtract(vec_avg(anl9_daily_numup), vec_avg(anl9_daily_numdn)), 22), sector)` |
| U4 | 上修占比 | `group_rank(divide(vec_avg(anl9_daily_numup), vec_avg(anl9_daily_numanalystall)), sector)` |
| U5 | unfiltered 净广度 | `group_rank(subtract(vec_avg(anl9_daily_numupunfiltered), vec_avg(anl9_daily_numdownunfiltered)), sector)` |

analyst_base_ref（VECTOR，cov 0.6683，事件型）：
| # | 模板 | 表达式 |
|---|---|---|
| V1 | 惊喜水平 | `group_rank(vec_avg(consensus_surprise_percentage), sector)` |
| V2 | 惊喜持续性 | `group_rank(ts_mean(vec_avg(consensus_surprise_percentage), 66), sector)` |
| V3 | 变异系数（分歧度，先验应为**负**向） | `group_rank(divide(vec_avg(consensus_stddev_estimate), vec_avg(consensus_mean_estimate)), sector)` |
| V4 | 分歧带形状 | `group_rank(divide(subtract(vec_avg(consensus_high_estimate), vec_avg(consensus_low_estimate)), vec_avg(consensus_stddev_estimate)), sector)` |
| V5 | 覆盖数门控惊喜 | `trade_when(greater(vec_avg(num_estimates_consensus), 3), group_rank(vec_avg(consensus_surprise_percentage), sector), -1)` |

> 前几波在 `analyst44`/`analyst10` 上反复打不上去，除了骨架问题，还有**载体选择问题**：
> 这两集已被回测 42/105 次，是「已经被人踩烂的面」；而 0 次回测的 `analyst9`/`analyst_base_ref` 连一次都没验过。

---

## 十一、wave277 实测结果与归因（2026-11-07）

设置：**SECTOR / decay 12 / trunc 0.04 / nan ON / maxTrade OFF**（用户指令：maxTrade 必须 OFF 才能拿到 investability_sharpe）

### 批 A `3Cpkiy2th5kfaGdt4CIVbQ0`（5/5 全出）
| # | 模板 | alpha | S | F | TO | 2Y | sub | invest | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| A1 | 单位分歧修正 eps/stddev | `npv6AlxE` | **0.97** | 0.71 | 0.0663 | **1.71** | 0.91 | 0.89 | 2 |
| A2 | 全净字段 eps/ffops-stddev | `E56mVM10` | 0.49 | 0.46 | **0.0165** | **2.25** | 0.55 | 0.34 | 3 |
| A3 | e73 骨架换第二腿(dps_lo) | `QPvWYAMQ` | 1.14 | 0.56 | 0.2425 | **0.44** | 0.85 | 0.94 | 3 |
| A4 | bps 二阶差分 | `QPvWYAMW` | 0.86 | 0.60 | 0.0818 | 1.44 | 0.90 | 0.87 | 3 |
| A5 | e73 骨架换腿(net_debt家数) | `VkxMdLV5` | **−0.09** | −0.02 | 0.1417 | 0.02 | −0.25 | −0.26 | 5 |

### 批 B `40yFJz7VH4DJaytgA0DehI5`（5/5 全出）
| # | 模板 | alpha | S | F | TO | 2Y | sub | invest | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| B1 | 债务修正净额（家数族） | `qML5EwqA` | 0.28 | 0.10 | 0.1297 | −0.16 | 0.15 | 0.13 | 5 |
| B2 | 股息预期带 hi−lo | `LLM852JM` | 0.28 | 0.09 | 0.1153 | 0.02 | 0.09 | 0.13 | 5 |
| B3 | 双修正共振 pretax%+roe | `ZYQXm1G1` | 0.08 | 0.01 | 0.1894 | −0.34 | −0.19 | −0.08 | 5 |
| B4 | 股息分歧形状 (hi−lo)/stddev | `6XdGA2O5` | 0.62 | 0.40 | **0.0237** | 1.52 | 0.65 | 0.58 | 3 |
| B5 | **修正一致性 ts_corr(eps,sales,66)** | `WjOYLxmj` | **−1.14** | −0.87 | 0.049 | **−1.64** | −1.06 | −1.03 | 5 |

### 归因（按模板族）
1. **分歧度族不增效**：A1（修正/分歧）S0.97 **低于**同字段纯水平（wave274 `QPvWKYOw` S1.24），A2 全净字段版更差（0.49）。
   ⇒ 「按分歧度缩放修正」在 KOR 是**减速器**不是放大器；学术上的分歧度异常主要在横截面水平上，不在修正缩放上。
2. **家数族（breadth）在 analyst44 上不成立**：B1（net_debt 上/下修家数）0.28、A5（eps 修正 × net_debt 家数）−0.09。
   ⇒ 论坛的「广度优于幅度」在 KOR/analyst44 的**net_debt 口径**上不成立；可能要换到 `analyst9` 的原生 numup/numdn 才有意义（wave279 待验）。
3. **ts_rank 骨架对第二腿极敏感**：A3（e73 骨架换 dps_lo）S1.14 但 **2Y 0.44**；而原版 e73Rw8qg 用 pretaxprofit_down_4w 是 1.62/2Y 稳健。
   ⇒ 「ts_rank 50 + ts_rank 22 价差」不是通用骨架，**第二腿的经济含义必须与第一腿互补**（水平 vs 修正家数），随便换腿会毁掉 2Y。
4. ★ **B5 是本轮唯一真正的新机制信号**：`ts_corr(eps修正, 销售修正, 66)` = **S −1.14 / 2Y −1.64 / TO 0.049 / invest −1.03**。
   强负且换手极低（4.9%），说明「EPS 与销售的修正一致性」是有效的**反向**信号：
   一致性高 = 共识已被充分定价 ⇒ 后续反转。这解释了为什么单纯追修正幅度疲软 —— 市场惩罚的是「同向共振」，不是「修正本身」。
   ⇒ 已派 wave281（8 条）做翻号 + 窗口(22/66/132) + 换腿(pretax/ffops) + 换分组(industry) + 平滑变体，
   设置沿用 SECTOR/d12/t0.04/nan ON 以做**受控对照**。注意：**不允许用 −S 估算翻号收益**（历史实证翻号不对称），必须实派。

### 当前最好（全 campaign）
| alpha | S | F | 2Y | 状态 |
|---|---:|---:|---:|---|
| `9qxGWend` | 1.48 | 1.26 | 1.74 | 判死（self 0.7328 > 0.7，且跨数据集非 ATOM） |
| `kqN8gwzk` | 1.26 | 0.93 | 1.61 | 字段被 ZY0R0mL8 占用 |
| `QPvWKYOw` | 1.24 | 0.97 | 1.88 | 字段被 3 条已提交占用 |
| `QPvWYAMQ` | 1.14 | 0.56 | 0.44 | 2Y 塌 |
| `WjOYLxmj` | −1.14 | −0.87 | −1.64 | wave281 翻号在测 |
| `npv6AlxE` | 0.97 | 0.71 | 1.71 | 分歧度族上限 |

---

## 十二、★ 我漏用的一整类杠杆：中性化档（KOR 11 档实测表）

复盘 `Claude/skills/wq-brain-ra-kor/references/_kor-gatebreak-evidence.md` 发现一个**方法论缺口**：
我这几波把 `neutralization` 固定成 SECTOR（外加测过一次 STATISTICAL 更差），
从来没试过 **FAST / SLOW / REVERSION_AND_MOMENTUM / CROWDING / NONE**。
而 KOR 实证（同一表达式、只改中性化）给出的是：

| 档 | S | F | 2Y | invest | failed_ra |
|---|---:|---:|---:|---:|---:|
| MARKET | 1.53 | 0.94 | 0.97 | 1.14 | 3 |
| REVERSION_AND_MOMENTUM | 1.68 | 0.92 | 1.44 | 1.21 | **2** ★ |
| FAST | **1.84** | 0.88 | 1.55 | 1.09 | 3 |
| SLOW | **1.94** | 0.94 | 1.01 | 1.01 | 3 |
| SLOW_AND_FAST | 1.73 | 0.73 | 1.31 | 0.88 | 3 |
| STATISTICAL | 1.53 | 0.74 | 0.91 | 0.83 | 4 |

**SECTOR→FAST 在同一机制上能带来 +0.3 量级的 S**（1.53→1.84）。我的候选卡在 1.1–1.5，
这批档位正是缺口所在，而我从没测过 —— 这是**最便宜的一段未开发杠杆**。

配套杠杆（同文件实证）：
- **decay**：2 → S1.92 / 2Y1.50；3 → S1.77–1.79 / 2Y1.56–1.58（2Y 峰）；8 → S1.41。**我固定用 4 或 12，落在非最优区**。
- **tail 0.2/0.8 → 0.25/0.75 = 纯改善**（S +0.04、F +0.03）。注意与「tail 0.05/0.95 削尾灾难」是**不同参数、不同结论**，不要混为一谈。
- **group_neutralize(sector) = ★突破**（F +0.12、2Y +0.35、failed_ra 2→0）。
- **禁**：`hump`（S 1.53→0.76）、`ts_mean/ts_decay_linear` 套在 rank 积上（S 1.79→1.15–1.50）、`group_zscore`（2Y 崩）。
- KOR 合法中性化 11 档：NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST。

### wave282 预设计：中性化 × decay 二维标定（在最佳新机制上）
载体 = wave281 里胜出的「修正一致性翻号」表达式（或 wave278/279/280 的最强者），设置扫描：
- 中性化：FAST / SLOW / REVERSION_AND_MOMENTUM / CROWDING / NONE（SECTOR 已有基线）
- decay：2 / 3（配合上面的 11 档里 F 与 2Y 的权衡）
- 可选：`tail(...,lower=0.2,upper=0.8,newval=0.25/0.75)` 包装

> **纪律升级**：以后定设置不要「一次定 SECTOR 然后只在表达式上加算子」。
> 中性化/decay 的 S 弹性（+0.3 量级）与换一个算子的弹性同量级，且成本只有一次回测。



