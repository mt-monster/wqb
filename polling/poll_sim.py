#!/usr/bin/env python3
"""poll_sim.py - 跨平台仿真轮询器（替代 6 个 sim_*_poll.sh 包装脚本）。

优化建议③：把版本化的 .sh 轮询脚本收敛为 1 个参数化工具。
用法:
    python polling/poll_sim.py --csv <status.csv> --pid <SIM_PID> --total <N> [--log <out.log>] [--name v4]
    # 也可用环境变量覆盖：POLL_CSV / POLL_PID / POLL_TOTAL / POLL_LOG
默认 --log 写入仓库根 logs/<name>_poll.log。
"""
import os, time, argparse, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_LOG = os.path.join(ROOT, "logs", "poll.log")


def alive(pid):
    if not pid:
        return False
    # Windows: tasklist; 其他: kill -0
    if os.name == "nt":
        out = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}"],
            capture_output=True, text=True,
        ).stdout
        return str(pid) in out
    try:
        os.kill(int(pid), 0)
        return True
    except OSError:
        return False


def complete_count(csv):
    if not csv or not os.path.exists(csv):
        return 0
    n = 0
    with open(csv, encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
    for line in lines[1:]:
        if "COMPLETE" in line:
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.environ.get("POLL_CSV", ""))
    ap.add_argument("--pid", default=os.environ.get("POLL_PID", ""))
    ap.add_argument("--total", type=int, default=int(os.environ.get("POLL_TOTAL", "0")))
    ap.add_argument("--name", default=os.environ.get("POLL_NAME", "poll"))
    ap.add_argument("--log", default=os.environ.get("POLL_LOG", ""))
    ap.add_argument("--timeout", type=int, default=120, help="最大轮询次数")
    a = ap.parse_args()

    log = a.log or os.path.join(ROOT, "logs", f"{a.name}_poll.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    pid = a.pid.strip() if a.pid else ""

    with open(log, "w", encoding="utf-8") as L:
        L.write(f"{a.name} poll start {time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"target={a.total} pid={pid}\n")
        for i in range(1, a.timeout + 1):
            done = complete_count(a.csv)
            is_alive = alive(pid)
            msg = f"{time.strftime('%H:%M:%S')} complete={done}/{a.total} sim_exited={not is_alive}"
            print(msg)
            L.write(msg + "\n")
            if a.total and done >= a.total:
                L.write("ALL_DONE\n")
                break
            if pid and not is_alive:
                L.write(f"SIM_EXITED_PARTIAL done={done}\n")
                break
            time.sleep(60)
        L.write(f"=== FINAL CSV ===\n")
        if a.csv and os.path.exists(a.csv):
            L.write(open(a.csv, encoding="utf-8", errors="ignore").read())
        L.write(f"{a.name} poll end {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"[poll_sim] 日志已写入 {log}")


if __name__ == "__main__":
    main()
