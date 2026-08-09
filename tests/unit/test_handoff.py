"""Unit tests for wqb.search.scheduler session pack generation and validation.

Covers:
- ``prepare_session_pack(materialize=False)`` returns correct path.
- ``prepare_session_pack(materialize=True)`` writes agent-brief.md + mcp-plan.json.
- ``validate_session_pack`` detects missing directory.
- ``validate_session_pack`` detects missing required files.
- ``validate_session_pack`` validates mcp-plan.json structure.
- ``validate_session_pack`` validates snapshot.results.json format.
- ``_render_agent_brief`` produces readable markdown.
"""

import json
import os

import pytest

from wqb.search.scheduler import Scheduler


@pytest.fixture
def scheduler(tmp_path):
    fm_file = str(tmp_path / "failure_memory.jsonl")
    return Scheduler(failure_memory_file=fm_file)


@pytest.fixture
def tmp_tracking(tmp_path):
    tracking_dir = tmp_path / "tracking"
    tracking_dir.mkdir()
    return str(tracking_dir)


# ---------------------------------------------------------------------------
# prepare_session_pack (non-materialized)
# ---------------------------------------------------------------------------

def test_prepare_session_pack_non_materialized_returns_path(scheduler):
    pack_dir = scheduler.prepare_session_pack("2026-04-22", materialize=False)
    assert "2026-04-22" in pack_dir
    assert "sessions" in pack_dir


# ---------------------------------------------------------------------------
# prepare_session_pack (materialized)
# ---------------------------------------------------------------------------

def test_prepare_session_pack_materialized_creates_files(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pack_dir = scheduler.prepare_session_pack("2026-04-22", materialize=True)
    assert os.path.isdir(pack_dir)
    assert os.path.exists(os.path.join(pack_dir, "agent-brief.md"))
    assert os.path.exists(os.path.join(pack_dir, "mcp-plan.json"))


def test_prepare_session_pack_mcp_plan_structure(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scheduler.prepare_session_pack("2026-04-22", materialize=True)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    mcp_path = os.path.join(pack_dir, "mcp-plan.json")
    with open(mcp_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    assert plan["date"] == "2026-04-22"
    assert "region" in plan
    assert "universe" in plan
    assert "budget" in plan
    assert "arms" in plan
    assert "neutralization_sweep" in plan
    assert "hard_rules" in plan
    assert "tool_order" in plan
    assert len(plan["tool_order"]) > 0


def test_prepare_session_pack_agent_brief_content(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scheduler.prepare_session_pack("2026-04-22", materialize=True)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    brief_path = os.path.join(pack_dir, "agent-brief.md")
    with open(brief_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "WQB Session Brief" in content
    assert "Neutralization Sweep" in content
    assert "Hard Rules" in content
    assert "Batch Sequence" in content


# ---------------------------------------------------------------------------
# validate_session_pack
# ---------------------------------------------------------------------------

def test_validate_session_pack_missing_directory(scheduler, tmp_path):
    result = scheduler.validate_session_pack(str(tmp_path / "nonexistent"))
    assert result["ok"] is False
    assert len(result["errors"]) > 0


def test_validate_session_pack_missing_files(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    os.makedirs(pack_dir, exist_ok=True)
    result = scheduler.validate_session_pack(pack_dir)
    assert result["ok"] is False
    assert any("Missing required file" in e for e in result["errors"])


def test_validate_session_pack_valid(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scheduler.prepare_session_pack("2026-04-22", materialize=True)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    # Write a valid snapshot.results.json to satisfy validation
    snapshot_path = os.path.join(pack_dir, "snapshot.results.json")
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"results": [{"expression": "rank(close)", "settings": {}, "result": {}}]}, f)
    result = scheduler.validate_session_pack(pack_dir)
    assert result["ok"] is True


def test_validate_session_pack_mcp_plan_missing_keys(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    os.makedirs(pack_dir, exist_ok=True)
    # Write an incomplete mcp-plan.json
    mcp_path = os.path.join(pack_dir, "mcp-plan.json")
    with open(mcp_path, "w", encoding="utf-8") as f:
        json.dump({"date": "2026-04-22"}, f)
    brief_path = os.path.join(pack_dir, "agent-brief.md")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write("# brief")
    # Write valid snapshot
    snapshot_path = os.path.join(pack_dir, "snapshot.results.json")
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"results": []}, f)
    result = scheduler.validate_session_pack(pack_dir)
    assert result["ok"] is False
    assert any("missing keys" in e for e in result["errors"])


def test_validate_session_pack_invalid_mcp_plan_json(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    os.makedirs(pack_dir, exist_ok=True)
    mcp_path = os.path.join(pack_dir, "mcp-plan.json")
    with open(mcp_path, "w", encoding="utf-8") as f:
        f.write("{invalid json")
    brief_path = os.path.join(pack_dir, "agent-brief.md")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write("# brief")
    snapshot_path = os.path.join(pack_dir, "snapshot.results.json")
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"results": []}, f)
    result = scheduler.validate_session_pack(pack_dir)
    assert result["ok"] is False
    assert any("not valid JSON" in e for e in result["errors"])


def test_validate_session_pack_snapshot_results_format(scheduler, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pack_dir = os.path.join("tracking", "sessions", "2026-04-22")
    os.makedirs(pack_dir, exist_ok=True)
    brief_path = os.path.join(pack_dir, "agent-brief.md")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write("# brief")
    # mcp-plan.json is valid
    mcp_path = os.path.join(pack_dir, "mcp-plan.json")
    with open(mcp_path, "w", encoding="utf-8") as f:
        json.dump({"date": "2026-04-22", "region": "USA", "universe": "TOP3000",
                    "budget": 100, "arms": [], "neutralization_sweep": []}, f)
    # snapshot.results.json has bad format (results is not a list)
    snapshot_path = os.path.join(pack_dir, "snapshot.results.json")
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump({"results": "not_a_list"}, f)
    result = scheduler.validate_session_pack(pack_dir)
    assert result["ok"] is False
    assert any("must be a list" in e for e in result["errors"])