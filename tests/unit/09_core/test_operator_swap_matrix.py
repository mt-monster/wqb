# -*- coding: utf-8 -*-
"""operator_swap_matrix 守护测试（用户 2026-11-20 新规则）。"""
import importlib.util, os, sys
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
spec = importlib.util.spec_from_file_location("osm", os.path.join(ROOT, "tools", "research", "operator_swap_matrix.py"))
osm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(osm)


def test_ts_zscore_swaps_are_window_class_only():
    cat = osm._load_catalog()
    r = osm.build_matrix("group_rank(ts_zscore(ts_backfill(F,60),250),industry)", "ts_zscore", cat)
    assert r["category"] == "Time Series"
    assert "ts_rank" in [x["op"] for x in r["replacements"]]
    assert "ts_mean" in [x["op"] for x in r["replacements"]]
    # 无窗/命名参算子必须被 arity 跳过
    skipped = {x["op"] for x in r["skipped"]}
    assert "days_from_last_change" in skipped and "hump" in skipped
    assert all(r["replacements"][i]["expression"].count("(") ==
               r["baseline"].count("(") for i in range(len(r["replacements"])))


def test_group_rank_swaps_keep_group_axis():
    cat = osm._load_catalog()
    r = osm.build_matrix("group_rank(ts_zscore(F,250),industry)", "group_rank", cat)
    assert r["category"] == "Group"
    for x in r["replacements"]:
        assert x["expression"].endswith("industry)"), x["expression"]


def test_noop_rank_shell_agg_skipped():
    cat = osm._load_catalog()
    r = osm.build_matrix("rank(ts_mean(F,66))", "ts_mean", cat)
    skipped = {x["op"]: x["reason"] for x in r["skipped"]}
    assert "no-op" in skipped.get("ts_sum", "")
    assert "no-op" in skipped.get("ts_av_diff", "")


def test_unknown_op_rejected():
    cat = osm._load_catalog()
    with pytest.raises(SystemExit):
        osm.build_matrix("foo(F)", "not_a_real_op_xyz", cat)


def test_nth_replaces_only_selected_occurrence():
    """逐层替换：同名算子多处时 --nth 只换第 N 处（记忆登记的缺陷已修）。"""
    expr = "group_rank(ts_zscore(x, 252), group_rank(y, 252))"
    cat = osm._load_catalog()
    # 不带 nth：全部替换
    full = osm._replace_op(expr, "group_rank", "group_zscore")
    assert full.count("group_zscore(") == 2
    # 带 nth=1：只换第一处
    first = osm._replace_op(expr, "group_rank", "group_zscore", nth=1)
    assert first.count("group_zscore(") == 1
    assert "group_rank(y" in first
    # 带 nth=2：只换第二处
    second = osm._replace_op(expr, "group_rank", "group_zscore", nth=2)
    assert second.count("group_zscore(") == 1
    assert "group_rank(ts_zscore(x" in second


def test_matrix_reports_occurrence_count_and_nth():
    expr = "group_rank(ts_zscore(x, 252), group_rank(y, 252))"
    cat = osm._load_catalog()
    m = osm.build_matrix(expr, "group_rank", cat, nth=2)
    assert m["n_occurrences"] == 2
    assert m["nth"] == 2
    for r in m["replacements"]:
        assert r["expression"].count("group_zscore(") <= 1
        assert "group_rank(ts_zscore(x" in r["expression"]  # 第一处仍是基线


def test_nth_out_of_range_raises():
    expr = "group_rank(ts_zscore(x, 252), group_rank(y, 252))"
    cat = osm._load_catalog()
    with pytest.raises(SystemExit):
        osm.build_matrix(expr, "group_rank", cat, nth=3)


def test_group_swaps_skip_non_binary_arity():
    """group_mean(x,weight,group)/group_backfill(x,group,d,std) 需 ≥3 参，不可当 2 参替换。

    2026-11-20 实测：把这两者当 group_rank 的 2 参替换会生成不可派发表达式，
    被 toolkit 静态门禁拒绝。arity 从平台 definition 精确判定。
    """
    cat = osm._load_catalog()
    assert osm._arity(cat, "group_rank") == 2
    assert osm._arity(cat, "group_zscore") == 2
    assert osm._arity(cat, "group_mean") == 3
    assert osm._arity(cat, "group_backfill") == 3  # std=4.0 是可选参，不计
    r = osm.build_matrix("group_rank(x, industry)", "group_rank", cat)
    skipped = {x["op"]: x["reason"] for x in r["skipped"]}
    assert "arity" in skipped.get("group_mean", "")
    assert "arity" in skipped.get("group_backfill", "")
    repl = {x["op"] for x in r["replacements"]}
    assert "group_zscore" in repl and "group_scale" in repl
    assert "group_mean" not in repl and "group_backfill" not in repl
