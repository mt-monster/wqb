---
last_verified: 2026-08-22
name: brain-feature-implementation
description: "根据 idea Markdown 文档实现 WorldQuant Brain 特征：下载数据集并生成文档中定义的 alpha 表达式 （alpha expressions / dataset download / expression generation）。 当用户提供 idea 文档、要求生成 alpha 表达式或下载数据集时使用。"
layer: L2
allowed-tools:
  - Read
  - Bash
  - TaskCreate
---







# Brain 特征实现（Brain Feature Implementation）

## 描述
本 skill 将 WorldQuant Brain idea 文档（Markdown）自动转换为可执行的 Alpha 表达式，并为每种独立的 idea 模式处理数据集下载和代码生成。

## 工作范围
*   本 skill 通过 `scripts/` 下的 Python 脚本操作本地 CSV 文件与 Brain 下载接口。
*   **skill 层不直接调用 WorldQuant Brain MCP 工具**；数据下载由 `fetch_dataset.py` 内部通过 `ace_lib` 调用 Brain API（需 `config.json` 提供凭据）。
*   **禁止编写自定义 Python 脚本**（如 `python -c ...` 或新建 `.py` 文件）来检查数据或生成表达式。必须使用 `scripts/implement_idea.py` 工具。
*   不要尝试在平台上提交 alpha 或运行模拟。只关注在本地生成表达式文件。

## 前置准备：config.json
`fetch_dataset.py` 从 **本 skill 根目录**读取 `config.json` 获取 Brain 登录凭据。首次使用前在该目录创建 `config.json`：

```json
{
  "BRAIN_CREDENTIALS": {
    "email": "your_brain_email@example.com",
    "password": "your_brain_password"
  }
}
```

缺文件或字段时脚本会打印错误并退出（不消耗平台资源）。凭据不要提交到版本库。

## 操作步骤

1.  **分析 idea 文档**
    *   读取提供的 markdown 文件。
    *   提取以下元数据：
        *   **数据集 ID**（如 `analyst15`）
        *   **区域**（如 `GLB`）
        *   **延迟**（如 `1` 或 `0`）
    *   *若缺少任何元数据，请向用户澄清。*

2.  **下载数据集**
    *   使用提取的参数执行下载脚本。
    *   **定位脚本**：
        *   检查当前工作目录（`ls -R` 或 `Get-ChildItem -Recurse`）。
        *   找到 `fetch_dataset.py` 的路径，它通常在 `brain-feature-implementation/scripts` 或 `scripts` 下。
    *   **运行命令**：
        *   运行前先切换到脚本所在目录。
        *   命令：
            ```bash
            cd <PATH_TO_SCRIPTS_FOLDER> && python fetch_dataset.py --datasetid <ID> --region <REGION> --delay <DELAY>
            ```
    *   等待下载完成。脚本会在 `../data/` 下创建文件夹。

3.  **规划实现**
    *   扫描 markdown 文件中的 **特征定义（Feature Definitions）** 或 **公式（Formulas）**。
    *   查找类似 `Definition: <formula>` 的模式或描述数学公式的代码块。
    *   使用 `TaskCreate` 工具创建计划，为每个独立的 idea/公式建立一个条目。
        *   *标题*：idea 名称或 ID（如 "3.1.1 Estimate Stability Score"）。
        *   *描述*：具体的模板公式（如 `template: "{st_dev} / abs({mean})"`）。

4.  **执行实现**
    *   对 Todo 列表中的每一项：
        *   **构造模板**：
            *   使用 Python format string 语法 `{variable}`。
            *   `{variable}` 必须匹配数据集中字段的 **后缀**（如 `mean`、`st_dev`、`gro`）。
            *   **关键**：模板中不要包含完整前缀或 horizon，脚本会自动检测。
            *   *正确示例*：对于 `anl15_gr_12_m_gro / anl15_gr_12_m_pe`，使用模板 `{gro} / {pe}`。
            *   *错误示例*：`{anl15_gr_12_m_gro} / {pe}`（包含前缀）。
            *   *错误示例*：`${gro} / ${pe}`（Shell 语法）。
        *   **确定数据集文件夹**：`{ID}_{REGION}_delay{DELAY}`（如 `analyst10_GLB_delay1`）。
        *   **运行脚本**：
            *   切换到包含 `implement_idea.py` 的文件夹（如步骤 2 所述）。
            *   命令：
                ```bash
                cd <PATH_TO_SCRIPTS_FOLDER> && python implement_idea.py --template "<TEMPLATE_STRING>" --dataset "<DATASET_FOLDER_NAME>"
                ```
            *   *注意*：脚本只接受 `--template` 和 `--dataset`。不要传其他参数，如 `--filters` 或 `--groupby`。
            *   **严格规则**：不要用 `python -c` 或创建临时脚本验证或处理结果。信任 `implement_idea.py` 的输出。
        *   验证输出（生成的表达式数量）。
        *   将 Todo 项标记为完成。

5.  **完成输出**
    *   所有 Todo 项完成后，将所有生成的表达式合并到单个文件中。
    *   **运行合并脚本**：
        *   切换到包含脚本的文件夹。
        *   命令：
            ```bash
            cd <PATH_TO_SCRIPTS_FOLDER> && python merge_expression_list.py --dataset "<DATASET_FOLDER_NAME>"
            ```
    *   这会在数据集目录下生成 `final_expressions.json`。
    *   向用户报告唯一表达式的总数以及最终文件的路径。

## 脚本依赖
本 skill 依赖其 `scripts/` 目录下的以下脚本：
- `fetch_dataset.py`：从 Brain API 下载数据。
- `implement_idea.py`：根据模板生成 alpha 表达式。
- `ace_lib.py` 与 `helpful_functions.py`：支持库。
