# -*- coding: utf-8 -*-
"""attempt_knowledge 存储层（KnowledgeMixin）守护（2026-11-15 P1）。"""
import json


def test_table_and_indexes_created(tmp_path):
    from wqb.store import CampaignStore

    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        cols = {r[1] for r in st.connection.execute("PRAGMA table_info(attempt_knowledge)")}
        for required in ("attempt_id", "region", "wave", "skeleton", "primary_wall",
                         "failure_class", "outcome", "knowledge_version"):
            assert required in cols
        idx = {r[1] for r in st.connection.execute("PRAGMA index_list(attempt_knowledge)")}
        assert {"idx_attempt_region_wave", "idx_attempt_region_ds", "idx_attempt_skeleton"} <= idx
    finally:
        st.close()


def test_upsert_merges_and_filters(tmp_path):
    from wqb.store import CampaignStore

    st = CampaignStore(str(tmp_path / "wqb.db"))
    try:
        n = st.upsert_attempt_knowledge([
            {"attempt_id": "A1", "region": "KOR", "wave": "1", "dataset": "ds",
             "metrics_json": {"sharpe": 1.2}, "outcome": "near", "family": "f1"},
            {"attempt_id": "A2", "region": "KOR", "wave": "1", "dataset": "ds",
             "metrics_json": {"sharpe": 0.4}, "outcome": "dead", "family": "f1"},
            {"attempt_id": None, "region": "KOR", "wave": "1"},  # 无 id 跳过
        ])
        assert n == 2
        got = st.list_attempt_knowledge(region="KOR", wave="1", family="f1")
        assert len(got) == 2
        assert {r["attempt_id"] for r in got} == {"A1", "A2"}
        # 合并：只改 outcome，不传 metrics
        st.upsert_attempt_knowledge([{"attempt_id": "A1", "outcome": "win"}])
        r = st.get_attempt_knowledge("A1")
        assert r["outcome"] == "win"
        assert r["metrics_json"] == {"sharpe": 1.2}
        assert json.loads(json.dumps(r["metrics_json"])) == {"sharpe": 1.2}
    finally:
        st.close()
