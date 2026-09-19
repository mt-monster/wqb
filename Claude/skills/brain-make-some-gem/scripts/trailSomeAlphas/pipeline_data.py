# -*- coding: utf-8 -*-
"""GEM 管线数据层：凭据/会话、DataFrame 工具、字段后缀候选与元数据块。

2026-09-12 从 run_pipeline.py 拆出。依赖：pipeline_paths（ace_lib）。

兼容性注意：headless_runner/run.py 通过替换 `run_pipeline.start_brain_session`
拦截会话创建 —— 本模块只提供原始实现；调用方必须经 run_pipeline 的模块全局
名（裸名）调用才能被 monkey-patch 拦截（见 run_pipeline.py 头部兼容性约束）。
"""
import json
import os
import re
from pathlib import Path

from pipeline_paths import ace_lib


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
