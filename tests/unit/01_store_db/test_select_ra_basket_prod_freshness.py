# -*- coding: utf-8 -*-
"""select_ra_basket 的 prod 新鲜度护栏（2026-10-03）。

背景：RA 步 1 的分流判据是「篮子条数 ≥ target 且覆盖 ≥ 3 座未点亮塔 → 跳步 7/8」。库里记录的 prod 值会过期——
IND 旧候选 09-19~23 实测 0.51–0.67，10-02 复测**全部** 0.83–0.99（社区同族 alpha 持续进 book），
拿陈旧值数篮子会把「库存足够」判错。本文件守三件事：

1. ``classify_prod`` 的五种状态（含「没有测量时间」按陈旧算、「旧高值」按已知撞墙算）；
2. ``prod_freshness_index`` 只读 ``alphas`` 表，查不到的 id 不进结果；
3. 两个新命令行参数存在且默认值是文档里写的那个（``--prod-max-age-days`` / ``--keep-prod-blocked``）。
"""
import datetime as dt
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

import select_ra_basket as sb  # noqa: E402

NOW = dt.datetime(2026, 10, 3, 12, 0, 0)


def _ago(days):
    return (NOW - dt.timedelta(days=days)).isoformat(timespec="seconds")


# ----------------------------------------------------------------------------- classify_prod

def test_unmeasured_when_prod_is_null():
    assert sb.classify_prod(None, _ago(0), 2, NOW) == ("unmeasured", None)
    assert sb.classify_prod(None, None, 2, NOW) == ("unmeasured", None)


def test_fresh_ok_and_fresh_blocked_split_at_the_ceiling():
    st, age = sb.classify_prod(0.6999, _ago(1), 2, NOW, ceiling=0.70)
    assert st == "fresh_ok" and 0.99 < age < 1.01
    assert sb.classify_prod(0.70, _ago(1), 2, NOW, ceiling=0.70)[0] == "fresh_blocked"   # 严格不等式的反面：= 上限即撞墙
    assert sb.classify_prod(0.93, _ago(0.1), 2, NOW, ceiling=0.70)[0] == "fresh_blocked"


def test_stale_values_are_void_even_when_they_look_good():
    """IND 实证：旧候选 0.51–0.67 → 复测 0.83–0.99。陈旧的「好值」不能算已核。"""
    assert sb.classify_prod(0.55, _ago(3), 2, NOW, ceiling=0.70)[0] == "stale_ok"
    assert sb.classify_prod(0.55, _ago(14), 2, NOW, ceiling=0.70)[0] == "stale_ok"


def test_stale_high_value_is_treated_as_known_blocked():
    assert sb.classify_prod(0.82, _ago(9), 2, NOW, ceiling=0.70)[0] == "stale_blocked"


def test_missing_or_unparseable_timestamp_counts_as_stale_not_fresh():
    assert sb.classify_prod(0.50, None, 2, NOW, ceiling=0.70) == ("stale_ok", None)
    assert sb.classify_prod(0.50, "不是时间", 2, NOW, ceiling=0.70) == ("stale_ok", None)
    assert sb.classify_prod(0.90, "", 2, NOW, ceiling=0.70) == ("stale_blocked", None)


def test_age_boundary_is_inclusive():
    assert sb.classify_prod(0.5, _ago(2), 2, NOW, ceiling=0.70)[0] == "fresh_ok"
    assert sb.classify_prod(0.5, _ago(2.01), 2, NOW, ceiling=0.70)[0] == "stale_ok"


def test_default_ceiling_comes_from_config():
    from wqb.config import PRODCORR_CEILING
    assert sb.classify_prod(PRODCORR_CEILING, _ago(0), 2, NOW)[0] == "fresh_blocked"
    assert sb.classify_prod(PRODCORR_CEILING - 0.01, _ago(0), 2, NOW)[0] == "fresh_ok"


# ----------------------------------------------------------------------------- prod_freshness_index

@pytest.fixture
def conn(tmp_path):
    db = tmp_path / "wqb.db"
    CampaignStore(str(db)).close()
    c = sqlite3.connect(str(db))
    c.execute("INSERT INTO regions (id, name) VALUES (1, 'TST')")
    c.execute("INSERT INTO datasets (id, name, region_id) VALUES (10, 'ds', 1)")
    rows = [
        ("A_FRESH_OK", 0.55, _ago(0.5)),
        ("A_FRESH_BAD", 0.81, _ago(1)),
        ("A_STALE_OK", 0.52, _ago(20)),
        ("A_STALE_BAD", 0.93, _ago(20)),
        ("A_UNDATED", 0.60, None),
        ("A_NONE", None, None),
    ]
    for aid, prod, ts in rows:
        c.execute(
            "INSERT INTO alphas (alpha_id, expression, region_id, dataset_id, prod_correlation, corr_checked_at) "
            "VALUES (?, 'rank(x)', 1, 10, ?, ?)", (aid, prod, ts))
    c.commit()
    yield c
    c.close()


def test_index_classifies_every_known_alpha_and_skips_unknown_ids(conn):
    ids = ["A_FRESH_OK", "A_FRESH_BAD", "A_STALE_OK", "A_STALE_BAD", "A_UNDATED", "A_NONE", "NOT_IN_DB"]
    idx = sb.prod_freshness_index(conn, ids, max_age_days=2, now=NOW)
    assert {k: v["status"] for k, v in idx.items()} == {
        "A_FRESH_OK": "fresh_ok",
        "A_FRESH_BAD": "fresh_blocked",
        "A_STALE_OK": "stale_ok",
        "A_STALE_BAD": "stale_blocked",
        "A_UNDATED": "stale_ok",
        "A_NONE": "unmeasured",
    }
    assert "NOT_IN_DB" not in idx
    assert idx["A_FRESH_OK"]["prod"] == 0.55 and idx["A_FRESH_OK"]["age_days"] == 0.5
    assert idx["A_UNDATED"]["age_days"] is None


def test_index_handles_more_ids_than_one_sqlite_chunk(conn):
    ids = [f"GHOST_{i}" for i in range(1200)] + ["A_FRESH_OK"]
    idx = sb.prod_freshness_index(conn, ids, max_age_days=2, now=NOW)
    assert list(idx) == ["A_FRESH_OK"]


def test_index_deduplicates_and_ignores_empty_ids(conn):
    idx = sb.prod_freshness_index(conn, ["A_FRESH_OK", "A_FRESH_OK", None, ""], max_age_days=2, now=NOW)
    assert list(idx) == ["A_FRESH_OK"]


# ----------------------------------------------------------------------------- CLI 契约

def test_cli_flags_exist_with_documented_defaults(monkeypatch):
    seen = {}

    async def fake_main_async(a):
        seen["a"] = a

    monkeypatch.setattr(sb, "main_async", fake_main_async)
    monkeypatch.setattr(sys, "argv", ["select_ra_basket.py", "cands.json"])
    sb.main()
    a = seen["a"]
    assert a.prod_max_age_days == sb.PROD_FRESH_DAYS == 2
    assert a.keep_prod_blocked is False

    monkeypatch.setattr(sys, "argv", ["select_ra_basket.py", "cands.json",
                                      "--prod-max-age-days", "5", "--keep-prod-blocked"])
    sb.main()
    assert seen["a"].prod_max_age_days == 5.0 and seen["a"].keep_prod_blocked is True
