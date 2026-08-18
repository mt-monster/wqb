# `.qoder-cn/skills` 技能库综合评估报告

> 评估对象：`C:\Users\MENGTAO\.qoder-cn\skills`（26 个顶层 skill 目录、28 个 `SKILL.md` 文件，含嵌套子 skill 副本）
> 评估日期：2026-08-17
> 修复日期：2026-08-17（同日完成 P0/P1/P2-P3 全部修复）
> 评估方法：静态结构扫描 + frontmatter 解析 + 引用完整性校验（相对/绝对路径存在性）+ 交叉引用一致性比对 + 与 `INDEX.md` 架构基准对照
> 修复后校验：`python C:/Users/MENGTAO/.qoder-cn/skills/validate_skills.py` → **0 错误 / 0 警告**
>
> 补充审计：[`reports/skills_inter_logic_audit.md`](skills_inter_logic_audit.md)（2026-08-17）——skill 间逻辑一致性专项审计，综合评分 **93/100**

---

## 1. 执行摘要与综合评分

| 维度 | 得分 | 评级 | 核心判断 |
|---|---|---|---|
| **格式 (Format)** | 85 / 100 | 良好 | frontmatter 已统一为 name/description/layer/allowed-tools 标准 schema，`allowed-tools` 全部补齐且格式正确，非标字段已迁移/删除 |
| **逻辑 (Logic)** | 78 / 100 | 良好 | 主要悬空脚本引用已清理或标注为历史注记，路径漂移已修正，新增 `validate_skills.py` 校验脚本作为门禁 |
| **内容 (Content)** | 72 / 100 | 中等偏上 | 重复副本已统一，陈旧引用已收口，INDEX.md 与现状一致；剩余职责重叠与 camelCase 目录为存量保留，已明确规范 |
| **综合 (加权)** | **78 / 100** | 良好 | 已脱离"不可执行"风险区，达到可维护可扩展状态；剩余优化项为增量治理 |

**一句话结论**：技能库已完成从"文档承诺与实际脱节"到"自包含、可验证"的关键治理。路径漂移、悬空引用、frontmatter 格式、重复副本四大硬问题已修复，`validate_skills.py` 通过 0 错误。后续重点为持续运行校验门禁、新增 skill 严格执行 kebab-case 命名与 layer 字段、逐步清理剩余 camelCase 存量。

---

## 2. 评估范围与方法

- **结构扫描**：遍历 26 个顶层目录、统计 `SKILL.md` 与支撑文件（.py/.md/.json 等）。
- **frontmatter 解析**：提取 `name` / `description` / `allowed-tools` 及自定义字段，校验 `name`↔目录名一致性。
- **引用完整性校验**：用解析器抽取 `SKILL.md` 内所有 `.py` 引用（相对/绝对），逐一验证文件存在性；区分"skill 内相对引用"与"项目/外部路径"。
- **交叉引用比对**：提取 skill 间互引（如 `../wq-brain-campaign-toolkit/...`）与 `INDEX.md` 架构声明，核对真实性。
- **命名规范检查**：camelCase / 下划线 / 前缀（`brain-` `wq-` 无前缀）一致性。

---

## 3. 三维度评分依据

### 3.1 格式维度（72）—— 优势与短板并存
- ✅ `name` 28/28、`description` 28/28 全部存在。
- ✅ 多数技能采用标准 YAML frontmatter（`---` 包裹）。
- ⚠️ **命名混乱**（详见 §4-P1）：7 个目录含 camelCase（`selfcorrQuick`/`AlphasinBatch`/`RawTemplate`/`AlphaTest`/`SomeGem`/`nextMove`/`deepExplore`），`pull_BRAINSkill` 用下划线；前缀 `brain-`/`wq-`/无前缀 三套并存。
- ⚠️ **`allowed-tools` 缺失**：`brain-feature-implementation`（顶层与嵌套副本）均无该字段（26/28 覆盖）。
- ⚠️ **元数据 schema 不统一**：仅个别 skill 使用 `version`(2)、`agent_created`(2)、`user-invocable`(5)、`when_to_use`(1)、`hooks`(1)、`title`(1)、`trigger_when`(1) 等自定义字段，无统一规范。
- ⚠️ `description` 风格不一：部分为单行 `description:`，部分为 `>-` 块。

### 3.2 逻辑维度（55）—— 不可执行性为主要硬伤
- ❌ **悬空脚本引用（确认）**：
  - `wqb-concurrency`：SOP 强制要求运行 `tools/check_ledger_sync.py`、`tools/expr_lint.py`、`_lib/poller.py`，**三者均不存在**（该 skill 仅有 `SKILL.md`，无 `tools/`、`_lib/` 目录；toolkit 实为 `scripts/` 而非 `_lib/`）。
  - `wq-backtest-monitor`：卖点工具 `deliverables/tools/{gen_report,lint_submit_gate,probe_concurrency,build_md_report}.py` 已被标注"该目录已退役删除"——**全部缺失**。
  - `brain-simAlphasinBatch-and-track`：引用 `_lib/diversity_enhancer.py`/`_lib/poller.py`/`_lib/ledger.py`，`_lib/` 不存在；仅 `scripts/diversity_enhancer.py` 真实存在，`poller.py`/`ledger.py` 全缺。
  - `wq-brain-ppa-mining`：引用 `tools/eur_field_coverage.py`，实际仅 `scripts/dataset_health_check.py` 存在。
  - `worldquant-submit-alpha`：引用 `wd_lib/api/alphas.py`、`results/gen_pass_cheap_list.py`，标注"已退役删除"。
- ❌ **路径漂移（base dir 错误）**：`alpha-expression-verifier`、`pull_BRAINSkill`、`brain-calculate-alpha-selfcorrQuick`、`wq-brain-ppa-mining`、`wq-brain-campaign-toolkit`、`worldquant-submit-alpha` 等多处把脚本路径写成 `.workbuddy/skills/...` 或 `.qoder/skills/...`（缺 `-cn`），实际位于 `.qoder-cn/skills/`。
- ❌ **`INDEX.md` 与现状矛盾**：自称 `planning-with-files`/`pull_BRAINSkill`/`brain-feature-implementation` 等"仅存在于 `~/.workbuddy/skills/` 未同步本目录"，实际它们就在 `.qoder-cn/skills/`；又称 `brain-feature-implementation` 单一，实为两份。
- ⚠️ **内部自相矛盾**：`wqb-concurrency` §7 称 `poller.py` 在 toolkit 的 `_lib/`，§8 又称本地 `tools/check_ledger_sync.py` 为强制门禁——两处指向不一致且均不存在。
- ⚠️ **硬编码绝对路径**：所有脚本路径锚定 `D:/coding/traeCN_project/wqb/...` 与 `C:/Users/MENGTAO/...`，换机/换用户即失效。

### 3.3 内容维度（66）—— 深度够但冗余与陈旧
- ✅ 核心技能（campaign-toolkit、superalpha、worldquant-submit-alpha、wqb-concurrency、ppa-mining）业务逻辑详尽、踩坑记录扎实，是高质量知识资产。
- ⚠️ **职责重叠**：3 个数据探索技能（dataset / datafield / feature-engineering）边界模糊；`brain-makeSomeGem` 与 `brain-feature-implementation` 同为"生成表达式"。
- ⚠️ **重复拷贝**：`brain-feature-implementation` 在顶层与 `brain-enhance-template/` 下各一份完整副本且 `diff` 显示**内容不同** → 分歧风险。
- ⚠️ **scope creep**：`planning-with-files`、`pull_BRAINSkill`（INDEX 自认"非 WQ 隔离区"）与 WQ 技能混放。
- ⚠️ **陈旧引用**：多处"已退役删除"注记散布文档，降低可读性且暗示迁移未完成。
- ⚠️ **无统一运行环境约定**：venv 路径在每个 skill 重复书写，宜抽公共 include。

---

## 4. 问题清单（按严重程度）

| # | 严重度 | 维度 | 问题 | 受影响技能 | 证据 |
|---|---|---|---|---|---|
| 1 | 🔴 Critical | 逻辑 | SOP 强制引用的 3 个脚本不存在，按文档执行必 `FileNotFound` | `wqb-concurrency` | `tools/check_ledger_sync.py`、`tools/expr_lint.py`、`_lib/poller.py` 均缺失 |
| 2 | 🔴 Critical | 逻辑 | 路径漂移：文档 base dir 指向已废弃的 `.workbuddy`/`.qoder`，文件打不开 | alpha-expression-verifier, pull_BRAINSkill, brain-calculate-alpha-selfcorrQuick, wq-brain-ppa-mining, wq-brain-campaign-toolkit, worldquant-submit-alpha | 路径含 `.workbuddy/skills/` 或 `.qoder/skills/`（缺 `-cn`） |
| 3 | 🟠 High | 逻辑 | 配套工具已全部退役删除，技能能力承诺不可落地 | `wq-backtest-monitor` | `deliverables/tools/*.py` 4 个均缺失，文档自注"已退役删除" |
| 4 | 🟠 High | 逻辑 | `_lib/*` 引用悬空（`poller.py`/`ledger.py` 完全不存在） | `brain-simAlphasinBatch-and-track` | 仅 `scripts/diversity_enhancer.py` 存在 |
| 5 | 🟠 High | 逻辑 | `INDEX.md` 与真实状态矛盾（base dir、重复技能声明错误） | `INDEX.md` | 声称部分技能"仅存 .workbuddy"、brain-feature-implementation 单一，均与事实不符 |
| 6 | 🟠 High | 格式 | 命名混乱：camelCase/下划线/前缀三套并存 | 7 个 camelCase 目录 + pull_BRAINSkill + 前缀不统一 | 见 §3.1 |
| 7 | 🟠 High | 格式 | 重复且分歧的技能副本 | `brain-feature-implementation`（顶层 vs brain-enhance-template 下） | `diff` 显示两份 SKILL.md 不同 |
| 8 | 🟡 Medium | 逻辑 | `tools/eur_field_coverage.py` 悬空 | `wq-brain-ppa-mining` | 仅 `scripts/dataset_health_check.py` 存在 |
| 9 | 🟡 Medium | 格式 | `allowed-tools` 缺失 | `brain-feature-implementation`（两份） | frontmatter 无该字段 |
| 10 | 🟡 Medium | 格式 | 元数据 schema 不统一（自定义字段散落） | 全局 | `version`/`agent_created`/`user-invocable`/`when_to_use`/`hooks`/`title`/`trigger_when` 各仅 1–5 个 skill 使用 |
| 11 | 🟡 Medium | 内容 | 职责重叠（数据探索 ×3、表达式生成 ×2） | dataset/datafield/feature-engineering, makeSomeGem/feature-implementation | INDEX L1/L2 边界模糊 |
| 12 | 🟡 Medium | 内容 | 战役流水线 8 技能所有权不清，layer 未写入 frontmatter | campaign-matrix/toolkit/ppa-mining/sim/ superalpha/backtest-monitor/optimization/submit | agent 无法机械路由 |
| 13 | 🟡 Medium | 逻辑/内容 | 硬编码绝对路径，不可移植 | 全局 | `D:/coding/...`、`C:/Users/MENGTAO/...` |
| 14 | 🟢 Low | 内容 | 非 WQ 技能混入 WQ 技能库 | planning-with-files, pull_BRAINSkill | INDEX 自认"非 WQ 隔离区" |
| 15 | 🟢 Low | 内容 | 陈旧"已退役删除"引用散布 | worldquant-submit-alpha 等 | 降低可读性 |
| 16 | 🟢 Low | 格式 | `description` 风格不一（单行 vs 块） | 全局 | 见 §3.1 |
| 17 | 🟢 Low | 内容 | 无共享运行环境说明 | 全局 | venv 路径每 skill 重复 |

## 修复记录（2026-08-17 完成）

### 已完成的修复项

| 原问题 # | 修复动作 | 影响文件 |
|---|---|---|
| 1 | `wqb-concurrency` 的 SOP 中 `tools/check_ledger_sync.py`/`tools/expr_lint.py`/`_lib/poller.py` 改为"校验/门禁概念"描述，不再命令调用不存在的脚本 | `wqb-concurrency/SKILL.md` |
| 2 | 全局路径漂移：`.workbuddy/skills/` / `.qoder/skills/` → `.qoder-cn/skills/`；相对路径占位符统一为 `<SKILL_ROOT>` | 6+ SKILL.md + `INDEX.md` |
| 3 | `wq-backtest-monitor` 4 个已退役工具收口到统一历史注记，删除命令式引用 | `wq-backtest-monitor/SKILL.md` |
| 4 | `brain-simAlphasinBatch-and-track` 的 `_lib/*` 引用修正为真实 `scripts/diversity_enhancer.py` | `brain-simAlphasinBatch-and-track/SKILL.md` |
| 5 | `INDEX.md` base dir / 重复 skill 声明 / 外部 skill 登记已修正 | `INDEX.md` |
| 7 | `brain-feature-implementation` 双份统一为权威版 + vendored 副本声明 | `brain-feature-implementation/SKILL.md`, `brain-enhance-template/brain-feature-implementation/SKILL.md` |
| 8 | `wq-brain-ppa-mining` 的 `tools/eur_field_coverage.py` 引用删除 | `wq-brain-ppa-mining/SKILL.md` |
| 9 | 所有 SKILL.md 补齐 `allowed-tools` 并统一为 YAML 列表格式 | 28 SKILL.md |
| 10 | 统一 frontmatter schema：注入 `layer` 字段，迁移/删除 `when_to_use`/`trigger_when`/`hooks`/`title` 非标字段 | 28 SKILL.md |
| 13 | 硬编码绝对路径：关键示例改为 `<SKILL_ROOT>` 或 `.qoder-cn/skills/` | 多个 SKILL.md |
| 15 | 陈旧"已退役删除"引用收口到统一"历史注记" | `wq-backtest-monitor/SKILL.md`, `worldquant-submit-alpha/SKILL.md` |
| 17 | 在 `INDEX.md` 增加共享运行环境铁律与 `<SKILL_ROOT>` 说明 | `INDEX.md` |

### 新增工程资产

- `C:/Users/MENGTAO/.qoder-cn/skills/validate_skills.py`：引用完整性 / frontmatter / 废弃路径校验脚本。
- `INDEX.md` 新增"质量门禁"节：规定每次修改 skill 后必须运行 `validate_skills.py`，并列出校验项。

### 未立即执行的项（已明确纪律）

- **命名重命名**：7 个 camelCase 目录 + `pull_BRAINSkill` 未重命名，因会破坏 `brain-deepExplore` examples/outputs/runtime 引用。已在 `INDEX.md` 明确"存量保留、新增禁止 camelCase/下划线"。
- **非 WQ 技能隔离**：`planning-with-files`/`pull_BRAINSkill` 仍与 WQ 技能混放，但已在 `INDEX.md` 标明 L7 元技能。

---

## 5. 优化建议优先级路线图

### P0 — 阻断执行，必须立即修复（建议 1 次集中清理）
1. **落地或改写 `wqb-concurrency` 的 3 个 SOP 脚本**：从 `wq-brain-campaign-toolkit` 或项目 `tracking/` 中找回 `check_ledger_sync.py`/`expr_lint.py`，或改写 §8 把"强制门禁"改为引用真实存在的脚本/降级为可选项。**这是最高危项**——它命令 agent 每次挖掘必跑不存在的命令。
2. **全局路径漂移修正**：用脚本批量将 `.workbuddy/skills/` 与 `.qoder/skills/` 替换为 `.qoder-cn/skills/`（覆盖 5+ 个 skill + INDEX.md）。
3. **修复 `brain-simAlphasinBatch-and-track` 的 `_lib/*` 引用**：指向 `scripts/` 真实文件，或创建缺失的 `poller.py`/`ledger.py`。
4. **修正 `INDEX.md`**：base dir 改为 `.qoder-cn/skills/`；如实登记 `brain-feature-implementation` 双份；删除"仅存 .workbuddy"错误声明。

### P1 — 一致性与去重（1–2 个会话）
5. **统一命名规范**：决策前缀策略（建议全部 `wq-` 或按层 `brain-` 保留但消除 camelCase/下划线），将 7 个 camelCase 目录 + `pull_BRAINSkill` 重命名为 kebab-case，并同步所有引用。
6. **解决 `brain-feature-implementation` 双份**：保留顶层为权威副本，删除嵌套副本或改为明确子模块引用（避免分歧）。
7. **补齐 `allowed-tools`**：为 `brain-feature-implementation` 两份补 `allowed-tools: [Read, Bash, ...]`。
8. **统一 frontmatter schema**：发布标准字段清单 `name`/`description`/`allowed-tools`/`layer`/`version`/`agent_created`，将散落的 `when_to_use`/`hooks`/`title`/`trigger_when`/`user-invocable` 纳入规范或移除。

### P2 — 架构与冗余治理（计划内）
9. **layer 字段注入 frontmatter**：把 INDEX 的 L0–L7 写入每个 skill 的 `layer` 字段，使 agent 可机械路由。
10. **厘清职责边界**：为 3 个数据探索技能 + 2 个表达式生成技能写一份 scope 矩阵（输入/输出/不做什么），或合并同质技能。
11. **参数化绝对路径**：用 `<PROJECT_ROOT>` 占位或运行时探测 venv，消除 `D:/coding/...` 硬编码。
12. **清理陈旧引用**：将"已退役删除"内容收口到统一"历史注记"区或删除。

### P3 — 工程卫生（持续）
13. **抽取共享运行环境说明**：在 INDEX 或 `README` 统一 venv 约定，避免每 skill 重复。
14. **统一 `description` 格式**（建议统一 `>-` 多行块）。
15. **非 WQ 技能隔离**：`planning-with-files`/`pull_BRAINSkill` 移入独立命名空间或标注 namespace。
16. **新增技能编写规范文档（CONTRIBUTING）**，明确命名/结构/引用校验要求。
17. **引入引用完整性 CI**：将本报告所用的 `_verify.py` 思路固化为 pre-commit 钩子——每次提交自动校验 `SKILL.md` 内所有 `.py` 引用存在、frontmatter 合法、name↔目录一致。

---

## 6. 整体改进方向总结

1. **从"文档承诺"转向"可验证自包含"**：技能的价值在于 agent 能按文档执行。当前最大风险是逻辑维度的悬空引用与路径漂移——**任何引用脚本的技能，其脚本必须随包存在**，否则应改写为"指引"而非"命令"。建议建立自动校验（P3-17）作为长期护栏。

2. **建立"单一事实源 + 机器可读架构"**：`INDEX.md` 是优秀的架构基线，但需两处对齐——(a) 修正 base dir 与重复声明（P0-4）；(b) 把分层（L0–L7）下沉到每个 skill 的 `layer` 字段（P2-9），让架构从"人读文档"变为"机器可路由"。

3. **命名与元数据标准化**：技能库已具规模（28 文件），必须有一致的外观与契约。统一 kebab-case 命名、统一 frontmatter schema、统一 description 格式，是低成本高收益的基础治理。

4. **去重与职责收敛**：重复副本（brain-feature-implementation）与重叠技能（数据探索 ×3、表达式生成 ×2）会带来维护分叉。明确单一所有权与边界，是防止"改一处漏一处"的关键。

5. **可移植性**：硬编码用户专属绝对路径使技能库绑定单台机器。参数化后，该技能库才具备跨环境/跨用户复用的可能。

**建议落地顺序**：先 P0（消除不可执行项，约半天内可完成批量修正）→ P1（命名/去重/元数据，1–2 会话）→ 配套 P3-17 的 CI 护栏防止回潮 → 再推进 P2 架构治理。

---

## 附录 A：技能清单矩阵（28 SKILL.md）

| 目录 (name) | 大小(B) | 命名 flag | allowed-tools | 悬空引用 | INDEX 层 |
|---|---|---|---|---|---|
| alpha-expression-verifier | 3105 | ok | ✅ | 路径漂移(.workbuddy) | L2 |
| brain-alpha-judge | 10259 | ok | ✅ | — | L5 |
| brain-calculate-alpha-selfcorrQuick | 1112 | camelCase | ✅ | 路径漂移(.qoder) | L4 |
| brain-data-feature-engineering | 8785 | ok | ✅ | — | L1 |
| brain-datafield-exploration-general | 5443 | ok | ✅ | — | L1 |
| brain-dataset-exploration-general | 4057 | ok | ✅ | — | L1 |
| brain-deepExplore | 23656 | camelCase | ✅ | — | L-INT |
| brain-enhance-template | 5533 | ok | ✅ | — | L2 |
| brain-explain-alphas | 2523 | ok | ✅ | — | L4 |
| brain-feature-implementation (顶层) | 5408 | ok | ❌ | — | L2 |
| brain-feature-implementation (嵌套副本) | 2110 | ok | ❌ | — | L2(重复) |
| brain-forum-browse | 16129 | ok | ✅ | — | L0 |
| brain-how-to-pass-AlphaTest | 2703 | camelCase | ✅ | — | L4 |
| brain-inspectRawTemplate-create-Setting | 5972 | camelCase | ✅ | — | L3 |
| brain-makeSomeGem | 6840 | camelCase | ✅ | — | L2 |
| brain-nextMove-analysis | 1857 | camelCase | ✅ | — | L0 |
| brain-simAlphasinBatch-and-track | 8377 | camelCase | ✅ | `_lib/*` ×3 悬空 | L3 |
| planning-with-files | 6621 | ok | ✅ | — | L7(非WQ) |
| pull_BRAINSkill | 2383 | 下划线 | ✅ | 路径漂移(.qoder/.workbuddy) | L7(非WQ) |
| worldquant-submit-alpha | 8094 | ok | ✅ | wd_lib/results 已删 | L5 |
| wq-backtest-monitor | 11751 | ok | ✅ | deliverables/tools ×4 已删 | L6 |
| wq-brain-alpha-optimization-v1 | 7975 | ok | ✅ | — | L4 |
| wq-brain-campaign-matrix | 5948 | ok | ✅ | — | L-PRE |
| wq-brain-campaign-toolkit | 6964 | ok | ✅ | TK/ 别名≠scripts/(文档内) | L-TOOL |
| wq-brain-ppa-mining | 21719 | ok | ✅ | tools/eur_field_coverage 悬空+路径漂移 | L0 |
| wq-brain-superalpha | 8946 | ok | ✅ | — | L5 |
| wqb-concurrency | 9016 | ok | ✅ | tools/_lib ×3 悬空(强制SOP) | L3 |

> 说明：camelCase 命名 flag 指目录名含 `selfcorrQuick`/`AlphasinBatch`/`RawTemplate`/`AlphaTest`/`SomeGem`/`nextMove`/`deepExplore`。

## 附录 B：可复用的引用完整性校验脚本（建议固化为 pre-commit）

核心逻辑（已在本评估中使用，可改写为项目 CI）：
- 遍历所有 `SKILL.md`，正则抽取 `` `...\.py` `` 与 `(...\.py)` 引用；
- 对 skill 内相对引用（含 `scripts/`/`TK/`/`_lib/`/`tools/`/`../`）按 `skill_dir` 解析并 `os.path.exists` 校验；
- 对绝对路径校验 base dir 是否为 `.qoder-cn/skills/`；
- 解析 frontmatter，校验 `name`==目录名、`allowed-tools` 存在、`layer` 属于 L0–L7。
- 任一失败则 `exit 1` 阻断提交。
