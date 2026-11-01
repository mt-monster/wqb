import json, io, sys
p = r"C:\Users\MENGTAO\.minimax\v2\sessions\2026\10\28\14-09-04-319-session_bXZzXzhmNGE4MGI5OTAyZTQwMzFiY2ZlNzcwMTNmMTZjODYy\reports\tool-outputs\dc54a1b992bd4c0943d6a7c3-b83505cff5251eebe90f141e72afb28b8ca09ccbe5e13cdffc14a191e31a0e44.readable.v1.jsonl"
lines = io.open(p, encoding="utf-8").read().splitlines()
chunks = []
for ln in lines:
    ln = ln.strip()
    if not ln:
        continue
    try:
        obj = json.loads(ln)
    except Exception:
        continue
    if isinstance(obj, dict) and "text" in obj:
        chunks.append(obj["text"])
raw = "".join(chunks)
print("RAW_LEN", len(raw))
data, _ = json.JSONDecoder().raw_decode(raw)
post = data.get("post", {})
print("TITLE:", post.get("title"))
body = post.get("body", "")
print("BODY_LEN", len(body))
out = io.open(r"D:\coding\traeCN_project\wqb\reports\_tmp_news18_post_body.txt", "w", encoding="utf-8")
out.write(body)
out.close()
cmts = data.get("comments", [])
print("N_COMMENTS", len(cmts))
buf = []
for c in cmts:
    buf.append("[%s] %s\n%s\n" % (c.get("author"), c.get("date"), c.get("body")))
io.open(r"D:\coding\traeCN_project\wqb\reports\_tmp_news18_post_comments.txt", "w", encoding="utf-8").write("\n".join(buf))
print("OK")