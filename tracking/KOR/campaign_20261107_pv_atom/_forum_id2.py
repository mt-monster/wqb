import json,sys,re,base64,urllib.parse
for tag in ["MAX","VOL"]:
    raw=open(sys.argv[1]+"/_forum_"+tag+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []):
        t=a.get("title") or ""
        link=a.get("link") or ""
        m=re.search(r"data=([^&]+)",link); aid=None
        if m:
            b64=m.group(1).split("--")[0]
            try:
                dec=urllib.parse.unquote(base64.b64decode(b64+"="*(-len(b64)%4)).decode("utf-8","ignore"))
                pm=re.search(r"posts/(\d+)",dec); aid=pm.group(1) if pm else None
            except: pass
        print(tag,"|",aid,"|",a.get("votes"),"|",t[:70])
