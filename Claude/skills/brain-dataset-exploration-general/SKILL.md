---
last_verified: 2026-08-22
name: brain-dataset-exploration-general
description: "提供对 WorldQuant BRAIN 整个数据集进行深入挖掘分析的综合工作流。 包括数据集选择、字段分类（field categorization）、详细描述生成与跨平台调研等步骤。 当用户想\"审计某个数据集\"、\"对字段分类\"或\"探索新数据集\"时使用。"
layer: L1
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`），确保依赖（requests/pandas/ply）可用。不要使用系统 Python。

# 数据集探索专家工作流

本工作流指导数据集的深度分析与分类。
详细岗位手册与具体 MCP 工具策略见 [reference.md](reference.md)。

## Phase 1: 数据集选择与初步评估
1. **确定数据集**：根据战略重要性或用户需求选择。
2. **初步探索**：
   - 用 `get_datasets` 查找数据集。
   - 用 `get_datafields` 统计字段数并检查覆盖率。
   - 用 `get_documentations` 查找相关文档。

## Phase 2: 字段分类
将数据字段归入逻辑类别：
- **业务职能（Business Function）**：财务（Financials）、市场数据（Market Data）、预测（Estimates）等。
- **数据类型（Data Type）**：Matrix、Vector。
- **更新频率（Update Frequency）**：日频（Daily）、季频（Quarterly）。
- **层级（Hierarchy）**：一级 -> 二级 -> 三级（如 Financials -> Income Statement -> Revenue）。

## Phase 3: 数据集双门槛评分与两段式探针（战役级）
战役级数据集初筛用双门槛评分（权威定义见 `wq-brain-ppa-mining §1.0`，执行走 `wq-brain-campaign-toolkit` 的 `score_datasets.py`，公式见其 `references/probe-scoring-v2.md`）：
- 评分公式：`0.40*cov + 0.30/(1+log10(1+alphaCount)) + 0.20*log1p(fieldCount)/log1p(1000) + 0.10*min(valueScore,10)/10`（vs 缺失按 0.3）；
- tier1 硬门槛：cov≥0.85 且 alphaCount≤50 且 fieldCount≥10 → 直接攻；tier2（cov≥0.85/ac≤200/fc≥5）→ 探针先行；
- **两段式探针**：Stage A 评完 `EARLY_RED` 即不跑 Stage B（省批）；三灯判定（v2）细节指向 toolkit references。

## Phase 4: 增强描述与分析
1. **描述**：撰写详细描述（业务背景、方法论、典型取值）。
2. **分析**：对关键字段使用 `brain-datafield-exploration-general` 的技术来理解分布与形态。

## Phase 5: 整合
1. **调研**：查阅论坛帖子获取社区见解（`brain-forum-browse` skill 或 `mcp__wq-brain-http__search_forum_posts`）。
2. **Alpha 思路**：基于数据集特征头脑风暴 alpha 概念。

## 关键：Region → Universe 映射（用于 `get_datasets`）
`get_datasets` **严格按照该区域的有效 universe 过滤**。传错 universe 会**静默返回空结果**（假阴性——数据其实存在，但你却会得出"没有数据"的结论）。务必按区域使用正确的 universe：

| 区域 | 有效 universe（get_datasets） | 备注 |
|---|---|---|
| USA | `TOP3000` | |
| GLB | `TOP3000` | |
| KOR | `TOP600` | 192 个数据集 / 15 个类别（截至 2026-08） |
| ASI | `TOP500` | 163 个数据集 |
| EUR | `TOP2500` | 也支持 `TOP1200` / `TOP800` / `TOP400` |
| CHN | `TOP2000U` | **不是** `TOP3000` |
| JPN | — | **不是有效的 EQUITY 区域** —— `get_datasets` 返回 0 |
| HKG / IND / MEA / DEU / GBR | 区域特定 | 通过 `get_platform_setting_options` 核实 |

指导说明：
- 用 `get_platform_setting_options` 获取权威 universe 列表（返回每个区域的有效 universe）。
- `get_datafields` 同样需要 `dataset_id` + 区域 universe。
- JPN 不在 EQUITY 区域列表中，不要调用 `get_datasets(region=JPN)`。
- 如果某区域返回 0 个数据集，先怀疑 universe 传错，再怀疑该区域为空。

## 核心职责
- **深入挖掘**：一次专注于一个数据集。
- **清点盘存**：为所有字段编目。
- **文档化**：改进描述。
