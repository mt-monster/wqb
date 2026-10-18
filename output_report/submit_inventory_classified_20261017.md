# 可提交 alpha 分类清单（盘点）

> 数据源：`submit_inventory_20261017-230846.json`（READY 池 162 颗）｜生成 2026-10-17T23:08:46+08:00
> 工具：`tools/verdict/submit_inventory.py --snapshot-only`（只读，绝不提交）
> 口径：RA 唯一通道（PPA 不接受）；模拟层无 FAIL/硬闸 WARNING + Failed-count=0 + prod/self<0.7

## 一、总览

| 分类 | 数量 | 含义 |
|---|---:|---|
| **SUBMIT_NOW** | **14**（原 21，USA 7 颗 refresh 后转出） | 全闸过 + 余量≥0.03 ⇒ 可提交（需用户逐次明示） |
| **THIN_MARGIN** | 18 | 全闸过但 prod/self 余量 <0.03 ⇒ 一碰就撞墙，建议不提 |
| **PROD_WALL** | **7**（USA，2026-10-18 refresh 实测） | 模拟层全过，仅相关性 ≥0.7（池子变化可恢复；勿 POST，会污染同族） |
| **HARD_BLOCKED** | 25 | 模拟层 FAIL / 硬闸 WARNING / Failed-count≠0 ⇒ 须修复重测 |
| **ALREADY_SUBMITTED** | 1 | 平台已 ACTIVE/SUBMITTED（勿重复 POST） |
| **CORR_UNKNOWN** | 97 | prod/self 缺失或未取得 ⇒ 先测相关性再判 |
| **ERROR** | 0 | 平台请求失败 |

台账全貌：`DEAD 717 / EXPIRED 67 / PROD_BLOCKED 7 / READY 162 / SELF_BLOCKED 2 / SUBMITTED 79 / SUPERSEDED 41`

## 二、SUBMIT_NOW（21）

### GBR（5）

| alpha | S | F | 2Y | TO | prod(余) | self(余) | ATOM | 数据集族 | 塔 |
|---|---:|---:|---:|---:|---:|---:|:--:|---|---|
| `P0gv3AO7` | 1.69 | 1.07 | 2.1 | 0.1362 | 0.5685 (0.1315) | 0.3888 (0.3112) | ✅ | (single/unprefixed) | GBR/D1/PV |
| `QPK26lQX` | 1.68 | 1.03 | 2.12 | 0.123 | 0.5385 (0.1615) | 0.4951 (0.2049) | ✅ | (single/unprefixed) | GBR/D1/MODEL |
| `j289xaxO` | 1.66 | 1.0 | 2.14 | 0.1282 | 0.5380 (0.1620) | 0.4839 (0.2161) | ✅ | (single/unprefixed) | GBR/D1/MODEL |
| `6XKwmQgE` | 1.62 | 1.04 | None | 0.1354 | 0.5956 (0.1044) | 0.4148 (0.2852) | ✅ | (single/unprefixed) | GBR/D1/PV |
| `QPKErLvX` | 1.59 | 1.0 | 1.72 | 0.1284 | 0.6593 (0.0407) | 0.5015 (0.1985) | ✅ | mdl | GBR/D1/MODEL |

### IND（9）

| alpha | S | F | 2Y | TO | prod(余) | self(余) | ATOM | 数据集族 | 塔 |
|---|---:|---:|---:|---:|---:|---:|:--:|---|---|
| `WjepYR7d` | 3.92 | 2.81 | 2.87 | 0.329 | 0.6573 (0.0427) | 0.6562 (0.0438) | ✅ | mdl | MATCHES_PYRAMID |
| `d51z7PVw` | 3.26 | 2.4 | 2.16 | 0.2886 | 0.5966 (0.1034) | 0.4461 (0.2539) | ✅ | oth | IND/D1/OTHER |
| `xA392Xpb` | 3.18 | 2.0 | None | 0.3288 | 0.6458 (0.0542) | 0.6452 (0.0548) | ✅ | (single/unprefixed) | IND/D1/PV |
| `JjQzbQJj` | 3.09 | 2.13 | 2.06 | 0.2932 | 0.5658 (0.1342) | 0.4090 (0.2910) | ❌ combined | BASE_MARKET,oth | IND/D1/OTHER |
| `3qX6wLJQ` | 3.07 | 2.34 | None | 0.2361 | 0.5071 (0.1929) | 0.3642 (0.3358) | ✅ | (single/unprefixed) | IND/D1/INSTITUTIONS |
| `kqJkPLeO` | 3.02 | 2.4 | 2.36 | 0.2247 | 0.5254 (0.1746) | 0.2703 (0.4297) | ❌ combined | BASE_MARKET,anl44 | IND/D1/PV |
| `e7QG2WJM` | 2.9 | 2.01 | 2.39 | 0.2873 | 0.5751 (0.1249) | 0.4043 (0.2957) | ✅ | oth | IND/D1/OTHER |
| `3qX6wLkP` | 2.84 | 1.74 | None | 0.3453 | 0.5836 (0.1164) | 0.5191 (0.1809) | ✅ | (single/unprefixed) | IND/D1/PV |
| `zq8wZgQO` | 1.6 | 1.12 | None | 0.0853 | 0.6477 (0.0523) | 0.3133 (0.3867) | ✅ | (single/unprefixed) | IND/D1/PV |

### USA（7）— ⚠ 已于 2026-10-18 refresh 后全部转 PROD_WALL，见第四节

原判 SUBMIT_NOW 的 7 颗，**prod 重测后全部爆线（0.9000–0.9991）**，已移出可提交清单。
下表保留旧快照仅供对照，**不可据此提交**：

| alpha | S | F | 旧 prod（已作废） | **新 prod（refresh）** | Δ |
|---|---:|---:|---:|---:|---:|
| `pw5RbrYX` | 2.07 | 1.21 | 0.5857 | **0.9000** | +0.3143 |
| `RR6bv6rz` | 2.04 | 1.20 | 0.5919 | **0.9054** | +0.3135 |
| `leKKGb9l` | 2.04 | 1.19 | 0.5896 | **0.9014** | +0.3118 |
| `rKeOaLvo` | 2.04 | 1.20 | 0.5932 | **0.9060** | +0.3128 |
| `KPrGMEe1` | 1.94 | 1.24 | 0.6593 | **0.9991** | +0.3398 |
| `KPrGp2G8` | 1.93 | 1.23 | 0.6649 | **0.9961** | +0.3312 |
| `rKe2woad` | 1.92 | 1.21 | 0.6697 | **0.9916** | +0.3219 |

## 三、THIN_MARGIN（18）

### GBR（8）

| alpha | S | F | 2Y | TO | prod(余) | self(余) | ATOM | 数据集族 | 塔 |
|---|---:|---:|---:|---:|---:|---:|:--:|---|---|
| `akxLxjVv` | 1.97 | 1.29 | 1.71 | 0.0814 | 0.6793 (0.0207) | 0.1129 (0.5871) | ✅ | (single/unprefixed) | GBR/D1/ANALYST |
| `d51O1kOX` | 1.97 | 1.29 | 1.71 | 0.0814 | 0.6793 (0.0207) | 0.1129 (0.5871) | ✅ | (single/unprefixed) | GBR/D1/ANALYST |
| `O08r8QNp` | 1.93 | 1.25 | 1.62 | 0.0793 | 0.6942 (0.0058) | 0.0597 (0.6403) | ✅ | (single/unprefixed) | GBR/D1/ANALYST |
| `blORMJwm` | 1.91 | 1.24 | 1.62 | 0.0789 | 0.6950 (0.0050) | 0.0623 (0.6377) | ✅ | (single/unprefixed) | GBR/D1/ANALYST |
| `P0gvv5gE` | 1.72 | 1.03 | 1.84 | 0.1223 | 0.6905 (0.0095) | 0.6364 (0.0636) | ✅ | (single/unprefixed) | GBR/D1/PV |
| `RR6NOlma` | 1.7 | 1.02 | 1.79 | 0.1224 | 0.6861 (0.0139) | 0.6348 (0.0652) | ✅ | (single/unprefixed) | GBR/D1/MODEL |
| `58gMMJEk` | 1.68 | 1.0 | 1.82 | 0.1235 | 0.6865 (0.0135) | 0.6386 (0.0614) | ✅ | (single/unprefixed) | GBR/D1/PV |
| `9qWwZ3go` | 1.67 | 1.09 | None | 0.134 | 0.6890 (0.0110) | 0.5952 (0.1048) | ✅ | mdl | GBR/D1/PV |

### IND（1）

| alpha | S | F | 2Y | TO | prod(余) | self(余) | ATOM | 数据集族 | 塔 |
|---|---:|---:|---:|---:|---:|---:|:--:|---|---|
| `786wl6b8` | 3.86 | 2.57 | 2.4 | 0.3721 | 0.6897 (0.0103) | 0.6786 (0.0214) | ✅ | mdl | MATCHES_PYRAMID |

### KOR（1）

| alpha | S | F | 2Y | TO | prod(余) | self(余) | ATOM | 数据集族 | 塔 |
|---|---:|---:|---:|---:|---:|---:|:--:|---|---|
| `LLZ6wZO2` | 1.99 | 1.53 | 2.24 | 0.144 | 0.6762 (0.0238) | 0.6760 (0.0240) | ✅ | oth | KOR/D1/FUNDAMENTAL |

### USA（8）

| alpha | S | F | 2Y | TO | prod(余) | self(余) | ATOM | 数据集族 | 塔 |
|---|---:|---:|---:|---:|---:|---:|:--:|---|---|
| `58gp1wdz` | 1.89 | 1.18 | 1.72 | 0.0609 | 0.6738 (0.0262) | 0.4237 (0.2763) | ✅ | (single/unprefixed) | USA/D1/PV |
| `1YZp6EP6` | 1.86 | 1.14 | 1.7 | 0.0613 | 0.6783 (0.0217) | 0.4214 (0.2786) | ✅ | (single/unprefixed) | USA/D1/PV |
| `XgJoXm50` | 1.84 | 1.12 | 1.68 | 0.0616 | 0.6823 (0.0177) | 0.4191 (0.2809) | ✅ | (single/unprefixed) | USA/D1/PV |
| `E5RGoOX1` | 1.81 | 1.09 | 1.65 | 0.0619 | 0.6869 (0.0131) | 0.4163 (0.2837) | ✅ | (single/unprefixed) | USA/D1/PV |
| `O08GeKx1` | 1.8 | 1.07 | 1.65 | 0.062 | 0.6911 (0.0089) | 0.4137 (0.2863) | ✅ | (single/unprefixed) | USA/D1/PV |
| `1YZpv1bK` | 1.79 | 1.06 | 1.66 | 0.062 | 0.6934 (0.0066) | 0.4122 (0.2878) | ✅ | (single/unprefixed) | USA/D1/PV |
| `YPMvZZvv` | 1.79 | 1.06 | 1.68 | 0.062 | 0.6958 (0.0042) | 0.4106 (0.2894) | ✅ | (single/unprefixed) | USA/D1/PV |
| `9qWpQlO9` | 1.78 | 1.05 | 1.69 | 0.0619 | 0.6982 (0.0018) | 0.4087 (0.2913) | ✅ | (single/unprefixed) | USA/D1/PV |

## CORR_UNKNOWN（97）

区域分布：ASI×1, DEU×4, EUR×2, GBR×51, GLB×12, HKG×2, IND×11, USA×14


## HARD_BLOCKED（25）

区域分布：ASI×1, EUR×2, GBR×2, GLB×13, USA×7

拦截原因：`FAILED_COUNT_RA:LOW_GLB_EMEA_SHARPE`×11, `SIM_FAIL:LOW_SUB_UNIVERSE_SHARPE`×9, `FAILED_COUNT_RA:LOW_2Y_SHARPE`×2, `FAILED_COUNT_RA:CONCENTRATED_WEIGHT`×2, `SIM_FAIL:LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO`×1


## ALREADY_SUBMITTED（1）

区域分布：GBR×1

| alpha | 区域 | 平台状态 |
|---|---|---|
| `npP83YQq` | GBR | ACTIVE |

## ⚠ 三条提交前必读

1. **相关性已过期**：清单中 prod/self 快照年龄 **175–288h（7–12 天）**，远超 48h 新鲜窗口纪律。实证 prod 会从 0.68 漂到 0.98 ⇒ **提交前必须 `check_correlation(refresh=True)` 重测**，拦不住就淘汰换下一颗。
2. **配额 1 次/天/区**：同区域一天只能提交 1 颗，需错峰安排。
3. **ATOM 明令（2026-10-17）**：combined（≥2 数据集）不作交付目标。本次 39 颗中 **37 判 ATOM、2 判 combined**（`JjQzbQJj`、`kqJkPLeO`，均含 `returns` 残差化标志）。⚠ `WjepYR7d` 含 `mdl37_` + 无前缀 pv 字段，疑似 combined 待 AtomResolver 复核。
---

## 四、★ prod refresh 实测更新（2026-10-17 23:44 → 10-18 00:07）

对 USA SUBMIT_NOW 7 颗执行 `check_correlation(refresh=True)` 重测，结果**全部爆线**：

| alpha | 旧 prod | 新 prod | Δ | 余量 | 判定 |
|---|---:|---:|---:|---:|---|
| `pw5RbrYX` | 0.5857 | **0.9000** | +0.3143 | −0.2000 | ❌ FAIL |
| `RR6bv6rz` | 0.5919 | **0.9054** | +0.3135 | −0.2054 | ❌ FAIL |
| `leKKGb9l` | 0.5896 | **0.9014** | +0.3118 | −0.2014 | ❌ FAIL |
| `rKeOaLvo` | 0.5932 | **0.9060** | +0.3128 | −0.2060 | ❌ FAIL |
| `KPrGMEe1` | 0.6593 | **0.9991** | +0.3398 | −0.2991 | ❌ FAIL |
| `KPrGp2G8` | 0.6649 | **0.9961** | +0.3312 | −0.2961 | ❌ FAIL |
| `rKe2woad` | 0.6697 | **0.9916** | +0.3219 | −0.2916 | ❌ FAIL |

**存档已更新**：`alpha_corr_cache` 权威表 7 条全部回写（source=platform_sync），明细 `results/usa_prod_refresh_20261017.json`。

### 结论与推论

1. **USA 7 颗全部转入 PROD_WALL，不可提交。** 旧快照（7–12 天前）系统性偏乐观 0.31–0.34。
2. **漂移幅度前所未见**：全部 7 颗同步从 ~0.59/0.66 跳到 0.90+，其中 2 颗逼近 1.0（0.9991 / 0.9961 ≈ 与某生产 alpha 近乎同一条腿）。这不是随机噪声，是**生产池被同机制 alpha 批量填满**的信号。
3. **⚠ 同等推论适用于其余区域**：IND / GBR / KOR 清单中的 prod 同样是 175–288h 前的快照，**在 refresh 之前一律不可信、不可提交**。特别提醒：我此前建议的 IND `3qX6wLJQ`（快照 prod 0.507）也必须先 refresh 再决定——快照越好看，越可能是过期幻觉。
4. **纪律固化**：>48h 的 prod 只作「待重测」标记，不构成提交依据。任何提交动作前必须 `check_correlation(refresh=True)` 实时终验。
