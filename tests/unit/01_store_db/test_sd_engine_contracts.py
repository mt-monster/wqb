# -*- coding: utf-8 -*-
"""skills 审查 S-D（引擎与执行层）的代码侧决策（2026-09-29，DEC-33..36）的回归护栏。

DEC-33  submit_ready 单存储：提交队列 = SQL 表 `submit_ready`；MCP `get_submit_ready` 读它，不再读 ledger 同名键
DEC-34  registry 写入契约单一实现（`wqb.registry_contract`）：CLI 与 MCP `upsert_registry_empirical` /
        `seal_dead_end` 共用；MCP 不再照单全收
DEC-35  多样性增强缺省 never：`build_wave.py` / `batch_simulator.py` 不改写显式 idea 的表达式
DEC-36  `ledger set-verdict` 废止提示（逐波结论的唯一真相源 = wave_results.verdict）；`pipeline --force` 语义写准
"""
import importlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOLKIT = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
for _p in (REPO, REPO / "src", REPO / "tools", TOOLKIT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402
from wqb import registry_contract as rc  # noqa: E402


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    return path


@pytest.fixture
def mcp(db_path, monkeypatch):
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    mod.set_db_path(db_path)        # 读写同源；隔离失效由 get_db_path() 的结果闸兜住
    return mod


def _reg_rows(db_path, region="KOR", layer="dead_end"):
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute(
            "SELECT entry_id, family, payload, dead_at FROM registry_empirical WHERE region=? AND layer=?",
            (region, layer)).fetchall()
    finally:
        conn.close()


# ----------------------------------------------------------------------------- DEC-34 契约本身

def test_dead_end_requires_id_family_reason_rule():
    ok = {"id": "KOR-X-DEAD", "family": "x", "reason": "带数据的理由", "rule": "下次怎么办"}
    assert rc.validate("dead_end", ok)["id"] == "KOR-X-DEAD"
    for missing in ("id", "family", "reason", "rule"):
        bad = {k: v for k, v in ok.items() if k != missing}
        with pytest.raises(rc.RegistryContractError, match=missing):
            rc.validate("dead_end", bad)


def test_contract_fills_dead_at_and_win_date():
    de = rc.validate("dead_end", {"id": "a", "family": "f", "reason": "r", "rule": "u"}, today="2026-09-29")
    assert de["dead_at"] == "2026-09-29"
    win = rc.validate("win", {"id": "w", "what": "concept", "key": "settings"}, today="2026-09-29")
    assert win["date"] == "2026-09-29"
    assert rc.dead_at_of(win) == "2026-09-29"                 # win 层的日期存进 dead_at 列（沿用旧行为）


def test_contract_campaign_status_enum_and_accessors():
    assert rc.STATUS_OK == ("untried", "in_progress", "exhausted")
    with pytest.raises(rc.RegistryContractError, match="status"):
        rc.validate("campaign", {"dataset": "d", "status": "done"})
    p = rc.validate("campaign", {"dataset": "model219", "status": "untried"})
    assert rc.entry_id_of("campaign", p) == "model219" and rc.family_of("campaign", p) == "model219"
    assert rc.family_of("win", {"what": "c"}) == "c" and rc.family_of("orphan", {"id": "o"}) is None


def test_contract_rejects_unknown_layer_and_non_dict():
    with pytest.raises(rc.RegistryContractError, match="layer"):
        rc.validate("cross_region", {"id": "x"})               # 免校验层不走 validate
    with pytest.raises(rc.RegistryContractError, match="对象"):
        rc.validate("dead_end", "not a dict")


def test_toolkit_cli_uses_the_shared_contract_not_a_copy():
    src = (TOOLKIT / "_lib" / "registry.py").read_text(encoding="utf-8")
    assert "registry_contract" in src
    assert "REQUIRED = {" not in src and "STATUS_OK = (" not in src, "toolkit 里不得另存一份校验规则"


# ----------------------------------------------------------------------------- DEC-34 MCP 写入

def test_mcp_upsert_rejects_dead_end_without_rule_and_writes_nothing(mcp, db_path):
    out = mcp.upsert_registry_empirical(
        region="KOR", layer="dead_end", entry_id="KOR-NORULE-DEAD",
        payload={"family": "f", "reason": "r"})
    assert "error" in out and "rule" in out["error"]
    assert _reg_rows(db_path) == []


def test_mcp_upsert_fills_id_from_entry_id_and_defaults(mcp, db_path):
    out = mcp.upsert_registry_empirical(
        region="KOR", layer="dead_end", entry_id="KOR-A-DEAD",
        payload={"family": "fam", "reason": "r", "rule": "u"})
    assert out["action"] == "inserted"
    (entry_id, family, payload, dead_at), = _reg_rows(db_path)
    p = json.loads(payload)
    assert entry_id == "KOR-A-DEAD" and p["id"] == "KOR-A-DEAD"
    assert family == "fam" and dead_at and p["dead_at"] == dead_at
    again = mcp.upsert_registry_empirical(
        region="KOR", layer="dead_end", entry_id="KOR-A-DEAD",
        payload={"family": "fam", "reason": "r2", "rule": "u"})
    assert again["action"] == "updated" and len(_reg_rows(db_path)) == 1


def test_mcp_upsert_entry_id_must_match_payload_id(mcp, db_path):
    out = mcp.upsert_registry_empirical(
        region="KOR", layer="win", entry_id="KOR-W1",
        payload={"id": "KOR-W2", "what": "w", "key": "k"})
    assert "error" in out and "不一致" in out["error"]
    assert _reg_rows(db_path, layer="win") == []


def test_mcp_upsert_campaign_uses_dataset_as_entry_id(mcp, db_path):
    out = mcp.upsert_registry_empirical(
        region="KOR", layer="campaign", entry_id="model219", payload={"status": "in_progress"})
    assert out["action"] == "inserted"
    (entry_id, family, _payload, _), = _reg_rows(db_path, layer="campaign")
    assert entry_id == "model219" and family == "model219"


def test_mcp_cross_region_layer_is_not_validated(mcp, db_path):
    out = mcp.upsert_registry_empirical(
        region="GLB", layer="cross_region", entry_id="L1", payload={"whatever": True})
    assert out["action"] == "inserted"


def test_cli_and_mcp_write_the_same_shape(mcp, db_path, monkeypatch):
    monkeypatch.setenv("WQB_WORKSPACE", str(REPO))
    from _lib.registry import RegistryStore
    RegistryStore("KOR", db_path=str(db_path)).upsert(
        "dead_end", {"id": "KOR-CLI-DEAD", "family": "f", "reason": "r", "rule": "u"})
    mcp.upsert_registry_empirical(
        region="KOR", layer="dead_end", entry_id="KOR-MCP-DEAD",
        payload={"family": "f", "reason": "r", "rule": "u"})
    shapes = {eid: sorted(json.loads(p)) for eid, _f, p, _d in _reg_rows(db_path)}
    assert shapes["KOR-CLI-DEAD"] == shapes["KOR-MCP-DEAD"]


# ----------------------------------------------------------------------------- DEC-34 seal_dead_end

def test_seal_dead_end_new_entry_needs_rule_and_has_no_side_effects(mcp, db_path):
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-NEW-DEAD", family="f", reason="r", wave_numbers=[1, 2])
    assert out["status"] == "error" and "rule" in out["error"]
    assert _reg_rows(db_path) == []
    conn = sqlite3.connect(str(db_path))
    try:
        n = conn.execute("SELECT COUNT(*) FROM ledger_kv WHERE key='salvage_pool'").fetchone()[0]
    finally:
        conn.close()
    assert n == 0, "校验失败不得沉降残值"


def test_seal_dead_end_with_rule_writes_full_shape_and_keeps_rule_on_reseal(mcp, db_path):
    # 2026-09-30：判死前取证闸（fail-closed）——正路：forum_recon 已把可靠的负结果落 ledger，封存时带上 question_key
    mcp._upsert_ledger_raw("KOR", "forum_recon_negative_0123456789", {"found": False, "status": "no_result",
                                                                      "question_key": "0123456789"})
    ok = mcp.seal_dead_end(region="KOR", entry_id="KOR-NEW-DEAD", family="f", reason="r",
                           rule="该族不再扩变体", forum_recon={"question_key": "0123456789", "found": False})
    assert ok["status"] == "success" and ok["action"] == "inserted"
    assert ok["forum_recon_gate"]["decision"] == "verified" and ok["forced"] is False
    (_e, family, payload, dead_at), = _reg_rows(db_path)
    p = json.loads(payload)
    assert p["id"] == "KOR-NEW-DEAD" and p["rule"] == "该族不再扩变体" and family == "f" and dead_at
    assert "salvage" in p
    again = mcp.seal_dead_end(region="KOR", entry_id="KOR-NEW-DEAD", reason="r2")   # 不再给 rule / family
    assert again["status"] == "success" and again["action"] == "updated"
    p2 = json.loads(_reg_rows(db_path)[0][2])
    assert p2["rule"] == "该族不再扩变体" and p2["reason"] == "r2"


# ----------------------------------------------------------------------------- DEC-33 submit_ready

def _queue_row(db_path, alpha_id, status, region="KOR"):
    from wqb.store import submit_queue as sq
    con = sq.connect(str(db_path))
    try:
        sq.ensure_table(con)
        con.execute("INSERT INTO submit_ready (alpha_id, region, expr, status, sharpe, fitness, added_at) "
                    "VALUES (?,?,?,?,?,?,?)", (alpha_id, region, "rank(x)", status, 1.7, 1.2, "2026-09-29"))
        con.commit()
    finally:
        con.close()


def test_get_submit_ready_reads_the_sql_queue_not_the_ledger_key(mcp, db_path):
    mcp.upsert_ledger_key(region="KOR", key="submit_ready", value=[{"id": "LEDGERONLY", "note": "audit"}])
    _queue_row(db_path, "QUEUED1", "READY")
    _queue_row(db_path, "GONE1", "SUBMITTED")
    _queue_row(db_path, "DEAD1", "DEAD")
    _queue_row(db_path, "OTHER", "READY", region="USA")
    ready = mcp.get_submit_ready("KOR")
    assert [r["alpha_id"] for r in ready] == ["QUEUED1"]              # 缺省只回 READY、只回本区、不含 ledger 键里的
    assert [r["alpha_id"] for r in mcp.get_submit_ready("KOR", status="submitted")] == ["GONE1"]
    assert {r["alpha_id"] for r in mcp.get_submit_ready("KOR", status="ALL")} == {"QUEUED1", "GONE1", "DEAD1"}
    assert mcp.get_submit_ready("KOR", status="NOPE")[0]["error"].startswith("invalid status")
    assert len(mcp.get_submit_ready("KOR", status="ALL", limit=1)) == 1


def test_ledger_catalog_marks_submit_ready_key_legacy():
    cat = json.loads((REPO / "docs" / "ledger_keys.json").read_text(encoding="utf-8"))["entries"]
    e = next(x for x in cat if x["key"] == "submit_ready")
    assert e["status"] == "legacy" and "SQL 表" in e["purpose"]
    assert not any("get_submit_ready" in (r.get("via") or "") for r in e["readers"])


# ----------------------------------------------------------------------------- DEC-35 多样性增强缺省

def test_diversity_enhancement_defaults_to_never_in_both_entry_points():
    bw = (TOOLKIT / "build_wave.py").read_text(encoding="utf-8")
    assert re.search(r'"--enhance-diversity",\s*default="never"', bw)
    bs = (REPO / "Claude" / "skills" / "brain-sim-alphas-in-batch-and-track" / "scripts"
          / "batch_simulator.py").read_text(encoding="utf-8")
    assert re.search(r'"--enhance-diversity",\s*default="never"', bs)
    assert 'enhance_diversity: str = "never"' in bs


# ----------------------------------------------------------------------------- DEC-36 废止提示与 --force

def _campaign(tmp_path, monkeypatch):
    camp = tmp_path / "ws" / "tracking" / "TST"
    (camp / "config").mkdir(parents=True)
    (camp / "config" / "settings.json").write_text(json.dumps({"region": "TST"}), encoding="utf-8")
    (camp / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    (tmp_path / "ws" / "src" / "wqb").mkdir(parents=True)
    db = tmp_path / "ws" / "data" / "wqb.db"
    db.parent.mkdir(parents=True)
    CampaignStore(str(db)).close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))
    return camp


def test_ledger_set_verdict_and_submit_ready_print_deprecation_notices(tmp_path, monkeypatch, capsys):
    from _lib.common import CampaignContext
    from _lib.ledger import cli_main
    ctx = CampaignContext(str(_campaign(tmp_path, monkeypatch)))
    assert cli_main(ctx, ["set-verdict", "5", "--json", json.dumps({"result": "FAIL"})]) == 0
    err = capsys.readouterr().err
    assert "废止" in err and "wave upsert" in err
    assert cli_main(ctx, ["submit-ready", "ABC123"]) == 0
    err = capsys.readouterr().err
    assert "legacy" in err and "不是提交队列" in err


def test_pipeline_force_help_states_what_it_bypasses():
    src = (TOOLKIT / "pipeline.py").read_text(encoding="utf-8")
    m = re.search(r'add_argument\("--force".*?\)\n', src, re.S)
    assert m and "submit_quota.enabled" in m.group(0) and "不提交 alpha" in m.group(0)


def test_quota_gate_is_off_by_default():
    import pipeline

    class _Ctx:
        @staticmethod
        def thresh(_key, default=None):
            return default
    q = pipeline.quota_cfg(_Ctx())
    assert q["enabled"] is False and q["limit"] == 4
