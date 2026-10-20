# Skills 内容审查与治理建议（2026-10-20）

> 范围：`Claude/skills/` —— 47 个 skill 目录 + 4 份根文档（INDEX / CONTRACT / GLOSSARY / CHANGELOG），合计 9.0 MB；`references/` 共 273 个文件 / 3.4 MB。
> 方法：只读审查（机器读数 + 逐文件抽样核查）。本轮未修改任何 skill、未写台账、未提交。
> 归属：本报告是人工审计，按 AGENTS.md §8.13 放 `reports/<主题>_<YYYYMMDD>.md`。

## 0. 结论速览

结构治理的底座是有效的：结构审计 FAIL=0、6 个安装位零漂移、frontmatter / 职责边界 / 命名都有机械闸。**问题集中在内容层——references 没有准入、索引与退休机制**：

- `references/` 已成为第二个「战役数据湖」：USA 一个 skill 占 **54 个文件 / 1.1 MB**（全部 references 的 41%），其中 **34 个文件在 SKILL.md 中没有链接**；今天新增 26 个未跟踪档案。
- 当前工作树**门禁红灯**：`tools/skill_lint.py` 退出码 1，53 条违规中 **27 条是新增**（USA 25、EUR 2），全部来自在途文件。按现有 pre-commit，这一状态无法提交。
- 四类系统性问题：① references 无准入/索引/退休；② 权威阈值仍在文档中复写（26 条存量基线）；③ `last_verified` 被批量盖章（44/47 同为 2026-10-18），已失去判别力；④ 区域入场状态不在 description，路由要到步 1 才失败。
- 另有两处结构债：5 个 SKILL.md 超过 CONTRACT 的 ≤250 行目标（KOR 604 行最严重，生成块只占约 12%）；4 组跨 skill 重复脚本。

## 1. 现状读数（机器证据）

| 项 | 读数 | 证据 |
|---|---|---|
| skill 目录 | 47（+4 份根文档） | `ls -d Claude/skills/*/ \| wc -l` |
| 体量 | 9.0 MB | `du -sh Claude/skills` |
| references | 273 文件 / 3.4 MB | `find Claude/skills/*/references -type f \| wc -l` |
| references 索引 | **0 个 `references/README.md`**（37 个 skill 有 references 目录） | `ls Claude/skills/*/references/README.md` |
| USA 单 skill | 54 文件 / 1.1 MB；34 个未在 SKILL.md 出现 | 逐文件比对 |
| 安装位同步 | 6/6 零漂移 | `tools/sync_skills.py --check` |
| 结构审计 | FAIL=0，WARN=4 | `tools/audit_structure.py` |
| **内容 lint** | **EXIT=1；53 违规 = 40 const-literal + 13 expr-gate；新增 27** | `tools/skill_lint.py` |
| 死指针 | 无新增；12 条基线；1 条 UNTRACK | `tools/code-audit/doc_path_refs.py` |
| 跨 skill 重复脚本 | B=4 组 | `tools/audit_skill_drift.py` |
| docs/skills 测试 | 1 failed / 694 passed（失败项即 lint 棘轮） | `pytest tests/unit/07_docs_skills/` |
| SKILL.md 行数 Top5 | KOR 604 / GBR 327 / pipeline 280 / DEU 264 / toolkit 254 | `wc -l` |
| allowed-tools | 36 个用 `mcp__wq-brain-http__*` 通配；10 个显式；1 个未声明 | `grep -l` |
| last_verified | 44×2026-10-18，3×2026-10-20 | `grep '^last_verified'` |

新增 27 条的分布：按 skill = USA 25、EUR 2；按类型 = const-literal 14、expr-gate 13（`equal_weight_leg_add` 9 + `infix_leg_sum` 4）。全部落在**在途文件**：USA 的 26 个未跟踪 `_usa-*-field-profile-20261020.md`，EUR 已暂存的 `_boundary-ops-eur.md`。

## 2. P0 —— 先处理，否则门禁不可信或无法提交

### 2.1 让 lint 转绿：27 条新增是「内容放错位置」而非文档笔误

field profile 本质是**战役档案**：数据集坐标、字段拥挤度、字段族、模板、逐批指标、原始表达式。它现在被存在 skill 的 `references/` 下，而 `skill_lint` 会扫描 skill 树里的每个 `.md`，于是研究记录里的 `add(腿A, 腿B)`、中缀求和被当成「毒模式」拦下。

这不是靠加几个反引号能长期解决的，建议按所有权处理：

- **首选（A+C）**：逐数据集 / 逐战役档案移出 skill 树 → `tracking/<REGION>/reference/` 或 `output_report/`；`references/` 只保留「跨波可复用」的方法论（playbook、数据集类别分支、判死清单）。档案里的交付状态、alpha ID、prod/self 数值本来就应该以 DB 为准。
- **过渡（B）**：保留下来的表达式证据块用 `<!-- lint:counterexample -->` 包裹（该机制已有 9 个文件在用，不是新造轮子）；同时在**生成端**加一次 lint，让违规在生成时失败，而不是等人提交时才红。
- 本轮不要批量改写其他会话的在途文件；先与 USA/EUR 的写入方对齐归属。

验收：`tools/skill_lint.py` 退出码 0；「相对基线新增 = 0」；基线只减不增。

### 2.2 references 的准入、索引与退休

现状足以说明问题：

- 273 个文件、3.4 MB、**零索引**；查找依赖 SKILL.md 手写链接，USA 有 34/54 文件不可达。
- `_usa-atom-delivery-log-20261020.md` 是**交付台账**（10/10、alpha ID、ACTIVE 状态、prod/self 数值）。这类内容会随平台状态变化，放进 skill 等于与 DB 真相源竞争；它应属于 `tracking/USA/reference/` 或 `output_report/`。
- 同步器会把 references 复制到 6 个安装位：USA 1.1 MB × 6，且过期结论会随同步扩散。
- 旧战役档案与新档案并存（20261014 / 20261018 / 20261019 / 20261020），没有 `active / superseded` 标记，agent 无法判断哪份是当前口径。

建议落一条 **references 契约**（写进 CONTRACT，并由测试守护）：

1. **准入**：只收「跨波可复用」的知识；单战役/单数据集的原始档案、交付日志、状态表一律外置到 `tracking/<R>/reference/` 或 `output_report/`。
2. **索引**：每个 skill 生成 `references/README.md`（文件、一句话用途、`as_of`、状态 active/superseded、owner），由工具生成而非手写。
3. **退休**：带日期的战役档案超过 N 天（建议 30）移入 `attic/` 或区域 reference；同一主题只保留最新一份 playbook。
4. **上限**：每 skill references ≤20 文件 / ≤300 KB（可按存量设基线，只许下降）。
5. **可达性**：每个 reference 必须被 SKILL.md 或 `references/README.md` 链接；未链接文件不得新增。

验收：新增 `test_skill_references_contract.py`（索引存在、可达、体积/数量棘轮）；USA 从 54 文件降到上限内；无未链接文件。

### 2.3 阈值数字单源化（存量 26 条基线）

`skill_lint` 的 40 条 const-literal 里，26 条在基线中，分布在提交链与诊断链的高风险文档：judge（PROD<0.7 / SELF<0.5）、submit-alpha、robustness（1.58 / 1.6）、repair、field-quality、selfcorr、next-move、GLOSSARY、optimization、pipeline 的 decision-table / loop-and-stop / prod-corr-avoidance / regions/GLB。

典型反例：`prod-corr-avoidance.md:39` 先写「见 `wqb.config` 的平台线」，下一句又写 `< 0.7` ——两边都占，既没有单源，也保留了漂移面。

建议：按 CONTRACT §2 硬裁定做一次机械替换（`见 config.PLATFORM_CHECK_LINES / GATES_PLATFORM / GATES_INTERNAL`），逐条删除基线项；不要用「实测推翻 / 修正为」的口吻改常量。验收：const-literal 违规 0（或仅剩带 `<!-- from config.X -->` 的引用）；基线无陈旧项。

### 2.4 `last_verified` 的语义与守护

44/47 个 skill 同为 `2026-10-18`，另 3 个为 `2026-10-20`。守护测试只要求「不早于最后一次提交 2 天以上」，于是批量刷新是**理性反应**，而不是治理失败。结果是这个字段不再区分「真的核对过」与「顺手改的日期」。

建议二选一：

- **方案 A（推荐，改动小）**：保留 `last_verified`，新增 `verified_by`（证据路径或命令）与 `content_sha`（非生成块正文哈希）。日期变更时哈希必须变；工具自动核对。
- **方案 B（更彻底）**：从 frontmatter 去掉日期，由 INDEX 从 git 计算「最后实质变更日」，skill 正文只写 `as_of` 快照条件。

验收：一条测试/工具能拒绝「只改日期不改内容」的提交；INDEX 仍能展示新鲜度。

## 3. P1 —— 结构与路由

### 3.1 超长 SKILL.md

CONTRACT 的目标是 SKILL.md ≤250 行；实测 KOR 604、GBR 327、pipeline 280、DEU 264、toolkit 254。KOR 更特殊：604 行里生成块（region-panel + manual）只有约 74 行（12%），其余是手写的六步方法论。

建议：

- KOR：六步纵深正文 → `references/_six-step-kor.md`；SKILL.md 只留职责边界、控制面板、组合索引、路由。
- GBR：字段画像驱动流程 → references；DEU 同理。
- pipeline：逐步细节 → `references/steps/`，SKILL.md 收敛为九步索引 + 失败分支。
- toolkit：子命令细节 → references，SKILL.md 留契约与入口。

验收：每个 SKILL.md ≤250 行；若确有例外，在 CONTRACT 登记理由（不要静默超限）。

### 3.2 区域路由信息缺失

7 个 probe-only 区（ASI / CHN / DEU / EUR / HKG / IND / TWN）+ MEA frozen；**14 个区域 skill 的 description 没有一个写出入场状态**（实测命中 0）。agent 只能开波到步 1 才被拒，浪费一次调度与上下文。

另有一处口径不一致：INDEX 写「每区一个 `wq-brain-ra-<区域>`（layer `L-RA-R`，14 个）」，而 KOR 的 frontmatter 是 `layer: L4` + `agent_created: true`；AGENTS.md 有例外说明，INDEX 没有。

建议：description 与首屏加 `【probe-only】` / `【frozen】`；INDEX 层表补 KOR 例外脚注；加一条测试比对 profile 的 `entry_verdict` 与 description 标记。

### 3.3 跨 skill 重复脚本（B=4）

`validator.py` ×4、`helpful_functions.py` ×4、`ace_lib.py` ×2、`diversity_enhancer.py` ×2。历史上 `diversity_enhancer` 的旧副本在安装到仓库外时 ImportError 后**静默降级**，多样性增强完全没生效却不报错——重复脚本不是整洁度问题，是正确性问题。

建议：单一实现放 `src/wqb/`（或共享包），skill 路径下只留薄 shim；A 类 GEM 内嵌快照保持现状；更新 `DIVERGED_ALLOWLIST`。验收：`audit_skill_drift` B=0。

### 3.4 `allowed-tools` 过宽

36 个 skill 用 `mcp__wq-brain-http__*` 通配，其中包含提交与 workflow 工具；只有 10 个显式声明，1 个（`brain-dataset-mining-experience`）未声明。最小权限在此基本失效。

建议：逐个改成显式清单；研究 / 监控 / 评审类 skill 不得声明提交类工具（提交只属于 L5 且必须用户确认）；利用现有能力基线测试做棘轮。验收：MCP 通配 0；提交工具只出现在 L5 skill。

### 3.5 死指针与手工复制的「铁律」

- 13 个区域 `rules/README.md` 把 `tools/skill_lint` 写成无 `.py` 的路径，已在 `doc_path_refs` 基线里。建议一次修完并清空该基线项。
- 抽样统计：139 行非平凡内容在 ≥4 个 skill 中重复。生成块（区域面板 / 导航）可接受；手写的锁定项、提交链、阈值副本是漂移面。建议收敛到 pipeline 的一份 canonical 文档，其余链接引用。

## 4. P2 —— 存量清理与长期机制

- `brain-inspect-raw-template-create-setting` 根目录仍有 `ace_lib.py` / `helpful_functions.py`（已知 P2-7），建议移入 `scripts/` 并留 import shim。
- `brain-alpha-judge/data/forum_corpus/` 等 4 个 `data/` 目录是**已登记的静态资产**（非运行期泄漏），保持现状，但在 SKILL.md 里写明快照日期，避免被误当实时语料。
- `planning-with-files` 是唯一声明 `hooks` 的 skill；Stop hook 用内联 `python -c`、PreToolUse 用 `bash -c`，建议改为 `$WQ_PY` + 脚本文件，降低 PATH/引号依赖。
- 在 CONTRACT 增加「skill 发布清单」：lint 绿、sync 零漂移、references 索引与可达性、allowed-tools 复核、无新增阈值字面量。

## 5. 建议执行顺序

1. 与在途 USA/EUR 写入方对齐，暂停往 references 增加战役档案。
2. 处理 27 条新增（外置 / 标记），让 `skill_lint` 与 pre-commit 转绿。
3. 落 references 契约：README 索引 + 准入/退休 + 可达性与体积测试（带基线）。
4. 阈值单源化，清 26 条基线。
5. 区域 description 写入场状态；INDEX 补 KOR 例外。
6. 拆分 KOR / GBR / pipeline。
7. 收敛 4 组重复脚本。
8. 改 `last_verified` 机制（`verified_by` + 内容哈希，或 git 派生）。

## 6. 边界与风险

- 不要在他人未暂存 / 在途文件上批量改写；不要直接删 references（先迁移或归档）。
- 不要手改 `profiles:*` 生成块；不要改 `wqb.config` 常量；不要用「修正 / 推翻」口吻重写阈值。
- 不要为了过闸把文档改成无信息量；本报告只读，未修改任何 skill。

## 7. 多 skills 目录的权威与治理（2026-10-20 补充）

### 7.1 唯一编辑权威与运行时顺序

**唯一编辑权威 = 仓库 `Claude/skills/`**（git 跟踪、可评审）。其余全部是派生安装位。但要注意：**运行时优先读安装位，仓库只是最后的兜底**。`wqb.workflow._common._skill_roots()` 的实际顺序：

```
WQ_SKILLS_DIR > APPDATA/LOCALAPPDATA Claude 位（本机均不存在）
> ~/.claude/skills > ~/.codex/skills > ~/.cline/skills > ~/.agents/skills
> ~/.qoder-cn/skills > ~/.cursor/skills > ~/.workbuddy/skills
> <repo>/Claude/skills（兜底）
```

`~/.qoder-cn/skills` 是指向 `~/.claude/skills` 的 junction（同一物理目录，sync 会自动去重）；`<repo>/.claude/skills` 是指向源的符号链接，供 Cline 项目级扫描，已被 `.gitignore` 忽略，**新 clone 不会自动存在**。`~/.trae-cn/skills` 是历史残根：现有 2 项（均为外部 skill：`local-mineru` / `writing-plans`；3 个旧 wq 副本已于 2026-10-20 清理），不在 sync 目标里，但仍出现在 toolkit / GEM 的 `HOST_DIRS` 中。

### 7.2 本机安装位盘点

（下表为 2026-10-20 清理前的基线；删除后复核见 7.2.1。）

| 根 | 类型 | 顶层 | 源→目标缺口 | 备注 |
|---|---|---|---|---|
| `<repo>/Claude/skills` | **源** | 47 | — | 9.0 MB，git 跟踪 |
| `<repo>/.claude/skills` | symlink → 源 | 47 | 0 | gitignored，新 clone 需重建 |
| `~/.claude/skills` | 拷贝 | 58（47 + 11 外部） | missing=0 / changed=0 | **82 个 install-only 文件（838 KB）**；总 97 MB（含运行产物） |
| `~/.qoder-cn/skills` | junction → `~/.claude/skills` | 同上 | — | sync 去重，不是第 7 个物理目标 |
| `~/.codex/skills` | 拷贝 | 47 + `.system` | 0 / 0 | 82 个 install-only 文件 |
| `~/.cline/skills` | 拷贝 | 47 | 0 / 0 | 24 个 install-only 文件 |
| `~/.agents/skills` | 拷贝 | 47 | 0 / 0 | 24 个 install-only 文件 |
| `~/.cursor/skills` | symlink + 拷贝混合 | 47 + 5 外部 | 0 / 0 | 23 个 symlink；82 个 install-only 文件 |
| `~/.workbuddy/skills` | 拷贝 | 47 + 13 外部 | 0 / 0 | 98 个 install-only 文件 |
| `~/.trae-cn/skills` | 历史残根 | 5 | — | 不在 sync 目标；建议归档 |

### 7.2.1 删除后复核（2026-10-20 10:40）

复核口径：`ls -d` 只数目录、不跟随符号链接；`sync --check` 全量比对**受维护的 5 个物理目标**（Cursor 已关闭）。

| 根 | 清理前 | 现在 | 结论 |
|---|---|---|---|
| 仓库 `Claude/skills/` | 47 skill / 9.0 MB | **47 skill / 9.1 MB** | **源未被删**：`git ls-files` 的 47 个 skill 目录全部在盘 |
| 项目 `.claude/skills` | symlink → 源 | 仍有效 | 无需重建 |
| `~/.claude/skills` | 58 目录（47 + 11 外部） | 58 目录 | 未动 |
| `~/.codex/skills` | 48（47 + `.system`） | 48 | 未动 |
| `~/.cline/skills` | 47 | 47 | 未动 |
| `~/.agents/skills` | 47 | 47 | 未动 |
| `~/.workbuddy/skills` | 60（47 + 13 外部） | 60 | 未动 |
| `~/.qoder-cn/skills` | junction → `~/.claude/skills` | 仍有效 | 无需重建 |
| `~/.cursor/skills` | 47 + 5 外部，23 个 symlink | **已删除（10:40）**；此前 10:28 清空后曾于 10:34 被同步重建为 51 项 | **已在同步源头关闭**：`sync_skills.py::DISABLED_INSTALL_ROOTS`，自动枚举与 `--target` 均拒绝 |
| `~/.trae-cn/skills` | 5（3 个旧 wq 副本 + 2 外部） | **2（仅 `local-mineru` / `writing-plans`）** | wq 副本已清；该根不在 sync 目标，删除可保留 |

四条结论：

1. **源完整**：47 个 skill 目录全部在。`git status` 里唯一的 `D` 是 `wq-brain-ra-eur/references/_probe-sop.md`（并行会话的 EUR 在途改动，已新增 `_boundary-ops-eur.md` 替换），不是本轮清理造成。
2. **删除能否保住，取决于该根是否在 sync 枚举面**：`~/.cursor/skills` 曾在枚举面内且目录仍存在 ⇒ 内容被清空后 6 分钟就被任何一次 `sync_skills.py` 回填。**已处置（2026-10-20）**：`tools/sync_skills.py` 新增 `DISABLED_INSTALL_ROOTS`，自动枚举与显式 `--target` 两条路径都拒绝该根；目录本身也已删除。只删内容不够，必须在同步源头关闭。
3. `~/.trae-cn/skills` 不在 `_common._skill_roots()`、也不在 sync 目标，删除可保留；但 toolkit/GEM 的 `HOST_DIRS` 仍含 `.trae-cn`，属既有的解析顺序不一致（见 7.4 第 4 条），当前不影响解析（`.claude` 在前且齐全）。
4. 当前门禁：`sync_skills.py --check` **5/5 OK**（Cursor 已不在目标集）；`audit_structure.py` FAIL=0 / WARN=4；`skill_lint.py` 仍红（51 条，新增 25 条），全部来自 USA/EUR 在途文档里的混信号示例，与目录清理无关。守护测试：`tests/unit/07_docs_skills/test_sync_skills_disabled_roots.py`（自动枚举跳过 / 显式目标拒绝 / 写盘前拦截）。

### 7.3 关键缺口：`--check` 绿 ≠ 安装位纯净

`sync_skills._check_one()` 只统计 `missing + changed`，**完全不看 `only_target`**；`--prune-orphans` 只处理「顶层名字在仓库不存在」的条目。于是**同名 skill 内部的 install-only 文件永远不会被清理**，也不会让 `--check` 变红。实测例子：

- `~/.claude/skills/brain-forum-browse/references/` 有 9 个仓库已不存在的旧文档（如 `mcp-tools-and-search.md`、`quotas-and-cooldown.md`）。
- `~/.claude/skills/wq-brain-campaign-toolkit/{references,attic,scripts/.pytest_cache}` 有旧 `S2_COMPLIANCE_*`、`enhancement-v2.md` 等 39 项。
- `~/.claude/skills/wq-brain-ra-gbr/references/` 有 5 个旧战役文档；`brain-alpha-judge/outputs/` 是运行产物。

因为 `~/.claude` 在解析链上先于仓库，**agent 读到的可能是这些 install-only 旧文档**，而不是源里的当前版本。这是「多目录」真正的风险，不是磁盘占用。

### 7.4 治理规则

1. **只改源**：任何修改只落 `Claude/skills/`；安装位只读。改完 `sync_skills.py` → `--check` → pre-commit / 测试。
2. **补「目标纯度」**：给 `sync_skills.py` 增加 `--purity`（只报告同名 skill 内的 install-only 文件）与 `--mirror --apply`（按仓库纪律**归档**到 `attic/sync_stale_<date>/<host>/`，不直接删）。运行时产物（`outputs/`、`logs/`、`__pycache__`、`.pytest_cache`）与外部 skill 进白名单。
3. **外部 skill 只登记不清理**：`~/.claude` 11 个、`~/.workbuddy` 13 个、codex `.system`、workbuddy 的迁移 json。写进一份清单（`docs/skills_roots.json`），防后来者误删。
4. **退役死根**：`~/.trae-cn/skills` 的 3 个 wq 副本已于 2026-10-20 清理，剩余 2 个宿主原生 skill（`local-mineru` / `writing-plans`）保持不动；解析顺序不一致仍需对齐——toolkit / GEM 的 `HOST_DIRS` 含 `.trae-cn`，`_common.py` 不含，与 AGENTS「四份必须同序」不一致。最好由一处生成，而不是四份手写。
5. **保留 junction / symlink**：`~/.qoder-cn/skills` 与项目 `.claude/skills` 都不要复制成实目录；为新 clone 提供一条重建符号链接的 setup 命令（该链接被 gitignore）。
6. **`WQ_SKILLS_DIR` 只用于隔离**：测试 / CI 沙箱可设；默认不设，绝不指向仓库根或祖先（现有 `_is_repo_related` 已拒绝）。
7. **定期盘点**：加 `tools/skills_roots_report.py`（或并入 sync），输出每个根的 missing / changed / extras / foreign；pre-commit 只跑 `--check`，盘点按月或发布前跑。

验收：`--check` 绿 **且** 纯度报告为 0（或仅剩基线）；外部 skill 数量与名字不变；死根已归档；四处解析顺序一致。

## 附录：复现命令

```bash
# 规模与结构
ls -d Claude/skills/*/ | wc -l
du -sh Claude/skills
find Claude/skills/*/references -type f | wc -l

# 门禁
world-quant-brain-mcp/.venv/Scripts/python.exe tools/skill_lint.py; echo $?
world-quant-brain-mcp/.venv/Scripts/python.exe tools/audit_structure.py
world-quant-brain-mcp/.venv/Scripts/python.exe tools/sync_skills.py --check

# references 可达性（USA）
cd Claude/skills/wq-brain-ra-usa
for f in references/*.md; do grep -qF "$(basename "$f")" SKILL.md || echo "unlinked: $f"; done

# 行数
wc -l Claude/skills/*/SKILL.md | sort -rn | head

# 重复脚本
world-quant-brain-mcp/.venv/Scripts/python.exe tools/audit_skill_drift.py
```
