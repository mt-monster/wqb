# -*- coding: utf-8 -*-
"""dispatch_batch.py — 派发一批表达式去仿真，并**把 sim id 落盘**（防丢失）。

背景（2026-10-05 踩坑）：直接调 `tools/submit_batch.py` 若用 `| tail -N` 截断输出，
sim id（在 Location 头/打印的 URL 里）会被丢掉，之后无法收割。
本包装把完整输出写入 `cache/dispatch_<label>.log` 与 `cache/dispatch_ids.jsonl`。

⚠ 另注：`tools/submit_batch.py` 在**全部子任务都因并发上限失败**时**仍打印 `ALL SUBMITTED`**
（2026-10-05 实测），所以**必须检查输出里是否有 `status=201` / 有无 `CONCURRENT`**，
不能只看尾行。

用法：
  python tracking/GBR/scripts/dispatch_batch.py <expr_file> --label <名> [submit_batch 的其余参数…]
  # 例：
  python tracking/GBR/scripts/dispatch_batch.py cache/_x.txt --label m109d \
      --region GBR --universe TOP700 --delay 1 --decay 12 --neutralization STATISTICAL

默认会自动重试（并发上限最多 8 次、每次等 45s）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SUBMIT = os.path.join(ROOT, "tools", "submit_batch.py")
CACHE = os.path.join(ROOT, "cache")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("expr_file")
    ap.add_argument("--label", required=True)
    ap.add_argument("--retries", type=int, default=8)
    ap.add_argument("--wait", type=int, default=45)
    # ⚠ 不能用 argparse.REMAINDER：它会把 `--label` 等本脚本参数一并吞进 rest，
    #   导致报 "--label is required"（2026-10-05 实测）。用 parse_known_args。
    a, rest = ap.parse_known_args()
    if rest and rest[0] == "--":
        rest = rest[1:]

    py = sys.executable
    cmd = [py, SUBMIT, "--path", a.expr_file] + rest
    out, sim_url = "", None
    for i in range(a.retries):
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        out = (p.stdout or "") + (p.stderr or "")
        if "CONCURRENT_SIMULATION_LIMIT_EXCEEDED" in out:
            print(f"[dispatch] try{i + 1}: 并发上限，等 {a.wait}s")
            time.sleep(a.wait)
            continue
        m = re.search(r"https://api\.worldquantbrain\.com/simulations/([A-Za-z0-9]+)", out)
        sim_url = m.group(0) if m else None
        break

    os.makedirs(CACHE, exist_ok=True)
    log = os.path.join(CACHE, f"dispatch_{a.label}.log")
    open(log, "w", encoding="utf-8").write(out + "\n")
    ok = bool(sim_url) and "status=201" in out
    rec = {
        "ts": _dt.datetime.now().isoformat(timespec="seconds"),
        "label": a.label, "expr_file": a.expr_file, "sim_url": sim_url,
        "sim_id": sim_url.rsplit("/", 1)[-1] if sim_url else None,
        "ok": ok,
        "has_concurrent": "CONCURRENT_SIMULATION_LIMIT_EXCEEDED" in out,
        "log": os.path.relpath(log, ROOT),
    }
    with open(os.path.join(CACHE, "dispatch_ids.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
