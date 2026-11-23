# -*- coding: utf-8 -*-
"""tests/unit/04_gates/test_sa_submit_gate_official_framework.py — SA 双评估闸官方框架落地单测。

覆盖 tools/gates/sa_submit_gate.py 2026-11-23 增补的四维：
  - ★边际论前置：perf-comp-delta<0 ⇒ HOLD（即便档位/池改善/乘数全达标）
  - VF 主导信号：LOW/OK/HIGH/PEAK 分档 + LOW 的「先养 VF」提示
  - SelfGrowth 代理：断更 / 质量倒退 ⇒ REGRESS
  - Quality 六维覆盖：披露缺口，不阻断
  - 向后兼容：不传任何新参数时 verdict 与旧版完全一致
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_GATE_DIR = str(_REPO / "tools" / "gates")
if _GATE_DIR not in sys.path:
    sys.path.insert(0, _GATE_DIR)

import sa_submit_gate as g  # noqa: E402

PY = _REPO / "world-quant-brain-mcp" / ".venv" / "Scripts" / "python.exe"
GATE = _REPO / "tools" / "gates" / "sa_submit_gate.py"


def _pool():
    return {"n": 58, "mean_pc": 0.6301, "mean_self": 0.5976}


def _mult(os_rank=0.85, theme=2.2, pyramid=1.2, vf=0.98):
    # (2.2 + 1.2 - 1) × (1 + 0.85) = 4.44 ≥ MULT_MIN(4.0) ⇒ 乘数闸不拦，
    # 才能单独验证边际论/VF/SelfGrowth/六维四维的影响。
    return {"theme": theme, "pyramid": pyramid, "os_rank": os_rank, "vf": vf}


def _row(**kw):
    base = dict(alpha="T", sharpe=6.0, fitness=7.0, prod=0.55, self=0.50, mutual=0.50)
    base.update(kw)
    return base


# ---------------- 边际论前置（首要判据）----------------

def test_perf_comp_negative_preempts_gold_candidate():
    """其余全达标（档位/池双向/乘数≥4/VF HIGH），仅边际为负 ⇒ 仍压 HOLD。"""
    r = g.evaluate(_row(), _pool(), _mult(), perf_comp_delta=-0.15)
    assert r["verdict"] == "HOLD"
    assert "组合边际为负" in r["reason"]
    assert r["perf_comp_delta"] == -0.15


def test_perf_comp_positive_does_not_block():
    r = g.evaluate(_row(), _pool(), _mult(), perf_comp_delta=0.12)
    assert r["verdict"] == "GO"
    assert r["perf_comp_delta"] == 0.12


def test_perf_comp_zero_does_not_block():
    r = g.evaluate(_row(), _pool(), _mult(), perf_comp_delta=0.0)
    assert r["verdict"] == "GO"


def test_perf_comp_does_not_override_redline():
    """REDLINE 优先级仍高于边际论。"""
    r = g.evaluate(_row(prod=0.75), _pool(), _mult(), perf_comp_delta=0.2)
    assert r["verdict"] == "REDLINE"


# ---------------- VF 主导信号 ----------------

@pytest.mark.parametrize("vf,level", [
    (0.50, "LOW"), (0.73, "LOW"), (0.89, "LOW"),
    (0.90, "OK"), (0.96, "OK"),
    (0.97, "HIGH"), (0.98, "HIGH"),
    (0.99, "PEAK"), (1.00, "PEAK"),
    (None, "UNKNOWN"),
])
def test_vf_signal_levels(vf, level):
    assert g.vf_signal(vf)["level"] == level


def test_vf_low_signal_does_not_change_verdict():
    """VF LOW 只提示，不阻断（保持档位判定独立）。"""
    r = g.evaluate(_row(), _pool(), _mult(vf=0.73), perf_comp_delta=0.1)
    assert r["verdict"] == "GO"
    assert r["vf_signal"]["level"] == "LOW"
    assert "RA" in r["vf_signal"]["note"]


# ---------------- SelfGrowth 代理 ----------------

def test_self_growth_zero_subs_is_regress():
    s = g.self_growth_signal(0, "up")
    assert s["level"] == "REGRESS"
    assert "断更" in s["note"]


def test_self_growth_down_trend_is_regress():
    s = g.self_growth_signal(5, "down")
    assert s["level"] == "REGRESS"
    assert "倒退" in s["note"]


@pytest.mark.parametrize("trend", ["down", "downward", "倒退", "下降"])
def test_self_growth_down_synonyms(trend):
    assert g.self_growth_signal(5, trend)["level"] == "REGRESS"


def test_self_growth_healthy():
    assert g.self_growth_signal(5, "up")["level"] == "OK"
    assert g.self_growth_signal(1, "flat")["level"] == "OK"


def test_self_growth_unknown_when_absent():
    assert g.self_growth_signal(None, None)["level"] == "UNKNOWN"


def test_self_growth_never_blocks():
    r = g.evaluate(_row(), _pool(), _mult(), perf_comp_delta=0.1, subs_7d=0, quality_trend="down")
    assert r["verdict"] == "GO"
    assert r["self_growth"]["level"] == "REGRESS"


# ---------------- Quality 六维覆盖 ----------------

def test_quality_dims_all_six():
    covered = ",".join(g.QUALITY_DIMS)
    q = g.quality_dim_coverage(covered)
    assert len(q["covered"]) == 6 and q["missing"] == []


def test_quality_dims_missing_reported():
    q = g.quality_dim_coverage("MCorrelation,MFitness,MTheme")
    assert set(q["missing"]) == {"MRegion", "MUniverse", "MDelay"}
    assert "3/6" in q["note"]


def test_quality_dims_absent_is_unknown():
    assert g.quality_dim_coverage(None)["note"].startswith("未传")


def test_quality_dims_is_informational_only():
    r = g.evaluate(_row(), _pool(), _mult(), perf_comp_delta=0.1, quality_dims="MCorrelation")
    assert r["verdict"] == "GO"
    assert len(r["quality_dims"]["missing"]) == 5


# ---------------- 向后兼容：不传新参数 ⇒ 结论不变 ----------------

def test_backward_compat_no_new_args():
    r = g.evaluate(_row(), _pool(), _mult())
    assert r["verdict"] == "GO"
    assert r["vf_signal"]["level"] == "UNKNOWN" or r["vf_signal"]["level"] == "HIGH"
    assert r["self_growth"]["level"] == "UNKNOWN"
    assert r["quality_dims"]["note"].startswith("未传")
    assert r["perf_comp_delta"] is None


def test_backward_compat_below_tier_still_below():
    r = g.evaluate(_row(sharpe=4.0), _pool(), _mult())
    assert r["verdict"] == "BELOW_TIER"


# ---------------- CLI ----------------

def test_cli_marginal_negative_exit_code():
    cmd = [str(PY), str(GATE), "--alpha", "T", "--sharpe", "6", "--fitness", "7",
           "--prod", "0.55", "--self", "0.5", "--mutual", "0.5",
           "--theme-mult", "2.2", "--pyramid-mult", "1.2", "--os-rank", "0.85", "--vf", "0.98",
           "--perf-comp-delta", "-0.15"]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 1
    assert "组合边际为负" in out.stdout
    assert "先养 VF" not in out.stdout  # VF 0.98 不应触发 LOW 提示


def test_cli_vf_low_prints_priority_hint():
    cmd = [str(PY), str(GATE), "--alpha", "T", "--sharpe", "6", "--fitness", "7",
           "--prod", "0.55", "--self", "0.5", "--mutual", "0.5",
           "--theme-mult", "2.2", "--pyramid-mult", "1.2", "--os-rank", "0.85", "--vf", "0.73",
           "--perf-comp-delta", "0.1"]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert "先养 VF" in out.stdout
    assert "VF[LOW]" in out.stdout
