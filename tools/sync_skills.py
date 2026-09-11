#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把仓库 Claude/skills/ 同步到 Agent 实际加载的全部 skill 安装位。

背景（2026-09-06 审计）：仓库副本与 `~/.claude/skills` 已漂移约两周 ——
`brain-make-some-gem` 仓库侧 last_verified=2026-09-05，安装位停在 2026-08-22；
`wq-brain-ra-pipeline` 仓库侧已修正 `check_expr_against_inspect` 的落点路径
并补了整链执行小节，安装位仍是旧文。于是 Agent 读的是旧 SOP，而回归测试
读的是新文，两边都"自洽"，问题只在运行时显形。

根因曾是 `install_now.py` 的 `if target_path.exists(): skip` —— 已装的 skill
永不更新，加上它的源目录 `~/mnt/skills` 在本机根本不存在，等于完全失效。

2026-09-10 审计补强：此前本脚本**只同步单个目标**（`resolve_install_root()` 取
首个命中），于是 `~/.codex/skills` / `~/.workbuddy/skills` 等不在同步链上的宿主
反复分叉——09-08 修过一次，09-10 又复发（ra-pipeline 落后 67 行）。现改为**多目标
同步**：自动枚举全部已存在的安装位，逐个同步 + 逐个校验。

    python tools/sync_skills.py --check     # 只报告漂移，任一目标有漂移则 exit 1（CI/单测用）
    python tools/sync_skills.py --dry-run   # 打印将要执行的动作，不写盘
    python tools/sync_skills.py             # 同步全部安装位
    python tools/sync_skills.py --target ~/.codex/skills --target ~/.cursor/skills
    python tools/sync_skills.py --prune-orphans            # 只列出安装位孤儿（仓库没有的顶层条目）
    python tools/sync_skills.py --prune-orphans --apply    # 归档孤儿到 attic/sync_orphans_<date>/

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


def _candidate_roots() -> List[Path]:
    """复用 workflow 的解析顺序（`wqb.workflow._common._skill_roots()`）。"""
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        from wqb.workflow._common import _skill_roots
        raw = _skill_roots()
    except Exception:
        raw = (
            os.environ.get("WQ_SKILLS_DIR") or "",
            os.path.expanduser("~/.claude/skills"),
            os.path.expanduser("~/.codex/skills"),
            os.path.expanduser("~/.qoder-cn/skills"),
            os.path.expanduser("~/.cursor/skills"),
            os.path.expanduser("~/.workbuddy/skills"),
        )
    return [Path(r) for r in raw if r]


def resolve_install_roots() -> List[Path]:
    """全部已存在的 skill 安装位（按解析顺序，去重，排除仓库源自身）。

    与 `wqb.workflow._common._skill_roots()` 同源，避免"同步到一个没人读的
    目录"。2026-09-10 起返回**列表**（多目标），不再只取首个命中。
    """
    source_resolved = SOURCE.resolve()
    seen, ordered = set(), []
    for candidate in _candidate_roots():
        try:
            resolved = candidate.resolve()
        except OSError:
            continue
        if resolved == source_resolved or resolved in seen:
            continue
        if candidate.is_dir():
            seen.add(resolved)
            ordered.append(candidate)
    return ordered


def resolve_install_root() -> Optional[Path]:
    """兼容旧调用：返回首个安装位（多目标请用 `resolve_install_roots()`）。"""
    roots = resolve_install_roots()
    return roots[0] if roots else None


#: 孤儿清理白名单：这些顶层条目不参与 prune。
#: 判据：① 非 WQ 全局技能（由 WorkBuddy / 其他项目独立维护，本仓库无源）
#:       ② 2026-09-10 审计 P2-1 已裁决"不处置"的废弃 skill。
#: 以 "." 开头的条目（WorkBuddy 迁移标记等）由代码统一放行，无需在此登记。
PROTECTED_ORPHANS = {
    "code-optimization", "dead-code-cleanup", "gold-analysis", "jin10-news",
    "brain-enhance-template",  # 已废止，裁决保留原位（P2-1）
}


def prune_orphans(target: Path, apply: bool = False) -> List[str]:
    """列出（并可选归档）安装位里"仓库根本没有的顶层条目"。

    只增不删是安全默认（历史产物不该被静默清掉），但长期会堆积改名前的旧
    skill 目录与一次性脚本 —— 2026-09-11 审计手工清了 21 项，说明缺口真实存在。
    故提供显式入口：默认**只打印**，`--apply` 才移入
    `<repo>/attic/sync_orphans_<YYYYMMDD>/<host>/`（移动而非删除，可回滚）。

    判据是"顶层条目在仓库完全不存在"，而非"子文件有差异"：后者
    （如 `brain-forum-browse/data/agent_profile.json`、GEM 的 `data/*_idea_*.json`）
    是运行时产物，属正常，**不得**当孤儿清理。
    """
    if not target.is_dir():
        return []
    src_top = {p.name for p in SOURCE.iterdir()}
    orphans = [
        entry.name for entry in sorted(target.iterdir(), key=lambda p: p.name)
        if entry.name not in src_top
        and entry.name not in PROTECTED_ORPHANS
        and not entry.name.startswith(".")
        and "migration" not in entry.name.lower()   # WorkBuddy 迁移标记（_bm_skillid_migration.json 等）
    ]
    if not orphans or not apply:
        return orphans

    import datetime
    host = target.resolve().parent.name or "target"
    stamp = datetime.date.today().strftime("%Y%m%d")
    dest_root = REPO_ROOT / "attic" / f"sync_orphans_{stamp}" / host
    links: List[str] = []
    for name in orphans:
        src = target / name
        # 悬空链接：symlink 与 Windows directory junction 都会「lexists 但 exists==False」。
        # 二者内容都不在本机（目标已删），跨盘 shutil.move 必失败（跟随悬空 reparse point）。
        # 故只记录 target 再摘除链接本身；symlink 用 unlink，junction 用 rmdir。
        if os.path.lexists(src) and not os.path.exists(src):
            try:
                tgt = os.readlink(src)
            except OSError:
                tgt = "<unresolvable>"
            links.append(f"{name}\t-> {tgt}")
            try:
                os.unlink(src)
            except OSError:
                try:
                    os.rmdir(src)
                except OSError as e:
                    print(f"    [warn] 无法移除悬空链接 {name}: {e}")
            continue
        dest = dest_root / name
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
    if links:
        dest_root.mkdir(parents=True, exist_ok=True)
        with open(dest_root / "dangling_symlinks.txt", "w", encoding="utf-8", newline="") as f:
            f.write("# 已删除的悬空符号链接（内容不在本机，仅留 target 备查）\n")
            f.write("\n".join(links) + "\n")
    return orphans


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


#: 运行时产物判据（安装位有、仓库没有，但**属正常**，不参与孤儿清理也不该刷屏）
RUNTIME_PARTS = {"data", "outputs", "output_report", "logs", "__pycache__"}
RUNTIME_SUFFIXES = (".log", ".csv", ".pyc", ".pyo")
RUNTIME_NAMES = {"agent_profile.json", "loop_state.json", "parsetab.py"}


def _is_runtime_artifact(rel: Path) -> bool:
    if any(part in RUNTIME_PARTS for part in rel.parts):
        return True
    if rel.suffix in RUNTIME_SUFFIXES:
        return True
    if ".bak_" in rel.name or rel.name in RUNTIME_NAMES:
        return True
    return False


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
    # 但历史遗留的其他文件不该被本工具静默清掉）。按顶层条目去重，避免刷屏。
    # 2026-09-11：把"运行时产物"（GEM 的 data/*_idea_*.json、ace.log 等）与
    # "真孤儿"（改名前的旧 skill 目录、一次性脚本）**分开报**，否则前者会把
    # 后者淹掉，读者以为一切正常。
    runtime = {rel for rel in only_target if _is_runtime_artifact(rel)}
    real_orphans = [rel for rel in only_target if rel not in runtime]
    for top in sorted({(rel.parts[0] if rel.parts else rel.as_posix()) for rel in real_orphans}):
        print(f"  ONLY-AT-INSTALL {top}（未删除，如确认是废弃 skill/产物请手工清理）")
    if runtime:
        print(f"  [runtime] {len(runtime)} 个运行时产物（正常，不计入孤儿）")

    return actions


def _check_one(target: Path) -> int:
    only_source, changed, _only_target = diff_tree(SOURCE, target)
    for rel in only_source:
        print(f"  MISSING  {rel.as_posix()}")
    for rel in changed:
        print(f"  STALE    {rel.as_posix()}")
    return len(only_source) + len(changed)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="只检查漂移，任一目标有漂移则 exit 1（不写盘）")
    ap.add_argument("--dry-run", action="store_true",
                    help="打印将要执行的动作，不写盘")
    ap.add_argument("--target", action="append", default=None,
                    help="显式指定安装位（可重复；默认自动枚举全部已存在安装位）")
    ap.add_argument("--prune-orphans", action="store_true",
                    help="列出安装位里仓库不存在的顶层条目（旧 skill 目录 / 一次性脚本）；"
                         "默认只打印，配 --apply 才归档（移动，非删除）")
    ap.add_argument("--apply", action="store_true",
                    help="配合 --prune-orphans：实际执行归档（默认 dry-run）")
    a = ap.parse_args()

    if not SOURCE.is_dir():
        print(f"[sync_skills] 源目录不存在：{SOURCE}", file=sys.stderr)
        return 2

    if a.target:
        targets = [Path(t) for t in a.target]
    else:
        targets = resolve_install_roots()
    if not targets:
        print("[sync_skills] 未找到 skill 安装位；用 --target 指定或设 WQ_SKILLS_DIR",
              file=sys.stderr)
        return 2

    print(f"[sync_skills] 源   : {SOURCE}")
    print(f"[sync_skills] 目标 : {len(targets)} 个安装位")

    if a.check:
        total_drift, drifted = 0, []
        for t in targets:
            n = _check_one(t)
            print(f"  [{'OK' if n == 0 else f'漂移 {n}'}] {t}")
            total_drift += n
            if n:
                drifted.append(t)
        if total_drift:
            print(f"[sync_skills] 共 {total_drift} 个文件漂移，涉及 {len(drifted)} 个安装位；"
                  f"跑 `python tools/sync_skills.py` 同步", file=sys.stderr)
            return 1
        print("[sync_skills] 全部安装位与仓库一致")
        return 0

    total = 0
    for t in targets:
        print(f"\n[sync_skills] -> {t}")
        total += sync(SOURCE, t, dry_run=a.dry_run)
    verb = "将同步" if a.dry_run else "已同步"
    print(f"\n[sync_skills] {verb} {total} 个文件（{len(targets)} 个安装位）")

    if a.prune_orphans:
        print("\n[sync_skills] 孤儿扫描（安装位有、仓库没有的**顶层条目**；"
              "子文件差异与 . 开头条目不算）")
        total_orphans = 0
        for t in targets:
            names = prune_orphans(t, apply=a.apply)
            total_orphans += len(names)
            flag = "" if names else "  (无)"
            print(f"  {t}{flag}")
            for n in names:
                print(f"    - {n}")
        if total_orphans and not a.apply:
            print(f"\n[sync_skills] 待归档 {total_orphans} 项 —— 加 --apply 执行"
                  f"（移入 attic/sync_orphans_<date>/<host>/，可回滚）")
        else:
            print(f"\n[sync_skills] {'已归档' if a.apply else '无需清理'} {total_orphans} 项")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
