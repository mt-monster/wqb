# WQ/BRAIN Skills 索引（INDEX）

> 本文件只做**路由与分层**：任务该找哪个 skill、skill 在挖掘链条上的位置、各阶段入口，以及由代码生成的闸表 / 区域表 / 计数表。
> 其余各有归处——**契约**（frontmatter / 职责边界 / 命名 / 共享产物 / 质量门禁）→ [`CONTRACT.md`](CONTRACT.md)；
> **术语、状态词表、「谁说了算」登记表** → [`GLOSSARY.md`](GLOSSARY.md)；**变更历史与迁移记录** → [`CHANGELOG.md`](CHANGELOG.md)；
> **环境变量、开关、凭据来源** → [`docs/env_and_switches.md`](../../docs/env_and_switches.md)；
> **提交链**（否决权威 / 放行权威、可达状态机、不可逆动作块）→ [`worldquant-submit-alpha/references/submit-chain.md`](worldquant-submit-alpha/references/submit-chain.md)。
> **last_verified: 2026-10-04**（索引整体有效性锚点；平台 operator / 阈值 / 区域状态变更后须同步刷新）。修改任何 skill 前先读 CONTRACT；新增 skill 必须归入下述某层并更新本索引。

## 任务 → skill 场景路由表

用户的话往往同时命中好几个 skill 的 description（「提交」命中 submit-alpha / superalpha / judge，「相关性」命中四个）。**先按下表路由，再读该 skill**。

| 用户说 | 首选 | 不选谁（为什么） |
|---|---|---|
| 「在 KOR 开战役 / 一键战役 / 持续挖掘 / 挖 regular 一路跑到可提交」 | `wq-brain-ra-pipeline` | `wq-brain-campaign-toolkit` 只是引擎（何时用、怎么判由 RA 定）；`wq-brain-campaign-matrix` 只查表 |
| 「调 KOR 的回测设置 / 阈值、看 KOR 某类数据集的配方与禁区」 | 区域 skill `wq-brain-ra-<区域小写>`（如 `wq-brain-ra-kor`） | 九步通用正文仍在 `wq-brain-ra-pipeline`；控制值改 `tracking/<R>/config/cells.json` 后重渲（`$WQ_PY -m wqb.profiles render --apply`），不手改生成块 |
| 「日报 / 早报 / 哪个区更值得挖 / 该不该转区」 | `brain-next-move-analysis` | 它只报告不决策：选区决策归 `wqb.region_rotation`，开战役走 RA |
| 「这个区有哪些数据集 / 哪些族已判死 / 挖到哪一步了」 | `wq-brain-campaign-matrix` | 整链挖掘走 RA；选区走 next-move |
| 「审计 / 探索某个数据集」 | `brain-dataset-exploration-general` | 选集是 RA 步 2（S0）；单字段评测走 `brain-datafield-exploration-general` |
| 「这个字段多久更新 / 值域多大 / 能不能当信号」 | `brain-datafield-exploration-general` | 只测不决策，测完交 `brain-data-feature-engineering` |
| 「为黑盒数据集写机制概念 / 想让 GEM 用我写的概念」 | `brain-data-feature-engineering`（人工，`source=manual`） | 节点 `workflow_feature_engineering` 产的是确定性模板、GEM 不注入 |
| 「生成候选表达式 / 跑 GEM / GEM 报 402、no meta.json」 | `brain-make-some-gem`（入口 `workflow_gem`） | `brain-feature-implementation` 只查模板语法，不是入口；外部 / 手写 idea 入库走 `brain-inspect-raw-template-create-setting` |
| 「检查一条表达式语法」 | `alpha-expression-verifier` | 只看语法；字段 / 类型 / 毒化的战役级预检走 toolkit `gate.py` |
| 「批量回测 / 盯回测进度」 | 正式波次 `workflow_batch_track`（RA 步 6）；盯任务与复盘 `wq-backtest-monitor`；手写列表 `brain-sim-alphas-in-batch-and-track` | 回测被 429 / 并发卡住 → `wqb-concurrency` |
| 「这个 alpha 为什么没过 / 怎么改进」 | 查原因 `brain-how-to-pass-alpha-test`（只读）；动手改 `wq-brain-alpha-optimization-v1` | `brain-alpha-repair` 只是被引用的配方索引；解释收益来源用 `brain-explain-alphas` |
| 「相关性怎么办」 | 单个 SELF → MCP `check_self_correlation`；批量 SELF / PPAC → `brain-calculate-alpha-selfcorr-quick`；PROD 墙 → RA 决策表 D0-P；过拟合 / 稳健性 → `brain-alpha-robustness` | 不要为「探 prod」去 `POST /submit`（通过即提交） |
| 「提交 alpha」 | REGULAR → `worldquant-submit-alpha`（先 `submit_verdict`，用户明确确认后）；SUPER → `wq-brain-superalpha`；PPA → 人工交接（`worldquant-submit-alpha/references/ppa-handoff.md`） | `brain-alpha-judge` 只是参考评审：不判可提交、不提交 |
| 「复盘 / 哪些 alpha 可提交 / 提交状态盘点」 | `wq-backtest-monitor`（回写 SOP 只在 RA 步 9） | 它触发并核验回写，不自己定 SOP |
| 「开 PPA 战役 / 这个数据集能不能打 PPA」 | `wq-brain-ppa-mining` | RA 常规战役的白名单排序走决策表 D4，不走它 |
| 「逛论坛 / 论坛里有没有某个做法」 | `brain-forum-browse` | 流水线里的问题驱动检索走 `tools/forum_recon.py` |
| 「导入外部 skill」 | `pull-brain-skills`（只暂存 + 静态审查） | 它不安装、不执行被导入内容 |

## 权威副本与生效方式

- **仓库 `Claude/skills/` = 编辑权威**（git 跟踪、单一可审）：所有新增 / 修改只改这里。
- **各宿主安装位 = 运行时优先**：Agent 实际加载、脚本实际解析的是安装位（`~/.claude/skills`、`~/.codex/skills`、`~/.cursor/skills`、`~/.workbuddy/skills` 等；`~/.qoder-cn/skills` 是指向 `~/.claude/skills` 的 Junction），仓库副本只在解析链**最末**兜底。
- 所以 **改完必须 `$WQ_PY tools/sync_skills.py`（`--check` 断言零漂移）才对 Agent 生效**；一旦漂移，运行时读到的是安装位那份，不是你刚改的那份。流程写在 AGENTS.md「skill 多目标单向同步」。
- 解析顺序以 `src/wqb/workflow/_common.py::_skill_roots()` 为准（`tools/wave_gate.py` 同序）：`WQ_SKILLS_DIR`（脚本级另有 `WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR`）> Claude 安装位 > `~/.claude/skills` > `~/.codex/skills` > 历史 Agent 位 > 仓库 `Claude/skills`（兜底）。
- 已归档 / 废弃的位置（项目内 `_unpacked_*` 扩展区、`cnhkmcp/untracked/skills` 僵尸副本）的处置记录在 CHANGELOG——**禁止调用**。

## 运行环境（全体 skill 共同前置）

所有 Python 命令使用 MCP venv，统一经变量 **`$WQ_PY`** 引用：不硬编码绝对路径、不用系统 Python、**不写裸 `python`**（`tools/skill_lint.py` 的 `bare-python` 棘轮会数）。

**`$WQ_PY` 的定义（单一事实源，按平台取 venv 里的解释器；`<repo>` = 工作区根）**：

| 平台 | 路径 | 在仓库根执行 |
|---|---|---|
| Windows | `<repo>/world-quant-brain-mcp/.venv/Scripts/python.exe` | PowerShell：`$WQ_PY = "$PWD\world-quant-brain-mcp\.venv\Scripts\python.exe"` |
| Linux / macOS / 云端容器 | `<repo>/world-quant-brain-mcp/.venv/bin/python` | bash：`export WQ_PY="$PWD/world-quant-brain-mcp/.venv/bin/python"` |
| **自动探测（跨平台，推荐）** | `tools/_pyenv.py` 依次找 `$WQ_PY`（须是存在的文件）→ `Scripts/python.exe` → `bin/python` → 当前解释器 | bash：`WQ_PY="$(python tools/_pyenv.py)"`；PowerShell：`$WQ_PY = python tools/_pyenv.py` |

换机器或换 venv 路径时，**只改此处定义**。venv 缺依赖时按 `world-quant-brain-mcp/requirements.txt` 装（含 vendored `ace_lib` 需要的 `tqdm` / `Jinja2`）。

**持久化铁律（2026-08-24 全量切库）**：战役**真相源**只走 DB——Agent 持久化用 `mcp__wqb-db__*` 或 `campaign.py` / toolkit 脚本的 `--from-db`；**禁止** `Write` / `Copy-Item` 战役 json / csv 当真相源（`candidates/*.json`、`cache/w*_batches.json`、`cache/gate_wave*.json`、`results/*.csv`、`reviews/*.json`、`final_expressions.json`）。**允许写的文件只有五类**（文档里出现的每个文件路径都须归入其中一类）：

| 类 | 例 | 规则 |
|---|---|---|
| A 真相源 | `data/wqb.db` | 只有 DB；其它文件都不是 |
| B 运行态缓存 | 后台任务 `meta.json` / `stdout.log`、`alpha_simulation_status.csv`、`data/gem_runs/**` | 可读、可丢，**不作交接**；结果同时在 DB |
| C 静态配置与凭证 | `settings.json` / `thresholds.json` / `platform_constraints.json`；本机 `config.json`（gitignore） | 入库（凭证除外）；agent 不读凭证文件 |
| D CLI 临时 `@file.json` | 一次性参数文件 | 放临时目录、用后清理，不入库 |
| E 人读产物 | `reports/`、`planning-with-files` 的 `task_plan.md` / `findings.md` / `progress.md`（仓库根、gitignore）、`WAVE_LEDGER.md` 快照 | 由 DB 生成或纯过程笔记，**不是战役产物**；战役**结果**仍只以 DB 台账为准 |

## 区域清单（权威：`src/wqb/config.py::REGIONS`）

区域集合的唯一事实源是代码常量 `src/wqb/config.py::REGIONS`。下表**由代码生成**（`$WQ_PY tools/index_tables.py regions`：`config.REGIONS` × profile 的 `entry_verdict` × `tracking/<R>/config/` 目录扫描），
`tests/unit/09_core/test_index_tables.py` 逐字比对——**改 profile 或目录后重新生成，不要手改**。此前人写的表有两处与事实不符（DEU 写 `active` 而 profile 是 `probe-only`；AMR 写「无战役目录」而 `tracking/AMR/config/` 存在）。

<!-- region-table:start -->
| region | profile | `tracking/<R>/config/` | `entry_verdict` | 步 1 的行为 |
|---|---|---|---|---|
| AMR | ✓ | ✓ | `active` | — |
| ASI | ✓ | ✓ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile） |
| CHN | ✓ | ✓ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile） |
| DEU | ✓ | ✓ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile） |
| EUR | ✓ | ✓ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile） |
| GBR | ✓ | ✓ | `active` | — |
| GLB | ✓ | ✓ | `active` | — |
| HKG | ✓ | ✓ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile） |
| IND | ✓ | ✓ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile） |
| JPN | ✓ | ✓ | `active` | — |
| KOR | ✓ | ✓ | `active` | — |
| MEA | ✓ | ✓ | `frozen` | 步 1 即拒，不进步 2（后门见 RA `scenarios.md` 情景 RA-08） |
| TWN | ✓ | ✗ | `probe-only` | 只许探针批，不开常规波（探针上限见 profile）；无战役目录：开波前先补 `tracking/TWN/config/{settings,thresholds}.json` |
| USA | ✓ | ✓ | `active` | — | <!-- lint:counterexample: TWN 为 probe-only 区：有 profile 但没有战役目录 -->
<!-- region-table:end -->

- **AMR**：`config.REGIONS` 里有，但**当前不是 RA 挖掘区**；要开必须先补 profile + 实测档位。**ALL** 是平台设置选项里的区域但不在 `config.REGIONS`——同样不是挖掘区。两者的平台侧事实（可用数据集、REGULAR 仿真的报错）是带日期的快照，登记在 [`region-profile-contract.md` §4](wq-brain-ra-pipeline/references/region-profile-contract.md)，不写在本文。
- 缺口清单的机检登记在 `tests/unit/06_wave_pipeline/test_region_alignment.py`（补上一个缺口就必须从登记里删掉）；每个缺口区域在步 1 的行为写在 ra-pipeline 的 [`region-profile-contract.md` §4](wq-brain-ra-pipeline/references/region-profile-contract.md)。
- 有 profile 的区按其 profile 注入静态配置 / 先验 / 闸门覆盖 / 循环策略；`frozen` 区步 1 直接拒绝；`probe-only` 区只许探针批。**新增 / 删除区域**须同步四处：`src/wqb/config.py::REGIONS`、profile 文件、战役目录、（本表随代码重新生成）——逐项做法见下。
- 三者冲突时：`tracking/<R>/config/` json > profile > 本表（本表是导出物，不是来源）。
- **区域 skill**：每区一个 `wq-brain-ra-<区域小写>`（layer `L-RA-R`，14 个），装区域控制面板（回测设置 / 阈值 / Mode B 主闸，每个值带来源）、本区流程差异与「区域 × 类别」组合分支文件。面板和组合文件由 `tracking/<R>/config/cells.json` + profile 生成，`$WQ_PY -m wqb.profiles check` 守一致；组合覆盖只许带证据、数值类锁定项只许收紧（锁定表 `src/wqb/profiles/locked.py`）。

### 开新区检查表（单一来源；matrix / ra-pipeline 只引用本节）

| # | 落点 | 做什么 | 验证 |
|---|---|---|---|
| 1 | `src/wqb/config.py::REGIONS` | 新增 `universes` / `neutralizations` / `delays` / `categories` / `default_universe`；档位用 `mcp__wq-brain-http__get_platform_setting_options` **实测**，禁止照抄 USA | `$WQ_PY -c "from wqb.config import REGIONS; print(sorted(REGIONS))"` |
| 2 | `tracking/<R>/config/` | 建 `settings.json`（仿真设置）+ `thresholds.json`（阈值），契约见 toolkit [`campaign-dir-contract.md`](wq-brain-campaign-toolkit/references/campaign-dir-contract.md)；`region` 必须与目录名一致 | `$WQ_PY Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py --campaign-dir tracking/<R> ledger keys` 不报错 |
| 3 | `wq-brain-ra-pipeline/references/regions/<R>.md` | 写 profile（front-matter 契约见 [`region-profile-contract.md`](wq-brain-ra-pipeline/references/region-profile-contract.md)），含 `entry_verdict` | `$WQ_PY -m pytest tests/unit/06_wave_pipeline/test_region_alignment.py` |
| 4 | 本文「区域清单」表 | `$WQ_PY tools/index_tables.py --apply` 重新生成（不手写） | `$WQ_PY -m pytest tests/unit/09_core/test_index_tables.py` |
| 5 | 首次入库 | `regions` 行在该区首次写入时由 `CampaignStore` 自动建；数据集资产用 `tools/discover_datasets.py` / `tools/ingest_dataset_assets.py`，字段级用 toolkit `scan_fields.py` | `mcp__wqb-db__get_region_config(<R>)` 不再报 `region not found` |
| 6 | 区域 skill 与组合文件 | `$WQ_PY -m wqb.profiles sync-cells --region <R> --apply` → `$WQ_PY -m wqb.profiles render --region <R> --apply` → `$WQ_PY tools/sync_skills.py --apply` | `$WQ_PY -m wqb.profiles check --region <R>`；`$WQ_PY -m pytest tests/unit/09_core/test_profiles_layer.py` |

`tracking/region_config.json` 目前**没有代码读取**（只有 JPN profile 提到过它），不在检查表内。区域相关的**带日期事实**（选项、无 pv1、robust 闸定义、破墙配方）一律写在各区 profile，带 `last_verified`，不写在本文。

## 分层架构（L0–L7）

**编号约定：`Ln ≡ Sn`**（L0 = S0 … L6 = S6，同一阶段的「层」与「阶段」是同一个东西）；`L-RA` / `L-RA-R` / `L-PRE` / `L-TOOL` 是编排层，不属于某一阶段。frontmatter 的 `layer` 用 `Ln`；RA 的「步 N」、gate.py 的「闸 N」、monitor 的「关」是各自的序号，不与 Ln / Sn 混用。

```
L-RA 编排        wq-brain-ra-pipeline（唯一挖掘编排：region→RA 九步 + 日循环/一键战役/PPA 分支）
L-RA-R 区域分支  wq-brain-ra-<区域小写> × 14（区域控制面板 + 区域 × 类别组合分支文件；由 wqb.profiles render 从 cells.json 生成）
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
                 · brain-alpha-robustness（S4→S5 必经闸：结论落台账 `robustness_<alpha_id>`，`submit_verdict` 读取）
                 · brain-alpha-repair（弱候选修复的配方索引；非改进入口，改进入口仍为 optimization-v1）
L5  过闸提交     brain-alpha-judge（仅参考评审） · worldquant-submit-alpha · wq-brain-superalpha
L6  监控复盘     wq-backtest-monitor · brain-dataset-mining-experience（字段/机制经验沉淀与复用）
L7  元技能       pull-brain-skills · planning-with-files
```

## 挖掘流水线阶段（S-PRE→S6；编排步骤为九步，见 `wq-brain-ra-pipeline`）

| 阶段 | 问题 | 入口 skill | 产出 |
|---|---|---|---|
| S-PRE 战役查表 | 该区域有什么、什么已死、挖到哪了？ | **wq-brain-campaign-matrix**（查 registry_empirical 表三层：静态配置 / 数据集资产 / 死路胜绩台账 → 预解析配置包；**不替代 S0 体检**） | region 配置包（universe / 中性化 / 排除族 / 候选集） |
| S0 情报选题 | 在哪挖？ | **S0 体检**（RA：ra-pipeline 决策表 D4 + 步 2，执行器 = `workflow_campaign(stage="S0")` 与 `campaign_intel.py s0-select`；**仅 PPA 战役**另适用 `wq-brain-ppa-mining` 的三硬门槛）；brain-next-move-analysis 是**并行情报层**（日报 / 金字塔分析，非流水线前置，不产配置） | region + dataset + universe + delay + 中性化 白名单 |
| S1 数据理解 | 用什么字段、怎么预处理？ | brain-dataset-exploration-general → brain-datafield-exploration-general → brain-data-feature-engineering | 字段白名单 + 预处理决策（backfill / winsorize / rank / zscore / trade_when 门控；VECTOR 先 `vec_*`，平台没有 `ts_event_*`） |
| S2 表达式生成 | 怎么写成表达式？ | brain-make-some-gem（批量）/ brain-feature-implementation（idea→本地 CSV）；alpha-expression-verifier 预检语法 | **`expressions` 表**（status=`gem` / `enhanced`）+ ledger `s2_<ds>_d<delay>_idea` |
| S3 设置仿真 | 怎么合法设置并批量跑？ | 正式波次 `workflow_batch_track`（RA 步 6）；外部 / 手写 idea 走 brain-inspect-raw-template-create-setting → brain-sim-alphas-in-batch-and-track；并发问题查 wqb-concurrency | **`backtest_results`**（DB）；`alpha_list.json` / status CSV 只是兼容 CLI 的运行态缓存，不是真相源 |
| S4 诊断优化 | 为什么不过闸？ | brain-how-to-pass-alpha-test（查阈值）→ wq-brain-alpha-optimization-v1（Mode B 想法层 → Mode A 参数层；入场资格见其 `references/mode-b-qualification.md`）→ brain-calculate-alpha-selfcorr-quick（本地快筛）→ brain-explain-alphas（收益来源归因）→ **稳健性闸**（brain-alpha-robustness，S4→S5 必经） | 达标 + 稳健变体 |
| S5 过闸提交 | 能不能提交？ | **否决**：资格门 + `tools/submit_verdict.py`（只能拦，不能放）+ prod 实测 + 稳健性闸；**放行**：用户明确确认 + `workflow_submit_alpha(confirm_submit=True)` → worldquant-submit-alpha（REGULAR）/ wq-brain-superalpha（SUPER）/ PPA 人工交接。链条与不可逆动作块见 submit-chain.md；brain-alpha-judge 仅作参考 | ACTIVE alpha |
| S6 监控复盘 | 跑得怎么样？ | wq-backtest-monitor：**日常回写由 RA 步 9 编排**，monitor 只在故障排查 / 盯任务 / 复盘时触发并核验；OS 表现监控与重着色**没有承接者** | 复盘报告 + 台账回写 → 反哺 S-PRE |

**toolkit 引擎映射**（战役目录内执行；子命令细节与并发 / 配额实现细节只在 `wq-brain-campaign-toolkit/SKILL.md` 与 `wqb-concurrency`）：

| 阶段 | toolkit 子命令 |
|---|---|
| S1 | scan_fields.py（typed catalog）/ score_datasets.py（评分 + 探针计划） |
| S2 | `build_wave.py`（去重 / 分桶 / 骨架配给，不产表达式）；门禁 `gate.py` / `tools/wave_gate.py`（步 5 可经 `workflow_execute(node="wave_gate")` 入链） |
| S3 | `pipeline.py`（四重门禁后按槽位并发提交，`--max-rounds` 多轮） |
| S4 | review_wave.py（walls 诊断）/ score_datasets.py --probe-score（三灯） |
| S5 | `pipeline.py quota`（ET 日历日配额闸；配额模型见下「提交配额口径」） |
| S6 | diversity_audit.py / campaign.py ledger / campaign.py dataset-experience（逐数据集中文经验） |

> **健康检查判据分层（设计意图，勿混用）**：S0 体检 = 开战役**前置硬门槛**（不过不挖）；S1 评分线 = 数据集 **tier 分层与白名单筛选**（不过仅降级处理）；**回填带**是 S0 未过但可救的窄带（tier2 保底，生成必须 `ts_backfill` 包裹；覆盖率低于硬地板则 `excluded`）。三层**数字**只在 `config.DATASET_HEALTH_SCORING`、各区 `thresholds.json` 与 ra-pipeline 决策表 D4 / toolkit `probe-scoring-v2.md`，本文不复写。

三角分工：`wq-brain-ra-pipeline` = when / what / 怎么挖，`wq-brain-campaign-matrix` = where（查表选区选集），`wq-brain-campaign-toolkit` = how（战役目录内怎么执行）。

## 闸门阶梯（两线三层）

> **数字的唯一事实源是 `src/wqb/config.py`**（`GATES_INTERNAL` / `GATES_PLATFORM` / `PLATFORM_CHECK_LINES` / `CONCURRENCY` / `WAIT_THRESHOLDS`）。本节与各 skill 的表述必须与之一致；新增判定逻辑请 `from wqb.config import gate_thresholds`，不要在 skill 文档或脚本中另写一份数字。
> **「平台 Sharpe 硬线」不是一个数**：IS Sharpe（`LOW_SHARPE`）与 2Y Sharpe（`LOW_2Y_SHARPE` / `IS_LADDER_SHARPE`）是两条不同的检查，`GATES_PLATFORM.sharpe_min` 取的是后者。下表按**检查名**给平台线 / 内部线 / 来源常量，由 `$WQ_PY tools/index_tables.py ladder` 生成、测试比对。

<!-- gate-ladder:start -->
| 检查 | 平台线（提交必须） | 内部线（研究阶段，省配额） | 来源常量（`src/wqb/config.py`） |
|---|---|---|---|
| IS Sharpe（`LOW_SHARPE`） | Delay-1 > 1.25 / Delay-0 > 2 | > 1.58 | `PLATFORM_CHECK_LINES.low_sharpe_min` / `GATES_INTERNAL.sharpe_min` |
| 2Y Sharpe（`LOW_2Y_SHARPE` / `IS_LADDER_SHARPE`） | > 1.58 | —（内部线已取 1.58） | `PLATFORM_CHECK_LINES.low_2y_sharpe_min`；提交准入线 `GATES_PLATFORM.sharpe_min` 取的就是它 |
| Fitness（`LOW_FITNESS`） | Delay-1 > 1 / Delay-0 > 1.3 | > 1 | `PLATFORM_CHECK_LINES.low_fitness_min` / `GATES_INTERNAL.fitness_min` |
| 换手（`LOW_TURNOVER` / `HIGH_TURNOVER`） | ∈ [1%, 70%] | ∈ [5%, 20%] | `PLATFORM_CHECK_LINES.turnover_range` / `GATES_INTERNAL.turnover_range` |
| Margin | 平台不检 | > 10 bp | `GATES_INTERNAL.margin_bp_min` |
| Returns | 平台不检 | > 5% | `GATES_INTERNAL.returns_min` |
| SELF 相关性 | < 0.7 | < 0.5 | `GATES_PLATFORM.self_corr_max` / `GATES_INTERNAL.self_corr_max` |
| PROD 相关性 | < 0.7 | — | `GATES_PLATFORM.prod_corr_max`（= `PRODCORR_CEILING`） |
<!-- gate-ladder:end -->

**过闸分层**（操作定义在 RA 步 5–8）：① IS 廉价闸 → ② PC 等待 → ③ 硬闸（PROD / SELF）。`PASS_CHEAP` 只代表过了 ①，绝不等于可提交。

### gate.py 闸编号（权威 = `gate.py` 的 `GATE_REGISTRY`，表由代码生成）

`wq-brain-campaign-toolkit/scripts/gate.py` 共 **8 闸 + 可选闸0**（闸 1–8 + 闸0），另有**子闸** 1b / 2b / 2b-2
与**附加闸 9**（窗口，默认 warn）。文档中出现的「5 闸」一律指闸 1–5，「7 闸」指闸 1–7；**不要**再用第三种口径。
下表由 `$WQ_PY Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py --print-gate-table` 生成（唯一注册表 = gate.py 的
`GATE_REGISTRY`），`tests/unit/04_gates/test_gate_registry_docs.py` 比对——**改闸先改注册表，再重新生成本表**：

<!-- gate-table:start -->
| 闸 | 名称 | 性质 | 开关 | 说明 |
|---|---|---|---|---|
| 闸0 | 语义反模式 | block | --gate0（默认关闭） | 恒等式 / 裸字段 / 元数据字段作信号腿（穿透闸 1–8 的废品） |
| 闸1 | 语法 | block | 常开 | alpha-expression-verifier 直调；缺失标 SYNTAX_UNKNOWN |
| 闸1b | 算子元数 + 命名参数 | block | 常开 | op_arity（catalog 驱动）；缺失标 ARITY_UNKNOWN |
| 闸1b-2 | 算子复杂度（调用点数 <10） | block | 常开（MAX_OP_CALLS 可调） | 铁律：表达式内函数调用计数须 <10；与 distinct operator_count 口径不同。实测过平台 Sharpe 线（`config.PLATFORM_CHECK_LINES`）的达标行 0 条触线 |
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

> 另有一道**独立的**「体检硬门」（`tools/field_inspect_gate.py`，由 `tools/wave_gate.py` 内置调用），
> 判据是 WebDataScope 字段体检包（低覆盖 / 高偏度 / 厚尾 / 单边 / 稀疏事件），**与闸 7 / 8 不同源**，勿混谈。

### 闸与逃生口总表（wave_gate 层 + 可豁免的闸）

表由 `$WQ_PY tools/waiver.py gates --markdown` 生成（唯一注册表 = `src/wqb/waiver.py` 的 `GATE_POLICIES`），
`tests/unit/09_core/test_waiver.py` 比对——**改政策先改注册表，再重新生成本表**。用了任一逃生口，`tools/wave_gate.py` 首屏点名，
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
> MCP `create_multi_simulation` 也内置 toolkit 静态门禁（语法 + 不可访问算子 + 毒模式），**MCP 直发批同样过闸**；细则见 toolkit `references/gate-rules.md`。

## MCP 工具/节点计数

其他 skill 一律**引用本段**，禁止裸写计数数字（`test_docs_consistency.py` 守护；历史变更见 CHANGELOG）：

- `wq-brain-http` 服务器：**69 个工具**。统计口径 = 各 `world-quant-brain-mcp/tools_*.py` 顶部 `@mcp.tool` 装饰器计数：
  `tools_account` 13 / `tools_alpha` 8 / `tools_config` 1 / `tools_corr` 3 / `tools_data` 10 / `tools_forum` 4 /
  `tools_labs` 3 / `tools_ops` 5 / `tools_sim` 6 / `tools_spc` 4 / `tools_submit` 0 / `tools_workflow` 12（合计 69）。
  由 `tests/unit/07_docs_skills/test_docs_consistency.py::test_mcp_tool_counts_match_index` 机械守护。
  **`tools_submit` 0 是有意的**：原生 `submit_alpha` 工具已于 2026-09-02 删除，提交统一走 workflow 节点 `workflow_submit_alpha`；
  所以「MCP 里没有 `submit_alpha` 工具」成立，而 `submit_batch` 是**仿真派发**（`POST /simulations`），不是提交。
- `wqb-db` 服务器：**47 个工具**（仓库根 `wqb_db_mcp.py` 的 `@mcp.tool` 装饰器计数，同样由 `test_mcp_tool_counts_match_index` 机械守护；名单引用由 `tests/unit/07_docs_skills/test_skill_integrity.py` 校验守护）。2026-09-30 方案 B 新增 3 个步级评估工具（`record_step_event` / `get_step_events` / `get_step_eval_report`，客观事件台账 + 九步矩阵，与已下线的 6 个旧工具不同名不同契约）。
- workflow 节点：**20 个**（`campaign` / `feature_engineering` / `gem` / `batch_track` / `judge` /
  `submit_alpha` / `superalpha` / `wave_gate` / `hypothesis_round` / `forum_recon` / `forum_recon_wave` / `structural_reconstruct` / `inventory_scan` / `gem_wave` / `unified_gate` / `auto_harvest` / `auto_review` / `auto_pyramid` / `modeb_improve` / `alpha_booster`）。权威 = `src/wqb/workflow/registry.py`，
  `tests/unit/02_workflow/test_workflow.py::test_registry_lists_all_nodes` 守护。

## 分工声明（防触发歧义）

- **wq-brain-alpha-optimization-v1 = 两模式单 skill**（唯一改进入口）：**Mode B 想法层**（换信号概念 / 数据字段组合，含卡闸后的组合腿救援）→ **Mode A 参数层**（冻结核心想法，8 候选严格批调 decay / 窗口 / 中性化 / truncation）。入场资格与模式切换判据以其 `references/mode-b-qualification.md` 为准——此前本节写的「70 / 30」「> 10 种结构才换数据集」是无法度量的口号，已删。
- **`brain-alpha-repair`** 只是被 optimization-v1 与 RA 步 7 引用的**配方索引**（降换手 / 提覆盖 / 降相关的修法与实证），不是改进入口。

## 嵌套副本（GEM 内嵌兜底，勿直接调用）

`brain-make-some-gem/scripts/trailSomeAlphas/skills/` 下的两个目录是 GEM 引擎的「内嵌 legacy 兜底」（`pipeline_paths._resolve_skill_dir`：环境变量 > `skill_roots` 候选 > 内嵌）。**顶层是源、内嵌是派生物**；四条可测纪律：

| # | 纪律 | 守护 |
|---|---|---|
| 1 | 内嵌 `scripts/`（`ace_lib` / `validator` / `implement_idea`）是**硬依赖**，不删除、不单独修改；`validator.py` 与 `alpha-expression-verifier` 权威版四处一起改 | `tests/unit/03_gem/test_gem_skill_paths.py::test_embedded_scripts_are_present_and_validator_is_byte_identical` |
| 2 | 内嵌 `brain-feature-implementation/SKILL.md` 与顶层逐字一致（两份 SKILL.md **正文从不进 LLM prompt**，同步只为不让同名文件互相矛盾） | `test_gem_skill_paths.py`；修复 `$WQ_PY tools/sync_gem_embedded_skill.py --apply` |
| 3 | 内嵌 `brain-data-feature-engineering/` **不得**出现 `SKILL.md`（出现即让解析改选内嵌位、静默屏蔽顶层文档）；其 `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md` 与顶层逐字一致并带 `GENERATED.md` | `test_gem_skill_paths.py` |
| 4 | GEM 产物（`*_ideas.md`、`final_expressions.json`）写 `GEM_REPORT_ROOT` / `WQB_GEM_DATA_ROOT`（缺省仓库 `data/gem_runs/`），不写进 skill 树 | `test_gem_skill_paths.py::test_gem_report_root_is_outside_skill_tree` |

实测二者都解析到安装位 / 仓库顶层，即**内嵌副本平时不生效**。

**待清理（非「权威版本」）**：`tracking/KOR/scripts/` 下的 KOR 专用历史实现（`gate.py` / `build_wave.py` / `metrics_cache.py` / `kor_pipeline_v2.py` 等，已被 toolkit 取代）。其 `README_NEW_TOOLING.md` 记载「是否转薄 wrapper 由用户另行决定」——**这是一个待用户裁定的事项**，本轮没有动它；新战役一律用 `wq-brain-campaign-toolkit/scripts/`（战役脚本的唯一权威实现，2026-08-15 起）。

## 提交配额口径

**单一来源：[`worldquant-submit-alpha/references/quota-and-tower.md`](worldquant-submit-alpha/references/quota-and-tower.md)**（模型、数据来源、复检与撞墙、点塔优选）。
一句话：REGULAR 4 + SUPER 1 + PPA 1 每 ET 日历日，三者并行不互占；日界按 `America/New_York` 计算（GMT+8 是夏令时 12:00 / 冬令时 13:00，**不要写死**）；
当日已提交数用 `$WQ_PY tools/quota_status.py` 的输出为准（列 `stage=OS` 按 `dateSubmitted` 数），**不用** `GET /users/self/activities/submissions`（缺 today 字段）。
