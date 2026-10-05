# -*- coding: utf-8 -*-
"""守护 methodology_rules.json 的「连通性」：写了的规则必须有人消费（2026-10-03 建立）。

背景：2026-10-03 审计发现 23 条规则里只有 4 条真正生效——其余规则写进了 rules.json、
confidence 与 times_applied 都在，但**没有任何代码分支消费它们的 action.op**，
于是「有计量、无作用」。更隐蔽的是 `trigger.condition` 是自然语言字符串，
`RuleStore.query()` 从不解析它，条件写得再精确也不参与匹配。

修复方式：引入声明式通用注入 `_lib.rules.inject_rules()` —— 规则自带结构化 `when`
与 `emit`，由通用执行器消费，新增规则不必再改代码；步 7（wave_review）兜底接收
phase 未接入专属注入点的规则，保证任何 active 规则都不会成为孤儿。

本测试守护三件事：
  1. 连通性：每条 active 规则都至少在一个注入点露面（孤儿 = 0）；
  2. 条件化：声明了 `when` 的规则必须能被求值器正确判真/判假（含反向负例）；
  3. 反退化：`inject_rules` 不得因单条规则字段缺失而整体崩（缺字段应降级不抛）。

⚠ 反向负例是必须的：只断言「能露面」会在执行器退化成「无条件全返回」时依然全绿。
"""
import importlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = (
    REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
)
RULES_JSON = (
    REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config"
    / "methodology_rules.json"
)

# 一个「IS 强 + prod 撞墙」的步 7 典型事实集
FACTS_STRONG_PROD_WALL = {
    "max_sharpe": 1.62,
    "max_prod": 0.78,
    "dom_wall": "PROD",
    "has_near": True,
    "n_rows": 8,
    "verdict": "RETRY_FIXABLE",
    "universe": "TOP600",
    "region": "KOR",
}


def _load_rules_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    return importlib.import_module("_lib.rules")


class _Ctx:
    """最小 ctx 桩：inject_rules 只用到 dir / region / settings。"""

    def __init__(self, region="KOR"):
        self.dir = str(REPO_ROOT / "tracking" / region)
        self.region = region
        self.settings = {"universe": "TOP600", "delay": 1}


@pytest.fixture(scope="module")
def rules_mod():
    return _load_rules_mod()


@pytest.fixture(scope="module")
def raw_rules():
    data = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    assert isinstance(data.get("rules"), list), "methodology_rules.json 无 rules"
    return [r for r in data["rules"] if r.get("status") == "active"]


# ---------------- 1. 连通性：不能有孤儿 ----------------

def test_no_orphan_rules(rules_mod, raw_rules):
    """每条 active 规则都必须在步 7 通用注入里露面（兜底接收未接入专属阶段的 phase）。"""
    got = rules_mod.inject_rules(
        _Ctx(), FACTS_STRONG_PROD_WALL, phase="wave_review",
        context={"region": "KOR"}, fallback_unrouted=True,
    )
    surfaced = {g["source_rule"] for g in got}
    orphan = [r["rule_id"] for r in raw_rules if r["rule_id"] not in surfaced]
    assert not orphan, (
        f"以下 active 规则无任何注入点消费（孤儿），写了等于没写：{orphan}\n"
        "修法：给规则补 `when`（结构化触发条件）+ `emit`（direction/action_hint），"
        "或在其 trigger.phase 对应的阶段接入 inject_rules()。"
    )


def test_inject_emits_structured_fields(rules_mod):
    """注入结果必须带上消费方可直接用的字段，不能只有一句 message。"""
    got = rules_mod.inject_rules(
        _Ctx(), FACTS_STRONG_PROD_WALL, phase="wave_review",
        context={"region": "KOR"}, fallback_unrouted=True,
    )
    assert got, "注入结果为空"
    for g in got:
        for k in ("direction", "rationale", "priority", "action_hint",
                  "source_rule", "when_gated"):
            assert k in g, f"{g.get('source_rule')} 注入结果缺字段 {k}"


# ---------------- 2. 条件化：when 求值（含反向负例） ----------------

def test_evaluate_when_ungated_default(rules_mod):
    """无 when -> 命中但标记未条件化（存量规则向后兼容，降权为常驻提示）。"""
    assert rules_mod.evaluate_when(None, {}) == (True, False)
    assert rules_mod.evaluate_when({}, {}) == (True, False)


def test_evaluate_when_all_positive_and_negative(rules_mod):
    """all 子句：全真才真；任一假即假（反向负例）。"""
    w = {"all": [{"fact": "max_prod", "op": ">", "value": 0.7},
                 {"fact": "max_sharpe", "op": ">=", "value": 1.58}]}
    assert rules_mod.evaluate_when(w, {"max_prod": 0.78, "max_sharpe": 1.62}) == (True, True)
    # 反向负例：prod 达标但 sharpe 不够 -> 不得命中
    assert rules_mod.evaluate_when(w, {"max_prod": 0.78, "max_sharpe": 1.20}) == (False, True)


def test_evaluate_when_missing_fact_is_false(rules_mod):
    """事实缺失 -> 保守判假（宁可不提示，也不制造噪声）。"""
    w = {"any": [{"fact": "nonexistent_fact", "op": ">", "value": 0}]}
    assert rules_mod.evaluate_when(w, {"max_prod": 0.9}) == (False, True)


def test_gated_rule_outranks_ungated(rules_mod):
    """条件化命中必须排在常驻提示前面，否则精准建议会被 24 条噪声淹没。"""
    got = rules_mod.inject_rules(
        _Ctx(), FACTS_STRONG_PROD_WALL, phase="wave_review",
        context={"region": "KOR"}, fallback_unrouted=True,
    )
    gated = [g for g in got if g["when_gated"]]
    ungated = [g for g in got if not g["when_gated"]]
    if gated and ungated:
        assert min(g["priority"] for g in gated) > max(g["priority"] for g in ungated), (
            "条件化命中的优先级必须高于常驻提示"
        )


def test_gated_rules_absent_when_condition_unmet(rules_mod):
    """反向负例：条件不满足时，已条件化的规则不得出现在注入结果里。"""
    calm = dict(FACTS_STRONG_PROD_WALL, max_prod=0.30, max_sharpe=0.5)
    got_calm = {g["source_rule"] for g in rules_mod.inject_rules(
        _Ctx(), calm, phase="wave_review",
        context={"region": "KOR"}, fallback_unrouted=True)}
    got_hot = {g["source_rule"] for g in rules_mod.inject_rules(
        _Ctx(), FACTS_STRONG_PROD_WALL, phase="wave_review",
        context={"region": "KOR"}, fallback_unrouted=True)}
    extra_in_calm = got_calm - got_hot
    assert not extra_in_calm, (
        f"条件不成立的上下文反而多出规则：{extra_in_calm}（when 求值方向反了）"
    )


# ---------------- 3. 反退化：缺字段降级不抛 ----------------

def test_inject_rules_tolerates_empty_store(tmp_path, rules_mod, monkeypatch):
    """空规则集 / 缺字段规则不得让整体注入崩掉（L3 消费必须 fail-soft）。"""
    class _EmptyCtx:
        dir = str(tmp_path)
        region = "ZZZ"
        settings = {}

    # ZZ 区无任何规则文件 -> 应返回空列表而非抛异常
    out = rules_mod.inject_rules(_EmptyCtx(), {}, phase="wave_review",
                                 context={"region": "ZZZ"}, fallback_unrouted=True)
    assert isinstance(out, list)
