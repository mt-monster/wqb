import json,sys,collections
for ds in ["behavioral_signals","equity_forum_data"]:
    raw=open(sys.argv[1]+"/_dfout_"+ds+".json",encoding="utf-8-sig").read()
    d=json.loads(raw[raw.find("{"):])
    res=d.get("results") or []
    print(ds, "types=", collections.Counter(f.get("type") for f in res).most_common())
