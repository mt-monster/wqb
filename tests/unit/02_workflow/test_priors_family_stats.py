# -*- coding: utf-8 -*-
"""P2 复用面：assemble_priors 注入 family/skeleton 实测统计 + GEM 渲染（2026-11-15）。"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
GEM = REPO_ROOT / "Claude" / "skills" / "brain-make-some-gem" / "scripts" / "trailSomeAlphas"
for p in (TOOLKIT, GEM):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from wqb.store import CampaignStore


class _Ctx:
    region = "KOR"
    prefix = "kor"

    def __init__(self, d):
        self.dir = str(d)

    def thresh(self, name):
        return {}

    def path(self, *parts):
        return os.path.join(self.dir, *parts)


def _seed(db):
    st = CampaignStore(str(db))
    try:
        st.upsert_ledger("KOR", "region_kb", {
            "tier": "demo",
            "win_recipes": [{"name": "w1", "skeleton": "rank(ts_backfill(F,N))"}],
            "dead_patterns": ["demo dead pattern"],
            "family_stats": [{
                "family": "f1", "n": 10, "n_win": 2, "n_near": 3, "max_sharpe": 2.0,
                "dominant_wall": "SHARPE", "dominant_wall_share": 0.5, "dead": False,
            }],
            "skeleton_stats": [{
                "skeleton": "rank ( ts_backfill ( F , N ) )", "n": 8, "n_win": 1, "n_near": 1,
                "max_sharpe": 0.7, "dominant_wall": "CW", "dominant_wall_share": 0.9,
                "dead": True,
            }],
        })
    finally:
        st.close()


def test_priors_include_measured_stats(tmp_path, monkeypatch):
    import assemble_priors

    db = tmp_path / "wqb.db"
    _seed(db)
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    payload = assemble_priors.assemble_priors_dict(_Ctx(tmp_path))
    assert payload["family_stats"][0]["family"] == "f1"
    assert payload["skeleton_stats"][0]["dead"] is True
    assert any("family_stats" in s for s in payload["_meta"]["sources"])
    matrix = payload["skeleton_field_matrix"]
    assert any(e.get("source") == "measured" for e in matrix["effective"])
    assert any(d.get("source") == "measured" and d.get("advisory") for d in matrix["dead"])


def test_compact_priors_text_renders_measured_section(tmp_path, monkeypatch):
    import assemble_priors
    import economic_priors

    db = tmp_path / "wqb.db"
    _seed(db)
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    payload = assemble_priors.assemble_priors_dict(_Ctx(tmp_path))
    text = economic_priors.compact_priors_text(payload, None)
    assert "Measured family/skeleton outcomes" in text
    assert "[DEAD]" in text and "[OK]" in text


def test_empty_stats_do_not_add_prompt_section(tmp_path, monkeypatch):
    import assemble_priors
    import economic_priors

    db = tmp_path / "wqb.db"
    st = CampaignStore(str(db))
    try:
        st.upsert_ledger("KOR", "region_kb", {
            "win_recipes": [{"name": "w1"}], "dead_patterns": ["x"],
        })
    finally:
        st.close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    payload = assemble_priors.assemble_priors_dict(_Ctx(tmp_path))
    assert "family_stats" not in payload
    assert "Measured family/skeleton outcomes" not in economic_priors.compact_priors_text(payload, None)
