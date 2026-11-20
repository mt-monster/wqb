# 各 Region 最优 SuperAlpha 方案 — 2026-11-18

> 工作流：清 api_cache(65 条) → `probe_sa_candidates --refresh` → 58 颗 ACTIVE SUPER 档位分类 → pyramid 倍率 →
> **30 条 SUPER 仿真（六批，2 并发成对）** → 2 颗 `refresh=True` 双闸 → 3 组互测 → 排序。
> **本轮未提交任何 alpha。** 全部动作在 `results/sa_scan_20261118/`。

> ⚠ **2026-11-18 09:50 判据更新**：本文档 §0.3 的排序口径（§5.5 字典序 + 三条件硬拦）已被
> [`docs/experience/01_platform_gates.md`](../docs/experience/01_platform_gates.md) §6.1「SA 提交准入分级」取代。
> 按新判据（ADMIT / REPORT / REDLINE / NO_EDGE / UNMEASURED）重判本轮 9 颗候选：
> **ADMIT 0 · REPORT 0 · REDLINE 3 · UNMEASURED 4 · NO_EDGE 2**。`E5QEZrl1` 由本文档「排序第一」降为
> **NO_EDGE**——F 6.51 虽高，S 5.02 低于区内最强 5.43×0.95=5.16，属横向替换而非升级。
> 分级明细见 `results/sa_scan_20261118/grade_out.md`，工具 `tools/super/sa_grade.py`。

---

## 0 执行摘要

### 0.1 池与档位（2026-11-18 06:3x 刷新）

| 区域 | REGULAR ACTIVE | ACTIVE SUPER | 变化 |
|---|---|---|---|
| USA | 52 | 11 | 池 51→52 |
| IND | 48 | 12 | — |
| KOR | 37 | 12 | — |
| GBR | 28 | 7 | **+1（`pwa8mYvV` 11-16 19:10 ET 提交）** |
| EUR | 28 | 5 | — |
| DEU | 22 | 2 | — |
| GLB | 19 | 5 | — |
| MEA | 19 | 2 | — |
| ASI | 10 | 2 | — |
| HKG | 7（BLOCKED，差 3） | 0 | — |

**SUPER ACTIVE 57 → 58**。唯一新增 = 上一轮排序第一 `pwa8mYvV`（GBR/TOP700 SLOW d3 l16 LC + `w²`，S5.05/F5.18/prod .6548）——用户已点名提交。

### 0.2 本轮结论

**唯一具边际的产出 = `E5QEZrl1`（IND/TOP500 INDUSTRY d1 l20，LC + `turnover<0.22`，combo `w³`）**

| 指标 | 值 | 三条件 |
|---|---|---|
| Sharpe | **5.02** | ✓（≥5，仅超 0.02） |
| Fitness | **6.51** | ✓（≥5，超 1.51） |
| Turnover | 0.1489 | — |
| prod_correlation | **0.6738** | ✗（>0.65，差 0.0238） |
| self_correlation | **0.6728** | ✓（<0.68） |
| IS checks | **9 PASS / 0 FAIL** | ✓ |

- 达成 **2 / 3**（S、F 达标；prod 差 0.0238）。这在本账户 58 颗 SUPER 里排得上前列（全账户仅 4 颗 3/3，全是已提交件）。
- **双闸实测**（2026-11-18 07:3x GMT+8，`refresh=True`）：prod **0.6738** / self **0.6728**，双 < 0.70 红线，0.68 余量闸余 **0.0062**（薄）。
- **区内边际成立**：F 6.51 > 该区现有最强 SUPER 的 F（`QPbjxMYw` 5.74，+0.77）。S 5.02 略低于区内最强 S（`pw52P3jb` 5.43）。
- **真独立席**：self top1 = `88vKp8Va` 0.6728（INDUSTRY d1 l10 已提交件），非既有席复制。

**本轮未能产出任何 3/3 件**，卡点全部是 prod，而不是 S/F（见 §6 元评估）。

### 0.3 本轮排序表（§5.5 字典序）

| 名次 | ID | ① IS 零 FAIL | ② 三条件达成度 | ③ 席位边际 | ④ prod 余量（0.68−prod） | 判定 |
|---|---|---|---|---|---|---|
| **1** | **`E5QEZrl1`** | ✓（0 FAIL） | **2/3**（S/F 达，prod 差 .0238） | **真独立席**（self top1 .6728 = `88vKp8Va`） | **0.0062** | **入表（唯一）** |
| ✗ | `d5axMLxx` | ✓ | 2/3 | 同席（与 `QPbjxMYw` ρ .7309） | **−0.0511** | 排除：prod .7311 > 0.70 红线 |
| ✗ | `6XMwkYJY` | ✓ | 1/3（S 4.99） | 同席（与 #1 ρ .9995） | 0.0002 | 排除：同席 + 余量过薄 |
| ✗ | `6XM9nYQY` | ✓ | 1/3（未测双闸） | 同席（与 #1 ρ **1.0000**） | — | 排除：同席 |
| — | 其余 26 条 | — | — | **未超区内最强 S 或 F ⇒ 无边际**，不进入排序 | — | 见 §1.2 |

⑤ Eff 未启用：①–④ 已唯一确定名次，无并列。

---

## 1 三条件达成矩阵

三条件 = `S ≥ 5 ∧ F ≥ 5 ∧ prod ≤ 0.65`；自设余量闸 `prod ≤ 0.68`、`self ≤ 0.68`。

### 1.1 本轮新建件（双闸 `refresh=True` 实测）

| # | ID | 区/档 | neut | d | l | selection | combo | S | F | TO | prod | self | 达成 | gap-to-{S5,F5,prod.65} |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **`E5QEZrl1`** | IND/TOP500 | INDUSTRY | 1 | 20 | LC + TO<.22 | w³ | **5.02** | **6.51** | .1489 | **.6738** | .6728 | **2/3** | +0.02 / +1.51 / **−0.0238** |
| 2 | `6XMwkYJY` | IND/TOP500 | INDUSTRY | 1 | 20 | LC + TO<.22 | w | 4.99 | 6.51 | .1465 | **.6798** | .6789 | 1/3 | −0.01 / +1.51 / −0.0298 |
| 3 | `6XM9nYQY` | IND/TOP500 | INDUSTRY | 1 | 20 | LC + TO<.22 | w² | 5.01 | 6.51 | .1481 | 未测（与 #1 ρ=**1.0000**，同席） | — | — | — |
| ✗ | `d5axMLxx` | IND/TOP500 | STATISTICAL | 1 | 20 | LC + TO<.22 | w | 6.14 | 7.57 | .1656 | **.7311 破线** | 未测 | 2/3 但闸死 | — |

> `6XMwkYJY`（w¹）prod .6798 与 `E5QEZrl1`（w³）ρ **0.9995**、与 `6XM9nYQY`（w²）ρ **1.0000** ⇒ **combo 幂次在本席已无自由度**，三颗只能取一。取 `E5QEZrl1`（S 最高、prod 最低）。

### 1.2 区内最强件对照（判「有无边际」的唯一依据）

| 区 | 现有最强 S | 现有最强 F | 已 3/3 颗数 | 本轮最佳新件 | 是否超区内最强 |
|---|---|---|---|---|---|
| USA | 6.39 `A1V0eZne` | 7.06 `A1V0eZne` | **1** | `KPgboEez` 4.61 / 4.15 | ✗ 无边际 |
| IND | 5.43 `pw52P3jb` | 5.74 `QPbjxMYw` | **2** | `E5QEZrl1` 5.02 / **6.51** | ✓ **F +0.77** |
| KOR | 5.96 `KPg60XNp` | 7.50 `KPg60XNp` | **1** | `qM7lKoYj` 5.11 / 6.72 | ✗ 无边际（双项均低） |
| GBR | 5.05 `pwa8mYvV` | 5.18 `pwa8mYvV` | 0 | `6XMwW3W5` 4.12 / 4.13 | ✗ 无边际 |
| EUR | 6.54 `E5Q7RGNR` | 4.69 `Wjl6JJQO` | 0 | `6XMw6Map` 3.29 / 2.95 | ✗ 无边际（基线已漂移） |
| GLB | 6.93 `LL5amzov` | 4.18 `LL5amzov` | 0 | `vRAJe0mr` 6.25 / 3.45 | ✗ 无边际 |
| DEU | 3.27 `vR1oxZA3` | 3.09 `vR1oxZA3` | 0 | 本轮未派 | — |
| MEA | 2.52 `78jYpn0Z` | 2.99 `78jYpn0Z` | 0 | 本轮未派 | — |
| ASI | 5.38 `d5WGG5bg` | 2.99 `d5WGG5bg` | 0 | 本轮未派（F 数学不可达，见 §6.3） | — |

---

## 2 四轴扫描矩阵（本轮 30 条仿真全表）

> 这是「配方轴被扫过」的唯一凭据。`sel` 列：`base` = 默认 `(0.7−prod)`；`lc*` = `long_count` 主键 + TO 上限；`to*` = 默认主键 + TO 上限。`F/S` = `√(R/TO)`，见 §6.1。

| 区 | neut | d | limit | selection | combo | S | F | TO | prod | F/S |
|---|---|---|---|---|---|---|---|---|---|---|
| IND | STATISTICAL | 1 | 14 | lc（TO<.6） | w | 6.10 | 5.96 | .2975 | — | 0.977 |
| IND | STATISTICAL | 1 | 14 | lc + TO<.22 | w | 5.74 | 7.08 | .1515 | — | 1.233 |
| IND | STATISTICAL | 1 | 16 | lc + TO<.22 | w | 5.96 | 7.38 | .1604 | — | 1.238 |
| **IND** | STATISTICAL | 1 | **20** | lc + TO<.22 | w | **6.14** | **7.57** | .1656 | **.7311** | 1.233 |
| IND | STATISTICAL | 1 | 24 | lc + TO<.22 | w | 6.07 | 7.43 | .1680 | — | 1.224 |
| IND | STATISTICAL | 1 | 28 | lc + TO<.22 | w | 6.25 | 7.29 | .1961 | — | 1.166 |
| IND | STATISTICAL | 5 | 20 | base + TO<.18 | w | 4.15 | 4.77 | .0982 | — | 1.149 |
| IND | INDUSTRY | 1 | 20 | base（TO<.5） | w | 4.48 | 4.13 | .3130 | — | 0.922 |
| IND | INDUSTRY | 1 | 16 | lc + TO<.22 | w | 4.95 | 6.47 | .1453 | — | 1.307 |
| **IND** | INDUSTRY | 1 | **20** | lc + TO<.22 | w³ | **5.02** | **6.51** | .1489 | **.6738** | 1.297 |
| IND | INDUSTRY | 1 | 20 | lc + TO<.22 | w² | 5.01 | 6.51 | .1481 | — | 1.299 |
| IND | INDUSTRY | 1 | 20 | lc + TO<.22 | w | 4.99 | 6.51 | .1465 | .6798 | 1.305 |
| IND | INDUSTRY | 1 | 20 | lc + TO<.26 | w | 4.97 | 6.23 | .1626 | — | 1.254 |
| IND | INDUSTRY | 1 | 24 | lc + TO<.22 | w | 4.86 | 6.47 | .1392 | — | 1.331 |
| IND | INDUSTRY | 1 | 28 | lc + TO<.22 | w | 4.86 | 6.47 | .1392 | — | 1.331 |
| IND | INDUSTRY | 2 | 20 | lc + TO<.22 | w | 4.85 | 6.59 | .1305 | — | 1.359 |
| IND | INDUSTRY | 1 | 24 | lc + TO<.18 | w | 3.75 | 4.51 | .0941 | — | 1.203 |
| IND | INDUSTRY | 1 | 28 | lc + TO<.18 | w | 3.75 | 4.51 | .0941 | — | 1.203 |
| IND | SLOW | 1 | 20 | lc + TO<.22 | w | 4.49 | 4.25 | .1946 | — | 0.947 |
| IND | SLOW | 1 | 24 | lc + TO<.22 | w | 4.36 | 4.12 | .1899 | — | 0.945 |
| IND | REVERSION_AND_MOMENTUM | 1 | 20 | lc + TO<.22 | w | 4.60 | 4.98 | .1766 | — | 1.083 |
| IND | SUBINDUSTRY | 10 | 20 | lc + TO<.22 | w | 4.13 | 5.22 | .0959 | — | 1.264 |
| KOR | SLOW | 1 | 30 | lc + TO<.15 | w | 4.94 | 6.41 | .1365 | — | 1.298 |
| KOR | SLOW | 1 | 30 | lc + TO<.13 | w | 5.11 | 6.72 | .1345 | — | 1.315 |
| GBR | SLOW | 3 | 16 | lc + TO<.14 | w | 4.12 | 4.13 | .1086 | — | 1.002 |
| GBR | SLOW | 5 | 14 | lc + TO<.14 | w | 4.09 | 4.06 | .1022 | — | 0.993 |
| GLB | STATISTICAL | 1 | 10 | lc（无 TO 上限） | w | 6.25 | 3.45 | .3321 | — | 0.552 |
| GLB | STATISTICAL | 1 | 10 | lc + TO<.20 | w | 5.68 | 3.87 | .1457 | — | 0.681 |
| GLB | STATISTICAL | 1 | 10 | base（默认） | — | **建单失败**：<10 成分 | — | — | — | — |
| GLB | STATISTICAL | 1 | 10 | lc + TO<.15 | — | **建单失败**：<10 成分 | — | — | — | — |
| USA | SLOW | 1 | 10 | base + TO<.12 | w | 4.61 | 4.15 | .1091 | — | 0.900 |
| EUR | SUBINDUSTRY | 1 | 10 | base（默认） | w | 3.29 | 2.95 | .1040 | — | 0.897 |

**轴覆盖度**：
- ① selection 主键：`long_count`（22 条）/ 默认 `(0.7−prod)`（4 条）/ **`long_count` + TO 上限（新，14 条）**
- ② limit：IND 14/16/18/20/24/28（六档，S 峰值 l20-l28，F 峰值 l20）；GLB 10；GBR 14/16；KOR 30
- ③ combo：w¹ / w² / w³（IND 同一席三点，ρ 1.0000 ⇒ **该轴已无自由度**）
- ④ 中性化族：IND 五族（STAT / INDUSTRY / SLOW / R&M / SUBINDUSTRY）；GLB / GBR / USA / EUR 单一最强族 + 0 异族（按 §0 铁律④不穷举）

---

## 3 互测矩阵（本地 `compute_mutual_correlation`，不占相关性槽）

### 3.1 本轮产出件 × IND 现有 12 颗 SUPER

| | d5axMLxx | E5QEZrl1 | 6XMwkYJY | QPbjxMYw | wpjrMnz5 | 88vKp8Va | MPaGzEx8 | 3qoG6nEe | pw52P3jb | wpbQjeKp |
|---|---|---|---|---|---|---|---|---|---|---|
| **d5axMLxx** | 1 | — | — | **.7309** | .6896 | .5289 | .5206 | .4508 | .3791 | .6208 |
| **E5QEZrl1** | — | 1 | .9995 | .5663⭑ | .5381⭑ | **.6728**⭑ | .6382⭑ | — | — | — |
| **6XMwkYJY** | .798 | .9995 | 1 | .5668 | .5386 | .6789 | .6432 | .4120 | — | — |

⭑ = `check_correlation(self)` 返回的 top5（`E5QEZrl1`）。

**判读**：
- `d5axMLxx` 的 prod **0.7311 ≈ 与自有 `QPbjxMYw` 的 ρ 0.7309**（逐位吻合）⇒ 该件即 `QPbjxMYw` 同席，prod 墙 = 自我拥挤。
- IND STAT 六档 LC 件（l14/l16/l20/l24/l28）互测 ρ .864–.970，与 `QPbjxMYw` 全在 **.732–.770** ⇒ **整族同席，全灭**。
- `E5QEZrl1` 与全池最大 ρ 0.6728（`88vKp8Va`）⇒ **真独立席**，但该 ρ 同时构成其 prod 下界。

---

## 4 分 Region 方案

### 4.1 IND / TOP500 — 唯一可行区（本轮推荐）

**最优配方**

```
settings : region=IND universe=TOP500 delay=1 decay=1 neutralization=INDUSTRY
           truncation=0.02 selectionHandling=POSITIVE selectionLimit=20
selection: if_else(is_nan(long_count), 1, long_count)
           * (self_correlation < 0.7) * (turnover > 0.01) * (turnover < 0.22)
combo    : stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500);
           ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic);
           w = 1 - maxCorr; w*w*w
```

**预期指标**（`E5QEZrl1` 本轮实测）：S 5.02 / F 6.51 / TO .1489 / R .2502 / DD .0284 / margin .00336
**双闸**：prod **0.6738**、self **0.6728**（2026-11-18 07:3x，refresh=True）→ 余量 prod **0.0062** / self 0.0072（**薄**）
**IS checks**：9 PASS / 0 FAIL（`MATCHES_COMPETITION` WARNING，全账户通用）
**辅助**：sub_universe 2.79 / 2Y 4.97 / robust 2.28 / investability 3.80

**为什么是 INDUSTRY 而不是 STATISTICAL**：STAT 族 S 更高（6.14 vs 5.02）但已与 `QPbjxMYw` 同席（ρ .73）；INDUSTRY 族 F 更高且席位独立。**STAT 的 S 优势无法兑现，是 prod 决定的，不是 S 决定的。**

### 4.2 其他区：本轮无边际（详见 §5）

---

## 5 撞墙档案（按死因归类）

### 5.1 prod 硬闸（本轮 3 例，全部为自我拥挤）

| 件 | 表面指标 | prod | 真正对手 | 结论 |
|---|---|---|---|---|
| `d5axMLxx` IND STAT l20 | S6.14 / F7.57（区最强） | **.7311** | 自有 `QPbjxMYw` ρ .7309 | 同席，闸死 |
| `A1xOakkY` GBR SLOW l16 | 上轮 .6621 | **.9993** | 自有 `pwa8mYvV`（同配置 w²） | **GBR 该席彻底封死** |
| `E5QEZrl1` IND INDUSTRY l20 | S5.02 / F6.51 | .6738 | 自有 `88vKp8Va` ρ .6728 | 过闸但余量仅 .0062 |

**★ 新实证（GBR 同席判定的判决性证据）**：`pwa8mYvV`（w²）11-16 提交后，`A1xOakkY`（同配置 w¹）prod 从 **0.6621 → 0.9993**。同一组件集合、仅 combo 幂次不同，提交一颗即把兄弟件推到 ρ≈1。⇒ **GBR/TOP700 l16 LC 席只有一颗，已用掉。**

### 5.2 池质量问题（S 天花板）

| 区 | 本轮最佳 | 区内最强 | 结论 |
|---|---|---|---|
| GBR | 4.12/4.13 | 5.05/5.18 | `turnover<0.14` 上限砍掉一半成分，S 掉 0.9 ⇒ GBR 成分池里低换手的都是弱信号 |
| EUR | 3.29/2.95 | 6.54/4.69 | **基线漂移**：同配置（SUBIND d1 l10 默认）历史 6.13 → 本轮 3.29 |
| GLB | 6.25/3.45 | 6.93/4.18 | S 够但 F 不可达（§6.2） |
| KOR | 5.11/6.72 | 5.96/7.50 | TO 上限在 KOR 只把 F/S 从 1.258 抬到 1.315（+4.5%），S 反降 0.85 |
| USA | 4.61/4.15 | 6.39/7.06 | `turnover<0.12` 上限过紧，S 掉 1.78 |
| DEU | 未派 | 3.27/3.09 | S 天花板 3.3，三条件数学不可能（需 S×1.53） |
| MEA | 未派 | 2.52/2.99 | 同上（平台已下架，不可新建） |
| ASI | 未派 | 5.38/2.99 | §6.3 证明 F≥5 数学不可达 |

### 5.3 建单失败（结构，非偶发）

| 组合 | 报错 | 判读 |
|---|---|---|
| `GLB/MINVOL1M` + 默认 selection（4 条：l10 d1/d3/TO<.20） | `At least 10 component alphas are required` | **GLB 成分池无 `prod_correlation` 值** ⇒ `(0.7−prod)` 全 NaN ⇒ 选中 0 颗 |
| `GLB/MINVOL1M` + `LC + TO<.15` | 同上 | 19 颗池里 TO<.15 的不足 10 颗 |
| `GBR/TOP700` + `LC + TO<.12` | 同上 | 28 颗池里 TO<.12 的不足 10 颗（TO<.14 可建） |
| `GLB/MINVOL1M` + 无 prod 项 selection | `Failed to create simulation / None` | 并发抖动，非配方问题（未重试，价值低） |

---

## 6 元评估：卡在哪一轴、需要什么外部条件

### 6.1 ★★★ 本轮唯一真发现：`F/S ≡ √(R/TO)` 是**成分集合属性**，只有 selection 层的 TO 上限能改它

30 条仿真逐条验证恒等式 `F/S = √(R/max(TO,0.125))`，**误差 ≤0.001，30/30 成立**：

| 配置 | S | F | TO | R | F/S | √(R/TO) |
|---|---|---|---|---|---|---|
| IND STAT l14，无 TO 上限 | 6.10 | 5.96 | .2975 | .2838 | 0.977 | 0.977 |
| IND STAT l20，**TO<.22** | 6.14 | 7.57 | .1656 | .2515 | **1.233** | 1.232 |
| IND INDUSTRY l20，默认 selection | 4.48 | 4.13 | .3130 | .2666 | 0.922 | 0.923 |
| IND INDUSTRY l20，**TO<.22** | 4.99 | 6.51 | .1465 | .2491 | **1.305** | 1.304 |
| KOR SLOW l30（= `KPg60XNp` 同族） | 5.96 | 7.50 | .1729 | .2737 | 1.258 | 1.258 |
| KOR SLOW l30，**TO<.13** | 5.11 | 6.72 | .1345 | .2327 | 1.315 | 1.315 |

**结论**：
- 过去 20 轮反复用的 decay / `maxTrade` / combo 时序平滑**都不可能改 F/S** —— 它们等比例压低 R 与 TO，比值不变（这也解释了 11-17 `maxTrade=ON` 为何"TO 降了但 F 反而降"）。
- **selection 层加 `turnover < X` 会换掉成分集合**，挑进来的低换手 alpha 天然有更高的 `R/TO` ⇒ **F/S 提升 26%–41%**（IND 实测），KOR 只有 +4.5%（该区低 TO 成分质量差）。
- 这是 `A1V0eZne`（USA，`turnover<0.22`，F/S = 7.06/6.39 = 1.105，全账户最高）配方第一次被**跨区复现并量化**。此前 6 轮把它当个案，没意识到它是 F 的唯一杠杆。

### 6.2 prod 是唯一真瓶颈，且 100% 由自有 BOOK 决定

本轮 3 次 prod 实测，3 次都精确等于「与某颗自有已提交件的 ρ」：

| 件 | prod 实测 | 自有对手 | 互测 ρ |
|---|---|---|---|
| `d5axMLxx` | 0.7311 | `QPbjxMYw` | 0.7309 |
| `A1xOakkY` | 0.9993 | `pwa8mYvV` | （同配置 w²） |
| `E5QEZrl1` | 0.6738 | `88vKp8Va` | 0.6728 |

**prod 无法通过配方轴降低**：IND INDUSTRY 族 prod 下界 = `88vKp8Va`（INDUSTRY d1 l10，prod .6753）的 .6728；要破 .65 必须离开该族，而离开该族 S 掉到 4.13–4.60（SUBIND 4.13 / RM 4.60 / SLOW 4.49）⇒ **S 与 prod 在 IND 是硬交换，无中间点**。

### 6.3 各区突破所需的外部条件（不接受"继续观察"）

| 区 | 当前缺口 | 突破所需的**具体外部条件** | 配方侧是否还有余地 |
|---|---|---|---|
| **IND** | prod .6738 → 需 ≤.65（差 .0238） | 池新增 1–2 颗 **INDUSTRY 族** REGULAR，且与 `88vKp8Va` 的 ρ < 0.4；或 `88vKp8Va` 自带衰减（OS 到期/被 supersede） | 否（族内已扫 5 族 × 6 limit × 3 combo，全表见 §2） |
| **GBR** | 需 S > 5.05 或 F > 5.18，且 prod < .68 | `pwa8mYvV` 席位已被自身占满（兄弟件 ρ .9993）；只能等 GBR 池新增与 `3qompGeZ`/`pwa8mYvV` 双低相关的成分 | 否（LC 主键 + TO 上限双向都试过，S 掉到 4.12） |
| **GLB** | F 4.18 → 需 ≥5，即 TO 需 −33% | **平台侧：GLB 成分的 `prod_correlation` 必须重新有值**（现在缺失 ⇒ 默认 selection 建不出单）；否则只能靠 LC 建单，而 LC 的 TO 是 .33 | 否（TO<.15 直接成分<10） |
| **EUR** | S 6.54 → 本轮同配置只能跑出 3.29 | 池重建：28 颗 EUR REGULAR 需重新筛选（当前成分与 8 月/11-13 的 6.13–6.54 成分已非同一批） | 否（本轮连基线都复现不了） |
| **KOR** | S 5.96 / F 7.50 已是账户前二 | 需 S > 5.96 且 prod ≤ .65；TO 上限只能把 F 抬 +4.5% 不能抬 S | 否 |
| **USA** | S 6.39 / F 7.06 | 需超 `A1V0eZne`；TO<.12 实测 S 4.61（过紧），TO<.22 是其原始配方已用尽 | 否 |
| **ASI** | F 2.99 → 需 ≥5 | **数学不可能**：F=5 需 `R/TO ≥ (5/5.38)²=0.864`，即 TO ≤ .0903/.864 = **.1045 < 平台 .125 下限**；ASI 池恰好 10 颗（TO 上限必破 10 颗下限） | 否（双重硬约束） |
| **DEU / MEA** | S 3.27 / 2.52 | 需 S×1.5 以上，池质量决定；MEA 平台已下架不可新建 | 否 |

### 6.4 本轮方法学修正（写回流程）

1. **§0 四轴排序要改**：`④ 中性化族` 仍为 0 增益（本轮 IND 五族对照再次确认：STAT 6.14 / INDUSTRY 5.02 / RM 4.60 / SLOW 4.49 / SUBIND 4.13，差异来自成分集合而非"族效应"）。但 **`① selection` 内部要拆成两个独立子轴**：主键（`long_count` vs `1−prod`）× **换手上限**（.6 / .22 / .18 / .15 / .13 / .12）。后者是本轮唯一有效的新杠杆。
2. **`② limit` 的峰值位置要按主键分别定**：IND STAT 在 l20–l28 平顶，IND INDUSTRY 在 l20 见顶后**回落**（l24 = l28 = 4.86，且两档逐位相同 ⇒ 该 filter 后候选恰好 ~24 颗，limit 已饱和）。
3. **GLB 的"默认 selection 建不出单"要写进停投理由**，不能写"prod 墙"——它是成分池数据缺失，性质不同。

---

## 7 提交建议（只写建议，不执行）

### 7.1 建议对象

| 顺位 | ID | 区 | prod / self（本轮实测） | IS FAIL | 与同档 SUPER 互测 ρ | 3/3 | 备注 |
|---|---|---|---|---|---|---|---|
| **#1** | **`E5QEZrl1`** | IND/TOP500 | **.6738 / .6728** | **0** | max .6728（`88vKp8Va`）= 新席 | 2/3 | 唯一具边际件；prod 余量仅 .0062 |
| #2 | — | — | — | — | — | — | 本轮无第二个具边际的独立席 |
| #3 | `6XMwkYJY` | IND/TOP500 | .6798 / .6789 | 0 | 与 #1 ρ **.9995** = 同席 | 1/3 | 仅作 #1 的等效备胎（同席不能叠加） |

**不建议提交 `d5axMLxx`**（S6.14/F7.57 账面最强）：prod 0.7311 > 0.70 合规红线，无豁免。

### 7.2 前置条件核对（逐条）

| 条件 | `E5QEZrl1` 状态 |
|---|---|
| `prod ≤ 0.68` | ✓ 0.6738（余量 0.0062，**薄**） |
| `self ≤ 0.68` | ✓ 0.6728（余量 0.0072） |
| IS checks 零 FAIL | ✓ 9 PASS / 0 FAIL |
| 台账 `robustness_<id>` 无 REJECT | ✓ 新件，无台账记录（非 REJECT） |
| 与同档已有 SUPER 互测 ρ < 0.7 | ✓ 最大 0.6728（`88vKp8Va`） |

### 7.3 配额

- `SUPER_SUBMISSION`：**1 颗 / ET 日历日 / 账户级**，00:00 ET 重置 = GMT+8 13:00。
- 当前 ET 日 = **2026-11-17**（`wqb.timeutil.et_today()`，实测 17:3x ET）。
- 本 ET 日 SUPER 配额：**未使用**（末次 SUPER 提交 = `pwa8mYvV`，ET **2026-11-16** 19:10）。
- ⇒ 若用户此刻点名，可立即提交；13:00 GMT+8 之后重置为下一个 ET 日，同样可用。

### 7.4 命令模板（只写，不跑）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit --alpha-id E5QEZrl1 --region IND
```

### 7.5 两个提交坑

1. **提交前停掉后台批次**：并发会让 `super_build.py submit` 的 `_probe_prod_max` 抛 ProxyError（本轮无后台批次在跑，安全）。
2. **prod 槽有冷却**：`logs/_dblock/correlation.cooldown.json`，平台侧真算 180–200s。本轮 prod 实测在 07:3x 完成，提交前若需复测须等冷却归零。

### 7.6 薄余量风险提示

`E5QEZrl1` 的 prod 余量 **0.0062** 属于「过闸但不抗漂移」级别（历史上 `gJWdxLbM` 曾 48h 内漂 +0.068）。若用户决定提交，**建议提交前再跑一次 `refresh=True` 复测**（本建议中不预跑，留待用户指令）。

---

## 8 算子利用率审计（按「是否有增益」分类，不按覆盖率）

| 算子 | 位置 | 本轮用量 | 增益判定 | 证据 |
|---|---|---|---|---|
| **`turnover`（作上限）** | SELECTION | 14/30 条 | **★★★ 强正增益（本轮唯一）** | F/S：IND STAT 0.977→1.233（+26%）、IND INDUSTRY 0.922→1.305（+41%）、KOR 1.258→1.315（+4.5%） |
| `long_count` | SELECTION（主键） | 22/30 条 | **★★ 必要条件** | 同 neut 同 limit：LC 6.14 vs 默认主键 IND INDUSTRY 4.48（此项受 neut 混淆，但 IND STAT 的 S 峰值只能由 LC 达到） |
| `prod_correlation` | SELECTION | 5/30 条 | **★ 负增益（GLB 阻断）** | GLB 成分池该字段缺失 ⇒ `(0.7−prod)` 全 NaN ⇒ 选中 0 颗 ⇒ 建单失败 |
| `self_correlation` | SELECTION（门控） | 30/30 条 | 中性 | 只作硬门控，取值 0.55/0.7 未见指标差异 |
| `is_nan` | SELECTION | 22/30 条 | 中性 | 只防 NaN 传播，不改指标 |
| `self_corr` + `reduce_max` | COMBO | 30/30 条 | 中性（已饱和） | combo 换 `w¹/w²/w³` 三档 ρ **1.0000**，指标差 ≤0.03 |
| `w` 幂次 | COMBO | w¹ 27 / w² 2 / w³ 1 | 微正（≤+0.03 S） | IND INDUSTRY 4.99→5.02（跨过 5.0 线，价值在此） |

**结论**：本轮新增有效算子 **1 个**（`turnover` 作 selection 上限）。官方 SA 可用算子 160 个，本工作区累计用过 ~15 个（9.4%），但**覆盖率与产出无关**——真正的杠杆是「用 `turnover` 改变成分集合」，而不是"多用几个算子"。

---

## 9 本轮动作清单

| 动作 | 数量 | 结果 |
|---|---|---|
| 清 api_cache | 65 条 | — |
| 池盘点 `--refresh` | 1 次 | 9 区 GO / HKG 7 颗 BLOCKED |
| ACTIVE SUPER 分类 | 58 颗 | 18 个 region+universe 档位 |
| pyramid 倍率 | 9 区 | 仅记录（SA 不参与塔计数） |
| SUPER 仿真 | 派发 **37 条**（6 批） | **30 条出数** / 7 条建单失败（6 × 成分<10 + 1 × `Failed to create simulation`） |
| 双闸 `refresh=True` | 2 颗 | `d5axMLxx` .7311 FAIL / `E5QEZrl1` .6738 PASS / `6XMwkYJY` .6798 PASS（3 颗实测） |
| 互测 `compute_mutual_correlation` | 3 组（21 颗次） | 识别同席 3 组 |
| 提交 | **0** | — |
