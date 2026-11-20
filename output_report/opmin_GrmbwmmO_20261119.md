# GrmbwmmO 优化报告（EUR / institutions / D1）

> 目标塔：`EUR/D1/INSTITUTIONS ×1.1`，当季 **0/3 空席位**（EUR 唯一还有真实数据集支撑的空塔）
> 结果：**9 项 RA 闸中 8 项 PASS，仅 `LOW_FITNESS 0.83` 未过**（原件 3 项失败）
> 共 11 批 / 58 颗仿真

---

## §1 原件诊断

```
group_neutralize(winsorize(ts_zscore(divide(count_institutional_buyers_security,
  add(count_institutional_buyers_security, count_institutional_sellers_security)), 252), std=0.35), country)
```
EUR / TOP2500 / D1 / decay 4 / **neutralization INDUSTRY** / truncation 0.08 / maxTrade OFF / nanHandling ON

| S | F | TO | R | DD | margin | sub | 2Y | invest_S | self |
|---|---|---|---|---|---|---|---|---|---|
| 1.32 | 0.67 | 7.34% | 3.26% | 3.32% | 8.88bp | 1.00 | 1.48 | 0.89 | **0.4038** |

`checks.fail = []`（IS 层全过），但 `ra_failed_checks = [LOW_SHARPE 1.32, LOW_FITNESS 0.67, LOW_2Y_SHARPE 1.48]`。

### 六维（当季 N=140，T1 5.7214 / T3 54 / T4 228）

| 项 | 值 |
|---|---|
| distinct ops | **5**（`add / divide / group_neutralize / ts_zscore / winsorize`）→ **ΔT1 −0.0051（改善）** |
| fields | 2 → ΔT2 **−0.0006（改善）** |
| T3 | +0 |
| **T4** | **+2**（两个 count 字段本季未用） |

### 逐年 Sharpe（决定性）

| 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| 1.71 | 0.63 | **0.13** | 1.63 | 1.64 | 1.44 | 1.30 | **2.76** | **2.08** | **0.72** |

### IS-Ladder 逐档日频复算（原件的真实瓶颈）

`get_record_set_data(pnl)` 差分 → `sqrt(250)×mean/std`，与平台口径一致（2Y 复算 1.497 vs 平台 1.48）。

| 窗口 | Sharpe | PASS 阈值（TO<30% 打 0.85 折） | 差 |
|---|---|---|---|
| **2Y** | **1.497** | 1.59 起 / 2.02 | **−0.093（< FAIL 1.59 ⇒ 第一档即死）** |
| 3Y | 1.832 | 2.02 | −0.188 |
| 4Y | 1.637 | 2.02 | −0.383 |
| 5Y | 1.593 | 2.02 | −0.427 |
| 6Y | 1.578 | 1.887 | −0.309（且 <1.59） |
| 7Y | 1.560 | 1.751 | −0.191 |
| 8Y | 1.383 | 1.615 | −0.232（且 <1.59） |
| 10Y | 1.324 | 1.35 | −0.026（但 8Y/9Y 均 <1.59，不可达） |

⇒ **唯一现实路径：2Y ≥ 1.59 且 3Y ≥ 2.02**（4Y 起各档差额更大且更差）。

---

## §2 第一轮：结构扫描（10 臂）

| 变体 | S | F | 2Y | sub |
|---|---|---|---|---|
| 原件（ws 0.35） | 1.32 | 0.67 | 1.48 | 1.00 |
| **ws 0.20** | **1.33** | **0.70** | **1.52** | 0.99 |
| ws 0.70 | 1.24 | 0.68 | 1.36 | 0.94 |
| **删除 winsorize** | **0.40** | 0.10 | **−0.44** | 0.57 |
| 净额 `(b−s)/(b+s)` | 1.21 | 0.54 | 1.12 | 0.85 |
| `buyers/holders` | 1.19 | 0.58 | 1.21 | 0.98 |
| `(b−s)/holders` | 1.24 | 0.58 | 1.25 | 0.96 |
| `buyers/(b+s+holders)` | 1.33 | 0.65 | 1.38 | 0.95 |
| `ts_delta(share,63)` | 1.33 | 0.65 | 1.38 | 0.95 |
| ts_zscore 窗 126 | 1.05 | 0.49 | 1.29 | 0.72 |
| ts_zscore 窗 504 | 1.31 | 0.66 | 1.46 | 1.00 |

### ★★★★★ 核心发现：`winsorize` 不是装饰，它就是信号本体

删除 `winsorize` ⇒ **S 1.32 → 0.40、2Y 1.48 → −0.44**（崩盘）。且**裁剪越紧越好**：0.20 > 0.35 > 0.70。
⇒ **有信息的是 z-score 的方向，不是幅度**；幅度（尤其是尾部）是噪声，必须压掉。

---

## §3 第二轮：分组轴 / 平台中性化 / universe（交叉证否）

| 维度 | 取值 | S | 2Y | sub |
|---|---|---|---|---|
| 表达式内分组轴 | **country** | **1.32** | **1.48** | **1.00** |
| | sector | 1.23 | 1.21 | 0.95 |
| | market | 1.23 | 1.21 | 0.95 |
| | subindustry | 1.16 | 1.10 | 0.81 |
| 平台 neutralization | **INDUSTRY** | **1.32** | **1.48** | **1.00** |
| | SUBINDUSTRY | 1.21 | 1.29 | 0.84 |
| | MARKET | 1.11 | 1.35 | 0.82 |
| universe | **TOP2500** | **1.32** | **1.48** | — |
| | TOP800 | 0.82 | 0.87 | 0.60 |
| 平台 neutralization | INDUSTRY + TOPCS1600 | 1.38–1.42 | 1.57–1.77 | 0.99–1.10 |

⇒ **三条都不可动**：country 轴、INDUSTRY、TOP2500。

---

## §4 第三轮：两个独立增益的叠加（ladder 突破）

| 变体 | S | F | 2Y | sub | failed_ra |
|---|---|---|---|---|---|
| z 窗 189（保留 group_neutralize） | 1.39 | 0.70 | 1.56 | 1.07 | 3 |
| `group_rank` 替 `group_neutralize`（z252） | 1.28 | 0.64 | **1.60** | 0.95 | **2** |
| **z189 + ws0.20 + group_rank（`Wjlb7zzd`）** | **1.40** | **0.72** | **1.65** | 1.05 | **2** |

### `Wjlb7zzd` 的 ladder 复算 —— **LOW_2Y 已解决**

| 窗口 | Sharpe | 阈值 | 判定 |
|---|---|---|---|
| 2Y | 1.657 | 1.59 | ✓ |
| **3Y** | **2.082** | **2.02** | **✓ PASS** |
| 4Y | 1.825 | 2.02 | — |
| 5Y | 1.749 | 2.02 | — |

逐年：2021 **3.20** / 2022 **2.53** / 2023 0.54。

> 注：`sign()` 替 winsorize 只到 S 1.32 / 2Y 1.45，劣于 winsorize 0.20 —— 说明需要**保留中段的梯度**，纯三态不够。

---

## §5 第四轮：集中度（失败，但揭示了 F 的机理）

`a = subtract(group_rank(...), 0.5); if_else(greater(abs(a), k), a, 0)`

| k | 保留票数占比 | S | F | 2Y | sub | DD |
|---|---|---|---|---|---|---|
| 0.20 | 60% | 1.30 | 0.65 | 1.49 | 0.97 | 2.90% |
| 0.30 | 40% | 0.80 | 0.33 | 1.59 | 0.50 | 6.58% |
| 0.35 | 30% | **0.13** | 0.03 | 0.50 | −0.21 | 21.5% |
| 0.40 | 20% | 0.12 | 0.04 | 0.42 | −0.29 | 24.3% |
| 0.45 | 10% | 0.22 | 0.09 | 0.63 | −0.20 | 22.2% |

⇒ **集中度是负向的**（信号越往尾部越无效，与 §2 的「尾部是噪声」完全一致）。

---

## §6 第五轮：双腿叠加（最大突破）

**腿 A**：`group_rank(winsorize(ts_zscore(buyers/(buyers+sellers), 189), std=0.20), country)`
**腿 B**：`group_rank(winsorize(ts_zscore(quantity_institutional_shares_acquired/aggregate_share_count_institutions, 189), std=0.20), country)`

| 组合 | S | F | 2Y | sub | R | TO | DD | failed |
|---|---|---|---|---|---|---|---|---|
| 原件 | 1.32 | 0.67 | 1.48 | 1.00 | 3.26% | 7.34% | 3.32% | 3 |
| `Wjlb7zzd` 单腿 A | 1.40 | 0.72 | 1.65 | 1.05 | 3.27% | 8.40% | 2.79% | 2 |
| `d5abON9x` A + 美元腿 | 1.53 | 0.78 | 2.34 | 1.18 | 3.24% | 8.91% | 2.94% | 2 |
| **`9qljEaxd` A + 股数腿** | **1.58** | **0.83** | **2.40** | **1.15** | 3.43% | 8.87% | **2.55%** | **1** |
| `wpoZQjEv` 2A + B | 1.56 | 0.83 | 2.14 | 1.15 | 3.56% | 8.87% | 2.36% | 2 |
| `0mPXjePq` A + 美元腿（z252） | 1.56 | 0.80 | 2.45 | 1.18 | 3.31% | 8.71% | 2.70% | 2 |
| `e7ab6d6E` 2:1 加权 | 1.53 | 0.80 | 2.10 | 1.17 | 3.44% | 8.90% | 2.51% | 2 |
| `E5QpVgVr` 三腿 | 1.45 | 0.67 | 2.55 | 1.08 | 2.67% | 7.72% | 2.79% | 2 |
| `9qljEald` A + 持有家数 | 0.94 | 0.50 | 0.53 | 0.67 | 3.59% | 8.17% | 7.20% | 3 |
| 机构持股比例（单独 / 组合） | −0.10 / 0.86 | — | — | — | — | — | — | — |

### 终选 `9qljEaxd`

```
a = group_rank(winsorize(ts_zscore(divide(count_institutional_buyers_security,
      add(count_institutional_buyers_security, count_institutional_sellers_security)), 189), std=0.20), country);
c = group_rank(winsorize(ts_zscore(divide(quantity_institutional_shares_acquired,
      add(aggregate_share_count_institutions, 0.0001)), 189), std=0.20), country);
add(a, c)
```
EUR / TOP2500 / D1 / decay 4 / INDUSTRY / truncation 0.08 / maxTrade OFF

| S | F | TO | R | DD | margin | sub | 2Y | invest_S | self | prod |
|---|---|---|---|---|---|---|---|---|---|---|
| **1.58** | **0.83** | 8.87% | 3.43% | **2.55%** | 7.73bp | **1.15** | **2.40** | **1.20** | **0.2619** | 未测 |

`checks.pass`：LOW_SHARPE / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / **LOW_2Y_SHARPE** / MATCHES_PYRAMID
`checks.fail`：**LOW_FITNESS 0.83（limit 1.0）**

---

## §7 第六轮：settings 与离散度放大（均无法突破 F）

| 变体 | S | F | R | TO |
|---|---|---|---|---|
| **`9qljEaxd`（decay 4）** | **1.58** | **0.83** | 3.43% | 8.87% |
| decay 2 | 1.54 | 0.79 | 3.33% | 11.11% |
| **decay 0** | 1.46 | 0.70 | 3.09% | **13.59%** |
| `signed_power(centered, 1.2)` | 1.57 | 0.83 | 3.47% | 9.02% |
| `signed_power(centered, 1.5)` | 1.55 | 0.82 | 3.52% | 9.26% |
| `signed_power(centered, 2)` | 1.52 | 0.81 | 3.57% | 9.65% |
| `signed_power(centered, 3)` | 1.38 | 0.74 | 3.64% | 10.33% |
| `multiply(a−0.5, c−0.5)` 合取 | −0.26 | — | −0.45% | 12.03% |

**`decay 0` 反而更差**：TO 被推过 12.5% 的 F 计费门槛（8.87% → 13.59%），分母从 `0.125` 变成实际 TO，F 掉到 0.70。

---

## §8 结论：`LOW_FITNESS` 是结构性硬墙

### 8.1 公式与机制的精确推导

`F = S · sqrt(|R| / max(TO, 0.125))`（已用多个已提交件验证，如 `KPgOY1lk` S 2.48/R 30.35%/TO 2.69% ⇒ F 3.864 ✓）

本件 TO 8.87% < 12.5% ⇒ 分母固定为 0.125。又 `R = S · vol`，故：

```
F = S^1.5 · sqrt(8 · vol)
```

终选件 vol = R/S = 3.43 / 1.58 = **2.171%** ⇒ `F = S^1.5 × 0.4168`

| 若 S = | 1.58 | 1.65 | 1.70 | 1.75 | 1.80 |
|---|---|---|---|---|---|
| F = | 0.83 | 0.88 | 0.92 | 0.96 | **1.00** |

⇒ **在当前 vol 下，F ≥ 1.0 需要 S ≈ 1.80**（或 **vol ≥ 3.17%** 而 S 保持 1.58）。

### 8.2 为什么两条路都被堵死

**S 的天花板**：本族 40+ 个变体的 S 全部落在 **1.38–1.58** 区间。最佳组合（双腿 + 收紧 winsorize + z189 + group_rank）恰好到 1.58。要 1.80 需再 +14%，而所有结构维度（形态、窗口、分组轴、中性化、universe、集中度、多腿、幂次放大）都已扫描完毕。

**vol 的天花板**：vol 锁定在 **2.12–2.22%**。原因是这个 alpha 在 2818 只票上近乎等权（`group_rank` + winsorize 把权重压平），收益离散度极低。所有能抬 vol 的手段都会同时杀 S：

| 抬 vol 的手段 | vol 变化 | S 代价 |
|---|---|---|
| 集中度 k=0.35 | — | 1.40 → **0.13** |
| `signed_power` 3 次 | — | 1.58 → **1.38** |
| 放宽 winsorize 0.20→0.70 | 2.17% → 2.99% | 1.58 → **1.24** |
| `decay 0` | — | 1.58 → **1.46**（且 TO 破 12.5%） |
| 缩 universe 到 TOP800 | 3.38% | 1.32 → **0.82** |

⇒ **S 与 vol 在本族内是互斥的**：S 偏好「压平尾部」（因为尾部是噪声），而压平必然压低 vol；F 偏好的恰恰是高 vol。这是数学上的两侧夹击。

### 8.3 交付判定

| 项 | 状态 |
|---|---|
| 9 项 RA 闸 | **8 PASS / 1 FAIL（仅 LOW_FITNESS）** |
| 相关性 | self **0.2619 PASS**（池 19 颗）；prod 未测（不可提交，无需消耗相关性槽） |
| 塔 | `EUR/D1/INSTITUTIONS ×1.1`，当季 **0/3**，交付即 1/3 |
| 六维 | ops **5** / **ΔT1 −0.0051（改善）** / ΔT2 +0.0136 / **T4 +4** |

**⇒ 不可提交。** 这是本族在 `institutions6` 上的性能上限：从 3 项失败做到 1 项失败，S +20%、F +24%、2Y 1.48→2.40、DD 3.32%→2.55%，但 `LOW_FITNESS` 需要的是「高波动高夏普」的组合，而这条 13F 广度信号在结构上给不出来。

---

## §9 可复用判据（本轮新增）

1. **`winsorize(z, std≈0.20)` 可以是一个信号的本体而非装饰**。判据：删掉后若 S 与 2Y 同时崩（本件 1.32→0.40、1.48→−0.44），说明原始 z-score 的幅度全是噪声，只有方向携带 alpha。
2. **`F = S^1.5 · sqrt(8·vol)`（TO<12.5% 时）**。这给了 F 闸一个可算的判定式：**低波动 alpha 族即使 S 达标也过不了 F**。反推：若某族 vol ≈2.2%，则 F 需要 S ≈1.80。
3. **`decay` 压到 0 可能反向伤害 F**：TO 若被推过 12.5%，F 的分母从 0.125 变成实际 TO，反噬。
4. **`f(x)=S(x)·sqrt(8·R(x)/0.125)` ⇒ S 与 vol 互斥时 F 有硬顶**。凡 obs 到「压平尾部提 S」的族，先算 vol 能否达到 `12.5/S²`，否则不要在 F 上耗预算。
5. **同数据集多腿相加是合法且有效的 S 杠杆**：腿 A（buyer 广度）+ 腿 B（股数流入强度）把 S 从 1.40 抬到 1.58、2Y 1.65→2.40，且 T4 从 +2 变 +4。ATOM 只限制「数据集数量」，不限制字段数量。
6. **LOW_2Y_SHARPE 的 ladder 可通过「2Y≥1.59 + 3Y≥2.02」达标**，无需 2Y 本身 ≥2.02。本件 2Y 1.657 仅够进档，真正通过靠 3Y 2.082。
7. **纠正一条上轮错判**：「`institutions6` 无信号」是形态用错导致的误判。同一数据集在原件的 `winsorize(ts_zscore(...,252), std=0.35)` 外壳下 S 1.32，说明数据集本身有 alpha，判死前必须换外壳重测。

---

## §10 数据索引

- 仿真：11 批 / 58 颗（batch id：`22HyzN2up4ZEbVUA2Lv9NoA`、`2Wm0BRaYZ4iMan4f0V30qJQ`、`4plKOO9i44xr9dIstLLnywY`、`4xea6ogB94kqbXJoghahJ5C`、`3gzABK3Ax4nFcHdhE9K9R9j`、`1V5mEy1GH4Tnannr5aNQL46`、`CWHoRdz64hS9cv1bSonGCpL`、`1gWccEbon4Cj9SkREC0VRF7`、`4g8LMd4CM4Tmb33ZSqsvNLN`、`7o9spcDe4pR8C1BrBYF0Hr`、`EHGEXaNc4wq9cNInTy1j8t`、`1TJTnlciR4Cw9BG1cks3hHnh`、`2P40Dvdew59Iac8SP3OsLJ5`、`2d6n0M43I5bw94CbYDLJh9f`）
- 关键件：`9qljEaxd`（终选，8/9）｜`Wjlb7zzd`（单腿，ladder 首次通过）｜`d5abON9x`（美元腿）｜`wpoZQjEv`（2:1）

---

## §11 论坛与官方文档查证（2026-11-19 22:48）

### 11.1 工具路径更正

`search_forum_posts` 持续返回 `navigation_failed: true`（0 结果且不可信）。正路是 **`search_forum_posts_local(keywords=[...])`** —— Zendesk 列表端点 + 本地过滤，`search_reliable: true`。

### 11.2 官方公式与硬闸（两处文档互证）

- `parameters-simulation-results`：`Fitness = Sharpe · sqrt(abs(Returns) / max(Turnover, 0.125))`
- `consultant-submission-tests`：**Fitness D1 门槛 = Greater than 1**（D0 = 1.5）
- `alpha-submission`：`Returns = annualized PnL / half of book size`；**book 固定 $20M、本金 $10M** ⇒ **杠杆由平台写死，不可调**
- 失败消息表里 Fitness 只有一条：「**Improve fitness**」——无任何豁免分支
- `submit_verdict(9qljEaxd)`：`verdict=BLOCKED`、`reason_code=SIM_FAIL:LOW_FITNESS`、`exit_code=1` ⇒ 提交层硬拦

### 11.3 官方「提高收益 5 法」逐条实测（post 8833033953559，212 赞）

| # | 官方建议 | 实测 | 结论 |
|---|---|---|---|
| 1 | 提高换手（TO 越高收益越高） | decay 4→2→0：TO 8.87→11.11→**13.59%**，但 R 3.43→3.33→**3.09%** | ✗ 收益反降；且 TO>12.5% 后 F 分母变实际 TO，**F 0.83→0.79→0.70** |
| 2 | 降低 decay | 同上 | ✗ |
| 3 | 更小 / 更流动的 universe | TOP800 S **0.82**/F 0.39；TOPCS1600 单腿 S 1.38–1.42/**F 0.76–0.78** | ✗ 均劣于 TOP2500 的 F **0.83** |
| 4 | 保收益与回撤不变的前提下提高波动率 | 集中度 k=0.20–0.45；`signed_power` 1.2/1.5/2/3× | ✗ vol 无法在保 S 前提下抬升；S 1.58→1.38，F 仍 ≤0.83 |
| 5 | 使用 news / analyst 数据集 | **未试** | **唯一未证否** |

第 1、2 条失败的机理是：`max(Turnover, 0.125)` 让 12.5% 以下成为「免费换手区」，但本族的额外换手全是噪声，收益不随之上升；一旦越过 12.5%，F 的分母立刻由 0.125 变成实际 TO，形成**双重惩罚**。

### 11.4 附带查到的 5 条新官方规则

1. **ATOM 可跳过 IS-Ladder**（`alpha-submission` 原文）：「ATOM Alphas can skip the IS Ladder Sharpe test. ATOM Alphas must pass regular IS tests and the 2Y Sharpe test.」⇒ `9qljEaxd` 只要 2Y 2.40 即充分。
2. **Cluster Test 不阻塞提交**：「Failing the Cluster Test does not block submission and does not affect eligibility」⇒ CLUSTER_TEST 1.06 无害。
3. **Pyramid 混用取最低倍数**（BRAIN TIPS 003）：「如果一个 Alpha 混用了多个 Pyramid 的数据，Pyramid 倍数按最低的那个算；其中有一个是 1，Pyramid 就相当于没有加成。」⇒ institutions 1.1 + analyst 1.3 ⇒ 仍按 **1.1**，**混 analyst 腿不掉塔倍数**。
4. **IS-Ladder 有 0.75× / 0.85× / 1.0× 三档**（状态消息表），按换手率分级；TO < 10% 可能适用 0.75× 档。
5. **未用字段免费额度**（11-17 公告）：只用 `alphaCount = 0` 字段的回测**不计入每日 5,000 次上限**。并发上限 8，GLB 占 2 槽。

### 11.5 论坛没有别的解法

`search_forum_posts_local` 扫 100 帖、命中 42–56 条：**无任何针对 LOW_FITNESS 的绕过方法**。只有区域 tip 帖把 LOW_FITNESS 列为最常见的卡点（例如 RAA 父子本因 EUR 与 ASI 的 LOW_FITNESS 卡在 2 个子本）。此前引用的关键帖 8394917303575 已 404 删除。

### 11.6 唯一剩余方向

论坛第 5 条 + 官方 Pyramid 规则共同允许的一条路：**给 `9qljEaxd` 加一条 analyst / news 的独立信息腿**（塔倍数仍按 1.1 计）。它同时抬 S 与 R（独立信息 → 分散化），是目前唯一能同时推动 F 两个因子的手段。

结构上只能用 `trade_when` 门控 / `bucket` 分组轴 / `neutralize` 残差三种形式（等权相加会被 `weighted_leg_mix_func_prefix` 拦）。代价是破坏 ATOM ⇒ 需走 IS-Ladder，但 3Y 2.082 ≥ 2.023 已达标，**不构成额外成本**。
