# -*- coding: utf-8 -*-
"""expressions.family 持久化回归（2026-10-20 P0-1 附带修复）。

背景：GEM runner（`trailSomeAlphas/run_pipeline.py`）自 2026-10-01 "family 落库" P0 起
就向 `upsert_expressions` 传 `[{"expression": e, "family": fam}, …]`，但 store 侧
`_sql_update/_sql_insert` 从未包含 family 列 → 键被静默丢弃。实测生产库该列仅
112/75464 行有值（GLB/KOR，均为一次性回写），「DB 族历史」对其余 99.85% 的行不存在。
本修复：① `_schema.ensure_schema` 补 family 列（新建库自带）；② `upsert_expressions`
写入 family（UPDATE 端 COALESCE 保旧值——没带 ≠ 清空）。

消费方 = `tools/full_coverage_gate.load_db_families`（模板族全量闸的 DB 历史）。
"""
import pytest

from wqb.store import CampaignStore


@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "camp.db"))
    conn = db.connection
    conn.execute("INSERT INTO regions (name) VALUES ('TEST')")
    conn.commit()
    yield db
    db.close()


def _families(db, wave="1"):
    rows = db.connection.execute(
        "SELECT expression, family FROM expressions WHERE wave=? ORDER BY expression",
        (wave,),
    ).fetchall()
    return {r[0]: r[1] for r in rows}


def test_ensure_schema_creates_family_column(store):
    cols = {r[1] for r in store.connection.execute("PRAGMA table_info(expressions)")}
    assert "family" in cols


def test_upsert_dict_items_persist_family(store):
    store.upsert_expressions(
        "TEST", "1",
        [
            {"expression": "rank(close)", "family": "F1_snr_cash"},
            {"expression": "rank(open)", "family": "F2_rev"},
            "rank(high)",  # 纯字符串条目：family 应为 NULL（不阻断）
        ],
        dataset="ds1",
    )
    fam = _families(store)
    assert fam["rank(close)"] == "F1_snr_cash"
    assert fam["rank(open)"] == "F2_rev"
    assert fam["rank(high)"] is None


def test_reupsert_without_family_preserves_existing(store):
    """没带 ≠ 清空：harvest/选波等后续 upsert 不带 family 时不得抹掉已有标签。"""
    store.upsert_expressions(
        "TEST", "1", [{"expression": "rank(close)", "family": "F1_snr_cash"}],
        dataset="ds1",
    )
    store.upsert_expressions("TEST", "1", ["rank(close)"], dataset="ds1")
    assert _families(store)["rank(close)"] == "F1_snr_cash"


def test_reupsert_with_new_family_overwrites(store):
    store.upsert_expressions(
        "TEST", "1", [{"expression": "rank(close)", "family": "old"}], dataset="ds1",
    )
    store.upsert_expressions(
        "TEST", "1", [{"expression": "rank(close)", "family": "new"}], dataset="ds1",
    )
    assert _families(store)["rank(close)"] == "new"