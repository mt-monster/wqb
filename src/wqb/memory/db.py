"""Simulation database: hash-based cache and bookkeeping tables.

Implements the simulation cache and trajectory bookkeeping (orchestrator
§10, §11, §12).  Uses SQLite as the backend.

Tables
------
- ``sim_cache`` — hash-deduplicated simulation results.  Before simulating,
  check the cache and reuse exact duplicates.
- ``trajectories`` — high-level search trajectories (one per session/dataset).
- ``trajectory_steps`` — individual steps within a trajectory (generation,
  simulation, repair, etc.).
- ``insights`` — lessons learned (both good and bad) attached to trajectories.
- ``batch_log`` — log of every ``create_multi_simulation`` batch.

Public API
----------
- :class:`SimulationDB` — the main database handle.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _json_dumps(obj) -> str:
    """Serialise *obj* to a JSON string (handles non-serialisable gracefully)."""
    return json.dumps(obj, ensure_ascii=False, default=str)


def _json_loads(s: str):
    """Deserialise a JSON string, returning ``None`` on failure."""
    if not s:
        return None
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None


# ---------------------------------------------------------------------------
# SimulationDB
# ---------------------------------------------------------------------------


class SimulationDB:
    """SQLite-backed simulation cache and bookkeeping store.

    Parameters
    ----------
    db_path : str
        Path to the SQLite database file.  Default: ``"data/wqb.db"``.

    Examples
    --------
    >>> db = SimulationDB("data/wqb.db")
    >>> db.init_tables()
    >>> h = db.compute_hash("rank(close)", {"region": "USA", "delay": 1})
    >>> db.put_cached(h, "rank(close)", "USA_D1_TOP3000", {"sharpe": 1.5})
    >>> db.get_cached(h)
    {'sharpe': 1.5}
    """

    REQUIRED_TABLES: List[str] = [
        "sim_cache",
        "trajectories",
        "trajectory_steps",
        "insights",
        "batch_log",
    ]

    def __init__(self, db_path: str = "data/wqb.db"):
        self.db_path = db_path
        # Ensure parent directory exists
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        # Connect with row factory for dict-like access
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        # Enable foreign keys
        self._conn.execute("PRAGMA foreign_keys = ON")

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the underlying SQLite connection."""
        return self._conn

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __enter__(self) -> "SimulationDB":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Schema initialisation
    # ------------------------------------------------------------------

    def init_tables(self) -> None:
        """Create all bookkeeping tables if they do not exist.

        Creates five tables:

        - ``sim_cache``: hash (PK), expression, settings_fingerprint,
          result_json, created_at.
        - ``trajectories``: id (PK), session_id, region, universe, dataset,
          paradigm, status, created_at.
        - ``trajectory_steps``: id (PK), trajectory_id (FK), step_type,
          expression, settings, result_json, created_at.
        - ``insights``: id (PK), trajectory_id (FK), insight_type, content,
          created_at.
        - ``batch_log``: id (PK), session_id, batch_id, expressions_json,
          results_json, created_at.
        """
        cur = self._conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sim_cache (
                hash                TEXT PRIMARY KEY,
                expression          TEXT NOT NULL,
                settings_fingerprint TEXT NOT NULL,
                result_json         TEXT NOT NULL,
                created_at          TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS trajectories (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                region     TEXT NOT NULL,
                universe   TEXT NOT NULL,
                dataset    TEXT NOT NULL,
                paradigm   TEXT NOT NULL,
                status     TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS trajectory_steps (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                trajectory_id  INTEGER NOT NULL,
                step_type      TEXT NOT NULL,
                expression     TEXT,
                settings       TEXT,
                result_json    TEXT,
                created_at     TEXT NOT NULL,
                FOREIGN KEY (trajectory_id) REFERENCES trajectories(id)
                    ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                trajectory_id  INTEGER NOT NULL,
                insight_type   TEXT NOT NULL,
                content        TEXT NOT NULL,
                created_at     TEXT NOT NULL,
                FOREIGN KEY (trajectory_id) REFERENCES trajectories(id)
                    ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS batch_log (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id       TEXT NOT NULL,
                batch_id         TEXT NOT NULL,
                expressions_json TEXT NOT NULL,
                results_json     TEXT NOT NULL,
                created_at       TEXT NOT NULL
            )
        """)

        # Indexes for common queries
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_traj_session "
            "ON trajectories(session_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_traj_dataset "
            "ON trajectories(dataset)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_steps_traj "
            "ON trajectory_steps(trajectory_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_insights_traj "
            "ON insights(trajectory_id)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_batch_session "
            "ON batch_log(session_id)"
        )

        self._conn.commit()

    # ------------------------------------------------------------------
    # Simulation cache (hash-based dedup)
    # ------------------------------------------------------------------

    def compute_hash(self, expression: str, settings: dict) -> str:
        """Compute a deterministic simulation hash from expression + settings.

        The hash is a SHA-256 digest of the canonical JSON serialisation of
        ``{"expression": expression, "settings": settings}`` with sorted keys.
        Two simulations with the same expression and settings will produce
        the same hash, enabling deduplication.

        Parameters
        ----------
        expression : str
            Alpha expression string.
        settings : dict
            Simulation settings (region, universe, neutralization, decay,
            delay, etc.).

        Returns
        -------
        str
            Hexadecimal SHA-256 digest.
        """
        canonical = json.dumps(
            {"expression": expression, "settings": settings},
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def get_cached(self, hash_key: str) -> Optional[dict]:
        """Look up a cached simulation result by hash.

        Parameters
        ----------
        hash_key : str
            The simulation hash from :meth:`compute_hash`.

        Returns
        -------
        dict or None
            The cached result dict, or ``None`` if not in cache.
        """
        cur = self._conn.cursor()
        cur.execute(
            "SELECT result_json FROM sim_cache WHERE hash = ?",
            (hash_key,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return _json_loads(row["result_json"])

    def put_cached(
        self,
        hash_key: str,
        expression: str,
        settings_fingerprint: str,
        result: dict,
    ) -> None:
        """Write a simulation result to the cache.

        If the hash already exists, the entry is updated (upsert).

        Parameters
        ----------
        hash_key : str
            The simulation hash from :meth:`compute_hash`.
        expression : str
            Alpha expression string.
        settings_fingerprint : str
            A short string identifying the settings (e.g.
            ``"USA_D1_TOP3000_SUBINDUSTRY"``).
        result : dict
            The simulation result to cache.
        """
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO sim_cache (hash, expression, settings_fingerprint,
                                   result_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(hash) DO UPDATE SET
                expression = excluded.expression,
                settings_fingerprint = excluded.settings_fingerprint,
                result_json = excluded.result_json,
                created_at = excluded.created_at
            """,
            (
                hash_key,
                expression,
                settings_fingerprint,
                _json_dumps(result),
                _now_iso(),
            ),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Trajectory bookkeeping
    # ------------------------------------------------------------------

    def record_trajectory(
        self,
        session_id: str,
        region: str,
        universe: str,
        dataset: str,
        paradigm: str,
    ) -> int:
        """Create a new search trajectory record.

        Parameters
        ----------
        session_id : str
            Unique session identifier.
        region : str
            Region code (e.g. ``"USA"``).
        universe : str
            Trading universe (e.g. ``"TOP3000"``).
        dataset : str
            Dataset ID.
        paradigm : str
            Paradigm name.

        Returns
        -------
        int
            The ``trajectory_id`` (auto-incremented primary key).
        """
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO trajectories
                (session_id, region, universe, dataset, paradigm, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?)
            """,
            (session_id, region, universe, dataset, paradigm, _now_iso()),
        )
        self._conn.commit()
        return cur.lastrowid

    def add_trajectory_step(
        self,
        trajectory_id: int,
        step_type: str,
        expression: str,
        settings: dict,
        result: dict,
    ) -> int:
        """Add a step to an existing trajectory.

        Parameters
        ----------
        trajectory_id : int
            The trajectory ID from :meth:`record_trajectory`.
        step_type : str
            Type of step (e.g. ``"generate"``, ``"simulate"``, ``"repair"``).
        expression : str
            The expression used in this step.
        settings : dict
            Settings used in this step.
        result : dict
            Result of this step.

        Returns
        -------
        int
            The step ID (auto-incremented primary key).
        """
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO trajectory_steps
                (trajectory_id, step_type, expression, settings,
                 result_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                trajectory_id,
                step_type,
                expression,
                _json_dumps(settings),
                _json_dumps(result),
                _now_iso(),
            ),
        )
        self._conn.commit()
        return cur.lastrowid

    def add_insight(
        self,
        trajectory_id: int,
        insight_type: str,
        content: str,
    ) -> int:
        """Record a lesson learned (good or bad) for a trajectory.

        Parameters
        ----------
        trajectory_id : int
            The trajectory ID.
        insight_type : str
            Type of insight (e.g. ``"positive"``, ``"negative"``,
            ``"structural_cause"``).
        content : str
            The insight text.

        Returns
        -------
        int
            The insight ID.
        """
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO insights
                (trajectory_id, insight_type, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (trajectory_id, insight_type, content, _now_iso()),
        )
        self._conn.commit()
        return cur.lastrowid

    def record_batch(
        self,
        session_id: str,
        batch_id: str,
        expressions: list,
        results: list,
    ) -> int:
        """Log a ``create_multi_simulation`` batch.

        Should be called after every batch (orchestrator rule §9: "Update
        ``batch-log.json`` after every ``create_multi_simulation`` batch;
        do not wait until the end of the session.").

        Parameters
        ----------
        session_id : str
            Session identifier.
        batch_id : str
            Unique batch identifier.
        expressions : list
            List of expression strings in the batch.
        results : list
            List of result dicts.

        Returns
        -------
        int
            The batch log entry ID.
        """
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO batch_log
                (session_id, batch_id, expressions_json, results_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                session_id,
                batch_id,
                _json_dumps(expressions),
                _json_dumps(results),
                _now_iso(),
            ),
        )
        self._conn.commit()
        return cur.lastrowid

    # ------------------------------------------------------------------
    # Doctor
    # ------------------------------------------------------------------

    def doctor(self) -> dict:
        """Check all bookkeeping tables and return a health report.

        Returns
        -------
        dict
            ``{"ok": bool, "missing_tables": list[str], "table_counts": dict}``
            where *table_counts* maps table name to row count.
        """
        cur = self._conn.cursor()

        # Check which tables exist
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        existing = {row["name"] for row in cur.fetchall()}

        missing = [t for t in self.REQUIRED_TABLES if t not in existing]

        # Count rows in each existing table
        table_counts: Dict[str, int] = {}
        for table in self.REQUIRED_TABLES:
            if table in existing:
                cur.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
                table_counts[table] = cur.fetchone()["cnt"]
            else:
                table_counts[table] = -1

        return {
            "ok": len(missing) == 0,
            "missing_tables": missing,
            "table_counts": table_counts,
        }
