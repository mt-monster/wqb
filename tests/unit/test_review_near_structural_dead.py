# -*- coding: utf-8 -*-
"""2026-09-19：near 池剔除"结构性死信号"（robust/limit 过低），让停止规则 B 真正能触发。

IND w170-175 实证：sentiment21 raw sharpe 1.76 但 LOW_ROBUST_UNIVERSE_SHARPE 0.24（limit 1.0），
此前仍按 sharpe>1.0 入 near → 全灭波记 PARTIAL → 连续 3 波 FAIL 的止损永不生效。
"""
import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _mods():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    for m in ("review_wave", "metrics_cache"):
        sys.modules.pop(m, None)
    return importlib.import_module("review_wave"), importlib.import_module("metrics_cache")


def test_metrics_row_carries_robust_and_sub_universe():
    _, mc = _mods()
    a = {"is": {"sharpe": 1.76, "fitness": 0.65, "margin": 0.00027, "turnover": 0.51,
                "checks": [{"name": "LOW_ROBUST_UNIVERSE_SHARPE", "result": "FAIL", "value": 0.24, "limit": 1},
                           {"name": "LOW_SUB_UNIVERSE_SHARPE", "result": "PASS", "value": 0.62, "limit": 0.5},
                           {"name": "LOW_2Y_SHARPE", "result": "PASS", "value": 1.93, "limit": 1.0}]},
         "regular": "divide(a, b)", "settings": {"neutralization": "STATISTICAL"}}
    r = mc.row_from_alpha("xA3M28op", a)
    assert r["robust_sharpe"] == 0.24 and r["robust_limit"] == 1
    assert r["sub_universe_sharpe"] == 0.62 and r["two_year_sharpe"] == 1.93
    assert r["failed_checks"] == ["LOW_ROBUST_UNIVERSE_SHARPE"]


def test_structurally_dead_and_near_semantics():
    rw, _ = _mods()
    t_near = {"sharpe_min": 1.0}
    dead = {"sharpe": 1.76, "robust_sharpe": 0.24, "robust_limit": 1.0}
    alive = {"sharpe": 1.76, "robust_sharpe": 0.9, "robust_limit": 1.0}
    unknown = {"sharpe": 1.76}                       # robust 缺失 → 不判死
    weak = {"sharpe": 0.8, "robust_sharpe": 0.9, "robust_limit": 1.0}
    assert rw.structurally_dead(dead, t_near) and not rw.structurally_dead(alive, t_near)
    assert not rw.structurally_dead(unknown, t_near)
    assert not rw.is_near(dead, t_near)
    assert rw.is_near(alive, t_near) and rw.is_near(unknown, t_near)
    assert not rw.is_near(weak, t_near)
    # 阈值可调：ratio 0.2 时 0.24/1.0 不再判死
    assert not rw.structurally_dead(dead, {"sharpe_min": 1.0, "robust_min_ratio": 0.2})


def test_robust_ratio_uses_limit_default_one():
    rw, _ = _mods()
    assert rw.robust_ratio({"robust_sharpe": 0.5}) == 0.5
    assert rw.robust_ratio({"robust_sharpe": 0.5, "robust_limit": 0.8}) == 0.625
    assert rw.robust_ratio({}) is None
