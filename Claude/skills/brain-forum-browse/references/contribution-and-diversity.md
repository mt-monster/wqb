# 独特贡献与多样性（contribution & diversity）

> 合并自 unique-contribution.md / content-diversity.md / personal-perspective.md / follow-on-impulses.md（2026-08-18 精简）。

## 1. 独特贡献（每逛必贡献）

**Hard rule：** 每次「逛论坛」session 必须完成至少一条 forum write，且含**独特个人价值**。无「今天只看看」——linker 兜底也算 write，但仍是你的独特信息，不是空话。

**必须做到：**
- 必贡献：每轮结束前有 MCP write（upvote 可附加但不单独满足「独特内容」）
- 独特内容：正文须含 ≥1 条线程里尚未出现的、可执行或可追溯的个人细节
- 不重复他人：禁止复述楼主/神评的结构、数字、操作步骤而不加新信息
- 不重复自己：禁止照搬 `action_ledger.past_contribution_snippets` 或近 5 轮同 angle_slug

**E1 本机 AI 对话史（合法经验来源）：** 须具体可追溯（工具 + 话题/日期/任务）、只写对话中真实发生过的 sim 设置/报错/指标/踩坑、与论坛帖相关。Citation 示例：`[E1: P4 Cursor chat 2026-06-09 — USA delay=1 PPAC ts_target_tvr_decay sim]`。禁止把对话里的推测当事实。

**禁止的「重复/空话」：** 「感谢分享」「+1」；复述楼主公式无新数据；复制神评改几个词；全网泛化「提高 Sharpe 要控制 turnover」；为凑必贡献发空洞帖（fallback linker 须带 E2 读帖依据 + 索引理由）。

**贡献前自检（写入 contribution plan）：**
```yaml
unique_contribution:
  mandatory: true
  thread_gap: "神评/楼主未覆盖的一点"
  my_unique_detail: "我提供的增量（一句话）"
  e1_sources: ["P5 get_user_alphas …" | "P4 Cursor chat …" | "P1 §…"]
  not_duplicate_of: ["post_id=… comment#… 已说过 X", "ledger snippet …"]
  community_similarity: pass | revised
```

## 2. 内容多样性（Community Similarity + angle 轮换）

对齐官方方向、差异化角度，防止 100 个 agent 发相同 Sharpe tips。**Evidence gate（hard）：** 多样性不免除证据要求，所有草稿主张先过 [evidence-and-review.md](evidence-and-review.md)。

**Angle pool（`action_ledger.content_angles_used[]`）：** ppac-turnover-operator / ppac-submission-debug / ppac-region-usa / vf-diversity-atom / beginner-first-template / theme-official-interpret / theme-counterexample / dataset-field-audit。选**近 5 轮未用**的 angle_slug；耗尽 → 换话题或 L1=linker。

**Community Similarity Check（saturation 后、draft 前，MCP read）：** search_forum_posts(keywords + L2) → read_forum_post top hits → claims[] overlap vs draft_claims → diversity_ok = community_ok AND personal_ok。失败：commenter → sub-argument；author → 新 angle/title 或 linker。

**Banned patterns：** Theme 后泛标题（无 dataset/region/operator）；与 7 天内 top-3 同【】模板；只同意 OP 的评论（须 ≥1 新可执行细节）；空洞表扬；parroting OP/神评无 E1/P5 数据。

**官方 appeal response（L3 announcement/competition）：** official_points ← get_messages；covered_points ← MCP keyword search + read top hits；只写 uncovered；标题须含 L2 + region/dataset/operator；全覆盖 → linker 或 commenter。

**Gap score diversity boost：** `gap_score_final = gap_score * (0.85 + 0.15 * diversity_boost)`；diversity_boost = 1.0（cluster<2）/ 0.5（==2）/ 0.0（>=3）。

## 3. 个人视角（Perspective Card + uniqueness check）

结合 skill memory + host external memory + MCP P5 产出独特论坛声音。

**Phase 0b MCP（P5，每轮默认）：** `get_user_alphas`（提取可验证 alpha/dataset 模式，tag `[brain_mcp]`）；`get_user_profile`（可选）。MCP fail → 省略 P5 事实，绝不编造指标。

**Perspective Card（draft 前必写，入 forum_findings.md）：**
```markdown
## Perspective Card
- memory_sources: [skill_local, claude_md, cursor_rules, brain_mcp, session]
- L2: ...
- angle_slug: ...
- 个人独特点（≥2 条，标注来源）: 1. [skill_local] ... 2. [CLAUDE.md] ...
- 社区已覆盖: ...
- 本人过往已说过（P0）: ...
- 本轮新信息: ...
```

**Personal Uniqueness Check：** self_overlap < 0.4 AND ≥1 self_claim 不在 community_claims AND ≥1 self_claim 不在 past_claims。失败：换 angle_slug、挑未用踩坑、换目标帖。

**禁止：** 编造 VF/rank/提交数；逐字复制过往 snippet；忽视 P1/P2 的泛论坛填充。

## 4. Follow-on Impulses（逛后延伸，非论坛 write）

高质量帖/公告触发的研究或探索想法，**记录并汇报**，不替代必贡献，不自动开新 pipeline。

**定位：** 交付物 = `forum_stroll_notes.md` 本节 + 聊天摘要；用户门控 = **不自动执行**，仅提案；证据 = 标注依据 tier，未验证假设标**待验证**。

**类型：**
- **A 技术帖研究 hook**：可复现细节与 P1/P5/当前 research 交集 → 待验证 sim，不写进 forum 跟评
- **B 官方/Theme/活动信号**：`[E2: get_messages/get_events]` 必须；对照 P5 缺口是否排一轮 makeSomeGem
- **C 开放问题/知识空白**：记入待研究；可选在 forum 只问有 E2 依据的 narrow question
- **D skill handoff**：标建议 skill + 启动条件，**禁止**在 follow-on 名义下直接调用 write/sim API

**记录格式（0–3 条）：**
```yaml
- id: F1
  spark: "E2 MCP read_forum_post post_id=…"  # 必填
  impulse_type: research_hook | theme_alignment | open_question | skill_handoff
  one_liner: "一句话描述（中文）"
  hypothesis: "待验证 | 已有 E1 …"
  suggested_next: "用户若感兴趣，可 …"
  handoff_skill: brain-makeSomeGem | none
  priority: now | later | maybe
  overlaps_contribution: true | false
```

**汇报语气：** 贡献执行后，用「延伸想法（可选，不自动做）」小节列 1–3 条 one_liner + suggested_next，不做 A/B/C 行动菜单。

**对抗性检查：** 必贡献已满足；≤3 条各有 spark；无「平台一定想要 X」无 E2 断言；待验证项未 sneak 进 forum 草稿；未自动启动 sim；handoff_skill 名称正确。
