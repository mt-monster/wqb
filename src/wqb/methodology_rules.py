# -*- coding: utf-8 -*-
"""methodology_rules 写入连通性校验（单一实现，2026-11-15）。

## 为什么有本模块

`methodology_rules.json` 里的 `type` / `action.op` 不是自由标签：**只有少数几个
op 真的被代码读取**。2026-10-31 的机器级核验（见 `docs/experience/04_engineering.md`
§15）确认：

| type | 真实消费点 | 效果 |
|---|---|---|
| `strategy` | `build_wave.py:789` / `pipeline.py:1499` 的常驻循环 | 无条件打印 `action.message`（咨询性） |
| `dead_end` | `build_wave.py:773-787` | 只有 `action.block_pattern` 会真正正则排除表达式 |
| `explore_contract` | `gate.py::get_contract_expiry_state/get_active_contract` | 多样性契约注入 / 过期 |
| `universe_lever` | `pipeline.py:1478` 的 `check_universe_lever` | `action.dead_universe` 命中即拦 |
| `diagnosis` | `recommend_next_wave` | 只认 `gradient_dilute` / `warn_rnf_drop` / `dead_universe` / `classify_failure_nature` / `fail_fast_stop` |

其余 op 没有任何代码读取 —— **新造一个 op 名 = 写了一条永不生效的规则**。
此前这只靠人读文档对照，没有机械闸（`test_methodology_rules_connectivity.py`
长期只存在于 docstring 里）。本模块把“能不能写”变成可执行判定：

- 已有规则里那些咨询性 op 收进 `ADVISORY_OPS` 白名单（**只收现状、只减不增**）；
- `status in ("active", "contested")` 的规则写入时，未知 op 直接拒绝；
- `status == "proposed"` 允许暂存草稿，但晋升（改回 active/contested）时重新校验。

## 与各写入方的关系

- `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/rules.py::RuleStore.upsert`
  在写库前调 `assert_writable()`（`wqb` 不可导入时降级为告警，见该文件的薄壳）。
- `tests/unit/07_docs_skills/test_methodology_rules_connectivity.py` 校验全局 + 区域
  全部 active/contested 规则都能过本模块，并验证新 op 被拒。
- 本模块**不碰数据库、不读文件**，纯判定。
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

#: 规则库里出现过的全部 type（新增 type 必须同时登记消费点）
RULE_TYPES = (
    "strategy",
    "diagnosis",
    "dead_end",
    "gate_override",
    "field_whitelist",
    "universe_lever",
    "explore_contract",
)

#: `diagnosis` 里真正被 `recommend_next_wave` 读取的 op（硬编码分支，见 _lib/rules.py）
CONSUMED_DIAGNOSIS_OPS = frozenset({
    "gradient_dilute",       # strategy 型也会命中；diagnosis 型由 recommend_next_wave 读
    "warn_rnf_drop",
    "dead_universe",
    "classify_failure_nature",
    "fail_fast_stop",
})

#: 有读取方、但只做打印/提示（不改变候选或闸门）的 op。
#:
#: ⚠ 只收 2026-10-31 核验时**已经存在**的 op。新增 op **不要**往这里加：
#: 先改消费代码（让它真的被读），再加规则；否则等于把死规则洗白成“已登记”。
ADVISORY_OPS = frozenset({
    # diagnosis（recommend_next_wave 不读，只有 strategy 常驻打印能看见它们）
    "check_sub_ratio",
    "assert_pyramid_source",
    "warn_region_yield",
    "flag_dataset_weak",
    # dead_end 里没有 block_pattern 的条目：不会拦表达式，只作为先验/提示
    "demote_zero_competition",
    "fail_fast_stop",
    # gate_override / field_whitelist：当前无 apply_rules 消费点（现状，非设计目标）
    "fix_metrics_fallback",
    "merge_whitelist_before_gate",
    "assert_settings_snapshot",
    "require_field_coverage",
    "require_min_template_families",
    "require_boundary_ops_exhaust",
    "prefer_category",
    # universe_lever 的 op 名（硬判定看 action.dead_universe；op 本身只作标识）
    "block_universe",
})

#: `explore_contract` 唯一合法 op（gate.py 按 action 字段消费）
CONTRACT_OP = "inject_diversity"

#: 写入时允许的 status；`proposed` 是草稿态，不参与 `query()` 默认过滤
RULE_STATUSES = ("active", "contested", "deprecated", "proposed")


class MethodologyRuleError(ValueError):
    """规则不满足写入连通性契约。"""


def _action(rule: Dict[str, Any]) -> Dict[str, Any]:
    a = rule.get("action")
    return a if isinstance(a, dict) else {}


def validate_rule(rule: Dict[str, Any]) -> List[str]:
    """返回问题列表（空 = 可写入）。不抛异常，便于测试与批量体检。"""
    problems: List[str] = []
    if not isinstance(rule, dict):
        return ["rule 必须是 dict"]
    rid = rule.get("rule_id")
    if not rid:
        problems.append("缺 rule_id")
    rtype = rule.get("type")
    if rtype not in RULE_TYPES:
        problems.append(f"非法 type: {rtype!r}（可选: {sorted(RULE_TYPES)}）")
        return problems
    status = rule.get("status") or "active"
    if status not in RULE_STATUSES:
        problems.append(f"非法 status: {status!r}（可选: {RULE_STATUSES}）")
    action = _action(rule)
    op = action.get("op")

    # strategy：常驻打印 action.message，任何 op 都“看得见”，不拦。
    if rtype == "strategy":
        return problems

    if rtype == "dead_end":
        # 唯一硬消费字段是 block_pattern；没有它就只能靠 advisory 白名单。
        if action.get("block_pattern"):
            return problems
        if op in ADVISORY_OPS:
            return problems
        problems.append(
            f"dead_end 规则 {rid!r} 既无 action.block_pattern（硬拦），op={op!r} 也不在 "
            "ADVISORY_OPS（咨询白名单）⇒ 写入后不会被任何代码读取"
        )
        return problems

    if rtype == "universe_lever":
        if not action.get("dead_universe"):
            problems.append(
                f"universe_lever 规则 {rid!r} 缺 action.dead_universe"
                "（check_universe_lever 只读这个字段）"
            )
        return problems

    if rtype == "explore_contract":
        if op != CONTRACT_OP:
            problems.append(
                f"explore_contract 规则 {rid!r} 的 op 必须是 {CONTRACT_OP!r}，得到 {op!r}"
            )
        return problems

    if rtype == "diagnosis":
        if op in CONSUMED_DIAGNOSIS_OPS:
            return problems
        if op in ADVISORY_OPS:
            return problems
        problems.append(
            f"diagnosis 规则 {rid!r} 的 op={op!r} 不被 recommend_next_wave 读取，"
            f"也不在 ADVISORY_OPS；可选: {sorted(CONSUMED_DIAGNOSIS_OPS | ADVISORY_OPS)}"
        )
        return problems

    # gate_override / field_whitelist：当前无消费点，只允许已登记的咨询 op
    if op in ADVISORY_OPS:
        return problems
    problems.append(
        f"{rtype} 规则 {rid!r} 的 op={op!r} 当前没有代码消费点（也不在 ADVISORY_OPS）"
    )
    return problems


def assert_writable(rule: Dict[str, Any]) -> None:
    """写入前校验；`proposed` 草稿放行（晋升时会被再次校验）。"""
    if not isinstance(rule, dict):
        raise MethodologyRuleError("rule 必须是 dict")
    if (rule.get("status") or "active") == "proposed":
        return
    problems = validate_rule(rule)
    if problems:
        raise MethodologyRuleError("；".join(problems))


def iter_rule_files() -> Iterable[str]:
    """规则文件的规范位置（全局 1 份 + 区域镜像）。仅供体检工具/测试使用。"""
    import glob
    import os

    from wqb.paths import find_repo_root

    here = str(find_repo_root(__file__))
    yield os.path.join(here, "Claude", "skills", "wq-brain-campaign-toolkit",
                       "config", "methodology_rules.json")
    for p in sorted(glob.glob(os.path.join(here, "tracking", "*", "reference",
                                           "methodology_rules.json"))):
        yield p
