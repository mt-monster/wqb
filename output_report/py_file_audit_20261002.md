# Python 文件体量与职责审计报告（2026-10-02）

> 范围：`D:\coding\traeCN_project\wqb`，共扫描 **1217 个 Python 文件**（排除 `.venv` / `__pycache__` / `.git` / `node_modules` / `site-packages`）。
> 工具：`tools/audit_file_sizes.py`（AST 静态分析，行数 / 最长函数 / 圈复杂度 / 函数类计数），原始数据 `logs/file_audit.json`。
> **约束（用户定案）**：所有拆分方案**必须保持对外接口与现有行为、功能逻辑完全不变** —— 全部走「抽模块 + 原文件 re-export / 委托」模式，不改任何公共签名。

---

## 0. 结论速览

| 严重度 | 数量 | 代表文件 |
|---|---|---|
| **P0 需拆分** | 3 | `nodes/campaign.py`（2256）、`pipeline.py`（1573）、`wqb_db_mcp.py`（2705） |
| **P1 建议拆分** | 4 | `gate.py`（1685）、`gem.py`（1619）、`build_wave.py`（1255）、`campaign_intel.py`（1416） |
| **P2 重复逻辑** | 2 组 | `ace_lib.py`×4 副本、`validator.py`×4+1 副本 |
| 无需动作 | — | `toolkit/campaign.py`（92 行分发器，设计良好） |

**核心问题不是"行数多"本身，而是"单文件承担 N 个正交职责 + 巨型 switch/上帝函数"**。最大的两个文件恰好是用户点名的 `campaign.py` 与 `pipeline.py`。

---

## 1. 重点深析一：`src/wqb/workflow/nodes/campaign.py`（2256 行，71 函数，max `run()` 681 行 / cc 143）

### 1.1 它现在承担了什么（7 个正交职责）

`run()` 是一个 **686 行的巨型 switch 路由器**，单个函数体内塞了 S0–S6 共 7 个阶段的全部编排逻辑：

| 职责 | 位置 | 行数级 |
|---|---|---|
| ① 参数校验 + campaign_dir 解析 + config 自动创建 | `run()` 前段 135–190 + `_ensure_campaign_config` | ~120 |
| ② stage→script 路由 + subcommand 路由 | `run()` 中段 194–260 | ~70 |
| ③ 缓存检查 / 回写（calibrate、assemble-priors） | `run()` 213–249 + 710–727 | ~60 |
| ④ **按 stage 构建命令**（S0–S6 每分支大量内嵌 if-elif，注入 dataset/wave/缓存参数） | `run()` 268–515 | ~250 |
| ⑤ argv 契约校验 + dry-run 短路 | `run()` 517–544 | ~30 |
| ⑥ **异步子进程执行**（Popen + 后台线程 + 文件落盘 + 超时 kill + 结果收集） | `run()` 546–790（含内嵌 `_wait_and_collect` ~130 行） | ~245 |
| ⑦ 各类闸门（分散在 run 外部，但被 run 调） | `_run_preflight` / `_run_quality_gate` / `_run_backlog_gate` / `_run_stop_rules_gate` / `_run_signal_floor_gate` / `_field_inspect_pack_check` / `_semantic_coverage_check` / `run_open_wave_gates` | ~1200 |

### 1.2 问题类型

- **过长**：2256 行，单函数 `run()` 681 行。
- **圈复杂度过高**：`run()` cc=**143**（全项目第 4）。根因是 `elif stage == "Sx"` 七分支 × 每分支内又有多层条件（calibrate / subcommand / dry_run / 闸成败），分支组合爆炸。
- **职责耦合**：编排路由（②④）、进程管理（⑥）、闸门判定（⑦）、缓存（③）**四种不同性质的逻辑**缠在同一个 run() 与同文件里；`_wait_and_collect` 还同时做结果收集 + DB 回写 + 缓存回写 + Mode B 资格线学习 + S4 walls 入库（5 件事）。

### 1.3 拆分方案（接口不变）

保持 `run(region, stage, ...)` 与全部 `_run_*` 闸函数的**现有签名与返回值**完全不动。原文件降级为**编排壳 + re-export**：

| 新模块 | 迁入内容 | 依据 |
|---|---|---|
| `nodes/campaign/gates.py` | 全部 `_run_preflight` / `_run_quality_gate` / `_run_backlog_gate` / `_run_stop_rules_gate` / `_run_signal_floor_gate` / `_field_inspect_pack_check` / `_semantic_coverage_check` / `run_open_wave_gates` | 闸门判定是一个独立职责簇，彼此同源（纯 DB/子进程判定），可从编排解耦单独测试 |
| `nodes/campaign/command.py` | 命令构建器 `build_command(stage, subcommand, dataset, wave, calibrate, extra_args) -> (cmd, steps)` —— 抽 run() 的 ②④ | 巨型 switch 的根因是「命令构建」散落在编排里；抽成纯函数后每个分支可单测 |
| `nodes/campaign/executor.py` | `launch_async(cmd, stage, region, ...) -> task` —— 抽 run() 的 ⑤⑥（Popen/线程/落盘/超时/kill）+ `_wait_and_collect` | 进程管理是独立的系统关注点，与业务编排无关 |
| `nodes/campaign/cache.py` | calibrate / assemble-priors 的 cache_key 决策 + 读写 | 缓存策略独立 |
| `nodes/campaign.py`（原文件） | 保留 `run()` 作为**薄编排**：依次调 command 构建 → gates → executor → cache；文件顶部 re-export 所有既有符号 | **对外接口零变化**：现有 `from wqb.workflow.nodes.campaign import run / _run_preflight / ...` 的调用方全部不需要改 |

**拆分依据（SRP + 测试性）**：一个函数应只做一件事。`run()` 现在的失败模式是「改 S4 的一个参数注入，要通读 686 行并担心碰坏 S3 的闸调用顺序」。拆分后：改命令构建只动 `command.py`，改进程管理只动 `executor.py`，二者互不干扰；每个模块的圈复杂度可压到 < 30。

---

## 2. 重点深析二：`Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py`（1573 行，47 函数，max 234 行 / cc 63）

### 2.1 它现在承担了什么（9 个正交职责）

| 职责 | 函数 | 行数级 |
|---|---|---|
| ① 配额闸（ET 日历日） | `submission_quota` / `quota_cfg` / `_parse_submitted_ts` / `_timeutil` | ~60 |
| ② checkpoint 续跑 | `ckpt_path` / `ckpt_load` / `ckpt_save` | ~50 |
| ③ 闸（gate 委托） | `stage_gate` / `stage_batch_gates` | ~80 |
| ④ **提交 + 轮询 + 收割 + 连坐隔离 + 槽位填充** | `submit_batch` / `_submit_single_batch` / `_poll_single_batch` / `_harvest_batch_alphas` / `_harvest_batch_errors` / `_isolate_error_batch` / `_mark_culprits_in_db` / `_update_ck_batch` / `_run_round`（内嵌 `_queue_retry_or_fail` / `_refill` / `_fill_slots`）/ `stage_submit_poll` | ~500 |
| ⑤ 回测完整性校验 | `check_backtest_completeness` / `_count_wave_backtest_rows` / `_report_completeness` | ~70 |
| ⑥ S4 walls 载荷 + 评审 | `build_s4_walls_payload` / `_write_s4_walls` / `stage_review` | ~200 |
| ⑦ 设置覆盖 + 先验 | `_cmd_main` 内的 `--set` / `--neutralization` / `settings_prior` 段 | ~100 |
| ⑧ CLI 入口 + 参数解析 | `main` / `_sub_campaign_arg` | ~80 |
| ⑨ 附加动作（prod-first / forum-recon） | `stage_prod_first` / `stage_forum_recon` | ~70 |

### 2.2 问题类型

- **过长**：1573 行。
- **职责耦合**：CLI 解析、设置先验、配额、checkpoint、提交调度、评审、台账回写全在一个文件。`_cmd_main`（1313–1496，~180 行）把「解析参数→覆盖设置→应用先验→硬门→S2 合规→加载表达式→过闸→提交→评审→回写」串成一长串过程式步骤。
- **圈复杂度**：`main`/`_cmd_main`/`_run_round` 组合 cc 达 63–118（`_run_round` 内嵌 3 个闭包函数 `_queue_retry_or_fail`/`_refill`/`_fill_slots`，槽位填充状态机复杂）。

### 2.3 拆分方案（接口不变）

`pipeline.py` 保留 `main()` / `_cmd_main()` 作为 CLI 与编排壳，各职责抽成子模块，原函数名 re-export：

| 新模块 | 迁入内容 | 依据 |
|---|---|---|
| `pipeline_pkg/quota.py` | ① 配额闸全部 | 配额是独立的外部约束关注点 |
| `pipeline_pkg/checkpoint.py` | ② checkpoint | 续跑机制独立，供其他脚本复用 |
| `pipeline_pkg/submitter.py` | ④ 提交/轮询/收割/隔离/槽位（`_run_round` 及其 3 个内嵌闭包提升为模块级） | 提交调度是最大的一块（~500 行），且状态机复杂值得单独测试 |
| `pipeline_pkg/completeness.py` | ⑤ 完整性校验 | 独立校验逻辑 |
| `pipeline_pkg/review_stage.py` | ⑥ S4 walls + 评审 | 评审是一个子阶段 |
| `pipeline_pkg/settings.py` | ⑦ 设置覆盖 + settings 先验 | 设置决策独立 |
| `pipeline.py`（原文件） | `main()` / `_cmd_main()` 薄编排 + 顶部 re-export 全部既有符号 | **接口零变化**：`python pipeline.py run --submit ...` 的行为逐字节不变 |

**拆分依据**：`pipeline.py` 的本质是「一条主线 + 多个旁路职责」。主线是 `run/quota` 编排；旁路（配额/checkpoint/完整性/walls/附加动作）各自正交。抽出后主线 `_cmd_main` 收敛为 ~60 行的编排，可读性与单测性大幅提升。这与 `toolkit/campaign.py`（92 行）已验证的「薄分发器」模式一致——后者就是好的对照样本。

---

## 3. 全量清单（按优先级排序）

> 问题类型缩写：**过长** = 行数；**巨型函数** = 单函数行数/cc；**职责耦合** = SRP 违反；**重复** = 同文件多副本；**cc** = 圈复杂度。

### P0（立即拆分）

| # | 文件 | 行数 | 问题类型 | 拆分 / 优化建议 |
|---|---|---|---|---|
| 1 | `src/wqb/workflow/nodes/campaign.py` | 2256→**1484**（已拆第一步）| 过长 + 巨型函数（`run` 681/cc143）+ 职责耦合（7 职）| §1.3：抽 `gates.py` / `command.py` / `executor.py` / `cache.py`，原文件留薄壳 re-export。**已落地第 1 步**：开波闸簇（2 常量 + 13 函数，783 行）抽至 `_campaign_open_gates.py`，全部测试绿、接口不变。详见文末「执行记录」 |
| 2 | `world-quant-brain-mcp/labs_data_analysis_agent.py` 与仓库根 `wqb_db_mcp.py` | 2705 | 过长 + 职责耦合（69 函数：wave/region/field/alpha/workflow/registry…）| 按域拆 `mcp/wave.py`、`mcp/region.py`、`mcp/field.py`、`mcp/workflow.py`…，原文件 re-export（MCP 工具函数签名不变） |
| 3 | `Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py` | 1573 | 过长 + 职责耦合（9 职）+ `_run_round` 状态机复杂 | §2.3：抽 `pipeline_pkg/{quota,checkpoint,submitter,completeness,review_stage,settings}.py` |

### P1（建议拆分）

| # | 文件 | 行数 | 问题类型 | 建议 |
|---|---|---|---|---|
| 4 | `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py` | 1685 | 过长 + `check_one` cc=**103** | 8 个闸各自抽成 `_gate/n{0..8}_*.py`，`check_one` 按闸号分发到各闸函数；`gate.py` 留表驱动壳 |
| 5 | `src/wqb/workflow/nodes/gem.py` | 1619 | 过长 + 巨型函数（`run` 338/cc46）+ 职责耦合（模板检测/进程/priors/ideas/字段上下文）| 抽 `gem/{priors.py, ideas.py, spawn.py, prompts.py}`，原文件 re-export |
| 6 | `tools/campaign_intel.py` | 1416 | 过长 + `_cmd_s0_select` cc=**142**（310 行）| `_cmd_s0_select` 拆「候选收集 → 评分 → 过滤 → 输出」四步纯函数；子命令分发留主文件 |
| 7 | `Claude/skills/wq-brain-campaign-toolkit/scripts/build_wave.py` | 1255 | 巨型函数（`main` 796 行 / cc **341**）| `main` 拆「加载表达式 → 评分 → 多样性 → 选波 → 回写」；单函数 796 行是最高优先 |
| 8 | `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py` | 1486 | 巨型函数（`main` 1109 行 / cc 259）| 同上，按阶段拆函数；该 main 是全项目最长单函数 |

### P2（重复逻辑）—— ⚠ 经逐案核实，多数**不需收敛**（见文末「核实记录」）

| # | 文件 | 行数 | 初判 | 核实结论 |
|---|---|---|---|---|
| 9 | `ace_lib.py` × 4 副本 | 1553/1535 | 重复逻辑，收敛 | **真实漂移但无害**：两版仅 `get_datasets` 重试容错一处差异；全仓唯一调用方 `trailSomeAlphas/run_pipeline.py` 用的恰是健壮版，两个 1535 缺陷版所在 skill 不调用它 ⇒ 缺陷在死路径，**收敛收益≈0，不做** |
| 10 | `validator.py` × 4 副本 + 1 src 版 | 1412 / 407 | 重复逻辑，收敛到 src 版 | **误判**：src 版（形状分类）与 skill 版（PLY 语法校验）**同名不同物**；且 skill 4 副本是**有意镜像**（单一来源约定 + `test_se_docs.py` 逐字节钉死）⇒ **不动** |
| 11 | `cache/backup_switch_main_20260929/wqb_db_mcp.py` | 2499 | 历史备份干扰检索 | **唯一仍成立**：归档/删除，避免干扰全量扫描与检索 |

### 对照样本（设计良好，无需拆分）

| 文件 | 行数 | 说明 |
|---|---|---|
| `Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py` | 92 | **薄子命令分发器**，职责单一（路由到各能力脚本）。**这正是 campaign.py 节点版应有的形态** |
| `src/wqb/store/campaign.py` | 351 | 存储层，规模适中 |
| `src/wqb/semantic_ledger.py` | 小 | 单一事实源（本轮新抽），是好的拆分范式 |

---

## 4. 通用拆分纪律（所有方案共用，保证接口/行为不变）

1. **抽模块 + 原文件 re-export**：把实现搬进 `*_pkg/` 子模块，原文件只留 `from ._pkg.x import *` / 显式 re-export。现有 `from xxx import yyy` 的调用方**一行不用改**。
2. **公共签名冻结**：所有 `def run(...)` / `def main()` / MCP 工具函数 / CLI argparse 的参数与默认值原样保留。
3. **先测试后移动**：移动前确保目标函数/模块的现有测试全绿；移动后重跑同一套测试（`tests/unit/02_workflow`、`tests/unit/08_forum_recon` 等）。本仓 2869 个单测是最强回归网。
4. **避免 safe-delete 钩子干扰**：全量跑 pytest 前先单跑目标目录确认绿（钩子会把 `01_store_db` 这类起子进程的测试成片打红，属环境噪声，见 MEMORY §4）。
5. **skill 单点写入**：toolkit / skills 下的文件只改仓库 `Claude/skills/…` 副本，改完 `python tools/sync_skills.py` 同步，不直改安装位。

---

## 5. 数据附表（全量 Top，来自 `logs/file_audit.json`）

- 行数 Top：`wqb_db_mcp.py`(2705) > `nodes/campaign.py`(2256) > `labs_data_analysis_agent.py`(2062) > `gate.py`(1685) > `gem.py`(1619) > `pipeline.py`(1573) > `build_wave.py`(1255)
- 单函数行数 Top：`run_pipeline.py::main`(1109) > `build_wave.py::main`(796) > `run_realenv.py::_main_body`(786) > `nodes/campaign.py::run`(681)
- 圈复杂度 Top：`run_realenv._main_body`(377) > `build_wave.main`(341) > `run_pipeline.main`(259) > `wave_gate/cli.main`(163) > `nodes/campaign.run`(143) > `campaign_intel._cmd_s0_select`(142)

---

## 6. 执行记录（2026-10-02，拆分已启动）

### 6.1 已完成：`campaign.py` 第 1 步 —— 开波闸簇抽离

- **手法**：AST 精确剪切（非手工逐行），新建 `src/wqb/workflow/nodes/_campaign_open_gates.py`（834 行），原文件顶部 `from ._campaign_open_gates import (...)` re-export。
- **内容**：`STOP_RULES_DEFAULTS` / `BACKLOG_GATE_DEFAULTS` 两常量 + 13 个函数（`run_open_wave_gates`、三道开波闸、停止规则求值及其辅助）。
- **结果**：`campaign.py` 2266 → **1484 行**（−35%）。
- **接口不变验证**：`from .nodes import campaign`（registry）、`from .campaign import run_open_wave_gates`（batch_track）、`from ...campaign import _normalize_verdict`（测试）全部照旧可用；S3 dry-run 冒烟通过（命令构建、闸调用顺序不变）。
- **连带同步（登记表跟随代码位置，均为正确更新，非功能变更）**：
  - `docs/env_and_switches.md`：3 个 `WQB_DISABLE_*_GATE` 的"读取方"路径 `campaign.py` → `_campaign_open_gates.py`（跑 `tools/index_tables.py --apply` 生成；`WQB_TRI_MODE` 仅为位置重排）。
  - `docs/ledger_keys.json`：`backlog_gate_override` 的 writer/reader via 更新到新文件。
- **清理**：删除 campaign.py 顶部 3 个 unused import（`_waiver` / `_contract_normalize_verdict` / `local_ts`，只被搬走的闸簇用）。
- **回归**：02_workflow + 06_wave_pipeline + 09_core + 07_docs_skills + 01_store_db + 04_gates 全绿。

### 6.2 待做（run() 内部，风险更高，建议单独一批）

`run()` 仍是 691 行的巨型 switch。下一步候选（按风险从低到高）：
1. **命令构建**：把 268–515 行的 `elif stage==...` 命令拼装抽成纯函数 `build_command(...) -> (cmd, steps, early_return)`。
2. **异步执行器**：把 546–790 行的 Popen/线程/落盘/超时/DB 回写抽成 `executor.py`（内嵌 `_wait_and_collect` 依赖 run 的 9 个局部变量，需封装 context 对象传入）。
3. **缓存**：calibrate/assemble-priors 的 cache_key 决策抽成 `cache.py`。

每步仍遵循「抽模块 + 原文件 re-export + 先测试后移动」。

---

## 7. P2 重复逻辑核实记录（2026-10-02）—— 区分「真重复 / 有意镜像 / 无害漂移」

> 教训：**初判靠"同名 + 行数接近"会误判**。收敛前必须逐案核实三件事：①内容是否真的语义重复（还是同名不同物）；②是否有单一来源/镜像约定（有意设计）；③差异代码是否真的被调用（还是死路径）。

### 7.1 `validator.py`：有意镜像，不动
- `src/wqb/expression/validator.py`（407 行）= 形状分类 + 批级多样性闸（`check_batch`/`classify_shape`）；
  skill 副本（1412 行）= PLY 完整语法校验引擎。**同名不同物**，两文件 docstring 已互相标注「命名辨析 2026-09-12」。
- skill 的 4 份副本：权威版 = `alpha-expression-verifier/scripts/validator.py`，其余 3 份为逐字节镜像，
  `tests/unit/07_docs_skills/test_se_docs.py` 钉死一致性；docstring 有同步命令与历史漂移事故（hump/bucket）记录。
  ⇒ **这是 skill 自包含的必要设计（sync 到安装位后独立运行），有测试兜底，不动。**

### 7.2 `ace_lib.py`：真实漂移但在死路径，不做
- 4 副本哈希分两组：1553 版×2（含 `get_datasets` 的 429 重试/非 json 容错）、1535 版×2（无容错）。函数集完全一致。
- **差异仅在 `get_datasets` 一处实现**。
- 全仓 `get_datasets` 调用方：仅 `trailSomeAlphas/run_pipeline.py:593`，而它用的是 **1553 健壮版**；
  两个 1535 缺陷版所在 skill（`brain-inspect-raw`、`brain-sim-alphas-in-batch-and-track`）**只调
  `get_instrument_type_region_delay` / `generate_alpha` / `get_credentials`，不调 `get_datasets`**。
  ⇒ **缺陷代码在无人调用的死路径，收敛无实际收益，不做。**
- （可选，零风险）若想防未来误用：给 4 份 `ace_lib.py` 补一行「单一来源」注释指向 1553 权威版——纯文档，非必须。

### 7.3 真正仍值得做的只有 #11
`cache/backup_switch_main_20260929/wqb_db_mcp.py`（2499 行历史备份）：干扰全量扫描与检索，建议归档/删除。

### 7.4 元结论（呼应「不要为拆而拆」）
- **闸簇抽离（已做）**：拆的是持续演进、被复用的独立业务逻辑——**值得**。
- **run() 内部拆分**：搬低频稳定的编排/执行器，收益递减 + 风险递增——**不做**。
- **validator / ace_lib 收敛**：一个是有意镜像、一个是死路径漂移——**都不做**。
- ⇒ 本仓当前的「结构问题」大多是有意设计或无害噪声；**唯一仍值得动的是删 cache 历史备份（#11）**。
