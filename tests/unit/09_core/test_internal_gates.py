# -*- coding: utf-8 -*-
"""内部严线接入流水线的守护用例（2026-11-16 用户定案 / 2026-11-19 落地）。

**背景**：2026-11-19 审计发现 `src/wqb/config.py::GATES_INTERNAL`
（prod 0.65 / self 0.50 / turnover∈[5%,20%]）**只有文档、没有任何执行点** ——
`GLOSSARY.md` / `INDEX.md` 都把它写成「研究阶段省配额的本地预筛」，而全仓 grep 显示
唯一读它的是 `index_tables.py`（出表）与 `skill_lint.py`（文档 lint）。
⇒ 「全闸候选」的表述比仓库口径宽一档（实测：EUR 交付 10 颗里 6 颗 prod 在 0.6604–0.6951）。

用户裁定：**接进流水线当硬预筛**。本用例把落地后的语义钉死：
  · prod≥0.65 / self≥0.50 / TO∉[5%,20%] ⇒ 不算 win（降为 near，**不删行**）
  · 未知值（None）**不判不过**（不得因缺数据误降级）
  · margin / returns **只作提示不进闸**（方向与量纲未取得一致口径）
  · `strict_internal=False` 可退回旧行为（便于对照与回滚）
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from wqb.config import GATES_INTERNAL  # noqa: E402
from wqb.knowledge import classify  # noqa: E402


def _m(**kw):
    base = {"sharpe": 2.0, "fitness": 1.2}
    base.update(kw)
    return base


# ------------------------------------------------------------------ 判据本身

def test_internal_gate_covers_prod_self_turnover():
    assert classify.internal_gate_failures(_m(prod_correlation=0.68)) == ["prod"]
    assert classify.internal_gate_failures(_m(self_correlation=0.55)) == ["self"]
    assert classify.internal_gate_failures(_m(turnover=0.30)) == ["turnover"]
    assert classify.internal_gate_failures(_m(turnover=0.01)) == ["turnover"]


def test_internal_gate_passes_clean_metrics():
    assert classify.internal_gate_failures(
        _m(prod_correlation=0.60, self_correlation=0.40, turnover=0.12)) == []


def test_unknown_values_are_not_failures():
    """未知（None）不判不过——不得因缺数据把好件误降级。"""
    assert classify.internal_gate_failures(_m()) == []
    assert classify.internal_gate_failures(
        _m(prod_correlation=0.60, self_correlation=None, turnover=None)) == []


def test_margin_and_returns_are_advisory_only():
    """margin / returns 只作提示，不进闸（方向与量纲未取得一致口径 ⇒ 判错会误杀合格件）。"""
    assert classify.internal_gate_failures(_m(margin=0.0001, returns=0.001)) == []
    assert "margin" in classify.internal_gate_advice(_m(margin=0.0001))
    assert "returns" in classify.internal_gate_advice(_m(returns=0.001))


def test_thresholds_come_from_config_single_source():
    """判据必须读 config.GATES_INTERNAL（唯一事实源），不得在别处硬写数字。"""
    assert classify.internal_gate_failures(
        _m(prod_correlation=float(GATES_INTERNAL["prod_corr_max"]) - 0.001)) == []
    assert classify.internal_gate_failures(
        _m(prod_correlation=float(GATES_INTERNAL["prod_corr_max"]))) == ["prod"]


# ------------------------------------------------------------------ outcome 语义

def test_platform_clean_but_internal_fail_is_near_not_win():
    """只过平台线（prod<0.70）但没过内部严线（prod<0.65）⇒ near，不是 win。"""
    out = classify.outcome("COMPLETE", _m(prod_correlation=0.68, self_correlation=0.40,
                                         turnover=0.12), [], [])
    assert out == "near"


def test_internal_clean_is_win():
    out = classify.outcome("COMPLETE", _m(prod_correlation=0.60, self_correlation=0.40,
                                         turnover=0.12), [], [])
    assert out == "win"


def test_strict_internal_can_be_disabled_for_comparison():
    """旧行为可退回（便于对照/回滚）。"""
    out = classify.outcome("COMPLETE", _m(prod_correlation=0.68, self_correlation=0.40,
                                         turnover=0.12), [], [], strict_internal=False)
    assert out == "win"


def test_unknown_metrics_still_unknown():
    assert classify.outcome("COMPLETE", {"sharpe": None}, [], []) == "unknown"


def test_error_and_dead_paths_unaffected():
    assert classify.outcome("ERROR", _m(prod_correlation=0.9), None, None) == "error"
    # 结构性墙（RN_EXPOSURE / SELF，见 classify.STRUCTURAL_WALLS）优先于内部严线：
    # 墙是更根本的死因（CW 不算结构死——可用 group_backfill 救）。
    assert classify.outcome("COMPLETE", _m(prod_correlation=0.9), ["RN_EXPOSURE"], []) == "dead"
    assert classify.outcome("COMPLETE", _m(prod_correlation=0.9), ["SELF"], []) == "dead"
    # 非结构墙（CW）仍走 near（既有语义，未被本次改动影响）
    assert classify.outcome("COMPLETE", _m(prod_correlation=0.9), ["CW"], []) == "near"


# ------------------------------------------------------------------ 流水线接线

def test_capture_records_internal_failures_in_next_action(tmp_path):
    """capture 把不过项写进 next_action（人工可复核「为何不算全闸」）。"""
    import inspect

    from wqb.knowledge import capture

    src = inspect.getsource(capture)
    assert "internal_gate_failures" in src, "capture 未接入内部严线判据"
    assert "|internal:" in src, "capture 未把不过项写进 next_action"


def test_yield_report_exposes_internal_block(tmp_path):
    """产出率报告并列给出内部严线口径（平台线答「能不能交」，内部线答「质量如何」）。"""
    import inspect

    from wqb.knowledge import yield_report

    src = inspect.getsource(yield_report)
    assert "_internal_stats" in src
    assert '"internal": _internal_stats(rows)' in src
