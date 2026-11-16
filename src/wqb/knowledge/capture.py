# -*- coding: utf-8 -*-
"""逐条回测经验索引的唯一写入方（2026-11-15）。

两条收批路径都只调本模块：
1. `pipeline.py stage_review`（`rows` 已带 `walls`，信息最全）；
2. `wqb_db_mcp.harvest_multisim_results`（只有平台读数，`walls` 留空，等 S4 补）。

本模块是**派生层**：只读 `backtest_results` / `expressions` / `s4_walls_*` / ledger，
写 `attempt_knowledge`；绝不改写事实表。重复调用是幂等的（除 `updated_at`）。
"""
from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional, Sequence

from wqb.expression.skeleton import structural_signature
from wqb.knowledge import classify, versions

#: 写进 settings_json 的设置维度（白名单，避免把整包 settings 塞进库）
_SETTINGS_KEYS = (
    "universe", "delay", "neutralization", "neut", "decay", "truncation",
    "nanHandling", "nan_handling", "maxTrade", "max_trade", "dataset", "region",
)


def _loads(v: Any) -> Dict[str, Any]:
    if isinstance(v, dict):
        return v
    if isinstance(v, str) and v:
        try:
            d = json.loads(v)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}
    return {}


def _as_list(v: Any) -> List[Any]:
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v:
        try:
            d = json.loads(v)
            return d if isinstance(d, list) else [d]
        except Exception:
            return [v]
    return []


def _as_names(items: Any) -> List[str]:
    """check 列表 → 名称列表（兼容平台 `{"name": ...}` 与纯字符串两种形态）。"""
    out: List[str] = []
    for x in _as_list(items):
        if isinstance(x, dict):
            name = x.get("name") or x.get("check") or x.get("check_name")
            if name:
                out.append(str(name))
        elif x not in (None, ""):
            out.append(str(x))
    return out


def _wave_rows(store: Any, region: str, wave: str) -> List[Dict[str, Any]]:
    rows = store.connection.execute(
        "SELECT * FROM backtest_results WHERE region=? AND wave=?", (region, wave)
    ).fetchall()
    return [dict(r) for r in rows]


def _expression_map(store: Any, region: str, wave: str) -> Dict[str, Dict[str, Any]]:
    rows = store.connection.execute(
        "SELECT * FROM expressions WHERE region=? AND wave=?", (region, wave)
    ).fetchall()
    if not rows:
        # 兼容老库：expressions.region/wave 冗余列可能为空，退回 wave_id 关联
        rows = store.connection.execute(
            "SELECT e.* FROM expressions e JOIN waves w ON e.wave_id=w.id "
            "JOIN regions r ON r.id=w.region_id WHERE r.name=? AND w.wave_number=?",
            (region, wave),
        ).fetchall()
    out: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        d = dict(r)
        code = (d.get("expression") or "").strip()
        if code:
            out[code] = d
    return out


def _s4_per_alpha(store: Any, region: str, wave: str) -> Dict[str, List[str]]:
    try:
        payload = store.get_ledger(region, f"s4_walls_{region}_{wave}")
    except Exception:
        payload = None
    if not isinstance(payload, dict):
        return {}
    per = payload.get("per_alpha") or {}
    if not isinstance(per, dict):
        return {}
    return {str(k): v for k, v in per.items() if isinstance(v, list)}


def _settings_for(expr_row: Dict[str, Any], wave_settings: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for src in (_loads(expr_row.get("settings_json")), wave_settings or {}):
        for k in _SETTINGS_KEYS:
            if src.get(k) is not None:
                merged[k] = src[k]
    return merged


def _merge_rows(base: Dict[str, Any], extra: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    out = dict(base)
    if extra:
        for k, v in extra.items():
            if v is not None:
                out[k] = v
    return out


def build_attempt_records(
    store: Any,
    region: str,
    wave: str,
    *,
    rows: Optional[Sequence[Dict[str, Any]]] = None,
    settings: Optional[Dict[str, Any]] = None,
    thresholds: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """构造（不写库）逐条经验记录。`dry_run` / 测试 / distill 都复用它。"""
    region = region.upper()
    wave = str(wave)
    expr_map = _expression_map(store, region, wave)
    bt_rows = _wave_rows(store, region, wave)
    per_alpha = _s4_per_alpha(store, region, wave)

    enrich_by_alpha: Dict[str, Dict[str, Any]] = {}
    enrich_by_expr: Dict[str, Dict[str, Any]] = {}
    for r in rows or []:
        if not isinstance(r, dict):
            continue
        aid = r.get("alpha_id") or r.get("id")
        code = (r.get("code") or r.get("expression") or r.get("expr") or "").strip()
        if aid:
            enrich_by_alpha[str(aid)] = r
        if code:
            enrich_by_expr[code] = r

    near_floor = float((thresholds or {}).get("near_sharpe_min")
                       or (thresholds or {}).get("sharpe_min") or 1.0)
    priors_sha = versions.priors_fingerprint(store, region, wave)
    rules_sha = versions.rules_fingerprint(store, region)
    kv = versions.knowledge_version(priors_sha, rules_sha)

    out: Dict[str, Dict[str, Any]] = {}
    for b in bt_rows:
        code = (b.get("code") or "").strip()
        expr_row = expr_map.get(code) or {}
        alpha_id = b.get("alpha_id")
        expr_id = b.get("expression_id")
        attempt_id = str(alpha_id) if alpha_id else f"expr:{expr_id}"
        payload = _loads(b.get("payload_json"))
        base = dict(payload)
        base.update({k: v for k, v in b.items() if v is not None and k != "payload_json"})
        extra = enrich_by_alpha.get(str(alpha_id)) if alpha_id else None
        if extra is None and code:
            extra = enrich_by_expr.get(code)
        merged = _merge_rows(base, extra)

        metrics = classify.metrics_from(merged)
        # RA 三态：列存在且为 '[]' = 已知全过；非空 = 有失败；NULL = 未知（不得当全过）
        ra_raw = b.get("ra_failed_checks")
        if ra_raw is None and "ra_failed_checks" in payload:
            ra_raw = payload.get("ra_failed_checks")
        ra_failed = _as_names(ra_raw) if ra_raw is not None else None
        raw_walls = _as_names(merged.get("walls")) if merged.get("walls") is not None else None
        if raw_walls is None:
            # 没有 review 的 walls 时，用平台读数兜底：failed_checks / RA 失败项 /
            # checks 里非 PASS 的项。这样 MCP 手工收批路径也能得到主墙，不必等 S4。
            raw_walls = _as_names(merged.get("failed_checks")) + list(ra_failed or [])
            if not raw_walls:
                non_pass = classify.checks_non_pass(payload)
                if non_pass:
                    raw_walls = [str(c.get("name")) for c in non_pass if c.get("name")]
            if not raw_walls:
                raw_walls = None
        pseudo = classify.pseudo_walls(metrics)
        if raw_walls is None:
            walls: Optional[List[Any]] = pseudo or None
        else:
            walls = list(dict.fromkeys(_as_names(raw_walls) + pseudo))
        if walls is None and str(alpha_id) in per_alpha:
            walls = list(dict.fromkeys(_as_names(per_alpha[str(alpha_id)]) + pseudo))
        elif isinstance(walls, list) and not walls and str(alpha_id) in per_alpha:
            walls = _as_names(per_alpha[str(alpha_id)])

        primary = classify.primary_wall(walls)
        outv = classify.outcome(
            merged.get("status") or b.get("status"), metrics, walls, ra_failed, near_floor)
        structural = classify.is_structural(walls, metrics)
        fclass = classify.failure_class(primary, outv)
        action = classify.next_action(primary, structural)

        skeleton = (expr_row.get("skeleton") or "").strip() or structural_signature(code)
        family = expr_row.get("family") or expr_row.get("bucket")
        settings_json = _settings_for(expr_row, settings)
        mechanism = None
        for src in (settings or {}, payload, expr_row):
            mechanism = src.get("mechanism") or src.get("hypothesis")
            if mechanism:
                break

        rec = {
            "attempt_id": attempt_id,
            "alpha_id": alpha_id,
            "expression_id": expr_id,
            "region": region,
            "wave": wave,
            "dataset": b.get("dataset") or (settings or {}).get("dataset"),
            "expression": code,
            "skeleton": skeleton or None,
            "family": family,
            "mechanism": mechanism,
            "source": expr_row.get("source"),
            "expected_exposure": expr_row.get("expected_exposure"),
            "settings_json": settings_json or None,
            "metrics_json": metrics or None,
            "walls_json": walls if walls is not None else None,
            "primary_wall": primary,
            "failure_class": fclass,
            "is_structural": 1 if structural else 0,
            "ra_failed_json": list(ra_failed) if ra_failed is not None else None,
            "checks_json": classify.checks_non_pass(payload) or None,
            "outcome": outv,
            "next_action": action,
            "priors_sha": priors_sha,
            "rules_sha": rules_sha,
            "knowledge_version": kv,
            "evidence_ref": (f"s4_walls_{region}_{wave}" if per_alpha else f"wave:{wave}"),
            # 用回测行的时间作为 attempt 时间（yield 按 knowledge_version 排时间线用）
            "created_at": b.get("created_at") or payload.get("created_at"),
        }
        out[attempt_id] = rec
    return list(out.values())


def refresh_attempt_knowledge(
    store: Any,
    region: str,
    wave: str,
    *,
    rows: Optional[Sequence[Dict[str, Any]]] = None,
    settings: Optional[Dict[str, Any]] = None,
    thresholds: Optional[Dict[str, Any]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """构建并写入本波逐条经验；返回摘要。失败由调用方决定是否阻断。"""
    records = build_attempt_records(
        store, region, wave, rows=rows, settings=settings, thresholds=thresholds)
    summary = {
        "region": region.upper(),
        "wave": str(wave),
        "records": len(records),
        "written": 0,
        "outcomes": _count(records, "outcome"),
        "primary_walls": _count(records, "primary_wall"),
        "knowledge_version": records[0].get("knowledge_version") if records else None,
        "dry_run": bool(dry_run),
    }
    if dry_run:
        return summary
    if records:
        summary["written"] = store.upsert_attempt_knowledge(records)
    return summary


def _count(records: Iterable[Dict[str, Any]], key: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for r in records:
        k = str(r.get(key) or "null")
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
