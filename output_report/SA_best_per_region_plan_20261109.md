# 各 Region 最优 SuperAlpha 方案（2026-11-09）

> 执行时刻：2026-11-09 06:30–07:20（GMT+8）｜工作区 `D:\coding\traeCN_project\wqb`
> 铁律：**只挖不提交**。本文全部为待执行配方与判死结论，提交权归用户；`ALLOW_ALPHA_SUBMIT=False` 闸锁保持。
> 数据时点：组件池 / 档位 / pyramid 全部本轮平台实测（`probe_sa_candidates --refresh`，2026-11-09T06:31，已先清 `api_cache.user_alphas%`）。
> 双闸值全部 `check_correlation(refresh=True)` 实测，非台账。

---

## 一、执行摘要

**本轮 0 颗可交付。** 扫描 7 颗存量候选 + 新建 2 档，全部卡在 `prod` 一侧，且**卡点同源**：不是平台他人拥挤，是**本账户自己已提交的 SUPER**。

### 1.1 四条本轮新结论

| # | 结论 | 证据（本轮实测） |
|---|---|---|
| ★1 | **SA prod 已成「自我拥挤」结构**：prod 最大值 = 与自己已提交 SUPER 的相关，而非第三方池 | `58EKWYGz` prod 0.7701 ≡ self 0.7701，top1 = **`vR1oxZA3`**（我们 11-08 提交的 DEU FAST）；`0mYak1nv` 0.6918 ≡ self 0.6920 vs `vR1oxZA3`；`bl6K2Oor` 0.6953 ≡ 0.6955 vs `vR1oxZA3` —— 三颗独立验证 |
| ★2 | **同档换中性化族不是新席**：同 `(region, universe, limit)` 下五族互相 0.69–0.77 | DEU/TOP500 l10 全族谱：FAST(已交) / CROWDING 0.6918 / SLOW 0.6953 / SECTOR 0.7701 / MARKET 0.7708 |
| ★3 | **SA 层族越粗 ⇒ prod 越高**（与 REGULAR 层 group 轴规律**反向**） | 细族 CROWDING/SLOW 0.69 < 粗族 SECTOR/MARKET 0.77；而粗族 F 更高（3.33/3.29 vs 3.11/2.32）⇒ **F 高 ≠ prod 干净** |
| ★4 | **提交一颗即毒死同档全部兄弟，且是 48h 内立即生效** | `vR1oxZA3` 11-08 22:48 提交前，`0mYak1nv`/`bl6K2Oor` 为 0.5165/0.4619；提交后 **+0.175 / +0.233** 顶到 0.6918/0.6953 |

### 1.2 优先队列（按可执行性排序）

| # | 对象 | 槽位 | 配方 | S | F | TO | prod | self | 余量(prod) | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `LLM2qe2M` | USA/TOP2000 | SECTOR d1 l10 cp3 | 3.73 | 4.02 | 0.1333 | **0.6957** | 0.6007 | **0.0043** | ⚠ 唯一贴线候选，余量 < 0.02 **不建议** |
| 2 | **产能路径 A** | HKG | 提交 **3 颗** HKG REGULAR（7→10） | — | — | — | — | **首颗 self=0** | — | 🟢 最高 ROI（pyramid D1 1.413） |
| 3 | **产能路径 B** | ASI | 提交 **1 颗** ASI REGULAR（9→10） | — | — | — | — | **首颗 self=0** | — | 🟢 次高 ROI（D1 1.181） |

> 队列第 1 项是「备选」不是「推荐」：0.0043 余量在 48h 漂移下必翻。按既有纪律（prod 余量 < 0.02 一律不交付）本轮**无可执行提交**。
> 队列 2/3 是**唯一能真正开新席的路径**，见 §5.2。

---

## 二、数据基线

### 2.1 组件池 eligibility（口径：ACTIVE + 已提交 REGULAR，IS 阶段不计入）

| Region | eligible | Δ vs 11-08 | 本地库 universe 分布 | verdict |
|---|---|---|---|---|
| USA | 47 | 0 | TOP3000 38 / TOP2000 5 / ILLIQUID_MINVOL1M 4（非法档） | GO |
| IND | 47 | 0 | TOP500 47 | GO |
| KOR | 34 | 0 | TOP600 34 | GO |
| GBR | **27** | **+3** | TOP700 27 | GO |
| EUR | 23 | 0 | TOP2500 13 / TOPCS1600 10 | GO |
| MEA | 19 | 0 | TOP400 19 | GO（**平台已下架**） |
| GLB | 18 | 0 | MINVOL1M 17 / TOPDIV3000 1 | GO |
| DEU | **16** | **+2** | TOP500 16 | GO |
| ASI | 9 | 0 | MINVOL1M 6 / MINVOL10M 3 | BLOCKED（差 1） |
| HKG | 7 | 0 | TOP800 7 | BLOCKED（差 3） |
| CHN | 0 | 0 | — | BLOCKED（差 10） |

> 池子增长（GBR +3 / DEU +2）**未转成任何产能**：GBR 三档实测 0.6867–0.6980，DEU 两新族 0.77 —— 池增长的边际收益已被自我拥挤吃掉。

### 2.2 档位占用分类（50 颗 ACTIVE SUPER）

| Region | Universe | SUPER | REGULAR | 已占族 | 档位类型 |
|---|---|---|---|---|---|
| USA | TOP3000 | 6 | 38 | STAT×2、SLOW、MARKET(l1000)、SUBIND、FAST | 🔴 饱和 |
| USA | TOP2000 | 1 | 5 | STATISTICAL(l15) | 🔴 已占（SECTOR 贴墙 0.6957） |
| USA | TOP1000 | 1 | 0 | STATISTICAL(l15) | 🔴 已占 |
| USA | TOP500 | 1 | 0 | CROWDING(l10) | 🔴 封档 |
| USA | TOPSP500 | 1 | 0 | STATISTICAL(l38) | 🔴 封档 |
| USA | TOP200 | 0 | 0 | — | ⚪ 零 OS（IS 不可达 S≤1.28） |
| IND | TOP500 | 12 | 47 | STAT×5、SUBIND×2、INDUSTRY、SLOW、RAM 等 | 🔴 饱和 |
| KOR | TOP600 | 11 | 34 | STAT×3、SUBIND×2、CROWDING、SLOW、RAM | 🔴 饱和 |
| GBR | TOP700 | 5 | 27 | STAT×2、FAST、RAM、SLOW | 🔴 饱和（本轮三测 0.687–0.698） |
| DEU | TOP500 | 2 | 16 | STATISTICAL、FAST | 🔴 **本轮封档**（余 3 族 0.69–0.77） |
| EUR | TOP2500 | 2 | 13 | CROWDING、STATISTICAL | 🔴 已占 |
| EUR | TOPCS1600 | 1 | 10 | STATISTICAL | 🔴 已占 |
| EUR | TOP1200 / TOP800 / TOP400 | 0 | 0 | — | ⚪ 零 SA（结构性 prod 墙 0.71–0.78，4 次确认） |
| GLB | MINVOL1M | 2 | 17 | STATISTICAL、SUBINDUSTRY | 🔴 已占 |
| GLB | MINVOL10M | 1 | 0 | SLOW | 🔴 已占 |
| GLB | TOP3000 | 1 | 0 | RAM | 🔴 已占 |
| GLB | TOPDIV3000 | 1 | 1 | STATISTICAL(l15) | 🔴 已占 |
| HKG | TOP800 / TOP500 | 0 | 7 | — | ⚪ **零 SA（池差 3）** |
| ASI | MINVOL1M / MINVOL10M / TOP500 | 0 | 9 | — | ⚪ **零 SA（池差 1）** |
| MEA | TOP400 | 2 | 19 | SUBINDUSTRY | ⛔ 区域已下架 |
| CHN / AMR | TOP2000U / TOP600 | 0 | 0 | — | ⛔ 无组件（池 0） |

**ACTIVE SUPER 50 分布**：IND 12 / KOR 11 / USA 10 / GBR 5 / GLB 5 / EUR 3 / DEU 2 / MEA 2。

### 2.3 pyramid 倍率（本轮拉取，D0 / D1 均值）

| Region | D0 均值 | **D1 均值** | D1 峰值 | 可建 SA？ |
|---|---|---|---|---|
| **DEU** | 1.850 | **1.613** | 1.8 | 封档（5 族全撞） |
| **CHN** | — | **1.608** | 1.9 | ⛔ 池 0 |
| AMR | 1.750 | 1.550 | 1.7 | ⛔ 池 0 |
| **HKG** | — | **1.413** | 1.7 | ⚪ **池 7/10 ⇒ 差 3 颗** |
| **GBR** | 1.679 | **1.413** | 1.7 | 封档 |
| KOR | — | 1.387 | 1.6 | 饱和 |
| EUR | 1.408 | 1.207 | 1.5 | prod 墙 |
| **ASI** | — | **1.181** | 1.5 | ⚪ **池 9/10 ⇒ 差 1 颗** |
| GLB | — | 1.177 | 1.4 | 饱和 |
| USA | 1.533 | 1.171 | 1.4 | 基本饱和 |
| IND | — | 1.140 | 1.4 | 饱和 |

> 解读：**DEU 依然是全账户价值最高的 SA 区（D1 1.613），但已封档**。下一个高价值未开发区是 **HKG（1.413，与 GBR 并列）**和 **CHN（1.608，成本最高）**——两者都没有 SURPER 占用，首颗 self 恒 0。

---

## 三、选点原则（本轮修订）

1. **档位占用类型 > 组件池大小**。池 27 的 GBR 全部贴墙，池 16 的 DEU 曾经全过 —— 决定成败的是「该档是否已有自己的 SA」，不是池多大。
2. **指标口径 = 约束优化**：`max S ∧ max F  s.t.  self<0.7 ∧ prod<0.7`（优选 `prod<0.6`），且**余量 ≥ 0.02**。本轮全部候选的失败点都在 prod，不在 S/F。
3. **中性化族不是席**（本轮新增，推翻 11-08 的「三空族=三席」）：同 `(region, universe, limit)` 下换族只改外权重，与已提交 SA 的相关仍在 0.69–0.77。**族的真实用途是调 S/F，不是开席**。
4. **族粗细分层（SA 层专用）**：
   - 追 **prod 干净** ⇒ 细族 `CROWDING` / `SLOW`（0.69）
   - 追 **S/F 高** ⇒ 粗族 `SECTOR` / `MARKET`（F 3.33/3.29），但 prod 0.77 必死
   - `FAST` 居中（0.5987 提交时），是 DEU 唯一成功过闸的族
5. **prod 是动态的、且主要被自己推动**：同档提交一颗，其余兄弟 48h 内上浮 +0.17~0.23。**同族只留一颗时先交余量大的**（这条在 DEU 已被反例验证：先交 FAST 余量 0.101，把余量 0.238 的 SLOW 顶死）。
6. **新席只有两条路**：新 universe（平台已无）或**新 region 的池子过 10**。

---

## 四、论坛指标标准（固化，本轮沿用不再调研）

来源：《【新人入门】Super Alpha 从入门到入门！》78 赞 / 39 评、《2024 super alpha比赛心得》22 赞 / 15 评、《Super Alpha 参数设置》12 赞（含 LY43440 实测）。

### 4.1 指标三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9**（冲 >10） | 0.20–0.27 | <0.5 |

> 本轮最好候选 `LLM2qe2M`（S3.73/F4.02/TO0.1333）落在 **A 档**，prod 0.6957 已进 B 档红线区。账户 C 档存量仍以 `A1V0eZne`（S6.39/F7.06）与 `LL5amzov`（S6.93/F4.18）为顶。

### 4.2 组成数量

- 平台硬下限 **10**（<10 直接 400）；论坛建议 30–100 起测、≤500。
- **实际生效数 = min(limit, 组件池)**；本轮 l10 仍是甜点（l12/l14 在多区已证推高 prod）。
- ⚠ 组件池是 **region 级 + delay 级**（`USA/TOP500 d0` 池为 0 ⇒ 跨 delay 借池是伪命题）。

### 4.3 组件筛选阈值

`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ **筛选强度必须匹配池子规模**：加严后组件 <10 ⇒ `At least 10 component alphas are required`。小池区（EUR/GLB/DEU）只能用宽松 `(1 - self_correlation)`。

### 4.4 中性化族规律

- Fitness 排序（IND 实测）：CROWDING ~8.9 > RAM 6.9–8.5 > SLOW/FAST 5.6–6.3。
- 选族规则（REGULAR 层）：TO<0.10 → SLOW；TO>0.20 → FAST。
- 区域基线：GLB/USA/DEU/EUR 走 STATISTICAL + decay 1；KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15（须逐区扫）。
- **SA 层修正（本轮）**：族越粗 prod 越高（见 §1.1 ★3）；`decay` 在 SA 组合层完全无效。

### 4.5 其他实证

- truncation 0.02 vs 0.08 对 SA 几乎无差异（S 3.74 vs 3.73）。
- `Selection Handling` 论坛推荐 Non-Zero；本工作区 50 颗全部 POSITIVE，无一被拒 ⇒ 非闸门项。
- `combo_power` 是唯一「不动 prod」的纯增益杠杆（cp1→cp5 S/F 单调微增），上限由 IS Ladder 决定（cp6 已死）。

---

## 五、分 Region 方案

### 5.1 已占档：换配方空间已耗尽（逐区实测）

| Region | 本轮实测 | 结果 | 结论 |
|---|---|---|---|
| **DEU** / TOP500 | `0mYak1nv` CROWDING l10 | prod 0.6918 / self 0.6920 | ❌ 余量 0.008 |
| | `bl6K2Oor` SLOW l10 | prod 0.6953 / self 0.6955 | ❌ 余量 0.005 |
| | `58EKWYGz` **SECTOR** l10（新建） | S2.81/F3.33/TO0.1201；prod **0.7701** | ❌ FAIL |
| | `JjeaK2mA` **MARKET** l10（新建） | S2.77/F3.29/TO0.1195；prod **0.7708** | ❌ FAIL |
| **GBR** / TOP700 | `N1N2WRXo` SUBIND l10 | prod 0.6867 / self 0.6766 | ❌ 余量 0.013 |
| | `vR1oxrld`（族未记）l10 | prod 0.6980 / self 0.6976 | ❌ 余量 0.002 |
| **USA** / TOP2000 | `LLM2qe2M` SECTOR l10 cp3 | prod **0.6957** / self 0.6007 | ⚠ 余量 0.0043（唯一 <0.7 的贴线项） |
| | `E56208rR` SECTOR l10 | prod **0.7032** | ❌ FAIL |
| **EUR** | `QPvoroQM` l10 | S2.20 / F1.19 | ❌ IS 先死 |

> **DEU 全族谱（5 族）**：FAST 0.5987（已提交）→ CROWDING 0.6918 → SLOW 0.6953 → SECTOR 0.7701 → MARKET 0.7708。
> ⇒ DEU/TOP500+l10 **封档**，无第六族可试。

### 5.2 唯一可开新席的两条路径（本轮核心交付）

| 路径 | 现状 | 需要动作 | 解锁后 | 价值 |
|---|---|---|---|---|
| **HKG** | 7 ACTIVE REGULAR / 0 SUPER | 提交 **3 颗** HKG REGULAR（`TOP800`） | 3 个零 SA 档（TOP800 7 颗池 + TOP500 零池）可建；**首颗 self = 0.0000** | pyramid D1 **1.413**（并列 GBR，全账户第 4） |
| **ASI** | 9 ACTIVE REGULAR / 0 SUPER | 提交 **1 颗** ASI REGULAR | MINVOL1M(6)/MINVOL10M(3)/TOP500 三档可建；**首颗 self = 0.0000** | pyramid D1 1.181 |
| （CHN） | 0 ACTIVE REGULAR | 提交 10 颗 | 首颗 self = 0，pyramid **1.608**（全账户第 2） | 成本最高，长期目标 |

> 说明：`self=0` 只保证 self 闸，**不保证 prod**（USA/TOP500 经验：零 OS 档 self 0.0000 但 prod 0.6530）。但零 SA 区意味着该区没有任何自己的 SA 进入生产池，prod 只由 REGULAR 与第三方决定 ⇒ 是唯一有余量的方向。

### 5.3 已死档（不再投入）

| 档位 | 死因 |
|---|---|
| EUR/TOP1200 · TOP800 · TOP400 | 结构性 prod 墙（0.7117 / 0.7337 / 0.7783 / 0.7342，4 次独立确认）；三档用的已是 CROWDING 最优族 ⇒ 无族可救 |
| USA/TOP200 | IS 不可达：STAT l30 S1.28、CROWDING l10 S0.95、l30 S1.28（=STAT），2Y Ladder 0.30 |
| USA/TOPSP500 | 反向：S 1.83 过 IS 但 prod 0.6906；换族/换 cp 均无效 |
| KOR/TOP600 | 11 颗 SUPER 饱和，FAST 族 0.8209，l14 0.935 |
| IND/TOP500 | 12 颗 SUPER 饱和，self/prod 双 0.72+ |
| MEA/TOP400 | 平台下架（`Region MEA is not available`） |
| CHN/TOP2000U · AMR/TOP600 | 无组件（池 0） |

---

## 六、停投区（更新）

**全区停投**：MEA（下架）· EUR（prod 墙）· IND（饱和）· KOR（饱和）· DEU（本轮封档）· GBR（三测全贴墙）
**分档停投**：USA-TOP3000 / TOP2000（SECTOR 0.6957 贴线）/ TOP500 / TOPSP500 / TOP200
**池不足**：ASI（9，差 1）· HKG（7，差 3）· CHN（0，差 10）
**唯一保留动作**：HKG / ASI 的 REGULAR 池补足 + 提交后首次建 SA（见 §5.2）

---

## 七、撞墙档案（本轮新增 7 条）

| # | 槽位 | 配方 | 撞墙读数 | 性质 |
|---|---|---|---|---|
| 1 | DEU/TOP500 | CROWDING d1 l10 | prod 0.6918 / self 0.6920（原 0.5165/0.4899） | **兄弟提交后上浮 +0.175** |
| 2 | DEU/TOP500 | SLOW d1 l10 | prod 0.6953 / self 0.6955（原 0.4619/0.4622） | **兄弟提交后上浮 +0.233** |
| 3 | DEU/TOP500 | **SECTOR** d1 l10 | prod 0.7701（IS 8/8 全 PASS，F 3.33 全场最高） | 粗族 prod 最脏 |
| 4 | DEU/TOP500 | **MARKET** d1 l10 | prod 0.7708（IS 8/8 全 PASS，F 3.29） | 粗族 prod 最脏 |
| 5 | GBR/TOP700 | SUBINDUSTRY l10 | prod 0.6867 / self 0.6766 | 池 +3 无改善 |
| 6 | GBR/TOP700 | l10 | prod 0.6980 / self 0.6976 | 贴墙 0.002 |
| 7 | USA/TOP2000 | SECTOR l10 | prod 0.7032 FAIL | 过线 |

**历史累计**（不再复测）：EUR 全域 / USA-TOP200·TOP500·TOPSP500·TOP3000 / IND / KOR / GLB / MEA / `combo_power≥6` / `decay` 轴 / `zscore(w)` / `rank(w)` / `sqrt(w)` / `ts_mean(w,20)` / `reduce_avg` / `reduce_percentage` / 严格 selection（加 `prod_correlation` 项）。

---

## 八、算子利用率审计（本轮要求项）

### 8.1 平台可用算子全景

官方《SuperAlpha Operators》附录（`page_id=appendix-operators`，2026-08-26 更新）：

| 类别 | 可用数 | 说明 |
|---|---|---|
| **COMBO 列** | **160** | 含时序全家族（`ts_*` 57 个）、`group_*` 18 个、`reduce_*` 13 个、向量算子 6 个 |
| **SELECTION 列** | **43** | 仅标量算子 + `universe_size`（唯一 selection 专属） |
| 两者交集 | ~40 | 只有基础代数 / 比较 / 条件 / 符号类可进 selection |

关键不对称：**时序类（`ts_*`）、分组类（`group_*`）、`rank`、`quantile`、`winsorize`、`normalize`、`scale` 全部只能进 COMBO，不能进 SELECTION** —— 这是 selection 侧长期只能用 `(1 - self_correlation)` 这类简单式的根本原因，不是我们没试。

### 8.2 本工作区实际用量

| 侧 | 已用 | 可用 | 利用率 | 用到的算子 |
|---|---|---|---|---|
| COMBO | **14** | 160 | **8.8%** | `generate_stats` `self_corr` `if_else` `reduce_max` `subtract` `multiply`（`w*w*w`）`rank` `sqrt` `ts_mean` `zscore` `reduce_avg` `reduce_percentage` `combo_weight`(=w) `nan` |
| SELECTION | **6** | 43 | **14.0%** | `subtract` `multiply` `add` `greater` `less` `equal`（+ 内置 `in`） |

**本轮新增算子 = 0**：本轮两个新建档走的是中性化轴（SECTOR / MARKET），不属于算子轴；combo / selection 表达式与默认模板逐字相同。

### 8.3 高价值未测算子（按 ROI 排序，均未在 SA 侧验证过）

| 优先级 | 算子 | 为什么值得试 | 风险 |
|---|---|---|---|
| P0 | `combo_weight`（作为独立入口而非 `w`） | 平台唯一 combo 权重原语，语义未摸清；可能支持按成分属性加权（非仅 `1-maxCorr`） | 需先做语义探针 |
| P1 | `one_side` / `rank_by_side` / `position_safeguard` | 直接作用在「多空两侧」上，可能改 TO 与 sub-universe 短板 | 可能只是 TO 抑制，F 反向 |
| P2 | `inst_pnl` / `inst_tvr` | 成分级 PnL/换手，可做「按成分质量加权」的新 combo 形态 | 计算慢，可能超时 |
| P3 | `hump` / `hump_decay` | TO 压缩器，B 档（TO<0.30）已达，收益有限 | 低 |
| P4 | `universe_size`（selection 侧） | 唯一 selection 专属算子，可做「小宇宙降权」 | 单区 universe 固定 ⇒ 常数，无方差 |

> ⚠ 但**算子轴已证 ROI 极低**：7 轮迭代里 combo 形变（`sqrt`/`ts_mean`/`rank`/`zscore`/幂次/reduce 系）无一产生可交付新席，全部撞同档兄弟。**本轮结论：先修池（§5.2），不要继续在算子轴上投入。**

---

## 九、执行清单

### 9.1 若用户要点名提交（本文不推荐任何一颗）

```bash
cd D:/coding/traeCN_project/wqb
# 提交前必须先停掉任何后台 sa_run / 批量构建，避免 prod 单并发冲突
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id <ID> --region <REGION>
# 等满 ~250s flip 窗后再复核
world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py status --alpha-id <ID>
```
- prod 闸 0.7 fail-closed，无豁免参数。
- 若选 `LLM2qe2M`：0.6957 距线仅 0.0043，**必须 refresh=True 复测**；一旦 >0.7 即失败。

### 9.2 推荐动作（产能路径，非提交 SA）

| 顺序 | 动作 | 目的 | 之前工作 |
|---|---|---|---|
| 1 | HKG 挖 3 颗 REGULAR 并提交 | HKG 池 7→10，SA 解锁（D1 1.413） | `wq-brain-ra-hkg` skill |
| 2 | HKG 首颗 SA（TOP800，SLOW/CROWDING l10） | self=0 的新席 | 池到位后 1 档试建 |
| 3 | ASI 挖 1 颗 REGULAR 并提交 | ASI 池 9→10，SA 解锁 | ASI 有 94 颗 IS 存量可挑 |
| 4 | ASI 首颗 SA（MINVOL1M，l10） | self=0 的新席 | 同上 |

### 9.3 配额与并发约束（不变）

- SUPER **1/天/区**，与 REGULAR 4/天/区独立计数。
- **并发仿真上限 = 2**（第 3 路必 429 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED`）。
- prod 检查**账号级单并发**：遇 `correlation_busy` 按 `retry_after` 隔时重查，**不要重新触发**。
- 台账 prod > 48h 不可信，交付前必 `refresh=True`。
- 单档 SA 仿真 ~5–8 min（本轮 2 档并行 5 分钟完成）。

### 9.4 本轮数据产物

| 文件 | 内容 |
|---|---|
| `results/sa_plan_20261109.json` | 池盘点（10 区 eligibility + 59 颗 SA 明细） |
| `results/sa_scan_20261109/slots_local.json` | 离线档位表（26 个 region×universe） |
| `results/sa_scan_20261109/slot_scan_local.py` | 档位重建脚本（可复用） |
| `results/sa_scan_20261109/res_deu_t500_sector.json` / `_market.json` | 本轮两个新建档 |
| `results/sa_scan_20261109/op_audit.py` / `op_audit.json` | 算子审计 |
| `results/sa_scan_20261109/probe_refresh.log` | 池刷新日志 |

---

## 附录 A：本轮双闸实测明细（全部 `refresh=True`）

| Alpha | 槽位 | 配方 | S | F | TO | prod | self | 判定 |
|---|---|---|---|---|---|---|---|---|
| `0mYak1nv` | DEU/TOP500 | CROWDING d1 l10 cp1 | 2.86 | 3.11 | 0.1229 | 0.6918 | 0.6920 | ❌ 余 0.008 |
| `bl6K2Oor` | DEU/TOP500 | SLOW d1 l10 cp1 | 2.66 | 2.32 | 0.1462 | 0.6953 | 0.6955 | ❌ 余 0.005 |
| `58EKWYGz` | DEU/TOP500 | **SECTOR** d1 l10 cp1 | 2.81 | **3.33** | 0.1201 | 0.7701 | 0.7701 | ❌ FAIL |
| `JjeaK2mA` | DEU/TOP500 | **MARKET** d1 l10 cp1 | 2.77 | 3.29 | 0.1195 | 0.7708 | — | ❌ FAIL |
| `N1N2WRXo` | GBR/TOP700 | SUBINDUSTRY d1 l10 cp1 | 3.49 | 3.25 | 0.1578 | 0.6867 | 0.6766 | ❌ 余 0.013 |
| `vR1oxrld` | GBR/TOP700 | l10 | 3.47 | 3.20 | — | 0.6980 | 0.6976 | ❌ 余 0.002 |
| `LLM2qe2M` | USA/TOP2000 | SECTOR d1 l10 cp3 | 3.73 | 4.02 | 0.1333 | 0.6957 | 0.6007 | ⚠ 余 0.0043 |
| `E56208rR` | USA/TOP2000 | SECTOR d1 l10 | 3.69 | 3.85 | — | 0.7032 | — | ❌ FAIL |

新建两档 IS 闸（8/8 PASS）：

| Alpha | S | F | TO | LOW_SHARPE | LOW_FIT | SUB_UNIV | IS_LADDER | CLUSTER |
|---|---|---|---|---|---|---|---|---|
| `58EKWYGz` | 2.81 | 3.33 | 0.1201 | 2.81/1.58 | 3.33/1.0 | 1.89/1.33 | 3.09/2.02 | 2.13/1 |
| `JjeaK2mA` | 2.77 | 3.29 | 0.1195 | 2.77/1.58 | 3.29/1.0 | 1.88/1.31 | 3.06/2.02 | 2.10/1 |

## 附录 B：判定说明

- `prod` 与 `self` 本轮出现 **逐位重合**（0.6918/0.6920、0.6953/0.6955、0.7701/0.7701），且 top1 均为自有 SA。这条把 §8 的「self 只跟已提交池比」与「prod 只跟生产池比」两个口径**并到一起**：本账户自有 SA 同时是两者的最大项。
- 由此推论：**在本账户已提交 50 颗 SA 的前提下，任何落入已占档的新 SA，其 prod 下限 ≈ 与最近兄弟的相关（0.69–0.77）**。这就是「SA 线全域饱和」的量化解释，也是 §5.2 必须走新 region 的原因。
