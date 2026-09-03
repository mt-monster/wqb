# -*- coding: utf-8 -*-
"""Q3 校准：把平台 Q3 OS alpha 完整信息回填本地 alphas 表（幂等 upsert）。"""
import json
import os
import shutil
import sqlite3
from datetime import datetime

DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
Q_START = "2026-07-01"
SOURCES = [
    r"C:\Users\MENGTAO\.box-agent\sessions\2e9aaa4a-b7b8-4c25-a59b-f1fb7c2d20c8\tool-results\call_12ecca5a8f4c43c99759f764.txt",
    r"C:\Users\MENGTAO\.box-agent\sessions\2e9aaa4a-b7b8-4c25-a59b-f1fb7c2d20c8\tool-results\call_c16fd38d54a546609c9f611f.txt",
]

def now():
    return datetime.now().isoformat(timespec="seconds")

# 1. 备份
bak = DB + ".bak_q3_calibrate_" + datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(DB, bak)
print(f"已备份: {bak}")

# 2. 读平台数据
plat = []
for f in SOURCES:
    with open(f, encoding="utf-8") as fh:
        plat.extend(json.load(fh)["results"])
plat_q = [a for a in plat if a.get("dateSubmitted") and a["dateSubmitted"][:10] >= Q_START]
print(f"平台 Q3 OS 记录: {len(plat_q)}")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# region -> region_id
regions = {r["name"]: r["id"] for r in cur.execute("SELECT id, name FROM regions")}
now_s = now()
updated, inserted, kept = 0, 0, 0

for a in plat_q:
    aid = a["id"]
    m = a.get("metrics") or {}
    s = a.get("settings") or {}
    ra = a.get("ra") or {}
    region = s.get("region")

    rid = regions.get(region)
    if rid is None:
        cur.execute("INSERT INTO regions (name, created_at, updated_at) VALUES (?,?,?)", (region, now_s, now_s))
        conn.commit()
        rid = cur.lastrowid
        regions[region] = rid

    # dataset 解析：ra.pyramid_short 或从 pyramids 取，找不到归 _unknown
    dataset = (ra.get("pyramid_short") or "_unknown").strip() or "_unknown"
    cur.execute("SELECT id FROM datasets WHERE name=? AND region_id=?", (dataset, rid))
    drow = cur.fetchone()
    if drow:
        ds_id = drow["id"]
    else:
        cur.execute(
            "INSERT INTO datasets (name, region_id, created_at, updated_at) VALUES (?,?,?,?)",
            (dataset, rid, now_s, now_s),
        )
        ds_id = cur.lastrowid

    vals = {
        "expression": a.get("code") or "",
        "region_id": rid,
        "dataset_id": ds_id,
        "universe": s.get("universe"),
        "delay": s.get("delay"),
        "neutralization": s.get("neutralization"),
        "sharpe": m.get("sharpe"),
        "fitness": m.get("fitness"),
        "margin": m.get("margin"),
        "turnover": m.get("turnover"),
        "two_year_sharpe": m.get("two_year_sharpe"),
        "status": "COMPLETE",
        "prod_correlation": m.get("prodCorrelation"),
        "self_correlation": m.get("selfCorrelation"),
        "is_ladder_sharpe": None,
        "platform_status": a.get("status") or "ACTIVE",
        "stage": "OS",
        "alpha_type": a.get("type") or "REGULAR",
        "date_submitted": (a.get("dateSubmitted") or "")[:19].replace("T", " ") or None,
    }

    cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (aid,))
    row = cur.fetchone()
    if row:
        sets = ", ".join(f"{k}=?" for k in vals)
        cur.execute(
            f"UPDATE alphas SET {sets}, updated_at=? WHERE id=?",
            list(vals.values()) + [now_s, row["id"]],
        )
        updated += 1
    else:
        cols = list(vals.keys())
        cur.execute(
            f"INSERT INTO alphas (alpha_id, {', '.join(cols)}, created_at, updated_at) "
            f"VALUES (?, {', '.join('?' * len(cols))}, ?, ?)",
            [aid] + list(vals.values()) + [now_s, now_s],
        )
        inserted += 1

conn.commit()

# 3. 顺带清理 submission_ledger 的 DRYRUN 残留
cur.execute("DELETE FROM submission_ledger WHERE status='DRYRUN'")
dryrun_deleted = cur.rowcount
conn.commit()
conn.close()

print(f"更新: {updated} | 新增: {inserted} | 清理 DRYRUN: {dryrun_deleted}")
print("Q3 校准完成")
