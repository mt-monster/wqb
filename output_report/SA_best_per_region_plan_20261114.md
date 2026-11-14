# 各 Region 最优 SuperAlpha 方案 · 2026-11-14（Run 19）

> 定时任务产出：**只挖不提交**。本轮未调用 `super_build.py submit`、未 POST `/alphas/{id}/submit`、未开 `WQB_ALLOW_ALPHA_SUBMIT=1`。提交权归用户点名。
> 数据源：`results/sa_scan_20261114/`（probe_refresh.log / super_list.json / mu_bar.json / rank_table.json / res_*.json / log_*.log）
> 双闸实测时刻：ET 2026-11-13 17:3x–17:5x（`refresh=True`，全部本轮重测，无沿用台账值）

---

## 一、执行摘要

**本轮排序第一 = `RReX6k6a`（DEU/TOP500 · REVERSION_AND_MOMENTUM · d1 · l10）**
S 2.92 / F 2.91 / TO 0.1381｜prod **0.5514** / self **0.5516**｜13 项 IS checks **0 FAIL**｜B 档双达标（TO<0.30 ∧ prod<0.60）｜prod 余量 **0.1486**（全轮最厚）

**质量口径第一 = `Wjl6JJQO`（EUR/TOP2500 · SUBINDUSTRY · d1 · l10）**
S 6.13 / F 4.69 / TO 0.2691｜prod **0.6413** / self **0.6173**｜Eff **6.32**（全轮最高）｜prod 余量仅 **0.0387**

两口径本轮仍分叉（与 11-13 同型），文档并列，未擅自合并。**建议主选 `RReX6k6a`**（B 档 + 余量最厚 + 新族 + DEU 塔倍率最高档），`Wjl6JJQO` 列为追求 S/F 上限的备选（承担 prod 漂移风险）。

**本轮产能来源**：10 档新建（4 个从未试过的族 × 3 个区域 + 3 条深化轴），新增 **4 颗过 0.68 余量闸**（`RReX6k6a` / `Wjlke2Xx` / `wpo6bEJ5` / `xAvMbRll`）+ 存量 5 颗重测全过；**2 颗撞 prod 红线**（`oma2WvGE` .7658 / `78YO6J31` .7636）；1 颗撞 sub-universe（`kqaRg6bO`）。

**★ 本轮最大发现**：`REVERSION_AND_MOMENTUM` 是 DEU/TOP500 的**最干净族**（prod .5514，比已提交的 FAST .5987 与 STAT 都低），且 S/F 双高。这推翻「DEU 族谱 S 与 prod 同向、F 最高者最不可交」的旧结论——R&M 同时拿到 F 2.91 与 prod 0.55。

---

## 二、数据基线

### 2.1 组件池 eligibility（`probe_sa_candidates --refresh`，2026-11-14 06:31）

| 区域 | ACTIVE 已提交 REGULAR | 变化 | IS 未提交存量 | verdict |
|---|---|---|---|---|
| USA | 47 | — | 0 | GO |
| IND | 47 | — | 0 | GO |
| KOR | 35 | — | 0 | GO |
| GBR | 28 | — | 704 | GO |
| EUR | 28 | **+1** | 84 | GO |
| MEA | 19 | — | 0 | GO（平台已下架）|
| GLB | 19 | — | 0 | GO |
| DEU | 19 | **+1** | 162 | GO |
| ASI | 10 | — | 0 | GO |
| HKG | 7 | — | 0 | **BLOCKED（差 3 颗）** |

- 池按 **(region, delay)** 计；universe 不切池（USA/TOP1000 仅 1 颗同 universe 组件仍可 l10 建成，已第 3 次复现）。
- IS 存量 950 颗（GBR 704 + DEU 162 + EUR 84）**不计入** SA 组件——必须先提交成 ACTIVE 才有产能。

### 2.2 档位占用表（ACTIVE SUPER = 55 颗，18 档）

| 区域 | universe | SUPER | 已占族（neut/decay/ID） | 档内余量 |
|---|---|---|---|---|
| **DEU** | TOP500 | **2** | FAST d1 `vR1oxZA3`(11-07)、STAT d1 `mLYLEm99`(10-18) | **3 族位空**（R&M/SLOW/CROWD/MARKET/SECTOR/INDUSTRY/SUBIND）|
| **EUR** | TOP2500 | **3** | CROWDING d1 `kqJOQgnk`、SLOW d2 `E5Q7RGNR`、STAT d1 `GrgGkV1o` | 2 族位空 |
| **USA** | TOP1000 | **1** | STAT d1 `LL5aX6Y2` | 5 族位空（但 S 天花板低）|
| **USA** | TOP2000 | **2** | SLOW d1 `e75avmq6`(11-12)、STAT d1 `vROw5Rkd` | 3 族位空，prod 已贴墙 |
| USA | TOP3000 | 6 | FAST/MARKET/SLOW×2/STAT/SUBIND | ≥5，换族不再分散 |
| USA | TOP500 | 1 | CROWDING d1 `E567rQvR` | 已封档（同席全灭）|
| USA | TOPSP500 | 1 | STAT d1 `2rj3ddl5`(l38) | 已封档 |
| IND | TOP500 | 12 | 9 族全占 | ≥5，饱和 |
| KOR | TOP600 | 11 | 7 族全占 | ≥5，饱和 |
| GBR | TOP700 | 6 | 5 族 + STAT×3 | ≥5，饱和 |
| GLB | MINVOL1M | 2 | STAT d1、SUBIND d10 | prod 墙（历史 FAST .7486）|
| GLB | MINVOL10M | 1 | SLOW d1 `LLMVPag1` | 同席全灭 |
| GLB | TOP3000 | 1 | R&M d1 | 停投 |
| GLB | TOPDIV3000 | 1 | STAT d1 | 停投（SLOW 建单必失败）|
| ASI | MINVOL1M | 1 | STAT d2 `d5WGG5bg` | 区域 prod 下界 0.51 被 `QPv88bJW` 顶高 |
| ASI | MINVOL10M | 1 | COUNTRY d3 `QPv88bJW` | 同上 |
| EUR | TOPCS1600 | 1 | STAT d1 | 同席全灭 |
| MEA | TOP400 | 2 | SUBIND d5 / d8 | **区域已下架，不可新建** |

**零 SUPER 档且池达标：无。**（ASI/TOP500 已 11-12 判死：S1.61/F0.62；USA/TOP200 历史判死；HKG 池 7/10；CHN/AMR 池 0）

### 2.3 Pyramid 倍率（D1，`get_pyramid_multipliers`）

| 区域 | D1 最高档 | 最高倍率 | 次高档 |
|---|---|---|---|
| **DEU** | model / news / other / analyst / fundamental / sentiment | **1.8** | pv 1.6、institutions 1.6、insiders 1.6 |
| GBR | sentiment | 1.7 | news / other / analyst 1.6 |
| KOR | analyst / fundamental / model / news / other / sentiment | 1.6 | — |
| ASI | analyst | 1.5 | other / sentiment 1.4 |
| EUR | other | 1.5 | news / sentiment 1.4 |
| USA | other / sentiment | 1.4 | model / analyst / earnings 1.3 |
| GLB | fundamental / analyst | 1.4 | news / model 1.3 |
| IND | analyst | 1.4 | news / other 1.3 |

- **塔计数按季度重置**，本轮未复核当季 lit 状态（`get_pyramid_alphas` 只返当季 ACTIVE；SA 线不改变塔计数）。
- **★★ SA 的 `is.checks` 无 `MATCHES_PYRAMID`** ⇒ **SA 不参与 pyramid 计数**，塔归属/点亮规则对 SA 不适用。倍率仅按数据集类别影响 Base Payment 的 Quality Factor（木桶短板：混 ≥3 类别计 0 塔）。

---

## 三、选点原则

1. **席位类型 > 同族/异族 > 边际指标 > 绝对指标**
2. 零 SUPER 档 = 正边际（本轮无）；已占档只交**异族**（同族预期 self>0.9，直接跳过）
3. 席位互斥优先于单颗优劣：`compute_mutual_correlation` 先砍同席件，再比指标
4. **prod 余量闸 0.68**（平台红线 0.7 − 0.02 余量），不放宽
5. **B 档双达标**（TO<0.30 ∧ prod<0.60）在字典序中优先于 S 高低
6. 台账 REJECT 优先于一切指标（本轮候选均无 `robustness_<id>` 记录）
7. 边际指标只在跨区可比；区内 U/ρ_eff/N_eff 严格单调于 S，无独立信息

---

## 四、论坛指标标准（§0 固化，2026-10-22 定稿，本轮未重复调研）

来源：《Super Alpha 从入门到入门》78赞/39评论、《2024 super alpha 比赛心得》22赞/15评论、《Super Alpha 参数设置》12赞（LY43440 实测）。

### 4.1 组成数量
- 平台硬下限 **10**（<10 报 400 `Ensure this value is greater than or equal to 10`）
- 论坛建议 **30–100 起测、≤500**；**实际生效 = min(limit, 池)**，池是 region 级 ⇒ SA 指标天花板由区域 ACTIVE REGULAR 数决定
- 本工作区实证：**l10 是最优甜点**（EUR l10 self0.33 → l12 0.29/prod0.61 → l30 0.28；KOR l14 self 0.935；USA TOP500 l12 直接 Ladder FAIL）

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.70 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.60** |
| C 比赛/优秀档 | 5.6–7.0 | 5.6–8.9 | 0.20–0.27 | <0.5 |

本轮对照：C 档仅 `Wjl6JJQO`（S6.13）接近；B 档双达标 5 颗（全部 DEU/TOP500）。

### 4.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ 加严后组件 <10 直接 `sim ERROR: At least 10 component alphas are required` ⇒ 小池区（EUR/GLB/DEU/ASI）只能用宽松 selection `(1 - prod_correlation)`。**⚠ `author_*` 是作者级聚合量，自有池内恒常数，论坛阈值不可消费。**

### 4.4 中性化族规律
- 族排序随区而异、**不可跨区照搬**（IND CROWDING≈RAM>SLOW/FAST；GBR/KOR 实测 SLOW 跑赢 CROWDING）
- **本轮新证**：DEU/TOP500 的 `REVERSION_AND_MOMENTUM` prod 0.5514 < SLOW_AND_FAST 0.5720 < SLOW 0.5951 < CROWDING 0.6434 < SUBIND 0.7400 ≈ MARKET ≈ SECTOR
- **decay 深化代价**：`kqaRg6bO`（EUR SUBIND d2）从 d1 的 S6.13/F4.69 掉到 S3.21/F2.85 且 `LOW_SUB_UNIVERSE_SHARPE` FAIL ⇒ **EUR 的 SUBIND 只能 d1**
- 其余不变项：truncation 0.02 vs 0.08 几乎无差异；`selectionHandling=POSITIVE` 历史全成功；`combo_power` 在 limit==池 时是 no-op

---

## 五、★ 边际收益排序（§0.6 五量，逐颗 `refresh=True` 实测）

### 5.1 口径
- `μ̄` = 该区 ACTIVE 已提交 REGULAR 的 IS Sharpe 均值（本轮重算：DEU **1.8263**(n=19)｜EUR **2.0764**(n=28)｜USA **1.9757**(n=47)）
- `N = min(selectionLimit, 池) = 10`
- `U = S/(μ̄√N)`｜`N_eff = (S/μ̄)²`｜`ρ_eff = (N·μ̄²/S² − 1)/(N−1)`｜`Eff = (S−μ̄)/max(prod,self)`｜`ΔCAP% = √(52/(1+51ρ))/√(51/(1+50ρ)) − 1`（ρ=max(prod,self)）
- `ρ_eff > 1` 表示 S<μ̄（组合劣于组件均值），非竞争件

### 5.2 排序表（字典序：① 全 PASS → ② 席位/族 → ③ B 档 → ④ prod 余量 → ⑤ U → ⑥ Eff）

| # | ID | Region/univ | 族·decay | S | F | TO | prod | self | U | N_eff | ρ_eff | Eff | ΔCAP% | B 档 | 席位类型 | 同/异族 | 双闸时刻 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **`RReX6k6a`** | DEU/TOP500 | **R&M d1** | **2.92** | **2.91** | 0.1381 | **0.5514** | 0.5516 | 0.5056 | 2.56 | +0.3235 | 1.98 | 0.038 | ✅ | 档内第 3 族（2 现有） | 异族 | ET 11-13 17:4x | **✅ 可交** |
| 2 | `Wjlke2Xx` | DEU/TOP500 | R&M d2 | 2.89 | 3.01 | 0.1251 | 0.5514 | 0.5516 | 0.5004 | 2.50 | +0.3326 | 1.93 | 0.036 | ✅ | 同上 | **同族（d1/d2）** | ET 11-13 17:5x | ✅ 可交但与 #1 同席 |
| 3 | `wpo6bEJ5` | DEU/TOP500 | SLOW_AND_FAST d1 | 2.81 | 2.14 | 0.1909 | 0.5720 | 0.5723 | 0.4866 | 2.37 | +0.3582 | 1.72 | 0.033 | ✅ | 同上 | 异族 | ET 11-13 17:5x | ✅ 可交，与 #1 ρ .7392 |
| 4 | `leaq3P9l` | DEU/TOP500 | SLOW d1 | 2.60 | 2.11 | 0.1608 | 0.5951 | 0.5954 | 0.4502 | 2.03 | +0.4371 | 1.30 | 0.024 | ✅ | 同上 | 异族 | ET 11-13 17:3x | ✅ 可交，与 #1 ρ .6777 |
| 5 | `1YNl3p5R` | USA/TOP1000 | CROWDING d1 | 2.61 | 2.38 | 0.1341 | 0.6011 | 0.6011 | 0.4178 | 1.75 | +0.5256 | 1.06 | 0.017 | ❌（差 0.0011）| 档内第 2 族（1 现有） | 异族 | ET 11-13 17:4x | ✅ 可交 |
| 6 | `xAvMbRll` | EUR/TOP2500 | **R&M d1** | 3.17 | 2.45 | 0.1090 | 0.6281 | 0.6282 | 0.4828 | 2.33 | +0.3656 | 1.74 | 0.032 | ❌ | 档内第 4 族（3 现有） | 异族 | ET 11-13 17:5x | ✅ 可交 |
| 7 | `Wjl6JJQO` | EUR/TOP2500 | SUBINDUSTRY d1 | **6.13** | **4.69** | 0.2691 | 0.6413 | 0.6173 | **0.9336** | **8.72** | **+0.0164** | **6.32** | **0.524** | ❌ | 同上 | 异族 | ET 11-13 17:4x | ✅ 可交（余量薄）|
| 8 | `2r5rA775` | DEU/TOP500 | CROWDING d1 | 3.00 | 3.15 | 0.1340 | 0.6434 | 0.6436 | 0.5195 | 2.70 | +0.3007 | 1.82 | 0.042 | ❌ | 同上 | 异族 | ET 11-13 17:3x | ✅ 但与 #1 ρ **.8748** 同席 |
| 9 | `Xg9WNRg8` | USA/TOP2000 | SLOW d1 | 4.74 | 4.10 | 0.1659 | 0.6493 | 0.6493 | 0.7587 | 5.76 | +0.0819 | 4.26 | 0.174 | ❌ | 档内第 3 族（2 现有） | 异族 | ET 11-13 17:4x | ✅ 余量 0.0307 |
| — | `oma2WvGE` | USA/TOP1000 | FAST d1 | 1.77 | 1.01 | 0.2714 | **0.7658** | — | 0.28 | 0.80 | +1.27 | — | — | ❌ | — | 异族 | ET 11-13 17:5x | **❌ prod 红线** |
| — | `78YO6J31` | USA/TOP2000 | SUBINDUSTRY d1 | 2.22 | 1.74 | 0.1981 | **0.7636** | — | 0.36 | 1.26 | +0.77 | — | — | ❌ | — | 异族 | ET 11-13 17:5x | **❌ prod 红线** |
| — | `kqaRg6bO` | EUR/TOP2500 | SUBIND d2 | 3.21 | 2.85 | 0.0891 | — | — | 0.49 | 2.39 | +0.35 | — | — | ❌ | — | — | — | **❌ SUB_UNIVERSE FAIL** |
| — | `ZYaZAaKY` | EUR/TOP2500 | SECTOR d1 | 3.32 | 3.08 | 0.1023 | 未测 | — | 0.51 | 2.56 | +0.32 | — | — | ❌ | — | — | — | 被 `Wjl6JJQO` 支配，省槽未测 |
| — | `GrmVOWlO` | DEU/TOP500 | R&M cp3 | 2.87 | 2.90 | 0.1313 | 未测 | — | 0.50 | 2.47 | +0.34 | — | — | ❌ | — | — | — | cp3 相对 cp1 全项劣化，省槽未测 |
| — | `d5aq1Zbg` | USA/TOP1000 | SUBIND d1 | 1.82 | 1.36 | 0.2017 | 未测 | — | 0.29 | 0.85 | +1.20 | — | — | ❌ | — | — | — | S<μ̄，非竞争 |

### 5.3 席位互斥矩阵（`compute_mutual_correlation`，本地计算不占槽）

```
                  RReX6k6a  leaq3P9l  2r5rA775  Wjl6JJQO  1YNl3p5R  Xg9WNRg8  78YO6J31  oma2WvGE  xAvMbRll
RReX6k6a            1.0000    0.6777    0.8748    0.0760    0.1060    0.0570    0.0319   -0.0517    0.1547
leaq3P9l            0.6777    1.0000    0.7387    0.0491    0.0306    0.0196   -0.0071   -0.0566    0.1107
2r5rA775            0.8748    0.7387    1.0000    0.1281    0.0779    0.0217    0.0594   -0.0089    0.1276
Wjl6JJQO            0.0760    0.0491    0.1281    1.0000    0.0276   -0.0399   -0.0250    0.0126    0.3570
1YNl3p5R            0.1060    0.0306    0.0779    0.0276    1.0000    0.5064    0.4093    0.4162    0.0973
Xg9WNRg8            0.0570    0.0196    0.0217   -0.0399    0.5064    1.0000    0.3293    0.2191    0.0292
78YO6J31            0.0319   -0.0071    0.0594   -0.0250    0.4093    0.3293    1.0000    0.6524    0.0886
oma2WvGE           -0.0517   -0.0566   -0.0089    0.0126    0.4162    0.2191    0.6524    1.0000    0.0470
xAvMbRll            0.1547    0.1107    0.1276    0.3570    0.0973    0.0292    0.0886    0.0470    1.0000
```

第二组（补 `wpo6bEJ5` / `d5aq1Zbg`，5×5 独立计算；跨组未测格记为 `—`）：

```
                  RReX6k6a  wpo6bEJ5  d5aq1Zbg  1YNl3p5R  Xg9WNRg8
RReX6k6a            1.0000    0.7392   -0.0344    0.1060    0.0570
wpo6bEJ5            0.7392    1.0000   -0.0530    0.0423    0.0349
d5aq1Zbg           -0.0344   -0.0530    1.0000    0.4508    0.2391
1YNl3p5R            0.1060    0.0423    0.4508    1.0000    0.5064
Xg9WNRg8            0.0570    0.0349    0.2391    0.5064    1.0000
```

核心结论：**DEU/TOP500 四颗为同一席**（`RReX6k6a`~`2r5rA775` .8748、~`wpo6bEJ5` .7392、~`leaq3P9l` .6777）⇒ 该档只能交 1 颗。

- **最大互斥独立子集（ρ<0.5）= 5 颗**：`{RReX6k6a, 1YNl3p5R, 78YO6J31, Wjl6JJQO, xAvMbRll}`（`max_subset_exact=true`）
- `1YNl3p5R` ~ `Xg9WNRg8` = **0.5064** ⇒ 同席临界，**不可叠加**；选 `Xg9WNRg8`（S4.74/F4.10）还是 `1YNl3p5R`（S2.61/F2.38）取决于是否接受余量 0.0307

### 5.4 读法（§0.6.1 四条）
1. **席位边际 > 指标边际** — 本轮无零 SUPER 档，故全靠异族
2. **同族=死、异族可共存** — `Wjlke2Xx`（d1/d2 同族）与 `RReX6k6a` 是同一席的镜像；`wpo6bEJ5`/`leaq3P9l` 虽异族但 ρ>0.67 仍属同席
3. **区内 U/ρ_eff/N_eff 无独立信息**（严格单调于 S）
4. **ΔCAP% 已退化** — 除 `Wjl6JJQO`（+0.524%，S6.13 才有的量级）其余均 ≤0.042%，不可当排序主键；真正有区分力的是 **Eff + 席位类型 + 同/异族**

---

## 六、分 Region 方案

### 6.1 DEU / TOP500 — ⭐ 本轮最优新增产能（池 19，2 颗 SUPER）

**最优配方（已建成并实测）**

| 项 | 值 |
|---|---|
| ID | **`RReX6k6a`** |
| 配方 | `region=DEU universe=TOP500 delay=1 neut=REVERSION_AND_MOMENTUM decay=1`，l10，self_gate .7，turnover_max .6，prod_ceiling 1.0，combo_power 1 |
| IS | S **2.92** / F **2.91** / TO **0.1381** / Ladder 3.44(vs 2.02) / SubUniv 1.89(vs 1.39) / Cluster 1.85(vs 1.0) |
| 双闸 | prod **0.5514** / self **0.5516**（ET 11-13 17:4x，`refresh=True`）|
| 余量 | prod 0.1486 / self 0.1484 |
| 档位 | DEU/TOP500 第 3 族（现有 FAST `vR1oxZA3`、STAT `mLYLEm99`）|
| 倍率 | DEU D1 最高 1.8（model/news/other/analyst/fundamental/sentiment）|
| 判定 | **✅ 全闸通过，B 档双达标，本轮排序第一** |

同席备选（不可叠加）：`Wjlke2Xx`(R&M d2，F3.01/TO.1251/prod .5514)｜`wpo6bEJ5`(SLOW_AND_FAST，S2.81/F2.14/.5720)｜`leaq3P9l`(SLOW，S2.60/F2.11/.5951)｜`2r5rA775`(CROWDING，S3.00/F3.15/.6434，非 B 档)

**族谱（本轮补全，含历史）**

| 族 | S | F | TO | prod | 判定 |
|---|---|---|---|---|---|
| **REVERSION_AND_MOMENTUM d1** | 2.92 | 2.91 | .1381 | **.5514** | ✅ 最优可行 |
| R&M d2 | 2.89 | 3.01 | .1251 | .5514 | ✅ 同席镜像（F 略高、S 略低）|
| SLOW_AND_FAST d1 | 2.81 | 2.14 | .1909 | .5720 | ✅ |
| SLOW d1 | 2.60 | 2.11 | .1608 | .5951 | ✅ |
| CROWDING d1 | 3.00 | 3.15 | .1340 | .6434 | 过闸但非 B |
| FAST d1（已提交 11-07）| — | — | — | .5987 | 已 ACTIVE |
| SUBINDUSTRY d1 | 2.95 | 3.36 | .1308 | .7400 | ❌ prod 红线 |
| INDUSTRY d1（11-12）| 3.14 | 3.63 | — | .7412 | ❌ prod 红线 |
| SECTOR / MARKET（11-09）| 2.81/2.77 | 3.33/3.29 | — | .7701/.7708 | ❌ prod 红线 |
| R&M cp3 | 2.87 | 2.90 | .1313 | 未测 | cp 负杠杆 |

### 6.2 EUR / TOP2500 — 质量上限最高，但余量最薄（池 28，3 颗 SUPER）

| 项 | 值 |
|---|---|
| ID | `Wjl6JJQO`（存量，本轮重测） |
| 配方 | `EUR/TOP2500 d1 SUBINDUSTRY decay=1` l10 |
| IS | S **6.13** / F **4.69** / TO .2691 / Ladder 5.32(vs 2.02) / SubUniv 3.65 |
| 双闸 | prod **0.6413** / self **0.6173**（ET 11-13 17:4x）|
| 余量 | prod **0.0387**（薄）/ self 0.0827 |
| 边际 | U **0.9336**、N_eff **8.72**、ρ_eff **+0.0164**（几乎零组件相关）、Eff **6.32**、ΔCAP **+0.524%** 全轮唯一有量级 |
| 判定 | ✅ 可交，但抗漂移能力弱（EUR 历史 48h +0.068 漂移记录）|

同席（ρ .94–.985，11-13 实测，判弃）：`O0WE25PR`(INDUSTRY S6.03/.6489)、`Jj8Zr1Xn`(MARKET S5.63/.6661)
独立异族（弱）：`xAvMbRll`(R&M S3.17/F2.45/.6281，与 `Wjl6JJQO` ρ .357)｜`ZYaZAaKY`(SECTOR S3.32/F3.08，被支配)
判死：`xAv05p9J`(FAST S7.10/prod .7165)｜`kqaRg6bO`(SUBIND d2，SUB_UNIVERSE FAIL)

**EUR 族规律（本轮补第 5 族）**：S 与 prod 同向——FAST 7.10/.7165 → SUBIND 6.13/.6413 → INDUSTRY 6.03/.6489 → MARKET 5.63/.6661 → SECTOR 3.32 → R&M 3.17/.6281。**S 最高的族必然最先撞墙。**

### 6.3 USA / TOP1000 — 空档最多，天花板最低（池 47，1 颗 SUPER）

| 候选 | 族 | S | F | TO | prod | 判定 |
|---|---|---|---|---|---|---|
| `1YNl3p5R` | CROWDING d1 | 2.61 | 2.38 | .1341 | **.6011** | ✅ 可交，B 档差 0.0011 |
| `d5aq1Zbg` | SUBIND d1 | 1.82 | 1.36 | .2017 | 未测 | S<μ̄，非竞争 |
| `oma2WvGE` | FAST d1 | 1.77 | 1.01 | .2714 | **.7658** | ❌ prod 红线 |
| `78YE2KVv`(11-13) | MARKET d1 | 1.71 | 1.35 | .1837 | .8001 | ❌ |
| 历史 | SLOW | — | 0.85 | — | — | ❌ F 死 |

**结论**：该档只剩 CROWDING 一条可行路，S 天花板 ≈2.6。空档多但无产能，**判为低优先**。

### 6.4 USA / TOP2000 — SLOW 已交，候选被顶到临界（池 47，2 颗 SUPER）

- `Xg9WNRg8`（SLOW d1，存量）：S **4.74** / F **4.10** / TO .1659｜prod **0.6493** / self 0.6493｜余量 **0.0307**｜Eff 4.26｜与已提交 `e75avmq6`（同 SLOW d1）ρ 仅 **0.4804** ⇒ **不是同席，仍可交**
- 新族全灭：SUBIND `78YO6J31` prod .7636｜FAST `RRenvW7b` .7493｜INDUSTRY `9qlL2Xlo` .7709｜CROWDING `E56208rR` .7032｜SECTOR .6957
- **结论**：只剩 SLOW 一颗，余量 0.0307 属「能过但薄」，非首选

### 6.5 其他区域
- **GBR/TOP700（6 颗）/ IND/TOP500（12）/ KOR/TOP600（11）/ USA/TOP3000（6）**：档内 ≥5，换族不再分散 ⇒ **停扫**
- **GLB 四档**：MINVOL10M 已同席全灭、TOP3000/TOPDIV3000 结构性 prod 墙、MINVOL1M 历史 FAST .7486 ⇒ **停投**
- **ASI 两档**：`QPv88bJW` 提交后 `A1VAAbWe` prod 0.6634→.7275（+0.064 定向毒化），区域 prod 下界 0.51 被顶高 ⇒ **停投**
- **EUR/TOPCS1600**：同席全灭；**EUR/TOP1200·800·400**：零 SUPER 但第 5 次判死（窄 universe 截断压 S）
- **MEA**：平台下架（400）；**HKG**：池 7/10；**CHN/AMR**：池 0

---

## 七、停投区 + 撞墙档案（累计，本轮新增标 ★）

| 区域/档 | 撞墙原因 | 首证 |
|---|---|---|
| ★ USA/TOP1000 FAST | prod **0.7658** | 11-14 |
| ★ USA/TOP2000 SUBINDUSTRY | prod **0.7636** | 11-14 |
| ★ EUR/TOP2500 SUBIND **d2** | `LOW_SUB_UNIVERSE_SHARPE` 1.62<1.67（S 从 6.13 掉到 3.21）| 11-14 |
| ★ DEU/TOP500 R&M **cp3** | 相对 cp1 全项劣化（S −0.05、F −0.01、TO −0.007）| 11-14 |
| ★ DEU/TOP500 MARKET/SECTOR/INDUSTRY/SUBIND | prod .74–.77 | 11-09~11-13 |
| EUR 全域（TOP2500 除外已 4 族）| prod 墙 + 窄 universe 截断压 S | 10-23~ |
| ASI 两档 | 兄弟提交后 +0.064 毒化 | 11-12 |
| GLB 四档 | prod 墙 / 同席全灭 / 建单失败 | 10-26~ |
| IND/KOR/GBR/USA-TOP3000 | 档内 ≥5 颗，换族不再分散 | 11-09~ |
| USA/TOP500·TOPSP500·TOP200 | 同席全灭 / S 不可达 | 10-27~ |
| MEA 全区 | 平台下架 400 | 10-24 |
| HKG / CHN / AMR | 池 7 / 0 / 0（<10）| 10-21~ |

---

## 八、执行清单（本轮已完成，可复跑）

```bash
cd D:/coding/traeCN_project/wqb
PY=world-quant-brain-mcp/.venv/Scripts/python.exe
D=results/sa_scan_20261114

# 0) 先清 api_cache 的 user_alphas%，再刷池（否则读 7 天旧缓存）
#    DELETE FROM api_cache WHERE cache_key LIKE 'user_alphas%'
$PY tools/probe/probe_sa_candidates.py --refresh

# 1) 本轮 10 档（已跑完，结果在 $D/res_*.json）
$PY tools/super_build.py select --region DEU --universe TOP500 --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_deu_t500_revmom_d1.json
$PY tools/super_build.py select --region DEU --universe TOP500 --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 2 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_deu_t500_revmom_d2.json
$PY tools/super_build.py select --region DEU --universe TOP500 --delay 1 --neutralization SLOW_AND_FAST --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_deu_t500_slowfast_d1.json
$PY tools/super_build.py select --region EUR --universe TOP2500 --delay 1 --neutralization REVERSION_AND_MOMENTUM --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_eur_t2500_revmom_d1.json
$PY tools/super_build.py select --region EUR --universe TOP2500 --delay 1 --neutralization SECTOR --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_eur_t2500_sector_d1.json
$PY tools/super_build.py select --region EUR --universe TOP2500 --delay 1 --neutralization SUBINDUSTRY --decay 2 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_eur_t2500_subind_d2.json
$PY tools/super_build.py select --region USA --universe TOP1000 --delay 1 --neutralization FAST --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t1000_fast_d1.json
$PY tools/super_build.py select --region USA --universe TOP1000 --delay 1 --neutralization SUBINDUSTRY --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t1000_subind_d1.json
$PY tools/super_build.py select --region USA --universe TOP2000 --delay 1 --neutralization SUBINDUSTRY --decay 1 --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 --json $D/res_usa_t2000_subind_d1.json

# 2) 双闸（逐颗，refresh=True；平台单并发，busy 隔 1.8s 重试）
#    check_correlation(alpha_id=..., correlation_type="both", refresh=True)

# 3) 席位互斥（本地，不占槽）
#    compute_mutual_correlation(alpha_ids=[...], threshold=0.5, years=4)
```

**工程约束**
- **并发仿真上限 = 2**：第 3 路必 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`；`super_build.py select` 只印 `[error] ... / None`，不显示 status_code ⇒ 批量必须 2 路
- **同式异 decay 同批会被平台去重** ⇒ 分两次派（本轮 batch5 已按此做）
- 单档仿真 3–8 min；universe 内 REGULAR=0 的档（GLB/MINVOL10M）需 ~35 min，勿按 8 min 判挂起
- `probe --json results/x.json` 会拼成 `results/results/x.json` 报错；纯文件名被忽略 ⇒ 用默认路径再复制
- GLB/TOPDIV3000 + SLOW **建单必失败**；USA/ILLIQUID_MINVOL1M **非法档位**
- ET 时间只信 `wqb.timeutil`（Git Bash `TZ=` 无效）

---

## 九、算子利用率审计

**官方 SA 算子表**：COMBO ≥160 个、SELECTION 专属 ≥43 个（2026-11-06 读官方《SuperAlpha Operators》附录）。

**本账户 55 颗 SA 实际使用**

| 维度 | 使用数 | 覆盖率 | 明细 |
|---|---|---|---|
| COMBO | **4** | **2.5%** | `generate_stats`、`self_corr`、`if_else`、`reduce_max`（全部来自默认模板，本轮 0 新增）|
| SELECTION | **0**（函数算子）| **0%** | selection 表达式只做字段比较：`prod_correlation`、`self_correlation`、`turnover` |
| 中性化族 | 9/11 | 82% | 本轮新增 **REVERSION_AND_MOMENTUM**（DEU + EUR）与 **SLOW_AND_FAST**（DEU）；未试 `NONE` |

**本轮 combo 模板**：`stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); w = 1 - maxCorr; w`

**结论**
1. COMBO 轴 2.5% 覆盖率，但历史已证 `zscore(w)`（毁灭性，S −1.14）、`rank(w)`/`sqrt(w)`/`ts_mean(w)`（全撞同席）、`cp≥6`（Ladder FAIL）⇒ **整形轴的边际收益已枯竭**，本轮 0 新增是合理结果
2. 本轮真正的杠杆在**中性化族轴**（R&M / SLOW_AND_FAST），不在算子轴
3. 唯一未试的高价值项仍是 `combo_weight`（语义未知）与 SELECTION 的 `universe_size`/`dataset_count`；后者在 IND 有效（产出 `3qoG6nEe`）但在 KOR 恒常数

---

## 十、提交建议（**本轮未提交，等待用户指令**）

### 10.1 建议对象

| 顺位 | ID | 档位/族 | S/F/TO | prod/self（`refresh=True` ET 11-13）| 四项合规检查 |
|---|---|---|---|---|---|
| **①** | **`RReX6k6a`** | DEU/TOP500 · R&M d1 | 2.92 / 2.91 / .1381 | **0.5514 / 0.5516** | ✅ prod≤0.68 ✅ self≤0.68 ✅ 13 checks 0 FAIL ✅ 台账无 `robustness_RReX6k6a` ✅ 异族（现有 FAST / STAT）|
| ② | `Wjl6JJQO` | EUR/TOP2500 · SUBIND d1 | 6.13 / 4.69 / .2691 | 0.6413 / 0.6173 | ✅ 全过，但 prod 余量 **0.0387** 薄；异族（现有 CROWD/SLOW/STAT）|
| ③ | `1YNl3p5R` | USA/TOP1000 · CROWDING d1 | 2.61 / 2.38 / .1341 | 0.6011 / 0.6011 | ✅ 全过；档内仅 1 颗 SUPER（余量最大）；但 S/F 最低 |

**推荐 ①**，理由：唯一同时满足「B 档双达标 + prod 余量 0.1486（抗漂移）+ 新族 + DEU D1 塔倍率最高 1.8」的候选；F 2.91 与 S 2.92 接近 1:1，`F=S×√(ret/max(TO,.125))` 已顶到 TO 下限附近，指标质量不虚。

若用户偏好 S/F 上限，选 **②**（S 是 ① 的 2.1 倍、Eff 3.2 倍），代价是 prod 余量只剩 0.0387。

⚠ **② 与 ① 不可叠加**：ρ 仅 0.076，是真正独立的两席，可先后提交（不同 ET 日）。

### 10.2 配额提示

- `SUPER_SUBMISSION` = **1 颗 / ET 日历日、账户级、00:00 ET 重置**（GMT+8 13:00）
- 当前 **ET 2026-11-13 17:5x**；末次 SUPER 提交 = `e75avmq6`（USA/TOP2000 SLOW）于 **ET 2026-11-12 19:53**
- ⇒ **本 ET 日（11-13）配额未使用**；距重置约 6h（GMT+8 2026-11-14 13:00）
- 403 零配额成本、不判死候选；同日重复 POST 只会继续 403，勿当探针

### 10.3 命令模板（**仅供用户手动执行，本轮未执行**）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit --alpha-id RReX6k6a --region DEU
```

备选：
```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit --alpha-id Wjl6JJQO --region EUR
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit --alpha-id 1YNl3p5R --region USA
```

### 10.4 两个已知提交坑

1. **提交前停后台批次**：并发仿真会让 `_probe_prod_max` 抛 ProxyError（对方占着 prod 槽）
2. **prod 槽有 195s 冷却**（`logs/_dblock/correlation.cooldown.json`）：未过期会 fail-fast，不是信号问题

### 10.5 提交后的连带影响（提前告知）

- 交 `RReX6k6a` ⇒ **同席 4 颗全废**（`Wjlke2Xx` / `wpo6bEJ5` / `leaq3P9l` / `2r5rA775`，ρ .68–.87），DEU/TOP500 变 3 颗；**DEU 族位只剩 MARKET/SECTOR/INDUSTRY/SUBIND（均 prod 墙）⇒ DEU 实质封档**
- 交 `Wjl6JJQO` ⇒ EUR/TOP2500 变 4 颗；`xAvMbRll`（ρ .357）仍可交，`O0WE25PR`/`Jj8Zr1Xn` 已判弃
- 交 `1YNl3p5R` ⇒ 顶高 `Xg9WNRg8`（现 ρ .5064，预计趋同）⇒ 二者只能选一

---

## 附录 A：本轮构建清单（10 档）

| # | 档位 | 族 | decay | ID | S | F | TO | prod | 结果 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | DEU/TOP500 | R&M | 1 | `RReX6k6a` | 2.92 | 2.91 | .1381 | .5514 | ✅ 排序第一 |
| 2 | DEU/TOP500 | R&M | 2 | `Wjlke2Xx` | 2.89 | 3.01 | .1251 | .5514 | ✅ 同席镜像 |
| 3 | DEU/TOP500 | SLOW_AND_FAST | 1 | `wpo6bEJ5` | 2.81 | 2.14 | .1909 | .5720 | ✅ |
| 4 | DEU/TOP500 | R&M cp3 | 1 | `GrmVOWlO` | 2.87 | 2.90 | .1313 | — | 被 #1 支配 |
| 5 | EUR/TOP2500 | R&M | 1 | `xAvMbRll` | 3.17 | 2.45 | .1090 | .6281 | ✅ 独立席 |
| 6 | EUR/TOP2500 | SECTOR | 1 | `ZYaZAaKY` | 3.32 | 3.08 | .1023 | — | 被 `Wjl6JJQO` 支配 |
| 7 | EUR/TOP2500 | SUBIND | 2 | `kqaRg6bO` | 3.21 | 2.85 | .0891 | — | ❌ SUB_UNIVERSE |
| 8 | USA/TOP1000 | FAST | 1 | `oma2WvGE` | 1.77 | 1.01 | .2714 | **.7658** | ❌ prod 红线 |
| 9 | USA/TOP1000 | SUBINDUSTRY | 1 | `d5aq1Zbg` | 1.82 | 1.36 | .2017 | — | S<μ̄ 非竞争 |
| 10 | USA/TOP2000 | SUBINDUSTRY | 1 | `78YO6J31` | 2.22 | 1.74 | .1981 | **.7636** | ❌ prod 红线 |

## 附录 B：本轮 `refresh=True` 双闸实测记录（11 颗）

| ID | prod | self | 结论 | 时刻（ET）|
|---|---|---|---|---|
| `RReX6k6a` | 0.5514 | 0.5516 | PASS（top1 = `vR1oxZA3`）| 11-13 17:4x |
| `Wjlke2Xx` | 0.5514 | 0.5516 | PASS（与 d1 逐位相同）| 11-13 17:5x |
| `wpo6bEJ5` | 0.5720 | 0.5723 | PASS | 11-13 17:5x |
| `leaq3P9l` | 0.5951 | 0.5954 | PASS（与 11-13 一致，零漂移）| 11-13 17:3x |
| `2r5rA775` | 0.6434 | 0.6436 | PASS（零漂移）| 11-13 17:3x |
| `1YNl3p5R` | 0.6011 | 0.6011 | PASS（零漂移）| 11-13 17:4x |
| `Wjl6JJQO` | 0.6413 | 0.6173 | PASS（零漂移）| 11-13 17:4x |
| `Xg9WNRg8` | 0.6493 | 0.6493 | PASS（self top1 = `vROw5Rkd` .6493；**与 `e75avmq6` 仅 .4804**）| 11-13 17:4x |
| `xAvMbRll` | 0.6281 | 0.6282 | PASS（self top1 = `GrgGkV1o` .6282）| 11-13 17:5x |
| `78YO6J31` | **0.7636** | — | FAIL（prod 早退）| 11-13 17:5x |
| `oma2WvGE` | **0.7658** | — | FAIL（prod 早退）| 11-13 17:5x |

**零漂移观察**：存量四颗（`leaq3P9l`/`2r5rA775`/`1YNl3p5R`/`Wjl6JJQO`/`Xg9WNRg8`）本轮重测值与 11-13 逐位相同 ⇒ 11-12 的 `e75avmq6` 提交未对它们产生定向毒化（与 11-12 记录的「同区新 ACTIVE +0.064」不同，因该次是同族跨 universe）。
