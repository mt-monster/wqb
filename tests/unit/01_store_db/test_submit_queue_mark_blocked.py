# -*- coding: utf-8 -*-
"""submit_queue.mark_blocked 回归（2026-10-05）：判定权威必须能「降」回队列。

背景坑（当日实测）：`tools/submit_verdict.py` 此前只升级不降级——出 BLOCKED /
ALREADY_SUBMITTED 时不写回 `submit_ready`，队列行继续挂上一轮手写的
`gate=PASS` + `status=READY`，盘点时把已被平台 RA 硬闸拦住的候选
（A1vOb5pE 1.63/1.78、ZYAWx9J3 1.42/1.58）和已 ACTIVE 的候选
（9qWaRGEK、gJZ7AvZO）当成「可提交」。8 条 READY 实测只有 1 颗真可提交。

本文件钉死 ``mark_blocked`` 与 ``mark_verified`` 的对称语义：
  1. BLOCKED（reason=FAILED_COUNT_*）→ DEAD，gate 记录实测 reason
  2. ALREADY_SUBMITTED                → SUBMITTED
  3. 已是 SUBMITTED 的行不动（勿覆盖终态）
  4. 已是 DEAD 且 gate 一致 → 幂等，只追加 recheck note
  5. 表里无此行 → changed=0，不抛异常（容错口径）
"""
import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from wqb.store import submit_queue as sq  # noqa: E402

_REGIONS = "CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);"


@pytest.fixture(autouse=True)
def db(tmp_path, monkeypatch):
    """**autouse**：每个用例都必须落到临时库。

    教训（2026-10-05）：本文件首版该 fixture 非 autouse，`_sync_queue` 那几个用例忘了
    声明依赖，`sq.connect()` 回退到 `default_db_path()` → 把测试行 A1/I1/H1 等
    **写进了真实 `data/wqb.db`**（9 行，已清理）。autouse 之后不可能再漏声明。
    """
    path = str(tmp_path / "t.db")
    con = sqlite3.connect(path)
    con.executescript(_REGIONS)
    con.commit()
    con.close()
    monkeypatch.setenv("WQB_DB_PATH", path)
    return path


def _ins(aid, gate="PASS", status=sq.STATUS_READY, prod=None, self_=None,
         sharpe=3.0, fitness=2.0):
    c = sq.connect()
    try:
        sq.ensure_table(c)
        sq._upsert(c, {
            "alpha_id": aid, "region": "IND", "universe": "TOP500",
            "sharpe": sharpe, "fitness": fitness, "two_year": 2.5,
            "turnover": 0.2, "prod": prod, "self": self_, "expr": "rank(a)",
        })
        c.commit()          # _upsert 不提交（由 enqueue 调用方负责），fixture 需自行提交
    finally:
        c.close()
    # 覆盖成「上一轮手写的旧判定」，模拟历史脏数据
    c = sq.connect()
    try:
        c.execute("UPDATE submit_ready SET gate=?, status=? WHERE alpha_id=?",
                  (gate, status, aid))
        c.commit()
    finally:
        c.close()


def _get(aid):
    c = sq.connect()
    try:
        row = c.execute(
            "SELECT status, gate, note FROM submit_ready WHERE alpha_id=?", (aid,)).fetchone()
        return dict(row) if row else None
    finally:
        c.close()


def test_blocked_reason_downgrades_to_dead():
    _ins("A1", gate="PASS: 4gates+prod0.69+self0.31",
         prod=0.69, self_=0.31)
    r = sq.mark_blocked("A1", reason="FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE")
    row = _get("A1")
    assert r["changed"] == 1 and r["status"] == sq.STATUS_DEAD
    assert row["status"] == sq.STATUS_DEAD
    # gate 记录实测 reason（不是旧的手写 PASS）
    assert row["gate"] == "FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE"
    # 旧判定不可信 → note 必须留痕
    assert "submit_verdict" in (row["note"] or "")
    # 指标保留，便于复盘
    c = sq.connect()
    try:
        assert c.execute("SELECT prod FROM submit_ready WHERE alpha_id='A1'").fetchone()[0] == 0.69
    finally:
        c.close()


def test_already_submitted_reason_downgrades_to_submitted():
    _ins("B1", gate="IS_ONLY", prod=0.65, self_=0.6)
    r = sq.mark_blocked("B1", reason="ALREADY_SUBMITTED")
    assert r["status"] == sq.STATUS_SUBMITTED
    assert _get("B1")["status"] == sq.STATUS_SUBMITTED
    assert _get("B1")["gate"] == "ALREADY_SUBMITTED"


def test_explicit_status_wins_over_inference():
    _ins("C1", gate="PASS")
    r = sq.mark_blocked("C1", reason="FAILED_COUNT_RA:LOW_SHARPE",
                        status=sq.STATUS_PROD_BLOCKED)
    assert r["status"] == sq.STATUS_PROD_BLOCKED
    assert _get("C1")["status"] == sq.STATUS_PROD_BLOCKED


def test_submitted_terminal_state_is_never_touched():
    _ins("D1", gate="SUBMIT_LAYER_VERIFIED", status=sq.STATUS_SUBMITTED)
    r = sq.mark_blocked("D1", reason="FAILED_COUNT_RA:LOW_SHARPE")
    assert r["changed"] == 0
    assert r["why"] == "not_found"                      # WHERE 已排除 SUBMITTED 终态
    row = _get("D1")
    assert row["status"] == sq.STATUS_SUBMITTED          # 终态不动
    assert row["gate"] == "SUBMIT_LAYER_VERIFIED"       # gate 不被覆盖


def test_dead_same_reason_is_idempotent_and_only_appends_note_once():
    """同一 reason 反复判定：第一次降级，之后只补一次 recheck，note 不再无限累加。"""
    _ins("E1", gate="PASS")
    r1 = sq.mark_blocked("E1", reason="FAILED_COUNT_RA:LOW_SHARPE")
    assert r1["changed"] == 1 and r1["why"] == "downgraded"
    first = _get("E1")

    r2 = sq.mark_blocked("E1", reason="FAILED_COUNT_RA:LOW_SHARPE")
    assert r2["changed"] == 1 and r2["why"] == "rechecked"
    second = _get("E1")
    assert second["status"] == sq.STATUS_DEAD
    assert second["gate"] == first["gate"]               # gate 不被重复写
    assert len(second["note"] or "") > len(first["note"] or "")

    # 第三次：同 reason 已在 note 里 → 不再累加
    r3 = sq.mark_blocked("E1", reason="FAILED_COUNT_RA:LOW_SHARPE")
    assert r3["changed"] == 1 and r3["why"] == "rechecked"
    assert _get("E1")["note"] == second["note"]


def test_missing_row_is_tolerated():
    r = sq.mark_blocked("NOT_EXIST", reason="FAILED_COUNT_RA:LOW_SHARPE")
    assert r["changed"] == 0 and r["why"] == "not_found"
    assert r["status"] == sq.STATUS_DEAD                 # 仍返回推断结果，便于上层日志


def test_marked_dead_row_is_excluded_from_list_ready():
    _ins("F1", gate="PASS")
    sq.mark_blocked("F1", reason="FAILED_COUNT_RA:LOW_SHARPE")
    ids = [r["alpha_id"] for r in sq.list_ready()]
    assert "F1" not in ids


def test_mark_verified_and_mark_blocked_are_symmetric_on_same_row():
    """同一行：先升级验证、后被判死 → 最终以平台判定的 DEAD 为准。"""
    _ins("G1", gate="IS_ONLY")
    assert sq.mark_verified("G1") == 1
    assert _get("G1")["status"] == sq.STATUS_READY
    sq.mark_blocked("G1", reason="FAILED_COUNT_RA:LOW_SHARPE")
    assert _get("G1")["status"] == sq.STATUS_DEAD


# ---- tools/submit_verdict.py::_sync_queue 的分派（含 ALREADY_SUBMITTED 早返回路径）----

def test_sync_queue_dispatch_upgrades_clean_verdict(capsys):
    """UNVERIFIABLE（现实中的「模拟层干净」）→ 升级 SUBMIT_LAYER_VERIFIED。"""
    from tools.submit_verdict import _sync_queue
    _ins("H1", gate="IS_ONLY")
    _sync_queue("H1", {"verdict": "UNVERIFIABLE", "reason_code": "UNVERIFIABLE_404"},
                {"is": {"sharpe": 3.0, "fitness": 2.0, "turnover": 0.2}})
    row = _get("H1")
    assert row["gate"] == "SUBMIT_LAYER_VERIFIED"
    assert row["status"] == sq.STATUS_READY
    assert "已升级" in capsys.readouterr().out


def test_sync_queue_dispatch_downgrades_already_submitted(capsys):
    """ALREADY_SUBMITTED 走 main() 的**提前 return** 分支，必须在此降级（否则成死代码）。"""
    from tools.submit_verdict import _sync_queue
    _ins("I1", gate="IS_ONLY")
    _sync_queue("I1", {"verdict": "ALREADY_SUBMITTED", "reason_code": "ALREADY_SUBMITTED"}, {})
    row = _get("I1")
    assert row["status"] == sq.STATUS_SUBMITTED
    assert row["gate"] == "ALREADY_SUBMITTED"
    assert "退出台账" in capsys.readouterr().out


def test_sync_queue_is_noop_for_verdicts_that_do_not_exist_in_queue(capsys):
    from tools.submit_verdict import _sync_queue
    _sync_queue("NOT_IN_QUEUE", {"verdict": "BLOCKED",
                                 "reason_code": "FAILED_COUNT_RA:LOW_SHARPE"}, {})
    out = capsys.readouterr().out
    assert "跳过降级" in out


def test_sync_queue_dispatch_downgrades_blocked(capsys):
    """BLOCKED（正常路径，非 ALREADY_SUBMITTED 提前 return）也必须降级到 DEAD。

    回归：A1vOb5pE / ZYAWx9J3 曾挂 `gate=PASS` + `status=READY` 却已被平台
    `FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE` 拦下；盘点工具把它们
    误标 SUBMIT_NOW。本用例锁定 BLOCKED → mark_blocked(reason=reason_code) → DEAD
    的传导，且 gate 必须记录**实测** reason_code 而非保留旧手写值。
    """
    from tools.submit_verdict import _sync_queue
    _ins("K1", gate="PASS: 4gates+prod0.69+self0.31", prod=0.69, self_=0.31)
    _sync_queue(
        "K1",
        {"verdict": "BLOCKED",
         "reason_code": "FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE"},
        {"is": {"sharpe": 1.63, "fitness": 1.78, "turnover": 0.2}},
    )
    row = _get("K1")
    assert row["status"] == sq.STATUS_DEAD
    assert row["gate"] == "FAILED_COUNT_RA:LOW_INVESTABILITY_CONSTRAINED_SHARPE"
    assert "已退出台账" in capsys.readouterr().out


def test_sync_queue_blocked_reason_falls_back_to_literal_blocked(capsys):
    """reason_code 缺失时 mark_blocked 仍要能降级，只是 gate 用兜底字符串 'BLOCKED'。"""
    from tools.submit_verdict import _sync_queue
    _ins("L1", gate="PASS")
    _sync_queue("L1", {"verdict": "BLOCKED", "reason_code": None}, {})
    row = _get("L1")
    assert row["status"] == sq.STATUS_DEAD
    assert row["gate"] == "BLOCKED"
    assert "已退出台账" in capsys.readouterr().out


def test_sync_queue_never_raises_on_store_error(capsys, monkeypatch):
    """队列写入异常不得影响判定结果与退出码（原设计契约）。"""
    from tools.submit_verdict import _sync_queue
    monkeypatch.setattr("wqb.store.submit_queue.mark_blocked",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    # 不应抛出
    _sync_queue("J1", {"verdict": "BLOCKED", "reason_code": "FAILED_COUNT_RA:LOW_SHARPE"}, {})
    assert "降级跳过" in capsys.readouterr().out
