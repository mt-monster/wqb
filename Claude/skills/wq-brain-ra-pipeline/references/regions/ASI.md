---
region: ASI
entry_verdict: probe-only
one_liner: "处女地：未开垦，analyst94 近闸（OS 0.666）/ analyst81 untried，全量探针建 baseline"
static:
  universe: []  # 必须 get_platform_setting_options 实测，禁止照抄任何区域
  universe_default: null
  delay: []     # 实测
  delay_default: null
  neutralization_default: SUBINDUSTRY
  notes: "static 层未建立，步 1 强制实测合法档位"
datasets:
  red: []
  red_reason: ""
  yellow: []
  green: [analyst94, analyst81]
priors:
  signal_families_include: [analyst]
  signal_families_exclude: []
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 5
  first_wave_probe_exemption: true
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖", "连续 3 波全 FAIL 且无新 dead_end"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(ASI)"
  last_verified: 2026-08-25
---

# ASI — 处女地全量探针区

## 定位与实证依据

ASI 基本未开垦：无 win 层、无死路记录，registry 接近空白。已有线索两条：analyst94 探出 OS Sharpe 0.666（近闸候选）、analyst81 在推荐榜且 untried。处女地的核心任务不是"出 ACTIVE"，而是**用最少的波次建立区域实证 baseline**：哪些档位合法、哪些数据集有信号、金字塔配额怎么落。

## 流程变体（相对九步骨架）

### 步 1 注入：static 层强制实测

`get_platform_setting_options(region=ASI)` 实测合法 universe 档 / delay / instrumentType，**禁止照抄 USA 或任何区域档位**（matrix 硬规则 3）。实测结果回写 regions 表 static 层后再进步 2。

### 步 2 注入：全量探针模式

- 全部候选数据集过 `dataset_health_check` + `score_datasets.py` 三灯评分，按分数排探针优先级；
- 金字塔配额照旧（≥2 非 MODEL），但无 win 层可读，候选顺序 = 三灯分数 × 已知线索（analyst94/analyst81 优先）。

### 步 6 注入：首波探针豁免（一次性）

首波允许 **全槽探针**（七槽制下即 7 槽，豁免骨架"弱探针最多 1 槽"约束一次），目的建 baseline；第二波起恢复正常约束，`max_probes_per_wave` 回落 1。

### 步 9 注入：强制回写加倍

处女地每个结论都是高价值实证：每波 verdict、每个数据集的探针结果（包括失败）必须回写 registry/ledger，**未回写视为本波未完成**（骨架已有，ASI 严格执行）。

## 避坑清单

- 禁止照抄他区 universe 档（CHN 默认档返空类事故的前科）。
- analyst94 近闸不等于可提交：OS 0.666 离闸还有距离，按 Mode A 微调路径走，不提前庆祝。
- 首波探针豁免仅一次：第二波仍全槽探针 = 违反填槽纪律。
