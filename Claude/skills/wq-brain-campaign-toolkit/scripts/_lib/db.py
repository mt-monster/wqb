# -*- coding: utf-8 -*-
"""_lib.db — toolkit 统一 wqb.db 连接工厂（2026-09-20 L1 收口）。

与规范工厂 ``src/wqb/db_conn.py`` 同口径（WAL + busy_timeout=60s +
foreign_keys=ON + synchronous=NORMAL）。toolkit 脚本运行于各自安装位、
拿不到仓库 src，故此处落地同构实现；两端由
``tests/unit/01_store_db/test_db_write_guards.py`` 的 PRAGMA 等价守卫共同看护。

⚠ **例外：测试期禁连生产库的判据不在这里复制**（2026-10-14 批次H / 10-15 补第三条路径）。
判定本体只有 ``wqb.db_conn.reject_production_db_under_tests`` 一份，本模块 ``connect()``
在可导入时委托它；判据一旦在这里出现第二份，「门面拦、store 放、toolkit 又放」那种
半边守住的老形状就会重演（守卫
``test_facade_and_store_share_one_implementation`` +
``test_toolkit_lib_db_delegates_to_core_guard``）。
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
    """规范 wqb.db 连接（同 src/wqb/db_conn.connect）。

    ⚠ 测试期禁连生产库这一条**不在这里再写一份判据**，而是委托规范核心
    ``wqb.db_conn.reject_production_db_under_tests``（2026-10-14 批次H）：
    门面与 ``CampaignStore`` 都被守住之后，toolkit 这条第三路径仍然静默写生产库
    —— ``_lib/ledger.py`` / ``_lib/registry.py`` / ``_lib/wave_results.py`` /
    ``_lib/region_gates.py`` 全都经本函数取连接，且都被 ``tests/`` 直接驱动
    （库里 2026-09-29 那批 ``wave_meta_covtest*`` / ``diversity_report_wcovtest*``
    就是这个形状写进去的）。判据只能有一份，否则早晚分叉。
    ImportError 只在「技能装在仓库外、``wqb`` 不可导入」时发生，那种场景下本函数
    服务的是真实战役运行而非 pytest，放行是设计内行为（守卫
    ``test_toolkit_lib_db_delegates_to_core_guard`` 钉住委托关系）。
    """
    target = db or default_db_path()
    try:
        from wqb.db_conn import reject_production_db_under_tests as _core_guard
    except Exception:  # pragma: no cover - 技能装在仓库外时走这里
        _core_guard = None
    if _core_guard is not None:
        _core_guard(target, entry="toolkit _lib.db")
    conn = sqlite3.connect(target, timeout=timeout)
    if row_factory is not None:
        conn.row_factory = row_factory
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)}")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn
