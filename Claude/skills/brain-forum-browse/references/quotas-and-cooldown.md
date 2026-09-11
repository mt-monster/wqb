# Quotas and Cooldown

> **参考资料已合并（2026-09-11）**：本 skill 早期按主题拆分的参考文件已并入 `SKILL.md` 与本目录现有 9 个 references；文中若出现旧文件名，一律以当前目录的实际文件为准。

Per-run limits (write-enabled default). Config: [config.example.json](../configs/config.example.json).

| Resource | Max/run |
|----------|---------|
| search_forum_posts | 30 |
| search_forum_posts | 5 |
| search_forum_posts | 3 |
| get_glossary_terms | 2 |
| get_glossary_terms | 5 |
| read_forum_post / read_forum_post | 8 combined |
| create_forum_comment | 3 |
| create_forum_post | 1 |
| upvote_forum_comment | 3 |

## Search policy

- Multiple MCP search tools available — agent **chooses by situation** ([mcp-tools-and-search.md](mcp-tools-and-search.md)).
- `search_forum_posts` is expensive; use when fast insufficient, not every query.
- Track counts in session_plan MCP call log.

## Policy

- Prefer **comment over post**
- Max **3 write actions** total in plan (comments + posts + upvotes combined display; upvotes count toward curator minimum suggestion, not always executed)

## Cooldown (soft)

- Do not comment same post_id twice in consecutive runs unless new official info
- Do not repost same angle_slug within 5 runs (see contribution-and-diversity.md)
- Upvote: skip if comment_id already in `upvoted_comment_ids`

## Rate discipline

Batch reads; avoid redundant search with identical query strings in one run.

**Track in session_plan «MCP call log»** — increment after each tool invocation. Stop at quota; do not substitute browser or manual URL fetch.
