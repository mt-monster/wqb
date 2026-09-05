---
name: brain-alpha-repair
layer: L4
description: "修复或演化弱候选 alpha：在保持多样性与可追溯性的前提下降 turnover、提覆盖、降相关性，或从反复失败的搜索轨迹中恢复。触发词：候选修复 / 降换手 / 提覆盖 / 降相关 / 失败轨迹恢复。"
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

> **定位声明（2026-08-23 单源化）**：**改进的唯一入口是 `wq-brain-alpha-optimization-v1`**（Mode B 想法层 70% / Mode A 参数层 30%）。本 skill 原有的可复用配方——5 轴旋转、降相关 6 武器、分布形态→修复方向映射、news/sentiment 专用方向、幽灵算子警告、体检硬门复验——已于 2026-08-23 全部上移进 optimization-v1 的对应工作流步骤，那里是权威表述。
>
> 本文件只保留**不适合放进通用工作流的补充实证与执行纪律**：WebDataScope failed-count 作为修复成功判据、GLB emotion 族降相关失败的完整实证（§2d）、USA REGULAR 的 universe 默认约定、trajectory 可追溯性要求。

# BRAIN Alpha 修复

## 触发场景

候选修复、降换手、提覆盖、降相关性、失败轨迹级恢复。

## 工作流

1. **先诊断再动手**。改公式前先读最新仿真指标、闸门失败原因与轨迹步骤。
1a. 修复属于 REGULAR 或 PPA 挖掘链时，以 [`../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md) 的 WebDataScope failed-count 门为修复目标。REGULAR 修复成功的唯一标准是 `Failed RA == 0`；PPA 是 `Failed PPA == 0`。改善 Sharpe/Fitness/相关性但 failed count 非零的修复仍是 reject，不得进入 `check_correlation` 或 `set_alpha_properties`。
2. **结构修复优先于暴力调参**。选定任何算子前先确认它在当前 `get_operators` 返回里（幽灵算子清单与替换表见 `wq-brain-alpha-optimization-v1` Step B3）。
   - **turnover**：用平台支持的降换手算子（线性时序衰减、仓位变化阻尼、TVR 目标调参）或调高仿真 `decay`；
   - **coverage**：时序或同侪组回填、重审向量聚合选择、复查 NaN 策略；
   - **correlation**：5 轴旋转（外层 wrapper / 标准化器 / 分组分类器 / signed-power 指数 / 前置算子非对称性）与**降相关 6 武器**（按实测降幅排序的动作序列，含案例 alpha ID 与 Mode B/A 归属）的权威表述已上移至 `wq-brain-alpha-optimization-v1`（Step B3 与「相关性反馈循环」节）。范式跃迁、`-rank` vs `reverse(rank)` 的 robust 闸差异、换壳优于磨参数，同处该节。
   - **news/sentiment 专用修复方向**（通用菜单在此类数据上适得其反）已上移至 `wq-brain-alpha-optimization-v1` 的「news / sentiment 的专用修复方向」；完整方向集仍在 [`docs/reference/news_sentiment_playbook.md`](docs/reference/news_sentiment_playbook.md)。
2b. **按字段分布形态选修复方向**（WebDataScope 数据包）已上移为 `wq-brain-alpha-optimization-v1` Step B2 的「分布形态 → 修复方向映射」表。本地数据包体检档案（`<dataset>_<REGION>_<UNIVERSE>_Delay<N>.bin`）的读取规则见 [`../brain-alpha-research/references/webdatascope-data-quality.md`](../brain-alpha-research/references/webdatascope-data-quality.md)。
2c. **修复后体检硬门复验**（`check_expr_against_inspect`，`ok=True` 才允许进入 `create_multi_simulation`）已上移为 `wq-brain-alpha-optimization-v1` 的「体检硬门复验」节。
2d. **GLB emotion 族降相关失败实证（2026-08-06，不可重蹈）**。v53-v67 GLB 系列共 42 个 PASS_CHEAP 候选（全部 emotion 信号族），在 GLB region 上 **100% 被 PROD_CORRELATION 硬闸挡掉**：探针实测 prodCorr 0.82-0.86（>0.7），跨 2 前缀(sxN_p0q2/tdN_p0q2)、2 universe(MINVOL1M/TOPDIV3000)、多种 neutralization 均失败。**结论**：(a) 不要把同族 PASS_CHEAP 当可提交池盲提交——全是死路；(b) 要拿到可提交 alpha 必须**换信号方向/降相关（正交化或新数据）**，不是重提交同一族；(c) **换壳(group_rank→group_zscore)比磨参数更有效**（论坛铁律）；(d) winner 提交后周围 family 变 self wall，需做**更远 field-level move** 而非同族微调。提交探测零成本（硬闸失败不消耗周额度），但浪费时间——先 5 个多样化探针（不同前缀×universe×neutralization）确认 prodCorr 再决定是否全量。
3. USA REGULAR 修复保持 `TOP3000` 默认 universe。用其他 USA universe 时台账必须记录 TOP3000 失败原因与该 universe 回答的诊断问题。
4. 改了设置就写新的 settings fingerprint 进台账，避免同一修复被盲目重试。
5. 修复记录为新的轨迹步骤，不是无记录的覆盖。

## 验证清单

1. 确认修复后的候选有独立的 settings fingerprint 或表达式哈希。
2. 确认相关 WebDataScope failed count 为零（REGULAR `Failed RA == 0`，PPA `Failed PPA == 0`）后才推进候选。
3. 确认修复路径在 `trajectory_steps` 可见。
4. 确认 §2d 的 GLB emotion 族教训在修复决策时被读取（换壳>磨参数 / winner 周围 family 变 self wall / 先 5 探针再全量）。
