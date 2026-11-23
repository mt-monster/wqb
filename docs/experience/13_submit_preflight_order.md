# 13 · 提交前预检清单与闸门排序（2026-11-21 定型 / 2026-11-22 v2 增补经济账）

> 缘起：用户问「梳理一下提交前的检查项，合理排序各闸门的前后顺序，特别注意新增的 VF 闸和六维影响的关系」。
> 本文是**唯一权威排序**，替代散落在 `01_platform_gates.md` §5/§17/§18 的零散描述。
> 相关：`01_platform_gates.md`（阈值细节）｜`12_reg_tuning_playbook.md`（精调）｜`tools/gates/vf_impact_gate.py`｜`tools/gates/sa_submit_gate.py`｜`tools/super/genius_tiebreak.py`

> ⚠ **本文只覆盖 REGULAR。SUPER 走另一条链**（2026-11-22 起）：`tools/gates/sa_submit_gate.py`（base 档位+池增益，铁律 16）+ `tools/super/sa_grade.py`（准入分级）+ 配额 SUPER 1/日。
> **两链不重叠**：② `VF/多样性分` 这一本账对 SA **没有对象**——`value_factor_trendScore` 只统计 REGULAR，SA 不进 N/A/P。把 SA 塞进本文的九阶段会白跑 VF 闸且误判。

---

## 0 核心认知：一次提交要付**五本互相正交的账**

很多人把「提交前检查」当成一张平铺的 checklist，导致顺序错乱（先跑贵的、后跑便宜的）、或者把两类完全不同的问题混为一谈。正确的模型是：**每交一颗，同时在五个独立账本上记账**。

| 账本 | 度量 | 谁决定方向 | 是闸还是排序键 | 可否事后补救 |
|---|---|---|---|---|
| **① 配额** | 当日 REGULAR 4 / SUPER 1 | ET 日界，不可回收 | **硬闸**（用完就没） | ❌ 不可 |
| **② VF / 多样性分** | `(A/N)×(P/216)×S_H` | **ΔP**（是否新开 pyramid 类别） | **硬闸**（BLOCK 退出码 3） | ❌ 不可（提交即污染） |
| **③ Genius 六维** | T1/T2 降、T3/T4 升 | **distinct 算子数 / 字段数** | **排序键**（不阻断） | ❌ 不可（分母 N 永久 +1） |
| **④ 组合边际贡献** | ΔS/ΔF/ΔRet/ΔTO/ΔDD | `performance_comparison` | **硬闸**（方案 D v2 L1/L2） | ❌ 不可 |
| **⑤ 经济账（VF 值 + base 值）** | `diversity_score` before→after；日 base before→after | ΔP ＋ 当日提交数 ＋ 水平锚 | **汇报硬要求**（用户 11-22 明令） | ❌ 不可（已污染/已结算） |

**关键：②③④⑤ 互不覆盖。** 过 VF 闸 ≠ 六维好 ≠ 边际贡献正 ≠ 经济账好看。四本账必须分别算，缺一本就是漏检。

### 0.1 第⑤本账怎么算（2026-11-22 定稿，唯一标准）

```bash
python tools/gates/base_forecast.py --date <ET日期> --report      # 或用 --alpha id1,id2
```
输出即可直接粘贴的「四数」块：

```
VF:   <before> → <after>（+x%）  N ..→..  A ..→..  P ..→..  ΔP=+k [新类别]
      valueFactor <v>（提交当天不变，平台按季更新）
base: 当日 n-1 颗 $X → n 颗 $Y（+$Z/天, +w%）
      锚定：$A × +w% ⇒ $B（+$D/天）
      单件 <id> $M | 乘数 (theme+pyr−1)×(1+OS) = T
```

三条口径铁律：
1. **VF 只认 `diversity_score` 的 before→after**（`(A/N)×(P/216)×S_H`）；`valueFactor` 本体按季更新，**当天不会变**——必须写明"不变"，否则读者会以为它动了。
2. **base 的绝对水平用锚，模型只出 Δ**：`日 base(提交后) = 最近5个有付日中位 × exp(β·Δf)`。
   纯模型绝对水平会因 OS/VF 跳档整体偏低（11-20 实测偏差 −37%）。
3. **乘数链逐项写出** `(theme + pyramid − 1) × (1 + OsmosisRank)`，三项都要有来源（平台字段）。
   单件 base 只用于排序，不当承诺。

---

## 1 四条排序原则

### 原则 1 — 零成本预判先行（fail fast）
配额、字段存在性、`ra_failed`、指标四闸、**ΔP、ΔT1** 全部可以用**已有数据或一次 `get_alpha_details` 免费拿到**。
这些一旦不过，后面的贵接口全是浪费。⇒ **永远先跑免费层。**

### 原则 2 — 能算的不要真跑
- **ΔP** 不用跑完整 VF 闸：`get_alpha_details().pyramids.list` 与当前在册类别集一比即知。
- **ΔT1/T2** 不用跑完整 `genius_tiebreak`：公式是闭式的（见 §3）。
这两项让「值不值得往下走」在**零网络成本**下就能判。

### 原则 3 — 贵的合并跑
`prod_corr` 是**相关性闸 + VF 闸**的共同依赖。跑一次 `check_correlation`，结果同时喂给两处。
`value_factor_trendScore` 同类。**禁止为同一个数跑两遍。**

### 原则 4 — 不可逆动作垫底
`set_alpha_properties`（全量覆盖接口，曾清空 115 颗 name）与 `workflow_submit_alpha(confirm_submit=True)`（**不可逆**，须用户确认）放最后一步。
**提交前的所有检查都不应触碰这两个接口。**

---

## 2 九阶段清单（按此顺序执行，前序不过即停）

### Stage 0 · 决策前置（零成本，纯读）

| # | 检查 | 判据 | 不过怎么办 |
|---|---|---|---|
| 0.1 | ET 日配额 | `quota_status.py` 首行；REGULAR<4 且 SUPER<1 | 等 ET 00:00 重置 |
| 0.2 | 类型与状态 | REGULAR / SUPER；`status=UNSUBMITTED`、`stage=IS` | PPA 一律排除（只认 RA） |
| 0.3 | **ΔP 预判** | `pyramids.list` 有无当季未出现的类别 | 记下 ΔP，喂给 Stage 6 |
| 0.4 | **ΔT1/ΔT2 预判** | 见 §3 闭式公式 | 记下，喂给 Stage 7 |

> ⚠ 0.3/0.4 是**预判不是裁决**。它们的作用是：让 5 颗候选在花任何网络成本前就能排出先后。

---

### Stage 1 · 表达式与结构（零成本）

| # | 检查 | 判据 | 备注 |
|---|---|---|---|
| 1.1 | `preflight_expressions` | `unknown_fields=[]` | ⚠ **不解析多语句**（变量名报 unknown），多语句件直接用仿真验证 |
| 1.2 | 算子数三口径 | `regular.operatorCount`=次数｜**T1/T3=distinct 且排除 backfill**｜PPA ≤8 | REGULAR 提交**无算子闸**，此项仅为六维 |
| 1.3 | 混腿形态 | 禁 `add(rank(A),rank(B))`；`multiply(rank,rank)` 会压向 0 侧损失排序 | 同形态仅窗差、`add(abs(x),0.01)` 放行 |
| 1.4 | 变量抽取 | 重复子式双倍计数；`a=...; <末行>` 赋值不计数 | 多语句平台接受，指标逐位不变 |

---

### Stage 2 · 性能硬闸（零网络，读已有仿真结果）

| # | 检查 | 判据 | 失效方式 |
|---|---|---|---|
| 2.1 | `LOW_SHARPE` | ≥ **1.58**（交付线，平台硬线 1.25 不可顶替） | fail |
| 2.2 | `LOW_FITNESS` | ≥ **1.0**（平台）｜**> 2.0**（VF 基础门槛） | WARNING / fail |
| 2.3 | 2Y / `IS_LADDER_SHARPE` | ≥ **1.58** | WARNING 视同 FAIL |
| 2.4 | `LOW_SUB_UNIVERSE_SHARPE` | **比值闸** sub/S ≥ **0.521** | fail |
| 2.5 | `CONCENTRATED_WEIGHT` | ≤ **0.1** | fail |
| 2.6 | `HIGH_TURNOVER` | 上限**区域特异**（GBR/D1=0.7，他区以平台返回 limit 为准） | fail |
| 2.7 | `investability_sharpe` | 硬闸仅 **ASI/JPN/HKG/TWN/KOR**；其余区 >0 即可 | fail |
| 2.8 | 生命周期 | S/2Y > **2.0** ⇒ 判死（<1.3 可救） | 判死 |
| 2.9 | `CLUSTER_TEST` | **阈值按区**（EUR limit 1.58、GBR 1.0）⇒ 读 `result` 字段不看数值 | WARNING |

> ★ **2026-11-23 补（RA 质量线，论坛实证）**：`fitness>2.0` 已写在 2.2；再补两条软判据——
> **margin > 万分之十（10bp）**（低于此赚不回手续费；新手常忽略）＋ **PnL 逐年平滑**（无平年/无暴跌年）。
> base 过关线可作快速体检：1 件 $1.5｜2 件 $1.7｜3 件 $1.85｜4 件 $2.0，低于此说明质量不过关、会拉低 VF。
> 这两条是**软判据**（影响排序与 VF，不直接 fail），与 §Stage 5 边际论配套。

---

### Stage 3 · RA 裁决（零成本，但必须 fail-closed）

| # | 检查 | 判据 |
|---|---|---|
| 3.1 | `ra_failed` | **必须为 false**。`true` ⇒ 直接排除，不是「披露即可」 |
| 3.2 | `ra_failed_checks` | 逐条读，区分「可调参修复」与「形态死」 |

> **这是最高性价比的一步**：一次 `get_alpha_details` 就能判死。`E56YX80G` 就是在这里出局的（CONCENTRATED_WEIGHT + LOW_SUB_UNIVERSE_SHARPE 双 fail）。

---

### Stage 4 · 相关性（首次触网，单并发槽，贵）

| # | 检查 | 判据 | 成本 |
|---|---|---|---|
| 4.1 | `check_self_correlation` | max < **0.7**（软线 0.55 是另一口径，勿混） | 本地计算，免费 |
| 4.2 | `check_correlation` | max prod < **0.7** | **~4 分钟，账号单并发** |
| 4.3 | `compute_mutual_correlation` | 与已提交件逐对 < 0.7（实操 < 0.5 更安全） | 本地，免费 |

**要点**：
- `get_alpha_details.metrics.selfCorrelation`（回填，软线 .55）**≠** `check_self_correlation`。报 self 必注来源。
- 当日有提交时快筛可能假低，**必用 `compute_mutual_correlation` 复核**。
- 48h 内 prod 缓存可直接过闸（节点内 `check_correlation(refresh=False)`）；**提交前那次独立 `refresh=True` 是冗余动作**，会抢同一单并发槽。
- `correlation_busy` 多为他人占槽，**不是本任务失败，勿反复重试**。

**产出**：`prod_corr` 同时喂给 Stage 6。

---

### Stage 5 · 组合边际贡献（网络）

> ★★★ **2026-11-23 定案：本阶段是「首要判据」，不是九阶段中普通的一环**（论坛实证：
> fit 1.03/self .1 提升地区组合 ＞ fit 1.98/self .68 降低组合；VF 由过去 3 个月各地区组合等权评定）。
> **看边际不看单件绝对** —— 单件 S/F 再高，若拉低所在地区组合，VF 受损，优先级高于档位/乘数。
> `sa_submit_gate.py --perf-comp-delta <0` 已把此判据前置为 REDLINE 之后的第一道闸。

| # | 检查 | 判据（方案 D v2 严格档） |
|---|---|---|
| 5.1 | `performance_comparison` | **L0 死区** `\|ΔS\|≤.02 ∧ \|ΔF\|≤.02 ∧ \|ΔRet\|≤.3pp` ⇒ neutral 放行 |
| 5.2 | 同上 | **L1 净效果** `ΔS<−.05 ∨ ΔF<−.05` ⇒ 硬拦 `net_block` |
| 5.3 | 同上 | **L2 配对** `ΔRet≤−.5pp ∧ (ΔTO≥+1.5pp ∨ ΔDD≥+.5pp)` ⇒ 硬拦 `pair_block` |
| 5.4 | 同上 | **L3** ΔTO/ΔDD 单独变差 ⇒ 仅 `soft_warnings` |

> ⚠ **预筛只预警不判死**，必回源 `performance_comparison` 原表。
> ⚠ **不设「点亮塔」豁免通道** —— 点塔只作排序键，不进闸门。

---

### Stage 6 · VF 闸（网络 × 3，40–60s）

```bash
python tools/gates/vf_impact_gate.py --alpha <id> --prod-corr <pc> [--fitness <f>]
```

| 退出码 | 判定 | 处置 |
|---|---|---|
| **0** | PASS（ΔP≥1） | 放行 |
| **1** | WARN（ΔP=0 但拖累<2） | 放行，**必须在提交描述中披露** |
| **3** | **BLOCK**（同质加厚 ∧ 拖累≥2） | **硬拦，不放行** |
| **4** | **UNDETERMINED**（PC/F 缺失） | **等同阻塞**，补数后重跑 |

**三层结构**：
- **L0 当期影响** —— `os is None` ⇒ 当期 VF 影响=0（事实陈述，不作拦截依据）
- **L1 多样性** —— `ΔP≥1` 必升（`(P+1)/P × N/(N+1) > 1`）；`ΔP=0` 至多持平，A 不增则必降 `N/(N+1)` ≈ **−1.27%**
- **L2 三拖累** —— ① (Region,Delay) 提交数 <10 ② 近3年/全期 S 比 <0.85 或 CV>0.5 或有平年 ③ **F<2.0 ∧ PC>0.65**

**硬拦规则**：`同质加厚（ΔP=0 ∧ 该类≥3）∧ L2 命中≥2` ⇒ BLOCK。
单颗高质件即使同质也不拦（拦了反损失 base）。

**边界（必须如实说）**：VF 本体由 OS 表现 + 与自己池差异 + 与他人差异决定，**提交前不可精确测得**。本闸只判可预测的多样性方向 + 拖累组合，**不能假装拦得住 VF 全貌**。

---

### Stage 7 · 六维完整核算（排序键，不是闸）

```bash
# 必须用 MCP 的 venv 跑（根环境缺 pydantic）
./world-quant-brain-mcp/.venv/Scripts/python.exe tools/super/genius_tiebreak.py \
    --compute --alphas <id1>,<id2>
```

| 维 | 方向 | 候选评估是否相关 |
|---|---|---|
| T1 avg distinct Operators / Alpha | **越低越好** | ✅ 必算 |
| T2 avg distinct Fields / Alpha | **越低越好** | ✅ 必算 |
| T3 Total distinct Operators | 越高越好 | ✅ 必算 |
| T4 Total distinct Fields | 越高越好 | ✅ 必算 |
| T5 Max Simulation Streak | 越高越好 | ❌ 靠每日仿真，与选件无关 |
| T6 Community leader | 越高越好 | ❌ 靠论坛/推荐，与选件无关 |

**用法**：当**多颗候选都已过 Stage 0–6**，用六维排名和做最终排序。**六维不阻断任何件。**

> ⚠ **六维基线滞后**：报 T4 前先扣当日已提交件用过的字段。
> ⚠ **六维窗口＝当季、每季重置**（Q4 面板真值 N=141：T1 5.73｜T2 2.07｜T3 54｜T4 227）。

---

### Stage 8 · 稳健性审计（半自动，fail-closed）

| # | 检查 | 判据 |
|---|---|---|
| 8.1 | `robustness_<id>` | 必须有**真审计**记录，缺失即阻塞 |
| 8.2 | 逐年稳定性 | 平年（S≤0）、CV>0.5、近3年衰减比 <0.85 需在描述中说明 |

---

### Stage 9 · 提交合规（不可逆前最后一道）

| # | 检查 | 判据 |
|---|---|---|
| 9.1 | 配额复核 | 提交瞬间再读一次（防跨进程抢占） |
| 9.2 | `description` | 三段式 `Idea:` / `Rationale for data used:` / `Rationale for operators used:`，**≤100 词英文**，`

` 分隔；**空描述会被平台静默丢弃**（201 但被丢） |
| 9.3 | `name` | 预先写好 |
| 9.4 | 属性接口 | REGULAR 用 `set_alpha_properties`；**SUPER 必须裸 PATCH**（前者对 SUPER 必 400） |
| 9.5 | **经济账四数就绪** | `base_forecast.py --report` 出块：VF 前后 / valueFactor / base 前后 / 单件乘数（**缺一不算汇报**） |
| 9.6 | 提交 | `workflow_submit_alpha(confirm_submit=True)`（**不可逆**，用户确认后） |

> ⚠ `set_alpha_properties` 是**全量覆盖**不是局部更新。改单个属性用最小字段 PATCH `{"tags":[...]}`，改前先 dump 快照。

### Stage 10 · 提交后（POST 之后必做，2026-11-22 血泪）

| # | 动作 | 原因 |
|---|---|---|
| 10.1 | **重设属性** `set_alpha_properties(name, color, tags, descriptions)` | `workflow_submit_alpha` 内部按 `build_name` **重算 name 并清空 tags**（实测 `KOR_R_instbrd_01` → `KOR_R_alpha_01`、tags 归零）。**POST 前设过一次也没用，节点会全量覆盖。** |
| 10.2 | 复核 `stage=OS / status=ACTIVE / dateSubmitted` | 201 是 async，需等 verify |
| 10.3 | 回填台账 | `tracking/SA_BASE/base_daily.jsonl` 补当日；`robustness_<id>` 已写 |
| 10.4 | **回执四数** | 把 Stage 9.5 的块发给用户（提交前预告 + 提交后回执各一次） |

---

## 3 ★★ VF 闸与六维的关系（本文重点）

### 3.1 它们是**完全正交**的两套判据

| | VF 闸 | 六维 |
|---|---|---|
| 看什么 | **pyramid 类别**（A/N/P/S_H） | **distinct 算子数 / 字段数** |
| 输入 | pyramids、F、PC、逐年 S | 表达式骨架、字段清单 |
| 性质 | **硬闸**（可 BLOCK） | **排序键**（不阻断） |
| L2 三条件 | 全是**表现指标**（样本数/衰减/F·PC） | 全是**结构指标**（ops/fields） |
| 结论 | 让全局乘数不降 | 让 Genius 同档排名升 |

⇒ **过 VF 闸不等于六维好，六维好也不保证过 VF 闸。两者必须分别算。**

### 3.2 但它们有一个**结构性张力**

- **开新塔（ΔP≥1）通常需要新数据集** ⇒ 新字段进 T4（好），同时推高 T2 均值（坏）
- **六维最省的件（少算子少字段）通常是窗口调参件** ⇒ ΔP=0 ⇒ **多样性分必降 1.27%**

⇒ **"VF 要的多而新" 与 "T1/T2 要的少而精" 天然拉扯。**

### 3.3 唯一同时讨好两者的形态

**用「已用过的算子」+「少量全新字段」+「开新塔」**：

- T3 **flat**（不新增算子 ⇒ T1 只受分母 N+1 拖累，代价最小）
- T4 **+n**（新字段刷总量）
- ΔP = **1**（多样性分必升）

**实证（2026-11-21 实测，Q4 基线 T1=5.7214 / T2=2.0857 / N=140）**：

| alpha | distinct ops | distinct fields | ΔT1 | ΔT2 | ΔT3 | ΔT4 | ΔP | VF 判定 |
|---|---:|---:|---:|---:|---|---:|---:|---|
| **`kqNb1g5d`** | **7**（全已用） | **4**（全新） | **+0.0091** | **+0.0136** | flat | **+4** | **+1** | **PASS** |
| `9qxLOPxr` | **9**（全已用） | 3（全新） | **+0.0233** | +0.0065 | flat | +3 | +1 | WARN |

⇒ **`kqNb1g5d` 在 VF 与六维两条线同时压制 `9qxLOPxr`**：六维代价只有 39%（ΔT1 0.0091 vs 0.0233）、T4 收益更大（+4 vs +3）、且 VF 是 PASS 而非 WARN。**这就是它该排第一的硬依据，不是感觉。**

### 3.4 零成本闭式公式（Stage 0.4 用）

```
ΔT1 = (distinct_ops − 当季 T1 均值) / (N_当季 + 1)
ΔT2 = (distinct_fields − 当季 T2 均值) / (N_当季 + 1)
```

Q4 当前 N=140 ⇒ 分母 141：

| distinct ops | ΔT1 | 解读 |
|---:|---:|---|
| 4 | **−0.0122** | **T1 改善**（唯一能降 T1 的区间） |
| 6 | +0.0020 | 几乎无损 |
| 7 | +0.0091 | 可接受 |
| 9 | +0.0233 | 明显代价 |
| 13 | +0.0516 | 昂贵 |

⇒ **ops < 5.73 是唯一能让 T1 变好的区间。** 季初第一颗用低 ops 件铺底能拉低整季起点。

### 3.5 一条必须记住的边界

**六维不是"加分项"，是"同档超额时的排序键"**。Genius 等级由「三项 eligibility 达标者之间的六维排名和」决定。
⇒ 六维差**不会**让你被拒，只会让你在同档竞争里排在后面。**所以它排不进硬闸序列，只能当 Stage 7 的排序依据。**

---

## 4 一页速查（打印版）

```
Stage 0  配额 / 类型 / ΔP预判 / ΔT1预判        零成本     不过即停
Stage 1  preflight / 算子三口径 / 混腿形态      零成本     修表达式
Stage 2  S·F·2Y·SUB·CW·TO·invest·生命周期      零成本     判死
Stage 3  ra_failed                             零成本     判死 ← 最高性价比
──────────────────────── 以下开始花网络成本 ────────────────────────
Stage 4  self / prod / mutual                  单并发槽   prod 喂 Stage 6
Stage 5  performance_comparison（方案D v2）     网络       neut/pass/block
Stage 6  vf_impact_gate                        40-60s     PASS/WARN/BLOCK/UNDET
Stage 7  genius_tiebreak                       网络+本地  仅排序，不阻断
Stage 8  robustness                           半自动     缺失即阻塞
──────────────────────── 以下不可逆 ────────────────────────
Stage 9  配额复核 / description / name / 经济账四数 / POST  —   提交
──────────────────────── 以下 POST 之后 ────────────────────────
Stage 10 重设属性(name/tags 会被节点覆盖) / 复核 ACTIVE / 回执四数
```

**派发纪律**：`create_multi_simulation` **≤4 臂/批**。≥5 臂在本账号并发下可能永久排队
（2026-11-22 实测：10 臂被 429；5 臂卡 `progress=0.35` 1.5h 未展开；拆 2/4/2 全部正常回收）。

**三句话总结**：
1. **免费的先跑完，再碰网络** —— Stage 0–3 能筛掉 70% 的件，全部零成本。
2. **VF 闸判「乘数会不会降」，六维判「同档排名会不会掉」，两张卷子分开答**，谁也不能替谁。
3. **唯一双赢形态 = 已用算子 + 少量新字段 + 开新塔**（T3 flat、T4 升、ΔP=1）。
4. **经济账不是判断题而是汇报题**：`--report` 出四数，缺一行都算没汇报（用户 11-22 明令）。
