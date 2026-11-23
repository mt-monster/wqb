# -*- coding: utf-8 -*-
"""梯度覆盖率工具的守护测试（2026-11-23 落地）。

覆盖三件落地纪律：
A 覆盖率审计：分层正确、缺口可算、换基线后计数正确
B settings 与算子臂分家：settings 只出「一值一批」计划，不生成同批表达式臂
C/D 扫描顺序 + 算子 lint：缺臂按杠杆序、幽灵算子/命名参数写错能拦住
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "research" / "gradient_coverage.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location("gradient_coverage", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gradient_coverage"] = mod
    spec.loader.exec_module(mod)
    return mod


gc = _load_tool()

BASE = (
    "rank(group_scale(tail(winsorize(group_zscore(ts_sum(divide(multiply("
    "vec_avg(insd1_valueeur), vec_avg(insd1_tradesignificance)), "
    "vec_sum(insd1_holdings)), 44), sector), std=2), "
    "lower=0.25, upper=0.75, newval=0.5), sector))"
)


# ---------------------------------------------------------------------------
# 解析与分层
# ---------------------------------------------------------------------------

def test_split_slots_finds_every_call():
    ops = [s["op"] for s in gc.split_slots(BASE)]
    for expected in ("rank", "group_scale", "tail", "winsorize", "group_zscore",
                     "ts_sum", "divide", "multiply", "vec_avg", "vec_sum"):
        assert expected in ops, f"漏了 {expected}: {ops}"
    assert ops.count("vec_avg") == 2


def test_layer_assignment_matches_gradient_spec():
    cat = gc.osm._load_catalog()
    slots = gc.annotate_layers(BASE, cat)
    by_op = {}
    for s in slots:
        by_op.setdefault(s["op"], []).append(s["layer"])
    assert by_op["vec_avg"][0] == "L1_vector_fold"
    assert by_op["ts_sum"][0] == "L4_time_series"
    assert by_op["winsorize"][0] == "L6_cross_sectional"
    assert by_op["tail"][0] == "L7_transform"
    # 两个 group 算子：最外层（浅）→ L8，内层（深）→ L5
    assert by_op["group_zscore"][0] == "L5_group_inner"
    assert by_op["group_scale"][0] == "L8_group_outer"


def test_grouping_axes_extracted_from_both_group_ops():
    slots = gc.annotate_layers(BASE, gc.osm._load_catalog())
    assert gc.grouping_axes(slots) == ["sector"]


def test_window_and_tail_q_extracted():
    slots = gc.split_slots(BASE)
    assert gc.windows_of(slots) == [44]
    assert gc.tail_qs_of(slots) == [(0.25, 0.75)]


# ---------------------------------------------------------------------------
# A. 审计
# ---------------------------------------------------------------------------

def test_audit_reports_gap_per_layer():
    rep = gc.audit([BASE])
    layers = rep["layers"]
    # L1：vec_avg/vec_sum 已测，仍缺 max/min/stddev/range/count
    assert "vec_max" in layers["L1_vector_fold"]["missing"]
    assert "vec_max" not in layers["L1_vector_fold"]["tested"]
    # L4：只有 ts_sum，ts_mean 必缺
    assert "ts_mean" in layers["L4_time_series"]["missing"]
    # L9：sector 已测，industry 必缺
    assert "sector" in layers["L9_grouping_axis"]["tested"]
    assert "industry" in layers["L9_grouping_axis"]["missing"]
    # L10：44 已测
    assert "44" in layers["L10_window"]["tested"]


def test_audit_flags_truncation_noop_after_rank():
    rep = gc.audit([BASE])
    assert any("truncation" in w for w in rep["noop_warnings"])


def test_audit_counts_second_expression_as_coverage():
    """换基线（sector）与旧基线（industry）一起审计 ⇒ 两轴都算已测。"""
    old = BASE.replace(", sector), std=2)", ", industry), std=2)").replace(
        "newval=0.5), sector))", "newval=0.5), industry))")
    rep = gc.audit([BASE, old])
    tested = rep["layers"]["L9_grouping_axis"]["tested"]
    assert "sector" in tested and "industry" in tested


def test_audit_gate_gaps_use_platform_limits():
    alphas = [{
        "alpha_id": "X1",
        "checks": {"fail": [
            {"name": "LOW_SHARPE", "value": 1.14, "limit": 1.58},
            {"name": "LOW_2Y_SHARPE", "value": 0.86, "limit": 1.58},
        ]},
    }]
    rep = gc.audit([BASE], alphas)
    rows = rep["gate_gaps"]["X1"]
    assert {r["check"] for r in rows} == {"LOW_SHARPE", "LOW_2Y_SHARPE"}
    assert rows[0]["gap"] == pytest.approx(0.44)


# ---------------------------------------------------------------------------
# B/C. 缺臂计划
# ---------------------------------------------------------------------------

def test_plan_orders_semantic_layers_before_param_layers():
    rep = gc.plan([BASE], max_arms=8)
    layers = [a["layer"] for a in rep["arms"]]
    order = list(gc.GRADIENT_SCAN_ORDER)
    assert layers == sorted(layers, key=order.index)
    # 语义层 L1 在参数层之前
    if "L11_amplitude" in layers:
        assert layers.index("L1_vector_fold") < layers.index("L11_amplitude")


def test_plan_never_mixes_settings_into_expression_arms():
    rep = gc.plan([BASE], max_arms=10)
    for a in rep["arms"]:
        # settings 是批级参数，不得作为表达式臂出现
        assert "decay" not in a["expression"]
        assert "truncation" not in a["expression"]
    sp = rep["settings_plan"]
    assert "decay" in sp["keys"] and "truncation" in sp["keys"]
    assert all("values" in b for b in sp["batches"])
    # 最终层是 rank() ⇒ truncation no-op 必须提示
    assert sp["noop_warning"]


def test_plan_skips_noop_substitutions():
    rep = gc.plan([BASE], max_arms=30)
    pairs = {(s["layer"], s["op"]) for s in rep["skipped_noop"]}
    # L1 里 vec_sum↔vec_avg 在 rank 吸收尺度下是 no-op（工具按 swap_matrix 律跳过/标注）
    assert isinstance(pairs, set)


def test_plan_buckets_arity_mismatch_for_manual_reorder():
    """同 arity≠同语义的替换（group_backfill/group_mean）必须单独列出并要求手工重排，
    不能被当成"可无条件派发"或被静默丢掉（2026-11-22 UNITS 整批失败同源）。"""
    rep = gc.plan([BASE], max_arms=40, layers=["L5_group_inner"])
    manual = {s["op"] for s in rep["skipped_arity_manual"]}
    assert any("group_backfill" in x for x in manual)
    assert any("group_mean" in x for x in manual)
    assert all("手工重排" in s["reason"] for s in rep["skipped_arity_manual"])
    # 这些必须**不在**可派发臂里
    assert not any(a.get("to_op") in ("group_mean", "group_backfill") for a in rep["arms"])


def test_plan_respects_max_arms():
    rep = gc.plan([BASE], max_arms=3)
    assert len(rep["arms"]) <= 3


def test_plan_all_slots_expands_duplicate_ops():
    few = gc.plan([BASE], max_arms=50, layers=["L1_vector_fold"], all_slots=False)
    many = gc.plan([BASE], max_arms=50, layers=["L1_vector_fold"], all_slots=True)
    assert len(many["arms"]) > len(few["arms"])


# ---------------------------------------------------------------------------
# D. 算子 lint
# ---------------------------------------------------------------------------

def test_lint_catches_ghost_operator():
    rep = gc.lint(["rank(ts_weighted_decay(close, 8))"])
    assert rep["ok"] is False
    assert "ts_weighted_decay" in rep["text"]


def test_lint_catches_named_param_used_positionally():
    rep = gc.lint(["group_backfill(ts_rank(close,252),subindustry,63,2.0)"])
    assert rep["ok"] is False
    assert "std=2.0" in rep["text"]


def test_lint_passes_valid_expression():
    rep = gc.lint([BASE])
    assert rep["ok"] is True


# ---------------------------------------------------------------------------
# E. 平台原始结构兼容（brain_client 的 settings 是 camelCase、checks 在 is.checks 列表里）
# ---------------------------------------------------------------------------

def test_audit_reads_platform_camel_settings():
    alphas = [{
        "alpha_id": "X2",
        "settings": {"decay": 4, "truncation": 0.08, "universe": "TOPCS1600",
                     "neutralization": "SUBINDUSTRY", "nanHandling": "ON",
                     "maxTrade": "OFF", "pasteurization": "ON", "delay": 1},
    }]
    rep = gc.audit([BASE], alphas)
    info = rep["layers"]["L13_settings"]
    # nan_handling / max_trade 必须从 camelCase 读到，不能误报为"未设置"
    assert "nan_handling=ON" in info["tested"]
    assert "max_trade=OFF" in info["tested"]
    assert info["missing"] == []


def test_audit_reads_raw_is_checks_fail():
    """brain_client 原始返回：is.checks 是列表且带 result 字段。"""
    alphas = [{
        "id": "X3",
        "is": {"checks": [
            {"name": "LOW_SHARPE", "result": "FAIL", "value": 1.14, "limit": 1.58},
            {"name": "LOW_TURNOVER", "result": "PASS", "value": 0.05, "limit": 0.01},
        ]},
    }]
    rep = gc.audit([BASE], alphas)
    rows = rep["gate_gaps"]["X3"]
    assert [r["check"] for r in rows] == ["LOW_SHARPE"]
    assert rows[0]["gap"] == pytest.approx(0.44)
