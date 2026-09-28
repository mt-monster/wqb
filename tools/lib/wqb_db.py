# -*- coding: utf-8 -*-
"""wqb_db.py - tools 层兼容 re-export（2026-09-20 L1 升级）。

规范工厂已上移 ``src/wqb/db_conn.py``（WAL + busy_timeout=60s）。
本文件保留 ``get_conn`` / ``DB_PATH`` 旧接口签名，内部转发工厂，
存量 ``from wqb_db import get_conn`` 调用方零改动获得新口径。

历史背景（2026-09-07 P1.4）：70+ 裸 sqlite3.connect 未启用 foreign_keys
产生孤儿行，当时以本文件为工厂收敛；2026-09-20 并发锁审计
（reports/db_concurrent_write_lock_audit_20260920.md）将工厂上移 src
并统一 busy_timeout=60s，本文件转为兼容层。
"""
import os
import sys
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent.parent      # tools/
_REPO_SRC = _TOOLS_DIR.parent / "src"
if str(_REPO_SRC) not in sys.path:
    sys.path.insert(0, str(_REPO_SRC))

from wqb.db_conn import connect as _connect  # noqa: E402

DB_PATH = os.path.join(str(_TOOLS_DIR.parent), "data", "wqb.db")


def get_conn(db_path=None, timeout=60.0):
    """兼容接口：转发规范工厂（WAL + busy_timeout=timeout*1000 + foreign_keys）。"""
    return _connect(db_path or DB_PATH, timeout=timeout)
