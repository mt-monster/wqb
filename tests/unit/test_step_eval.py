# -*- coding: utf-8 -*-
"""步级评估 v2（2026-09-30 方案 B）契约测试。

锁定设计红线（对应 attic/step_metrics_20260917/README.md 复活前提）：
- R1 事件可审计：event_type 封闭词表、source 必填、拒收 NaN/评估结论式数值；
- R2 评分单点：所有分数经 wqb.step_scoring，且契约 = 比率∈[0,1] 或 None；
- R3 无反事实入库：事件只有"发生/次数"语义；
- R5 边界安全：0 分母 → None（不报 0、不除零）；
- 只读性：step_funnel --full 跑完 DB 字节不变（沿用 hash 断言模式）；
- 守护兼容：旧 7 文件名仍不存在（test_step_funnel_p5 的下线终态不被推翻）。
"""
import hashlib
import json
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.step_events import (  # noqa: E402
    EVENT_VOCAB, record_event, safe_record_event, query_events, aggregate_conn,
)
from wqb.step_scoring import (  # noqa: E402
    safe_ratio, safe_rate, score_metrics, compute_scores,
)
from wqb.step_eval import build_step_eval  # noqa: E402
import step_funnel  # noqa: E402


# ------------------------------------------------------------------ fixtures

def _mkdb(tmp_path, with_tables=("expressions", "gate_results", "backtest_results",
                                 "wave_results", "ledger_kv", "fields")):
    db = tmp_path / "eval.db"
    conn = sqlite3.connect(str(db))
    if "expressions" in with_tables:
        conn.execute("""CREATE TABLE expressions(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, status TEXT,
            expected_exposure TEXT, created_at TEXT, updated_at TEXT)""")
    if "gate_results" in with_tables:
        conn.execute("""CREATE TABLE gate_results(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, dataset TEXT,
            all_pass INTEGER, report_json TEXT, created_at TEXT, updated_at TEXT)""")
    if "backtest_results" in with_tables:
        conn.execute("""CREATE TABLE backtest_results(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, status TEXT,
            sharpe REAL, fitness REAL, created_at TEXT)""")
    if "wave_results" in with_tables:
        conn.execute("""CREATE TABLE wave_results(
            id INTEGER PRIMARY KEY, region TEXT, wave_number TEXT, verdict TEXT,
            created_at TEXT, updated_at TEXT)""")
    if "ledger_kv" in with_tables:
        conn.execute("""CREATE TABLE ledger_kv(
            id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT,
            created_at TEXT, updated_at TEXT)""")
    if "fields" in with_tables:
        conn.execute("""CREATE TABLE fields(
            id INTEGER PRIMARY KEY, dataset_id TEXT, field_name TEXT,
            user_count INTEGER, coverage REAL, created_at TEXT)""")
    conn.commit()
    return db, conn


def _seed(conn, region="TEST"):
    # 白名单 4 集：1 个判死交集 + 非 model 前缀 3 个（金字塔配额合规）
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value,created_at,updated_at) VALUES (?,?,?,?,?)",
        (region, "s0_whitelist",
         json.dumps({"datasets": ["news1", "anl2", "pv3", "model9"]}),
         "2026-09-01T00:00:00", "2026-09-02T00:00:00"))
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
        (region, "news1_dead", json.dumps({"reason": "x"})))
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
        (region, "submit_ready", json.dumps([{"id": "a"}, {"id": "b"}])))
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
        (region, "submit_ready_blocked", json.dumps([{"id": "c"}])))
    # fields：news1 有 10 个字段（过闸），其中 6 个冷门（user_count<=9）
    for i in range(10):
        conn.execute(
            "INSERT INTO fields(dataset_id,field_name,user_count,coverage,created_at)"
            " VALUES (?,?,?,?,?)",
            ("news1", f"f{i}", 3 if i < 6 else 80, 0.9, "2026-09-01T00:00:00"))
    conn.execute(
        "INSERT INTO fields(dataset_id,field_name,user_count,coverage,created_at)"
        " VALUES (?,?,?,?,?)", ("anl2", "g0", 80, 0.9, "2026-09-01T00:00:00"))
    # expressions：5 条，2 条声明 exposure，2 条未消化（gem+pending）
    conn.executemany(
        "INSERT INTO expressions(region,wave,status,expected_exposure,created_at)"
        " VALUES (?,?,?,?,?)",
        [(region, "w1", "backtested", "EV", "2026-09-01T00:00:00"),
         (region, "w1", "backtested", None, "2026-09-01T00:00:00"),
         (region, "w1", "backtested", "EV", "2026-09-01T00:00:00"),
         (region, "w1", "gem", None, "2026-09-01T00:00:00"),
         (region, "w1", "pending", None, "2026-09-01T00:00:00")])
    conn.execute(
        "INSERT INTO gate_results(region,wave,dataset,all_pass,report_json,created_at)"
        " VALUES (?,?,?,?,?,?)",
        (region, "w1", "news1", 1, json.dumps({"total": 5, "passed": 3}),
         "2026-09-01T01:00:00"))
    # backtest：4 行，3 COMPLETE 1 ERROR；2 条过廉价闸
    conn.executemany(
        "INSERT INTO backtest_results(region,wave,status,sharpe,fitness,created_at)"
        " VALUES (?,?,?,?,?,?)",
        [(region, "w1", "COMPLETE", 1.9, 1.2, "2026-09-03T00:00:00"),
         (region, "w1", "COMPLETE", 1.7, 1.1, "2026-09-03T01:00:00"),
         (region, "w1", "COMPLETE", 1.2, 0.8, "2026-09-03T02:00:00"),
         (region, "w1", "ERROR", None, None, "2026-09-03T03:00:00")])
    # wave_results：2 波，1 波 verdict 非空
    conn.executemany(
        "INSERT INTO wave_results(region,wave_number,verdict,created_at,updated_at)"
        " VALUES (?,?,?,?,?)",
        [(region, "w1", "PASS", "2026-09-01T00:00:00", "2026-09-04T00:00:00"),
         (region, "w2", None, "2026-09-02T00:00:00", "2026-09-05T00:00:00")])
    conn.commit()


# ------------------------------------------------------------------ R1 事件台账

def test_event_vocab_rejects_unknown_type(tmp_path):
    db, conn = _mkdb(tmp_path, with_tables=())
    conn.close()
    with pytest.raises(ValueError, match="封闭词表"):
        record_event("TEST", "S0", "accuracy_is_085", source="x::y", db_path=str(db))


def test_event_source_required(tmp_path):
    db, conn = _mkdb(tmp_path, with_tables=())
    conn.close()
    with pytest.raises(ValueError, match="source"):
        record_event("TEST", "S0", "cache_hit", source="", db_path=str(db))


def test_event_rejects_nan_and_inf(tmp_path):
    db, conn = _mkdb(tmp_path, with_tables=())
    conn.close()
    with pytest.raises(ValueError):
        record_event("TEST", "S0", "cache_hit", source="x::y", value=float("nan"),
                     db_path=str(db))
    with pytest.raises(ValueError):
        record_event("TEST", "S0", "cache_hit", source="x::y", value=float("inf"),
                     db_path=str(db))


def test_event_dedupe_key_is_idempotent(tmp_path):
    db, conn = _mkdb(tmp_path, with_tables=())
    conn.close()
    kw = dict(region="TEST", step="S0", event_type="cache_hit", source="x::y",
              dedupe_key="k1", db_path=str(db))
    r1 = record_event(**kw)
    r2 = record_event(**kw)
    assert r1["recorded"] is True
    assert r2["recorded"] is False and r2["reason"] == "duplicate"
    rows = query_events(region="TEST", db_path=str(db))
    assert len(rows) == 1


def test_safe_record_event_never_raises(tmp_path):
    db, conn = _mkdb(tmp_path, with_tables=())
    conn.close()
    # 词表违规也被吞掉（旁路绝不打断主流程）
    r = safe_record_event("TEST", "S0", "not_in_vocab", source="x::y", db_path=str(db))
    assert r["recorded"] is False and str(r["reason"]).startswith("suppressed:")


def test_query_events_missing_table_returns_empty(tmp_path):
    db, conn = _mkdb(tmp_path, with_tables=())
    conn.close()
    assert query_events(region="TEST", db_path=str(db)) == []


# ------------------------------------------------------------------ R2/R5 评分单点

def test_safe_ratio_zero_denominator_is_none_not_zero():
    assert safe_ratio(0, 0) is None
    assert safe_ratio(5, 0) is None
    assert safe_ratio(None, 3) is None
    assert safe_rate(3, 6) == 0.5


def test_score_metrics_skips_ineligible_and_none():
    ms = [{"value": 0.8, "score_eligible": True},
          {"value": 99.0, "score_eligible": False},   # 原始量不参与
          {"value": None, "score_eligible": True},    # 未知不参与
          {"value": 0.6, "score_eligible": True}]
    assert score_metrics(ms) == pytest.approx(0.7)
    assert score_metrics([]) is None
    assert score_metrics([{"value": None, "score_eligible": True}]) is None


def test_compute_scores_contract_ranges():
    """契约：Q/E/G/ROI ∈ [0,1] 或 None；unit_cost ≥1 或 None；0/0 → None 不除零。"""
    matrix = {"S0": {"quality": [{"value": 0.5, "score_eligible": True}],
                     "efficiency": [], "gain": []}}
    s = compute_scores(matrix, {"backtested": 0, "cheap_pass": 0})
    assert s["roi"] is None and s["unit_cost"] is None       # 0/0 边界
    s = compute_scores(matrix, {"backtested": 10, "cheap_pass": 2})
    assert s["roi"] == pytest.approx(0.2) and s["unit_cost"] == pytest.approx(5.0)
    assert s["quality"] == pytest.approx(0.5)
    assert s["efficiency"] is None and s["gain"] is None     # 无指标 → None 非 0
    s = compute_scores(matrix, {"backtested": None, "cheap_pass": None})
    assert s["roi"] is None
    # 上游口径漂移时夹取（防 13.33 超界类事故）
    bad = {"S0": {"quality": [{"value": 13.33, "score_eligible": True}],
                  "efficiency": [], "gain": []}}
    assert compute_scores(bad)["quality"] == pytest.approx(1.0)


# ------------------------------------------------------------------ step_eval 只读推导

def test_step_eval_empty_db_structure_and_no_guessing(tmp_path):
    _db, conn = _mkdb(tmp_path, with_tables=())
    res = build_step_eval(conn, "NOPE")
    conn.close()
    assert set(res["steps"]) == {"S-PRE", "S0", "S1", "S2", "S2->S3", "S3",
                                 "S4", "S4->S5", "S6"}
    # 缺表 → 指标条目仍在但 value=None（未知，不报 0）
    for dims in res["steps"].values():
        for m in (dims["quality"] + dims["efficiency"] + dims["gain"]):
            if m["value"] is not None:
                pytest.fail(f"空库不应有值：{m}")
    assert res["scores"]["quality"] is None
    assert res["scores"]["roi"] is None


def test_step_eval_seeded_values(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _seed(conn)
    res = build_step_eval(conn, "TEST")
    conn.close()
    st = res["steps"]
    by = lambda s, d, n: next(m for m in st[s][d] if m["name"] == n)["value"]
    # S-PRE：白名单 4 集 ∩ dead{news1} = 1 → compliance = 3/4
    assert by("S-PRE", "quality", "dead_path_compliance") == pytest.approx(0.75)
    # S0：非 model 前缀 3 个 ≥2 → 1.0
    assert by("S0", "quality", "pyramid_quota_compliance") == 1.0
    # S1：news1 10 字段过闸、anl2 1 字段不过 → 1/2（model9/pv3 无 fields 记录）
    assert by("S1", "quality", "field_gate_rate") == pytest.approx(0.25)
    # S1 冷门字段：6/11
    assert by("S1", "gain", "cold_field_ratio") == pytest.approx(6 / 11)
    # S2：声明率 2/5；消费效率 (5-2)/5
    assert by("S2", "quality", "concept_declare_rate") == pytest.approx(0.4)
    assert by("S2", "efficiency", "consumption_efficiency") == pytest.approx(0.6)
    # S2->S3：表达式级通过率 3/5
    assert by("S2->S3", "quality", "expr_gate_pass_rate") == pytest.approx(0.6)
    # S3：完成率 3/4；非浪费 3/4
    assert by("S3", "quality", "complete_rate") == pytest.approx(0.75)
    assert by("S3", "efficiency", "non_waste_rate") == pytest.approx(0.75)
    # S4->S5：ready 2 / cheap_pass 2 = 1.0；blocked 补数 2/3
    assert by("S4->S5", "quality", "submit_ready_conversion") == pytest.approx(1.0)
    assert by("S4->S5", "efficiency", "blocked_complement") == pytest.approx(2 / 3)
    # S6：verdict 非空率 1/2
    assert by("S6", "quality", "verdict_nonempty_rate") == pytest.approx(0.5)
    # 评分契约
    sc = res["scores"]
    for k in ("quality", "efficiency", "gain", "roi"):
        assert sc[k] is None or 0.0 <= sc[k] <= 1.0, k
    assert sc["roi"] == pytest.approx(0.5)   # cheap 2 / backtested 4
    assert sc["unit_cost"] == pytest.approx(2.0)


def test_step_eval_consumes_t2_events(tmp_path):
    db, conn = _mkdb(tmp_path)
    _seed(conn)
    conn.close()
    record_event("TEST", "S0", "cache_hit", source="t::x", db_path=str(db))
    record_event("TEST", "S3", "batch_error_cascade", value=3, source="t::x",
                 db_path=str(db))
    conn = sqlite3.connect(str(db))
    res = build_step_eval(conn, "TEST")
    conn.close()
    st = res["steps"]
    cache = next(m for m in st["S0"]["gain"] if m["name"] == "cache_reuse_rate")
    assert cache["tier"] == "T2" and cache["value"] == 1.0   # 1 hit / (1+0)
    cascade = next(m for m in st["S3"]["gain"] if m["name"] == "batch_error_cascade")
    assert cascade["value"] == 3.0


# ------------------------------------------------------------------ 只读性与守护兼容

def test_full_mode_does_not_modify_db(tmp_path, monkeypatch, capsys):
    db, conn = _mkdb(tmp_path)
    _seed(conn)
    conn.close()
    before = hashlib.sha256(db.read_bytes()).hexdigest()
    monkeypatch.setattr(step_funnel, "resolve_db_path", lambda: str(db))
    monkeypatch.setattr(sys, "argv",
                        ["step_funnel.py", "--region", "TEST", "--full", "--format", "json"])
    assert step_funnel.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["region"] == "TEST"
    after = hashlib.sha256(db.read_bytes()).hexdigest()
    assert before == after, "--full 必须只读，DB 被改动了"


def test_full_mode_formats_render(tmp_path, monkeypatch, capsys):
    db, conn = _mkdb(tmp_path)
    _seed(conn)
    conn.close()
    monkeypatch.setattr(step_funnel, "resolve_db_path", lambda: str(db))
    for fmt, marker in (("markdown", "九步质量效能增益矩阵"),
                        ("html", "<html>")):
        monkeypatch.setattr(sys, "argv",
                            ["step_funnel.py", "--region", "TEST", "--full",
                             "--format", fmt])
        assert step_funnel.main() == 0
        assert marker in capsys.readouterr().out


def test_guard_locked_files_still_absent():
    """下线终态不被推翻：旧 7 文件名不得复活（新方案文件名刻意避开）。"""
    for gone in ("tools/step_metrics_collector.py", "tools/step_gain_reporter.py",
                 "tools/wave_summary_computer.py", "tools/campaign_summary_computer.py",
                 "tools/migrate_step_metrics.py",
                 "src/wqb/workflow/nodes/step_metrics.py",
                 "tests/unit/test_step_metrics.py"):
        assert not os.path.exists(os.path.join(REPO, gone)), f"旧名复活：{gone}"


def test_event_vocab_is_closed_and_documented():
    """词表条目必须有语义说明（R1 可审计）。"""
    assert all(isinstance(v, str) and v for v in EVENT_VOCAB.values())
    assert "cache_hit" in EVENT_VOCAB and "mode_b_blocked" in EVENT_VOCAB
