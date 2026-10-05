# wq 工作台 · 全量测试总结报告

> 生成时间：2026-10-01 11:16（GMT+8）　|　运行模式：pytest --collect-only 口径，并行度 4
> 解释器：`D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe`　|　参数：`-q --no-header -p no:cacheprovider -ra`

## 一、总览指标

| 指标 | 数值 |
|---|---|
| 分组数 | 12
| 测试文件 | 180
| 用例总数（收集口径） | 2863
| 实际执行（通过+失败+跳过+错误） | 2895
| ✅ 通过 | 2850
| ❌ 失败 | 17
| ⏭ 跳过 | 28
| ⚠ 错误 | 0
| **通过率** | **99.5%**
| 累计耗时（并行墙钟近似） | 156.9s |

## 二、分组结果明细

| 分组 | 业务域 | 文件 | 用例 | 通过 | 失败 | 跳过 | 错误 | 耗时 | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| `01_store_db` | 存储/数据原子层 | 25 | 338 | 365 | 5 | 0 | 0 | 50.82s | ❌ |
| `02_workflow` | 战役工作流编排 | 17 | 254 | 243 | 0 | 11 | 0 | 12.31s | ✅ |
| `03_gem` | GEM 概念优先信号生成引擎 | 9 | 80 | 80 | 0 | 0 | 0 | 4.09s | ✅ |
| `04_gates` | 提交前闸门体系 | 13 | 158 | 156 | 2 | 0 | 0 | 10.90s | ❌ |
| `05_submit_quota` | 提交与配额链路 | 16 | 166 | 166 | 0 | 0 | 0 | 8.16s | ✅ |
| `06_wave_pipeline` | 波次流水线全链路 | 24 | 263 | 259 | 1 | 3 | 0 | 17.73s | ❌ |
| `07_docs_skills` | 文档/技能一致性（双轨同源守护） | 25 | 784 | 776 | 4 | 4 | 0 | 22.80s | ❌ |
| `08_forum_recon` | 论坛情报复盘决策 | 17 | 218 | 215 | 3 | 0 | 0 | 5.61s | ❌ |
| `09_core` | 核心域包(src/wqb) | 20 | 459 | 453 | 2 | 4 | 0 | 4.41s | ❌ |
| `10_toolkit_scripts` | 工具脚本正确性 | 8 | 41 | 39 | 0 | 2 | 0 | 0.46s | ✅ |
| `mcp_pkg` | MCP 服务包(wq-brain-http)单体 | 5 | 92 | 88 | 0 | 4 | 0 | 6.71s | ✅ |
| `tests_root` | tests 根级 CLI 入口 | 1 | 10 | 10 | 0 | 0 | 0 | 1.73s | ✅ |

## 三、测了哪些功能与业务场景（重点）

全量用例覆盖 **WorldQuant BRAIN alpha 挖掘工作区** 的整条链路——从字段/数据存储、
GEM 信号生成、提交前闸门与配额，到波次回测流水线、论坛情报复盘决策，以及 MCP 服务与文档/技能同源守护。

### `01_store_db` 01_store_db　（338 用例）

- **业务场景**：存储/数据原子层：alpha 数据 atom 标注与落地、字段目录索引构建、波次选择(wave selection)构建、S1 分类字段分诊 B 阶段。验证数据如何被规范写入与回读。

- **覆盖范围**：25 个测试文件，365 通过 / 5 失败 / 0 跳过 / 0 错误。

### `02_workflow` 02_workflow　（254 用例）

- **业务场景**：战役工作流编排：alpha_properties 部分 PATCH 提交属性读写、campaign prompt 命令(P4)、detached 首输出心跳保活、judge 评审检查清单(P3)。验证九步流水线的节点行为。

- **覆盖范围**：17 个测试文件，243 通过 / 0 失败 / 11 跳过 / 0 错误。

### `03_gem` 03_gem　（80 用例）

- **业务场景**：GEM 概念优先信号生成引擎：控制台 watch、组合字段、pipeline 模式、pregate 平台约束预检。验证 brain-make-some-gem 如何把 idea 渲染成合法 alpha 表达式。

- **覆盖范围**：9 个测试文件，80 通过 / 0 失败 / 0 跳过 / 0 错误。

### `04_gates` 04_gates　（158 用例）

- **业务场景**：提交前闸门体系：catalog gate、cluster variants、gate5 覆盖矩阵、equal_weight_leg_add（组合形态铁律——禁止两条独立信号腿加权相加）。验证提交层四闸与混信号铁律拦截。

- **覆盖范围**：13 个测试文件，156 通过 / 2 失败 / 0 跳过 / 0 错误。

### `05_submit_quota` 05_submit_quota　（166 用例）

- **业务场景**：提交与配额链路：鉴权瞬断重试、batch 状态鉴权、batch submit_verdict 阶段2 否决权威。验证平台 POST 提交、403/瞬断处理与配额判定。

- **覆盖范围**：16 个测试文件，166 通过 / 0 失败 / 0 跳过 / 0 错误。

### `06_wave_pipeline` 06_wave_pipeline　（263 用例）

- **业务场景**：波次流水线全链路：backlog 丢弃守卫、未消费 backlog 闸门(P0/P2)、harvest 字段路径与 longcount 字段校验。验证 构建波次→并发回测→harvest 收口 的守卫。

- **覆盖范围**：24 个测试文件，259 通过 / 1 失败 / 3 跳过 / 0 错误。

### `07_docs_skills` 07_docs_skills　（784 用例）

- **业务场景**：文档/技能一致性（双轨同源守护）：审计修复、alpha repair 文档、docs 一致性(292)、经验库引用。验证 skill/文档与代码同源、引用不漂移。

- **覆盖范围**：25 个测试文件，776 通过 / 4 失败 / 4 跳过 / 0 错误。

### `08_forum_recon` 08_forum_recon　（218 用例）

- **业务场景**：论坛情报复盘决策：campaign intel 落地、饱和数据集标记、prod 首波、S0 选区排名。验证「论坛情报→挖掘方向」的复盘与选向逻辑。

- **覆盖范围**：17 个测试文件，215 通过 / 3 失败 / 0 跳过 / 0 错误。

### `09_core` 09_core　（459 用例）

- **业务场景**：核心域包(src/wqb)：config 域常量、dataset experience、diversity 多样性、field semantic classify 字段语义分类。验证规范核心包的行为契约。

- **覆盖范围**：20 个测试文件，453 通过 / 2 失败 / 4 跳过 / 0 错误。

### `10_toolkit_scripts` 10_toolkit_scripts　（41 用例）

- **业务场景**：工具脚本正确性：degraded pack 标记、OS decay 基准/校准、s2 字段校验器。验证辅助工具链的输出符合预期。

- **覆盖范围**：8 个测试文件，39 通过 / 0 失败 / 2 跳过 / 0 错误。

### `mcp_pkg` MCP 包　（92 用例）

- **业务场景**：MCP 服务包(wq-brain-http)单体：brain_api 门面、mcp_tools 工具、submit_verdict 工具、tools_workflow 节点注册。验证 MCP 层与上层 workflow 节点同步。

- **覆盖范围**：5 个测试文件，88 通过 / 0 失败 / 4 跳过 / 0 错误。

### `tests_root` tests 根级　（10 用例）

- **业务场景**：tests 根级 CLI 入口：toolified cli 命令行装配。验证根级命令入口可用。

- **覆盖范围**：1 个测试文件，10 通过 / 0 失败 / 0 跳过 / 0 错误。

## 四、失败 / 异常明细

### `01_store_db` 01_store_db（失败 5 条）

- `tests/unit/01_store_db/test_db_write_guards.py::TestNoNakedSqliteConnect::test_no_naked_connect_outside_whitelist`
- `tests/unit/01_store_db/test_ledger_key_catalog.py::test_catalog_schema`
- `tests/unit/01_store_db/test_ledger_key_catalog.py::test_code_refs_exist_and_mention_the_key`
- `tests/unit/01_store_db/test_submit_queue_gates.py::test_prod_sibling_marks_untested_twin_dead`
- `tests/unit/01_store_db/test_submit_queue_gates.py::test_regrade_ready_applies_new_gates_to_legacy_rows`

### `04_gates` 04_gates（失败 2 条）

- `tests/unit/04_gates/test_semantic_gate_failclosed.py::test_semantic_gate_no_db_write_when_not_from_db`
- `tests/unit/04_gates/test_semantic_gate_failclosed.py::test_gate_result_final_verdict_is_persisted`

### `06_wave_pipeline` 06_wave_pipeline（失败 1 条）

- `tests/unit/06_wave_pipeline/test_wave_gate_waiver_phase.py::test_cli_declares_waiver_mode_flag`

### `07_docs_skills` 07_docs_skills（失败 4 条）

- `tests/unit/07_docs_skills/test_docs_consistency.py::test_node_registration_audit_is_clean`
- `tests/unit/07_docs_skills/test_sd_portability.py::test_no_author_drive_paths_in_runtime_string_constants`
- `tests/unit/07_docs_skills/test_se_docs.py::test_gm_mode_b_and_quality_estimation_and_emit_ideas_claims_hold`
- `tests/unit/07_docs_skills/test_skill_integrity.py::test_registry_meta_matches_node_signature`

### `08_forum_recon` 08_forum_recon（失败 3 条）

- `tests/unit/08_forum_recon/test_opportunity_scan_xregion.py::test_playable_excludes_all_dead_end_hits`
- `tests/unit/08_forum_recon/test_opportunity_scan_xregion.py::test_playable_excludes_lit_categories`
- `tests/unit/08_forum_recon/test_opportunity_scan_xregion.py::test_playable_excludes_red_family_categories`

### `09_core` 09_core（失败 2 条）

- `tests/unit/09_core/test_index_tables.py::test_env_registry_covers_every_env_var_read_by_code_and_nothing_is_stale`
- `tests/unit/09_core/test_waiver.py::test_policy_defaults_agree_with_code_where_derivable`

## 五、结论与说明

- 通过率 **99.5%**（2850/2863），整体健康。
- 测试引擎与本工作台「测试中心」模块**同源**（均调用 pytest，参数一致），本报告即模块「运行本组」在全部 12 个分组上的汇总体现。
- 并行运行（workers=4）下，少数带共享状态/网络 mock 的用例结果可能与串行略有出入；如需严格串行复现，加 `--workers 1`。
- 业务重点守卫生效验证：组合形态铁律（禁止两条独立信号腿相加，`04_gates/test_gate_equal_weight_leg_add`）、提交层四闸与 SUB 比值闸（`04_gates`）、提交路由 fail-closed 否决权威（`05_submit_quota`、`mcp_pkg/test_submit_verdict_tool_unit`）、双轨同源（`07_docs_skills`）、波次流水线守卫（`06_wave_pipeline`）均有专项用例覆盖。

⚠ 存在 17 失败 / 0 错误，建议优先排查第四节明细对应文件。