# -*- coding: utf-8 -*-
"""tracking JSON 归档策略工具（dry-run 优先，绝不删除数据）。

背景：tracking/ 累计 ~34 MB JSON（台账/波次记录/候选池），长期仅增不删，
git 仓库体积与本地噪音持续膨胀。本工具提供"可复盘、可撤销"的归档路径：

  - 扫描 tracking/ 下全部 *.json，按目录统计数量/体积/最旧修改时间
  - 标记"可归档候选"：mtime 早于 --older-than 天，或落在 results/cache/_* 子目录
  - 默认 dry-run：只打印归档计划与将释放的体积，不改动任何文件
  - --apply：把候选移动到 tracking/_archive_json/<原相对路径>，原结构保留、可 git mv 追溯

安全护栏：
  * 永不 os.remove / shutil.rmtree —— 只 move 到归档区，随时可还原
  * 默认 dry-run；--apply 才落盘
  * 跳过 .git / __pycache__ / _archive_json 自身

用法:
  python archive_json_plan.py                 # dry-run 全景
  python archive_json_plan.py --older-than 30  # 仅看 30 天前的候选
  python archive_json_plan.py --older-than 30 --apply   # 实际归档
"""
import argparse
import os
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # tracking/reference/tooling -> tracking/
TRACKING = ROOT  # 已是 tracking/ 根
ARCHIVE = TRACKING / "_archive_json"
SKIP = {".git", "__pycache__", "_archive_json"}


def scan():
    rows = []
    for dp, dn, fn in os.walk(TRACKING):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if not f.endswith(".json"):
                continue
            p = Path(dp) / f
            try:
                sz = p.stat().st_size
                mtime = p.stat().st_mtime
            except OSError:
                continue
            rel = p.relative_to(TRACKING)
            rows.append((rel, sz, mtime))
    return rows


def main():
    ap = argparse.ArgumentParser(description="tracking JSON 归档策略（dry-run 优先）")
    ap.add_argument("--older-than", type=int, default=0,
                    help="仅把 mtime 早于 N 天的 JSON 视为候选（0=全部）")
    ap.add_argument("--min-size-kb", type=float, default=0,
                    help="仅把大于该 KB 的文件视为候选")
    ap.add_argument("--apply", action="store_true", help="实际移动到归档区（默认仅打印计划）")
    args = ap.parse_args()

    rows = scan()
    now = time.time()
    older_s = args.older_than * 86400
    candidates = []
    total_sz = 0
    for rel, sz, mtime in rows:
        if args.older_than and (now - mtime) < older_s:
            continue
        if sz < args.min_size_kb * 1024:
            continue
        candidates.append((rel, sz, mtime))
        total_sz += sz

    print(f"tracking/ JSON 总览: {len(rows)} 文件, {sum(s for _, s, _ in rows)/1024/1024:.2f} MB")
    print(f"归档候选: {len(candidates)} 文件, 将释放 {total_sz/1024/1024:.2f} MB")
    print("-" * 80)
    # 按目录聚合
    by_dir = {}
    for rel, sz, _ in candidates:
        d = str(rel.parent)
        by_dir.setdefault(d, [0, 0])
        by_dir[d][0] += 1
        by_dir[d][1] += sz
    for d, (cnt, sz) in sorted(by_dir.items(), key=lambda x: -x[1][1]):
        print(f"  {d:50s} {cnt:5d} files  {sz/1024:.1f} KB")

    if not candidates:
        print("\n无候选。")
        return

    if not args.apply:
        print("\n[DRY-RUN] 未改动任何文件。加 --apply 执行归档（移动到 _archive_json/）。")
        return

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    moved = 0
    for rel, sz, _ in candidates:
        dst = ARCHIVE / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(TRACKING / rel), str(dst))
        moved += 1
    print(f"\n[APPLY] 已归档 {moved} 文件到 {ARCHIVE}")
    print("如需还原: 从 _archive_json/ 移回原路径（tracked 文件建议 git mv）。")


if __name__ == "__main__":
    main()
