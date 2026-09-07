#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回填 expressions.fingerprint 并建索引，让全历史去重真正可用。

背景（2026-09-06 审计）：`upsert_expressions` 只写调用方传进来的 fingerprint，
而绝大多数调用方不传 —— 实测 9 924 行里 3 059 行（30.8%）为 NULL，KOR 单区
1 008 行。任何按 fingerprint 做的查重都会静默漏掉这三成；全库重复表达式
1 833 行（18.5%）就是这么攒出来的。写入侧已在
`wqb.store._expressions.expression_fingerprint` 修好，本脚本处理存量。

    python tools/backfill_fingerprints.py --dry-run   # 只报告
    python tools/backfill_fingerprints.py             # 回填 + 建索引

只写 fingerprint 列，不删除、不合并任何行 —— 重复行怎么处置是策略问题
（哪条保留、状态如何合并），交给人决定，脚本只负责让重复变得可见。
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from wqb.store._expressions import expression_fingerprint  # noqa: E402

DB_PATH = os.path.join(REPO_ROOT, "data", "wqb.db")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=DB_PATH)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    conn = sqlite3.connect(a.db)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        total = conn.execute("SELECT COUNT(*) FROM expressions").fetchone()[0]
        rows = conn.execute(
            "SELECT id, expression FROM expressions "
            "WHERE fingerprint IS NULL OR fingerprint = ''"
        ).fetchall()
        print(f"expressions 总行数 {total}，缺指纹 {len(rows)} "
              f"（{100 * len(rows) / total:.1f}%）")

        if a.dry_run:
            for eid, expr in rows[:5]:
                print(f"  {eid} -> {expression_fingerprint(expr)}  {expr[:60]}")
            print("（--dry-run，未写库）")
            return 0

        conn.executemany(
            "UPDATE expressions SET fingerprint=? WHERE id=?",
            [(expression_fingerprint(expr), eid) for eid, expr in rows],
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_expr_fingerprint "
            "ON expressions(region, fingerprint)"
        )
        conn.commit()

        remaining = conn.execute(
            "SELECT COUNT(*) FROM expressions "
            "WHERE fingerprint IS NULL OR fingerprint = ''"
        ).fetchone()[0]
        print(f"已回填 {len(rows)} 行，剩余缺失 {remaining}")

        print("\n回填后可见的跨波重复（同区同指纹出现 >1 次）：")
        dups = conn.execute(
            "SELECT region, COUNT(*) - COUNT(DISTINCT fingerprint) FROM expressions "
            "GROUP BY region ORDER BY 2 DESC"
        ).fetchall()
        for region, n in dups:
            if n:
                print(f"  {region}: {n} 条重复")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
