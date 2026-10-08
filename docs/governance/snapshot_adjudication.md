# 抢救点独有源码的三态裁决台账（snapshot adjudication）

> **本文件由 `tools/code-audit/snapshot_adjudicate.py --apply` 生成，请勿手改正文表**；
> 要改裁决请改 `tests/fixtures/snapshot_adjudication.json`（人工依据的唯一入口），再重跑生成。
> 上位文档：[`branch_policy.md`](branch_policy.md)（取件纪律与抢救点清单）。

> ⚠ **本文件是清单，不是路径承诺**：表里绝大多数路径**按定义就不在工作区**（它们只在对象库的某个快照里）。因此 `tools/code-audit/doc_path_refs.py` 把本文件归为**非活文档**，不对它做死指针判定（实测当活文档扫会新增 542 条假 BROKEN，把闸顶成永久红）；本文件自身的一致性由它自己的生成器守：`snapshot_adjudicate.py --check`，并由 `tests/unit/07_docs_skills/test_governance_gates_selfcheck.py` 在 pre-commit 里拦过期台账。

## 0. 这份台账解决什么问题

抢救点（`preserve/*` tag；如出现 `wip/*` 分支也一并纳入）里有一批「对象库有、`main` 没有」的源码与文档。
2026-10-06 治理评审的实测缺口：那串以「恢复丢失的源码 / P4 收尾」为标题的提交只裁决了 6 件，
其余**无台账、无裁决、无闸**。本文件把「有没有人判过」变成可校验的读数：
`PENDING` 必须归零；新增一件独有文件而没人裁决，`--check` 即红（守护测试见 `tests/unit/07_docs_skills/test_snapshot_adjudication.py`）。

## 1. 三态口径（不得自造第四态）

| 态 | 含义 | 判据 |
|---|---|---|
| `RESTORED` | 已取回 `main` | 本次或历次治理已 checkout 并入库，留痕用 |
| `DROPPED` | 裁决**不回迁** | 零活动引用 / 职责已被现通道覆盖 / 属未合入工作线且单件回迁会造悬空依赖；**逐件必须写依据**。另含一类**机械判定**：路径重组且 blob 逐字相等（件未丢失，只是搬过目录） |
| `ARTIFACT` | 运行产物 / 数据转储 | 可重跑的 dump、断点、缓存；不是「人的结论」，不入库 |
| `PENDING` | 待人工裁决 | 代码 / 文档 / 结论类资产且尚无人判过 —— **这一态非 0 就是欠债** |

## 2. 读数

- 清单总数（所有抢救点 ∪ 未跟踪父提交，减去 `main`）：**845**
- `RESTORED` = 0；`DROPPED` = 102；`ARTIFACT` = 216；`PENDING` = 527
- fixture 与清单逐件对应，无陈旧条目

取数口径（两条腿都要，只取受跟踪部分会漏关键依赖 —— 本仓已踩过）：

```bash
git ls-tree -r --name-only <ref>       # 受跟踪树
git ls-tree -r --name-only <ref>^3     # stash 式快照的未跟踪父提交
```

## 3. 逐件表

### 3.2 `DROPPED`（102 件）

| 路径 | 依据 | 来源 |
|---|---|---|
| `Claude/skills/brain-alpha-judge/references/future-improvement-guide.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/judge_planning_docs_20260929/future-improvement-guide.md`（blob 相等） | rule |
| `Claude/skills/brain-alpha-judge/references/improvement-roadmap.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/judge_planning_docs_20260929/improvement-roadmap.md`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/DIVERSITY_EXTRACT_QUICKSTART.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_docs_20260929/DIVERSITY_EXTRACT_QUICKSTART.md`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/DIVERSITY_EXTRACT_README.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_docs_20260929/DIVERSITY_EXTRACT_README.md`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/DIVERSITY_EXTRACT_SUMMARY.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_docs_20260929/DIVERSITY_EXTRACT_SUMMARY.md`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/references/enhancement-v2.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_docs_20260929/enhancement-v2.md`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/prescreen.py` | main 侧调用通道尚未接线：`src/wqb/workflow/_common.py:274 resolve_toolkit_file()` 全仓**零调用方**（`git grep 'resolve_toolkit_file(' -- src tools` 只命中其定义），其 docstring 提到本文件只是为了说明「安装位可能滞后于仓库副本」。因此缺它不产生任何故障，回迁也不会生效 —— 属同一条预筛线，接线时成套取。 | human |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/budget_planner.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/budget_planner.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/campaign_mutex.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/campaign_mutex.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/composition_validator.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/composition_validator.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/distill_experience.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/distill_experience.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/family_atlas.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/family_atlas.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/os_feedback.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/os_feedback.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/signal_classifier.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/toolkit_zero_ref_20260928/signal_classifier.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-ra-pipeline/scripts/dataset_health_check.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/ra_pipeline_shell_20260928/dataset_health_check.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-ra-pipeline/scripts/ralph_daily_loop.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/ra_pipeline_shell_20260928/ralph_daily_loop.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-ra-pipeline/scripts/ralph_runner.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/ra_pipeline_shell_20260928/ralph_runner.py`（blob 相等） | rule |
| `Claude/skills/wq-brain-ra-pipeline/templates/daily_state.template.json` | 路径重组，件未丢失：main 已有内容逐字相同的 `attic/ra_pipeline_shell_20260928/daily_state.template.json`（blob 相等） | rule |
| `docs/operator_modeb_research.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `docs/design/operator_modeb_research.md`（blob 相等） | rule |
| `docs/skills_pipeline_analysis.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `docs/design/skills_pipeline_analysis.md`（blob 相等） | rule |
| `docs/skills_pipeline_optimization.md` | 路径重组，件未丢失：main 已有内容逐字相同的 `docs/design/skills_pipeline_optimization.md`（blob 相等） | rule |
| `reports/operator_usage_audit.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/operator_usage_audit.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/operator_usage_audit.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/operator_usage_audit.py`。 | human |
| `reports/opswap_analyze.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/opswap_analyze.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/opswap_analyze.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/opswap_analyze.py`。 | human |
| `reports/opswap_build_plan.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/opswap_build_plan.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/opswap_build_plan.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/opswap_build_plan.py`。 | human |
| `reports/opswap_driver.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tools/legacy/opswap_driver.py`（blob 相等） | rule |
| `src/wqb/dataset_pair_matrix.py` | main 侧零消费方：`git grep 'get_dataset_pair_recommendations\|dataset_pair_matrix' -- src tools` = 0 命中；唯一提及处 `tests/unit/02_workflow/test_inventory_scan_basket_shape.py:38` 写的是 `try: import … except ImportError: dpm = None`，即节点已按「该模块可能不存在」设计。单件回迁会**静默启用一个未经评审的功能**（跨数据集对推荐），属危险方向。配套 `tests/unit/test_dataset_pair_matrix.py` 同线。要启用请整线取回并补 registry/README 登记。 | human |
| `src/wqb/semantic_ledger.py` | 属「S1 语义自动补做」整条未合入工作线，单件回迁即造孤儿模块：其文档明列的两个消费方在 main 都不存在（`git grep '_semantic_coverage_check' -- src tools` = 0 命中；`tools/field_semantic_classify.py` 的产物 schema 里根本没有 `families`/`family_stats` 键，见其 L200-L212）。main 侧读同一台账键的是 `tools/wave_gate_pkg/gates_semantic.py`，它只用 `blocked_fields`，不需要 `ledger_has_l35`。配套件同属该线：`tests/unit/02_workflow/test_s1_semantic_autoclassify.py`、`tests/unit/10_toolkit_scripts/test_semantic_classify_all.py`、`test_semantic_field_pool_filter.py`。⚠ 更正记录：HEAD 曾按「全仓从未存在」结案，那是把「工作区/`git ls-files` 没有」当成「对象库没有」——实测 `git cat-file -s 4910e65:src/wqb/semantic_ledger.py` = 2407 字节。证据留在抢救点，取回须**整线成套**。 | human |
| `src/wqb/workflow/nodes/_campaign_open_gates.py` | main 零引用：`git grep 'campaign_open_gates' -- src tools tests` = 0 命中，且 `src/wqb/workflow/registry.py` 未注册其节点。回迁即造「代码里有、链路上不跑」的幽灵模块（本仓对 workflow 节点有五处同步登记纪律，单文件回迁必然漂移）。 | human |
| `tests/unit/01_store_db/test_corr_single_source.py` | 它断言的是 `_corr_cache.py` 的**第三版契约**，而该实现无论在 main 还是在快照里都不存在：实测 `git show 05b64a6:src/wqb/store/_corr_cache.py` 的 `normalize_corr_source()` 返回 `{"source","detail"}` 且 `_LEGACY_SOURCE_ALIASES` 把 `prod_first` 映射到 `prod_first_screen`；测试却要求 `CORR_FRESH_SECONDS`、`source_detail`、并把 6 个自由文本一律收敛到 `platform_sync`。按 pathspec 取回 = 当场 7 红（`ImportError: CORR_FRESH_SECONDS`），且会把一条未完成的契约伪装成「守卫测试」。顶层符号比对显示 main 的 `_corr_cache.py` 是快照版的超集（多出 `get_corr_authoritative_batch`），故该件属未合入分叉线 —— 由该线所有者整线合并，不做单件回迁。 | human |
| `tests/unit/test_backlog_gate_unconsumed_p0p2.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/06_wave_pipeline/test_backlog_gate_unconsumed_p0p2.py`（blob 相等） | rule |
| `tests/unit/test_batch_submit_verdict_phase2.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/05_submit_quota/test_batch_submit_verdict_phase2.py`（blob 相等） | rule |
| `tests/unit/test_dataset_pair_matrix.py` | 被测对象 `src/wqb/dataset_pair_matrix.py` 不在 main（见该件裁决），回迁即造 collection 期 ImportError。与 subject 同线成套取回。 | human |
| `tests/unit/test_handoff.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/09_core/test_handoff.py`（blob 相等） | rule |
| `tests/unit/test_memory.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/09_core/test_memory.py`（blob 相等） | rule |
| `tests/unit/test_n35_reharvest_state_preservation.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/01_store_db/test_n35_reharvest_state_preservation.py`（blob 相等） | rule |
| `tests/unit/test_observability.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/09_core/test_observability.py`（blob 相等） | rule |
| `tests/unit/test_region_gates_p0p1.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/01_store_db/test_region_gates_p0p1.py`（blob 相等） | rule |
| `tests/unit/test_scheduler.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/09_core/test_scheduler.py`（blob 相等） | rule |
| `tests/unit/test_search.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/09_core/test_search.py`（blob 相等） | rule |
| `tests/unit/test_stop_rules_axis_scope.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/06_wave_pipeline/test_stop_rules_axis_scope.py`（blob 相等） | rule |
| `tests/unit/test_stop_rules_verdict_p0p3.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/06_wave_pipeline/test_stop_rules_verdict_p0p3.py`（blob 相等） | rule |
| `tests/unit/test_wave_key_contract.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tests/unit/06_wave_pipeline/test_wave_key_contract.py`（blob 相等） | rule |
| `tools/_db_fk_fix.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/_db_fk_fix.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/_db_fk_fix.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/_db_fk_fix.py`。 | human |
| `tools/_db_p0_fix.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/_db_p0_fix.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/_db_p0_fix.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/_db_p0_fix.py`。 | human |
| `tools/_db_quality_check.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 2（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-01。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/_db_quality_check.py`。 | human |
| `tools/_kor_s6_writeback.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tracking/KOR/scripts/_kor_s6_writeback.py`（blob 相等） | rule |
| `tools/archive_json_files.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/data-repair/archive_json_files.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/data-repair/archive_json_files.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/data-repair/archive_json_files.py`。 | human |
| `tools/archive_json_to_attic.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/data-repair/archive_json_to_attic.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/data-repair/archive_json_to_attic.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/data-repair/archive_json_to_attic.py`。 | human |
| `tools/backfill_alpha_metrics.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/data-repair/backfill_alpha_metrics.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/data-repair/backfill_alpha_metrics.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/data-repair/backfill_alpha_metrics.py`。 | human |
| `tools/backfill_backtest_dataset.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tools/legacy/backfill_backtest_dataset.py`（blob 相等） | rule |
| `tools/backfill_expression_status_once.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/backfill_expression_status_once.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/backfill_expression_status_once.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/backfill_expression_status_once.py`。 | human |
| `tools/check_ledger_sync.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tools/ledger/check_ledger_sync.py`（blob 相等） | rule |
| `tools/convert_alpha_list_to_exprs.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/fields/convert_alpha_list_to_exprs.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/fields/convert_alpha_list_to_exprs.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/fields/convert_alpha_list_to_exprs.py`。 | human |
| `tools/data-repair/archive_json_files.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/data-repair/archive_json_files.py`。 | human |
| `tools/data-repair/archive_json_to_attic.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 2（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/data-repair/archive_json_to_attic.py`。 | human |
| `tools/data-repair/backfill_alpha_metrics.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/data-repair/backfill_alpha_metrics.py`。 | human |
| `tools/data-repair/backfill_alphas_from_ckpt.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/data-repair/backfill_alphas_from_ckpt.py`。 | human |
| `tools/direct_submit.py` | 2026-10-06 §5.3 逐件核验（`docs/governance/branch_policy.md`）：全仓只命中治理文档自身；`tools/wave_gate.py`·`quality_predict.py` 里的 `direct_submit` 是 `qp_summary["direct_submit"]` 计数字段键；`DIRECT_CONNECT_WHITELIST`（7 项，有 `test_db_write_guards.py::test_whitelist_files_exist` 断言）不含它；提交链已由 MCP `workflow_submit_alpha` + `tools/super_build.py submit` 覆盖。已同时登记进 `audit_structure_baseline.json` 的 `retired_paths`（S12 拦复活）。 | human |
| `tools/fields/convert_alpha_list_to_exprs.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/fields/convert_alpha_list_to_exprs.py`。 | human |
| `tools/fix_stale_fk_20260928.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tools/legacy/fix_stale_fk_20260928.py`（blob 相等） | rule |
| `tools/fix_submit_ready_check_20260928.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/fix_submit_ready_check_20260928.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/fix_submit_ready_check_20260928.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/fix_submit_ready_check_20260928.py`。 | human |
| `tools/harvest_batch.py` | §5.3：`pipeline.py` 里的 `_harvest_batch_alphas` 是本地函数非该脚本；收批已统一走 `tools/harvest_multisim.py`（多 multisim 批量收）。零活动引用。已登记 retired_paths。 | human |
| `tools/harvest_by_expr.py` | §5.3：零活动引用；按表达式收批的需求已由 `tools/harvest_multisim.py` 覆盖。已登记 retired_paths。 | human |
| `tools/hkg_d1_model_probe.py` | 2026-10-06 用户主动退役（同批还有 probe2 / triage_platform_status_sweep_v3 / verify_ready8）。引用面实测：除历史面外全仓命中只剩 `tools/THEMES.json` 与 `tools/audit_structure_baseline.json` 两处登记痕迹（code=0 doc=0 test=0），即**零活动引用**。已 `git rm` 并连带把 `s11_tools_top_level` 159→155、`retired_paths` 17→21（S12 拦复活）、THEMES `probe.files` 与 `counts`/`top_n` 同步收紧。不搬 `attic/`：`.gitignore:87` 整目录忽略 `attic/`，搬过去等于造出「未跟踪源码」新债。取看：`git show b62447f:tools/hkg_d1_model_probe.py`。 | human |
| `tools/hkg_d1_model_probe2.py` | 同上批：零活动引用（只剩 THEMES/基线登记痕迹），2026-10-06 `git rm` 退役并登记 `retired_paths`。probe2 是 probe 的第二版变体，两者职责已被 `tools/probe/` 主题目录下的现役探针覆盖。取看：`git show b62447f:tools/hkg_d1_model_probe2.py`。 | human |
| `tools/kor_ledger_write.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tracking/KOR/scripts/kor_ledger_write.py`（blob 相等） | rule |
| `tools/kor_spre_read.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tracking/KOR/scripts/kor_spre_read.py`（blob 相等） | rule |
| `tools/legacy/_db_fk_fix.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-30。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/_db_fk_fix.py`。 | human |
| `tools/legacy/_db_p0_fix.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-30。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/_db_p0_fix.py`。 | human |
| `tools/legacy/backfill_2y_six.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/backfill_2y_six.py`。 | human |
| `tools/legacy/backfill_expression_status_once.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-05。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/backfill_expression_status_once.py`。 | human |
| `tools/legacy/backfill_fingerprints.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/backfill_fingerprints.py`。 | human |
| `tools/legacy/calibrate_q3_alphas.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-25。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/calibrate_q3_alphas.py`。 | human |
| `tools/legacy/corr_batch_head_candidates.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-25。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/corr_batch_head_candidates.py`。 | human |
| `tools/legacy/death_level.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-25。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/death_level.py`。 | human |
| `tools/legacy/fix_submit_ready_check_20260928.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-30。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/fix_submit_ready_check_20260928.py`。 | human |
| `tools/legacy/migrate_campaign_state.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/migrate_campaign_state.py`。 | human |
| `tools/legacy/migrate_db_schema.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/migrate_db_schema.py`。 | human |
| `tools/legacy/migrate_field_validation.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/migrate_field_validation.py`。 | human |
| `tools/legacy/migrate_ideas_to_db.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/migrate_ideas_to_db.py`。 | human |
| `tools/legacy/n1qmj_decorrelate_variants.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-25。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/n1qmj_decorrelate_variants.py`。 | human |
| `tools/legacy/operator_usage_audit.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-30。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/operator_usage_audit.py`。 | human |
| `tools/legacy/opswap_analyze.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-30。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/opswap_analyze.py`。 | human |
| `tools/legacy/opswap_build_plan.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-30。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/opswap_build_plan.py`。 | human |
| `tools/legacy/submit_883wzj1w.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/submit_883wzj1w.py`。 | human |
| `tools/legacy/submit_883wzj1w_writeback.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/submit_883wzj1w_writeback.py`。 | human |
| `tools/legacy/sync_reference.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-05。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/sync_reference.py`。 | human |
| `tools/legacy/triage_pass4_check.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/triage_pass4_check.py`。 | human |
| `tools/legacy/triage_platform_status_sweep.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/triage_platform_status_sweep.py`。 | human |
| `tools/legacy/triage_salvage_neut.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/triage_salvage_neut.py`。 | human |
| `tools/legacy/triage_salvage_top300.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/triage_salvage_top300.py`。 | human |
| `tools/legacy/triage_softdelete_batch1.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 0（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-09-20。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/legacy/triage_softdelete_batch1.py`。 | human |
| `tools/parse_simresult.py` | 路径重组，件未丢失：main 已有内容逐字相同的 `tools/backtest/parse_simresult.py`（blob 相等） | rule |
| `tools/probe/prod4_quick.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/probe/prod4_quick.py`。 | human |
| `tools/probe/prod_scan.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/probe/prod_scan.py`。 | human |
| `tools/research/neutralization_scan.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/research/neutralization_scan.py`。 | human |
| `tools/rotation/region_whitelist.py` | 2026-10-06 `tools/` 批量规范退役（第 2 批 35 件之一）。引用面实测：活代码 import / 子进程路径 = 0；真实测试断言 = 0（按修正口径重查，只看 tests/**/test_*.py）；活 SOP 命令引用 = 0；文档面只剩名录/历史 = 0；配置登记 = 1（THEMES/基线）；历史报告命中 = 0。最后一次内容提交 2026-10-04。走 git rm 而非搬 attic/（`.gitignore` 整目录忽略 attic/，搬过去=造未跟踪源码新债）；已登记 retired_paths 由 S12 拦复活。取看：`git show f58ddc3:tools/rotation/region_whitelist.py`。 | human |
| `tools/self_batch.py` | §5.3：零活动引用；self 侧走 MCP `check_self_correlation` 与 skill `brain-calculate-alpha-selfcorr-quick`。已登记 retired_paths。 | human |
| `tools/sync_reference.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/legacy/sync_reference.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/legacy/sync_reference.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/legacy/sync_reference.py`。 | human |
| `tools/triage_platform_status_sweep_v3.py` | 零活动引用（`tools/legacy/README.md` L79 那行是退役记录本身，不是调用）。`tools/legacy/README.md` 当时写的是临时保留理由（「并发会话在飞、避免误删」，mtime 2026-09-24），已于 2026-10-06 追认完成并改写为退役记录。存量分诊/状态横扫的职责已由 `tools/triage_*` 现役脚本与 `prod_blocked_recheck.py` 覆盖。取看：`git show b62447f:tools/triage_platform_status_sweep_v3.py`。 | human |
| `tools/verify_ready8.py` | 零活动引用（只剩 THEMES/基线登记痕迹）。名字里的 ready8 是 2026-09 某批候选的一次性核对手套，不属于任何现役链（提交判定走 `tools/verdict/submit_inventory.py` 与 `wqb.submit_verdict_core`，AGENTS.md §3.5 已写明后者是否决权威）。取看：`git show b62447f:tools/verify_ready8.py`。 | human |
| `tracking/EUR/scripts/backfill_alphas_from_ckpt.py` | 同一件在快照里的**旧顶层路径**（退役当时它位于 `tools/data-repair/backfill_alphas_from_ckpt.py`，2026-10-06 随批量规范退役 `git rm`）。判据与依据同 `tools/data-repair/backfill_alphas_from_ckpt.py` 那条：五种引用形态（import/路径、无后缀调用、动态导入、字符串表、真实测试断言）实测全为 0，见 docs/governance/branch_policy.md §5.4。取看：`git show f58ddc3:tools/data-repair/backfill_alphas_from_ckpt.py`。 | human |

### 3.3 `ARTIFACT`（216 件）

| 路径 | 依据 | 来源 |
|---|---|---|
| `output_report/py_complexity_scan.json` | output_report/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w10.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w11.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w12.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w13.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w14.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w15.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w16.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w17.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w18.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w19.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w20.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w21.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w3.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w4.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w5.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w6.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w7.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/exprs_asi_w8.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w1.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w10.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w11.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w12.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w13_industry.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w13_market.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w14.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w15.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w16_tr006.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w17.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w18.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w19_d20.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w19_d28.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w1_sector.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w2.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w20.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w21_minvol10m.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w21_top500.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w2_sector.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w3.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w4.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w5.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w6.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w8.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/probe_asi_w9_market.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/s2_intraday_pv_feats_d1_selected.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/ASI/candidates/s2_ipv_corr_volume_v1.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/DEU/candidates/DEAD_ENDS.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/DEU/candidates/probe_deu_shrt3_w13.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/DEU/candidates/wave_DEUDUAL2_checkpoint.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/DEU/candidates/wave_DEUDUAL2_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/DEU/candidates/wave_DEUDUAL_checkpoint.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/DEU/candidates/wave_DEUDUAL_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/DEAD_ENDS_pattern_scores.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag1_s1.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag1_subind.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag2_subind.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag3_sub.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag4_sub.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag5_sub.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag6_grid.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag7_decay.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag8_2y.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_diag9_final.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_pattern_p01.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/EUR/candidates/probe_eur_wiki_v1.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/FORUM/forum_recon_cache.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/GLB/reports/glb_10tower_viable_20261002.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/GLB/scripts/_serial_s23_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s24_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s25_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s26_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s27_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s28_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s29_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s30_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s31_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s32_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s33_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLB/scripts/_serial_s34_ckpt.json` | 断点 / 缓存 / 报表类运行产物 | rule |
| `tracking/GLOBAL/config/field_count_strategy.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/IND/candidates/probe_ind_pv_w12.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/kor_si_all_fields.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/kor_si_pool.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w1_d30.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w2_d30c.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w3_neg.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w4_neg.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w5.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w6_dirsplit.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w7.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_insd5_w8.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_inst6.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_inst6_all.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_risk_w14.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/probe_kor_sent_w15_fast.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/prod_measure_si12.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3B_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3_exprs.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3_modeA.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3_modeA_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3_probe_design.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_AL3_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_CROSSFIELD_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_CROSS_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_DECOUPLE2_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_DECOUPLE3_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_DECOUPLE4_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_DECOUPLE_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_FINAL_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_HUMP2_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_HUMP3_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_HUMP4_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_HUMP_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RATIOC_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RATIOD_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RATIOE_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RATIO_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RSK59B2_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RSK59B_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_RSK59_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SHORTSELL_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI10_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI11_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI12_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI12_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI13_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI13_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI14_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI14_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI15_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI15_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI16_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI16_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI17_results.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI17_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI38AGG_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI3M_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI3U_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI3_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI4_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI5_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI6_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI7_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI8_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SI9_submitted.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/KOR/candidates/wave_SIFINAL_ledger.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/PPA_USA/README.md` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/PPA_USA/handoff_2rmEZlKx.md` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/PPA_USA/handoff_mL6Ozm72.md` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/PPA_USA/handoff_zqbaoRwR.md` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/USA/other466_semantic_classify.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/USA/reference/usa_generation_constraints.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/mining/field_inspect_deu_pattern_scores.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_deu_pv30.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_kor_model56.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_kor_other106.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_kor_other395.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_kor_shortinterest38.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_usa_analyst_consensus.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_usa_insiders3.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_usa_order_flow_imb.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_usa_other699.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/mining/field_inspect_usa_shortinterest29.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_all_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_asi_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_asi_nofail.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_deu_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_gbr_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_glb_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_ind_1358_all.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_ind_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_ind_inst6.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_ind_w12.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/ids_kor_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_asi_nofail.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_deu_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_gbr_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_ind_1358_all.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_ind_inst6.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_ind_w12.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/prod_kor_261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/pyramid_asi261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/prod_probe/pyramid_ind261.json` | 运行期数据目录（可重跑 / 探针 dump） | rule |
| `tracking/reference/EUR_other571_fields.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/EUR_pattern_scores_fields.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/ds_category_map.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_deu_shrt3_w13.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_diag1.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_diag2.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_diag3.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_diag4.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_diag5.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_pattern.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_eur_wiki.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_ind_pv_w12.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w1.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w2.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w3.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w4.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w5.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w6.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w7.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w8.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_insd5_w9.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_inst6_all.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_inst6_w11.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_institutions6.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_risk_w14.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/exprs_kor_sent_w15.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/fields_KOR_insiders5.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/kor_strong_fields.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/pyramid_state_20260929.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/round_status_20260929.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/strong_ds_scan.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |
| `tracking/reference/zero_competition_scan.json` | tracking/ 下的 .json 运行产物（可重跑） | rule |

### 3.4 `PENDING`（527 件）

| 路径 | 依据 | 来源 |
|---|---|---|
| `Claude/skills/brain-alpha-research/references/webdatascope-data-quality.md` | 同名件在 main 是 `Claude/skills/brain-alpha-research-field-quality/references/webdatascope-data-quality.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-explain-alphas/scripts/arxiv_api.py` | 同名件在 main 是 `Claude/skills/wq-brain-alpha-optimization-v1/scripts/arxiv_api.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/contribution-and-diversity.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/contribution-and-diversity.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/evidence-and-review.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/evidence-and-review.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/mcp-by-phase.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/mcp-by-phase.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/mcp-tools-and-search.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `Claude/skills/brain-forum-browse/references/modes-and-contract.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/modes-and-contract.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/quotas-and-cooldown.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/quotas-and-cooldown.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/recon-and-gap.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/recon-and-gap.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/workspace-and-memory.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/workspace-and-memory.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/references/write-style-zh.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/write-style-zh.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/templates/forum_findings.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/templates/write-path/forum_findings.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/brain-forum-browse/templates/run_contract.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/templates/write-path/run_contract.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/wq-brain-alpha-optimization-v1/scripts/.arxiv_cache.json` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `Claude/skills/wq-brain-campaign-toolkit/references/S2_COMPLIANCE_CHECKLIST.md` | 同名件在 main 是 `attic/toolkit_docs_20260929/S2_COMPLIANCE_CHECKLIST.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/wq-brain-campaign-toolkit/references/S2_COMPLIANCE_GUIDE.md` | 同名件在 main 是 `attic/toolkit_docs_20260929/S2_COMPLIANCE_GUIDE.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/wq-brain-campaign-toolkit/references/rules-declarative-injection.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `Claude/skills/wq-brain-campaign-toolkit/tests/test_enhance_v2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `Claude/skills/wq-brain-ppa-mining/scripts/dataset_health_check.py` | 同名件在 main 是 `attic/ppa_mining_20260929/dataset_health_check.py`, `attic/ra_pipeline_shell_20260928/dataset_health_check.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `Claude/skills/wq-brain-superalpha/references/selection-playbook.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `docs/design_s1_family_deadend.md` | 同名件在 main 是 `docs/design/design_s1_family_deadend.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/modeb_operator_optimization_plan.md` | 同名件在 main 是 `docs/design/modeb_operator_optimization_plan.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/prod_corr_persistence_design_20260918.md` | 同名件在 main 是 `docs/design/prod_corr_persistence_design_20260918.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/reference/brain-labs-data-analysis-agent.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `docs/skills-optimization-roadmap.md` | 同名件在 main 是 `docs/design/skills-optimization-roadmap.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/skills_review_decisions.md` | 同名件在 main 是 `docs/design/skills_review_decisions.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/structural_reconstruction.md` | 同名件在 main 是 `docs/design/structural_reconstruction.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/structural_reconstruction_integration.md` | 同名件在 main 是 `docs/design/structural_reconstruction_integration.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/submit_queue_design.md` | 同名件在 main 是 `docs/design/submit_queue_design.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `docs/submittable_alpha_optimization.md` | 同名件在 main 是 `docs/design/submittable_alpha_optimization.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `output_report/EUR_wave269_campaign_report.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/GLB_RA_campaign_20260919_S-PRE_to_S1.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/db_quality_assessment_20260928.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/eur_2y_sharpe_raise_methodology_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/eur_new_category_progress_20261005.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/eur_risk70_metric_tuning_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/factor_optimization_potential_20260928.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/gbr_analyst47_tvr_decay_verdict_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/gbr_campaign_progress_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/gbr_forum_literature_recon_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/gbr_model_category_mining_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/gbr_trackA_verdict_trackB_wave1_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/ind_other532_reversal_campaign_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/l4_eur_other460_hypotheses_20261001.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/org_audit_20261001.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/py_file_audit_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/pyramid_tower_report.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/ra_pipeline_stage_audit_20260916_v3.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/skills_fix_plan_20261003.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/skills_review_20261003.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/skills_stage_review_20261001.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/step9_s6_evaluation_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/ts_max_usage_audit.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/usa_analyst_breakthrough_20261004_s2.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/usa_analyst_category_report_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/usa_campaign_report_20261003.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/wq_forum_posting_analysis.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/wq_full_test_report_20261001_1115.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `output_report/wq_full_test_report_20261001_1116.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/README.md` | 同名件在 main 是 `Claude/skills/brain-forum-browse/references/write-path/README.md`, `Claude/skills/brain-make-some-gem/scripts/headless_runner/README.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `reports/d9_status_backfill_rollback_20261005.json` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/dataset_experience/asi_continuation_score_campain.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/dataset_experience/asi_model28_campain.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/dataset_experience/asi_pattern_scores_campain.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/dataset_experience/asi_pv13_campain.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/db_schema_audit_2026-08-26.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/db_table_structure_review_2026-08-26.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/feature_engineering_eval_2026-08-27.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/forum-experience/alpha_templates_forum_2026-08-05.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/forum-experience/glb_forum_experience_2026-08-05.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/forum-experience/ppa_forum_experience_2026-08-07.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/forum_alpha_inspiration_taxonomy_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/forum_to_skills_integration_plan_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/project-audit/progress_2026-08-15.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/structure_review_20261004.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/temp_and_deadcode_scan_2026-08-28.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/tmp_cleanup_2026-08-30.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `reports/toolkit_usage_review_2026-08-31.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_build_wave_family_probe.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_dataset_meta.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_region_catalog.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_select_ra_basket_exclude_dead.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_semantic_field_pool_filter.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_submit_queue_mark_blocked.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_towers.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/01_store_db/test_whitelist_write_guard.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/02_workflow/test_pipeline_submit_retry_completeness.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/02_workflow/test_s1_semantic_autoclassify.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/04_gates/test_s0_viability_p7.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/05_submit_quota/test_quota_typing_unit.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/06_wave_pipeline/test_recent_closed_waves_window.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/06_wave_pipeline/test_s4_walls_prescreen_20261002.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/06_wave_pipeline/test_s6_events_instrumentation_20261002.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/07_docs_skills/test_methodology_rules_connectivity.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/07_docs_skills/test_no_dilution_rules.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/09_core/test_semantic_ledger.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/10_toolkit_scripts/test_probe_batch_exempts_diversity.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/10_toolkit_scripts/test_semantic_classify_all.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/10_toolkit_scripts/test_slots_is_full_refill.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/10_toolkit_scripts/test_step9_audit.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/10_toolkit_scripts/test_submit_inventory_classify.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tests/unit/test_alpha_properties_patch_partial.py` | 同名件在 main 是 `tests/unit/02_workflow/test_alpha_properties_patch_partial.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_audit_fixes.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_audit_fixes.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_auth_transient_retry.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_auth_transient_retry.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_backlog_drop_guard.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_backlog_drop_guard.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_batch_status_auth.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_batch_status_auth.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_batch_status_watch_transient.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_batch_status_watch_transient.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_brain_alpha_repair_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_brain_alpha_repair_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_build_wave_selection.py` | 同名件在 main 是 `tests/unit/01_store_db/test_build_wave_selection.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_campaign_intel_20260919_landing.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_campaign_intel_20260919_landing.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_campaign_intel_mark_saturated.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_campaign_intel_mark_saturated.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_campaign_intel_prod_first.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_campaign_intel_prod_first.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_campaign_intel_s0_rank_p1.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_campaign_intel_s0_rank_p1.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_campaign_prompt_commands_p4.py` | 同名件在 main 是 `tests/unit/02_workflow/test_campaign_prompt_commands_p4.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_catalog_gate_p3.py` | 同名件在 main 是 `tests/unit/04_gates/test_catalog_gate_p3.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_category_field_triage_b.py` | 同名件在 main 是 `tests/unit/01_store_db/test_category_field_triage_b.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_closure_ledger.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_closure_ledger.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_cluster_variants.py` | 同名件在 main 是 `tests/unit/04_gates/test_cluster_variants.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_concept_overlap.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_concept_overlap.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_concept_taxonomy_map.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_concept_taxonomy_map.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_config.py` | 同名件在 main 是 `tests/unit/09_core/test_config.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_dataset_experience.py` | 同名件在 main 是 `tests/unit/09_core/test_dataset_experience.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_db_wave_membership.py` | 同名件在 main 是 `tests/unit/01_store_db/test_db_wave_membership.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_db_write_guards.py` | 同名件在 main 是 `tests/unit/01_store_db/test_db_write_guards.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_dblock_dead_holder.py` | 同名件在 main 是 `tests/unit/01_store_db/test_dblock_dead_holder.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_dead_end_forum_gate.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_dead_end_forum_gate.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_detached_first_output_heartbeat.py` | 同名件在 main 是 `tests/unit/02_workflow/test_detached_first_output_heartbeat.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_diagnostics.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_diagnostics.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_diversity.py` | 同名件在 main 是 `tests/unit/09_core/test_diversity.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_docs_consistency.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_docs_consistency.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_experience_kb_refs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_experience_kb_refs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_expression_status.py` | 同名件在 main 是 `tests/unit/01_store_db/test_expression_status.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_field_semantic_classify.py` | 同名件在 main 是 `tests/unit/09_core/test_field_semantic_classify.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_forum_cache_builder_paths.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_forum_cache_builder_paths.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_forum_recon.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_forum_recon.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_forum_recon_node.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_forum_recon_node.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_forum_recon_wave.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_forum_recon_wave.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gate5_coverage_matrix.py` | 同名件在 main 是 `tests/unit/04_gates/test_gate5_coverage_matrix.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gate_equal_weight_leg_add.py` | 同名件在 main 是 `tests/unit/04_gates/test_gate_equal_weight_leg_add.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gate_region_invalid_group_fields.py` | 同名件在 main 是 `tests/unit/04_gates/test_gate_region_invalid_group_fields.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gate_registry_docs.py` | 同名件在 main 是 `tests/unit/04_gates/test_gate_registry_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gem_console_watch.py` | 同名件在 main 是 `tests/unit/03_gem/test_gem_console_watch.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gem_group_fields.py` | 同名件在 main 是 `tests/unit/03_gem/test_gem_group_fields.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gem_pregate_platform_constraints.py` | 同名件在 main 是 `tests/unit/03_gem/test_gem_pregate_platform_constraints.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gem_provenance_p1p2p3.py` | 同名件在 main 是 `tests/unit/03_gem/test_gem_provenance_p1p2p3.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gem_repeated_placeholder.py` | 同名件在 main 是 `tests/unit/03_gem/test_gem_repeated_placeholder.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_gem_skill_paths.py` | 同名件在 main 是 `tests/unit/03_gem/test_gem_skill_paths.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ghost_operator_lists.py` | 同名件在 main 是 `tests/unit/09_core/test_ghost_operator_lists.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_glossary_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_glossary_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_grammar.py` | 同名件在 main 是 `tests/unit/09_core/test_grammar.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_harvest_checks_path.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_harvest_checks_path.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_harvest_longcount_fields.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_harvest_longcount_fields.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_harvest_multisim_retry.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_harvest_multisim_retry.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_harvest_multisim_transient_retry.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_harvest_multisim_transient_retry.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_how_to_pass_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_how_to_pass_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_index_tables.py` | 同名件在 main 是 `tests/unit/09_core/test_index_tables.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_inspect_degraded_pack_marking.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_inspect_degraded_pack_marking.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_inspect_mode_failclosed_p1p1.py` | 同名件在 main 是 `tests/unit/04_gates/test_inspect_mode_failclosed_p1p1.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_jpn_no_pv1_rules.py` | 同名件在 main 是 `tests/unit/04_gates/test_jpn_no_pv1_rules.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_judge_checklist_p3.py` | 同名件在 main 是 `tests/unit/02_workflow/test_judge_checklist_p3.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_judge_gates_match_config.py` | 同名件在 main 是 `tests/unit/02_workflow/test_judge_gates_match_config.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_judge_never_submits.py` | 同名件在 main 是 `tests/unit/02_workflow/test_judge_never_submits.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ledger_key_catalog.py` | 同名件在 main 是 `tests/unit/01_store_db/test_ledger_key_catalog.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ledger_set_at_file.py` | 同名件在 main 是 `tests/unit/01_store_db/test_ledger_set_at_file.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ledger_whitelist_schema_p0p4.py` | 同名件在 main 是 `tests/unit/01_store_db/test_ledger_whitelist_schema_p0p4.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_mcp_config_portable.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_mcp_config_portable.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_mcp_ping_calls.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_mcp_ping_calls.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_mining_efficiency_guards.py` | 同名件在 main 是 `tests/unit/02_workflow/test_mining_efficiency_guards.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_mode_b_qualification_doc.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_mode_b_qualification_doc.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_mode_b_qualify_cli.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_mode_b_qualify_cli.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_n30_wave_results_writers.py` | 同名件在 main 是 `tests/unit/01_store_db/test_n30_wave_results_writers.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_n31_harvest_entry.py` | 同名件在 main 是 `tests/unit/01_store_db/test_n31_harvest_entry.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_n32_review_entry.py` | 同名件在 main 是 `tests/unit/01_store_db/test_n32_review_entry.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_n35_alpha_state_merge.py` | 同名件在 main 是 `tests/unit/01_store_db/test_n35_alpha_state_merge.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_op_arity.py` | 同名件在 main 是 `tests/unit/09_core/test_op_arity.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_opportunity_scan_xregion.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_opportunity_scan_xregion.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_optimization_landing_20260925.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_optimization_landing_20260925.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_optimization_v1_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_optimization_v1_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_os_decay_benchmark.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_os_decay_benchmark.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_os_decay_calibration.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_os_decay_calibration.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_p0_fixes_20260927.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_p0_fixes_20260927.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_p1_batch2_20260927.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_p1_batch2_20260927.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_p1_fixes_20260927.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_p1_fixes_20260927.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_pf_family_aggregation.py` | 同名件在 main 是 `tests/unit/04_gates/test_pf_family_aggregation.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_pipeline_error_isolation.py` | 同名件在 main 是 `tests/unit/02_workflow/test_pipeline_error_isolation.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_pipeline_submit_ready_shape.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_pipeline_submit_ready_shape.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_planning_with_files_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_planning_with_files_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ppa_handoff.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_ppa_handoff.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_priors_cache_key_p2p12.py` | 同名件在 main 是 `tests/unit/02_workflow/test_priors_cache_key_p2p12.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_prod_screen_from_file.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_prod_screen_from_file.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_pull_skills_safety.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_pull_skills_safety.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_pyenv.py` | 同名件在 main 是 `tests/unit/09_core/test_pyenv.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_quota_et_day.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_quota_et_day.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_r3_failed_count_single_source.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_r3_failed_count_single_source.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ra_failed_checks_single_definition.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_ra_failed_checks_single_definition.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_ra_sop_template.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_ra_sop_template.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_recon_evidence.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_recon_evidence.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_recon_wave.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_recon_wave.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_region_alignment.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_region_alignment.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_region_rotation.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_region_rotation.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_research.py` | 同名件在 main 是 `tests/unit/09_core/test_research.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_review_near_structural_dead.py` | 同名件在 main 是 `tests/unit/08_forum_recon/test_review_near_structural_dead.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_run_logged_subprocess.py` | 同名件在 main 是 `tests/unit/02_workflow/test_run_logged_subprocess.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_s2_field_validator.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_s2_field_validator.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_score_datasets_whitelist_p0p6.py` | 同名件在 main 是 `tests/unit/04_gates/test_score_datasets_whitelist_p0p6.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_sd_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_sd_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_sd_engine_contracts.py` | 同名件在 main 是 `tests/unit/01_store_db/test_sd_engine_contracts.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_sd_portability.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_sd_portability.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_se_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_se_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_seal_dead_end_gate.py` | 同名件在 main 是 `tests/unit/01_store_db/test_seal_dead_end_gate.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_selfcorr_quick_script.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_selfcorr_quick_script.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_semantic_gate_failclosed.py` | 同名件在 main 是 `tests/unit/04_gates/test_semantic_gate_failclosed.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_sf_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_sf_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_sf_sweeps.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_sf_sweeps.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_shape_quota.py` | 同名件在 main 是 `tests/unit/01_store_db/test_shape_quota.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_skeleton_dedup_p5.py` | 同名件在 main 是 `tests/unit/09_core/test_skeleton_dedup_p5.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_skill_boundaries.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_skill_boundaries.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_skill_hooks_and_tools_guard.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_skill_hooks_and_tools_guard.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_skill_integrity.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_skill_integrity.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_skill_lint.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_skill_lint.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_skills.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_skills.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_slots_arbitration.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_slots_arbitration.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_step_eval.py` | 同名件在 main 是 `tests/unit/02_workflow/test_step_eval.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_step_funnel_p5.py` | 同名件在 main 是 `tests/unit/02_workflow/test_step_funnel_p5.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_store.py` | 同名件在 main 是 `tests/unit/01_store_db/test_store.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_structural_reconstruct.py` | 同名件在 main 是 `tests/unit/09_core/test_structural_reconstruct.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_alpha_gate.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_submit_alpha_gate.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_alpha_super_guard.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_submit_alpha_super_guard.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_chain_defaults.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_submit_chain_defaults.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_queue_gates.py` | 同名件在 main 是 `tests/unit/01_store_db/test_submit_queue_gates.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_queue_turnover_limit.py` | 同名件在 main 是 `tests/unit/01_store_db/test_submit_queue_turnover_limit.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_ready_unique_selfheal.py` | 同名件在 main 是 `tests/unit/01_store_db/test_submit_ready_unique_selfheal.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_submit_verdict_core.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_submit_verdict_core.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_super_build_prod_gate.py` | 同名件在 main 是 `tests/unit/05_submit_quota/test_super_build_prod_gate.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_sync_skills_ignores_secret_files.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_sync_skills_ignores_secret_files.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_threshold_relations.py` | 同名件在 main 是 `tests/unit/01_store_db/test_threshold_relations.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_time_bombs.py` | 同名件在 main 是 `tests/unit/09_core/test_time_bombs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_timeutil.py` | 同名件在 main 是 `tests/unit/09_core/test_timeutil.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_toolkit_api_429_backoff.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_toolkit_api_429_backoff.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_triage_gate_failclosed.py` | 同名件在 main 是 `tests/unit/04_gates/test_triage_gate_failclosed.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_validator_bucket_range_required.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_validator_bucket_range_required.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_validator_densify_group.py` | 同名件在 main 是 `tests/unit/10_toolkit_scripts/test_validator_densify_group.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wait_thresholds.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_wait_thresholds.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_waiver.py` | 同名件在 main 是 `tests/unit/09_core/test_waiver.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wave_gate_auto_insert_contract.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_wave_gate_auto_insert_contract.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wave_gate_terminal_states.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_wave_gate_terminal_states.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wave_gate_waiver_phase.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_wave_gate_waiver_phase.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wave_id_contract_p2p6.py` | 同名件在 main 是 `tests/unit/02_workflow/test_wave_id_contract_p2p6.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wave_verdict_contract.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_wave_verdict_contract.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wave_verdict_enum.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_wave_verdict_enum.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_weighted_mix_structural_gate5.py` | 同名件在 main 是 `tests/unit/04_gates/test_weighted_mix_structural_gate5.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_window_whitelist_p4.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_window_whitelist_p4.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wiring_fixes_20260915.py` | 同名件在 main 是 `tests/unit/06_wave_pipeline/test_wiring_fixes_20260915.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_workflow.py` | 同名件在 main 是 `tests/unit/02_workflow/test_workflow.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_workflow_chain_irreversible_guard.py` | 同名件在 main 是 `tests/unit/02_workflow/test_workflow_chain_irreversible_guard.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_workflow_nodes.py` | 同名件在 main 是 `tests/unit/02_workflow/test_workflow_nodes.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_workflow_popen_stdin_devnull.py` | 同名件在 main 是 `tests/unit/02_workflow/test_workflow_popen_stdin_devnull.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tests/unit/test_wq_backtest_monitor_docs.py` | 同名件在 main 是 `tests/unit/07_docs_skills/test_wq_backtest_monitor_docs.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/_check_op_submitted.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/_fix_queue_20261005.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/_kor_harvest_wave.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/_kor_s6_writeback2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/backfill_alpha_metrics_from_platform.py` | 同名件在 main 是 `tools/data-repair/backfill_alpha_metrics_from_platform.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/candidate_health_card.py` | 同名件在 main 是 `tools/verdict/candidate_health_card.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/enqueue_propose.py` | 同名件在 main 是 `tools/ledger/enqueue_propose.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/gbr_pre_submit_check.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/gen_gbr_candidates_report.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/kor_opportunity_scan.py` | 同名件在 main 是 `tracking/KOR/scripts/kor_opportunity_scan.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/probe_sa_candidates.py` | 同名件在 main 是 `tools/probe/probe_sa_candidates.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/probe_sa_unsubmitted.py` | 同名件在 main 是 `tools/probe/probe_sa_unsubmitted.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/probe_towers_sa.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/research/build_cluster_variants.py` | 同名件在 main 是 `tools/build_cluster_variants.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/scan_backup_ra.py` | 同名件在 main 是 `tools/ledger/scan_backup_ra.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/submit_inventory.py` | 同名件在 main 是 `tools/verdict/submit_inventory.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/test_gbr_batch_isolation.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/tmp_a16_axes.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/validate_gbr_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tools/verdict/os_decay_benchmark.py` | 同名件在 main 是 `tools/os_decay_benchmark.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tools/verify_region_op.py` | 同名件在 main 是 `tools/verdict/verify_region_op.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tracking/2026-10-02_analyst_mining.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/2026-10-02_robustness.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/2026-10-02_sentiment_research.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/2026-10-02_usa_tower_scan.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/2026-10-03_robustness.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/2026-10-05_robustness.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/ASI/ideas/ideas_continuation_score_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/ASI/ideas/ideas_model28_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/ASI/ideas/ideas_pattern_scores_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/ASI/ideas/ideas_pv13_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/ASI/ideas/ideas_pv13_post_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_deu_datasets.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_deu_err.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_deu_err2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_deu_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_harvest_deu.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_harvest_deu2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_poll_deu.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_probe_deu3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_probe_deu4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_probe_deu_syntax.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_run_deu_dual.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_run_deu_dual2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/DEU/scripts/tmp_scan_targets.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/ACCUMULATED_CANDIDATES.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/check_wave_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/direct_submit.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/fetch_prod.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave333.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave334.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave335.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave336.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave337.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave338.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave339.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/gen_wave340.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/run_wave269_fincf_residual.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/run_wave_single_fanout.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/tmp_eur_nlp_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/tmp_eur_pricedl.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/tmp_eur_probe.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/EUR/scripts/tmp_eur_probe2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GBR/scripts/check_corr.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GBR/scripts/dispatch_batch.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GBR/scripts/gen_candidates_report.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GBR/scripts/harvest_expr.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GLB/reports/glb_10tower_matrix_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GLB/reports/l4_other432_20261003.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GLB/scripts/_serial_runner.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/GLOBAL/templates/s2_candidate_pool_template.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/HKG/priors/ideas_analyst39_wave1.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/IND/scripts/_alpha_checks.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/IND/scripts/_harvest.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/IND/scripts/_metrics.py` | 同名件在 main 是 `src/wqb/expression/_metrics.py` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tracking/IND/scripts/_probe_is.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/IND/scripts/_probe_model29.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/IND/scripts/_prod_batch.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/ideas/ideas_risk60_wave185_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/ideas/ideas_xfam_wave186_20261002.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/harvest_batch.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/self_batch.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_check.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_check_props.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_check_pyr.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_check_val.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_check_wave104.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_clear_tag.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_cmp_settings.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_db_writeback.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_desc_si12.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_err2_si5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_err_pricedl.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_err_si5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_events.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_find_recent.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_get_metrics.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_harvest2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_harvest3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_harvest_si12.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_inspect.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_isolate_si5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_kor_active_list.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_kor_pricedl_probe.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_kor_si_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_map_wave.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_measure3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_measure_batch.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_measure_prod.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_measure_prod2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_name_mLmG.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_patch_desc.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll6.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll7.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll8.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll_all.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll_all2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_poll_si.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_pp_quota.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_ppa_count.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_pricedl_single.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_probe_ops.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_probe_pool.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_probe_prod.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_prod2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_prod3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_prod4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_prod5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_prod_ratio.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_pyr_status.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_risk59.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_cross.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_crossfield.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_decouple.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_decouple2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_decouple3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_decouple4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_final.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_hump.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_hump2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_hump3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_hump4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_ratio_b.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_ratio_c.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_ratio_c2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_ratio_c3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_ratio_d.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_ratio_e.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_rsk59.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_rsk59b.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_rsk59b2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_shortsell.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si10.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si11.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si12.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si13.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si14.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si15.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si16.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si17.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si38agg.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si3_wave.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si3main_wave.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si3util_wave.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si5_wave.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si6.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si7.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si8.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_run_si9.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_set_desc.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_si3_probe.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_si3_validate.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_si_finalize.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_submit.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_submit1.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_submit_plan.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_submit_serial.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_summary.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_theme_cmp.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_themes_probe.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_today_ppa.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_validate_agg.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_validate_cross.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_validate_pricedl2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_validate_ratio_d.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_validate_ratio_d2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_validate_si5_rel.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_verdict.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/KOR/scripts/tmp_write_props.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/USA/reference/usa_earn_wave01_findings.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/_archive/findings.md` | 同名件在 main 是 `Claude/skills/planning-with-files/templates/findings.md`, `docs/plans/findings.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tracking/_archive/progress.md` | 同名件在 main 是 `Claude/skills/planning-with-files/templates/progress.md`, `docs/plans/progress.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `tracking/reference/fetch_alpha_metrics_batch.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w1.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w10.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w11.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w12.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w14.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w15.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w6.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w7.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_asi_w8.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_w12.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_w13.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_w14.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/gen_w15.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_alpha_full.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_audit_noprod.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_audit_ready.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_axis_check.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_check_family.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_diag6_grid.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_diag7_decay.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_diag8_2y.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_diag9_final.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_diag_err.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_ds_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_ds_fields2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_ds_meta.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_eur_ds_by_cat.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_explore_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_fetch_pyramid.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_fields_price_dl.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_find_eur_pattern_alphas.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_diag1.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_diag2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_diag3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_diag4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_diag5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_pattern.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_eur_wiki.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_kor_insd5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_kor_insd5_w2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_kor_insd5_w3.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_kor_insd5_w4.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_kor_insd5_w5.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_gen_kor_insd5_w6.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_list_targets.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_now_status.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_other571_fields.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_probe_conc.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_probe_generic.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_probe_prod.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_probe_serial.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_probe_serial2.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_pyr_radar.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_scan_strong_ds.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_scan_zero_comp.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_show_probe.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_study_all_actives.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_study_eur_actives.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_tower_map.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `tracking/reference/tmp_two_ds.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `world-quant-brain-mcp/docs/MCP_TEST_REPORT_20260913.md` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `world-quant-brain-mcp/docs/QUICK_START.md` | 同名件在 main 是 `world-quant-brain-mcp/QUICK_START.md` 但**内容不同**（分叉或版本差）——需人工比对 | rule |
| `world-quant-brain-mcp/probe_direct_auth.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `world-quant-brain-mcp/probe_labs_live.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `world-quant-brain-mcp/start_mcp_http_servers.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |
| `world-quant-brain-mcp/stop_mcp_http_servers.py` | 需人工裁决：代码 / 文档 / 结论类资产，main 无同名件 | rule |

## 4. 处置纪律

- 取件用 `git checkout <ref> -- <path>` 再 `git restore --staged <path>`；**禁 `git stash pop/apply`、禁 `git restore --staged .`**（会扫到别人的在途文件）。
- 判 `DROPPED` 前必须做**三源交叉**：`git ls-files`（main）+ 每个 `preserve/*` 的 `ls-tree` + `git log --all --diff-filter=D -- <path>`。任一为「有」就不得写「从未存在」（2026-10-06 就发生过一次：`src/wqb/semantic_ledger.py` 被按「工作区没有」误判成「从未落地」）。
- 分叉线不得单件回迁：若「A 有 B 无」与「B 有 A 无」同时存在，只能由该线所有者整线合并，任何方向覆盖都丢工作（`branch_policy.md` §2 取件纪律）。

