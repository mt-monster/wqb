# -*- coding: utf-8 -*-
"""2026-09-21：`tools_sim.harvest_multisim_alphas` 的 8 路并行 GET 遇瞬断（SSL EOF / 非 200）
必须重试，而不是把该 child 吞成 error 行（code 为空 → 入库时静默跳过）。
实证：ASI s2_aea_gated2_d1 波 8 条 COMPLETE，首次收批只落库 1 条，重跑才 8 条。"""
import asyncio
import sys
import types
from pathlib import Path

import pytest

pytest.importorskip("redis")  # tools_sim -> mcp_core -> brain_mixin_transport 需要 MCP venv 依赖；系统解释器下跳过

REPO_ROOT = Path(__file__).resolve().parents[3]
MCP_DIR = REPO_ROOT / "world-quant-brain-mcp"
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))


class _Resp:
    def __init__(self, code, payload):
        self.status_code = code
        self._p = payload

    def json(self):
        return self._p


class _FlakyClient:
    """每个 URL 第一次请求抛连接错误，第二次成功。"""
    base_url = "https://api.example"

    def __init__(self):
        self.calls = {}

    async def ensure_authenticated(self):
        pass

    def _response_payload(self, r):
        return {}

    async def _request(self, method, url, **kw):
        n = self.calls.get(url, 0) + 1
        self.calls[url] = n
        if n == 1:
            raise ConnectionError(f"Failed to connect to {url}")
        if url.endswith("/simulations/MS1"):
            return _Resp(200, {"children": ["c1", "c2"]})
        if "/simulations/c" in url:
            cid = url.rsplit("/", 1)[-1]
            return _Resp(200, {"alpha": f"A{cid}", "status": "COMPLETE",
                               "regular": {"code": f"rank(x_{cid})"}})
        if "/alphas/" in url:
            aid = url.rsplit("/", 1)[-1]
            return _Resp(200, {"id": aid, "regular": {"code": f"rank(x_{aid[1:]})"},
                               "is": {"sharpe": 2.0, "fitness": 1.2, "turnover": 0.1, "checks": []},
                               "settings": {}, "status": "UNSUBMITTED"})
        return _Resp(500, {})


@pytest.fixture
def tools_sim(monkeypatch):
    import tools_sim as ts  # noqa: PLC0415
    monkeypatch.setattr(ts, "brain_client", _FlakyClient())
    monkeypatch.setattr(asyncio, "sleep", _no_sleep)
    return ts


async def _no_sleep(_):
    return None


def test_harvest_retries_transient_failures_and_returns_codes(tools_sim):
    r = asyncio.run(tools_sim.harvest_multisim_alphas("https://api.example/simulations/MS1"))
    assert r.get("success") is True, r
    assert r["total"] == 2 and r["error_count"] == 0, r
    codes = sorted(a.get("expression") for a in r["alphas"])
    assert codes == ["rank(x_c1)", "rank(x_c2)"]  # regular 为 dict 时也归一成字符串
    assert all(a.get("alpha_id") for a in r["alphas"])


def test_get_with_retry_gives_up_on_hard_http_error(tools_sim):
    """404/401 这类硬错误不重试（避免放大 429 风险）。"""
    class _C(_FlakyClient):
        async def _request(self, method, url, **kw):
            self.calls[url] = self.calls.get(url, 0) + 1
            return _Resp(404, {})
    c = _C()
    tools_sim.brain_client = c
    r = asyncio.run(tools_sim.harvest_multisim_alphas("https://api.example/simulations/MS1"))
    assert "error" in r and "404" in str(r["error"])
    assert c.calls["https://api.example/simulations/MS1"] == 1
