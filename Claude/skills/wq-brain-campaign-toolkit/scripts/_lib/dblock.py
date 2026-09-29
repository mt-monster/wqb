# -*- coding: utf-8 -*-
"""_lib/dblock.py - wqb.db 写库互斥（文件 token，2026-09-20 L3）。

与规范实现 ``src/wqb/db_write_lock.py`` 同构（toolkit 安装位拿不到仓库 src，
故落地同构版本；两端由 tests/unit/test_db_write_guards.py 行为守卫看护）。

设计：单文件锁 ``logs/_dblock/dbwrite.lock.json``，O_CREAT|O_EXCL 原子创建；
TTL 自愈（mtime 超时回收，崩溃不留死锁）；同 pid 重入=续约；任何异常降级
放行（绝不阻断主流程）。不能用 DB ledger 实现（抢锁本身是写库，自举悖论）。

环境变量：WQB_DBLOCK_DIR / WQB_DBLOCK_DISABLE=1 / WQB_ROOT（同 slots.py）。
"""
from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager

_POLL_SEC = 2.0

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "..", "..", "..", "..", ".."))


def lock_dir():
    if os.environ.get("WQB_DBLOCK_DIR"):
        return os.environ["WQB_DBLOCK_DIR"]
    root = os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT") or _REPO_ROOT
    return os.path.join(root, "logs", "_dblock")


def _prune_expired(d, ttl_sec):
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
            pass



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

def acquire(tag="generic", ttl_sec=900.0, wait_timeout=90.0, owner=None):
    info = {"ok": True, "token": None, "waited": 0.0, "degraded": False}
    if os.environ.get("WQB_DBLOCK_DISABLE") == "1":
        return info
    pid = os.getpid()
    owner = owner or f"{pid}"
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
            try:
                with open(tok, "r", encoding="utf-8") as f:
                    cur = json.load(f)
                if cur.get("pid") == pid:
                    os.utime(tok, None)
                    info["token"] = tok
                    return info
            except (OSError, ValueError):
                pass
            fd = os.open(tok, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, json.dumps({"owner": owner, "pid": pid, "tag": tag,
                                     "at": time.time()}).encode())
            os.close(fd)
            info["token"] = tok
            return info
        except FileExistsError:
            pass
        except OSError as e:
            print(f"[dblock][WARN] token 写入失败，降级放行: {e}")
            info["degraded"] = True
            return info
        if time.time() >= deadline:
            print(f"[dblock][WARN] 等待 {wait_timeout}s 未获得写锁（tag={tag}），降级放行")
            info["degraded"] = True
            return info
        time.sleep(_POLL_SEC)
        info["waited"] = wait_timeout - max(0.0, deadline - time.time())


def release(token, pid=None):
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
def write_lock(tag="generic", ttl_sec=900.0, wait_timeout=90.0, owner=None):
    info = acquire(tag=tag, ttl_sec=ttl_sec, wait_timeout=wait_timeout, owner=owner)
    try:
        yield info
    finally:
        release(info.get("token"))  # 仅当持有者是本人时删除
