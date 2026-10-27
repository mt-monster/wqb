# -*- coding: utf-8 -*-
"""tests/unit/09_core/test_corr_slot_cross_process.py — 跨进程槽互斥的端到端验证。

**真·跨进程**：起一个子进程持锁，主进程尝试 acquire ⇒ 必须拿到 busy。
（单进程内测不出这个性质 —— 同 pid 是「续约」，见 ``test_correlation_slot.py``。）
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb import correlation_slot as cs  # noqa: E402

# 子进程脚本：拿住槽并等父进程来抢
# argv: [0]=脚本 [1]=src 目录 [2]=占位 [3]=睡眠秒数
HOLDER = r'''
import os, sys, time
sys.path.insert(0, sys.argv[1])
from wqb import correlation_slot as cs
info = cs.acquire("holder", ttl_sec=120)
assert info["acquired"], info
print("HELD", flush=True)
time.sleep(float(sys.argv[3]))
'''


def test_other_process_holding_slot_yields_busy(tmp_path, monkeypatch):
    d = tmp_path / "_dblock"
    script = tmp_path / "holder.py"
    script.write_text(HOLDER, encoding="utf-8")

    # ⚠ **父进程也必须**指向同一个锁目录（否则父子用不同 token 文件，测了个寂寞）
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)

    env = dict(os.environ)
    env["WQB_DBLOCK_DIR"] = str(d)
    env["PYTHONPATH"] = str(SRC)
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.Popen(
        [sys.executable, str(script), str(SRC), "x", "20"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True,
        encoding="utf-8",
    )
    try:
        # 等子进程真的拿到锁
        line = proc.stdout.readline()
        assert "HELD" in line, f"holder failed: {line!r} {proc.stderr.read()!r}"
        time.sleep(0.2)

        info = cs.acquire("main", ttl_sec=120)
        assert info["busy"] is True, (
            "另一个进程持锁时本地 acquire 必须返回 busy（跨进程互斥失效）")
        assert info["acquired"] is False
        assert info["token"] is None
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:  # pragma: no cover
            proc.kill()


def test_slot_frees_after_holder_exits(tmp_path, monkeypatch):
    """持锁进程退出后（token 退役），槽必须能被重新拿到 —— 不留死锁。"""
    d = tmp_path / "_dblock"
    script = tmp_path / "holder.py"
    script.write_text(HOLDER, encoding="utf-8")

    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)

    env = dict(os.environ)
    env["WQB_DBLOCK_DIR"] = str(d)
    env["PYTHONPATH"] = str(SRC)
    env["PYTHONIOENCODING"] = "utf-8"

    proc = subprocess.Popen(
        [sys.executable, str(script), str(SRC), "x", "0.2"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True,
        encoding="utf-8",
    )
    line = proc.stdout.readline()
    assert "HELD" in line
    proc.wait(timeout=15)

    # 持锁者已退出 ⇒ 死持有者回收（按 pid 判活）⇒ 本进程可拿到
    info = cs.acquire("main", ttl_sec=120)
    assert info["acquired"] is True, "持锁进程退出后槽应可重新获取（留了死锁）"
    cs.release(info["token"])
