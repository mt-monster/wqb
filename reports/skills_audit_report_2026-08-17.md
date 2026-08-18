# Skills 体系综合评估报告

> 评估对象：`world-quant-brain-mcp\.venv\Lib\site-packages\cnhkmcp\untracked\skills` 下 20 个 skill
> 评估时间：2026-08-17
> 评估维度：结构格式（Format）、业务逻辑（Logic）、内容完整性（Content）
> 方法：逐文件读取全部 20 个 `SKILL.md` + 目录树扫描 + 相对链接解析校验 + 跨 skill 重复/端口性核查

---

## 1. 总体评分

| 维度 | 得分 | 说明 |
|---|---|---|
| 结构格式（Format） | **62 / 100** | 目录骨架基本统一，但 7/20 的 `name`≠目录名、frontmatter 字段严重不齐、存在非标准子目录与孤儿文件 |
| 业务逻辑（Logic） | **58 / 100** | 核心编排逻辑（deepExplore 契约、enhance 长任务协议、sim 续跑语义）质量高；但硬编码作者机器路径、子 skill 4×/3× 复制、MCP server 名与项目配置不符等会**直接破坏执行** |
| 内容完整性（Content） | **70 / 100** | 多数 skill 的 `SKILL.md`+`reference.md` 充实（alpha-judge 语料、forum-browse 26 篇 references 尤佳）；但 9 个缺 `examples.md`、运行时产物污染目录、语言策略不统一 |
| **综合（加权 0.3/0.4/0.3）** | **≈ 63 / 100** | 逻辑权重最高（可执行 skill 的核心），拉低总分 |

**结论**：体系已具备可用的"骨架"，但处于"从 Claude Code/Cursor 导入后未适配 WorkBuddy、且多轮手工复制累积"的状态。最大风险不在单篇文档质量，而在**跨 skill 一致性缺失**与**复制/端口性腐化**。

---

## 2. 问题清单及严重程度

### P0 — 严重（阻塞执行或导致错误结果）

| # | 问题 | 影响范围 | 证据 |
|---|---|---|---|
| P0-1 | **子 skill 多副本复制，无单一真源** | `brain-feature-implementation` ×4、`brain-data-feature-engineering` ×3 | `untracked/skills/`、`untracked/skills/brain-enhance-template/`、`untracked/skills/brain-makeSomeGem/scripts/trailSomeAlphas/skills/`、`untracked/APP/trailSomeAlphas/skills/` 均含副本。任一处修复无法自动同步，必然漂移 |
| P0-2 | **硬编码作者机器路径** | `brain-makeSomeGem`、`brain-inspectRawTemplate-create-Setting`、`planning-with-files`、`pull_BRAINSkill`、`alpha-expression-verifier` | `makeSomeGem` 示例写死 `D:/BRAINProject/cnhkmcp/...` 与 `C:/Python313/python.exe`；`inspectRawTemplate` 全用 `C:/Python313/python.exe`；`pull_BRAINSkill`/`planning-with-files` 写死 `.claude/skills/`。在本机/WorkBuddy 环境下命令直接失败 |
| P0-3 | **MCP server 名与项目配置不符（集成断裂风险）** | `brain-forum-browse` | skill 全程引用 `user-brain-api` / `mcp_brain-api_*`；而项目 `.mcp.json` 为 `{"mcpServers":{}}`（空），AGENTS.md 所述 `wqb-mcp` 亦未在 `.mcp.json` 落地。该 skill 大概率无法连到真实 MCP |
| P0-4 | **`name` ≠ 目录名，破坏 skill 路由** | 7/20：alpha-expression-verifier、brain-calculate-alpha-selfcorrQuick、brain-deepExplore、brain-inspectRawTemplate-create-Setting、brain-makeSomeGem、brain-simAlphasinBatch-and-track、pull_BRAINSkill | 例如 `alpha-expression-verifier` 的 frontmatter `name: expression_verifier`；`brain-makeSomeGem` 的 `name: brain-make-some-gem` |

### P1 — 高（一致性 / 可维护性）

| # | 问题 | 影响 |
|---|---|---|
| P1-1 | **frontmatter 字段不齐** | `allowed-tools` 仅 9/20 具备；`user-invocable: true` 仅 4/20（makeSomeGem/enhance/sim 等明显用户可调用却未声明）；`version` 仅 planning-with-files；`hooks` 仅 planning-with-files。加载器行为不可预测 |
| P1-2 | **描述语言策略不统一** | 12 个纯英文 description、8 个含中文。同一中文项目上下文下体验割裂 |
| P1-3 | **非标准子目录命名** | `brain-enhance-template` 用 `knowledge/`、`testingTemplate/`（应 `references/`）；`brain-deepExplore` 用 `schemas/`、`templates/`（应 `references/`+`configs/`） |
| P1-4 | **运行时产物污染 skill 源目录** | `brain-alpha-judge/outputs/`（13 json+7 md 历史跑批）、`brain-inspectRawTemplate-create-Setting/processed_templates/`、`brain-makeSomeGem/outputs/`、`brain-enhance-template/outputs/`。应 gitignore 或外置运行时目录 |
| P1-5 | **错误路径指令** | `alpha-expression-verifier` SKILL.md 指引 `.claude/skills/expression_verifier/scripts/...`，实际目录是 `alpha-expression-verifier` → 按文档操作找不到脚本 |
| P1-6 | **错别字与内部引用不一致** | `brain-deepExplore` 第 64 行 `-lafu Write daily objective...`（"lafu" 明显错字）；其 description 用连字符变体、正文用原始目录名，互指不一致 |
| P1-7 | **游离文档置于 skills 根目录** | `Claude_Skill_Creation_Guide.md`、`longTaskSolution.md`、`Ralph_Loop_AchieveGuide.md` 无 `SKILL.md`，不是合法 skill，却混在 skills 目录下 |
| P1-8 | **`.cursor/skills/brain-forum-browse` 镜像副本** | 与 `untracked/skills/brain-forum-browse` 平行存在，双份维护必漂移 |

### P2 — 中（完整性 / 规范）

| # | 问题 | 影响 |
|---|---|---|
| P2-1 | **9 个 skill 缺 `examples.md`** | alpha-expression-verifier、brain-calculate-alpha-selfcorrQuick、brain-explain-alphas、brain-how-to-pass-AlphaTest、brain-improve-alpha-performance、brain-datafield-exploration-general、brain-dataset-exploration-general、brain-nextMove-analysis、pull_BRAINSkill（forum-browse/inspectRawTemplate 亦无 examples） |
| P2-2 | **孤儿文件** | `brain-data-feature-engineering/OUTPUT_TEMPLATE.md`（SKILL.md 未引用）、`brain-enhance-template/README.md` |
| P2-3 | **语法/拼写瑕疵** | `brain-calculate-alpha-selfcorrQuick` description "this can be very fast than query"（应为 faster than querying） |
| P2-4 | **命名风格混杂** | kebab-case（brain-alpha-judge）、camelCase（brain-makeSomeGem 目录）、PascalCase（pull_BRAINSkill 目录）、snake（pull_brainskill 的 name）并存 |
| P2-5 | **知识型 skill 过薄** | brain-datafield/dataset-exploration-general、brain-explain-alphas、brain-nextMove-analysis 仅 2 文件，无脚本无示例，可操作性弱 |

### P3 — 低（改进方向）

| # | 问题 |
|---|---|
| P3-1 | "长任务协议"（detached + 轮询 + artifact-first 判定）在 deepExplore / enhance-template / makeSomeGem / sim-batch 中重复实现，应抽公共参考 |
| P3-2 | 仅 planning-with-files 有 `version` 字段，其余缺版本追踪 |
| P3-3 | `brain-how-to-pass-AlphaTest` 未覆盖 `IS_LADDER_SHARPE` 等 `wq-brain-alpha-optimization-v1` 引用的闸门，知识断层 |

---

## 3. 逐 skill 速查卡

| Skill | 格式 | 逻辑 | 内容 | 主要问题 |
|---|---|---|---|---|
| alpha-expression-verifier | 中 | 低 | 中 | name≠dir、路径指令错、缺 references |
| brain-alpha-judge | 优 | 优 | 优 | outputs 产物污染（P1-4） |
| brain-calculate-alpha-selfcorrQuick | 中 | 中 | 中 | 语法错、缺 examples、EN-only |
| brain-data-feature-engineering | 中 | 低 | 中 | 孤儿文件、副本×3、EN-only |
| brain-datafield-exploration-general | 中 | 中 | 中 | 极简、缺 examples |
| brain-dataset-exploration-general | 中 | 中 | 中 | 极简、缺 examples |
| brain-deepExplore | 中 | 中 | 优 | 错别字、name≠dir、非标子目录 |
| brain-enhance-template | 中 | 低 | 优 | 嵌套副本×1(190文件)、非标目录、README孤儿 |
| brain-explain-alphas | 中 | 中 | 中 | 极简、缺 examples |
| brain-feature-implementation | 中 | 低 | 中 | 副本×4、EN-only |
| brain-forum-browse | 优 | 低 | 优 | MCP 名不符、.cursor 镜像 |
| brain-how-to-pass-AlphaTest | 中 | 中 | 中 | 缺 examples、闸门覆盖不全 |
| brain-improve-alpha-performance | 中 | 中 | 中 | 缺 examples |
| brain-inspectRawTemplate-create-Setting | 中 | 低 | 中 | 硬编码路径、name≠dir、产物 |
| brain-makeSomeGem | 中 | 低 | 优 | 硬编码路径、name≠dir、副本×3 |
| brain-nextMove-analysis | 中 | 中 | 中 | 极简、缺 examples |
| brain-simAlphasinBatch-and-track | 优 | 优 | 优 | name≠dir、outputs 产物 |
| planning-with-files | 优 | 中 | 优 | 路径写死 .claude（迁移残留）、hooks 用 bash |
| pull_BRAINSkill | 中 | 低 | 中 | name≠dir、路径写死 .claude |
| wq-brain-alpha-optimization-v1 | 优 | 优 | 优 | 结构良好，最佳范例之一 |

---

## 4. 优化建议优先级路线图

### 阶段 1（P0，立即，约 1–2 天）
1. **统一 `name` 与目录名**（P0-4）：将 7 个 skill 的 frontmatter `name` 改为与目录完全一致（kebab-case 为准）。
2. **去硬编码路径**（P0-2）：全量替换 `D:/BRAINProject/...`、`C:/Python313/python.exe`、`.claude/skills/` 为相对路径或 `${PYTHON}`/`${SKILL_DIR}` 变量；在 SKILL.md 顶部加"运行时约定"小节说明解释器与根目录取值。
3. **子 skill 单一真源**（P0-1）：保留 `untracked/skills/brain-feature-implementation` 与 `brain-data-feature-engineering` 为权威版，其余 3 处改为软链或 import 引用，删除物理副本。
4. **核实并修正 forum-browse MCP 接线**（P0-3）：对照实际 MCP 配置确认 server 名（`user-brain-api` vs `wqb-mcp`），修正 SKILL.md 与调用示例；空 `.mcp.json` 需补齐。

### 阶段 2（P1，一致性，约 2–3 天）
5. 制定并落地 **SKILL.md frontmatter 规范**：强制 `name`/`description`/`allowed-tools`/`user-invocable`；`version` 建议全量；用脚本（见 §5）校验。
6. 统一 **描述语言策略**：中文项目下建议 description 以中文为主、关键术语保留英文。
7. 规范化子目录：统一为 `scripts/ references/ configs/ data/ outputs(→运行时外置)`；改名 `knowledge/`→`references/`、`testingTemplate/`→`tests/`、`schemas/`+`templates/`→`references/`+`configs/`。
8. 运行时产物外置：将各 skill 的 `outputs/`、`processed_templates/` 移出 skill 或加入 `.gitignore`。
9. 修正 `alpha-expression-verifier` 路径指令、`brain-deepExplore` 错别字与内部引用。
10. 处理游离文档（P1-7）：3 个根目录 md 移入 `docs/` 或并入对应 skill 的 `references/`；删除/生成 `.cursor` 镜像。

### 阶段 3（P2，完整性，约 2 天）
11. 为 9 个缺 `examples.md` 的 skill 补最小可执行示例（含命令与预期输出）。
12. 清理孤儿文件，补充 `brain-how-to-pass-AlphaTest` 的 `IS_LADDER_SHARPE` 等闸门说明。
13. 适度扩充过薄的知识型 skill（加 1–2 个真实案例）。

### 阶段 4（P3，长效）
14. 抽取"长任务协议"公共参考文档，被 4 个 skill 共享引用。
15. 全量加 `version`，建立变更日志。

---

## 5. 整体改进方向总结

**根因**：本 skills 体系是从 Claude Code（`.claude/skills/`）与 Cursor（`.cursor/skills/`）生态**导入但未适配 WorkBuddy** 的产物，叠加多轮"复制目录即部署"的手工操作，导致（a）路径与 server 名指向原作者环境、（b）同一子 skill 在多处分叉、（c）frontmatter/命名规范未统一。

**三条主线改进意见**：

1. **建立单一真源 + 引用而非复制**。所有可复用子 skill（feature-implementation、data-feature-engineering）只保留一份，下游通过 import/软链消费，彻底消除漂移。这是当前最高杠杆的修复。
2. **以"规范 + 自动化校验"替代人工约定**。建议把本次评估用的链接/命名检查脚本（`skills_audit_linkcheck.py` 思路）固化进仓库 CI：每次改动 skill 自动校验 `name==目录`、`allowed-tools` 存在、相对链接有效、无硬编码绝对路径。规范本身写成 `docs/skills-convention.md`（SKILL.md 模板 + frontmatter 必填字段 + 标准目录）。
3. **执行上下文适配 WorkBuddy**。所有路径改为相对/变量、MCP server 名对齐项目实际配置、运行时产物外置。让 skill 在"本机 + WorkBuddy"环境下开箱即用，而非仅原作者机器可用。

完成阶段 1–2 后，综合评分预计可由 63 提升至 **80+**；阶段 3–4 完成后可达 **88+** 的"可维护、可移植、自校验"水准。
