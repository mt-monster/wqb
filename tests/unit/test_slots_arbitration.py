# -*- coding: utf-8 -*-
"""2026-09-19 账户级槽位仲裁（_lib/slots.py）：跨进程 token 文件、cap、陈旧回收、降级。"""
import importlib
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
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
