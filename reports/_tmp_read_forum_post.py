import json, re, sys

p = sys.argv[1]
raw = open(p, encoding="utf-8").read()
obj, _ = json.JSONDecoder().raw_decode(raw)
chunks = [json.loads(l) for l in raw.splitlines()[1:] if l.strip()]
chunks.sort(key=lambda c: c.get("index", 0))
text = "".join(c["text"] for c in chunks)
data, _ = json.JSONDecoder().raw_decode(text)
print("TOP KEYS:", list(data.keys()))
post = data.get("post", data)
print("TITLE:", post.get("title"))
d = post.get("details", {})
print("URL:", d.get("url"))
print("VOTES:", d.get("votes"), "DATE:", d.get("date"))
body = post.get("body", "") or ""
print("BODY LEN:", len(body))
for kw in ["insd1", "holdings", "流量", "存量", "tradesignificance", "valueeur", "66", "1.59", "1.53"]:
    idxs = [m.start() for m in re.finditer(re.escape(kw), body)]
    print(f"  kw={kw!r} hits={len(idxs)} first5={idxs[:5]}")
open(r"D:/coding/traeCN_project/wqb/reports/_tmp_forum_43212475386007_body.txt", "w", encoding="utf-8").write(body)
print("saved body to reports/_tmp_forum_43212475386007_body.txt")
