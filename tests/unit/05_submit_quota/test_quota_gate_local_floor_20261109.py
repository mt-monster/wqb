# -*- coding: utf-8 -*-
"""配额闸「本地下限」守护（2026-11-09 实证缺陷）。

背景（实测，不是推理）：
    `akK9ooZv` 提交时，`P0obGoQJ` 已 ACTIVE **67 秒**（平台真值
    `dateSubmitted=2026-11-09T02:41:01-05:00`），但同一时刻闸门仍报
    `ET 今日 REGULAR 0/4 → 剩余 4`。约 1 小时后 OS 池才收录这两颗。
    根因：`_quota_gate` 只数平台 `stage=OS` 池，而当天刚提交的 alpha 在
    OS 批次开跑前仍留在 `stage=IS`（不带 stage 时 MCP 默认就是 IS，且
    IS 列表按 `-dateSubmitted` 排序时未提交项 null 排在最前，同样捞不到）。

修法：`used = max(平台 OS 池, 本地 submission_ledger 当日 ACTIVE)`。
    只抬不降 ⇒ 不会放松既有闸门；本地不可读时行为与旧版完全一致。

这里覆盖四个点：
  1. 平台漏计（OS 池为空）+ 本地有 1 颗 → used=1，不再报 0。
  2. 平台漏计 + 本地已满 4 颗 → blocked（旧版会放行第 5 颗）。
  3. 平台读数高于本地 → 以平台为准（不被本地拉低）。
  4. 本地不可读（无库/异常）→ 与旧版一致，纯平台口径。
"""
from __future__ import annotations

import datetime as _dt

import pytest

from wqb.timeutil import et_today
from wqb.workflow.nodes import submit_alpha as sa


class _FakeClient:
    """只实现 get_user_alphas 的最小桩。"""

    def __init__(self, results):
        self._results = results
        self.calls = 0

    async def get_user_alphas(self, **kwargs):  # noqa: D401 - 桩
        self.calls += 1
        assert kwargs.get("stage") == "OS", "配额闸必须只查 OS 池（本地下限另行兜底）"
        if self._results is None:
            return {"results": None}
        return {"results": self._results}


def _entry(alpha_id: str, *, day_offset: int = 0, type_: str = "REGULAR") -> dict:
    """构造一条 dateSubmitted = ET 今日 - day_offset 的记录（平台格式 -05:00）。"""
    base = _dt.datetime.strptime(et_today(), "%Y-%m-%d") + _dt.timedelta(days=-day_offset)
    stamp = base.replace(hour=2, minute=41, second=1).strftime("%Y-%m-%dT%H:%M:%S-05:00")
    return {"id": alpha_id, "type": type_, "dateSubmitted": stamp,
            "settings": {"region": "ASI"}}


def _stub_local(monkeypatch, used: int | None, super_used: int = 0):
    """把 _local_today_quota 换成固定返回值；None = 读不到。"""
    if used is None:
        monkeypatch.setattr(sa, "_local_today_quota", lambda *a, **k: None)
        return
    monkeypatch.setattr(
        sa, "_local_today_quota",
        lambda *a, **k: {"regular_used": used, "super_used": super_used,
                         "et_day": et_today()})


def test_platform_lag_falls_back_to_local(monkeypatch):
    """平台 OS 池漏计 → 用本地 1 颗补上，不再谎报 0/4。"""
    _stub_local(monkeypatch, 1)
    gate = sa._quota_gate(_FakeClient([]), "akK9ooZv")

    assert gate["allowed"] is True
    assert gate["used"] == 1, "平台报 0 而本地有 1 颗，必须取 1"
    assert gate["local_used"] == 1
    assert gate["remaining"] == 3


def test_local_full_blocks_fifth_submission(monkeypatch):
    """本地已 4 颗、平台仍报 0 ⇒ 必须拦下第 5 颗（旧版会放它去撞 403）。"""
    _stub_local(monkeypatch, 4)
    gate = sa._quota_gate(_FakeClient([]), "zzzzzzzz")

    assert gate["allowed"] is False
    assert gate["used"] == 4
    assert gate["remaining"] == 0
    assert "REGULAR_SUBMISSION" in gate["reason"]


def test_platform_wins_when_higher(monkeypatch):
    """平台读数更高时以平台为准，本地下限绝不拉低用量。"""
    _stub_local(monkeypatch, 1)
    client = _FakeClient([_entry("a"), _entry("b"), _entry("c")])

    gate = sa._quota_gate(client, "dddddddd")

    assert gate["used"] == 3
    assert gate["local_used"] == 1
    assert gate["remaining"] == 1


def test_local_unavailable_keeps_old_behaviour(monkeypatch):
    """本地读不到 ⇒ 纯平台口径，行为与 2026-11-09 之前完全一致。"""
    _stub_local(monkeypatch, None)
    gate = sa._quota_gate(_FakeClient([_entry("a")]), "eeeeeeee")

    assert gate["allowed"] is True
    assert gate["used"] == 1
    assert gate["local_used"] is None


def test_previous_day_entries_do_not_count(monkeypatch):
    """昨天的提交不计入今日（ET 日历日切齐），避免跨日误拦。"""
    _stub_local(monkeypatch, None)
    gate = sa._quota_gate(_FakeClient([_entry("old", day_offset=1)]), "ffffffff")

    assert gate["used"] == 0
    assert gate["remaining"] == 4


def test_local_reader_is_readonly_and_tolerates_missing_db(tmp_path):
    """_local_today_quota 对不存在的库必须返回 None（绝不抛、绝不写）。"""
    missing = tmp_path / "nope.db"
    assert sa._local_today_quota(str(missing)) is None


def test_local_reader_counts_today_rows(tmp_path, monkeypatch):
    """建一个临时库，写入今日 1 颗 ACTIVE + 昨日 1 颗 + 1 颗 FAILED，只应计 1。"""
    import sqlite3

    db = tmp_path / "quota.db"
    con = sqlite3.connect(db)
    con.execute(
        "CREATE TABLE submission_ledger (id INTEGER PRIMARY KEY, alpha_id TEXT, "
        "region TEXT, submission_type TEXT, status TEXT, quota_used INT, verdict TEXT, "
        "submitted_at TEXT, verified_at TEXT, created_at TEXT, updated_at TEXT)")
    today = _entry("today")["dateSubmitted"]
    yday = _entry("yday", day_offset=1)["dateSubmitted"]
    rows = [
        ("today", "ASI", "REGULAR", "ACTIVE", today),
        ("yday", "ASI", "REGULAR", "ACTIVE", yday),
        ("bad", "ASI", "REGULAR", "FAILED", today),
    ]
    con.executemany(
        "INSERT INTO submission_ledger (alpha_id, region, submission_type, status, submitted_at) "
        "VALUES (?,?,?,?,?)", rows)
    con.commit()
    con.close()

    q = sa._local_today_quota(str(db))

    assert q is not None
    assert q["regular_used"] == 1, "只数今日 ACTIVE，昨日与 FAILED 都不计"


def test_gate_never_raises_on_client_error(monkeypatch):
    """平台调用异常保持 fail-open（既有政策不变），不因本地下限引入新故障点。"""
    _stub_local(monkeypatch, 2)

    class _Boom:
        async def get_user_alphas(self, **kwargs):
            raise RuntimeError("boom")

    gate = sa._quota_gate(_Boom(), "gggggggg")
    assert gate["allowed"] is True
    assert gate["used"] is None


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
