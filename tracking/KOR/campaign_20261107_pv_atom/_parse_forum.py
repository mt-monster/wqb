import json,sys
for i in range(3):
    raw=open(sys.argv[1]+"/_forum"+str(i)+".json",encoding="utf-8-sig").read()
    s=raw.find("{")
    if s<0: print("q",i,"NOJSON",raw[:80]); continue
    try: d=json.loads(raw[s:])
    except: print("q",i,"PARSEFAIL",raw[:80]); continue
    res=d.get("results") or d.get("articles") or d.get("posts") or []
    print("q",i,"n=",len(res))
    for a in res[:10]:
        print("  ",a.get("article_id") or a.get("id"),"|",(a.get("title") or "")[:70])
