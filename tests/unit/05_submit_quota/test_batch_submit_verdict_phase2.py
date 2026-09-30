# -*- coding: utf-8 -*-
"""2026-09-24：tools/batch_submit_verdict.py Phase2 字段语义回归。

实证（2026-09-23 P0-1 GLB/ASI 收割，19/19 全部假阴性）：
  1. check_self_correlation 顶层返回 passes_check（没有 all_passed）——旧代码读
     all_passed 使 self 恒为 FAIL；
  2. check_correlation(production) 的 max/passes 在 checks["production"] 里——旧代码
     读顶层 max_correlation 使 prod_max 恒 None；
  3. prod 未决（pending / correlation_busy / data_unavailable）时 all_passed=None，
     bool(None)=False 被误判 FAIL——未决≠撞墙。
"""
from tools.batch_submit_verdict import _phase2_outcome


def _prod_decided(max_corr, passes):
    """check_correlation(production) 已决返回结构（brain_mixin_correlation.py:813-821）。"""
    return {
        "alpha_id": "X", "threshold": 0.7, "correlation_type": "production",
        "checks": {"production": {"max_correlation": max_corr, "passes_check": passes}},
        "all_passed": passes,
    }


def _prod_pending(status="pending"):
    """check_correlation(production) 未决返回结构（pending/busy/data_unavailable 同型）。"""
    return {
        "alpha_id": "X", "threshold": 0.7, "correlation_type": "production",
        "checks": {"production": {"max_correlation": None, "passes_check": None,
                                  "status": status}},
        "all_passed": None, "status": status,
    }


def _self_decided(max_corr):
    """check_self_correlation 已决返回结构（brain_mixin_correlation.py:697-705）。"""
    return {
        "alpha_id": "X", "threshold": 0.7, "correlation_type": "self",
        "max_correlation": max_corr, "passes_check": max_corr < 0.7,
        "local_calculation": True,
    }


def test_self_uses_passes_check_not_all_passed():
    """bug 1：self 判定必须读 passes_check；旧代码读不存在的 all_passed 恒 FAIL。"""
    oc = _phase2_outcome(_prod_decided(0.5, True), _self_decided(0.0))
    assert oc["self_pass"] is True          # 旧代码这里是 False
    assert oc["verdict"] == "PROMOTE"


def test_prod_max_read_from_checks_production():
    """bug 2：prod max/passes 在 checks['production']，不在顶层。"""
    oc = _phase2_outcome(_prod_decided(0.62, True), _self_decided(0.30))
    assert oc["prod_max"] == 0.62           # 旧代码恒 None
    assert oc["prod_pass"] is True
    assert oc["verdict"] == "PROMOTE"


def test_prod_undecided_is_not_fail():
    """bug 3：prod 未决（all_passed=None）不得误判 FAIL，应为 PENDING 留待下轮。"""
    for status in ("pending", "correlation_busy", "data_unavailable"):
        oc = _phase2_outcome(_prod_pending(status), _self_decided(0.10))
        assert oc["prod_pass"] is None      # 未决不是 False
        assert oc["verdict"] == "PENDING"   # 旧代码判 BLOCKED_CORR（假阴性）
        assert oc["self_pass"] is True


def test_prod_wall_blocks():
    """prod 已决且 ≥0.7 → BLOCKED_PROD（真撞墙仍要拦）。"""
    oc = _phase2_outcome(_prod_decided(0.83, False), _self_decided(0.10))
    assert oc["verdict"] == "BLOCKED_PROD"
    assert oc["prod_pass"] is False


def test_self_wall_blocks():
    """self 已决且 ≥0.7 → BLOCKED_SELF。"""
    oc = _phase2_outcome(_prod_decided(0.50, True), _self_decided(0.90))
    assert oc["verdict"] == "BLOCKED_SELF"
    assert oc["self_pass"] is False


def test_legacy_top_level_fallback():
    """兜底：缓存命中/旧结构只有顶层 max_correlation 时仍能判。"""
    res_prod = {"max_correlation": 0.55, "all_passed": True}
    oc = _phase2_outcome(res_prod, _self_decided(0.20))
    assert oc["prod_max"] == 0.55
    assert oc["prod_pass"] is True
    assert oc["verdict"] == "PROMOTE"


def test_none_inputs_are_pending_not_fail():
    """异常路径：非 dict 返回（None 等）不判死，PENDING 留待下轮。"""
    oc = _phase2_outcome(None, None)
    assert oc["verdict"] == "PENDING"
