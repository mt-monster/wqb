# -*- coding: utf-8 -*-
"""GateMixin: gate result upsert/get for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, Optional

from ._common import _dumps, _loads, _now


class GateMixin:
    """Gate result read/write methods."""

    def upsert_gate_result(
        self, region: str, wave: str, dataset: str, report: Dict[str, Any]
    ) -> Dict[str, Any]:
        now = _now()
        all_pass = 1 if report.get("all_pass") else 0
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id FROM gate_results WHERE region=? AND wave=? AND dataset=?",
            (region, str(wave), dataset),
        )
        row = cur.fetchone()
        payload = _dumps(report)
        if row:
            cur.execute(
                """UPDATE gate_results SET all_pass=?, report_json=?, updated_at=?
                   WHERE id=?""",
                (all_pass, payload, now, int(row[0])),
            )
            action = "updated"
        else:
            cur.execute(
                """INSERT INTO gate_results
                   (region, wave, dataset, all_pass, report_json, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?)""",
                (region, str(wave), dataset, all_pass, payload, now, now),
            )
            action = "inserted"
        self.connection.commit()
        self.upsert_ledger(region, f"gate_w{wave}_{dataset}", report)
        return {"action": action, "region": region, "wave": str(wave), "dataset": dataset}

    def get_gate_result(self, region: str, wave: str, dataset: str) -> Optional[Dict[str, Any]]:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT report_json FROM gate_results WHERE region=? AND wave=? AND dataset=?",
            (region, str(wave), dataset),
        )
        row = cur.fetchone()
        if row:
            return _loads(row[0])
        return self.get_ledger(region, f"gate_w{wave}_{dataset}")
