# -*- coding: utf-8 -*-
"""回归：wqb.db 写锁对「持有者进程已死」的 token 立即回收（2026-09-20）。

事故：GLB 三条 pipeline 被一个已退出的 build_wave 持有者（pid 18224）拖住，
每个写者各等满 wait_timeout（90-120s）才降级放行；TTL 900s 内 detached 任务
stdout 长期为空，被误判为僵死并被人工 kill 重发。两份同构实现
（src/wqb/db_write_lock.py 与 toolkit _lib/dblock.py）都要守住。
"""
from __future__ import annotations

import json
import os
import sys
import time

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts"))

from wqb import db_write_lock as canon  # noqa: E402
from _lib import dblock as toolkit  # noqa: E402


@pytest.mark.parametrize("mod", [canon, toolkit], ids=["src", "toolkit"])
def test_dead_holder_token_is_reclaimed_immediately(mod, tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(tmp_path))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    tok = tmp_path / "dbwrite.lock.json"
    # 造一个"死持有者"：pid 取一个几乎不可能存活的大值
    dead_pid = 2_000_000_000
    tok.write_text(json.dumps({"owner": "x", "pid": dead_pid, "tag": "dbwrite_build_wave",
                               "at": time.time()}), encoding="utf-8")
    t0 = time.time()
    info = mod.acquire(tag="ut", ttl_sec=900, wait_timeout=20)
    elapsed = time.time() - t0
    assert info["degraded"] is False
    assert info["token"] and os.path.isfile(info["token"])
    assert elapsed < 5, f"死持有者应立即回收，实测等了 {elapsed:.1f}s"
    cur = json.loads(tok.read_text(encoding="utf-8"))
    assert cur["pid"] == os.getpid()
    mod.release(info["token"])
    assert not tok.exists()


@pytest.mark.parametrize("mod", [canon, toolkit], ids=["src", "toolkit"])
def test_live_holder_is_respected(mod, tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(tmp_path))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    tok = tmp_path / "dbwrite.lock.json"
    # 用本进程 pid 之外的一个确定存活的进程：父进程
    live_pid = os.getppid()
    tok.write_text(json.dumps({"owner": "y", "pid": live_pid, "tag": "other", "at": time.time()}),
                   encoding="utf-8")
    t0 = time.time()
    info = mod.acquire(tag="ut", ttl_sec=900, wait_timeout=3)
    assert info["degraded"] is True  # 活持有者：等到超时后降级，不抢
    assert time.time() - t0 >= 2.5
    assert json.loads(tok.read_text(encoding="utf-8"))["pid"] == live_pid


def test_pid_alive_helpers():
    assert canon._pid_alive(os.getpid()) is True
    assert toolkit._pid_alive(os.getpid()) is True
    assert canon._pid_alive(2_000_000_000) is False
    assert toolkit._pid_alive(2_000_000_000) is False
