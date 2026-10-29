# -*- coding: utf-8 -*-
"""相关性槽的「按结果分流冷却」+「同 alpha 在飞标记」（2026-10-28 P0-1 / P0-2）。

背景（14h 日志实测，见 ``reports/prod_corr_timing_20261028.md``）：

- 旧 ``release()`` **无条件**写 195s 冷却 ⇒ 一次「一个 GET 就拿到既有值」也被罚
  3 分钟，吞吐被压到 ~4 alpha/小时。
- 更隐蔽的一条：``slot()`` 的 ``finally`` 无条件 ``release(info["token"])``，而拿不到槽时
  ``token is None`` ⇒ ``release(None)`` 仍会 ``write_cooldown(None)``。于是**每一次**
  busy 轮询都把冷却续期 195s —— 越查越堵，观察到的现象是「明明加了锁还是一直锁着」。

本文件钉住：
  1. 冷却可按结果写（秒数 / 不写 / 清除），``settle_seconds()`` 读环境变量；
  2. **抢槽失败不得改写冷却**（上面第二条的回归守卫）；
  3. inflight 侧车：mark/get/n 累加/TTL 过期/清除，且与写库锁 token 文件分开。
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
from wqb.config import WAIT_THRESHOLDS as W  # noqa: E402


@pytest.fixture()
def lock_env(tmp_path, monkeypatch):
    """锁目录 / 冷却 / 在飞标记全部指到 tmp（不碰仓库 logs/_dblock）。"""
    d = tmp_path / "_dblock"
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    monkeypatch.delenv("WQB_CORR_COOLDOWN_SEC", raising=False)
    monkeypatch.delenv("WQB_CORR_SETTLE_SEC", raising=False)
    monkeypatch.delenv("WQB_CORR_INFLIGHT_TTL_SEC", raising=False)
    return d


def _spoof_other_process(token_path) -> None:
    """把 token 的 pid 改成父进程（测试期间必然存活）⇒ 模拟「别的进程持锁」。"""
    p = Path(token_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    data["pid"] = os.getppid()
    p.write_text(json.dumps(data), encoding="utf-8")


# --------------------------------------------------------------- 冷却按结果写
class TestOutcomeCooldown:
    def test_write_cooldown_seconds_is_respected(self, lock_env):
        cs.write_cooldown(3)
        rem = cs.cooldown_remaining()
        assert 0 < rem <= 3.05

    def test_write_cooldown_zero_clears(self, lock_env):
        cs.write_cooldown(30)
        cs.write_cooldown(0)
        assert cs.cooldown_remaining() == 0.0

    def test_write_cooldown_default_is_cooldown_sec(self, lock_env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_COOLDOWN_SEC", "7")
        cs.write_cooldown(None)
        assert 0 < cs.cooldown_remaining() <= 7.05

    def test_settle_seconds_reads_env(self, lock_env, monkeypatch):
        assert cs.settle_seconds() == pytest.approx(cs.COOLDOWN_SETTLE_SEC)
        monkeypatch.setenv("WQB_CORR_SETTLE_SEC", "2.5")
        assert cs.settle_seconds() == pytest.approx(2.5)
        monkeypatch.setenv("WQB_CORR_SETTLE_SEC", "not-a-number")
        assert cs.settle_seconds() == pytest.approx(cs.COOLDOWN_SETTLE_SEC)

    def test_release_without_cooldown_writes_nothing(self, lock_env):
        info = cs.acquire("t1", ttl_sec=60)
        cs.release(info["token"], cooldown=False)
        assert cs.cooldown_remaining() == 0.0

    def test_release_with_explicit_seconds(self, lock_env):
        info = cs.acquire("t1", ttl_sec=60)
        cs.release(info["token"], cooldown=True, seconds=9)
        assert 0 < cs.cooldown_remaining() <= 9.05

    def test_acquire_reports_cooldown_with_retry_after(self, lock_env):
        cs.write_cooldown(4)
        info = cs.acquire("t1", ttl_sec=60)
        assert info["acquired"] is False and info["busy"] is True
        assert info.get("cooldown") is True
        assert 0 < float(info["retry_after"]) <= 4.05


class TestFailedAcquireMustNotTouchCooldown:
    """★ 回归守卫：抢不到槽时不得改写冷却（旧 ``slot()`` 的 ``release(None)`` 坑）。"""

    def test_failed_acquire_by_cooldown_does_not_extend_it(self, lock_env):
        cs.write_cooldown(5)
        with cs.slot("ctx", ttl_sec=60) as s:
            assert s["acquired"] is False
        rem = cs.cooldown_remaining()
        # 旧实现走 release(None) → write_cooldown(None) → 195s
        assert 0 < rem <= 5.05, f"冷却被失败路径续期到 {rem}s（旧 bug 回来过）"

    def test_failed_acquire_by_other_holder_writes_no_cooldown(self, lock_env):
        holder = cs.acquire("holder", ttl_sec=120)
        _spoof_other_process(holder["token"])
        try:
            with cs.slot("ctx", ttl_sec=60) as s:
                assert s["acquired"] is False and s["busy"] is True
            assert cs.cooldown_remaining() == 0.0
        finally:
            cs.release(holder["token"])

    def test_failed_acquire_does_not_swallow_exception(self, lock_env):
        """finally 里不能 `return`（会吞异常）——用崩溃路径反查。"""
        cs.write_cooldown(5)
        with pytest.raises(RuntimeError):
            with cs.slot("ctx", ttl_sec=60) as s:
                assert not s["acquired"]
                raise RuntimeError("boom")
        assert 0 < cs.cooldown_remaining() <= 5.05

    def test_successful_slot_still_writes_default_cooldown(self, lock_env):
        """拿到槽的路径行为不变：缺省仍写 WQB_CORR_COOLDOWN_SEC（195s）。"""
        with cs.slot("ctx", ttl_sec=60) as s:
            assert s["acquired"] is True
            s["cooldown_seconds"] = 6  # 调用方按结果覆写
        assert 0 < cs.cooldown_remaining() <= 6.05


# --------------------------------------------------------------- TTL 常量一致性
class TestTtlConsistency:
    def test_default_ttl_covers_max_single_hold(self):
        """TTL 的硬要求是「> 单次最长持锁」，不是「≥ 5× 窗口」（2026-10-28 改口径）。

        最长持锁 ≈ 窗口 + 一个慢轮询台阶（30 s）+ 抖动。旧的「≥ 5×」是窗口 120 时
        凑出 600 的经验式：窗口调到 240 后照它办得把 TTL 抬到 1200（进程崩溃残留
        20 分钟），代价大于收益。600 对 240 仍有 2.2× / 330 s 绝对余量。
        """
        assert cs.DEFAULT_TTL_SEC >= W["prod_corr_timeout_s"] + 120

    def test_settle_is_much_shorter_than_full_cooldown(self):
        assert cs.COOLDOWN_SETTLE_SEC < cs.COOLDOWN_SEC_DEFAULT / 10

    def test_mcp_lock_ttl_default_matches_slot_ttl(self):
        """MCP 侧的 env 缺省必须与 correlation_slot 的 DEFAULT_TTL_SEC 同值。"""
        src = (REPO / "world-quant-brain-mcp" / "brain_mixin_transport.py").read_text(
            encoding="utf-8")
        assert 'BRAIN_CORRELATION_LOCK_TTL_SECONDS", "600"' in src
        assert cs.DEFAULT_TTL_SEC == 600.0


# --------------------------------------------------------------- inflight 侧车
class TestInflightSidecar:
    def test_mark_get_clear_roundtrip(self, lock_env):
        assert cs.inflight_get("A1") == {}
        rec = cs.inflight_mark("A1", base_max=0.42)
        assert rec["n"] == 1 and rec["base_max"] == 0.42
        got = cs.inflight_get("A1")
        assert got and got["n"] == 1
        assert cs.inflight_clear("A1") is True
        assert cs.inflight_get("A1") == {}
        assert cs.inflight_clear("A1") is False

    def test_remark_increments_n_and_keeps_started_at(self, lock_env):
        first = cs.inflight_mark("A1")
        second = cs.inflight_mark("A1")
        assert second["n"] == 2
        assert second["started_at"] == first["started_at"]
        assert second["base_max"] == first["base_max"]

    def test_ttl_expiry_prunes_entry(self, lock_env):
        cs.inflight_mark("A1", ttl_sec=0.05)
        assert cs.inflight_get("A1")
        time.sleep(0.12)
        assert cs.inflight_get("A1") == {}
        assert cs.inflight_all() == {}

    def test_ttl_env_override(self, lock_env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_INFLIGHT_TTL_SEC", "1")
        rec = cs.inflight_mark("A1")
        assert rec["expires_at"] - time.time() <= 1.05

    def test_two_alphas_are_independent(self, lock_env):
        cs.inflight_mark("A1")
        cs.inflight_mark("A2")
        assert set(cs.inflight_all()) == {"A1", "A2"}
        cs.inflight_clear("A1")
        assert set(cs.inflight_all()) == {"A2"}

    def test_sidecar_file_is_separate_from_lock_token(self, lock_env):
        assert cs.INFLIGHT_NAME != cs.LOCK_NAME
        assert cs.INFLIGHT_NAME != cs.COOLDOWN_NAME
        cs.inflight_mark("A1")
        assert Path(cs.inflight_path()).is_file()


class TestHolderTag:
    def test_holder_tag_matches_op_name(self, lock_env):
        info = cs.acquire("get_production_correlation(ABC)", ttl_sec=60)
        try:
            assert cs.holder_tag() == "corr:get_production_correlation(ABC)"
        finally:
            cs.release(info["token"])
        assert cs.holder_tag() is None

    def test_holder_tag_none_when_absent(self, lock_env):
        assert cs.holder_tag() is None
