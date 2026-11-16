# -*- coding: utf-8 -*-
"""distill.py — 波级 / 区域级经验蒸馏 CLI（2026-11-15）。

- `--wave W`：蒸馏单波，打印 `wave_lessons`；
- 不传 `--wave`：只看区域累计统计（`distill_region`）；
- `--publish`：写 `wave_lessons_<R>_<W>`（区域快照不写）/ `region_kb.family_stats` /
  `experience_proposals_<R>` / `KB/template_kb.measured_*`；
- 不传 `--wave` 时做区域快照：proposals 与 measured templates 会刷新，但**不推进规则生命周期**；
- `--dry-run`：只算不写（`--publish` 被忽略）。

用法：
    python tools/knowledge/distill.py --region KOR --wave 101
    python tools/knowledge/distill.py --region KOR --wave 101 --publish
    python tools/knowledge/distill.py --region KOR --json
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
from wqb.knowledge.distill import distill_region, distill_wave, publish_region_stats  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="波级 / 区域级经验蒸馏")
    ap.add_argument("--region", required=True, help="区域（如 KOR）")
    ap.add_argument("--wave", default=None, help="波号；缺省只做区域累计统计")
    ap.add_argument("--publish", action="store_true", help="写 ledger（wave_lessons / region_kb / proposals）")
    ap.add_argument("--dry-run", action="store_true", help="只算不写（覆盖 --publish）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / data/wqb.db）")
    a = ap.parse_args()

    db = a.db or os.environ.get("WQB_DB_PATH") or default_db_path()
    if not os.path.isfile(db):
        print(f"[knowledge] 找不到 DB：{db}", file=sys.stderr)
        return 2
    store = CampaignStore(db)
    try:
        if a.wave:
            lesson = distill_wave(store, a.region, a.wave)
            result = {"wave_lessons": lesson}
            if a.publish and not a.dry_run:
                result["published"] = publish_region_stats(store, a.region, lesson)
        else:
            region_stats = distill_region(store, a.region)
            result = {"region_stats": region_stats}
            if a.publish and not a.dry_run:
                lesson = dict(region_stats)
                lesson["wave"] = "region"
                # publish 子模块统一用 by_family/by_skeleton（与 distill_wave 同形）
                lesson["by_family"] = region_stats.get("family_stats") or []
                lesson["by_skeleton"] = region_stats.get("skeleton_stats") or []
                result["published"] = publish_region_stats(store, a.region, lesson)
    finally:
        store.close()

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        lesson = result.get("wave_lessons")
        if lesson:
            print(f"[knowledge] wave={lesson['wave']} n={lesson['n_attempts']} "
                  f"outcomes={lesson.get('outcome_mix')} kv={lesson.get('knowledge_version')}")
            print(f"  by_family={len(lesson.get('by_family') or [])} "
                  f"by_skeleton={len(lesson.get('by_skeleton') or [])} "
                  f"dead_families={len((lesson.get('proposals') or {}).get('dead_families') or [])} "
                  f"dead_skeletons={len((lesson.get('proposals') or {}).get('dead_skeletons') or [])}")
        stats = result.get("region_stats")
        if stats:
            print(f"[knowledge] region={stats['region']} sample={stats['sample_size']} "
                  f"families={len(stats['family_stats'])} skeletons={len(stats['skeleton_stats'])}")
        pub = result.get("published")
        if pub:
            print(f"[knowledge] published={json.dumps(pub, ensure_ascii=False)}")
        elif a.publish and a.dry_run:
            print("[knowledge] --dry-run：跳过 publish")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
