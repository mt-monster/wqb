# -*- coding: utf-8 -*-
"""`tools/gates/gradient_stop_gate.py` 守护测试（2026-11-23 用户「三、优化空间 全部落地」）。

验收口径（每条都对应一条被实证过的浪费）：
1. D1 L1 极差止损：insiders N1 实测 max_S 0.68 / 极差 0.69 ⇒ 必须判 STOP（否则会白烧 L2–L5）
2. D1 反向：insiders N2 极差 0.93 ⇒ 必须判 CONTINUE（risk60 T4 极差 0.78 一路做到 L5 才出货）
3. D2 TO 带：带外高 S（N1 0.68@57.8%）不得当结论，带内最佳才是真读数
4. D3 三点检测：S/F/2Y 冠军不重合 ⇒ SWING（本轮 8 个模板全 SWING，只有 risk60 T4 一件 COINCIDE）
5. D4 三查：裸常数 UNITS / 已标准化字段再 zscore / VECTOR 未降维
6. D5 prod 前置：prod 密墙(≥0.90) ⇒ TRANSFER；红线(≥0.70) ⇒ STOP；不可用 ⇒ PROD_UNAVAILABLE
   （本轮 imb5 实证：三颗 near prod 0.967–0.973，梯度跑完才查；前置可省 ~70 臂）
"""
import json

import pytest

from tools.gates.gradient_stop_gate import (
    PROD_DENSE_WALL,
    judge_l1_range,
    judge_prod_precheck,
    judge_three_point,
    judge_to_band,
    lint_expression,
    main,
)


def _rows(spec):
    return [
        {
            "idx": i,
            "label": a,
            "S": s,
            "F": f,
            "Y2": y,
            "TO": t,
            "sub": sb,
            "RA": ra,
        }
        for i, (a, s, f, y, t, sb, ra) in enumerate(spec)
    ]


# insiders N1 L1 干净批（10 臂，实读）
N1 = [
    ("78YPZY2x", 0.68, 0.28, 1.12, 0.578, 0.59, 4),
    ("N1PEQPGw", 0.66, 0.27, 0.94, 0.582, 0.62, 4),
    ("E5QnvQML", 0.54, 0.19, 0.65, 0.588, 0.43, 4),
    ("6XM6rM2L", 0.50, 0.22, 1.27, 0.042, 0.53, 3),
    ("rK7a57M1", 0.44, 0.19, 0.81, 0.071, 0.43, 3),
    ("e7aM9aPl", 0.41, 0.14, 0.82, 0.565, 0.26, 4),
    ("d5aJOa6j", 0.40, 0.20, 1.38, 0.078, 0.52, 3),
    ("rK7a57n9", 0.40, 0.19, 1.05, 0.127, 0.44, 4),
    ("zqd7YdEO", 0.26, 0.10, 1.13, 0.066, 0.46, 3),
    ("j2ak3aJW", -0.01, 0.00, -0.33, 0.205, -0.56, 5),
]

# insiders N2 L1（10 臂，实读）—— 极差 0.93，是「值得继续」的对照
N2 = [
    ("QP0RvKbw", 0.77, 0.39, 1.28, 0.547, 0.71, 4),
    ("O0WdA8Jd", 0.42, 0.14, 0.93, 0.592, 0.46, 4),
    ("88NWRPlX", 0.41, 0.13, 0.59, 0.593, 0.45, 4),
    ("N1PENVVg", 0.37, 0.11, 0.79, 0.593, 0.45, 4),
    ("XgaZ9JR1", 0.28, 0.11, 0.56, 0.064, 0.41, 3),
    ("QP0RvK3W", 0.11, 0.03, -0.15, 0.051, 0.22, 3),
    ("O0WdA88d", 0.07, 0.02, 0.24, 0.090, 0.23, 4),
    ("YPa31Mb6", -0.03, 0.00, -0.82, 0.030, 0.29, 3),
    ("bla06ORM", -0.06, -0.01, 0.24, 0.127, 0.29, 4),
    ("E5Qn6RpG", -0.16, -0.04, -0.44, 0.018, 0.47, 3),
]


# ── D1 ────────────────────────────────────────────────────────────────────
def test_l1_range_stops_when_ceiling_low_and_range_narrow():
    """N1 实读：max_S 0.68 < 1.0 且极差 0.69 < 0.7 ⇒ STOP。"""
    r = judge_l1_range(_rows(N1))
    assert r["verdict"] == "STOP"
    assert r["max_S"] == pytest.approx(0.68, abs=1e-6)
    assert r["range"] == pytest.approx(0.69, abs=1e-6)
    assert r["max_by"] == "78YPZY2x"


def test_l1_range_continues_when_range_wide():
    """N2 实读：极差 0.93 ⇒ 仍有信息可挖，必须 CONTINUE（不许误杀）。"""
    r = judge_l1_range(_rows(N2))
    assert r["verdict"] == "CONTINUE"
    assert r["range"] == pytest.approx(0.93, abs=1e-6)
    assert r["max_by"] == "QP0RvKbw"


def test_l1_range_continues_when_max_s_high():
    """max_S ≥ 1.0 时即使极差窄也继续（天花板够高就别停）。"""
    rows = _rows(
        [
            ("a", 1.20, 1.0, 1.6, 0.15, 0.8, 0),
            ("b", 1.10, 0.9, 1.5, 0.16, 0.7, 1),
        ]
    )
    assert judge_l1_range(rows)["verdict"] == "CONTINUE"


def test_l1_range_no_data():
    assert judge_l1_range([])["verdict"] == "NO_DATA"


# ── D2 ────────────────────────────────────────────────────────────────────
def test_to_band_flags_out_of_band_high_s():
    """N1 的 0.68 来自 TO 57.8% 的臂 ⇒ 必须点名「不可交易」，带内最佳只有 0.44。"""
    r = judge_to_band(_rows(N1))
    assert r["verdict"] == "READY_TO_JUDGE"
    assert r["best_out_of_band"]["label"] == "78YPZY2x"
    assert r["best_out_of_band"]["S"] == pytest.approx(0.68, abs=1e-6)
    assert r["best_out_of_band"]["TO"] > 0.20
    assert r["best_in_band"]["label"] == "rK7a57M1"
    assert r["best_in_band"]["S"] == pytest.approx(0.44, abs=1e-6)
    assert 0.05 <= r["best_in_band"]["TO"] <= 0.20


def test_to_band_requires_tuning_when_all_out():
    rows = _rows(
        [
            ("a", 0.9, 0.5, 1.0, 0.55, 0.4, 4),
            ("b", 0.8, 0.4, 0.9, 0.60, 0.3, 4),
        ]
    )
    r = judge_to_band(rows)
    assert r["verdict"] == "TO_FIRST"
    assert r["best_in_band"] is None


# ── D3 ────────────────────────────────────────────────────────────────────
def test_three_point_swing_when_champions_differ():
    """N1：best S 在 78YPZY2x，best 2Y 在 d5aJOa6j ⇒ SWING。"""
    r = judge_three_point(_rows(N1))
    assert r["verdict"] == "SWING"
    assert r["best_S"]["label"] == "78YPZY2x"
    assert r["best_2Y"]["label"] == "d5aJOa6j"


def test_three_point_coincide():
    rows = _rows(
        [
            ("win", 1.7, 1.2, 1.9, 0.12, 0.9, 0),
            ("x", 1.1, 0.8, 1.2, 0.15, 0.6, 3),
            ("y", 0.9, 0.6, 1.0, 0.18, 0.5, 4),
        ]
    )
    assert judge_three_point(rows)["verdict"] == "COINCIDE"


# ── D4 ────────────────────────────────────────────────────────────────────
def test_lint_catches_bare_constant_units_trap():
    """本轮实测：`add(字段, 0.0001)` ⇒ 平台 UNITS WARNING ⇒ 10/10 臂作废。"""
    iss = lint_expression("group_rank(divide(total_buy_shares,add(avg_buy_shares,0.0001)),sector)")
    assert [i["code"] for i in iss] == ["BARE_CONSTANT_UNITS"]


def test_lint_catches_zscore_on_standardized_field():
    """本轮实测：ts_zscore(directional_indicator,252) ⇒ TO 0.00 / S 0.00。"""
    iss = lint_expression("group_rank(ts_zscore(directional_indicator,252),sector)")
    assert [i["code"] for i in iss] == ["ZSCORE_ON_STANDARDIZED"]


def test_lint_catches_unreduced_vector():
    iss = lint_expression(
        "group_rank(ts_zscore(rsk60_offer,252),sector)",
        field_types={"rsk60_offer": "VECTOR"},
    )
    assert "VECTOR_NOT_REDUCED" in [i["code"] for i in iss]


def test_lint_passes_clean_expression():
    assert lint_expression("group_rank(divide(total_buy_shares,avg_buy_shares),sector)") == []
    assert (
        lint_expression(
            "group_rank(ts_zscore(vec_avg(rsk60_offer),252),sector)",
            field_types={"rsk60_offer": "VECTOR"},
        )
        == []
    )


def test_lint_does_not_flag_field_to_field_comparison():
    """字段对字段比较（代替 `> 1`）不属于裸常数坑。"""
    assert (
        lint_expression(
            "trade_when(greater(total_buy_shares,avg_buy_shares),directional_indicator,-1)"
        )
        == []
    )


# ── CLI 退出码 ────────────────────────────────────────────────────────────
def test_cli_exit_codes(tmp_path, capsys):
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"results": [{"alpha_id": a, "sharpe": s, "fitness": f,
                                          "two_year_sharpe": y, "turnover": t,
                                          "sub_universe_sharpe": sb,
                                          "failed_ra_count": ra}
                                         for a, s, f, y, t, sb, ra in N1]}), encoding="utf-8")
    assert main(["--metrics", str(m), "--all"]) == 2  # STOP + SWING ⇒ 阻断

    e = tmp_path / "e.txt"
    e.write_text("group_rank(divide(total_buy_shares,avg_buy_shares),sector)\n", encoding="utf-8")
    assert main(["--lint-expr", str(e)]) == 0  # 干净 ⇒ 放行
    capsys.readouterr()


# ── 杠杆登记表（优化 #2 落地）────────────────────────────────────────────
def test_nonportable_lever_registry_keeps_kernel_fingerprints():
    """每条跨核杠杆结论必须带「核指纹」，否则就是不可核对的结论（优化 #2）。"""
    from wqb.config import GRADIENT_NONPORTABLE_LEVERS as T

    assert set(T) >= {"signed_power_2", "ts_mean_smoothing", "raise_decay", "lower_truncation"}
    for lever, buckets in T.items():
        assert buckets, f"{lever} 空登记"
        for bucket, rec in buckets.items():
            assert "kernel" in rec, f"{lever}.{bucket} 缺核指纹"
            assert rec["kernel"].strip(), f"{lever}.{bucket} 核指纹为空"
            assert "delta" in rec, f"{lever}.{bucket} 缺 Δ 读数"


def test_noop_laws_cover_this_round_findings():
    """本轮新增的四条 no-op / 结构型死因必须在册（否则下轮会重踩）。"""
    from wqb.config import GRADIENT_NOOP_LAWS as L

    for key in (
        "zscore_on_already_standardized_field",
        "signed_power_on_positive_rank_shell",
        "decay_noop_when_turnover_already_low",
        "group_aggregator_always_collapses",
    ):
        assert key in L and L[key].strip(), f"缺 no-op 律 {key}"


# ── D5 prod 前置闸（优化 #2：prod 前置到 S/2Y 探针同批之后）──────────────
def _prod(max_corr, **kw):
    blk = {"max_correlation": max_corr}
    blk.update(kw)
    return {"checks": {"production": blk}}


def test_d5_dense_wall_transfers():
    """prod ≥ 0.90 是密墙：同集换骨架无效（imb5 三颗 0.967/0.967/0.973 实证）。"""
    r = judge_prod_precheck(_prod(0.9726))
    assert r["verdict"] == "TRANSFER"
    assert r["prod"] == 0.9726
    assert "换数据集" in r["detail"] or "换信息源" in r["detail"]


def test_d5_redline_stops():
    """0.70 ≤ prod < 0.90 ⇒ STOP（不投更深梯度，但还没到密墙）。"""
    r = judge_prod_precheck(_prod(0.76))
    assert r["verdict"] == "STOP"
    assert r["threshold"] == pytest.approx(0.7)


def test_d5_clean_continues():
    """prod < 0.70 ⇒ CONTINUE（prod 侧不构成障碍）。"""
    r = judge_prod_precheck(_prod(0.55))
    assert r["verdict"] == "CONTINUE"


def test_d5_pending_is_unavailable_not_pass():
    """pending/busy 时必须 PROD_UNAVAILABLE（不可判闸），绝不能当 pass。"""
    r = judge_prod_precheck({"status": "pending", "checks": {"production": {"status": "pending"}}})
    assert r["verdict"] == "PROD_UNAVAILABLE"
    assert "refresh=True" in r["detail"]


def test_d5_preread_not_usable():
    """预读值(provisional)只许证伪不许放行 ⇒ 判 PROD_UNAVAILABLE 除非已证伪。"""
    r = judge_prod_precheck(_prod(0.60, provisional=True))
    assert r["verdict"] == "PROD_UNAVAILABLE"
    # 但预读值若已 ≥ 阈值（证伪方向），必须能 STOP/TRANSFER —— 不能因来源差就放过
    r2 = judge_prod_precheck(_prod(0.95, provisional=True))
    assert r2["verdict"] == "TRANSFER"


def test_d5_cli_blocks_on_transfer(tmp_path, capsys):
    p = tmp_path / "prod.json"
    p.write_text(json.dumps(_prod(0.9726)), encoding="utf-8")
    assert main(["--prod", str(p)]) == 2
    out = capsys.readouterr().out
    assert "TRANSFER" in out


def test_d5_cli_passes_when_clean(tmp_path, capsys):
    p = tmp_path / "prod.json"
    p.write_text(json.dumps(_prod(0.42)), encoding="utf-8")
    assert main(["--prod", str(p)]) == 0
    capsys.readouterr()


def test_d5_dense_wall_constant_is_090():
    assert PROD_DENSE_WALL == 0.90
