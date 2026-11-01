# -*- coding: utf-8 -*-
"""Parse the externalized get_datasets(GBR) artifact and summarize coverage by category."""
import json
import io
import sys
from collections import defaultdict

ART = (r"C:\Users\MENGTAO\.minimax\v2\sessions\2026\10\28\14-09-04-319-session_bXZzXzhmNGE4MGI5OTAyZTQwMzFiY2ZlNzcwMTNmMTZjODYy"
       r"\reports\tool-outputs\7fb475d9fa0acba589342997-c57552b7dc24eb8d73b5fbd766a7c98330ba524175e0e5a8ca00be31be311fc1.readable.v1.jsonl")

lines = io.open(ART, encoding="utf-8").read().splitlines()
chunks = []
for ln in lines:
    if not ln.strip():
        continue
    obj = json.loads(ln)
    if "text" in obj:
        chunks.append(obj["text"])
raw = "".join(chunks)
data, end = json.JSONDecoder().raw_decode(raw)
print("[INFO] raw chars=%d parsed_end=%d" % (len(raw), end), file=sys.stderr)

# locate results list
cands = []
if isinstance(data, dict):
    for key in ("results", "result", "datasets"):
        v = data.get(key)
        if isinstance(v, list):
            cands = v
            break
        if isinstance(v, dict):
            for k2 in ("results", "datasets"):
                if isinstance(v.get(k2), list):
                    cands = v[k2]
                    break
if not cands and isinstance(data, list):
    cands = data

print("[INFO] dataset count=%d" % len(cands), file=sys.stderr)

by_cat = defaultdict(list)
for d in cands:
    if not isinstance(d, dict):
        continue
    cat = (d.get("category") or "?").lower()
    by_cat[cat].append(d)

rows = []
for cat, items in by_cat.items():
    cov_items = [x for x in items if (x.get("coverage") or 0) > 0.0]
    hi = [x for x in items if (x.get("coverage") or 0) >= 0.60]
    rows.append((cat, len(items), len(cov_items), len(hi)))

rows.sort(key=lambda r: (-r[3], -r[2], r[0]))
print("\n=== GBR/TOP700/D1 dataset coverage by category ===")
print("%-22s %5s %8s %8s" % ("category", "total", "cov>0", "cov>=0.6"))
for cat, tot, covn, hin in rows:
    print("%-22s %5d %8d %8d" % (cat, tot, covn, hin))

print("\n=== datasets with coverage >= 0.60 (sorted by coverage desc) ===")
hi_all = [x for x in cands if isinstance(x, dict) and (x.get("coverage") or 0) >= 0.60]
hi_all.sort(key=lambda x: -(x.get("coverage") or 0))
print("%-30s %-16s %7s %6s %8s %8s" % ("id", "category", "cov", "fields", "alphaCnt", "users"))
for x in hi_all:
    print("%-30s %-16s %7.4f %6s %8s %8s" % (
        x.get("id"), (x.get("category") or "?").lower(), x.get("coverage") or 0,
        x.get("fieldCount"), x.get("alphaCount"), x.get("userCount")))
print("\n[TOTAL] %d datasets with cov>=0.60" % len(hi_all))
