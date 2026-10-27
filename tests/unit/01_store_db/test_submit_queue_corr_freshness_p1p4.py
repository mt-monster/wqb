# -*- coding: utf-8 -*-
"""提交队列相关性新鲜度标注（2026-10-20 P1-4）。

背景（实测）：`get_submit_ready(READY)` 的行**全部**是 `gate=IS_ONLY` —— prod 是
2026-10-08 的旧读数（0.479/0.484）、self 未测。下游（提交核对 / step-8 就绪判定）
只看 prod/self 数字本身，无法分辨「刚测的」与「两周前的」。本测试覆盖
`annotate_corr_freshness` 的三类判据与两处时刻来源优先级：

  1. prod/self 任一为 None        → stale('missing')（无论时刻多新）
  2. 无可用检测时刻                → stale('no_timestamp')
  3. age > 48h                     → stale('aged')；≤48h → fresh
  4. 时刻优先级：corr_times（alphas.corr_checked_at）> verified_at（仅平台实测组）
  5. 批量入队的 verified_at 是入队时刻、不代表测过 —— verified_by='alphas' 不采信
  6. list_ready 端到端：可达 alphas.corr_checked_at；缺表/缺列（最小夹具）不崩
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from wqb.store import submit_queue as sq  # noqa: E402

NOW = datetime(2026, 10, 20, 12, 0, 0)


def _row(**kw):
    base = dict(alpha_id="AA1", region="EUR", prod=0.3, self=0.4,
                verified_by="verify", verified_at=(NOW - timedelta(hours=1)).isoformat())
    base.update(kw)
    return base


# ---------------- 判据 1：prod/self 未测全 ----------------

def test_missing_self_flags_stale_missing():
    r = sq.annotate_corr_freshness([_row(self=None)], corr_times={}, now=NOW)[0]
    assert r["corr_stale"] is True
    assert r["corr_stale_reason"] == "missing"
    assert r["corr_age_hours"] == 1.0  # 时刻仍在，只是 missing 优先


def test_missing_prod_and_self_both_scenarios():
    for kw in ({"prod": None}, {"self": None}):
        r = sq.annotate_corr_freshness([_row(**kw)], now=NOW)[0]
        assert r["corr_stale_reason"] == "missing", kw


# ---------------- 判据 2：无检测时刻 ----------------

def test_no_timestamp_when_nothing_available():
    r = sq.annotate_corr_freshness(
        [_row(verified_by="alphas", verified_at=None)], corr_times={}, now=NOW)[0]
    assert r["corr_stale"] is True
    assert r["corr_stale_reason"] == "no_timestamp"
    assert r["corr_age_hours"] is None


def test_batch_enqueue_verified_at_not_trusted():
    """verified_by='alphas' 的 verified_at 只是入队时刻（甚至可能是刚才），不采信。"""
    r = sq.annotate_corr_freshness(
        [_row(verified_by="alphas", verified_at=NOW.isoformat())], corr_times={}, now=NOW)[0]
    assert r["corr_stale"] is True
    assert r["corr_stale_reason"] == "no_timestamp"


# ---------------- 判据 3：时效 ----------------

def test_aged_over_48h():
    ts = (NOW - timedelta(hours=72)).isoformat()
    r = sq.annotate_corr_freshness([_row(alpha_id="AA1")], corr_times={"AA1": ts}, now=NOW)[0]
    assert r["corr_age_hours"] == 72.0
    assert r["corr_stale"] is True
    assert r["corr_stale_reason"] == "aged"


def test_fresh_below_threshold():
    ts = (NOW - timedelta(hours=5)).isoformat()
    r = sq.annotate_corr_freshness([_row(alpha_id="AA1")], corr_times={"AA1": ts}, now=NOW)[0]
    assert r["corr_age_hours"] == 5.0
    assert r["corr_stale"] is False
    assert r["corr_stale_reason"] == ""


def test_stale_after_hours_override():
    ts = (NOW - timedelta(hours=5)).isoformat()
    r = sq.annotate_corr_freshness([_row(alpha_id="AA1")], corr_times={"AA1": ts},
                                   now=NOW, stale_after_hours=1.0)[0]
    assert r["corr_stale"] is True
    assert r["corr_stale_reason"] == "aged"


# ---------------- 判据 4：时刻优先级 ----------------

def test_corr_times_wins_over_verified_at():
    """alphas.corr_checked_at（旧）存在时，不得被行内新的 verified_at 冒充新鲜。"""
    old = (NOW - timedelta(hours=100)).isoformat()
    r = sq.annotate_corr_freshness([_row(alpha_id="AA1")], corr_times={"AA1": old}, now=NOW)[0]
    assert r["corr_age_hours"] == 100.0
    assert r["corr_stale_reason"] == "aged"


def test_platform_verified_at_fallback():
    """无 corr_times 时，平台实测组（verify/API/submit_verdict）的 verified_at 可作时刻。"""
    r = sq.annotate_corr_freshness(
        [_row(verified_by="submit_verdict", verified_at=(NOW - timedelta(hours=2)).isoformat())],
        corr_times={}, now=NOW)[0]
    assert r["corr_age_hours"] == 2.0
    assert r["corr_stale"] is False


def test_unparsable_timestamp_is_no_timestamp():
    r = sq.annotate_corr_freshness(
        [_row(alpha_id="AA1")], corr_times={"AA1": "not-a-time"}, now=NOW)[0]
    # corr_times 不可解析 → 回退 verified_by=verify 的行内 verified_at（1h 前，可解析）
    assert r["corr_stale"] is False
    r2 = sq.annotate_corr_freshness(
        [_row(verified_by="alphas", verified_at="garbage")], corr_times={}, now=NOW)[0]
    assert r2["corr_stale_reason"] == "no_timestamp"


# ---------------- 判据 6：list_ready 端到端 ----------------

def _mk_db(tmp_path, with_corr_col=True):
    db = str(tmp_path / "t.db")
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE IF NOT EXISTS alphas (alpha_id TEXT PRIMARY KEY)")
    if with_corr_col:
        con.execute("ALTER TABLE alphas ADD COLUMN corr_checked_at TEXT")
    con.commit()
    con.close()
    return db


def _ins(con, aid, **kw):
    rec = dict(alpha_id=aid, region="EUR", universe="TOP2500", delay=1,
               neutralization="SUBINDUSTRY", expr="rank(close)", skeleton="rank(F)",
               sharpe=2.0, fitness=1.5, turnover=0.2, two_year=2.1,
               prod=0.3, self=0.4, status="READY",
               # 运行时相对时刻（list_ready 用真实 now；写死日期会随时间变陈旧）
               verified_by="verify",
               verified_at=(datetime.now() - timedelta(hours=1)).isoformat(timespec="seconds"))
    rec.update(kw)
    con.execute(
        "INSERT INTO submit_ready (alpha_id,region,universe,delay,neutralization,expr,skeleton,"
        "sharpe,fitness,turnover,two_year,prod,self,status,verified_by,verified_at) "
        "VALUES (:alpha_id,:region,:universe,:delay,:neutralization,:expr,:skeleton,"
        ":sharpe,:fitness,:turnover,:two_year,:prod,:self,:status,:verified_by,:verified_at)", rec)


def test_list_ready_annotates_from_alphas_corr_checked_at(tmp_path):
    db = _mk_db(tmp_path)
    con = sq.connect(db)
    sq.ensure_table(con)
    _ins(con, "AA1")
    # list_ready 用真实 now，故用「相对现在 72h 前」的时间戳
    real_old = (datetime.now() - timedelta(hours=72)).isoformat(timespec="seconds")
    con.execute("INSERT INTO alphas (alpha_id, corr_checked_at) VALUES ('AA1', ?)", (real_old,))
    con.commit()
    con.close()

    rows = sq.list_ready(region="EUR", db_path=db)
    assert len(rows) == 1
    r = rows[0]
    assert r["corr_stale"] is True and r["corr_stale_reason"] == "aged"
    assert 70 < r["corr_age_hours"] < 74
    # 关键：corr_checked_at（两三天前）压过行内 verify 的 verified_at（1h 前）
    assert r["corr_age_hours"] > 48


def test_list_ready_survives_missing_corr_column_and_table(tmp_path):
    """最小夹具库：alphas 无 corr_checked_at 列 → 回退 verified_at，不崩。"""
    db = _mk_db(tmp_path, with_corr_col=False)
    con = sq.connect(db)
    sq.ensure_table(con)
    _ins(con, "AA1")
    con.commit()
    con.close()
    rows = sq.list_ready(region="EUR", db_path=db)
    assert rows[0]["corr_stale"] is False  # verify 1h 前 → 新鲜
    assert rows[0]["corr_age_hours"] is not None

    db2 = str(tmp_path / "no_alphas.db")
    con = sq.connect(db2)
    sq.ensure_table(con)
    _ins(con, "BB1")
    con.commit()
    con.close()
    rows2 = sq.list_ready(region="EUR", db_path=db2)  # alphas 表整个缺失
    assert rows2 and rows2[0]["corr_stale"] is False


def test_fixture_no_corr_col_returns_empty_map(tmp_path):
    db = _mk_db(tmp_path, with_corr_col=False)
    con = sq.connect(db)
    con.execute("INSERT INTO alphas (alpha_id) VALUES ('AA1')")
    assert sq._corr_checked_times(con, ["AA1"]) == {}
    con.close()