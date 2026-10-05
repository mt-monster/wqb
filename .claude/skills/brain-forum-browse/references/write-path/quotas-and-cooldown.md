# 配额与冷却（Quotas and Cooldown）

> **休眠**（写路径）：只在 MCP 有论坛写工具时适用，见 [README.md](README.md)。
> 读取预算是**现役**规则（只读 explore 也用），与 [../../configs/config.example.json](../../configs/config.example.json) 的 `quotas` 一致；写操作配额只在写路径生效。均为惯例，服务端不强制（服务端只有可选的全局限速 `FORUM_RATE_LIMIT_SECONDS`，缺省关）。

## 每次运行的上限

| 资源 | 上限 / 次运行 | 性质 |
|---|---|---|
| `search_forum_posts` | 30 | 读取预算 |
| `read_forum_post` | 8 | 读取预算 |
| `get_glossary_terms` | 5 | 读取预算 |
| `get_messages` | 5 | 读取预算 |
| `get_events` | 5 | 读取预算 |
| `create_forum_comment` | 3 | 写配额 |
| `create_forum_post` | 1 | 写配额 |
| `upvote_forum_comment` | 3 | 写配额 |

（历史文档里同一个工具出现多个不同的上限——那是工具改名合并留下的重复行，以本表为准。）

## 策略

- **评论优先于发帖**。
- 写操作合计（评论 + 发帖 + 点赞）**计划 ≤ 3 个**；点赞计入 curator 最低推荐，但不一定执行。与「每轮 ≥ 1 个写操作」不冲突：有写工具时每轮写操作数 ∈ [1, 3]。
- 搜索次数按需，别每次都调满；同一关键词一次运行里不重复搜；批量读取。

## 冷却（软）

- 同一 `post_id` 不在连续两次运行里评论，除非有新的官方信息；
- 同一 `angle_slug` 5 次运行内不重发（见 [contribution-and-diversity.md](contribution-and-diversity.md)）；
- 点赞：`comment_id` 已在 `upvoted_comment_ids` 里则跳过。

## 计数

在 session_plan 的「MCP call log」里每调一次加 1；到上限就停，**不用浏览器或手输 URL 代替**。
