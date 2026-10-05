# -*- coding: utf-8 -*-
"""`field_semantic_classify.py --all` 批量补跑（2026-10-01）的回归护栏。

契约（用户定案）：默认只跑「**有 catalog ∧ 有字段 ∧ 未判死**」的活跃集；
已有 `s1_semantic_<ds>` 的默认跳过（--force 才重跑）。

三道过滤缺一不可，每条都有实测依据：
  ① 有 catalog（ledger `catalog_<ds>` 键存在）
  ② 有字段（`fields` 表该集字段数 > 0）—— **实测 249 个 `cache_*` 前缀 catalog 键
     在 fields 表零字段**，只按 ① 选会浪费 37% 工作量在幽灵键上
  ③ 未判死（排除 `dead_dataset_index` 的 dataset_dead ∪ saturated）

另：`classify_dataset()` 是单跑与批量的**唯一**执行体——禁止两条路径各写一份。
"""
import importlib
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src", REPO / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


@pytest.fixture
def fsc(tmp_path, monkeypatch):
    """把 tools/field_semantic_classify.py 装到临时库上。"""
    mod = importlib.import_module("field_semantic_classify")
    db = tmp_path / "wqb.db"
    from wqb.store import CampaignStore
    CampaignStore(str(db)).close()
    conn = sqlite3.connect(str(db))
    conn.execute("INSERT OR IGNORE INTO regions (name) VALUES ('TST')")
    rid = conn.execute("SELECT id FROM regions WHERE name='TST'").fetchone()[0]
    # 真数据集：good1（有 catalog+有字段）、dead1（有 catalog+有字段但判死）
    # 幽灵：ghost1（有 catalog 键但 fields 零行）
    for ds in ("good1", "dead1", "ghost1"):
        conn.execute("INSERT INTO datasets (name, region_id) VALUES (?,?)", (ds, rid))
    for ds in ("good1", "dead1"):
        did = conn.execute("SELECT id FROM datasets WHERE name=?", (ds,)).fetchone()[0]
        conn.execute("INSERT INTO fields (dataset_id, field_name, field_type, coverage, user_count, alpha_count, description) "
                     "VALUES (?,?,?,?,?,?,?)", (did, f"{ds}_revenue", "MATRIX", 0.9, 0, 1, "total revenue"))
        conn.execute("INSERT INTO ledger_kv (region,key,value,updated_at) VALUES ('TST',?, '{}','2026-10-01')",
                     (f"catalog_{ds}",))
    conn.execute("INSERT INTO ledger_kv (region,key,value,updated_at) VALUES ('TST','catalog_ghost1','{}','2026-10-01')")
    conn.execute("INSERT INTO ledger_kv (region,key,value,updated_at) VALUES ('TST','dead1_dead','{}','2026-10-01')")
    conn.commit()
    conn.close()
    monkeypatch.setattr(mod, "db_connect", lambda *a, **k: _conn(db, k))
    mod._TEST_DB = str(db)
    return mod


def _conn(db, kw):
    c = sqlite3.connect(str(db))
    if kw.get("row_factory") is not None:
        c.row_factory = kw["row_factory"]
    return c


def test_active_selection_excludes_dead_and_ghost(fsc):
    """① 有 catalog ② 有字段 ③ 未判死 —— 三条过滤各剔一个。"""
    conn = _conn(fsc._TEST_DB, {"row_factory": sqlite3.Row})
    try:
        selected, skipped = fsc._active_catalog_datasets(conn, "TST")
    finally:
        conn.close()
    assert selected == ["good1"]
    assert "dead1" in skipped and "判死" in skipped["dead1"]
    assert "ghost1" in skipped and "幽灵" in skipped["ghost1"]


def test_dry_run_lists_without_writing(fsc, capsys):
    class A:
        region = "TST"; force = False; dry_run = True
    rc = fsc.run_all(A())
    out = capsys.readouterr().out
    assert rc == 0
    assert "would classify: good1" in out
    conn = _conn(fsc._TEST_DB, {})
    try:
        n = conn.execute("SELECT COUNT(*) FROM ledger_kv WHERE region='TST' AND key LIKE 's1_semantic_%'").fetchone()[0]
    finally:
        conn.close()
    assert n == 0, "dry-run 不得写库"


def test_batch_writes_ledger_and_is_idempotent(fsc, capsys, tmp_path, monkeypatch):
    class A:
        region = "TST"; force = False; dry_run = False
    rc = fsc.run_all(A())
    assert rc == 0
    conn = _conn(fsc._TEST_DB, {})
    try:
        n = conn.execute("SELECT COUNT(*) FROM ledger_kv WHERE region='TST' AND key LIKE 's1_semantic_%'").fetchone()[0]
    finally:
        conn.close()
    assert n == 1, "应只为 good1 写台账"
    # 第二次跑：已有台账 → 默认跳过
    rc2 = fsc.run_all(A())
    out2 = capsys.readouterr().out
    assert rc2 == 0
    assert "待跑: 0" in out2


def test_force_reruns_existing(fsc, capsys):
    class A:
        region = "TST"; force = False; dry_run = False
    fsc.run_all(A())
    capsys.readouterr()
    A.force = True
    fsc.run_all(A())
    out = capsys.readouterr().out
    assert "待跑: 1" in out


def test_classify_dataset_is_single_executor(fsc, tmp_path):
    """单跑与批量共用同一执行体；rc=1 表示该集无字段（幽灵键）。"""
    out_p = tmp_path / "o.json"
    rc, payload = fsc.classify_dataset("TST", "good1", write_ledger=False,
                                       out_path=str(out_p), quiet=True)
    assert rc == 0 and payload["total_fields"] == 1
    rc2, _ = fsc.classify_dataset("TST", "ghost1", write_ledger=False,
                                  out_path=str(out_p), quiet=True)
    assert rc2 == 1, "幽灵键（fields 零行）应返回 rc=1"
