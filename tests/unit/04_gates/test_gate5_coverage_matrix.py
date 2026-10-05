# -*- coding: utf-8 -*-
"""闸5 覆盖矩阵（skills 审查 X-3 / T0-10，2026-09-29）：同一数学结构，写法不同判定不得相反。

政策（用户 2026-09-13 路线 A / 2026-09-28 定案）：**禁止把两条及以上独立信号腿按任意（等/非等）权重
线性相加——无论函数式 add(...)、multiply 函数式，还是中缀 `+`；权重在左、在右、还是没有。**
唯一豁免：价差 subtract(A,B) / A-B——须两腿同源（同一组字段 / 同一数据集）且有单一经济含义
（platform_constraints.spread_signal_ruling，用户 2026-09-28 裁定）。

矩阵维度：形态（函数式 / 中缀）× 权重位置（左 / 右 / 无）× 运算（add / 加号 / 减号 / subtract）。
期望值写在测试里：以后改闸 5 必须同时改这里（不是改完没人发现）。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TK = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
GATE = TK / "scripts" / "gate.py"
PC = TK / "config" / "platform_constraints.json"


@pytest.fixture(scope="module")
def g():
    for p in (str(REPO / "src"), str(GATE.parent)):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location("_gate_matrix_test", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_gate_matrix_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def _pc():
    pc = json.loads(PC.read_text(encoding="utf-8"))
    pc["_region"] = "USA"
    return pc


def _check(g, expr, fields=("aaa1", "bbb1", "ccc1"), field_dataset=None):
    pc = _pc()
    if field_dataset:
        pc["_field_dataset"] = field_dataset
    wl = (set(fields), "MATRIX", {f: "MATRIX" for f in fields}, [])
    return g.check_one(expr, wl, "D1", list(pc["poison_patterns"]), pc)


def _poison(item):
    return sorted({i.split("]")[0][len("[POISON:"):] for i in item["issues"] if i.startswith("[POISON:")})


def _blocked(g, expr, **kw):
    return bool(_poison(_check(g, expr, **kw)))


# 每行：(表达式, 是否应被闸5 拦, 说明)
MATRIX = [
    # —— 函数式 add / multiply ——
    ("add(0.6*rank(aaa1), 0.4*rank(bbb1))", True, "add + 系数在左"),
    ("add(multiply(rank(aaa1),0.6), multiply(rank(bbb1),0.4))", True, "add + multiply 权重在右"),
    ("add(rank(aaa1), rank(bbb1))", True, "add 等权"),
    ("add(rank(aaa1), -rank(bbb1))", True, "add 镜像腿（≡ 价差，但 add 一律违规：用户裁定）"),
    # —— 中缀加号（此前全部放行的洞）——
    ("0.6*rank(aaa1) + 0.4*rank(bbb1)", True, "中缀 + 权重在左"),
    ("rank(aaa1)*0.6 + rank(bbb1)*0.4", True, "中缀 + 权重在右（此前放行）"),
    ("rank(aaa1) + rank(bbb1)", True, "中缀 + 等权（此前放行）"),
    ("scale(rank(aaa1)) + scale(-rank(bbb1)) * 0.35", True, "V9 顶层形态（此前放行）"),
    ("rank(aaa1) - rank(bbb1) + rank(ccc1)", True, "价差再加第三腿"),
    ("-rank(aaa1) - rank(bbb1)", True, "两负腿 = -(A+B)"),
    ("rank(aaa1) + rank(bbb1) + rank(ccc1)", True, "链式三腿"),
    ("group_rank(rank(aaa1)*0.6 + rank(bbb1)*0.4, industry)", True, "嵌套在 group_rank 内"),
    ("ts_decay_linear(rank(aaa1) + rank(bbb1), 22)", True, "嵌套在 ts_decay_linear 内"),
    ("ts_decay_linear(aaa1,5)*rank(bbb1*ccc1) + ts_decay_linear(aaa1,10)*(1-rank(bbb1*ccc1))", True,
     "HP-05 的流动/非流动 decay 相加（rank 加权的两腿混合）"),
    # —— 价差：合规（同源 + 有经济含义；单数据集批天然同源）——
    ("subtract(rank(aaa1), rank(bbb1))", False, "函数式价差"),
    ("rank(aaa1) - rank(bbb1)", False, "中缀价差（≡ subtract）"),
    ("group_rank(subtract(ts_rank(aaa1,252), ts_rank(bbb1,252)), industry)", False, "价差外包单信号几何"),
    ("trade_when(greater(ccc1,0), rank(aaa1) - rank(bbb1), -1)", False, "价差 + 事件门控"),
    # —— 单信号 / 标量 / 同形态多窗 / 乘积交互 ——
    ("abs(aaa1) + 0.01", False, "1 腿 + epsilon"),
    ("divide(ts_delta(aaa1,66), add(abs(ts_mean(aaa1,252)), 0.05))", False, "epsilon 分母"),
    ("ts_mean(aaa1,22) + ts_mean(aaa1,66)", False, "同形态仅窗口不同 = 单信号多窗平滑"),
    ("add(ts_mean(aaa1,22), ts_mean(aaa1,66))", False, "同上（函数式）"),
    ("rank(aaa1) * 0.5", False, "单腿缩放"),
    ("rank(aaa1) * rank(bbb1)", False, "乘积交互（非加和）"),
    ("rank(aaa1) - 1e-3", False, "科学计数法标量"),
    ("winsorize(rank(aaa1) - rank(bbb1), std=4)", False, "价差 + 命名参数"),
    ("(rank(aaa1) > 0 ? rank(bbb1) - rank(ccc1) : 0)", False, "三元式内不切项（宁可漏判不可误伤）"),
]


@pytest.mark.parametrize("expr,blocked,why", MATRIX, ids=[m[2] for m in MATRIX])
def test_gate5_matrix(g, expr, blocked, why):
    got = _blocked(g, expr)
    assert got == blocked, f"{why}: {expr} → 闸5 {'拦' if got else '放'}，期望 {'拦' if blocked else '放'}"


def test_same_math_different_syntax_is_not_judged_oppositely(g):
    """核心不变量：同一加和结构（+ 号 / add()），无论写法都判同一结果。"""
    trios = [
        ("add(rank(aaa1), rank(bbb1))", "rank(aaa1) + rank(bbb1)"),
        ("add(multiply(0.6,rank(aaa1)), multiply(0.4,rank(bbb1)))", "rank(aaa1)*0.6 + rank(bbb1)*0.4"),
        ("add(abs(aaa1), 0.01)", "abs(aaa1) + 0.01"),
        ("add(ts_mean(aaa1,22), ts_mean(aaa1,66))", "ts_mean(aaa1,22) + ts_mean(aaa1,66)"),
    ]
    for func_form, infix_form in trios:
        assert _blocked(g, func_form) == _blocked(g, infix_form), (func_form, infix_form)


def test_subtract_and_infix_minus_are_the_same_spread(g):
    assert _blocked(g, "subtract(rank(aaa1), rank(bbb1))") == _blocked(g, "rank(aaa1) - rank(bbb1)") is False


# ── 价差规则（用户 2026-09-28 裁定 + 2026-10-01 修正）──────────────────────────
FD = {"aaa1": "D1", "aaa2": "D1", "bbb1": "D2"}


def test_cross_dataset_spread_blocked_only_when_undeclared(g):
    """2026-10-01 用户修正：跨集本身不是违规判据；判据 = 跨集 且 未声明经济含义。"""
    expr = "subtract(rank(aaa1), rank(bbb1))"
    # 未声明 → 拦
    item = _check(g, expr, fields=("aaa1", "aaa2", "bbb1"), field_dataset=FD)
    assert _poison(item) == ["spread_cross_dataset"]
    # 中缀减号同判
    assert _poison(_check(g, "rank(aaa1) - rank(bbb1)", fields=("aaa1", "bbb1"), field_dataset=FD)) == [
        "spread_cross_dataset"]
    # 同源（同一数据集）放行；单数据集批（无映射）放行
    assert _poison(_check(g, "subtract(rank(aaa1), rank(aaa2))", fields=("aaa1", "aaa2"), field_dataset=FD)) == []
    assert _poison(_check(g, expr, fields=("aaa1", "bbb1"))) == []


def test_declared_cross_spread_pair_is_allowed(g):
    """已声明 (D1,D2) 经济含义 → 跨集价差放行（用户 2026-10-01 澄清：合规且鼓励）。"""
    expr = "subtract(rank(aaa1), rank(bbb1))"
    pc = _pc()
    pc["_field_dataset"] = FD
    pc["_declared_spread_pairs"] = [["D1", "D2"]]
    wl = ({"aaa1", "aaa2", "bbb1"}, "MATRIX", {f: "MATRIX" for f in ("aaa1", "aaa2", "bbb1")}, [])
    item = g.check_one(expr, wl, "D1", list(pc["poison_patterns"]), pc)
    assert _poison(item) == [], "已声明的跨集价差应放行"
    # 顺序无关
    pc["_declared_spread_pairs"] = [["D2", "D1"]]
    item2 = g.check_one(expr, wl, "D1", list(pc["poison_patterns"]), pc)
    assert _poison(item2) == []
    # 声明了别的集对 → 仍拦
    pc["_declared_spread_pairs"] = [["D1", "D9"]]
    item3 = g.check_one(expr, wl, "D1", list(pc["poison_patterns"]), pc)
    assert _poison(item3) == ["spread_cross_dataset"]


def test_declared_cross_spread_does_not_whitelist_add(g):
    """声明只豁免 subtract 价差，绝不豁免 add 混腿（用户铁律）。"""
    pc = _pc()
    pc["_field_dataset"] = FD
    pc["_declared_spread_pairs"] = [["D1", "D2"]]
    wl = ({"aaa1", "bbb1"}, "MATRIX", {f: "MATRIX" for f in ("aaa1", "bbb1")}, [])
    item = g.check_one("add(rank(aaa1), rank(bbb1))", wl, "D1", list(pc["poison_patterns"]), pc)
    assert "equal_weight_leg_add" in _poison(item) or "infix_leg_sum" in _poison(item)


def test_weighted_spread_only_warns(g):
    item = _check(g, "subtract(multiply(0.6, rank(aaa1)), rank(bbb1))")
    assert _poison(item) == []
    assert any(w.startswith("[SPREAD_WEIGHTED]") for w in item["warnings"])
    item2 = _check(g, "0.6*rank(aaa1) - 0.4*rank(bbb1)")
    assert any(w.startswith("[SPREAD_WEIGHTED]") for w in item2["warnings"])
    # 无系数价差不告警
    assert not any(w.startswith("[SPREAD_WEIGHTED]") for w in _check(g, "rank(aaa1) - rank(bbb1)")["warnings"])


# ── 配置与缓存 ────────────────────────────────────────────────────────────────
def test_new_poison_entries_registered_in_single_source():
    pc = json.loads(PC.read_text(encoding="utf-8"))
    by_name = {p["name"]: p for p in pc["poison_patterns"]}
    for name in ("infix_leg_sum", "spread_cross_dataset"):
        assert name in by_name, f"platform_constraints 缺 {name}"
        assert by_name[name]["severity"] == "block" and by_name[name].get("_structural") is True
    assert "spread_signal_ruling" in pc          # 用户裁定原文仍在
    assert "spread_cross_dataset" in by_name["equal_weight_leg_add"]["rule"]   # 合规替代与拦截项互相指引


def test_gate_signature_tracks_detector_code_version(g, monkeypatch):
    pc = _pc()
    wl = ({"aaa1"}, "MATRIX", {"aaa1": "MATRIX"}, [])
    a = g.gate_signature(["D1"], wl, list(pc["poison_patterns"]), pc)
    monkeypatch.setattr(g, "GATE_CODE_VERSION", "bumped-for-test")
    b = g.gate_signature(["D1"], wl, list(pc["poison_patterns"]), pc)
    assert a != b, "判定器代码变更必须让逐条缓存失效（GATE_CODE_VERSION 入签名）"
