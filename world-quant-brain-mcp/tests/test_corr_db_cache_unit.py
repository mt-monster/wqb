"""alpha_corr_cache 接线单元测试 —— check_correlation 的第二级（wqb 库）缓存。

背景：prod 相关性结果的缓存后端此前只有 Redis，而本机 Redis 常未启动
（``redis_client=None`` → 读写全 no-op），导致多会话各自重复打平台
单并发队列，每颗 alpha 等 1-5 分钟；self 相关性有文件缓存（pkl）所以秒回，
prod 却没有对应兜底。

本组测试验证：无 Redis 时也能用 ``data/wqb.db`` 的 ``alpha_corr_cache``
读/写 prod 结果，且库不可用时**只告警、不阻断**主查询流程。
"""
import builtins
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from brain_mixin_correlation import CorrelationMixin


def _shell():
    """构造不触发 __init__ 的空壳，只测 DB 缓存读写（不碰网络/Redis）。"""
    c = CorrelationMixin.__new__(CorrelationMixin)
    c._corr_cache_store_singleton = None
    c.log = lambda *a, **k: None
    return c


@pytest.fixture
def isolated_db(tmp_path, monkeypatch):
    """把 WQB_DB_PATH 指向临时库，避免测试写生产库。"""
    db = tmp_path / "corr.db"
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    return db


def test_db_corr_cache_write_then_hit(isolated_db):
    c = _shell()
    assert c._db_corr_cache_get("simX") is None

    c._db_corr_cache_set("simX", prod=0.8474, records=[[0.7, 0.8, 9]])

    got = c._db_corr_cache_get("simX")
    assert got is not None
    assert abs(got["max"] - 0.8474) < 1e-9
    assert got["records"] == [[0.7, 0.8, 9]]
    assert got["source"] == "platform"


def test_db_corr_cache_visible_across_instances(isolated_db):
    """跨实例可见 —— 对应「多个 MCP 进程共享同一份 SQLite」。"""
    c1 = _shell()
    c1._db_corr_cache_set("simZ", prod=0.68)

    c2 = _shell()  # 新壳 = 新连接，模拟另一个进程
    got = c2._db_corr_cache_get("simZ")
    assert got is not None
    assert abs(got["max"] - 0.68) < 1e-9


def test_db_cache_degrades_when_store_unavailable(monkeypatch):
    """库不可用时读返回 None、写静默返回，绝不抛（不阻断查询主流程）。"""
    c = _shell()
    monkeypatch.setattr(c, "_corr_cache_store", lambda: None)

    assert c._db_corr_cache_get("simY") is None
    assert c._db_corr_cache_set("simY", prod=0.5) is None


def test_corr_cache_store_marks_failure_on_import_error(monkeypatch):
    """wqb 库导入失败 → 标记哨兵，避免每次查询都重试并刷日志。"""
    c = _shell()
    warnings = []
    c.log = lambda msg, level="INFO", **k: warnings.append((level, msg))

    real_import = builtins.__import__

    def boom(name, *a, **k):
        if name == "wqb.store" or name.startswith("wqb.store."):
            raise ImportError("simulated: wqb.store unavailable")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", boom)

    assert c._corr_cache_store() is None
    assert c._corr_cache_store_singleton is False
    assert any(lvl == "WARNING" for lvl, _ in warnings)
    # 第二次调用直接命中哨兵，不再尝试导入
    assert c._corr_cache_store() is None


def test_db_corr_cache_out_of_range_rejected(isolated_db):
    """越界值不入缓存（与 persist_correlation 同口径，防异常值污染）。"""
    c = _shell()
    c._db_corr_cache_set("simW", prod=1.7)
    assert c._db_corr_cache_get("simW") is None
