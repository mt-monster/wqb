# -*- coding: utf-8 -*-
"""yield_report.py — 知识版本产出率报告（2026-11-15 P4）。

按 `attempt_knowledge.knowledge_version` 分组，输出每版的 win/near/dead 率、最高/平均 |S|、
prod/self clean 率，并写 `output_report/experience_yield_<region>_<YYYYMMDD>.md` 与
ledger `experience_yield_<region>`。

用法：
    python tools/knowledge/yield_report.py --region KOR
    python tools/knowledge/yield_report.py --region KOR --dry-run --json
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
from wqb.knowledge.yield_report import compute_yield, write_yield_report  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="知识版本产出率报告")
    ap.add_argument("--region", required=True)
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / data/wqb.db）")
    ap.add_argument("--out-dir", default=os.path.join(str(REPO_ROOT), "output_report"))
    ap.add_argument("--dry-run", action="store_true", help="只算不写（不落文件、不写 ledger）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    db = a.db or os.environ.get("WQB_DB_PATH") or default_db_path()
    if not os.path.isfile(db):
        print(f"[knowledge] 找不到 DB：{db}", file=sys.stderr)
        return 2
    store = CampaignStore(db)
    try:
        if a.dry_run:
            out = {"report": compute_yield(store, a.region), "path": None}
        else:
            out = write_yield_report(store, a.region, a.out_dir)
    finally:
        store.close()

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        r = out["report"]
        print(f"[knowledge] region={r['region']} sample={r['sample_size']} "
              f"versions={len(r['versions'])}")
        for v in r["versions"][:8]:
            print(f"  {v['knowledge_version']:<20} n={v['n']:<5} win={v['win_rate']:.1%} "
                  f"near={v['near_rate']:.1%} dead={v['dead_rate']:.1%} "
                  f"max|S|={v['max_abs_sharpe']:.2f}")
        if out.get("path"):
            print(f"  report -> {out['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
