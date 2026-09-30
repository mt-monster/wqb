# -*- coding: utf-8 -*-
"""论坛取证证据契约（`src/wqb/recon_evidence.py`）守护——**故障 ≠ 无解**（2026-09-29 事故）。

契约的意义：写入方（tools/forum_recon.py、forum_recon_wave 节点）、判死闸（MCP seal_dead_end）、统计方（tools/step_funnel.py）
对「什么算无解」必须是同一个理解。旧版写入方把鉴权失败记成 found=false 落 forum_recon_negative_*，统计方按前缀数成「有货」，
判死方（人）把它当「论坛无解」——三处各懂各的。
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tools"))

from wqb import recon_evidence as RE  # noqa: E402


# ----------------------------------------------------------------------------- 键
def test_question_key_is_the_stable_sha1_prefix_and_ignores_outer_whitespace():
    q = "GLB model264 慢基本面强度墙有无破墙配方"
    assert RE.question_key(q) == hashlib.sha1(q.encode("utf-8")).hexdigest()[:10]
    assert RE.question_key("  " + q + "\n") == RE.question_key(q)
    assert len(RE.question_key(q)) == 10


def test_the_tool_uses_the_shared_question_key():
    import forum_recon as fr
    assert fr._qkey("同一个问题") == RE.question_key("同一个问题")


def test_key_builders_and_kinds_do_not_confuse_the_longer_prefixes():
    qk = RE.question_key("q")
    assert RE.key_found(qk) == f"forum_recon_{qk}"
    assert RE.key_negative(qk) == f"forum_recon_negative_{qk}"
    assert RE.key_error(qk) == f"forum_recon_error_{qk}"
    assert RE.key_wave(97) == "forum_recon_wave_97" and RE.key_wave("s2_ds_d1") == "forum_recon_wave_s2_ds_d1"
    assert RE.key_kind(RE.key_found(qk)) == "found"
    assert RE.key_kind(RE.key_negative(qk)) == "negative"
    assert RE.key_kind(RE.key_error(qk)) == "error"
    assert RE.key_kind(RE.key_wave(97)) == "wave"
    # 有货键的 qkey 恒为 10 位十六进制——别的 forum_recon_ 开头的键不是有货记录
    assert RE.key_kind("forum_recon_cache") is None and RE.key_kind("forum_recon_") is None
    assert RE.key_kind("prod_first_97") is None and RE.key_kind(None) is None


def test_summarize_keys_counts_kinds_and_ignores_foreign_keys():
    qk = [RE.question_key(x) for x in "abc"]
    keys = [RE.key_found(qk[0]), RE.key_negative(qk[1]), RE.key_error(qk[2]), RE.key_wave(1), "other_key"]
    assert RE.summarize_keys(keys) == {"found": 1, "negative": 1, "error": 1, "wave": 1}


# ----------------------------------------------------------------------------- 记录分类
@pytest.mark.parametrize("rec,kind", [
    ({"found": True, "status": "ok"}, "found"),
    ({"found": True}, "found"),
    ({"found": True, "search_errors": 1}, "found"),                         # 有货但中途失败过：仍是有货
    ({"found": False, "status": "no_result"}, "negative"),
    ({"found": False}, "negative"),                                          # 旧版的真负结果（没有 status）
    ({"found": None, "status": "error", "error": "x"}, "error"),
    ({"found": None}, "unknown"),
    ({"found": False, "error": "forum auth failed: TypeError"}, "error"),   # 旧版把鉴权失败记成 found=false + error
    ({"status": "error"}, "error"),
    ({}, "unknown"), (None, "unknown"), ("x", "unknown"), ([], "unknown"),
])
def test_classify_record(rec, kind):
    assert RE.classify_record(rec) == kind


def test_status_of():
    assert RE.status_of(True) == "ok" and RE.status_of(False) == "no_result" and RE.status_of(None) == "error"


# ----------------------------------------------------------------------------- 判死闸的纯判定
def _neg(**kw):
    return dict({"question_key": "abcdef0123", "found": False, "status": "no_result"}, **kw)


def test_only_a_reliable_negative_with_a_question_key_is_allowed():
    ok = RE.evaluate_forum_recon(_neg())
    assert ok["allowed"] is True and ok["code"] == RE.CODE_ALLOWED
    assert RE.evaluate_forum_recon({"question_key": "k", "found": False})["allowed"] is True        # 旧版真负结果（无 status）


@pytest.mark.parametrize("evidence,code", [
    (None, RE.CODE_MISSING),
    ({}, RE.CODE_MISSING),
    ("found=false", RE.CODE_NOT_A_RECORD),
    (_neg(found=True, status="ok"), RE.CODE_FOUND),                                   # 论坛有解：转武器，不得判死
    ({"question_key": "k", "found": None, "status": "error"}, RE.CODE_ERROR),        # 故障 ≠ 无解
    ({"question_key": "k", "found": False, "error": "forum auth failed"}, RE.CODE_ERROR),
    ({"question_key": "k", "status": "error"}, RE.CODE_ERROR),
    ({"question_key": "k"}, RE.CODE_UNKNOWN),                                        # 缺 found
    ({"found": False, "status": "no_result"}, RE.CODE_NO_KEY),                       # 无法追溯到 ledger 记录
    ({"found": False, "question_key": "  "}, RE.CODE_NO_KEY),
])
def test_everything_else_is_refused_with_a_specific_code(evidence, code):
    v = RE.evaluate_forum_recon(evidence)
    assert v["allowed"] is False and v["code"] == code and v["message"]


# ----------------------------------------------------------------------------- 按 qkey 找结局
def _store(records):
    def get(region, key):
        return records.get((region, key))
    return get


def test_a_reliable_outcome_beats_a_later_error():
    qk = "0123456789"
    get = _store({
        ("KOR", RE.key_negative(qk)): {"found": False, "status": "no_result", "searched_at": "2026-09-01T00:00:00"},
        ("KOR", RE.key_error(qk)): {"found": None, "status": "error", "searched_at": "2026-09-30T00:00:00"},
    })
    out = RE.resolve_outcome(get, "KOR", qk)
    assert out["kind"] == "negative" and out["key"] == RE.key_negative(qk)     # 之后的故障不撤销之前可靠的「无解」


def test_only_errors_resolve_to_error_and_nothing_resolves_to_none():
    qk = "0123456789"
    get = _store({("KOR", RE.key_error(qk)): {"found": None, "status": "error", "searched_at": "2026-09-30T00:00:00"}})
    assert RE.resolve_outcome(get, "KOR", qk)["kind"] == "error"
    assert RE.resolve_outcome(_store({}), "KOR", qk) is None


def test_freshest_reliable_record_wins_and_global_is_the_fallback_scope():
    qk = "0123456789"
    get = _store({
        ("KOR", RE.key_found(qk)): {"found": True, "searched_at": "2026-09-01T00:00:00"},
        ("KOR", RE.key_negative(qk)): {"found": False, "searched_at": "2026-09-20T00:00:00"},
    })
    assert RE.resolve_outcome(get, "KOR", qk)["kind"] == "negative"
    only_global = _store({("GLOBAL", RE.key_negative(qk)): {"found": False, "searched_at": "2026-09-20T00:00:00"}})
    out = RE.resolve_outcome(only_global, "KOR", qk)
    assert out["kind"] == "negative" and out["region"] == "GLOBAL"


def test_a_legacy_error_shaped_record_under_the_negative_key_is_not_reliable():
    qk = "0123456789"
    get = _store({("KOR", RE.key_negative(qk)): {"found": False, "error": "forum auth failed: TypeError",
                                                  "searched_at": "2026-09-29T00:00:00"}})
    out = RE.resolve_outcome(get, "KOR", qk)
    assert out["kind"] == "error"                                                  # 旧库里遗留的「故障 ≡ 无解」记录被识破


# ----------------------------------------------------------------------------- 统计方（step_funnel）不再把故障数成有货
def test_step_funnel_counts_only_reliable_outcomes_toward_the_hit_rate(tmp_path):
    import step_funnel
    db = tmp_path / "t.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY AUTOINCREMENT, region TEXT, key TEXT, value TEXT, "
                 "UNIQUE(region, key))")
    qk = [RE.question_key(x) for x in ("a", "b", "c", "d")]
    rows = [("KOR", RE.key_found(qk[0])), ("KOR", RE.key_found(qk[1])), ("KOR", RE.key_negative(qk[2])),
            ("GLOBAL", RE.key_error(qk[3])), ("KOR", RE.key_error(qk[0])), ("KOR", RE.key_wave(97))]
    conn.executemany("INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?)", [(r, k, "{}") for r, k in rows])
    conn.commit()
    res = step_funnel.build_funnel(conn, "KOR")
    conn.close()
    fr = res["steps"]["forum_recon"]
    assert (fr["n_found"], fr["n_negative"], fr["n_error"]) == (2, 1, 2)
    assert fr["n_recon"] == 3 and fr["hit_rate"] == round(2 / 3, 4)              # 故障与波标记不进分母
    assert "工具故障 2 次（不计入）" in step_funnel.render(res)                     # 报告里如实写出故障次数


# ----------------------------------------------------------------------------- 判死闸的完整判定（声明 + ledger 核对）
def _claim(qk="0123456789", **kw):
    return dict({"question_key": qk, "found": False, "status": "no_result"}, **kw)


def test_verify_evidence_allows_a_claim_the_ledger_backs_up_and_reports_the_trace():
    qk = "0123456789"
    get = _store({("KOR", RE.key_negative(qk)): {"found": False, "status": "no_result", "searched_at": "2026-09-30T01:02:03"}})
    v = RE.verify_evidence(_claim(qk), get, "KOR")
    assert v["allowed"] is True and v["code"] == RE.CODE_ALLOWED
    assert (v["question_key"], v["ledger_key"], v["ledger_region"], v["searched_at"]) == (
        qk, RE.key_negative(qk), "KOR", "2026-09-30T01:02:03")


@pytest.mark.parametrize("records,code", [
    ({}, RE.CODE_NOT_IN_LEDGER),                                                                          # 声明能编；ledger 是工具写的
    ({"found": {"found": True, "searched_at": "2026-09-30"}}, RE.CODE_LEDGER_FOUND),
    ({"error": {"found": None, "status": "error", "searched_at": "2026-09-30"}}, RE.CODE_LEDGER_ERROR),
    ({"negative": {"found": False, "error": "forum auth failed", "searched_at": "2026-09-29"}}, RE.CODE_LEDGER_ERROR),   # 旧版假负结果
    ({"negative": {"found": False, "searched_at": "2026-09-01"}, "found": {"found": True, "searched_at": "2026-09-02"}}, RE.CODE_LEDGER_FOUND),
])
def test_verify_evidence_refuses_what_the_ledger_does_not_back_up(records, code):
    qk = "0123456789"
    key_of = {"found": RE.key_found, "negative": RE.key_negative, "error": RE.key_error}
    get = _store({("KOR", key_of[k](qk)): v for k, v in records.items()})
    v = RE.verify_evidence(_claim(qk), get, "KOR")
    assert v["allowed"] is False and v["code"] == code and v["message"]


def test_verify_evidence_never_consults_the_ledger_for_a_claim_that_is_already_refused():
    def _boom(region, key):
        raise AssertionError("声明层就拒绝的，不该去查 ledger")
    for bad in (None, {}, "x", {"question_key": "k", "found": True}, {"question_key": "k", "found": None, "status": "error"},
                {"found": False}):
        assert RE.verify_evidence(bad, _boom, "KOR")["allowed"] is False
