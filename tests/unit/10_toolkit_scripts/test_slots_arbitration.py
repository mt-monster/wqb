# -*- coding: utf-8 -*-
"""2026-09-19 账户级槽位仲裁（_lib/slots.py）：跨进程 token 文件、cap、陈旧回收、降级。"""
import importlib
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _slots(monkeypatch, tmp_path, cap="2"):
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    monkeypatch.setenv("WQB_SLOTS_DIR", str(tmp_path / "slots"))
    monkeypatch.setenv("WQB_GLOBAL_SLOTS", cap)
    sys.modules.pop("_lib.slots", None)
    return importlib.import_module("_lib.slots")


def test_acquire_release_respects_cap(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap="2")
    t1 = sl.acquire("a", log=lambda *_: None)
    t2 = sl.acquire("b", log=lambda *_: None)
    assert t1 and t2 and len(sl.live_tokens()) == 2
    # 第三个拿不到：等待超时后降级返回 None（不阻断）
    t3 = sl.acquire("c", wait_sec=0, poll_sec=0.01, log=lambda *_: None)
    assert t3 is None
    sl.release(t1)
    assert len(sl.live_tokens()) == 1
    t4 = sl.acquire("d", wait_sec=0, poll_sec=0.01, log=lambda *_: None)
    assert t4 is not None
    sl.relabel(t4, "MSID123")
    assert any(x["label"] == "MSID123" for x in sl.status())


def test_cap_zero_disables(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap="0")
    assert sl.acquire("x", log=lambda *_: None) is None
    sl.release(None)   # 幂等


def test_stale_tokens_are_reclaimed(monkeypatch, tmp_path):
    sl = _slots(monkeypatch, tmp_path, cap="1")
    d = tmp_path / "slots"
    d.mkdir()
    # 进程已死（pid 999999 基本不存在）
    (d / "dead.slot").write_text(f"999999|old|{time.time()}", encoding="utf-8")
    # 超龄（7 小时前）
    (d / "aged.slot").write_text(f"{os.getpid()}|aged|{time.time() - 7 * 3600}", encoding="utf-8")
    assert sl.live_tokens() == []
    assert sl.acquire("fresh", wait_sec=0, poll_sec=0.01, log=lambda *_: None) is not None


def test_nonblock_returns_none_without_waiting(monkeypatch, tmp_path):
    """2026-10-02 死锁修复：在飞满时 nonblock=True 立即返回 None，绝不阻塞。

    这是 pipeline._refill 主线程补批路径的关键——若此处阻塞，会与同进程
    尚未轮询的 future 构成自锁（见 slots.py 模块 docstring「死锁」段）。
    """
    sl = _slots(monkeypatch, tmp_path, cap="2")
    t1 = sl.acquire("a", nonblock=True, log=lambda *_: None)
    t2 = sl.acquire("b", nonblock=True, log=lambda *_: None)
    assert t1 and t2
    t0 = time.time()
    t3 = sl.acquire("c", nonblock=True, log=lambda *_: None)
    elapsed = time.time() - t0
    assert t3 is None
    assert elapsed < 0.5, f"nonblock 不应等待，实测 {elapsed:.3f}s"
    # 释放一个后 nonblock 立刻能拿到
    sl.release(t1)
    assert sl.acquire("d", nonblock=True, log=lambda *_: None) is not None
    sl.release(t2)


def test_blocking_mode_still_waits_and_times_out(monkeypatch, tmp_path):
    """回归保护：默认（阻塞）语义不变——短暂等待后超时降级返回 None。"""
    sl = _slots(monkeypatch, tmp_path, cap="1")
    t1 = sl.acquire("a", log=lambda *_: None)
    assert t1
    t2 = sl.acquire("b", wait_sec=1, poll_sec=0.2, log=lambda *_: None)
    assert t2 is None
    sl.release(t1)
