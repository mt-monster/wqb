---
name: brain-dataset-mining-experience
layer: L6
description: 每波 S6 收尾、或下一轮选字段前要读某区域某数据集的已验证机制与失败边界时使用：按区域 / 数据集沉淀字段级经验（中文文档 reports/dataset_experience/<region>_<ds>_campain.md）。只读台账，不回测、不判死、不替代闸门。
last_verified: 2026-09-29
---

# 数据集与字段挖掘经验

## 职责边界

- **本 skill 负责**：逐数据集的中文**经验沉淀**——已验证机制与失败边界，产出 `reports/dataset_experience/<region小写>_<真实dataset_id>_campain.md`。
- **本 skill 不做**：**只读台账**——不回测、不判死（判死 = ra-pipeline 步 9 的 dead-end 封存）、不写任何结构化台账（verdict / registry / ledger 键都不是本 skill 写的）；未回测 / 待出相关性的结论不得记为已验证。
- **上游 / 下游**：上游 = 本波已回测的数据集（DB `backtest_results`）；下游 = 下一轮 S-PRE / S1 / S2 读取。`data/wqb.db` 仍是数据与判定权威，Markdown 是供人与后续 agent 阅读的**派生**经验。

文件名沿用 `campain` 写法；数据集 id 来自平台 / DB，不把示例 `new18` 当作真实数据集。总结范围与索引维护在 [`reports/dataset_experience/README.md`](reports/dataset_experience/README.md)（仓库根相对）。

## 主流程连接

- **S6（步 9）**：先完成 S3 收批、S4 诊断，以及 `upsert_wave_result`（含 `verdict`，波结论的唯一写入口）之后，再调用本技能更新本波**每个实际回测的数据集**。（`s6_verdict_<wave>` 已废止，不要再写。）
- **S-PRE / S1**：读对应经验文件，按 region / delay / universe / 时间范围判断适用性。
- **S2**：机制文档引用相关经验与 alpha / wave，说明继承什么、避免什么、准备证伪什么。经验**不替代** GEM、字段体检或门禁。
- **判死粒度**：单次失败只约束「字段搭配＋结构＋设置」，**不能据此判死整个字段或数据集**；推翻旧经验须提供新证据。
- 一次纠错复验的边界见 [`post-wave-reading.md`](../wq-brain-campaign-toolkit/references/post-wave-reading.md)（只有命中缺陷白名单才允许，且只做一次）。

## 更新方法

首选现有 campaign 节点（不新增编排器）：

```text
mcp__wq-brain-http__workflow_campaign(
  region="EUR", stage="S6", subcommand="dataset-experience",
  dataset="news46", extra_args=["--delay", "1"], dry_run=True)
```

检查命令后同参数 `dry_run=False`；用 `workflow_task_status` 收取异步终态。

- 省略 `--waves`：累计该数据集**全部**已完成历史；只总结本次战役时显式传 `--waves 245,246,247,248,249`。
- 省略 `dataset`：覆盖筛选范围内**每个**已有完成回测的数据集。
- `--delay` 传**本战役的 delay**（D1 战役 `--delay 1`，D0 战役 `--delay 0`；只接受 0 / 1）。

兼容入口（仓库根，MCP venv；只是薄壳，参数解析与实现都在 `src/wqb/research/dataset_experience.py`，只读 DB、无平台请求）：

```powershell
& $WQ_PY tools/dataset_experience.py --region EUR --waves 245,246,247,248,249 --delay 1 [--dataset news46] [--dry-run]
```

默认输出固定到仓库 `reports/dataset_experience`，不随工作目录变化；`--dry-run` 只显示计划、不写文件。

### 核验（不能只凭任务 `succeeded`）

工具只替换 `BEGIN/END WQB DATASET EVIDENCE` 标记之间的自动证据，保留块外人工复盘；它打印 `UPDATED` / `UNCHANGED` / `DRY-RUN <path> rows=<n>`。收到终态后核对文件：

```powershell
Select-String -Path reports/dataset_experience/eur_news46_campain.md -Pattern '范围：|筛选：'
```

**期望**：`范围：` 行写出 `<REGION> / <dataset>`、本次传入的全部波次与「去重后 N 条已完成回测」（N = `rows=`）；`筛选：` 行的 `delay=` / `waves=` 与你传的参数一致。波次缺失或 N 偏少 → 说明这次没覆盖到，重新读取再刷新（发现他人并发编辑时也是重新读取再刷新——写入会拒绝覆盖被别人改过的文件）。

## 文件骨架（块外写在哪里）

```markdown
# <REGION> · <dataset> 因子挖掘经验
<!-- BEGIN WQB DATASET EVIDENCE -->
## 数据库证据快照 / ## 字段证据与使用经验 / ## 已完成候选逐条记录   ← 自动生成，不要手改
<!-- END WQB DATASET EVIDENCE -->
## 人工机制复盘        ← 块外，人工写在这里
### 1. 范围与设置
### 2. 字段经验
### 3. 机制对照
### 4. 后续决策
### 5. 边界
```

新文件首次生成时块外只有一行占位（「待结合原式、字段语义与平台核查补充」）；分析写在 `## 人工机制复盘` 之下。

## 人工机制复盘（五节各写什么）

1. **范围与设置**：区分新增回测、历史复核、只读研究、数据诊断；保留波号、alpha id、时间及可复现原式。
2. **字段经验**：真实 id、平台含义、类型、coverage / users 与读取日期；分别说明主信号、分母、条件、分组轴。名称与描述冲突时写明，不凭名称脑补。
3. **机制对照**：同一条候选的 Sharpe / Fitness / 2Y / Sub / Robust / 换手及实测相关性；缺失写「未核实」，**不拼接不同候选的最好指标**。平台 UNITS 等口径警告随原式保留；有测量缺陷的比较不写成机制有效 / 无效的证据。
4. **后续决策**：有效线索、已失败结构、失败原因、应跳过的重复尝试、重新开启所需证据。未回测结构只放待验证区；有增益但未达增强资格的研究问题，引用 ledger 键 `research_leads_w<W>`（字段格式见 [`post-wave-reading.md`](../wq-brain-campaign-toolkit/references/post-wave-reading.md)），与 near / ready 分开；不因候选未达标就丢弃未解决的研究问题。
5. **边界**：IS 不是 OS；冷门不保证低相关；空失败列表不等于 Regular 全通过；near / combo 不等于可提交；收益的因果解释只能标为**推论**。

## 完成后

给出简短的「输入 → 结论 → 下一步」摘要。**结构化结论不经本 skill 回写**：波结论 = `upsert_wave_result`，判死 = 步 9 的 `seal_dead_end`，registry 走 registry 写入契约；本文件不成为第二套闸门。
