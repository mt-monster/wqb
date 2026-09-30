# -*- coding: utf-8 -*-
"""2026-09-21：brain_mixin_auth 认证 POST 遇传输瞬断（SSL EOF 等）必须重试，而不是让整条命令
在发请求前崩掉（当天 xr-probe / submit_queue add / alpha_checks 共 4 次栽在 /authentication）。"""
import asyncio
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
MCP_DIR = REPO_ROOT / "world-quant-brain-mcp"
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

requests = pytest.importorskip("requests")


class _Resp:
    status_code = 201
    text = ""

    def json(self):
        return {}


class _Cookies(dict):
    def clear(self):
        super().clear()

    def get(self, k, default=None):
        return super().get(k, default)


class _Session:
    def __init__(self, n_fail):
        self.n_fail = n_fail
        self.calls = 0
        self.cookies = _Cookies({"t": "jwt"})
        self.auth = None
        self.headers = {}

    def request(self, method, url, **kw):
        self.calls += 1
        if self.calls <= self.n_fail:
            raise requests.exceptions.SSLError("EOF occurred in violation of protocol")
        return _Resp()


def _make_client(n_fail):
    import brain_mixin_auth as m  # noqa: PLC0415

    class C(m.BrainAuthMixin if hasattr(m, "BrainAuthMixin") else object):
        pass

    mixin = None
    for name in dir(m):
        obj = getattr(m, name)
        if isinstance(obj, type) and hasattr(obj, "_authenticate_unlocked"):
            mixin = obj
            break
    assert mixin is not None, "auth mixin not found"

    class Client(mixin):
        def __init__(self):
            self.session = _Session(n_fail)
            self._default_timeout_seconds = 5
            self._auth_check_ttl_seconds = 60
            self._auth_validated_until = 0.0
            self.auth_credentials = {"email": "e", "password": "p"}
            self.logs = []

        def log(self, msg, level="INFO"):
            self.logs.append((level, msg))

    return Client()


async def _no_sleep(_):
    return None


def test_auth_retries_transient_ssl_error(monkeypatch):
    monkeypatch.setattr(asyncio, "sleep", _no_sleep)
    c = _make_client(n_fail=2)
    r = asyncio.run(c._authenticate_unlocked("e", "p"))
    assert c.session.calls == 3
    assert (r or {}).get("status") == "authenticated"


def test_auth_gives_up_after_three_transient_failures(monkeypatch):
    monkeypatch.setattr(asyncio, "sleep", _no_sleep)
    c = _make_client(n_fail=10)
    with pytest.raises(requests.exceptions.SSLError):
        asyncio.run(c._authenticate_unlocked("e", "p"))
    assert c.session.calls == 3
