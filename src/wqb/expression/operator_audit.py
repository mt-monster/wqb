"""wqb.expression.operator_audit - Ghost operator detection and platform reconciliation.

This module implements the operator audit pipeline described in the
orchestrator SKILL.md (section 16):

* :class:`GhostOperatorError` – raised when a dispatched expression contains
  a purged ghost operator.
* :func:`operator_audit` – compares the library's declared operator set
  (from :data:`wqb.config.OP_FAMILIES` and
  :data:`wqb.expression.grammar._OP_ARITY`) with the live operator list
  returned by the BRAIN platform, classifying each operator as *verified*,
  *ghost*, or *missing*.
* :func:`ensure_safe_for_dispatch` – pre-flight check that raises
  :class:`GhostOperatorError` if any expression in a batch references a
  ghost operator.
* :func:`get_ghost_operators` – returns the hardcoded ghost-operator
  blacklist (purged 2026-04-23).

Typical usage::

    from wqb.expression.operator_audit import operator_audit, ensure_safe_for_dispatch

    # 1. Reconcile with the live platform
    report = operator_audit(live_operators=[...])

    # 2. Guard a batch before dispatch
    ensure_safe_for_dispatch(expressions=[...])
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from wqb.config import (
    GHOST_OPERATORS as _CFG_GHOST,
    OP_FAMILIES,
    VERIFIED_SAFE_OPERATORS,
)
from wqb.expression.grammar import (
    _OP_ARITY,
    VERIFIED_OPERATORS,
    extract_operators,
)


# ---------------------------------------------------------------------------
# Exception
# ---------------------------------------------------------------------------

class GhostOperatorError(Exception):
    """Raised when a dispatched expression contains a purged ghost operator.

    Ghost operators were removed from the library on 2026-04-23 after it was
    discovered that they never existed on the live BRAIN platform.  Any
    expression referencing one of these operators will fail at simulation
    time with a platform-side error, so this pre-flight check prevents
    wasted API quota.
    """

    def __init__(self, operator: str, expression: str = "") -> None:
        self.operator = operator
        self.expression = expression
        if expression:
            msg = (
                f"Ghost operator '{operator}' found in expression: {expression}. "
                f"This operator was purged on 2026-04-23 and does not exist "
                f"on the live BRAIN platform."
            )
        else:
            msg = (
                f"Ghost operator '{operator}' (purged 2026-04-23) "
                f"does not exist on the live BRAIN platform."
            )
        super().__init__(msg)


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def get_ghost_operators() -> Set[str]:
    """Return the hardcoded set of ghost operators (purged 2026-04-23).

    Returns
    -------
    set[str]
        A copy of the :data:`wqb.config.GHOST_OPERATORS` set.
    """
    return set(_CFG_GHOST)


def _build_library_operator_set() -> Set[str]:
    """Collect every operator declared in the library.

    The union of:

    * All operators listed in :data:`wqb.config.OP_FAMILIES`.
    * All keys of :data:`wqb.expression.grammar._OP_ARITY`.
    * All entries in :data:`wqb.config.VERIFIED_SAFE_OPERATORS`.
    * All entries in :data:`wqb.config.GHOST_OPERATORS` (for reporting).
    """
    library_ops: Set[str] = set()

    for family_ops in OP_FAMILIES.values():
        library_ops.update(family_ops)

    library_ops.update(_OP_ARITY.keys())
    library_ops.update(VERIFIED_SAFE_OPERATORS)
    library_ops.update(_CFG_GHOST)  # include known ghosts for audit reporting

    return library_ops


# ---------------------------------------------------------------------------
# Operator audit
# ---------------------------------------------------------------------------

_DEFAULT_OUTPUT_PATH = "data/operators_verified.json"


def operator_audit(
    live_operators: List[str],
    output_path: str = _DEFAULT_OUTPUT_PATH,
) -> Dict[str, Any]:
    """Reconcile library-declared operators with the live platform list.

    Compares the set of operators declared in the library (from
    :data:`OP_FAMILIES`, :data:`_OP_ARITY`, and :data:`VERIFIED_SAFE_OPERATORS`)
    against the operators returned by the BRAIN platform's ``/operators``
    endpoint.

    Classification:

    * **verified** – present in both the library and the platform.
    * **ghost** – declared in the library (including the hardcoded
      :data:`GHOST_OPERATORS` blacklist) but absent from the platform.
      These operators must never be dispatched.
    * **missing** – present on the platform but not declared in the library.
      These are candidates for library extension.

    The result is written to *output_path* as a JSON file and also returned
    as a dictionary.

    Parameters
    ----------
    live_operators:
        List of operator names returned by the live BRAIN platform.
    output_path:
        Path to write the JSON audit report.  Parent directories are
        created automatically.  Defaults to ``"data/operators_verified.json"``.

    Returns
    -------
    dict
        A dictionary with keys:

        * ``verified`` – sorted list of verified operator names.
        * ``ghost`` – sorted list of ghost operator names.
        * ``missing`` – sorted list of missing (extension-candidate) names.
        * ``known_ghosts`` – sorted list of hardcoded ghost operators.
        * ``summary`` – dict with counts.
        * ``timestamp`` – ISO-format generation timestamp.
    """
    from datetime import datetime, timezone

    library_ops = _build_library_operator_set()
    live_set: Set[str] = set(op.strip() for op in live_operators if op.strip())

    # Operators in both library and platform
    verified = library_ops & live_set

    # Operators declared in library (including known ghosts) but not on platform
    ghost = library_ops - live_set

    # Operators on platform but not declared anywhere in the library
    missing = live_set - library_ops

    # Hardcoded known ghosts (subset of ghost)
    known_ghosts = _CFG_GHOST & ghost

    result: Dict[str, Any] = {
        "verified": sorted(verified),
        "ghost": sorted(ghost),
        "missing": sorted(missing),
        "known_ghosts": sorted(known_ghosts),
        "summary": {
            "total_library_declared": len(library_ops),
            "total_live": len(live_set),
            "total_verified": len(verified),
            "total_ghost": len(ghost),
            "total_missing": len(missing),
            "total_known_ghosts": len(known_ghosts),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Write to file
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


# ---------------------------------------------------------------------------
# Dispatch safety check
# ---------------------------------------------------------------------------

def _load_verified_ops(path: str = _DEFAULT_OUTPUT_PATH) -> Set[str]:
    """Load the verified-operator set from a JSON audit report.

    If the file does not exist, falls back to
    :data:`wqb.expression.grammar.VERIFIED_OPERATORS`.

    Parameters
    ----------
    path:
        Path to the JSON file produced by :func:`operator_audit`.

    Returns
    -------
    set[str]
        The set of verified operator names.
    """
    p = Path(path)
    if p.exists():
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            verified_list = data.get("verified", [])
            if verified_list:
                return set(verified_list)
        except (json.JSONDecodeError, OSError):
            pass

    # Fallback to the grammar's compiled verified set
    return set(VERIFIED_OPERATORS)


def ensure_safe_for_dispatch(
    expressions: List[str],
    verified_ops: Optional[Set[str]] = None,
) -> None:
    """Pre-flight check: ensure no expression references a ghost operator.

    Scans every expression in *expressions* for operator names and raises
    :class:`GhostOperatorError` if any ghost operator (from
    :data:`GHOST_OPERATORS`) is found.

    Parameters
    ----------
    expressions:
        List of BRAIN expression strings to be dispatched.
    verified_ops:
        Optional set of verified operator names.  If ``None``, the function
        loads the verified set from ``data/operators_verified.json``
        (falling back to :data:`VERIFIED_OPERATORS` if the file is absent).
        This set is used for informational logging of unverified—but
        non-ghost—operators.

    Raises
    ------
    GhostOperatorError
        If any expression contains an operator present in
        :data:`GHOST_OPERATORS`.

    Examples
    --------
    >>> from wqb.expression.operator_audit import ensure_safe_for_dispatch
    >>> ensure_safe_for_dispatch(["subtract(close, volume)"])  # safe
    >>> ensure_safe_for_dispatch(["ts_entropy(close, 5)"])  # raises
    Traceback (most recent call last):
        ...
    wqb.expression.operator_audit.GhostOperatorError: Ghost operator 'ts_entropy' ...
    """
    if verified_ops is None:
        verified_ops = _load_verified_ops()

    ghost_ops = get_ghost_operators()

    for expr in expressions:
        ops_in_expr = extract_operators(expr)
        for op in ops_in_expr:
            if op in ghost_ops:
                raise GhostOperatorError(operator=op, expression=expr)
            # Operators not in verified_ops and not in ghost_ops are
            # "unverified" — they may or may not exist on the platform.
            # We do not raise here; the caller can inspect verified_ops
            # separately if stricter checking is desired.


# ---------------------------------------------------------------------------
# Convenience: rebuild verified set from library (no platform call needed)
# ---------------------------------------------------------------------------

def get_verified_operators() -> Set[str]:
    """Return the set of all library-declared non-ghost operators.

    This is equivalent to :data:`wqb.expression.grammar.VERIFIED_OPERATORS`
    and is provided as a convenience entry point from this module.

    Returns
    -------
    set[str]
        Operators declared in the library that are NOT in
        :data:`GHOST_OPERATORS`.
    """
    library_ops = _build_library_operator_set()
    return library_ops - _CFG_GHOST
