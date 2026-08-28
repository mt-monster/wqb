# -*- coding: utf-8 -*-
"""archive_json_to_attic.py - 单轨数据库模式：把所有历史 JSON 归档到 attic。

归档三类：
1. campaign_state JSON -> attic/json_archive/campaign_state/<REGION>/
2. registry JSON -> attic/json_archive/registry/
3. wave results JSON -> attic/json_archive/wave_results/<REGION>/

安全：移动而非删除，attic 目录保留完整结构。
用法：
  python tools/archive_json_to_attic.py --dry-run
  python tools/archive_json_to_attic.py
"""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATTIC = ROOT / "attic" / "json_archive"


def archive_file(src, dst_dir, dry_run, moved):
    """移动单个文件到归档目录。"""
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        # 已存在则加序号
        i = 1
        while True:
            dst = dst_dir / f"{src.stem}_{i}{src.suffix}"
            if not dst.exists():
                break
            i += 1
    if dry_run:
        print(f"  [DRY] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    else:
        shutil.move(str(src), str(dst))
        moved.append((src, dst))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    moved = []

    # 1. campaign_state JSON
    print("=== 1. campaign_state JSON ===")
    for fp in sorted(ROOT.glob("tracking/**/*_campaign_state.json")):
        # 从路径推断 region
        region = "UNKNOWN"
        for p in fp.parts:
            if p.upper() in ("ASI", "EUR", "GBR", "HKG", "IND", "KOR", "MEA", "USA", "GLB", "DEU"):
                region = p.upper()
                break
        archive_file(fp, ATTIC / "campaign_state" / region, args.dry_run, moved)

    # 2. registry JSON
    print("\n=== 2. registry JSON ===")
    # 旧单文件 + 备份
    for name in ("campaign_registry.json", "campaign_registry.json.bak-p1"):
        fp = ROOT / "research-data" / name
        if fp.exists():
            archive_file(fp, ATTIC / "registry", args.dry_run, moved)
    # 拆分目录
    registry_dir = ROOT / "research-data" / "registry"
    if registry_dir.exists():
        for fp in sorted(registry_dir.glob("*.json")):
            archive_file(fp, ATTIC / "registry" / "split", args.dry_run, moved)

    # 3. wave results JSON
    print("\n=== 3. wave results JSON ===")
    for fp in sorted(ROOT.glob("tracking/*/results/wave*_results.json")):
        region = fp.parts[-3]
        archive_file(fp, ATTIC / "wave_results" / region, args.dry_run, moved)
    # 归档目录里的也移
    for fp in sorted(ROOT.glob("tracking/*/results/_archive/*.json")):
        region = fp.parts[-4]
        archive_file(fp, ATTIC / "wave_results" / region / "_archive", args.dry_run, moved)

    print(f"\n[{'DRY-RUN' if args.dry_run else 'DONE'}] moved {len(moved)} files")
    if not args.dry_run and moved:
        # 写归档清单
        manifest = ATTIC / "MANIFEST.txt"
        with open(manifest, "w", encoding="utf-8") as f:
            f.write(f"# JSON archive manifest - {len(moved)} files\n")
            f.write(f"# Archived at: 2026-08-21 (single-track DB mode)\n\n")
            for src, dst in moved:
                f.write(f"{src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}\n")
        print(f"[MANIFEST] {manifest}")


if __name__ == "__main__":
    main()
