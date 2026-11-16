# -*- coding: utf-8 -*-
"""step9_audit.py 基础行为测试（2026-11-15 补：该工具此前完全没有测试）。

不覆盖全部六项（dataset_experience 依赖磁盘、dead_end_win 依赖 registry 的近似推断），
只守住最容易静默退化的三条：
  - 硬判据 ①：closed + verdict 枚举；
  - 软判据 ②：key_findings 含点塔行 + prod-first；
  - 硬判据 ⑥：priors 快照不早于本波回写。
"""
import importlib.util
import json
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
_TOOL = REPO_ROOT / "tools" / "step9_audit.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("step9_audit_under_test", _TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _conn():
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE wave_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT, wave_number TEXT, key_findings TEXT,
            verdict TEXT, status TEXT, updated_at TEXT
        );
        CREATE TABLE ledger_kv (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT, key TEXT, value TEXT
        );
        """
    )
    conn.row_factory = sqlite3.Row
    return conn


def test_wave_row_requires_closed_and_verdict_enum():
    mod = _load_module()
    conn = _conn()
    conn.execute(
        "INSERT INTO wave_results(region,wave_number,verdict,status,updated_at) VALUES (?,?,?,?,?)",
        ("KOR", "101", "PASS", "closed", "2026-11-15T10:00:00"),
    )
    row = conn.execute("SELECT id, updated_at FROM wave_results WHERE region='KOR'").fetchone()
    item = mod.check_wave_row(conn, "KOR", "101", row["id"])
    assert item["status"] == "pass"

    conn.execute("UPDATE wave_results SET status='open' WHERE wave_number='101'")
    item = mod.check_wave_row(conn, "KOR", "101", row["id"])
    assert item["status"] == "fail" and not item["soft"]

    conn.execute("UPDATE wave_results SET status='closed', verdict='FULL_RED' WHERE wave_number='101'")
    item = mod.check_wave_row(conn, "KOR", "101", row["id"])
    assert item["status"] == "fail"


def test_key_findings_needs_pyramid_and_prod_first():
    mod = _load_module()
    conn = _conn()
    conn.execute(
        "INSERT INTO wave_results(region,wave_number,key_findings,verdict,status,updated_at) "
        "VALUES (?,?,?,?,?,?)",
        ("KOR", "101", '["[pyramid] 点亮 2 塔", "prod-first 未跑"]', "PASS", "closed",
         "2026-11-15T10:00:00"),
    )
    it = mod.check_key_findings(conn, "KOR", "101", None)
    assert it["status"] == "pass"
    assert it["soft"] is True

    conn.execute("UPDATE wave_results SET key_findings='[\"只有结论\"]' WHERE wave_number='101'")
    it = mod.check_key_findings(conn, "KOR", "101", None)
    assert it["status"] == "fail" and it["soft"] is True


def test_priors_snapshot_must_be_newer_than_wave_writeback():
    mod = _load_module()
    conn = _conn()
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
        ("KOR", "priors_snapshot_kor", '{"generated_at":"2026-11-15T09:00:00"}'),
    )
    it = mod.check_priors_snapshot(conn, "KOR", "2026-11-15T10:00:00")
    assert it["status"] == "fail" and not it["soft"]

    it = mod.check_priors_snapshot(conn, "KOR", "2026-11-15T08:00:00")
    assert it["status"] == "pass"

    conn.execute("DELETE FROM ledger_kv")
    it = mod.check_priors_snapshot(conn, "KOR", "2026-11-15T08:00:00")
    assert it["status"] == "unknown"


def test_wave_lessons_present_and_fresh():
    mod = _load_module()
    conn = _conn()
    lesson = {
        "n_attempts": 12,
        "knowledge_version": "aaaaaaaa-bbbbbbbb",
        "published_at": "2026-11-15T10:05:00",
    }
    conn.execute(
        "INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
        ("KOR", "wave_lessons_KOR_101", json.dumps(lesson)),
    )
    it = mod.check_wave_lessons(conn, "KOR", "101", "2026-11-15T10:00:00")
    assert it["status"] == "pass" and it["soft"] is True

    # 结论回写晚于蒸馏 → 过期（软失败）
    it = mod.check_wave_lessons(conn, "KOR", "101", "2026-11-15T11:00:00")
    assert it["status"] == "fail" and it["soft"] is True

    # 缺键 → 软失败并给命令
    it = mod.check_wave_lessons(conn, "KOR", "102", "2026-11-15T10:00:00")
    assert it["status"] == "fail" and "distill" in (it.get("hint") or "")

