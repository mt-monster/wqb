# 各 Region 最优 SuperAlpha 方案 — 2026-10-25 全流程扫描

> 生成时间：2026-10-25 23:40 → 2026-10-26 02:0x（GMT+8）
> 工作目录：`D:\coding\traeCN_project\wqb`
> 产物目录：`results/sa_scan_20261025/`（pool_refresh.json / super_list.json / universes.json / slots_classified.json / gates_refresh.json / gates_v9.json / configs_v9.json / configs_v10.json / res_v9.jsonl / run_*.log）
> **本报告全部为待执行配方，未做任何提交动作**（只挖不提交铁律）。

---

## 0. 执行摘要（按价值排序的优先队列）

| # | 优先级 | 区域/档位 | 配方 | 状态 | IS (S/F/TO) | 双闸 prod / self | 余量 | 动作 |
|---|---|---|---|---|---|---|---|---|
| 1 | **P0** | USA / TOP500 | CROWDING d1 l10 **cp3** (`P0MRkP0M`) | **已建、未提交、SAFE** | **1.77** / **1.29** / **0.1606** | **0.6530** / **0.0000** | **0.047 / 0.700** | **★ 首选，等用户点名提交** |
| 2 | **P0** | USA / TOP500 | CROWDING d1 l10 cp1 (`LL5rpRY2`) | **已建、未提交、SAFE** | 1.74 / 1.25 / 0.1647 | 0.6530 / 0.0000 | 0.047 / 0.700 | 次选（同档同族，四项均弱于 #1） |
| 3 | P1 | USA / TOPSP500 | **SECTOR** d1 l10 (`6XAWkbw7`) | 已建、fails=[] PASS | **1.83** / **1.35** / 0.1575 | 0.6906 / 0.0000 | **0.0094** | 余量 <0.02 ⇒ **不交付**，留档观察漂移 |
| 4 | P2 | EUR / TOP2500 | CROWDING d1 l10 (`kqJOQgnk`) | **已提交 ACTIVE**（10-23） | 3.92 / 3.40 / 0.1481 | 0.6546 / 0.5765 | 0.045 / 0.124 | 封档 |
| 5 | P3 | GLB / MINVOL10M | CROWDING d1 l10 (`Vkd5pK6M`) | 已建 | 4.25 / 2.66 / 0.2395 | 0.6917 / 0.0000 | **0.0083** | 余量不足 ⇒ 不交付 |
| 6 | P3 | GBR / TOP700 | SLOW d1 l10 (`1YjPdQJR`) | 已建 | 3.95 / 3.29 / 0.1710 | 0.6983 / 0.6985 | **0.0017 / 0.0015** | 双闸同时贴边 ⇒ 不交付 |

**本轮结论一句话**：
- **USA 是唯一仍有产能的区域**：ZERO-OS 空档三个（TOP200/TOP500/TOPSP500），prod 全线健康（0.53–0.69），本轮在 TOP500 与 TOPSP500 各打出一颗 `fails=[]` PASS，其中 **`P0MRkP0M` 双闸余量 0.047/0.700 达标，是本轮唯一新增可交付**。
- **★ 新发现：`combo_power=3`（组合权重 `w³`）在 USA/TOP500 上是纯增益** —— S 1.74→**1.77**、F 1.25→**1.29**、TO 0.1647→**0.1606**，且 **prod 完全不动（0.6530）**、fails 从 `[]` 保持 `[]`。⇒ 这是继 CROWDING 之后第二个有效杠杆，且**不动 prod 轴**（与换族/加 limit 截然不同）。
- **★ 新发现：`SECTOR` 是唯一能破 USA/TOPSP500 IS Ladder 的中性化族**（CROWDING/STATISTICAL/MARKET/SUBINDUSTRY 全部 2Y FAIL），但代价是 prod 抬到 0.6906（余量仅 0.0094）。
- **★ 新发现：`decay` 在 SA 组合层完全无效** —— TOPSP500 CROWDING d0 与 d1 的 S/F/TO/prod **四项逐字相同**（1.70/1.16/0.1566/0.6246）。组件 alpha 各自已带 decay，SA 层再设不产生任何差异。
- **严格 selection 是负杠杆**：USA/TOP500 `(1-self)*(TO<0.3)*(prod<0.6)` ⇒ S 1.74→**1.47**、TO 反而升到 0.1448 无损、prod 未改善。论坛严格阈值在 USA 档位不适用。
- **limit↑ ⇒ prod↑ 铁律再证**：TOPSP500 CROWDING l10 0.6246 → l20 **0.7198** 撞墙；TOP500 CROWDING l10 0.6530（fails=[]）→ l12 0.6588 但 **IS Ladder FAIL**。
- **EUR 三个 ZERO-OS 空档全线撞 prod 墙**（TOP1200 0.7337 / TOP800 0.7117 / TOP400 0.7783），`gJWdxLbM` 48h 漂移 0.6988→**0.7666** 已确认 ⇒ **EUR 全域停投**。

---

## 1. 数据基线

### 1.1 组件池 eligibility 表（口径：stage=OS + type=REGULAR + status=ACTIVE，region 级）

取数前已清 `api_cache`（`DELETE FROM api_cache WHERE cache_key LIKE '%user_alphas%'`，清出 6 条 + 1 条 alpha*）。

| Region | 组件池 | 上轮(10-24) | Δ | 判定 | ACTIVE REGULAR 的 universe 分布 |
|---|---|---|---|---|---|
| IND | **52** | 51 | +1 | GO（池最大） | TOP500: 52 |
| USA | **49** | 49 | 0 | **GO（唯一有空档）** | TOP3000:38, TOP2000:6, TOP1000:1, ILLIQUID_MINVOL1M:4 |
| KOR | **38** | 37 | +1 | GO（但单 universe 已饱和） | TOP600: 38 |
| MEA | 21 | 21 | 0 | **BLOCKED — 平台已下架**（见 §1.4） | TOP400: 21 |
| GBR | 20 | 20 | 0 | GO（无空档） | TOP700: 20 |
| EUR | 18 | 18 | 0 | GO（但空档全撞 prod 墙） | TOPCS1600:10, TOP2500:8 |
| GLB | 15 | 15 | 0 | GO | MINVOL1M:12, TOPDIV3000:2, TOP3000:1 |
| DEU | 11 | 11 | 0 | GO（无空档） | TOP500: 11 |
| ASI | 9 | 9 | 0 | **BLOCKED**（<10 平台硬下限） | MINVOL1M:6, MINVOL10M:3 |
| HKG | 6 | 6 | 0 | **BLOCKED**（<10 硬下限） | TOP800: 6 |
| CHN / JPN / TWN / AMR | 0 | — | — | 无组件 | — |

### 1.2 平台权威 universe 清单（EQUITY，来自 `get_platform_setting_options`）

| Region | delay | 合法 universe |
|---|---|---|
| USA | 0 / 1 | TOP3000, TOP2000, TOP1000, **TOP500, TOP200, TOPSP500** |
| EUR | 0 / 1 | TOP2500, **TOP1200, TOP800, TOP400**, TOPCS1600 |
| GLB | 1 | TOP3000, MINVOL1M, **MINVOL10M**, TOPDIV3000 |
| ASI | 1 | MINVOL1M, MINVOL10M, **TOP500** |
| HKG | 1 | TOP800, **TOP500** |
| KOR | 1 | TOP600 |
| IND | 1 | TOP500 |
| DEU | 0 / 1 | TOP500 |
| GBR | 0 / 1 | TOP700 |
| AMR | 0 / 1 | TOP600 |
| CHN | 0 / 1 | TOP2000U |
| **MEA** | — | **不在清单 ⇒ 平台已下架（二次确认）** |

### 1.3 档位占用分类表（region × universe）

分类口径：`ZERO-OS` = 该档无任何 ACTIVE OS alpha（REGULAR+SUPER）⇒ **self 恒 0.0000**；
`ZERO-SA` = 有 REGULAR 但无 SUPER ⇒ self 非零但偏低；`OCCUPIED` = 已有 SUPER 占用。

| Region | Universe | 池 | REG ACTIVE | SUPER ACTIVE | 分类 | 本轮结论 |
|---|---|---|---|---|---|---|
| **USA** | **TOP500** | 49 | 0 | 0 | **ZERO-OS** | ✅ **CROWDING l10 / l10-cp3 双 PASS** |
| **USA** | **TOPSP500** | 49 | 0 | 0 | **ZERO-OS** | ⚠ SECTOR l10 PASS 但 prod 余量 0.0094 |
| USA | TOP200 | 49 | 0 | 0 | **ZERO-OS** | ❌ S 0.94–1.28 全崩（prod 0.62–0.69 健康） |
| USA | TOP3000 | 49 | 38 | 3 | OCCUPIED | ❌ prod 0.7433 撞墙 |
| USA | TOP2000 | 49 | 6 | 1 | OCCUPIED | 未测（self 风险高） |
| USA | TOP1000 | 49 | 1 | 1 | OCCUPIED | 未测 |
| EUR | TOP1200 | 18 | 0 | 0 | **ZERO-OS** | ❌ prod 0.7337 撞墙 |
| EUR | TOP800 | 18 | 0 | 0 | **ZERO-OS** | ❌ S1.40 + prod 0.7117 |
| EUR | TOP400 | 18 | 0 | 0 | **ZERO-OS** | ❌ S1.23 + prod 0.7783 |
| EUR | TOP2500 | 18 | 8 | 2 | OCCUPIED | ✅ `kqJOQgnk` 已 ACTIVE |
| EUR | TOPCS1600 | 18 | 10 | 1 | OCCUPIED | ❌ `gJWdxLbM` 漂移 0.7666 |
| GLB | MINVOL10M | 15 | 0 | 0 | **ZERO-OS** | ⚠ CROWDING 0.6917 余量 0.0083 |
| GLB | MINVOL1M | 15 | 12 | 2 | OCCUPIED | 未测 |
| GLB | TOP3000 | 15 | 1 | 1 | OCCUPIED | ❌ 0.864 撞墙 |
| GLB | TOPDIV3000 | 15 | 2 | 1 | OCCUPIED | 未测 |
| IND | TOP500 | 52 | 52 | **11** | OCCUPIED（最挤） | ❌ CROWDING l10 双闸 0.7733 |
| KOR | TOP600 | 38 | 38 | 9 | OCCUPIED | ❌ l10 0.673 / l14 0.935 |
| GBR | TOP700 | 20 | 20 | 2 | OCCUPIED | ⚠ SLOW 0.6983/0.6985 双贴边 |
| DEU | TOP500 | 11 | 11 | 1 | OCCUPIED | ❌ 0.764 撞墙 |
| MEA | TOP400 | 21 | 21 | 2 | OCCUPIED | ❌ 平台下架 |
| ASI | TOP500 | 9 | 0 | 0 | ZERO-OS | ❌ 池 9 < 10 硬下限 |
| HKG | TOP500 | 6 | 0 | 0 | ZERO-OS | ❌ 池 6 < 10 硬下限 |
| ASI | MINVOL1M / MINVOL10M | 9 | 6 / 3 | 0 | ZERO-SA | ❌ 池不足 |
| HKG | TOP800 | 6 | 6 | 0 | ZERO-SA | ❌ 池不足 |

> **ACTIVE OS SUPER 总数 = 37**（与 10-24 完全一致）⇒ 本轮用户未提交任何 SA，`LL5rpRY2` 仍为 UNSUBMITTED。

### 1.4 Pyramid 倍率表（各区域最大值，明细见 `pool_refresh.json`）

| Region | D0 最高 | D1 最高 | 备注 |
|---|---|---|---|
| USA | 1.8 (sentiment) | 1.4 (other) | 类别最全，15 类 |
| DEU | 1.9 (model) | 1.8 (model) | 倍率最高但无空档 |
| GBR | 1.9 (news) | 1.7 (sentiment) | |
| EUR | 1.7 (other) | 1.5 (other) | |
| KOR | — | 1.6 (analyst) | 仅 D1 |
| IND | — | 1.4 (analyst) | 仅 D1 |
| GLB | — | 1.4 (fundamental) | 仅 D1 |
| ASI | — | 1.5 (analyst) | |
| HKG | — | 1.7 (analyst) | |
| AMR / CHN | 1.9 / 1.9 (sentiment / fundamental) | 1.7 / 1.9 | 无组件池 |
| **MEA** | — | — | **不在 pyramid 清单，确认下架** |

---

## 2. 选点原则

1. **档位占用类型 > 组件池大小**。IND 池 52 最大但 TOP500 已堆 11 颗 SUPER ⇒ self 0.77 双撞；USA 池 49 但有 3 个 ZERO-OS 空档 ⇒ self=0，这才是唯一可交付来源。
   - 优先序：`ZERO-OS` > `ZERO-SA` > `OCCUPIED`（同档换配方）。
2. **指标 = 约束优化**：`max IS Sharpe s.t. self<0.7 且 prod<0.7`，优选 `prod<0.6` 且 `TO<0.30`（社区合格档）。
3. **prod 是档位属性不是配方属性**（10-24 发现，本轮再证）：USA 空档 prod 0.53–0.69 全健康；EUR 空档 0.71–0.78 全撞墙。换族只能在同一档位内平移 prod ±0.05，救不了一个坏档位。
4. **中性化族规律（本轮 USA 实测）**：

   | 档位 | 族 | S | F | prod | 结论 |
   |---|---|---|---|---|---|
   | TOPSP500 | CROWDING l10 | 1.70 | 1.16 | **0.6246** | prod 最优，但 2Y FAIL |
   | TOPSP500 | STATISTICAL l10 | 1.52 | 0.72 | **0.5294** | **prod 最健康**，S 不足 |
   | TOPSP500 | SECTOR l10 | **1.83** | **1.35** | 0.6906 | **唯一破 Ladder**，prod 贴边 |
   | TOPSP500 | MARKET l10 | — | — | 0.694 | 2Y 1.55 FAIL |
   | TOPSP500 | SUBINDUSTRY l10 | — | — | 0.7479 | 撞墙 |
   | TOP500 | CROWDING l10 | 1.74 | 1.25 | 0.6530 | **SAFE** |
   | TOP500 | CROWDING l10 **cp3** | **1.77** | **1.29** | **0.6530** | **★ 纯增益：S↑ F↑ TO↓ 而 prod 纹丝不动** |
   | TOP500 | CROWDING l12 | 1.75 | 1.34 | 0.6588 | Ladder FAIL |
   | TOP500 | FAST l10 | 1.63 | 0.86 | 0.6665 | 8Y 1.52 FAIL |
   | TOP500 | SLOW l10 | 1.35 | 0.60 | 0.6317 | S 崩 |

   ⇒ **族越粗（SECTOR/MARKET/SUBINDUSTRY）prod 越高、越易破 Ladder；族越细（CROWDING/STATISTICAL）prod 越低但 Ladder 难过**。USA/TOPSP500 上 SECTOR 是唯一交点。
5. **limit 是双刃**：l10 是双闸甜点；l12/l20 一律推高 prod 0.005–0.095 且常引入 Ladder FAIL。
6. **decay 在 SA 组合层无效**（本轮新证，d0 ≡ d1 四项逐字相同）⇒ 不必再扫 decay 轴。
7. **严格 selection 是负杠杆**（USA/TOP500 S −0.27）⇒ 论坛 `(TO<0.3)*(prod<0.6)` 阈值只适用于 IND/USA 大池，**且实测在 USA 反而伤 S**；小池区禁用（组件 <10 直接 400）。

---

## 3. 论坛指标标准（引用 §0 固化标准，来源：2026-10-22 论坛调研定稿）

### 3.1 组成数量（Selection Limit）
- 平台硬下限 **10**（<10 ⇒ 400 `Ensure this value is greater than or equal to 10`）
- 论坛 78 赞帖建议 30–100 起测、≤500；LY43440 实测 IND 取 300
- **实际生效数 = min(limit, 组件池)**；组件池是 **region 级**而非 universe 级

### 3.2 指标三档
| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

> 本轮 `6XAWkbw7`（S1.83/F1.35/TO0.1575）落在 A 档 + TO 达 B 档，但 **prod 0.6906 未达 B 档 0.6** ⇒ 只能算 A 档边缘。

### 3.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`；`author_returns_to_drawdown>2`（官方建议 1–4）。
⚠ **筛选强度必须匹配池子规模**：加严后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。

### 3.4 中性化族规律（论坛）
Fitness 排序（IND 实测）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**；选族：TO<0.10 → SLOW，TO>0.20 → FAST。
⚠ 本轮 USA 实测与论坛 IND 结论**方向不一致**（USA/TOPSP500 上 SECTOR 才是破 Ladder 的族）⇒ **不可跨区外推**。

### 3.5 其他
- truncation 0.02 vs 0.08 对 SA 几乎无差异；论坛推荐 `Selection Handling = Non-Zero`，本工作区 37 颗 SA 全用 `POSITIVE` 均成功。

---

## 4. 分 Region 方案

### 4.1 USA —— **唯一活跃区（P0/P1）**

**基线**：池 49；ZERO-OS 空档 3 个（TOP500 / TOPSP500 / TOP200）；prod 全线健康。

| 档位 | 最优配方 | IS S/F/TO | prod / self | 余量 | 判定 |
|---|---|---|---|---|---|
| **TOP500** | CROWDING d1 l10 **cp3** `P0MRkP0M` | **1.77** / **1.29** / **0.1606** | 0.6530 / 0.0000 | **0.047 / 0.700** | **★ SAFE 可交付（首选）** |
| **TOP500** | CROWDING d1 l10 cp1 `LL5rpRY2` | 1.74 / 1.25 / 0.1647 | 0.6530 / 0.0000 | 0.047 / 0.700 | SAFE 可交付（次选） |
| TOPSP500 | **SECTOR** d1 l10 `6XAWkbw7` | 1.83 / 1.35 / 0.1575 | 0.6906 / 0.0000 | **0.0094** | 边缘 PASS，**不交付** |
| TOPSP500 | STATISTICAL d1 l10 `E5VjjdkL` | 1.52 / 0.72 / 0.1981 | **0.5294** / 0.0000 | **0.1706** | prod 最健康，S 不足 |
| TOP200 | 任何族 | ≤1.28 | 0.62–0.69 | — | S 天花板不足，判死 |

**下一步配方队列（configs_v10.json，已备好未执行）**：
1. `usa_tops500_sector_d1_l10_strict` —— 用严格 selection 把 SECTOR 的 prod 从 0.6906 压到 <0.67（本轮 TOP500 上严格 selection 已证明能压 TO，对族内 prod 的效果待测）
2. `usa_tops500_sector_d0_l10` / `usa_tops500_sector_d1_l10_cp3` —— SECTOR 族内提 S
3. `usa_tops500_statistical_d1_l20 / l30` —— 从 prod 0.5294 起加组件把 S 推过 1.58（prod 余量 0.17 有充足空间）
4. `usa_tops500_industry_d1_l10` —— SECTOR 与 SUBINDUSTRY 之间的中间档

### 4.2 EUR —— **停投（全域 prod 墙）**

| 档位 | 分类 | 实测 prod | 判定 |
|---|---|---|---|
| TOP2500 | OCCUPIED | 0.6546 | ✅ `kqJOQgnk` 已 ACTIVE，封档 |
| TOPCS1600 | OCCUPIED | **0.7666**（10-23 为 0.6988） | ❌ 48h 漂移 +0.068 |
| TOP1200 | ZERO-OS | **0.7337** | ❌ 墙 |
| TOP800 | ZERO-OS | **0.7117** + S1.40 | ❌ 墙 |
| TOP400 | ZERO-OS | **0.7783** + S1.23 | ❌ 墙 |

⇒ 三个 ZERO-OS 空档 self 均为 0（档位价值本应最高），但 **prod 全部 >0.70**。**prod 是档位属性**，换族/换 limit/换 decay 均救不回 ⇒ **EUR 全域停投**，仅维持已 ACTIVE 的 `kqJOQgnk`。

### 4.3 GLB —— 低优先（仅 MINVOL10M 空档，prod 贴边）

| 档位 | 配方 | IS | prod / self | 余量 |
|---|---|---|---|---|
| MINVOL10M | CROWDING d1 l10 `Vkd5pK6M` | 4.25 / 2.66 / 0.2395 | 0.6917 / 0.0000 | **0.0083** |
| MINVOL10M | MARKET d1 l10 | — | 0.7620 | ❌ |
| TOP3000 | CROWDING | — | 0.8640 | ❌ |
| MINVOL1M / TOPDIV3000 | OCCUPIED | — | 未测 | 次选 |

⇒ 池 15 太小，MINVOL10M 是唯一空档但 CROWDING prod 0.6917 余量 <0.02。**SLOW / INDUSTRY 两档本轮因账号相关度锁被占未建成**，留作 v10 备选。

### 4.4 IND / KOR / DEU / GBR —— 停投（无空档）

| Region | 池 | 唯一/主 universe | SUPER 已占 | 判定 |
|---|---|---|---|---|
| IND | 52 | TOP500（唯一） | **11** | 池最大但最挤，CROWDING l10 双闸 **0.7733** |
| KOR | 38 | TOP600（唯一） | 9 | l10 0.673 / l14 **0.935** |
| DEU | 11 | TOP500（唯一） | 1 | 0.764 撞墙 |
| GBR | 20 | TOP700（唯一） | 2 | SLOW 0.6983/0.6985 双贴边 |

⇒ 单 universe 区域 = 同档无限堆叠，self 只增不减。**池子增长不转化为产能**。

### 4.5 MEA / ASI / HKG / CHN / JPN / TWN / AMR —— 停投（硬约束）

- **MEA**：平台已下架 —— `get_platform_setting_options` 的 EQUITY 清单中**无 MEA**，且 pyramid 列表也无 MEA，叠加 10-24 实测 `400 Region MEA is not available.`。历史 2 颗 8 月 SA 仍 ACTIVE。**21 池作废。**
- **ASI 9 / HKG 6**：<10 平台硬下限，`sim ERROR: At least 10 component alphas are required`。
- **CHN / JPN / TWN / AMR**：零组件池。

---

## 5. 撞墙档案（已验证不可用，勿重复）

| 档位 | 配方 | 死因 |
|---|---|---|
| USA/TOP3000 | CROWDING d1 l10 | prod **0.7433** |
| USA/TOP200 | CROWDING l10 | S **0.94**；l30 S 1.28 + prod 0.6942 |
| USA/TOPSP500 | CROWDING l10 | 2Y **1.50** FAIL（prod 0.6246 健康） |
| USA/TOPSP500 | CROWDING **l20** `ZYm8JK80` | prod **0.7198** + Ladder FAIL |
| USA/TOPSP500 | CROWDING l10 cp3 `2rjgY38P` | prod **0.6933** + Ladder FAIL |
| USA/TOPSP500 | MARKET l10 | 2Y 1.55 FAIL |
| USA/TOPSP500 | SUBINDUSTRY l10 | prod **0.7479** |
| USA/TOP500 | SLOW l10 | S **1.35** |
| USA/TOP500 | FAST l10 | F 0.86 + 8Y 1.52 FAIL |
| USA/TOP500 | CROWDING **l12** `leMnoxLA` | IS Ladder FAIL（prod 0.6588 尚可） |
| USA/TOP500 | CROWDING l10 **strict** `MP0EJLLz` | S **1.47**（严格 selection 伤 S） |
| EUR/TOPCS1600 | CROWDING l10 `gJWdxLbM` | prod **0.7666**（漂移自 0.6988） |
| EUR/TOP1200 | CROWDING l10 `npAQgjYM` | prod **0.7337** |
| EUR/TOP800 / TOP400 | CROWDING l10 | prod **0.7117 / 0.7783** |
| GLB/TOP3000 | CROWDING | prod **0.8640** |
| GLB/MINVOL10M | MARKET l10 | prod **0.7620** |
| IND/TOP500 | CROWDING l10 `leMYEjgN` | self & prod **0.7733 双撞** |
| KOR/TOP600 | CROWDING l14 | self **0.935** |
| DEU/TOP500 | CROWDING | prod **0.7640** |
| GBR/TOP700 | SLOW l10 `1YjPdQJR` | prod 0.6983 + self 0.6985 **双贴边** |
| GBR/TOP700 | 严格 selection | 组件 <10 ⇒ **400 ERROR** |
| MEA 全区 | 任意 | **400 Region not available** + 平台清单已除名 |

---

## 6. 执行清单

### 6.1 立即可执行的下一步（v10，配置已就绪）

```bash
cd C:/Users/MENGTAO/wqb-scripts
nohup D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe sa_run.py \
  --configs D:/coding/traeCN_project/wqb/results/sa_scan_20261025/configs_v10.json \
  --out D:/coding/traeCN_project/wqb/results/sa_scan_20261025/res_v10.jsonl \
  > D:/coding/traeCN_project/wqb/results/sa_scan_20261025/run_v10.log 2>&1 &
```

`configs_v10.json` 六档（全部 USA/TOPSP500）：SECTOR-strict / SECTOR-d0 / SECTOR-cp3 / STATISTICAL-l20 / STATISTICAL-l30 / INDUSTRY-l10。

**补测 prod**（v9 遗留）：
```bash
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  D:/coding/traeCN_project/wqb/results/sa_scan_20261025/refresh_gates.py
```

### 6.2 配额与并发约束

- **SUPER 配额 1/天/区**，与 REGULAR 4/天/区独立计数 ⇒ 队列按「一天一区一颗」排期。
- **账号级 prod 相关度单并发**：本轮 `P0MRkP0M` 补测因 `corr-lock Busy`（IND/USA/KOR campaign lane 在跑）阻塞 ⇒ **跑 SA 批次前先确认无 campaign lane 占锁**，否则 prod 恒为 None。
- 单档仿真 ~6–8 分钟；一批 6 档 ≈ 45 分钟。

### 6.3 建议执行顺序

1. **提交 `P0MRkP0M`（若用户点名）** —— 本轮首选，S/F/TO 全面优于 `LL5rpRY2` 而双闸完全相同。提交前先停后台批次，等满 250s flip 窗后 `status` 复核。
2. **v10 追加 `usa_top500_crowding_d1_l10_cp4/cp5`** —— cp3 已证纯增益，继续推幂次看 S/F 是否继续单调升（prod 不动则无风险）。
3. 跑 v10 六档（USA/TOPSP500 破 Ladder + 降 prod 双目标）。
4. GLB/MINVOL10M 补 SLOW / INDUSTRY 两档（低优先）。
5. EUR / IND / KOR / DEU / GBR / MEA / ASI / HKG 本轮不排期。

### 6.4 提交命令（仅当用户明确点名某颗 alpha）

```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id <id> --region <REGION>
# 内置 prod 闸 0.7，fail-closed，无豁免参数
# 等满 ~250s flip 窗后：
world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py status --alpha-id <id>
```

⚠ 提交前必先停掉后台 `sa_run.py` 批次（并发加剧代理不稳，会导致 `_probe_prod_max` 抛 ProxyError 中止）。
⚠ 提交前必 `check_correlation(refresh=True)` 重测（台账 >48h 不可信，本轮 `gJWdxLbM` 再证）。

---

## 7. 铁律复核

- ✅ **只挖不提交** —— 本轮无任何提交动作，全部为待执行配方。
- ✅ **prod ≥ 0.7 = 合规红线，无豁免** —— `6XAWkbw7`(0.6906) / `Vkd5pK6M`(0.6917) / `1YjPdQJR`(0.6983) 三颗虽 PASS 但余量 <0.02，一律**不交付**。
- ✅ 组件池只看 ACTIVE 已提交 REGULAR（IS 阶段 UNSUBMITTED 不计入）。
- ✅ 台账 prod 已全部 `refresh=True` 重测（7 颗存量 + 6 颗新建）。
- ✅ **余量 ≥0.02 才算安全** —— 本轮达标者两颗：`P0MRkP0M` 与 `LL5rpRY2`，双闸余量均为 0.047 / 0.700（前者 S/F/TO 全面更优）。
- ✅ 本轮实测全部 `refresh=True`（7 颗存量 + 6 颗新建，其中 `P0MRkP0M` 网络重试 27 次 / 497s 才拿到 PC，勿因超时判死）。
