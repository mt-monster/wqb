# -*- coding: utf-8 -*-
"""submit_ready 体检卡三层列（2026-10-06）。

背景：体检卡（tools/verdict/candidate_health_card.py）暴露出 `submit_ready` 表缺 margin /
returns / drawdown / long·short_count / 约束变体 sharpe 共 7 列 —— 直连候选（只登记在
submit_ready、不在 alphas 的那些）的这些指标全库不可见，每次体检只能绕过 DB 打平台 GET。

本测试守住三件事（否则 schema 源头改错了不会红）：
  1. 新建库（fresh）经 ensure_table 即带这 7 列；
  2. **老库**（无这 7 列）经 ensure_table 自动 ALTER 补齐（迁移自愈），且旧数据不动；
  3. `_upsert` 往返：新列能写入，且**二次入队带 None 不覆盖已有值**（COALESCE 保序）。
"""
import sqlite3

NEW_COLS = ("margin", "returns", "drawdown", "long_count", "short_count",
            "investability_constrained_sharpe", "risk_neutralized_sharpe")

#: 2026-10-06 之前的 submit_ready DDL（不含新 7 列），用于模拟老库。
_OLD_DDL = """
CREATE TABLE submit_ready (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    alpha_id       TEXT    NOT NULL,
    region         TEXT    NOT NULL,
    universe       TEXT,
    delay          INTEGER,
    decay          INTEGER,
    neutralization TEXT,
    expr           TEXT,
    skeleton       TEXT,
    suggested_tags TEXT,
    sharpe         REAL,
    fitness        REAL,
    turnover       REAL,
    two_year       REAL,
    sub_universe   REAL,
    cluster_test   REAL,
    prod           REAL,
    self           REAL,
    gate           TEXT    DEFAULT 'UNVERIFIED',
    verified_at    TEXT,
    verified_by    TEXT,
    towers         TEXT,
    family         TEXT,
    status         TEXT    DEFAULT 'READY',
    added_at       TEXT,
    note           TEXT,
    UNIQUE(alpha_id, region)
);
"""


def _cols(con, table="submit_ready"):
    return {r[1] for r in con.execute(f"PRAGMA table_info({table})")}


def test_ensure_table_adds_health_cols_on_fresh_db():
    from wqb.store import submit_queue as sq
    con = sqlite3.connect(":memory:")
    try:
        sq.ensure_table(con)
        missing = [c for c in NEW_COLS if c not in _cols(con)]
        assert not missing, f"fresh 库缺体检卡列: {missing}"
    finally:
        con.close()


def test_migrate_backfills_health_cols_on_legacy_db():
    """老库（无新列）经 ensure_table 自动补齐，且旧行数据无损。"""
    from wqb.store import submit_queue as sq
    con = sqlite3.connect(":memory:")
    try:
        con.executescript(_OLD_DDL)
        con.execute("INSERT INTO submit_ready (alpha_id, region, status, sharpe) "
                    "VALUES ('x','GBR','READY',1.7)")
        con.commit()
        assert not (set(NEW_COLS) & _cols(con)), "前置失败：老库不应已有新列"

        sq.ensure_table(con)

        missing = [c for c in NEW_COLS if c not in _cols(con)]
        assert not missing, f"老库迁移后仍缺列: {missing}"
        row = con.execute(
            "SELECT alpha_id, status, sharpe, margin, risk_neutralized_sharpe "
            "FROM submit_ready").fetchone()
        assert row[0] == "x" and row[1] == "READY" and row[2] == 1.7
        assert row[3] is None and row[4] is None, "新列应为 NULL（不影响既有数据）"
    finally:
        con.close()


def test_upsert_roundtrips_health_cols_and_preserves_on_none():
    """新列可写入；二次入队带 None 不抹掉已有值（ON CONFLICT COALESCE 保序）。"""
    from wqb.store import submit_queue as sq
    con = sqlite3.connect(":memory:")
    try:
        sq.ensure_table(con)
        rec = {"alpha_id": "aaaa1111", "region": "GBR", "sharpe": 1.9, "fitness": 1.1,
               "turnover": 0.1, "two_year": 2.0, "sub_universe": 0.9,
               "margin": 0.00072, "returns": 0.046, "drawdown": 0.026,
               "long_count": 453, "short_count": 456,
               "investability_constrained_sharpe": 1.10}
        sq.enqueue(con, rec)
        r = con.execute(
            "SELECT margin, returns, drawdown, long_count, short_count, "
            "investability_constrained_sharpe FROM submit_ready WHERE alpha_id='aaaa1111'"
        ).fetchone()
        assert abs(r[0] - 0.00072) < 1e-9
        assert abs(r[1] - 0.046) < 1e-9 and r[3] == 453 and r[4] == 456
        assert abs(r[5] - 1.10) < 1e-9

        # 二次入队：margin=None（未测），不得覆盖既有 0.00072
        rec2 = {"alpha_id": "aaaa1111", "region": "GBR", "sharpe": 2.0, "fitness": 1.2,
                "turnover": 0.1, "two_year": 2.1, "sub_universe": 0.9, "margin": None}
        sq.enqueue(con, rec2)
        r2 = con.execute(
            "SELECT margin, long_count FROM submit_ready WHERE alpha_id='aaaa1111'"
        ).fetchone()
        assert abs(r2[0] - 0.00072) < 1e-9, "None 覆盖了已有 margin（COALESCE 失效）"
        assert r2[1] == 453, "None 覆盖了已有 long_count"
    finally:
        con.close()
