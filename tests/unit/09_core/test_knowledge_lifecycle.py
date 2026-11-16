# -*- coding: utf-8 -*-
"""P3：统计规则 proposed → active / contested 生命周期（2026-11-15）。"""
from wqb.store import CampaignStore
from wqb.knowledge.capture import refresh_attempt_knowledge
from wqb.knowledge.distill import distill_wave, publish_region_stats


def _seed_dead(store, wave, n=5, sharpe=0.4):
    fields = ["close", "open", "high", "low", "volume", "vwap"][:n]
    exprs = [f"rank(ts_backfill({f}, 66))" for f in fields]
    store.upsert_expressions("KOR", wave, [{"expression": e, "status": "selected"} for e in exprs],
                             dataset="demo")
    rows = [{
        "alpha_id": f"{wave}-{i}", "code": e, "status": "COMPLETE",
        "sharpe": sharpe + i * 0.01, "fitness": 0.3, "turnover": 0.3, "margin": 0.0001,
        "failed_checks": ["CONCENTRATED_WEIGHT"],
        "checks": [{"name": "CONCENTRATED_WEIGHT", "result": "FAIL"}],
    } for i, e in enumerate(exprs)]
    store.upsert_backtest_rows("KOR", wave, rows, dataset="demo")
    store.upsert_ledger("KOR", f"wave_meta_{wave}", {"priors_sha": "b" * 64})


def _seed_win(store, wave):
    expr = "rank(ts_backfill(close, 66))"
    store.upsert_expressions("KOR", wave, [{"expression": expr, "status": "selected"}],
                             dataset="demo")
    store.upsert_backtest_rows("KOR", wave, [{
        "alpha_id": f"{wave}-win", "code": expr, "status": "COMPLETE",
        "sharpe": 1.9, "fitness": 1.2, "turnover": 0.1, "margin": 0.001,
        "two_year_sharpe": 1.7, "ra_failed_checks": [], "checks": [],
    }], dataset="demo")


def _run(store, wave):
    refresh_attempt_knowledge(store, "KOR", wave)
    lesson = distill_wave(store, "KOR", wave)
    pub = publish_region_stats(store, "KOR", lesson)
    return lesson, pub


def _stat_rule(store):
    data = store.get_methodology_rules("KOR") or {}
    return next((r for r in (data.get("rules") or [])
                 if str(r.get("rule_id", "")).startswith("stat_dead_")), None)


def test_proposed_does_not_enter_methodology_rules_until_confirmed(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead(st, "1")
        _lesson, pub = _run(st, "1")
        # proposals 里应有 1 条 proposed、confirmations=1
        prop = st.get_ledger("KOR", "experience_proposals_KOR")
        rules = prop["proposals"]["rules"]
        assert rules and rules[0]["status"] == "proposed"
        assert rules[0]["confirmations"] == 1
        assert "stat_dead_" in rules[0]["rule_id"]
        # methodology_rules 仍为空（proposed 不写入）
        assert _stat_rule(st) is None
    finally:
        st.close()


def test_second_independent_wave_promotes_to_active(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead(st, "1")
        _run(st, "1")
        _seed_dead(st, "2")
        _lesson, pub = _run(st, "2")
        assert pub["promotions"]["promoted"], pub["promotions"]
        rule = _stat_rule(st)
        assert rule is not None
        assert rule["status"] == "active"
        assert rule["confirmations"] == 2
        assert rule["times_applied"] == 2 and rule["times_succeeded"] == 2
        assert rule["type"] == "strategy"          # 只晋升咨询型，不生成硬拦截
    finally:
        st.close()


def test_win_on_same_skeleton_contests_promoted_rule(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead(st, "1")
        _run(st, "1")
        _seed_dead(st, "2")
        _run(st, "2")
        assert _stat_rule(st)["status"] == "active"
        _seed_win(st, "3")
        _lesson, pub = _run(st, "3")
        assert pub["promotions"]["contested"], pub["promotions"]
        rule = _stat_rule(st)
        assert rule["status"] == "contested"
        assert rule["contradictions"] >= 1
        assert rule["confidence"] < 1.0
    finally:
        st.close()
