# 数据集审计背景资料

> 主流程见 [`SKILL.md`](SKILL.md)。2026-09-29 由 436 行英文「Dataset Exploration Expert — Job Duty Manual」精简为本文：岗位描述、成功指标、职业发展等泛论已删；其中的「BRAIN 6-Tips」方法论**只在** [`brain-datafield-exploration-general`](../brain-datafield-exploration-general/SKILL.md) 保留一份（此前两处各抄一遍，且都带着不可用的算子）。

## 审计结论模板（对话里写，或存 `reports/dataset_audit_<REGION>_<ds>.md`）

1. **画像**：region / delay / universe（写明取自 `config.REGIONS` 还是 `get_platform_setting_options`）；字段数；`coverage` 分布与 `< 0.4` 占比；平台 `alphaCount` / `userCount` / `pyramidMultiplier`；category 点亮状态。
2. **分类**：`s1_semantic_<ds>` 的 signal / blocked 数量、各经济大类的字段数；非财报数据集多数落 `other` 是预期。
3. **代表字段**（≤ 12）：每个字段一行——`type`、`coverage`、`userCount`、`frequency`、`distribution_shape`（来自体检包，缺包写「不在包内」）、一行经济含义。
4. **风险与限制**：低覆盖、稀疏事件、VECTOR / EVENT 类型陷阱（见 datafield-exploration 的「类型先行」）、拥挤度（prod 墙风险）。
5. **机制假设**（**不写表达式**）：一句话经济叙事 + 建议的主 / 辅信号数据。
6. **下一步**：进 S0 白名单 / 交特征工程 / 放弃，及理由。

## MCP 工具速查（名字已按 `world-quant-brain-mcp/tools_*.py` 核对）

| 用途 | 工具 |
|---|---|
| 找数据集 / 字段 | `get_datasets` / `get_datafields`（`get_datasets` 传错 universe 会静默返回空） |
| 平台合法设置 | `get_platform_setting_options` / `get_operators` |
| 文档 | `get_documentations`（目录）/ `get_documentation_page`（单页；页名以目录为准） |
| 仿真（字段深挖用） | `create_simulation`（单条探针）/ `create_multi_simulation`（合批，见 datafield-exploration §0） |
| 论坛 / 赛事（默认不用） | `search_forum_posts` / `read_forum_post` / `get_glossary_terms` / `get_events` / `get_competition_details` |

（旧文要求「总是先调 `authenticate`」：不需要——各工具在调用前由 MCP 服务端自行 `ensure_authenticated`；`authenticate` 无参数，只在排查登录状态时手动调。）

## 平台文档页（旧稿里出现过的页名，以 `get_documentations` 目录为准）

`vector-datafields`（VECTOR 处理）、`group-data-fields`（GROUP 处理）、`simulation-settings`（仿真设置）、`data`（数据概念）、`how-use-data-explorer`（Data Explorer）、`19-alpha-examples`（示例）。
