# -*- coding: utf-8 -*-
"""S6 事件埋点守护（2026-10-02 落地，方案 B step_events）。

步 9（S6）复盘回写的两个客观动作此前**没有埋点**，导致 step_eval 的
salvage / kb_refresh 维度恒为空（不是「没发生」，而是「没人记账」）：

  * `salvage_collected`  ← `wqb_db_mcp.py::seal_dead_end`（判死沉降真正入池的残值）
  * `region_kb_refreshed` ← `campaign.py::run(assemble-priors)`（区域 KB→priors 刷新）

契约：
  * 事件只在**动作真正发生**时写入（沉降 0 条不记；失败不记）；
  * 埋点走 `safe_record_event`（永不抛）——事件台账是旁路观察者，绝不阻塞主流程；
  * `dedupe_key` 幂等：同一 dead_end 重封、同一天多次跑 assemble-priors 不重复计数。
"""
import importlib
import os
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

QK = "0123456789"


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    return path


@pytest.fixture
def isolated_db(db_path, monkeypatch):
    """step_events.record_event 经 resolve_db_path() 解析库路径，优先读 WQB_DB_PATH。
    必须隔离，否则会写进真实默认库 data/wqb.db。"""
    monkeypatch.setenv("WQB_DB_PATH", str(db_path))
    return db_path


@pytest.fixture
def mcp(db_path, monkeypatch):
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)        # 读写同源；隔离失效由 get_db_path() 的结果闸兜住
    return mod


def _events(db_path, event_type=None):
    conn = sqlite3.connect(str(db_path))
    try:
        # step_events 是惰性建表（首次写事件才建）——没写过事件时表不存在，按空处理
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='step_events'"
        ).fetchone()
        if not exists:
            return []
        if event_type:
            return conn.execute(
                "SELECT region, wave, step, event_type, value, source, dedupe_key "
                "FROM step_events WHERE event_type=?", (event_type,),
            ).fetchall()
        return conn.execute("SELECT event_type FROM step_events").fetchall()
    finally:
        conn.close()


def _seed_wave_via_ledger(mcp, region, wave_number, alpha_ids):
    """构造一个含候选的 wave_results 行，供 seal_dead_end 沉降扫描。
    候选带 sharpe=1.0（达辅料线），才会真正入 salvage_pool。"""
    import json
    conn = sqlite3.connect(str(mcp.DB_PATH))
    try:
        conn.execute(
            "INSERT INTO wave_results(region, wave_number, candidates) VALUES (?,?,?)",
            (region, wave_number, json.dumps([{"alpha_id": a, "sharpe": 1.0} for a in alpha_ids])),
        )
        conn.commit()
    finally:
        conn.close()


def _seed_reliable_negative(mcp, region="KOR", qkey=QK):
    mcp._upsert_ledger_raw(region, f"forum_recon_negative_{qkey}",
                           {"found": False, "status": "no_result", "question_key": qkey,
                            "searched_at": "2026-10-02T00:00:00"})


# ------------------------------------------------------------- salvage_collected
def test_salvage_collected_event_written_when_residue_enters_pool(mcp, isolated_db):
    _seed_reliable_negative(mcp)
    _seed_wave_via_ledger(mcp, "KOR", 1, ["A1", "A2"])
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-EVT-DEAD", family="f", reason="r", rule="u",
                            wave_numbers=[1],
                            forum_recon={"question_key": QK, "found": False, "status": "no_result"})
    assert out["status"] == "success"
    rows = _events(isolated_db, "salvage_collected")
    assert len(rows) == 1, rows
    region, wave, step, etype, value, source, dedupe = rows[0]
    assert region == "KOR" and step == "S6" and etype == "salvage_collected"
    assert source == "wqb_db_mcp.py::seal_dead_end"
    assert value == float(out["salvaged_count"])
    assert dedupe == "seal_dead_end:KOR-EVT-DEAD"


def test_no_salvage_event_when_nothing_enters_pool(mcp, isolated_db):
    """沉降 0 条（波次无候选）→ 不记事件——事件语义是「动作发生」，不是「调用发生」。"""
    _seed_reliable_negative(mcp)
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-EVT-DEAD", family="f", reason="r", rule="u",
                            wave_numbers=[],  # 不扫任何波
                            forum_recon={"question_key": QK, "found": False, "status": "no_result"})
    assert out["status"] == "success" and out["salvaged_count"] == 0
    assert _events(isolated_db, "salvage_collected") == []


def test_resealing_same_dead_end_does_not_double_count(mcp, isolated_db):
    _seed_reliable_negative(mcp)
    _seed_wave_via_ledger(mcp, "KOR", 1, ["A1"])
    kw = dict(region="KOR", entry_id="KOR-EVT-DEAD", family="f", reason="r", rule="u", wave_numbers=[1],
              forum_recon={"question_key": QK, "found": False, "status": "no_result"})
    mcp.seal_dead_end(**kw)
    mcp.seal_dead_end(region="KOR", entry_id="KOR-EVT-DEAD")   # 幂等重封
    rows = _events(isolated_db, "salvage_collected")
    assert len(rows) == 1, f"dedupe_key 未生效：{rows}"


def test_instrumentation_never_breaks_seal_when_db_unwritable(mcp, monkeypatch):
    """旁路契约：事件台账写失败绝不阻塞判死（safe_record_event 吞异常）。"""
    _seed_reliable_negative(mcp)
    _seed_wave_via_ledger(mcp, "KOR", 1, ["A1"])
    import wqb.step_events as SE

    def _boom(*a, **k):
        raise sqlite3.OperationalError("database is locked")
    monkeypatch.setattr(SE, "record_event", _boom)
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-EVT-DEAD", family="f", reason="r", rule="u",
                            wave_numbers=[1],
                            forum_recon={"question_key": QK, "found": False, "status": "no_result"})
    assert out["status"] == "success" and out["salvaged_count"] == 1   # 主流程照常


# ------------------------------------------------------------- region_kb_refreshed
def test_region_kb_event_source_is_the_assemble_priors_node():
    """埋点位置必须落在 assemble-priors 成功分支（源码级守护，防被误删）。"""
    src = (REPO / "src" / "wqb" / "workflow" / "nodes" / "campaign.py").read_text(encoding="utf-8")
    assert '"region_kb_refreshed"' in src
    assert "campaign.py::run(assemble-priors)" in src
    # 事件必须写在 `_wait_and_collect` 收尾线程的 assemble-priors 成功分支里
    # （紧跟 assemble_priors_cache 写库之后，同一 elif 块）
    i_branch = src.index('elif subcommand == "assemble-priors":\n                        # 与上方 cache_key 同名')
    i_cache = src.index("assemble_priors_cache_{region}", i_branch)
    i_evt = src.index("region_kb_refreshed", i_branch)
    assert i_cache < i_evt, "事件应写在缓存标记之后（同一分支）"
    assert i_evt - i_branch < 1200, "事件应与该分支其他写库动作相邻，不应飘到别处"


def test_both_event_types_are_registered_in_closed_vocab():
    from wqb.step_events import EVENT_VOCAB
    assert "salvage_collected" in EVENT_VOCAB
    assert "region_kb_refreshed" in EVENT_VOCAB


def test_record_region_kb_event_roundtrip(isolated_db):
    """按埋点参数实写一次，验证词表/step/幂等键组合合法可落库。"""
    from wqb.step_events import record_event, query_events
    r = record_event("KOR", "S2", "region_kb_refreshed", value=1.0,
                     source="campaign.py::run(assemble-priors)",
                     dedupe_key="assemble-priors:20261002",
                     metadata={"wave": None}, db_path=str(isolated_db))
    assert r["recorded"] is True
    r2 = record_event("KOR", "S2", "region_kb_refreshed", value=1.0,
                      source="campaign.py::run(assemble-priors)",
                      dedupe_key="assemble-priors:20261002",
                      metadata={"wave": None}, db_path=str(isolated_db))
    assert r2["recorded"] is False and r2["reason"] == "duplicate"
    assert len(query_events(region="KOR", event_type="region_kb_refreshed",
                            db_path=str(isolated_db))) == 1
