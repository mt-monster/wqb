---
last_verified: 2026-09-29
name: brain-alpha-repair
layer: L4
description: "弱候选修复的配方索引与补充实证（非改进入口）：降换手 / 提覆盖 / 降相关的修法指向与模板、GLB emotion 族降相关失败实证、修复成功判据（failed-count）。仅在被 wq-brain-alpha-optimization-v1 或 RA 步 7 引用时读取；要动手改候选请用 wq-brain-alpha-optimization-v1。"
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 修复（配方索引）

## 职责边界

- **本 skill 负责**：弱候选修复的**配方索引与补充实证**——降换手 / 提覆盖 / 降相关三类模板、GLB emotion 族降相关失败实证、修复成功判据（failed-count）。
- **本 skill 不做**：**不是改进入口**——改进的唯一入口是 `wq-brain-alpha-optimization-v1`（本 skill 不再有与它同批的触发词，只在被它或 RA 步 7 引用时读取）；不执行改进、不回测、不提交。
- **上游 / 下游**：上游 = `wq-brain-alpha-optimization-v1` / RA 步 7 的引用；下游 = `wq-brain-alpha-optimization-v1`（动手改）。

> **配方去哪了**：旧版声明「5 轴旋转、降相关 6 武器、分布形态 → 修复方向映射、news/sentiment 专用方向、幽灵算子警告、体检硬门复验已上移进 optimization-v1」，核对后**并不成立**：其中 4 项在别处**有**（字段体检文档 / 代码闸 / RA step5 / `news_sentiment_playbook.md`），「5 轴旋转」与「降相关 6 武器」**原文已遗失、不可恢复，已撤回**。逐项去向见 [`references/repair-recipes.md`](references/repair-recipes.md)（每一项由测试逐条 grep 校验）。

## 修复工作流

1. **先诊断再动手**。改公式前先读最新仿真指标与闸门失败原因；失败的检查 → 该往哪个方向修的速查表在 [`brain-how-to-pass-alpha-test`](../brain-how-to-pass-alpha-test/SKILL.md)「失败点 → 修法族」。
2. **修复成功的判据 = failed-count 清零**。口径、`PENDING` / `WARNING` 语义与「未清零不得 `set_alpha_properties`、不得推进下游」只在 RA [`webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md) §1 定义一处，这里只引用：REGULAR 看 `Failed RA == 0`，PPA 看 `Failed PPA == 0`。**怎么判是 REGULAR 还是 PPA**：候选走 PPA 通道（RA 的 PPA 分支 / 标签 `CH_PPA` / 平台 `classifications` 含 `Power Pool Alpha`）→ PPA，否则 REGULAR。
3. **结构修复优先于暴力调参**。选算子前对照 `known_ops`（`platform_constraints.json`）与 `ghost_ops`，不要为此全量拉 `get_operators`；表达式级幽灵检查用 `tools/campaign_intel.py ghost-audit`。三类的可复制模板与适用条件见 [`references/repair-recipes.md`](references/repair-recipes.md) §二：
   - **turnover**：`ts_decay_linear` / `ts_mean`（窗口取 5 / 22）、`hump(x, hump=k)`（命名参数）、`ts_target_tvr_hump`；换手已低于 12.5% 不要再降；
   - **coverage**：`ts_backfill(x, 66)` / `group_backfill`，VECTOR 先经 `vec_avg` 等聚合；
   - **correlation**：**不磨参数**——先读 RA 决策表 [D0-P](../wq-brain-ra-pipeline/references/decision-table.md) 再选动作；news / sentiment 数据必须走 [`docs/reference/news_sentiment_playbook.md`](docs/reference/news_sentiment_playbook.md)（通用菜单在此类数据上适得其反）。
4. **修复后的可追溯性**用现存机制：`expressions` 表的 `fingerprint`（表达式哈希）+ `settings_json`（设置）已随入库记录，够回答「这个修复试过没有」；**不需要**另写轨迹表（旧版要求的 `trajectory_steps` 在生产代码里没有任何写入方，agent 既写不了也「看见」不了；「settings fingerprint」也没有生成者）。
5. **区域约定**在各区 profile 里：USA REGULAR 的 universe 约定见 RA [`regions/USA.md`](../wq-brain-ra-pipeline/references/regions/USA.md)「步 7 注入：修复用 universe 约定」。
6. **GLB emotion 族降相关失败实证**（事实 / 结论 / 适用范围）见 [`references/repair-recipes.md`](references/repair-recipes.md) §三——本 skill 是该教训的唯一完整版，其它文档只允许引用、不复制全文。

## 验证清单（每一项都可检）

1. 修复后的候选在 `expressions` 里有独立的 `fingerprint` 与 `settings_json`（`mcp__wqb-db__list_expressions` 可查）。
2. failed-count 为零（REGULAR `Failed RA == 0` / PPA `Failed PPA == 0`）后才推进候选。
3. 用到的算子都在 `known_ops` 内，且 `ghost-audit` 退出码为 0。
4. 若 region = GLB 且信号族 = emotion：本轮台账里有 ≥ 1 个平台 prod 读数（`alphas.prod_correlation` 非空，或 ledger `prod_first_<wave>`）——没有读数就不得推进（教训是「同族全撞墙」）。

## 情景卡

三张卡（降换手 / 覆盖不足 / 降相关）在 [`references/scenarios.md`](references/scenarios.md)：症状 → 动作 → 预期 → 验收，并注明每一张的失败分支。
