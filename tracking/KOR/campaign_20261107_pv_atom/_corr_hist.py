import json, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
p = (d.get("checks") or {}).get("production") or {}
print("max=", p.get("max_correlation"))
for b in (p.get("histogram_nonzero") or []):
    lo, hi = b["range"]
    if lo >= 0.3:
        print(f"[{lo},{hi}) n={b['n']}")
self_c = (d.get("checks") or {}).get("self") or {}
print("self_max=", self_c.get("max_correlation"))
