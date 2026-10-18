#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 `tracking/MANIFEST.json`（全量索引 + 逻辑统一名），并可选把 >500 KB 大件压一份
zip 到 `tracking/archive/large/`（冷备，原件保留）。

用法（2026-10-14 加 `--dry-run` / `--no-archive`，此前**只有**「写索引 + 压 zip」一种形态）：

    python tracking/reference/tooling/generate_manifest.py --dry-run     # 只量，不落任何盘
    python tracking/reference/tooling/generate_manifest.py --no-archive  # 只写 MANIFEST.json
    python tracking/reference/tooling/generate_manifest.py               # 旧默认：写索引 + 压 zip

为什么要加这两个开关：`--dry-run` 让「副作用规模」在跑之前可核对（实测索引面 13,866 件 /
78.2 MB，>500 KB 的 19 件合计 17.8 MB 会被**再压一份**进 `tracking/archive/large/`，
而该目录 git 不跟踪 —— 正是 AGENTS.md §8.4 第 6 条「磁盘只增不减」的那类增量）；
`--no-archive` 让「只要索引」这个真实需求不必连带造 17.8 MB 未跟踪二进制。

`BASE` 原先写死 `r"D:\\coding\\traeCN_project\\wqb\\tracking"`：仓库一挪盘（或别人克隆）
就静默指错目录，且 `tracking/` **不在** `audit_structure` S4 的扫描面（只 src/ + tools/），
所以这条硬编码没有任何闸看得见。现按 AGENTS.md §8.13 改为向上探测
`pyproject.toml` + `src/wqb` 双标记定仓库根，与文件自身层数解耦。
"""
import argparse
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path


def _find_repo_root() -> Path:
    """向上探测双标记定仓库根——**与文件层数无关**（AGENTS.md §8.13 禁层数硬编码）。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            return parent
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


BASE = str(_find_repo_root() / "tracking")

STAGE_MAP = {
    "candidates": "cand", "results": "result", "reviews": "review",
    "reports": "report", "scripts": "script", "reference": "ref",
    "ra": "ra", "ppa": "ppa", "deepexplore": "deep", "sims": "sim",
}
TYPE_KW = [
    ("review", "review"), ("eval", "eval"), ("verdict", "verdict"),
    ("report", "report"), ("summary", "summary"), ("recap", "recap"),
    ("candidate", "cand"), ("seed", "seed"), ("plan", "plan"),
    ("exprs", "exprs"), ("expression", "exprs"), ("matrix", "matrix"),
    ("fields", "fields"), ("field", "fields"), ("score", "score"),
    ("whitelist", "whitelist"), ("campaign", "campaign"),
    ("diversity", "diversity"), ("family", "family"), ("orthogonal", "ortho"),
    ("minusrank", "minusrank"), ("boost", "boost"), ("fix", "fix"),
    ("dilute", "dilute"), ("ai_model", "aimodel"), ("model", "model"),
    ("chart", "chart"), ("state", "state"), ("list", "list"),
    ("alpha", "alpha"), ("dataset", "dataset"), ("args", "args"),
    ("idea", "idea"), ("result", "result"), ("metric", "metric"),
    ("sim", "sim"), ("break", "break"), ("final", "final"),
    ("valid", "valid"), ("output", "output"), ("health", "health"),
    ("recommendation", "reco"), ("feature", "feature"),
    ("portability", "port"), ("academic", "academic"), ("method", "method"),
    ("search", "search"), ("supplement", "supplement"), ("condensed", "condensed"),
    ("dump", "dump"), ("poll", "poll"), ("submit", "submit"),
    ("enhance", "enhance"), ("progress", "progress"), ("loop", "loop"),
    ("quality", "quality"), ("pdf", "pdf"), ("multiplier", "mult"),
    ("forum", "forum"), ("new", "new"), ("cs1600", "cs1600"),
]

REGIONS = {"EUR", "KOR", "USA", "IND", "GLB", "DEU", "FORUM"}


def derive_type(name):
    low = name.lower()
    for kw, label in TYPE_KW:
        if kw in low:
            return label
    return os.path.splitext(name)[1].lstrip(".") or "data"


def unified_name(region, life, name):
    stage = STAGE_MAP.get(life, life)
    m = re.search(r'(wave|v|round|batch|d|step)(\d+)', name.lower())
    wave = m.group(2) if m else "x"
    type_ = derive_type(name)
    return f"{region}_{stage}_{wave}_{type_}"


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="生成 tracking/MANIFEST.json（默认还会把 >500 KB 件压一份 zip 进 "
                    "tracking/archive/large/，原件保留）。--dry-run 只量不写；"
                    "--no-archive 只写索引不压 zip。")
    ap.add_argument("--dry-run", action="store_true",
                    help="只统计并打印（索引面件数 / >500 KB 件数与体积），不写 MANIFEST.json、"
                         "不压 zip、不删临时件")
    ap.add_argument("--no-archive", action="store_true",
                    help="写 MANIFEST.json，但跳过 >500 KB 的 zip 冷备（避免在 git 不跟踪的 "
                         "tracking/archive/large/ 里堆二进制）")
    args = ap.parse_args(argv)

    # load move map for original paths
    orig = {}
    mm = os.path.join(BASE, "_move_map.json")
    if os.path.exists(mm):
        with open(mm, encoding="utf-8") as f:
            mv = json.load(f)  # old_rel -> new_rel
        inv = {v: k for k, v in mv.items()}
    else:
        inv = {}

    records = []
    for root, dirs, files in os.walk(BASE):
        # skip archive, backup, temp, manifest itself
        rel_root = os.path.relpath(root, BASE)
        parts = rel_root.split(os.sep)
        top = parts[0] if rel_root != "." else "(root)"
        if top in ("archive",) or rel_root.startswith("archive"):
            continue
        if "tracking_backup" in root:
            continue
        for fn in files:
            if fn in ("MANIFEST.json", "_move_map.json", "_inventory_tmp.json"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, BASE).replace(os.sep, "/")
            try:
                sz = os.path.getsize(full)
            except OSError:
                sz = -1
            # region + lifecycle
            region = top if top in REGIONS else (top if top in ("reference", "mining", "sessions", "runs") else "GLOBAL")
            life = parts[1] if len(parts) > 1 else "root"
            if region in ("reference", "mining", "sessions", "runs"):
                life = life if life != "root" else region
            ext = os.path.splitext(fn)[1].lstrip(".").lower()
            u = unified_name(region if region in REGIONS else top, life, fn)
            orig_path = inv.get(rel)
            records.append({
                "path": rel,
                "region": region if region in REGIONS else top,
                "lifecycle": life,
                "type": ext,
                "size_bytes": sz,
                "unified_name": u,
                "original_path": orig_path,
            })

    records.sort(key=lambda r: (r["region"], r["lifecycle"], r["path"]))
    large = [r for r in records if r["size_bytes"] > 500_000]
    total_mb = sum(r["size_bytes"] for r in records) / 1048576
    large_mb = sum(r["size_bytes"] for r in large) / 1048576

    # 旧写法把 "generated" 硬编码成 "2026-08-14"：产物会声称一个不是本次运行的日期，
    # 索引的新鲜度因此**不可信**（而新鲜度正是数据湖索引唯一的价值）。改为真实运行日。
    manifest = {
        "generated": time.strftime("%Y-%m-%d"),
        "base": "tracking/",
        "total_files": len(records),
        "total_bytes": sum(r["size_bytes"] for r in records),
        "regions": sorted(REGIONS),
        "lifecycle_dirs": ["candidates", "results", "reviews", "reports", "scripts", "reference"],
        "convention": "{REGION}/{lifecycle}/{REGION}_{stage}_{wave}_{type}.{ext}",
        "files": records,
    }

    print(f"索引面：{len(records)} 件 / {total_mb:.1f} MB；"
          f">500 KB 的 {len(large)} 件合计 {large_mb:.1f} MB")
    if args.dry_run:
        print("[dry-run] 未写 MANIFEST.json、未压 zip、未删临时件。")
        for r in large[:10]:
            print(f"   {r['size_bytes']/1048576:7.1f} MB  {r['path']}")
        return 0

    with open(os.path.join(BASE, "MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"MANIFEST.json written: {len(records)} files indexed.")

    # ---- scheme ④: archive large files (compressed cold backup, originals kept) ----
    if args.no_archive:
        print(f"[--no-archive] 跳过 {len(large)} 件大件的 zip 冷备"
              f"（{large_mb:.1f} MB 会落进 git 不跟踪的 tracking/archive/large/）。")
    else:
        arch_dir = os.path.join(BASE, "archive", "large")
        os.makedirs(arch_dir, exist_ok=True)
        for r in large:
            src = os.path.join(BASE, r["path"])
            zname = os.path.basename(r["path"]).rsplit(".", 1)[0] + ".zip"
            zpath = os.path.join(arch_dir, zname)
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(src, os.path.basename(src))
            print(f"  archived -> archive/large/{zname} ({r['size_bytes']/1024:.0f}KB)")
        print(f"Archived {len(large)} large files (originals retained for compatibility).")

    # ---- scheme ⑥: remove temp inventory file ----
    tmp = os.path.join(BASE, "_inventory_tmp.json")
    if os.path.exists(tmp):
        os.remove(tmp)
        print("Removed temp _inventory_tmp.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
