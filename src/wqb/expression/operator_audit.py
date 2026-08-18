"""wqb.expression.operator_audit — catalog vs live-platform operator audit.

Ghost operators are declared in the operator catalog but do not exist on the
live BRAIN platform (e.g. ``ts_entropy``, ``tanh``). Dispatching them burns
simulation budget on guaranteed errors, so every batch must pass
``ensure_safe_for_dispatch`` before ``create_multi_simulation``.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Set

from wqb.config import GHOST_OPERATORS, VERIFIED_SAFE_OPERATORS
from wqb.expression.grammar import extract_identifiers


class GhostOperatorError(ValueError):
    """Raised when an expression contains a ghost operator."""


def _operator_library() -> Set[str]:
    """Declared operator library: verified catalog ops + declared ghosts."""
    return set(VERIFIED_SAFE_OPERATORS) | GHOST_OPERATORS


def get_ghost_operators() -> Set[str]:
    """Return the ghost-operator blacklist."""
    return set(GHOST_OPERATORS)


def get_verified_operators() -> Set[str]:
    """Return verified-safe operators, excluding any ghost."""
    return set(VERIFIED_SAFE_OPERATORS) - GHOST_OPERATORS


def operator_audit(live_ops: Iterable[str],
                   output_path: Optional[str] = None) -> Dict:
    """Diff the declared operator library against live platform operators.

    - verified: declared and live.
    - ghost: declared but missing from the live platform.
    - missing: live but absent from the declared library.

    Optionally writes the audit result to ``output_path`` (JSON).
    """
    live = set(live_ops)
    library = _operator_library()
    verified = sorted(library & live)
    ghost = sorted(library - live)
    missing = sorted(live - library)
    summary = {
        "total_live": len(live),
        "total_verified": len(verified),
        "total_ghost": len(ghost),
        "total_library_declared": len(library),
        "total_missing": len(missing),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    result = {
        "verified": verified,
        "ghost": ghost,
        "missing": missing,
        "summary": summary,
    }
    if output_path:
        parent = os.path.dirname(os.path.abspath(output_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    return result


def ensure_safe_for_dispatch(expressions: List[str],
                             verified_ops: Optional[Set[str]] = None) -> None:
    """Raise ``GhostOperatorError`` if any expression uses a ghost operator.

    The ghost blacklist is authoritative: even if a caller-supplied
    ``verified_ops`` set contains the ghost name, dispatch is blocked.
    """
    ghosts = get_ghost_operators()
    for expr in expressions:
        used = extract_identifiers(expr)
        bad = sorted(used & ghosts)
        if bad:
            raise GhostOperatorError(
                f"Ghost operator(s) {bad} in expression: {expr}"
            )
