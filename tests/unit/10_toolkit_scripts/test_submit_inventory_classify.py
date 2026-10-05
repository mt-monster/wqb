# -*- coding: utf-8 -*-
"""tools/submit_inventory.py 分类器回归（2026-10-05）：相关性缺失必须 fail-closed。

背景坑（当日实测）：脚本首版的 `classify()` 里 prod / self 用
``round(lim - v, 4) if v is not None else None`` 计算余量——**None 被当成「余量充足」**，
导致 5 颗 gate=`FAIL:PROD_SIBLING`（prod 从未实测，仅因同骨架兄弟撞墙而被推定阻塞）的
GBR 候选被误判成 `SUBMIT_NOW`，并被 `mark_verified` 升级成 `status=READY` +
`gate=SUBMIT_LAYER_VERIFIED: prodNone+selfNone`——从「等池子松动的候选」直接跳成
「可提交」，READY 从 2 条被污染到 7 条。

平台 SELF_CORRELATION 是真实硬闸（线 0.7），prod 或 self 只要有一个未实测就**无法确认**
通过，必须判 `CORR_UNKNOWN`，绝不进入 SUBMIT_NOW / THIN_MARGIN。本文件钉死该语义。
"""
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.store import submit_queue as sq  # noqa: E402
import submit_inventory as si  # noqa: E402

_REGIONS = "CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);"
OK_RES = {"verdict": "UNVERIFIABLE", "reason_code": "UNVERIFIABLE_404",
          "verdict_note": "提交层 404（死端点）"}


# ---------------- classify：fail-closed ----------------

def test_submit_now_when_clean_fresh_with_margin():
    b, code, _ = si.classify(OK_RES, 0.5626, 0.1301, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("SUBMIT_NOW", "SUBMIT_NOW")
    assert "0.1374" in _


def test_thin_margin_below_threshold():
    b, code, note = si.classify(OK_RES, 0.6762, 0.6760, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("THIN_MARGIN", "THIN_MARGIN")
    assert "0.0238" in note


@pytest.mark.parametrize("prod,selfc,tag", [
    (None, 0.5, "CORR_MISSING_PROD"),   # ← 本次事故的核心场景
    (0.5, None, "CORR_MISSING_SELF"),   # 平台 SELF 是真硬闸，缺了同样不能判
    (None, None, "CORR_MISSING_BOTH"),
])
def test_missing_corr_fails_closed_not_submit_now(prod, selfc, tag):
    b, code, _ = si.classify(OK_RES, prod, selfc, True, 0.03, 0.7, 0.7)
    assert b == "CORR_UNKNOWN", f"{tag}: prod={prod} self={selfc} 不得进入 SUBMIT_NOW/THIN_MARGIN"
    assert code == "CORR_MISSING"


def test_missing_margin_never_becomes_submit_now_even_when_fresh():
    """余量算不出来时不得当 0 处理再走 THIN_MARGIN，也不得默认 SUBMIT_NOW。"""
    b, code, _ = si.classify(OK_RES, None, None, True, 0.03, 0.7, 0.7)
    assert b == "CORR_UNKNOWN" and code == "CORR_MISSING"


def test_stale_freshness_is_corr_unknown():
    b, code, _ = si.classify(OK_RES, 0.5, 0.5, False, 0.03, 0.7, 0.7)
    assert (b, code) == ("CORR_UNKNOWN", "CORR_STALE_OR_MISSING")


def test_prod_above_line_is_prod_wall():
    b, code, _ = si.classify(OK_RES, 0.9936, None, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("PROD_WALL", "FAIL:PROD")


def test_self_above_line_is_prod_wall():
    b, code, _ = si.classify(OK_RES, 0.5, 0.94, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("PROD_WALL", "FAIL:SELF")


def test_blocked_verdict_is_hard_blocked():
    res = dict(OK_RES, verdict="BLOCKED", reason_code="FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE")
    b, code, _ = si.classify(res, 0.5, 0.5, True, 0.03, 0.7, 0.7)
    assert b == "HARD_BLOCKED"
    assert code.startswith("FAILED_COUNT_RA")


def test_sim_fail_beats_good_corr():
    res = dict(OK_RES, verdict="BLOCKED", reason_code="SIM_FAIL:LOW_ROBUST_UNIVERSE_SHARPE")
    b, code, _ = si.classify(res, 0.1, 0.1, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("HARD_BLOCKED", "SIM_FAIL:LOW_ROBUST_UNIVERSE_SHARPE")


def test_already_submitted_short_circuits():
    res = dict(OK_RES, verdict="ALREADY_SUBMITTED", reason_code="ALREADY_SUBMITTED")
    b, code, _ = si.classify(res, 0.5, 0.5, True, 0.03, 0.7, 0.7)
    assert b == "ALREADY_SUBMITTED"


# ---------------- classify：边界 ----------------

def test_exact_line_is_blocked_not_thin_margin():
    b, code, _ = si.classify(OK_RES, 0.7, 0.5, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("PROD_WALL", "FAIL:PROD")


def test_one_cent_below_line_is_thin_margin():
    b, code, _ = si.classify(OK_RES, 0.69, 0.5, True, 0.03, 0.7, 0.7)
    assert (b, code) == ("THIN_MARGIN", "THIN_MARGIN")


# ---------------- corr_fresh ----------------

def test_corr_fresh_requires_both_measured():
    assert si.corr_fresh(1.0, 1.0, 48) == (True, "")
    assert si.corr_fresh(None, 1.0, 48) == (False, "prod 未实测")
    assert si.corr_fresh(1.0, None, 48) == (False, "self 未实测")
    ok, reason = si.corr_fresh(49.0, 49.0, 48)
    assert ok is False and "prod 已 49.0h" in reason and "self 已 49.0h" in reason


def test_corr_fresh_only_one_side_stale():
    ok, reason = si.corr_fresh(49.0, 1.0, 48)
    assert ok is False and "prod 已 49.0h" in reason and "self" not in reason


# ---------------- sync_row：队列同步 ----------------

@pytest.fixture(autouse=True)
def db(tmp_path, monkeypatch):
    """**autouse**：每个用例都必须落到临时库。

    教训（2026-10-05，见 test_submit_queue_mark_blocked.py）：非 autouse 时漏声明的
    用例会回退 `default_db_path()` → 把测试行写进真实 `data/wqb.db`。
    """
    path = str(tmp_path / "t.db")
    con = sqlite3.connect(path)
    con.executescript(_REGIONS)
    con.commit()
    con.close()
    monkeypatch.setenv("WQB_DB_PATH", path)
    return path


def _ins(aid, *, gate, status=sq.STATUS_READY, prod=None, self_=None):
    c = sq.connect()
    try:
        sq.ensure_table(c)
        sq._upsert(c, {"alpha_id": aid, "region": "GBR", "universe": "TOP700",
                       "sharpe": 2.0, "fitness": 1.5, "two_year": 2.0, "turnover": 0.15,
                       "prod": prod, "self": self_, "expr": "rank(a)"})
        c.execute("UPDATE submit_ready SET gate=?, status=? WHERE alpha_id=?",
                  (gate, status, aid))
        c.commit()
    finally:
        c.close()


def _row(aid, gate, status=sq.STATUS_PROD_BLOCKED, prod=None, self_=None):
    return {"alpha_id": aid, "region": "GBR", "status": status, "gate": gate,
            "prod": prod, "self": self_, "note": "",
            "sharpe": 2.0, "fitness": 1.5, "two_year": 2.0, "turnover": 0.15}


def test_corr_unknown_keeps_original_status_and_gate():
    """PROD_SIBLING 行相关性未实测 → 保留 PROD_BLOCKED + 原判据，只追加 note。"""
    aid = "SIB00001"
    _ins(aid, gate="FAIL:PROD_SIBLING(XgbNvvkX=0.70)", status=sq.STATUS_PROD_BLOCKED)
    out = si.sync_row(_row(aid, "FAIL:PROD_SIBLING(XgbNvvkX=0.70)"),
                      "CORR_UNKNOWN", OK_RES, None, None, True,
                      db_path=None, thin=0.03)
    assert out["synced"] is True and out["why"] == "noted_keep_original"
    c = sq.connect()
    try:
        r = c.execute("SELECT status, gate, note FROM submit_ready WHERE alpha_id=?", (aid,)).fetchone()
    finally:
        c.close()
    assert r["status"] == sq.STATUS_PROD_BLOCKED
    assert r["gate"] == "FAIL:PROD_SIBLING(XgbNvvkX=0.70)"
    assert "corr_未实测@" in r["note"]


def test_corr_unknown_note_is_idempotent_same_day():
    aid = "SIB00002"
    _ins(aid, gate="FAIL:PROD_SIBLING(j289gVAk=0.71)", status=sq.STATUS_PROD_BLOCKED)
    row = _row(aid, "FAIL:PROD_SIBLING(j289gVAk=0.71)")
    si.sync_row(row, "CORR_UNKNOWN", OK_RES, None, None, True, db_path=None, thin=0.03)
    si.sync_row(row, "CORR_UNKNOWN", OK_RES, None, None, True, db_path=None, thin=0.03)
    c = sq.connect()
    try:
        note = c.execute("SELECT note FROM submit_ready WHERE alpha_id=?", (aid,)).fetchone()[0] or ""
    finally:
        c.close()
    assert note.count("corr_未实测@") == 1


def test_submit_now_writes_enriched_gate_and_sources_inventory():
    aid = "GOOD0001"
    _ins(aid, gate="IS_ONLY", status=sq.STATUS_READY, prod=0.5626, self_=0.1301)
    out = si.sync_row(_row(aid, "IS_ONLY", status=sq.STATUS_READY,
                           prod=0.5626, self_=0.1301),
                      "SUBMIT_NOW", OK_RES, 0.5626, 0.1301, True,
                      db_path=None, thin=0.03)
    assert out["synced"] is True and out["why"] == "upgraded"
    c = sq.connect()
    try:
        r = c.execute("SELECT status, gate, verified_by, prod, self FROM submit_ready "
                      "WHERE alpha_id=?", (aid,)).fetchone()
    finally:
        c.close()
    assert r["status"] == sq.STATUS_READY
    assert r["gate"].startswith("SUBMIT_LAYER_VERIFIED")      # LIKE 过滤仍可用
    assert "0.1374" in r["gate"]                               # 余量信息没被刷丢
    assert r["verified_by"] == "submit_inventory"
    assert abs(r["prod"] - 0.5626) < 1e-9


def test_thin_margin_gate_flags_do_not_submit():
    aid = "THIN0001"
    _ins(aid, gate="IS_ONLY", status=sq.STATUS_READY, prod=0.6762, self_=0.6760)
    si.sync_row(_row(aid, "IS_ONLY", status=sq.STATUS_READY,
                     prod=0.6762, self_=0.6760),
                "THIN_MARGIN", OK_RES, 0.6762, 0.6760, True,
                db_path=None, thin=0.03)
    c = sq.connect()
    try:
        gate = c.execute("SELECT gate FROM submit_ready WHERE alpha_id=?", (aid,)).fetchone()[0]
    finally:
        c.close()
    assert "建议不提" in gate and "0.0238" in gate


def test_no_sync_flag_is_noop():
    aid = "NOOP0001"
    _ins(aid, gate="FAIL:PROD_SIBLING(XgbNvvkX=0.70)", status=sq.STATUS_PROD_BLOCKED)
    out = si.sync_row(_row(aid, "FAIL:PROD_SIBLING(XgbNvvkX=0.70)"),
                      "CORR_UNKNOWN", OK_RES, None, None, False,
                      db_path=None, thin=0.03)
    assert out == {"alpha_id": aid, "bucket": "CORR_UNKNOWN",
                   "synced": False, "why": "no_sync_queue"}


def test_unhandled_bucket_is_noop():
    out = si.sync_row(_row("X1", "PASS"), "ERROR", OK_RES, None, None, True,
                      db_path=None, thin=0.03)
    assert out["synced"] is False and out["why"] == "bucket_not_synced"
