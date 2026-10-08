# -*- coding: utf-8 -*-
"""enqueue_sweep.py（漏盘兜底：可交付 alpha 补入 submit_ready）守卫测试。

锁定三件事（全部离线 fixture 库）：
  1. 只挑「可交付」：IS 过线 + 最新 backtest ra_failed_checks 空 + 非 add 混腿；
  2. 已在 submit_ready 的不重复入队；平台 ACTIVE / 已提交 / DEAD 的不入；
  3. dry-run 回滚不落盘，commit 落盘且跑列填充审计。
"""
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools", "ledger"))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

import enqueue_sweep as S  # noqa: E402

CORE = ("if_else(greater(mean_estimate_targetprice_annual12_tribes, "
        "median_estimate_targetprice_annual12_tribes), "
        "stddev_estimate_fxadj_targetprice_annual12_tribes, "
        "reverse(stddev_estimate_fxadj_targetprice_annual12_tribes))")


def _make_db(tmp_path, rows):
    db = str(tmp_path / "sweep.db")
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE alphas (
            id INTEGER PRIMARY KEY, alpha_id TEXT, expression TEXT,
            region_id INTEGER, dataset_id INTEGER,
            universe TEXT, delay INTEGER, neutralization TEXT,
            sharpe REAL, fitness REAL, margin REAL, turnover REAL,
            two_year_sharpe REAL, status TEXT,
            prod_correlation REAL, self_correlation REAL,
            alpha_type TEXT, date_submitted TEXT, is_ladder_sharpe REAL,
            soft_deleted INTEGER DEFAULT 0, disposition TEXT,
            platform_status TEXT, sub_universe_sharpe REAL,
            returns REAL, drawdown REAL, long_count INTEGER, short_count INTEGER,
            cluster_test REAL);
        CREATE TABLE backtest_results (
            id INTEGER PRIMARY KEY, alpha_id TEXT, ra_failed_checks TEXT,
            risk_neutralized_sharpe REAL);
    """)
    con.execute("INSERT INTO regions VALUES (1, 'USA')")
    for i, r in enumerate(rows, 1):
        con.execute(
            "INSERT INTO alphas (id, alpha_id, expression, region_id, universe, delay,"
            " neutralization, sharpe, fitness, margin, turnover, two_year_sharpe, status,"
            " prod_correlation, self_correlation, sub_universe_sharpe, returns,"
            " long_count, short_count) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, r["alpha_id"], f"group_rank({CORE}, subindustry)", 1,
             "TOP3000", 1, "STATISTICAL", r.get("sharpe", 2.0), r.get("fitness", 1.2),
             0.002, r.get("turnover", 0.05), r.get("two_year", 1.8),
             r.get("status", "UNSUBMITTED"), r.get("prod"), r.get("self"),
             0.9, 0.04, 1600, 1400))
        if r.get("ra_fails") is not None:
            import json
            con.execute(
                "INSERT INTO backtest_results (alpha_id, ra_failed_checks) VALUES (?, ?)",
                (r["alpha_id"], json.dumps(r["ra_fails"])))
    con.commit()
    con.close()
    return db


def test_sweep_picks_only_deliverables(tmp_path):
    db = _make_db(tmp_path, [
        {"alpha_id": "good0001"},                                   # 可交付
        {"alpha_id": "rafail1", "ra_fails": ["LOW_SUB_UNIVERSE_SHARPE"]},  # RA 挂
        {"alpha_id": "lowshp1", "sharpe": 0.5},                      # IS 不过线
        {"alpha_id": "active1", "status": "UNSUBMITTED",
         "prod": 0.5, "self": 0.4},                                 # 可交付（会入）
        {"alpha_id": "done001", "status": "COMPLETE"},               # 可交付
        {"alpha_id": "subm001", "status": "UNSUBMITTED",
         "two_year": 1.9},                                          # 可交付
    ])
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    recs = S.find_deliverables(con, region="USA")
    got = sorted(r["alpha_id"] for r in recs)
    con.close()
    assert got == ["active1", "done001", "good0001", "subm001"]


def test_sweep_skips_already_queued(tmp_path):
    db = _make_db(tmp_path, [{"alpha_id": "good0001"}, {"alpha_id": "good0002"}])
    from wqb.store import submit_queue as sq
    con = sq.connect(db)
    sq.ensure_table(con)
    sq.enqueue(con, {"alpha_id": "good0001", "region": "USA", "sharpe": 2.0,
                     "fitness": 1.2, "expr": f"group_rank({CORE}, subindustry)"})
    con.commit()
    con.row_factory = sqlite3.Row
    recs = S.find_deliverables(con, region="USA")
    con.close()
    assert [r["alpha_id"] for r in recs] == ["good0002"]


def test_sweep_commit_and_dry_run(tmp_path):
    db = _make_db(tmp_path, [{"alpha_id": "good0001"}])
    assert S.run(region="USA", db_path=db, dry_run=True) == 0
    con = sqlite3.connect(db)
    assert con.execute("SELECT COUNT(*) FROM submit_ready").fetchone()[0] == 0
    con.close()
    assert S.run(region="USA", db_path=db) == 0
    con = sqlite3.connect(db)
    row = con.execute("SELECT alpha_id, status, family FROM submit_ready").fetchone()
    con.close()
    assert row[0] == "good0001" and row[1] == "READY" and row[2]   # family 派生已填
