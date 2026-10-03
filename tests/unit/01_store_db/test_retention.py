# -*- coding: utf-8 -*-
"""test_retention.py — tools/retention.py 的守护测试（2026-10-03）

为什么需要守护测试
------------------
磁盘已连续 5 次回涨（2026-09-20 清到 390M → 09-25 472M → 10-03 **1210M +
cache/ 296M**）。旧报告 P3 建议过保留策略工具，但「建议」不解决问题——**没有
守护的策略等于没有策略**：靠人记得跑，几个月后必然回涨。

所以本文件的核心不是测工具功能（那是 pytest 的基本职责），而是**把复发变成
CI 红灯**：断言 data/ 备份数量、cache/ 陈旧探针体积在阈值内。任何人（或
并行会话）再堆备份，测试即红。

⚠ 测试**只读**，不删任何真实文件；工具的删除路径用 tmp_path 沙箱验证。
"""
import importlib.util
import os
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "retention.py"

#: 守护阈值（与 AGENTS.md §8.3 既定政策一致：data/ 只留 live + 最新 1 份备份）
MAX_DATA_BAKS = 2          # 最新 1 份 + 允许 1 份在途（正在恢复/比对中）
MAX_STALE_PROBE_MB = 1024  # cache/_probe 允许的陈旧体积上限
PROBE_STALE_DAYS = 7


def _load_tool():
    """按文件路径加载 tools/retention.py（tools/ 不是包）。"""
    spec = importlib.util.spec_from_file_location("wq_retention", TOOL)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ret():
    if not TOOL.is_file():
        pytest.skip("tools/retention.py 不存在")
    return _load_tool()


def _age(path: Path, days: float, now: float) -> None:
    ts = now - days * 86400
    os.utime(path, (ts, ts))


# ---------------- 沙箱行为验证（不碰真实仓库） ----------------

def test_collect_data_baks_keeps_newest_and_spares_live(ret, tmp_path, monkeypatch):
    """只回收超出保留数的旧备份；live DB 与 WAL 附属永不进候选。"""
    data = tmp_path / "data"
    data.mkdir()
    (data / "wqb.db").write_bytes(b"live")
    (data / "wqb.db-wal").write_bytes(b"wal")
    (data / "wqb.db-shm").write_bytes(b"shm")
    now = time.time()
    for i, age_days in enumerate([9.0, 5.0, 0.5]):   # 3 份备份，新→旧
        p = data / f"wqb.db.bak_2026{i:02d}"
        p.write_bytes(b"x" * 1024)
        _age(p, age_days, now)

    monkeypatch.setattr(ret, "DATA", data)
    targets = ret.collect_data_baks(keep=1)
    names = sorted(t.path.name for t in targets)

    # 最新那份（age 0.5）被保留 → 应回收 age 9.0 与 5.0 两份
    assert names == ["wqb.db.bak_202600", "wqb.db.bak_202601"]
    for t in targets:
        assert t.path.name not in ret.LIVE_DB_NAMES


def test_collect_data_baks_spares_live_even_when_only_live_exists(ret, tmp_path, monkeypatch):
    """只有 live DB 时候选必须为空（回归：keep=0 也不许删 live）。"""
    data = tmp_path / "data"
    data.mkdir()
    (data / "wqb.db").write_bytes(b"live")
    monkeypatch.setattr(ret, "DATA", data)
    assert ret.collect_data_baks(keep=1) == []
    assert ret.collect_data_baks(keep=0) == []


def test_collect_stale_probe_dbs_respects_age(ret, tmp_path, monkeypatch):
    """超过保留期的探针库进候选，未超期的保留。"""
    cache = tmp_path / "cache"
    probe = cache / "_probe"
    probe.mkdir(parents=True)
    now = time.time()
    old, new = probe / "old.db", probe / "new.db"
    for f, age in ((old, 30.0), (new, 1.0)):
        f.write_bytes(b"x" * 2048)
        _age(f, age, now)
    monkeypatch.setattr(ret, "CACHE", cache)

    targets = ret.collect_stale_probe_dbs(keep_days=7, now=now)
    assert [t.path.name for t in targets] == ["old.db"]



def test_collect_logs_skips_protected_runtime_dirs(ret, tmp_path, monkeypatch):
    """⚠ 并发会话的运行时状态目录（_dblock/_slots/_async_tasks）绝不可进候选。

    这些目录由运行中的 MCP 进程持续读写，删了会破坏在跑流水线（AGENTS.md §8.4）。
    """
    logs = tmp_path / "logs"
    for d in ret.LOGS_PROTECTED_DIRS:
        (logs / d).mkdir(parents=True)
        (logs / d / "state.json").write_text("{}")
    ptmp = logs / "_pytest_run_123"
    ptmp.mkdir()
    (logs / "old.txt").write_text("x")
    now = time.time()
    _age(logs / "old.txt", 60.0, now)
    monkeypatch.setattr(ret, "LOGS", logs)

    targets = ret.collect_logs(keep_days=14, now=now)
    names = {t.path.name for t in targets}
    assert "old.txt" in names
    assert any(n.startswith("_pytest_") for n in names)
    for protected in ret.LOGS_PROTECTED_DIRS:
        assert protected not in names, f"受保护运行时目录被列入回收：{protected}"


def test_main_check_exit_codes(ret, tmp_path, monkeypatch):
    """--check 有可回收项返回 1（守护测试靠这个退出码）；非法参数返回 2。"""
    data = tmp_path / "data"
    data.mkdir()
    (data / "wqb.db").write_bytes(b"live")
    now = time.time()
    for i, age in enumerate([20.0, 1.0]):
        p = data / f"wqb.db.bak_x{i}"
        p.write_bytes(b"x")
        _age(p, age, now)
    monkeypatch.setattr(ret, "DATA", data)
    monkeypatch.setattr(ret, "CACHE", tmp_path / "nope")
    monkeypatch.setattr(ret, "LOGS", tmp_path / "nope2")

    assert ret.main(["--check"]) == 1
    assert ret.main(["--keep-data-baks", "0", "--check"]) == 2  # 参数非法


def test_main_dry_run_does_not_delete(ret, tmp_path, monkeypatch):
    """★ 默认 dry-run 绝不能删文件（删除纪律：一切删除走显式确认）。"""
    data = tmp_path / "data"
    data.mkdir()
    (data / "wqb.db").write_bytes(b"live")
    stale, fresh = data / "wqb.db.bak_old", data / "wqb.db.bak_new"
    stale.write_bytes(b"y" * 1024)
    _age(stale, 40.0, time.time())
    fresh.write_bytes(b"z" * 1024)
    monkeypatch.setattr(ret, "DATA", data)
    monkeypatch.setattr(ret, "CACHE", tmp_path / "nope")
    monkeypatch.setattr(ret, "LOGS", tmp_path / "nope2")

    assert ret.main([]) == 0            # dry-run 成功
    assert stale.is_file(), "dry-run 删了文件——严重回归"
    assert fresh.is_file()

    # --apply 才真删，且只删超期的
    assert ret.main(["--apply"]) == 0
    assert not stale.exists(), "--apply 应删超期备份"
    assert fresh.is_file(), "--apply 误删了保留期内备份"
    assert (data / "wqb.db").is_file(), "--apply 删了 live DB——灾难性回归"


# ---------------- ★ 守护断言：真实仓库的复发防线 ----------------

def test_real_data_dir_backup_count_within_policy(ret):
    """★ 真实 data/ 的备份数必须在阈值内。

    2026-10-03 实测曾堆到 3 份陈旧备份（合计 900 MB）→ 复发即红。
    阈值 2 = 最新 1 份 + 允许 1 份在途。
    """
    if not ret.DATA.is_dir():
        pytest.skip("data/ 不存在（干净克隆）")
    baks = [p for p in ret.DATA.iterdir()
            if p.is_file() and p.name not in ret.LIVE_DB_NAMES
            and any(p.name.startswith(pfx) for pfx in ret.DATA_BAK_PREFIXES)]
    assert len(baks) <= MAX_DATA_BAKS, (
        f"data/ 有 {len(baks)} 份备份（>{MAX_DATA_BAKS}），超保留策略：\n"
        + "\n".join(
            f"  · {p.name}  {p.stat().st_size / 1048576:.1f} MB  "
            f"{time.strftime('%Y-%m-%d', time.localtime(p.stat().st_mtime))}"
            for p in sorted(baks))
        + "\n  → 跑 `python tools/retention.py` 查看，--apply 回收"
    )


def test_real_cache_stale_probe_volume_within_limit(ret):
    """★ 真实 cache/_probe 的陈旧体积必须在阈值内。

    2026-10-03 实测有 282.7 MB 的 probe.db（当时仅 4.07 天，未超 7 天阈值，
    故本断言当时为绿——但若长期不清理或再堆一份即会红）。
    """
    probe = ret.CACHE / "_probe"
    if not probe.is_dir():
        pytest.skip("cache/_probe 不存在")
    now = time.time()
    stale_mb = 0.0
    for f in probe.iterdir():
        if not f.is_file():
            continue
        try:
            st = f.stat()
        except OSError:
            continue
        if now - st.st_mtime > PROBE_STALE_DAYS * 86400:
            stale_mb += st.st_size / 1048576
    assert stale_mb <= MAX_STALE_PROBE_MB, (
        f"cache/_probe 有 {stale_mb:.1f} MB 陈旧产物（>{MAX_STALE_PROBE_MB} MB）"
        f" → 跑 `python tools/retention.py` 后 --apply 回收"
    )


def test_retention_cli_help_is_self_documenting(ret):
    """--help 自文档（AGENTS.md §6：工具化纪律要求 --help 自解释）。"""
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            ret.main(["--help"])
        except SystemExit:
            pass
    text = buf.getvalue()
    for flag in ("--keep-data-baks", "--probe-keep-days", "--logs-keep-days",
                 "--apply", "--check"):
        assert flag in text, f"--help 未提及 {flag}"
