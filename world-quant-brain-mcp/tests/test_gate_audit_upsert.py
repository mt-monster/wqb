"""gate-audit 落库 upsert 测试（2026-11-23 修复）。

根因：生产 data/wqb.db 是历史库，gate_results 零 UNIQUE 索引 ⇒ 原
`INSERT ... ON CONFLICT(region,wave,dataset) DO UPDATE` 每次都抛
「no matching constraint」，所有 MCP 直发批审计行静默丢失。
修复：先 UPDATE ... WHERE，rowcount=0 再 INSERT（不依赖约束）。

本测试用临时库建**无约束**表复现历史库，另建**有约束**表验证兼容，
全程无网络、不碰生产库（db_conn.connect 的 pytest 硬闸天然生效）。
"""
import hashlib
import json
import os
import sqlite3
import sys

import pytest

MCP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(MCP_DIR)
SRC = os.path.join(REPO_ROOT, "src")
for p in (MCP_DIR, SRC):
    if p not in sys.path:
        sys.path.insert(0, p)


def _make_db(tmp_path, with_unique: bool):
    """建临时库；with_unique=False 复现历史库（零索引）。"""
    db = str(tmp_path / "wqb.db")
    con = sqlite3.connect(db)
    unique = ", UNIQUE(region, wave, dataset)" if with_unique else ""
    con.execute(
        "CREATE TABLE gate_results ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "region TEXT NOT NULL, wave TEXT NOT NULL, dataset TEXT NOT NULL, "
        "all_pass INTEGER, report_json TEXT NOT NULL, created_at TEXT, updated_at TEXT"
        f"{unique})"
    )
    con.commit()
    con.close()
    return db


@pytest.fixture
def mod(monkeypatch, tmp_path):
    import tools_sim
    db = _make_db(tmp_path, with_unique=False)
    monkeypatch.setattr(tools_sim, "_resolve_audit_db", lambda: db)
    return tools_sim, db


def _rows(db):
    con = sqlite3.connect(db)
    try:
        return con.execute(
            "SELECT region,wave,dataset,all_pass,report_json,created_at,updated_at "
            "FROM gate_results ORDER BY id"
        ).fetchall()
    finally:
        con.close()


def test_historical_db_no_unique_writes_without_error(mod):
    """无约束历史库：落库成功，不抛 ON CONFLICT 错。"""
    tools_sim, db = mod
    tools_sim._record_gate_pass("USA", ["rank(close)", "rank(volume)"], None)
    rows = _rows(db)
    assert len(rows) == 1, f"应写入恰好 1 行，实际 {len(rows)}"
    assert rows[0][0] == "USA"
    assert rows[0][1].startswith("mcp_direct_")
    assert rows[0][3] == 1  # all_pass
    report = json.loads(rows[0][4])
    assert report["passed"] == 2 and report["total"] == 2


def test_idempotent_resend_updates_not_inserts(mod):
    """同批重发：幂等刷新，不新增行。"""
    tools_sim, db = mod
    tools_sim._record_gate_pass("USA", ["rank(close)", "rank(volume)"], None)
    tools_sim._record_gate_pass("USA", ["rank(close)", "rank(volume)"],
                                {"gate": "toolkit_static", "failed_expressions": {"1": ["ghost"]}})
    rows = _rows(db)
    assert len(rows) == 1, f"重发应仍 1 行，实际 {len(rows)}"
    assert rows[0][3] == 0, "失败报告应覆盖 all_pass=0"
    assert "ghost" in rows[0][4]


def test_duplicate_keys_all_refreshed(mod):
    """历史重复键（同键多行）：全部刷新，不新增第 N+1 行。"""
    tools_sim, db = mod
    con = sqlite3.connect(db)
    fp = hashlib.sha1("\n".join(["rank(close)"]).encode()).hexdigest()[:16]
    wkey = f"mcp_direct_{fp[:8]}"
    for i in range(3):
        con.execute(
            "INSERT INTO gate_results (region,wave,dataset,all_pass,report_json,created_at,updated_at) "
            "VALUES (?,?,?,?,?,?,?)",
            ("EUR", wkey, "mcp_direct", 1, json.dumps({"i": i}), "t0", "t0"),
        )
    con.commit()
    con.close()
    tools_sim._record_gate_pass("EUR", ["rank(close)"], {"gate": "x", "failed_expressions": {}})
    rows = _rows(db)
    assert len(rows) == 3, f"重复键应被刷新而非新增，实际 {len(rows)} 行"
    assert all(r[3] == 0 for r in rows), "3 行都应被刷新为 all_pass=0"


def test_unique_constraint_db_also_works(monkeypatch, tmp_path):
    """有 UNIQUE 约束的新库：同样写入成功（兼容两代 schema）。"""
    import tools_sim
    db = _make_db(tmp_path, with_unique=True)
    monkeypatch.setattr(tools_sim, "_resolve_audit_db", lambda: db)
    tools_sim._record_gate_pass("KOR", ["rank(volume)"], None)
    tools_sim._record_gate_pass("KOR", ["rank(volume)"], None)
    rows = _rows(db)
    assert len(rows) == 1, f"有约束库重发也应 1 行，实际 {len(rows)}"


def test_no_db_is_noop(monkeypatch):
    """找不到库时安静跳过（不抛异常、不阻断发批）。"""
    import tools_sim
    monkeypatch.setattr(tools_sim, "_resolve_audit_db", lambda: None)
    tools_sim._record_gate_pass("USA", ["rank(close)"], None)  # 不抛即通过
