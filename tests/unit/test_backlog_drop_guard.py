# -*- coding: utf-8 -*-
"""积压裁决（标 dropped）的守卫测试（2026-09-17）。

背景：EUR 2,235 条 gated 积压里 1,667 条（74.6%）被加固后的门禁拦下
（1,430 条命中新增的结构加权混合判定）→ 用户裁决标 `dropped`。
批量改状态属不可逆操作，故以「迁移工具三守卫」惯例实现并在此锁定：
  ① `--apply-drop` 必须配 `--db-backup`（否则拒绝执行）；
  ② 保护态：只动 `alpha_id IS NULL` 且状态仍为来源状态的行；
  ③ 幂等：重跑零变更；分批 rowcount 校验；ledger 台账留痕。
"""
import json
import os
import sqlite3
import sys
import types

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))


def _mkdb(path):
    conn = sqlite3.connect(path)
    conn.execute("""CREATE TABLE expressions (
        id INTEGER PRIMARY KEY, region TEXT, status TEXT, alpha_id TEXT,
        expression TEXT, skeleton TEXT, wave TEXT, dataset TEXT, updated_at TEXT)""")
    conn.execute("""CREATE TABLE ledger_kv (
        id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT,
        created_at TEXT, updated_at TEXT)""")
    rows = [
        # (id, region, status, alpha_id, expr)
        (1, "EUR", "gated", None, "rank(a)"),          # 失败且在来源态 → 应 dropped
        (2, "EUR", "gated", "ABC123", "rank(b)"),      # 有 alpha → 保护
        (3, "EUR", "pending", None, "rank(c)"),        # 状态不匹配 → 保护
        (4, "EUR", "gated", None, "rank(d)"),          # 不在失败清单 → 不动
        (5, "USA", "gated", None, "rank(e)"),          # 别的区 → 不动
    ]
    for i, reg, st, aid, e in rows:
        conn.execute("INSERT INTO expressions (id, region, status, alpha_id, expression) "
                     "VALUES (?,?,?,?,?)", (i, reg, st, aid, e))
    conn.commit()
    conn.close()


def _args(db, backup, status="gated"):
    return types.SimpleNamespace(
        region="EUR", status=status, db=db, db_backup=backup,
        drop_batch_size=200, apply_drop=True, gate_filter=True)


@pytest.fixture()
def mod():
    import importlib
    import pick_backlog_representatives as m
    return importlib.reload(m)


def test_drop_respects_protected_states(tmp_path, mod):
    db = str(tmp_path / "t.db")
    _mkdb(db)
    backup = str(tmp_path / "t.db.bak")
    mod._apply_drop(_args(db, backup), [1, 2, 3])   # 4/5 不在失败清单

    conn = sqlite3.connect(db)
    got = dict(conn.execute("SELECT id, status FROM expressions").fetchall())
    conn.close()
    assert got[1] == "dropped", "失败且在来源态的行必须被废弃"
    assert got[2] == "gated", "有 alpha_id 的行必须受保护"
    assert got[3] == "pending", "状态已变的行必须受保护"
    assert got[4] == "gated", "不在失败清单的行不得被改"
    assert got[5] == "gated", "其他区域不得被改"
    assert os.path.isfile(backup), "必须先落备份"


def test_drop_is_idempotent(tmp_path, mod):
    db = str(tmp_path / "t.db")
    _mkdb(db)
    mod._apply_drop(_args(db, str(tmp_path / "b1.bak")), [1, 2, 3])
    # 第二次：1 已是 dropped（状态不匹配来源态）→ 不再改
    mod._apply_drop(_args(db, str(tmp_path / "b2.bak")), [1, 2, 3])
    conn = sqlite3.connect(db)
    n = conn.execute("SELECT COUNT(*) FROM expressions WHERE status='dropped'").fetchone()[0]
    conn.close()
    assert n == 1, "重跑不得产生额外变更"


def test_drop_writes_ledger_audit(tmp_path, mod):
    db = str(tmp_path / "t.db")
    _mkdb(db)
    mod._apply_drop(_args(db, str(tmp_path / "b.bak")), [1])
    conn = sqlite3.connect(db)
    row = conn.execute("SELECT key, value FROM ledger_kv WHERE region='EUR'").fetchone()
    conn.close()
    assert row and row[0] == "drop_batch_backlog_gate_filter"
    payload = json.loads(row[1])
    assert payload["count"] == 1 and payload["to_status"] == "dropped"


def test_apply_drop_requires_backup(tmp_path, mod, monkeypatch, capsys):
    """三守卫①：`--apply-drop` 不给 `--db-backup` 必须拒绝执行。"""
    db = str(tmp_path / "t.db")
    _mkdb(db)
    argv = ["pick_backlog_representatives.py", "--region", "EUR",
            "--out", str(tmp_path / "o.json"), "--gate-filter", "--apply-drop",
            "--db", db]
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit) as e:
        mod.main()
    assert "--db-backup" in str(e.value)


def test_apply_drop_requires_gate_filter(tmp_path, mod, monkeypatch):
    """三守卫①补：`--apply-drop` 不给 `--gate-filter` 也必须拒绝
    （防止凭旧 id 文件批量改状态）。"""
    argv = ["pick_backlog_representatives.py", "--region", "EUR",
            "--out", str(tmp_path / "o.json"), "--apply-drop",
            "--db-backup", str(tmp_path / "b.bak")]
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit) as e:
        mod.main()
    assert "--gate-filter" in str(e.value)


def test_refuses_to_overwrite_existing_backup(tmp_path, mod):
    db = str(tmp_path / "t.db")
    _mkdb(db)
    backup = str(tmp_path / "existing.bak")
    open(backup, "w").close()
    with pytest.raises(SystemExit):
        mod._apply_drop(_args(db, backup), [1])
