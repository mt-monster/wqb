# -*- coding: utf-8 -*-
"""2026-09-27 两个 P0 的回归护栏（见 reports/ra_pipeline_stage_review_20260927.md N1 / N2）。

P0-1  wave_results 写入契约（src/wqb/wave_results_contract.py）
      - 只补写 key_findings 不得清空已有 verdict（此前会 → 停止规则 B 把该波当 UNKNOWN、放行下一波）
      - status='closed' 必须带 verdict；字符串波号（s2_<ds>_d1）可经 MCP 读写
      - MCP 工具与 DirectDBWriter 直写兜底走同一实现
P0-2  priors 快照回流
      - campaign 节点 assemble-priors 默认带 --snapshot-ledger、不拼 --dataset/--wave
      - GEM 节点在快照缺失 / 早于 KB 源（region_kb / template_kb / operator_principle_kb /
        registry win·dead_end）时给出可见告警；两种写入时钟（本地 T / UTC 空格）先归一再比
      - （真实环境演练补充）assemble-priors 不受 S2 开波闸拦截 —— 区域停波时知识仍能回流
"""
import asyncio
import importlib
import json
import sqlite3
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src", REPO_ROOT / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402
from wqb import wave_results_contract as contract  # noqa: E402


# ---------------------------------------------------------------- fixtures

@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()          # 建出完整 schema（含 wave_results / ledger_kv）
    return path


@pytest.fixture
def db_mcp(db_path, monkeypatch):
    """加载 wqb_db_mcp 并把模块级 DB_PATH 指到临时库（它不读 WQB_DB_PATH，必须改属性）。"""
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)        # 读写同源；隔离失效由 get_db_path() 的结果闸兜住
    return mod


def _row(db_path, region, wave):
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute(
            "SELECT verdict, status, key_findings FROM wave_results WHERE region=? AND wave_number=?",
            (region, str(wave)),
        ).fetchone()
    finally:
        conn.close()


# ---------------------------------------------------------------- P0-1：合并语义

def test_findings_only_update_keeps_verdict(db_mcp, db_path):
    assert db_mcp.upsert_wave_result("KOR", 104, verdict="FAIL", key_findings=["0 达标"])["action"] == "inserted"
    r = db_mcp.upsert_wave_result("KOR", 104, key_findings=["[pyramid] ANALYST 2/3"])
    assert r["action"] == "updated" and r["updated_fields"] == ["key_findings"]
    verdict, status, findings = _row(db_path, "KOR", 104)
    assert (verdict, status) == ("FAIL", "closed")
    assert json.loads(findings) == ["[pyramid] ANALYST 2/3"]      # 传入即整列替换


def test_insert_closed_without_verdict_is_rejected(db_mcp, db_path):
    r = db_mcp.upsert_wave_result("KOR", 7, key_findings=["探针全灭"])
    assert "error" in r and "verdict" in r["error"]
    assert _row(db_path, "KOR", 7) is None                         # 拒绝即不写库


def test_open_wave_without_verdict_is_allowed(db_mcp, db_path):
    assert db_mcp.upsert_wave_result("KOR", 8, status="open", focus="进行中")["action"] == "inserted"
    assert _row(db_path, "KOR", 8)[:2] == (None, "open")


def test_writing_verdict_closes_open_wave(db_mcp, db_path):
    db_mcp.upsert_wave_result("KOR", 9, status="open")
    db_mcp.upsert_wave_result("KOR", 9, verdict="PARTIAL")
    assert _row(db_path, "KOR", 9)[:2] == ("PARTIAL", "closed")


def test_findings_only_update_on_open_wave_keeps_it_open(db_mcp, db_path):
    db_mcp.upsert_wave_result("KOR", 10, status="open")
    db_mcp.upsert_wave_result("KOR", 10, key_findings=["中途记录"])
    assert _row(db_path, "KOR", 10)[:2] == (None, "open")


def test_hollow_closed_row_must_get_a_verdict(db_mcp, db_path):
    conn = sqlite3.connect(str(db_path))
    conn.execute("INSERT INTO wave_results (region, wave_number, status) VALUES ('KOR', '11', 'closed')")
    conn.commit()
    conn.close()
    r = db_mcp.upsert_wave_result("KOR", 11, key_findings=["补记"])
    assert "error" in r
    assert db_mcp.upsert_wave_result("KOR", 11, verdict="FAIL", key_findings=["补记"])["action"] == "updated"
    assert _row(db_path, "KOR", 11)[:2] == ("FAIL", "closed")


def test_normalized_verdict_note_keeps_existing_findings(db_mcp, db_path):
    db_mcp.upsert_wave_result("KOR", 12, verdict="FAIL", key_findings=["a", "b"])
    db_mcp.upsert_wave_result("KOR", 12, verdict="RED: 14 全灭")
    verdict, _, findings = _row(db_path, "KOR", 12)
    assert verdict == "FAIL"
    assert json.loads(findings) == ["原 verdict（写入时归一）: RED: 14 全灭", "a", "b"]


def test_unrecognized_verdict_and_bad_status_rejected(db_mcp, db_path):
    assert "error" in db_mcp.upsert_wave_result("KOR", 13, verdict="机制确认但天花板明确")
    assert "error" in db_mcp.upsert_wave_result("KOR", 13, verdict="FAIL", status="done")
    assert _row(db_path, "KOR", 13) is None


def test_string_and_int_wave_numbers(db_mcp, db_path):
    db_mcp.upsert_wave_result("KOR", "s2_analyst44_d1", verdict="FAIL")
    assert db_mcp.get_wave_result("KOR", "s2_analyst44_d1")["verdict"] == "FAIL"
    db_mcp.upsert_wave_result("KOR", 97, verdict="PASS")
    assert db_mcp.get_wave_result("KOR", "97")["verdict"] == "PASS"   # 97 与 "97" 是同一行


def test_mcp_layer_accepts_string_wave_numbers(db_mcp):
    """经 FastMCP 参数校验层调用（此前 wave_number: int 会直接拒绝字符串波号）。"""
    async def go():
        await db_mcp.mcp.call_tool("upsert_wave_result",
                                   {"region": "KOR", "wave_number": "s2_pv1_d1", "verdict": "FAIL"})
        return await db_mcp.mcp.call_tool("get_wave_result",
                                          {"region": "KOR", "wave_number": "s2_pv1_d1"})
    out = asyncio.run(go())
    assert '"FAIL"' in str(out)


def test_stop_rule_b_survives_findings_only_update(db_mcp, db_path, tmp_path, monkeypatch):
    """端到端：3 个 closed FAIL 波 → 规则 B 拦截；只补写 key_findings 后仍拦截。"""
    from wqb.workflow.nodes import campaign as cp

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    monkeypatch.delenv("WQB_DISABLE_STOP_RULES_GATE", raising=False)
    camp = tmp_path / "tracking" / "KOR"
    (camp / "config").mkdir(parents=True)
    for w in (1, 2, 3):
        db_mcp.upsert_wave_result("KOR", w, verdict="FAIL")
    assert cp._run_stop_rules_gate("KOR", None, str(camp))["success"] is False

    db_mcp.upsert_wave_result("KOR", 3, key_findings=["[pyramid] ANALYST 2/3"])
    gate = cp._run_stop_rules_gate("KOR", None, str(camp))
    assert gate["success"] is False, gate
    assert gate["evidence"]["recent_closed_verdicts"] == ["FAIL", "FAIL", "FAIL"]


def test_direct_db_writer_shares_the_contract(db_path):
    from mcp_batch_writer import DirectDBWriter

    with DirectDBWriter(str(db_path)) as w:
        assert w.upsert_wave_result("KOR", "w4", verdict="FAIL")["action"] == "inserted"
        assert w.upsert_wave_result("KOR", "w4", key_findings=["x"])["action"] == "updated"
        assert "error" in w.upsert_wave_result("KOR", "w5", key_findings=["y"])
    assert _row(db_path, "KOR", "w4")[:2] == ("FAIL", "closed")
    assert _row(db_path, "KOR", "w5") is None


def test_contract_rejects_unknown_columns():
    conn = sqlite3.connect(":memory:")
    with pytest.raises(TypeError):
        contract.upsert_wave_result(conn, "KOR", 1, "2026-09-27T00:00:00", verdcit="FAIL")


# ---------------------------------------------------------------- P0-2：priors 快照

def _campaign_dry_run(monkeypatch, **params):
    from wqb.workflow.nodes import campaign as cp

    for gate in ("WQB_DISABLE_SIGNAL_FLOOR_GATE", "WQB_DISABLE_STOP_RULES_GATE",
                 "WQB_DISABLE_BACKLOG_GATE"):
        monkeypatch.setenv(gate, "1")
    result = cp.run(region="KOR", stage="S2", subcommand="assemble-priors",
                    _context={"dry_run": True}, **params)
    assert result["success"] is True, result
    return next(s["command"] for s in result["steps"] if s.get("step") == "build_command").split()


def test_assemble_priors_command_writes_snapshot(monkeypatch):
    cmd = _campaign_dry_run(monkeypatch, dataset="analyst44", wave="105")
    tail = cmd[cmd.index("assemble-priors"):]
    assert tail == ["assemble-priors", "--snapshot-ledger"], cmd   # 不拼 --dataset/--wave


def test_assemble_priors_snapshot_flag_not_duplicated(monkeypatch):
    cmd = _campaign_dry_run(monkeypatch, extra_args=["--snapshot-ledger"])
    assert cmd.count("--snapshot-ledger") == 1, cmd


def test_assemble_priors_not_blocked_by_stop_rules(db_mcp, db_path, monkeypatch):
    """真实环境演练发现：区域命中停止规则 B 后，S2 开波闸连 assemble-priors 一起拦 → 快照永远刷不新。"""
    from wqb.workflow.nodes import campaign as cp

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    for gate in ("WQB_DISABLE_SIGNAL_FLOOR_GATE", "WQB_DISABLE_STOP_RULES_GATE", "WQB_DISABLE_BACKLOG_GATE"):
        monkeypatch.delenv(gate, raising=False)
    for w in (1, 2, 3):
        db_mcp.upsert_wave_result("KOR", w, verdict="FAIL")

    wave = cp.run(region="KOR", stage="S2", dataset="analyst44", wave="4", _context={"dry_run": True})
    assert wave["success"] is False and "停止规则" in wave["error"]        # 开波仍被拦

    priors = cp.run(region="KOR", stage="S2", subcommand="assemble-priors", _context={"dry_run": True})
    assert priors["success"] is True, priors
    steps = {s["step"]: s for s in priors["steps"]}
    assert steps["region_gates"]["skipped"] is True and "stop_rules_gate" not in steps
    assert steps["build_command"]["command"].endswith("assemble-priors --snapshot-ledger")


def _ledger(db_path, region, key, updated_at):
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) VALUES (?,?,?,?,?)",
        (region, key, json.dumps({"wins": [], "dead_ends": []}), updated_at, updated_at),
    )
    conn.commit()
    conn.close()


def test_gem_warns_when_snapshot_older_than_region_kb(db_path, monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _ledger(db_path, "KOR", "priors_snapshot_kor", "2026-09-20T10:00:00")
    _ledger(db_path, "KOR", "region_kb", "2026-09-21T09:00:00")
    step = gem._priors_snapshot_freshness("KOR")
    assert step["stale_sources"] == ["KOR/region_kb@2026-09-21 09:00:00"]
    assert "assemble-priors" in step["warning"]


def test_gem_warns_when_registry_changed_after_snapshot(db_path, monkeypatch):
    """S6 最常见的回写是判死封存 / 登记 win（registry_empirical），不是 region_kb。"""
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _ledger(db_path, "KOR", "priors_snapshot_kor", "2026-09-21T09:05:00")
    _ledger(db_path, "GLOBAL", "region_kb", "2026-09-22T00:00:00")    # 不是 assemble-priors 的源
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "INSERT INTO registry_empirical (region, layer, entry_id, payload, created_at, updated_at) "
        "VALUES ('KOR', 'dead_end', 'KOR-X-DEAD', '{}', ?, ?)", ("2026-09-21T10:00:00",) * 2)
    conn.commit()
    conn.close()
    step = gem._priors_snapshot_freshness("KOR")
    assert step["stale_sources"] == ["KOR/registry_empirical(win,dead_end)@2026-09-21 10:00:00"]


@pytest.mark.skipif(not hasattr(time, "tzset"), reason="time.tzset 仅 POSIX 可用")
def test_ledger_ts_converts_sqlite_utc_to_local(monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("TZ", "Asia/Shanghai")
    time.tzset()
    try:
        assert gem._ledger_ts("2026-09-27 04:00:00") == "2026-09-27 12:00:00"   # SQLite datetime('now')：UTC
        assert gem._ledger_ts("2026-09-27T04:00:00") == "2026-09-27 04:00:00"   # Python isoformat：本地
    finally:
        monkeypatch.undo()
        time.tzset()


def test_gem_quiet_when_snapshot_is_fresh(db_path, monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    _ledger(db_path, "KOR", "region_kb", "2026-09-21T09:00:00")
    _ledger(db_path, "KOR", "priors_snapshot_kor", "2026-09-21T09:05:00")
    step = gem._priors_snapshot_freshness("KOR")
    assert "warning" not in step and "stale_sources" not in step


def test_gem_dry_run_reports_missing_snapshot(db_path, monkeypatch):
    from wqb.workflow.nodes import gem

    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    # 显式给 data_category：否则 infer_data_category 走 _common._platform_category，
    # 它用模块常量 _DB_PATH（不认 WQB_DB_PATH）connect，会在仓库默认路径建出空库
    result = gem.run(region="KOR", dataset_id="analyst44", delay=1, universe="TOP600",
                     data_category="analyst", _context={"dry_run": True})
    step = next(s for s in result["steps"] if s.get("step") == "priors_snapshot_check")
    assert "fail-closed" in step["warning"]
    assert step["warning"] in result.get("warnings", [])
