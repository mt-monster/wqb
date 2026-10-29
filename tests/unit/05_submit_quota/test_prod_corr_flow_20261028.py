# -*- coding: utf-8 -*-
"""prod 相关性主流程三层（2026-10-28 P0-1 / P0-2 / P1-1 / P2-9）的离线守卫。

被测对象 = ``brain_mixin_spcread``（``get_production_correlation`` /
``_poll_production_correlation`` / ``_corr_release_plan``）与
``brain_mixin_correlation.check_correlation`` 的透传面。全部用壳实例 + 桩
（``__new__``），**不联网、不写生产库、不碰仓库 logs/_dblock**。

三层语义（14h 日志实证，见 ``reports/prod_corr_timing_20261028.md``）：

1. **冷却按结果分流**（P0-1）：success → 只留 ``settle``（5s）；pending → 平台
   Retry-After 或 195s；4xx 终态 / 异常 → **不写**。旧版无条件 195s，且 busy
   路径也会续期（``slot()`` 的 ``release(None)``），吞吐被压到 ~4 alpha/小时。
2. **inflight 侧车**（P0-2）：开轮询即标记；同 alpha（非 refresh）在 TTL 内
   只预读等待、**不二次触发**；pending 保留标记（平台仍在算）、其余结果清除。
3. **同 alpha 等待**（P1-1）：锁被他进程占着但 holder 恰是同一 alpha ⇒ 等预读
   结果而不是立即 busy；refresh 保持 fail-fast（终验要的是新算的值）。
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from brain_api import BrainApiClient  # noqa: E402
from wqb import corr_timing as ct  # noqa: E402
from wqb import correlation_slot as cs  # noqa: E402


def _shell(*, busy_retry_after: int = 180) -> BrainApiClient:
    c = BrainApiClient.__new__(BrainApiClient)
    c.base_url = "https://api.worldquantbrain.com"
    c._brain_correlation_local_lock = asyncio.Lock()
    c._brain_correlation_busy_retry_after_seconds = busy_retry_after
    c._logs: list = []
    c.log = lambda msg, level="INFO": c._logs.append(str(msg))
    return c


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    """锁目录指到 tmp；sleep 归零；join 窗口默认 0（要等的用例自己调大）。"""
    d = tmp_path / "_dblock"
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    monkeypatch.setenv("WQB_CORR_JOIN_WAIT_SEC", "0")
    monkeypatch.delenv("WQB_CORR_SETTLE_SEC", raising=False)

    async def _fast(_s):
        return None
    monkeypatch.setattr(asyncio, "sleep", _fast)
    return d


class _FakeResponse:
    def __init__(self, status_code=200, body=None, text="", headers=None):
        self.status_code = status_code
        self._body = body if body is not None else {}
        self.text = text if text else (json.dumps(self._body) if self._body else "")
        self.headers = headers or {}

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError(f"HTTP {self.status_code}", response=self)


def _stub_common(c, *, lock=None, poll=None, read=None, release_calls=None):
    async def _auth():
        return None
    c.ensure_authenticated = _auth
    if read is None:
        async def read(_aid, quiet=False):
            return None
    c._read_existing_prod_correlation = read
    if lock is None:
        async def lock(_op):
            return {"acquired": True, "backend": "file",
                    "lock_key": "k", "lock_token": "k"}
    c._try_acquire_brain_correlation_lock = lock
    calls = release_calls if release_calls is not None else []
    async def _release(info, op, *, cooldown=True, seconds=None):
        calls.append({"cooldown": cooldown, "seconds": seconds})
    c._release_brain_correlation_lock = _release
    if poll is None:
        async def poll(_aid, _mw=None):
            return {"status": "ok", "max": 0.3, "records": []}
    if poll is not False:  # False = 保留真实轮询实现（打点断言需要）
        c._poll_production_correlation = poll
    return calls


# ---------------------------------------------------------------- P0-1 冷却分流
class TestReleasePlan:
    def test_success_uses_settle_seconds(self, _env, monkeypatch):
        c = _shell()
        monkeypatch.setenv("WQB_CORR_SETTLE_SEC", "2")
        assert c._corr_release_plan({"status": "ok", "max": 0.3}) == (True, 2.0)

    def test_pending_uses_platform_retry_after(self, _env):
        c = _shell()
        assert c._corr_release_plan({"status": "pending",
                                     "platform_retry_after": 42}) == (True, 42.0)

    def test_pending_without_retry_after_uses_default(self, _env):
        c = _shell()
        assert c._corr_release_plan({"status": "pending"}) == (True, None)

    def test_pending_with_absurd_retry_after_falls_back(self, _env):
        c = _shell()
        assert c._corr_release_plan({"status": "pending",
                                     "platform_retry_after": 99999}) == (True, None)

    @pytest.mark.parametrize("result", [
        {"status": "data_unavailable", "http_status": 403},
        {"status": "correlation_busy"},
        None,
        {},
    ])
    def test_non_outcomes_write_no_cooldown(self, _env, result):
        c = _shell()
        assert c._corr_release_plan(result) == (False, None)


class TestReleaseWiring:
    def test_pre_read_hit_never_locks_or_cools_down(self, _env, tmp_path):
        c = _shell()
        calls = _stub_common(c, read=None)

        async def _read(_aid, quiet=False):
            return {"status": "ok", "max": 0.55, "records": [],
                    "source": "alpha_detail_cached", "alpha_id": "TGT"}

        async def _lock(_op):
            pytest.fail("预读命中不得抢槽")
        c._read_existing_prod_correlation = _read
        c._try_acquire_brain_correlation_lock = _lock

        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["source"] == "alpha_detail_cached" and r["max"] == 0.55
        assert calls == []
        assert cs.cooldown_remaining() == 0.0

    def test_success_release_uses_settle_and_clears_inflight(self, _env):
        c = _shell()
        seen_inflight: list = []

        async def _poll(_aid, _mw=None):
            seen_inflight.append(bool(cs.inflight_get("TGT")))
            return {"status": "ok", "max": 0.31, "records": []}

        calls = _stub_common(c, poll=_poll)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["status"] == "ok"
        assert seen_inflight == [True], "开轮询时必须先标记 inflight"
        assert calls and calls[0]["cooldown"] is True
        assert calls[0]["seconds"] == pytest.approx(cs.settle_seconds())
        assert cs.inflight_get("TGT") == {}, "已决结果必须清除 inflight 标记"

    def test_pending_keeps_inflight_and_reports_written_cooldown(self, _env):
        c = _shell()
        calls = _stub_common(c, poll=lambda *a, **k: _async_ret({
            "status": "pending", "message": "still computing",
            "attempts": 3, "elapsed_ms": 120000}))
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["status"] == "pending"
        assert calls[0]["cooldown"] is True and calls[0]["seconds"] is None
        assert r["retry_after"] == pytest.approx(cs.COOLDOWN_SEC_DEFAULT)
        assert r["inflight"] is True
        assert cs.inflight_get("TGT"), "pending 保留 inflight（平台仍在算）"

    def test_pending_honors_platform_retry_after(self, _env):
        c = _shell()
        calls = _stub_common(c, poll=lambda *a, **k: _async_ret({
            "status": "pending", "attempts": 2, "elapsed_ms": 120000,
            "platform_retry_after": 42}))
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert calls[0]["seconds"] == 42.0
        assert r["retry_after"] == 42

    def test_terminal_4xx_clears_inflight_without_cooldown(self, _env):
        c = _shell()
        calls = _stub_common(c, poll=lambda *a, **k: _async_ret({
            "status": "data_unavailable", "http_status": 403}))
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["status"] == "data_unavailable"
        assert calls[0]["cooldown"] is False and calls[0]["seconds"] is None
        assert cs.inflight_get("TGT") == {}
        assert "retry_after" not in r


# ---------------------------------------------------------------- P1-1 busy / join
class TestBusyAndJoin:
    def test_busy_other_alpha_fails_fast(self, _env):
        c = _shell(busy_retry_after=180)

        async def _lock(_op):
            return {"acquired": False, "backend": "file", "cooldown": False,
                    "holder": "corr:get_production_correlation(OTHER)",
                    "retry_after": None}

        async def _poll(*a, **k):
            pytest.fail("抢不到槽不得触发平台计算")
        calls = _stub_common(c, lock=_lock, poll=_poll)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["status"] == "correlation_busy"
        assert r["retry_after"] == 180
        assert r["holder"] == "corr:get_production_correlation(OTHER)"
        assert calls == []  # 没拿到槽 ⇒ 不能 release（更不能再写冷却）

    def test_busy_passes_through_cooldown_remaining(self, _env):
        c = _shell()

        async def _lock(_op):
            return {"acquired": False, "backend": "file", "cooldown": True,
                    "holder": None, "retry_after": 12}
        _stub_common(c, lock=_lock)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["retry_after"] == 12 and r["cooldown"] is True

    def test_same_alpha_holder_joins_instead_of_busy(self, _env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_JOIN_WAIT_SEC", "5")
        c = _shell()
        seq = [None, {"status": "ok", "max": 0.44, "records": [],
                      "source": "alpha_detail_cached", "alpha_id": "TGT"}]

        async def _read(_aid, quiet=False):
            return seq.pop(0) if seq else seq

        async def _lock(op):
            return {"acquired": False, "backend": "file",
                    "holder": f"corr:{op}", "retry_after": None, "cooldown": False}

        async def _poll(*a, **k):
            pytest.fail("同 alpha 等待拿到值后不得再触发计算")
        calls = _stub_common(c, lock=_lock, poll=_poll, read=_read)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["max"] == 0.44 and r.get("joined") is True
        assert r["source"] == "alpha_detail_cached"
        assert calls == []
        assert any("same_alpha_join" in ln for ln in c._logs)

    def test_same_alpha_wait_timeout_falls_back_to_busy(self, _env):
        c = _shell()

        async def _lock(op):
            return {"acquired": False, "backend": "file",
                    "holder": f"corr:{op}", "retry_after": None, "cooldown": False}
        _stub_common(c, lock=_lock)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["status"] == "correlation_busy"
        assert any("same_alpha_wait_timeout" in ln for ln in c._logs)

    def test_refresh_does_not_join_same_alpha(self, _env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_JOIN_WAIT_SEC", "5")
        c = _shell()
        reads: list = []

        async def _read(_aid, quiet=False):
            reads.append(1)
            return {"status": "ok", "max": 0.44, "records": []}

        async def _lock(op):
            return {"acquired": False, "backend": "file",
                    "holder": f"corr:{op}", "retry_after": None, "cooldown": False}
        _stub_common(c, lock=_lock, read=_read)
        r = asyncio.run(c.get_production_correlation("TGT", use_pre_read=False))
        assert r["status"] == "correlation_busy"
        assert reads == [], "refresh 是终验语义：不得拿别人正在算的旧结果"


# ---------------------------------------------------------------- P0-2 inflight
class TestInflightShortCircuit:
    def test_inflight_marker_blocks_retrigger(self, _env):
        cs.inflight_mark("TGT")
        c = _shell()

        async def _lock(_op):
            pytest.fail("inflight 命中不得再抢槽")
        _stub_common(c, lock=_lock)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["status"] == "correlation_busy"
        assert r["inflight"] is True
        assert r["retry_after"] == 30
        assert cs.inflight_get("TGT"), "被挡住时不得清掉在飞标记"

    def test_inflight_join_returns_value(self, _env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_JOIN_WAIT_SEC", "5")
        cs.inflight_mark("TGT")
        c = _shell()
        seq = [None, {"status": "ok", "max": 0.39, "records": [],
                      "source": "alpha_detail_cached", "alpha_id": "TGT"}]

        async def _read(_aid, quiet=False):
            return seq.pop(0) if seq else seq
        _stub_common(c, read=_read)
        r = asyncio.run(c.get_production_correlation("TGT"))
        assert r["max"] == 0.39 and r.get("joined") is True
        assert any("inflight_join" in ln for ln in c._logs)

    def test_refresh_ignores_inflight_marker(self, _env):
        cs.inflight_mark("TGT")
        c = _shell()
        polled = []

        async def _poll(_aid, _mw=None):
            polled.append(1)
            return {"status": "ok", "max": 0.2, "records": []}
        _stub_common(c, poll=_poll)
        r = asyncio.run(c.get_production_correlation("TGT", use_pre_read=False))
        assert r["status"] == "ok" and polled == [1]


# ---------------------------------------------------------------- 打点与轮询
class TestTimingInstrumentation:
    def test_timing_lines_parse_and_use_declared_fields(self, _env):
        c = _shell()
        # 保留真实 _poll_production_correlation：success 打点在轮询体里（P2-8）
        calls = _stub_common(c, poll=False)

        async def _req(method, url, **kw):
            return _FakeResponse(200, {"max": 0.3, "records": []})
        c._request = _req
        asyncio.run(c.get_production_correlation("TGT"))
        assert calls  # 走完一轮，锁已按结果释放
        lines = [ln for ln in c._logs if ct.MARKER in ln]
        assert lines, "成功路径必须打 [corr-t] 点"
        recs = [ct.parse_line(ln) for ln in lines]
        assert all(r is not None for r in recs), lines
        success = [r for r in recs if r["event"] == "success"]
        assert success, [r["event"] for r in recs]
        r = success[0]
        assert r["alpha"] == "TGT" and r["status"] == "ok"
        assert r["max"] == 0.3 and r["source"] == "platform_poll"
        assert isinstance(r["elapsed_ms"], int) and r["ts"]
        unknown = {k for rec in recs for k in rec} - set(ct.FIELDS)
        assert not unknown, f"打点字段未在 wqb.corr_timing.FIELDS 声明：{sorted(unknown)}"

    def test_poll_captures_retry_after_and_meta(self, _env):
        c = _shell()
        responses = [
            _FakeResponse(200, text="", headers={"Retry-After": "7"}),
            _FakeResponse(200, {"max": 0.4, "records": [[0.0, 0.1, 2]]}),
        ]

        async def _req(method, url, **kw):
            return responses.pop(0)
        c._request = _req
        r = asyncio.run(c._poll_production_correlation("TGT", max_wait_seconds=30))
        assert r["status"] == "ok" and r["max"] == 0.4
        assert r["attempts"] == 2
        assert r["computed"] is True, "见过空体 ⇒ 确实触发了一次平台计算"
        assert r["platform_retry_after"] == 7.0

    def test_poll_ignores_absurd_retry_after(self, _env):
        c = _shell()
        responses = [
            _FakeResponse(200, text="", headers={"Retry-After": "600"}),
            _FakeResponse(200, {"max": 0.4, "records": []}),
        ]

        async def _req(method, url, **kw):
            return responses.pop(0)
        c._request = _req
        r = asyncio.run(c._poll_production_correlation("TGT", max_wait_seconds=30))
        assert "platform_retry_after" not in r, ">30s 的 Retry-After 不该当轮询间隔用"

    def test_poll_terminal_4xx_returns_immediately(self, _env):
        c = _shell()
        calls: list = []

        async def _req(method, url, **kw):
            calls.append(url)
            return _FakeResponse(403, {})
        c._request = _req
        r = asyncio.run(c._poll_production_correlation("TGT", max_wait_seconds=120))
        assert r["status"] == "data_unavailable" and r["http_status"] == 403
        assert len(calls) == 1, "4xx 是终态：不得在持锁状态下重试满整个窗口"

    def test_poll_zero_window_reports_pending_without_trigger(self, _env):
        c = _shell()

        async def _req(method, url, **kw):
            pytest.fail("窗口为 0 时不应再打平台")
        c._request = _req
        r = asyncio.run(c._poll_production_correlation("TGT", max_wait_seconds=0))
        assert r["status"] == "pending" and r["computed"] is False


# ---------------------------------------------------------------- check_correlation 透传
class TestCheckCorrelationSurfacing:
    def _shell_check(self, prod_result):
        c = _shell()
        c._prod_corr_store = lambda *a, **k: None
        c._prod_corr_cached = lambda aid: None
        c._prod_corr_last_known = lambda aid: {"max": 0.9, "age_hours": 30,
                                               "stale": True, "source": "alphas"}

        async def _auth():
            return None
        c.ensure_authenticated = _auth

        async def _prod(aid, max_wait_seconds=None, use_pre_read=True):
            return prod_result
        c.get_production_correlation = _prod
        return c

    def test_pending_surfaces_retry_after_inflight_last_known(self):
        c = self._shell_check({"status": "pending", "message": "m",
                               "retry_after": 195, "inflight": True,
                               "attempts": 4, "elapsed_ms": 120000})
        r = asyncio.run(c.check_correlation("TGT", "production", 0.7))
        assert r["status"] == "pending"
        assert r["retry_after"] == 195 and r["inflight"] is True
        assert r["last_known"]["max"] == 0.9
        assert r["checks"]["production"]["attempts"] == 4

    def test_busy_surfaces_holder_and_inflight(self):
        c = self._shell_check({"status": "correlation_busy", "message": "b",
                               "retry_after": 30, "inflight": True,
                               "holder": "corr:x"})
        r = asyncio.run(c.check_correlation("TGT", "production", 0.7))
        assert r["status"] == "correlation_busy"
        assert r["checks"]["production"]["holder"] == "corr:x"

    def test_preread_marks_provisional(self):
        c = self._shell_check({"status": "ok", "max": 0.5, "records": [],
                               "source": "alpha_detail_cached", "alpha_id": "TGT"})
        r = asyncio.run(c.check_correlation("TGT", "production", 0.7))
        assert r["provisional"] is True
        assert r["checks"]["production"]["provisional"] is True
        assert r["all_passed"] is True

    def test_slim_surfaces_inflight(self):
        mcp_core = pytest.importorskip("mcp_core")
        busy = {
            "alpha_id": "TGT", "threshold": 0.7, "correlation_type": "production",
            "checks": {"production": {"max_correlation": None, "passes_check": None,
                                      "status": "correlation_busy",
                                      "inflight": True, "retry_after": 30}},
            "all_passed": None, "status": "correlation_busy",
            "retry_after": 30, "inflight": True,
        }
        out = mcp_core._slim_check_correlation(busy)
        assert out["inflight"] is True
        assert out["checks"]["production"]["inflight"] is True


# ---------------------------------------------------------------- 工具
async def _async_ret(value):
    return value
