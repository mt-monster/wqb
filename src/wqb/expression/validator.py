"""wqb.expression.validator - Batch diversity validation and shape classification.

This module implements the batch-level diversity gates mandated by the
orchestrator SKILL.md (section 13).  Every simulation batch must pass all
five gates before dispatch:

1. **Dual-field** – at least 3 expressions contain two or more data fields.
2. **Outer wrappers** – at least 2 distinct top-level operators.
3. **Windows** – at least 2 distinct window parameters.
4. **Group variables** – at least 2 distinct group variables (when group
   operators are used).
5. **Shape signatures** – at least 2 distinct shape signatures.

A *shape signature* is a 5-tuple::

    (top_op, binop, pre_op_family_a, pre_op_family_b, window_bucket)

that captures the structural "shape" of an expression for diversity purposes.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple

from wqb.config import OP_FAMILIES, get_operator_family
from wqb.expression.grammar import (
    extract_fields,
    extract_operators,
    extract_windows,
    parse_expression,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Operators that combine two sub-signals into one (the "binop" in the
#: shape signature).  Extended 2026-08-02 to include logical combination ops.
_BINARY_COMBINATION_OPS: Set[str] = {
    "subtract", "divide", "multiply", "add",
    "or", "and",  # logical combination ops
}

#: Group operators whose last argument is a group-variable name.
#: Extended 2026-08-02 to include all group operators from the platform.
_GROUP_OPS: Set[str] = {
    "group_neutralize",
    "group_rank",
    "group_zscore",
    "group_mean",
    "group_max",
    "group_min",
    "group_backfill",
    "group_scale",
    "group_count",
    "group_sum",
    "group_std_dev",
}


# ---------------------------------------------------------------------------
# Shape signature
# ---------------------------------------------------------------------------

def _find_binary_combination(
    parsed: Dict[str, Any],
) -> Tuple[Optional[str], Optional[Dict], Optional[Dict]]:
    """Breadth-first search for the first binary combination operator.

    Returns
    -------
    tuple
        ``(op_name, left_operand, right_operand)`` or ``(None, None, None)``
        if no binary combination operator is found.
    """
    queue: deque = deque([parsed])
    while queue:
        node = queue.popleft()
        if not isinstance(node, dict):
            continue

        op = node.get("operator")
        args = node.get("args", [])

        if op in _BINARY_COMBINATION_OPS and len(args) >= 2:
            return op, args[0], args[1]

        for arg in args:
            if isinstance(arg, dict):
                queue.append(arg)

    return None, None, None


def _operand_pre_op_family(arg: Optional[Dict]) -> str:
    """Return the operator family for a binary operand, or ``"NONE"``.

    If the operand is a raw field (not a function call), the family is
    ``"NONE"``.
    """
    if not isinstance(arg, dict):
        return "NONE"

    if arg.get("type") == "call":
        op_name = arg.get("operator", "")
        return get_operator_family(op_name)

    return "NONE"


def _window_bucket(windows: List[int]) -> str:
    """Classify a list of window values into a bucket.

    Buckets:
    - ``"short"``  – max window ≤ 5
    - ``"mid"``    – 6 ≤ max window ≤ 20
    - ``"long"``   – 21 ≤ max window ≤ 63
    - ``"xlong"``  – max window > 63
    - ``"none"``   – no windows present
    """
    if not windows:
        return "none"
    max_w = max(windows)
    if max_w <= 5:
        return "short"
    elif max_w <= 20:
        return "mid"
    elif max_w <= 63:
        return "long"
    else:
        return "xlong"


def _shape_signature(expr: str) -> Tuple[Optional[str], Optional[str], str, str, str]:
    """Compute the shape signature of an expression.

    The signature is a 5-tuple::

        (top_op, binop, pre_op_family_a, pre_op_family_b, window_bucket)

    where:

    * *top_op* – the outermost operator name (or ``None``).
    * *binop* – the main binary combination operator name
      (``subtract`` / ``divide`` / ``multiply`` / ``add``), or ``None``.
    * *pre_op_family_a* – operator family of the A-side pre-processor
      (e.g. ``"RANK"``, ``"TS_RANK"``), or ``"NONE"`` if the A side is a
      raw field.
    * *pre_op_family_b* – same for the B side.
    * *window_bucket* – one of ``"short"``, ``"mid"``, ``"long"``,
      ``"xlong"``, ``"none"``.

    Parameters
    ----------
    expr:
        A BRAIN expression string.

    Returns
    -------
    tuple
        The 5-element shape signature.
    """
    parsed = parse_expression(expr)
    top_op = parsed.get("operator")

    windows = extract_windows(expr)
    w_bucket = _window_bucket(windows)

    binop, left, right = _find_binary_combination(parsed)

    fam_a = _operand_pre_op_family(left)
    fam_b = _operand_pre_op_family(right)

    return (top_op, binop, fam_a, fam_b, w_bucket)


# ---------------------------------------------------------------------------
# Shape classes
# ---------------------------------------------------------------------------

SHAPE_CLASSES: Dict[str, Dict[str, str]] = {
    "S1": {
        "name": "symmetric_dual_preop",
        "description": (
            "Symmetric dual pre-processing "
            "(pre_op_family_a == pre_op_family_b != NONE)"
        ),
    },
    "S4": {
        "name": "asymmetric_dual_preop",
        "description": (
            "Asymmetric dual pre-processing "
            "(pre_op_family_a != pre_op_family_b, both != NONE)"
        ),
    },
    "S5": {
        "name": "single_side_preop",
        "description": (
            "Single-side pre-processing "
            "(one side has pre_op, other side raw field)"
        ),
    },
    "S9": {
        "name": "cross_layer",
        "description": (
            "Cross-layer combination "
            "(one side rank family, other side group family)"
        ),
    },
}


def classify_shape(expr: str) -> str:
    """Classify an expression into one of the shape classes S1/S4/S5/S9.

    The classification is based on the pre-op families of the two operands
    of the main binary combination operator:

    * **S9** – cross-layer: one side is ``RANK`` family, the other is
      ``GROUP`` family.
    * **S1** – symmetric dual pre-op: both sides have the same non-``NONE``
      family.
    * **S4** – asymmetric dual pre-op: both sides have pre-ops but from
      different families.
    * **S5** – single-side pre-op: exactly one side has a pre-op.
    * **S0** – no pre-op on either side (raw spread / ratio).

    Parameters
    ----------
    expr:
        A BRAIN expression string.

    Returns
    -------
    str
        One of ``"S1"``, ``"S4"``, ``"S5"``, ``"S9"``, or ``"S0"``.
    """
    _, _, fam_a, fam_b, _ = _shape_signature(expr)

    # S9: cross-layer (rank vs group)
    if (fam_a == "RANK" and fam_b == "GROUP") or (
        fam_a == "GROUP" and fam_b == "RANK"
    ):
        return "S9"

    # S1: symmetric dual pre-op
    if fam_a != "NONE" and fam_a == fam_b:
        return "S1"

    # S4: asymmetric dual pre-op
    if fam_a != "NONE" and fam_b != "NONE" and fam_a != fam_b:
        return "S4"

    # S5: single-side pre-op
    if (fam_a != "NONE") != (fam_b != "NONE"):
        return "S5"

    return "S0"


# ---------------------------------------------------------------------------
# Group variable extraction
# ---------------------------------------------------------------------------

def _extract_group_vars(parsed: Dict[str, Any]) -> List[str]:
    """Recursively extract group-variable names from group operators.

    The last argument of a group operator (e.g. ``group_neutralize(x, market)``)
    is treated as the group variable.

    Parameters
    ----------
    parsed:
        A parsed expression dictionary from :func:`parse_expression`.

    Returns
    -------
    list[str]
        Group-variable names found in the expression tree.
    """
    group_vars: List[str] = []

    def _visit(node: Any) -> None:
        if not isinstance(node, dict):
            return

        op = node.get("operator")
        args = node.get("args")

        if op is not None and args:
            if op in _GROUP_OPS and len(args) > 0:
                last = args[-1]
                if isinstance(last, dict) and last.get("type") == "field":
                    group_vars.append(last["value"])
            for arg in args:
                _visit(arg)

    _visit(parsed)
    return group_vars


# ---------------------------------------------------------------------------
# Batch diversity check
# ---------------------------------------------------------------------------

def check_batch(
    expressions: List[str],
) -> Tuple[bool, str, Dict[str, Any]]:
    """Validate that a batch of expressions meets all diversity gates.

    All five rules below must be satisfied for ``ok=True``:

    1. At least 3 expressions contain two or more data fields (dual-field).
    2. At least 2 distinct outer-wrapper operators.
    3. At least 2 distinct window parameters.
    4. At least 2 distinct group variables (only checked when group
       operators are present in the batch).
    5. At least 2 distinct shape signatures.

    Parameters
    ----------
    expressions:
        List of BRAIN expression strings.

    Returns
    -------
    tuple[bool, str, dict]
        ``(ok, reason, details)`` where:

        * *ok* – ``True`` if all gates pass.
        * *reason* – human-readable summary of failures (or success message).
        * *details* – dictionary with per-gate counts and per-expression
          analysis.
    """
    dual_field_count = 0
    outer_wrappers: Set[Optional[str]] = set()
    all_windows: Set[int] = set()
    all_group_vars: Set[str] = set()
    all_shapes: Set[Tuple] = set()
    uses_groups = False

    per_expr: List[Dict[str, Any]] = []

    for expr in expressions:
        parsed = parse_expression(expr)
        fields = extract_fields(expr)
        windows = extract_windows(expr)
        ops = extract_operators(expr)

        # Dual-field
        is_dual = len(fields) >= 2
        if is_dual:
            dual_field_count += 1

        # Outer wrapper
        top_op = parsed.get("operator")
        if top_op:
            outer_wrappers.add(top_op)

        # Windows
        for w in windows:
            all_windows.add(w)

        # Group variables
        expr_group_vars = _extract_group_vars(parsed)
        if expr_group_vars:
            uses_groups = True
        for gv in expr_group_vars:
            all_group_vars.add(gv)

        # Also detect group operators without explicit group-var extraction
        if any(op in _GROUP_OPS for op in ops):
            uses_groups = True

        # Shape signature
        sig = _shape_signature(expr)
        all_shapes.add(sig)

        per_expr.append({
            "expression": expr,
            "fields": fields,
            "field_count": len(fields),
            "is_dual_field": is_dual,
            "top_op": top_op,
            "windows": windows,
            "group_vars": expr_group_vars,
            "shape_signature": list(sig),
            "shape_class": classify_shape(expr),
        })

    # Evaluate gates
    gates: List[Tuple[str, bool, str]] = []

    gates.append((
        "dual_field",
        dual_field_count >= 3,
        f"need >=3 dual-field expressions, got {dual_field_count}",
    ))

    gates.append((
        "outer_wrappers",
        len(outer_wrappers) >= 2,
        f"need >=2 distinct outer wrappers, got {sorted(w for w in outer_wrappers if w)}",
    ))

    gates.append((
        "windows",
        len(all_windows) >= 2,
        f"need >=2 distinct windows, got {sorted(all_windows)}",
    ))

    if uses_groups:
        gates.append((
            "group_vars",
            len(all_group_vars) >= 2,
            f"need >=2 distinct group variables, got {sorted(all_group_vars)}",
        ))

    gates.append((
        "shape_signatures",
        len(all_shapes) >= 2,
        f"need >=2 distinct shape signatures, got {len(all_shapes)}",
    ))

    failed = [(name, msg) for name, passed, msg in gates if not passed]
    ok = len(failed) == 0

    if ok:
        reason = "all diversity checks passed"
    else:
        reason = "; ".join(f"[{name}] {msg}" for name, msg in failed)

    details: Dict[str, Any] = {
        "total": len(expressions),
        "dual_field_count": dual_field_count,
        "distinct_outer_wrappers": sorted(w for w in outer_wrappers if w),
        "distinct_windows": sorted(all_windows),
        "uses_groups": uses_groups,
        "distinct_group_vars": sorted(all_group_vars),
        "distinct_shape_count": len(all_shapes),
        "distinct_shapes": [list(s) for s in sorted(all_shapes, key=lambda t: tuple(str(x) for x in t))],
        "gates": {name: {"passed": passed, "message": msg} for name, passed, msg in gates},
        "per_expression": per_expr,
    }

    return ok, reason, details
