# 环境变量与开关目录

> 回答两类问题：「某个行为怎么开 / 关？」「这个变量谁读、缺省多少？」。skills 审查 IX-13（此前这些只散落在 INDEX 的变更日志里，
> 想找「怎么关连坐隔离」只能读历史条目）。
>
> - §2 的表由 `python tools/index_tables.py env` **生成**（缺省值与读取方来自代码扫描，用途来自 [`env_registry.json`](env_registry.json)）；
>   `tests/unit/09_core/test_index_tables.py` 守护：**代码里读取的每个变量必须登记，登记的每个变量必须仍被读取**。加变量 = 改 `env_registry.json` → `python tools/index_tables.py --apply`。
> - 闸与逃生口的**政策**（waiver、日期翻转、谁批准）不在这里，见 [`Claude/skills/INDEX.md`](../Claude/skills/INDEX.md)「闸与逃生口总表」。
> - **凭据类变量只登记名字与来源。任何文档、日志、回报都不得出现值；agent 不读 `.env` / `config.json`**（AGENTS.md 安全约束）。

## 1. 凭据来源与外发通道登记（skills 审查 T0-15 / X-9）

全库曾有 ≥ 8 种凭据来源、变量名互不相同。**标准名 = `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`**（MCP 服务、toolkit、feature-implementation、judge、GEM、sim-alphas 都认）；
其余是旧别名，只为兼容。新增消费者必须先认标准名，并在下表登记。

| 消费者 | 来源顺序（先者优先） | 会不会把凭据落盘 | 备注 |
|---|---|---|---|
| MCP 服务 `wq-brain-http`（`brain_config.py`） | 配置文件（`MCP_CONFIG_FILE`，缺省 `~/.brain_mcp_config.json`）→ **被**环境变量 `CREDENTIALS_*` 覆盖；`world-quant-brain-mcp/.env` 经 python-dotenv 载入环境（`override=False`） | 否 | `.env` 由**服务进程**读，agent 不读 |
| toolkit（`_lib/common.py`） | `CREDENTIALS_*` → `WQ_USERNAME` / `WQ_PASSWORD` → `BRAIN_CREDENTIALS` 文件（缺省 `~/.brain_credentials`）→ `MCP_CONFIG_FILE` → MCP `.env` | 否 | workflow 节点把标准名桥接成 `WQ_*` |
| GEM runner（`headless_runner/run.py`） | 环境（`CREDENTIALS_*` → `BRAIN_USERNAME` / `BRAIN_EMAIL` / `BRAIN_PASSWORD`）→ `scripts/headless_runner/config.json`（用户自建、gitignore、不参与 sync） | 否 | 启动只打印**来源**；缺键只报键名 |
| sim-alphas `batch_simulator.py` | 环境（`CREDENTIALS_*` → 旧别名 → `BRAIN_CREDENTIAL_*`）→ `configs/config.json`（gitignore）→ MCP `.env` | **否**（已覆盖 `ace_lib.get_credentials`） | 此前 `config.json` 排在环境变量之前；vendored `ace_lib` 默认会把口令**明文写进** `~/secrets/platform-brain.json` |
| feature-implementation `fetch_dataset.py` | 环境（`CREDENTIALS_*` → 旧别名）→ skill 根 `config.json`（仅环境不全时才需要） | 否（覆盖 `ace_lib.get_credentials`） | 不回显邮箱 |
| judge `load_credentials.py` | **只读进程环境**（`CREDENTIALS_*` → 旧别名） | 否 | 发现 `configs/config.json` / `~/secrets/platform-brain.json` 里有明文只在 stderr 提示迁移，不读、不打值 |
| selfcorr-quick `skill.py` | 环境（`CREDENTIALS_*` → `BRAIN_USERNAME` / `BRAIN_PASSWORD`）；命令行 `--password` 仍可用但告警 | 否 | 产物落固定目录（`WQ_SELFCORR_OUT_DIR`），不落 CWD |
| inspect-raw `load_credentials.py` | 环境（`CREDENTIALS_*` 优先）→ 旧别名 | 否 | 测试钉死「标准名优先」 |
| `tools/fetch_all_universes.py` | `CREDENTIALS_*` → `WQ_USERNAME` / `WQ_PASSWORD`；`.env` 路径 `WQ_ENV_PATH` | 否 | 一次性运维脚本 |
| `tools/forum_recon.py`（HTTP 实现复用 `forum_research.py`；论坛只读检索） | 进程环境 `CREDENTIALS_*` → MCP `world-quant-brain-mcp/.env`（`forum_research.load_creds` 的路径约定） | 否 | 缺凭据 = **工具故障**（记 `forum_recon_error_<qkey>`，不是「论坛无解」）；不打印、不记录值 |

**外发通道**（凭据之外，另一类泄露面——把研究资产发给第三方）：

| 通道 | 发什么 | 缺省 | 出处 |
|---|---|---|---|
| GEM → Moonshot（密钥 `MOONSHOT_API_KEY`） | GEM prompt：字段 id / 描述、priors（win / dead_end 摘要）、算子清单 | 开（这是 GEM 的本职；给 `ideas_file` 则完全不调） | `brain-make-some-gem` SKILL「前置：LLM 通道」 |
| judge → LLM | 候选的指标摘要；表达式原文默认**不**发（`judge.llm.send_expression=true` 才发） | **关**（`judge.llm.enabled=true` 且设了 `BRAIN_JUDGE_LLM_API_KEY` 才启用；LLM 只能收紧判定，不能放行） | `brain-alpha-judge` SKILL |
| arXiv 概念抽取 → 第三方 LLM | 公开论文摘要（**不**含候选表达式） | 关（`--llm` 才发；密钥 `OPENAI_API_KEY` 或 `scripts/.arxiv_llm.env`） | `wq-brain-alpha-optimization-v1` `arxiv_api.py` |
| 论坛 / 论文检索 | 查询词 | 开（只读） | `brain-forum-browse` / `tools/forum_recon.py` |

## 2. 变量目录（生成）

缺省列是代码里第一处字面量默认值（`—` = 没有默认或默认不是字面量）；「读取方」只列前两处，`+N` 是其余数量。

<!-- env-table:start -->
#### 凭据与外发通道（只登记名字与来源；任何文档 / 日志 / 回报都不得出现值）

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `BRAIN_CREDENTIALS` | — | toolkit `_lib/common.py`：凭据**文件**路径（缺省 `~/.brain_credentials`，JSON 列表 / 对象）——只放本机、不入库 | `wq-brain-campaign-toolkit/scripts/_lib/common.py` | — |
| `BRAIN_CREDENTIAL_EMAIL` | — | vendored `ace_lib.get_credentials()` 读的邮箱（sim-alphas / feature-implementation / inspect-raw 共用的那份库）。**注意**：该库在 `~/secrets/platform-brain.json` 不存在时会把它**明文写盘**——调用方必须覆盖 `ace_lib.get_credentials`（sim-alphas 的 `batch_simulator`、GEM、`fetch_dataset` 都已覆盖） | `brain-feature-implementation/scripts/ace_lib.py` · `brain-inspect-raw-template-create-setting/ace_lib.py` · +4 | — |
| `BRAIN_CREDENTIAL_PASSWORD` | — | vendored `ace_lib.get_credentials()` 读的口令（同上） | `brain-feature-implementation/scripts/ace_lib.py` · `brain-inspect-raw-template-create-setting/ace_lib.py` · +4 | — |
| `BRAIN_EMAIL` | — | 旧别名（BRAIN 邮箱）；同时是 GEM runner / sim-alphas 传给下游子进程的**内部变量**（runner 自己写它）。新代码用 `CREDENTIALS_EMAIL` | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-feature-implementation/scripts/fetch_dataset.py` · +7 | — |
| `BRAIN_JUDGE_LLM_API_KEY` | — | judge `llm_judge.py` 的 LLM 通道密钥（缺省不启用；启用即外发候选字段——见 judge SKILL 的外发边界） | `brain-alpha-judge/scripts/vendor/llm_judge.py` | — |
| `BRAIN_PASSWORD` | — | 旧别名（BRAIN 口令）；同时是 GEM runner / sim-alphas 传给下游子进程的内部变量。新代码用 `CREDENTIALS_PASSWORD` | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-calculate-alpha-selfcorr-quick/scripts/skill.py` · +10 | — |
| `BRAIN_USERNAME` | — | 旧别名（BRAIN 邮箱）：judge 的 `load_credentials`、feature-implementation、GEM runner 兜底。新代码用 `CREDENTIALS_EMAIL` | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-calculate-alpha-selfcorr-quick/scripts/skill.py` · +8 | — |
| `CREDENTIALS_EMAIL` | — | BRAIN 账号邮箱——**标准名**：MCP 服务 / toolkit / feature-implementation / judge / GEM runner 共用，优先于下面的旧别名 | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-calculate-alpha-selfcorr-quick/scripts/skill.py` · +16 | — |
| `CREDENTIALS_PASSWORD` | — | BRAIN 账号口令——标准名（同上） | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-calculate-alpha-selfcorr-quick/scripts/skill.py` · +16 | — |
| `MCP_CONFIG_FILE` | — | toolkit / `tools/lib/api_client.py`：`~/.brain_mcp_config.json` 路径覆盖（凭据来源之一） | `wq-brain-campaign-toolkit/scripts/_lib/common.py` · `tools/lib/api_client.py` · +1 | — |
| `MOONSHOT_API_KEY` | — | GEM 的 LLM 通道密钥（优先于 `config.json` 的 `moonshot_api_key`；给了 `ideas_file` 就不需要） | `brain-make-some-gem/scripts/headless_runner/run.py` · `brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py` · +1 | — |
| `MOONSHOT_BASE_URL` | `https://api.moonshot.cn/v1` | GEM 的 LLM 端点（runner 从 `config.json` 的 `moonshot_base_url` 写入） | `brain-make-some-gem/scripts/headless_runner/run.py` · `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_llm.py` | — |
| `MOONSHOT_RETRIES` | `3` | GEM LLM 调用的重试次数（runner 缺省 3，`pipeline_llm` 缺省 2）；401 / 402 / 403 不重试 | `brain-make-some-gem/scripts/headless_runner/run.py` · `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_llm.py` | — |
| `MOONSHOT_RETRY_BACKOFF` | `2` | GEM LLM 重试的退避秒数 | `brain-make-some-gem/scripts/headless_runner/run.py` · `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_llm.py` | — |
| `OPENAI_API_KEY` | — | optimization-v1 `concept_extract.py`（arXiv 概念抽取）的 LLM 密钥；也读 `scripts/.arxiv_llm.env` / `.env`（gitignore、不参与 sync）。会外发论文文本，**不**外发候选表达式 | `wq-brain-alpha-optimization-v1/scripts/concept_extract.py` · `tests/unit/02_workflow/test_judge_never_submits.py` | — |
| `OPENAI_BASE_URL` | — | 同上：LLM 端点（缺省 DeepSeek 兼容端点） | `wq-brain-alpha-optimization-v1/scripts/concept_extract.py` | — |
| `OPENAI_MODEL` | — | 同上：LLM 模型名 | `wq-brain-alpha-optimization-v1/scripts/concept_extract.py` | — |
| `WQ_ENV_PATH` | — | `tools/fetch_all_universes.py`：MCP `.env` 路径（缺省 `world-quant-brain-mcp/.env`）；agent 不读该文件 | `tools/fetch_all_universes.py` | — |
| `WQ_PASSWORD` | — | toolkit 传统别名（口令）：同上 | `wq-brain-campaign-toolkit/scripts/_lib/common.py` · `src/wqb/workflow/_common.py` · +1 | — |
| `WQ_USERNAME` | — | toolkit 传统别名（邮箱）：`_lib/common.py`、`tools/fetch_all_universes.py` 兜底；workflow 节点会把标准名桥接成它 | `wq-brain-campaign-toolkit/scripts/_lib/common.py` · `src/wqb/workflow/_common.py` · +1 | — |

#### 路径与根

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `BRAIN_API_URL` | `https://api.worldquantbrain.com` | 平台 API 根（judge / helpful_functions / ace_lib 读；测试环境可改指别处） | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-feature-implementation/scripts/ace_lib.py` · +8 | — |
| `BRAIN_URL` | `https://platform.worldquantbrain.com` | 平台网页根（拼 alpha 链接用；judge / helpful_functions 读） | `brain-alpha-judge/scripts/vendor/load_credentials.py` · `brain-feature-implementation/scripts/helpful_functions.py` · +4 | — |
| `WQB_ALLOW_REAL_DB` | — | `=1` 允许测试运行中 wqb-db 连生产 `data/wqb.db`（默认拒绝：2026-10-04 隔离 patch 静默失效导致测试写生产库后加的**结果层硬闸**，见 `wqb_db_mcp._reject_production_db_under_tests`）。只给确实要读真库的存量体检测试用，必须在测试里写明理由 | `tests/unit/07_docs_skills/test_audit_fixes.py` · `wqb_db_mcp.py` | — |
| `WQB_CAMPAIGN_DIR` | — | workflow 节点使用的战役目录覆盖 | `src/wqb/workflow/_common.py` · `tests/unit/01_store_db/test_n30_wave_results_writers.py` · +3 | — |
| `WQB_DBLOCK_DIR` | — | DB 写锁文件目录（缺省在仓库根下） | `wq-brain-campaign-toolkit/scripts/_lib/dblock.py` · `src/wqb/db_write_lock.py` · +2 | — |
| `WQB_DB_PATH` | — | `data/wqb.db` 路径覆盖（`wqb.db_conn` 单点解析，其余入口都经它） | `brain-data-feature-engineering/scripts/feature_engineering.py` · `brain-inspect-raw-template-create-setting/scripts/_workspace.py` · +46 | — |
| `WQB_GEM_DATA_ROOT` | — | GEM 产物根（缺省 `data/gem_runs`；`final_expressions.json` 与 `output_report/` 都在其下） | `brain-feature-implementation/scripts/fetch_dataset.py` · `brain-feature-implementation/scripts/implement_idea.py` · +9 | — |
| `WQB_ROOT` | — | 工作区根覆盖（各脚本的仓库根缺省由文件相对位置推导；只有脚本被复制到别处运行时才需要设） | `brain-data-feature-engineering/scripts/feature_engineering.py` · `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_kb.py` · +20 | — |
| `WQB_SLOTS_DIR` | — | 账户级槽位 token 目录（缺省 `logs/_slots`） | `wq-brain-campaign-toolkit/scripts/_lib/slots.py` · `tests/unit/10_toolkit_scripts/test_slots_arbitration.py` | — |
| `WQB_TASK_ROOT` | — | 后台任务目录（缺省 `logs/_async_tasks`；`workflow_task_status` 读它） | `src/wqb/workflow/_common.py` · `tests/unit/02_workflow/test_mining_efficiency_guards.py` · +4 | — |
| `WQB_WORKSPACE` | — | 工作区根覆盖（同 `WQB_ROOT`，wave_gate / GEM 等按各自的解析顺序取用） | `brain-data-feature-engineering/scripts/feature_engineering.py` · `brain-make-some-gem/scripts/headless_runner/run.py` · +9 | — |
| `WQB_WORKSPACE_ROOT` | — | 工作区根覆盖（同 `WQB_ROOT`，toolkit 的 gate / pipeline 用） | `wq-brain-campaign-toolkit/scripts/gate.py` · `wq-brain-campaign-toolkit/scripts/pipeline.py` · +3 | — |
| `WQ_PROJECT_ROOT` | — | 工作区根覆盖（同 `WQB_ROOT`，GEM 的 pipeline_kb 等用） | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_kb.py` · `brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py` · +12 | — |
| `WQ_SELFCORR_OUT_DIR` | — | selfcorr-quick 的产物目录（缺省 `data/selfcorr_quick`） | `brain-calculate-alpha-selfcorr-quick/scripts/skill.py` · `tests/unit/05_submit_quota/test_selfcorr_quick_script.py` | — |

#### 解释器与 skill / 工具目录

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `BRAIN_VALID_OP_PATH` | — | validator 读的算子清单 JSON 路径覆盖 | `alpha-expression-verifier/scripts/validator.py` · `brain-feature-implementation/scripts/validator.py` · +2 | — |
| `WQB_OPERATORS_CATALOG` | — | `op_arity` 读的算子目录路径覆盖（缺省按 `docs/reference` → `data/` → `research-data/` 顺序找） | `src/wqb/expression/op_arity.py` | — |
| `WQB_SCRIPTS` | — | 仓库外自建脚本目录覆盖（缺省 `~/wqb-scripts`）；`tools/preflight_wave.py` 用它拼 `wqb_tools.py` CLI 路径，以免在源码里写死盘符绝对路径（S4 守卫） | `tools/preflight_wave.py` | — |
| `WQB_TOOLS_LIB` | — | GEM 引擎找 `tools/lib`（`vector_wrap.py` 所在）的覆盖 | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_paths.py` · `wq-brain-campaign-toolkit/scripts/build_wave.py` · +1 | — |
| `WQ_MCP_DIR` | — | MCP 目录覆盖（缺省 `<仓库根>/world-quant-brain-mcp`） | `tests/unit/09_core/test_pyenv.py` · `tools/_pyenv.py` · +6 | — |
| `WQ_PY` | — | MCP venv 解释器覆盖（`tools/_pyenv.py`、workflow 节点子进程）；文档里的 `$WQ_PY` 就是它 | `src/wqb/workflow/_common.py` · `tests/unit/09_core/test_pyenv.py` · +4 | — |
| `WQ_RA_PIPELINE_DIR` | — | GEM `skeletons.py` 找 RA skill 目录的覆盖 | `brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py` · `wq-brain-campaign-toolkit/scripts/assemble_priors.py` | — |
| `WQ_ROBUSTNESS_SKILL_DIR` | — | `tools/forum_cache_builder.py` 找 robustness skill 目录的覆盖 | `tests/unit/08_forum_recon/test_forum_cache_builder_paths.py` · `tools/forum_cache_builder.py` | — |
| `WQ_SKILLS_DIR` | — | skill 根覆盖（解析顺序首位；测试也用它指定被守护的 skills 目录） | `brain-make-some-gem/scripts/trailSomeAlphas/skill_roots.py` · `wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py` · +2 | — |
| `WQ_TOOLKIT_DIR` | — | toolkit `scripts/` 目录覆盖 | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_kb.py` · `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_pregate.py` · +6 | — |
| `WQ_VALIDATOR_DIR` | — | alpha-expression-verifier `scripts/` 目录覆盖 | `wq-brain-campaign-toolkit/scripts/gate.py` · `mcp/tools_sim.py` | — |

#### 闸、开关与生成约束

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `BACKFILL_PC_FRESH` | — | `tools/backfill_prod_corr.py`：`=1` 忽略缓存重新取 prod 相关性 | `tools/backfill_prod_corr.py` | — |
| `CAMPAIGN_NO_CACHE` | — | `=1` 关闭 toolkit 的 metrics_cache | `wq-brain-campaign-toolkit/scripts/metrics_cache.py` | — |
| `CAMPAIGN_SKIP_DIR_CHECK` | — | `=1` 跳过战役目录合法性检查（仅测试） | `wq-brain-campaign-toolkit/scripts/_lib/common.py` | — |
| `LC_FRESH` | — | `tools/backfill_longcount.py`：`=1` 忽略 checkpoint 强制全量重跑（同 --fresh） | `tools/backfill_longcount.py` | — |
| `WQB_ALLOW_ALPHA_SUBMIT` | — | `=1` 允许 workflow 提交 alpha（`wqb.config.ALLOW_ALPHA_SUBMIT`）——**只解除闸门的 fail-closed，不等于自动提交**：真正提交仍需 `confirm_submit=True` + 用户明确确认（AGENTS.md §7）。`world-quant-brain-mcp/main.py:23` 按仓库根 `setdefault` 为 `1`（stdio 时代由客户端 env 注入，HTTP 常驻模式下客户端不起进程、无人注入） | `src/wqb/config.py` · `tests/unit/05_submit_quota/test_global_submit_lock.py` · +1 | — |
| `WQB_DISABLE_BACKLOG_GATE` | — | =1 跳过积压闸——开波闸簇 _run_backlog_gate 确实读取它（2026-10-06 更正旧「幽灵开关」说法：那是拆分文件未落盘导致读取点暂时消失的误判）。仅测试/沙箱隔离；生产放行走 waiver（AGENTS.md §8.1.2） | `src/wqb/workflow/nodes/campaign.py` · `tests/unit/02_workflow/test_workflow_nodes.py` | — |
| `WQB_DISABLE_REGION_GATES` | — | `=1` 关闭 toolkit 开波区域闸整体（catalog / signal_floor / stop_rules / backlog）——仅测试隔离；生产上跳过闸须走 waiver（AGENTS.md §8.1.2） | `wq-brain-campaign-toolkit/scripts/_lib/region_gates.py` · `tests/unit/01_store_db/test_region_gates_p0p1.py` | — |
| `WQB_DISABLE_SIGNAL_FLOOR_GATE` | — | =1 跳过信号天花板闸——开波闸簇 _run_signal_floor_gate 确实读取它（2026-10-06 更正旧「幽灵开关」说法）。仅测试/沙箱隔离；生产放行走 waiver（AGENTS.md §8.1.2） | `src/wqb/workflow/nodes/campaign.py` · `tests/unit/02_workflow/test_workflow_nodes.py` · +1 | — |
| `WQB_DISABLE_STOP_RULES_GATE` | — | =1 跳过停止规则闸——开波闸簇 _run_stop_rules_gate 确实读取它（2026-10-06 更正旧「幽灵开关」说法）。仅测试/沙箱隔离；生产放行走 waiver（AGENTS.md §8.1.2） | `src/wqb/workflow/nodes/campaign.py` · `tests/unit/02_workflow/test_workflow_nodes.py` · +1 | — |
| `WQB_FAMILY_CAP_UNKNOWN` | `0` | build_wave：`=1` 时对「未知」族也套同族封顶（缺省 0） | `wq-brain-campaign-toolkit/scripts/build_wave.py` | — |
| `WQB_GATE_MODE` | — | wave_gate / build_wave 的开波区域闸模式 `off|warn|enforce`（缺省 warn；日期翻转见 INDEX 闸与逃生口总表） | `wq-brain-campaign-toolkit/scripts/_lib/region_gates.py` · `tests/conftest.py` · +3 | — |
| `WQB_GEM_MAX_PER_SKELETON` | `12` | GEM 预闸：同骨架变体封顶（缺省 12，0 关闭） | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_pregate.py` · `tests/unit/03_gem/test_gem_pregate_platform_constraints.py` | 2026-09-19 |
| `WQB_INSPECT_MODE` | — | 体检硬门模式 `off|warn|enforce`（缺省 warn；新数据集首波自适应 enforce） | `src/wqb/workflow/nodes/wave_gate.py` · `tools/wave_gate.py` · +2 | — |
| `WQB_INVALID_FIELDS` | — | GEM 预闸：区域不可用字段覆盖（缺省读 `platform_constraints.json` 的 `region_invalid_fields`） | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_pregate.py` | — |
| `WQB_INVALID_GROUP_FIELDS` | — | GEM 预闸：区域非法 group 字段覆盖（缺省读 `region_invalid_group_fields`） | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_pregate.py` · `tests/unit/03_gem/test_gem_pregate_platform_constraints.py` | — |
| `WQB_LEDGER_BACKEND` | `sqlite` | toolkit ledger 后端（缺省 `sqlite`） | `wq-brain-campaign-toolkit/scripts/_lib/ledger.py` · `tests/unit/01_store_db/test_ledger_set_at_file.py` | — |
| `WQB_MAX_FIELD_REPEAT` | `3` | gate.py：同批内同一字段允许出现的次数上限 | `wq-brain-campaign-toolkit/scripts/gate.py` | — |
| `WQB_RULES_FILE_ONLY` | — | `=1` 时 toolkit 规则只读文件、不读 DB（隔离 / 排障用） | `wq-brain-campaign-toolkit/scripts/_lib/rules.py` | — |
| `WQB_SEM_MODE` | — | 闸 SEM（字段语义归类）模式 `off|warn|enforce`（缺省 enforce） | `tests/unit/06_wave_pipeline/test_wave_gate_waiver_phase.py` · `tools/wave_gate.py` · +2 | — |
| `WQB_STARTUP_CHECKS` | `always` | DB `ensure_schema` 启动自检：`always`（缺省）/ `once`（每进程一次）/ `0`（关） | `src/wqb/store/_schema.py` | — |
| `WQB_TRI_MODE` | — | S1 分诊闸逃生口：`=off` 关闭 fail-closed 分诊（同 --triage-gate off），醒目告警 | `wq-brain-campaign-toolkit/scripts/scan_fields.py` | — |
| `WQB_VECTOR_TS_FORBIDDEN_REGIONS` | — | GEM 预闸：禁止 `ts_*(vec_*)` 的区域清单覆盖（缺省读 `region_vector_ts_forbidden`） | `brain-make-some-gem/scripts/trailSomeAlphas/pipeline_pregate.py` | — |
| `WQB_WAIVER_MODE` | — | waiver 模式 `off|warn|enforce`（`--waiver-mode` 优先；缺省 warn：用了逃生口但台账没有 waiver 只在首屏告警，enforce 则 exit 2） | `src/wqb/waiver.py` · `tests/unit/06_wave_pipeline/test_wave_gate_waiver_phase.py` · +1 | — |

#### 并发、超时与轮询

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `API_SETTINGS_TIMEOUT` | `30` | MCP 传输层默认 API 超时（秒，缺省 30） | `mcp/brain_mixin_transport.py` | — |
| `BRAIN_AUTH_CHECK_TTL_SECONDS` | `300` | MCP 认证有效性检查的缓存秒数（缺省 300） | `mcp/brain_mixin_transport.py` | — |
| `BRAIN_CORRELATION_BUSY_RETRY_AFTER_SECONDS` | `180` | 相关性槽位忙时返回的建议重试秒数（缺省 180） | `mcp/brain_mixin_transport.py` | — |
| `BRAIN_CREATE_SIMULATION_MAX_CONCURRENCY` | `6` | MCP `create_simulation` 的并发上限（缺省 6） | `mcp/brain_mixin_transport.py` | — |
| `BRAIN_MAX_CONCURRENCY` | `8` | MCP 层 HTTP 请求并发上限（缺省 8）——**与模拟并发令牌 `slots=2` 不是同一个量** | `mcp/brain_mixin_transport.py` | — |
| `BRAIN_PYRAMID_ALPHAS_TIMEOUT_SECONDS` | `15` | 金字塔 alphas 查询超时（缺省 15） | `mcp/brain_mixin_correlation.py` | — |
| `BRAIN_SC_POOL_SYNC_DEBOUNCE_SECONDS` | `1` | SELF 相关性池同步的去抖秒数（缺省 1） | `mcp/brain_mixin_transport.py` | — |
| `BRAIN_USER_ALPHAS_CLIENT_FILTER_MAX_SCAN` | `1000` | `get_user_alphas` 客户端过滤的最大扫描条数（缺省 1000） | `mcp/brain_mixin_simulation.py` | — |
| `FE_API_TIMEOUT` | `120` | feature_engineering 拉字段的平台 API 超时（秒，缺省 120） | `brain-data-feature-engineering/scripts/feature_engineering.py` | — |
| `GEM_META_TIMEOUT_SEC` | `90` | gem 节点等 runner 写出 `meta.json` 握手的秒数（缺省 90）；超时报「no meta.json」——先查 LLM 通道 | `src/wqb/workflow/nodes/gem.py` | — |
| `WQB_CALIBRATE_TIMEOUT` | — | score_datasets 校准阶段的软超时（秒；超预算后周期性打线程栈） | `wq-brain-campaign-toolkit/scripts/score_datasets.py` | — |
| `WQB_CAMPAIGN_TIMEOUT` | — | campaign 节点子进程超时（秒） | `src/wqb/workflow/nodes/campaign.py` · `tests/unit/02_workflow/test_workflow_nodes.py` | — |
| `WQB_DETACHED_FIRST_OUTPUT_SEC` | `20` | detached 后台任务的首次输出心跳窗口（秒；超时判启动即死） | `src/wqb/workflow/nodes/batch_track.py` | — |
| `WQB_FORUM_RECON_TIMEOUT_SEC` | — | forum_recon / forum_recon_wave 节点及 pipeline.py --forum-recon 阶段的超时（秒；缺省 900） | `wq-brain-campaign-toolkit/scripts/pipeline.py` · `src/wqb/workflow/nodes/forum_recon.py` · +1 | — |
| `WQB_GLOBAL_SLOTS` | `2` | 账户级模拟并发令牌数（多流水线同跑共享）；缺省 = `config.CONCURRENCY['slots']`，2026-10-06 定案为 2（旧 7）；0 = 关闭仲裁 | `wq-brain-campaign-toolkit/scripts/_lib/slots.py` · `tests/unit/02_workflow/test_pipeline_error_isolation.py` · +2 | 2026-09-19 |
| `WQB_WAVE_GATE_TIMEOUT_SEC` | — | wave_gate 节点子进程超时（秒） | `src/wqb/workflow/nodes/wave_gate.py` · `tests/unit/02_workflow/test_run_logged_subprocess.py` | — |
| `SA_PROBE_CACHE_TTL_HOURS` | `6` | SA 盘点缓存新鲜度窗口（小时，默认 6）——tools/probe/probe_sa_candidates.py 的 results/sa_probe_cache.json TTL；--cache-ttl-hours 优先 | `tools/probe/probe_sa_candidates.py` | — |

#### MCP 服务与平台传输

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `FORUM_RATE_LIMIT_SECONDS` | `0` | MCP 传输层对论坛请求的最小间隔（秒，缺省 0） | `mcp/brain_mixin_transport.py` | — |
| `MCP_HOST` | `127.0.0.1` | streamable-http 监听地址 | `mcp/main.py` · `mcp/mcp_core.py` · +1 | — |
| `MCP_PORT` | `8000` | streamable-http 监听端口 | `mcp/main.py` · `mcp/mcp_core.py` · +1 | — |
| `MCP_STREAMABLE_HTTP_PATH` | `/mcp` | streamable-http 路径 | `mcp/mcp_core.py` | — |
| `MCP_TRANSPORT` | `streamable-http` | MCP 服务传输方式（缺省 `streamable-http`；2026-10-05 起两个 server 常驻 HTTP，客户端只连 URL 不再起进程） | `mcp/main.py` · `wqb_db_mcp.py` | — |

#### 论坛 / Labs 浏览器通道

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `FORUM_MAX_CONCURRENCY` | `1` | 论坛浏览器会话并发（缺省 1） | `mcp/forum_functions.py` | — |
| `FORUM_SETTINGS_BASE_URL` | `https://support.worldquantbrain.com` | 论坛站点根（缺省官方支持站；测试环境可改指别处） | `mcp/forum_functions.py` | — |
| `FORUM_SETTINGS_HEADLESS` | `true` | 论坛浏览器是否无头（缺省 true） | `mcp/forum_functions.py` | — |
| `FORUM_SETTINGS_TIMEOUT` | `15` | 论坛选择器等待超时（秒） | `mcp/forum_functions.py` | — |
| `LABS_AGENT_SCRIPT` | — | Labs 分析引擎脚本路径覆盖 | `mcp/labs_functions.py` | — |
| `LABS_MAX_CONCURRENCY` | `1` | Labs 浏览器会话并发（缺省 1） | `mcp/labs_functions.py` | — |
| `LABS_PLATFORM_URL` | `https://platform.worldquantbrain.com` | Labs 所在的平台站点根 | `mcp/labs_functions.py` | — |
| `LABS_SETTINGS_HEADLESS` | — | Labs 浏览器是否无头（缺省跟随 `FORUM_SETTINGS_HEADLESS`） | `mcp/labs_functions.py` | — |
| `LABS_SETTINGS_TIMEOUT` | `30` | Labs 选择器等待超时（秒） | `mcp/labs_functions.py` | — |

#### 内部标记（勿手设）

| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |
|---|---|---|---|---|
| `GEM_ERR_FILE` | — | GEM runner 子进程的 stderr 文件路径（runner 自己设，勿手设） | `brain-make-some-gem/scripts/headless_runner/run.py` | — |
| `GEM_LOG_FILE` | — | GEM runner `--detached` 子进程的日志文件路径（runner 自己设，勿手设） | `brain-make-some-gem/scripts/headless_runner/run.py` | — |
| `GEM_META_FILE` | — | GEM runner 子进程的 `meta.json` 握手文件路径（runner 自己设，勿手设） | `brain-make-some-gem/scripts/headless_runner/run.py` | — |
| `WQB_DBLOCK_DISABLE` | — | `=1` 关闭 DB 写锁——仅测试隔离，生产禁用 | `wq-brain-campaign-toolkit/scripts/_lib/dblock.py` · `src/wqb/db_write_lock.py` · +1 | — |
| `WQB_PBR_BOOTSTRAPPED` | — | `tools/prod_blocked_recheck.py` 的防递归重入标记（勿手设） | `tools/prod_blocked_recheck.py` | — |
| `WQB_PYENV_REEXEC` | — | `tools/_pyenv.py` 的防递归重入标记（勿手设） | `tests/unit/09_core/test_pyenv.py` · `tools/_pyenv.py` | — |
| `WQB_SQ_BOOTSTRAPPED` | — | `tools/submit_queue.py` 的防递归重入标记（勿手设） | `tools/submit_queue.py` | — |
<!-- env-table:end -->

## 3. CLI 开关（不是环境变量）

闸类开关的**缺省 / 日期翻转 / waiver 批准人**统一登记在 INDEX 的「闸与逃生口总表」（`src/wqb/waiver.py::GATE_POLICIES` 生成），下面只列**功能类**开关：

| 开关 | 所属 | 作用 | 缺省 |
|---|---|---|---|
| `--no-isolate-errors` | toolkit `pipeline.py` | 关闭「连坐隔离」：ERROR 批不再解析子模拟、不再把坏式回写 `expressions.status='fail'`、不再重发无辜兄弟 | 隔离开（2026-09-19 起） |
| `--enhance-diversity {never,auto,always}` | toolkit `build_wave.py` / sim-alphas `batch_simulator.py` | 是否在入批 / 发送前改写表达式做多样性增强 | `never`（DEC-35：缺省不改写，结构多样性交下游闸 6） |
| `--skip-diversity-gate` | `gate.py` 闸 6 | 逃生阀；须有 waiver | 闸常开 |
| `--batch-type {probe,repair}` | `gate.py` / `pipeline.py` / `wave_gate.py` | 探针 / 修复批豁免闸 6 与 qp 标注 | 常规批 |
| `--gate0` / `--sanity-longcount` / `--sanity-event-type` | `gate.py` | 打开闸 0 / 闸 7 / 闸 8（功能开关：开得越多越严，不是逃生口） | 关 |
| `--waiver-mode {off,warn,enforce}`（或 `WQB_WAIVER_MODE`） | `tools/wave_gate.py` | 用了逃生口但台账没有 waiver 时：不检查 / 首屏告警 / exit 2 | `warn` |
| `--dry-run` / `dry_run` | GEM runner、多数节点 | 只验证命令 / 计划能构建；**验证不了 LLM 可达性、平台状态**（GEM 的 `402` 干跑照样 OK） | 关 |
| `--detached` | GEM runner、sim-alphas | 后台启动并写 `meta.json`；用 `workflow_task_status` 查，不翻日志 | 关（节点缺省 True） |
| `--allow-prod-above-07` | `tools/super_build.py` | 豁免 SUPER 的 prod ≥ 0.7 闸——**红线邻近，须用户明确要求** | 闸强制 |
| `--confirm-submit` | judge `judge_alpha.py` | **已移除**的旧参数：传入即报错 exit 2（judge 不提交；提交只走 `workflow_submit_alpha`） | — |
