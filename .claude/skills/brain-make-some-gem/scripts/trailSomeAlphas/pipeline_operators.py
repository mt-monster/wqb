# -*- coding: utf-8 -*-
"""GEM 算子层：平台算子过滤与默认算子池。

2026-09-12 从 run_pipeline.py 拆出。
"""
import re

from pipeline_data import pick_first_present_column


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
