# -*- coding: utf-8 -*-
"""datasets 表伪数据集行修复器（2026-11-06 新增）。

问题
====
CampaignStore._ensure_dataset(region, name) 会按传入的**任意字符串**现建
datasets 行，而 _ensure_wave / _backtest 把**塔位组合标签**、**表达式描述**、
**region 名**原样透传进去 —— 于是 datasets 表里混进了 'risk/model'、
'pv/model/other'、'fundamental44|institutions6'、'KOR' 这类**从来不是数据集**
的行。

实测规模（2026-11-06，data/wqb.db）
----------------------------------
- 非 id 形 96 行 = 14 个 '_unknown' 哨兵（**合法**，store 刻意使用）+ 82 行真脏；
- 脏行挂着 alphas 261 条 / waves 79 条 / field_profile 4 条外键引用
  => **不能直接 DELETE**（alphas.dataset_id 是 NOT NULL）；
- 任何「按 datasets 表统计」的结论都会被这些行污染（集数排名、category 分布、
  覆盖度分母…）。

修法（五步，同一事务）
----------------------
1. **归档**：脏行的 name / region / 各表引用计数落 datasets_phantom_archive
   （保审计痕迹，不是静默删除）。
2. **补哨兵**：缺 '_unknown' 的区先补建该行。
3. **重指向**：所有指向 datasets.id 的外键列（PRAGMA 动态发现，不只 alphas /
   waves / field_profile / fields 这四张）改指本区哨兵。「未知」比假名诚实 ——
   同 tools/data-repair/backfill_expression_dataset.py。
4. **删除**活表行。
5. **洗白** expressions.dataset：等于脏名的行置 NULL
   （--keep-expression-dataset 关闭此步）。

判定口径
--------
真数据集 id 形状 = ^[a-z][a-z0-9_]*$，单一来源 wqb.config.is_phantom_dataset_name
（写入口 _ensure_dataset 用的是同一个函数，两侧不会漂）。
本脚本只认**形状**；id 形的假名（例：region 名写成小写）需要平台目录才能识破 ——
走 tools/gates/category_coverage_audit.py --show-extra-local，其 extra_local
即「本地有、平台无」的差集。

用法
====
    # 只出报告，不写库（默认）
    python tools/db/datasets_phantom_repair.py

    # 真修：一致性备份 -> 归档 -> 重指向 -> 删除 -> 洗白 expressions
    python tools/db/datasets_phantom_repair.py --apply

    # 机器可读
    python tools/db/datasets_phantom_repair.py --json

退出码
------
0 无需修复 / 修复成功；1 发现脏行但未给 --apply；2 库不存在 / 备份失败 / 拒绝执行。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_HERE = Path(__file__).resolve()


def _bootstrap_src() -> Path:
    """把仓库 src/ 塞进 sys.path —— 向上探测，不数层数（AGENTS.md §8.13）。"""
    for parent in _HERE.parents:
        if (parent / "src" / "wqb").is_dir():
            return parent / "src"
    raise RuntimeError(f"未能在 {_HERE} 之上找到 src/wqb（不在本工作区内运行？）")


_SRC = _bootstrap_src()
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from wqb.config import DATASET_SENTINEL, is_phantom_dataset_name  # noqa: E402
from wqb.db_conn import connect as db_connect                     # noqa: E402
from wqb.db_write_lock import write_lock                          # noqa: E402
from wqb.paths import find_repo_root                              # noqa: E402

ARCHIVE_TABLE = "datasets_phantom_archive"

ARCHIVE_DDL = """
CREATE TABLE IF NOT EXISTS datasets_phantom_archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    category TEXT,
    status TEXT,
    refs_json TEXT NOT NULL DEFAULT '{}',
    repointed_to INTEGER,
    repointed_to_name TEXT NOT NULL DEFAULT '_unknown',
    archived_at TEXT NOT NULL,
    note TEXT
);
CREATE INDEX IF NOT EXISTS idx_dpa_region_name
    ON datasets_phantom_archive(region, name);
"""


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _table_exists(cur, table: str) -> bool:
    cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cur.fetchone() is not None


def dataset_fk_columns(cur) -> List[Tuple[str, str]]:
    """枚举所有指向 datasets 的外键列 (表, 列)。

    动态发现而不是硬编码 [alphas, waves, field_profile, fields]：将来新增
    「引用 dataset」的表若被漏掉，DELETE 会撞 FK（PRAGMA foreign_keys 默认 OFF
    时则静默留下悬挂引用 —— 更糟）。PRAGMA 读的是库里的真实外键定义。
    """
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    out: List[Tuple[str, str]] = []
    for (t,) in cur.fetchall():
        try:
            fks = cur.execute(f'PRAGMA foreign_key_list("{t}")').fetchall()
        except Exception:  # noqa: BLE001 - 视图 / 虚拟表不响应 PRAGMA
            continue
        for fk in fks:
            # (id, seq, table, from, to, on_update, on_delete, match)
            if fk[2] == "datasets":
                out.append((t, fk[3]))
    return out


def collect_rows(cur) -> List[Dict[str, Any]]:
    """列出 datasets 表全部行（带 region 名）。"""
    cur.execute(
        "SELECT d.id, d.name, r.name, d.category, d.status "
        "FROM datasets d JOIN regions r ON r.id = d.region_id "
        "ORDER BY r.name, d.name"
    )
    return [
        {"id": int(i), "name": n or "", "region": reg, "category": cat, "status": st}
        for (i, n, reg, cat, st) in cur.fetchall()
    ]


def build_plan(cur, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """出修复计划：脏行清单 + 各表引用计数 + expressions 命中 + 缺哨兵的区。"""
    sentinels = [r for r in rows if r["name"] == DATASET_SENTINEL]
    dirty = [
        r for r in rows
        if r["name"] != DATASET_SENTINEL and is_phantom_dataset_name(r["name"])
    ]
    dirty_ids = [r["id"] for r in dirty]
    fks = dataset_fk_columns(cur)

    refs: Dict[str, Dict[int, int]] = {}
    if dirty_ids:
        holes = ",".join("?" * len(dirty_ids))
        for table, col in fks:
            try:
                cur.execute(
                    f'SELECT "{col}", COUNT(*) FROM "{table}" '
                    f'WHERE "{col}" IN ({holes}) GROUP BY "{col}"',
                    dirty_ids,
                )
                refs[f"{table}.{col}"] = {int(k): int(c) for k, c in cur.fetchall()}
            except Exception:  # noqa: BLE001 - 表结构异常不应阻断计划生成
                refs[f"{table}.{col}"] = {}

    expr_hits: Dict[str, int] = {}
    if dirty_ids and _table_exists(cur, "expressions"):
        holes = ",".join("?" * len(dirty_ids))
        cur.execute(
            f"SELECT dataset, COUNT(*) FROM expressions "
            f"WHERE dataset IN ({holes}) GROUP BY dataset",
            [r["name"] for r in dirty],
        )
        expr_hits = {str(k): int(c) for k, c in cur.fetchall()}

    have_sentinel = {r["region"] for r in sentinels}
    need_sentinel = sorted({r["region"] for r in dirty} - have_sentinel)

    return {
        "datasets_total": len(rows),
        "sentinel_rows": len(sentinels),
        "sentinel_regions": sorted(have_sentinel),
        "phantom_rows": len(dirty),
        "phantom_by_region": dict(Counter(r["region"] for r in dirty).most_common()),
        "phantom_names": sorted({r["name"] for r in dirty}),
        "ref_columns": [f"{t}.{c}" for t, c in fks],
        "refs": {k: sum(v.values()) for k, v in refs.items()},
        "expression_hits": expr_hits,
        "regions_missing_sentinel": need_sentinel,
        "_dirty": dirty,
    }


def _ensure_sentinel(cur, region: str, now: str) -> int:
    """取该区 '_unknown' 哨兵行 id，缺则补建。"""
    cur.execute(
        "SELECT d.id FROM datasets d JOIN regions r ON r.id = d.region_id "
        "WHERE r.name=? AND d.name=?",
        (region, DATASET_SENTINEL),
    )
    row = cur.fetchone()
    if row:
        return int(row[0])
    cur.execute("SELECT id FROM regions WHERE name=?", (region,))
    rid_row = cur.fetchone()
    if not rid_row:
        raise RuntimeError(f"region 不存在: {region}")
    cur.execute(
        "INSERT INTO datasets (name, region_id, created_at, updated_at) VALUES (?,?,?,?)",
        (DATASET_SENTINEL, int(rid_row[0]), now, now),
    )
    return int(cur.lastrowid)


def apply_repair(cur, plan: Dict[str, Any], *, scrub_expressions: bool) -> Dict[str, Any]:
    """归档 -> 补哨兵 -> 重指向 -> 删除 -> 洗白 expressions。调用方负责 commit。"""
    now = _now()
    cur.executescript(ARCHIVE_DDL)

    dirty: List[Dict[str, Any]] = plan["_dirty"]
    if not dirty:
        return {"archived": 0, "repointed": {}, "deleted": 0, "expressions_scrubbed": 0}

    fks = dataset_fk_columns(cur)
    by_region: Dict[str, List[Dict[str, Any]]] = {}
    for r in dirty:
        by_region.setdefault(r["region"], []).append(r)

    archived = 0
    repointed: Dict[str, int] = {}
    deleted = 0
    for region, rows in by_region.items():
        sentinel_id = _ensure_sentinel(cur, region, now)
        ids = [r["id"] for r in rows]
        holes = ",".join("?" * len(ids))

        # 1) 归档（含各表引用计数）
        refs_json: Dict[str, Any] = {}
        for table, col in fks:
            cur.execute(
                f'SELECT COUNT(*) FROM "{table}" WHERE "{col}" IN ({holes})', ids
            )
            refs_json[f"{table}.{col}"] = int(cur.fetchone()[0])
        for r in rows:
            cur.execute(
                f"INSERT INTO {ARCHIVE_TABLE} "
                "(dataset_id, name, region, category, status, refs_json, "
                " repointed_to, repointed_to_name, archived_at, note) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    r["id"], r["name"], region, r["category"], r["status"],
                    json.dumps(refs_json, ensure_ascii=False),
                    sentinel_id, DATASET_SENTINEL, now,
                    "name 不合平台 dataset id 形状，判为伪数据集行",
                ),
            )
            archived += 1

        # 2) 重指向所有外键列（必须先于 DELETE：alphas.dataset_id 是 NOT NULL，
        #    且 PRAGMA foreign_keys 默认 OFF 时删了也不会报错，只会留悬挂引用）
        for table, col in fks:
            cur.execute(
                f'UPDATE "{table}" SET "{col}"=? WHERE "{col}" IN ({holes})',
                [sentinel_id] + ids,
            )
            if cur.rowcount:
                key = f"{table}.{col}"
                repointed[key] = repointed.get(key, 0) + int(cur.rowcount)

        # 3) 删除活表行
        cur.execute(f"DELETE FROM datasets WHERE id IN ({holes})", ids)
        deleted += int(cur.rowcount)

    scrubbed = 0
    if scrub_expressions and plan["expression_hits"] and _table_exists(cur, "expressions"):
        names = list(plan["expression_hits"].keys())
        holes = ",".join("?" * len(names))
        cur.execute(
            f"UPDATE expressions SET dataset=NULL, updated_at=? "
            f"WHERE dataset IN ({holes})",
            [now] + names,
        )
        scrubbed = int(cur.rowcount)

    return {
        "archived": archived,
        "repointed": repointed,
        "deleted": deleted,
        "expressions_scrubbed": scrubbed,
    }


def backup_db(db: Path, *, tag: str = "phantom") -> Path:
    """SQLite 一致性快照备份（sqlite3 backup API，不用 copy2）。

    为什么不用 shutil.copy2：wqb.db 是共享资产，其他会话可能正在写；直接拷
    文件可能拿到「主文件已改、WAL 未盖」的撕裂快照 —— 备份看着有、恢复时缺页。
    backup API 走的是事务一致性读取。
    """
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = db.with_name(f"{db.name}.bak_{tag}_{stamp}")
    src = db_connect(str(db), readonly=True)
    try:
        dst = db_connect(str(bak))
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
    return bak


def _emit(report: Dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return
    print(f"库: {report['db']}")
    print("-" * 64)
    print(f"datasets 总行数           : {report['datasets_total']}")
    print(f"  '_unknown' 哨兵（合法）  : {report['sentinel_rows']} "
          f"（{len(report['sentinel_regions'])} 个区）")
    print(f"  伪数据集行（真脏）       : {report['phantom_rows']}")
    if report["regions_missing_sentinel"]:
        print(f"  缺哨兵需补建的区         : {report['regions_missing_sentinel']}")
    if report["phantom_by_region"]:
        print("按区分布:")
        for region, n in report["phantom_by_region"].items():
            print(f"  {region:<12} {n}")
    if report["refs"]:
        print("脏行持有引用（修复后改指本区哨兵）:")
        for key, n in report["refs"].items():
            print(f"  {key:<28} {n}")
    if report["expression_hits"]:
        total = sum(report["expression_hits"].values())
        print(f"expressions.dataset 命中脏名 : {total} 条（{len(report['expression_hits'])} 个名字）")
    if report.get("phantom_names"):
        print("脏名样本（最多 10 个）:")
        for n in report["phantom_names"][:10]:
            print(f"  - {n}")
    if report.get("applied") is not None:
        print("-" * 64)
        if report.get("backup"):
            print(f"备份: {report['backup']}")
        if report["applied"]:
            res = report.get("result") or {}
            print(f"已归档 {res.get('archived', 0)} 行 / 删除 {res.get('deleted', 0)} 行")
            if res.get("repointed"):
                for k, v in sorted(res["repointed"].items()):
                    print(f"  重指向 {k}: {v}")
            print(f"expressions 洗白: {res.get('expressions_scrubbed', 0)} 行")
            print(f"修复后复检伪数据集行: {report.get('phantom_rows_after')}")
        else:
            print("未写库（缺 --apply）。")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="修复 datasets 表的伪数据集行（归档 + 重指向 + 删除 + 洗白 expressions）"
    )
    ap.add_argument("--db", default=None, help="缺省 <仓库根>/data/wqb.db")
    ap.add_argument("--apply", action="store_true", help="真正写库；缺省只出报告")
    ap.add_argument("--keep-expression-dataset", action="store_true",
                    help="不洗白 expressions.dataset（缺省会置 NULL）")
    ap.add_argument("--no-backup", action="store_true",
                    help="跳过备份（仅限沙箱 / 测试库，生产库会被拒绝）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    a = ap.parse_args(argv)

    prod = (find_repo_root(_HERE) / "data" / "wqb.db").resolve()
    db = Path(a.db).resolve() if a.db else prod
    if not db.is_file():
        print(f"[FATAL] 数据库不存在: {db}", file=sys.stderr)
        return 2
    if a.no_backup and db == prod:
        print("[FATAL] --no-backup 不允许对生产库使用（备份是唯一的回滚路径）",
              file=sys.stderr)
        return 2

    scrub = not a.keep_expression_dataset

    if not a.apply:
        conn = db_connect(str(db), readonly=True)
        try:
            plan = build_plan(conn.cursor(), collect_rows(conn.cursor()))
        finally:
            conn.close()
        report = {"db": str(db), "applied": False, "backup": None}
        report.update({k: v for k, v in plan.items() if not k.startswith("_")})
        _emit(report, as_json=a.json)
        return 1 if plan["phantom_rows"] else 0

    with write_lock(tag="datasets_phantom_repair", ttl_sec=900):
        backup: Optional[Path] = None
        if not a.no_backup:
            try:
                backup = backup_db(db)
            except Exception as exc:  # noqa: BLE001
                print(f"[FATAL] 备份失败，拒绝写库: {exc}", file=sys.stderr)
                return 2

        conn = db_connect(str(db))
        try:
            cur = conn.cursor()
            plan = build_plan(cur, collect_rows(cur))
            result: Dict[str, Any] = {}
            if plan["phantom_rows"]:
                result = apply_repair(cur, plan, scrub_expressions=scrub)
                conn.commit()
            phantom_after = None
            after = build_plan(cur, collect_rows(cur))
            phantom_after = after["phantom_rows"]
        finally:
            conn.close()

        report = {"db": str(db), "applied": True,
                  "backup": str(backup) if backup else None, "result": result}
        report.update({k: v for k, v in plan.items() if not k.startswith("_")})
        report["phantom_rows_after"] = phantom_after
        _emit(report, as_json=a.json)
        return 0 if phantom_after == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
