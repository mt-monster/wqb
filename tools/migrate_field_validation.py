# -*- coding: utf-8 -*-
"""数据库迁移：字段可用性验证态（2026-08-31）。

迁移内容（全部幂等，可重复执行）：
1. fields 表加三列：
   - verified INTEGER DEFAULT 0      -- 0未验证 1可用 -1不可用
   - verified_context TEXT           -- 形如 "IND/TOP500/D1"
   - verified_at TIMESTAMP
2. 新建 external_fields 表：记录区域上下文里引用、但本地 fields 表未灌的字段
   （如 IND 引用的 mdl238_global_rank / anl9_* / fnd86_*）。
3. 补索引：fields(dataset_id, verified)、fields(field_name)

用法：
    python tools/migrate_field_validation.py            # 默认 data/wqb.db
    python tools/migrate_field_validation.py --dry-run  # 只打印不执行
    python tools/migrate_field_validation.py --db path/to.db
"""
import argparse
import sqlite3
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
            actions.append(f"[DRY] {desc}: {sql[:90]}")
        else:
            cur.execute(sql)
            actions.append(f"[OK] {desc}")

    # 1. fields 加 verified 三列
    if not _has_column(cur, "fields", "verified"):
        do("ALTER TABLE fields ADD COLUMN verified INTEGER DEFAULT 0",
           "fields.verified 列")
    else:
        actions.append("[SKIP] fields.verified 已存在")

    if not _has_column(cur, "fields", "verified_context"):
        do("ALTER TABLE fields ADD COLUMN verified_context TEXT",
           "fields.verified_context 列")
    else:
        actions.append("[SKIP] fields.verified_context 已存在")

    if not _has_column(cur, "fields", "verified_at"):
        do("ALTER TABLE fields ADD COLUMN verified_at TIMESTAMP",
           "fields.verified_at 列")
    else:
        actions.append("[SKIP] fields.verified_at 已存在")

    # 2. external_fields 表
    if not _has_table(cur, "external_fields"):
        do("""CREATE TABLE external_fields (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              field_name TEXT NOT NULL,
              region TEXT NOT NULL,            -- 在哪个区域上下文被引用/验证
              source_regions TEXT,             -- 本地 fields 表里该字段实际归属的区域(JSON数组)
              in_local_db INTEGER DEFAULT 0,   -- 1=本地 fields 表存在(跨区), 0=本地未灌(平台字段)
              verified INTEGER DEFAULT 0,      -- 0未验证 1可用 -1不可用
              first_seen_alpha TEXT,           -- 首次出现的 alpha_id
              use_count INTEGER DEFAULT 0,     -- 在该区域 alpha 中出现次数
              note TEXT,
              created_at TIMESTAMP,
              updated_at TIMESTAMP,
              UNIQUE(field_name, region)
           )""", "external_fields 表")
    else:
        actions.append("[SKIP] external_fields 已存在")

    # 3. 索引
    if not _has_index(cur, "idx_fields_ds_verified"):
        do("CREATE INDEX idx_fields_ds_verified ON fields(dataset_id, verified)",
           "索引 fields(dataset_id,verified)")
    else:
        actions.append("[SKIP] idx_fields_ds_verified 已存在")

    if not _has_index(cur, "idx_fields_name"):
        do("CREATE INDEX idx_fields_name ON fields(field_name)",
           "索引 fields(field_name)")
    else:
        actions.append("[SKIP] idx_fields_name 已存在")

    if not _has_index(cur, "idx_ext_fields_region"):
        do("CREATE INDEX idx_ext_fields_region ON external_fields(region, verified)",
           "索引 external_fields(region,verified)")
    else:
        actions.append("[SKIP] idx_ext_fields_region 已存在")

    if not dry_run:
        conn.commit()
    return actions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/wqb.db")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    actions = migrate(conn, dry_run=args.dry_run)
    for a in actions:
        print(a)
    conn.close()
    print(f"\n{'[DRY-RUN] 未执行任何更改' if args.dry_run else '迁移完成'}: {args.db}")


if __name__ == "__main__":
    main()
