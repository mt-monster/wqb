# MCP 工具与搜索策略（tools & search）

> 合并自 mcp-forum-tools.md / forum-search-strategy.md（2026-08-18 精简）。按阶段工具映射见 [mcp-by-phase.md](mcp-by-phase.md)。

## 1. 服务器与铁律

**默认：所有 BRAIN 平台 + 论坛操作走 MCP。** 不要在运行时探测/列举工具；不要用浏览器、WebFetch 或静态语料当 live 论坛数据。

- MCP server：`wq-brain-http`，工具前缀 `mcp__wq-brain-http__`
- 默认中文论坛：`topic_id = 12913416465431`
- **环境适配（2026-08）：** wq-brain-http 只实现**只读**工具（搜索/读帖/术语表/消息/活动），**未实现**发帖、跟评、点赞。写工具不可用时**降级为只读浏览**并在 session_plan 记录，绝不改用浏览器或静态语料冒充。

**Auth：** `email`/`password` 可选（由 MCP 服务端配置提供）；never read or commit credential files。

## 2. 工具映射表（wq-brain-http）

### 只读（已实现）

| 用途 | 工具 | 关键参数 |
|------|------|----------|
| 公告/Theme/比赛 | `get_messages` | `limit=30` |
| 事件 | `get_events` | — |
| 关键词搜索（唯一搜索工具） | `search_forum_posts` | `search_query`, `max_results` |
| 术语表/HC | `get_glossary_terms` | — |
| 读帖+评论 | `read_forum_post` | `article_id`, `include_comments=true` |
| 个人 alpha 事实（P5） | `get_user_alphas` | `limit=20` |
| 个人资料 | `get_user_profile` | `user_id="self"` |

### 写（wq-brain-http 未实现）

`create_forum_comment` / `create_forum_post` / `upvote_forum_comment` — 需服务端 `forum_functions.py` 补充后才可写；在此之前 skill 降级为只读浏览。

### 已安装但超出本 skill 范围（除非用户明确要求）

`delete_forum_comment`、`delete_forum_vote`、模拟/数据集/alpha 相关工具。

## 3. 搜索策略（按场景自选，非固定 fast→slow pipeline）

**Tool menu：**

| 工具 | 场景 | 速度 |
|------|------|------|
| `search_forum_posts` | 中文论坛内关键词（唯一搜索工具；结果少时用更宽关键词多搜几次模拟 slow） | ~1s |
| `search_forum_posts`（browse） | 全帖浏览/live registry/热帖，无关键词时 | ~1s |
| `get_glossary_terms` | GLOSSARY_VOID、官方文档、L2 seed tokens | ~1s |
| `read_forum_post` | 读帖+全部评论（`include_comments=true`） | ~1s |

**How to choose：**
```
Need keyword in 中文论坛?     → search_forum_posts first
Fast enough / rich results?   → stop; read top hits
Sparse or still unsure?       → 更宽关键词再搜一次
Need browse without keyword?  → search_forum_posts (browse)
Need glossary / HC doc?       → get_glossary_terms
Combining multiple tools?     → merge by post_id; dedupe in findings
```

**Prefer fewer calls：** one well-chosen tool beats running every tool every phase.

**Suggested by phase：** Phase 2 Official Scan（get_messages + get_events + get_glossary_terms）；Phase 3 Live Registry（search_forum_posts browse）；Phase 4 Gap Scan（search_forum_posts per L2 token）；Phase 7 Saturation（search_forum_posts on title）；Phase 8 Diversity（search_forum_posts + read_forum_post）。

**Anti-patterns：** 只会用 fast 不知有 slow/list/HC；fast 已够还总调 slow；WebFetch/浏览器替代 MCP；首次搜索空就宣称"无帖"而不换方法。

**Quotas：** 见 [quotas-and-cooldown.md](quotas-and-cooldown.md)。search_forum_posts 较贵，max 5/run。

## 4. Fallback policy

| Situation | Action |
|-----------|--------|
| 首次关键词搜索空/稀 | 更宽关键词再搜，或改用 get_messages/get_events 找信号 |
| `read_forum_post` fails | retry once；换 article_id 别名 |
| 任何写工具缺失 | log in session_plan；skip write；**never browser** |
| MCP server down / auth fail | **stop run**；请用户修 MCP，不离线凑合 |

## 5. Example calls

```json
{ "tool": "mcp__wq-brain-http__search_forum_posts",
  "arguments": { "search_query": "PPAC turnover", "max_results": 15 } }

{ "tool": "mcp__wq-brain-http__read_forum_post",
  "arguments": { "article_id": "32984819083415", "include_comments": true } }

{ "tool": "mcp__wq-brain-http__get_glossary_terms", "arguments": {} }
```
