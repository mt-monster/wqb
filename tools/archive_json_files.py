# -*- coding: utf-8 -*-
"""archive_json_files.py - 把已迁 DB 的 JSON 文件归档到 attic（移出活跃路径，不删除）。

归档目标：attic/json_archive_2026-08-21/
  - campaign_registry.json + .bak-p1 + registry/ 目录
  - tracking/<REGION>/*_d1_campaign_state.json（9 个）
  - tracking/<REGION>/results/wave*_results.json + _archive/（保留目录结构）

用法：
  python tools/archive_json_files.py --dry-run
  python tools/archive_json_files.py
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "attic" / "json_archive_2026-08-21"


def move(src, dst_root, dry_run, rel_base=ROOT):
    """移动文件/目录到归档，保留相对路径。"""
    src = Path(src)
    if not src.exists():
        return None
    rel = src.relative_to(rel_base)
    dst = dst_root / rel
    if dry_run:
        return (str(src), str(dst))
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    return (str(src), str(dst))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    moved = []

    # 1) registry 旧单文件 + 备份 + 拆分目录
    for p in [
        ROOT / "research-data" / "campaign_registry.json",
        ROOT / "research-data" / "campaign_registry.json.bak-p1",
    ]:
        r = move(p, ARCHIVE, args.dry_run)
        if r:
            moved.append(r)

    # registry/ 拆分目录整体归档
    reg_dir = ROOT / "research-data" / "registry"
    if reg_dir.exists():
        r = move(reg_dir, ARCHIVE, args.dry_run)
        if r:
            moved.append(r)

    # 2) 9 个区域 campaign_state.json
    for fp in ROOT.glob("tracking/*/*_d1_campaign_state.json"):
        # KOR/results 下的重复也归档
        r = move(fp, ARCHIVE, args.dry_run)
        if r:
            moved.append(r)
    for fp in ROOT.glob("tracking/*/results/*_d1_campaign_state.json"):
        r = move(fp, ARCHIVE, args.dry_run)
        if r:
            moved.append(r)

    # 3) wave 结果文件（活跃 + 归档目录）
    for region_dir in ROOT.glob("tracking/*"):
        if not region_dir.is_dir():
            continue
        results = region_dir / "results"
        if not results.exists():
            continue
        for fp in results.glob("wave*_results.json"):
            r = move(fp, ARCHIVE, args.dry_run)
            if r:
                moved.append(r)
        arch = results / "_archive"
        if arch.exists():
            r = move(arch, ARCHIVE, args.dry_run)
            if r:
                moved.append(r)

    print(f"[{'DRY-RUN' if args.dry_run else 'OK'}] moved {len(moved)} items -> {ARCHIVE}")
    for s, d in moved:
        print(f"  {Path(s).relative_to(ROOT)}  ->  {Path(d).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
