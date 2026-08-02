"""wqb.expression.grammar - BRAIN alpha expression parser and operator metadata.

This module provides:

* ``_OP_ARITY`` – a mapping from operator name to its argument count
  (1 = unary, 2 = binary, 3 = ternary).  Operators that accept a variable
  number of arguments (e.g. ``ts_regression``) are stored as a ``list[int]``.
* ``GHOST_OPERATORS`` – re-exported from :mod:`wqb.config` for convenience.
* ``VERIFIED_OPERATORS`` – the set of operators known to exist on the live
  BRAIN platform (all declared operators minus ghosts, union with the
  explicitly verified-safe list).
* ``parse_expression(expr)`` – a recursive-descent parser that converts a
  BRAIN expression string into a structured dictionary.
* ``extract_operators(expr)`` / ``extract_fields(expr)`` /
  ``extract_windows(expr)`` – lightweight extraction helpers.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set, Union

from wqb.config import GHOST_OPERATORS as _CFG_GHOST
from wqb.config import VERIFIED_SAFE_OPERATORS

# ---------------------------------------------------------------------------
# Operator arity table
# ---------------------------------------------------------------------------

# Arity values: 1 = unary, 2 = binary, 3 = ternary.
# Operators with variable arity use a list (e.g. ts_regression accepts
# both 2-arg and 3-arg forms).
_OP_ARITY: Dict[str, Union[int, List[int]]] = {
    # ---- Unary (arity = 1) ----
    "rank": 1,
    "zscore": 1,
    "sign": 1,
    "abs": 1,
    "log": 1,
    "sqrt": 1,
    "ts_rank": 1,
    "ts_zscore": 1,
    "ts_quantile": 1,
    "ts_av_diff": 1,
    "ts_decay_linear": 1,
    "ts_ir": 1,
    "ts_max_diff": 1,
    "last_diff_value": 1,
    "days_from_last_change": 1,
    "nan_mask": 1,
    "hump": 1,
    "bucket": 1,
    "densify": 1,
    "jump_decay": 1,
    "ts_kurtosis": 1,
    "ts_co_skewness": 1,
    "group_max": 1,
    "group_min": 1,
    "group_rank": 1,
    "group_zscore": 1,
    "group_mean": 1,
    "group_neutralize": 1,
    "neutralize": 1,
    "rank_by_side": 1,
    # --- Added 2026-08-02: base-level cross-sectional & math (operator audit) ---
    "reverse": 1,         # negate: -x
    "inverse": 1,         # reciprocal: 1/x
    "winsorize": 1,       # winsorize(x, std=4) — clip outliers cross-sectionally
    "normalize": 1,       # normalize(x, useStd=false, limit=0.0)
    "quantile": 1,        # quantile(x, driver="gaussian", sigma=1.0) — cross-sectional
    "scale": 1,           # scale(x, scale=1, longscale=1, shortscale=1)
    "is_nan": 1,          # is_nan(x) — NaN detection
    "not": 1,             # not(x) — logical NOT
    "ts_step": 1,         # ts_step(1) — constant step function
    # --- Genius-level (require genius account) ---
    "pasteurize": 1,      # genius: pasteurize(x)
    "vec_count": 1,       # genius: vec_count(x)
    "vec_stddev": 1,      # genius: vec_stddev(x)
    "vec_range": 1,       # genius: vec_range(x)

    # ---- Binary (arity = 2) ----
    "add": 2,
    "subtract": 2,
    "multiply": 2,
    "divide": 2,
    "min": 2,
    "max": 2,
    "ts_corr": 2,
    "ts_covariance": 2,
    "vec_sum": 2,
    "vec_avg": 2,
    "vec_max": 2,
    "vec_min": 2,
    "vec_norm": 2,
    "vec_choose": 2,
    "signed_power": 2,
    "power": 2,
    # --- Added 2026-08-02: logical & window-parameter binary (operator audit) ---
    "or": 2,              # or(input1, input2) — logical OR
    "and": 2,             # and(input1, input2) — logical AND

    # ---- Window-parameter binary (arity = 2, second arg is a window) ----
    "ts_delay": 2,
    "ts_delta": 2,
    "ts_returns": 2,
    "ts_mean": 2,
    "ts_std_dev": 2,
    "ts_sum": 2,
    "ts_min": 2,
    "ts_max": 2,
    "ts_backfill": 2,
    "group_backfill": 2,
    # --- Added 2026-08-02: additional window-parameter binary ---
    "ts_product": 2,      # ts_product(x, d) — product over window
    "ts_scale": 2,        # ts_scale(x, d, constant=0) — scale to window range
    "ts_arg_max": 2,      # ts_arg_max(x, d) — position of max in window
    "ts_arg_min": 2,      # ts_arg_min(x, d) — position of min in window
    "ts_count_nans": 2,   # ts_count_nans(x, d) — count NaNs in window
    # --- Group binary (x, group) ---
    "group_scale": 2,     # group_scale(x, group)
    # --- Genius-level group binary ---
    "group_count": 2,     # genius: group_count(x, group)
    "group_sum": 2,       # genius: group_sum(x, group)
    "group_std_dev": 2,   # genius: group_std_dev(x, group)
    "group_cartesian_product": 2,  # genius: group_cartesian_product(g1, g2)

    # ---- Variable-arity operators ----
    # ts_regression: 2-arg (y, x) or 3-arg (y, x, d) / 4-arg (y, x, d, lag)
    "ts_regression": [2, 3, 4],

    # ---- Ternary (arity = 3) ----
    "trade_when": 3,
    # --- Added 2026-08-02: conditional & k-th element ---
    "if_else": 3,         # if_else(cond, true_val, false_val) — conditional logic
    "kth_element": 3,     # kth_element(x, d, k, ignore="NaN") — k-th element in window

    # ---- Quaternary (arity = 4) — genius-level ---
    "tail": 4,            # genius: tail(x, lower, upper, newval) — tail clipping
    "ts_target_tvr_decay": 4,  # genius: TVR-targeted decay
    "ts_target_tvr_hump": 4,   # genius: TVR-targeted hump
}

# ---------------------------------------------------------------------------
# Ghost and verified operator sets
# ---------------------------------------------------------------------------

GHOST_OPERATORS: Set[str] = set(_CFG_GHOST)

#: All operators declared in the library that are NOT ghosts, unioned with
#: the explicitly verified-safe list.  These are safe to use in dispatched
#: expressions.
VERIFIED_OPERATORS: Set[str] = (
    {op for op in _OP_ARITY if op not in GHOST_OPERATORS}
    | set(VERIFIED_SAFE_OPERATORS)
)

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches an identifier immediately followed by '(' (an operator call).
_OP_CALL_RE: re.Pattern[str] = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")

# Matches any identifier token.
_IDENT_RE: re.Pattern[str] = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

# Matches a standalone numeric literal (not part of an identifier).
_NUM_RE: re.Pattern[str] = re.compile(r"(?<![a-zA-Z0-9_])-?\d+(?:\.\d+)?")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _split_top_level(s: str) -> List[str]:
    """Split *s* on commas that are at parenthesis depth 0.

    Parameters
    ----------
    s:
        The interior of a function-call argument list, e.g.
        ``"ts_rank(close, 5), ts_rank(volume, 10)"``.

    Returns
    -------
    list[str]
        Top-level argument substrings, stripped of surrounding whitespace.
    """
    parts: List[str] = []
    depth = 0
    current: List[str] = []
    for ch in s:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth -= 1
            current.append(ch)
        elif ch == "," and depth == 0:
            token = "".join(current).strip()
            if token:
                parts.append(token)
            current = []
        else:
            current.append(ch)
    token = "".join(current).strip()
    if token:
        parts.append(token)
    return parts


def _parse_arg(s: str) -> Dict[str, Any]:
    """Parse a single argument token into a typed dictionary.

    Returns one of::

        {"type": "call",    "operator": "...", "args": [...]}
        {"type": "number",  "value": 5}
        {"type": "field",   "value": "close"}
    """
    s = s.strip()

    # Try to match a function call:  name(args...)
    match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$", s, re.DOTALL)
    if match:
        op_name = match.group(1)
        inner = match.group(2)
        arg_strs = _split_top_level(inner)
        return {
            "type": "call",
            "operator": op_name,
            "args": [_parse_arg(a) for a in arg_strs],
        }

    # Try to match a numeric literal
    if re.match(r"^-?\d+(?:\.\d+)?$", s):
        if "." in s:
            return {"type": "number", "value": float(s)}
        return {"type": "number", "value": int(s)}

    # Otherwise it is a field or group-variable name
    return {"type": "field", "value": s}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_expression(expr: str) -> Dict[str, Any]:
    """Parse a BRAIN alpha expression string into a structured dictionary.

    The returned dictionary has the following shape::

        {
            "operator": "subtract",        # top-level operator name
            "arity": 2,                    # number of top-level arguments
            "args": [ ... ],               # list of parsed argument dicts
            "fields": ["close", "volume"], # unique field names (in order)
            "operators": ["subtract", "ts_rank"],  # unique op names
            "windows": [5, 10],            # all numeric constants
            "raw": "subtract(ts_rank(...))",
        }

    Each element in *args* is itself a dict produced by :func:`_parse_arg`::

        {"type": "call",   "operator": "ts_rank", "args": [...]}
        {"type": "number", "value": 5}
        {"type": "field",  "value": "close"}

    Parameters
    ----------
    expr:
        A BRAIN expression string, e.g.
        ``"subtract(ts_rank(close, 5), ts_rank(volume, 10))"``.

    Returns
    -------
    dict
        Structured representation of the expression.
    """
    expr = expr.strip()

    fields = extract_fields(expr)
    operators = extract_operators(expr)
    windows = extract_windows(expr)

    match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$", expr, re.DOTALL)
    if match:
        op_name = match.group(1)
        inner = match.group(2)
        arg_strs = _split_top_level(inner)
        parsed_args = [_parse_arg(a) for a in arg_strs]
        return {
            "operator": op_name,
            "arity": len(parsed_args),
            "args": parsed_args,
            "fields": fields,
            "operators": operators,
            "windows": windows,
            "raw": expr,
        }

    # Bare field or constant (no function call wrapper)
    parsed = _parse_arg(expr)
    return {
        "operator": None,
        "arity": 0,
        "args": [parsed],
        "fields": fields,
        "operators": operators,
        "windows": windows,
        "raw": expr,
    }


def extract_operators(expr: str) -> List[str]:
    """Extract all operator names from *expr*, preserving first-occurrence order.

    An operator is any identifier immediately followed by an opening
    parenthesis.

    Parameters
    ----------
    expr:
        BRAIN expression string.

    Returns
    -------
    list[str]
        Unique operator names in order of first appearance.
    """
    seen: Set[str] = set()
    result: List[str] = []
    for m in _OP_CALL_RE.finditer(expr):
        name = m.group(1)
        if name not in seen:
            seen.add(name)
            result.append(name)
    return result


def extract_fields(expr: str) -> List[str]:
    """Extract all field names from *expr*, preserving first-occurrence order.

    A field is any identifier that is **not** immediately followed by ``(``
    (i.e. not an operator) and is not a numeric literal.

    Parameters
    ----------
    expr:
        BRAIN expression string.

    Returns
    -------
    list[str]
        Unique field / group-variable names in order of first appearance.
    """
    result: List[str] = []
    seen: Set[str] = set()
    for m in _IDENT_RE.finditer(expr):
        ident = m.group()
        # Skip if this identifier is followed by '(' → it's an operator
        rest = expr[m.end():]
        if rest.lstrip().startswith("("):
            continue
        if ident in seen:
            continue
        seen.add(ident)
        result.append(ident)
    return result


def extract_windows(expr: str) -> List[int]:
    """Extract all numeric constants (window parameters) from *expr*.

    Parameters
    ----------
    expr:
        BRAIN expression string.

    Returns
    -------
    list[int]
        All integer constants found in the expression, in order of
        appearance.  Float values are truncated to ``int``.
    """
    windows: List[int] = []
    for m in _NUM_RE.finditer(expr):
        val = m.group()
        if "." in val:
            windows.append(int(float(val)))
        else:
            windows.append(int(val))
    return windows


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def is_known_operator(name: str) -> bool:
    """Return ``True`` if *name* is a declared operator in :data:`_OP_ARITY`."""
    return name in _OP_ARITY


def is_ghost_operator(name: str) -> bool:
    """Return ``True`` if *name* is a purged ghost operator."""
    return name in GHOST_OPERATORS


def get_arity(name: str) -> Union[int, List[int], None]:
    """Return the arity (or list of valid arities) for *name*.

    Returns ``None`` if the operator is unknown.
    """
    return _OP_ARITY.get(name)
