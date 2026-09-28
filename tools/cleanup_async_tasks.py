#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""logs/_async_tasks TTL 归档清理工具（2026-09-25 结构优化目标 D）。

背景：logs/_async_tasks/ 下每个 detached 任务一个目录（gem/batch_track/campaign/fe），
含 meta.json + stdout.log + stderr.log，已积累 800+ 文件，无生命周期管理。

本工具：
  - 扫描根目录（resolve_async_tasks_root()，WQB_TASK_ROOT 可覆盖）；
  - 识别两种布局：dir 布局（<task_id>/meta.json）与 flat 布局（<task_id>.json / *.log）；
  - TTL 判定：dir 读 meta.json 的 finished_at（无则 started_at，再无则目录 mtime），
    flat 读文件 mtime；默认 7 天，--days N 覆盖；
  - 保护在飞任务：meta.json status 为 running/initializing 的一律跳过；
  - 归档而非删除（AGENTS.md 约束）：--apply 移动到 attic/async_tasks_<YYYYMMDD>/，
    默认 dry-run 只打印统计。

用法：
    python tools/cleanup_async_tasks.py            # dry-run，只打印统计
    python tools/cleanup_async_tasks.py --apply    # 归档超龄任务到 attic/
    python tools/cleanup_async_tasks.py --days 14  # 自定义 TTL
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from wqb.workflow._common import resolve_async_tasks_root  # noqa: E402


def _parse_ts(value) -> datetime | None:
    """尽力解析 ISO 时间戳为 aware datetime；失败返回 None。"""
    if not value:
        return None
    try:
        s = str(value).strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _dir_age_ts(task_dir: Path) -> datetime:
    """dir 布局的年龄时间戳：meta.finished_at > started_at > 目录 mtime。"""
    meta_file = task_dir / "meta.json"
    if meta_file.is_file():
        try:
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            for key in ("finished_at", "started_at"):
                ts = _parse_ts(meta.get(key))
                if ts:
                    return ts
        except Exception:
            pass
    return datetime.fromtimestamp(task_dir.stat().st_mtime, tz=timezone.utc)


def _is_active(task_dir: Path) -> bool:
    """meta.json status 为 running/initializing 视为在飞，跳过。"""
    meta_file = task_dir / "meta.json"
    if not meta_file.is_file():
        return False
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        status = str(meta.get("status") or "").lower()
        return status in ("running", "initializing", "pending")
    except Exception:
        return False


def scan(root: Path, ttl_days: int) -> dict:
    """扫描任务根目录，返回分类统计与超龄清单。"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=ttl_days)
    dirs = []       # (path, age_ts, size_bytes)
    flat = []       # (path, age_ts, size_bytes)
    active = 0
    total_dirs = 0
    total_flat = 0

    if not root.is_dir():
        return {"root": str(root), "cutoff": cutoff, "dirs": [], "flat": [], "active": 0,
                "total_dirs": 0, "total_flat": 0}

    for entry in root.iterdir():
        if entry.is_dir():
            total_dirs += 1
            if _is_active(entry):
                active += 1
                continue
            age = _dir_age_ts(entry)
            if age < cutoff:
                size = sum(f.stat().st_size for f in entry.rglob("*") if f.is_file())
                dirs.append((entry, age, size))
        elif entry.is_file():
            total_flat += 1
            age = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc)
            if age < cutoff:
                flat.append((entry, age, entry.stat().st_size))

    return {"root": str(root), "cutoff": cutoff, "dirs": dirs, "flat": flat,
            "active": active, "total_dirs": total_dirs, "total_flat": total_flat}


def main() -> int:
    ap = argparse.ArgumentParser(description="logs/_async_tasks TTL 归档清理")
    ap.add_argument("--days", type=int, default=7, help="TTL 天数（默认 7）")
    ap.add_argument("--apply", action="store_true", help="实际归档（默认 dry-run 只打印）")
    args = ap.parse_args()

    root = Path(resolve_async_tasks_root())
    result = scan(root, args.days)

    n_dirs = len(result["dirs"])
    n_flat = len(result["flat"])
    size_dirs = sum(s for _, _, s in result["dirs"])
    size_flat = sum(s for _, _, s in result["flat"])

    print(f"[cleanup] root={result['root']}")
    print(f"[cleanup] TTL={args.days}d cutoff={result['cutoff'].isoformat()}")
    print(f"[cleanup] dir 布局: 共 {result['total_dirs']}，在飞 {result['active']}，超龄 {n_dirs}（{size_dirs/1e6:.1f} MB）")
    print(f"[cleanup] flat 布局: 共 {result['total_flat']}，超龄 {n_flat}（{size_flat/1e6:.1f} MB）")

    if not args.apply:
        print("[cleanup] dry-run：未做任何移动。加 --apply 归档到 attic/。")
        if n_dirs:
            print("[cleanup] 超龄 dir 样例（前 10）:")
            for p, age, size in result["dirs"][:10]:
                print(f"  {p.name}  age={age.date()}  {size/1e6:.2f} MB")
        return 0

    # --apply：归档而非删除
    stamp = datetime.now().strftime("%Y%m%d")
    attic = REPO_ROOT / "attic" / f"async_tasks_{stamp}"
    moved = 0
    for p, _, _ in result["dirs"]:
        dst = attic / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dst))
        moved += 1
    for p, _, _ in result["flat"]:
        dst = attic / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dst))
        moved += 1
    print(f"[cleanup] 已归档 {moved} 项到 {attic}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
