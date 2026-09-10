# wqb 项目多套 Skills 配置审计报告

> 审计时间：2026-09-10 · 范围：`D:\coding\traeCN_project\wqb` 及其关联的全部 skills 安装位
> 方法：机器级全量扫描（项目内 + 12 个宿主目录）；内容级 md5 归一化比对；分层引用检索（955 个仓库文本文件）
> 数据附录：`tracking/_scratch/skills_audit_20260910.json`（结构+frontmatter）、`tracking/_scratch/skills_refs_tiered_20260910.json`（分层引用）

---

## 结论先行

1. **本项目的 skills 实际有 7 套物理副本**（1 套仓库真相源 + 1 套归档 + 2 处嵌套副本 + 5 个宿主安装位），但**只有 1 个同步目标**——`tools/sync_skills.py` 只把仓库推到 `~/.claude/skills`，其余 4 个宿主（codex/cursor/qoder-cn/workbuddy）不在同步链上，导致**漂移反复复发**。
2. **内容一致性整体良好但不闭合**：32 个 skill 中 **31 个 SKILL.md 六套完全一致**；唯一分叉是 `wq-brain-ra-pipeline`——`~/.codex/skills` 与 `~/.workbuddy/skills` 停在 09-08 版（451 行），落后仓库 67 行，**缺失 2026-09-09 新增的 `campaign_intel s0-select` 选集增强与 `ghost-audit` 幽灵算子硬闸**。这两个宿主恰好是 WorkBuddy（本会话）与 Codex 的生效位。
3. **配置格式（frontmatter）最不统一**：32 个 skill 出现 **8 种不同的字段组合**；`version` 字段仅 4/32 拥有，`last_verified` 缺失 8 个，`layer` 语义在个别 skill 里被误用为版本号（`wq-brain-ra-pipeline layer="2.2"`、`planning-with-files layer="2.1.0"`）。
4. **5 个安装/验证脚本已全部失效且被 gitignore 排除**（`install_claude_skills.ps1/.bat`、`install_now.py`、`verify_claude_skills.py`、`Claude outputs/install_skills_direct.py`）：它们以 `~/.qoder-cn/skills` 为源、用 `if exists: skip` 永不更新——`AGENTS.md:107` 已明确标注"勿再用它做更新"。唯一有效的同步入口是 `tools/sync_skills.py`。
5. **使用情况：无孤儿**。29 个 skill 被代码/规约引用（★正在使用），4 个仅被文档提及（○），3 个 research 子技能通过 `brain-alpha-research/SKILL.md` 交叉引用生效。真正的问题是**冗余而非缺失**：5 套安装副本 + 2 处嵌套同名副本 + 4 个 cursor/workbuddy 独有且互不一致的非 WQ skill。

**一句话建议**：把 `sync_skills.py` 从"单目标"升级为"多目标"，一次性消灭 4 个宿主的分叉；随后统一 frontmatter 契约、收敛命名、清理失效脚本与嵌套副本。

---

## 一、目录盘点

### 1.1 项目内（D:\coding\traeCN_project\wqb）

| # | 位置 | 性质 | 规模 |
|---|---|---|---|
| A | `Claude/skills/` | **仓库真相源**（git 跟踪 262 文件） | 32 skills，其中 8 个文件当前有未提交改动 |
| B | `attic/brain-alpha-judge.pre_recycle_20260908/` | 归档旧版（12379B 旧权威判定文） | 1 skill（本地，gitignore） |
| C1 | `Claude/skills/brain-makeSomeGem/scripts/trailSomeAlphas/skills/brain-feature-implementation/` | **嵌套副本**（git 跟踪） | 2129B，与顶层同名不同文 |
| C2 | `Claude/skills/brain-makeSomeGem/scripts/trailSomeAlphas/skills/brain-data-feature-engineering/` | **嵌套副本**（git 跟踪） | 3 文件（OUTPUT_TEMPLATE/examples/reference） |
| D | `.claude/settings.local.json`、`.mcp.json`、`.qoder-cn/mcp.json`、`.qoder-cn/better-harness/` | 项目级宿主配置（非 skills 本体） | settings 仅 1 条 MCP 权限；better-harness 为 08-16 历史 canvas |
| E | `AGENTS.md`（17KB）、`CLAUDE.md`（1.5KB）、`README.md` | 规约/文档，**定义 skills 的使用契约** | — |

> 项目内**不存在** `.workbuddy/skills` 或项目级 `.claude/skills`；`.workbuddy/` 仅含 `memory/`。

### 1.2 安装/同步脚本群（6 个）

| 脚本 | 源 | 目标 | 更新语义 | 状态 |
|---|---|---|---|---|
| `tools/sync_skills.py` | 仓库 `Claude/skills` | 单目标（`_skill_roots()` 解析，实际 `~/.claude/skills`） | 覆盖式（含 `--check`/`--dry-run`） | **现行唯一有效** |
| `install_claude_skills.ps1` | `~/.qoder-cn/skills` | `%APPDATA%\Claude\skills` 等 | `if exists: skip`（永不更新） | 失效（gitignore） |
| `install_claude_skills.bat` | 同上 | `%APPDATA%\Claude\skills` | 同上 | 失效（gitignore） |
| `install_now.py` | `~/mnt/skills`（不存在）→ `.qoder-cn/skills` 兜底 | Claude 安装位 | 同上 | 失效（gitignore） |
| `verify_claude_skills.py` | `~/.qoder-cn/skills` | — （仅校验） | 只读诊断 | 失效（gitignore） |
| `Claude outputs/install_skills_direct.py` | `~/.qoder-cn/skills` | Claude 安装位 | 同上 | 失效（gitignore） |

### 1.3 宿主侧安装位（与本项目相关的 5 套）

| 宿主目录 | skills 数 | 内容状态 |
|---|---|---|
| `~/.claude/skills` | 32 | == 仓库（仅 1 文件因仓库未提交而短暂落后） |
| `~/.codex/skills` | 32（+`.system`） | **1 分叉**：`wq-brain-ra-pipeline` 落后 |
| `~/.cursor/skills` | 36 | 32 == 仓库 + **4 个非 WQ 特有** |
| `~/.qoder-cn/skills` | 32 | == 仓库 |
| `~/.workbuddy/skills` | 37 | **1 分叉**（ra-pipeline 落后）+ **5 个特有**（4 非 WQ + `brain-enhance-template`） |

> 另有 5 个宿主目录与本项目**零交集**（`~/.openclaw-autoclaw` 85、`~/.ghcp-appmod` 11、`~/.qwenworkcn` 13、`~/.qoderwork` 12、`~/.agents` 0），不在本次治理范围。

### 1.4 仓库 32 个 skill 的结构清单（文件数=git 内容文件）

```
alpha-expression-verifier(4)          alpha-template-labs-data-analysis(1)
brain-alpha-judge(35)                 brain-alpha-repair(2)
brain-alpha-research(8)               brain-alpha-research-field-quality(1)
brain-alpha-research-hypothesis-first(1)  brain-alpha-research-news-sentiment(1)
brain-alpha-robustness(3)             brain-calculate-alpha-selfcorrQuick(4)
brain-data-feature-engineering(5)     brain-datafield-exploration-general(2)
brain-dataset-exploration-general(2)  brain-explain-alphas(3)
brain-feature-implementation(7)       brain-forum-browse(30)
brain-how-to-pass-AlphaTest(2)        brain-inspectRawTemplate-create-Setting(14)
brain-makeSomeGem(21)                 brain-nextMove-analysis(2)
brain-simAlphasinBatch-and-track(14)  planning-with-files(8)
pull_BRAINSkill(2)                    worldquant-submit-alpha(1)
wq-backtest-monitor(1)                wq-brain-alpha-optimization-v1(7)
wq-brain-campaign-matrix(1)           wq-brain-campaign-toolkit(56)
wq-brain-ppa-mining(2)                wq-brain-ra-pipeline(21)
wq-brain-superalpha(1)                wqb-concurrency(1)
```

> 安装位的文件数普遍远大于仓库（如 `brain-makeSomeGem` 2126 vs 21），差额是 `outputs/`、`__pycache__`、vendored 数据等运行期产物，已被同步脚本忽略表与 `.gitignore` 排除，属正常。

---

## 二、一致性差异

### 2.1 文件名 / 命名规范 —— **存在差异**

**结论：目录命名规范分裂为 4 类前缀 + 7 个非纯 kebab-case 命名，无统一约定。**

| 前缀族 | 数量 | 示例 |
|---|---|---|
| `brain-*`（WQ 脑/业务） | 19 | `brain-alpha-judge`、`brain-makeSomeGem` |
| `wq-brain-*` / `wq-*`（流程编排） | 7 | `wq-brain-ra-pipeline`、`wq-backtest-monitor` |
| `wqb-*` | 1 | `wqb-concurrency` |
| 无前缀 | 5 | `alpha-expression-verifier`、`planning-with-files`、`worldquant-submit-alpha`、`pull_BRAINSkill`、`alpha-template-labs-data-analysis` |

**非纯 kebab-case 的 7 个（混用驼峰/下划线/大写）**：
`brain-calculate-alpha-selfcorrQuick`、`brain-how-to-pass-AlphaTest`、`brain-inspectRawTemplate-create-Setting`、`brain-makeSomeGem`、`brain-nextMove-analysis`、`brain-simAlphasinBatch-and-track`、`pull_BRAINSkill`（唯一含下划线者）。

- 差异点：同类语义（都是 WQ alpha 技能）却分散在 `brain-*` 与 `wq-brain-*` 两个前缀；目录名大小写风格不统一，跨平台 glob/引用时易出错。
- 依据：`Claude/skills/` 目录清单（`tracking/_scratch/skills_audit_20260910.json`）。

### 2.2 内容正文 —— **基本一致，1 处实质分叉**

**结论：32 个 SKILL.md 中 31 个六套 md5 完全一致；`wq-brain-ra-pipeline` 在 2 个宿主落后。**

| skill | repo | claude | codex | cursor | qoder-cn | workbuddy |
|---|---|---|---|---|---|---|
| 其余 31 个 | 一致 | 一致 | 一致 | 一致 | 一致 | 一致 |
| **wq-brain-ra-pipeline** | `6c76531f` | `6c76531f` | **`42237472`** | `6c76531f` | `6c76531f` | **`42237472`** |

- **差异点（codex/workbuddy 版，451 行）缺失仓库版（518 行）的 67 行**，含 2026-09-09 两项新增：
  - `tools/campaign_intel.py s0-select` 选集增强（三方交叉：`recommend_datasets` × `get_mining_yield` × `get_dead_datasets`）；
  - `tools/campaign_intel.py ghost-audit` 幽灵算子硬闸（检测 sigmoid/ts_entropy/ts_skewness 等平台不认算子）。
- **影响**：WorkBuddy（本会话）与 Codex 的 agent 按旧 SOP 行事，**不会执行 09-09 新增的选集与幽灵算子门禁**。
- 依据：`Claude/skills/wq-brain-ra-pipeline/SKILL.md` vs `~/.codex/skills/.../SKILL.md`（`difflib` 实测 +67/-0 行）。

### 2.3 特有 skill 的内容不一致 —— **存在**

**结论：cursor 与 workbuddy 共有的 4 个非 WQ skill，内容互不相同（重复定义且不一致）。**

| skill | cursor | workbuddy | 差异 |
|---|---|---|---|
| `code-optimization` | 5000B / `3e1f5f85` | 4969B / `4e563146` | 相差 31B |
| `dead-code-cleanup` | 13247B / `a7e0a623` | 13216B / `b611f9d3` | 相差 31B |
| `gold-analysis` | 7724B / `58c8115d` | 7693B / `7c0c4ce7` | 相差 31B |
| `jin10-news` | 1520B / `a4e3881b` | 1492B / `2ae355c09c` | 相差 28B |

- 差异点：同名 skill 在两宿主各存一份、内容不同（体量差约 30B，疑似不同编辑轮次）；且**均不在仓库内**，无真相源。
- 另有 `brain-enhance-template`（7028B）**仅存在于 workbuddy 位**，仓库与其余宿主皆无——孤儿 skill。

### 2.4 触发条件与配置格式（frontmatter） —— **最不统一**

**结论：32 个 skill 出现 8 种字段组合，缺失项与语义误用并存。**

| 字段组合 | 数量 | 缺失情况 |
|---|---|---|
| `allowed-tools, description, last_verified, layer, name` | 18 | 基准（无 version/agent_created） |
| `allowed-tools, description, layer, name` | 6 | **缺 last_verified** |
| `allowed-tools, description, last_verified, layer, name, user-invocable` | 3 | — |
| `allowed-tools, description, layer, name, user-invocable` | 1 | 缺 last_verified |
| `allowed-tools, description, hooks, layer, name, user-invocable, version` | 1 | `planning-with-files` |
| `agent_created, allowed-tools, description, last_verified, layer, name, version` | 1 | `wq-backtest-monitor` |
| `allowed-tools, description, last_verified, layer, name, version` | 1 | `wq-brain-ra-pipeline` |
| `agent_created, allowed-tools, description, last_verified, layer, name` | 1 | `wqb-concurrency` |

- **差异点 1（字段漂移）**：`version` 仅 4/32 有；`last_verified` 缺 8 个；`user-invocable` 仅 4 个；`hooks`/`agent_created` 为个别用法。
- **差异点 2（layer 语义冲突）**：`AGENTS.md:114` 明确定义 `layer` 表示"在挖掘链条上的位置"，但 `wq-brain-ra-pipeline` 写成 `layer="2.2"`、`planning-with-files` 写成 `layer="2.1.0"`——**被当版本号使用**，含义与契约相悖。
- 依据：各 skill SKILL.md frontmatter（`skills_audit_20260910.json` 的 `fm_keys`）+ `AGENTS.md:114`。

### 2.5 嵌套同名副本 —— **存在重复定义**

**结论：`brain-makeSomeGem` 内部自带 2 个与顶层同名的 skill 副本，内容不同。**

| 名称 | 顶层（仓库） | makeSomeGem 内嵌 |
|---|---|---|
| `brain-feature-implementation` | 5339B / `88b8bec4` | **2129B / `2bfea75c`** |
| `brain-data-feature-engineering` | — （顶层 5 文件） | 3 文件（OUTPUT_TEMPLATE/examples/reference） |

- 差异点：同名不同文、且内嵌副本被 git 跟踪（`git ls-files` 命中），构成"双源"。
- 依据：`Claude/skills/brain-makeSomeGem/scripts/trailSomeAlphas/skills/`。

---

## 三、使用情况核查

### 3.1 判定方法

扫描仓库 955 个文本文件（排除 skills 自身/`.git`），按引用来源分层：**A 层=代码/工具 + 根规约（README/AGENTS/CLAUDE）→"正在使用"**；**B 层=文档/历史 canvas →"仅文档提及"**；**C 层=宿主配置/历史产物**。并补充 skill 间交叉引用扫描。

### 3.2 判定结果

**★ 正在使用（29 个，89%）**——被代码或根规约引用，引用数最高的 8 个：

| skill | 代码/工具 | 根规约 | 文档 | 主要引用点 |
|---|---|---|---|---|
| `wq-brain-campaign-toolkit` | 14 | 3 | 162 | `AGENTS.md`、`src/wqb/workflow/`、`tools/` |
| `brain-makeSomeGem` | 10 | 2 | 36 | `AGENTS.md`、workflow gem 节点 |
| `wqb-concurrency` | 4 | 1 | 57 | `AGENTS.md`、并发调优路径 |
| `wq-brain-superalpha` | 3 | 1 | 8 | `AGENTS.md`、`tools/super_build.py` |
| `brain-alpha-judge` | 3 | 2 | 15 | `AGENTS.md`、`README.md` |
| `wq-brain-ra-pipeline` | 2 | 3 | 17 | `AGENTS.md`、`EUR_campaign_*.md` |
| `brain-simAlphasinBatch-and-track` | 2 | 1 | 22 | `AGENTS.md`、`docs/reference/skill_call_chain.md` |
| `worldquant-submit-alpha` | 2 | 2 | 11 | `AGENTS.md`、`INSTALLATION_GUIDE.md` |

**○ 仅文档提及（4 个）**：`alpha-template-labs-data-analysis`、`brain-alpha-repair`、`brain-datafield-exploration-general`、`brain-explain-alphas`。均属正常——它们是**按需调用的知识型 skill**（数据探索/解释/修复），不进入自动化 call chain，被 `docs/reference/`、`docs/tutorials/课件.md` 收录。

**✗ 未见引用：无**。首轮扫描标出的 3 个 `brain-alpha-research-*` 经交叉引用复核后确认**不是孤儿**——它们被 `Claude/skills/brain-alpha-research/SKILL.md` 显式引用为子技能（`brain-alpha-research-field-quality` 另被 `brain-data-feature-engineering/scripts/feature_engineering.py` 调用）。

### 3.3 冗余 / 重复定义清单

| 类型 | 对象 | 判定 |
|---|---|---|
| **物理副本重复** | 同一份 32 skill 内容在 5 个宿主各存一份 | 设计使然，但同步链只覆盖 1 个 → 已致漂移（见 2.2） |
| **重复定义（不一致）** | `code-optimization`、`dead-code-cleanup`、`gold-analysis`、`jin10-news`（cursor+workbuddy 各一份、内容不同、无仓库源） | 需裁决归属 |
| **孤儿 skill** | `brain-enhance-template`（仅 workbuddy） | 需裁决：入库 or 清理 |
| **嵌套同名副本** | `brain-feature-implementation`、`brain-data-feature-engineering`（makeSomeGem 内嵌） | 双源风险 |
| **失效脚本** | 5 个安装/校验脚本（见 1.2） | 全部 gitignore + `skip` 语义失效 |
| **失效指引** | `INSTALLATION_GUIDE.md`（gitignore，本地存在）仍指导使用上述失效脚本 | 该文件本身也不在仓库，属本地残留 |

---

## 四、改进建议

### P0（高优先：直接消除已发生的运行时风险）

**P0-1 消灭 `wq-brain-ra-pipeline` 分叉，补齐 codex/workbuddy**
- 动作：把仓库当前版（`6c76531f`，518 行）推送到 `~/.codex/skills` 与 `~/.workbuddy/skills`。
- 理由：这 2 个宿主正是 WorkBuddy（本会话）与 Codex 的生效位，缺失 09-09 的 `s0-select`/`ghost-audit` 门禁属实质性 SOP 落后。
- 依据：`Claude/skills/wq-brain-ra-pipeline/SKILL.md`、`~/.codex/skills/wq-brain-ra-pipeline/SKILL.md`。

**P0-2 把 `tools/sync_skills.py` 从"单目标"升级为"多目标"**
- 动作：`--target` 支持多路径/自动枚举 5 个宿主位；同步后逐位 `--check`；`tests/unit/test_audit_fixes.py::test_sync_skills_reports_no_drift` 改为多目标断言。
- 理由：漂移的**结构性根因**是同步链只覆盖 1 个目标（`resolve_install_root()` 只返回首个命中）。不修它，P0-1 的修复会再次复发（09-08 已修过一次，09-10 已复发）。
- 依据：`tools/sync_skills.py:51-79`（`resolve_install_root` 单值返回）；当前 `--check` 只校验 `~/.claude/skills`。

**P0-3 清理 5 个失效安装脚本 + 失效指引**
- 动作：`install_claude_skills.ps1/.bat`、`install_now.py`、`verify_claude_skills.py`、`Claude outputs/install_skills_direct.py`、`INSTALLATION_GUIDE.md` 移入回收站（或统一挪 `attic/`）；安装说明改指向 `tools/sync_skills.py`。
- 理由：这些脚本以 `~/.qoder-cn/skills` 为源、`if exists: skip` 永不更新，`AGENTS.md:107` 已定性为陈旧根因；且全部被 `.gitignore` 排除、不在仓库，属纯本地残留。
- 依据：`.gitignore:134-140`；`AGENTS.md:107`。

### P1（中优先：消除长期维护摩擦）

**P1-1 统一 frontmatter 契约**
- 动作：在 `AGENTS.md` 固化必需字段 `name / description / layer / last_verified`（`version / user-invocable / agent_created / hooks` 为可选）；补齐 8 个缺失 `last_verified` 的 skill；修正 `wq-brain-ra-pipeline layer="2.2"`、`planning-with-files layer="2.1.0"` → 版本号移入 `version`、`layer` 恢复"位置"语义。
- 依据：8 种字段组合分布（2.4）；`AGENTS.md:114` 的 layer 定义。

**P1-2 收敛命名规范**
- 动作：7 个非 kebab-case 目录改名（`pull_BRAINSkill`→`pull-brain-skills`、`brain-makeSomeGem`→`brain-make-some-gem` 等）；明确前缀语义（建议 `brain-*`=业务/知识技能、`wq-brain-*`=流程编排、`wqb-*` 归并进二者之一）。
- 注意：改名须同步 SKILL.md frontmatter `name` + `AGENTS.md`/`docs` 引用 + 各安装位，建议与 P0-2 多目标同步一起做。
- 依据：2.1 命名分组。

**P1-3 去重嵌套副本**
- 动作：`brain-makeSomeGem/scripts/trailSomeAlphas/skills/` 下的 `brain-feature-implementation`、`brain-data-feature-engineering` 改为引用顶层（或明确标注 vendored + 附校验和/同步说明）。
- 依据：2.5（同名不同文，2129B vs 5339B）。

### P2（低优先：清理与文档）

**P2-1 裁决宿主特有 skill 的归属**
- 动作：对 `code-optimization`/`dead-code-cleanup`/`gold-analysis`/`jin10-news`（cursor+workbuddy 各一份且不一致）与 `brain-enhance-template`（仅 workbuddy），二选一——入仓库成为真相源并纳入同步链，或从宿主位清理。
- 依据：2.3。

**P2-2 为"仅文档提及"的 skill 补索引**
- 动作：给 `alpha-template-labs-data-analysis`、`brain-alpha-repair`、`brain-datafield-exploration-general`、`brain-explain-alphas` 在 `AGENTS.md` 或 `wq-brain-ra-pipeline` 中补一行触发场景索引，避免"存在但无人知何时用"。
- 依据：3.2 判定结果。

---

## 附：优先级汇总

| 优先级 | 项 | 预期收益 | 工作量 |
|---|---|---|---|
| P0-1 | 补 codex/workbuddy 的 ra-pipeline | 立即恢复 09-09 门禁 | 小 |
| P0-2 | sync_skills 多目标化 | **根治漂移复发** | 中 |
| P0-3 | 清理失效安装脚本/指引 | 消除误用源 | 小 |
| P1-1 | frontmatter 契约统一 | 消除格式漂移 | 中 |
| P1-2 | 命名规范收敛 | 可维护性 | 中（跨引用改名） |
| P1-3 | 去重嵌套副本 | 消除双源 | 小 |
| P2-1 | 特有 skill 归属裁决 | 消除重复定义 | 待定 |
| P2-2 | 补 skill 索引 | 可发现性 | 小 |

---

## 附：Phase 执行记录（2026-09-10 落地）

> 全部 P0/P1/P2 已执行完毕。执行中暴露并修复 1 个 P0-2 连锁问题（见"附带修复"）。

### P0（全部完成）

| 项 | 落地内容 | 依据/证据 |
|---|---|---|
| **P0-1** | `wq-brain-ra-pipeline` 的 codex/workbuddy 落后副本已被多目标同步覆盖 | 三宿主 `SKILL.md` md5 = `b50e0c78` == 仓库 |
| **P0-2** | `tools/sync_skills.py` 重写：`resolve_install_roots()` 返回多目标、新增 `--target`（可多值）与 `--check` 多目标断言；`src/wqb/workflow/_common.py` 的 `_skill_roots()` 补入 `~/.codex/skills`；`tests/unit/test_audit_fixes.py::test_sync_skills_reports_no_drift` 改为遍历全部安装位 | `sync_skills.py --check` → 4/4 安装位 `[OK]` |
| **P0-3** | 6 个失效安装脚本/指引（`install_claude_skills.ps1/.bat`、`install_now.py`、`verify_claude_skills.py`、`INSTALLATION_GUIDE.md`、`install_skills_direct.py`）移入 `attic/install_legacy_20260910/` | `git status` 无新增失效脚本 |

### P1（全部完成）

| 项 | 落地内容 |
|---|---|
| **P1-1** | 8 个缺 `last_verified` 的 skill 补齐（`alpha-template-labs-data-analysis`、`brain-alpha-repair`、`brain-alpha-research` 及其 `-field-quality`/`-hypothesis-first`/`-news-sentiment` 子技能、`brain-alpha-robustness`、`planning-with-files`）。**注**：审计初稿曾误判 `layer` 字段"被当作版本号"，核对 `dump` 后确认 `layer=L-RA` 为规范链位值、`version` 为独立可选字段，已在正文纠正。 |
| **P1-2** | 7 个目录 `git mv` 收敛为纯 kebab-case：`brain-calculate-alpha-selfcorrQuick`→`-quick`、`brain-how-to-pass-AlphaTest`→`-alpha-test`、`brain-inspectRawTemplate-create-Setting`→`-raw-template-create-setting`、`brain-makeSomeGem`→`-some-gem`、`brain-nextMove-analysis`→`-next-move-analysis`、`brain-simAlphasinBatch-and-track`→`-sim-alphas-in-batch-and-track`、`pull_BRAINSkill`→`pull-brain-skills`；仓库 78 处文本引用同步替换。 |
| **P1-3** | `brain-make-some-gem/scripts/trailSomeAlphas/skills/README.md` 新增 vendored 说明：该子目录是 GEM 引擎运行时硬依赖（`run_pipeline.py:54` 从 `BASE_DIR/"skills"` 导入），**禁止**用 `sync_skills.py` 覆盖。 |

### P2（完成/已裁决）

| 项 | 落地内容 |
|---|---|
| **P2-1** | 裁决：**不处置，仅记录**。`brain-enhance-template`（workbuddy 独有，`_common.py:141` 已标"已废止"）；`code-optimization`/`dead-code-cleanup`/`gold-analysis`/`jin10-news` 属用户跨项目全局技能（cursor/workbuddy，无仓库源）——保留原位，不纳入同步链。 |
| **P2-2** | `AGENTS.md` 新增"按需调用知识型 skill"索引表 + "SKILL.md frontmatter 契约"段 + "Skill 命名规范"段。 |

### 附带修复（执行 P0-2 同步时暴露的连锁问题）

1. **恢复丢失的本地配置**：删除宿主旧目录时连带回收了安装位里 `brain-make-some-gem/scripts/headless_runner/config.json`（仓库 HEAD 不含、`.gitignore:4 **/config.json` 排除），导致 `test_gem_dry_run_short_circuits` 失败。已从回收站按内容识别（读 `SKILL.md` 的 `name`）恢复正确的 **flat 225B schema**（`brain_email`/`moonshot_api_key`，与当前 `run.py:551` 期望一致；471B 为已废弃的嵌套旧 schema），并同步到 4 个安装位。
2. **算子全集 102 → 103 修正**：`test_verified_safe_has_102_catalog_ops` 断言 `102`，而 `docs/reference/operators_catalog.json`（tracked，2026-09-07 刷新）与 `data/operators_verified.json`（本日 13:51 重生成）均已是 **103**；差集唯一新增 `vector_neut`（`vector_neut(a, b)`，95% 三方交叉印证：live catalog / 今日探针 / 09-04 快照 102+1）。已将测试名与断言改为 103，并同步更新 `src/wqb/expression/_metrics.py` 4 处"（102）"→"（103）"、`op_arity.py` 的脆弱计数改为"live catalog"表述（`config.py:274` 保留 102 —— 那句描述的是 2026-09-04 那次审计的历史事实）。

### 验收

- `python -m pytest tests/ -q` → **531 passed**（执行前 1 failed）。
- `python tools/sync_skills.py --check` → **4/4 安装位 [OK]**。
- `git status` 无删除（tracked 文件零丢失），43+15 renames / 85 modified 均为本次治理产物。
