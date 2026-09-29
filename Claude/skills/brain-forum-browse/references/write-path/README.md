# 论坛写路径（休眠 · DORMANT）

> **本目录当前不适用。** 激活条件：`wq-brain-http` 出现 `create_forum_comment` / `create_forum_post` / `upvote_forum_comment` 任一工具。
> 现状：一个都没有（工具清单见 [../../SKILL.md](../../SKILL.md) §1，`tests/unit/test_se_docs.py` 对照代码签名）。
> 在此之前：不走 Run Contract / Auto-Send E1 / 对抗审查 / curator，不靠浏览器绕过；用户要文案时只**起草、不发布**——起草同样遵守本目录的证据规则与下面的脱敏清单。

## 文件

| 文件 | 内容 |
|---|---|
| [modes-and-contract.md](modes-and-contract.md) | 模式、Run Contract、Auto-Send E1（A1–A8 可检条件清单） |
| [evidence-and-review.md](evidence-and-review.md) | 证据分级 E1 / E2 / E3 与对抗审查 |
| [contribution-and-diversity.md](contribution-and-diversity.md) | 独特贡献、社区相似度、个人独特性、延伸想法 |
| [recon-and-gap.md](recon-and-gap.md) | 官方扫描、gap 评分、L2 / L3、角色矩阵、索引帖 |
| [workspace-and-memory.md](workspace-and-memory.md) | 磁盘工作区、外部记忆 harvest、profile 引导、与 judge 的边界 |
| [quotas-and-cooldown.md](quotas-and-cooldown.md) | 写操作配额与冷却 |
| [write-style-zh.md](write-style-zh.md) | 写作风格与论坛原生 HTML |
| [mcp-by-phase.md](mcp-by-phase.md) | 各阶段用哪个工具 |

配套：模板 `templates/write-path/`（`session_plan.md` / `forum_stroll_notes.md` / `run_contract.md` / `forum_findings.md`）、脚本 `scripts/init_workspace.py --write-path`、`init_profile.py`、`validate_profile.py`、`harvest_external_memory.py`、`md_to_forum_html.py`。

## 阶段表（按执行顺序）

本目录的文件沿用历史编号（Phase 0–9、1.5、7.5，数字不是执行顺序）；下表给出**执行顺序**与对照。

| 顺序 | 历史编号 | 名称 | 用到的工具 | 何时 |
|---|---|---|---|---|
| 1 | Phase 0 | 加载工作区 | 无（读本地文件） | 总是 |
| 2 | Phase 0a | 外部记忆 harvest | 无（读宿主记忆文件；会读私人内容，见脱敏） | 可选，记忆过期时 |
| 3 | Phase 0b | 个人事实同步 | `get_user_alphas`、可选 `get_user_profile` | 总是 |
| 4 | Phase 1 | Profile | 无 | 缺 `agent_profile.json` 时先引导 |
| 5 | Phase 2 | 官方扫描 | `get_messages`、`get_events`、`search_forum_posts`、`get_glossary_terms` | contribute（explore 轻量） |
| 6 | Phase 3 | 实时登记册 | `search_forum_posts` | contribute |
| 7 | Phase 4 | Gap 扫描 | `search_forum_posts`、`get_glossary_terms` | contribute |
| 8 | Phase 5 | 角色选择 | 无 | contribute |
| 9 | Phase 6 | 深读 | `read_forum_post` | 总是 |
| 10 | Phase 7 | 饱和度检查（发新帖时） | `search_forum_posts`、`read_forum_post` | 发新帖 |
| 11 | Phase 7.5 | 证据 + 对抗审查 | 无写；可读 | 每份草稿（Auto-Send E1 除外） |
| 12 | Phase 8 | 多样性闸 | `search_forum_posts`、`read_forum_post` | 每份草稿 |
| 13 | Phase 1.5 | Run Contract（**停**等「同意执行」） | 无 | 每次有写操作（Auto-Send E1 除外） |
| 14 | Phase 9 | 执行写操作 | `create_forum_*`、`upvote_forum_comment` | 同意之后 |

## 术语（仅本目录；与全库其它同形标签无关）

- **证据 E1 / E2 / E3**：E1 = 个人一手经验（自己的 sim / 提交事实、下面的记忆层）；E2 = 本轮 MCP 读到的平台 / 论坛数据；E3 = 具名外部论文（arXiv ID，或标题 + 作者）。
- **记忆层 P0–P5**：P0 = 动作台账（`outputs/workspace/action_ledger.json`）、P1 = 个人经验文件、P2 = 项目记忆文件、P3 = 用户级记忆、P4 = 会话 / 宿主记忆与 AI 对话史、P5 = BRAIN MCP 事实。与全库其它的 P 编号（S0 的 P5 饱和拍平、probe 模板 P5、审计 P-codes）**无关**。
- **内容层级 L1 / L2 / L3**：L1 = 本轮角色（commenter / author / linker / curator 等）、L2 = 用户专长标签、L3 = 从公告 / 热帖里派生的信号模式。与全库的「L1 层」（技能层级）**无关**。**Scout 不是角色**，是 contribute 流程里的扫描 / gap 工作。

## 已裁决的冲突

- 「每轮必贡献」只在**有写工具**时成立（决策树见 [modes-and-contract.md](modes-and-contract.md) §2）；没有写工具 = 休眠，不存在该义务。
- 「每轮必须 ≥ 1 个写操作」与「每次最多计划 3 个写操作」不冲突：有写工具时，每轮写操作数 ∈ [1, 3]。
- **linker 兜底只有一个条件**：本轮有 E2（MCP 读到的帖）**且**有明确的索引理由；「无话可说也硬发一条链接」不允许。

- **数值阈值都是经验启发式**：本目录里的 `title_sim ≥ 0.65`、`self_overlap < 0.4`、`gap_threshold 0.45` 等没有实测来源，也没有代码在用；启用写路径前应先用真实数据重新校准，不要当作规则背。

## 公开内容脱敏清单（任何要发到论坛的文字，含起草稿）

1. 账号、邮箱、用户 ID、token、口令——一律不出现。
2. 私有路径（盘符、用户名目录、内部仓库路径）。
3. 宿主 AI 对话史（P4）：只可**转述已核实的事实**，不贴对话原文；引用对话内容须先得到用户同意，并去掉他人 / 私有信息。
4. 可完整复现的表达式 + 设置：除非用户明确同意公开，只讲机制与现象，不贴可直接复用的完整配方。
5. 未证实的指标 / 排名 / 提交记录：不写（证据规则见 [evidence-and-review.md](evidence-and-review.md)）。
6. 发布前草稿全文给用户过目（Run Contract 已要求含草稿全文）。
