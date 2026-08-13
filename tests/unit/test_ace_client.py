"""ace_client (shared_libs) 单元测试 — tri-state 提交判定 + 配额估算 (无网络).

AceClient 通过 __new__ 构造 (绕过 __init__ 的登录), 注入 FakeSession/FakeResponse
脚本化响应, 验证:
- classify_check_pass 三态 (True/False/None)
- _read_verdict 四态 (PASS/FAIL/PENDING/CLEARED)
- get_submit_verdict 对 PENDING 异步检查的多轮轮询
- get_submission_quota 的 48h 窗口统计
- extract_max_correlation 递归提取
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

SKILLS_LIBS = Path.home() / ".zcode" / "skills" / "shared_libs"
if str(SKILLS_LIBS) not in sys.path:
    sys.path.insert(0, str(SKILLS_LIBS))

pytestmark = pytest.mark.skipif(
    not (SKILLS_LIBS / "ace_client.py").exists(),
    reason="shared_libs/ace_client.py 不存在 (skills 未注册)",
)

from ace_client import (  # noqa: E402
    AceClient,
    classify_check_pass,
    extract_max_correlation,
)


import json as _json


class FakeResponse:
    def __init__(self, status_code=200, payload=None, headers=None):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}
        self.headers = headers or {}
        # 真实响应 text 为 JSON 字符串 (ace_client 以 text 非空判定 body 存在)
        self.text = _json.dumps(self._payload)

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    """脚本化响应队列: 每次调用依次弹出响应。"""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def _next(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if not self.responses:
            return FakeResponse()
        return self.responses.pop(0)

    def get(self, url, params=None):
        return self._next("GET", url, params=params)

    def post(self, url, **kwargs):
        return self._next("POST", url, **kwargs)

    def request(self, method, url, **kwargs):
        return self._next(method, url, **kwargs)


def make_client(responses):
    client = AceClient.__new__(AceClient)
    client.base_url = "https://api.worldquantbrain.com"
    client.session = FakeSession(responses)
    return client


# ---------------------------------------------------------------------------
# classify_check_pass 三态
# ---------------------------------------------------------------------------

def test_classify_true_bool():
    assert classify_check_pass({"result": True}) is True


def test_classify_false_bool():
    assert classify_check_pass({"result": False}) is False


def test_classify_pass_string():
    assert classify_check_pass({"result": "PASS"}) is True


def test_classify_fail_string():
    assert classify_check_pass({"result": "failed"}) is False


def test_classify_pending_is_none():
    assert classify_check_pass({"result": "PENDING"}) is None


def test_classify_warning_is_none():
    assert classify_check_pass({"result": "warning"}) is None


def test_classify_unknown_key_is_none():
    assert classify_check_pass({"status": "whatever-unknown"}) is None


# ---------------------------------------------------------------------------
# _read_verdict 四态
# ---------------------------------------------------------------------------

def _verdict_payload(checks):
    return {"is": {"checks": checks}}


def test_read_verdict_pass():
    client = make_client([FakeResponse(200, _verdict_payload([{"name": "LOW_SHARPE", "result": "PASS"}]))])
    v = client._read_verdict("A", 201)
    assert v["verdict"] == "PASS" and v["final_success"] is True


def test_read_verdict_fail_403():
    client = make_client([FakeResponse(403, _verdict_payload([{"name": "LOW_2Y_SHARPE", "result": "FAIL"}]))])
    v = client._read_verdict("A", 201)
    assert v["verdict"] == "FAIL"
    assert "LOW_2Y_SHARPE" in v["failed_checks"]


def test_read_verdict_cleared_404():
    client = make_client([FakeResponse(404, {})])
    v = client._read_verdict("A", 201)
    assert v["verdict"] == "CLEARED" and v["final_success"] is False


def test_read_verdict_pending_async():
    # 200 但 PROD_CORRELATION 仍 PENDING → PENDING (异步未落定, 不可判成功)
    client = make_client([FakeResponse(200, _verdict_payload([
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "PROD_CORRELATION", "result": "PENDING"},
    ]))])
    v = client._read_verdict("A", 201)
    assert v["verdict"] == "PENDING" and v["final_success"] is False
    assert "PROD_CORRELATION" in v["pending_async_checks"]


def test_read_verdict_pending_nonasync_is_pass():
    # 非异步检查 (普通 warning 类) PENDING 不应阻塞判定
    client = make_client([FakeResponse(200, _verdict_payload([
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "SOME_OTHER", "result": "PENDING"},
    ]))])
    v = client._read_verdict("A", 201)
    assert v["verdict"] == "PASS"


# ---------------------------------------------------------------------------
# get_submit_verdict 多轮轮询 (qMNEG2Z2 教训: 首轮 200+PENDING 必须轮询)
# ---------------------------------------------------------------------------

def test_submit_verdict_polls_until_async_resolves():
    pending = FakeResponse(200, _verdict_payload([
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "PROD_CORRELATION", "result": "PENDING"},
    ]))
    passed = FakeResponse(200, _verdict_payload([{"name": "LOW_SHARPE", "result": "PASS"}]))
    # POST → 首轮 GET (pending) → 第二轮 GET (pass)
    client = make_client([FakeResponse(201, {}), pending, passed])
    v = client.get_submit_verdict("A", poll_rounds=3, poll_interval=0.0)
    assert v["final_success"] is True
    assert v["poll_rounds_used"] == 1


def test_submit_verdict_false_positive_guard():
    """首轮 200 误判成功的回归测试 (修复前 qMNEG2Z2 误报 PASS)。"""
    # 首轮 GET 返回 200 且 PROD_CORRELATION PENDING — 旧逻辑误判 success=True
    pending = FakeResponse(200, _verdict_payload([
        {"name": "LOW_SHARPE", "result": "PASS"},
        {"name": "PROD_CORRELATION", "result": "PENDING"},
    ]))
    rejected = FakeResponse(403, _verdict_payload([{"name": "PROD_CORRELATION", "result": "FAIL"}]))
    client = make_client([FakeResponse(201, {}), pending, rejected])
    v = client.get_submit_verdict("A", poll_rounds=3, poll_interval=0.0)
    assert v["final_success"] is False          # 不能把首轮 200 当成功
    assert "PROD_CORRELATION" in v["failed_checks"]


# ---------------------------------------------------------------------------
# get_submission_quota 48h 窗口
# ---------------------------------------------------------------------------

def _submitted(ago_hours, aid):
    return (aid, (datetime.now(timezone.utc) - timedelta(hours=ago_hours)).isoformat())


def test_quota_within_window():
    client = AceClient.__new__(AceClient)
    client.base_url = "x"
    client.get_user_alphas = lambda **kw: {"results": [
        {"id": a, "dateSubmitted": ts} for a, ts in [
            _submitted(1, "a1"), _submitted(20, "a2"), _submitted(60, "a3"),
        ]
    ]}
    q = client.get_submission_quota(window_hours=48, limit=4)
    assert q["used"] == 2          # 60h 前的 a3 不计
    assert q["remaining"] == 2
    assert q["hours_until_release"] is not None


def test_quota_exhausted():
    client = AceClient.__new__(AceClient)
    client.base_url = "x"
    client.get_user_alphas = lambda **kw: {"results": [
        {"id": a, "dateSubmitted": ts} for a, ts in [
            _submitted(1, "a1"), _submitted(2, "a2"), _submitted(3, "a3"), _submitted(4, "a4"),
        ]
    ]}
    q = client.get_submission_quota(window_hours=48, limit=4)
    assert q["remaining"] == 0


def test_quota_network_error_returns_error_key():
    client = AceClient.__new__(AceClient)
    client.base_url = "x"

    def boom(**kw):
        raise ConnectionError("TLS 中断")

    client.get_user_alphas = boom
    q = client.get_submission_quota()
    assert "error" in q


# ---------------------------------------------------------------------------
# extract_max_correlation
# ---------------------------------------------------------------------------

def test_extract_max_correlation_nested():
    payload = {"results": [{"correlation": 0.62}, {"correlation": 0.839},
                           {"meta": {"max_corr": 0.3}}]}
    assert extract_max_correlation(payload) == 0.839


def test_extract_max_correlation_empty():
    assert extract_max_correlation({"a": [1, 2, 3]}) is None
