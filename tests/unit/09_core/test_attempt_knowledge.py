# -*- coding: utf-8 -*-
"""attempt_knowledge 逐条经验索引（2026-11-15 P1）。

守住四件事：
1. 分类字段正确（主墙 / 失败类别 / outcome / 知识版本）；
2. 派生层可幂等重建（连跑两次，除 updated_at 外逐字节一致）；
3. 合并式写入（第二次不带 metrics 不把已有值清空）；
4. 不回写事实表（backtest_results 的指标保持不变）。
"""
import json

from wqb.store import CampaignStore
from wqb.knowledge.capture import build_attempt_records, refresh_attempt_knowledge


def _store(tmp_path):
    return CampaignStore(str(tmp_path / "wqb.db"))


def _seed(store, region="KOR", wave="901", ds="demo"):
    exprs = [
        "rank(ts_backfill(close, 66))",
        "rank(ts_backfill(open, 66))",
        "ts_corr(rank(close), rank(volume), 20)",
    ]
    store.upsert_expressions(region, wave, [{"expression": e, "status": "selected"} for e in exprs],
                             dataset=ds)
    rows = [
        {"alpha_id": "W1", "code": exprs[0], "status": "COMPLETE", "sharpe": 1.9, "fitness": 1.2,
         "turnover": 0.10, "margin": 0.001, "two_year_sharpe": 1.7, "sub_universe_sharpe": 1.1,
         "ra_failed_checks": [], "checks": []},
        {"alpha_id": "N1", "code": exprs[1], "status": "COMPLETE", "sharpe": 1.20, "fitness": 0.80,
         "turnover": 0.10, "margin": 0.001, "two_year_sharpe": 0.90, "sub_universe_sharpe": 0.60,
         "ra_failed_checks": ["LOW_2Y_SHARPE"],
         "checks": [{"name": "LOW_2Y_SHARPE", "result": "FAIL", "limit": 1.58, "value": 0.9}],
         "failed_checks": ["LOW_2Y_SHARPE"]},
        {"alpha_id": "D1", "code": exprs[2], "status": "COMPLETE", "sharpe": 0.40, "fitness": 0.30,
         "turnover": 0.30, "margin": 0.0001,
         "failed_checks": ["CONCENTRATED_WEIGHT"],
         "checks": [{"name": "CONCENTRATED_WEIGHT", "result": "FAIL"}]},
    ]
    store.upsert_backtest_rows(region, wave, rows, dataset=ds)
    store.upsert_ledger(region, f"wave_meta_{wave}", {"priors_sha": "a" * 64})
    return exprs


def _canon(rows):
    out = []
    for r in rows:
        d = dict(r)
        d.pop("updated_at", None)
        d.pop("created_at", None)
        out.append(json.dumps(d, sort_keys=True, ensure_ascii=False))
    return sorted(out)


def test_capture_classifies_wall_outcome_and_version(tmp_path):
    st = _store(tmp_path)
    try:
        _seed(st)
        summary = refresh_attempt_knowledge(
            st, "KOR", "901", settings={"universe": "TOP600", "delay": 1})
        assert summary["records"] == 3 and summary["written"] == 3
        assert summary["knowledge_version"].startswith("aaaaaaaa-")
        rows = {r["attempt_id"]: r for r in st.list_attempt_knowledge(region="KOR", wave="901")}
        assert rows["W1"]["outcome"] == "win"
        assert rows["W1"]["failure_class"] == "pass"
        assert rows["N1"]["primary_wall"] == "2Y"
        assert rows["N1"]["failure_class"] == "2y"
        assert rows["N1"]["outcome"] == "near"
        assert rows["D1"]["primary_wall"] == "CW"
        assert rows["D1"]["failure_class"] == "cw"
        assert rows["D1"]["outcome"] == "dead"
        # skeleton 由表达式结构签名补出（expressions.skeleton 为空）
        assert "ts_backfill" in rows["W1"]["skeleton"]
        assert rows["W1"]["settings_json"]["universe"] == "TOP600"
        assert rows["W1"]["ra_failed_json"] == []       # 已知 RA 全过
        assert rows["N1"]["ra_failed_json"] == ["LOW_2Y_SHARPE"]
    finally:
        st.close()


def test_capture_is_idempotent(tmp_path):
    st = _store(tmp_path)
    try:
        _seed(st)
        refresh_attempt_knowledge(st, "KOR", "901")
        first = _canon(st.list_attempt_knowledge(region="KOR", wave="901"))
        refresh_attempt_knowledge(st, "KOR", "901")
        second = _canon(st.list_attempt_knowledge(region="KOR", wave="901"))
        assert first == second
    finally:
        st.close()


def test_partial_update_does_not_clear_metrics(tmp_path):
    st = _store(tmp_path)
    try:
        _seed(st)
        refresh_attempt_knowledge(st, "KOR", "901")
        before = st.get_attempt_knowledge("W1")
        st.upsert_attempt_knowledge([{"attempt_id": "W1", "next_action": "manual_note"}])
        after = st.get_attempt_knowledge("W1")
        assert after["next_action"] == "manual_note"
        assert after["metrics_json"] == before["metrics_json"]
    finally:
        st.close()


def test_capture_does_not_touch_facts(tmp_path):
    st = _store(tmp_path)
    try:
        _seed(st)
        before = st.connection.execute(
            "SELECT alpha_id, sharpe, fitness FROM backtest_results ORDER BY alpha_id"
        ).fetchall()
        refresh_attempt_knowledge(st, "KOR", "901")
        after = st.connection.execute(
            "SELECT alpha_id, sharpe, fitness FROM backtest_results ORDER BY alpha_id"
        ).fetchall()
        assert [tuple(r) for r in before] == [tuple(r) for r in after]
    finally:
        st.close()


def test_build_records_dry_run_has_no_side_effect(tmp_path):
    st = _store(tmp_path)
    try:
        _seed(st)
        recs = build_attempt_records(st, "KOR", "901")
        assert len(recs) == 3
        assert st.list_attempt_knowledge(region="KOR", wave="901") == []
    finally:
        st.close()


def test_unknown_ra_status_is_not_treated_as_win(tmp_path):
    """RA 列 NULL = 未知，不得当“全过”；强指标但没有 RA 信息 → near，不是 win。"""
    st = _store(tmp_path)
    try:
        st.upsert_expressions("KOR", "903", [{"expression": "rank(close)", "status": "selected"}],
                              dataset="demo")
        st.upsert_backtest_rows("KOR", "903", [{
            "alpha_id": "U1", "code": "rank(close)", "status": "COMPLETE",
            "sharpe": 1.9, "fitness": 1.2, "turnover": 0.1, "margin": 0.001,
        }], dataset="demo")
        refresh_attempt_knowledge(st, "KOR", "903")
        row = st.get_attempt_knowledge("U1")
        assert row["ra_failed_json"] is None
        assert row["outcome"] == "near"
    finally:
        st.close()
