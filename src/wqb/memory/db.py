"""wqb.memory.db — SimulationDB: hash cache + trajectory bookkeeping.

Backed by SQLite. Five tables:

- ``trajectories`` — one row per mining trajectory (session × arm).
- ``trajectory_steps`` — ordered steps of a trajectory.
- ``insights`` — positive/negative lessons attached to trajectories.
- ``batch_log`` — every dispatched simulation batch.
- ``sim_cache`` — expression+settings hash → simulation result (dedup).
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

REQUIRED_TABLES = [
    "trajectories",
    "trajectory_steps",
    "insights",
    "batch_log",
    "sim_cache",
]


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def _json_loads(s: Optional[str]) -> Any:
    if not s:
        return None
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SimulationDB:
    """SQLite-backed simulation cache and bookkeeping store."""

    def __init__(self, path: str):
        self.path = path
        self.connection: Optional[sqlite3.Connection] = sqlite3.connect(path)

    # -- lifecycle ---------------------------------------------------------

    def init_tables(self) -> None:
        cur = self.connection.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS trajectories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                region TEXT,
                universe TEXT,
                dataset TEXT,
                paradigm TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS trajectory_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trajectory_id INTEGER NOT NULL,
                step_type TEXT,
                expression TEXT,
                settings_json TEXT,
                result_json TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trajectory_id INTEGER NOT NULL,
                kind TEXT,
                text TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS batch_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                batch_id TEXT,
                expressions_json TEXT,
                results_json TEXT,
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS sim_cache (
                hash TEXT PRIMARY KEY,
                expression TEXT NOT NULL,
                settings_key TEXT,
                result_json TEXT,
                created_at TEXT,
                updated_at TEXT
            );
            """
        )
        self.connection.commit()

    def doctor(self) -> Dict:
        """Health check: required tables present + per-table row counts."""
        cur = self.connection.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing = {row[0] for row in cur.fetchall()}
        missing = [t for t in REQUIRED_TABLES if t not in existing]
        counts: Dict[str, int] = {}
        for table in REQUIRED_TABLES:
            if table in existing:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cur.fetchone()[0]
        return {"ok": not missing, "missing_tables": missing,
                "table_counts": counts}

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()

    def __enter__(self) -> "SimulationDB":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # -- hash cache --------------------------------------------------------

    def compute_hash(self, expression: str, settings: Dict) -> str:
        """Deterministic SHA-256 of expression + settings (key-order safe)."""
        payload = _json_dumps({"expression": expression, "settings": settings})
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def put_cached(self, h: str, expression: str, settings_key: str,
                   result: Any) -> None:
        cur = self.connection.cursor()
        cur.execute("SELECT 1 FROM sim_cache WHERE hash = ?", (h,))
        now = _now_iso()
        if cur.fetchone():
            cur.execute(
                "UPDATE sim_cache SET expression=?, settings_key=?, "
                "result_json=?, updated_at=? WHERE hash=?",
                (expression, settings_key, _json_dumps(result), now, h),
            )
        else:
            cur.execute(
                "INSERT INTO sim_cache "
                "(hash, expression, settings_key, result_json, created_at, "
                "updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (h, expression, settings_key, _json_dumps(result), now, now),
            )
        self.connection.commit()

    def get_cached(self, h: str) -> Optional[Any]:
        cur = self.connection.cursor()
        cur.execute("SELECT result_json FROM sim_cache WHERE hash = ?", (h,))
        row = cur.fetchone()
        if row is None:
            return None
        return _json_loads(row[0])

    # -- bookkeeping ---------------------------------------------------------

    def record_trajectory(self, session_id: str, region: str, universe: str,
                          dataset: str, paradigm: str) -> int:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO trajectories "
            "(session_id, region, universe, dataset, paradigm, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, region, universe, dataset, paradigm, _now_iso()),
        )
        self.connection.commit()
        return cur.lastrowid

    def add_trajectory_step(self, trajectory_id: int, step_type: str,
                            expression: str, settings: Dict,
                            result: Any) -> int:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO trajectory_steps "
            "(trajectory_id, step_type, expression, settings_json, "
            "result_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (trajectory_id, step_type, expression, _json_dumps(settings),
             _json_dumps(result), _now_iso()),
        )
        self.connection.commit()
        return cur.lastrowid

    def add_insight(self, trajectory_id: int, kind: str, text: str) -> int:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO insights (trajectory_id, kind, text, created_at) "
            "VALUES (?, ?, ?, ?)",
            (trajectory_id, kind, text, _now_iso()),
        )
        self.connection.commit()
        return cur.lastrowid

    def record_batch(self, session_id: str, batch_id: str,
                     expressions: List[str], results: List[Any]) -> int:
        cur = self.connection.cursor()
        cur.execute(
            "INSERT INTO batch_log "
            "(session_id, batch_id, expressions_json, results_json, "
            "created_at) VALUES (?, ?, ?, ?, ?)",
            (session_id, batch_id, _json_dumps(expressions),
             _json_dumps(results), _now_iso()),
        )
        self.connection.commit()
        return cur.lastrowid
