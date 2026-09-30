# WQ/BRAIN Skills 契约（CONTRACT）

> 本文是 skill 的**写作契约**：frontmatter、职责边界、命名、硬裁定、共享产物归属、质量门禁。
> 从 `INDEX.md` 拆出（skills 审查 IX-01）：INDEX 只管**路由与分层**，契约在这里，变更历史在 [`CHANGELOG.md`](CHANGELOG.md)，术语与状态词表在 [`GLOSSARY.md`](GLOSSARY.md)。
> `AGENTS.md` 的「Skill layer 取值表 / frontmatter 契约 / 命名规范」是同一套规则的摘要；冲突以本文为准并同步 AGENTS.md。
> **写 skill 时的定位**：SKILL.md 只放**规则**（≤ 250 行为目标）；实证叙事、事故、区域细节放 `references/`；带日期的变更进 `CHANGELOG.md`；快照类事实必须带 `as_of` 与失效条件，或改成命令生成。

## 1. frontmatter 规范（所有 SKILL.md 必须）

```yaml
---
name: <dir-name>                 # 必须与所在目录名一致（tests/unit/07_docs_skills/test_skill_integrity.py 校验）
layer: <L-RA|L-PRE|L-TOOL|L0|L1|L2|L3|L4|L5|L6|L7>   # 挖掘链条位置，不是优先级、也不是版本号
description: "..."               # 单行双引号字符串；≤ 300 字；只写「何时触发 + 范围 + 不做」，不写实现细节
last_verified: YYYY-MM-DD        # 最近一次对照代码 / 平台核实内容正确的日期
allowed-tools:                   # 可选；写了就必须是 YAML 列表，禁止块标量
  - Read
  - Bash
---
```

| 字段 | 是否必需 | 含义 / 规则 |
|---|---|---|
| `name` / `layer` / `description` / `last_verified` | **必需** | `layer` 取值见 AGENTS.md「Skill layer 取值表」。`description` 是**触发条件**（不是功能清单）：最长 300 字（`tests/unit/07_docs_skills/test_sf_docs.py` 守护），此前最长 702 字。批量机械刷新 `last_verified` 无效——它必须随内容核对而改 |
| `allowed-tools` | 可选（**缺省 = 继承宿主默认权限**） | 声明时只列该 skill 实际要用的工具。**能力棘轮**：任何 skill 不得比 `tests/fixtures/skill_capabilities_baseline.json` 多出工具；要加，先改基线并写明理由，由人审查 |
| `user-invocable` | 可选 | `true` = 该 skill 也可由用户以 `/<skill 名>` 直接调用，而不只是被 agent 按 description 触发；不影响路由与边界 |
| `version` | 可选 | 外部来源 skill 的**上游版本号**，只登记来源，与本库的 `last_verified` 无关 |
| `agent_created` | 可选 | 仅模型创建的技能标注 |
| `hooks` | 可选（**受限**） | 在 agent 生命周期事件上自动执行的命令，等价于任意命令执行：只有白名单内的 skill 可声明（现只有 `planning-with-files`），必须在该 skill 正文逐条写明每个钩子做什么与成本，经人工审查后才可加入白名单。钩子命令不得含未解析占位符（如 `<SKILL_ROOT>`）、外发、动态执行、删除、凭据读取——`tests/unit/07_docs_skills/test_skill_hooks_and_tools_guard.py` 守护 |

禁止出现 `when_to_use` / `trigger_when` / `title` 等非标字段。

## 2. 正文必备段：`## 职责边界`（新 skill 缺此段不予合入）

frontmatter 只说「我是谁」，**职责边界**才说清「我不管什么、该找谁」。所有 SKILL.md 正文必须在 H1 标题之后紧跟该段，格式为**三条**：

```markdown
## 职责边界

- **本 skill 负责**：<产物 / 动作>
- **本 skill 不做**：<明确排除>（遇到 → 转 <skill 或工具>）
- **上游 / 下游**：上游 = <谁给我>；下游 = <我给谁>
```

由 `tests/unit/07_docs_skills/test_skill_boundaries.py` 机械守护（缺段 / 缺条目即红）。**这只是形式覆盖**——它不保证内容为真：2026-09-29 审查发现至少 6 个 skill 的边界声明与正文 / 代码矛盾（submit-alpha 声称只管 REGULAR 而正文含 SUPER / PPA，judge 声称不提交而脚本能 POST，monitor 声称不是写入方而强制回写……）。所以：**边界段里「不做」的动作，正文出现时必须带「仅引用」标记或指向承接者**；内容一致性靠各 skill 的 doc→code 测试（如 `test_se_docs.py`）和 `tools/skill_lint.py` 棘轮。

**两条硬裁定（写入边界段时须遵守）**：

1. **skill 不得改写权威常量**。`src/wqb/config.py` 的 `REGIONS` / `REGION_PRIORITY` / `GATES` / `PLATFORM_CHECK_LINES` / `CONCURRENCY` / `WAIT_THRESHOLDS` / `PARADIGMS` / `SHAPE_CLASSES` 是唯一权威；skill 只能**引用**，**禁止**用「修正为…」/「撤回…」/「实测推翻…」等口吻改写，也不要在文档里复写数字（要写就写「见 `config.X`」）。若 skill 的实证观测与常量冲突，**保留观测但显式标注冲突并裁定以 config 为准**（样板见 `brain-alpha-research` §12(a)）。
2. **同一产物只能有一个主写方**。DB 表 / 产物文件若被多个 skill 提及，边界段必须写明「唯一正式写入方 = X；Y 仅在 <场景> 作逃生阀」（样板见 RA `step9-writeback.md` §9.4 与 `brain-sim-alphas-in-batch-and-track` 对 `wave_results` 的约定）。

## 3. 命名规范

目录名与 frontmatter `name` **一律纯 kebab-case**（小写字母 + 连字符），禁止驼峰与下划线。前缀语义：`brain-*` = 业务 / 知识技能；`wq-brain-*` = 流程编排；`wqb-*` = 横切工具（并发等）。`wq-brain-campaign-toolkit` 是该规范下首个**引擎层**（L-TOOL）实例。

**改名配套动作**（缺一即断链）：`git mv` 目录 → 全库 grep 替换引用 → 改代码侧硬编码（如 `src/wqb/workflow/nodes/gem.py` 的 `resolve_skill_dir("brain-make-some-gem")`）→ `tools/sync_skills.py` 推送到全部安装位。历史改名清单在 [`CHANGELOG.md`](CHANGELOG.md)。

## 4. 共享产物归属

> 背景：硬裁定②此前实质覆盖率仅 1/33（全库只有 `campaign-toolkit` 一处写明），「谁写 / 谁读」没人写清，直接导致两起事故：① `priors_snapshot` 无人认领刷新责任，GBR 快照落后 KB 源 8 天；② `wave_gate` 三方调用无主写方，自动链 100% `TypeError`。
> **ledger 键的完整目录**（键 / 写入方 / 读取方 / 刷新责任 / 状态，含「有读取方无写入方」的登记）在 [`docs/ledger_keys.json`](../../docs/ledger_keys.json)，由 `tools/ledger_keys.py`（扫描代码与文档并对账）与 `tests/unit/01_store_db/test_ledger_key_catalog.py` 守护：skill 里出现的每个 ledger 键必须在目录内，有读取方而无写入方的键必须登记 `orphan`。下表只列**共享产物的最小权威清单**；新增共享产物必须同步此表。

| 产物 | 唯一正式写入方 | 只读消费方 | 刷新 / 失效责任 | 逃生阀 |
|---|---|---|---|---|
| `wave_results` | **`wqb.wave_results_contract.upsert_wave_result`**（唯一写入函数：verdict 枚举归一 / 合并语义 / closed 须带 verdict）；入口两个且等价——MCP `upsert_wave_result`、toolkit `campaign.py wave upsert`，都走这个函数 | ra-pipeline 步 9、`wq-backtest-monitor`（只读核验） | 波级收尾由 S6 回写（顺序与契约见 RA `step9-writeback.md`） | —（有 MCP 用 MCP，无 MCP 用 CLI；不要两边各写一遍） |
| `registry_empirical` | toolkit `campaign.py registry` / `upsert_registry_empirical`（写入契约 `wqb.registry_contract`，两条路径同一份校验） | ra-pipeline 步 1–2、`wq-brain-campaign-matrix` | 每波 S6 回写 win / dead | 会话内轻量 `upsert_registry_empirical` |
| `ledger_kv` | toolkit ledger 子命令 | ra-pipeline 各步、`brain-*` 只读 | 按键定（见目录）；`s0_whitelist` 有契约归一（replace / merge 双侧 canonicalize） | 会话内 `upsert_ledger_key` |
| `expressions` | `brain-make-some-gem`（S2 生成；`run_pipeline.py` 收尾自己写，`status=gem`） | 门禁闸、S3 回测 | 状态推进走 `set_expression_status` | — |
| `field_catalog` | S1 `scan_fields` → `upsert_field_catalog` | 门禁闸 2 字段白名单、GEM（**只读**；已存在则跳过概念化） | 换数据集 / 换 delay 时重建 | — |
| **`priors_snapshot_<region>`** | **`workflow_campaign(stage=S2, subcommand=assemble-priors)`（唯一）** | **`brain-make-some-gem`（只读，禁止回写）** | **S6 复盘回写后必须重跑**（默认带 `--snapshot-ledger`）；否则下一波 GEM 读旧先验 | 无。GEM 侧发现 stale 仅 WARN，**不得据此继续实跑**（2026-09-27 GBR 实证落后 8 天） |
| `submit_ready`（SQL 表，**单存储**；同名 ledger 键只是 legacy 审计副本） | `wqb.store.submit_queue`（S3 收批 `harvest_multisim` 过闸候选自动入队、提交后自动退役；DEC-33） | 步 8 提交判定（MCP `get_submit_ready`）、`tools/submit_queue.py`、`super_build.py` | 每次 prod 复检后刷新（库内值会过期，提交前必须实测） | — |

`<SKILL_ROOT>` 表示技能库根目录。**真相源 = 仓库 `Claude/skills/`**，各宿主安装位由 `tools/sync_skills.py` 同步（见 INDEX「权威副本与生效方式」）。脚本入口一律经 `$WQ_TOOLKIT_DIR` / `$WQ_VALIDATOR_DIR` 引用，禁止在 SKILL.md 中写出含用户名的绝对路径。

## 5. 质量门禁

新增或修改 skill 后，必须跑：

```bash
$WQ_PY -m pytest tests/unit/07_docs_skills/test_skill_integrity.py tests/unit/07_docs_skills/test_skill_boundaries.py tests/unit/07_docs_skills/test_docs_consistency.py tests/unit/07_docs_skills/test_sf_docs.py -q
$WQ_PY tools/sync_skills.py            # 仓库 → 全部安装位（改完必须 sync 才对 Agent 生效）
$WQ_PY tools/sync_skills.py --check    # 仓库与全部安装位零漂移
$WQ_PY tools/skill_lint.py             # 命令 / 子命令 / 必填参数 / MCP 签名 / 表达式过闸 / .env 读取 / 裸 python 棘轮
```

校验内容：

- 每个 `SKILL.md` 存在且 frontmatter 完整；`name` 与目录名一致；`layer` 合法；`description` ≤ 300 字；`allowed-tools` 为 YAML 列表且不超出能力基线。
- **每个 `SKILL.md` 正文含 `## 职责边界` 段，且具备「本 skill 负责 / 不做 / 上游·下游」三条**。
- 无已废弃路径引用（`.workbuddy/skills/` / `.qoder/skills/` / `.cursor/skills/`）；skill 内相对链接与 `.py` 引用指向真实存在的文件——范围含 `references/**/*.md`（`test_docs_consistency.py` 递归扫描全部 `*.md`）。
- 计数 / 闸表 / 区域表 / 环境变量表由代码生成并逐字比对（`test_docs_consistency.py`、`test_gate_registry_docs.py`、`test_waiver.py`、`test_index_tables.py`）。
- 「唯一 / 权威」宣称、命令与参数、表达式过闸、裸 `python`、`.env` 读取指令：`tools/authority_claims.py` 与 `tools/skill_lint.py` 的棘轮（只许减不许增）。

**失败于环境 vs 失败于内容**：守护测试若依赖宿主状态（`~/.claude/skills` 里的非仓库目录）或未入库的运行态数据（`data/operators_verified.json`），必须 **skip 并说明原因**，不得让干净克隆红；被守护的 skills 目录可用 `WQ_SKILLS_DIR` 指定。校验不通过（exit 1）时禁止合并 / 发布。
