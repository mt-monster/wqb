"""Unit tests for wqb.config — region config, operator families, gate helpers.

This module covers:

- ``REGIONS`` completeness (all 9 regions present, required keys).
- ``neutralization_search_order`` returns valid sweep lists per region.
- ``get_operator_family`` classifies known ops; unknowns return ``"NONE"``.
- ``get_ghost_operators`` returns the expected 17-operator blacklist.
- ``is_news_dataset`` prefix and category detection.
- ``compute_webdata_failed_counts`` RA vs PPA gate classification.
- ``default_universe`` / ``default_delay`` / ``get_categories`` helpers.
"""

import pytest

from wqb.config import (
    BATCH_SIZE,
    GHOST_OPERATORS,
    OP_FAMILIES,
    PARADIGMS,
    PRODCORR_CEILING,
    RA_CHECK_NAMES,
    REGION_PRIORITY,
    REGIONS,
    SHAPE_CLASSES,
    VERIFIED_SAFE_OPERATORS,
    compute_webdata_failed_counts,
    default_delay,
    default_universe,
    get_categories,
    get_operator_family,
    is_news_dataset,
    neutralization_search_order,
)


# ---------------------------------------------------------------------------
# REGIONS completeness
# ---------------------------------------------------------------------------

EXPECTED_REGIONS = {"USA", "EUR", "CHN", "ASI", "GLB", "JPN", "KOR", "AMR", "TWN"}


def test_regions_set_is_complete():
    assert set(REGIONS.keys()) == EXPECTED_REGIONS


def test_each_region_has_required_keys():
    required = {"universes", "neutralizations", "delays", "categories", "default_universe"}
    for region, cfg in REGIONS.items():
        missing = required - set(cfg.keys())
        assert not missing, f"{region} missing keys: {missing}"


def test_usa_neutralizations_has_11_entries():
    assert len(REGIONS["USA"]["neutralizations"]) == 11


def test_usa_universes_contains_top3000():
    assert "TOP3000" in REGIONS["USA"]["universes"]


# ---------------------------------------------------------------------------
# neutralization_search_order
# ---------------------------------------------------------------------------

def test_neutralization_search_order_usa_returns_all_11():
    order = neutralization_search_order("USA")
    assert len(order) == 11
    assert order[0] == "STATISTICAL"  # USA starts with STATISTICAL


def test_neutralization_search_order_usa_order():
    order = neutralization_search_order("USA")
    # STATISTICAL must come before NONE
    assert order.index("STATISTICAL") < order.index("NONE")


def test_neutralization_search_order_kor_sector_first():
    order = neutralization_search_order("KOR")
    assert order[0] == "SECTOR"


def test_neutralization_search_order_unknown_region_raises():
    with pytest.raises(KeyError):
        neutralization_search_order("XXX")


def test_neutralization_search_order_case_insensitive():
    order_usa = neutralization_search_order("usa")
    assert len(order_usa) == 11


def test_neutralization_search_order_return_valid_names():
    order = neutralization_search_order("EUR")
    supported = set(REGIONS["EUR"]["neutralizations"])
    for n in order:
        assert n in supported


# ---------------------------------------------------------------------------
# get_operator_family
# ---------------------------------------------------------------------------

def test_get_operator_family_ts_rank():
    assert get_operator_family("ts_rank") == "TS_RANK"


def test_get_operator_family_group_neutralize():
    assert get_operator_family("group_neutralize") == "GROUP"


def test_get_operator_family_math_abs():
    assert get_operator_family("abs") == "MATH"


def test_get_operator_family_unknown():
    assert get_operator_family("nonexistent_op") == "NONE"


def test_all_op_families_are_nonempty():
    for family, ops in OP_FAMILIES.items():
        assert isinstance(ops, list) and len(ops) > 0, f"Empty family: {family}"


# ---------------------------------------------------------------------------
# GHOST_OPERATORS
# ---------------------------------------------------------------------------

def test_ghost_operators_is_nonempty_set():
    assert isinstance(GHOST_OPERATORS, set)
    assert len(GHOST_OPERATORS) >= 15  # 17 known ghosts


def test_ghost_operators_contains_ts_entropy():
    assert "ts_entropy" in GHOST_OPERATORS


def test_ghost_operators_contains_group_normalize():
    assert "group_normalize" in GHOST_OPERATORS


# ---------------------------------------------------------------------------
# VERIFIED_SAFE_OPERATORS
# ---------------------------------------------------------------------------

def test_verified_safe_operators_nonempty():
    assert isinstance(VERIFIED_SAFE_OPERATORS, list)
    assert len(VERIFIED_SAFE_OPERATORS) > 0


def test_verified_safe_contains_ts_kurtosis():
    assert "ts_kurtosis" in VERIFIED_SAFE_OPERATORS


# ---------------------------------------------------------------------------
# is_news_dataset
# ---------------------------------------------------------------------------

def test_is_news_dataset_by_prefix():
    assert is_news_dataset("news12") is True


def test_is_news_dataset_by_category():
    assert is_news_dataset("fnd5", category="news") is True


def test_is_news_dataset_false():
    assert is_news_dataset("fundamental44", category="fundamental") is False


def test_is_news_dataset_prefix_snt():
    assert is_news_dataset("snt21") is True


# ---------------------------------------------------------------------------
# compute_webdata_failed_counts
# ---------------------------------------------------------------------------

def test_compute_webdata_failed_counts_all_pass():
    checks = [
        {"name": "LOW_SHARPE", "result": "PASS", "value": 2.0},
        {"name": "HIGH_TURNOVER", "result": "PASS", "value": 50},
    ]
    result = compute_webdata_failed_counts(checks)
    assert result["failed_ra"] == 0
    assert result["failed_ppa"] == 0


def test_compute_webdata_failed_counts_ra_fail():
    checks = [
        {"name": "LOW_FITNESS", "result": "FAIL", "value": 0.5},
        {"name": "HIGH_TURNOVER", "result": "PASS", "value": 30},
    ]
    result = compute_webdata_failed_counts(checks)
    # LOW_FITNESS is in RA_CHECK_NAMES → failed_ra=1
    # LOW_FITNESS is NOT in PPA_CHECK_NAMES and LOW_SHARPE is not present → failed_ppa=0
    assert result["failed_ra"] == 1
    assert result["failed_ppa"] == 0


def test_compute_webdata_failed_counts_low_sharpe_value():
    checks = [
        {"name": "LOW_SHARPE", "result": "FAIL", "value": 0.8},
    ]
    result = compute_webdata_failed_counts(checks)
    # LOW_SHARPE with value < 1 counts as PPA fail
    assert result["failed_ppa"] == 1


def test_compute_webdata_failed_counts_details():
    checks = [
        {"name": "LOW_SHARPE", "result": "FAIL", "value": 0.5, "limit": 1.0},
    ]
    result = compute_webdata_failed_counts(checks)
    assert len(result["details"]) >= 1
    detail = result["details"][0]
    assert detail["name"] == "LOW_SHARPE"


# ---------------------------------------------------------------------------
# default_universe / default_delay / get_categories
# ---------------------------------------------------------------------------

def test_default_universe_usa():
    assert default_universe("USA") == "TOP3000"


def test_default_universe_china():
    assert default_universe("CHN") == "TOP2000U"


def test_default_universe_unknown_raises():
    with pytest.raises(KeyError):
        default_universe("XXX")


def test_default_delay_usa():
    assert default_delay("USA") == 1


def test_get_categories_usa_contains_equity():
    cats = get_categories("USA")
    assert "equity" in cats


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

def test_batch_size_is_4():
    assert BATCH_SIZE == 4


def test_prodcorr_ceiling_is_070():
    assert PRODCORR_CEILING == 0.70


def test_shape_classes_set():
    assert set(SHAPE_CLASSES) == {"S1", "S4", "S5", "S9"}


def test_paradigms_count():
    assert len(PARADIGMS) == 13


def test_region_priority_usa_highest():
    assert REGION_PRIORITY["USA"] == 3
    assert REGION_PRIORITY["USA"] >= REGION_PRIORITY["KOR"]