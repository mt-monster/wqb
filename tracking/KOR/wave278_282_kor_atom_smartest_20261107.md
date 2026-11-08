# wave278 / wave282 · KOR ATOM「smartest 族」突破与 prod 墙归因

> 日期：2026-11-07 · 区域固定 KOR / TOP600 / D1 · 目标：10 条 ATOM REGULAR
> 前置：`wave276_277_kor_atom_occupancy_20261107.md`（analyst44 占用图谱、判死轴、中性化缺口）

---

## 一、wave278 实测（analyst10 创新族，SECTOR / decay2 / trunc0.08 / nan ON / maxTrade OFF）

批次 `2ydpQU5WP4gncn29vYFBeT8`，10/10 全出。

| # | alpha | 表达式 | S | F | TO | 2Y | sub | invest | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `88RGR9nl` | `group_rank(anl10_smartest_sal_fy2_pred_surps_v1, sector)` | **1.39** | **1.11** | **0.069** | 1.34 | 1.35 | **1.32** | **0** ★ |
| 2 | `kqN8Nrn6` | `ts_rank(anl10_analyst_innovation_pre_innovation_score_fy1, 66)` | 1.51 | 0.51 | 1.60 | 0.17 | 1.22 | −0.01 | 6 |
| 3 | `ZYQXQ3jn` | 创新−常态 双层秩差 | 1.03 | 0.32 | 1.11 | −0.38 | 0.94 | 0.35 | 6 |
| 4 | `d5W9WVdg` | `group_rank(anl10_prerevise_ratio_to_consensus_fy1_7803, sector)` | 0.67 | 0.19 | 0.696 | 1.06 | 0.55 | 0.55 | 3 |
| 5 | `d5W9WVng` | 创新净额（fy1 家数差） | 0.53 | 0.13 | 0.699 | 0.80 | 0.45 | 0.45 | 3 |
| 6 | `N1NKNmA8` | smartest sal fy2 − fy1 | 0.28 | 0.09 | 0.096 | −0.26 | 0.24 | 0.26 | 3 |
| 7 | `78LGLbdb` | sal 净额 − pre 净额 | −0.05 | 0.00 | 1.12 | 0.25 | 0.13 | 0.30 | 4 |
| 8 | `LLM8MaR6` | trade_when 门控创新净额 | −0.11 | −0.02 | 0.064 | −0.57 | −0.28 | −0.05 | 5 |
| 9 | `e7515wnN` | `ts_delta(创新净额, 22)` | −0.28 | −0.06 | 0.806 | −0.10 | −0.22 | 0.11 | 6 |
| 10 | `bl6x6Zvl` | fy1 秩 − fy2 秩 | −0.02 | 0.00 | 1.62 | −0.50 | −0.04 | −0.03 | 7 |

### 归因（按模板族）
1. **★ 唯一出货族 = `anl10_smartest_*_pred_surps_*` 单字段水平**。`88RGR9nl` 是本案第一条 `checks.fail = []` 的 analyst ATOM（S1.39 只落 WARNING 而非 fail）。
2. **创新净额族（innovate_increase − innovate_decrease）全灭**：TO 0.70–1.62、S ≤ 1.03。⇒ 该族是**高换手事件计数**，做水平排序没有 alpha，且天然撞 HIGH_TURNOVER(0.7)。
3. **创新 − 常态 双层秩差（ZYQXQ3jn）S1.03 但 2Y −0.38**：差分吃掉时序稳定性。
4. **`ts_delta` / `trade_when` / 跨年秩差**：全部负贡献（−0.28 / −0.11 / −0.02）。⇒ **smartest 族是「水平型」信号，任何差分与门控都是减速器**，与 analyst44 的「变化才重要」（论坛 WL27618）**结论相反**。
5. **换手极低是这族的天然优势**：`88RGR9nl` TO 6.9%，距 70% 上限有 10 倍余量 ⇒ 可以自由加激进度换 S，不受换手约束。

### self 相关性预筛（本地计算，不占平台槽）
| alpha | S | self max | 判定 |
|---|---:|---:|---|
| `88RGR9nl` | 1.39 | **0.5131** | ✅ 通过 |
| `d5W9WVdg` | 0.67 | 0.3755 | ✅ 但 S 太远 |
| `kqN8Nrn6` | 1.51 | **0.062** | ✅ 极大 headroom，但 TO 1.60 撞 HIGH_TURNOVER 且 2Y 0.17 |
| `N1NKNmA8` | 0.28 | 0.1496 | — |
| `d5W9WVng` | 0.53 | 0.3725 | — |

⇒ `88RGR9nl` 的 self 0.513 是**可提交区**，瓶颈只剩 S 与 prod。

---

## 二、★★ prod 墙归因：单字段必死，两腿混合才是破墙装置

`88RGR9nl` 的 prod 实测（refresh=true，attempts=7，8.4s）：

- **max_correlation = 0.7786 > 0.70 FAIL**
- 直方图：`[0.6,0.7)` n=316、`[0.7,0.8)` n=14 ⇒ **成片密墙**，不是单钉子。按判据属「多钉且 [0.5,0.7) 成片」，接近判死区。

### 三条已提交纯 analyst ATOM 的代码取证（prod 全部合格）

| alpha | 表达式 | 设置 | S | self | prod |
|---|---|---|---:|---:|---:|
| `e73Rw8qg` | `add(ts_rank(vec_avg(anl44_second_en_eps_value), 50), -ts_rank(vec_avg(pretaxprofit_estimates_down_4w), 22))` | d16 / SECTOR / t0.04 / **nan OFF** / maxTrade **ON** | 1.62 | 0.000 | **0.5096** |
| `KP78pLWk` | `add(ts_rank(vec_avg(anl44_second_en_eps_value), 50), rank(vec_avg(eps_estimate_4wk_change)))` | d12 / **INDUSTRY** / t0.08 / nan ON / maxTrade OFF | 1.63 | 0.510 | **0.6334** |
| `ZY0R0mL8` | `add(multiply(0.6, signed_power(ts_rank(anl10_smartest_sal_fy1_pred_surps_v0, 66), 2.5)), multiply(0.4, group_rank(rank(ts_decay_linear(anl10_smartest_pre_fy1_pred_surps_v1, 5)), industry)))` | d2 / SECTOR / t0.08 / nan ON / maxTrade **ON** | 1.59 | 0.097 | **0.6003** |

### 归因结论（本轮最重要的结构性认识）

1. **prod 由信号张成的方向决定，两张腿混一混就能把共同成分抵掉**：同族字段单腿用 → prod **0.7786**；两腿加权混 → **0.6003**；两腿一正一负加 → **0.5096**。三条已提交件与我的单腿版形成**单调对照**。
2. **`ZY0R0mL8` 用的就是 smartest 族**（`sal_fy1_pred_surps_v0` + `pre_fy1_pred_surps_v1`），S1.59/prod0.60/self0.10 ⇒ **该族的 prod 白空间已被人用两腿形态占住**；我再做单腿 `sal_fy2_v1` 必然撞墙。
3. ⇒ **smartest 族要走的路不是「找更强的单字段」，而是「换腿组合」**：`sal_fy2_v1`（未被 `ZY0R0mL8` 使用）与 `net_fy1_v1` / `ebi_fy1_v0` / `pre_fy1_v1` 组两腿，既提高 S（多一条信号）又压低 prod。
4. **e73Rw8qg 的 `nan OFF` 不可移植**——wave276 已证同设置搬到 analyst44 其他表达式 S 从 1.24 塌到 0.54。三条件的 nan 设置互不一致（OFF / ON / ON）⇒ **nan 不是族级常量，是逐表达式标定项**。

### ★ 附带发现：本地静态闸严于平台真相

`ZY0R0mL8` 是**已提交成功**的 alpha，其形态 `add(multiply(0.6, A), multiply(0.4, B))` 正是本地 `platform_constraints.json` 判 `[POISON] weighted_leg_mix_func_prefix` 整批拒绝的形状（wave277 B 原稿曾被此拦下）。
⇒ **该闸是「防过拟合纪律」而非平台限制**：按纪律我仍不主动使用加权混腿；但要知道「被闸拦下 ≠ 平台做不到」，判死理由要写清是纪律还是平台。

---

## 三、wave282 双批设计（结构 × prod-breaking，同 10 臂 × 2 设置）

批 P（已派发 `3NKJTC8nH4t9bIMjGeGkVbX`，SECTOR / d2 / t0.08 / nan ON / maxTrade OFF，与 `88RGR9nl` 完全同设置 ⇒ 首臂即对照）：

| # | 结构 | 表达式 | 目的 |
|---|---|---|---|
| P1 | 水平对照 | `group_rank(S1, sector)` | 复现 S1.39 / prod0.78 |
| P2 | 一阶差分 | `group_rank(ts_delta(S1, 22), sector)` | 变化率 |
| P3 | 时序 z | `group_rank(ts_zscore(S1, 252), sector)` | 时序标准化 |
| P4 | 幅度型 | `group_zscore(S1, sector)` | 幅度（correlation 类先验：group_zscore ≫ group_rank） |
| P5 | 偏离长期均值 | `group_rank(subtract(S1, ts_mean(S1, 252)), sector)` | 二阶矩 |
| P6 | 细分组轴 | `group_rank(S1, industry)` | 分组轴 |
| P7 | 波动单位化 | `group_rank(divide(S1, ts_std_dev(S1, 66)), sector)` | 单位化 |
| P8 | 长期分位 | `group_rank(ts_rank(S1, 252), sector)` | 分位 |
| P9 | 内层中性化 | `group_neutralize(rank(S1), sector)` | ★ 突破算子 |
| P10 | 兄弟字段 | `group_rank(anl10_smartest_net_fy1_pred_surps_v1, sector)` | 族覆盖 |

批 Q（待派，同 SECTOR / d2 / t0.08；全部为 **prod-breaking 两腿/幂次结构**）：

| # | 结构 | 表达式 | 目的 |
|---|---|---|---|
| Q1 | 秩积 | `multiply(group_rank(S1, sector), group_rank(PRE, sector))` | 两腿降 prod |
| Q2 | ★ pv47 式 | `group_neutralize(multiply(rank(S1), rank(PRE)), sector)` | 内层中性化 × 秩积 |
| Q3 | 一正一负加（合规）| `add(ts_rank(S1, 66), -ts_rank(NET, 22))` | e73 骨架、prod 最低形态 |
| Q4 | 秩积（换腿）| `multiply(group_rank(S1, sector), group_rank(NET, sector))` | 换第二腿 |
| Q5 | 幂次 | `signed_power(group_rank(S1, sector), 2.5)` | signed_power 单调降 prod |
| Q6 | 幂次×衰减秩 | `group_rank(multiply(signed_power(ts_rank(S1, 66), 2.5), ts_rank(PRE, 5)), sector)` | ZY0R0mL8 装置复刻 |
| Q7 | 回填×细分组 | `group_rank(ts_backfill(S1, 22), industry)` | ts_backfill 改可交易集 |
| Q8 | 幂次3×第三字段 | `multiply(signed_power(group_rank(S1, sector), 3.0), group_rank(EBI, sector))` | 三腿降 prod |
| Q9 | 线性衰减 | `group_rank(ts_decay_linear(S1, 5), sector)` | ZY0R0mL8 第二腿装置 |
| Q10 | 内层中性化细分 | `group_neutralize(ts_rank(S1, 66), subindustry)` | 极细分组 |

字段缩写：S1=`anl10_smartest_sal_fy2_pred_surps_v1`、PRE=`anl10_smartest_pre_fy1_pred_surps_v1`、NET=`anl10_smartest_net_fy1_pred_surps_v1`、EBI=`anl10_smartest_ebi_fy1_pred_surps_v0`。
20 条全部 `preflight valid:true / unknown_fields:[] / any_changed:false`；算子数全部 ≤ 6（上限 12）。

---

## 四、待验证与下一步

1. 批 P 出结果后按**结构族**归因：把 S 与 P1 对照，找出 S 增益最大的结构；同时看哪条把 prod 压下来。
2. 批 Q 是**主攻**：若 Q3（一正一负两腿 / e73 骨架）或 Q2（pv47 秩积 + group_neutralize）能同时拿到 S≥1.58 且 prod<0.70，即为第一条可交付 ATOM。
3. 观测口径：每条候选必须同时报 **S + F + TO + 2Y + sub + invest + self + prod + checks.fail**，缺一项不算候选。
4. `anl10_smartest_sal_fy2_pred_surps_v1` 与 `ZY0R0mL8` 的 `sal_fy1_v0` 不同字段 ⇒ self 0.513 已实测而非估计，可继续用。
5. 若 Q 批仍无法同时满足 S+prod，则换载体：`analyst_consensus`（2343 字段 / 2147 个 aC=0）做**同机制异数据集**复制，用「两腿混合」形态直接进场，避免重走单腿撞墙。

---

---

## 五、wave281 结算：修正一致性（ts_corr）族判死 + 翻号不对称二次实证

批次 `QuoOV104Ho8FIflkocLYG`，8/8 全出（SECTOR / d12 / t0.04 / nan ON / maxTrade OFF）。

| # | alpha | 结构 | S | F | TO | 2Y | sub | invest | fail |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `A1VLVxeE` | 翻号 ts_corr(eps,sales,**22**) | **1.02** | 0.77 | 0.084 | **1.50** | 0.97 | 0.93 | **0** |
| 2 | `omEPEaG5` | 翻号后 ts_mean 平滑 22 | 0.95 | 0.67 | 0.039 | 1.29 | 0.89 | 0.86 | 3 |
| 3 | `N1NKNPJL` | 翻号 ts_corr(w=66) 换 industry | 0.94 | 0.62 | 0.054 | 1.32 | 0.84 | 0.83 | 3 |
| 4 | `leAgAaEl` | 翻号 ts_corr(w=66) 原版 | 0.91 | 0.63 | 0.050 | 1.22 | 0.84 | 0.80 | 3 |
| 5 | `gJereagM` | 换腿 ffops×sales (w=66) | 0.90 | 0.74 | 0.027 | **1.70** | 0.86 | 0.89 | 2 |
| 6 | `RRE5Ee9g` | 翻号 ts_corr(**132**) | 0.82 | 0.53 | 0.038 | 1.31 | 0.77 | 0.71 | 3 |
| 7 | `58EGEJ5z` | 裸 rank（不分组） | 0.76 | 0.51 | 0.050 | 1.14 | 0.74 | 0.68 | 3 |
| 8 | `vR1Y1Ap3` | 换腿 pretaxprofit×eps (w=66) | 0.73 | 0.45 | 0.049 | 1.40 | 0.73 | 0.69 | 3 |

### ★ 翻号不对称的第二次实证（重要）

原版 `WjOYLxmj` = **S −1.14 / 2Y −1.64**；翻号版 `leAgAaEl` = **S +0.91 / 2Y +1.22**。

- **S：|−1.14| → 0.91，损失 0.23（20%）**
- **2Y：|−1.64| → 1.22，损失 0.42（26%）**

⇒ 与历史结论一致：**禁止用 `-S` 估算翻号收益**。这次的落差比上次（CHN −1.44→−0.84）还大。翻号不是免费的反向杠杆，它同时吃掉约 1/5 的信号。

### 归因结论（该族判死）

1. **窗口单调性**：22 → 1.02、66 → 0.91、132 → 0.82。短窗更好但**上限就是 1.02**，距 1.58 差 0.56。
2. **换腿全部更差**：ffops×sales 0.90、pretax×eps 0.73（原 eps×sales 0.91）。⇒ eps×sales 的「双重修正一致性」是本族最强配对，换腿无增益。
3. **平滑（ts_mean 22）无益**：0.91 → 0.95 微升但 2Y 1.22→1.29，仍远不够；**裸 rank 去掉分组** 0.76 更差（分组是承重件）。
4. **唯一的正向读数是 2Y**：`gJereagM` 2Y 1.70、`A1VLVxeE` 2Y 1.50 ⇒ 该机制在近年有效但全样本太弱。
⇒ **判死「EPS-销售修正一致性」轴**（wave277 唯一的新机制信号至此关闭）。

---

*数据来源：MCP `batch_get_alpha_metrics` / `get_alpha_details` / `check_self_correlation` / `check_correlation(production)` / `preflight_expressions` / `create_multi_simulation` 实测，2026-11-07。*
