# -*- coding: utf-8 -*-
"""P0-1 开波前 prod 探针（`campaign_intel.py prod-probe`）守护。

两条轴：
  1. **封族线单源**：CLI `--prod-max` 缺省必须 == `wave_gate_pkg.gates_pf.PROBE_SEAL_THRESHOLD`
     （0.75）。两处各自演化 = 「CLI 判封族」与「闸认封族」错位；prod-first 的 0.7 不得被抄过来。
  2. **早退不联网**：新集（无历史行）/ 无强度候选 / --dry-run / 锁被占 四条路径都在
     import `brain_api` 之前返回（与仓内 dry-run 契约一致）；命中探针时才写
     `prod_family_*`（带 probe=true）+ `prod_probe_*` 台账，有族被封 ⇒ exit 2。

依据：reports/usa_mining_history_review_20261023.md §10 P0-1。
"""
import asyncio
import importlib.util
import os
import sqlite3
import sys
import types

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load(name="campaign_intel"):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(REPO, "tools", "campaign_intel.py"))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def _make_db(tmp_path, rows=(), alpha_id=None):
    """最小库：backtest_results / alphas / ledger_kv（prod-probe 只碰这三张表）。"""
    p = tmp_path / "wqb.db"
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE backtest_results (alpha_id TEXT, region TEXT, dataset TEXT, "
              "sharpe REAL, fitness REAL, turnover REAL, two_year_sharpe REAL, "
              "ra_failed_checks TEXT, code TEXT, wave TEXT)")
    c.execute("CREATE TABLE alphas (alpha_id TEXT PRIMARY KEY, prod_correlation REAL, "
              "prod_corr_source TEXT, corr_checked_at TEXT)")
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY AUTOINCREMENT, region TEXT NOT NULL, "
              "key TEXT NOT NULL, value JSON NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
              "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(region, key))")
    c.executemany(
        "INSERT INTO backtest_results(alpha_id, region, dataset, sharpe, fitness, turnover, "
        "two_year_sharpe, ra_failed_checks, code, wave) VALUES(?,?,?,?,?,?,?,?,?,?)", rows)
    if alpha_id:
        c.execute("INSERT INTO alphas(alpha_id) VALUES(?)", (alpha_id,))
    c.commit()
    c.close()
    return p


def _args(ci, *extra):
    return ci.build_parser().parse_args(
        ["prod-probe", "--region", "TESTREG", "--dataset", "dsX", *extra])


# ---------------------------------------------------------------------------
# 1. 封族线单源
# ---------------------------------------------------------------------------
def test_cli_prod_max_default_matches_gate_threshold():
    """CLI 封族线 == 闸 PF 的 PROBE_SEAL_THRESHOLD（改一处必须改另一处）。"""
    ci = _load()
    from wave_gate_pkg.gates_pf import PROBE_SEAL_THRESHOLD
    a = ci.build_parser().parse_args(
        ["prod-probe", "--region", "USA", "--dataset", "insider_agg_matrix"])
    assert a.prod_max == pytest.approx(PROBE_SEAL_THRESHOLD)
    assert PROBE_SEAL_THRESHOLD == pytest.approx(0.75)


def test_prod_first_default_unchanged():
    """prod-first（收批后）仍用 0.7：它的语义是「本波 STOP」，不是开波前封族线。"""
    ci = _load()
    a = ci.build_parser().parse_args(["prod-first", "--region", "R", "--wave", "w1"])
    assert a.prod_max == pytest.approx(0.7)


def test_main_dispatches_prod_probe(monkeypatch):
    """`main()` 的派发表必须登记 prod-probe（漏登记 = 解析通过、运行 KeyError）。"""
    ci = _load()
    seen = {}

    def fake_run(coro):
        seen["name"] = coro.cr_code.co_name
        coro.close()
        return 0

    monkeypatch.setattr(ci, "_bootstrap", lambda: None)
    monkeypatch.setattr(ci.asyncio, "run", fake_run)
    monkeypatch.setattr(sys, "argv",
                        ["campaign_intel.py", "prod-probe", "--region", "USA",
                         "--dataset", "x", "--dry-run"])
    with pytest.raises(SystemExit) as e:
        ci.main()
    assert e.value.code == 0
    assert seen["name"] == "_cmd_prod_probe"


# ---------------------------------------------------------------------------
# 2. 早退路径（都不应 import brain_api —— 所以本文件全程不装 MCP 环境）
# ---------------------------------------------------------------------------
def test_no_history_exits_zero_with_p1_1_hint(monkeypatch, tmp_path, capsys):
    """新集无历史行 ⇒ exit 0 + 提示走 P1-1 裸探针（不是静默跳过）。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[])
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    rc = asyncio.run(ci._cmd_prod_probe(_args(ci)))
    assert rc == 0
    err = capsys.readouterr().err
    assert "无历史回测行" in err and "P1-1" in err


def test_no_strength_candidate_exits_zero(monkeypatch, tmp_path, capsys):
    """有历史行但全低于 --min-sharpe ⇒ 不探（先裸探针验强度）。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[
        ("A1", "TESTREG", "dsX", 0.4, 0.3, 0.2, 0.5, "[]", "rank(ts_mean(field_alpha, 22))", "w1"),
    ])
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    rc = asyncio.run(ci._cmd_prod_probe(_args(ci)))
    assert rc == 0
    assert "无 |S|≥1.0 候选" in capsys.readouterr().err


def test_dry_run_lists_probes_and_writes_nothing(monkeypatch, tmp_path, capsys):
    """--dry-run：列拟探族，不联网/不写库（ledger/alphas 均为空）。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[
        ("A1", "TESTREG", "dsX", 2.0, 1.5, 0.2, 2.2, "[]", "rank(ts_mean(field_alpha, 22))", "w1"),
        ("A2", "TESTREG", "dsX", 1.9, 1.4, 0.2, 2.0, "[]", "rank(ts_mean(field_alpha, 22))", "w2"),  # 同族
        ("A3", "TESTREG", "dsX", 1.2, 1.1, 0.2, 1.3, "[]", "rank(ts_delta(field_gamma, 5))", "w1"),
    ], alpha_id="A1")
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    monkeypatch.setattr(ci, "_pf_acquire_lock", lambda: pytest.fail("dry-run 不应取锁"))
    rc = asyncio.run(ci._cmd_prod_probe(_args(ci, "--dry-run")))
    out = capsys.readouterr().out
    assert rc == 0
    assert "dry-run：拟探 2 个族" in out          # A1/A2 同族只留 1 + A3
    c = sqlite3.connect(dbp)
    assert c.execute("SELECT COUNT(*) FROM ledger_kv").fetchone()[0] == 0
    assert c.execute("SELECT prod_correlation FROM alphas").fetchone()[0] is None
    c.close()


def test_lock_busy_exits_three_before_network(monkeypatch, tmp_path, capsys):
    """锁被占（另一 prod 探针在跑）⇒ exit 3，且尚未 import brain_api。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[
        ("A1", "TESTREG", "dsX", 2.0, 1.5, 0.2, 2.2, "[]", "rank(ts_mean(field_alpha, 22))", "w1"),
    ])
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    monkeypatch.setattr(ci, "_pf_acquire_lock", lambda: None)
    monkeypatch.setitem(sys.modules, "brain_api", None)  # 若提前 import 会 ImportError
    rc = asyncio.run(ci._cmd_prod_probe(_args(ci)))
    assert rc == 3
    assert "另一个 prod 探针进程" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# 3. 探针完成：指纹带 probe=true，封族 ⇒ exit 2，台账带耗时
# ---------------------------------------------------------------------------
class _FakeBrain:
    def __init__(self, values):
        self.values = values
        self.calls = []

    async def ensure_authenticated(self):
        return None

    async def check_correlation(self, alpha_id, correlation_type="production",
                                threshold=0.7, refresh=False):
        self.calls.append(alpha_id)
        v = self.values[alpha_id]
        return {"checks": {"production": {"max_correlation": v,
                                          "passes_check": v < threshold}}}

    @property
    def last_calls(self):
        return self.calls


def _inject_brain(monkeypatch, values):
    fake = _FakeBrain(values)
    mod = types.ModuleType("brain_api")
    mod.BrainApiClient = lambda *a, **k: fake
    monkeypatch.setitem(sys.modules, "brain_api", mod)
    return fake


def test_probe_seals_family_and_writes_fingerprints(monkeypatch, tmp_path, capsys):
    """prod=0.81 ≥ 0.75 ⇒ SEAL：写 probe=true 指纹 + summary（含 started_at/at）+ exit 2。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[
        ("A1", "TESTREG", "dsX", 2.0, 1.5, 0.2, 2.2, "[]", "rank(ts_mean(field_alpha, 22))", "w1"),
        ("A2", "TESTREG", "dsX", 1.8, 1.3, 0.2, 1.9, "[]", "rank(ts_delta(field_beta, 5))", "w1"),
    ], alpha_id="A1")
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    monkeypatch.setattr(ci, "_pf_acquire_lock", lambda: "FAKE_LOCK")
    monkeypatch.setattr(ci, "_pf_release_lock", lambda _l: None)
    fake = _inject_brain(monkeypatch, {"A1": 0.81, "A2": 0.42})

    rc = asyncio.run(ci._cmd_prod_probe(_args(ci, "--top-k", "2", "--refresh")))
    out = capsys.readouterr().out
    assert rc == 2                                   # 有族被封
    assert set(fake.last_calls) == {"A1", "A2"}      # 每族 1 条

    c = sqlite3.connect(dbp)
    c.row_factory = sqlite3.Row
    import json as _json
    rows = {r["key"]: _json.loads(r["value"]) for r in
            c.execute("SELECT key, value FROM ledger_kv WHERE region='TESTREG'")}
    assert "prod_family_TESTREG_rank→ts_mean" in rows
    fp = rows["prod_family_TESTREG_rank→ts_mean"]
    assert fp["probe"] is True and fp["sealed"] is True
    assert fp["prod_corr"] == pytest.approx(0.81)
    assert fp["alpha_id"] == "A1" and fp["dataset"] == "dsX"
    assert "prod_family_TESTREG_rank→ts_delta" in rows
    assert rows["prod_family_TESTREG_rank→ts_delta"]["sealed"] is False
    summary = rows["prod_probe_TESTREG_dsX"]
    assert summary["sealed"] == 1 and summary["clean"] == 1 and summary["probed"] == 2
    assert summary["prod_max"] == pytest.approx(0.75)
    assert summary["started_at"] and summary["at"]
    assert summary["sealed_families"][0]["family"] == "field_alpha"   # 台账记字段族名
    assert c.execute("SELECT prod_correlation FROM alphas WHERE alpha_id='A1'").fetchone()[0] \
        == pytest.approx(0.81)
    c.close()


def test_probe_clean_returns_zero(monkeypatch, tmp_path):
    """全族 < 0.75 ⇒ exit 0，指纹 sealed=false（下一波照常开）。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[
        ("A1", "TESTREG", "dsX", 2.0, 1.5, 0.2, 2.2, "[]", "rank(ts_mean(field_alpha, 22))", "w1"),
    ])
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    monkeypatch.setattr(ci, "_pf_acquire_lock", lambda: "FAKE_LOCK")
    monkeypatch.setattr(ci, "_pf_release_lock", lambda _l: None)
    _inject_brain(monkeypatch, {"A1": 0.55})
    rc = asyncio.run(ci._cmd_prod_probe(_args(ci, "--refresh")))
    assert rc == 0


def test_probe_unknown_prod_does_not_write_fingerprint(monkeypatch, tmp_path):
    """平台返回 pending（无 max_correlation）⇒ UNKNOWN：不写指纹、不写 alphas 列。"""
    ci = _load()
    dbp = _make_db(tmp_path, rows=[
        ("A1", "TESTREG", "dsX", 2.0, 1.5, 0.2, 2.2, "[]", "rank(ts_mean(field_alpha, 22))", "w1"),
    ])
    monkeypatch.setattr(ci, "db_connect", lambda _p: sqlite3.connect(dbp))
    monkeypatch.setattr(ci, "_pf_acquire_lock", lambda: "FAKE_LOCK")
    monkeypatch.setattr(ci, "_pf_release_lock", lambda _l: None)

    class _PendingBrain(_FakeBrain):
        async def check_correlation(self, alpha_id, **kw):
            return {"status": "pending", "checks": {"production": {"max_correlation": None}},
                    "message": "prod calc queued"}

    mod = types.ModuleType("brain_api")
    mod.BrainApiClient = lambda *a, **k: _PendingBrain({})
    monkeypatch.setitem(sys.modules, "brain_api", mod)

    rc = asyncio.run(ci._cmd_prod_probe(_args(ci, "--max-tries", "1", "--poll-sec", "0", "--refresh")))
    assert rc == 0
    c = sqlite3.connect(dbp)
    n_fp = c.execute("SELECT COUNT(*) FROM ledger_kv WHERE key LIKE 'prod_family_%'").fetchone()[0]
    n_sum = c.execute("SELECT COUNT(*) FROM ledger_kv WHERE key LIKE 'prod_probe_%'").fetchone()[0]
    assert n_fp == 0 and n_sum == 1
    c.close()
