---
region: EUR
entry_verdict: probe-only
one_liner: "2026-10-02 起 probe-only：EUR/D1 被项目自身实证判为结构性穷尽（库存 47/47 族 prod ≥ 0.70、7 个战役全 exhausted、23 条高 Sharpe 未测簇核实后可提交新增 = 0）；历史 win 机制 = 慢 MODEL 残差 × 快 PV（0.4/0.6 加权写法已被闸 5 禁止，只许条件 / 分组 / 残差三式），SUBINDUSTRY + decay4"
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
  stop_conditions: ["白名单被 dead_end 全覆盖", "EUR/D1 结构性穷尽（2026-10-02）——升 active 须出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(EUR)"
  last_verified: 2026-10-02
---

# EUR — win 机制复用区（2026-10-02 起 probe-only）

## ★ 2026-10-02 现状：结构性穷尽 → `probe-only`

来源：WorkBuddy 记忆 2026-10-02（用户要求转 EUR 后的调查；全部是项目内既有证据，不是新猜测）。

- **未点亮塔路径数学上封闭**（09-09）：`Fitness_upper = Sharpe_max × sqrt(returns_max / 0.125)`，要同时过平台的 Fitness 线与 Sharpe 线（`config.PLATFORM_CHECK_LINES`）需 returns ≥ 0.05，而 EUR 数据集 returns 天花板普遍 < 0.03；唯一 returns 达标的 ohlcv 族（0.061）撞字段级 prod 墙 0.80–0.82（四种算子几何全撞）。
- **库存 47/47 族 prod ≥ 0.70**（最低 0.7068），零竞争新轴三塔全灭，universe 换档否证（TOP2500 2.19 → TOP1200 0.33 → TOP400 0.50）；当前未提交候选 prod 全部 ≥ 0.7411，已 ACTIVE 的最低 0.5463。
- 过闸率 4.9%（259 波 / 594 回测，29 条 ≥ 1.58，137 条 dead_end，7 个 campaign 全 exhausted）；185 个数据集只测过 47 个，但大量「未测」是被 S0 硬地板排除的假机会（cov < 0.6 / usableFields < 10 / alphaCount > 1500）。
- 处女地 4 波新挖 max sharpe 0.22–0.93；10-02 仍有探针 `other460` best S 1.22 / 2Y 0.91，远低于 EUR 的 2Y 硬闸 1.6。
- ⚠ 设置口径三处不一致，动手前先定：`tracking/EUR/config/settings.json` = TOPCS1600 / SUBINDUSTRY / decay4 / trunc0.08 / maxTrade ON / nanHandling ON；WAVE_LEDGER 记 TOP2500 / COUNTRY / decay6；wave261 的 settings_json 是 TOP2500 / SUBINDUSTRY / decay4。
- **升 active 的条件**：出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源（决策表 D0-P「诊断前置」）；否则只许探针。下面的「win 换腿」章节是历史画像，仅在升档后适用。

## 定位与实证依据（2026-10-02 之前的历史画像）

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
