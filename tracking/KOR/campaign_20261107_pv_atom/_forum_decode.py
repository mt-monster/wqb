import json,sys,re,base64,urllib.parse
seen={}
for i in range(3):
    raw=open(sys.argv[1]+"/_forum"+str(i)+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []):
        t=a.get("title") or ""
        if not any(k in t for k in ["隔夜跳空","成交量冲击与隔夜","MAX效应","拉锯战暗藏","过度反应","日内动量与隔夜","渔利"]): continue
        link=a.get("link") or ""
        m=re.search(r"data=([^&]+)", link)
        aid=None
        if m:
            b64=m.group(1).split("--")[0]
            try:
                dec=base64.b64decode(b64+"="*(-len(b64)%4)).decode("utf-8","ignore")
                dec=urllib.parse.unquote(dec)
                pm=re.search(r"posts/(\d+)", dec)
                if pm: aid=pm.group(1)
            except Exception as e: aid=None
        if aid and aid not in seen: seen[aid]=(t,a.get("votes"))
for aid,(t,v) in seen.items(): print(aid,"|",v,"|",t[:72])
