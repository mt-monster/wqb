#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""reset_low_cov_skips.py — 把 SKIPPED_LOW_COV 的集从断点/结果里摘除，使其重新入队。

背景（2026-10-25）
------------------
覆盖率门槛 0.8 → 0.6 后，原先被判 SKIPPED_LOW_COV 的 32 个集里有 11 个（cov 0.60–0.79）
应当真正开跑。但 checkpoint 的 `done` 已把它们标记完成，续跑会直接跳过
⇒ 必须把它们从 `done` 与 `results` 里摘掉，流水线才会重新排到它们。

安全设计
--------
* 只动 `verdict == SKIPPED_LOW_COV` 的条目；`SKIPPED_TOO_FEW_FIELDS` / `DEAD` / `ALIVE` 一律不碰
  （TOO_FEW_FIELDS 是字段数不足，与覆盖率无关，放宽覆盖率不影响它）。
* 先备份到 `results/_reset_backup_<ts>/`，再原子写。
* 断言：摘除后 `done` 里不应再出现任何 SKIPPED_LOW_COV 的集名。

用法
----
  python tools/reset_low_cov_skips.py --dry-run     # 只看会摘谁
  python tools/reset_low_cov_skips.py               # 执行
"""
import argparse
import json
import os
import shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CKPT = os.path.join(ROOT, "results", "full_template_campaign_checkpoint.json")
RESULTS = os.path.join(ROOT, "results", "full_template_campaign_results.json")
DIGEST = os.path.join(ROOT, "results", "campaign_digest.md")
TARGET = "SKIPPED_LOW_COV"


def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ck = json.load(open(CKPT, encoding="utf-8"))
    res = json.load(open(RESULTS, encoding="utf-8"))
    rs = res.get("results") or {}
    done = list(ck.get("done") or [])

    victims = [k for k, v in rs.items()
               if isinstance(v, dict) and v.get("verdict") == TARGET]
    victims.sort()
    print(f"[reset] 待摘除 {TARGET} = {len(victims)} 个")
    print(f"[reset] 摘除前 done={len(done)}")
    for k, v in sorted(((k, rs[k]) for k in victims), key=lambda x: -(x[1].get("coverage") or 0)):
        cov = v.get("coverage")
        print(f"   {k:28s} cov={cov:.3f}" if cov is not None else f"   {k}")

    if args.dry_run:
        print("[reset] dry-run，未改动")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(ROOT, "results", f"_reset_backup_{ts}")
    os.makedirs(bdir, exist_ok=True)
    for p in (CKPT, RESULTS):
        shutil.copy2(p, os.path.join(bdir, os.path.basename(p)))
    print(f"[reset] 已备份到 {bdir}")

    for k in victims:
        rs.pop(k, None)
        if k in done:
            done.remove(k)
        (ck.get("sims") or {}).pop(k, None)

    ck["done"] = done
    res["results"] = rs
    atomic_write_json(CKPT, ck)
    atomic_write_json(RESULTS, res)

    # 断言：done 里不再有 SKIPPED_LOW_COV 的集
    left = [k for k in done if (rs.get(k) or {}).get("verdict") == TARGET]
    assert not left, f"仍残留 {left}"

    # digest 里也把对应行删掉，避免汇报口径与 done 不一致（同集重跑会重新追加）
    if os.path.exists(DIGEST):
        keep = []
        for line in open(DIGEST, encoding="utf-8"):
            if any(f"**{k}**(" in line for k in victims):
                continue
            keep.append(line)
        tmp = DIGEST + ".tmp"
        open(tmp, "w", encoding="utf-8").writelines(keep)
        os.replace(tmp, DIGEST)
        print(f"[reset] digest 已清理，剩余 {len(keep)} 行")

    print(f"[reset] 完成：done {len(done)}，results {len(rs)}")


if __name__ == "__main__":
    main()
