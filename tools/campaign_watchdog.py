"""campaign_watchdog.py — 心跳看门狗（2026-10-23 缺陷6）

背景：2026-10-22 夜间流水线在 news54 之后**静默退出**（stderr 为空、断点完整），
停了 4 小时无人发现。原因多半是后台 shell 生命周期结束把子进程带走。

判据：心跳文件 stale（> STALE 秒未更新）且心跳里的 pid 已不存在 ⇒ 按心跳记录的 argv 重启。
心跳由 full_template_campaign.beat() 在每个集开始/结束写入（cache/campaign_heartbeat.json）。

用法：
    python tools/campaign_watchdog.py            # 前台循环（120s 一次）
    schtasks /Create /TN WQB_Campaign_Watchdog /TR "<venv> <abs path>" /SC MINUTE /MO 10 /F   # 常驻
"""
import ctypes
import json
import os
import subprocess
import sys
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HB = os.path.join(ROOT, "cache", "campaign_heartbeat.json")
LOG = os.path.join(ROOT, "cache", "campaign_run.log")
WD_LOG = os.path.join(ROOT, "cache", "watchdog.log")
VENV_PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
CAMPAIGN = os.path.join(ROOT, "tools", "full_template_campaign.py")
STALE_SEC = 900          # 15 分钟无心跳 = 可疑
INTERVAL = 120

# 2026-10-28：Windows 下所有子进程必须隐藏窗口。
# 计划任务设为 Hidden=True 只能隐藏"任务本体"的窗口，脚本内部再 spawn 的
# powershell / python 子进程仍会各自弹一个控制台窗口 —— 实测每 10 分钟闪一次。
CREATE_NO_WINDOW = 0x08000000
_NO_WINDOW = CREATE_NO_WINDOW if os.name == "nt" else 0


def _log(msg):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line)
    try:
        with open(WD_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def pid_alive(pid):
    """跨平台判活。Windows 上 os.kill(pid, 0) 会 TerminateProcess，绝不能用。"""
    if not pid:
        return False
    if os.name == "nt":
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if h:
            ctypes.windll.kernel32.CloseHandle(h)
            return True
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except OSError:
        return False


def campaign_running():
    """除心跳 pid 外，再兜底扫一遍进程（防止心跳 pid 记录滞后）。"""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -like '*full_template_campaign*' } | "
             "Measure-Object).Count"],
            capture_output=True, text=True, timeout=60,
            creationflags=_NO_WINDOW).stdout.strip()
        return out.isdigit() and int(out) > 0
    except Exception:
        return False


def read_hb():
    try:
        with open(HB, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def restart(argv):
    cmd = [VENV_PY, CAMPAIGN] + list(argv or [])
    _log(f"重启流水线：{' '.join(cmd[1:])}")
    flags = 0
    if os.name == "nt":
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        # 2026-10-28：补 CREATE_NO_WINDOW，否则重启流水线时也会弹一个控制台窗口
        flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
    with open(LOG, "a", encoding="utf-8") as out:
        subprocess.Popen(cmd, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                         creationflags=flags)
    _log("已拉起")


def main():
    once = "--once" in sys.argv          # 计划任务模式：只检查一次就退出（避免重复常驻循环）
    _log(f"watchdog 启动（stale={STALE_SEC}s, interval={INTERVAL}s, once={once}）")
    while True:
        hb = read_hb()
        if not hb:
            _log("无心跳文件（首次运行？）→ 跳过本轮")
        else:
            age = time.time() - float(hb.get("epoch") or 0)
            alive = pid_alive(hb.get("pid")) or campaign_running()
            if age > STALE_SEC and not alive:
                _log(f"心跳已 {age:.0f}s 未更新且进程不在（pid={hb.get('pid')}, ds={hb.get('dataset')}）")
                restart(hb.get("argv") or [])
                time.sleep(60)          # 给新进程启动时间，避免连续重启
            elif age > STALE_SEC:
                _log(f"心跳 {age:.0f}s 未更新，但进程仍在（pid={hb.get('pid')}）→ 只有卡死才处理，本轮跳过")
        if once:
            return
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
