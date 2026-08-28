"""Unit tests for wqb.store.CampaignStore — campaign artifact DB writes."""

import pytest

from wqb.store import CampaignStore


@pytest.fixture
def store(tmp_path):
    db = CampaignStore(str(tmp_path / "camp.db"))
    yield db
    db.close()


def test_upsert_expressions_roundtrip(store):
    out = store.upsert_expressions(
        "EUR", "39", ["rank(close)", "rank(volume)"],
        dataset="multi_horizon_alpha", status="gem",
    )
    assert out["n"] == 2
    rows = store.list_expressions("EUR", "39", dataset="multi_horizon_alpha")
    assert [r["expression"] for r in rows] == ["rank(close)", "rank(volume)"]
    assert rows[0]["status"] == "gem"


def test_upsert_expressions_idempotent(store):
    store.upsert_expressions("EUR", "1", ["rank(a)"], status="pending")
    store.upsert_expressions("EUR", "1", [{"expression": "rank(a)", "status": "selected"}])
    rows = store.list_expressions("EUR", "1")
    assert len(rows) == 1
    assert rows[0]["status"] == "selected"


def test_field_catalog_roundtrip(store):
    cat = {
        "dataset": "model238",
        "region": "EUR",
        "universe": "TOP2500",
        "delay": 1,
        "data_type": "MATRIX",
        "field_count": 2,
        "fields": [
            {"id": "mdl238_a", "type": "MATRIX", "coverage": 0.9, "userCount": 1, "alphaCount": 3},
            {"id": "mdl238_b", "type": "VECTOR", "coverage": 0.8, "userCount": 0, "alphaCount": 0},
        ],
    }
    store.upsert_field_catalog("EUR", cat)
    got = store.get_field_catalog("EUR", "model238")
    assert got["data_type"] == "MATRIX"
    ids = {f["id"] for f in got["fields"]}
    assert ids == {"mdl238_a", "mdl238_b"}


def test_gate_result_roundtrip(store):
    report = {"all_pass": True, "total": 8, "passed": 8}
    store.upsert_gate_result("EUR", "38", "shortinterest6", report)
    got = store.get_gate_result("EUR", "38", "shortinterest6")
    assert got["all_pass"] is True
    assert got["total"] == 8


def test_backtest_rows_and_alphas(store):
    store.upsert_expressions("EUR", "38", ["rank(x)"], dataset="mh")
    n = store.upsert_backtest_rows(
        "EUR", "38",
        [{"id": "abc123", "code": "rank(x)", "sharpe": 1.2, "fitness": 0.8,
          "two_year_sharpe": 1.1, "margin_bp": 12, "turnover_pct": 8}],
        dataset="mh",
    )
    assert n == 1
    rows = store.list_backtest_rows("EUR", "38")
    assert rows[0]["alpha_id"] == "abc123"
    assert abs(rows[0]["margin"] - 0.0012) < 1e-9


def test_checkpoint_and_ranking(store):
    store.upsert_checkpoint("EUR", "38", {"wave": "38", "batches": []})
    ck = store.get_checkpoint("EUR", "38")
    assert ck["wave"] == "38"
    store.upsert_ranking("EUR", {"ranking": [{"id": "ds1", "tier": "tier1"}]})
    rk = store.get_ranking("EUR")
    assert rk["ranking"][0]["id"] == "ds1"


def test_methodology_rules_and_idea(store):
    store.upsert_methodology_rules("EUR", {"version": 1, "rules": [{"rule_id": "a"}]})
    rules = store.get_methodology_rules("EUR")
    assert rules["rules"][0]["rule_id"] == "a"
    store.upsert_idea("EUR", "mh", 1, {"template": "t", "idea": "i", "expression_list": ["rank(a)"]})
    idea = store.get_idea("EUR", "mh", 1)
    assert idea["expression_list"] == ["rank(a)"]


def test_history_expressions_across_waves(store):
    store.upsert_expressions("EUR", "1", ["rank(a)"])
    store.upsert_expressions("EUR", "2", ["rank(b)"])
    hist = set(store.history_expressions("EUR"))
    assert hist == {"rank(a)", "rank(b)"}
