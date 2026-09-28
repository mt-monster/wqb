# -*- coding: utf-8 -*-
"""tests/unit/test_db_write_guards.py — 并发写锁治理守卫（2026-09-20 L1/L3）。

四类守卫（reports/db_concurrent_write_lock_audit_20260920.md 方案验收）：
  1. 连接工厂 PRAGMA 规范（WAL / busy_timeout=60s / foreign_keys=ON）
  2. DB 写锁 mutex 行为（互斥 / 重入续约 / TTL 自愈 / 释放幂等 / owner 保护）
  3. **静态禁裸 connect**（活跃目录白名单外禁止 sqlite3.connect——防回归主闸）
  4. 锁探针（db_lock_audit.probe_once 对临时库正常出报告）
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb import db_conn  # noqa: E402
from wqb import db_write_lock as dwl  # noqa: E402


# ---------------- 1. 连接工厂 ----------------

class TestConnFactory:
    def test_pragmas_applied(self, tmp_path):
        db = tmp_path / "wqb.db"
        conn = db_conn.connect(str(db))
        try:
            assert conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
            assert conn.execute("PRAGMA busy_timeout").fetchone()[0] == 60000
            assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        finally:
            conn.close()

    def test_default_timeout_is_60s(self, tmp_path):
        db = tmp_path / "wqb.db"
        conn = db_conn.connect(str(db))
        try:
            # 连接层 timeout 也应默认 60s（sqlite3.connect 的 timeout 参数）
            assert conn.execute("PRAGMA busy_timeout").fetchone()[0] == int(60 * 1000)
        finally:
            conn.close()

    def test_row_factory_passthrough(self, tmp_path):
        db = tmp_path / "wqb.db"
        conn = db_conn.connect(str(db), row_factory=sqlite3.Row)
        try:
            conn.execute("CREATE TABLE t(x)")
            conn.execute("INSERT INTO t VALUES (1)")
            r = conn.execute("SELECT x FROM t").fetchone()
            assert r["x"] == 1
        finally:
            conn.close()

    def test_default_db_path_env_override(self, tmp_path, monkeypatch):
        monkeypatch.setenv("WQB_DB_PATH", str(tmp_path / "alt.db"))
        assert db_conn.default_db_path() == str(tmp_path / "alt.db")


# ---------------- 2. 写锁 mutex（文件 token） ----------------

@pytest.fixture()
def lock_env(tmp_path, monkeypatch):
    d = tmp_path / "_dblock"
    monkeypatch.setenv("WQB_DBLOCK_DIR", str(d))
    monkeypatch.delenv("WQB_DBLOCK_DISABLE", raising=False)
    return d


class TestDbWriteLock:
    def test_acquire_then_release(self, lock_env):
        info = dwl.acquire(tag="t1", ttl_sec=600, wait_timeout=1)
        assert info["ok"] and not info["degraded"] and info["token"]
        assert (lock_env / "dbwrite.lock.json").is_file()
        dwl.release(info["token"])
        assert not (lock_env / "dbwrite.lock.json").exists()

    def test_reentrant_same_pid_renews(self, lock_env):
        i1 = dwl.acquire(tag="t1", ttl_sec=600, wait_timeout=1)
        mtime1 = os.path.getmtime(i1["token"])
        time.sleep(0.02)
        i2 = dwl.acquire(tag="t1", ttl_sec=600, wait_timeout=1)
        assert i2["ok"] and i2["token"] == i1["token"]  # 重入=续约
        assert os.path.getmtime(i2["token"]) >= mtime1
        dwl.release(i2["token"])

    def test_second_holder_times_out_degraded(self, lock_env, monkeypatch):
        """**活的外部持有者** → 等待超时 → 降级放行且不删他人 token。

        注意：伪造 pid 必须是**确定存活**的进程（用父进程 pid，与
        test_dblock_dead_holder.py::test_live_holder_is_respected 同法）。
        若拿一个大数当 pid，会被 `_reclaim_dead_holder` 判死**立即回收**——
        那是 test_dblock_dead_holder 覆盖的另一条路径，与本用例意图相反。
        """
        i1 = dwl.acquire(tag="t1", ttl_sec=600, wait_timeout=1)
        # 伪造他人持有：改成父进程 pid（测试运行期间必然存活）
        tok = lock_env / "dbwrite.lock.json"
        data = json.loads(tok.read_text(encoding="utf-8"))
        data["pid"] = os.getppid()
        tok.write_text(json.dumps(data), encoding="utf-8")
        monkeypatch.setattr(dwl.time, "sleep", lambda s: None)  # 加速轮询
        i2 = dwl.acquire(tag="t2", ttl_sec=600, wait_timeout=0.5)
        assert i2["degraded"] is True  # 降级放行（不阻断）
        assert tok.is_file()  # 他人 token 未被误删
        # 自己的 release 不应删他人 token（owner 保护）
        dwl.release(i2.get("token"))
        assert tok.is_file()

    def test_ttl_self_heal(self, lock_env, monkeypatch):
        """持有者崩溃 → token 过期（mtime 老于 TTL）→ 新进程可立即拿锁。"""
        i1 = dwl.acquire(tag="t1", ttl_sec=600, wait_timeout=1)
        tok = lock_env / "dbwrite.lock.json"
        stale = time.time() - 700  # 超过 ttl 600
        os.utime(tok, (stale, stale))
        monkeypatch.setattr(dwl.time, "sleep", lambda s: None)
        i2 = dwl.acquire(tag="t2", ttl_sec=600, wait_timeout=2)
        assert i2["ok"] and not i2["degraded"]  # 过期回收后直接拿到
        dwl.release(i2["token"])

    def test_disable_env(self, lock_env, monkeypatch):
        monkeypatch.setenv("WQB_DBLOCK_DISABLE", "1")
        info = dwl.acquire(tag="t1", wait_timeout=1)
        assert info["ok"] and info["token"] is None
        assert not (lock_env / "dbwrite.lock.json").exists()

    def test_contextmanager_releases_on_exception(self, lock_env):
        with pytest.raises(RuntimeError):
            with dwl.write_lock(tag="t1", ttl_sec=600, wait_timeout=1):
                raise RuntimeError("boom")
        assert not (lock_env / "dbwrite.lock.json").exists()


# ---------------- 3. 静态禁裸 connect（防回归主闸） ----------------

ALLOWED_FILES = {REPO / p for p in db_conn.DIRECT_CONNECT_WHITELIST}
SCAN_ROOTS = [REPO / "src", REPO / "tools",
              REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit",
              REPO / "Claude" / "skills" / "brain-make-some-gem",
              REPO / "Claude" / "skills" / "brain-data-feature-engineering"]
EXCLUDE_DIR_PARTS = {"legacy", "attic", "__pycache__", "_scratch"}
EXCLUDE_PREFIXES = ("backfill_", "migrate_", "triage_", "calibrate_q3", "submit_883")


class TestNoNakedSqliteConnect:
    def test_no_naked_connect_outside_whitelist(self):
        """活跃代码白名单外禁止 sqlite3.connect( —— 裸连接是 database is locked
        事故根因之一（timeout 不一、无 WAL）。新连接一律走 wqb.db_conn / _lib.db。"""
        violations = []
        for root in SCAN_ROOTS:
            if not root.is_dir():
                continue
            for p in root.rglob("*.py"):
                parts = set(p.parts)
                if parts & EXCLUDE_DIR_PARTS:
                    continue
                if p.name.startswith(EXCLUDE_PREFIXES) or p in ALLOWED_FILES:
                    continue
                text = p.read_text(encoding="utf-8", errors="replace")
                for lineno, line in enumerate(text.splitlines(), 1):
                    s = line.strip()
                    if "sqlite3.connect(" in s and not s.startswith("#"):
                        # 允许工厂内的定义与 re-export
                        violations.append(f"{p.relative_to(REPO)}:{lineno}: {s[:90]}")
        assert not violations, "白名单外出现裸 sqlite3.connect（应改走 wqb.db_conn / _lib.db）:\n" + "\n".join(violations)

    def test_whitelist_files_exist(self):
        for f in ALLOWED_FILES:
            assert f.is_file(), f"白名单文件缺失: {f}"

    def test_whitelist_files_are_pragma_compliant(self):
        """白名单文件要么是工厂/转发层（含 db_conn 引用），要么内联含
        busy_timeout PRAGMA——防止白名单被滥用为裸连接后门。"""
        for f in ALLOWED_FILES:
            text = f.read_text(encoding="utf-8", errors="replace")
            ok = ("busy_timeout" in text) or ("from wqb.db_conn import" in text)
            assert ok, f"白名单文件缺 PRAGMA 规范或工厂转发: {f}"


# ---------------- 4. 锁探针 ----------------

class TestLockAuditProbe:
    def test_probe_once_on_tmp_db(self, tmp_path):
        sys.path.insert(0, str(REPO / "tools"))
        try:
            from db_lock_audit import probe_once  # noqa
        except ImportError:
            pytest.skip("tools 不在可导入路径（由 CLI 直接跑）")
        db = tmp_path / "probe.db"
        conn = sqlite3.connect(str(db))
        conn.execute("CREATE TABLE t(x)"); conn.commit(); conn.close()
        ev = probe_once(db_path=str(db), alert_sec=10.0, probe_timeout=5.0)
        assert ev["error"] is None
        assert ev["wait_sec"] < 10.0
        assert ev["alert"] is False
