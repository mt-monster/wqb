import json
d = json.load(open("tracking/KOR/reference/kor_dataset_ranking.json", encoding="utf-8"))
rows = [r for r in d["ranking"] if not r["dead"] and not r["hard_excluded"] and r["usableFieldCount"] >= 8]
rows.sort(key=lambda r: -r["score"])
print("CAND", len(rows))
for r in rows:
    print("%-26s %-14s ac=%-6s cov=%.3f fc=%-5s uf=%-5s uc=%-5s vs=%-4s tier=%s sc=%.3f" % (r["id"], r["category"], r["alphaCount"], r["coverage"], r["fieldCount"], r["usableFieldCount"], r["userCount"], r["valueScore"], r["tier"], r["score"]))