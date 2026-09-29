# WQ/BRAIN Skills 架构索引（INDEX）

> 本文件是全部 WQ/BRAIN skill 的架构基准：分层定位、挖掘流水线入口规则、闸门阶梯、权威版本声明。
> 修改任何 skill 前先读本文件；新增 skill 必须归入下述某层并更新本索引。
> **last_verified: 2026-09-29**（索引整体有效性锚点；平台 operator/阈值/区域状态变更后须同步刷新）。
> **术语、状态词表（alpha / 波 / 区域三层）、跨文档「谁说了算」登记表见 [`GLOSSARY.md`](GLOSSARY.md)**——同一个词只用那里定义的含义；
> 提交链（否决权威 / 放行权威、可达状态机、不可逆动作块）见 [`worldquant-submit-alpha/references/submit-chain.md`](worldquant-submit-alpha/references/submit-chain.md)。
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

`tools/wave_gate.py` 的解析顺序为 `WQ_VALIDATOR_DIR`/`WQ_TOOLKIT_DIR` →
`~/.claude/skills` → `~/.codex/skills` → `~/.qoder-cn/skills` → `~/.cursor/skills` →
`~/.workbuddy/skills` → 仓库 `Claude/skills`（兜底），与 `src/wqb/workflow/_common.py::_skill_roots()` 保持一致。

## 运行环境铁律（全体 skill 共同前置）

所有 Python 命令使用 MCP venv，统一经变量 **`$WQ_PY`** 引用，不要硬编码绝对路径、不要使用系统 Python。

**战役产物持久化铁律（2026-08-24 全量切库）**：Agent 持久化只走 `mcp__wqb-db__*` 或 `campaign.py` / toolkit 脚本的 `--from-db`；**禁止** `Write` / `Copy-Item` 战役 json/csv（`candidates/*.json`、`cache/w*_batches.json`、`cache/gate_wave*.json`、`results/*.csv`、`reviews/*.json`、`final_expressions.json` 当真相源）。静态配置（`settings.json`/`thresholds.json`/`platform_constraints.json`）与凭证、CLI 临时 `@file.json`、BRAIN 原始 CSV 仍用文件。**规划文件**（`planning-with-files` 的 `task_plan.md` / `findings.md` / `progress.md`，仓库根、已 gitignore）是**过程笔记，不是战役产物**，不受本条限制——但战役**结果**仍只以 DB 台账为准。

**`$WQ_PY` 定义（本机单一事实源）：**路径 = `<repo>/world-quant-brain-mcp/.venv/Scripts/python.exe`（`<repo>` = 工作区根；**禁止硬编码绝对盘符路径**，换机即断）。
```bash
# bash / sh（在仓库根执行）
export WQ_PY="$PWD/world-quant-brain-mcp/.venv/Scripts/python.exe"
```
```powershell
# PowerShell（在仓库根执行）
$WQ_PY = "$PWD\world-quant-brain-mcp\.venv\Scripts\python.exe"
```

换机器或换 venv 路径时，**只改此处定义**，全体 skill 文档内的 `$WQ_PY` 引用自动生效。各 skill 正文中出现的 `$WQ_PY` 一律按本定义解析。

## 区域清单（权威：`src/wqb/config.py::REGIONS`）

区域集合的唯一事实源是代码常量 `src/wqb/config.py::REGIONS`（**14 个**）。skill 文档、profile 目录、
战役目录三者必须与下表一致——2026-09-11 审计曾发现"代码 14 / profile 11 / 各处口头清单各异"的三方漂移。

| region | profile<br>`wq-brain-ra-pipeline/references/regions/<R>.md` | 战役目录<br>`tracking/<R>/` | `entry_verdict` | 缺口（步 1 的行为） |
|---|---|---|---|---|
| AMR | ✗ 未建 | 仅 `config/`（`settings.json` / `thresholds.json`），无波产物 | —（`config.REGIONS` 有） | 无 profile：走「处女地模板」（参照 ASI），且**先补 profile** 再开波 |
| ASI | ✓ | ✓ | `probe-only` | — |
| CHN | ✓ | ✓ | `probe-only` | — |
| DEU | ✓（2026-09-11 补） | ✓ | `active` | — |
| EUR | ✓ | ✓ | `active` | — |
| GBR | ✓ | ✓ | `active` | — |
| GLB | ✓ | ✓ | `active` | — |
| HKG | ✓ | ✓ | `probe-only` | — （profile 的 `universe` 已于 2026-09-29 从 `config.REGIONS` 回填；步 1 仍复核） |
| IND | ✓ | ✓ | `active` | — |
| JPN | ✓（2026-09-15 补） | ✓ | `active` | — |
| KOR | ✓ | ✓ | `active` | — |
| MEA | ✓ | ✓ | `frozen` | 步 1 即拒，不进步 2；后门见 ra-pipeline `references/scenarios.md` 情景 RA-08 |
| TWN | ✓ | ✗ 无目录 | `probe-only` | 开波前先补 `tracking/TWN/config/{settings,thresholds}.json` |
| USA | ✓ | ✓ | `active` | — |

缺口清单的机检登记在 `tests/unit/test_region_alignment.py`（补上一个缺口就必须从登记里删掉）；每个缺口区域在步 1 的行为写在 ra-pipeline 的 [`region-profile-contract.md` §4](wq-brain-ra-pipeline/references/region-profile-contract.md)。

规则（与 `wq-brain-ra-pipeline` 步 1 一致）：
- **有 profile 的区**按其 profile 注入静态配置 / 先验 / 闸门覆盖 / 循环策略执行。
- **无 profile 的区**（AMR）走"处女地模板"（参照 ASI profile）；开新区前必须先补 profile + `tracking/<R>/config/`。
- `frozen` 区（MEA）步 1 直接拒绝，不进入步 2。
- 新增/删除区域时必须同步四处：`src/wqb/config.py::REGIONS`、本表、profile 文件、战役目录（逐项做法与验证见下「开新区检查表」）。

### 开新区检查表（单一来源；matrix / ra-pipeline 只引用本节）

| # | 落点 | 做什么 | 验证 |
|---|---|---|---|
| 1 | `src/wqb/config.py::REGIONS` | 新增 `universes` / `neutralizations` / `delays` / `categories` / `default_universe`；档位用 `mcp__wq-brain-http__get_platform_setting_options` **实测**，禁止照抄 USA | `python -c "from wqb.config import REGIONS; print(sorted(REGIONS))"` |
| 2 | `tracking/<R>/config/` | 建 `settings.json`（仿真设置）+ `thresholds.json`（阈值），契约见 toolkit [`campaign-dir-contract.md`](wq-brain-campaign-toolkit/references/campaign-dir-contract.md)；`region` 必须与目录名一致 | `python Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py --campaign-dir tracking/<R> ledger keys` 不报错 |
| 3 | `wq-brain-ra-pipeline/references/regions/<R>.md` | 写 profile（front-matter 契约见 [`region-profile-contract.md`](wq-brain-ra-pipeline/references/region-profile-contract.md)），含 `entry_verdict` | `pytest tests/unit/test_region_alignment.py` |
| 4 | 本文「区域清单」表 | 加一行（profile / 战役目录 / `entry_verdict` / 缺口） | `pytest tests/unit/test_docs_consistency.py` |
| 5 | 首次入库 | `regions` 行在该区首次写入时由 `CampaignStore` 自动建；数据集资产用 `tools/discover_datasets.py` / `tools/ingest_dataset_assets.py`，字段级用 toolkit `scan_fields.py` | `mcp__wqb-db__get_region_config(<R>)` 不再报 `region not found` |

`tracking/region_config.json` 目前**没有代码读取**（只有 JPN profile 提到过它），不在检查表内。

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
                 · brain-alpha-repair（弱候选修复的配方索引与补充实证；非改进入口，改进入口仍为 optimization-v1）
L5  过闸提交     brain-alpha-judge · worldquant-submit-alpha · wq-brain-superalpha
L6  监控复盘     wq-backtest-monitor · brain-dataset-mining-experience（字段/机制经验沉淀与复用）
L7  元技能       pull-brain-skills · planning-with-files
```

## 外部扩展区迁入记录（2026-08-23 完成）

原「外部 Agent Skill 登记」段登记的 4 个 skill 历史上只存在于项目内 `.workbuddy/skills/_unpacked_brain/` 扩展区，
2026-08-23 已全部迁入本权威目录并归层，外部扩展区随项目级副本一并归档：

| name | 迁入层 | 功能 |
|---|---|---|
| ~~brain-alpha-orchestrator~~ | — | 2026-08-31 已并入 `wq-brain-ra-pipeline`（独有硬门已迁移：ghost-op/PPA 门禁、check_batch+check_expr_against_inspect、批次故障协议、failed-count 资格门） |
| brain-alpha-repair | L4 | 弱候选修复的配方索引与补充实证（三类模板 + GLB emotion 实证 + failed-count 判据；非改进入口） |
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
| S0 情报选题 | 在哪挖？ | **wq-brain-ppa-mining §1.0 体检**（cov≥0.85/alphaCount≤50/fields≥10 三硬门槛，不可跳过；方法定义见 ppa-mining §1.0，执行工具为 toolkit `score_datasets.py`（权威）/ `dataset_health_check.py`（兜底，随 ppa-mining 分发于 `wq-brain-ppa-mining/scripts/`））；brain-next-move-analysis 为**并行情报层**（日报/金字塔分析，非流水线前置，不产出配置） | region+dataset+universe+delay+中性化 白名单 |
| S1 数据理解 | 用什么字段、怎么预处理？ | brain-dataset-exploration-general → brain-datafield-exploration-general → brain-data-feature-engineering | 字段白名单 + 预处理决策（backfill/winsorize/rank/zscore/ts_event_*） |
| S2 表达式生成 | 怎么写成表达式？ | brain-make-some-gem（批量，含增强策略）/ brain-feature-implementation（idea→本地CSV）；alpha-expression-verifier 预检语法 | **`expressions` 表**（status=`gem`/`enhanced`）+ ledger `s2_<ds>_d<delay>_idea` |
| S3 设置仿真 | 怎么合法设置并批量跑？ | brain-inspect-raw-template-create-setting → brain-sim-alphas-in-batch-and-track；并发问题查 wqb-concurrency | alpha_list.json → IS 指标 + status CSV |
| S4 诊断优化 | 为什么不过闸？ | brain-how-to-pass-alpha-test（查阈值）→ wq-brain-alpha-optimization-v1（**两模式**：先 Mode B 想法层，后 Mode A 参数层；prod_corr≥0.7 回 Mode B）→ brain-calculate-alpha-selfcorr-quick（本地快筛 self-corr/PPAC）→ brain-explain-alphas（收益来源归因）→ **过拟合/稳健性闸**（brain-alpha-robustness，S4→S5 必经） | 达标 + 稳健变体 |
| S5 过闸提交 | 能不能提交？ | 廉价闸→PC 等待→硬闸 → `tools/submit_verdict.py`（提交层唯一权威）→ worldquant-submit-alpha（REGULAR）/ wq-brain-superalpha（SUPER）；brain-alpha-judge 仅作 PPA 主题/相关性人工核对清单与 trend score 参考（2026-08-31 起不再承担最终判定） | ACTIVE alpha |
| S6 监控复盘 | 跑得怎么样？ | wq-backtest-monitor（进度 / ETA / 提交状态盘点 / 复盘报告；台账回写的 SOP 只在 `wq-brain-ra-pipeline` 步 9，monitor 只触发并核验）；OS 表现监控与重着色**没有承接者** | 复盘报告 + 台账回写 → 反哺 S-PRE |

**toolkit 引擎映射**（战役目录内执行，详见 `wq-brain-campaign-toolkit/SKILL.md`）：
| 阶段 | toolkit 子命令 |
|---|---|
| S1 | scan_fields.py（typed catalog）/ score_datasets.py（评分+探针计划） |
| S2 | 表达式由 `brain-make-some-gem` 生成（`wq-brain-ra-pipeline` 步 4 强制 invoke）；`build_wave.py` 只做去重/分桶/骨架配给；门禁 `gate.py`（8 闸）——步 5 可经 `workflow_execute(node="wave_gate")` 入链 |
| S3 | **七槽填槽模式（wqb-concurrency §8，2026-08-25 更新 5→7，pipeline.py 代码 N=min(7,批数)）**：四重门禁后 7 批 multisim 同提、统一轮询、即收即补；pipeline.py `stage_submit_poll` 已改造为 ThreadPoolExecutor 并行实现（N=min(7, 批数)），支持单轮（默认）与多轮即收即补（`--max-rounds>1`），单批在飞串行已彻底废弃 |
| S4 | review_wave.py（walls 诊断）/ score_datasets.py --probe-score（三灯） |
| S5 | pipeline.py quota（ET 日历日配额闸）<br>**配额是两条独立通道**：`REGULAR_SUBMISSION` 4/日 + `SUPER` 1/日；**PPA 另有独立 `POWER_POOL_SUBMISSION` 1/日**（与 REGULAR 并行、不占其额度）。三者均 00:00 ET 重置。日循环应先提 PPA 那一颗 |
| S6 | diversity_audit.py / campaign.py ledger / campaign.py dataset-experience（逐数据集中文经验） |

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

### gate.py 闸编号（权威 = `gate.py` 的 `GATE_REGISTRY`，表由代码生成）

`wq-brain-campaign-toolkit/scripts/gate.py` 共 **8 闸 + 可选闸0**（闸 1–8 + 闸0），另有**子闸** 1b / 2b / 2b-2
与**附加闸 9**（窗口，默认 warn）。文档中出现的"5 闸"一律指闸1–5，"7 闸"指闸1–7；**不要**再用第三种口径。
下表由 `python wq-brain-campaign-toolkit/scripts/gate.py --print-gate-table` 生成（唯一注册表 = gate.py 的
`GATE_REGISTRY`），`tests/unit/test_gate_registry_docs.py` 比对——**改闸先改注册表，再重新生成本表**：

<!-- gate-table:start -->
| 闸 | 名称 | 性质 | 开关 | 说明 |
|---|---|---|---|---|
| 闸0 | 语义反模式 | block | --gate0（默认关闭） | 恒等式 / 裸字段 / 元数据字段作信号腿（穿透闸 1–8 的废品） |
| 闸1 | 语法 | block | 常开 | alpha-expression-verifier 直调；缺失标 SYNTAX_UNKNOWN |
| 闸1b | 算子元数 + 命名参数 | block | 常开 | op_arity（catalog 驱动）；缺失标 ARITY_UNKNOWN |
| 闸2 | 字段白名单 | block | 常开（--dataset） | typed catalog 优先 → legacy 兜底 |
| 闸2b | 区域非法 group 字段 | block | 常开（platform_constraints.region_invalid_group_fields） | 如 JPN 的 sector/industry/subindustry 是 Invalid data field，整批连坐 |
| 闸2b-2 | 区域不可用字段 + VECTOR 上套 ts_* | block | 常开（region_invalid_fields / region_vector_ts_forbidden） | 如 JPN 无 pv1 字段 |
| 闸3 | 类型 | block | 常开 | VECTOR 需 vec_* 包裹（数据驱动）；MATRIX 禁 vec_* |
| 闸4 | 平台不可访问算子 + quantile 元数 + banned_patterns | block | 常开 | ts_min/ts_max 等（对全部 idents 判定，不是 ops_used） |
| 闸5 | 毒模式 | block | 常开 | 平台级 platform_constraints 正则 + 结构判定（add 加权 / add 等权 / 中缀 + / 跨数据集价差）+ 区域级生成约束 |
| 闸6 | 批级多样性 | block | 常开（--skip-diversity-gate 为逃生阀） | diversity_audit 契约强制；repair 批豁免 |
| 闸7 | longCount 真实性 | warn | --sanity-longcount | VECTOR 字段实际 longCount < 80 → WARN |
| 闸8 | EVENT 类型 | block | --sanity-event-type | 引用 type==EVENT 字段 → FAIL（平台无 ts_event_*；先单条探针） |
| 闸9 | 非标准窗口 | warn | 常开；window_whitelist_enforce=true 升 block（缺省 false） | 白名单 1/5/22/66/252/504/1008/1260；其他窗口须给出解释或实测证据 |
<!-- gate-table:end -->

> 另有一道**独立的**"体检硬门"（`tools/field_inspect_gate.py`，由 `tools/wave_gate.py` 内置调用），
> 判据是 WebDataScope 字段体检包（低覆盖/高偏度/厚尾/单边/稀疏事件），**与闸7/8 不同源**，勿混谈。

### 闸与逃生口总表（wave_gate 层 + 可豁免的闸；X-6）

表由 `python tools/waiver.py gates --markdown` 生成（唯一注册表 = `src/wqb/waiver.py` 的 `GATE_POLICIES`），
`tests/unit/test_waiver.py` 比对——**改政策先改注册表，再重新生成本表**。用了任一逃生口，`tools/wave_gate.py` 首屏点名，
台账须有对应 waiver（AGENTS.md §8.1.2；缺省 warn，`--waiver-mode enforce` 无 waiver 即 exit 2）。

<!-- switch-table:start -->
| 闸 id（waiver 的 gate） | 层 | 判据 | 逃生口 | 缺省 | 日期翻转 | waiver 批准人 / 最长 |
|---|---|---|---|---|---|---|
| `stop_rules` | 开波区域闸（节点一律拦截；CLI 随 gate-mode） | 区域停止规则闸（规则 A / B1 / B2） | `WQB_DISABLE_STOP_RULES_GATE=1（仅测试隔离）` | 常开 | — | user / 30 天 |
| `backlog` | 开波区域闸（节点一律拦截；CLI 随 gate-mode） | 区域积压闸（conversion / pending+gated / 未消费） | `WQB_DISABLE_BACKLOG_GATE=1（仅测试隔离）` | 常开 | — | user / 30 天 |
| `region_gates` | wave_gate / build_wave CLI | 开波区域闸整体降级（catalog / signal_floor / stop_rules / backlog） | `--gate-mode warn\|off`、`WQB_GATE_MODE=warn\|off` | warn 至 2026-10-11，之后 enforce | **2026-10-12**（TB-02） | user / 7 天 |
| `inspect` | wave_gate 内置 | 字段体检硬门（缺体检包） | `--inspect-mode off\|warn`、`WQB_INSPECT_MODE` | warn；新数据集首波自适应 enforce | — | user/agent / 7 天 |
| `semantic` | wave_gate 内置 | 闸 SEM 字段语义归类 | `--skip-semantic-gate`、`--semantic-gate off\|warn`、`WQB_SEM_MODE` | enforce（缺台账 exit 2） | — | user/agent / 7 天 |
| `diversity` | gate.py 闸 6 | gate.py 闸 6 多样性契约 | `--skip-diversity-gate` | 常开（repair / probe 批豁免） | — | user/agent / 3 天 |
| `prod_family` | wave_gate 内置 | 闸 PF 信号族死路预检 | `--no-prod-family-gate` | 开 | — | user/agent / 3 天 |
<!-- switch-table:end -->

> 另：**PROD 饱和闸**（字段热度 + 数据集占比，`tools/wave_gate.py` 内置，常开）无逃生口，enforced 态违规直接拦截。
> **红线**（提交前的用户确认、凭据、平台限额）不可豁免（`wqb.waiver.RED_LINES`）。gate.py 的 `--gate0` / `--sanity-longcount` /
> `--sanity-event-type` / `window_whitelist_enforce` 是**功能开关**（开得越多越严），不是逃生口，见上面的闸表。

### MCP 工具/节点计数（唯一基准，2026-09-12 核定）

其他 skill 一律**引用本段**，禁止裸写计数数字（`test_docs_consistency.py` 守护）：

- `wq-brain-http` 服务器：**69 个工具**。统计口径 = 各 `world-quant-brain-mcp/tools_*.py` 顶部 `@mcp.tool` 装饰器计数：
  `tools_account` 13 / `tools_alpha` 8 / `tools_config` 1 / `tools_corr` 3 / `tools_data` 10 / `tools_forum` 4 /
  `tools_labs` 3 / `tools_ops` 5 / `tools_sim` 6 / `tools_spc` 4 / `tools_submit` 0 / `tools_workflow` 12（合计 69）。
  由 `tests/unit/test_docs_consistency.py::test_mcp_tool_counts_match_index` 机械守护（装饰器数变了测试即红）。
- `wqb-db` 服务器：**44 个工具**（仓库根 `wqb_db_mcp.py` 的 `@mcp.tool` 装饰器计数，同样由
  `test_mcp_tool_counts_match_index` 机械守护；名单引用由 `tests/unit/test_skill_integrity.py` 校验守护）。
  2026-09-15 起含 `set_expression_status`（批量改状态，只传 id/状态过滤，不回传表达式正文）。
  2026-09-16 起含 `workflow_inventory_scan` / `workflow_gem_wave` /
  `workflow_unified_gate` / `workflow_auto_harvest` / `workflow_auto_review` / `workflow_auto_pyramid`。
  2026-09-27（N31）：`harvest_multisim_results` 复位为工具——09-19 起 `@mcp.tool()` 错挂在私有函数
  `_flatten_platform_alpha` 上（该函数随之退出工具表，总数不变）；`workflow_auto_harvest` 带 `alphas` 时同样入库。
  ⚠ **2026-09-26 P2.1 移除 1 个（45→44）**：`workflow_field_understanding` ——
  field_understanding 节点删除（重复的第三套 S1 实现），S1 字段理解走 `feature_engineering`。
  ⚠ **2026-09-18 新增 2 个（43→45）**：`persist_correlation`（相关性检查结果直落 `alphas`，
  NULL-only / [0,1] 校验 / source 溯源）、`get_alpha_corr_metrics`（本地库筛选相关性，
  **零平台配额**）。配套：alphas 表 +9 列（sub_universe_sharpe / returns / drawdown / long_count /
  short_count / concentrated_weight / cluster_test / prod_corr_source / corr_checked_at），
  `CampaignStore.persist_correlation` 为唯一落库入口。
  ⚠ **2026-09-17 移除 6 个（49→43）**：`record_step_metrics` / `get_step_metrics` /
  `compute_wave_summary` / `compute_campaign_summary` / `get_step_gain_report` /
  `workflow_step_metrics` —— step-metrics 子系统整体下线（归档 `attic/step_metrics_20260917/`），
  替代方案 `tools/step_funnel.py`（只读步级漏斗）。
- workflow 节点：**19 个**（`campaign` / `feature_engineering` / `gem` / `batch_track` / `judge` /
  `submit_alpha` / `superalpha` / `wave_gate` / `hypothesis_round` / `forum_recon` / `structural_reconstruct` / `inventory_scan` / `gem_wave` / `unified_gate` / `auto_harvest` / `auto_review` / `auto_pyramid` / `modeb_improve` / `alpha_booster`）。权威 = `src/wqb/workflow/registry.py`，
  `tests/unit/test_workflow.py::test_registry_lists_all_nodes` 守护。
  ⚠ 2026-09-17：`step_metrics` 节点已下线（18→17）；`modeb_improve` 节点上线（17→18）。
  ⚠ 2026-09-18：`alpha_booster` 节点上线（18→19，通用 Alpha 短板提升，S4 增强）。
  ⚠ 2026-09-26 P2.1：`field_understanding` 节点删除（19→18，重复的第三套 S1 实现）；
  同批修复 `auto_pyramid`/`auto_review`/`alpha_booster`/`modeb_improve` 假 dry-run（诚实构建命令/计划）。
  ⚠ 2026-09-28 P4：`forum_recon` 节点上线（18→19，论坛问题驱动只读检索；额度=以查出有效文章为标准），
  由 ra-pipeline 步 4/5/7/9 的 recon 触发点经 `workflow_execute` 调用。

## 2026-09-19 挖掘流程优化落地（RA×10 战役复盘，细节见 wq-brain-ra-pipeline 各步）

- ① **连坐隔离**：`pipeline.py` ERROR 批解析子模拟 → 坏式回写 `expressions.status='fail'` → 无辜兄弟重发一次（`--no-isolate-errors` 关）。
- ② **账户级槽位仲裁**：`_lib/slots.py`（`logs/_slots/` token 文件，`WQB_GLOBAL_SLOTS` 缺省 7，陈旧自动回收），多流水线同跑不再超 C≈7。
- ③ **prod-first 探针**：`tools/campaign_intel.py prod-first --region R --wave W` 收批后族级串行探 prod，STOP 族不扩变体；结果入 `alphas.prod_correlation` + ledger `prod_first_<wave>`。
- ④ **near 池剔除结构性死信号**：`review_wave.is_near/structurally_dead`（robust/limit < `near.robust_min_ratio` 缺省 0.5）；metrics 行新增 `robust_sharpe/robust_limit/sub_universe_sharpe`；停止规则 B 因此真正可触发。
- ⑤ **产出率严格口径**：`get_mining_yield(strict=True)` 默认 `yield_rate=ra_clean/backtested`，另给 `prod_clean/prod_blocked/prod_wall_ratio`；`s0-select` 同源，并新增跨区负先验 / 字段数守卫 / maxS 列。
- ⑥ **GEM 生成侧预闸扩展**：`hump` 命名参数、`bucket` 缺 range 补/丢、区域非法 group 字段（`platform_constraints.json` `region_invalid_group_fields`）、非标窗口别名归一、同骨架换字段封顶（`WQB_GEM_MAX_PER_SKELETON` 缺省 12）。
- ⑦ **闸门**：`gate.py` 闸 2b 区域非法 group 字段 FAIL；validator `bucket()` 必带 range/buckets。
- ⑧ **台账修复**：pipeline 收批写 `backtest_results.dataset`（此前恒 NULL，928 行）；历史空值回填（`backfill_backtest_dataset.py`，只填空）**已一次性跑完并归档到 `tools/legacy/`**（见 `tools/README.md`），不再是可调用入口；`build_wave` 波号残留（全 dropped）时回退源池。

## 2026-09-15 接线修复（审计落地，细节见各 skill）

- ① 设置层先验：`region_kb.gate_priors` 的 decay/neutralization 由 toolkit `pipeline.py run` 直接改写设置（`_lib/region_kb.py`），GEM prompt 只再注入 operator-count / field-family。
- ② GEM：节点/MCP 透传 `pipeline_mode`（runner 缺省 phased，skeleton 可达）；S1 模板渲染文档不再自动注入；落盘前 `pipeline_pregate.py` 归一 `quantile` 默认 driver、丢弃加权混合毒模式。
- ③ 台账：`expressions.dataset`/`backtest_results.dataset` 污染已回填（`tools/backfill_expression_dataset.py`）；pipeline 收批后自动刷新 `region_kb`（recent_waves / gate_priors_local / updated_at）。
- ④ `workflow_campaign(stage="S4")` 先解析本波 alpha_id 再拼 `review_wave.py --alphas`。
- ⑤ `s2_field_pool` 跨主体簇轮转采样，`builder_version` 版本化缓存。
- ⑥ S2-COMPLIANCE 降级为提示；`pipeline.py` 中止路径 rc=2。
- ⑦ `RN_EXPOSURE` 墙进 `review_wave.walls()/passes()`；停止规则 SQL 化（`campaign` 节点 S2/S3 前置，`stop_rules_override` 台账放行）；`wave_results.verdict` 写入强制枚举。

## 分工声明（防触发歧义）

> **toolkit 门禁强制点（2026-09-01 落地）**：MCP `create_multi_simulation` 已内置 toolkit gate 静态门禁
> （语法 + 不可访问算子 + 毒模式，规则复用 toolkit `platform_constraints.json` 与 alpha-expression-verifier）。
> **MCP 直发批 = 也过闸**，不再存在"绕过 toolkit 流程"的通道；被拒批次的修复提示会指向 wave_gate.py / pipeline.py 正规链。

- **wq-brain-alpha-optimization-v1 = 两模式单 skill**（2026-08-15 合并 `brain-improve-alpha-performance` 后已**彻底移除**该目录；本 skill 为唯一改进入口）：
  - **Mode B 想法层**（默认入口，70%）：换信号概念/数据字段组合（arXiv 概念引入、5 步工作流）。
  - **Mode A 参数层**（30%）：同想法下调 decay/窗口/中性化/truncation、8 候选严格本地验证。
- 先想法后参数（70/30 原则）；两者都失败 >10 种结构才转向换数据集。

## 权威版本声明（嵌套副本勿直接调用）

| 副本位置 | 权威版本 | 引擎**实际**用哪份（2026-09-26 实测） |
|---|---|---|
| brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-data-feature-engineering（模板子集；**故意无 SKILL.md**） | 顶层 brain-data-feature-engineering | 顶层/安装位（内嵌因缺 SKILL.md 被解析探针跳过） |
| brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-feature-implementation（`scripts/` 为硬依赖；`SKILL.md` 为自动同步副本） | 顶层 brain-feature-implementation | 顶层/安装位；`SKILL.md` 由 `tools/sync_gem_embedded_skill.py` 同步并由测试守护 |
| tracking/KOR/scripts\ 下 9 个新链脚本（gate/build_wave/kor_pipeline/score_datasets/review_wave/metrics_cache/scan_fields/diversity_audit/kor_ledger，区域历史实现） | wq-brain-campaign-toolkit/scripts/（战役脚本唯一权威实现，2026-08-15 起） | — |

**GEM 内嵌副本的真实角色（2026-09-26 审计重写，旧文请勿再沿用）**：
`pipeline_paths.py::_resolve_skill_dir()` 的解析顺序是 **环境变量（`WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR`）
> `skill_roots` 候选（主安装位优先，仓库 `Claude/skills/` 兜底）> 内嵌 legacy 兜底**。
实测二者都解析到 `~/.claude/skills/...`，即**内嵌副本平时不生效**。

⚠ 旧文称"嵌套副本是运行时依赖，不删除、不修改"——**该结论已被实测推翻**，且它掩盖了一个真缺陷：
内嵌 dfe 目录**连 SKILL.md 都没有**，而 `read_text_optional()` 失败返回**空串**，
导致顶层 322 行的字段工程文档**从未进入 LLM prompt** 且完全静默（现已修）。
故纪律改为：

- 内嵌 `scripts/`（`ace_lib` / `validator`）**是**硬依赖，**不删除、不修改**；
- 内嵌 `brain-feature-implementation/SKILL.md` **必须与顶层逐字一致**（它进 LLM prompt），
  由 `tests/unit/test_gem_skill_paths.py` 守护，修复入口 `tools/sync_gem_embedded_skill.py --apply`；
- 内嵌 dfe **不得**出现 `SKILL.md`（出现即会让解析改选内嵌位、再次静默屏蔽顶层文档，测试会红）；
- GEM 产物（`*_ideas.md`）写 `GEM_REPORT_ROOT`（= 仓库 `data/gem_runs/output_report/`），**不再写进 skill 树**。

## 并发口径（演进注记）

- 旧模型：固定槽位 C=5（wqb-concurrency 阶梯实测，2026-07 前）。
- 新模型：**Token-Bucket，突发容量 C≈7、慢补充 ~1 令牌/20–40s**（参数唯一来源 `config.CONCURRENCY`；参数表与七槽填槽 SOP 见 `wqb-concurrency` §8）。
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
可选字段：`version` / `user-invocable` / `allowed-tools` / `agent_created` / `hooks`（`user-invocable: true` = 该 skill 也可由用户以 `/<skill 名>` 直接调用，而不只是被 agent 按 description 触发；不影响路由与边界。`version` = 外部来源 skill 的**上游版本号**，只登记来源，与本库的 `last_verified` 无关。`hooks` = 在 agent 生命周期事件上自动执行的命令，等价于任意命令执行：只有白名单内的 skill 可声明（`tests/unit/test_skill_hooks_and_tools_guard.py`），且必须在该 skill 正文逐条写明每个钩子做什么与成本，经人工审查后才可加入白名单）。
禁止出现 `when_to_use` / `trigger_when` / `title` 等非标字段。
权威契约见 `AGENTS.md §SKILL.md frontmatter 契约`。

### 正文必备段：`## 职责边界`（2026-09-26 新增，**新 skill 缺此段不予合入**）

frontmatter 只说"我是谁"，**职责边界**才说清"我不管什么、该找谁"。2026-09-26 审计实测
**边界声明覆盖率仅 39%（13/33）**，是选错 skill / 重复实现的主因。所有 SKILL.md 正文必须在
H1 标题之后紧跟该段，格式为**三条**：

```markdown
## 职责边界

- **本 skill 负责**：<产物 / 动作>
- **本 skill 不做**：<明确排除>（遇到 → 转 <skill 或工具>）
- **上游 / 下游**：上游 = <谁给我>；下游 = <我给谁>
```

由 `tests/unit/test_skill_boundaries.py` 机械守护（缺段 / 缺条目即红）。

**两条硬裁定（写入边界段时须遵守）**：

1. **skill 不得改写权威常量**。`src/wqb/config.py` 的 `REGIONS` / `REGION_PRIORITY` /
   `GATES` / `CONCURRENCY` / `PARADIGMS` / `SHAPE_CLASSES` 是唯一权威；skill 只能**引用**，
   **禁止**用"修正为…" / "撤回…" / "实测推翻…"等口吻改写。若 skill 的实证观测与常量冲突，
   **保留观测但显式标注冲突并裁定以 config 为准**（样板见 `brain-alpha-research` §12(a)）。
2. **同一产物只能有一个主写方**。DB 表 / 产物文件若被多个 skill 提及，边界段必须写明
   「唯一正式写入方 = X；Y 仅在 <场景> 作逃生阀」（样板见 RA `step9-writeback.md` §9.4 与
   `brain-sim-alphas-in-batch-and-track` 对 `wave_results` 的约定）。

### 共享产物归属表（2026-09-27 补）

> 背景：硬裁定②此前**实质覆盖率仅 1/33**（全库只有 `campaign-toolkit` 一处写明），
> 「谁写 / 谁读」没人写清 → 直接导致两起事故：① `priors_snapshot` 无人认领刷新责任，
> GBR 快照落后 KB 源 8 天；② `wave_gate` 三方调用无主写方，自动链 100% `TypeError`。
> 下表是**共享产物的最小权威清单**；新增共享产物必须同步此表。

| 产物 | 唯一正式写入方 | 只读消费方 | 刷新 / 失效责任 | 逃生阀 |
|---|---|---|---|---|
| `wave_results` | **`wqb.wave_results_contract.upsert_wave_result`（唯一写入函数：verdict 枚举归一 / 合并语义 / closed 须带 verdict）**；入口两个且等价——MCP `upsert_wave_result`、toolkit `campaign.py wave upsert`，都走这个函数 | ra-pipeline 步 9、`wq-backtest-monitor`（只读核验） | 波级收尾由 S6 回写（顺序与契约见 RA `step9-writeback.md`） | —（有 MCP 用 MCP，无 MCP 用 CLI；不要两边各写一遍） |
| `registry_empirical` | toolkit `campaign.py registry` / `upsert_registry_empirical` | ra-pipeline 步 1–2、`wq-brain-campaign-matrix` | 每波 S6 回写 win/dead | 会话内轻量 `upsert_registry_empirical`（战役目录内仍走 CLI 以保必填校验） |
| `ledger_kv` | toolkit ledger 子命令 | ra-pipeline 各步、`brain-*` 只读 | 按 key 定；`s0_whitelist` 有契约归一（replace/merge 双侧 canonicalize） | 会话内 `upsert_ledger_key` |
| `expressions` | `brain-make-some-gem`（S2 生成） | 门禁闸、S3 回测 | 状态推进走 `set_expression_status` | — |
| `field_catalog` | S1 `scan_fields` → `upsert_field_catalog` | 门禁闸 2 字段白名单、GEM（**只读**；已存在则跳过概念化） | 换数据集 / 换 delay 时重建 | — |
| **`priors_snapshot_<region>`** | **`workflow_campaign(stage=S2, subcommand=assemble-priors)`（唯一）** | **`brain-make-some-gem`（只读，禁止回写）** | **S6 复盘回写后必须重跑**（默认带 `--snapshot-ledger`）；否则下一波 GEM 读旧先验 | 无。GEM 侧发现 stale 仅 WARN，**不得据此继续实跑**（2026-09-27 GBR 实证落后 8 天） |
| `submit_ready` | ra-pipeline 步 7→8（`upsert_ledger_key`） | 步 8 提交判定、`super_build.py` | 每次 prod 复检后刷新（库内值会过期，提交前必须实测） | — |

> `<SKILL_ROOT>` 表示技能库根目录。**真相源 = 仓库 `Claude/skills/`**，各宿主安装位由
> `tools/sync_skills.py` 同步（见文首）。脚本入口一律经 `$WQ_TOOLKIT_DIR` / `$WQ_VALIDATOR_DIR`
> 引用，禁止在 SKILL.md 中写出含用户名的绝对路径。

## 质量门禁

新增或修改 skill 后，必须跑以下两条（2026-09-11 校正：此前的 `validate_skills.py` **本仓库并不存在**，
是悬空引用，已替换为真实门禁）：

```bash
pytest tests/unit/test_skill_integrity.py -q   # name==目录名、frontmatter 完整、registry 元数据与节点签名一致
pytest tests/unit/test_skill_boundaries.py -q  # 2026-09-26 新增：职责边界段存在且完整、L5 执行权互斥已声明
python tools/sync_skills.py --check            # 仓库与全部安装位零漂移
```

校验内容：
- 每个 `SKILL.md` 存在且 frontmatter 完整（`name`/`layer`/`description`/`last_verified`）。
- `name` 与目录名一致；`layer` 在合法分层列表中。
- **每个 `SKILL.md` 正文含 `## 职责边界` 段，且具备「本 skill 负责 / 不做 / 上游·下游」三条**
  （2026-09-26 新增；`test_skill_boundaries.py` 守护，缺段即红）。
- `tools/workflow` 节点元数据的 `required_params/optional_params` 与节点 `run()` 签名一致。
- `allowed-tools` 为 YAML 列表格式。
- 无已废弃路径引用（`.workbuddy/skills/` / `.qoder/skills/` / `.cursor/skills/`）。
- skill 内相对 `.py` 引用指向真实存在的文件。

校验不通过（exit 1）时禁止合并/发布。

## 提交配额口径

**单一来源：[`worldquant-submit-alpha/references/quota-and-tower.md`](worldquant-submit-alpha/references/quota-and-tower.md)**（模型、数据来源、复检与撞墙、点塔优选）。
一句话：**REGULAR 4 + SUPER 1 + PPA 1 每 ET 日历日**（三者并行不互占），00:00 ET 重置，换算 GMT+8 为夏令时 12:00 / 冬令时 13:00（以 `python tools/quota_status.py`
输出为准）；当日已提交数用 `quota_status.py`（列 `stage=OS` 按 `dateSubmitted` 数），**不用** `GET /users/self/activities/submissions`（缺 today 字段）。

## 2026-09-19 平台区域硬事实（当日实测，优先级高于任何旧记）

- `get_platform_setting_options` 现含区域 **ALL**（D1，LARGE/MEDIUM/SMALL）与 **AMR**（TOP600）。**ALL 不能跑 REGULAR**（平台 400 "Region ALL is not available for simulation type REGULAR"）；AMR 只有 sentiment7 + univ1，无 pv1。两者都不是 RA 挖掘区。
- **JPN/TOP1600/D1 无 pv1**（close/adv20/returns 全部 Invalid data field），且 `ts_*(vec_*(VECTOR))` 必 ERROR；GEM 预闸与闸 2b 已按 `region_invalid_fields` / `vector_ts_forbidden` 处理。
- **IND robust 闸 = 流动性子集重跑 Sharpe ≥ 1.0**（官方 India Alphas 页）；日内反转族（尾盘一小时、价量相关）IS 4–6 但 prod 0.79–1.0 撞墙；破 robust 墙的配方是自归一化（ts_zscore / 相对 252 日均值偏离）+ 市值十分位 group_rank + decay 7–10（pwRJmvP3 ACTIVE 实证）。
- **prod 竞速**：prod 0.60–0.70 的候选必须当天提交（pv103 一小时内被外部同款堵成 1.0）。
