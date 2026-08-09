# -*- coding: utf-8 -*-
"""Task (a): write task11's 8 re-run IS metrics back into results_glb_first.jsonl.

The original stage1 run reported task11 (fo idx80-87) as a transient ERROR, so
fetch_child_results wrote 8 placeholder records with sharpe=None. The later probe
re-ran those 8 alphas (COMPLETE) and stored the new simulation IDs in
cache/probe_failed_6_11.json (tag task11_idx80-87).

This script:
  1. reads the 8 COMPLETE simulation IDs for task11 from the probe json
  2. fetches authoritative IS metrics (via glb_machine_lib.fetch_child_results)
  3. replaces the 8 placeholder task_no==11 records in results_glb_first.jsonl
     with the 8 real records (matched by expression, idempotent)
"""
import os
import sys
import json
import pickle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_machine_lib import login
from glb_pipeline import fetch_child_results  # reuse the real fetch logic

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "cache")
FO_PKL = os.path.join(CACHE, "stage1_first_order.pkl")
PROBE = os.path.join(CACHE, "probe_failed_6_11.json")
RESULTS = os.path.join(CACHE, "results_glb_first.jsonl")


def main():
    fo = pickle.load(open(FO_PKL, "rb"))
    task11 = fo[80:88]  # (expr, decay) in order

    probe = json.load(open(PROBE))
    t11_tag = next(t for t in probe if t["tag"] == "task11_idx80-87")
    sim_ids = [c["id"] for c in t11_tag["children"]]
    assert len(sim_ids) == 8, f"expected 8 sim ids, got {len(sim_ids)}"
    assert len(task11) == 8

    print(f"Fetching IS metrics for {len(sim_ids)} task11 sims ...")
    s = login()
    real_records = fetch_child_results(s, sim_ids, "glb_first", 11, task11)
    print(f"Fetched {len(real_records)} records")
    for r in real_records:
        ism = r.get("is", {})
        print(f"  sharpe={ism.get('sharpe')}  status={r.get('status')}  "
              f"expr={r.get('expression')[:70]}")

    # Validate we actually got metrics
    ok = [r for r in real_records if r.get("is", {}).get("sharpe") is not None]
    if len(ok) < 8:
        print(f"WARNING: only {len(ok)}/8 records have IS metrics; "
              f"aborting writeback to avoid partial corruption")
        return

    # Merge: drop placeholders (task_no==11, sharpe None) and append real ones
    recs = [json.loads(l) for l in open(RESULTS, encoding="utf-8") if l.strip()]
    before = len(recs)
    placeholders = [r for r in recs
                    if r.get("task_no") == 11 and r.get("is", {}).get("sharpe") is None]
    kept = [r for r in recs if not (r.get("task_no") == 11
                                    and r.get("is", {}).get("sharpe") is None)]
    merged = kept + real_records
    print(f"results lines: before={before}, placeholders removed={len(placeholders)}, "
          f"after={len(merged)}")

    tmp = RESULTS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in merged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, RESULTS)
    print(f"Wrote {len(merged)} records to {RESULTS}")
    print("Task (a) done: task11 IS metrics written back.")


if __name__ == "__main__":
    main()
