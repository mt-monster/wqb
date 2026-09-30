# -*- coding: utf-8 -*-
"""build_field_index 的离线单测（不触网）：catalog 构造 + 本地字段计数。"""
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

import build_field_index as bfi  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402


def test_build_catalog_shape():
    raw = [
        {"id": "f1", "type": "MATRIX", "coverage": 0.9, "userCount": 3,
         "alphaCount": 10, "description": "x" * 300},
        {"id": None},  # 无 id 的条目应被丢弃
    ]
    cat = bfi.build_catalog("GLB", "analyst14", raw)
    assert cat["dataset"] == "analyst14"
    assert cat["region"] == "GLB"
    assert cat["field_count"] == 1
    assert cat["fields"][0]["id"] == "f1"
    assert len(cat["fields"][0]["description"]) == 120  # 截断到 120


def test_local_field_counts_keyed_by_region_and_name(tmp_path):
    store = CampaignStore(str(tmp_path / "c.db"))
    conn = store.connection
    conn.execute("INSERT INTO regions (name) VALUES ('KOR')")
    rid = conn.execute("SELECT id FROM regions WHERE name='KOR'").fetchone()[0]
    conn.execute("INSERT INTO datasets (name, region_id) VALUES ('analyst14', ?)", (rid,))
    dsid = conn.execute("SELECT id FROM datasets WHERE name='analyst14'").fetchone()[0]
    for f in ("anl14_a", "anl14_b"):
        conn.execute("INSERT INTO fields (dataset_id, field_name) VALUES (?, ?)", (dsid, f))
    conn.commit()
    counts = bfi.local_field_counts(store)
    assert counts[("KOR", "analyst14")] == 2
    store.close()
