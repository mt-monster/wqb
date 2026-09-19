# -*- coding: utf-8 -*-
"""闸5 结构判定（weighted_signal_mix_structural）守卫测试。

背景（2026-09-17，报告 output_report/ra_pipeline_s123_optimization_20260917.md §2.1）：
既有 weighted_signal_mix 正则要求两条腿都紧跟
(rank|zscore|ts_rank|group_rank|normalize|scale)，而真实语料主流是
``add(0.4*rank(a), 0.6*subtract(0, rank(b)))`` 镜像腿 → 实测抽 220 条
真闸只 block 19%（漏 81%）。本测试锁定修复后的行为契约：

- 原漏网形态（镜像腿/嵌套 add/GEM 函数式外套）必须 BLOCK；
- 等权 add、单腿系数缩放、五类结构交互等合法形态必须放行；
- 配置条目存在且带 ``_structural`` 标记（regex 占位永假，判定在 gate 侧）。
"""
import json
import os
import re
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TK_SCRIPTS = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")
CFG = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit",
                   "config", "platform_constraints.json")


@pytest.fixture(scope="module")
def gate():
    sys.path.insert(0, TK_SCRIPTS)
    import gate  # noqa: PLC0415
    return gate


@pytest.fixture(scope="module")
def poison():
    pc = json.loads(open(CFG, encoding="utf-8").read())
    return [p for p in pc["poison_patterns"] if p.get("severity", "block") == "block"], pc


def _poison_hits(gate, poison, expr):
    pats, pc = poison
    o = gate.check_one(expr, (set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr)),
                              "MATRIX", {}, []), None, pats, pc)
    return [i for i in o["issues"] if "POISON" in i]


# ---------------------------------------------------------------------------
# 配置契约
# ---------------------------------------------------------------------------

def test_structural_entry_exists_with_marker():
    pc = json.loads(open(CFG, encoding="utf-8").read())
    entry = next((p for p in pc["poison_patterns"]
                  if p["name"] == "weighted_signal_mix_structural"), None)
    assert entry is not None, "结构判定毒模式条目缺失"
    assert entry.get("_structural") is True, "必须带 _structural 标记（判定在 gate 侧，不走 regex）"
    # regex 是占位永假——结构判定绝不依赖它
    assert not re.search(entry["regex"], "add(0.4*rank(a), 0.6*rank(b))")


# ---------------------------------------------------------------------------
# 原漏网形态必须 BLOCK（修复回归）
# ---------------------------------------------------------------------------
# 分两类：
#   ① 星号中缀 + 镜像腿 —— 旧正则的主漏网形态（81% 漏网的主体），
#      必须由**新结构判定** weighted_signal_mix_structural 拦下；
#   ② 函数式 multiply 外套 —— 由旧正则 func_prefix/suffix 负责
#      （add(multiply(0.7,…)…) 形状它本来就拦得住），只要求"被任一毒模式拦"。
MUST_BLOCK_STRUCTURAL = [
    "add(0.4*rank(close), 0.6*subtract(0, rank(returns)))",
    "add(0.4*subtract(0, rank(close)), 0.6*rank(returns))",
    "add(0.4*subtract(0, rank(close)), 0.6*subtract(0, rank(returns)))",
    # 嵌套于 rank 的中缀混合（顶层不是 add，须扫描全部 add(）
    "rank(add(0.5*ts_mean(a, 22), 0.5*ts_mean(b, 66)))",
]
MUST_BLOCK_ANY = [
    # GEM 8 月真实产出形态：函数式 multiply 权重（func_prefix 拦）
    "quantile(add(multiply(0.7, rank(fnd6_xyz)), multiply(0.3, rank(fnd7_abc))))",
]


@pytest.mark.parametrize("expr", MUST_BLOCK_STRUCTURAL)
def test_leaked_forms_now_blocked(gate, poison, expr):
    hits = _poison_hits(gate, poison, expr)
    assert any("weighted_signal_mix_structural" in h for h in hits), \
        f"镜像腿/嵌套中缀形态漏网（结构判定未命中）: {expr}"


@pytest.mark.parametrize("expr", MUST_BLOCK_ANY)
def test_functional_forms_blocked_by_any_poison(gate, poison, expr):
    hits = _poison_hits(gate, poison, expr)
    assert hits, f"函数式加权混合漏网（func_prefix/suffix 也不该漏）: {expr}"


# ---------------------------------------------------------------------------
# 合法形态必须放行（防误伤——收紧闸门的最大风险）
# ---------------------------------------------------------------------------

MUST_PASS = [
    "add(rank(close), rank(returns))",                     # 等权（无系数）
    "rank(0.5*multiply(close, returns))",                  # 单腿系数缩放（非 add 上下文）
    "multiply(0.5, rank(close))",                          # 函数式单腿缩放
    "divide(flow, add(stock, 0.0001))",                    # 分母 eps 保护
    # 五类结构交互（用户定案唯一放行的组合形态，2026-09-16 直调实测全 PASS）
    "ts_corr(rank(fnd6_x), rank(fnd7_y), 66)",
    "group_zscore(ts_delta(fnd6_x, 22), subindustry)",
    "subtract(rank(fnd6_ebitda), rank(fnd7_revenue))",
    "if_else(greater(ts_mean(fnd6_x, 5), 0), rank(fnd7_y), -1)",
    # 单系数腿 + 常数偏移（只有 1 个系数腿）
    "add(0.5*rank(close), 5)",
]


@pytest.mark.parametrize("expr", MUST_PASS)
def test_legitimate_forms_still_pass(gate, poison, expr):
    hits = _poison_hits(gate, poison, expr)
    assert not hits, f"合法形态被误伤: {expr} → {hits}"


# ---------------------------------------------------------------------------
# 判定器单元行为
# ---------------------------------------------------------------------------

def test_detector_unit_semantics(gate):
    d = gate._detect_weighted_mix_structural
    # 星号中缀（含镜像腿、嵌套 add）必须命中
    assert d("add(0.4*rank(a), 0.6*rank(b))")
    assert d("add(0.4*subtract(0, rank(a)), 0.6*rank(b))")
    assert d("rank(add(0.5*ts_mean(a, 22), 0.5*ts_mean(b, 66)))")
    # 等权不拦（无系数）
    assert not d("add(rank(a), rank(b))")
    # 单系数腿不拦（<2 条系数腿）
    assert not d("add(0.5*rank(a), 5)")
    # 函数式 multiply(权重, 腿) 不属于本判定器职责（由 func_prefix/suffix 正则拦），
    # 但实测中它常与星号中缀混用，故此处只锁定"不崩溃、语义稳定"：
    assert isinstance(d("add(multiply(0.7, rank(a)), multiply(0.3, rank(b)))"), bool)
    # 括号不平衡宁漏不误伤
    assert not d("add(0.4*rank(a), 0.6*rank(b")


def test_detector_handles_functional_multiply_via_gate(gate, poison):
    """函数式 multiply(权重, 腿) 的加权混合必须仍被旧正则拦（回归保护）。

    结构判定只补星号中缀镜像腿的漏网；func_prefix/suffix 两条正则的
    覆盖面不能被本次改动破坏。
    """
    hits = _poison_hits(gate, poison,
                        "add(multiply(0.7, rank(a)), multiply(0.3, rank(b)))")
    assert hits, "函数式 weighted mix 回归漏网（func_prefix/suffix 失效）"
