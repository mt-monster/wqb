# -*- coding: utf-8 -*-
"""db_lock_audit.py - wqb.db 写锁探针（2026-09-20 L2）。

背景：多会话并发下 WAL 单写者被长事务占据（2026-09-20 实测 ≥30min），
当时靠进程 CPU 反推才定位。本工具常态化测量「写锁等待时长」并记录
持有者线索，事件写 **JSONL 文件**（logs/db_lock_events.jsonl）而非
DB——探针自身不得参与抢锁。

用法：
  python tools/db_lock_audit.py --once                 # 单轮测量（CI/pytest 可用）
  python tools/db_lock_audit.py --once --json          # 机器可读输出
  python tools/db_lock_audit.py --daemon --interval 30 # 常驻循环（默认 30s/轮）
  python tools/db_lock_audit.py --alert-sec 10         # 告警阈值（默认 10s）

单轮语义：
  1. 计时 ``BEGIN IMMEDIATE``（受 busy_timeout 约束，探针连接 timeout=15s）
  2. 立即 ROLLBACK（不真正写）
  3. wait >= alert_sec 视为告警事件；记录：等待秒数、锁 token 持有者
     （logs/_dblock/dbwrite.lock.json 内容）、当时活跃的 python 写者进程
     （psutil 可选，缺失则跳过）。
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

EVENTS_FILE = REPO / "logs" / "db_lock_events.jsonl"
LOCK_TOKEN = REPO / "logs" / "_dblock" / "dbwrite.lock.json"


def _snapshot_writers():
    """活跃 python 进程快照（psutil 可选）。"""
    try:
        import psutil  # noqa
    except ImportError:
        return None
    out = []
    for p in psutil.process_iter(["pid", "name", "cmdline", "cpu_times"]):
        try:
            name = (p.info.get("name") or "").lower()
            if "python" not in name:
                continue
            cmd = " ".join(p.info.get("cmdline") or [])
            if "wqb" in cmd.lower() or "pipeline" in cmd.lower():
                ct = p.info.get("cpu_times")
                out.append({"pid": p.info["pid"],
                            "cpu": round((ct.user + ct.system) if ct else 0, 1),
                            "cmd": cmd[:120]})
        except Exception:
            continue
    return out


def _lock_holder():
    try:
        with open(LOCK_TOKEN, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def probe_once(db_path=None, alert_sec=10.0, probe_timeout=15.0):
    """单轮写锁探针。返回事件 dict（wait_sec < alert 且无异常时 also 返回，便于基线）。"""
    t0 = time.time()
    wait = None
    err = None
    try:
        conn = db_connect(default_db_path() if db_path is None else db_path,
                          timeout=probe_timeout)
        try:
            conn.execute("PRAGMA busy_timeout=%d" % int(probe_timeout * 1000))
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("ROLLBACK")
        finally:
            conn.close()
    except sqlite3.OperationalError as e:
        err = str(e)
    wait = round(time.time() - t0, 3)
    event = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "wait_sec": wait,
        "alert": (err is not None) or (wait >= alert_sec),
        "error": err,
        "threshold": alert_sec,
        "dblock_holder": _lock_holder(),
        "writers": _snapshot_writers(),
    }
    return event


def append_event(event, path=EVENTS_FILE):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"[audit][WARN] 事件落盘失败: {e}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="wqb.db 写锁探针（事件写 JSONL，不占写锁）")
    ap.add_argument("--once", action="store_true", help="单轮测量后退出")
    ap.add_argument("--daemon", action="store_true", help="常驻循环")
    ap.add_argument("--interval", type=float, default=30.0, help="daemon 轮询间隔秒")
    ap.add_argument("--alert-sec", type=float, default=10.0, help="告警阈值秒")
    ap.add_argument("--max-runs", type=int, default=0, help="daemon 最大轮数（0=无限，测试用）")
    ap.add_argument("--json", action="store_true", help="stdout 输出 JSON")
    ap.add_argument("--db", default=None, help="覆盖 DB 路径（pytest 用）")
    a = ap.parse_args()

    def run_round():
        ev = probe_once(db_path=a.db, alert_sec=a.alert_sec)
        if ev["alert"]:
            append_event(ev)
        if a.json:
            print(json.dumps(ev, ensure_ascii=False))
        else:
            flag = "ALERT" if ev["alert"] else "ok"
            print(f"[audit] wait={ev['wait_sec']}s {flag}"
                  + (f" holder={ev['dblock_holder'].get('tag') if ev['dblock_holder'] else None}"
                     if ev["dblock_holder"] else "")
                  + (f" error={ev['error']}" if ev["error"] else ""))
        return ev

    if a.once or not a.daemon:
        ev = run_round()
        sys.exit(2 if ev["error"] else 0)
    runs = 0
    while True:
        run_round()
        runs += 1
        if a.max_runs and runs >= a.max_runs:
            break
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
