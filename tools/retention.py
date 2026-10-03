#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""retention.py — data/ cache/ logs/ 运行期保留策略（2026-10-03 立项）

解决什么
--------
磁盘已连续 5 次回涨（2026-09-20 清到 390M/29M → 09-25 回涨 472M/46M →
10-03 再回涨 **1210M / 296M**）。根因不是没有清理动作，而是**没有保留策略**：
`data/` 每次修数据前先 `cp` 一份备份，`.bak_*` 只增不减；`cache/` 下探针产物
无人负责。旧报告 P3 建议过 `retention.py`，但它至今不存在——本工具是它的落地。

为什么不是 `clean_logs.py`
-------------------------
`clean_logs.py`（2026-09-30）只管 `logs/` 的 ACL 锁死目录与过期文件，**覆盖不到
`data/` 与 `cache/`**。历史教训（AGENTS.md §8.4）：这两个目录复发 5 次而没人
拦住，正是因为清理工具的覆盖面与实际膨胀点不匹配。本工具覆盖三处，且三者
策略不同（见下）。

策略（全部 dry-run 默认）
-------------------------
1. ``data/*.bak*``  —— 只留**最新 1 份**（既定政策，§8.3）。live ``wqb.db`` 永不删。
2. ``cache/_probe/*.db`` —— 探针库，mtime ≥ ``--probe-keep-days``（默认 7）即回收。
   实测 2026-10-03 有一份 282.7 MB 的 ``cache/_probe/probe.db`` 滞留 4 天。
3. ``logs/`` 过期文件与 pytest 临时目录 —— 复用既有 ``clean_logs.py`` 的口径
   （保持单一事实源，不在此重写 ACL 处理与管理员提权提示）。

安全边界（不可协商）
--------------------
- ``wqb.db`` / ``wqb.db-wal`` / ``wqb.db-shm`` **永不删**——live 台账。
- 只删**已识别模式**的文件，不做任意目录递归删除。
- 默认 dry-run；``--apply`` 才真删。
- 锁死（ACL 拒绝访问）对象只报告、不提权，交给人处理（同 clean_logs 纪律）。
- 绝不碰 ``tracking/`` ``src/`` ``tools/`` ``tests/``。

用法
----
    python tools/retention.py                  # dry-run（默认）
    python tools/retention.py --apply          # 真删
    python tools/retention.py --check          # 只判退出码（守护测试用）

退出码：0=无事可做/成功，1=有可回收项（--check）或部分失败，2=工具故障
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from pathlib import Path
from typing import List, NamedTuple, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA = REPO_ROOT / "data"
CACHE = REPO_ROOT / "cache"
LOGS = REPO_ROOT / "logs"

#: live DB 主文件及其 WAL 附属——**永不删除**（AGENTS.md §8.3）
LIVE_DB_NAMES = {"wqb.db", "wqb.db-wal", "wqb.db-shm"}

#: data/ 备份识别前缀
DATA_BAK_PREFIXES = ("wqb.db.bak", "wqb_backup", "wqb.db-journal")

#: cache/ 下受管的探针目录（其余 cache 内容一律不碰）
MANAGED_CACHE_DIRS = ("_probe",)

#: logs/ 受管的运行时子目录——并发会话 MCP 进程持续读写，**绝不删除**（§8.4）
LOGS_PROTECTED_DIRS = ("_async_tasks", "_slots", "_dblock", "_dblock_smoketest")


class Target(NamedTuple):
    path: Path
    size: int
    reason: str

    @property
    def is_dir(self) -> bool:
        return self.path.is_dir()


def _human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{int(n)} B"
        n /= 1024.0
    return f"{n:.1f} GB"


def _safe_mtime(p: Path) -> Optional[float]:
    try:
        return p.stat().st_mtime
    except OSError:
        return None


def _size(p: Path) -> int:
    try:
        if p.is_dir():
            total = 0
            for root, _d, names in os.walk(p, onerror=lambda _e: None):
                for nm in names:
                    try:
                        total += (Path(root) / nm).stat().st_size
                    except OSError:
                        continue
            return total
        return p.stat().st_size
    except OSError:
        return 0



def collect_data_baks(keep: int = 1) -> List[Target]:
    """data/ 的陈旧备份：按 mtime 倒序保留最新 ``keep`` 份，其余可回收。

    ⚠ live DB 与其 WAL 附属在任何情况下都不进候选集（硬保护）。
    """
    if not DATA.is_dir():
        return []
    cands = []
    for child in DATA.iterdir():
        if not child.is_file():
            continue
        if child.name in LIVE_DB_NAMES:
            continue
        if not any(child.name.startswith(pfx) for pfx in DATA_BAK_PREFIXES):
            continue
        mt = _safe_mtime(child)
        if mt is None:
            continue
        cands.append((mt, child))
    cands.sort(reverse=True)  # 最新在前
    return [Target(c, _size(c), f"data/ 备份，仅留最新 {keep} 份")
            for _mt, c in cands[keep:]]


def collect_stale_probe_dbs(keep_days: int, now: float) -> List[Target]:
    """cache/_probe/ 下超过保留期的探针库（实测单份可达 282 MB）。"""
    cutoff = now - keep_days * 86400
    out: List[Target] = []
    for dname in MANAGED_CACHE_DIRS:
        d = CACHE / dname
        if not d.is_dir():
            continue
        for child in sorted(d.iterdir()):
            if not child.is_file():
                continue
            mt = _safe_mtime(child)
            if mt is None or mt >= cutoff:
                continue
            out.append(Target(child, _size(child),
                              f"cache/{dname}/ 探针产物，mtime ≥ {keep_days} 天"))
    return out


def collect_logs(keep_days: int, now: float) -> List[Target]:
    """logs/ 的过期散落文件 + pytest 临时目录（顶层）。

    受管运行时子目录（`_async_tasks` / `_slots` / `_dblock`）由并发会话的 MCP
    进程持续读写，**一律跳过**（AGENTS.md §8.4：删了会破坏在跑流水线）。
    """
    if not LOGS.is_dir():
        return []
    cutoff = now - keep_days * 86400
    out: List[Target] = []
    for child in sorted(LOGS.iterdir()):
        if child.is_dir():
            if child.name.startswith(("pytest_", "_pytest_")):
                # pytest basetemp 一律回收，不看年龄（无战役产物）
                out.append(Target(child, _size(child), "logs/ pytest 临时目录"))
            continue
        mt = _safe_mtime(child)
        if mt is None or mt >= cutoff:
            continue
        if child.name == "test-results.xml":
            continue  # 当前 pytest 结果，除非过期否则保留
        out.append(Target(child, _size(child), f"logs/ 过期文件（≥{keep_days} 天）"))
    return out


def collect(keep_data_baks: int, probe_keep_days: int, logs_keep_days: int,
            now: Optional[float] = None) -> List[Target]:
    now = now if now is not None else time.time()
    return (collect_data_baks(keep_data_baks)
            + collect_stale_probe_dbs(probe_keep_days, now)
            + collect_logs(logs_keep_days, now))


def _remove(t: Target) -> bool:
    """删除单个目标。返回是否成功。"""
    try:
        if t.is_dir:
            shutil.rmtree(t.path)
        else:
            t.path.unlink()
        return True
    except OSError as e:
        print(f"  [skip] {t.path.name}: {e}", file=sys.stderr)
        return False


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="data/ cache/ logs/ 运行期保留策略（默认 dry-run，--apply 才真删）")
    ap.add_argument("--keep-data-baks", type=int, default=1,
                    help="data/ 保留最新几份备份（默认 1；live wqb.db 永不删）")
    ap.add_argument("--probe-keep-days", type=int, default=7,
                    help="cache/_probe 探针产物保留天数（默认 7）")
    ap.add_argument("--logs-keep-days", type=int, default=14,
                    help="logs/ 过期文件保留天数（默认 14，同 clean_logs）")
    ap.add_argument("--apply", action="store_true", help="真删；缺省只打印")
    ap.add_argument("--check", action="store_true",
                    help="静默：只判退出码（有可回收项返回 1，供守护测试用）")
    args = ap.parse_args(argv)

    if args.keep_data_baks < 1:
        print("[retention] --keep-data-baks 必须 >= 1（live wqb.db 永不删）", file=sys.stderr)
        return 2

    targets = collect(args.keep_data_baks, args.probe_keep_days, args.logs_keep_days)

    if args.check:
        return 1 if targets else 0

    if not targets:
        print("[retention] 无可回收项：data/ cache/ logs/ 均在保留策略内。")
        return 0

    total = sum(t.size for t in targets)
    by_reason: dict = {}
    for t in targets:
        by_reason[t.reason] = by_reason.get(t.reason, 0) + t.size
    print(f"[retention] 可回收 {len(targets)} 项，合计 {_human(total)}：\n")
    for reason, size in sorted(by_reason.items(), key=lambda x: -x[1]):
        print(f"  {reason:<46} {_human(size):>10}")
    print()
    for t in targets:
        print(f"  [{'dir ' if t.is_dir else 'file'}] {t.path.name:<44} "
              f"{_human(t.size):>10}  ({t.reason})")

    if not args.apply:
        print(f"\n[dry-run] 将回收 {_human(total)}。加 --apply 执行。")
        return 0

    freed = 0
    ok = 0
    for t in targets:
        if _remove(t):
            ok += 1
            freed += t.size
    fail = len(targets) - ok
    print(f"\n[apply] 已回收 {ok} 项（{_human(freed)}），失败 {fail} 项。")
    return 1 if fail else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
