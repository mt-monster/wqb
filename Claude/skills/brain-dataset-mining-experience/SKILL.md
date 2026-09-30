---
name: brain-dataset-mining-experience
layer: L6
description: 按区域和数据集沉淀字段级因子挖掘经验，生成或更新如 eur_news18_campain.md 的中文文档。用于每波 S6 复盘、总结已挖数据集，以及下一轮选字段前读取已验证机制与失败边界。只读 DB、仅产出派生 Markdown，不替代回测、提交判定或挖掘编排。
last_verified: 2026-09-28
---

# 数据集与字段挖掘经验

## 职责边界

- **本 skill 负责**：逐数据集的中文**经验沉淀**：已验证机制与失败边界，产出 `reports/dataset_experience/<region>_<ds>_campain.md`
- **本 skill 不做**：**只读 DB、仅产出派生 Markdown**：不回测、不判死（判死 = ra-pipeline 步 9 的 dead-end 封存）、不改 DB 结构化台账；未回测/待出相关性的结论不得记为已验证
- **上游 / 下游**：上游 = 本波已回测的数据集；下游 = 下一轮 S-PRE/S1/S2 消费



产物：`reports/dataset_experience/<region小写>_<真实dataset_id>_campain.md`。
沿用用户的 `campain` 文件名写法；数据集 id 来自平台/DB，不把示例 `new18` 当作真实数据集。
`data/wqb.db` 仍为数据与判定权威，Markdown 是供人和后续 Agent 阅读的派生经验。

## 主流程连接

- **S6**：先收回回测、完成 S4 与 `s6_verdict_<wave>` 回写，再调用本技能更新本波每个实际回测数据集。
- **S-PRE／S1**：读对应经验文件，按 region/delay/universe/时间范围判断适用性。
- **S2**：机制文档引用相关经验与 alpha/wave，说明继承什么、避免什么、准备证伪什么。经验不替代 GEM、字段体检或门禁。
- 单次失败只约束"字段搭配＋结构＋设置"，本 skill **只记搭配 + 失败指标**，**不下"已死/判死"结论**（判死 = ra-pipeline 步 9 的 dead-end 封存）；推翻旧经验须提供新证据。

## 更新方法

首选现有 campaign 节点（不新增编排器）：

```text
mcp__wq-brain-http__workflow_campaign(
  region="EUR", stage="S6", subcommand="dataset-experience",
  dataset="news46", extra_args=["--delay", "1"], dry_run=True)
```

检查命令后同参数 `dry_run=False`；用 `workflow_task_status` 收取异步终态。
省略 wave 累计该数据集全部已完成历史；只总结本次战役时显式传 `--waves 245,246,247,248,249`。
省略 dataset 覆盖筛选范围内每个已有完成回测的数据集。D1 战役始终传 `--delay 1`。

兼容入口（仓库根，MCP venv）：

```powershell
& $WQ_PY tools/dataset_experience.py --region EUR --waves 245,246,247,248,249 --delay 1
```

权威实现为 `src/wqb/research/dataset_experience.py`（唯一逻辑体，只读 DB、无平台请求）。
三入口关系：**首选** `workflow_campaign` 的 `dataset-experience` 子命令（不新增编排器）；**兼容入口** `tools/dataset_experience.py` 是同一实现的 CLI 薄封装；两者最终都调 `src/wqb/research/dataset_experience.py` 这一唯一逻辑体。
默认输出固定到仓库 `reports/dataset_experience`，不随 toolkit 的工作目录变化。
收取 S6 结果后核对仓库文件的波次和行数，不能只凭任务 succeeded 判定经验已刷新。
工具仅替换 `BEGIN/END WQB DATASET EVIDENCE` 标记内的自动证据，保留块外人工复盘。
新的分析写在块外；发现他人并发编辑时重新读取再刷新。

## 人工机制复盘

1. **范围与设置**：区分新增回测、历史复核、只读研究和数据诊断；保留波号、alpha id、时间及可复现原式。
2. **字段经验**：真实 id、平台含义、类型、coverage/users 与读取日期；分别说明主信号、分母、条件、分组轴。名称与描述冲突时写明，不凭名称脑补。
3. **机制对照**：同条候选的 Sharpe/Fitness/2Y/Sub/Robust/换手及实测相关性；缺失写未核实，不拼接不同候选最好指标。平台UNITS等口径警告须随原式保留；有**测量缺陷**的比较（跨 UNITS、跨 universe、跨延迟、跨区域、数据周期不一致）不写成机制有效/无效的证据。
4. **后续决策**：有效线索、已失败结构、失败原因、应跳过的重复尝试、重新开启所需证据。未回测结构只放待验证区；有增益但未达增强资格的研究问题引用ledger `research_leads_w<W>`，与near/ready分开。一次纠错复验的边界见主流程链接的选波清单，不因候选未达标就丢弃未解决的研究问题。
5. **边界**：IS 不是 OS；冷门不保证低相关；空失败列表不等于 Regular 全通过；near/combo 不等于可提交；收益因果解释只能标为推论。

`s6_verdict_*`／registry 的结构化结论由上游 S6 完成回写（本 skill 只消费、不回写），经验文件不成为第二套闸门。
`reports/dataset_experience/README.md` 维护总结范围与索引。完成后给出简短的输入→结论→下一步摘要。
