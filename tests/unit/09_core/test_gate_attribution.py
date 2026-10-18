# -*- coding: utf-8 -*-
"""``wqb.gate_attribution`` 单测 —— 闸失败归因（只差一两闸先归因再定向推闸）。

夹具全部取自 **2026-10-16 KOR 实测读数**，不是构造值：本组的价值就是「公式与判据
对真实平台数据成立」，换夹具等于失去意义。

覆盖三条主线：
1. F 闸闭式公式 ``F = S×√(returns/max(TO,0.125))``（三点反解，含 TO<地板 的两例）
2. ``failing_gates`` 的口径：WARNING 计入失败、且**不轻信状态桶**（pass 里 value<limit 也算失败）
3. 归因路由：剪刀差 ⇒ BLOCKED/SWITCH；ladder 近段衰减 ⇒ SWITCH_AXIS；降级路径不崩
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))

from wqb.gate_attribution import (  # noqa: E402
    TO_FLOOR,
    attribute,
    detect_scissor,
    failing_gates,
    fitness_feasibility,
    fitness_formula,
    normalize_checks,
    normalize_metrics,
    normalize_yearly,
)


# ---------------------------------------------------------------------------
# 1. F 闸公式：三点反解（alpha_id, S, returns, TO, 平台 F）
# ---------------------------------------------------------------------------

F_CASES = [
    ("akVJLlWO", 1.51, 0.0746, 0.0852, 1.17),   # TO < 地板 ⇒ 无地板公式会算成 1.41
    ("QPYr21wg", 1.29, 0.101, 0.0203, 1.16),   # TO << 地板
    ("bl82VavN", 1.79, 0.0933, 0.2835, 1.03),  # TO > 地板
]


@pytest.mark.parametrize("alpha_id,s,ret,to,platform", F_CASES)
def test_fitness_formula_matches_platform(alpha_id, s, ret, to, platform):
    assert fitness_formula(s, ret, to) == pytest.approx(platform, abs=0.005)


def test_floor_is_load_bearing():
    """TO 低于地板时公式必须被地板托住——否则 akVJLlWO 会差 0.24。"""
    naive = 1.51 * (0.0746 / 0.0852) ** 0.5
    assert naive == pytest.approx(1.41, abs=0.02)
    assert fitness_formula(1.51, 0.0746, 0.0852) == pytest.approx(1.17, abs=0.01)
    assert TO_FLOOR == 0.125


# ---------------------------------------------------------------------------
# 2. F 闸可行性：闭式 TO 天花板 + 「减速不可达」判定
# ---------------------------------------------------------------------------

def test_feasibility_gives_exact_to_ceiling():
    """npAknPww 实测：S 1.62 / ret 0.081 / TO 0.2819 ⇒ 天花板 0.2126，需砍 24.6%。"""
    f = fitness_feasibility(1.62, 0.081, 0.2819, target=1.0)
    assert f["to_target"] == pytest.approx(0.2126, abs=1e-3)
    assert f["feasible_by_slowing"] is True
    assert f["arithmetic_verdict"] == "slowing_enough"
    assert f["to_cut_pct"] == pytest.approx(0.2459, abs=1e-3)


def test_feasibility_impossible_when_below_floor():
    """to_target ≤ 地板 ⇒ 减速路线数学上不可达（实测导出 0.0432 < 0.125）。"""
    f = fitness_feasibility(1.2, 0.03, 0.5, target=1.0)
    assert f["to_target"] < TO_FLOOR
    assert f["feasible_by_slowing"] is False
    assert f["arithmetic_verdict"] == "need_more_returns_or_sharpe"


def test_feasibility_already_passing():
    f = fitness_feasibility(1.79, 0.0933, 0.2835, target=1.0)
    assert f["arithmetic_verdict"] == "already_passes"


# ---------------------------------------------------------------------------
# 3. failing_gates 口径
# ---------------------------------------------------------------------------

def test_warning_counts_as_failure():
    """平台把 WARNING 视同 FAIL 计入 failed_ra（npAkbXl3 实测）。"""
    checks = {"fail": [], "warning": [{"name": "LOW_SHARPE", "value": 1.48, "limit": 1.58}]}
    names = [g["name"] for g in failing_gates(checks)]
    assert names == ["LOW_SHARPE"]


def test_does_not_trust_state_bucket():
    """列在 pass 里但 value 真没过线 ⇒ 照样判失败（口径漂移防护）。"""
    checks = {"fail": [], "warning": [], "pass": [
        {"name": "IS_LADDER_SHARPE", "value": 1.17, "limit": 1.58}]}
    gates = failing_gates(checks)
    assert [g["name"] for g in gates] == ["IS_LADDER_SHARPE"]
    assert gates[0]["state"] == "value_violation"
    assert gates[0]["direction"] == "lower"


def test_upper_bound_gates_are_not_misjudged_as_fail():
    """`HIGH_TURNOVER` 是上界闸：TO 0.0872 < limit 0.7 ⇒ 通过，**不得**判失败。

    2026-10-17 真实取数实证：`78oQl0n5` 曾因缺少方向表被误报「失败闸 1 道
    HIGH_TURNOVER」，进而把全闸通过的候选判成 PUSH_TARGETED。
    """
    checks = {"fail": [], "warning": [], "pass": [
        {"name": "HIGH_TURNOVER", "value": 0.0872, "limit": 0.7},
        {"name": "LOW_TURNOVER", "value": 0.0872, "limit": 0.01}]}
    assert failing_gates(checks) == []


def test_upper_bound_gate_fails_when_exceeding():
    checks = {"fail": [], "warning": [], "pass": [
        {"name": "HIGH_TURNOVER", "value": 0.85, "limit": 0.7}]}
    gates = failing_gates(checks)
    assert [g["name"] for g in gates] == ["HIGH_TURNOVER"]
    assert gates[0]["direction"] == "upper"


def test_normalize_yearly_accepts_raw_recordset():
    """裸 API 的 yearly-stats 是 ``[schema, row…]``，不归一会 AttributeError。"""
    raw = [["year", "sharpe", "turnover"],
           [2021, 0.65, 0.35], [2022, 1.88, 0.60], [2023, 1.31, 0.53]]
    ys = normalize_yearly(raw)
    assert len(ys) == 3
    assert ys[1]["year"] == 2022 and ys[1]["sharpe"] == 1.88


def test_normalize_metrics_reads_inline_is_fields():
    """裸 API 把指标内联在 ``is`` 里（无 metrics 子键）。"""
    detail = {"is": {"sharpe": 1.6, "turnover": 0.0872, "returns": 0.0788,
                     "fitness": 1.27},
              "checks": [{"name": "IS_LADDER_SHARPE", "value": 2.27,
                          "limit": 1.58, "result": "PASS"}]}
    m = normalize_metrics(detail)
    assert m["turnover"] == 0.0872 and m["returns"] == 0.0788
    assert m["two_year_sharpe"] == 2.27


def test_non_numeric_checks_excluded():
    checks = {"fail": [], "warning": [{"name": "MATCHES_THEMES"}], "pass": [
        {"name": "LOW_SHARPE", "value": 1.79, "limit": 1.58}]}
    assert failing_gates(checks) == []


def test_platform_limit_wins_over_fallback():
    """闸线取平台 limit；平台没给才退到 DEFAULTS。"""
    g = failing_gates({"fail": [{"name": "LOW_SHARPE", "value": 1.5}]})[0]
    assert g["limit"] == 1.58


# ---------------------------------------------------------------------------
# 4. 两种平台形状都要吃（list 形状漏判 = 静默失效）
# ---------------------------------------------------------------------------

def test_normalize_checks_list_shape():
    """list 形状（裸 API）必须归一成功：FAIL 被认出、PASS 且 value≥limit 不算。"""
    raw = [{"name": "LOW_FITNESS", "result": "FAIL", "value": 0.87, "limit": 1.0},
           {"name": "LOW_SHARPE", "result": "PASS", "value": 1.62, "limit": 1.58},
           {"name": "MATCHES_THEMES", "result": "WARNING"}]
    norm = normalize_checks(raw)
    assert [e["name"] for e in norm["fail"]] == ["LOW_FITNESS"]
    # 只剩 LOW_FITNESS：LOW_SHARPE 1.62 ≥ 1.58 不算，MATCHES_THEMES 非数值闸被排除
    assert [g["name"] for g in failing_gates(norm)] == ["LOW_FITNESS"]


def test_normalize_checks_list_shape_warning_becomes_failure():
    """list 形状下 WARNING 同样计入失败（npAkbXl3 口径）。"""
    raw = [{"name": "LOW_SHARPE", "result": "WARNING", "value": 1.48, "limit": 1.58},
           {"name": "LOW_SHARPE_PLACEHOLDER", "result": "PASS"}]
    norm = normalize_checks(raw)
    assert [g["name"] for g in failing_gates(norm)] == ["LOW_SHARPE"]


def test_normalize_metrics_both_shapes():
    assert normalize_metrics({"metrics": {"sharpe": 1.5}})["sharpe"] == 1.5
    assert normalize_metrics({"is": {"metrics": {"sharpe": 1.7}}})["sharpe"] == 1.7


# ---------------------------------------------------------------------------
# 5. 剪刀差（KOR 分析师族 6 点实测）
# ---------------------------------------------------------------------------

SCISSOR_SIBLINGS = [
    {"label": "akVJLlWO", "sharpe": 1.51, "prod_corr": 0.6989},
    {"label": "58j7W5KN", "sharpe": 1.53, "prod_corr": 0.7010},
    {"label": "KPmeOmJ1", "sharpe": 1.53, "prod_corr": 0.7010},
    {"label": "xA1wgWKn", "sharpe": 1.55, "prod_corr": 0.7117},
    {"label": "JjP0Z6bA", "sharpe": 1.58, "prod_corr": 0.7063},
    {"label": "QPYe3WpW", "sharpe": 1.58, "prod_corr": 0.7087},
]


def test_scissor_detected_on_real_siblings():
    sc = detect_scissor(SCISSOR_SIBLINGS, sharpe_now=1.51)
    assert sc is not None and sc["same_direction"] is True
    assert sc["verdict"] == "scissor_structural"
    assert sc["crossing"] is False
    assert sc["prod_at_sharpe_158"] >= 0.70


def test_scissor_needs_three_points():
    assert detect_scissor(SCISSOR_SIBLINGS[:2], sharpe_now=1.51) is None


def test_thin_prod_headroom_blocks_sharpe_push():
    """akVJLlWO：prod 0.6989（余量 0.0011）+ 只差 S ⇒ 必须 BLOCKED_BY_CORRELATION。"""
    r = attribute({
        "alpha_id": "akVJLlWO",
        "metrics": {"sharpe": 1.51, "fitness": 1.17, "turnover": 0.0852,
                    "returns": 0.0746, "two_year_sharpe": 2.23},
        "checks": {"fail": [], "warning": [
            {"name": "LOW_SHARPE", "value": 1.51, "limit": 1.58}], "pass": []},
        "correlation": {"production": {"max_correlation": 0.6989, "passes_check": True}},
        "siblings": SCISSOR_SIBLINGS,
    })
    assert r["verdict"] == "BLOCKED_BY_CORRELATION"
    assert r["gate_count"] == 1
    assert r["eligible_for_targeted_push"] is True
    assert "prod 中性" in r["stop_rule"]


# ---------------------------------------------------------------------------
# 6. 逐年归因：按闸分诊 + 样本量诚实性
# ---------------------------------------------------------------------------

YR_SHORTINTEREST = [
    {"year": str(y), "sharpe": s} for y, s in
    [(2014, 2.55), (2015, 3.57), (2016, 3.53), (2017, 1.78), (2018, 1.80),
     (2019, 1.42), (2020, 1.07), (2021, 0.31), (2022, 0.66), (2023, 1.60)]
]


def test_ladder_recent_decay_routes_to_switch_axis():
    """bl82VavN：只差 2Y 一闸，但末 2 年均值 1.13 << 前段 2.00 ⇒ 机制层天花板。"""
    r = attribute({
        "alpha_id": "bl82VavN",
        "metrics": {"sharpe": 1.79, "fitness": 1.03, "turnover": 0.2835,
                    "returns": 0.0933, "two_year_sharpe": 1.17},
        "checks": {"fail": [{"name": "IS_LADDER_SHARPE", "value": 1.17, "limit": 1.58}],
                   "warning": [{"name": "MATCHES_THEMES"}],
                   "pass": [{"name": "LOW_SHARPE", "value": 1.79, "limit": 1.58},
                            {"name": "LOW_FITNESS", "value": 1.03, "limit": 1.0}]},
        "yearly": YR_SHORTINTEREST,
        "correlation": {"production": {"max_correlation": 0.4616, "passes_check": True}},
    })
    assert r["gate_count"] == 1
    ya = r["yearly_attribution"]
    assert ya["class_for_ladder"] == "recent_decay"
    assert ya["flags"] == {"single_collapse": True, "recent_decay": True}
    assert r["verdict"] == "SWITCH_AXIS"
    # prod 余量 0.24 ⇒ 不是相关性问题，是机制问题
    assert r["correlations"]["prod"]["headroom"] > 0.2


def test_three_year_sample_flagged_not_ok():
    """3 年样本无法做「前段 vs 末 2 段」对比 ⇒ 必须自报 sample_ok=False。"""
    r = attribute({
        "alpha_id": "x",
        "metrics": {"sharpe": 1.79, "fitness": 1.03, "turnover": 0.2835, "returns": 0.0933},
        "checks": {"fail": [{"name": "IS_LADDER_SHARPE", "value": 1.17, "limit": 1.58}]},
        "yearly": [{"year": "2021", "sharpe": 0.31}, {"year": "2022", "sharpe": 0.66},
                   {"year": "2023", "sharpe": 1.60}],
    })
    assert r["yearly_attribution"]["sample_ok"] is False
    assert r["yearly_attribution"]["n_years"] == 3


def test_degradation_without_optional_inputs():
    """缺 yearly / correlation 时不崩，仍给出通用杠杆。"""
    r = attribute({
        "alpha_id": "x",
        "metrics": {"sharpe": 1.2, "fitness": 0.5, "turnover": 0.5, "returns": 0.03},
        "checks": {"fail": [{"name": "LOW_SHARPE", "value": 1.2, "limit": 1.58},
                            {"name": "LOW_FITNESS", "value": 0.5, "limit": 1.0}]},
    })
    assert r["yearly_attribution"] is None
    assert r["correlations"]["measured"] is False
    assert r["verdict"] in {"PUSH_TARGETED", "SWITCH_AXIS", "BLOCKED_BY_CORRELATION"}
    gates = {d["gate"] for d in r["diagnoses"]}
    assert gates == {"LOW_SHARPE", "LOW_FITNESS"}
    # F 闸在缺数据时也必须给出闭式结论（不可达）
    f_diag = next(d for d in r["diagnoses"] if d["gate"] == "LOW_FITNESS")
    assert f_diag["fitness_feasibility"]["arithmetic_verdict"] == "need_more_returns_or_sharpe"


def test_unmapped_gate_is_explicit():
    """本表未收的闸要显式标 UNMAPPED，不能静默吞掉。"""
    r = attribute({
        "alpha_id": "x",
        "metrics": {"sharpe": 1.0, "fitness": 0.5, "turnover": 0.4, "returns": 0.02},
        "checks": {"fail": [{"name": "LOW_RETURNS", "value": 0.02, "limit": 0.05}]},
    })
    assert r["diagnoses"][0]["cause_class"] == "UNMAPPED"
    assert "gate-attribution.md" in r["diagnoses"][0]["note"]


def test_more_than_two_gates_flagged_ineligible():
    r = attribute({
        "alpha_id": "npAknPww",
        "metrics": {"sharpe": 1.62, "fitness": 0.87, "turnover": 0.2819, "returns": 0.081},
        "checks": {"fail": [{"name": "LOW_FITNESS", "value": 0.87, "limit": 1.0},
                            {"name": "IS_LADDER_SHARPE", "value": 1.51, "limit": 1.58}],
                   "warning": [{"name": "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
                                "value": 0.89, "limit": 1.15}]},
        "yearly": YR_SHORTINTEREST,
    })
    assert r["gate_count"] == 3
    assert r["eligible_for_targeted_push"] is False


def test_zero_simulations_consumed():
    """归因必须是零成本动作——这条是机制承诺，靠测试钉住。"""
    r = attribute({"alpha_id": "x",
                   "metrics": {"sharpe": 1.5, "fitness": 1.1, "turnover": 0.1, "returns": 0.05},
                   "checks": {"fail": [{"name": "LOW_SHARPE", "value": 1.5, "limit": 1.58}]}})
    assert r["simulations_consumed"] == 0


def test_all_levers_have_evidence_and_cost():
    """杠杆表每条都要可追溯（证据 + 代价），否则又变成通用清单。"""
    r = attribute({
        "alpha_id": "x",
        "metrics": {"sharpe": 1.5, "fitness": 0.9, "turnover": 0.28, "returns": 0.08},
        "checks": {"fail": [{"name": "LOW_FITNESS", "value": 0.9, "limit": 1.0},
                            {"name": "IS_LADDER_SHARPE", "value": 1.4, "limit": 1.58}]},
        "yearly": YR_SHORTINTEREST,
    })
    for d in r["diagnoses"]:
        assert d["levers"], f"{d['gate']} 没有杠杆"
        for lv in d["levers"]:
            assert lv["rank"] >= 1 and lv["lever"] and lv["rationale"]
            assert "evidence" in lv and "cost" in lv

# ---------------------------------------------------------------------------
# 相关性闸（2026-10-17 补）：平台把 PROD/SELF 标 PENDING，真值在 correlation
# 不补这一层 ⇒ 「RA 全过 + prod 不过」会误报「失败闸 0 道」
# ---------------------------------------------------------------------------

def _mk_corr_case(prod: float, selfc: float, sharpe: float = 1.60) -> dict:
    return {
        "alpha_id": "corr_case",
        "metrics": {"sharpe": sharpe, "fitness": 1.27, "turnover": 0.0872,
                    "returns": 0.0788, "two_year_sharpe": 2.27},
        "checks": {"fail": [], "warning": [{"name": "MATCHES_THEMES"}], "pass": [
            {"name": "LOW_SHARPE", "value": sharpe, "limit": 1.58},
            {"name": "LOW_FITNESS", "value": 1.27, "limit": 1.0},
            {"name": "IS_LADDER_SHARPE", "value": 2.27, "limit": 1.58, "year": 2},
            {"name": "PROD_CORRELATION", "value": None, "state": "PENDING"},
            {"name": "SELF_CORRELATION", "value": None, "state": "PENDING"},
        ]},
        "correlation": {"production": {"max_correlation": prod, "passes_check": prod < 0.70},
                        "self": {"max_correlation": selfc, "passes_check": selfc < 0.70}},
    }


def test_correlation_is_first_class_gate():
    """prod=0.7051 必须被计入失败闸（旧版会误报 count=0）。"""
    r = attribute(_mk_corr_case(prod=0.7051, selfc=0.49))
    assert r["gate_count"] == 1
    assert [f["name"] for f in r["failed_gates"]] == ["PROD_CORRELATION"]
    assert r["verdict"] == "PUSH_CORRELATION_CORNER"


def test_correlation_strict_inequality_at_exactly_limit():
    """提交层是严格不等式：prod 恰为 0.7000 判 FAIL（KOR 实测 passes_check=false）。"""
    r = attribute(_mk_corr_case(prod=0.7000, selfc=0.49))
    assert [f["name"] for f in r["failed_gates"]] == ["PROD_CORRELATION"]


def test_all_gates_pass_yields_ready():
    """实测全闸通过样本 78oQl0n5：prod 0.6991 / self 0.4957 ⇒ READY，不再建议推。"""
    r = attribute(_mk_corr_case(prod=0.6991, selfc=0.4957))
    assert r["gate_count"] == 0
    assert r["verdict"] == "READY"


def test_ra_pass_without_correlation_measurement_is_not_ready():
    """RA 全过但没测相关性 ⇒ 不得判 READY（防止凭『0 道失败』误判就绪）。"""
    p = _mk_corr_case(prod=0.0, selfc=0.0)
    p.pop("correlation")
    r = attribute(p)
    assert r["verdict"] == "PUSH_TARGETED"


def test_mechanism_crowded_vs_knife_edge():
    """余量 <0.01 = 刀锋（继续找角点）；远离线 = 机制拥挤（换字段）。"""
    near = attribute(_mk_corr_case(prod=0.7051, selfc=0.49))
    far = attribute(_mk_corr_case(prod=0.78, selfc=0.49))
    assert near["diagnoses"][0]["cause_class"] == "knife_edge"
    assert far["diagnoses"][0]["cause_class"] == "mechanism_crowded"
    assert near["verdict"] == "PUSH_CORRELATION_CORNER"
    assert far["verdict"] == "BLOCKED_BY_CORRELATION"
