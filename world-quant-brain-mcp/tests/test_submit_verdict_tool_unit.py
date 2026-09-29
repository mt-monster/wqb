# -*- coding: utf-8 -*-
"""MCP submit_verdict 工具：走 wqb.submit_verdict_core 的薄包装（无网络，打桩 brain_client）。

契约（2026-09-29 X-2 整改）：
  - 已提交者短路，不发 GET /submit；
  - 未提交且提交层 404 → UNVERIFIABLE（exit_code 10，不是 0）；
  - 提交层 403 → BLOCKED；
  - 返回体带 exit_code / reason_code / next_step，且保留历史键。
"""
import asyncio
import os
import sys

MCP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.normpath(os.path.join(MCP_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import mcp_core  # noqa: E402,F401  先于 tools_ops 导入（同 test_tools_workflow_unit）
import tools_ops  # noqa: E402


class _Resp:
    def __init__(self, status, body=None):
        self.status_code = status
        self._body = body or {}
        self.text = "x" if body else ""

    def json(self):
        return self._body


class _StubClient:
    base_url = "https://api.example.invalid"

    def __init__(self, detail, submit_resp):
        self._detail, self._resp, self.requests = detail, submit_resp, []

    async def ensure_authenticated(self):
        return True

    async def get_alpha_details(self, alpha_id):
        return self._detail

    async def _request(self, method, url, **kw):
        self.requests.append((method, url))
        return self._resp


def _run(stub, alpha_id="A1"):
    orig = tools_ops.brain_client
    tools_ops.brain_client = stub
    try:
        fn = tools_ops.submit_verdict
        fn = getattr(fn, "fn", fn)          # FastMCP 装饰后可能包了一层
        return asyncio.run(fn(alpha_id))
    finally:
        tools_ops.brain_client = orig


def _detail(status="UNSUBMITTED", checks=None, **kw):
    d = {"status": status, "type": "REGULAR", "is": {"checks": checks or []}}
    d.update(kw)
    return d


def test_fresh_alpha_404_is_unverifiable_with_exit_code_10():
    stub = _StubClient(_detail(), _Resp(404))
    out = _run(stub)
    assert out["verdict"] == "UNVERIFIABLE" and out["exit_code"] == 10
    assert stub.requests == [("GET", "https://api.example.invalid/alphas/A1/submit")]
    assert "check_correlation" in out["next_step"]


def test_already_submitted_short_circuits_without_submit_layer_request():
    stub = _StubClient(_detail("ACTIVE"), _Resp(404))
    out = _run(stub)
    assert out["verdict"] == "ALREADY_SUBMITTED" and out["exit_code"] == 11
    assert stub.requests == []             # 不再对已提交者发 GET /submit


def test_403_blocks_with_check_names():
    stub = _StubClient(_detail(), _Resp(403, {"detail": ["PROD_CORRELATION"]}))
    out = _run(stub)
    assert out["verdict"] == "BLOCKED" and out["exit_code"] == 1
    assert out["reason_code"] == "SUBMIT_403:PROD_CORRELATION"


def test_failed_count_gate_blocks_and_keeps_legacy_keys():
    warn = {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "WARNING", "value": 0.2, "limit": 0.5}
    out = _run(_StubClient(_detail(checks=[warn]), _Resp(404)))
    assert out["verdict"] == "BLOCKED" and out["failed_ra"] == 1
    for k in ("sim_fails", "sim_warnings", "hard_gate_warnings", "failed_ra_items", "submit_status",
              "submit_checks", "submit_layer_view", "prepost_unverifiable", "is_ppa"):
        assert k in out, k


def test_exceptions_are_reported_not_raised():
    class Boom(_StubClient):
        async def get_alpha_details(self, alpha_id):
            raise RuntimeError("net down")
    out = _run(Boom({}, _Resp(404)))
    assert "submit_verdict failed" in out["error"]
