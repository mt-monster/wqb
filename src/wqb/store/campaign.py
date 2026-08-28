# -*- coding: utf-8 -*-
"""CampaignStore: denormalized campaign writes on data/wqb.db.

Existing tables (expressions/fields/waves/datasets/regions/…) keep their
FK layout. This module adds region/wave/dataset columns where missing and
a gate_results table, then upserts by (region, wave, expression).
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

ExprItem = Union[str, Dict[str, Any]]

_DEFAULT_REL = Path("data") / "wqb.db"


def default_db_path(workspace_root: Optional[str] = None) -> str:
    env = os.environ.get("WQB_DB_PATH")
    if env:
        return env
    if workspace_root:
        return str(Path(workspace_root) / _DEFAULT_REL)
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / _DEFAULT_REL
        if cand.exists() or (parent / "src" / "wqb").is_dir():
            return str(parent / _DEFAULT_REL)
    return str(Path.cwd() / _DEFAULT_REL)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _loads(raw: Any) -> Any:
    if raw is None:
        return None
    if isinstance(raw, (dict, list)):
        return raw
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw


def _as_expr(item: ExprItem) -> Dict[str, Any]:
    if isinstance(item, str):
        return {"expression": item}
    expr = item.get("expression") or item.get("expr") or item.get("code") or item.get("regular") or ""
    out = dict(item)
    out["expression"] = expr
    return out


class CampaignStore:
    """SQLite campaign artifact store."""

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

    # -- schema ------------------------------------------------------------

    def _columns(self, table: str) -> set:
        cur = self.connection.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        return {row[1] for row in cur.fetchall()}

    def _add_column(self, table: str, name: str, ddl: str) -> None:
        cols = self._columns(table)
        if name not in cols:
            self.connection.execute(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}")

    def ensure_schema(self) -> None:
        cur = self.connection.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL UNIQUE,
                universe_legal JSON,
                delay_legal JSON,
                neutralization_default VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                region_id INTEGER NOT NULL,
                category VARCHAR(50),
                field_count INTEGER,
                coverage DECIMAL(5,4),
                alpha_count INTEGER,
                value_score DECIMAL(3,1),
                pyramid_multiplier DECIMAL(3,1),
                tier VARCHAR(10),
                status VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, region_id),
                FOREIGN KEY (region_id) REFERENCES regions(id)
            );
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER NOT NULL,
                field_name VARCHAR(200) NOT NULL,
                field_type VARCHAR(20),
                coverage DECIMAL(5,4),
                user_count INTEGER,
                alpha_count INTEGER,
                description TEXT,
                field_group VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(dataset_id, field_name),
                FOREIGN KEY (dataset_id) REFERENCES datasets(id)
            );
            CREATE TABLE IF NOT EXISTS waves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region_id INTEGER NOT NULL,
                wave_number VARCHAR(20) NOT NULL,
                dataset_id INTEGER,
                expression_count INTEGER DEFAULT 0,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_id, wave_number),
                FOREIGN KEY (region_id) REFERENCES regions(id),
                FOREIGN KEY (dataset_id) REFERENCES datasets(id)
            );
            CREATE TABLE IF NOT EXISTS expressions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wave_id INTEGER NOT NULL,
                expression TEXT NOT NULL,
                fingerprint VARCHAR(100),
                status VARCHAR(20) DEFAULT 'pending',
                alpha_id VARCHAR(50),
                sharpe DECIMAL(8,4),
                fitness DECIMAL(8,4),
                margin DECIMAL(10,6),
                turnover DECIMAL(8,4),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(wave_id, expression),
                FOREIGN KEY (wave_id) REFERENCES waves(id)
            );
            CREATE TABLE IF NOT EXISTS backtest_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression_id INTEGER NOT NULL,
                alpha_id VARCHAR(50),
                status VARCHAR(20),
                sharpe DECIMAL(8,4),
                fitness DECIMAL(8,4),
                turnover DECIMAL(8,4),
                margin DECIMAL(10,6),
                returns DECIMAL(8,4),
                drawdown DECIMAL(8,4),
                two_year_sharpe DECIMAL(8,4),
                sub_universe_sharpe DECIMAL(8,4),
                long_count INTEGER,
                short_count INTEGER,
                pnl BIGINT,
                book_size BIGINT,
                concentrated_weight DECIMAL(8,4),
                ra_failed_count INTEGER,
                ra_failed_checks JSON,
                ppa_failed_count INTEGER,
                ppa_failed_checks JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (expression_id) REFERENCES expressions(id)
            );
            CREATE TABLE IF NOT EXISTS diversity_potential (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region_id INTEGER NOT NULL,
                dataset_id INTEGER NOT NULL,
                diversity_score DECIMAL(5,4),
                recommended_rounds INTEGER,
                field_categories JSON,
                operator_buckets JSON,
                parameter_space JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_id, dataset_id),
                FOREIGN KEY (region_id) REFERENCES regions(id),
                FOREIGN KEY (dataset_id) REFERENCES datasets(id)
            );
            CREATE TABLE IF NOT EXISTS ledger_kv (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                key VARCHAR(200) NOT NULL,
                value JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region, key)
            );
            CREATE TABLE IF NOT EXISTS gate_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region TEXT NOT NULL,
                wave TEXT NOT NULL,
                dataset TEXT NOT NULL,
                all_pass INTEGER,
                report_json TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT,
                UNIQUE(region, wave, dataset)
            );
            CREATE TABLE IF NOT EXISTS workflow_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_key VARCHAR(200) NOT NULL UNIQUE,
                config_value JSON NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS submission_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alpha_id VARCHAR(50) NOT NULL,
                region VARCHAR(50),
                submission_type VARCHAR(20),
                status VARCHAR(20),
                quota_used INTEGER DEFAULT 0,
                quota_remaining INTEGER,
                verdict JSON,
                submitted_at TIMESTAMP,
                verified_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(alpha_id, submitted_at)
            );
            CREATE TABLE IF NOT EXISTS alphas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alpha_id VARCHAR(50) NOT NULL UNIQUE,
                expression TEXT NOT NULL,
                region_id INTEGER NOT NULL,
                dataset_id INTEGER NOT NULL,
                universe VARCHAR(20),
                delay INTEGER,
                neutralization VARCHAR(50),
                sharpe DECIMAL(8,4),
                fitness DECIMAL(8,4),
                margin DECIMAL(10,6),
                turnover DECIMAL(8,4),
                two_year_sharpe DECIMAL(8,4),
                status VARCHAR(20) DEFAULT 'UNSUBMITTED',
                prod_correlation DECIMAL(5,4),
                self_correlation DECIMAL(5,4),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (region_id) REFERENCES regions(id),
                FOREIGN KEY (dataset_id) REFERENCES datasets(id)
            );

            CREATE TABLE IF NOT EXISTS wave_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                wave_number TEXT NOT NULL,
                focus TEXT,
                context TEXT,
                key_findings JSON,
                candidates JSON,
                batches JSON,
                verdict TEXT,
                status VARCHAR(20),
                source_file VARCHAR(200),
                archived INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                full_payload JSON,
                UNIQUE(region, wave_number)
            );
            CREATE TABLE IF NOT EXISTS registry_empirical (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                layer VARCHAR(20) NOT NULL,
                entry_id VARCHAR(100),
                family VARCHAR(200),
                payload JSON NOT NULL,
                dead_at VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region, layer, entry_id)
            );
            CREATE TABLE IF NOT EXISTS cross_region_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id VARCHAR(100) NOT NULL UNIQUE,
                family VARCHAR(200),
                finding TEXT,
                rule TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS campaign_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region_id INTEGER NOT NULL,
                current_wave VARCHAR(20),
                submit_ready_count INTEGER DEFAULT 0,
                target_count INTEGER DEFAULT 10,
                status VARCHAR(20) DEFAULT 'active',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_id),
                FOREIGN KEY (region_id) REFERENCES regions(id)
            );
            """
        )
        for col, ddl in (
            ("region", "TEXT"),
            ("wave", "TEXT"),
            ("dataset", "TEXT"),
            ("settings_json", "TEXT"),
        ):
            self._add_column("expressions", col, ddl)
        for col, ddl in (
            ("region", "TEXT"),
            ("wave", "TEXT"),
            ("dataset", "TEXT"),
            ("code", "TEXT"),
            ("payload_json", "TEXT"),
        ):
            self._add_column("backtest_results", col, ddl)
        self._add_column("datasets", "data_type", "TEXT")
        self._add_column("datasets", "catalog_json", "TEXT")
        self._add_column("diversity_potential", "payload_json", "TEXT")
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_expr_region_wave "
            "ON expressions(region, wave)"
        )
        self.connection.commit()

    # -- helpers -----------------------------------------------------------

    def _ensure_region(self, name: str) -> int:
        cur = self.connection.cursor()
        cur.execute("SELECT id FROM regions WHERE name=?", (name,))
        row = cur.fetchone()
        if row:
            return int(row[0])
        cur.execute(
            "INSERT INTO regions (name, created_at, updated_at) VALUES (?,?,?)",
            (name, _now(), _now()),
        )
        self.connection.commit()
        return int(cur.lastrowid)

    def _ensure_dataset(self, region: str, name: str, extra: Optional[Dict] = None) -> int:
        rid = self._ensure_region(region)
        extra = extra or {}
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id FROM datasets WHERE name=? AND region_id=?",
            (name, rid),
        )
        row = cur.fetchone()
        now = _now()
        if row:
            did = int(row[0])
            sets = []
            args: List[Any] = []
            for k in ("category", "field_count", "coverage", "alpha_count",
                      "tier", "status", "data_type", "catalog_json"):
                if k in extra and extra[k] is not None:
                    sets.append(f"{k}=?")
                    args.append(extra[k])
            if sets:
                args.extend([now, did])
                cur.execute(
                    f"UPDATE datasets SET {', '.join(sets)}, updated_at=? WHERE id=?",
                    args,
                )
                self.connection.commit()
            return did
        cur.execute(
            """INSERT INTO datasets
               (name, region_id, category, field_count, coverage, alpha_count,
                tier, status, data_type, catalog_json, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                name, rid,
                extra.get("category"),
                extra.get("field_count"),
                extra.get("coverage"),
                extra.get("alpha_count"),
                extra.get("tier"),
                extra.get("status"),
                extra.get("data_type"),
                extra.get("catalog_json"),
                now, now,
            ),
        )
        self.connection.commit()
        return int(cur.lastrowid)

    def _ensure_wave(self, region: str, wave: str, dataset: Optional[str] = None) -> int:
        rid = self._ensure_region(region)
        ds_id = self._ensure_dataset(region, dataset) if dataset else None
        cur = self.connection.cursor()
        cur.execute(
            "SELECT id FROM waves WHERE region_id=? AND wave_number=?",
            (rid, str(wave)),
        )
        row = cur.fetchone()
        now = _now()
        if row:
            wid = int(row[0])
            if ds_id is not None:
                cur.execute(
                    "UPDATE waves SET dataset_id=?, updated_at=? WHERE id=?",
                    (ds_id, now, wid),
                )
                self.connection.commit()
            return wid
        cur.execute(
            """INSERT INTO waves
               (region_id, wave_number, dataset_id, status, created_at, updated_at)
               VALUES (?,?,?,?,?,?)""",
            (rid, str(wave), ds_id, "pending", now, now),
        )
        self.connection.commit()
        return int(cur.lastrowid)

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

    # -- submission_ledger --------------------------------------------------

    def upsert_submission(self, alpha_id: str, region: Optional[str] = None,
                          submission_type: str = "REGULAR", status: str = "PENDING",
                          quota_used: int = 0, quota_remaining: Optional[int] = None,
                          verdict: Optional[Dict] = None, submitted_at: Optional[str] = None,
                          verified_at: Optional[str] = None) -> Dict[str, Any]:
        """Upsert submission record."""
        cur = self.connection.cursor()
        now = _now()
        submitted_at = submitted_at or now
        verdict_json = _dumps(verdict) if verdict else None

        cur.execute(
            "SELECT id FROM submission_ledger WHERE alpha_id=? AND submitted_at=?",
            (alpha_id, submitted_at),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                """UPDATE submission_ledger SET region=?, submission_type=?, status=?,
                   quota_used=?, quota_remaining=?, verdict=?, verified_at=?, updated_at=?
                   WHERE alpha_id=? AND submitted_at=?""",
                (region, submission_type, status, quota_used, quota_remaining,
                 verdict_json, verified_at, now, alpha_id, submitted_at),
            )
            action = "updated"
        else:
            cur.execute(
                """INSERT INTO submission_ledger
                   (alpha_id, region, submission_type, status, quota_used, quota_remaining,
                    verdict, submitted_at, verified_at, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (alpha_id, region, submission_type, status, quota_used, quota_remaining,
                 verdict_json, submitted_at, verified_at, now, now),
            )
            action = "inserted"
        self.connection.commit()
        return {"action": action, "alpha_id": alpha_id, "submitted_at": submitted_at}

    def get_submission(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """Get latest submission record for alpha."""
        cur = self.connection.cursor()
        cur.execute(
            """SELECT * FROM submission_ledger WHERE alpha_id=?
               ORDER BY submitted_at DESC LIMIT 1""",
            (alpha_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return dict(row)

    def list_submissions(self, region: Optional[str] = None, status: Optional[str] = None,
                         limit: int = 100) -> List[Dict[str, Any]]:
        """List submission records."""
        cur = self.connection.cursor()
        sql = "SELECT * FROM submission_ledger WHERE 1=1"
        params: List[Any] = []
        if region:
            sql += " AND region=?"
            params.append(region)
        if status:
            sql += " AND status=?"
            params.append(status)
        sql += " ORDER BY submitted_at DESC LIMIT ?"
        params.append(limit)
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def get_quota_status(self, region: Optional[str] = None, window_hours: int = 48) -> Dict[str, Any]:
        """Get submission quota status for the rolling window."""
        cur = self.connection.cursor()
        # 计算窗口内的提交数
        cutoff = datetime.now().timestamp() - (window_hours * 3600)
        cutoff_str = datetime.fromtimestamp(cutoff).isoformat()

        sql = """SELECT COUNT(*) as used FROM submission_ledger
                 WHERE submitted_at > ? AND status IN ('SUBMITTED', 'ACTIVE')"""
        params: List[Any] = [cutoff_str]
        if region:
            sql += " AND region=?"
            params.append(region)

        cur.execute(sql, params)
        used = cur.fetchone()[0]

        # 默认配额限制（可从 platform_constraints.json 读取）
        quota_limit = 4  # 48h 滚动配额

        return {
            "used": used,
            "limit": quota_limit,
            "remaining": max(0, quota_limit - used),
            "window_hours": window_hours,
            "region": region,
        }

    # -- expressions -------------------------------------------------------

    def upsert_expressions(
        self,
        region: str,
        wave: str,
        items: Sequence[ExprItem],
        dataset: Optional[str] = None,
        status: str = "pending",
    ) -> Dict[str, Any]:
        wave_id = self._ensure_wave(region, str(wave), dataset)
        now = _now()
        n = 0
        cur = self.connection.cursor()
        # 冗余列 region/wave/dataset 必须从 wave_id 关联派生，避免与父表（waves→regions/datasets）漂移
        cur.execute(
            "SELECT r.name, w.wave_number, d.name FROM waves w "
            "JOIN regions r ON r.id=w.region_id "
            "LEFT JOIN datasets d ON d.id=w.dataset_id WHERE w.id=?",
            (wave_id,),
        )
        _wr = cur.fetchone()
        resolved_region = _wr["name"] if _wr else region
        resolved_wave = str(_wr["wave_number"]) if _wr else str(wave)
        resolved_dataset = _wr["name"] if _wr and _wr["name"] else (dataset or None)
        for raw in items:
            item = _as_expr(raw)
            expr = (item.get("expression") or "").strip()
            if not expr:
                continue
            st = item.get("status") or status
            settings = item.get("settings") or item.get("settings_json")
            settings_json = _dumps(settings) if isinstance(settings, (dict, list)) else settings
            cur.execute(
                "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                (wave_id, expr),
            )
            row = cur.fetchone()
            vals = (
                item.get("fingerprint"),
                st,
                item.get("alpha_id"),
                item.get("sharpe"),
                item.get("fitness"),
                item.get("margin"),
                item.get("turnover"),
                resolved_region,
                resolved_wave,
                resolved_dataset,
                settings_json,
                now,
            )
            if row:
                cur.execute(
                    """UPDATE expressions SET fingerprint=?, status=?, alpha_id=?,
                       sharpe=?, fitness=?, margin=?, turnover=?, region=?, wave=?,
                       dataset=?, settings_json=?, updated_at=? WHERE id=?""",
                    vals + (int(row[0]),),
                )
            else:
                cur.execute(
                    """INSERT INTO expressions
                       (wave_id, expression, fingerprint, status, alpha_id, sharpe,
                        fitness, margin, turnover, region, wave, dataset,
                        settings_json, created_at, updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (wave_id, expr) + vals + (now,),
                )
            n += 1
        cur.execute(
            "UPDATE waves SET expression_count=?, updated_at=? WHERE id=?",
            (n, now, wave_id),
        )
        self.connection.commit()
        return {"n": n, "region": region, "wave": str(wave), "dataset": dataset}

    def list_expressions(
        self,
        region: str,
        wave: str,
        dataset: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM expressions WHERE region=? AND wave=?"
        params: List[Any] = [region, str(wave)]
        if dataset:
            sql += " AND (dataset=? OR dataset IS NULL)"
            params.append(dataset)
        if status:
            sql += " AND status=?"
            params.append(status)
        sql += " ORDER BY id"
        cur = self.connection.cursor()
        cur.execute(sql, params)
        out = []
        for row in cur.fetchall():
            d = dict(row)
            if d.get("settings_json"):
                d["settings"] = _loads(d["settings_json"])
            out.append(d)
        if out:
            return out
        # fallback: old rows without denormalized region/wave
        rid = None
        cur.execute("SELECT id FROM regions WHERE name=?", (region,))
        r = cur.fetchone()
        if not r:
            return []
        rid = int(r[0])
        cur.execute(
            "SELECT id FROM waves WHERE region_id=? AND wave_number=?",
            (rid, str(wave)),
        )
        w = cur.fetchone()
        if not w:
            return []
        cur.execute(
            "SELECT * FROM expressions WHERE wave_id=? ORDER BY id",
            (int(w[0]),),
        )
        return [dict(row) for row in cur.fetchall()]

    def history_expressions(self, region: str, exclude_waves: Optional[Sequence[str]] = None) -> List[str]:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT expression, wave, status FROM expressions WHERE region=?",
            (region,),
        )
        skip = {str(w) for w in (exclude_waves or [])}
        skip_status = {"gem", "raw"}
        out = []
        for r in cur.fetchall():
            if r[1] and str(r[1]) in skip:
                continue
            if (r[2] or "") in skip_status:
                continue
            if r[0]:
                out.append(r[0])
        return out

    save_wave_expressions = upsert_expressions
    load_wave_expressions = list_expressions

    # -- field catalog -----------------------------------------------------

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

    # -- gate --------------------------------------------------------------

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

    # -- backtest ----------------------------------------------------------

    def upsert_backtest_rows(
        self, region: str, wave: str, rows: Sequence[Dict[str, Any]],
        dataset: Optional[str] = None,
    ) -> int:
        wave_id = self._ensure_wave(region, str(wave), dataset)
        n = 0
        cur = self.connection.cursor()
        now = _now()
        rid = self._ensure_region(region)
        ds_id = self._ensure_dataset(region, dataset or "_unknown")
        for r in rows:
            code = r.get("code") or r.get("expression") or r.get("expr") or ""
            alpha_id = r.get("id") or r.get("alpha_id")
            expr_id = None
            if code:
                cur.execute(
                    "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                    (wave_id, code),
                )
                erow = cur.fetchone()
                if erow:
                    expr_id = int(erow[0])
                else:
                    self.upsert_expressions(
                        region, str(wave),
                        [{"expression": code, "alpha_id": alpha_id, "status": "backtested"}],
                        dataset=dataset,
                    )
                    cur.execute(
                        "SELECT id FROM expressions WHERE wave_id=? AND expression=?",
                        (wave_id, code),
                    )
                    erow = cur.fetchone()
                    expr_id = int(erow[0]) if erow else None
            if expr_id is None:
                continue
            margin = r.get("margin")
            if margin is None and r.get("margin_bp") is not None:
                margin = r["margin_bp"] / 10000.0
            turnover = r.get("turnover")
            if turnover is None and r.get("turnover_pct") is not None:
                turnover = r["turnover_pct"] / 100.0
            failed = r.get("failed_checks") or r.get("ra_failed_checks") or []
            payload = _dumps(r)
            cur.execute(
                """INSERT INTO backtest_results
                   (expression_id, alpha_id, status, sharpe, fitness, turnover,
                    margin, two_year_sharpe, sub_universe_sharpe, ra_failed_checks,
                    region, wave, dataset, code, payload_json, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    expr_id, alpha_id, r.get("status") or "COMPLETE",
                    r.get("sharpe"), r.get("fitness"), turnover, margin,
                    r.get("two_year_sharpe"), r.get("sub_universe_sharpe"),
                    _dumps(failed) if failed else None,
                    region, str(wave), dataset, code, payload, now,
                ),
            )
            if alpha_id:
                cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (alpha_id,))
                arow = cur.fetchone()
                aval = (
                    code or "",
                    rid, ds_id,
                    r.get("universe"), r.get("delay"),
                    r.get("neut") or r.get("neutralization"),
                    r.get("sharpe"), r.get("fitness"), margin, turnover,
                    r.get("two_year_sharpe"),
                    r.get("status") or "UNSUBMITTED",
                    r.get("prod_corr") or r.get("prod_correlation"),
                    r.get("self_corr") or r.get("self_correlation"),
                    now,
                )
                if arow:
                    cur.execute(
                        """UPDATE alphas SET expression=?, region_id=?, dataset_id=?,
                           universe=?, delay=?, neutralization=?, sharpe=?, fitness=?,
                           margin=?, turnover=?, two_year_sharpe=?, status=?,
                           prod_correlation=?, self_correlation=?, updated_at=?
                           WHERE id=?""",
                        aval + (int(arow[0]),),
                    )
                else:
                    cur.execute(
                        """INSERT INTO alphas
                           (alpha_id, expression, region_id, dataset_id, universe,
                            delay, neutralization, sharpe, fitness, margin, turnover,
                            two_year_sharpe, status, prod_correlation, self_correlation,
                            created_at, updated_at)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (alpha_id,) + aval + (now,),
                    )
            n += 1
        self.connection.commit()
        return n

    save_backtest_results = upsert_backtest_rows

    def list_backtest_rows(self, region: str, wave: str) -> List[Dict[str, Any]]:
        cur = self.connection.cursor()
        cur.execute(
            "SELECT * FROM backtest_results WHERE region=? AND wave=? ORDER BY id",
            (region, str(wave)),
        )
        out = []
        for row in cur.fetchall():
            d = dict(row)
            if d.get("payload_json"):
                d["payload"] = _loads(d["payload_json"])
            out.append(d)
        return out

    # -- diversity / ranking / checkpoint / rules --------------------------

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

    # -- alphas -----------------------------------------------------------

    def get_alpha_by_id(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """根据 alpha_id 查询 alpha 详情（含 region 名）。"""
        cur = self.connection.cursor()
        cur.execute(
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE a.alpha_id=?",
            (alpha_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def list_alphas_by_region(self, region: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出某 region 的全部 alpha（可选 status 过滤）。"""
        cur = self.connection.cursor()
        sql = (
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE r.name=?"
        )
        params: List[Any] = [region]
        if status:
            sql += " AND a.status=?"
            params.append(status)
        sql += " ORDER BY a.updated_at DESC"
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def search_alphas_by_sharpe(
        self,
        region: Optional[str] = None,
        min_sharpe: float = 1.0,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """按 sharpe 搜索 alpha（sharpe >= min_sharpe）。"""
        cur = self.connection.cursor()
        sql = (
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE a.sharpe >= ?"
        )
        params: List[Any] = [min_sharpe]
        if region:
            sql += " AND r.name=?"
            params.append(region)
        sql += " ORDER BY a.sharpe DESC LIMIT ?"
        params.append(limit)
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]


def get_database_integration(workspace_root: Optional[str] = None) -> CampaignStore:
    """Compatibility alias for pipeline / inspect / diversity_extract."""
    return CampaignStore.from_workspace(workspace_root)
