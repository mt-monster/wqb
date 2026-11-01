# 各 Region 最优 SuperAlpha 方案 · 全流程扫描报告

> 生成时间：2026-11-01 12:15 (GMT+8)
> 数据来源：`probe_sa_candidates.py --refresh`（缓存已清空后重新拉取）、
> `get_pyramid_multipliers`（216 条 D0/D1 倍率）、`get_operators`（103 算子）、
> `get_user_alphas(OS,REGULAR)`（REGULAR OS 档位分布）、`get_user_alphas(OS,SUPER)`（SUPER 全景）、
> `sa_run.py` v2 批次 6 档实测（含双闸 prod/self）。
> **铁律：只挖不提交**。本报告全部为待执行配方，默认不做任何提交动作。

---

## 1. 执行摘要 · 优先队列

### ★ 核心结论：SA 线已全域饱和，但 FAST 族在 OCCUPIED 档打开新空间

2026-11-01 刷新盘点 + 6 档新建实测确认：

| 状态 | 数量 |
|---|---|
| 已 ACTIVE SUPER | **43 颗**（跨 8 区） |
| 未提交 SA 候选（IS 阶段） | **9 颗**（无法查 prod/self，仅 IS 指标） |
| 可建 SA 区域 | 8 个（USA/IND/KOR/GBR/EUR/GLB/DEU/MEA） |
| **可用零占用档** | **0 个** |
| **本轮新建 PASS** | **3 颗**（IND/GBR/EUR FAST 族） |

**所有可用 universe 均已被 SUPER 占用**。唯一标注为 ZERO-SA 的 `USA/ILLIQUID_MINVOL1M` 经实测 **平台不开放该 universe 的 SA 创建**（HTTP 400 `Universe ILLIQUID_MINVOL1M is not available.`），8 档候选全部 SELECT-FAILED。

**ZERO-OS 档（self 恒 0）共 5 个，全部已验证撞墙**：

| Region | Universe | 撞墙原因 | 实测 prod |
|---|---|---|---|
| USA | TOP200 | S 不可达（CROWDING l10 S0.95 / l30 S1.28 = STAT l30） | 0.5857（健康但 S 死） |
| EUR | TOP1200 | prod 墙 | 0.7337 |
| EUR | TOP800 | prod 墙 | 0.7117 |
| EUR | TOP400 | prod 墙 | 0.7783 |
| ASI | TOP500 | 组件池 9 < 10 | — |
| HKG | TOP500 | 组件池 6 < 10 | — |

### ★★★ 本轮最大发现：FAST 中性化族在 IND/GBR/EUR 破墙

6 档 OCCUPIED 换族实测中，**FAST 族 3 档全 PASS**，STAT/CROWDING/SLOW/MARKET 全撞：

| # | 配置 | ID | S | F | TO | self | prod | 余量 | 判 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | IND/TOP500 FAST d1 l10 | `mLoqx1v1` | 4.52 | 3.66 | 0.298 | 0.651 | 0.651 | 0.049 | ✅ PASS |
| 2 | GBR/TOP700 FAST d1 l10 | `rKRbrZKo` | 3.80 | 2.96 | 0.207 | 0.476 | 0.617 | 0.083 | ✅ PASS |
| 3 | EUR/TOP2500 FAST d1 l10 | `9qx9aAa2` | 4.83 | 3.99 | 0.175 | 0.671 | 0.670 | 0.030 | ✅ PASS |
| 4 | USA/TOP3000 SLOW d1 l10 | `bl6NWjNR` | 5.77 | 5.70 | 0.169 | 0.783 | 0.783 | — | ❌ BLOCKED |
| 5 | USA/TOP3000 MARKET d1 l10 | `gJemoaZO` | 4.35 | 5.48 | 0.133 | 0.828 | 0.828 | — | ❌ BLOCKED |
| 6 | KOR/TOP600 CROWDING d1 l10 | `RREN2WPg` | 3.89 | 5.48 | 0.104 | 0.955 | 0.955 | — | ❌ BLOCKED |

**⇒ FAST 是继 CROWDING 之后第二个跨区有效的破墙族**（IND/GBR/EUR 均 PASS），且 self 余量显著优于 STAT（IND FAST self 0.651 vs STAT 0.77+）。
**⇒ USA/TOP3000 的 SLOW/MARKET 双撞**（self/prod 0.78–0.83）⇒ USA 仍是最难破的档。

### 优先队列（按剩余可探索空间排序）

| 优先级 | Region | 组件池 | 已占SA | 策略 |
|---|---|---|---|---|
| **P0** | **IND** | 45 | 11 | ⭐ FAST 已 PASS（`mLoqx1v1`）；可继续试 FAST l12/l14/cp3 |
| **P0** | **GBR** | 21 | 5 | ⭐ FAST 已 PASS（`rKRbrZKo`）；CROWDING 已 PASS（`kqNmmaoO`） |
| **P1** | **EUR** | 19 | 5 | ⭐ FAST 已 PASS（`9qx9aAa2`）；prod 余量 0.030 偏薄 |
| **P1** | **USA** | 46 | 12 | 池最大；SLOW/MARKET 撞墙；仅剩 `GrW88N5G`(CROWDING UNSUBMITTED) |
| **P2** | **KOR** | 30 | 10 | CROWDING 撞墙（self 0.955）；FAST 未试 |
| **P3** | **GLB** | 17 | 6 | 小池；所有档已占；FAST 未试 |
| **P4** | **DEU** | 11 | 1 | 池刚过线；观望 |
| ❌ | **MEA** | 19 | 2 | 平台不开放新建（不在 platform_options） |
| ❌ | **ASI** | 9 | 0 | 组件不足（9<10） |
| ❌ | **HKG** | 6 | 0 | 组件不足（6<10） |

---

## 2. 数据基线

### 2.1 组件池 eligibility（2026-11-01 实测，缓存已清空后刷新）

| Region | ACTIVE 已提交 | IS 未提交 | 总 REGULAR | 判定 |
|---|---|---|---|---|
| USA | 46 | 308 | 455 | **GO** |
| IND | 45 | 242 | 291 | **GO** |
| KOR | 30 | 71 | 103 | **GO** |
| GBR | 21 | 51 | 72 | **GO** |
| MEA | 19 | 0 | 19 | **GO**（平台不开放新建） |
| EUR | 19 | 262 | 287 | **GO** |
| GLB | 17 | 0 | 17 | **GO** |
| DEU | 11 | 16 | 27 | **GO**（刚过线） |
| ASI | 9 | 0 | 9 | **BLOCKED** |
| HKG | 6 | 0 | 6 | **BLOCKED** |

> 组件池 = 该 region 已提交且 ACTIVE 的 REGULAR（IS 阶段 UNSUBMITTED 不计入）。
> 与 10-31 相比：USA 45→46(+1)、GBR 20→21(+1)、DEU 10→11(+1)、EUR 18→19(+1)、GLB 17→17(持平)。

### 2.2 档位占用分类（region × universe，2026-11-01 实测）

| Region | Universe | REGULAR | SUPER | 分类 |
|---|---|---|---|---|
| USA | TOP3000 | 37 | 4 | OCCUPIED |
| USA | TOP2000 | 5 | 1 | OCCUPIED |
| USA | TOP1000 | 0 | 1 | OCCUPIED |
| USA | TOP500 | 0 | 1 | OCCUPIED |
| USA | TOPSP500 | 0 | 1 | OCCUPIED |
| USA | TOP200 | 0 | 0 | **ZERO-OS（撞墙：S 不可达）** |
| USA | ILLIQUID_MINVOL1M | 4 | 0 | **ZERO-SA（平台不开放 SA 创建）** |
| IND | TOP500 | 45 | 11 | OCCUPIED（饱和） |
| KOR | TOP600 | 30 | 10 | OCCUPIED（饱和） |
| GBR | TOP700 | 21 | 3 | OCCUPIED |
| EUR | TOP2500 | 10 | 2 | OCCUPIED |
| EUR | TOPCS1600 | 9 | 1 | OCCUPIED |
| EUR | TOP1200 | 0 | 0 | **ZERO-OS（撞墙：prod 0.7337）** |
| EUR | TOP400 | 0 | 0 | **ZERO-OS（撞墙：prod 0.7783）** |
| EUR | TOP800 | 0 | 0 | **ZERO-OS（撞墙：prod 0.7117）** |
| GLB | MINVOL1M | 16 | 2 | OCCUPIED |
| GLB | MINVOL10M | 0 | 1 | OCCUPIED |
| GLB | TOP3000 | 0 | 1 | OCCUPIED |
| GLB | TOPDIV3000 | 1 | 1 | OCCUPIED |
| DEU | TOP500 | 11 | 1 | OCCUPIED |
| MEA | TOP400 | 19 | 2 | OCCUPIED（平台不开放新建） |
| ASI | MINVOL10M | 3 | 0 | ZERO-SA（池 9<10） |
| ASI | MINVOL1M | 6 | 0 | ZERO-SA（池 9<10） |
| ASI | TOP500 | 0 | 0 | ZERO-OS（池 9<10） |
| HKG | TOP500 | 0 | 0 | ZERO-OS（池 6<10） |
| HKG | TOP800 | 6 | 0 | ZERO-SA（池 6<10） |

**分类判据**：
- **ZERO-OS**：无 REGULAR 也无 SUPER ⇒ self 恒 0.0000（但全部撞墙）
- **ZERO-SA**：有 REGULAR 但无 SUPER ⇒ self 非零但偏低（0.28–0.33）
- **OCCUPIED**：已有 ≥1 颗 SUPER ⇒ 新建 SA 的 self 与已有 SUPER 正相关

### 2.3 Pyramid 倍率（D0/D1，按 region）

| Region | D0 avg | D1 avg | D1 最高类 |
|---|---|---|---|
| DEU | 1.84 | 1.63 | analyst/earnings/fundamental/model/news/other (1.8) |
| CHN | 1.74 | 1.61 | other (1.9) |
| AMR | 1.75 | 1.55 | sentiment (1.9) |
| GBR | 1.69 | 1.43 | analyst/earnings/fundamental/news/other (1.9) |
| HKG | — | 1.41 | analyst (1.7) |
| KOR | — | 1.39 | analyst/earnings/fundamental/model/news/other (1.6) |
| EUR | 1.40 | 1.20 | other (1.5) |
| GLB | — | 1.19 | analyst/sentiment (1.4) |
| ASI | — | 1.18 | analyst (1.5) |
| USA | 1.53 | 1.16 | sentiment (1.8) |
| IND | — | 1.14 | analyst/news/other (1.3–1.4) |

> D1 倍率整体低于 D0；DEU/GBR 的 D1 倍率最高（1.63/1.43）⇒ 同样 IS 表现下 OS 期望更高。
> IND 的 D1 倍率最低（1.14）⇒ IND 的 OS Sharpe 需要 IS Sharpe 更强才划算。

### 2.4 平台 SA 算子盘点（`get_operators`，共 103 个）

| 类别 | 数数 | SA combo/selection 相关 |
|---|---|---|
| Time Series | 30 | `ts_mean`, `ts_backfill`, `ts_decay_linear` |
| Arithmetic | 16 | `signed_power` |
| Reduce | 14 | `reduce_max`, `reduce_min`, `reduce_mean`, `reduce_percentage`, `reduce_avg`, `reduce_ir`, `reduce_stddev` |
| Logical | 11 | `if_else` |
| Group | 11 | `group_rank`, `group_backfill`, `group_zscore`, `combo_a` |
| Cross Sectional | 7 | `rank`, `ts_rank` |
| Vector | 7 | `vec_avg`, `vec_sum` |
| Transformational | 4 | `generate_stats` |
| Special | 3 | `self_corr`, `universe_size` |

**算子利用率审计**（回答"本次组建是否充分利用"）：
- SA combo 标配 = `generate_stats` + `self_corr` + `if_else` + `reduce_max`（多样性加权），已充分利用。
- 本工作区实际用到：combo 仅 `generate_stats` `self_corr` `reduce_max` `if_else` `rank` `*` ≈ **6/105 (6%)**；selection 变量仅 `self_correlation` `prod_correlation` `turnover` ≈ 3/25 (12%)。
- **18 个 `author_*` 在自有池中恒为常数** ⇒ 论坛 `author_fitness≥2` 阈值在本工作区不可消费。
- 未测高价值轴：`combo_weight`（combo 专属权重算子）、`zscore(w)`、`winsorize`、`signed_power(rank(w),3)`（禁偶数幂）、selection 侧 `universe_size(universe)` 偏好项、`vec_avg`/`vec_sum`（多字段 combo）。

---

## 3. 选点原则

### 3.1 档位占用类型 > 组件池大小

1. **ZERO-OS 档**（self 恒 0）：最优，但 5 个 ZERO-OS 档全部撞墙（§4）。
2. **ZERO-SA 档**（self 0.28–0.33）：次优，但唯一可用的 `USA/ILLIQUID_MINVOL1M` 平台不开放。
3. **OCCUPIED 档**：可建但 self 与已有 SUPER 正相关（同族 self 可达 0.99），须换族/换结构才能降 self。

### 3.2 指标 = 约束优化

```
max IS Sharpe
s.t. self < 0.7  (余量 ≥ 0.02)
     prod < 0.7  (余量 ≥ 0.02，合规红线，无豁免)
     优选 prod < 0.6（社区合格档）
```

### 3.3 中性化族规律（实测，禁跨区外推）

| 族 | 适用场景 | 代表区域 |
|---|---|---|
| **CROWDING** | 池中大型、STAT 撞墙时首选 | GBR PASS、USA 自过但 prod 高 |
| **FAST** | USA 窄档（TOP500/TOPSP500） | USA/TOP500 PASS、USA/TOP3000 PASS |
| **SLOW** | TO<0.10 时 | 本轮首次测 USA/TOP3000 |
| **MARKET** | TO>0.20 时 | 本轮首次测 USA/TOP3000 |
| **SECTOR** | KOR/IND/GBR（须逐区验证） | KOR/IND/GBR 走 SECTOR + decay 15 |
| **STATISTICAL** | ⚠ 全域撞墙（self/prod 双超 0.7） | 不推荐 |

**F 闸排序**（IND 实测）：CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3。
**选族规则**：TO<0.10 → SLOW；TO>0.20 → FAST。

### 3.4 论坛指标标准（引用 §0，标注三档与筛选阈值）

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

**组件筛选阈值**：`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ 筛选强度必须匹配池子规模：加严约束后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。
小池区（EUR/GLB/DEU）只能用宽松 selection `(1 - self_correlation)`，论坛严格阈值仅适用于 IND/USA 等大池区。

---

## 4. 分 Region 方案

### 4.1 USA（组件池 46，已占 12 颗 SA）

**现状**：池最大，但所有可用 universe 均 OCCUPIED。TOP3000 已占 4 颗（含已提交 `gJePPn0K` FAST、`E567rQvR` CROWDING cp rank）。

**最优配方**（按优先级）：

| # | 配置 | 策略 | 状态 |
|---|---|---|---|
| 1 | `usa3000_crowd_d1_l10` | CROWDING 破 STAT 墙 | `GrW88N5G` UNSUBMITTED（S4.51/F5.57/TO0.134） |
| 2 | `usa3000_slow_d1_l10` | SLOW 族 | ❌ 撞墙（self/prod 0.783） |
| 3 | `usa3000_market_d1_l10` | MARKET 族 | ❌ 撞墙（self/prod 0.828） |
| 4 | `usa3000_crowd_d1_l10_cp3` | combo_power 增益 | 待实测 prod/self |

**预期**：USA/TOP3000 是最难破的档——SLOW/MARKET/CROWDING 全撞，self/prod 基数 0.78–0.83。仅剩 `GrW88N5G`（CROWDING UNSUBMITTED）和 combo 整形（`rank(w)`/`cp3`）未试。

### 4.2 IND（组件池 45，已占 11 颗 SA）⭐

**现状**：池大但 TOP500 唯一 universe 已饱和（11 颗）。STAT 全死，CROWDING self 0.7733 撞墙。

**最优配方**：

| # | 配置 | 策略 | 状态 |
|---|---|---|---|
| 1 | `ind500_fast_d1_l10` | FAST 族 | ✅ **PASS** `mLoqx1v1`（S4.52/F3.66/TO0.298, self 0.651/prod 0.651, 余量 0.049） |
| 2 | `ind500_fast_d1_l12` | FAST + 大 limit | 待建（⚠ limit↑ 推高 self/prod） |
| 3 | `ind500_fast_d1_l10_cp3` | FAST + combo_power | 待建（cp 增益不动 prod） |

**预期**：IND 的 D1 pyramid 倍率最低（1.14），OS Sharpe 需要 IS 更强。FAST 是首个在 IND 破墙的族。

### 4.3 KOR（组件池 30，已占 10 颗 SA）

**现状**：TOP600 唯一 universe 已饱和（10 颗）。STAT 全死。

**最优配方**：

| # | 配置 | 策略 | 状态 |
|---|---|---|---|
| 1 | `kor600_crowd_d1_l10` | CROWDING 族 | ❌ 撞墙（self/prod 0.955） |
| 2 | `kor600_fast_d1_l10` | FAST 族 | 待建（未试） |

**预期**：KOR 池 30 中等，CROWDING self 0.955 撞墙（同族堆叠）。FAST 是最后未试族。

### 4.4 GBR（组件池 21，已占 5 颗 SA）⭐

**现状**：CROWDING d1 l10 已 PASS（`kqNmmaoO` UNSUBMITTED，S3.66/F3.60/TO0.1526）。STAT 全死。

**最优配方**：

| # | 配置 | 策略 | 状态 |
|---|---|---|---|
| 1 | `gbr700_crowd_d1_l10` | CROWDING 已 PASS | `kqNmmaoO` UNSUBMITTED |
| 2 | `gbr700_fast_d1_l10` | FAST 族 | ✅ **PASS** `rKRbrZKo`（S3.80/F2.96/TO0.207, self 0.476/prod 0.617, 余量 0.083） |

**预期**：GBR 的 D1 pyramid 倍率 1.43（高），OS 期望好。CROWDING + FAST 双族均已 PASS。

### 4.5 EUR（组件池 19，已占 5 颗 SA）⭐

**现状**：小池；STAT 全死（self 0.815–0.869）；3 个 ZERO-OS 档 prod 全撞（0.71–0.78）。

**最优配方**：

| # | 配置 | 策略 | 状态 |
|---|---|---|---|
| 1 | `eur2500_fast_d1_l10` | FAST 族 | ✅ **PASS** `9qx9aAa2`（S4.83/F3.99/TO0.175, self 0.671/prod 0.670, 余量 0.030） |
| 2 | `eur_topcs1600_crowd_d1_l10` | 换 universe + CROWDING | 历史（self 0.33/prod 0.56） |

**预期**：EUR prod 余量 0.030 偏薄（prod 漂移实证：`gJWdxLbM` 48h 内 +0.068）。交付前必须 refresh=True 复测。

### 4.6 GLB（组件池 17，已占 6 颗 SA）

**现状**：小池；STAT 全死（self 0.873）；所有档已占。

**最优配方**：无新档可用。仅剩换族（CROWDING/FAST/SLOW 在 MINVOL1M 已测）。

### 4.7 DEU（组件池 11，已占 1 颗 SA）

**现状**：池刚过线（11），任何组件流失即不可建。D1 pyramid 倍率最高（1.63）。

**最优配方**：观望。池子涨到 ≥17 才有余量。

### 4.8 MEA（组件池 19，已占 2 颗 SA）

**现状**：平台不开放新建（不在 platform_options 的 region 列表）。已占 2 颗保留。

---

## 5. 停投区

| Region | 理由 |
|---|---|
| **MEA** | 平台不开放新建 SA（`Region MEA is not available.`），已占 2 颗保留 |
| **ASI** | 组件池 9 < 10 硬下限，不可建 |
| **HKG** | 组件池 6 < 10 硬下限，不可建 |
| **EUR** | prod 墙结构性（3 个 ZERO-OS 档 prod 0.71–0.78，STAT self 0.81–0.87），换族无解 |
| **USA/TOP200** | S 不可达（CROWDING l10 S0.95、l30 S1.28），prod 健康但 IS 死 |
| **USA/ILLIQUID_MINVOL1M** | 平台不开放该 universe 的 SA 创建（实测 8 档全 400） |

---

## 6. 撞墙档案（已验证不可用的候选）

### 6.1 全域死族
| 族 | 范围 | 实测 |
|---|---|---|
| **STATISTICAL d1** | 所有 region | self 0.695–0.873，prod 0.666–0.873，全线双超 |
| **decay d0** | SA 组合层 | 与 d1 逐字相同（SA 层 decay 无效） |
| **combo_power ≥6** | USA/TOP500 | 2Y 恰为 1.58 == limit ⇒ Ladder FAIL |
| **selection 排序量 = prod_correlation** | 所有 | S 1.77→1.04，毁灭性负杠杆 |

### 6.2 区域撞墙
| Region | Universe | 配方 | 撞墙原因 |
|---|---|---|---|
| USA | TOP200 | CROWDING/STAT all limit | S 不可达（max 1.28） |
| USA | TOP3000 | STAT d1 | self 0.695–0.823 |
| USA | TOP3000 | CROWDING | prod 0.723 超红线 |
| USA | TOP3000 | SLOW d1 l10 | self 0.783 / prod 0.783（本轮实测） |
| USA | TOP3000 | MARKET d1 l10 | self 0.828 / prod 0.828（本轮实测） |
| USA | ILLIQUID_MINVOL1M | 全 8 档 | 平台不开放该 universe（HTTP 400） |
| EUR | TOP1200 | CROWDING d1 | prod 0.7337 |
| EUR | TOP800 | CROWDING d1 | prod 0.7117 |
| EUR | TOP400 | CROWDING d1 | prod 0.7783 |
| EUR | TOP2500 | STAT d1 | self 0.815–0.869 |
| GLB | MINVOL1M | STAT d1 | self 0.873 |
| GLB | MINVOL1M | MARKET | prod 0.762 |
| IND | TOP500 | CROWDING d1 | self 0.7733 / prod 0.7733 |
| KOR | TOP600 | STAT d1 | self 0.935（l14） |
| KOR | TOP600 | CROWDING d1 l10 | self 0.955 / prod 0.955（本轮实测） |
| DEU | TOP500 | STAT d1 | prod 0.764 |
| GBR | TOP700 | STAT d1 | self 0.814 |

### 6.3 已提交 SA 的同档候选（作废）
同档同族第二颗 self ≈ 1（如 USA/TOPSP500 l40 两颗 self 0.9872/0.9871）⇒ 该档封死。

---

## 7. 执行清单

### 7.1 构建命令

```bash
# v2 批次（OCCUPIED 档换族，运行中）
cd C:/Users/MENGTAO/wqb-scripts
nohup .../python.exe sa_run.py \
  --configs sa_plan_20261101/configs_v2.json \
  --out sa_plan_20261101/res_v2.jsonl > sa_plan_20261101/run_v2.log 2>&1 &

# 单颗提交（仅当用户明确点名）
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 .../python.exe tools/super_build.py submit \
  --alpha-id <ID> --region <REGION>
```

### 7.2 配额约束

| 约束 | 值 |
|---|---|
| SUPER 配额 | **1 颗/天/区**（与 REGULAR 4/天/区独立计数） |
| 组件池硬下限 | **10**（<10 直接 400） |
| selectionLimit 实际生效 | min(limit, 组件池) |
| prod 合规红线 | **≥0.7 = 合规红线，无豁免入口** |
| 台账 prod 有效期 | **48h**，超时必须 `refresh=True` 重测 |

### 7.3 建议执行顺序

1. **等待 v2 批次结算**（6 档，~45 分钟），逐档查 IS 指标。
2. **对 IS 过线的候选查双闸**：`check_correlation(alpha_id=<ID>, refresh=True)` → prod + self。
3. **优选落"社区合格档"**：prod < 0.6 且 TO < 0.30。
4. **prod 余量 <0.02 一律不交付**。
5. **用户点名后才提交**（`super_build.py submit`），提交前先停掉后台 sa_run.py 批次。
6. **提交后等满 flip 窗（~250s）**，`super_build.py status --alpha-id <ID>` 确认 `status=ACTIVE`。

### 7.4 本轮新建 PASS 候选（UNSUBMITTED，待用户点名提交）

| ID | Region | 配置 | S | F | TO | self | prod | 余量 | 建议 |
|---|---|---|---|---|---|---|---|---|---|
| `mLoqx1v1` | IND | TOP500 FAST d1 l10 | 4.52 | 3.66 | 0.298 | 0.651 | 0.651 | 0.049 | ⭐ 首选，IND 唯一破墙族 |
| `rKRbrZKo` | GBR | TOP700 FAST d1 l10 | 3.80 | 2.96 | 0.207 | 0.476 | 0.617 | 0.083 | ✅ **已提交 ACTIVE**（11-01 用户点名） |
| `9qx9aAa2` | EUR | TOP2500 FAST d1 l10 | 4.83 | 3.99 | 0.175 | 0.671 | 0.670 | 0.030 | ⚠ 余量偏薄，交付前必 refresh |

### 7.5 既有 UNSUBMITTED 候选（IS 阶段，无法查 prod/self）

| ID | Region | 配置 | S | F | TO | 建议 |
|---|---|---|---|---|---|---|
| `GrW88N5G` | USA | TOP3000 CROWDING l10 | 4.51 | 5.57 | 0.134 | ⭐ USA 最后希望 |
| `kqNmmaoO` | GBR | TOP700 CROWDING l10 | 3.66 | 3.60 | 0.153 | ⭐ 已知 PASS 族 |
| `88R66Eqo` | USA | TOP3000 STAT l30 | 5.61 | 5.95 | 0.152 | STAT 死，不建议 |
| `vR1zzNMr` | USA | TOP3000 STAT l10 | 5.44 | 5.26 | 0.167 | STAT 死，不建议 |
| `gJePPWMK` | USA | TOP3000 STAT l12 | 5.45 | 5.21 | 0.174 | STAT 死，不建议 |
| `bl6PWV2p` | EUR | TOP2500 STAT l14 | 4.63 | 3.41 | 0.155 | STAT 死 + EUR prod 墙 |
| `2rAZnM6N` | EUR | TOP2500 STAT l12 | 4.78 | 3.43 | 0.168 | STAT 死 + EUR prod 墙 |
| `O0Am5P3q` | GLB | MINVOL1M STAT l12 | 7.65 | 4.57 | 0.308 | STAT 死 + TO 超标 |
| `78LXXZ9b` | GBR | TOP700 STAT l12 | 4.52 | 4.03 | 0.170 | STAT 死 |

> ⚠ 提交 UNSUBMITTED 候选后，其 prod/self 才可查。建议优先提交 `GrW88N5G`（CROWDING 族，USA/TOP3000 未占席）。

---

## 8. 关键约束（铁律）

- **只挖不提交**：方案全部为待执行配方，默认不做任何提交动作（提交权归用户）。
- **prod ≥ 0.7 = 合规红线，无豁免入口**。
- **组件池只看 ACTIVE 已提交 REGULAR**（IS 阶段 UNSUBMITTED 不计入）。
- **SUPER 配额 1/天/区**，与 REGULAR 4/天/区独立计数。
- **台账 prod > 48h 不可信**，必须 `refresh=True` 重测。
- **prod 是账号级单并发**：被并行任务占会返回 null（`correlation_busy`），需 8×40s 患者式重试。
- **SA 线全域饱和**：无零占用档可用，剩余空间仅限 OCCUPIED 档换族 + UNSUBMITTED 候选提交。

---

*报告生成：2026-11-01 11:30 GMT+8 · 数据已清缓存后刷新 · 下轮建议：v2 批次结算后更新双闸实测值*