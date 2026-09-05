# -*- coding: utf-8 -*-
"""CampaignStore: denormalized campaign writes on data/wqb.db.

Existing tables (expressions/fields/waves/datasets/regions/…) keep their
FK layout. This module adds region/wave/dataset columns where missing and
a gate_results table, then upserts by (region, wave, expression).

Architecture (2026-08-29 refactor): the original 1240-line monolith was
split into focused mixins, mirroring the brain_api decomposition pattern.
CampaignStore inherits all mixins; public API is unchanged.

    CampaignStore
      ├── SchemaMixin          (_schema.py)         ensure_schema, _ensure_region/dataset/wave
      ├── LedgerMixin          (_ledger.py)         upsert/get_ledger
      ├── ExpressionsMixin     (_expressions.py)    upsert/list/history_expressions
      ├── FieldCatalogMixin    (_field_catalog.py)  upsert/get_field_catalog
      ├── FieldProfileMixin   (_field_profile.py)  upsert/get_field_profile
      ├── GateMixin            (_gate.py)           upsert/get_gate_result
      ├── BacktestMixin        (_backtest.py)       upsert_backtest_rows, record_submission
      ├── DiversityMixin       (_diversity.py)      diversity, ranking, checkpoint, rules, ideas
      ├── AlphasMixin          (_alphas.py)         get/list/search alphas
      └── SubmissionsMixin     (_submissions.py)    upsert/get/list_submissions, quota_status

Shared utilities (ExprItem, default_db_path, _now, _dumps, _loads, _as_expr)
live in _common.py and are re-exported here for backward compatibility.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

# Re-export shared utilities for backward compatibility
# (callers may do `from wqb.store.campaign import default_db_path, ExprItem, …`)
from ._common import (  # noqa: F401
    ExprItem,
    _DEFAULT_REL,
    _as_expr,
    _dumps,
    _loads,
    _now,
    default_db_path,
)

# Import mixins
from ._schema import SchemaMixin
from ._ledger import LedgerMixin
from ._expressions import ExpressionsMixin
from ._field_catalog import FieldCatalogMixin
from ._field_profile import FieldProfileMixin
from ._gate import GateMixin
from ._backtest import BacktestMixin
from ._diversity import DiversityMixin
from ._alphas import AlphasMixin
from ._submissions import SubmissionsMixin


class CampaignStore(
    SchemaMixin,
    LedgerMixin,
    ExpressionsMixin,
    FieldCatalogMixin,
    FieldProfileMixin,
    GateMixin,
    BacktestMixin,
    DiversityMixin,
    AlphasMixin,
    SubmissionsMixin,
):
    """SQLite campaign artifact store.

    All table-specific CRUD methods are inherited from focused mixins.
    This class only manages connection lifecycle and schema initialization.
    """

    def __init__(self, path: Optional[str] = None):
        self.path = path or default_db_path()
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.ensure_schema()

    @classmethod
    def from_workspace(cls, workspace_root: Optional[str] = None) -> "CampaignStore":
        return cls(default_db_path(workspace_root))

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> "CampaignStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def get_database_integration(workspace_root: Optional[str] = None) -> CampaignStore:
    """Compatibility alias for pipeline / inspect / diversity_extract."""
    return CampaignStore.from_workspace(workspace_root)
