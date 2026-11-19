# forum_recon 触发表（全流水线唯一一张）

> 旧文里同一个工具有 5 个触发点，分散在步 1 / 4 / 5 / 7 / 9，`--out` 目标各不相同，而步 1 又写着「论坛默认不查」——这句话把其余四处架空了。
> 现统一为本表：**不在本表内的场合不查论坛**（选区已有 registry / yield 先验，论坛检索是 token 黑洞）；在表内的场合按本表做。
> 工具：`tools/forum_recon.py`（问题驱动的**只读**检索；`brain-forum-browse` 的 recon 模式经它执行，免贡献义务）；节点等价入口 `workflow_execute(node="forum_recon")`。
> **波级默认取证**：`tools/forum_recon_wave.py` / 节点 `forum_recon_wave`——收批时由代码替 Agent 问一次（见下「波级默认取证」），不必每次记得触发。
> **需要论坛 / 平台可达**——本环境无凭据或出口被拦时工具返回**故障**（退出码 1、`found=null`、记 `forum_recon_error_<qkey>`），此时按各行「取不到时」处理。**故障 ≠ 无解**：不得当作 `found=false`，更不是判死证据。
>
> **★ 查论坛唯一方式（2026-11-18 用户裁定）**：一律按 [`docs/reference/forum_and_doc_tools_guide.md`](../../../../docs/reference/forum_and_doc_tools_guide.md)，
> 只经 `wq-brain-http` 的 5 个 MCP 工具（`search_forum_posts` / `read_forum_post` / `get_glossary_terms` / `get_documentations` / `get_documentation_page`）；
> 论坛访问单一实现 = `tools/lib/forum_mcp.py`（`forum_recon` 传输层已切到它）。**不再** requests 抓 HTML / 直连 Zendesk API（`forum_research.py` 旧抓取链**已删除**），
> **不拿 WebSearch 当论坛通道**（WebSearch/WebFetch 只用于论文线 EVID-PAPER）。机械闸：`tests/unit/08_forum_recon/test_forum_single_way_gate.py`。
> **search 不可靠时（超时 / 0 结果）的正路** = guide §2.3 文档两步绕行：`get_documentations` → `get_documentation_page(page_id)` → 从正文 `<a href=".../posts/<数字>">` 提取 id → `read_forum_post` 直读；
> 或直接 `read_forum_post` 读归档记忆里已知的 article_id。**读帖（read）与文档两步已实测跑通；search 服务端 Playwright 不稳，超时/0 结果一律记故障，不是「论坛无解」。**

## 触发点

| # | 步 | 触发条件（**怎么发现**该查了） | 问题模板 | `--out` | 命中后 | 取不到时 |
|---|---|---|---|---|---|---|
| **0** | **步 4** | **新机制首次派波**（机制证据闸 `check_evidence_gate` 的取证动作，2026-11-15 落地）：某数据集×机制组合**首次**设计回测臂时，必须先出论坛+论文双留痕——gate.py 的 `EVID-FORUM`/`EVID-PAPER` 项在 S2→S3 门按 7 天窗口回查 ledger，缺留痕即阻断（`--require-evidence` 硬约束）或 WARN。**检索词按三维矩阵各至少 1 个**：① 机制措辞词（错位/错配/联动失效/传导/拥挤/出清…）② 算子×字段词（如 `ts_corr returns` / `ts_regression sentiment`）③ 数据集名——三次漏检实证（FF65210 情绪相关性帖/WL58980 横向点塔帖均因只按数据集名检索而漏） | `"<数据集> <机制措辞> 模板"` + `"<算子> <字段> template"` + `"<数据集名> alpha"` 三查 | `ledger`（论文线写 `forum_paper_recon_<qkey>`：论文名+方向+适用边界） | 命中的模板进设计稿素材；**作者线反查**：评论区 ≥200 字方法论长评的作者，以其 ID 再查一轮 | 论坛超时/WebSearch 不可达时降级为本地 `docs/experience` 论文库 grep，**留痕仍必写**（注明降级） |
| 1 | 步 1 | **判死区复开评估**：某区被 `frozen` / 停止规则 A · B2 停下后，有人（用户或 agent）想复开——判据是「有翻案线索吗」，不是「想再试试」 | `"<REGION> <被判死的数据集/族> 有无翻案线索"` | `ledger` | 线索写入 `forum_recon_<qkey>`，供复开评估读；**不改变** `entry_verdict`（那只能按该区 profile 的后门走） | 维持判死 |
| 2 | 步 4 | **机制枯竭 / 同质化**：GEM 产出触每骨架封顶（`WQB_GEM_MAX_PER_SKELETON`，缺省 12），或 win 配方**无腿可换** | `"<数据集/机制> 换腿骨架 / 论坛验证模板"` | `kb` | 合入 `KB/community_tpl_kb.forum_recon_entries[]`；模板**先过 `ghost_operator_advisory`** 替换幽灵算子，再重跑 GEM | 缩窄数据集 / 换集，**不手写表达式** |
| 3 | 步 5 | **闸 6（批级多样性）FAIL 且 `KB/community_tpl_kb` 按 category 检索无货** | `"<category> 骨架 / 换腿参考"` | `kb` | 同 2，回步 4 补骨架 | 拆回单集组合，不停挖 |
| 4 | 步 7 | **卡闸找武器**：Mode B 常规改进 2–3 轮仍卡墙（prod / 2Y / CW / tvr / robust）且未到判死 | `"<墙名+数据集> 破墙配方"`，`--context region=$REGION,dataset=$DS,wall=<WALL>` | `ledger` | **先读本波默认取证的结论**（ledger `forum_recon_wave_<wave>` 标记 → 它指向的 `forum_recon_<qkey>`，见下「波级默认取证」）；无货 / 需换角度才手动 live 查。命中的配方 / 手法入 idea 池供 Mode B Step B3；写 `forum_recon_<qkey>` 留痕。**每波 ≤ 1 次** | 继续 Mode B / 转判死流程 |
| 5 | 步 9 | **判死前取证**（含 D0-P 的 prod 墙判死分支；`seal_dead_end` 的 **fail-closed 硬闸**，见 [`step9-writeback.md`](step9-writeback.md) §9.5） | `"<数据集/信号族> 有无解法"`，`--context region=$REGION,dataset=$DS,family=<族>` | `negative` | `found=false`（退出码 2；**可靠的**负结果已入 `forum_recon_negative_<qkey>`）= 论坛无解的取证，闸放行；`found=true` → 该帖配方转 salvage / Mode B 武器，**不得直接判死** | 工具故障（退出码 1、`found=null`）**不是取证**，闸拒绝；修好后重跑。确需绕过须人工确认：`force_seal=True`（留痕），或本次封存不要求论坛取证 `require_forum_recon=False` |

## 额度与缓存（所有触发点共用）

- **额度以查出有效文章为标准**，不设小硬顶：`--limit` = 目标有效文章数（缺省 3，命中即收束）；搜不到有效文章就扩关键词变体继续搜，直到 `--max-search-rounds`（缺省 8；**防失控安全上限**，不是额度）。
- **有效文章** = 标题不含「公告 / 直播 / 签到 / 问卷 / 获奖 / 名单公示」，正文 ≥ 200 字，且前 2000 字内含可操作标记之一（实测 / 指标 / sharpe / fitness / 表达式 / 字段 / 算子 / 配方 / 换手 / turnover / 稳健 / prod / 相关性 / 中性化 / 破墙 / 回测 / 因子 …，以 `tools/forum_recon.py` 的 `ACTION_MARKERS` 为准）。
- **缓存 7 天**（`tracking/FORUM/forum_recon_cache.json`）：同一问题（`qkey`）7 天内命中缓存不重复 live 查——**只缓存可靠结局**（有货 / 无解）；工具故障不入缓存（故障应当重试，不该被回放一周），旧版遗留的「`found=false` + `error`」条目也不回放。缓存文件不分 region，回放时会把记录补写进**本 region** 的 ledger（判死闸按 `question_key` 回 ledger 核对）。触发点 4 的「每波 ≤ 1 次」是防 token 黑洞的操作约定，在缓存之上。
- 每条有效文章带：post_id / 标题 / 赞数 / 摘录 / 适用边界（context）/ 幽灵算子标注。
- **退出码 = 三种结局**：0 = 有产出（`found=true`，`status=ok`）；2 = **可靠的**无解（`found=false`，`status=no_result`，负结果已入库）；1 = **工具故障**（`found=null`，`status=error`：凭据缺失 / 依赖缺失 / 鉴权失败 / 检索全失败 / 读帖全失败 / 对照检索失败，含未捕获异常）。「无解」只在检索**可靠完成**时成立：鉴权成功、每轮检索都没抛异常、搜到的帖子至少读成功一篇，且末尾用固定对照词（`alpha`）再搜一次仍有结果（会话过期 / 被拦 / 页面改版时搜索页会安静地返回 0 条）。判断「无解」看退出码 2；退出码 1 永远不是取证。`--dry-run` 只输出检索计划（关键词包 + 缓存状态），零网络零写库。凭据：由 **MCP 服务端配置**读取（`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`）；`forum_recon` 作为 MCP 客户端**不收、不读、不传**口令（guide §2.4），不打印、不记录凭据值。
- 产出**必入库**（含负结果与故障）：`found=true` 按 `--out` 落 `KB/community_tpl_kb` 或 `<region>/forum_recon_<qkey>`；可靠的 `found=false` 一律落 `forum_recon_negative_<qkey>`（负结果也是判死证据）；工具故障落 `forum_recon_error_<qkey>`（审计用，**不是取证**）。键契约见 `docs/ledger_keys.json`；三种记录的分类与判死闸的判定是同一份实现（`src/wqb/recon_evidence.py`），写入方、判死闸、`tools/step_funnel.py` 的命中率统计（故障不计入）都从那里取。

## 与 `brain-forum-browse` 的分工

`brain-forum-browse` 是**逛论坛**的 skill（有写工具时按 gap 驱动贡献）；recon 是它的一个模式，**只读、问题驱动、无贡献义务**。流水线里只用 recon，不触发逛论坛流程；论坛帖里的表达式**默认未实证**（先过幽灵算子与闸 5，再进 prod-first），不得当作 win 直接回写。

## 波级默认取证（`forum_recon_wave`）

「卡墙时想起去查」靠 Agent 的记性不可靠，所以**收批时由代码替 Agent 问一次**，之后 Mode B 找武器（触发点 4）与判死取证（触发点 5）都先读这条 ledger 记录：

- **入口**：`pipeline.py … --forum-recon`（评审、prod-first 之后；`batch_track` 节点缺省带上，`forum_recon=False` 可关——离线 / 无论坛凭据的环境）。手动 / 补跑：`python tools/forum_recon_wave.py --region $REGION --wave $W [--dataset $DS] [--force] [--dry-run]`，或节点 `workflow_execute(node="forum_recon_wave", params={"region": …, "wave": …})`（节点 dry-run 只构建命令；要看派生出的问题，用工具的 `--dry-run`，它只读库、零网络零写库）。
- **派生问题**（机械、确定、无 LLM；规则与阈值的取值理由见 `src/wqb/recon_wave.py`）：本波每条已出指标的回测行归 **pass**（RA 闸全过）/ **blocked**（过了强度线、被别的墙挡住：2Y / CW / robust / SUB / tvr / prod）/ **weak**（强度线没过——缺想法，不是缺配方；`ra_failed_checks` 为 NULL 与空同义，强度线另按 `GATES_PLATFORM` 数值兜底）。
  ① 同一堵墙挡住 ≥ 2 条 → **墙问题** `"<REGION> <数据集> <墙> 破墙配方"`（触发点 4）；② 否则本波没有 pass、没有 blocked、weak ≥ 2 → **判死取证问题** `"<REGION> <数据集> 有无解法"`（触发点 5）；③ 其余**不问**（本波有产出，或没有共同瓶颈——不在触发表内，不查论坛）。2 = 能把「共同瓶颈」与「个案」分开的最小值，不是统计推导；并列的墙按 prod > 2Y > CW > robust > SUB > tvr。问题里带 region，所以同数据集同墙的问题**跨波复用 7 天缓存**、跨区不串。
- **每波 ≤ 1 次**：结果落 ledger（`forum_recon_<qkey>` / `forum_recon_negative_<qkey>` / `forum_recon_error_<qkey>`），另留完成标记 `forum_recon_wave_<wave>`（含问题、`question_key`、结局、落点、派生依据）。**可靠结局（有货 / 无解）占用本波额度**，之后再调直接回放标记；**工具故障不占额度**（故障 ≠ 取证，修好后同一波可重跑）；`--force` 忽略标记重跑。
- **只读、不阻断**：论坛不可达 / 缺凭据只打印，不影响收批结论。退出码同 `forum_recon`：0 = 有货，或本波没有需要问的问题；2 = 可靠的无解；1 = 工具故障（节点里对应 `found` = True / None（skipped）/ False / None（error））。
- **怎么读**：卡墙时先读 `forum_recon_wave_<wave>`（`status` = ok / no_result / error）→ 它的 `question_key` 指向 `forum_recon_<qkey>`（有货：文章与配方，走 Mode B 武器、模板先过 `ghost_operator_advisory`）/ `forum_recon_negative_<qkey>`（无解）/ `forum_recon_error_<qkey>`（故障：先修工具）。判死时把 `question_key` 传给 `seal_dead_end`（见步 9 §9.5）。

## 落地记录与已知缺口（2026-09-30）

2026-09-29 并行会话的文案曾把下面四项写成已存在；2026-09-30 合并 main 时核对代码发现都不存在，当日随后逐项落地：

| 能力 | 现状 |
|---|---|
| 故障语义 | `tools/forum_recon.py`：故障 → `forum_recon_error_<qkey>`、`found=null`、退出码 1、不入缓存；live 路径此前**从未跑通过**（`load_creds(None)` 按元组解包，永远 TypeError），一并修复。共享契约 `src/wqb/recon_evidence.py` |
| 波级默认取证 | `tools/forum_recon_wave.py` + 节点 `forum_recon_wave`（五处同步已过 `tools/audit_node_registration.py`）+ `pipeline.py --forum-recon` + `batch_track` 缺省带上（本节上文） |
| 判死闸 | `seal_dead_end(…, forum_recon=, force_seal=, require_forum_recon=True)`：fail-closed，按 `question_key` 回 ledger 核对，只放行可靠的「论坛无解」；拒绝时不沉降、不写库；绕过留痕在 `payload.forum_recon_gate`（步 9 §9.5） |
| 形状配额机检 | `tools/shape_quota_check.py`（步 4 §4.5.1；不入闸链） |

**已知缺口（如实写出，别当作已覆盖）**：
- **live 路径实测状态（2026-11-18 更新）**：传输层已切 MCP（`tools/lib/forum_mcp.py`）。**读帖 `read_forum_post` 与文档两步绕行已端到端实测跑通**（stateless MCP 服务，`mcp_http_caller.McpHttpClient` 已兼容无 session-id）；**`search_forum_posts` 服务端 Playwright 不稳**（超时 / 安静返回 0 条），故 search 驱动的自动 recon 常报故障（退出码 1）——这是工具故障不是「无解」。发现论坛知识请优先用文档两步绕行 + 已知 article_id 直读。页面改版会让「有效文章」判据与对照检索失效，表现为故障而不是「无解」。
- **判死闸只在 `seal_dead_end` 上**：`campaign.py registry add-dead-end`（无 MCP 时的 CLI 备选路径）与 `upsert_registry_empirical(layer="dead_end")`（低层写入口）**不经取证闸**——判死统一走 `seal_dead_end`，走别的口时判死前须人工核对取证（同 §9.5 ①）。
- **闸认的是证据可靠，不核对相关性**：能追溯到 ledger、不是故障、没被更新的「有货」推翻即放行；问的问题是否对得上要判死的那个族，看留痕里的 `question` 由人判断。也**不给证据龄设上限**（留痕有 `searched_at`）。
- `forum_recon_wave` 的派生阈值（同墙 ≥ 2 条）与 `shape_quota_check` 的阈值（≥ 3 个形状族、`trade_when` ≤ 40%）是经验值，不是统计推导；积累几波证据后再评估是否调整。
