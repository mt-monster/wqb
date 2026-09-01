# -*- coding: utf-8 -*-
"""数据库迁移脚本：应用所有 schema 优化（2026-08-30）。

迁移内容：
1. 删除 workflow_configs 表
2. 删除 backtest_results 的死字段：concentrated_weight, ra_failed_count, ppa_failed_count, ppa_failed_checks
3. 删除 waves.completed_at 字段
4. 删除 submission_ledger.quota_remaining 字段
5. backtest_results 去重 + UNIQUE 约束
6. 补索引：backtest_results(alpha_id), backtest_results(region,wave),
   submission_ledger(alpha_id), wave_results(region), alphas(platform_status)
7. cross_region_lessons 数据迁移到 registry_empirical (layer='cross_region')
8. diversity_potential 数据迁移到 ledger_kv（已有双写，确认覆盖）
9. 回填 expressions 表指标（从 alphas 表同步）

用法：
    python tools/migrate_db_schema.py            # 默认 data/wqb.db
    python tools/migrate_db_schema.py --dry-run  # 只打印不执行
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _has_column(cur, table, col):
    cur.execute(f"PRAGMA table_info({table})")
    return any(r[1] == col for r in cur.fetchall())


def _has_table(cur, table):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cur.fetchone() is not None


def _has_index(cur, name):
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", (name,))
    return cur.fetchone() is not None


def migrate(conn, dry_run=False):
    cur = conn.cursor()
    actions = []

    def do(sql, desc):
        if dry_run:
            actions.append(f"[DRY] {desc}: {sql[:80]}")
        else:
            cur.execute(sql)
            actions.append(f"[OK] {desc}")

    def do_execscript(sql, desc):
        if dry_run:
            actions.append(f"[DRY] {desc}")
        else:
            cur.executescript(sql)
            actions.append(f"[OK] {desc}")

    # 1. 删除 workflow_configs 表
    if _has_table(cur, "workflow_configs"):
        do("DROP TABLE workflow_configs", "删除空表 workflow_configs")

    # 2. 删除 backtest_results 死字段
    for col in ["concentrated_weight", "ra_failed_count", "ppa_failed_count", "ppa_failed_checks"]:
        if _has_column(cur, "backtest_results", col):
            do(f"ALTER TABLE backtest_results DROP COLUMN {col}", f"删除 backtest_results.{col}")

    # 3. 删除 waves.completed_at
    if _has_column(cur, "waves", "completed_at"):
        do("ALTER TABLE waves DROP COLUMN completed_at", "删除 waves.completed_at")

    # 4. 删除 submission_ledger.quota_remaining
    if _has_column(cur, "submission_ledger", "quota_remaining"):
        do("ALTER TABLE submission_ledger DROP COLUMN quota_remaining", "删除 submission_ledger.quota_remaining")

    # 5. backtest_results 去重 + UNIQUE 约束
    if not _has_index(cur, "idx_backtest_results_alpha_unique"):
        # 先去重：保留每个 alpha_id 的最新行
        if _has_table(cur, "backtest_results"):
            dup_count = cur.execute(
                "SELECT COUNT(*) - COUNT(DISTINCT alpha_id) FROM backtest_results WHERE alpha_id IS NOT NULL"
            ).fetchone()[0]
            if dup_count > 0:
                do_execscript(
                    "DELETE FROM backtest_results WHERE id NOT IN "
                    "(SELECT MAX(id) FROM backtest_results WHERE alpha_id IS NOT NULL GROUP BY alpha_id);",
                    f"backtest_results 去重（删除 {dup_count} 条重复行）"
                )
        do(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_backtest_results_alpha_unique "
            "ON backtest_results(alpha_id)",
            "创建 backtest_results.alpha_id UNIQUE 索引"
        )

    # 6. 补索引
    indexes = [
        ("idx_backtest_results_alpha_id", "CREATE INDEX IF NOT EXISTS idx_backtest_results_alpha_id ON backtest_results(alpha_id)"),
        ("idx_backtest_results_region_wave", "CREATE INDEX IF NOT EXISTS idx_backtest_results_region_wave ON backtest_results(region, wave)"),
        ("idx_submission_ledger_alpha_id", "CREATE INDEX IF NOT EXISTS idx_submission_ledger_alpha_id ON submission_ledger(alpha_id)"),
        ("idx_wave_results_region", "CREATE INDEX IF NOT EXISTS idx_wave_results_region ON wave_results(region)"),
        ("idx_alphas_platform_status", "CREATE INDEX IF NOT EXISTS idx_alphas_platform_status ON alphas(platform_status)"),
    ]
    for name, sql in indexes:
        if not _has_index(cur, name):
            do(sql, f"创建索引 {name}")

    # 7. cross_region_lessons → registry_empirical
    if _has_table(cur, "cross_region_lessons"):
        rows = cur.execute("SELECT lesson_id, family, finding, rule FROM cross_region_lessons").fetchall()
        if rows:
            migrated = 0
            for lesson_id, family, finding, rule in rows:
                payload = json.dumps({"finding": finding or "", "rule": rule or ""}, ensure_ascii=False)
                existing = cur.execute(
                    "SELECT id FROM registry_empirical WHERE layer='cross_region' AND entry_id=?",
                    (lesson_id,)
                ).fetchone()
                if not existing:
                    if not dry_run:
                        cur.execute(
                            "INSERT INTO registry_empirical (region, layer, entry_id, family, payload, created_at, updated_at) "
                            "VALUES ('GLOBAL', 'cross_region', ?, ?, ?, ?, ?)",
                            (lesson_id, family, payload, _now(), _now())
                        )
                    migrated += 1
            actions.append(f"[{'DRY' if dry_run else 'OK'}] cross_region_lessons → registry_empirical: {migrated} 条迁移")
        # 数据迁移完成后删除旧表（读取方已改为 registry_empirical）
        do("DROP TABLE IF EXISTS cross_region_lessons", "删除已废弃表 cross_region_lessons")

    # 8. diversity_potential 数据已在双写时进入 ledger_kv，确认覆盖
    if _has_table(cur, "diversity_potential"):
        dp_rows = cur.execute("SELECT COUNT(*) FROM diversity_potential").fetchone()[0]
        if dp_rows > 0:
            # 检查每条是否已在 ledger_kv
            missing = 0
            dp_data = cur.execute(
                "SELECT dp.region_id, d.name as dataset_name, dp.payload_json "
                "FROM diversity_potential dp JOIN datasets d ON dp.dataset_id=d.id"
            ).fetchall()
            for rid, ds_name, payload_json in dp_data:
                region_name = cur.execute("SELECT name FROM regions WHERE id=?", (rid,)).fetchone()[0]
                kv = cur.execute(
                    "SELECT value FROM ledger_kv WHERE region=? AND key=?",
                    (region_name, f"diversity_{ds_name}")
                ).fetchone()
                if not kv and payload_json:
                    if not dry_run:
                        cur.execute(
                            "INSERT OR REPLACE INTO ledger_kv (region, key, value, created_at, updated_at) "
                            "VALUES (?, ?, ?, ?, ?)",
                            (region_name, f"diversity_{ds_name}", payload_json, _now(), _now())
                        )
                    missing += 1
            actions.append(f"[{'DRY' if dry_run else 'OK'}] diversity_potential → ledger_kv: {missing} 条补写")
        # 迁移后可安全删除表
        do("DROP TABLE IF EXISTS diversity_potential", "删除已废弃表 diversity_potential")

    # 9. 回填 expressions 表指标
    if _has_table(cur, "expressions") and _has_table(cur, "alphas"):
        null_count = cur.execute(
            "SELECT COUNT(*) FROM expressions WHERE alpha_id IS NOT NULL AND sharpe IS NULL"
        ).fetchone()[0]
        if null_count > 0:
            if not dry_run:
                cur.execute(
                    """UPDATE expressions SET
                       sharpe=(SELECT a.sharpe FROM alphas a WHERE a.alpha_id=expressions.alpha_id),
                       fitness=(SELECT a.fitness FROM alphas a WHERE a.alpha_id=expressions.alpha_id),
                       margin=(SELECT a.margin FROM alphas a WHERE a.alpha_id=expressions.alpha_id),
                       turnover=(SELECT a.turnover FROM alphas a WHERE a.alpha_id=expressions.alpha_id),
                       updated_at=?
                       WHERE alpha_id IS NOT NULL AND sharpe IS NULL
                       AND EXISTS (SELECT 1 FROM alphas a WHERE a.alpha_id=expressions.alpha_id AND a.sharpe IS NOT NULL)""",
                    (_now(),)
                )
            actions.append(f"[{'DRY' if dry_run else 'OK'}] 回填 expressions 指标: {null_count} 条")

    if not dry_run:
        conn.commit()

    return actions


def main():
    ap = argparse.ArgumentParser(description="wqb 数据库 schema 迁移")
    ap.add_argument("--db", default=os.path.join("data", "wqb.db"), help="数据库路径")
    ap.add_argument("--dry-run", action="store_true", help="只打印不执行")
    ap.add_argument("--backup", action="store_true", default=True, help="迁移前自动备份")
    a = ap.parse_args()

    if not os.path.isfile(a.db):
        print(f"数据库不存在: {a.db}")
        sys.exit(1)

    # 备份
    if a.backup and not a.dry_run:
        bak = f"{a.db}.bak_schema_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(a.db, bak)
        print(f"已备份: {bak}")

    conn = sqlite3.connect(a.db)
    conn.row_factory = sqlite3.Row
    print(f"迁移 {'(DRY RUN)' if a.dry_run else ''}: {a.db}")
    print("=" * 60)
    actions = migrate(conn, dry_run=a.dry_run)
    for a in actions:
        print(a)
    conn.close()
    print(f"\n完成: {len(actions)} 个操作")


if __name__ == "__main__":
    main()
