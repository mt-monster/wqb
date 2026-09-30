---
region: EUR
entry_verdict: active
one_liner: "win 机制已验证区：慢 MODEL 残差 × 快 PV 的跨周期结构（历史 0.4/0.6 加权写法已被闸 5 禁止，只许条件 / 分组 / 残差三式），SUBINDUSTRY + decay4，策略=换腿扩配"
static:
  universe: [TOP2500, TOPCS1600, TOP1200, TOP800, TOP400]
  universe_default: TOP2500
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "SUBINDUSTRY + decay4 为 win 实证设置；档位以 src/wqb/config.py::REGIONS['EUR'] 为准（2026-09-22 实测：ILLIQUID_MINVOL1M 已不可用、TOP1600 不在档位表；IS 强度集中在 TOP2500，窄档易塔陷）"
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
    - "（机制）慢 MODEL 残差 × 快 PV 的跨周期 / 跨数据源结构；neutralization=SUBINDUSTRY；decay=4。历史落地写法是 0.40/0.60 加权相加，2026-09-13 起被路线 A 与闸 5 禁止——只许以条件 / 分组 / 残差入场，不记录混合比例"
gate_overrides:
  cw_gate: WARN
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "缺省（决策表 D15：新数据集 8 探针无 |S|≥0.5 即判死）；本区无额外规则"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(EUR)"
  last_verified: 2026-08-25
---

# EUR — win 机制复用区

## 定位与实证依据

EUR 已有平台级验证的**机制**：慢 MODEL 残差（低相关底座）× 快 PV（弹性），中性化 SUBINDUSTRY，decay 4（registry win 层）。历史落地写法是 `0.40 × 慢 + 0.60 × 快` 的加权相加——**该写法自 2026-09-13 起被路线 A 与闸 5 禁止，不得照抄**；现只许改写成条件 / 分组 / 残差三式（见 optimization-v1 `structural-interaction-forms.md`）。价值在机制，不在具体字段，也不在比例。策略不是找新配方，而是**按该机制换腿扩配**：换慢腿字段、换快腿字段、换数据集组合。

## 流程变体（相对九步骨架）

### 步 4 注入：win 换腿升为强制

骨架约束"每波至少 `win_replay_slots_min` 槽按 win 机制换腿"在 EUR **升为硬约束 ≥2 槽**：

- 慢腿候选：model 系数据集未用过的残差字段；
- 快腿候选：pv 系未用过的量价字段；
- 中性化 / decay 跟 win 配方，不重新扫参数（那是 Mode A 的事，不在生成阶段）；结构性组合里没有「混合比例」这个参数可调。

### 步 6 注入：设置探索默认开启

骨架列为"可另探"的两项在 EUR 默认排入探索队列（每波最多占 1 槽，不挤占 win 换腿槽）：

1. `TOPCS1600`；
2. `delay 0`。

> `ILLIQUID_MINVOL1M` 已从平台档位表移除（2026-09-22 实测，且对 EUR 已被永久停提），不得再排入；`TOP1200` / `TOP800` / `TOP400` 等窄档实测易塔陷（`config.REGIONS['EUR']['_note']`），只作单点对照探针，不作探索主线。

### 步 9 注入：win 配方版本化回写

每次 win 换腿产出新 ACTIVE，回写 win 层时必须记录**换的是哪条腿 + 新字段 id**，形成配方族谱，避免下一波重复换同一条腿。

## 避坑清单

- 禁止只穷举同金字塔换字段（骨架反模式，EUR 最容易犯）。
- **不调混合比例**：加权 / 等权相加已被闸 5 禁止（路线 A，2026-09-13 起），也违背「禁止混信号调参」；换腿时每波只动一个变量（慢腿字段 / 快腿字段 / 条件分位阈值）。
- EUR 无死路记录不等于安全：新数据集仍走 8 探针快判死。
