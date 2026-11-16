# 各 Region 最优 SuperAlpha 方案 · 2026-11-16（配方四轴版）

> 执行窗口：2026-11-16 06:31 → 08:0x（GMT+8，ET 2026-11-15 18:3x–20:0x）
> **本轮未提交任何 alpha**（`WQB_ALLOW_ALPHA_SUBMIT` 未开启，未调用 `submit` / POST `/submit`）。
> 判据：三条件 `S ≥ 5 ∧ F ≥ 5 ∧ prod ≤ 0.65`；自设余量闸 `prod ≤ 0.68 ∧ self ≤ 0.68` 不放宽。

---

## 0 执行摘要

**一轮定论：GBR 首次在 S 与 F 上双过三条件，唯一缺口是 prod 0.012。**

| 序 | ID | 档位 | 配方 | S | F | TO | prod | self | 三条件 | 席位 |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | `A1xOakkY` | GBR/TOP700 | SLOW d3 **l16** LC | **5.07** | **5.21** | .1348 | **.6621** | .6618 | 2/3（prod −0.012） | 新席 ρ.646 |
| 2 | `YPaW2WKq` | GBR/TOP700 | SLOW d4 l14 LC | 5.08 | 5.26 | .1292 | .6623 | .6625 | 2/3（prod −0.012） | 同席（ρ.995） |
| 3 | `P05XXeNx` | GBR/TOP700 | SLOW d3 l14 LC | 5.14 | 5.18 | .1385 | .6629 | .6631 | 2/3（prod −0.013） | 同席 |
| 4 | `QP055ze5` | GBR/TOP700 | SLOW d5 l16 LC | 4.95 | 5.22 | **.1203** | **.6540** | .6536 | 1/3（S−0.05, prod−0.004） | 同席 |
| 5 | `akaWlXm2` | GBR/TOP700 | SLOW d1 l16 LC | **5.19** | 4.84 | .1687 | .6659 | .6656 | 1/3（F−0.16） | 同席 |

- **排序第一 = `A1xOakkY`（未提交，待用户指令）**。前 5 名全部是 **GBR/TOP700 SLOW 同一席**（互测 ρ .995），**只能取一颗**。
- GBR 现役最强 = `3qompGeZ` S4.42/F4.27/.6221 ⇒ 本轮件 **S +0.65 / F +0.94**，边际成立。
- 三条件全达区仍是 **USA / IND / KOR**（全部为已提交件，本轮无新建件入列）。
- 本轮共 **33 条仿真**（32 新建 + 1 条平台去重命中已提交件）。

---

## 1 池与档位基线（2026-11-16 06:35 刷新）

### 1.1 组件池（ACTIVE 已提交 REGULAR，硬前置 ≥10）

| 区 | 池 | 环比 11-15 | 区 | 池 | 环比 |
|---|---|---|---|---|---|
| USA | **49** | +1 | GLB | 19 | 0 |
| IND | **48** | +1 | DEU | 21 | 0 |
| KOR | 35 | 0 | MEA | 19 | 0（区域已下架） |
| GBR | 28 | 0 | ASI | 10 | 0 |
| EUR | 28 | 0 | HKG | 7 | 0 ⇒ **BLOCKED（7/10）** |

### 1.2 ACTIVE SUPER = **57**（+1）

新增唯一一颗：**`KPg60XNp` KOR/TOP600 SLOW d1 **l30** → S5.96 / F7.50 / TO .1729 / prod .5475**（ET 11-15 01:25 提交）
⇒ **KOR 成为第 3 个三条件达标区**（此前 KOR 最佳 9qWbA1g9 = 4.98/4.93/.6883）。

**★ 该件同时证伪两条旧口径**：
1. **`l10` 甜点论失效**：KOR l30（86% of 35）拿到 S5.96/F7.50，prod 反而 .5475 最干净 —— limit 不是"越大 prod 越脏"的单调关系，KOR 的 prod 峰在更早的 l12（`rKOPg9gd` .8312）。
2. **本轮复现撞平台去重**：我用 `SLOW d1 l30 + LC + CBW` 重跑，平台直接返回**同一个 alpha id `KPg60XNp`** ⇒ 该件的 selection 主键**就是 `long_count`**、combo 就是 CBW。**完全相同配置不会新建，会返回既有件**（以后重跑同配方要先比对 settings）。

### 1.3 档位占用（18 档）

| 区 | Universe | SUPER | 状态 |
|---|---|---|---|
| IND | TOP500 | 12 | 🔴 饱和 |
| KOR | TOP600 | 12 | 🔴 饱和（新件 l30 占宽位） |
| GBR | TOP700 | 6 | 🟡 **本轮唯一产出区**（SLOW 席干净） |
| USA | TOP3000 | 6 | 🔴 饱和 |
| EUR | TOP2500 | 4 | 🟡 SLOW@现行位已占，F 结构性短 |
| USA | TOP2000 | 2 | 🔴 停投 |
| DEU / MEA / GLB(MINVOL1M, MINVOL10M) | — | 各 2/1 | 🔴 停投 |
| **零 SUPER 档** | — | 0 | ⚫ **连续第 5 轮为 0** |

### 1.4 Pyramid 倍率（D1，仅记录）

DEU 1.5–1.8（最高）/ GBR 1.6 / KOR 1.6 / EUR 1.5 / ASI 1.5 / USA 1.4 / GLB 1.4。
**SA 的 `is.checks` 无 `MATCHES_PYRAMID` ⇒ SA 不参与塔计数**，倍率不作选塔理由。

---

## 2 配方四轴扫描矩阵（本轮 33 条，全部 `refresh` 新建）

> 唯一凭据：每条都给 `区/族/decay/limit/主键 → S/F/TO`。prod 空 = 未实测（不入排序表）。

| # | tag | ID | 区 | 族 | d | lim | 主键 | S | F | TO | prod | self |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | gbr_slow_d1_l16 | akaWlXm2 | GBR | SLOW | 1 | 16 | LC | 5.19 | 4.84 | 0.1687 | 0.6659 | 0.6656 |
| 2 | gbr_slow_d3_l14lc | P05XXeNx | GBR | SLOW | 3 | 14 | LC | 5.14 | 5.18 | 0.1385 | 0.6629 | 0.6631 |
| 3 | gbr_stat_d3_l16 | O0W5kZ3d | GBR | STATISTICAL | 3 | 16 | LC | 5.13 | 5.16 | 0.1382 | 0.8001 | 0.8003 |
| 4 | gbr_slow_d4_l14lc | YPaW2WKq | GBR | SLOW | 4 | 14 | LC | 5.08 | 5.26 | 0.1292 | 0.6623 | 0.6625 |
| 5 | gbr_slow_d3_l16lc | A1xOakkY | GBR | SLOW | 3 | 16 | LC | 5.07 | 5.21 | 0.1348 | 0.6621 | 0.6618 |
| 6 | gbr_stat_d5_l16lc | Jj85XGll | GBR | STATISTICAL | 5 | 16 | LC | 5.02 | 5.25 | 0.1240 | — | — |
| 7 | gbr_stat_d3_l18lc | QP05lOoK | GBR | STATISTICAL | 3 | 18 | LC | 5.00 | 5.12 | 0.1352 | — | — |
| 8 | gbr_slow_d4_l16lc | ZYaW25v1 | GBR | SLOW | 4 | 16 | LC | 5.00 | 5.27 | 0.1265 | — | — |
| 9 | gbr_slow_d5_l16lc | QP055ze5 | GBR | SLOW | 5 | 16 | LC | 4.95 | 5.22 | 0.1203 | 0.6540 | 0.6536 |
| 10 | gbr_slow_d3_l16mix | E5QrrYlP | GBR | SLOW | 3 | 16 | MIX | 4.74 | 4.77 | 0.1336 | — | — |
| 11 | gbr_sec_d3_l16 | XgaYLGd8 | GBR | SECTOR | 3 | 16 | LC | 4.19 | 5.01 | 0.1209 | — | — |
| 12 | gbr_sec_d3_l18 | N1P56Z0p | GBR | SECTOR | 3 | 18 | LC | 4.02 | 4.85 | 0.1163 | — | — |
| 13 | gbr_sub_d3_l16lc | VkNYYRp0 | GBR | SUBINDUSTRY | 3 | 16 | LC | 3.93 | 4.28 | 0.1245 | — | — |
| 14 | gbr_cwd_d3_l16lc | YPaWW9po | GBR | CROWDING | 3 | 16 | LC | 3.83 | 4.39 | 0.1232 | — | — |
| 15 | gbr_sec_d3_l16m | e7aqK9GO | GBR | SECTOR | 3 | 16 | MIX | 3.75 | 4.26 | 0.1215 | — | — |
| 16 | glb_stat_d1_l11 | QP05jLGQ | GLB | STATISTICAL | 1 | 11 | LC | 6.56 | 3.76 | 0.3088 | — | — |
| 17 | glb_stat_d1_l12m | e7aqKPVM | GLB | STATISTICAL | 1 | 12 | MIX | 6.48 | 3.61 | 0.2644 | — | — |
| 18 | glb_stat_d3_l12 | P05X6vgp | GLB | STATISTICAL | 3 | 12 | LC | 6.29 | 4.22 | 0.2042 | 0.8366 | — |
| 19 | glb_stat_d1_l10lc | vRAJe0mr | GLB | STATISTICAL | 1 | 10 | LC | 6.25 | 3.45 | 0.3321 | — | — |
| 20 | glb_stat_d4_l12lc | mLaxxOz6 | GLB | STATISTICAL | 4 | 12 | LC | 6.11 | 4.23 | 0.1861 | 0.8275 | — |
| 21 | glb_stat_d1_l10d | 1YWnmQdz | GLB | STATISTICAL | 1 | 10 | 1-prod | 6.04 | 3.20 | 0.2468 | — | — |
| 22 | glb_stat_d5_l12lc | RRekabkd | GLB | STATISTICAL | 5 | 12 | LC | 5.95 | 4.22 | 0.1726 | — | — |
| 23 | glb_slow_d3_l14lc | blaWWQrR | GLB | SLOW | 3 | 14 | LC | 5.92 | 3.97 | 0.1721 | — | — |
| 24 | glb_rm_d1_l14lc | 2r5nnGQJ | GLB | REVERSION_AND_MOMENTUM | 1 | 14 | LC | 4.73 | 3.19 | 0.2462 | — | — |
| 25 | eur_stat_d1_l16m | rK7rLxzo | EUR | STATISTICAL | 1 | 16 | MIX | 5.04 | 3.77 | 0.1576 | — | — |
| 26 | eur_sub_d1_l24d | 3q0n6vV0 | EUR | SUBINDUSTRY | 1 | 24 | 1-prod | 4.48 | 4.71 | 0.1185 | — | — |
| 27 | eur_sub_d1_l16d | MP655j2L | EUR | SUBINDUSTRY | 1 | 16 | 1-prod | 4.19 | 4.10 | 0.1338 | — | — |
| 28 | eur_sub_d1_l16m | LLKl6KVM | EUR | SUBINDUSTRY | 1 | 16 | MIX | 4.10 | 4.02 | 0.1314 | — | — |
| 29 | eur_slow_d2_l16d | Jj85Xd0l | EUR | SLOW | 2 | 16 | 1-prod | 3.83 | 2.87 | 0.1273 | — | — |
| 30 | eur_sub_d1_l12m | gJaoKM2O | EUR | SUBINDUSTRY | 1 | 12 | MIX | 3.64 | 3.32 | 0.1315 | — | — |
| 31 | eur_sub_d1_l10lc | xAvmzOPb | EUR | SUBINDUSTRY | 1 | 10 | LC | 3.59 | 3.21 | 0.1360 | — | — |
| 32 | eur_slow_d2_l12m | e7aqKbQE | EUR | SLOW | 2 | 12 | MIX | 3.30 | 2.27 | 0.1222 | — | — |
| 33 | kor_slow_d1_l30lc | KPg60XNp | KOR | SLOW | 1 | 30 | LC | 5.96 | 7.50 | 0.1729 | — | — |

**四轴归因（本轮）**

| 轴 | 本轮实际动作 | 结果 |
|---|---|---|
| **① 主键 `long_count`** | GBR 5 族 × l16；GLB 3 族；EUR 2 族 | **GBR 是全轮唯一受益区**：SLOW l16 S4.42(现役)→5.19。**EUR/GLB 全部反向**：EUR SUBIND l10 LC S6.13→3.59；GLB l10 LC S6.04→6.25 但 TO .2468→.3321（F 3.20→3.45 仍不够） |
| **② limit 曲线** | GBR l14/16/18、GLB l11/12/14、EUR l12/16/24 | **GBR 峰 = l14–l16（50–57%）**，l18 转跌（4.02–5.00）；**EUR limit↑ 单调摊薄 S**（l10 6.54 → l24 4.48）；GLB l11 S 峰但 TO 炸 |
| **③ combo 形状** | 全程 `w=1−maxCorr`（CBW），未改 | 未动（历史已封：cp≥3/rank/zscore/sqrt 全负） |
| **④ 中性化族** | GBR 5 族对照；GLB 3 族；EUR 3 族 | **零增益维再证**：GBR 族间差异全部来自 prod（STAT .800 / SLOW .662 / SECTOR 未测），S 由 limit+主键决定 |

---

## 3 三条件达成矩阵

| 区 | 本轮最佳件 | S | F | TO | prod | self | gap→S5 | gap→F5 | gap→prod.65 | 项数 |
|---|---|---|---|---|---|---|---|---|---|---|
| **GBR** | `A1xOakkY` | 5.07 | 5.21 | .1348 | .6621 | .6618 | **+0.07** | **+0.21** | **−0.012** | **2/3** |
| USA | `A1V0eZne`（已提交） | 6.39 | 7.06 | .1178 | .6146 | .5884 | +1.39 | +2.06 | +0.035 | ✅ 3/3 |
| IND | `QPbjxMYw` / `wpbQjeKp`（已提交） | 5.37/5.41 | 5.74/5.27 | .2042/.2345 | .650/.631 | 同 | +0.37 | +0.74 | 0.000/+0.019 | ✅ 3/3 |
| KOR | `KPg60XNp`（已提交 11-15） | 5.96 | 7.50 | .1729 | .5475 | .5475 | +0.96 | +2.50 | +0.103 | ✅ 3/3 |
| GLB | `mLaxxOz6` | 6.11 | 4.23 | .1861 | **.8275** | — | +1.11 | **−0.77** | −0.178 | 1/3 |
| EUR | `3q0n6vV0`（本轮）/ 现役 `E5Q7RGNR` | 4.48 / 6.54 | 4.71 / 4.54 | .1185/.2263 | —/.567 | —/.375 | −0.52/+1.54 | −0.29/−0.46 | — | 1/3 |
| DEU | `vR1oxZA3` | 3.27 | 3.09 | .1828 | .5987 | .5987 | −1.73 | −1.91 | +0.051 | 0/3 |
| MEA | `78jYpn0Z` | 2.52 | 2.99 | .0522 | .6996 | .6996 | −2.48 | −2.01 | −0.050 | 0/3 |
| ASI | `d5WGG5bg` | 5.38 | 2.99 | .2923 | .5100 | .5100 | +0.38 | −2.01 | +0.140 | 1/3 |

> EUR 本轮新建件全部劣于现役（6.54），按 §5.5 硬前置「未超区内最强件即无边际」⇒ **EUR 本轮无边际**。

---

## 4 互测矩阵（本地 `compute_mutual_correlation`，4 年日收益）

| | A1xOakkY | akaWlXm2 | O0W5kZ3d | 3qompGeZ | QPvGdLYQ |
|---|---|---|---|---|---|
| **A1xOakkY** | 1 | **.9952** | .8091 | .6618 | .6209 |
| **akaWlXm2** | .9952 | 1 | .8089 | .6656 | .6238 |
| **O0W5kZ3d** | .8091 | .8089 | 1 | .8003 | .4958 |
| **3qompGeZ**（现役） | .6618 | .6656 | .8003 | 1 | .5104 |
| **QPvGdLYQ**（现役） | .6209 | .6238 | .4958 | .5104 | 1 |

**判读**
1. `A1xOakkY` / `akaWlXm2` / `P05XXeNx` / `YPaW2WKq` / `QP055ze5` / `ZYaW25v1` 互为 **ρ .995** ⇒ **同一席**（只差 decay/limit），全族只能取 1 颗。
2. 与现役 `3qompGeZ` ρ **.646–.666 < 0.7** ⇒ **真独立席**（不是同席替代）。
3. `O0W5kZ3d`（STAT）与 `3qompGeZ` ρ .8003 ⇒ 与现役 STAT 族同席，且 prod .8001 双杀。

---

## 5 分 Region 方案

### 5.1 GBR / TOP700 — **本轮唯一有产能的区**

**最优配方（`A1xOakkY`）**
```
region=GBR  universe=TOP700  delay=1  neutralization=SLOW  decay=3  truncation=0.02
selectionLimit=16  selectionHandling=POSITIVE  nanHandling=ON

selection = if_else(is_nan(long_count), 1, long_count) * (self_correlation < 0.7)
            * (turnover > 0.01) * (turnover < 0.6)
combo     = stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500);
            ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic);
            w = 1 - maxCorr; w
```
预期：S 5.07 / F 5.21 / TO .1348 / 2Y 5.10 / sub 3.31 / 13 checks 0 FAIL
双闸（实测 07:14 ET）：prod **.6621** / self **.6618** ⇒ 余量 .0179 / .0182
对照现役 `3qompGeZ`（S4.42/F4.27/.6221）：**S +0.65、F +0.94**，且 ρ .646 独立席。

**同席备选（三选一，不可叠加）**

| ID | 配方差异 | 优势 | 劣势 |
|---|---|---|---|
| `YPaW2WKq` | decay 4 / l14 | **F 5.26 最高**、TO .1292 最低 | S 5.08 略低于 P05XXeNx |
| `P05XXeNx` | decay 3 / l14 | **S 5.14 最高** | F 5.18 最低、余量 .0171 |
| `QP055ze5` | decay 5 / l16 | **prod .6540 最低**（离 .65 仅 0.004） | S 4.95 差 0.05 |

> 选型建议：若要「压 prod 冲三条件」选 `QP055ze5`（再补一点 S 即可）；若要「稳过 0.68 闸且指标最厚」选 `A1xOakkY`；若要「F 最高」选 `YPaW2WKq`。

### 5.2 GLB / MINVOL1M — **F 结构性短，本轮判无边际**

- 最佳：`mLaxxOz6` STAT d4 l12 → S6.11 / F4.23 / TO .1861，**prod .8275** 双杀。
- F 天花板实测：d1 3.20 → d3 4.22 → d4 4.23 → d5 4.22（**decay 收益在 d3 见顶**，TO 已压到 .1726 仍 F 4.22）。
- 换族：SLOW l14 S5.92/**F3.97**（更差）；R&M l14 S4.73/F3.19（最差）。
- **§4.0 基线复现发现池漂移**：`LL5amzov`（STAT d1 l10，10-14 提交）录 S6.93，本轮同配置重跑 `1YWnmQdz` 仅 **S6.04 / F3.20** ⇒ **历史 6.93 不可作为本轮基线**（GLB 池虽仍 19 颗，成分质量已变）。

### 5.3 EUR / TOP2500 — **F 结构性短，全部轴负向**

- 现役最佳：`E5Q7RGNR` SLOW d2 l10 S6.54/F4.54/.567；F 差 0.46。
- 本轮 8 条全劣：`3q0n6vV0` l24 S4.48（limit↑ 摊薄）；`xAvmzOPb` LC S3.59（LC 崩）；MIX 3.30–4.10（混主键崩）。
- **结论**：EUR 的 S 全部来自 l10 少数高分化成分，任何"扩成分"操作都摊薄 S；F 只能靠压 TO，而 EUR 的 decay d3 已知杀 S（11-15）。⇒ **EUR 停投（第 7 次确认）**。

### 5.4 USA / IND / KOR — 三条件已达标，本轮不投入

- USA `A1V0eZne` 6.39/7.06/.6146、IND `QPbjxMYw`+`wpbQjeKp`、KOR `KPg60XNp` 6.0/7.5/.5475 全为已提交件。
- 新增件必须 **同时超过区内最强 S 与 F** 才有边际；本轮把算力按"差距最小的区优先"原则全投 GBR/GLB/EUR，USA/IND/KOR **未派仿真**（有意为之，非遗漏）。

### 5.5 DEU / MEA / ASI — 池质量不足，停投

DEU 池 21 但 S 天花板 3.27；MEA 区域已下架（新建 400）；ASI 池 10，F 天花板 2.99。

---

## 6 撞墙档案（本轮新增，全部带实测值）

| 类别 | 撞墙项 | 实测 |
|---|---|---|
| **prod 族级** | GBR `STATISTICAL` | `O0W5kZ3d` prod **.8001**（S5.13/F5.16 IS 双过，prod 一票否决）；GBR 已有 3 颗 STAT SUPER |
| **prod 族级** | GLB `STATISTICAL` | `.8366`（d3 l12）、`.8275`（d4 l12）两样本，同族全灭 |
| **S 天花板** | GBR `SECTOR` | l14 4.53（11-15）/ l16 4.19 / l18 4.02 ⇒ 单调跌，无 l 可取 |
| **S 天花板** | GBR `SUBINDUSTRY` / `CROWDING` | 3.93 / 3.83（l16 d3），均低于 SLOW 的 5.07 |
| **F 天花板** | GLB 全区 | max F 4.23（S6.11），需 TO ≤ .168 才能 F5，已压到 .1726 仍差 |
| **F 天花板** | EUR 全区 | max F 4.71（S4.48）；现役 F4.54（S6.54） |
| **轴负向** | `MIX = LC×(0.7−prod)` 主键 | GBR −0.33 S（5.07→4.74）、EUR −1.6 S、GLB −0.05 S |
| **轴负向** | EUR limit↑ | l10 6.54 → l16 4.19 → l24 4.48 |
| **平台机制** | 同配置去重 | KOR `SLOW d1 l30 + LC + CBW` 重跑直接返回 `KPg60XNp`（不新建） |

---

## 7 算子利用率审计（按「是否有增益」分类，不按覆盖率）

| 分类 | 算子/片段 | 本轮证据 |
|---|---|---|
| **有正增益** | `if_else(is_nan(long_count),1,long_count)` 作排序主键 | GBR SLOW l16：S 4.42(现役 STAT 默认主键) → **5.19**；全轮唯一增益轴 |
| **零增益（保号单调）** | `(self_correlation<0.7)`、`(turnover>0.01)*(turnover<0.6)` 门控 | l10 下加不加同批产出相同（只做成分过滤，不改序） |
| **负增益** | `(0.7 - prod_correlation)` 混入主键 | GBR −0.33 / EUR −1.6 / GLB −0.05 |
| **负增益** | limit 超区内峰（GBR l18、EUR l16+） | GBR 4.02–5.00 / EUR 4.19–4.48 |
| **未使用（历史已封）** | `combo_power`≥3、`rank(w)`、`zscore(w)`、`sqrt(w)`、`ts_mean(w,n)`、`winsorize` | 11-07～11-14 五轮全负，本轮不重复投入 |
| **不可用** | `author_*` 系列、裸 `sharpe`/`fitness` | 自有池恒常数 / 平台无此字段（11-15 已定案） |

> 覆盖率口径：本轮 33 条仿真只用到 **2 个** selection 表达式片段 + 1 个固定 combo ⇒ 低覆盖率是**刻意的**（四轴中 ③④ 已证零增益，重复扫不产生信息）。

---

## 8 元评估：卡在哪一轴，需要什么外部条件

**结论：全轮只剩 1 个缺口 —— GBR 的 prod（0.6621 vs 目标 0.65，差 0.012），其余区全是结构性的 S/F 上限。**

1. **GBR 卡 prod，不卡配方。** 本轮已把 GBR 的 S 从 4.42 推到 5.19（+17%）、F 从 4.27 推到 5.26（+23%），两个指标都过了三条件线。prod 的 .662–.666 平台来自**与现有 6 颗 GBR SUPER 的相关**（top1 = `3qompGeZ` .646、`QPvGdLYQ` .621）。
   - 唯一可动的是 **decay**：d1 .6659 → d3 .6621 → d5 .6540（**−0.012/两档**），但每加深一档 S 掉 0.06–0.12。
   - **要突破需要外部条件之一**：① GBR 池再增 3–5 颗 REGULAR（`pool ↑ ⇒ prod ↓` 在 DEU 有 −0.048 先例）；② 现有 GBR SUPER 中某个被 SUPERSEDED 释放席位；③ 找到 S>5 ∧ prod<.65 的第六族（SECTOR/SUBIND/CROWDING 已证 S 天花板 4.5 以下）。

2. **GLB 卡 F，且 STAT 族已毒。** F 的唯一杠杆是 TO（`F = S·√(R/TO)`），GLB 的 TO 已从 .2468 压到 .1726（−30%），F 只从 3.20 升到 4.23，因为 **R 同步下滑**（S 6.04→5.95）。**要突破需 combo 层权重时序平滑**（`ts_mean(w, n)` / `hump`），本轮未测 —— 这是下一轮唯一未试过的 F 杠杆。

3. **EUR 卡 F 且已无自由成分。** limit/主键/decay 三轴全负，S 6.54 的成分集无法再扩。**除非换信息源（新数据集进池），否则 EUR 永久停投。**

4. **本轮没有"继续观察"这种结论**：GBR 有明确的可执行下一步（decay 4 / 池增长），GLB 有明确未试杠杆（combo 时序平滑），EUR 有明确死刑判据（三轴全负 + 7 次确认）。

---

## 9 提交建议（**只写建议，本轮未执行任何提交**）

### 9.1 建议对象

| 顺位 | ID | prod（实测 07:14 ET） | self | IS checks | 台账 REJECT | 与同档已有 SUPER 互测 ρ | 判定 |
|---|---|---|---|---|---|---|---|
| **1** | `A1xOakkY` | **.6621** ✅ ≤.68 | **.6618** ✅ | **0 FAIL / 0 WARNING** | 无（新建，未入台账） | .6461（`3qompGeZ`）✅ <0.7 新席 | **可交（余量 .0179）** |
| 2 | `YPaW2WKq` | .6623 ✅ | .6625 ✅ | 0 FAIL | 无 | .995 vs 顺位 1 ⇒ **同席，顺位 1 提交后作废** | 备选（F 最高 5.26） |
| 3 | `P05XXeNx` | .6629 ✅ | .6631 ✅ | 0 FAIL | 无 | 同上 | 备选（S 最高 5.14） |

> **三颗同席，只能交一颗**。若用户偏好"prod 最干净"，则换 `QP055ze5`（.6540 / self .6536，但 S 4.95 < 5）。

### 9.2 配额

- 规则：`SUPER_SUBMISSION` **1 颗 / ET 日历日 / 账户级 / 00:00 ET 重置**。
- 当前 ET：**2026-11-15 18:3x**；本 ET 日**已用**（`KPg60XNp` 提交时间 ET 2026-11-15 01:25）。
- ⇒ **下一个可用配额 = GMT+8 2026-11-16 13:00**（ET 11-16 00:00 重置）。
- 若今日提交，需等 13:00 后；届时本轮双闸值（07:1x 实测）仍在 48h 保鲜内，但**建议提交前 `refresh=True` 复测**（GBR 池在涨，prod 会漂）。

### 9.3 命令模板（**只写，未运行**）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 \
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit \
  --alpha-id A1xOakkY --region GBR
```

### 9.4 两个提交坑（历史实证，非本轮）

1. **提交前停掉后台批次**：并发仿真会让 `_probe_prod_max` 抛 ProxyError ⇒ fail-closed 拒交（会被误读成 prod 超标）。
2. **prod 槽 195s 冷却**（`logs/_dblock/correlation.cooldown.json`）：若刚做过 `check_correlation`，需等冷却归零再 submit，否则同样 fail-closed。

---

## 10 本轮产物清单

| 类型 | 路径 |
|---|---|
| 本文档 | `output_report/SA_best_per_region_plan_20261116.md` |
| 池盘点 | `results/sa_scan_20261116/probe_refresh.log` |
| SUPER 档位表 | `results/sa_scan_20261116/super_list.json`（57 颗 ACTIVE） |
| 扫描矩阵 | `results/sa_scan_20261116/scan_matrix.json`、`matrix_table.md` |
| 仿真原始产物 | `results/sa_scan_20261116/res_*.json` + `log_*.log`（33 组） |
| 构建脚本 | `build.sh` / `build2.sh` / `build3.sh` / `build4.sh` |

---

## 11 追加批次（11:29–12:05）：按「近十日新提交 REGULAR 的区」重试组 SA

### 11.1 新件分布（近 10 日 ACTIVE REGULAR，30 颗）

| 区 | 池 | 新件 | 占比 | 新件族构成 |
|---|---|---|---|---|
| DEU | 21 | **9** | **43%** | FAST×4 / SUBIND×5（**同骨架克隆**） |
| EUR | 28 | 6 | 21% | MARKET d1×3 / SUBIND d4 / CROWDING d8 / SLOW_AND_FAST d1 |
| KOR | 35 | 5 | 14% | REVERSION_AND_MOMENTUM×5（**同族克隆**） |
| GBR | 28 | 4 | 14% | FAST d5×4（**同族克隆**） |
| USA | 49 | 3 | 6% | SUBIND d15 / SUBIND d3 / STAT d2 |
| IND / GLB / ASI | — | 各 1 | 2–10% | — |

### 11.2 二批结果（15 条：12 成功 + 2 条连接中断后重试 + 1 条重试）

| ID | 区 | 族 / d / l / trunc | S | F | TO | prod（实测 11:5x） | 判定 |
|---|---|---|---|---|---|---|---|
| `A1xOakkY` | GBR | SLOW d3 l16 .02 | 5.07 | 5.21 | .1348 | .6621 | **去重命中**，与早批逐位一致 |
| `9qlAlWpd` | GBR | SLOW d3 l16 **.08** | 5.07 | 5.21 | .1348 | 同 A1xOakkY | **truncation no-op 再证**（指标逐位相同） |
| `RRekewMz` | GBR | SLOW d3 **l20** | 4.96 | 5.23 | .1307 | **.6822** | l↑ ⇒ **prod 反而变差**，l14–16 才是双优区 |
| `d5alW1aX` | GBR | **FAST d5** l16 | 4.84 | 4.76 | .1523 | — | 用新 4 颗 FAST 克隆建同族 SA ⇒ 更差 |
| `E5Qr6z3m` | KOR | **R&M d4 l30** | 4.34 | **6.66** | .1292 | **.7400** | 用新 5 颗 R&M 克隆建同族 ⇒ **prod 越红线** |
| `WjlWYEEj` | DEU | **FAST d2 l16** | **3.44** | **3.37** | .1711 | **.8847** | **DEU 区纪录**（现役 3.27/3.09），prod 死 |
| `O0W5A3Zv` | DEU | SUBIND d4 l16 | 3.09 | 3.64 | .0923 | — | F 最高，S 不足 |
| `QP0qovwp` | GLB | STAT d1 **l12** | **6.71** | 3.93 | .2884 | — | **GLB S 新高**（早批 6.56），F 仍短 1.07 |
| `kqaLNvkz` | EUR | SUBIND d1 l10 .02 | 3.29 | 2.95 | .1040 | — | 现役 `Wjl6JJQO` 6.13 **不可复现** |
| `wpoJoZwl` | EUR | SUBIND d1 l10 **.08** | 3.29 | 2.95 | .1040 | — | 与上行**逐位相同** ⇒ trunc 排除 |
| `d5alazZx` | EUR | SLOW d2 l10 .08 | 2.85 | 1.85 | .1024 | — | 现役 `E5Q7RGNR` 6.54 **不可复现** |
| `O0W5Anpv` | EUR | **MARKET d1** l10 | 3.29 | 3.06 | .1022 | — | MARKET 族无效（新占族失败） |

### 11.3 三条硬结论

1. **「新提交区」不等于「成功率高」——关键在于新件是否异质。**
   本轮新件绝大多数是**同骨架克隆**（DEU 9 颗 FAST/SUBIND、KOR 5 颗 R&M、GBR 4 颗 FAST），用**同族**建 SA 等于把组合对齐到克隆簇：
   - DEU FAST SA → prod **.8847**
   - KOR R&M SA → prod **.7400**（连平台 0.7 红线都破）
   - GBR FAST SA → S 4.84（比 SLOW 5.07 低）
   ⇒ **只有跨族/跨中性化取件才能稀释 prod**；同族新件越多，该族 SA 越难交。

2. **`truncation` 在 SA 层彻底无效（第二轮独立证实）。** 同配置 .02 与 .08 产出 `9qlAlWpd` / `A1xOakkY`、`wpoJoZwl` / `kqaLNvkz`，**指标与 TO 逐位相同**。此前"EUR 现役件都是 .08 所以是命中因子"的猜测被排除。

3. **EUR 现役最强件（6.13 / 6.54）已不可复现。** 默认 selection + 同族 + 同 decay + 同 limit（.02 或 .08）本轮只给 3.29 / 2.85。
   ⇒ 要么池已漂移，要么**现役件的 selection 不是默认模板**（记录缺失）。**11-15「EUR 必须用默认 1-prod」这条结论的复现基础不成立**，需按现役件 selection 反查后再判。

### 11.4 本轮排序（合并两批，未提交）

| 序 | ID | 区 | 配方 | S | F | prod | self | 三条件 |
|---|---|---|---|---|---|---|---|---|
| **1** | `A1xOakkY` | GBR | SLOW d3 l16 LC | 5.07 | 5.21 | **.6621** | .6618 | 2/3（prod −0.012） |
| 2 | `YPaW2WKq` | GBR | SLOW d4 l14 LC | 5.08 | 5.26 | .6623 | .6625 | 2/3（同席） |
| 3 | `P05XXeNx` | GBR | SLOW d3 l14 LC | 5.14 | 5.18 | .6629 | .6631 | 2/3（同席） |
| — | `QP0qovwp` | GLB | STAT d1 l12 LC | 6.71 | 3.93 | 未测（F 短 1.07，不入表） | — | 不达标 |
| — | `WjlWYEEj` | DEU | FAST d2 l16 LC | 3.44 | 3.37 | .8847 | — | prod 死 |

**二批未产生任何可交件，第一名不变（`A1xOakkY`，仍未提交）。**

### 11.5 二批工程记录

- W1 两条（GBR l20 / DEU FAST d2）首次派发即 `ConnectionError 10053/10054`（**平台侧瞬断，非并发超限**），重试后 1 成功 1 需三试。
- 结论：`super_build.py select` 的轮询阶段对网络抖动无重试，**长批次建议外层加 `|| retry`**，否则会丢件且不报警（退出码仍为 0 的假成功需看 `[result]` 行）。
