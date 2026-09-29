# 论坛 MCP 工具与搜索（tools & troubleshooting）

> 只写**现役**工具。历史上的 fast / slow / list / help-center 系列、`create_forum_*`、`upvote_forum_comment`、`delete_forum_*` 都未注册，一律当作不存在。
> 主流程与模式见 [../SKILL.md](../SKILL.md)；故障排查表在 SKILL §4。

## 1. 服务器

- MCP 服务：`wq-brain-http`，工具前缀 `mcp__wq-brain-http__`。运行时**不要探测 / 列举工具**——直接用下表的名字；只有工具「搜不到」时才去排查（SKILL §4）。
- 默认中文论坛话题 ID：`12913416465431`（`configs/config.example.json` 的 `default_topic_id`）。
- 凭据只在服务端：工具没有 `email` / `password` 参数；agent 不读 `.env`、不打印或传递口令。

## 2. 工具签名（与代码逐项对照，测试守护）

| 用途 | 工具 | 参数（缺省） |
|---|---|---|
| 公告 / 主题 / 比赛 | `get_messages` | `limit`（无，建议 30）、`offset`（0） |
| 事件 | `get_events` | 无 |
| 关键词搜帖 | `search_forum_posts` | `search_query`、`max_results`（50） |
| 读帖 + 评论 | `read_forum_post` | `article_id`、`include_comments`（true） |
| 术语表 | `get_glossary_terms` | 无 |
| 用户自己的 alpha 事实 | `get_user_alphas` | `stage`（IS）、`limit`（30，建议 20）、`offset`（0） |
| 用户资料 | `get_user_profile` | `user_id`（self） |

`article_id` 可带标题后缀（如 `32984819083415-新人求模板`），也可只用数字前缀。

## 3. 搜索选型

```
要找关键词？        → search_forum_posts（先精后宽）
首搜为空 / 稀疏？    → 换更宽的关键词再搜一次；不要据一次为空宣称「无帖」
没有关键词、想逛逛？  → 用宽泛词（如 "PPAC"、"Sharpe"、"模板"）搜，或从 get_messages / get_events 取话题
要术语 / 官方文档？   → get_glossary_terms（只作种子词；锚帖不深读）
多次搜索合并？       → 按 post_id 去重
```

- 一个选得好的调用胜过每次把所有工具都跑一遍；同一关键词一次运行里不重复搜。
- 反模式：把浏览器 / WebFetch 当 MCP 的替代；首次搜索为空就停；把 judge 的静态语料当实时论坛。

## 4. 读取预算（惯例，服务端不强制）

`search_forum_posts` ≤ 30、`read_forum_post` ≤ 8、`get_glossary_terms` ≤ 5、`get_messages` ≤ 5、`get_events` ≤ 5（每次运行；与 `configs/config.example.json` 的 `quotas` 一致）。服务端只有一个可选的全局限速（环境变量 `FORUM_RATE_LIMIT_SECONDS`，缺省 0 = 关）；触发时返回 `status: rate_limited` 与 `retry_after`。

## 5. 失败处理

| 情形 | 动作 |
|---|---|
| 首次关键词搜索为空 / 稀 | 换更宽关键词再搜；或改用 `get_messages` / `get_events` 找话题 |
| `read_forum_post` 失败 | 重试一次；仍失败则在笔记里记「读取失败：<id>」并跳过 |
| `rate_limited` | 等 `retry_after` 秒后重试一次 |
| 缺凭据（`Authentication credentials not provided …`） | 停止；请用户在本机配好服务端凭据；**不在对话里传口令** |
| MCP 服务不可用 / 出口被拦 | 报告并停止；**不改用浏览器 / WebFetch / 静态语料** |

## 6. 调用示例

```json
{ "tool": "mcp__wq-brain-http__search_forum_posts",
  "arguments": { "search_query": "PPAC turnover", "max_results": 15 } }

{ "tool": "mcp__wq-brain-http__read_forum_post",
  "arguments": { "article_id": "32984819083415", "include_comments": true } }

{ "tool": "mcp__wq-brain-http__get_glossary_terms", "arguments": {} }
```
