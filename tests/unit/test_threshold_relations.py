# -*- coding: utf-8 -*-
"""阈值口径的**关系**守护（skills 审查 X-11，2026-09-29）：同一个词（Sharpe/Fitness/Turnover…）在仓库里
曾有 3–5 个取值（1.25 / 1.3 / 1.58；0.75 / 1.0；4–40% / 5–20% / 1–70%）。它们各有用途，但用途必须写清、
关系必须钉住——本测试把「谁比谁宽、谁等于谁」写成断言，任何一方漂移就红。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.config import GATES_INTERNAL, GATES_PLATFORM, PLATFORM_CHECK_LINES as PL  # noqa: E402
from wqb.store.submit_queue import LIM  # noqa: E402


def test_platform_lines_are_registered_per_check_name():
    assert PL["low_sharpe_min"] == {"delay1": 1.25, "delay0": 2.0}
    assert PL["low_fitness_min"] == {"delay1": 1.0, "delay0": 1.3}
    assert PL["turnover_range"] == (0.01, 0.70)
    assert PL["low_2y_sharpe_min"] == 1.58


def test_gates_platform_sharpe_is_the_2y_line_not_the_low_sharpe_line():
    """GATES_PLATFORM.sharpe_min（1.58）= 平台 2Y 线，**不是** LOW_SHARPE 线（Delay-1 为 1.25）。"""
    assert GATES_PLATFORM["sharpe_min"] == PL["low_2y_sharpe_min"] > PL["low_sharpe_min"]["delay1"]
    assert GATES_PLATFORM["fitness_min"] == PL["low_fitness_min"]["delay1"]
    assert GATES_PLATFORM["turnover_range"] == PL["turnover_range"]


def test_internal_lines_are_at_least_as_strict_as_platform_lines():
    assert GATES_INTERNAL["sharpe_min"] >= GATES_PLATFORM["sharpe_min"]
    assert GATES_INTERNAL["fitness_min"] >= GATES_PLATFORM["fitness_min"]
    lo_i, hi_i = GATES_INTERNAL["turnover_range"]
    lo_p, hi_p = GATES_PLATFORM["turnover_range"]
    assert lo_p <= lo_i and hi_i <= hi_p                     # 内部换手窗 ⊂ 平台换手窗
    assert GATES_INTERNAL["self_corr_max"] <= GATES_PLATFORM["self_corr_max"]


def test_submit_queue_lines_come_from_config():
    assert LIM["sharpe"] == GATES_PLATFORM["sharpe_min"]
    assert LIM["fitness"] == GATES_PLATFORM["fitness_min"]
    assert LIM["two_year"] == PL["low_2y_sharpe_min"]
    assert LIM["turnover_hi"] == GATES_PLATFORM["turnover_range"][1]


def _pre_submit_numbers():
    src = (ROOT / "world-quant-brain-mcp" / "brain_mixin_simulation.py").read_text(encoding="utf-8")
    body = src[src.index("def pre_submit_check"):]
    body = body[:body.index("return {", body.index("failures = []"))]
    return {
        "sharpe": float(re.search(r"if sharpe <= ([\d.]+)", body).group(1)),
        "fitness": float(re.search(r"if fitness <= ([\d.]+)", body).group(1)),
        "turn_lo": float(re.search(r"if turnover < ([\d.]+)", body).group(1)),
        "turn_hi": float(re.search(r"elif turnover > ([\d.]+)", body).group(1)),
        "returns": float(re.search(r"if returns <= ([\d.]+)", body).group(1)),
    }


def test_pre_submit_check_is_a_relaxed_local_screen_with_pinned_relations():
    """pre_submit_check 是宽松的本地预检（不是平台线、也不是内部线）；关系钉死，漂移即红。"""
    n = _pre_submit_numbers()
    assert n == {"sharpe": 1.3, "fitness": 0.75, "turn_lo": 0.04, "turn_hi": 0.40, "returns": 0.04}
    assert n["sharpe"] < GATES_INTERNAL["sharpe_min"]                     # 比内部线宽
    assert n["sharpe"] > PL["low_sharpe_min"]["delay1"]                   # 但不低于平台 LOW_SHARPE 线
    assert n["fitness"] < GATES_PLATFORM["fitness_min"]                   # 比平台 Fitness 线宽（平台在提交时复核）
    lo_i, hi_i = GATES_INTERNAL["turnover_range"]
    assert n["turn_lo"] <= lo_i and n["turn_hi"] >= hi_i                  # 换手窗 ⊇ 内部窗
    assert n["returns"] < GATES_INTERNAL["returns_min"]                   # 比内部 Returns 线宽


def test_pre_submit_docstring_states_it_is_not_the_platform_line():
    src = (ROOT / "world-quant-brain-mcp" / "brain_mixin_simulation.py").read_text(encoding="utf-8")
    doc = src[src.index("def pre_submit_check"):][:900]
    assert "NOT the platform lines" in doc and "PLATFORM_CHECK_LINES" in doc
