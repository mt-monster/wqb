# -*- coding: utf-8 -*-
"""P4：template_kb measured 层写入 + assemble_priors 读取（2026-11-15）。"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TOOLKIT) not in sys.path:
    sys.path.insert(0, str(TOOLKIT))

from wqb.store import CampaignStore
from wqb.knowledge.capture import refresh_attempt_knowledge
from wqb.knowledge.distill import distill_wave, publish_region_stats


class _Ctx:
    region = "KOR"
    prefix = "kor"

    def __init__(self, d):
        self.dir = str(d)

    def thresh(self, name):
        return {}

    def path(self, *parts):
        return os.path.join(self.dir, *parts)


def _seed(store):
    exprs = [
        "rank(ts_backfill(close, 66))",
        "rank(ts_backfill(open, 66))",
        "rank(ts_backfill(high, 66))",
        "rank(ts_backfill(low, 66))",
        "rank(ts_backfill(volume, 66))",
    ]
    store.upsert_expressions("KOR", "10", [{"expression": e, "status": "selected"} for e in exprs],
                             dataset="demo")
    rows = [{
        "alpha_id": f"D{i}", "code": e, "status": "COMPLETE",
        "sharpe": 0.4 + i * 0.01, "fitness": 0.3, "turnover": 0.3, "margin": 0.0001,
        "failed_checks": ["CONCENTRATED_WEIGHT"],
        "checks": [{"name": "CONCENTRATED_WEIGHT", "result": "FAIL"}],
    } for i, e in enumerate(exprs)]
    # 一条赢家（不同骨架），用来产生 measured_validated
    rows.append({
        "alpha_id": "W", "code": "ts_corr(rank(close), rank(volume), 20)",
        "status": "COMPLETE", "sharpe": 1.9, "fitness": 1.2, "turnover": 0.1,
        "margin": 0.001, "two_year_sharpe": 1.7, "ra_failed_checks": [], "checks": [],
    })
    store.upsert_expressions("KOR", "10",
                             [{"expression": rows[-1]["code"], "status": "selected"}],
                             dataset="demo")
    store.upsert_backtest_rows("KOR", "10", rows, dataset="demo")


def test_publish_templates_writes_measured_and_preserves_manual(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        st.upsert_ledger("KB", "template_kb", {
            "templates": [{"id": "manual", "name": "人工模板", "validated": {"KOR": "ok"}}],
        })
        _seed(st)
        refresh_attempt_knowledge(st, "KOR", "10")
        lesson = distill_wave(st, "KOR", "10")
        pub = publish_region_stats(st, "KOR", lesson)
        assert pub["templates"]["failed"] >= 1
        assert pub["templates"]["validated"] >= 1
        kb = st.get_ledger("KB", "template_kb")
        assert kb["templates"] and kb["templates"][0]["id"] == "manual"   # 人工层保留
        assert kb["measured_failed"] and kb["measured_failed"][0]["region"] == "KOR"
        assert kb["measured_validated"] and kb["measured_validated"][0]["region"] == "KOR"
        assert kb["measured_source"].endswith("publish_templates")
    finally:
        st.close()


def test_assemble_priors_reads_measured_templates(tmp_path, monkeypatch):
    import assemble_priors

    db = tmp_path / "wqb.db"
    st = CampaignStore(str(db))
    try:
        st.upsert_ledger("KB", "template_kb", {
            "templates": [],
            "measured_validated": [{
                "kind": "skeleton", "name": "rank ( ts_backfill ( F , N ) )", "region": "KOR",
                "n": 8, "n_win": 1, "max_sharpe": 1.9, "wave": "10",
                "evidence_attempt_ids": ["W"],
            }],
            "measured_failed": [{
                "kind": "skeleton", "name": "ts_corr ( rank ( F ) , rank ( F ) , N )",
                "region": "KOR", "n": 8, "max_sharpe": 0.6, "dominant_wall": "CW",
                "dominant_wall_share": 0.9, "wave": "10",
            }],
        })
        st.upsert_ledger("KOR", "region_kb", {
            "win_recipes": [{"name": "w1"}], "dead_patterns": ["x"],
        })
    finally:
        st.close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    payload = assemble_priors.assemble_priors_dict(_Ctx(tmp_path))
    assert any(w.get("source") == "template_kb_measured" for w in payload["wins"])
    assert any(d.get("source") == "template_kb_measured_failed" for d in payload["dead_ends"])
