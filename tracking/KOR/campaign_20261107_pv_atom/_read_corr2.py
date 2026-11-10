import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
p=(d.get("checks") or {}).get("production") or {}
print("ZYQ1MNQ8(SLOW_sector) prod max=",p.get("max_correlation"),"pass=",p.get("passes_check"),"status=",p.get("status"))
for b in (p.get("histogram_nonzero") or []):
    if b["range"][0]>=0.6: print(b["range"],"n=",b["n"])
