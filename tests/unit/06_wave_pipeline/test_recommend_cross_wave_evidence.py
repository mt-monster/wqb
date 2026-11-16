# -*- coding: utf-8 -*-
"""P2：review_wave 推荐附跨波实测证据（2026-11-15）。"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TOOLKIT) not in sys.path:
    sys.path.insert(0, str(TOOLKIT))

from wqb.store import CampaignStore


class _Ctx:
    region = "KOR"
    dir = ""

    def __init__(self, d):
        self.dir = str(d)


def test_cross_wave_stats_are_attached_to_recommendations(tmp_path, monkeypatch):
    import _lib.rules as rules

    db = tmp_path / "wqb.db"
    st = CampaignStore(str(db))
    try:
        st.upsert_ledger("KOR", "region_kb", {
            "skeleton_stats": [{
                "skeleton": "rank ( ts_backfill ( F , N ) )",
                "n": 8, "n_win": 0, "n_near": 0, "max_sharpe": 0.6,
                "dominant_wall": "CW", "dominant_wall_share": 0.9, "dead": True,
            }],
        })
    finally:
        st.close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))

    ctx = _Ctx(tmp_path)
    stats = rules.cross_wave_stats(ctx)
    assert stats and stats[0]["dominant_wall"] == "CW"

    rows = [{"sharpe": 0.5, "fitness": 0.3, "walls": ["CONCENTRATED_WEIGHT"]}
            for _ in range(5)]
    recs = rules.recommend_next_wave(ctx, rows, near=[], wave_meta={"region": "KOR"})
    assert recs, "CW 主导应至少产出一条建议"
    assert any(r.get("cross_wave_evidence") for r in recs)
