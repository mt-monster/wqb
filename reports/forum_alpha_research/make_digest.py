import json, re

src = "D:/coding/traeCN_project/wqb/reports/forum_alpha_research/read_posts.json"
out = "D:/coding/traeCN_project/wqb/reports/forum_alpha_research/digest.txt"

data = json.load(open(src, encoding="utf-8"))

def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s

lines = []
for i, p in enumerate(data, 1):
    lines.append(f"\n{'='*80}\n[{i}] {p.get('title')}  (id={p.get('id')}, comments={p.get('n_comments')})\n{'='*80}")
    body = clean(p.get("body") or "")
    lines.append("BODY: " + body)
    # pick top 3 longest comments
    comments = sorted(p.get("comments") or [], key=lambda c: len(c.get("text", "")), reverse=True)
    for j, c in enumerate(comments[:4], 1):
        ct = clean(c.get("text", ""))
        if len(ct) < 40:
            continue
        lines.append(f"  C{j} ({c.get('author')}): {ct}")

open(out, "w", encoding="utf-8").write("\n".join(lines))
print("digest lines:", len(lines), "->", out)
