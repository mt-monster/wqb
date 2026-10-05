# -*- coding: utf-8 -*-
"""N32（2026-09-28）：workflow_auto_review 在真实表结构上跑通（只读评审报告）。

此前 auto_review 从未在真实 backtest_results 上跑过（单测只覆盖 dry-run）：
  ① turnover / sharpe 等指标为 NULL 时 `bt.get(k, 0) > x` → `TypeError`（ERROR 行没有指标）；
  ② auto_report 往并不存在的 `review_results` 表 `INSERT OR REPLACE`（schema 无此表）；
  ③ auto_prescreen 走 subprocess 打平台 API，无法在真实表结构上单测；步骤按下标取，
     关掉某个 auto_* 开关即 IndexError。
本文件全部走 FastMCP 的 `call_tool` / `list_tools`（参数校验与注册表都是真的），
在真实 CampaignStore schema 上落几行（含 NULL 指标的 ERROR 行），断言节点只读跑通且不写库。
"""
import asyncio
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

WAVE = "s2_n32_d1"


# ---------------------------------------------------------------- fixtures / helpers

@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(path))
    return path


@pytest.fixture
def db_mcp(db_path, monkeypatch):
    # 复位执行器单例：让它按本测试的 WQB_DB_PATH 解析库，测试完全命中临时库、不碰仓库真库
    monkeypatch.setattr("wqb.workflow.executor._default_executor", None, raising=False)
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)        # 读写同源；隔离失效由 get_db_path() 的结果闸兜住
    return mod


def _tools(mod):
    return {t.name: t for t in asyncio.run(mod.mcp.list_tools())}


def _call(mod, name, args):
    out = asyncio.run(mod.mcp.call_tool(name, args))
    if isinstance(out, tuple):
        out = out[1]
    if isinstance(out, dict):
        return out.get("result", out)
    return json.loads(out[0].text)


def _rows(db_path, sql, *args):
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute(sql, args).fetchall()
    finally:
        conn.close()


def _report(r):
    return next(s for s in r["output"]["steps"] if s["step"] == "auto_report")["report"]


def _seed(db_path, wave, rows):
    st = CampaignStore(str(db_path))
    st.upsert_backtest_rows("KOR", wave, rows)
    st.close()


# 三行：过硬闸的 COMPLETE、卡闸的 COMPLETE、无任何指标的 ERROR（NULL 是旧代码 TypeError 的直接触发点）
_READY = {"alpha_id": "rA", "code": "rank(a)", "status": "COMPLETE",
          "sharpe": 1.91, "fitness": 1.30, "turnover": 0.12, "two_year_sharpe": 1.7}
_WEAK = {"alpha_id": "rB", "code": "rank(b)", "status": "COMPLETE",
         "sharpe": 0.60, "fitness": 0.30, "turnover": 0.05, "two_year_sharpe": 0.4}
_ERROR = {"alpha_id": "rC", "code": "rank(c)", "status": "ERROR"}   # sharpe/fitness/turnover 全 NULL


# ---------------------------------------------------------------- 注册表

def test_workflow_auto_review_is_registered(db_mcp):
    tools = _tools(db_mcp)
    assert "workflow_auto_review" in tools
    assert {"region", "wave"} <= set(tools["workflow_auto_review"].inputSchema["properties"])
    assert not [n for n in tools if n.startswith("_")]


# ---------------------------------------------------------------- 主路径：真实 schema + NULL 指标

def test_review_reads_real_schema_with_null_metrics_and_writes_nothing(db_mcp, db_path):
    _seed(db_path, WAVE, [_READY, _WEAK, _ERROR])
    before = _rows(db_path, "SELECT * FROM backtest_results ORDER BY id")

    r = _call(db_mcp, "workflow_auto_review", {"region": "KOR", "wave": WAVE})   # 旧代码：NULL turnover → TypeError
    assert r["success"] is True, r
    assert r["output"]["backtest_count"] == 3

    rep = _report(r)
    assert (rep["total"], rep["passed"], rep["error"]) == (3, 1, 1)              # 只有 rA 过 1.58/1.0；rC 是 ERROR
    # 本地 S4 分层：rA→READY（含 tvr∈[0.04,0.40]），rC(ERROR)→REJECT，rB(弱信号 fitness<0.5 且 sharpe<1.0)→REJECT
    pre = next(s for s in r["output"]["steps"] if s["step"] == "auto_prescreen")
    assert pre["tiers"] == {"READY": 1, "REVIEW": 0, "REJECT": 2}
    assert pre["ready"] == ["rA"] and set(pre["reject"]) == {"rB", "rC"}

    # 只读：一个字节都没改，且并未凭空建出 review_results 表
    assert _rows(db_path, "SELECT * FROM backtest_results ORDER BY id") == before
    assert _rows(db_path, "SELECT name FROM sqlite_master WHERE type='table' AND name='review_results'") == []


def test_review_null_turnover_does_not_crash_even_with_prescreen_off(db_mcp, db_path):
    # 关掉 auto_prescreen：旧代码此路径不走 subprocess，直接在 walls 诊断处 NULL turnover → TypeError（快、无网络）
    _seed(db_path, "n32b", [_ERROR, _WEAK])                                     # rC 全 NULL、rB sharpe=0.6/turnover=0.05
    r = _call(db_mcp, "workflow_auto_review",
              {"region": "KOR", "wave": "n32b", "auto_prescreen": False})
    assert r["success"] is True, r                                              # 旧代码：success False（TypeError）
    steps = {s["step"] for s in r["output"]["steps"]}
    assert "auto_prescreen" not in steps                                        # 关掉的开关不建步骤（旧代码按下标取会错位/越界）
    walls = next(s for s in r["output"]["steps"] if s["step"] == "auto_walls")["walls"]
    assert walls["structural"] is True                                          # rB sharpe 0.6<1.0 触发；rC 的 NULL sharpe 不误触发
    assert walls["turnover"] is False                                           # 没有任何非空 turnover>0.7（rC 的 NULL 不误触发）


def test_review_report_only_never_touches_review_results_table(db_mcp, db_path):
    # 全为非 NULL 指标：旧代码能过 walls，但在 auto_report 处 INSERT review_results → OperationalError（快、无网络）
    _seed(db_path, "n32c", [_READY, _WEAK])
    r = _call(db_mcp, "workflow_auto_review",
              {"region": "KOR", "wave": "n32c", "auto_prescreen": False, "auto_salvage": False})
    assert r["success"] is True, r                                              # 旧代码：no such table review_results
    rep = _report(r)
    assert (rep["total"], rep["passed"]) == (2, 1)
    assert _rows(db_path, "SELECT name FROM sqlite_master WHERE type='table' AND name='review_results'") == []


def test_review_says_so_when_wave_has_no_rows(db_mcp, db_path):
    r = _call(db_mcp, "workflow_auto_review", {"region": "KOR", "wave": "empty"})
    assert r["success"] is False and "empty" in r["error"]


def test_review_salvage_legs_matched_by_boost_dim_null_safe(db_mcp, db_path):
    # salvage_pool 里放一条 boost_2y 辅助腿；卡 2Y 闸的行应命中它（NULL 指标不得让检索崩）
    st = CampaignStore(str(db_path))
    st.upsert_backtest_rows("KOR", "n32d", [_ERROR, _WEAK])                     # rC NULL、rB 2Y=0.4<1.58
    st.upsert_ledger("KOR", "salvage_pool",
                     {"entries": [{"alpha_id": "leg1", "boost_dims": ["boost_2y"]},
                                  {"alpha_id": "leg2", "boost_dims": ["boost_tvr"]}]})
    st.close()
    r = _call(db_mcp, "workflow_auto_review", {"region": "KOR", "wave": "n32d"})
    assert r["success"] is True, r
    sv = next(s for s in r["output"]["steps"] if s["step"] == "auto_salvage")
    assert sv["salvage_count"] == 1 and [e["alpha_id"] for e in sv["salvage_legs"]] == ["leg1"]
