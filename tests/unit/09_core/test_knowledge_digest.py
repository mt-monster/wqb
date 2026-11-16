# -*- coding: utf-8 -*-
"""P4：区域经验摘要（2026-11-15）。"""
from wqb.store import CampaignStore
from wqb.knowledge.digest import BEGIN, END, render_digest, write_digest, write_region_digest


def _seed(store):
    store.upsert_attempt_knowledge([
        {"attempt_id": "a1", "region": "KOR", "wave": "1", "knowledge_version": "v1",
         "outcome": "win", "skeleton": "sk-win", "metrics_json": {"sharpe": 1.9},
         "created_at": "2026-11-01T00:00:00"},
        {"attempt_id": "a2", "region": "KOR", "wave": "1", "knowledge_version": "v1",
         "outcome": "dead", "skeleton": "sk-dead", "primary_wall": "CW",
         "walls_json": ["CONCENTRATED_WEIGHT"], "metrics_json": {"sharpe": 0.5},
         "created_at": "2026-11-01T01:00:00"},
        {"attempt_id": "a3", "region": "KOR", "wave": "1", "knowledge_version": "v1",
         "outcome": "dead", "skeleton": "sk-dead", "primary_wall": "CW",
         "walls_json": ["CONCENTRATED_WEIGHT"], "metrics_json": {"sharpe": 0.4},
         "created_at": "2026-11-01T02:00:00"},
        {"attempt_id": "a4", "region": "KOR", "wave": "1", "knowledge_version": "v1",
         "outcome": "dead", "skeleton": "sk-dead", "primary_wall": "CW",
         "walls_json": ["CONCENTRATED_WEIGHT"], "metrics_json": {"sharpe": 0.3},
         "created_at": "2026-11-01T03:00:00"},
    ])
    store.upsert_ledger("KOR", "experience_proposals_KOR", {
        "proposals": {"dead_families": [], "dead_skeletons": [{"skeleton": "sk-dead"}],
                      "wins": [], "rules": []},
    })


def test_render_digest_contains_sections(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed(st)
        text = render_digest(st, "KOR")
        assert text.strip().startswith(BEGIN) and END in text
        assert "KOR 经验摘要" in text
        assert "有效骨架" in text and "sk-win" in text
        assert "统计死路" in text and "sk-dead" in text
        assert "待确认提案" in text
    finally:
        st.close()


def test_write_digest_preserves_text_outside_markers(tmp_path):
    path = tmp_path / "digest.md"
    path.write_text("人工笔记\n" + BEGIN + "\nold\n" + END + "\n尾部\n", encoding="utf-8")
    write_digest(str(path), BEGIN + "\nnew\n" + END + "\n")
    text = path.read_text(encoding="utf-8")
    assert text.startswith("人工笔记\n") and text.endswith("尾部\n")
    assert "new" in text and "old" not in text


def test_write_region_digest_creates_file(tmp_path):
    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        _seed(st)
        out = write_region_digest(st, "KOR", str(tmp_path / "priors" / "experience_digest.md"))
        assert (tmp_path / "priors" / "experience_digest.md").is_file()
        assert out["region"] == "KOR"
    finally:
        st.close()
