# -*- coding: utf-8 -*-
"""atom/combined 分类（wqb.expression.atom）+ 写入期自动打标（upsert_expressions）回归。"""
import os
import sys
import tempfile

import pytest

from wqb.expression.atom import classify_atom, extract_fields
from wqb.store import CampaignStore


# --------------------------------------------------------------------------
# 抽取器：kwarg / 字符串值 / 多行变量 不得被当作数据字段
# --------------------------------------------------------------------------
def test_extract_fields_drops_kwargs_and_string_values():
    e = 'quantile(subtract(fnd86_a, fnd86_b), driver="gaussian", sigma=1.0)'
    assert extract_fields(e) == ["fnd86_a", "fnd86_b"]


def test_extract_fields_drops_string_enum():
    e = 'rank(bucket(rank(x), range="0,1,0.2"))'
    assert extract_fields(e) == ["x"]


def test_extract_fields_drops_multiline_variables():
    e = "M5 = close;\nB = volume;\nadd(M5, B)"
    assert extract_fields(e) == ["close", "volume"]


def test_extract_fields_keeps_base_and_grouping():
    # 基础行情与分组键保留给解析器判定，不在抽取阶段剔除
    e = "group_rank(anl14_x, industry)"
    assert extract_fields(e) == ["anl14_x", "industry"]


# --------------------------------------------------------------------------
# 分类：atom / combined / unknown
# --------------------------------------------------------------------------
FAKE = {
    "anl14_a": "analyst14", "anl14_b": "analyst14",
    "news_x": "news104", "pv_y": "pv29", "pv1_x": "pv1", "macro_z": "macro12",
}


def test_classify_atom_single_dataset():
    assert classify_atom("rank(anl14_a)", FAKE)["verdict"] == "atom"
    assert classify_atom("anl14_a - anl14_b", FAKE)["verdict"] == "atom"


def test_classify_atom_base_only_is_atom():
    # 官方口径：基础行情字段属 pv1 数据集；纯 pv1 信号是单数据集 ⇒ atom
    res = classify_atom("rank(returns)", FAKE)
    assert res["verdict"] == "atom"
    assert res["datasets"] == ["pv1"]


def test_classify_atom_pv1_field_plus_base_is_still_atom():
    # 纠正点 a：pv1 字段 + returns 是同一个数据集，不得数成两个
    m = dict(FAKE, pv1_px="pv1")
    res = classify_atom("rank(pv1_px - returns)", m)
    assert res["verdict"] == "atom"
    assert res["datasets"] == ["pv1"]


def test_classify_combined_cross_dataset():
    res = classify_atom("ts_co_skewness(news_x, returns, 20)", FAKE)
    assert res["verdict"] == "combined"
    assert set(res["datasets"]) == {"news104", "pv1"}
    assert classify_atom("regression_neut(anl14_a, pv_y)", FAKE)["verdict"] == "combined"


def test_classify_grouping_key_is_neutral():
    for g in ("country", "exchange", "market", "sector", "industry", "subindustry"):
        assert classify_atom("group_rank(anl14_a, %s)" % g, FAKE)["verdict"] == "atom"


def test_classify_grouping_key_beyond_official_six_is_not_neutral():
    # 纠正点 c：官方只豁免 6 个；region 之类不再无条件中性（不在字段表 ⇒ unknown）
    assert classify_atom("group_rank(anl14_a, region)", FAKE)["verdict"] == "unknown"


def test_classify_pv1_operators_break_atom():
    # 纠正点 b：官方原文「inst_pnl() / convert() 视为使用 pv1」
    for e in ("inst_pnl(anl14_a)", "convert(anl14_a)"):
        res = classify_atom(e, FAKE)
        assert res["verdict"] == "combined", e
        assert res["datasets"] == ["analyst14", "pv1"], e
        assert res["pv1_operators"] == [e.split("(")[0]]
    # pv1 集自身用 inst_pnl 仍是单数据集
    assert classify_atom("inst_pnl(pv1_x)", FAKE)["verdict"] == "atom"


def test_classify_size_arg_breaks_atom():
    # 用 pv1 字段当算子参数（非豁免）同样破坏 ATOM
    res = classify_atom("vector_neut(anl14_a, rank(cap))", FAKE)
    assert res["verdict"] == "combined"
    assert set(res["datasets"]) == {"analyst14", "pv1"}


def test_classify_unknown_field():
    res = classify_atom("rank(totally_unknown_field_xyz)", FAKE)
    assert res["verdict"] == "unknown"
    assert res["unknown_fields"] == ["totally_unknown_field_xyz"]


# --------------------------------------------------------------------------
# 写入期自动打标：upsert_expressions 落库即带 atom_flag
# --------------------------------------------------------------------------
@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "camp.db"))
    conn = db.connection
    conn.execute("INSERT INTO regions (name) VALUES ('TEST')")
    rid = conn.execute("SELECT id FROM regions WHERE name='TEST'").fetchone()[0]
    for ds, fld in (("analyst14", "anl14_a"), ("news104", "news_x")):
        conn.execute("INSERT INTO datasets (name, region_id) VALUES (?, ?)", (ds, rid))
        dsid = conn.execute(
            "SELECT id FROM datasets WHERE name=?", (ds,)).fetchone()[0]
        conn.execute(
            "INSERT INTO fields (dataset_id, field_name) VALUES (?, ?)", (dsid, fld))
    conn.commit()
    yield db
    db.close()


def test_upsert_writes_atom_flag(store):
    store.upsert_expressions(
        "TEST", "1",
        ["rank(returns)", "anl14_a - returns", "ts_co_skewness(news_x, returns, 20)"],
        dataset="analyst14",
    )
    got = {
        r["expression"]: (r["atom_flag"], r["atom_n_datasets"])
        for r in store.list_expressions("TEST", "1")
    }
    assert got["rank(returns)"] == ("atom", 1)
    assert got["anl14_a - returns"] == ("combined", 2)
    assert got["ts_co_skewness(news_x, returns, 20)"] == ("combined", 2)


def test_upsert_atom_flag_idempotent(store):
    items = ["rank(returns)", "anl14_a - returns"]
    store.upsert_expressions("TEST", "1", items, dataset="analyst14")
    store.upsert_expressions("TEST", "1", items, dataset="analyst14")
    rows = store.list_expressions("TEST", "1")
    assert len(rows) == 2  # 同 wave 同 expr 不重复插入
    assert {r["atom_flag"] for r in rows} == {"atom", "combined"}
