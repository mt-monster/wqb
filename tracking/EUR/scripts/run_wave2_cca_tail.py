#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wave2 chart_cnn_alpha tail collector.
主 runner 因 PermissionError 崩溃后，收割最后一批在飞 multisim 的结果，
合并进 wave2_cca_probe_results.json / csv。
"""
import csv
import json
import sys
import time
from pathlib import Path

TOOLKIT = Path("C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts")
sys.path.insert(0, str(TOOLKIT))

from _lib.common import CampaignContext, atomic_write, load_credentials
from _lib.api import Api
from _lib.poller import TERMINAL
import metrics_cache

DATASET = "chart_cnn_alpha"
MSID = "2ziQcAaRT5eH9xzvXuJsTxJ"
OUT_JSON = Path("tracking/EUR/results/wave2_cca_probe_results.json")
OUT_CSV = Path("tracking/EUR/results/wave2_cca_probe_results.csv")
POLL_INTERVAL = 20


def fetch_rows(api, fetcher, msid):
    ms = json.load(api.get(f"/simulations/{msid}"))
    ids = []
    for c in ms.get("children", []):
        try:
            sim = json.load(api.get(f"/simulations/{c}"))
            if sim.get("alpha"):
                ids.append(sim["alpha"])
        except Exception as e:
            print(f"[child] {c} err {e}", file=sys.stderr)
    if not ids and ms.get("alpha"):
        ids.append(ms["alpha"])
    rows = []
    for aid in ids:
        r = fetcher.fetch(aid)
        if isinstance(r, dict) and "error" not in r:
            rows.append(r)
        else:
            print(f"[child] alpha {aid} fetch err: {r}", file=sys.stderr)
    return rows


def main():
    ctx = CampaignContext("tracking/EUR")
    api = Api()
    api.login(*load_credentials())
    fetcher = metrics_cache.MetricsFetcher(ctx)

    while True:
        d = json.load(api.get(f"/simulations/{MSID}"))
        status = d.get("status")
        progress = d.get("progress")
        print(f"[tail] status={status} progress={progress}")
        if status in TERMINAL:
            break
        time.sleep(POLL_INTERVAL)

    rows = fetch_rows(api, fetcher, MSID)
    print(f"[tail] fetched {len(rows)} rows")
    if not rows:
        print("[tail] no rows, exit")
        return

    payload = json.load(open(OUT_JSON, encoding="utf-8"))
    existing_codes = {r.get("code") for r in payload.get("results", [])}
    new_results = []
    for r in rows:
        r["dataset"] = DATASET
        r["multisim"] = MSID
        r["batch_idx"] = 0
        if r.get("code") in existing_codes:
            continue
        new_results.append(r)
    payload["results"].extend(new_results)
    payload["results"].sort(
        key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99)
    )
    payload["total_alphas"] = len(payload["results"])
    payload["ran_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    atomic_write(str(OUT_JSON), payload)

    fieldnames = [
        "id", "dataset", "code", "decay", "truncation", "sharpe", "fitness",
        "two_year_sharpe", "margin_bp", "turnover_pct", "rn_sharpe", "rn_fitness",
        "failed_checks", "multisim", "batch_idx",
    ]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in payload["results"]:
            w.writerow(r)

    print(f"[tail] merged rows={len(payload['results'])} new={len(new_results)}")
    for r in payload["results"][:12]:
        print(
            f"{r['id']} sh={r.get('sharpe') or 0:.2f} fit={r.get('fitness') or 0:.2f} "
            f"2y={r.get('two_year_sharpe') or 0:.2f} mg={r.get('margin_bp') or 0:.1f}bp "
            f"tvr={r.get('turnover_pct') or 0:.1f}% rn={r.get('rn_sharpe') or 0:.2f} "
            f"rnf={r.get('rn_fitness') or 0:.2f} {r.get('code', '')[:40]}"
        )


if __name__ == "__main__":
    main()
