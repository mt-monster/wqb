# -*- coding: utf-8 -*-
"""`seal_dead_end` 的前置取证闸（fail-closed，2026-09-30）守护。

判死是永久封存一条路。2026-09-29 实证：5 条 recon 记录里 2 条是工具故障，旧代码把它们记成 found=false，
等于「工具坏了 ≡ 论坛无解」→ 误把活路判死。闸的契约：
  * 只有**可靠的**「论坛无解」放行——声明 found=false，且按 question_key 回 ledger 能找到可靠的负结果，且没有更新的「有货」推翻它；
  * 有货 / 故障 / 缺失 / 无法核对一律拒绝，**且没有任何副作用**（不沉降、不写库）；
  * 绕过只有两条（force_seal / require_forum_recon=False），都留痕在 payload.forum_recon_gate。
"""
import importlib
import inspect
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import recon_evidence as RE  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402

QK = "0123456789"
SEAL = dict(region="KOR", entry_id="KOR-GATE-DEAD", family="慢基本面族", reason="3 波 sharpe<1.0", rule="该族不再扩变体")


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    return path


@pytest.fixture
def mcp(db_path, monkeypatch):
    sys.modules.pop("wqb_db_mcp", None)
    mod = importlib.import_module("wqb_db_mcp")
    monkeypatch.setattr(mod, "DB_PATH", db_path)
    return mod


def _neg(mcp, region="KOR", qkey=QK, **kw):
    mcp._upsert_ledger_raw(region, RE.key_negative(qkey), dict({"found": False, "status": "no_result", "question_key": qkey,
                                                                 "searched_at": "2026-09-30T00:00:00"}, **kw))


def _found(mcp, region="KOR", qkey=QK, **kw):
    mcp._upsert_ledger_raw(region, RE.key_found(qkey), dict({"found": True, "status": "ok", "question_key": qkey,
                                                              "searched_at": "2026-09-30T00:00:00"}, **kw))


def _err(mcp, region="KOR", qkey=QK, **kw):
    mcp._upsert_ledger_raw(region, RE.key_error(qkey), dict({"found": None, "status": "error", "question_key": qkey,
                                                              "error": "auth", "searched_at": "2026-09-30T00:00:00"}, **kw))


def _registry(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute("SELECT entry_id, payload FROM registry_empirical WHERE layer='dead_end'").fetchall()
    finally:
        conn.close()


def _ledger_keys(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        return {r[0] for r in conn.execute("SELECT key FROM ledger_kv").fetchall()}
    finally:
        conn.close()


def _assert_refused_without_side_effects(out, db_path, code, before_keys):
    assert out["status"] == "error" and out["gate"] == "forum_recon" and out["code"] == code, out
    assert "force_seal" in out["error"] and "require_forum_recon" in out["error"]       # 告诉调用方绕过口在哪、且需人工确认
    assert _registry(db_path) == []                                                     # 没写库
    assert _ledger_keys(db_path) == before_keys                                         # 没沉降（salvage_pool 键不产生）


# ----------------------------------------------------------------------------- 签名
def test_the_gate_is_fail_closed_by_default(mcp):
    sig = inspect.signature(mcp.seal_dead_end)
    assert sig.parameters["require_forum_recon"].default is True                        # 缺省要取证
    assert sig.parameters["force_seal"].default is False and sig.parameters["forum_recon"].default is None


# ----------------------------------------------------------------------------- 放行
def test_a_reliable_no_result_recorded_in_the_ledger_lets_the_seal_through(mcp, db_path):
    _neg(mcp, question="KOR 慢基本面族 有无解法")
    out = mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False, "status": "no_result"})
    assert out["status"] == "success" and out["forced"] is False
    gate = out["forum_recon_gate"]
    assert gate["decision"] == "verified" and gate["question_key"] == QK
    assert gate["question"] == "KOR 慢基本面族 有无解法"                                   # 留痕：判死依据的是哪个问题（相关性由人看，闸不判）
    assert gate["ledger_key"] == RE.key_negative(QK) and gate["ledger_region"] == "KOR" and gate["searched_at"] == "2026-09-30T00:00:00"
    (eid, payload), = _registry(db_path)
    p = json.loads(payload)
    assert eid == "KOR-GATE-DEAD" and p["forum_recon_gate"]["decision"] == "verified"
    assert p["forum_recon"] == {"question_key": QK, "found": False, "status": "no_result"}          # 判死时依据的证据随条目留存


def test_only_whitelisted_evidence_fields_are_persisted(mcp, db_path):
    _neg(mcp)
    mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False, "articles": ["x"] * 100, "evil": {"a": 1}})
    p = json.loads(_registry(db_path)[0][1])
    assert set(p["forum_recon"]) == {"question_key", "found"}


def test_a_negative_recorded_under_global_counts_for_any_region(mcp):
    _neg(mcp, region="GLOBAL")                            # tools/forum_recon.py 缺 region 语境时落 GLOBAL
    out = mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False})
    assert out["status"] == "success" and out["forum_recon_gate"]["ledger_region"] == "GLOBAL"


def test_a_newer_reliable_negative_beats_an_older_hit(mcp):
    _found(mcp, searched_at="2026-09-01T00:00:00")
    _neg(mcp, searched_at="2026-09-20T00:00:00")
    out = mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False})
    assert out["status"] == "success"


def test_evidence_already_on_the_entry_is_used_when_no_argument_is_given(mcp):
    _neg(mcp)
    mcp.upsert_registry_empirical(region="KOR", layer="dead_end", entry_id="KOR-GATE-DEAD", family="慢基本面族",
                                  payload={"id": "KOR-GATE-DEAD", "family": "慢基本面族", "reason": "r", "rule": "u",
                                           "forum_recon": {"question_key": QK, "found": False}})
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-GATE-DEAD")
    assert out["status"] == "success" and out["forum_recon_gate"]["decision"] == "verified"


# ----------------------------------------------------------------------------- 拒绝（每一种都不产生副作用）
def test_missing_evidence_is_refused(mcp, db_path):
    before = _ledger_keys(db_path)
    out = mcp.seal_dead_end(**SEAL, wave_numbers=[1, 2])
    _assert_refused_without_side_effects(out, db_path, RE.CODE_MISSING, before)
    assert "forum_recon.py" in out["error"]


@pytest.mark.parametrize("evidence,code,setup", [
    ({"question_key": QK, "found": True, "status": "ok"}, RE.CODE_FOUND, None),                       # 声明有货：转武器，不得判死
    ({"question_key": QK, "found": None, "status": "error"}, RE.CODE_ERROR, None),                    # 故障 ≠ 无解
    ({"question_key": QK, "found": False, "error": "forum auth failed: TypeError"}, RE.CODE_ERROR, None),   # 旧版把鉴权失败记成 found=false + error
    ({"question_key": QK}, RE.CODE_UNKNOWN, None),
    ({"found": False}, RE.CODE_NO_KEY, None),                                                         # 无法追溯
    ("found=false", RE.CODE_NOT_A_RECORD, None),
    ({"question_key": QK, "found": False}, RE.CODE_NOT_IN_LEDGER, None),                              # 声明能编：ledger 里没有这条
    ({"question_key": QK, "found": False}, RE.CODE_LEDGER_FOUND, "found"),                            # ledger 里其实有货
    ({"question_key": QK, "found": False}, RE.CODE_LEDGER_ERROR, "error"),                            # ledger 里只有故障记录
    ({"question_key": QK, "found": False}, RE.CODE_LEDGER_ERROR, "legacy"),                           # 旧库遗留的「found=false + error」假负结果
])
def test_everything_but_a_reliable_no_result_is_refused_without_side_effects(mcp, db_path, evidence, code, setup):
    if setup == "found":
        _found(mcp)
    elif setup == "error":
        _err(mcp)
    elif setup == "legacy":
        mcp._upsert_ledger_raw("KOR", RE.key_negative(QK), {"found": False, "error": "forum auth failed: TypeError",
                                                             "searched_at": "2026-09-29T00:00:00"})
    before = _ledger_keys(db_path)
    out = mcp.seal_dead_end(**SEAL, wave_numbers=[1, 2], forum_recon=evidence)
    _assert_refused_without_side_effects(out, db_path, code, before)


def test_a_newer_hit_overrules_an_older_negative(mcp, db_path):
    _neg(mcp, searched_at="2026-09-01T00:00:00")
    _found(mcp, searched_at="2026-09-20T00:00:00")                    # 论坛后来有解了：不能拿旧的无解判死
    before = _ledger_keys(db_path)
    out = mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False})
    _assert_refused_without_side_effects(out, db_path, RE.CODE_LEDGER_FOUND, before)


def test_contract_errors_still_come_first_and_the_message_is_unchanged(mcp, db_path):
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-NEW-DEAD", family="f", reason="r", wave_numbers=[1, 2])
    assert out["status"] == "error" and "rule" in out["error"] and "gate" not in out            # 缺 rule：先报契约错误
    assert _registry(db_path) == []


# ----------------------------------------------------------------------------- 绕过（人工确认 + 留痕）
def test_force_seal_lets_a_refused_seal_through_and_leaves_the_overridden_code(mcp, db_path):
    out = mcp.seal_dead_end(**SEAL, force_seal=True)                    # 缺证据
    assert out["status"] == "success" and out["forced"] is True
    gate = out["forum_recon_gate"]
    assert gate["decision"] == "forced" and gate["overridden_code"] == RE.CODE_MISSING and gate["overridden_message"]
    assert json.loads(_registry(db_path)[0][1])["forum_recon_gate"]["decision"] == "forced"      # 留痕在条目里


def test_force_seal_over_a_contradicting_hit_still_records_what_it_overrode(mcp):
    _found(mcp)
    out = mcp.seal_dead_end(**SEAL, force_seal=True, forum_recon={"question_key": QK, "found": False})
    assert out["forced"] is True and out["forum_recon_gate"]["overridden_code"] == RE.CODE_LEDGER_FOUND


def test_force_seal_is_not_recorded_as_forced_when_the_evidence_already_holds(mcp):
    _neg(mcp)
    out = mcp.seal_dead_end(**SEAL, force_seal=True, forum_recon={"question_key": QK, "found": False})
    assert out["forced"] is False and out["forum_recon_gate"]["decision"] == "verified"


def test_require_forum_recon_false_waives_the_gate_and_says_so(mcp, db_path):
    out = mcp.seal_dead_end(**SEAL, require_forum_recon=False)
    assert out["status"] == "success" and out["forced"] is False
    assert out["forum_recon_gate"]["decision"] == "waived"
    assert json.loads(_registry(db_path)[0][1])["forum_recon_gate"]["decision"] == "waived"


# ----------------------------------------------------------------------------- 重复封存
@pytest.mark.parametrize("how", ["verified", "forced", "waived"])
def test_resealing_reuses_the_earlier_gate_decision_without_new_evidence(mcp, db_path, how):
    if how == "verified":
        _neg(mcp)
        first = mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False})
    elif how == "forced":
        first = mcp.seal_dead_end(**SEAL, force_seal=True)
    else:
        first = mcp.seal_dead_end(**SEAL, require_forum_recon=False)
    assert first["status"] == "success"
    again = mcp.seal_dead_end(region="KOR", entry_id="KOR-GATE-DEAD", reason="补一条理由")           # 补数据 / 补沉降范围，不再要证据
    assert again["status"] == "success" and again["action"] == "updated" and again["forum_recon_gate"]["decision"] == how


def test_an_entry_sealed_before_the_gate_existed_needs_evidence_to_be_resealed(mcp, db_path):
    mcp.upsert_registry_empirical(region="KOR", layer="dead_end", entry_id="KOR-LEGACY-DEAD", family="f",
                                  payload={"id": "KOR-LEGACY-DEAD", "family": "f", "reason": "r", "rule": "u"})
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-LEGACY-DEAD", reason="补一条")
    assert out["status"] == "error" and out["code"] == RE.CODE_MISSING


def test_new_evidence_on_a_reseal_is_verified_again(mcp):
    _neg(mcp)
    mcp.seal_dead_end(**SEAL, forum_recon={"question_key": QK, "found": False})
    _found(mcp, searched_at="2026-10-05T00:00:00")                                                   # 封存之后论坛有解了
    out = mcp.seal_dead_end(region="KOR", entry_id="KOR-GATE-DEAD", forum_recon={"question_key": QK, "found": False})
    assert out["status"] == "error" and out["code"] == RE.CODE_LEDGER_FOUND                          # 带了新声明就重新核对，不再沿用旧结论


# ----------------------------------------------------------------------------- 上游写入方与闸对同一条记录的理解一致
def test_the_recon_tool_and_the_gate_agree_on_what_a_reliable_negative_is(mcp, tmp_path, monkeypatch):
    """闸放行的记录 = `tools/forum_recon.py` 真正落下的负结果（不是测试手写的形状）。"""
    import forum_recon as fr
    monkeypatch.setattr(fr, "RECON_CACHE", str(tmp_path / "recon_cache.json"))
    monkeypatch.setattr(fr, "_load_ghost_names", lambda db: [])
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    monkeypatch.setattr(fr, "_control_probe", lambda s, f: None)

    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        stats["searches_ok"] = stats.get("searches_ok", 0) + 1                                        # 检索成功、没有有效文章
        return []
    monkeypatch.setattr(fr, "live_search_round", _round)
    out = fr.recon("KOR 慢基本面族 有无解法", {"region": "KOR"}, "negative", 1, 2, "a", False, str(mcp.DB_PATH))
    assert out["found"] is False and out["status"] == "no_result"
    sealed = mcp.seal_dead_end(**SEAL, forum_recon={"question_key": out["question_key"], "found": out["found"], "status": out["status"]})
    assert sealed["status"] == "success" and sealed["forum_recon_gate"]["ledger_key"] == RE.key_negative(out["question_key"])
    # 同一个问题的工具故障：写 forum_recon_error_*，闸不认
    fake_q = "KOR 另一族 有无解法"
    monkeypatch.setattr(fr, "_live_session", lambda: (_ for _ in ()).throw(fr.ReconToolError("auth_failed", "鉴权失败")))
    bad = fr.recon(fake_q, {"region": "KOR"}, "negative", 1, 2, "a", False, str(mcp.DB_PATH))
    assert bad["found"] is None
    refused = mcp.seal_dead_end(region="KOR", entry_id="KOR-OTHER-DEAD", family="f", reason="r", rule="u",
                                forum_recon={"question_key": bad["question_key"], "found": False})
    assert refused["status"] == "error" and refused["code"] == RE.CODE_LEDGER_ERROR
