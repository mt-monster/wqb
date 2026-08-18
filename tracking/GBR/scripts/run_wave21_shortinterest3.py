#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wave21 shortinterest3 five-slot backtest runner.
Input gbr_wave21_exprs.json (meta+expressions), single dataset 3 batches x 8 exprs,
5 multisim concurrent fill, poll to TERMINAL, fetch IS metrics, write JSON/CSV.
"""
import csv
import json
import sys
import time
from pathlib import Path

TOOLKIT = Path("C:/Users/MENGTAO/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts")
sys.path.insert(0, str(TOOLKIT))

from _lib.common import CampaignContext, atomic_write, load_credentials
from _lib.api import Api, api_call
from _lib.poller import TERMINAL
import metrics_cache

DATASET = "shortinterest3"
INPUT = "tracking/GBR/candidates/gbr_wave21_exprs.json"
SLOTS = 5
BATCH_SIZE = 8
POLL_INTERVAL = 15
STALL_MINUTES = 8


def save_progress(out_json, out_csv, results, candidates):
    results_sorted = sorted(
        results, key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99)
    )
    payload = {
        "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": DATASET,
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


def load_batches():
    d = json.load(open(INPUT, encoding="utf-8"))
    exprs = d.get("expressions") or d.get("exprs") or d
    return [exprs[i : i + BATCH_SIZE] for i in range(0, len(exprs), BATCH_SIZE)]


def submit_batch(api, settings, batch_idx, batch):
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
    print(f"[submit] {DATASET} batch{batch_idx+1} multisim={msid} n={len(batch)}")
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
    rows = []
    for aid in ids:
        r = fetcher.fetch(aid)
        if isinstance(r, dict) and "error" not in r:
            rows.append(r)
        else:
            print(f"[child] alpha {aid} fetch err: {r}", file=sys.stderr)
    return rows


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

    pending = load_batches()
    inflight = {}
    results = []
    candidates = []

    out_dir = Path("tracking/GBR/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "wave21_shortinterest3_results.json"
    out_csv = out_dir / "wave21_shortinterest3_results.csv"

    # initial fill
    while len(inflight) < SLOTS and pending:
        batch = pending.pop(0)
        msid = submit_batch(api, settings, 0, batch)
        inflight[msid] = {"batch_idx": 0, "batch": batch}
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
                    print(f"[stall] {msid} progress={progress} unchanged {STALL_MINUTES}min, STALLED")
                    done.append(msid)
                    for expr in rec["batch"]:
                        results.append({
                            "id": "STALLED", "dataset": DATASET, "code": expr,
                            "multisim": msid, "batch_idx": rec["batch_idx"], "error": "STALLED",
                        })
                else:
                    print(f"[poll] {msid} status={status} progress={progress}")
                continue

            print(f"[poll] {msid} -> {status}")
            done.append(msid)
            if msid in last_seen:
                del last_seen[msid]
            rows = fetch_rows_for_multisim(api, fetcher, msid)
            for r in rows:
                r["dataset"] = DATASET
                r["multisim"] = msid
                r["batch_idx"] = rec["batch_idx"]
                results.append(r)
                if passes_user_thresholds(r, thresholds):
                    candidates.append(r)
            if pending:
                new_idx = rec["batch_idx"] + 1
                new_batch = pending.pop(0)
                new_msid = submit_batch(api, settings, new_idx, new_batch)
                inflight[new_msid] = {"batch_idx": new_idx, "batch": new_batch}
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
        "dataset": DATASET,
        "slots": SLOTS,
        "batch_size": BATCH_SIZE,
        "total_alphas": len(results),
        "candidates": candidates,
        "results": results,
    }
    atomic_write(str(out_json), payload)
    print(f"[save] {out_json} rows={len(results)} candidates={len(candidates)}")

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
            f"{r['id']} sh={r.get('sharpe') or 0:.2f} fit={r.get('fitness') or 0:.2f} "
            f"2y={r.get('two_year_sharpe') or 0:.2f} mg={r.get('margin_bp') or 0:.1f}bp "
            f"tvr={r.get('turnover_pct') or 0:.1f}% rn={r.get('rn_sharpe') or 0:.2f}"
        )
    print(f"\nUSER-THRESHOLD candidates: {len(candidates)}")


if __name__ == "__main__":
    main()
