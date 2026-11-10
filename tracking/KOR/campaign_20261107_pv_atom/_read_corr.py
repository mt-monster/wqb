import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
p=(d.get("checks") or {}).get("production") or {}
print("MPY2zXM9 prod max=",p.get("max_correlation"),"pass=",p.get("passes_check"),"status=",p.get("status"))
h=p.get("histogram_nonzero") or []
for b in h:
    if b["range"][0]>=0.6: print(b["range"],"n=",b["n"])
