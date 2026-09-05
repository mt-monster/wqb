# 侦察与缺口（recon & gap）

> 合并自 official-scan.md / forum-as-registry.md / gap-workflow.md / gap-detection.md / saturation-check.md / l2-search-tokens.md / l3-signal-patterns.md / role-matrix.md / index-post-protocol.md（2026-08-18 精简）。MCP 工具细节见 [mcp-tools-and-search.md](mcp-tools-and-search.md)。

## 1. Official Scan（Phase 2）

contribute/hybrid recon 必做；explore 欢迎 purposeful signals 但不要求 formal gap 打分。

**并行 MCP 批次（一次全发）：** `get_messages(limit=30)` + `get_events()` + `search_forum_posts(max_results=50)` + `get_glossary_terms()`（L2 seed tokens only）。

**Outputs：** `outputs/runs/<run_id>/scan_<ts>.json`（contribute 必，explore 可选）；`forum_findings.md` 记公告/置顶/热帖；新置顶 → `skip_registry.json`。

**Pin detection heuristics：** 高票 + 导航/术语标题模式；已知锚 `4902349883927`；topic listing 官方置顶模式。

## 2. Live Registry（Phase 3）

无远程 JSON registry，**live forum content = MCP reads only**。

**Dedup before post：** `search_forum_posts(title_keywords + L2 tokens)` → 稀疏则宽关键词再搜 → `read_forum_post` on hits；title_sim ≥ 0.65 → comment/linker not new post。

**Per-run `forum_manifest.json`** 捕获 gap_list/session_l1/actions，非全局 registry。本地过滤 `skip_registry`，deprioritize ledger `read_post_ids`/`contributed_post_ids`（除非 STALE_FAQ refresh）。

## 3. Gap Detection & Workflow（Phase 4）

**Gap types：**

| Type | Trigger | Default action |
|------|---------|----------------|
| UNANSWERED_THREAD | comment_count=0 + question shape | comment |
| UNDERSERVED_THREAD | vote_sum≥5, comment_count≤2 | comment |
| TOPIC_VOID | bucket search_scarcity≥0.7 | post (saturation) |
| GLOSSARY_VOID | term zero results | post |
| STALE_FAQ | >180d stale, few comments | comment |

**Scoring formula：**
```
gap_score = 0.35*search_scarcity + 0.30*engagement_gap + 0.15*recency_boost
          + 0.20*quality_void - 0.40*dup_penalty - 0.25*already_read_penalty
```
- `already_read_penalty = 1` if post_id ∈ `read_post_ids`
- Admission: `gap_score >= 0.45`（config `gap_threshold`）
- `search_scarcity = 1 - min(1, result_count / 10)`（per L2 token，from `configs/topic-buckets.yaml`）
- `dup_penalty`：title 与近帖 sim ≥0.65 或本周已贡献同 gap type 时高

**Exclusions：** Hard：`skip_registry.pinned_post_ids`、`contributed_post_ids`（STALE_FAQ 有更新除外）；Soft：已读帖 penalty。

**Workflow：** MCP search + merge Phase 2 hits → 本地过滤 skip_registry → classify gap_type → 每 L2 token MCP search → 本地评分排序 → top 5 入 `forum_findings.md`，top 1 驱动 Role Pick → top gap 连续 2 轮未行动 → `low_roi_post_ids`。

**Output files：** `gap_run_<ts>.json` / `gap_run_<ts>.md`；更新 `session_plan.md` Phase 4 ✓。

**recommended_action → session L1 映射：** UNANSWERED/UNDERSERVED/STALE_FAQ → comment(commenter)；TOPIC_VOID/GLOSSARY_VOID → post(author)；high dup cluster → link(linker)。

## 4. Saturation Check（author 规划 create_forum_post 时必做，MCP only）

```
1. title_keywords ← draft title + L2 tokens
2. MCP search（通常 search_forum_posts；模糊则宽关键词）
3. MCP read_forum_post on hits where title_sim > 0.5
4. ≥2 posts with sim ≥ 0.65 → BLOCK_POST
5. 1 post sim ≥ 0.65 → WARN → commenter on that post
6. cluster ≥ 3 similar titles in 7d → BLOCK_POST, recommend linker
```

| Result | Next step |
|--------|-----------|
| ALLOW | Proceed author draft |
| WARN | Auto: prefer commenter on existing post with narrow angle；document in Run Contract |
| BLOCK_POST | Auto recommend linker；fallback commenter |

Log 入 `forum_findings.md` + `session_plan.md` Phase 7。commenter/linker/curator-only runs 不需要。

## 5. L2 Search Tokens & L3 Signal Patterns

**L2 tokens（map profile `l2[]` to search/gap buckets，source `configs/topic-buckets.yaml`）：** 每 token → 通常 `search_forum_posts`；Gap Scan 稀缺搜索；Community Similarity 时 append L2 tokens；官方 appeal 标题含 L2 label + region/dataset/operator。多 L2 tag 时 union tokens、dedupe searches。

| L2 | Primary tokens |
|----|----------------|
| PPAC | PPAC, Power Pool, turnover, maxTrade, ts_target_tvr |
| VF | Value Factor, VF, ATOM, pyramid |
| correlation | self-corr, correlation |
| dataset | analyst*, fundamental*, model*, sentiment* |

**L3 Signal Patterns（runtime-derived weights，无持久 registry）：**

| Signal in scan text | L3 slug | L1 bias |
|---------------------|---------|---------|
| competition deadline / 截止 | deadline-responder | commenter, linker |
| Theme / pyramid / multiplier announcement | announcement-explainer | author |
| topic post_count spike | hotspot-commenter | commenter + curator upvote focus |
| new feature / API change | announcement-explainer | author |
| glossary / 术语 | glossary-responder | author or commenter |

应用：match against `get_messages` + `get_events` + hot topic titles → emit `l3_signals[]` → Role Pick ±1 tie-break toward biased L1 → 信号消失自动 drop。**Cross-filter with L2：** 只 boost tokens 与 user `l2[]` 重叠的 gap。

## 6. Role Matrix（L1 per session，pick one）

| L1 | When | Write actions |
|----|------|---------------|
| commenter | UNANSWERED, UNDERSERVED, STALE_FAQ | 1–3 中文跟评 |
| author | TOPIC_VOID, GLOSSARY_VOID, saturation ALLOW | 0–1 中文新帖 |
| linker | dup cluster, index opt-in, author BLOCK | 带链接跟评 / 索引 |

**Scout 不是 L1** — scan/gap 内建于 contribute pipeline；explore 不要求 upfront formal gap。

**Role Pick algorithm：**
```
1. Top gap recommended_action → L1 map
2. L3 micro-adjust (announcement → author; hotspot → commenter)
3. Saturation BLOCK and top=post → linker > commenter
4. Last 2 role_history same L1 → rotate tie-break
5. 不问用户选 L1 — fold into Run Contract Phase 1.5；用户可 修改 before 同意执行
```

**Downgrade rules（Deep Read 发现已有实质中文答案）：** author → linker 或 commenter（narrow sub-question）；仍可对质量评论跑 curator。

**Curator heuristics：** Upvote candidates：非本人内容、中文、≥150 字、可执行细节（operator/region/tests）。Not upvote：空洞表扬、OP 复读、英文填充、营销腔。Limits：每帖每轮 max 1 upvote；track `upvoted_comment_ids`。

## 7. Index Post Protocol（可选，linker，`index_protocol_opt_in: true`）

**Title：** `【社区索引】{L2} · {YYYY-MM}`。**Body：** 简短 intro + 3–8 条优质帖链接（各带一行描述）+ 可选 HTML comment marker `<!-- brain-forum-index:l2=PPAC;updated=... -->`。

**Rules：** MCP first（search `【社区索引】{L2}`）；同月同 L2 有索引 → `create_forum_comment` 更新；无 → `create_forum_post`；不重复 saturation-blocked 话题（linker 并入现有索引帖）；中文；body 必须 HTML。仍跑 Community Similarity，须加**新链接**。
