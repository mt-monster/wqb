# -*- coding: utf-8 -*-
"""波级 / 区域级经验蒸馏（2026-11-15，P2）。

输入：`attempt_knowledge`（逐条派生解释）。
输出：
- `wave_lessons_<region>_<wave>`：单波完整统计 + 待确认提案；
- `region_kb.family_stats` / `skeleton_stats`：区域累计统计（上限 40，供 assemble_priors → GEM）；
- `experience_proposals_<region>`：待人工/agent 确认的 dead/win/rule 提案。

纪律：
- 只产出**统计与提案**，不自动 `seal_dead_end`、不自动把规则转 active；
- `distill_wave` / `distill_region` 返回**确定性**结果（不含时间戳），重复运行可直接比对；
- 写 `region_kb` 走完整 read-modify-write，不手写 JSON、不做部分 merge。
"""
from __future__ import annotations

import datetime
import re
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence

from wqb.knowledge import classify
from wqb.knowledge import config as kcfg
from wqb.knowledge.lifecycle import promote_rules
from wqb.knowledge.templates import publish_templates
from wqb.knowledge.versions import canonical_hash


def _max_abs(values: Iterable[Any]) -> float:
    nums = [abs(float(v)) for v in values if isinstance(v, (int, float))]
    return round(max(nums), 4) if nums else 0.0


def _wall_histogram(attempts: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    hist: Dict[str, int] = {}
    for a in attempts:
        walls = a.get("walls_json") or []
        if isinstance(walls, str):
            walls = [walls]
        seen = {classify.canonical_wall(w) for w in walls}
        pw = a.get("primary_wall")
        if pw:
            seen.add(classify.canonical_wall(pw))
        for w in seen:
            hist[w] = hist.get(w, 0) + 1
    return dict(sorted(hist.items(), key=lambda kv: (-kv[1], kv[0])))


def _outcome_mix(attempts: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    mix: Dict[str, int] = {}
    for a in attempts:
        k = str(a.get("outcome") or "unknown")
        mix[k] = mix.get(k, 0) + 1
    return dict(sorted(mix.items(), key=lambda kv: (-kv[1], kv[0])))


def _examples(attempts: Sequence[Dict[str, Any]], cap: int) -> List[str]:
    """优先 win，其次 near，再按 |sharpe| 降序。"""
    order = {"win": 0, "near": 1, "dead": 2, "error": 3, "unknown": 4}

    def key(a):
        m = a.get("metrics_json") or {}
        s = m.get("sharpe") if isinstance(m, dict) else None
        return (order.get(str(a.get("outcome")), 9), -abs(float(s or 0)))

    out, seen = [], set()
    for a in sorted(attempts, key=key):
        aid = a.get("attempt_id")
        if aid and aid not in seen:
            seen.add(aid)
            out.append(str(aid))
        if len(out) >= cap:
            break
    return out


def _group_stats(
    attempts: Sequence[Dict[str, Any]],
    key: str,
    *,
    cap: int,
) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for a in attempts:
        groups[str(a.get(key) or "_unknown")].append(a)
    rows: List[Dict[str, Any]] = []
    for name, items in groups.items():
        n = len(items)
        mix = _outcome_mix(items)
        hist = _wall_histogram(items)
        dom_wall = next(iter(hist), None)
        dom_share = round((hist.get(dom_wall, 0) / n) if dom_wall else 0.0, 4)
        max_s = _max_abs((a.get("metrics_json") or {}).get("sharpe") for a in items
                         if isinstance(a.get("metrics_json"), dict))
        max_2y = _max_abs((a.get("metrics_json") or {}).get("two_year_sharpe") for a in items
                          if isinstance(a.get("metrics_json"), dict))
        max_f = _max_abs((a.get("metrics_json") or {}).get("fitness") for a in items
                         if isinstance(a.get("metrics_json"), dict))
        dead = (
            n >= kcfg.MIN_FAMILY_N
            and max_s < kcfg.DEAD_MAX_SHARPE
            and dom_share >= kcfg.DEAD_WALL_SHARE
            and dom_wall not in (None, "UNKNOWN")
        )
        rows.append({
            key: name,
            "n": n,
            "n_win": mix.get("win", 0),
            "n_near": mix.get("near", 0),
            "n_dead": mix.get("dead", 0),
            "n_error": mix.get("error", 0),
            "n_unknown": mix.get("unknown", 0),
            "max_sharpe": max_s,
            "max_two_year": max_2y,
            "max_fitness": max_f,
            "dominant_wall": dom_wall,
            "dominant_wall_share": dom_share,
            "wall_histogram": hist,
            "outcome_mix": mix,
            "dead": bool(dead),
            "examples": _examples(items, kcfg.EXAMPLES),
        })
    rows.sort(key=lambda r: (-r["n"], -r["max_sharpe"], r[key]))
    return rows[:cap]


def _settings_stats(attempts: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for dim in ("neutralization", "universe", "decay"):
        agg: Dict[str, List[int]] = defaultdict(lambda: [0, 0])
        for a in attempts:
            st = a.get("settings_json") or {}
            if not isinstance(st, dict):
                continue
            v = st.get(dim)
            if v in (None, ""):
                continue
            k = str(v)
            agg[k][1] += 1
            if a.get("outcome") == "win":
                agg[k][0] += 1
        cells = {
            k: {"n": t, "wins": w, "win_rate": round(w / t, 4)}
            for k, (w, t) in agg.items() if t >= kcfg.MIN_CELL_N
        }
        if cells:
            out[f"by_{dim}"] = dict(sorted(cells.items()))
    return out


def _rule_proposals(
    region: str, wave: str, groups: Sequence[Dict[str, Any]], kind: str
) -> List[Dict[str, Any]]:
    out = []
    label = "族" if kind == "family" else "骨架"
    for g in groups:
        name = str(g.get(kind) or "_unknown")
        slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:40] or kind
        out.append({
            "rule_id": f"stat_dead_{kind}_{region.lower()}_{slug}",
            "type": "strategy",  # strategy 型会被常驻打印；proposed 不参与 query() 默认过滤
            "status": "proposed",
            "trigger": {"region": region, kind: name},
            "action": {
                "op": "family_stat_dead",
                "params": {
                    kind: name,
                    "n": g.get("n"),
                    "max_sharpe": g.get("max_sharpe"),
                    "dominant_wall": g.get("dominant_wall"),
                    "dominant_wall_share": g.get("dominant_wall_share"),
                },
                "message": (
                    f"[proposed] {region} {label} {name} 在 {g.get('n')} 条回测中最高 |S|={g.get('max_sharpe')}，"
                    f"主墙 {g.get('dominant_wall')} 占 {g.get('dominant_wall_share'):.0%}；"
                    "是否判死需 forum_recon 取证 + seal_dead_end"
                ),
            },
            "evidence": {"source": "distill_wave", "wave": wave,
                         "attempt_ids": g.get("examples") or []},
            "confidence": 0.5,
            "source": "distill_wave",
        })
    return out


def distill_wave(store: Any, region: str, wave: str) -> Dict[str, Any]:
    """单波蒸馏（确定性：无时间戳）。"""
    region = region.upper()
    attempts = store.list_attempt_knowledge(region=region, wave=str(wave), limit=20000)
    by_family = _group_stats(attempts, "family", cap=kcfg.TOP_FAMILIES)
    by_skeleton = _group_stats(attempts, "skeleton", cap=kcfg.TOP_SKELETONS)
    dead_families = [g for g in by_family if g.get("dead") and g.get("family") != "_unknown"]
    dead_skeletons = [g for g in by_skeleton if g.get("dead") and g.get("skeleton") != "_unknown"]
    wins = [
        {
            "family": g["family"],
            "n": g["n"],
            "n_win": g["n_win"],
            "max_sharpe": g["max_sharpe"],
            "examples": g["examples"],
        }
        for g in by_family if g["n_win"] > 0 and g["family"] != "_unknown"
    ]
    mix = _outcome_mix(attempts)
    n = len(attempts)
    surprises: List[Dict[str, Any]] = []
    try:
        kb = store.get_ledger(region, "region_kb") or {}
        prior = ((kb.get("gate_priors_local") or {}).get("pass_rate")
                 if isinstance(kb, dict) else None)
        if prior is not None and n >= kcfg.MIN_CELL_N:
            observed = round(mix.get("win", 0) / n, 4)
            delta = round(observed - float(prior), 4)
            if abs(delta) >= 0.2:
                surprises.append({
                    "kind": "win_rate_vs_local_prior",
                    "observed": observed,
                    "prior": float(prior),
                    "delta": delta,
                    "n": n,
                    "note": "口径不同（win=全闸+RA，prior=内部线），只作事实提示",
                })
    except Exception:
        pass
    return {
        "region": region,
        "wave": str(wave),
        "n_attempts": n,
        "outcome_mix": mix,
        "knowledge_version": (attempts[0].get("knowledge_version") if attempts else None),
        "by_family": by_family,
        "by_skeleton": by_skeleton,
        "settings": _settings_stats(attempts),
        "surprises": surprises,
        "proposals": {
            "dead_families": dead_families,
            "dead_skeletons": dead_skeletons,
            "wins": wins,
            "rules": (_rule_proposals(region, str(wave), dead_families, "family")
                      + _rule_proposals(region, str(wave), dead_skeletons, "skeleton")),
        },
    }


def distill_region(store: Any, region: str, window_waves: int = 20) -> Dict[str, Any]:
    """区域累计蒸馏（确定性：无时间戳）。`window_waves` 当前按全量统计，参数保留给 P4。"""
    region = region.upper()
    attempts = store.list_attempt_knowledge(region=region, limit=50000)
    versions: Dict[str, int] = {}
    for a in attempts:
        k = str(a.get("knowledge_version") or "na")
        versions[k] = versions.get(k, 0) + 1
    # `_unknown` 分组只诊断用（GEM 未写 family / 表达式为空），不进 GEM priors
    family_stats = [g for g in _group_stats(attempts, "family", cap=kcfg.TOP_FAMILIES)
                    if g.get("family") != "_unknown"]
    skeleton_stats = [g for g in _group_stats(attempts, "skeleton", cap=kcfg.TOP_SKELETONS)
                      if g.get("skeleton") != "_unknown"]
    dead_families = [g for g in family_stats if g.get("dead")]
    dead_skeletons = [g for g in skeleton_stats if g.get("dead")]
    return {
        "region": region,
        "sample_size": len(attempts),
        "family_stats": family_stats,
        "skeleton_stats": skeleton_stats,
        "knowledge_versions": dict(sorted(versions.items(), key=lambda kv: (-kv[1], kv[0]))[:20]),
        # 区域快照级提案（没有 single-wave 证据；wave 记 "region"）
        "proposals": {
            "dead_families": dead_families,
            "dead_skeletons": dead_skeletons,
            "wins": [
                {"family": g["family"], "n": g["n"], "n_win": g["n_win"],
                 "max_sharpe": g["max_sharpe"], "examples": g["examples"]}
                for g in family_stats if g["n_win"] > 0
            ],
            "rules": (_rule_proposals(region, "region", dead_families, "family")
                      + _rule_proposals(region, "region", dead_skeletons, "skeleton")),
        },
    }


def _merge_rule(old: Optional[Dict[str, Any]], new: Dict[str, Any], wave: str) -> Dict[str, Any]:
    """规则提案合并：更新统计/消息，**保留生命周期字段**（confirmations/status/confidence/times）。"""
    if not old:
        out = dict(new)
        out.setdefault("confirmations", 0)
        out["last_seen_wave"] = wave
        return out
    out = dict(old)
    for k in ("type", "action", "trigger"):
        if new.get(k) is not None:
            out[k] = new[k]
    ev_old = old.get("evidence") if isinstance(old.get("evidence"), dict) else {}
    ev_new = new.get("evidence") if isinstance(new.get("evidence"), dict) else {}
    ids = list(dict.fromkeys(list(ev_old.get("attempt_ids") or [])
                            + list(ev_new.get("attempt_ids") or [])))[:20]
    out["evidence"] = {**ev_old, **ev_new, "attempt_ids": ids}
    out["last_seen_wave"] = wave
    return out


def _merge_proposals(existing: Any, lesson: Dict[str, Any]) -> Dict[str, Any]:
    base = existing if isinstance(existing, dict) else {}
    prop = base.get("proposals") if isinstance(base.get("proposals"), dict) else {}
    wave = str(lesson.get("wave") or "")
    out: Dict[str, List[Dict[str, Any]]] = {
        "dead_families": list(prop.get("dead_families") or []),
        "dead_skeletons": list(prop.get("dead_skeletons") or []),
        "wins": list(prop.get("wins") or []),
        "rules": list(prop.get("rules") or []),
    }
    new = lesson.get("proposals") or {}

    for target, key_fields in (("dead_families", ("family",)),
                               ("dead_skeletons", ("skeleton",)),
                               ("wins", ("family",))):
        for item in (new.get(target) or []):
            if not isinstance(item, dict):
                continue
            key = tuple(str(item.get(k)) for k in key_fields)
            out[target] = [x for x in out[target] if tuple(str(x.get(k)) for k in key_fields) != key]
            out[target].insert(0, item)
        out[target] = out[target][:200]

    by_id = {str(r.get("rule_id")): r for r in out["rules"] if isinstance(r, dict) and r.get("rule_id")}
    for item in (new.get("rules") or []):
        if not isinstance(item, dict) or not item.get("rule_id"):
            continue
        rid = str(item["rule_id"])
        by_id[rid] = _merge_rule(by_id.get(rid), item, wave)
    out["rules"] = list(by_id.values())[:200]
    return {
        "region": lesson.get("region") or base.get("region"),
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "last_wave": wave or base.get("last_wave"),
        "proposals": out,
    }


def publish_region_stats(
    store: Any,
    region: str,
    lesson: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """把区域累计统计写回 region_kb，并落 wave_lessons / proposals。"""
    region = region.upper()
    region_stats = distill_region(store, region)
    kb = store.get_ledger(region, "region_kb") or {}
    if not isinstance(kb, dict):
        kb = {}
    before = canonical_hash({k: kb.get(k) for k in ("family_stats", "skeleton_stats")})
    kb["family_stats"] = region_stats["family_stats"]
    kb["skeleton_stats"] = region_stats["skeleton_stats"]
    kb["knowledge_stats"] = {
        "sample_size": region_stats["sample_size"],
        "knowledge_versions": region_stats["knowledge_versions"],
        "computed_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "wqb.knowledge.distill.distill_region",
    }
    kb["updated_at"] = datetime.date.today().isoformat()
    changed = canonical_hash({k: kb.get(k) for k in ("family_stats", "skeleton_stats")}) != before
    store.upsert_ledger(region, "region_kb", kb)

    result: Dict[str, Any] = {
        "ok": True,
        "changed": changed,
        "family_stats": len(kb["family_stats"]),
        "skeleton_stats": len(kb["skeleton_stats"]),
        "sample_size": region_stats["sample_size"],
    }
    if lesson:
        wave = str(lesson.get("wave") or "")
        if wave and wave != "region":
            key = f"wave_lessons_{region}_{wave}"
            payload = dict(lesson)
            payload["published_at"] = datetime.datetime.now().isoformat(timespec="seconds")
            store.upsert_ledger(region, key, payload)
            result["wave_lessons_key"] = key
        existing = store.get_ledger(region, f"experience_proposals_{region}")
        merged = _merge_proposals(existing, lesson)
        result["promotions"] = promote_rules(
            store, region, lesson, merged.get("proposals", {}).get("rules") or [])
        store.upsert_ledger(region, f"experience_proposals_{region}", merged)
        result["templates"] = publish_templates(store, region, lesson)
        result["proposals"] = {
            k: len(v) for k, v in (merged.get("proposals") or {}).items()
        }
    return result
