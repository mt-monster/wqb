# -*- coding: utf-8 -*-
"""digest.py — 区域经验摘要（2026-11-15 P4）。

生成 `tracking/<REGION>/priors/experience_digest.md`：机器段可刷新，标记外人工笔记保留。

用法：
    python tools/knowledge/digest.py --region KOR
    python tools/knowledge/digest.py --region KOR --dry-run --print
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
from wqb.knowledge.digest import render_digest, write_region_digest  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="区域经验摘要")
    ap.add_argument("--region", required=True)
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / data/wqb.db）")
    ap.add_argument("--path", default=None,
                    help="输出路径（缺省 tracking/<REGION>/priors/experience_digest.md）")
    ap.add_argument("--dry-run", action="store_true", help="只渲染不写")
    ap.add_argument("--print", action="store_true", help="把渲染内容打到 stdout")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    db = a.db or os.environ.get("WQB_DB_PATH") or default_db_path()
    if not os.path.isfile(db):
        print(f"[knowledge] 找不到 DB：{db}", file=sys.stderr)
        return 2
    region = a.region.upper()
    path = a.path or os.path.join(str(REPO_ROOT), "tracking", region, "priors",
                                  "experience_digest.md")
    store = CampaignStore(db)
    try:
        if a.dry_run:
            content = render_digest(store, region)
            out = {"path": path, "dry_run": True, "chars": len(content)}
        else:
            out = write_region_digest(store, region, path)
            content = None
    finally:
        store.close()

    if a.print and content:
        print(content)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif not a.print:
        print(f"[knowledge] region={region} digest -> {out['path']}"
              + ("（dry-run）" if a.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
