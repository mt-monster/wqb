# -*- coding: utf-8 -*-
"""rebuild.py — 从事实表幂等重建 `attempt_knowledge`（2026-11-15）。

用途：
- 首次上线后回填历史波次；
- 验证“派生层可由事实表重建”这一不变量；
- 修复 capture 逻辑后重算。

只读事实表（backtest_results / expressions / ledger），只写 `attempt_knowledge`。
`--dry-run` 只构建不写行（注意：打开 CampaignStore 会执行幂等 `ensure_schema`，
新表/索引可能被创建——这是 additive DDL，不改变既有表）。

用法：
    python tools/knowledge/rebuild.py --region KOR --wave 101
    python tools/knowledge/rebuild.py --region KOR --all
    python tools/knowledge/rebuild.py --region KOR --all --dry-run --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _bootstrap():
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return parent
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


REPO_ROOT = _bootstrap()

from wqb.store import CampaignStore, default_db_path  # noqa: E402
from wqb.knowledge.capture import refresh_attempt_knowledge  # noqa: E402


def _waves(store, region):
    rows = store.connection.execute(
        "SELECT DISTINCT wave FROM backtest_results WHERE region=? ORDER BY wave", (region,)
    ).fetchall()
    return [str(r[0]) for r in rows if r[0] not in (None, "")]


def _prune(store, region: str, waves) -> int:
    """删除本批波次里已不在 backtest_results 的 attempt 行（重建必须与事实一致）。

    按 500 波分批：SQLite 默认变量上限 999，GBR 单区已 518 波，留余量。
    """
    total = 0
    for i in range(0, len(waves), 500):
        total += _prune_chunk(store, region, waves[i:i + 500])
    return total


def _prune_chunk(store, region: str, waves) -> int:
    if not waves:
        return 0
    q = ",".join("?" * len(waves))
    params = (region, *waves)
    facts = store.connection.execute(
        f"SELECT wave, alpha_id, expression_id FROM backtest_results "
        f"WHERE region=? AND wave IN ({q})", params).fetchall()
    valid = {}
    for w, aid, eid in facts:
        key = str(aid) if aid else f"expr:{eid}"
        valid.setdefault(str(w), set()).add(key)
    existing = store.connection.execute(
        f"SELECT attempt_id, wave FROM attempt_knowledge WHERE region=? AND wave IN ({q})",
        params).fetchall()
    stale = [(aid,) for aid, w in existing if aid not in valid.get(str(w), set())]
    if stale:
        cur = store.connection.cursor()
        cur.execute("BEGIN")
        try:
            cur.executemany("DELETE FROM attempt_knowledge WHERE attempt_id=?", stale)
            store.connection.commit()
        except Exception:
            store.connection.rollback()
            raise
    return len(stale)


def main() -> int:
    ap = argparse.ArgumentParser(description="从事实表重建 attempt_knowledge（幂等）")
    ap.add_argument("--region", required=True, help="区域（如 KOR）")
    ap.add_argument("--wave", action="append", default=[], help="波号，可多次传")
    ap.add_argument("--all", action="store_true", help="重建该区全部波（按 backtest_results 去重）")
    ap.add_argument("--dry-run", action="store_true", help="只构建不写行")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / data/wqb.db）")
    ap.add_argument("--no-prune", action="store_true",
                    help="不删除本批波次里已不在 backtest_results 的旧行（默认删除）")
    a = ap.parse_args()

    db = a.db or os.environ.get("WQB_DB_PATH") or default_db_path()
    if not os.path.isfile(db):
        print(f"[knowledge] 找不到 DB：{db}", file=sys.stderr)
        return 2
    store = CampaignStore(db)
    try:
        waves = _waves(store, a.region.upper()) if a.all else [str(w) for w in a.wave]
        if not waves:
            print("[knowledge] 没有可重建的波（传 --wave 或 --all）", file=sys.stderr)
            return 2
        out = []
        for w in waves:
            out.append(refresh_attempt_knowledge(
                store, a.region.upper(), w, dry_run=a.dry_run))
        pruned = 0 if (a.dry_run or a.no_prune) else _prune(store, a.region.upper(), waves)
    finally:
        store.close()

    if a.json:
        print(json.dumps({"db": db, "waves": out, "pruned": pruned}, ensure_ascii=False, indent=2))
    else:
        total = sum(x.get("written", 0) for x in out)
        print(f"[knowledge] rebuild region={a.region.upper()} waves={len(out)} "
              f"rows={total} pruned={pruned} dry_run={a.dry_run} db={db}")
        for x in out:
            print(f"  wave={x['wave']:<12} records={x['records']:<5} "
                  f"written={x['written']:<5} outcomes={x.get('outcomes')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
