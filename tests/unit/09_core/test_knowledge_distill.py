# -*- coding: utf-8 -*-
"""波级 / 区域级经验蒸馏（2026-11-15 P2）。"""
import json

from wqb.store import CampaignStore
from wqb.knowledge.capture import refresh_attempt_knowledge
from wqb.knowledge.distill import distill_region, distill_wave, publish_region_stats


def _seed_dead_skeleton(store, region="KOR", wave="902", n=5):
    fields = ["close", "open", "high", "low", "volume", "vwap"][:n]
    exprs = [f"rank(ts_backfill({f}, 66))" for f in fields]
    store.upsert_expressions(region, wave, [{"expression": e, "status": "selected"} for e in exprs],
                             dataset="demo")
    rows = []
    for i, e in enumerate(exprs):
        rows.append({
            "alpha_id": f"D{i}", "code": e, "status": "COMPLETE",
            "sharpe": 0.4 + i * 0.01, "fitness": 0.3, "turnover": 0.3, "margin": 0.0001,
            "failed_checks": ["CONCENTRATED_WEIGHT"],
            "checks": [{"name": "CONCENTRATED_WEIGHT", "result": "FAIL"}],
        })
    store.upsert_backtest_rows(region, wave, rows, dataset="demo")
    store.upsert_ledger(region, f"wave_meta_{wave}", {"priors_sha": "b" * 64})
    return exprs


def test_distill_wave_marks_dead_skeleton(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead_skeleton(st, n=5)
        refresh_attempt_knowledge(st, "KOR", "902")
        lesson = distill_wave(st, "KOR", "902")
        assert lesson["n_attempts"] == 5
        assert lesson["outcome_mix"]["dead"] == 5
        sk = [g for g in lesson["by_skeleton"] if g["n"] == 5]
        assert sk and sk[0]["dead"] is True
        assert sk[0]["dominant_wall"] == "CW"
        assert sk[0]["dominant_wall_share"] == 1.0
        assert len(lesson["proposals"]["dead_skeletons"]) == 1
        rules = lesson["proposals"]["rules"]
        assert rules and rules[0]["status"] == "proposed"
        assert rules[0]["type"] == "strategy"
    finally:
        st.close()


def test_dead_threshold_needs_min_samples(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead_skeleton(st, n=2)
        refresh_attempt_knowledge(st, "KOR", "902")
        lesson = distill_wave(st, "KOR", "902")
        assert not [g for g in lesson["by_skeleton"] if g["dead"]]
        assert lesson["proposals"]["dead_skeletons"] == []
    finally:
        st.close()


def test_distill_wave_is_deterministic(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead_skeleton(st, n=5)
        refresh_attempt_knowledge(st, "KOR", "902")
        a = distill_wave(st, "KOR", "902")
        b = distill_wave(st, "KOR", "902")
        assert json.dumps(a, sort_keys=True, ensure_ascii=False) == \
               json.dumps(b, sort_keys=True, ensure_ascii=False)
    finally:
        st.close()


def test_publish_writes_kb_lessons_and_proposals(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead_skeleton(st, n=5)
        refresh_attempt_knowledge(st, "KOR", "902")
        lesson = distill_wave(st, "KOR", "902")
        pub = publish_region_stats(st, "KOR", lesson)
        assert pub["ok"] is True
        assert pub["wave_lessons_key"] == "wave_lessons_KOR_902"
        kb = st.get_ledger("KOR", "region_kb") or {}
        assert kb["skeleton_stats"] and kb["skeleton_stats"][0]["dead"] is True
        # family 全是 _unknown → 不发布（只留给 skeleton 维度）
        assert kb["family_stats"] == []
        stored = st.get_ledger("KOR", "wave_lessons_KOR_902")
        assert stored["n_attempts"] == 5
        assert stored["published_at"]
        prop = st.get_ledger("KOR", "experience_proposals_KOR")
        assert len(prop["proposals"]["dead_skeletons"]) == 1
    finally:
        st.close()


def test_distill_region_filters_unknown_family(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed_dead_skeleton(st, n=5)
        refresh_attempt_knowledge(st, "KOR", "902")
        stats = distill_region(st, "KOR")
        assert stats["sample_size"] == 5
        assert stats["family_stats"] == []
        assert len(stats["skeleton_stats"]) == 1
    finally:
        st.close()
