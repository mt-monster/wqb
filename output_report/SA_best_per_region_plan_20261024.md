# 各 Region 最优 SuperAlpha 方案 — 2026-10-24 全流程扫描

> 生成时间：2026-10-24 23:41 → 2026-10-25 01:0x（GMT+8）
> 工作目录：`D:\coding\traeCN_project\wqb`
> 产物目录：`results/sa_scan_20261024/`（pool_refresh.json / super_list.json / slots_classified.json / gates_refresh.json / res_v7.jsonl / res_v8.jsonl）
> **本报告全部为待执行配方，未做任何提交动作**（只挖不提交铁律）。

---

## 0. 执行摘要（按价值排序的优先队列）

| # | 优先级 | 区域/档位 | 配方 | 状态 | 双闸（prod / self） | 余量 | 动作 |
|---|---|---|---|---|---|---|---|
| 1 | **P0** | USA / TOP500 | CROWDING d1 l10 (`LL5rpRY2`) | **已建、未提交、SAFE** | 0.6530 / **0.0000** | 0.047 / 0.700 | **等用户点名提交** |
| 2 | P1 | GLB / MINVOL10M | CROWDING d1 l10 (`Vkd5pK6M`) | 已建 | 0.6917 / 0.0000 | **0.008** | 余量 <0.02 ⇒ **不交付**，仅留档 |
| 3 | P1 | USA / TOPSP500 | CROWDING d1 l10 → 2Y 1.50 FAIL | 撞墙 | 0.6246 / 0.0000 | 0.075 | 需换族提 2Y（MARKET SUBINDUSTRY 均失败） |
| 4 | P2 | EUR / TOP2500 | CROWDING d1 l10 (`kqJOQgnk`) | **已提交 ACTIVE**（10-23） | 0.6546 / 0.5765 | 0.045 / 0.124 | 封档，EUR 本日配额已用 |
| 5 | P2 | GBR / TOP700 | SLOW d1 l10 (`1YjPdQJR`) | 已建 | 0.6983 / 0.6985 | **0.0017** | 余量过薄 ⇒ 不交付 |
| 6 | — | EUR / TOPCS1600 | CROWDING d1 l10 (`gJWdxLbM`) | **prod 漂移失效** | 0.6988 → **0.7666** | −0.067 | **台账刷新后判死** |

**本轮结论一句话**：
- 组件池全面增长（IND 38→**51**、USA 44→**49**、KOR 28→**37**、EUR 14→**18**、GLB 11→**15**），但**新增池子全部落在已饱和档位**（IND/KOR 单 universe），**未转化为新的可交付 SA**。
- **唯一新增可交付 = `LL5rpRY2`（USA/TOP500 零 OS 档）**。
- **MEA 已被平台停用**（新建仿真 400 `Region MEA is not available.`）⇒ 21 池作废，MEA 转停投区。
- 上一轮判 PASS 的 `gJWdxLbM`（EUR/TOPCS1600）**prod 48h 内从 0.6988 漂到 0.7666**，证实「台账 prod >48h 不可信」铁律。

---

## 1. 数据基线

### 1.1 组件池 eligibility 表（口径：stage=OS + type=REGULAR + status=ACTIVE，region 级）

| Region | 组件池 | 上轮(10-23) | Δ | 判定 | OS REGULAR ACTIVE 的 universe 分布 |
|---|---|---|---|---|---|
| IND | **51** | 38 | **+13** | GO（池最大） | TOP500: 51 |
| USA | **49** | 44 | +5 | GO | TOP3000:38, TOP2000:6, TOP1000:1, ILLIQUID_MINVOL1M:4 |
| KOR | **37** | 28 | +9 | GO | TOP600: 37 |
| MEA | 21 | 19 | +2 | **BLOCKED**（平台 400：Region not available） | TOP400: 21 |
| GBR | 20 | 18 | +2 | GO | TOP700: 20 |
| EUR | 18 | 14 | +4 | GO | TOPCS1600:10, TOP2500:8 |
| GLB | 15 | 11 | +4 | GO | MINVOL1M:12, TOPDIV3000:2, TOP3000:1 |
| DEU | 11 | 10 | +1 | GO | TOP500: 11 |
| ASI | 9 | 9 | 0 | **BLOCKED**（<10 硬下限） | MINVOL1M:6, MINVOL10M:3 |
| HKG | 6 | 6 | 0 | **BLOCKED**（<10 硬下限） | TOP800: 6 |
| CHN / JPN / TWN / AMR | 0 | — | — | 无组件 | — |

> ⚠ 取数前已 `DELETE FROM api_cache WHERE cache_key LIKE '%user_alphas%'`（`--refresh` 单独使用仍吃 7 天 TTL，会漏当日提交）。本轮实测清出 25 条 user_alphas 缓存 + 7 条 alpha* 缓存。

### 1.2 档位占用分类表（region × universe）

分类口径：`ZERO-OS` = 该档无任何 ACTIVE OS alpha（REGULAR+SUPER）⇒ **self 恒 0.0000**；
`ZERO-SA` = 有 REGULAR 但无 SUPER；`OCCUPIED` = 已有 SUPER 占用。

| Region | Universe | 组件池 | REG ACTIVE | SUPER ACTIVE | 分类 | 本轮实测 |
|---|---|---|---|---|---|---|
| USA | TOP3000 | 49 | 38 | 3 | OCCUPIED | prod 0.7433 撞墙（10-23） |
| USA | TOP2000 | 49 | 6 | 1 | OCCUPIED | — |
| USA | TOP1000 | 49 | 1 | 1 | OCCUPIED | — |
| **USA** | **TOP500** | 49 | 0 | 0 | **ZERO-OS** | ✅ **S1.74 prod0.653 self0.0 = SAFE** |
| USA | TOP200 | 49 | 0 | 0 | **ZERO-OS** | ❌ S0.94 崩（prod 0.6167 健康） |
| USA | TOPSP500 | 49 | 0 | 0 | **ZERO-OS** | ❌ 2Y 1.50（prod 0.6246 健康） |
| EUR | TOP2500 | 18 | 8 | 2 | OCCUPIED | ✅ 已占（kqJOQgnk 10-23） |
| EUR | TOPCS1600 | 18 | 10 | 1 | OCCUPIED | ❌ prod 0.7666（漂移） |
| EUR | TOP1200 | 18 | 0 | 0 | **ZERO-OS** | ❌ prod 0.7337 |
| EUR | TOP800 | 18 | 0 | 0 | **ZERO-OS** | ❌ S1.40 + prod 0.7117 |
| EUR | TOP400 | 18 | 0 | 0 | **ZERO-OS** | ❌ S1.23 + prod 0.7783 |
| GLB | TOP3000 | 15 | 1 | 1 | OCCUPIED | ❌ self/prod 0.8638 |
| GLB | MINVOL1M | 15 | 12 | 2 | OCCUPIED | — |
| **GLB** | **MINVOL10M** | 15 | 0 | 0 | **ZERO-OS** | ⚠ S4.25 prod0.6917 余量 0.008 |
| GLB | TOPDIV3000 | 15 | 2 | 1 | OCCUPIED | — |
| KOR | TOP600 | 37 | 37 | 9 | OCCUPIED | ❌ l14 self 0.9351 |
| GBR | TOP700 | 20 | 20 | 2 | OCCUPIED | ⚠ self 0.6259~0.6985 |
| DEU | TOP500 | 11 | 11 | 1 | OCCUPIED | ❌ self 0.7642 |
| IND | TOP500 | 51 | 51 | 11 | OCCUPIED | ❌ CROWDING l10 self/prod **0.7733** |
| MEA | TOP400 | 21 | 21 | 2 | OCCUPIED | 🚫 区域停用 |
| MEA | TOP200 | 21 | 0 | 0 | ZERO-OS | 🚫 区域停用（400） |
| ASI | MINVOL1M / MINVOL10M | 9 | 6 / 3 | 0 | ZERO-SA | 🚫 池<10 |
| ASI | TOP500 | 9 | 0 | 0 | ZERO-OS | 🚫 池<10 |
| HKG | TOP800 / TOP500 | 6 | 6 / 0 | 0 | ZERO-SA / ZERO-OS | 🚫 池<10 |
| CHN / JPN / AMR / TWN | 全部 | 0 | 0 | 0 | ZERO-OS | 🚫 无组件 |

### 1.3 Pyramid 倍率表（D0 / D1，avg / max）

| Region | D0 avg / max | D1 avg / max | 备注 |
|---|---|---|---|
| AMR | 1.75 / 1.9 | 1.55 / 1.7 | 无组件 |
| CHN | 1.74 / 1.9 | 1.61 / 1.9 | 无组件 |
| **DEU** | **1.84 / 1.9** | 1.63 / 1.8 | 倍率最高 |
| GBR | 1.69 / 1.9 | 1.44 / 1.7 | |
| USA | 1.53 / 1.8 | 1.16 / 1.4 | |
| HKG | — | 1.41 / 1.7 | 池<10 |
| KOR | — | 1.39 / 1.6 | |
| **EUR** | 1.40 / 1.7 | **1.20 / 1.5** | 可用区中 D1 最低 |
| GLB | — | 1.19 / 1.4 | |
| **IND** | — | **1.14 / 1.4** | D1 全表最低 ⇒ 同 Sharpe 下点塔收益最差 |
| ASI | — | 1.18 / 1.5 | 池<10 |

> 判读：SA 全部走 delay=1（D1）。**IND 的 D1 倍率 1.14 全表最低**，即便 SA 指标好，点塔折算也最吃亏；**DEU 1.63 最高但已 self 撞墙**。

---

## 2. 选点原则

1. **档位占用类型 > 组件池大小**。ZERO-OS 档 self 恒 0.0000，直接消灭一整条闸门；池子再大（IND 51）落在 OCCUPIED 档也是废池（实测 self 0.7733）。
2. **指标 = 约束优化**：`max IS Sharpe s.t. self < 0.7 且 prod < 0.7`，**优选 prod < 0.6 且 TO < 0.30**（社区合格档）。余量 <0.02 一律不交付。
3. **中性化族规律**（本轮再次验证）：
   - 同档 USA/TOP500 三族对照：**CROWDING S1.74 > FAST S1.63 > SLOW S1.35**。CROWDING 仍是 SA 最强族。
   - 但 CROWDING **不改 prod 上限**：USA TOP3000 0.7433、EUR TOP1200 0.7337 换族后依旧撞墙。
   - 换族会**显著动 prod**：USA/TOPSP500 CROWDING 0.6246 → MARKET **0.6940** → SUBINDUSTRY **0.7479**（族越细 prod 越高）。
4. **prod 是档位属性，不是配方属性**：EUR TOP1200/TOP800/TOP400 三个 ZERO-OS 档 prod 分别 0.7337 / 0.7117 / 0.7783，**全部撞墙**；而 USA TOP500/TOP200/TOPSP500 三档 prod 0.653 / 0.6167 / 0.6246，**全部健康**。⇒ **EUR 全域 prod 墙，USA 窄档 prod 健康**。
5. **窄 universe 会压垮 IS**：EUR TOP800 S1.40、TOP400 S1.23、USA TOP200 S0.94，均是「池子够但股票池太窄信号被稀释」。

---

## 3. 论坛指标标准（固化，2026-10-22 定稿）

来源：《【新人入门】Super Alpha 从入门到入门！》78赞/39评论、《2024 super alpha比赛心得》22赞/15评论、《Super Alpha 参数设置》12赞（含 LY43440 实测回复）。

### 3.1 组成数量（Selection Limit）
- 平台硬下限 **10**（<10 直接 400 `Ensure this value is greater than or equal to 10`）
- 论坛建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300
- **实际生效数 = min(limit, 组件池)**；组件池是 **region 级** ⇒ SA 指标天花板由该 region 的 ACTIVE REGULAR 数决定

### 3.2 指标三档
| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

### 3.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`（官方建议 1–4）。
⚠ **筛选强度必须匹配池子规模**：加严后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。**小池区只能用宽松 selection `(1 - self_correlation)`**。

### 3.4 中性化族规律
- Fitness 排序（IND 实测）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**
- 选族规则：**TO<0.10 → SLOW；TO>0.20 → FAST**
- 区域族基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15
- ⚠ **组件数↑ ⇒ self↑ 且 prod↑**（本工作区修正版）：KOR l10 0.673 → l14 **0.935**；USA TOP500 l10 是唯一甜点，不要盲目加大 limit

### 3.5 其他实证
- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区历史 37 颗 SA 全用 POSITIVE 均成功

---

## 4. 分 Region 方案

### 4.1 USA — **本轮唯一可交付区**

| 项 | 值 |
|---|---|
| 组件池 | **49**（全表第 2） |
| 推荐档位 | **TOP500（ZERO-OS ⇒ self 恒 0）** |
| 最优配方 | `neutralization=CROWDING, delay=1, selectionLimit=10, decay=1, truncation=0.02, selectionHandling=POSITIVE, maxTrade=OFF, componentActivation=IS, nanHandling=ON` |
| selection 表达式 | `(1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)` |
| 已建 alpha | **`LL5rpRY2`** |
| IS 指标 | Sharpe **1.74** / Fitness **1.25** / Turnover **0.1647** / IS Ladder 全 PASS |
| 双闸实测 | **prod 0.6530** / **self 0.0000**（10-24 refresh 复测，与 10-23 台账一致，稳定） |
| 余量 | prod **0.047** / self **0.700** ⇒ **SAFE** |
| 档位 | 社区合格档需 prod<0.6 ⇒ 0.653 略超；平台底线档达标 |
| 动作 | **待用户点名后提交**（USA 本日 SUPER 配额未用） |

**同档换族对照（USA/TOP500，全部 ZERO-OS self=0）**：
| 族 | alpha | S | F | TO | prod | 判定 |
|---|---|---|---|---|---|---|
| **CROWDING** | `LL5rpRY2` | **1.74** | **1.25** | 0.1647 | 0.6530 | ✅ **PASS SAFE** |
| FAST | `O0JjRlxb` | 1.63 | 0.86 | 0.2430 | 0.6665 | ❌ F<1.0 + 8Y ladder 1.52 |
| SLOW | `58j1rAmN` | 1.35 | 0.60 | 0.2344 | 0.6317 | ❌ S/F 双 FAIL |
| MARKET（TOPSP500 档） | `VkdLm378` | 1.77 | 1.37 | 0.1522 | 0.6940 | ❌ 2Y 1.55 |

### 4.2 GLB — prod 余量过薄，仅留档

| 项 | 值 |
|---|---|
| 组件池 | 15 |
| 唯一空档 | **MINVOL10M（ZERO-OS）** |
| 配方 | CROWDING d1 l10 |
| 已建 alpha | `Vkd5pK6M` |
| IS 指标 | S **4.25** / F **2.66** / TO 0.2395（指标本身很好） |
| 双闸 | prod **0.6917** / self **0.0000** |
| 余量 | **prod 0.0083 ⇒ 低于 0.02 安全线，不交付** |
| 换族对照 | **CROWDING 0.6917（最优）** vs MARKET `E5VMzKY1` S4.06/F2.66 **prod 0.7620** vs SLOW（本轮仿真超时，下轮补测） |
| 建议 | 观察 prod 是否回落；或等 GLB 组件池继续增长后重扫（换族已证明只会推高 prod，优先级降） |

> 已占档：MINVOL1M×2、TOP3000、TOPDIV3000。GLB TOP3000 实测 self/prod **0.8638** 撞墙。

### 4.3 EUR — 全域 prod 墙，本轮无新增可交付

| 项 | 值 |
|---|---|
| 组件池 | 18（+4） |
| 已占 | TOP2500×2、TOPCS1600×1 |
| 三个 ZERO-OS 空档实测 | **TOP1200 prod 0.7337 / TOP800 prod 0.7117 / TOP400 prod 0.7783 — 全撞墙** |
| TOP800 附加问题 | S 仅 1.40（2Y 0.99），信号本身也崩 |
| TOP400 附加问题 | S 仅 1.23（2Y 0.67） |
| 结论 | **EUR 三个空档全部证伪**；只剩同档换配方。10-23 已占 TOP2500（`kqJOQgnk` S3.92/F3.40 prod 0.6546/self 0.5765，ACTIVE） |
| 建议 | **停投**。若坚持，只考虑 EUR TOP2500 换族（与已占 2 颗拉开 self 距离），但 self 起点 0.5765 余量仅 0.124 |

### 4.4 IND — 池最大但档位最饱和，判死

| 项 | 值 |
|---|---|
| 组件池 | **51（全表最大，+13）** |
| 档位 | **唯一 universe TOP500**，已占 **11 颗 SUPER** |
| 本轮实测 | CROWDING d1 l10 → `leMYEjgN` S **4.32** / F **4.35** / TO 0.2185，但 **self 0.7732 / prod 0.7733 双撞** |
| 倍率 | D1 = **1.14（全表最低）** |
| 结论 | **IND 已到顶**。池子增长只会让组件更拥挤、self 更高 |
| 建议 | **停投**。除非平台新增 IND universe |

### 4.5 KOR — 单 universe + 9 颗已占，判死

- 池 37（+9，全表第 3），唯一 universe TOP600，已占 **9 颗**。
- l14 实测 self/prod **0.9351**（10-23）；l10 0.673（余量仅 0.027）。
- **建议停投**。

### 4.6 GBR — self 卡在 0.63~0.70，余量过薄

- 池 20，唯一 universe TOP700，已占 2 颗。
- 实测：CROWDING l10 self 0.6259 / prod 0.7122（10-23）→ BLOCKED；
  SLOW l10 `1YjPdQJR` S3.95/F3.29 **self 0.6985 / prod 0.6983**，余量 **0.0015 / 0.0017** ⇒ **不交付**。
- 严格 selection 会导致组件 <10 ERROR。
- **建议：仅保留 SLOW d1 l10 作观察位，不主动交付**。

### 4.7 DEU — self 撞墙

- 池 11（刚过 10 下限），唯一 universe TOP500，已占 1 颗。
- CROWDING d1 l10 实测 self **0.7642** / prod 0.764 ⇒ BLOCKED。
- l10 已是平台硬下限，无法通过减小 limit 降 self。
- **建议停投**。

### 4.8 MEA — 🚫 **本轮新发现：区域已被平台停用**

- 池 21（+2），历史 2 颗 SUPER ACTIVE（2026-08-21 / 08-28，TOP400）。
- **本轮 4 档全部 400**：
  ```
  {"settings":{"region":["Region MEA is not available."],
    "universe":["Universe TOP200 is not available for instrument type EQUITY and region MEA."],
    "neutralization":["Neutralization CROWDING is not available for instrument type EQUITY, region MEA and universe TOP200."]}}
  ```
  MEA/TOP400 + CROWDING 同样返回 `Region MEA is not available.` + `Neutralization CROWDING is not available ... region MEA`。
- ⇒ **MEA 新建仿真已被平台关闭（历史 8 月提交仍保留）**。21 池作废。
- **建议：MEA 移入停投区**，后续仅周期性复检区域是否恢复。

### 4.9 ASI / HKG / CHN / JPN / TWN / AMR — 池不足或无组件

- ASI 9（差 1 颗到 10）、HKG 6 ⇒ 硬下限拦截，无法建 SA。
- CHN/JPN/TWN/AMR 池 = 0。
- **建议：全部停投**。

---

## 5. 停投区清单

| Region | 停投理由 | 复检条件 |
|---|---|---|
| **MEA** | **平台 400 `Region MEA is not available.`**（新建仿真被关闭） | 周期性重试 1 档 400 探针，恢复即重启 |
| **IND** | 单 universe + 11 颗已占，self/prod 双撞 0.773；D1 倍率 1.14 最低 | 平台新增 IND universe |
| **KOR** | 单 universe + 9 颗已占，l10 self 0.673 / l14 0.935 | — |
| **DEU** | 单 universe + self 0.7642；l10 已是硬下限无法再降 | 池 ≥20 后重扫 |
| **EUR** | 三个 ZERO-OS 空档 prod 全撞墙（0.7117–0.7783） | 池 ≥30 后重扫 |
| **GBR** | 单 universe，self 卡 0.63–0.70，余量 <0.002 | 池 ≥35 后重扫 |
| **ASI / HKG** | 组件池 <10 硬下限 | ASI 需 +1、HKG 需 +4 |
| **CHN / JPN / TWN / AMR** | 组件池 = 0 | — |

---

## 6. 撞墙档案（已验证不可用）

### 6.1 本轮新增（2026-10-24）

| 档位 | alpha | S | F | TO | self | prod | 死因 |
|---|---|---|---|---|---|---|---|
| MEA/TOP200 CROWDING d1 l10 | — | — | — | — | — | — | **400 区域不可用** |
| MEA/TOP200 CROWDING d1 l20 | — | — | — | — | — | — | 400 区域不可用 |
| MEA/TOP200 SECTOR d1 l10 | — | — | — | — | — | — | 400 区域+universe 不可用 |
| MEA/TOP400 CROWDING d1 l10 | — | — | — | — | — | — | 400 区域 + CROWDING 不支持 MEA |
| EUR/TOP800 CROWDING d1 l10 | `A1Q5LxVd` | 1.40 | 0.81 | 0.1726 | 0.0 | **0.7117** | S+F+2Y(0.99) 三 FAIL + prod 撞墙 |
| EUR/TOP400 CROWDING d1 l10 | `j2eJoEqO` | 1.23 | 0.67 | 0.1827 | 0.0 | **0.7783** | S+F+2Y(0.67) 三 FAIL + prod 撞墙 |
| USA/TOP200 CROWDING d1 l10 | `KPmvGKWp` | 0.94 | 0.54 | 0.1731 | 0.0 | 0.6167 | **IS 崩**（prod 健康但无意义） |
| IND/TOP500 CROWDING d1 l10 | `leMYEjgN` | 4.32 | 4.35 | 0.2185 | **0.7732** | **0.7733** | self/prod 双撞 |
| USA/TOP500 SLOW d1 l10 | `58j1rAmN` | 1.35 | 0.60 | 0.2344 | 0.0 | 0.6317 | S/F FAIL |
| USA/TOP500 FAST d1 l10 | `O0JjRlxb` | 1.63 | 0.86 | 0.2430 | 0.0 | 0.6665 | F 0.86<1.0 + 8Y ladder 1.52 |
| USA/TOPSP500 MARKET d1 l10 | `VkdLm378` | 1.77 | 1.37 | 0.1522 | 0.0 | 0.6940 | 2Y 1.55<1.58 |
| USA/TOPSP500 SUBINDUSTRY d1 l10 | `mLYN0dJx` | 1.73 | 1.11 | 0.1700 | 0.0 | **0.7479** | prod 撞墙 |
| USA/TOP200 CROWDING d1 **l30** | `qMEpGoY2` | 1.28 | 0.88 | 0.1738 | 0.0 | 0.6942 | 加大 limit 只把 S 0.94→1.28（仍 FAIL），**prod 0.6167→0.6942 恶化** ⇒ 复证「组件数↑ ⇒ prod↑」 |
| GLB/MINVOL10M MARKET d1 l10 | `E5VMzKY1` | 4.06 | 2.66 | 0.2392 | 0.0 | **0.7620** | 换族推高 prod（CROWDING 0.6917 已是最优） |

### 6.2 历史撞墙（沿用 10-23 档案）

| 档位 | 实测 | 死因 |
|---|---|---|
| USA/TOP3000 CROWDING d1 l10 | prod 0.7433 | prod 墙 |
| USA/TOPSP500 CROWDING d1 l10 | 2Y 1.50 | IS ladder |
| GLB/TOP3000 | self 0.8638 | self 墙 |
| KOR/TOP600 l14 | self 0.9351 | self 墙（组件数↑ 恶化） |
| DEU/TOP500 | self 0.7642 | self 墙 |
| EUR/TOP1200 | prod 0.7337 | prod 墙 |
| GBR/TOP700 + 严格 selection | — | 组件 <10 ERROR |

### 6.3 漂移失效（重要）

| alpha | 档位 | 10-23 台账 prod | 10-24 refresh 实测 | 结论 |
|---|---|---|---|---|
| `gJWdxLbM` | EUR/TOPCS1600 | 0.6988（判 PASS） | **0.7666** | **48h 内漂移 +0.068，判死** |
| `kqJOQgnk` | EUR/TOP2500 | 0.6546 | 0.6546 | 稳定（已提交 ACTIVE） |
| `LL5rpRY2` | USA/TOP500 | 0.6530 | 0.6530 | 稳定 |

> **铁律复证**：台账 prod >48h 不可信，交付前必须 `check_correlation(refresh=True)` 当场终验。

---

## 7. 执行清单

### 7.1 立即可执行（等用户点名）

```bash
# 前置：先停掉后台 sa_run.py 批次（并发会加剧代理不稳）
cd D:/coding/traeCN_project/wqb

# 提交（仅当用户明确点名 LL5rpRY2）
WQB_ALLOW_ALPHA_SUBMIT=1 \
  D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id LL5rpRY2 --region USA

# 复核：等满 flip 窗（~250s）后
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py status --alpha-id LL5rpRY2
# 确认 status=ACTIVE，不只看 POST 回执
```

### 7.2 下一轮扫描建议（按优先级）

| # | 目标 | 配方 | 目的 |
|---|---|---|---|
| 1 | USA/TOP500 | CROWDING d1 **l12 / l14** | l10 已 SAFE，测大 limit 能否提 S（⚠ 组件数↑ 会推高 prod，需实测） |
| 2 | USA/TOP500 | CROWDING **d0** l10 | 换 delay，D0 倍率 1.53 > D1 1.16 |
| 3 | GLB/MINVOL10M | SLOW d1 l10（补测，本轮仿真轮询超时） | 把 prod 0.6917 压进余量 ≥0.02（优先级已降：MARKET 换族反推高到 0.762） |
| 4 | USA/TOPSP500 | INDUSTRY / STATISTICAL d1 l10 | 找 2Y ≥1.58 的族（prod 0.6246 健康，只差 2Y） |
| 5 | USA/TOP1000 / TOP2000 | CROWDING d1 l10 | 已占档换配方，靠 self 距离取胜 |
| 6 | MEA | 单档 400 探针 | 复检区域是否恢复 |

### 7.3 构建命令模板

```bash
cd D:/coding/traeCN_project/wqb
nohup D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe -u \
  C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261024/configs_vN.json \
  --out results/sa_scan_20261024/res_vN.jsonl \
  > results/sa_scan_20261024/run_vN.log 2>&1 &
```

config 字段：`tag / region / universe / delay / neutralization / decay / combo_power / selection_limit / truncation`，可选 `selection`（默认 `(1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)`）。
续跑：已存在 `<out>.<tag>.json` 且含 alpha id 的项自动跳过。

### 7.4 配额与约束

| 约束 | 值 |
|---|---|
| SUPER 提交配额 | **1 / 天 / 区**（与 REGULAR 4/天/区 独立计数） |
| 建仿真 | 不消耗提交配额，但平台单并发、单档 ~6–8 分钟 |
| selectionLimit | **≥10 硬下限**；实测 l10 常最优 |
| prod 红线 | **≥0.7 无豁免**；交付要求余量 ≥0.02 |
| self 红线 | **≥0.7 无豁免** |
| prod 台账保鲜 | **48h**，交付前必 `refresh=True` 重测 |
| 组件池口径 | 只看 ACTIVE 已提交 REGULAR，IS 阶段 UNSUBMITTED 不计 |

### 7.5 建议执行顺序（下一天）

1. 提交 `LL5rpRY2`（USA）—— 唯一 SAFE 候选，占用 USA 当日 SUPER 配额。
2. 同日并行建（不占配额）：GLB/MINVOL10M 换族、USA/TOPSP500 换族、USA/TOP500 l12/l14/d0。
3. 全部建完后统一 `check_correlation(refresh=True)` 终验，余量 ≥0.02 才纳入交付池。

---

## 8. 本轮产物

| 文件 | 内容 |
|---|---|
| `results/sa_scan_20261024/pool_refresh.json` | 组件池 + 档位占用 + pyramid 全量快照 |
| `results/sa_scan_20261024/super_list.json` | 463 条 SUPER（37 ACTIVE）明细 |
| `results/sa_scan_20261024/slots_classified.json` | region×universe 档位分类（ZERO-OS / ZERO-SA / OCCUPIED） |
| `results/sa_scan_20261024/gates_refresh.json` | 7 颗既有候选 refresh=True 双闸实测 |
| `results/sa_scan_20261024/res_v7.jsonl` | 本轮 10 档构建结果 |
| `results/sa_scan_20261024/res_v8.jsonl` | 换族探针 6 档结果 |
| `results/sa_scan_20261024/refresh_pool.py` / `fetch_super.py` / `refresh_gates.py` | 可复用取数脚本 |

---

## 9. 铁律核对

- ✅ **只挖不提交**：本轮 16 档全部仅建仿真 + 双闸实测，**零提交动作**（`LL5rpRY2` 待用户点名）。
- ✅ **prod ≥0.7 红线**：`gJWdxLbM`（0.7666）、`mLYN0dJx`（0.7479）、`npAQgjYM`（0.7337）等全部判 BLOCKED，无豁免。
- ✅ 组件池口径 = OS REGULAR ACTIVE（IS UNSUBMITTED 不计）。
- ✅ 台账 prod 全部 `refresh=True` 重测，捕获 1 例漂移失效。
- ✅ 余量 <0.02 一律不交付（`Vkd5pK6M` 0.0083、`1YjPdQJR` 0.0017）。
