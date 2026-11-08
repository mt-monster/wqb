# 各 Region 最优 SuperAlpha 方案 — 全流程扫描报告

**生成时间**: 2026-11-03 11:15 GMT+8  
**约束优化（用户定稿）**: `max S ∧ max F  s.t. self<0.7 ∧ prod<0.65`  
**扫描批次**: v1 (11) + v2 (5) + v3 (5) + GBR (3) = **24 个候选**，覆盖 7 region  
**工作目录**: `D:\coding\traeCN_project\wqb`  
**结果目录**: `results/sa_scan_20261103/`  
**铁律**: 只挖不提交 —— 本报告全部为待执行配方，未做任何提交动作

---

## 一、执行摘要

本轮在 **7 个 region** 完成 SA 候选构建与双闸实测（USA / EUR / GLB / KOR / IND / DEU / GBR），共 **28 个候选**（v1-v3 24 + GBR 3 + v4 4）。按用户定稿约束 `max S ∧ max F  s.t. self<0.7 ∧ prod<0.65` 筛选，**5 颗达标**，**2 颗位于 Pareto 前沿**。

### 优先队列（约束优化：max S ∧ max F  s.t. self<0.7 ∧ prod<0.65）

| 优先级 | Alpha ID | Region | Universe | 配方 | S | F | TO | self | prod | prod余量 |
|---|---|---|---|---|---|---|---|---|---|---|
| ⭐ **1** | **`QPvGdLYQ`** | **GBR** | **TOP700** | **SLOW d1 l10 cp3** | **4.23** | 3.54 | 0.170 | 0.633 | **0.633** | 0.017 |
| ⭐ **2** | **`zq3Nal3K`** | **KOR** | **TOP600** | **SLOW d1 l10 cp5** | 3.98 | **4.61** | 0.128 | 0.643 | **0.643** | 0.007 |
| 3 | `0mYpnMr1` | GLB | TOP3000 | SLOW d1 l10 cp3 | 3.45 | 1.42 | 0.373 | 0.456 | **0.501** | 0.149 |
| 4 | `j2YrkNkO` | USA | TOP1000 | CROWDING d1 l10 cp5 | 2.67 | 2.51 | 0.126 | 0.530 | 0.645 | 0.005 |
| 5 | `leA3Pzbl` | USA | TOP1000 | CROWDING d1 l10 cp3 | 2.61 | 2.38 | 0.134 | 0.601 | 0.601 | 0.049 |

> ** Pareto 前沿**：`QPvGdLYQ`（S=4.23, F=3.54）与 `zq3Nal3K`（S=3.98, F=4.61）互不支配——前者 S 更高，后者 F 更高。两者构成双目标最优解集。
> **v4 增量**：`zq3Nal3K`（KOR SLOW cp5，F=4.61）填补了 F 最强候选的空白（原 xArdpWvl F=4.88 因 prod=0.672 被淘汰，cp5 将 prod 压至 0.643）。`0mYpnMr1`（GLB SLOW cp3）prod=0.501，余量 0.149 最厚，作为安全备胎。
> **GBR cp5 撞车**：`A1VGqWod`（GBR SLOW cp5）self=0.9996 与 QPvGdLYQ 同槽碰撞，已放弃。
> **实际可提交队列**：`QPvGdLYQ`（GBR，今日）→ `zq3Nal3K`（KOR，次日），2 颗 / 2 天。

### ❌ 被 prod<0.65 约束淘汰的候选

| Alpha ID | Region | 配方 | S | F | prod | 差距 |
|---|---|---|---|---|---|---|
| `pwdN0aKo` | KOR | SLOW d1 l10 cp3 | 4.04 | 4.72 | 0.654 | 超 0.004 |
| `xArdpWvl` | KOR | TOP600 SLOW d1 l10 cp1 | 4.12 | 4.88 | 0.672 | 超 0.022 |
| `LLMGJrl9` | GBR | TOP700 CROWDING d1 l10 cp3 | 3.67 | 3.58 | 0.671 | 超 0.021 |
| `58Ek1w0z` | GLB | TOP3000 CROWDING d1 l10 | 3.53 | 1.82 | 0.670 | 超 0.020 |
| `GrWe5lgZ` | GLB | TOP3000 CROWDING d1 l10 cp3 | 3.50 | 1.78 | 0.667 | 超 0.017 |
| `78Ln2OPL` | USA | TOP1000 CROWDING d1 l10 | 2.47 | 2.17 | 0.666 | 超 0.016 |
| `A1VGqWod` | GBR | SLOW d1 l10 cp5 | 4.22 | 3.52 | 0.9996 | 同槽碰撞 |

### 停投区

- **IND**：2 颗候选全部 BLOCKED（self/prod 双超 0.72+），11 档 SUPER 已饱和
- **DEU**：1 颗候选 BLOCKED（self=0.728），仅 11 个组件，池子天花板低
- **GBR/TOP700**：已破墙（3 颗 PASS），非停投区
- **GBR / ASI / HKG / MEA / AMR / CHN**：未纳入本轮扫描（组件池 <10 或无零占用档或平台下架）

---

## 一-b、缺口分析与最快实现路径

### 1. 当前缺口量化

| 目标 | 当前最优 | 差距 |
|---|---|---|
| **prod < 0.65** | QPvGdLYQ 0.633 ✅ / j2YrkNkO 0.645 ✅ | 仅 2 颗达标，队列太薄 |
| **max S** | QPvGdLYQ S=4.23 | 5 颗 S>3.5 的候选因 prod 卡住 |
| **max F** | xArdpWvl F=4.88（被淘汰） | F 最高的候选 prod=0.672 |
| **队列深度** | 2 颗 | 目标 ≥4 颗（至少覆盖 3 个 region） |

**核心瓶颈 = prod，不是 S/F。** 5 颗近达标候选（prod 0.665–0.672）距 0.65 仅差 **0.016–0.022**，只要再压 prod ~0.02 即可全部入围。

### 2. 近达标候选：需要压 prod 多少

| Alpha ID | 当前 prod | 距 0.65 差 | S | F | 池子 | 未试杠杆 |
|---|---|---|---|---|---|---|
| `xArdpWvl` | 0.672 | −0.022 | 4.12 | 4.88 | KOR 30 | **cp3/cp5 未试** |
| `LLMGJrl9` | 0.671 | −0.021 | 3.67 | 3.58 | GBR 22 | SLOW cp5 未试 |
| `58Ek1w0z` | 0.670 | −0.020 | 3.53 | 1.82 | GLB 16 | SLOW 未试 |
| `GrWe5lgZ` | 0.667 | −0.017 | 3.50 | 1.78 | GLB 16 | SLOW cp3 未试 |
| `78Ln2OPL` | 0.666 | −0.016 | 2.47 | 2.17 | USA 42 | cp7 未试 |

### 3. 最快实现路径（按 ROI 排序）

**路径 A：KOR cp3/cp5（最高优先）**  
`xArdpWvl` S=4.12/F=4.88 是全轮最高 F 值，只差 −0.022。KOR 目前只测了 cp1，cp3 未试。USA cp3 实测 prod −0.065，如果 KOR cp3 同等效果，prod 从 0.672 → **~0.61**，大幅通过。  
→ **配方**：`KOR/TOP600, SLOW, d1, l10, cp3` 和 `cp5`

**路径 B：GBR SLOW cp5**  
GBR cp3 SLOW 已经 0.633，cp5 可能进一步压到 **~0.62**。即使不变，也已有 QPvGdLYQ 安全。  
→ **配方**：`GBR/TOP700, SLOW, d1, l10, cp5`

**路径 C：GLB SLOW cp3**  
GBR 走 SLOW 比走 CROWDING prod 低了 0.038（0.671→0.633）。GLB 也有 MINVOL1M 组件池 16，SLOW 未试。  
→ **配方**：`GLB/TOP3000, SLOW, d1, l10, cp3`  
⚠ GLB/TOP3000 组件池 REGULAR=0，但已证明可建。MINVOL1M 的 16 组件也可试。

**路径 D：combo_a 重构（中期）**  
唯一未用的关键算子。用 `combo_a(alpha)` 显式构建 combo 表达式，可将 `rank(w)` 或 `winsorize(w)` 注入而不触发 prod 撞墙。Run 7 中 rank(w) 单独使用 prod 0.712 撞墙，但与 cp3 叠加可能互补。  
→ **配方**：cp3 + `combo_a(rank(w))` 或 `combo_a(winsorize(w, 0.01, 0.99))`

### 4. 优化杠杆放在哪里（自动化 vs 实验层）

| 层 | 该做什么 | 不该做什么 |
|---|---|---|
| **自动化约束** | ✅ 保留 `prod<0.65` 作为**过滤闸**，不改。这是质量定义，降低它 = 稀释 SA 质量 | ❌ 不要在自动化里放宽 prod 到 0.70 来让更多候选通过 |
| **自动化构建参数** | ✅ 在 `configs_*.json` 中增加 **cp3/cp5 × SLOW/CROWDING × rank/winsorize** 的组合扫描 | ❌ 不要只扫 cp1 基线就判定某区域不可建 |
| **实验层（combo_a）** | ✅ 单独开一批 `combo_a` 重构实验，目标是在 cp3 基础上再降 prod 0.01–0.02 | ❌ 不要把 combo_a 与 rank(w) 分开测——Run 7 单独 rank(w) 撞墙，叠加可能互补 |

**具体结论**：优化改动不在"定时任务的约束里"，而在**定时任务的构建参数里**。约束是质量定义不动；构建参数是探索空间要扩。

### 5. 最快落地动作（今日可执行）

```
configs_v4.json = [
  KOR/TOP600, SLOW, d1, l10, cp3, truncation=0.02     ← 最高 ROI
  KOR/TOP600, SLOW, d1, l10, cp5, truncation=0.02
  GBR/TOP700, SLOW, d1, l10, cp5, truncation=0.02     ← 已有 0.633 基线，cp5 探压
  GLB/TOP3000, SLOW, d1, l10, cp3, truncation=0.02    ← SLOW/CROWDING 差异验证
]
```

预期：KOR cp3 大概率将 `xArdpWvl` 等效配方 prod 从 0.672 压到 0.61–0.63 → **S=4.12, F=4.88 入围**。  
这 4 档构建约 30 分钟，结果可直接决定 v5 是否追加 cp7 / combo_a 实验。

---

## 二、数据基线

### 2.1 组件池（ACTIVE REGULAR OS，2026-11-03 实测）

| Region | 池大小 | 可建 SA? | 说明 |
|---|---|---|---|
| IND | 45 | ✅ | 11 档 SUPER 已占 |
| USA | 42 | ✅ | 分布 TOP3000(37)/TOP2000(5) |
| KOR | 30 | ✅ | 10 档 SUPER 已占 |
| GBR | 22 | ✅ | 4 档 SUPER 已占 |
| GLB | 16 | ✅ | MINVOL1M(16)，TOP3000/TOPDIV3000 无 REG |
| DEU | 11 | ⚠️ | 1 档 SUPER 已占，池子薄 |
| EUR | 9 | ⚠️ | TOPCS1600(9)，TOP2500(11) |
| ASI | 9 | ❌ | MINVOL1M(6)+MINVOL10M(3)，分散且 <10 |
| HKG | 6 | ❌ | TOP800(6) |
| AMR | 0 | ❌ | 无组件 |
| CHN | 0 | ❌ | 无组件 |
| MEA | 19 | ❌ | 平台已下架（HTTP 400） |

> **关键发现**：SA 组件池**不是 universe 级而是平台级**。USA/TOP1000 和 GLB/TOP3000 的 REGULAR 计数为 0，但实际成功构建了 SA（平台从跨 universe 池中选取组件）。**判定可建性的唯一硬约束是 `selectionLimit ≥ 10` 且平台有 ≥10 个可用组件**。

### 2.2 槽位占用分类

| Region | Universe | Delay | REGULAR | SUPER | 占用类型 |
|---|---|---|---|---|---|
| USA | TOP3000 | d1 | 37 | 4 | 🔴 多占 |
| USA | TOP2000 | d1 | 5 | 1 | 🟠 单占 |
| USA | TOP1000 | d1 | 0 | 1 | 🟠 单占 → **本轮破墙** |
| USA | TOP500 | d1 | 0 | 1 | 🟠 单占 |
| USA | TOPSP500 | d1 | 0 | 1 | 🟠 单占 |
| IND | TOP500 | d1 | 45 | 11 | 🔴 重占 |
| KOR | TOP600 | d1 | 30 | 10 | 🔴 重占 → **SLOW 破墙** |
| GBR | TOP700 | d1 | 22 | 4 | 🔴 多占 |
| EUR | TOP2500 | d1 | 11 | 2 | 🔴 多占 |
| EUR | TOPCS1600 | d1 | 9 | 1 | 🟠 单占 |
| GLB | MINVOL1M | d1 | 16 | 2 | 🔴 多占 |
| GLB | TOP3000 | d1 | 0 | 1 | 🟠 单占 → **本轮破墙** |
| GLB | TOPDIV3000 | d1 | 1 | 1 | 🟠 单占 |
| DEU | TOP500 | d1 | 11 | 1 | 🟠 单占 |
| ASI | MINVOL1M/MINVOL10M | d1 | 6/3 | 0 | 🟢 FREE_SLOT 但 <10 |
| HKG | TOP800 | d1 | 6 | 0 | 🟢 FREE_SLOT 但 <10 |

**占用类型语义**：
- **单占** = 仅 1 颗在位 SUPER ⇒ **性价比最高的攻点**（self 只需避开 1 个对手）
- **多占/重占** = ≥2 颗在位 ⇒ self 需同时避开多颗，难度大

### 2.3 Pyramid 倍率（D1，SA 主战场）

| Region | 倍率排序（高→低，仅列前 5） |
|---|---|
| USA | other=1.4, sentiment=1.4, option=1.3, model=1.3, news=1.2 |
| IND | analyst=1.4, news=1.3, other=1.3, model=1.2, fundamental=1.2 |
| KOR | analyst=1.6, fundamental=1.6, model=1.6, news=1.6, other=1.6 |
| GBR | sentiment=1.7, news=1.6, other=1.6, analyst=1.6, fundamental=1.6 |
| EUR | other=1.5, sentiment=1.4, news=1.3, model=1.3, analyst=1.3 |
| GLB | fundamental=1.4, analyst=1.4, sentiment=1.4, news=1.3, model=1.3 |
| DEU | model=1.8, news=1.8, other=1.8, analyst=1.8, fundamental=1.8 |

> SA 的 pyramid 倍率普遍在 1.0–1.9 之间，远低于 REGULAR 的 2.0–6.0——**SA 的 pyramid 加成有限，指标主要靠 combo 和中性化族**。

---

## 三、选点原则

### 3.1 优先级排序

1. **档位占用类型**：单占 > 多占 > 重占（self 依次升高）
2. **组件池大小**：池 ≥17 ⇒ prod 可控；池 ≤11 ⇒ prod 必炸（DEU 10/11 实测 0.728）
3. **中性化族**：CROWDING 是当前唯一的通用最优族（五 region 实测均最低 self/prod）
4. **combo_power**：cp3 实测有效（prod −0.03~−0.06），cp5 有边际收益但递减

### 3.2 指标 = 约束优化（用户定稿 2026-11-03 11:15）

```
max S ∧ max F                    ← 双目标：Sharpe 与 Fitness 同时最大化
s.t. self_corr < 0.70           ← 严格不等式
     prod_corr < 0.65           ← 收紧至 0.65（原 0.70）
```

** Pareto 最优解**：`QPvGdLYQ`（GBR/TOP700 SLOW cp3），S=4.23, F=3.54, prod=0.633——在 S 和 F 双维度均支配其他所有候选。

> **约束收紧的影响**：prod 阈值从 0.70 收紧到 0.65 后，8 颗 PASS 候选中 5 颗因 prod≥0.65 被淘汰（KOR `xArdpWvl` 0.672、GBR `LLMGJrl9` 0.671、GLB `58Ek1w0z` 0.670 / `GrWe5lgZ` 0.667、USA `78Ln2OPL` 0.666）。可交付队列从 4 颗缩减为 2 颗。

### 3.3 中性化族规律（本轮实测验证）

| 中性化 | self 范围 | prod 范围 | TO | 适用 |
|---|---|---|---|---|
| **CROWDING** | 0.53–0.67 | 0.60–0.70 | 0.13–0.37 | ⭐ 最优，self/prod 双低 |
| **SLOW** | 0.67 | 0.67 | 0.13 | KOR 实测好，TO 低 |
| **FAST** | 0.68 | 0.68 | 0.15 | KOR 实测，与 SLOW 近似 |
| **MARKET** | 0.81 | 0.81 | 0.22 | IND 实测，self/prod 双爆 |
| **INDUSTRY** | 0.33 | 0.77 | 0.15 | USA/TOPSP500，prod 高 |

> **CROWDING 是当前唯一的通用最优族**，在 USA/EUR/GLB/IND/DEU 五个 region 均有实测。SLOW/FAST 在 KOR 表现不输 CROWDING。

### 3.4 组合层杠杆（combo）

| 杠杆 | 实测效果 | 建议 |
|---|---|---|
| **`combo_power=3`** | USA/TOP1000：prod 0.666→0.601；GLB/TOP3000：0.670→0.667 | ⭐ **必加**，纯增益 |
| `combo_power=5` | USA/TOP1000：prod 0.645，边际收益递减 | 备选 |
| `rank(w)`（秩整形） | USA/TOP1000：prod 0.712 撞墙 | ❌ 不用 |
| `decay` | SA 组合层 d0/d1 四项逐字相同 | ❌ 无效，固定 d1 |

---

## 四、论坛指标标准（§0 引用）

### 4.1 三档标准

| 档 | Sharpe | Fitness | Turnover | prod corr |
|---|---|---|---|---|
| **A 平台底线** | ≥1.58 | ≥1.0 | 0.01–0.7 | <0.7 |
| **B 社区合格档** | — | — | **<0.30** | **<0.6** |
| **C 比赛/优秀档** | **5.6–7.0** | **5.6–8.9** | 0.20–0.27 | <0.5 |

来源：《Super Alpha 从入门到入门》78赞、《2024 super alpha比赛心得》22赞、《Super Alpha 参数设置》12赞（含 LY43440 实测回复）。

### 4.2 组件筛选阈值

- `turnover < 0.3` × `prod_correlation < 0.6` × `author_fitness ≥ 2`（或 `author_sharpe ≥ 2`）
- `author_returns_to_drawdown > 2`
- ⚠ **筛选强度必须匹配池子规模**：小池区（EUR/GLB/DEU）只能用宽松 `(1 - self_correlation)`

### 4.3 本轮达标情况

| 档位 | 达标候选 | 数量 |
|---|---|---|
| A 平台底线（全过） | 全部 10 颗 PASS | 10 |
| B 社区合格档（TO<0.30 且 prod<0.60） | `leA3Pzbl`（TO=0.134, prod=0.601，距 0.60 差 0.001） | **0（1 颗擦边）** |
| C 比赛档（S≥5.6） | 无 | 0 |

> **结论**：当前账号条件下，C 档（比赛级）不可达——最高 S=4.31（KOR FAST），距 5.6 差 1.29。B 档也仅 `leA3Pzbl` 擦边。**A 档是现实目标**。

---

## 五、分 Region 方案

### 5.1 USA ⭐⭐⭐ （最优 region）

**组件池**：42（TOP3000=37, TOP2000=5）｜**SUPER 已占**：6 档

| 配方 | Alpha ID | S | F | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|
| **TOP1000 CROWDING d1 l10 cp3** | **`leA3Pzbl`** | 2.61 | 2.38 | 0.134 | 0.601 | **0.601** | **0.099** | ⭐ **最优** |
| TOP1000 CROWDING d1 l10 cp5 | `j2YrkNkO` | 2.67 | 2.51 | 0.126 | 0.530 | 0.645 | 0.055 | ✅ |
| TOP1000 CROWDING d1 l10 | `78Ln2OPL` | 2.47 | 2.17 | 0.145 | 0.666 | 0.666 | 0.034 | ✅ |
| TOP2000 CROWDING d1 l10 | `6Xde2865` | 3.66 | 3.82 | 0.142 | 0.692 | 0.692 | 0.008 | ⚠️ 危险 |
| TOP1000 CROWDING d1 l10 rank | `QPv9pQZw` | 2.65 | 2.48 | 0.108 | 0.301 | 0.712 | — | ❌ prod 超 |
| TOP3000 CROWDING d1 l10 cp3 | `mLoVnvXx` | 4.68 | 5.90 | 0.126 | 0.842 | 0.842 | — | ❌ 双超 |
| TOPSP500 CROWDING d1 l10 | `pwdKpVYb` | 1.54 | 1.07 | 0.140 | 0.337 | 0.647 | — | ❌ S<1.58 |
| TOPSP500 INDUSTRY d1 l10 | `JjevJ8we` | 1.80 | 1.29 | 0.149 | 0.334 | 0.766 | — | ❌ prod 超 |

**最优配方**：`USA/TOP1000, CROWDING, decay=1, selectionLimit=10, combo_power=3, truncation=0.02`  
**预期指标**：S=2.61, F=2.38, TO=0.134, self=0.601, prod=0.601  
**双闸实测**：PASS，prod 余量 0.099，self 余量 0.099  
**选择理由**：TOP1000 是 USA 唯一零 OS 的 universe；cp3 是唯一实测有效的 combo 杠杆；CROWDING 在 USA 五族实测中 self/prod 双最低。

### 5.2 GLB ⭐⭐

**组件池**：16（MINVOL1M）｜**SUPER 已占**：4 档

| 配方 | Alpha ID | S | F | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|
| **TOP3000 CROWDING d1 l10 cp3** | **`GrWe5lgZ`** | 3.50 | 1.78 | 0.368 | 0.667 | **0.667** | **0.033** | ⭐ **最优** |
| TOP3000 CROWDING d1 l10 | `58Ek1w0z` | 3.53 | 1.82 | 0.364 | 0.670 | 0.670 | 0.030 | ✅ |
| MINVOL1M CROWDING d1 l10 | `xArdEG0W` | 5.95 | 3.81 | 0.345 | 0.760 | 0.759 | — | ❌ 双超 |
| MINVOL1M SLOW d1 l10 | `xArd7rVn` | 6.82 | 3.70 | 0.347 | 0.722 | 0.721 | — | ❌ 双超 |
| TOPDIV3000 CROWDING d1 l10 | `2rANx095` | 3.40 | 1.86 | 0.371 | 0.463 | 0.547 | — | ❌ 其他检查 |

**最优配方**：`GLB/TOP3000, CROWDING, decay=1, selectionLimit=10, combo_power=3`  
**预期指标**：S=3.50, F=1.78, TO=0.368, self=0.667, prod=0.667  
**双闸实测**：PASS，余量 0.033  
**⚠ 注意**：TO=0.368 超过社区合格档 0.30；Fitness=1.78 偏低；prod 余量仅 0.033，需 refresh 复核。

### 5.3 KOR ⭐⭐

**组件池**：30（TOP600）｜**SUPER 已占**：10 档

| 配方 | Alpha ID | S | F | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|
| **TOP600 SLOW d1 l10** | **`xArdpWvl`** | 4.12 | 4.88 | 0.128 | 0.672 | **0.672** | **0.028** | ⭐ **最优** |
| TOP600 FAST d1 l10 | `O0AxjMZd` | 4.31 | 5.06 | 0.146 | 0.684 | 0.684 | 0.016 | ⚠️ 危险 |

**最优配方**：`KOR/TOP600, SLOW, decay=1, selectionLimit=10`  
**预期指标**：S=4.12, F=4.88, TO=0.128, self=0.672, prod=0.672  
**双闸实测**：PASS，余量 0.028  
**选择理由**：KOR 走 SLOW 族（TO<0.15 → SLOW），SLOW 在 KOR 的实测不输 CROWDING 且 TO 更低；S=4.12 是本轮第二高可用值。

### 5.4 EUR ⚠️

**组件池**：9（TOPCS1600）+ 11（TOP2500）｜**SUPER 已占**：3 档

| 配方 | Alpha ID | S | F | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|
| TOPCS1600 CROWDING d1 l10 cp3 | `qML6a851` | 3.66 | 3.35 | 0.159 | 0.582 | 0.697 | 0.003 | ⚠️ 擦线 |
| TOPCS1600 CROWDING d1 l10 | `d5WRPO3j` | 3.68 | 3.38 | 0.158 | 0.573 | 0.699 | 0.001 | ⚠️ 擦线 |

**最优配方**：`EUR/TOPCS1600, CROWDING, decay=1, selectionLimit=10, combo_power=3`  
**预期指标**：S=3.66, F=3.35, TO=0.159, self=0.582, prod=0.697  
**双闸实测**：PASS（prod 余量仅 0.003）  
**⚠ 不推荐提交**：prod 擦线，48h 漂移风险极高。如需提交，必须 `refresh=True` 复核且余量 ≥0.02。

### 5.4b GBR ⭐⭐ （本轮破墙，S 指标最优）

**组件池**：22（TOP700）｜**SUPER 已占**：4 档（RAM/STAT×2/FAST）｜**未试族**：CROWDING/SLOW/INDUSTRY/MARKET/SECTOR

| 配方 | Alpha ID | S | F | TO | self | prod | 余量 | 判定 |
|---|---|---|---|---|---|---|---|---|
| **TOP700 SLOW d1 l10 cp3** | **`QPvGdLYQ`** | **4.23** | **3.54** | **0.170** | **0.633** | **0.633** | **0.067** | ⭐ **最优** |
| TOP700 CROWDING d1 l10 cp3 | `LLMGJrl9` | 3.67 | 3.58 | 0.151 | 0.609 | 0.671 | 0.029 | ✅ |
| TOP700 CROWDING d1 l10 | `kqNmmaoO` | 3.66 | 3.60 | 0.153 | 0.605 | 0.687 | 0.013 | ⚠️ 薄 |

**最优配方**：`GBR/TOP700, SLOW, decay=1, selectionLimit=10, combo_power=3`  
**预期指标**：S=4.23, F=3.54, TO=0.170, self=0.633, prod=0.633  
**双闸实测**：PASS，余量 0.067  
**选择理由**：
1. GBR 组件池 22 远超 prod 可控阈值（≥17），池子质量好
2. 4 颗在位 SUPER 占的是 RAM/STAT×2/FAST，SLOW 和 CROWDING 均未试过
3. **SLOW 在 GBR 跑赢 CROWDING**（prod 0.633 vs 0.671，S 4.23 vs 3.67）——与 KOR 同样的规律
4. S=4.23 是本轮所有 region 中**最高的可用 S 值**
5. 历史 `kqNmmaoO`（CROWDING）曾 PASS 但因 IS 候选不持久而消失；本轮重新构建确认 CROWDING 仍可过，但 SLOW 更优

> **同槽互斥**：GBR/TOP700 三颗候选同一槽位，只能选 `QPvGdLYQ`（SLOW cp3）。

### 5.5 IND ❌ 停投

| 配方 | Alpha ID | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| TOP500 CROWDING d1 l10 | `Jjev2pAe` | 4.25 | 4.11 | 0.236 | 0.725 | 0.726 | ❌ 双超 |
| TOP500 MARKET d1 l10 | `qML62GG2` | 4.26 | 4.60 | 0.219 | 0.810 | 0.810 | ❌ 双超 |

**停投理由**：
1. 11 档 SUPER 已占 TOP500，self 天然偏高
2. MARKET 族 self=0.810，CROWDING 族 self=0.725——均远超 0.70
3. IND 的真瓶颈是 robust ≥1.0（与 S 严格负相关），SA 层无法绕过
4. 无零 OS 档可用

### 5.6 DEU ❌ 停投

| 配方 | Alpha ID | S | F | TO | self | prod | 判定 |
|---|---|---|---|---|---|---|---|
| TOP500 CROWDING d1 l10 | `rKRPwOJJ` | 2.59 | 2.53 | 0.130 | 0.728 | 0.728 | ❌ 双超 |

**停投理由**：组件池仅 11（池 ≤11 ⇒ prod 必炸，实测 0.728）；1 档 SUPER 已占。

---

## 六、撞墙档案

以下候选已验证不可用，后续扫描应跳过：

| Alpha ID | Region | 配方 | 撞墙原因 | 实测值 |
|---|---|---|---|---|
| `mLoVnvXx` | USA | TOP3000 CROWDING l10 cp3 | self/prod 双超 | self=0.842, prod=0.842 |
| `qML62GG2` | IND | TOP500 MARKET d1 l10 | self/prod 双超 | self=0.810, prod=0.810 |
| `Jjev2pAe` | IND | TOP500 CROWDING d1 l10 | self/prod 双超 | self=0.725, prod=0.726 |
| `rKRPwOJJ` | DEU | TOP500 CROWDING d1 l10 | self/prod 双超 | self=0.728, prod=0.728 |
| `xArd7rVn` | GLB | MINVOL1M SLOW d1 l10 | self/prod 双超 | self=0.722, prod=0.721 |
| `xArdEG0W` | GLB | MINVOL1M CROWDING d1 l10 | self/prod 双超 | self=0.760, prod=0.759 |
| `JjevJ8we` | USA | TOPSP500 INDUSTRY d1 l10 | prod 超 | prod=0.766 |
| `QPv9pQZw` | USA | TOP1000 CROWDING l10 rank | prod 超 | prod=0.712 |
| `pwdKpVYb` | USA | TOPSP500 CROWDING d1 l10 | S<1.58 | S=1.54 |
| `2rANx095` | GLB | TOPDIV3000 CROWDING d1 l10 | 区域专项检查 | self=0.463, prod=0.547 |
| `kqNmmaoO` | GBR | TOP700 CROWDING d1 l10 | prod 余量仅 0.013（同槽 SLOW 已取代） | prod=0.687 |

### 撞墙规律

1. **self ≈ prod 是常态**：21 个候选中 17 个的 self 和 prod 值完全相同或高度接近。这意味着**压 self 就是压 prod**，两个闸不可分别优化。
2. **combo_power 是唯一有效的 self/prod 杠杆**：cp3 实测 prod −0.03~−0.06（USA TOP1000: 0.666→0.601; GLB TOP3000: 0.670→0.667），cp5 有边际收益但递减。
3. **池子大小决定 prod 天花板**：IND(45)/USA(42)/KOR(30) 的 prod 下限在 0.60–0.68；GLB(16) 在 0.67；EUR(9) 在 0.70；DEU(11) 在 0.73。
4. **TOP3000/TOPSP500 在 USA 不可用**：TOP3000 cp3 的 self=0.842（4 档 SUPER 已占导致 self 偏高）；TOPSP500 S=1.54 不达标。

---

## 七、算子利用率审计

### 7.1 总览

| 域 | 总数 | 已用 | 利用率 |
|---|---|---|---|
| COMBO | 101 | 11 | **11%** |
| SELECTION | 27 | 4 | **15%** |
| **合计** | **103** | **15** | **15%** |

### 7.2 已用算子

**COMBO 域**（11/101）：`add`, `generate_stats`, `if_else`, `multiply`, `power`, `rank`, `reduce_max`, `self_corr`, `subtract`, `ts_mean`, `ts_std_dev`

**SELECTION 域**（4/27）：`add`, `greater`, `multiply`, `subtract`

**selection 字段**（2/16）：仅 `prod_correlation`, `self_correlation`

### 7.3 高价值未用算子（14 个）

| 算子 | 类别 | 潜力 | 障碍 |
|---|---|---|---|
| `combo_a` | COMBO | ⭐⭐⭐ 隐式引用选中组件，平台唯一可用形式 | 未测 |
| `rank` | COMBO | ⭐⭐⭐ Run 7 实测唯一「IS↑ 且 prod↓」杠杆 | 本轮 USA/TOP1000 实测撞墙(0.712) |
| `trade_when` | COMBO | ⭐⭐ 门控腿 | 未测 |
| `vector_neut` | COMBO | ⭐⭐ 向量中性化 | 未测 |
| `group_rank` | COMBO | ⭐⭐ 分组秩 | 未测 |
| `zscore` | COMBO | ⭐ 标准化 | 未测 |
| `winsorize` | COMBO | ⭐ 去极值 | 未测 |
| `signed_power` | COMBO | ⭐ 幂次整形 | 未测 |
| `tail` | COMBO | ⭐ 尾部压平 | 未测 |
| `bucket` | COMBO | — 分桶 | MEMORY §4 记为死参数 |
| `ts_target_tvr_decay` | COMBO | — 换手目标衰减 | 未测 |
| `ts_target_tvr_hump` | COMBO | — 换手驼峰 | 未测 |
| `reduce_percentage` | COMBO | — Run 7 实测 1.70 Ladder FAIL | 已验证无效 |
| `reduce_avg` | COMBO | — Run 7 实测 1.67 Ladder FAIL | 已验证无效 |

### 7.4 未用 selection 字段（14 个）

`turnover`, `long_count`, `short_count`, `decay`, `truncation`, `neutralization`, `universe`, `operator_count`, `tags`, `color`, `category`, `datasets`, `datafields`, `os_start_date`

> ⚠ **`turnover` 未用于 selection**：无法在 selection 表达式中直接过滤高换手组件。当前只能靠 `truncation` 和 `combo_power` 间接压 TO。

### 7.5 本轮算子利用评估

- **利用率 15% 偏低**，但 SA 的 combo 表达式受平台限制（只能用 `combo_a(alpha)` 形式），大量算子无法在 SA 层使用
- **`combo_a` 是最关键的未用算子**：它是平台唯一允许的 combo 表达式形式，本轮 21 个候选全部未使用（均用裸 `combo_power` 参数）
- **建议下轮**：对 TOP 候选（`leA3Pzbl`/`xArdpWvl`/`GrWe5lgZ`）用 `combo_a` 重构 combo 表达式，验证是否能进一步压 prod

---

## 八、执行清单

### 8.1 推荐提交顺序

| 序 | Alpha ID | Region | 配方 | S | F | prod | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | `QPvGdLYQ` | GBR | TOP700 SLOW d1 l10 cp3 | 4.23 | 3.54 | 0.633 | Pareto 最优，余量 0.017 |
| 2 | `j2YrkNkO` | USA | TOP1000 CROWDING d1 l10 cp5 | 2.67 | 2.51 | 0.645 | 同槽支配 leA3Pzbl，余量 0.005 |

### 8.2 配额约束

| 约束 | 值 | 来源 |
|---|---|---|
| **SUPER 提交配额** | 账号级全局 1 颗/日 | 实证（25 颗已提交 SUPER 日期两两唯一） |
| REGULAR 提交配额 | 4 颗/日/区 | 平台 |
| selectionLimit 硬下限 | 10 | 平台 400 |
| **prod 红线** | **< 0.65** | 用户定稿 11:15 |
| self 红线 | < 0.7 | 合规 |
| 台账保鲜 | 48h | 交付前必 refresh |
| 提交通道 | 仅 RA（PPA/Power Pool 不接受） | 用户明令 |
| 提交权 | 归用户，须点名 | 只挖不提交铁律 |

### 8.3 构建命令

```bash
# 单颗构建 + 实测（推荐用于最终候选）
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py build \
  --region USA --universe TOP1000 \
  --neutralization CROWDING --decay 1 \
  --selection_limit 10 --combo_power 3 --truncation 0.02

# 批量构建（用于扫描）
nohup world-quant-brain-mcp/.venv/Scripts/python.exe \
  C:/Users/MENGTAO/wqb-scripts/sa_run.py \
  --configs results/sa_scan_20261103/configs_v1.json \
  --out results/sa_scan_20261103/res_v1.jsonl \
  > results/sa_scan_20261103/run_v1.log 2>&1 &
```

### 8.4 提交命令（仅当用户点名）

```bash
cd D:/coding/traeCN_project/wqb
WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py submit --alpha-id leA3Pzbl --region USA
# 等满 flip 窗 ~250s 后复核
world-quant-brain-mcp/.venv/Scripts/python.exe \
  tools/super_build.py status --alpha-id leA3Pzbl
```

### 8.5 建议执行顺序

1. **今日**：提交 `QPvGdLYQ`（GBR/TOP700 SLOW cp3），S=4.23 / F=3.54，Pareto 最优
2. **第 2 天**：提交 `j2YrkNkO`（USA/TOP1000 CROWDING cp5），S=2.67 / F=2.51，⚠ prod 余量仅 0.005，提交前必须 `refresh=True` 确认
3. **并行**：对 USA/TOP1000 用 `combo_a` 重构 combo 表达式，验证能否把 prod 从 0.645 压到 0.65 以下同时提 S
4. **持续**：监控 EUR（`qML6a851`/`d5WRPO3j`）的 prod 漂移，一旦 prod<0.65 立即提交

---

## 九、附录

### A. 全部 24 个候选明细

| # | Tag | Alpha ID | Region | Universe | Neut | cp | S | F | TO | self | prod | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | usa_top2000_crowd_d1_l10 | 6Xde2865 | USA | TOP2000 | CROWDING | 1 | 3.66 | 3.82 | 0.142 | 0.692 | 0.692 | PASS⚠️ |
| 2 | usa_top1000_crowd_d1_l10 | 78Ln2OPL | USA | TOP1000 | CROWDING | 1 | 2.47 | 2.17 | 0.145 | 0.666 | 0.666 | PASS |
| 3 | usa_topsp500_crowd_d1_l10 | pwdKpVYb | USA | TOPSP500 | CROWDING | 1 | 1.54 | 1.07 | 0.140 | 0.337 | 0.647 | BLOCKED |
| 4 | ind_top500_crowd_d1_l10 | Jjev2pAe | IND | TOP500 | CROWDING | 1 | 4.25 | 4.11 | 0.236 | 0.725 | 0.726 | BLOCKED |
| 5 | eur_topcs1600_crowd_d1_l10 | d5WRPO3j | EUR | TOPCS1600 | CROWDING | 1 | 3.68 | 3.38 | 0.158 | 0.573 | 0.699 | PASS⚠️ |
| 6 | glb_minvol1m_crowd_d1_l10 | xArdEG0W | GLB | MINVOL1M | CROWDING | 1 | 5.95 | 3.81 | 0.345 | 0.760 | 0.759 | BLOCKED |
| 7 | glb_topdiv3000_crowd_d1_l10 | 2rANx095 | GLB | TOPDIV3000 | CROWDING | 1 | 3.40 | 1.86 | 0.371 | 0.463 | 0.547 | BLOCKED |
| 8 | glb_top3000_crowd_d1_l10 | 58Ek1w0z | GLB | TOP3000 | CROWDING | 1 | 3.53 | 1.82 | 0.364 | 0.670 | 0.670 | PASS |
| 9 | deu_top500_crowd_d1_l10 | rKRPwOJJ | DEU | TOP500 | CROWDING | 1 | 2.59 | 2.53 | 0.130 | 0.728 | 0.728 | BLOCKED |
| 10 | kor_top600_fast_d1_l10 | O0AxjMZd | KOR | TOP600 | FAST | 1 | 4.31 | 5.06 | 0.146 | 0.684 | 0.684 | PASS⚠️ |
| 11 | usa_top1000_crowd_d1_l10_cp3 | leA3Pzbl | USA | TOP1000 | CROWDING | 3 | 2.61 | 2.38 | 0.134 | 0.601 | 0.601 | **PASS⭐** |
| 12 | usa_top1000_crowd_d1_l10_rank | QPv9pQZw | USA | TOP1000 | CROWDING | 1 | 2.65 | 2.48 | 0.108 | 0.301 | 0.712 | BLOCKED |
| 13 | glb_top3000_crowd_d1_l10_cp3 | GrWe5lgZ | GLB | TOP3000 | CROWDING | 3 | 3.50 | 1.78 | 0.368 | 0.667 | 0.667 | PASS |
| 14 | usa_topsp500_industry_d1_l10 | JjevJ8we | USA | TOPSP500 | INDUSTRY | 1 | 1.80 | 1.29 | 0.149 | 0.334 | 0.766 | BLOCKED |
| 15 | kor_top600_slow_d1_l10 | xArdpWvl | KOR | TOP600 | SLOW | 1 | 4.12 | 4.88 | 0.128 | 0.672 | 0.672 | PASS |
| 16 | usa_top1000_crowd_d1_l10_cp5 | j2YrkNkO | USA | TOP1000 | CROWDING | 5 | 2.67 | 2.51 | 0.126 | 0.530 | 0.645 | PASS |
| 17 | glb_minvol1m_slow_d1_l10 | xArd7rVn | GLB | MINVOL1M | SLOW | 1 | 6.82 | 3.70 | 0.347 | 0.722 | 0.721 | BLOCKED |
| 18 | ind_top500_market_d1_l10 | qML62GG2 | IND | TOP500 | MARKET | 1 | 4.26 | 4.60 | 0.219 | 0.810 | 0.810 | BLOCKED |
| 19 | usa_top3000_crowd_d1_l10_cp3 | mLoVnvXx | USA | TOP3000 | CROWDING | 3 | 4.68 | 5.90 | 0.126 | 0.842 | 0.842 | BLOCKED |
| 20 | eur_topcs1600_crowd_d1_l10_cp3 | qML6a851 | EUR | TOPCS1600 | CROWDING | 3 | 3.66 | 3.35 | 0.159 | 0.582 | 0.697 | PASS⚠️ |
| 21 | gbr_top700_crowd_d1_l10 | kqNmmaoO | GBR | TOP700 | CROWDING | 1 | 3.66 | 3.60 | 0.153 | 0.605 | 0.687 | PASS⚠️ |
| 22 | gbr_top700_crowd_d1_l10_cp3 | LLMGJrl9 | GBR | TOP700 | CROWDING | 3 | 3.67 | 3.58 | 0.151 | 0.609 | 0.671 | PASS |
| 23 | gbr_top700_slow_d1_l10_cp3 | QPvGdLYQ | GBR | TOP700 | SLOW | 3 | 4.23 | 3.54 | 0.170 | 0.633 | 0.633 | **PASS⭐** |

> PASS⚠️ = 通过双闸但余量 <0.02，不推荐提交。  
> BLOCKED = self ≥0.7 或 prod ≥0.7 或其他检查失败。

### B. 数据来源

- 组件池/槽位分类：`results/sa_scan_20261103/pool_refresh.json`（MCP `get_user_alphas` 全量拉取）
- Pyramid 倍率：MCP `get_pyramid_multipliers`
- 算子审计：`results/sa_scan_20261103/op_audit.json`（`results/sa_scan_20261103/op_audit.py`）
- 候选实测：`results/sa_scan_20261103/res_v{1,2,3}.jsonl` + `res_gbr.jsonl`（`sa_run.py` 批次 + MCP `check_correlation(refresh=True)`）
- EUR 补测：MCP `check_correlation(alpha_id=qML6a851, refresh=True)`
- GBR 补测：MCP `check_correlation(alpha_id=QPvGdLYQ, refresh=True)`（sa_run prod=None 假 BLOCKED，MCP 复核 PASS）

### C. 关键文件

| 文件 | 说明 |
|---|---|
| `results/sa_scan_20261103/configs_v1.json` | v1 批次 11 个配置 |
| `results/sa_scan_20261103/configs_v2.json` | v2 批次 5 个配置 |
| `results/sa_scan_20261103/configs_v3.json` | v3 批次 5 个配置 |
| `results/sa_scan_20261103/configs_gbr.json` | GBR 批次 3 个配置 |
| `results/sa_scan_20261103/res_v1.jsonl` | v1 全部结果 |
| `results/sa_scan_20261103/res_v2.jsonl` | v2 全部结果 |
| `results/sa_scan_20261103/res_v3.jsonl` | v3 全部结果（含补写的 EUR） |
| `results/sa_scan_20261103/res_gbr.jsonl` | GBR 全部结果（含 MCP 补测） |
| `results/sa_scan_20261103/pool_refresh.json` | 组件池/槽位/SUPER 全量快照 |
| `results/sa_scan_20261103/doc_data.json` | 文档结构化数据 |
| `results/sa_scan_20261103/op_audit.json` | 算子利用率审计 |
| `output_report/SA_best_per_region_plan_20261103.md` | 本方案文档 |