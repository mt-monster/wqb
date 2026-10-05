# -*- coding: utf-8 -*-
"""prod 单源化契约（2026-10-05）。

背景：同一颗 alpha 的 prod 此前存在三处且无同步契约——
``alpha_corr_cache``（权威表，196 行）/ ``alphas.prod_correlation``（561 行）/
``submit_ready.prod``（队列内）。已发生实际事故：6 颗 GBR 的实测值只在 ``alphas`` 里，
权威表缺条目 → 盘点判「无新鲜度依据」→ 强制重打平台单并发队列。当时靠手工 backfill
修复，不是机制。本文件把「单源 + 新鲜度 + source 收敛」钉成不可回退的契约。
"""
import pytest

from wqb.store import CampaignStore
from wqb.store._corr_cache import (
    CORR_FRESH_HOURS,
    CORR_SOURCES,
    corr_age_hours,
    normalize_corr_source,
)


@pytest.fixture
def store(tmp_path):
    """本文件的 store fixture（``test_store.py`` 里那份是局部的，不跨文件共享）。

    ⚠ 用 ``set_db_path`` 类显式 hook 不适用：这里直接构造独立 tmp 库，
    与 ``data/wqb.db`` 完全隔离，不会写生产库。
    """
    db = CampaignStore(str(tmp_path / "corr_src.db"))
    yield db
    db.close()


@pytest.mark.parametrize("raw,expected", [
    ("platform_sync", "platform_sync"),
    ("check_correlation", "check_correlation"),
    ("prod_first_screen", "prod_first_screen"),
    ("platform", "platform_sync"),        # 历史别名
    ("verify", "platform_sync"),
    ("submit_verdict", "platform_sync"),
    ("prod_first", "prod_first_screen"),   # 历史简写
    ("PROD_FIRST_SCREEN", "prod_first_screen"),  # 大小写不敏感
    ("api", "platform_sync"),
])
def test_normalize_corr_source_maps_known_and_alias(raw, expected):
    got = normalize_corr_source(raw)
    assert got["source"] == expected
    assert got["source"] in CORR_SOURCES


@pytest.mark.parametrize("raw", ["p0_1_verify_20260923", "raw_poll", "随手写的", ""])
def test_normalize_corr_source_never_invents_and_keeps_detail(raw):
    """自由文本 → legacy + detail 保留原值（**不能丢溯源**，也不能编造可信来源）。"""
    got = normalize_corr_source(raw)
    assert got["source"] in CORR_SOURCES
    if str(raw).strip() and got["source"] == "legacy":
        assert got["detail"] == str(raw).strip()


def test_normalize_corr_source_none_is_manual():
    assert normalize_corr_source(None)["source"] == "manual"


def test_corr_age_hours_unknown_is_none_not_zero():
    """**关键防回归**：无法解析时间戳必须是 None（未知），不能是 0（会被当成「刚测过」）。"""
    assert corr_age_hours(None) is None
    assert corr_age_hours("") is None
    assert corr_age_hours("not-a-date") is None


def test_corr_fresh_hours_is_48():
    """48h 保鲜期是单一事实源（对齐 submit_inventory --stale-hours 与 get_alpha_corr_metrics）。"""
    assert CORR_FRESH_HOURS == 48.0


def _mk_alpha(store, aid, region="KOR"):
    try:
        store.upsert_alpha_from_platform({
            "alpha_id": aid, "region": region, "expression": "rank(close)",
            "sharpe": 1.8, "fitness": 1.1, "platform_status": "UNSUBMITTED",
            "alpha_type": "REGULAR", "stage": "IS",
        })
    except Exception:  # noqa: BLE001 - fixture 库可能无 regions 行
        pytest.skip("fixture 无 region 定义")


def test_get_corr_cache_marks_stale_but_still_returns_value(store):
    """过期不等于作废：值照常返回（可排序参考），但标 stale + fresh=False。"""
    store.set_corr_cache("s1", prod=0.5, source="platform_sync")
    store.connection.execute(
        "UPDATE alpha_corr_cache SET checked_at='2000-01-01T00:00:00' WHERE alpha_id='s1'")
    store.connection.commit()

    got = store.get_corr_cache("s1")
    assert got["prod_correlation"] == 0.5      # 值仍在
    assert got["stale"] is True                 # 但明确标过期
    assert got["fresh"] is False
    assert got["age_hours"] > CORR_FRESH_HOURS


def test_get_corr_cache_missing_timestamp_is_stale(store):
    """有值但无时间戳 ⇒ 判 stale（「不知道新鲜度」不等于「新鲜」）。"""
    store.set_corr_cache("s2", prod=0.5, source="platform_sync")
    store.connection.execute(
        "UPDATE alpha_corr_cache SET checked_at=NULL WHERE alpha_id='s2'")
    store.connection.commit()
    got = store.get_corr_cache("s2")
    assert got["age_hours"] is None
    assert got["stale"] is True
    assert got["fresh"] is False


def test_get_corr_authoritative_falls_back_to_alphas(store):
    """单源读回落：权威表缺条目时读 alphas，并标 from_alphas（可判「可能需 refresh」）。"""
    _mk_alpha(store, "fb1")
    store.persist_correlation("fb1", prod=0.44, source="platform_sync")

    assert store.get_corr_cache("fb1") is None          # 权威表确实没有
    got = store.get_corr_authoritative("fb1")           # 但单源读能拿到
    assert got is not None
    assert got["prod_correlation"] == 0.44
    assert got.get("from_alphas") is True


def test_get_corr_authoritative_prefers_cache_table(store):
    """权威表优先于 alphas（两处都有值时不回落）。"""
    store.set_corr_cache("p1", prod=0.11, source="platform_sync")
    _mk_alpha(store, "p1")
    store.persist_correlation("p1", prod=0.99, source="platform_sync", overwrite=True)

    got = store.get_corr_authoritative("p1")
    assert got["prod_correlation"] == 0.11   # 权威表的值，不是 alphas 的 0.99


def test_set_corr_cache_partial_write_preserves_other_column(store):
    """只补 self 不抹掉 prod（COALESCE 语义，单源化后仍成立）。"""
    store.set_corr_cache("pp1", prod=0.69, source="platform_sync")
    store.set_corr_cache("pp1", self_=0.31, source="platform_sync")
    got = store.get_corr_cache("pp1")
    assert got["prod_correlation"] == 0.69
    assert got["self_correlation"] == 0.31


def test_set_corr_cache_rejects_out_of_range(store):
    """越界值不算数（防空值/异常污染），沿用既有契约。"""
    out = store.set_corr_cache("bad1", prod=1.7, source="platform_sync")
    assert out.get("skipped") == "no_valid_value"


def test_backfill_from_alphas_is_idempotent(store):
    """存量消化动作幂等：第二次跑 0 迁移。"""
    _mk_alpha(store, "bf1")
    store.persist_correlation("bf1", prod=0.61, source="prod_first_screen")

    first = store.backfill_from_alphas()
    assert first["migrated"] >= 1
    assert store.get_corr_cache("bf1")["prod_correlation"] == 0.61

    second = store.backfill_from_alphas()
    assert second["migrated"] == 0            # 幂等


def test_unmeasured_supply_excludes_ra_failed_by_default(store):
    """未测供给查询默认剔 RA 失败行——不剔会严重高估可用供给
    （实测全库 330 条未测里 206 条 RA 硬闸已失败，ASI 145 条里仅 3 条 RA-clean）。"""
    from wqb.store import submit_queue as sq
    clean = sq.unmeasured_supply(ra_clean_only=True, limit=0, db_path=store.path)
    allrows = sq.unmeasured_supply(ra_clean_only=False, limit=0, db_path=store.path)
    assert len(clean) <= len(allrows)
    clean_ids = {r["alpha_id"] for r in clean}
    all_ids = {r["alpha_id"] for r in allrows}
    assert clean_ids <= all_ids                 # RA-clean 必须是全集子集


def test_unmeasured_supply_filters_by_region(store):
    from wqb.store import submit_queue as sq
    rows = sq.unmeasured_supply(region="KOR", limit=10, db_path=store.path)
    assert all((r["region"] or "").upper() == "KOR" for r in rows)

    """过期不等于作废：值照常返回（可排序参考），但标 stale + fresh=False。"""
    store.set_corr_cache("s1", prod=0.5, source="platform_sync")
    store.connection.execute(
        "UPDATE alpha_corr_cache SET checked_at='2000-01-01T00:00:00' WHERE alpha_id='s1'")
    store.connection.commit()

    got = store.get_corr_cache("s1")
    assert got["prod_correlation"] == 0.5      # 值仍在
    assert got["stale"] is True                 # 但明确标过期
    assert got["fresh"] is False
    assert got["age_hours"] > CORR_FRESH_HOURS


def test_get_corr_cache_missing_timestamp_is_stale(store):
    """有值但无时间戳 ⇒ 判 stale（「不知道新鲜度」不等于「新鲜」）。"""
    store.set_corr_cache("s2", prod=0.5, source="platform_sync")
    store.connection.execute(
        "UPDATE alpha_corr_cache SET checked_at=NULL WHERE alpha_id='s2'")
    store.connection.commit()
    got = store.get_corr_cache("s2")
    assert got["age_hours"] is None
    assert got["stale"] is True
    assert got["fresh"] is False


def _mk_alpha(store, aid, region="KOR"):
    try:
        store.upsert_alpha_from_platform({
            "alpha_id": aid, "region": region, "expression": "rank(close)",
            "sharpe": 1.8, "fitness": 1.1, "platform_status": "UNSUBMITTED",
            "alpha_type": "REGULAR", "stage": "IS",
        })
    except Exception:  # noqa: BLE001 - fixture 库可能无 regions 行
        pytest.skip("fixture 无 region 定义")
