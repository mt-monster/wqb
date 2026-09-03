# -*- coding: utf-8 -*-
"""回填 alphas 缺失指标（2Y/sharpe/fitness/turnover/margin），逐列短事务防锁。"""
import sqlite3
import sys
import time
from datetime import datetime

DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
ts = datetime.now().isoformat(timespec="seconds")


def with_retry(fn, max_retry=8, wait=10):
    for i in range(max_retry):
        try:
            return fn()
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and i < max_retry - 1:
                print(f"  locked, retry {i+1}/{max_retry} after {wait}s")
                time.sleep(wait)
            else:
                raise


def backfill(col, from_payload):
    def run():
        conn = sqlite3.connect(DB, timeout=10)
        cur = conn.cursor()
        if from_payload:
            src = "json_extract(b.payload_json, '$.%s')" % col
        else:
            src = "b.two_year_sharpe" if col == "two_year_sharpe" else col
        # 直连路径：backtest_results.alpha_id 直接关联（expressions 中转路径覆盖不全）
        cur.execute(
            f"""
            UPDATE alphas SET {col} = (
                SELECT {src} FROM backtest_results b
                WHERE b.alpha_id = alphas.alpha_id AND {src} IS NOT NULL
                ORDER BY b.id DESC LIMIT 1
            ), updated_at = ?
            WHERE {col} IS NULL AND alpha_id IS NOT NULL AND EXISTS (
                SELECT 1 FROM backtest_results b
                WHERE b.alpha_id = alphas.alpha_id AND {src} IS NOT NULL
            )
            """,
            (ts,),
        )
        n = cur.rowcount
        conn.commit()
        conn.close()
        return n
    return with_retry(run)


print("== 回填 two_year_sharpe ==")
print("  从列值:", backfill("two_year_sharpe", from_payload=False))
print("  从payload:", backfill("two_year_sharpe", from_payload=True))

for col in ["sharpe", "fitness", "turnover", "margin"]:
    print(f"== 回填 {col} ==")
    print("  从payload:", backfill(col, from_payload=True))

# 验证
conn = sqlite3.connect(DB, timeout=10)
r = conn.execute(
    """SELECT COUNT(*),
    SUM(CASE WHEN two_year_sharpe IS NOT NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN sharpe IS NOT NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN fitness IS NOT NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN turnover IS NOT NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN margin IS NOT NULL THEN 1 ELSE 0 END)
    FROM alphas"""
).fetchone()
conn.close()
print(f"\n回填后: 总量={r[0]} | 2Y={r[1]} | sharpe={r[2]} | fitness={r[3]} | turnover={r[4]} | margin={r[5]}")
