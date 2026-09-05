---
last_verified: 2026-08-22
name: brain-forum-browse
description: "通过 MCP 运行 WorldQuant BRAIN 中文论坛（live forum browse）：默认 **explore stroll** （有目的或涌现式浏览；每轮必须有**独特贡献**，来自个人经验 + AI 对话）。 contribute 模式 = 更严格的 gap 驱动 Recon + 必选 curator。 触发词：逛一逛论坛、逛论坛、看看论坛、去论坛转转、填论坛空白、论坛贡献、browse the forum。"
layer: L0
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__wq-brain-http__*
---







# Brain Forum Browse

## 何时使用（选择本 skill）

**当用户说出类似以下内容时自动启用：**

- **逛一逛论坛** / 逛论坛 / 看看论坛 / 去论坛转转
- 社区共建、填论坛空白、论坛贡献、点赞优质帖
- Agent World 论坛、PPAC 论坛、中文论坛、WorldQuant 论坛
- forum gap、browse the forum（`forum ecosystem` 为旧称，等同本 skill）

**不要用于：** alpha 提交前审查 → 使用 `brain-alpha-judge`（静态语料，无实时论坛 MCP）。

论坛是实时登记册（live registry）。**默认运行 = 带强制贡献的 explore stroll** — 有目的或涌现式浏览，**始终以写操作收尾**（评论、发帖和/或 curator 点赞）。**不允许无贡献的浏览。**

## 运行模式（先读这个）

| 用户意图 | 模式 | 行为 |
|----------|------|------|
| **逛一逛 / 看看 / 转转**（默认） | **explore** | stroll → **必贡献** → **auto-send E1?** 或 7.5+Contract → 6–9 |
| **贡献 / 填空白 / 跟评 / 发帖** | **contribute** | 完整 Recon → gap → 更严 write 计划 + 必 curator → Phase 7.5 → Run Contract → 同意执行 → write |
| **逛为主，可能回一句** | **hybrid**（已弃用别名） | **等同 explore** — 同样必贡献；仅用户话术不同 |

详见 [run-modes.md](references/modes-and-contract.md)。

**禁止所有模式：** 浏览完后「你想先做哪一项？」菜单。

**Run Contract** — 写操作前的标准路径；**唯一例外：** 单条 E1 评论/帖子（仅 1 次写）、零推断 → [auto-send-e1.md](references/modes-and-contract.md)（无需 `同意执行`）。

## 最低贡献标准（explore 每轮必达）

**贡献义务决策树（唯一表述，替代分散规则）：**

```
MCP 环境是否提供论坛写工具？
├─ 是 → 每次「逛一逛论坛」会话必须以 ≥1 个论坛写操作结束（不允许只浏览）。
│        每次写操作必须包含独特个人价值（E1/E2/E3 证据支撑）。
└─ 否（如 wq-brain-http 仅只读工具）→ 写贡献义务自动豁免，本会话降级为
         只读浏览，但必须在会话记录（session_plan.md / forum_stroll_notes.md）
         中注明豁免原因。
```

每次写操作必须包含**独特的个人价值** — 见 [unique-contribution.md](references/contribution-and-diversity.md)。

1. **≥1 个有证据支撑的写操作** — 评论 **或** 新帖，每条论断都必须追溯到 E1/E2/E3
2. **明确的用户批准计划**，含评论 + curator 点赞组合（当点赞是主要动作时，若帖子值得仍优先评论）

**推荐默认：** ≥1 条包含**独特** E1/E2/E3 细节的评论 — 不是空洞称赞或复读。

**若浏览后确实无话可说：** 在 `forum_stroll_notes.md` 中记录原因，然后仍尝试 **linker 式最小价值**（有帮助的链接、索引指路、窄问题的回复）— **避免空会话**。

## 默认：MCP 完成一切（平台 + 论坛）

**本 skill 的默认执行方式 = 全部走 MCP。** 只要涉及 BRAIN 平台或中文论坛，就必须调用 `wq-brain-http` 工具 — **没有**「先凭记忆/网页/静态语料凑合」的备选路径。

> **环境适配（2026-08）**：当前 MCP 服务器为 `wq-brain-http`（服务名 `brain-platform-mcp`，工具前缀 `mcp__wq-brain-http__*`，**HTTP 端点 `http://localhost:8876/mcp`**，2026-08-17 实测可用）。论坛访问用此 8876 端点；备选 stdio 为 `wq-brain-stdio`（`python main.py` + `MCP_TRANSPORT=stdio`）。
> wq-brain-http 只实现**只读**论坛工具（搜索 / 读帖 / 术语表 / 消息 / 活动），**未实现**发帖、跟评、
> 点赞等写工具。执行时按下表映射；写工具不可用时**降级为只读浏览**并在 session_plan 记录，
> 绝不改用浏览器或静态语料冒充。工具映射详见 [mcp-forum-tools.md](references/mcp-tools-and-search.md)。

| 要做的事 | 必须用的 MCP（wq-brain-http） | 禁止 |
|----------|--------------|------|
| 看公告 / Theme / 比赛 | `get_messages`, `get_events` | 编造公告、读 alpha-judge 语料当 live |
| 列帖 / 搜帖 / 读帖 | 见下方 **Search 工具链** + `read_forum_post` | 浏览器 |
| 术语种子 | `get_glossary_terms` | 把 glossary 锚帖当 gap 深读 |
| 用户 alpha 事实 (P5) | `get_user_alphas`（Phase 0b **默认执行**） | 编造 VF/提交记录 |
| 发帖 / 跟评 / 点赞 | **wq-brain-http 未实现**（`create_forum_*`, `upvote_forum_comment` 不存在） | 降级为只读；Contract 未 `同意执行` 前禁止任何 write |

**唯一不走 MCP 的：** skill 本地 workspace（Phase 0）、宿主 memory 文件（Phase 0a）、`agent_profile.json`（Phase 1）。这些是**工作记忆**，不是论坛真相源。

## 执行模型（先读这个）

```
1. Infer run_mode (default explore) — see modes-and-contract.md
2. init_workspace --new-run; load memory; get_user_alphas (0b)
3. explore → stroll → contribution plan → forum_stroll_notes.md
   → auto-send E1? (A1–A8 + MD→HTML + chat HTML preview) → Phase 9
   OR Phase 7.5 → Run Contract → 同意执行 → Phase 6–9
4. contribute → Recon → 7.5 → Contract → 同意执行 → execute
5. follow-on impulses (optional); never post-browse menu
```

MCP 服务器：**wq-brain-http**（`mcp__wq-brain-http__*`，**HTTP 端点 `http://localhost:8876/mcp`**，2026-08-17 实测可用、返回真实论坛数据）。备选 stdio：`wq-brain-stdio`（`python main.py` + `MCP_TRANSPORT=stdio`）。默认中文话题 ID：**`12913416465431`**。

**运行时不要探测或列举 MCP 工具** — 直接使用 [mcp-forum-tools.md](references/mcp-tools-and-search.md) 中的确切工具名。凭据来自 MCP 服务器配置；仅在认证失败时才传 `email`/`password`。

**反面模式：** 不进行 web fetch / Playwright / 手动输入论坛 URL；不编造 post_id/标题/评论；不用 `brain-alpha-judge` 语料冒充实时论坛；不用 `delete_forum_*`；除非用户明确转向 alpha 研究，否则不用模拟工具。

**MCP 不可用时：** 向用户报告错误并**停止** — 不要用浏览器或静态文件临时凑合。

## Search 工具箱（多种方法，按情况选用）

平台提供 **多种 MCP 搜索/浏览方式**，Agent **按场景自行选择**（不必每次 slow）。菜单与选型见 [forum-search-strategy.md](references/mcp-tools-and-search.md).

| 工具（wq-brain-http） | 典型场景 |
|------|----------|
| `search_forum_posts` | 中文论坛内关键词（唯一搜索工具；结果少时用更宽关键词多搜几次模拟 slow） |
| `read_forum_post` | 读帖 + 评论区（`include_comments=true` 深读） |
| `get_glossary_terms` | 术语表 / HC 文档（替代 `list_help_center_articles`） |
| `get_messages` / `get_events` | topic 发现（Phase 2） |

## 可用 MCP 工具（按阶段）

| Phase | 工具（wq-brain-http） | 关键参数 | 说明 |
|-------|------|----------|-------|
| 0b | `get_user_alphas` | `limit`, `stage` | P5 个人事实 |
| 2 | `get_messages` | `limit=30` | 官方扫描（Official Scan） |
| 2 | `get_events` | — | 比赛 / 主题 |
| 2 | `get_glossary_terms` | — | Phase 2 默认 batch；仅作种子 |
| 3–4 | `search_forum_posts` | `search_query`, `max_results` | 关键词搜索（替代 fast/slow/list 系列） |
| 4 | `get_glossary_terms` | — | GLOSSARY_VOID / 零结果时（替代 HC 工具） |
| 6–8 | `read_forum_post` | `article_id`, `include_comments=true` | 深读 + 全部评论（替代 fast/full 两个工具） |
| curator | `read_forum_post` | `article_id`, `include_comments=true` | 用评论区文本判断 upvote 目标（`get_forum_comment_votes` 未实现） |

**写操作（Run Contract 同意执行后）：** — **wq-brain-http 未实现** `create_forum_comment` / `create_forum_post` / `upvote_forum_comment`。当前环境降级为只读浏览；待服务端 `forum_functions.py` 补充写工具后再启用。

**已安装但超出范围**（除非用户要求，否则不要调用）：`delete_forum_comment`、`delete_forum_vote`、模拟/数据集/alpha 相关工具。

完整参数：[mcp-forum-tools.md](references/mcp-tools-and-search.md) · 搜索协议：[forum-search-strategy.md](references/mcp-tools-and-search.md)。

## 首次运行前

**每次浏览（stroll）：**

```bash
python scripts/init_workspace.py --new-run
```

**Explore 首触发（逛论坛）：** 上述即可开 MCP；profile / harvest **可延后** — 见 [profile-bootstrap.md](references/workspace-and-memory.md).

**Contribute 或要固定 L2 时：**

```bash
python scripts/init_profile.py
python scripts/validate_profile.py
python scripts/harvest_external_memory.py --write   # optional if stale
```

**HTML 转换（Phase 9 前）：**

```bash
python scripts/md_to_forum_html.py --input draft.md --output submit.html
```

## 硬性规则

- **每轮必贡献（不可协商）**：每次会话**必须**以 ≥1 个论坛写操作结束 — 不允许只浏览就退出。每次写操作都要加入**独特的个人内容**（你的指标、sim/调试故事、视角）— **不是**复读楼主/热评，**不是**空洞的「感谢分享/+1」。E1 在具体且属实的前提下可包含**宿主 AI 对话历史**（P4）。仅在有 E2 + 你的索引理由时才可用 linker 兜底。见 [unique-contribution.md](references/contribution-and-diversity.md) 及上文「最低贡献标准」。**豁免条件**：见上文「贡献义务决策树」（MCP 无写工具时自动豁免，须记录原因）。
- **仅限有证据支撑的写操作**：每条评论/帖子论断必须追溯到 ≥1 个来源 — **E1** 个人经验（P0–P5 记忆、sim/提交事实）、**E2** MCP 平台/论坛数据、或 **E3** 具名的外部论文（arXiv ID 或标题+作者）。**禁止：** 臆测、无依据的猜测、虚构的 VF/排名/提交记录、「我觉得可能」、含糊的「研究表明」。见 [evidence-and-review.md](references/evidence-and-review.md)。
- **对抗性审查子代理（Adversarial review subagent）**：标准路径 — 每份草稿之后、Contract 之前。仅在 auto-send E1 时**跳过**（由 A1–A8 检查清单替代）。见 [evidence-and-review.md](references/evidence-and-review.md)、[auto-send-e1.md](references/modes-and-contract.md)。
- **MCP 优先**：Phase 2–9 中凡涉及平台/论坛信息的步骤，**一律先调 MCP**；本地文件只存 MCP 结果摘要，不能代替 MCP 读取。
- **先文件后 MCP**：**任何**论坛 MCP 调用前先加载 `outputs/workspace/`。每个阶段更新 `outputs/runs/<run_id>/session_plan.md`。
- **论坛数据仅来自 MCP**：每个帖子标题、评论正文、投票数都必须来自 MCP `read_*` / `search_*` / `list_*` — 绝不凭记忆或静态语料假设。
- **Role Pick / Draft / Act 前重读**：在草稿、Run Contract 和执行前，重读 `session_plan.md` + `forum_findings.md`（contribute）或 `forum_stroll_notes.md`（explore）的前 30 行。
- **论坛写操作只用中文**。不得虚构 VF、排名或提交记录。
- **论坛提交格式 = HTML**：笔记/Contract 中可用 Markdown 起草；MCP 写操作前，**`create_forum_comment.body` / `create_forum_post.details` 必须是论坛原生 HTML**，而不是原始 Markdown。见 [write-style-zh.md](references/write-style-zh.md)。
- **运行模式默认 explore**：「逛论坛」= 带强制贡献的 stroll（有目的或涌现式 emergent）— [run-modes.md](references/modes-and-contract.md)。
- **Run Contract 闸门**：标准路径 — 计划中的写操作需要 Contract + `同意执行`。**例外：** [auto-send-e1.md](references/modes-and-contract.md) — **恰好 1** 次仅含 E1 的事实性写操作、零推断 → 检查清单后直接写。
- **自动执行**：合同同意后跑完 write，不逐项菜单.
- **Curator**：**contribute** — 符合条件时 Contract 中必须含 ≥1 次点赞；**explore** — 值得时推荐 ≥1 次点赞（计划时写入 Contract）。
- **多样性闸门**：社区相似度（Community Similarity）+ 个人独特性（Personal Uniqueness）— 见 [content-diversity.md](references/contribution-and-diversity.md)、[personal-perspective.md](references/contribution-and-diversity.md)。
- **harvest 时外部记忆只读** — 只写回 skill 工作区。见 [external-memory-sources.md](references/workspace-and-memory.md)。
- **Search 工具箱**：论坛搜索有多种 MCP 工具 — Agent 按 [forum-search-strategy.md](references/mcp-tools-and-search.md) **自行选型**；不必每次 slow，也不要只知道 fast。
- **alpha-judge 边界**：rubric/语料只读；judge 绝不调用实时论坛。见 [merge-with-alpha-judge.md](references/workspace-and-memory.md)。
- **后续灵感（追加）**：完成必选论坛贡献后，记录 0–3 条由阅读引发的**可选**研究/探索/技能交接想法（技术帖、公告、主题）。**不自动执行**；不是浏览后菜单；未验证的假设保持**待验证**状态且不进入论坛草稿。见 [follow-on-impulses.md](references/contribution-and-diversity.md)。

## Pipeline（随 run_mode 裁剪）

| run_mode | 流程 |
|----------|------|
| **explore**（默认） | 0→0a→0b→1 → stroll → contribution plan → **auto-send E1?** or 7.5 → Contract? → 6–9 → follow-on |
| **contribute** | 0–5 Recon → Phase 7.5 → 1.5 Contract (STOP) → 6–9 Execute |
| **hybrid**（已弃用，= explore） | **同 explore**（弃用别名） |

| Phase | explore | contribute |
|-------|---------|------------|
| 0–0b | memory + MCP | 同 explore |
| 2–5 | 轻量 scan / purposeful signals（**不要求** formal gap） | 完整 gap + role pick |
| 7.5 | 标准路径必做；**auto-send E1 跳过** | 同 explore |
| 1.5 | 标准路径必做；**auto-send E1 跳过** | 同 explore |
| 6–9 | auto-send 或 **Contract 同意后** execute | 全执行 |

模板：[forum_stroll_notes.md](templates/forum_stroll_notes.md)、[run_contract.md](templates/run_contract.md)。  
详情：[run-modes.md](references/modes-and-contract.md)、[mcp-by-phase.md](references/mcp-by-phase.md)。

**Scout 不是角色** — 它是 contribute 模式中的 scan/gap 工作。每个会话 **L1**；explore 浏览在 Contract 时从浏览发现中挑选 L1。

## 记忆栈（P0–P5）

| P | 来源 |
|---|--------|
| P0 | `outputs/workspace/action_ledger.json` |
| P1 | `outputs/workspace/personal_experience_memory.md` |
| P2–P3 | 项目/用户文件（CLAUDE.md, AGENTS.md, .cursor/rules, …） |
| P4 | 会话 / 宿主记忆 |
| P5 | BRAIN MCP 事实 |

Perspective Card 必须用 ≥2 层标签标注 `memory_sources[]`。详情：[file-workspace.md](references/workspace-and-memory.md)。

## 配额

见 [quotas-and-cooldown.md](references/quotas-and-cooldown.md)。优先评论而非发帖；每次运行最多计划 3 个写操作。

## 写作风格

[write-style-zh.md](references/write-style-zh.md) — 标题需要 L2 + 区域/数据集/算子；评论需要可执行的细节。

**证据 + 审查：** [evidence-and-review.md](references/evidence-and-review.md) — 所有写操作必需。

## 可选 linker 索引

当 `index_protocol_opt_in: true` 时启用：[index-post-protocol.md](references/recon-and-gap.md)。

## 参考资料索引

- **模式与合同：** [modes-and-contract.md](references/modes-and-contract.md)（run-modes + run-contract + auto-send-e1）
- **贡献与多样性：** [contribution-and-diversity.md](references/contribution-and-diversity.md)（unique-contribution + content-diversity + personal-perspective + follow-on-impulses）
- **证据与审查：** [evidence-and-review.md](references/evidence-and-review.md)
- **工具与搜索：** [mcp-tools-and-search.md](references/mcp-tools-and-search.md)（mcp-forum-tools + forum-search-strategy）· 按阶段映射 [mcp-by-phase.md](references/mcp-by-phase.md)
- **侦察与缺口：** [recon-and-gap.md](references/recon-and-gap.md)（official-scan + forum-as-registry + gap-workflow + gap-detection + saturation-check + l2/l3 + role-matrix + index-post-protocol）
- **配额：** [quotas-and-cooldown.md](references/quotas-and-cooldown.md)
- **工作区与记忆：** [workspace-and-memory.md](references/workspace-and-memory.md)（file-workspace + external-memory-sources + profile-bootstrap + merge-with-alpha-judge）
- **写作风格：** [write-style-zh.md](references/write-style-zh.md)
- **HTML 转换：** `scripts/md_to_forum_html.py`
