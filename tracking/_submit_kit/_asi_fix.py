# -*- coding: utf-8 -*-
"""补 ASI 数据集目录（catalog_sync 的 universe fallback bug 导致 ASI 拉成 0）。"""
import asyncio
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(WQ_ROOT / "tracking" / "_submit_kit"))
DB = WQ_ROOT / "data" / "wqb.db"


async def main():
    from brain_api import BrainApiClient
    from _catalog_sync import fetch_page_all, UNIVERSE_CANDIDATES

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    rows = None
    for uni in UNIVERSE_CANDIDATES["ASI"]:
        rows, err = await fetch_page_all(brain, "ASI", uni, 1)
        if rows:
            print(f"[ASI] uni={uni} → {len(rows)} 个数据集")
            break
    if not rows:
        print(f"[ASI] 全部 universe 失败: {err}")
        return

    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    cur.execute("SELECT id FROM regions WHERE name='ASI'")
    rid = cur.fetchone()
    if not rid:
        print("[ASI] regions 表无 ASI！")
        return
    rid = rid[0]
    cur.execute("SELECT status, COUNT(*) FROM datasets GROUP BY status")
    st = cur.fetchall()
    default_status = max(st, key=lambda x: x[1])[0] if st else "active"
    now = datetime.now().isoformat(timespec="seconds")
    ins = upd = 0
    for d in rows:
        cur.execute("SELECT id FROM datasets WHERE region_id=? AND name=?", (rid, d["id"]))
        if cur.fetchone():
            cur.execute("UPDATE datasets SET category=?, field_count=?, coverage=?, "
                        "alpha_count=?, value_score=?, pyramid_multiplier=?, updated_at=?, "
                        "delay=COALESCE(delay,1) WHERE region_id=? AND name=?",
                        (d.get("category"), d.get("field_count"), d.get("coverage"),
                         d.get("alpha_count"), d.get("value_score"),
                         d.get("pyramid_multiplier"), now, rid, d["id"]))
            upd += 1
        else:
            cur.execute("INSERT INTO datasets (name, region_id, category, field_count, "
                        "coverage, alpha_count, value_score, pyramid_multiplier, status, "
                        "created_at, updated_at, delay) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (d["id"], rid, d.get("category"), d.get("field_count"),
                         d.get("coverage"), d.get("alpha_count"), d.get("value_score"),
                         d.get("pyramid_multiplier"), default_status, now, now, 1))
            ins += 1
    con.commit()
    cur.execute("SELECT COUNT(*), SUM(CASE WHEN category IS NULL THEN 1 ELSE 0 END) "
                "FROM datasets WHERE region_id=?", (rid,))
    n, nullc = cur.fetchone()
    con.close()
    print(f"[ASI] 插入 {ins} / 更新 {upd}；现共 {n} 个数据集，NULL 类别 {nullc}")


if __name__ == "__main__":
    asyncio.run(main())
