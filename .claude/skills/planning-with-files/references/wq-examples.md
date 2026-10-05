# WQ 场景示例：一次 RA 战役的 task_plan

> 主文见 [`../SKILL.md`](../SKILL.md)。**结果的真相源是 DB 台账**；下面每个阶段的「检查点」告诉你这一步的产物该在台账的哪个键 / 表里查到，规划文件只记过程。九步的定义以 RA SOP（`wq-brain-ra-pipeline`）为准，这里只是把它映射成 `### Phase` 与检查点，并保持模板要求的 `**Status:**` 行格式（`scripts/check-complete.sh` 与 Stop 钩子按它计数）。

```markdown
# Task Plan: KOR fundamental17 开第 190 波

## Goal
在 KOR 用 fundamental17 走完 RA 九步，产出可提交候选或有证据的判死。

## Phases

### Phase 1: S-PRE 库存盘点 + 查表
- **Status:** complete
- 检查点：`get_campaign_summary` / `get_dead_ends` 已读；篮子口径 = Failed RA == 0

### Phase 2: S0 选集（数据集）
- **Status:** complete
- 检查点：`campaign_intel.py s0-select` 输出已存；选定数据集写入本计划的 Decisions

### Phase 3: S1 字段目录 + 闸 SEM 前置
- **Status:** in_progress
- 检查点：ledger `s1_semantic_<ds>` 存在（缺失 → 闸 SEM exit 2）

### Phase 4: S2 概念优先 GEM
- **Status:** pending
- 检查点：`list_expressions(region, wave, dataset)` 有本波表达式；priors 快照日期已记

### Phase 5: 门禁（wave_gate）
- **Status:** pending
- 检查点：`get_gate_result(region, wave, dataset)` 有记录且 `all_pass=1`

### Phase 6: S3 七槽回测 + 收割
- **Status:** pending
- 检查点：`backtest_results` 有本波行（`harvest_multisim_results` 已入库）

### Phase 7: S4 诊断改进
- **Status:** pending
- 检查点：`s4_walls_<region>_<wave>` 已写；每条候选有去向

### Phase 8: 提交（需用户明确确认）
- **Status:** pending
- 检查点：`submit_verdict` 结论已读；**未经用户确认不提交**

### Phase 9: S6 回写
- **Status:** pending
- 检查点：`get_wave_result` 的 verdict 非空；`assemble-priors` 已重跑

## Decisions
| Decision | Rationale |
|---|---|
| 选 fundamental17 | S0 输出：未点亮塔 × 高产出 × 未判死 |

## Errors Encountered
| Error | Attempt | Resolution |
|---|---|---|
```

**恢复时怎么用**：五问先读本文件确定当前阶段，再用检查点里写的台账查询核对**结果**；两者不一致以台账为准，并在 `progress.md` 记一行差异原因。
