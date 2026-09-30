# -*- coding: utf-8 -*-
"""2026-09-21：submit_queue 的换手上限必须与平台一致（config.GATES_PLATFORM 1%–70%），
不得硬编码 0.4：GLB 候选 d5bnE8jJ（tvr 0.446，其余全过）曾被判 FAIL:HIGH_TURNOVER→DEAD。"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from wqb.config import GATES_PLATFORM  # noqa: E402
from wqb.store import submit_queue as sq  # noqa: E402


def test_turnover_limit_matches_platform_gate():
    assert sq.LIM["turnover_hi"] == GATES_PLATFORM["turnover_range"][1] == 0.70


def test_turnover_045_passes_and_075_fails():
    ok, why = sq.is_pass(3.62, 1.49, None, 0.446, 0.63, 0.14, ra_failed_checks=[], expr="trade_when(x, y, z)")
    assert ok, why
    ok2, why2 = sq.is_pass(3.62, 1.49, None, 0.75, 0.63, 0.14, ra_failed_checks=[], expr="trade_when(x, y, z)")
    assert not ok2 and why2 == "HIGH_TURNOVER"


def test_dead_row_revives_when_readd_passes(tmp_path, monkeypatch):
    """2026-09-21：本地误判 DEAD 的候选在重新 add 且闸门通过时必须复活为 READY
    （SUBMITTED 仍粘滞）。实证：d5bnE8jJ 首次 add 被旧换手上限判 DEAD，修复后再 add 仍卡 DEAD。"""
    db = tmp_path / "q.db"
    con = sq.connect(str(db))
    sq.ensure_table(con)
    rec = dict(alpha_id="aaaa1111", region="GLB", expr="trade_when(x, y, z)", sharpe=3.6, fitness=1.49,
               turnover=0.446, prod=0.63, self=0.14)
    monkeypatch.setitem(sq.LIM, "turnover_hi", 0.4)
    sq.enqueue(con, rec, note="first")
    row = con.execute("SELECT status, gate FROM submit_ready WHERE alpha_id='aaaa1111'").fetchone()
    assert row[0] == "DEAD" and "HIGH_TURNOVER" in row[1], row
    monkeypatch.setitem(sq.LIM, "turnover_hi", 0.7)
    sq.enqueue(con, rec, note="second")
    row = con.execute("SELECT status, gate, note FROM submit_ready WHERE alpha_id='aaaa1111'").fetchone()
    assert row[0] == "READY", row
    assert "revived" in (row[2] or "")
    # SUBMITTED 粘滞
    con.execute("UPDATE submit_ready SET status='SUBMITTED' WHERE alpha_id='aaaa1111'")
    con.commit()
    sq.enqueue(con, rec, note="third")
    assert con.execute("SELECT status FROM submit_ready WHERE alpha_id='aaaa1111'").fetchone()[0] == "SUBMITTED"
