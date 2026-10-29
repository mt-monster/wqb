# 各 Region 最优 SuperAlpha 方案 — 2026-10-28 夜间全流程扫描

生成时间：2026-10-28 01:30–03:40 (GMT+8)　|　扫描目录：`results/sa_scan_20261028/`
铁律：**只挖不提交**（全部为待执行配方）；**prod ≥ 0.7 = 合规红线，无豁免**；prod 值一律 `refresh=True` 实测。

---

## 0. 执行摘要（按价值排序）

| 优先级 | α id | Region / 档位 | 配方 | Sharpe | Fitness | TO | prod | self | 余量(prod/self) | fails |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| **P0 ★NEW** | `E567rQvR` | **USA / TOP500** | CROWDING d1 l10 **combo=`rank(w)`** | **1.82** | **1.41** | 0.1489 | **0.6360** | 0.0000 | **0.064 / 0.700** | **无** |
| ~~P1~~ | `78LAAm92` | USA / TOP500 | CROWDING d1 l10 cp5 | 1.79 | 1.32 | 0.1575 | 0.6530 | 0.0000 | 0.047 / 0.700 | 无（**已作废**） |
| ~~P2~~ | `78LAAZx1` | USA / TOP500 | CROWDING d1 l10 cp4 | 1.78 | 1.30 | 0.1589 | 0.6530 | 0.0000 | 0.047 / 0.700 | 无（**已作废**） |
| ~~P3~~ | `P0MRkP0M` | USA / TOP500 | CROWDING d1 l10 cp3 | 1.77 | 1.29 | 0.1606 | 0.6530 | 0.0000 | 0.047 / 0.700 | 无（**已作废**） |
| ~~P4~~ | `LL5rpRY2` | USA / TOP500 | CROWDING d1 l10 cp1 | 1.74 | 1.25 | 0.1647 | 0.6530 | 0.0000 | 0.047 / 0.700 | 无（**已作废**） |

**本轮唯一方法论突破**：combo 里把权重从 `w^power`（幂次整形）换成 **`rank(w)`（秩整形）** —— 首次实现 **IS 与 prod 同时改善**（S 1.79→1.82、F 1.32→1.41、TO 0.1575→0.1489、prod 0.6530→**0.6360**）。此前所有杠杆（换族 / limit / decay / combo_power）都只在 IS 一动、prod 一动之间二选一。

- **三面边界已实测封闭**：幂次叠加（`rank(w)^3` S1.58 Ladder FAIL）、limit 加大（`rank(w)`+l12 S1.70 FAIL）、聚合族替换（`reduce_avg` 1.67 / `reduce_percentage` 1.70 FAIL）全为负向 ⇒ `rank(w)`@l10 是局部最优，不是中间点。
> **✅ 已提交（用户 02:10 点名）**：`E567rQvR` 走 `super_build.py submit`，prod 闸实测 0.636 过闸 → POST 201 → **status=ACTIVE**，name `USA_S_10comp_67rQvR`。
> ⇒ **USA/TOP500 已封档**，P1–P4 四颗同档候选作废；SA 线全域无 ZERO-OS 空档，下一轮只能等平台新增 universe 或已有档换配方。

- 六颗候选互斥，**同档只出 1 席**。
- 全局只剩 ~~USA/TOP500 一个可交付档~~（**已于 02:15 提交并 ACTIVE，见下方**）；其余区域要么饱和、要么 prod 墙、要么池不足（见 §4）。
- 已提交 SUPER 仍 **39** 颗（最近 10-26 `LLMVPag1` GLB）⇒ 用户自 10-26 起未再提交，`LL5rpRY2`/`P0MRkP0M`/`78LAAZx1`/`78LAAm92`/`E567rQvR` 全部 UNSUBMITTED。

---

## 1. 数据基线

### 1.1 组件池 eligibility（口径：stage=OS + type=REGULAR + status=ACTIVE）

| Region | 池 | universe 分布 | 可建 | Δ vs 10-27 |
|---|---:|---|---|---|
| USA | **50** | TOP3000:38 / TOP2000:6 / ILLIQUID_MINVOL1M:4 / TOP1000:1 / TOPSP500:1 | ✅ | 持平 |
| IND | 53 | TOP500:53 | ✅ | 持平 |
| KOR | 39 | TOP600:39 | ✅ | 持平 |
| GBR | 20 | TOP700:20 | ✅ | 持平 |
| GLB | 21 | MINVOL1M:17 / TOPDIV3000:2 / MINVOL10M:1 / TOP3000:1 | ✅ | 持平 |
| EUR | 19 | TOPCS1600:10 / TOP2500:9 | ✅ | **+1** |
| DEU | 11 | TOP500:11 | ✅ | 持平 |
| MEA | 21 | TOP400:21 | ❌ 平台下架 | — |
| ASI | 9 | MINVOL1M:6 / MINVOL10M:3 | ❌ <10 | — |
| HKG | 6 | TOP800:6 | ❌ <10 | — |
| CHN/JPN/TWN/AMR | 0 | — | ❌ | — |

> ⚠ 组件池 **region 级但按 (region, delay) 双键**：USA 50 颗全为 d1，故 `USA/TOP500 d0` 直接 400。

### 1.2 档位占用分类（ACTIVE OS SUPER = 39）

| 类别 | 档位 | 说明 |
|---|---|---|
| **ZERO-OS**（self ≡ 0.0000） | **USA/TOP200**、**USA/TOP500**、EUR/TOP1200、EUR/TOP400、EUR/TOP800、ASI/TOP500、HKG/TOP500 | 该档无任何已提交 alpha |
| ZERO-SA（self 低但非 0） | ASI/MINVOL1M、ASI/MINVOL10M、HKG/TOP800 | 池均 <10，不可建 |
| OCCUPIED | IND/TOP500(11)、KOR/TOP600(9)、USA/TOP3000(3)、GLB/MINVOL1M(2)、EUR/TOP2500(2)、GBR/TOP700(2)、MEA/TOP400(2)、USA/TOP1000、USA/TOP2000、USA/TOPSP500、GLB/MINVOL10M、GLB/TOP3000、GLB/TOPDIV3000、EUR/TOPCS1600、DEU/TOP500 | 同档再建 self≈1 |

**结论**：可建且价值 > 0 的档只剩 **USA/TOP500**（ZERO-OS + prod 健康）。USA/TOP200 本轮实测判死（§5）。

### 1.3 Pyramid 倍率（`get_pyramid_multipliers`，216 条）

| Region | D1 区间 | D0 是否可用 | 备注 |
|---|---|---|---|
| DEU | 1.2–1.8 | ✅ 1.8–1.9 | 全平台最高 |
| GBR / HKG | 1.0–1.7 | GBR ✅ 1.3–1.9 | — |
| KOR | 1.0–1.6 | ❌ | — |
| EUR | 1.0–1.5 | ✅ 1.2–1.7 | — |
| ASI / IND / GLB / USA | 1.0–1.4 / 1.5 | 仅 USA ✅ (1.0–1.8) | USA D0 倍率最高（sentiment 1.8）但 d0 池 = 0 |

---

## 2. 选点原则（本轮实证更新）

1. **档位占用类型 > 组件池大小**：ZERO-OS ⇒ self 恒 0；OCCUPIED ⇒ 同族 self≈1（KOR l40 实测 0.9872/0.9871）。池子增长（EUR +1）若落在已饱和档，对产能零贡献。
2. **指标 = 约束优化**：`max IS  s.t. self < 0.7 且 prod < 0.7`，优选 prod < 0.6（社区合格档）。
3. **中性化族规律**：CROWDING 是 USA/TOP500 的 IS 最优族（同档 CROWDING 1.74 > FAST 1.63 > SLOW 1.35）；但 **GLB/MINVOL10M 反例**（SLOW 0.560 < STAT 0.639 < CROWDING 0.698 < INDUSTRY 0.748）⇒ 族不可跨区照搬。EUR 三零档本来就用 CROWDING 仍全撞 prod ⇒ 无族可救。
4. **combo 整形 > combo 幂次**（本轮新增）：`rank(w)` 同时抬 IS 与降 prod；`w^power` 只抬 IS、prod 纹丝不动。
5. **selection 排序变量必须还是 `self_correlation`**：换成 `prod_correlation` 排序 IS 崩塌（§5 W1）。
6. **limit↑ = 双刃**：self↑ / prod↑ / Ladder 易 FAIL。l10 仍是可交付甜点。
7. **decay 在 SA 组合层无效**（d0 与 d1 四项逐字相同），不必再扫。

---

## 3. 论坛指标标准（2026-10-22 定稿，沿用）

### 3.1 三档

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| A 平台底线 | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| B 社区合格档 | — | — | **<0.30** | **<0.6** |
| C 比赛/优秀档 | **5.6–7.0** | **5.6–8.9** | 0.20–0.27 | <0.5 |

### 3.2 组成数量
平台硬下限 **10**；论坛建议 30–100 起测、≤500；**实际生效 = min(limit, 组件池)**。

### 3.3 组件筛选阈值
`turnover<0.3` × `prod_corr<0.6` × `author_fitness≥2`（或 `author_sharpe≥2`）；`author_returns_to_drawdown>2`。
⚠ **筛选强度必须匹配池子规模**：小池区（EUR/GLB/DEU）只能用宽松 `(1 - self_correlation)`；USA 实测严格 selection 是**负杠杆**（S 1.74→1.47）。
⚠ **本轮新增否定**：把排序量从 `self_correlation` 换成 `prod_correlation` 也是负杠杆且更剧烈（S 1.77→**1.04**）。

### 3.4 其他
truncation 0.02 vs 0.08 几乎无差异；`Selection Handling = POSITIVE`（本工作区 39 颗 SA 全用，无一失败）。

---

## 4. 分 Region 方案

### 4.1 USA / TOP500 — 唯一可交付档（P0）

- 档位性质：**ZERO-OS**（0 REGULAR、0 SUPER）⇒ **self 恒 0.0000**；组件池 50（全 d1）。
- 基准配方：`CROWDING` / `delay 1` / `decay 1` / `selectionLimit 10` / `truncation 0.02` / `selectionHandling POSITIVE` / selection `(1 + 0*(prod_correlation>0)) * (1 - self_correlation)`。

**combo 谱系对照（本轮核心实验）**

| combo 尾部 | α id | Sharpe | Fitness | TO | prod | 2Y Ladder | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| `w`（cp1） | `LL5rpRY2` | 1.74 | 1.25 | 0.1647 | 0.6530 | pass | PASS |
| `w*w*w`（cp3） | `P0MRkP0M` | 1.77 | 1.29 | 0.1606 | 0.6530 | pass | PASS |
| `w^4`（cp4） | `78LAAZx1` | 1.78 | 1.30 | 0.1589 | 0.6530 | pass | PASS（本轮复测） |
| `w^5`（cp5） | `78LAAm92` | 1.79 | 1.32 | 0.1575 | **0.6530**（本轮首测） | pass | PASS |
| `w^6`（cp6） | `N1NwwYq7` | 1.79 | 1.33 | 0.1562 | — | **1.58==1.58 FAIL** | FAIL |
| **`rank(w)`** | **`E567rQvR`** | **1.82** | **1.41** | **0.1489** | **0.6360** | pass | **★最佳** |
| `1 - reduce_avg(ic)` | `WjOqWGNG` | 1.67 | 1.17 | 0.1679 | — | 1.54 FAIL | FAIL |
| `1 - reduce_percentage(ic,0.75)` | `LLMjl2kM` | 1.70 | 1.20 | 0.1673 | — | 1.56 FAIL | FAIL |
| `rank(w)^3`（幂次叠加） | `Xg9r299a` | 1.58 | 1.11 | 0.1665 | — | FAIL | **幂次与秩整形互斥** |
| `rank(w)` + l12 | `vR1qeoMz` | 1.70 | 1.27 | 0.1588 | — | FAIL | 秩整形救不了 l12 |

**推荐交付**：`E567rQvR`（combo=`rank(w)`）—— IS 全过 + **prod 0.6360（本轮两次独立 `refresh=True` 实测一致，余量 0.064）** + self 0.0000（余量 0.700）。距社区 B 档（prod<0.6）差 0.036，是当前体系里 USA 线最优。
**提交前必做**：再走一次 `check_correlation(refresh=True)`（铁律，台账 >48h 即不可信），并确认当日 SUPER 配额（1/ET 日/区）。

#### 4.1.1 秩整形的两个边界（v18 实测）

| 变体 | α id | S / F / TO | 结果 |
|---|---|---|---|
| `r = rank(w); r*r*r`（幂次叠加在秩之后） | `Xg9r299a` | 1.58 / 1.11 / 0.1665 | **IS_LADDER FAIL** —— 幂次与秩整形**互斥**：`rank(w)` 已把权重压到秩空间，再乘幂只会重新拉开离散度并击穿 Ladder。 |
| `rank(w)` + `selectionLimit 12` | `vR1qeoMz` | 1.70 / 1.27 / 0.1588 | **IS_LADDER FAIL** —— 秩整形救不了 limit，l10 仍是唯一甜点。 |

⇒ **`rank(w)` @ l10 / 无幂次 = 该档局部最优**：三面（幂次叠加、limit 加大、聚合族替换）均已证为负向，`E567rQvR` 是当前可达边界。

### 4.2 USA / TOP200 — 本轮判死

| 配方 | S / F / TO | 结论 |
|---|---|---|
| STAT l40 / l50（10-25） | 1.12 / 0.51 / 0.2220 | 两档逐字相同，S 不可达 |
| STAT l30（10-24） | 1.28 | 仍 FAIL |
| **CROWDING cp3 l10（本轮）** | **0.95 / 0.55 / 0.1696** | 比 STAT 更差 |
| **CROWDING cp3 l30（本轮）** | **1.28 / 0.88 / 0.1739** | 与 STAT l30 同值 ⇒ 换族救不了 |

⇒ **USA/TOP200 永久停投**：CROWDING 在 TOP500 的 +0.20 S 救赎未能在 TOP200 复现，窄 universe 的 S 天花板与中性化族无关。

### 4.3 EUR — prod 墙（停投）

| 档位 | 配方 | S / F / TO | prod | 状态 |
|---|---|---|---:|---|
| TOP1200 | CROWDING d1 l10 | 2.06 / 1.47 / 0.1627 | 0.7337 | 过 IS，prod 超标 |
| TOP800 | CROWDING d1 l10 | 1.40 / 0.81 / 0.1726 | 0.7117 | IS 亦不过 |
| TOP400 | CROWDING d1 l10 | 1.23 / 0.67 / 0.1827 | 0.7783 | IS 亦不过 |
| TOPCS1600（已占） | `gJWdxLbM` | — | 0.6988→**0.7666**（48h 漂移 +0.068） | 漂移实证 |
| TOP2500（已占） | `kqJOQgnk` 已 10-23 提交 | S3.92/F3.40 | 0.6546 | 封档 |

三个零占用档本就用本区 prod 最优族 CROWDING ⇒ **全域停投**。

### 4.4 GLB / IND / KOR / DEU / GBR — 档位饱和（停投）

| Region | 唯一/全部 universe | SUPER 占位 | 池 | 历史最佳 | 状态 |
|---|---|---:|---:|---|---|
| GLB | MINVOL1M / MINVOL10M / TOP3000 / TOPDIV3000 | 1+2+1+1 | 21 | `LL5amzov` S6.93/F4.18；`LLMVPag1` S4.25/F2.19 prod 0.5599（10-26 已提交） | 四档全占，停投 |
| IND | TOP500 | 11 | 53 | S5.43/F5.74 | 饱和；CROWDING l10 self/prod 双 0.7733 |
| KOR | TOP600 | 9 | 39 | S4.98/F5.94 | 饱和；l14 self 0.935 |
| GBR | TOP700 | 2 | 20 | S3.44/F2.99 | 严格 selection 组件 <10 |
| DEU | TOP500 | 1 | 11 | S2.27/F1.67 | 池仅 11；prod 0.764 |

### 4.5 MEA / ASI / HKG / CHN / JPN / TWN / AMR — 不可建

- **MEA**：平台 `Region MEA is not available.`（新建 400，CROWDING 亦不可用）；历史 2 颗仍 ACTIVE。
- **ASI(9) / HKG(6)**：低于平台硬下限 10。
- **CHN / JPN / TWN / AMR**：池 = 0。

---

## 5. 撞墙档案（累计，★=本轮新增）

| # | 区域 / 档位 | 配方 | 现象 | 结论 |
|---|---|---|---|---|
| ★W1 | USA/TOP500 | selection `(0.7 - prod_correlation)` 排序 | **S 1.04 / F 0.59** | **排序量换 prod = 毁灭性负杠杆** |
| ★W2 | USA/TOP500 | combo `reduce_avg` | S1.67，2Y 1.54 FAIL | 均值聚合劣于最大值聚合 |
| ★W3 | USA/TOP500 | combo `reduce_percentage(ic,0.75)` | S1.70，2Y 1.56 FAIL | 分位聚合亦劣 |
| ★W4 | USA/TOP200 | CROWDING cp3 l10 | S0.95/F0.55 | 窄 universe 换族无效 |
| ★W5 | USA/TOP200 | CROWDING cp3 l30 | S1.28/F0.88（=STAT l30） | TOP200 S 天花板 = 1.28 |
| ★W6 | USA/TOP500 | `rank(w)^3` | S1.58/F1.11，Ladder FAIL | 幂次与秩整形互斥 |
| ★W7 | USA/TOP500 | `rank(w)` + l12 | S1.70/F1.27，Ladder FAIL | 秩整形救不了 limit |
| N1 | USA/TOP500 d0 | CROWDING d0 | 400 `At least 10 component` | d0 池=0，delay 不可换 |
| N2 | USA/TOP500 cp6 | `w^6` | IS_LADDER 1.58==1.58 | combo_power 上限 = 5 |
| N3 | USA/TOP500 l12 | cp1 l12 | Ladder FAIL | l10 甜点 |
| N4 | USA/TOP500 strict | `(1-self)*(TO<0.3)*(prod<0.6)` | S 1.74→1.47 | 论坛严格阈值在 USA 为负 |
| N6 | USA/TOPSP500 | CROWDING/SECTOR/MARKET/SUBIND | 0.625–0.748，已被 `2rj3ddl5` 占 | 同族 self 0.987，封档 |
| N8 | EUR/TOP1200·800·400 | CROWDING l10 | 0.734/0.712/0.778 | 全域 prod 墙 |
| N9–10 | GLB/MINVOL10M | INDUSTRY 0.748 / MARKET 0.762 / CROWDING l12 0.698 | 余量 ≤0.02 | 仅 SLOW 可用（已提交） |
| N11 | KOR/TOP600 | CROWDING l14 | self 0.935 | 组件↑⇒self↑ |
| N12 | IND/TOP500 | CROWDING l10 | self/prod 双 0.7733 | 双撞 |
| N14 | MEA 全区 | 任意 | 400 区域下架 | 平台侧 |

---

## 6. ★ 平台 SA 算子清单与利用率审计（本轮新增专题）

来源：平台官方文档 `Selection expression`（selection 变量/算子）与 `SuperAlpha Operators`（Selection / Combo 可用算子矩阵）。

### 6.1 规模

| 类别 | 数量 | 说明 |
|---|---:|---|
| Selection / Combo **通用算子** | **42** | abs、add、and、arc_*、ceiling、clamp、divide、equal、exp、floor、frac、greater、if_else、inverse、is_nan 系、less、log、max、min、multiply、nan_mask、nan_out、negate、not、or、power、purify、reverse、round、s_log_1p、sigmoid、sign、signed_power、sqrt、subtract、tanh、to_nan … |
| **仅 Combo 可用** | **105** | generate_stats、self_corr、reduce_* 全族、group_* 全族、ts_* 全族、vector_neut/proj、trade_when、hump、rank、quantile、zscore、winsorize、scale、normalize、one_side、pasteurize、position_safeguard、inst_pnl、convert、**combo_weight**、bucket、densify、filter、keep、tail、kth_element … |
| **仅 Selection 可用** | **1** | `universe_size(universe)` |
| Selection **可用变量** | **25 + 18** | Alpha 属性 25 个（turnover / self_correlation / prod_correlation / long_count / short_count / decay / truncation / neutralization / universe / category / color / dataset(s) / datafields / dataset_count / datacategories / datacategory_count / datafield_count / operator_count / favorite / name / tags / os_start_date / classifications / competitions）+ **author_\* 18 个** |

### 6.2 本次组建实际用到的

| 层 | 已用 | 未用 |
|---|---|---|
| selection 变量 | `self_correlation`、`prod_correlation`（含 no-op 门 `(1+0*(prod>0))`）、`turnover`（仅 strict 变体，已证负） | 其余 22 个 Alpha 属性 + **全部 18 个 `author_*`** |
| selection 算子 | `*` `+` `>`（multiply / add / greater） | `universe_size`、比较与逻辑族、if_else、power、signed_power 等 39 个 |
| combo 算子 | `generate_stats`、`self_corr`、`reduce_max`、`if_else`、`rank`（本轮新增）、`*`（幂次） | **约 100 个**，含 combo_weight、reduce_avg/ir/stddev/percentage/min/count、group_*、ts_*、trade_when、hump、quantile、zscore、winsorize、vector_neut、one_side、inst_pnl … |

**利用率**：combo 侧 6/105 ≈ **6%**；selection 变量 3/25 ≈ **12%**（若计 author_* 则 3/43 ≈ 7%）。

### 6.3 为什么多数算子"用不上"——以及哪些真该试

1. **`author_*` 18 个在自有池里是常数**（同一作者 = 我），对本工作区的 selection 无区分力 ⇒ 论坛的 `author_fitness≥2` 只对"跨作者/比赛池"有意义，**本工作区该阈值不可消费**。
2. **`universe_size` 只在 selection 可用**：USA/TOP500 组件全在 TOP3000 等有限几档，区分度低；但在 USA（6 个 universe 有组件）理论上可做"偏好宽/窄 universe 成分"，属**未测轴**。
3. **combo 里真正有杠杆的两族已部分测过**：
   - 聚合族 `reduce_*`：**最大值最优**（reduce_max 1.74 > reduce_percentage(0.75) 1.70 > reduce_avg 1.67）；
   - 整形族：`rank(w)` **> `w^5` > `w^1`**；但**整形与幂次不可叠加**（`rank(w)^3` S1.58 < `rank(w)` 1.82），`reduce_*` 与整形的组合同样劣化。
   - **仍未测**：`combo_weight`（平台专为 combo 提供的权重算子）、`zscore(w)`、`quantile(w,…)`、`winsorize(w,…)`、`one_side`、`trade_when`、`group_*`/`ts_*` 在权重向量上的投影（`vector_neut`）、`hump` 对权重的时间整形。
4. **下一轮优先算子实验（按性价比）**：
   ① `zscore(w)`（与 rank 同族不同范化）　② `combo_weight` 语义摸底　③ `rank(w)` × l12/l14（秩整形能否放宽 limit）　④ `winsorize(rank(w), …)` + `signed_power(rank(w), 3)`（论坛禁用偶数幂）　⑤ selection 侧 `universe_size(universe)` 偏好项。

---

## 7. 执行清单

### 7.1 复现命令

```bash
cd /d/coding/traeCN_project/wqb
PY=world-quant-brain-mcp/.venv/Scripts/python.exe

# ① 组件池 + 档位 + pyramid（先清 api_cache，否则吃到 7 天旧数据）
$PY results/sa_scan_20261028/refresh_pool.py     # 内含 DELETE FROM api_cache WHERE cache_key LIKE '%user_alphas%'
$PY results/sa_scan_20261028/fetch_super.py      # SUPER 必须 alpha_type="SUPER" 单独拉
$PY results/sa_scan_20261028/slot_scan.py

# ② 建 SA（后台，nohup 写日志，勿用管道）
nohup $PY C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261028/configs_v16b.json \
  --out     results/sa_scan_20261028/res_v16b.jsonl \
  > results/sa_scan_20261028/run_v16b.log 2>&1 &

# ③ 双闸实测（患者式，账号级单并发，需轮询）
$PY results/sa_scan_20261028/prod_patient.py     # 目标写 prod_targets2.json
$PY results/sa_scan_20261028/prod_patient3.py    # 目标写 prod_targets3.json
```

### 7.2 配额与并发约束

- SUPER **1/ET 日/区**，与 REGULAR 4/ET 日/区独立计数；00:00 ET 重置。
- **prod 账号级单并发**：并行开多个 `sa_run.py` 只会互相打掉（`correlation_busy`，返回 None 非报错）。**不要为提速开多进程**。
- 单档仿真 ~6–8 分钟；一批 5 档 ≈ 40 分钟。

### 7.3 若用户点名提交（未点名则不执行）

```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 \
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py \
  submit --alpha-id E567rQvR --region USA
# 复核（等满 ~250s flip 窗）：
... tools/super_build.py status --alpha-id E567rQvR   # 必须 status=ACTIVE，不只看 POST 回执
```

⚠ 提交前先停掉后台 `sa_run.py` 批次；提交任一颗 ⇒ USA/TOP500 封档，其余四颗作废。

### 7.4 下一轮（10-29 夜）候选动作

1. ~~`E567rQvR` prod 复核~~ —— **已提交并 ACTIVE**（prod 0.636）。改为**监控**：OS 起跑后观察 `OSMOSIS_ALLOCATION`（当前 WARNING，无值）与 OS Sharpe 是否衰减。
2. 算子轴（§6.3 ④）：`zscore(w)` / `combo_weight` / `winsorize` / `signed_power(rank(w),3)`。
3. ~~limit 轴 `rank(w)` + l12~~ —— **已证负**（§4.1.1），不必再扫 l14。
4. 不再扫：USA/TOP200、EUR 全域、GLB、IND、KOR、DEU、GBR、MEA；ASI/HKG 池不足。
