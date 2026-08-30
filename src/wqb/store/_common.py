# -*- coding: utf-8 -*-
"""Shared utilities and constants for CampaignStore mixins.

Kept in a dedicated module so every mixin (`_schema`, `_ledger`,
`_expressions`, …) imports the same module-level helpers instead of
redefining them.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

ExprItem = Union[str, Dict[str, Any]]

_DEFAULT_REL = Path("data") / "wqb.db"


def default_db_path(workspace_root: Optional[str] = None) -> str:
    env = os.environ.get("WQB_DB_PATH")
    if env:
        return env
    if workspace_root:
        return str(Path(workspace_root) / _DEFAULT_REL)
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / _DEFAULT_REL
        if cand.exists() or (parent / "src" / "wqb").is_dir():
            return str(parent / _DEFAULT_REL)
    return str(Path.cwd() / _DEFAULT_REL)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _loads(raw: Any) -> Any:
    if raw is None:
        return None
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw


def _as_expr(item: ExprItem) -> Dict[str, Any]:
    if isinstance(item, str):
        return {"expression": item}
    expr = item.get("expression") or item.get("expr") or item.get("code") or item.get("regular") or ""
    out = dict(item)
    out["expression"] = expr
    return out
