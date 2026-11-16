# -*- coding: utf-8 -*-
"""P4：知识版本产出率（2026-11-15）。"""
import json

from wqb.store import CampaignStore
from wqb.knowledge.yield_report import compute_yield, render_yield_markdown, write_yield_report


def _seed(store):
    rows = [
        {"attempt_id": "v1a", "region": "KOR", "wave": "1", "knowledge_version": "v1",
         "outcome": "win", "metrics_json": {"sharpe": 2.0, "prod_correlation": 0.5,
                                            "self_correlation": 0.2},
         "created_at": "2026-11-01T00:00:00"},
        {"attempt_id": "v1b", "region": "KOR", "wave": "1", "knowledge_version": "v1",
         "outcome": "near", "metrics_json": {"sharpe": 1.3, "prod_correlation": 0.9,
                                             "self_correlation": 0.8},
         "created_at": "2026-11-01T01:00:00"},
        {"attempt_id": "v2a", "region": "KOR", "wave": "2", "knowledge_version": "v2",
         "outcome": "dead", "metrics_json": {"sharpe": 0.4},
         "created_at": "2026-11-02T00:00:00"},
    ]
    store.upsert_attempt_knowledge(rows)


def test_compute_yield_groups_by_version(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed(st)
        r = compute_yield(st, "KOR")
        assert r["sample_size"] == 3
        by = {v["knowledge_version"]: v for v in r["versions"]}
        assert by["v1"]["n"] == 2 and by["v1"]["n_win"] == 1 and by["v1"]["n_near"] == 1
        assert by["v1"]["win_rate"] == 0.5 and by["v1"]["near_rate"] == 0.5
        assert by["v1"]["prod"] == {"n_known": 2, "clean_rate": 0.5}
        assert by["v1"]["self"] == {"n_known": 2, "clean_rate": 0.5}
        assert by["v2"]["prod"]["n_known"] == 0 and by["v2"]["prod"]["clean_rate"] is None
        assert r["latest"]["knowledge_version"] == "v2"
        assert r["delta"]["win_rate"] == -0.5
    finally:
        st.close()


def test_render_and_write_report(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed(st)
        r = compute_yield(st, "KOR")
        text = render_yield_markdown(r)
        assert "KOR 经验知识版本产出率" in text and "knowledge_version" in text
        assert "最新版 vs 上一版" in text
        out = write_yield_report(st, "KOR", str(tmp_path / "output_report"))
        assert "experience_yield_kor_" in out["path"] and out["path"].endswith(".md")
        assert (tmp_path / "output_report").is_dir()
        snap = st.get_ledger("KOR", "experience_yield_KOR")
        assert snap["sample_size"] == 3 and snap["report_path"] == out["path"]
        assert json.loads(json.dumps(snap, ensure_ascii=False))
    finally:
        st.close()
