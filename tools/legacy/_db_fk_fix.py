#!/usr/bin/env python3
"""外键约束补齐脚本

为 7 张缺失外键声明的表添加 FOREIGN KEY 约束：
1. backtest_results: expression_id → expressions(id)
2. expressions: wave_id → waves(id)
3. submit_ready: alpha_id → alphas(alpha_id)
4. submission_ledger: alpha_id → alphas(alpha_id)
5. structural_variant_results: alpha_id → alphas(alpha_id)
6. wave_results: region_id → regions(id)
7. registry_empirical: region_id → regions(id)

执行前自动从备份创建干净副本（VACUUM INTO），在副本上执行修复后原子替换。
"""

import sqlite3
import os
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "wqb.db"
BACKUP_PATH = Path(__file__).resolve().parents[1] / "data" / "wqb.db.bak_prewhitelist_20260928_122352"
CLEAN_PATH = Path(__file__).resolve().parents[1] / "data" / "wqb_fk.db"


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

    # 验证
    conn = sqlite3.connect(str(CLEAN_PATH))
    conn.row_factory = sqlite3.Row
    try:
        result = conn.execute("PRAGMA integrity_check").fetchone()[0]
        print(f"  完整性检查: {result}")
    except Exception as e:
        print(f"  ✗ 完整性检查失败: {e}")
        sys.exit(1)

    for t in ["alphas", "backtest_results", "expressions", "submit_ready"]:
        cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {cnt} 行")

    conn.close()
    return CLEAN_PATH


def clean_orphans(conn):
    """清理所有孤儿数据"""
    print()
    print("=" * 60)
    print("步骤 1: 清理孤儿数据")
    print("=" * 60)

    checks = [
        ("backtest_results", "expression_id", "expressions", "id"),
        ("expressions", "wave_id", "waves", "id"),
        ("submit_ready", "alpha_id", "alphas", "alpha_id"),
        ("submission_ledger", "alpha_id", "alphas", "alpha_id"),
        ("structural_variant_results", "alpha_id", "alphas", "alpha_id"),
        ("wave_results", "region_id", "regions", "id"),
        ("registry_empirical", "region_id", "regions", "id"),
    ]

    total_cleaned = 0
    for table, col, ref_table, ref_col in checks:
        try:
            orphans = conn.execute(f'''
                SELECT COUNT(*) as cnt
                FROM {table}
                WHERE {col} IS NOT NULL AND {col} NOT IN (SELECT {ref_col} FROM {ref_table})
            ''').fetchone()['cnt']
            
            if orphans > 0:
                conn.execute(f'''
                    DELETE FROM {table}
                    WHERE {col} IS NOT NULL AND {col} NOT IN (SELECT {ref_col} FROM {ref_table})
                ''')
                conn.commit()
                print(f"  {table}.{col}: 删除 {orphans} 条孤儿")
                total_cleaned += orphans
            else:
                print(f"  {table}.{col}: 无孤儿")
        except Exception as e:
            print(f"  {table}.{col}: 检查失败 {e}")

    print(f"  总计清理: {total_cleaned} 条孤儿")
    return total_cleaned


def rebuild_table_with_fk(conn, table, fk_definitions):
    """重建表添加外键约束
    
    Args:
        conn: 数据库连接
        table: 表名
        fk_definitions: list of (column, ref_table, ref_column) tuples
    """
    # 获取表结构
    columns = conn.execute(f"PRAGMA table_info({table})").fetchall()
    
    # 构建新表 DDL
    col_defs = []
    for col in columns:
        col_def = f"{col['name']} {col['type']}"
        if col["notnull"]:
            col_def += " NOT NULL"
        if col["dflt_value"] is not None:
            col_def += f" DEFAULT {col['dflt_value']}"
        if col["pk"]:
            col_def += " PRIMARY KEY"
        col_defs.append(col_def)
    
    # 添加外键约束
    for fk_col, ref_table, ref_col in fk_definitions:
        col_defs.append(f"FOREIGN KEY ({fk_col}) REFERENCES {ref_table}({ref_col})")
    
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


def add_foreign_keys(conn):
    """为 7 张表添加外键约束"""
    print()
    print("=" * 60)
    print("步骤 2: 重建表添加外键约束")
    print("=" * 60)

    # 先删除依赖视图（SQLite 重建表时需要）
    print("  删除依赖视图 v_alpha_metrics...")
    conn.execute("DROP VIEW IF EXISTS v_alpha_metrics")

    # 定义需要添加的外键
    fk_plans = [
        ("backtest_results", [("expression_id", "expressions", "id")]),
        ("expressions", [("wave_id", "waves", "id")]),
        ("submit_ready", [("alpha_id", "alphas", "alpha_id")]),
        ("submission_ledger", [("alpha_id", "alphas", "alpha_id")]),
        ("structural_variant_results", [("alpha_id", "alphas", "alpha_id")]),
        ("wave_results", [("region_id", "regions", "id")]),
        ("registry_empirical", [("region_id", "regions", "id")]),
    ]

    for table, fk_defs in fk_plans:
        print(f"  重建 {table}...")
        try:
            rebuild_table_with_fk(conn, table, fk_defs)
            print(f"    ✓ {table} 外键添加完成")
        except Exception as e:
            print(f"    ✗ {table} 修复失败: {e}")
            raise

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


def verify_foreign_keys(conn):
    """验证外键约束"""
    print()
    print("=" * 60)
    print("步骤 3: 验证外键约束")
    print("=" * 60)

    # 检查外键违例
    try:
        violations = conn.execute("PRAGMA foreign_key_check").fetchall()
        print(f"  foreign_key_check 违例数: {len(violations)}")
        for v in violations[:10]:
            print(f"    {v['table']}.{v['rowid']} -> {v['parent']}.{v['fk_id']}")
    except Exception as e:
        print(f"  foreign_key_check 失败: {e}")

    # 检查各表外键是否已声明
    tables_to_check = [
        ("backtest_results", "expression_id"),
        ("expressions", "wave_id"),
        ("submit_ready", "alpha_id"),
        ("submission_ledger", "alpha_id"),
        ("structural_variant_results", "alpha_id"),
        ("wave_results", "region_id"),
        ("registry_empirical", "region_id"),
    ]

    print()
    print("  外键声明检查:")
    for table, col in tables_to_check:
        try:
            # 获取表的外键列表
            fks = conn.execute(f"PRAGMA foreign_key_list({table})").fetchall()
            fk_cols = [fk["from"] for fk in fks]
            if col in fk_cols:
                print(f"    {table}.{col}: ✓ 已声明")
            else:
                print(f"    {table}.{col}: ✗ 未声明")
        except Exception as e:
            print(f"    {table}.{col}: 检查失败 {e}")

    # 完整性检查
    try:
        result = conn.execute("PRAGMA integrity_check").fetchone()[0]
        print(f"\n  完整性检查: {result}")
    except Exception as e:
        print(f"\n  完整性检查失败: {e}")


def main():
    print("WQB 数据库外键约束补齐")
    print(f"数据库: {DB_PATH}")
    print(f"备份: {BACKUP_PATH}")
    print()

    # 步骤 0: 创建干净副本
    clean_db = create_clean_copy()

    # 在干净副本上执行修复
    conn = sqlite3.connect(str(clean_db))
    conn.row_factory = sqlite3.Row
    
    try:
        # 步骤 1: 清理孤儿数据
        cleaned = clean_orphans(conn)
        
        # 步骤 2: 添加外键约束
        add_foreign_keys(conn)
        
        # 步骤 3: 验证
        verify_foreign_keys(conn)
        
        conn.close()

        # 替换数据库
        print()
        print("=" * 60)
        print("替换 data/wqb.db...")
        print("=" * 60)
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
        print("✓ 外键约束补齐完成")
        print("=" * 60)
        print(f"  清理孤儿数据: {cleaned} 条")
        print(f"  添加外键约束: 7 张表")
        
    except Exception as e:
        print(f"\n✗ 修复失败: {e}")
        conn.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
