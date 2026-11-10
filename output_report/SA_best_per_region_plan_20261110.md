# 各 Region 最优 SuperAlpha 方案 · 2026-11-10

> 扫描时点：2026-11-10 06:30–07:10（GMT+8）｜组件池缓存 `generated_at=2026-11-10T06:30:42+08:00`
> 数据源：`results/sa_plan_20261110.json`（probe --refresh）、`results/sa_scan_20261110/`
> **本文件全部为待执行配方，本轮未提交任何 alpha。提交权归用户。**

---

## 一、执行摘要

### 1.1 一句话结论

**ASI 组件池首次达标（10 颗），成为全账户唯一「ZERO_SA + 池够」的新档 ⇒ 本轮唯一新增产能 = 首颗 ASI SuperAlpha。**
其余 8 个 GO 区全部处于「同档换配方 = 同席」状态，无法新增独立席位。

### 1.2 优先队列表（按价值排序）

| # | 槽位 | 配方 | Alpha ID | S | F | TO | prod | self | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| ⭐1 | ASI/MINVOL1M | STATISTICAL d2 l10 cp1 | `d5WGG5bg` | **5.38** | 2.99 | **0.2923** | **0.5100** | **0.5100** | **0.190** | 全闸 PASS·B 档双达标 |
| 2 | ASI/MINVOL1M | STATISTICAL d1 l10 cp1 | `gJe2lMKO` | 5.57 | 2.89 | 0.3483 | 0.5091 | 0.5090 | 0.191 | 全闸 PASS·TO 超 B 档 |
| 3 | ASI/MINVOL1M | COUNTRY d3 l10 cp1 | `A1VAAbWe` | 4.60 | **3.33** | 0.2458 | 0.6315 | 0.6315 | 0.068 | 全闸 PASS·F 最高 |
| 4 | ASI/MINVOL1M | CROWDING d3 l10 cp1 | `N1NZZo7g` | 4.58 | 3.28 | 0.2461 | 0.6574 | 0.6574 | 0.043 | 全闸 PASS·余量薄 |
| 5 | ASI/MINVOL1M | SECTOR d3 l10 cp1 | `npvEEWO8` | 4.30 | 3.12 | 0.2455 | 0.6593 | 未测 | 0.041 | 全闸 PASS·备胎 |

**第 1–5 名同属 ASI/MINVOL1M 一档 ⇒ 互斥，只能交一颗。** 交一颗即 ASI 封档（当日 ASI 的 SUPER 配额用完）。

推荐交付：**`d5WGG5bg`** —— 唯一同时满足「TO<0.30 且 prod<0.60」双 B 档阈值，且 S 最高（5.38），prod/self 余量 0.19（抗生产池漂移）。

### 1.3 本轮关键新发现（3 条，均改写判据）

1. **★★★ 「新区域 ⇒ prod 免费」是错的**。ASI 零 SUPER，但首颗 SA 的 prod **不是 0**，而是**与自有 REGULAR 成分的最大相关**：四族实测 prod 与 self 逐位相同（0.5091/0.5090、0.5100/0.5100、0.6315/0.6315、0.6574/0.6574），top1 全部是自有 REGULAR `88jaV5lv`。⇒ **SA 的 prod 下界由区域里最强的同族 REGULAR 成分决定**，与有没有已提交 SUPER 无关。
2. **★ ASI 的 F 天花板 ≈ 3.36，达不到 4.5**。decay 1→2→3→4→5 的 F 走 2.89→2.99→3.03→3.18(FAIL)→3.36(FAIL)，**decay≥4 必触发 `LOW_ROBUST_UNIVERSE_RETURNS`**。F 峰值被稳健性闸截断在 decay=3。根因是成分本身 R 只有 9–14%、S 最高 3.06。
3. **★ ASI/TOP500 与 ASI/MINVOL10M 均劣于 MINVOL1M**：MINVOL10M COUNTRY d3 = S3.61/F2.55（MINVOL1M 同配方 4.60/3.33）⇒ 再次验证 **SA universe 必须与多数成分所在 universe 对齐**（7/10 成分在 MINVOL1M）。

---

## 二、数据基线

### 2.1 组件池 eligibility（硬前置：同区 ≥10 颗 ACTIVE 已提交 REGULAR）

| Region | ACTIVE 组件 | IS 未提交存量 | 相对 11-02 | verdict | 可建 universe |
|---|---:|---:|---|---|---|
| USA | 47 | 0 | +1 | GO | TOP3000/2000/1000/500/TOPSP500/TOP200 |
| IND | 47 | 0 | +2 | GO | TOP500（唯一） |
| KOR | 34 | 32 | +4 | GO | TOP600（唯一） |
| GBR | 28 | 113 | +7 | GO | TOP700（唯一） |
| **ASI** | **10** | 0 | **+1 ⇒ 首次跨过 10** | **GO（新）** | MINVOL1M / MINVOL10M / TOP500 |
| EUR | 23 | 73 | +4 | GO | TOP2500/CS1600/1200/800/400 |
| MEA | 19 | 0 | 0 | **平台已下架** | — （`get_platform_setting_options` 无 MEA） |
| GLB | 18 | 0 | +1 | GO | MINVOL1M / MINVOL10M / TOP3000 / TOPDIV3000 |
| DEU | 17 | 732 | +6 | GO | TOP500（唯一） |
| HKG | 7 | 0 | +1 | **BLOCKED（差 3）** | TOP800 / TOP500 |

合计 250 颗 ACTIVE REGULAR（11-02 为 239）。**唯一质变是 ASI 9→10。**

### 2.2 档位占用分类（region × universe）

| 类型 | 槽位 | REGULAR | SUPER | 含义 |
|---|---|---:|---:|---|
| **ZERO_SA（可建）** | **ASI/MINVOL1M** | 7 | 0 | ✅ 本轮唯一新档 |
| ZERO_SA（池不足） | ASI/MINVOL10M | 3 | 0 | 需与 MINVOL1M 合并算区级池 |
| ZERO_SA（池不足） | HKG/TOP800 | 7 | 0 | 差 3 颗 |
| ZERO_OS（无组件） | ASI/TOP500, USA/TOP200, EUR/TOP1200/800/400, CHN/TOP2000U, AMR/TOP600, HKG/TOP500 | 0 | 0 | 无组件可建（EUR 三档为结构性 prod 墙） |
| OCCUPIED | USA/TOP3000 | 38 | 6 | 满 |
| OCCUPIED | USA/TOP2000 | 5 | 1 | 满 |
| OCCUPIED | USA/TOP1000 / TOP500 / TOPSP500 | 0/0/0 | 1/1/1 | 满 |
| OCCUPIED | IND/TOP500 | 47 | **12** | 满（最拥挤） |
| OCCUPIED | KOR/TOP600 | 34 | **11** | 满 |
| OCCUPIED | GBR/TOP700 | 28 | 6 | 满 |
| OCCUPIED | EUR/TOP2500 | 13 | 2 | 满 |
| OCCUPIED | EUR/TOPCS1600 | 10 | 1 | 满 |
| OCCUPIED | GLB/MINVOL1M | 17 | 2 | 满 |
| OCCUPIED | GLB/MINVOL10M / TOP3000 / TOPDIV3000 | 0/0/1 | 1/1/1 | 满 |
| OCCUPIED | DEU/TOP500 | 17 | 2 | 满 |
| NON_PLATFORM | MEA/TOP400 | 19 | 2 | 区域下架，不能新建 |
| NON_PLATFORM | USA/ILLIQUID_MINVOL1M | 4 | 0 | 不在 platform options |

**已 ACTIVE SUPER = 51 颗**（11-09 为 50）：DEU 2 / EUR 3 / GBR 6 / GLB 5 / IND 12 / KOR 11 / MEA 2 / USA 10 / **ASI 0**。

### 2.3 Pyramid D1 倍率（当季）

| Region | D1 均值 | 峰值类别 | 当季已点亮类别（≥3 颗） |
|---|---:|---|---|
| **DEU** | **1.613** | model 1.8 | analyst 6 / model 3 / other 2 / shortinterest 2 |
| CHN | 1.608 | other 1.9 | 全 0（池 0，需先攒 REGULAR） |
| AMR | 1.550 | sentiment 1.7 | 全 0 |
| **GBR** | 1.413 | sentiment 1.7 | model 6 / pv 4 / shortinterest 4 / news 3 / analyst 3 / fundamental 3 / other 2 |
| **HKG** | 1.413 | analyst 1.7 | 仅 pv 1（差 2） |
| KOR | 1.387 | analyst 1.6 | shortinterest 4 / analyst 3 / fundamental 3 / model 3 / pv 2 / risk 2 |
| EUR | 1.207 | other 1.5 | analyst 10 / model 3 / imbalance 3 / fundamental 3 / pv 2 / insiders 2 / risk 2 / sentiment 2 / other 2 |
| **ASI** | 1.181 | analyst 1.5 | **other 3（已亮）** |
| GLB | 1.177 | fundamental 1.4 | other 4 / model 3 / pv 2 |
| USA | 1.175 | other 1.4 | analyst 6 / model 4 / other 2 / risk 2 / institutions 1 / earnings 1 |
| IND | 1.140 | analyst 1.4 | pv 11 / news 4 / other 4 / analyst 3 / model 3 / fundamental 3 / risk 3 |
| MEA | — | — | 下架 |

⚠ **ASI `other` 已点亮（3/3）** ⇒ 新提交的 ASI SA 若被平台归入 `other`，**不产生新的塔**；塔倍率（1.181）不作为本轮选点理由。

---

## 三、选点原则

**优先级：档位占用类型 > 组件池大小 > 配方。**

1. **零 OS 档 > 零 SA 档 > 已占档换配方。** 本轮零 OS 档全部无组件（EUR 三档另有结构性墙），零 SA 档只有 ASI 达标 ⇒ 结论唯一。
2. **「已占档换配方」= 同席，不是新增。** 依据：SA prod ≡ self ≡ 与自有池最大相关（本轮四族逐位验证），换中性化族/limit/combo/decay 只改数值不改身份。DEU l10 五族谱 0.60→0.77、ASI l10 六族谱 0.51→0.66 都是同一席位移。
3. **指标 = 约束优化**：`max S` s.t. `self<0.7 ∧ prod<0.7`（合规线），优选 `prod<0.60 ∧ TO<0.30`（B 档）。三档目标 `S>4.5 ∧ F>4.5 ∧ prod<0.65` 先过线再比。
4. **中性化族规律（本轮 ASI 六族实测，S 降序 / F 降序）**：
   - S：STATISTICAL 5.38–5.57 > SLOW 5.30 > FAST 5.22 > COUNTRY 4.92 > CROWDING 4.89 > SUBINDUSTRY 4.70 > SECTOR 4.61
   - F：COUNTRY 3.19 > CROWDING 3.15 > SECTOR 3.01 > STATISTICAL 2.89 ≈ SLOW 2.78 > SUBINDUSTRY 2.82
   - prod：STATISTICAL **0.51** < COUNTRY 0.63 < CROWDING 0.66 ≈ SECTOR 0.66
   - ⇒ **STATISTICAL 是 ASI 的 prod 最优族**（与 GLB 的 SLOW 特例同构：族越「粗」prod 越脏这条在 ASI 反向，STAT 最干净）。
   - ⇒ 通用选族规则仍是：`TO<0.10 → SLOW；TO>0.20 → FAST`；区域基线 GLB/USA/DEU/EUR 走 STATISTICAL，KOR/IND/GBR 走 SECTOR/SUBINDUSTRY（REGULAR 通道经验）。
5. **decay 是 F 的唯一杠杆但有机上限**：decay≥2 才生效；ASI 在 **decay=3 触顶**（F 3.33），decay≥4 必掉 `LOW_ROBUST_UNIVERSE_RETURNS`。GBR 历史同型：dec1→dec5 F 3.88→4.27，但 prod 也同步上行。
6. **limit 轴在 ASI 上无自由度**：`实际生效数 = min(limit, 组件池) = min(10,10) = 10` ⇒ l10/l12/l30 三档会得到完全相同的组合，本轮不扫。

---

## 四、论坛指标标准（引用本轮固化，2026-10-22 定稿）

来源：《【新人入门】Super Alpha 从入门到入门！》78 赞/39 评、《2024 super alpha 比赛心得》22 赞/15 评、《Super Alpha 参数设置》12 赞（含 LY43440 实测回复）。

### 4.1 组成数量
- 平台硬下限 **10**（<10 直接 400 `Ensure this value is greater than or equal to 10`）。
- 78 赞帖建议 **30–100 起测、≤500**；实测 IND 取 300（long/short 各 ~250）。
- **实际生效数 = min(limit, 组件池)**；池是 **(region, delay) 双键**（USA/TOP500 d0 直接 400，因 d0 池为 0）。

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr | 本轮对应 |
|---|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 | 19/19 档全过 |
| B 社区合格档 | — | — | **<0.30** | **<0.60** | **`d5WGG5bg` 唯一命中** |
| C 比赛/优秀档 | 5.6–7.0 | 5.6–8.9 | 0.20–0.27 | <0.5 | 未达（ASI S 5.38 差 0.22、F 远未及） |

### 4.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`（官方建议 1–4）。

⚠ **两条不可用**：
- **`author_*` 在自有池恒为常数** ⇒ 论坛 author 阈值无法消费。
- **筛选强度必须匹配池规模**：ASI 池恰好 10，任何硬过滤（如 `turnover<0.3` 会剔掉 TO=0.5586 的 `E5R56EbR`）都会掉到 9 颗 ⇒ 直接 400。小池区只能用宽松 selection。

### 4.4 其他
- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）。
- `Selection Handling = Non-Zero` 为论坛推荐；本账户历史 51 颗 SA 全用 POSITIVE 均成功，本轮沿用 POSITIVE。
- **prod corr 是档位属性 + 成分属性，不是配方属性**：换族只能在同一席位内 ±0.15 浮动；真正的下界是成分相关性。

---

## 五、分 Region 方案

### 5.1 ⭐ ASI（唯一新增产能）

**基线**：组件池 10 颗（7 MINVOL1M + 3 MINVOL10M），全 delay=1；零 SUPER；pyramid D1 1.181（`other` 已亮）。
成分画像：S 1.72–3.06、TO 0.0965–0.5586、7 颗 SECTOR 中性化、最强成分 `P0obGoQJ`(S3.06/SLOW) 与 `88jaV5lv`(S2.35/SECTOR)。

**构建命令**（唯一推荐配方）：

```bash
cd D:/coding/traeCN_project/wqb
world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py select \
  --region ASI --universe MINVOL1M --delay 1 \
  --neutralization STATISTICAL --decay 2 \
  --selection-limit 10 --self-gate 0.7 --turnover-max 0.6 --prod-ceiling 1.0 \
  --json results/sa_scan_20261110/res_asi_mv1m_stat_d2.json
```

> 参数说明：`--turnover-max 0.6`（池内最高 TO 0.5586，用默认 0.5 会剔掉 1 颗 ⇒ 组件不足 10）；`--prod-ceiling 1.0`（池内存在 prod≥0.7 成分时避免被 POSITIVE 剔除）。

**六族 × decay 全谱实测（19 档）**

| 配方 | ID | S | F | TO | R | 最大回撤 | margin | prod | self | IS 检查 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **STAT d2** | **`d5WGG5bg`** | **5.38** | 2.99 | **0.2923** | 9.01% | 0.86% | 6.2bp | **0.5100** | **0.5100** | 全 PASS |
| STAT d1 | `gJe2lMKO` | 5.57 | 2.89 | 0.3483 | 9.39% | 0.93% | 5.4bp | 0.5091 | 0.5090 | 全 PASS |
| STAT d1 cp3 | `2rAYY11w` | 5.58 | 2.89 | 0.3508 | 9.40% | 0.93% | — | 未测 | — | cp 在 l10 池=limit 时几乎 no-op |
| STAT d3 | `P0oVVaXq` | 5.22 | 3.03 | 0.2584 | 8.72% | — | — | — | — | ❌ ROBUST_UNIVERSE_RETURNS |
| STAT d5 | `Jje9Akgx` | 4.98 | 3.09 | 0.2145 | 8.28% | — | — | — | — | ❌ ROBUST_SHARPE + ROBUST_RETURNS |
| SLOW d1 | `E56djvqr` | 5.30 | 2.78 | 0.3423 | 9.39% | — | — | 未测 | — | 全 PASS |
| FAST d1 | `Jje9Ao3x` | 5.22 | 2.94 | 0.3438 | 10.88% | — | — | 未测 | — | ❌ ROBUST_SHARPE |
| **COUNTRY d3** | **`A1VAAbWe`** | 4.60 | **3.33** | 0.2458 | 12.86% | 3.03% | 10.5bp | 0.6315 | 0.6315 | 全 PASS |
| COUNTRY d1 | `A1VApzGE` | 4.92 | 3.19 | 0.3272 | 13.74% | 2.71% | 8.4bp | 未测 | — | 全 PASS |
| COUNTRY d1 cp3 | `P0oVVeX7` | 4.91 | 3.17 | 0.3295 | 13.75% | — | — | 未测 | — | cp3 无增益 |
| COUNTRY d4 | `zq3VVORo` | 4.47 | 3.36 | 0.2222 | 12.54% | — | — | — | — | ❌ ROBUST_SHARPE + ROBUST_RETURNS |
| **CROWD d3** | **`N1NZZo7g`** | 4.58 | 3.28 | 0.2461 | 12.64% | 3.16% | 10.3bp | 0.6574 | 0.6574 | 全 PASS |
| CROWD d1 | `58EXmwv1` | 4.89 | 3.15 | 0.3268 | 13.54% | 2.93% | 8.3bp | 未测 | — | 全 PASS |
| CROWD d1 cp3 | `2rAYYMgZ` | 4.87 | 3.12 | 0.3291 | 13.55% | — | — | 未测 | — | cp3 无增益 |
| CROWD d5 | `vR1QQv8a` | 4.34 | 3.34 | 0.2038 | 12.10% | — | — | — | — | ❌ ROBUST_UNIVERSE_RETURNS |
| **SECTOR d3** | **`npvEEWO8`** | 4.30 | 3.12 | 0.2455 | 12.96% | 4.21% | 10.6bp | 0.6593 | 未测 | 全 PASS |
| SECTOR d2 | `6Xdkk19Y` | 4.44 | 3.08 | 0.2770 | 13.37% | 4.13% | 9.7bp | 未测 | — | 全 PASS |
| SECTOR d1 | `bl6wmR8q` | 4.61 | 3.01 | 0.3262 | 13.90% | — | — | 未测 | — | 全 PASS |
| SUBIND d1 | `N1NZdPmX` | 4.70 | 2.82 | 0.3403 | 12.26% | — | — | 未测 | — | 全 PASS |
| MINVOL10M COUNTRY d3 | `QPv88bJW` | 3.61 | 2.55 | 0.2607 | 12.97% | — | — | — | — | 全 PASS 但指标全面劣化 |

**结论**：
- 唯一双 B 档 = `d5WGG5bg`（S5.38 / F2.99 / TO0.2923 / prod0.5100）。
- 追 F 选 `A1VAAbWe`（F3.33，margin 10.5bp）但 S 低 0.78 且 prod 余量只剩 0.068。
- **F>4.5 在 ASI 不可达**（成分 S 上限 3.06、R 上限 14%），报告层面明确记为结构性缺口，不列入可达目标。

### 5.2 HKG（差 3 颗，最高 ROI 的池投资）

- 池 7/10，`ZERO_SA`（TOP800 有 7 颗 REGULAR、0 颗 SUPER），pyramid D1 1.413（第 3 高），仅有 `pv=1`。
- **补 3 颗 ACTIVE REGULAR 即可开档，且是零 SUPER 全新席位。**
- 建议方向：`pv`（已有 1 颗，再补 2 可点亮）与 `analyst/model`（D1 1.7 峰值）。

### 5.3 已占档区域（本轮不新增，仅维护）

| Region | 席位 | 现状 | 结论 |
|---|---|---|---|
| USA | 6 档 10 颗 | TOP3000 6 颗，最强 `A1V0eZne` S6.39/F7.06/TO0.1178 | 满；TOP200/TOP500/TOPSP500/TOP1000 各 1 颗后封档 |
| IND | TOP500 12 颗 | `wpbQjeKp` F5.27 / `QPbjxMYw` F5.74 / `pw52P3jb` S5.43 | 最拥挤，prod 天花板 0.77 |
| KOR | TOP600 11 颗 | `RRA9EZKz` F5.94 / `9qWJv1do` F5.54 / `88RNX7la` F5.28 | 满 |
| GBR | TOP700 6 颗 | `3qompGeZ` S4.42/F4.27/TO0.1366（dec5 生效） | 满；l10→l11 就穿 0.65 |
| GLB | 4 档 5 颗 | `LL5amzov` S6.93/F4.18 为全账户 S 王 | 满 |
| EUR | 2 档 3 颗 | `GrgGkV1o` S4.21 / `kqJOQgnk` F3.40 | 满；三零 OS 档结构性 prod 墙 |
| DEU | TOP500 2 颗 | `vR1oxZA3` S3.27/F3.09/TO0.1828 | 满；l10 五族谱 0.60→0.77 |
| MEA | — | 2 颗历史 SA 仍 ACTIVE，但区域已下架 | 不可新建 |

---

## 六、停投区

| 区域/档位 | 停投理由 | 最后确认 |
|---|---|---|
| **MEA 全区** | `get_platform_setting_options` 无 MEA（18 个组合里没有）；新建仿真 400 `Region MEA is not available` | 2026-11-10 复核 |
| **EUR TOP1200 / TOP800 / TOP400** | 零 OS 但零组件；历史实测 prod 0.7117 / 0.7337 / 0.7783 全撞（结构性） | 2026-11-08 |
| **EUR TOP2500 / TOPCS1600** | 已占 2+1 颗；`gJWdxLbM` 曾 0.6988→0.7666 漂移 | 2026-10-24 |
| **IND / KOR / DEU / GBR** | 唯一 universe 且已占 12/11/2/6 颗；同档换族=同席 | 2026-11-09 |
| **USA TOP3000 / TOP2000 / TOP1000 / TOP500 / TOPSP500 / TOP200** | 全部已占；TOP200 无组件且历史判死（S1.07） | 2026-11-02 |
| **GLB 全域** | 4 档全占 | 2026-11-09 |
| **CHN / AMR / JPN / TWN** | 池 0 或区域不可用 | 2026-11-02 |
| **HKG** | 池 7<10，**唯一「补数据即可解锁」的停投区** | 2026-11-10 |
| **ASI/MINVOL10M、ASI/TOP500** | 同区 MINVOL1M 更优（MINVOL10M 实测 S3.61 vs 4.60），TOP500 无组件 | 2026-11-10 |

---

## 七、撞墙档案（已验证不可用）

| 候选/配方 | 撞的墙 |
|---|---|
| `zq3VVORo` ASI COUNTRY d4 | `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` + `LOW_ROBUST_UNIVERSE_RETURNS`（decay≥4 通病） |
| `vR1QQv8a` ASI CROWDING d5 | `LOW_ROBUST_UNIVERSE_RETURNS` |
| `P0oVVaXq` ASI STAT d3 | `LOW_ROBUST_UNIVERSE_RETURNS` |
| `Jje9Akgx` ASI STAT d5 | ROBUST_SHARPE + ROBUST_RETURNS 双 FAIL |
| `Jje9Ao3x` ASI FAST d1 | `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` |
| `QPv88bJW` ASI/MINVOL10M COUNTRY d3 | universe 与成分错配：S3.61/F2.55（MINVOL1M 同配方 4.60/3.33） |
| `2rAYY11w` / `2rAYYMgZ` / `P0oVVeX7` cp3（l10=池上限） | cp3 在池=limit 时近似 no-op（S ±0.02），不构成杠杆 |
| ASI SECTOR d1 + CROWDING d3 余量 | prod 0.6593 / 0.6574，余量 0.041–0.043 < 0.05，不推荐交付 |
| `58EKWYGz` / `JjeaK2mA` DEU SECTOR / MARKET | prod 0.7701 / 0.7708（= 自有 `vR1oxZA3` 相关） |
| `0mYak1nv` / `bl6K2Oor` DEU CROWDING / SLOW | 0.6918 / 0.6953，余量 <0.01 |
| `LLM2qe2M` / `E56208rR` USA TOP2000 SECTOR | 0.6957 / 0.7032 FAIL |
| EUR 全部零 OS 档 | prod 0.71–0.78 |
| HKG 建 SA | `At least 10 component alphas are required`（池 7） |
| `combo_power ≥6` | IS Ladder 2Y 掉到 1.58 == limit ⇒ FAIL |
| `zscore(w)` combo | 权重中心化致非负权重反向下单（S −1.14） |
| `rank(w)` / `sqrt(w)` / `ts_mean(w,20)` | 与已占同席互测 0.74–0.99，非新增 |

---

## 八、执行清单

### 8.1 构建（如需重建 `d5WGG5bg`）

见 §5.1 命令块。参数不可省 `--turnover-max 0.6 --prod-ceiling 1.0`。

### 8.2 提交（**仅在用户明确点名时执行**）

```bash
cd D:/coding/traeCN_project/wqb
# 1) 先停后台 sa_run/select 批次（并发会加剧代理不稳）
# 2) 提交（内置 prod 闸 0.7，fail-closed，无豁免参数）
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id d5WGG5bg --region ASI
# 3) 等满 flip 窗（~250s）后复核 ACTIVE（不只看 POST 回执）
world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py status --alpha-id d5WGG5bg
```

### 8.3 配额与顺序约束

- **SUPER 配额 = 1 / 天 / 区**，与 REGULAR 4/天/区独立。ASI 今日尚未使用 ⇒ 今天可交 1 颗。
- **交一颗即 ASI/MINVOL1M 封档**，其余 4 颗同档候选同时作废。
- **prod 台账 48h 作废** ⇒ 提交前必须 `check_correlation(refresh=True)` 复测（本轮实测值 07:00 前后，48h 内有效）。
- prod 是账号级单并发：遇 `correlation_busy` 按 `retry_after` 隔时重查，**不要重新触发**（`inflight=true` 时尤其不要）。

### 8.4 建议执行顺序

1. **今天**：`d5WGG5bg`（ASI 首颗，prod 余量 0.19）。
2. **本周**：补 3 颗 HKG REGULAR（优先 `pv` 1→3、`analyst`/`model`），池过 10 后开 HKG/TOP800 首颗 SA（零 SUPER，D1 1.413）。
3. **持续**：不再对已占档做配方迭代（四轴全封）；产能只来自新 region 或新 universe。

---

## 九、SA 算子清单与利用率审计（本轮要求项）

### 9.1 平台官方清单（`get_documentation_page("appendix-operators")`，2026-11-10 实抓）

官方《SuperAlpha Operators》表共 **160 个 Combo 可用算子** + **43 个 Selection 可用算子**（`universe_size` 为 Selection 独有；`combo_weight`/`generate_stats`/`self_corr`/全部 `ts_*`/`group_*`/`reduce_*` 等为 Combo 独有）。

- **Selection 独有**：`universe_size`
- **Combo 独有（选区）**：`bucket` `combo_weight` `convert` `count` `days_from_last_change` `densify` `filter` `generate_stats` `group_backfill` `group_count` `group_extra` `group_max/mean/median/min` `group_neutralize` `group_normalize` `group_percentage` `group_rank` `group_scale` `group_std_dev` `group_sum` `group_vector_neut/proj` `group_zscore` `hump` `hump_decay` `inst_pnl` `inst_tvr` `jump_decay` `keep` `kth_element` `last_diff_value` `left_tail` `log_diff` `normalize` `one_side` `pasteurize` `position_safeguard` `quantile` `rank` `rank_by_side` `rank_gmean_amean_diff` `reduce_*`(14) `regression_neut/proj` `replace` `right_tail` `round_down` `scale` `scale_down` `self_corr` `tail` `trade_when` `truncate` `ts_*`(~60) `unit` `vector_neut/proj` `winsorize` `zscore`
- **双列通用（43 个）**：`abs` `add` `and` `arc_cos/sin/tan` `ceiling` `clamp` `divide` `equal` `exp` `floor` `frac` `greater` `if_else` `inverse` `is_finite/nan/not_finite/not_nan` `less` `log` `max` `min` `multiply` `nan_mask` `nan_out` `negate` `not` `or` `power` `purify` `reverse` `round` `s_log_1p` `sigmoid` `sign` `signed_power` `sqrt` `subtract` `tanh` `to_nan`
- 官方补充语义：`self_corr(input, K)` 输出 (D×N×N) 矩阵；`reduce_*` 作用在最后一维，`reduce_count/reduce_avg/reduce_percentage/reduce_stddev` 带 threshold。

### 9.2 本工作区实际利用率（扫 44 个 SA 定义 / 73 个产物文件）

| 通道 | 官方算子数 | 已用 | 利用率 | 已用算子 |
|---|---:|---:|---:|---|
| **Combo** | 160 | **5** | **3.1%** | `generate_stats`(44) `self_corr`(44) `reduce_max`(44) `if_else`(44) `ts_ir`(1) |
| **Selection** | 43 | **0** | **0%（仅算术 `*`/`<`/`>` + 字段）** | — |

标准 combo 模板实际只用了 4 个函数：
```
stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500);
ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); w = 1 - maxCorr; w
```
selection 模板只用字段（`prod_correlation` / `self_correlation` / `turnover`）与算术运算，**没有调用任何 Selection 专属算子**。

### 9.3 本轮组建的算子使用情况

**本轮 19 档全部沿用同一 combo 骨架，新增使用算子 = 0。** 变化的只有 settings 侧参数（neutralization / decay），不属于算子轴。
原因是 `selectionLimit=10 == 组件池 10`，组合权重完全由 `w=1-maxCorr` 决定，任何 `rank/scale/winsorize/quantile` 整形都只能改动极小数值（cp3 实测 S ±0.02 即证）。

### 9.4 结论与建议（诚实版）

- **算子轴不是当前瓶颈**：SA 的 S/F/prod 由「席位 + 成分」两项决定，算子只影响最后的权重整形。11-07/11-08/11-09 三轮已分别证伪 `zscore(w)`、`rank(w)`、`sqrt(w)`、`ts_mean(w,20)`、`cp≥6`、`reduce_*`、`tail/winsorize` —— 全部「不提升或破闸」。
- **仍未被测的高价值项**：`combo_weight`（官方唯一用于读取成分权重的算子，语义未摸底）、`universe_size(universe)` 作为 selection 偏好项（唯一 Selection 专属算子）。
- **优先级**：`combo_weight` 摸底（低风险、可能改变权重口径）> `universe_size` 偏好（仅影响选谁，不影响指标）> 其余 150 个算子（ROI 已证极低）。

---

## 附录 A · 本轮产出文件

| 文件 | 内容 |
|---|---|
| `results/sa_plan_20261110.json` | 组件池 + 51 颗 SUPER 全量快照（缓存 06:30:42） |
| `results/sa_scan_20261110/slots_local.json` | 档位分类（含 NON_PLATFORM 识别） |
| `results/sa_scan_20261110/res_asi_*.json` | 19 档 SA 构建产物（含 checks 全明细） |
| `results/sa_scan_20261110/op_audit.json` | 算子利用率审计 |
| `results/sa_scan_20261110/pyramid_d1mean.json` | 各区域 D1 均值 |
| `logs/sa_asi_lane{A,B}_20261110.log`、`logs/sa_asi_r{2,3}_lane{A,B}_20261110.log` | 构建日志（双通道串行） |

## 附录 B · 双闸实测记录（`refresh=True`）

| ID | prod | self | 时间 | 来源 |
|---|---:|---:|---|---|
| `gJe2lMKO` | 0.5091 | 0.5090 | 06:5x | check_correlation(refresh=True) |
| `d5WGG5bg` | 0.5100 | 0.5100 | 06:5x | check_correlation(refresh=True) |
| `A1VAAbWe` | 0.6315 | 0.6315 | 07:0x | check_correlation(refresh=True) |
| `N1NZZo7g` | 0.6574 | 0.6574 | 07:0x | check_correlation(refresh=True) |
| `npvEEWO8` | 0.6593 | 未测 | 07:1x | check_correlation(production, refresh=True) |

> 三项独立验证 prod ≡ self ⇒ top1 相关对象为自有 REGULAR 成分（`88jaV5lv` 0.51–0.66），非第三方、非自有 SUPER。

---

## 执行记录（2026-11-10 08:17）

| 项 | 值 |
|---|---|
| 提交 alpha | `d5WGG5bg`（ASI/MINVOL1M STATISTICAL d2 l10） |
| 结果 | **ACTIVE**，stage=OS，name `ASI_S_10comp_WGG5bg` |
| prod / self 快照 | 0.5100 / 0.5100（与提交前 probe max 0.51 逐位一致，Δ=0） |
| checks | 13 项全 PASS；仅 `MATCHES_COMPETITION` WARNING（信息项） |
| 贴线项 | `LOW_ROBUST_UNIVERSE_RETURNS` 0.0811 vs limit 0.0811（零余量）；`ROBUST_SHARPE` 4.91 vs 4.84 |
| 影响 | ASI 零 SUPER 档已被占用 ⇒ 同档其余 11 颗候选（gJe2lMKO / A1VAAbWe / N1NZZo7g / npvEEWO8 等）作废 |

---

## 追加（2026-11-10 08:45）· 边际收益排序与提交规则变更

### A. 规则变更（已写入定时任务 `bd08ec45`，此后每轮强制执行）

| 项 | 旧 | 新 |
|---|---|---|
| 提交 | 只挖不提交，提交权归用户点名 | **每轮自动提交边际收益排序第一**（用户 11-10 授权）；其余仍只挖不提交 |
| 同档判定 | 同档换族 = 同席，边际≈0 | **同族=死、异族可共存**；档内 SUPER ≥5 颗后异族也失效 |
| 排序主键 | S / F | 席位/族边际 > B 档双达标 > prod 余量 > U > Eff |

硬闸（全部满足才自动提交）：`prod<0.68`、`self<0.68`、checks 零 FAIL、该区当日 SUPER 配额未用、台账无 REJECT。

### B. 边际收益五量（自建，平台无对应字段）

| 指标 | 公式 | 用途 |
|---|---|---|
| `U` | `S/(μ̄·√N)` | 分散度捕获率 |
| `N_eff` | `(S/μ̄)²` | 等效独立腿数 |
| `ρ_eff` | `(N·μ̄²/S²−1)/(N−1)` | 隐含组件平均相关 |
| `Eff` | `(S−μ̄)/max(prod,self)` | **唯一有跨候选区分力** |
| `ΔCAP%` | `√(52/(1+51ρ))/√(51/(1+50ρ))−1` | 已退化（+0.01% 量级），不作主键 |

⚠ 区内 `μ̄`、`N` 恒定 ⇒ `U/N_eff/ρ_eff` 严格单调于 S，**区内无独立信息**，只在跨区可比。

### C. 本轮实测（`refresh=True`，均在 `d5WGG5bg` 提交后测得）

| ID | 档位 | 族 | S | F | TO | prod | self | 余量 | 判定 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `d5WGG5bg` | ASI/MINVOL1M | STAT d2 | 5.38 | 2.99 | 0.2923 | **0.5100** | **0.5100** | 0.190 | ✅ 排序第一，已 ACTIVE |
| `gJe2lMKO` | ASI/MINVOL1M | STAT d1 | 5.57 | 2.89 | 0.3483 | **0.9906** | — | — | ❌ 同族必死 |
| `A1VAAbWe` | ASI/MINVOL1M | COUNTRY d3 | 4.60 | **3.33** | 0.2458 | **0.6634** | **0.6634** | 0.037 | ✅ 过闸（本轮可交） |
| `npvEEWO8` | ASI/MINVOL1M | SECTOR d3 | 4.30 | 3.12 | 0.2455 | **0.6593** | **0.6593** | 0.041 | ✅ 过闸（本轮可交） |
| `kqNYbVzg` | GLB/MINVOL1M | SLOW d1 | 6.82 | 3.70 | 0.3466 | **0.7209** | — | — | ❌ 档内第 3 颗 |
| `npvGgKJa` | GBR/TOP700 | INDUSTRY d1 | 4.10 | 4.07 | 0.1657 | **0.7170** | — | — | ❌ 档内已 6 颗 |

### D. 三条派生结论

1. **同族 vs 异族是数量级差异**：STAT d1 vs STAT d2 = **0.9906**；STAT d2 vs COUNTRY d3 = **0.6633**、vs SECTOR d3 = **0.6364**。换族带来的去相关约 0.32。
2. **异族有效但受档位容量约束**：档内 1 颗时异族可共存（0.63–0.66）；档内 6 颗时异族也顶到 0.717；档内 2 颗时第 3 颗 0.7209。⇒ **档内 SUPER ≥5 即饱和，换族不再是杠杆**。
3. **提交会定向顶高邻近候选**：`A1VAAbWe` 0.6315→0.6634（top1 从 `88jaV5lv` 换成 `d5WGG5bg`）；`npvEEWO8` 纹丝不动（top1 仍 `88jaV5lv`，d5WGG5bg 只排第二 0.6364）⇒ 漂移只作用于「与新增颗相关 > 原 top1」的候选，不是普涨。

### E. 本轮执行状态

- **排序第一 `d5WGG5bg`：已在平台（ACTIVE）**，`submit_verdict` 返回 `ALREADY_SUBMITTED`，未重复 POST。
- **未新增提交**：ASI 当日配额已被 #1 占用（全账户历史零「同区同日 2 颗」，平台强制 1/天/区；无论按 ET 还是 UTC 日历，`d5WGG5bg` 与此刻同一日）。
- **下轮不预设提交对象**：`A1VAAbWe` / `npvEEWO8` 仅为本轮过闸记录，**不构成下轮预选承诺**。下轮须按 §G 先重跑方案、再按新排序表取第 1 名。

### F. 对第五节「已占档区域」的修正

原文「同档换族=同席」对 **ASI 不成立**（1 颗占用即可容第 2 颗异族）。对其他区的验证结果：

| 区 | 档内 SUPER | 异族实测 | 结论 |
|---|---:|---|---|
| ASI/MINVOL1M | 1 | 0.6593–0.6634 过 | **可容第 2 颗** |
| GLB/MINVOL1M | 2 | 0.7209 死 | 饱和 |
| GBR/TOP700 | 6 | 0.7170 死 | 饱和 |
| DEU/TOP500 | 2 | 0.69–0.77 死（旧测） | 饱和 |
| USA/TOP2000 | 1 | 0.6957–0.7032 死（旧测） | 饱和 |
| EUR/TOP2500 | 2 | 0.6546（CROWD）/0.4621（STAT） | **待测异族**（未实测新族） |

⇒ **EUR/TOP2500 是下一个值得试异族的档**（现有 max corr 仅 0.4621，为全账户最低）。

### G. 规则修正（2026-11-10 09:35，用户明令）· 每轮独立决策

原 §E 写「明日 06:30 自动提交 `A1VAAbWe`」被用户否定：**不是按本方案预定的候选提交**。

| 项 | 错误写法（作废） | 现行规则 |
|---|---|---|
| 提交对象来源 | 上轮方案预选好、次日直接执行 | **每轮先跑完整方案，再取本轮排序表第 1 名** |
| 上轮结论效力 | 「明日首交 XXX」视为承诺 | 只作候选池输入，**不作提交对象**；必须重算五量 + `refresh=True` 重测双闸 + 重查配额/档内族 |
| 文档与提交顺序 | 可先提交后补文档 | **方案文档先落盘（含本轮排序表 + 提交判定段），再提交** |

已写入定时任务 `bd08ec45` §0.7（每轮独立决策）+ §7（前置：文档已落盘）+ §9（记忆里禁止写「明日首交 XXX」这类预选承诺）。
