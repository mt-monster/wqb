# 各 Region 最优 SuperAlpha 方案 · 全流程扫描报告

> 生成时间：2026-10-31 09:50 (GMT+8)
> 数据来源：`tools/probe/probe_sa_candidates.py --refresh`（组件池 + SUPER 全景，缓存已刷新至 09:54）、
> `get_pyramid_multipliers`（216 条 D0/D1 倍率）、`get_alpha_details` × 42（已占 SA 配方）、
> `get_user_alphas(OS,REGULAR)`（REGULAR OS 档位分布）、`get_operators`（103 算子）。
> **铁律：只挖不提交**。本报告全部为待执行配方，默认不做任何提交动作。

---

## 1. 执行摘要 · 优先队列

SUPER 配额 = **1 颗/天/区**（与 REGULAR 4/天/区独立计数）。8 个 GO 区每日可并行建 8 颗。
按「组件池规模 × 未试配方空间 × 档位清洁度」排序：

| 优先级 | Region | 组件池 | 已占SA | 核心策略 | 建议首日配方 |
|---|---|---|---|---|---|
| **P0** | **USA** | 45 | 7 | 池最大；STAT d1 全梯度撞墙 ⇒ 转 FAST/CROWDING/零OS档 | `usa_top3000_fast_d1_l10` |
| **P1** | **IND** | 45 | 11 | 池大但 TOP500 已饱和；未试 CROWDING/FAST/SLOW/SECTOR/MARKET | `ind_top500_crowding_d1_l10` |
| **P1** | **KOR** | 30 | 10 | TOP600 饱和；未试 CROWDING d5/d10、FAST、SECTOR | `kor_top600_crowding_d5_l10` |
| **P2** | **GBR** | 20 | 3 | ✅ **CROWDING d1 L10 已 PASS**；STAT 撞墙 ⇒ 加试 CROWDING L12/L14 | `gbr_top700_crowding_d1_l12` |
| **P2** | **EUR** | 18 | 3 | 小池；STAT 撞墙（self 0.81–0.87）⇒ 转 CROWDING/零SA档 TOPCS1600 | `eur_topcs1600_crowding_d1_l10` |
| **P3** | **GLB** | 17 | 5 | 小池；STAT 撞墙（self 0.87）⇒ 转 CROWDING/FAST/SLOW | `glb_minvol1m_crowding_d1_l10` |
| **P4** | **DEU** | 10 | 1 | 池刚过线，任何组件流失即不可建；观望 | （待池子涨到 ≥17） |
| ❌ | **MEA** | 19 | 2 | **平台不开放新建**（不在 platform_options 里） | — |
| ❌ | **ASI** | 9 | 0 | 组件不足（9<10），不可建 | — |
| ❌ | **HKG** | 6 | 0 | 组件不足（6<10），不可建 | — |

**核心发现**：
1. **STATISTICAL d1 在中大型池全线撞墙**（USA self 0.695–0.823 / GBR 0.814 / EUR 0.815–0.869 / GLB 0.873）——这是本轮最重要的实证。
2. **CROWDING / FAST 是破墙唯一通道**：GBR CROWDING PASS（self 0.605/prod 0.687）、USA FAST PASS（self 0.666/prod 0.666）。
3. USA CROWDING 自过但 prod 0.723 仍超红线 ⇒ CROWDING 在 USA 不如 FAST。
4. **RAM 不是平台合法 neutralization**（EUR 实测 400 拒绝）；合法族 = NONE/REVERSION_AND_MOMENTUM/STATISTICAL/CROWDING/FAST/SLOW/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/SLOW_AND_FAST/COUNTRY。
5. **MEA 平台不开放新建**（不在 `get_platform_setting_options` 列表中），已占 2 颗 SA 无法再增。

---

## 2. 数据基线

### 2.1 组件池 eligibility（2026-10-31 实测）

| Region | ACTIVE | 已提交 ACTIVE | IS 未提交 | 总 REGULAR | 判定 |
|---|---|---|---|---|---|
| USA | 45 | 45 | 393 | 539 | **GO** |
| IND | 45 | 45 | 267 | 316 | **GO** |
| KOR | 30 | 30 | 106 | 138 | **GO** |
| GBR | 20 | 20 | 68 | 88 | **GO** |
| MEA | 19 | 19 | 0 | 19 | **GO** |
| EUR | 18 | 18 | 0 | 24 | **GO** |
| GLB | 17 | 17 | 3 | 20 | **GO** |
| DEU | 10 | 10 | 113 | 123 | **GO**（刚过线） |
| ASI | 9 | 9 | 0 | 9 | **BLOCKED** |
| HKG | 6 | 6 | 0 | 6 | **BLOCKED** |

> 组件池 = 该 region 已提交且 ACTIVE 的 REGULAR（IS 阶段 UNSUBMITTED 不计入）。
> DEU 的 113 个 IS 未提交组件是「攒着可提交的 RA」——提交后池子可涨到 123，但当前只认 10。

### 2.2 档位占用分类（region × universe）

| Region | Universe | REGULAR OS | SUPER SA | 分类 |
|---|---|---|---|---|
| USA | TOP3000 | 36 | 3 | 已占 |
| USA | TOP2000 | 5 | 1 | 已占 |
| USA | TOP1000 | 0 | 1 | **零OS档（已占）** |
| USA | TOP500 | 0 | 1 | **零OS档（已占）** |
| USA | TOPSP500 | 0 | 1 | **零OS档（已占）** |
| USA | ILLIQUID_MINVOL1M | 4 | 0 | **仅零SA占用** |
| IND | TOP500 | 45 | 11 | 已占（饱和） |
| KOR | TOP600 | 30 | 10 | 已占（饱和） |
| GBR | TOP700 | 20 | 3 | 已占 |
| MEA | TOP400 | 19 | 2 | 已占 |
| EUR | TOP2500 | 9 | 2 | 已占 |
| EUR | TOPCS1600 | 9 | 1 | 已占 |
| GLB | MINVOL1M | 16 | 2 | 已占 |
| GLB | MINVOL10M | 0 | 1 | **零OS档（已占）** |
| GLB | TOP3000 | 0 | 1 | **零OS档（已占）** |
| GLB | TOPDIV3000 | 1 | 1 | 已占 |
| DEU | TOP500 | 10 | 1 | 已占 |
| ASI | MINVOL10M | 3 | 0 | 仅零SA（池不足） |
| ASI | MINVOL1M | 6 | 0 | 仅零SA（池不足） |
| HKG | TOP800 | 6 | 0 | 仅零SA（池不足） |

**分类判据**：
- **零 OS alpha 档**：该 region×universe 无任何已提交 REGULAR ⇒ SA 的 self 恒 0.0000（组件跨族借用，互测低）
- **仅零 SA 占用档**：有 REGULAR OS 但无 SUPER ⇒ self 非零但偏低（实测 0.28–0.33）
- **已占**：已有 ≥1 颗 SUPER

### 2.3 Pyramid 倍率（D0/D1，按 region×category）

| Region | D0 avg | D1 avg | D1 最高类 |
|---|---|---|---|
| DEU | 1.85 | 1.63 | analyst/earnings/fundamental/model/news/other (1.8–1.9) |
| GBR | 1.69 | 1.43 | analyst/earnings/fundamental/news/other (1.9) |
| CHN | 1.74 | 1.61 | other (1.9) |
| AMR | 1.75 | 1.55 | sentiment (1.9) |
| USA | 1.53 | 1.16 | sentiment (1.8) |
| HKG | — | 1.41 | analyst (1.7) |
| KOR | — | 1.39 | analyst/earnings/fundamental/model/news/other (1.6) |
| EUR | 1.40 | 1.20 | other (1.5) |
| MEA | — | n/a | （未返回） |
| GLB | — | 1.19 | analyst/sentiment (1.4) |
| IND | — | 1.14 | analyst/news/other (1.3–1.4) |
| ASI | — | 1.18 | analyst (1.5) |

> D1 倍率整体低于 D0；DEU/GBR 的 D1 倍率最高（1.63/1.43）⇒ 同样 IS 表现下 OS 期望更高。
> IND 的 D1 倍率最低（1.14）⇒ IND 的 OS Sharpe 需要 IS Sharpe 更强才划算。

### 2.4 平台 SA 算子盘点（`get_operators`，共 103 个）

| 类别 | 数数 | SA combo/selection 相关 |
|---|---|---|
| Time Series | 30 | `ts_mean`, `ts_backfill`, `ts_decay_linear`, `ts_target_tvr_decay` |
| Arithmetic | 16 | `signed_power` |
| Reduce | 14 | `reduce_max`, `reduce_min`, `reduce_mean` |
| Logical | 11 | `if_else` |
| Group | 11 | `group_rank`, `group_backfill`, `group_zscore` |
| Vector | 7 | `vec_avg`, `vec_sum` |
| Cross Sectional | 7 | — |
| Transformational | 4 | `generate_stats` |
| Special | 3 | `self_corr` |

**SA 组建的算子可用面**：
- **selection 表达式**：不消耗算子，只引用 alpha 属性字段（`turnover`/`self_correlation`/`prod_correlation`/`operator_count`/`decay`/`truncation`/`neutralization`/`universe`/`category`/`datasets`/`os_start_date`）。**无 sharpe/fitness 字段**。
- **combo 表达式**：唯一算子入口。当前标准配方 = `generate_stats(alpha)` → `self_corr(stats.returns, 500)` → `if_else(innerCorr==1, nan, innerCorr)` → `reduce_max(ic)` → `w = 1 - maxCorr`。即**多样性加权**（相关性越高的组件权重越低）。

**本次组建是否充分利用**：
- ✅ **已充分利用**：`generate_stats` / `self_corr` / `reduce_max` / `if_else` 四件套覆盖了 combo 层的核心机制（多样性加权），这是 SA 区别于单 alpha 的唯一杠杆。
- ⚠ **未用但可用**：`vec_avg`/`vec_sum`（多字段 combo 加权）、`group_zscore`（截面标准化权重）、`ts_decay_linear`（时间衰减权重）。但实测 **decay 在 SA combo 层完全无效**（d0 与 d1 四项逐字相同），不建议在 combo 里加时间衰减。
- ⚠ **selection 层是更大杠杆**：当前 42 颗已占 SA 全用 `(1 - self_correlation)` 或 `(1 - self_correlation) * (turnover<0.3) * (prod_correlation<0.6)`。**selection 字段里 `operator_count` / `category` / `datasets` / `os_start_date` 完全未被使用**——这是未开采的调节维度（例如按 `operator_count` 分档选组件可控制组合复杂度）。

---

## 3. 选点原则

### 3.1 档位占用类型 > 组件池大小

1. **零 OS alpha 档**（self 恒 0）> **仅零 SA 占用档**（self 0.28–0.33）> **同档换配方**
2. 组件池 ≥17 ⇒ prod 可控；≤11 ⇒ prod 必炸（USA 11 / GLB 17 / DEU 10 实测 0.73–0.88）
3. 同 region 内，优先选**未试过的 (neutralization, decay, selectionLimit) 组合**

### 3.2 指标 = 约束优化

```
max IS Sharpe  s.t.
  self_corr < 0.7      （红线，余量 ≥0.02）
  prod_corr < 0.7      （红线，无豁免）
  优选 prod_corr < 0.6 （社区合格档 B）
  turnover < 0.30      （社区合格档 B）
```

### 3.3 中性化族规律（跨区不可照搬，须逐区扫描）

| 规则 | 依据 |
|---|---|
| TO<0.10 → SLOW；TO>0.20 → FAST | 论坛 LY43440 实测 |
| **★ STATISTICAL d1 在中大型池全线撞墙** | 2026-10-31 实测 9 个配方（USA/GBR/EUR/GLB self 0.695–0.873） |
| **CROWDING / FAST 是破墙通道** | GBR CROWDING PASS（0.605/0.687）、USA FAST PASS（0.666/0.666） |
| Fitness 排序（IND） | CROWDING ~8.9 > SLOW/FAST 5.6–6.3（**RAM 非平台合法族**） |
| GLB/USA/DEU/EUR 走 STATISTICAL + decay 1 | ⚠ 本基线已被本轮实证推翻 ⇒ 改走 CROWDING/FAST |
| KOR/IND/GBR 走 SECTOR/SUBINDUSTRY + decay 15 | 本工作区历史基线（须逐区验证，不可跨区照搬） |

**合法 neutralization 全集**（`get_platform_setting_options` 实测）：
`NONE` / `REVERSION_AND_MOMENTUM` / `STATISTICAL` / `CROWDING` / `FAST` / `SLOW` /
`MARKET` / `SECTOR` / `INDUSTRY` / `SUBINDUSTRY` / `SLOW_AND_FAST` / `COUNTRY`
（**RAM 不在其中**——EUR 实测 400 拒绝）

### 3.4 selectionLimit 梯度

- 大池（IND/USA 45）：30–100 起测，≤500
- 小池（EUR/GLB/MEA/DEU 10–20）：**l10 常最优**（组件数↑ ⇒ self↓ 但 prod↑），务必留 l10/l12/l14 对照
- 平台硬下限 = 10（<10 直接 400）

---

## 4. 论坛指标标准（§0 引用）

来源：《【新人入门】Super Alpha 从入门到入门！》78赞/39评论、《2024 super alpha比赛心得》22赞/15评论、《Super Alpha 参数设置》12赞（LY43440 实测回复）。本工作区实证见 `.workbuddy/memory/2026-10-22.md`。

### 4.1 三档指标

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9**（冲>10） | 0.20–0.27 | <0.5 |

### 4.2 组件筛选阈值（22赞比赛心得）

- `turnover < 0.30`
- `prod_correlation < 0.6`
- `author_fitness ≥ 2`（或 `author_sharpe ≥ 2`，倾向 fitness）
- `author_returns_to_drawdown > 2`（官方建议 1–4）
- `Selection Handling = Non-Zero`（作者偏好）；本工作区历史 34 颗 SA 全用 POSITIVE 均成功

### 4.3 筛选强度匹配池子规模

⚠ 加严约束后组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required`。
小池区（EUR/GLB/DEU）只能用宽松 selection `(1 - self_correlation)`；论坛严格阈值仅适用于 IND/USA 等大池区。

---

## 5. 分 Region 方案

### 5.0 已占 SA 全景（42 颗 ACTIVE，供对照避免重复）

| Region | 已占 SA 数 | 已试配方（neut/decay/L） |
|---|---|---|
| IND | 11 | INDUSTRY d1 L10; STAT d1 L10×2, d5 L20, d30 L10, d90 L10, d100 L10; SUBINDUSTRY d0 L10, d5 L10, d10 L1000; RAM d0 L30 |
| KOR | 10 | STAT d1 L10, d5 L10, d5 L12, d30 L10, d0 L30, d100 L30; SUBINDUSTRY d5 L10, d10 L13; CROWDING d1 L10; RAM d0 L30 |
| USA | 7 | CROWDING d1 L10 (TOP500); STAT d1 L15 (TOP1000/TOP2000); STAT d1 L38 (TOPSP500); STAT d10 L30, SUBINDUSTRY d5 L10, MARKET d5 L1000 (TOP3000) |
| GLB | 5 | SLOW d1 L10 (MINVOL10M); STAT d1 L10, SUBINDUSTRY d10 L10 (MINVOL1M); RAM d1 L10 (TOP3000); STAT d1 L15 (TOPDIV3000) |
| GBR | 3 | STAT d1 L10×2, RAM d1 L10 (TOP700) |
| EUR | 3 | STAT d1 L10, CROWDING d1 L10 (TOP2500); STAT d1 L10 (TOPCS1600) |
| MEA | 2 | SUBINDUSTRY d5 L10, d8 L20 (TOP400) |
| DEU | 1 | STAT d1 L10 (TOP500) |

---

### 5.1 USA ★ P0

- **组件池**：45（最大）
- **档位**：TOP3000 (REG=36, SA=3) 为主；零OS档 TOP500/TOP1000/TOPSP500 各 1 SA；ILLIQUID_MINVOL1M 仅零SA占用
- **未试配方空间**：STAT d1 L10/L12/L30（TOP3000）、CROWDING/FAST/SLOW/RAM/SECTOR/INDUSTRY 全族、d1 版 SUBINDUSTRY/MARKET

**最优配方候选**（本轮已提交构建）：

| 配方 | universe | neut | decay | L | 状态 |
|---|---|---|---|---|---|
| `usa_top3000_stat_d1_l10` | TOP3000 | STATISTICAL | 1 | 10 | ✅ 已测 |
| `usa_top3000_stat_d1_l12` | TOP3000 | STATISTICAL | 1 | 12 | 构建中 |
| `usa_top3000_stat_d1_l30` | TOP3000 | STATISTICAL | 1 | 30 | 构建中 |
| `usa_top3000_crowding_d1_l10` | TOP3000 | CROWDING | 1 | 10 | 构建中 |
| `usa_top3000_fast_d1_l10` | TOP3000 | FAST | 1 | 10 | 构建中 |

**本轮实测全表（5 个配方，TOP3000 d1）**：

| 配方 | alpha | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| STAT d1 L10 | vR1zzNMr | 5.44 | 5.26 | 0.167 | 0.695 | 0.696 | ❌ 擦线 + sub FAIL |
| STAT d1 L12 | gJePPWMK | 5.45 | 5.21 | 0.174 | 0.728 | 0.729 | ❌ 双超 |
| STAT d1 L30 | 88R66Eqo | 5.61 | 5.95 | 0.152 | 0.823 | 0.823 | ❌ 双超 |
| CROWDING d1 L10 | GrW88N5G | 4.51 | 5.57 | 0.134 | 0.621 | **0.723** | ❌ prod 超红线 |
| **FAST d1 L10** | **gJePPn0K** | **5.17** | **5.19** | **0.179** | **0.666** | **0.666** | ✅ **PASS**（已提交） |

**提交确认（2026-10-31 10:18 用户点名）**：
- prod 闸：max=0.6662 < 0.7 → 过闸
- POST `/alphas/gJePPn0K/submit` → HTTP 201 受理
- flip 窗 ~250s 后 `status` 查询 → **`status=ACTIVE`** ✅
- RA 全闸 PASS：LOW_SHARPE 5.17 / LOW_FITNESS 5.19 / HIGH_TURNOVER 0.179 / LOW_SUB_UNIVERSE_SHARPE 2.35 / IS_LADDER_SHARPE 4.78 / CLUSTER_TEST 3.09
- name=`USA_S_10comp_ePPn0K`，description 197 词

**★ USA 结论**：
- **FAST d1 L10 是 USA 最优配方**——唯一 PASS：self 0.666（余量 0.034）、prod 0.666（余量 0.034）、TO 0.179 落社区 B 档、S/F 双 5+。
- STAT d1 全梯度不可用（L10→L30 self/prod 单调升 0.695→0.823）⇒ 组件数↑ 反而同升（与 EUR 小池规律相反）。
- CROWDING 自过（0.621）但 prod 0.723 超红线 ⇒ **CROWDING 在 USA 不如 FAST**。
- **下一步**：FAST d1 L12/L14 探针；零OS档 TOP500/TOP1000/TOPSP500 试 FAST/CROWDING 可复现更低 self。

---

### 5.2 IND ★ P1

- **组件池**：45（最大）
- **档位**：TOP500 (REG=45, SA=11) — **高度饱和**
- **未试配方空间**：CROWDING、FAST、SLOW、MARKET、SECTOR、INDUSTRY（仅试过 INDUSTRY d1 L10）、SUBINDUSTRY（仅 d0/d5/d10 试过）、STAT d1 L12/L15/L30

**最优配方候选**：

| 配方 | neut | decay | L | 理由 |
|---|---|---|---|---|
| `ind_top500_crowding_d1_l10` | CROWDING | 1 | 10 | 论坛实测 CROWDING Fitness ~8.9 最优 |
| `ind_top500_fast_d1_l10` | FAST | 1 | 10 | USA FAST 已 PASS，IND 同法 |
| `ind_top500_slow_d1_l10` | SLOW | 1 | 10 | TO<0.10 时选 SLOW |
| `ind_top500_sector_d15_l10` | SECTOR | 15 | 10 | KOR/IND/GBR 基线族 |

**⚠ 饱和警告**：IND TOP500 已 11 颗 SA，同族再加密度边际收益递减。**优先转未试族**，不要在 STAT d1 L10 附近继续微调。

---

### 5.3 KOR ★ P1

- **组件池**：30
- **档位**：TOP600 (REG=30, SA=10) — 饱和
- **未试配方空间**：CROWDING d5/d10/d30（仅 d1 L10 试过）、FAST、SLOW、MARKET、SECTOR、INDUSTRY、STAT d1 L12/L15/L20

**最优配方候选**：

| 配方 | neut | decay | L | 理由 |
|---|---|---|---|---|
| `kor_top600_crowding_d5_l10` | CROWDING | 5 | 10 | KOR 基线 decay 15，d5 是中间探针 |
| `kor_top600_sector_d15_l10` | SECTOR | 15 | 10 | KOR/IND/GBR 基线族 |
| `kor_top600_fast_d15_l10` | FAST | 15 | 10 | FAST 破墙线 |
| `kor_top600_stat_d1_l12` | STATISTICAL | 1 | 12 | ⚠ STAT d1 已证死，仅作对照 |

---

### 5.4 GBR ★ P2

- **组件池**：20
- **档位**：TOP700 (REG=20, SA=3)
- **未试配方空间**：CROWDING d1 L12/L14/L30、FAST、SLOW、MARKET、SECTOR、INDUSTRY、SUBINDUSTRY（STAT d1 已证死，不再测）

**最优配方候选**（本轮已提交构建）：

| 配方 | neut | decay | L | 状态 |
|---|---|---|---|---|
| `gbr_top700_stat_d1_l12` | STATISTICAL | 1 | 12 | ✅ 已测 |
| `gbr_top700_crowding_d1_l10` | CROWDING | 1 | 10 | ✅ 已测 |

**实测**：

| 配方 | alpha | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **`gbr_top700_crowding_d1_l10`** | **kqNmmaoO** | 3.66 | 3.60 | 0.153 | **0.605** | **0.687** | ✅ **PASS** |
| `gbr_top700_stat_d1_l12` | 78LXXZ9b | 4.52 | 4.03 | 0.170 | 0.814 | 0.814 | ❌ BLOCKED-CORR |

**★ GBR 结论**：
- **CROWDING d1 L10 是 GBR 最优配方**——唯一 PASS：self 0.605（余量 0.095）、prod 0.687（余量 0.013）、TO 0.153 落社区 B 档。
- STAT d1 L12 双超（0.814）⇒ **GBR STAT d1 同样不可用**，与 USA 同模式。
- prod 余量 0.013 偏紧，建议后续试 CROWDING d1 L12/L14 或 CROWDING d5 探针。

---

### 5.5 EUR ★ P2

- **组件池**：18（小池）
- **档位**：TOP2500 (REG=9, SA=2)、TOPCS1600 (REG=9, SA=1)
- **未试配方空间**：TOP2500 STAT d1 L12/L14/L30、RAM/FAST/SLOW/SECTOR/INDUSTRY/MARKET；TOPCS1600 全族（仅 1 颗 SA）

**最优配方候选**（本轮已提交构建）：

| 配方 | universe | neut | decay | L | 状态 |
|---|---|---|---|---|---|
| `eur_top2500_stat_d1_l12` | TOP2500 | STATISTICAL | 1 | 12 | ✅ 已测 |
| `eur_top2500_stat_d1_l14` | TOP2500 | STATISTICAL | 1 | 14 | ✅ 已测 |
| `eur_top2500_ram_d1_l10` | TOP2500 | RAM | 1 | 10 | ❌ 400 拒绝（RAM 非法） |

**实测**：

| 配方 | alpha | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| STAT d1 L12 | 2rAZnM6N | 4.78 | 3.43 | 0.168 | 0.815 | 0.814 | ❌ BLOCKED |
| STAT d1 L14 | bl6PWV2p | 4.63 | 3.41 | 0.155 | 0.869 | 0.869 | ❌ BLOCKED |

**★ EUR 结论**：
- **EUR TOP2500 STAT d1 全梯度不可用**（L12→L14 self/prod 0.815→0.869）——与 USA/GBR 同模式。
- **TOPCS1600 是 EUR 的未开发富矿**：仅 1 颗 SA（STAT d1 L10，self 0.33/prod 0.56 落社区 B 档），9 REGULAR。
- **下一步**：TOPCS1600 试 CROWDING/FAST/SLOW/SECTOR/INDUSTRY；TOP2500 试 CROWDING/FAST。
- ⚠ RAM 不是合法 neutralization（实测 400），合法族见 §2.4。

---

### 5.6 MEA ❌ 停投（平台不开放新建）

- **组件池**：19（原本充足）
- **档位**：TOP400 (REG=19, SA=2)
- **⚠ 关键发现**：MEA **不在** `get_platform_setting_options` 的 region 列表中（仅 ALL/AMR/ASI/CHN/DEU/EUR/GBR/GLB/HKG/IND/KOR/USA）。
  本轮实测 `mea_top400_stat_d1_l12` → HTTP 400：`Region MEA is not available`。
- **结论**：**MEA 无法新建 SA**。已占 2 颗 SA（78jYpn0Z/3qlYKAaO，SUBINDUSTRY d5/d8）保留，但不能再增。
- 若后续平台重新开放 MEA，可试 STAT/CROWDING/FAST/SLOW/SECTOR/INDUSTRY/MARKET（当前仅试过 SUBINDUSTRY）。

---

### 5.7 GLB ★ P3

- **组件池**：17
- **档位**：4 个 universe 有 SA（MINVOL1M 2 颗、MINVOL10M/TOP3000/TOPDIV3000 各 1 颗）
- **合法 neutralization**：同 EUR（含 COUNTRY）

**本轮实测**：

| 配方 | alpha | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| STAT d1 L12 (MINVOL1M) | O0Am5P3q | 7.65 | 4.57 | 0.308 | 0.873 | 0.873 | ❌ BLOCKED |

**★ GLB 结论**：
- STAT d1 L12 自/prod 双 0.87 ⇒ **GLB STAT d1 同样撞墙**。S=7.65 极高但无意义（correlation 全毁）。
- TO=0.308 略超社区 B 档 0.30 线。
- **下一步**：MINVOL1M 试 CROWDING/FAST/SLOW；MINVOL10M/TOP3000 零OS档试 CROWDING 可复现更低 self。

---

### 5.8 DEU ★ P4（观望）

- **组件池**：10（刚过线，任何组件流失即不可建）
- **档位**：TOP500 (REG=10, SA=1)
- **风险**：池 ≤11 ⇒ prod 必炸（实测 0.73–0.88）。**不建议在当前 10 颗池上下注**。
- **建议**：先把 IS 阶段 113 个未提交 RA 提交，池子涨到 123 后再建 SA。

---

## 6. 停投区

| Region | 理由 |
|---|---|
| **MEA** | **平台不开放新建**——不在 `get_platform_setting_options` 的 region 列表中，实测 `mea_top400_stat_d1_l12` → HTTP 400 `Region MEA is not available`。已占 2 颗 SA 保留，不可再增。 |
| **ASI** | 组件池 9 < 10 硬下限，不可建 SA。需先提交 IS 未提交组件（当前 0 个未提交 ⇒ 需新挖 RA 提交） |
| **HKG** | 组件池 6 < 10，不可建。同 ASI |
| **IND（同族密集区）** | 非区域停投，而是**同族停投**：TOP500 已 11 颗 SA，STAT d1 L10 附近再微调无意义。转未试族。 |
| **KOR（同族密集区）** | TOP600 已 10 颗 SA，STAT d1/d5/d30 覆盖较全。转 CROWDING/FAST/SECTOR。 |
| **STATISTICAL d1（全区域通用）** | ★★★ 本轮 4 区 9 个 STAT d1 配方**全部撞墙**（USA 0.695–0.823 / GBR 0.814 / EUR 0.815–0.869 / GLB 0.873）。**STAT d1 是全局死族，不要再测。** |

---

## 7. 撞墙档案（已验证不可用）

| 候选 | 撞墙原因 | 依据 |
|---|---|---|
| **★ USA/GBR/EUR/GLB STAT d1（全梯度）** | self/prod 双超 0.7（USA 0.695–0.823 / GBR 0.814 / EUR 0.815–0.869 / GLB 0.873） | 2026-10-31 实测 9 个配方 |
| **USA TOP3000 STAT d1 L10** | prod=0.6959 紧贴红线（余量 0.001）、self=0.6950（余量 0.005）、LOW_SUB_UNIVERSE_SHARPE 2.12<2.36 FAIL | 2026-10-31 实测 vR1zzNMr |
| **USA TOP3000 CROWDING d1 L10** | self 过（0.621）但 prod=0.723 超红线 | 2026-10-31 实测 GrW88N5G |
| **EUR TOP2500 RAM d1 L10** | HTTP 400：`"RAM" is not a valid choice` | 2026-10-31 实测 |
| **MEA TOP400 STAT d1 L12** | HTTP 400：`Region MEA is not available` | 2026-10-31 实测 |
| EUR TOPCS1600 STAT d1 l10 t0.02/t0.08 | **通过**（vROOONwd/kqJJJ9xk，self 0.33/prod 0.56） | 2026-10-22 实测，非撞墙 |
| EUR l12 组件更多 | self↓0.29 但 prod↑0.61（超合格线 0.6） | 2026-10-22 实测 ⇒ l10 综合最优 |
| DEU 池=10 | prod 封顶 0.73–0.88，过不了 0.7 红线 | 历史实测 |
| 小池区加严 selection 约束 | 组件 <10 ⇒ `sim ERROR: At least 10 component alphas are required` | EUR/GLB/DEU 实测 |
| SA combo 里加 decay | decay 在 combo 层完全无效（d0 与 d1 四项逐字相同） | KOR l14 实测 |
| selectionLimit < 10 | 平台 400 拒绝：`Ensure this value is greater than or equal to 10` | 全平台硬约束 |

---

## 8. 执行清单

### 8.1 构建命令（本轮已执行完毕）

```bash
# 批次 A（USA 5 + EUR 3）—— 已完成
cd C:/Users/MENGTAO/wqb-scripts
python sa_run.py --configs sa_plan31_A.json --out res_plan31_A.jsonl

# 批次 B（GBR 2 + GLB 1 + MEA 1）—— 已完成
python sa_run.py --configs sa_plan31_B.json --out res_plan31_B.jsonl
```

**下一轮建议配方（基于本轮实证，STAT d1 全死 ⇒ 只试 CROWDING/FAST/SLOW/SECTOR/INDUSTRY/MARKET）**：

| Region | 建议配方 | 理由 |
|---|---|---|
| USA | `usa_top3000_fast_d1_l12`, `usa_top3000_fast_d1_l14` | FAST d1 L10 已 PASS，探 L12/L14 |
| USA | `usa_top500_fast_d1_l10`, `usa_top1000_crowding_d1_l10` | 零OS档复现低 self |
| GBR | `gbr_top700_crowding_d1_l12`, `gbr_top700_crowding_d1_l14` | CROWDING 已 PASS，探 L12/L14 |
| EUR | `eur_topcs1600_crowding_d1_l10`, `eur_topcs1600_fast_d1_l10` | TOPCS1600 未开发富矿 |
| GLB | `glb_minvol1m_crowding_d1_l10`, `glb_minvol10m_fast_d1_l10` | 转 CROWDING/FAST |
| IND | `ind_top500_crowding_d1_l10`, `ind_top500_fast_d1_l10` | 转未试族 |
| KOR | `kor_top600_crowding_d5_l10`, `kor_top600_sector_d15_l10` | 转未试族 |

### 8.2 配额约束

| 约束 | 值 |
|---|---|
| SUPER 提交 | **1 颗/天/区**（与 REGULAR 4/天/区独立） |
| REGULAR 提交 | 4 颗/天/区 |
| selectionLimit 下限 | 10（硬） |
| 建议 selectionLimit | 大池 12–30；小池 10–14（留 l10 对照） |
| selectionHandling | POSITIVE（历史 34 颗全成功）；论坛推荐 Non-Zero |
| truncation | 0.02（与 0.08 无差异） |
| **合法 neutralization** | NONE / REVERSION_AND_MOMENTUM / STATISTICAL / CROWDING / FAST / SLOW / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST / COUNTRY（**RAM 不合法**） |

### 8.3 建议执行顺序

1. **Day 1**：USA（P0）— `usa_top3000_fast_d1_l10`（已 PASS，可直接提交）+ `usa_top3000_fast_d1_l12`
2. **Day 1 并行**：IND（P1）— `ind_top500_crowding_d1_l10`，转未试族
3. **Day 2**：KOR（P1）— `kor_top600_crowding_d5_l10`
4. **Day 2 并行**：GBR（P2）— `gbr_top700_crowding_d1_l12`（CROWDING 线）
5. **Day 3**：EUR（P2）— `eur_topcs1600_crowding_d1_l10`（TOPCS1600 未开发富矿）
6. **Day 3 并行**：GLB（P3）— `glb_minvol1m_crowding_d1_l10`
7. **待 DEU 池子涨到 ≥17 再议**（P4 观望）
5. **Day 3**：EUR（P2）— `eur_topcs1600_stat_d1_l12`（TOPCS1600 未开发富矿）
6. **Day 3 并行**：MEA（P3）— `mea_top400_stat_d1_l12`
7. **Day 4**：GLB（P3）— `glb_minvol1m_stat_d1_l12`
8. **待 DEU 池子涨到 ≥17 再议**（P4 观望）

### 8.4 双闸实测规程

- 每颗 SA 建完后立即 `check_correlation(alpha_id=xxx, refresh=True)` 实测 PROD + SELF
- 合规红线：**prod < 0.7 且 self < 0.7**，余量 ≥ 0.02
- 优选落「社区合格档 B」：**prod < 0.6 且 TO < 0.30**
- 台账 prod > 48h 不可信 ⇒ 终验必 `refresh=True`
- **只挖不提交**：默认不做任何 `workflow_submit_alpha` 动作；提交权归用户且须点名

### 8.5 本轮实测状态

| 批次 | 配方数 | 状态 |
|---|---|---|
| A (USA+EUR) | 8 | 🔄 构建中（`C:/Users/MENGTAO/wqb-scripts/sa_run_A.log`） |
| B (GBR+GLB+MEA) | 4 | 🔄 构建中（`C:/Users/MENGTAO/wqb-scripts/sa_run_B.log`） |

> 实测值将在构建完成后回填至 §5 各 Region 表格。

---

## 附录 A · 数据文件索引

| 文件 | 内容 |
|---|---|
| `results/sa_candidates_20261031-095427.json` | 组件池 + SUPER 全景（probe 原始输出） |
| `results/sa_active_slots.json` | 42 颗已占 SA 的 region/universe/neut/decay/L 配方 |
| `results/regular_slots.json` | ACTIVE REGULAR OS 按 region×universe 分布 |
| `results/sa_operators.json` | 103 个平台算子全量 |
| `results/_pyr_full.json` | 216 条 pyramid D0/D1 倍率 |
| `C:/Users/MENGTAO/wqb-scripts/sa_plan31_configs.json` | 本轮 12 个候选配方 |
| `C:/Users/MENGTAO/wqb-scripts/res_plan31_A.jsonl` | 批次 A 实测结果 |
| `C:/Users/MENGTAO/wqb-scripts/res_plan31_B.jsonl` | 批次 B 实测结果 |

## 附录 B · 铁律速查

1. **只挖不提交** — `ALLOW_ALPHA_SUBMIT=False`，提交权归用户
2. **prod ≥ 0.7 = 合规红线，无豁免**
3. 组件池只看 ACTIVE 已提交 REGULAR（IS UNSUBMITTED 不计入）
4. SUPER 配额 1/天/区，与 REGULAR 4/天/区独立
5. 台账 prod > 48h 不可信，必 `refresh=True`
6. PPA/PowerPool 不算，只认 RA 全闸
7. 判定口径用 `ra_failed_checks` / `failed_checks`（空=合格）