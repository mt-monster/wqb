# -*- coding: utf-8 -*-
"""经验提案的生命周期：proposed → active / contested（2026-11-15 P3）。

只管理**自动生成的统计规则**（`rule_id` 以 `stat_dead_` 开头 / `source=distill_wave`）：
- 同一模式在**新的独立波次**再次成立 → `confirmations += 1`；
- 满 `PROMOTE_MIN_CONFIRMATIONS` 波且无矛盾 → `status=active`（只允许 `type=strategy`，
  会被 `build_wave` / `pipeline` 的常驻循环打印；**不生成任何硬拦截规则**）；
- 出现反例（同族/同骨架出现 `n_win > 0`）→ `status=contested`、confidence × 0.7。

**判死永不自动**：`dead_end` / `universe_lever` 型规则不在此模块的晋升范围内；判死仍走
`forum_recon` + `seal_dead_end`（AGENTS.md §8.16）。
"""
from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional, Sequence

from wqb.knowledge import config as kcfg


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def _stat_rule(rule: Dict[str, Any]) -> bool:
    rid = str(rule.get("rule_id") or "")
    return rid.startswith("stat_dead_") or rule.get("source") in ("distill_wave", "distill_promote")


def _retag(rule: Dict[str, Any], tag: str) -> None:
    """把 action.message 的 `[proposed]` 前缀换成当前状态，避免 active 规则仍自称提案。"""
    action = rule.get("action")
    if not isinstance(action, dict):
        return
    msg = str(action.get("message") or "")
    for old in ("[proposed]", "[active]", "[contested]"):
        if msg.startswith(old):
            msg = msg[len(old):].lstrip()
            break
    action["message"] = f"[{tag}] {msg}".rstrip()


def _pattern_verdict(rule: Dict[str, Any], lesson: Dict[str, Any]) -> Optional[bool]:
    """True=确认；False=反例；None=本波无相关证据（不改变状态）。"""
    action = rule.get("action") or {}
    if action.get("op") != "family_stat_dead":
        return None
    params = action.get("params") or {}
    family = params.get("family")
    skeleton = params.get("skeleton")
    if family:
        groups = lesson.get("by_family") or []
        name, kind = family, "family"
    elif skeleton:
        groups = lesson.get("by_skeleton") or []
        name, kind = skeleton, "skeleton"
    else:
        return None
    g = next((x for x in groups if isinstance(x, dict) and x.get(kind) == name), None)
    if not g:
        return None
    if (g.get("n_win") or 0) > 0:
        return False
    return bool(g.get("dead"))


def promote_rules(
    store: Any,
    region: str,
    lesson: Dict[str, Any],
    rules: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    """更新提案计数并按阈值晋升/标 contested；写回 region methodology_rules（DB）。"""
    region = region.upper()
    wave = str(lesson.get("wave") or "")
    data = store.get_methodology_rules(region) or {"version": 1, "rules": []}
    if not isinstance(data, dict):
        data = {"version": 1, "rules": []}
    stored = {r.get("rule_id"): r for r in (data.get("rules") or []) if isinstance(r, dict)}
    summary = {"confirmed": [], "promoted": [], "contested": [], "skipped": []}
    changed = False

    for rule in rules:
        if not isinstance(rule, dict) or not _stat_rule(rule):
            continue
        rid = rule.get("rule_id")
        verdict = _pattern_verdict(rule, lesson)
        if verdict is None:
            summary["skipped"].append(rid)
            continue
        base = dict(stored.get(rid) or {})
        base.update({k: v for k, v in rule.items() if v is not None})
        # 已入库规则的生命周期字段优先于提案：避免 region 快照把 active 降回 proposed
        if rid in stored:
            for k in ("status", "confirmations", "times_applied", "times_succeeded",
                      "confidence", "validated_at", "contest_evidence"):
                if stored[rid].get(k) is not None:
                    base[k] = stored[rid][k]
        base.setdefault("confirmations", 0)
        base.setdefault("times_applied", 0)
        base.setdefault("times_succeeded", 0)
        base.setdefault("confidence", 0.5)
        base["last_seen_wave"] = wave
        # 区域快照（wave="region"）只刷新统计，不推进生命周期：
        # “2 个独立波次确认”必须来自真实波次，不能被一次 bulk 重算刷满。
        if wave == "region":
            rule.clear()
            rule.update(base)
            summary["skipped"].append(rid)
            continue
        changed = True
        if verdict:
            base["confirmations"] += 1
            base["times_applied"] += 1
            base["times_succeeded"] += 1
            base["confidence"] = min(1.0, round(float(base["confidence"]) + 0.1, 3))
            waves = list(base.get("confirmed_waves") or [])
            if wave and wave not in waves:
                waves.append(wave)
            base["confirmed_waves"] = waves[-10:]
            summary["confirmed"].append(rid)
            if (base.get("status") == "proposed"
                    and base["confirmations"] >= kcfg.PROMOTE_MIN_CONFIRMATIONS
                    and base.get("type") == "strategy"):
                base["status"] = "active"
                base["validated_at"] = _now()
                base["source"] = "distill_promote"
                summary["promoted"].append(rid)
        else:
            base["status"] = "contested"
            base["contradictions"] = int(base.get("contradictions") or 0) + 1
            base["confidence"] = round(float(base["confidence"]) * 0.7, 3)
            ev = list(base.get("contest_evidence") or [])
            ev.append({"wave": wave, "reason": "same family/skeleton produced n_win>0",
                       "at": _now()})
            base["contest_evidence"] = ev[-10:]
            summary["contested"].append(rid)
        _retag(base, str(base.get("status") or "proposed"))
        rule.clear()
        rule.update(base)
        # 只有进入 active / contested 才写进 methodology_rules；
        # proposed 只留在 experience_proposals，避免被 RuleStore.query() 默认读成生效规则。
        if base.get("status") in ("active", "contested"):
            stored[rid] = base

    if changed and stored:
        data["rules"] = list(stored.values())
        data["updated_at"] = _now()
        store.upsert_methodology_rules(region, data)
    return summary
