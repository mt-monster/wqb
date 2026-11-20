# -*- coding: utf-8 -*-
"""tests/unit/09_core/test_corr_slot_short_hold_20261117.py

「每 30 分钟一条 195s 伪冷却」事故（2026-11-17 实测）回归守卫。

事故形态
--------
``logs/_dblock/correlation.cooldown.json`` 每 30 min 出现一条 195s 冷却，写入 pid
每条都短命退出。定位结果：``WorkBuddy/Claw`` 面板的「自动终验」
（``panel_ui_js_cand.picksAutoVerify``，``PICKS_AUTO_THROTTLE_MS = 30min``）每半小时
挑一颗候选，POST ``/api/refresh-corr`` → ``wq_prod_backfill.py --alpha <id>``
（slot tag ``prod_backfill(<id>)``）。该类调用**只读平台已有值**：

    08:36:41  acquire(tag=prod_backfill(QP02jR9w))
    08:37:02  release(...) → 写 195s 冷却        # 持槽仅 **21s**

一次真实的 prod/self 计算平台侧要 180–200s，21s 拿到值只可能是既有值直读
⇒ 账号槽根本没被占用，195s 冷却纯属自伤（账号每 30 min 有 3.25 min 伪冷却，
``super_build.py submit`` 首跑正好撞上）。

本组用例守住三条不变量：
  1. 持槽 < ``min_hold_for_cooldown()`` 且未显式给 ``seconds`` ⇒ **不写冷却**；
  2. 持槽足够长（真算过）⇒ 照旧写 195s；
  3. 显式 ``seconds`` / ``cooldown=False`` 的调用点语义**不变**（调用方优先）。
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
    monkeypatch.delenv("WQB_CORR_MIN_HOLD_FOR_COOLDOWN", raising=False)
    monkeypatch.delenv("WQB_CORR_UNAVAILABLE_STREAK", raising=False)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _make_token(d: Path, held_s: float, tag: str = "prod_backfill(TESTID01)") -> Path:
    """造一个「本进程在 held_s 秒前拿到」的 token 文件。"""
    p = d / cs.LOCK_NAME
    p.write_text(json.dumps({
        "owner": "%d@test" % os.getpid(),
        "pid": os.getpid(),
        "tag": "corr:" + tag,
        "at": time.time() - held_s,
    }), encoding="utf-8")
    return p


def _audit_lines(d: Path):
    p = d / cs.COOLDOWN_AUDIT_NAME
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


class TestShortHoldSkipsCooldown:
    def test_21s_hold_writes_no_cooldown(self, lock_env):
        """事故现场复刻：持槽 21s 的既有值直读 ⇒ 不得留 195s 冷却。"""
        tok = _make_token(lock_env, held_s=21.0)
        cs.release(str(tok))
        assert cs.cooldown_remaining() == 0.0
        acts = [r["action"] for r in _audit_lines(lock_env)]
        assert acts == ["skip_short"]

    def test_audit_records_tag_and_hold(self, lock_env):
        tok = _make_token(lock_env, held_s=21.0)
        cs.release(str(tok))
        rec = _audit_lines(lock_env)[0]
        assert rec["tag"] == "corr:prod_backfill(TESTID01)"
        assert rec["held_s"] == pytest.approx(21.0, abs=1.0)
        assert rec["cooldown_s"] is None

    def test_zero_hold_via_slot_context(self, lock_env):
        """最极端情形：acquire 后立刻 release（缓存命中）⇒ 同样不留冷却。"""
        with cs.slot("prod_backfill(FAST01)") as s:
            assert s["acquired"] is True
        assert cs.cooldown_remaining() == 0.0

    def test_threshold_is_env_overridable(self, lock_env, monkeypatch):
        monkeypatch.setenv("WQB_CORR_MIN_HOLD_FOR_COOLDOWN", "10")
        tok = _make_token(lock_env, held_s=21.0)
        cs.release(str(tok))
        # 21s > 10s 阈值 ⇒ 按「算过」处理，照写冷却
        assert cs.cooldown_remaining() > 100


class TestLongHoldStillWritesCooldown:
    def test_200s_hold_writes_195s(self, lock_env):
        """真算过（≥180s）⇒ 冷却语义不变。"""
        tok = _make_token(lock_env, held_s=200.0)
        cs.release(str(tok))
        rem = cs.cooldown_remaining()
        assert 180 < rem <= cs.COOLDOWN_SEC_DEFAULT + 2
        assert [r["action"] for r in _audit_lines(lock_env)] == ["write"]

    def test_unreadable_token_falls_back_to_old_behaviour(self, lock_env):
        """token 读不出 ``at``（旧文件/半写）⇒ 保守照旧写冷却，绝不因新逻辑放行。"""
        p = lock_env / cs.LOCK_NAME
        p.write_text("not-json", encoding="utf-8")
        cs.release(str(p))
        assert cs.cooldown_remaining() > 100


class TestCallerDecisionWins:
    def test_explicit_seconds_honoured_on_short_hold(self, lock_env):
        """调用方显式给 seconds（如算成功后 5s 收尾）⇒ 不套用短持槽规则。"""
        tok = _make_token(lock_env, held_s=5.0)
        cs.release(str(tok), seconds=5.0)
        assert 0 < cs.cooldown_remaining() <= 6

    def test_cooldown_false_on_long_hold_writes_nothing(self, lock_env):
        tok = _make_token(lock_env, held_s=300.0)
        cs.release(str(tok), cooldown=False)
        assert cs.cooldown_remaining() == 0.0
        assert [r["action"] for r in _audit_lines(lock_env)] == ["skip_by_caller"]
