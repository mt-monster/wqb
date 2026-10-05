# -*- coding: utf-8 -*-
"""archive_submit_ready.py — submit_ready 终态残留归档（移动，非删除；可回滚）。

用途
----
submit_ready 被设计成「当天配额吃不下」的**活水队列**，但终态行（DEAD/EXPIRED/
SUPERSEDED/SUBMITTED）会持续堆积，把表变成坟场，掩盖真正可提交的候选。
本工具把终态行移到 `submit_ready_archive`，主表只留活水。

安全设计（三条）
----------------
1. **移动而非删除**：先 INSERT 进归档表，再 DELETE 主表行，同一个事务。
2. **双备份**：归档表里存全字段（含 orig_id），并导出 JSON 快照到
   `output_report/archive_submit_ready_<batch>.json`。
3. **可回滚**：`--restore <batch>` 由归档表按 batch 完整迁回主表。

**绝不支持**不带 `--region` 的整表归档（防误操全库，与 store.retire_region 同口径）。

用法
----
  # 预览
  python tools/archive_submit_ready.py --region IND --status DEAD,EXPIRED --dry-run
  # 执行
  python tools/archive_submit_ready.py --region IND --status DEAD,EXPIRED
  # 回滚
  python tools/archive_submit_ready.py --restore 20261001-003000

退出码: 0=成功, 1=失败
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "src")))
from wqb.db_conn import connect as db_connect  # noqa: E402  规范工厂（禁裸 sqlite3.connect）

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DB = os.environ.get("WQB_DB_PATH") or os.path.join(_REPO, "data", "wqb.db")
_OUT = os.path.join(_REPO, "output_report")

_COLS = [
    "alpha_id", "region", "universe", "delay", "decay", "neutralization", "expr",
    "skeleton", "suggested_tags", "sharpe", "fitness", "turnover", "two_year",
    "sub_universe", "cluster_test", "prod", "self", "gate", "verified_at",
    "verified_by", "towers", "family", "status", "added_at", "note",
]

_ARCHIVE_DDL = """
CREATE TABLE IF NOT EXISTS submit_ready_archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orig_id INTEGER,
    batch VARCHAR(40),
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archive_reason TEXT,
    alpha_id VARCHAR(32), region VARCHAR(16),
    universe VARCHAR(32), delay INTEGER, decay INTEGER, neutralization VARCHAR(24),
    expr TEXT, skeleton TEXT, suggested_tags TEXT,
    sharpe REAL, fitness REAL, turnover REAL, two_year REAL,
    sub_universe REAL, cluster_test REAL, prod REAL, self REAL,
    gate TEXT, verified_at TIMESTAMP, verified_by VARCHAR(24),
    towers TEXT, family TEXT, status VARCHAR(20), added_at TIMESTAMP, note TEXT
);
CREATE INDEX IF NOT EXISTS ix_sqa_batch ON submit_ready_archive(batch);
CREATE INDEX IF NOT EXISTS ix_sqa_aid  ON submit_ready_archive(alpha_id, region);
"""


def _conn(readonly=False):
    """走规范工厂（统一 timeout / busy_timeout / WAL）；只读用 readonly=True。"""
    conn = db_connect(_DB, readonly=readonly)
    conn.row_factory = sqlite3.Row
    return conn


def _snapshot(rows, batch, reason):
    os.makedirs(_OUT, exist_ok=True)
    path = os.path.join(_OUT, f"archive_submit_ready_{batch}.json")
    payload = {
        "batch": batch, "reason": reason, "db": _DB,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "count": len(rows),
        "rows": [dict(r) for r in rows],
    }
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, default=str)
    os.replace(tmp, path)
    return path


def _select(con, region, statuses):
    q = f"SELECT id, {', '.join(_COLS)} FROM submit_ready WHERE 1=1"
    ps = []
    if region:
        q += " AND region=?"
        ps.append(region)
    if statuses:
        q += f" AND status IN ({','.join('?' * len(statuses))})"
        ps.extend(statuses)
    q += " ORDER BY status, added_at"
    return con.execute(q, ps).fetchall()


def cmd_archive(a):
    if not a.region and not a.all_regions:
        print("[archive] 必须指定 --region（或显式 --all-regions）；拒绝无区域限定的整表操作")
        return 1
    statuses = [s.strip().upper() for s in a.status.split(",") if s.strip()]
    con = _conn()
    con.row_factory = sqlite3.Row
    try:
        con.executescript(_ARCHIVE_DDL)
        rows = _select(con, a.region, statuses)
        if not rows:
            print(f"[archive] 无匹配行（region={a.region or 'ALL'}, status={statuses}）")
            return 0

        print(f"[archive] 匹配 {len(rows)} 行 | region={a.region or 'ALL'} | status={statuses}")
        by = {}
        for r in rows:
            by[r["status"]] = by.get(r["status"], 0) + 1
        for k, v in sorted(by.items(), key=lambda x: -x[1]):
            print(f"    {k:14s} {v}")

        if a.dry_run:
            print("[archive] dry-run：未写入、未删除")
            return 0

        batch = datetime.now().strftime("%Y%m%d-%H%M%S")
        snap = _snapshot(rows, batch, a.reason or f"archive {a.region or 'ALL'} {statuses}")
        print(f"[archive] JSON 快照: {snap}")

        cols = ", ".join(_COLS)
        marks = ", ".join("?" * len(_COLS))
        ids = [r["id"] for r in rows]
        con.execute("BEGIN")
        try:
            for r in rows:
                con.execute(
                    f"INSERT INTO submit_ready_archive "
                    f"(orig_id, batch, archive_reason, {cols}) VALUES (?,?,?,{marks})",
                    [r["id"], batch, a.reason or "", *[r[c] for c in _COLS]])
            con.execute(
                f"DELETE FROM submit_ready WHERE id IN ({','.join('?' * len(ids))})", ids)
            con.commit()
        except Exception:
            con.rollback()
            raise
        print(f"[archive] batch={batch}：已归档 {len(rows)} 行，主表删除同批行（同一事务）")
        print(f"[archive] 回滚方式: python tools/archive_submit_ready.py --restore {batch}")
    finally:
        con.close()
    return 0


def cmd_restore(a):
    con = _conn()
    con.row_factory = sqlite3.Row
    try:
        con.executescript(_ARCHIVE_DDL)
        rows = con.execute(
            "SELECT * FROM submit_ready_archive WHERE batch=?", (a.restore,)).fetchall()
        if not rows:
            print(f"[restore] batch {a.restore} 无记录")
            return 1
        ins = skip = 0
        con.execute("BEGIN")
        try:
            for r in rows:
                dup = con.execute(
                    "SELECT 1 FROM submit_ready WHERE alpha_id=? AND region=?",
                    (r["alpha_id"], r["region"])).fetchone()
                if dup:
                    skip += 1
                    continue
                cols = ", ".join(_COLS)
                marks = ", ".join("?" * len(_COLS))
                con.execute(
                    f"INSERT INTO submit_ready ({cols}) VALUES ({marks})",
                    [r[c] for c in _COLS])
                ins += 1
            con.execute("DELETE FROM submit_ready_archive WHERE batch=?", (a.restore,))
            con.commit()
        except Exception:
            con.rollback()
            raise
        print(f"[restore] batch={a.restore}：迁回 {ins} 行，跳过已存在 {skip} 行，归档表已清理")
    finally:
        con.close()
    return 0


def main():
    p = argparse.ArgumentParser(description="submit_ready 终态残留归档（可回滚）")
    p.add_argument("--region", help="限定区域（强烈建议；不带 --all-regions 时必填）")
    p.add_argument("--all-regions", action="store_true", help="显式允许跨区域（需谨慎）")
    p.add_argument("--status", default="DEAD,EXPIRED", help="逗号分隔的终态，默认 DEAD,EXPIRED")
    p.add_argument("--reason", help="归档说明")
    p.add_argument("--dry-run", action="store_true", help="只预览")
    p.add_argument("--restore", help="按 batch 号回滚")
    a = p.parse_args()
    return cmd_restore(a) if a.restore else cmd_archive(a)


if __name__ == "__main__":
    sys.exit(main())
