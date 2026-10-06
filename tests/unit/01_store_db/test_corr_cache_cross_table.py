# -*- coding: utf-8 -*-
"""prod corr 跨表一致性护栏（2026-10-06）。

背景：2026-10-06 评估发现 set_corr_cache 与 alphas 表之间的 mirror 链是
NULL-only，导致 3 行 >0.01 冲突（E5pbM7Nm / VkaZYdbG / wpZ3RP96，cache 拿到
新的平台实测值、alphas 留着 2026-09-20 的旧值）。同时 select_ra_basket /
prod_saturation_gate / submit_queue / prod_first_screen 全部只读 alphas 表，
权威表里的 191 条 cache-only 行对它们完全不可见 ⇒ 被重新排队打平台单并发队列
（历史「6 颗 GBR 重复测量」的根因）。

本文件锁三件事：
  1. set_corr_cache 联动 alphas 时**必须覆盖**已有旧值（overwrite=True 语义）；
  2. get_corr_authoritative_batch 能同时读「cache-only」和「cache ∩ alphas」两种行，
     且正确标 from_alphas；
  3. CampaignStore.search_alphas_by_sharpe(merge_corr_cache=True) 把缓存优先合并进
     返回行，让 prod_saturation_gate 等消费者看到最新值。
"""
import datetime as dt
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402


@pytest.fixture
def store(tmp_path):
    db = tmp_path / "wqb.db"
    s = CampaignStore(str(db))
    s.connection.execute("INSERT INTO regions (id, name) VALUES (1, 'TST')")
    s.connection.execute(
        "INSERT INTO datasets (id, name, region_id) VALUES (10, 'ds', 1)")
    # 造一根 alphas 行——后续 set_corr_cache 才能联动写入（否则 mirror 报 not_found）
    s.connection.execute(
        "INSERT INTO alphas (alpha_id, expression, region_id, dataset_id, "
        "prod_correlation, corr_checked_at) "
        "VALUES ('HAS_OLD', 'rank(x)', 1, 10, 0.6678, "
        "'2026-09-20T04:04:00')")
    s.connection.commit()
    yield s
    s.close()


def _hours_ago(h):
    return (dt.datetime.now() - dt.timedelta(hours=h)).isoformat(timespec="seconds")


# ----------------------------------------------------------------------------- set_corr_cache mirror overwrite

def test_set_corr_cache_overwrites_stale_alpha_value(store):
    """权威表拿到新平台值后，mirror 必须覆盖 alphas 里的旧值——
    而非 NULL-only 静默丢弃（E5pbM7Nm 0.6678→0.981 那条路径）。"""
    store.set_corr_cache("HAS_OLD", prod=0.981, self_=0.60,
                         source="platform_sync",
                         checked_at=_hours_ago(1))
    row = store.connection.execute(
        "SELECT prod_correlation, self_correlation, prod_corr_source "
        "FROM alphas WHERE alpha_id='HAS_OLD'").fetchone()
    assert float(row[0]) == 0.981, \
        "mirror 必须以 overwrite 语义覆盖 alphas 旧值，否则消费者只读 alphas 就永远看到陈旧数"
    assert float(row[1]) == 0.60
    assert row[2] == "platform_sync"
    # 权威表本身也是新值
    assert store.get_corr_cache("HAS_OLD")["prod_correlation"] == 0.981


def test_set_corr_cache_only_prod_still_preserves_existing_self(store):
    """COALESCE 语义：只补 prod 时不应把已存在的 self 抹掉。"""
    store.set_corr_cache("HAS_OLD", prod=0.9, source="platform_sync")
    assert store.get_corr_cache("HAS_OLD")["self_correlation"] is None
    store.set_corr_cache("HAS_OLD", self_=0.7, source="platform_sync")
    rec = store.get_corr_cache("HAS_OLD")
    assert rec["prod_correlation"] == 0.9 and rec["self_correlation"] == 0.7


# ----------------------------------------------------------------------------- get_corr_authoritative_batch

def test_authoritative_batch_reads_cache_only_rows(store):
    """仿真阶段 alpha 不在 alphas 表里，只有 alpha_corr_cache 有——
    批量读必须能拿到它们（这是「191 条 cache-only 行不可见」缺陷的正面验证）。"""
    store.set_corr_cache("CACHE_ONLY", prod=0.55, source="check_correlation")
    recs = store.get_corr_authoritative_batch(["CACHE_ONLY", "GHOST"])
    assert "CACHE_ONLY" in recs
    assert recs["CACHE_ONLY"]["from_alphas"] is False
    assert recs["CACHE_ONLY"]["prod_correlation"] == 0.55
    assert "GHOST" not in recs


def test_authoritative_batch_prefers_cache_over_alphas(store):
    """两表都有时，权威表优先；标 from_alphas=False。"""
    store.set_corr_cache("HAS_OLD", prod=0.95, source="platform_sync")
    recs = store.get_corr_authoritative_batch(["HAS_OLD"])
    r = recs["HAS_OLD"]
    assert r["from_alphas"] is False
    assert r["prod_correlation"] == 0.95


def test_authoritative_batch_falls_back_to_alphas_when_cache_absent(store):
    """缓存缺、alphas 有 → 回落并标 from_alphas=True。"""
    store.connection.execute(
        "INSERT INTO alphas (alpha_id, expression, region_id, dataset_id, "
        "prod_correlation, corr_checked_at) "
        "VALUES ('ALPHAS_ONLY', 'rank(x)', 1, 10, 0.42, '2026-10-01T12:00:00')")
    store.connection.commit()
    recs = store.get_corr_authoritative_batch(["ALPHAS_ONLY"])
    assert recs["ALPHAS_ONLY"]["from_alphas"] is True
    assert recs["ALPHAS_ONLY"]["prod_correlation"] == 0.42


def test_authoritative_batch_handles_empty_and_many_ids(store):
    """分块 / 空 id 过滤：与 list_corr_cache 同契约。"""
    assert store.get_corr_authoritative_batch([]) == {}
    assert store.get_corr_authoritative_batch([None, "", ""]) == {}
    big = [f"ID_{i}" for i in range(1200)]
    recs = store.get_corr_authoritative_batch(big)
    assert recs == {}


# ----------------------------------------------------------------------------- search_alphas_by_sharpe merge

def test_search_alphas_by_sharpe_merges_cache_priority(store):
    """prod_saturation_gate 依赖的 search_alphas_by_sharpe 默认 merge_corr_cache=True：
    返回行的 prod_correlation 应以权威表为准。

    注意：由于 set_corr_cache 会 mirror 覆盖 alphas，若两条路径都走 set_corr_cache，
    合并前后差异无法体现。此处直接手写权威表绕过 mirror，才能验证 merge 语义本身。
    """
    store.connection.execute(
        "UPDATE alphas SET sharpe=1.7 WHERE alpha_id='HAS_OLD'")
    store.connection.commit()
    # 直接写权威表，绕过 set_corr_cache 的 mirror → alphas 仍是 0.6678
    store.connection.execute(
        "INSERT INTO alpha_corr_cache (alpha_id, prod_correlation, source, checked_at) "
        "VALUES (?, ?, ?, ?) "
        "ON CONFLICT(alpha_id) DO UPDATE SET prod_correlation=excluded.prod_correlation, "
        "source=excluded.source, checked_at=excluded.checked_at",
        ("HAS_OLD", 0.83, "platform_sync", _hours_ago(1)))
    store.connection.commit()

    rows = store.search_alphas_by_sharpe(min_sharpe=1.5, limit=10)
    r = [x for x in rows if x["alpha_id"] == "HAS_OLD"][0]
    assert r["prod_correlation"] == 0.83  # 合并后来自 cache

    # 关掉合并 → 拿到 alphas 原值（回归测试用）
    rows2 = store.search_alphas_by_sharpe(min_sharpe=1.5, limit=10,
                                          merge_corr_cache=False)
    r2 = [x for x in rows2 if x["alpha_id"] == "HAS_OLD"][0]
    assert r2["prod_correlation"] == 0.6678
