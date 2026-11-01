import json, io, sys

p = r"C:\Users\MENGTAO\.minimax\v2\sessions\2026\10\28\14-09-04-319-session_bXZzXzhmNGE4MGI5OTAyZTQwMzFiY2ZlNzcwMTNmMTZjODYy\reports\tool-outputs\905e22b1077b686160c859fd-1b4f1f1de5b6e10b9306003b5e305118cfed8b6dc8a64e84aae7c4c60372b475.readable.v1.jsonl"

chunks = []
with io.open(p, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") == "chunk" and isinstance(o.get("text"), str):
            chunks.append((o.get("index", 0), o["text"]))
chunks.sort(key=lambda x: x[0])
raw = "".join(t for _, t in chunks)

data, end = json.JSONDecoder().raw_decode(raw)
if isinstance(data, dict) and "result" in data and "results" not in data:
    data = data["result"]

res = data.get("results", data)
out = []
for i, r in enumerate(res if isinstance(res, list) else [], 1):
    if not isinstance(r, dict):
        continue
    out.append("--- %d ---" % i)
    out.append("TITLE: %s" % (r.get("title") or "")[:220])
    out.append("URL: %s" % (r.get("url") or r.get("link") or ""))
    sn = (r.get("snippet") or r.get("description") or r.get("content") or "")
    out.append("SNIP: %s" % sn[:900])

txt = "\n".join(out)
op = r"D:\coding\traeCN_project\wqb\reports\_tmp_ws_loanfee.txt"
with io.open(op, "w", encoding="utf-8") as f:
    f.write(txt)
print("written", len(txt), "bytes; results:", len(res) if isinstance(res, list) else "n/a")
for line in txt.splitlines():
    print(line)
