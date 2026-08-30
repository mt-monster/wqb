# -*- coding: utf-8 -*-
"""LedgerMixin: ledger_kv and workflow_configs CRUD for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._common import _dumps, _loads, _now


class LedgerMixin:
    """ledger_kv and workflow_configs read/write methods."""

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

    # -- workflow_configs ---------------------------------------------------

    def upsert_workflow_config(self, config_key: str, config_value: Any, description: Optional[str] = None) -> Dict[str, Any]:
        """Upsert workflow configuration."""
        cur = self.connection.cursor()
        payload = _dumps(config_value)
        now = _now()
        cur.execute(
            "SELECT id FROM workflow_configs WHERE config_key=?",
            (config_key,),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE workflow_configs SET config_value=?, description=?, updated_at=? WHERE config_key=?",
                (payload, description, now, config_key),
            )
            action = "updated"
        else:
            cur.execute(
                "INSERT INTO workflow_configs (config_key, config_value, description, created_at, updated_at) "
                "VALUES (?,?,?,?,?)",
                (config_key, payload, description, now, now),
            )
            action = "inserted"
        self.connection.commit()
        return {"action": action, "config_key": config_key}

    def get_workflow_config(self, config_key: str) -> Any:
        """Get workflow configuration."""
        cur = self.connection.cursor()
        cur.execute(
            "SELECT config_value FROM workflow_configs WHERE config_key=?",
            (config_key,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return _loads(row[0])

    def list_workflow_configs(self, prefix: Optional[str] = None) -> List[str]:
        """List workflow config keys."""
        cur = self.connection.cursor()
        if prefix:
            cur.execute(
                "SELECT config_key FROM workflow_configs WHERE config_key LIKE ? ORDER BY config_key",
                (f"{prefix}%",),
            )
        else:
            cur.execute("SELECT config_key FROM workflow_configs ORDER BY config_key")
        return [row[0] for row in cur.fetchall()]
