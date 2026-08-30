# -*- coding: utf-8 -*-
"""DiversityMixin: diversity potential, ranking, checkpoint, rules, reviews, ideas."""
from __future__ import annotations

from typing import Any, Dict, Optional

from ._common import _dumps, _loads, _now


class DiversityMixin:
    """Diversity potential, ranking, checkpoint, methodology, review, idea methods."""

    def upsert_diversity(self, region: str, dataset: str, data: Dict[str, Any]) -> None:
        ds_id = self._ensure_dataset(region, dataset)
        rid = self._ensure_region(region)
        now = _now()
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id FROM diversity_potential WHERE region_id=? AND dataset_id=?",
            (rid, ds_id),
        )
        row = cur.fetchone()
        payload = _dumps(data)
        vals = (
            data.get("diversity_score"),
            data.get("recommended_rounds"),
            _dumps(data.get("field_categories") or data.get("field_groups") or {}),
            _dumps(data.get("operator_buckets") or {}),
            _dumps(data.get("parameter_space") or {}),
            payload,
            now,
        )
        if row:
            cur.execute(
                """UPDATE diversity_potential SET diversity_score=?, recommended_rounds=?,
                   field_categories=?, operator_buckets=?, parameter_space=?,
                   payload_json=?, updated_at=? WHERE id=?""",
                vals + (int(row[0]),),
            )
        else:
            cur.execute(
                """INSERT INTO diversity_potential
                   (region_id, dataset_id, diversity_score, recommended_rounds,
                    field_categories, operator_buckets, parameter_space,
                    payload_json, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (rid, ds_id) + vals + (now,),
            )
        self.connection.commit()
        self.upsert_ledger(region, f"diversity_{dataset}", data)

    save_diversity_potential = upsert_diversity

    def get_diversity(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        cached = self.get_ledger(region, f"diversity_{dataset}")
        if isinstance(cached, dict):
            return cached
        rid = self._ensure_region(region)
        cur = self.connection.cursor()
        cur.execute(
            "SELECT d.payload_json FROM diversity_potential d "
            "JOIN datasets s ON d.dataset_id=s.id "
            "WHERE d.region_id=? AND s.name=?",
            (rid, dataset),
        )
        row = cur.fetchone()
        if not row:
            return None
        return _loads(row[0])

    load_diversity_potential = get_diversity

    def upsert_ranking(self, region: str, payload: Dict[str, Any]) -> None:
        self.upsert_ledger(region, "s0_ranking", payload)

    def get_ranking(self, region: str) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, "s0_ranking")
        return val if isinstance(val, dict) else None

    def upsert_checkpoint(self, region: str, wave: str, ck: Dict[str, Any]) -> None:
        self.upsert_ledger(region, f"ckpt_w{wave}", ck)

    def get_checkpoint(self, region: str, wave: str) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, f"ckpt_w{wave}")
        return val if isinstance(val, dict) else None

    def upsert_methodology_rules(self, region: str, data: Dict[str, Any]) -> None:
        self.upsert_ledger(region, "methodology_rules", data)

    def get_methodology_rules(self, region: str) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, "methodology_rules")
        return val if isinstance(val, dict) else None

    def upsert_review(self, region: str, tag: str, payload: Dict[str, Any]) -> None:
        self.upsert_ledger(region, f"review_{tag}", payload)

    def upsert_idea(self, region: str, dataset: str, delay: int, idea: Dict[str, Any]) -> None:
        self.upsert_ledger(region, f"s2_{dataset}_d{delay}_idea", idea)

    def get_idea(self, region: str, dataset: str, delay: int) -> Optional[Dict[str, Any]]:
        val = self.get_ledger(region, f"s2_{dataset}_d{delay}_idea")
        return val if isinstance(val, dict) else None
