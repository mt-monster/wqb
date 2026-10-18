# -*- coding: utf-8 -*-
"""tests/unit/01_store_db/test_db_write_guards.py — 并发写锁治理守卫（2026-09-20 L1/L3）。

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

REPO = Path(__file__).resolve().parents[3]
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
EXCLUDE_PREFIXES = ("backfill_", "migrate_", "triage_", "calibrate_q3", "submit_883", "fix_", "_db_")


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
        # 2026-10-14 主题下沉：db_lock_audit.py 现住 tools/db/（脚本不是包，按目录加 path）
        sys.path.insert(0, str(REPO / "tools" / "db"))
        try:
            from db_lock_audit import probe_once  # noqa
        except ImportError:
            pytest.skip("tools/db 不在可导入路径（由 CLI 直接跑）")
        db = tmp_path / "probe.db"
        conn = sqlite3.connect(str(db))
        conn.execute("CREATE TABLE t(x)"); conn.commit(); conn.close()
        ev = probe_once(db_path=str(db), alert_sec=10.0, probe_timeout=5.0)
        assert ev["error"] is None
        assert ev["wait_sec"] < 10.0
        assert ev["alert"] is False


# ---------------- 5. 测试期禁连生产库（结果层硬闸） ----------------
#
# 战例（AGENTS.md §8.4 第 9 项）：2026-10-04 拆 `wqb_db_mcp` 使 `mod.DB_PATH = tmp` 这类
# 属性式隔离**静默失效**，测试把 14 行写进了生产 `data/wqb.db`。事后在门面上加了
# `_reject_production_db_under_tests`。2026-10-14 全量回归实测到**同一类失效换了条路**：
# tools/ 与 toolkit 的直写路径走 `CampaignStore`，不经门面 ——
# `tests/unit/04_gates/test_inspect_mode_failclosed_p1p1.py` 起 subprocess 跑
# `tools/wave_gate.py`，子进程拿 CLI 缺省库位，往生产 `ledger_kv` 写了
# `KOR/gate_ws2_pytest_inspect_model109`（`updated_at=2026-10-14T23:27:21`），
# 而库里同期还躺着 2026-09-28 / 10-03 / 10-04 的测试件。所以判定本体上移到
# `wqb.db_conn`，store 与门面**共用一份**。下面这组用例守的就是这个形状。

PRODUCTION_DB = REPO / "data" / "wqb.db"


class TestProductionDbGuardUnderTests:
    def test_store_rejects_production_db_under_pytest(self, monkeypatch):
        """pytest 下 `CampaignStore(生产库)` 必须**就地报错**，不是静默写进去。"""
        from wqb.store import CampaignStore

        monkeypatch.setenv("PYTEST_CURRENT_TEST", "manual::case")
        monkeypatch.delenv("WQB_ALLOW_REAL_DB", raising=False)
        with pytest.raises(RuntimeError, match="隔离未生效"):
            CampaignStore(str(PRODUCTION_DB))

    def test_facade_and_store_share_one_implementation(self):
        """判定本体只许一处（两处各写一份早晚分叉，§8.4 第 9 项「读写同源」同一条纪律）。

        取面 = `SCAN_ROOTS`（src / tools / 三个 toolkit）+ 门面 `wqb_db_mcp.py`：
        门面必须算进来，因为这次要防的正是「门面有闸、直写路径没闸」这种半边守住的形状。
        """
        faces = [REPO / "wqb_db_mcp.py"]
        for root in SCAN_ROOTS:
            if root.is_dir():
                faces.extend(root.rglob("*.py"))
        hits = sorted(
            str(p.relative_to(REPO)).replace("\\", "/")
            for p in faces
            if not (set(p.parts) & EXCLUDE_DIR_PARTS)
            and "PYTEST_CURRENT_TEST" in p.read_text(encoding="utf-8", errors="replace")
        )
        assert hits == ["src/wqb/db_conn.py"], f"生产库闸出现第二份判定（应收敛到 wqb.db_conn）：{hits}"

    def test_tmp_db_still_constructs_under_pytest(self, tmp_path, monkeypatch):
        """非空过守卫的另一面：**已隔离**的临时库照常能用。

        ⚠ 路径形态刻意取 `tmp_path/ws/data/wqb.db`（与本仓大量用例的隔离布局一致：
        `CampaignStore.from_workspace(tmp_path/"ws")` 派生出来的就是这种仿生产结构）。
        第一版判定按「以 `/data/wqb.db` 结尾」匹配，把这类**已经隔离好**的库全认成生产库，
        实测 27 个用例 ERROR + 5 个 FAILED —— 后缀匹配是错的判据，见 `db_conn` 的说明。
        """
        from wqb.store import CampaignStore

        monkeypatch.setenv("PYTEST_CURRENT_TEST", "manual::case")
        monkeypatch.delenv("WQB_ALLOW_REAL_DB", raising=False)
        isolated = tmp_path / "ws" / "data" / "wqb.db"
        store = CampaignStore(str(isolated))
        try:
            store.upsert_ledger("KOR", "guard_probe_key", {"ok": True})
            assert store.get_ledger("KOR", "guard_probe_key") == {"ok": True}
        finally:
            store.close()
        # 顺带钉住判据的边界：仓库根那个才是生产库，临时目录里同名同布局的不算
        assert Path(db_conn.production_db_path()).resolve() == PRODUCTION_DB.resolve()

    def test_escape_hatch_is_explicit(self, monkeypatch):
        """放行必须靠显式声明：`WQB_ALLOW_REAL_DB=1` 才放行，缺省一律拦。"""
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "manual::case")
        monkeypatch.delenv("WQB_ALLOW_REAL_DB", raising=False)
        with pytest.raises(RuntimeError):
            db_conn.reject_production_db_under_tests(PRODUCTION_DB, entry="probe")
        monkeypatch.setenv("WQB_ALLOW_REAL_DB", "1")
        assert db_conn.reject_production_db_under_tests(PRODUCTION_DB, entry="probe") is None

    def test_production_runs_outside_pytest_untouched(self, monkeypatch):
        """闸只在 pytest 下生效：生产服务/CLI（无 PYTEST_CURRENT_TEST）不得被这条闸拦掉。"""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        monkeypatch.delenv("WQB_ALLOW_REAL_DB", raising=False)
        assert db_conn.reject_production_db_under_tests(PRODUCTION_DB, entry="probe") is None

    def test_windows_path_forms_are_both_caught(self, monkeypatch):
        """盘符与分隔符形态都要命中：生产库路径在 Windows 上是反斜杠的。"""
        monkeypatch.setenv("PYTEST_CURRENT_TEST", "manual::case")
        monkeypatch.delenv("WQB_ALLOW_REAL_DB", raising=False)
        for form in (str(PRODUCTION_DB), str(PRODUCTION_DB).replace("\\", "/"),
                     str(PRODUCTION_DB).upper()):
            with pytest.raises(RuntimeError, match="生产库"):
                db_conn.reject_production_db_under_tests(form, entry="probe")

    def test_toolkit_lib_db_delegates_to_core_guard(self, monkeypatch, tmp_path):
        """**第三条路径**（2026-10-15 补）：toolkit `_lib/db.connect()` 也必须被守住。

        门面与 CampaignStore 都接上判定之后，还剩一条独立取连接路径：toolkit 为了
        「装在仓库外也能跑」自带一份同构连接工厂 `_lib/db.py`，而 `_lib/ledger.py` /
        `_lib/registry.py` / `_lib/wave_results.py` / `_lib/region_gates.py` 全部经它取连接、
        且都被 `tests/` 直接驱动（库里 2026-09-29 那批 `wave_meta_covtest*` /
        `diversity_report_wcovtest*` 就是这个形状写进生产库的）。

        这一条**刻意不是再写一份判据**：`_lib/db.connect()` 委托 `wqb.db_conn` 的判定本体，
        所以上一条 `test_facade_and_store_share_one_implementation` 的
        「`PYTEST_CURRENT_TEST` 只出现在 `src/wqb/db_conn.py`」仍然成立 —— 有人把判据复制进
        skill 侧，那条用例立刻红；本条用例保证委托关系没被摘掉。
        """
        import importlib.util

        monkeypatch.setenv("PYTEST_CURRENT_TEST", "manual::case")
        monkeypatch.delenv("WQB_ALLOW_REAL_DB", raising=False)
        monkeypatch.delenv("WQB_DB_PATH", raising=False)

        mod_path = (REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
                    / "scripts" / "_lib" / "db.py")
        spec = importlib.util.spec_from_file_location("_wq_toolkit_db_probe", mod_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # 缺省库位在这台机器上就是生产库（向上探测命中仓库根）⇒ 正是静默写库的形状
        assert Path(mod.default_db_path()).resolve() == PRODUCTION_DB.resolve()
        with pytest.raises(RuntimeError, match="隔离未生效"):
            mod.connect()
        # 显式传临时库照常可用（非空过：证明拦的是「身份」而不是「toolkit 不许连库」）
        # 注：toolkit 的 connect() 不建父目录（建目录是 CampaignStore 的职责），先自建
        isolated = tmp_path / "ws" / "data" / "wqb.db"
        isolated.parent.mkdir(parents=True, exist_ok=True)
        conn = mod.connect(str(isolated))
        try:
            conn.execute("CREATE TABLE t (x)")
            conn.commit()
        finally:
            conn.close()
