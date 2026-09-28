# -*- coding: utf-8 -*-
"""2026-09-21：tools/batch_status.py 必须在请求前确保已认证，并对 401 自动重认证一次。
实证：新进程无 JWT 时 batch_status 每条 HTTP 401，--watch 永远不终止（ASI Mode-A 批）。"""
import asyncio
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location("batch_status_mod", REPO_ROOT / "tools" / "batch_status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Resp:
    def __init__(self, code, payload=None):
        self.status_code = code
        self._p = payload or {}
        self.text = "x"

    def json(self):
        return self._p


class _Brain:
    base_url = "https://api.example"

    def __init__(self, codes):
        self.codes = list(codes)
        self.auth_calls = 0
        self._auth_validated_until = 0.0

    async def ensure_authenticated(self):
        self.auth_calls += 1

    async def _request(self, method, url, **kw):
        code = self.codes.pop(0)
        return _Resp(code, {"status": "COMPLETE", "alpha": "abc", "is": {"sharpe": 1.0}})

    def _simulation_error_message(self, data):
        return ""


def test_fetch_one_authenticates_first_and_retries_on_401():
    mod = _load()
    brain = _Brain([401, 200])
    out = asyncio.run(mod.fetch_one(brain, "https://api.example/simulations/x"))
    assert out.get("status") == "COMPLETE", out
    assert brain.auth_calls >= 2  # pre-request ensure + 401 refresh
    assert not brain.codes


def test_fetch_one_no_retry_when_200():
    mod = _load()
    brain = _Brain([200])
    out = asyncio.run(mod.fetch_one(brain, "https://api.example/simulations/x"))
    assert out.get("status") == "COMPLETE"
    assert brain.auth_calls == 1


def test_complete_children_count_as_terminal_and_not_error():
    mod = _load()

    class _B(_Brain):
        async def _request(self, method, url, **kw):
            if url.endswith("/simulations/parent"):
                return _Resp(200, {"children": ["c1", "c2"]})
            return _Resp(200, {"status": "COMPLETE", "alpha": "abc", "is": {"sharpe": 1.0}})

        def _simulation_error_message(self, data):
            return "COMPLETE"  # 平台把 status 字面量当 message 回传的形态

    brain = _B([])
    out = asyncio.run(mod.fetch_batch(brain, "parent"))
    assert out["terminal"] == 2 and out["all_terminal"] is True, out
    assert out["errors"] == 0, out


def test_warning_status_is_terminal():
    mod = _load()
    assert "WARNING" in mod.TERMINAL


def test_bare_fail_child_status_is_terminal():
    """2026-09-21：平台子模拟会返回裸 `FAIL`（非 FAILED）；父为 ERROR。
    ASI price_signal_dl 批 8 子全 FAIL，--watch 显示 0/8 terminal 永不退出。CLI 与 MCP 两处集合须同步。"""
    mod = _load()
    assert "FAIL" in mod.TERMINAL and "FAILED" in mod.TERMINAL
    src = (REPO_ROOT / "world-quant-brain-mcp" / "tools_ops.py").read_text(encoding="utf-8")
    line = [ln for ln in src.splitlines() if ln.strip().startswith("TERMINAL = {")][0]
    assert '"FAIL"' in line
