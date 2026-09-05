---
region: IND
entry_verdict: active
one_liner: "TOP500 长窗结构区：2Y Sharpe 强，scale(-rank(x)) 破墙语法实证，评审加 2Y 权重"
static:
  universe: [TOP500]
  universe_default: TOP500
  delay: [1]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "长窗结构有效面，单看 IS Sharpe 会误杀"
datasets:
  red: [anl39, qfl]
  red_reason: "anl39/qfl 判死"
  yellow: []
  green: [mdl177（长窗结构）, 慢变量基本面集]
priors:
  signal_families_include: [long_window_structure, slow_fundamental, mdl177_family]
  signal_families_exclude: [anl39_family, qfl_family]
  syntax_patterns:
    - "scale(-rank(x))  # 破墙语法实证：反向缩放排名结构"
  win_recipes:
    - "mdl177 长窗结构族（3 颗 ACTIVE，2Y Sharpe 强）"
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
  judge_two_year_sharpe_weight: high
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(IND)"
  last_verified: 2026-08-25
---

# IND — 长窗结构区

## 定位与实证依据

IND TOP500 的有效面在**长窗结构**：mdl177 族已产 3 颗 ACTIVE，共同特征是 IS Sharpe 中等但 **2Y Sharpe 显著强**——长窗信号衰减慢，样本外稳健。anl39 / qfl 判死。另有语法级实证：`scale(-rank(x))` 反向缩放结构在 IND 破墙成功（绕过自检相关性/方向约束），已入 priors。当前 1 颗 submit_ready。

## 流程变体（相对九步骨架）

### 步 4 注入：语法模式入 priors

GEM `--priors-file` 必须携带 `syntax_patterns`：`scale(-rank(x))` 作为推荐骨架模板之一。注意它是**结构模板**不是字段——GEM 仍需概念优先选定字段后套用。

### 步 7/8 注入：评审加 2Y 维度（IND 核心变体）

- 步 7 诊断时拉 `get_alpha_yearly_stats`，`two_year_sharpe` 纳入判定：IS Sharpe 1.0–1.25 但 2Y Sharpe ≥1.5 的候选**不降格、不判死**，进 Mode A 微调（decay/窗口），不进 Mode B 换概念；
- 步 8 judge 阶段向用户报告时必须并列 IS / 2Y 两列，禁止只报 IS Sharpe（IND 误杀主因）。

### 步 6 注入：长窗设置优先

窗口/decay 探索顺序：长窗（≥250d）优先于短窗；decay 大值（≥10）优先。短窗量价族在 IND 无实证支持，探针额度让给长窗。

## 避坑清单

- anl39 / qfl 族不进白名单。
- 禁止用 IS Sharpe 单指标判 IND 候选死刑（2Y 强信号会被误杀）。
- `scale(-rank(x))` 不万能：仅用于方向反转型信号，正报型信号套用它必然翻转逻辑。
