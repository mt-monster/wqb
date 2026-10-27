# -*- coding: utf-8 -*-
"""单实例锁：同一区域只允许一个 supervisor、一个 campaign（EUR 只有一条车道）。

为什么需要（2026-10-25 事故）
------------------------------
同一份 EUR 断点上一度叠了 3 个 campaign：误用 `ps -W` 判定"进程已死"，
于是反复重启。checkpoint/results 是**无锁的 load→modify→save**，
多写者会丢更新、可能写出重复 done —— 事后只能靠人工比对。

设计
----
* 锁文件放在 `<repo>/cache/lane_<REGION>_<role>.lock`，内容是 PID。
* `O_CREAT|O_EXCL` 原子创建；已存在时读 PID：
  - PID 仍存活 ⇒ 抛 `AlreadyRunning`（调用方应退出，不要抢）
  - PID 已死（被强杀留下的残锁）⇒ 视为陈旧，接管并覆写
* 存活判定不用 psutil：Windows 下 `os.kill(pid, 0)` 对不存在进程抛 OSError；
  POSIX 同理。够用且零依赖。
* 进程正常退出时在 finally 里释放；被强杀则留残锁，下次启动自动接管。
"""
import os

from .config import REGION, ROOT


class AlreadyRunning(RuntimeError):
    pass


def _lock_path(role):
    tag = REGION
    return os.path.join(ROOT, "cache", f"lane_{tag}_{role}.lock")


def _alive(pid):
    """判断 PID 是否存活。

    ⚠ 2026-10-25 实测教训：**Windows 上不能用 `os.kill(pid, 0)` 判活**。
    ① Python 在 Windows 上把非 CTRL_* 信号一律交给 TerminateProcess（有误杀风险）；
    ② 即使不误杀，权限不足时抛 `PermissionError`（是 `OSError` 子类），
       会被当成"进程已死" ⇒ 把别人的锁当陈旧残锁删掉并抢走（今天真实发生，误删了 supervisor 锁）。
    改用 Win32 `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` + `GetExitCodeProcess`：
    打不开时用 GetLastError 区分「不存在」与「权限不足（存在）」。
    """
    if not pid or pid <= 0:
        return False
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        k32.OpenProcess.restype = wintypes.HANDLE
        k32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        k32.GetExitCodeProcess.restype = wintypes.BOOL
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        ERROR_ACCESS_DENIED = 5
        h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not h:
            return ctypes.get_last_error() == ERROR_ACCESS_DENIED
        try:
            code = wintypes.DWORD()
            if not k32.GetExitCodeProcess(h, ctypes.byref(code)):
                return True          # 查不到退出码：保守认为活着
            return code.value == STILL_ACTIVE
        finally:
            k32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True                  # 存在但没权限 → 活着
    except Exception:
        return True                  # 无法确认 → 保守认为活着
    return True


class InstanceLock:
    """with InstanceLock("supervisor"): ...  —— 退出时释放。"""

    def __init__(self, role):
        self.role = role
        self.path = _lock_path(role)
        self.pid = os.getpid()
        self.acquired = False

    def __enter__(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(self.pid).encode())
                os.close(fd)
                self.acquired = True
                return self
            except FileExistsError:
                old = 0
                try:
                    old = int(open(self.path, encoding="utf-8").read().strip() or 0)
                except Exception:
                    pass
                if _alive(old):
                    raise AlreadyRunning(
                        f"{self.role} 已在运行（PID {old}，锁 {self.path}）"
                        f"⇒ 拒绝启动，避免同一断点上双写")
                # 陈旧残锁：接管
                try:
                    os.remove(self.path)
                except OSError:
                    pass
        raise AlreadyRunning(f"{self.role} 锁获取失败：{self.path}")

    def __exit__(self, *exc):
        if self.acquired:
            try:
                if int(open(self.path, encoding="utf-8").read().strip() or 0) == self.pid:
                    os.remove(self.path)
            except Exception:
                pass
            self.acquired = False
        return False


def status():
    """调试用：当前各角色的锁持有者。"""
    out = {}
    for role in ("supervisor", "campaign"):
        p = _lock_path(role)
        pid = 0
        try:
            pid = int(open(p, encoding="utf-8").read().strip() or 0)
        except Exception:
            pass
        out[role] = {"path": p, "pid": pid, "alive": _alive(pid)}
    return out
