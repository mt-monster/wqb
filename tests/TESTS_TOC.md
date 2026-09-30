# tests/ 测试归类方案（待审核）

> 生成：一次性脚本 `tests/.gen_tests_toc.py`（源分析可复跑）。**本清单仅归档，未搬移任何文件。**

`tests/unit/` 现平铺 173 个测试文件（排除 `test_toolified_cli.py`）。
建议按被测源码模块归入以下主题子目录。

| 子目录 | 主题 | 文件数 |
|---|---|--:|
| `tests/unit/01_store_db/` | store 存储层 / db 连接 / submit_queue | 25 |
| `tests/unit/02_workflow/` | workflow 编排 / 执行 / 节点通用 | 17 |
| `tests/unit/03_gem/` | GEM 表达生成引擎 | 8 |
| `tests/unit/04_gates/` | 信号 / 提交闸门（含组合形态铁律） | 13 |
| `tests/unit/05_submit_quota/` | 提交 / 判定 / 配额 / 相关性 | 16 |
| `tests/unit/06_wave_pipeline/` | 战役 pipeline / 波形 / 台账 / 波门 | 24 |
| `tests/unit/07_docs_skills/` | 文档 / Skill 一致性 | 25 |
| `tests/unit/08_forum_recon/` | 论坛情报 / 侦察 / 复盘 / 概念 | 17 |
| `tests/unit/09_core/` | 核心基础模块（config/expression/research/search 等） | 20 |
| `tests/unit/10_toolkit_scripts/` | tools/ 与 skills scripts 第三方工具脚本 | 8 |
| **合计** | | **173** |

---

## `tests/unit/01_store_db/` — store 存储层 / db 连接 / submit_queue（25）

- `test_atom_labeler.py`
- `test_build_field_index.py`
- `test_build_wave_selection.py`
- `test_category_field_triage_b.py`
- `test_db_wave_membership.py`
- `test_db_write_guards.py`
- `test_dblock_dead_holder.py`
- `test_expression_status.py`
- `test_ledger_key_catalog.py`
- `test_ledger_set_at_file.py`
- `test_ledger_whitelist_schema_p0p4.py`
- `test_n30_wave_results_writers.py`
- `test_n31_harvest_entry.py`
- `test_n32_review_entry.py`
- `test_n35_alpha_state_merge.py`
- `test_n35_reharvest_state_preservation.py`
- `test_region_gates_p0p1.py`
- `test_sd_engine_contracts.py`
- `test_seal_dead_end_gate.py`
- `test_shape_quota.py`
- `test_store.py`
- `test_submit_queue_gates.py`
- `test_submit_queue_turnover_limit.py`
- `test_submit_ready_unique_selfheal.py`
- `test_threshold_relations.py`

## `tests/unit/02_workflow/` — workflow 编排 / 执行 / 节点通用（17）

- `test_alpha_properties_patch_partial.py`
- `test_campaign_prompt_commands_p4.py`
- `test_detached_first_output_heartbeat.py`
- `test_judge_checklist_p3.py`
- `test_judge_gates_match_config.py`
- `test_judge_never_submits.py`
- `test_mining_efficiency_guards.py`
- `test_pipeline_error_isolation.py`
- `test_priors_cache_key_p2p12.py`
- `test_run_logged_subprocess.py`
- `test_step_eval.py`
- `test_step_funnel_p5.py`
- `test_wave_id_contract_p2p6.py`
- `test_workflow.py`
- `test_workflow_chain_irreversible_guard.py`
- `test_workflow_nodes.py`
- `test_workflow_popen_stdin_devnull.py`

## `tests/unit/03_gem/` — GEM 表达生成引擎（8）

- `test_gem_console_watch.py`
- `test_gem_group_fields.py`
- `test_gem_pipeline_mode.py`
- `test_gem_pregate_platform_constraints.py`
- `test_gem_provenance_p1p2p3.py`
- `test_gem_repeated_placeholder.py`
- `test_gem_skill_paths.py`
- `test_prompt_kb.py`

## `tests/unit/04_gates/` — 信号 / 提交闸门（含组合形态铁律）（13）

- `test_catalog_gate_p3.py`
- `test_cluster_variants.py`
- `test_gate5_coverage_matrix.py`
- `test_gate_equal_weight_leg_add.py`
- `test_gate_region_invalid_group_fields.py`
- `test_gate_registry_docs.py`
- `test_inspect_mode_failclosed_p1p1.py`
- `test_jpn_no_pv1_rules.py`
- `test_pf_family_aggregation.py`
- `test_score_datasets_whitelist_p0p6.py`
- `test_semantic_gate_failclosed.py`
- `test_triage_gate_failclosed.py`
- `test_weighted_mix_structural_gate5.py`

## `tests/unit/05_submit_quota/` — 提交 / 判定 / 配额 / 相关性（16）

- `test_auth_transient_retry.py`
- `test_batch_status_auth.py`
- `test_batch_status_watch_transient.py`
- `test_batch_submit_verdict_phase2.py`
- `test_pipeline_submit_ready_shape.py`
- `test_ppa_handoff.py`
- `test_prod_screen_from_file.py`
- `test_quota_et_day.py`
- `test_r3_failed_count_single_source.py`
- `test_ra_failed_checks_single_definition.py`
- `test_selfcorr_quick_script.py`
- `test_submit_alpha_gate.py`
- `test_submit_alpha_super_guard.py`
- `test_submit_chain_defaults.py`
- `test_submit_verdict_core.py`
- `test_super_build_prod_gate.py`

## `tests/unit/06_wave_pipeline/` — 战役 pipeline / 波形 / 台账 / 波门（24）

- `test_backlog_drop_guard.py`
- `test_backlog_gate_unconsumed_p0p2.py`
- `test_harvest_checks_path.py`
- `test_harvest_longcount_fields.py`
- `test_harvest_multisim_retry.py`
- `test_harvest_multisim_transient_retry.py`
- `test_mcp_config_portable.py`
- `test_mcp_ping_calls.py`
- `test_optimization_landing_20260925.py`
- `test_p0_fixes_20260927.py`
- `test_p1_batch2_20260927.py`
- `test_p1_fixes_20260927.py`
- `test_region_alignment.py`
- `test_region_rotation.py`
- `test_stop_rules_axis_scope.py`
- `test_stop_rules_verdict_p0p3.py`
- `test_wave_gate_auto_insert_contract.py`
- `test_wave_gate_terminal_states.py`
- `test_wave_gate_waiver_phase.py`
- `test_wave_key_contract.py`
- `test_wave_verdict_contract.py`
- `test_wave_verdict_enum.py`
- `test_window_whitelist_p4.py`
- `test_wiring_fixes_20260915.py`

## `tests/unit/07_docs_skills/` — 文档 / Skill 一致性（25）

- `test_audit_fixes.py`
- `test_brain_alpha_repair_docs.py`
- `test_docs_consistency.py`
- `test_experience_kb_refs.py`
- `test_glossary_docs.py`
- `test_how_to_pass_docs.py`
- `test_mode_b_qualification_doc.py`
- `test_mode_b_qualify_cli.py`
- `test_optimization_v1_docs.py`
- `test_planning_with_files_docs.py`
- `test_pull_skills_safety.py`
- `test_ra_sop_template.py`
- `test_sd_docs.py`
- `test_sd_portability.py`
- `test_se_docs.py`
- `test_sf_docs.py`
- `test_sf_sweeps.py`
- `test_skill_boundaries.py`
- `test_skill_hooks_and_tools_guard.py`
- `test_skill_integrity.py`
- `test_skill_lint.py`
- `test_skills.py`
- `test_sync_skills_ignores_secret_files.py`
- `test_wait_thresholds.py`
- `test_wq_backtest_monitor_docs.py`

## `tests/unit/08_forum_recon/` — 论坛情报 / 侦察 / 复盘 / 概念（17）

- `test_campaign_intel_20260919_landing.py`
- `test_campaign_intel_mark_saturated.py`
- `test_campaign_intel_prod_first.py`
- `test_campaign_intel_s0_rank_p1.py`
- `test_closure_ledger.py`
- `test_concept_overlap.py`
- `test_concept_taxonomy_map.py`
- `test_dead_end_forum_gate.py`
- `test_diagnostics.py`
- `test_forum_cache_builder_paths.py`
- `test_forum_recon.py`
- `test_forum_recon_node.py`
- `test_forum_recon_wave.py`
- `test_opportunity_scan_xregion.py`
- `test_recon_evidence.py`
- `test_recon_wave.py`
- `test_review_near_structural_dead.py`

## `tests/unit/09_core/` — 核心基础模块（config/expression/research/search 等）（20）

- `test_config.py`
- `test_dataset_experience.py`
- `test_diversity.py`
- `test_field_semantic_classify.py`
- `test_ghost_operator_lists.py`
- `test_grammar.py`
- `test_handoff.py`
- `test_index_tables.py`
- `test_memory.py`
- `test_observability.py`
- `test_op_arity.py`
- `test_pyenv.py`
- `test_research.py`
- `test_scheduler.py`
- `test_search.py`
- `test_skeleton_dedup_p5.py`
- `test_structural_reconstruct.py`
- `test_time_bombs.py`
- `test_timeutil.py`
- `test_waiver.py`

## `tests/unit/10_toolkit_scripts/` — tools/ 与 skills scripts 第三方工具脚本（8）

- `test_inspect_degraded_pack_marking.py`
- `test_os_decay_benchmark.py`
- `test_os_decay_calibration.py`
- `test_s2_field_validator.py`
- `test_slots_arbitration.py`
- `test_toolkit_api_429_backoff.py`
- `test_validator_bucket_range_required.py`
- `test_validator_densify_group.py`
