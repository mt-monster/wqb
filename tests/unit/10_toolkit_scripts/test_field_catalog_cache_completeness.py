# -*- coding: utf-8 -*-
"""2026-10-20：S1 字段目录缓存必须带完整性凭据。

B 面：即便拉取端已改全量分页，只要缓存还把「TTL 内但内容短」的旧目录当真，
analyst7 的 299/1111 就会在 24 小时有效期里继续被复用。本文件守三件事：

1. 缺 `complete` / `complete=False` / 带 `truncated_reason` 的目录既不命中也不写入；
2. 完整目录照常命中（TTL 仍然是第二道闸，不是唯一一道）；
3. 历史 `field_catalog` 表条目同样受此约束。
"""
import datetime
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TK = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TK) not in sys.path:
    sys.path.insert(0, str(TK))

from _lib import field_catalog_cache as fcc  # noqa: E402
from _lib import wqb_store  # noqa: E402


class FakeStore:
    def __init__(self, ledger=None, catalog=None):
        self.ledger = ledger
        self.catalog = catalog
        self.saved_ledger = {}
        self.saved_catalog = None
        self.closed = 0

    def get_ledger(self, region, key):
        return self.ledger

    def get_field_catalog(self, region, dataset):
        return self.catalog

    def upsert_ledger(self, region, key, value):
        self.saved_ledger[key] = value

    def upsert_field_catalog(self, region, catalog):
        self.saved_catalog = catalog

    def close(self):
        self.closed += 1


def _catalog(n_fields=1111, *, complete=True, truncated_reason=None,
             fetched_at=None, fields=None):
    return {
        "dataset": "analyst7",
        "field_count": n_fields if fields is None else len(fields),
        "platform_count": 1111,
        "complete": complete,
        "truncated_reason": truncated_reason,
        "fetched_at": fetched_at or datetime.datetime.now().isoformat(timespec="seconds"),
        "fields": fields if fields is not None
        else [{"id": "f%d" % i} for i in range(n_fields)],
    }


def _ledger_cache(catalog, *, cached_at=None):
    out = dict(catalog)
    out["cache_metadata"] = {
        "cached_at": cached_at or datetime.datetime.now().isoformat(timespec="seconds"),
        "ttl_seconds": 86400,
        "source": "platform_api",
    }
    return out


@pytest.fixture
def ctx():
    return types.SimpleNamespace(region="EUR")


def _manager(ctx, store):
    return fcc.FieldCatalogCache(ctx)


def _patch_store(monkeypatch, store):
    """把假 store 打到**现役** `_lib.wqb_store` 模块对象上。

    为什么不能直接 `monkeypatch.setattr(wqb_store, ...)`：本模块顶部 `from _lib import wqb_store`
    抓到的是**导入当时**那个对象。而 `test_pipeline_error_isolation` 会把 `_lib.wqb_store`
    从 `sys.modules` 弹出后重新导入（造出**新**模块对象），而 `field_catalog_cache` 是在
    调用点 `from _lib.wqb_store import get_store`（78/101/171/211/224/250 行）——它解析到新对象。
    于是 patch 打在旧对象上、生产代码读新对象 ⇒ 真 `CampaignStore` ⇒ 生产库守卫拒绝 ⇒
    单跑绿、全量红（2026-10-27 实测 6 条）。

    判据：**patch 必须打在 `sys.modules` 里当前生效的那个对象上**，并当场断言生效。
    """
    import importlib

    live = importlib.import_module("_lib.wqb_store")      # 恒等于 sys.modules 里的现役对象
    assert sys.modules["_lib.wqb_store"] is live, "取到的不是现役模块对象"
    monkeypatch.setattr(live, "get_store", lambda ctx=None: store)
    assert sys.modules["_lib.wqb_store"].get_store() is store, "patch 没落在现役模块上"


@pytest.mark.parametrize("bad", [
    pytest.param(_ledger_cache(_catalog(299, complete=False)), id="complete_false"),
    pytest.param(_ledger_cache(_catalog(299, complete=None)), id="complete_missing"),
    pytest.param(_ledger_cache(_catalog(1111, truncated_reason="max_items_cap")),
                 id="truncated_reason"),
])
def test_incomplete_ledger_cache_is_not_served(ctx, monkeypatch, bad):
    store = FakeStore(ledger=bad, catalog=None)
    _patch_store(monkeypatch, store)
    manager = _manager(ctx, store)
    assert manager.get_cached_catalog("analyst7") is None
    assert store.closed >= 1


def test_complete_ledger_cache_is_served(ctx, monkeypatch):
    store = FakeStore(ledger=_ledger_cache(_catalog()), catalog=None)
    _patch_store(monkeypatch, store)
    manager = _manager(ctx, store)
    got = manager.get_cached_catalog("analyst7")
    assert got is not None
    assert got["field_count"] == 1111


def test_complete_but_expired_cache_is_not_served(ctx, monkeypatch):
    old = (datetime.datetime.now() - datetime.timedelta(seconds=10)).isoformat(timespec="seconds")
    store = FakeStore(ledger=_ledger_cache(_catalog(), cached_at=old), catalog=None)
    _patch_store(monkeypatch, store)
    manager = fcc.FieldCatalogCache(ctx, ttl_seconds=5)
    assert manager.get_cached_catalog("analyst7") is None


@pytest.mark.parametrize("bad", [
    pytest.param(_catalog(299, complete=False), id="complete_false"),
    pytest.param(_catalog(299, complete=None), id="legacy_missing_complete"),
])
def test_incomplete_db_catalog_is_not_served(ctx, monkeypatch, bad):
    store = FakeStore(ledger=None, catalog=bad)
    _patch_store(monkeypatch, store)
    manager = _manager(ctx, store)
    assert manager.get_cached_catalog("analyst7") is None


def test_complete_db_catalog_is_served(ctx, monkeypatch):
    store = FakeStore(ledger=None, catalog=_catalog())
    _patch_store(monkeypatch, store)
    manager = _manager(ctx, store)
    assert manager.get_cached_catalog("analyst7")["field_count"] == 1111


def test_save_refuses_incomplete_catalog(ctx, monkeypatch):
    store = FakeStore()
    _patch_store(monkeypatch, store)
    manager = _manager(ctx, store)
    manager.save_catalog_cache("analyst7", _catalog(299, complete=False))
    manager.save_catalog_cache("analyst7", _catalog(1111, truncated_reason="search_window_capped"))
    assert store.saved_ledger == {}
    assert store.saved_catalog is None


def test_save_writes_complete_catalog_with_metadata(ctx, monkeypatch):
    store = FakeStore()
    _patch_store(monkeypatch, store)
    manager = _manager(ctx, store)
    manager.save_catalog_cache("analyst7", _catalog())
    key = "catalog_cache_analyst7"
    assert key in store.saved_ledger
    assert store.saved_ledger[key]["cache_metadata"]["source"] == "platform_api"
    assert store.saved_catalog["complete"] is True
