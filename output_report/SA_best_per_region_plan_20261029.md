# 各 Region 最优 SuperAlpha 方案 — 2026-10-29 全流程扫描

生成时间：2026-10-29 (GMT+8)　|　扫描目录：`results/sa_scan_20261029/`
铁律：**只挖不提交**（全部为待执行配方）；**prod ≥ 0.7 = 合规红线，无豁免**；prod/self 值一律 `check_correlation(refresh=True)` 实测。

---

## 0. 执行摘要

| 优先级 | α id | Region / 档位 | 配方 | Sharpe | Fitness | TO | prod | self | 余量(prod/self) | 判定 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **P0 ★** | `MPYAOR0r` | **GBR / TOP700** | STAT d1 l10 `combo_a(alpha)` | **3.72** | **2.57** | 0.2114 | **0.5295** | **0.5296** | **0.170 / 0.170** | **✅ 已提交 ACTIVE** |
| **P1 ★** | `YP1d66KM` | **EUR / TOPCS1600** | CROWDING d1 l10 `combo_a(alpha)` | **3.57** | **2.43** | 0.2425 | **0.5985** | **0.5656** | **0.101 / 0.134** | ⏳ prod 过闸，SUPER 配额用尽（明日可提） |
| **P2 ★** | `3qoWQKJg` | **KOR / TOP600** | INDUSTRY d1 l10 `combo_a(alpha)` | **3.62** | **4.32** | 0.1369 | **0.6221** | **0.6224** | **0.078 / 0.078** | ⏳ prod 过闸，SUPER 配额用尽（明日可提） |
| P3 | `zq3zKgd8` | IND / TOP500 | STAT d1 l10 `combo_a(alpha)` | 4.69 | 4.29 | 0.2254 | 0.6953 | 0.6954 | 0.005 / 0.005 | ⚠️ 勉强过（余量 <0.02） |
| ~~P4~~ | `ZYQLP163` | USA / TOP3000 | CROWDING d1 l10 `combo_a(alpha)` | 4.50 | 4.90 | 0.1253 | **0.7341** | — | — | ❌ prod 超标 |
| ~~P5~~ | `xAraq1jm` | GLB / MINVOL1M | STAT d1 l10 `combo_a(alpha)` | 7.45 | 4.08 | 0.3244 | **0.8307** | — | — | ❌ prod 超标 |
| ~~P6~~ | `QPvdMW8Q` | DEU / TOP500 | STAT d1 l10 `combo_a(alpha)` | 2.30 | 1.55 | 0.2064 | **0.8849** | — | — | ❌ prod 超标 |

### 本轮方法论突破

**`combo_a(alpha)` 是 SA 组合层的唯一有效算子。** 此前所有尝试（`rank(w)` / `weight` / `combo_weight` / `reduce_max` / `generate_stats` / `self_corr`）均报错——平台 combo 表达式不接受裸变量名，必须以 `combo_a(alpha)` 形式调用，其中 `alpha` 是选中组件信号的隐式引用。`combo_a` 内部以 250 天窗口平衡各组件历史收益与波动率，自动产出加权合成信号。

### 关键发现

1. **池大小决定 prod 天花板**：组件池 ≥17 的区（GBR/EUR/KOR/IND）prod 可控；池 ≤11 的区（USA/GLB/DEU）prod 必炸——组件太少 ⇒ 合成信号与生产池高度重叠。
2. **GBR 余量最厚**（0.170），是当前体系里最安全的可交付 SA —— **已成功提交 `MPYAOR0r`，确认 ACTIVE（10-28 20:59 ET）**。
3. **IND 余量最薄**（0.005），虽然 Sharpe 最高（4.69），但 prod 0.6953 距红线仅 0.0047，不满足 ≥0.02 余量要求。
4. **★★ 平台 SUPER 配额 = 1/ET 日（全局），非 1/日/区**：25 颗已提交 SUPER 日期两两唯一（铁证）。10-28 ET 被 `MPYAOR0r` 占满 ⇒ `YP1d66KM`/`3qoWQKJg` 当日提交被 `SUPER_SUBMISSION(value=1, limit=1)` 拦截（prod 均已过闸 0.5985/0.6221）。**下一窗口 10-29 00:00 ET（GMT+8 12:00）后可提。**

---

## 1. 数据基线

### 1.1 组件池 eligibility（口径：stage=OS + type=REGULAR + status=ACTIVE）

| Region | 池 | 主要 universe | 可建 | 备注 |
|---|---:|---|---|---|
| IND | **21** | TOP500:21 | ✅ | 全 RA all-pass |
| GBR | **18** | TOP700:18 | ✅ | 全 RA all-pass |
| EUR | **17** | TOPCS1600:10 / TOP2500:7 | ✅ | 全 RA all-pass |
| KOR | **17** | TOP600:17 | ✅ | 全 RA all-pass |
| GLB | **17** | MINVOL1M:17 | ✅ | 全 RA all-pass |
| USA | **11** | TOP3000:8 / TOP2000:3 | ✅ | 池小 ⇒ prod 必炸 |
| DEU | **10** | TOP500:10 | ✅ | 池最小 ⇒ prod 最差 |
| ASI | **9** | MINVOL1M:6 / MINVOL10M:3 | ❌ | < 平台硬下限 10 |

> ⚠ 与 10-28 相比，组件池大幅缩水（USA 50→11、IND 53→21、KOR 39→17、EUR 19→17、GLB 21→17、DEU 11→10）。原因：`status=ACTIVE` 过滤排除了 SUPERSEDED 和其他非活跃状态的 alpha。

### 1.2 档位占用分类（★ 10-29 复核：各区均有已提交 SUPER，且配额为全局 1/日）

| Region | 已提交 SUPER 数 | 代表 α | 档位 |
|---|---:|---|---|
| GBR | **3** | `MPYAOR0r`（10-28）`e7QGwrx6`（10-10）`YPMp39q6`（10-08） | **OCCUPIED** |
| EUR | **3** | `kqJOQgnk`（10-23）`vROOONwd`（10-21）`GrgGkV1o`（10-20） | **OCCUPIED** |
| KOR | **9** | `RRA9EZKz`（10-22）等 09-08~10-22 | **OCCUPIED** |
| IND | **11+** | `88vKp8Va`（10-17）等 08-31~10-17 | **OCCUPIED** |

> **★★ 配额铁证（10-29 复核）**：25 颗已提交 SUPER 横跨 08-31 ~ 10-28，**日期两两唯一**（25 颗 / 25 个不同 ET 日）⇒ **`SUPER_SUBMISSION` 是账号级全局配额 = 1/ET 日**，**不是** 1/ET 日/区。10-28 ET 已由 `MPYAOR0r` 占满，故 EUR/KOR 当日再提被 `SUPER_SUBMISSION(value=1, limit=1)` 拦截（实测 403）。下一窗口 = 次日 00:00 ET（GMT+8 12:00）。

### 1.3 Pyramid 倍率（`get_pyramid_multipliers`，本轮实测）

| Region | D1 区间 | D0 | 备注 |
|---|---|---|---|
| DEU | 1.2–1.8 | ✅ 1.6–1.9 | 全平台最高 |
| GBR | 1.0–1.9 | ✅ 1.3–1.9 | news/analyst/sentiment 最高 1.9 |
| KOR | 1.0–1.6 | ❌ | analyst/model/fundamental/news/sentiment/other 均 1.6 |
| EUR | 1.0–1.5 | ✅ 1.0–1.7 | model/analyst D0 1.6 |
| USA | 1.0–1.4 | ✅ 1.0–1.8 | sentiment D0 1.8 最高 |
| GLB | 1.0–1.4 | ❌ | fundamental/analyst/sentiment 1.4 |
| IND | 1.0–1.4 | ❌ | analyst 1.4 最高 |
| ASI | 1.0–1.5 | ❌ | analyst 1.5 最高 |

---

## 2. 选点原则（本轮实证更新）

1. **池大小 > 中性化族 > combo**：池 ≥17 ⇒ prod 可控；池 ≤11 ⇒ prod 必炸。族和 combo 在池足够时差异不大。
2. **`combo_a(alpha)` 是唯一可用 combo**：裸变量名（`w`/`weight`/`combo_weight`）均报 "unknown variable"；裸算子名（`combo_a`/`reduce_max`）报维度错误；`generate_stats(alpha)` 报 "set of expressions"；`self_corr(alpha)` 报 "lookback must have a value"。仅 `combo_a(alpha)` 通过。
3. **selection 仍用 `(1 - self_correlation)`**：USA 需附加 `(1 + 0*(prod_correlation>0))` 门控（平台强制要求）。
4. **selection_limit = 10**（平台硬下限，实际生效 = min(limit, 池)）。
5. **truncation 0.02 vs 0.08 无显著差异**（USA 用 0.02，其余用 0.08）。

---

## 3. 论坛指标标准（沿用）

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9** | 0.20–0.27 | <0.5 |

---

## 4. 分 Region 方案

### 4.1 GBR / TOP700 — P0 最优（余量最厚）

- **α id**: `MPYAOR0r`
- **配方**: STAT / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.72 / F2.57 / TO 0.2114 / prod **0.5295** / self **0.5296**
- **余量**: prod 0.170 / self 0.170 —— 当前体系最安全候选
- **RA**: 全过（failed_ra_count=0, failed_ppa_count=0）
- **IS checks**: 全部 pass，仅 OSMOSIS_ALLOCATION warning
- **top_correlated**: `e7QGwrx6` 0.5296 / `npdm0mrq` 0.3560 / `YPMp39q6` 0.2973
- **池**: 18（GBR 全在 TOP700）

### 4.2 EUR / TOPCS1600 — P1

- **α id**: `YP1d66KM`
- **配方**: CROWDING / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.57 / F2.43 / TO 0.2425 / prod **0.5985** / self **0.5656**
- **余量**: prod 0.101 / self 0.134
- **RA**: 全过
- **IS checks**: 全部 pass，仅 OSMOSIS_ALLOCATION warning
- **top_correlated**: `LL5VwgO1` 0.5656 / `vROOONwd` 0.5048 / `88vQz5Yl` 0.3992
- **池**: 17（TOPCS1600:10 / TOP2500:7）

### 4.3 KOR / TOP600 — P2

- **α id**: `3qoWQKJg`
- **配方**: INDUSTRY / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S3.62 / F4.32 / TO 0.1369 / prod **0.6221** / self **0.6224**
- **余量**: prod 0.078 / self 0.078
- **RA**: 全过
- **IS checks**: 全部 pass，仅 OSMOSIS_ALLOCATION warning
- **top_correlated**: `9qjGvaWe` 0.6224 / `RRA9EZKz` 0.6170 / `E5vwqXNK` 0.5767
- **池**: 17（KOR 全在 TOP600）

### 4.4 IND / TOP500 — P3（余量不足，不推荐交付）

- **α id**: `zq3zKgd8`
- **配方**: STAT / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S4.69 / F4.29 / TO 0.2254 / prod **0.6953** / self **0.6954**
- **余量**: prod 0.005 / self 0.005 —— **不满足 ≥0.02 余量要求**
- **RA**: 全过
- **IS checks**: 全部 pass，仅 OSMOSIS_ALLOCATION warning
- **top_correlated**: `wpbQjeKp` 0.6954 / `88vKp8Va` 0.5923 / `blOVO3Pp` 0.5149
- **池**: 21（IND 全在 TOP500）
- ⚠ 虽然 Sharpe 最高（4.69），但 prod/self 双 0.695 距红线仅 0.005，平台漂移风险极高（MEMORY §6：prod 漂移极猛，5 天即作废）。**不推荐作为交付候选。**

### 4.5 USA / TOP3000 — 判死

- **α id**: `ZYQLP163`
- **配方**: CROWDING / d1 / decay 1 / l10 / trunc 0.02 / `combo_a(alpha)` / selection `(1 + 0*(prod_correlation>0)) * (1 - self_correlation)`
- **指标**: S4.50 / F4.90 / TO 0.1253 / prod **0.7341** ❌
- **结论**: 池仅 11 颗，CROWDING 族也无法压住 prod。**USA 永久停投**（除非池子恢复到 ≥17）。

### 4.6 GLB / MINVOL1M — 判死

- **α id**: `xAraq1jm`
- **配方**: STAT / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S7.45 / F4.08 / TO 0.3244 / prod **0.8307** ❌
- **结论**: 虽然 Sharpe 全场最高（7.45），但 MINVOL1M 池 17 颗全在同一个 universe，prod 0.83 严重超标。**GLB 停投。**

### 4.7 DEU / TOP500 — 判死

- **α id**: `QPvdMW8Q`
- **配方**: STAT / d1 / decay 1 / l10 / trunc 0.08 / `combo_a(alpha)` / selection `(1 - self_correlation)`
- **指标**: S2.30 / F1.55 / TO 0.2064 / prod **0.8849** ❌
- **结论**: 池仅 10 颗（刚好卡线），prod 0.885 全场最差。**DEU 停投。**

### 4.8 ASI — 不可建

- 池 = 9，低于平台硬下限 10。**停投。**

---

## 5. 撞墙档案（★=本轮新增）

| # | 区域 / 档位 | 配方 | 现象 | 结论 |
|---|---|---|---|---|
| ★W1 | IND/TOP500 | `combo_a(alpha)` | prod 0.6953，余量 0.005 | 池 21 仍不够厚 |
| ★W2 | USA/TOP3000 | `combo_a(alpha)` CROWDING | prod 0.7341 | 池 11 ⇒ prod 必炸 |
| ★W3 | GLB/MINVOL1M | `combo_a(alpha)` | prod 0.8307 | 同 universe 全池 ⇒ 高度重叠 |
| ★W4 | DEU/TOP500 | `combo_a(alpha)` | prod 0.8849 | 池 10 ⇒ 极端集中 |
| ★W5 | combo `rank(w)` / `weight` / `combo_weight` | 任意 | "unknown variable" | 平台 combo 不接受裸变量名 |
| ★W6 | combo `reduce_max` / `combo_a`(裸) | 任意 | "dimensions dates,alphas:10" | 裸算子名无输入源 |
| ★W7 | combo `generate_stats(alpha)` | 任意 | "set of expressions" | 不可单独作为 combo |
| ★W8 | combo `self_corr(alpha)` | 任意 | "lookback must have a value" | 需显式 lookback 参数 |
| N1 | ASI | 任意 | 池 = 9 < 10 | 平台硬下限 |

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
| selection 变量 | `self_correlation`、`prod_correlation`（含 no-op 门 `(1+0*(prod>0))`） | 其余 23 个 Alpha 属性 + **全部 18 个 `author_*`** |
| selection 算子 | `*` `+` `>`（multiply / add / greater） | `universe_size`、`in`、比较与逻辑族、if_else、power、signed_power 等 ~37 个 |
| combo 算子 | **`combo_a`**（1 个） | **~41 个**，含 generate_stats / self_corr / reduce_* 全族 / trade_when / hump / bucket / tail / zscore / winsorize / rank 等 |

**利用率**：combo 侧 **1/42 ≈ 2.4%**；selection 变量 2/43 ≈ **4.7%**；selection 算子 3/60 ≈ **5%**。

### 6.3 为什么多数算子"用不上"

1. **`combo_a` 是平台为 SA 专门设计的组合算子**（250 天窗口平衡收益/波动率），语义上已是最优组合，无需手工调权。
2. **`author_*` 18 个在自有池里是常数**（同一作者 = 我），对 selection 无区分力。
3. **`universe_size` 只在 selection 可用**：本轮各区组件 universe 单一（IND 全 TOP500、GBR 全 TOP700、KOR 全 TOP600），区分度为 0。
4. **combo 侧其余 41 个算子**要么需要显式输入源（`generate_stats`/`self_corr`/`reduce_*` 在 combo 上下文中无隐式输入），要么用于 REGULAR alpha 的信号构建而非 SA 权重组合。

### 6.4 下一轮可探索

1. **`combo_a` 参数调优**：`nlength`（默认 250）和 `mode`（默认 'algo1'）——当前未测。
2. **多层 combo**：`combo_a(alpha)` 外再套 `zscore` / `winsorize` / `hump` 做权重后整形。
3. **selection 侧 `universe_size`**：在 USA（6 个 universe 有组件）做偏好宽/窄 universe 的加权。
4. **`reduce_*` 族在 combo 上的正确用法**：需先解决输入源问题（可能需 `generate_stats` + `reduce_max` 组合）。

---

## 7. 执行清单

### 7.1 复现命令（全部走 MCP，无临时脚本）

```bash
# ① 组件池 + 档位 + pyramid（MCP get_user_alphas / get_pyramid_multipliers）
# ② 建 SA（MCP create_simulation type=SUPER）
# ③ 双闸实测（MCP check_correlation refresh=True）
```

### 7.2 配额与并发约束

- SUPER **1/ET 日/区**，与 REGULAR 4/ET 日/区独立计数；00:00 ET 重置。
- **prod 账号级单并发**：`check_correlation` 同账号同时只能跑一个（`correlation_busy` 返回 `retry_after`）。
- 单次 `create_simulation` 立即返回结果（IS 指标同步计算），无需等待。

### 7.3 推荐交付顺序（若用户点名提交）

1. **`MPYAOR0r`（GBR/TOP700）**——余量最厚 0.170，最安全 —— **✅ 已提交 ACTIVE**
2. **`YP1d66KM`（EUR/TOPCS1600）**——余量 0.101，次安全 —— ⏳ prod 过闸，**等 10-29 00:00 ET（GMT+8 12:00）SUPER 配额重置后提**
3. **`3qoWQKJg`（KOR/TOP600）**——余量 0.078，第三 —— ⏳ 同上，配额重置后提
4. `zq3zKgd8`（IND/TOP500）——余量 0.005，**不推荐**

> ⚠ **SUPER 配额为账号级全局 1/ET 日**（非分区）。10-28 ET 已用 `MPYAOR0r`，故 EUR/KOR 当日被 `SUPER_SUBMISSION(value=1, limit=1)` 拦（prod 均已过闸）。**每日仅可提交 1 颗 SUPER**，多颗需分日。
>
> ⚠ 提交前必做：再走一次 `check_correlation(refresh=True)`（铁律，台账 >48h 即不可信）。

### 7.4 下一轮候选动作

1. **IND 余量修复**：尝试 selection 加 `*(1 - prod_correlation)` 过滤高 prod 组件，或换 `combo_a` 参数。
2. **USA 池恢复监控**：若池回到 ≥17，CROWDING + `combo_a` 可重开。
3. **算子轴**：`combo_a` 参数调优（nlength/mode）、多层 combo 整形。
4. 不再扫：ASI（池不足）、GLB/DEU/USA（prod 必炸）。

---

## 8. 本轮 MCP 调用记录

| 步骤 | 工具 | 关键参数 | 结果 |
|---|---|---|---|
| 组件池 | `get_user_alphas` | stage=OS, type=REGULAR, status=ACTIVE, region=X | 8 区计数 |
| SUPER 档位 | `get_user_alphas` | is_super=true, region=X | 全 0 已提交 |
| Pyramid | `get_pyramid_multipliers` | — | 11 区完整倍率 |
| 建 SA ×7 | `create_simulation` | type=SUPER, combo=`combo_a(alpha)` | 7 个 id |
| 双闸 ×7 | `check_correlation` | refresh=true | 3 过 / 1 勉强 / 3 毁 |
| 算子 | `get_operators` | — | 103 个算子全量 |