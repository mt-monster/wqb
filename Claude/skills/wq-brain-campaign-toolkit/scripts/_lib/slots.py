# -*- coding: utf-8 -*-
"""_lib/slots.py - 账户级回测槽位仲裁（跨进程，2026-09-19）。

背景：pipeline.py 每个进程各自锁 n_slots=min(7, 批数)，两条流水线同跑（IND w171 + JPN w8
实测）在飞 10-13 个 multisim，超过 wqb-concurrency §8 实测的账户级 C≈7；此前只能靠 429 退避
被动兜底，没有主动仲裁。

实现：目录 `<repo>/logs/_slots/` 下每个在飞 multisim 一个 token 文件（内容 pid/msid/时间戳），
提交前 `acquire()` 数一遍活 token，≥cap 则等待（轮询），拿到即写 token；terminal 后 `release()`
删 token。陈旧 token（进程已死 或 超过 max_age 秒）自动回收，避免崩溃残留占坑。
纯标准库；任何异常都降级为"不仲裁"（打印 warn），绝不阻断提交。

环境变量：WQB_GLOBAL_SLOTS（cap，缺省 7；0 关闭）、WQB_SLOTS_DIR（目录）。
"""
from __future__ import annotations

import os
import sys
import threading
import time
import uuid

#: 进程内串行化 acquire 的"数 token → 建 token"临界区（ThreadPool 并行提交时 6 个线程同时数到 1 就一起冲过 cap）
_ACQ_LOCK = threading.Lock()

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "..", "..", "..", "..", ".."))


def slots_dir():
    if os.environ.get("WQB_SLOTS_DIR"):
        return os.environ["WQB_SLOTS_DIR"]
    # 工作区根优先取环境变量（skill 装在 ~/.claude/skills 时 __file__ 上溯不到仓库）
    root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or _REPO_ROOT
    if not os.path.isdir(os.path.join(root, "logs")):
        for cand in (r"D:\coding\traeCN_project\wqb",):
            if os.path.isdir(os.path.join(cand, "logs")):
                root = cand
                break
    return os.path.join(root, "logs", "_slots")


def global_cap():
    try:
        return int(os.environ.get("WQB_GLOBAL_SLOTS", "7"))
    except ValueError:
        return 7


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not h:
                return False
            try:
                code = ctypes.c_ulong()
                ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(code))
                return bool(ok) and code.value == 259  # STILL_ACTIVE
            finally:
                ctypes.windll.kernel32.CloseHandle(h)
        except Exception:
            return True  # 判不了就当活着（保守：不误回收）
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _read_token(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            parts = f.read().strip().split("|")
        pid = int(parts[0]) if parts and parts[0].isdigit() else 0
        ts = float(parts[2]) if len(parts) > 2 else 0.0
        return pid, (parts[1] if len(parts) > 1 else ""), ts
    except Exception:
        return 0, "", 0.0


def live_tokens(max_age_sec: int = 6 * 3600):
    """返回活 token 路径列表；顺手回收陈旧 token（进程已死或超龄）。"""
    d = slots_dir()
    if not os.path.isdir(d):
        return []
    now = time.time()
    alive = []
    for name in os.listdir(d):
        if not name.endswith(".slot"):
            continue
        p = os.path.join(d, name)
        pid, _, ts = _read_token(p)
        stale = (ts and now - ts > max_age_sec) or (pid and not _pid_alive(pid))
        if stale:
            try:
                os.remove(p)
            except OSError:
                pass
            continue
        alive.append(p)
    return alive


def acquire(label: str = "", cap: int | None = None, wait_sec: int = 1800, poll_sec: float = 10.0,
            log=print):
    """拿一个账户级槽位。返回 token 路径（release 用）；cap<=0 时返回 None（不仲裁）。
    等待超时也返回 None（降级为不仲裁，绝不阻断提交）。"""
    cap = global_cap() if cap is None else cap
    if cap <= 0:
        return None
    d = slots_dir()
    try:
        os.makedirs(d, exist_ok=True)
    except OSError as e:
        log(f"[slots] 目录不可用，降级不仲裁: {e}")
        return None
    deadline = time.time() + wait_sec
    warned = False
    while True:
        with _ACQ_LOCK:
            n = len(live_tokens())
            if n < cap:
                path = os.path.join(d, f"{int(time.time())}_{os.getpid()}_{uuid.uuid4().hex[:6]}.slot")
                try:
                    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(f"{os.getpid()}|{label}|{time.time()}")
                    return path
                except OSError:
                    continue  # 极小概率撞名，重试
        if not warned:
            log(f"[slots] 账户级在飞 {n} >= cap {cap}，等待其它流水线释放槽位…")
            warned = True
        if time.time() > deadline:
            log(f"[slots] 等待 {wait_sec}s 超时，降级为不仲裁提交")
            return None
        time.sleep(poll_sec)


def release(token_path):
    if not token_path:
        return
    try:
        os.remove(token_path)
    except OSError:
        pass


def relabel(token_path, label: str):
    """提交成功后把 msid 写进 token（便于排障：谁占着坑）。"""
    if not token_path:
        return
    try:
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(f"{os.getpid()}|{label}|{time.time()}")
    except OSError:
        pass


def status():
    """给排障用：当前活 token 列表。"""
    out = []
    for p in live_tokens():
        pid, label, ts = _read_token(p)
        out.append({"pid": pid, "label": label, "age_sec": int(time.time() - ts) if ts else None})
    return out


if __name__ == "__main__":  # python _lib/slots.py → 打印当前占坑情况
    import json
    print(json.dumps({"cap": global_cap(), "dir": slots_dir(), "live": status()},
                     ensure_ascii=False, indent=1))
    sys.exit(0)
