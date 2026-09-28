"""Regressions for real EUR campaign failure modes; no platform requests."""
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import sys
import time

import pytest

REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mcp_efficiency", REPO / "tools/mcp_ping.py")
ping = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ping)


def test_silent_server_deadline_and_no_retry(tmp_path):
    script = tmp_path / "silent.py"
    calls = tmp_path / "calls.txt"
    script.write_text("import sys,time\nfrom pathlib import Path\n"
                      "line=sys.stdin.readline()\nPath(sys.argv[1]).write_text(line)\n"
                      "time.sleep(10)\n", encoding="utf-8")
    client = ping.McpStdioClient(sys.executable, [str(script), str(calls)], {}, timeout=1)
    try:
        started = time.monotonic()
        with pytest.raises(ping.McpCallTimeout) as caught:
            client._send("tools/call", {"name": "simulate"})
        assert time.monotonic() - started < 3
        assert caught.value.outcome_unknown is True
        with pytest.raises(RuntimeError, match="reconcile"):
            client._send("tools/call", {"name": "simulate"})
        assert len(calls.read_text().splitlines()) == 1
    finally:
        client.close()


def test_response_after_notification_and_junk(tmp_path):
    script = tmp_path / "respond.py"
    script.write_text("import sys,json\nq=json.loads(sys.stdin.readline())\n"
                      "print('startup log',flush=True)\n"
                      "print(json.dumps({'method':'notice'}),flush=True)\n"
                      "print(json.dumps({'id':q['id'],'result':{'ok':True}}),flush=True)\n",
                      encoding="utf-8")
    c = ping.McpStdioClient(sys.executable, [str(script)], {}, timeout=3)
    try:
        assert c._send("initialize")["result"]["ok"] is True
    finally:
        c.close()


def test_timeout_result_does_not_send_next_call(monkeypatch, capsys):
    class Client:
        def __init__(self, *a): pass
        def initialize(self): pass
        def list_tools(self): return [{"name": "simulate"}]
        def _send(self, *a): raise ping.McpCallTimeout("tools/call", 3, "simulate")
        def close(self): pass
    monkeypatch.setattr(ping, "McpStdioClient", Client)
    assert ping.run_calls({"command": "unused"}, [{"tool": "simulate"}]) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["outcome_unknown"] and result["retry_safe"] is False


def test_native_process_identity():
    from wqb.workflow.process_identity import process_identity, match_process
    observed = process_identity(os.getpid())
    assert observed and observed["created_at"] <= time.time()
    assert observed["executable"]
    assert match_process({"process_identity": observed}, observed) is True


def test_null_terminal_fields_do_not_finish_running_task(tmp_path, monkeypatch):
    from wqb.workflow import tasks
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path))
    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: True)
    identity = {"created_at": 100, "executable": "python"}
    monkeypatch.setattr(tasks, "process_identity", lambda pid: identity)
    (tmp_path / "task.json").write_text(json.dumps({"pid": 1, "success": None,
        "returncode": None, "finished_at": None, "process_identity": identity}), encoding="utf-8")
    assert tasks.get_task("task")["status"] == "running"


def test_unreadable_process_identity_is_unknown(tmp_path, monkeypatch):
    from wqb.workflow import tasks
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path))
    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: True)
    monkeypatch.setattr(tasks, "process_identity", lambda pid: None)
    (tmp_path / "task.json").write_text(json.dumps({"pid": 1}), encoding="utf-8")
    assert tasks.get_task("task")["status"] == "unknown"


@pytest.mark.parametrize("layout", ["flat", "dir"])
def test_reused_pid_is_not_running_or_succeeded(tmp_path, monkeypatch, layout):
    from wqb.workflow import tasks
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path))
    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: True)
    monkeypatch.setattr(tasks, "process_identity", lambda pid: {"created_at": 200, "executable": "other"})
    data = {"pid": 41592, "status": "running", "process_identity": {"created_at": 100, "executable": "python"}}
    path = tmp_path / "task.json"
    if layout == "dir":
        (tmp_path / "task").mkdir()
        path = tmp_path / "task/meta.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    actual = tasks.get_task("task")
    assert actual["status"] == "unknown"
    assert "PID_IDENTITY_MISMATCH" in actual["error"]


def test_authoritative_exit_beats_live_reused_pid(tmp_path, monkeypatch):
    from wqb.workflow import tasks
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path))
    monkeypatch.setattr(tasks, "_pid_alive", lambda pid: True)
    monkeypatch.setattr(tasks, "process_identity", lambda pid: {"created_at": 200})
    d = tmp_path / "task"
    d.mkdir()
    (d / "meta.json").write_text(json.dumps({"pid": 1, "returncode": 7,
        "process_identity": {"created_at": 100}}), encoding="utf-8")
    assert tasks.get_task("task")["status"] == "failed"


def test_salvage_exact_alpha_provenance_and_no_mutation():
    from wqb.research.salvage_provenance import resolve_salvage_entries
    c = sqlite3.connect(":memory:")
    for table in ("backtest_results", "expressions"):
        c.execute(f"CREATE TABLE {table}(region TEXT,alpha_id TEXT,dataset TEXT)")
    c.executemany("INSERT INTO backtest_results VALUES(?,?,?)", [
        ("EUR", "a", "fundamental23"), ("EUR", "b", "news46"),
        ("USA", "c", "other1"), ("EUR", "d", "news50"), ("EUR", "d", "fundamental23")])
    original = [{"alpha_id": "a", "dataset": "stale"}, {"alpha_id": "b"},
                {"alpha_id": "c"}, {"alpha_id": "d"}]
    rows = resolve_salvage_entries(c, "EUR", original)
    assert rows[0]["dataset"] == "fundamental23"
    assert rows[1]["dataset"] == "news46"
    assert rows[2]["datasets"] == []
    assert rows[3]["datasets"] == ["fundamental23", "news50"]
    assert original[0]["dataset"] == "stale"
    c.close()


def test_salvage_exclusion_requires_known_independent_sources(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("efficiency_db_mcp", REPO / "wqb_db_mcp.py")
    db_mcp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(db_mcp)
    path = tmp_path / "provenance.db"
    c = sqlite3.connect(path)
    for table in ("backtest_results", "expressions"):
        c.execute(f"CREATE TABLE {table}(region TEXT,alpha_id TEXT,dataset TEXT)")
    c.executemany("INSERT INTO backtest_results VALUES(?,?,?)", [
        ("EUR", "a", "fundamental23"), ("EUR", "b", "news46"),
        ("EUR", "d", "news50"), ("EUR", "d", "fundamental23")])
    c.commit()
    c.close()
    monkeypatch.setattr(db_mcp, "_conn", lambda: sqlite3.connect(path))
    monkeypatch.setattr(db_mcp, "_get_ledger_raw", lambda *a: {
        "entries": [{"alpha_id": a, "sharpe": 1.5} for a in ("a", "b", "c", "d")]})
    result = db_mcp.get_salvage_pool("EUR", exclude_dataset="fundamental23")
    assert [e["alpha_id"] for e in result["entries"]] == ["b"]
    assert result["excluded_unknown_provenance"] == 1
