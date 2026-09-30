# -*- coding: utf-8 -*-
"""db_conn — data/wqb.db 规范连接工厂（single point of truth，2026-09-20）。

背景（reports/db_concurrent_write_lock_audit_20260920.md）：
  多会话并发下 `database is locked` 事故的四个根因之一是裸
  ``sqlite3.connect`` 散布全库且 ``busy_timeout`` 不一（默认 5s~30s）。
  本模块是全库唯一允许直接调用 ``sqlite3.connect`` 打开 **wqb.db** 的地方。

规范（所有经本工厂的连接自动获得）：
  - ``journal_mode=WAL``      读写并发不互斥（幂等，持久化于库文件）
  - ``busy_timeout=60000``    写锁排队 60s（统一口径，替代 5s/10s/30s 不一）
  - ``foreign_keys=ON``       外键约束（2026-09-07 P1.4 起口径）
  - ``synchronous=NORMAL``    WAL 下安全且更快

守卫：``tests/unit/test_db_write_guards.py::test_no_naked_sqlite_connect``
静态扫描活跃目录，禁止白名单外出现 ``sqlite3.connect(``。

零依赖设计：本模块只 import 标准库；``default_db_path`` 与
``wqb.store._common`` 保持同口径（WQB_DB_PATH 环境变量优先），
但刻意复制而非 import，避免把轻量工具脚本拖进 store 包的 import 链。
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any, Optional

_DEFAULT_REL = Path("data") / "wqb.db"

#: 允许直接 ``sqlite3.connect`` 的文件（相对仓库根，/ 分隔）。静态守卫消费。
#: GEM/feature_engineering 三处为「无 src 依赖环境」的合规内联（已升级 PRAGMA），
#: 守卫要求其内容含 busy_timeout 以确保升级到位。
DIRECT_CONNECT_WHITELIST = (
    "src/wqb/db_conn.py",           # 本文件
    "wqb_db_mcp.py",                # MCP server 自管连接（配置同规范）
    "tools/lib/wqb_db.py",          # tools 层兼容 re-export
    "tools/shape_quota_check.py",   # 2026-09-28：只读配额检查器（ro URI，一次性诊断工具）
    "Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/db.py",  # toolkit 同构工厂
    "Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py",
    "Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py",
    "Claude/skills/brain-data-feature-engineering/scripts/feature_engineering.py",
)


def default_db_path(workspace_root: Optional[str] = None) -> str:
    """与 ``wqb.store._common.default_db_path`` 同口径的 DB 路径解析。

    优先级：``WQB_DB_PATH`` 环境变量 > workspace_root > 向上探测仓库根 >
    cwd/data/wqb.db。
    """
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


def connect(
    db: Optional[str] = None,
    timeout: float = 60.0,
    row_factory: Any = None,
    readonly: bool = False,
) -> sqlite3.Connection:
    """打开一个符合全库规范的 wqb.db 连接。

    Args:
        db: DB 路径；缺省走 :func:`default_db_path`（测试可传临时路径）。
        timeout: sqlite3 连接层 timeout（秒），同时写入 ``busy_timeout``。
            60s 覆盖已知的全部短事务竞争窗口；长事务应由
            ``wqb.store.db_write_mutex`` 调度而非拉长本参数。
        row_factory: 可选（如 ``sqlite3.Row``）。
        readonly: **只读工具必须传 True**（2026-09-20 补：step_funnel 只读契约）。
            置 True 时以 ``mode=ro`` URI 打开，并**跳过会改写库文件的
            ``PRAGMA journal_mode=WAL``**——WAL 是持久化的库级属性，一旦设置
            即使不写任何行也会改变 DB 文件字节，破坏
            ``tests/unit/test_step_funnel_p5.py::test_run_does_not_modify_db``。

    Returns:
        已应用规范 PRAGMA 的 ``sqlite3.Connection``。
    """
    path = db or default_db_path()
    if readonly:
        # as_uri() 正确处理 Windows 盘符、反斜杠与空格。
        conn = sqlite3.connect(f"{Path(path).as_uri()}?mode=ro", uri=True, timeout=timeout)
    else:
        conn = sqlite3.connect(path, timeout=timeout)
    if row_factory is not None:
        conn.row_factory = row_factory
    conn.execute("PRAGMA foreign_keys=ON")
    if not readonly:
        # journal_mode=WAL 幂等且持久化（库级）；只读连接必须跳过，否则改库字节。
        conn.execute("PRAGMA journal_mode=WAL")
    # busy_timeout 与连接 timeout 同口径（连接级，只读同样适用）。
    conn.execute(f"PRAGMA busy_timeout={int(timeout * 1000)}")
    if not readonly:
        conn.execute("PRAGMA synchronous=NORMAL")
    return conn
