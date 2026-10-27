# -*- coding: utf-8 -*-
"""闸5 分母位假阳性回归测试（2026-10-27，P0-P4）。

背景（真实误伤形态）：
  闸5「等权混腿」判据是「`add` 的顶层实参里 ≥2 个是信号腿」。但**分母位**的 `add` 不是混腿 ——
  `(a-b)/(a+b)` 是**同一个信号**的归一化，分母的作用是缩放，不是第二条腿。旧实现不看位置，
  于是这类财务比率写法（净额 / 总额、`(CFO-NI)/(CFO+NI)` 之类）全被判成毒化。
  实测这些式子在 4 份区域参考文档里被写成「可用的归一化模板」，却被自己的闸拦下。

修法（详见 `reports/codebase_governance_review_20261027.md` §4-P0-P4）：
  两个检测器判之前先 `_mask_denominators()` —— 分母位（中缀 `/` 的右操作数、`divide(x,D)` 的第二实参，
  引号内的 `/` 如 `range="0,1,0.1"` 不算）内容替换成常量 `0`，于是 `add(...)` 在分母里不再被当作腿。
  **价差收集仍走原式**（否则 `subtract(a,b)/(a+b)` 的价差判定会被一并 mask 掉）。

  窄修口径：`divide(a, add(rank(b), rank(c)))` 这种「分母里真的是两条腿」的式子也放行 ——
  分母不参与方向，拦它没有经济含义；真混腿在**分子/外层**照样拦（本文件最后一组用例守这条）。

本文件把报告 §4-P0-P4 的验收表固化成回归：误伤必须消失、真违规不得回退。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
GATE = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts" / "gate.py"
PC = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json"

_GATE_MOD = None


def _load_gate():
    """按文件路径加载 gate.py（同 `test_gate_equal_weight_leg_add.py` 的取法，只加载一次）。"""
    global _GATE_MOD
    if _GATE_MOD is not None:
        return _GATE_MOD
    spec = importlib.util.spec_from_file_location("_gate_denom", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_gate_denom"] = mod
    try:
        spec.loader.exec_module(mod)
    except SystemExit:  # 顶层可能有 CLI 守卫
        pass
    _GATE_MOD = mod
    return mod


def _pc() -> dict:
    return json.loads(PC.read_text(encoding="utf-8"))


def _blocked(expr: str) -> bool:
    """走 `check_one` 全链路（不只单测检测器），返回是否被闸5 判毒。"""
    g = _load_gate()
    pc = _pc()
    fields = ["aaa1", "bbb1", "ccc1"]
    wl = (set(fields), "MATRIX", {f: "MATRIX" for f in fields}, [])
    item = g.check_one(expr, wl, "D1", list(pc["poison_patterns"]), {**pc, "_region": "USA"})
    return any(i.startswith("[POISON:") for i in item["issues"])


@pytest.mark.parametrize("expr,why", [
    ("divide(subtract(aaa1,bbb1), add(aaa1,bbb1))", "(a-b)/(a+b) 函数式"),
    ("(aaa1 - bbb1) / (aaa1 + bbb1)", "(a-b)/(a+b) 中缀"),
    ("divide(subtract(aaa1,bbb1), add(ts_mean(aaa1,20), ts_mean(bbb1,20)))", "分母带窗口"),
    ("ts_rank(divide(subtract(aaa1,bbb1), add(add(aaa1,bbb1),1)),66)", "嵌套 + eps"),
    ("divide(aaa1, add(rank(bbb1), rank(ccc1)))", "分母位两条 rank（窄修口径）"),
    ("aaa1 / (rank(bbb1) + rank(ccc1))", "同上中缀写法"),
    ("subtract(aaa1,bbb1) / add(ccc1, 1)", "净额 / (总额+1)"),
    ("(aaa1 - bbb1) / (ccc1 + 1)", "同上中缀"),
    ("divide(ts_delta(aaa1,66), add(abs(ts_mean(aaa1,252)), 0.05))", "epsilon 分母（既有放行，不得回退）"),
])
def test_denominator_position_is_not_a_signal_leg(expr, why):
    """分母位的 `add` 不是第二条信号腿：不得判毒（旧实现全部误伤）。"""
    assert not _blocked(expr), f"分母位被误判为混腿（{why}）: {expr}"


@pytest.mark.parametrize("expr,why", [
    ("divide(add(rank(aaa1),rank(bbb1)), 2)", "分子位混腿照样拦"),
    ("add(rank(aaa1),rank(bbb1))", "裸 add 照样拦"),
    ("rank(aaa1) + rank(bbb1)", "中缀等权仍拦"),
    ("group_rank(rank(aaa1)*0.6 + rank(bbb1)*0.4, industry)", "嵌套加权中缀仍拦"),
    ("ts_decay_linear(add(ts_mean(aaa1,22), ts_mean(bbb1,66)), 5)", "窗口不同也算两条腿"),
    ("divide(add(rank(aaa1),rank(bbb1)), add(ccc1,1))", "分子混腿 + 分母归一化：仍拦"),
])
def test_real_multi_leg_add_still_blocked(expr, why):
    """真混腿不得因分母位放行而漏过（防止修复方向反掉）。"""
    assert _blocked(expr), f"真混腿漏过闸5（{why}）: {expr}"


@pytest.mark.parametrize("expr", [
    "rank(aaa1) * rank(bbb1)",
    "divide(rank(aaa1), rank(bbb1))",
    "multiply(0.5, rank(aaa1))",
    "add(ts_mean(aaa1, 22), ts_mean(aaa1, 66))",
])
def test_compliant_forms_unaffected(expr):
    """既有放行形态不受本次改动影响。"""
    assert not _blocked(expr), f"合规式被误拦: {expr}"


def test_masking_is_what_makes_the_difference(monkeypatch):
    """变异反查：把掩码换成恒等函数，`(a-b)/(a+b)` 必须重新被判毒。

    没有这一条，第一组用例在「掩码被删掉但 `_is_signal_leg` 恰好改松」时仍会绿 ——
    绿的来源不可辨。`check_one` 是纯函数（不走逐条缓存），所以替换立即生效。
    """
    g = _load_gate()
    expr = "divide(subtract(aaa1,bbb1), add(aaa1,bbb1))"
    assert not _blocked(expr), "前置不成立：带掩码时应放行"
    monkeypatch.setattr(g, "_mask_denominators", lambda s: s, raising=True)
    assert _blocked(expr), "掩码失效后仍放行：本组用例没有真正验证分母位修复"


def test_gate_code_version_covers_denominator_change():
    """判定逻辑改了就必须 bump `GATE_CODE_VERSION`，否则逐条缓存会给出旧结论。

    取「不早于」而非等值：以后再 bump 不该让本用例变红。
    """
    g = _load_gate()
    date_part, _, seq = str(g.GATE_CODE_VERSION).partition(".")
    y, m, d = (int(x) for x in date_part.split("-"))
    assert (y, m, d, int(seq or 0)) >= (2026, 10, 27, 1), (
        f"GATE_CODE_VERSION 未随分母位修复更新（现为 {g.GATE_CODE_VERSION}）")


def test_denominator_helpers_exist():
    """分母位掩码是本次修复的实现载体：被改名/删除要让签名层先红，而不是静默失效。"""
    g = _load_gate()
    for name in ("_paren_close", "_operand_span", "_top_level_arg_spans",
                 "_denominator_spans", "_mask_denominators"):
        assert callable(getattr(g, name, None)), f"gate.py 缺少 {name}（分母位掩码实现被移动/删除）"
