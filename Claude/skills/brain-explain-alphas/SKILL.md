---
last_verified: 2026-09-28
name: brain-explain-alphas
description: "提供分析并解释 WorldQuant BRAIN alpha 表达式的逐步工作流。 当用户要求解释某个具体 alpha 表达式、某个 datafield 的作用、或算子如何协同工作时使用。 包括数据字段查询（data field lookup）、算子分析与外部调研等步骤。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







# Alpha 表达式解释工作流

## 职责边界

- **本 skill 负责**：收益来源归因与机制解释（按需：Mode B 换概念前先查概念重叠）
- **本 skill 不做**：不改表达式、不回测、不判提交；**不是每候选必经**（按需调用）
- **上游 / 下游**：上游 = 具体 alpha；下游 = optimization-v1 Mode B



本手册提供分析并解释 WorldQuant BRAIN alpha 表达式的工作流。
完整详细工作流与示例见 [reference.md](reference.md)。

## 第 1 步：拆解 Alpha 表达式
把 alpha 表达式拆解为基本组成部分：数据字段与算子。
*示例：* `quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))`
- **数据字段**：`oth423_find`、`shrt3_bar`
- **算子**：`quantile`、`ts_regression`、`group_mean`、`vec_max`

## 第 2 步：分析数据字段
使用 `mcp__wq-brain-http__get_datafields` 工具获取每个数据字段的详细信息。
- 必填/推荐参数：`instrument_type`（如 `EQUITY`）、`region`、`delay`、`universe`、`data_type`（`MATRIX`/`VECTOR`）、`search`（关键字）。
- 识别：工具类型（Instrument Type）、区域（Region）、延迟（Delay）、股票池（Universe）、数据类型（Data Type，Matrix/Vector）。
- 注意：Vector 数据需要聚合（如 `vec_max`）。

## 第 3 步：理解算子
使用 `mcp__wq-brain-http__get_operators` 工具理解每个算子的作用。

## 第 4 步：查阅官方文档
使用 `mcp__wq-brain-http__get_documentations` 和 `mcp__wq-brain-http__get_documentation_page` 深入理解相关概念（如向量数据处理）。

## 第 5 步：借助外部调研拓宽理解（可选，仅做理解性检索）
在 arXiv 上搜索学术论文以辅助**理解** alpha 思路：`python scripts/arxiv_api.py "<keywords>" -n 10`（脚本随本 skill 附在 `scripts/` 下）。
本 skill 的 arXiv 检索**只服务于解释/理解**，**不做概念提取、不落盘候选池**——概念提取与 `--concepts --llm` 结构化落盘属 `wq-brain-alpha-optimization-v1` Step B3（见其 `arXiv_API_Tool_Manual.md`）的职责，勿在此重复。

## 第 6 步：综合并解释
按以下结构组织解释：
1. **思路（Idea）**：策略的高层概述。
2. **数据理由（Rationale for data）**：为什么选这些字段？它们代表什么？
3. **算子理由（Rationale for operators）**：它们如何变换数据？
4. **进一步启发（Further Inspiration）**：可能的改进方向。

## 附录：向量数据（Vector Data）
向量数据在每个交易日对每只工具记录多条事件（如新闻）。它需要聚合（如 `vec_mean`、`vec_sum`）才能变成可被其他算子使用的矩阵值。

## 衔接协议
- **上游（分场景）**：
  - 场景①（Mode B 换概念前查概念重叠）：上游 = `wq-brain-alpha-optimization-v1` Step B3（动手换概念之前）；
  - 场景②（提交前收益来源确认）：上游 = `brain-calculate-alpha-selfcorr-quick`（本地快筛后的候选）。
- **本 skill 角色**：S4 **按需**工具（2026-09-01 精简：从每候选必经改为按需调用）。两个触发场景用**硬判据**：
  ① **Mode B 换概念前**（`wq-brain-alpha-optimization-v1` Step B3 换信号概念/字段组合之前）查与既有 book 的概念重叠；
  ② **robustness Phase C 判定 CONDITIONAL 且用户要求**复核收益来源时。
  日常近闸候选（robustness 判定 PASS 或 REJECT）不必逐条归因。
- **下游**：**brain-alpha-robustness**（过拟合/稳健性必经闸，S4→S5）→ `tools/submit_verdict.py`（提交层权威判定；`brain-alpha-judge` 仅作可选参考评审）。
