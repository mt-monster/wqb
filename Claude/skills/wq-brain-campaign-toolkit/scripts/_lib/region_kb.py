# -*- coding: utf-8 -*-
"""region_kb.py - region_kb 台账的两条接线（2026-09-15 审计落地）。

① 设置层先验（settings prior）：`region_kb.gate_priors`（库存实测过闸率，
   `tools/build_gate_prior_from_inventory.py` 产出）里 decay / neutralization 两个维度
   此前只被 `assemble-priors` 渲染成文本塞进 GEM 的 LLM prompt——LLM 只写表达式，
   改不了仿真设置；S3 实际用的永远是 settings.json 的固定值（GBR：decay=14 过闸率
   28.3% n=46 vs decay=4 3.9% n=408，三波仍以 decay4 跑 → 0/44）。本模块把这两个
   维度分流到 S3：`apply_settings_prior(ctx, ...)` 在 pipeline run 装载设置后按实测
   证据改写 `ctx.settings`，显式 `--set` / `--neutralization` 钉住的维度不动。

③ 波后自动刷新：`refresh_after_wave(...)` 在 pipeline stage_review 写完 wave_results 后
   把本波摘要追加进 `region_kb.recent_waves`、用本地 backtest_results 重算
   `gate_priors_local`（by_neutralization / by_operator_count / by_field_family；
   本地行不带 decay，故无 by_decay）、并刷新 `updated_at`。此前 GBR 三波关闭后
   `region_kb.updated_at` 仍停在 09-12——回路只写 wave_results，不回 KB。

纯标准库；读写只碰 ledger_kv 的 `region_kb` 一个 key（定向 upsert，不整区重写）。
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import sqlite3
from collections import defaultdict

from .ledger import make_ledger_store

#: 与 tools/build_gate_prior_from_inventory.py 同口径（算子调用计数 / 字段族前缀）
_OP_CALL_RE = re.compile(r"\b([a-z][a-z0-9_]{2,})\s*\(")
_FIELD_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9_]{3,})\b")
_KNOWN_OPS = set("""
rank add multiply subtract divide group_rank group_zscore group_neutralize group_mean group_sum
group_count group_scale group_std_dev group_backfill ts_mean ts_delta ts_zscore ts_rank ts_backfill
ts_decay_linear ts_std_dev ts_sum ts_max ts_min ts_corr ts_covariance ts_regression ts_av_diff
ts_arg_max ts_arg_min ts_product ts_quantile ts_count_nans ts_scale ts_step ts_returns ts_ir
ts_delay ts_kurtosis ts_max_diff vec_avg vec_sum vec_max vec_min vec_stddev vec_count vec_range
winsorize scale normalize signed_power quantile power reverse zscore abs log sign sqrt inverse
densify pasteurize hump kth_element trade_when if_else bucket greater less equal and or not is_nan
not_equal less_equal greater_equal max min days_from_last_change last_diff_value
industry sector subindustry market country exchange std range rettype driver
returns close open high low volume vwap cap adv20 sharesout
""".split())

#: 最小格子样本量（与库存工具一致：样本太小的格子不进先验）
MIN_CELL_N = 15
RECENT_WAVES_CAP = 20

#: settings prior 默认参数（区域 thresholds.json 的 `settings_prior` 节可覆盖）
SETTINGS_PRIOR_DEFAULTS = {
    "enabled": True,
    "dims": ["decay", "neutralization"],
    "min_n": 30,        # 推荐格子最少样本
    "min_lift": 2.0,    # 推荐格子过闸率 ≥ 当前设置过闸率 × min_lift 才改
    "floor_rate": 0.02, # 当前设置无样本时按此地板算 lift，避免除零把任何格子都当成"大幅提升"
}


# ---------------------------------------------------------------- 工具函数

def _now():
    return _dt.datetime.now().isoformat(timespec="seconds")


def _op_count(code):
    return len(_OP_CALL_RE.findall(code or ""))


def _op_bin(n):
    if n <= 4:
        return "<=4"
    if n <= 8:
        return "5-8"
    return ">8"


def _field_family(code):
    for t in _FIELD_TOKEN_RE.findall(code or ""):
        if t in _KNOWN_OPS or t.isdigit():
            continue
        m = re.match(r"^([a-z]+)", t)
        return m.group(1) if m else t
    return "?"


def _db_path(ctx):
    store = make_ledger_store(ctx)
    return getattr(store, "db_path", None)


def load_region_kb(ctx):
    """读 region_kb（缺失返回 {}）。"""
    path = _db_path(ctx)
    if not path:
        return {}
    conn = sqlite3.connect(path)
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key='region_kb'", (ctx.region,)
        ).fetchone()
    finally:
        conn.close()
    if not row or not row[0]:
        return {}
    try:
        kb = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
    except Exception:
        return {}
    return kb if isinstance(kb, dict) else {}


def save_region_kb(ctx, kb):
    """定向 upsert region_kb（不整区重写，保留 created_at）。"""
    path = _db_path(ctx)
    if not path:
        raise RuntimeError("ledger db path unavailable")
    now = _now()
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) VALUES (?,?,?,?,?) "
            "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
            (ctx.region, "region_kb", json.dumps(kb, ensure_ascii=False), now, now),
        )
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------- ① settings prior

def _best_cell(table, min_n):
    best = None
    for name, v in (table or {}).items():
        if not isinstance(v, dict):
            continue
        n = int(v.get("n") or 0)
        if n < min_n:
            continue
        rate = float(v.get("rate") or 0.0)
        if best is None or rate > best[1]:
            best = (name, rate, n)
    return best


def _cast_like(current, value):
    """把先验格子名（字符串）转成与当前设置同类型（decay 是 int）。"""
    if isinstance(current, bool):
        return value
    if isinstance(current, int):
        try:
            return int(value)
        except (TypeError, ValueError):
            return value
    if isinstance(current, float):
        try:
            return float(value)
        except (TypeError, ValueError):
            return value
    return value


def settings_prior_recommendations(ctx, cfg=None):
    """按 gate_priors（库存实测优先，缺则 gate_priors_local）给出设置层推荐。

    返回 list[dict]：{dim, current, current_rate, current_n, recommended, rate, n, source, apply}
    apply=True 表示证据达标（n≥min_n 且 rate ≥ current_rate×min_lift）。不改 ctx。
    """
    cfg = dict(SETTINGS_PRIOR_DEFAULTS, **(cfg or {}))
    kb = load_region_kb(ctx)
    gp, source = kb.get("gate_priors"), "gate_priors"
    if not isinstance(gp, dict) or not gp:
        gp, source = kb.get("gate_priors_local"), "gate_priors_local"
    if not isinstance(gp, dict) or not gp:
        return []
    out = []
    for dim in cfg.get("dims") or []:
        table = gp.get(f"by_{dim}")
        if not isinstance(table, dict) or not table:
            continue
        current = ctx.settings.get(dim)
        cur_cell = table.get(str(current)) if current is not None else None
        cur_rate = float(cur_cell.get("rate") or 0.0) if isinstance(cur_cell, dict) else None
        cur_n = int(cur_cell.get("n") or 0) if isinstance(cur_cell, dict) else 0
        best = _best_cell(table, int(cfg.get("min_n", 30)))
        if not best:
            continue
        name, rate, n = best
        base = cur_rate if cur_rate is not None else float(cfg.get("floor_rate", 0.02))
        base = max(base, float(cfg.get("floor_rate", 0.02)))
        lift = rate / base if base > 0 else float("inf")
        rec = _cast_like(current, name)
        out.append({
            "dim": dim, "current": current, "current_rate": cur_rate, "current_n": cur_n,
            "recommended": rec, "rate": rate, "n": n, "lift": round(lift, 2),
            "source": source,
            "apply": (rec != current) and (lift >= float(cfg.get("min_lift", 2.0))),
        })
    return out


def apply_settings_prior(ctx, pinned=(), cfg=None, log=print):
    """把达标推荐写进 ctx.settings；pinned 维度（用户显式 --set/--neutralization）不动。

    返回实际改写的 list[dict]。关闭：thresholds.json `settings_prior.enabled=false`。
    """
    cfg = dict(SETTINGS_PRIOR_DEFAULTS, **(cfg or {}))
    if cfg.get("enabled") is False:
        log("[settings-prior] 已关闭（thresholds.settings_prior.enabled=false）")
        return []
    recs = settings_prior_recommendations(ctx, cfg)
    if not recs:
        log("[settings-prior] region_kb 无 gate_priors/gate_priors_local，跳过")
        return []
    applied = []
    for r in recs:
        cur_txt = (f"{r['current_rate']:.1%}(n={r['current_n']})"
                   if r["current_rate"] is not None else "无样本")
        if r["dim"] in set(pinned):
            log(f"[settings-prior] {r['dim']}={r['current']} 已被显式钉住，不改"
                f"（实测最优 {r['recommended']} {r['rate']:.1%} n={r['n']}）")
            continue
        if r["apply"]:
            ctx.settings[r["dim"]] = r["recommended"]
            applied.append(r)
            log(f"[settings-prior] {r['dim']} {r['current']}→{r['recommended']}："
                f"当前 {cur_txt} vs 实测 {r['rate']:.1%}(n={r['n']}) lift×{r['lift']}"
                f"（源 {r['source']}；显式 --set {r['dim']}=... 可钉住）")
        else:
            log(f"[settings-prior] {r['dim']}={r['current']} 保持：当前 {cur_txt}，"
                f"最优格 {r['recommended']} {r['rate']:.1%}(n={r['n']}) lift×{r['lift']} 未达 "
                f"min_lift={cfg.get('min_lift')}")
    return applied


# ---------------------------------------------------------------- ③ 波后刷新

def compute_local_gate_priors(ctx, sharpe_min=1.58, fitness_min=1.0):
    """用本地 backtest_results 重算条件过闸率（by_neutralization / by_operator_count /
    by_field_family）。pass 口径 = sharpe>sharpe_min 且 fitness>fitness_min 且无 RA failed checks。
    本地行不带 decay，故没有 by_decay——decay 维度仍以库存工具的 gate_priors 为准。"""
    path = _db_path(ctx)
    if not path:
        return {}
    conn = sqlite3.connect(path)
    try:
        rows = conn.execute(
            "SELECT sharpe, fitness, ra_failed_checks, payload_json FROM backtest_results "
            "WHERE region=? AND sharpe IS NOT NULL", (ctx.region,)
        ).fetchall()
    finally:
        conn.close()
    records = []
    for sharpe, fitness, ra_failed, payload in rows:
        try:
            p = json.loads(payload) if isinstance(payload, (str, bytes)) and payload else {}
        except Exception:
            p = {}
        code = p.get("code") or ""
        fails = ra_failed
        if isinstance(fails, str):
            try:
                fails = json.loads(fails)
            except Exception:
                fails = [fails] if fails else []
        passed = (float(sharpe or 0) > sharpe_min and float(fitness or 0) > fitness_min
                  and not fails)
        records.append({
            "passed": passed,
            "neutralization": p.get("neut"),
            "operator_count": _op_bin(_op_count(code)) if code else None,
            "field_family": _field_family(code) if code else None,
        })
    if not records:
        return {}

    def rate_table(key):
        agg = defaultdict(lambda: [0, 0])
        for r in records:
            k = r.get(key)
            if k in (None, ""):
                continue
            agg[str(k)][1] += 1
            if r["passed"]:
                agg[str(k)][0] += 1
        return {k: {"rate": round(p / t, 4), "n": t} for k, (p, t) in agg.items() if t >= MIN_CELL_N}

    return {
        "sample_size": len(records),
        "pass_rate": round(sum(1 for r in records if r["passed"]) / len(records), 4),
        "by_neutralization": rate_table("neutralization"),
        "by_operator_count": rate_table("operator_count"),
        "by_field_family": rate_table("field_family"),
        "generated_at": _now(),
        "source": "pipeline:stage_review (local backtest_results)",
    }


def refresh_after_wave(ctx, wave, rows, candidates, near, verdict=None, dataset=None, log=print):
    """波次关闭后刷新 region_kb：recent_waves 追加 + gate_priors_local 重算 + updated_at。"""
    kb = load_region_kb(ctx)
    best = max((float(r.get("sharpe") or 0.0) for r in rows), default=0.0)
    entry = {
        "wave": str(wave), "dataset": dataset, "n": len(rows),
        "candidates": len(candidates), "near": len(near),
        "best_sharpe": round(best, 3), "verdict": verdict, "at": _now(),
    }
    recent = [w for w in (kb.get("recent_waves") or []) if isinstance(w, dict)
              and str(w.get("wave")) != str(wave)]
    recent.append(entry)
    kb["recent_waves"] = recent[-RECENT_WAVES_CAP:]
    t = ctx.thresh("review") or {}
    local = compute_local_gate_priors(
        ctx, float(t.get("sharpe_min", 1.58) or 1.58), float(t.get("fitness_min", 1.0) or 1.0))
    if local:
        kb["gate_priors_local"] = local
    kb["updated_at"] = _now()[:10]
    save_region_kb(ctx, kb)
    log(f"[region_kb] 刷新：recent_waves+1（{wave} best={best:.2f} cand={len(candidates)}）"
        f"{' gate_priors_local n=' + str(local.get('sample_size')) if local else ''} updated_at={kb['updated_at']}")
    return kb
