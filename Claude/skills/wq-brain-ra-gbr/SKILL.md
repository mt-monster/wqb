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

## 本区流程差异（相对九步骨架）

<!-- profiles:manual:start -->
- **S0 / S2**：白名单 10 个数据集（2026-08-26 建）；本波至少 2 槽按 win 机制换腿；PROD 饱和族（starmine 四向、delta66、other455×model264）不生成新变体；model238 只作复合从腿。
- **S3 回测**：SUBINDUSTRY + decay 4 跟 win；STATISTICAL 是有实证的 A / B 对照轨（wave57 8 / 8 孪生提升，见 [GBR × model](references/model.md)）。
- **S4 改进**：GBR 的硬墙是 prod，不是 IS；rn 低于 0.3 的反转候选按因子暴露处理。
- **S9 回写**：每波 FAIL 必须写 dead_end，可精确定义的族另加规则；win 过闸即回写 win_recipes。2026-09-15 曾因 0 / 327 的产出触发停止规则，新波次先过开波闸。
（来源：GBR profile）
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
