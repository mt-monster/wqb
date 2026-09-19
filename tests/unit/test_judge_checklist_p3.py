# -*- coding: utf-8 -*-
"""回归测试：judge 节点「三态 → 逐闸清单」（2026-09-17 P3）。

背景：`judge` 只是**参考评审层**（提交判定权威 = `tools/submit_verdict.py`），
但它返回的 `verdict` 是 READY/REVIEW/BLOCK 的**聚合结论**，极易被读成提交裁决。

本次加固（附加字段，不改既有契约）：
1. 新增 `checklist`：逐闸摊平为事实清单，让调用方据事实判断而非只看一个字；
2. 新增 `degraded_gates` + `warning`：把 `unavailable` 的闸显式列出。

第 2 点修的是一个真实 **fail-open**：`_compute_final_verdict` 只对
`platform_check` / `correlation` 的 `pass=False` 判 BLOCK，而降级的闸多数返回
`pass=True, unavailable=True`（如 correlation / trend_score）→ 全部闸取不到数时
仍会输出 `verdict=READY`，且旧返回体里**看不出任何闸缺失**。
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.workflow.nodes.judge import _compute_final_verdict, build_checklist  # noqa: E402


# ---- 复现 fail-open -------------------------------------------------------

def test_readme_verdict_ignores_unavailable_gates():
    """锁定既有语义：降级闸返回 pass=True → 聚合结论仍为 READY（故必须靠清单暴露）。"""
    gates = [
        {"gate": "platform_check", "pass": True},
        {"gate": "correlation", "pass": True, "unavailable": True},
        {"gate": "yearly_attribution", "pass": True, "negative_years": []},
        {"gate": "trend_score", "pass": True, "unavailable": True},
    ]
    assert _compute_final_verdict(gates) == "READY"  # 即 fail-open 的来源


def test_degraded_gates_are_derivable_and_nonempty():
    """降级闸必须能被机器识别出来（degraded_gates 的构造依据）。"""
    gates = [
        {"gate": "correlation", "pass": True, "unavailable": True},
        {"gate": "trend_score", "pass": True, "unavailable": True},
        {"gate": "platform_check", "pass": True},
    ]
    degraded = [g.get("gate") for g in gates if g.get("unavailable")]
    assert degraded == ["correlation", "trend_score"]


def test_hard_gate_failure_blocks():
    gates = [{"gate": "platform_check", "pass": False, "unavailable": True}]
    assert _compute_final_verdict(gates) == "BLOCK"


def test_negative_year_yields_review():
    gates = [
        {"gate": "platform_check", "pass": True},
        {"gate": "correlation", "pass": True},
        {"gate": "yearly_attribution", "pass": True, "negative_years": [2024]},
    ]
    assert _compute_final_verdict(gates) == "REVIEW"


# ---- checklist ------------------------------------------------------------

def test_checklist_puts_key_fields_first_and_keeps_scalars():
    gates = [
        {"gate": "platform_check", "pass": True, "sharpe": 1.7, "fitness": 1.2,
         "nested": {"a": 1}, "notes": "ok"},
    ]
    rows = build_checklist(gates)
    assert len(rows) == 1
    row = rows[0]
    assert list(row.keys())[:3] == ["gate", "pass", "unavailable"]
    assert row["sharpe"] == 1.7 and row["fitness"] == 1.2
    assert row["notes"] == "ok"
    assert "nested" not in row, "嵌套结构应被跳过，避免清单臃肿"


def test_checklist_normalizes_missing_pass_to_false():
    """缺 pass 字段一律视为 False —— 不得让"没有结论"看起来像"通过"。"""
    rows = build_checklist([{"gate": "correlation"}])
    assert rows[0]["pass"] is False
    assert rows[0]["unavailable"] is False


def test_checklist_exposes_unavailable_flag():
    rows = build_checklist([{"gate": "correlation", "pass": True, "unavailable": True}])
    assert rows[0]["unavailable"] is True


def test_checklist_survives_malformed_input():
    assert build_checklist([]) == []
    assert build_checklist(None) == []
    assert build_checklist(["not-a-dict", None, 42]) == []


def test_checklist_covers_every_gate():
    gates = [{"gate": f"g{i}", "pass": True} for i in range(5)]
    assert len(build_checklist(gates)) == 5


# ---- 职责边界不回归 -------------------------------------------------------

def test_judge_has_no_submit_path():
    """judge 不得重新长出提交开关（2026-09-05 已移除）。"""
    src = open(os.path.join(REPO, "src", "wqb", "workflow", "nodes", "judge.py"),
               encoding="utf-8").read()
    assert "confirm_submit" not in src
    assert "submit_verdict" in src, "应保留'权威在 submit_verdict'的指引"
