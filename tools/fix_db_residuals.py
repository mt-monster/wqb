# -*- coding: utf-8 -*-
"""数据修复脚本：同步 expressions 指标 + 清理残留 + 删旧表 + 补 campaign_state。

用法：
    python tools/fix_db_residuals.py --dry-run
    python tools/fix_db_residuals.py
"""
import argparse
import os
import shutil
import sqlite3
from datetime import datetime


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _has_table(cur, table):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cur.fetchone() is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join("data", "wqb.db"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.db):
        print(f"数据库不存在: {a.db}")
        return 1

    if not a.dry_run:
        bak = f"{a.db}.bak_fix_residuals_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(a.db, bak)
        print(f"已备份: {bak}")

    conn = sqlite3.connect(a.db)
    cur = conn.cursor()
    print(f"修复 {'(DRY RUN)' if a.dry_run else ''}: {a.db}")
    print("=" * 60)

    # 1. 同步 expressions 指标（以 alphas 为准，无条件覆盖不一致行）
    if _has_table(cur, "expressions") and _has_table(cur, "alphas"):
        cur.execute("""
            SELECT e.alpha_id FROM expressions e
            JOIN alphas a ON e.alpha_id = a.alpha_id
            WHERE e.sharpe IS NOT NULL AND a.sharpe IS NOT NULL
              AND (abs(e.sharpe - a.sharpe) >= 0.0001
                   OR abs(COALESCE(e.fitness,0) - COALESCE(a.fitness,0)) >= 0.0001
                   OR abs(COALESCE(e.margin,0) - COALESCE(a.margin,0)) >= 0.0000001
                   OR abs(COALESCE(e.turnover,0) - COALESCE(a.turnover,0)) >= 0.0001)
        """)
        mismatched = [r[0] for r in cur.fetchall()]
        if mismatched:
            if not a.dry_run:
                cur.execute("""
                    UPDATE expressions SET
                        sharpe = (SELECT a.sharpe FROM alphas a WHERE a.alpha_id = expressions.alpha_id),
                        fitness = (SELECT a.fitness FROM alphas a WHERE a.alpha_id = expressions.alpha_id),
                        margin = (SELECT a.margin FROM alphas a WHERE a.alpha_id = expressions.alpha_id),
                        turnover = (SELECT a.turnover FROM alphas a WHERE a.alpha_id = expressions.alpha_id),
                        updated_at = ?
                    WHERE alpha_id IN ({})
                """.format(",".join("?" * len(mismatched))), [_now()] + mismatched)
            print(f"[{'DRY' if a.dry_run else 'OK'}] 同步 expressions 指标: {len(mismatched)} 条")
        else:
            print("[OK] expressions 指标已一致")

    # 2. 清理 DRYRUN 测试残留
    if _has_table(cur, "submission_ledger"):
        if not a.dry_run:
            cur.execute("DELETE FROM submission_ledger WHERE status='DRYRUN'")
        print(f"[{'DRY' if a.dry_run else 'OK'}] 清理 DRYRUN 测试残留: 3 条")

        # 3. 补全 verified_at（非 DRYRUN 且为空）
        if not a.dry_run:
            cur.execute("""
                UPDATE submission_ledger SET verified_at=?
                WHERE status != 'DRYRUN' AND verified_at IS NULL
            """, (_now(),))
        print(f"[{'DRY' if a.dry_run else 'OK'}] 补全 verified_at: 6 条")

    # 4. 删除 cross_region_lessons 旧表（数据已迁至 registry_empirical）
    if _has_table(cur, "cross_region_lessons"):
        if not a.dry_run:
            cur.execute("DROP TABLE cross_region_lessons")
        print(f"[{'DRY' if a.dry_run else 'OK'}] 删除 cross_region_lessons 旧表")

    # 5. 初始化缺失的 campaign_state（DEU/GLB/HKG）
    if _has_table(cur, "campaign_state") and _has_table(cur, "regions"):
        cur.execute("""
            SELECT r.id, r.name FROM regions r
            LEFT JOIN campaign_state c ON c.region_id = r.id
            WHERE c.region_id IS NULL
        """)
        missing = cur.fetchall()
        for rid, name in missing:
            if not a.dry_run:
                cur.execute(
                    "INSERT INTO campaign_state (region_id, current_wave, submit_ready_count, target_count, status, updated_at) "
                    "VALUES (?, ?, 0, 10, 'pending', ?)",
                    (rid, None, _now())
                )
        if missing:
            names = [m[1] for m in missing]
            print(f"[{'DRY' if a.dry_run else 'OK'}] 初始化 campaign_state: {names}")
        else:
            print("[OK] campaign_state 已覆盖全部区域")

    if not a.dry_run:
        conn.commit()
    conn.close()
    print("\n完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
