import json,sys
want={"6XdNQ1qJ","kqN9MXLd","xAr5oQzN","pwd3kEo3","j2YMamMo","E56xMbaJ"}
for off in [0,100]:
    raw=open(sys.argv[1]+"/_pool_"+str(off)+".json",encoding="utf-8-sig").read()
    d=json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []):
        if a.get("id") in want:
            ra=a.get("ra") or {}; ch=a.get("checks") or {}
            print("==",a["id"],"S",a["metrics"].get("sharpe"),"F",a["metrics"].get("fitness"),"2Y",a["metrics"].get("two_year_sharpe"))
            print("   raF",ra.get("failed_ra_count"),ra.get("ra_failed_checks"))
            print("   settings neut",(a.get("settings") or {}).get("neutralization"),"decay",(a.get("settings") or {}).get("decay"))
            print("   expr",a.get("code"))
