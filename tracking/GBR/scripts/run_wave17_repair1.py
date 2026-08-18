#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
"""wave17 batch1 修复批：单 multisim 8 表达式（bucket 已换 ts_zscore）。"""
import csv
import json
import sys
import time
from pathlib import Path

TOOLKIT = Path(os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
sys.path.insert(0, str(TOOLKIT))

from _lib.common import CampaignContext, atomic_write, load_credentials
from _lib.api import Api, api_call
from _lib.poller import TERMINAL
import metrics_cache

DATASET = "predictive_starmine"
INPUT = "tracking/GBR/candidates/gbr_wave17_repair1_exprs.json"
POLL_INTERVAL = 15
STALL_MINUTES = 8


def main():
    ctx = CampaignContext("tracking/GBR")
    settings = ctx.settings
    api = Api()
    api.login(*load_credentials())
    fetcher = metrics_cache.MetricsFetcher(ctx)

    exprs = json.load(open(INPUT, encoding="utf-8"))
    payloads = [
        {
            "type": "REGULAR",
            "settings": {k: v for k, v in settings.items() if not k.startswith("_")},
            "regular": e,
        }
        for e in exprs
    ]
    r = api_call(api, "post", "/simulations", payloads)
    loc = r.headers.get("Location") or ""
    msid = loc.rstrip("/").split("/")[-1]
    print(f"[submit] repair1 multisim={msid} n={len(exprs)}")

    last_prog, last_ts = None, time.time()
    while True:
        d = json.load(api.get(f"/simulations/{msid}"))
        status, progress = d.get("status"), d.get("progress")
        if status in TERMINAL:
            print(f"[poll] {msid} -> {status}")
            break
        if progress != last_prog:
            last_prog, last_ts = progress, time.time()
        elif time.time() - last_ts > STALL_MINUTES * 60:
            print(f"[stall] {msid} unchanged {STALL_MINUTES}min")
            break
        print(f"[poll] {msid} status={status} progress={progress}")
        time.sleep(POLL_INTERVAL)

    ms = json.load(api.get(f"/simulations/{msid}"))
    rows = []
    ids = []
    for c in ms.get("children", []):
        try:
            sim = json.load(api.get(f"/simulations/{c}"))
            if sim.get("status") in ("ERROR", "CANCELLED"):
                print(f"[child] {c} {sim.get('status')} msg={sim.get('message', '')[:80]}")
            if sim.get("alpha"):
                ids.append(sim["alpha"])
        except Exception as e:
            print(f"[child] {c} err {e}", file=sys.stderr)
    if not ids and ms.get("alpha"):
        ids.append(ms["alpha"])
    for aid in ids:
        r = fetcher.fetch(aid)
        if isinstance(r, dict) and "error" not in r:
            r["dataset"] = DATASET
            r["multisim"] = msid
            rows.append(r)

    rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    out_json = Path("tracking/GBR/results/wave17_repair1_results.json")
    out_csv = Path("tracking/GBR/results/wave17_repair1_results.csv")
    atomic_write(str(out_json), {
        "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": DATASET, "multisim": msid, "total_alphas": len(rows), "results": rows,
    })
    fieldnames = [
        "id", "dataset", "code", "sharpe", "fitness", "two_year_sharpe",
        "margin_bp", "turnover_pct", "rn_sharpe", "rn_fitness", "failed_checks", "multisim",
    ]
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("\n=== repair1 results ===")
    for r in rows:
        print(
            f"{r['id']} sh={r.get('sharpe') or 0:.2f} fit={r.get('fitness') or 0:.2f} "
            f"2y={r.get('two_year_sharpe') or 0:.2f} mg={r.get('margin_bp') or 0:.1f}bp "
            f"tvr={r.get('turnover_pct') or 0:.1f}% rn={r.get('rn_sharpe') or 0:.2f} "
            f"{r.get('code', '')[:50]}"
        )


if __name__ == "__main__":
    main()
