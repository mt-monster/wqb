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
from typing import Any, Dict, List, Optional

from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
from wqb.config import is_pseudo_alpha  # 伪 alpha 黑名单（经济学池生成侧剔除，单源）

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
from ._field_catalog import FieldCatalogMixin, POOL_BUILDER_VERSION
from ._field_economic import build_economic_field_pool, classify_fields
from ._field_patterns import (
    extract_field_patterns,
    build_field_combination_rules,
    persist_field_patterns,
    merge_field_patterns_across_waves,
)
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

    # ---- 经济学字段归类（2026-09-25 落地） ----

    def build_economic_field_pool(
        self,
        region: str,
        dataset: str,
        max_fields: int = 30,
        min_per_category: int = 2,
        max_per_category: int = 8,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """按经济学含义构建字段池（替代/增强旧 _pick_cross_cluster）。

        与旧方法的区别：
        - 旧：按"主体 token"分簇（mean_ask_price → ask），无经济学含义
        - 新：按经济学类别分簇（value/growth/quality/...），有经济学约束
        """
        catalog = self.get_field_catalog(region, dataset)
        if not catalog or not catalog.get("fields"):
            return {"error": f"catalog not found: {region}/{dataset}"}

        fields = [f for f in catalog["fields"] if self._field_name(f)
                  and not is_pseudo_alpha(self._field_name(f))]  # 剔除 riskfree/beta/基准伪 alpha
        pool, stats = build_economic_field_pool(
            fields, max_fields=max_fields,
            min_per_category=min_per_category,
            max_per_category=max_per_category,
        )

        payload = {
            "region": region,
            "dataset": dataset,
            "candidate_field_pool": pool,
            "pool_size": len(pool),
            "economic_stats": stats,
            "source": "economic_category",
            # 必须与 _field_catalog.POOL_BUILDER_VERSION 同步（get_candidate_field_pool
            # 按版本判缓存新鲜度，硬编码不一致 → 经济学池缓存永不命中，每次重建）
            "builder_version": POOL_BUILDER_VERSION,
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s2_field_pool_{dataset}", payload)
        return payload

    def classify_dataset_fields(
        self,
        region: str,
        dataset: str,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """对数据集字段做经济学含义聚类并持久化。"""
        catalog = self.get_field_catalog(region, dataset)
        if not catalog or not catalog.get("fields"):
            return {"error": f"catalog not found: {region}/{dataset}"}

        fields = [f for f in catalog["fields"] if self._field_name(f)]
        clusters = classify_fields(fields)

        payload = {
            "region": region,
            "dataset": dataset,
            "total_fields": len(fields),
            "categories": {
                cat: {
                    "count": len(fields),
                    "top_fields": [
                        self._field_name(f) for f in fields[:5]
                    ],
                    "avg_quality": round(
                        sum(self._quality_score(f) for f in fields) / len(fields), 3
                    ) if fields else 0,
                }
                for cat, fields in clusters.items()
            },
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s1_economic_clusters_{dataset}", payload)
        return payload

    # ---- S6 字段组合规律挖掘（2026-09-25 落地） ----

    def extract_wave_field_patterns(
        self,
        region: str,
        wave: str,
        min_sharpe: float = 0.5,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """从指定波的回测结果中提取字段组合规律。"""
        cur = self.connection.cursor()
        # 2026-09-25 修复：backtest_results 表达式列是 code（非 expression）；
        # code 为空的行回退 expression_id → expressions 表。
        cur.execute(
            "SELECT COALESCE(b.code, e.expression) AS expr, b.sharpe, b.fitness "
            "FROM backtest_results b LEFT JOIN expressions e ON b.expression_id = e.id "
            "WHERE b.region=? AND b.wave=? AND b.sharpe IS NOT NULL",
            (region, str(wave)),
        )
        rows = [
            {"expression": r[0], "sharpe": r[1], "fitness": r[2]}
            for r in cur.fetchall() if r[0]
        ]
        if not rows:
            return {"error": f"no backtest results for {region}/{wave}"}

        patterns = extract_field_patterns(rows, min_sharpe=min_sharpe)
        rules = build_field_combination_rules(patterns)

        if persist:
            persist_field_patterns(self, region, str(wave), patterns, rules)

        return {
            "region": region,
            "wave": wave,
            "total_rows": len(rows),
            "patterns": patterns,
            "rules": rules,
        }

    def merge_region_field_patterns(
        self,
        region: str,
        waves: Optional[List[str]] = None,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """合并多波字段组合规律，找跨波稳定模式。"""
        if waves is None:
            # 自动获取最近 10 波
            cur = self.connection.cursor()
            cur.execute(
                "SELECT DISTINCT wave FROM backtest_results WHERE region=? "
                "ORDER BY id DESC LIMIT 10",
                (region,),
            )
            waves = [str(r[0]) for r in cur.fetchall()]

        merged = merge_field_patterns_across_waves(self, region, waves)
        if persist and "error" not in merged:
            self.upsert_ledger(region, f"s6_field_patterns_{region}_merged", merged)
        return merged

    def __init__(self, path: Optional[str] = None):
        self.path = path or default_db_path()
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = db_connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA cache_size=-64000")
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
