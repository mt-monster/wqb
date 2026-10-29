# 各 Region 最优 SuperAlpha 方案 — 2026-10-27 夜间全流程扫描

> 生成时间：2026-10-27 23:40 → 10-28 00:20（GMT+8）
> 工作目录：`D:\coding\traeCN_project\wqb`　产物目录：`results/sa_scan_20261027_night/`
> 上午版留存：`output_report/SA_best_per_region_plan_20261027_am.md`
> **本报告全部为待执行配方，未做任何提交动作**（只挖不提交铁律；提交权归用户点名）。

---

## 0. 执行摘要（按价值排序）

| # | 优先级 | 区域 / 档位 | 配方 | α id | IS（S / F / TO） | prod / self | 余量 | 状态与动作 |
|---|---|---|---|---|---|---|---|---|
| 1 | **P0 首选** | **USA / TOP500**（ZERO-OS 新档） | **CROWDING d1 l10 cp4** | **`78LAAZx1`** | **1.78 / 1.30 / 0.1589** | **0.6530** / 0.0000 | **0.047** / 0.700 | **本轮新建，prod 今晚 23:55 实测，IS 11 项全 PASS** |
| 2 | P0 备选（同档同族，互斥） | USA / TOP500 | CROWDING d1 l10 **cp5** | `78LAAm92` | 1.79 / **1.32** / 0.1575 | **未取到**（同族 cp1/3/4 均 0.6530，直方图逐桶重合） | ≈0.047 | 四项指标全场最优，prod 因队列占用未落 |
| 3 | P0 备选（同档同族，互斥） | USA / TOP500 | CROWDING d1 l10 **cp3** | `P0MRkP0M` | 1.77 / 1.29 / 0.1606 | 0.6530（10-26 00:25 缓存） | 0.047 | 连续三日稳定；同 #1 二选一 |
| 4 | P0 备选（同档同族，互斥） | USA / TOP500 | CROWDING d1 l10 cp1 | `LL5rpRY2` | 1.74 / 1.25 / 0.1647 | 0.6530（10-26 缓存，今日 refresh 队列被占） | 0.047 | 最早那颗，指标最低 |
| 5 | — | GLB / MINVOL10M | SLOW d1 l10 cp1 | `LLMVPag1` | 4.25 / 2.19 / 0.2570 | 0.5599 / 0.0000 | 0.140 | **已于 10-27 09:16 提交 ACTIVE ⇒ 档位已占** |
| 6 | **作废** | GLB / MINVOL10M | STAT / CROWDING l12 / INDUSTRY | `0mYm1gqv` / `Vkx1v6a0` / `vR1wKx2b` | 4.49 / 4.17 / 4.16 | 0.639 / 0.698 / 0.748 | — | #5 提交后同档第二颗 self≈1 ⇒ 全部作废 |
| 7 | 撞墙 | USA / TOP200（ZERO-OS） | STATISTICAL l40 / l50 | `E56OZ85R` / `Vkx1vLOw` | **1.12 / 0.51** | 0.5857 / 0.0000 | — | S 天花板 1.12，2Y Ladder 0.30 ⇒ 判死 |
| 8 | 撞墙 | USA / TOP500 **d0** | CROWDING d0 cp3 | — | — | — | — | **`At least 10 component alphas are required`**（d0 池枯竭） |

**三句话结论**

1. **今晚唯一可交付的仍是 USA / TOP500 这一档**，且已把该档配方推到边界：`combo_power` 1→5 单调抬升（S 1.74→1.79、F 1.25→1.32、TO 0.1647→0.1575），**prod 纹丝不动在 0.6530**；到 **cp6 撞上 IS Ladder 的严格不等式**（2Y = 1.58 == 1.58 ⇒ FAIL）。**cp5 是可用上限，cp4 是已验证上限。**
2. **EUR 全域 prod 墙是"族也救不了"的性质**：三个零占用档用的**本来就是 CROWDING**（该区 prod 最优族），实测 0.7337 / 0.7117 / 0.7783，其中 TOP800（S1.40）、TOP400（S1.23）连云 IS 都不过。**EUR 不需要再扫配方。**
3. **修正一条方法论口径**：SA 组件池不是"region 级"，而是 **(region, delay) 级**。USA 的 50 颗组件全在 d1，故 USA/TOP500 d0 直接 400（组件 <10）。此前"组件池是 region 级"的说法只在同 delay 内成立。

---

## 1. 数据基线

### 1.1 组件池 eligibility（口径：stage=OS + type=REGULAR + status=ACTIVE）

取数前已清 `api_cache`（`DELETE ... WHERE cache_key LIKE '%user_alphas%'`），再全量翻 OS（**361 条**，上午 356 条）。

| Region | 组件池 | 上午(08:02) | Δ | 判定 | 组件 universe 分布 |
|---|---:|---:|---:|---|---|
| IND | **53** | 53 | 0 | GO（池最大，但唯一 universe 已 11 颗 SUPER） | TOP500: 53 |
| USA | **50** | 50 | 0 | **GO（唯一还有可交付零占用档）** | TOP3000:38, TOP2000:6, ILLIQ_MINVOL1M:4, TOPSP500:1, TOP1000:1 |
| KOR | **39** | 39 | 0 | GO（单 universe，9 颗 SUPER） | TOP600: 39 |
| MEA | 21 | 21 | 0 | **BLOCKED — 平台已下架** | TOP400: 21 |
| GBR | **20** | 20 | 0 | GO（无空档） | TOP700: 20 |
| EUR | **18** | 18 | 0 | GO 但 **prod 墙** | TOPCS1600:10, TOP2500:8 |
| GLB | **21** | 16 | **+5** | GO（四档全占） | MINVOL1M:17, TOPDIV3000:2, TOP3000:1, MINVOL10M:1 |
| DEU | **11** | 11 | 0 | GO（单档已占） | TOP500: 11 |
| ASI | 9 | 9 | 0 | **BLOCKED**（<10 硬下限） | MINVOL1M:6, MINVOL10M:3 |
| HKG | 6 | 6 | 0 | **BLOCKED**（<10） | TOP800: 6 |
| CHN / JPN / TWN / AMR | 0 | 0 | 0 | 无组件 | — |

**变化点**：GLB 16→21（+5，均为今日提交的 d1 REGULAR）。其余区域零变化 ⇒ **产能瓶颈不在池子，在档位**。

### 1.2 平台权威 universe 清单（EQUITY，`get_platform_setting_options`）

| Region | 合法 universe | 空档（无 SUPER） |
|---|---|---|
| USA | TOP3000, TOP2000, TOP1000, **TOP500**, TOP200, TOPSP500 | **TOP500**（可建）、TOP200（S 死） |
| EUR | TOP2500, **TOP1200**, TOPCS1600, **TOP800, TOP400** | 三个，但 prod 墙 |
| GLB | TOP3000, MINVOL1M, MINVOL10M, TOPDIV3000 | 无 |
| ASI | MINVOL1M, MINVOL10M, TOP500 | TOP500（池 9，不可建） |
| HKG | TOP800, TOP500 | TOP500（池 6，不可建） |
| IND / KOR / GBR / DEU | TOP500 / TOP600 / TOP700 / TOP500（各唯一） | 无 |
| MEA | **平台无此 region**（新建 400） | — |

> `USA / ILLIQUID_MINVOL1M` 有 4 颗 REGULAR OS，但**不在当前 platform options 内** ⇒ 视为历史残留档，不可新建。

### 1.3 档位占用分类（ACTIVE OS SUPER = **39**，上午 38）

口径：`stage=OS + status=ACTIVE + alpha_type="SUPER"`（服务端过滤单独拉；SUPER 不出现在 stage=OS 全表、`is_super` 恒 False）。

| Region | Universe | 组件池 | REG ACTIVE | SUPER ACTIVE | 分类 | self 预期 |
|---|---|---:|---:|---:|---|---|
| **USA** | **TOP500** | 50 | 0 | 0 | **ZERO-OS** | **0.0000** |
| USA | TOP200 | 50 | 0 | 0 | ZERO-OS | 0.0000 |
| EUR | TOP1200 | 18 | 0 | 0 | ZERO-OS | 0.0000 |
| EUR | TOP800 | 18 | 0 | 0 | ZERO-OS | 0.0000 |
| EUR | TOP400 | 18 | 0 | 0 | ZERO-OS | 0.0000 |
| ASI | MINVOL1M / MINVOL10M | 9 | 6 / 3 | 0 | ZERO-SA | low，但池 <10 不可建 |
| HKG | TOP800 | 6 | 6 | 0 | ZERO-SA | low，池 <10 不可建 |
| USA | TOP3000 / TOP2000 / TOP1000 / TOPSP500 | 50 | 38 / 6 / 1 / 1 | 3 / 1 / 1 / 1 | OCCUPIED | — |
| IND | TOP500 | 53 | 53 | **11** | OCCUPIED | — |
| KOR | TOP600 | 39 | 39 | **9** | OCCUPIED | — |
| GLB | MINVOL1M / MINVOL10M / TOPDIV3000 / TOP3000 | 21 | 17 / 1 / 2 / 1 | 2 / 1 / 1 / 1 | OCCUPIED | — |
| GBR | TOP700 | 20 | 20 | 2 | OCCUPIED | — |
| EUR | TOP2500 / TOPCS1600 | 18 | 8 / 10 | 2 / 1 | OCCUPIED | — |
| DEU | TOP500 | 11 | 11 | 1 | OCCUPIED | — |
| MEA | TOP400 | 21 | 21 | 2 | 平台下架 | — |

**新增占档**：`GLB|MINVOL10M` ×1 —— `LLMVPag1`（10-27 09:16 提交，S4.25/F2.19/prod 0.5599）。GLB 四档自此全满。

### 1.4 Pyramid 倍率（`get_pyramid_multipliers`，216 条）

| Region | d0 均值 / 峰值 | d1 均值 / 峰值 | 备注 |
|---|---|---|---|
| DEU | **1.84 / 1.9** | 1.63 / 1.8 | 全站最高，但单档已占 |
| GBR | 1.69 / 1.9 | 1.43 / 1.7 | 高倍率、无空档 |
| KOR | — | 1.39 / 1.6 | 9 颗 SUPER 已摊薄 |
| HKG | — | 1.41 / 1.7 | 池不足 |
| USA | 1.53 / 1.8 | **1.16 / 1.4** | d1 倍率最低（池最大、竞争者最多） |
| EUR | 1.40 / 1.7 | 1.20 / 1.5 | 空档存在但 prod 墙 |
| GLB | — | 1.19 / 1.4 | 四档全占 |
| IND | — | 1.14 / 1.4 | 11 颗 SUPER |
| ASI | — | 1.18 / 1.5 | 池不足 |
| CHN | 1.74 / 1.9 | 1.61 / 1.9 | 无组件 |

**读法**：倍率与"该区已被挖多深"严格负相关 —— DEU/GBR 高倍率正是"没被挖过"，但两者都没有空档；**USA/TOP500 倍率仅 1.16，却是唯一可交付档**，说明当前阶段收益来源是"新席位"，不是"高倍率"。

---

## 2. 选点原则（本轮实证更新）

1. **档位占用类型 > 组件池大小**。GLB 池从 16 涨到 21（+31%），但因四档全占，产能增量为 **0**；USA 池原地不动，却因为 TOP500 是 ZERO-OS，仍是唯一产出点。
2. **指标 = 约束优化**：`max IS Sharpe s.t. prod < 0.7 且 self < 0.7`，工程上要求余量 ≥ 0.02，优选 prod < 0.6 且 TO < 0.30（社区合格档）。
   本轮 #1~#4 全部满足 `prod 0.653 / self 0.000 / TO 0.157`，但 **prod 余量只有 0.047**（未达 0.6 档）。
3. **中性化族规律（跨区实测汇总）**

   | 区域 | prod 最优 → 最差 | 是否推翻"CROWDING 恒优" |
   |---|---|---|
   | GLB / MINVOL10M | SLOW 0.560 < STAT 0.639 < CROWDING 0.698 < INDUSTRY 0.748 | **是** |
   | USA / TOPSP500 | CROWDING 0.625 < SECTOR 0.691 < MARKET 0.694 < SUBIND 0.748 | 否 |
   | GLB / MINVOL1M | CROWDING 0.692 < MARKET 0.762 | 否 |
   | USA / TOP500 | CROWDING 0.653（cp1/3/4 恒定） | 否 |
   | KOR / TOP600 | CROWDING 0.673（l10） | 否 |

   ⇒ **CROWDING 在 5 个区域中 4 个最优，但不可跨区外推**；GLB 的 SLOW 是唯一反例（`LLMVPag1` 靠它拿到 0.560）。
4. **TO<0.10 → SLOW；TO>0.20 → FAST**（论坛规律）：USA/TOP500 cp5 TO=0.1575 落在中间区，CROWDING 仍最稳。
5. **`combo_power` 是唯一"不动 prod 的纯增益轴"**，但有硬上限：受 IS Ladder 严格不等式约束（§4.1）。
6. **组件池按 (region, delay) 分池**：跨 delay 借池不成立（USA d0 = 0 组件）。

---

## 3. 论坛指标标准（沿用 2026-10-22 定稿，无需重复调研）

来源：《【新人入门】Super Alpha 从入门到入门！》78 赞/39 评论、《2024 super alpha 比赛心得》22 赞/15 评论、《Super Alpha 参数设置》12 赞（含 LY43440 实测回复）。

### 3.1 三档标准

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

**本轮落位**：`78LAAZx1` 满足 A 档全部四项 + B 档 TO 项（0.159），**prod 0.653 未达 B 档 0.6**；IND（11 颗 S 5.43/F 5.74）、KOR（9 颗 S 4.98/F 5.94）已摸到 C 档下沿，但被 prod 与档位饱和锁死。

### 3.2 组成数量（Selection Limit）

- 平台硬下限 **10**（<10 直接 400：`Ensure this value is greater than or equal to 10`）。
- 论坛建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300。
- **实际生效数 = min(limit, 组件池)**，且 **池按 (region, delay) 计**。
- 本轮反证：USA/TOP500 **l12 直接 IS Ladder FAIL**；GLB/MINVOL10M l12 prod 0.698（余量 0.002）也差于 l10。⇒ **小池区/窄档一律 l10 起，加大 limit 会同时推高 prod 并引入 Ladder FAIL。**

### 3.3 组件筛选阈值

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。

⚠ **筛选强度必须匹配池子规模**：
- 严格 selection `(1-self)*(TO<0.3)*(prod<0.6)` 在 USA/TOP500 实测 **S 1.74→1.47**（负杠杆）⇒ 论坛阈值不适用 USA。
- GBR/DEU 等小池区加严后组件 <10 ⇒ `At least 10 component alphas are required`。
- **本轮统一用宽松 selection `(1 + 0*(prod_correlation>0)) * (1 - self_correlation)`**，全部成功出候选。

### 3.4 其他实证
- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）⇒ 固定 0.02。
- `Selection Handling = POSITIVE`：本工作区 39 颗 ACTIVE SA 全部使用，无一失败。
- **`decay` 在 SA 组合层完全无效**：TOPSP500 d0 与 d1 的 S/F/TO/prod 逐字相同 ⇒ 该轴不必再扫。

---

## 4. 分 Region 方案

### 4.1 USA / TOP500 — 唯一可交付档（P0）

- 档位性质：**ZERO-OS**（0 REGULAR、0 SUPER）⇒ `self` 恒 **0.0000**；组件池 50（region 级，全 d1）。
- 最佳配方：`CROWDING` / `delay 1` / `decay 1` / `selectionLimit 10` / `truncation 0.02` / `selectionHandling POSITIVE`，combo 权重取 `w^power`。

**combo_power 扫描（本轮核心实验，一次一变量）**

| cp | α id | Sharpe | Fitness | Turnover | prod | self | fails | 判定 |
|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | `LL5rpRY2` | 1.74 | 1.25 | 0.1647 | 0.6530 | 0.0000 | — | PASS |
| 3 | `P0MRkP0M` | 1.77 | 1.29 | 0.1606 | 0.6530 | 0.0000 | — | PASS |
| **4** | **`78LAAZx1`** | **1.78** | **1.30** | **0.1589** | **0.6530** | **0.0000** | — | **PASS（本轮实测 prod）** |
| 5 | `78LAAm92` | **1.79** | **1.32** | **0.1575** | 未取到（同族代理 0.653） | 0.0000 | — | PASS（prod 待补） |
| 6 | `N1NwwYq7` | 1.79 | 1.33 | 0.1562 | — | 0.0000 | **IS_LADDER 1.58==1.58** | **FAIL（严格不等式）** |

**cp5 的 prod 兜底证据**（本地 `alpha_corr_cache` 直方图，逐桶对比 cp3 与 cp4）：

| prod 桶 | cp3 `P0MRkP0M` | cp4 `78LAAZx1` |
|---|---:|---:|
| 0.5–0.6 | 48 | 49 |
| 0.6–0.7 | 6 | 6 |
| ≥0.7 | **0** | **0** |

⇒ 两代幂次的最大相关桶分布几乎逐桶重合，且 ≥0.7 桶恒为 0；`combo_power` 对权重形状的改变不足以跨过 0.653 这个结构值。**cp5 的 prod 结构上必然同为 0.6530**，但交付前仍须实测确认（铁律：>48h 或未测即 `refresh=True`）。

**结论**
1. `combo_power` 单调微增（cp1→cp5：S +0.05、F +0.07、TO −0.007），**prod 完全不动**（cp1/3/4 三次独立实测均 0.6530，逐位相同）⇒ 与"换族/加 limit"本质不同，是**零成本增益**。
2. **上限由 IS Ladder 而非 prod 决定**：cp6 的 2Y Sharpe 恰为 1.58（limit 亦 1.58），平台按严格不等式判 FAIL。
3. **优先级**：`78LAAZx1`（cp4，prod 今晚实测）> `78LAAm92`（cp5，指标最好但 prod 未复测）> `P0MRkP0M`（cp3）> `LL5rpRY2`（cp1）。四颗互斥，**同档只出 1 席**。

### 4.2 GLB — 已饱和（本轮封档）

- 池 16→**21**（+5），但四档全占；`LLLMVPag1`（MINVOL10M SLOW d1 l10）10-27 09:16 提交 ACTIVE，**prod 0.5599 / self 0.0000**，是本轮体系里唯一进 B 档（prod<0.6）的 SA。
- 同档其余三颗（`0mYm1gqv` STAT 0.639 / `Vkx1v6a0` CROWDING l12 0.698 / `vR1wKx2b` INDUSTRY 0.748）⇒ 提交后第二颗 self≈1，**全部作废**。
- **结论：GLB 停投**，直到平台新增 universe。

### 4.3 EUR — prod 墙确证，配方已用尽（停投）

| 档位 | 最佳已知配方 | S / F / TO | prod | 判定 |
|---|---|---|---:|---|
| TOP1200 | CROWDING d1 l10 | 2.06 / 1.47 / 0.1627 | **0.7337** | 过 IS，prod 超标 |
| TOP800 | CROWDING d1 l10 | **1.40** / 0.81 / 0.1726 | 0.7117 | IS 亦不过 |
| TOP400 | CROWDING d1 l10 | **1.23** / 0.67 / 0.1827 | 0.7783 | IS 亦不过 |
| TOPCS1600（已占） | — | `gJWdxLbM` 0.6988→**0.7666** 漂移 | — | — |
| TOP2500（已占） | — | `kqJOQgnk` S3.92/F3.40 | 0.6546→已提交 | — |

**关键**：三个零占用档用的**本来就是 CROWDING**（本区 prod 最优族），不存在"换族可救"的空间 ⇒ **EUR 全域停投**，除非平台生产池结构变化。

### 4.4 IND / KOR / DEU / GBR — 档位饱和（停投）

| Region | 唯一 universe | SUPER 占位 | 池 | 历史最佳 | 状态 |
|---|---|---:|---:|---|---|
| IND | TOP500 | **11** | 53 | S 5.43 / F 5.74 | 饱和，同档再建 self≈1 |
| KOR | TOP600 | **9** | 39 | S 4.98 / F 5.94 | 饱和；l14 实测 self 0.935 |
| GBR | TOP700 | 2 | 20 | S 3.44 / F 2.99 | 严格 selection 后组件<10 |
| DEU | TOP500 | 1 | 11 | S 2.27 / F 1.67 | 池仅 11，加严即 <10；产能 0.764 撞墙 |

### 4.5 MEA / ASI / HKG / CHN / JPN / TWN / AMR — 不可建

- **MEA**：平台 `Region MEA is not available.`（新建 400，CROWDING 亦不可用）；历史 2 颗仍 ACTIVE。
- **ASI（9）/ HKG（6）**：低于平台硬下限 10，任何 selection 都选不出 10 个组件。
- **CHN / JPN / TWN / AMR**：组件池 0。

---

## 5. 撞墙档案（累计，含本轮新增）

| # | 区域 / 档位 | 配方 | 现象 | 结论 |
|---|---|---|---|---|
| N1 | **USA / TOP500 d0** | CROWDING d0 cp3 | `At least 10 component alphas are required` | **d0 池 = 0（USA 50 颗全 d1）⇒ delay 不可换** |
| N2 | **USA / TOP500 cp6** | CROWDING d1 l10 cp6 | IS_LADDER 1.58 == 1.58 FAIL | combo_power 上限 = **5** |
| N3 | USA / TOP500 l12 | CROWDING d1 l12 cp1 | Ladder FAIL | l10 是唯一甜点 |
| N4 | USA / TOP500 strict | `(1-self)*(TO<0.3)*(prod<0.6)` | S 1.74→1.47 | 论坛严格阈值在 USA 是负杠杆 |
| N5 | USA / TOP200 | STAT l40/l50 | S1.12/F0.51、2Y 0.30 | S 天花板不可达 |
| N6 | USA / TOPSP500 | CROWDING / SECTOR / MARKET / SUBIND | 0.625–0.748，且已被 `2rj3ddl5` 占（同族 self 0.987） | 封档 |
| N7 | USA / TOPSP500 | SECTOR cp3 | prod 0.6906（余量 0.009） | 不交付 |
| N8 | EUR / TOP1200·TOP800·TOP400 | 均为 CROWDING d1 l10 | prod 0.734 / 0.712 / 0.778；后两者 IS 亦不过 | 全域 prod 墙 |
| N9 | GLB / MINVOL10M | INDUSTRY 0.748 / CROWDING l12 0.698 | 余量 ≤0.002 | 只有 SLOW 可用（已提交） |
| N10 | GLB / MINVOL10M | MARKET | 0.762 | 族越细 prod 越高 |
| N11 | KOR / TOP600 | CROWDING l14 | self **0.935** | 组件数↑⇒self↑ |
| N12 | IND / TOP500 | CROWDING l10 | self 0.7733 / prod 0.7733 | 双撞 |
| N13 | GBR / DEU | 严格 selection | 组件 <10 报错 | 小池只能用宽松 selection |
| N14 | MEA 全区 | 任意 | 400 `Region MEA is not available.` | 平台下架 |

---

## 6. 执行清单

### 6.1 构建命令（复现本轮全部候选）

```bash
cd /d/coding/traeCN_project/wqb

# ① 组件池 + 档位 + pyramid（先清缓存，否则吃到 7 天旧数据）
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  results/sa_scan_20261027_night/refresh_pool.py
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  results/sa_scan_20261027_night/fetch_super.py
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  results/sa_scan_20261027_night/slot_scan.py

# ② 建 SA（后台，勿用管道，nohup 写日志）
nohup D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261027_night/configs_v15.json \
  --out     results/sa_scan_20261027_night/res_v15.jsonl \
  > results/sa_scan_20261027_night/run_v15.log 2>&1 &
```

**configs 模板**（`selectionLimit` 必须 ≥10）：
```json
{"tag":"usa_top500_crowding_cp5","region":"USA","universe":"TOP500","delay":1,
 "neutralization":"CROWDING","decay":1,"combo_power":5,"selection_limit":10,"truncation":0.02}
```

### 6.2 配额约束

| 项 | 限制 | 说明 |
|---|---|---|
| SUPER 提交 | **1 / 天 / region** | 与 REGULAR 4/天/区**独立计数** |
| REGULAR 提交 | 4 / 天 / region | — |
| prod 并发 | **账号级 1** | 多进程并发必现 `correlation_busy` / `None`，**不要为提速开多进程** |
| 仿真时长 | 单档 6–8 min | 一批 4 档 ≈ 30 min |

### 6.3 建议执行顺序（若用户决定提交）

1. **首选**：`78LAAZx1`（USA/TOP500，cp4，prod 今晚 23:55 实测 0.6530）。
   ```bash
   cd /d/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 \
     world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py \
     submit --alpha-id 78LAAZx1 --region USA
   ```
2. **替代**：`78LAAm92`（cp5）。**提交前必须先跑一次 `check_correlation(refresh=True)`**，因本轮未取到 prod。
3. **提交前**：确认没有后台 `sa_run.py` 在跑（并发会让 `_probe_prod_max` 抛 ProxyError 中止，无副作用但需重试）。
4. **提交后**：等满 **~250s flip 窗**，用 `tools/super_build.py status --alpha-id <id>` 复核 `status=ACTIVE`，**不看 POST 回执**。
5. 提交后 **USA/TOP500 即封档**，其余三颗同档候选同时作废 ⇒ 只出 1 席。

### 6.4 下一轮（10-28 夜）候选动作

| 优先级 | 动作 | 触发条件 |
|---|---|---|
| 1 | 复核 `78LAAm92`（cp5）prod | prod 队列空闲时，8×40s 患者式重试 |
| 2 | 若 USA/TOP500 已被提交 ⇒ 全域无 ZERO-OS 空档，**SA 线整体转停** | 等平台新增 universe |
| 3 | 验证 `USA / ILLIQUID_MINVOL1M` 是否可新建 | 该档有 4 颗 REGULAR 但不在 platform options |
| 4 | 不再扫 EUR / GLB / IND / KOR / DEU / GBR | 已确认饱和或 prod 墙 |

---

## 7. 本轮方法论增量（可复用）

1. **`combo_power` 的真实约束是 IS Ladder，不是 prod**。prod 对 cp 完全不敏感（三次独立实测逐位相同 0.6530），但 2Y Sharpe 随 cp 缓慢上行并在 cp6 精确撞线（1.58==1.58）。⇒ **推 cp 时必须同步看 2Y，不能用"prod 没变"当作安全信号。**
2. **组件池 = (region, delay) 双键**。`USA/TOP500 d0` 的 400 不是配置错误，而是 d0 池为空。跨 delay"借池"是伪命题。
3. **"零占用档"是唯一能把 self 压到 0 的结构**。USA/TOP500 四颗候选 self 全 0.0000，与 EUR/GLB 的"零 SA 档"（self 0.28–0.33）不同 —— 后者仍有 REGULAR OS 持仓重合。
4. **池子增长 ≠ 产能增长**。GLB +5 组件（+31%）对产出零贡献，因为四档全被占。**判据应看"未被占用的 (region, universe)"，不是池大小。**
5. **prod 队列是全局单并发资源**。本轮 cp5/prod 复测连续 5 次返回 `null`（并行 campaign 占用），夜间自动化必须给 prod 步骤留 2–3 倍时间预算，并准备"以同族已测值代理"的兜底。

---

*本报告由夜间自动化生成；全部配方未提交。prod/self 实测值已标注取数时间，超过 48h 需 `refresh=True` 重测。*
