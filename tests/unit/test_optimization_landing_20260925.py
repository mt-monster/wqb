# -*- coding: utf-8 -*-
"""2026-09-25 优化落地回归：
P9 upsert_ledger_key append/merge 防覆写模式；
P3 get_alpha_corr_metrics 相关性值保鲜期标注（corr_age_hours / corr_stale）。"""
import datetime
import importlib.util
import sqlite3
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


_SCHEMA = """
CREATE TABLE ledger_kv (
    id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT,
    created_at TEXT, updated_at TEXT
);
CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE alphas (
    id INTEGER PRIMARY KEY, alpha_id TEXT, region_id INTEGER,
    sharpe REAL, fitness REAL, turnover REAL,
    prod_correlation REAL, self_correlation REAL,
    prod_corr_source TEXT, corr_checked_at TEXT,
    status TEXT, date_submitted TEXT
);
"""


@pytest.fixture()
def dbm(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "_wqb_db_mcp_opt20260925", str(REPO_ROOT / "wqb_db_mcp.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.DB_PATH = tmp_path / "opt.db"  # 绝不碰真库
    conn = sqlite3.connect(str(mod.DB_PATH))
    conn.executescript(_SCHEMA)
    conn.commit()
    conn.close()

    import types

    def _fn(name):
        f = getattr(mod, name)
        return getattr(f, "fn", f)  # FastMCP FunctionTool → 原函数

    return types.SimpleNamespace(
        DB_PATH=mod.DB_PATH,
        upsert_ledger_key=_fn("upsert_ledger_key"),
        get_alpha_corr_metrics=_fn("get_alpha_corr_metrics"),
    )


# ---------------- P9: upsert_ledger_key append / merge ----------------


def test_p9_replace_default_behavior_preserved(dbm):
    r1 = dbm.upsert_ledger_key("GLB", "k1", {"a": 1})
    assert r1["action"] == "inserted" and r1["mode"] == "replace"
    r2 = dbm.upsert_ledger_key("GLB", "k1", {"b": 2})
    assert r2["action"] == "updated"
    conn = sqlite3.connect(str(dbm.DB_PATH))
    val = conn.execute("SELECT value FROM ledger_kv WHERE key='k1'").fetchone()[0]
    conn.close()
    assert '"b": 2' in val and '"a": 1' not in val  # 旧行为：整值覆盖


def test_p9_append_list_concat(dbm):
    dbm.upsert_ledger_key("GLB", "log", [{"n": 1}], mode="append")
    r = dbm.upsert_ledger_key("GLB", "log", [{"n": 2}], mode="append")
    assert r["action"] == "updated" and r["appended_n"] == 1 and r["total_n"] == 2
    r = dbm.upsert_ledger_key("GLB", "log", {"n": 3}, mode="append")  # 单值自动包装
    assert r["total_n"] == 3
    conn = sqlite3.connect(str(dbm.DB_PATH))
    val = conn.execute("SELECT value FROM ledger_kv WHERE key='log'").fetchone()[0]
    conn.close()
    import json
    assert json.loads(val) == [{"n": 1}, {"n": 2}, {"n": 3}]


def test_p9_append_refuses_non_list_existing_and_never_clobbers(dbm):
    dbm.upsert_ledger_key("GLB", "cfg", {"a": 1})
    r = dbm.upsert_ledger_key("GLB", "cfg", ["x"], mode="append")
    assert "error" in r and "not list" in r["error"]
    conn = sqlite3.connect(str(dbm.DB_PATH))
    val = conn.execute("SELECT value FROM ledger_kv WHERE key='cfg'").fetchone()[0]
    conn.close()
    assert '"a": 1' in val  # 原值未被覆写


def test_p9_merge_recursive_and_refuses_mismatch(dbm):
    dbm.upsert_ledger_key("GLB", "wl", {"datasets": ["a"], "meta": {"x": 1, "y": 2}}, mode="replace")
    r = dbm.upsert_ledger_key("GLB", "wl", {"meta": {"y": 9, "z": 3}, "note": "n"}, mode="merge")
    assert r["action"] == "updated" and r["merged_keys"] == 2
    import json
    conn = sqlite3.connect(str(dbm.DB_PATH))
    val = json.loads(conn.execute("SELECT value FROM ledger_kv WHERE key='wl'").fetchone()[0])
    conn.close()
    assert val["datasets"] == ["a"]  # 未覆盖的键保留
    assert val["meta"] == {"x": 1, "y": 9, "z": 3}  # 递归合并：新值胜标量
    assert val["note"] == "n"
    # 错配拒绝：list 上 merge → error 且不覆写
    r2 = dbm.upsert_ledger_key("GLB", "datasets_key", [1], mode="replace")
    r3 = dbm.upsert_ledger_key("GLB", "datasets_key", {"a": 1}, mode="merge")
    assert "error" in r3 and "not dict" in r3["error"]
    # 非 dict value 拒绝
    r4 = dbm.upsert_ledger_key("GLB", "wl", [1], mode="merge")
    assert "error" in r4


def test_p9_invalid_mode_rejected(dbm):
    r = dbm.upsert_ledger_key("GLB", "k", 1, mode="overwrite")
    assert "error" in r


# ---------------- P7: 任务状态 meta 权威 + deferred 延后态 ----------------


def test_p7_dir_layout_honors_explicit_meta_status(tmp_path):
    """meta.json 显式 status 优先于『死进程+stderr 空→succeeded』推断（gem 402 误报事故）。"""
    from wqb.workflow import tasks as wt

    task_root = tmp_path / "tasks"
    tdir = task_root / "gem_test_failed"
    tdir.mkdir(parents=True)
    import json as _json

    (tdir / "meta.json").write_text(
        _json.dumps({
            "task_id": "gem_test_failed", "pid": 999999,
            "status": "failed", "error": "exit code 1",
            "started_at": "2026-09-25T12:00:00", "finished_at": "2026-09-25T12:01:00",
            "cmd": ["python", "x"],
        }),
        encoding="utf-8",
    )
    # traceback 打在 stdout、stderr 干净——旧推断会误判 succeeded
    (tdir / "stdout.log").write_text("RuntimeError: Moonshot API error 402\n", encoding="utf-8")
    (tdir / "stderr.log").write_text("", encoding="utf-8")
    old_root = wt.task_root  # 存函数对象（不是调用结果）
    try:
        wt.task_root = lambda: str(task_root)
        got = wt.get_task("gem_test_failed")
    finally:
        wt.task_root = old_root
    assert got["status"] == "failed"
    assert got["error"]


def test_p7_dir_layout_meta_completed_maps_to_succeeded(tmp_path):
    from wqb.workflow import tasks as wt

    task_root = tmp_path / "tasks"
    tdir = task_root / "gem_test_ok"
    tdir.mkdir(parents=True)
    import json as _json

    (tdir / "meta.json").write_text(
        _json.dumps({"task_id": "gem_test_ok", "pid": 999999, "status": "completed"}),
        encoding="utf-8",
    )
    old_root = wt.task_root
    try:
        wt.task_root = lambda: str(task_root)
        got = wt.get_task("gem_test_ok")
    finally:
        wt.task_root = old_root
    assert got["status"] == "succeeded"


def test_p7_deferred_not_dispatched_by_load_wave_expressions(tmp_path):
    """deferred 为真延后态：默认派发视图排除，显式 status 过滤可见。"""
    from wqb.store import CampaignStore

    store = CampaignStore(str(tmp_path / "defer.db"))
    try:
        store.upsert_expressions(
            "GLB",
            "w_defer_test",
            [
                {"expression": "rank(x1)", "status": "selected"},
                {"expression": "rank(x2)", "status": "gated"},
                {"expression": "rank(x3)", "status": "deferred"},
            ],
        )
        rows = store.load_wave_expressions("GLB", "w_defer_test")
        statuses = sorted(r.get("status") for r in rows)
        assert statuses == ["gated", "selected"]  # deferred 不进派发视图
        only_deferred = store.list_expressions("GLB", "w_defer_test", status="deferred")
        assert len(only_deferred) == 1 and only_deferred[0]["expression"] == "rank(x3)"
    finally:
        store.close()


def _seed_alpha(conn, alpha_id, hours_ago, prod=0.5):
    checked = None
    if hours_ago is not None:
        t = datetime.datetime.now() - datetime.timedelta(hours=hours_ago)
        checked = t.strftime("%Y-%m-%dT%H:%M:%S")
    conn.execute(
        "INSERT INTO alphas (alpha_id, region_id, sharpe, fitness, turnover, "
        "prod_correlation, self_correlation, prod_corr_source, corr_checked_at, status) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        (alpha_id, 1, 2.0, 1.5, 0.1, prod, 0.2, "check_correlation", checked, "UNSUBMITTED"),
    )


def test_p3_staleness_annotation(dbm):
    conn = sqlite3.connect(str(dbm.DB_PATH))
    conn.execute("INSERT INTO regions (id, name) VALUES (1, 'GLB')")
    _seed_alpha(conn, "fresh1", hours_ago=1)
    _seed_alpha(conn, "stale1", hours_ago=72)
    _seed_alpha(conn, "null1", hours_ago=None)
    conn.commit()
    conn.close()
    rows = dbm.get_alpha_corr_metrics(region="GLB")
    by_id = {r["alpha_id"]: r for r in rows}
    assert by_id["fresh1"]["corr_stale"] is False
    assert by_id["fresh1"]["corr_age_hours"] < 48
    assert by_id["stale1"]["corr_stale"] is True
    assert by_id["stale1"]["corr_age_hours"] > 48
    assert by_id["null1"]["corr_stale"] is True
    assert by_id["null1"]["corr_age_hours"] is None


def test_p3_custom_stale_after_hours(dbm):
    conn = sqlite3.connect(str(dbm.DB_PATH))
    conn.execute("INSERT INTO regions (id, name) VALUES (1, 'GLB')")
    _seed_alpha(conn, "mid1", hours_ago=30)
    conn.commit()
    conn.close()
    rows = dbm.get_alpha_corr_metrics(region="GLB", stale_after_hours=48)
    assert rows[0]["corr_stale"] is False
    rows = dbm.get_alpha_corr_metrics(region="GLB", stale_after_hours=10)
    assert rows[0]["corr_stale"] is True


def test_p3_space_separated_timestamp_parsed(dbm):
    conn = sqlite3.connect(str(dbm.DB_PATH))
    conn.execute("INSERT INTO regions (id, name) VALUES (1, 'GLB')")
    t = datetime.datetime.now() - datetime.timedelta(hours=2)
    conn.execute(
        "INSERT INTO alphas (alpha_id, region_id, sharpe, fitness, turnover, "
        "prod_correlation, self_correlation, prod_corr_source, corr_checked_at, status) "
        "VALUES (?,?,?,?,?,?,?,?,?,?)",
        ("sp1", 1, 2.0, 1.5, 0.1, 0.5, 0.2, "manual", t.strftime("%Y-%m-%d %H:%M:%S"), "UNSUBMITTED"),
    )
    conn.commit()
    conn.close()
    rows = dbm.get_alpha_corr_metrics(region="GLB")
    assert rows[0]["corr_stale"] is False and rows[0]["corr_age_hours"] < 48