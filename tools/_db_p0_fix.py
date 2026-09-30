#!/usr/bin/env python3
"""P0 数据质量修复脚本

修复内容：
1. 清理 submit_ready 中引用不存在 alpha 的脏数据（22 条）
2. 清理 expressions 中 wave_id=0 的孤儿记录（18 条）
3. 统一 alpha_id 字段类型为 VARCHAR(50)
4. 统一 region 字段类型为 VARCHAR(50)

执行前自动从备份创建干净副本（VACUUM INTO），避免损坏的数据库影响修复。
"""

import sqlite3
import os
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "wqb.db"
BACKUP_PATH = Path(__file__).resolve().parents[1] / "data" / "wqb.db.bak_prewhitelist_20260928_122352"
CLEAN_PATH = Path(__file__).resolve().parents[1] / "data" / "wqb_p0.db"


def create_clean_copy():
    """从备份创建干净副本"""
    print("=" * 60)
    print("步骤 0: 从备份创建干净副本 (VACUUM INTO)")
    print("=" * 60)
    print(f"  源: {BACKUP_PATH}")
    print(f"  目标: {CLEAN_PATH}")

    if not BACKUP_PATH.exists():
        print(f"  ✗ 备份不存在: {BACKUP_PATH}")
        sys.exit(1)

    # 删除可能存在的旧干净副本
    if CLEAN_PATH.exists():
        CLEAN_PATH.unlink()

    conn = sqlite3.connect(str(BACKUP_PATH))
    try:
        conn.execute(f"VACUUM INTO '{CLEAN_PATH}'")
        print("  ✓ VACUUM INTO 成功")
    except Exception as e:
        print(f"  ✗ VACUUM INTO 失败: {e}")
        sys.exit(1)
    finally:
        conn.close()

    # 验证干净副本
    conn = sqlite3.connect(str(CLEAN_PATH))
    conn.row_factory = sqlite3.Row
    try:
        result = conn.execute("PRAGMA integrity_check").fetchone()[0]
        print(f"  完整性检查: {result}")
    except Exception as e:
        print(f"  ✗ 完整性检查失败: {e}")
        sys.exit(1)

    # 检查关键数据量
    for t in ["alphas", "backtest_results", "expressions", "submit_ready"]:
        cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {cnt} 行")

    conn.close()
    return CLEAN_PATH


def fix_submit_ready_orphans(conn):
    """清理 submit_ready 中引用不存在 alpha 的记录"""
    print()
    print("=" * 60)
    print("P0-1: 清理 submit_ready 脏数据")
    print("=" * 60)

    dirty = conn.execute("""
        SELECT sr.alpha_id, sr.region, sr.status, sr.gate
        FROM submit_ready sr
        LEFT JOIN alphas a ON sr.alpha_id = a.alpha_id
        WHERE a.alpha_id IS NULL
    """).fetchall()

    print(f"  发现 {len(dirty)} 条脏数据（引用不存在的 alpha）:")
    for row in dirty:
        print(f"    alpha_id={row['alpha_id']}, region={row['region']}, status={row['status']}, gate={row['gate']}")

    if dirty:
        conn.execute("""
            DELETE FROM submit_ready
            WHERE alpha_id IN (
                SELECT sr.alpha_id
                FROM submit_ready sr
                LEFT JOIN alphas a ON sr.alpha_id = a.alpha_id
                WHERE a.alpha_id IS NULL
            )
        """)
        conn.commit()
        print(f"  ✓ 已删除 {len(dirty)} 条脏数据")
    else:
        print("  ✓ 无脏数据")

    # 验证
    remaining = conn.execute("""
        SELECT COUNT(*) as cnt
        FROM submit_ready sr
        LEFT JOIN alphas a ON sr.alpha_id = a.alpha_id
        WHERE a.alpha_id IS NULL
    """).fetchone()["cnt"]
    print(f"  验证: 剩余脏数据 {remaining} 条")
    return len(dirty)


def fix_expression_orphans(conn):
    """清理 expressions 中 wave_id=0 的孤儿记录"""
    print()
    print("=" * 60)
    print("P0-2: 清理孤儿表达式 (wave_id=0)")
    print("=" * 60)

    orphans = conn.execute("""
        SELECT id, wave_id, expression, status
        FROM expressions
        WHERE wave_id = 0 OR wave_id NOT IN (SELECT id FROM waves)
    """).fetchall()

    print(f"  发现 {len(orphans)} 条孤儿表达式:")
    for row in orphans:
        expr_preview = row["expression"][:50] if row["expression"] else "NULL"
        print(f"    id={row['id']}, wave_id={row['wave_id']}, status={row['status']}, expr={expr_preview}...")

    if orphans:
        conn.execute("""
            DELETE FROM expressions
            WHERE wave_id = 0 OR wave_id NOT IN (SELECT id FROM waves)
        """)
        conn.commit()
        print(f"  ✓ 已删除 {len(orphans)} 条孤儿表达式")
    else:
        print("  ✓ 无孤儿表达式")

    # 验证
    remaining = conn.execute("""
        SELECT COUNT(*) as cnt
        FROM expressions
        WHERE wave_id = 0 OR wave_id NOT IN (SELECT id FROM waves)
    """).fetchone()["cnt"]
    print(f"  验证: 剩余孤儿表达式 {remaining} 条")
    return len(orphans)


def rebuild_table(conn, table, col_overrides=None):
    """重建表以修改列类型
    
    Args:
        conn: 数据库连接
        table: 表名
        col_overrides: dict, 列名 -> 新类型
    """
    col_overrides = col_overrides or {}
    
    # 获取表结构
    columns = conn.execute(f"PRAGMA table_info({table})").fetchall()
    col_defs = []
    for col in columns:
        col_type = col_overrides.get(col["name"], col["type"])
        col_def = f"{col['name']} {col_type}"
        if col["notnull"]:
            col_def += " NOT NULL"
        if col["dflt_value"] is not None:
            col_def += f" DEFAULT {col['dflt_value']}"
        if col["pk"]:
            col_def += " PRIMARY KEY"
        col_defs.append(col_def)
    
    # 获取索引（跳过 autoindex）
    indexes = conn.execute(f"PRAGMA index_list({table})").fetchall()
    index_sqls = []
    for idx in indexes:
        idx_name = idx["name"]
        if idx_name.startswith("sqlite_autoindex_"):
            continue
        idx_info = conn.execute(f"PRAGMA index_info({idx_name})").fetchall()
        idx_cols = [info["name"] for info in idx_info]
        unique = "UNIQUE " if idx["unique"] else ""
        index_sqls.append(f"CREATE {unique}INDEX IF NOT EXISTS {idx_name} ON {table} ({', '.join(idx_cols)})")
    
    # 重建表
    conn.execute("BEGIN TRANSACTION")
    try:
        conn.execute(f"ALTER TABLE {table} RENAME TO {table}_old")
        conn.execute(f"CREATE TABLE {table} ({', '.join(col_defs)})")
        col_names = [col["name"] for col in columns]
        conn.execute(f"INSERT INTO {table} ({', '.join(col_names)}) SELECT {', '.join(col_names)} FROM {table}_old")
        conn.execute(f"DROP TABLE {table}_old")
        for idx_sql in index_sqls:
            conn.execute(idx_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise


def fix_alpha_id_type(conn):
    """统一 alpha_id 字段类型为 VARCHAR(50)"""
    print()
    print("=" * 60)
    print("P0-3: 统一 alpha_id 字段类型为 VARCHAR(50)")
    print("=" * 60)

    tables = ["alphas", "backtest_results", "expressions", 
              "structural_variant_results", "submission_ledger", "submit_ready"]
    
    need_fix = []
    for table in tables:
        cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
        for col in cols:
            if col["name"] == "alpha_id":
                if col["type"] != "VARCHAR(50)":
                    need_fix.append((table, col["type"]))
                    print(f"  {table}.alpha_id: {col['type']} -> VARCHAR(50)")
                else:
                    print(f"  {table}.alpha_id: {col['type']} (已正确)")
                break

    if not need_fix:
        print("  ✓ 所有表 alpha_id 类型已正确")
        return 0

    for table, old_type in need_fix:
        print(f"  修复 {table}...")
        rebuild_table(conn, table, {"alpha_id": "VARCHAR(50)"})
        print(f"    ✓ {table} 修复完成")

    return len(need_fix)


def fix_region_type(conn):
    """统一 region 字段类型为 VARCHAR(50)"""
    print()
    print("=" * 60)
    print("P0-4: 统一 region 字段类型为 VARCHAR(50)")
    print("=" * 60)

    tables = ["backtest_results", "expressions", "external_fields", 
              "gate_results", "submit_ready", "ledger_kv", 
              "registry_empirical", "structural_variant_results", 
              "submission_ledger", "wave_results"]
    
    need_fix = []
    for table in tables:
        try:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            for col in cols:
                if col["name"] == "region":
                    if col["type"] != "VARCHAR(50)":
                        need_fix.append((table, col["type"]))
                        print(f"  {table}.region: {col['type']} -> VARCHAR(50)")
                    else:
                        print(f"  {table}.region: {col['type']} (已正确)")
                    break
        except Exception as e:
            print(f"  {table}: 检查失败 {e}")

    if not need_fix:
        print("  ✓ 所有表 region 类型已正确")
        return 0

    # 先删除依赖视图
    print("  删除依赖视图 v_alpha_metrics...")
    conn.execute("DROP VIEW IF EXISTS v_alpha_metrics")

    for table, old_type in need_fix:
        print(f"  修复 {table}...")
        rebuild_table(conn, table, {"region": "VARCHAR(50)"})
        print(f"    ✓ {table} 修复完成")

    # 重建视图
    print("  重建视图 v_alpha_metrics...")
    conn.execute("""
        CREATE VIEW v_alpha_metrics AS
        SELECT a.alpha_id,
               r.name  AS region,
               a.expression,
               a.status AS local_status,
               a.platform_status,
               a.stage,
               a.alpha_type,
               a.sharpe   AS a_sharpe,
               a.fitness  AS a_fitness,
               a.turnover AS a_turnover,
               b.sharpe   AS b_sharpe,
               b.fitness  AS b_fitness,
               b.turnover AS b_turnover,
               a.prod_correlation,
               a.self_correlation,
               a.two_year_sharpe,
               b.sub_universe_sharpe,
               a.date_submitted
        FROM alphas a
        LEFT JOIN regions r ON a.region_id = r.id
        LEFT JOIN backtest_results b ON a.alpha_id = b.alpha_id
    """)
    conn.commit()
    print("    ✓ 视图重建完成")

    return len(need_fix)


def main():
    print("WQB 数据库 P0 修复")
    print(f"数据库: {DB_PATH}")
    print(f"备份: {BACKUP_PATH}")
    print()

    # 步骤 0: 创建干净副本
    clean_db = create_clean_copy()

    # 在干净副本上执行修复
    conn = sqlite3.connect(str(clean_db))
    conn.row_factory = sqlite3.Row
    
    try:
        # P0-1: 清理 submit_ready 脏数据
        dirty_count = fix_submit_ready_orphans(conn)
        
        # P0-2: 清理孤儿表达式
        orphan_count = fix_expression_orphans(conn)
        
        # P0-3: 统一 alpha_id 类型
        alpha_id_fixed = fix_alpha_id_type(conn)
        
        # P0-4: 统一 region 类型
        region_fixed = fix_region_type(conn)
        
        print()
        print("=" * 60)
        print("P0 修复完成 - 最终验证")
        print("=" * 60)

        # 验证 submit_ready 脏数据
        dirty = conn.execute("""
            SELECT COUNT(*) as cnt
            FROM submit_ready sr
            LEFT JOIN alphas a ON sr.alpha_id = a.alpha_id
            WHERE a.alpha_id IS NULL
        """).fetchone()["cnt"]
        print(f"  submit_ready 脏数据: {dirty} 条")

        # 验证孤儿表达式
        orphans = conn.execute("""
            SELECT COUNT(*) as cnt
            FROM expressions
            WHERE wave_id = 0 OR wave_id NOT IN (SELECT id FROM waves)
        """).fetchone()["cnt"]
        print(f"  孤儿表达式: {orphans} 条")

        # 验证 alpha_id 类型
        for table in ["alphas", "backtest_results", "expressions", 
                      "structural_variant_results", "submission_ledger", "submit_ready"]:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            for col in cols:
                if col["name"] == "alpha_id":
                    print(f"  {table}.alpha_id: {col['type']}")
                    break

        # 验证 region 类型
        for table in ["backtest_results", "expressions", "external_fields", 
                      "gate_results", "submit_ready", "ledger_kv", 
                      "registry_empirical", "structural_variant_results", 
                      "submission_ledger", "wave_results"]:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            for col in cols:
                if col["name"] == "region":
                    print(f"  {table}.region: {col['type']}")
                    break

        # 验证完整性
        try:
            result = conn.execute("PRAGMA integrity_check").fetchone()[0]
            print(f"  完整性检查: {result}")
        except Exception as e:
            print(f"  完整性检查失败: {e}")

        conn.close()

        # 替换损坏的数据库
        print()
        print("替换 data/wqb.db...")
        try:
            if DB_PATH.exists():
                DB_PATH.unlink()
                print("  已删除旧的 wqb.db")
        except Exception as e:
            print(f"  删除失败: {e}")

        try:
            os.rename(str(clean_db), str(DB_PATH))
            print("  ✓ 已替换为修复后的数据库")
        except Exception as e:
            print(f"  ✗ 替换失败: {e}")
            sys.exit(1)

        print()
        print("=" * 60)
        print("✓ P0 修复全部完成")
        print("=" * 60)
        print(f"  submit_ready 脏数据: {dirty_count} 条已删除")
        print(f"  孤儿表达式: {orphan_count} 条已删除")
        print(f"  alpha_id 类型修复: {alpha_id_fixed} 张表")
        print(f"  region 类型修复: {region_fixed} 张表")
        
    except Exception as e:
        print(f"\n✗ 修复失败: {e}")
        conn.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
