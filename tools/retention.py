#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""retention.py — data/ cache/ logs/ results/ 运行期保留策略（2026-10-03 立项，2026-10-18 补 results/）

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
4. ``cache/_scratch/pt/`` —— **pytest basetemp 目录**（子目录名就是测试函数名截断，
   如 ``test_a_db_without_the_expressi0``）。2026-10-14 布局审计实测 737 个，是全仓
   153 个空目录的主要来源。按 ``--pytest-temp-keep-hours``（默认 24 小时）回收；
   **不采用「一律回收」**：正在跑的并行会话有自己的新鲜 basetemp，秒删会把它的
   临时目录从脚下抽走。
5. ``cache/_scratch/`` 顶层散件 —— **默认不回收，需 ``--scratch-files`` 显式开启**。
   原因（实测）：这一层混着**批次输入件**（``asi_fix2_spec.json`` 里逐条写着
   ``cache/_scratch/asi_fix2_variants.txt``），删掉等于废掉一次可复跑的派批。
   开启后仍只收 mtime ≥ ``--scratch-keep-days``（默认 30 天）的文件。
6. ``results/`` 的 ``*.json`` checkpoint —— mtime ≥ ``--results-keep-days``
   （默认 30 天）即回收（2026-10-18 增补）。**与前三处最大的差别：这不是垃圾区，
   是续跑断点区**（AGENTS.md §1 明示三个脚本硬编码引用其路径，移动会破坏续跑）
   ⇒ 只原地删、不移动；且只认顶层 ``*.json``，活跃批次的近期断点天然被年龄闸挡住。

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
    python tools/retention.py --scratch-files --apply   # 连 `_` 前缀草稿件一起清

退出码：0=无事可做/成功，1=有可回收项（--check）或部分失败，2=工具故障
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import List, NamedTuple, Optional


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)
DATA = REPO_ROOT / "data"
CACHE = REPO_ROOT / "cache"
LOGS = REPO_ROOT / "logs"
RESULTS = REPO_ROOT / "results"

#: live DB 主文件及其 WAL 附属——**永不删除**（AGENTS.md §8.3）
LIVE_DB_NAMES = {"wqb.db", "wqb.db-wal", "wqb.db-shm"}

#: data/ 备份识别前缀
DATA_BAK_PREFIXES = ("wqb.db.bak", "wqb_backup", "wqb.db-journal")

#: cache/ 下受管的探针目录（其余 cache 内容一律不碰）
MANAGED_CACHE_DIRS = ("_probe",)

#: cache/_scratch —— 会话草稿区（gitignore）。2026-10-14 起纳入保留策略。
SCRATCH_DIRNAME = "_scratch"
#: pytest basetemp 条目的**命名签名**：`--basetemp=<目录>` 产出的临时目录是
#: `test_<用例名截断><序号>`（实测 `test_a_db_without_the_expressi0`、
#: `test_zip_slip_is_refused0`），默认 TMP 布局则是 `pytest-of-<user>-0`。
#: **必须带尾序号**——只按 `test_` 前缀判会把任何人造的目录当 basetemp（写完
#: 第一版就被自己的回归测试逮到：`asi_46_probe/test_looks_like_a_case` 误进候选）。
BASTEMP_CHILD_RE = re.compile(r"^(?:test_|pytest-).+\d$")
#: 顶层草稿件识别：仓库自有约定是 `_` 前缀（AGENTS.md §5 规约 1「`logs/_*.py` 下划线前缀
#: 即临时脚本」），外加 `.diff`（diff 快照，无消费方）。其余一律不碰。
SCRATCH_DRAFT_PREFIXES = ("_",)
SCRATCH_DRAFT_SUFFIXES = (".diff",)
#: 永不受影响的批次输入件（即便名字命中上面的模式）——`cache/_scratch` 里混着
#: `*_spec.json` 指向的 `*_variants.txt`，删了等于废掉一次可复跑的派批。
SCRATCH_INPUT_PATTERNS = ("_spec.json", "_variants.txt", ".items.json")
PYTEST_TEMP_KEEP_HOURS_DEFAULT = 24.0
SCRATCH_FILES_KEEP_DAYS_DEFAULT = 30.0
#: ``results/`` checkpoint 默认保留天数（2026-10-18 增补）。
#: 取 30 天与 `cache/_scratch` 散件同档：一个派批的续跑窗口远短于 30 天，
#: 超期断点已无复跑价值，而 160 个 checkpoint 持续累积无人负责。
RESULTS_KEEP_DAYS_DEFAULT = 30.0

#: logs/ 受管的运行时子目录——并发会话 MCP 进程持续读写，**绝不删除**（§8.4）
LOGS_PROTECTED_DIRS = ("_async_tasks", "_slots", "_dblock", "_dblock_smoketest")

#: ``results/`` 永不回收的件（AGENTS.md §1：``results/`` 的续跑断点被
#: ``backfill_longcount.py`` / ``batch_submit_verdict.py`` / ``prod_blocked_recheck.py``
#: 硬编码引用，**移动会破坏续跑**）。
#:
#: ⇒ 本策略**只按年龄回收**、**默认不删**（需 ``--apply``），
#: 且绝不删「近期被读写过的」——活跃批次的 checkpoint 一定比 30 天新，
#: 天然被年龄闸挡住；此处显式登记是为防将来有人把年龄阈值调到 0。
RESULTS_NEVER_DELETE = ("wqb.db",)


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


def collect_results(keep_days: float, now: float) -> List[Target]:
    """`results/` 的过期 checkpoint（2026-10-18 增补）。

    为什么补这一处：`retention.py` 原覆盖 `data/ cache/ logs/` 三处，**不含 `results/`**，
    而实测 `results/` 有 160 个 `*.json` checkpoint 持续累积、无人负责。

    与其余三处的关键差别：**`results/` 是续跑断点区，不是垃圾区**。
    AGENTS.md §1 明示 `backfill_longcount.py` / `batch_submit_verdict.py` /
    `prod_blocked_recheck.py` 硬编码引用它的路径，**移动会破坏续跑**
    ⇒ 回收只能「原地删」，不能「移走」。

    保守策略：
    - 只认 `*.json`（checkpoint 的实际形态），不递归、不碰子目录；
    - 只回收 mtime 早于 ``--results-keep-days``（默认 30 天）的；
    - 活跃批次的 checkpoint 必然比阈值新，天然被挡住，无需额外识别「在跑批次」。
    """
    if not RESULTS.is_dir():
        return []
    cutoff = now - keep_days * 86400
    out: List[Target] = []
    for child in sorted(RESULTS.iterdir()):
        if child.is_dir() or child.suffix != ".json":
            continue
        if child.name in RESULTS_NEVER_DELETE:
            continue
        mt = _safe_mtime(child)
        if mt is None or mt >= cutoff:
            continue
        out.append(Target(child, _size(child),
                          f"results/ checkpoint，mtime ≥ {keep_days:g} 天"))
    return out


def _is_scratch_file(name: str) -> bool:
    """顶层散件是否「确认是草稿形态」（`_` 前缀或 `.diff`），且不是批次输入件。"""
    if any(pat in name for pat in SCRATCH_INPUT_PATTERNS):
        return False
    return (name.startswith(SCRATCH_DRAFT_PREFIXES)
            or name.endswith(SCRATCH_DRAFT_SUFFIXES))


def _is_basetemp_child(p: Path) -> bool:
    """条目是否是 pytest basetemp 产出的临时目录（认命名签名，不认容器名）。

    容器名实测有两种写法（`pt` 与 `pt2`），所以按**子条目签名**判定，不按容器名白名单。
    """
    return p.is_dir() and bool(BASTEMP_CHILD_RE.match(p.name))


def _is_basetemp_container(d: Path) -> bool:
    try:
        return any(_is_basetemp_child(c) for c in d.iterdir())
    except OSError:
        return False


def collect_scratch(temp_keep_hours: float, files_keep_days: float, now: float,
                    include_files: bool = False) -> List[Target]:
    """cache/_scratch/ 的回收面（策略 4/5）。

    - basetemp 容器里的 `test_*` / `pytest-*` 目录：mtime ≥ ``temp_keep_hours``
      小时即回收。新鲜目录一律保留 —— 并行会话正在跑的 pytest 有自己的 basetemp，
      「一律回收」会把它的临时目录从脚下抽走（这是本函数用小时而非 0 的原因）。
    - 顶层文件：**默认不回收**（``include_files=False``）。只有显式开启、
      命中草稿形态、且 mtime ≥ ``files_keep_days`` 天才进候选。
      批次输入件（``*_spec.json`` / ``*_variants.txt``）不在形态内，开了也不碰。
    - 既不是 basetemp 容器、又不是草稿文件的条目**一律不碰**（只删已识别模式）。
    """
    root = CACHE / SCRATCH_DIRNAME
    if not root.is_dir():
        return []
    out: List[Target] = []

    temp_cutoff = now - temp_keep_hours * 3600
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        if not _is_basetemp_container(d):
            continue
        for sub in sorted(d.iterdir()):
            if not _is_basetemp_child(sub):
                continue
            mt = _safe_mtime(sub)
            if mt is None or mt >= temp_cutoff:
                continue
            out.append(Target(sub, _size(sub),
                              f"cache/{SCRATCH_DIRNAME}/{d.name}/ pytest basetemp"
                              f"（≥{temp_keep_hours:g} h）"))

    if include_files:
        files_cutoff = now - files_keep_days * 86400
        for child in sorted(root.iterdir()):
            if child.is_dir():
                continue
            if not _is_scratch_file(child.name):
                continue
            mt = _safe_mtime(child)
            if mt is None or mt >= files_cutoff:
                continue
            out.append(Target(child, _size(child),
                              f"cache/{SCRATCH_DIRNAME}/ 草稿件"
                              f"（≥{files_keep_days:g} 天，--scratch-files）"))
    return out


def collect(keep_data_baks: int, probe_keep_days: int, logs_keep_days: int,
            now: Optional[float] = None,
            scratch_temp_hours: float = PYTEST_TEMP_KEEP_HOURS_DEFAULT,
            scratch_files_days: float = SCRATCH_FILES_KEEP_DAYS_DEFAULT,
            scratch_include_files: bool = False,
            results_keep_days: float = RESULTS_KEEP_DAYS_DEFAULT) -> List[Target]:
    now = now if now is not None else time.time()
    return (collect_data_baks(keep_data_baks)
            + collect_stale_probe_dbs(probe_keep_days, now)
            + collect_logs(logs_keep_days, now)
            + collect_scratch(scratch_temp_hours, scratch_files_days, now,
                              include_files=scratch_include_files)
            + collect_results(results_keep_days, now))


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
    ap.add_argument("--pytest-temp-keep-hours", type=float,
                    default=PYTEST_TEMP_KEEP_HOURS_DEFAULT,
                    help="cache/_scratch basetemp 目录保留小时数（默认 24；"
                         "小于该值是「正在跑的会话的临时目录」，不回收）")
    ap.add_argument("--scratch-files", action="store_true",
                    help="额外把 cache/_scratch/ 顶层的草稿形态文件（`_` 前缀 / `.diff`）"
                         "列入回收候选。**默认关闭**：该层混着 `*_spec.json` 指向的批次"
                         "输入件，删了会废掉一次可复跑的派批")
    ap.add_argument("--scratch-keep-days", type=float,
                    default=SCRATCH_FILES_KEEP_DAYS_DEFAULT,
                    help="配合 --scratch-files：草稿件保留天数（默认 30）")
    ap.add_argument("--results-keep-days", type=float,
                    default=RESULTS_KEEP_DAYS_DEFAULT,
                    help="results/ checkpoint 保留天数（默认 30）。⚠ results/ 是"
                         "**续跑断点区**（AGENTS.md §1：移动会破坏续跑），本策略只"
                         "原地删超期 `*.json`，不移动、不碰活跃批次的近期断点")
    ap.add_argument("--apply", action="store_true", help="真删；缺省只打印")
    ap.add_argument("--check", action="store_true",
                    help="静默：只判退出码（有可回收项返回 1，供守护测试用）")
    args = ap.parse_args(argv)

    if args.keep_data_baks < 1:
        print("[retention] --keep-data-baks 必须 >= 1（live wqb.db 永不删）", file=sys.stderr)
        return 2

    targets = collect(args.keep_data_baks, args.probe_keep_days, args.logs_keep_days,
                      scratch_temp_hours=args.pytest_temp_keep_hours,
                      scratch_files_days=args.scratch_keep_days,
                      scratch_include_files=args.scratch_files,
                      results_keep_days=args.results_keep_days)

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
