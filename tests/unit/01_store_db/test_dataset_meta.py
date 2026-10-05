"""Unit tests for FieldCatalogMixin — 数据集级元数据与 catalog 枚举（2026-10-01）。

背景：`tools/fetch_dataset_assets.py` 从「拉取 → data/dataset_assets/*.json → 另一脚本入库」
的两步式中转改为直连入库，新增两个库层方法：
  - `upsert_dataset_meta`：写数据集级行（含尚未拉字段的数据集）
  - `list_catalog_datasets`：按 region 枚举已有 catalog 的数据集（文件面枚举的 DB 替代）
本文件锁定它们的契约与幂等性。
"""

import pytest

from wqb.store import CampaignStore


@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "camp.db"))
    yield db
    db.close()


PLATFORM_DS = {
    "id": "fundamental1",
    "name": "Management and Executive Data",
    "category": {"id": "fundamental", "name": "Fundamental"},
    "fieldCount": 205,
    "coverage": 0.87,
    "alphaCount": 239,
    "valueScore": 4.0,
    "pyramidMultiplier": 1.1,
    "delay": 1,
}


def test_upsert_dataset_meta_accepts_platform_keys(store):
    """平台原始键（id/category dict/fieldCount/valueScore/…）直接可用。"""
    out = store.upsert_dataset_meta("USA", PLATFORM_DS)
    assert out["dataset"] == "fundamental1"
    row = store.connection.execute(
        "SELECT category, field_count, coverage, alpha_count, value_score, "
        "pyramid_multiplier, delay FROM datasets WHERE name='fundamental1'"
    ).fetchone()
    assert tuple(row) == ("fundamental", 205, 0.87, 239, 4.0, 1.1, 1)


def test_upsert_dataset_meta_is_idempotent_and_updates_in_place(store):
    """同 (name, region) 不产生第二行；二次调用只更新显式给的字段。"""
    store.upsert_dataset_meta("USA", PLATFORM_DS)
    store.upsert_dataset_meta("USA", {"id": "fundamental1", "coverage": 0.95})
    rows = store.connection.execute(
        "SELECT coverage, field_count FROM datasets WHERE name='fundamental1'"
    ).fetchall()
    assert len(rows) == 1
    assert rows[0][0] == 0.95        # 更新
    assert rows[0][1] == 205         # 未传的字段保留（extra 只覆盖显式键）


def test_upsert_dataset_meta_does_not_write_a_fieldless_catalog_json(store):
    """`catalog_json` 是字段目录存放位——数据集级元数据不得写进去。

    否则 `get_field_catalog` 的 catalog_json 短路分支会返回「无 fields 的伪 catalog」，
    下游 `gate.load_whitelist` 会把它当成空字段白名单。
    """
    store.upsert_dataset_meta("USA", PLATFORM_DS)
    blob = store.connection.execute(
        "SELECT catalog_json FROM datasets WHERE name='fundamental1'"
    ).fetchone()[0]
    assert not blob
    cat = store.get_field_catalog("USA", "fundamental1")
    assert cat is not None and cat["fields"] == []   # 无字段 → 空 catalog，不是伪 catalog


def test_upsert_dataset_meta_then_fields_yields_full_catalog(store):
    """元数据先落、字段后到 → get_field_catalog 返回真实字段目录。"""
    store.upsert_dataset_meta("USA", PLATFORM_DS)
    store.upsert_field_catalog("USA", {"dataset": "fundamental1", "fields": [
        {"id": "annual_base_salary", "type": "MATRIX", "coverage": 0.2},
        {"id": "board_network", "type": "VECTOR", "coverage": 0.1},
    ]})
    cat = store.get_field_catalog("USA", "fundamental1")
    assert len(cat["fields"]) == 2
    assert {f["id"] for f in cat["fields"]} == {"annual_base_salary", "board_network"}


def test_upsert_dataset_meta_requires_id(store):
    with pytest.raises(ValueError):
        store.upsert_dataset_meta("USA", {"coverage": 0.5})


def test_list_catalog_datasets_only_returns_datasets_with_fields(store):
    """枚举口径 = 有 ≥1 字段行（仅建元数据行的数据集不算「有 catalog」）。"""
    store.upsert_dataset_meta("USA", {"id": "meta_only"})
    store.upsert_field_catalog("USA", {"dataset": "model219", "fields": [{"id": "a"}]})
    store.upsert_field_catalog("USA", {"dataset": "news12", "fields": [{"id": "b"}]})
    assert store.list_catalog_datasets("USA") == ["model219", "news12"]


def test_list_catalog_datasets_is_region_scoped(store):
    store.upsert_field_catalog("USA", {"dataset": "usa_ds", "fields": [{"id": "a"}]})
    store.upsert_field_catalog("KOR", {"dataset": "kor_ds", "fields": [{"id": "b"}]})
    assert store.list_catalog_datasets("USA") == ["usa_ds"]
    assert store.list_catalog_datasets("KOR") == ["kor_ds"]


def test_list_catalog_datasets_unknown_region_is_empty_and_side_effect_free(store):
    """未知 region 返回 []，且不像 `_ensure_region` 那样建行。"""
    assert store.list_catalog_datasets("NOPE") == []
    n = store.connection.execute("SELECT COUNT(*) FROM regions").fetchone()[0]
    assert n == 0
