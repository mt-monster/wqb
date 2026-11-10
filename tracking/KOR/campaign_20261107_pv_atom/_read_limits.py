import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
ch=d.get("checks") or {}
for k in ["fail","warning","pass"]:
    for c in (ch.get(k) or []):
        if isinstance(c,dict) and c.get("name") in ["LOW_SHARPE","LOW_2Y_SHARPE","LOW_FITNESS","LOW_SUB_UNIVERSE_SHARPE"]:
            print(k,"|",c.get("name"),"| value",c.get("value"),"| limit",c.get("limit"))
print("S",d.get("metrics",{}).get("sharpe"),"2Y",d.get("metrics",{}).get("two_year_sharpe"))
