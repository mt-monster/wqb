# -*- coding: utf-8 -*-
"""tests/unit/09_core/test_corr_slot_stale_cooldown_20261117.py

残留锁事故（2026-11-17 实测）回归守卫。

事故形态
--------
`tools/super_build.py submit` 首跑 **attempts=0** 直接 fail-closed 退出，日志只说
「账号级相关性槽被其它进程占用」，实际原因是 ``logs/_dblock/correlation.cooldown.json``
里一条 **195s 冷却**（写入进程 pid 已死）——平台占槽时长本来是**已知的**，却被当成
未知持有者一律放弃；人工等 TTL 到期后重跑即成功。

本组用例守住两条新不变量：
  1. **脏冷却不得锁死账号**：半写/非 JSON、以及 ``until`` 远超可信上限（时钟跳变或
     被手改的远期值）⇒ 退役为 ``.stale`` 并返回 0；
     ``clear_cooldown`` 走改名退役（``os.replace``）而非 ``unlink``。
  2. **busy 必须分因**：``acquire`` 的 ``reason`` 区分 ``cooldown``（已知时长，可等）
     / ``token_busy``（存活持有者，fail-fast）/ ``platform_unavailable``（熔断）。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb import correlation_slot as cs  # noqa: E402


@pytest.fixture()
def lock_env(tmp_path, monkeypatch):
    d = tmp_path / "_dblock"
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    monkeypatch.delenv("WQB_CORR_COOLDOWN_SEC", raising=False)
    monkeypatch.delenv("WQB_CORR_UNAVAILABLE_STREAK", raising=False)
    monkeypatch.delenv("WQB_CORR_UNAVAILABLE_SEC", raising=False)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_raw(d: Path, payload) -> Path:
    p = d / cs.COOLDOWN_NAME
    p.write_text(payload if isinstance(payload, str) else json.dumps(payload),
                 encoding="utf-8")
    return p


class TestStaleCooldownSelfHeal:
    def test_corrupt_json_is_retired_not_blocking(self, lock_env):
        """半写/截断的 JSON ⇒ 不得当成 195s 冷却，退役后立即放行。"""
        p = _write_raw(lock_env, '{"until": 1794876017.9, "sec": 19')  # 截断
        assert cs.cooldown_remaining() == 0.0
        assert not p.exists()
        assert (lock_env / (cs.COOLDOWN_NAME + ".stale")).exists()

    def test_non_object_json_is_retired(self, lock_env):
        p = _write_raw(lock_env, "[1, 2, 3]")
        assert cs.cooldown_remaining() == 0.0
        assert not p.exists()

    def test_absurd_future_until_is_treated_as_stale(self, lock_env):
        """``until`` = now + 10h（时钟跳变 / 手改）⇒ 退役，不锁账号 10 小时。"""
        p = _write_raw(lock_env, {"until": time.time() + 36000, "sec": 36000,
                                   "pid": 999999, "at": "2026-11-17 00:00:00"})
        assert cs._cooldown_sane_max() < 36000
        assert cs.cooldown_remaining() == 0.0
        assert not p.exists()

    def test_normal_cooldown_still_blocks(self, lock_env):
        """正常 195s 冷却**必须照旧阻塞**——脏值自愈不得放宽真实占槽。"""
        cs.write_cooldown(30)
        assert 0 < cs.cooldown_remaining() <= 30.05
        info = cs.acquire("t")
        assert info["acquired"] is False and info["busy"] is True
        assert info["reason"] == "cooldown"
        assert 0 < info["retry_after"] <= 30.05

    def test_clear_cooldown_renames_instead_of_unlinking(self, lock_env):
        cs.write_cooldown(60)
        p = lock_env / cs.COOLDOWN_NAME
        cs.clear_cooldown()
        assert not p.exists()
        stale = lock_env / (cs.COOLDOWN_NAME + ".stale")
        assert stale.exists()                      # 可追溯：谁写过这条冷却
        assert json.loads(stale.read_text(encoding="utf-8"))["sec"] == 60.0
        assert cs.cooldown_remaining() == 0.0


class TestAcquireReasonCodes:
    def test_ok_reason(self, lock_env):
        info = cs.acquire("t")
        assert info["acquired"] and info["reason"] == "ok"
        cs.release(info["token"], cooldown=False)

    def test_token_busy_reports_live_holder(self, lock_env):
        """存活持有者 ⇒ ``token_busy`` + holder 快照（不许当 cooldown 等）。"""
        i1 = cs.acquire("holder")
        tok = Path(i1["token"])
        data = json.loads(tok.read_text(encoding="utf-8"))
        data["pid"] = os.getppid()                 # 父进程：测试期间必然存活
        tok.write_text(json.dumps(data), encoding="utf-8")

        i2 = cs.acquire("other")
        assert i2["acquired"] is False and i2["busy"] is True
        assert i2["reason"] == "token_busy"
        assert i2["holder"]["pid"] == os.getppid()
        assert i2["holder"]["alive"] is True
        cs.release(i1["token"], cooldown=False)

    def test_platform_unavailable_reason(self, lock_env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_UNAVAILABLE_STREAK", "1")
        cs.note_pending_streak("ABC123")
        info = cs.acquire("t")
        assert info["acquired"] is False
        assert info["reason"] == "platform_unavailable"
        cs.clear_unavailable()
