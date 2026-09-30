# -*- coding: utf-8 -*-
"""`submit_ready` 唯一约束自愈回归（2026-09-28）。

背景（真实缺陷，影响所有区域）：
  P0 迁移「改名→新建同名表」重建 `submit_ready` 时**丢了 `UNIQUE(alpha_id, region)`**，
  但入队 upsert 用 `ON CONFLICT(alpha_id,region)` →
    `sqlite3.OperationalError: ON CONFLICT clause does not match any PRIMARY KEY or UNIQUE constraint`
  → **过闸候选静默不入队**。实测 other466 一轮 7 条 `submit_ready +7` 全部丢失，
  且 `harvest_multisim.py --auto-upsert` 只打印一行 `[queue] 入队跳过` 就继续，无异常抛出。

修法：`submit_queue.SCHEMA` 增加 `CREATE UNIQUE INDEX IF NOT EXISTS ux_sr_alpha_region`，
并在 `_schema.ensure_schema()` 末尾调用 `submit_queue.ensure_table()`，
使**任何被迁移过的库一经 store 打开即自动补回约束**（幂等）。

本测试守护：① 空表建库后索引存在；② 模拟"迁移丢约束"的老库，经 store 打开后自愈；
③ upsert（ON CONFLICT(alpha_id,region)）在自愈后可正常 INSERT 与 UPDATE。
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))

from wqb.store import CampaignStore  # noqa: E402
from wqb.store import submit_queue as sq  # noqa: E402

IDX = "ux_sr_alpha_region"


def _indexes(db):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        return {r[0] for r in c.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='submit_ready'")}
    finally:
        c.close()


def test_fresh_db_has_unique_alpha_region_index(tmp_path):
    """全新库：ensure_table 后必须存在唯一索引。"""
    db = str(tmp_path / "fresh.db")
    con = sq.connect(db)
    sq.ensure_table(con)
    con.commit()
    con.close()
    assert IDX in _indexes(db), "新建库缺 ux_sr_alpha_region（入队 upsert 会失败）"


def test_migrated_db_self_heals_on_store_open(tmp_path):
    """模拟迁移丢约束的老库：经 CampaignStore 打开后自动补回。

    夹具只造 **丢了 UNIQUE 的 submit_ready**，不造 alphas ——
    `ensure_schema()` 会自行 `CREATE TABLE IF NOT EXISTS alphas`（若夹具先造了残缺
    alphas，后续建索引会因缺 prod_correlation 等列而报错，那是夹具问题不是产品问题）。
    """
    db = str(tmp_path / "migrated.db")
    con = sqlite3.connect(db)
    con.executescript(
        """
        CREATE TABLE submit_ready (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alpha_id TEXT NOT NULL,
            region TEXT NOT NULL,
            status TEXT DEFAULT 'READY'
        );
        """)
    con.commit()
    con.close()
    assert IDX not in _indexes(db), "前置：老库不应有该索引"

    CampaignStore(db).close()  # 打开即应触发自愈

    assert IDX in _indexes(db), "store 打开未自愈：submit_ready 仍缺唯一约束"


def test_upsert_works_after_heal(tmp_path):
    """自愈后 ON CONFLICT(alpha_id,region) 必须能 INSERT 且能 UPDATE。"""
    db = str(tmp_path / "upsert.db")
    con = sq.connect(db)
    sq.ensure_table(con)
    # submit_ready 有 FK 指向 alphas；夹具自建最小 alphas 以满足 FK
    con.execute("CREATE TABLE IF NOT EXISTS alphas (alpha_id TEXT PRIMARY KEY)")
    con.execute("INSERT INTO alphas (alpha_id) VALUES ('AA1')")
    sql = ("INSERT INTO submit_ready (alpha_id, region, status) VALUES (?,?,?) "
           "ON CONFLICT(alpha_id,region) DO UPDATE SET status=excluded.status")
    con.execute(sql, ("AA1", "KOR", "READY"))
    con.execute(sql, ("AA1", "KOR", "BLOCKED"))  # 第二次应走 DO UPDATE
    got = con.execute(
        "SELECT status FROM submit_ready WHERE alpha_id='AA1' AND region='KOR'").fetchone()[0]
    con.commit()
    con.close()
    assert got == "BLOCKED", f"upsert 未走 UPDATE，status={got}"


def test_schema_constant_declares_the_index():
    """静态守卫：索引必须写在 SCHEMA 常量里（否则新库仍缺）。"""
    assert IDX in sq.SCHEMA, f"SCHEMA 未声明 {IDX}（新库/迁移库都会缺约束）"
