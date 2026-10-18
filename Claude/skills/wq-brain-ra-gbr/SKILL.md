---
name: wq-brain-ra-gbr
description: "在 GBR 区挖 REGULAR alpha、调 GBR 的回测设置或阈值、查 GBR 某类数据集（区域 × 类别组合）的配方与禁区时使用：GBR 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。"
layer: L-RA-R
allowed-tools:
  - Read
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "1.1"
last_verified: 2026-10-09
---

# GBR 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：GBR 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 GBR 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 GBR，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

0. **先读方法论主文** `docs/reference/field_profile_to_alpha_playbook.md`（七层链路：选区域 → 选字段族 → 开批前三闸 → 信号构造 → **结构维度** → 参数微调 → 闸门判定 → 闭环回填）。**七层是「想什么」，九步是「怎么做」**；本区落地映射见下面「字段画像驱动流程」。
1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region GBR --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region GBR --apply
   $WQ_PY -m wqb.profiles render --region GBR --apply
   ```

<!-- region-scaffold:nav:start -->
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **GBR 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/GBR/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/GBR/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->

## 区域控制面板

<!-- profiles:region-panel:start -->
**入场状态**：`active`　达成区扩挖：4 ACTIVE（全闸过 2 + rn 弱 2）+ 白名单 10 数据集（8-26 建），目标累计 10 → 再挖 6

| 回测设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | settings.json |
| region | GBR | settings.json |
| universe | TOP700 | settings.json |
| delay | 1 | settings.json |
| neutralization | SUBINDUSTRY | settings.json |
| decay | 4 | settings.json |
| truncation | 0.08 | settings.json |
| maxTrade | ON | settings.json |
| pasteurization | ON | settings.json |
| unitHandling | VERIFY | settings.json |
| nanHandling | ON | settings.json |
| language | FASTEXPR | settings.json |
| visualization | false | settings.json |
| startDate | 2014-01-01 | settings.json |
| endDate | 2023-12-31 | settings.json |

| 阈值 | 值 | 来源 |
|---|---|---|
| Mode B 主闸（sharpe / fitness） | 1.25 / 0.8 | default（实时值含区域台账，看 explain） |
| review.sharpe_min | 1.58 | thresholds.json |
| review.fitness_min | 1.0 | thresholds.json |
| review.turnover_min | 0.05 | thresholds.json |
| review.turnover_max | 0.3 | thresholds.json |
| review.two_year_sharpe_min | 1.6 | thresholds.json |
| near.sharpe_min | 1.2 | thresholds.json |
| diversity.signal_floor.max_sharpe_floor | 0.5 | thresholds.json |

**循环与闸门（profile front-matter）**
- 每波探针位上限：2
- 快判死：缺省（决策表 D15：新数据集 8 探针无 ／S／≥0.5 即判死）；本区无额外规则
- 停止条件：白名单被 dead_end 全覆盖
- 闸门特化（文档级）：cw_gate=WARN——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责

**平台事实**
- 宇宙是单一国家（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组等于全市场，别用
<!-- profiles:region-panel:end -->

## 组合分支（区域 × 类别）

<!-- profiles:cells-index:start -->
| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |
|---|---|---|---|---|---|---|---|---|
| model | MODEL | active | — | — | 283 / 23 | 18（9） | 13 / 1 | [references/model.md](references/model.md) |
| fundamental | Fundamental | active | — | — | 89 / 0 | 0（0） | 3 / 0 | [references/fundamental.md](references/fundamental.md) |
| institutions | Institutions | active | — | — | 88 / 0 | 0（0） | 2 / 0 | [references/institutions.md](references/institutions.md) |
| analyst | Analyst | active | — | — | 63 / 0 | 0（0） | 5 / 0 | [references/analyst.md](references/analyst.md) |
| pv | PV | active | — | — | 63 / 0 | 1（1） | 3 / 0 | [references/pv.md](references/pv.md) |
| news | News-Sentiment | active | — | — | 56 / 0 | 0（0） | 5 / 0 | [references/news.md](references/news.md) |
| other | Other | active | — | — | 54 / 0 | 0（0） | 4 / 0 | [references/other.md](references/other.md) |
| sentiment | News-Sentiment | active | — | — | 43 / 0 | 0（0） | 2 / 0 | [references/sentiment.md](references/sentiment.md) |
| shortinterest | ShortInterest | active | — | — | 21 / 0 | 0（0） | 1 / 0 | [references/shortinterest.md](references/shortinterest.md) |
| insiders | Insider | active | — | — | 18 / 0 | 0（0） | 1 / 0 | [references/insiders.md](references/insiders.md) |
| option | Option | active | — | — | 15 / 0 | 0（0） | 1 / 0 | [references/option.md](references/option.md) |
| earnings | Earnings | active | — | — | 14 / 0 | 0（0） | 1 / 0 | [references/earnings.md](references/earnings.md) |
| macro | Other | active | — | — | 11 / 0 | 0（0） | 1 / 0 | [references/macro.md](references/macro.md) |
| risk | Risk | active | — | — | 0 / 0 | 0（0） | 1 / 0 | [references/risk.md](references/risk.md) |

说明：5 条判死 / 胜绩连类别也推断不出；证据于 2026-10-04 只读汇总。
<!-- profiles:cells-index:end -->

## 字段画像驱动流程（Playbook 七层链路 → 九步映射）

> **方法论主文**：`docs/reference/field_profile_to_alpha_playbook.md`（跨区域通用；本区只写差异）。
> 读法：**先按本表定位当前在哪一层，再走九步** —— 七层是「想什么」，九步是「怎么做」，画像回填让两者复利。

| Playbook 层 | 核心动作 | 九步 | GBR 落地 |
|---|---|---|---|
| **0 选区域** | 画像 `ALIVE` 数 + 未测池规模定优先级 | 步 1 | `$WQ_PY tools/fields/field_profile.py --list`（GBR：1.55 万字段 / 285 已测 / 2578 未测 / **49 ALIVE + 34 WEAK** / 465 判死） |
| **1 选字段族** | 九类 verdict 处置 + ★跨区对照 | 步 2 / 3 | `$WQ_PY tools/fields/field_profile.py --query --region GBR --verdict ALIVE` |
| **2 开批前三闸** | 值型 / 元数 / 算子实集合 / **字段存在性** | 步 5 | `_lint_expr_values` ＋ `op_arity.ensure_safe_for_dispatch` ＋ `dispatch` 内置 `op-lint` / `field-type-lint` ＋ `validate_expressions` |
| **3 信号构造** | 禁混信号；**5 放行形态用满** | 步 4 | 见下「合规模板」 |
| **4 结构维度** ★ | 合成模板 / 外层算子 / 残差化轴 / 分组粒度 | 步 4 / 7 | ★ **最大杠杆 —— 先扫结构，再扫参数** |
| **5 参数微调** | 窗长 / gran / decay / 中性化档 | 步 7 | 必须在结构确定**之后**（换结构后参数最优会漂移） |
| **6 闸门判定** | IS 闸 ＋ `submit_verdict` ＋ **prod/self 双端点** | 步 7 / 8 | 见下「判定口径」 |
| **7 闭环回填** | 画像复利 | 步 9 | `$WQ_PY tools/fields/field_profile.py --build --region GBR` |

> 本区基线快照（ALIVE/WEAK 字段全表 + 各类 verdict 分布 + 战役目标）见 [`references/_field-profile-playbook.md`](references/_field-profile-playbook.md)。

### 第 1 层 · verdict 九类处置表

| verdict | 判据 | 处置 | GBR 规模 |
|---|---|---|---|
| `UNUSABLE` | `coverage < 0.6` | **永久剔除** | ANALYST 1742 / MODEL 4071 / OTHER 1930 / PV 1412 |
| `AXIS_ONLY` | `ftype == GROUP` | **只能当分组轴**，不进信号白名单 | OTHER 1200 / PV 190 |
| `UNTESTED` | 过前两关且 `n_tests == 0` | 可探（按机制族排优先级） | **2578**（MODEL 1160 / PV 537 / ANALYST 474 / OTHER 365 …） |
| **`ALIVE`** | 单信号 `S ≥ 1.58` | **过闸线 ⇒ 直接可做** | **49**（MODEL 14 / ANALYST 16 / PV 3 …） |
| `WEAK` | 单信号 `S ≥ 1.10` | **有信号但不够强 ⇒ 优先深挖** | **34** |
| `DEAD` | 已测 `S < 1.10` | 不再投入 | **465** |
| **`DEAD_STATIC`** | `to_med < 0.03` | **静态属性，任何骨架都无用** | 32 |
| **`DEAD_TURNOVER`** | `to_med > 0.70` | **被 HIGH_TURNOVER 闸直接拒** | NEWS 6 / MODEL 2 / PV 1 |
| **`DEAD_COUNT`** | 名字含 `num/count` 且 2Y≥1.3 且 S≤0.7 | **「2Y 有 S 无」判死形态** | INSTITUTIONS 3 |

### 第 1 层 · ★ 跨区对照（最强的筛字段手段）

**规则**：同机制在某区 `ALIVE`、在另一区未测 ⇒ **优先在对它有效的区做，或回本区补测那个「形式」**。
- **形式 > 机制**：EUR 的 `predicted_surprise_pct_*` ALIVE（S2.09），DEU 只测过绝对版（0.74）⇒ DEU 的 34 个 pct 变体未测 = **被误判的机制**。
- **同机制跨区可反向**：`shortinterest` 在 KOR ALIVE（S2.35）、在 DEU 族级否证。
- **⚠ 高 S 陷阱**：`*_label*` / `*_bucket*`（分位数 / 概率桶标签）**不是信号** ⇒ **开批前必核 `fields.description`**。
- **字段名骗人**：`iv_projected_*` 实为 DPS 预测；`liquidity_money_flow_alignment` 实为 Relative Turnover；**后缀判类型会翻车**（`_tribes` 有 MATRIX 也有 VECTOR）⇒ 以 `get_datafields` 的 `type` 为准。

### 第 3 层 · 合规模板（5 放行形态，必须用满）

| 形态 | 示例 | 经济含义 |
|---|---|---|
| `add`（双窗） | `add(ts_mean(F,1), ts_mean(F,120))` | 快慢双窗：短期变化 + 中期水平 |
| `divide` | `divide(A, B)` | 信息比率 / 标准化 |
| `subtract(rank,rank)` | `subtract(rank(A), rank(B))` | 相对强弱 / **行业内相对** |
| `if_else` / `trade_when` | `trade_when(cond, sig, -1)` | 事件门控 / 条件筛选 |
| `group_rank` / `group_zscore` | `group_zscore(x, group)` | 组内标准化（非保序 ⇒ 独立杠杆） |

**算子数 < 10**（超了判复杂）；**禁止两条独立信号腿相加**（加权 / 等权 / `add` / 中缀 `+` 一律违规）。

### 第 4 层 · ★★ 结构维度 > 参数维度（本区与 DEU 的共同铁律）

**GBR 实证**：`ts_arg_max`（时效量纲）、`group_neutralize` **施加在原始信号上**（而非加工后）、`残差化 × 平滑` 串联 —— 三者都是**结构级**发现；而「保序变换 / `truncation` / 模拟层 `decay` / `nanHandling`」这类**参数级**动作在本区全灭。
**⇒ 纪律：卡住时先问「结构维度扫过没有」，再问「参数扫过没有」。**

结构维度清单（每项独立杠杆）：

| 维度 | 扫描范围 | GBR 结论 |
|---|---|---|
| **合成模板** | 双窗 / 差值 / 比率 / 行业内相对 / 门控 | 「行业内相对」与「残差化 × 平滑」是最大单次增益 |
| **外层算子** | `rank` / `ts_decay_linear` / `signed_power` / `group_zscore` / `winsorize` / `ts_rank` | `ts_decay_linear` 有效（不牺牲 TO）；`signed_power` 给 2Y 但压 S |
| **算子作用位置** ★ | `group_neutralize` 施于**原始信号** vs **加工后** | 顺序决定 2Y 过 / 不过（1.71 vs 1.57） |
| **残差化轴** | `vector_neut(SIG, rank(axis))` | GBR 实测偏弱，但是「改持仓」类杠杆，值得按族试 |
| **分组轴粒度** | `subindustry` / `industry` / `sector` / 统计聚类 | **轴越细 S 越高、PROD 也越高** ⇒ 核心取舍 |
| **换量纲** | `ts_delta` / `ts_rank` / `ts_arg_max` / `ts_returns` / `ts_max_diff` | **族特异极强**（M1 有效、M2 毁灭）⇒ 严禁跨集外推 |
| **算子叠加** | `signed_power(ts_decay_linear(...))` | **叠加无效**（2Y 反降）⇒ 单算子最优 |

### 第 6 层 · 判定口径（GBR 版）

1. **IS 层**：`LOW_SHARPE ≥ 1.58` ｜ `LOW_FITNESS ≥ 1.0` ｜ `TO ∈ [0.03, 0.70]` ｜ `sub ≥ 0.78` ｜ `CLUSTER_TEST ≥ 1` ｜ `LOW_2Y_SHARPE ≥ 1.58`（数值随 delay/区域浮动，权威见 config.PLATFORM_CHECK_LINES）。
   **★ 平台把 ladder 四舍五入到 2 位再严格比较 ⇒ 真值须 ≥ limit + 0.005。**
2. **`submit_verdict`**：唯一否决权威（只能拦不能放）；`UNVERIFIABLE_404` = 处女提交的真实形态，**不是 BLOCKED**。
3. **★ 相关性双端点（最易漏、代价最大）**：
   - `check_correlation` → **prod ≤ 0.70**；`check_self_correlation` → **self ≤ 0.70**。
   - **一条腿（机制）只产 1 颗** —— 同族提交一颗后，同持仓变体的 prod/self 会被推爆（GBR 实证：`gJZQZkZe` 提交后同腿 `rKe5L9q3` prod 0.6737 → **0.9933**）。
   - 降 prod 杠杆分两类：**改持仓**（换残差轴 / 字段 / 概念 / `trade_when` 分层）✅ ｜ **只改时序**（`hump` / `decay` / `ts_mean` 慢化）⚠️ **爆 self**。
   - **拥挤层诊断**：换 2–3 种结构 prod 会动（>0.01）= **结构层**（改持仓仍可用）；换 ≥5 种纹丝不动 = **机制层**（弃族）。

## 六步纵深骨架（本区覆盖）

> 通用方法见 [六步纵深骨架 · 通用主文档](../wq-brain-ra-pipeline/references/_six-step-core.md)。
> 本节只写 **GBR 的 override**：主 skills 未覆盖的本区平台事实、实测杠杆、已死轴、工程坑。
> **覆盖主 skills 同名条目；铁律与锁定项不可放宽。** 无实证处标「待实测」。

### ① 六法体检 · 本区覆盖

- **字段画像驱动**：本区走「Playbook 七层链路 → 九步映射」（见上文「字段画像驱动流程」）。
- **待实测**：离线体检包退化范围、不可用算子。

### ② 组装 · 本区覆盖

- **白名单 10 个数据集**（2026-08-26 建）；本波至少 2 槽按 win 机制换腿。
- **PROD 饱和族**（starmine 四向、delta66、other455×model264）**不生成新变体**；`model238` 只作复合从腿。
- **判定口径（GBR 版）**见上文「第 6 层 · 判定口径（GBR 版）」。

### ③ 归因 · 本区覆盖

- **硬墙是 prod，不是 IS** ⇒ 归因读数多指向因子暴露而非强度。
- **rn 低于 0.3 的反转候选按因子暴露处理**。

### ④ 破闸杠杆 · 本区覆盖

- **`SUBINDUSTRY` + `decay 4` 跟 win**；`STATISTICAL` 是有实证的 **A / B 对照轨**（wave57 8/8 孪生提升，见 [GBR × model](references/model.md)）。
- **★★ 2Y 闸随中性化浮动**（内置轴 **1.58 宽** / 因子型 **2.02 严**）⇒ 换中性化档即换 2Y 线，**逐档重判**。
- **结构维度 > 参数维度**（本区与 DEU 的共同铁律）。
- **★ 2026-10-13 晚场**：全面字段画像 + `LOW_2Y_SHARPE` 闸线地图（区域级铁律）见上文。

### ⑤ 算子穷举 · 本区覆盖

- **待实测**：完整算子清单（本区实证集中在七层链路，算子穷举记录待补）。

### ⑥ 终验 · 本区覆盖

- **待实测**：本区 prod 分布（已知硬墙是 prod）。
- **S9 回写**：每波 FAIL 必须写 `dead_end`，可精确定义的族另加规则；win 过闸即回写 `win_recipes`。

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **S0 / S2**：白名单 10 个数据集（2026-08-26 建）；本波至少 2 槽按 win 机制换腿；PROD 饱和族（starmine 四向、delta66、other455×model264）不生成新变体；model238 只作复合从腿。
- **S3 回测**：SUBINDUSTRY + decay 4 跟 win；STATISTICAL 是有实证的 A / B 对照轨（wave57 8 / 8 孪生提升，见 [GBR × model](references/model.md)）。
- **S4 改进**：GBR 的硬墙是 prod，不是 IS；rn 低于 0.3 的反转候选按因子暴露处理。
- **S9 回写**：每波 FAIL 必须写 dead_end，可精确定义的族另加规则；win 过闸即回写 win_recipes。2026-09-15 曾因 0 / 327 的产出触发停止规则，新波次先过开波闸。
（来源：GBR profile）

### ★★ 2026-10-13 · GBR 空间封闭裁决（88 条新仿真后的终局）

**结论：GBR 在「未点亮塔」里已无可挖空间；「10 颗可提交」不可达；连「补塔」都不可行。**

| 未点亮塔 | ALIVE 字段 | 终局 |
|---|---|---|
| **ANALYST**（塔 2） | 20 | 五数据集全判死：analyst7（breadth 族拥挤 + 182 未测字段全属该族且「换字段不造腿」）／analyst47（**F 墙**）／analyst9（处女池无信号）／analyst_factor_signals（IS 弱）／analyst93（类型 D，S 0.80）|
| **OTHER**（塔 1） | 3 | techindi_model 三字段**同一条腿**（互相关 0.88~0.93，已被 `3qVP6pNO` 占）；未测 40 字段（`dl_riskfree_returns`）= `probability_label*`/`quantile_label*` **桶标签 + 连续预测**，连续预测已实测 **2Y −0.28 全塌** |
| **PV**（塔 1） | 3 | `pv47_spret`/`pv47_for_statssimple_only_spret` 撞既有硬 dead_end（PROD-SAT）；`pattern_scores` 唯一 ALIVE 字段已被 `A1G7o1EE` 占；未测 37 字段（`pv29`）= `industry_grouping_*` **聚类标签（AXIS_ONLY，非信号）** |
| 其余 11 类 | **0** | 无 ALIVE |

**★ 三条终局证据**
1. **「未测大盘」的真相**：GBR 未测字段集中在 `analyst7`(182，属已判死族) / `model*`(已点亮塔) / `pv29`(轴) / `dl_riskfree_returns`(标签) ⇒ **未测 ≠ 有信号**，多数是标签/轴类非信号字段。
2. **历储备候选已被同腿自锁**：`rKe5L9q3` prod/self **0.9933 FAIL**、`zqbYwOmV` **0.9411 FAIL**（与已提交的 `gJZQZkZe` 同腿）⇒ ANALYST 塔**无法由旧储备补到 3/3**。
3. **新增判死形态「F 墙（不变量型）」**（详见 [analyst.md](references/analyst.md)）：`F = S×√(returns/max(TO,0.125))`，若族内 **S 与 1/√TO 严格同向** ⇒ 乘积是经济不变量，全参数空间扫不上去。

⇒ **GBR 的下一步只能是换 region 或接受现有 19 颗 ACTIVE**（两者均需用户明示）。

### ★★★ 2026-10-13 晚场 · 全面字段画像 + `LOW_2Y_SHARPE` 闸线地图（区域级铁律）

**① 全面画像方法（可复用）**：平台 `get_datasets(GBR,D1,TOP700)` = **177 数据集** × 本地 `field_profile --query --region GBR --limit 20000` = **15,523 字段** 交叉 ⇒ **66 个未点亮塔候选**（有未测/未知池 + 画像无判死）。画像 verdict 全分布：`UNKNOWN_COVERAGE 7444 / UNUSABLE 3409 / UNTESTED 2501 / AXIS_ONLY 1390 / DEAD 388 / ALIVE 52 / WEAK 47 / DEAD_STATIC 20 / DEAD_COUNT 5 / DEAD_TURNOVER 4`。

**② ★★★ `LOW_2Y_SHARPE` 闸线机制（2026-10-14 深挖修正，取代 10-13 的初版结论）**：

**初版（不完整）**：闸线按中性化浮动——内置轴 1.58 / 因子模型型 2.02。

**修正版（get_alpha_details 逐条读真值后）**：**闸线是「分档」的，显示的是当前正在卡的那一档**——
1. **`2Y < 1.58` ⇒ 显示 limit 1.58**（卡第 1 档）；
2. **`2Y ≥ 1.58` ⇒ 显示 limit 2.02**（已过第 1 档、进第 2 档）。
   ⇒ 实测序列完美阶跃：2Y 1.51/1.53/1.55/1.56/1.57 → limit 1.58；2Y 1.58/1.59/1.60/1.61/1.64/1.66/1.73/1.79/1.82 → limit 2.02。
   ⇒ **真正要过 2Y 闸需 2Y ≥ 2.02**（除非该 alpha 所处的档位本身低于 2.02）。
3. **例外：高换手 alpha 的档位更低**——技术指标冠军 `O0J1A88J`（**TO 0.2068**，CROWDING + sector 轴）**以 2Y 1.90 通过**，说明其适用档位 ≤1.90 ≠ 2.02。本区低换手信号（TO 0.03~0.08）**无法进该档**。
4. **表达式内分组轴影响 S 与 2Y**（sector 轴 S 1.53 / 2Y 1.53；subindustry 轴 S 1.72 / 2Y 1.73 @ CROWDING），但不改变上述分档规则。
5. ⚠ **`harvest` 输出的 `2Y_OK / 2Y_DEAD` 用房子静态阈值 1.58，对严档会误判** ⇒ **判定必须逐条 `get_alpha_details` 读 `is.checks` 的 limit**。

**★ 2026-10-14 晨 · 「窄带」精确化（30+ 条真值实证，决策级结论）**：
平台比较**真值**（显示四舍五入）⇒ **唯一可过带 = 真值 2Y ∈ [1.580, 1.585)**（显示 1.58、limit 1.58、判 PASS；**带宽仅 0.005**）。
- 真值 <1.580 → 显示 1.57/1.58、limit 1.58 → FAIL；
- 真值 ≥1.585 → 显示 1.59+、**limit 跳 2.02** → FAIL。
⚠ **危险特性：本区可用杠杆是「跳跃式」的**——CDS 腿（S 1.62）在 CROWDING/w66~85 时真值 ≈1.578（带下方 0.002）；一旦 `maxTrade OFF`（2Y 显示 1.59）或换 FAST 中性化（1.61）**立刻跳出带外并触发 2.02 档**。**⇒ 缺 0.002 也等于不可达；不要指望参数微调落在 0.005 带内。**

**★ 破闸纪律（最终版）**：① 要么把 **S 与 2Y 一起抬过 2.02**（需族级新机制，本区未找到）；② 要么进 **高换手低档位**（仅技术指标类信号可达 TO ≥0.15；CDS/信用类天然 TO ≤0.08 进不去）；③ **禁止**在 1.58 附近做微调——只会触发跳档。

⚠ 另：**GBR 平台 `LOW_SHARPE` 实测闸线 = 1.58**（非 config 的 delay1=1.25）；须 ≥ 1.585 真值。

**★ 破闸纪律（2026-10-14 修正）**：不要在宽档上盲目追高 S——**S 与 2Y 要一起抬过 2.02**，或**设法进入高换手低档位**（本区仅技术指标类信号可达 TO ≥0.15）。

**③ CDS 信用价差 = 未点亮塔处女池唯一活机制，但撞 2Y 墙**（详见 [other.md](references/other.md)）：16 机制探针筛选，仅 `other169.mid_par_spread_basis_points` 活（S 1.52 / F 1.07 / 2Y 1.57 @ SUBINDUSTRY）；~65 条全扫描（窗口/算子族/vec 聚合/外层/复合轴/11 中性化/decay 网格/字段）**无一提过 base**。

**④ 处女池「近静态」判据（新判死形态）**：GBR TOP700 上状态量/评级/低频类数据（ESG、分析师创新度、供应链占比、期权 IV）单字段水平信号 **TO 0.016~0.041（< review.turnover_min 0.05）且 2Y 多负** ⇒ 任何骨架无用。**开波前按机制类型预筛**。

**⑤ 本轮判定**：新增可提交 **0 颗**；GBR「10 颗可提交」在本区现有数据下**不可达**（唯一活腿卡 `LOW_2Y_SHARPE`，最接近处差 0.01）。报告 `output_report/GBR_field_profile_cds_20261013.md`。

### ★★★★ 探针派发 SOP（2026-10-14 定稿，全文见 [references/_probe-sop.md](references/_probe-sop.md)）

**GBR 特有前提**：multi-sim **上限 8 条**（DEU 为 10）；**`LOW_2Y_SHARPE` 闸线随中性化浮动**（内置轴 1.58 宽 / 因子模型型 2.02 严）；单一 universe **TOP700**（D0 多数数据集无字段）。

**第 0 步零成本筛选（按序）**：① **塔闸**（只挖未点亮塔 × ALIVE 密度；model 已点亮→排除）；② **语义闸**（字段级 description，剔标签/轴/元数据类）；③ **画像闸**（cov<0.6、to_med<0.03、count 族）；④ **★近静态闸**（状态量/评级/低频类 TO 0.016~0.041 ⇒ 直跳，本轮 16 机制中 8 个命中）；⑤ **历史闸**（禁自造结构、禁重测已判死族）；⑥ 概念族分组（同族免测）。

**第 1 步探针批构造（8 槽 = 2 结构 × 3 跨族字段 + 2 机动）**：
- 结构 A = house 底座 `group_rank(ts_mean(vec_avg(F),N), subindustry)`；结构 B = techindi 配方（双窗 + `group_neutralize` + `ts_target_tvr_decay` @ CROWDING/decay2）。
- 机动 2 槽 = `vec_max`（VECTOR）/ `reverse`（方向不明——GBR 实证 `days_from_last_change` 原始 −1.39、反向 +1.39）。
- **发批前六闸**：expr-lint / op-arity / **平台实时字段类型（MATRIX 错标 VECTOR ⇒ 整批 FAIL）** / op-lint（GBR 102 算子；`vector_neut` 不在清单、`tail` 必用命名参）/ **骨架 R2（单模板 ≤60%，须重组骨架非绕闸）** / probe-slot。

**第 2 步读数三分法（GBR 闸线口径）**：S≥1.58 **且 2Y ≥ 本档闸线**（宽 1.58 / 严 2.02，真值须 ≥ 闸线+0.005）→ 全闸验证；**S 1.0–1.58 不判死**（结构没找对的信号带）；S<0.5 判死（自检「真双结构？真跨族？」）。识别两种 GBR 判死形态：**「F 墙」**与**「2Y 有 S 无」**。

**第 3 步出闸去重**：PnL Pearson / `compute_mutual_correlation`（同族跨数据集 = 同腿，只出 1 颗）；GBR 硬墙是 **prod** 不是 IS。
<!-- profiles:manual:end -->

## 改控制

- **区域级**：`tracking/GBR/config/settings.json`（仿真设置）、`tracking/GBR/config/thresholds.json`（阈值）。
- **组合级**：`tracking/GBR/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region GBR
  $WQ_PY -m wqb.profiles render --region GBR --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[GBR profile](../wq-brain-ra-pipeline/references/regions/GBR.md)（入场裁决、红绿榜、证据附录）。
