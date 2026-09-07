#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把仓库 Claude/skills/ 同步到 Agent 实际加载的 skill 安装位。

背景（2026-09-06 审计）：仓库副本与 `~/.claude/skills` 已漂移约两周 ——
`brain-makeSomeGem` 仓库侧 last_verified=2026-09-05，安装位停在 2026-08-22；
`wq-brain-ra-pipeline` 仓库侧已修正 `check_expr_against_inspect` 的落点路径
并补了整链执行小节，安装位仍是旧文。于是 Agent 读的是旧 SOP，而回归测试
读的是新文，两边都"自洽"，问题只在运行时显形。

根因是 `install_now.py` 的 `if target_path.exists(): skip` —— 已装的 skill
永不更新，加上它的源目录 `~/mnt/skills` 在本机根本不存在，等于完全失效。

本脚本取代它承担 repo → 安装位的同步：

    python tools/sync_skills.py --check     # 只报告漂移，有漂移则 exit 1（CI/单测用）
    python tools/sync_skills.py --dry-run   # 打印将要执行的动作，不写盘
    python tools/sync_skills.py             # 执行同步

方向是单向的：**仓库是源，安装位是派生物**。安装位的本地修改会被覆盖，
要改 skill 请改仓库副本再同步。
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "Claude" / "skills"

#: 不参与同步的产物/缓存（与 .gitignore 的 Claude/skills 规则同口径）
IGNORE_DIRS = {"__pycache__", "outputs", "output_report", "processed_templates", ".git"}
IGNORE_SUFFIXES = (".pyc", ".pyo")
IGNORE_NAMES = {"parsetab.py", "parser.out"}


def _is_ignored(rel: Path) -> bool:
    if any(part in IGNORE_DIRS for part in rel.parts):
        return True
    if rel.name in IGNORE_NAMES or rel.suffix in IGNORE_SUFFIXES:
        return True
    if ".bak_" in rel.name:
        return True
    return False


def resolve_install_root() -> Optional[Path]:
    """定位 Agent 实际加载的 skill 目录（复用 workflow 的解析顺序）。

    与 `wqb.workflow._common._skill_roots()` 同源，避免"同步到一个没人读的
    目录"。排除仓库副本自身（它是源，不是目标）。
    """
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        from wqb.workflow._common import _skill_roots
        roots = _skill_roots()
    except Exception:
        roots = (
            os.environ.get("WQ_SKILLS_DIR") or "",
            os.path.expanduser("~/.claude/skills"),
        )

    source_resolved = SOURCE.resolve()
    for root in roots:
        if not root:
            continue
        candidate = Path(root)
        try:
            if candidate.resolve() == source_resolved:
                continue
        except OSError:
            continue
        if candidate.is_dir():
            return candidate
    return None


def _read_normalized(path: Path) -> Optional[bytes]:
    """读文件并归一化换行符。

    仓库侧是 CRLF、安装位是 LF（或反之）是常态，逐字节比较会把 33 个 skill
    全报成漂移 —— 首次实测 27 个"漂移"里只有 5 个是真的。
    """
    try:
        return path.read_bytes().replace(b"\r\n", b"\n")
    except OSError:
        return None


def diff_tree(source: Path, target: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """返回 (仅源有, 内容不同, 仅目标有) 的相对路径列表。"""
    src_files = {
        p.relative_to(source)
        for p in source.rglob("*")
        if p.is_file() and not _is_ignored(p.relative_to(source))
    }
    dst_files = {
        p.relative_to(target)
        for p in target.rglob("*")
        if p.is_file() and not _is_ignored(p.relative_to(target))
    }

    only_source = sorted(src_files - dst_files)
    only_target = sorted(dst_files - src_files)
    changed = sorted(
        rel for rel in (src_files & dst_files)
        if _read_normalized(source / rel) != _read_normalized(target / rel)
    )
    return only_source, changed, only_target


def sync(source: Path, target: Path, dry_run: bool) -> int:
    only_source, changed, only_target = diff_tree(source, target)
    actions = 0

    for rel in only_source + changed:
        verb = "ADD " if rel in only_source else "UPD "
        print(f"  {verb} {rel.as_posix()}")
        actions += 1
        if dry_run:
            continue
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, dst)

    # 安装位多出来的文件只报告不删除：可能是本地产物（outputs 已在忽略表里，
    # 但历史遗留的其他文件不该被本工具静默清掉）。
    for rel in only_target:
        print(f"  ONLY-AT-INSTALL {rel.as_posix()}（未删除，如确认是废弃文件请手工清理）")

    return actions


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="只检查漂移，有漂移则 exit 1（不写盘）")
    ap.add_argument("--dry-run", action="store_true",
                    help="打印将要执行的动作，不写盘")
    ap.add_argument("--target", default=None,
                    help="显式指定安装位（默认按 _skill_roots() 解析）")
    a = ap.parse_args()

    if not SOURCE.is_dir():
        print(f"[sync_skills] 源目录不存在：{SOURCE}", file=sys.stderr)
        return 2

    target = Path(a.target) if a.target else resolve_install_root()
    if target is None:
        print("[sync_skills] 未找到 skill 安装位；用 --target 指定或设 WQ_SKILLS_DIR",
              file=sys.stderr)
        return 2

    print(f"[sync_skills] 源   : {SOURCE}")
    print(f"[sync_skills] 目标 : {target}")

    if a.check:
        only_source, changed, only_target = diff_tree(SOURCE, target)
        drift = len(only_source) + len(changed)
        for rel in only_source:
            print(f"  MISSING  {rel.as_posix()}")
        for rel in changed:
            print(f"  STALE    {rel.as_posix()}")
        if drift:
            print(f"[sync_skills] 漂移 {drift} 个文件；跑 "
                  f"`python tools/sync_skills.py` 同步", file=sys.stderr)
            return 1
        print("[sync_skills] 安装位与仓库一致")
        return 0

    actions = sync(SOURCE, target, dry_run=a.dry_run)
    verb = "将同步" if a.dry_run else "已同步"
    print(f"[sync_skills] {verb} {actions} 个文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
