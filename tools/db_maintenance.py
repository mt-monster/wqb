# -*- coding: utf-8 -*-
"""db_maintenance.py - wqb.db 维护工具（2026-09-20 L4）。

子命令：
  checkpoint   WAL checkpoint（默认 TRUNCATE，清 -wal 积压；需无活跃写者窗口）
  orphans      清理 MCP server 孤儿实例（wqb_db_mcp.py / brain main.py，
               PPID 已死 或 启动超 24h 且 PPID 非当前会话树）——psutil 可选
  lock-status  打印当前写锁 token（logs/_dblock/）

用法：
  python tools/db_maintenance.py checkpoint
  python tools/db_maintenance.py orphans --dry-run
  python tools/db_maintenance.py lock-status
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
from wqb.db_conn import connect as db_connect, default_db_path  # noqa: E402


def cmd_checkpoint(mode: str) -> int:
    db = default_db_path()
    conn = db_connect(db, timeout=15.0)
    try:
        t0 = time.time()
        row = conn.execute(f"PRAGMA wal_checkpoint({mode})").fetchone()
        busy, log_pages, ckpt_pages = row
        print(f"[checkpoint] mode={mode} busy={busy} log_pages={log_pages} "
              f"checkpointed={ckpt_pages} took={time.time()-t0:.2f}s")
        if busy:
            print("[checkpoint] 返回 busy=1：存在活跃读者/写者阻止完整 checkpoint"
                  "（TRUNCATE 需独占窗口，可稍后重试或用 PASSIVE）")
            return 1
        return 0
    finally:
        conn.close()


def _find_server_procs():
    try:
        import psutil
    except ImportError:
        print("[orphans] psutil 未安装（pip install psutil），跳过")
        return None
    targets = []
    for p in psutil.process_iter(["pid", "ppid", "name", "cmdline", "create_time", "ppid"]):
        try:
            # 只匹配 python 解释器进程——WorkBuddy.exe 等 GUI 进程的 cmdline
            # 也可能包含 MCP 配置路径关键词，误杀即杀掉用户桌面应用（2026-09-20）
            pname = (p.info.get("name") or "").lower()
            if "python" not in pname:
                continue
            cmd = " ".join(p.info.get("cmdline") or [])
            if ("wqb_db_mcp.py" in cmd) or ("world-quant-brain-mcp" in cmd and "main.py" in cmd):
                targets.append(p)
        except Exception:
            continue
    return targets


def cmd_orphans(dry_run: bool, max_age_h: float = 24.0) -> int:
    procs = _find_server_procs()
    if procs is None:
        return 2
    if not procs:
        print("[orphans] 未发现 MCP server 实例")
        return 0
    alive_parents = {p.pid for p in procs}
    orphans, keep = [], []
    for p in procs:
        ppid = p.info.get("ppid") or 0
        age_h = (time.time() - (p.info.get("create_time") or time.time())) / 3600
        # 孤儿判据：父进程已死（且父不是当前进程树）或实例超龄
        is_orphan = (ppid not in alive_parents and ppid != os.getpid()) or age_h > max_age_h
        (orphans if is_orphan else keep).append((p, ppid, age_h))
    print(f"[orphans] 共 {len(procs)} 个 MCP server：{len(orphans)} 孤儿 / {len(keep)} 存活")
    for p, ppid, age_h in orphans:
        cmd = " ".join(p.info.get("cmdline") or [])[:100]
        print(f"  ORPHAN pid={p.pid} ppid={ppid} age={age_h:.1f}h :: {cmd}")
        if not dry_run:
            try:
                p.terminate()
                print(f"  -> terminated {p.pid}")
            except Exception as e:
                print(f"  -> terminate 失败: {e}")
    for p, ppid, age_h in keep:
        cmd = " ".join(p.info.get("cmdline") or [])[:80]
        print(f"  keep    pid={p.pid} ppid={ppid} age={age_h:.1f}h :: {cmd}")
    return 0


def cmd_lock_status() -> int:
    tok = REPO / "logs" / "_dblock" / "dbwrite.lock.json"
    if not tok.is_file():
        print("[lock] 无持有者")
        return 0
    try:
        data = json.loads(tok.read_text(encoding="utf-8"))
        age = time.time() - tok.stat().st_mtime
        print(f"[lock] 持有者 owner={data.get('owner')} pid={data.get('pid')} "
              f"tag={data.get('tag')} age={age:.0f}s mtime={datetime.fromtimestamp(tok.stat().st_mtime)}")
        return 0
    except (OSError, ValueError) as e:
        print(f"[lock] token 读取失败: {e}")
        return 1


def main():
    ap = argparse.ArgumentParser(description="wqb.db 维护：WAL checkpoint / MCP 孤儿清理 / 锁状态")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("checkpoint")
    sp.add_argument("--mode", default="TRUNCATE", choices=("PASSIVE", "FULL", "RESTART", "TRUNCATE"))
    sp2 = sub.add_parser("orphans")
    sp2.add_argument("--dry-run", action="store_true")
    sp2.add_argument("--max-age-h", type=float, default=24.0)
    sub.add_parser("lock-status")
    a = ap.parse_args()
    if a.cmd == "checkpoint":
        sys.exit(cmd_checkpoint(a.mode))
    if a.cmd == "orphans":
        sys.exit(cmd_orphans(a.dry_run, a.max_age_h))
    if a.cmd == "lock-status":
        sys.exit(cmd_lock_status())


if __name__ == "__main__":
    main()
