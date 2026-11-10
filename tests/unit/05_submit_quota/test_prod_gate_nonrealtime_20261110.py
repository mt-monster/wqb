# -*- coding: utf-8 -*-
"""2026-11-10 审查 P0-1 / P1-2：_prod_gate 对「非实时来源」与残留 provisional 的守护。

背景：缓存命中分支不带 provisional，而 peek 值历史上经手工 SQL 落库、source 可以是
任意自由文本、checked_at 用的是写库时刻 ⇒ 旧值可被当成新鲜实测直接过 0.7 闸。
修复后：source ∈ NON_REALTIME_SOURCES（或缓存值根本无来源标记）按 provisional 处理，
补一次 refresh=True 真重测；重测后仍只有预读/非实时值 ⇒ fail-closed。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.workflow.nodes import submit_alpha as sa  # noqa: E402


class _Client:
    """第一次返回缓存值，refresh=True 时返回平台实测值（可配置）。"""

    def __init__(self, cached_payload, live_payload=None):
        self.cached_payload = cached_payload
        self.live_payload = live_payload
        self.calls = []

    async def check_correlation(self, alpha_id, correlation_type="production",
                                threshold=0.7, refresh=False):
        self.calls.append(refresh)
        if refresh and self.live_payload is not None:
            return self.live_payload
        return self.cached_payload


def _cached(max_corr=0.42, source="check_correlation"):
    return {"all_passed": True, "checks": {"production": {
        "max_correlation": max_corr, "passes_check": True,
        "from_cache": True, "source": source, "cached_at": "2026-11-10T00:00:00"}}}


def _live(max_corr=0.42):
    return {"all_passed": True, "checks": {"production": {
        "max_correlation": max_corr, "passes_check": True}}}


@pytest.fixture(autouse=True)
def _no_force_refresh(monkeypatch):
    monkeypatch.delenv("WQB_PROD_GATE_REFRESH", raising=False)


def test_realtime_cache_source_passes_without_refetch():
    c = _Client(_cached(source="check_correlation"))
    r = sa._prod_gate(c, "A1")
    assert r["allowed"] is True
    assert c.calls == [False], "平台实测来源不该额外重测"


def test_prod_peek_source_passes_without_refetch():
    """peek 读的是平台端点已算结果，带真实测量时刻即可判闸（不强制重测）。"""
    c = _Client(_cached(source="prod_peek"))
    r = sa._prod_gate(c, "A1")
    assert r["allowed"] is True
    assert c.calls == [False]


@pytest.mark.parametrize("src", ["manual", "legacy", "alphas_backfill",
                                 "checkpoint_backfill", "triage_local"])
def test_non_realtime_source_forces_refresh(src):
    c = _Client(_cached(source=src), live_payload=_live(0.4))
    r = sa._prod_gate(c, "A1")
    assert c.calls == [False, True], "非实时来源必须补一次真重测"
    assert r["allowed"] is True


def test_missing_source_on_cache_forces_refresh():
    payload = _cached()
    del payload["checks"]["production"]["source"]
    c = _Client(payload, live_payload=_live(0.4))
    r = sa._prod_gate(c, "A1")
    assert c.calls == [False, True]
    assert r["allowed"] is True


def test_non_realtime_source_blocked_when_refresh_fails():
    c = _Client(_cached(source="legacy"),
                live_payload={"status": "pending", "checks": {"production": {
                    "max_correlation": None, "status": "pending"}}})
    r = sa._prod_gate(c, "A1")
    assert r["allowed"] is False
    assert "fail-closed" in r["reason"]


def test_residual_provisional_after_refresh_is_blocked():
    """P1-2：重测后仍带 provisional ⇒ 不得放行（旧实现重算后不再检查）。"""
    still_provisional = {"checks": {"production": {
        "max_correlation": 0.4, "passes_check": True,
        "source": "alpha_detail_cached", "provisional": True}}}
    c = _Client(_cached(source="legacy"), live_payload=still_provisional)
    r = sa._prod_gate(c, "A1")
    assert r["allowed"] is False
    assert r["provisional"] is True
    assert "非实时来源" in r["reason"] or "预读" in r["reason"]


def test_threshold_comes_from_config():
    from wqb.config import PRODCORR_CEILING
    assert sa._PROD_THRESHOLD == float(PRODCORR_CEILING)


def test_cache_source_untrusted_helper():
    assert sa._cache_source_untrusted({"from_cache": True, "source": "legacy"}) is True
    assert sa._cache_source_untrusted({"from_cache": True, "source": None}) is True
    assert sa._cache_source_untrusted({"from_cache": True, "source": "prod_peek"}) is False
    assert sa._cache_source_untrusted({"from_cache": False, "source": "legacy"}) is False
    assert sa._cache_source_untrusted({}) is False
