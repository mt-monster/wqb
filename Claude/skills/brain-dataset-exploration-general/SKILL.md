---
last_verified: 2026-09-28
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

## 职责边界

- **本 skill 负责**：**数据集级**审计与分类（选集）：该数据集值不值得挖、类别/覆盖/拥挤度画像
- **本 skill 不做**：不做单字段深度评测（→ `brain-datafield-exploration-general`）；不做特征工程决策；**区域/universe 档位一律引用 `src/wqb/config.py`，不得自行维护区域表**
- **上游 / 下游**：上游 = S0 白名单；下游 = 单字段探索



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

## Phase 3: 数据集级定性（战役级评分见 ppa-mining / toolkit）
**本 skill 在此阶段只做数据集级定性**（该数据集值不值得挖、类别/覆盖/拥挤度画像）。战役级双门槛评分与两段式探针由 `wq-brain-ppa-mining §1.0`（权威定义）与 `wq-brain-campaign-toolkit` 的 `score_datasets.py`（执行，公式见其 `references/probe-scoring-v2.md`）负责，本 skill 不重复维护其数值，需要时直接路由：
- 评分公式、tier1/tier2 硬门槛 → `wq-brain-ppa-mining §1.0`；
- 两段式探针（Stage A `EARLY_RED` 省批）与三灯判定（v2）→ `wq-brain-campaign-toolkit` references。

## Phase 4: 增强描述与分析
1. **描述**：撰写详细描述（业务背景、方法论、典型取值）。
2. **单字段分析**：对数据集内需要深入理解的字段，路由到 `brain-datafield-exploration-general` 做单字段评测（"关键字段"的判据与 6 种评测方法见该 skill）——本 skill 不做单字段深度评测。

## Phase 5: 整合
1. **调研**：查阅论坛帖子获取社区见解（`brain-forum-browse` skill 或 `mcp__wq-brain-http__search_forum_posts`）。
2. **不做 alpha 概念头脑风暴**：特征/alpha 概念生成是 `brain-data-feature-engineering` 的职责，本 skill 到此为止的产出是数据集级画像与字段分类。

## 关键：Region → Universe 映射（用于 `get_datasets`）

**本 skill 不维护 Region→Universe 快照表**（见职责边界）。`get_datasets` **严格按照该区域的有效 universe 过滤**；唯一权威来源是 `get_platform_setting_options` 的实时返回值（固化的合法档位以 `src/wqb/config.py::REGIONS` 为准）。传错 universe 会**静默返回空结果**（假阴性——数据其实存在，但你却会得出"没有数据"的结论）。

- 用 `get_platform_setting_options` 获取权威 universe 列表（返回每个区域的有效 universe）。
- `get_datafields` 同样需要 `dataset_id` + 区域 universe。
- 某区域若在实时返回值里**不是有效 EQUITY 区域**（如 JPN），不要调用 `get_datasets(region=...)`，直接按"无 EQUITY 数据集"处理。
- 如果某区域返回 0 个数据集，先怀疑 universe 传错，再怀疑该区域为空。

## 核心职责
- **深入挖掘**：一次专注于一个数据集。
- **清点盘存**：为所有字段编目。
- **文档化**：改进描述。
