# -*- coding: utf-8 -*-
"""2026-09-20：toolkit _lib/api.py 传输层必须对 HTTP 429 做退避重试。
ASI S1 实证：scan_fields.py 直接 api.get，一个 429 就让整个字段扫描崩溃 → catalog 缺失 → gate.py 必崩。"""
import io
import sys
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TK = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TK) not in sys.path:
    sys.path.insert(0, str(TK))

from _lib import api as tk_api  # noqa: E402


def _http_error(code, headers=None):
    return urllib.error.HTTPError("https://x", code, "msg", headers or {}, io.BytesIO(b""))


def test_429_is_retried_then_succeeds(monkeypatch):
    sleeps = []
    monkeypatch.setattr(tk_api.time, "sleep", lambda s: sleeps.append(s))
    calls = {"n": 0}

    def open_fn():
        calls["n"] += 1
        if calls["n"] < 3:
            raise _http_error(429)
        return "ok"

    assert tk_api._open_with_retry(open_fn, rate_base_delay=1) == "ok"
    assert calls["n"] == 3
    assert sleeps == [1, 2]


def test_non_429_http_error_raises_immediately(monkeypatch):
    monkeypatch.setattr(tk_api.time, "sleep", lambda s: None)
    calls = {"n": 0}

    def open_fn():
        calls["n"] += 1
        raise _http_error(400)

    try:
        tk_api._open_with_retry(open_fn)
    except urllib.error.HTTPError as e:
        assert e.code == 400
    else:
        raise AssertionError("400 must raise")
    assert calls["n"] == 1


def test_429_exhausts_after_rate_retries(monkeypatch):
    monkeypatch.setattr(tk_api.time, "sleep", lambda s: None)
    calls = {"n": 0}

    def open_fn():
        calls["n"] += 1
        raise _http_error(429)

    try:
        tk_api._open_with_retry(open_fn, rate_retries=3)
    except urllib.error.HTTPError as e:
        assert e.code == 429
    assert calls["n"] == 3
