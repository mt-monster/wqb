import json,sys,re,html
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
p=d.get("post") or {}
body=p.get("body") or ""
body=re.sub(r"<[^>]+>"," ",body); body=html.unescape(body); body=re.sub(r"[ \t]+"," ",body)
print("TITLE",p.get("title"))
print(body[:2600])
print("---COMMENTS---")
for c in (d.get("comments") or [])[:4]: print("*",(c.get("body") or "")[:200])
