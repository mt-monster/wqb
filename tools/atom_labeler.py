#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""atom_labeler.py — WorldQuant BRAIN "atom / combined" 信号分类器（CLI + 批量回写）。

判定口径的唯一实现见 ``src/wqb/expression/atom.py``（纯函数）；本工具只提供
DB 字段解析器（AtomResolver）与命令行入口：
  - 单表达式判定：--expr "rank(returns)"
  - 批量回写 expressions.atom_flag / atom_n_datasets：--backfill [--dry-run|--apply]
  - 自检：--selftest

判定规则：
  atom     = 单数据集（含纯基础行情信号）
  combined = 跨数据集（≥2 个 dataset）
  unknown  = 引用了未收录进 fields 表的数据字段（需刷新字段缓存）
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import sqlite3
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(REPO_ROOT, "data", "wqb.db")

# 经规范连接工厂打开 wqb.db（避免裸 sqlite3.connect 导致的 database is locked 事故）。
# 工具脚本直跑时 src/ 不在 sys.path，需显式插入仓库 src 目录。
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
from wqb import db_conn  # 全库唯一合规的 sqlite 连接入口（WAL + busy_timeout=60s）

# 复用库模块（单一口径源）
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
from wqb.expression.atom import (  # noqa: E402
    BASE_MARKET_FIELDS,
    BASE_MARKET_NAME,
    GROUPING_KEYS,
    RESERVED,
    classify_atom,
    classify_stale,
    extract_fields,
    strip_comments,
)

# 字段索引已完整扫描（prior Task B 结论：dry-run 待补=0）的区域；这些区里
# unknown 字段不在 fields 表即判定为平台已下架（stale_field）。其余区域
# （ASI/CHN/GBR/JPN）索引未完整，同名 unknown 可能是"本地未缓存"，标 unverified。
COMPLETE_REGIONS = {"USA", "GLB", "EUR", "DEU", "IND", "MEA", "KOR", "HKG"}


class AtomResolver:
    """字段 → 数据集 解析器（DB `fields` 表为主，base/grouping 内置，逐字段缓存）。"""

    def __init__(self, db_path: str = DEFAULT_DB):
        self.db_path = db_path
        self._conn = None
        self._cache: dict[str, str | None] = {}

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = db_conn.connect(self.db_path, row_factory=sqlite3.Row)
        return self._conn

    def resolve(self, field: str) -> tuple[str, str | None]:
        if field in BASE_MARKET_FIELDS:
            return ("base", BASE_MARKET_NAME)
        if field.lower() in GROUPING_KEYS:
            return ("grouping", None)
        if field in self._cache:
            ds = self._cache[field]
            return ("dataset", ds) if ds else ("unknown", None)
        row = self.conn.execute(
            "SELECT d.name FROM fields f JOIN datasets d ON d.id = f.dataset_id "
            "WHERE f.field_name = ? LIMIT 1",
            (field,),
        ).fetchone()
        ds = row["name"] if row else None
        self._cache[field] = ds
        return ("dataset", ds) if ds else ("unknown", None)

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None


def classify(expr: str, resolver: AtomResolver | None = None) -> dict:
    own = resolver is None
    if own:
        resolver = AtomResolver()
    try:
        return classify_atom(expr, {}, resolve=resolver.resolve)
    finally:
        if own:
            resolver.close()


# 兼容旧调用名
classify_atom_db = classify


def annotate_expressions_table(db_path: str = DEFAULT_DB, dry_run: bool = True,
                               limit: int | None = None,
                               stale_only: bool = False) -> dict:
    """批量回写 expressions 的 atom_flag / atom_n_datasets / stale_flag。

    stale_only=True 时只处理 atom_flag='unknown' 的行（数据清洗场景，避免重算全库）；
    否则全量重算。幂等建列、分批提交。
    """
    conn = db_conn.connect(db_path, row_factory=sqlite3.Row)
    try:
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(expressions)")}
        added = []
        for c, ddl in (("atom_flag", "VARCHAR(16)"),
                       ("atom_n_datasets", "INTEGER"),
                       ("stale_flag", "VARCHAR(16)")):
            if c not in cols:
                conn.execute(f"ALTER TABLE expressions ADD COLUMN {c} {ddl}")
                added.append(c)
        if added:
            conn.commit()

        resolver = AtomResolver(db_path)
        if stale_only:
            rows = conn.execute(
                "SELECT id, region, expression FROM expressions WHERE atom_flag='unknown'"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, region, expression FROM expressions WHERE expression IS NOT NULL"
            ).fetchall()
        if limit:
            rows = rows[:limit]
        stats = {"total": len(rows), "atom": 0, "combined": 0, "unknown": 0,
                 "empty": 0, "errors": 0,
                 "stale_field": 0, "dirty": 0, "stale_field_unverified": 0}
        combined_examples: list[dict] = []
        unknown_fields: dict[str, int] = {}
        BATCH = 2000
        pending = 0
        for r in rows:
            try:
                res = classify(r["expression"], resolver)
            except Exception as e:
                stats["errors"] += 1
                print(f"[warn] id={r['id']} 解析异常: {e}", file=sys.stderr)
                continue
            v = res["verdict"]
            stale = None
            if v == "atom":
                stats["atom"] += 1
            elif v == "combined":
                stats["combined"] += 1
                if len(combined_examples) < 20:
                    combined_examples.append({
                        "id": r["id"], "datasets": res["datasets"],
                        "expression": (r["expression"] or "")[:200]})
            elif v == "unknown":
                stats["unknown"] += 1
                for f in res["unknown_fields"]:
                    unknown_fields[f] = unknown_fields.get(f, 0) + 1
                stale = classify_stale(r["expression"], res["unknown_fields"])
                if stale == "stale_field":
                    reg = r["region"]
                    if reg is not None and reg not in COMPLETE_REGIONS:
                        stale = "stale_field_unverified"
                stats[stale] += 1
            else:
                stats["empty"] += 1
            if not dry_run:
                conn.execute(
                    "UPDATE expressions SET atom_flag=?, atom_n_datasets=?, stale_flag=? WHERE id=?",
                    (v, res["n_datasets"], stale, r["id"]))
                pending += 1
                if pending >= BATCH:
                    conn.commit()
                    pending = 0
        if not dry_run and pending:
            conn.commit()
        stats["combined_examples"] = combined_examples
        stats["top_unknown_fields"] = sorted(unknown_fields.items(), key=lambda kv: -kv[1])[:20]
        stats["added_columns"] = added
        return stats
    finally:
        conn.close()


def _selftest() -> int:
    cases = [
        ("rank(returns)", "atom"),
        ("abs(volume)", "atom"),
        ("log(close)", "atom"),
        ("rank(anl14_actvalue_bvps_fp0)", "atom"),
        ("anl14_fieldA - anl14_fieldB", "atom"),
        ("group_rank(anl14_x, industry)", "atom"),
        ("ts_co_skewness(news_session_range_pct, returns, 20)", "combined"),
        ("regression_neut(anl14_x, pv_y)", "combined"),
        ("ts_corr(anl14_x, macro_y, 20)", "combined"),
        # 修复用例：kwarg / 字符串值 / 多行变量 不应被当作字段
        ('quantile(subtract(fnd86_a, fnd86_b), driver="gaussian", sigma=1.0)', "atom"),
        ('group_rank(fnd86_x, bucket(rank(fnd86_b), buckets="2,5,6,7,10"))', "atom"),
        ("rank(ts_regression(fnd86_a, ts_delay(fnd86_b, 5), 66, lag=0, rettype=0))", "atom"),
        # 跨数据集仍应 combined（证明 kwarg/字符串被排除后只剩真字段）
        ('group_rank(fnd86_x, bucket(rank(fnd93_y), buckets="2,5,6,7,10"))', "combined"),
        ("M5 = close;\nB = volume;\nadd(M5, B)", "atom"),
        ("A = anl14_x;\nD90_22 = pv_y;\nadd(A, D90_22)", "combined"),
    ]

    class FakeResolver(AtomResolver):
        _FAKE = {
            "returns": ("base", "BASE_MARKET"), "volume": ("base", "BASE_MARKET"),
            "close": ("base", "BASE_MARKET"), "industry": ("grouping", None),
            "anl14_actvalue_bvps_fp0": ("dataset", "analyst14"),
            "anl14_fieldA": ("dataset", "analyst14"), "anl14_fieldB": ("dataset", "analyst14"),
            "anl14_x": ("dataset", "analyst14"),
            "news_session_range_pct": ("dataset", "news104"),
            "pv_y": ("dataset", "pv29"), "macro_y": ("dataset", "macro12"),
            "fnd86_a": ("dataset", "fundamental86"), "fnd86_b": ("dataset", "fundamental86"),
            "fnd86_x": ("dataset", "fundamental86"), "fnd93_y": ("dataset", "fundamental93"),
            "a": ("dataset", "dsA"), "b": ("dataset", "dsB"),
        }

        def resolve(self, field):
            if field in self._FAKE:
                return self._FAKE[field]
            return super().resolve(field)

    ok = 0
    for expr, expect in cases:
        res = classify(expr, FakeResolver(":memory:"))
        got = res["verdict"]
        mark = "OK " if got == expect else "FAIL"
        if got == expect:
            ok += 1
        print(f"[{mark}] expect={expect:8s} got={got:8s} n_ds={res['n_datasets']}  {expr[:70]}")
    print(f"\nselftest: {ok}/{len(cases)} passed")
    return 0 if ok == len(cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="WorldQuant atom/combined 信号分类器")
    ap.add_argument("--expr", help="判定单条表达式")
    ap.add_argument("--backfill", action="store_true", help="批量回写 expressions 表")
    ap.add_argument("--stale-only", action="store_true",
                    help="只处理 atom_flag='unknown' 的行（数据清洗，避免重算全库）")
    ap.add_argument("--dry-run", action="store_true", help="只统计不写库（backfill 默认）")
    ap.add_argument("--apply", action="store_true", help="真正写库（backfill 时）")
    ap.add_argument("--limit", type=int, help="backfill 限制行数（调试用）")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return _selftest()

    if a.expr:
        print(json.dumps(classify(a.expr), ensure_ascii=False, indent=1))
        return 0

    if a.backfill:
        dry = not a.apply
        mode = "stale-only" if a.stale_only else "full"
        if not dry:
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup = f"{a.db}.bak_atom_{stamp}"
            shutil.copy2(a.db, backup)
            print(f"[backup] {backup}")
        stats = annotate_expressions_table(a.db, dry_run=dry, limit=a.limit,
                                           stale_only=a.stale_only)
        print(f"[backfill:{mode}] total={stats['total']} atom={stats['atom']} "
              f"combined={stats['combined']} unknown={stats['unknown']} "
              f"empty={stats['empty']} errors={stats['errors']}")
        if stats["unknown"]:
            print(f"[backfill:{mode}] stale 细分: "
                  f"stale_field={stats['stale_field']} "
                  f"dirty={stats['dirty']} "
                  f"stale_field_unverified={stats['stale_field_unverified']}")
        print(f"[backfill:{mode}] added_columns={stats.get('added_columns')} "
              f"{'(dry-run)' if dry else '(applied)'}")
        if stats.get("top_unknown_fields"):
            print("--- unknown 高频字段（若为 kwarg/变量则是抽取遗漏，否则是缓存缺口）---")
            for f, c in stats["top_unknown_fields"]:
                print(f"  {f} x{c}")
        if stats.get("combined_examples"):
            print("--- combined 示例 ---")
            for ex in stats["combined_examples"][:5]:
                print(f"  id={ex['id']} datasets={ex['datasets']}")
                print(f"    {ex['expression']}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
