# -*- coding: utf-8 -*-
"""2026-09-19 prod-first 探针的纯函数部分（族归并 / 排序 / 判定）。网络部分不在此测。"""
import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load():
    spec = importlib.util.spec_from_file_location("campaign_intel", os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules["campaign_intel"] = m
    spec.loader.exec_module(m)
    return m


def test_family_is_field_set_not_operators():
    ci = _load()
    assert ci._pf_family("rank(ts_mean(snt21_pos_mean, 22))") == "snt21_pos_mean"
    same = ci._pf_family("divide(ts_backfill(snt21_pos_mean, 5), ts_backfill(snt21_pos_max, 5))")
    assert same == "snt21_pos_max+snt21_pos_mean"
    assert ci._pf_family("group_rank(x1234, subindustry)") == "x1234"


def test_pick_probes_ra_clean_first_and_one_per_family():
    ci = _load()
    rows = [
        {"alpha_id": "a", "sharpe": 1.9, "fitness": 1.2, "ra_failed_checks": "[]", "code": "rank(f_one)"},
        {"alpha_id": "b", "sharpe": 2.5, "fitness": 0.6, "ra_failed_checks": '["LOW_FITNESS"]', "code": "rank(f_two)"},
        {"alpha_id": "c", "sharpe": 2.4, "fitness": 0.5, "ra_failed_checks": '["LOW_FITNESS"]', "code": "ts_mean(f_two, 22)"},  # 同族 b
        {"alpha_id": "d", "sharpe": 0.8, "fitness": 0.3, "ra_failed_checks": None, "code": "rank(f_three)"},          # 低于 min_sharpe
        {"alpha_id": "e", "sharpe": -1.7, "fitness": -0.9, "ra_failed_checks": '["LOW_SHARPE"]', "code": "rank(f_four)"},
    ]
    probes = ci._pf_pick_probes(rows, top_k=3, min_sharpe=1.0, sharpe_min=1.58, fitness_min=1.0)
    ids = [p["alpha_id"] for p in probes]
    assert ids[0] == "a"                       # RA-clean 优先
    assert "c" not in ids and "b" in ids       # 同族只留最强
    assert "d" not in ids                      # 低于 min_sharpe
    assert ids == ["a", "b", "e"]              # 反向强信号也探（|S|）
    assert ci._pf_pick_probes(rows, top_k=1, min_sharpe=1.0, sharpe_min=1.58, fitness_min=1.0)[0]["alpha_id"] == "a"


def test_verdict_thresholds():
    ci = _load()
    assert ci._pf_verdict(0.55, "ok", 0.7) == "EXPAND"
    assert ci._pf_verdict(0.7, "ok", 0.7).startswith("STOP")
    assert ci._pf_verdict(None, "pending", 0.7) == "UNKNOWN(pending)"
