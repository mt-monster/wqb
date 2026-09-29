# -*- coding: utf-8 -*-
"""SUPER 的提交只走 super_build（内置 prod 闸），不经 submit_alpha 节点（skills 审查 SP-13 / T0-4）。

此前 SKILL 教的是 `workflow_submit_alpha(confirm_submit=True, force=True)` 连调两次：本节点没有 prod 闸，
`force=True` 还跳过本地预检，第一次通过的 POST 就是真提交——「prod ≥ 0.7 不提交」的用户铁律在该路径无强制。
现在节点在任何副作用（改属性 / POST）之前拒绝 SUPER 的 confirm_submit，`force` 也不能放行。
"""
import asyncio
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))

from wqb.workflow.nodes import submit_alpha as SA  # noqa: E402


class _FakeClient:
    """只记录被调用的方法；submit_alpha / set_alpha_properties 一旦被调用测试就该红。"""

    def __init__(self, alpha_type):
        self.alpha_type = alpha_type
        self.calls = []

    async def get_alpha_details(self, alpha_id):
        self.calls.append("get_alpha_details")
        return {"id": alpha_id, "type": self.alpha_type, "status": "UNSUBMITTED", "tags": [],
                "settings": {"region": "GLB"},
                "is": {"sharpe": 3.0, "fitness": 3.0, "margin": 0.01, "turnover": 0.1,
                       "returns": 0.2, "checks": []}}

    def pre_submit_check(self, details):
        return {"passed": True, "failures": [], "warnings": []}

    async def set_alpha_properties(self, *a, **k):
        self.calls.append("set_alpha_properties")
        return {}

    async def submit_alpha(self, alpha_id):
        self.calls.append("submit_alpha")
        return {"success": True, "reason": "IS checks passed", "status_code": 200, "checks": []}


def _run(monkeypatch, client, **kw):
    monkeypatch.setattr(SA, "_get_brain_client", lambda: client)
    monkeypatch.setattr(SA, "_run_async", lambda coro: asyncio.new_event_loop().run_until_complete(coro))
    monkeypatch.setattr(SA, "_poll_status", lambda c, aid, t: "ACTIVE")
    monkeypatch.setattr(SA, "_derive_tags", lambda *a, **k: [])
    monkeypatch.setattr(SA, "_retire_queue", lambda *a, **k: 0)
    return SA.run("A1", _context={"store": None}, **kw)


@pytest.mark.parametrize("force", [False, True])
def test_super_confirm_submit_is_refused_before_any_side_effect(monkeypatch, force):
    client = _FakeClient("SUPER")
    res = _run(monkeypatch, client, confirm_submit=True, force=force)
    assert res["submitted"] is False and res["success"] is False
    assert res["reason"] == "super_requires_super_build" and res["blocked"] is True
    assert "super_build.py submit" in res["error"] and "force=True" in res["error"]
    assert "submit_alpha" not in client.calls and "set_alpha_properties" not in client.calls


def test_super_precheck_only_is_still_allowed(monkeypatch):
    client = _FakeClient("SUPER")
    res = _run(monkeypatch, client, confirm_submit=False)
    assert res["success"] is True and res["submitted"] is False
    assert "submit_alpha" not in client.calls


def test_regular_confirm_submit_is_unchanged(monkeypatch):
    client = _FakeClient("REGULAR")
    res = _run(monkeypatch, client, confirm_submit=True)
    assert "submit_alpha" in client.calls and res["submitted"] is True


@pytest.mark.parametrize("bad", [None, "oops", {}, {"type": None}])
def test_alpha_type_helper_tolerates_odd_details(bad):
    assert SA._alpha_type(bad) == ""


def test_alpha_type_is_case_insensitive():
    assert SA._alpha_type({"type": " super "}) == "SUPER"
