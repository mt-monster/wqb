# fundamental22（ESG Data）字段画像与批次 19 预登记（USA / TOP3000 / D1）

as_of 2026-10-21　｜　平台：USA　｜　delay 1　｜　universe TOP3000
数据来源：`get_datafields(region="USA", dataset_id="fundamental22", universe="TOP3000", delay=1, filter_sharpe=false)`，`complete=true / platform_count=14`。

## 0. 数据集元信息

| 项 | 值 |
|---|---|
| 数据集 id | `fundamental22`（ESG Data） |
| 字段数 | **14（全部 VECTOR，无 MATRIX）** |
| 数据集 alphaCount | 81（来自 2026-10-19 的 fundamental 扫描表；**14 个字段的 aC 之和 = 103**，大于 81 属正常——一条 alpha 可同时引用多字段） |
| 覆盖率 | 全部 0.7229–0.7234（同一底表的切片，覆盖率差异 < 0.0006） |
| 用户数 | 3–12，单字段 aC 3–15 |
| 语义 | **匿名**：字段 id 只有 `a0..a9 / as / s1 / s2 / value`，描述多为模板文本（"Value of the field"），仅 `a4` 明确标为 Social 主题 KPI。**没有任何可读的指标名 ⇒ 本集必须按「数值行为」而非「经济语义」设计机制** |
| 是否点亮 | 未点亮（USA/D1 本季亮塔 = model 4 / analyst 1 / earnings 1） |
| 入选理由 | 剩余 fundamental 中 **aC 次低且从未挖过**：更低的 fnd67 已判死（S≤0.64）、fnd35 仅 1 字段、fnd25 仅 8 字段且 cov 0.38；fnd22 的 14 字段 aC 3–15 / uC 3–12 是平台上**最不拥挤**的一档，是破 prod 相关性的最优赌注 |

## 1. 字段清单（14/14，ATOM 全覆盖）

| # | 字段 id | 类型 | cov | aC | uC | 描述（截断） |
|---|---|---|---|---|---|---|
| 1 | `fnd22_a0_value` | VECTOR | 0.7229 | 6 | 4 | Value of the field |
| 2 | `fnd22_a1_value` | VECTOR | 0.7234 | 6 | 5 | ESG KPI 数值，按位置映射到 codebook item |
| 3 | `fnd22_a2_value` | VECTOR | 0.7234 | 7 | 5 | ESG 特征/指标数值，语义取决于映射 |
| 4 | `fnd22_a3_value` | VECTOR | 0.7234 | 6 | 6 | ESG KPI 数值，指标取决于 module 映射 |
| 5 | `fnd22_a4_value` | VECTOR | 0.7231 | 6 | 5 | **Social (A4) 主题** KPI 数值/评分 |
| 6 | `fnd22_a5_value` | VECTOR | 0.7234 | 8 | 7 | Value of the field |
| 7 | `fnd22_a6_value` | VECTOR | 0.7234 | 12 | 9 | Value of the field |
| 8 | `fnd22_a7_value` | VECTOR | 0.7234 | **15** | **12** | Value of the field（本集最拥挤字段） |
| 9 | `fnd22_a8_value` | VECTOR | 0.7233 | 4 | 3 | Value of the field |
| 10 | `fnd22_a9_value` | VECTOR | 0.7234 | **3** | **3** | Value of the field（本集最冷字段） |
| 11 | `fnd22_as_value` | VECTOR | 0.7234 | 5 | 5 | Value of the field |
| 12 | `fnd22_s1_value` | VECTOR | 0.7233 | 13 | 8 | ESG metric/KPI 数值 |
| 13 | `fnd22_s2_value` | VECTOR | 0.7234 | 5 | 3 | Value of the field |
| 14 | `fnd22_value` | VECTOR | 0.7234 | 7 | 5 | 特定 ESG KPI 的数值 |

**ATOM 记账**：14 个字段全部非豁免（无 country/exchange/market/sector/industry 字段），全部在批次 19 的机制设计里被覆盖或排队（本批 8 条用到 `a7 / s1 / value / a6 / a5`；`a0..a4 / a8 / a9 / as / s2` 在第二批（若发）按同一机制族轮换）。

## 2. 字段分型与机制映射（按数值行为，不按名字）

`ESG KPI` 的共同特征：**低频（年/季更新）、非负、量纲各异、向量长度不固定（一条记录一列 KPI 值）**。因此：

| 家族归属 | 字段 | 依据 | 机制 |
|---|---|---|---|
| **Change**（主） | `a7`（s1 并行） | 值型 KPI，按公司自身历史基线可算变化 | `ts_av_diff(vec_avg(x), 504|252)` — 长窗变化，ESG 评分年度修订的常见形态 |
| **Attention**（披露广度） | `fnd22_value` | 向量长度 ≈ 报告披露的 KPI 条数 | `ts_av_diff(vec_count(x), 252)` — 披露条数变化（首次披露/停止披露是 ESG 事件） |
| **Dispersion**（分歧） | `a7` | 同公司同日报多条 KPI，其离散度 = 内部 KPI 不一致度 | `vec_stddev(x)` + INDUSTRY 中性化（论坛：Fundamental→INDUSTRY） |
| **Propagation**（扩散） | `a7` | 同行业内的 KPI 分布形状随同业披露扩散而变化 | `ts_entropy(group_rank(vec_avg(x), sector), 60)` |
| **Change × 次聚合** | `a7` | 同一字段的第二种 `vec_*` 聚合（`vec_max`）验证聚合选择是否承重 | `ts_av_diff(vec_max(x), 504)` |

VECTOR 纪律：**所有字段先 `vec_*` 聚合再进标量算子**；本批用了 **4 种聚合**（`vec_avg` / `vec_count` / `vec_stddev` / `vec_max`），满足"含 VECTOR 时 ≥2 种聚合"。

## 3. 批次 19：预登记（发批前写定，事后不得放宽）

**闸线（USA/D1）**：S ≥ 1.58；F ≥ 1.0；2Y ≥ 1.58；TO ∈ [0.01, 0.70]；**SUB ≥ 0.43 × S**（平台 SUB 门槛恒为 S 的 0.43）；CW ≤ 0.1。
**prod**：只在 IS 全过后测（D0-P）；`<0.60` 正常，`0.60–0.70` 不做变体，`0.70–0.75` 只做一次结构化尝试，`≥0.75` 判死。

**本批要回答的问题（预登记，收批后逐条作答）**：
1. fnd22 的数值 KPI 是否具备**足够的截面区分力**？（匿名 ESG 分项常见"全市场同涨同跌"⇒ 壳层归一化后仍无区分）
2. `vec_count` 的披露广度变化能否独立成信号？（与 fnd21 的 `pulse` 不同，这里是**条数**而非价格反应）
3. `INDUSTRY` 中性化能否让 `vec_stddev` 分歧腿过 SUB？（fnd21 上 SUBINDUSTRY 下分歧腿 SUB/S≈0.14，属壳层问题）

**预登记判死线**：若本批 8 条**无一**满足 `S ≥ 1.40 且 F ≥ 0.85`（即连"值得改进的苗子"都不成立），则判 fnd22 **低产区**，第二批只做字段轮换（a0–a4/a8/a9/as/s2），不再追加壳层变体；若连轮换批也全灭，则按 8 统计族口径 `seal_dead_end`（需论坛 recon 闸，人工确认）。

## 4. 批次 19 回测读数

**发批记录**：A = `2pHLCkgXc54A94xPXhchvTC`（4 臂，CROWDING/decay10 为主）。
B 首轮 `2nBj7120b585aaUK5EKO65z` **整批 CANCELLED** —— 根因：`ts_entropy` 不在平台 live 算子表（103 个）里，一条坏算子连坐兄弟。
P5 改为 `ts_corr(vec_avg(a7), group_mean(vec_avg(a7), 1, sector), 252)`（行业同步性 = 传播/羊群强度；`ts_corr` 与 `group_mean` 均已在 live 表核对）后重发 B = `2wLH88cVh51U9yMvMK4RONs`，4/4 COMPLETE。

设置：USA / TOP3000 / D1 / truncation 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling ON；除注明外 neutralization = CROWDING、decay = 10；startDate 平台缺省 2014-01-01。

| 臂 | 机制 | 字段 × 算子 | alpha | S | F | 2Y | SUB | TO | 判决 |
|---|---|---|---|---|---|---|---|---|---|
| P1 | Change | `ts_av_diff(vec_avg(a7), 504)` | `58jjwPr6` | 0.48 | 0.23 | 0.76 | 0.28 | 1.80% | 三闸全灭 |
| P2 | Change | `ts_av_diff(vec_avg(s1), 504)` | `E5VVw98J` | 0.54 | 0.28 | 0.82 | 0.55 | 1.79% | 三闸全灭 |
| P3 | Attention（披露广度） | `ts_av_diff(vec_count(value), 252)` | `YPxxpREl` | 0.65 | 0.39 | 1.30 | 0.53 | 2.89% | S/F 灭，2Y 差 0.28 |
| **P4** | **Dispersion** | `vec_stddev(a7)` + INDUSTRY | `xA11xJGw` | **0.78** | **0.52** | 1.07 | 0.63 | 1.24% | **全批最强**，仍三闸灭 |
| P5' | Propagation（行业同步） | `ts_corr(vec_avg(a7), group_mean(vec_avg(a7),1,sector), 252)` | `O0JJgawp` | 0.64 | 0.36 | **1.61** | 0.68 | 2.13% | **2Y 唯一过线**，S/F 灭 |
| P6 | Change | `ts_av_diff(vec_avg(a6), 504)` | `9qEEk0Pd` | 0.57 | 0.32 | 1.02 | 0.61 | 1.85% | 三闸全灭 |
| P7 | Change | `ts_av_diff(vec_avg(a5), 252)` | `6XAANOP5` | 0.48 | 0.24 | 0.76 | 0.37 | 2.17% | 三闸全灭 |
| P8 | Change × vec_max | `ts_av_diff(vec_max(a7), 504)` | `XgRRM6PX` | 0.40 | 0.18 | 0.67 | 0.10 | 1.83% | 四闸灭（含 SUB） |

### 4.1 归因（先归因，不盲扫）

1. **收益量级不足，且被换手下限锁死 F**。全批 TO **1.24–2.89%**，远低于 Fitness 公式 `F = S·sqrt(RET / max(TO, 0.125))` 的 12.5% 地板 ⇒ `F ≈ 0.6·S`（RET 2.6–4.5%）。要让 F=1.0 配 S=0.78，RET 需 ≈ 20.5%，是现状的 5 倍。**根因是数据频率**：ESG KPI 年/季更新，`ts_av_diff(504)` 已是 2 年窗，仍只能产生 ~2% 换手。这不是壳层能修的——换任何标量算子都不改变"信息每年只变一次"。
2. **截面区分力排序恒定**：Dispersion `vec_stddev`（0.78）> 披露广度 `vec_count`（0.65）> 行业同步（0.64，但 2Y 1.61 最稳）> 水平变化（0.40–0.57）> `vec_max` 变化（0.40，SUB 崩到 0.10）。**同一公司同日报多条 KPI 的内部不一致度，是本集唯一带 >0.7 S 的结构**；水平/变化腿基本无信息（匿名 ESG 分项的"全市场同涨同跌"猜想被证实）。
3. **SUB 不是瓶颈**：除 P8（0.10）外全部 SUB/S 0.58–0.87，远高于 0.43 线；2Y 在 P5'/P3 上也能过。**卡点是 S 与 F 的绝对量级**。
4. **壳层已排除**：4 种 `vec_*` 聚合（avg / count / stddev / max）× 2 种中性化（CROWDING / INDUSTRY）落在同一量级，说明 0.8 是数据的截面区分力上限，不是归一化问题。

### 4.2 预登记判死线执行

预登记线（§3）：**无一满足 `S ≥ 1.40 且 F ≥ 0.85` ⇒ 判 fnd22 低产区**。
实测最高 S = 0.78、最高 F = 0.52，**距苗子线尚差 0.62 / 0.33** ⇒ **触发判死线**。

- 不追加壳层变体（按预登记）。
- 第二批仅做字段轮换：`a0 / a3 / a9` × 同一 Change 壳 + `a2` × Dispersion 壳（同一 `vec_stddev` 壳，属字段轮换），multisim 见 §5。
- 若轮换批仍无一达到 `S ≥ 1.0`（连"可改进"都不成立），则按 8 统计族口径走 `seal_dead_end`（需 forum recon 闸 + 人工确认，本文件只预登记、不代替闸）。

## 5. 批次 19b：字段轮换批（预登记的执行）

multisim = `4vTyMvdHu4RO8VZ3C5m9K1I`（4 臂，CROWDING / decay 10 / trunc 0.08）。
轮换字段 = 首批未覆盖的 `a0 / a3 / a9 / a2`（4 个最冷字段，aC 6/6/3/7）；壳层与首批 Change 腿完全一致，**不追加新壳**。

| 臂 | 字段 | 表达式 | alpha | S | F | 2Y | SUB | TO | 判决 |
|---|---|---|---|---|---|---|---|---|---|
| R1 | `a0` | `q(ts_av_diff(vec_avg(a0), 504))` | `vROOPZqG` | 0.65 | 0.39 | 0.74 | 0.43 | 1.95% | FAIL |
| R2 | `a3` | `q(ts_av_diff(vec_avg(a3), 504))` | `P0MMKxaE` | 0.60 | 0.33 | 0.97 | 0.49 | 1.81% | FAIL |
| R3 | `a9` | `q(ts_av_diff(vec_avg(a9), 504))` | `wp99W3xl` | 0.51 | 0.25 | 0.61 | 0.32 | 1.92% | FAIL |
| R4 | `a2` | `q(ts_av_diff(vec_avg(a2), 504))` | `RRAAP9Qo` | 0.67 | 0.39 | 1.26 | 0.60 | 1.77% | FAIL |

> 注：原 P4 的 Dispersion 壳（`vec_stddev` + INDUSTRY）本轮**未**用于 a2，以保持"只换字段"的批次纯度；若 R1–R4 全部低于 S 1.0 即直接判死，不再补 dispersion 轮换。

### 5.1 轮换批归因与终判

- **读数形状与首批同构**：S 0.51–0.67、F 0.25–0.39、TO 1.77–1.95%（仍在 12.5% 地板下方）。R4 的 2Y 1.26 / SUB 0.60 是 12 臂里最好的尾部读数，但 S 仍只有 0.67。
- **归因**：换字段（4 个最冷字段）后 S 波动仅 0.51–0.67，与首批 0.40–0.78 完全重叠 ⇒ **差异来自字段噪声，不来自字段选择**。真正的约束是**数据节奏**：ESG 年/季更新使 `ts_av_diff(…,504)` 的换手天然落在 2%，Fitness 被 `F = S·sqrt(RET/0.125)` 当场封顶（S 0.67 ⇒ F 上限 ≈0.67）。
- **壳层不是瓶颈**：首批已用 4 种 `vec_*` 聚合 × 2 种中性化（SUBINDUSTRY / CROWDING）× 3 种机制族（Change / Attention / Dispersion），读数全部落在 S<0.8 的同一带内。
- **终判（按预登记执行）**：12 臂（8 + 4）**无一**达到 `S ≥ 1.0`，轮换批判死条件成立 ⇒ `fnd22` 判 **low-yield 数据集，不再投入仿真**。`seal_dead_end` 的论坛 recon 闸 + 人工确认**未执行**，本文件只作预登记结论，不代替封存闸。
- **可复用结论**：VECTOR 型匿名 ESG/KPI 数据在 USA/D1 上**结构性不适配 Fitness 闸**——除非能在同一字段上做出 >10% 换手的机制（例如把年频披露差分成事件型），否则 `ts_av_diff` 长窗族一律先算 `F ≤ S` 上限再决定是否发批，避免 12 条仿真的沉没成本。
