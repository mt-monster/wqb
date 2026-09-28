# -*- coding: utf-8 -*-
"""db_write_lock — wqb.db 写库互斥（文件 token，跨进程，2026-09-20 L3）。

背景（reports/db_concurrent_write_lock_audit_20260920.md）：多会话并发下
WAL 单写者被长事务占据，其余写者各自 ``busy_timeout`` 超时报错。本模块
把「写库流程」串行化：流程开始前抢 token，结束释放；竞争者有序轮询等待
而非盲目撞锁。

设计（与 ``_lib/slots.py`` 同哲学）：
  - token 文件：``logs/_dblock/dbwrite.lock.json``（O_CREAT|O_EXCL 原子创建，单文件锁）
  - TTL 自愈：mtime 超过 ttl 的 token 视为持有者已死，自动回收（崩溃不留死锁）
  - 重入：同 (pid, tag) 再 acquire 视为续约（重写 token 延长 mtime）
  - 降级：任何异常 → 打印 warn 并放行（绝不阻断主流程）；``WQB_DBLOCK_DISABLE=1`` 关闭
  - **不能用 DB ledger 实现 mutex**：抢 mutex 本身也是写库（自举悖论），故用文件锁

环境变量：``WQB_DBLOCK_DIR``（目录）、``WQB_DBLOCK_DISABLE=1``（关闭）、
``WQB_ROOT``（仓库根探测，同 slots.py）。

用法::

    from wqb.db_write_lock import write_lock

    with write_lock(tag="wave_gate_GBR_64", ttl_sec=900):
        ...  # 写库流程（gate_results / expressions 批量写等）
"""
from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "..", ".."))
_POLL_SEC = 2.0


def lock_dir():
    if os.environ.get("WQB_DBLOCK_DIR"):
        return os.environ["WQB_DBLOCK_DIR"]
    root = os.environ.get("WQB_ROOT") or _REPO_ROOT
    if not os.path.isdir(os.path.join(root, "logs")):
        for cand in (r"D:\coding\traeCN_project\wqb",):
            if os.path.isdir(os.path.join(cand, "logs")):
                root = cand
                break
    return os.path.join(root, "logs", "_dblock")


def _prune_expired(d: str, ttl_sec: float) -> None:
    """回收过期 token（持有者崩溃/TTL 超时）。unlink 幂等，竞争安全。"""
    now = time.time()
    try:
        names = os.listdir(d)
    except OSError:
        return
    for name in names:
        if not name.endswith(".json"):
            continue
        p = os.path.join(d, name)
        try:
            if now - os.path.getmtime(p) > ttl_sec:
                os.unlink(p)
        except OSError:
            pass  # 已被其他竞争者回收



def _pid_alive(pid) -> bool:
    """持有者进程是否存活（2026-09-20 补：死 pid 的 token 立即回收，不等 TTL）。

    实证：GLB 三条 pipeline 因一个已退出的 build_wave 持有者（pid 18224）各等满
    90-120s 才降级放行；TTL 900s 内所有写者都被拖慢，detached 任务 stdout 长期为空
    被误判为"僵死"。判不出存活（异常）时按存活处理，交给 TTL 兜底。
    """
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return True
    if pid <= 0:
        return True
    try:
        if os.name == "nt":
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            k32 = ctypes.windll.kernel32
            h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not h:
                return False  # 打不开 = 不存在（拒绝访问时也当存活以免误杀，见下）
            try:
                code = ctypes.c_ulong()
                if k32.GetExitCodeProcess(h, ctypes.byref(code)):
                    return code.value == STILL_ACTIVE
                return True
            finally:
                k32.CloseHandle(h)
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False
    except Exception:
        return True


def _reclaim_dead_holder(tok: str) -> bool:
    """token 持有者 pid 已死则删除 token；返回是否回收了。"""
    try:
        with open(tok, "r", encoding="utf-8") as f:
            cur = json.load(f)
        pid = cur.get("pid")
        if pid is not None and not _pid_alive(pid):
            os.unlink(tok)
            print(f"[dblock] 回收死持有者 token（pid={pid} tag={cur.get('tag')}）")
            return True
    except (OSError, ValueError):
        pass
    return False

def acquire(tag: str = "generic", ttl_sec: float = 900.0,
            wait_timeout: float = 90.0, owner: str = None) -> dict:
    """抢写锁 token；失败退避轮询至 wait_timeout；异常降级放行。

    互斥语义：单文件锁 ``dbwrite.lock.json``，``O_CREAT|O_EXCL`` 原子创建；
    持有者 = 文件内容中的 pid；同 pid 重入视为续约（utime 延长 TTL）。

    Returns:
        {"ok": bool, "token": path|None, "waited": float, "degraded": bool}
    """
    info = {"ok": True, "token": None, "waited": 0.0, "degraded": False}
    if os.environ.get("WQB_DBLOCK_DISABLE") == "1":
        return info
    pid = os.getpid()
    owner = owner or f"{pid}@{os.uname().nodename if hasattr(os, 'uname') else 'win'}"
    deadline = time.time() + max(wait_timeout, 0.0)
    d = lock_dir()
    tok = os.path.join(d, "dbwrite.lock.json")
    try:
        os.makedirs(d, exist_ok=True)
    except OSError as e:
        print(f"[dblock][WARN] 目录不可建，降级放行: {e}")
        info["degraded"] = True
        return info

    while True:
        try:
            _prune_expired(d, ttl_sec)
            _reclaim_dead_holder(tok)
            # 重入：文件存在且持有者是自己 → 续约
            try:
                with open(tok, "r", encoding="utf-8") as f:
                    cur = json.load(f)
                if cur.get("pid") == pid:
                    os.utime(tok, None)
                    info["token"] = tok
                    return info
            except (OSError, ValueError):
                pass  # 文件不存在或损坏 → 视为无主，走创建
            fd = os.open(tok, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, json.dumps({"owner": owner, "pid": pid, "tag": tag,
                                     "at": time.time()}).encode())
            os.close(fd)
            info["token"] = tok
            return info
        except FileExistsError:
            pass  # 他人持有 → 轮询等待
        except OSError as e:
            print(f"[dblock][WARN] token 写入失败，降级放行: {e}")
            info["degraded"] = True
            return info
        if time.time() >= deadline:
            print(f"[dblock][WARN] 等待 {wait_timeout}s 未获得写锁（tag={tag}），降级放行——"
                  f"持有者见 {tok}")
            info["degraded"] = True
            return info
        time.sleep(_POLL_SEC)
        info["waited"] = wait_timeout - max(0.0, deadline - time.time())


def release(token: str, pid: int = None) -> None:
    """释放写锁（幂等；仅当持有者是 pid 本人时删除，防误删他人）。"""
    if not token:
        return
    me = pid if pid is not None else os.getpid()
    try:
        with open(token, "r", encoding="utf-8") as f:
            cur = json.load(f)
        if cur.get("pid") == me:
            os.unlink(token)
    except (OSError, ValueError):
        pass


@contextmanager
def write_lock(tag: str = "generic", ttl_sec: float = 900.0,
               wait_timeout: float = 90.0, owner: str = None):
    """写库流程互斥上下文。降级时照常放行（不阻断）。"""
    info = acquire(tag=tag, ttl_sec=ttl_sec, wait_timeout=wait_timeout, owner=owner)
    try:
        yield info
    finally:
        release(info.get("token"))  # 仅当持有者是本人时删除
