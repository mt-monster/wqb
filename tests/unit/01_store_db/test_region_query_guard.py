# -*- coding: utf-8 -*-
"""region 作用域守卫 —— 防「跨区串号」回归（2026-10-06 事故后重建）。

## 事故
`fields` 表**无 region 列**，region 只能经 `datasets.region_id` 关联；同名数据集在最多
13 个区各有一个 dataset_id（`model38` 有 9 个）。实测踩坑：`LIKE '%star_val%'` 不带 region
命中 GLB/EUR/DEU 的行 ⇒ 误判「GBR `model38` 有 star_val 字段」；补上 region 又查不到
⇒ 被误读成「数据被并发会话重写」。**真相只是查询串了区。**

本文件两道防线：
  1. **行为层**：`RegionCatalog` 的区隔离 / 歧义拒绝（临时 DB，确定性）。
  2. **静态层**：扫全仓 `FROM fields` 是否带 region 过滤（**棘轮**：新增一处即失败）。
"""
import os
import sqlite3
import sys

import pytest

from wqb.region_catalog import (
    RegionAmbiguityError,
    RegionCatalog,
    dataset_names_in_region,
    field_names_in_region,
    resolve_dataset_ids,
)

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "..", ".."))

# 静态层基线：已存在于历史代码里的疑点（棘轮，只增不减地"允许"这些）
# 新增条目会让测试失败 → 强制新代码带 region 过滤。
GUARD_BASELINE = {
    "tools/atom_labeler.py:70",
    "tools/ingest_dataset_assets.py:152",
    "tools/validate_fields_batch.py:129",
    "tools/wave_gate.py:1463",
    "tools/wave_gate_pkg/gates_quality.py:120",
    "src/wqb/alpha_properties.py:345",
    "src/wqb/step_eval.py:200",
    "src/wqb/step_eval.py:213",
    "src/wqb/step_eval.py:221",
    "src/wqb/step_eval.py:222",
    "src/wqb/store/_backtest.py:380",
    "src/wqb/store/_expressions.py:95",
    "src/wqb/store/_field_catalog.py:380",
}
SKIP_DIRS = {"__pycache__", ".git", "attic", "legacy", ".venv", "venv",
             "site-packages", "node_modules", "dist", "build"}


@pytest.fixture()
def tmp_catalog(tmp_path):
    """两个区各有同名数据集 `model38`，字段不同 —— 串区就会露馅。"""
    db = tmp_path / "cat.db"
    con = sqlite3.connect(str(db))
    con.executescript("""
        CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE datasets (id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER,
                               category TEXT, field_count INTEGER, alpha_count INTEGER);
        CREATE TABLE fields (id INTEGER PRIMARY KEY, dataset_id INTEGER, field_name TEXT,
                             field_type TEXT, coverage REAL, alpha_count INTEGER);
        INSERT INTO regions VALUES (7,'GBR'), (8,'GLB');
        INSERT INTO datasets VALUES (264,'model38',7,'MODEL',71,10407),
                                    (893,'model38',8,'MODEL',200,8514);
        INSERT INTO fields VALUES (1,264,'star_val_piv_ratio','MATRIX',0.61,0),
                                  (2,264,'gb_only_field','MATRIX',0.9,0),
                                  (3,893,'star_val_buyback_yield','MATRIX',0.78,0);
    """)
    con.commit()
    con.close()
    return str(db)


# --------------------------------------------------------------------------
# 1. 行为层：区隔离
# --------------------------------------------------------------------------
def test_same_dataset_name_yields_region_specific_fields(tmp_catalog):
    with RegionCatalog(db=tmp_catalog) as rc:
        gbr = rc.field_names("model38", "GBR")
        glb = rc.field_names("model38", "GLB")
    assert gbr == ["gb_only_field", "star_val_piv_ratio"]
    assert glb == ["star_val_buyback_yield"]
    assert set(gbr).isdisjoint(glb), "同名数据集的跨区字段不得混合"


def test_field_exists_is_region_scoped(tmp_catalog):
    with RegionCatalog(db=tmp_catalog) as rc:
        assert rc.field_exists("GBR", "model38", "gb_only_field")
        assert not rc.field_exists("GLB", "model38", "gb_only_field")
        assert rc.field_exists("GLB", "model38", "star_val_buyback_yield")
        assert not rc.field_exists("GBR", "model38", "star_val_buyback_yield")


def test_dataset_ids_and_names_are_region_scoped(tmp_catalog):
    with RegionCatalog(db=tmp_catalog) as rc:
        assert rc.dataset_ids("GBR") == [264]
        assert rc.dataset_ids("GLB") == [893]
        assert rc.dataset_names("GBR") == ["model38"]
        assert rc.region_of_dataset(264) == "GBR"
        assert rc.region_of_dataset(893) == "GLB"


def test_region_ambiguity_is_rejected_not_silently_resolved(tmp_catalog):
    with RegionCatalog(db=tmp_catalog) as rc:
        with pytest.raises(RegionAmbiguityError):
            rc.region_of_dataset("model38")      # 两个区都有 → 必须显式指定
        txt = rc.explain("model38")
        assert "2 个区" in txt and "GBR" in txt and "GLB" in txt


def test_module_helpers_are_region_scoped(tmp_catalog):
    assert field_names_in_region("model38", "GBR", db=tmp_catalog) == [
        "gb_only_field", "star_val_piv_ratio"]
    assert dataset_names_in_region("GLB", db=tmp_catalog) == ["model38"]
    assert resolve_dataset_ids("model38", region="GBR", db=tmp_catalog) == [264]
    assert resolve_dataset_ids("model38", region="DEU", db=tmp_catalog) == []
    with pytest.raises(RegionAmbiguityError):
        resolve_dataset_ids("model38", db=tmp_catalog)   # 不给 region 且跨区 → 拒绝


def test_unknown_region_raises(tmp_catalog):
    with RegionCatalog(db=tmp_catalog) as rc:
        with pytest.raises(ValueError):
            rc.region_id("XXX")


# --------------------------------------------------------------------------
# 2. 静态层：全仓 `FROM fields` 的 region 过滤棘轮
# --------------------------------------------------------------------------
def _scan_bare_from_fields():
    import re
    hits = set()
    for root_name in ("tools", "tracking", "src"):
        root = os.path.join(REPO, root_name)
        if not os.path.isdir(root):
            continue
        for dirpath, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in files:
                if not fn.endswith(".py"):
                    continue
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, REPO).replace("\\", "/")
                try:
                    with open(p, encoding="utf-8", errors="ignore") as f:
                        txt = f.read()
                except OSError:
                    continue
                for m in re.finditer(r"FROM\s+fields", txt, re.I):
                    seg = txt[max(0, m.start() - 500): m.end() + 500]
                    if re.search(r"region_id", seg):
                        continue
                    hits.add(f"{rel}:{txt[:m.start()].count(chr(10)) + 1}")
    return hits


def test_no_new_unscoped_fields_query():
    """棘轮：允许基线内历史债，但**新增**一处缺 region 的 `FROM fields` 即失败。"""
    found = _scan_bare_from_fields()
    new = sorted(found - GUARD_BASELINE)
    assert not new, (
        "新增了未按 region 过滤的 `FROM fields` 查询（会静默串区）：\n  "
        + "\n  ".join(new)
        + "\n请改为经 `wqb.region_catalog.RegionCatalog`，或显式带 `d.region_id=?`。"
    )


def test_guard_baseline_has_no_stale_entries():
    """基线里的条目若已修复（扫描不到）应删除，防止基线无限膨胀。"""
    found = _scan_bare_from_fields()
    stale = sorted(GUARD_BASELINE - found)
    if stale:
        pytest.skip("以下基线条目已不存在（建议从 GUARD_BASELINE 移除）：\n  "
                    + "\n  ".join(stale))
