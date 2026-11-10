import json,sys,re
seen=set()
for i in range(3):
    raw=open(sys.argv[1]+"/_forum"+str(i)+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []):
        t=a.get("title") or ""
        if any(k in t for k in ["隔夜跳空","成交量冲击与隔夜","MAX效应","拉锯战暗藏","过度反应","日内动量与隔夜"]):
            link=a.get("link") or ""
            m=re.search(r"(\d{10,})", link)
            aid=m.group(1) if m else link
            if aid in seen: continue
            seen.add(aid)
            print(aid,"|",t[:72],"|",a.get("votes"))
