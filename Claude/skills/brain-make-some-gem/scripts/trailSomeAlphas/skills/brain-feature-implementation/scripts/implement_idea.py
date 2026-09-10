import pandas as pd
from pathlib import Path
import argparse
import sys
import re
import json
import time
import itertools


def _safe_filename_component(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(value)).strip("_")


def _parse_dataset_folder_parts(dataset_folder_name: str) -> tuple[str, str, str] | None:
    """Parse '<datasetId>_<REGION>_delay<DELAY>' into (datasetId, REGION, DELAY).

    Returns None if parsing fails.
    """

    name = str(dataset_folder_name)
    marker = "_delay"
    pos = name.rfind(marker)
    if pos == -1:
        return None

    prefix = name[:pos]
    delay_str = name[pos + len(marker) :]
    if not delay_str.isdigit():
        return None

    region_pos = prefix.rfind("_")
    if region_pos == -1:
        return None

    dataset_id = prefix[:region_pos]
    region = prefix[region_pos + 1 :]
    if not dataset_id or not region:
        return None

    return dataset_id, region, delay_str

def load_data(dataset_name=None):
    script_dir = Path(__file__).resolve().parent
    workspace_dir = script_dir.parent
    
    if not dataset_name:
        data_root = workspace_dir / "data"
        if not data_root.exists():
            print("Error: Data directory not found.", file=sys.stderr)
            sys.exit(1)
            
        subdirs = [d for d in data_root.iterdir() if d.is_dir()]
        
        if len(subdirs) == 1:
            dataset_name = subdirs[0].name
            print(f"Auto-detected dataset: {dataset_name}", file=sys.stderr)
        elif len(subdirs) > 1:
            print("Error: Multiple datasets found. Please specify --dataset.", file=sys.stderr)
            print("Available datasets:", file=sys.stderr)
            for d in subdirs:
                print(f"  {d.name}", file=sys.stderr)
            sys.exit(1)
        else:
            print("Error: No dataset folders found inside data directory.", file=sys.stderr)
            sys.exit(1)

    dataset_dir = workspace_dir / "data" / dataset_name
    data_path = dataset_dir / f"{dataset_name}.csv"
    
    print(f"Loading data from {data_path}...", file=sys.stderr)
    try:
        df = pd.read_csv(data_path)
        return df, dataset_dir
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}. Please run fetch_dataset.py first.", file=sys.stderr)
        sys.exit(1)

def extract_keys_from_template(template):
    return re.findall(r'\{([A-Za-z0-9_]+)\}', template)


def _matches_metric(field_id: str, metric: str) -> bool:
    """Return True if field_id is a plausible match for metric.

    For very short metrics, require token-boundary matches to avoid accidental
    matches (e.g. 'ta' in 'total').
    """

    fid = str(field_id)
    m = str(metric)
    if len(m) <= 3:
        return re.search(rf"(^|_){re.escape(m)}(_|$)", fid, flags=re.IGNORECASE) is not None
    return m in fid


def _common_prefix_len(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


# ---------------------------------------------------------------------------
# 轻量语义 lint（P1a：落盘前拦截恒等式 / 裸字段 / 元数据腿；与 gate.py 闸0 同规则）
# ---------------------------------------------------------------------------

_METADATA_SUFFIX_RE = re.compile(
    r"(periodend|periodtype|fyearend|periodnum|analyststart|"
    r"curfperiod|curperiod|fiscalend|reportdate)",
    re.IGNORECASE,
)
_NOOP_SECOND = {
    "add": {0.0},
    "subtract": {0.0},
    "multiply": {0.0, 1.0},
    "divide": {1.0},
    "power": {0.0, 1.0},
}
_BARE_FIELD_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_NONFIELD_TOKENS = {
    "returns", "close", "open", "high", "low", "volume", "vwap",
    "subindustry", "industry", "sector", "market", "country",
}


def _split_top_args(s: str) -> list:
    """按顶层逗号切分函数参数（嵌套括号不切）。"""
    args, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def _iter_fn_calls(expr: str):
    """遍历表达式中所有 fn(...) 调用的 (fn_name, args_str)。"""
    for m in re.finditer(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", expr):
        fn = m.group(1)
        depth = 1
        i = m.end()
        while i < len(expr) and depth > 0:
            if expr[i] == "(":
                depth += 1
            elif expr[i] == ")":
                depth -= 1
            i += 1
        yield fn, expr[m.end():i - 1]


def _is_number(s: str):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def semantic_lint(expr: str, known_fields: set | None = None) -> list:
    """生成端闸0：恒等式 / 裸字段 / 元数据腿。返回 issue 列表（空=通过）。"""
    issues = []

    if _BARE_FIELD_RE.match(expr.strip()):
        token = expr.strip()
        if token not in _NONFIELD_TOKENS:
            issues.append(f"BARE_FIELD:{token}")

    for fn, args_str in _iter_fn_calls(expr):
        args = _split_top_args(args_str)
        if len(args) < 2:
            continue
        if fn in ("subtract", "divide") and args[0] == args[1]:
            issues.append(f"IDENTITY:{fn}({args[0]},{args[1]})")
        elif fn in _NOOP_SECOND:
            v = _is_number(args[1])
            if v is not None and v in _NOOP_SECOND[fn]:
                issues.append(f"NOOP:{fn}({args[0]},{args[1]})")

    if known_fields:
        for token in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr):
            if token in known_fields and _METADATA_SUFFIX_RE.search(token):
                issues.append(f"META_FIELD:{token}")

    return issues


def _field_matches_family(profile: dict, family_match: dict, field_id: str | None = None) -> bool:
    """判断单字段画像是否满足模板族的机制前提（mechanism_premise）/ field_profile_match 硬约束。

    family_match 支持的键（全部为可选，缺省不约束）：
      shape: [str, ...]          分布形状白名单（zero_inflated/point_mass/spread/ceiling/concentrated）
      forbidden_shape: [str, ...] 分布形状黑名单（命中即拒，mechanism_premise 新增）
      coverage_max: float        覆盖率上限（稀疏事件型用）
      coverage_min: float        覆盖率下限（稠密连续型用）
      integer: bool              是否离散字段（IntegerStatus）
      freq: [str, ...]           更新频率白名单（monthly/quarterly/...）
      data_type: [str, ...]      数据类型白名单（MATRIX/VECTOR）—— 由调用方按字段 type 注入 profile['data_type']
      semantic_requirement: {field_name_pattern: [regex, ...]}  字段名语义正则（命中其一即通过；空=不约束）

    family_match 可以是 field_profile_match 或 mechanism_premise（调用方择一传入）。
    field_id 用于 semantic_requirement 的字段名正则匹配（无则不校验语义）。
    """
    if not family_match:
        return True
    if not profile:
        # 无画像数据时不做硬过滤（降级为不约束），避免把无画像字段全排掉
        return True

    # 形状黑名单（mechanism_premise.forbidden_shape）：命中即拒，优先于白名单
    forbidden = family_match.get("forbidden_shape")
    if forbidden and (profile.get("shape") or "unknown") in forbidden:
        return False

    # shape_requirement 嵌套（mechanism_premise.shape_requirement）→ 展开合并到顶层判断
    shape_req = family_match.get("shape_requirement") or {}
    shapes = family_match.get("shape") or shape_req.get("shape")
    if shapes:
        if (profile.get("shape") or "unknown") not in shapes:
            return False

    cov = profile.get("coverage")
    cov_max = family_match.get("coverage_max") or shape_req.get("coverage_max")
    if cov_max is not None and cov is not None:
        if float(cov) > float(cov_max):
            return False
    cov_min = family_match.get("coverage_min") or shape_req.get("coverage_min")
    if cov_min is not None and cov is not None:
        if float(cov) < float(cov_min):
            return False

    if "integer" in family_match or "integer" in shape_req:
        want_int = bool(family_match.get("integer", shape_req.get("integer")))
        if bool(profile.get("integer")) != want_int:
            return False

    freqs = family_match.get("freq") or shape_req.get("freq")
    if freqs:
        if (profile.get("freq") or "") not in freqs:
            return False

    dtypes = family_match.get("data_type")
    if dtypes:
        ftype = (profile.get("data_type") or profile.get("type") or "").upper()
        if ftype and ftype not in [str(d).upper() for d in dtypes]:
            return False

    # 字段名语义正则（mechanism_premise.semantic_requirement.field_name_pattern）
    sem = family_match.get("semantic_requirement") or {}
    patterns = sem.get("field_name_pattern") or []
    if patterns and field_id:
        fid = str(field_id).lower()
        if not any(re.search(p, fid, flags=re.IGNORECASE) for p in patterns):
            return False

    return True


def filter_ids_by_family(ids, field_profile_map: dict | None, family_match: dict | None):
    """按模板族机制前提过滤绑定池。返回 (kept_ids, dropped_count)。

    field_profile_map: {field_id: profile}；family_match: 模板族的 field_profile_match 或 mechanism_premise。
    任一缺省 → 不过滤（向后兼容）。
    """
    if not field_profile_map or not family_match:
        return list(ids), 0
    kept = [fid for fid in ids
            if _field_matches_family(field_profile_map.get(fid) or {}, family_match, field_id=fid)]
    return kept, len(ids) - len(kept)


def match_single_horizon_auto(df, template, max_expressions=24, lint_enabled: bool = True,
                              field_whitelist: set | None = None,
                              field_profile_map: dict | None = None,
                              family_match: dict | None = None):
    """Generate expressions from a template by matching each {variable} to dataset field ids.

    Previous behavior required all variables to share an identical "base prefix".
    That is often too strict for datasets with mixed naming conventions.

    New behavior:
    - Build candidate lists per metric.
    - Iterate over a limited set of primary candidates.
    - For each primary candidate, pick the closest-looking candidates for other metrics
      (by common prefix length), but DO NOT require the same base.
    - Combine candidates (capped) and render expressions.
    """

    metrics = extract_keys_from_template(template)
    if not metrics:
        print("Error: No variables found in template (use {variable} format).", file=sys.stderr)
        return []

    metrics = sorted(metrics, key=len, reverse=True)
    primary = metrics[0]

    ids = df["id"].dropna().astype(str).tolist()
    if field_whitelist:
        before = len(ids)
        ids = [fid for fid in ids if fid in field_whitelist]
        print(f"[whitelist] 绑定池收窄: {before} -> {len(ids)} 字段", file=sys.stderr)
        if not ids:
            print("[whitelist] warn: 白名单与数据集字段零交集，本模板无候选", file=sys.stderr)
            return []

    # 字段画像硬约束（模板族 field_profile_match）：形状/覆盖/离散/频率分流。
    # 默认不启用（无 profile/family 时不过滤），向后兼容。
    if field_profile_map and family_match:
        before = len(ids)
        ids, dropped = filter_ids_by_family(ids, field_profile_map, family_match)
        print(f"[family] 画像过滤: {before} -> {len(ids)} 字段（剔除 {dropped} 个画像不兼容）", file=sys.stderr)
        if not ids:
            print("[family] warn: 画像过滤后绑定池为空，本模板无候选", file=sys.stderr)
            return []

    # Build candidates per metric. Exact field-id match wins: that is the
    # economic binding from a concept-first idea. Fuzzy suffix match is fallback.
    candidates_by_metric: dict[str, list[str]] = {}
    for m in metrics:
        exact = [fid for fid in ids if fid.lower() == str(m).lower()]
        cands = exact if exact else [fid for fid in ids if _matches_metric(fid, m)]
        # de-dup while preserving order
        seen = set()
        uniq = []
        for x in cands:
            if x not in seen:
                seen.add(x)
                uniq.append(x)
        candidates_by_metric[m] = uniq

    if not candidates_by_metric.get(primary):
        return []
    for m in metrics[1:]:
        if not candidates_by_metric.get(m):
            return []

    MAX_PRIMARY_CANDIDATES = 8
    MAX_SECONDARY_CHOICES = 3
    MAX_EXPRESSIONS = max(1, int(max_expressions))

    results = []
    seen_expr = set()
    known_fields = set(ids)
    lint_stats: dict[str, int] = {}

    def _bump(rule: str) -> None:
        lint_stats[rule] = lint_stats.get(rule, 0) + 1

    primary_candidates = candidates_by_metric[primary][:MAX_PRIMARY_CANDIDATES]
    for primary_id in primary_candidates:
        # For each secondary metric, choose best candidates by similarity to primary_id
        chosen_by_metric: dict[str, list[str]] = {primary: [primary_id]}
        for m in metrics[1:]:
            cands = candidates_by_metric[m]
            ranked = sorted(cands, key=lambda fid: _common_prefix_len(primary_id, fid), reverse=True)
            chosen_by_metric[m] = ranked[:MAX_SECONDARY_CHOICES]

        # Combine candidates across metrics
        metric_order = metrics
        pools = [chosen_by_metric[m] for m in metric_order]
        for combo in itertools.product(*pools):
            # 同一字段填入 2+ 占位符 → 构造上即退化（subtract(x,x)/divide(x,x) 温床），源头跳过
            if len(set(combo)) < len(combo):
                _bump("same_field_combo")
                continue
            field_map = dict(zip(metric_order, combo))
            try:
                expr = template.format(**field_map)
            except Exception:
                continue
            if expr in seen_expr:
                continue
            if lint_enabled:
                issues = semantic_lint(expr, known_fields)
                if issues:
                    for issue in issues:
                        _bump(issue.split(":", 1)[0].lower())
                    continue
            seen_expr.add(expr)
            results.append(("flex", expr))
            if len(results) >= MAX_EXPRESSIONS:
                if lint_stats:
                    print(f"[lint] blocked: {lint_stats}", file=sys.stderr)
                return results

    if lint_stats:
        print(f"[lint] blocked: {lint_stats}", file=sys.stderr)
    return results

def main():
    parser = argparse.ArgumentParser(description="Generate Alpha Expressions based on patterns")
    parser.add_argument("--template", required=True, help="Python format string (e.g. '{st_dev} / abs({mean})')")
    parser.add_argument("--dataset", help="Name of the dataset folder. Auto-detected if only one exists.")
    parser.add_argument(
        "--idea",
        default="",
        help="Optional natural-language description of what this template represents.",
    )
    parser.add_argument(
        "--max-expressions",
        type=int,
        default=24,
        help="Cap combinatorial expansion per template (default 24). Exact field-id matches stay 1:1.",
    )
    parser.add_argument(
        "--no-lint",
        action="store_true",
        help="Disable semantic lint (identity/bare-field/metadata-leg blocking). Lint is ON by default.",
    )
    parser.add_argument(
        "--field-whitelist",
        default=None,
        help="Path to a JSON array of allowed field ids (S1 field_whitelist). "
             "When provided, the binding pool is narrowed to these ids.",
    )
    parser.add_argument(
        "--field-profile",
        default=None,
        help="Path to a JSON object mapping field_id -> profile (shape/coverage/integer/freq/...). "
             "Used together with --family-match for profile-driven binding pool filtering.",
    )
    parser.add_argument(
        "--family-match",
        default=None,
        help="Path to a JSON object of template-family field_profile_match conditions "
             "(shape/coverage_max/coverage_min/integer/freq/data_type). "
             "When provided with --field-profile, binding pool is filtered by profile.",
    )

    args = parser.parse_args()

    whitelist_set = None
    if args.field_whitelist:
        try:
            wl_raw = json.loads(Path(args.field_whitelist).read_text(encoding="utf-8"))
            if isinstance(wl_raw, list):
                whitelist_set = {str(x).strip() for x in wl_raw if str(x).strip()}
                print(f"[whitelist] loaded {len(whitelist_set)} ids from {args.field_whitelist}", file=sys.stderr)
        except Exception as exc:
            print(f"[whitelist] warn: 读取失败，忽略白名单: {exc}", file=sys.stderr)
            whitelist_set = None

    field_profile_map = None
    if args.field_profile:
        try:
            fp_raw = json.loads(Path(args.field_profile).read_text(encoding="utf-8"))
            if isinstance(fp_raw, dict):
                field_profile_map = fp_raw
                print(f"[family] loaded {len(field_profile_map)} field profiles from {args.field_profile}", file=sys.stderr)
        except Exception as exc:
            print(f"[family] warn: 画像读取失败，忽略画像过滤: {exc}", file=sys.stderr)
            field_profile_map = None

    family_match = None
    if args.family_match:
        try:
            fm_raw = json.loads(Path(args.family_match).read_text(encoding="utf-8"))
            if isinstance(fm_raw, dict):
                family_match = fm_raw
                print(f"[family] loaded family_match: {list(fm_raw.keys())}", file=sys.stderr)
        except Exception as exc:
            print(f"[family] warn: family_match 读取失败，忽略: {exc}", file=sys.stderr)
            family_match = None

    df, dataset_dir = load_data(args.dataset)

    results = match_single_horizon_auto(
        df, args.template, max_expressions=args.max_expressions,
        lint_enabled=not args.no_lint, field_whitelist=whitelist_set,
        field_profile_map=field_profile_map, family_match=family_match,
    )
        
    # Output
    expression_list = []
    if not results:
        print("No matching expressions found.")
    else:
        print(f"Generated {len(results)} expressions:\n")
        # print(f"{'Context':<30} | Expression")
        # print("-" * 120)
        
        for context, expr in results:
            # print(f"{context:<30} | {expr}")
            expression_list.append(expr)
            
    # Save results to JSON (Always save for debugging)
    # Use nanosecond precision to avoid collisions when called in a tight loop.
    timestamp = time.time_ns()
    json_output = {
        "template": args.template,
        "idea": args.idea,
        "expression_list": expression_list
    }
    
    parts = _parse_dataset_folder_parts(dataset_dir.name)
    if parts:
        dataset_id, region, delay_str = parts
        prefix = f"{_safe_filename_component(dataset_id)}_{_safe_filename_component(region)}_{_safe_filename_component(delay_str)}"
    else:
        # Fallback: keep output stable even if dataset folder naming differs.
        prefix = _safe_filename_component(dataset_dir.name) or "dataset"

    output_file = dataset_dir / f"{prefix}_idea_{timestamp}.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=4, ensure_ascii=False)
        print(f"\nSaved idea configuration to: {output_file}")
    except Exception as e:
        print(f"Error saving JSON: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
