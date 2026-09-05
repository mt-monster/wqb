# Alpha 表达式解释工作流

本手册提供分析并解释 WorldQuant BRAIN alpha 表达式的分步工作流。按本指南操作，可高效收集必要信息，理解任何 alpha 背后的逻辑与潜在策略。

## 第 1 步：拆解 Alpha 表达式

第一步将 alpha 表达式拆解为基本组成部分：数据字段与算子。

例如，给定表达式 `quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))`：

- **数据字段**：`oth423_find`、`shrt3_bar`
- **算子**：`quantile`、`ts_regression`、`group_mean`、`vec_max`

## 第 2 步：分析数据字段

使用 MCP 工具 `get_datafields`（服务器 `wq-brain-http`）获取每个数据字段的详细信息。

示例调用：

```
mcp__wq-brain-http__get_datafields(instrument_type="EQUITY", region="ASI", delay=1, universe="MINVOL1M", data_type="VECTOR", search="shrt3_bar")
```

高效检索技巧：

- **指定参数**：尽量提供已知的全部信息，包括 `instrument_type`、`region`、`delay`、`universe` 与 `data_type`（MATRIX 或 VECTOR）。
- **迭代检索**：若第一次未找到目标字段，尝试不同的参数组合。例如 ASI 区域有两个 universe：`MINVOL1M` 与 `ILLIQUID_MINVOL1M`。
- **核对数据类型**：务必确认数据是 MATRIX（每只股票每天一个值）还是 VECTOR（每只股票每天多个值）。这对理解数据如何被使用至关重要。

示例字段信息：

- `oth423_find`：ASI 区域 "Fundamental Income and Dividend Model" 数据集的 matrix 数据字段，表示 "Find score"，可能反映基本面吸引力。
- `shrt3_bar`：ASI 区域 "Securities Lending Files Data" 数据集的 vector 数据字段，提供评级向量（1-10），表示借入某只股票的意愿强度，是卖空兴趣的代理指标。

## 第 3 步：理解算子

使用 MCP 工具 `get_operators`（服务器 `wq-brain-http`）获取全部可用算子及其描述。

该命令的输出信息丰富。本手册附录提供了最常用算子的速查表。

## 第 4 步：查阅官方文档

对于更复杂的主题，官方 BRAIN 文档是宝贵资源。使用 `get_documentations` 工具（MCP `wq-brain-http`）查看可用文档列表，再用 `get_documentation_page` 阅读具体页面。

示例：为更好理解 vector 数据字段，可查阅 "Vector Data Fields" 文档（`vector-datafields`）。该文档说明：vector 数据每个工具每天包含多个值，必须先通过 vector 算子聚合，才能与其他算子一起使用。

## 第 5 步：借助外部调研拓宽理解（可选——使用 arxiv_api.py 脚本获取最新研究论文）

为获取前沿思路与灵感，可使用本 skill 附带的 `arxiv_api.py` 脚本在 arXiv 上搜索学术论文。

工作流：

1. **识别关键词**：基于对 alpha 的分析，识别相关关键词。对于示例，关键词为："short interest"、"fundamental analysis"、"relative value"、"news sentiment"。
2. **运行脚本**（从本 skill 的 `scripts/` 目录执行）：

```
python scripts/arxiv_api.py "your keywords here" -n 10
```

若本地无此脚本，可回退到 HTTPS arXiv API 查询（https://export.arxiv.org/api/query），或跳过此步并在解释中注明。

## 第 6 步：综合并解释

收集完必要信息后，按清晰简洁的格式组织解释。推荐模板：

- **思路（Idea）**：alpha 策略的高层概述。
- **数据理由（Rationale for data）**：为什么选择这些数据字段？它们代表什么？
- **算子理由（Rationale for operators）**：算子如何逐步变换数据生成最终信号。
- **进一步启发（Further Inspiration）**：基于研究的新 alpha 思路。

## 故障排查（Troubleshooting）

- **SSL 错误**：运行访问互联网的 Python 脚本时若遇到 `CERTIFICATE_VERIFY_FAILED` 错误，可借助 AI 修改脚本或调整执行方式。

## 附录 A：理解 Vector 数据

Vector 数据是一种特殊的数据字段类型：每个工具每天记录的事件数量可以变化。这与标准 matrix 数据形成对比——matrix 数据每个工具每天只有一个值。

例如，新闻情绪数据通常是 vector，因为一只股票一天内可能有多篇新闻文章。要在大多数 BRAIN 算子中使用此类数据，必须先通过 vector 算子将其聚合成单一值。
