"""check_correlation 的 prod 缓存 — 落 SQLite 权威表（无网络）。

创建于 2026-10-06：设计文档 `docs/design/prod_corr_persistence_design_20260918.md`
§6.2 第 4 条声称「check_correlation 的 prod 缓存改两级 Redis → wqb 库」，§6.3 又称
新增了本文件（5 个用例）——**两者在实现里都不存在**：`check_correlation` 只写 Redis，
而 Redis 未启动时读写静默 no-op，缓存整条失效。本文件补齐该契约并锁定回归。

被测行为（每条都对应一次真实事故）：
  1. 命中新鲜缓存 ⇒ 不占平台单并发队列；
  2. 缓存过期（>48h）⇒ 回源平台，绝不拿陈值过 0.7 的闸；
  3. 平台实测结果 ⇒ 写入 alpha_corr_cache（source=check_correlation）；
  4. refresh=True ⇒ 强制回源；
  5. 缓存后端不可用 ⇒ 降级放行，不抛异常。
"""
import asyncio
import os
from datetime import datetime, timedelta

import pytest

import brain_api
from brain_api import BrainApiClient

# src/wqb 需要可导入（_cache_backend 延迟导入 wqb.store）
import sys
from pathlib import Path
_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def make_shell():
    return BrainApiClient.__new__(BrainApiClient)


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """把缓存后端指向临时库，绝不污染 data/wqb.db。"""
    db = tmp_path / "corr_cache_test.db"
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    return db


def _platform_payload(max_corr=0.42):
    return {
        "max": max_corr,
        "records": [[0.0, 0.1, 3], [0.7, 0.8, 0]],
        "min": 0.0,
    }


def _run(coro):
    return asyncio.run(coro)


def _seed_cache(db, alpha_id, prod, hours_ago):
    """直接写权威表，模拟"之前测过"的存量。"""
    from wqb.store import CampaignStore
    store = CampaignStore(str(db))
    ts = (datetime.now() - timedelta(hours=hours_ago)).isoformat(timespec="seconds")
    store.set_corr_cache(alpha_id, prod=prod, records=[[0.7, 0.8, 0]],
                         source="platform_sync", checked_at=ts)
    store.close()


def _read_cache(db, alpha_id):
    from wqb.store import CampaignStore
    store = CampaignStore(str(db))
    try:
        return store.get_corr_cache(alpha_id)
    finally:
        store.close()


# ---------------------------------------------------------------------------

def test_prod_cache_hit_skips_platform(tmp_db):
    """新鲜缓存命中 ⇒ 不打平台单并发队列。"""
    _seed_cache(tmp_db, "AAA111", 0.55, hours_ago=2)

    c = make_shell()
    calls = []

    async def fake_platform(aid):
        calls.append(aid)
        return _platform_payload()

    async def noop_auth():
        return None

    c.ensure_authenticated = noop_auth
    c.get_production_correlation = fake_platform

    res = _run(c.check_correlation("AAA111", "production", 0.7))
    assert calls == [], "命中新鲜缓存就不该占用平台相关性队列"
    chk = res["checks"]["production"]
    assert chk["from_cache"] is True
    assert chk["max_correlation"] == 0.55
    assert chk["passes_check"] is True


def test_prod_cache_stale_refetches(tmp_db):
    """缓存超过 48h ⇒ 回源平台。生产池会漂移，陈值比没值更危险。"""
    _seed_cache(tmp_db, "BBB222", 0.55, hours_ago=72)

    c = make_shell()
    calls = []

    async def fake_platform(aid):
        calls.append(aid)
        return _platform_payload(0.91)

    async def noop_auth():
        return None

    c.ensure_authenticated = noop_auth
    c.get_production_correlation = fake_platform

    res = _run(c.check_correlation("BBB222", "production", 0.7))
    assert calls == ["BBB222"], "过期缓存必须回源"
    assert res["checks"]["production"]["max_correlation"] == 0.91
    assert res["checks"]["production"]["passes_check"] is False
    # 回源后的新值覆盖旧值
    assert _read_cache(tmp_db, "BBB222")["prod_correlation"] == 0.91


def test_prod_result_persisted_to_authoritative_table(tmp_db):
    """平台实测结果写入 alpha_corr_cache，source 标 check_correlation。"""
    c = make_shell()

    async def fake_platform(aid):
        return _platform_payload(0.63)

    async def noop_auth():
        return None

    c.ensure_authenticated = noop_auth
    c.get_production_correlation = fake_platform

    _run(c.check_correlation("CCC333", "production", 0.7))

    rec = _read_cache(tmp_db, "CCC333")
    assert rec is not None, "实测结果必须落权威表，否则下次还得重打队列"
    assert rec["prod_correlation"] == 0.63
    assert rec["source"] == "check_correlation"
    assert rec["fresh"] is True


def test_refresh_bypasses_cache(tmp_db):
    """refresh=True 即使有新鲜缓存也强制回源（提交前终验语义）。"""
    _seed_cache(tmp_db, "DDD444", 0.55, hours_ago=1)

    c = make_shell()
    calls = []

    async def fake_platform(aid):
        calls.append(aid)
        return _platform_payload(0.80)

    async def noop_auth():
        return None

    c.ensure_authenticated = noop_auth
    c.get_production_correlation = fake_platform

    res = _run(c.check_correlation("DDD444", "production", 0.7, refresh=True))
    assert calls == ["DDD444"]
    assert res["checks"]["production"]["max_correlation"] == 0.80


def test_cache_backend_unavailable_degrades(tmp_db):
    """后端不可用 ⇒ 降级为无缓存（照常回源），绝不抛异常阻断查询。"""
    c = make_shell()
    calls = []

    async def fake_platform(aid):
        calls.append(aid)
        return _platform_payload(0.31)

    async def noop_auth():
        return None

    c.ensure_authenticated = noop_auth
    c.get_production_correlation = fake_platform
    c._cache_backend = lambda: None          # 模拟 wqb.store 导入失败

    res = _run(c.check_correlation("EEE555", "production", 0.7))
    assert calls == ["EEE555"]
    assert res["checks"]["production"]["max_correlation"] == 0.31
