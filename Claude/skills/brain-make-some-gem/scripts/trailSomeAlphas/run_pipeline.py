import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import csv
import time
from pathlib import Path

import requests


# ---------------- expected_exposure 兜底（2026-09-01） ----------------
# LLM 生成 idea 时有时漏写 **Expected Exposure** 行（实测 520 条仅 14% 覆盖），
# gate.py 的收益来源多样性闸读不到标签就降级 WARN、形同虚设。
# 此函数对缺失项按 Concept/Mechanism 关键词推断标签并显式追加该行。

_EXPOSURE_KEYWORDS = [
    ("momentum", ["momentum", "trend", "drift", "continuation", "post-earnings", "pead"]),
    ("reversal", ["reversal", "overreaction", "mean-revert", "mean revert", "short-term reversal"]),
    ("value", ["value", "underval", "book-to-market", "earnings yield", "cheap"]),
    ("quality", ["quality", "profitab", "roa", "roe", "accrual", "earnings quality"]),
    ("growth", ["growth", "expansion", "revision up", "upgrade"]),
    ("lowvol", ["low vol", "lowvol", "defensive", "stability", "stable"]),
    ("liquidity", ["liquidity", "amihud", "turnover cost", "tradability"]),
    ("sentiment", ["sentiment", "news tone", "crowd", "attention", "buzz", "panic", "fear"]),
    ("flow", ["ownership", "institutional", "holdings", "insider", "buyback", "flow"]),
    ("risk", ["risk", "volatility", "tail", "drawdown", "distress", "default"]),
]


def _ensure_expected_exposure(idea_text: str) -> str:
    """idea 文本缺 **Expected Exposure** 行时按关键词推断并追加。已有则原样返回。"""
    if not idea_text:
        return idea_text
    if re.search(r"\*\*Expected Exposure\*\*\s*:", idea_text, re.IGNORECASE):
        return idea_text
    tl = idea_text.lower()
    for label, kws in _EXPOSURE_KEYWORDS:
        if any(k in tl for k in kws):
            return idea_text.rstrip() + f"\n- **Expected Exposure** (inferred): {label}\n"
    return idea_text.rstrip() + "\n- **Expected Exposure** (inferred): other\n"

# Ensure UTF-8 stdout on Windows to avoid UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"
FEATURE_ENGINEERING_DIR = SKILLS_DIR / "brain-data-feature-engineering"
FEATURE_IMPLEMENTATION_DIR = SKILLS_DIR / "brain-feature-implementation"
FEATURE_IMPLEMENTATION_SCRIPTS = FEATURE_IMPLEMENTATION_DIR / "scripts"

sys.path.insert(0, str(FEATURE_IMPLEMENTATION_SCRIPTS))
try:
    import ace_lib  # type: ignore
except Exception as exc:
    raise SystemExit(f"Failed to import ace_lib from {FEATURE_IMPLEMENTATION_SCRIPTS}: {exc}")
try:
    from validator import ExpressionValidator  # type: ignore
except Exception as exc:
    raise SystemExit(f"Failed to import ExpressionValidator from {FEATURE_IMPLEMENTATION_SCRIPTS}: {exc}")

from economic_priors import compact_priors_text, concept_first_rules, load_priors

import skeletons  # 同目录骨架库（P0: skeleton mode 填槽协议）
from skill_roots import candidate_paths_under_skill  # 技能根单源（同目录）

# 复用工作区 tools/lib 下的 vector_wrap（单一权威源）。
# 生成端兜底：LLM 未必遵守 prompt 里的 vec_* 指示，落盘前自动裹上聚合。
def _find_tools_lib() -> Path | None:
    env = os.environ.get("WQB_TOOLS_LIB")
    if env and (Path(env) / "vector_wrap.py").is_file():
        return Path(env)
    # 从常见工作区根向上/已知位置探测 vector_wrap.py
    candidates = [
        Path(os.environ.get("WQB_ROOT", "")) / "tools" / "lib" if os.environ.get("WQB_ROOT") else None,
        Path("D:/coding/traeCN_project/wqb/tools/lib"),
    ]
    for c in candidates:
        if c and (c / "vector_wrap.py").is_file():
            return c
    return None


_REPO_TOOLS_LIB = _find_tools_lib()
if _REPO_TOOLS_LIB and str(_REPO_TOOLS_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_TOOLS_LIB))
try:
    from vector_wrap import wrap_naked_vectors  # type: ignore
except Exception:
    wrap_naked_vectors = None

def load_brain_credentials(config_path: Path) -> tuple[str, str]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    creds = data.get("BRAIN_CREDENTIALS", {})
    email = creds.get("email")
    password = creds.get("password")
    if not email or not password:
        raise ValueError("BRAIN_CREDENTIALS missing in config.json")
    return email, password

def load_brain_credentials_from_env_or_args(username: str | None, password: str | None, config_path: Path) -> tuple[str, str]:
    env_user = os.environ.get("BRAIN_USERNAME") or os.environ.get("BRAIN_EMAIL")
    env_pass = os.environ.get("BRAIN_PASSWORD")
    final_user = username or env_user
    final_pass = password or env_pass
    if final_user and final_pass:
        return final_user, final_pass
    return load_brain_credentials(config_path)

def start_brain_session(email: str, password: str):
    ace_lib.get_credentials = lambda: (email, password)
    return ace_lib.start_session()

def pick_first_present_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    # also try case-insensitive
    lower_map = {col.lower(): col for col in df.columns}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    return None


DEFAULT_OPERATORS = [
    {"name": "rank", "category": "section", "description": "rank(field) — cross-sectional percentile rank"},
    {"name": "ts_rank", "category": "section", "description": "ts_rank(field, window) — time-series percentile rank"},
    {"name": "zscore", "category": "section", "description": "zscore(field) — cross-sectional z-score"},
    {"name": "ts_zscore", "category": "section", "description": "ts_zscore(field, window) — time-series z-score"},
    {"name": "delta", "category": "momentum", "description": "delta(field) — first difference"},
    {"name": "ts_delta", "category": "momentum", "description": "ts_delta(field, window) — field[t] - field[t-window]"},
    {"name": "ts_sum", "category": "aggregation", "description": "ts_sum(field, window) — cumulative sum over N bars"},
    {"name": "ts_mean", "category": "aggregation", "description": "ts_mean(field, window) — moving average"},
    {"name": "ts_stddev", "category": "aggregation", "description": "ts_stddev(field, window) — moving std dev"},
    {"name": "ts_max", "category": "aggregation", "description": "ts_max(field, window) — max over N bars"},
    {"name": "ts_min", "category": "aggregation", "description": "ts_min(field, window) — min over N bars"},
    {"name": "decay_linear", "category": "momentum", "description": "decay_linear(field, window) — linearly decaying sum"},
    {"name": "signed_power", "category": "section", "description": "signed_power(field, power) — monotonic rank-preserving"},
    {"name": "abs", "category": "section", "description": "abs(field) — absolute value"},
    {"name": "sign", "category": "section", "description": "sign(field) — +1/-1/0"},
    {"name": "log", "category": "section", "description": "log(field) — natural log"},
    {"name": "sqrt", "category": "section", "description": "sqrt(field) — square root"},
    {"name": "pow", "category": "section", "description": "pow(field, p) — field^p"},
    {"name": "min", "category": "section", "description": "min(field1, field2) — element-wise min"},
    {"name": "max", "category": "section", "description": "max(field1, field2) — element-wise max"},
    {"name": "mean", "category": "section", "description": "mean(field1, field2) — element-wise mean"},
    {"name": "scale", "category": "section", "description": "scale(field) — rescale so sum of abs values = 1"},
    {"name": "trimscale", "category": "section", "description": "trimscale(field) — trimmed scale"},
    {"name": "add", "category": "section", "description": "add(field1, field2) — element-wise sum"},
    {"name": "subtract", "category": "section", "description": "subtract(field1, field2) — element-wise difference"},
    {"name": "group_zscore", "category": "neutralization", "description": "group_zscore(field, group_field)"},
    {"name": "group_neutralize", "category": "neutralization", "description": "group_neutralize(field, group_field)"},
    {"name": "ts_backfill", "category": "aggregation", "description": "ts_backfill(field, window) — fill gaps backward"},
    {"name": "ts_regression", "category": "momentum", "description": "ts_regression(field, target, window) — beta"},
    {"name": "product", "category": "section", "description": "product(field1, field2) — element-wise product"},
    {"name": "covariance", "category": "momentum", "description": "covariance(field1, field2, window)"},
    {"name": "correlation", "category": "momentum", "description": "correlation(field1, field2, window)"},
    {"name": "delay", "category": "momentum", "description": "delay(field, bars) — lag by N bars"},
    {"name": "ts_minmax", "category": "aggregation", "description": "ts_minmax(field, window) — normalize to [0,1]"},
    {"name": "ts_count", "category": "aggregation", "description": "ts_count(field, window) — count non-null"},
    {"name": "group_sum", "category": "aggregation", "description": "group_sum(field, group_field)"},
    {"name": "group_rank", "category": "aggregation", "description": "group_rank(field, group_field)"},
]


def select_dataset(datasets_df, data_category: str, dataset_id: str | None):
    if dataset_id:
        return dataset_id, None, None, datasets_df

    category_col = pick_first_present_column(
        datasets_df,
        ["category", "data_category", "dataCategory", "category_name", "dataCategory_name"],
    )

    filtered = datasets_df
    if category_col:
        filtered = datasets_df[datasets_df[category_col].astype(str).str.lower() == data_category.lower()]

    if filtered.empty:
        filtered = datasets_df

    id_col = pick_first_present_column(filtered, ["id", "dataset_id", "datasetId"])
    name_col = pick_first_present_column(filtered, ["name", "dataset_name", "datasetName"])
    desc_col = pick_first_present_column(filtered, ["description", "desc", "dataset_description"])

    if not id_col:
        raise ValueError("Unable to locate dataset id column from dataset list")

    row = filtered.iloc[0]
    return row[id_col], row.get(name_col) if name_col else None, row.get(desc_col) if desc_col else None, datasets_df


def build_field_summary(fields_df, max_fields: int | None = None):
    id_col = pick_first_present_column(fields_df, ["id", "field_id", "fieldId"])
    desc_col = pick_first_present_column(fields_df, ["description", "desc"])

    total = int(fields_df.shape[0])
    cov_col = pick_first_present_column(fields_df, ["coverage", "Coverage"])
    type_col = pick_first_present_column(fields_df, ["type", "dataType", "data_type"])
    if max_fields is None:
        # Default: pass ALL fields to the prompt.
        subset = fields_df
    else:
        n = min(int(max_fields), total)
        if n < total and cov_col:
            # Truncation path: keep highest-coverage fields instead of arbitrary head().
            def _cov_key(v):
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return -1.0
            subset = fields_df.assign(
                _cov_rank=fields_df[cov_col].map(_cov_key)
            ).sort_values("_cov_rank", ascending=False, kind="stable").head(n).drop(columns=["_cov_rank"])
        else:
            subset = fields_df.head(n)

    rows = []
    for _, row in subset.iterrows():
        desc = row.get(desc_col)
        # Collapse embedded newlines/whitespace so one field renders as one prompt line.
        desc = re.sub(r"\s+", " ", str(desc)).strip() if desc is not None else ""
        item = {
            "id": row.get(id_col),
            "description": desc,
        }
        if cov_col:
            item["coverage"] = row.get(cov_col)
        if type_col:
            item["type"] = row.get(type_col)
        rows.append(item)
    return rows, fields_df.shape[0]


def read_text_optional(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def build_allowed_metric_suffixes(fields_df, max_suffixes: int = 300) -> list[str]:
    """Derive a practical list of placeholder candidates from dataset field ids.

    `implement_idea.py` matches `{variable}` by searching for that substring in the
    field id and then using the *base* (everything before first occurrence) to
    align the other variables. In practice, good placeholders tend to be the
    trailing 2-5 underscore-joined tokens.
    """

    id_col = pick_first_present_column(fields_df, ["id", "field_id", "fieldId"])
    if not id_col:
        return []

    field_ids = fields_df[id_col].dropna().astype(str).tolist()
    dataset_code = detect_dataset_code(field_ids)

    counts: dict[str, int] = {}
    for raw in field_ids:
        parts = [p for p in str(raw).split("_") if p]
        if len(parts) < 2:
            continue

        # Collect suffix candidates from the tail.
        # Prefer multi-token names, but allow single-token suffixes when they're
        # specific enough (e.g., "inventories").
        # IMPORTANT: never allow the "suffix" to equal the full id (that would
        # encourage the LLM to emit {full_field_id}, violating the suffix-only rule).
        for n in range(1, min(6, len(parts))):
                suffix = "_".join(parts[-n:])
                # Filter out overly-generic / numeric suffixes
                if suffix.replace("_", "").isdigit():
                    continue
                if dataset_code and suffix.lower().startswith(dataset_code.lower() + "_"):
                    continue
                if n == 1 and len(suffix) < 8:
                    continue
                if len(suffix) < 6:
                    continue
                counts[suffix] = counts.get(suffix, 0) + 1

    # Prefer suffixes that show up multiple times and have underscores
    ranked = sorted(
        counts.items(),
        key=lambda kv: (kv[1], kv[0].count("_"), len(kv[0])),
        reverse=True,
    )

    suffixes: list[str] = []
    for suffix, _ in ranked:
        if suffix not in suffixes:
            suffixes.append(suffix)
        if len(suffixes) >= max_suffixes:
            break
    return suffixes


def build_allowed_suffixes_from_ids(dataset_ids: list[str], max_suffixes: int = 300) -> list[str]:
    """Build suffix candidates from downloaded dataset ids.

    This is used to normalize/validate templates for `implement_idea.py`.
    """

    counts: dict[str, int] = {}
    for raw in dataset_ids:
        parts = [p for p in str(raw).split("_") if p]
        if len(parts) < 2:
            continue
        for n in range(1, 6):
            if len(parts) >= n:
                suffix = "_".join(parts[-n:])
                if suffix.replace("_", "").isdigit():
                    continue
                if n == 1 and len(suffix) < 8:
                    continue
                if len(suffix) < 6:
                    continue
                counts[suffix] = counts.get(suffix, 0) + 1

    ranked = sorted(
        counts.items(),
        key=lambda kv: (kv[1], kv[0].count("_"), len(kv[0])),
        reverse=True,
    )

    suffixes: list[str] = []
    for suffix, _ in ranked:
        if suffix not in suffixes:
            suffixes.append(suffix)
        if len(suffixes) >= max_suffixes:
            break
    return suffixes


def detect_dataset_code(dataset_ids: list[str]) -> str | None:
    if not dataset_ids:
        return None
    counts: dict[str, int] = {}
    for fid in dataset_ids:
        tok = (str(fid).split("_", 1)[0] or "").strip()
        if tok:
            counts[tok] = counts.get(tok, 0) + 1
    if not counts:
        return None
    return max(counts.items(), key=lambda kv: kv[1])[0]

def ensure_metadata_block(markdown_text: str, dataset_id: str, region: str, delay: int) -> str:
    """Ensure the ideas markdown contains the metadata block used by the pipeline."""

    has_dataset = re.search(r"^\*\*Dataset\*\*:\s*\S+", markdown_text, flags=re.MULTILINE) is not None
    has_region = re.search(r"^\*\*Region\*\*:\s*\S+", markdown_text, flags=re.MULTILINE) is not None
    has_delay = re.search(r"^\*\*Delay\*\*:\s*\d+", markdown_text, flags=re.MULTILINE) is not None
    if has_dataset and has_region and has_delay:
        return markdown_text

    block = [
        "",
        f"**Dataset**: {dataset_id}",
        f"**Region**: {region}",
        f"**Delay**: {delay}",
        "",
    ]

    lines = markdown_text.splitlines()
    insert_at = 0
    for i, line in enumerate(lines[:10]):
        if line.strip():
            insert_at = i + 1
            break
    new_lines = lines[:insert_at] + block + lines[insert_at:]
    return "\n".join(new_lines).lstrip("\n")

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


def render_skeleton_ideas_md(dataset_id: str, region: str, delay: int,
                             layers: dict, metas: list, dropped: dict) -> str:
    """把填槽结果渲染为 ideas.md（Concept 块自 slots 渲染，保持元数据头/ledger 契约）。"""
    lines = [
        f"**Dataset**: {dataset_id}",
        f"**Region**: {region}",
        f"**Delay**: {delay}",
        "",
        "# Skeleton-mode ideas (operator-topology constrained)",
        "",
        f"Field layering: signal={len(layers['signal'])}, scale={len(layers['scale'])}, "
        f"metadata={len(layers['metadata'])} (excluded), date={len(layers['date'])} (excluded).",
        "",
        "## Signal fields used",
        "",
    ]
    used = sorted({m["field"] for m in metas} | {m["field2"] for m in metas if m.get("field2")})
    for fid in used:
        lines.append(f"- `{fid}`")
    lines += ["", "## Concepts", ""]
    by_family: dict[str, list] = {}
    for m in metas:
        by_family.setdefault(m["family"], []).append(m)
    for fam, items in sorted(by_family.items()):
        lines.append(f"### family: {fam}")
        lines.append("")
        for i, m in enumerate(items, 1):
            lines.append(f"**Concept {fam}.{i}**")
            lines.append("")
            lines.append(f"- skeleton: `{m['skeleton_id']}` window={m['window']} sign={m['sign']}")
            lines.append(f"- rationale: {m['rationale'] or '(none)'}")
            lines.append("")
            lines.append("**Implementation Example**")
            lines.append("")
            lines.append(f"`{m['expr']}`")
            lines.append("")
    lines += [
        "## Slot-drop statistics",
        "",
        f"```json\n{json.dumps(dropped, ensure_ascii=False, indent=2)}\n```",
        "",
    ]
    return "\n".join(lines)


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

    system_prompt, user_prompt = skeletons.build_skeleton_prompt(
        dataset_id=dataset_id, region=region, delay=delay,
        field_layers=layers, descriptions=descriptions,
        n_slots=n_slots, region_priors=priors,
        window_pool=window_pool,
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
            "5. No standalone rank({x}) / ts_zscore({x}, N). No markdown fences."
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
    print("[phased] Phase 2/3: Field mapping...", flush=True)
    batches = batch_fields_by_dataset(fields_df, max_batch=50)
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
        except (json.JSONDecodeError, Exception) as exc:
            print(f"[phased]   Warning: batch {batch_key} mapping failed: {exc}", file=sys.stderr)

    mapping_json = json.dumps(all_mapping_results, ensure_ascii=False, indent=2)
    print(f"[phased]   Total mapping entries: {len(all_mapping_results)}", flush=True)

    # ---- Phase 3: Report Generation ----
    print("[phased] Phase 3/3: Report generation...", flush=True)
    sys_prompt, user_prompt = build_phased_prompts(
        dataset_id, dataset_name, dataset_description, data_category,
        region, delay, universe, data_type, [],
        allowed_operators, allowed_metric_suffixes,
        phase="report",
        mapping_results=mapping_json,
        priors=priors,
    )
    report = call_moonshot(api_key, model_report, sys_prompt, user_prompt, timeout_s=timeout_s)
    print("[phased] Done.", flush=True)
    return report
    if datafields_df is None or getattr(datafields_df, "empty", True):
        return 0.0
    dtype_col = pick_first_present_column(datafields_df, ["type", "dataType", "data_type"])
    if not dtype_col:
        return 0.0
    counts = datafields_df[dtype_col].astype(str).value_counts().to_dict()
    vector_count = counts.get("VECTOR", 0)
    total = sum(counts.values())
    return (vector_count / total) if total else 0.0


def _vector_ratio_from_datafields_df(datafields_df) -> float:
    if datafields_df is None or getattr(datafields_df, "empty", True):
        return 0.0
    dtype_col = pick_first_present_column(datafields_df, ["type", "dataType", "data_type"])
    if not dtype_col:
        return 0.0
    counts = datafields_df[dtype_col].astype(str).value_counts().to_dict()
    vector_count = counts.get("VECTOR", 0)
    total = sum(counts.values())
    return (vector_count / total) if total else 0.0


def filter_operators_df(operators_df, keep_vector: bool):
    """Apply user-confirmed operator filters.

    Rules:
    - Keep only scope == REGULAR
    - Keep category == Group (2026-09-06: 原先整类剥离，与 prompt 要求冲突)
    - Keep category == Vector only if keep_vector is True
    - Drop only the ghost operator `neutralize` (2026-09-06: 原正则误伤 scale/normalize/group_*)
    """

    df = operators_df.copy()

    name_col = pick_first_present_column(df, ["name", "operator", "op", "id"])
    scope_col = pick_first_present_column(df, ["scope", "scopes"])
    category_col = pick_first_present_column(df, ["category", "group", "type"])
    desc_col = pick_first_present_column(df, ["description", "desc", "help", "doc", "documentation"])
    definition_col = pick_first_present_column(df, ["definition", "syntax"])

    if scope_col:
        df = df[df[scope_col].astype(str).str.upper() == "REGULAR"]

    if category_col:
        # 2026-09-06 修复：不再整类剥离 Group 算子。
        # 原因：prompt（L602/L618/L1350/L2497-99）硬性要求「至少 1 个 concept 使用
        # group_zscore / group_rank / group_neutralize / group_mean」，但此处把
        # category=="group" 整类删掉，导致 allowed_operators 与 prompt 自相矛盾——
        # 模型（EUR wave124 实测）耗费大量推理在这个冲突上并最终放弃 group 算子。
        # group_* 全部在平台 live 102 算子内（operator_audit 已验证）。
        if not keep_vector:
            df = df[df[category_col].astype(str).str.lower() != "vector"]

    if name_col:
        # 2026-09-03 修复：放开 rank/zscore（BRAIN 标准算子，多样性必需）
        # 原 banned 正则过严，把 rank/ts_zscore/group_rank 当中性化算子禁掉，
        # 导致 GEM 被迫全部用 quantile(..., driver="gaussian") 包裹，骨架单一。
        # 保留 neutral/normal/scal 过滤（防止中性化算子滥用）。
        # 2026-09-06 修复：原正则按子串杀 neutral|normal|scal，误伤三类已验证算子：
        #   scale / ts_scale / group_scale（跨区铁律 SCALE-NEG-RANK-ROBUST-SYNTAX
        #     明确推荐 scale(-rank(x)) 过 robust 闸，实测 1.01 vs reverse 写法 0.90）
        #   normalize / group_normalize、group_neutralize
        # 真正必须禁的只有裸 neutralize —— 它是平台幽灵算子（operator_audit ghost）。
        banned = re.compile(r"^neutralize$", flags=re.IGNORECASE)
        df = df[~df[name_col].astype(str).str.contains(banned, na=False)]

        # de-dup by operator name
        df = df.drop_duplicates(subset=[name_col]).reset_index(drop=True)

    cols = [c for c in [name_col, category_col, scope_col, desc_col, definition_col] if c]
    allowed = []
    for _, row in df.iterrows():
        item = {
            "name": row.get(name_col) if name_col else None,
            "category": row.get(category_col) if category_col else None,
            "scope": row.get(scope_col) if scope_col else None,
            "description": row.get(desc_col) if desc_col else None,
            "definition": row.get(definition_col) if definition_col else None,
        }
        # drop None keys to keep prompt compact
        allowed.append({k: v for k, v in item.items() if v is not None})

    return df, allowed, cols

def call_moonshot(api_key: str, model: str, system_prompt: str, user_prompt: str, timeout_s: int = 900):
    base_url = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],

        # Default to streaming so the user can observe model progress.
        "stream": True,
    }

    retries = int(os.environ.get("MOONSHOT_RETRIES", "2"))
    backoff_s = float(os.environ.get("MOONSHOT_RETRY_BACKOFF", "2"))

    def _stream_sse_and_collect(resp: requests.Response) -> str:
        """Read OpenAI-compatible SSE stream and print deltas live.

        Still returns the full accumulated assistant content so existing callers
        (which expect a string) keep working.
        """

        content_parts: list[str] = []
        thinking_parts: list[str] = []
        thinking = False

        # Ensure requests doesn't try to decode as bytes.
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            line = raw_line.strip()
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break

            try:
                event = json.loads(data_str)
            except Exception:
                continue

            choices = event.get("choices") or []
            if not choices:
                continue
            choice0 = choices[0] if isinstance(choices[0], dict) else None
            if not choice0:
                continue

            delta = choice0.get("delta") or {}
            if not isinstance(delta, dict):
                delta = {}

            # Moonshot/Kimi exposes reasoning tokens as `reasoning_content`.
            reasoning = delta.get("reasoning_content")
            if reasoning:
                if not thinking:
                    thinking = True
                    print("=============开始思考=============", flush=True)
                thinking_parts.append(str(reasoning))
                print(str(reasoning), end="", flush=True)

            piece = delta.get("content")
            if piece:
                if thinking:
                    thinking = False
                    print("\n=============思考结束=============", flush=True)
                content_parts.append(str(piece))
                print(str(piece), end="", flush=True)

            finish_reason = choice0.get("finish_reason")
            if finish_reason:
                break

        # If the stream ended while still "thinking", close the marker cleanly.
        if thinking:
            print("\n=============思考结束=============", flush=True)

        return "".join(content_parts)

    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout_s, stream=True)
            resp.encoding = "utf-8"
            if resp.status_code >= 300:
                raise RuntimeError(f"Moonshot API error {resp.status_code}: {resp.text}")

            # Prefer SSE streaming when available.
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "text/event-stream" in ctype or payload.get("stream"):
                return _stream_sse_and_collect(resp)

            data = resp.json()
            break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            last_exc = exc
            if attempt >= retries:
                raise
            time.sleep(backoff_s * (2**attempt))
        except requests.exceptions.RequestException as exc:
            # Other request-layer issues: retry a bit, but don't loop forever.
            last_exc = exc
            if attempt >= retries:
                raise
            time.sleep(backoff_s * (2**attempt))
    else:
        raise last_exc or RuntimeError("Moonshot request failed")

    try:
        return data["choices"][0]["message"]["content"]
    except Exception as exc:
        raise RuntimeError(f"Unexpected Moonshot response: {data}") from exc
def _ensure_mandatory_sections(content: str, dataset_id: str, region: str, delay: int) -> str:
    """Ensure the ideas markdown contains all mandatory sections for downstream parsing.

    Required sections (checked by regex, auto-appended if missing):
      - ## 字段（Fields）
      - ## 特征（Features）
      - ## 建议（Implementation Examples）
      - ## 字段白名单（Field Whitelist）
      - ## Concepts
    """
    if not content:
        return content

    # Check for mandatory sections (allow both Chinese and English headers)
    has_fields = re.search(r"^##\s+字段|^##\s+Fields", content, flags=re.MULTILINE | re.IGNORECASE)
    has_features = re.search(r"^##\s+特征|^##\s+Features", content, flags=re.MULTILINE | re.IGNORECASE)
    has_examples = re.search(r"^##\s+建议|^##\s+Implementation", content, flags=re.MULTILINE | re.IGNORECASE)
    has_whitelist = re.search(r"^##\s+字段白名单|^##\s+Field Whitelist", content, flags=re.MULTILINE | re.IGNORECASE)
    has_concepts = re.search(r"^##\s+Concepts|^##\s+概念", content, flags=re.MULTILINE | re.IGNORECASE)

    missing = []
    if not has_fields:
        missing.append("字段（Fields）")
    if not has_features:
        missing.append("特征（Features）")
    if not has_examples:
        missing.append("建议（Implementation Examples）")
    if not has_whitelist:
        missing.append("字段白名单（Field Whitelist）")
    if not has_concepts:
        missing.append("Concepts")

    if not missing:
        return content

    # Auto-append missing sections with sensible defaults
    lines = [content.rstrip(), ""]
    lines.append("---")
    lines.append("")
    lines.append("## Auto-appended mandatory sections (GEM 生成端兜底)")
    lines.append("")

    if not has_fields:
        lines.extend([
            "## 字段（Fields）",
            "",
            "| Field ID | Type | Coverage | Role |",
            "|---|---|---|---|",
            f"| (auto-generated from {dataset_id}) | MATRIX | N/A | 主信号 |",
            "",
        ])

    if not has_features:
        lines.extend([
            "## 特征（Features）",
            "",
            "- ts_backfill：对低覆盖率稀疏字段做时间序列回填",
            "- group_zscore / group_rank：截面中性化（cross-sectional）",
            "- rank / winsorize：防厚尾与极值",
            "",
        ])

    if not has_examples:
        # Extract existing Implementation Examples from Concepts
        examples = re.findall(r"\*\*Implementation Example\*\*[:\s]*`([^`]+)`", content)
        if not examples:
            examples = re.findall(r"Implementation Example[:\s]*`([^`]+)`", content, flags=re.IGNORECASE)
        lines.extend([
            "## 建议（Implementation Examples）",
            "",
        ])
        if examples:
            for i, ex in enumerate(examples[:10], 1):
                lines.append(f"- concept_{i}: `{ex}`")
        else:
            lines.append("- (no Implementation Examples found in Concepts)")
        lines.append("")

    if not has_whitelist:
        # Extract field ids from backticks in the whole document
        field_ids = re.findall(r"`([a-z][a-z0-9_]{3,})`", content)
        field_ids = sorted(set(f for f in field_ids if not f.startswith(("rank", "ts_", "vec_", "group_", "add", "sub", "mul", "div"))))
        lines.extend([
            "## 字段白名单（Field Whitelist）",
            "",
            "```",
        ])
        lines.extend(field_ids[:50])  # cap at 50
        lines.extend([
            "```",
            "",
        ])

    if not has_concepts:
        lines.extend([
            "## Concepts",
            "",
            "(Concept blocks were not found in the original output; see above sections for extracted fields and templates.)",
            "",
        ])

    print(f"[sections] auto-appended missing mandatory sections: {', '.join(missing)}", flush=True)
    return "\n".join(lines)


def save_ideas_report(content: str, region: str, delay: int, dataset_id: str) -> Path:
    # Ensure mandatory sections before saving
    content = _ensure_mandatory_sections(content, dataset_id, region, delay)
    output_dir = FEATURE_ENGINEERING_DIR / "output_report"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{region}_delay{delay}_{dataset_id}_ideas.md"
    output_path = output_dir / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path

def extract_templates(markdown_text: str) -> list[str]:
    """Extract implementation templates from idea markdown.

    For pipeline robustness, this function returns ONLY the template strings.
    The recommended, higher-fidelity parser is `extract_template_blocks()`,
    which returns both template + idea text per **Concept** block.
    """

    blocks = extract_template_blocks(markdown_text)
    templates = [b["template"] for b in blocks if b.get("template")]
    return sorted(set(t.strip() for t in templates if t and t.strip()))


def extract_table_template_blocks(markdown_text: str) -> list[dict[str, str]]:
    """Fallback parser for markdown tables that contain a `{placeholder}` template.

    Accepts both column orders:
      | ID | `template` | rationale |
      | # | Idea | `template` |
    """
    row_re = re.compile(r"^\|\s*(?:\d+\s*)?\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|?\s*$")
    out: list[dict[str, str]] = []
    seen: set[str] = set()

    def _add(template: str, rationale: str) -> None:
        template = template.strip()
        if "{" not in template or "}" not in template or template in seen:
            return
        seen.add(template)
        idea = f"**Concept**: {rationale}\n- **Implementation Example**: `{template}`"
        out.append({"template": template, "idea": idea})

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("|---"):
            continue
        matched = row_re.match(stripped)
        if matched:
            _add(matched.group(1).strip(), matched.group(2).strip().strip("|").strip())
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        template = None
        other: list[str] = []
        for cell in cells:
            bt = re.search(r"`([^`]+)`", cell)
            if bt and "{" in bt.group(1) and "}" in bt.group(1) and template is None:
                template = bt.group(1).strip()
            else:
                other.append(re.sub(r"`+", "", cell).strip())
        if template:
            rationale = " ".join(x for x in other if x and x != "---" and not x.isdigit())
            _add(template, rationale)
    return out


def extract_named_template_blocks(markdown_text: str) -> list[dict[str, str]]:
    """Fallback for LLM headings: - **Template**: `expr` plus nearby Rationale."""
    named_re = re.compile(r"\*\*Template\*\*\s*:\s*`([^`]+)`", flags=re.IGNORECASE)
    rationale_re = re.compile(r"\*\*Rationale\*\*\s*:\s*(.*)$", flags=re.IGNORECASE)
    heading_re = re.compile(r"^#{2,6}\s+(.*)$")
    out: list[dict[str, str]] = []
    current_heading = ""
    pending_template: str | None = None
    pending_rationale = ""
    pending_heading = ""

    def _flush() -> None:
        nonlocal pending_template, pending_rationale, pending_heading
        if pending_template and "{" in pending_template and "}" in pending_template:
            idea = f"**Concept**: {pending_heading or pending_rationale}\n{pending_rationale}".strip()
            out.append({"template": pending_template.strip(), "idea": idea})
        pending_template = None
        pending_rationale = ""
        pending_heading = ""

    for line in markdown_text.splitlines():
        stripped = line.strip()
        hm = heading_re.match(stripped)
        if hm:
            _flush()
            current_heading = hm.group(1).strip()
            continue
        tm = named_re.search(stripped)
        if tm:
            _flush()
            pending_template = tm.group(1).strip()
            pending_heading = current_heading
            continue
        rm = rationale_re.search(stripped)
        if rm and pending_template:
            pending_rationale = (rm.group(1) or "").strip()
    _flush()
    return out


def extract_template_blocks(markdown_text: str) -> list[dict[str, str]]:
    """Parse **Concept** blocks and extract {template, idea}.

    A "block" is a section that starts with a line like:
      **Concept**: ...
    and contains a line like:
      - **Implementation Example**: `...`

    Output:
      [{"template": <string>, "idea": <string>}, ...]

    Notes:
    - `template` is taken from inside backticks when present; otherwise uses the
      remainder of the line after ':'.
    - `idea` is the rest of the block text (including the concept line and
      bullets) excluding the implementation example line.
    """

    concept_re = re.compile(r"^\*\*Concept\*\*\s*:\s*(.*)\s*$")
    impl_re = re.compile(r"\*\*Implementation Example\*\*\s*:\s*(.*)$", flags=re.IGNORECASE)
    backtick_re = re.compile(r"`([^`]*)`")
    boundary_re = re.compile(r"^(?:-{3,}|#{1,6}\s+.*)\s*$")

    lines = markdown_text.splitlines()
    blocks: list[list[str]] = []
    current: list[str] = []

    def _flush():
        nonlocal current
        if current:
            # Trim leading/trailing blank lines in block.
            while current and not current[0].strip():
                current.pop(0)
            while current and not current[-1].strip():
                current.pop()
            if current:
                blocks.append(current)
        current = []

    for line in lines:
        if concept_re.match(line.strip()):
            _flush()
            current = [line]
            continue

        # If we are inside a concept block and hit a section boundary (e.g. '---', '### Q2'),
        # close the block so unrelated headings don't get included in the idea text.
        if current and boundary_re.match(line.strip()):
            _flush()
            continue

        if current:
            current.append(line)

    _flush()

    out: list[dict[str, str]] = []
    for block_lines in blocks:
        template: str | None = None
        impl_line_idx: int | None = None

        # Find the implementation example line (or its continuation).
        for i, raw in enumerate(block_lines):
            m = impl_re.search(raw)
            if not m:
                continue

            impl_line_idx = i
            tail = (m.group(1) or "").strip()

            # Case 1: template is in backticks on the same line.
            bt = backtick_re.search(tail)
            if bt:
                template = bt.group(1).strip()
                break

            # Case 2: tail itself is the template.
            if tail and ("{" in tail and "}" in tail):
                template = tail.strip().strip("`")
                break

            # Case 3: template is on the next non-empty line, often in backticks.
            for j in range(i + 1, min(i + 4, len(block_lines))):
                nxt = block_lines[j].strip()
                if not nxt:
                    continue
                bt2 = backtick_re.search(nxt)
                if bt2:
                    template = bt2.group(1).strip()
                    break
                if "{" in nxt and "}" in nxt:
                    template = nxt.strip().strip("`")
                    break
            break

        if not template or "{" not in template or "}" not in template:
            continue

        # idea = all block text except the implementation example line itself.
        idea_lines: list[str] = []
        for i, raw in enumerate(block_lines):
            if impl_line_idx is not None and i == impl_line_idx:
                continue
            idea_lines.append(raw)

        idea = "\n".join(idea_lines).strip()
        out.append({"template": template.strip(), "idea": idea})

    if not out:
        out = extract_table_template_blocks(markdown_text)
    if not out:
        out = extract_named_template_blocks(markdown_text)

    return out

def load_dataset_ids_from_csv(dataset_csv_path: Path) -> list[str]:
    if not dataset_csv_path.exists():
        return []
    ids: list[str] = []
    with dataset_csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if "id" not in (reader.fieldnames or []):
            return []
        for row in reader:
            v = (row.get("id") or "").strip()
            if v:
                ids.append(v)
    return ids

def safe_dataset_id(dataset_id: str) -> str:
    return "".join([c for c in dataset_id if c.isalnum() or c in ("-", "_")])

def run_script(args_list: list[str], cwd: Path):
    result = subprocess.run(args_list, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed: "
            + " ".join(args_list)
            + f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout


def delete_path_if_exists(path: Path):
    """Best-effort delete a file or directory."""

    try:
        if not path.exists():
            return
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
    except Exception:
        # Best-effort cleanup only; rerun should still proceed.
        return

def _wqb_campaign_store():
    """Locate CampaignStore from skill scripts (workspace src/)."""
    roots = [
        os.environ.get("WQB_ROOT"),
        os.environ.get("WQ_PROJECT_ROOT"),
        r"D:\coding\traeCN_project\wqb",
    ]
    for root in roots:
        if not root:
            continue
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            from wqb.store import CampaignStore
            db = os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")
            return CampaignStore(db)
    raise ImportError("wqb.store not found; set WQB_ROOT")


def _load_template_families() -> dict:
    """加载 toolkit config/template_families.json（字段画像驱动模板族）。

    定位顺序：WQ_TOOLKIT_DIR 覆盖 → `skill_roots()`（技能根单源：env → ~/.claude →
    ~/.codex → 历史位 → 仓库自带 Claude/skills，见同目录 skill_roots.py 模块头）。
    返回 {'families': [...], 'free_explore_family': {...}}；找不到返回 {}。
    """
    candidates = []
    env = os.environ.get("WQ_TOOLKIT_DIR")
    if env:
        # WQ_TOOLKIT_DIR 指向 scripts/，config 在其上一级
        candidates.append(os.path.join(os.path.dirname(env), "config", "template_families.json"))
        candidates.append(os.path.join(env, "config", "template_families.json"))
    candidates.extend(candidate_paths_under_skill(
        "wq-brain-campaign-toolkit", "config", "template_families.json"))
    for path in candidates:
        try:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            continue
    return {}


def _check_family_dataset_fit(family: dict, data_category: str) -> tuple:
    """机制⇄数据类别匹配门：数据集类别是否在族的 mechanism_premise.data_category 内。

    返回 (fit: bool, reason: str)。data_category 为空（未约束）→ 通过。
    这是烧配额前的拦截门：analyst 数据集不该进 event_conviction 族（KOR 实证全 fail）。
    """
    premise = family.get("mechanism_premise") or {}
    allowed = premise.get("data_category") or (family.get("field_profile_match") or {}).get("data_category") or []
    if not allowed:
        return True, ""
    dc = (data_category or "").strip().lower()
    allowed_l = [str(c).lower() for c in allowed]
    if dc and dc not in allowed_l:
        exclusion = premise.get("dataset_exclusion") or ""
        reason = (f"数据集类别 '{data_category}' 不在族 '{family.get('family_id')}' 的适用类别 {allowed}"
                  f"（机制前提不匹配）" + (f"；{exclusion}" if exclusion else ""))
        return False, reason
    return True, ""


def _prepare_family_binding(region: str, dataset_id: str, family_id: str,
                            out_dir: Path, data_category: str | None = None) -> tuple:
    """为模板族生成准备画像过滤输入（field_profile + family_match JSON 文件）。

    流程：① 机制⇄数据类别匹配门（不匹配返回 ('BLOCKED', reason)）；② 读 field_profile；
    ③ 优先取 mechanism_premise 作为 family_match（含 forbidden_shape + semantic_requirement），
    fallback 到 field_profile_match；④ 各写一个 JSON 文件供 implement_idea.py 消费。
    返回 (field_profile_path, family_match_path)；('BLOCKED', reason) 表示机制不匹配应拦截；
    (None, None) 表示跳过画像过滤（降级）。
    """
    families_cfg = _load_template_families()
    families = families_cfg.get("families") or []
    family = next((f for f in families if f.get("family_id") == family_id), None)
    if not family:
        print(f"[family] warn: template family '{family_id}' 未在 template_families.json 注册，跳过画像过滤", flush=True)
        return None, None

    # 机制⇄数据类别匹配门（烧配额前拦截）
    if data_category:
        fit, reason = _check_family_dataset_fit(family, data_category)
        if not fit:
            print(f"[family] BLOCKED: {reason}", flush=True)
            return "BLOCKED", reason

    # 优先 mechanism_premise（含 forbidden_shape + semantic_requirement），fallback field_profile_match
    family_match = family.get("mechanism_premise") or family.get("field_profile_match") or {}
    if not family_match:
        print(f"[family] warn: family '{family_id}' 无 mechanism_premise/field_profile_match，跳过画像过滤", flush=True)
        return None, None

    try:
        store = _wqb_campaign_store()
        try:
            profile_map = store.get_field_profile_map(region, dataset_id)
        finally:
            try:
                store.close()
            except Exception:
                pass
    except Exception as exc:
        print(f"[family] warn: 读取 field_profile 失败（{exc}），跳过画像过滤", flush=True)
        return None, None
    if not profile_map:
        print(f"[family] warn: {region}/{dataset_id} 无 field_profile（先跑 tools/field_profile_backfill.py），跳过画像过滤", flush=True)
        return None, None

    out_dir.mkdir(parents=True, exist_ok=True)
    fp_path = out_dir / "family_field_profile.json"
    fm_path = out_dir / "family_match.json"
    fp_path.write_text(json.dumps(profile_map, ensure_ascii=False, indent=1), encoding="utf-8")
    fm_path.write_text(json.dumps(family_match, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[family] 模板族 '{family_id}' 画像过滤就绪: {len(profile_map)} 字段画像, "
          f"match={list(family_match.keys())}", flush=True)
    return str(fp_path), str(fm_path)


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

    if s1_record and not args.ideas_file and not args.regen_ideas and args.pipeline_mode != "skeleton":
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

                try:
                    report = call_moonshot(api_key, args.moonshot_model, system_prompt, user_prompt)
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

        normalized_pairs: list[tuple[str, str]] = []
        for item in block_pairs:
            t = str(item.get("template") or "").strip()
            idea_text = str(item.get("idea") or "").strip()
            if not t:
                continue

            if dataset_ids and allowed_suffixes:
                normalized_t, ok = normalize_template_placeholders(t, dataset_ids, allowed_suffixes, dataset_code)
                if not ok:
                    continue
                normalized_pairs.append((normalized_t, idea_text))
            else:
                # No dataset ids to validate against; pass through.
                normalized_pairs.append((t, idea_text))

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
                        valid_expressions[idx] = new_expr
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
                    "ts_arg_max": "quantile(-ts_arg_max(ts_backfill({s}, 66), 20))",
                    "ts_arg_min": "quantile(ts_arg_min(ts_backfill({s}, 66), 20))",
                    "ts_av_diff": "quantile(ts_av_diff(ts_backfill({s}, 66), 20))",
                    "group_rank": "group_rank(ts_backfill({s}, 66), sector)",
                    "group_zscore": "group_zscore(ts_backfill({s}, 66), sector)",
                    "group_neutralize": "group_neutralize(ts_backfill({s}, 66), sector)",
                    "group_mean": "group_mean(ts_backfill({s}, 66), sector)",
                    "group_backfill": "group_backfill({s}, sector, 20)",
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
