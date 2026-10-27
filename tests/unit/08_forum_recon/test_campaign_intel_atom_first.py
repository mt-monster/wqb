# -*- coding: utf-8 -*-
"""`campaign_intel.py atom-first` 守护（2026-10-26 用户指令「ATOM 优先，其他只作备选」）。

三条轴：
  1. **闸线不宽于平台**：config 的 `turnover_range` 是全局宽线（0.70），IND/D1 平台
     HIGH_TURNOVER 实际线是 0.40 —— 默认宽线会把 `A1NJVm3e`（TO 0.4722、平台 FAIL）报成「全过」。
     `--turnover-max` 必须能把它拉回 FAIL。
  2. **平台 failed_checks 优先**：回测行 payload 里三种存放形态都要能读出来，并映射进五闸维度；
     认不出的（CONCENTRATED_WEIGHT）进 extras，不得被静默吞掉。
  3. **分流不混排**：atom 区与备选区各自排序，绝不交叉。

依据：docs/reference/ind_campaign_runbook_20261025.md §9（官方 single-dataset-alphas 口径）。
"""
import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load(name="campaign_intel_atom_first_probe"):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def test_parser_atom_first_defaults():
    m = _load()
    ap = m.build_parser()
    a = ap.parse_args(["atom-first", "--region", "IND"])
    assert a.delay == 1
    assert a.min_sharpe == 0.8
    assert a.top == 20
    assert a.turnover_max is None
    assert a.include_submitted is False
    assert a.dataset == []


def test_turnover_cap_restores_platform_line():
    """A1NJVm3e：TO 0.4722，config 宽线放行，IND 平台线 0.40 必须拦。"""
    m = _load()
    failed_wide, n_wide = m._atom_gate_flags(5.19, 3.55, 2.37, 2.11, 0.4722, 1)
    assert failed_wide == [] and n_wide == 5          # 宽线：误报「全过」
    failed_ind, n_ind = m._atom_gate_flags(5.19, 3.55, 2.37, 2.11, 0.4722, 1,
                                           turnover_max=0.4)
    assert failed_ind == ["TO"] and n_ind == 4


def test_gate_flags_five_dimensions():
    m = _load()
    assert m._atom_gate_flags(1.0, 0.9, 1.2, 0.8, 0.02, 1)[0] == ["S", "F", "2Y", "sub"]
    assert m._atom_gate_flags(None, None, None, None, None, 1)[0] == ["S", "F", "2Y", "sub", "TO"]


def test_payload_failed_checks_three_shapes():
    m = _load()
    assert m._payload_failed_checks('{"failed_checks": ["HIGH_TURNOVER"]}') == ["HIGH_TURNOVER"]
    assert m._payload_failed_checks(
        '{"checks": {"fail": [{"name": "CONCENTRATED_WEIGHT"}]}}') == ["CONCENTRATED_WEIGHT"]
    assert m._payload_failed_checks(
        '{"is": {"checks": [{"name": "LOW_FITNESS", "result": "FAIL"},'
        ' {"name": "LOW_SHARPE", "result": "PASS"}]}}') == ["LOW_FITNESS"]
    assert m._payload_failed_checks(None) == []
    assert m._payload_failed_checks("not-json") == []


def test_merge_platform_failures_maps_and_keeps_extras():
    m = _load()
    failed, extras = m._merge_platform_failures([], ["HIGH_TURNOVER", "CONCENTRATED_WEIGHT"])
    assert failed == ["TO"]
    assert extras == ["CONCENTRATED_WEIGHT"]
    # 已在本地判定里的维度不重复追加
    failed, extras = m._merge_platform_failures(["TO"], ["HIGH_TURNOVER"])
    assert failed == ["TO"] and extras == []
    # 2Y 两个载体都映射到同一维
    failed, _ = m._merge_platform_failures([], ["IS_LADDER_SHARPE"])
    assert failed == ["2Y"]


def test_submitted_filter_sql_uses_status_not_stage():
    """缺省排除已提交件必须作用于 alphas.status（stage=IS 的 ACTIVE 也要排除）。"""
    src = open(os.path.join(REPO, "tools", "campaign_intel.py"), encoding="utf-8").read()
    assert "al.status NOT IN" in src and "ACTIVE" in src
