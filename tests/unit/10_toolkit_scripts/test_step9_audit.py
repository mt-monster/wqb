# -*- coding: utf-8 -*-
"""回归测试：步 9（S6）完成定义只读校验器（2026-10-02 新增）。

## 背景
`step9-writeback.md §9.7` 声明「缺任何一项 = 本波未完成」，但此前**无任何代码强制**
（GEM 对 stale 先验快照只 WARN），导致 GBR 快照静默落后 8 天。本测试锁定新校验器：

1. 六项判据的正确性（§9.7 一一对应）；
2. **软/硬判据分级**（wave_row/priors_snapshot 硬；其余软，strict 才算失败）；
3. **NULL/缺失不判失败**（unknown ≠ fail，与预筛口径一致）；
4. **只读性**——跑完 DB 文件字节不变（本工具的核心承诺）。
"""

import hashlib
import json
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

import step9_audit  # noqa: E402


def _mkdb(tmp_path, *, tables=("wave_results", "registry_empirical", "ledger_kv", "backtest_results")):
    db = tmp_path / "t.db"
    conn = sqlite3.connect(str(db))
    if "wave_results" in tables:
        conn.execute("""CREATE TABLE wave_results(
            id INTEGER PRIMARY KEY, region TEXT, wave_number TEXT, focus TEXT, context TEXT,
            key_findings TEXT, candidates TEXT, batches TEXT, verdict TEXT, status TEXT,
            source_file TEXT, archived INTEGER, created_at TEXT, updated_at TEXT,
            full_payload TEXT, region_id INTEGER)""")
    if "registry_empirical" in tables:
        conn.execute("""CREATE TABLE registry_empirical(
            id INTEGER PRIMARY KEY, region TEXT, layer TEXT, entry_id TEXT, family TEXT,
            payload TEXT, dead_at TEXT, created_at TEXT, updated_at TEXT, region_id INTEGER)""")
    if "ledger_kv" in tables:
        conn.execute("""CREATE TABLE ledger_kv(
            id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT,
            created_at TEXT, updated_at TEXT)""")
    if "backtest_results" in tables:
        conn.execute("""CREATE TABLE backtest_results(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, dataset TEXT, status TEXT,
            sharpe REAL, created_at TEXT)""")
    conn.commit()
    return db, conn


def _wave(conn, region="TEST", wave="w1", verdict="PASS", status="closed",
          findings=None, updated_at="2026-10-02T00:00:00"):
    conn.execute(
        "INSERT INTO wave_results(region,wave_number,verdict,status,key_findings,updated_at) "
        "VALUES (?,?,?,?,?,?)",
        (region, wave, verdict, status, json.dumps(findings or []), updated_at),
    )
    conn.commit()


def _snap(conn, region="TEST", ts="2026-10-02T01:00:00"):
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
        (region, f"priors_snapshot_{region.lower()}", json.dumps({"generated_at": ts})),
    )
    conn.commit()


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# ---------------- 第 1 项：wave_row（硬） ----------------

def test_wave_row_pass(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn)
    r = step9_audit.check_wave_row(conn, "TEST", "w1", None)
    assert r["status"] == "pass" and not r["soft"]


def test_wave_row_missing_is_hard_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    r = step9_audit.check_wave_row(conn, "TEST", "w1", None)
    assert r["status"] == "fail" and not r["soft"]


def test_wave_row_open_status_is_hard_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, status="open")
    r = step9_audit.check_wave_row(conn, "TEST", "w1", None)
    assert r["status"] == "fail"


def test_wave_row_non_enum_verdict_is_hard_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, verdict="GREEN: 2 候选达标")
    r = step9_audit.check_wave_row(conn, "TEST", "w1", None)
    assert r["status"] == "fail"


# ---------------- 第 2 项：key_findings（软） ----------------

def test_key_findings_pass_when_both_present(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, findings=["pyramid: 点亮 pv3", "prod-first 已跑"])
    r = step9_audit.check_key_findings(conn, "TEST", "w1", None)
    assert r["status"] == "pass" and r["soft"]


def test_key_findings_missing_is_soft_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, findings=["best sharpe=1.9"])
    r = step9_audit.check_key_findings(conn, "TEST", "w1", None)
    assert r["status"] == "fail" and r["soft"]


# ---------------- 第 6 项：priors_snapshot（硬） ----------------

def test_priors_snapshot_stale_is_hard_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, updated_at="2026-10-02T19:00:00")
    _snap(conn, ts="2026-10-02T01:00:00")
    r = step9_audit.check_priors_snapshot(conn, "TEST", "2026-10-02T19:00:00")
    assert r["status"] == "fail" and not r["soft"]


def test_priors_snapshot_fresh_passes(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, updated_at="2026-10-02T19:00:00")
    _snap(conn, ts="2026-10-02T19:30:00")
    r = step9_audit.check_priors_snapshot(conn, "TEST", "2026-10-02T19:00:00")
    assert r["status"] == "pass"


def test_priors_snapshot_absent_is_unknown_not_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    r = step9_audit.check_priors_snapshot(conn, "TEST", "2026-10-02T19:00:00")
    assert r["status"] == "unknown"


# ---------------- 第 5 项：dataset_experience（软，含拼写 campain） ----------------

def test_dataset_experience_detects_missing(tmp_path, monkeypatch):
    _db, conn = _mkdb(tmp_path)
    conn.execute("INSERT INTO backtest_results(region,wave,dataset,status,created_at) "
                 "VALUES ('TEST','w1','dsX','COMPLETE','2026-10-02')")
    conn.commit()
    exp = tmp_path / "reports" / "dataset_experience"
    exp.mkdir(parents=True)
    monkeypatch.setattr(step9_audit, "REPO_ROOT", str(tmp_path))
    r = step9_audit.check_dataset_experience(conn, "TEST", "w1")
    assert r["status"] == "fail" and "dsX" in r["detail"]


def test_dataset_experience_present_passes_with_campain_spelling(tmp_path, monkeypatch):
    _db, conn = _mkdb(tmp_path)
    conn.execute("INSERT INTO backtest_results(region,wave,dataset,status,created_at) "
                 "VALUES ('TEST','w1','dsX','COMPLETE','2026-10-02')")
    conn.commit()
    exp = tmp_path / "reports" / "dataset_experience"
    exp.mkdir(parents=True)
    (exp / "test_dsX_campain.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(step9_audit, "REPO_ROOT", str(tmp_path))
    r = step9_audit.check_dataset_experience(conn, "TEST", "w1")
    assert r["status"] == "pass"


# ---------------- 汇总与分级：complete / hard_fail / soft_fail ----------------

def test_audit_complete_only_when_both_grades_pass(tmp_path, monkeypatch):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, findings=["pyramid 点亮", "prod-first 已跑"], updated_at="2026-10-02T19:00:00")
    _snap(conn, ts="2026-10-02T19:30:00")
    conn.execute("INSERT INTO backtest_results(region,wave,dataset,status,created_at) "
                 "VALUES ('TEST','w1','dsX','COMPLETE','2026-10-02')")
    conn.commit()
    exp = tmp_path / "reports" / "dataset_experience"
    exp.mkdir(parents=True)
    (exp / "test_dsX_campain.md").write_text("x", encoding="utf-8")
    monkeypatch.setattr(step9_audit, "REPO_ROOT", str(tmp_path))
    res = step9_audit.audit(conn, "test", "w1")
    assert res["complete"] is True
    assert res["hard_fail"] == [] and res["soft_fail"] == []


def test_audit_hard_fail_blocks_even_when_soft_ok(tmp_path, monkeypatch):
    _db, conn = _mkdb(tmp_path)
    _wave(conn, findings=["pyramid 点亮", "prod-first 已跑"], updated_at="2026-10-02T19:00:00")
    # 无快照 → unknown（不是 fail）；制造一个硬失败：verdict 非枚举
    conn.execute("UPDATE wave_results SET verdict='GREEN: 2' WHERE wave_number='w1'")
    conn.commit()
    exp = tmp_path / "reports" / "dataset_experience"
    exp.mkdir(parents=True)
    monkeypatch.setattr(step9_audit, "REPO_ROOT", str(tmp_path))
    res = step9_audit.audit(conn, "TEST", "w1")
    assert "wave_row" in res["hard_fail"]


def test_audit_unknown_not_counted_as_fail(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _wave(conn)
    res = step9_audit.audit(conn, "TEST", "w1")
    # dead_end_win / saturated / dataset_experience 无证据 → unknown，不在 fail 列表
    assert "dead_end_win" in res["unknown"]
    assert "saturated" in res["unknown"]
    assert "dead_end_win" not in res["hard_fail"] + res["soft_fail"]


# ---------------- 只读性：跑完 DB 字节不变（核心承诺） ----------------

def test_audit_is_readonly(tmp_path):
    db, conn = _mkdb(tmp_path)
    _wave(conn)
    conn.commit()
    conn.close()
    before = _digest(db)
    from wqb.db_conn import connect as db_connect
    conn = db_connect(str(db), readonly=True)
    try:
        step9_audit.audit(conn, "TEST", "w1")
    finally:
        conn.close()
    assert _digest(db) == before, "step9_audit 必须只读，跑完 DB 字节不变"
