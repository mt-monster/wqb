import json,sys,re,html
for aid in ["40460201701015","22174527569303","25766755764631"]:
    raw=open(sys.argv[1]+"/_post_"+aid+".json",encoding="utf-8-sig").read()
    s=raw.find("{")
    if s<0: print("==",aid,"NOJSON",raw[:100]); continue
    try: d=json.loads(raw[s:])
    except: print("==",aid,"PARSEFAIL",raw[:100]); continue
    print("\n========",aid,"========")
    # find body/content
    body=d.get("body") or d.get("content") or d.get("article",{}).get("body") or ""
    if not body:
        print("keys",list(d.keys()))
        body=json.dumps(d,ensure_ascii=False)
    body=re.sub(r"<[^>]+>"," ",body); body=html.unescape(body); body=re.sub(r"\s+"," ",body)
    print(body[:1800])
