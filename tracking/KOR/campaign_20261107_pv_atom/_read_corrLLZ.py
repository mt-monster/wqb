import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
ch=d.get("checks") or {}
for k in ["production","self"]:
    p=ch.get(k) or {}
    print(k,"max=",p.get("max_correlation"),"pass=",p.get("passes_check"),"status=",p.get("status"))
print("all_passed=",d.get("all_passed"))
