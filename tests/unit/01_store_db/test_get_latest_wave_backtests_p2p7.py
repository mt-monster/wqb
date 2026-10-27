# -*- coding: utf-8 -*-
"""2026-10-20 P2-7：get_latest_wave 支持「有回测的最近波」（has_backtests=True）。

背景：EUR wave_results 最新 = 269（prod 扫荡，backtest_results 零行），S4 诊断读
plain get_latest_wave 拿到一个没有任何回测证据的波。has_backtests=True 先在
backtest_results 里找最近波号（CAST 数值序，同值以最近回测写入时间兜底）再回读
wave_results；默认 False 行为逐字不变（向后兼容）。

口径（写死在测试里，别放松）：
- 精确波号优先；找不到且波号为数值型时回退 CAST 相等（'91' ↔ '91c'）。
- 该波在 wave_results 无记录 / 与 status 过滤不符 → 回 error，**不回退到更旧的波**
  （避免把「无台账」伪装成「有证据」）。
- 返回附 backtest_count / backtest_last_at。
"""
import importlib
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src", REPO_ROOT / "world-quant-brain-mcp"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()          # 建出完整 schema
    return path


@pytest.fixture
def db_mcp(db_path):
    """加载 wqb_db_mcp 并把库指到临时库（set_db_path 显式 hook，非属性 patch）。"""
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)
    return mod


def _wave(db_path, region, number, status="closed", verdict="FAIL"):
    con = sqlite3.connect(str(db_path))
    try:
        con.execute(
            "INSERT INTO wave_results (region, wave_number, status, verdict, key_findings) "
            "VALUES (?,?,?,?,?)", (region, str(number), status, verdict, "[]"))
        con.commit()
    finally:
        con.close()


def _bt(db_path, region, wave, n=1, created_at=None):
    con = sqlite3.connect(str(db_path))
    try:
        for i in range(n):
            if created_at:
                con.execute(
                    "INSERT INTO backtest_results (expression_id, region, wave, sharpe, created_at) "
                    "VALUES (1,?,?,?,?)",
                    (region, str(wave), 1.0 + i, created_at))
            else:
                con.execute(
                    "INSERT INTO backtest_results (expression_id, region, wave, sharpe) VALUES (1,?,?,?)",
                    (region, str(wave), 1.0 + i))
        con.commit()
    finally:
        con.close()


def test_has_backtests_skips_sweep_wave(db_mcp, db_path):
    """EUR 269 形状：最新波无回测 → plain 给 269，has_backtests 给有回测的 261。"""
    _wave(db_path, "EUR", 269)
    _wave(db_path, "EUR", 261)
    _bt(db_path, "EUR", 261, n=20)

    plain = db_mcp.get_latest_wave("EUR")
    assert plain["wave_number"] == "269" and "backtest_count" not in plain

    with_bt = db_mcp.get_latest_wave("EUR", has_backtests=True)
    assert with_bt["wave_number"] == "261"
    assert with_bt["backtest_count"] == 20
    assert with_bt["backtest_last_at"] is not None


def test_no_backtests_region_errors(db_mcp, db_path):
    _wave(db_path, "EUR", 10)
    r = db_mcp.get_latest_wave("EUR", has_backtests=True)
    assert "error" in r and "no wave with backtests" in r["error"]


def test_backtest_wave_without_ledger_row_errors(db_mcp, db_path):
    """回测波在 wave_results 无记录 → error（不回退到 10 波）。"""
    _wave(db_path, "EUR", 10)
    _bt(db_path, "EUR", 50, n=3)
    r = db_mcp.get_latest_wave("EUR", has_backtests=True)
    assert "error" in r and "50" in r["error"] and "台账未回写" in r["error"]
    assert r["wave_number"] == "50" and r["backtest_count"] == 3


def test_status_filter_mismatch_errors_not_fallbacks(db_mcp, db_path):
    """最新回测波 status=open，过滤 closed → error 点名，不静默退到旧波。"""
    _wave(db_path, "EUR", 261, status="open")
    _wave(db_path, "EUR", 260, status="closed")
    _bt(db_path, "EUR", 261, n=5)
    _bt(db_path, "EUR", 260, n=5)
    r = db_mcp.get_latest_wave("EUR", status="closed", has_backtests=True)
    assert "error" in r and "261" in r["error"] and "open" in r["error"]


def test_status_filter_match_ok(db_mcp, db_path):
    _wave(db_path, "EUR", 261)
    _bt(db_path, "EUR", 261)
    r = db_mcp.get_latest_wave("EUR", status="closed", has_backtests=True)
    assert r.get("error") is None and r["wave_number"] == "261"


def test_numeric_cast_fallback_91c(db_mcp, db_path):
    """wave_results 存 '91c'、backtest 存 '91'：精确未中，CAST 相等回退命中。"""
    _wave(db_path, "KOR", "91c")
    _bt(db_path, "KOR", "91", n=4)
    r = db_mcp.get_latest_wave("KOR", has_backtests=True)
    assert r.get("error") is None and r["wave_number"] == "91c"


def test_string_wave_exact_match(db_mcp, db_path):
    """字符串波号（s2_<ds>_d1 形态）精确命中，不走 CAST 回退。"""
    _wave(db_path, "AMR", "s2_analyst11_d1")
    _bt(db_path, "AMR", "s2_analyst11_d1", n=8)
    r = db_mcp.get_latest_wave("AMR", has_backtests=True)
    assert r.get("error") is None and r["wave_number"] == "s2_analyst11_d1"


def test_all_string_waves_tiebreak_by_last_bt_time(db_mcp, db_path):
    """全部 CAST=0 的字符串波：以最近回测写入时间兜底（AMR 实测同形）。"""
    _wave(db_path, "AMR", "s2_a_d1")
    _wave(db_path, "AMR", "s2_b_d1")
    _bt(db_path, "AMR", "s2_a_d1", created_at="2026-10-01 10:00:00")
    _bt(db_path, "AMR", "s2_b_d1", created_at="2026-10-02 10:00:00")
    r = db_mcp.get_latest_wave("AMR", has_backtests=True)
    assert r.get("error") is None and r["wave_number"] == "s2_b_d1"


def test_numeric_beats_string_same_cast_bucket(db_mcp, db_path):
    """数值波 12 与字符串波同处（CAST 0）：数值大者胜——与既有 CAST 排序语义一致。"""
    _wave(db_path, "KOR", "s2_x_d1")
    _wave(db_path, "KOR", "12")
    _bt(db_path, "KOR", "s2_x_d1", created_at="2026-10-05 10:00:00")   # 更晚写
    _bt(db_path, "KOR", "12", created_at="2026-10-01 10:00:00")
    r = db_mcp.get_latest_wave("KOR", has_backtests=True)
    assert r.get("error") is None and r["wave_number"] == "12"