# -*- coding: utf-8 -*-
"""组合证据：从 data/wqb.db 只读汇总「区域 × 类别」的回测与判死 / 胜绩，写进 cells.json 的 evidence 块（2026-10-04）。

为什么要「推断绑定」：registry 的 win / dead_end 有六成多没有 `payload.dataset`，按 payload 只能把三成多
的条目归到类别。这里在**不写库**的前提下按条目 id / family 文本推断数据集（`PV106` → pv106、`FND93` →
fundamental93、`ANALYST-CONSENSUS` → analyst_consensus），推断不出数据集再按类别关键词归类；每条都标
`bound`（payload / inferred / keyword），给人看时区分清楚。真正的回填（写库）另行由用户批准。
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .cells import load_cells, save_cells
from .taxonomy import category_from_prefix, expand_abbrev, normalize_category

#: 条目 id / family 里的类别关键词（token 开头匹配，其后只能是数字或空）
_KEYWORDS: List[Tuple[str, str]] = [
    ("SOCIALMEDIA", "socialmedia"), ("SENTIMENT", "sentiment"), ("SENT", "sentiment"), ("NEWS", "news"),
    ("ANALYST", "analyst"), ("ANL", "analyst"), ("OPTION", "option"), ("INSIDERS", "insiders"),
    ("INSIDER", "insiders"), ("INSD", "insiders"), ("INSTITUTIONS", "institutions"), ("INST", "institutions"),
    ("MODEL", "model"), ("MDL", "model"), ("IPV", "pv"), ("PV", "pv"), ("RISK", "risk"), ("RSK", "risk"),
    ("SHORTINTEREST", "shortinterest"), ("SHORT", "shortinterest"), ("SI", "shortinterest"),
    ("EARNINGS", "earnings"), ("ERN", "earnings"), ("FUNDAMENTAL", "fundamental"), ("FND", "fundamental"),
    ("FUND", "fundamental"), ("OTHER", "other"), ("OTH", "other"), ("MACRO", "macro"), ("MCR", "macro"),
    ("IMBALANCE", "imbalance"), ("IMB", "imbalance"),
]


def _connect(db: Optional[str]):
    from wqb.db_conn import connect, default_db_path
    path = db or default_db_path()
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    return connect(path, readonly=True, timeout=10.0)


def _region_datasets(conn, region: str) -> Dict[str, str]:
    """本区 datasets 表：name（小写）→ 平台类别。

    本区该行类别为空时，先借同名数据集在别区的平台类别（182 个空类别里 58 个可这样补），再退前缀推断。
    """
    elsewhere: Dict[str, str] = {}
    for name, cat in conn.execute(
            "SELECT name, category FROM datasets WHERE category IS NOT NULL AND category != '' ORDER BY id"):
        if name:
            elsewhere[str(name).lower()] = normalize_category(cat)
    out: Dict[str, str] = {}
    for name, cat in conn.execute(
            "SELECT d.name, d.category FROM datasets d JOIN regions g ON g.id = d.region_id WHERE g.name = ?",
            (region,)):
        if not name:
            continue
        low = str(name).lower()
        c = normalize_category(cat)
        if c == "unknown":
            c = elsewhere.get(low) or normalize_category(category_from_prefix(low) or "other")
        out[low] = c
    return out


def _cat_of_dataset(ds: str, table: Dict[str, str]) -> str:
    """数据集 → 类别；回测行没写数据集（历史行 dataset 为空）返回 unknown，不并进任何组合。"""
    low = (ds or "").strip().lower()
    if not low or low in ("?", "none", "null"):
        return "unknown"
    if low in table:
        return table[low]
    return normalize_category(category_from_prefix(low) or "other")


def region_stats(region: str, db: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """本区按类别的回测 / RA 全过 / prod 统计（只读）。"""
    from wqb.config import GATES_PLATFORM, PRODCORR_CEILING
    region = region.upper()
    s_min, f_min = float(GATES_PLATFORM["sharpe_min"]), float(GATES_PLATFORM["fitness_min"])
    stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "backtests": 0, "ra_clean": 0, "prod_measured": 0, "prod_clean": 0, "prod_blocked": 0,
        "datasets": defaultdict(int)})
    conn = _connect(db)
    try:
        table = _region_datasets(conn, region)
        for ds, sharpe, fitness, ra in conn.execute(
                "SELECT dataset, sharpe, fitness, ra_failed_checks FROM backtest_results WHERE upper(region) = ?",
                (region,)):
            cat = _cat_of_dataset(ds or "", table)
            st = stats[cat]
            st["backtests"] += 1
            st["datasets"][str(ds or "?")] += 1
            try:
                failed = json.loads(ra) if ra else []
            except (TypeError, ValueError):
                failed = ["?"]
            if (sharpe is not None and float(sharpe) >= s_min and fitness is not None
                    and float(fitness) >= f_min and not failed):
                st["ra_clean"] += 1
        for ds, pc in conn.execute(
                "SELECT d.name, a.prod_correlation FROM alphas a JOIN regions g ON g.id = a.region_id "
                "LEFT JOIN datasets d ON d.id = a.dataset_id WHERE g.name = ? AND a.prod_correlation IS NOT NULL",
                (region,)):
            cat = _cat_of_dataset(ds or "", table)
            st = stats[cat]
            st["prod_measured"] += 1
            if float(pc) < float(PRODCORR_CEILING):
                st["prod_clean"] += 1
            else:
                st["prod_blocked"] += 1
    finally:
        conn.close()
    return {c: dict(v, datasets=dict(v["datasets"])) for c, v in stats.items()}


def _tokens(*texts: str) -> List[str]:
    toks: List[str] = []
    for t in texts:
        toks += [x for x in re.split(r"[^A-Za-z0-9]+", str(t or "")) if x]
    return toks


def _infer(entry_id: str, family: str, table: Dict[str, str]) -> Tuple[Optional[str], Optional[str], str]:
    """(dataset, category, bound)：先认数据集名（含 2–3 词连写与缩写），再认类别关键词。"""
    toks = _tokens(entry_id, family)
    low = [t.lower() for t in toks]
    for n in (3, 2, 1):
        for i in range(len(low) - n + 1):
            cand = "_".join(low[i:i + n])
            if cand in table:
                return cand, table[cand], "inferred"
            if n == 1:
                ex = expand_abbrev(cand)
                if ex and ex in table:
                    return ex, table[ex], "inferred"
    for t in toks:
        up = t.upper()
        for kw, cat in _KEYWORDS:
            if up.startswith(kw) and (up[len(kw):].isdigit() or up[len(kw):] == ""):
                return None, cat, "keyword"
    return None, None, "unbound"


def registry_entries(region: str, db: Optional[str] = None) -> List[Dict[str, Any]]:
    """本区 win / dead_end 条目，带类别归属（payload.dataset > 推断数据集 > 关键词）。"""
    region = region.upper()
    out: List[Dict[str, Any]] = []
    conn = _connect(db)
    try:
        table = _region_datasets(conn, region)
        for layer, entry_id, family, payload in conn.execute(
                "SELECT layer, entry_id, family, payload FROM registry_empirical "
                "WHERE upper(region) = ? AND layer IN ('dead_end', 'win') ORDER BY layer, entry_id", (region,)):
            try:
                p = json.loads(payload) if payload else {}
            except (TypeError, ValueError):
                p = {}
            if not isinstance(p, dict):
                p = {}
            ds = p.get("dataset")
            if not ds and isinstance(p.get("datasets"), list) and p["datasets"]:
                ds = p["datasets"][0]
            if isinstance(ds, (list, tuple)):
                ds = ds[0] if ds else None
            if ds:
                ds_low = str(ds).lower()
                cat, bound = _cat_of_dataset(ds_low, table), "payload"
            else:
                ds_low, cat, bound = _infer(str(entry_id or p.get("id") or ""), str(family or p.get("family") or ""), table)
            text = p.get("rule") if layer == "dead_end" else p.get("key")
            out.append({
                "layer": layer, "id": entry_id or p.get("id"),
                "family": (family or p.get("family") or p.get("what") or "")[:120],
                "text": str(text or p.get("reason") or "")[:160],
                "dataset": ds_low, "category": cat, "bound": bound,
            })
    finally:
        conn.close()
    return out


def sync_cells(region: str, *, db: Optional[str] = None, config_dir: Optional[Path] = None,
               apply: bool = False, min_backtests: int = 20, today: Optional[str] = None) -> Dict[str, Any]:
    """把只读汇总的证据写进 cells.json 的 evidence 块（不碰人写的 backtest / thresholds / generation / s4）。

    组合的建档线：本区该类别回测 ≥ min_backtests，或有任何（绑定 / 推断）判死 / 胜绩条目，或文件里已有。
    """
    region = region.upper()
    stats = region_stats(region, db)
    entries = registry_entries(region, db)
    data = load_cells(region, config_dir)
    data.setdefault("schema_version", 1)
    data["region"] = region
    cells = data.setdefault("cells", {})
    by_cat: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    unbound = 0
    for e in entries:
        if e["category"]:
            by_cat[e["category"]].append(e)
        else:
            unbound += 1
    unattributed = (stats.pop("unknown", None) or {}).get("backtests", 0)
    wanted = ({c for c, s in stats.items() if s["backtests"] >= min_backtests} | set(by_cat) | set(cells)) - {"unknown"}
    added = sorted(wanted - set(cells))
    day = today or _dt.date.today().isoformat()
    for cat in sorted(wanted):
        cell = cells.setdefault(cat, {"status": "auto"})
        st = stats.get(cat) or {"backtests": 0, "ra_clean": 0, "prod_measured": 0, "prod_clean": 0,
                                "prod_blocked": 0, "datasets": {}}
        top = sorted(st["datasets"].items(), key=lambda kv: -kv[1])
        ents = by_cat.get(cat, [])
        cell["datasets"] = sorted({d for d, _ in top} | {e["dataset"] for e in ents if e.get("dataset")})
        cell["evidence"] = {
            "synced_at": day,
            "backtests": st["backtests"], "ra_clean": st["ra_clean"],
            "prod_measured": st["prod_measured"], "prod_clean": st["prod_clean"], "prod_blocked": st["prod_blocked"],
            "top_datasets": [{"dataset": d, "backtests": n} for d, n in top[:8]],
            "dead_ends": [{k: e[k] for k in ("id", "family", "text", "dataset", "bound")}
                          for e in ents if e["layer"] == "dead_end"],
            "wins": [{k: e[k] for k in ("id", "family", "text", "dataset", "bound")}
                     for e in ents if e["layer"] == "win"],
        }
    data["evidence_synced_at"] = day
    data["unbound_registry_entries"] = unbound
    data["unattributed_backtests"] = unattributed
    summary = {"region": region, "cells": sorted(wanted), "added": added, "unbound_registry_entries": unbound,
               "unattributed_backtests": unattributed, "applied": False}
    if apply:
        summary["path"] = str(save_cells(region, data, config_dir))
        summary["applied"] = True
    summary["data"] = data
    return summary


def matrix(regions: Optional[List[str]] = None, db: Optional[str] = None) -> List[Dict[str, Any]]:
    """全区域 × 类别证据矩阵（只读），供审计与选区参考。"""
    from wqb.config import REGIONS
    rows: List[Dict[str, Any]] = []
    for r in regions or sorted(REGIONS):
        try:
            stats = region_stats(r, db)
            ents = registry_entries(r, db)
        except FileNotFoundError:
            break
        cnt: Dict[str, Dict[str, int]] = defaultdict(lambda: {"dead": 0, "win": 0})
        for e in ents:
            if e["category"]:
                cnt[e["category"]]["dead" if e["layer"] == "dead_end" else "win"] += 1
        for c in sorted(set(stats) | set(cnt)):
            s = stats.get(c) or {}
            rows.append({"region": r, "category": c, "backtests": s.get("backtests", 0),
                         "ra_clean": s.get("ra_clean", 0), "prod_clean": s.get("prod_clean", 0),
                         "dead": cnt[c]["dead"], "win": cnt[c]["win"]})
    return rows
