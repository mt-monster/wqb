import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wave20 EUR intraday_pv_feats seasonal probe runner.
Input: eur_wave24_ipv_items.json [{code, note}],
5 multisim concurrent fill (batch_size=8), poll to TERMINAL, fetch IS metrics,
write JSON/CSV. 澶嶇敤 wave5 浜旀Ы濉Ы妯″紡锛坵qb-concurrency 搂8锛夈€?
"""
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

DATASET = "intraday_pv_feats"
INPUT = "tracking/EUR/candidates/eur_wave24_ipv_items.json"
SLOTS = 5
BATCH_SIZE = 8
POLL_INTERVAL = 15
STALL_MINUTES = 8
# 灞€閮ㄨ鐩栵細鐢ㄦ埛瑕佹眰鍙傝€?TOP700锛圗UR 鍚堟硶妗ｄ綅鏈€鎺ヨ繎 TOP800锛夛紱
# 涓嶄慨鏀瑰叡浜?settings.json锛堝閮ㄤ細璇?wave6c 浣跨敤 TOP2500锛岄伩鍏嶅啀娆￠厤缃啿绐侊級
UNIVERSE_OVERRIDE = "TOP2500"


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
        "id", "dataset", "code", "decay", "truncation", "sharpe", "fitness",
        "two_year_sharpe", "margin_bp", "turnover_pct", "rn_sharpe", "rn_fitness",
        "failed_checks", "multisim", "batch_idx",
    ]
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in results_sorted:
            w.writerow(r)
    print(f"[save] rows={len(results_sorted)} candidates={len(candidates)}")


def load_batches():
    items = json.load(open(INPUT, encoding="utf-8"))
    return [items[i : i + BATCH_SIZE] for i in range(0, len(items), BATCH_SIZE)]


def submit_batch(api, settings, batch_idx, batch):
    payloads = []
    for it in batch:
        s = {k: v for k, v in settings.items() if not k.startswith("_")}
        if it.get("decay") is not None:
            s["decay"] = it["decay"]
        if it.get("truncation") is not None:
            s["truncation"] = it["truncation"]
        if it.get("neut") is not None:
            s["neutralization"] = it["neut"]
        payloads.append({"type": "REGULAR", "settings": s, "regular": it["code"]})
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
    ctx = CampaignContext("tracking/EUR")
    settings = ctx.settings
    if UNIVERSE_OVERRIDE:
        settings["universe"] = UNIVERSE_OVERRIDE
    print(f"[universe] {settings['universe']} (override={UNIVERSE_OVERRIDE or 'off'})")
    thresholds = ctx.thresh("review")

    api = Api()
    api.login(*load_credentials())
    fetcher = metrics_cache.MetricsFetcher(ctx)

    pending = load_batches()
    inflight = {}
    results = []
    candidates = []

    out_dir = Path("tracking/EUR/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "wave24_ipv_results.json"
    out_csv = out_dir / "wave24_ipv_results.csv"

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
                    for it in rec["batch"]:
                        results.append({
                            "id": "STALLED", "dataset": DATASET, "code": it["code"],
                            "decay": it.get("decay"), "truncation": it.get("truncation"),
                            "multisim": msid, "batch_idx": rec["batch_idx"], "error": "STALLED",
                        })
                else:
                    print(f"[poll] {msid} status={status} progress={progress}")
                continue

            print(f"[poll] {msid} -> {status}")
            done.append(msid)
            if msid in last_seen:
                del last_seen[msid]
            meta_map = {it["code"]: it for it in rec["batch"]}
            rows = fetch_rows_for_multisim(api, fetcher, msid)
            for r in rows:
                r["dataset"] = meta_map.get(r.get("code"), {}).get("dataset", DATASET)
                r["multisim"] = msid
                r["batch_idx"] = rec["batch_idx"]
                meta = meta_map.get(r.get("code"), {})
                r["decay"] = meta.get("decay")
                r["truncation"] = meta.get("truncation")
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


if __name__ == "__main__":
    main()

