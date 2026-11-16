# -*- coding: utf-8 -*-
"""规则连通性守护（2026-11-15 建立，补上长期只存在于 docstring 的那只）。

背景：`methodology_rules.json` 的 `type` / `action.op` 只有少数几个真的被代码读取。
2026-10-31 机器级核验（`docs/experience/04_engineering.md` §15）确认：
`diagnosis` 只有 4 个硬编码 op 会被 `recommend_next_wave` 读取，`dead_end` 只有
`block_pattern` 会真拦表达式，`gate_override` / `field_whitelist` 当前无消费点。
**新造一个 op 名 = 写一条永不生效的规则**，而此前没有机械闸。

本测试守四件事：
  1. 全局 + 区域全部 active/contested 规则都能通过 `wqb.methodology_rules.validate_rule`；
  2. `ADVISORY_OPS` 白名单里的每个 op 在现存规则里真实出现（防止白名单变成永久豁免通道）；
  3. `RuleStore.upsert` 对未知 active op 抛错、对 `proposed` 放行、对 `strategy` 放行；
  4. `query()` 默认不返回 `proposed`（草稿不会悄悄改变行为）。
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TOOLKIT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(TOOLKIT_SCRIPTS))

from wqb.methodology_rules import (
    ADVISORY_OPS,
    CONSUMED_DIAGNOSIS_OPS,
    MethodologyRuleError,
    iter_rule_files,
    validate_rule,
)


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _all_rules():
    for path in iter_rule_files():
        data = _load(path)
        for r in data.get("rules") or []:
            yield path, r


def test_all_live_rules_pass_connectivity_validator():
    """现存 active/contested 规则必须全部能过校验——否则说明校验规则写错了。"""
    bad = []
    n = 0
    for path, rule in _all_rules():
        if (rule.get("status") or "active") not in ("active", "contested"):
            continue
        n += 1
        problems = validate_rule(rule)
        if problems:
            bad.append((str(Path(path).relative_to(REPO_ROOT)), rule.get("rule_id"), problems))
    # 2026-11-15 实测：全局 28 条 + 区域 31 条 = 59 条，其中 active/contested 47 条
    # （其余 12 条为 deprecated explore_contract）。门槛只防路径解析退化成空集。
    assert n >= 40, f"只读到 {n} 条 active/contested 规则，路径解析可能错了"
    assert not bad, "以下规则无法通过连通性校验:\n" + "\n".join(map(str, bad))


def test_advisory_allowlist_has_no_stale_entries():
    """白名单只收现状：每个 advisory op 必须在规则文件里真实出现。

    没有这条，`ADVISORY_OPS` 会退化成“谁都能加”的永久豁免通道——正是
    S13/S11 反复踩过的坑（登记表只增不减）。
    """
    seen = set()
    for _path, rule in _all_rules():
        op = (rule.get("action") or {}).get("op")
        if op:
            seen.add(op)
    stale = sorted(set(ADVISORY_OPS) - seen)
    assert not stale, f"ADVISORY_OPS 里以下 op 已不在任何规则文件中，应删除: {stale}"


def test_consumed_diagnosis_ops_have_code_branch():
    """4 个硬编码 diagnosis op 必须在 `_lib/rules.py` 的 recommend_next_wave 里出现。"""
    src = (TOOLKIT_SCRIPTS / "_lib" / "rules.py").read_text(encoding="utf-8", errors="ignore")
    missing = [op for op in sorted(CONSUMED_DIAGNOSIS_OPS) if op not in src]
    assert not missing, f"这些 op 宣称被消费，但 _lib/rules.py 里找不到: {missing}"


def test_unknown_active_op_is_rejected():
    rule = {
        "rule_id": "pytest_unknown_active_op",
        "type": "diagnosis",
        "status": "active",
        "action": {"op": "definitely_not_consumed_anywhere", "message": "x"},
    }
    problems = validate_rule(rule)
    assert problems and "不被" in problems[0] or "没有代码消费点" in problems[0]


def test_proposed_unknown_op_is_allowed():
    rule = {
        "rule_id": "pytest_proposed_unknown_op",
        "type": "diagnosis",
        "status": "proposed",
        "action": {"op": "future_op_pending_wiring", "message": "x"},
    }
    # 草稿可以存，晋升时必须重新校验
    from wqb.methodology_rules import assert_writable

    assert_writable(rule)  # 不抛
    rule["status"] = "active"
    with pytest.raises(MethodologyRuleError):
        assert_writable(rule)


def test_strategy_any_op_is_visible():
    rule = {
        "rule_id": "pytest_strategy_advisory",
        "type": "strategy",
        "status": "active",
        "action": {"op": "whatever", "message": "会被常驻循环打印"},
    }
    assert validate_rule(rule) == []


def test_dead_end_block_pattern_is_hard_consumed():
    rule = {
        "rule_id": "pytest_dead_end_block",
        "type": "dead_end",
        "status": "active",
        "action": {"block_pattern": r"rank\\(ts_backfill\\(", "message": "x"},
    }
    assert validate_rule(rule) == []


def test_rule_store_rejects_unknown_active_op(tmp_path, monkeypatch):
    from _lib.rules import RuleStore

    monkeypatch.setenv("WQB_RULES_FILE_ONLY", "1")
    store = RuleStore(str(tmp_path))
    with pytest.raises(MethodologyRuleError):
        store.upsert({
            "rule_id": "pytest_store_reject",
            "type": "diagnosis",
            "status": "active",
            "action": {"op": "definitely_not_consumed_anywhere", "message": "x"},
        }, global_scope=False)


def test_rule_store_query_hides_proposed(tmp_path, monkeypatch):
    from _lib.rules import RuleStore

    monkeypatch.setenv("WQB_RULES_FILE_ONLY", "1")
    store = RuleStore(str(tmp_path))
    store.upsert({
        "rule_id": "pytest_store_proposed",
        "type": "diagnosis",
        "status": "proposed",
        "action": {"op": "future_op_pending_wiring", "message": "x"},
    }, global_scope=False)
    assert not [r for r in store.query(rule_type="diagnosis") if r["rule_id"] == "pytest_store_proposed"]
    assert [r for r in store.query(rule_type="diagnosis", status="proposed")
            if r["rule_id"] == "pytest_store_proposed"]
