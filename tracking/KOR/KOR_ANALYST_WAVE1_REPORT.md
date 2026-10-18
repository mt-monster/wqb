# KOR Analyst 战役 — Wave 1 结算（36 条全灭，但诊断出 4 条活苗）

- 区域：**KOR / TOP600 / D1**（全程锁定，未换 region）
- 设置：`decay=4` `neutralization=STATISTICAL` `truncation=0.08` `nanHandling=OFF` `maxTrade=OFF` `unitHandling=VERIFY`
- 区间：2014-01-01 ~ 2023-12-31（FULL）
- 金字塔：全部命中 `KOR/D1/ANALYST`（multiplier **1.6**）—— 白名单选对了

## 一、活苗（只差 2–3 闸，进 Wave2）

| alpha id | 机制 | S | fit | TO | sub-S | 2Y-S | failed_ra | 缺哪些闸 |
|---|---|---|---|---|---|---|---|---|
| `A1QdnZwg` | 一致预期意外百分比 | **1.11** | 0.65 | 0.10 | 0.66 | 0.79 | 3 | LOW_SHARPE / LOW_FITNESS / LOW_2Y |
| `e76JdWZE` | FY2 EPS 3月修正 | 0.91 | 0.55 | 0.12 | **1.06** | 0.17 | 3 | 同上 |
| `omoenmZm` | 目标价分歧收敛(30d) | 0.74 | 0.37 | 0.15 | 0.73 | 0.57 | 3 | 同上 |
| `9qEQa2Or` | FY1 EPS 3月修正 | 0.63 | 0.32 | 0.12 | 0.62 | 0.41 | 3 | 同上 |

四颗共同点：**`CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_INVESTABILITY` 全部 PASS**，只被「强度不够」卡住 ⇒ 属可破闸类型，不是结构死。

## 二、失败指纹（决定 Wave2 方向）

### 1. `analyst_base_ref` 的 DISP 族在 KOR 基本无效（**反直觉**）
论坛主配方（分歧度收敛）在 KOR 失效：

| 表达式 | S | 说明 |
|---|---|---|
| `group_rank(stddev/mean)` DISP水平 | **-0.12** | 方向为负 |
| `group_rank((high-low)/mean)` | -0.12 | 同 |
| `group_zscore(ts_delta(DISP,30))` 收敛 | -0.05 | 加了收敛也救不回 |
| `stddev/mean` 用 20/30 期平滑分母 | 0.13 | 仍近零 |

⇒ **结论：KOR 的分歧度水平本身无横截面定价，分歧收敛也无**。与论坛（USA/EUR 口径）的差异可能来自 KOR 分析师覆盖结构。

### 2. `analyst_base_ref` 覆盖稀疏 → `CONCENTRATED_WEIGHT=1.0` 直接死
所有用 `vec_avg(consensus_*)` 的：`longCount=6` / `shortCount=6`，`CONCENTRATED_WEIGHT=1.0`（限 0.1）。
**唯一例外**是 `consensus_surprise_percentage`（uc=15，覆盖好）→ longCount 322/316 ⇒ **该数据集内只有 surprise 类字段可用，其余 9 个字段全部稀疏不可用**。

### 3. `analyst_consensus` 的目标价/长期EPS 族：部分可用
- ✅ `stddev_estimate_targetprice_annual12_tribes` + `mean_...`（S=0.18 水平 / **0.74 收敛**）
- ✅ `max/min/mean_estimate_targetprice_annual12_tribes` 区间收敛（S=0.58, sub=0.71）
- ❌ `stddev/mean/median_estimate_eps_longterm`（S=-0.27 ~ -0.20，全负）
- ❌ 偏度 `skew` 类在两个数据集**全部近零**（-0.26 ~ 0.49）⇒ **KOR 不吃 EstimateSkew，论坛第 5 信号在 KOR 无效**

### 4. `analyst_factor_signals` 方向分裂（必须正反都测）
- ✅ **修正类正向**：`eps_y1/y2_estimate_change_3mo`(0.63/0.91)、`eps_revision_magnitude`(0.37)、`revenue_estimate_trend_slope_1yr`(0.36)
- ✅ **意外类正向**：`eps_surprise_stddev`(0.17)
- ❌ **CAGR 类反向**：`eps_y1_cagr_2yr`(**-0.69**)、`eps_y1_cagr_5yr`(-0.70) ⇒ 高 CAGR 在 KOR 是负向
- ❌ `eps_estimate_trend_slope_1yr`(-0.38)、`eps_q1_estimate_sequential`(-0.31)、`eps_q1/y1_estimate_skewness`(-0.26/0.02)

### 5. `analyst81` 信用违约族全负
`anl81_probability_of_default_percent` S=-0.34、`default_likelihood_percent` S=-0.40。
⇒ **违约概率高 = 负向**，直接 `group_rank` 方向错；若要救需 `negate`，但强度不够（|S|<0.5 无救）。

### 6. 覆盖数（num_estimates）无信号
`vec_avg(num_estimates_consensus)` S=-0.07、`estimate_count_eps_longterm` S=-0.07 ⇒ 论坛建议的「覆盖数做质量过滤」在 KOR 不能当独立信号，只能当门控。

## 三、Wave2 破闸设计（33 条）

针对上述指纹：
- **A1QdnZwg（surprise）**：signed_power 2/3 压尾、`ts_decay_linear` 平滑（保 robust）、`ts_delta` 取变化、`trade_when(rank(adv20)>0.5)` 提集中度、`negate` 测反方向、`winsorize`、`ts_mean(22)`。
- **e76JdWZE / 9qEQa2Or（EPS 修正）**：signed_power、ts_delta、ts_decay_linear、ts_mean(10)、门控、rank vs zscore。
- **omoenmZm（目标价分歧收敛）**：**signed_power 2 / 2.5**（2.5 是 IS 最优点，且 prod 在 2.5–4.0 平坦）、收敛窗 10/30/60、先 `ts_mean(10)` 再 delta（降噪）、winsorize。
- 反向验证：`w2_tpd_neg`、`w2_epsdisp_neg`、`w2_y2_neg`、`w2_surp_z_neg`。

## 四、可复用结论（写回 skill reference）

1. **KOR/D1/ANALYST 塔 multiplier = 1.6**（KOR 现有塔里最高之一），Analyst 语义数据在 KOR 是有效矿脉。
2. **论坛主配方（DISP 收敛）不可跨区照搬**：USA/EUR 有效，**KOR 无效甚至反向**。分析师覆盖结构差异会让同一机制换向。
3. **KOR 的 DISP 水平类（stddev/mean）一律负向** ⇒ 若要用必须 `negate`；但 negate 后 |S| 仍 <0.15，不值得投。
4. **EstimateSkew（mean−median 归一）在 KOR 全线无效**（两数据集 n=4 全部 |S|<0.5，两条近零）。
5. **EPS 预期 CAGR 在 KOR 是负向信号**（-0.7），与 USA 的成长动量直觉相反。
6. **稀疏 VECTOR 字段的 `CONCENTRATED_WEIGHT=1.0` 是数据集级判决**：同一数据集内先按 `userCount` 排，覆盖好的字段（uc≥15）才值得投。`analyst_base_ref` 只有 `consensus_surprise_percentage` 通过此判。
7. **2Y 闸普遍是最大杀手**：Wave1 四条活苗 2Y_S 全在 0.17–0.79，远低于 1.58 ⇒ KOR 的 2022–2023 段（AI 半导体行情）与分析师预期类信号**不同步**，这是 KOR 特有的结构性障碍，需专门用 `ts_decay_linear` / `hump` 拉长持仓去适配。
---

# Wave 2 中期结算（已收 12 / 33 条）

## 一、三条最重要的可复用结论

### ★★★ 1. `group_rank` 之前的 `signed_power` = 完全白用
| 表达式 | S | fit | TO | sub | 2Y |
|---|---|---|---|---|---|
| `group_rank(SURP, industry)` | 1.11 | 0.65 | 0.1007 | 0.66 | 0.79 |
| `group_rank(signed_power(SURP, 2), industry)` | **1.11** | **0.65** | **0.1007** | **0.66** | **0.79** |
| `group_rank(signed_power(SURP, 3), industry)` | **1.11** | **0.65** | **0.1007** | **0.66** | **0.79** |

**逐位相同**。`rank` 只看序，任何单调变换都被吃掉。
⇒ **铁律：`signed_power` / `winsorize` 必须放在 `group_zscore` 或无 rank 的链路里**；放 `group_rank` 前 = 0 收益（与项目 MEMORY 里「signed_power 是压 prod 核心算子」不矛盾——那条前提是骨架末端没有 rank）。
⚠ 对照：`group_zscore(signed_power(ts_delta(TPD,30), 2))` 确实降了 TO（0.1469→0.1589 略升）但 S 降（0.74→0.65）⇒ zscore 链路下 signed_power 也非稳赚，需实测。

### ★★★ 2. `trade_when(greater(rank(adv20), 0.5), X, -1)` = 本轮最强杠杆
FY2 EPS 3 月修正，同一字段同一窗口，只加一层流动性门控：

| 表达式 | S | fit | TO | sub | 2Y | inv | 塔 |
|---|---|---|---|---|---|---|---|
| `group_zscore(ts_backfill(eps_y2_estimate_change_3mo,60), industry)` | 0.91 | 0.55 | 0.119 | 1.06 | **0.17** | 0.77 | ANALYST |
| `trade_when(greater(rank(adv20),0.5), group_zscore(...), -1)` | **1.02** | **0.66** | 0.099 | **1.08** | **1.28** | **0.92** | **PV(1.4) + ANALYST(1.6) 双塔** |

三处同时改善：S +0.11、**2Y +1.11**、TO −0.02，并**解锁 PV 塔**（`pyramid_short` 由 `analyst` 变 `pv/analyst`，`effective: 2`）。
⇒ 门控把「低流动性噪声票」剔掉后，信号在近 2 年（KOR AI 行情）也站得住 —— 这正是 Wave1 全体栽在 `LOW_2Y_SHARPE` 的根治手段。

### ★★ 3. `ts_decay_linear(x, 5)` 是 KOR 的 2Y 专用药
surprise 骨架：TO 0.1007→**0.0953**，2Y 0.79→**1.05**，inv 0.79→0.82，S 1.11→1.07（小降）。
⇒ 与门控同族但作用点不同：门控提「横截面纯度」，decay 提「时间持续性」。两者叠加是 Wave3 主线。

## 二、分歧度族（论坛主配方）在 KOR 的确认死亡
| 变体 | S | 备注 |
|---|---|---|
| `ts_delta(DISP, 30)` 基准 | 0.74 | 族内最优 |
| `ts_delta(DISP, 10)` | 0.45 | TO 0.27 爆 |
| `ts_delta(DISP, 60)` | 0.37 | **2Y −0.38** |
| `signed_power(...,2)` | 0.65 | 降 S |
| `signed_power(...,2.5)` | 0.62 | 再降 |
⇒ **窗口 30 是唯一甜点**，60 直接把 2Y 打成负。论坛说的「30 日覆盖共识形成期」在 KOR 同样成立。

## 三、`ts_delta` 在 KOR analyst 类信号上普遍失效
surprise 取 20 日变化：S **−0.03**、CONCENTRATED_WEIGHT 0.268 失败。
⇒ KOR analyst 语义信号的持续性很强（水平值 > 变化值），**不要照搬「意外的意外」类构造**。

## 四、Wave3（27 条，已过门禁）设计
主线 = 门控 × decay_linear × 修正/意外族：
- A 组 surprise 门控扫描（门控阈值 0.3/0.5/0.7 × decay0/5/10 × rank/zscore × winsorize）
- B 组 FY2 修正门控 + decay/ts_mean/winsorize/rank（`w3_y2_gate_dec` 为头号种子）
- C 组 FY1 修正 / 修正幅度 / 营收斜率 同族 diversify
- D 组 目标价分歧收敛 + 门控（救 2Y）
- E 组 一致预期水平 + 门控（覆盖差，仅探针）

---

# Wave2 全量结算（33 条，6 批）

收割批次：`3AnQw0JS59AbsiOwMA2HyP`(6) / `4zefH6cuQ4JP9qKY4uMLtRV`(6) / `1B2jDM6iI4hxa9p16obQuaFc`(6) / `33uRbsb8s4ZdcnN8QhfIepu`(6) / `FpBwQ5xr4SbaYRipf2dmEJ`(6) = **30 条 COMPLETE**；`1vyK1ZaEV56MckxXmEIgw9z`(3) 全 CANCELLED（`negate` 不存在，连坐）。

## 一、S 榜（TOP 8）
| rank | alpha id | 骨架 | S | fit | TO | sub | 2Y | inv | 塔 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `A1QdnZwg` | group_rank(SURP120, industry) | **1.11** | 0.65 | 0.101 | 0.66 | 0.79 | 0.79 | ANALYST |
| 1= | `qMEZAKa1` | group_rank(**winsorize**(SURP120, std=4), industry) | **1.11** | 0.65 | 0.101 | 0.66 | 0.79 | 0.79 | ANALYST |
| 1= | `58jVvMn1` | group_rank(**signed_power**(SURP120,2), industry) | **1.11** | 0.65 | 0.101 | 0.66 | 0.79 | 0.79 | ANALYST |
| 1= | `wp9VeLqx` | group_rank(**signed_power**(SURP120,3), industry) | **1.11** | 0.65 | 0.101 | 0.66 | 0.79 | 0.79 | ANALYST |
| 5 | `omoeYV7n` | group_rank(**ts_decay_linear**(SURP120,5), industry) | 1.07 | 0.62 | 0.095 | 0.61 | **1.05** | 0.82 | ANALYST |
| 6 | `58jVvOxX` | **trade_when**(rank(adv20)>0.5, group_zscore(Y2_3mo,60), -1) | 1.02 | 0.66 | 0.099 | **1.08** | **1.28** | 0.92 | **PV+ANALYST 双塔** |
| 7 | `Vkdopvr5` | group_rank(Y2_3mo, industry) | 0.99 | 0.56 | 0.112 | **1.06** | 0.95 | 0.73 | ANALYST |
| 8 | `6XAbwVzY` | group_zscore(winsorize(Y2_3mo,std=4), industry) | 0.95 | 0.58 | 0.119 | **1.10** | 0.19 | 0.80 | ANALYST |

## 二、★★ 三条铁律（本波正式确认）

### 铁律 1：`group_rank` 链路的**任何单调变换 = 完全白用**（逐位相同，非近似）
`SURP120` 裸 / `signed_power(...,2)` / `signed_power(...,3)` / `winsorize(...,std=4)` 四条，
**S=1.11 fit=0.65 TO=0.1007 returns=0.0435 pnl=4496037 longCount=322 shortCount=316 全部逐位一致**。
⇒ `group_rank` 只看序，`signed_power`/`winsorize` 在其前被完全吃掉。
**必须放在 `group_zscore` 内或无 rank 链路**（实测 `group_zscore(signed_power(ts_delta(DISP,30),2), industry)` S 由 0.74→0.65，**确实生效但降 S**）。

### 铁律 2：`trade_when` 门控是唯一同时改善 sub + 2Y + 塔数的杠杆
同字段同 backfill 的三档对照：
| 结构 | S | sub | 2Y | 塔 |
|---|---|---|---|---|
| `group_rank(Y2_3mo, industry)` | 0.99 | **1.06** | 0.95 | 1 |
| `trade_when(g, group_zscore(Y2_3mo,industry), -1)` | 1.02 | **1.08** | **1.28** | **2（PV+ANALYST）** |
⇒ 门控剔掉低流动性噪声票后，`IS_LADDER_SHARPE` 这一族从「整体塌陷」转为「只差 0.30」。**Wave3/4 主线。**

### 铁律 3：`group_rank` vs `group_zscore` 的 2Y 表现**反直觉**
`group_zscore(ts_backfill(Y2_3mo,60), industry)` 2Y 仅 **0.17**，`group_rank` 同字段 2Y **0.95**。
⇒ **2Y 偏好 rank 链路**（更抗尾部极值），但 sub/inv 偏好 zscore 链路。
⇒ 破闸配方：**门控统一 + rank/zscore 视 2Y 与 sub 谁更紧来选**。

## 三、失败指纹（Wave2 新增）
- **`ts_delta` 在本区是毒药**：`surprise` 取 20 日变化 S=**−0.03**（CONCENTRATED_WEIGHT 0.268）；`Y2_3mo` 变体 S 由 0.99 塌到 −1.10。⇒ **KOR analyst 语义信号一律用水平值，禁用 ts_delta/ts_mean 嵌套差分**。
- **`signed_power` 在 zscore 链路降 S**：`ts_delta(DISP,30)` 0.74 → sp2 **0.65** → sp2.5 **0.62**。幂次越大越差。
- **`winsorize` 同样在 zscore 链路降 S**：0.74 → **0.79**(升) 但 2Y 0.82→0.64、TO 0.147→0.145。总体无效。
- **DISP 族窗口复验**（Wave1 结论）：30 日 S=0.74/2Y=0.57 最优；60 日 2Y **−0.38**；10 日 TO 0.273 爆表。**确认死亡，不再投入。**
- **门控阈值单调性**：Wave3 待验（0.3/0.5/0.7 三档）。

## 四、当前 KOR 最强三档（距 RA 全过）
| 档位 | alpha id | 差什么 |
|---|---|---|
| 最佳综合 | `58jVvOxX` | LOW_SHARPE 1.02/1.58（差 0.56）、LOW_FITNESS 0.66/1.0（差 0.34）、**IS_LADDER_SHARPE 1.28/1.58（差 0.30）** |
| 最佳 S | `A1QdnZwg` | LOW_SHARPE 差 0.47、FITNESS 差 0.35、2Y 差 0.79 |
| 最佳 sub | `6XAbwVzY` | sub 1.10 / inv 0.80，但 S 差 0.63、2Y 差 1.39 |

> 共同点：`CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_INVESTABILITY` **已全 PASS**，纯卡「强度 + 2Y」。
> ⇒ Wave3/4 只需攻 **S ↑ 与 2Y ↑**，不再碰换手/集中度/可投资性。

---

# Wave3 首批结算（9 条 / 15 条）+ ★★ 两条反转结论

已收：`Ec1j6c7V4xocCmDfYIYMk4`(6, surprise 门控扫描) / `3O9NtD2Uy4rQ9UmECO02rhq`(3, 目标价分歧+门控)。

## ★★ 反转 1：`trade_when` 门控**不是普适增益，是字段依赖的**（推翻 Wave2 铁律2的普适性）
同一 surprise 字段、同骨架，只换门控：
| 结构 | S | fit | TO | sub | 2Y | inv | 塔 |
|---|---|---|---|---|---|---|---|
| `group_rank(SURP120, industry)`（**无门控**） | **1.11** | **0.65** | 0.101 | 0.66 | 0.79 | 0.79 | 1 |
| `trade_when(rank(adv20)>**0.5**, group_rank(SURP120,industry), -1)` | 0.52 | 0.21 | 0.085 | 0.29 | 1.13 | 0.35 | 2 |
| `trade_when(rank(adv20)>**0.3**, 同上)` | **0.70** | 0.33 | 0.092 | 0.44 | 0.65 | 0.42 | 2 |
| `trade_when(rank(adv20)>**0.7**, 同上)` | 0.27 | 0.08 | 0.078 | 0.21 | 0.83 | 0.22 | 2 |

⇒ **surprise 字段上门控把 S 从 1.11 打到 0.27–0.70**，与 Wave2 在 `eps_y2_estimate_change_3mo` 上的 +0.03 方向相反。
⇒ 门控是**换字段后的赌注**，不是骨架升级。**必须逐字段 A/B**，不能默认套。
⇒ 门控阈值单调性（仅 surprise 字段）：**0.3 > 0.5 > 0.7**，宽松档最优 ⇒ 门控本身是「减权」而非「择强」，越紧越伤。

## ★★ 反转 2：门控确实**能救 2Y，但代价是砍掉 60% 的 S**
`trade_when(g, group_rank(ts_decay_linear(SURP120,5), industry), -1)`：**2Y 1.26**（全 Wave3 最高，距线仅 0.32），但 S 0.51。
⇒ 2Y 与 S 在本区**结构性对立**。想要 2Y 过 1.58，代价必然是 S 掉到 0.5 附近 —— 除非找到「S 和 2Y 同向升」的字段。
⇒ **判据升级：破 2Y 的唯一正道是换字段，不是加算子。**

## 三、目标价分歧族（DISP）正式判死
| 结构 | S | 2Y |
|---|---|---|
| `trade_when(g0.5, group_zscore(ts_delta(ts_decay_linear(DISP,5),30), industry), -1)` | 0.15 | −0.26 |
| `trade_when(g0.5, group_zscore(ts_delta(ts_mean(DISP,10),30), industry), -1)` | 0.16 | −0.30 |
| `trade_when(g0.5, group_zscore(ts_backfill(vec_avg(consensus_mean_estimate),60), industry), -1)` | 0.04 | −0.28 |
⇒ 全部 S≈0.1、2Y 全负、CLUSTER_TEST 全负 ⇒ **后段样本信号反向**。
⇒ 加上 Wave1/Wave2 共 4 波 40+ 条实证，**DISP/目标价分歧族在 KOR 判死，不再投入**。

## 四、平滑层排序（surprise 门控内实测，2Y 口径）
`ts_decay_linear(5)` **2Y 1.26** > 裸 backfill **2Y 1.13** > `ts_mean(22)` **2Y 0.85**。
⇒ 与 Wave2 一致：**decay_linear 是 2Y 专用药，ts_mean 是 2Y 毒药**（但 TO 压得最低）。

## 五、Wave4 设计（86 条，已过门禁 86/86）—— 转向「字段多样化」
**问题诊断**：Wave1–3 共 70+ 条只测了 **3 个字段**（`consensus_surprise_percentage` / `eps_y2_estimate_change_3mo` / `targetprice stddev÷mean`），
而 `analyst_factor_signals` 有 **52 个 userCount≤5 的未点亮字段**（其中 25 个 uc=0 纯白空间）。
⇒ **瓶颈不在算子穷举，在字段覆盖**。算法搜索空间已探到头，继续加算子边际收益趋零。

**Wave4 结构**：42 字段 × 2 变体（裸 `group_rank` vs `trade_when(g0.5, group_rank)`）+ 4 条头号种子加 `decay_linear(5)`
- 变体对设计直接服务「反转1」：**逐字段 A/B 门控增益**，产出「门控适用字段白名单」
- 机制簇覆盖：Revision 6 / Slope 10 / Growth 20 / Disp 8 / Skew 12 / Surp 10 / Seq 4 / CAGR 12 / RevDecay 4
- 含 Wave1 判死族的**门控版复核**（CAGR / Skew）—— 判死结论只对无门控成立，门控可能翻案

---

# Wave3 全量结算（27 条）+ Wave4 首批结算（36/86 条）
# ★★★ 两条诊断级结论：其中一条**推翻本报告上一节的判断**

已收 Wave3：`Ec1j6c7V4xocDmDfYIYMk4`(6) / `4BFRtY4iZ5329nIZGBOFlm3`(6) / `2ds8EvvK4mV8Qi7m8V9p1R`(6) / `2SrnP86Fr5dTbC3117ckGsWU`(6) / `3O9NtD2Uy4rQ9UmECO02rhq`(3) = 27 条全收。
已收 Wave4：批 1/3/4/5/7/8 = 36 条（6 字段 × 2 骨架 × 6 批）。

## 一、★★★ 诊断反转：**「字段多样化」假设被证伪**（推翻上一节第五段的转向依据）
上一节我判断「瓶颈不是算子穷举，是字段覆盖」，据此派了 86 条 Wave4。**首批 36 条实测结果：字段覆盖不是瓶颈。**

| 字段（Wave4 新测，全部 uc≤5） | 骨架 | S | fit | 2Y | 判 |
|---|---|---|---|---|---|
| `eps_q1_estimate_change_1mo` | rank / gate | 0.10 / **−0.46** | 0.02 / −0.18 | −0.79 / −1.06 | 死（且门控反向） |
| `eps_estimate_trend_slope_1yr` | rank / gate | −0.39 / 0.07 | — | 0.13 / 0.21 | 死 |
| `eps_estimate_trend_slope_2yr` | rank / gate | −0.44 / −0.30 | — | −0.82 / −1.06 | 死 |
| `eps_q1_estimate_qoq_growth` | rank / gate | −0.66 / −0.15 | — | −1.31 / −0.72 | 死 |
| `eps_q2_estimate_qoq_growth` | rank / gate | −0.06 / 0.09 | — | −0.12 / 0.26 | 死 |
| `eps_trailing_4q_estimate` | rank / gate | −0.31 / −0.24 | — | −0.67 / −1.36 | 死 |
| `eps_actual_q1_yoy_growth` | rank / gate | −0.11 / −0.24 | — | −0.07 / −0.57 | 死 |
| `revenue_q1_estimate_yoy_growth` | rank / gate | −0.10 / **−0.58** | — | −0.40 / −1.25 | 死 |
| `revenue_q1_estimate_qoq_growth` | rank / gate | 0.03 / **0.17** | 0.00 / 0.04 | **1.16 / 1.34** | 弱苗 |
| `revenue_q2_estimate_qoq_growth` | rank / gate | −0.39 / −0.12 | — | −1.06 / −0.50 | 死 |
| `revenue_trailing_4q_estimate` | rank / gate | 0.03 / −0.29 | — | −0.01 / −0.51 | 死 |
| `revenue_estimate_volatility_adj_2yr` | rank / gate | −0.65 / −0.61 | — | −0.27 / −0.82 | 死 |
| `revenue_revision_magnitude` | rank / gate | 0.31 / **0.60** | 0.09 / 0.27 | −0.01 / 0.27 | **弱苗** |
| `revenue_estimate_trend_slope_3yr` | rank / gate | 0.07 / −0.45 | — | −0.69 / −1.14 | 死 |
| `eps_q1_estimate_yoy_growth` | rank / gate | −0.17 / −0.11 | — | −0.72 / −1.01 | 死 |
| `revenue_q2_estimate_coeff_var` | rank / gate | **0.79** / 0.29 | **0.39** / 0.09 | 0.28 / 0.40 | **本波最强** |
| `eps_q1_estimate_skewness` | rank / gate | −0.26 / −0.16 | — | −0.81 / −0.24 | 死 |
| `eps_y1_estimate_skewness` | rank / gate | 0.02 / −0.09 | — | −0.10 / −0.07 | 死 |

⇒ **18 个新字段里 15 个 S<0.3 且 2Y 多为负**，最高 S 仅 0.79。
⇒ **真正的信号只集中在 2 个字段**：`eps_y2_estimate_change_3mo`（S 0.99–1.02）与 `consensus_surprise_percentage`（S 1.11）。
⇒ **修正后的诊断：KOR analyst 族的信号源极度稀疏**（≈2/60 字段有效），不是「遍地是信号只差结构」。
⇒ **正确打法 = 在这 2 个字段上穷举结构 + 设置档**，而不是继续铺字段。⇒ Wave5 转向（30 条，全打最强腿）。

## 二、★ 门控 A/B 的最终统计（21 组对照，跨 Wave3+4）
| 方向 | 组数 | 说明 |
|---|---|---|
| 门控 **赢** | 5 | `revenue_q2_coeff_var`(0.79→0.29 是**输**，见下) |
| 门控 **输** | 12 | 典型：`revenue_q2_coeff_var` 0.79→0.29、`revenue_q1_yoy` −0.10→−0.58、`eps_q1_change_1mo` 0.10→−0.46 |
| 门控仅「减亏」（负→近零）| 4 | `eps_q1_qoq` −0.66→−0.15 等 |
⇒ **门控净效应为负**。它唯一**稳定**的三项收益是：① TO 压低 5–40% ② 多命中 PV 塔（`analyst`→`pv/analyst`）③ failed_ra 偶尔 −1。
⇒ **门控降级为「塔位工具」**，不是强度工具。**只在需要 PV 塔时使用**，不为提 S 用。

## 三、★★ Wave3 关键突破：`winsorize` 在**门控+zscore 链路**里真实生效
| 结构 | S | fit | TO | 2Y | inv | failed_ra |
|---|---|---|---|---|---|---|
| `trade_when(g0.5, group_zscore(ts_backfill(Y2,60), industry), -1)` | 1.02 | 0.53 | — | — | 0.91 | 4 |
| `trade_when(g0.5, group_zscore(**winsorize**(ts_backfill(Y2,60), std=4), industry), -1)` | 1.01 | **0.64** | — | 1.21 | **0.91** | **3** |
⇒ fit 0.53→**0.64**、returns 0.0387→**0.0509**、`leMZVYen` 是**全战唯一 PPA 全过**候选。
⇒ 修正 Wave2 铁律1的适用范围：**`winsorize`/`signed_power` 被 rank 吃掉，但在 `group_zscore` 内并非无效** —— 之前观察到的「降 S」是用了 `ts_delta` 毒字段造成的混淆。
⇒ **正解 = `group_zscore(winsorize(x, std=4), industry)`**（削极端离群 → 提 fit/inv），而非 `group_rank(signed_power(...))`。

## 四、★★★ 全战 2Y 最高的两条（都在最优字段上）
| alpha id | 结构 | S | fit | 2Y | inv | 差什么 |
|---|---|---|---|---|---|---|
| `KPmRbQdj` | `trade_when(g0.5, group_zscore(ts_mean(ts_backfill(Y2,60),10), industry), -1)` | 0.89 | 0.54 | **1.51** | 0.92 | S 差 0.69 / fit 差 0.46 / **2Y 差 0.07** |
| `pwvg6ZX6` | `trade_when(g0.5, group_zscore(ts_decay_linear(ts_backfill(Y2,60),5), industry), -1)` | **0.97** | 0.61 | **1.42** | 0.94 | S 差 0.61 / fit 差 0.39 / **2Y 差 0.16** |
| `O0JvZvxg` | `trade_when(g0.5, group_rank(ts_backfill(revenue_q1_estimate_qoq_growth,120), industry), -1)` | 0.17 | 0.04 | **1.34** | 0.05 | 弱苗，2Y 有信号但 S 太低 |

## 五、Wave5 设计（30 条，已过门禁 30/30）—— 全部押在最优字段
基座 `trade_when(greater(rank(adv20),0.5), …, -1)` + `ts_backfill(eps_y2_estimate_change_3mo, 60)`：
- 组1 平滑层 × winsorize 笛卡尔（raw/dec3/dec5/dec8/m8/m10/m15 × 有无 win = 14 条）
- 组2 rank 链路对照（3 条）
- 组3 truncation 0.05/0.10 设置档（4 条）
- 组4 门控阈值 0.2/0.4/0.5/0.6 复验（4 条）
- 组5 门控替代形式 + 中性轴 subindustry/sector（5 条）

---

# Wave5 结算（24 条已收 / 30 条）+ ★★ 全战最强 alpha 出现

## 一、★★★ `npAb8VXw` = **全战最强**（S/fit/sub/inv 四项全场最高）
```
trade_when(greater(rank(adv20), 0.4),
           group_zscore(winsorize(ts_backfill(eps_y2_estimate_change_3mo, 60), std=4), industry), -1)
```
| 指标 | 值 | 闸线 | 缺口 |
|---|---|---|---|
| S | **1.14** | 1.58 | 0.44 |
| fit | **0.77** | 1.0 | 0.23 |
| sub | **1.35** | 0.51×S=0.60 | **PASS** |
| inv | **1.09** | — | **PASS** |
| TO | 0.103 | <0.7 | PASS |
| **2Y / LADDER** | **0.53** | 1.58 | **1.05** |

⇒ 四项过了三项半，**唯一硬短板是 2Y**（0.53，距线 1.05，是全部缺口里最大的）。

## 二、★★ 门控阈值是「S ↔ 2Y 反向权衡旋钮」（本波最重要发现）
同一 winsorize 腿，只换 `rank(adv20) >` 的阈值：
| 阈值 | S | fit | sub | inv | **2Y** |
|---|---|---|---|---|---|
| 0.2 | 0.93 | 0.57 | 1.11 | 0.81 | 0.28 |
| **0.4** | **1.14** | **0.77** | **1.35** | **1.09** | 0.53 |
| 0.5 | 1.01 | 0.64 | 1.07 | 0.91 | **1.21** |
| 0.5 + `ts_mean(10)` | 0.89 | 0.54 | 0.92 | 0.92 | **1.51** |
| 0.5 + `ts_mean(15)`+zw | 0.86 | 0.51 | 0.89 | 0.88 | **1.53** |

⇒ **阈值 0.4 = S 峰（1.14）｜ 阈值 0.5 + 长平滑 = 2Y 峰（1.51–1.53）**，两者方向完全相反。
⇒ **2Y 对门控阈值极度敏感（0.28→0.53→1.21）** ⇒ 信号强度集中在极窄时间段，**这是本区 S 上不去 + 2Y 上不去的共同根因**。
⇒ 平滑层 2Y 排序：`mean15`(1.53) > `mean10`(1.51) > `dec5`(1.42) > `dec3`(1.35) > `raw`(1.28)，**长均值是 2Y 主力**。

## 三、★ `winsorize` 最终裁决：**在 zscore 链路里也是负的**（修正 Wave3 的乐观结论）
Wave3 曾看到 winsorize 提 fit（0.53→0.64），Wave5 用 6 组干净配对复核：
| 配对 | S Δ | fit Δ | 2Y Δ |
|---|---|---|---|
| raw vs zw_raw | −0.01 | −0.02 | −0.07 |
| dec3 vs zw_dec3 | −0.02 | −0.02 | −0.07 |
| dec5 vs zw_dec5 | −0.02 | −0.02 | −0.08 |
| m15 vs zw_m15 | −0.06 | −0.05 | **+0.18** |
⇒ 6/6 中 5 组全负；唯一 m15 组是「S/fit 降、2Y 升」的**时间交易**，不是无条件增益。
⇒ **根因**：`group_zscore` 已做组内截面标准化，极值在组内被削掉；`winsorize` 叠加 = 二次截尾，只损信息。
⇒ **Wave5 铁律：`group_zscore` 链路里不要加 `winsorize`**。Wave3 的「fit 提升」实为与门控/字段变体混淆造成的假象（**本报告第二次自我纠错**）。

## 四、★ 平滑层 S 与 2Y 反向（不可同时取极值）
按 S：raw 1.02 > dec3 0.99 > dec5 0.97；按 2Y：dec5 1.42 > dec3 1.35 > raw 1.28。
⇒ 公式化：`S ≈ 1.02 − 0.01×(平滑强度)`，`2Y ≈ 1.28 + 0.06×(平滑强度)`（本骨架内近似线性）。
⇒ **调参层已是零和**：拿 S 就丢 2Y，拿 2Y 就丢 S。⇒ 必须换维度（group 层 / 门控字段 / 数据集），不能靠算子。

## 五、Wave6 设计（27 条，已过门禁 27/27）—— 双段组合攻 2Y
基座 = `trade_when(greater(rank(adv20), thr), group_zscore(FIXER, grp), -1)`
- 组1 **门控阈值 {0.4,0.45,0.5} × 2Y修复器 {dec5,dec8,mean10,mean15} = 12 条**（核心：叠「0.4 拿 S」与「长均值拿 2Y」）
- 组2 门控 {0.4,0.5} × winsorize × 平滑 4 条（复核 winsorize 在长平滑下是否翻转）
- 组3 **换 group 层** {subindustry, sector} 4 条 —— 换中性轴救 2Y
- 组4 `market` 分组（全市场 zscore）2 条
- 组5 门控阈值细扫 {0.35,0.42,0.48} 3 条 —— 找 S 峰精确位置
- 组6 group_rank vs group_zscore 最终对照 2 条

## 六、本波两次自我纠错记录（诚实存档）
1. **「字段多样化是瓶颈」被 86 条 Wave4 证伪**（18 新字段 15 个 S<0.3）⇒ 真实瓶颈是**信号源稀疏**（≈2/60 字段有效）。
2. **「winsorize 在 zscore 链路提 fit」被 Wave5 6 组配对证伪** ⇒ 实为混淆假象。
⇒ 共同教训：**单条对比得出的「杠杆」极可能是混淆**；本区只有「≥5 组同向对照」的结论可复用。

---

# Wave6 结算（15 条已收 / 27 条）—— 调参层宣告死亡，转设置层

## 一、★★★ 零和关系**严格成立**（2×2 完整网格，单调反序）
门控阈值 {0.4, 0.5} × 平滑 {dec5, mean10}，`group_zscore(winsorize(...), industry)`：
| | **S** | **2Y** |
|---|---|---|
| thr0.4 / dec5 | **1.10** | 0.75 |
| thr0.4 / mean10 | 1.09 | 1.12 |
| thr0.5 / dec5 | 0.95 | 1.34 |
| thr0.5 / mean10 | 0.85 | **1.47** |

⇒ S 排序与 2Y 排序**完全反序**，无一例外。
⇒ **S 与 2Y 是同一条曲线上滑动取点，调参层无法抬高曲线上沿**。
⇒ 复现噪声实测：同配方重跑偏移 ±0.04（`kqJ5Prz8` vs `npAb8ZXw`；`WjLmVV9x` vs `KPmRbQdj`），
**已落到平台复现噪声地板** ⇒ 此网格附近继续微调**无信息增益**。

## 二、★ group 层扫描：**放宽分组是死路**（方向与假设相反）
| group 层 | S | 2Y |
|---|---|---|
| **industry** | **1.06 / 0.91** | **0.95 / 0.71** |
| subindustry | 0.73 | 0.83 |
| sector | 1.03 | 0.47 |
| market | 0.93 / 0.88 | **−0.04** / 0.45 |
⇒ **越粗的分组越伤 2Y**（market 直接 −0.04，等于全局择时，time-series 动量全没）。
⇒ `industry` 是唯一同时保住 S 与 2Y 的档。**分组轴判死，不再来。**

## 三、★ `group_zscore` vs `group_rank` 最终裁决：**zscore 全线胜**
同一最优腿（dec5 + industry）：zscore S=0.98/2Y=1.37 ｜ rank 最好 S=0.79/2Y=0.79。
S 差 0.19–0.32、2Y 差 0.54–0.58，fit/sub/inv 同向。
⇒ **修正 Wave2 铁律3**：`group_rank` 的 2Y 优势**只在无门控时成立**；**有门控时 zscore 全面胜出**。
⇒ 最终骨架定型：`trade_when(流动性门控, group_zscore(平滑腿, industry), -1)`。

## 四、★★★ 当前全战 TOP5（0 过闸；全部只差 2Y/S/fit 三闸，形态全干净）
| # | alpha id | 结构要点 | S | fit | TO | sub | 2Y | inv | 差什么 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `E5VAGovr` | thr **0.42** + dec5 + industry | 1.06 | 0.69 | 0.094 | **1.38** | 0.95 | 1.07 | S 0.52 / fit 0.31 / 2Y 0.63 |
| 2 | `npAb8VXw` | thr 0.4 + winsorize + industry | **1.14** | **0.77** | 0.103 | **1.35** | 0.53 | **1.09** | S 0.44 / fit 0.23 / **2Y 1.05** |
| 3 | `WjLmVV9x` | thr 0.5 + mean10 + winsorize | 0.85 | 0.50 | 0.084 | 0.89 | **1.47** | 0.88 | S 0.73 / fit 0.50 / **2Y 0.11** |
| 4 | `N1eoRwJL` | thr 0.5 + mean15 + winsorize | 0.86 | 0.51 | 0.080 | 0.89 | **1.53** | 0.88 | S 0.72 / fit 0.49 / **2Y 0.05** |
| 5 | `KPmRbQdj` | thr 0.5 + mean10 | 0.89 | 0.54 | 0.084 | 0.92 | 1.51 | 0.92 | S 0.69 / fit 0.46 / 2Y 0.07 |

⇒ **全战 2Y 最高 1.53（距线 0.05），但 S 只有 0.86**。⇒ 曲线端点确认：**KOR analyst 单字段的 S 天花板 ≈1.14，2Y 天花板 ≈1.53，两者不可兼得。**

## 五、Wave7 设计（36 条，已过门禁 36/36）—— 唯一未动过的维度：仿真设置层
Wave1-6 共 ~250 条全部锁定 `decay=4 / STATISTICAL / trunc=0.08 / nanHandling=OFF / maxTrade=OFF`。
调参层已死 ⇒ 剩下唯一未探索维度 = **设置层**。两条基座表达式**完全不变**，只改设置：
- 基座 A（S 峰）`trade_when(>0.4, group_zscore(dec5, industry), -1)`
- 基座 B（2Y 峰）`trade_when(>0.5, group_zscore(mean10, industry), -1)`

单变量扫描（**刻意避免 Wave6 的双变量交叉归因**）：
- 轴1 `decay` ∈ {0,1,2,6,8,12,16}（默认 4）
- 轴2 `neutralization` ∈ {MARKET, SECTOR, INDUSTRY, SUBINDUSTRY, CROWDING, FAST, SLOW}（默认 STATISTICAL）
- 轴3 `truncation` ∈ {0.05, 0.10, 0.20}（默认 0.08）
- 轴4 `nanHandling` ∈ {ON}（默认 OFF）

⇒ 新增脚本 `kor_run_wave2.py`：multi-sim 的 settings 是**批级**，故按 `setting_override` 分组派发。

---

# Wave7/8 结算 + 全战役阶段结论（Wave1-8 累计 ~350 条）

## 一、★★★ 头号突破：门控阈值**非单调**，存在双峰
`trade_when(greater(rank(adv20), thr), group_zscore(winsorize(ts_backfill(Y2,60),std=4), industry), -1)`：
| thr | S | fit | TO | sub | **2Y** | inv |
|---|---|---|---|---|---|---|
| 0.4 | 1.14 | 0.77 | 0.103 | 1.35 | 0.53 | 1.09 |
| 0.5 | 1.01 | 0.64 | 0.099 | 1.07 | 1.21 | 0.91 |
| **0.55** | 0.98 | 0.62 | 0.098 | 1.05 | 0.84 | 0.93 |
| **0.6** | **1.15** | **0.80** | 0.096 | 1.14 | **1.20** | 0.99 |
| 0.65 | 0.91 | 0.56 | 0.092 | 0.98 | 0.63 | 0.82 |
| 0.7 | 0.69 | 0.37 | 0.091 | 0.80 | 0.07 | 0.69 |
| 0.8 | 0.31 | 0.12 | 0.091 | 0.58 | −0.65 | 0.36 |

⇒ **0.4 与 0.6 是双峰，0.5 是谷底**（此前所有结论都只在 ≤0.4 区采样，漏掉了更好的 0.6）。
⇒ **0.6 是全局最优点**：S 1.15 / fit 0.80 / 2Y 1.20 —— **首次出现 S 与 2Y 同时高于 0.4 档**（S +0.01、2Y +0.67），**零和被打破**。
⇒ 0.6 + `ts_decay_linear(…, 4)` 变体 `XgREW8a8`：**S 1.13 / fit 0.78 / 2Y 1.49 / inv 1.02**，是当前最均衡的单点。

## 二、★★ 死轴清单（全部实测判死，不再投入）
| 维度 | 实测 | 判决 |
|---|---|---|
| 门控阈值 >0.6 | 0.65–0.8 单调塌方至 S=0.31 | 死（峰值 0.6，窄峰 ±0.05） |
| `ts_backfill` 窗口 | 20/40/90/120/250 → fit 极差 **0.02** | 死（字段月频，无长空缺） |
| `ts_decay_linear` 窗口 | W2/3/4/6 fit 0.80/0.78/0.78/0.74 | 死（最好 0.80，缺口 0.20） |
| group 层放宽 | market → 2Y **−0.04**；subindustry → S 0.73 | 死（industry 唯一最优） |
| `group_rank` vs `group_zscore` | 有门控时 zscore 全线胜（2Y 差 0.54–0.58） | 死 |
| `winsorize` | 6 组配对 5 组全负 | 死 |
| **仿真 decay 设置** | 1→8，S 只移动 **0.03**（1.09–1.12） | **死（动态范围比缺口小一个数量级）** |
| 门控字段替换 | `volume` 略优 S+0.03 但 2Y −0.32；相对换手率/`abs(returns)` S 0.83/0.84 | 死（`adv20` 最优） |
| 乘法式门控 | `ts_rank(volume,20)` TO 0.264 翻 2.8 倍、fit 腰斩 | 死 |

## 三、★★★ 阶段结论：KOR analyst 族的**硬天花板已探明**
**8 波 ~350 条回测，全部实测天花板**：
- **S 上限 1.16**（闸 1.58，缺 0.42）
- **fit 上限 0.81**（闸 1.0，缺 0.19）
- **2Y 上限 1.57**（闸 1.58，**唯一实质达标的一条**：`leMZvXV7` decay=6 档）

**唯一同时做到 S≥1.1 且 2Y≥1.2 的两条**（形态全干净，其余 6 项检查全 PASS）：
| alpha id | 表达式 | S | fit | TO | sub | 2Y | inv |
|---|---|---|---|---|---|---|---|
| `qMEZNWgA` | `trade_when(>0.6, group_zscore(winsorize(ts_backfill(eps_y2_estimate_change_3mo,60),std=4), industry), -1)` | **1.15** | **0.80** | 0.096 | 1.14 | 1.20 | 0.99 |
| `XgREW8a8` | `trade_when(>0.6, group_zscore(ts_decay_linear(ts_backfill(Y2,60),4), industry), -1)` | 1.13 | 0.78 | 0.089 | 1.09 | **1.49** | **1.02** |

⇒ **S 缺口 0.42 是单字段信息量的硬上限，不是调参问题**。所有 9 个维度已扫尽（字段/算子/门控/分组/窗口/平滑/truncation/decay/中性化）。

## 四、下一步唯一有理据的方向
1. **换数据集**（保持 KOR）：`analyst_consensus` 的 2343 字段（2184 个 uc=0）尚未系统扫过 —— 但 Wave4 已证明该数据集的字段信噪比同样极低（18 字段 15 个 S<0.3），**优先级低**。
2. **正交第二腿**：`multiply(rank(Y2_leg), rank(正交信号))` 是本区唯一未测的**强度叠加**结构（不同于已死的时间平滑叠加）。风险：可能触发 prod corr 墙。
3. **换区域**（违反用户 KOR 锁定约束，仅作记录）。

⇒ **诚实结论：10 个 RA 过闸 alpha 的目标，在 KOR analyst 单字段路径下不可达。当前最强候选距全闸还差 2 项（S −0.42 / fit −0.19）。**

---

## Wave9 结算（结构层，全部证伪）

37 条候选分3 组，收割 12 条（2 批 COMPLETE）：

| 组 | 结构 | S | fit | 2Y | 判定 |
|---|---|---|---|---|---|
| DualRank | `multiply(group_rank(BF60,ind), group_rank(BF60,ind))` 双窗 | 1.01 | 0.60 | 1.02–1.06 | ❌ 低于天花板 |
| DualRank | 短窗 5 / 10 / 20 × 长窗 60 / 120 全组合 | 1.01 | 0.60 | — | ❌ 窗口无关 |
| OrthLeg | `multiply(rank(BF eps_change), rank(BF coeff_var))` | 0.02–0.28 | 0.00–0.09 | — | ❌ 灾难 |
| OrthLeg | `multiply(rank(BF eps_change), rank(BF revision_magnitude))` | 1.01 | 0.60 | 1.14 | ❌ 不如单腿 |

**Wave9 铁律**：双窗秩乘积在 KOR analyst 上**无效**（与项目记忆里 GBR 的成功经验相反）。
⇒ 跨区经验不可移植，必须逐区实测。
正交第二腿（跨字段 multiply rank）**必然摧毁信号**：非相关字段相乘= 噪声占优。

## Wave7 设置层结算（decay / neutralization / truncation）+ fit瓶颈定量诊断

### fit 闸公式反算（`F = S × sqrt(returns / max(TO,0.125))`）

| 候选 | S | fit | returns | TO | 过 fit=1.0 所需 returns | 倍数 |
|---|---|---|---|---|---|---|
| decay_linear d12 | 1.13 | 0.76 | 0.0569 | 0.082 | 0.0979 | ×1.72 |
| decay_linear d0 | 1.12 | 0.75 | 0.0564 | 0.104 | 0.0996 | ×1.77 |
| ts_mean tr0.2 | 0.89 | 0.54 | 0.0455 | 0.084 | 0.1578 | ×3.47 |
| XgREW8a8（历史最强） | 1.13 | 0.78 | 0.0553 | 0.089 | 0.0979 | ×1.77 |

⇒ **★★ fit 闸的真正瓶颈是 returns 幅度，不是 S**。
即使 S 提到 1.58（+40%），仍需 returns 提升 72% 才能过 fit。
⇒ 只追 S 的方向全部无效；必须找returns 杠杆。

### truncation = 死轴（硬证据）

`truncation ∈ {0.05, 0.08, 0.10, 0.20}` 四档实测 **returns 全部 = 0.0549**、
`TO=0.0941`、`margin=0.001168` 完全一致 ⇒ truncation 在 KOR 对本表达式**无任何作用**。
（原因：表达式已经过 `group_zscore(...,industry)` 硬中性化，权重已被压平。）

### decay 轴：收益几乎不变，S/2Y 有trade-off

| decay | S | fit | returns | TO | 2Y | sub |
|---|---|---|---|---|---|---|
| 0 | 1.12 | 0.75 | 0.0564 | 0.1043 | 0.62 | 1.32 |
| 12 | 1.13 | 0.76 | 0.0569 | 0.0820 | 1.07 | 1.27 |

decay 0→12：returns 只+0.9%，TO 降 21%。**decay 不动returns**，只降 TO。
⇒ 又一条returns 死轴。

### ★★★ neutralization = 唯一强returns 杠杆（Wave7 最重要发现）

| neutralization | S | fit | returns | TO | margin | 2Y |
|---|---|---|---|---|---|---|
| **CROWDING** | 1.06 | **0.74** | **0.0615** | **0.0646** | **0.001903** | 0.89 |
| STATISTICAL | 1.13 | 0.76 | 0.0569 | 0.0820 | 0.001387 | 1.07 |
| FAST | 0.95 | 0.60 | 0.0495 | 0.1205 | 0.000822 | **1.53** |

**CROWDING 把 returns 推到 0.0615（历史最高，比 STATISTICAL +8%）且 TO 降到 0.065、
margin 翻倍到 0.0019** ⇒ 唯一同时改善 returns 与换手的轴。
**FAST 是 2Y 之王（1.53，距闸 1.58 仅 0.05）但returns 最差。**

### ★★ 平台硬约束：KOR/D1 唯一合法 universe = TOP600

`get_platform_setting_options` 实测：KOR/Delay=1 的 Universe 列表**只有 `["TOP600"]`**。
⇒ universe 杠杆（TOP1000/TOP3000 扩容增returns）在 KOR **被平台锁死**，不可用。
⇒ KOR 的 returns 只能靠：中性轴 + 平滑结构 + 门控 + decay，无外部扩容手段。

### S ↔ 2Y 明确 trade-off（本区铁律）

- `ts_decay_linear` 链 → S 高（1.13）、returns 高（0.057）、**2Y 低（0.62–1.20）**
- `ts_mean` 链 → S 低（0.89）、returns 低（0.046）、**2Y 高（1.37–1.53）**

⇒ 想同时过 S闸和 2Y 闸，不能只用一个平滑器，需结构混合（Wave10 A6 组）。

## Wave10 设计（returns 专项，围绕 CROWDING 枢轴）

31 条候选，31/31 过门禁。分组：
- A1 CROWDING × 门控阈值细扫 {0.30,0.35,0.40,0.45,0.50,0.55,0.60}（7）
- A2 CROWDING × 平滑谱（ts_decay_linear 2/3/5/8/12、ts_mean 5/10/20/40、纯 backfill）（10）
- A4 门控腿替换 {vol_rel, close}×thr{0.4,0.6}（4）
- A5 CROWDING × group_rank/subindustry 双中性层（2）
- A6 FAST×CROWDING 折中（宽门控 + 长平滑）（4）
- A7 反向信号对照（1）
- A3 decay 8/12/16/20（4，已派 decay12）

已派批次：`W7rrUfJs4mFbqhUA1GuN3` / `2nOdLWabI5da9vt5hejF5k9` /
`4vIRdc1s64kWc52T2PYBWw4` / `NKAmd4bf4CUcAR8TBYoxsb`(decay12)

---

## ★★★★★ Phase C 归因复盘（本战役方法论纠偏 —— 最重要的一节）

### 方法论缺陷：Wave1–10 的波次设计全程缺归因

Wave1–10 全部由「单点标量（sharpe/fitness/returns/TO/2Y/sub/inv）+ 参数扫描」驱动。
拿到标量没过闸就换下一个轴，**从未做过逐年归因 / PnL 形态归因 / 多腿归因**。
⇒ 后果：像 2Y 崩塌（S=1.13 但 2Y=0.62–1.20）这种**明确的归因信号**，被当成"再调一个设置轴"处理，
而 2Y崩塌本身就是"收益集中在个别年份"的指纹，调设置轴永远治不了根。
⇒ **纪律**：任何 S 上不去/ 2Y 上不去的候选，先归因再决定是否继续扫参数。

### 归因对象：`qMEZNWgA`（S=1.15 / fit=0.80 / 2Y=1.20，历史最强）

**逐年归因（get_alpha_yearly_stats）**：

| 年份 | PnL | 占正收益 | S | fit |
|---|---|---|---|---|
| 2014 | 531,718 | 8.1% | 0.97 | 0.62 |
| 2015 | 974,200 | 14.9% | 1.56 | 1.35 |
| 2016 | **-307,567** | -4.7% | **-0.60** | -0.29 |
| 2017 | 595,024 | 9.1% | 1.29 | 0.87 |
| 2018 | 23,362 | 0.4% | **0.05** | 0.01 |
| 2019 | **1,419,867** | **21.7%** | **2.81** | 2.93 |
| 2020 | 756,846 | 11.6% | 1.34 | 1.06 |
| 2021 | 953,485 | 14.6% | 1.62 | 1.38 |
| 2022 | 1,128,752 | 17.3% | 2.18 | 2.03 |
| 2023 | 150,152 | 2.3% | **0.27** | 0.09 |

**PnL 形态归因（get_alpha_pnl，2586 点降采样）**：
曲线整体呈**阶梯式累积**（健康形态，非尖峰暴涨），但阶梯间有 4 段长期停滞/回撤：
- 2014H1 单边下跌至 **-611,538**（全程最深回撤），下半年才开始爬升
- 2016 唯一负年，S=-0.60
- 2018 几乎零收益（S=0.05），全年 PnL 仅 +23k
- 2023 几乎失效（S=0.27），曲线在 2022 末已完全走平

### ★ 归因结论（四条，全部可复用）

1. **不是极端单年依赖**：2019 单年占正收益 21.7%（健康阈值 <30%），top3年 53.9%。
   剔除 2019 总 PnL 仅 -23%。⇒ 整体信号是真实的，不是单年拟合。
2. **4/10 年份 S<1.0**（2014 0.97 / 2016 -0.60 / 2018 0.05 / 2023 0.27）
   ⇒ **这才是 2Y/IS_LADDER 闸（1.58）上不去的直接原因**。
   2Y 闸只看最近 2 年（2022 S=2.18 但 2023 S=0.27），所以 2Y 值在 0.62–1.53 间剧烈摆动
   —— 取决于 2Y 窗口恰好落在哪两年，**与参数优劣无关**。
3. **信号在最近 2 年（2022→2023）明显衰减**：S 从 2.18 崩到 0.27。
   ⇒ 这是「分析师预期修正动量」在 KOR 的**机制性失效**（预期修正类信号在信息传导被充分定价后必然衰减），
   不是过拟合，也不是参数没调好。
4. **长期停滞段（2016/2018/2023）说明信号强度有 regime依赖**，平滑器只能把阶梯连得更平滑，
   不能把停滞段变出收益 ⇒ **调设置轴对 returns/2Y 的天花板没有作用**（已被 decay/truncation/universe 三死轴实测证明）。

### ★★★ Wave10 阶段性成果：returns 创新高（唯一真实进展）

`e76J6Eap` = CROWDING 中性 × **decay=12** × ts_decay_linear(5) × thr0.4：

| 指标 | 本候选 | 前最高 (qMEZNWgA) | 变化 |
|---|---|---|---|
| **returns** | **0.0638** | 0.0553 | **+15.4%** |
| **margin** | **0.002359** | 0.001013 | **+133%** |
| turnover | **0.0541** | 0.0960 | -43.6% |
| fitness | 0.79 | 0.80 | ≈ |
| sharpe | 1.11 | 1.15 | -3.5% |
| 2Y | 1.03 | 1.20 | -14% |
| sub | 1.28 | 1.14 | +12.3% |
| investability_fitness | **0.86** | 0.99 | -13% |

⇒ **CROWDING × decay12 是 returns/换手/margin 的联合最优点**，是本战役目前最有价值的一次结构突破。
⇒ 但 fit 仍 0.79（差 0.21）、2Y 仍 1.03（差 0.55）。
按 `F = S×sqrt(returns/0.125)` 反算，S=1.11 时 fit=1.0 需 returns=0.1014，
**当前 0.0638，还需 +59%** ⇒ returns 杠杆已接近耗尽（已用尽 decay/truncation/universe/CROWDING 四条轴）。

### 战役最终诊断（诚实结论）

**KOR analyst_factor_signals 单字段路径存在硬天花板，10 个 RA 全过闸 alpha 在该数据集内不可达**：
- S 天花板 ≈ 1.16（350+ 条实测，闸 1.58）
- returns 天花板 ≈ 0.064（闸需 ~0.10）
- 2Y 天花板≈ 1.57（闸1.58，且因窗口随机性不可控）
- 三闸同时达标需returns +59% 且 S +42% ⇒ 两个独立维度同时突破，已无未用杠杆

剩余唯一未开采方向：**analyst_consensus 数据集（2343字段，此前完全未扫）**，
以及**换机制而非换参数**（寻找 regime 无关的机制，如分析师覆盖广度变化而非修正幅度）。

---

## Phase D：铁律 F 强制归因 — `e76J6Eap` 逐年 + PnL 复盘（Wave10 收割后）

> 合规前置：`e76J6Eap` = Wave10 优胜（CROWDING × decay12｜ret 0.0638 / margin 0.00236 / TO 0.054）。
> 按**铁律 F**，未跑完这份归因不得开下一波。本节即开波准入结论。

### D.1 归因三问逐条作答（`get_alpha_yearly_stats` 全 10 年）

| 年 | S | returns | fitness | 判读 |
|---|---|---|---|---|
| 2014 | 1.03 | 0.055 | 0.68 | 勉强 |
| **2015** | **2.07** | 0.129 | 2.10 | ★ 唯一强年 |
| **2016** | **0.08** | 0.0044 | 0.02 | ✘ 归零年 |
| **2017** | **0.02** | 0.0009 | 0.00 | ✘ 归零年 |
| 2018 | 0.84 | 0.0546 | 0.56 | 未过 |
| 2019 | 1.86 | 0.091 | 1.59 | 过 |
| 2020 | 1.19 | 0.0789 | 0.95 | 勉强 |
| 2021 | 1.66 | 0.1026 | 1.50 | 过 |
| 2022 | 1.83 | 0.1041 | 1.67 | 过 |
| **2023** | **0.30** | 0.0183 | 0.11 | ✘ 归零年 |

**问 1 — S<1.0 的年份占几成？**
`2016(0.08) / 2017(0.02) / 2018(0.84) / 2023(0.30)` = **4/10 = 四成**。
⇒ **≥3 成，触发铁律 F 的「结构性不可达」判定：2Y 闸（LADDER 取最近两年 S 均值 ≈ (1.83+0.30)/2 = 1.07）在任何参数档都上不到 1.58。禁止再扫设置轴。**

**问 2 — 单年收益集中度？**
正 PnL 年份合计 ≈ 665.9 万；top1 = 2015 的 134.6 万 = **20.2%**（<30% 阈值）⇒ **不是单年过拟合**。
2023 未归零前口径下，2019 年 94.9 万 = 14.2%。
⇒ 集中度健康，**问题不是「某一年撑起来」，而是「有 4 年根本不赚」**。

**问 3 — PnL 曲线形态与停滞段数？**
`get_alpha_pnl`（2586 点，downsample 至 160）：曲线为**长期阶梯累积**，但存在
**3 段明显停滞/横盘**：① 2014Q2（-28.6 万 → +15.8 万，横跨约 6 个月）；
② **2015-09 → 2018-04 累计 2.5 年横在 180~210 万区间**（这是最致命的一段）；
③ 2023-04 → 2023-12 横在 640~680 万。
⇒ **停滞段 ≥3 ⇒ regime 依赖确诊**，`decay`/`ts_mean`/`hump` 一类平滑器**结构上无效**（对应 skill 已死轴清单）。

### D.2 归因读数 → 发波决策（查 skill「归因读数 → 发波决策表」）

| 读数 | 判定 | 处置 |
|---|---|---|
| S<1.0 占 4 成 | **2Y 结构性不可达** | ⛔ 停扫 `decay` / 中性化档 / 窗口 |
| top1 集中度 20.2% | 非过拟合 | ✅ 允许换机制（不需换字段以避嫌）|
| 停滞段 ≥3 | **regime 依赖** | ⛔ 平滑器谱整族不再扫 |
| 2016/2017 连续两年 S≈0.02–0.08 | **机制性失效区间** | ⛔ 同类「预期修正幅度」字段族整体降级 |

**⇒ Wave10 之后的唯一合规动作：换机制族（analyst_consensus / 覆盖广度类），不是继续调 CROWDING×decay。**
旧路线的 S 天花板（≈1.16）与本归因一致：单字段分析师修正幅度在 KOR 无 regime 稳定性。

### D.3 Wave10 收割结算（`W7rrUfJs4mFbqhUA1GuN3` / `2nOdLWabI5da9vt5hejF5k9`，18/18 完成）

| alpha | S | fit | TO | 判读 |
|---|---|---|---|---|
| `JjPLP6Yj` | **1.35** | **1.10** | 0.0556 | ★ **Wave10 唯一双闸过拟合闸候选**（S≥1.58 仍差 0.23）|
| `zqrz3Y6G` | 1.09 | 0.77 | 0.0561 | 主闸未过 |
| `JjPLexEn` | 1.08 | 0.76 | 0.0564 | 主闸未过 |
| `O0JvArE1` | 0.97 | 0.65 | 0.0500 | 主闸未过 |
| 其余 13 条 | 0.64–1.06 | 0.34–0.74 | — | 主闸未过 |

**结论：CROWDING 中性轴把 fit 从 0.74 抬到 1.10（`JjPLP6Yj`），证明 returns 杠杆真实存在且有效；
但 S 只到 1.35，距 1.58 仍差 0.23，且 D.1 已证明 2Y 结构性不可达 ⇒ 该轴收益已榨干。**
第三批 `4vIRdc1s64kWc52T2PYBWw4` 仍 `terminal=0`，在飞，按已死轴清单**不作为下一波设计依据**。

---

## Phase E：②.d 通道 B 首次实跑（外部金融论文取证）— 结论直接命中 Phase D 的补救方向

> 触发：用户指出「论坛模板是辅助，来源不应只是论坛，还要加即时从外部金融论文获取的灵感模板」。
> ②.d 已改为**双通道**（A=论坛给表达模板，B=外部论文给机制与实证）。本节是通道 B 的**第一次实跑取证**。

### E.1 检索式与判读（`domain_search`，A-1 五问的答案写进 query）

query：**「研究分析师预测修正广度与修正幅度对横截面股票收益的预测力差异及其行为金融机制证据」**

⚠ **重要限定（通道 B 自身声明的）**：「广度 > 幅度」**未被任何单一权威论文以「控制幅度后广度仍显著」的干净检验证实**，
证据多来自联合信号构建与商用回测（含回测偏差、未计交易成本、样本期差异）⇒ 按 ②.d 纪律，**当假说不当模板**。

### E.2 三条可直接落成 ②.a 声明的机制结论

| # | 机制结论 | 文献支撑 | ⇒ 对 KOR 的含义 |
|---|---|---|---|
| **E-1** | **广度优于幅度**：分析师倾向「小幅渐进修正」而非一次性大改 ⇒ **单次幅度未必有预测力**；`(#上调 − #下调)/ 覆盖数`（广度）刻画群体共识强度 | Anasel 白皮书；Pomegra | ★ **Phase D 判死的正是「幅度」路线**（`analyst_factor_signals` 修正幅度）⇒ 文献与实证**双向一致**，说明换广度不是逃避 |
| **E-2** | **机制 = 市场反应不足（underreaction）**：修正后价格**渐进漂移**而非瞬时重定价 ⇒ 天然对应**变化率/漂移类形态**，非水平 | Givoly & Lakonishok 1979/80；Stickel 1991（修正>5% 上调 → 4 个月异常收益 +4.7%）；Chan/Jegadeesh/Lakonishok 1996（6 个月多空差 **7.7%**、12 个月 8.7%）| 形态方向：**ts_delta / 移动平均**，符合 ②.b「强度型 ⇒ ts_delta 后多窗乘积」 |
| **E-3** | **持有期 1–3 个月，效应集中在修正潮之后** | QunatMemo（修正广度+幅度 TOP-BOTTOM 年化 5–10%，效应在修正潮后 1–3 月）；华泰金工 241203（修正幅度+上调占比合成，月度 RankIC **3.99%**，TOP 年化超额 **9.55%**）| 窗口候选：**22 / 66 / 126**（1–3 月），而非 5 日短窗 |

### E.3 反向证据（必须一并记录，防单边叙事）

| 反向发现 | 含义 |
|---|---|
| **Hirshleifer Lim & Teoh 2009 分心假说**：同日盈余公告越多 ⇒ 对任一家的反应越不足 | ⇒ 广度类信号在**财报密集期**可能更强也可能更噪声，需按市场状态分箱 |
| **分析师自身乐观偏差**：对好消息上调更及时、对坏消息下调更迟缓 ⇒ **向下修正后的漂移更大**（Bond Univ，第三月 FF alpha −6.90%） | ⇒ **方向不对称**，铁律 B（正反各测一条）在此**不是形式要求，是机制要求** |
| **Gleason & Lee 2003**：漂移随**覆盖分析师数增加而减弱**（信息传递更充分）；明星分析师修正漂移**减弱** | ⚠ **对 KOR 尤其不利**——TOP600 是小宇宙，覆盖广度天然受限 ⇒ 广度信号的信息含量可能不足。**这是 Wave11 的最大风险，须开波前先量覆盖分布** |
| **Hsu & Jin 2014**：PFRD 主要集中于**低价股**，且 **2002 年后漂移幅度下降**（定价效率提升） | ⇒ 需实测 KOR 2014–2023 是否有**近年衰减**（与 Phase D 的 2023 崩塌年吻合）|
| **分散度异象方向相反**：DMS 2002 / Cen Wei Yang 2017 —— 预测**分歧度高 ⇒ 未来收益低**（Miller 卖空约束） | ⚠ **别把「广度」与「分歧度」混为一谈**：高分散度对应**低**广度，二者共同刻画共识结构，**方向相反** |

### E.4 给 Wave11 的设计结论（写进战报备查）

1. **机制族切换有文献支撑**：从「修正幅度」切到「**修正广度 / 上调占比**」，Phase D 的实证判死与 E-1 的文献结论**双向一致**。
2. **但 E-3 的 Gleason & Lee 覆盖数效应是反向风险**：KOR/TOP600 小宇宙覆盖广度受限，**开波前必须先量 `analyst_consensus` 的覆盖家数分布**（`count_*` 字段），若覆盖普遍 <3 家 ⇒ **广度路线同样不可行**，需退到「单分析师修正的时序形态」。
3. **窗口候选由文献给定**：22 / 66 / 126，而非盲扫 1/5/22/66/252。
4. **方向必须正反各测**（铁律 B 在此为机制要求，见 E-3 第二条）。
5. ⚠ **通道 B 自身声明的证据强度不足**（无干净检验、回测偏差、USA 样本偏误）⇒ **Wave11 候选数须从严**（铁律 G 收窄），且**不得把本节当"已验证模板"引用**。
