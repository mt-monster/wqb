#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backfill_backtest_dataset.py — 回填 backtest_results.dataset 为 NULL 的历史行（只填空，不覆盖）。

背景（2026-09-19）：`pipeline.py` 两处 `save_backtest_results(region, wave, rows)` 从未传 dataset，
store 侧 `upsert_backtest_rows(..., dataset=None)` 落库即 NULL —— 实测 4505 行里 928 行为 NULL
（IND 322 / MEA 379 / USA 117 / EUR 58 / JPN 40 / KOR 12）。后果：`get_mining_yield(by_dataset=True)`
与 `campaign_intel s0-select` 的按集产出率把当天刚跑完的集显示为"从未回测"（IND w170-175 七集
197 条全部不可见），选集先验失真。pipeline 已修（传 dataset=ck["dataset"]），本工具补历史。

回填来源（按优先级，取第一个可用且不等于区域名 / '_unknown' 的）：
  1. expressions.dataset（经 backtest_results.expression_id）——但 2026-09-15 前有 ~7.4k 行被写成
     区域名（memory: gbr-campaign-state），等于 region 的值视为无效；
  2. waves.dataset_id → datasets.name（经 expressions.wave_id）。

用法:
    python tools/backfill_backtest_dataset.py --dry-run      # 只报告可回填数
    python tools/backfill_backtest_dataset.py                # 执行（只 UPDATE dataset IS NULL 的行）
    python tools/backfill_backtest_dataset.py --region IND   # 限定区域
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.environ.get("WQB_DB_PATH") or os.path.join(REPO_ROOT, "data", "wqb.db")

SQL_RESOLVE = """
SELECT b.id, b.region,
       CASE WHEN e.dataset IS NOT NULL AND e.dataset<>'' AND e.dataset<>b.region THEN e.dataset END AS via_expr,
       CASE WHEN d.name IS NOT NULL AND d.name<>'_unknown' AND d.name<>b.region THEN d.name END AS via_wave
FROM backtest_results b
LEFT JOIN expressions e ON e.id=b.expression_id
LEFT JOIN waves w ON w.id=e.wave_id
LEFT JOIN datasets d ON d.id=w.dataset_id
WHERE b.dataset IS NULL {region_filter}
"""


def resolve(conn, region=None):
    rf = "AND b.region=?" if region else ""
    cur = conn.execute(SQL_RESOLVE.format(region_filter=rf), (region,) if region else ())
    plan = []
    for bid, reg, via_expr, via_wave in cur.fetchall():
        ds = via_expr or via_wave
        if ds:
            plan.append((bid, reg, ds, "expr" if via_expr else "wave"))
    return plan


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    conn = sqlite3.connect(a.db)
    total_null = conn.execute(
        "SELECT COUNT(*) FROM backtest_results WHERE dataset IS NULL" + (" AND region=?" if a.region else ""),
        (a.region,) if a.region else ()).fetchone()[0]
    plan = resolve(conn, a.region)
    by_src = {}
    for _, reg, ds, src in plan:
        by_src[(reg, src)] = by_src.get((reg, src), 0) + 1
    print(f"[backfill] dataset IS NULL 行: {total_null}；可回填: {len(plan)}；不可回填: {total_null - len(plan)}")
    for (reg, src), n in sorted(by_src.items()):
        print(f"  {reg:5s} via {src:4s}: {n}")
    if a.dry_run or not plan:
        print("[backfill] dry-run，未写库" if a.dry_run else "[backfill] 无可回填行")
        return 0
    cur = conn.cursor()
    cur.executemany("UPDATE backtest_results SET dataset=? WHERE id=? AND dataset IS NULL",
                    [(ds, bid) for bid, _, ds, _ in plan])
    conn.commit()
    print(f"[backfill] 已回填 {cur.rowcount if cur.rowcount >= 0 else len(plan)} 行")
    return 0


if __name__ == "__main__":
    sys.exit(main())
