# -*- coding: utf-8 -*-
"""judge_alpha.INTERNAL_HARD_GATES 与 wqb.config 一致（skills 审查 JD-09 / JD-17）。

judge 脚本自带一份内部硬闸常量（skill 自包含，不 import wqb）；这是内部闸的第三份拷贝
（config.GATES_INTERNAL、submit_queue.LIM、此处）。脚本注释早就写着「由本测试断言」，但测试文件并不存在——
现在补上：数值漂移必红。PPA 不套 REGULAR 的 1.58 严线：平台对 PPA 只看 LOW_SHARPE value < 1（compute_webdata_failed_counts）。
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "Claude" / "skills" / "brain-alpha-judge" / "scripts" / "vendor"))

from wqb.config import GATES_INTERNAL, PLATFORM_CHECK_LINES, compute_webdata_failed_counts  # noqa: E402


def _judge():
    path = ROOT / "Claude" / "skills" / "brain-alpha-judge" / "scripts" / "judge_alpha.py"
    spec = importlib.util.spec_from_file_location("judge_alpha_gate_test", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["judge_alpha_gate_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_regular_internal_lines_equal_config():
    g = _judge().INTERNAL_HARD_GATES
    assert g["sharpe_min"] == GATES_INTERNAL["sharpe_min"]
    assert g["fitness_min"] == GATES_INTERNAL["fitness_min"]
    # 2Y 线 = 平台 LOW_2Y_SHARPE 线（1.58），不是 IS Sharpe 线（1.25）
    assert g["two_year_min"] == PLATFORM_CHECK_LINES["low_2y_sharpe_min"]


def test_ppa_sharpe_line_is_the_platform_ppa_line_not_the_regular_one():
    """PPA 的 LOW_SHARPE 只在 value < 1 时计失败：Sharpe ∈ [1.0, 1.58) 的合法 PPA 不得被内部严线判 BLOCK。"""
    judge = _judge()
    assert judge.INTERNAL_HARD_GATES["ppa_sharpe_min"] == 1.0
    ppa = {"type": "PPA", "is": {"sharpe": 1.2, "fitness": 0.5, "checks": []}}
    assert judge.internal_hard_gate_failures(ppa) == []
    regular = {"type": "REGULAR", "is": {"sharpe": 1.2, "fitness": 0.5, "checks": []}}
    names = {f["name"] for f in judge.internal_hard_gate_failures(regular)}
    assert {"LOW_SHARPE", "LOW_FITNESS"} <= names
    # 与平台口径同向：value < 1 才计 PPA 失败
    checks = [{"name": "LOW_SHARPE", "result": "PASS", "value": 0.9, "limit": 1.25}]
    counts = compute_webdata_failed_counts(checks)
    assert counts["failed_ppa"] >= 1


def test_ppa_detection_by_type_or_tag():
    judge = _judge()
    assert judge._is_ppa({"type": "PPA"}) is True
    assert judge._is_ppa({"tags": ["CH_PPA", "PowerPoolSelected"]}) is True
    assert judge._is_ppa({"type": "REGULAR", "tags": ["CH_REG"]}) is False
