# -*- coding: utf-8 -*-
"""FieldCatalogMixin: field catalog upsert/get for CampaignStore."""
from __future__ import annotations

from statistics import median
from typing import Any, Dict, List, Optional

from ._common import _dumps, _loads, _now


class FieldCatalogMixin:
    """Field catalog read/write methods."""

    @staticmethod
    def _field_name(field: Dict[str, Any]) -> Optional[str]:
        return field.get("id") or field.get("field_name") or field.get("name")

    @staticmethod
    def _field_type(field: Dict[str, Any]) -> Optional[str]:
        return field.get("type") or field.get("field_type")

    @staticmethod
    def _prefix_for(field_name: str, depth: int = 1) -> str:
        parts = [p for p in str(field_name).split("_") if p]
        if not parts:
            return str(field_name)
        depth = max(1, min(depth, len(parts)))
        return "_".join(parts[:depth])

    @staticmethod
    def _risk_flags(prefix: str, fields: List[Dict[str, Any]], coverages: List[float]) -> List[str]:
        flags: List[str] = []
        vector_count = sum(1 for f in fields if str(FieldCatalogMixin._field_type(f) or "").upper() == "VECTOR")
        if vector_count:
            flags.append("vector_fields_present")
        if coverages:
            med = median(coverages)
            if med < 0.5:
                flags.append("low_coverage_median")
        if prefix in {"news", "event", "vec", "vector"}:
            flags.append("sparse_or_complex_prefix")
        return flags

    def build_field_prefix_clusters(
        self,
        region: str,
        dataset: str,
        prefix_depth: int = 1,
        top_n: int = 10,
        samples_per_cluster: int = 5,
        coverage_high: float = 0.85,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """Build S1 field-prefix cluster summary from DB catalog and persist to ledger_kv."""
        catalog = self.get_field_catalog(region, dataset)
        if not catalog:
            return {"error": f"catalog not found: {region}/{dataset}"}

        fields = [f for f in (catalog.get("fields") or []) if self._field_name(f)]
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for field in fields:
            name = self._field_name(field)
            if not name:
                continue
            prefix = self._prefix_for(name, depth=prefix_depth)
            grouped.setdefault(prefix, []).append(field)

        clusters: List[Dict[str, Any]] = []
        for prefix, items in grouped.items():
            names = [self._field_name(f) for f in items if self._field_name(f)]
            coverages = [float(f.get("coverage")) for f in items if f.get("coverage") is not None]
            vector_count = sum(1 for f in items if str(self._field_type(f) or "").upper() == "VECTOR")
            high_cov = sum(1 for c in coverages if c >= coverage_high)
            clusters.append({
                "prefix": prefix,
                "count": len(items),
                "coverage_mean": round(sum(coverages) / len(coverages), 4) if coverages else None,
                "coverage_median": round(median(coverages), 4) if coverages else None,
                "high_coverage_count": high_cov,
                "vector_count": vector_count,
                "sample_fields": names[:samples_per_cluster],
                "risk_flags": self._risk_flags(prefix, items, coverages),
            })

        clusters.sort(key=lambda x: (-x["count"], x["prefix"]))
        risk_clusters = [c for c in clusters if c["risk_flags"]]
        payload = {
            "region": region,
            "dataset": dataset,
            "prefix_depth": prefix_depth,
            "total_fields": len(fields),
            "total_clusters": len(clusters),
            "top_clusters": clusters[:top_n],
            "risk_clusters": risk_clusters[:top_n],
            "source": "field_prefix_cluster_db",
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s1_prefix_{dataset}", payload)
        return payload

    def get_field_prefix_clusters(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        """Read persisted S1 field-prefix cluster summary from ledger_kv."""
        cached = self.get_ledger(region, f"s1_prefix_{dataset}")
        return cached if isinstance(cached, dict) else None

    @staticmethod
    def _derive_candidate_field_pool(summary: Optional[Dict[str, Any]], max_fields: int = 30) -> List[str]:
        if not summary:
            return []
        pool: List[str] = []
        seen = set()
        for cluster in summary.get("top_clusters") or []:
            if cluster.get("risk_flags"):
                continue
            for name in cluster.get("sample_fields") or []:
                if name and name not in seen:
                    seen.add(name)
                    pool.append(name)
                if len(pool) >= max_fields:
                    return pool
        for cluster in summary.get("top_clusters") or []:
            for name in cluster.get("sample_fields") or []:
                if name and name not in seen:
                    seen.add(name)
                    pool.append(name)
                if len(pool) >= max_fields:
                    return pool
        return pool

    def build_candidate_field_pool(
        self,
        region: str,
        dataset: str,
        max_fields: int = 30,
        persist: bool = True,
    ) -> Dict[str, Any]:
        """Derive S2 candidate field pool from prefix summary and persist to ledger_kv."""
        summary = self.get_field_prefix_clusters(region, dataset)
        if not summary:
            summary = self.build_field_prefix_clusters(region, dataset, persist=True)
        if summary.get("error"):
            return summary
        pool = self._derive_candidate_field_pool(summary, max_fields=max_fields)
        payload = {
            "region": region,
            "dataset": dataset,
            "candidate_field_pool": pool,
            "pool_size": len(pool),
            "source": "s1_prefix_summary",
            "updated_at": _now(),
        }
        if persist:
            self.upsert_ledger(region, f"s2_field_pool_{dataset}", payload)
        return payload

    def get_candidate_field_pool(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        """Read persisted S2 candidate field pool from ledger_kv."""
        cached = self.get_ledger(region, f"s2_field_pool_{dataset}")
        return cached if isinstance(cached, dict) else None

    def upsert_field_catalog(self, region: str, catalog: Dict[str, Any]) -> Dict[str, Any]:
        dataset = catalog.get("dataset") or catalog.get("id")
        if not dataset:
            raise ValueError("catalog missing dataset")
        fields = catalog.get("fields") or []
        extra = {
            "field_count": catalog.get("field_count", len(fields)),
            "data_type": catalog.get("data_type"),
            "catalog_json": _dumps(catalog),
            "status": "scanned",
        }
        ds_id = self._ensure_dataset(region, dataset, extra)
        cur = self.connection.cursor()
        n = 0
        for f in fields:
            fname = self._field_name(f)
            if not fname:
                continue
            cur.execute(
                "SELECT id FROM fields WHERE dataset_id=? AND field_name=?",
                (ds_id, fname),
            )
            row = cur.fetchone()
            vals = (
                self._field_type(f),
                f.get("coverage"),
                f.get("userCount") if "userCount" in f else f.get("user_count"),
                f.get("alphaCount") if "alphaCount" in f else f.get("alpha_count"),
                (f.get("description") or "")[:240],
                f.get("field_group"),
            )
            if row:
                cur.execute(
                    """UPDATE fields SET field_type=?, coverage=?, user_count=?,
                       alpha_count=?, description=?, field_group=? WHERE id=?""",
                    vals + (int(row[0]),),
                )
            else:
                cur.execute(
                    """INSERT INTO fields
                       (dataset_id, field_name, field_type, coverage, user_count,
                        alpha_count, description, field_group, created_at)
                       VALUES (?,?,?,?,?,?,?,?,?)""",
                    (ds_id, fname) + vals + (_now(),),
                )
            n += 1
        self.connection.commit()
        self.upsert_ledger(region, f"catalog_{dataset}", catalog)
        return {"n": n, "region": region, "dataset": dataset}

    def get_field_catalog(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        cached = self.get_ledger(region, f"catalog_{dataset}")
        if isinstance(cached, dict) and cached.get("fields"):
            return cached
        rid = self._ensure_region(region)
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id, data_type, catalog_json, field_count FROM datasets "
            "WHERE name=? AND region_id=?",
            (dataset, rid),
        )
        ds = cur.fetchone()
        if not ds:
            return None
        if ds["catalog_json"]:
            blob = _loads(ds["catalog_json"])
            if isinstance(blob, dict):
                return blob
        cur.execute(
            "SELECT field_name, field_type, coverage, user_count, alpha_count, "
            "description, field_group FROM fields WHERE dataset_id=?",
            (int(ds["id"]),),
        )
        fields = []
        for r in cur.fetchall():
            fields.append({
                "id": r["field_name"],
                "type": r["field_type"],
                "coverage": r["coverage"],
                "userCount": r["user_count"],
                "alphaCount": r["alpha_count"],
                "description": r["description"],
                "field_group": r["field_group"],
            })
        return {
            "dataset": dataset,
            "region": region,
            "data_type": ds["data_type"] or "MATRIX",
            "field_count": len(fields),
            "fields": fields,
        }
