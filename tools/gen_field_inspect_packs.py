#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 WebDataScope 数据包生成体检硬门用的按数据集分文件体检包。

体检硬门（`tools/field_inspect_gate.py`，接在 `tools/wave_gate.py` 里）需要
`tracking/mining/field_inspect_<region 小写>_<dataset>.json`。本脚本负责产出它们。

为什么不直接用 `webdata_quality.py --export-expr`：
  1. 它一次导出整个 region×delay 的全部数据集到**一个** 29 MB 文件，而闸每次
     只查一个数据集 —— 每波解析 29 MB JSON 纯属浪费；
  2. 文件里 60% 体积是 `expressions`（候选表达式建议），闸只用
     `metadata` + `advices`，不需要。

所以这里做两件事：调一次导出拿到全量，然后**瘦身 + 按数据集拆分**
（USA/D1 实测 29 MB / 102 数据集 → 每个约 135 KB）。

    python tools/gen_field_inspect_packs.py --region USA --delay 1
    python tools/gen_field_inspect_packs.py --all          # 数据包里所有 region×delay
    python tools/gen_field_inspect_packs.py --all --dry-run

注：2026-09-07 修复 `webdata_quality.py` 的 `rsplit('_', 2)` 越界 bug 之前，
`--export-expr` 恒产出 0 字段 —— 现存两份体检包 `fields` 为空即源于此。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from typing import Dict, List, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ZIP = os.path.join(REPO_ROOT, "research-data", "WebData_20260219_V0.10.9.zip")
OUT_DIR = os.path.join(REPO_ROOT, "tracking", "mining")
WEBDATA = os.path.join(REPO_ROOT, "tools", "webdata_quality.py")

#: 闸只消费这两个键，其余（expressions 等）不落盘
KEEP_KEYS = ("field", "metadata", "advices")


def available_combos(zip_path: str) -> List[Tuple[str, int]]:
    """数据包里存在的 (region, delay) 组合。"""
    with zipfile.ZipFile(zip_path) as zf:
        dsl = json.loads(zf.read("data/dataSetList.json"))
    combos = set()
    for name in dsl:
        parts = name.split("_")
        if len(parts) < 4:
            continue
        region, delay = parts[1], parts[3]
        if not delay.startswith("Delay"):
            continue  # 如 ASI 的 MINVOL1M 档，非标准 delay 维度
        combos.add((region, int(delay[len("Delay"):])))
    return sorted(combos)


def export_combined(zip_path: str, region: str, delay: int, py: str) -> Dict:
    """调 webdata_quality.py 导出该 region×delay 的全量体检数据。"""
    fd, tmp = tempfile.mkstemp(suffix=".json", prefix=f"fi_{region}_d{delay}_")
    os.close(fd)
    cmd = [py, WEBDATA, "--zip", zip_path, "--region", region,
           "--delay", str(delay), "--export-expr", tmp]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=REPO_ROOT)
    if proc.returncode != 0:
        os.unlink(tmp)
        raise RuntimeError(
            f"webdata_quality.py 失败 rc={proc.returncode}: "
            f"{(proc.stderr or proc.stdout or '')[-500:]}"
        )
    try:
        with open(tmp, "r", encoding="utf-8") as f:
            return json.load(f)
    finally:
        os.unlink(tmp)


def slim_entry(entry: Dict) -> Dict:
    return {k: entry.get(k) for k in KEEP_KEYS if k in entry}


def write_packs(data: Dict, region: str, delay: int, dry_run: bool) -> Tuple[int, int]:
    """按数据集拆分写盘，返回 (数据集数, 字段数)。"""
    fields = data.get("fields") or {}
    n_ds = n_field = 0
    for dataset, entries in sorted(fields.items()):
        if not entries:
            continue
        pack = {
            "region_delay": data.get("region_delay"),
            "neutralization": data.get("neutralization"),
            "delay": delay,
            "source": "webdata_quality.py --export-expr (slim: metadata+advices)",
            "fields": {dataset: {k: slim_entry(v) for k, v in entries.items()}},
        }
        out = os.path.join(
            OUT_DIR, f"field_inspect_{region.lower()}_{dataset}.json"
        )
        n_ds += 1
        n_field += len(entries)
        if dry_run:
            continue
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(pack, f, ensure_ascii=False)
    return n_ds, n_field


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--zip", default=DEFAULT_ZIP)
    ap.add_argument("--region", default=None)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--all", action="store_true",
                    help="数据包里所有 region×delay 组合")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--py", default=sys.executable)
    a = ap.parse_args()

    if not os.path.isfile(a.zip):
        print(f"[packs] 数据包不存在：{a.zip}", file=sys.stderr)
        return 2

    if a.all:
        combos = available_combos(a.zip)
    elif a.region:
        combos = [(a.region.upper(), a.delay)]
    else:
        print("[packs] 需指定 --region 或 --all", file=sys.stderr)
        return 2

    print(f"[packs] 数据包 {os.path.basename(a.zip)}；待处理 {len(combos)} 个组合")
    total_ds = total_field = 0
    for region, delay in combos:
        try:
            data = export_combined(a.zip, region, delay, a.py)
        except Exception as e:
            print(f"  {region}/D{delay}: 导出失败 —— {e}")
            continue
        n_ds, n_field = write_packs(data, region, delay, a.dry_run)
        total_ds += n_ds
        total_field += n_field
        print(f"  {region}/D{delay}: {n_ds} 数据集 / {n_field} 字段"
              + ("（dry-run，未写盘）" if a.dry_run else ""))

    verb = "将生成" if a.dry_run else "已生成"
    print(f"[packs] {verb} {total_ds} 个体检包，覆盖 {total_field} 个字段 → {OUT_DIR}")
    if total_ds == 0:
        print("[packs] 一个都没产出 —— 检查 region/delay 是否在数据包里"
              "（--all 可列出全部组合）", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
