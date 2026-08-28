# Skills DB 单轨审计报告（2026-08-25）

范围：`c:\Users\MENGTAO\.qoder-cn\skills` 全树（统一战役后与 trae 侧完全一致，differ=0），全部 `.py` 脚本（排除 .pytest_cache/__pycache__/outputs/tests）。
方法：静态扫描写调用（atomic_write/write_text/json.dump/to_csv/open('w')）× DB 调用（upsert_*/get_store/save_ranking/save_catalog/list_expressions/ledger_kv…），再对全部命中文件逐个人工复核写目标。
判据（AGENTS.md §5 规则0）：战役产物 expressions/gate/ranking/checkpoint/review/batches **只入库**，禁止落 `tracking/*/candidates|cache|results|reviews/*.json|*.csv`。

## 总览

| 分类 | 文件数 | 含义 |
|---|---|---|
| 合规（DB 主轨） | 17 | 核心战役管线全部 DB 单轨，文件写仅限配置引导/显式测试出口 |
| 违规 A（candidates/reference 产物落文件） | 12 | toolkit 11 + inspectRawTemplate 1 |
| 违规 B（体检报告落 tracking/mining） | 2 | ppa-mining / ra-pipeline 各 1 份同名脚本 |
| 设计冲突（文档化 CSV 续跑未入库） | 1 | simAlphasinBatch batch_simulator |
| 无关/设计如此 | ~40 | 凭据会话、API 结果导出、数据集下载缓存、模板流程中间文件、测试夹具、工具函数本身 |

## 合规清单（核心管线，DB 主轨）

| 文件 | 文件写残留 | 判定说明 |
|---|---|---|
| `_lib/wqb_store.py` / `_lib/wave_results.py` / `_lib/registry.py` / `_lib/diversity_extractor.py` | 无 | DB 访问层本身 |
| `build_wave.py` / `diversity_audit.py` / `diversity_slots.py` / `check_ledger_sync.py` | 无 | 纯 DB |
| `scan_fields.py` | 无 | `save_catalog(ctx, cat)` 入库 |
| `diversity_extract.py` | settings/thresholds 缺失时写默认**配置** | 表达式/多样性 upsert 入库 |
| `gate.py` | 仅 `--cache-file` 显式重定向时写缓存文件 | 默认缓存与 gate_results 均入 ledger_kv/gate_results |
| `pipeline.py` | 仅 `--checkpoint-dir` 测试路径写文件 | checkpoint 默认走 `ledger_kv/ckpt_w<W>`（代码注释明示） |
| `review_wave.py` | 仅显式 `--out`（测试） | DB 主轨 |
| `score_datasets.py` | 写 `thresholds.json` **配置**（dataset_health 校准） | ranking/catalog/probe plan 全 DB |
| `enhance_template.py` | `WQB_ENHANCE_SCRATCH` 可选 scratch | `upsert_expressions(status="enhanced")` 主轨 |
| `build_alpha_list.py` | 仅显式 `--out` 兼容出口 | `--from-db` + `save_wave_expressions` 主轨 |
| `run_pipeline.py`（makeSomeGem） | data_dir 工作目录产物（final_expressions.json 等，下游 headless_runner 消费） | `upsert_expressions(status="gem")` + `upsert_idea` 主轨 |
| `_lib/ledger.py` | 旧 JSON 后端保留（已弃用，默认 SqliteLedgerStore） | 向后兼容 |
| `_lib/rules.py` | `WQB_RULES_FILE_ONLY=1` 逃生门 + 一次性文件→DB 迁移 | ledger_kv 主轨 |

## 违规 A：candidates/reference 战役产物仍走文件轨

全部在 `wq-brain-campaign-toolkit/scripts/`（除标注外），写路径均为 `ctx.path("candidates"/"reference", …)` + `atomic_write`，无对应 DB upsert：

| 脚本 | 落盘产物 | 建议去向 |
|---|---|---|
| `build_mix.py` | `candidates/mix_*.json`（混信号候选） | expressions 表（status="mix"） |
| `migrate_templates.py` | `candidates/migrated_*.json` | expressions 表（status="migrated"） |
| `neutralization_sweep.py` | `candidates/settings_sweep_alpha_list.json` + `settings_sweep_plan.json` | expressions 表 + ledger_kv |
| `ortho_prescreen.py` | `candidates/ortho_kept_exprs.json` + `reference/ortho_prescreen_report.json` | expressions 表 + ledger_kv |
| `proxy_prescreen.py` | `candidates/proxy_kept_exprs.json` + `reference/proxy_score_report.json` + `proxy_model_features.json` + joblib 模型 | expressions 表 + ledger_kv（模型文件可豁免为二进制资产） |
| `param_opt.py` | `reference/param_opt_next.json`（TPE 建议） | ledger_kv |
| `param_matrix.py` | 参数矩阵回测结果 JSON ×2（`--no-poll` 与终态） | wave_results/backtest_rows |
| `fit_mix_weights.py` | `reference/mix_weights_fit.json` | ledger_kv |
| `rescue_checklist.py` | `reference/rescue_checklist_<ds>.json` | ledger_kv |
| `harvest.py` | metrics rows JSON（`open(out_path,"w")`） | backtest_rows/metrics 表 |
| `calibrate_probe.py` | `reference/probe_weights_calibrated.json`（另写 thresholds.json 配置——配置部分合理豁免） | ledger_kv |
| `brain-inspectRawTemplate-create-Setting/scripts/resolve_settings.py` | candidates alpha list（"Wrote candidates"） | expressions 表 |

另：`_lib/operator_coverage.py` 的 `save()` 与 L409 payload 落 reference 文件（catalog 写入已是 DB 优先+文件兜底，合规）；覆盖率数据建议入 ledger_kv。

## 违规 B：体检报告默认落共享数据湖

| 脚本 | 问题 |
|---|---|
| `wq-brain-ppa-mining/scripts/dataset_health_check.py` | `--out-dir` 默认 `tracking/mining`，`field_coverage_*.json` 落共享数据湖（AGENTS.md：tracking/mining 勿改动） |
| `wq-brain-ra-pipeline/scripts/dataset_health_check.py` | 同上（同名副本） |

建议：体检结果入 ledger_kv（如 `health_<region>_d<delay>`），文件仅显式 `--out-dir` 时写。

## 设计冲突

| 脚本 | 问题 |
|---|---|
| `brain-simAlphasinBatch-and-track/scripts/batch_simulator.py` | 文档化设计为 `outputs/<stem>_simulation_status.csv` 断点续跑 + `diversity_report.json`/`signal_evidence.json` 落 CSV 同目录。规则0 将 batches 列为 DB-only 产物；该 skill（S3 编排器）与 campaign toolkit 引擎的批次台账双轨并存。建议：批次状态同步 upsert 到 waves/batches 表，CSV 降为导出视图。 |

## 无关/设计如此（豁免，抽样）

- **平台基础设施**：`ace_lib.py`×4（凭据/会话文件）、`helpful_functions.py`×4（alpha PnL/yearly stats API 结果导出）
- **数据下载缓存**：`fetch_dataset.py`×3（数据集 CSV）、`headless_runner/run.py`（数据集拦截 CSV + task meta）、`arxiv_api.py`×2（论文 PDF）
- **模板流程中间文件**（idea→表达式文件流，该技能文档化契约）：`implement_idea.py`×3、`merge_expression_list.py`×3、`enhance_template/scripts/run.py`、`fetch_sim_options.py`、`parse_idea_file.py`
- **评审/分析报告输出**（用户指定输出路径的交付物）：`judge_alpha.py`、`dataset_health_check` 的显式输出
- **本地计算缓存**：`selfcorrQuick/skill.py`（pickle）、`metrics_cache.py`、`gate.py --cache-file`
- **运行时状态**：`adhoc.py`/`ralph_daily_loop.py`/`ralph_runner.py`（runner state）、task `meta.json`
- **论坛工作区**：`brain-forum-browse/*`×4（自有 memory 约定，非 WQ 战役）
- **测试夹具**：`test_*.py`×4（tmp_path 临时目录）
- **工具定义本身**：`_lib/common.py`（atomic_write）

## 结论

核心战役管线（S0 score_datasets → scan_fields → makeSomeGem run_pipeline → build_wave → gate → pipeline → review_wave → diversity/rules/ledger）**已全量 DB 单轨**；文件写残留集中在 toolkit 的 12 个**外围/一次性特征脚本**（mix/ortho/proxy/param*/rescue/harvest/calibrate/migrate/sweep）与 2 份体检脚本、1 个批次模拟器。这些脚本多为低频手工调用，未阻塞主管线单轨，但与规则0 字面冲突，建议按上表"建议去向"列排期整改（每脚本约 10–30 行改动：atomic_write(ctx.path(...)) → st.upsert_ledger/expressions，保留显式 --out 出口）。

## 整改完成状态（2026-08-25 追加）

15 个文件残留脚本全部完成 DB 单轨迁移，经验证（py_compile 16 个脚本 0 失败 + batch_simulator 冒烟 ALL PASS），并同步至 trae 侧 `.trae-cn\skills` 双树 identical（受影响 5 个 skill 目录 differ=0）。

| 分类 | 脚本 | 落库去向（主轨） | 兼容出口 |
|---|---|---|---|
| A1 | `build_mix.py` | expressions 表 status="mix"（新增 `--wave`） | `--out` |
| A2 | `migrate_templates.py` | expressions 表 status="migrated"（`--wave`） | `--out` |
| A3 | `neutralization_sweep.py` | expressions status="sweep" + ledger `settings_sweep_plan` | — |
| A4 | `ortho_prescreen.py` | expressions status="ortho_kept" + ledger `ortho_prescreen_report` | — |
| A5 | `proxy_prescreen.py` | model features→ledger `proxy_model_features`、report→ledger `proxy_score_report`、PASS→expressions status="proxy_kept" | joblib 模型豁免二进制 |
| A6 | `param_opt.py` | ledger `param_opt_next` | `--out` |
| A7 | `param_matrix.py` | ledger `param_matrix_<name>` | `--out` |
| A8 | `fit_mix_weights.py` | ledger `mix_weights_fit` | `--out` |
| A9 | `rescue_checklist.py` | ledger（证据双轨读：DB 优先 + 文件兜底） | `--out` |
| A10 | `harvest.py` | ledger `harvest_<msid>`（文件仅 `--out`） | `--out` |
| A11 | `calibrate_probe.py` | ledger `probe_weights_calibrated`（thresholds.json 配置豁免） | `--out` |
| A12 | `_lib/operator_coverage.py` | ledger（DB 优先 + 文件兜底） | 兜底文件 |
| A13 | `inspectRawTemplate/resolve_settings.py` | ledger（`--out`） | `--out` |
| B1 | `ra-pipeline/dataset_health_check.py` | ledger `health_<region>_d<delay>_<universe>`（`--out-dir` 默认 None） | 显式 `--out-dir` |
| B2 | `ppa-mining/dataset_health_check.py` | 同上 | 显式 `--out-dir` |
| C | `batch_simulator.py` | 续跑真相源→DB ledger（合成桶 BATCH：`sim_batch_<stem>`；结果按区域分桶 `sim_batch_results:<id>`）；死代码 `database/adapter` 通道移除 | CSV 降为导出视图（S4 下游仍读） |

### C（设计冲突）整改要点
原 CSV 断点续跑为唯一真实持久化，`database/adapter` 指向不存在模块（死代码）。现改为：
1. **续跑真相源 = DB ledger**：`_load_state` 优先读 DB（键 `sim_batch_<stem>`，合成桶 `BATCH` 保证无区域上下文可确定性续跑），CSV 仅为导出视图兜底。
2. **结果台账 = DB ledger**：`_save_to_database` 按 alpha 区域分桶写 `sim_batch_results:<id>`；区域经新增 `_extract_region`（settings/settings_json/top-level）提取，缺省 `BATCH`。
3. **增量 + 末次flush**：每次 COMPLETED 后增量 `_persist_resume()`，批结束时再 flush，中断仍以 DB 为真相源。
4. CSV 保留写入（作为导出视图，兼容 S4 `simulation_status.csv` 下游契约）。

**验证**：`py_compile` 16/16 通过；`batch_simulator` 冒烟（`_extract_region` 4 用例 + ledger 幂等回路 + 无状态初始化）ALL PASS。
