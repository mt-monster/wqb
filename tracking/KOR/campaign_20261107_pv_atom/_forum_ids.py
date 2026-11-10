import json,sys
for i in range(3):
    raw=open(sys.argv[1]+"/_forum"+str(i)+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    res=d.get("results") or d.get("articles") or d.get("posts") or []
    if i==0 and res: print("KEYS:",list(res[0].keys()))
    for a in res:
        t=a.get("title") or ""
        if any(k in t for k in ["隔夜跳空","成交量冲击与隔夜","MAX效应","拉锯战","过度反应","日内动量与隔夜"]):
            aid=a.get("article_id") or a.get("id") or a.get("articleId") or a.get("post_id")
            print(i,"|",aid,"|",t[:75],"| votes",a.get("votes") or a.get("vote_count"))
