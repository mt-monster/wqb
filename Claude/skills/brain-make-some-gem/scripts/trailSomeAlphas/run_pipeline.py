# -*- coding: utf-8 -*-
"""GEM 管线编排入口（concept-first / phased / skeleton 三模式）。

2026-09-12 模块化拆分：原 2642 行单文件收敛为 9 个同目录子模块：
  pipeline_paths.py        环境引导与共享依赖（路径常量/sys.path/ace_lib/validator/vector_wrap）
  pipeline_data.py         凭据与会话、DataFrame 工具、字段后缀候选与元数据块
  pipeline_placeholders.py 占位符三级匹配/压缩/归一化（防字段名拼接幻觉）
  pipeline_operators.py    平台算子过滤与默认算子池
  pipeline_prompts.py      single/phased 模式的 prompt 构建
  pipeline_reports.py      ideas markdown 读写（渲染/落盘/Concept 块解析）
  pipeline_llm.py          Moonshot LLM 调用（SSE 流式）
  pipeline_io.py           子进程/CSV/文件工具
  pipeline_kb.py           DB 存储与模板族绑定
本文件保留：编排（main）、skeleton/phased 执行器，以及对外兼容名字。

！！兼容性约束（勿破坏）：headless_runner/run.py 依赖以下模块级名字，并会在运行
时替换它们以拦截调用：rp.ace_lib / rp.start_brain_session / rp.run_script /
rp.call_moonshot（另引用 rp.main / rp.FEATURE_IMPLEMENTATION_DIR）。因此：
  1. 这些名字必须继续存在于本模块命名空间（由下方 re-export 提供）；
  2. 本模块（含 run_skeleton_generation / run_phased_pipeline / main）调用它们时
     必须用裸名（模块全局查找），不得改为 pipeline_*.xxx() 形式，否则 patch 失效。
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path


# --- 环境引导（必须最先执行：sys.path / UTF-8 stdout / ace_lib 等）---
import pipeline_paths  # noqa: F401
from pipeline_paths import FEATURE_ENGINEERING_DIR, FEATURE_IMPLEMENTATION_DIR, FEATURE_IMPLEMENTATION_SCRIPTS, ace_lib, ExpressionValidator, wrap_naked_vectors
from pipeline_data import build_allowed_metric_suffixes, build_allowed_suffixes_from_ids, build_field_summary, detect_dataset_code, ensure_metadata_block, load_brain_credentials_from_env_or_args, pick_first_present_column, read_text_optional, start_brain_session
from pipeline_llm import call_moonshot  # noqa: F401  （run.py patch 点，需 rp 全局调用）
from pipeline_io import (  # noqa: F401
    delete_path_if_exists,
    load_dataset_ids_from_csv,
    run_script,  # run.py patch 点，需 rp 全局调用
    safe_dataset_id,
)
from pipeline_kb import _prepare_family_binding, _wqb_campaign_store
from pipeline_operators import (  # noqa: F401
    DEFAULT_OPERATORS,
    _vector_ratio_from_datafields_df,
    filter_operators_df,
)
from pipeline_placeholders import normalize_template_placeholders
from pipeline_prompts import batch_fields_by_dataset, build_compact_operator_summary, build_phased_prompts, build_prompt
from pipeline_reports import _ensure_expected_exposure, extract_template_blocks, render_phased_ideas_md, render_skeleton_ideas_md, save_ideas_report

from economic_priors import load_priors

import skeletons  # 同目录骨架库（P0: skeleton mode 填槽协议）


def _load_skeleton_stats(region: str) -> dict:
    """聚合骨架级实测统计（只读、幂等；2026-09-13 新增）。

    数据链：idea ledger（s2_*_idea）的 skeleton_metas（expr→skeleton_id 归因）
           × expressions/backtest_results（expr→sharpe/fitness 指标）
           → per-skeleton {n, pass, pass_rate, best_sharpe, avg_sharpe}。
    历史产物无归因（skeleton_metas 为 2026-09-13 起埋点）时返回 {}，
    消费端（build_skeleton_prompt）自动降级为默认顺序。
    """
    import sqlite3
    root = os.environ.get("WQB_ROOT") or r"D:\coding\traeCN_project\wqb"
    db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
    if not os.path.isfile(db):
        return {}
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        # 1) 归因：s2_*_idea ledger 的 skeleton_metas（expr → skeleton_id）
        expr_to_skel = {}
        rows = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key LIKE 's2\\_%\\_idea' ESCAPE '\\'",
            (region,),
        ).fetchall()
        for r in rows:
            try:
                d = json.loads(r["value"])
            except (json.JSONDecodeError, TypeError):
                continue
            for m in (d.get("skeleton_metas") or []):
                if not isinstance(m, dict):
                    continue
                e = str(m.get("expr") or "").strip()
                sid = str(m.get("skeleton_id") or "").strip()
                if e and sid:
                    expr_to_skel[e] = sid
        if not expr_to_skel:
            return {}
        # 2) 指标：backtest_results.code 兜底 + expressions 表覆盖（同 key 取 expressions 值）
        metrics = {}
        for r in conn.execute(
            "SELECT code, sharpe, fitness FROM backtest_results WHERE region=?",
            (region,),
        ):
            e = str(r["code"] or "").strip()
            if e and e not in metrics:
                metrics[e] = {"sharpe": r["sharpe"], "fitness": r["fitness"]}
        for r in conn.execute(
            "SELECT expression, sharpe, fitness FROM expressions WHERE region=?",
            (region,),
        ):
            e = str(r["expression"] or "").strip()
            if e:
                metrics[e] = {"sharpe": r["sharpe"], "fitness": r["fitness"]}
        # 3) 聚合（只统计有 sharpe 的已回测表达式）
        agg = {}
        for e, sid in expr_to_skel.items():
            m = metrics.get(e)
            if not m or not isinstance(m.get("sharpe"), (int, float)):
                continue
            s = agg.setdefault(sid, {"n": 0, "pass": 0, "best_sharpe": None, "sum_sharpe": 0.0})
            sh = float(m["sharpe"])
            fit = m.get("fitness")
            s["n"] += 1
            if sh >= 1.58 and isinstance(fit, (int, float)) and fit >= 1.0:
                s["pass"] += 1
            s["sum_sharpe"] += sh
            if s["best_sharpe"] is None or sh > s["best_sharpe"]:
                s["best_sharpe"] = sh
        out = {}
        for sid, s in agg.items():
            out[sid] = {
                "n": s["n"],
                "pass": s["pass"],
                "pass_rate": round(s["pass"] / s["n"], 4),
                "best_sharpe": round(s["best_sharpe"], 3),
                "avg_sharpe": round(s["sum_sharpe"] / s["n"], 3),
            }
        return out
    finally:
        conn.close()


def run_skeleton_generation(
    api_key: str,
    model: str,
    dataset_id: str,
    region: str,
    delay: int,
    fields_df,
    n_slots: int = 40,
    use_priors: bool = True,
    max_retries: int = 2,
    window_pool: dict | None = None,
) -> tuple:
    """SKELETON MODE：LLM 填槽 + 代码组装表达式。

    经济学意义 = 骨架拓扑（代码枚举）× 槽位字段（LLM 决定）× 方向（符号）。
    LLM 只输出结构化 JSON，表达式由 skeletons 模块组装，语法合法性构造保证。

    Args:
        window_pool: 窗口池覆盖（如 {"daily": [10, 22]}），透传给
            build_skeleton_prompt；为 None 时用默认 WINDOW_DOMAINS。

    返回 (ideas_path, result_dict)；result_dict 含 expressions/metas/dropped/layers。
    """
    id_col = pick_first_present_column(fields_df, ["id", "field_id", "fieldId"])
    desc_col = pick_first_present_column(fields_df, ["description", "desc"])
    type_col = pick_first_present_column(fields_df, ["type", "dataType", "data_type", "field_type"])
    if not id_col:
        raise RuntimeError("[skeleton] fields_df has no id column")
    field_ids = fields_df[id_col].dropna().astype(str).tolist()
    descriptions: dict[str, str] = {}
    if desc_col:
        for fid, dsc in zip(fields_df[id_col], fields_df[desc_col]):
            descriptions[str(fid)] = "" if dsc is None else str(dsc)
    field_types: dict[str, str] = {}
    if type_col:
        for fid, typ in zip(fields_df[id_col], fields_df[type_col]):
            field_types[str(fid)] = "" if typ is None else str(typ)

    layers = skeletons.classify_fields(field_ids, descriptions, types=field_types or None)
    print(
        f"[skeleton] field layering: signal={len(layers['signal'])}, "
        f"scale={len(layers['scale'])}, metadata={len(layers['metadata'])} (excluded), "
        f"date={len(layers['date'])} (excluded), "
        f"vector={len(layers.get('vector', []))} (need vec_* aggregation), "
        f"group={len(layers.get('group', []))}",
        flush=True,
    )
    if not layers["signal"]:
        raise RuntimeError("[skeleton] no signal fields after layering (all metadata/scale?)")

    priors = skeletons.load_region_priors(region) if use_priors else ""
    if priors:
        print(f"[skeleton] region priors loaded for {region} ({len(priors)} chars)", flush=True)

    # 骨架实测统计（2026-09-13）：区域级 DB 聚合（n/pass_rate/best_sharpe），
    # 供 prompt 按实测胜率排序标注；与 --no-region-priors 联动（关先验=关一切注入）。
    skeleton_stats = None
    if use_priors:
        try:
            skeleton_stats = _load_skeleton_stats(region)
            if skeleton_stats:
                _tot = sum(s.get("n", 0) for s in skeleton_stats.values())
                print(f"[skeleton] 实测骨架统计: {len(skeleton_stats)} 个骨架有回测样本（{_tot} 条）", flush=True)
            else:
                print("[skeleton] 实测骨架统计: 暂无（自 2026-09-13 起随波次积累）", flush=True)
        except Exception as exc:
            print(f"[skeleton] warn: 骨架实测统计不可用（{exc}），按默认顺序", flush=True)
            skeleton_stats = None

    system_prompt, user_prompt = skeletons.build_skeleton_prompt(
        dataset_id=dataset_id, region=region, delay=delay,
        field_layers=layers, descriptions=descriptions,
        n_slots=n_slots, region_priors=priors,
        window_pool=window_pool,
        skeleton_stats=skeleton_stats,
    )

    slots: list = []
    for attempt in range(max_retries + 1):
        raw_report = call_moonshot(api_key, model, system_prompt, user_prompt)
        slots = skeletons.parse_slots_json(raw_report)
        if slots:
            break
        print(
            f"[skeleton] LLM output not parseable as slots JSON "
            f"(attempt {attempt + 1}/{max_retries + 1})",
            file=sys.stderr,
        )
        user_prompt += (
            "\n\nYour previous reply was not a valid JSON array. "
            "Return ONLY the JSON array, no prose, no code fences."
        )
    if not slots:
        raise RuntimeError("[skeleton] LLM produced no parseable slot entries.")

    exprs, metas, dropped = skeletons.assign_slots(
        slots,
        signal_fields=set(layers["signal"]),
        scale_fields=set(layers["scale"]),
    )
    print(f"[skeleton] slots={len(slots)} -> exprs={len(exprs)} (dropped: {dropped})", flush=True)
    if not exprs:
        raise RuntimeError(f"[skeleton] all slot entries were dropped: {dropped}")

    ideas_path = save_ideas_report(
        render_skeleton_ideas_md(dataset_id, region, delay, layers, metas, dropped),
        region, delay, dataset_id,
    )
    return ideas_path, {
        "expressions": exprs,
        "metas": metas,
        "dropped": dropped,
        "layers": layers,
    }





def run_phased_pipeline(
    api_key: str,
    model_structure: str,
    model_mapping: str,
    model_report: str,
    dataset_id: str,
    dataset_name: str | None,
    dataset_description: str | None,
    data_category: str,
    region: str,
    delay: int,
    universe: str,
    data_type: str,
    fields_df,
    allowed_operators: list[dict],
    allowed_metric_suffixes: list[str],
    timeout_s: int = 300,
    priors: dict | None = None,
    batch_size: int = 50,
) -> str:
    """Execute the 3-phase pipeline — SOLUTION A orchestrator.

    Returns the final ideas markdown report.
    Each phase uses its own model (configurable via Solution D).
    """
    # ---- Phase 1: Structure Parse ----
    print("[phased] Phase 1/3: Structure parse...", flush=True)
    sys_prompt, user_prompt = build_phased_prompts(
        dataset_id, dataset_name, dataset_description, data_category,
        region, delay, universe, data_type, [],
        allowed_operators, allowed_metric_suffixes,
        phase="structure",
    )
    structure_json = call_moonshot(api_key, model_structure, sys_prompt, user_prompt, timeout_s=timeout_s)

    # ---- Phase 2: Field Mapping (batched) ----
    print(f"[phased] Phase 2/3: Field mapping (batch_size={batch_size})...", flush=True)
    # 2026-09-18 ③：batch_size 从硬编码 50 改为参数透传（gem.py 节点默认 100），
    # 防拆散同族字段（如订单流 bid_*/ask_* 跨批导致跨族机制无法设计）。
    batches = batch_fields_by_dataset(fields_df, max_batch=batch_size)
    all_mapping_results: list[dict] = []

    for idx, (batch_key, batch_fields) in enumerate(batches):
        print(f"[phased]   Batch {idx+1}/{len(batches)}: {batch_key} ({len(batch_fields)} fields)", flush=True)
        sys_prompt, user_prompt = build_phased_prompts(
            dataset_id, dataset_name, dataset_description, data_category,
            region, delay, universe, data_type, [],
            allowed_operators, allowed_metric_suffixes,
            phase="mapping",
            structure_result=structure_json,
            batch_key=batch_key,
            batch_fields=batch_fields,
            priors=priors,
        )
        try:
            result = call_moonshot(api_key, model_mapping, sys_prompt, user_prompt, timeout_s=timeout_s)
            # Parse JSON array
            result_stripped = result.strip().strip("```json").strip("```").strip()
            parsed = json.loads(result_stripped)
            if isinstance(parsed, list):
                all_mapping_results.extend(parsed)
            else:
                all_mapping_results.append(parsed)
        except Exception as exc:
            print(f"[phased]   Warning: batch {batch_key} mapping failed: {exc}", file=sys.stderr)

    print(f"[phased]   Total mapping entries: {len(all_mapping_results)}", flush=True)

    # ---- Phase 3: Deterministic render（2026-09-13：确定性直译，替代 LLM 重写）----
    # JSON → markdown 直译：消除最后一段自由文本（字段名拼接幻觉面归零）；
    # 占位符合法性由下游归一化兜底；Phase 2 无模板时渲染为空 → 下游 fail fast。
    print("[phased] Phase 3/3: Deterministic render (no LLM call)...", flush=True)
    report = render_phased_ideas_md(all_mapping_results, dataset_id, region, delay)
    n_blocks = report.count("**Concept**:")
    print(f"[phased]   rendered {n_blocks} concept blocks", flush=True)
    if model_report:
        print(f"[phased]   note: model_report={model_report} is unused in deterministic mode", flush=True)
    print("[phased] Done.", flush=True)
    return report


def _normalize_template_pairs(block_pairs, dataset_ids, allowed_suffixes, dataset_code):
    """占位符归一化 + 严格校验：返回 (normalized_pairs, rejected_templates)。

    2026-09-12 新增（字段名拼接幻觉可观测性 + 反馈重试支撑）：
    rejected_templates 收集被拒模板（占位符无法匹配真实字段），原实现静默 continue，
    导致“整波因模板全被拒而失败”不可诊断、也无从反馈给 LLM 重生成。
    """
    normalized_pairs: list[tuple[str, str]] = []
    rejected_templates: list[str] = []
    for item in block_pairs:
        t = str(item.get("template") or "").strip()
        idea_text = str(item.get("idea") or "").strip()
        if not t:
            continue
        if dataset_ids and allowed_suffixes:
            normalized_t, ok = normalize_template_placeholders(t, dataset_ids, allowed_suffixes, dataset_code)
            if not ok:
                rejected_templates.append(t)
                continue
            normalized_pairs.append((normalized_t, idea_text))
        else:
            # No dataset ids to validate against; pass through.
            normalized_pairs.append((t, idea_text))
    return normalized_pairs, rejected_templates


def main():
    parser = argparse.ArgumentParser(description="Run feature engineering + implementation pipeline")
    parser.add_argument("--data-category", required=True, help="Dataset category (e.g., analyst, fundamental)")
    parser.add_argument("--region", required=True, help="Region (e.g., USA, GLB, EUR)")
    parser.add_argument("--delay", required=True, type=int, help="Delay (0 or 1)")
    parser.add_argument("--universe", default="TOP3000", help="Universe (default: TOP3000)")
    parser.add_argument("--dataset-id", required=True, help="Dataset id (required)")
    parser.add_argument("--instrument-type", default="EQUITY", help="Instrument type (default: EQUITY)")
    parser.add_argument(
        "--data-type",
        default="MATRIX",
        choices=["MATRIX", "VECTOR"],
        help="Data type to request from BRAIN datafields (MATRIX or VECTOR). Default: MATRIX",
    )
    parser.add_argument("--wave", default=None, help="Campaign wave id for DB upsert (default s2_<ds>_d<delay>)")
    parser.add_argument("--ideas-file", default=None, help="Use existing ideas markdown instead of generating")
    parser.add_argument(
        "--regen-ideas",
        action="store_true",
        help="Force regenerating ideas markdown even if the default ideas file already exists",
    )
    parser.add_argument("--moonshot-api-key", default=None, help="Moonshot API key (prefer env MOONSHOT_API_KEY)")
    parser.add_argument("--moonshot-model", default="kimi-k2.6", help="Moonshot model (default: k2.5)")
    parser.add_argument("--username", default=None, help="BRAIN username/email (override config/env)")
    parser.add_argument("--password", default=None, help="BRAIN password (override config/env)")
    parser.add_argument(
        "--max-fields",
        type=int,
        default=None,
        help="If set, pass TOP N fields to LLM; if omitted, randomly sample 50 (or all if <50)",
    )
    parser.add_argument(
        "--no-operators-in-prompt",
        action="store_true",
        help="Do not include allowed_operators in the idea-generation prompt",
    )
    parser.add_argument(
        "--max-operators",
        type=int,
        default=300,
        help="Max filtered operators to include in prompt (default: 300)",
    )
    parser.add_argument(
        "--pipeline-mode",
        default="single",
        choices=["single", "phased", "skeleton"],
        help=("Pipeline mode. 'single' = one-shot LLM call (default). "
              "'phased' = 3-phase split (structure→mapping→report) for long prompts. "
              "'skeleton' = P0 slot-filling: LLM picks fields/skeleton/window/sign, "
              "code assembles expressions (syntax guaranteed, semantic lint applied)."),
    )
    parser.add_argument(
        "--skeleton-slots",
        type=int,
        default=40,
        help="Skeleton mode: number of slot entries to request from LLM (default: 40).",
    )
    parser.add_argument(
        "--skeleton-window-pool",
        default=None,
        help="Skeleton mode: path to JSON file {freq: [w1, ...]} overriding default window pools "
             "(e.g. {\"daily\": [5, 10, 21]}); only listed domains are overridden.",
    )
    parser.add_argument(
        "--no-region-priors",
        action="store_true",
        help="Skeleton/single mode: do not inject region profile priors into the prompt.",
    )
    parser.add_argument(
        "--model-for-structure",
        default=None,
        help="Model for Phase 1 (structure parse). Defaults to --moonshot-model. "
             "Use a non-reasoning model (e.g. deepseek-chat-v3.2) for speed.",
    )
    parser.add_argument(
        "--model-for-mapping",
        default=None,
        help="Model for Phase 2 (field mapping). Defaults to --moonshot-model. "
             "Use a non-reasoning model for speed.",
    )
    parser.add_argument(
        "--model-for-report",
        default=None,
        help="Model for Phase 3 (report generation). Defaults to --moonshot-model.",
    )
    parser.add_argument(
        "--compact-operators",
        action="store_true",
        help=("SOLUTION C: Use compact operator summary (name|category|1-line) "
              "instead of full operator definitions in prompt."),
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Fields per batch in phased mode (default: 50). SOLUTION B.",
    )
    parser.add_argument(
        "--priors-file",
        default=None,
        help=("JSON with wins[] / dead_ends[] for concept-first generation. "
              "Optional: if omitted, priors are read from DB ledger key "
              "priors_snapshot_<region> (written by campaign.py assemble-priors --snapshot); "
              "file is a fallback only when DB has no snapshot."),
    )
    parser.add_argument(
        "--max-expressions",
        type=int,
        default=24,
        help="Cap implement_idea expansion per template (default 24)",
    )
    parser.add_argument(
        "--require-operators",
        default=None,
        help=("Comma-separated operators (e.g. ts_arg_max,ts_arg_min): best-effort nudge for GEM "
              "to prefer these operators in >= --require-count final expressions; the authoritative "
              "diversity guarantee is the build_wave contract skeleton injection (layer ②)."),
    )
    parser.add_argument(
        "--require-count",
        type=int,
        default=2,
        help="Min expressions that must use --require-operators (default 2)",
    )
    parser.add_argument(
        "--template-family",
        default=None,
        help=("Template family id from toolkit config/template_families.json "
              "(e.g. event_conviction_ratio / continuous_spread_pair). When provided, "
              "field binding pool is filtered by the family's field_profile_match "
              "conditions using field_profile from data/wqb.db (shape-driven routing). "
              "Omit to disable profile filtering (backward compatible)."),
    )

    args = parser.parse_args()
    priors = load_priors(args.priors_file, region=args.region)

    # --- S1⇄S2 状态机（代码级，不再依赖 agent 记得传 --ideas-file）---
    # 无显式 --ideas-file 且未强制重生成时，自查 s1_<ds>_d<delay> ledger：
    # 命中且 ideas_md_path 可读 → 自动注入，跳过内部 ideas 生成；
    # 未命中/不可读 → 走自含生成，跑完后回写 ledger（见尾部 upsert_ledger）。
    # skeleton 模式不消费 ideas 文件，跳过注入但仍允许读 whitelist。
    s1_key = f"s1_{args.dataset_id}_d{args.delay}"
    s1_record = None
    try:
        _st = _wqb_campaign_store()
        try:
            _rec = _st.get_ledger(args.region, s1_key)
        finally:
            _st.close()
        if isinstance(_rec, dict):
            s1_record = _rec
    except Exception as exc:
        print(f"[s1] ledger 自查不可用（{exc}），按无记录处理", flush=True)

    _tpl_sources = ("feature_engineering_node", "standalone", "standalone_v2")
    _s1_src = str((s1_record or {}).get("source") or "").strip()
    _s1_is_template = any(_s1_src == t or _s1_src.startswith(t + " ") or _s1_src.startswith(t + "(")
                          for t in _tpl_sources)
    if s1_record and _s1_is_template and not args.ideas_file:
        # 2026-09-15 ②：模板渲染文档（feature_engineering.py，无 LLM）不再自动注入，
        # 否则本管线一行 LLM 都不调、整波退化为 8 个模板的占位符展开。
        print(f"[s1] ledger {s1_key} 命中但 source={_s1_src!r} 是模板渲染文档，"
              f"不注入 --ideas-file，改走概念优先自含生成", flush=True)
    elif s1_record and not args.ideas_file and not args.regen_ideas and args.pipeline_mode != "skeleton":
        _p = str(s1_record.get("ideas_md_path") or "").strip()
        if _p and Path(_p).exists():
            args.ideas_file = _p
            print(
                f"[s1] ledger {s1_key} 命中（source={s1_record.get('source')}），"
                f"自动注入 --ideas-file: {_p}",
                flush=True,
            )
        else:
            print(f"[s1] ledger {s1_key} 命中但 ideas_md_path 不可读（{_p or '空'}），改走自含生成", flush=True)

    config_path = FEATURE_IMPLEMENTATION_DIR / "config.json"
    email, password = load_brain_credentials_from_env_or_args(args.username, args.password, config_path)
    session = start_brain_session(email, password)

    # Always rerun cleanly: remove prior generated artifacts so we never reuse stale ideas/data.
    # - If --ideas-file is provided, we treat it as user-managed input and do NOT delete it.
    # - We DO delete the dataset-specific folder under feature-implementation/data.
    if not args.ideas_file:
        default_ideas = (
            FEATURE_ENGINEERING_DIR
            / "output_report"
            / f"{args.region}_delay{args.delay}_{args.dataset_id}_ideas.md"
        )
        delete_path_if_exists(default_ideas)

    guessed_dataset_folder = f"{safe_dataset_id(args.dataset_id)}_{args.region}_delay{args.delay}"
    guessed_dataset_dir = FEATURE_IMPLEMENTATION_DIR / "data" / guessed_dataset_folder
    delete_path_if_exists(guessed_dataset_dir)

    ideas_path = None
    skeleton_result = None  # skeleton 模式的产物（expressions/metas/dropped/layers）
    single_shot_prompts = None  # single-shot 最近一次 (system, user) prompt（反馈重试用）
    if args.ideas_file:
        ideas_path = Path(args.ideas_file).resolve()
        if not ideas_path.exists():
            raise FileNotFoundError(f"Ideas file not found: {ideas_path}")
    else:
        # Always regenerate ideas (never reuse an existing markdown report).
        datasets_df = ace_lib.get_datasets(
            session,
            instrument_type=args.instrument_type,
            region=args.region,
            delay=args.delay,
            universe=args.universe,
            theme="ALL",
        )

        dataset_name = None
        dataset_description = None
        id_col = pick_first_present_column(datasets_df, ["id", "dataset_id", "datasetId"])
        name_col = pick_first_present_column(datasets_df, ["name", "dataset_name", "datasetName"])
        desc_col = pick_first_present_column(datasets_df, ["description", "desc", "dataset_description"])
        if id_col:
            matched = datasets_df[datasets_df[id_col].astype(str) == str(args.dataset_id)]
            if not matched.empty:
                row = matched.iloc[0]
                dataset_name = row.get(name_col) if name_col else None
                dataset_description = row.get(desc_col) if desc_col else None

        fields_df = ace_lib.get_datafields(
            session,
            instrument_type=args.instrument_type,
            region=args.region,
            delay=args.delay,
            universe=args.universe,
            dataset_id=args.dataset_id,
            data_type=args.data_type,
        )

        feature_engineering_skill_md = read_text_optional(FEATURE_ENGINEERING_DIR / "SKILL.md")
        feature_implementation_skill_md = read_text_optional(FEATURE_IMPLEMENTATION_DIR / "SKILL.md")
        allowed_metric_suffixes = build_allowed_metric_suffixes(fields_df, max_suffixes=300)

        allowed_operators = []
        if not args.no_operators_in_prompt:
            try:
                operators_df = ace_lib.get_operators(session)
                keep_vector = _vector_ratio_from_datafields_df(fields_df) > 0.5
                _, allowed_ops, _ = filter_operators_df(operators_df, keep_vector=keep_vector)
                if args.max_operators is not None and args.max_operators > 0:
                    allowed_operators = allowed_ops[: args.max_operators]
                else:
                    allowed_operators = allowed_ops
            except Exception as exc:
                print(f"Warning: failed to fetch/filter operators; using DEFAULT_OPERATORS fallback. Error: {exc}", file=sys.stderr)
        if not allowed_operators:
            print("[operators] Empty operator set — falling back to DEFAULT_OPERATORS (32 ops)", flush=True)
            allowed_operators = DEFAULT_OPERATORS

        api_key = (
            args.moonshot_api_key
            or os.environ.get("MOONSHOT_API_KEY")
        )
        if not api_key:
            raise ValueError("Moonshot API key missing. Set MOONSHOT_API_KEY or pass --moonshot-api-key")

        # Determine phase-specific models (Solution D)
        model_structure = args.model_for_structure or args.moonshot_model
        model_mapping = args.model_for_mapping or args.moonshot_model
        model_report = args.model_for_report or args.moonshot_model

        # ---- SKELETON MODE (P0: 骨架枚举 + LLM 语义填槽) ----
        if args.pipeline_mode == "skeleton":
            print(f"[skeleton-mode] model={args.moonshot_model}, "
                  f"slots={args.skeleton_slots}, priors={'off' if args.no_region_priors else 'on'}",
                  flush=True)
            window_pool = None
            if args.skeleton_window_pool:
                with open(args.skeleton_window_pool, "r", encoding="utf-8") as _f:
                    window_pool = json.load(_f)
                print(f"[skeleton-mode] window_pool override: {window_pool}", flush=True)
            ideas_path, skeleton_result = run_skeleton_generation(
                api_key=api_key,
                model=args.moonshot_model,
                dataset_id=args.dataset_id,
                region=args.region,
                delay=args.delay,
                fields_df=fields_df,
                n_slots=args.skeleton_slots,
                use_priors=not args.no_region_priors,
                window_pool=window_pool,
            )

        # ---- PHASED PIPELINE MODE (Solutions A+B+C+D) ----
        elif args.pipeline_mode == "phased":
            print(f"[phased-mode] Structure model={model_structure}, "
                  f"Mapping model={model_mapping}, Report model={model_report}, "
                  f"Batch size={args.batch_size}", flush=True)
            report = run_phased_pipeline(
                api_key=api_key,
                model_structure=model_structure,
                model_mapping=model_mapping,
                model_report=model_report,
                dataset_id=args.dataset_id,
                dataset_name=dataset_name,
                dataset_description=dataset_description,
                data_category=args.data_category,
                region=args.region,
                delay=args.delay,
                universe=args.universe,
                data_type=args.data_type,
                fields_df=fields_df,
                allowed_operators=allowed_operators,
                allowed_metric_suffixes=allowed_metric_suffixes,
                timeout_s=300,
                priors=priors,
                batch_size=args.batch_size,
            )
        else:
            # ---- SINGLE-SHOT MODE (default, original behavior) ----
            current_max_fields = args.max_fields  # None means all
            max_token_retries = 5
            report = None

            # If compact operators requested (Solution C), replace allowed_operators
            ops_for_prompt = allowed_operators
            if args.compact_operators:
                ops_summary = build_compact_operator_summary(allowed_operators)
                print(f"[compact-ops] Operator summary: {len(ops_summary)} chars", flush=True)
                # In single-shot mode, we still pass full operators but note it
                # (compact summary is primarily for phased mode)

            # P2: region priors injection (single-shot mode)
            region_priors = ""
            if not args.no_region_priors:
                region_priors = skeletons.load_region_priors(args.region)
                if region_priors:
                    print(f"[priors] region priors loaded for {args.region} ({len(region_priors)} chars)", flush=True)

            for token_attempt in range(max_token_retries + 1):
                fields_summary, field_count = build_field_summary(fields_df, max_fields=current_max_fields)
                n_fields_in_prompt = len(fields_summary)

                # 数据集形状画像（稀疏事件型判定）→ 注入 concept_first_rules 的形状约束。
                # 来源：ledger s1_profile_<dataset>（field_profile_backfill 写入）；读不到则 None（不注入）。
                _data_profile = None
                try:
                    _st = _wqb_campaign_store()
                    try:
                        _data_profile = _st.get_ledger(args.region, f"s1_profile_{args.dataset_id}")
                        if not _data_profile:
                            _data_profile = _st.dataset_shape_summary(args.region, args.dataset_id)
                    finally:
                        try:
                            _st.close()
                        except Exception:
                            pass
                except Exception:
                    _data_profile = None

                system_prompt, user_prompt = build_prompt(
                    dataset_id=args.dataset_id,
                    dataset_name=dataset_name,
                    dataset_description=dataset_description,
                    data_category=args.data_category,
                    region=args.region,
                    delay=args.delay,
                    universe=args.universe,
                    data_type=args.data_type,
                    fields_summary=fields_summary,
                    field_count=field_count,
                    feature_engineering_skill_md=feature_engineering_skill_md,
                    feature_implementation_skill_md=feature_implementation_skill_md,
                    allowed_metric_suffixes=allowed_metric_suffixes,
                    allowed_operators=ops_for_prompt,
                    priors=priors,
                    region_priors=region_priors,
                    require_ops=([o.strip() for o in args.require_operators.split(",") if o.strip()]
                                 if args.require_operators else None),
                    require_count=args.require_count,
                    data_profile=_data_profile,
                )

                last_system_prompt, last_user_prompt = system_prompt, user_prompt
                try:
                    report = call_moonshot(api_key, args.moonshot_model, system_prompt, user_prompt)
                    single_shot_prompts = (last_system_prompt, last_user_prompt)
                    break
                except Exception as exc:
                    err_msg = str(exc).lower()
                    is_token_error = any(kw in err_msg for kw in ("token", "context_length", "too long", "too large", "413", "400"))
                    if is_token_error and n_fields_in_prompt > 10:
                        current_max_fields = max(10, n_fields_in_prompt // 2)
                        print(
                            f"[token-limit] Reducing fields from {n_fields_in_prompt} to {current_max_fields} "
                            f"(attempt {token_attempt + 1}/{max_token_retries})",
                            file=sys.stderr,
                        )
                        continue
                    raise

            if report is None:
                raise RuntimeError("Failed to get LLM response after reducing fields.")

        # Save first, then normalize placeholders after dataset download.
        # skeleton 模式已由 run_skeleton_generation 内部落盘 ideas（且 report 未定义），跳过重复保存。
        if skeleton_result is None:
            ideas_path = save_ideas_report(report, args.region, args.delay, args.dataset_id)

    ideas_text = ideas_path.read_text(encoding="utf-8")

    # Ensure metadata exists for downstream parsing/reuse.
    ideas_text = ensure_metadata_block(ideas_text, dataset_id=args.dataset_id, region=args.region, delay=args.delay)
    ideas_path.write_text(ideas_text, encoding="utf-8")

    # Parse metadata
    dataset_id_match = re.search(r"\*\*Dataset\*\*:\s*(\S+)", ideas_text)
    dataset_id = dataset_id_match.group(1) if dataset_id_match else args.dataset_id

    # Download dataset for implementation
    fetch_script = FEATURE_IMPLEMENTATION_SCRIPTS / "fetch_dataset.py"
    run_script(
        [
            sys.executable,
            str(fetch_script),
            "--datasetid",
            dataset_id,
            "--region",
            args.region,
            "--delay",
            str(args.delay),
            "--universe",
            args.universe,
            "--instrument-type",
            args.instrument_type,
            "--data-type",
            args.data_type,
        ],
        cwd=FEATURE_IMPLEMENTATION_SCRIPTS,
    )

    dataset_folder = f"{safe_dataset_id(dataset_id)}_{args.region}_delay{args.delay}"

    # If the ideas file references a different dataset id than the CLI args,
    # ensure we also clean that dataset folder before fetching.
    if dataset_folder != guessed_dataset_folder:
        delete_path_if_exists(FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder)

    dataset_csv_path = FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder / f"{dataset_folder}.csv"
    if not dataset_csv_path.exists():
        raise RuntimeError(
            "Dataset CSV was not created by fetch_dataset.py. "
            f"Expected: {dataset_csv_path}"
        )
    dataset_ids = load_dataset_ids_from_csv(dataset_csv_path)

    # --- S1 field_whitelist 生效：收窄占位符合法集 + implement_idea 绑定池 ---
    # 白名单来自 s1_<ds>_d<delay> ledger（standalone S1 或 s2_nested 回写）。
    # 与数据集字段零交集时忽略白名单并告警（防 S1 陈旧决策把绑定池清空）。
    bind_ids = dataset_ids
    whitelist_path = None
    if s1_record and dataset_ids:
        raw_wl = s1_record.get("field_whitelist")
        if _s1_is_template:
            # 2026-09-15 ②/⑤：模板渲染 S1 记录的 field_whitelist 是文档白名单块的**前 30 行（字母序）**
            # ——GBR intraday_pv_feats 实测 30 条全是 *_ask_price_*。不再拿它收窄绑定池；
            # 改用 store 的跨簇候选池 s2_field_pool_<ds>（builder_version>=2），没有就用全目录。
            raw_wl = None
            try:
                _st2 = _wqb_campaign_store()
                try:
                    _pool = _st2.get_ledger(args.region, f"s2_field_pool_{args.dataset_id}")
                finally:
                    _st2.close()
                if isinstance(_pool, dict) and int(_pool.get("builder_version") or 0) >= 2:
                    raw_wl = _pool.get("candidate_field_pool")
                    print(f"[s1] 模板渲染记录：改用跨簇候选池 s2_field_pool_{args.dataset_id}"
                          f"（{len(raw_wl or [])} 字段，覆盖 {_pool.get('clusters_covered')} 簇）作绑定白名单", flush=True)
                else:
                    print("[s1] 模板渲染记录：无版本化候选池，绑定池 = 全目录字段", flush=True)
            except Exception as _exc:
                print(f"[s1] 候选池读取异常（{_exc}），绑定池 = 全目录字段", flush=True)
        wl_ids = [str(x).strip() for x in raw_wl if str(x).strip()] if isinstance(raw_wl, list) else []
        if wl_ids:
            ds_set = set(dataset_ids)
            in_pool = [f for f in wl_ids if f in ds_set]
            missing = [f for f in wl_ids if f not in ds_set]
            if in_pool:
                bind_ids = in_pool
                whitelist_path = FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder / "s1_field_whitelist.json"
                whitelist_path.write_text(json.dumps(bind_ids, ensure_ascii=False, indent=1), encoding="utf-8")
                print(
                    f"[s1] field_whitelist 生效: 绑定池 {len(dataset_ids)} -> {len(bind_ids)} 字段"
                    + (f"；{len(missing)} 个白名单 id 不在本数据集（忽略）: {missing[:5]}" if missing else ""),
                    flush=True,
                )
            else:
                print(f"[s1] warn: field_whitelist（{len(wl_ids)} 个）与数据集字段零交集，忽略白名单", flush=True)

    allowed_suffixes = build_allowed_suffixes_from_ids(bind_ids, max_suffixes=300) if bind_ids else []
    dataset_code = detect_dataset_code(dataset_ids) if dataset_ids else None

    # --- 字段画像注入（2026-09-11）：供 implement_idea 孤字段增强的稀疏事件门控 ---
    # 从 DB 读 field_profile_map（webdatascope 体检回填，含 shape/coverage），
    # 写临时 JSON 传 --field-profile。画像缺失时跳过（孤字段增强降级为不加门控）。
    orphan_fp_path = None
    try:
        _store = _wqb_campaign_store()
        try:
            _profile_map = _store.get_field_profile_map(args.region, dataset_id)
        finally:
            try:
                _store.close()
            except Exception:
                pass
        if _profile_map:
            orphan_fp_path = FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder / "orphan_field_profile.json"
            orphan_fp_path.write_text(json.dumps(_profile_map, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[orphan] field_profile 注入: {len(_profile_map)} 字段画像（稀疏事件门控用）", flush=True)
    except Exception as exc:
        print(f"[orphan] warn: 读取 field_profile 失败（{exc}），孤字段增强不加门控", flush=True)
        orphan_fp_path = None

    if args.pipeline_mode == "skeleton":
        # ---- SKELETON MODE: 直写 idea JSON + final_expressions + meta，绕过模板展开 ----
        if skeleton_result is None:
            raise ValueError("--ideas-file is not supported in skeleton mode; skeleton mode generates its own ideas.")
        data_dir = FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder
        data_dir.mkdir(parents=True, exist_ok=True)
        ts_tag = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        exprs = skeleton_result["expressions"]
        idea_payload_sk = {
            "template": "skeleton_mode",
            "idea": (f"skeleton-mode slot filling: {len(exprs)} expressions, "
                     f"dropped={skeleton_result['dropped']}"),
            "expression_list": exprs,
            # 骨架归因持久化（2026-09-13）：供 _load_skeleton_stats 聚合实测胜率；
            # expr 已与最终表达式对齐（vec 包裹/wrapper 替换后的映射见 meta 同步逻辑）。
            "skeleton_metas": skeleton_result["metas"],
        }
        idea_json_path = data_dir / f"{dataset_folder}_idea_{ts_tag}.json"
        idea_json_path.write_text(json.dumps(idea_payload_sk, ensure_ascii=False, indent=4), encoding="utf-8")
        (data_dir / "final_expressions.json").write_text(
            json.dumps(exprs, ensure_ascii=False, indent=4), encoding="utf-8")
        (data_dir / "final_expressions_meta.json").write_text(
            json.dumps(skeleton_result["metas"], ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[skeleton] wrote {len(exprs)} expressions + meta + idea JSON to {data_dir.name}/", flush=True)
        # 供下方 DB idea_payload 使用
        templates = ["skeleton_mode"]
        template_to_idea = {"skeleton_mode": idea_payload_sk["idea"]}
    else:
        # Extract {template, idea} pairs from **Concept** blocks.
        block_pairs = extract_template_blocks(ideas_text)
        if not block_pairs:
            raise ValueError("No **Concept** blocks with **Implementation Example** found in the ideas file.")

        normalized_pairs, rejected_templates = _normalize_template_pairs(
            block_pairs, dataset_ids, allowed_suffixes, dataset_code)

        # 字段名拼接幻觉可观测性（2026-09-12）：被拒模板不再静默丢弃。
        if rejected_templates:
            print(f"[validate] 丢弃 {len(rejected_templates)}/{len(block_pairs)} 个模板"
                  f"（占位符无法匹配真实字段，疑似字段名拼接幻觉）:", flush=True)
            for _t in rejected_templates[:8]:
                print(f"[validate]   - {_t}", flush=True)

        # S1 概念字段 ⊄ field_whitelist 显式告警（2026-09-13）：白名单收窄绑定池会把
        # 不在池内的概念字段静默丢弃（GLB fundamental23 实测：8 个概念字段只有 2 个
        # 在池内，整波退化为 2 字段的孤字段增强）。此处对“模板占位符是真实数据集
        # 字段、但不在生效白名单”的情况告警，暴露 S1 概念与候选池的口径分叉。
        if whitelist_path is not None and block_pairs:
            _ds_set = set(dataset_ids or [])
            _wl_set = set(bind_ids or [])
            _outside = sorted({
                ph for item in block_pairs
                for ph in re.findall(r"\{([A-Za-z0-9_]+)\}", str(item.get("template") or ""))
                if ph in _ds_set and ph not in _wl_set
            })
            if _outside:
                print(
                    f"[s1] warn: {len(_outside)} 个概念模板字段不在 field_whitelist 绑定池"
                    f"（相关模板将无候选/降级模糊匹配）: {_outside[:8]}",
                    flush=True,
                )

        # 生成-校验反馈闭环（2026-09-12）：全部模板被拒时，带拒绝清单重生成一次。
        # 仅 single-shot 自含生成路径适用（--ideas-file / skeleton / phased 不重置）。
        if not normalized_pairs and rejected_templates and single_shot_prompts is not None:
            print("[feedback-retry] 全部模板被拒，带错误清单重生成一次...", flush=True)
            fb_sys, fb_user = single_shot_prompts
            fb_user = fb_user + (
                "\n\n---\n\nCRITICAL REPAIR (automated validator REJECTED your previous report):\n"
                f"{len(rejected_templates)} of your Implementation Example templates used placeholders "
                "that match NO real field id (typical cause: concatenating two field names into ONE placeholder).\n"
                "Rejected templates:\n"
                + "\n".join(f"  - {_t}" for _t in rejected_templates[:10])
                + "\nRULES: every {placeholder} MUST be an EXACT suffix from allowed_placeholders. "
                "If a concept needs two fields, use TWO separate placeholders. "
                "Rewrite the FULL report (with metadata + all mandatory sections) using valid templates only."
            )
            report = call_moonshot(api_key, args.moonshot_model, fb_sys, fb_user)
            ideas_path = save_ideas_report(report, args.region, args.delay, args.dataset_id)
            ideas_text = ideas_path.read_text(encoding="utf-8")
            ideas_text = ensure_metadata_block(ideas_text, dataset_id=args.dataset_id, region=args.region, delay=args.delay)
            ideas_path.write_text(ideas_text, encoding="utf-8")
            block_pairs = extract_template_blocks(ideas_text)
            normalized_pairs, rejected_templates = _normalize_template_pairs(
                block_pairs, dataset_ids, allowed_suffixes, dataset_code)
            print(f"[feedback-retry] 重生成后有效模板 {len(normalized_pairs)}/{len(block_pairs)}"
                  f"（仍被拒 {len(rejected_templates)}）", flush=True)

        if not normalized_pairs:
            raise ValueError("No valid templates remain after normalization/validation.")

        # 2026-09-01 expected_exposure 兜底（详见下方调用处注释）
        template_to_idea = {t: txt for t, txt in normalized_pairs}

        # De-dup by template; keep the first non-empty idea.
        template_to_idea: dict[str, str] = {}
        for t, idea_text in normalized_pairs:
            if t not in template_to_idea or (not template_to_idea[t] and idea_text):
                template_to_idea[t] = idea_text

        # 2026-09-01 expected_exposure 兜底：LLM 有时漏写 **Expected Exposure** 行
        # （实测 520 条 idea 仅 14% 覆盖，gate 收益来源多样性闸长期降级 WARN）。
        # 此处对缺失项按 Concept/Mechanism 关键词推断标签并显式追加该行，
        # 保证 idea ledger 每条都带 exposure，下游 gate._extract_exposure_from_idea 可直接消费。
        template_to_idea = {t: _ensure_expected_exposure(txt) for t, txt in template_to_idea.items()}

        templates = sorted(template_to_idea.keys())

        implement_script = FEATURE_IMPLEMENTATION_SCRIPTS / "implement_idea.py"

        # 字段画像驱动模板族（可选）：--template-family 指定时，按族 mechanism_premise
        # 过滤绑定池（形状+语义双校验）。默认不启用，向后兼容。
        # 机制⇄数据类别匹配门：不匹配则拦截整个生成（烧配额前）。
        family_fp_path = None
        family_fm_path = None
        if getattr(args, "template_family", None):
            family_fp_path, family_fm_path = _prepare_family_binding(
                args.region, dataset_id, args.template_family,
                FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder,
                data_category=args.data_category,
            )
            if family_fp_path == "BLOCKED":
                raise ValueError(
                    f"模板族 '{args.template_family}' 与数据集 '{dataset_id}' "
                    f"(category={args.data_category}) 机制前提不匹配，已拦截生成：{family_fm_path}"
                )

        for template in templates:
            idea_text = template_to_idea.get(template, "")
            cmd = [
                sys.executable,
                str(implement_script),
                "--template",
                template,
                "--dataset",
                dataset_folder,
                "--idea",
                idea_text,
                "--max-expressions",
                str(args.max_expressions),
            ]
            if whitelist_path is not None:
                cmd += ["--field-whitelist", str(whitelist_path)]
            if family_fp_path is not None and family_fm_path is not None:
                cmd += ["--field-profile", family_fp_path, "--family-match", family_fm_path]
            elif orphan_fp_path is not None:
                # 孤字段增强画像注入（无 family_match 时独立传 field_profile，供稀疏事件门控）
                cmd += ["--field-profile", str(orphan_fp_path)]
            run_script(cmd, cwd=FEATURE_IMPLEMENTATION_SCRIPTS)

        merge_script = FEATURE_IMPLEMENTATION_SCRIPTS / "merge_expression_list.py"
        run_script(
            [
                sys.executable,
                str(merge_script),
                "--dataset",
                dataset_folder,
            ],
            cwd=FEATURE_IMPLEMENTATION_SCRIPTS,
        )

    final_path = FEATURE_IMPLEMENTATION_DIR / "data" / dataset_folder / "final_expressions.json"
    if final_path.exists():
        try:
            raw = json.loads(final_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RuntimeError(f"Failed to read final expressions: {final_path}. Error: {exc}")

        expressions = raw if isinstance(raw, list) else []

        # VECTOR 数据集兜底：LLM 未必遵守 prompt 的 vec_* 指示，落盘前自动裹聚合。
        vector_fields: list[str] = []
        if str(args.data_type).upper() == "VECTOR" and wrap_naked_vectors is not None:
            try:
                import pandas as pd  # 局部导入，避免无 pandas 环境影响 MATRIX 路径
                fdf = pd.read_csv(dataset_csv_path)
                idc = pick_first_present_column(fdf, ["id", "field_id", "fieldId"])
                tyc = pick_first_present_column(fdf, ["type", "dataType", "data_type"])
                if idc and tyc:
                    vector_fields = fdf.loc[fdf[tyc].astype(str).str.upper() == "VECTOR", idc] \
                        .dropna().astype(str).tolist()
            except Exception as exc:
                print(f"[vector-fix] warn: 无法读取 VECTOR 字段清单，跳过自动修复: {exc}")
                vector_fields = []

        validator = ExpressionValidator()
        valid_expressions: list[str] = []
        expr_map: dict[str, str] = {}  # 原始 expr -> 裹 vec_* 后的 expr（skeleton meta 对齐用）
        invalid_count = 0
        fixed_count = 0
        for expr in expressions:
            if not isinstance(expr, str) or not expr.strip():
                invalid_count += 1
                continue
            e = expr.strip()
            orig = e
            if vector_fields:
                e2, wrapped = wrap_naked_vectors(e, vector_fields)
                if wrapped:
                    fixed_count += 1
                    e = e2
            result = validator.check_expression(e)
            if result.get("valid"):
                valid_expressions.append(e)
                expr_map[orig] = e
            else:
                invalid_count += 1

        # 2026-09-03 骨架多样性后处理：检测外层 wrapper 是否全部相同，如果是则强制替换
        # 根因：ideas 阶段的 Implementation Example 已包含具体算子（如 quantile），
        #       GEM 表达式生成只是机械展开模板（template.format），没有改变算子，
        #       导致 LLM 在 ideas 阶段用的算子（quantile）被原样保留到最终表达式。
        # 解决：检测外层 wrapper 同质化，强制替换 30% 为多样 wrapper。
        if valid_expressions:
            import re as _re
            from collections import Counter as _Counter
            
            def _get_outer_wrapper(expr: str) -> str:
                m = _re.match(r'(\w+)\(', expr)
                return m.group(1) if m else 'unknown'
            
            wrappers = [_get_outer_wrapper(e) for e in valid_expressions]
            wrapper_counts = _Counter(wrappers)
            most_common_wrapper, most_common_count = wrapper_counts.most_common(1)[0]
            total = len(valid_expressions)
            
            # 如果最常用 wrapper 占比 >70%，强制替换 30% 为多样 wrapper
            if most_common_count / total > 0.7:
                print(f"[skeleton-diversity] 检测到外层 wrapper 同质化: {most_common_wrapper} 占比 {most_common_count}/{total} ({most_common_count/total:.1%})", flush=True)
                
                # 多样 wrapper 池（BRAIN 标准算子）
                diverse_wrappers = [
                    ('rank', lambda inner: f'rank({inner})'),
                    ('ts_zscore', lambda inner: f'ts_zscore({inner}, 22)'),
                    ('group_rank', lambda inner: f'group_rank({inner}, subindustry)'),
                    ('winsorize', lambda inner: f'winsorize(rank({inner}), std=4)'),
                    ('ts_quantile', lambda inner: f'ts_quantile({inner}, 22, driver="gaussian")'),
                ]
                
                # 计算需要替换的数量（30%）
                num_to_replace = max(1, int(total * 0.3))
                replaced = 0
                
                # 从最常用 wrapper 的表达式中随机选择替换
                import random as _random
                _random.seed(42)  # 确定性
                indices = [i for i, w in enumerate(wrappers) if w == most_common_wrapper]
                _random.shuffle(indices)
                
                for idx in indices[:num_to_replace]:
                    orig_expr = valid_expressions[idx]
                    # 提取内层表达式（去掉外层 wrapper）
                    m = _re.match(r'\w+\((.*)\)', orig_expr)
                    if not m:
                        continue
                    inner = m.group(1)
                    # 去掉 quantile 的 driver 参数
                    inner = _re.sub(r',\s*driver\s*=\s*"[^"]*"\s*$', '', inner)
                    
                    # 选择一个多样 wrapper（轮转）
                    wrapper_name, wrapper_fn = diverse_wrappers[replaced % len(diverse_wrappers)]
                    new_expr = wrapper_fn(inner)
                    
                    # 验证新表达式
                    if validator.check_expression(new_expr).get("valid"):
                        old_expr = valid_expressions[idx]
                        valid_expressions[idx] = new_expr
                        # 2026-09-12 修复：同步改写 expr_map，保证 skeleton meta 对齐
                        # 不因 wrapper 替换而失配（原实现只改列表，meta 仍指向旧表达式）。
                        for _k, _v in list(expr_map.items()):
                            if _v == old_expr:
                                expr_map[_k] = new_expr
                        replaced += 1
                        print(f"[skeleton-diversity] 替换 #{idx}: {most_common_wrapper} -> {wrapper_name}", flush=True)
                
                print(f"[skeleton-diversity] 强制替换 {replaced}/{num_to_replace} 条表达式的外层 wrapper", flush=True)

        # ③ 算子多样性 best-effort 补注（次保障，--require-operators）：GEM 输出命中不足时，
        #    用绑定池 top 字段按已知算子形状自动补注。注意：此处的"硬保证"仅对 _shapes 已定义
        #    且绑定池非空的算子成立，且只补到 require_count 条；真正的全量结构性保证在
        #    ② (build_wave 契约注入：12 算子全池 + 全数据集角色池)，③ 只是锦上添花，
        #    绝不能替代 ②，也不应被理解为 GEM 必须独自满足闸门。
        if args.require_operators:
            req_ops = [o.strip() for o in args.require_operators.split(",") if o.strip()]
            _pat = re.compile(r"\b(" + "|".join(re.escape(o) for o in req_ops) + r")\s*\(")
            hits = sum(1 for e in valid_expressions if _pat.search(e))
            if hits < args.require_count:
                _pool_ids = [f for f in (bind_ids or dataset_ids or []) if isinstance(f, str) and f]
                _is_vec = str(args.data_type).upper() == "VECTOR"

                def _sig(f: str) -> str:
                    return f"vec_avg({f})" if _is_vec else f

                _shapes = {
                    "ts_arg_max": "quantile(-ts_arg_max(ts_backfill({s}, 66), 22))",
                    "ts_arg_min": "quantile(ts_arg_min(ts_backfill({s}, 66), 22))",
                    "ts_av_diff": "quantile(ts_av_diff(ts_backfill({s}, 66), 22))",
                    "group_rank": "group_rank(ts_backfill({s}, 66), sector)",
                    "group_zscore": "group_zscore(ts_backfill({s}, 66), sector)",
                    "group_neutralize": "group_neutralize(ts_backfill({s}, 66), sector)",
                    "group_mean": "group_mean(ts_backfill({s}, 66), sector)",
                    "group_backfill": "group_backfill({s}, sector, 22)",
                }
                _tops = _pool_ids[:2]
                _added = []
                for _op in req_ops:
                    _shape = _shapes.get(_op)
                    if not _shape:
                        print(f"[require-ops] warn: 算子 {_op} 无已知合成形状，跳过补注")
                        continue
                    for _f in _tops:
                        _cand = _shape.format(s=_sig(_f))
                        if _cand in valid_expressions or _cand in _added:
                            continue
                        if not validator.check_expression(_cand).get("valid"):
                            continue
                        _added.append(_cand)
                        if hits + len(_added) >= args.require_count:
                            break
                    if hits + len(_added) >= args.require_count:
                        break
                if _added:
                    valid_expressions.extend(_added)
                    print(f"[require-ops] 补注 {len(_added)} 条多样性表达式 "
                          f"（命中 {hits}+{len(_added)}/{args.require_count}，req={req_ops}）")
                else:
                    print(f"[require-ops] warn: 无法合成合规补注表达式"
                          f"（命中 {hits}/{args.require_count}，候选字段 {len(_pool_ids)}）")

        # ---- 生成侧预闸（2026-09-15 ②）：quantile 默认 driver 无损归一化 + 毒模式丢弃 ----
        # 闸门统计里最高频的两类 FAIL（[ARITY] quantile 312 次 / [POISON] 加权混合 74 次）
        # 全是生成侧产物；在这里拦下，闸 4/5 只作兜底。
        try:
            from pipeline_pregate import (pregate as _pregate, normalize_quantile as _norm_q,
                                          normalize_named_only as _norm_named,
                                          normalize_bucket as _norm_bucket,
                                          normalize_windows as _norm_win)
            valid_expressions, _pg = _pregate(valid_expressions, region=args.region)
            # 同步 expr_map（skeleton meta 对齐）：被归一化改写的表达式更新映射，被丢弃的移除
            # （2026-09-19：与 pregate 内部同序应用全部无损归一化，否则映射对不上被误删）
            def _same_norm(_v):
                _v, _ = _norm_q(_v)
                _v, _ = _norm_named(_v)
                _v, _, _ = _norm_bucket(_v)
                _v, _, _ = _norm_win(_v)
                return _v
            _kept_set = set(valid_expressions)
            for _k, _v in list(expr_map.items()):
                _v2 = _same_norm(_v)
                if _v2 in _kept_set:
                    expr_map[_k] = _v2
                else:
                    expr_map.pop(_k, None)
            print(f"[pregate] in={_pg['in']} kept={_pg['kept']} "
                  f"quantile_normalized={_pg['quantile_normalized']} poison_dropped={_pg['poison_dropped']} "
                  f"named_arg={_pg['named_arg_normalized']} bucket_fixed/dropped={_pg['bucket_range_added']}/{_pg['bucket_dropped']} "
                  f"invalid_group_dropped={_pg['invalid_group_dropped']} windows_normalized={_pg['windows_normalized']}", flush=True)
        except Exception as _exc:
            print(f"[pregate] warn: 预闸异常，按原样落盘（闸门仍兜底）: {_exc}", flush=True)

        final_path.write_text(json.dumps(valid_expressions, ensure_ascii=False, indent=4), encoding="utf-8")
        print(f"Filtered invalid expressions: {invalid_count}")
        if fixed_count:
            print(f"[vector-wrap] 自动裹 vec_* 修复 {fixed_count} 条裸用 VECTOR 字段的表达式")

        # skeleton 模式：meta 与最终表达式对齐（剔除被 validator 滤掉的，同步 vec_* 改写）
        meta_path = final_path.parent / "final_expressions_meta.json"
        if meta_path.exists():
            try:
                metas_raw = json.loads(meta_path.read_text(encoding="utf-8"))
                if isinstance(metas_raw, list):
                    synced = []
                    for m in metas_raw:
                        if not isinstance(m, dict):
                            continue
                        mapped = expr_map.get(str(m.get("expr", "")).strip())
                        if mapped is not None:
                            m["expr"] = mapped
                            synced.append(m)
                    meta_path.write_text(json.dumps(synced, ensure_ascii=False, indent=2), encoding="utf-8")
                    print(f"[skeleton] meta 对齐: {len(synced)}/{len(metas_raw)} 条保留", flush=True)
            except Exception as exc:
                print(f"[skeleton] warn: meta 对齐失败: {exc}")

        wave = args.wave or f"s2_{dataset_id}_d{args.delay}"
        try:
            st = _wqb_campaign_store()
            try:
                st.upsert_expressions(
                    args.region, str(wave), valid_expressions,
                    dataset=dataset_id, status="gem",
                )
                idea_payload = {
                    "dataset": dataset_id,
                    "region": args.region,
                    "delay": args.delay,
                    "universe": args.universe,
                    "data_type": args.data_type,
                    "ideas_path": str(ideas_path),
                    "expression_list": valid_expressions,
                    "templates": templates,
                    "template_to_idea": template_to_idea,
                }
                st.upsert_idea(args.region, dataset_id, int(args.delay), idea_payload)
                # 自含 LLM 生成路径（非 --ideas-file 注入、非 skeleton）→ 回写 s1 ledger（source=s2_nested）。
                # field_whitelist = 表达式实际引用字段 ∩ 数据集字段，供下次 S2 收窄绑定池。
                if not args.ideas_file and args.pipeline_mode != "skeleton":
                    ds_id_set = set(dataset_ids or [])
                    used_fields = sorted(
                        {tok for e in valid_expressions for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", e)}
                        & ds_id_set
                    )
                    st.upsert_ledger(args.region, s1_key, {
                        "dataset": dataset_id,
                        "region": args.region,
                        "delay": args.delay,
                        "universe": args.universe,
                        "ideas_md_path": str(ideas_path),
                        "field_whitelist": used_fields,
                        "concept_count": len(templates),
                        "source": "s2_nested",
                        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    })
                    print(f"[s1] 回写 ledger {s1_key}: whitelist={len(used_fields)} 字段, source=s2_nested", flush=True)
            finally:
                st.close()
            print(f"[db] expressions/{args.region}/{wave} n={len(valid_expressions)} status=gem")
            print(f"[db] idea ledger s2_{dataset_id}_d{args.delay}_idea")
        except Exception as exc:
            print(f"[db] GEM 入库失败: {exc}")
            raise
    else:
        print(f"Warning: final_expressions.json not found: {final_path}")

    print(f"Ideas report: {ideas_path}")
    print(f"Expressions -> db (wave={args.wave or f's2_{dataset_id}_d{args.delay}'})")


if __name__ == "__main__":
    main()
