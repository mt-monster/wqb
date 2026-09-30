# -*- coding: utf-8 -*-
r"""step_eval — 九步质量效能增益矩阵的**唯一推导点**（T1 只读推导 + T2 事件聚合，2026-09-30 方案 B）。

## 契约

- **只读**：本模块对既有表（expressions/gate_results/backtest_results/wave_results/
  fields/ledger_kv）与 `step_events` 事件表**只 SELECT**，绝不建表、绝不写库
  （写事件走 `step_events.record_event`，只在埋点处调用）。
- **不猜数**：缺表/缺键/0 分母一律产出 `value=None`（未知），绝不报 0。
- 每条指标带 `source`（推导 SQL 口径或事件类型）与 `tier`（T1 推导 / T2 事件），
  R1 可审计；评分统一走 `step_scoring`（R2 单点）。
- T3 反事实估算不进本模块（永不入库，报告估算区由渲染层处理）。

## 九步矩阵（指标名 → 口径）

| 步 | quality（好方向比率） | efficiency | gain |
|---|---|---|---|
| S-PRE | dead_path_compliance = 1−\|白名单∩判死集\|/\|白名单\| | n/a（显式 None） | dead_paths_excluded（判死键数，计数） |
| S0 | pyramid_quota_compliance（白名单非 model 前缀 ≥2） | s0_ranking_span_days（原始量） | cache_reuse_rate（T2 事件） |
| S1 | field_gate_rate（白名单数据集中字段数 ≥10 占比） | fields_span_days（原始量） | cold_field_ratio（user_count≤9 占比） |
| S2 | concept_declare_rate（expected_exposure 非空占比） | consumption_efficiency = 1−unconsumed/total | priors_reuse（先验快照/缓存键存在 1/0） |
| S2->S3 | expr_gate_pass_rate（report_json passed/total） | gate_coverage（被门禁检过的表达式占比） | gate_blocked_expr + ghost_blocked（T2 计数） |
| S3 | complete_rate（COMPLETE/rows） | non_waste_rate = 1−(ERROR+CANCELLED)/rows | T2 重试/连坐计数 |
| S4 | walls_coverage（s4_walls_* 键/波数） | review_latency_days（原始量） | salvage_pool_size（计数） |
| S4->S5 | submit_ready_conversion（ready/达标数） | blocked_complement = 1−blocked/(ready+blocked) | （与门禁拦截同源，不重复计） |
| S6 | verdict_nonempty_rate | wave_span_days（原始量） | region_kb_refreshed（T2 计数） |

ROI = cheap_pass / backtest_rows；unit_cost = backtest_rows / cheap_pass（原始量）。
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from wqb.step_events import aggregate_conn as _events_aggregate
from wqb.step_scoring import compute_scores, safe_rate

#: 廉价闸口径（与 step_funnel / 战役 SOP 一致；非提交层阈值）
CHEAP_SHARPE = 1.58
CHEAP_FITNESS = 1.0

#: 生成池"尚未被回测消化"状态（与 step_funnel backlog 口径一致）
_UNCONSUMED = ("gem", "selected", "pending", "gated")

#: MODEL 族数据集命名启发（S0 金字塔配额：白名单 ≥2 个非 MODEL）
_MODEL_RE = re.compile(r"^(model|mdl)", re.I)


def _metric(name: str, value: Optional[float], unit: str, source: str, tier: str,
            score_eligible: bool, note: str = "") -> Dict[str, Any]:
    return {"name": name, "value": value, "unit": unit, "source": source,
            "tier": tier, "score_eligible": score_eligible, "note": note}


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone() is not None


def _scalar(conn: sqlite3.Connection, sql: str, params: Tuple = ()) -> Any:
    try:
        row = conn.execute(sql, params).fetchone()
        return row[0] if row else None
    except sqlite3.Error:
        return None


def _ledger_json(conn: sqlite3.Connection, region: str, key: str) -> Any:
    """读 ledger 键并解析 JSON；缺键/脏 JSON 返回 None。"""
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)
        ).fetchone()
    except sqlite3.Error:
        return None
    if not row or row[0] is None:
        return None
    try:
        return json.loads(row[0])
    except (json.JSONDecodeError, TypeError):
        return None


def _days_between(a: Optional[str], b: Optional[str]) -> Optional[float]:
    """两个 ISO 时间戳之间天数（b−a）；解析失败返回 None。"""
    if not a or not b:
        return None
    try:
        ta = datetime.fromisoformat(str(a).replace(" ", "T"))
        tb = datetime.fromisoformat(str(b).replace(" ", "T"))
        return abs((tb - ta).total_seconds()) / 86400.0
    except (ValueError, TypeError):
        return None


def _whitelist_datasets(conn: sqlite3.Connection, region: str) -> List[str]:
    v = _ledger_json(conn, region, "s0_whitelist")
    if isinstance(v, dict):
        ds = v.get("datasets")
        if isinstance(ds, list):
            return [str(d) for d in ds]
    if isinstance(v, list):
        return [str(d) for d in v]
    return []


def _dead_datasets(conn: sqlite3.Connection, region: str) -> List[str]:
    try:
        rows = conn.execute(
            "SELECT key FROM ledger_kv WHERE region=? AND key LIKE '%_dead'", (region,)
        ).fetchall()
    except sqlite3.Error:
        return []
    return [str(k).replace("_dead", "") for (k,) in rows]


def build_step_eval(conn: sqlite3.Connection, region: str,
                    wave: Optional[str] = None) -> Dict[str, Any]:
    """构建九步质量效能增益矩阵（只读推导 + 事件聚合）。

    Args:
        conn: 只读连接（推荐 `connect_db_readonly`；普通连接亦可，本函数不写）
        region: 区域（统一转大写）
        wave: 可选波次过滤（部分指标天然是全区口径，无法按波过滤时在 note 标注）

    Returns:
        {"region", "wave", "steps": {step: {"quality": [...], "efficiency": [...],
         "gain": [...]}}, "events": {...}, "counts": {...}, "scores": {...}}
    """
    region = str(region).upper()
    steps: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
    for s in ("S-PRE", "S0", "S1", "S2", "S2->S3", "S3", "S4", "S4->S5", "S6"):
        steps[s] = {"quality": [], "efficiency": [], "gain": []}

    events = _events_aggregate(conn, region, wave)

    def _ev(step: str, etype: str) -> Optional[Dict[str, Any]]:
        return (events.get(step) or {}).get(etype)

    # ---------------- S-PRE ----------------
    wl = _whitelist_datasets(conn, region)
    dead = _dead_datasets(conn, region)
    if wl:
        overlap = len(set(wl) & set(dead))
        q = safe_rate(len(wl) - overlap, len(wl))
    else:
        q = None
    steps["S-PRE"]["quality"].append(_metric(
        "dead_path_compliance", q, "ratio",
        "ledger s0_whitelist.datasets 与 *_dead 键交集：1−|交集|/|白名单|", "T1", True,
        note=None if wl else "s0_whitelist 缺失/为空 → n/a"))
    steps["S-PRE"]["efficiency"].append(_metric(
        "lookup_latency", None, "s", "MCP 层不回传耗时 → n/a（R3 禁估算）", "T1", False,
        note="n/a"))
    steps["S-PRE"]["gain"].append(_metric(
        "dead_paths_excluded", float(len(dead)) if _table_exists(conn, "ledger_kv") else None,
        "count", "ledger *_dead 键计数", "T1", False))

    # ---------------- S0 ----------------
    if wl:
        non_model = [d for d in wl if not _MODEL_RE.match(d)]
        q = 1.0 if len(non_model) >= 2 else 0.0
    else:
        q = None
    steps["S0"]["quality"].append(_metric(
        "pyramid_quota_compliance", q, "0/1",
        "s0_whitelist 非 model/mdl 前缀数据集 ≥2 → 1（启发式：^model|^mdl）", "T1", True))
    span = None
    if _table_exists(conn, "ledger_kv"):
        row = conn.execute(
            "SELECT created_at, updated_at FROM ledger_kv WHERE region=? AND key='s0_ranking'",
            (region,)).fetchone()
        if row:
            span = _days_between(row[0], row[1])
    steps["S0"]["efficiency"].append(_metric(
        "s0_ranking_span_days", span, "days",
        "ledger_kv s0_ranking created_at→updated_at", "T1", False))
    hits = (_ev("S0", "cache_hit") or {}).get("count")
    applied = (_ev("S0", "calibrate_applied") or {}).get("count")
    if hits is None and applied is None:
        cache_rate = None
        note = "n/a（无事件源）"
    else:
        cache_rate = safe_rate(hits or 0, (hits or 0) + (applied or 0))
        note = ""
    steps["S0"]["gain"].append(_metric(
        "cache_reuse_rate", cache_rate, "ratio",
        "step_events cache_hit/(cache_hit+calibrate_applied)", "T2", True, note=note))

    # ---------------- S1 ----------------
    if wl and _table_exists(conn, "fields"):
        ok = 0
        total = 0
        for d in wl:
            total += 1
            n = _scalar(conn, "SELECT COUNT(*) FROM fields WHERE dataset_id=?", (d,))
            if (n or 0) >= 10:
                ok += 1
        q = safe_rate(ok, total) if total else None
    else:
        q = None
    steps["S1"]["quality"].append(_metric(
        "field_gate_rate", q, "ratio",
        "fields 表每数据集字段数 ≥10 的白名单占比（S1 失败分支口径）", "T1", True,
        note=None if (wl and _table_exists(conn, "fields")) else "fields 表/白名单缺失 → n/a"))
    span = None
    if _table_exists(conn, "fields"):
        row = conn.execute(
            "SELECT MIN(created_at), MAX(created_at) FROM fields WHERE created_at IS NOT NULL"
        ).fetchone()
        if row:
            span = _days_between(row[0], row[1])
    steps["S1"]["efficiency"].append(_metric(
        "fields_span_days", span, "days", "fields.created_at 时间窗", "T1", False))
    cold = None
    if _table_exists(conn, "fields"):
        n_cold = _scalar(conn, "SELECT COUNT(*) FROM fields WHERE user_count<=9")
        n_known = _scalar(conn, "SELECT COUNT(*) FROM fields WHERE user_count IS NOT NULL")
        cold = safe_rate(n_cold, n_known)
    steps["S1"]["gain"].append(_metric(
        "cold_field_ratio", cold, "ratio",
        "fields.user_count≤9 占比（prod-corr 规避纪律：冷门字段 ≥50% 预算）", "T1", True))

    # ---------------- S2 ----------------
    if _table_exists(conn, "expressions"):
        n_total = _scalar(conn, "SELECT COUNT(*) FROM expressions WHERE region=?"
                         + (" AND wave=?" if wave else ""),
                         (region, str(wave)) if wave else (region,))
        n_declared = _scalar(conn, "SELECT COUNT(*) FROM expressions WHERE region=?"
                             + (" AND wave=?" if wave else "")
                             + " AND expected_exposure IS NOT NULL",
                             (region, str(wave)) if wave else (region,))
        q = safe_rate(n_declared, n_total)
        by_status = {str(k): int(v) for k, v in conn.execute(
            "SELECT status, COUNT(*) FROM expressions WHERE region=?"
            + (" AND wave=?" if wave else "") + " GROUP BY status",
            (region, str(wave)) if wave else (region,)).fetchall()}
        n_unconsumed = sum(by_status.get(k, 0) for k in _UNCONSUMED)
        e = safe_rate((n_total or 0) - n_unconsumed, n_total)
    else:
        q = e = None
    steps["S2"]["quality"].append(_metric(
        "concept_declare_rate", q, "ratio",
        "expressions.expected_exposure 非空占比（Expected Exposure 声明会被验证）", "T1", True))
    steps["S2"]["efficiency"].append(_metric(
        "consumption_efficiency", e, "ratio",
        "1−unconsumed(gem+selected+pending+gated)/total", "T1", True))
    priors = None
    if _table_exists(conn, "ledger_kv"):
        # 注意 LIKE 字面量的下划线粒度必须与 docs/ledger_keys.json 键形态对齐
        #（扫描器把 % 归一为 <x>，'priors_snapshot%' 会变成 priors_snapshot<x> 而
        # 脱离目录的 priors_snapshot_<region> 覆盖，test_ledger_key_catalog 会抓）。
        n = _scalar(conn,
                    "SELECT COUNT(*) FROM ledger_kv WHERE region=? AND "
                    "(key LIKE 'priors_snapshot_%' OR key LIKE 'assemble_priors_cache_%')",
                    (region,))
        priors = 1.0 if (n or 0) > 0 else 0.0
    steps["S2"]["gain"].append(_metric(
        "priors_reuse", priors, "0/1",
        "ledger priors_snapshot_*/assemble_priors_cache_* 键存在", "T1", True))

    # ---------------- S2->S3 ----------------
    expr_total = expr_passed = 0
    have_expr_counts = False
    gated_exprs = None
    if _table_exists(conn, "gate_results"):
        wb = " AND wave=?" if wave else ""
        wp: Tuple = (region, str(wave)) if wave else (region,)
        for (rj,) in conn.execute(
                "SELECT report_json FROM gate_results WHERE region=?" + wb
                + " AND report_json IS NOT NULL", wp):
            try:
                d = json.loads(rj)
            except (json.JSONDecodeError, TypeError):
                continue
            if isinstance(d, dict) and isinstance(d.get("total"), int) \
                    and isinstance(d.get("passed"), int):
                expr_total += d["total"]
                expr_passed += d["passed"]
                have_expr_counts = True
        q = safe_rate(expr_passed, expr_total) if have_expr_counts else None
        # 门禁覆盖率：被门禁检过的表达式 / 生成的表达式
        if _table_exists(conn, "expressions"):
            n_gen = _scalar(conn, "SELECT COUNT(*) FROM expressions WHERE region=?" + wb, wp)
            gated_exprs = safe_rate(expr_total if have_expr_counts else None, n_gen)
    else:
        q = None
    steps["S2->S3"]["quality"].append(_metric(
        "expr_gate_pass_rate", q, "ratio",
        "gate_results.report_json Σpassed/Σtotal（表达式级；pipeline 式 schema 无计数 → n/a）",
        "T1", True))
    steps["S2->S3"]["efficiency"].append(_metric(
        "gate_coverage", gated_exprs, "ratio",
        "被门禁检过的表达式数/生成表达式数", "T1", True))
    gb = (_ev("S2->S3", "gate_blocked_expr") or {}).get("sum")
    ghost = (_ev("S2->S3", "ghost_blocked") or {}).get("sum")
    steps["S2->S3"]["gain"].append(_metric(
        "gate_blocked_expr", gb, "count",
        "step_events gate_blocked_expr（按设计未烧的配额）", "T2", False,
        note="" if gb is not None else "n/a（无事件源）"))
    steps["S2->S3"]["gain"].append(_metric(
        "ghost_blocked", ghost, "count",
        "step_events ghost_blocked（幽灵算子拦截）", "T2", False,
        note="" if ghost is not None else "n/a（无事件源）"))

    # ---------------- S3 ----------------
    n_rows = n_complete = n_waste = cheap = backtested = None
    if _table_exists(conn, "backtest_results"):
        wb = " AND wave=?" if wave else ""
        wp = (region, str(wave)) if wave else (region,)
        n_rows = _scalar(conn, "SELECT COUNT(*) FROM backtest_results WHERE region=?" + wb, wp)
        n_complete = _scalar(conn, "SELECT COUNT(*) FROM backtest_results WHERE region=?"
                             + wb + " AND status='COMPLETE'", wp)
        n_waste = _scalar(conn, "SELECT COUNT(*) FROM backtest_results WHERE region=?"
                          + wb + " AND status IN ('ERROR','CANCELLED')", wp)
        cheap = _scalar(conn,
                        "SELECT COUNT(*) FROM backtest_results WHERE region=?" + wb
                        + " AND sharpe>?" + " AND fitness>=?",
                        wp + (CHEAP_SHARPE, CHEAP_FITNESS))
        backtested = n_rows
    steps["S3"]["quality"].append(_metric(
        "complete_rate", safe_rate(n_complete, n_rows), "ratio",
        "backtest_results status='COMPLETE'/rows", "T1", True))
    steps["S3"]["efficiency"].append(_metric(
        "non_waste_rate",
        None if n_rows is None else safe_rate((n_rows or 0) - (n_waste or 0), n_rows),
        "ratio", "1−(ERROR+CANCELLED)/rows", "T1", True))
    retry = (_ev("S3", "retry_sent") or {}).get("sum")
    cascade = (_ev("S3", "batch_error_cascade") or {}).get("sum")
    steps["S3"]["gain"].append(_metric(
        "retry_sent", retry, "count", "step_events retry_sent", "T2", False,
        note="" if retry is not None else "n/a（无事件源）"))
    steps["S3"]["gain"].append(_metric(
        "batch_error_cascade", cascade, "count", "step_events batch_error_cascade", "T2", False,
        note="" if cascade is not None else "n/a（无事件源）"))

    # ---------------- S4 ----------------
    n_waves = n_walls = None
    if _table_exists(conn, "wave_results"):
        n_waves = _scalar(conn,
                          "SELECT COUNT(*) FROM wave_results WHERE region=?"
                          + (" AND wave_number=?" if wave else ""), (region, str(wave)) if wave else (region,))
    if _table_exists(conn, "ledger_kv"):
        # 's4_walls_%_%' 两段通配对应目录 s4_walls_<region>_<wave> 的两段占位粒度
        n_walls = _scalar(conn,
                          "SELECT COUNT(*) FROM ledger_kv WHERE region=? AND key LIKE 's4_walls_%_%'",
                          (region,))
    steps["S4"]["quality"].append(_metric(
        "walls_coverage", safe_rate(n_walls, n_waves), "ratio",
        "ledger s4_walls_* 键数 / wave_results 波数", "T1", True))
    span = None
    if _table_exists(conn, "backtest_results") and _table_exists(conn, "wave_results"):
        a = _scalar(conn, "SELECT MIN(created_at) FROM backtest_results WHERE region=?", (region,))
        b = _scalar(conn, "SELECT MAX(updated_at) FROM wave_results WHERE region=?", (region,))
        span = _days_between(a, b)
    steps["S4"]["efficiency"].append(_metric(
        "review_latency_days", span, "days",
        "backtest_results.min(created_at)→wave_results.max(updated_at)（近似）", "T1", False))
    salvage = None
    v = _ledger_json(conn, region, "salvage_pool")
    if isinstance(v, dict):
        entries = v.get("entries")
        salvage = float(len(entries)) if isinstance(entries, list) else None
    elif isinstance(v, list):
        salvage = float(len(v))
    steps["S4"]["gain"].append(_metric(
        "salvage_pool_size", salvage, "count",
        "ledger salvage_pool.entries 计数", "T1", False))

    # ---------------- S4->S5 ----------------
    ready = None
    v = _ledger_json(conn, region, "submit_ready")
    if isinstance(v, list):
        ready = float(len(v))
    elif isinstance(v, dict):
        for k in ("items", "alphas", "entries", "ready"):
            if isinstance(v.get(k), list):
                ready = float(len(v[k]))
                break
    blocked = None
    v = _ledger_json(conn, region, "submit_ready_blocked")
    if isinstance(v, list):
        blocked = float(len(v))
    elif isinstance(v, dict):
        for k in ("items", "alphas", "entries", "blocked"):
            if isinstance(v.get(k), list):
                blocked = float(len(v[k]))
                break
    steps["S4->S5"]["quality"].append(_metric(
        "submit_ready_conversion", safe_rate(ready, cheap), "ratio",
        "ledger submit_ready / backtest 达标数(cheap_pass)", "T1", True))
    steps["S4->S5"]["efficiency"].append(_metric(
        "blocked_complement",
        None if (ready is None and blocked is None)
        else safe_rate(ready or 0, (ready or 0) + (blocked or 0)),
        "ratio", "1−blocked/(ready+blocked)", "T1", True))
    steps["S4->S5"]["gain"].append(_metric(
        "quota_saved_by_gate", None, "count",
        "与 S2->S3 gate_blocked_expr 同源，不重复计（设计约定）", "T1", False, note="见 S2->S3"))

    # ---------------- S6 ----------------
    n_verdict = None
    if _table_exists(conn, "wave_results"):
        wb = " AND wave_number=?" if wave else ""
        wp = (region, str(wave)) if wave else (region,)
        n_verdict = _scalar(conn,
                            "SELECT COUNT(*) FROM wave_results WHERE region=?" + wb
                            + " AND verdict IS NOT NULL AND TRIM(verdict)<>''", wp)
    steps["S6"]["quality"].append(_metric(
        "verdict_nonempty_rate", safe_rate(n_verdict, n_waves), "ratio",
        "wave_results.verdict 非空占比（历史薄弱点：曾 97/133 空）", "T1", True))
    span = None
    if _table_exists(conn, "wave_results"):
        row = conn.execute(
            "SELECT MIN(created_at), MAX(updated_at) FROM wave_results WHERE region=?",
            (region,)).fetchone()
        if row:
            span = _days_between(row[0], row[1])
    steps["S6"]["efficiency"].append(_metric(
        "wave_span_days", span, "days",
        "wave_results.created_at→updated_at 时间窗", "T1", False))
    refresh = (_ev("S6", "region_kb_refreshed") or {}).get("sum")
    steps["S6"]["gain"].append(_metric(
        "region_kb_refreshed", refresh, "count",
        "step_events region_kb_refreshed", "T2", False,
        note="" if refresh is not None else "n/a（无事件源）"))

    counts = {
        "backtested": float(backtested) if backtested is not None else None,
        "cheap_pass": float(cheap) if cheap is not None else None,
    }
    scores = compute_scores(steps, counts)
    return {
        "region": region,
        "wave": wave,
        "steps": steps,
        "events": events,
        "counts": counts,
        "scores": scores,
    }
