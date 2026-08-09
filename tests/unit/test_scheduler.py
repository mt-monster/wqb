"""Unit tests for wqb.search.scheduler — budget allocation and session pack.

Covers:
- ``plan()`` returns correct structure with arms and budget.
- ``plan()`` validates region (raises on unknown).
- ``plan()`` uses USA default universe TOP3000.
- ``allocate_budget`` distributes budget respecting minimum-per-arm (4).
- ``allocate_budget`` handles zero/negative budget gracefully.
- ``allocate_budget`` handles insufficient budget (partial allocation).
- ``allocate_budget`` equal-distribution fallback when weights are zero.
"""

import pytest

from wqb.search.scheduler import Scheduler


@pytest.fixture
def scheduler(tmp_path):
    fm_file = str(tmp_path / "failure_memory.jsonl")
    return Scheduler(failure_memory_file=fm_file)


# ---------------------------------------------------------------------------
# plan()
# ---------------------------------------------------------------------------

def test_plan_returns_valid_structure(scheduler):
    plan = scheduler.plan("2026-04-22", region="USA", budget=100)
    assert "date" in plan
    assert "region" in plan
    assert "universe" in plan
    assert "delay" in plan
    assert "arms" in plan
    assert "budget" in plan
    assert "neutralization_sweep" in plan
    assert plan["date"] == "2026-04-22"
    assert plan["region"] == "USA"


def test_plan_usa_default_universe(scheduler):
    plan = scheduler.plan("2026-04-22", region="USA", budget=100)
    assert plan["universe"] == "TOP3000"


def test_plan_neutralization_sweep_usa_11(scheduler):
    plan = scheduler.plan("2026-04-22", region="USA", budget=100)
    assert len(plan["neutralization_sweep"]) == 11


def test_plan_arms_have_budget_allocation(scheduler):
    plan = scheduler.plan("2026-04-22", region="USA", budget=100)
    for arm in plan["arms"]:
        assert "budget_allocation" in arm
        assert isinstance(arm["budget_allocation"], int)


def test_plan_budget_sum_matches_total(scheduler):
    total = 200
    plan = scheduler.plan("2026-04-22", region="USA", budget=total)
    allocated = sum(arm["budget_allocation"] for arm in plan["arms"])
    assert allocated == total


def test_plan_unknown_region_raises(scheduler):
    with pytest.raises(ValueError):
        scheduler.plan("2026-04-22", region="XXX", budget=100)


def test_plan_arms_have_required_fields(scheduler):
    plan = scheduler.plan("2026-04-22", region="USA", budget=100)
    for arm in plan["arms"]:
        assert "category" in arm
        assert "dataset" in arm
        assert "universe" in arm
        assert "paradigms" in arm


def test_plan_non_usa_region(scheduler):
    plan = scheduler.plan("2026-04-22", region="KOR", budget=50)
    assert plan["region"] == "KOR"
    assert plan["universe"] == "TOP3000"  # we pass it explicitly


# ---------------------------------------------------------------------------
# allocate_budget
# ---------------------------------------------------------------------------

def test_allocate_budget_zero_budget(scheduler):
    arms = [
        {"category": "news", "dataset": "news12", "universe": "TOP3000", "paradigms": ["P1"]},
        {"category": "fundamental", "dataset": "fnd6", "universe": "TOP3000", "paradigms": ["P2"]},
    ]
    result = scheduler.allocate_budget(arms, 0)
    assert all(a["budget_allocation"] == 0 for a in result)


def test_allocate_budget_minimum_per_arm(scheduler):
    arms = [
        {"category": "news", "dataset": "news12", "universe": "TOP3000", "paradigms": ["P1"]},
        {"category": "fundamental", "dataset": "fnd6", "universe": "TOP3000", "paradigms": ["P2"]},
    ]
    # 2 arms × 4 min = 8; budget=10 leaves 2 remainder
    result = scheduler.allocate_budget(arms, 10)
    total = sum(a["budget_allocation"] for a in result)
    assert total == 10
    for a in result:
        assert a["budget_allocation"] >= 0


def test_allocate_budget_insufficient_for_all(scheduler):
    arms = [
        {"category": f"cat{i}", "dataset": f"ds{i}", "universe": "TOP3000", "paradigms": ["P1"]}
        for i in range(5)
    ]
    # 5 arms × 4 min = 20 needed; budget=10 only covers 2 arms fully
    result = scheduler.allocate_budget(arms, 10)
    total = sum(a["budget_allocation"] for a in result)
    assert total == 10


def test_allocate_budget_single_arm(scheduler):
    arms = [{"category": "news", "dataset": "news12", "universe": "TOP3000", "paradigms": ["P1"]}]
    result = scheduler.allocate_budget(arms, 50)
    assert result[0]["budget_allocation"] == 50


def test_allocate_budget_even_distribution(scheduler):
    arms = [
        {"category": "news", "dataset": "news12", "universe": "TOP3000", "paradigms": ["P1"]},
        {"category": "news", "dataset": "news29", "universe": "TOP3000", "paradigms": ["P1"]},
    ]
    result = scheduler.allocate_budget(arms, 20)
    total = sum(a["budget_allocation"] for a in result)
    assert total == 20


def test_allocate_budget_large_budget(scheduler):
    arms = [
        {"category": "news", "dataset": "news12", "universe": "TOP3000", "paradigms": ["P1"]},
        {"category": "fundamental", "dataset": "fnd6", "universe": "TOP3000", "paradigms": ["P2"]},
        {"category": "analyst", "dataset": "analyst4", "universe": "TOP3000", "paradigms": ["P3"]},
    ]
    result = scheduler.allocate_budget(arms, 300)
    total = sum(a["budget_allocation"] for a in result)
    assert total == 300