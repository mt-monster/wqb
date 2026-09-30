---
last_verified: 2026-09-28
name: brain-datafield-exploration-general
description: "提供 6 种经过验证的方法来评估 WorldQuant BRAIN 平台上的新数据字段（datafield）。 涵盖覆盖率（coverage）、非零值、更新频率、取值范围、中心趋势与分布形态的评测方法。 当用户想了解某个具体 datafield 时使用（如\"这个字段是什么？\"\"它多久更新一次？\"）。"
layer: L1
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







**运行环境**：所有 Python 命令使用 MCP venv（`$WQ_PY`），确保依赖（requests/pandas/ply）可用。不要使用系统 Python。

# 评估新数据字段的 6 种方法

## 职责边界

- **本 skill 负责**：**单字段级**评测（覆盖/非零/更新频率/取值范围/中心趋势/分布形态）
- **本 skill 不做**：不选数据集（上游已定）；不做特征工程决策；不生成表达式
- **上游 / 下游**：上游 = 数据集探索；下游 = 特征工程决策 / S1 字段白名单



本 skill 提供 6 种方法，用于快速评估 WorldQuant BRAIN 平台上的新数据字段（datafield）。
完整指南与详细示例见 [reference.md](reference.md)。

**重要**：运行这些模拟时使用 **Neutralization: None**、**Decay: 0**、**Test Period: P0Y0M**。
**指标**：查看 IS Summary 中的 **Long Count** 与 **Short Count**。

## 前置：字段 type 确认（强制，先于任何评测）

`get_datafields` 返回的 `type` 元数据**仅供参考**：KOR 的做空兴趣（short-interest）/ 特殊收益（special-returns）/ 内幕交易（insider）/ 新闻（news）数据集实测中，字段元数据标为 VECTOR 仍会触发 `winsorize does not support event inputs`。因此**单字段诊断模拟是强制前置**，不能只信 `type` 标记：

- **VECTOR** 字段：直接用于 `rank()` / `ts_*` 等算子，`winsorize` 安全。
- **EVENT** 字段：在任何 `winsorize` / `rank` / `ts_*` 之前，一律先用 `ts_event_*`（`ts_event_sum` / `ts_event_count` / `ts_event_mean`）聚合为逐日数值序列。

EVENT 字段携带时间戳/发生标志，而非逐日数值序列，`winsorize(x, std=N)` 作用于 event 输入会硬性失败（`winsorize does not support event inputs`，全有或全无——批处理中只要一个 event 字段，整批模拟报错）；普通 `rank()` / `ts_rank()` / `ts_mean()` 也可能按引擎类型检查拒绝 EVENT 输入。诊断时对事件风格数据集默认假设 `winsorize` 作用于 event，优先 `ts_event_*` / 去掉 `winsorize`。

## 1. 基础覆盖率分析（Basic Coverage Analysis）
*   **表达式**：`datafield`（VECTOR 字段可直接用于 `rank()` / `ts_*` 等算子；`vec_*` 是横截面算子，通常不是单股信号想要的）
*   **解读**：覆盖率 % =（Long Count + Short Count）/ 股票池大小（Universe Size）。

## 2. 非零值覆盖率
*   **表达式**：`datafield != 0 ? 1 : 0`
*   **解读**：真实覆盖率（剔除零值）。区分缺失数据（NaN）与真实零值。

## 3. 数据更新频率分析
*   **表达式**：`ts_std_dev(datafield, N) != 0 ? 1 : 0`
*   **解读**：更新频率。改变 `N`：
    *   `N=5`（周）：计数低说明按周更新。
    *   `N=22`（月）：按月更新。
    *   `N=66`（季度）：按季度更新。

## 4. 数据取值范围分析
*   **表达式**：`abs(datafield) > X`
*   **解读**：检查数值范围。改变 `X`（如 1、10、100）以检查量纲（例如是否已归一化到 -1 到 1？）。

## 5. 中心趋势分析
*   **表达式**：`ts_median(datafield, 1000) > X`
*   **解读**：一段时间内的典型取值（5 年中位数）。改变 `X` 以找出中心值。

## 6. 数据分布形态分析
*   **表达式**：`X < scale_down(datafield) && scale_down(datafield) < Y`
*   **解读**：分布形态。`scale_down` 将数据映射到 0-1。改变 `X` 与 `Y`（如 0.1-0.2）以检查分桶。

## 备注：向量数据（VECTOR）
VECTOR 字段应**直接**用于时间序列 / 排名类算子，如 `rank()`、`ts_rank()`、`ts_mean()`、`ts_zscore()`。**不要**把它们包在 `vec_op()` / `vec_sum()` / `vec_mean()` 中——这些是**横截面**算子，通常产生与单股时间序列信号不同的（按日、跨资产的）信号。

## 附录：批量字段收割（战役级，走 toolkit；非本 skill 的 6 种单字段方法）
本 skill 的 6 评测法适合**单字段定性**。战役级**全量字段收割**走 `wq-brain-campaign-toolkit` 的 `scan_fields.py`，落 typed catalog（`reference/<region>_<dataset>_fields.json`，字段级含 type/coverage/userCount/alphaCount；data_type 由字段 type 众数推断）——该 catalog 是 toolkit `gate.py` 闸2/3 的数据源。
⚠️ **陷阱：GET /data-fields 裸 `dataset=` 被平台静默忽略**（返回全宇宙、10000 条上限），必须用 `dataset.id=<id>`（KOR 2026-08-15 实测）。字段 `type` 确认与 EVENT 处理见上方「前置」节。
