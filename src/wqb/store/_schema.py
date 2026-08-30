# -*- coding: utf-8 -*-
"""SchemaMixin: table creation and internal helpers for CampaignStore.

These helpers (`_columns`, `_add_column`, `_ensure_region`,
`_ensure_dataset`, `_ensure_wave`) are used by multiple mixins, so they
live in the schema mixin alongside `ensure_schema`.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._common import _now


class SchemaMixin:
    """Schema management and shared region/dataset/wave helpers."""

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
                source VARCHAR(20),          -- 候选来源（gem/manual/probe/diversity/coverage/mode_a/mode_b），
                                             -- 与 status（流水线状态）正交，勿再混入 status
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
                -- 平台侧状态（审计 P0-2 新增）。alphas.status 保留本地语义，
                -- platform_status 存平台 status，二者同名不同义，勿混用。
                platform_status TEXT,
                stage TEXT,               -- IS | OS
                alpha_type TEXT,          -- REGULAR | SUPER
                date_submitted TIMESTAMP,
                -- IS_LADDER_SHARPE 提交硬闸（2026-08-29 新增）：年度阶梯稳健性，
                -- 平台 checks 已算好，harvest 时回写；可预判"能否过闸"。
                is_ladder_sharpe DECIMAL(8,4),
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
