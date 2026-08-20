# -*- coding: utf-8 -*-
"""archive_wave_results.py - 把已关闭的旧 wave 结果文件合并归档，活跃目录只留最近 N 个。

判断"已关闭"：文件内有最终裁决标记（key_findings 含 FINAL VERDICT / REJECTED / SUBMITTED）
或 wave 编号 < 当前最大编号 - keep_recent。

归档目标：tracking/<REGION>/results/_archive/waves_<min>-<max>.json（合并为一个文件）。
原文件移动到 _archive/raw/ 备份（不删除，防丢）。

用法：
  python tools/archive_wave_results.py --region MEA --keep-recent 5 --dry-run
  python tools/archive_wave_results.py --region MEA --keep-recent 5
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CLOSED_MARKERS = ("FINAL VERDICT", "REJECTED", "SUBMITTED", "EXHAUSTED", "DEAD")


def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def wave_num(p):
    m = re.search(r"wave(\d+)_results\.json$", p.name)
    return int(m.group(1)) if m else -1


def is_closed(data):
    """判断 wave 是否已关闭（有最终裁决）。data 可能是 dict 或 list。"""
    if isinstance(data, list):
        # 顶层是 list 的旧格式：整个序列化为文本扫描
        text = json.dumps(data, ensure_ascii=False)
        return any(m in text for m in CLOSED_MARKERS)
    if not isinstance(data, dict):
        return False
    findings = data.get("key_findings", [])
    if isinstance(findings, list):
        blob = " ".join(str(x) for x in findings)
    else:
        blob = str(findings)
    verdict = str(data.get("verdict", ""))
    status = str(data.get("status", ""))
    text = f"{blob} {verdict} {status}"
    return any(m in text for m in CLOSED_MARKERS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--keep-recent", type=int, default=5,
                    help="活跃目录保留最近 N 个 wave（默认 5）")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    results_dir = ROOT / "tracking" / args.region / "results"
    if not results_dir.exists():
        print(f"[ERROR] not found: {results_dir}")
        return 1

    files = sorted(results_dir.glob("wave*_results.json"), key=wave_num)
    if not files:
        print("[INFO] no wave files")
        return 0

    max_wave = max(wave_num(f) for f in files)
    threshold = max_wave - args.keep_recent

    to_archive = []
    for f in files:
        wn = wave_num(f)
        if wn < 0:
            continue
        try:
            data = load_json(f)
        except Exception as e:
            print(f"[SKIP] {f.name} parse error: {e}")
            continue
        closed = is_closed(data)
        old = wn <= threshold
        # 只归档“已关闭且旧”的：最近 N 个即使 CLOSED 也保留（可能还在跟进）
        if closed and old:
            to_archive.append((wn, f, data, closed, old))

    if not to_archive:
        print(f"[INFO] nothing to archive (max_wave={max_wave}, threshold={threshold})")
        return 0

    print(f"region={args.region}  max_wave={max_wave}  keep_recent={args.keep_recent}  threshold={threshold}")
    print(f"to_archive={len(to_archive)} / total={len(files)}")
    for wn, f, _, closed, old in to_archive:
        tag = []
        if closed:
            tag.append("CLOSED")
        if old:
            tag.append("OLD")
        print(f"  wave{wn:>3d}  {f.stat().st_size:>6d} B  [{'/'.join(tag)}]  {f.name}")

    if args.dry_run:
        print("[DRY-RUN] no changes made")
        return 0

    # 合并归档
    archive_dir = results_dir / "_archive"
    raw_dir = archive_dir / "raw"
    archive_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    merged = {
        "region": args.region,
        "archived_at": __import__("datetime").date.today().isoformat(),
        "wave_range": [min(w for w, *_ in to_archive), max(w for w, *_ in to_archive)],
        "count": len(to_archive),
        "waves": {f"wave{wn}": data for wn, _, data, *_ in to_archive},
    }
    out = archive_dir / f"waves_{merged['wave_range'][0]}-{merged['wave_range'][1]}.json"
    dump_json(out, merged)

    # 移动原文件到 raw 备份
    for wn, f, _, *_ in to_archive:
        shutil.move(str(f), str(raw_dir / f.name))

    print(f"[OK] archived {len(to_archive)} waves -> {out}")
    print(f"[OK] raw files moved -> {raw_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
