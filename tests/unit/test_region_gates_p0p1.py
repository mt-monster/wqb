# -*- coding: utf-8 -*-
"""P0-1 开波闸下沉到 toolkit 入口（2026-09-17）.

背景（实测）：signal_floor / stop_rules / backlog 三道闸原先只由 workflow 的 S2/S3
节点调用，**直调 toolkit 脚本（build_wave.py / wave_gate.py）会完全绕过** ——
实证 JPN 2026-09-16：`_run_backlog_gate` 判定为拦截（conversion=0.0%），该区却照跑
完整波（gem 1,640 / 回测 0）。本模块把闸下沉到开波唯一入口。

本测试覆盖：
  1. `_lib.region_gates.run_region_gates` 的三种模式（off/warn/enforce）语义；
  2. `WQB_DISABLE_REGION_GATES=1` 逃生口；
  3. 破坏性回归：enforce 下必须 ok=False（否则下沉等于没做）。
"""
import io
import json
import sqlite3
import sys

import pytest

from wqb.workflow import _common

TK = _common.REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


@pytest.fixture
def rg():
    if str(TK) not in sys.path:
        sys.path.insert(0, str(TK))
    from _lib import region_gates
    return region_gates


def _setup(tmp_path, monkeypatch, gem=300, backtested=20):
    """造一个"积压超限"的区：gem 远多于 backtested → conversion 低。"""
    campaign = tmp_path / "tracking" / "TESTREG"
    (campaign / "config").mkdir(parents=True)
    (campaign / "config" / "thresholds.json").write_text(
        json.dumps({"diversity": {}}, ensure_ascii=False), encoding="utf-8")

    db = tmp_path / "wqb_test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE expressions (id INTEGER PRIMARY KEY, region TEXT, status TEXT)")
    conn.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    conn.execute("CREATE TABLE wave_results (region TEXT, status TEXT, verdict TEXT, "
                 "created_at TEXT, updated_at TEXT)")
    conn.execute("CREATE TABLE backtest_results (id INTEGER PRIMARY KEY, region TEXT, "
                 "sharpe REAL, fitness REAL, wave TEXT)")
    for _ in range(gem):
        conn.execute("INSERT INTO expressions (region, status) VALUES ('TESTREG','gem')")
    for _ in range(backtested):
        conn.execute("INSERT INTO expressions (region, status) VALUES ('TESTREG','backtested')")
    conn.commit()
    conn.close()

    monkeypatch.setenv("WQB_DB_PATH", str(db))
    monkeypatch.setenv("WQB_WORKSPACE_ROOT", str(_common.REPO_ROOT))
    monkeypatch.delenv("WQB_DISABLE_REGION_GATES", raising=False)
    return campaign


def test_off_mode_skips_everything(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="off", out=io.StringIO())
    assert rep["ok"] is True
    assert rep["skipped_reason"] == "gate-mode=off"
    assert rep["results"] == {}


def test_env_escape_hatch_skips(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    monkeypatch.setenv("WQB_DISABLE_REGION_GATES", "1")
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="enforce", out=io.StringIO())
    assert rep["ok"] is True
    assert "WQB_DISABLE_REGION_GATES" in str(rep["skipped_reason"])


def test_warn_mode_reports_hits_but_allows(rg, tmp_path, monkeypatch):
    """灰度默认：命中积压闸但不阻断（避免一上线就全池停摆）。"""
    campaign = _setup(tmp_path, monkeypatch)
    buf = io.StringIO()
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="warn", out=buf)
    assert rep["ok"] is True, "warn 模式不得阻断"
    assert "backlog" in rep["hits"], "gem 300/320 应命中积压闸"
    text = buf.getvalue()
    assert "灰度" in text and "未拦截" in text or "仅告警不阻断" in text


def test_enforce_mode_blocks(rg, tmp_path, monkeypatch):
    """enforce：同一场景必须 ok=False（这是"下沉"是否真正生效的判据）。"""
    campaign = _setup(tmp_path, monkeypatch)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="enforce", out=io.StringIO())
    assert rep["ok"] is False
    assert "backlog" in rep["hits"]


def test_clean_region_passes_all_gates(rg, tmp_path, monkeypatch):
    """无积压的区在 enforce 下也应放行（不得误伤）。"""
    campaign = _setup(tmp_path, monkeypatch, gem=0, backtested=300)
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="enforce", out=io.StringIO())
    assert rep["ok"] is True, f"健全区被误拦: {rep.get('hits')}"


def test_load_gates_and_invalid_mode_falls_back(rg, tmp_path, monkeypatch):
    campaign = _setup(tmp_path, monkeypatch)
    C, err = rg.load_gates(str(campaign))
    assert C is not None, f"应能从 campaign_dir 推导工作区根: {err}"
    assert callable(C._run_backlog_gate)
    # 非法 mode 回落到 warn（不阻断）
    rep = rg.run_region_gates(str(campaign), "TESTREG", mode="bogus", out=io.StringIO())
    assert rep["mode"] == rg.MODE_WARN
    assert rep["ok"] is True
