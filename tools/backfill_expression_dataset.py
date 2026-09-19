#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backfill_expression_dataset.py — 修复 expressions.dataset 被写成 region 名的污染行。

背景（2026-09-15 审计）：`upsert_expressions` 的 SELECT 曾把 `name` 列重复选入，
导致 `expressions.dataset` 落成 region 名（如 'GBR'）。全库 7,434/13,855 行（54%）
受影响，`get_mining_yield(by_dataset=True)` 与 `campaign_intel s0-select` 的
`hist_yield_rate` 因此对一半样本失明。写入侧已于 2026-09-15 修复，本工具只做存量回填。

解析顺序（确定性、可复现；命中即停，不猜）：
  1. waves → datasets：`expressions.wave_id` → `waves.dataset_id` → `datasets.name`
     （跳过 name 仍等于 region 的伪数据集行，如 datasets#1822 'KOR'）
  2. wave 标签：`s2_<dataset>_d<delay>`
  3. gate_results：同 (region, wave) 只有一个 distinct dataset 时采用
  4. 其余 → dataset=NULL（"未知"比"等于 region 名"诚实；`by_dataset` 会归入 null 桶）

幂等：只处理 `dataset = region` 的行；重复运行无副作用。

用法：
    python tools/backfill_expression_dataset.py              # 干跑：只统计不写
    python tools/backfill_expression_dataset.py --apply      # 先备份再写
    python tools/backfill_expression_dataset.py --db path/to.db --apply
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(REPO_ROOT, "data", "wqb.db")
WAVE_LABEL_RE = re.compile(r"^s2_(.+)_d\d+$")


def plan(conn: sqlite3.Connection):
    """返回 (updates: list[(id, dataset|None, source)], stats: dict)。"""
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT id, region, wave, wave_id FROM expressions WHERE dataset IS NOT NULL AND dataset = region"
    ).fetchall()
    stats = {"polluted": len(rows), "waves_datasets": 0, "wave_label": 0, "gate_results": 0, "null": 0}
    updates = []
    # 预取 gate_results 的 (region, wave) → 唯一 dataset
    gate_map = {}
    for region, wave, n_ds, ds in cur.execute(
        "SELECT region, wave, COUNT(DISTINCT dataset), MIN(dataset) FROM gate_results "
        "WHERE dataset IS NOT NULL AND dataset != '' GROUP BY region, wave"
    ):
        if n_ds == 1 and ds and ds != region:
            gate_map[(region, str(wave))] = ds
    for eid, region, wave, wave_id in rows:
        ds = None
        src = "null"
        if wave_id is not None:
            r = cur.execute(
                "SELECT d.name FROM waves w JOIN datasets d ON d.id = w.dataset_id WHERE w.id = ?",
                (wave_id,),
            ).fetchone()
            if r and r[0] and r[0] != region:
                ds, src = r[0], "waves_datasets"
        if ds is None and wave:
            m = WAVE_LABEL_RE.match(str(wave))
            if m and m.group(1) != region:
                ds, src = m.group(1), "wave_label"
        if ds is None and wave:
            g = gate_map.get((region, str(wave)))
            if g:
                ds, src = g, "gate_results"
        stats[src] += 1
        updates.append((eid, ds, src))
    return updates, stats


def apply(conn: sqlite3.Connection, updates) -> int:
    cur = conn.cursor()
    now = dt.datetime.now().isoformat(timespec="seconds")
    n = 0
    for eid, ds, _src in updates:
        cur.execute(
            "UPDATE expressions SET dataset = ?, updated_at = ? WHERE id = ? AND dataset = region",
            (ds, now, eid),
        )
        n += cur.rowcount
    conn.commit()
    return n


def plan_backtests(conn: sqlite3.Connection):
    """backtest_results.dataset 缺失/等于 region 的行 → 从 expressions / wave 标签 / gate_results 解析。

    `get_mining_yield(by_dataset=True)` 的 backtested 计数按 backtest_results 自身的
    dataset 列分组，expressions 修好了它没修等于白修（GBR 实测 327 条回测 81 条落在 null 桶）。
    """
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT id, region, wave, expression_id, alpha_id FROM backtest_results "
        "WHERE dataset IS NULL OR dataset = '' OR dataset = region"
    ).fetchall()
    stats = {"missing": len(rows), "expression_id": 0, "alpha_id": 0, "wave_label": 0,
             "gate_results": 0, "unresolved": 0}
    gate_map = {}
    for region, wave, n_ds, ds in cur.execute(
        "SELECT region, wave, COUNT(DISTINCT dataset), MIN(dataset) FROM gate_results "
        "WHERE dataset IS NOT NULL AND dataset != '' GROUP BY region, wave"
    ):
        if n_ds == 1 and ds and ds != region:
            gate_map[(region, str(wave))] = ds
    updates = []
    for bid, region, wave, expression_id, alpha_id in rows:
        ds, src = None, "unresolved"
        if expression_id is not None:
            r = cur.execute(
                "SELECT dataset FROM expressions WHERE id = ? AND dataset IS NOT NULL "
                "AND dataset != '' AND dataset != region", (expression_id,)).fetchone()
            if r:
                ds, src = r[0], "expression_id"
        if ds is None and alpha_id:
            r = cur.execute(
                "SELECT dataset FROM expressions WHERE alpha_id = ? AND dataset IS NOT NULL "
                "AND dataset != '' AND dataset != region ORDER BY id DESC LIMIT 1", (alpha_id,)).fetchone()
            if r:
                ds, src = r[0], "alpha_id"
        if ds is None and wave:
            m = WAVE_LABEL_RE.match(str(wave))
            if m and m.group(1) != region:
                ds, src = m.group(1), "wave_label"
        if ds is None and wave:
            g = gate_map.get((region, str(wave)))
            if g:
                ds, src = g, "gate_results"
        stats[src] += 1
        if ds is not None:
            updates.append((bid, ds, src))
    return updates, stats


def apply_backtests(conn: sqlite3.Connection, updates) -> int:
    cur = conn.cursor()
    n = 0
    for bid, ds, _src in updates:
        cur.execute(
            "UPDATE backtest_results SET dataset = ? WHERE id = ? "
            "AND (dataset IS NULL OR dataset = '' OR dataset = region)", (ds, bid))
        n += cur.rowcount
    conn.commit()
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description="回填 expressions.dataset 污染行（默认干跑）")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--apply", action="store_true", help="真正写库（先自动备份）")
    ap.add_argument("--report", default=None, help="把逐行计划写成 JSON（默认不写）")
    a = ap.parse_args()
    if not os.path.isfile(a.db):
        print(f"[error] db not found: {a.db}")
        return 2
    conn = sqlite3.connect(a.db)
    try:
        updates, stats = plan(conn)
        print(f"[plan] expressions: polluted={stats['polluted']} → waves_datasets={stats['waves_datasets']} "
              f"wave_label={stats['wave_label']} gate_results={stats['gate_results']} "
              f"unresolved→NULL={stats['null']}")
        bt_updates, bt_stats = plan_backtests(conn)
        print(f"[plan] backtest_results: missing={bt_stats['missing']} → expression_id={bt_stats['expression_id']} "
              f"alpha_id={bt_stats['alpha_id']} wave_label={bt_stats['wave_label']} "
              f"gate_results={bt_stats['gate_results']} unresolved(留空)={bt_stats['unresolved']}")
        if a.report:
            with open(a.report, "w", encoding="utf-8") as f:
                json.dump({"stats": stats, "updates": updates,
                           "backtest_stats": bt_stats, "backtest_updates": bt_updates},
                          f, ensure_ascii=False, indent=1)
            print(f"[plan] report -> {a.report}")
        if not a.apply:
            print("[dry-run] 未写库；加 --apply 执行")
            return 0
        if not updates and not bt_updates:
            print("[apply] 无需处理")
            return 0
        conn.close()
        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = f"{a.db}.bak_dataset_backfill_{stamp}"
        shutil.copy2(a.db, backup)
        print(f"[backup] {backup}")
        conn = sqlite3.connect(a.db)
        n = apply(conn, updates)
        left = conn.execute(
            "SELECT COUNT(*) FROM expressions WHERE dataset IS NOT NULL AND dataset = region"
        ).fetchone()[0]
        print(f"[apply] expressions updated={n} remaining_polluted={left}")
        nb = apply_backtests(conn, bt_updates)
        left_bt = conn.execute(
            "SELECT COUNT(*) FROM backtest_results WHERE dataset IS NULL OR dataset = '' OR dataset = region"
        ).fetchone()[0]
        print(f"[apply] backtest_results updated={nb} remaining_missing={left_bt}（无法解析者保持 NULL）")
        return 0 if left == 0 else 1
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
