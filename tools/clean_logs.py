# -*- coding: utf-8 -*-
"""clean_logs.py - logs/ 运行期目录清理（2026-09-30 结构审计 P0）

解决什么
--------
`logs/` 是运行期账本（pytest 结果、_async_tasks 批次目录、_slots 槽位账本、
dblock 锁），被 .gitignore 排除。实测 2127 个可读文件 / 17.6 MB，另有 22 个
pytest 临时目录（`pytest_*` / `_pytest_*`）在 2026-09-24 手工跑 pytest 时
指定 `--basetemp`/`--cache-dir` 落到 logs/ 下，跑完残留且 ACL 拒绝访问。

那 22 个目录的危害不是占空间（都是空目录），而是**破坏递归扫描**：任何
`Get-ChildItem -Recurse` / `os.walk` / 依赖收集都会在它们上面抛
PermissionError 或刷屏拒绝访问信息，掩盖真实错误。

分两层处理
----------
1. **普通层（默认，本工具能自己做完）**：按保留天数删运行期文件/目录。
   默认 `--keep-days 14`，只动 logs/ 内部，不碰 data/ tracking/ src/。
2. **锁死层（`--report-locked`）**：探测 ACL 拒绝访问的目录并打印需管理员
   执行的 takeown/icacls/rmdir 命令。**不自行提权**——本仓库的删除纪律是
   一切删除走显式确认，工具只出命令，人来执行。

退出码
------
0 = 清理完成（或 dry-run 无事可做）
1 = 工具故障（参数错误、IO 异常）
2 = 存在锁死目录，需人工以管理员执行 `--report-locked` 输出的命令

不做什么
--------
- 不删 `data/wqb.db` 及任何战役产物
- 不碰 `.gitignore` 已排除范围之外的文件
- 不动 `test-results.xml`（pytest 当前结果，除非超过 keep-days）
- 不静默删除：默认 dry-run，加 `--apply` 才真删
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS = REPO_ROOT / "logs"

#: 受管的运行期子目录/前缀。pytest 临时目录单独归类（它们才是锁死的那些）。
PYTEST_TMP_PREFIXES = ("pytest_", "_pytest_")
#: 明确的运行期子目录名，白名单之外的 logs/ 子目录一律不动（避免误删
#: 未来新增的账本目录）。
MANAGED_SUBDIRS = ("_async_tasks", "_slots", "_dblock", "_dblock_smoketest")


def _human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0
    return f"{n:.1f} GB"


def _dir_size(p: Path) -> tuple[int, int]:
    """(bytes, files)。遇到拒绝访问的子项跳过而非抛错——那正是要报告的对象。"""
    total = files = 0
    for root, _dirs, names in os.walk(p, onerror=lambda _e: None):
        for nm in names:
            try:
                total += (Path(root) / nm).stat().st_size
                files += 1
            except OSError:
                continue
    return total, files


def is_locked(p: Path) -> bool:
    """能否读这个目录。读不了就是 ACL 锁死。"""
    try:
        os.listdir(p)
        return False
    except OSError:
        return True


def collect_expired(keep_days: int, now: float) -> list[Path]:
    """列出超过保留期的受管对象。"""
    cutoff = now - keep_days * 86400
    out: list[Path] = []
    for child in sorted(LOGS.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(PYTEST_TMP_PREFIXES):
            out.append(child)  # pytest 临时目录一律回收，不看年龄
            continue
        if child.name not in MANAGED_SUBDIRS:
            continue
        try:
            mtime = child.stat().st_mtime
        except OSError:
            continue
        if mtime < cutoff:
            out.append(child)
    return out


def collect_stale_files(keep_days: int, now: float) -> list[Path]:
    """logs/ 顶层的过期散落文件（不含 test-results.xml 等当前结果）。"""
    cutoff = now - keep_days * 86400
    out: list[Path] = []
    for child in sorted(LOGS.iterdir()):
        if not child.is_file():
            continue
        try:
            if child.stat().st_mtime < cutoff:
                out.append(child)
        except OSError:
            continue
    return out


def report_locked() -> int:
    """打印锁死目录 + 需管理员执行的命令。返回锁死目录数。"""
    locked = [
        d for d in sorted(LOGS.iterdir())
        if d.is_dir() and d.name.startswith(PYTEST_TMP_PREFIXES) and is_locked(d)
    ]
    if not locked:
        print("[clean_logs] 无锁死目录。")
        return 0

    print(f"[clean_logs] 发现 {len(locked)} 个 ACL 锁死的 pytest 临时目录：\n")
    for d in locked:
        print(f"  - {d.name}")
    print(
        "\n以下命令需**以管理员身份**在 PowerShell 执行（本工具不自行提权，\n"
        "删除纪律要求人工确认）。整目录删除是安全的：它们都是 pytest 的\n"
        "--basetemp/--cache-dir 临时目录，无战役产物。\n"
    )
    print("  # 1) 逐个夺权 + 复位 ACL + 删除")
    for d in locked:
        q = str(d)
        print(f'  takeown /F "{q}" /R /D Y')
        print(f'  icacls "{q}" /reset /T /C')
        print(f'  rmdir /S /Q "{q}"')
    print(
        "\n  # 2) 或一次性批量（管理员 PowerShell 单行）\n"
        f'  Get-ChildItem "{LOGS}" -Directory | '
        'Where-Object { $_.Name -match "^(pytest_|_pytest_)" } | '
        "ForEach-Object { takeown /F $_.FullName /R /D Y; "
        "icacls $_.FullName /reset /T /C; Remove-Item $_.FullName -Recurse -Force }\n"
    )
    print("  # 3) 删完复验（应输出 0）：")
    print(f'  Get-ChildItem "{LOGS}" -Directory | '
          'Where-Object { $_.Name -match "^(pytest_|_pytest_)" } | Measure-Object')
    return len(locked)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="logs/ 运行期清理（默认 dry-run，--apply 才真删）",
    )
    ap.add_argument("--keep-days", type=int, default=14,
                    help="运行期目录/文件保留天数（默认 14）")
    ap.add_argument("--apply", action="store_true",
                    help="真删；缺省只打印将删什么")
    ap.add_argument("--report-locked", action="store_true",
                    help="只探测 ACL 锁死目录并打印管理员命令，不做清理")
    args = ap.parse_args(argv)

    if not LOGS.is_dir():
        print(f"[clean_logs] {LOGS} 不存在，跳过。")
        return 0

    if args.report_locked:
        n = report_locked()
        return 2 if n else 0

    now = time.time()
    dirs = collect_expired(args.keep_days, now)
    files = collect_stale_files(args.keep_days, now)

    if not dirs and not files:
        print(f"[clean_logs] logs/ 无超过 {args.keep_days} 天的受管对象。")
    else:
        print(f"[clean_logs] 保留期 {args.keep_days} 天；logs/ 共 "
              f"{_human(_dir_size(LOGS)[0])}。\n")
        for d in dirs:
            b, n = _dir_size(d)
            print(f"  [dir ] {d.name:<44} {_human(b):>10}  {n:>5} files")
        for f in files:
            try:
                b = f.stat().st_size
            except OSError:
                b = 0
            print(f"  [file] {f.name:<44} {_human(b):>10}")
        total_dirs = len(dirs)
        total_files = len(files)
        if not args.apply:
            print(f"\n[dry-run] 将删 {total_dirs} 个目录 / {total_files} 个文件。"
                  "加 --apply 执行。")
        else:
            ok = fail = 0
            for d in dirs:
                try:
                    shutil.rmtree(d)
                    ok += 1
                except OSError as e:
                    print(f"  [skip] {d.name}: {e}", file=sys.stderr)
                    fail += 1
            for f in files:
                try:
                    f.unlink()
                    ok += 1
                except OSError as e:
                    print(f"  [skip] {f.name}: {e}", file=sys.stderr)
                    fail += 1
            print(f"\n[apply] 已删 {ok} 项，失败 {fail} 项。")

    n_locked = report_locked()
    return 2 if n_locked else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
