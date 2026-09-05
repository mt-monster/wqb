---
region: CHN
entry_verdict: probe-only
one_liner: "实测档位区：默认档返空类试错前科，static 层必须实测建立，禁止任何外推"
static:
  universe: []  # 必须实测；历史教训：默认档返空
  universe_default: null
  delay: []     # 实测
  delay_default: null
  neutralization_default: null  # 实测后定
  notes: "A 股市场结构特殊（涨跌停/T+1），信号语义需重新审视"
datasets:
  red: []
  red_reason: ""
  yellow: []
  green: []
priors:
  signal_families_include: []
  signal_families_exclude: [glb_emotion]
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 2
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(CHN)"
  last_verified: 2026-08-25
---

# CHN — 实测档位区

## 定位与实证依据

CHN 有"默认档返空"类试错前科：照抄默认 universe 档导致回测返空，白烧配额。A 股市场结构特殊（涨跌停限制、T+1、散户占比高），量价/情绪信号的语义与欧美市场不同，**不能直接移植任何区域的信号族假设**。当前 registry 近空白，第一步是建立可信的 static 层。

## 流程变体（相对九步骨架）

### 步 1 注入：static 层强制实测（CHN 核心变体）

1. `get_platform_setting_options(CHN)` 实测全部合法 universe 档 / delay / neutralization / instrumentType；
2. 每档先用 1 条裸 PV 探针验证**返空与否**（返空档直接标记不可用）；
3. 实测结果回写 regions 表 static 层后，才允许进步 2。**禁止照抄任何区域档位**（matrix 硬规则 3 在 CHN 升为最高优先级）。

### 步 4 注入：信号语义审查

GEM 生成时 priors 必须声明 A 股特殊性：

- 涨跌停 ±10%（主板）/±20%（创业/科创）：日内动量信号截断，ts_returns 类表达式需考虑截断效应；
- T+1：当日买入不可卖出，反转信号衰减结构与美股不同；
- 概念优先生成，禁止直接移植 USA 动量/反转族参数。

### 步 7 注入：HKG 联动对照

近闸候选与 HKG 区 ACTIVE 互查（若已有），A/H 溢价相关信号需注意跨区暴露。

## 避坑清单

- 档位未实测前，任何生成/回测请求一律拒绝（返空事故防线）。
- 量价信号先过"涨跌停截断"常识审查再进七槽。
- GLB emotion 铁律照 exclusion。
