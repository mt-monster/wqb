---
name: brain-alpha-research-hypothesis-first
layer: L1
description: "饱和数据集（≥1 万 alpha）的假设优先挖掘工作流。当模板采样空间已被挖尽、需要用可证伪假设驱动（hypothesis-first）而非模板遍历的方式挖掘时使用。触发词：饱和数据集 / 假设优先 / hypothesis-first / 模板挖尽。"
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 研究 — 假设优先（Hypothesis-First）

## 触发场景

本 skill 适用于以下任务：目标数据集已饱和（≥1 万 alpha）且模板采样空间挖尽，需要假设优先挖掘。

具体切换信号：
- 数据集 alpha 总量 ≥10K（如 `news12`：120K alpha / 21K 用户）。
- 一次 90 条仿真的模板会话已见顶（如 news12 Fitness ≈ 0.42 墙，2026-04-23 实测）。
- 论坛高赞自动化流程（80 赞 Gemini-CLI 模板工作流，帖 HZ32281）等已把模板空间挖到天花板。

## 工作流

### 1. 何时切换

见上节触发信号；满足其一即从模板遍历切换到假设驱动。

### 2. 构建 `data/field_semantics/<region>_<dataset>.yaml`（字段语义元数据）

每个字段一条：
```yaml
- name: anl14_mean_ndebt_fy1
  physical_unit: ratio
  causal_chain_to_returns: "资产负债表杠杆信号 -> 违约风险重定价"
  anchor_only: false          # anchor-only 字段（news_spy_close、news_eod_close 等）永远不能当主信号
  correlated_fields: [anl14_mean_ndebt_fy2]
```
`anchor_only: true` 的字段**禁止**用作主信号。

### 3. 构建 `data/hypothesis_catalog/<dataset>_hypotheses.yaml`（假设目录）

≥20 条可证伪假设，每条：
```yaml
- id: H_overreaction_earnings
  class: over_reaction
  minimal_expression: "rank(ts_zscore(returns, 20))"
  ablation_no_gate: "rank(ts_zscore(returns, 20))"   # 同结构但去掉事件门控
  control_constant: "rank(ts_zscore(volume, 20))"     # 常数/对照组
  variant: "rank(ts_zscore(returns, 20)) * sign(...)"
```

假设类别（12 类）：`over_reaction / under_reaction / dispersion / event_conditional / propagation / information_asymmetry / cross_dataset / horizon_spread / regime / residual / slow_diffusion / urgency`。

### 4. 派发 — `run_hypothesis_round`

`src/wqb/research/hypothesis_miner.py::run_hypothesis_round(catalog_path, max_hypotheses=1)` 自动派发**一个实验 = 4 条 alpha**：主假设 + 去门控消融 + 常数对照 + 变体。计算归因增量（主假设 vs 对照组 Sharpe 差）。

### 5. 判定 — verdict 驱动下一步

`judge()` 返回四态之一：
- **rejected（证伪）** → 该假设一批结案（省下 ~40 条变体追踪的仿真）。
- **partially_supported（部分支持）** → 按诊断细化具体参数。
- **supported（支持）** → 满足用户指标则交 `brain-alpha-robustness` 审计。
- **needs_refinement（需打磨）** → 调整表达式后循环。

> 伪信号（主假设 Sharpe ≈ 对照组 Sharpe）在**第一批就被 REJECT**。

### 6. 台账

跨会话知识累积到 `data/hypothesis_ledger/<session>.jsonl`。对假设类别的元学习取代逐臂 bandit 后验。

## 与其他 skill 的关系

- 候选需要修复时先用 `brain-alpha-repair` 诊断。
- `submit_alpha` 前用 `brain-alpha-robustness` 验证。
- 字段质量先验（`get_datafields` 的 `alphaCount`/`userCount`）仍作为种子排序依据，服从全部主题/金字塔/覆盖闸门。

## 验证清单

1. 确认字段语义 YAML 已构建并带 `anchor_only` 标记。
2. 确认假设目录有 ≥20 条可证伪假设。
3. 确认 `run_hypothesis_round` 每个实验派发 4 条 alpha（主假设/消融/对照/变体）。
4. 确认伪信号在第一批即被 REJECT。
