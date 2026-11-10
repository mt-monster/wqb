# -*- coding: utf-8 -*-
"""2026-11-10 查 prod 机制审查 —— 第一批 P0 修复的守护测试。

覆盖：
  P0-2  set_corr_cache 纯 records 更新不得刷新 checked_at（防「旧值洗新」）
  P1-8  corr_age_hours 对 aware 时间戳 + naive now 不再误判 stale
  P0-1  prod_peek 登记词 + 历史自由文本别名归一 + NON_REALTIME_SOURCES 分层
  P0-3  prod_wait.parse 不再扫直方图 records（防把 bin 上界/计数当 prod）
  P0-1  prod_peek_ingest 以产物 at 作 checked_at，且三重校验拒绝坏产物
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
for p in (ROOT / "src", ROOT / "tools", ROOT / "tools" / "probe"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from wqb.store import CampaignStore  # noqa: E402
from wqb.store._corr_cache import (  # noqa: E402
    CORR_SOURCES, NON_REALTIME_SOURCES, corr_age_hours, normalize_corr_source,
)


@pytest.fixture
def store(tmp_path):
    s = CampaignStore(str(tmp_path / "hardening.db"))
    yield s
    s.close()


# ---------------------------------------------------------------- P0-2
def test_records_only_update_keeps_checked_at(store):
    old = (datetime.now() - timedelta(hours=30)).isoformat(timespec="seconds")
    store.set_corr_cache("A1", prod=0.42, source="check_correlation", checked_at=old)
    before = store.get_corr_cache("A1")
    assert before["checked_at"] == old

    # 只补直方图、不带任何有效值 ⇒ 不得把 30h 前的测量时刻刷成「刚测过」
    out = store.set_corr_cache("A1", records=[[0.4, 0.5, 7]], source="legacy")
    after = store.get_corr_cache("A1")
    assert after["checked_at"] == old, "纯 records 更新刷新了 checked_at（旧值被洗新）"
    assert after["prod_correlation"] == 0.42
    assert after["source"] == "check_correlation", "纯 records 更新不该改来源"
    assert out["meta_refreshed"] is False


def test_invalid_prod_does_not_refresh_timestamp(store):
    old = (datetime.now() - timedelta(hours=10)).isoformat(timespec="seconds")
    store.set_corr_cache("A2", prod=0.5, checked_at=old)
    # 越界值被 _corr_value 置 None，但 records 非空 ⇒ 旧实现会刷新 checked_at
    store.set_corr_cache("A2", prod=1.7, records=[[0.0, 0.1, 1]])
    rec = store.get_corr_cache("A2")
    assert rec["checked_at"] == old
    assert rec["prod_correlation"] == 0.5


def test_valid_value_refreshes_timestamp(store):
    old = (datetime.now() - timedelta(hours=10)).isoformat(timespec="seconds")
    store.set_corr_cache("A3", prod=0.5, checked_at=old)
    store.set_corr_cache("A3", prod=0.6, source="check_correlation")
    rec = store.get_corr_cache("A3")
    assert rec["prod_correlation"] == 0.6
    assert rec["checked_at"] != old
    assert rec["fresh"] is True


# ---------------------------------------------------------------- P1-8
def test_age_hours_aware_timestamp_not_misjudged():
    ts = (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()
    age = corr_age_hours(ts)
    assert age is not None, "aware 时间戳被误判成无法解析（→ stale → 无谓重测）"
    assert 2.5 <= age <= 3.5


def test_age_hours_naive_and_aware_agree():
    naive = (datetime.now() - timedelta(hours=5)).isoformat(timespec="seconds")
    aware = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
    a, b = corr_age_hours(naive), corr_age_hours(aware)
    assert a is not None and b is not None
    assert abs(a - b) < 0.05


def test_age_hours_unknown_is_none_not_zero():
    assert corr_age_hours(None) is None
    assert corr_age_hours("not-a-date") is None


# ---------------------------------------------------------------- P0-1 词表
def test_prod_peek_registered_and_aliases_normalized():
    assert "prod_peek" in CORR_SOURCES
    for raw in ("no-lock peek", "no-lock peek batch", "prod_wait_peek", "prod_peek_batch"):
        assert normalize_corr_source(raw)["source"] == "prod_peek"


def test_non_realtime_sources_exclude_platform_measurements():
    # peek 读的是平台端点已算结果，带真实测量时刻即可判闸
    assert "prod_peek" not in NON_REALTIME_SOURCES
    assert "check_correlation" not in NON_REALTIME_SOURCES
    assert "platform_sync" not in NON_REALTIME_SOURCES
    for s in ("manual", "legacy", "alphas_backfill", "checkpoint_backfill", "triage_local"):
        assert s in NON_REALTIME_SOURCES


# ---------------------------------------------------------------- P0-3 parse
def test_parse_never_reads_histogram():
    from prod_wait import parse
    # 只有直方图、没有 max ⇒ 必须 None（旧实现会返回 3 或 0.8）
    assert parse({"records": [[0.0, 0.1, 3], [0.7, 0.8, 0]]}) is None
    assert parse({"records": [[0.9, 1.0, 12345]]}) is None
    assert parse({"max": 0.62, "records": [[0.9, 1.0, 999]]}) == 0.62
    assert parse({"schema": {"max": 0.31}}) == 0.31
    assert parse({"max_correlation": 0.44}) == 0.44


def test_parse_rejects_out_of_range():
    from prod_wait import parse
    assert parse({"max": 1.5}) is None
    assert parse({"max": -0.2}) is None
    assert parse({"max": "abc"}) is None
    assert parse(None) is None


# ---------------------------------------------------------------- P0-1 ingest
def _write_payload(dirpath, alpha_id, prod, at, **extra):
    p = dirpath / f"prod_peek_{alpha_id}.json"
    p.write_text(json.dumps({"alpha_id": alpha_id, "prod": prod, "at": at,
                             "histogram": [[0.0, 0.1, 2]], **extra}), encoding="utf-8")
    return p


def test_ingest_uses_probe_time_as_checked_at(store, tmp_path):
    from prod_peek_ingest import ingest_one
    at = (datetime.now() - timedelta(hours=6)).isoformat(timespec="seconds")
    _write_payload(tmp_path, "B1", 0.6635, at)
    res = ingest_one(store, "B1", str(tmp_path))
    assert res["ok"] is True
    rec = store.get_corr_cache("B1")
    assert rec["prod_correlation"] == 0.6635
    assert rec["source"] == "prod_peek"
    assert rec["checked_at"] == at, "必须用探测时刻，不能用写库时刻"
    assert 5.5 <= rec["age_hours"] <= 6.5
    assert rec["fresh"] is True


def test_ingest_rejects_missing_timestamp(store, tmp_path):
    from prod_peek_ingest import ingest_one
    _write_payload(tmp_path, "B2", 0.5, None)
    res = ingest_one(store, "B2", str(tmp_path))
    assert res["ok"] is False
    assert "测量时刻" in res["reason"]
    assert store.get_corr_cache("B2") is None


def test_ingest_rejects_out_of_range_and_mismatched_id(store, tmp_path):
    from prod_peek_ingest import ingest_one
    at = datetime.now().isoformat(timespec="seconds")
    _write_payload(tmp_path, "B3", 1.4, at)
    assert ingest_one(store, "B3", str(tmp_path))["ok"] is False
    _write_payload(tmp_path, "B4", 0.5, at)
    assert ingest_one(store, "OTHER", str(tmp_path))["ok"] is False


def test_ingest_dry_run_writes_nothing(store, tmp_path):
    from prod_peek_ingest import ingest_one
    at = datetime.now().isoformat(timespec="seconds")
    _write_payload(tmp_path, "B5", 0.4, at)
    res = ingest_one(store, "B5", str(tmp_path), dry_run=True)
    assert res["ok"] is True and res["dry_run"] is True
    assert store.get_corr_cache("B5") is None


def test_ingest_stale_payload_flagged(store, tmp_path):
    from prod_peek_ingest import ingest_one
    at = (datetime.now() - timedelta(hours=90)).isoformat(timespec="seconds")
    _write_payload(tmp_path, "B6", 0.4, at)
    res = ingest_one(store, "B6", str(tmp_path))
    assert res["ok"] is True and res["stale"] is True
    assert "warning" in res
    assert store.get_corr_cache("B6")["stale"] is True
