# MCP by Phase（各阶段用哪个工具）

> **休眠**（写路径）：只在 MCP 有论坛写工具时适用，见 [README.md](README.md)。阶段的**执行顺序**与历史编号对照表在 README；本文只写每个阶段的工具与参数。
> 铁律：平台 + 论坛全部走 MCP（`wq-brain-http`，前缀 `mcp__wq-brain-http__`）；运行时不探测工具；MCP 不可用 → 停止并报告，**不用浏览器 / 静态语料**。工具签名与故障排查见 [../tools-and-troubleshooting.md](../tools-and-troubleshooting.md)。

| 阶段 | 工具（参数） | 说明 |
|---|---|---|
| Phase 0 加载工作区 | 无 | 读 `outputs/workspace/*`；`python scripts/init_workspace.py --write-path --new-run` 建 run 目录（脚本路径相对 skill 目录） |
| Phase 0a 外部记忆 harvest | 无 | `python scripts/harvest_external_memory.py --write`；读宿主记忆文件，写 `external_memory_snapshot.json`（隐私见 [workspace-and-memory.md](workspace-and-memory.md) §2） |
| Phase 0b 个人事实同步 | `get_user_alphas(limit=20)`；可选 `get_user_profile(user_id="self")` | **每次会话都做**；MCP 认证失败才跳过并在 session_plan 记原因，不编造 alpha 事实 |
| Phase 1 Profile | 无 | 读 `data/agent_profile.json`，缺则 `init_profile.py` |
| Phase 2 官方扫描 | 并行：`get_messages(limit=30)`、`get_events()`、`search_forum_posts(max_results=50)`、`get_glossary_terms()` | 术语表只作 L2 种子词，不深读；写 `scan_<ts>.json` |
| Phase 3 实时登记册 | `search_forum_posts(search_query=…, max_results=50)` | 本地再按 `skip_registry`、`read_post_ids` / `contributed_post_ids` 过滤 |
| Phase 4 Gap 扫描 | `search_forum_posts`（每个 L2 token）；空 / 稀疏 → 更宽关键词再搜；GLOSSARY_VOID 时 `get_glossary_terms` | 本地评分见 [recon-and-gap.md](recon-and-gap.md) |
| Phase 5 角色选择 | 无 | 只写 `session_l1` 到 session_plan |
| Phase 6 深读 | `read_forum_post(article_id=…, include_comments=true)` | 每次运行 ≤ 8 次；curator 的点赞目标也从这些读取的评论里挑 |
| Phase 7 饱和度（发新帖时） | `search_forum_posts`（标题关键词）；命中且 title_sim > 0.5 时 `read_forum_post` | 结果 ALLOW / WARN / BLOCK_POST，见 [contribution-and-diversity.md](contribution-and-diversity.md) |
| Phase 7.5 证据 + 对抗审查 | 无写；可读 | 每份草稿；细则见 [evidence-and-review.md](evidence-and-review.md)；**审查子代理要宿主允许派生子代理**，不允许时由主 agent 逐条对照证据清单自审并在合同里写明「未派生子代理」 |
| Phase 8 多样性 | 只读：`search_forum_posts` + `read_forum_post` | 事实性论断因多样性调整而变化 → 对受影响草稿重跑 7.5 |
| Phase 1.5 Run Contract | 无 | 见 [modes-and-contract.md](modes-and-contract.md) §4；模板 [run_contract.md](../../templates/write-path/run_contract.md) |
| Phase 9 执行 | `create_forum_comment(post_id, body=HTML)`；`create_forum_post(topic_id=12913416465431, title, details=HTML)`；`upvote_forum_comment(post_id, comment_id)` | 写前 Markdown → 论坛 HTML（[write-style-zh.md](write-style-zh.md)）；**这三个工具当前均未注册** |

写操作之后：更新本地台账、`forum_memory.md`、`agent_profile.role_history`；最后 0–3 条延伸想法写进笔记或 findings（不进 Run Contract、不自动调用其它 skill）。读取预算与写配额见 [quotas-and-cooldown.md](quotas-and-cooldown.md)。

## 卡住时的选型

```
官方 / 主题 / 比赛文本？        → get_messages、get_events
按关键词找帖？                 → search_forum_posts（稀疏就换更宽的词）
无关键词想浏览？                → 用宽泛词搜 search_forum_posts
术语 / 帮助文档？              → get_glossary_terms
帖子正文 + 评论？              → read_forum_post(article_id)
要评论 / 发帖 / 点赞？          → create_forum_comment / create_forum_post / upvote_forum_comment（Run Contract 同意后；当前未注册）
认证失败？                     → 停止，请用户修服务端配置；不在对话里传口令、不用浏览器
MCP 服务不可用？               → 停止并报告（排查表见 ../../SKILL.md §4）
想拿 alpha-judge 语料当实时论坛？ → 禁止；必须 MCP read / search
```

### brain-alpha-judge 边界

- judge 的 rubric（只读）只影响**质量线**，见 [workspace-and-memory.md](workspace-and-memory.md) §4；
- judge 的静态语料**不是** E2 证据，实时论断必须来自 MCP 读取；
- 提交前审查 → `tools/submit_verdict.py`（`brain-alpha-judge` 仅参考层）；论坛写 → 本 skill + 证据分级。
