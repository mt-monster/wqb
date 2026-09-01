# -*- coding: utf-8 -*-
"""LedgerMixin: ledger_kv CRUD for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict

from ._common import _dumps, _loads, _now


class LedgerMixin:
    """ledger_kv read/write methods."""

    # -- ledger ------------------------------------------------------------

    def upsert_ledger(self, region: str, key: str, value: Any) -> Dict[str, Any]:
        cur = self.connection.cursor()
        payload = _dumps(value)
        now = _now()
        cur.execute(
            "SELECT id FROM ledger_kv WHERE region=? AND key=?",
            (region, key),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE ledger_kv SET value=?, updated_at=? WHERE region=? AND key=?",
                (payload, now, region, key),
            )
            action = "updated"
        else:
            cur.execute(
                "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) "
                "VALUES (?,?,?,?,?)",
                (region, key, payload, now, now),
            )
            action = "inserted"
        self.connection.commit()
        return {"action": action, "region": region, "key": key}

    def get_ledger(self, region: str, key: str) -> Any:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            (region, key),
        )
        row = cur.fetchone()
        if not row:
            return None
        return _loads(row[0])

    # -- workflow_configs 已废弃（功能被 ledger_kv 替代），相关 CRUD 已移除
