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
                -- completed_at 已废弃（从未回写），不再创建
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
                ra_failed_checks JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (expression_id) REFERENCES expressions(id)
            );
            -- diversity_potential 已废弃（数据统一存入 ledger_kv），不再创建
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
            -- workflow_configs 已废弃（0 行，功能被 ledger_kv 替代），不再创建
            CREATE TABLE IF NOT EXISTS submission_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alpha_id VARCHAR(50) NOT NULL,
                region VARCHAR(50),
                submission_type VARCHAR(20),
                status VARCHAR(20),
                quota_used INTEGER DEFAULT 0,
                -- quota_remaining 已废弃（从未写入），不再创建
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
            -- cross_region_lessons 已废弃（数据迁移至 registry_empirical layer='cross_region'），不再创建
            CREATE TABLE IF NOT EXISTS field_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER NOT NULL,
                field_name VARCHAR(200) NOT NULL,
                shape VARCHAR(30),
                coverage DECIMAL(5,4),
                skew DECIMAL(8,3),
                kurt DECIMAL(8,3),
                integer INTEGER DEFAULT 0,
                freq VARCHAR(20),
                pos_ratio DECIMAL(5,4),
                neg_ratio DECIMAL(5,4),
                near_zero_ratio DECIMAL(5,4),
                source VARCHAR(40),
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(dataset_id, field_name),
                FOREIGN KEY (dataset_id) REFERENCES datasets(id)
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
        # 索引：覆盖高频查询路径
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_expr_region_wave "
            "ON expressions(region, wave)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_backtest_results_alpha_id "
            "ON backtest_results(alpha_id)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_backtest_results_region_wave "
            "ON backtest_results(region, wave)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_submission_ledger_alpha_id "
            "ON submission_ledger(alpha_id)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_wave_results_region "
            "ON wave_results(region)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_alphas_platform_status "
            "ON alphas(platform_status)"
        )
        self.connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_field_profile_dataset "
            "ON field_profile(dataset_id)"
        )
        # backtest_results 幂等：alpha_id 唯一约束（消除重复 INSERT）
        # 注意：SQLite ON CONFLICT 需要非 partial UNIQUE INDEX
        self.connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_backtest_results_alpha_unique "
            "ON backtest_results(alpha_id)"
        )
        # 2026-09-07 P0-3：wave 键一致性校验（WARN 不阻断）。
        # 根因：gate_results.wave 与 waves.wave_number 同为 TEXT，但历史写入方
        # 混用 int 波号与 's2_xxx_d1' 字符串波号；tools/wave_gate.py 曾用
        # type=int 只接受整数波号，字符串波号的波无法进门禁 → gate_rows=0
        # 静默断链（ws2_* 波 6100 条积压的直接根因）。
        # 此校验在 ensure_schema 尾部执行：发现"有表达式但 gate_results 无记录"
        # 的活跃波即打 WARN，让断链在启动时可见。
        try:
            cur = self.connection.cursor()
            cur.execute(
                """
                SELECT w.wave_number, r.name, COUNT(e.id) AS ec
                FROM waves w
                JOIN regions r ON r.id = w.region_id
                LEFT JOIN expressions e ON e.wave_id = w.id
                LEFT JOIN gate_results g
                       ON g.region = r.name AND g.wave = w.wave_number
                WHERE w.status IN ('pending', 'gated')
                  AND g.id IS NULL
                GROUP BY w.id
                HAVING ec > 0
                ORDER BY ec DESC
                LIMIT 5
                """
            )
            orphans = cur.fetchall()
            if orphans:
                total_cur = self.connection.cursor()
                total_cur.execute(
                    """
                    SELECT COUNT(*), COALESCE(SUM(ec), 0) FROM (
                        SELECT w.id, COUNT(e.id) AS ec
                        FROM waves w
                        LEFT JOIN expressions e ON e.wave_id = w.id
                        LEFT JOIN gate_results g
                               ON g.region = (SELECT name FROM regions WHERE id = w.region_id)
                              AND g.wave = w.wave_number
                        WHERE w.status IN ('pending', 'gated') AND g.id IS NULL
                        GROUP BY w.id HAVING ec > 0
                    )
                    """
                )
                tot = total_cur.fetchone()
                names = ", ".join(f"{r[1]}/{r[0]}({r[2]}条)" for r in orphans)
                print(
                    f"[wave-key-check] WARN: {tot[0]} 个活跃波（{tot[1]} 条表达式）"
                    f"无 gate_results 记录（门禁断链或未执行）。Top: {names}。"
                    f"修复入口: tools/wave_gate.py --wave <wave_number>（已支持字符串波号）"
                )
        except Exception as exc:  # pragma: no cover - 校验自身不阻断启动
            print(f"[wave-key-check] 校验异常（忽略）: {exc}")
        # 2026-09-07 P2-1：波次 TTL 回收检查（WARN 不阻断）。
        # pending/gated 波超 7 天无更新即视为 stale —— 历史教训：08-25 生成的
        # ws2_* 波因无 TTL 兜底无声积压 6100 条表达式，污染 pending 池统计。
        # stale 波不自动改状态（数据主权在人），只打 WARN 提示裁决：
        #   补门禁 tools/wave_gate.py --wave <wave_number> 或人工标 dropped。
        try:
            cur2 = self.connection.cursor()
            cur2.execute(
                """
                SELECT wave_number,
                       (SELECT name FROM regions WHERE id = region_id) AS region,
                       expression_count,
                       updated_at
                FROM waves
                WHERE status IN ('pending', 'gated')
                  AND updated_at < datetime('now', '-7 days')
                ORDER BY updated_at
                LIMIT 5
                """
            )
            stale = cur2.fetchall()
            if stale:
                cur3 = self.connection.cursor()
                cur3.execute(
                    """
                    SELECT COUNT(*), COALESCE(SUM(expression_count), 0)
                    FROM waves
                    WHERE status IN ('pending', 'gated')
                      AND updated_at < datetime('now', '-7 days')
                    """
                )
                tot = cur3.fetchone()
                names = ", ".join(f"{r[1]}/{r[0]}({r[2]}条,{r[3][:10]})" for r in stale)
                print(
                    f"[wave-ttl-check] WARN: {tot[0]} 个 pending/gated 波超 7 天未动"
                    f"（约 {tot[1]} 条表达式积压）。Top: {names}。"
                    f"裁决入口: 补门禁 tools/wave_gate.py --wave <wave_number>，"
                    f"或废弃波标 status='dropped'（勿留死库存）"
                )
        except Exception as exc:  # pragma: no cover
            print(f"[wave-ttl-check] 校验异常（忽略）: {exc}")
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
