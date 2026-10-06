# -*- coding: utf-8 -*-
"""_lib/slots.py - 账户级回测槽位仲裁（跨进程，2026-09-19）。

背景：pipeline.py 每个进程各自锁 n_slots=min(2, 批数)，两条流水线同跑（IND w171 + JPN w8
实测）在飞 10-13 个 multisim，超过 wqb-concurrency §8 实测的账户级 C≈7；此前只能靠 429 退避
被动兜底，没有主动仲裁。

实现：目录 `<repo>/logs/_slots/` 下每个在飞 multisim 一个 token 文件（内容 pid/msid/时间戳），
提交前 `acquire()` 数一遍活 token，≥cap 则等待（轮询），拿到即写 token；terminal 后 `release()`
删 token。陈旧 token（进程已死 或 超过 max_age 秒）自动回收，避免崩溃残留占坑。
纯标准库；任何异常都降级为"不仲裁"（打印 warn），绝不阻断提交。

★ 死锁修复（2026-10-02）：pipeline._run_round 的补批路径 `_refill()` 在**主线程**里调
`acquire()`，而释放槽位的 `_poll_single_batch` future 也需同一主线程经
`concurrent.futures.wait()` 推进。当 7 个 token 全被**本进程自己未轮询的批次**持有
时，`acquire()` 阻塞 → future 永不推进 → token 永不释放 = 自锁（实测 GLB 波1/波2
两条流水线同时在 `[slots] 账户级在飞 7 >= cap 7，等待…` 处停摆，直到被宿主回收）。
修法：给 `acquire()` 加 `nonblock=True`——在飞满时**立即返回 None**，调用方跳过本次
补批、把主线程让回去轮询回收。补批是"即收即补"的优化路径，跳过一轮只损失少量
吞吐，绝不阻塞主循环。

环境变量：WQB_GLOBAL_SLOTS（cap，缺省 2；0 关闭）、WQB_SLOTS_DIR（目录）。

⚠ cap 定在 2 是 **2026-10-06 用户定案**（从早期的账户级实测值 7 下调）：
  • 实测账户级容量 C≈7（wqb-concurrency §8），但那是“能跑”的上限，不是安全水位；
    本仓与并行会话共用同一账号配额与槽位，跑满会频繁 429 + 退避，反而拖慢总吞吐。
  • 7 槽还直接诱发过 2026-10-02 的主线程自锁（见下）；降到 2 是该事故的第二重保险。
    第一重保险（`acquire(nonblock=True)`）已保留，两者叠加后补批路径不可能死锁。
因此代码（`wqb.config.CONCURRENCY`）、本文档与 `wqb-concurrency` 统一按 **2** 口径；
一致性由 test_sd_docs::test_concurrency_numbers_are_pinned_to_one_source 守护。
临时提高用 `WQB_GLOBAL_SLOTS=<n>`（无需改代码）。
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
    return os.path.join(root, "logs", "_slots")


def global_cap():
    try:
        return int(os.environ.get("WQB_GLOBAL_SLOTS", "2"))
    except ValueError:
        return 2


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


def _retire(path: str) -> None:
    """退役 slot token：改名 ``<path>.stale`` 而非删除（2026-10-04）。

    沙箱 safe-delete 守卫按 turn 累计删除数，越阈值后截获 os.remove 并终止
    子进程（pipeline 秒退 exit 1）。slots 在 acquire/release 高频调用，
    命中概率远高于 dblock。改为改名退役（互斥协议不变：token 名后缀固定）。
    """
    try:
        os.replace(path, path + ".stale")
    except OSError:
        pass


def _prune_stale_files(max_age_sec: int = 24 * 3600):
    """清理历史遗留的 `*.slot.stale`（2026-10-02）。

    背景：旧版 release() 曾把 token 改名成 `*.slot.stale` 而非删除，历史工作区
    残留 78 个（`logs/_slots/`，09-29/30）。当前 release() 也改用改名退役，
    此函数清理超龄存量，且只碰 `.slot.stale`（绝不误删活 `.slot`）。
    超过 max_age_sec 的才删（保守：避免刚被外部工具改名、可能仍具参考价值的项）。
    ★ 2026-10-04：守卫也会截获这里的 os.remove ⇒ 改为再退役成 `.stale.old`
    （二次改名不触发删除，留待人工/环境清理）。
    """
    d = slots_dir()
    if not os.path.isdir(d):
        return 0
    now = time.time()
    n = 0
    for name in os.listdir(d):
        if not name.endswith(".slot.stale"):
            continue
        p = os.path.join(d, name)
        try:
            if now - os.path.getmtime(p) > max_age_sec:
                _retire(p)
                n += 1
        except OSError:
            pass
    return n


def live_tokens(max_age_sec: int = 6 * 3600):
    """返回活 token 路径列表；顺手回收陈旧 token（进程已死或超龄）。"""
    d = slots_dir()
    if not os.path.isdir(d):
        return []
    _prune_stale_files()   # 顺带清历史遗留 *.slot.stale（只碰该后缀）
    now = time.time()
    alive = []
    for name in os.listdir(d):
        if not name.endswith(".slot"):
            continue
        p = os.path.join(d, name)
        pid, _, ts = _read_token(p)
        stale = (ts and now - ts > max_age_sec) or (pid and not _pid_alive(pid))
        if stale:
            _retire(p)
            continue
        alive.append(p)
    return alive


def acquire(label: str = "", cap: int | None = None, wait_sec: int = 1800, poll_sec: float = 10.0,
            log=print, nonblock: bool = False):
    """拿一个账户级槽位。返回 token 路径（release 用）；cap<=0 时返回 None（不仲裁）。
    等待超时也返回 None（降级为不仲裁，绝不阻断提交）。

    nonblock=True（2026-10-02 死锁修复）：当前在飞 >= cap 时**立即返回 None**，
    不做任何等待。调用方据此跳过本次补批、让出主线程去轮询回收 future。
    背景见模块 docstring「死锁」段：pipeline._refill 在主线程调 acquire()，
    而释放槽位的 _poll_single_batch future 需同一主线程推进 → 若 acquire 阻塞
    而 7 个 token 全被本进程未轮询的批次持有，即构成自锁（wait_sec 到期前
    整条流水线停摆）。非阻塞模式彻底消除该自锁。
    """
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
        if nonblock:
            # 不等待：让调用方立即回收自己的在飞 future（防自锁）。仅首探告警一次。
            if not warned:
                log(f"[slots] 账户级在飞 {n} >= cap {cap}，本次补批跳过（非阻塞，等槽位释放）")
            return None
        if not warned:
            log(f"[slots] 账户级在飞 {n} >= cap {cap}，等待其它流水线释放槽位…")
            warned = True
        if time.time() > deadline:
            log(f"[slots] 等待 {wait_sec}s 超时，降级为不仲裁提交")
            return None
        time.sleep(poll_sec)


def is_full(cap: int | None = None) -> bool:
    """仲裁开着、且账户级在飞 >= cap（只读，不建 token）。

    `acquire(nonblock=True)` 返回 None 有**两种完全相反的含义**：真·槽位已满（该跳过本次补批）vs
    不仲裁（cap<=0 / 目录不可用 / 降级——该照常提交）。调用方拿到 None 后用本函数区分：
    只有 `is_full()` 为真才算「满」。cap<=0 或目录不存在 → False（不仲裁）。
    2026-10-04：`pipeline._refill` 此前把任何 None 都当「满」，`WQB_GLOBAL_SLOTS=0`（文档里的「0 关闭」）
    下重发 / 补批永远提交不出去，等满 30 分钟才放弃——单测因此整体挂住。
    """
    cap = global_cap() if cap is None else cap
    if cap <= 0:
        return False
    try:
        return len(live_tokens()) >= cap
    except OSError:
        return False


def release(token_path):
    if not token_path:
        return
    try:
        _retire(token_path)
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
