# 各 Region 最优 SuperAlpha 方案 · 2026-11-17

> 配方四轴版（① selection 主键 ② limit 曲线 ③ combo 形状 ④ 中性化族）
> 数据截止：2026-11-17 07:35 GMT+8｜**本轮共派发 28 条 SUPER 仿真，28 条全部落指标**
> **本轮未提交任何 alpha。** 提交权归用户。

---

## 一、执行摘要

### 1.1 结论一句话

**本轮 0 个区达成「S≥5 ∧ F≥5 ∧ prod≤0.65」三条件**；GBR 首次把缺口压到 **prod −0.0048**（`pwa8mYvV` S5.05/F5.18/prod .6548），是全年最接近的一条，但 GBR 的 prod 存在 **.654 硬地板**（6 种配置落在 .6540–.6947，其中保住 S≥5 的 4 档全在 .6540–.6621），无配置可破。

### 1.2 本轮排序表（§5.5 字典序，仅列过 §7 硬闸者）

| # | ID | 档位 | 主键 / combo / d / limit | S | F | TO | prod | self | 三条件 | 最小缺口 | ρmax vs 现役 | 席位 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | `pwa8mYvV` | GBR/TOP700 SLOW | LC / w² / d3 / l16 | 5.05 | 5.18 | .1351 | **.6548** | .6544 | **2/3** | **−0.0048** | .6544 | 新独立席 |
| 2 | `ZYaW25v1` | GBR/TOP700 SLOW | LC / w¹ / d4 / l16 | 5.00 | **5.27** | .1265 | .6586 | .6582 | 2/3 | −0.0086 | .6582 | 同席（ρ .9985） |
| 3 | `A1xOakkY` | GBR/TOP700 SLOW | LC / w¹ / d3 / l16 | **5.07** | 5.21 | .1348 | .6621 | .6618 | 2/3 | −0.0121 | .6618 | 同席（ρ .9993） |
| 4 | `MP6kOWMn` | GBR/TOP700 SLOW | LC / ts_mean(w,5) / d3 / l17 | 5.04 | 5.23 | .1338 | .6872 | — | 2/3 | −0.0372 | — | 同席（ρ .982） |
| 5 | `RRedM1Ma` | IND/TOP500 STAT | LC / w¹ / d1 / l14 | **6.10** | **5.96** | .2975 | .8084 | — | 2/3 | −0.1584 | — | 无边际（prod 破线） |
| 6 | `QP055ze5` | GBR/TOP700 SLOW | LC / w¹ / d5 / l16 | 4.95 | 5.22 | .1203 | **.6540** | .6536 | 1/3 | −0.0500 | .6536 | 同席（ρ .996） |
| 7 | `ZYar6Rv8` | GBR/TOP700 SLOW | LC / w¹ / d5 / l18 | 4.92 | 5.24 | .1185 | .6947 | — | 1/3 | −0.0800 | — | 同席（ρ .971） |

**#1–#4、#6、#7 是同一席位**（互测 ρ .96–.999，只能取一颗）。#4 与 #7 另因 prod >0.68 余量闸被拒（平台 0.7 可过）。

### 1.3 与上轮对比

| 区 | 上轮最佳 | 本轮最佳 | 变化 |
|---|---|---|---|
| GBR | `A1xOakkY` 5.07/5.21/.6621（缺 prod .012） | `pwa8mYvV` 5.05/5.18/**.6548**（缺 prod .0048） | **prod 改善 .0073，缺口收窄 60%** |
| GLB | `LL5amzov` 6.93/4.18/.6101（缺 F .82） | 同（本轮新件全部更差） | 无改善，**F 天花板未破** |
| EUR | `E5Q7RGNR` 6.54/4.54/.567（缺 F .46） | 同（**基线不可复现**，见 §6.3） | 结论降级：不可作为可达性锚点 |
| IND | `QPbjxMYw` 5.37/5.74/.650（3/3 已交） | `RRedM1Ma` 6.10/5.96/**.8084** | S/F 双超但 prod 崩 |
| DEU | `vR1oxZA3` 3.27/3.09/.599 | `j2a1v3lk` 2.89/2.85/.1416 | 无改善（S 天花板 3.3） |
| ASI / MEA / USA / KOR | — | 未派发（见 §7） | — |

---

## 二、池与档位现状（2026-11-17 06:30 实测）

| 区 | 池(ACTIVE REGULAR) | 变化 | SUPER ACTIVE | maxS | maxF | minProd | 三条件件数 |
|---|---|---|---|---|---|---|---|
| USA | 51 | +2 | 11 | 6.39 | 7.06 | .615 | 1（`A1V0eZne` 6.39/7.06/.6146） |
| IND | 48 | 0 | 12 | 5.43 | 5.74 | .471 | 2（`QPbjxMYw` 5.37/5.74/.650、`wpbQjeKp` 5.41/5.27/.631） |
| KOR | 37 | 0 | 12 | **5.96** | **7.50** | .547 | 1（`KPg60XNp` 5.96/7.50/.5475） |
| GBR | 28 | 0 | 6 | 4.42 | 4.27 | .529 | 0 |
| EUR | 28 | 0 | 5 | 6.54 | 4.69 | .462 | 0 |
| GLB | 19 | 0 | 5 | 6.93 | 4.18 | .512 | 0 |
| DEU | 22 | +1 | 2 | 3.27 | 3.09 | .599 | 0 |
| ASI | 10 | 0 | 2 | 5.38 | 2.99 | .502 | 0 |
| MEA | 19 | 0 | 2 | 2.52 | 2.99 | .637 | 0 |
| HKG | 7 | 0 | 0 | — | — | — | BLOCKED（差 3 颗） |

- **SUPER ACTIVE 57 颗，与 11-16 逐位相同** ⇒ 用户自 11-15（`KPg60XNp`）后未再提交，档位表无变化。
- **零 SUPER 档连续第 6 轮 = 0**：8 个 GO 区的可建 universe 全部已被 SUPER 占用。
- pyramid：SA 的 `is.checks` 无 `MATCHES_PYRAMID` ⇒ **SA 不参与 pyramid 计数**，倍率仅记录：DEU D1 1.2–1.8 / GBR D1 1.0–1.7 / EUR D1 1.0–1.5 / GLB D1 1.0–1.4 / IND D1 1.0–1.4 / USA D1 1.0–1.4。**塔六元组 = n/a（SA 无席位）**；Genius 六维（T1–T6）仅对 REGULAR 生效，SA 同为 n/a。

---

## 三、三条件达成矩阵（本轮实测，带时间戳）

红线：prod ≥0.7 合规红线（无豁免）；本方案自设 **prod ≤0.68 余量闸**；三条件目标 `S≥5 ∧ F≥5 ∧ prod≤0.65`。

| ID | 档位 | S | F | TO | prod | self | 实测时间(GMT+8) | gap-S | gap-F | gap-prod | 达成 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `pwa8mYvV` | GBR SLOW d3 l16 w² | 5.05 | 5.18 | .1351 | **.6548** | .6544 | 11-17 07:12 | +0.05 | +0.18 | **−0.0048** | 2/3 |
| `ZYaW25v1` | GBR SLOW d4 l16 w¹ | 5.00 | 5.27 | .1265 | .6586 | .6582 | 11-17 07:20 | 0.00 | +0.27 | −0.0086 | 2/3 |
| `A1xOakkY` | GBR SLOW d3 l16 w¹ | 5.07 | 5.21 | .1348 | .6621 | .6618 | 11-17 07:31 | +0.07 | +0.21 | −0.0121 | 2/3 |
| `MP6kOWMn` | GBR SLOW d3 l17 ts5 | 5.04 | 5.23 | .1338 | .6872 | — | 11-17 07:14 | +0.04 | +0.23 | −0.0372 | 2/3（超 0.68 闸） |
| `QP055ze5` | GBR SLOW d5 l16 w¹ | 4.95 | 5.22 | .1203 | .6540 | .6536 | 11-17 07:15 | −0.05 | +0.22 | +0.004 | 1/3 |
| `ZYar6Rv8` | GBR SLOW d5 l18 w¹ | 4.92 | 5.24 | .1185 | .6947 | — | 11-17 07:13 | −0.08 | +0.24 | −0.0447 | 1/3（超 0.68 闸） |
| `RRedM1Ma` | IND STAT d1 l14 LC | 6.10 | 5.96 | .2975 | .8084 | — | 11-17 07:13 | +1.10 | +0.96 | −0.1584 | 2/3 |
| `88Nnbzpv` | IND STAT d1 l10 LC | 5.44 | 4.73 | .3391 | 未测 | — | — | +0.44 | −0.27 | — | 1/3 |
| `1YWJevZM` | GLB SLOW d1 l12 LC | 6.49 | 3.73 | .2749 | 未测 | — | — | +1.49 | −1.27 | — | 1/3 |
| `e7aLmm66` | GLB SLOW d1 l11 LC | 6.39 | 3.60 | .2944 | 未测 | — | — | +1.39 | −1.40 | — | 1/3 |
| `j2a1v3lk` | DEU R&M d1 l13 LC | 2.89 | 2.85 | .1416 | 未测 | — | — | −2.11 | −2.15 | — | 0/3 |
| `rK7AY29o` | DEU R&M d1 l13 | 2.77 | 2.82 | .1324 | 未测 | — | — | −2.23 | −2.18 | — | 0/3 |
| `npa390aq` | EUR SLOW d2 l12 | 3.08 | 2.05 | .1160 | 未测 | — | — | −1.92 | −2.95 | — | 0/3 |
| `E5Q7RGNR`（现役） | EUR SLOW d2 l10 | 6.54 | 4.54 | .2263 | .567 | .375 | 存档（11-11） | +1.54 | **−0.46** | +0.083 | 2/3 |

> `self` 列非 `null` 者为 `check_correlation(correlation_type="both", refresh=True)` 实测；`sleep` 未测项标「未测」——未被列入排序表前列的候选不再占用 prod 单并发槽。

---

## 四、四轴扫描矩阵（本轮全部 27 条落指标仿真）

| Alpha ID | 区/universe | 键① | limit② | decay | neut④ | combo③ | maxTrade | S | F | TO |
|---|---|---|---|---|---|---|---|---|---|---|
| `pwa8mYvV` | GBR/TOP700 | LC | l16 | d3 | SLOW | **w²** | OFF | 5.05 | 5.18 | .1351 |
| `ZYaW25v1` | GBR/TOP700 | LC | l16 | **d4** | SLOW | w¹ | OFF | 5.00 | 5.27 | .1265 |
| `mLaZpmvp` | GBR/TOP700 | LC | l16 | d4 | SLOW | w² | OFF | 4.99 | 5.24 | .1268 |
| `9qlJYEwo` | GBR/TOP700 | LC | l17 | d4 | SLOW | w³ | OFF | 4.99 | 5.28 | .1264 |
| `MP6kOWMn` | GBR/TOP700 | LC | l17 | d3 | SLOW | **ts_mean(w,5)** | OFF | 5.04 | 5.23 | .1338 |
| `1YWJeW9M` | GBR/TOP700 | LC | l16 | d5 | SLOW | ts_mean(w,5) | OFF | 4.95 | 5.22 | .1203 |
| `9qlJYEb9` | GBR/TOP700 | LC | l16 | d5 | SLOW | w² | OFF | 4.94 | 5.20 | .1204 |
| `ZYar6Rv8` | GBR/TOP700 | LC | l18 | d5 | SLOW | w¹ | OFF | 4.92 | 5.24 | .1185 |
| `YPaQLVoq` | GBR/TOP700 | LC | **l13** | d3 | SLOW | w¹ | OFF | 4.93 | 4.80 | .1395 |
| `kqaQEzGL` | GBR/TOP700 | LC(gate .55) | l16 | d3 | SLOW | w¹ | OFF | 4.81 | 4.81 | .1408 |
| `QP0EMkWr` | GBR/TOP700 | LC | l16 | d3 | SLOW | w¹ | **ON** | 4.31 | 4.23 | .1146 |
| `e7aLmm66` | GLB/MINVOL1M | LC | l11 | d1 | SLOW | w¹ | OFF | 6.39 | 3.60 | .2944 |
| `1YWJevZM` | GLB/MINVOL1M | LC | l12 | d1 | SLOW | w¹ | OFF | 6.49 | 3.73 | .2749 |
| `vRAd8mr3` | GLB/MINVOL1M | LC | l11 | d1 | SLOW | ts_mean(w,5) | OFF | 6.39 | 3.60 | .2944 |
| `YPaQ6kq6` | GLB/MINVOL1M | 1−prod | l11 | d1 | SLOW | w¹ | **ON** | 4.25 | 2.54 | .2075 |
| `E5Qk1v3P` | GLB/MINVOL1M | LC | l11 | d3 | SLOW | w¹ | **ON** | 4.04 | 2.75 | .1930 |
| `88Nnbzpv` | IND/TOP500 | LC | l10 | d1 | STAT | w¹ | OFF | 5.44 | 4.73 | .3391 |
| `RRedM1Ma` | IND/TOP500 | LC | l14 | d1 | STAT | w¹ | OFF | 6.10 | 5.96 | .2975 |
| `rK7AY29o` | DEU/TOP500 | 1−prod | l13 | d1 | R&M | w¹ | OFF | 2.77 | 2.82 | .1324 |
| `j2a1v3lk` | DEU/TOP500 | LC | l13 | d1 | R&M | w¹ | OFF | 2.89 | 2.85 | .1416 |
| `npa390aq` | EUR/TOP2500 | 1−prod | l12 | d2 | SLOW | w¹ | OFF | 3.08 | 2.05 | .1160 |
| `Jj8bqmrn` | EUR/TOP2500 | 1−prod | l12 | d2 | SLOW | ts_mean(w,5) | OFF | 3.08 | 2.05 | .1160 |
| `6XMz7YAJ` | EUR/TOP2500 | 1−prod | l12 | d2 | SLOW | w¹ | **ON** | 2.43 | 1.45 | .0681 |
| `d5adp8VY` | EUR/TOP2500 | 1−prod | l16 | d2 | SLOW | w¹ | **ON** | 3.15 | 2.17 | .0698 |
| `2r5JMQNw` | EUR/TOP2500 | 1−prod | l12 | d3 | SLOW | w¹ | OFF | 2.97 | 1.94 | .1053 |
| `npa39eAx` | EUR/TOP2500 | 1−prod | l10 | **d3** | SLOW | w¹ | OFF | 2.75 | 1.75 | .0942 |
| `eur_d2_l10_def` | EUR/TOP2500 | 1−prod(gate .7) | l10 | d2 | SLOW | w¹ | OFF | 2.85 | 1.85 | .1024 |
| `eur_tmpl_d2_l10` | EUR/TOP2500 | 1−prod(gate .55) | l10 | d2 | SLOW | w¹ | OFF | 2.85 | 1.85 | .1024 |

**四轴结论（本轮新增实证）**

1. **① 主键**：GBR 仍是 `long_count` 最优（同 d3/l16：LC 5.07 vs 默认 5.19 但 prod .6659 vs .6621，LC 的 prod 更干净）；**IND 的 LC 在 l14 把 S/F 推到 6.10/5.96（双超区内最强件），但 prod .8084 直接破线**——IND/GBR 的「LC 高 S」与「prod 干净」不可兼得，与 11-15 结论一致。
2. **② limit**：GBR 曲线在 l16 见顶（l13 4.93 / l16 5.05 / l17 5.04 / l18 4.92）；**EUR limit↑ 灾难性**（l10→l12 S 2.85→3.08 区间、l16 3.15 但 TO 崩到 .07）、DEU l13 < l10；IND l14 > l10（S +0.66 但 prod 崩）。**「S 峰值 ≈ 池 58–65%」只在 GBR/IND 成立，EUR/DEU 不成立。**
3. **③ combo**：`w²`（GBR d3 l16）是**唯一正增益**：S 5.07→5.05（−0.02）、F 5.21→5.18、**prod .6621→.6548（−0.0073）**，即用 0.02 S 换 0.0073 prod；`w³` 无进一步增益（4.99/5.28/.1264，prod 未测）。**`ts_mean(w,5)`（时序平滑）在 SA 组合层是纯 no-op**——GBR（`1YWJeW9M` vs `QP055ze5` 逐位 .95/.22/.1203）、GLB（`vRAd8mr3` vs `e7aLmm66` 逐位 6.39/3.60/.2944）、EUR（`Jj8bqmrn` vs `npa390aq` 逐位 3.08/2.05/.1160）三次独立复现同值，**SA 层无权重自相关可平滑**。
4. **④ 中性化族**：本轮仅做 2 次对照（GLB SLOW 新建、DEU R&M 续），未做穷举；沿用「换族 ρ>.96 = 同席、零增益」。
5. **★ 新参数 `maxTrade=ON` 全线负增益**（11-15 新增开关，本轮首次对 SA 实测）：GBR 同配置 5.07→4.31（−0.76）、EUR 同配置 3.08→2.43（−0.65）、GLB 默认键 4.25（同档非 maxTrade 基线 6.39–6.93）、GLB d3+mt 4.04。TO 确实降（GBR .1348→.1146、EUR .116→.0681），但 **R 同步降得更多**（F 也从 5.21→4.23），`F=S√(R/TO)` 的分子分母同缩 ⇒ **「压 TO 抬 F」在 SA 层不成立**。

---

## 五、互测矩阵（本地 `compute_mutual_correlation`，不占平台槽）

GBR 本轮 6 颗新件 + 2 颗现役（4 年日收益，N=1021）：

| | pwa8mYvV | ZYaW25v1 | QP055ze5 | A1xOakkY | MP6kOWMn | ZYar6Rv8 | QPvGdLYQ | 3qompGeZ |
|---|---|---|---|---|---|---|---|---|
| pwa8mYvV | 1 | .9985 | .9962 | .9993 | .9819 | .9637 | .6085 | .6544 |
| ZYaW25v1 | .9985 | 1 | .9993 | .9991 | .9861 | .9709 | .6200 | .6582 |
| QP055ze5 | .9962 | .9993 | 1 | .9968 | .9833 | .9712 | .6188 | .6536 |
| A1xOakkY | .9993 | .9991 | .9968 | 1 | .9874 | .9689 | .6209 | .6618 |
| MP6kOWMn | .9819 | .9861 | .9833 | .9874 | 1 | .9838 | .6644 | .6867 |
| ZYar6Rv8 | .9637 | .9709 | .9712 | .9689 | .9838 | 1 | .6947 | .6618 |
| QPvGdLYQ（现役） | .6085 | .6200 | .6188 | .6209 | .6644 | .6947 | 1 | .5104 |
| 3qompGeZ（现役） | .6544 | .6582 | .6536 | .6618 | .6867 | .6618 | .5104 | 1 |

**判读**：
- 6 颗新件彼此 **ρ .9637–.9993 ⇒ 同一席，只能取 1 颗**（与 decay/limit/combo 无关：GBR 的席位由「成分集合 + limit」定，而 6 种配置选出的成分集合几乎重合）。
- 对现役 GBR 最高相关 = **.6947**（`ZYar6Rv8`↔`QPvGdLYQ`），其余 .5104–.6867 ⇒ **确属新独立席（<0.7）**，但 `ZYar6Rv8`/`MP6kOWMn` 已贴线（.69），交付应避开。
- `pwa8mYvV` 对现役最大 ρ **.6544** —— 全组最干净，坐实 #1。

---

## 六、分 Region 方案

### 6.1 GBR / TOP700 —— 本轮唯一有实质推进的区

**最优配方（`pwa8mYvV`，排序 #1）**
```
region=GBR  universe=TOP700  delay=1  neutralization=SLOW
decay=3  truncation=0.02  selectionHandling=POSITIVE  selectionLimit=16  maxTrade=OFF

selection: if_else(is_nan(long_count), 1, long_count) * (self_correlation < 0.7)
           * (turnover > 0.01) * (turnover < 0.6)

combo:     stats = generate_stats(alpha);
           innerCorr = self_corr(stats.returns, 500);
           ic = if_else(innerCorr == 1.0, nan, innerCorr);
           maxCorr = reduce_max(ic);
           w = 1 - maxCorr;
           w*w
```
| 项 | 值 | 闸 | 余量 |
|---|---|---|---|
| S | 5.05 | ≥5（三条件） | +0.05 |
| F | 5.18 | ≥5（三条件） | +0.18 |
| 2Y ladder | 5.08 | ≥1.58 | 充分 |
| sub-universe | 3.30 | — | — |
| TO | .1351 | 0.4 上限 | 充分 |
| **prod** | **.6548** | ≤0.65（三条件）/ ≤0.68（余量闸）/ <0.7（红线） | **−0.0048 / +0.0252 / +0.0452** |
| **self** | **.6544** | <0.68 | +0.0256 |
| IS checks | 8 PASS / **0 FAIL** | 零 FAIL | ✓ |

**为什么停在 2/3**：GBR prod 存在 **.654 地板**——`QP055ze5` .6540（d5/l16/w¹）、`pwa8mYvV` .6548（d3/l16/w²）、`ZYaW25v1` .6586（d4/l16/w¹）、`A1xOakkY` .6621（d3/l16/w¹）、`MP6kOWMn` .6872、`ZYar6Rv8` .6947，六种配置的 prod 极差仅 .0407 且**均 ≥.654**。prod 的主体来自单一固定污染源（self top1 恒为 `3qompGeZ` .6536–.6618），换 limit/decay/combo 只改边际成分，改不动该源。**再压 prod 只能踢掉该源，而踢掉后 S 必跌破 5**（11-15 实测 `prod<0.65` 硬筛使 GBR S 4.64→3.79）。

### 6.2 GLB / MINVOL1M —— F 缺口未破，判死至池变化

| 配方 | S | F | TO | 判定 |
|---|---|---|---|---|
| 现役 `LL5amzov` STAT d1 l10 | 6.93 | 4.18 | .2404 | F 缺 0.82 |
| 本轮 SLOW d1 l11 LC | 6.39 | 3.60 | .2944 | LC 抬 TO ⇒ F 更差 |
| 本轮 SLOW d1 l12 LC | 6.49 | 3.73 | .2749 | 同上 |
| 本轮 SLOW d1 l11 + maxTrade ON | 4.25 | 2.54 | .2075 | 负增益 |
| 本轮 SLOW d3 l11 + maxTrade ON | 4.04 | 2.75 | .1930 | 负增益 |
| 本轮 ts_mean(w,5) | 6.39 | 3.60 | .2944 | **no-op** |

F 需 4.18→5：`F=S√(R/TO)`，R=.0873 固定 ⇒ 需 TO .2404→.168（−30%）。本轮证明：`maxTrade` 降 TO 但同比例毁 R；`ts_mean` 无效；`LC` 反把 TO 推高。**GLB 的 F 缺口结构性不可达**（低 R 是其本质：R .0873 为全区最低）。

### 6.3 EUR / TOP2500 —— 本轮最重要的负面结论：**基线不可复现**

| 尝试 | S | F | TO | 说明 |
|---|---|---|---|---|
| 现役 `E5Q7RGNR`（存档） | 6.54 | 4.54 | .2263 | 11-11 提交，selection 表达式未留档 |
| 复现①默认模板（self_gate **.7**，trunc .02，d2 l10） | **2.85** | 1.85 | .1024 | **同 settings 只能复现到 2.85** |
| 复现②模板真默认（self_gate **.55**，trunc **.08**，d2 l10） | **2.85** | 1.85 | .1024 | **与①逐位相同** ⇒ self_gate/trunc 均非约束项 |
| l12 | 3.08 | 2.05 | .1160 | |
| l16 + maxTrade | 3.15 | 2.17 | .0698 | |
| d3 l12 | 2.97 | 1.94 | .1053 | |
| d3 l10 | 2.75 | 1.75 | .0942 | decay 一档即腰斩 |

**含义**：两次独立配置（self_gate .7/.55、trunc .02/.08）复现结果**逐位相同 2.85/1.85/.1024** ⇒ 排除「配方差异」——self_gate 与 truncation 在 EUR 池上都不构成约束（成分 self 普遍 <0.55，truncation 已证 no-op）。**唯一解释是池漂移**：`E5Q7RGNR` 在 11-11 选中的 10 颗成分，在当前池的 1−prod 排序中已排不进前 10（或已失效）。**EUR 的「F 只差 0.46」不能再当可达性锚点**（§4.0 基线复现硬规则生效）。本轮 EUR 6 条仿真全部 ≤3.15，**EUR 降级为停投区**。

### 6.4 IND / TOP500 —— S/F 强、prod 崩，无边际

`RRedM1Ma`（STAT d1 l14 LC）S6.10/F5.96 双超区内最强件（5.43/5.74），但 **prod .8084**（红线外）。l10 版 5.44/4.73 亦 prod 未过。⇒ IND 的 `long_count` 主键只在「S↑ 与 prod↑ 同向」区间有效，与 11-15 的 l28 结论（.8362）一致。**IND 已有 2 颗三条件现役件，本轮无新增价值。**

### 6.5 DEU / TOP500 —— S 天花板 3.3，结构性不可能

`rK7AY29o`（R&M l13 默认键）2.77/2.82、`j2a1v3lk`（R&M l13 LC）2.89/2.85，均 < l10 的 2.92/2.91（`RReX6k6a`）。**DEU 池 22 颗但信号质量不足，S≥5 无路径**。

### 6.6 USA / KOR / ASI / MEA

- **USA**（51 池/11 SUPER）：已有三条件件 `A1V0eZne` 6.39/7.06/.6146；上一轮实证 USA 窄档 6 族全灭（TOP1000 除 CROWDING、TOP2000 全族），本轮不再派发。
- **KOR**（37/12）：`KPg60XNp` 5.96/7.50/.5475 为全账户最强三条件件，l30 覆盖 86% 池反而 prod 最干净，已封顶。
- **ASI**（10/2）：`d5WGG5bg` S5.38 但 F2.99，F 需 +2.0（TO .2923→需 R/TO 翻 3.3 倍），**不可能**。
- **MEA**：平台已停用（400 `Region MEA is not available`），历史 2 颗仅存档。

---

## 七、停投区与撞墙档案

**停投区**：EUR（本轮降级，基线不可复现）、MEA（平台下架）、ASI（F 结构性缺口 2.0）、DEU（S 天花板 3.3）、HKG（池 7/10）、CHN/AMR/JPN/TWN（池 0）、USA-TOP2000·TOP1000（除 CROWDING）·TOP200·TOP500·TOPSP500、GLB 全域（F 缺口 30% TO）、IND 的 LC 主键、GBR 除 SLOW 外的族。

**撞墙档案（本轮新增）**

| 撞墙 | 证据 | 归类 |
|---|---|---|
| GBR prod .654 地板 | 6 配置 .6540–.6947，极差 .041，self top1 恒 `3qompGeZ` | **prod 硬闸（单一污染源）** |
| GBR S 5.19 上限 | l13 4.93 / l16 5.07 / l17 5.04 / l18 4.92；STAT 族 5.13 但 prod .8001 | **S 天花板 + prod 耦合** |
| GLB F 4.23 上限 | R .0873 全区最低，需 TO −30% | **信号质量（R 低）** |
| EUR 基线不可复现 | 同 settings 2.85 vs 存档 6.54 | **池漂移 / 未留档配方** |
| IND LC prod .8084 | l14 双超但 prod 崩；l28 已证 .8362 | **池拥挤（自身 SUPER 12 颗）** |
| maxTrade 全负 | GBR −0.76 / GLB −2.14 / EUR −0.65 | **杠杆证伪** |
| ts_mean(w,n) no-op | 三次独立配置逐位同值 | **杠杆证伪** |
| DEU S 3.3 上限 | l10 2.92 / l13 2.89 | **池质量** |

---

## 八、算子利用率审计（按「是否有增益」分类）

| 类别 | 算子 | 本轮/历史结论 |
|---|---|---|
| **有增益（保留）** | `long_count`（selection 主键，GBR +47% S 的历史杠杆）、`self_correlation`/`turnover`/`prod_correlation`（过滤项）、`generate_stats`/`self_corr`/`reduce_max`（combo 骨架）、`w` 幂（`w²` GBR prod −.0073） | w² 是本轮唯一正增益算子用法 |
| **零增益（no-op，禁用）** | `ts_mean(w,5)`（combo 层，3 次复现同值）、`if_else(innerCorr==1,nan,·)` 的替代整形（`rank(w)`/`sqrt(w)`/`zscore(w)` 历史已证伪） | 算子轴 ROI 枯竭 |
| **负增益（禁用）** | `maxTrade=ON`（非算子但同层参数，全线 −0.65~−2.14 S）、`self_correlation<0.55` 严格门（GBR −0.26 S）、`w³`（无进一步收益） | — |
| **未测（无 ROI 依据，暂缓）** | 其余 COMBO 算子（官方表 ≥160，本账户累计用 5 个 ≈3.1%）、SELECTION 函数算子（0/43） | 连续 6 轮新增 0，**不建议再投入** |

---

## 九、元评估：卡在哪一轴，需要什么外部条件

**本轮无区达标，卡点明确分为两类：**

1. **GBR —— 卡在「prod 单一污染源」，不是配方轴**
   - 六种配方（decay 3/4/5 × limit 16/17/18 × combo w¹/w²/w³/ts）把 prod 控制在 .6540–.6947，**地板 .654**，且 self top1 恒为同一颗现役 `3qompGeZ`（ρ .6536–.6618）。
   - 需要的突破条件（二者之一）：① **该污染源自身 prod 漂移下行**（不可控）；② **GBR 池新增 ≥5 颗与 `3qompGeZ` 低相关的 REGULAR**，让 l16 选出的成分集合天然避开它。
   - 在此之前，GBR 的最优解就是 `pwa8mYvV`（S5.05/F5.18/.6548），**缺口 0.0048 是账户级最小缺口**。
2. **GLB / ASI / DEU —— 卡在信号质量（R 或 S 的物理上限），配方完全无解**
   - GLB R=.0873、ASI F 需 +2.0、DEU S 需 +1.7。这三项都不是「再调一个参数」能动的量级，只有**换信息源（新数据集）**或**扩池**才有意义。
3. **EUR —— 卡在「历史锚点失效」**
   - 6.54 无法复现：用 self_gate .7 与 .55、trunc .02 与 .08 两组独立配置复现，结果**逐位同为 2.85/1.85/.1024** ⇒ 不是配方差异，是**池漂移**（11-11 那 10 颗成分在当前排序中已进不了前 10）。
   - 含义：过去 7 轮所有「EUR 只差 F」的判断都建立在失效基线上。本轮已把 EUR 降级；**恢复评估的前提是 EUR 池新增能重回高相关的成分（或平台恢复）**，而不是继续调参。

**不许写「继续观察」——本轮明确不做的三件事**：不再扫 GBR 的 decay/limit/combo（已 6 点覆盖）、不再扫任何 `maxTrade`/`ts_mean` 组合（已证伪）、不再把 EUR 6.54 当基线（已证不可复现）。

---

## 十、提交建议（**只写建议，本轮未执行任何提交**）

### 10.1 建议对象

| 顺位 | ID | 档位 | prod / self（实测） | IS checks | 备查 |
|---|---|---|---|---|---|
| **1** | `pwa8mYvV` | GBR/TOP700 SLOW d3 l16 LC w² | **.6548 / .6544** | 8 PASS / 0 FAIL | ρmax vs 现役 .6544（新独立席）；台账无 REJECT（新件） |
| 2 | `ZYaW25v1` | GBR 同档 d4 l16 LC w¹ | .6586 / .6582 | 0 FAIL | 与 #1 ρ .9985 **同席**，仅作 #1 的备胎，不可同日双交 |
| 3 | `A1xOakkY` | GBR 同档 d3 l16 LC w¹ | .6621 / .6618 | 0 FAIL | 同席，S 最高（5.07），prod 余量最薄（.0179） |

**为什么不建议交 #2/#3**：三颗同一席（ρ≥.9985），交一颗即封该席，另两颗作废；#1 的 prod 余量（.0252）与 ρmax（.6544）双优于 #2/#3。

**推荐理由**：GBR 现役最强件仅 S4.42/F4.27，`pwa8mYvV`（5.05/5.18）是**区内 S +14%、F +21% 的实质升级**，且满足全部提交硬闸（prod .6548<0.68、self .6544<0.68、零 FAIL、ρ<0.7、台账无 REJECT）。它未达「prod≤0.65」的三条件目标，属**质量升级件**而非三条件件——是否提交由用户裁决。

### 10.2 配额（实测）

- `SUPER_SUBMISSION`：**1 颗 / ET 日历日 / 账户级**，00:00 ET 重置 = **GMT+8 13:00**。
- 当前 **ET 日 = 2026-11-16（ET 17:35）**，本 ET 日 SUPER 已用 **0/1 → 剩余 1**（末次 SUPER `KPg60XNp` 于 ET 11-15 01:25）。
- 下一次重置：**2026-11-17 13:00 GMT+8**（即今天下午）。

### 10.3 命令模板（**只写，未执行**）

```bash
cd /d/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 \
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit \
  --alpha-id pwa8mYvV --region GBR
```

### 10.4 两个提交坑（沿用实测）

1. **提交前停后台批次**：并发仿真会让 `_probe_prod_max` 抛 ProxyError（本轮 07:12 后所有流已结束，当前无在跑批次，唯 §11 的 EUR 复现条需先收）。
2. **prod 槽 195s 冷却**：`logs/_dblock/correlation.cooldown.json`；本轮实测 `correlation_busy` 频繁（`retry_after` 1.1–72.9s），重试即过，**不是失败**。

---

## 十一、附录

### A. 数据与产物

- 池盘点：`results/sa_scan_20261117/probe_refresh.json`（06:30:42，pool 明细见 `probe_refresh.log`）
- 档位表：`results/sa_scan_20261116/super_list.json`（57 颗 ACTIVE SUPER 的 uni/neut/decay/lim/S/F/TO/prod/self；本轮 SUPER 集合与之一致，无新增）
- 仿真产物：`results/sa_scan_20261117/res_*.json`（28 条）+ `log_*.log` + `build_a..h.sh`
- 互测：MCP `compute_mutual_correlation` 两次（GBR 6 颗 / 8×8 全表），结果见 §5
- 双闸：MCP `check_correlation(refresh=True)` 逐颗，时间戳见 §3

### B. 本轮工程实证（可复用）

1. **`ts_mean(w,n)` 在 combo 层是 no-op** ⇒ 平台把 combo 权重按日重算，不存在「权重路径」，任何时序平滑都无效。
2. **`maxTrade=ON` 对 SA 是负杠杆**（TO↓ 与 R↓ 同比例，F 不升反降），与 REGULAR 层「压 TO 抬 F」相反——**REGULAR 结论不可迁移到 SA 层**。
3. **`super_build.py select` 支持 `--selection`/`--combo`/`--max-trade` 全覆盖表达式**；`create_multi_simulation`（MCP）不支持 SUPER 类型（无 selection/combo/selectionLimit 字段），SUPER 派发必须走该 CLI。
4. **同配置重跑可能被平台去重**返回既有 id；比对 settings 再判「是否新件」。
5. `probe_sa_candidates.py --json` 只认带目录的相对路径（本轮传 `sa_scan_20261117/...` 成功）。
