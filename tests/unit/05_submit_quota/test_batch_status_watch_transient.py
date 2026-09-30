# -*- coding: utf-8 -*-
"""2026-09-21：tools/batch_status.py --watch 遇网络瞬断（transport 层抛 ConnectionError）
必须继续轮询而不是整个 watcher 崩溃（ASI mech_screen 批实证：两个 multisim 已 COMPLETE，
watcher 因一次 Failed to connect 退出，下游 harvest 收到 0 条）。"""
import asyncio
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


def _load():
    spec = importlib.util.spec_from_file_location("batch_status_mod2", REPO_ROOT / "tools" / "batch_status.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Resp:
    def __init__(self, payload):
        self.status_code = 200
        self._p = payload
        self.text = "x"

    def json(self):
        return self._p


class _FlakyBrain:
    """前 n_fail 次请求抛 ConnectionError，之后返回 COMPLETE 的单条 simulation。"""
    base_url = "https://api.example"

    def __init__(self, n_fail):
        self.n_fail = n_fail
        self.calls = 0

    async def ensure_authenticated(self):
        pass

    async def _request(self, method, url, **kw):
        self.calls += 1
        if self.calls <= self.n_fail:
            raise ConnectionError(f"Failed to connect to {url}")
        if url.endswith("/simulations/sim1"):  # multisim 父：展开一个子任务
            return _Resp({"children": ["child1"]})
        return _Resp({"status": "COMPLETE", "alpha": "abc12345", "is": {"sharpe": 2.0, "fitness": 1.2}})

    @staticmethod
    def _simulation_error_message(data):
        return ""


async def _no_sleep(_):
    return None


def test_watch_survives_transient_connection_error():
    mod = _load()
    brain = _FlakyBrain(n_fail=2)
    final, ok = asyncio.run(mod.watch_loop(brain, ["sim1"], watch=True, interval=0, max_waits=10, sleep=_no_sleep))
    assert ok is True
    assert brain.calls >= 3


def test_watch_gives_up_after_max_consecutive_failures():
    mod = _load()
    brain = _FlakyBrain(n_fail=100)
    with pytest.raises(ConnectionError):
        asyncio.run(mod.watch_loop(brain, ["sim1"], watch=True, interval=0, max_waits=50,
                                   sleep=_no_sleep, max_net_fail=3))
    assert brain.calls == 3


def test_no_watch_keeps_raising_immediately():
    mod = _load()
    brain = _FlakyBrain(n_fail=1)
    with pytest.raises(ConnectionError):
        asyncio.run(mod.watch_loop(brain, ["sim1"], watch=False, interval=0, max_waits=1, sleep=_no_sleep))


def test_non_transient_exception_propagates():
    mod = _load()

    class _Broken(_FlakyBrain):
        async def _request(self, method, url, **kw):
            raise ValueError("bad payload")

    with pytest.raises(ValueError):
        asyncio.run(mod.watch_loop(_Broken(0), ["sim1"], watch=True, interval=0, max_waits=5, sleep=_no_sleep))
