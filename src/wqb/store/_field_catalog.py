# -*- coding: utf-8 -*-
"""FieldCatalogMixin: field catalog upsert/get for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, Optional

from ._common import _dumps, _loads, _now


class FieldCatalogMixin:
    """Field catalog read/write methods."""

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
            fname = f.get("id") or f.get("field_name") or f.get("name")
            if not fname:
                continue
            cur.execute(
                "SELECT id FROM fields WHERE dataset_id=? AND field_name=?",
                (ds_id, fname),
            )
            row = cur.fetchone()
            vals = (
                f.get("type") or f.get("field_type"),
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
