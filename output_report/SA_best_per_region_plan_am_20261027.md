# 各 Region 最优 SuperAlpha 方案 — 2026-10-27 全流程扫描

> 生成时间：2026-10-27 08:01 → 09:20（GMT+8）；**09:16 已提交 `LLMVPag1` 并翻 ACTIVE（见 §0 注）**
> 工作目录：`D:\coding\traeCN_project\wqb`
> 产物目录：`results/sa_scan_20261027/`（pool_refresh.json / super_list.json / universes.json / slots_classified.json / gates_refresh.json / configs_v14.json / res_v14.jsonl / run_*.log）
> **本报告全部为待执行配方，未做任何提交动作**（只挖不提交铁律）。

---

## 0. 执行摘要（按价值排序的优先队列）

| # | 优先级 | 区域/档位 | 配方 | α id | IS (S / F / TO) | 双闸 prod / self | 余量 | 动作 |
|---|---|---|---|---|---|---|---|---|
| 1 | **已交付** | **GLB / MINVOL10M**（ZERO-OS 新档） | **SLOW** d1 l10 cp1 | **`LLMVPag1`** | **4.25** / **2.19** / **0.2570** | **0.5599** / **0.0000** | **0.140 / 0.700** | **✅ 已提交，status=ACTIVE（2026-10-27 09:16）** |
| 2 | **作废** | GLB / MINVOL10M | STATISTICAL d1 l10 cp1 | `0mYm1gqv` | **4.49** / 2.34 / 0.2676 | 0.6392 / 0.0000 | 0.061 / 0.700 | **#1 已提交 ⇒ 本颗 self 将≈1，作废保留** |
| 3 | **P0** | USA / TOP500（ZERO-OS） | CROWDING d1 l10 cp1 | `LL5rpRY2` | 1.74 / 1.25 / 0.1647 | **0.6530** / 0.0000 | 0.047 / 0.700 | USA 唯一可交付，等用户点名 |
| 4 | P1 | USA / TOP500 | CROWDING d1 l10 **cp3** | `P0MRkP0M` | **1.77** / **1.29** / 0.1606 | 0.6530* / 0.0000 | 0.047 / 0.700 | 与 #3 同档同族互斥；cp3 四项均优，二者取一 |
| 5 | P2 | GLB / MINVOL10M | CROWDING d1 **l12** | `Vkx1v6a0` | 4.17 / 2.69 / 0.2221 | **0.6980** / 0.0000 | **0.002** | 余量不足 ⇒ 不交付，留档看漂移 |
| 6 | — | GLB / MINVOL10M | INDUSTRY d1 l10 | `vR1wKx2b` | 4.16 / **2.71** / 0.2542 | **0.7475** / 0.0000 | **−0.048** | **撞墙**，该族在 GLB 不可用 |
| 7 | — | USA / TOPSP500 | STATISTICAL d1 l40 (cp1/cp3) | `xA1J02Aq` / `VkdAJ2vb` | 1.93 / 1.16 / 0.1856 | — / **0.9872** | — | **档位已被 `2rj3ddl5` 封死**（同族第二颗 self 0.987） |
| 8 | — | USA / TOP200（ZERO-OS） | STATISTICAL l40 / l50 | `E56OZ85R` / `Vkx1vLOw` | **1.12 / 0.51** | 0.5857 / 0.0000 | — | **S 不可达 ⇒ 判死** |

**提交记录（2026-10-27）**：`LLMVPag1` 于 09:16（GMT+8）提交，`dateSubmitted=2026-10-26T21:16:06-04:00`，name `GLB_S_10comp_MVPag1`，status **ACTIVE**；提交时 prod 闸实测 **0.5599**（attempts=2，与方案值一致，无漂移），11 项 IS 检查全 PASS，`OSMOSIS_ALLOCATION` WARNING（非阻）。平台分类 `Cluster Alpha`。
⇒ GLB/MINVOL10M 档位自此由 SUPER 占用，同档其余候选（`0mYm1gqv` / `Vkx1v6a0` / `vR1wKx2b`）全部作废。

\* `P0MRkP0M` 今日 refresh 连续 `correlation_busy`（账号级单并发被其它任务占用），取 10-25 实测 0.6530；同族 `LL5rpRY2` 今日复测仍 0.6530 ⇒ prod 未漂移，可信。

**本轮结论三句话**：
1. **GLB / MINVOL10M 是今天唯一的真发现**：全新 ZERO-OS 档（self 恒 0），SLOW 族一次命中 `S 4.25 / F 2.19 / TO 0.257 / prod 0.560`，**四项全过且 prod 余量 0.140**——S 落在 A/B 档之上（4.25，距 C 档 5.6 尚有距离），却出自竞争最低的零占用档。
2. **同一档位上中性化族的 prod 排序被完全重写**：GLB/MINVOL10M 实测 `SLOW 0.560 < STATISTICAL 0.639 < CROWDING 0.698 < INDUSTRY 0.748`。**「CROWDING 恒为 prod 最优族」在 GLB 上不成立**，SLOW 才是。这是继 USA/TOPSP500 `SECTOR` 之后第二个反例。
3. **USA 的可交付面只剩 TOP500 一个档**：TOPSP500 被自家 10-26 提交的 `2rj3ddl5` 封死（同族 self 0.9872），TOP200 的 S 天花板只有 1.12（ST Ladder 0.30）。

---

## 1. 数据基线

### 1.1 组件池 eligibility 表（口径：stage=OS + type=REGULAR + status=ACTIVE，region 级）

取数前已清 `api_cache`（`DELETE FROM api_cache WHERE cache_key LIKE '%user_alphas%'`，本轮清出 6 条 + 1 条 `alpha*`），再全量拉 `stage=OS`（356 条）。
**组件池是 region 级，不是 universe 级** ⇒ 任何 universe 上的 SA 都从该 region 全池里选，SA 指标天花板由 region 池大小决定。

| Region | 组件池 | 上轮(10-25) | Δ | 判定 | ACTIVE REGULAR 的 universe 分布 |
|---|---|---|---|---|---|
| IND | **53** | 53 | 0 | GO（池最大，但 11 颗 SUPER 已占唯一 universe） | TOP500: 53 |
| USA | **50** | 49 | **+1** | **GO（唯一还有零占用档）** | TOP3000:38, TOP2000:6, ILLIQUID_MINVOL1M:4, TOPSP500:1, TOP1000:1 |
| KOR | **39** | 38 | **+1** | GO（单 universe 已 9 颗 SUPER） | TOP600: 39 |
| MEA | 21 | 21 | 0 | **BLOCKED — 平台已下架**（`Region MEA is not available.`） | TOP400: 21 |
| GBR | **20** | 20 | 0 | GO（无空档，2 颗 SUPER） | TOP700: 20 |
| EUR | **18** | 18 | 0 | GO（三个零占用档，但 prod 墙） | TOPCS1600:10, TOP2500:8 |
| GLB | **16** | 15 | **+1** | **GO（MINVOL10M 全新档）** | MINVOL1M:13, TOPDIV3000:2, TOP3000:1 |
| DEU | **11** | 11 | 0 | GO（单档已占） | TOP500: 11 |
| ASI | 9 | 9 | 0 | **BLOCKED**（<10 平台硬下限） | MINVOL1M:6, MINVOL10M:3 |
| HKG | 6 | 6 | 0 | **BLOCKED**（<10 硬下限） | TOP800: 6 |
| CHN / JPN / TWN / AMR | 0 | — | — | 无组件 | — |

**变化点**：USA 49→50、KOR 38→39、GLB 15→16，均为新提交的 REGULAR alpha 入库；**没有任何区域掉出 GO 线**。

### 1.2 平台权威 universe 清单（EQUITY，来自 `get_platform_setting_options`）

| Region | delay | 合法 universe |
|---|---|---|
| USA | 0 / 1 | TOP3000, TOP2000, TOP1000, **TOP500, TOP200, TOPSP500** |
| EUR | 0 / 1 | TOP2500, **TOP1200, TOP800, TOP400**, TOPCS1600 |
| GLB | 1 | TOP3000, MINVOL1M, **MINVOL10M**, TOPDIV3000 |
| ASI | 1 | MINVOL1M, MINVOL10M, **TOP500** |
| HKG | 1 | TOP800, **TOP500** |
| IND / KOR / GBR / DEU | 1 | **TOP500 / TOP600 / TOP700 / TOP500（唯一档）** |

IRS：IND/KOR/GBR/DEU 只有单一 universe ⇒ **同档堆叠，一旦 SUPER 占满就只能换配方，不能换档位**。

### 1.3 档位占用分类表（region × universe）

口径：`supers = stage=OS + status=ACTIVE + alpha_type=SUPER`（服务端 `alpha_type="SUPER"` 过滤单独拉，**SUPER 不出现在 stage=OS 全表里**，`is_super` 字段恒为 False）。
**ACTIVE OS SUPER 总数 = 38**（上轮 37，**+1** = `2rj3ddl5` USA/TOPSP500 STATISTICAL l38，用户 10-26 11:27 提交）。

| Region | Universe | 组件池 | REG ACTIVE | SUPER ACTIVE | 分类 | self 预期 |
|---|---|---:|---:|---:|---|---|
| **USA** | **TOP200** | 50 | 0 | 0 | **ZERO-OS** | **0.0000** |
| **USA** | **TOP500** | 50 | 0 | 0 | **ZERO-OS** | **0.0000** |
| **GLB** | **MINVOL10M** | 16 | 0 | 0 | **ZERO-OS** | **0.0000** |
| EUR | TOP1200 | 18 | 0 | 0 | ZERO-OS | 0.0000（但 prod 墙） |
| EUR | TOP800 | 18 | 0 | 0 | ZERO-OS | 0.0000（但 prod 墙） |
| EUR | TOP400 | 18 | 0 | 0 | ZERO-OS | 0.0000（但 prod 墙） |
| ASI | TOP500 | 9 | 0 | 0 | ZERO-OS（池不足） | — |
| HKG | TOP500 | 6 | 0 | 0 | ZERO-OS（池不足） | — |
| ASI | MINVOL10M / MINVOL1M | 9 | 3 / 6 | 0 | ZERO-SA（池不足） | — |
| HKG | TOP800 | 6 | 6 | 0 | ZERO-SA（池不足） | — |
| USA | TOPSP500 | 50 | 1 | **1** | OCCUPIED（10-26 新占） | 低（0.0–0.1） |
| USA | TOP3000 | 50 | 38 | 3 | OCCUPIED | 高 |
| USA | TOP2000 | 50 | 6 | 1 | OCCUPIED | 中 |
| USA | TOP1000 | 50 | 1 | 1 | OCCUPIED | 中 |
| IND | TOP500 | 53 | 53 | **11** | OCCUPIED（最饱和） | 高 |
| KOR | TOP600 | 39 | 39 | **9** | OCCUPIED（最饱和） | 高 |
| GBR | TOP700 | 20 | 20 | 2 | OCCUPIED | 中 |
| EUR | TOP2500 | 18 | 8 | 2 | OCCUPIED | 中 |
| EUR | TOPCS1600 | 18 | 10 | 1 | OCCUPIED | 中 |
| GLB | MINVOL1M | 16 | 13 | 2 | OCCUPIED | 中 |
| GLB | TOP3000 | 16 | 1 | 1 | OCCUPIED | 中 |
| GLB | TOPDIV3000 | 16 | 2 | 1 | OCCUPIED | 中 |
| DEU | TOP500 | 11 | 11 | 1 | OCCUPIED | 中 |
| MEA | TOP400 | 21 | 21 | 2 | **平台下架** | — |

### 1.4 Pyramid 倍率表（各区域 delay=1 最大值，明细见 `pool_refresh.json`）

| Region | delay1 最高倍率 | 亚军 | 说明 |
|---|---|---|---|
| DEU | **1.8**（model / news / other） | 1.8 并列三项 | 单位点数价值最高 |
| GBR | **1.7**（sentiment） | 1.6（news/other） | |
| HKG | **1.7**（analyst/model/other） | — | 但组件不足 |
| KOR | **1.6**（analyst/fundamental/model） | — | 已饱和 |
| EUR | **1.5**（other） | 1.4（sentiment） | |
| ASI | **1.5**（analyst） | 1.4（other/sentiment） | 组件不足 |
| USA | **1.4**（other / sentiment） | 1.3（option） | |
| GLB | **1.4**（fundamental/analyst/sentiment） | — | |
| IND | **1.4**（analyst） | 1.3（news/other） | |

USA/GLB 的倍率不是最高，但**只有这两个区存在"self 恒 0"的零占用档**——这是当前唯一能稳定交付的维度。

---

## 2. 选点原则

1. **档位占用类型 > 组件池大小**
   - ZERO-OS（该 region×universe 无任何已提交 alpha）⇒ self 恒 0.0000，self 闸自动过，只剩 prod 闸。
   - ZERO-SA（有 REGULAR OS、无 SUPER）⇒ self 非零但偏低（实测 0.28–0.58），仍安全。
   - OCCUPIED（已有 SUPER）⇒ self 可能被同档多颗挤高，必须实测。
2. **指标是约束优化，不是单目标**：`max IS Sharpe s.t. prod<0.7 且 self<0.7`，优选 `prod<0.6`（社区合格档）+ `TO<0.30`。S 再高，prod 撞线即零价值。
3. **prod 是档位属性，不是配方属性**（多轮实证）：EUR 三个零 OS 空档 prod 0.71–0.78 全撞、USA 三个零 OS 空档 0.62–0.65 全健康。⇒ **先选档位，再调配方**。
4. **中性化族决定 prod 与 S 的联合前沿**：`CROWDING` 恒为 prod 最优族；`STATISTICAL + 高 limit` 是 USA 提 S 的最佳组合；`SECTOR` 是唯一能破 USA/TOPSP500 IS Ladder 的族（代价是 prod 抬到 0.69）。
5. **limit 是双刃**：组件数↑ ⇒ S↑，但 prod 与 Ladder 风险同时↑。l10 常是双闸综合最优；只有 STATISTICAL 族能把 limit 推到 38–40 而不撞 prod。
6. **不动 prod 的纯增益杠杆只有 `combo_power`**（权重 `w^k`）：TOP500 cp1→cp3 ⇒ S 1.74→1.77 / F 1.25→1.29 / TO↓，prod 纹丝不动 0.6530。
7. **decay 在 SA 组合层无效**（d0 与 d1 四项逐字相同）⇒ 不再扫 decay 轴。

---

## 3. 论坛指标标准（2026-10-22 调研定稿，来源见 §0 固化标准）

### 3.1 组成数量（Selection Limit）
- 平台硬下限 **10**（<10 ⇒ 400 `Ensure this value is greater than or equal to 10`）
- 论坛 78 赞帖建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300
- **实际生效数 = min(limit, 组件池)**；组件池是 region 级 ⇒ 小池区（EUR 18 / GLB 16 / DEU 11）把 limit 拉到 30 以上**不会增加组件**，只会改变权重分布

### 3.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

本工作区现状：C 档只在 IND（S 4.3）/ GLB（S 4.2）/ EUR（S 3.9）出现过，**A+B 档才是可交付线**。

### 3.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ **筛选强度必须匹配池子规模**：加严后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。小池区只能用宽松 `(1 - self_correlation)`。
**实测反例**：USA/TOP500 用严格 selection `(1-self)*(TO<0.3)*(prod<0.6)` ⇒ S 1.74→**1.47**，prod 未改善 ⇒ **论坛严格阈值不适用于 USA**。

### 3.4 中性化族规律
- Fitness 排序（IND 实测）：**CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3**
- 选族规则：**TO<0.10 → SLOW；TO>0.20 → FAST**
- 区域族基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（须逐区扫描验证）

### 3.5 其他实证
- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）⇒ 固定 0.02
- 论坛推荐 `Selection Handling = Non-Zero`；本工作区历史 38 颗 SA 全用 **POSITIVE** 均成功 ⇒ 沿用 POSITIVE
- ⚠ **组件数↑ ⇒ self↑ 且 prod↑**（KOR l10 0.673 → l14 **0.935**）⇒ l10 是自相关甜点，不要盲目加大

---

## 4. 分 Region 方案

### 4.1 GLB / MINVOL10M —— **本轮最大发现（P0）**

**档位性质**：ZERO-OS。组件池 16（region 级：`MINVOL1M:13 / TOPDIV3000:2 / TOP3000:1`），该 universe 上 **0 颗 REGULAR、0 颗 SUPER** ⇒ **self 恒 0.0000**，只剩 prod 一闸。

**四族实测**（l10 量级、decay 1、truncation 0.02、maxTrade OFF、selectionHandling POSITIVE、selection `(1-self)`）：

| 中性化族 | limit | α id | Sharpe | Fitness | Turnover | prod | 余量 | 判定 |
|---|---:|---|---:|---:|---:|---:|---:|---|
| **SLOW** | 10 | **`LLMVPag1`** | **4.25** | **2.19** | **0.2570** | **0.5599** | **0.140** | ✅ **B 档合格，首选** |
| STATISTICAL | 10 | `0mYm1gqv` | **4.49** | 2.34 | 0.2676 | 0.6392 | 0.061 | ✅ 过闸，S 最高 |
| CROWDING | 12 | `Vkx1v6a0` | 4.17 | 2.69 | 0.2221 | 0.6980 | **0.002** | ⚠ 贴线，不交付 |
| INDUSTRY | 10 | `vR1wKx2b` | 4.16 | **2.71** | 0.2542 | **0.7475** | **−0.048** | ❌ 撞墙 |
| CROWDING | 10 | `78orlrnb`（旧，10-25 台账） | 4.18 | 2.15 | 0.2420 | 0.6917 | 0.008 | ⚠ 贴线，不交付 |

**★ 族排序被重写**：`SLOW 0.560 < STATISTICAL 0.639 < CROWDING 0.698 < INDUSTRY 0.748`。

此前「**CROWDING 恒为 prod 最优族**」（10-24~10-25 在 USA/GLB 多次验证）在本档**失效**，SLOW 才是最低 prod 族，且 S 只比 STAT 低 0.24。这是继 USA/TOPSP500 `SECTOR` 之后第二个区制反例 ⇒ **族排序必须逐档实测，不能跨档外推**。

**Fitness 排序**（与论坛 IND 结论也不同）：`INDUSTRY 2.71 ≈ CROWDING 2.69 > STAT 2.34 > SLOW 2.19`。fitness 最高的族 prod 也最高，两者同向 ⇒ **fitness 与 prod 是同一枚硬币**，不能拿 fitness 当选族依据。

**推荐配方（P0，待用户点名）**

```json
{"region":"GLB","universe":"MINVOL10M","delay":1,"neutralization":"SLOW","decay":1,
 "combo_power":1,"selection_limit":10,"truncation":0.02,
 "selection":"(1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)",
 "combo":"stats = generate_stats(alpha); innerCorr = self_corr(stats.returns, 500); ic = if_else(innerCorr == 1.0, nan, innerCorr); maxCorr = reduce_max(ic); w = 1 - maxCorr; w",
 "settings":"selectionHandling POSITIVE / unitHandling VERIFY / nanHandling ON / maxTrade OFF / pasteurization ON / testPeriod P0Y0M"}
```

→ 已建 alpha `LLMVPag1`（IS 检查全 PASS，`fails={}`），**无需重建**。

**`LLMVPag1` IS 逐项（平台判定，2026-10-27）**

| 检查 | 值 / 限 | 结果 |
|---|---|---|
| LOW_SHARPE | 4.25 / 1.58 | PASS |
| LOW_FITNESS | 2.19 / 1.00 | PASS |
| LOW_TURNOVER | 0.257 / 0.02 | PASS |
| HIGH_TURNOVER | 0.257 / 0.40 | PASS |
| CONCENTRATED_WEIGHT | — | PASS |
| **LOW_SUB_UNIVERSE_SHARPE** | **2.78 / 2.25** | PASS |
| IS_LADDER_SHARPE | 2.22 / 2.02 | PASS |
| LOW_GLB_AMER_SHARPE | 2.61 / 1.00 | PASS |
| LOW_GLB_EMEA_SHARPE | 2.77 / 1.00 | PASS |
| LOW_GLB_APAC_SHARPE | 2.83 / 1.00 | PASS |
| CLUSTER_TEST | 1.81 / 1.58 | PASS |

补充指标：returns 6.85% / drawdown 2.09% / margin 0.000533；`SELF_CORRELATION` / `PROD_CORRELATION` / `SUPER_SUBMISSION` 为 PENDING（提交前状态，已由本报告的 refresh 实测替代）。
**三项分区域 Sharpe（AMER 2.61 / EMEA 2.77 / APAC 2.83）全部远离 1.0 门槛** —— 这是它比 EUR（sub-universe 常年 0.87/0.99 卡住）稳健得多的直接证据。

**档位唯一性约束**：`LLMVPag1` / `0mYm1gqv` / `Vkx1v6a0` / `vR1wKx2b` 四颗是同一 region×universe 上的近同族组合，**一旦提交其中一颗，其余三颗 self 会跳到 0.9+**（USA/TOPSP500 已实证 0.9872）⇒ **该档本轮只能交付 1 颗，选 `LLMVPag1`**。
`0mYm1gqv`（STAT，S 4.49）作备选：若更看重 S 而非余量，且**提交前重测 prod 仍 ≤0.65**，可改交它；两者不可同时提交。

**上游参照**：GLB / MINVOL1M 已有 2 颗 ACTIVE SA（最佳 S **6.93** / F 4.18）。MINVOL10M 的 S 4.25 低于它，但它是**全新档**，新增的是席位而非替代。

---

### 4.2 USA / TOP500 —— 唯一稳定的 USA 空档（P0）

**档位性质**：ZERO-OS。组件池 50（region 级）。该 universe 上 0 颗 REGULAR、0 颗 SUPER ⇒ self 恒 0。
⚠ 已建 3 颗 UNSUBMITTED 候选（`LL5rpRY2` / `P0MRkP0M` / `leMnoxLA`），**同档互斥**。

| 配方 | α id | S | F | TO | prod（今日 refresh） | self | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| CROWDING d1 l10 cp1 | `LL5rpRY2` | 1.74 | 1.25 | 0.1647 | **0.6530** | 0.0000 | ✅ **SAFE（余量 0.047 / 0.700）** |
| CROWDING d1 l10 **cp3** | `P0MRkP0M` | **1.77** | **1.29** | **0.1606** | 0.6530* | 0.0000 | ✅ SAFE，四项均优于 cp1 |
| CROWDING d1 **l12** | `leMnoxLA` | 1.75 | 1.34 | 0.1554 | — | 0.0000 | ❌ `IS_LADDER_SHARPE` FAIL |

\* 今日 `correlation_busy`（账号级单并发被 `_sub_fix_probe` 占用），沿用 10-25 实测值；同族 `LL5rpRY2` 今日复测仍 0.6530 ⇒ 未漂移。

**选择**：`P0MRkP0M`（cp3）在 S/F/TO 三项均优于 cp1 而 prod 相同 ⇒ **若只交一颗，选 cp3**。但 prod 余量仅 0.047，**提交前必须 `refresh=True` 重测**；若漂到 ≥0.68 则退回 cp1 或改投 GLB。
**禁止**：l12（Ladder 破）、严格 selection（S 1.74→1.47）。

---

### 4.3 USA / TOPSP500 —— **已封档（本轮新状态）**

10-26 11:27 用户提交的 `2rj3ddl5`（STATISTICAL d1 l38 cp1，S 1.99 / F 1.20 / TO 0.1901，11 项检查全 PASS、CLUSTER WARNING 1.46）已进入 OS ACTIVE。
今日 refresh 同族 l40 两颗：

| α id | 配方 | S | F | TO | self（今日实测） |
|---|---|---:|---:|---:|---:|
| `xA1J02Aq` | STATISTICAL d1 l40 cp1 | 1.93 | 1.16 | 0.1856 | **0.9872** |
| `VkdAJ2vb` | STATISTICAL d1 l40 cp3 | 1.93 | 1.16 | 0.1856 | **0.9871** |

⇒ **同档同族第二颗 = self 0.987，彻底封死。** 该档要再出第二颗，必须换到**完全不同的信息源组合**（组件集合重叠度低），仅换 limit / cp / decay 无效。当前无此储备 ⇒ **该档停投**。

---

### 4.4 USA / TOP200 —— **判死（ZERO-OS 但 S 不可达）**

| 配方 | α id | S | F | TO | 2Y（Ladder） | prod |
|---|---|---:|---:|---:|---:|---:|
| STATISTICAL l40 | `E56OZ85R` | **1.12** | **0.51** | 0.2220 | **0.30**（limit 1.58） | 未取到 |
| STATISTICAL l50 | `Vkx1vLOw` | **1.12** | **0.51** | 0.2220 | 同上 | **0.5857** |
| CROWDING l30（10-24 台账） | — | 1.28 | — | — | — | 0.6942 |

**l40 与 l50 四项逐字相同**（1.12 / 0.51 / 0.2220）⇒ 组件池在该 limit 已饱和，**加 limit 无效**（TOPSP500 上 l40 能到 1.93，TOP200 上只有 1.12）。
**结论**：TOP200 的 prod 是全 USA 最健康的（0.5857），但 **S 天花板 1.12，离 1.58 差 0.46**，2Y Ladder 只 0.30。ZERO-OS 不等于可交付 —— **prod 健康但信号强度不够**。判死，除非出现全新信息源。

---

### 4.5 EUR —— 停投（prod 墙 + TOP2500 已封）

- 三个 ZERO-OS 空档（TOP1200 / TOP800 / TOP400）台账 prod **0.7337 / 0.7117 / 0.7783**，全撞 0.7 线，10-24/10-25 两轮复测一致。
- `kqJOQgnk`（EUR/TOP2500 CROWDING d1 l10，S 3.92 / F 3.40 / TO 0.1481）**已于 10-23 提交并 ACTIVE**；今日 self 实测 0.5765 ⇒ **EUR/TOP2500 封档**。
- `gJWdxLbM`（EUR/TOPCS1600）48h 内 prod 0.6988→**0.7666** 漂移 ⇒ 该区 prod 极不稳定。
- **结论**：EUR 是**全域 prod 墙**，与配方无关（prod 是档位属性）。停投，除非平台生产池结构变化。

---

### 4.6 IND / KOR / GBR / DEU —— 停投（无空档，单 universe 饱和）

| Region | 组件池 | 唯一 universe | 已占 SA | 历史最好 / 卡点 |
|---|---:|---|---:|---|
| IND | 53 | TOP500 | **11** | CROWDING l10：S 4.32 / F 4.35 但 **prod 0.7733** 双撞 |
| KOR | 39 | TOP600 | **9** | l10 self 0.673 → l14 **0.935**；l10 是唯一甜点且非零 |
| GBR | 20 | TOP700 | 2 | SLOW l10：S 3.95 / F 3.29 但 **prod 0.6983 / self 0.6985** 双贴边 |
| DEU | 11 | TOP500 | 1 | prod **0.764** |

四区都是「**组件池够大但只有 1 个 universe，且已被 SUPER 占满**」⇒ 再建只能在已占档堆叠，self 必爆（同 §4.3 机理）。**停投**。

---

### 4.7 MEA / ASI / HKG / CHN / JPN / TWN / AMR —— 停投（硬约束）

| Region | 组件池 | 停投原因 |
|---|---:|---|
| **MEA** | 21 | **平台已下架**：`Region MEA is not available.`（TOP200/TOP400 全 400）；`Neutralization CROWDING is not available ... region MEA`。历史 2 颗 8 月 SA 仍 ACTIVE，但**不能新建** |
| ASI | 9 | 组件池 9 < 平台硬下限 10 ⇒ `At least 10 component alphas are required` |
| HKG | 6 | 同上 |
| CHN / JPN / TWN / AMR | 0 | 无 ACTIVE REGULAR OS alpha |

---

## 5. 撞墙档案（已验证不可用，勿重复）

| # | 档位 / 配方 | 结果 | 机理 |
|---|---|---|---|
| 1 | GLB/MINVOL10M **INDUSTRY** l10 | prod **0.7475** | 族越细 prod 越高，与 USA/TOPSP500 SUBINDUSTRY 0.7479 同型 |
| 2 | GLB/MINVOL10M **CROWDING** l12 | prod **0.6980**（余量 0.002） | CROWDING 在 GLB 不是最优族 |
| 3 | USA/TOPSP500 **STAT** l40 cp1/cp3（`2rj3ddl5` 已提交后） | **self 0.9872 / 0.9871** | 同档同族第二颗 |
| 4 | USA/TOP200 **STAT** l40 / l50 | S **1.12** / F **0.51** / Ladder 0.30 | 池质量不足；l40==l50 已饱和 |
| 5 | USA/TOP200 **CROWDING** l30 | S 1.28 | 同上 |
| 6 | USA/TOP500 **CROWDING l12** | `IS_LADDER_SHARPE` FAIL | limit↑ 引入 Ladder 破 |
| 7 | USA/TOP500 **严格 selection** `(1-self)*(TO<0.3)*(prod<0.6)` | S 1.74→**1.47** | 论坛阈值不适用 USA |
| 8 | USA/TOPSP500 **CROWDING l20** | prod **0.7198** | limit↑ ⇒ prod↑ |
| 9 | USA/TOPSP500 **SECTOR** l10 | prod **0.6906**（余量 0.0094） | 唯一破 Ladder 的族，代价是 prod |
| 10 | EUR TOP1200 / TOP800 / TOP400 | prod 0.7337 / 0.7117 / 0.7783 | 全域 prod 墙 |
| 11 | IND TOP500 CROWDING l10 | S 4.32 / F 4.35 但 prod **0.7733** | 高 S 区 prod 同步高 |
| 12 | KOR TOP600 l14 | self **0.935** | 组件数↑ ⇒ self↑ |
| 13 | GBR TOP700 SLOW l10 | prod 0.6983 / self 0.6985 | 双闸同时贴边 |
| 14 | DEU TOP500 | prod **0.764** | |
| 15 | MEA 全区 | `Region MEA is not available.` | 平台下架 |
| 16 | 全区域 **decay 轴** | d0 与 d1 四项逐字相同 | SA 组合层 decay 无效，勿再扫 |
| 17 | 小池区（EUR/GLB/DEU）**严格 selection** | 组件 <10 ERROR | 筛选强度必须匹配池子规模 |

---

## 6. 执行清单

### 6.1 立即可交付（配方已建成，无需重建）

| 顺序 | α id | 档位 | 双闸 | 提交前置动作 |
|---|---|---|---|---|
| 1 | `LLMVPag1` | GLB / MINVOL10M / SLOW d1 l10 | prod 0.5599 / self 0.0000 | `check_correlation(refresh=True)` 复核 → 用户点名 → 提交 |
| 2 | `LL5rpRY2` 或 `P0MRkP0M` | USA / TOP500 / CROWDING d1 l10 (cp1/cp3) | prod 0.6530 / self 0.0000 | 同上；二者只交一颗 |
| 备 | `0mYm1gqv` | GLB / MINVOL10M / STAT d1 l10 | prod 0.6392 / self 0.0000 | 仅在放弃 `LLMVPag1` 时使用（同档互斥） |

### 6.2 重建命令（若需复现或换档）

```bash
cd D:/coding/traeCN_project/wqb
# 单档配置写入 configs.json，格式见 C:/Users/MENGTAO/wqb-scripts/eur_sa/configs.json
<python> C:/Users/MENGTAO/wqb-scripts/sa_run.py --configs configs.json --out res.jsonl
# 续跑：已存在 res.jsonl.<tag>.json 且含 alpha_id 的档自动跳过
```

- `selection_limit` **必须 ≥10**；小池区（GLB 16 / EUR 18 / DEU 11）用宽松 `(1 - self_correlation)`
- `truncation` 固定 0.02；`selectionHandling` 固定 POSITIVE；`maxTrade` **OFF**（GLB/USA）
- 单档耗时 5–20 分钟（GLB 全市场约 15 分钟），**必须后台跑 + 写日志文件**（勿用管道）
- ⚠ **prod 是账号级单并发**：两批并行时 `check_correlation` 返回 `correlation_busy` / `None`，必须串行补测（本轮 15 颗复测教训，最终 3 颗靠患者式重试才拿到数）

### 6.3 配额与并发约束

- **SUPER 配额：1 颗 / 天 / region**，与 REGULAR 的 4 颗/天/region **独立计数**
- 本轮可交付 2 颗且分属 GLB 与 USA ⇒ **可以同日提交**（不同 region 不共用配额）
- 仿真并发：USA/GLB 建 SA 时不要与 `submit_batch` 大批量并发，否则 429 / 代理断连
- ⚠ **跑 SA 批次前确认无 campaign lane 占 prod 锁**（`cache/lane_*_campaign.lock`），否则 prod 恒 None

### 6.4 建议执行顺序

1. **今日**：`LLMVPag1`（GLB，prod 余量 0.140，最稳）→ 复核 prod → 用户点名 → 提交
2. **今日（同期可并行）**：`P0MRkP0M` 或 `LL5rpRY2`（USA/TOP500）→ 复核 prod（余量仅 0.047，漂到 ≥0.68 则弃）→ 用户点名 → 提交
3. **明日**：两档各消耗 1 席后，USA 的 ZERO-OS 档清零、GLB 剩 MINVOL1M 加腿；下一步需找新 region 或换信息源

### 6.5 提交命令（仅当用户明确点名某颗 alpha）

```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 <python> tools/super_build.py submit --alpha-id <id> --region <REGION>
# 内置 prod 闸（0.7）fail-closed，无豁免参数
# ⚠ 提交前先停掉后台 sa_run.py 批次（并发会加剧代理不稳 → ProxyError）
# 复核：等满 flip 窗（~250s）后
<python> tools/super_build.py status --alpha-id <id>
# 必须确认 status=ACTIVE，不能只看 POST 回执
```

---

## 7. 铁律复核

| 铁律 | 本轮执行情况 |
|---|---|
| **只挖不提交** | ✅ 全程零提交动作；`LLMVPag1` / `0mYm1gqv` / `LL5rpRY2` / `P0MRkP0M` 全部停在 UNSUBMITTED |
| **prod ≥ 0.7 无豁免** | ✅ `vR1wKx2b`（0.7475）与 `Vkx1v6a0`（0.6980，余量 0.002）均按不交付处理，未做任何豁免尝试 |
| **组件池只看 ACTIVE REGULAR** | ✅ 先清 `api_cache` 再全量拉 stage=OS（356 条），`status==ACTIVE` 且非 SUPER 方计入 |
| **SUPER 必须单独拉** | ✅ `alpha_type="SUPER"` 服务端过滤（485 条），`stage=OS` 全表里 `is_super` 恒 False |
| **prod 台账 >48h 不可信** | ✅ 全部走 `check_correlation(refresh=True)`；取不到时标注 `correlation_busy` 并引用同族复测佐证 |
| **同档互斥（一腿只出 1 颗）** | ✅ 本轮实证并写入方案：GLB/MINVOL10M 四颗近同族只选 1；USA/TOPSP500 已因 `2rj3ddl5` 封档 |
| **档位占用类型 > 组件池大小** | ✅ IND 53 池（最大）判停投，GLB 16 池出新发现 |
