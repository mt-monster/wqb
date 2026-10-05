# -*- coding: utf-8 -*-
"""_lib.db — toolkit 统一 wqb.db 连接工厂（2026-09-20 L1 收口）。

与规范工厂 ``src/wqb/db_conn.py`` 同口径（WAL + busy_timeout=60s +
foreign_keys=ON + synchronous=NORMAL）。toolkit 脚本运行于各自安装位、
拿不到仓库 src，故此处落地同构实现；两端由
``tests/unit/01_store_db/test_db_write_guards.py`` 的 PRAGMA 等价守卫共同看护。
"""
import os
import sqlite3
from pathlib import Path

_DEFAULT_REL = Path("data") / "wqb.db"


def default_db_path(workspace_root=None):
    """与 src/wqb/db_conn.default_db_path 同口径。"""
    env = os.environ.get("WQB_DB_PATH")
    if env:
        return env
    if workspace_root:
        return str(Path(workspace_root) / _DEFAULT_REL)
    here = Path(__file__).resolve()
    for parent in here.parents:
        cand = parent / _DEFAULT_REL
        if cand.exists() or (parent / "src" / "wqb").is_dir():
            return str(parent / _DEFAULT_REL)
    return str(Path.cwd() / _DEFAULT_REL)


def connect(db=None, timeout=60.0, row_factory=None):
    """规范 wqb.db 连接（同 src/wqb/db_conn.connect）。"""
    conn = sqlite3.connect(db or default_db_path(), timeout=timeout)
    if row_factory is not None:
        conn.row_factory = row_factory
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)}")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn
