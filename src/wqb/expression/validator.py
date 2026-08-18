"""wqb.expression.validator — batch diversity gates and shape classification.

``check_batch`` enforces the 5 diversity gates before a batch may be
dispatched to ``create_multi_simulation``:

1. ``shape_signatures`` — ≥2 distinct shape signatures.
2. ``outer_wrappers`` — ≥2 distinct outermost operators.
3. ``dual_field`` — ≥3 expressions combining two or more fields.
4. ``group_vars`` — when group operators appear, ≥2 distinct group vars.
5. ``windows`` — ≥2 distinct lookback windows (when windows are used).
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Set, Tuple

from wqb.config import GHOST_OPERATORS, SHAPE_CLASSES, get_operator_family
from wqb.expression.grammar import Node, ParseError, parse_expression

# Binary combiners whose two operands form a "shape".
_BINARY_COMBINERS = {"subtract", "divide", "add", "multiply", "max", "min"}

# Group variables are not datafields.
_GROUP_VARS = {
    "market", "sector", "subindustry", "industry", "country",
    "exchange", "currency", "quantile",
}

# Operators + constants never count as datafields.
_NON_FIELD_NAMES = _GROUP_VARS | GHOST_OPERATORS | {"true", "false", "nan"}


def _is_operator(name: str) -> bool:
    return get_operator_family(name) != "NONE" or name in GHOST_OPERATORS


def _fields_of(node: Node) -> Set[str]:
    """Collect datafield identifiers from an AST."""
    out: Set[str] = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if n.is_call:
            stack.extend(n.args)
        else:
            name = n.name.lower()
            if name in _NON_FIELD_NAMES:
                continue
            if re.fullmatch(r"\d+(?:\.\d+)?", name):
                continue
            if not _is_operator(name):
                out.add(name)
    return out


def _outer_wrapper(node: Node) -> str:
    return node.name if node.is_call else ""


def _window_bucket(expr: str) -> str:
    """Bucket the largest numeric window used in the expression."""
    numbers = [int(float(m)) for m in re.findall(r"\b(\d+(?:\.\d+)?)\b", expr)]
    if not numbers:
        return "none"
    top = max(numbers)
    if top <= 5:
        return "short"
    if top <= 20:
        return "mid"
    if top <= 60:
        return "long"
    return "xlong"


def _arg_family(arg: Node) -> str:
    """Family of the pre-op wrapping an operand (NONE for raw fields)."""
    if arg.is_call:
        return get_operator_family(arg.name)
    return "NONE"


def _shape_signature(expr: str) -> Tuple[str, str, str, str, str]:
    """5-tuple: (top_op, combiner, fam_a, fam_b, window_bucket)."""
    try:
        root = parse_expression(expr)
    except ParseError:
        return ("INVALID", "", "NONE", "NONE", "none")
    top = root.name if root.is_call else ""
    if root.is_call and root.name in _BINARY_COMBINERS and len(root.args) >= 2:
        fam_a = _arg_family(root.args[0])
        fam_b = _arg_family(root.args[1])
        return (top, root.name, fam_a, fam_b, _window_bucket(expr))
    return (top, "", "NONE", "NONE", _window_bucket(expr))


def classify_shape(expr: str) -> str:
    """Classify a binary-combiner expression into a shape class.

    S0: both operands raw fields. S1: same non-NONE family both sides.
    S5: one side wrapped, other raw. S4: two different families.
    S9: anything else.
    """
    try:
        root = parse_expression(expr)
    except ParseError:
        return "S9"
    if root.is_call and root.name in _BINARY_COMBINERS and len(root.args) >= 2:
        fam_a = _arg_family(root.args[0])
        fam_b = _arg_family(root.args[1])
        if fam_a == "NONE" and fam_b == "NONE":
            return "S0"
        if fam_a != "NONE" and fam_b != "NONE":
            return "S1" if fam_a == fam_b else "S4"
        return "S5"
    return "S9"


def _group_vars_of(node: Node) -> Set[str]:
    out: Set[str] = set()
    stack = [node]
    while stack:
        n = stack.pop()
        if not n.is_call:
            continue
        if n.name.startswith("group_") and len(n.args) >= 2:
            gv = n.args[1]
            if not gv.is_call:
                out.add(gv.name)
        stack.extend(n.args)
    return out


def check_batch(expressions: List[str]) -> Tuple[bool, str, Dict]:
    """Validate a batch of expressions against the 5 diversity gates.

    Returns ``(ok, reason, details)`` where details carries ``gates``,
    ``per_expression`` and ``total``.
    """
    per_expression: List[Dict] = []
    signatures: Set[Tuple] = set()
    wrappers: Set[str] = set()
    dual_field_count = 0
    group_vars: Set[str] = set()
    windows: Set[str] = set()
    has_group_ops = False

    for expr in expressions:
        try:
            root = parse_expression(expr)
        except ParseError:
            root = None
        fields = _fields_of(root) if root else set()
        if root is not None:
            wrappers.add(_outer_wrapper(root))
            group_vars |= _group_vars_of(root)
            has_group_ops = has_group_ops or any(
                n.name.startswith("group_")
                for n in _iter_calls(root)
            )
        sig = _shape_signature(expr)
        signatures.add(sig)
        if sig[4] != "none":
            windows.add(sig[4])
        if len(fields) >= 2:
            dual_field_count += 1
        per_expression.append({
            "expression": expr,
            "shape_class": classify_shape(expr),
            "shape_signature": [str(x) for x in sig],
            "fields": sorted(fields),
        })

    gates: Dict[str, Dict] = {
        "shape_signatures": {
            "passed": len(signatures) >= 2,
            "detail": f"{len(signatures)} distinct shape signature(s)",
        },
        "outer_wrappers": {
            "passed": len(wrappers) >= 2,
            "detail": f"{len(wrappers)} distinct outer wrapper(s)",
        },
        "dual_field": {
            "passed": dual_field_count >= 3,
            "detail": f"{dual_field_count} dual-field expression(s)",
        },
        "group_vars": {
            "passed": (not has_group_ops) or len(group_vars) >= 2,
            "detail": f"group vars: {sorted(group_vars) or 'none'}",
        },
        "windows": {
            "passed": len(windows) >= 2,
            "detail": f"window buckets: {sorted(windows) or 'none'}",
        },
    }

    failed = [name for name, g in gates.items() if not g["passed"]]
    ok = not failed
    reason = "" if ok else "failed gates: " + ", ".join(failed)
    details = {
        "gates": gates,
        "per_expression": per_expression,
        "total": len(expressions),
        "failed_gates": failed,
    }
    return ok, reason, details


def _iter_calls(node: Node):
    stack = [node]
    while stack:
        n = stack.pop()
        if n.is_call:
            yield n
            stack.extend(n.args)
