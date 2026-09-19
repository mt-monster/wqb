# -*- coding: utf-8 -*-
"""S0 白名单机制 P0–P6 评分逻辑回归（2026-09-14 review 落地）。

守护 score_datasets.py 的新增纯逻辑（无网络/无 auth）：
- P0 empirical_prior：经验强度先验项（默认 weight=0 关闭 → 与旧版逐条一致）
- P2 apply_saturation_demotion + apply_floor_tiers 守卫：prod 饱和集降级且不被保底带复活
- P3 _check_universe_consistency：台账 universe 与 settings 漂移告警
- P5 category_weight flatten：饱和区 model 权重封顶 1.0
- P6 _expr_fields：token 去重 + 剔除群组变量关键字（根治 calibrate 甜区污染）

campaign_intel.py 的 P1（est_seats/--target）依赖 DB + 平台，属集成路径，此处不覆盖；
其 argparse 契约由 tests/unit/test_audit_fixes.py::validate_argv 与 --help 保障。
"""
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"

if str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS))

sd = pytest.importorskip("score_datasets", reason="score_datasets.py 不在 toolkit scripts 目录")


# ---------------------------------------------------------------------------
# P0 empirical_prior + score 集成
# ---------------------------------------------------------------------------

def test_p0_weight_zero_disables_prior():
    """默认 empirical_weight=0.0 → 先验恒 0（各区域行为与旧版一致）。"""
    assert sd.empirical_prior("ds1", {"ds1": {"ceiling_ratio": 0.9}}, {"empirical_weight": 0.0}) == 0.0


def test_p0_ceiling_ratio_scaled_by_weight():
    h = {"empirical_weight": 0.4, "empirical_prior_neutral": 0.45}
    assert sd.empirical_prior("ds1", {"ds1": {"ceiling_ratio": 0.8}}, h) == pytest.approx(0.32)


def test_p0_ratio_clamped_to_unit_interval():
    h = {"empirical_weight": 0.4, "empirical_prior_neutral": 0.45}
    assert sd.empirical_prior("hi", {"hi": {"ceiling_ratio": 2.0}}, h) == pytest.approx(0.4)
    assert sd.empirical_prior("lo", {"lo": {"ceiling_ratio": -1.0}}, h) == pytest.approx(0.0)


def test_p0_missing_record_uses_neutral():
    h = {"empirical_weight": 0.4, "empirical_prior_neutral": 0.45}
    assert sd.empirical_prior("dsX", {}, h) == pytest.approx(0.4 * 0.45)


def test_p0_best_sharpe_fallback_over_gate():
    h = {"empirical_weight": 0.4, "empirical_prior_neutral": 0.45, "_gate_sharpe": 1.58}
    # best_sharpe == gate_sharpe → ceiling_ratio 1.0 → 0.4
    assert sd.empirical_prior("ds2", {"ds2": {"best_sharpe": 1.58}}, h) == pytest.approx(0.4)


def test_p0_score_integration_delta_equals_prior():
    """category_weight 关闭时，开启先验的 score 增量恰为 empirical_prior。"""
    ds = {"id": "ds1", "coverage": 0.8, "alphaCount": 10, "valueScore": 5, "category": "model"}
    off = {"empirical_weight": 0.0, "category_weight_enable": False}
    on = {"empirical_weight": 0.4, "empirical_prior_neutral": 0.45, "category_weight_enable": False}
    s_off = sd.score(ds, 100, dict(off), {})
    s_on = sd.score(ds, 100, dict(on), {"ds1": {"ceiling_ratio": 0.8}})
    assert (s_on - s_off) == pytest.approx(0.32)
    # weight=0 时即便传 emp 也忽略
    assert sd.score(ds, 100, dict(off), {"ds1": {"ceiling_ratio": 0.8}}) == pytest.approx(s_off)


# ---------------------------------------------------------------------------
# P5 category_weight flatten
# ---------------------------------------------------------------------------

_HW = {"category_weight_enable": True, "category_weights": {"model": 1.3, "pv": 1.3},
       "category_weight_floor": 0.9, "category_weight_cap": 1.15}


def test_p5_model_capped_when_region_saturated():
    assert sd.category_weight({"category": "model"}, dict(_HW)) == pytest.approx(1.15)
    sat = dict(_HW, _region_saturated=True, flatten_model_when_saturated=True)
    assert sd.category_weight({"category": "model"}, sat) == pytest.approx(1.0)


def test_p5_flatten_only_affects_model():
    sat = dict(_HW, _region_saturated=True, flatten_model_when_saturated=True)
    assert sd.category_weight({"category": "pv"}, sat) == pytest.approx(1.15)


def test_p5_flatten_disabled_keeps_cap():
    sat = dict(_HW, _region_saturated=True, flatten_model_when_saturated=False)
    assert sd.category_weight({"category": "model"}, sat) == pytest.approx(1.15)


def test_p5_category_weight_disabled_returns_neutral():
    assert sd.category_weight({"category": "model"}, {}) == 1.0


# ---------------------------------------------------------------------------
# P2 apply_saturation_demotion + 保底带守卫
# ---------------------------------------------------------------------------

def test_p2_demotion_marks_and_excludes():
    rows = [{"id": "cont", "tier": "tier1", "score": 0.9},
            {"id": "other", "tier": "tier1", "score": 0.8}]
    n = sd.apply_saturation_demotion(rows, {"cont": {"reason": "prod_saturation"}},
                                     {"saturation_demotion_enable": True})
    assert n == 1
    assert rows[0]["tier"] == "excluded"
    assert rows[0]["tier_note"] == "saturated:prod_saturation"
    assert rows[0]["saturated"] is True
    assert rows[1]["tier"] == "tier1"  # 未命中不受影响


def test_p2_noop_when_empty_or_disabled():
    r1 = [{"id": "x", "tier": "tier1"}]
    assert sd.apply_saturation_demotion(r1, {}, {"saturation_demotion_enable": True}) == 0
    assert r1[0]["tier"] == "tier1"
    r2 = [{"id": "cont", "tier": "tier1"}]
    assert sd.apply_saturation_demotion(r2, {"cont": True}, {"saturation_demotion_enable": False}) == 0
    assert r2[0]["tier"] == "tier1"


def test_p2_floor_tier_guard_skips_saturated(monkeypatch):
    """饱和降级项不得被保底带复活；非饱和 excluded 项照常复活。"""
    monkeypatch.setattr(sd, "backfill_band", lambda r, h: True)
    saturated_row = {"id": "cont", "tier": "excluded", "saturated": True, "hard_excluded": False}
    virgin_row = {"id": "virgin", "tier": "excluded", "hard_excluded": False}
    sd.apply_floor_tiers([saturated_row, virgin_row], {})
    assert saturated_row["tier"] == "excluded"
    assert virgin_row["tier"] == "tier2"


# ---------------------------------------------------------------------------
# P3 _check_universe_consistency
# ---------------------------------------------------------------------------

class _Ctx:
    def __init__(self, universe):
        self.settings = {"universe": universe}


def test_p3_consistent_and_empty_are_ok():
    assert sd._check_universe_consistency(_Ctx("TOPCS1600"), {}) is True
    assert sd._check_universe_consistency(_Ctx(""), {"s0_ranking": {"universe": "TOP2500"}}) is True
    ok = {"s0_ranking": {"universe": "TOPCS1600"},
          "s0_whitelist": {"settings": {"universe": "TOPCS1600"}}}
    assert sd._check_universe_consistency(_Ctx("TOPCS1600"), ok) is True


def test_p3_detects_ranking_and_whitelist_drift(capsys):
    drift = {"s0_ranking": {"universe": "TOP2500"},
             "s0_whitelist": {"settings": {"universe": "TOPCS1600"}}}
    assert sd._check_universe_consistency(_Ctx("TOPCS1600"), drift) is False
    wl_drift = {"s0_whitelist": {"settings": {"universe": "TOP2500"}}}
    assert sd._check_universe_consistency(_Ctx("TOPCS1600"), wl_drift) is False
    assert "universe 不一致" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# P6 _expr_fields：去重 + 剔除群组变量
# ---------------------------------------------------------------------------

def test_p6_dedups_repeated_field():
    assert sd._expr_fields("subtract(close, close)") == ["close"]


def test_p6_strips_group_variables_keeps_real_fields():
    got = sd._expr_fields("group_neutralize(subtract(rank(a_field), rank(b_field)), subindustry)")
    assert "subindustry" not in got
    assert set(got) == {"a_field", "b_field"}


def test_p6_sweet_spot_pollution_root_cause_fixed():
    """复现 EUR pv1 甜区污染根因：group_neutralize 第二参不得被当字段投票。"""
    got = sd._expr_fields(
        "group_neutralize(rank(predicted_surprise_pct_f12m_revenue_4), subindustry)")
    assert "subindustry" not in got
    assert "predicted_surprise_pct_f12m_revenue_4" in got


def test_p6_strips_all_group_variants():
    assert sd._expr_fields("add(x, industry) + sector") == ["x"]
