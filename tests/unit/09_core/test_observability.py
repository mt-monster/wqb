"""Unit tests for wqb.memory.events — EventLog append-only store.

Covers:
- ``emit`` writes a JSONL record to the correct date file.
- ``EventLog.read`` returns events for a specific date.
- ``EventLog.query`` filters by event name.
- ``EventLog.recent`` returns the N most recent events.
- ``EventLog.list_dates`` and ``EventLog.count``.
- ``emit_to_dir`` allows specifying a custom directory.
- Event type constants are exported correctly.
"""

import json
import os
from datetime import datetime, timezone, timedelta

import pytest

from wqb.memory.events import (
    ALL_EVENT_TYPES,
    EVENT_ALPHA_QUALIFIED,
    EVENT_ALPHA_REJECTED,
    EVENT_ROBUSTNESS_AUDIT,
    EVENT_SCHEDULER_PLAN,
    EVENT_SIMULATION_BATCH,
    EventLog,
    emit,
    emit_to_dir,
    _event_file_path,
    _today_str,
)


@pytest.fixture
def events_dir(tmp_path):
    return str(tmp_path / "events")


def test_emit_creates_directory_and_file(events_dir):
    record = emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=1.5)
    assert os.path.isdir(events_dir)
    today = _today_str()
    filepath = os.path.join(events_dir, f"{today}.jsonl")
    assert os.path.exists(filepath)
    assert record["event"] == EVENT_ALPHA_QUALIFIED
    assert record["sharpe"] == 1.5


def test_emit_to_dir_writes_jsonl(events_dir):
    emit_to_dir(events_dir, EVENT_ROBUSTNESS_AUDIT, decision="REJECT")
    today = _today_str()
    filepath = os.path.join(events_dir, f"{today}.jsonl")
    with open(filepath, "r", encoding="utf-8") as f:
        line = f.read().strip()
    record = json.loads(line)
    assert record["event"] == EVENT_ROBUSTNESS_AUDIT
    assert record["decision"] == "REJECT"


def test_emit_to_dir_multiple_appends(events_dir):
    emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=1.0)
    emit_to_dir(events_dir, EVENT_ALPHA_REJECTED, reason="decay_ratio")
    today = _today_str()
    filepath = os.path.join(events_dir, f"{today}.jsonl")
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l for l in f.read().strip().split("\n") if l]
    assert len(lines) == 2
    assert json.loads(lines[0])["event"] == EVENT_ALPHA_QUALIFIED
    assert json.loads(lines[1])["event"] == EVENT_ALPHA_REJECTED


# ---------------------------------------------------------------------------
# EventLog.read
# ---------------------------------------------------------------------------

def test_eventlog_read_nonexistent_date_returns_empty(events_dir):
    log = EventLog(events_dir)
    events = log.read("2020-01-01")
    assert events == []


def test_eventlog_read_today(events_dir):
    emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=1.5)
    log = EventLog(events_dir)
    events = log.read()
    assert len(events) == 1
    assert events[0]["event"] == EVENT_ALPHA_QUALIFIED


def test_eventlog_read_invalid_json_skipped(events_dir):
    today = _today_str()
    filepath = os.path.join(events_dir, f"{today}.jsonl")
    os.makedirs(events_dir, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("not json\n")
        f.write('{"event": "alpha.qualified", "timestamp": "2026-01-01T00:00:00+00:00", "sharpe": 1.0}\n')
    log = EventLog(events_dir)
    events = log.read()
    assert len(events) == 1
    assert events[0]["sharpe"] == 1.0


# ---------------------------------------------------------------------------
# EventLog.query
# ---------------------------------------------------------------------------

def test_eventlog_query_by_event_name(events_dir):
    emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=1.0)
    emit_to_dir(events_dir, EVENT_ALPHA_REJECTED, reason="low_sharpe")
    emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=2.0)
    log = EventLog(events_dir)
    qualified = log.query(event_name=EVENT_ALPHA_QUALIFIED)
    rejected = log.query(event_name=EVENT_ALPHA_REJECTED)
    assert len(qualified) == 2
    assert len(rejected) == 1


def test_eventlog_query_all(events_dir):
    emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=1.0)
    emit_to_dir(events_dir, EVENT_ALPHA_REJECTED, reason="decay")
    log = EventLog(events_dir)
    all_events = log.query()
    assert len(all_events) == 2


# ---------------------------------------------------------------------------
# EventLog.recent
# ---------------------------------------------------------------------------

def test_eventlog_recent_all(events_dir):
    for i in range(3):
        emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=float(i))
    log = EventLog(events_dir)
    recent = log.recent(5)
    assert len(recent) == 3


def test_eventlog_recent_limited(events_dir):
    for i in range(10):
        emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=float(i))
    log = EventLog(events_dir)
    recent = log.recent(3)
    assert len(recent) == 3


def test_eventlog_recent_nonexistent_dir():
    log = EventLog("nonexistent_dir_abc123")
    assert log.recent(5) == []


# ---------------------------------------------------------------------------
# EventLog.list_dates / count
# ---------------------------------------------------------------------------

def test_eventlog_list_dates(events_dir):
    today = _today_str()
    filepath = os.path.join(events_dir, f"{today}.jsonl")
    os.makedirs(events_dir, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write('{"event": "alpha.qualified", "timestamp": "x"}\n')
    log = EventLog(events_dir)
    dates = log.list_dates()
    assert today in dates


def test_eventlog_list_dates_empty():
    log = EventLog(events_dir := "nonexistent_empty_abc")
    assert log.list_dates() == []


def test_eventlog_count(events_dir):
    emit_to_dir(events_dir, EVENT_ALPHA_QUALIFIED, sharpe=1.0)
    emit_to_dir(events_dir, EVENT_ALPHA_REJECTED, reason="decay")
    log = EventLog(events_dir)
    assert log.count() == 2
    assert log.count(event_name=EVENT_ALPHA_QUALIFIED) == 1


# ---------------------------------------------------------------------------
# Event type constants
# ---------------------------------------------------------------------------

def test_all_event_types_constant():
    assert EVENT_ROBUSTNESS_AUDIT in ALL_EVENT_TYPES
    assert EVENT_SIMULATION_BATCH in ALL_EVENT_TYPES
    assert EVENT_ALPHA_QUALIFIED in ALL_EVENT_TYPES
    assert EVENT_ALPHA_REJECTED in ALL_EVENT_TYPES
    assert EVENT_SCHEDULER_PLAN in ALL_EVENT_TYPES


def test_event_types_are_strings():
    for t in ALL_EVENT_TYPES:
        assert isinstance(t, str)
        assert len(t) > 0