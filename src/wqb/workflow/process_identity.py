"""Read process identity without shelling out or relying on PID liveness alone."""
from __future__ import annotations

import os
from pathlib import Path


def process_identity(pid):
    """Return creation time and executable; inaccessible cases are unknown."""
    if not pid:
        return None
    try:
        if os.name == "nt":
            import ctypes
            from ctypes import wintypes
            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel.OpenProcess.restype = wintypes.HANDLE
            kernel.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
            kernel.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD,
                                                         wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
            handle = kernel.OpenProcess(0x1000, False, int(pid))
            if not handle:
                return None
            try:
                creation, exit_time, system, user = (wintypes.FILETIME() for _ in range(4))
                if not kernel.GetProcessTimes(handle, ctypes.byref(creation), ctypes.byref(exit_time),
                                              ctypes.byref(system), ctypes.byref(user)):
                    return None
                ticks = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
                buf, size = ctypes.create_unicode_buffer(32768), wintypes.DWORD(32768)
                exe = (buf.value if kernel.QueryFullProcessImageNameW(handle, 0, buf, ctypes.byref(size))
                       else None)
                return {"created_at": ticks / 10_000_000 - 11644473600, "executable": exe}
            finally:
                kernel.CloseHandle(handle)
        stat = Path(f"/proc/{int(pid)}/stat").read_text()
        start_ticks = int(stat[stat.rfind(")") + 2:].split()[19])
        boot = next(int(s.split()[1]) for s in Path("/proc/stat").read_text().splitlines()
                    if s.startswith("btime "))
        return {"created_at": boot + start_ticks / os.sysconf("SC_CLK_TCK"),
                "executable": os.readlink(f"/proc/{int(pid)}/exe")}
    except (OSError, ValueError, StopIteration, IndexError):
        return None


def match_process(meta, observed):
    """Compare saved identity, or legacy launch time, with the live process."""
    if not observed:
        return None
    saved = meta.get("process_identity") or {}
    expected = saved.get("created_at")
    tolerance = 0.05
    if expected is None:
        from datetime import datetime
        try:
            expected = datetime.fromisoformat(meta["started_at"]).timestamp()
        except (KeyError, ValueError, TypeError):
            return None
        tolerance = 5.0  # legacy timestamps were recorded just after Popen
    if abs(float(observed["created_at"]) - float(expected)) > tolerance:
        return False
    expected_exe = saved.get("executable")
    if not expected_exe and isinstance(meta.get("cmd"), list) and meta["cmd"]:
        expected_exe = meta["cmd"][0]
    if expected_exe and observed.get("executable"):
        norm = lambda s: os.path.normcase(os.path.normpath(s))
        actual = observed["executable"]
        if os.path.isabs(expected_exe):
            if norm(expected_exe) != norm(actual):
                return False
        elif norm(os.path.basename(expected_exe)) != norm(os.path.basename(actual)):
            return False
    return True
