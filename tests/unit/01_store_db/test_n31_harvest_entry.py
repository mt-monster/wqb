# -*- coding: utf-8 -*-
"""N31（2026-09-27）：SOP 步 6 的手动补收入口回到 MCP 层；workflow_auto_harvest 能用了。

726a350 把 `_flatten_platform_alpha` 插进了 `harvest_multisim_results` 与它的 `@mcp.tool()` 之间：
装饰器挂到了私有函数上（公开工具里多了 `_flatten_platform_alpha`），SOP 写的
`mcp__wqb-db__harvest_multisim_results` 从此 Unknown tool，测试把这条引用列进了"已移除工具"白名单。
声称承接它的 `workflow_auto_harvest` 按不存在的列读写，三种调用方式全部报错。

本文件的调用一律走 FastMCP 的 `call_tool` / `list_tools`（参数校验与注册表都是真的），
输入是 wq-brain-http `harvest_multisim_alphas` 的返回形态（`mcp_core._slim_alpha` + alpha_id / expression）。
"""
import asyncio
import importlib
import json
import re
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

SOP = REPO_ROOT / "Claude" / "skills" / "wq-brain-ra-pipeline" / "SKILL.md"
WAVE = "s2_n31_d1"


def _platform_alpha(aid, sharpe, fitness, two_year=None):
    """harvest_multisim_alphas 返回的一条 alpha：指标嵌在 metrics，checks 分桶，ra 预计算。"""
    metrics = {"sharpe": sharpe, "fitness": fitness, "turnover": 0.12, "longCount": 300, "shortCount": 290,
               "prodCorrelation": 0.41}
    if two_year is not None:
        metrics["two_year_sharpe"] = two_year
    failed = [{"name": "LOW_SHARPE", "value": sharpe, "limit": 1.58}] if sharpe < 1.58 else []
    code = f"rank(ts_delta(x_{aid}, 5))"
    return {"alpha_id": aid, "id": aid, "expression": code, "code": code, "status": "UNSUBMITTED",
            "settings": {"region": "KOR", "universe": "TOP600", "delay": 1, "neutralization": "SUBINDUSTRY",
                         "decay": 4},
            "metrics": metrics,
            "checks": {"fail": failed, "warning": [], "pass": [], "pending": []},
            "ra": {"failed_ra_count": len(failed), "ra_failed": bool(failed),
                   **({"ra_failed_checks": ["LOW_SHARPE"]} if failed else {})}}


BATCH = [_platform_alpha("pA", 1.91, 1.30, 2.1), _platform_alpha("pB", 1.25, 0.80), _platform_alpha("pC", 0.60, 0.30)]
RESPONSE = {"success": True, "multisimulation_id": "MS_N31", "total": 3, "complete": 3, "error_count": 0,
            "alphas": BATCH, "errors": None}


# ---------------------------------------------------------------- fixtures / helpers

@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(path))
    return path


@pytest.fixture
def db_mcp(db_path, tmp_path, monkeypatch):
    cdir = tmp_path / "tracking" / "KOR"                      # near 线固定 1.2，不随仓库配置变
    (cdir / "config").mkdir(parents=True)
    (cdir / "config" / "thresholds.json").write_text(json.dumps({"near": {"sharpe_min": 1.2}}), encoding="utf-8")
    monkeypatch.setenv("WQB_CAMPAIGN_DIR", str(cdir))
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    monkeypatch.setattr(mod, "DB_PATH", db_path)
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


# ---------------------------------------------------------------- 注册表

def test_sop_harvest_entry_is_registered_and_no_private_tool_is(db_mcp):
    tools = _tools(db_mcp)
    assert "harvest_multisim_results" in tools
    assert not [n for n in tools if n.startswith("_")]            # 此前 _flatten_platform_alpha 是公开工具
    assert {"alphas", "multisim_id", "dataset"} <= set(tools["harvest_multisim_results"].inputSchema["properties"])
    assert {"alphas", "dataset"} <= set(tools["workflow_auto_harvest"].inputSchema["properties"])
    # SOP 里写的每个 wqb-db 工具都在活的注册表里（不只是静态扫描装饰器）
    # 2026-09-29：ra-pipeline 拆成核心 SKILL.md + references/（步 6 的收批命令在 step6-backtest.md）——SOP 指整个目录
    named = set(re.findall(r"mcp__wqb-db__([A-Za-z0-9_]+)",
                           "\n".join(p.read_text(encoding="utf-8") for p in sorted(SOP.parent.rglob("*.md")))))
    assert "harvest_multisim_results" in named and named <= set(tools), named - set(tools)


# ---------------------------------------------------------------- 入库（SOP 步 6 第二步）

def test_harvest_takes_platform_output_as_is(db_mcp, db_path):
    out = _call(db_mcp, "harvest_multisim_results", {"region": "KOR", "wave": WAVE, "alphas": RESPONSE})
    assert (out["upserted"], out["multisim_id"]) == (3, "MS_N31")
    assert out["wave_result"].startswith("inserted") and "暂定 verdict=PASS" in out["wave_result"]
    got = _rows(db_path, "SELECT alpha_id, sharpe, fitness, turnover, two_year_sharpe, "
                         "json_extract(payload_json, '$.multisim_id') FROM backtest_results WHERE wave=? "
                         "ORDER BY alpha_id", WAVE)
    assert got == [("pA", 1.91, 1.30, 0.12, 2.1, "MS_N31"), ("pB", 1.25, 0.80, 0.12, None, "MS_N31"),
                   ("pC", 0.60, 0.30, 0.12, None, "MS_N31")]                       # 嵌套 metrics 已拍平
    assert _rows(db_path, "SELECT verdict, source_file FROM wave_results WHERE wave_number=?", WAVE) == \
        [("PASS", "harvest:auto")]
    # 只传 alphas 列表（SOP 原写法）同样可以，按 alpha_id 幂等
    again = _call(db_mcp, "harvest_multisim_results",
                  {"region": "KOR", "wave": WAVE, "alphas": BATCH, "multisim_id": "MS_N31"})
    assert again["upserted"] == 3
    assert _rows(db_path, "SELECT COUNT(*) FROM backtest_results WHERE wave=?", WAVE) == [(3,)]


def test_harvest_says_so_when_input_is_unusable(db_mcp):
    out = _call(db_mcp, "harvest_multisim_results", {"region": "KOR", "wave": WAVE, "alphas": {"not": "alphas"}})
    assert out["upserted"] == 0 and "warning" in out                                # 此前静默返回 0
    out = _call(db_mcp, "harvest_multisim_results",
                {"region": "KOR", "wave": WAVE, "alphas": json.dumps(RESPONSE, ensure_ascii=False)})
    assert out["upserted"] == 3 and "warning" not in out


# ---------------------------------------------------------------- workflow_auto_harvest

def test_workflow_auto_harvest_ingests_then_reports(db_mcp, db_path):
    r = _call(db_mcp, "workflow_auto_harvest", {"region": "KOR", "wave": WAVE, "alphas": RESPONSE})
    assert r["success"] is True and r["ingest"]["upserted"] == 3 and r["ingest"]["multisim_id"] == "MS_N31"
    steps = {s["step"]: s for s in r["output"]["steps"]}
    assert steps["auto_harvest"]["rows"] == 3 and steps["auto_link"]["linked_count"] == 3
    rep = steps["auto_report"]["report"]
    assert (rep["total"], rep["passed"]) == (3, 1)                                   # 只有 pA 过 1.58 / 1.0
    assert _rows(db_path, "SELECT verdict FROM wave_results WHERE wave_number=?", WAVE) == [("PASS",)]


def test_workflow_auto_harvest_report_only_reads_real_schema_and_writes_nothing(db_mcp, db_path):
    st = CampaignStore(str(db_path))
    st.upsert_backtest_rows("KOR", "94", [
        {"alpha_id": "r1", "code": "rank(a)", "status": "ERROR"},                    # 没有指标的 ERROR 行
        {"alpha_id": "r2", "code": "rank(b)", "sharpe": 1.7, "fitness": 1.1, "status": "COMPLETE",
         "ra_failed_checks": ["LOW_2Y_SHARPE"]}])
    st.close()
    before = _rows(db_path, "SELECT * FROM backtest_results ORDER BY id")
    r = _call(db_mcp, "workflow_auto_harvest", {"region": "KOR", "wave": "94"})     # 此前：no column 'expression'
    assert r["success"] is True, r
    rep = next(s for s in r["output"]["steps"] if s["step"] == "auto_report")["report"]
    assert (rep["total"], rep["passed"], rep["error"]) == (2, 1, 1)
    r = _call(db_mcp, "workflow_auto_harvest", {"region": "KOR", "wave": "94", "auto_upsert": False})
    assert r["success"] is True, r                                                    # 此前：IndexError
    r = _call(db_mcp, "workflow_auto_harvest", {"region": "KOR", "wave": "94", "multisim_id": "nope"})
    assert r["success"] is False and "multisim_id=nope" in r["error"]                # 此前：no column multisim_id
    assert _rows(db_path, "SELECT * FROM backtest_results ORDER BY id") == before     # 只读：一个字节都没改
