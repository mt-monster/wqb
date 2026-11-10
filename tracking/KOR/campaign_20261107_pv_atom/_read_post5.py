import json,sys,re,html
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
body=(d.get("post") or {}).get("body") or ""
body=re.sub(r"<[^>]+>"," ",body); body=html.unescape(body)
# print from Version 4 onward
i=body.find("Version 4")
print(body[i-200:] if i>=0 else body[-2600])
