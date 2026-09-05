---
region: EUR
entry_verdict: active
one_liner: "win 配方已验证区：0.4 慢 MODEL 残差 + 0.6 快 PV，SUBINDUSTRY + decay4，策略=换腿扩配"
static:
  universe: [TOP1600, TOPCS1600, ILLIQUID_MINVOL1M]
  universe_default: TOP1600
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "SUBINDUSTRY + decay4 为 win 实证设置"
datasets:
  red: []
  red_reason: ""
  yellow: []
  green: [model 系（慢残差腿）, pv 系（快腿）, analyst 系]
priors:
  signal_families_include: [slow_model_residual, fast_pv, analyst]
  signal_families_exclude: []
  syntax_patterns: []
  win_recipes:
    - "0.40 × 慢 MODEL 残差 + 0.60 × 快 PV；neutralization=SUBINDUSTRY；decay=4"
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(EUR)"
  last_verified: 2026-08-25
---

# EUR — win 配方复用区

## 定位与实证依据

EUR 已有平台级验证配方：**`0.40 × 慢 MODEL 残差 + 0.60 × 快 PV`，中性化 SUBINDUSTRY，decay 4**（registry win 层）。该配方的价值在机制不在具体字段——慢残差提供低相关底座，快 PV 提供弹性。策略不是找新配方，而是**按该机制换腿扩配**：换慢腿字段、换快腿字段、换数据集组合。

## 流程变体（相对九步骨架）

### 步 4 注入：win 换腿升为强制

骨架约束"每波至少 `win_replay_slots_min` 槽按 win 机制换腿"在 EUR **升为硬约束 ≥2 槽**：

- 慢腿候选：model 系数据集未用过的残差字段；
- 快腿候选：pv 系未用过的量价字段；
- 比例 / 中性化 / decay 跟 win 配方，不重新扫参数（那是 Mode A 的事，不在生成阶段）。

### 步 6 注入：设置探索默认开启

骨架列为"可另探"的三项在 EUR 默认排入探索队列（每波最多占 1 槽，不挤占 win 换腿槽）：

1. `ILLIQUID_MINVOL1M`（非流动性宇宙）；
2. `TOPCS1600`；
3. `delay 0`。

### 步 9 注入：win 配方版本化回写

每次 win 换腿产出新 ACTIVE，回写 win 层时必须记录**换的是哪条腿 + 新字段 id**，形成配方族谱，避免下一波重复换同一条腿。

## 避坑清单

- 禁止只穷举同金字塔换字段（骨架反模式，EUR 最容易犯）。
- win 配方比例（0.4/0.6）不作为搜索起点的唯一值——可在 0.3–0.5 / 0.5–0.7 区间微调，但每波只动一个变量。
- EUR 无死路记录不等于安全：新数据集仍走 8 探针快判死。
