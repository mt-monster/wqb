import json, re, collections, os

p = r"C:\Users\MENGTAO\.minimax\v2\sessions\2026\10\28\14-09-04-319-session_bXZzXzhmNGE4MGI5OTAyZTQwMzFiY2ZlNzcwMTNmMTZjODYy\reports\tool-outputs\270bd3b915467dd111d5aa60-2a95ece12cb22a81a1e9da7f21d4857af20052c5343555091b2afe89cfb7043f.readable.v1.jsonl"

raw = open(p, encoding="utf-8").read()
obj, _ = json.JSONDecoder().raw_decode(raw)
chunks = obj["chunks"] if "chunks" in obj else None
if chunks is None:
    chunks = [json.loads(l) for l in raw.splitlines()[1:] if l.strip()]
chunks.sort(key=lambda c: c.get("index", c.get("byte_offset", 0)))
text = "".join(c["text"] for c in chunks)
data, _ = json.JSONDecoder().raw_decode(text)

res = data["results"]
print("count", data.get("count"), "platform_count", data.get("platform_count"),
      "complete", data.get("complete"))
print("types", collections.Counter(r["type"] for r in res))
print("coverage min/max", min(r["coverage"] for r in res), max(r["coverage"] for r in res))

# prefix / family clustering on id
def fam(fid):
    # strip trailing _fkwN / _N / etc
    s = re.sub(r"_(fkw|fw|m)\d+$", "", fid)
    s = re.sub(r"_\d+$", "", s)
    return s

cnt = collections.Counter(fam(r["id"]) for r in res)
print("\n--- family clusters (top 40) ---")
for k, v in cnt.most_common(40):
    sub = [r for r in res if fam(r["id"]) == k]
    ac = sum(r["alphaCount"] for r in sub)
    uc = max(r["userCount"] for r in sub)
    cov = max(r["coverage"] for r in sub)
    ex = sub[0]["id"]
    print(f"{k:52s} n={v:3d} ac={ac:5d} uc={uc:4d} cov={cov:.4f} ex={ex}")

print("\n--- top 25 by alphaCount ---")
for r in sorted(res, key=lambda x: -x["alphaCount"])[:25]:
    print(f'{r["id"]:50s} {r["type"]:8s} cov={r["coverage"]:.4f} uc={r["userCount"]:4d} ac={r["alphaCount"]:5d}')

print("\n--- 8 sample descriptions ---")
for r in res[:8]:
    print(f'{r["id"]}: {r["description"][:150]}')
