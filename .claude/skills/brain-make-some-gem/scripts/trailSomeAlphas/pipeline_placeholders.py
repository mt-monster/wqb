# -*- coding: utf-8 -*-
"""GEM 占位符卫生层：字段名三级匹配 / 压缩 / 归一化。

2026-09-12 从 run_pipeline.py 拆出。纯函数、无 IO（仅 stderr 诊断）。

链路：build_allowed_*_suffixes（pipeline_data 产出候选后缀）
      → compress_to_known_suffix（压缩幻觉名到已知后缀）
      → validate_placeholders_strict（三级匹配拦截拼接幻觉复合名）
      → normalize_template_placeholders（归一化 + 严格校验闸）
      → implement_idea.py 绑定真实字段。

设计意图：LLM 会把多个字段名拼接成一个幻觉复合名（如
'mean_similarity_max_similarity_...'），本层在落盘/绑定前拦截，
是"字段名拼接幻觉"四层防御中的第 2/3 层（prompt 预防 → 本层拦截 → 绑定兜底）。
"""
import re
import sys


def compress_to_known_suffix(var: str, allowed_suffixes: list[str]) -> str | None:
    v = var.lower()
    for sfx in sorted(allowed_suffixes, key=len, reverse=True):
        if v.endswith(sfx.lower()):
            return sfx
    return None


def placeholder_is_reasonably_matchable(var: str, dataset_ids: list[str]) -> bool:
    """Heuristic check that a placeholder is likely to match real ids.

    We avoid treating very short tokens as valid unless they match a token boundary.
    """

    v = var
    if len(v) <= 3:
        pat = re.compile(rf"(^|_){re.escape(v)}(_|$)", flags=re.IGNORECASE)
        return any(pat.search(str(fid)) for fid in dataset_ids)
    return any(v in str(fid) for fid in dataset_ids)


def validate_placeholders_strict(template: str, dataset_ids: list[str]) -> tuple[str, bool, list[str]]:
    """Strict validation: reject placeholders that are clearly hallucinated composite names.

    A placeholder is invalid if:
    - It does not match any field id (exact, suffix, or substring)
    - It looks like a composite of multiple field names (e.g. 'mean_similarity_max_similarity_...')

    A placeholder is valid if:
    - Exact match with a field id
    - Suffix match with one or more field ids (implement_idea.py will expand combinations)
    - Substring match with a field id (fuzzy match)

    Returns (template, is_valid, invalid_placeholders).
    """
    vars_in_template = re.findall(r"\{([A-Za-z0-9_]+)\}", template)
    if not vars_in_template:
        return template, False, []

    invalid: list[str] = []
    ds_set = set(dataset_ids)

    for var in vars_in_template:
        # Exact match is always valid
        if var in ds_set:
            continue
        # Suffix match is valid (implement_idea.py will expand to all matching fields)
        if any(fid.endswith(var) for fid in dataset_ids):
            continue
        # Substring match is valid (fuzzy)
        if any(var in fid for fid in dataset_ids):
            continue
        # No match at all - this is a hallucinated field name
        invalid.append(var)

    return template, len(invalid) == 0, invalid


def normalize_template_placeholders(
    template: str,
    dataset_ids: list[str],
    allowed_suffixes: list[str],
    dataset_code: str | None,
) -> tuple[str, bool]:
    """Normalize placeholders to suffix-only form, without dataset-specific aliasing.

    - Strips dataset code prefix (e.g. fnd72_*) when present.
    - Compresses placeholders to the longest known suffix.
    - Returns (normalized_template, is_valid).
    """

    vars_in_template = re.findall(r"\{([A-Za-z0-9_]+)\}", template)
    if not vars_in_template:
        return template, False

    mapping: dict[str, str] = {}
    for var in set(vars_in_template):
        new_var = var
        if dataset_code and new_var.lower().startswith(dataset_code.lower() + "_"):
            new_var = new_var[len(dataset_code) + 1 :]

        compressed = compress_to_known_suffix(new_var, allowed_suffixes)
        if compressed:
            new_var = compressed

        mapping[var] = new_var

    normalized = template
    for src, dst in mapping.items():
        normalized = normalized.replace("{" + src + "}", "{" + dst + "}")

    # Validate: every placeholder should look matchable in real ids.
    vars_after = re.findall(r"\{([A-Za-z0-9_]+)\}", normalized)
    ok = all(placeholder_is_reasonably_matchable(v, dataset_ids) for v in vars_after)

    # Strict validation: reject composite/hallucinated field names
    if ok:
        _, strict_ok, invalid = validate_placeholders_strict(normalized, dataset_ids)
        if not strict_ok:
            print(f"[validate] strict check failed, invalid placeholders: {invalid}", file=sys.stderr)
            ok = False

    return normalized, ok
