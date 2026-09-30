# -*- coding: utf-8 -*-
"""submit_alpha 提交前置闸（P0）守护 —— 2026-09-29.

把 brain-alpha-robustness 的 Phase B.0 硬门（WebDataScope Failed RA/PPA==0）
与提交层四闸（LOW_SHARPE/LOW_FITNESS/LOW_2Y_SHARPE 的模拟层 WARNING）焊进提交路由，
从「靠 Agent 记得调 skill」升级为「不过闸就提交不出去」。

核心契约（fail-closed）：
  - 无法判定（非 dict / 无 is.checks）→ blocked，不放行；
  - 模拟层 FAIL / 硬闸 WARNING / Failed RA·PPA 非零 → blocked；
  - confirm_submit=True 且未声明 robustness_audited → blocked；
  - force=True 可绕过（留痕），保持「平台 403 零成本兜底」不变。
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest


# ---------------------------------------------------------------- _submit_gate 纯函数
@pytest.fixture
def gate():
    from wqb.workflow.nodes import submit_alpha as sa
    return sa._submit_gate


def _checks(*items):
    return {"is": {"checks": list(items)}}


def test_gate_passes_clean_checks(gate):
    r = gate(_checks({"name": "LOW_SHARPE", "result": "PASS", "value": 1.8, "limit": 1.58}))
    assert r["passed"] is True and r["blocked"] is False


def test_gate_blocks_on_sim_fail(gate):
    r = gate(_checks({"name": "LOW_FITNESS", "result": "FAIL", "value": 0.5, "limit": 1.0}))
    assert r["blocked"] is True
    assert any("FAIL" in s for s in r["blocked_reasons"])


def test_gate_blocks_on_hard_gate_warning(gate):
    # 模拟层 WARNING，但 LOW_SHARPE 在提交层是硬闸 FAIL
    r = gate(_checks({"name": "LOW_SHARPE", "result": "WARNING", "value": 1.5, "limit": 1.58}))
    assert r["blocked"] is True
    assert any("硬闸" in s for s in r["blocked_reasons"])


def test_gate_blocks_on_failed_ra_count(gate):
    # CONCENTRATED_WEIGHT 是 RA 资格门项，WARNING 即计失败（WebDataScope 口径）
    r = gate(_checks({"name": "CONCENTRATED_WEIGHT", "result": "WARNING", "value": 0.9}))
    assert r["blocked"] is True
    assert r["failed_ra"] == 1
    assert any("Phase B.0" in s for s in r["blocked_reasons"])


def test_gate_blocks_on_empty_checks_fail_closed(gate):
    # fail-closed：无 is.checks（回测未完成/预检失败）→ 阻断，不放行
    r = gate({"is": {}})
    assert r["blocked"] is True
    assert any("fail-closed" in s for s in r["blocked_reasons"])


def test_gate_blocks_on_non_dict_fail_closed(gate):
    r = gate(None)
    assert r["blocked"] is True
    assert any("非 dict" in s for s in r["blocked_reasons"])


def test_gate_ppa_uses_ppa_count(gate):
    # PPA 候选看 Failed PPA 计数，而非 RA
    r = gate({"type": "PPA", "is": {"checks": [
        {"name": "LOW_TURNOVER", "result": "WARNING", "value": 0.5},  # PPA 资格门项
    ]}})
    assert r["is_ppa"] is True
    assert r["failed_ppa"] == 1
    assert r["blocked"] is True


# ---------------------------------------------------------------- run() 集成
@pytest.fixture
def sa(monkeypatch):
    from wqb.workflow.nodes import submit_alpha as sa_mod
    return sa_mod


def _patch_client(monkeypatch, sa, details):
    monkeypatch.setattr(sa, "_get_brain_client", lambda: MagicMock())
    # details 兼作 submit 的返回：带 success=True 使 result["submitted"] 判定成立
    _d = dict(details) if isinstance(details, dict) else {"is": {}}
    _d.setdefault("success", True)
    monkeypatch.setattr(sa, "_run_async", lambda x, *a, **k: _d)
    # 避免走到提交后的 poll 轮询（180s）卡住单测
    monkeypatch.setattr(sa, "_poll_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(sa, "_current_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(sa, "_classify_submit_response", lambda *a, **k: "confirmed")


def test_run_gate_blocked_returns_without_submit(monkeypatch, sa):
    _patch_client(monkeypatch, sa, _checks(
        {"name": "LOW_FITNESS", "result": "FAIL", "value": 0.5, "limit": 1.0}))
    out = sa.run(alpha_id="X", confirm_submit=True)
    assert out["blocked"] is True
    assert "submit_gate" in out["reason"]
    assert out.get("submitted") is False


def test_run_robustness_not_audited_blocks_submit(monkeypatch, sa):
    # gate 通过，但未声明 robustness_audited → 提交被 fail-closed 拒绝
    _patch_client(monkeypatch, sa, _checks(
        {"name": "LOW_SHARPE", "result": "PASS", "value": 1.8, "limit": 1.58}))
    out = sa.run(alpha_id="X", confirm_submit=True, robustness_audited=False)
    assert out["blocked"] is True
    assert "robustness" in out["reason"]
    assert out.get("submitted") is False


def test_run_robustness_audited_allows_submit(monkeypatch, sa):
    _patch_client(monkeypatch, sa, _checks(
        {"name": "LOW_SHARPE", "result": "PASS", "value": 1.8, "limit": 1.58}))
    out = sa.run(alpha_id="X", confirm_submit=True, robustness_audited=True)
    assert out.get("blocked") is not True
    # 走到提交（mock 的 submit 返回 confirmed + poll ACTIVE）
    assert out.get("submitted") is True


def test_run_force_bypasses_gate_and_robustness(monkeypatch, sa):
    # force=True：gate FAIL + 未声明 robustness 均被绕过
    _patch_client(monkeypatch, sa, _checks(
        {"name": "LOW_FITNESS", "result": "FAIL", "value": 0.5, "limit": 1.0}))
    out = sa.run(alpha_id="X", confirm_submit=True, force=True)
    assert out.get("blocked") is not True


def test_run_precheck_mode_does_not_require_robustness(monkeypatch, sa):
    # confirm_submit=False（仅预检）：不强制 robustness 声明，正常返回状态
    _patch_client(monkeypatch, sa, _checks(
        {"name": "LOW_SHARPE", "result": "PASS", "value": 1.8, "limit": 1.58}))
    out = sa.run(alpha_id="X", confirm_submit=False, robustness_audited=False)
    assert out.get("blocked") is not True
    assert out.get("submitted") is False
    assert out.get("final_status") == "ACTIVE"
