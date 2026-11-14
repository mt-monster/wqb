# 总体篮子全量排序（截至 2026-11-13 12:20 GMT+8）

只读盘点，**未提交**。候选池来自 85 份近期文档交叉去重 + 平台逐颗实读（47 颗）。

---

## 0 一句话结论

**47 颗活跃候选 → 36 颗无硬闸 → 去同席后 32 颗可执行 → 本轮最多点亮 4 座新塔。**
**推荐交前 3 颗：`omEdka3v` + `wpo8olA6` + `ZYQ116ln`**（各点亮一座不同区的塔，彼此 ρ < 0.09）。

⚠ 本报告推翻 11-12 `EUR/DELIVERABLE_17_VERIFIED.md`：那 17 颗里 **6 颗 ΔSharpe 为负（提交硬闸）**、**1 颗稳健台账 REJECT**，实际只有 10 颗可交。

---

## 1 候选池与去重

| 层 | 数量 | 说明 |
|---|---:|---|
| 文档交叉去重后活跃 id | 47 | 已剔已 ACTIVE / 判死 / SUPERSEDED / REJECT / SUPER 独立线 |
| 平台实读成功 | **47** | 全部 `UNSUBMITTED`、checks 0 FAIL、CW PASS |
| 无硬闸可排序 | **36** | prod 已闭环且 <.7、ΔS≥0、mix 未硬拦、台账非 REJECT |
| 排除 | 11 | 明细见 §5 |
| 去同席后可执行 | **32** | 贪心按分数取，跳过 ρ≥.7 的已选件 |

**已 ACTIVE 剔除**（本轮不可重复提交）：`9qlZLVNd` `XgaG2Vom` `E5Q7RGNR` `e75avmq6` `O0W0w3P7` `P0oolrZq` `78Yk8VR1` `E5QZ1NgJ` `zq3eb7No` `bl6AvMkN` `rKRx2Alj` `GrW9OxmG` `vR1oxZA3` `bl6OWZ2M` 等 119 条台账。
**SUPER 独立配额线**单列（`leaq3P9l` `1YNl3p5R` `2r5rA775` `Wjl6JJQO` `Jj8Zr1Xn` 等），不进 RA 排序。

**口径**：打分 = 塔25 / prod20 / self15 / 稳健15 / ΔS10 / 算子10 / 指标10 / 闭环5（满分 110）。`self` 缺失按中位 8 分计（不虚高）。

---

## 2 ★ 全量可执行顺位（32 颗，含逐颗塔信息）

塔格 = **归属 → 当季现值 → 交后 → 是否新点亮**；「增量」扣除了同塔被前序候选点亮的部分。

| # | alpha | 区 | 分 | S/F | ops | prod | self | ΔS | **塔归属→现值→交后→点亮** | **塔增量** | 待办 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---:|---|
| **1** | **`omEdka3v`** | GBR | **92** | 2.51/1.40 | 8 | .6026 | .492 | +.59 | SHORT 4→5 否｜**OTHER 2→3 点亮** | **+1** | 三问 |
| **2** | **`wpo8olA6`** | DEU | **88** | 1.65/1.27 | 8 | .6306 | — | +.56 | SHORT 3→4 否｜**OTHER 2→3 点亮** | **+1** | **零待办** |
| **3** | **`ZYQ116ln`** | KOR | **75** | 1.86/1.10 | **3** | .6981 | .212 | +.24 | **PV 2→3 点亮** | **+1** | prod 贴线 .002 |
| 4 | `leAmmre8` | GBR | 72 | 2.97/1.40 | 9 | .6887 | .450 | +.69 | SHORT 4→5 否｜OTHER（已被 #1 点亮） | 0 | 三问·prod 贴线 |
| 5 | `6XdkW08J` | GBR | 71 | 2.60/1.95 | 8 | .6267 | .340 | +.42 | SHORT 4→5 否｜MODEL 6→7 否 | 0 | 三问 |
| 6 | `O0A6Qz7p` | GBR | 64 | 2.18/1.52 | 10 | .6984 | — | +.09 | SHORT 4→5 否｜OTHER（已点亮） | 0 | 三问·prod 刷新/贴线 |
| 7 | `88NmN37X` | DEU | 62 | 1.79/1.53 | 9 | .5541 | — | **+.74** | SHORT 3→4 否｜INSIDERS 0→1 否 | 0 | prod 刷新 |
| 8 | `JjeNJ00O` | EUR | 62 | 2.60/1.35 | 10 | .6813 | — | +.03 | **RISK 2→3 点亮**｜IMBALANCE 3→4 否 | **+1** | 三问·prod 贴线 |
| 9 | `YP1baJrv` | EUR | 62 | 2.23/1.19 | 9 | **.6999** | — | +.02 | RISK（已点亮）｜OTHER 3→4 否 | 0 | 三问·**prod 仅差 .0001，必须 refresh** |
| 10 | `zq3Yrb3G` | EUR | 61 | 2.87/1.65 | 15 | .6872 | — | +.03 | RISK（已点亮）｜ANALYST 10→11 否｜SENTIMENT 3→4 否 | 0 | 三问·prod 贴线 |
| 11 | `Xg9dPpp0` | GBR | 60 | 1.97/1.44 | 9 | **.4000** | — | +.42 | SHORT 4→5 否｜RISK 0→1 否｜FUNDAMENTAL 3→4 否 | 0 | 三问·prod 刷新 |
| 12 | `mLaLllmK` | EUR | 60 | **3.98/2.21** | **5** | .6579 | .301 | **+.84** | OTHER 3→4 否 | 0 | — |
| 13 | `omExeqLb` | GBR | 59 | 2.43/1.78 | 8 | .6143 | .419 | +.52 | SHORT 4→5 否｜MODEL 6→7 否 | 0 | 三问 |
| 14 | `6XMmE0EL` | EUR | 58 | 2.35/1.02 | 5 | .6529 | .249 | +.33 | OTHER 3→4 否 | 0 | — |
| 15 | `WjOeNE6O` | EUR | 56 | 2.90/1.85 | 5 | .6411 | **.641** | +.54 | IMBALANCE 3→4 否｜OTHER 3→4 否 | 0 | 三问·prod 刷新 |
| 16 | `RREGX1kd` | GBR | 54 | 1.65/1.09 | 9 | .5940 | — | +.33 | SHORT 4→5 否｜ANALYST 3→4 否 | 0 | 三问·prod 刷新 |
| 17 | `Jje6mrpO` | GBR | 53 | 2.37/1.58 | 10 | .5565 | — | +.09 | SHORT 4→5 否｜RISK 0→1 否｜FUNDAMENTAL 3→4 否 | 0 | 三问·prod 刷新 |
| 18 | `LLM0e20m` | GBR | 53 | 1.75/1.17 | 11 | .5386 | — | +.08 | SHORT 4→5 否｜NEWS 3→4 否 | 0 | 三问·prod 刷新 |
| 19 | `rKRRjM51` | IND | 53 | **3.34/2.65** | 7 | .6752 | .652 | +.38 | INSTITUTIONS 1→2 否｜PV 11→12 否 | 0 | prod 刷新 |
| 20 | `pwdd7Za6` | GBR | 52 | 1.69/1.04 | 8 | .6238 | — | +.30 | SHORT 4→5 否｜PV 4→5 否 | 0 | prod 刷新 |
| 21 | `rKRx7v6m` | EUR | 52 | 3.22/2.14 | 7 | .6756 | .428 | +.39 | SENTIMENT 3→4 否｜OTHER 3→4 否 | 0 | 三问 |
| 22 | `9qlz29Oe` | DEU | 50 | 1.86/1.34 | 12 | **.4700** | — | +.08 | SHORT 3→4 否｜NEWS 0→1 否 | 0 | 三问·稳健 CONDITIONAL |
| 23 | `RREPm361` | DEU | 49 | 2.02/1.25 | **5** | .6881 | .328 | **+.73**(PP) | ANALYST 6→7 否 | 0 | 三问·prod 贴线 .012 |
| 24 | `ZYa6x531` | EUR | 49 | 1.74/1.01 | 8 | .6964 | — | +.20 | EARNINGS 1→2 否 | 0 | 三问·prod 贴线 |
| 25 | `1YNMAA8M` | DEU | 48 | 1.58/1.36 | 8 | .6951 | — | +.43 | MODEL 3→4 否｜ANALYST 6→7 否 | 0 | prod 刷新/贴线·S 贴线 |
| 26 | `rKRx0M2m` | GBR | 48 | 2.29/1.56 | 11 | .6232 | .443 | +.01 | SHORT 4→5 否｜RISK 0→1 否 | 0 | 三问 |
| 27 | `2r5MqmVJ` | EUR | 45 | 1.74/1.03 | 8 | .6740 | — | +.15 | EARNINGS 1→2 否 | 0 | 三问 |
| 28 | `Jj8qXO5m` | EUR | 45 | 1.74/1.03 | 8 | .6663 | — | +.14 | EARNINGS 1→2 否 | 0 | 三问 |
| 29 | `78L5GaeZ` | EUR | 43 | 3.02/2.35 | 10 | .6662 | — | +.05 | ANALYST 10→11 否｜OTHER 3→4 否 | 0 | 三问 |
| 30 | `E56GgqLL` | EUR | 43 | 1.68/1.17 | **24** | .5524 | — | 0.00 | FUNDAMENTAL 3→4 否｜OTHER 3→4 否 | 0 | — |
| 31 | `d5apEYRx` | EUR | 41 | 1.77/1.05 | 8 | .6887 | — | +.17 | EARNINGS 1→2 否 | 0 | 三问·prod 贴线 |
| 32 | `d5a2vxzY` | DEU | 36 | 1.60/1.08 | 12 | .6039 | .604 | +.07 | SHORT 3→4 否 | 0 | 三问·三闸零余量 |

**塔点亮总账（当季 `get_pyramid_alphas` 实读，点亮线 ≥3）**：本轮最多新增 **4 座** —— `GBR/D1/OTHER 2→3`、`DEU/D1/OTHER 2→3`、`KOR/D1/PV 2→3`、`EUR/D1/RISK 2→3`。
同塔第二颗起**增量为 0**（表里已扣除）：例如 `leAmmre8` / `O0A6Qz7p` 也挂 GBR/OTHER，但 #1 已点亮。
⇒ **按分数排序 ≠ 按塔边际排序**；若目标是「用最少提交点亮最多塔」，取 #1 #2 #3 #8 四颗即可覆盖 4 座。

---

## 3 同席互斥（4 年日收益，17 颗头部 17×17）

| 超阈对 | ρ | 让位 |
|---|---:|---|
| `qM7KxkQV` ~ `88NmN37X` | **0.9773** | `qM7KxkQV`（分 61 < 62） |
| `omEdka3v` ~ `pwdLp9z6` | 0.8619 | `pwdLp9z6`（分 82） |
| `xAvK73Qg` ~ `Jj8VQwoe` | 0.7619 | `Jj8VQwoe` |
| `wpo8olA6` ~ `xAvK73Qg` | 0.7409 | `xAvK73Qg`（分 71） |
| `wpo8olA6` ~ `Jj8VQwoe` | 0.7372 | `Jj8VQwoe`（分 64） |

**最大独立集 = 13**（头部 17 颗）。族内 `qM7` 四颗 ρ .9346–1.0000 只留 1；DEU-OTHER 三颗 ρ .7372–.7619 只留 1。

⚠ **与今天上午六颗盘点的口径差异**：单独看那 6 颗时 `qM7KxkQV` 是首选；放进总体篮子后，同族的 `88NmN37X`（prod .5541 / ΔS +.74 / 9 ops / self 更干净）分数更高 ⇒ **`qM7KxkQV` 让位**。取哪颗取决于你是否已决定用 `88NmN37X` 换防。

---

## 4 ★ 推翻 11-12 EUR 交付篮子

`tracking/EUR/DELIVERABLE_17_VERIFIED.md` 宣称 17 颗「四重验证通过」，但本轮逐颗跑只读预检：

| alpha | 该报告 | 本轮实判 |
|---|---|---|
| `mL617YPx` | 篮子第 1 颗，prod .5421 | **`submit_gate` BLOCKED**：`ledger_kv[EUR/robustness_mL617YPx] = REJECT`（近三年 CV .641） |
| `N1P02YwL` | #4 | **ΔS −0.05 硬闸** |
| `VkxWmpYG` | #12 | **ΔS −0.04 硬闸** |
| `xArjE96W` | #3 | **ΔS −0.03 硬闸** |
| `qME6VWbj` | #9 | **ΔS −0.03 硬闸** |
| `WjOAJWxd` | #13 | **ΔS −0.01 硬闸** |
| `N1NGbddg` | #15 | **ΔS −0.12 硬闸**（与 11-11 session 报告一致） |
| `rKRx7v6m` / `WjOeNE6O` | #11 / #6 | 早年稳健/ΔS 冲突，本轮预检放行，但排位靠后 |

⇒ **17 颗里只有 10 颗真能交**，且 `YP1baJrv` prod .6999 差 .0001 必须重测。该报告的四重验证**没有包含 ΔS 闸与稳健台账闸**。

---

## 5 排除清单（11 颗）

| alpha | 排除原因 |
|---|---|
| `ZYQv7j2Q` | prod **.8159** + self **.816** 双超线 |
| `mL617YPx` | 稳健台账 **REJECT**，`submit_gate` 硬拦 |
| `N1NGbddg` / `N1P02YwL` / `VkxWmpYG` / `xArjE96W` / `qME6VWbj` / `WjOAJWxd` | **ΔS < 0 硬闸**（force 不豁免） |
| `LLMv6joe` / `d5a2aO7v` / `zqdvb0YE` | prod 未闭环（且 `d5a2aO7v`/`zqdvb0YE` 属 qM7 同族 ρ≈1.0） |

另已排除（未进 47 池）：`6XM87Zb7`(prod .7768) `2r50PAzJ`(ΔS −.02 + stack 5 腿) `Jj8w52Me`(stack 4 腿) `A1xZ7kNW`(CW 硬拦 + prod .8377)、各 op-min 变体、SUPERSEDED / REJECT / prod 超线族。

---

## 6 推荐

**只交 3 席（ET 11-12 剩 4 席）**：

| 序 | alpha | 理由 | 待办 |
|---|---|---|---|
| 1 | **`wpo8olA6`** | 8 ops、prod .6306、ΔS +.56、**mix kind=none 免三问**、稳健 PASS、prod 缓存 38.6h 有效 ⇒ **全闭环零待办** | 无 |
| 2 | **`omEdka3v`** | 8 ops、prod .6026、self .492、ΔS +.59、GBR OTHER 点亮 | 答 2 腿三问 |
| 3 | **`ZYQ116ln`** | 3 ops（最少）、prod .6981 贴线、KOR PV 点亮、与 #1/#2 ρ < .09 | `refresh=True` 终验 |

三颗点亮 **DEU/GBR/KOR 三座不同区塔**，彼此近乎正交。若再加第 4 席取 **`JjeNJ00O`**（EUR RISK 点亮，但 prod .6813 需 refresh + 三问）。

**提交前统一动作**：① 26 颗 `two_leg`/`three_leg` 需答三问；② 标「prod 刷新」的缓存 >48h 已作废，须 `refresh=True`；③ 标「prod 贴线」的余量 <.02，`YP1baJrv` 仅 .0001 建议直接弃；④ `RREPm361` 的 self 缓存 .6879 是旧值，实测 **.3275**；⑤ ΔS 禁横比（本池分 `EUR:1` / `EUR:1:POWER_POOL` / `DEU:1` / `DEU:1:POWER_POOL` / `GBR:1` / `GBR:1:POWER_POOL` / `IND:1:PP` / `KOR:1:PP` 共 8 个分区）。

**配额**：ET 2026-11-12 22:42 时 REGULAR 0/4 剩 4、SUPER 1/1 用尽；距 ET 次日重置约 1h。

---

## 7 产物与工程备注

- `results/full_basket_platform_20261113.json`（47 颗平台读数）
- `results/full_basket_corr_20261113.json`（prod/self/稳健）
- `results/full_basket_preflight_20261113.json`（47 颗 mix/ΔS/gate，只读）
- `results/full_basket_ranking_20261113.json`（36 排序 + 11 排除）
- `results/full_basket_executable_20261113.json`（32 可执行 + 4 让位 + 塔总账）
- 脚本：`results/_batch_preflight_local_20261113.py`、`_full_basket_rank_20261113.py`、`_full_basket_exec_20261113.py`

⚠ **MCP 服务在批量预检第 6 颗掉线**（`WinError 10054` 后全部 404）。已改为**本地节点直调** `wqb.workflow.nodes.submit_alpha.run(confirm_submit=False)` 完成 47 颗，结果一致。服务需重启后才能恢复 MCP 通道。
⚠ 本地库 `alphas.status` 有 8 颗状态错位（看似 UNSUBMITTED 实为 ACTIVE），本轮全部以平台 `GET /alphas/{id}` 为准。
