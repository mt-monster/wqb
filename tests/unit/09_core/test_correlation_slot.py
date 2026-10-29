# -*- coding: utf-8 -*-
"""tests/unit/09_core/test_correlation_slot.py — 平台 prod「账号级单并发槽」的跨进程互斥。

背景（实测 bug，2026-10-22）：平台 ``GET /alphas/{id}/correlations/prod`` 是
**每账号仅 1 个在飞**的接口；本仓的相关性查询散落在**多个进程**（MCP 常驻服务 +
若干 CLI 工具 + 一次性脚本），它们各自新建 ``BrainApiClient`` ⇒ 进程内 asyncio 锁
互不相识 ⇒ 一方卡住即可把另一方堵到轮询上限（实测空转 800s+ / 1499s 才出数）。

本组用例守住修复的两条不变量：
  1. **跨进程真互斥**：槽被他人持有时**立即返回 busy**，不排队、不降级放行。
  2. **写库锁与相关性锁互不干扰**：两种锁 TTL 不同，共用一个目录 ⇒ 短 TTL 的写锁
     不得回收长 TTL 的相关性锁 token（否则两个进程同时自认持有）。

另附回归守卫：`prod_corr_timeout_s` 不得回涨到 3600（占槽一小时）。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb import correlation_slot as cs  # noqa: E402
from wqb import db_write_lock as dwl  # noqa: E402
from wqb.config import WAIT_THRESHOLDS as W  # noqa: E402


@pytest.fixture()
def lock_env(tmp_path, monkeypatch):
    """把锁目录指到 tmp（不碰仓库里的 logs/_dblock）。"""
    d = tmp_path / "_dblock"
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    return d


class TestCorrelationSlotBasics:
    def test_acquire_then_release(self, lock_env):
        info = cs.acquire("t1", ttl_sec=600)
        assert info["acquired"] and not info["busy"]
        assert info["token"] and Path(info["token"]).is_file()
        cs.release(info["token"])
        assert not Path(info["token"]).exists()

    def test_second_holder_is_busy_not_degraded(self, lock_env):
        """**核心不变量**：**别的进程**持锁 ⇒ 立即 busy（不放行、不排队）。

        放行等于让第二个进程也去打这个单并发接口 —— 正是事故形态。

        「别的进程」用**父进程 pid** 伪造（测试运行期间必然存活 ⇒ 不会被
        ``_reclaim_dead_holder`` 判死回收）；若拿一个大数当 pid，会被当死持有者
        **立即回收**（那是另一条路径，与本用例意图相反）。
        """
        import json
        i1 = cs.acquire("holder", ttl_sec=600)
        assert i1["acquired"]
        tok = Path(i1["token"])
        data = json.loads(tok.read_text(encoding="utf-8"))
        data["pid"] = os.getppid()
        tok.write_text(json.dumps(data), encoding="utf-8")

        i2 = cs.acquire("other", ttl_sec=600)
        assert i2["busy"] is True
        assert i2["acquired"] is False
        assert i2["token"] is None      # 没拿到 token ⇒ 绝不能去 release 别人的
        cs.release(i1["token"])

    def test_same_pid_is_reentrant_renewal(self, lock_env):
        """同 pid 再 acquire = **续约**（与 ``db_write_lock`` 同语义）。

        故本模块**不能**承担进程内互斥——同进程的两个协程会各自"续约"同一 token。
        进程内互斥由 MCP 侧的 asyncio.Lock 承担（**先**进程内锁、**后**跨进程锁，
        顺序不可换）；本模块只管跨进程。
        """
        i1 = cs.acquire("t1", ttl_sec=600)
        i2 = cs.acquire("t1", ttl_sec=600)
        assert i2["acquired"] and not i2["busy"]
        assert i2["token"] == i1["token"]
        cs.release(i1["token"])

    def test_release_is_idempotent(self, lock_env):
        info = cs.acquire("t1", ttl_sec=600)
        cs.release(info["token"])
        cs.release(info["token"])       # 幂等，不抛
        assert not Path(info["token"]).exists()

    def test_release_does_not_remove_other_holder_token(self, lock_env):
        """owner 保护：自己的 release 不得删掉他人的 token。"""
        i1 = cs.acquire("holder", ttl_sec=600)
        tok = Path(i1["token"])
        # 伪装成他人持有（父进程 pid 在测试期间必然存活）
        import json
        data = json.loads(tok.read_text(encoding="utf-8"))
        data["pid"] = os.getppid()
        tok.write_text(json.dumps(data), encoding="utf-8")
        cs.release(str(tok))
        assert tok.is_file()

    def test_slot_context_manager_yields_info_and_releases(self, lock_env):
        with cs.slot("ctx", ttl_sec=600) as s:
            assert s["acquired"]
            tok = s["token"]
            assert Path(tok).is_file()
        assert not Path(tok).exists()

    def test_slot_context_manager_releases_on_exception(self, lock_env):
        import pytest
        with pytest.raises(RuntimeError):
            with cs.slot("ctx", ttl_sec=600) as s:
                tok = s["token"]
                raise RuntimeError("boom")
        assert not Path(tok).exists()

    def test_lock_file_name_is_separate_from_db_write_lock(self, lock_env):
        """两种锁必须用**不同** token 文件（TTL 不同，共用会互相回收）。"""
        assert cs.LOCK_NAME == "correlation.lock.json"
        assert cs.LOCK_NAME != "dbwrite.lock.json"
        assert cs.slot_path().endswith(cs.LOCK_NAME)


class TestLockIsolation:
    def test_db_write_lock_does_not_reclaim_correlation_token(self, lock_env):
        """短 TTL 的写锁不得回收长 TTL 的相关性锁 token。

        反例（修复前）：``_prune_expired`` 扫目录里全部 ``*.json`` ⇒ 写锁（TTL 900s）
        会把仍在持有的相关性锁 token 当过期回收 ⇒ 两个进程同时自认持有。
        """
        corr = cs.acquire("corr", ttl_sec=3600)
        assert corr["acquired"]
        tok = Path(corr["token"])
        # 把相关性 token 的 mtime 调到「比写锁 TTL 更老」
        stale = os.path.getmtime(tok) - 5000
        os.utime(tok, (stale, stale))
        # 写锁来抢（同目录）—— 不得动相关性 token
        db = dwl.acquire(tag="db", ttl_sec=900, wait_timeout=0.5)
        assert db["ok"]
        assert tok.is_file(), "写锁把仍在持有的相关性锁 token 回收了（跨锁串扰）"
        dwl.release(db.get("token"))
        cs.release(corr["token"])

    def test_correlation_lock_does_not_reclaim_db_write_token(self, lock_env):
        """反向同理：相关性锁不得动写库锁的 token。"""
        db = dwl.acquire(tag="db", ttl_sec=900, wait_timeout=0.5)
        assert db["ok"]
        tok = Path(db["token"])
        stale = os.path.getmtime(tok) - 5000
        os.utime(tok, (stale, stale))
        corr = cs.acquire("corr", ttl_sec=3600)
        assert corr["acquired"]
        assert tok.is_file(), "相关性锁回收了写库锁 token（跨锁串扰）"
        cs.release(corr["token"])
        dwl.release(db.get("token"))


class TestTimeoutGuard:
    def test_prod_corr_timeout_does_not_exceed_15_minutes(self):
        """**回归守卫**：轮询窗口不得回涨到 3600（占槽一小时 → 堵死整账号）。

        2026-10-28：窗口 120 → 240 —— 一次正常计算 180–200 s，120 会让每条真实查询
        都收在 pending。900 上界保留：别以"多给点余量"的名义回到 15 分钟堵死整账号。
        """
        assert W["prod_corr_timeout_s"] <= 900

    def test_mcp_poll_window_matches_config(self):
        """MCP 客户端的轮询窗口必须与 ``WAIT_THRESHOLDS`` 同源（守护测试既有约定）。"""
        import re
        src = (REPO / "world-quant-brain-mcp" / "brain_mixin_spcread.py").read_text(
            encoding="utf-8")
        assert int(re.search(r"_PROD_CORR_WAIT_S\s*=\s*(\d+)", src).group(1)) == \
            W["prod_corr_timeout_s"]


class TestProdCorrResponseShapeGuard:
    """**回归守卫**：平台 ``/correlations/prod`` 偶发返回 **数组** 形态。

    历史 bug（2026-10-22 实测）：解析端直接 ``corr_data.get('max')``，
    而 ``except`` 只捕获 ``json.JSONDecodeError`` ⇒ 遇到 list 时抛
    ``AttributeError: 'list' object has no attribute 'get'`` 逃逸到调用方，
    被记成 ``status=error:AttributeError``（与网络抖动混为一谈）。

    本组用例守住两件事：
      1. 调用 ``.get()`` 前必须有 ``isinstance(..., dict)`` 类型守卫；
      2. ``except`` 分支必须兜住 ``AttributeError``，任何非预期响应形态
         都不得让整条 prod 查询崩掉。
    """

    SRC = REPO / "world-quant-brain-mcp" / "brain_mixin_spcread.py"

    def test_type_guard_before_get(self):
        src = self.SRC.read_text(encoding="utf-8")
        # 归一化 list→dict 的守卫，且 .get 前有 isinstance 保护
        assert "isinstance(corr_data, list)" in src
        assert "isinstance(corr_data, dict) and corr_data.get('max')" in src

    def test_attribute_error_is_caught(self):
        src = self.SRC.read_text(encoding="utf-8")
        assert "except AttributeError" in src
