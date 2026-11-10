import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
recs=d.get("records") or []
print("years:", [(r["year"], r["longCount"], round(r["pnl"]), r["sharpe"]) for r in recs])
empty=[r["year"] for r in recs if r["longCount"]==0 or r["pnl"]==0]
print("empty_years:", empty or "NONE")
