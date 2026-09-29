---
last_verified: 2026-09-29
name: brain-explain-alphas
description: "拆解并解释一个 WorldQuant BRAIN alpha 表达式：数据字段含义、算子作用、收益来源归因；并可在 Mode B 换概念前做与本区 book 的概念重叠检查。当用户要求解释某个具体 alpha 表达式、某个 datafield 的作用、算子如何协同，或要确认候选的收益来源 / 概念是否与既有 alpha 重叠时使用。按需调用，不是每候选必经。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# Alpha 表达式解释工作流

## 职责边界

- **本 skill 负责**：拆解并解释表达式（数据理由 / 算子理由 / 收益来源归因）；按需做**概念重叠检查**（Mode B 换概念前，第 7 步，有对应的程序 `tools/concept_overlap.py`）。
- **本 skill 不做**：不改表达式、不回测、不判提交；**不是每候选必经**——按需调用，跳过它不影响下游 `brain-alpha-robustness` 入场。
- **上游 / 下游**：上游 = 具体 alpha（常在 `brain-calculate-alpha-selfcorr-quick` 之后）；下游 = `wq-brain-alpha-optimization-v1` Mode B（换概念）、`brain-alpha-robustness`（S4 → S5 必经闸）。链图：`selfcorr-quick →（可选）explain-alphas → robustness`。

完整详细工作流、成品示例与两张情景卡见 [reference.md](reference.md)。

## 第 1 步：拆解 Alpha 表达式

把表达式拆成数据字段与算子。

*示例：* `quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))`

- **数据字段**：`oth423_find`、`shrt3_bar`
- **算子**：`quantile`、`ts_regression`、`group_mean`、`vec_max`

## 第 2 步：分析数据字段

用 `mcp__wq-brain-http__get_datafields` 取每个字段的详细信息。**真实签名**：

`get_datafields(region, dataset_id, universe, delay=1, data_type="", search=None, filter_sharpe=True)`

- **必传**：`region`、`dataset_id`、`universe`（`dataset_id` 未知时显式传 `None`，靠 `search` 找）。**没有 `instrument_type` 参数**（工具内部写死 EQUITY）。
- **推荐**：`data_type`（`MATRIX` / `VECTOR`）、`search`（用**完整 field id**）。
- **解释既有 alpha 时必须 `filter_sharpe=False`**：默认 `True` 会静默过滤 OS / IS Sharpe < 0 的字段，而被解释 alpha 的字段可能恰是 Sharpe < 0（作者取了负号）——按名字搜得「空」并不代表字段不存在。
- **返回为空时按序排查**：换 universe / region → 核对 delay → 核对 `dataset_id`（传 `None` 重搜）。
- 识别：数据类型（Matrix / Vector）、区域、延迟、股票池、所属数据集。**VECTOR 必须先经 `vec_*` 聚合；MATRIX 禁用 `vec_*`**（`platform_constraints.json` 的 `vec_rules`，KOR 24/24 ERROR 实证）。

## 第 3 步：理解算子

用 `mcp__wq-brain-http__get_operators` 取算子说明（**无参数、返回全量**，取回后只读表达式里用到的几个）。某个算子查不到 → 先怀疑是幽灵 / 未核验算子（`known_ops` 与 `ghost_ops` 见 `platform_constraints.json`），别当成「平台文档缺失」。

## 第 4 步：查阅官方文档

`get_documentations`（列表）+ `get_documentation_page(page_id)`（读页）。例：为理解 vector 字段读 `vector-datafields` 页。

## 第 5 步：借助外部调研拓宽理解（可选）

用全库**唯一一份**脚本：`$WQ_PY Claude/skills/wq-brain-alpha-optimization-v1/scripts/arxiv_api.py "<通用关键词>" -n 10`。

**外发边界**：查询词发往 `export.arxiv.org`——**只发通用关键词**（如 `short interest`、`relative value`），**不发**未公开表达式、数据集 / 字段名、alpha id。`--llm` 会另把公开论文摘要发给第三方 LLM，密钥与用法见 optimization-v1 的 [`arXiv_API_Tool_Manual.md`](../wq-brain-alpha-optimization-v1/arXiv_API_Tool_Manual.md)。脚本不可用时可跳过本步并在解释里注明。

## 第 6 步：综合并解释

按四段组织（成品示例见 reference.md §成品示例）：

1. **思路（Idea）**：策略的高层概述。
2. **数据理由（Rationale for data）**：字段代表什么。**事实（取自数据集描述）与推测分开写**；收益来源要有证据——哪一年（`get_alpha_yearly_stats`）、PnL 曲线形状（`get_alpha_pnl`）；long / short 侧与行业集中度平台没有直接接口，**未核验就写「未核验」，不要编**。
3. **算子理由（Rationale for operators）**：算子如何逐步变换数据。
4. **进一步启发（Further Inspiration）**——**结构化 3 栏**，Mode B 才能消费：`新概念名` / `候选字段` / `预计与既有 book 的正交性（高 / 中 / 低 + 依据）`。

**落点**：默认写在本轮回复里；需要留痕就并入 S6 的 `wave_result.key_findings`。**不新造 ledger 键。**

## 第 7 步：概念重叠检查（按需；Mode B 换概念前）

输入 = 目标表达式（或已入库的 alpha id）+ 本区 book（`alphas` 表里 ACTIVE 的 alpha）。比对两个维度——**信号族**（字段集合）与**骨架指纹**（前 2 个算子）——与闸 PF / prod-first 同一口径：

```bash
$WQ_PY tools/concept_overlap.py --region <REGION> --alpha-id <ID>
$WQ_PY tools/concept_overlap.py --region <REGION> --expr "<表达式>"            # 尚未入库的想法
$WQ_PY tools/concept_overlap.py --region <REGION> --expr "..." --book-json book.json   # book 用 get_user_alphas 的 ACTIVE 导出
```

输出 `verdict`：`HIGH`（字段集合相同，或同骨架且字段 Jaccard ≥ 0.5）→ 换概念；`MEDIUM` → 可继续但优先换骨架 / 字段，提交前必测 SELF / PROD；`LOW` / `CLEAR` → 概念基本不同。**这是启发式提示，不是平台判定**：不能凭它放行或否决，真实相关性只有 `check_self_correlation` / `check_correlation` 给得出。

## 附录：向量数据（Vector Data）

向量数据每个交易日对每只工具记录多条事件（如新闻）。要变成可被其他算子使用的矩阵值，必须先经 vector 算子聚合：`vec_avg`、`vec_sum`、`vec_max`、`vec_min`、`vec_count`、`vec_range`、`vec_stddev`（`vec_norm` 不在 `known_ops`，用前先 `get_operators` 复核）。**没有 `vec_mean`**——均值聚合是 `vec_avg`。全集以 `platform_constraints.json` 的 `vector_only_ops` 为准。
