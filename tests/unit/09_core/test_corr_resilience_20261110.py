# -*- coding: utf-8 -*-
"""2026-11-10 审查第三批：平台停摆熔断 / inflight 异常清理 / 可配置窗口 的守护测试。

背景（2026-11-09 夜 KOR 实测）：平台 prod 服务停摆时本地机制自我放大等待——
240s 轮询 → pending → 195s 冷却 + inflight 残留 300s → busy → 再 240s，
三颗 alpha 各空转 241s，无 cancel、无短路。
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO / "src", REPO / "world-quant-brain-mcp"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import correlation_slot as cs  # noqa: E402


@pytest.fixture()
def lock_env(tmp_path, monkeypatch):
    d = tmp_path / "_dblock"
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    monkeypatch.delenv("WQB_CORR_COOLDOWN_SEC", raising=False)
    monkeypatch.delenv("WQB_CORR_UNAVAILABLE_STREAK", raising=False)
    monkeypatch.delenv("WQB_CORR_UNAVAILABLE_SEC", raising=False)
    return d


def _run(coro):
    return asyncio.run(coro)


# ------------------------------------------------------------------ 熔断
def test_streak_below_threshold_does_not_trip(lock_env):
    cs.note_pending_streak("A1")
    cs.note_pending_streak("A2")
    assert cs.unavailable_remaining() == 0.0


def test_streak_at_threshold_trips_and_blocks_acquire(lock_env, monkeypatch):
    monkeypatch.setenv("WQB_CORR_UNAVAILABLE_STREAK", "3")
    monkeypatch.setenv("WQB_CORR_UNAVAILABLE_SEC", "120")
    for aid in ("A1", "A2", "A3"):
        cs.note_pending_streak(aid)
    rem = cs.unavailable_remaining()
    assert 110 <= rem <= 120
    info = cs.acquire("get_production_correlation(A4)")
    assert info["acquired"] is False and info["busy"] is True
    assert info.get("unavailable") is True
    assert info["retry_after"] > 0


def test_clear_unavailable_restores_service(lock_env, monkeypatch):
    monkeypatch.setenv("WQB_CORR_UNAVAILABLE_STREAK", "1")
    cs.note_pending_streak("A1")
    assert cs.unavailable_remaining() > 0
    cs.clear_unavailable()
    assert cs.unavailable_remaining() == 0.0
    cs.clear_unavailable()  # 幂等


def test_success_would_reset_streak_file(lock_env, monkeypatch):
    monkeypatch.setenv("WQB_CORR_UNAVAILABLE_STREAK", "5")
    cs.note_pending_streak("A1")
    cs.note_pending_streak("A2")
    cs.clear_unavailable()
    cs.note_pending_streak("A3")
    assert cs.unavailable_remaining() == 0.0, "清除后计数应从零重新累积"


# ------------------------------------------------------------------ sidecar 原子性
def test_inflight_semantics_unchanged_under_sidecar_lock(lock_env):
    assert cs.inflight_get("B1") == {}
    r1 = cs.inflight_mark("B1")
    r2 = cs.inflight_mark("B1")
    assert r2["n"] == r1["n"] + 1
    assert r2["started_at"] == r1["started_at"]
    assert cs.inflight_get("B1")["n"] == 2
    assert cs.inflight_clear("B1") is True
    assert cs.inflight_clear("B1") is False
    assert cs.inflight_get("B1") == {}


def test_sidecar_lock_is_released_after_exception(lock_env):
    with pytest.raises(RuntimeError):
        with cs._sidecar_lock():
            raise RuntimeError("boom")
    # 锁已释放 ⇒ 再次进入不应阻塞
    with cs._sidecar_lock():
        cs.inflight_mark("B2")
    assert cs.inflight_get("B2")


# ------------------------------------------------------------------ MCP 层
def _shell():
    from brain_api import BrainApiClient
    return BrainApiClient.__new__(BrainApiClient)


def test_release_plan_no_cooldown_when_not_computed():
    c = _shell()
    assert c._corr_release_plan({"status": "pending", "computed": False}) == (False, None)
    cd, sec = c._corr_release_plan({"status": "pending", "computed": True})
    assert cd is True


def test_get_production_correlation_short_circuits_when_unavailable(lock_env, monkeypatch):
    monkeypatch.setenv("WQB_CORR_UNAVAILABLE_STREAK", "1")
    cs.note_pending_streak("C1")
    c = _shell()
    calls = []

    async def noop_auth():
        return None

    async def no_preread(*a, **k):
        return None

    async def boom_lock(*a, **k):
        calls.append("lock")
        return {"acquired": True}

    c.ensure_authenticated = noop_auth
    c._read_existing_prod_correlation = no_preread
    c._try_acquire_brain_correlation_lock = boom_lock
    r = _run(c.get_production_correlation("C1", use_pre_read=False))
    assert r["status"] == "platform_unavailable"
    assert r["max"] is None and r["retry_after"] > 0
    assert calls == [], "熔断期间不得抢锁、不得发请求"


def test_check_correlation_rejects_unknown_type():
    c = _shell()

    async def noop_auth():
        return None

    c.ensure_authenticated = noop_auth
    r = _run(c.check_correlation("D1", "nonsense", 0.7))
    assert "error" in r
    assert r["all_passed"] is None, "未知类型不得假通过"


def test_check_correlation_passes_timeout_through():
    c = _shell()
    seen = {}

    async def noop_auth():
        return None

    async def fake_platform(aid, **kwargs):
        seen.update(kwargs)
        return {"status": "ok", "max": 0.4, "records": []}

    c.ensure_authenticated = noop_auth
    c._prod_corr_cached = lambda aid: None
    c.get_production_correlation = fake_platform
    _run(c.check_correlation("E1", "production", 0.7, timeout_s=12.5))
    assert seen.get("max_wait_seconds") == 12.5


def test_cache_hit_marks_non_realtime_source_provisional():
    c = _shell()
    assert c._corr_cache_provisional({"source": "legacy"}) is True
    assert c._corr_cache_provisional({"source": None}) is True
    assert c._corr_cache_provisional({"source": "manual"}) is True
    assert c._corr_cache_provisional({"source": "check_correlation"}) is False
    assert c._corr_cache_provisional({"source": "prod_peek"}) is False
    assert c._corr_cache_provisional({"source": "platform_sync"}) is False


def test_platform_unavailable_is_fail_closed_in_verdict():
    from wqb.prod_verdict import gate_allowed, prod_verdict
    r = {"status": "platform_unavailable",
         "checks": {"production": {"max_correlation": None, "status": "platform_unavailable"}}}
    v = prod_verdict(r)
    assert v["value"] is None and v["usable"] is False
    assert gate_allowed(r) is False
