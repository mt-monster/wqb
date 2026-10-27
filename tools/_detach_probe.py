# -*- coding: utf-8 -*-
"""脱离 Job object 的存活探针：每 5 秒写一行心跳，共 120 秒。"""
import os
import sys
import time

LOG = os.path.join(ROOT, "logs", "_detach_probe.log")


def main():
    pid = os.getpid()
    ppid = os.getppid()
    for i in range(24):
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write("%s pid=%d ppid=%d tick=%d\n"
                     % (time.strftime("%H:%M:%S"), pid, ppid, i))
        time.sleep(5)


if __name__ == "__main__":
    main()
