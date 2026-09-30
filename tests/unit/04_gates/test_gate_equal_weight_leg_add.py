# -*- coding: utf-8 -*-
"""闸5「等权混腿」毒模式回归测试（2026-09-28 新增，纪律红线）。

背景（真实违规 + 闸门漏洞）：
  全局纪律：**不得把两条独立信号腿加权相加，无论写成 add(multiply(0.4,...)) 还是 0.4A+0.6B**。
  但既有 `_detect_weighted_mix_structural` 只拦「实参以 系数* 开头」的腿，
  **明文豁免等权 `add(rank(a), rank(b))`** → 等权即 0.5A+0.5B，属同一违规族。

  实证代价：KOR wave189/190 共 **7 条** `add(group_rank(腿A), group_rank(腿B))`
  （含 S=2.11 / F=1.80 / 2Y=1.89 的漂亮结果）全部漏过闸5，已全部作废。

本测试守护：等权双腿形态必须被拦；合规形态（价差/门控/epsilon/同形态多窗）必须放行。
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


def _load_gate():
    spec = importlib.util.spec_from_file_location("_gate_poison", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_gate_poison"] = mod
    try:
        spec.loader.exec_module(mod)
    except SystemExit:  # gate.py 顶层可能有 sys.exit 守卫
        pass
    return mod


def _non_field():
    pc = json.loads(PC.read_text(encoding="utf-8"))
    return (set(pc["known_ops"]) | set(pc["group_identifiers"])
            | set(pc["driver_args"]) | set(pc.get("kw_args") or []))


def _blocked(g, expr):
    return (g._detect_equal_weight_leg_add(expr, _non_field())
            or g._detect_weighted_mix_structural(expr))


_T1 = "subtract(ts_rank(divide(subtract(aaa1, bbb1), ccc1), 252), ts_rank(divide(bbb1, ccc1), 252))"
_T2 = "subtract(divide(subtract(aaa1, bbb1), ccc1), divide(bbb1, ccc1))"


@pytest.mark.parametrize("expr", [
    # 真实违规式（KOR wave189 的 2rwoAp8b / wave190 的 6 条同构）
    f"add(group_rank({_T1}, industry), group_rank({_T2}, industry))",
    f"add(group_rank({_T1}, sector), group_rank({_T2}, industry))",
    f"ts_decay_linear(add(group_rank({_T1}, industry), group_rank({_T2}, industry)), 22)",
    f"group_rank(add(group_rank({_T1}, industry), group_rank({_T2}, industry)), industry)",
    f"winsorize(add(group_rank({_T1}, industry), group_rank({_T2}, industry)), std=4)",
    # 加权形态（既有判定已覆盖，此处确保不回归）
    "add(multiply(0.4, rank(aaa1)), multiply(0.6, rank(bbb1)))",
    "add(multiply(0.5, group_rank(aaa1, industry)), group_rank(bbb1, sector))",
])
def test_equal_weight_multi_leg_add_is_blocked(expr):
    """两条独立信号腿相加（等权或加权）必须被闸5 拦截。"""
    assert _blocked(_load_gate(), expr), f"混腿未被拦截（闸门漏洞）: {expr}"


@pytest.mark.parametrize("expr", [
    # 价差（单一信号，规则允许）
    f"group_rank({_T1}, industry)",
    f"subtract(group_rank({_T1}, industry), group_rank({_T2}, industry))",
    # 事件门控
    f"trade_when(greater(ccc1, 0), {_T1}, -1)",
    f"if_else(greater(ccc1, 0), {_T2}, reverse({_T2}))",
    # epsilon 分母（1 腿 + 标量）
    "divide(ts_delta(aaa1, 66), add(abs(ts_mean(aaa1, 252)), 0.05))",
    # 同形态仅窗口不同 = 单信号多窗平滑
    "add(ts_mean(aaa1, 22), ts_mean(aaa1, 66))",
    # 单腿缩放
    "multiply(0.5, rank(aaa1))",
])
def test_compliant_forms_are_not_blocked(expr):
    """合规形态不得被误伤（误伤会把合规做法一起禁掉）。"""
    assert not _blocked(_load_gate(), expr), f"合规式被误拦: {expr}"


def test_poison_entry_documented_in_config():
    """新毒模式必须登记在单一事实源 config，且 rule 写明'等权同属违规'与合规替代。"""
    pc = json.loads(PC.read_text(encoding="utf-8"))
    names = {p.get("name") for p in pc["poison_patterns"]}
    assert "equal_weight_leg_add" in names, "config 缺 equal_weight_leg_add 条目"
    entry = next(p for p in pc["poison_patterns"] if p.get("name") == "equal_weight_leg_add")
    assert entry.get("severity") == "block"
    rule = entry["rule"]
    rule_ns = rule.replace(" ", "")  # 归一空格：config 写的是 subtract(rank(A),rank(B))
    for kw in ("等权", "0.4A+0.6B", "任何含混表述不构成本例外的例外"):
        assert kw in rule, f"rule 需写明: {kw}"
    for kw in ("ts_scale", "subtract(rank(A),rank(B))", "ModeB"):
        assert kw.replace(" ", "") in rule_ns, f"rule 需给出合规替代: {kw}"


def test_no_add_leg_violation_left_in_kor_waves():
    """已作废的 7 条违规式不得以未 dropped 状态残留（防线：DB 实况）。"""
    import sqlite3
    db = REPO / "data" / "wqb.db"
    if not db.exists():
        pytest.skip("no db")
    bad_ids = {"2rwoAp8b", "QPbp025Q", "LLNYKgk2", "levPaQQO",
               "58zdJaMN", "xA3pvPPb", "78NRYd3b"}
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        rows = c.execute(
            "SELECT b.alpha_id, COALESCE(e.status,'(no expr)') FROM backtest_results b "
            "LEFT JOIN expressions e ON e.expression=b.code "
            "WHERE b.alpha_id IN (%s) AND COALESCE(e.status,'') != 'dropped'"
            % ",".join("?" * len(bad_ids)), tuple(bad_ids)).fetchall()
    finally:
        c.close()
    assert not rows, f"违规式未被作废/未落 dropped: {rows}"


def test_spread_signal_ruling_documented():
    """用户 2026-09-28 对「单信号价差 vs 拼腿」的裁定必须登记在单一事实源。

    没有这条守卫，后续会话极易把合规的 subtract(rank(A),rank(B)) 价差误判为拼腿而误杀，
    或反过来把不同概念的拼腿当作价差放行。
    """
    pc = json.loads(PC.read_text(encoding="utf-8"))
    r = pc.get("spread_signal_ruling")
    assert r, "config 缺 spread_signal_ruling（用户裁定）"
    text = json.dumps(r, ensure_ascii=False)
    for kw in ("同源", "经济含义", "拼腿", "add 一律违规"):
        assert kw in text, f"裁定需写明判据: {kw}"
    ids = {c.get("alpha") for c in r.get("confirmed_cases", [])}
    for aid in ("3qXvopQO", "npd5AZj8", "kqo6J1pK"):
        assert aid in ids, f"裁定需含已确认案例 {aid}"


def test_confirmed_compliant_alphas_pass_gate():
    """被裁定为合规的 3 颗，必须能通过（新）闸5 —— 防误杀。"""
    g = _load_gate()
    ok = [
        # 3qXvopQO：价差 + group_rank
        "group_rank(subtract(ts_rank(divide(subtract(aaa1, bbb1), ccc1), 252), "
        "ts_rank(divide(bbb1, ccc1), 252)), industry)",
        # npd5AZj8：价差 + 事件门控
        "trade_when(greater(ccc1, 0), subtract(ts_rank(divide(subtract(aaa1, bbb1), ccc1), 252), "
        "ts_rank(divide(bbb1, ccc1), 252)), -1)",
        # kqo6J1pK：价差 + 单信号平滑
        "ts_decay_linear(subtract(ts_rank(divide(subtract(aaa1, bbb1), ccc1), 252), "
        "ts_rank(divide(bbb1, ccc1), 252)), 22)",
        # 单信号几何叠加
        "ts_rank(group_rank(subtract(divide(subtract(aaa1, bbb1), ccc1), divide(bbb1, ccc1)), industry), 252)",
    ]
    for e in ok:
        assert not _blocked(g, e), f"已裁定的合规价差式被误杀: {e}"
