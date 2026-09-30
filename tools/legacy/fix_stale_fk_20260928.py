#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""fix_stale_fk_20260928.py — 修复 P0 迁移遗留的悬空外键（2026-09-28）。

症状：任何 INSERT 到 expressions/backtest_results 报
  `sqlite3.OperationalError: no such table: main.waves_old`
  `sqlite3.OperationalError: no such table: main.expressions_old`

根因：P0 迁移把 `waves`/`expressions` 改名→新建同名表（表重建型迁移），
但**忘了把引用方表的外键从旧名改到新名**：
  - expressions.wave_id        REFERENCES "waves_old"(id)      ← waves_old 已不存在
  - backtest_results.expres...  REFERENCES "expressions_old"(id) ← expressions_old 已不存在
SQLite 在 prepare 阶段解析外键目标，目标表不存在即报错 —— 与 `PRAGMA foreign_keys`
开关无关，所以不是"关掉 FK 检查"能绕过的。

修法：按依赖顺序（先 expressions 后 backtest_results）重建两表，仅把外键目标名改成现行表名，
其余 DDL 原样保留，并重建其索引。全程：
  1) 先在**副本**上执行 + 校验（integrity_check / 行数 / 试插入 / FK 目标解析）
  2) 校验通过且 `--apply` 才动真实库（先自动备份）

用法:
  python tools/fix_stale_fk_20260928.py --db data/wqb.db            # 仅在副本上验证
  python tools/fix_stale_fk_20260928.py --db data/wqb.db --apply    # 校验通过后落地
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

# 表名 -> (悬空旧名, 现行新名)
FK_FIX = {
    "expressions": ("waves_old", "waves"),
    "backtest_results": ("expressions_old", "expressions"),
}
# 依赖顺序：被引用者先修
ORDER = ["expressions", "backtest_results"]


def _schema(conn, kind, name):
    r = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type=? AND name=?", (kind, name)).fetchone()
    return r[0] if r else None


def _indexes(conn, table):
    return [r[0] for r in conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL",
        (table,))]


def _patch_fk(ddl: str, old: str, new: str) -> str:
    """把 DDL 里对 old 表的外键目标改成 new（保留原引号风格）。"""
    pat = re.compile(r'REFERENCES\s+(["\']?)%s\1\s*\(' % re.escape(old), re.I)
    if not pat.search(ddl):
        # 也尝试不带引号的形式
        pat = re.compile(r'REFERENCES\s+%s\s*\(' % re.escape(old), re.I)
    return pat.sub(lambda m: 'REFERENCES "%s"(' % new, ddl, count=1)


def rebuild(conn, table, old, new, *, dry=True):
    ddl = _schema(conn, "table", table)
    if not ddl:
        return f"[skip] {table} 不存在"
    if old not in ddl:
        return f"[skip] {table} DDL 未引用 {old}"
    new_ddl = _patch_fk(ddl, old, new)

    idx = _indexes(conn, table)
    n_before = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]

    # 依赖该表的**视图**必须先卸下：DROP TABLE 时 SQLite 会校验视图有效性，
    # 视图指向已删表 → `error in view ...: no such table`（2026-09-28 实证）。
    # 卸载 → 重建表 → 原样恢复视图。
    views = [(r[0], r[1]) for r in conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view' AND sql IS NOT NULL")]
    dependent = [(n, s) for n, s in views
                 if re.search(r'\b%s\b' % re.escape(table), s or "", re.I)]

    tmp = f"{table}__fkfix"
    stmts = [f"DROP VIEW IF EXISTS \"{n}\"" for n, _ in dependent]
    stmts += [
        f"DROP TABLE IF EXISTS {tmp}",
        _patch_fk(re.sub(r'^CREATE\s+TABLE\s+["\']?%s["\']?' % re.escape(table),
                         f'CREATE TABLE {tmp}', new_ddl, flags=re.I), old, new),
        f"INSERT INTO {tmp} ({','.join(cols)}) SELECT {','.join(cols)} FROM {table}",
        f"DROP TABLE {table}",
        f"ALTER TABLE {tmp} RENAME TO {table}",
    ]
    stmts += [_patch_fk(s.replace(table, table, 1), old, new) for s in idx]
    stmts += [s for _, s in dependent]

    conn.execute("PRAGMA foreign_keys=OFF")
    for s in stmts:
        conn.execute(s)
    n_after = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.commit()
    return (f"[fix ] {table}: FK {old} -> {new}；行数 {n_before} -> {n_after}；"
            f"索引 {len(idx)} 个 + 依赖视图 {len(dependent)} 个已重建；"
            f"{'行数一致 OK' if n_before == n_after else '★行数不一致!!'}")


def verify(conn):
    out = []
    out.append(("integrity_check", conn.execute("PRAGMA integrity_check").fetchall()[:1]))
    for t in ORDER + ["waves", "alphas", "ledger_kv"]:
        try:
            out.append((f"count {t}", conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]))
        except Exception as e:
            out.append((f"count {t}", f"ERR {e}"))
    # 试插入（回滚，不留痕）—— 验证 prepare 阶段外键解析已通过
    try:
        conn.execute("BEGIN")
        wid = conn.execute("SELECT id FROM waves LIMIT 1").fetchone()
        eid = conn.execute("SELECT id FROM expressions LIMIT 1").fetchone()
        if wid and eid:
            conn.execute("INSERT INTO expressions (wave_id, expression) VALUES (?,?)",
                         (wid[0], "__fk_probe__"))
            conn.execute("INSERT INTO backtest_results (expression_id, alpha_id) VALUES (?,?)",
                         (eid[0], "__fk_probe__"))
        conn.execute("ROLLBACK")
        out.append(("试插入 expressions+backtest_results", "OK（已回滚）"))
    except Exception as e:
        try:
            conn.execute("ROLLBACK")
        except Exception:
            pass
        out.append(("试插入", f"ERR {type(e).__name__}: {e}"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/wqb.db")
    ap.add_argument("--apply", action="store_true", help="校验通过后落地真实库（先自动备份）")
    a = ap.parse_args()

    real = (REPO / a.db) if not Path(a.db).is_absolute() else Path(a.db)
    if not real.exists():
        print(f"[ERR] 找不到 {real}")
        return 1

    work = REPO / "cache" / "_dbrepair" / f"fkfix_{time.strftime('%H%M%S')}"
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
        for t in ORDER:
            old, new = FK_FIX[t]
            print("  " + rebuild(conn, t, old, new))
        print("\n[副本校验]")
        rows = verify(conn)
        for k, v in rows:
            print(f"  {k:<42} {v}")
        ok = (rows[0][1] == [("ok",)] and
              all("ERR" not in str(v) for _, v in rows) and
              all("ERR" not in str(v) for _, v in rows) and
              "OK" in str(dict(rows).get("试插入 expressions+backtest_results", "")))
    finally:
        conn.close()

    if not ok:
        print("\n[中止] 副本校验未通过，不动真实库。")
        return 1
    print("\n[副本校验通过]")
    if not a.apply:
        print("（未加 --apply，未改动真实库）")
        return 0

    bak = real.with_name(real.name + f".bak_fkfix_{time.strftime('%Y%m%d_%H%M%S')}")
    shutil.copy2(real, bak)
    print(f"[备份] {bak}")

    # 落地：把修好的副本覆盖回真实库，并清掉 WAL/SHM（副本已 checkpoint）
    for ext in ("-wal", "-shm"):
        p = Path(str(real) + ext)
        if p.exists():
            p.unlink()
    shutil.copy2(copy, real)
    print(f"[落地] {real}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
