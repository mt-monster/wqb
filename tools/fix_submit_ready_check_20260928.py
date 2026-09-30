#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""fix_submit_ready_check_20260928.py — 修复 P0 迁移给 `submit_ready` 加错的 CHECK（2026-09-28）。

症状：入队报 `CHECK constraint failed: status IN ('SUBMITTED','DEAD','BLOCKED','READY')`。

根因：**规范 schema（`submit_queue.SCHEMA`）根本没有 CHECK**；P0 迁移「改名→新建同名表」
重建时**自作主张加了一个更严的 CHECK**，且漏了代码状态机实际会写的两个值：
  - `STATUS_EXPIRED`    （tools/submit_queue.py:336，`--verify` 判定软失效时写）
  - `STATUS_SUPERSEDED` （src/wqb/store/submit_queue.py:614，同骨架新候选顶替旧候选时写）
→ 任何走到这两条路径都会 CHECK 失败。

修法：按**规范 DDL** 重建该表（规范里无 CHECK，状态合法性由代码保证），保数据、保索引、
保 `UNIQUE(alpha_id, region)`（该约束此前刚自愈回来，重建时必须保留——否则入队 bug 复发）。
流程与 `fix_stale_fk_20260928.py` 同纪律：**先在副本上验证，`--apply` 才落地**（落地前自动备份）。

用法:
  python tools/fix_submit_ready_check_20260928.py --db data/wqb.db            # 副本验证
  python tools/fix_submit_ready_check_20260928.py --db data/wqb.db --apply    # 落地
"""
from __future__ import annotations

import argparse
import re
import shutil
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from wqb.store import submit_queue as sq  # noqa: E402

TABLE = "submit_ready"


def _canonical_ddl() -> str:
    """从 submit_queue.SCHEMA 里取规范的 CREATE TABLE 语句。"""
    for stmt in sq.SCHEMA.split(";"):
        s = stmt.strip()
        if s.upper().startswith("CREATE TABLE") and TABLE in s:
            return s
    raise RuntimeError("SCHEMA 里找不到 submit_ready 的 CREATE TABLE")


def _indexes(conn, table):
    return [r[0] for r in conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL",
        (table,))]


def rebuild(conn) -> str:
    ddl = _canonical_ddl()
    if "CHECK" in ddl.upper():
        raise RuntimeError("规范 DDL 里出现了 CHECK —— 与预期不符，中止（避免把错误固化）")

    idx = _indexes(conn, TABLE)
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({TABLE})")]
    n_before = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]

    # 依赖该表的视图先卸后建（DROP TABLE 时 SQLite 会校验视图有效性）
    views = [(r[0], r[1]) for r in conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view' AND sql IS NOT NULL")]
    dependent = [(n, s) for n, s in views
                 if re.search(r"\b%s\b" % re.escape(TABLE), s or "", re.I)]

    tmp = f"{TABLE}__chkfix"
    stmts = [f'DROP VIEW IF EXISTS "{n}"' for n, _ in dependent]
    stmts += [
        f"DROP TABLE IF EXISTS {tmp}",
        ddl.replace("CREATE TABLE IF NOT EXISTS", "CREATE TABLE", 1)
           .replace(TABLE, tmp, 1),
        "INSERT INTO {t} ({c}) SELECT {c} FROM {s}".format(
            t=tmp, c=",".join(f'"{x}"' for x in cols), s=TABLE),
        f"DROP TABLE {TABLE}",
        f"ALTER TABLE {tmp} RENAME TO {TABLE}",
    ]
    stmts += idx
    stmts += [s for _, s in dependent]

    con = conn
    con.execute("PRAGMA foreign_keys=OFF")
    for s in stmts:
        con.execute(s)
    n_after = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    con.commit()
    return (f"[fix ] {TABLE}: 重建去掉错误 CHECK；行数 {n_before} -> {n_after}；"
            f"索引 {len(idx)} + 视图 {len(dependent)} 已重建；"
            f"{'行数一致 OK' if n_before == n_after else '★行数不一致!!'}")


def verify(conn):
    out = []
    out.append(("integrity_check", conn.execute("PRAGMA integrity_check").fetchall()[:1]))
    out.append(("行数", conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]))
    # 关键验证：EXPIRED / SUPERSEDED 现在必须可写（此前正是这两个值触发 CHECK 失败）
    for st in ("EXPIRED", "SUPERSEDED", "READY", "DEAD", "BLOCKED", "SUBMITTED"):
        try:
            conn.execute("BEGIN")
            conn.execute(
                f"INSERT INTO {TABLE} (alpha_id, region, status) VALUES ('__probe__', 'ZZT', ?)", (st,))
            conn.execute("ROLLBACK")
            out.append((f"写 status={st}", "OK"))
        except Exception as e:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
            out.append((f"写 status={st}", f"ERR {type(e).__name__}: {e}"))
    # 唯一约束必须还在（否则入队 bug 复发）
    idx = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name=?", (TABLE,))}
    out.append(("唯一索引 ux_sr_alpha_region", "在" if "ux_sr_alpha_region" in idx else "★缺失"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/wqb.db")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    real = Path(a.db) if Path(a.db).is_absolute() else REPO / a.db
    if not real.exists():
        print(f"[ERR] 找不到 {real}")
        return 1

    work = REPO / "cache" / "_dbrepair" / f"srchk_{time.strftime('%H%M%S')}"
    work.mkdir(parents=True, exist_ok=True)
    copy = work / "wqb.db"
    shutil.copy2(real, copy)
    for ext in ("-wal", "-shm"):
        src = Path(str(real) + ext)
        if src.exists():
            shutil.copy2(src, Path(str(copy) + ext))
    print(f"[副本] {copy}")

    conn = sqlite3.connect(str(copy))
    try:
        print("  " + rebuild(conn))
        print("\n[副本校验]")
        rows = verify(conn)
        for k, v in rows:
            print(f"  {k:<34} {v}")
        ok = (rows[0][1] == [("ok",)] and
              all("ERR" not in str(v) for _, v in rows) and
              "在" in str(dict(rows).get("唯一索引 ux_sr_alpha_region")))
    finally:
        conn.close()

    if not ok:
        print("\n[中止] 副本校验未通过，不动真实库。")
        return 1
    print("\n[副本校验通过]")
    if not a.apply:
        print("（未加 --apply，未改动真实库）")
        return 0

    bak = real.with_name(real.name + f".bak_srchk_{time.strftime('%Y%m%d_%H%M%S')}")
    shutil.copy2(real, bak)
    print(f"[备份] {bak}")
    for ext in ("-wal", "-shm"):
        p = Path(str(real) + ext)
        if p.exists():
            p.unlink()
    shutil.copy2(copy, real)
    print(f"[落地] {real}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
