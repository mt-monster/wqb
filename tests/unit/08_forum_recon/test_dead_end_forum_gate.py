"""
Unit tests for _forum_recon_gate fail-closed (HEAD reviewed 4-param interface).

Tests cover:
  1. require=False (waive) → {"ok": True, "trace": {"decision": "waived"}}
  2. require=True, no evidence → {"ok": False, "verdict": {"code": "recon_missing"}}
  3. require=True, evidence has "found": True → {"ok": False, "verdict": {"code": "recon_found"}}
  4. require=True, evidence has "error" → {"ok": False, "verdict": {"code": "recon_error"}}
  5. require=True, valid negative evidence + ledger record → {"ok": True}
  6. require=True, evidence passes but ledger not found → {"ok": False, "verdict": {"code": "recon_not_in_ledger"}}
  7. require=True, evidence passes but ledger says "found" → {"ok": False, "verdict": {"code": "recon_ledger_found"}}
  8. require=True, force_seal=True overrides → {"ok": True, "trace": {"decision": "forced"}}
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_WQB_DB_MCP = _REPO_ROOT / "wqb_db_mcp.py"
_WQB_SRC = _REPO_ROOT / "src" / "wqb"


def _load_db_mcp():
    spec = importlib.util.spec_from_file_location("wqb_db_mcp_test", _WQB_DB_MCP)
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("wqb_db_mcp_test", mod)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(autouse=True)
def _ensure_wqb_src_on_path(monkeypatch):
    monkeypatch.setattr(sys, "path", [_WQB_SRC, *sys.path])


def _ledger_with(*records):
    """Return a fake _get_ledger_raw that matches records by (region, key).

    The key parameter passed by resolve_outcome is the FULL ledger key
    (e.g. "forum_recon_negative_q_123"), not the bare qkey.
    """
    def fake_get(region, key):
        for r in records:
            if r.get("region") == region and r.get("key") == key:
                return r
        return None
    return fake_get


@pytest.mark.parametrize("payload,evidence_hint", [
    ({}, None),
    ({"payload": {}}, None),
    ({"forum_recon": None}, None),
    (None, None),
])
def test_gate_waives_when_require_false(payload, evidence_hint):
    """require=False (waive) → ok=True, decision=waived, no evidence."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig("TEST", payload, evidence_hint, False, require_forum_recon=False)
    assert result["ok"] is True
    assert result["trace"]["decision"] == "waived"


def test_gate_blocks_when_no_evidence(monkeypatch):
    """require=True, no evidence → ok=False, code=recon_missing."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig("TEST", {}, None, False, require_forum_recon=True)
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_missing"


def test_gate_blocks_when_forum_has_solution(monkeypatch):
    """require=True, evidence has 'found': True → ok=False, code=recon_found."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": True, "solution": "X"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_found"


def test_gate_blocks_on_tool_error(monkeypatch):
    """require=True, evidence has 'error' → ok=False, code=recon_error."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"error": "timeout", "found": False}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_error"


def test_gate_distinguishes_false_from_none(monkeypatch):
    """require=True: None is 'recon_missing'; {'found': False} without key is 'recon_no_question_key'."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate

    # None evidence
    result = orig("TEST", {"forum_recon": None}, None, False, require_forum_recon=True)
    assert result["verdict"]["code"] == "recon_missing"

    # {"found": False} without question_key → recon_no_question_key
    result = orig("TEST", {"forum_recon": {"found": False}}, None, False, require_forum_recon=True)
    assert result["verdict"]["code"] == "recon_no_question_key"

    # {} vs {"forum_recon": {}} both yield recon_missing
    result_dict = orig("TEST", {}, None, False, require_forum_recon=True)
    result_nested = orig("TEST", {"forum_recon": {}}, None, False, require_forum_recon=True)
    assert result_dict["verdict"]["code"] == "recon_missing"
    assert result_nested["verdict"]["code"] == "recon_missing"


def test_gate_forces_when_force_seal(monkeypatch):
    """require=True, force_seal=True → ok=True even when evidence says found=True."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": True, "solution": "X"}},
        None,
        True,
        require_forum_recon=True,
    )
    assert result["ok"] is True
    assert result["trace"]["decision"] == "forced"
    assert result["trace"]["overridden_code"] == "recon_found"


def test_gate_blocks_when_no_key(monkeypatch):
    """require=True, evidence lacks 'question_key' → ok=False, code=recon_no_question_key."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": False, "question": "q"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_no_question_key"


def test_gate_blocks_when_non_dict_evidence(monkeypatch):
    """require=True, evidence is not a dict → ok=False, code=recon_not_a_record."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": "some string"},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_not_a_record"


def test_gate_blocks_when_unknown_kind(monkeypatch):
    """require=True, evidence has no 'found' key → ok=False, code=recon_unknown."""
    mod = _load_db_mcp()
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"foo": "bar"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_unknown"


def test_gate_allows_with_ledger_negative(monkeypatch):
    """require=True, valid negative evidence + ledger has matching negative → ok=True."""
    mod = _load_db_mcp()
    monkeypatch.setattr(mod, "_get_ledger_raw", _ledger_with({
        "region": "TEST",
        "key": "forum_recon_negative_q_123",
        "forum_recon": {"found": False, "searched_at": "2026-09-30T00:00:00", "question": "q"},
    }))
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": False, "question_key": "q_123", "searched_at": "2026-09-30T00:00:00", "question": "q"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is True
    assert result["trace"]["decision"] == "verified"


def test_gate_blocks_when_ledger_missing(monkeypatch):
    """require=True, evidence passes but ledger has no record → ok=False, code=recon_not_in_ledger."""
    mod = _load_db_mcp()
    monkeypatch.setattr(mod, "_get_ledger_raw", _ledger_with())
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": False, "question_key": "q_123", "searched_at": "2026-09-30T00:00:00", "question": "q"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_not_in_ledger"


def test_gate_blocks_when_ledger_has_found(monkeypatch):
    """require=True, evidence passes but ledger says 'found' → ok=False, code=recon_ledger_found."""
    mod = _load_db_mcp()
    monkeypatch.setattr(mod, "_get_ledger_raw", _ledger_with({
        "region": "TEST",
        "key": "forum_recon_q_123",
        "forum_recon": {"found": True, "solution": "X", "searched_at": "2026-09-30T00:00:00", "question": "q"},
    }))
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": False, "question_key": "q_123", "searched_at": "2026-09-30T00:00:00", "question": "q"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_ledger_found"


def test_gate_blocks_when_ledger_has_error(monkeypatch):
    """require=True, evidence passes but ledger says 'error' → ok=False, code=recon_ledger_error."""
    mod = _load_db_mcp()
    monkeypatch.setattr(mod, "_get_ledger_raw", _ledger_with({
        "region": "TEST",
        "key": "forum_recon_error_q_123",
        "forum_recon": {"error": "tool_error", "searched_at": "2026-09-30T00:00:00", "question": "q"},
    }))
    orig = mod._forum_recon_gate
    result = orig(
        "TEST",
        {"forum_recon": {"found": False, "question_key": "q_123", "searched_at": "2026-09-30T00:00:00", "question": "q"}},
        None,
        False,
        require_forum_recon=True,
    )
    assert result["ok"] is False
    assert result["verdict"]["code"] == "recon_ledger_error"


def test_gate_passes_forum_recon_keyword(monkeypatch):
    """forum_recon parameter is extracted from payload and passed to verify_evidence."""
    mod = _load_db_mcp()
    monkeypatch.setattr(mod, "_get_ledger_raw", _ledger_with({
        "region": "TEST",
        "key": "forum_recon_negative_q_123",
        "forum_recon": {"found": False, "searched_at": "2026-09-30T00:00:00", "question": "q"},
    }))
    orig = mod._forum_recon_gate
    evidence = {"found": False, "question_key": "q_123", "searched_at": "2026-09-30T00:00:00", "question": "q"}
    result = orig("TEST", {"forum_recon": evidence}, evidence, False, require_forum_recon=True)
    assert result["ok"] is True
    assert result["evidence"]["question_key"] == "q_123"
