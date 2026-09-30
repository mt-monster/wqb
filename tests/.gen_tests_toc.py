"""tests/ 归类工具：单一真源 MAP（文件名 -> 主题子目录）。

子命令：
  python tests/.gen_tests_toc.py            # 生成 tests/TESTS_TOC.md 方案清单
  python tests/.gen_tests_toc.py move       # 执行 git mv 搬移 173 文件进子目录
  python tests/.gen_tests_toc.py annotate   # 同步更新 src/tools 里 tests/unit/test_xxx.py 注释路径

归类依据 = 被测源码模块（wqb.* import）+ 文件名主题双参考，人工裁定。
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

UNIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "unit")

# 主题目录中文名
DIR_CN = {
    "01_store_db": "store 存储层 / db 连接 / submit_queue",
    "02_workflow": "workflow 编排 / 执行 / 节点通用",
    "03_gem": "GEM 表达生成引擎",
    "04_gates": "信号 / 提交闸门（含组合形态铁律）",
    "05_submit_quota": "提交 / 判定 / 配额 / 相关性",
    "06_wave_pipeline": "战役 pipeline / 波形 / 台账 / 波门",
    "07_docs_skills": "文档 / Skill 一致性",
    "08_forum_recon": "论坛情报 / 侦察 / 复盘 / 概念",
    "09_core": "核心基础模块（config/expression/research/search 等）",
    "10_toolkit_scripts": "tools/ 与 skills scripts 第三方工具脚本",
}

# 完整映射：文件名(无.py) -> 目录。人工裁定，覆盖全部 173 个。
M = {}

def put(dirname, names):
    for n in names:
        if n in M:
            raise SystemExit(f"[dup] {n} 已在 {M[n]}，又归入 {dirname}")
        M[n] = dirname


put("01_store_db", [
    "test_store", "test_expression_status", "test_db_write_guards",
    "test_db_wave_membership", "test_submit_queue_gates", "test_submit_queue_turnover_limit",
    "test_threshold_relations", "test_n31_harvest_entry", "test_n35_alpha_state_merge",
    "test_n35_reharvest_state_preservation", "test_n30_wave_results_writers",
    "test_seal_dead_end_gate", "test_shape_quota", "test_submit_ready_unique_selfheal",
    "test_dblock_dead_holder", "test_atom_labeler", "test_build_field_index",
    "test_build_wave_selection", "test_sd_engine_contracts", "test_ledger_key_catalog",
    "test_ledger_set_at_file", "test_ledger_whitelist_schema_p0p4", "test_region_gates_p0p1",
    "test_category_field_triage_b", "test_n32_review_entry",
])
put("02_workflow", [
    "test_workflow", "test_workflow_nodes", "test_workflow_chain_irreversible_guard",
    "test_detached_first_output_heartbeat", "test_run_logged_subprocess",
    "test_workflow_popen_stdin_devnull", "test_priors_cache_key_p2p12",
    "test_alpha_properties_patch_partial", "test_step_eval", "test_step_funnel_p5",
    "test_pipeline_error_isolation", "test_wave_id_contract_p2p6",
    "test_campaign_prompt_commands_p4", "test_judge_checklist_p3",
    "test_judge_gates_match_config", "test_judge_never_submits", "test_mining_efficiency_guards",
])
put("03_gem", [
    "test_gem_console_watch", "test_gem_group_fields", "test_gem_pipeline_mode",
    "test_gem_pregate_platform_constraints", "test_gem_provenance_p1p2p3",
    "test_gem_repeated_placeholder", "test_gem_skill_paths", "test_prompt_kb",
])
put("04_gates", [
    "test_gate5_coverage_matrix", "test_gate_equal_weight_leg_add",
    "test_gate_region_invalid_group_fields", "test_gate_registry_docs",
    "test_weighted_mix_structural_gate5", "test_semantic_gate_failclosed",
    "test_triage_gate_failclosed", "test_score_datasets_whitelist_p0p6",
    "test_catalog_gate_p3", "test_inspect_mode_failclosed_p1p1", "test_jpn_no_pv1_rules",
    "test_pf_family_aggregation", "test_cluster_variants",
])
put("05_submit_quota", [
    "test_submit_alpha_gate", "test_submit_alpha_super_guard", "test_submit_chain_defaults",
    "test_submit_verdict_core", "test_batch_submit_verdict_phase2",
    "test_super_build_prod_gate", "test_quota_et_day", "test_selfcorr_quick_script",
    "test_auth_transient_retry", "test_batch_status_auth", "test_batch_status_watch_transient",
    "test_r3_failed_count_single_source", "test_ra_failed_checks_single_definition",
    "test_pipeline_submit_ready_shape", "test_ppa_handoff", "test_prod_screen_from_file",
])
put("06_wave_pipeline", [
    "test_wave_gate_auto_insert_contract", "test_wave_gate_terminal_states",
    "test_wave_gate_waiver_phase", "test_wave_key_contract", "test_wave_verdict_contract",
    "test_wave_verdict_enum", "test_region_rotation", "test_region_alignment", "test_optimization_landing_20260925",
    "test_backlog_drop_guard", "test_backlog_gate_unconsumed_p0p2",
    "test_window_whitelist_p4", "test_stop_rules_axis_scope", "test_stop_rules_verdict_p0p3",
    "test_harvest_checks_path", "test_harvest_longcount_fields", "test_harvest_multisim_retry",
    "test_harvest_multisim_transient_retry", "test_wiring_fixes_20260915",
    "test_p0_fixes_20260927", "test_p1_batch2_20260927", "test_p1_fixes_20260927",
    "test_mcp_ping_calls", "test_mcp_config_portable",
])
put("07_docs_skills", [
    "test_docs_consistency", "test_skill_integrity", "test_skill_lint", "test_skills",
    "test_skill_boundaries", "test_skill_hooks_and_tools_guard",
    "test_sync_skills_ignores_secret_files", "test_glossary_docs", "test_how_to_pass_docs",
    "test_planning_with_files_docs", "test_brain_alpha_repair_docs", "test_experience_kb_refs",
    "test_ra_sop_template", "test_optimization_v1_docs", "test_pull_skills_safety",
    "test_wq_backtest_monitor_docs", "test_sd_docs", "test_sd_portability", "test_sf_docs",
    "test_sf_sweeps", "test_se_docs", "test_wait_thresholds",
    "test_mode_b_qualification_doc", "test_mode_b_qualify_cli", "test_audit_fixes",
])
put("08_forum_recon", [
    "test_forum_recon", "test_forum_recon_node", "test_forum_recon_wave",
    "test_forum_cache_builder_paths", "test_recon_evidence", "test_recon_wave",
    "test_opportunity_scan_xregion", "test_concept_overlap", "test_concept_taxonomy_map",
    "test_campaign_intel_20260919_landing", "test_campaign_intel_mark_saturated",
    "test_campaign_intel_prod_first", "test_campaign_intel_s0_rank_p1", "test_diagnostics",
    "test_review_near_structural_dead", "test_dead_end_forum_gate", "test_closure_ledger",
])
put("09_core", [
    "test_config", "test_grammar", "test_op_arity", "test_research", "test_search",
    "test_memory", "test_observability", "test_scheduler", "test_handoff", "test_timeutil",
    "test_time_bombs", "test_waiver", "test_pyenv", "test_field_semantic_classify",
    "test_structural_reconstruct", "test_diversity", "test_ghost_operator_lists",
    "test_dataset_experience", "test_index_tables", "test_skeleton_dedup_p5",
])
put("10_toolkit_scripts", [
    "test_s2_field_validator", "test_validator_bucket_range_required",
    "test_validator_densify_group", "test_os_decay_benchmark", "test_os_decay_calibration",
    "test_slots_arbitration", "test_toolkit_api_429_backoff", "test_inspect_degraded_pack_marking",
])

# ============ 校验覆盖 ============
def _check_cover():
    files = sorted(f for f in os.listdir(UNIT)
                   if f.endswith(".py") and f.startswith("test_") and f != "test_toolified_cli.py")
    names = [f[:-3] for f in files]
    missing = [n for n in names if n not in M]
    unused = [n for n in M if n not in names]
    if missing:
        raise SystemExit(f"[未覆盖] {len(missing)} 个未归入映射: {missing}")
    if unused:
        raise SystemExit(f"[多余] {len(unused)} 个映射在真实文件里不存在: {unused}")
    return names


def generate():
    # 直接基于映射 M 生成（搬移后文件已不平铺，不再依赖磁盘扫描）
    names = sorted(M.keys())
    by_dir = defaultdict(list)
    for n in names:
        by_dir[M[n]].append(n + ".py")
    count_by_dir = {d: len(by_dir[d]) for d in by_dir}
    total = len(names)

    lines = []
    lines.append("# tests/ 测试归类方案（已执行搬移）")
    lines.append("")
    lines.append(f"> 生成：一次性脚本 `tests/.gen_tests_toc.py`（源分析可复跑）。本清单为 `tests/unit/` 下测试文件的主题归类映射。")
    lines.append("")
    lines.append(f"`tests/unit/` 下 {total} 个测试文件（排除 `test_toolified_cli.py`）归入以下主题子目录。")
    lines.append("")
    lines.append("| 子目录 | 主题 | 文件数 |")
    lines.append("|---|---|--:|")
    for d in sorted(by_dir):
        lines.append(f"| `tests/unit/{d}/` | {DIR_CN[d]} | {count_by_dir[d]} |")
    lines.append(f"| **合计** | | **{total}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    for d in sorted(by_dir):
        lines.append(f"## `tests/unit/{d}/` — {DIR_CN[d]}（{count_by_dir[d]}）")
        lines.append("")
        for fname in sorted(by_dir[d]):
            lines.append(f"- `{fname}`")
        lines.append("")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TESTS_TOC.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"已生成 {out}（{total} 文件，{len(by_dir)} 个主题目录）")


def move():
    """搬移每个 test 文件进对应主题子目录（同卷 rename，不触发沙箱 unlink 守卫）。

    已跟踪 -> git mv（保留历史）；未跟踪 -> os.rename（等同 rename，无 unlink）。
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    moved = 0
    skipped = 0
    for n, d in M.items():
        src = os.path.join(repo_root, "tests", "unit", n + ".py")
        dst_dir = os.path.join(repo_root, "tests", "unit", d)
        dst = os.path.join(dst_dir, n + ".py")
        if not os.path.exists(src):
            skipped += 1
            continue
        os.makedirs(dst_dir, exist_ok=True)
        tracked = os.system(
            f'git -C "{repo_root}" ls-files --error-unmatch "{os.path.relpath(src, repo_root)}" >nul 2>&1'
        ) == 0
        if tracked:
            rc = os.system(f'git -C "{repo_root}" mv "{src}" "{dst}"')
            if rc != 0:
                raise SystemExit(f"[git mv 失败] rc={rc} {src} -> {dst}")
        else:
            os.rename(src, dst)
        moved += 1
    print(f"已搬移 {moved} 个文件进子目录（跳过已搬 {skipped} 个）")


def annotate():
    """同步更新 src/ tools/ 等 .py 里 tests/unit/test_xxx.py 注释路径 -> tests/unit/<dir>/test_xxx.py。"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roots = [os.path.join(repo_root, "src"),
             os.path.join(repo_root, "tools"),
             os.path.join(repo_root, "pipeline")]
    pat = re.compile(r"(tests/unit/)(test_[A-Za-z0-9_]+\.py)")
    changed_files = 0
    changed_lines = 0
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, fnames in os.walk(root):
            if "__pycache__" in dirpath:
                continue
            for fn in fnames:
                if not fn.endswith(".py"):
                    continue
                fp = os.path.join(dirpath, fn)
                try:
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                def repl(m):
                    name = m.group(2)[:-3]
                    d = M.get(name)
                    if d is None:
                        return m.group(0)
                    return f"tests/unit/{d}/{m.group(2)}"
                new = pat.sub(repl, txt)
                if new != txt:
                    open(fp, "w", encoding="utf-8").write(new)
                    changed_files += 1
                    changed_lines += sum(1 for a, b in zip(txt.splitlines(), new.splitlines()) if a != b)
    print(f"已同步注释路径：{changed_files} 个文件，{changed_lines} 行")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    if cmd == "move":
        move()
    elif cmd == "annotate":
        annotate()
    else:
        generate()