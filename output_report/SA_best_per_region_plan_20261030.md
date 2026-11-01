# 各 Region 最优 SuperAlpha 方案 — 2026-10-30 全流程扫描

生成时间：2026-10-30 (GMT+8)　|　扫描目录：`results/sa_scan_20261030/`
铁律：**只挖不提交**（全部为待执行配方）；**prod ≥ 0.7 = 合规红线，无豁免**；prod/self 值一律 `check_correlation(refresh=True)` 实测。

---

## 0. 执行摘要

| 优先级 | α id | Region / 档位 | 配方 | Sharpe | Fitness | TO | prod | self | 余量(prod/self) | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **P0 ★** | `O0Aw0Y7Y` | **KOR / TOP600** | STAT d1 l10 `combo_a(alpha)` | **4.27** | **4.76** | 0.1517 | **0.5581** | **0.5581** | **0.142 / 0.142** | ✅ 双闸全过，余量最厚（新） |
| **P1 ★** | `bl62YwRN` | **IND / TOP500** | CROWDING d1 l10 `combo_a(alpha)` | 3.70 | 3.38 | 0.2134 | **0.5636** | **0.5634** | **0.136 / 0.137** | ✅ 双闸全过，余量厚 |
| **P2 ★** | `6XdPxKN5` | **USA / TOP3000** | INDUSTRY d1 l10 `combo_a(alpha)` | **4.99** | **5.53** | 0.1264 | **0.6065** | **0.6060** | **0.094 / 0.094** | ✅ 双闸全过（**池 45 → USA 复活**） |
| **P3 ★** | `MPYAOR0r` | **GBR / TOP700** | STAT d1 l10 `combo_a(alpha)` | 3.72 | 2.57 | 0.2114 | **0.5295** | **0.5296** | **0.170 / 0.170** | ✅ 已提交 ACTIVE（10-28） |
| **P4 ★** | `YP1d66KM` | **EUR / TOPCS1600** | CROWDING d1 l10 `combo_a(alpha)` | 3.57 | 2.43 | 0.2425 | **0.5985** | **0.5656** | **0.101 / 0.134** | ✅ 已建未提交（10-23） |
| **P5** | `3qoWQKJg` | **KOR / TOP600** | INDUSTRY d1 l10 `combo_a(alpha)` | 3.62 | 4.32 | 0.1369 | **0.6221** | **0.6224** | 0.078 / 0.078 | ✅ 已建未提交（10-22） |
| ~~P6~~ | `zq3zKgd8` | IND / TOP500 | STAT d1 l10 `combo_a(alpha)` | 4.69 | 4.29 | 0.2254 | **0.6953** | **0.6954** | 0.005 / 0.005 | ⚠️ 勉强过（余量 <0.02，不推荐） |
| ~~P7~~ | `akK2Jnm6` | USA / TOP3000 | CROWDING d1 l10 `combo_a(alpha)` | 4.62 | 5.30 | 0.1208 | **0.7075** | 0.606 | — | ❌ prod 超标（0.0075） |
| ~~P8~~ | `0mYko03p` | USA / TOP3000 | STAT d1 l10 `combo_a(alpha)` | 5.71 | 5.52 | 0.1428 | 0.5165 | 0.450 | — | ❌ IS FAIL（LOW_SUB_UNIVERSE_SHARPE 2.21<2.47） |
| ~~P9~~ | `xAraq1jm` | GLB / MINVOL1M | STAT d1 l10 `combo_a(alpha)` | 7.45 | 4.08 | 0.3244 | **0.8307** | 0.831 | — | ❌ prod 超标 |
| ~~P10~~ | `QPvdMW8Q` | DEU / TOP500 | STAT d1 l10 `combo_a(alpha)` | 2.30 | 1.55 | 0.2064 | **0.8849** | 0.885 | — | ❌ prod 超标 |

### 本轮最大发现：组件池大幅增长 ⇒ USA 复活

**10-29 → 10-30 组件池变化**（口径：stage=OS + type=REGULAR + status=ACTIVE + 已提交）：

| Region | 10-29 池 | 10-30 池 | 变化 | 影响 |
|---|---:|---:|---:|---|
| **USA** | 11 | **45** | **+309%** | **从"prod 必炸"→ INDUSTRY 族 prod 0.6065 可过闸** |
| **IND** | 21 | **45** | +114% | CROWDING 族 prod 0.5636（STAT 仍 0.695） |
| **KOR** | 17 | **30** | +76% | STAT 族 prod 0.5581（新最优，超越 INDUSTRY 0.6221） |
| GBR | 18 | 18 | — | STAT 0.5295 仍是最优 |
| EUR | 17 | 18 | +6% | CROWDING 0.5985 |
| GLB | 17 | 17 | — | prod 0.831 仍炸（同 universe 重叠） |
| DEU | 10 | 10 | — | prod 0.885 仍炸（池最小） |
| **MEA** | — | **19** | 新 | ⚠ STATISTICAL 不可用，CROWDING/INDUSTRY 扫描中 |

> **核心规律确认**：池大小决定 prod 天花板。池 ≥17 ⇒ prod 可控；池 ≤11 ⇒ prod 必炸。USA 从 11→45 是本轮回差最大的单区变化，直接让 USA 从"永久停投"变为"P2 可交付"。

### 本轮方法论

1. **`combo_a(alpha)` 仍是唯一有效 combo 算子**（103 个算子中仅此 1 个在 SA 组合层可用）。
2. **中性化族选择是 prod 的第一杠杆**（> 池大小 > selection_limit）：
   - USA：INDUSTRY (0.607) ≫ CROWDING (0.708) > STAT (IS FAIL)
   - IND：CROWDING (0.564) ≫ STAT (0.695)
   - KOR：STAT (0.558) > INDUSTRY (0.622)
   - GBR：STAT (0.530)（唯一测试）
   - EUR：CROWDING (0.599)（唯一测试）
3. **l10 在所有区域均最优**（与 10-22 EUR 实测一致：组件数↑ ⇒ self↓ 但 prod↑，l10 双闸综合最优）。
4. **SUPER 配额 = 账号级全局 1/ET 日**（41 颗已提交 SUPER 日期两两唯一，铁证）。

---

## 1. 数据基线

### 1.1 组件池 eligibility（口径：stage=OS + type=REGULAR + status=ACTIVE + 已提交）

| Region | 池 | 主要 universe | 可建 | 备注 |
|---|---:|---|---|---|
| USA | **45** | TOP3000 | ✅ | 池大幅增长，INDUSTRY 族可过闸 |
| IND | **45** | TOP500 | ✅ | CROWDING 族 prod 0.564 |
| KOR | **30** | TOP600 | ✅ | STAT 族 prod 0.558（新最优） |
| MEA | **19** | TOP400 | ❌ | 平台不支持 SA 创建（非组件不足） |
| GBR | **18** | TOP700 | ✅ | STAT 族 prod 0.530 |
| EUR | **18** | TOPCS1600:12 / TOP2500:6 | ✅ | CROWDING 族 prod 0.599 |
| GLB | **17** | MINVOL1M | ✅ | 同 universe 全池 ⇒ prod 0.831 必炸 |
| DEU | **10** | TOP500 | ✅ | 池最小 ⇒ prod 0.885 必炸 |
| ASI | **9** | MINVOL1M:5 / MINVOL10M:4 | ❌ | < 平台硬下限 10 |
| HKG | **6** | TOP800 | ❌ | < 平台硬下限 10 |

### 1.2 档位占用分类（★ 10-30 复核）

| Region | 已提交 SUPER 数 | 代表 α（最新 3 颗） | 档位类型 |
|---|---:|---|---|
| IND | **11** | `88vKp8Va`(10-17) `pw52P3jb`(10-12) `wpbQjeKp`(10-09) | OCCUPIED |
| KOR | **9** | `RRA9EZKz`(10-22) `9qWJv1do`(10-06) `9qWbA1g9`(10-04) | OCCUPIED |
| USA | **7** | `E567rQvR`(10-27) `2rj3ddl5`(10-25) `LL5aX6Y2`(10-19) | OCCUPIED |
| GLB | **5** | `LLMVPag1`(10-26) `LL5amzov`(10-14) `npARO63x`(10-15) | OCCUPIED |
| GBR | **3** | `MPYAOR0r`(10-28) `e7QGwrx6`(10-10) `YPMp39q6`(10-08) | OCCUPIED |
| EUR | **3** | `kqJOQgnk`(10-23) `vROOONwd`(10-21) `GrgGkV1o`(10-20) | OCCUPIED |
| MEA | **2** | `78jYpn0Z`(08-28) `3qlYKAaO`(08-21) | OCCUPIED（旧） |
| DEU | **1** | `mLYLEm99`(10-18) | OCCUPIED |

> **★★ 配额铁证**：41 颗已提交 SUPER 横跨 08-31 ~ 10-28，**日期两两唯一**（41 颗 / 41 个不同 ET 日）⇒ **`SUPER_SUBMISSION` 是账号级全局配额 = 1/ET 日**，**不是** 1/ET 日/区。最新占用日 = 10-28 ET（`MPYAOR0r`），下一窗口 = 10-29 00:00 ET 已过 ⇒ **当前（10-30 ET）SUPER 配额可用**。

**未提交 SA 候选：26 颗**（IS 阶段，含 `E560WoZr` USA S6.61、`Vkxwjvm5` KOR S5.49、`0mYkl508` IND S4.58 等）。

### 1.3 Pyramid 倍率（`get_pyramid_multipliers`，10-30 实测）

| Region | D0 区间 | D1 区间 | 备注 |
|---|---|---|---|
| DEU | 1.6–1.9 | 1.2–1.8 | 全平台最高（model/analyst D0 1.9） |
| GBR | 1.3–1.9 | 1.0–1.7 | news/analyst D0 1.9 |
| EUR | 1.0–1.7 | 1.0–1.5 | model/analyst D0 1.6 |
| USA | 1.0–1.8 | 1.0–1.4 | sentiment D0 1.8 |
| KOR | — | 1.0–1.6 | analyst/model 1.6 |
| GLB | — | 1.0–1.4 | fundamental/analyst 1.4 |
| IND | — | 1.0–1.4 | analyst 1.4 |
| MEA | — | — | 未返回（SA 不可用） |

---

## 2. 选点原则（10-30 实证更新）

1. **池大小 > 中性化族 > selection_limit**：池 ≥17 ⇒ prod 可控；池 ≤11 ⇒ prod 必炸。族和 combo 在池足够时差异不大。
2. **中性化族是 prod 第一杠杆**（本轮实测）：
   - USA：INDUSTRY (0.607) ≫ CROWDING (0.708) —— 同池不同族差 0.10
   - IND：CROWDING (0.564) ≫ STAT (0.695) —— 同池不同族差 0.13
   - KOR：STAT (0.558) > INDUSTRY (0.622) —— 反转（与 IND 相反）
   ⇒ **族的选择必须逐区扫描，不可跨区照搬**（IND CROWDING 最优，KOR STAT 最优）。
3. **`combo_a(alpha)` 是唯一可用 combo**：裸变量名（`w`/`weight`）报 "unknown variable"；裸算子名报维度错误；`generate_stats`/`self_corr`/`reduce_*` 在 combo 上下文无隐式输入。仅 `combo_a(alpha)` 通过（含 `nlength=250, mode='algo1'` 默认参数）。
4. **selection 仍用 `(1 - self_correlation)`**：小池区（EUR/GLB/DEU）宽松 selection 即可；USA 曾用 `(1 + 0*(prod_correlation>0)) * (1 - self_correlation)` 但本轮 CROWDING 族 prod 仍 0.708。
5. **selection_limit = 10**（平台硬下限，实际生效 = min(limit, 池)）。
6. **truncation 0.02 vs 0.08 无显著差异**（USA 用 0.02，其余用 0.08）。

---

## 3. 论坛指标标准（§0 固化，引用）

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

**组件筛选阈值**（论坛 22 赞比赛心得）：`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。⚠ 小池区只能用宽松 selection `(1 - self_correlation)`。

**中性化族规律**（LY43440 实测 IND）：Fitness 排序 **CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**；选族规则 **TO<0.10 → SLOW；TO>0.20 → FAST**。

---

## 4. 分 Region 方案

### 4.1 KOR / TOP600 — P0 最优（本轮新发现，余量最厚）

- **α id**: `O0Aw0Y7Y`
- **配方**: STATISTICAL / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S4.27 / F4.76 / TO 0.1517 / prod **0.5581** / self **0.5581**
- **余量**: prod 0.142 / self 0.142 —— 本轮新测，超越 IND CROWDING 成为余量最厚候选
- **RA**: 全过（failed_ra_count=0）
- **IS checks**: 全部 pass
- **池**: 30（KOR 全在 TOP600）
- **对比**: 同区 INDUSTRY 族 `3qoWQKJg` prod 0.6221（余量 0.078）⇒ STAT 族在 KOR 显著优于 INDUSTRY

### 4.2 IND / TOP500 — P1（CROWDING 族最优）

- **α id**: `bl62YwRN`
- **配方**: CROWDING / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.70 / F3.38 / TO 0.2134 / prod **0.5636** / self **0.5634**
- **余量**: prod 0.136 / self 0.137
- **RA**: 全过
- **IS checks**: 全部 pass
- **池**: 45（IND 全在 TOP500）
- **对比**: 同区 STAT 族 `zq3zKgd8` prod 0.6953（余量 0.005）⇒ CROWDING 族在 IND 显著优于 STAT

### 4.3 USA / TOP3000 — P2（池增长 ⇒ 复活）

- **α id**: `6XdPxKN5`
- **配方**: INDUSTRY / d1 / decay 1 / l10 / trunc 0.02 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S4.99 / F5.53 / TO 0.1264 / prod **0.6065** / self **0.6060**
- **余量**: prod 0.094 / self 0.094
- **RA**: 全过
- **IS checks**: 全部 pass
- **池**: 45（USA 全在 TOP3000）
- **★ 10-29 判死 → 10-30 复活**：池 11→45，INDUSTRY 族 prod 从 0.7341→0.6065（-0.128）。**USA 不再是永久停投区。**
- **同池对比**：CROWDING 族 `akK2Jnm6` prod 0.7075（仍超标）；STAT 族 `0mYko03p` prod 0.5165 但 IS FAIL（LOW_SUB_UNIVERSE_SHARPE 2.21<2.47）⇒ **INDUSTRY 是 USA 唯一可交付族**。

### 4.4 GBR / TOP700 — P3（已提交，余量最厚）

- **α id**: `MPYAOR0r`（**已提交 ACTIVE，10-28 20:59 ET**）
- **配方**: STATISTICAL / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.72 / F2.57 / TO 0.2114 / prod **0.5295** / self **0.5296**
- **余量**: prod 0.170 / self 0.170 —— 全场最厚
- **池**: 18（GBR 全在 TOP700）

### 4.5 EUR / TOPCS1600 — P4（已建未提交）

- **α id**: `YP1d66KM`（**已建未提交，10-23 创建**）
- **配方**: CROWDING / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.57 / F2.43 / TO 0.2425 / prod **0.5985** / self **0.5656**
- **余量**: prod 0.101 / self 0.134
- **池**: 18（TOPCS1600:12 / TOP2500:6）

### 4.6 KOR / TOP600 — P5（INDUSTRY 族备选）

- **α id**: `3qoWQKJg`（**已建未提交，10-22 创建**）
- **配方**: INDUSTRY / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.62 / F4.32 / TO 0.1369 / prod **0.6221** / self **0.6224**
- **余量**: prod 0.078 / self 0.078
- **池**: 30

### 4.7 IND / TOP500 — P6（STAT 族，余量不足）

- **α id**: `zq3zKgd8`
- **配方**: STATISTICAL / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S4.69 / F4.29 / TO 0.2254 / prod **0.6953** / self **0.6954**
- **余量**: prod 0.005 / self 0.005 —— **不满足 ≥0.02 余量要求，不推荐交付**
- **池**: 45

### 4.8 USA / TOP3000 — 判死（CROWDING 族）

- **α id**: `akK2Jnm6`
- **配方**: CROWDING / d1 / decay 1 / l10 / trunc 0.02 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S4.62 / F5.30 / TO 0.1208 / prod **0.7075** ❌ / self 0.606
- **结论**: 池 45 仍不够压住 CROWDING 族 prod。**USA CROWDING 停投**（INDUSTRY 是唯一可交付族）。

### 4.9 USA / TOP3000 — 判死（STAT 族 IS FAIL）

- **α id**: `0mYko03p`
- **配方**: STATISTICAL / d1 / decay 1 / l10 / trunc 0.02 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S5.71 / F5.52 / TO 0.1428 / prod 0.5165 / self 0.450 —— **prod/self 双优**
- **IS FAIL**: `LOW_SUB_UNIVERSE_SHARPE` value=2.21 limit=2.47（差 0.26）
- **结论**: prod 余量 0.183 是全场最厚，但 IS sub-universe Sharpe 不过平台闸。**不可交付**。若后续能修复 sub-universe Sharpe（换 selection 或调 truncation），这颗是隐藏宝石。

### 4.10 GLB / MINVOL1M — 判死

- **α id**: `xAraq1jm`
- **配方**: STAT / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S7.45 / F4.08 / TO 0.3244 / prod **0.8307** ❌
- **结论**: 池 17 颗全在 MINVOL1M 同一 universe ⇒ 合成信号与生产池高度重叠。**GLB 停投**（除非换 universe）。

### 4.11 DEU / TOP500 — 判死

- **α id**: `QPvdMW8Q`
- **配方**: STAT / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S2.30 / F1.55 / TO 0.2064 / prod **0.8849** ❌
- **结论**: 池仅 10 颗（刚好卡线），prod 全场最差。**DEU 停投**。

### 4.12 MEA / TOP400 — 判死（平台不支持 SA）

- **α id**: 无（构建失败）
- **配方**: STAT / CROWDING / INDUSTRY 均失败
- **现象**: HTTP 400 —— "Region MEA is not available."（STAT/CROWDING/INDUSTRY 三族全部拒绝）
- **结论**: 虽然 MEA 有 19 颗 ACTIVE REGULAR 组件（满足 ≥10 硬下限），但 **平台不支持在 MEA 区域创建 SUPER alpha**。**MEA 停投**（非组件不足，是平台区域限制）。

### 4.13 ASI / HKG — 不可建

- ASI 池 = 9 < 10；HKG 池 = 6 < 10。**停投**。

---

## 5. 撞墙档案（★=本轮新增）

| # | 区域 / 档位 | 配方 | 现象 | 结论 |
|---|---|---|---|---|
| ★W1 | USA/TOP3000 | `combo_a(alpha)` CROWDING | prod 0.7075（超 0.0075） | 池 45 仍不够压 CROWDING |
| ★W2 | USA/TOP3000 | `combo_a(alpha)` STAT | prod 0.5165 但 IS FAIL | LOW_SUB_UNIVERSE_SHARPE 2.21<2.47 |
| ★W3 | IND/TOP500 | `combo_a(alpha)` STAT | prod 0.6953（余量 0.005） | CROWDING 族远优于 STAT |
| ★W4 | MEA/TOP400 | STAT / CROWDING / INDUSTRY | HTTP 400 "Region MEA is not available" | 平台不支持 MEA 区域 SA 创建 |
| ★W5 | USA/TOP3000 | CROWDING prod 实测 | PC 超时 240s ×3 颗 | 平台 prod 计算慢，需耐心重试 |
| W6 | GLB/MINVOL1M | `combo_a(alpha)` | prod 0.8307 | 同 universe 全池 ⇒ 高度重叠 |
| W7 | DEU/TOP500 | `combo_a(alpha)` | prod 0.8849 | 池 10 ⇒ 极端集中 |
| W8 | combo `rank(w)` / `weight` / `combo_weight` | 任意 | "unknown variable" | 平台 combo 不接受裸变量名 |
| W9 | combo `reduce_max` / `combo_a`(裸) | 任意 | "dimensions dates,alphas:10" | 裸算子名无输入源 |
| W10 | combo `generate_stats(alpha)` | 任意 | "set of expressions" | 不可单独作为 combo |
| W11 | combo `self_corr(alpha)` | 任意 | "lookback must have a value" | 需显式 lookback 参数 |
| N1 | ASI | 任意 | 池 = 9 < 10 | 平台硬下限 |
| N2 | HKG | 任意 | 池 = 6 < 10 | 平台硬下限 |

---

## 6. ★ 平台 SA 算子清单与利用率审计

来源：`get_operators`（103 个算子）+ 本轮 SA 组装实测。

### 6.1 规模

| 类别 | 数量 | 说明 |
|---|---:|---|
| 通用算子（COMBO + REGULAR + SELECTION） | ~60 | add / multiply / subtract / power / signed_power / rank / zscore / winsorize / ts_* / group_* / if_else 等 |
| **仅 COMBO 可用** | ~42 | generate_stats / self_corr / reduce_* 全族 / combo_a / trade_when / hump / bucket / tail / densify 等 |
| **仅 SELECTION 可用** | 2 | `universe_size` / `in` |
| Selection 可用变量 | 25 + 18 | 25 个 Alpha 属性 + 18 个 `author_*` |

### 6.2 本轮实际用到的

| 层 | 已用 | 未用 |
|---|---|---|
| selection 变量 | `self_correlation`、`prod_correlation` | 其余 23 个 Alpha 属性 + **全部 18 个 `author_*`** |
| selection 算子 | `*` `+` `>`（multiply / add / greater） | `universe_size`、`in`、比较与逻辑族、if_else、power、signed_power 等 ~37 个 |
| combo 算子 | **`combo_a`**（1 个） | **~41 个**，含 generate_stats / self_corr / reduce_* 全族 / trade_when / hump / bucket / tail / zscore / winsorize / rank 等 |

**利用率**：combo 侧 **1/42 ≈ 2.4%**；selection 变量 2/43 ≈ **4.7%**；selection 算子 3/60 ≈ **5%**。

### 6.3 为什么多数算子"用不上"

1. **`combo_a` 是平台为 SA 专门设计的组合算子**（250 天窗口平衡收益/波动率），语义上已是最优组合，无需手工调权。
2. **`author_*` 18 个在自有池里是常数**（同一作者 = 我），对 selection 无区分力。
3. **`universe_size` 只在 selection 可用**：本轮各区组件 universe 单一（IND 全 TOP500、GBR 全 TOP700、KOR 全 TOP600、USA 全 TOP3000），区分度为 0。⇒ USA 有 2 个 universe（TOP2000/TOP3000）时可尝试。
4. **combo 侧其余 41 个算子**要么需要显式输入源（`generate_stats`/`self_corr`/`reduce_*` 在 combo 上下文中无隐式输入），要么用于 REGULAR alpha 的信号构建而非 SA 权重组合。

### 6.4 下一轮可探索

1. **`combo_a` 参数调优**：`nlength`（默认 250）和 `mode`（默认 'algo1'）——当前未测。
2. **多层 combo**：`combo_a(alpha)` 外再套 `zscore` / `winsorize` / `hump` 做权重后整形。
3. **selection 侧 `universe_size`**：在 USA（2 个 universe 有组件）做偏好宽/窄 universe 的加权。
4. **`reduce_*` 族在 combo 上的正确用法**：需先解决输入源问题（可能需 `generate_stats` + `reduce_max` 组合）。
5. **USA STAT 族 sub-universe Sharpe 修复**：`0mYko03p` 的 prod/self 双优（0.517/0.450），仅卡在 LOW_SUB_UNIVERSE_SHARPE（2.21 vs 2.47），换 selection 或调 truncation 可能修复。

---

## 7. 执行清单

### 7.1 复现命令（全部走 MCP，无临时脚本）

```bash
# ① 组件池 + 档位 + pyramid（MCP get_user_alphas / get_pyramid_multipliers）
# ② 建 SA（MCP create_simulation type=SUPER，combo="combo_a(alpha)"）
# ③ 双闸实测（MCP check_correlation refresh=True）
```

### 7.2 配额与并发约束

- SUPER **1/ET 日（账号级全局）**，与 REGULAR 4/ET 日/区独立计数；00:00 ET 重置。
- **prod 账号级单并发**：`check_correlation` 同账号同时只能跑一个（`correlation_busy` 返回 `retry_after`）。
- 单次 `create_simulation` 立即返回结果（IS 指标同步计算），无需等待。
- **prod PC 计算可能 >240s**：本轮 3 颗 USA alpha 均超时，需耐心重试（`check_correlation(refresh=True)`）。

### 7.3 推荐交付顺序（若用户点名提交）

| 顺序 | α id | Region | 余量 | 状态 | 备注 |
|---|---|---|---:|---|---|
| 1 | `O0Aw0Y7Y` | KOR/TOP600 | 0.142 | ✅ 新建 | 本轮最优，双闸全过 |
| 2 | `bl62YwRN` | IND/TOP500 | 0.136 | ✅ 新建 | CROWDING 族，双闸全过 |
| 3 | `6XdPxKN5` | USA/TOP3000 | 0.094 | ✅ 新建 | USA 复活首颗 |
| 4 | `MPYAOR0r` | GBR/TOP700 | 0.170 | ✅ 已提交 | 10-28 ACTIVE |
| 5 | `YP1d66KM` | EUR/TOPCS1600 | 0.101 | ⏳ 已建未提交 | 10-23 创建，可提交 |
| 6 | `3qoWQKJg` | KOR/TOP600 | 0.078 | ⏳ 已建未提交 | 10-22 创建，可提交 |

> ⚠ **SUPER 配额 = 1/ET 日全局**。当前（10-30 ET）配额可用，每日仅可提交 1 颗 SUPER，多颗需分日。
> ⚠ 提交前必做：再走一次 `check_correlation(refresh=True)`（铁律，台账 >48h 即不可信）。
> ⚠ 提交前先停掉后台 sa_run.py 批次：并发会加剧代理不稳，导致 `_probe_prod_max` 抛 ProxyError 中止。

### 7.4 下一轮候选动作

1. **MEA 扫描完成**：CROWDING / INDUSTRY 族（后台运行中）。
2. **USA STAT 族修复**：`0mYko03p` 换 selection 或调 truncation 试修 LOW_SUB_UNIVERSE_SHARPE。
3. **KOR STAT 族深扫**：`O0Aw0Y7Y` 余量 0.142，可试 l12/l15 梯度（组件数↑ ⇒ self↓ 但 prod↑，需找平衡点）。
4. **IND CROWDING 族深扫**：`bl62YwRN` 余量 0.136，同上。
5. **算子轴**：`combo_a` 参数调优（nlength/mode）、多层 combo 整形。
6. 不再扫：ASI（池不足）、GLB/DEU（prod 必炸）、USA CROWDING（prod 超标）。

---

## 8. 本轮 MCP 调用记录

| 步骤 | 工具 | 关键参数 | 结果 |
|---|---|---|---|
| 组件池 | `get_user_alphas` | stage=OS, type=REGULAR, status=ACTIVE | 10 区计数（USA 45 / IND 45 / KOR 30 / GBR 18 / MEA 19 / EUR 18 / GLB 17 / DEU 10 / ASI 9 / HKG 6） |
| SUPER 档位 | `get_user_alphas` | is_super=true, limit=100 | 41 颗全部 ACTIVE，跨 8 区 |
| Pyramid | `get_pyramid_multipliers` | — | 13 区完整倍率 |
| 算子 | `get_operators` | — | 103 个算子全量 |
| 建 SA ×12 | `create_simulation` type=SUPER | combo=`combo_a(alpha)` | 12 个 id（1 个 MEA 失败） |
| 双闸 ×12 | `check_correlation` refresh=true | production + self | 7 过 / 1 IS FAIL / 3 超标 / 1 MEA 失败 |
| USA prod 补测 | `check_correlation` refresh=true | akK2Jnm6 / 6XdPxKN5 / 0mYko03p | 0.708 FAIL / 0.607 PASS / 0.517 PASS |