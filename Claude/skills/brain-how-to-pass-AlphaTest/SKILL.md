---
last_verified: 2026-08-22
name: brain-how-to-pass-AlphaTest
description: "提供 WorldQuant BRAIN alpha 提交测试的详细要求、阈值与改进建议。 涵盖 Fitness、Sharpe、Turnover、Weight、Sub-universe 与 Self-Correlation 测试。 当用户询问 alpha 提交失败原因、如何提升 alpha 指标或测试要求时使用 （submission tests / thresholds / improvement tips / 提交测试 / 通过测试）。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







# BRAIN Alpha 提交测试：要求与改进建议

本 skill 提供通过 alpha 提交测试的关键要求与专家建议。
完整细节、阈值与社区策略请阅读 [reference.md](reference.md)。

## 概述

Alpha 必须通过一系列提交前检查，以确保其满足质量阈值。

## 1. Fitness
### 要求
- 至少为 "Average"：Delay-0 需大于 1.3，或 Delay-1 需大于 1。
- Fitness = Sharpe * sqrt(abs(Returns) / max(Turnover, 0.125))。

### 改进建议
- 提高 Sharpe/Returns 并降低 Turnover。
- 使用分组算子（group operators，如搭配 pv13）来提升 fitness。
- 用 `mcp__wq-brain-http__get_alpha_details` 工具检查（返回 `is.checks`；提交配额从 submit 响应的 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 读，`get_submission_quota` 已于 2026-08-25 移除）。

## 2. Sharpe Ratio
### 要求
- Delay-0 需大于 2，或 Delay-1 需大于 1.25。
- Sharpe = sqrt(252) * IR，其中 IR = mean(PnL) / stdev(PnL)。

### 改进建议
- 关注低波动下的稳定 PnL。
- 对流动性/非流动性股票分别对信号做 decay。
- 若 Sharpe 为负（如 -1 到 -2），可尝试翻转符号：`-original_expression`。

## 3. Turnover
### 要求
- 1% < Turnover < 70%。

### 改进建议
- 使用衰减函数（`ts_decay_linear`）平滑信号。

## 4. Weight Test（平台检查名 `CONCENTRATED_WEIGHT`）
### 要求
- 任一股票的权重上限 <10%。

### 改进建议
- 使用中性化（如 `neutralize(x, "MARKET")`）来分散权重。
  ⚠️ **2026-09-01 实测修正（IND/TOP500 实证）：中性化对本闸无效**，见下。

### ★ 实测要点（2026-09-01，IND analyst 修正族双例验证）
- **本闸是"隐形第四闸"，且无法预检**：不同于 SELF/PROD，**它无 value/limit**，IS 阶段只显示
  `WARNING` 或 `PASS`，**提交后才判 FAIL（403）**。IS 阶段 WARNING 的 alpha 提交后必 FAIL
  （硬闸失败零成本，不消耗配额）。→ **提交纪律：先看 IS 阶段该闸状态，WARNING 就别提。**
- **根因在表达式结构，不在参数**：瞬时离散计数/事件类信号 → 权重集中 → FAIL；
  同一信号加时间平滑（`ts_mean(x, 10)`）→ **PASS**。
  | 构造 | 本闸 | 结果 |
  |---|---|---|
  | `add(0.6*rank(subtract(U30,D30)), 0.4*(-rank(ts_mean(RES,10))))`（A 项瞬时） | WARNING | 提交 FAIL（4.26/3.97 也照拦） |
  | `add(0.6*rank(subtract(U14,D14)), 0.4*(-rank(ts_mean(RES,10))))`（A 项瞬时） | WARNING | 提交 FAIL |
  | `add(0.6*rank(ts_mean(subtract(U14,D14),10)), 0.4*(-rank(ts_mean(RES,10))))`（A 项平滑） | **PASS** | 提交成功（3.70/3.19） |
  | `rank(ts_mean(subtract(U30,D30),10))`（单信号平滑） | **PASS** | 已 ACTIVE |
- **参数层全无效（别再试）**：换 neutralization（MARKET/SECTOR/INDUSTRY/SUBINDUSTRY 四档）仍 WARNING；
  truncation 0.08→0.02/0.01 仍 WARNING；末端再套 `rank(...)` **反而变 FAIL**；`scale(x, 1)` 语法错（scale 只收 1 输入）。
- **结论**：事件/计数类字段（分析师评级变动、新闻计数、财报事件等）构造时**默认加时间平滑**
  （`ts_mean` / `ts_decay_linear`），不要直接 rank 瞬时值。

## 5. Sub-universe Test
### 要求
- Sub-universe Sharpe >= 0.75 * sqrt(subuniverse_size / alpha_universe_size) * alpha_sharpe。

### 改进建议
- 避免使用与市值相关的乘数。
- 对流动性/非流动性部分分别做 decay。

## 6. Self-Correlation
### 要求
- 与自身已提交 alpha 的 PnL 相关性 <0.7。

### 改进建议
- 提交多样化的 idea。
- 使用 `mcp__wq-brain-http__check_correlation` 工具。
- 对负相关 alpha 做变换。

## 通用建议
- **从简单开始**：先使用 `ts_rank` 等基础算子。
- **优化设置**：选择 TOP3000 等股票池（USA, D1）。
- **ATOM 原则**：避免混合数据集，以受益于放宽的 "ATOM" 提交标准（近 2 年 Sharpe / Last 2Y Sharpe）。

## 衔接协议
- **上游**：S3 `brain-simAlphasinBatch-and-track`（回测结果优先查 **backtest_results 表**（`mcp__wqb-db__*` 查询工具，结构化真相源）；`simulation_status.csv` 候选池为排障兼容回退）。
- **本 skill 角色**：S4 链首步——失败项定位与阈值判定。
- **FAIL 回流纪律（2026-09-02，区域无关，强制）**：判定 FAIL 后候选不得直接丢弃/只留 near_pool，按资格线分流：
  1. 对照区域 `thresholds.json` 的 `mode_b_qualification`（缺省 sharpe≥1.25 且 fitness≥0.8）：**达标 → 强制进
     `wq-brain-alpha-optimization-v1`**（Mode B 想法层 → 常规 2–3 轮仍卡结构性闸 → 其「组合腿救援」协议
     消费 salvage_pool 补强腿）；**未达标 → 判死**（dead_end 回写 + wave 台账 closed，勿送 near_pool / 勿发增强波）。
  2. 快达标因子（S≥1.0 且 prod corr<0.5）已由 S4 `review_wave.py --write-ledger` 自动幂等写入台账
     `salvage_pool`（对齐 `_salvage_to_pool` entry 结构，带 boost_dims 卡点标注），**无需人工手写入池**。
- **下游**：`wq-brain-alpha-optimization-v1`（先 Mode B 想法层，后 Mode A 参数层）→ `brain-calculate-alpha-selfcorrQuick` → `brain-explain-alphas`。
