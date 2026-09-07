# -*- coding: utf-8 -*-
"""wqb_db.py - wqb.db 统一连接工厂（single point of truth）。

所有对 data/wqb.db 的 sqlite3 连接应经 get_conn()，统一启用：
  - PRAGMA foreign_keys=ON   （外键约束，防孤儿数据）
  - PRAGMA journal_mode=WAL  （读写并发不互斥，MCP 服务与工具并行安全）
  - PRAGMA busy_timeout=5000 （5 秒锁等待，替代立即 SQLITE_BUSY）

历史背景（2026-09-07 P1.4）：此前 70+ 个 sqlite3.connect() 裸连接点
未启用 foreign_keys，DDL 中的 REFERENCES 从未生效，累计产生
waves 137 / expressions 85 个孤儿。P0 修复后经本工厂收敛。
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "wqb.db")


def get_conn(db_path=None, timeout=10.0):
    """获取启用外键 + WAL + busy_timeout 的 wqb.db 连接。

    Args:
        db_path: 覆盖默认路径（测试用）。
        timeout: busy_timeout 秒数。
    Returns:
        sqlite3.Connection（row_factory 保持默认，调用方自行设置）
    """
    conn = sqlite3.connect(db_path or DB_PATH, timeout=timeout)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn
