# -*- coding: utf-8 -*-
"""JPN 无 pv1 硬事实（2026-09-19）：区域不可用基础字段 + ts_*(…vec_*(…)) 禁用，GEM 预闸与 gate 闸2b 同源。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "Claude", "skills", "brain-make-some-gem", "scripts", "trailSomeAlphas"))
sys.path.insert(0, os.path.join(ROOT, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts"))

import pipeline_pregate as pg  # noqa: E402
import gate  # noqa: E402

VEC_TS = "rank(ts_delta(ts_backfill(vec_avg(mean_flash_estimate_eps_annual12_3), 22), 66))"
VEC_OK = "rank(vec_avg(mean_flash_estimate_eps_annual12_3))"
PV = "rank(ts_delta(close, 5))"
MATRIX_TS = "rank(ts_zscore(actual_earnings_surprise_pct_lastq_medium, 22))"
PRE_CLOSE_FIELD = "rank(mean_last_trade_price_return_30m_pre_close_2)"


def test_has_ts_over_vec():
    assert pg.has_ts_over_vec(VEC_TS)
    assert pg.has_ts_over_vec("rank(ts_mean(vec_sum(f), 5))")
    assert not pg.has_ts_over_vec(VEC_OK)
    assert not pg.has_ts_over_vec(MATRIX_TS)
    assert not pg.has_ts_over_vec("group_rank(vec_avg(f), market)")


def test_pregate_jpn_drops_pv1_and_vector_ts_but_keeps_others():
    kept, rep = pg.pregate([PV, VEC_OK, VEC_TS, PRE_CLOSE_FIELD, MATRIX_TS], log=lambda *a, **k: None, region="JPN")
    assert VEC_OK in kept and MATRIX_TS in kept
    assert PRE_CLOSE_FIELD in kept, "字段名内含 close 子串不能误杀（词边界）"
    assert PV not in kept and VEC_TS not in kept
    assert rep["invalid_field_dropped"] == 1 and rep["vector_ts_dropped"] == 1
    assert rep["poison_dropped"] == 0


def test_pregate_other_regions_untouched():
    kept, rep = pg.pregate([PV, VEC_TS], log=lambda *a, **k: None, region="IND")
    assert kept == [PV, VEC_TS]
    assert rep["invalid_field_dropped"] == 0 and rep["vector_ts_dropped"] == 0


def test_platform_constraints_declare_jpn_rules():
    p = os.path.join(ROOT, "Claude", "skills", "wq-brain-campaign-toolkit", "config", "platform_constraints.json")
    pc = json.load(open(p, encoding="utf-8"))
    assert "close" in pc["region_invalid_fields"]["JPN"]
    assert "JPN" in pc["region_vector_ts_forbidden"]


def test_gate_ts_over_vec_helper_matches_pregate():
    for e in (VEC_TS, VEC_OK, MATRIX_TS, PV, "rank(ts_mean(vec_sum(f), 5))"):
        assert gate._ts_over_vec(e) == pg.has_ts_over_vec(e)
