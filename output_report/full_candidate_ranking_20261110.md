# 待提交候选全量归纳与排序（2026-11-11 00:0x，ET 11-10）

> 口径：**只挖不提交**｜只认 REGULAR / RA 全闸｜台账 → 硬闸 → 指标｜塔计数按季度、只认 `get_pyramid_alphas`｜ΔS 分区内才可比｜算子数=硬指标
> 数据来源：本轮平台逐颗实测（22 颗 GET / 17×17 互相关 / 11 次 self 实测 / 6 次闸门预检）+ 各来源清单交叉核对

## 0 一句话

**候选池共 22 颗活跃件，其中 5 颗被硬闸判死、2 颗属 SUPER 线，真正可排序的 RA 件 15 颗。**
**本轮最重要的发现是 3 处旧读数失真**：`xAvK6b0q` self 实测 **0.9330**、`0mY5EZJv` self 实测 **0.9954**（旧表都当作可交）、`YP1zY8EM` prod **0.729** 超线。自池随今日两颗提交增长后，历史 self 值必须重测。

**最优 2 席组合**：`wpo8olA6`（DEU OTHER 点亮，免三问）+ `omEdka3v`（GBR OTHER 点亮），二者 ρ = **0.019**，点亮两座不同区的 OTHER 塔。

---

## 1 候选池来源与去重（4 层）

| 层 | 来源 | 性质 |
|---|---|---|
| L0 最新权威 | `tracking/DEU/atom_orthogonal/FINAL_DELIVERY_REPORT_11ALPHAS_20261111.md`(23:21)、`REPLACE_Jj8VQwoe_WITH_xAvK73Qg_20261111.md`(23:30) | 5 颗待授权 + 替换提案 |
| L1 推荐名单 | `submit_candidates_20261110.md`（A 档剩 2 席 / B 档）、`submittable_ranking_20261109.md`、`SA_*_plan_20261110.md` | 排名与同席替代 |
| L2 op-min 交付件 | 8 份 `opmin_*.md`（`wpo8olA6` / `d5a2aO7v` / `88NmN37X` / `zqdvb0YE` / `0mY5EZJv` / `YP1zY8EM` / `LLMv6joe` / `mLovqRV6`） | 定案候选、未提交 |
| L3 区域池 / 机读 | `gbr_delivery_manifest_20261110.md`、`results/submit_pool_ranked_20261110.json`、`submit_pool_towers_20261110.json`、`submit_staging_*.json` | 未评估、待 prod、同族互斥 |

⚠ `data/wqb.db` 的 `submit_ready` 表（2044 行）`added_at` 最新只到 **10-31**，**不含本轮候选**；`alphas.disposition` 只有 DEAD/SUBMITTED/NULL，不能用来筛待提交。本轮清单以文档 id 为准。

---

## 2 ★ 硬闸判死（5 颗，本轮实测推翻旧结论）

| alpha | 判死项 | 实测值 | 对端 / 说明 |
|---|---|---|---|
| **`xAvK6b0q`** | **self FAIL** | **0.9330** | 撞今日提交的 `E5QZ1NgJ`。旧表记「PASS、5 ops、待 prod」⇒ 现已不可交 |
| **`0mY5EZJv`** | **self FAIL** | **0.9954** | 撞已 ACTIVE 的 `bl6AvMkN`（op-min 交付件，旧表未测 self） |
| **`YP1zY8EM`** | **prod 超线** | **0.729** | >0.70 无豁免；另有 CLUSTER_TEST WARNING |
| `mLovqRV6` | 硬闸 WARNING | 2Y = **1.27** | `LOW_2Y_SHARPE` 属提交层升级项；该族 46 变体已全判死 |
| `P05JM61x` | 平台 FAIL | **4 项 FAIL** | S1.46 / F0.79 / ladder1.36 / sub0.61 |

⇒ **自池漂移是本轮最大教训**：今天 18:17 两颗 ACTIVE 后，池从 17→20（DEU）/31→48（KOR）/29→34（GBR）。凡 self 读数来自 11-10 白天之前的，一律重测。

---

## 3 全量排序主表（RA 线 15 颗，100 分制）

**打分口径（透明）**：塔边际 25｜prod 余量 20｜self 余量 15｜稳健 15｜算子数 10｜指标厚度 10｜闭环完备 5。
分数是**质量分**，不是可交顺序；可交顺位见 §6（还要过同席与 prod 闭环）。

| # | alpha | 区 | 分 | ops | S/F | prod（来源） | self | ΔS（分区） | 稳健 | **塔归属 → 当季计数 → 交后 → 新点亮** | 塔增量 | 状态 |
|---:|---|---|---:|---:|---|---|---|---|---|---|---:|---|
| **1** | **`omEdka3v`** | GBR | **81** | 8 | 2.51/1.40 | 0.6026（缓存） | 0.4164 | +0.26（GBR:PP） | PASS | OTHER 2→**3**、SHORT 4→5 | **+1** ✅ | 仅差三问 |
| **2** | **`wpo8olA6`** | DEU | **74** | **8** | 1.65/1.27 | 0.6306（缓存） | 0.5784 | +0.56（DEU:PP） | PASS | OTHER 2→**3**、SHORT 3→4 | **+1** ✅ | **全闭环、免三问** |
| 3 | `6XdkW08J` | GBR | 62 | 8 | **2.60/1.95** | 0.6267（缓存） | **0.3393** | +0.23（GBR:PP） | PASS（CV .057 全场最稳） | SHORT 4→5、MODEL 6→7 | 0 | 仅差三问 |
| 4 | `qM7KxkQV` | DEU | 59 | 11 | 1.72/1.34 | **0.543（最厚）** | 0.5429 | +0.08（DEU:1） | **PASS（CV .157）** | SHORT 3→4、INSIDERS 0→1 | 0 | 11 ops ⇒ 应换 8ops 件 |
| 5 | `xAvK73Qg` | DEU | 56 | 11 | 2.04/1.77 | **未闭环**（终验中） | 0.5424 | +0.09（DEU:1） | NO_RECORD | OTHER 2→3、SHORT 3→4 | +1 | 与 `#2` ρ .741 同席 |
| 6 | `Jj8VQwoe` | DEU | 56 | 12 | 1.65/1.24 | 0.6124（用户值，平台 20min 未出） | 0.5645 | +0.05（最薄） | CONDITIONAL | OTHER 2→3、SHORT 3→4 | +1 | 与 `#2` ρ .737 同席、被支配 |
| 7 | `RREPm361` | DEU | 51 | **5** | 2.02/1.25 | **0.6881（余量仅 .0119）** | **0.3275** | +0.73（DEU:PP） | PASS（台账无明细） | ANALYST 6→7 | 0 | 唯一近正交，prod 贴线 |
| 8 | `9qlz29Oe` | DEU | 45 | 12 | 1.86/1.34 | **0.47（最宽，但未入缓存）** | 0.4552 | +0.08（DEU:1） | **CONDITIONAL（最差）** | SHORT 3→4、NEWS 0→1 | 0 | 2017 −0.20 / 2023 0.30 / CV .638 |
| 9 | `88NmN37X` | DEU | 36 | 9 | 1.79/**1.53** | 未闭环（曾 prod fail-closed） | 0.5538 | +0.74（DEU:PP） | PASS | SHORT 3→4、INSIDERS 0→1 | 0 | qM7 家族 ρ .954–.977 |
| 10 | `1YNMAA8M` | DEU | 35 | 8 | 1.58/1.36 | **0.6951（余量 .0049）** | **0.6946（余量 .0054）** | +0.43（DEU:PP） | PASS | MODEL 3→4、ANALYST 6→7 | 0 | prod/self 双贴线，已被 `#7` 取代 |
| 11 | `P0oolrZq` | GLB | 34 | 6 | **3.45/2.37** | 0.6578（缓存） | 0.5679 | +0.69（GLB） | NO_RECORD | RISK 1→2、OTHER 4→5 | 0 | 11-09 配额已翻篇；CLUSTER WARN |
| 12 | `d5a2aO7v` | DEU | 33 | **8** | 1.66/1.36 | 未闭环 | 0.5450 | +0.64（DEU:PP） | NO_RECORD | SHORT 3→4、INSIDERS 0→1 | 0 | **qM7 家族算子最少件**（op-min 首选） |
| 13 | `LLMv6joe` | DEU | 31 | **15** | 1.65/1.17 | 未闭环 | 0.3585 | 未测 | NO_RECORD | SHORT 3→4 | 0 | RREwqrNa(REJECT) 族派生、算子最多 |
| 14 | `zqdvb0YE` | DEU | 30 | 9 | 1.72/1.34 | 未闭环 | 0.5428 | +0.68（DEU:PP） | NO_RECORD | SHORT 3→4、INSIDERS 0→1 | 0 | 与 `qM7KxkQV` **ρ=1.0000** 逐位无损 |
| 15 | `d5a2vxzY` | DEU | 28 | 12 | **1.60/1.08** 双贴线 | 0.6039（用户值） | **0.6038** | +0.07（DEU:1） | CONDITIONAL | SHORT 3→4 | 0 | ATOM 单塔、末年 1.12 回落 |

**塔计数基准**（`get_pyramid_alphas` 当季）：DEU/D1 analyst 6｜model 3｜shortinterest 3｜other 2｜insiders 0｜news 0；GBR/D1 shortinterest 4｜model 6｜other 2；GLB/D1 risk 1｜other 4。
点亮线 = 当季 ≥3 ⇒ **只有 `OTHER 2→3` 能新点亮**（DEU 与 GBR 各一座）。INSIDERS/NEWS 0→1 只是起步，不算点亮。

⚠ **ΔS 三套基准**：`DEU:1`（组合 S≈3.32）、`…:POWER_POOL`（S≈1.73）、`GBR:1:POWER_POOL`。**只各自看符号，+0.73 与 +0.08 不可横比。**

---

## 4 SUPER 线（2 颗，独立配额 0/1，不进 RA 排序）

| alpha | 区 | S/F | prod | 说明 |
|---|---|---|---|---|
| `A1VAAbWe` | ASI | **4.60/3.33** | 0.6634（缓存） | 11-10 08:45 过闸记录，**非预选承诺**（每轮独立决策） |
| `npvEEWO8` | ASI | 4.30/3.12 | 0.6593（缓存） | 同上 |

两者 `type=SUPER`、无 `regular.code`、无塔标记。SUPER 与 REGULAR 是两条独立配额线。

---

## 5 互相关矩阵结论（17 颗，4 年日收益，本地计算不占 prod 槽）

- **最大独立集 = 12 颗**：`qM7KxkQV, wpo8olA6, RREPm361, 9qlz29Oe, d5a2vxzY, omEdka3v, 6XdkW08J, xAvK6b0q, 0mY5EZJv, 1YNMAA8M, LLMv6joe, P0oolrZq`
- **9 组超阈对**，分两簇：

| 簇 | 对 | ρ | 裁决 |
|---|---|---|---|
| **qM7 家族**（4 颗只能留 1） | `qM7KxkQV`~`zqdvb0YE` | **1.0000** | 逐位无损压缩，取算子最少的 `d5a2aO7v`(8) 或 prod 闭环的 `qM7KxkQV`(11) |
| | `qM7KxkQV`~`88NmN37X` / `88NmN37X`~`zqdvb0YE` | .9773 | 同上 |
| | `d5a2aO7v`~`88NmN37X` / `qM7KxkQV`~`d5a2aO7v` / `d5a2aO7v`~`zqdvb0YE` | .954 / .9346 | 同上 |
| **OTHER 家族**（3 颗只能留 1） | `Jj8VQwoe`~`xAvK73Qg` | .7619 | 取 `wpo8olA6`（8 ops、prod 闭环、PASS、免三问） |
| | `wpo8olA6`~`xAvK73Qg` / `wpo8olA6`~`Jj8VQwoe` | .7409 / .7372 | 同上 |

- 最紧但仍可共存：`d5a2vxzY`~`9qlz29Oe` = **0.6704**（共享 `max_loan_rate_p5_d1` 腿）。
- 最正交组合：`omEdka3v`~`wpo8olA6` = **0.019**；`6XdkW08J` 与 DEU 全族 ≈ −0.02~0.03。

---

## 6 ★ 可执行顺位（叠加硬闸 + prod 闭环 + 同席裁决）

| 顺位 | alpha | 为什么 | 提交前唯一待办 |
|---:|---|---|---|
| **1** | **`wpo8olA6`** | DEU OTHER 点亮 +1｜8 ops｜prod .6306 权威缓存｜self .5784｜PASS｜**`mix kind=none` 免三问**｜ΔS +0.56 | **无**（全闭环） |
| **2** | **`omEdka3v`** | GBR OTHER 点亮 +1｜prod .6026 缓存｜self .4164｜PASS｜ΔS +0.26｜与 #1 ρ **0.019** | 答 2 腿三问 |
| 3 | `6XdkW08J` | 指标最强 S2.60/F1.95｜CV .057 全场最稳｜self .3393｜与 #2 ρ .153 | 答三问（塔增量 0） |
| 4 | `qM7KxkQV` | prod 余量最厚 .157｜稳健最好 CV .157｜与 `9qlz29Oe` ρ .338 | 答三问；**按算子铁律应换 `d5a2aO7v`，但那件 prod 未闭环** |
| 5 | `RREPm361` | 5 ops｜近正交 ρ≤.16｜self .3275｜ΔS +0.73 | **prod `refresh=True` 终验**（余量 .0119，漂移即死）+ 三问 |
| 6 | `9qlz29Oe` | prod 余量最宽 .23｜S1.86/F1.34 | prod 落权威表 + 三问 + **description 如实披露 2017 负年 / 2023 0.30 / CV .638** |
| — | `Jj8VQwoe` `xAvK73Qg` | 与 #1 同席；`Jj8VQwoe` 六项中五项被 #1 支配 | 不交 |
| — | qM7 家族另 3 颗 | 与 #4 同席 ρ≥.93 | 只留 1 颗 |
| — | `1YNMAA8M` `P0oolrZq` `LLMv6joe` | 双贴线 / 配额翻篇 / 15 ops 且 REJECT 族派生 | 备胎 |

**ET 11-10 配额 2/4，剩 2 席 ⇒ 推荐交 #1 + #2**：点亮 DEU 与 GBR 两座 OTHER 塔、彼此 ρ .019、两颗都 8 算子 / PASS / prod 缓存有效，且 #1 免三问。

---

## 7 其余待提交池归纳（未进入逐颗打分，因未评估 / 同族锁死）

| 组 | 颗数 | 代表 id | 缺什么 / 为什么不排序 |
|---|---:|---|---|
| GBR manifest 已确认可交付 | 10 | `rKRx0M2m` `pwdd7Za6` `pwdLp9z6` `O0A6Qz7p` `leAmmre8` `omExeqLb` `RREGX1kd` `LLM0e20m` `Xg9dPpp0` `Jje6mrpO` | 报告明示「暂不提交」；未做本轮 self/ΔS/塔实测 |
| GBR 待 prod 确认 | 16 | `88jV1LEW` `mLomxW71` `bl6avAXp` `3qoXwW1z` … | prod 未闭环，平台 prod 槽单并发 |
| `loaned_share_*` 同族 | 5 | `ZYQv7j2Q` `58EdlON6` `LLM0ePj2` `O0AX7Zw1` `zq3nNGp8` | 互相关 0.50–0.9485，只能选 1；且与已 ACTIVE 的 `akK9ooZv` ρ .68–.95 永久出局 |
| `submit_pool_ranked` 其余 | ~30 | `rKRPAWv9` `Xg9dPpp0` `9qxNbxJx` `kqNAz9pP` `qMLJjleO` … | 本地池快照，多数为 11-09 及更早；`9qxnNkeq` REJECT、`gJe2a8wJ` CW FAIL |
| staging JSON 过时状态 | 3 | `1YNMAA8M` `E569ZE7L` `mLovbnm2` | `READY_PENDING_USER_AUTHORIZATION` 但已分别被取代 / self=1.0 / WITHDRAWN |

**明确排除总账**：已 ACTIVE（`78Yk8VR1` `E5QZ1NgJ` `rKRx2Alj` `zq3eb7No` `bl6AvMkN` `0mY1QPEv` `d5WGG5bg` 等 20+）、台账 REJECT（`RREwqrNa` `mL617YPx` `9qxnNkeq`）、ΔS 负硬闸（`KPJ1rG0j` `leAnKOEA` `P0oR7vYw`）、prod 超线（`gJe2lMKO` .9906 等）、SUPERSEDED（`E569ZE7L` `1YWqzPGQ` `2rAYpJKx` `QPvx8M1W` 及各 op-min 变体系）。

---

## 8 文档矛盾裁决（以本轮实测为准）

| 矛盾 | 采信 |
|---|---|
| 塔计数按 20 颗全历史 OS 反推（`DEU_OS_INVENTORY_AND_DELTA_20261111.md` 称 OTHER 4 已亮、INSIDERS 1） | ❌ 错。**按季度重置**，当季 OTHER **2 未亮**、INSIDERS **0** |
| `9qlz29Oe`「第 11 颗正式成立」（只要求十年零空窗） | ⚠ 口径更松。按 RA 稳健口径 CONDITIONAL（负年 + CV .638 + 2023 崩塌） |
| `Jj8VQwoe` 在 11 颗篮子仍列「待授权」 | 本轮判 **SUPERSEDED**（与 `wpo8olA6` ρ .7372 同席且被支配）；`REPLACE_..._xAvK73Qg` 提案亦被 ρ .7409 否掉 |
| `1YNMAA8M` staging 仍 `READY_PENDING_USER_AUTHORIZATION` | ❌ 已被 `RREPm361` 取代；prod/self 双贴线，降备胎 |
| `xAvK6b0q` / `0mY5EZJv` 旧表按「待提交/可交」 | ❌ **本轮 self 实测 0.9330 / 0.9954 判死** |
| `A1VAAbWe` / `npvEEWO8` 08:45「本轮可交」 | 只是过闸记录；§G 明令每轮独立决策，且属 SUPER 线 |
| `FINAL_VERDICT_9DELIVERED` 判「第 10 颗不成立、定格 9 颗」 | 已被 22:56 / 23:21 推翻（11 颗） |

---

## 8bis 零散候选逐颗处置（补齐 Tier 1 / 附录项，避免遗漏）

| alpha | 来源 | 处置 |
|---|---|---|
| `RReJ36Wa` `j2a5vodk` | `submit_candidates_20261110` 附四 | prod 当时 inflight 未闭环；本轮候选池已由 11 颗篮子与 op-min 件覆盖 ⇒ 备胎，不进排序 |
| `xAvK6b0q` | A 档附录「5 ops 压缩件」 | **本轮 self 0.9330 判死**（见 §2） |
| `E569ZE7L` | staging 旧版排第 1 | self = 1.0000 撞今日 `78Yk8VR1` ⇒ 永不提交 |
| `1YWqzPGQ` | staging 旧版第 3 | 被 8ops `wpo8olA6` 取代；与 `Jj8VQwoe` ρ .8924、2016 S −1.00 |
| `1YNMAA8M` | staging `READY_PENDING_USER_AUTHORIZATION` | 纳入主表 #10（双贴线备胎） |
| `mLovbnm2` `2rAYpJKx` | op-min / 11-09 排名 | `WITHDRAWN_DO_NOT_SUBMIT` / 与已 ACTIVE 的 `rKRx2Alj` ρ≈1 ⇒ 永久出局 |
| `QPvx8M1W` `KPgKPRAx` `P05JWgdw` | A 档附录 | 分别被 `E5QZ1NgJ` 取代 / 2021 塌到 0.18 不采纳 / 塔点不亮判死 |
| `gJe2lMKO` | SA 优先级队列 #2 | 08:45 实测 prod **0.9906**，同族必死 |
| `A1VAAbWe` `npvEEWO8` | SA 队列 #3/#5 | 纳入 §4 SUPER 线 |
| `E56jA0AP` `9qxnYPjd` `N1NErpxo` `A1VXlbgd` | 11-09 排名欠 prod / SA 线 | 配额已翻篇，无本轮 prod 权威读数 ⇒ 不进本轮排序 |
| `LLKPwej2` | ALPHA12 提案 | self 0.7161 > 0.7 判死 |
| `vRAKQ1eb` | sentiment27 BE28 | 最高 S 0.95，不足以交付 |
| `j2Y7qlA5` `kqNAz9pP` `qMLJjleO` `rKRx7v6m` `RREwqrNa` | B 档同席替代 | 前两颗与 `E569ZE7L` 同席；`qMLJjleO` 与 #3 OTHER 塔重合；`rKRx7v6m` 与已提交 `0mY1QPEv` 同源；`RREwqrNa` 台账 REJECT |

## 9 落库与产物

- `results/full_rank_platform_20261110.json`（22 颗平台实时读数）
- `results/full_rank_scores_20261110.json`（15 颗打分与分项）
- 本轮新建/沿用稳健台账：`wpo8olA6`=PASS、`qM7KxkQV`=PASS、`RREPm361`=PASS、`9qlz29Oe`/`d5a2vxzY`/`Jj8VQwoe`=CONDITIONAL、`omEdka3v`/`6XdkW08J`/`88NmN37X`/`1YNMAA8M`/`xAvK6b0q`=PASS；`NO_RECORD` 9 颗
- **本轮未提交任何 alpha**（提交权归用户点名）
