# WQ/BRAIN Skills 架构索引（INDEX）

> 本文件是全部 WQ/BRAIN skill 的架构基准：分层定位、挖掘流水线入口规则、闸门阶梯、权威版本声明。
> 修改任何 skill 前先读本文件；新增 skill 必须归入下述某层并更新本索引。
> **last_verified: 2026-09-11**（索引整体有效性锚点；平台 operator/阈值/区域状态变更后须同步刷新）。
> 现行审计：`output_report/skills_multi_copy_audit_20260910.md`（多副本治理 P0/P1/P2）；
> 工具使用率见 `reports/toolkit_usage_review_2026-08-31.md`（更早审计已归档 `attic/`）。

## 唯一权威副本（2026-09-11 修订）

**真相源是仓库 `Claude/skills/`**（git 跟踪、单一可审）；各宿主安装位由 `tools/sync_skills.py`
**多目标同步**（`--target` 可多值、`--check` 断言全部目标无漂移）。历史上"以某个安装位为权威"
的做法已被 2026-09-10 审计废止——那正是漂移反复复发的根因（各安装位互相独立、分叉无人察觉）。

| 位置 | 处置 |
|---|---|
| **仓库 `Claude/skills/`** | **权威**。所有新增/修改只改这里，随后跑 `tools/sync_skills.py` |
| `~/.claude/skills` | Claude Code 安装位（同步目标） |
| `~/.codex/skills` | Codex 安装位（同步目标；2026-09-10 前不在解析链，导致长期分叉） |
| `~/.cursor/skills` | Cursor 安装位（同步目标；WQ 技能为指向 `.claude` 的 Junction，非独立拷贝） |
| `~/.qoder-cn/skills` | 历史位，整目录 Junction 到 `~/.claude/skills`（sync 去重后不单列） |
| `~/.workbuddy/skills` | WorkBuddy Agent 工作区（同步目标；另含非 WQ 全局技能，见文末注） |
| `<wqb>/.qoder-cn/skills/_unpacked_wq`（26 个，停留 08-17） | 已归档 `attic/skills_archive/2026-08-23-pre-consolidation/proj-qoder-cn-skills/` |
| `<wqb>/.workbuddy/skills/_unpacked_brain`（35 个，混合体） | 已归档 `attic/skills_archive/2026-08-23-pre-consolidation/proj-workbuddy-skills/` |
| `world-quant-brain-mcp/.venv/.../cnhkmcp/untracked/skills`（20 个，含已废弃 `brain-improve-alpha-performance`） | 第三方包内僵尸副本，**禁止调用**，随包升级自行消失 |

`tools/gate.py` / `tools/wave_gate.py` 的解析顺序为 `WQ_VALIDATOR_DIR`/`WQ_TOOLKIT_DIR` →
`~/.claude/skills` → `~/.codex/skills` → `~/.qoder-cn/skills` → `~/.cursor/skills` →
`~/.workbuddy/skills` → 仓库 `Claude/skills`（兜底），与 `src/wqb/workflow/_common.py::_skill_roots()` 保持一致。

## 运行环境铁律（全体 skill 共同前置）

所有 Python 命令使用 MCP venv，统一经变量 **`$WQ_PY`** 引用，不要硬编码绝对路径、不要使用系统 Python。

**战役产物持久化铁律（2026-08-24 全量切库）**：Agent 持久化只走 `mcp__wqb-db__*` 或 `campaign.py` / toolkit 脚本的 `--from-db`；**禁止** `Write` / `Copy-Item` 战役 json/csv（`candidates/*.json`、`cache/w*_batches.json`、`cache/gate_wave*.json`、`results/*.csv`、`reviews/*.json`、`final_expressions.json` 当真相源）。静态配置（`settings.json`/`thresholds.json`/`platform_constraints.json`）与凭证、CLI 临时 `@file.json`、BRAIN 原始 CSV 仍用文件。

**`$WQ_PY` 定义（本机单一事实源）：**
```bash
# bash / sh
export WQ_PY="D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe"
```
```powershell
# PowerShell
$WQ_PY = "D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe"
```

换机器或换 venv 路径时，**只改此处定义**，全体 skill 文档内的 `$WQ_PY` 引用自动生效。各 skill 正文中出现的 `$WQ_PY` 一律按本定义解析。

## 区域清单（权威：`src/wqb/config.py::REGIONS`）

区域集合的唯一事实源是代码常量 `src/wqb/config.py::REGIONS`（**14 个**）。skill 文档、profile 目录、
战役目录三者必须与下表一致——2026-09-11 审计曾发现"代码 14 / profile 11 / 各处口头清单各异"的三方漂移。

| region | profile<br>`wq-brain-ra-pipeline/references/regions/<R>.md` | 战役目录<br>`tracking/<R>/` | `entry_verdict` |
|---|---|---|---|
| AMR | ✗ 未建 | ✗ | —（`config.REGIONS` 有；无 profile → ra-pipeline 按"处女地模板"路由） |
| ASI | ✓ | ✓ | `probe-only` |
| CHN | ✓ | ✓ | `probe-only` |
| DEU | ✓（2026-09-11 补） | ✓ | `active` |
| EUR | ✓ | ✓ | `active` |
| GBR | ✓ | ✓ | `active` |
| GLB | ✓ | ✓ | `active` |
| HKG | ✓ | ✓ | `probe-only` |
| IND | ✓ | ✓ | `active` |
| JPN | ✗ 未建 | ✗ | —（`config.REGIONS` 有；**本工作区未启用**，无 profile/战役目录） |
| KOR | ✓ | ✓ | `active` |
| MEA | ✓ | ✓ | `frozen`（步 1 即拒；唯一后门见该区 profile） |
| TWN | ✓ | ✗ | `probe-only` |
| USA | ✓ | ✓ | `active` |

规则（与 `wq-brain-ra-pipeline` 步 1 一致）：
- **有 profile 的区**按其 profile 注入静态配置 / 先验 / 闸门覆盖 / 循环策略执行。
- **无 profile 的区**（AMR / JPN）走"处女地模板"（参照 ASI profile）；开新区前必须先补 profile + `tracking/<R>/config/`。
- `frozen` 区（MEA）步 1 直接拒绝，不进入步 2。
- 新增/删除区域时必须同步四处：`src/wqb/config.py::REGIONS`、本表、profile 文件、战役目录。

## 分层架构（L0–L7）

```
L-RA 编排        wq-brain-ra-pipeline（唯一挖掘编排：region→RA 九步 + 日循环/一键战役/PPA 分支；brain-deepExplore 已并入并废止）
L-INT 编排       （brain-alpha-orchestrator 已于 2026-08-31 并入 wq-brain-ra-pipeline）
L-PRE 战役查表   wq-brain-campaign-matrix（区域×数据集矩阵：输入 region → 预解析配置包；registry=data/wqb.db 单轨 SQLite，registry_empirical 表；战役后强制回写台账）
L-TOOL 战役引擎 wq-brain-campaign-toolkit（region 无关执行引擎：gate/pipeline/wave/probe/ledger/scan/review/diversity，输入=战役目录+子命令；服务 S1–S6 多阶段，为战役脚本唯一权威实现）
L0  情报选题     brain-next-move-analysis · brain-forum-browse · wq-brain-ppa-mining
                 · alpha-template-labs-data-analysis（S0 前 Brain Labs 原始数据分析）
L1  数据理解     brain-dataset-exploration-general · brain-datafield-exploration-general
                 · brain-data-feature-engineering · brain-alpha-research
                 · brain-alpha-research-field-quality · brain-alpha-research-hypothesis-first
                 · brain-alpha-research-news-sentiment
L2  表达式生成   brain-make-some-gem · brain-feature-implementation
                 · alpha-expression-verifier
L3  设置仿真     brain-inspect-raw-template-create-setting
                 · brain-sim-alphas-in-batch-and-track · wqb-concurrency
L4  诊断优化     brain-how-to-pass-alpha-test
                 · wq-brain-alpha-optimization-v1（两模式：Mode B 想法层 + Mode A 参数层）
                 · brain-calculate-alpha-selfcorr-quick
                 · brain-explain-alphas
                 · brain-alpha-robustness（S4→S5 必经闸）
                 · brain-alpha-repair（弱候选修复配方；改进入口仍为 optimization-v1）
L5  过闸提交     brain-alpha-judge · worldquant-submit-alpha · wq-brain-superalpha
L6  监控复盘     wq-backtest-monitor
L7  元技能       pull-brain-skills · planning-with-files
```

## 外部扩展区迁入记录（2026-08-23 完成）

原「外部 Agent Skill 登记」段登记的 4 个 skill 历史上只存在于项目内 `.workbuddy/skills/_unpacked_brain/` 扩展区，
2026-08-23 已全部迁入本权威目录并归层，外部扩展区随项目级副本一并归档：

| name | 迁入层 | 功能 |
|---|---|---|
| ~~brain-alpha-orchestrator~~ | — | 2026-08-31 已并入 `wq-brain-ra-pipeline`（独有硬门已迁移：ghost-op/PPA 门禁、check_batch+check_expr_against_inspect、批次故障协议、failed-count 资格门） |
| brain-alpha-repair | L4 | 弱候选修复（5 轴旋转 + 6 武器去相关 + 体检硬门） |
| brain-alpha-research | L1 | 数据集/字段/设置研究（forum 模板 / 13 范式 / news 分类 / WebDataScope 预筛） |
| alpha-template-labs-data-analysis | L0 | Brain Labs 原始数据分析（S0 前研究步骤，MCP labs 工具链） |

> `brain-alpha-robustness` 已于 2026-08-22 迁入 L4 层，2026-08-23 同步到最新版本。
> 注：`code-optimization`、`dead-code-cleanup`、`gold-analysis`、`jin10-news` 为通用非 WQ 元技能，
> 仅由 `~/.workbuddy/skills` 独立维护，**不进入本目录**，避免 WQ 任务中误触发。
> 历史 `.cursor/skills/` 冗余副本已于 2026-08-16 全部移除。
> `wq-brain-campaign-auto`（2026-08-22）与 `brain-deepExplore`（2026-08-24）均已并入 `wq-brain-ra-pipeline`；触发词「一键战役 / auto campaign / 开战役 / 持续挖掘」归 ra-pipeline。
> 本目录同时包含 `pull-brain-skills`、`planning-with-files` 两个元技能，用于 skill 导入与复杂任务规划，与 WQ 技能链共用运行环境约定。

## 挖掘流水线阶段（S-PRE→S6；编排步骤为九步，见 `wq-brain-ra-pipeline`）

| 阶段 | 问题 | 入口 skill | 产出 |
|---|---|---|---|
| S-PRE 战役查表 | 该区域有什么、什么已死、挖到哪了？ | **wq-brain-campaign-matrix**（查 registry_empirical 表三层：静态配置/数据集资产/死路胜绩台账 → 预解析配置包；**不替代 S0 体检**） | region 配置包（universe/中性化/排除族/候选集） |
| S0 情报选题 | 在哪挖？ | **wq-brain-ppa-mining §1.0 体检**（cov≥0.85/alphaCount≤50/fields≥10 三硬门槛，不可跳过；方法定义见 ppa-mining §1.0，执行工具为 toolkit `score_datasets.py`（权威）/ `dataset_health_check.py`（兜底））；brain-next-move-analysis 为**并行情报层**（日报/金字塔分析，非流水线前置，不产出配置） | region+dataset+universe+delay+中性化 白名单 |
| S1 数据理解 | 用什么字段、怎么预处理？ | brain-dataset-exploration-general → brain-datafield-exploration-general → brain-data-feature-engineering | 字段白名单 + 预处理决策（backfill/winsorize/rank/zscore/ts_event_*） |
| S2 表达式生成 | 怎么写成表达式？ | brain-make-some-gem（批量，含增强策略）/ brain-feature-implementation（idea→本地CSV）；alpha-expression-verifier 预检语法 | **`expressions` 表**（status=`gem`/`enhanced`）+ ledger `s2_<ds>_d<delay>_idea` |
| S3 设置仿真 | 怎么合法设置并批量跑？ | brain-inspect-raw-template-create-setting → brain-sim-alphas-in-batch-and-track；并发问题查 wqb-concurrency | alpha_list.json → IS 指标 + status CSV |
| S4 诊断优化 | 为什么不过闸？ | brain-how-to-pass-alpha-test（查阈值）→ wq-brain-alpha-optimization-v1（**两模式**：先 Mode B 想法层，后 Mode A 参数层；prod_corr≥0.7 回 Mode B）→ brain-calculate-alpha-selfcorr-quick（本地快筛 self-corr/PPAC）→ brain-explain-alphas（收益来源归因）→ **过拟合/稳健性闸**（brain-alpha-robustness，S4→S5 必经） | 达标 + 稳健变体 |
| S5 过闸提交 | 能不能提交？ | 廉价闸→PC 等待→硬闸 → `tools/submit_verdict.py`（提交层唯一权威）→ worldquant-submit-alpha（REGULAR）/ wq-brain-superalpha（SUPER）；brain-alpha-judge 仅作 PPA 主题/相关性人工核对清单与 trend score 参考（2026-08-31 起不再承担最终判定） | ACTIVE alpha |
| S6 监控复盘 | 跑得怎么样？ | wq-backtest-monitor（进程枚举/四关审计/ETA + §14 台账回写）；日常由 `wq-brain-ra-pipeline` 步 9 编排 | 复盘报告 + 台账回写 → 反哺 S-PRE |

**toolkit 引擎映射**（战役目录内执行，详见 `wq-brain-campaign-toolkit/SKILL.md`）：
| 阶段 | toolkit 子命令 |
|---|---|
| S1 | scan_fields.py（typed catalog）/ score_datasets.py（评分+探针计划） |
| S2 | 表达式由 `brain-make-some-gem` 生成（`wq-brain-ra-pipeline` 步 4 强制 invoke）；`build_wave.py` 只做去重/分桶/骨架配给；门禁 `gate.py`（8 闸）——步 5 可经 `workflow_execute(node="wave_gate")` 入链 |
| S3 | **七槽填槽模式（wqb-concurrency §8，2026-08-25 更新 5→7，pipeline.py 代码 N=min(7,批数)）**：四重门禁后 7 批 multisim 同提、统一轮询、即收即补；pipeline.py `stage_submit_poll` 已改造为 ThreadPoolExecutor 并行实现（N=min(7, 批数)），支持单轮（默认）与多轮即收即补（`--max-rounds>1`），单批在飞串行已彻底废弃 |
| S4 | review_wave.py（walls 诊断）/ score_datasets.py --probe-score（三灯） |
| S5 | pipeline.py quota（ET 日历日配额闸）<br>**配额是两条独立通道**：`REGULAR_SUBMISSION` 4/日 + `SUPER` 1/日；**PPA 另有独立 `POWER_POOL_SUBMISSION` 1/日**（与 REGULAR 并行、不占其额度）。三者均 00:00 ET 重置。日循环应先提 PPA 那一颗 |
| S6 | diversity_audit.py / campaign.py ledger |

> **健康检查判据分层（设计意图，勿混用）**：S0 体检（ppa-mining §1.0：cov≥0.85 / α≤50 / f≥10）= 开战役**前置硬门槛**（不过不挖）；S1 评分（score_datasets.py 默认线：cov≥0.7 / f≥5 / α≤1000）= 数据集 **tier 分层与白名单筛选**（不过仅降级处理）。S0 严格、S1 宽松，两层判据并存是有意设计。

三角分工：`wq-brain-ra-pipeline`=when/what/怎么挖，`wq-brain-campaign-matrix`=where（查表选区选集），`wq-brain-campaign-toolkit`=how（战役目录内怎么执行）。

## 闸门阶梯（唯一基准表述，两线三层）

> **数字的唯一事实源是 `src/wqb/config.py` 的 `GATES` / `CONCURRENCY`**（2026-08-23 落地）。
> 本节与各 skill 的表述必须与之一致；新增判定逻辑请 `from wqb.config import gate_thresholds`，
> 不要在 skill 文档或脚本中另写一份数字。

**内部严线**（研究仿真阶段即要求，省配额）：
Sharpe>1.58 · Fitness>1.0 · TVR∈[5%,20%] · Margin>10bp · Returns>5% · SELF_CORR<0.50

**平台硬线**（提交阶段必须）：
Sharpe>1.58 · Fitness>1.0 · TVR∈[1%,70%] · Weight/Concentration 达标 · SubUniverse 达标 · SELF_CORRELATION<0.7 · PROD_CORRELATION<0.7

**层级**：① IS 廉价闸 → ② PC 等待 → ③ 硬闸（PROD/SELF）。PASS_CHEAP 只代表过了 ①，绝不等于可提交。

### gate.py 闸编号（权威 = `gate.py` 模块头，2026-09-11 核定）

`wq-brain-campaign-toolkit/scripts/gate.py` 共 **8 闸 + 可选闸0**。文档中出现的"5 闸"一律指闸1–5，
"7 闸"指闸1–7；**不要**再用第三种口径：

| 闸 | 判据 | 开关 |
|---|---|---|
| 闸0 | 语义反模式（恒等式等废品，穿透闸1–8） | `--gate0`（默认关闭） |
| 闸1 | 语法（+ 1b 算子元数/命名参数，catalog 驱动） | 常开 |
| 闸2 | 字段白名单（typed catalog 优先 → legacy 兜底） | 常开（`--dataset`） |
| 闸3 | VECTOR 类型需 `vec_*` 包裹（数据驱动，非正则猜） | 常开 |
| 闸4 | 平台不可访问算子（`ts_min`/`ts_max`）+ `quantile` 元数 | 常开 |
| 闸5 | 毒模式（平台级 `platform_constraints.json` + 区域级生成约束） | 常开 |
| 闸6 | 批级多样性（`check_batch_diversity`，`--skip-diversity-gate` 为逃生阀） | 常开 |
| 闸7 | longCount 真实性（VECTOR 字段实际 longCount < 80 → WARN；小宇宙区域 profile 可升 FAIL） | `--sanity-longcount` |
| 闸8 | EVENT 类型（`type==EVENT` 却未用 `ts_event_*` → FAIL） | `--sanity-event-type` |

> 另有一道**独立的**"体检硬门"（`tools/field_inspect_gate.py`，由 `tools/wave_gate.py` 内置调用），
> 判据是 WebDataScope 字段体检包（低覆盖/高偏度/厚尾/单边/稀疏事件），**与闸7/8 不同源**，勿混谈。

## 分工声明（防触发歧义）

> **toolkit 门禁强制点（2026-09-01 落地）**：MCP `create_multi_simulation` 已内置 toolkit gate 静态门禁
> （语法 + 不可访问算子 + 毒模式，规则复用 toolkit `platform_constraints.json` 与 alpha-expression-verifier）。
> **MCP 直发批 = 也过闸**，不再存在"绕过 toolkit 流程"的通道；被拒批次的修复提示会指向 wave_gate.py / pipeline.py 正规链。

- **wq-brain-alpha-optimization-v1 = 两模式单 skill**（2026-08-15 合并 `brain-improve-alpha-performance` 后已**彻底移除**该目录；本 skill 为唯一改进入口）：
  - **Mode B 想法层**（默认入口，70%）：换信号概念/数据字段组合（arXiv 概念引入、5 步工作流）。
  - **Mode A 参数层**（30%）：同想法下调 decay/窗口/中性化/truncation、8 候选严格本地验证。
- 先想法后参数（70/30 原则）；两者都失败 >10 种结构才转向换数据集。

## 权威版本声明（嵌套副本勿直接调用）

| 副本位置 | 权威版本 |
|---|---|
| brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-data-feature-engineering（520 行旧版，无合法 frontmatter） | 顶层 brain-data-feature-engineering |
| brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-feature-implementation | 顶层 brain-feature-implementation |
| tracking/KOR/scripts\ 下 9 个新链脚本（gate/build_wave/kor_pipeline/score_datasets/review_wave/metrics_cache/scan_fields/diversity_audit/kor_ledger，区域历史实现） | wq-brain-campaign-toolkit/scripts/（战役脚本唯一权威实现，2026-08-15 起） |

嵌套副本是 headless runner 的运行时依赖（`FEATURE_IMPLEMENTATION_DIR` 约定），**不删除、不修改**；新调用一律走顶层权威版。

## 并发口径（演进注记）

- 旧模型：固定槽位 C=5（wqb-concurrency 阶梯实测，2026-07 前）。
- 新模型：**Token-Bucket，突发容量 C≈7、慢补充 ~1 令牌/20–40s**（wq-backtest-monitor §6，2026-08 实测）。
- 配置基准以新模型为准：瞬时提交 ≤6 安全、批间 ≥45s、禁同账号 ≥8 齐射。
- **七槽填槽模式（2026-08-25 更新 5→7，每次挖掘必须执行）**：四重门禁后 7 批 multisim 同提实证安全（连续多波 0 连坐），每轮 7 批×8 条同提→统一轮询→即收即补保持槽位常满，单轮吞吐 ×7；SOP 全文见 `wqb-concurrency` §8。旧"单批在飞串行"模式废弃。

## 命名规范（2026-09-10 已全量统一）

目录名与 frontmatter `name` **一律纯 kebab-case**（小写字母 + 连字符），禁止 camelCase 与下划线。
前缀语义：`brain-*` = 业务/知识技能，`wq-brain-*` = 流程编排，`wqb-*` = 横切工具（并发等）。
正文契约见 `AGENTS.md §Skill 命名规范`。

2026-09-10 审计已把 7 个历史命名**全部改名**（不再保留例外；旧名禁止在任何文档/代码/引用中再出现）：

| 旧名（禁用） | 现名 |
|---|---|
| `pull_BRAINSkill` | `pull-brain-skills` |
| `brain-makeSomeGem` | `brain-make-some-gem` |
| `brain-simAlphasinBatch-and-track` | `brain-sim-alphas-in-batch-and-track` |
| `brain-calculate-alpha-selfcorrQuick` | `brain-calculate-alpha-selfcorr-quick` |
| `brain-how-to-pass-AlphaTest` | `brain-how-to-pass-alpha-test` |
| `brain-inspectRawTemplate-create-Setting` | `brain-inspect-raw-template-create-setting` |
| `brain-nextMove-analysis` | `brain-next-move-analysis` |

> `brain-deepExplore`（2026-08-24 并入）与 `brain-alpha-orchestrator`（2026-08-31 并入）均已不存在，
> 触发词归 `wq-brain-ra-pipeline`。
> 改名配套动作（缺一即断链）：`git mv` 目录 → 全库 grep 替换引用 → 改代码侧硬编码
> （如 `src/wqb/workflow/nodes/gem.py` 的 `resolve_skill_dir("brain-make-some-gem")`）→
> `tools/sync_skills.py` 推送到全部安装位。

`wq-brain-campaign-toolkit` 为该规范下首个**引擎层**（L-TOOL）实例。

## frontmatter 规范（所有 SKILL.md 必须）

```yaml
---
name: <dir-name>                 # 必须与所在目录名一致（tests/unit/test_skill_integrity.py 校验）
description: "..."               # 单行双引号字符串，避免 YAML 块标量解析歧义
layer: <L-RA|L-PRE|L-TOOL|L0|L1|L2|L3|L4|L5|L6|L7>  # 挖掘链条位置，不是优先级、也不是版本号
last_verified: YYYY-MM-DD        # 必需：最近一次对照平台核实内容正确的日期
allowed-tools:                   # 必须是 YAML 列表，禁止写成块标量
  - Read
  - Bash
  - ...
version: "1.0"                   # 可选，内容版本递增用（与 layer 无关）
agent_created: true              # 可选，仅模型创建的技能标注
---
```

必需字段：`name` / `layer` / `description` / `last_verified`；
可选字段：`version` / `user-invocable` / `allowed-tools` / `agent_created` / `hooks`。
禁止出现 `when_to_use` / `trigger_when` / `title` 等非标字段。
权威契约见 `AGENTS.md §SKILL.md frontmatter 契约`。

> `<SKILL_ROOT>` 表示技能库根目录。**真相源 = 仓库 `Claude/skills/`**，各宿主安装位由
> `tools/sync_skills.py` 同步（见文首）。脚本入口一律经 `$WQ_TOOLKIT_DIR` / `$WQ_VALIDATOR_DIR`
> 引用，禁止在 SKILL.md 中写出含用户名的绝对路径。

## 质量门禁

新增或修改 skill 后，必须跑以下两条（2026-09-11 校正：此前的 `validate_skills.py` **本仓库并不存在**，
是悬空引用，已替换为真实门禁）：

```bash
pytest tests/unit/test_skill_integrity.py -q   # name==目录名、frontmatter 完整、registry 元数据与节点签名一致
python tools/sync_skills.py --check            # 仓库与全部安装位零漂移
```

校验内容：
- 每个 `SKILL.md` 存在且 frontmatter 完整（`name`/`layer`/`description`/`last_verified`）。
- `name` 与目录名一致；`layer` 在合法分层列表中。
- `tools/workflow` 节点元数据的 `required_params/optional_params` 与节点 `run()` 签名一致。
- `allowed-tools` 为 YAML 列表格式。
- 无已废弃路径引用（`.workbuddy/skills/` / `.qoder/skills/` / `.cursor/skills/`）。
- skill 内相对 `.py` 引用指向真实存在的文件。

校验不通过（exit 1）时禁止合并/发布。

## 提交配额口径（重要修正，2026-09-01 定案）

提交配额 = **REGULAR 4 颗/ET 日历日 + SUPER 1 颗/ET 日历日**，**00:00 ET（= 12:00 GMT+8）重置**。旧"48h 滚动窗口"口径已证伪（08-12 一次 48h 内提交 6 颗全成功），勿再沿用。

- `get_submission_quota` MCP 工具已于 2026-08-25 移除，**不要依赖它**；其旧返回的 `hours_until_release` 语义本身也有 bug。
- 剩余额度从 submit 响应的 `REGULAR_SUBMISSION` / `SUPER_SUBMISSION` check 的 `value/limit` 读（value 从 0 起计数，limit=4/1）；硬闸 FAIL 的提交**不消耗**配额（status 保持 UNSUBMITTED）。
- 判断"今天 ET 日已用几颗"：拉 `/users/self/activities/submissions`（按日聚合）或本地 DB `alphas.date_submitted`（EDT `-04:00`）按当前 ET 日过滤。
