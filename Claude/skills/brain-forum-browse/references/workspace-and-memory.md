# 工作区与记忆（workspace & memory）

> 合并自 file-workspace.md / external-memory-sources.md / profile-bootstrap.md / merge-with-alpha-judge.md（2026-08-18 精简）。

## 1. File Workspace（跨会话磁盘记忆）

`outputs/workspace/` = disk；context = RAM。

**Core files：**

| File | Purpose |
|------|---------|
| `action_ledger.json` | 全历史：read/comment/post/upvote、angles、snippets |
| `skip_registry.json` | 置顶与低 ROI 帖（gap 候选排除） |
| `forum_memory.md` | 人读 run 摘要 |
| `personal_experience_memory.md` | 手编研究习惯（P1） |
| `external_memory_snapshot.json` | Phase 0a host AI 记忆 harvest |

Per-run 快照入 `outputs/runs/<run_id>/`。

**Read before MCP（每轮）：**
1. 读 workspace 文件（缺失则 `scripts/init_workspace.py` 建）。
2. 拷贝模板到 `outputs/runs/<run_id>/`：`session_plan.md`；explore → 另加 `forum_stroll_notes.md`；contribute/hybrid → `forum_findings.md`。
3. **然后**才调 forum/platform MCP — 顺序不可反。
4. **绝不用** 浏览器/WebFetch/alpha-judge 静态语料替代 live forum state。

**Pinned post trap：** 默认 skip `4902349883927`（glossary 锚）。加 `skip_registry.pinned_post_ids` 的启发式：`vote_sum >= 50` 且标题含 `术语|必读|glossary|导航`；topic top-3 高 comment_count 低 gap_score → `pinned_low_roi`。规则：`get_glossary_terms` → seed tokens only，不 Deep Read 锚帖；`search_forum_posts` 结果过 `skip_registry` 再 gap 评分；同 post_id 在 gap_list 连续 2 轮未贡献 → `low_roi_post_ids`。

**Ledger updates：** Deep Read 完成 → `read_post_ids`；comment/post/upvote 成功 → `contributed_*` + `past_contribution_snippets`；新置顶 → `pinned_marked` + `skip_registry`。

**already_read_penalty：** gap 评分时 post_id ∈ `read_post_ids` → -0.25。Hard exclude：`contributed_post_ids`（STALE_FAQ 有更新除外）。

## 2. External Memory Sources（Phase 0a harvest，只读）

结果只写 `outputs/workspace/external_memory_snapshot.json`。

**Priority stack（P0–P5）：**

| P | Source | Location |
|---|--------|----------|
| P0 | Skill action ledger | `outputs/workspace/action_ledger.json` |
| P1 | Skill experience | `outputs/workspace/personal_experience_memory.md` |
| P2 | Project memory files | 见 host 表 |
| P3 | User-level memory | `~/.claude/CLAUDE.md` 等 |
| P4 | Session / host memories；**AI 工具对话史**（Cursor/Claude/Kimi research 对话） |
| P5 | BRAIN MCP facts | `get_user_alphas` 等 |

冲突：forum facts → P0；alpha facts → P5；preferences P1 > P2 > P3。

**Host scan paths（按 `agent_profile.preferred_host` 定顺序）：**
- cursor：`.cursor/rules/*.mdc`、`AGENTS.md`、`.cursorrules`
- claude_code：项目 `CLAUDE.md`/`MEMORY.md`、`~/.claude/CLAUDE.md`
- kimi：`AGENTS.md`、项目 `memory/`
- codex：`AGENTS.md`、`.codex/`、`instructions.md`
- windsurf：`.windsurfrules`、`AGENTS.md`
- copilot：`.github/copilot-instructions.md`
- generic：`todo.md`、README research sections

**AI 工具对话史（P4，独特贡献燃料）：** 当前 session 聊天（tag `P4 session`）；Cursor `.cursor/…/agent-transcripts/*.jsonl`；Claude/Kimi 项目记忆。规则：只引**该对话真实说过/sim 过的**；`evidence_sources` 注明日期/话题；绝不凭对话记忆编造指标。

**Do NOT scan：** `.env`、`user_config.json`、任何含密码/token 的文件。

**Harvest procedure：** 找项目根（向上走 .git 或 CLAUDE.md）→ glob/read 存在的路径 → 提取 BRAIN 相关 bullets（region/dataset/workflow/submission 习惯）→ 写 `external_memory_snapshot.json {harvested_at, mode, sources, merged_bullets}` → 更新 `forum_findings.md` Memory Sources 表 → 零文件则 mode=session-only 从当前聊天提取。

**Write-back policy：** Act 后只更新 **skill workspace**；不自动改 `CLAUDE.md` 或 Cursor rules，除非用户明确要求。

## 3. Profile Bootstrap（`data/agent_profile.json` 缺失时首跑）

**Explore-first（默认逛论坛触发）：**
1. `python scripts/init_workspace.py --new-run` — 必做
2. `get_user_alphas`（Phase 0b）— 必做
3. **Defer L2 interview** — 从 P5/P0–P4/聊天推断 specialty；`agent_profile.json` 可暂缺或最小 `{}`
4. 用户明确 contribute/填空白 或第二轮再跑 `init_profile.py`

**Contribute-first 或用户愿意配置时，问（仅 L2）：** 1–3 个 primary specialties（PPAC/VF/beginner/correlation/SuperAlpha/templates/region/dataset）；可选 `l2_params`（region/dataset id）；可选 `preferred_host`（cursor/claude_code/kimi/codex/windsurf/copilot/generic）。

**Do NOT ask：** L1 role（每轮 Role Pick 定）；explore 是否 curator（explore 仅推荐，contribute 合同必考虑）。

**Run（要 profile 时）：** `init_profile.py` → `validate_profile.py` → `init_workspace.py --new-run`；可选（stale host memory）`harvest_external_memory.py --write`。

**Output：** `data/agent_profile.json`（schema 见 `data/agent_profile.schema.json`）。**role_history：** 每次 Act 后 append `{at, l1, gap_type}`，保留近 20 条。

## 4. 与 brain-alpha-judge 的边界

| Task | Skill |
|------|-------|
| Pre-submit alpha review | `brain-alpha-judge` — 静态 `forum_corpus/`，无 live forum |
| Browse forum, fill gaps, contribute | `brain-forum-browse` — **live MCP only** |
| 把 forum 标准沉淀进 judge | 人工：从 MCP reads 筛选 → 更新 alpha-judge corpus |

**MCP-only rule：** brain-forum-browse 必须用 MCP 做所有 live forum/platform 读写；judge 静态 `forum_corpus/` 仅作风格参考，MCP 可用时绝不替代。

**Allowed cross-use：** brain-forum-browse 可**读** alpha-judge rubric/corpus 提升草稿质量；judge 运行时**不调** forum MCP。

**Evidence vs judge corpus：** judge `forum_corpus/` = 风格/rubric 参考，**不是** live 主张的 E2 证据；E2 必须 MCP `read_*`/`search_*`；E1 必须 `get_user_alphas`/P0–P5。Forum writes 用 [evidence-and-review.md](evidence-and-review.md)。

**Corpus path：** `.qoder-cn/skills/brain-alpha-judge/data/forum_corpus/`。不复制进 brain-forum-browse。发现流：live MCP read → 人工筛选 → 加入 judge corpus + index.json。
