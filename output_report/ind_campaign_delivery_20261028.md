# IND 战役交付报告（regular alpha 候选池 · 20 颗）

- 快照时间：2026-10-28（Asia/Shanghai；报告只反映当日平台读数，后续回测/相关性会变动）
- 战役：IND / EQUITY / TOP500 / DELAY 1 / 截断 0.08 / 单位 VERIFY / nanHandling OFF
  （中性化：前 10 颗 INDUSTRY（`58jPrvZ1` 为 STATISTICAL），第 11–19 颗统一 STATISTICAL + decay 126，
  第 20 颗 STATISTICAL + decay 126，见 §3 注）
- 口径来源：`docs/reference/ind_campaign_runbook_20261025.md` + `wq-brain-ra-ind` skill
- **本报告不构成提交动作**。20 颗全部 `status=UNSUBMITTED` / `stage=IS`；任何真实提交
  （`POST /alphas/{id}/submit`）都必须先取得用户明确确认。

## 1. 交付结论

| 项 | 结果 |
|---|---|
| 目标 | 未点亮塔优先，挖 **20** 颗 regular alpha（ATOM 优先） |
| 已验证可交付 | **20 颗**（IS 全闸通过、RA 失败项 0、self < 0.70、十年 2014–2023 齐全；**prod 已实测 10 颗**，第 11–19 颗 + 第 20 颗 prod 仍待测，见 §3 末注） |
| 未点亮塔产出 | **10 颗**：RISK 2（`58EbwZeN`/`88RoVq6V`）、INSTITUTIONS 6（`E567pmkK`/`E5VNe67L`/`KPmvEYeE`/`88vwZE17`/`ZYmgngv0`/`leAOVRb2`）、SENTIMENT 1（`Vkx9RbJV`）、IMBALANCE 1（`ZYQ5J7j1`） |
| 已点亮塔产出 | **10 颗**：FUNDAMENTAL 1（`2rA0e6MN`）、ANALYST 9（`58jPrvZ1` + 8 颗 flash-estimate 残差） |
| ATOM | **3 颗**（`pyramids.effective == 1`）：`58EbwZeN`、`88RoVq6V`（risk68）；`58jPrvZ1`（ANALYST，mult 1.4 最高乘子塔）。**其余 17 颗 `effective == 2`，不是 ATOM**（`returns` 作 `ts_regression` 因变量即计入 PV 归属，见 §2 行 5；ATOM 上限的实测依据见 §3.3 实验 E/F/G/H 与归因 D0） |
| 可共存性 | 20 颗本地 PnL 互相关 **190 对全部 < 0.70，最大对 0.6699（E5VNe67L↔KPmvEYeE）**，`missing_pnl=[]`，`max_subset_exact=true`，`max_mutually_below_subset_size=**20**` |
| 第 20 颗 | **已补齐**：`leAOVRb2`（INSTITUTIONS 未点亮塔，机构买卖**广度**残差）S2.56 / F1.81 / 2Y2.40 / rob1.60 / sub1.41 / ra=0 / self 0.4954 / 对池最大 **0.4678**；覆盖 2014–2023 全十年，最差年 1.25。取证见 §3 行 20、§3.3 实验 H |
| 备选（落选池可启用） | `88RowlOW`（IMBALANCE，S2.32/F1.45，ra=0，对池最大 0.5629；与 ZYQ5J7j1 0.8581 互斥，只在 ZYQ5J7j1 落选时启用） |

## 2. 五项约束遵从

| # | 约束（用户原话要点） | 落地方式 | 证据 |
|---|---|---|---|
| 1 | 未点亮塔跑流水线，挖 20 颗 regular（最好 ATOM） | 按 `get_pyramid_alphas()` **当季**口径逐一核对塔位；20 颗中 10 颗落在未点亮塔（RISK 2 / INSTITUTIONS 6 / SENTIMENT 1 / IMBALANCE 1） | §5 塔覆盖表；ATOM 3 颗 `effective==1` |
| 2 | 近闸候选按 `wq-brain-ra-ind` SOP 定向挖掘 | 对 `LOW_ROBUST_UNIVERSE_SHARPE`（IND 真瓶颈）/`HIGH_TURNOVER`/`IS_LADDER_SHARPE` 卡口候选定向修复；第 11–19 颗是「**残差几何（returns 对因子做 252 日回归取残差）+ decay 126 + STATISTICAL**」这一族的成批产出，第 20 颗把同一几何搬到未点亮塔的**机构买卖广度**字段（`rg_grdev` 7 臂族同批全灭，见 §6） | §6 排除/修复链；§4 Form E；§3.3 实验 A–H |
| 3 | 开波并发 = 2；查 prod 必须走 MCP | 并发上限 2 = **每批最多 2 条表达式**（multisim 每条表达式各占一个仿真槽）；本轮全部批次 ≤ 2 臂，无 429。prod/self 全部 `check_correlation` / `check_self_correlation` **MCP 工具**，`correlation_busy` 时按顶层 `retry_after` 退避，无自建 HTTP、无临时 requests 脚本 | §7 复现命令；prod 结果落 `logs/_tmp_prod_final.json`（10 颗）与 `logs/_prod9/*.json`（第 11–19 颗） |
| 4 | 覆盖率可动态调整，但近十年必须有数据 | 接受 cov 较低的 ALIVE 字段；对交付候选逐个 `get_alpha_yearly_stats`，要求 **2014–2023 十个完整年度**都有 PnL | 20/20 颗均 10 个年度，见 §3.2 |
| 5 | 禁止 PV / MODEL / OTHER 字段两两组腿 | 20 颗**全部为单数据集表达式**（`add(A,B)` 跨集相加为 0、`trade_when(PV条件, 信号)` 为 0、PV/MODEL/OTHER 字段配对为 0）。`returns` 只在残差几何里作 `ts_regression` **因变量（基准）**；它会把 `pyramids.effective` 推到 2，故这 17 颗**不申报 ATOM** | 表达式原文见 §4 |

- `eff` = 平台 `pyramids.effective`（1 = 单数据集 ATOM；2 = 中性化/`returns` 基准把第二个数据集记为归属，**不是两条信号相加**）。
- 本轮 MODEL 候选 `RR7vlM2o` 因 prod 0.8219 出局（§6），最终池 **不含 MODEL 腿**。

## 3. 交付候选表（20 颗）

平台读数（IS 段）。`rob` = `LOW_ROBUST_UNIVERSE_SHARPE` 实测值；`self` 为本地 OS 池计算
（`local_calculation=true`，`pool_size=50`，`excluded_power_pool_count=7`）；`prod` 为
`check_correlation(correlation_type=production)` 平台实测。

| # | alpha | 塔 / 数据集 | Sharpe | Fitness | Turnover | 2Y | rob | sub | ra 失败 | eff | self | prod |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `58EbwZeN` | RISK / risk68 `rsk68_residual_return` | 2.76 | 1.76 | 0.2728 | 2.48 | 1.05 | 1.30 | 0 | **1** | 0.4298 ✓ | 0.5887 ✓ |
| 2 | `88RoVq6V` | RISK / risk68 `rsk68_residual_return` | 3.35 | 2.29 | 0.2712 | 2.21 | 1.30 | 1.59 | 0 | **1** | 0.3769 ✓ | 0.5732 ✓ |
| 3 | `E567pmkK` | INSTITUTIONS 族 | 2.93 | 1.81 | 0.3393 | 2.60 | 1.62 | 1.77 | 0 | 2 | 0.2925 ✓ | 0.4924 ✓ |
| 4 | `E5VNe67L` | INSTITUTIONS 族 | 3.20 | 2.52 | 0.2497 | 3.00 | 1.80 | 1.64 | 0 | 2 | 0.6648 ✓ | 0.6643 ✓ |
| 5 | `KPmvEYeE` | INSTITUTIONS 族 | 3.07 | 2.36 | 0.2387 | 3.14 | 1.49 | 1.65 | 0 | 2 | 0.6086 ✓ | 0.6162 ✓ |
| 6 | `88vwZE17` | INSTITUTIONS 族 | 2.46 | 1.73 | 0.2369 | 2.60 | 1.57 | 1.38 | 0 | 2 | 0.5796 ✓ | 0.5788 ✓ |
| 7 | `2rA0e6MN` | FUNDAMENTAL / fundamental90 `game_relative_rtn_vol` | 2.31 | 1.67 | 0.1841 | 2.74 | 1.21 | 1.47 | 0 | 2 | 0.3251 ✓ | 0.4926 ✓ |
| 8 | `Vkx9RbJV` | **SENTIMENT（未点亮塔）** / sentiment21 `snt21_pos_mean` | 3.14 | 2.08 | 0.3037 | 2.37 | 1.26 | 1.62 | 0 | 2 | 0.4281 ✓ | **0.6939 ✓（余量仅 0.0061）** |
| 9 | `ZYQ5J7j1` | **IMBALANCE（未点亮塔）** / imbalance5 `imb5_score` | 2.40 | 1.51 | 0.3669 | 2.54 | 1.06 | 1.18 | 0 | 2 | 0.3442 ✓ | 0.6693 ✓ |
| 10 | `58jPrvZ1` | **ANALYST（mult 1.4）** / flash estimate EBT 离散度（单数据集） | 1.64 | 1.27 | 0.1142 | 2.23 | 1.12 | 1.55 | 0 | **1** | 0.4843 ✓ | 0.5354 ✓ |
| 11 | `kqJkPLeO` | ANALYST / `anl44_eps_best_eeps_cur_yr` 残差 | 3.02 | 2.40 | 0.2247 | 2.36 | 1.70 | 1.63 | 0 | 2 | 0.4943 ✓ | ⏳ |
| 12 | `j2el6dlk` | ANALYST / `eps_y1_estimate_skewness` 残差 | 2.87 | 2.29 | 0.2167 | 2.66 | 1.82 | 1.72 | 0 | 2 | 0.4106 ✓ | ⏳ |
| 13 | `omowNkL2` | ANALYST / `est_ptp` 残差 | 2.72 | 2.12 | 0.2180 | 2.66 | 1.64 | 1.93 | 0 | 2 | 0.4541 ✓ | ⏳ |
| 14 | `WjLwPVpk` | ANALYST / `eps_y1_cagr_2yr` 残差 | 2.66 | 2.00 | 0.2200 | 2.18 | 1.75 | 1.88 | 0 | 2 | 0.5278 ✓ | ⏳ |
| 15 | `QPYrG5q5` | ANALYST / `eps_y1_estimate_coeff_var` 残差 | 2.54 | 1.96 | 0.2031 | 2.47 | 2.02 | 2.16 | 0 | 2 | 0.4173 ✓ | ⏳ |
| 16 | `P0MrGA2M` | ANALYST / `anl4_afv4_eps_low` 残差 | 2.54 | 1.89 | 0.2168 | 2.27 | 1.32 | 1.70 | 0 | 2 | 0.4637 ✓ | ⏳ |
| 17 | `LL5b9dR2` | ANALYST / `revenue_q1_estimate_skewness` 残差 | 2.05 | 1.68 | 0.1549 | 2.03 | 1.66 | 1.78 | 0 | 2 | 0.2204 ✓ | ⏳ |
| 18 | `e7683WbN` | ANALYST / `anl4_afv4_div_mean` 残差 | 1.94 | 1.30 | 0.2044 | 1.78 | **1.01** | 1.14 | 0 | 2 | 0.4079 ✓ | ⏳ |
| 19 | `ZYmgngv0` | **INSTITUTIONS（未点亮塔）** / `(mv_acquired/qty_acquired) − (mv_disposed/qty_disposed)` 残差 | 2.39 | 1.69 | 0.2291 | 2.23 | 1.09 | 1.06 | 0 | 2 | **0.5431 ✓** | ⏳ |
| 20 | `leAOVRb2` | **INSTITUTIONS（未点亮塔）** / 机构买卖**广度** `(buyers−sellers)/(holders+1)` 残差 | 2.56 | 1.81 | 0.2318 | 2.40 | 1.60 | 1.41 | 0 | 2 | 0.4954 ✓ | ⏳ |

- **第 11–20 颗的共同设置**：`decay 126` / `STATISTICAL` 中性化 / `truncation 0.08` /
  `pasteurization ON` / `unitHandling VERIFY` / `nanHandling OFF` / `maxTrade OFF` /
  `2014-01-01 → 2023-12-31` / `FULL`。与第 1–10 颗（decay 6 / INDUSTRY）不同，**不要混用重跑**。
- **第 11–20 颗不是 ATOM**：10 颗全部 `pyramids.effective == 2`（8 颗 `pv/analyst`，2 颗 `institutions/pv`），
  原因是残差几何以 `returns` 作回归因变量。**按用户口径（"用了PV的returns 不算 ATOM"）不得计入 ATOM**。
- **第 20 颗 `leAOVRb2` 的来历**：先用**纯字段**形状试了同一字段（`RREQro2n`，S **−0.53**，`effective=1`），
  换成残差几何后 S 2.56、`effective=2`。两组**同字段、同 backfill 66、同 STATISTICAL 中性化**，
  只差几何（纯字段 arm decay 63、残差 arm decay 126）⇒ 本报告最干净的「同字段只差几何」对照（§3.3 实验 H）。
- **第 18 颗 `e7683WbN` 余量最薄**：rob 1.01、sub 1.14 刚过 1.0 线，且 `checks.warning` 多一条
  `CLUSTER_TEST`（0.9/1，非硬失败）。**它是第 11–20 颗里最该被替换的一颗**。
- **第 19 颗 `ZYmgngv0` 的 self 最高**（0.5431，对手 `0mjk2ZQv`），仍是本池安全区；
  第 20 颗 `leAOVRb2` self 0.4954、对池最大互相关 0.4678，比前者更宽松。
- 第 11–20 颗 `checks.fail` 均为空；`warning` 只有 `MATCHES_THEMES` / `OSMOSIS_ALLOCATION`（`e7683WbN` 多 `CLUSTER_TEST`）。
- 4 颗 INSTITUTIONS 族（1–6 中的 3–6）：`pyramids.datasets` 在详情接口返回空，故**不臆造精确数据集 id**，统一记作「institutions 族」。
- **第 11–20 颗 prod 的实测状态（2026-10-28 12:05 – 13:04 多轮核查）**：平台 `check_correlation` 连续多轮
  全部返回 `status=correlation_busy`（相关性单并发槽被并行 GLB 会话长期占用），**尚无本轮有效实测**。
  `leAOVRb2` 与第 11–19 颗同样落 `correlation_busy`（`last_known=null`）。
  退避重试轨迹：`retry_after` 114.1s → 180s → 50.3s → （按点抢槽，MCP 调用超时 -32603）→ 98.5s → 超时 → 62.0s，
  即**槽位在释放瞬间就被并行会话的下一次计算重新占满**，本会话拿不到计算窗口。
  这不是本会话自争（`prod9c` 已自然结束，无本会话进程），是账号级单并发槽被外部会话持续使用。
  平台随附的 `last_known`（`age_hours≈276–278`、`stale=true`，即 2026-10-16/17 的旧实测）为：
  `kqJkPLeO 0.5254` / `j2el6dlk 0.5087` / `omowNkL2 0.5027` / `WjLwPVpk 0.5334` / `QPYrG5q5 0.4734` /
  `P0MrGA2M 0.5187` / `LL5b9dR2 0.2947` / `e7683WbN 0.4530` / `ZYmgngv0`（无记录）。
  **9/9 旧值均 < 0.70，但陈旧值不能作提交判据**（§6 `j2eo0oMO` 教训：DB/缓存值会与实时值差 0.4）。
- self 最紧的两颗仍是 institutions 族（E5VNe67L 0.6648、KPmvEYeE 0.6086），同族批量提交前要把新的 OS 池重算一次。

### 3.1 互相关（能否同篮共存）

`compute_mutual_correlation(20 ids, threshold=0.7, years=4)`，`matrix` 为 dict-of-dict，
`num_points=1023`，`max_subset_exact=true`，`missing_pnl=[]`，`max_mutually_below_subset_size=20`：

- **190 对全部 < 0.70，`pairs_over_threshold=[]`**
- 最大对 = E5VNe67L ↔ KPmvEYeE = **0.6699**；次高 ZYmgngv0↔E5VNe67L 0.6419、
  58EbwZeN↔88RoVq6V 0.6616、E5VNe67L↔88vwZE17 0.6417
- **新增 9 颗内部最紧**：`omowNkL2↔P0MrGA2M 0.6289`、`kqJkPLeO↔WjLwPVpk 0.6172`、
  `P0MrGA2M↔e7683WbN 0.5965`（同几何族，两两 0.42–0.63 之间）
- **新增 9 颗与老 10 颗最紧**：`ZYmgngv0↔E5VNe67L 0.6419`、`ZYmgngv0↔KPmvEYeE 0.5630`、
  `WjLwPVpk↔E5VNe67L 0.5616`；`58jPrvZ1` 对新增 9 颗 0.02–0.08（几乎正交）
- **第 20 颗 `leAOVRb2` 的入池核对（20 颗跑完后补测）**：对 19 颗**最大 0.4678**，
  无一对超过 0.5；`max_mutually_below_subset_size` 由 19 升到 **20** ⇒ 全池仍可同篮
- `58jPrvZ1` 对另 9 颗老池：0.1253(E567pmkK) / 0.0893(KPmvEYeE) / 0.0860(E5VNe67L) /
  0.0823(2rA0e6MN) / 0.0682(Vkx9RbJV) / 0.0483(ZYQ5J7j1) / 0.0398(58EbwZeN) / 0.0324(88vwZE17) / −0.0228(88RoVq6V)

补位候选的硬冲突（不能与现有池共存，故不入池）：
`Vkx9RbJV↔leAqNPX7 0.8425`（leAqNPX7 是全池最强 S3.56/F2.86，但 Vkx9RbJV 已在池）、
`Vkx9RbJV↔QPvJ87ng 0.7052`、`ZYQ5J7j1↔88RowlOW 0.8581`（同族取前者）。
同族兄弟 `1YjrRqeW↔58jPrvZ1 = 0.9884`（1YjrRqeW 指标更好但只在两者中取一，已选 58jPrvZ1）。

**第 20 颗补位的族内饱和实测（2026-10-28 12:09，21 颗一次性本地互相关）**：
新收的 `anl4_ptp_high/low` 残差两臂（`78Lbx868` S2.61/F2.00/rob1.63、`LLManLZ1` S2.67/F2.07/rob1.61，
`failed_ra_count=0`）与池内 `omowNkL2`（`est_ptp` 残差）**0.9301 / 0.9406** ⇒ 同族只容一颗，
`ptp` 档位已被第 13 颗占用，两臂**不能入池**（互相关判据 < 0.70）。
这也解释了为什么「同几何换字段」在第 9 颗之后边际收益趋零：残差几何把 `returns` 这个共同因子留在
分母里，**同族字段的残差时序高度同构**（池内 9 颗两两 0.42–0.63 也是同一根因）。

### 3.2 年度覆盖与逐年 Sharpe（十年约束的硬证据）

`get_alpha_yearly_stats` 实测：**20/20 颗全部覆盖 2014–2023 共 10 个完整年度**
（不足十年的候选在筛选阶段即被剔除）。

| alpha | 年度区间 | 年数 | 最差年度 Sharpe |
|---|---|---|---|
| 58EbwZeN | 2014–2023 | 10 | 0.67 |
| 88RoVq6V | 2014–2023 | 10 | 1.15 |
| E567pmkK | 2014–2023 | 10 | 1.03 |
| E5VNe67L | 2014–2023 | 10 | 1.70 |
| KPmvEYeE | 2014–2023 | 10 | 1.45 |
| 88vwZE17 | 2014–2023 | 10 | **0.30** |
| 2rA0e6MN | 2014–2023 | 10 | 0.82 |
| Vkx9RbJV | 2014–2023 | 10 | 1.66 |
| ZYQ5J7j1 | 2014–2023 | 10 | 0.37 |
| 58jPrvZ1 | 2014–2023 | 10 | **−0.55（2015）** |
| kqJkPLeO | 2014–2023 | 10 | 1.40（2021） |
| j2el6dlk | 2014–2023 | 10 | **0.57（2015）** |
| omowNkL2 | 2014–2023 | 10 | 1.05（2021） |
| WjLwPVpk | 2014–2023 | 10 | 1.09（2021） |
| QPYrG5q5 | 2014–2023 | 10 | **−0.31（2015）** |
| P0MrGA2M | 2014–2023 | 10 | 0.71（2021） |
| LL5b9dR2 | 2014–2023 | 10 | **0.51（2017）** |
| e7683WbN | 2014–2023 | 10 | 0.82（2015） |
| ZYmgngv0 | 2014–2023 | 10 | 0.85（2015） |
| leAOVRb2 | 2014–2023 | 10 | **1.25（2015）** |

- 负值年只有两颗：`58jPrvZ1`（2015 −0.55）、`QPYrG5q5`（2015 −0.31）。
- 弱年聚集在 2015 与 2021（IND 小盘两段逆风），提交排序按 §8 建议。
- `58jPrvZ1` 逐年：2014 2.39 / 2015 **−0.55** / 2016 1.84 / 2017 2.27 / 2018 0.62 / 2019 2.22 /
  2020 2.29 / 2021 1.01 / 2022 2.67 / 2023 1.82。
- `leAOVRb2` 逐年：2014 5.70 / 2015 **1.25** / 2016 1.95 / 2017 1.27 / 2018 2.57 / 2019 3.02 /
  2020 3.65 / 2021 1.62 / 2022 2.62 / 2023 2.22 —— **十年无负年**，最差年 1.25 也在 1.0 以上。

### 3.3 归因分析与对比实验（2026-10-28 追加）

这一节回答「这批为什么能过闸、下一批该往哪挖」。全部数字来自平台实测，**推断部分单独标注**。

#### 实验 A：字段族 → rob 的受控对比（Form E 9 臂，同几何同设置，仅换 F）

| 字段族 | 成员 | rob 逐个 | rob 均值 | sub 均值 | S 均值 |
|---|---|---|---|---|---|
| 分析师预期**分布矩**（分歧/偏度/离散系数） | `eps_y1_estimate_coeff_var` / `eps_y1_estimate_skewness` / `eps_y1_cagr_2yr` | 2.02 / 1.82 / 1.75 | **1.86** | 1.92 | 2.69 |
| 预期**水平**（EPS / 目标价点估计） | `anl44_eps_best_eeps_cur_yr` / `est_ptp` / `anl4_afv4_eps_low` | 1.70 / 1.64 / 1.32 | 1.55 | 1.75 | 2.76 |
| 收入预期分布偏度 | `revenue_q1_estimate_skewness` | 1.66 | 1.66 | 1.78 | 2.05 |
| 单一截面分歧量 | `anl4_afv4_div_mean` | **1.01** | 1.01 | 1.14 | 1.94 |
| 机构交易金额/股数比 | `(mv_acquired/qty_acquired) − (mv_disposed/qty_disposed)` | 1.09 | 1.09 | 1.06 | 2.39 |

- **结论 1（rob 维度）**：预期分布的**形状**比**水平**更 robust（1.86 vs 1.55）；单一截面分歧量最差（1.01，
  贴着 1.0 线），机构资金流形式的残差也弱（1.09）。
- **字段语义取证**：`eps_y1_estimate_coeff_var` / `eps_y1_estimate_skewness` 的描述由同族字段反证 ——
  `get_datafields(IND)` 实测 `revenue_q1_estimate_coeff_var` = "Coefficient of variation (std/mean) of Q1
  revenue estimates"、`eps_q2_estimate_skewness` = "Pearson's skewness of the forecast Q2 EPS estimate
  distribution" ⇒ 二者是**分析师分歧度**而非水平量。
- **机制解释（推断，非实测）**：残差几何 `rank(−ts_regression(z(returns), z(F)))` 提的是「F 相对股价的领先量」。
  对分布矩字段，这个领先量编码**分析师群体认知的漂移**（分歧扩大/收缩先于价格反应）；对水平字段，它更接近
  「目标价相对价格的距离」，在 TOP500（小盘权重更高）子宇宙里噪声更大 ⇒ rob 更低。
- **预注册检验**：补第 20 颗的 `anl4_ptp_high/low` 两臂正是本假设的对照点 —— 若「水平类」成立，rob 应落在
  1.3–1.7 而**不应** >1.8。实测 rob **1.63 / 1.61**（S2.61/2.67），落在预测区间内 —— 假设成立；
  但这两臂与池内 `omowNkL2`（`est_ptp` 残差）互相关 **0.9301 / 0.9406** ⇒ 指标达标却不可同篮（§3.1）。

#### 实验 B：几何对比（同一信号概念，两条几何）

| 几何 | 定义 | 实测 | 结论 |
|---|---|---|---|
| `rg_grdev` | `signed_power(subtract(group_rank(dev(F,252), sector), 0.5), 3)` | 4 臂 COMPLETE：rob **0.89 / 0.57 / 0.22 / 0.35**（S 最高 1.85） | **全灭** |
| Form E | `rank(−ts_regression(z(returns,252), z(F,252), 252, rettype=0))` + decay 126 | 9 臂全过：rob **1.01–2.02** | **可用** |

⇒ 同样的「分析师/基本面字段 + 与价格的关系」，**残差回归几何在 IND 的 robust 子宇宙上系统性优于
组内秩偏离 + 三次幂几何**。这是把 `rg_grdev` 判死（而非继续调参）的依据：4 臂跨度 0.22–0.89，
失败是几何性的，不是某一档参数运气差。

#### 实验 C：decay / 滞后轴（同字段 `ern3_pre_interval`）

| alpha | 形状差异 | S | 2Y | rob | TO |
|---|---|---|---|---|---|
| `akV5kJl6` | `ts_delay(F,21)` + **decay 126** | 2.39 | **1.27 ✗** | **1.89** | 0.222 |
| `O0JLKQR7` | 无滞后 + **decay 252** | 1.88 | **1.07 ✗** | 1.17 | 0.223 |

⇒ 拉长 decay（126→252）**没有降低换手**（0.222→0.223），却让 S −0.51 / 2Y −0.20 / rob −0.72。
两点结论：① 该族的换手由字段自身特性决定，decay 不是压换手杠杆；② decay 甜区在 126 附近，
再拉长是纯损失。两条的 2Y 都不达 1.58，故都不是候选（§6.1）。

#### 实验 D：换手目标 vs 平滑器（`unlit4` 三臂）

`QPvJRG8p` / `88RoWpMm` / `KPJ0AGWl`：S 2.32–3.02，**唯一失败项是 HIGH_TURNOVER**（实测 0.4116 / 0.4880，
硬线 0.40）；把 `target_tvr` 从 0.40 降到 0.35 / 0.30 重跑 ⇒ 全部 ra=0。
⇒ IND 的 `ts_target_tvr_hump` 要在目标值上留 **≈0.05 下偏余量**：平台实测换手系统性高于 target。

#### 实验 E：Form D 纯字段几何的泛化性检验（2026-10-28 12:22 追加，负结果）

把第 10 颗（`58jPrvZ1`，Form D，S3.35、`effective=1`）的形状**原样**套到另两个字段上：

```
signed_power(subtract(group_rank(divide(subtract(ts_backfill(F,22), ts_mean(ts_backfill(F,22),252)),
  add(abs(ts_mean(ts_backfill(F,22),252)),1)), sector), 0.5), 3)
```

| 臂 | 字段（塔） | Sharpe | Fitness | TO | 失败项 |
|---|---|---|---|---|---|
| `leAOr3R5` | `anl4_ptp_high`（ANALYST） | 1.01 | 0.60 | 0.0683 | LOW_SHARPE / LOW_FITNESS / LOW_ROBUST / LOW_2Y |
| `A1VZk7gW` | institutions 买卖均价差（**未点亮塔**） | 0.32 | 0.10 | 0.0677 | 同上四项 |

- **结论 1：Form D 的 3.35 不是「形状」的功劳**，是「EBT 年度估计离散度 + 组内秩三次幂」这一特定化学反应；
  换字段即崩到 0.32–1.01 ⇒ **该形状不可泛化**。
- **结论 2（对照组，本轮最强的一条归因）**：同两个字段换成残差几何（Form E）⇒ S **2.61 / 2.67**、全闸 0 失败。
  ⇒ **收益来源是「扣掉市场共同因子」这一步，不是字段本身**；而扣因子必然把 `returns` 带进表达式 ⇒
  `pyramids.effective` 从 1 变 2。**「ATOM」与「强度」在 IND 是同一个几何约束的两端，不能兼得**。

#### 实验 F：EARNINGS 未点亮塔两条路径的负结果（2026-10-28 12:30 追加）

**F-1 残差几何 × 转录情绪（失败）**：`88R9LdZm` = `rank(-ts_regression(ts_zscore(returns,252),
ts_zscore(ts_backfill(vec_avg(ern11_composite_sentiment_score),60),252), 252, rettype=0))`，设置同第 11–19 颗。

权威读数（`batch_get_alpha_metrics` + `get_alpha_details`）：**S 1.15 / F 0.73 / TO 0.1399 / 2Y 1.33 /
rob 1.06 / sub 1.26**，`failed_ra_count=3`（LOW_SHARPE / LOW_FITNESS / IS_LADDER_SHARPE）。
`pyramids.effective=2`（pv+earnings）——残差几何照旧不带 ATOM。

- **口径教训（必须记住）**：收割脚本打印的 `checks.fail=[]` **不可作判据**。该臂三项失败被平台放在
  `checks.warning` 里（`LOW_SHARPE value 1.15 limit 1.58`），`fail` 数组确实为空。**「零 fail」≠「过闸」**，
  必须以 `ra.failed_ra_count` / `ra.ra_failed_checks` 为准（与 AGENTS §8.7 的 RA 口径同源）。
- 归因：转录文本情绪（`alphaCount 83`，拥挤度极低）在 IND **信息强度不够**——拥挤度低不等于有效。

**F-2 事件稀疏字段必须用长 backfill（根因诊断）**：同批 `MPYRxon9`（`eps_change_percentage_value` 残差）
返回 **S 0.0 / TO 0.0**、失败 `LOW_SHARPE / LOW_TURNOVER / CONCENTRATED_WEIGHT`，即**几乎无持仓**。

根因定位：该字段是季度事件型（VECTOR，coverage 0.3647），平均事件间隔约 63 个交易日，而表达式用
`ts_backfill(..., 60)` ⇒ 填不满间隔、序列带空隙，`ts_zscore(...,252)` 需要连续窗口 ⇒ 大面积 NaN ⇒ 秩化后
几乎没有可交易标的。**规则：事件型字段的 `ts_backfill` 窗口必须 > 事件间隔（季度 ⇒ ≥ 252）**。

#### 实验 G：纯字段 ATOM 的第三次反证（2026-10-28 12:30 派发 / 12:37 收割，两臂全灭）

设计意图：Form D 只在 `58jPrvZ1` 成功过一次，为判断「纯字段形状能否在别的塔复现」，用**最朴素的
`rank` 形状**（不带组内秩、不带三次幂）测两个未点亮塔的经济上最强的字段。两臂都实测
`pyramids.effective = 1`（`IND/D1/INSTITUTIONS`、`IND/D1/EARNINGS`）⇒ **纯字段路线确实产出 ATOM**。

| 臂 | 表达式要点 | S | F | TO | 判读 |
|---|---|---|---|---|---|
| `RREQro2n` | 机构**买卖广度**比：`(buyers − sellers)/(holders+1)`，institutions6 | **−0.53** | −0.22 | 0.0734 | 符号反成 +0.53 也远低于 1.58 ⇒ 该字段 IC 量级不足 |
| `MPYRxnKa` | EPS surprise：`(actual − estimated)/|estimated|`，earnings6 | 0 | — | **0（zero-trade）**，`longCount=0/shortCount=0` |

- `MPYRxnKa` 把 `ts_backfill` 从 60 拉到 **252**（覆盖季度事件间隔）后**仍是 0 持仓** ⇒ 根因不是回填窗口，
  而是 **earnings6 的 VECTOR 字段经 `vec_avg` 后不可用**（2/2 臂 zero-trade）。该数据集在本区**判死**。
- 至此纯字段 ATOM 的**四类字段**全灭：分析师点估计（`anl4_ptp_high` S1.01）、机构买卖均价差（S0.32）、
  机构买卖广度（S−0.53）、EPS surprise（0 持仓）。**唯一能同时给 ATOM 与强度的字段族是
  `risk68_residual_return`（它本身就是残差收益，S2.76/3.35）**，而该族在池里已占 2 颗、族内互相关 0.6616，
  第 3 颗必然越线 ⇒ **ATOM 在 IND 的可挖上限已到**（本轮 3/20 = 15.0%）。

#### 实验 H：同字段、同 backfill、只差几何（第 20 颗的直接对照，2026-10-28 12:30 两批并行派发）

这是全场最干净的一组对照：**同一个字段**（institutions6 机构买卖广度 `(buyers−sellers)/(holders+1)`）、
**同一 backfill 窗口 66**、**同一 STATISTICAL 中性化**、同一 2014–2023 / FULL，**只有几何不同**。

| 臂 | 几何 | decay | S | F | TO | rob | eff |
|---|---|---|---|---|---|---|---|
| `RREQro2n` | 纯字段 `rank(F)` | 63 | **−0.53** | −0.22 | 0.0734 | 失败 | **1（ATOM）** |
| `leAOVRb2` | 残差 `rank(−ts_regression(z(returns), z(F), 252, rettype=0))` | 126 | **2.56** | 1.81 | 0.2318 | **1.60** | 2 |

- **几何把同一个字段从 −0.53 抬到 2.56**（差 3.09 个 Sharpe，符号翻转）。同一个字段在同一区域、
  同一覆盖率、同一十年窗口上「没信号」与「强信号」的区别，全部来自**扣掉市场共同因子**这一步。
- 代价只有一项且不可规避：`returns` 进入表达式 ⇒ `pyramids.effective` 1→2。
  ⇒ 这是「ATOM ↔ 强度」在**单字段层面**的定量证据（前三次反证见实验 E/G，机制归因见 D0）。
- 副产品：纯字段组当时用了 decay 63（短 decay），残差组 decay 126 —— 但实验 C 已独立证明
  decay 只影响换手/S 的小幅摆动（126→252 时 TO 0.222→0.223、S −0.51），**不足以解释 3.09 的差距**，
  故结论归给几何而非 decay。

#### 归因 D0：ATOM 的结构性边界（实测反证）

- Form E 9 颗全部 `pyramids.effective = 2`。原因不是「两条信号相加」，而是 **`returns` 作 `ts_regression`
  因变量时被平台计入 PV 数据集归属** ⇒ **残差几何在结构上不可能产出 ATOM**（与用户裁定「kqJweZQz
  用了 PV 的 returns 不算 ATOM」同一口径）。
- 要 ATOM 只能走**纯字段变换**形状：Form D（`58jPrvZ1` = 单字段组内秩 + 三次幂，`effective=1`）。
  代价是强度：Form D 全池最弱（S1.64 / F1.27 / TO0.1142，2015 年 −0.55）。
- ⇒ **本轮实测的 ATOM–强度权衡**：20 颗里 3 颗 ATOM（S 1.64 / 2.76 / 3.35），17 颗非 ATOM 的 S 集中在
  1.94–3.20。**ATOM 不是靠挑选得到的，是几何决定的**。


## 4. 表达式原文（口径证据）

- Form A（Vkx9RbJV / ZYQ5J7j1 系，`target_tvr` 取 0.30–0.35）：
  `rank(-ts_regression(ts_zscore(returns, W), ts_zscore(ts_delay(ts_backfill(F,22), L), Z), W, rettype=0))`
  → 分组秩化 → `ts_target_tvr_hump(ts_mean(..., industry), 5, target_tvr=X)`
- Form B（2rA0e6MN 系）：同一残差形状 → `ts_decay_linear(<resid>, 12)`
- Form D（`58jPrvZ1`，ANALYST 原生离散度，非残差形状）：

  ```
  signed_power(subtract(group_rank(divide(subtract(ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22),
    ts_mean(ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22), 252)),
    add(abs(ts_mean(ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22), 252)), 1)), sector), 0.5), 3)
  ```

- **Form E（第 11–19 颗 + 第 20 颗，裸残差 rank，本轮新族）**：
  `rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(F, 252), 252, rettype=0))`
  → 直接作 alpha（无平滑器、无分组中性化；`decay 126` 在设置层完成换手压制）。
  10 条原文（F 逐条替换）：

  | alpha | F |
  |---|---|
  | `kqJkPLeO` | `anl44_eps_best_eeps_cur_yr` |
  | `j2el6dlk` | `eps_y1_estimate_skewness` |
  | `omowNkL2` | `est_ptp` |
  | `WjLwPVpk` | `eps_y1_cagr_2yr` |
  | `QPYrG5q5` | `eps_y1_estimate_coeff_var` |
  | `P0MrGA2M` | `anl4_afv4_eps_low` |
  | `LL5b9dR2` | `revenue_q1_estimate_skewness` |
  | `e7683WbN` | `anl4_afv4_div_mean` |
  | `ZYmgngv0` | `(market_value_institutional_shares_acquired / quantity_institutional_shares_acquired) − (market_value_institutional_shares_disposed / quantity_institutional_shares_disposed)` |
  | `leAOVRb2` | `ts_backfill((count_institutional_buyers_security − count_institutional_sellers_security) / (count_institutional_holders_security + 1), 66)`（**唯一带 backfill 的一条**：源字段是稀疏事件型） |

  `leAOVRb2` 完整原文：

  ```
  rank(-ts_regression(ts_zscore(returns, 252), ts_zscore(ts_backfill(divide(subtract(count_institutional_buyers_security,
    count_institutional_sellers_security), add(count_institutional_holders_security, 1)), 66), 252), 252, rettype=0))
  ```

四条形状都不是多信号相加：`returns` 仅作 Form A/B/E 的残差因变量；`ts_target_tvr_hump` / `ts_decay_linear`
是同一信号的换手平滑器；Form D 是单一字段的组内秩变换。

## 5. 塔覆盖（当前当季 pyramid 口径）

`get_pyramid_alphas()` 实测 IND/D1（≥3 颗 = 点亮）：
`insiders 0 / news 4 / other 4 / pv 8 / analyst 3 / model 3 / macro 2 / imbalance 0 / fundamental 3 /
option 0 / sentiment 0 / shortinterest 0 / earnings 1 / risk 1 / institutions 1`。

> **本节是 2026-10-28 交付时点的快照。** 同日随后又跑了「未点亮塔覆盖扩展」
> （`IND / unlit28` 39 行 + `IND / unlit28b` 28 行，共 67 行；详见
> [`ind_unlit_tower_expansion_20261028.md`](ind_unlit_tower_expansion_20261028.md)），
> 并在收尾时复核当季塔位：`risk 3`（已点亮）、`institutions 1`、`earnings 1`、`macro 2`，
> 其余 `option / sentiment / shortinterest / insiders / imbalance` 仍为 0。
> 两处快照不一致的只有 `risk`（1→3），其余行不受影响；具体是哪 2 颗进了 RISK 计数未在本轮核实（`get_pyramid_alphas` 只回计数，须查 `get_user_alphas` 方能定位）。

| 塔 | 状态 | 本轮产出 | 备注 |
|---|---|---|---|
| RISK | **未点亮 1/3**（mult 1.0） | **2 颗（均 ATOM）**：`58EbwZeN`、`88RoVq6V` | **两颗全交即点亮**；O0AYgqAJ 因 prod 0.7226 剔除 |
| INSTITUTIONS | **未点亮 1/3**（mult 1.0） | **6 颗**：`E567pmkK`、`E5VNe67L`、`KPmvEYeE`、`88vwZE17`、`ZYmgngv0`、`leAOVRb2` | **任交 2 颗即点亮**；ZYmgngv0 为买卖均价差、leAOVRb2 为买卖**广度**，二者同塔不同字段 |
| SENTIMENT | **未点亮 0/3**（mult 1.2） | **1 颗**：`Vkx9RbJV` | `RRE3g7Ne` prod 0.7058 被硬闸淘汰；`leAqNPX7`（S3.56/F2.86）与 Vkx9RbJV 0.8425 不可共存；`news_sentiment_transfer` 两批 16 臂全灭 |
| IMBALANCE | **未点亮 0/3**（mult 1.0） | **1 颗**：`ZYQ5J7j1` | 同族 `88RowlOW`（S2.32）与它 0.8581 互斥，作落选备选 |
| ANALYST | 已点亮（mult 1.4，最高） | **9 颗**：`58jPrvZ1`(ATOM) + 8 颗残差 | flash-estimate 族本轮首次成批出成品（Form E） |
| FUNDAMENTAL | 已点亮（mult 1.2） | 1 颗 | `2rA0e6MN` |
| MODEL | 已点亮（mult 1.2） | **0 颗** | `RR7vlM2o` 刷新后 prod **0.8219** 出局 |
| EARNINGS | **未点亮 1/3**（mult 1.1） | 0 颗 | earnings3 第二颗：F 0.91→1.03 但 Sharpe 1.48 触发 LOW_SHARPE，已止 |
| MACRO | **未点亮 2/3**（mult 1.0） | 0 颗 | macro63 唯一 ALIVE 字段单用无信号；全部强结果都是 `add(PV残差, mcr63_membership)`，**违反约束 5** |
| OPTION | **未点亮 0/3**（mult 1.2） | 0（塔位放弃） | option1 四臂全灭（S 0.24–0.60）；option30 唯一 ALIVE 臂 S1.29/F0.62 四闸齐挂 |
| INSIDERS | **未点亮 0/3**（mult 1.2） | 0 | 唯一字段 `insd5_nm_kor` 是韩文人名 VECTOR |
| SHORTINTEREST | **未点亮 0/3**（mult 1.0） | 0 | 3 个字段实为涨跌停比率，历史最佳 S 0.22 |

**诚实说明**：20 颗里 **10 颗落在未点亮塔**（RISK 2 / INSTITUTIONS 6 / SENTIMENT 1 / IMBALANCE 1），
**10 颗落在已点亮塔**（ANALYST 9 / FUNDAMENTAL 1）。未点亮塔的字段池本身贫瘠——insiders 唯一字段是
韩文人名、shortinterest 三字段是涨跌停比率、option1 四臂全灭、option30 唯一 ALIVE 字段四闸齐挂、
sentiment26 18 字段全 DEAD/UNUSABLE、macro63 只能靠 PV 组腿。真正有产出的是 institutions / risk68 /
sentiment21 / imbalance5 与 **analyst flash-estimate（本轮新开）**。

**两条本轮经验**：
1. **IND 的 `LOW_ROBUST_UNIVERSE_SHARPE` 是几何问题，不是参数问题**：`rg_grdev` 族（signed_power 的
   group_rank 偏离度）4 臂实测 rob **0.22 / 0.35 / 0.57 / 0.89**，全部 < 1.0 而 S 最高 1.85 ⇒ 整族判死。
   同一批残差几何 `rank(-ts_regression(zscore(returns), zscore(F)))` 8/8 过闸，**差别只在「扣不扣掉市场共同因子」**。
2. **decay 是残差族的换手开关**：同一表达式 decay 6 换手 ~0.45–0.55（超硬线 0.40），
   抬到 **decay 126** 后落到 0.15–0.23，且 Sharpe 不降 ⇒ 该族不要再用 `ts_target_tvr_hump` 压换手。

## 6. 排除清单（附理由，避免重复挖）

| alpha / 批次 | 结论 | 理由 |
|---|---|---|
| `RR7vlM2o` | 弃（MODEL ATOM） | **prod 刷新实测 0.8219** > 0.70 ⇒ 族级必死；由 `58jPrvZ1` 补位 |
| `O0AYgqAJ` | 弃 | **prod 实测 0.7226**；直方图 [0.7,0.8) 桶 n=1 ⇒ 族级必死，不做窗口救活 |
| `RRE3g7Ne` | 弃 | **prod 实测 0.7058**；[0.7,0.8) 桶 n=2 ⇒ 族级必死，不救 |
| `MP0Jx9Yn` / `MP0JNAGn` | 弃 | prod **0.7859 / 0.7857**，双双超线且远离可救区间 |
| `gJWnrZgg` | 弃 | prod 0.6998 名义在线下（余量 0.0002），但与 `78oeRVzO` 同 **fnd86 簇**，该簇 [0.7,0.8) 桶 n≥1 ⇒ 族级必死 |
| `78oeRVzO` | **不是候选** | 全闸漂亮（prod 0.6835、对池 max −0.0158、eff=1），但 `status=ACTIVE`、`dateSubmitted=2026-10-26` ⇒ 已提交存量 |
| `j2eo0oMO` | 弃 | 平台 self 刷新 **0.7041** > 0.70（新对手 `0mjk2ZQv`）。⚠ DB 记的 self=0.2925 是陈旧值 ⇒ **DB 的 self/prod 列不能作判闸依据** |
| `pw52P3jb` / `wpbQjeKp` / `wpjrMnz5`（`search_alphas_by_sharpe` 高 S 榜） | **不是候选** | 实测均 `status=ACTIVE` / `stage=OS` / `tags=["CH_SUPER"]` / `dateSubmitted` 2026-09~10 ⇒ 已提交的 SUPER 存量。**高 S 榜必须看 status/stage** |
| `rg_grdev_p3_sec` 7 臂 | **族判死** | 4 条 COMPLETE：rob **0.89 / 0.57 / 0.22 / 0.35** 全部 <1.0（S 最高 1.85）；另 3 条 `add` 量纲不兼容 WARNING |
| institutions6 六颗（`bl8210Wq` / `mLYdVKap` / `VkdZ3wKM` / `gJWXMXNl` / `RRA91Z01` / `78o31b2Q`） | 弃 | 与既有池各 ≥2 对 ≥0.70（max 0.993 为族内） |
| `omLwErNm` | 弃 | `LOW_2Y_SHARPE` 实测 **1.44 < IND limit 1.58** |
| `P02rXRAp` | 弃 | 全闸通过（eff=1、self 0.5499）但 **prod 0.9643** ⇒ PV 日内反转概念与 prod 池重仓 |
| `xA392Xpb` | 弃 | self-corr **0.7011** > 0.70 硬拦 |
| `leAqNPX7` / `QPvJ87ng` / `88RowlOW` | 弃（88RowlOW 留备选） | 与池内 Vkx9RbJV 0.8425 / 0.7052，ZYQ5J7j1 0.8581 互斥 |
| `bl6kAV6M` | 弃 | 与 O0AYgqAJ 同信号族（冗余），且 ra 含 IS_LADDER_SHARPE |
| `MPYW2NWM`（earnings3 #2） | 弃 | LOW_SHARPE(1.48) + IS_LADDER 双硬失败 |
| `0mYl59j1` / `E567xY6G` | 弃 | LOW_ROBUST_UNIVERSE_SHARPE 硬失败 |
| `78LA2R9L` / `LLMj2YJ2` / `WjOqJzMQ` / `leAq1Gd2` / `E567xz1m` | 弃 | ra 失败 3–4 项 |
| option1 四臂 / option30 四臂 | 塔位放弃 | option1: S 0.24–0.60；option30 `option_daily_traded_contracts`: S1.29/F0.62 + 4 项 ra 失败 |
| `QPvJRG8p` / `88RoWpMm` / `KPJ0AGWl`（unlit4 三臂） | 弃（已由 unlit5 修复版替代） | 只卡 HIGH_TURNOVER（0.413–0.488>0.40） |
| `78odJop1` / `e72L9vq6` / `6XqzlA5K` / `npAEleVa` / `wp91wGx2` | 弃 | 与既有池互相关 > 0.7 或指标不足 |
| risk71 三颗 | 弃 | 指标合格但与既有 risk 族互相关 > 0.7（同源信号） |
| `news_sentiment_transfer` 两批 16 臂 | **数据集判死** | 批 1 最好 S1.04/F0.37；批 2 最好 S0.77/F0.17，全批 TO≈0.53–0.58、多项 2Y 为负 |
| `shortinterest5` 三字段 | 数据集判死 | 字段实为涨跌停比率，历史最佳 S 0.22 |
| `macro63` | 判死（约束 5 冲突） | 唯一 ALIVE 字段单字段 S=0；强结果全是 `add(rank(PV残差), mcr63_membership)` 两条腿 |
| `insiders5` | 数据集判死 | 唯一字段 `insd5_nm_kor` 是韩文人名 VECTOR |
| `sentiment26` | 数据集判死 | 18 字段全 DEAD / UNUSABLE |

### 6.1 存量 IND alpha 全量盘点（2026-10-28 12:00 追加；**零回测成本路径**）

目的：在不占回测槽的前提下找第 20 颗。取证 = `get_user_alphas(stage=IS, region=IND, type=REGULAR,
limit=100, order="-is.sharpe")` → 38 行 + `batch_get_alpha_metrics` 12 颗 + `get_alpha_details` 3 颗 +
`check_self_correlation` 1 颗。**结论：存量无一可直接补位**，但排掉了一批未来会重复挖的对象。

| alpha | 实测 | 结论 |
|---|---|---|
| `1YjMln26` | S3.91 / F2.95 / TO0.306 / 2Y2.17 / rob1.28 / sub1.47 / **ra=0**；`pyramids.effective=1`（IND/D1/PV）⇒ **全闸过且是 ATOM** | **出局：`check_self_correlation` = 0.7411 > 0.70**（对手 `wpZ1vYzY`，pool 50 / full 57 / 排除 PP 7）。存量里唯一近成品，只差 self 墙 |
| `ZY7X0Jz8` | S1.76 / F1.36 / TO0.10 / 2Y1.78 / rob1.03 / sub1.04 / **ra=0**；eff=1（PV） | 出局：表达式 `add(group_rank(tc_max/tc_median, industry), multiply(-0.2, group_rank(ts_delta(pv106_wli_spreadbp,151), industry)))` = **两条腿加权相加** ⇒ 违反约束 5 + 「禁腿相加」 |
| `zqbGoLpK` | S2.62 / F2.01 / TO0.21 / 2Y2.03 / rob1.14 / sub1.34 / **ra=0** | 出局：`trade_when(PV条件 cap, oth532 信号)` 且 `effective=2`（PV+OTHER）⇒ 违反约束 5 |
| `WjL5aw3d` | S**4.60** / F2.37 / **TO 0.831** | 出局：HIGH_TURNOVER（硬线 0.40）。`rsk68_weight_edadv` 族，其 hump 版 `bl6kAV6M` 已因 IS_LADDER 出局 |
| `akV5kJl6` / `O0Jl0ekb` | S2.39/2.30、F1.75/1.65、rob **1.89/1.89**（本区最强 rob）、TO 0.222/0.223 | 出局：唯一失败是 **2Y 1.27 / 1.37 < 1.58**。ern3 同族同几何（decay 126），两条互斥 ⇒ 若要抢救**只需一条** |
| `N1Nmjmd8` / `E5R0o0q1` | rob 0.80 / 0.59 | 出局：rg_grdev 族同几何，rob 墙（该族已判死） |
| `MLjnnzKE` | `GET /alphas/MLjnnzKE` → **404 Not Found** | 已被删除，不入候选（曾 S2.90/F2.40） |
| `leKV1GbN` / `Wj7rjAKZ` / `ZYQ5gdz3` / `LLMj90kM` / `XgRpWAW8` / `pwRXMRjX` / `3qlGbd3z` / `WjOQXQ5O` / `RR1YnMaz` / `le32pdG8` / `LLXo6bwL` / `e72M9p6d` | 2Y 分别 0.73/1.81/1.98/0.96/1.49/2.77/1.72/2.51/2.74/2.40/0.50/1.80；rob 0.78/0.78/0.52/1.00/0.93/0.84/0.65/0.89/0.87/0.95/0.59/0.92 | 出局：ra ≥ 1（rob / 2Y / sub 至少一项在线下） |
| `vRkE9GAd` | S1.80 / F1.31 | 出局：`add(multiply(0.5,·), multiply(0.5,·))` = 两腿加权 ⇒ 约束 5 + 禁腿相加 |
| `78Lbx868` / `LLManLZ1` | `anl4_ptp_high/low` 残差（c4 批，全闸 0 失败：S2.61/2.67、F2.00/2.07、2Y2.87/2.56、rob1.63/1.61、sub1.86/1.93） | 出局：与池内 `omowNkL2` **0.9301 / 0.9406** 互相关 ⇒ 同族（ptp 档）已占，`add` 不进池。**指标达标但不可同篮**，留作该族备份替换件 |

## 7. 复现与核验命令（全部走 MCP）

```bash
# 1) 候选指标（20 颗一次）
python tools/mcp_http_caller.py --service wq-brain-http --session-file cache/_mcp_sess_alt \
  batch_get_alpha_metrics @<metrics-args>.json

# 2) 金字塔归属（ATOM 判据 = pyramids.effective == 1）
python tools/mcp_http_caller.py --service wq-brain-http --session-file cache/_mcp_sess_ctx \
  get_alpha_details @<details-args>.json

# 3) 本地互相关（不占平台相关性槽；matrix 可复用抽任意子集）
python tools/mcp_http_caller.py --service wq-brain-http --session-file cache/_mcp_sess_c \
  compute_mutual_correlation @<20 ids 的 args>.json

# 4) self（本地 OS 池）/ prod（平台，单飞；busy 时按顶层 retry_after 退避）
python tools/mcp_http_caller.py --service wq-brain-http --session-file cache/_mcp_sess_sc \
  check_self_correlation @<args: alpha_id + correlation_type=self>.json
python tools/mcp_http_caller.py --service wq-brain-http --session-file cache/_mcp_sess_prod \
  check_correlation @<args: alpha_id + correlation_type=production + refresh=true>.json

# 5) 十年覆盖
python tools/mcp_http_caller.py --service wq-brain-http --session-file cache/_mcp_sess_c \
  get_alpha_yearly_stats @<args: alpha_id>.json
```

判据：`ra.failed_ra_count == 0`（**不要用 `checks.fail` 判**，硬失败可能落在 `checks.warning`）+ self<0.70 + prod<0.70 +
近十年 10 个年度全有 PnL + 塔位未点亮优先 + 20 颗两两 <0.70。
`prod` 与 `self` **必须平台/本地实测**，不得取 DB 缓存（§6 `j2eo0oMO`）。

## 8. 下一步（未执行）

1. **第 20 颗已落地：`leAOVRb2`（INSTITUTIONS 未点亮塔，机构买卖广度残差）**。补位路径与四条负结果：
   ① **同几何换字段已饱和**：`anl4_ptp_high/low` 两臂全闸 0 失败（S2.61/2.67），但与池内 `omowNkL2`
   互相关 **0.9301 / 0.9406** ⇒ 不可同篮（§3.1）；
   ② **纯字段 ATOM 2 臂全灭**：`RREQro2n` S−0.53、`MPYRxnKa` 0 持仓（backfill 拉到 252 仍 zero-trade
   ⇒ earnings6 本区判死，§3.3 实验 G）；
   ③ **同字段只差几何**：广度字段纯字段 −0.53 → 残差 +2.56（§3.3 实验 H），
   代价是 `effective` 1→2；④ **存量路径已穷尽**（§6.1 的 19 颗非池 IND alpha 无一可直补）。
   ⇒ 现池 20/20：IS 全闸通过、RA 失败 0、十年覆盖 20/20、self 全 <0.70、190 对互相关全部 <0.70。
2. **待测：第 11–20 颗共 10 颗 prod**。`check_correlation` 的相关性单并发槽被并行 GLB 会话持续占用
   （`correlation_busy`，本窗口 `retry_after` 114→180→50→98→62s，两次按点抢槽均以 MCP 超时 -32603 告终），
   本会话按顶层 `retry_after` 退避重试共 6 轮，仍无一笔本轮有效值。
   **prod ≥ 0.70 即出局，不得跳测、不得用 `last_known` 陈旧值代替**（§6 `j2eo0oMO`）。
   槽位空出后按 `leAOVRb2` → `kqJkPLeO`…`ZYmgngv0` 顺序补测即可（每颗一次 refresh=true）。
3. **提交前逐颗**：用户明确确认 → `submit_verdict` 预检（**只能拦不能放**）→ 当季 pyramid 点亮状态复读
   → `check_correlation(refresh=true)` 复测 self/prod → `workflow_submit_alpha(confirm_submit=True)`。
4. **建议提交顺序**（仅建议，未执行）——按「塔乘子 × 互相关余量 × 弱年风险」：
   `58jPrvZ1`（ANALYST 1.4 ATOM，最正交）→ `Vkx9RbJV`（SENTIMENT 未点亮，须先复测 prod）
   → `2rA0e6MN`（FUNDAMENTAL 1.2）→ `88RoVq6V` / `58EbwZeN`（RISK 双 ATOM，**交完即点亮 RISK**）
   → `E567pmkK` / `E5VNe67L`（**任交两颗即点亮 INSTITUTIONS**）→ `KPmvEYeE` → `88vwZE17`
   → `ZYQ5J7j1`（TO 0.3669 最高 + 2023 弱年，末位）。
   第 11–20 颗建议排在上述之后（同几何族，先交老池避免自我竞争）；
   其中 `leAOVRb2`（S2.56 / rob1.60 / 十年无负年 / 对池最大 0.4678）是第 11–20 颗里质量最好的一颗，
   可作为 INSTITUTIONS 点亮的第 2 颗与 `E567pmkK` 配对。
5. **三颗需要用户拍板的弱点**：
   - `Vkx9RbJV` prod 0.6939，余量仅 0.0061（再测上浮即出局，备选 `88RowlOW` 与 ZYQ5J7j1 互斥）；
   - `58jPrvZ1` 2015 年 Sharpe −0.55 + 池内最弱指标，换来 ATOM/最高乘子/正交性；
   - `e7683WbN` rob 1.01 / sub 1.14 贴线，且 `CLUSTER_TEST` warning —— 建议优先替换它（备选 `78Lbx868`，
     全闸 0 失败，但需先与 `omowNkL2` 二选一，二者 0.9301 不可同篮）。
6. 本轮**不提交**任何 alpha；20 颗保持 UNSUBMITTED。
