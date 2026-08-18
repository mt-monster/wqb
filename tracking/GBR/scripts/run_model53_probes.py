#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
"""
5-slot concurrent multisim runner for GBR model53 Stage-A probes.
Reads stageA expression files, keeps up to 5 multisim in flight (8 exprs each),
polls to terminal, fetches alpha IS metrics, writes JSON/CSV results.
"""
import csv
import json
import sys
import time
from pathlib import Path

# dataset 由命令行参数指定，默认 model53
DATASET = sys.argv[1] if len(sys.argv) > 1 else "model53"

TOOLKIT = Path(os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
sys.path.insert(0, str(TOOLKIT))

from _lib.common import CampaignContext, atomic_write, load_credentials
from _lib.api import Api, api_call
from _lib.poller import TERMINAL
import metrics_cache

DATASETS = {
    DATASET: f"tracking/GBR/candidates/probe_{DATASET}_stageA_exprs.json",
}
SLOTS = 5
BATCH_SIZE = 8
POLL_INTERVAL = 15
STALL_MINUTES = 8


def save_progress(out_json, out_csv, results, candidates):
    results_sorted = sorted(
        results,
        key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99),
    )
    payload = {
        "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "slots": SLOTS,
        "batch_size": BATCH_SIZE,
        "total_alphas": len(results_sorted),
        "candidates": candidates,
        "results": results_sorted,
    }
    atomic_write(str(out_json), payload)
    fieldnames = [
        "id", "dataset", "code", "sharpe", "fitness", "two_year_sharpe",
        "margin_bp", "turnover_pct", "rn_sharpe", "rn_fitness",
        "failed_checks", "multisim", "batch_idx",
    ]
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in results_sorted:
            w.writerow(r)
    print(f"[save] rows={len(results_sorted)} candidates={len(candidates)}")


def load_batches(ds):
    exprs = json.load(open(DATASETS[ds], encoding="utf-8"))
    return [exprs[i : i + BATCH_SIZE] for i in range(0, len(exprs), BATCH_SIZE)]


def submit_batch(api, settings, ds, batch_idx, batch):
    payloads = [
        {
            "type": "REGULAR",
            "settings": {k: v for k, v in settings.items() if not k.startswith("_")},
            "regular": e,
        }
        for e in batch
    ]
    body = payloads[0] if len(payloads) == 1 else payloads
    r = api_call(api, "post", "/simulations", body)
    loc = r.headers.get("Location") or ""
    msid = loc.rstrip("/").split("/")[-1]
    print(f"[submit] {ds} batch{batch_idx+1} multisim={msid} n={len(batch)}")
    return msid


def fetch_rows_for_multisim(api, fetcher, msid):
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
    return [fetcher.fetch(aid) for aid in ids]


def passes_user_thresholds(r, t):
    if r.get("sharpe") is None:
        return False
    if not (r.get("sharpe") > t["sharpe_min"]):
        return False
    if not ((r.get("fitness") or 0) > t["fitness_min"]):
        return False
    if not ((r.get("two_year_sharpe") or 0) > t["two_year_sharpe_min"]):
        return False
    if not ((r.get("margin_bp") or 0) > t["margin_min"] * 10000):
        return False
    tv = r.get("turnover_pct")
    if tv is None:
        return False
    if not (t["turnover_min"] * 100 < tv < t["turnover_max"] * 100):
        return False
    if r.get("failed_checks"):
        return False
    rn = {"sharpe": r.get("rn_sharpe"), "fitness": r.get("rn_fitness")}
    if not (rn["sharpe"] is not None and rn["sharpe"] > 1.0):
        return False
    if not ((rn["fitness"] or 0) > 0.7):
        return False
    return True


def main():
    ctx = CampaignContext("tracking/GBR")
    settings = ctx.settings
    thresholds = ctx.thresh("review")

    api = Api()
    api.login(*load_credentials())
    fetcher = metrics_cache.MetricsFetcher(ctx)

    pending = {ds: load_batches(ds) for ds in DATASETS}
    inflight = {}
    results = []
    candidates = []

    out_dir = Path("tracking/GBR/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / f"5slot_{DATASET}_probe_results.json"
    out_csv = out_dir / f"5slot_{DATASET}_probe_results.csv"

    for ds in DATASETS:
        if len(inflight) >= SLOTS:
            break
        if pending[ds]:
            batch = pending[ds].pop(0)
            msid = submit_batch(api, settings, ds, 0, batch)
            inflight[msid] = {"ds": ds, "batch_idx": 0, "batch": batch}
            time.sleep(0.3)

    last_seen = {}

    while inflight:
        done = []
        now = time.time()
        for msid in list(inflight.keys()):
            rec = inflight[msid]
            try:
                d = json.load(api.get(f"/simulations/{msid}"))
            except Exception as e:
                print(f"[poll] {msid} check err {e}", file=sys.stderr)
                continue
            status = d.get("status")
            progress = d.get("progress")

            if status not in TERMINAL:
                prev_prog, prev_ts = last_seen.get(msid, (None, now))
                if progress != prev_prog:
                    last_seen[msid] = (progress, now)
                elif now - prev_ts > STALL_MINUTES * 60:
                    print(f"[stall] {msid} {rec['ds']} progress={progress} unchanged for {STALL_MINUTES}min, treating as STALLED")
                    done.append(msid)
                    for expr in rec["batch"]:
                        results.append({
                            "id": "STALLED",
                            "dataset": rec["ds"],
                            "code": expr,
                            "multisim": msid,
                            "batch_idx": rec["batch_idx"],
                            "error": "STALLED",
                        })
                else:
                    print(f"[poll] {msid} {rec['ds']} status={status} progress={progress}")
                continue

            print(f"[poll] {msid} {rec['ds']} -> {status}")
            done.append(msid)
            if msid in last_seen:
                del last_seen[msid]
            rows = fetch_rows_for_multisim(api, fetcher, msid)
            for r in rows:
                if isinstance(r, dict) and "error" not in r:
                    r["dataset"] = rec["ds"]
                    r["multisim"] = msid
                    r["batch_idx"] = rec["batch_idx"]
                    results.append(r)
                    if passes_user_thresholds(r, thresholds):
                        candidates.append(r)
            ds = rec["ds"]
            if pending[ds]:
                new_idx = rec["batch_idx"] + 1
                new_batch = pending[ds].pop(0)
                new_msid = submit_batch(api, settings, ds, new_idx, new_batch)
                inflight[new_msid] = {"ds": ds, "batch_idx": new_idx, "batch": new_batch}
                last_seen[new_msid] = (None, time.time())
                time.sleep(0.3)

        for msid in done:
            if msid in inflight:
                del inflight[msid]

        if results or candidates:
            save_progress(out_json, out_csv, results, candidates)

        if inflight:
            time.sleep(POLL_INTERVAL)

    results.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))

    payload = {
        "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "slots": SLOTS,
        "batch_size": BATCH_SIZE,
        "total_alphas": len(results),
        "candidates": candidates,
        "results": results,
    }
    atomic_write(str(out_json), payload)
    print(f"[save] {out_json}  rows={len(results)} candidates={len(candidates)}")

    fieldnames = [
        "id", "dataset", "code", "sharpe", "fitness", "two_year_sharpe",
        "margin_bp", "turnover_pct", "rn_sharpe", "rn_fitness",
        "failed_checks", "multisim", "batch_idx",
    ]
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in results:
            w.writerow(r)
    print(f"[save] {out_csv}")

    print("\n=== TOP 10 SHARPE ===")
    for r in results[:10]:
        print(
            f"{r['id']} {r['dataset']:<22} sh={r.get('sharpe') or 0:.2f} "
            f"fit={r.get('fitness') or 0:.2f} 2y={r.get('two_year_sharpe') or 0:.2f} "
            f"mg={r.get('margin_bp') or 0:.1f}bp tvr={r.get('turnover_pct') or 0:.1f}% "
            f"rn={r.get('rn_sharpe') or 0:.2f}"
        )
    print(f"\nUSER-THRESHOLD candidates: {len(candidates)}")


if __name__ == "__main__":
    main()
