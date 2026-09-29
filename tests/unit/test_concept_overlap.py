# -*- coding: utf-8 -*-
"""tools/concept_overlap.py：EX-01 的「概念重叠检查」有了对应的程序（字段集合 + 骨架指纹，与闸 PF / prod-first 同源）。"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import concept_overlap as C  # noqa: E402

BOOK = [
    {"alpha_id": "A1", "expression": "rank(ts_zscore(snt21_pos_mean, 66))"},
    {"alpha_id": "A2", "expression": "group_rank(ts_delta(fnd28_ebit, 22), industry)"},
    {"alpha_id": "A3", "expression": "rank(ts_zscore(divide(snt21_pos_mean, snt21_pos_max), 22))"},
]


def test_same_skeleton_and_half_the_fields_is_high():
    out = C.compare("rank(ts_zscore(snt21_pos_max, 252))", BOOK)
    assert out["verdict"] == "HIGH"
    top = out["overlaps"][0]
    assert top["alpha_id"] == "A3" and top["same_skeleton"] is True and top["jaccard"] == 0.5
    assert top["shared_fields"] == ["snt21_pos_max"]
    assert "换概念" in out["advice"]


def test_different_skeleton_with_half_the_fields_is_medium():
    out = C.compare("rank(ts_rank(snt21_pos_max, 66))", BOOK)
    assert out["verdict"] == "MEDIUM" and out["overlaps"][0]["same_skeleton"] is False


def test_identical_field_set_is_high_even_with_another_skeleton():
    out = C.compare("group_rank(ts_delta(snt21_pos_mean, 5), industry)", BOOK)
    assert out["verdict"] == "HIGH" and out["overlaps"][0]["alpha_id"] == "A1"


def test_small_shared_fraction_and_other_skeleton_is_low():
    out = C.compare("group_rank(fnd28_ebit + fnd28_sales + fnd28_cf, industry)", BOOK)
    assert out["verdict"] == "LOW" and out["overlaps"][0]["jaccard"] == pytest.approx(0.333, abs=1e-3)


def test_no_shared_fields_is_clear_and_says_to_still_measure():
    out = C.compare("rank(ts_zscore(mdl135_d01_icc, 66))", BOOK)
    assert out["verdict"] == "CLEAR" and out["overlaps"] == [] and "实测" in out["advice"]


def test_target_alpha_is_excluded_from_its_own_book():
    out = C.compare("rank(ts_zscore(snt21_pos_mean, 66))", BOOK, exclude_alpha_id="A1")
    assert all(o["alpha_id"] != "A1" for o in out["overlaps"])


def test_jaccard_threshold_is_adjustable():
    strict = C.compare("rank(ts_zscore(snt21_pos_max, 252))", BOOK, jaccard_high=0.9)
    assert strict["overlaps"][0]["level"] == "MEDIUM"       # 同骨架但 0.5 < 0.9 → 降为 MEDIUM


def test_definitions_are_the_same_functions_the_gates_use():
    """字段集合 / 骨架指纹不另写一份：与 campaign_intel / wave_gate 的实现逐字一致。"""
    from campaign_intel import _pf_family as field_family
    from wave_gate import _pf_family as skeleton_fp
    expr = "quantile(ts_regression(oth423_find,group_mean(oth423_find,vec_max(shrt3_bar),country),90))"
    fields, skel = C._families(expr)
    assert "+".join(sorted(fields)) == field_family(expr) == "oth423_find+shrt3_bar"
    assert skel == skeleton_fp(expr) == "quantile→ts_regression"


@pytest.fixture()
def tmp_db(tmp_path):
    p = tmp_path / "wqb.db"
    c = sqlite3.connect(p)
    c.executescript("""
        CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE alphas(alpha_id TEXT, expression TEXT, status TEXT, prod_correlation REAL, region_id INTEGER);
        INSERT INTO regions VALUES (1,'KOR'),(2,'USA');
        INSERT INTO alphas VALUES ('K1','rank(ts_zscore(snt21_pos_mean, 66))','ACTIVE',0.61,1);
        INSERT INTO alphas VALUES ('K2','rank(ts_zscore(fnd28_ebit, 66))','UNSUBMITTED',NULL,1);
        INSERT INTO alphas VALUES ('U1','rank(ts_zscore(snt21_pos_mean, 66))','ACTIVE',NULL,2);
    """)
    c.commit()
    c.close()
    return str(p)


def test_book_from_db_is_region_scoped_and_active_only(tmp_db):
    book = C.load_book_from_db("kor", db_path=tmp_db)
    assert [b["alpha_id"] for b in book] == ["K1"] and book[0]["prod_correlation"] == 0.61


def test_cli_with_alpha_id_and_db(tmp_db, monkeypatch, capsys):
    monkeypatch.setenv("WQB_DB_PATH", tmp_db)
    assert C.main(["--region", "KOR", "--alpha-id", "K2"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["region"] == "KOR" and out["target"]["alpha_id"] == "K2" and out["verdict"] == "CLEAR"


def test_cli_book_json_and_unknown_alpha(tmp_path, monkeypatch, capsys, tmp_db):
    monkeypatch.setenv("WQB_DB_PATH", tmp_db)
    bj = tmp_path / "book.json"
    bj.write_text(json.dumps(BOOK), encoding="utf-8")
    assert C.main(["--region", "KOR", "--expr", "rank(ts_zscore(snt21_pos_max, 252))", "--book-json", str(bj)]) == 0
    assert json.loads(capsys.readouterr().out)["verdict"] == "HIGH"
    assert C.main(["--region", "KOR", "--alpha-id", "NOPE"]) == 2       # 不在 alphas 表 → 让调用方改用 --expr
