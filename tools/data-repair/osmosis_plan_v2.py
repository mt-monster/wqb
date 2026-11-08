#!/usr/bin/env python
"""Osmosis 分配方案 v2 —— 相关性剪枝 + inv 衰减剔除 + USA(OS 选池) 纳入。

## 为什么需要 v2（2026-11-04 论坛/官方复核结论）

v1（`osmosis_allocate.py`）只做「按 inv 质量比例分 100k」，有三个与官方指南/论坛实证
不符的地方：

1. **无池内相关性剪枝**。官方 tip：`Use Alphas lists to evaluate intra-set correlations
   and eliminate Alphas that exhibit high mutual correlation`；论坛 HZ20306(23赞)/JX84394(61赞)
   均把「PnL 聚类去重、每簇留代表」视为核心。实测 v1 的 141 颗按 PnL 相关折算只有
   ≈30 个有效独立信号（GLB 22 颗只剩 3.1 个），`dailyOsmosisRank` 仅 0.35。
2. **未按 inv 衰减剔除**。官方 tip：`Exclude Alphas whose Sharpe ratio declines by
   approximately 60% or more after investability constraints are applied`。
   v1 只有绝对闸 `inv < 1.0`，实测 IND 有 9 颗（14.1% 点数）衰减 ≥60% 仍在池。
3. **USA 用纸面 inv 选池是错的**。USA 是唯一有真实 OS 的区（124 颗，`os.sharpe` 均值
   0.548）。按 inv 排序会把 OS 最高的那批（inv 全为 None，maxTrade=ON）整批漏掉。
   ⇒ USA 的权重口径改为 **os.sharpe**，门槛 `--usa-min-os`。

## 与 v1 的关系（2026-11-05 起 v1 已归档）

- v1 `osmosis_allocate.py` 的分配逻辑（`build_plan` / `replan` / CLI）**已删除**，文件归档在
  `attic/osmosis_v1_20261105/`。共用部分（平台池加载 / quality / apply_plan / zero_others /
  断点续跑）抽到 `osmosis_core.py`，本文件只保留 v2 的分配算法。
- 产出 `results/osmosis_plan_v2.json`；`results/osmosis_plan.json` 是**平台实际状态**的
  canonical 快照（由本工具写平台后回读重建）。
- 相关矩阵有 20h 磁盘缓存（`results/osmosis_corr_cache.json`）：首跑约 3 分钟，
  命中后 <5 秒。PnL 缺失时不再当「零相关」处理（旧实现会静默跳过剪枝）。

## 分配算法（每 scope 独立 100k）

1. 候选过滤：ACTIVE REGULAR（USA 额外要求 `os.sharpe >= --usa-min-os`）
2. 硬闸：`inv < --drop-inv-below` 剔除；`(is-inv)/is >= --decay-cut` 剔除；
   `TO > --turnover-cut` 且 `inv < --turnover-inv-min` 剔除
3. SA 池：按 inv 取每 scope topN（预算 `--sa-share`，单颗 `--sa-max`，超额回流 RA）
4. 相关性剪枝：SA 先固定为锚点；RA 按权重降序贪心接受，
   与已保留集合 `ρ >= --corr-cut` 丢弃，`ρ ∈ [--corr-soft, --corr-cut)` 保留但权重 ×`--soft-weight`
5. 若剪枝后 scope 内颗数 <10（平台硬要求），按权重回补被丢弃者（权重 ×0.25，标记 forced）
6. RA 池按权重点数化，最后 trim 到恰好 100,000

## 用法

    PYTHONPATH=world-quant-brain-mcp python tools/data-repair/osmosis_plan_v2.py
    PYTHONPATH=world-quant-brain-mcp python tools/data-repair/osmosis_plan_v2.py --scopes IND,KOR,GBR,GLB,DEU
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import statistics
import sys
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.join(_ROOT, "tools", "data-repair"))

import osmosis_core as core  # noqa: E402

RESULTS = os.path.join(_ROOT, "results")
OUT_PATH = os.path.join(RESULTS, "osmosis_plan_v2.json")
# ★ 平台侧「non-compensated」alpha 黑名单：这类 alpha 无法 PATCH 点数
# （400 "Cannot update Osmosis points for non-compensated alpha"），
# 每次 apply 失败后自动追加，下次规划直接排除，避免重复占位后又不达标。
BLACKLIST_PATH = os.path.join(RESULTS, "osmosis_noncompensated.json")


def load_blacklist() -> set:
    if not os.path.exists(BLACKLIST_PATH):
        return set()
    try:
        d = json.load(open(BLACKLIST_PATH, encoding="utf-8"))
        return set(d.get("ids", []) if isinstance(d, dict) else d)
    except Exception:
        return set()


def add_blacklist(ids) -> int:
    cur = load_blacklist()
    new = [i for i in ids if i not in cur]
    if not new:
        return 0
    cur |= set(new)
    json.dump({"ids": sorted(cur), "updated": time.strftime("%Y-%m-%dT%H:%M:%S")},
              open(BLACKLIST_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return len(new)
TARGET = 100_000
MIN_PER_SCOPE = 10
MIN_SCOPES = 3


# --------------------------------------------------------------------------- #
# 平台数据
# --------------------------------------------------------------------------- #
def build_pool() -> List[Dict[str, Any]]:
    core.PROD_POLICY = "ignore"          # 分配阶段不看 prod（用户 2026-10-21 定）
    return core.load_candidates_platform()


CORR_CACHE = os.path.join(RESULTS, "osmosis_corr_cache.json")


def _cache_key(ids: List[str], years: int) -> str:
    import hashlib
    h = hashlib.md5(("|".join(sorted(ids)) + f"|{years}").encode()).hexdigest()[:16]
    return h


def _load_corr_cache() -> Dict[str, Any]:
    if not os.path.exists(CORR_CACHE):
        return {}
    try:
        return json.load(open(CORR_CACHE, encoding="utf-8"))
    except Exception:
        return {}


def _save_corr_cache(cache: Dict[str, Any]) -> None:
    tmp = CORR_CACHE + ".tmp"
    json.dump(cache, open(tmp, "w", encoding="utf-8"))
    os.replace(tmp, CORR_CACHE)


async def _matrix_cached(ids: List[str], years: int = 4, ttl_hours: float = 20.0
                         ) -> Tuple[Dict[str, Dict[str, float]], List[str]]:
    """取池内相关矩阵，返回 (matrix, missing_ids)。

    ★ 2026-11-05 修正两个实测问题：
    1. **静默降级**：任一 alpha 的 PnL 取不到时，它只从矩阵里消失；调用方
       `row.get(x, 0.0)` 会把它当成「零相关」⇒ 剪枝被悄悄跳过（同一天三次跑
       GLB 分别得到 18/19/21 颗）。现显式返回 missing，并由 plan_scope 降权 + 告警。
    2. **重复取数**：每次跑都重新拉全部 PnL，实测偶发 10+ 分钟（空响应重试）。
       加 20h 磁盘缓存（`results/osmosis_corr_cache.json`），同日 review + plan 只算一次。
    """
    from brain_api import brain_client
    if not ids:
        return {}, []
    if len(ids) < 2:
        return {ids[0]: {ids[0]: 1.0}}, []

    key = _cache_key(ids, years)
    cache = _load_corr_cache()
    import time as _t
    hit = cache.get(key)
    if hit and (_t.time() - hit.get("ts", 0)) < ttl_hours * 3600:
        return hit.get("matrix") or {}, hit.get("missing") or []

    res = await brain_client.get_mutual_correlation(ids, threshold=0.9, years=years)
    mat = res.get("matrix") or {}
    missing = list(res.get("missing_pnl") or [])
    if not missing:
        missing = [i for i in ids if i not in mat]
    if mat:
        cache[key] = {"ts": _t.time(), "years": years, "n": len(ids),
                      "matrix": mat, "missing": missing}
        _save_corr_cache(cache)
    return mat, missing


# --------------------------------------------------------------------------- #
# 过滤
# --------------------------------------------------------------------------- #
def decay_of(a: Dict[str, Any]) -> Optional[float]:
    s, inv = a.get("sharpe"), a.get("investability_sharpe")
    if s is None or inv is None or s <= 0:
        return None
    return (s - inv) / s


def passes_filters(a: Dict[str, Any], args) -> Tuple[bool, str]:
    inv = a.get("investability_sharpe")
    if inv is not None and inv < args.drop_inv_below:
        return False, "inv<%g" % args.drop_inv_below
    d = decay_of(a)
    if d is not None and d >= args.decay_cut:
        return False, "inv衰减%.0f%%" % (d * 100)
    to = a.get("turnover")
    if to is not None and to > args.turnover_cut:
        # 官方：TO>20% 仅在「investability 后仍稳健」时才可保留。
        # 稳健证据二选一：inv >= 阈值，或（USA）真实 OS >= 1.0（OS 是费后 PnL，已含成本侵蚀）。
        osv = a.get("os_sharpe")
        robust = (inv is not None and inv >= args.turnover_inv_min) or                  (osv is not None and osv >= args.turnover_os_min)
        if not robust:
            return False, "TO>%.0f%%" % (args.turnover_cut * 100)
    return True, ""


def base_weight(a: Dict[str, Any], usa: bool) -> float:
    """权重口径：USA 用真实 OS sharpe（唯一可信的 OOS 证据）；其余用 v1 的 quality()。

    USA 的两种模式：
      * `--usa-min-os X>0`：硬门槛，只留 OS>=X（纯净但样本薄）
      * `--usa-min-os 0`：混合口径——有 OS 用 OS（负值压到 0.05），无 OS 用
        `0.75 × quality(inv)`（近期提交、OS 尚未累积的按纸面值打折参与，不独占权重）
    """
    if usa:
        v = a.get("os_sharpe")
        if v is not None:
            return max(float(v), 0.05)
        return 0.75 * core.quality(a)
    return core.quality(a)


# --------------------------------------------------------------------------- #
# 单 scope 规划
# --------------------------------------------------------------------------- #
def plan_scope(region: str, rows: List[Dict[str, Any]], mat: Dict[str, Dict[str, float]],
               args, log: Dict[str, Any]) -> List[Dict[str, Any]]:
    # 区域差异由共享层常量给出（数据层口径；ratchet 禁区内字面量分支）
    usa = region in core.OS_SHARPE_REGIONS
    ras = [r for r in rows if r.get("alpha_type") != "SUPER"]
    sas = [r for r in rows if r.get("alpha_type") == "SUPER"]

    # --- 1. 过滤 ---
    kept_c, dropped_filter = [], []
    for r in ras:
        if r["alpha_id"] in args._blacklist:
            dropped_filter.append((r["alpha_id"], "non_compensated"))
            continue
        if usa and args.usa_min_os > 0:
            osv = r.get("os_sharpe")
            if osv is None or osv < args.usa_min_os:
                dropped_filter.append((r["alpha_id"], "OS<%.2f" % args.usa_min_os))
                continue
        ok, why = passes_filters(r, args)
        (kept_c if ok else dropped_filter).append(
            r if ok else (r["alpha_id"], why))
    log["dropped_filter"] = dropped_filter

    weight = {r["alpha_id"]: base_weight(r, usa) for r in kept_c}
    kept_c = [r for r in kept_c if weight[r["alpha_id"]] > 0]

    # --- 2. SA 锚点（按 inv 取 topN）---
    sas_sorted = sorted(
        [s for s in sas if (s.get("investability_sharpe") or 0) > 0],
        key=lambda s: s.get("investability_sharpe") or 0, reverse=True)
    sa_keep = sas_sorted[: args.sa_top_n]
    log["sa_pool"] = len(sas_sorted)
    log["sa_dropped"] = [s["alpha_id"] for s in sas_sorted[args.sa_top_n:]]

    # --- 3. 相关性剪枝（SA 为锚，RA 贪心）---
    # ★ 相关未知（PnL 取不到）的 alpha **不能当作零相关**：保留但权重打折 + 显式记账。
    anchors = [s["alpha_id"] for s in sa_keep]
    kept_ra, dropped_corr, soft, unknown = [], [], {}, []
    for r in sorted(kept_c, key=lambda r: weight[r["alpha_id"]], reverse=True):
        rid = r["alpha_id"]
        row = mat.get(rid)
        if row is None:
            unknown.append(rid)
            weight[rid] *= args.corr_unknown_weight
            kept_ra.append(r)
            continue
        refs = anchors + [k["alpha_id"] for k in kept_ra]
        mc = max([row.get(x, 0.0) for x in refs], default=0.0)
        if mc >= args.corr_cut:
            dropped_corr.append((rid, round(mc, 3)))
            continue
        if mc >= args.corr_soft:
            soft[rid] = mc
            weight[rid] *= args.soft_weight
        kept_ra.append(r)
    log["dropped_corr"] = dropped_corr
    log["soft"] = soft
    log["corr_unknown"] = unknown
    if unknown:
        print(f"[warn] {region}: {len(unknown)} 颗无 PnL/相关数据，按未知相关处理（权重 ×{args.corr_unknown_weight}）"
              f"：{unknown[:8]}", file=sys.stderr)
    if any(a not in mat for a in anchors):
        print(f"[warn] {region}: SA 锚点缺相关行 -> 该 scope 的剪枝可能不完整", file=sys.stderr)

    # --- 3b. 数量上限（论坛实证：每区 15–20 颗优于铺满；OC2025 全量分析 62 赞）---
    log["dropped_cap"] = []
    if args.max_ra and len(kept_ra) > args.max_ra:
        kept_ra.sort(key=lambda r: weight[r["alpha_id"]], reverse=True)
        for r in kept_ra[args.max_ra:]:
            log["dropped_cap"].append((r["alpha_id"], round(weight[r["alpha_id"]], 3)))
        kept_ra = kept_ra[:args.max_ra]

    # --- 4. 不足 10 颗则回补（平台硬要求）---
    forced: List[str] = []
    if len(kept_ra) + len(sa_keep) < MIN_PER_SCOPE:
        need = MIN_PER_SCOPE - len(kept_ra) - len(sa_keep)
        pool = {r["alpha_id"]: r for r in kept_c}
        for rid, _ in sorted(dropped_corr, key=lambda t: -t[1])[::-1]:
            if need <= 0:
                break
            if rid not in pool:
                continue
            weight[rid] *= 0.25
            kept_ra.append(pool[rid])
            forced.append(rid)
            need -= 1
        log["forced"] = forced

    # --- 5. 点数 ---
    plan: List[Dict[str, Any]] = []
    sa_budget = int(round(TARGET * args.sa_share)) if sa_keep and kept_ra else (
        TARGET if sa_keep else 0)
    sa_alloc: Dict[str, int] = {}
    if sa_keep:
        sq = sum((s.get("investability_sharpe") or 0) for s in sa_keep) or 1.0
        for s in sa_keep:
            pts = int(round(sa_budget * (s.get("investability_sharpe") or 0) / sq))
            pts = max(1, min(args.sa_max, pts))
            sa_alloc[s["alpha_id"]] = pts
    ra_budget = TARGET - sum(sa_alloc.values())
    sq = sum(weight[r["alpha_id"]] for r in kept_ra) or 1.0

    # ★ REGULAR 单颗上限（2026-11-05 新增）：对齐论坛 DL61056(22赞) 的
    #   REGULAR_MAX_POINTS_PER_ALPHA=15,000。用途是护栏，不是当前约束——
    #   现有 6 scope 最大 REGULAR 恰为 10,000（DEU 2rmGAPqN）。薄池 + 单颗极高 inv
    #   时（如某 scope 只剩 10 颗、一颗 inv 4.9 其余 1.2）裸算可冲到 ~19,700 ⇒ 需要闸。
    #   超出的点数按「剩余容量」比例回流给同池其他 REGULAR，不蒸发。
    ra_pts: Dict[str, int] = {}
    for r in kept_ra:
        rid = r["alpha_id"]
        ra_pts[rid] = max(1, int(round(ra_budget * weight[rid] / sq)))
    cap_ra = args.regular_max_pts if args.regular_max_pts and args.regular_max_pts > 0 else 0
    if cap_ra:
        for _ in range(4):
            excess = sum(max(0, p - cap_ra) for p in ra_pts.values())
            if excess <= 0:
                break
            for k in ra_pts:
                ra_pts[k] = min(ra_pts[k], cap_ra)
            capacity = sum(cap_ra - p for p in ra_pts.values())
            if capacity <= 0:
                break
            for k in ra_pts:
                room = cap_ra - ra_pts[k]
                if room > 0:
                    ra_pts[k] += int(excess * room / capacity)
        log["ra_capped"] = [k for k, p in ra_pts.items() if p >= cap_ra]

    for s in sa_keep:
        plan.append({"region": region, "delay": s.get("delay") or 1, "alpha_id": s["alpha_id"],
                     "alpha_type": "SUPER", "pool": "SA", "points": sa_alloc[s["alpha_id"]],
                     "inv": s.get("investability_sharpe"), "os": s.get("os_sharpe"),
                     "prod": s.get("prod")})
    for r in kept_ra:
        rid = r["alpha_id"]
        plan.append({"region": region, "delay": r.get("delay") or 1, "alpha_id": rid,
                     "alpha_type": "REGULAR", "pool": "RA", "points": ra_pts[rid],
                     "inv": r.get("investability_sharpe"), "os": r.get("os_sharpe"),
                     "prod": r.get("prod"), "weight": round(weight[rid], 4),
                     "corr_max": round(soft.get(rid, 0.0), 3),
                     "forced": rid in forced})

    # --- 6. 精确 trim 到 100k（差额优先落在最大、且未触 REGULAR 上限的项）---
    diff = TARGET - sum(p["points"] for p in plan)
    if diff:
        cand = [p for p in plan
                if p["alpha_type"] != "SUPER" and (not cap_ra or p["points"] < cap_ra)]
        if not cand:
            cand = [p for p in plan if p["alpha_type"] != "SUPER"] or plan
        if diff > 0:
            top = max(cand, key=lambda p: p["points"])
            add = diff if not cap_ra else min(diff, max(0, cap_ra - top["points"]))
            top["points"] += add
            diff -= add
            # 仍有剩余（全部触顶）⇒ 均摊给最小项，宁可略微超限也不让 scope 不足 100k
            if diff > 0:
                pool = [p for p in plan if p["alpha_type"] != "SUPER"] or plan
                pool.sort(key=lambda p: p["points"])
                pool[0]["points"] += diff
        else:
            top = max(cand, key=lambda p: p["points"])
            top["points"] = max(1, top["points"] + diff)
    log["n_total"] = len(plan)
    return plan


def corr_stats(ids: List[str], mat: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """池内相关的三个决策指标：平均/最大相关、>0.7 对数、n_eff。"""
    if len(ids) < 2:
        return {"mean": 0.0, "max": 0.0, "pairs07": 0, "neff": float(len(ids))}
    vals = []
    for i, a in enumerate(ids):
        row = mat.get(a) or {}
        for b in ids[i + 1:]:
            if b in row:
                vals.append(row[b])
    if not vals:
        return {"mean": 0.0, "max": 0.0, "pairs07": 0, "neff": float(len(ids))}
    return {"mean": round(statistics.mean(vals), 3), "max": round(max(vals), 3),
            "pairs07": sum(1 for v in vals if v > 0.70),
            "neff": round(len(ids) ** 2 / (len(ids) + 2 * sum(vals)), 1)}


def neff(ids: List[str], mat: Dict[str, Dict[str, float]]) -> float:
    if len(ids) < 2:
        return float(len(ids))
    vals = []
    for i, a in enumerate(ids):
        row = mat.get(a) or {}
        for b in ids[i + 1:]:
            if b in row:
                vals.append(row[b])
    if not vals:
        return float(len(ids))
    return len(ids) ** 2 / (len(ids) + 2 * sum(vals))


# --------------------------------------------------------------------------- #
# CLI / 编排
# --------------------------------------------------------------------------- #
def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Osmosis 分配 v2（相关性剪枝 + 衰减闸 + 数量收敛 + 单颗封顶）")
    ap.add_argument("--scopes", default="IND,KOR,GBR,GLB,DEU,USA")
    ap.add_argument("--out", default=OUT_PATH)
    ap.add_argument("--corr-cut", type=float, default=0.70)
    ap.add_argument("--corr-soft", type=float, default=0.60)
    ap.add_argument("--corr-unknown-weight", type=float, default=0.50,
                    help="PnL 缺失、相关未知的 alpha 权重折扣（不当零相关处理）")
    ap.add_argument("--soft-weight", type=float, default=0.50)
    ap.add_argument("--decay-cut", type=float, default=0.60)
    ap.add_argument("--drop-inv-below", type=float, default=1.0)
    ap.add_argument("--turnover-cut", type=float, default=0.20)
    ap.add_argument("--turnover-inv-min", type=float, default=1.5)
    ap.add_argument("--turnover-os-min", type=float, default=1.0)
    ap.add_argument("--usa-min-os", type=float, default=0.0)
    ap.add_argument("--max-ra", type=int, default=20,
                    help="每 scope REGULAR 颗数上限（0=不限）。论坛实证 15–20 优于铺满")
    ap.add_argument("--sa-top-n", type=int, default=4)
    ap.add_argument("--sa-share", type=float, default=0.22)
    ap.add_argument("--sa-max", type=int, default=10_000)
    ap.add_argument("--regular-max-pts", type=int, default=15_000,
                    help="单颗 REGULAR 点数上限（默认 15000，对齐论坛 DL61056；0=不限）")
    ap.add_argument("--years", type=int, default=4)
    ap.add_argument("--apply", action="store_true", help="写入平台（默认只出 plan）")
    ap.add_argument("--no-zero", action="store_true",
                    help="只 PATCH 计划内 alpha，不零化计划外（分区重排必须加，否则会清空其他 scope）")
    ap.add_argument("--dry-run", action="store_true", help="与 --apply 同用：只预览不写")
    ap.add_argument("--force-repatch", action="store_true",
                    help="清空 checkpoint，强制重写全部（点数值有变更时必须带）")
    return ap


def make_plan(pool: List[Dict[str, Any]], want: List[str], args
              ) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    """按 scope 列表生成计划，返回 (plan, logs, mats)。

    ★ 供 CLI 与只读诊断工具复用（`review_osmosis_best.py` 用它算「应有方案」），
    避免各脚本各自维护一份分配算法（v1 的教训）。
    """
    # ★ 强制 ignore prod：调用方（如 review_osmosis_best）可能把全局 PROD_POLICY 设成
    #   exclude/discount 用于自己的展示；那会让 quality() 打折，导致同一池算出不同方案
    #   （实测 GLB 18 vs 19 的差异就来自这里）。分配口径与调用方状态解耦。
    core.PROD_POLICY = "ignore"

    by_reg: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in pool:
        by_reg[r["region"]].append(r)

    plan: List[Dict[str, Any]] = []
    logs: Dict[str, Dict[str, Any]] = {}
    mats: Dict[str, Dict[str, Dict[str, float]]] = {}
    for reg in want:
        rows = by_reg.get(reg) or []
        ids = [r["alpha_id"] for r in rows]
        mat, missing = (asyncio.run(_matrix_cached(ids, args.years)) if len(ids) >= 2
                        else ({}, []))
        if missing:
            print(f"[warn] {reg}: 相关矩阵缺 {len(missing)}/{len(ids)} 颗（PnL 取不到）：{missing[:8]}",
                  file=sys.stderr)
        log_missing = missing
        mats[reg] = mat
        log: Dict[str, Any] = {}
        sel = plan_scope(reg, rows, mat, args, log)
        sel_ids = [p["alpha_id"] for p in sel]
        log["n_before"] = len(rows)
        log["missing_pnl"] = log_missing
        log["before"] = corr_stats(ids, mat)
        log["after"] = corr_stats(sel_ids, mat)
        log["neff_before"] = log["before"]["neff"]
        log["neff_after"] = log["after"]["neff"]
        logs[reg] = log
        plan.extend(sel)
        print(f"[{reg}] 候选 {len(rows)} → 计划 {len(sel)} 颗 / "
              f"{sum(p['points'] for p in sel):,} 点 | n_eff {log['neff_before']} → {log['neff_after']} "
              f"| 剔除: 硬闸 {len(log['dropped_filter'])} / 相关 {len(log['dropped_corr'])} "
              f"| soft降权 {len(log['soft'])} | forced {len(log.get('forced', []))}",
              file=sys.stderr)
    return plan, logs, mats


def print_summary(plan: List[Dict[str, Any]], want: List[str], logs: Dict[str, Any]) -> None:
    print("\nscope  n   点数      SA颗 SA合计 SA最大 | n_eff 前→后")
    for r in want:
        ps = [p for p in plan if p["region"] == r]
        sa = [p for p in ps if p["alpha_type"] == "SUPER"]
        print(f"{r:5} {len(ps):3} {sum(p['points'] for p in ps):>8,} "
              f"{len(sa):4} {sum(p['points'] for p in sa):>7,} "
              f"{max([p['points'] for p in sa], default=0):>6,} | "
              f"{logs[r]['neff_before']}→{logs[r]['neff_after']}")
    print(f"合计  {len(plan):3} {sum(p['points'] for p in plan):>8,}")


def main() -> int:
    args = build_arg_parser().parse_args()
    args._blacklist = load_blacklist()
    want = [s.strip().upper() for s in args.scopes.split(",") if s.strip()]

    pool = build_pool()
    plan, logs, _mats = make_plan(pool, want, args)

    # 校验
    tgt = {r: [p for p in plan if p["region"] == r] for r in want}
    bad = [r for r, ps in tgt.items() if sum(p["points"] for p in ps) != TARGET]
    thin = [r for r, ps in tgt.items() if len(ps) < MIN_PER_SCOPE]
    if bad:
        print(f"❌ scope 点数不等于 100k: {bad}", file=sys.stderr)
    if thin:
        print(f"❌ scope 少于 10 颗: {thin}", file=sys.stderr)
    if len(want) < MIN_SCOPES:
        print("❌ scope 数 <3", file=sys.stderr)

    json.dump(plan, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    if args.apply:
        if args.force_repatch and os.path.exists(core.CKPT_PATH):
            os.remove(core.CKPT_PATH)
            print(f"[ckpt] 已清空 {core.CKPT_PATH}（强制重写全部）", file=sys.stderr)
        ok, skip, fail, failures, _applied = asyncio.run(core.apply_plan(plan, dry_run=args.dry_run))
        print(f"[patch] OK={ok} 跳过={skip} 失败={fail}", file=sys.stderr)
        if failures:
            for k, v in failures.items():
                print(f"  失败[{k}]: {len(v)} 颗 -> {v[:10]}", file=sys.stderr)
            if failures.get("non_compensated"):
                n = add_blacklist(failures["non_compensated"])
                print(f"[blacklist] 新增 {n} 颗 non-compensated -> {BLACKLIST_PATH}", file=sys.stderr)
        if not args.dry_run and not args.no_zero:
            z_ok, z_fb, z_err = asyncio.run(core.zero_others(pool, plan, False))
            print(f"[zero] 非计划 alpha 清零: null成功={z_ok} 回退1={z_fb} 失败={z_err}", file=sys.stderr)

    meta = {"scopes": want,
            "args": {k: v for k, v in vars(args).items() if not k.startswith("_")},
            "logs": logs}
    json.dump(meta, open(args.out.replace(".json", "_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nplan v2 -> {args.out}", file=sys.stderr)

    print_summary(plan, want, logs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
