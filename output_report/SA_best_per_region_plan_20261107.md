# 各 Region 最优 SuperAlpha 方案（2026-11-07 06:30 扫描 · Run 13）

> **口径**：本方案全部为**待执行配方**，Run 13 本身**未提交任何 alpha**（提交权归用户，须点名）。
> **数据时点**：组件池/档位 2026-11-07 06:30（`probe_sa_candidates --refresh`，已先清 `api_cache`）；
> 双闸 07:00–07:35 平台实时计算（新 alpha 首次查询无缓存 ⇒ 均为 live 值，非台账）。
> **产物目录**：`results/sa_scan_20261107_r13/`｜上一版：`output_report/SA_best_per_region_plan_20261107.md`（03:10 版）

> ### 📌 提交记录（用户点名执行）
> **2026-11-07 10:03（ET 11-06 21:03:54）`3qoG6nEe` 已提交 → `status=ACTIVE`**，SUPER 配额 11-06 用 1/1。
> 提交前 `check_correlation(both)` 复测：prod **0.4708** / self **0.4714**（均 <0.7，余量 0.229）；prod 闸 live-probe 值同 0.4708。
> 稳健性台账 `robustness_3qoG6nEe` = **PASS**（10 年全正、负年 0、近 3 年 S 2.98/4.02/4.26、CV 0.181、margin 13.6bp）。
> 平台 checks：9 项全 PASS（含 `CLUSTER_TEST 2.62`、`LOW_ROBUST_UNIVERSE_SHARPE 2.26`、`IS_LADDER 4.15/2.02`），唯 `MATCHES_COMPETITION` WARNING（不挡）。
> **副作用**：IND/TOP500 **SLOW 族已封**；`MPYzlkd6`（↔0.7837 同席）正式作废。

---

## 一、执行摘要

### 1.1 本轮结论（三句话）

1. **组件池与档位零变化**：REGULAR ACTIVE **239**、SUPER ACTIVE **48**（自 11-05 提交 `88RNX7la` 后用户未再提交）⇒ **8 个 GO 区所有可建 universe 仍全部被 SUPER 占用**，SA 线全域饱和，本轮无「新空档」可开。
2. **三条「组合层权重整形」轴全线证伪**（9 档实测）：`sqrt(w)`、`ts_mean(w,20)`、`rank(w)` **均不产生新独立席**，其中 3 颗 PASS 全部撞已占同席（`0.9901` / `0.7837` / `0.7419` / `0.9917`）。⇒ **combo 权重整形不是 SA 的第二增长曲线，席位才是。**
3. **唯一新增（弱）席位**：`KPJzqnnz` GLB/TOP3000 CROWDING `rank(w)`，双闸 0.6623/0.6617 全过、与全池最大相关仅 **0.1781**（真独立席），但 S 3.46 / F 1.74 / TO **0.3711**（超社区 B 档 TO<0.30）⇒ 定为**备胎第 8 颗**，不作首选。

### 1.2 优先队列（收入序，双闸实测均在 24h 内）

> `Score = 2Y × F × margin × D1均值`（序数代理）。**收入序 ≠ 提交序**。
> SUPER 配额 **账号级 1/ET 日（跨区共享）**；被 prod 闸拦下**不消耗**配额。

| 序 | Alpha ID | Region/Universe | S | F | TO | self | **prod** | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| ~~1~~ | `3qoG6nEe` | IND/TOP500 | 4.45 | **3.67** | 0.266 | **0.4714** | **0.4708** ✓ | **0.229** | ✅ **已提交 → ACTIVE**（2026-11-06 21:03:54 ET）；IND TOP500 SLOW 档已封 |
| ⭐**2** | `xAr1Y5gg` | USA/TOP1000 | 2.80 | 2.05 | 0.146 | **0.3295** | **0.4777** ✓ | **0.222** | ✅ self 最安全（C 档） |
| ⭐**3** | `xAr1YZQb` | EUR/TOPCS1600 | 4.32 | 3.97 | 0.149 | 0.6007 | **0.6007** ✓ | 0.099 | ✅ EUR 唯一席（B 档贴线） |
| ⭐**4** | `e75avmq6` | USA/TOP2000 | 4.29 | 4.00 | **0.103** | **0.4871** | **0.6373** ✓ | 0.063 | ✅ 低 TO / 费后强 |
| **5** | `1YNl3p5R` | USA/TOP1000 | 2.61 | **2.38** | **0.134** | 0.6011 | 0.6011 ✓ | 0.099 | ✅ 11-07 新增席（CROWDING） |
| 6 | `Xg9WNRg8` | USA/TOP2000 | **4.74** | 4.10 | 0.166 | 0.6493 | 0.6493 ✓ | 0.051 | ✅ S 最高，余量薄 |
| 7 | `P0oM2P8L` | DEU/TOP500 | 2.40 | 1.92 | 0.152 | 0.5526 | **0.5522** ✓ | 0.148 | ✅ DEU 唯一席，D1 倍率 1.62 全场第一 |
| **8（备胎）** | `KPJzqnnz` | GLB/TOP3000 | 3.46 | 1.74 | **0.3711** ⚠ | 0.6623 | 0.6617 ✓ | 0.038 | ⚠ **本轮新增独立席**，TO 超 B 档、margin 0.000506 收入贡献低 |
| — | `MPYzlkd6` | IND/TOP500 | 4.49 | 3.65 | 0.278 | 0.6070 | 0.6066 ✓ | 0.093 | ✗ 同席（↔`3qoG6nEe` **0.7837**）且 prod 高 0.136 |
| — | `VkxzqnEb` | USA/TOP1000 | 2.83 | 2.09 | 0.146 | 0.3356 | **0.4729** ✓ | 0.227 | ✗ 同席（↔`xAr1Y5gg` **0.9917**）；指标略优但 self 略差 ⇒ 与 #2 等价备选 |
| — | `kqNGkWxd` | USA/TOP2000 | 3.66 | 3.82 | 0.142 | 0.6903 | 0.6903 ✓ | 0.010 | ✗ 同席（↔`Xg9WNRg8` **0.7419**）+ 余量 0.0097 < 0.02 红线 |
| — | `akKz2gmv` | DEU/TOP500 | 2.51 | 1.97 | 0.164 | 0.5840 | **0.5836** ✓ | 0.116 | ✗ 同席（↔`P0oM2P8L` **0.9901**）且 prod 高 0.031 |
| — | `omEGwNwk` | GBR/TOP700 | 3.64 | 3.58 | 0.154 | 0.7332 | 0.7333 ✗ | — | ✗ CROWDING 在 GBR **双闸全撞** |
| — | `d5Wz8KEJ` | KOR/TOP600 | 4.30 | **5.05** | 0.145 | 0.8209 | 0.8209 ✗ | — | ✗ FAST 族在 KOR 双闸全撞 |
| — | `e75G8KZl` | GLB/MINVOL1M | **6.82** | 3.71 | 0.345 | 0.7221 | 0.7208 ✗ | — | ✗ S 全场最高但双闸各超 0.02 |
| — | `0mYg9ldr` | USA/TOP3000 | 4.40 | **5.42** | 0.097 | 0.6707 | **0.7690** ✗ | — | ✗ prod 最脏（`rank(w)` 在 CROWDING 放大集中度） |

**互测（本地 `compute_mutual_correlation`，不占 prod 槽）**
- 队列 7 颗（1.2 表 #1–#7）两两最大 **0.5606**（`xAr1Y5gg`↔`1YNl3p5R`），最大独立子集 = **7**。
- 加入 `KPJzqnnz` 后最大独立子集仍 **7 颗**：它与队列 7 颗各项 ≤0.1781（最接近 `1YNl3p5R` 0.1781），但与 `VkxzqnEb` 抢同一席 —— 因 `VkxzqnEb` 与 `xAr1Y5gg` 互斥（0.9917），可替换后仍维持 7。
- 跨区近零相关（IND/DEU/KOR/GLB ↔ USA −0.05~0.08）。

### 1.3 提交排期建议（一天一颗，SUPER 配额账号级）

| 天序 | Alpha | Region | 理由 | 风险 |
|---|---|---|---|---|
| ~~Day 1~~ | `3qoG6nEe` | IND | ✅ **已提交 ACTIVE**（2026-11-06 21:03:54 ET，checks 全 PASS / RA failed 0） | 已封：IND/TOP500 SLOW 族 |
| Day 2 | `xAr1Y5gg` | USA/TOP1000 | 双闸余量 0.222/0.370 最抗漂移 | S 2.80 偏低 |
| Day 3 | `xAr1YZQb` | EUR | EUR 唯一可交付席 | prod 0.6007 贴 B 档、EUR 全域墙 |
| Day 4 | `e75avmq6` | USA/TOP2000 | TO 0.103、F 4.00 | prod 0.6373 余量 0.063 |
| Day 5 | `1YNl3p5R` | USA/TOP1000 | 独立席（↔#2 0.5606） | prod 0.6011 |
| Day 6 | `Xg9WNRg8` | USA/TOP2000 | S 4.74 最高 | 余量 0.051，提交前必 `refresh=True` |
| Day 7 | `P0oM2P8L` | DEU | D1 倍率 1.62 第一 | S/F 偏低，收入靠倍率 |
| Day 8（可选） | `KPJzqnnz` | GLB/TOP3000 | 唯一真独立新席（max 0.1781） | TO 0.3711、margin 0.000506 |

---

## 二、数据基线（2026-11-07 06:30 刷新）

### 2.1 组件池 eligibility（region 级，ACTIVE 已提交 REGULAR）

| Region | 组件池 | REGULAR 总量 | 未提交（IS） | 判定 |
|---|---|---|---|---|
| USA | **47** | 148 | 0 | ✅ GO |
| IND | **47** | 51 | 0 | ✅ GO |
| KOR | **33** | 520 | 485 | ✅ GO |
| GBR | **24** | 24 | 0 | ✅ GO |
| EUR | **22** | 343 | 315 | ✅ GO |
| MEA | 19 | 19 | 0 | ⛔ 平台已下架（新建 400） |
| GLB | **18** | 18 | 0 | ✅ GO |
| DEU | **13** | 163 | 150 | ✅ GO（池薄，prod 墙） |
| ASI | 9 | 9 | 0 | ⛔ 池 <10 硬下限 |
| HKG | 7 | 7 | 0 | ⛔ 池 <10 硬下限 |

> **口径修正（沿用 11-03 实证）**：组件池在**平台层是 region 级（跨 universe）**，`selectionLimit≥10` 时平台可从跨 universe 池抽组件 —
> 故 `REGULAR=0` 的档位（USA/TOP1000、GLB/TOP3000）仍能建成 SA。**但 delay 是池的第二键**（`USA/TOP500 d0` 池 = 0 ⇒ 400）。

### 2.2 档位占用分类（platform universes）

| 区域 | Universe | REGULAR | SUPER | 分类 |
|---|---|---|---|---|
| USA | TOP3000 | 38 | 6 | 🔴 OCCUPIED |
| USA | TOP2000 | 5 | 1 | 🔴 OCCUPIED |
| USA | TOP1000 | 0 | 1 | 🔴 OCCUPIED |
| USA | TOP500 | 0 | 1 | 🔴 OCCUPIED |
| USA | TOPSP500 | 0 | 1 | 🔴 OCCUPIED |
| USA | TOP200 | 0 | 0 | ⚪ ZERO_OS（历史判死：S≤1.28） |
| USA | ILLIQUID_MINVOL1M | 4 | 0 | ⚫ 非平台档（池 4） |
| IND | TOP500 | 47 | 11 | 🔴 OCCUPIED |
| KOR | TOP600 | 33 | 11 | 🔴 OCCUPIED |
| GBR | TOP700 | 24 | 5 | 🔴 OCCUPIED |
| EUR | TOP2500 | 13 | 2 | 🔴 OCCUPIED |
| EUR | TOPCS1600 | 9 | 1 | 🔴 OCCUPIED |
| EUR | TOP1200 / TOP800 / TOP400 | 0 | 0 | ⚪ ZERO_OS（结构性 prod 墙 0.71–0.78） |
| GLB | MINVOL1M | 17 | 2 | 🔴 OCCUPIED |
| GLB | MINVOL10M | 0 | 1 | 🔴 OCCUPIED |
| GLB | TOP3000 | 0 | 1 | 🔴 OCCUPIED |
| GLB | TOPDIV3000 | 1 | 1 | 🔴 OCCUPIED |
| DEU | TOP500 | 13 | 1 | 🔴 OCCUPIED |
| MEA | TOP400 | 19 | 2 | ⚫ 非平台档（区域下架） |
| ASI | MINVOL1M / MINVOL10M | 6 / 3 | 0 | ⚪ ZERO_SA（region 池 9 <10） |
| ASI / HKG / CHN / AMR | TOP500 / TOP800 / TOP2000U / TOP600 | 0 | 0 | ⚪ ZERO_OS（无组件） |

**结论**：**零 OS 档 7 个，全部为「无组件」或「历史判死」**；零 SA 档（ASI 2 个 / HKG 1 个）卡 region 池 <10。⇒ 本轮无「新空档」可开，产能只能靠**同档换配方做出新独立席**。

### 2.3 Pyramid 倍率（D1 按类别均值，越高越值钱）

| Region | D1 均值 | 最高类别（D1） |
|---|---|---|
| **DEU** | **1.619** | model/news/other/analyst/fundamental/sentiment 均 **1.8** |
| GBR | 1.413 | sentiment 1.7 / news·other·analyst 1.6 |
| HKG | 1.413 | analyst/model/other 1.7 |
| KOR | 1.387 | analyst/fundamental/model/news/other/sentiment **1.6** |
| EUR | 1.200 | other 1.5 / sentiment 1.4 |
| GLB | 1.192 | fundamental/analyst/sentiment 1.4 |
| ASI | 1.181 | analyst 1.5 |
| USA | 1.169 | other/sentiment 1.4 |
| IND | 1.140 | analyst 1.4 |

---

## 三、选点原则

1. **档位占用类型 > 组件池大小**：`零 OS alpha 档`（self 恒 0）> `仅零 SA 占用档`（self 0.28–0.33）> `同档换配方`。当前零 OS 档全不可建 ⇒ **只剩第三类**，判据从「找空档」变成「找**真独立席**（互测 <0.7）」。
2. **指标 = 约束优化**：`max S ∧ max F s.t. self<0.7 ∧ prod<0.7`（优选 **prod<0.6**，交付红线余量 **≥0.02**）。
   - 2026-11-03 起用户收紧口径：`prod<0.65` 双目标 Pareto。本轮实测 `KPJzqnnz` 0.6617 位于 0.65–0.70 之间 ⇒ 只作备胎。
3. **`SELF ≈ PROD` 是常态但非恒等**（`e75avmq6` 0.4871 vs 0.6373 差 0.15）⇒ **两闸禁互推**，必须各测。
4. **中性化族规律（不可跨区照搬）**
   - Fitness 排序（IND 实测）：CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3。
   - **族越"快"⇒ S 越高、prod 越脏**：GLB/MINVOL1M FAST S 6.34 但 self 0.7384/prod 0.7486 双撞；同区 SLOW 仅 0.560。
   - GBR：**SLOW(0.633) < STAT(0.671) < CROWDING(0.733)** ⇒ 英联邦市场 SLOW 有特殊优势，**"CROWDING 恒最优"不成立**。
   - 区域基线（须逐区扫）：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15。
5. **`limit` 不是杠杆**：`l10 → l12/l14` 使 prod↑（KOR l14 self 0.935；EUR l30 self 0.28 但 prod 0.61）⇒ **l10 是双闸最优点**，已在 48 颗中固化。
6. **`decay` 在 SA 组合层无效**：`d0` 与 `d1` 四项逐字相同（TOPSP500 CROWDING 1.70/1.16/0.1566/0.6246）⇒ 不再扫。

---

## 四、论坛指标标准（2026-10-22 定稿，无需重复调研）

> 来源：《【新人入门】Super Alpha 从入门到入门！》78 赞/39 评论、《2024 super alpha 比赛心得》22 赞/15 评论、《Super Alpha 参数设置》12 赞（含 LY43440 实测回复）。

### 4.1 组成数量

- **平台硬下限 = 10**（<10 直接 400：`Ensure this value is greater than or equal to 10`）。
- 论坛建议 **30–100 起测、≤500**；LY43440 实测 IND 取 300。
- **实际生效 = min(limit, 组件池)**；**池是 region 级** ⇒ SA 指标天花板由该 region 的 ACTIVE REGULAR 数决定。
- ⚠ 组件数↑ ⇒ **self↑ 且 prod↑**（EUR 实测 l10 self 0.33/prod 0.56 → l12 0.29/0.61 → l30 0.28/0.61；KOR l10 0.673 → l14 **0.935**）⇒ **l10 双闸综合最优**，不要盲目加大 limit。

### 4.2 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

**本账户落点**：C 档 prod（<0.5）= `3qoG6nEe` 0.4708 / `xAr1Y5gg` 0.4777 / `VkxzqnEb` 0.4729；
B 档（<0.6）= `P0oM2P8L` 0.5522 / `akKz2gmv` 0.5836；
A 档 = `xAr1YZQb` 0.6007 / `1YNl3p5R` 0.6011 / `e75avmq6` 0.6373 / `Xg9WNRg8` 0.6493 / `KPJzqnnz` 0.6617。
**TO 达 B 档（<0.30）的仅 7 颗队列中的 6 颗**，`KPJzqnnz`（0.3711）与 `e75G8KZl`（0.3449）不达标。

### 4.3 组件筛选阈值

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ **筛选强度必须匹配池规模**：加严后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。小池区（EUR/GLB/DEU）只能用宽松 `(1 - self_correlation)`。
⚠ **`author_*` 在本账户恒为常数**（作者级聚合量）⇒ 论坛阈值**不可消费**。
⚠ **严格 selection 是负杠杆**：USA/TOP500 `(1-self)*(TO<0.3)*(prod<0.6)` ⇒ S 1.74→1.47；把排序量换成 `prod_correlation` 更毁灭（S 1.77→1.04）。**排序必须留在 `self_correlation`**。

### 4.4 其他实证

- `truncation` 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）。
- 论坛推荐 `Selection Handling = Non-Zero`；本账户 48 颗 SA 全用 `POSITIVE` 均成功。

---

## 五、分 Region 方案

> 每区给「最优配方 + 预期指标 + 双闸实测 + 余量」。已交付队列成员标注 `★`。

### 5.1 IND / TOP500（池 47，11 席）

| 项 | 值 |
|---|---|
| **最优配方** | `SLOW` d1 l10 cp1 + selection `if_else(dataset_count==1,2,1)*(1-self_correlation)` |
| **Alpha** | `3qoG6nEe` |
| **预期/实测** | S **4.45** / F **3.67** / TO 0.266 / 2Y 4.15 |
| **双闸** | self **0.4714** / prod **0.4708** |
| **余量** | **0.229**（全场最厚） |
| 判据 | `dataset_count==1` 分档把单科目组件前置，是同档唯一能压 prod 的选择器 |

⚠ IND 已有 11 席（STAT 5 / SUB 2 / RAM / INDUSTRY / 无 SLOW）⇒ SLOW 是**唯一未占族**，`3qoG6nEe` 一旦提交即封档。
本轮 `MPYzlkd6`（SLOW+`sqrt(w)`）互测 ↔`3qoG6nEe` **0.7837**、prod 高 0.136 ⇒ **回填失败，勿用**。

### 5.2 USA（池 47，10 席，跨 5 个 universe）

| Universe | 配方 | Alpha | S | F | TO | self | prod | 余量 |
|---|---|---|---|---|---|---|---|---|
| TOP1000 | SLOW d1 l10 cp3 | ★`xAr1Y5gg` | 2.80 | 2.05 | 0.146 | **0.3295** | **0.4777** | **0.222** |
| TOP1000 | CROWDING d1 l10 cp3 | ★`1YNl3p5R` | 2.61 | 2.38 | 0.134 | 0.6011 | 0.6011 | 0.099 |
| TOP2000 | SLOW d1 l10 cp3 | ★`e75avmq6` | 4.29 | 4.00 | **0.103** | 0.4871 | 0.6373 | 0.063 |
| TOP2000 | SLOW d1 l10 cp3 | ★`Xg9WNRg8` | **4.74** | 4.10 | 0.166 | 0.6493 | 0.6493 | 0.051 |

- TOP1000/TOP2000 是 **USA 唯一能连供 4 颗的档位**（两两最大 0.5606）。
- 等价备选：`VkxzqnEb`（TOP1000 SLOW + `rank(w)`）prod **0.4729**（略优于 `xAr1Y5gg` 0.4777）、S 2.83、F 2.09，但 ↔`xAr1Y5gg` **0.9917** ⇒ **二者只取一，取已验的 `xAr1Y5gg`**。
- TOP3000 已 6 席（MARKET/SUB/STAT/FAST/SLOW×2），本轮 CROWDING+`rank(w)`（`0mYg9ldr` S4.40/F5.42/TO0.097）**prod 0.769 撞墙** ⇒ 该族关闭。
- TOP500 / TOPSP500 / TOP200 已判死（见 §七）。

### 5.3 GBR / TOP700（池 24，5 席）

| 族 | 已占 | 实测 prod |
|---|---|---|
| REVERSION_AND_MOMENTUM | `YPMp39q6` | — |
| STATISTICAL | `e7QGwrx6` / `MPYAOR0r` | ~0.671 |
| FAST | `rKRbrZKo` | — |
| **SLOW** | `QPvGdLYQ`（S 4.23） | **0.633**（族内最优） |
| CROWDING | **本轮 `omEGwNwk`** | **0.7333 双撞** ⇒ 关闭 |

⇒ **GBR 五族全占，本轮 CROWDING 试完即全封**。无新增席。

### 5.4 EUR（池 22，3 席 + 3 空档）

| Universe | 配方 | Alpha | prod |
|---|---|---|---|
| TOPCS1600 | STAT d1 l10 | ★`xAr1YZQb`（S4.32/F3.97） | 0.6007 |
| TOP2500 | STAT d1 l10 | `GrgGkV1o` | — |
| TOP2500 | CROWDING d1 l10 | `kqJOQgnk` | — |
| TOP1200/TOP800/TOP400 | CROWDING（已试） | — | **0.7337 / 0.7117 / 0.7783** ⇒ 结构性墙 |

⇒ **EUR 全域 prod 墙**（唯一可用 = `xAr1YZQb`，余量 0.099）。

### 5.5 KOR / TOP600（池 33，11 席）

11 席覆盖 SUB×2 / STAT×5 / RAM / CROWDING / SLOW（含 cp7 的 `88RNX7la`，S 4.45/F 5.28）。**唯一未占族 = FAST**，本轮实测 `d5Wz8KEJ`（FAST + `ts_mean(w,20)`）S 4.30/F **5.05** 但 self **0.8209** / prod 0.8209 ⇒ **双撞，FAST 在 KOR 关闭**。
⇒ **KOR 12 族位全部试完，封档。**

### 5.6 GLB（池 18，4 universe / 5 席）

| 档位 | 已占 | 本轮尝试 | 结论 |
|---|---|---|---|
| MINVOL1M | SUBINDUSTRY `A1NQ57NW`、STAT `LL5amzov`(S6.93) | SLOW+`sqrt(w)` `e75G8KZl` S **6.82** | self 0.7221 / prod 0.7208 ✗ |
| MINVOL10M | SLOW `LLMVPag1`(prod 0.56) | — | 已封 |
| TOP3000 | RAM `QPKVK8VW` | CROWDING+`rank(w)` **`KPJzqnnz`** | ✅ **独立席（max 0.1781）**，prod 0.6617、TO 0.3711 ⇒ 备胎 |
| TOPDIV3000 | STAT `npARO63x` | — | 已封 |

### 5.7 DEU / TOP500（池 13，1 席）

| 配方 | Alpha | S | F | TO | self | prod | 余量 |
|---|---|---|---|---|---|---|---|
| **SLOW d1 l10 cp1** | ★`P0oM2P8L` | 2.40 | 1.92 | 0.152 | 0.5526 | **0.5522** | 0.148 |
| SLOW + `sqrt(w)` | `akKz2gmv` | 2.51 | 1.97 | 0.164 | 0.5840 | 0.5836 | 0.116（↔P0oM2P8L **0.9901** 同席） |

⇒ DEU 池 13 只够 1 席；`sqrt(w)` 与 cp1 等效且更脏 ⇒ **保留 `P0oM2P8L`**（D1 倍率 1.62 全场第一）。

### 5.8 ASI / HKG（池不足）

ASI 9（MINVOL1M 6 + MINVOL10M 3）、HKG 7（TOP800 7）。**距硬下限 10 各差 1 / 3 颗** ⇒ 唯一解 = 先把本区攒着的 RA 提交成 ACTIVE（IS 不计入）。

---

## 六、停投区（已饱和，无新增席）

| 区域 / 档位 | 理由 |
|---|---|
| **EUR 全域** | 三空档 prod 0.7337/0.7117/0.7783；已占两档 0.60+。结构性墙，族不可救 |
| **IND / TOP500** | 11 席，SLOW 是最后空族（本轮已用掉并被同席证伪） |
| **KOR / TOP600** | 11 席 + FAST 本轮证伪 ⇒ 12 族位全满 |
| **GBR / TOP700** | 5 席 + CROWDING 本轮证伪 ⇒ 6 族位全满 |
| **DEU / TOP500** | 池 13，仅 1 席容量，已占 |
| **GLB / MINVOL1M·MINVOL10M·TOPDIV3000** | 分别 2/1/1 席，族已满 |
| **USA / TOP500·TOPSP500·TOP200** | S 不可达（1.28–1.99）或 prod 撞墙 |
| **USA / TOP3000** | 6 席，5 族全占；本轮 CROWDING 0.769 关闭第 6 族 |
| **MEA / ASI / HKG / CHN / JPN / TWN / AMR** | 区域下架 / 池 <10 / 无组件 |

---

## 七、撞墙档案（累计，含本轮）

### 7.1 本轮新增（9 条实测）

| Alpha | 档位 | 配方 | 撞点 |
|---|---|---|---|
| `e75G8KZl` | GLB/MINVOL1M | SLOW + `sqrt(w)` | self 0.7221 / prod 0.7208（各超 0.02） |
| `omEGwNwk` | GBR/TOP700 | CROWDING + `sqrt(w)` | self 0.7332 / prod 0.7333 |
| `d5Wz8KEJ` | KOR/TOP600 | **FAST** + `ts_mean(w,20)` | self 0.8209 / prod 0.8209 |
| `0mYg9ldr` | USA/TOP3000 | CROWDING + `rank(w)` | prod **0.7690**（S4.40/F5.42 白瞎） |
| `kqNGkWxd` | USA/TOP2000 | CROWDING + `ts_mean(w,20)` | 余量 0.0097 + ↔`Xg9WNRg8` 0.7419 同席 |
| `MPYzlkd6` | IND/TOP500 | SLOW + `sqrt(w)` | ↔`3qoG6nEe` **0.7837** 同席，prod 高 0.136 |
| `akKz2gmv` | DEU/TOP500 | SLOW + `sqrt(w)` | ↔`P0oM2P8L` **0.9901** 同席 |
| `VkxzqnEb` | USA/TOP1000 | SLOW + `rank(w)` | ↔`xAr1Y5gg` **0.9917** 同席（指标持平，self 略差） |
| `KPJzqnnz` | GLB/TOP3000 | CROWDING + `rank(w)` | 无撞（唯一 PASS 新席），但 TO 0.3711 + margin 0.000506 ⇒ 备胎 |

### 7.2 历史累积（不再重试）

`zscore(w)`（S −1.14，非负权重被中心化 ⇒ 一半反向下单）｜`combo_power` cp6+（2Y == limit 即 FAIL）｜`rank(w)^3`（Ladder FAIL）｜`reduce_avg` / `reduce_percentage(0.75)`（Ladder FAIL）｜selection 换 `prod_correlation` 排序（S 1.77→1.04）｜严格 selection（S −0.27）｜`in(classifications,"ATOM")`（IND S 4.45→3.21）｜`in()` 在 KOR 恒常数（互测 1.0000）｜`ts_ir` / `combo_a`（S 5.23/5.72 但 `LOW_SUB_UNIVERSE_SHARPE`）｜limit l12/l14 ｜decay d0/d5 ｜EUR 三空档 ｜MEA ｜USA TOP500/TOPSP500/TOP200 ｜GLB MINVOL1M FAST ｜IND FAST（0.6467）

---

## 八、平台 SA 算子清单与利用率审计

**官方《SuperAlpha Operators》附录**（`appendix-operators`，lastModified 2026-08-26）：
**162 个条目 → 去重后 161 个算子**，其中 **combo 可用 160**、**selection 可用 43**（`universe_size` 仅 selection）。
⚠ `get_operators` 返回的 103 个是 **REGULAR 全集**，不是 SA 全集 —— 两者不可混用。
⚠ 官方表**非穷尽**：`combo_a` 表外可用（已实测通过）。

### 8.1 利用率（48 颗 ACTIVE SUPER + 本轮 9 档）

| 维度 | 已用 | 覆盖率 |
|---|---|---|
| combo 算子 | **8**（`generate_stats`/`self_corr`/`if_else`/`equal`/`reduce_max`/`subtract`/`multiply`/`rank`） | 8/160 = **5.0%** |
| selection 算子 | **9**（`greater`/`multiply`/`subtract`/`add`/`less`/`sqrt`/`if_else`/`or`/`equal`） | 9/43 = **20.9%** |
| 全算子并集 | **14** | 14/161 = **8.7%**（本轮 8.1% → 8.7%，**仅新增 `ts_mean`**） |
| 未用算子 | **147** | — |

### 8.2 本轮 9 档的算子构成

- **骨架（强制，8 个）**：`generate_stats` → `self_corr` → `if_else` → `equal` → `reduce_max` → `subtract` → 赋值 → 收尾
- **形变（仅 3 个，占 combo 空间的 1.9%）**：`sqrt(w)` ×3 档 / `ts_mean(w,20)` ×2 档 / `rank(w)` ×3 档
- **selection（3 个）**：`subtract` / `multiply` / `equal`（`if_else(dataset_count==1,...)` 那档）

### 8.3 结论：**没有充分利用，且方向性错误**

1. **96% 的 combo 算子从未被使用**，且 48 颗 SA 的 combo 有 **44 颗是完全相同的骨架**，差异只在尾部 `w` 的幂次 —— 这是「一颗 alpha 换 48 次参数」而非 48 个设计。
2. 本轮补测的三个形变算子**全部无效**（见 §七）—— 说明**形变不是杠杆**。
3. 真正未被开发的是**语义型 combo 算子**（不是形变）：`combo_weight`（语义未摸底，P0）、`inst_pnl`/`inst_tvr`（组合层换手/收益归因）、`one_side`/`rank_by_side`（多空侧分离）、`left_tail`/`right_tail`/`tail`（组件尾部裁剪）、`filter`/`keep`（组件准入）、`group_*` 系列（按组件属性分组加权）。
4. **但**：本轮 9 档再次证明 **prod/self 由「席位」而非「配方」决定**（同档同族哪怕换 3 种形变仍撞 0.74–0.99）⇒ **继续深耕 combo 算子 ROI 极低**，更高 ROI 是**扩大组件池**（提交新 REGULAR，尤其 ASI 9→10、HKG 7→10，可直接开新档）与**等生产池漂移**。

---

## 九、执行清单

### 9.1 构建命令（复用，勿改脚本）

```bash
cd D:/coding/traeCN_project/wqb
# 新建 SA 批次（耐心轮询，勿用管道否则中断）
world-quant-brain-mcp/.venv/Scripts/python.exe \
  C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261107_r13/configs_v1.json \
  --out results/sa_scan_20261107_r13/res_v1.jsonl \
  --max-polls 70 --interval 10 > results/sa_scan_20261107_r13/run_v1.log 2>&1 &
```

configs 关键字段：`region/universe/delay/neutralization/decay/selection_limit/truncation/selection[/combo]`；
`combo` 省略时用标准骨架 `w^combo_power`；`selection_limit` **必须 ≥10**。

### 9.2 配额约束

- **SUPER = 账号级 1/ET 日**（跨区共享），REGULAR 4/天/区，两者独立计数。
- 被 prod 闸拦下**不消耗**配额；已提交不可撤回。
- 提 S 会同比抬高 `IS_LADDER` 门槛（`limit = max(1.58, 0.52×S)`），故排期优先「余量最厚」而非「S 最高」。

### 9.3 建议执行顺序

1. **Day 1 `3qoG6nEe`** — 提交前 `check_correlation(refresh=True)` 终验（台账 03:19 值 0.4708，余量 0.229 足以抗漂移）。
2. 之后按 §1.3 一天一颗；每颗提交前单独 `refresh=True`（prod 账号级单并发，遇 `correlation_busy` 隔 40s 重查，勿重派）。
3. `KPJzqnnz` 排在最后；若 `KPJzqnnz` 与 `1YNl3p5R` 同日，取 `1YNl3p5R`（TO 0.134 vs 0.3711、margin 高 2.6 倍）。
4. 若当日配额已被 REGULAR 任务占用，顺延，**不要并发**。
5. 提交后等满 ~250s flip 窗再 `status` 复核 `ACTIVE`，并复查 `tags`（平台会自动追加 `PowerPoolSelected`，需 `set_alpha_properties` 清回，须同传 descriptions）。

### 9.4 停止条件

- 7 颗队列全部提交完 ⇒ SA 线本轮产能耗尽；
- 若要继续，只有两条路：① **提交 REGULAR 把 ASI(9)/HKG(7) 推到 ≥10** 开新档；② 等生产池漂移使某颗 prod 回落（48h 复测一次）。

---

## 附录 A：本轮 9 档实测全表

| Tag | Alpha | 档位 | 形变 | S | F | TO | 2Y | margin | self | prod | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| glb_mv1m_slow_sqrtw | `e75G8KZl` | GLB/MINVOL1M SLOW | `sqrt(w)` | **6.82** | 3.71 | 0.3449 | 5.27 | 0.000592 | 0.7221 | 0.7208 | ✗ 双撞 |
| ind_t500_slow_sqrtw | `MPYzlkd6` | IND/TOP500 SLOW | `sqrt(w)` | 4.49 | 3.65 | 0.2776 | 4.18 | 0.001321 | 0.6070 | 0.6066 | ✗ 同席 0.7837 |
| gbr_t700_crowd_sqrtw | `omEGwNwk` | GBR/TOP700 CROWDING | `sqrt(w)` | 3.64 | 3.58 | 0.1543 | 3.18 | 0.001930 | 0.7332 | 0.7333 | ✗ 双撞 |
| kor_t600_fast_tsmean20 | `d5Wz8KEJ` | KOR/TOP600 **FAST** | `ts_mean(w,20)` | 4.30 | **5.05** | 0.1454 | 3.21 | 0.002756 | 0.8209 | 0.8209 | ✗ 双撞 |
| usa_t2000_crowd_tsmean20 | `kqNGkWxd` | USA/TOP2000 CROWDING | `ts_mean(w,20)` | 3.66 | 3.82 | 0.1415 | 4.18 | 0.002182 | 0.6903 | 0.6903 | ✗ 同席 0.7419 + 余量 0.010 |
| deu_t500_slow_sqrtw | `akKz2gmv` | DEU/TOP500 SLOW | `sqrt(w)` | 2.51 | 1.97 | 0.1638 | 4.01 | 0.001239 | 0.5840 | 0.5836 | ✗ 同席 0.9901 |
| usa_t3000_crowd_rankw | `0mYg9ldr` | USA/TOP3000 CROWDING | `rank(w)` | 4.40 | **5.42** | 0.0966 | 5.44 | 0.003930 | 0.6707 | **0.7690** | ✗ prod |
| usa_t1000_slow_rankw | `VkxzqnEb` | USA/TOP1000 SLOW | `rank(w)` | 2.83 | 2.09 | 0.1455 | 3.04 | 0.001090 | 0.3356 | **0.4729** | ✗ 同席 0.9917（等价备选） |
| glb_t3000_crowd_rankw | `KPJzqnnz` | GLB/TOP3000 CROWDING | `rank(w)` | 3.46 | 1.74 | 0.3711 | 2.63 | 0.000506 | 0.6623 | 0.6617 | ✅ **新独立席**（备胎） |

## 附录 B：本轮互测矩阵（节选，threshold 0.7）

| | `VkxzqnEb` | `xAr1Y5gg` | `1YNl3p5R` | `3qoG6nEe` | `KPJzqnnz` |
|---|---|---|---|---|---|
| `VkxzqnEb` | 1.00 | **0.9917** | 0.5680 | 0.0076 | 0.0714 |
| `xAr1Y5gg` | 0.9917 | 1.00 | 0.5606 | 0.0081 | 0.0727 |
| `1YNl3p5R` | 0.5680 | 0.5606 | 1.00 | 0.0769 | 0.1781 |
| `3qoG6nEe` | 0.0076 | 0.0081 | 0.0769 | 1.00 | 0.0141 |
| `KPJzqnnz` | 0.0714 | 0.0727 | 0.1781 | 0.0141 | 1.00 |

`akKz2gmv`↔`P0oM2P8L` **0.9901**｜`MPYzlkd6`↔`3qoG6nEe` **0.7837**｜`kqNGkWxd`↔`Xg9WNRg8` **0.7419**｜`kqNGkWxd`↔`e75avmq6` 0.3460｜`mLYLEm99`↔`P0oM2P8L` 0.5526。

## 附录 C：数据产物

| 文件 | 内容 |
|---|---|
| `results/sa_candidates_20261107-063310.json` | 组件池 + SUPER 全量（probe 输出；⚠ 该脚本 `--json` 会二次拼接 `results/`，传相对名即可，传 `results/...` 会变 `results/results/...` 并抛 FileNotFoundError） |
| `results/sa_scan_20261107_r13/slots_local.json` | 离线重建的 region×universe 档位表 + 48 颗 SA 配方 |
| `results/sa_scan_20261107_r13/configs_v1.json` / `configs_v2.json` | 本轮 6 + 3 档配方 |
| `results/sa_scan_20261107_r13/res_v1.jsonl` / `res_v2.jsonl` | 逐档结果（含 self/prod/fails） |
| `results/sa_scan_20261107_r13/op_audit_v3.json` | 算子利用率审计（161 官方 / 14 已用 / 147 未用） |
| `results/sa_scan_20261107_r13/run_v1.log` / `run_v2.log` | 构建日志（缓冲，靠 res 文件判进度） |
