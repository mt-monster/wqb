# -*- coding: utf-8 -*-
"""2026-09-19 落地项的守卫测试：
  - prod-first 进程锁（死 pid 回收 / 活 pid 拒绝）
  - backlog-drop：只清「无回测」波；--close-backtested 只关已回测波并 drop 残留
  - prod_saturation_gate：字段饱和必须有 prod 撞墙证据（不再按本账户 IS 过闸计数误判）
  - s0-select：category_lit 默认剔除（--include-lit 保留）
"""
import asyncio
import importlib.util
import json
import os
import sqlite3
import sys
import types

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- prod-first lock
def test_prod_first_lock_recycles_dead_pid_and_blocks_live(tmp_path, monkeypatch):
    ci = _load("campaign_intel", "tools/campaign_intel.py")
    lock = tmp_path / ".prod_first.lock"
    monkeypatch.setattr(ci, "_PF_LOCK", str(lock))
    # 死 pid（极大值不可能存活）→ 回收并拿到锁
    lock.write_text("999999999", encoding="utf-8")
    monkeypatch.setattr(ci, "_pid_alive", lambda pid: False)
    assert ci._pf_acquire_lock() == str(lock)
    assert lock.read_text(encoding="utf-8") == str(os.getpid())
    # 另一个活进程持锁 → 拒绝
    lock.write_text("4242", encoding="utf-8")
    monkeypatch.setattr(ci, "_pid_alive", lambda pid: pid == 4242)
    assert ci._pf_acquire_lock() is None
    # 自己持锁 → 允许（幂等）
    lock.write_text(str(os.getpid()), encoding="utf-8")
    assert ci._pf_acquire_lock() == str(lock)
    ci._pf_release_lock(str(lock))
    assert not lock.exists()


# ---------------------------------------------------------------- backlog-drop
def _mk_backlog_db(path):
    conn = sqlite3.connect(path)
    conn.executescript("""
    CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE waves (id INTEGER PRIMARY KEY, region_id INTEGER, wave_number TEXT, status TEXT);
    CREATE TABLE expressions (id INTEGER PRIMARY KEY, wave_id INTEGER, region TEXT, wave TEXT,
        expression TEXT, status TEXT, alpha_id TEXT, created_at TEXT, updated_at TEXT);
    CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, wave TEXT, alpha_id TEXT);
    CREATE TABLE gate_results (id INTEGER PRIMARY KEY, region TEXT, wave TEXT);
    INSERT INTO regions VALUES (1, 'USA');
    -- w1: 陈旧、无 gate、无回测 → 该 drop
    INSERT INTO waves VALUES (1, 1, 'old_pool', 'pending');
    INSERT INTO expressions VALUES (1, 1, 'USA', 'old_pool', 'rank(a)', 'pending', NULL, '2026-01-01T00:00:00', NULL);
    INSERT INTO expressions VALUES (2, 1, 'USA', 'old_pool', 'rank(b)', 'pending', NULL, '2026-01-01T00:00:00', NULL);
    -- w2: 陈旧但有 gate → 默认不动，--include-gated 才动
    INSERT INTO waves VALUES (2, 1, 'gated_pool', 'gated');
    INSERT INTO expressions VALUES (3, 2, 'USA', 'gated_pool', 'rank(c)', 'gated', NULL, '2026-01-01T00:00:00', NULL);
    INSERT INTO gate_results VALUES (1, 'USA', 'gated_pool');
    -- w3: 已回测（部分残留未跑）→ 永不 drop；--close-backtested 关掉并 drop 残留
    INSERT INTO waves VALUES (3, 1, '77', 'gated');
    INSERT INTO expressions VALUES (4, 3, 'USA', '77', 'rank(d)', 'selected', 'ALPHA1', '2026-01-01T00:00:00', NULL);
    INSERT INTO expressions VALUES (5, 3, 'USA', '77', 'rank(e)', 'selected', NULL, '2026-01-01T00:00:00', NULL);
    INSERT INTO backtest_results VALUES (1, 'USA', '77', 'ALPHA1');
    -- w4: 新鲜、无回测 → 不动
    INSERT INTO waves VALUES (4, 1, 'fresh', 'pending');
    INSERT INTO expressions VALUES (6, 4, 'USA', 'fresh', 'rank(f)', 'pending', NULL, '2099-01-01T00:00:00', NULL);
    """)
    conn.commit()
    conn.close()


def _run_backlog(ci, tmp_path, **kw):
    a = types.SimpleNamespace(region=None, older_than_days=7, pattern=None, include_gated=False,
                              include_backtested=False, show=50, apply=False, close_backtested=False)
    for k, v in kw.items():
        setattr(a, k, v)
    return asyncio.run(ci._cmd_backlog_drop(a))


def test_backlog_drop_only_touches_unbacktested_stale_waves(tmp_path, monkeypatch, capsys):
    ci = _load("campaign_intel", "tools/campaign_intel.py")
    db = tmp_path / "data" / "wqb.db"
    db.parent.mkdir()
    _mk_backlog_db(str(db))
    monkeypatch.setattr(ci, "_REPO_ROOT", str(tmp_path))

    # dry-run 不写库
    assert _run_backlog(ci, tmp_path) == 0
    conn = sqlite3.connect(str(db))
    assert conn.execute("SELECT status FROM waves WHERE id=1").fetchone()[0] == "pending"

    # apply：只有 w1 被 drop；w2（有 gate）/w3（有回测）/w4（新鲜）不动
    _run_backlog(ci, tmp_path, apply=True)
    st = dict(conn.execute("SELECT id, status FROM waves").fetchall())
    assert st == {1: "dropped", 2: "gated", 3: "gated", 4: "pending"}
    assert conn.execute("SELECT COUNT(*) FROM expressions WHERE wave_id=1 AND status='dropped'").fetchone()[0] == 2

    # --include-gated：w2 也 drop；w3 仍不动
    _run_backlog(ci, tmp_path, apply=True, include_gated=True)
    st = dict(conn.execute("SELECT id, status FROM waves").fetchall())
    assert st[2] == "dropped" and st[3] == "gated"

    # --close-backtested：w3 → closed，残留未跑的 e5 → dropped，已跑的 e4 不动
    _run_backlog(ci, tmp_path, apply=True, close_backtested=True)
    assert conn.execute("SELECT status FROM waves WHERE id=3").fetchone()[0] == "closed"
    assert conn.execute("SELECT status FROM expressions WHERE id=5").fetchone()[0] == "dropped"
    assert conn.execute("SELECT status FROM expressions WHERE id=4").fetchone()[0] == "selected"
    # 幂等：重跑零变更
    _run_backlog(ci, tmp_path, apply=True, include_gated=True, close_backtested=True)
    assert conn.execute("SELECT status FROM waves WHERE id=4").fetchone()[0] == "pending"
    conn.close()


# ---------------------------------------------------------------- prod_saturation_gate
class _FakeStore:
    def __init__(self, rows):
        self._rows = rows

    def search_alphas_by_sharpe(self, region, min_sharpe, limit):
        return self._rows

    def close(self):
        pass


def test_prod_saturation_requires_prod_wall_evidence(monkeypatch):
    psg = _load("prod_saturation_gate", "tools/prod_saturation_gate.py")
    # 同一字段 10 条 IS 过闸 alpha：无任何 prod 信息 → 只是 candidate，不 FAIL
    rows = [{"expression": "rank(ts_zscore(vec_avg(fld_a), 252))", "sharpe": 1.8, "dataset_id": 1,
             "prod_correlation": None} for _ in range(10)]
    monkeypatch.setattr(psg, "_load_store", lambda db_path=None: _FakeStore(rows))
    rep = psg.check_wave(["rank(ts_delta(vec_avg(fld_a), 66))"], "IND")
    assert rep["status"] == "enforced" and rep["passed"] is True
    assert rep["saturated_fields"] == [] and rep["saturation_candidates_no_prod"] == ["fld_a"]
    # 已知 prod 中 ≥50% 撞墙且 ≥2 条 → 饱和 FAIL
    rows2 = [dict(r, prod_correlation=0.82 if i < 6 else 0.4) for i, r in enumerate(rows)]
    monkeypatch.setattr(psg, "_load_store", lambda db_path=None: _FakeStore(rows2))
    rep = psg.check_wave(["rank(ts_delta(vec_avg(fld_a), 66))"], "IND")
    assert rep["saturated_fields"] == ["fld_a"] and rep["passed"] is False
    # 只有 1 条撞墙（其余干净）→ 不饱和（IND mean_flash_estimate_eps prod 0.58 误判的根因）
    rows3 = [dict(r, prod_correlation=0.9 if i == 0 else 0.55) for i, r in enumerate(rows)]
    monkeypatch.setattr(psg, "_load_store", lambda db_path=None: _FakeStore(rows3))
    rep = psg.check_wave(["rank(ts_delta(vec_avg(fld_a), 66))"], "IND")
    assert rep["saturated_fields"] == [] and rep["passed"] is True


# ---------------------------------------------------------------- pipeline stage_prod_first hook
def test_pipeline_has_prod_first_stage_and_flag():
    pl = _load("pipeline_landing", "Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py")
    assert callable(getattr(pl, "stage_prod_first", None))
    src = open(os.path.join(REPO, "Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py"), encoding="utf-8").read()
    assert '"--prod-first"' in src and "stage_prod_first(ctx, a)" in src
    assert 'choices=["explore", "repair", "probe"]' in src
