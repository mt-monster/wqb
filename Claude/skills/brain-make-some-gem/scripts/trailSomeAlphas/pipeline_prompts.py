# -*- coding: utf-8 -*-
"""GEM prompt 构建层：single / phased 两种模式的提示词组装。

2026-09-12 从 run_pipeline.py 拆出。纯文本组装，不发起 LLM 调用
（LLM 调用统一走 pipeline_llm.call_moonshot，且需经 run_pipeline 全局名
调用以保持 headless_runner/run.py 的 monkey-patch 拦截语义）。
"""
import json
import re

from economic_priors import compact_priors_text, concept_first_rules
from pipeline_data import pick_first_present_column


def format_operators_for_prompt(allowed_operators, desc_limit: int = 160) -> str:
    """概念模式 system prompt 的算子块紧凑序列化。

    旧实现直接 f-string Python repr：单引号、description 内 \\\\r\\\\n 字面量、
    恒为 REGULAR 的 scope 字段，全是噪声。新格式每行一个 JSON 对象：
    name/category/definition（用法语法全保留）+ description（去换行、截 160 字符）。
    """
    if not allowed_operators:
        return '"allowed_operators": []'
    lines = []
    for op in allowed_operators:
        if not isinstance(op, dict):
            lines.append(json.dumps(op, ensure_ascii=False))
            continue
        entry = {"name": op.get("name"), "category": op.get("category")}
        definition = re.sub(r"\s+", " ", str(op.get("definition") or "")).strip()
        if definition:
            entry["definition"] = definition
        desc = re.sub(r"\s+", " ", str(op.get("description") or "")).strip()
        if len(desc) > desc_limit:
            desc = desc[:desc_limit].rstrip() + "…"
        if desc:
            entry["description"] = desc
        lines.append(json.dumps(entry, ensure_ascii=False))
    return '"allowed_operators": [\n' + ",\n".join(lines) + "\n]"


def build_prompt(
    dataset_id: str,
    dataset_name: str | None,
    dataset_description: str | None,
    data_category: str,
    region: str,
    delay: int,
    universe: str,
    data_type: str,
    fields_summary: list[dict],
    field_count: int,
    feature_engineering_skill_md: str,
    feature_implementation_skill_md: str,
    allowed_metric_suffixes: list[str],
    allowed_operators,
    priors: dict | None = None,
    region_priors: str = "",
    require_ops: list[str] | None = None,
    require_count: int = 2,
    data_profile: dict | None = None,
):
    # Concept-first: do NOT dump full SKILL.md (that caused field×operator wrapping).
    # Keep the 8-question checklist as a short reminder, then force mechanism → fields.
    priors = priors or {}
    fe_hint = ""
    if feature_engineering_skill_md:
        fe_hint = (
            "Use the 8 questions from feature-engineering as a checklist only: "
            "invariant / change / anomaly / interaction / structure / accumulation / relative / essence. "
            "Do not copy the skill file. Each answer must be a priced mechanism."
        )
    prompt_lines = [
            concept_first_rules(data_profile),
            fe_hint,
            compact_priors_text(priors, data_category),
            "",
            format_operators_for_prompt(allowed_operators),
            '"allowed_placeholders": ' + json.dumps(allowed_metric_suffixes, ensure_ascii=False),
            "",
        ]

    if str(data_type).upper() == "VECTOR":
        prompt_lines.append(
            "since all the following the data is vector type data, before you do any process, you should choose a vector operator to generate its statistical feature to use, the data cannot be directly use. for example, if datafieldA and datafieldB are vector type data, you can use vec_avg(datafieldA) -  vec_avg(datafieldB), where vec_avg() operator is used to generate the average of the data on a certain date. similarly, vector type operator can only be used on the vector type operator directly and cannot be nested, for example vec_avg(vec_sum(datafield)) is a false use."
        )
        vector_ops: list[str] = []
        if isinstance(allowed_operators, list):
            for op in allowed_operators:
                if not isinstance(op, dict):
                    continue
                category = str(op.get("category") or "").strip().lower()
                name = str(op.get("name") or "").strip()
                if category == "vector" and name:
                    vector_ops.append(name)

        if vector_ops:
            vector_ops = sorted(set(vector_ops), key=lambda x: x.lower())
        else:
            vector_ops = ["vec_avg", "vec_sum", "vec_max", "vec_min", "vec_std", "vec_count"]

        prompt_lines.append("the available vector operators are: " + ", ".join(vector_ops))

    if region_priors:
        prompt_lines.extend(
            [
                f"REGION PRIORS (empirical knowledge from prior campaigns in {region} - treat as strong hints for directionality and field selection):",
                region_priors,
                "",
            ]
        )

    prompt_lines.extend(
        [
            "CRITICAL OUTPUT RULES (to ensure implement_idea.py can generate expressions):",
            "- Every Implementation Example MUST be a Python format template using {variable}.",
            "- Every {variable} MUST come from the allowed_placeholders list provided in user content.",
            "- When you implement ideas, ONLY use operators from allowed_operators provided.",
            "- Do NOT include dataset codes/prefixes/horizons in {variable} (suffix-only).",
            "- If you show raw field ids in tables, use backticks `like_this`, NOT {braces}.",
            "- Include these metadata lines verbatim somewhere near the top:",
            "  **Dataset**: <dataset_id>",
            "  **Region**: <region>",
            "  **Delay**: <delay>",
            "",
            "MANDATORY SECTION STRUCTURE (for downstream parsing):",
            "Your output MUST contain these exact section headers in this order:",
            "  ## 字段（Fields）",
            "  - A markdown table listing ALL fields you reference: | Field ID | Type | Coverage | Role |",
            "  - Role must be one of: 主信号 / 辅助信号 / group/bucket / 禁用",
            "  ## 特征（Features）",
            "  - Preprocessing decisions: ts_backfill / group_zscore / group_rank / vec_* / rank / winsorize",
            "  ## 建议（Implementation Examples）",
            "  - A consolidated list of ALL Implementation Example templates from your Concepts below",
            "  - Format: `- {concept_name}: \\`template_with_{placeholder}\\``",
            "  ## 字段白名单（Field Whitelist）",
            "  - A fenced code block (```) containing ONLY the field ids you actually use, one per line",
            "  ## Concepts",
            "  - Your concept blocks with **Concept** / **Mechanism** / **Fields** / **Implementation Example** / **Direction** / **Expected Exposure**",
            "",
            "OPERATOR SYNTAX RULES (platform parser is strict):",
            "- bucket() MUST use named parameter: bucket(expr, range=\"start,end,step\") or bucket(expr, buckets=\"t1,t2,...\").",
            "  NEVER use positional string like bucket(expr, \"0.3,0.7\") — platform rejects with 'must be an expression'.",
            "  Correct: bucket(rank(cap), range=\"0,1,0.1\")  → 10 buckets (0-0.1, 0.1-0.2, ..., 0.9-1.0)",
            "  Correct: bucket(rank(cap), buckets=\"0.3,0.7\") → 3 buckets (<0.3, 0.3-0.7, >0.7)",
            "  Wrong:   bucket(rank(cap), \"0.3,0.7\")        → parse ERROR",
            "- trade_when(x, y, z): x=condition, y=alpha_when_true, z=alpha_when_false (all three required).",
            "- group_neutralize(x, group): group must be a field like industry/sector/subindustry or bucket(...) output.",
            "- quantile(x): ONE argument only. The platform default driver is already gaussian, so",
            "  quantile(x, driver=\"gaussian\") is redundant (auto-normalized) and other drivers are rejected by the campaign gate.",
            "- NEVER blend two independent signal legs with fixed weights — add(multiply(0.4, A), multiply(0.6, B)),",
            "  0.4*rank(A)+0.6*rank(B), nested add(multiply(rank(x),a), add(...)) are all BLOCKED (mixed-signal weight",
            "  tuning = overfitting). Combine legs structurally instead: ts_corr / divide / subtract / if_else /",
            "  trade_when / group_* on ONE mechanism.",
        ]
    )
    if require_ops:
        prompt_lines.append(
            f"OPERATOR DIVERSITY NUDGE (best-effort): prefer at least {require_count} of the ideas "
            f"to include an Implementation Example using one of these operators: "
            f"{', '.join(require_ops)}. NOTE: this is a soft nudge only — the authoritative "
            f"structural diversity guarantee is the build_wave contract skeleton injection "
            f"(layer ②), which deterministically injects these operators regardless of GEM output."
        )

    system_prompt = "\n".join(prompt_lines)

    # --- user prompt: compact JSON header + one plain-text line per field ---
    # (previously a pretty-printed JSON array of per-field objects; the repeated
    # keys/indentation cost ~2x the payload on wide catalogs like model25's 554 fields)
    field_types = {
        str(f.get("type")).strip()
        for f in fields_summary
        if f.get("type") not in (None, "")
    }
    uniform_type = next(iter(field_types)) if len(field_types) == 1 else None

    format_note = "fields are listed one per line after this JSON header as: field_id :: description [cov=x.xx"
    if uniform_type:
        format_note += f"]; all fields type={uniform_type}"
    else:
        format_note += " type=...]"
    if len(fields_summary) < field_count:
        format_note += (
            f"; catalog truncated to top {len(fields_summary)} of {field_count} fields by coverage"
        )

    user_header = {
        "instructions": {
            "output_format": "Markdown Concept blocks only (no SKILL dump, no code fences around the whole report).",
            "implementation_examples": (
                "Each Implementation Example must be a template with {variable} placeholders. "
                "CRITICAL: Placeholders must be EXACT field ids from the field list below. "
                "Do NOT combine multiple field names into one placeholder (e.g. do NOT create "
                "'mean_similarity_max_similarity_...' from 'mean_similarity' + 'max_similarity'). "
                "If you need multiple fields, use separate placeholders: {field1}, {field2}. "
                "Bind placeholders to the distinctive suffix of the 2–3 fields named in **Fields**. "
                "Do not emit a generic {score}/{value}/{field} that matches the whole catalog."
            ),
            "no_code_fences": True,
            "do_not_invent_placeholders": True,
            "min_multi_field_concepts": 3,
        },
        "dataset_context": {
            "dataset_id": dataset_id,
            "dataset_name": dataset_name,
            "dataset_description": dataset_description,
            "category": data_category,
            "region": region,
            "delay": delay,
            "universe": universe,
            "field_count": field_count,
        },
        "field_format": format_note,
    }

    field_lines: list[str] = []
    for f in fields_summary:
        fid = str(f.get("id") or "").strip()
        desc = str(f.get("description") or "").strip()
        line = f"{fid} :: {desc}" if desc else fid
        meta: list[str] = []
        cov = f.get("coverage")
        if cov is not None:
            try:
                meta.append(f"cov={float(cov):.2f}")
            except (TypeError, ValueError):
                meta.append(f"cov={cov}")
        if not uniform_type and f.get("type") not in (None, ""):
            meta.append(f"type={f.get('type')}")
        if meta:
            line += "  [" + " ".join(meta) + "]"
        field_lines.append(line)

    user_prompt = json.dumps(user_header, ensure_ascii=False) + "\n\n" + "\n".join(field_lines)
    return system_prompt, user_prompt


def build_compact_operator_summary(allowed_operators, max_ops: int | None = None) -> str:
    """Build a compact operator reference — SOLUTION C (算子模块化拆分).

    Instead of full operator definitions with lengthy descriptions, produce a
    terse table: `name | category | 1-line-signature`. This keeps the prompt
    focused on the *actionable* operator interface without drowning the model
    in prose that causes attention dispersion.

    Full operator details remain available to implement_idea.py at runtime;
    the LLM only needs the summary to select operators.
    """
    if not allowed_operators:
        return "(no operators specified)"
    ops = allowed_operators[:max_ops] if max_ops else allowed_operators
    lines = ["Operator | Category | Usage", "---------|----------|------"]
    for op in ops:
        name = str(op.get("name", ""))
        cat = str(op.get("category", ""))
        # Compact signature: try description first, then definition
        desc = str(op.get("description") or op.get("definition") or "")
        # Truncate long descriptions to 80 chars
        desc = desc[:80] + ("…" if len(desc) > 80 else "")
        lines.append(f"{name} | {cat} | {desc}")
    return "\n".join(lines)


def batch_fields_by_dataset(fields_df, max_batch: int = 100) -> list[tuple[str, list[dict]]]:
    """Split fields into dataset-grouped batches — SOLUTION B (字段分层定义).

    Fields from the same dataset share a prefix token (e.g. 'starmine_', 'fnd72_').
    Grouping by dataset prefix ensures each batch has coherent semantics and
    avoids attention dilution across unrelated datasets.

    Returns list of (group_key, fields_subset) where group_key is the detected
    dataset code or 'mixed' for ungroupable fields.
    """
    id_col = pick_first_present_column(fields_df, ["id", "field_id", "fieldId"])
    desc_col = pick_first_present_column(fields_df, ["description", "desc"])
    if not id_col:
        return [("mixed", [])]

    # Detect prefix for each field
    groups: dict[str, list[dict]] = {}
    for _, row in fields_df.iterrows():
        fid = str(row.get(id_col) or "")
        prefix = fid.split("_", 1)[0] if "_" in fid else "mixed"
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append({
            "id": row.get(id_col),
            "description": row.get(desc_col),
        })

    # Convert to list, cap batch size
    result = []
    for prefix in sorted(groups.keys()):
        items = groups[prefix]
        if len(items) > max_batch:
            # Further split large batches
            for i in range(0, len(items), max_batch):
                result.append((f"{prefix}_part{ i // max_batch}", items[i:i+max_batch]))
        else:
            result.append((prefix, items))
    return result


def build_phased_prompts(
    dataset_id: str,
    dataset_name: str | None,
    dataset_description: str | None,
    data_category: str,
    region: str,
    delay: int,
    universe: str,
    data_type: str,
    fields_by_batch: list[tuple[str, list[dict]]],
    allowed_operators: list[dict],
    allowed_metric_suffixes: list[str],
    phase: str = "mapping",  # "structure" | "mapping" | "report"
    structure_result: str | None = None,
    batch_key: str | None = None,
    batch_fields: list[dict] | None = None,
    mapping_results: str | None = None,
    priors: dict | None = None,
):
    """Build phase-specific prompts — SOLUTION A (分片流水线).

    Phase 1 (structure): operator logic + dataset context → JSON operator map
    Phase 2 (mapping): batch fields + structure JSON → field→operator combos
    Phase 3 (report): all mapping results → ideas markdown

    Each phase has a focused, small prompt that avoids the 50-min reasoning trap.
    """
    compact_ops = build_compact_operator_summary(allowed_operators)

    if phase == "structure":
        # Phase 1: Build operator→category reference (small prompt, no fields)
        system_prompt = (
            "You are a WorldQuant BRAIN alpha expression architect.\n"
            "Task: Given the available operators below, produce a JSON object mapping\n"
            "each operator name to its category and a 10-word usage hint.\n"
            "Output ONLY valid JSON, no markdown fences.\n"
            "Format: {\"operator_name\": {\"category\": \"...\", \"hint\": \"...\"}, ...}"
        )
        user_content = {
            "dataset_id": dataset_id,
            "region": region,
            "delay": delay,
            "universe": universe,
            "operators_summary": compact_ops,
        }
        return system_prompt, json.dumps(user_content, ensure_ascii=False, indent=2)

    elif phase == "mapping":
        # Phase 2: Map fields to operators (medium prompt, one batch of fields)
        batch_fields_json = json.dumps(batch_fields or [], ensure_ascii=False)
        structure_json = structure_result or "{}"
        system_prompt = (
            "You generate WorldQuant BRAIN CONCEPTS, not per-field operator wraps.\n"
            "Read the field batch as a story. Propose 3-6 mechanisms that need 2-3 fields each.\n"
            "Rules:\n"
            "1. Each item is a mechanism (disagreement / residual / change-vs-level / intensity).\n"
            "2. Use ONLY operators from the operator map.\n"
            "3. Placeholders are distinctive suffixes of the named fields, not generic {score}.\n"
            "4. Output JSON array: [{\"mechanism\": \"...\", \"field_ids\": [\"...\"], "
            "\"templates\": [\"ops({var})\", ...], \"why\": \"...\"}, ...]\n"
            "5. No standalone rank({x}) / ts_zscore({x}, N). No markdown fences.\n"
            "6. quantile(x) takes ONE argument (default driver is gaussian; do not pass driver=).\n"
            "7. NEVER blend legs with fixed weights (add(multiply(0.4,A),multiply(0.6,B)) / 0.4*rank(A)+0.6*rank(B)):"
            " blocked as mixed-signal tuning. Combine structurally (ts_corr / divide / subtract / if_else / trade_when / group_*)."
        )
        user_content = {
            "operator_map": structure_json,
            "fields_batch": batch_fields_json,
            "batch_key": batch_key,
            "allowed_suffixes": allowed_metric_suffixes[:50],
            "region": region,
            "delay": delay,
            "priors": compact_priors_text(priors or {}, data_category),
        }
        return system_prompt, json.dumps(user_content, ensure_ascii=False, indent=2)

    elif phase == "report":
        # Phase 3: Generate ideas markdown from mapping results (medium prompt, aggregated results)
        # 2026-09-13 legacy：run_phased_pipeline 的 Phase 3 已改走确定性直译
        # （pipeline_reports.render_phased_ideas_md），本分支保留供对照/回退用。
        mapping_json = mapping_results or "[]"
        system_prompt = (
            "You are writing an ideas report for WorldQuant BRAIN Regular Alphas.\n"
            "Keep only mechanisms with a priced story. Drop lone rank/ts_zscore wraps.\n"
            "For each mapping item, produce:\n"
            "  **Concept**: <mechanism name>\n"
            "  - **Mechanism**: <who vs who / what surprise>\n"
            "  - **Fields**: `id1`, `id2`\n"
            "  - **Implementation Example**: `<operator_template({variable})>`\n"
            "  - **Direction**: ...\n"
            "  - **Why not crowded**: ...\n"
            "Output valid markdown. Include metadata:\n"
            "  **Dataset**: {dataset_id}\n"
            "  **Region**: {region}\n"
            "  **Delay**: {delay}"
        )
        user_content = {
            "dataset_id": dataset_id,
            "region": region,
            "delay": delay,
            "universe": universe,
            "data_category": data_category,
            "mapping_results": mapping_json,
            "allowed_suffixes": allowed_metric_suffixes[:30],
        }
        return system_prompt, json.dumps(user_content, ensure_ascii=False, indent=2)

    raise ValueError(f"Unknown phase: {phase}")
